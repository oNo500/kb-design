"""Immutable combined entity vocabulary with preserved identities and source states."""
from collections import defaultdict
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile

from rdflib import BNode, Graph, Literal, RDF, SKOS, URIRef
from rdflib.namespace import OWL
from rdflib.compare import to_canonical_graph

from .diff import canonical_bytes, parse_turtle
from .edit import NAME_RULES, ROLES, XL, _check_names, _iri

KIND_CLASSES = {
    'person': 'http://www.wikidata.org/entity/Q5',
    'organization': 'http://www.wikidata.org/entity/Q43229',
    'software': 'http://www.wikidata.org/entity/Q7397',
    'programming-language': 'http://www.wikidata.org/entity/Q9143',
    'large-language-model': 'http://www.wikidata.org/entity/Q115305900',
}


def _json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def _json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique)


def _relative(value):
    if not isinstance(value, str) or not value or '\\' in value:
        raise ValueError('Expected a relative source path')
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ('', '.', '..') for part in value.split('/')):
        raise ValueError(f'Unsafe relative path: {value}')
    return path


def _digest(value):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value):
        raise ValueError('Expected a SHA-256 hash')
    return value


def _plain_path(path):
    path = Path(path).absolute()
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError(f'Path contains a symbolic link: {path}')
    return path.resolve()


def _read_pinned(path, expected):
    path = _plain_path(path)
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != _digest(expected):
        raise ValueError(f'Source sha256 hash differs: {path}')
    return raw


def _file_set(directory, names):
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError(f'Invalid delivery directory: {directory}')
    expected_dirs = {str(parent) for name in names for parent in PurePosixPath(name).parents if str(parent) != '.'}
    files, directories = set(), set()
    for path in directory.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Delivery contains a symbolic link: {path}')
        relative = path.relative_to(directory).as_posix()
        if path.is_file():
            files.add(relative)
        elif path.is_dir():
            directories.add(relative)
        else:
            raise ValueError(f'Delivery contains a special file: {path}')
    if files != set(names) or directories != expected_dirs:
        raise ValueError(f'Delivery has an incomplete or extra file set: {directory}')


def _configuration(raw):
    document = _json(raw)
    if (not isinstance(document, dict) or set(document) != {'schema_version', 'policy', 'authority', 'sources'}
            or document['schema_version'] != 1 or document['policy'] != 'basic-fields-v1'):
        raise ValueError('Unsupported entity build configuration')
    authority = document['authority']
    if not isinstance(authority, dict) or set(authority) != {'path', 'sha256'}:
        raise ValueError('Authority requires a pinned path and sha256')
    _relative(authority['path'])
    _digest(authority['sha256'])
    if not isinstance(document['sources'], list) or not document['sources']:
        raise ValueError('At least one pinned entity source is required')
    keys = set()
    for item in document['sources']:
        required = {'key', 'directory', 'manifest_sha256', 'entity_file'}
        if not isinstance(item, dict) or not required <= set(item) or set(item) - required - {'audit_file'}:
            raise ValueError('Invalid entity source configuration')
        key = item['key']
        if not isinstance(key, str) or not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', key) or key in keys:
            raise ValueError('Source keys must be unique lowercase identifiers')
        keys.add(key)
        for field in ('directory', 'entity_file', 'audit_file'):
            if field in item:
                _relative(item[field])
        _digest(item['manifest_sha256'])
    return document


def _source_inputs(document, context_raw):
    context = _json(context_raw)
    if (not isinstance(context, dict) or set(context) != {'schema_version', 'source_root'}
            or context['schema_version'] != 1 or not isinstance(context['source_root'], str)):
        raise ValueError('Invalid frozen build context')
    root = Path(context['source_root'])
    # No filesystem lookup: frozen deliveries remain verifiable after copying.
    if not root.is_absolute() or str(root) != context['source_root'] or '..' in root.parts:
        raise ValueError('Frozen source root must be a normalized absolute path')
    return {item['key']: {**item, 'public_id': (root / item['directory'] / item['entity_file']).as_uri()}
            for item in document['sources']}


