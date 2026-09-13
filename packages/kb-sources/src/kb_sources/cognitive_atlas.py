"""Capture official lists and per-record details without interpreting relations."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

import yaml
from kb_sources.download import SourceError, fetch, verify


def detail_files(rows, kind):
    if not isinstance(rows, list) or not rows:
        raise SourceError('Cognitive Atlas requires a nonempty list')
    seen, result = set(), []
    for row in rows:
        identity = row.get('id') if isinstance(row, dict) else None
        if not isinstance(identity, str) or not re.fullmatch(r'[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*', identity) or identity in seen:
            raise SourceError(f'duplicate or invalid Cognitive Atlas ID: {identity}')
        seen.add(identity)
        result.append({'id': identity.replace('_', '-').lower(), 'filename': identity + '.json',
                       'format': 'json', 'url': f'https://www.cognitiveatlas.org/api/v-alpha/{kind}?id={identity}'})
    return sorted(result, key=lambda item: item['filename'])


def validate_detail(value, identity, kind):
    if (not isinstance(value, dict) or value.get('id') != identity or value.get('type') != kind
            or not all(isinstance(value.get(field), list) for field in
                       (['relationships'] if kind == 'concept' else ['concepts', 'contrasts', 'conditions']))):
        raise SourceError(f'incomplete or mismatched {kind} detail: {identity}')


def acquire(manifest, output, workers=4):
    """Resume hash-verified batches; output is a source bundle, not a vocabulary."""
    if not 1 <= workers <= 4:
        raise SourceError('workers must be 1..4')
    root = Path(output).resolve()
    root.mkdir(parents=True, exist_ok=True)
    plans = root / 'manifests'
    plans.mkdir(exist_ok=True)
    snapshots = root / 'snapshots'
    started = datetime.now(timezone.utc).isoformat()

    def receive(path):
        raw = path.read_bytes()
        spec = yaml.safe_load(raw)
        existing = sorted((snapshots / spec['id']).glob('*'))
        for candidate in existing:
            if candidate.name.startswith('.'):
                continue
            receipt = verify(candidate)
            if receipt['request_sha256'] == hashlib.sha256(raw).hexdigest():
                return candidate
        return fetch(path, snapshots, timeout=30, retries=2)

    catalog = receive(Path(manifest))
    planned = []
    counts = {}
    for kind, filename in [('concept', 'concepts.json'), ('task', 'tasks.json')]:
        rows = json.loads((catalog / filename).read_bytes())
        items = detail_files(rows, kind)
        counts[kind] = len(items)
        for offset in range(0, len(items), 50):
            batch_id = f'cognitive-atlas-{kind}-{offset // 50:03d}'
            spec = {'schema_version': 1, 'id': batch_id, 'title': f'Cognitive Atlas {kind} details',
                    'version': 'catalog snapshot ' + catalog.name, 'files': items[offset:offset + 50]}
            path = plans / (batch_id + '.yaml')
            encoded = yaml.safe_dump(spec, sort_keys=False)
            if path.exists() and path.read_text() != encoded:
                raise SourceError('existing plan differs; use a new output directory')
            path.write_text(encoded)
            planned.append((kind, path))

    def capture(item):
        kind, path = item
        snapshot = receive(path)
        receipt = verify(snapshot)
        relations = Counter()
        for entry in receipt['files']:
            value = json.loads((snapshot / entry['filename']).read_bytes())
            validate_detail(value, Path(entry['filename']).stem, kind)
            for relation in value.get('relationships', value.get('concepts', [])):
                relations[str(relation.get('relationship', '<missing>'))] += 1
        print(f'{path.stem}: verified {len(receipt["files"])} details', flush=True)
        return {'kind': kind, 'snapshot': str(snapshot.relative_to(root)),
                'records': len(receipt['files']), 'relationship_occurrences': dict(relations)}

    with ThreadPoolExecutor(max_workers=workers) as pool:
        batches = list(pool.map(capture, planned))
    report = {'status': 'complete_for_catalog', 'started_at': started,
              'finished_at': datetime.now(timezone.utc).isoformat(),
              'catalog': str(catalog.relative_to(root)), 'counts': counts, 'batches': batches,
              'limits': ['Concept and task lists plus every listed detail; other object types not separately enumerated',
                         'Live API is not a transactional or officially versioned snapshot',
                         'Relationships and directions preserved in original JSON; no SKOS conversion or adoption',
                         'Relationship occurrences may include reciprocal and repeated statements']}
    (root / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report


def export_source(bundle, output):
    """Create a hash-recorded transcription for consumers without HTTP dependencies."""
    import os
    import tempfile
    root = Path(bundle).resolve()
    target = Path(output).absolute()
    if target.exists() or root == target.resolve() or root in target.resolve().parents:
        raise SourceError('export requires a new directory outside the source bundle')
    report_bytes = (root / 'report.json').read_bytes()
    report = json.loads(report_bytes)
    if report.get('status') != 'complete_for_catalog':
        raise SourceError('source bundle is incomplete')
    used = []

    def read_snapshot(relative):
        path = (root / relative).resolve()
        if root not in path.parents:
            raise SourceError('snapshot path escapes source bundle')
        receipt = verify(path)
        used.append(path)
        return path, receipt

    catalog, receipt = read_snapshot(report['catalog'])
    expected = {}
    for kind, filename in [('concept', 'concepts.json'), ('task', 'tasks.json')]:
        rows = json.loads((catalog / filename).read_bytes())
        detail_files(rows, kind)
        expected[kind] = {row['id'] for row in rows}
    records, seen = [], {'concept': set(), 'task': set()}
    for batch in report['batches']:
        kind = batch['kind']
        if kind not in seen:
            raise SourceError('unknown detail kind')
        path, receipt = read_snapshot(batch['snapshot'])
        for entry in receipt['files']:
            detail = json.loads((path / entry['filename']).read_bytes())
            identity = Path(entry['filename']).stem
            validate_detail(detail, identity, kind)
            if identity not in expected[kind] or identity in seen[kind]:
                raise SourceError('unexpected or duplicate detail ID')
            seen[kind].add(identity)
            records.append({'kind': kind, 'id': identity, 'detail': detail,
                            'source_url': entry['url'], 'sha256': entry['sha256'],
                            'snapshot': str(path), 'filename': entry['filename']})
    if seen != expected:
        raise SourceError('details do not cover the complete catalogs')
    data = {'representation': 'cognitive-atlas-source-transcription',
            'source': {'bundle': str(root), 'report_sha256': hashlib.sha256(report_bytes).hexdigest()},
            'records': sorted(records, key=lambda row: (row['kind'], row['id']))}
    encoded = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.export-', dir=target.parent) as tmp:
        stage = Path(tmp) / 'result'; stage.mkdir()
        (stage / 'source.json').write_bytes(encoded)
        record = {'source': data['source'], 'outputs': {'source.json': hashlib.sha256(encoded).hexdigest()},
                  'implementation_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        (stage / 'record.json').write_text(json.dumps(record, indent=2) + '\n')
        for path in used:
            verify(path)
        if (root / 'report.json').read_bytes() != report_bytes:
            raise SourceError('source report changed during export')
        if target.exists():
            raise SourceError('output appeared during export')
        os.rename(stage, target)
    return {'output': str(target), 'concepts': len(seen['concept']), 'tasks': len(seen['task'])}
