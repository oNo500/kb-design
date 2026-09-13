"""Explicitly adopted Chinese SKOS labels, independent of source snapshots."""
from datetime import date
import hashlib
import json
import re

from rdflib import BNode, DCTERMS, Graph, Literal, RDF, SKOS, URIRef
from rdflib.compare import to_canonical_graph
import yaml

LABEL_PROPERTIES = {SKOS.prefLabel, SKOS.altLabel, SKOS.hiddenLabel}
NODE_TYPES = {SKOS.Concept, SKOS.Collection, SKOS.ConceptScheme}
MODEL_NOTICE = '模型知识 · 第 5 级，外部用法未核实'


def _text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{name} must be nonempty text')
    return value


def label_context(graph, uri):
    """Bind the target identity, English names, and complete local note graphs."""
    node = URIRef(uri)
    if not set(graph.objects(node, RDF.type)) & NODE_TYPES:
        raise ValueError(f'Label target is not an existing SKOS object: {uri}')
    context = Graph()
    for value in graph.objects(node, RDF.type):
        context.add((node, RDF.type, value))
    for prop in LABEL_PROPERTIES:
        for value in graph.objects(node, prop):
            if isinstance(value, Literal) and (value.language or '').lower().split('-')[0] == 'en':
                context.add((node, prop, value))
    pending = []
    for prop in (SKOS.definition, SKOS.scopeNote, DCTERMS.description):
        for value in graph.objects(node, prop):
            context.add((node, prop, value))
            if isinstance(value, (BNode, URIRef)):
                pending.append(value)
    seen = {node}
    while pending:
        subject = pending.pop()
        if subject in seen:
            continue
        seen.add(subject)
        for triple in graph.triples((subject, None, None)):
            context.add(triple)
            if isinstance(triple[2], BNode):
                pending.append(triple[2])
    canonical = to_canonical_graph(context)
    statements = sorted(' '.join(term.n3() for term in triple) + ' .' for triple in canonical)
    raw = ('\n'.join(statements) + '\n').encode()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'statements': statements}


def _basis(value, bibliography):
    if not isinstance(value, dict) or type(value.get('level')) is not int:
        raise ValueError('Label basis needs an explicit level')
    level = value['level']
    if level == 5:
        if set(value) != {'level', 'model'} or not isinstance(value['model'], dict):
            raise ValueError('Model basis must be distinct from external references')
        model = value['model']
        if set(model) != {'name', 'date', 'rationale', 'approval'}:
            raise ValueError('Model basis requires name, date, rationale and approval')
        for key in model:
            _text(model[key], 'model.' + key)
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', model['date']):
            raise ValueError('Model date must use YYYY-MM-DD')
        date.fromisoformat(model['date'])
        return MODEL_NOTICE
    if level not in range(1, 5) or set(value) != {'level', 'references'}:
        raise ValueError('Active labels require external level 1-4 or model level 5')
    references = value['references']
    if not isinstance(references, list) or not references:
        raise ValueError('External basis requires references')
    ids = set()
    for ref in references:
        if not isinstance(ref, dict) or set(ref) != {'source', 'locator'}:
            raise ValueError('External reference requires source and locator')
        source = _text(ref['source'], 'reference source')
        _text(ref['locator'], 'reference locator')
        if source not in bibliography:
            raise ValueError(f'Unregistered label reference: {source}')
        ids.add(source)
    if level == 4 and len(ids) < 2:
        raise ValueError('Level 4 requires at least two distinct registered sources')
    return f'外部依据 · 第 {level} 级'


def apply_labels(graph, ttl_raw, adoptions_raw, bibliography_raw=None):
    """Return a label-only delta and versionable provenance. Never mutate graph."""
    metadata = json.loads(adoptions_raw)
    if (not isinstance(metadata, dict) or set(metadata) != {'schema_version', 'records'}
            or metadata['schema_version'] != 1 or not isinstance(metadata['records'], list)):
        raise ValueError('Expected label adoption schema_version 1 and records')
    bibliography = {}
    if bibliography_raw is not None:
        book = yaml.safe_load(bibliography_raw)
        if not isinstance(book, dict) or book.get('schema_version') != 3 or not isinstance(book.get('references'), list):
            raise ValueError('Expected bibliography schema_version 3')
        for ref in book['references']:
            if not isinstance(ref, dict) or not isinstance(ref.get('id'), str):
                raise ValueError('Invalid bibliography identity')
            if ref['id'] in bibliography:
                raise ValueError('Duplicate bibliography identity')
            bibliography[ref['id']] = ref
    labels = Graph().parse(data=ttl_raw, format='turtle', publicID='urn:kb-vocab:labels:input')
    for subject, prop, value in labels:
        if (not isinstance(subject, URIRef) or prop not in LABEL_PROPERTIES
                or not isinstance(value, Literal) or not str(value).strip()
                or not re.fullmatch(r'zh(?:-[a-z0-9]+)*', (value.language or '').lower())):
            raise ValueError('Chinese label input may contain only Chinese SKOS label triples')
        label_context(graph, str(subject))
        if (subject, prop, value) in graph:
            raise ValueError('Label is already inherited; retain its original editing source')
    active = {}; ids = set(); output = []; contexts = {}
    required = {'id', 'accept', 'uri', 'property', 'language', 'label', 'original', 'basis'}
    for record in metadata['records']:
        if not isinstance(record, dict) or not required.issubset(record) or set(record) - required - {'reason'}:
            raise ValueError('Incomplete or unknown label adoption fields')
        ident = _text(record['id'], 'adoption id')
        if ident in ids or type(record['accept']) is not bool:
            raise ValueError('Adoption IDs must be unique and accept must be boolean')
        ids.add(ident)
        if not record['accept']:
            continue  # Inactive/history records do not acquire any output effect.
        for key in ('uri', 'property', 'language', 'label'):
            _text(record[key], key)
        triple = (URIRef(record['uri']), URIRef(record['property']), Literal(record['label'], lang=record['language']))
        if triple not in labels or triple in active:
            raise ValueError('Accepted record must match one unique active label triple')
        uri = record['uri']
        if uri not in contexts:
            contexts[uri] = label_context(graph, uri)
        if record['original'] != contexts[uri]:
            raise ValueError(f'Label adoption context is stale: {uri}')
        notice = _basis(record['basis'], bibliography)
        active[triple] = record
        output.append(dict(record, notice=notice))
    if set(active) != set(labels):
        raise ValueError('Every Chinese label requires a current accepted record')
    # Validate only affected labels. Full graph/profile checks remain the build gate.
    for subject in set(labels.subjects()):
        values = {prop: set(graph.objects(subject, prop)) | set(labels.objects(subject, prop)) for prop in LABEL_PROPERTIES}
        langs = [(v.language or '').lower() for v in values[SKOS.prefLabel]]
        if len(langs) != len(set(langs)):
            raise ValueError(f'Chinese label conflicts with an existing preferred label: {subject}')
        for a, b in ((SKOS.prefLabel, SKOS.altLabel), (SKOS.prefLabel, SKOS.hiddenLabel), (SKOS.altLabel, SKOS.hiddenLabel)):
            if values[a] & values[b]:
                raise ValueError(f'Label property conflict: {subject}')
    return labels, {'schema_version': 1, 'records': sorted(output, key=lambda row: row['id']),
                    'checks': 'Explicit adoption, current context and registered reference identities. Semantic evidence and human authorization are not independently authenticated.'}