def _source_states(manifest, item, files):
    if 'audit_file' in item:
        audit = _json(files[item['audit_file']])
        rows = audit.get('records')
        if not isinstance(rows, list):
            raise ValueError('Entity audit must explicitly identify entity records')
        states = {}
        for index, row in enumerate(rows):
            if not isinstance(row, dict) or not isinstance(row.get('id'), str) or row['id'] in states:
                raise ValueError('Entity audit has an invalid or duplicate identity')
            states[row['id']] = (row, f"{item['audit_file']}#/records/{index}")
        return states
    identities, states = manifest.get('entity_iris'), manifest.get('source_states')
    if (not isinstance(identities, list) or any(not isinstance(iri, str) for iri in identities)
            or len(identities) != len(set(identities)) or not isinstance(states, dict)
            or set(identities) != set(states) or any(not isinstance(row, dict) for row in states.values())):
        raise ValueError('Source manifest must explicitly identify entities and original states')
    return {iri: (states[iri], 'manifest.json#/source_states/' + iri.replace('~', '~0').replace('/', '~1'))
            for iri in identities}


def _closure(graph, subject):
    result, pending, seen = Graph(), [subject], set()
    while pending:
        node = pending.pop()
        if node in seen:
            continue
        seen.add(node)
        for triple in graph.triples((node, None, None)):
            result.add(triple)
            value = triple[2]
            if isinstance(value, (BNode, URIRef)) and any(graph.triples((value, None, None))):
                pending.append(value)
    return canonical_bytes(result)


def _name_check(graph):
    # Only this temporary graph gets entailed projections. The delivered graph
    # retains exactly the source statements, including missing/empty names.
    check = graph + Graph()
    incomplete = []
    labels = set(graph.subjects(RDF.type, XL.Label)) | set(graph.subjects(XL.literalForm, None))
    for role in ROLES:
        labels.update(graph.objects(None, role))
    for label in labels:
        forms = list(graph.objects(label, XL.literalForm))
        if len(forms) > 1:
            raise ValueError(f'XL literalForm conflict: {label}')
        complete = (isinstance(label, URIRef) and (label, RDF.type, XL.Label) in graph and len(forms) == 1
                    and isinstance(forms[0], Literal) and bool(str(forms[0]).strip()))
        if not complete:
            incomplete.append({'label': str(label), 'reason': 'missing stable Label IRI, explicit type or one nonempty literalForm',
                               'subjects': sorted({str(subject) for role in ROLES for subject in graph.subjects(role, label)})})
            check.remove((label, RDF.type, XL.Label))
            check.remove((label, XL.literalForm, None))
            for role in ROLES:
                check.remove((None, role, label))
    for role, plain in ROLES.items():
        for subject, value in list(check.subject_objects(plain)):
            if isinstance(value, Literal) and not str(value).strip():
                check.remove((subject, plain, value))
        for subject in set(check.subjects(role, None)):
            # Existing projections must match; do not repair conflicting input.
            if not any(graph.objects(subject, plain)):
                for label in check.objects(subject, role):
                    for form in check.objects(label, XL.literalForm):
                        check.add((subject, plain, form))
    _check_names(check)
    return sorted(incomplete, key=lambda row: row['label'])


def _preferred(graph, subject):
    values = set(graph.objects(subject, SKOS.prefLabel))
    for label in graph.objects(subject, XL.prefLabel):
        forms = list(graph.objects(label, XL.literalForm))
        if isinstance(label, URIRef) and (label, RDF.type, XL.Label) in graph and len(forms) == 1:
            values.add(forms[0])
    return {value for value in values if isinstance(value, Literal) and str(value).strip()}


