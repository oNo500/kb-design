"""Verified local inputs and non-overwriting evaluation bundle publication."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from rdflib import Graph
from rdflib.compare import isomorphic
from .validation import validate_graph


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_source(path):
    path = Path(path).absolute()
    raw = path.read_bytes()
    source = {'path': str(path), 'sha256': digest(raw), 'verification': 'local-file-only'}
    receipt_path = path.parent / 'receipt.json'
    if receipt_path.exists():
        receipt_raw = receipt_path.read_bytes()
        receipt = json.loads(receipt_raw)
        if digest(receipt_raw) != path.parent.name:
            raise ValueError('Source receipt does not match snapshot identity')
        entries = [entry for entry in receipt['files'] if entry['filename'] == path.name]
        if len(entries) != 1 or entries[0]['sha256'] != digest(raw) or entries[0]['size'] != len(raw):
            raise ValueError('Source bytes do not match acquisition receipt')
        if digest((path.parent / 'source.yaml').read_bytes()) != receipt['request_sha256']:
            raise ValueError('Source request does not match acquisition receipt')
        source.update(receipt['source'])
        source.update(snapshot_id=path.parent.name, url=entries[0]['final_url'],
                      acquired_at=receipt['acquired_at'], verification='receipt-and-content-verified')
    return raw, source


def publish_bundle(output, graph, report, ledger, source, extras=None, allow_invalid=False):
    output = Path(output).absolute()
    if output.exists():
        raise ValueError(f'Output already exists: {output}')
    if source.get('snapshot_id') and output.resolve().is_relative_to(Path(source['path']).resolve().parent):
        raise ValueError('Output must be outside the source directory')
    validation = validate_graph(graph)
    if not validation['valid'] and not allow_invalid:
        raise ValueError('Projection failed validation; no bundle published')
    report = dict(report, source=source, validation=validation)
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.vocab-', dir=output.parent))
    try:
        graph.serialize(stage / 'vocabulary.ttl', format='turtle')
        restored = Graph().parse(stage / 'vocabulary.ttl', format='turtle')
        if not isomorphic(graph, restored):
            raise ValueError('Turtle round trip changed the RDF graph')
        for filename, value in (('report.json', report), ('mapping-ledger.json', ledger),
                                ('validation.json', validation), ('source.json', source)):
            (stage / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        for filename, raw in (extras or {}).items():
            if Path(filename).name != filename or (stage / filename).exists():
                raise ValueError('Unsafe or reserved extra filename')
            (stage / filename).write_bytes(raw)
        (stage / 'index.md').write_text('# 词表产物\n\n评估产物，不改变正式词表。\n\n'
            '- [Turtle](vocabulary.ttl)\n- [来源](source.json)\n- [报告](report.json)\n'
            '- [映射账本](mapping-ledger.json)\n- [校验结果](validation.json)\n\n'
            + ('当前校验通过。\n' if validation['valid'] else '保留原生来源图；存在未解决的校验问题，详见报告。\n'), encoding='utf-8')
        manifest = {p.name: {'sha256': digest(p.read_bytes()), 'size': p.stat().st_size}
                    for p in sorted(stage.iterdir())}
        (stage / 'manifest.json').write_text(json.dumps({'files': manifest}, indent=2) + '\n')
        if output.exists():
            raise ValueError('Output appeared during publication')
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return report