def _assemble(document, files, inputs):
    graph, graphs, declarations = Graph(), [], defaultdict(list)
    for item in document['sources']:
        key = item['key']
        source_files = {name.removeprefix(f'sources/{key}/'): raw for name, raw in files.items() if name.startswith(f'sources/{key}/')}
        manifest = _json(source_files['manifest.json'])
        original = parse_turtle(source_files[item['entity_file']], public_id=inputs[key]['public_id'])
        # Blank nodes in separate source documents have separate scopes.
        nodes = {node: BNode() for triple in original for node in triple if isinstance(node, BNode)}
        isolated = Graph()
        for triple in original:
            isolated.add(tuple(nodes.get(node, node) for node in triple))
        duplicate_graph = False
        for prior_key, prior in graphs:
            if canonical_bytes(prior) == canonical_bytes(isolated):
                duplicate_graph = True
                continue
            shared = {s for s in prior.subjects() if isinstance(s, URIRef)} & {s for s in isolated.subjects() if isinstance(s, URIRef)}
            for subject in sorted(shared, key=str):
                if _closure(prior, subject) != _closure(isolated, subject):
                    raise ValueError(f'IRI conflict between {prior_key} and {key}: {subject}')
                if any(isinstance(value, BNode) for triple in parse_turtle(_closure(isolated, subject)) for value in triple):
                    raise ValueError(f'IRI conflict needs explicit handling of shared blank-node closure: {subject}')
        graphs.append((key, isolated))
        if not duplicate_graph:
            graph += isolated
        for iri, (state, pointer) in _source_states(manifest, item, source_files).items():
            declarations[iri].append({'key': key, 'entity_file': f'sources/{key}/{item["entity_file"]}',
                                      'record': f'sources/{key}/{pointer}', 'state': state})
    # Diagnostics must refer to canonical blank nodes, never parser/random IDs.
    graph = to_canonical_graph(graph)
    incomplete_names = _name_check(graph)
    incomplete_users = {iri for row in incomplete_names for iri in row['subjects']}
    records, names = {}, defaultdict(set)
    known_classes = set(KIND_CLASSES.values())
    for iri, sources in sorted(declarations.items()):
        try:
            subject = _iri(iri)
            stable = True
        except ValueError:
            subject, stable = URIRef(iri), False
        classes = sorted(str(value) for value in graph.objects(subject, RDF.type) if str(value) in known_classes)
        preferred = _preferred(graph, subject)
        incompatible = any((subject, RDF.type, cls) in graph for cls in (SKOS.Concept, SKOS.ConceptScheme, SKOS.Collection, SKOS.OrderedCollection, XL.Label))
        checks = {'stable_iri': stable, 'category': len(classes) == 1 and not incompatible,
                  'preferred_name': bool(preferred), 'source': bool(sources)}
        reasons = [name for name, passed in checks.items() if not passed]
        if iri in incomplete_users:
            reasons.append('incomplete_xl_name')
        if (any(source['state'].get('status') == 'deprecated' for source in sources)
                or any(isinstance(value, Literal) and value.toPython() is True for value in graph.objects(subject, OWL.deprecated))):
            reasons.append('deprecated')
        diagnostics = ['preferred_name_without_language'] if any(not value.language for value in preferred) else []
        records[iri] = {'sources': sources, 'basic_fields': checks, 'class_iris': classes,
                        'preferred_names': sorted(value.n3() for value in preferred),
                        'eligible': not reasons, 'ineligible_reasons': reasons, 'diagnostics': diagnostics}
        for value in preferred:
            names[(str(value), (value.language or '').lower())].add(iri)
    turtle = canonical_bytes(graph)
    files['entities.ttl'] = turtle
    manifest = {'schema_version': 1, 'operation': 'unified-entities-build', 'policy': document['policy'],
                'formal_release': False, 'consumer_activated': False,
                'authority': document['authority'], 'sources': inputs,
                'entities': records, 'entity_iris': sorted(records),
                'eligible_entity_iris': [iri for iri, row in records.items() if row['eligible']],
                'ineligible': {iri: row['ineligible_reasons'] for iri, row in records.items() if not row['eligible']},
                'same_name_candidates': [{'text': text, 'language': language or None, 'entity_iris': sorted(iris)}
                                         for (text, language), iris in sorted(names.items()) if len(iris) > 1],
                'validation': {'incomplete_xl_names': incomplete_names, 'checked': ['pinned source manifests and complete file hashes', 'shared IRI subject and closure equality', *NAME_RULES],
                               'name_check_view': 'Only the validation graph adds SKOS-XL entailed ordinary labels. Incomplete XL names are excluded from that partial conflict check, retained verbatim in RDF, reported here, and block all referring entities. This does not certify complete input-graph conformance.',
                               'not_checked': ['external facts', 'semantic identity between different IRIs', 'authority validity', 'full-graph SHACL']},
                'graph_sha256': sha256(turtle).hexdigest(),
                'files': {name: sha256(raw).hexdigest() for name, raw in sorted(files.items())}}
    files['manifest.json'] = _json_bytes(manifest)
    return manifest


def _verify_output(output, files):
    _file_set(output, files)
    for name, raw in files.items():
        if (output / name).read_bytes() != raw:
            raise ValueError(f'Existing output delivery differs or is damaged: {name}')


def build_entities(config: Path, source_root: Path, output: Path) -> dict:
    """Freeze all source files and combine explicitly identified entity records."""
    config, source_root, output = _plain_path(config), _plain_path(source_root), _plain_path(output)
    config_raw = config.read_bytes()
    document = _configuration(config_raw)
    authority_path = source_root / document['authority']['path']
    authority_raw = _read_pinned(authority_path, document['authority']['sha256'])
    context_raw = _json_bytes({'schema_version': 1, 'source_root': str(source_root)})
    files = {'config.json': config_raw, 'authority.md': authority_raw, 'build-context.json': context_raw}
    pinned = {config: config_raw, authority_path: authority_raw}
    inputs, source_sets = _source_inputs(document, context_raw), {}
    for item in document['sources']:
        directory = _plain_path(source_root / item['directory'])
        if output == directory or output in directory.parents or directory in output.parents:
            raise ValueError('The output must be separate from every source directory')
        raw = _read_pinned(directory / 'manifest.json', item['manifest_sha256'])
        manifest = _json(raw)
        hashes = manifest.get('files')
        if not isinstance(hashes, dict) or not hashes or 'manifest.json' in hashes:
            raise ValueError('Source manifest requires a complete nonrecursive file hash map')
        for name, digest in hashes.items():
            _relative(name)
            _digest(digest)
        if item['entity_file'] not in hashes or ('audit_file' in item and item['audit_file'] not in hashes):
            raise ValueError('Source entity data and audit must be manifest-pinned')
        names = set(hashes) | {'manifest.json'}
        _file_set(directory, names)
        source_sets[directory] = names
        source_files = {'manifest.json': raw}
        for name, digest in hashes.items():
            source_files[name] = _read_pinned(directory / name, digest)
        for name, content in source_files.items():
            pinned[directory / name] = content
            files[f'sources/{item["key"]}/{name}'] = content
    if any(path == output or output in path.parents for path in pinned):
        raise ValueError('The output cannot contain any input')
    manifest = _assemble(document, files, inputs)
    def unchanged():
        for directory, names in source_sets.items():
            _file_set(directory, names)
        for path, raw in pinned.items():
            if _plain_path(path).read_bytes() != raw:
                raise ValueError(f'Source changed during entity build: {path}')
    unchanged()
    if output.exists():
        _verify_output(output, files)
        return manifest
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f'.{output.name}-', dir=output.parent))
    try:
        for name, raw in files.items():
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        unchanged()
        _plain_path(output)
        if output.exists():
            raise ValueError('Output appeared during entity build')
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return manifest


def validate_delivery(output: Path) -> dict:
    """Verify full delivery bytes and rebuild the manifest from frozen originals."""
    output = _plain_path(output)
    manifest = _json((output / 'manifest.json').read_bytes())
    if manifest.get('operation') != 'unified-entities-build' or not isinstance(manifest.get('files'), dict):
        raise ValueError('Not a unified entity delivery')
    files = {}
    for name, digest in manifest['files'].items():
        _relative(name)
        files[name] = _read_pinned(output / name, digest)
    _file_set(output, set(files) | {'manifest.json'})
    if not {'config.json', 'authority.md', 'build-context.json'} <= set(files):
        raise ValueError('Delivery lacks frozen build inputs; rebuild into a new version directory')
    document = _configuration(files['config.json'])
    inputs = _source_inputs(document, files['build-context.json'])
    if manifest.get('sources') != inputs:
        raise ValueError('Source metadata differs from frozen configuration and build context')
    if sha256(files['authority.md']).hexdigest() != document['authority']['sha256']:
        raise ValueError('Authority hash differs in delivery')
    originals = {name: files[name] for name in ('config.json', 'authority.md', 'build-context.json')}
    for item in document['sources']:
        prefix = f'sources/{item["key"]}/'
        raw = files[prefix + 'manifest.json']
        if sha256(raw).hexdigest() != item['manifest_sha256']:
            raise ValueError('Source manifest hash differs in delivery')
        hashes = _json(raw)['files']
        for name, digest in hashes.items():
            _relative(name)
            if sha256(files[prefix + name]).hexdigest() != _digest(digest):
                raise ValueError('Source file hash differs in delivery')
            originals[prefix + name] = files[prefix + name]
        originals[prefix + 'manifest.json'] = raw
    expected = _assemble(document, originals, inputs)
    if expected != manifest:
        raise ValueError('Delivery metadata differs from preserved source records')
    _verify_output(output, originals)
    return manifest


def set_current(output: Path, current: Path) -> None:
    """Atomically replace only a symlink after validating the immutable target."""
    output = _plain_path(output)
    validate_delivery(output)
    current = Path(current).absolute()
    _plain_path(current.parent)
    if current == output or output in current.parents or current in output.parents:
        raise ValueError('Current pointer must be outside the delivery')
    if current.exists() and not current.is_symlink():
        raise ValueError('Current must be absent or an existing symbolic link')
    current.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix='.entity-current-', dir=current.parent)
    os.close(descriptor)
    temporary = Path(temporary)
    try:
        temporary.unlink()
        temporary.symlink_to(os.path.relpath(output, current.parent), target_is_directory=True)
        if current.exists() and not current.is_symlink():
            raise ValueError('Current became a regular file or directory')
        os.replace(temporary, current)
    finally:
        temporary.unlink(missing_ok=True)
