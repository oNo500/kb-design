"""PhilPapers category-feed projection, preserving third-party provenance."""
import json
from collections import Counter

from rdflib import DCTERMS, Graph, Literal, RDF, SKOS, URIRef

from kb_vocab.validation import validate_graph

SCHEME = URIRef('urn:kb-vocab:philpapers:scheme')
CONTRACT = 'https://philarchive.org/help/api/json.html'


def _identity(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError('category identity must be a positive integer')
    text = str(value)
    if not text.isascii() or not text.isdigit() or int(text) <= 0 or str(int(text)) != text:
        raise ValueError('category identity must be a canonical positive integer')
    return text


def _node(identity):
    return URIRef('urn:kb-vocab:philpapers:category:' + identity)


def project_philpapers(raw, source):
    """Map category parent IDs; primary-parent selection remains in the ledger.

    Root ID 1 is omitted by the official feed contract. Its immediate children
    can be scheme top concepts, but no missing root concept is manufactured.
    The cached upstream revision is unknown; no official-snapshot claim is made.
    """
    data = json.loads(raw)
    if not isinstance(data, list) or not data:
        raise ValueError('category feed must be a nonempty list')
    rows = []
    identities = set()
    for position, row in enumerate(data):
        if not isinstance(row, list) or len(row) != 4:
            raise ValueError(f'category row {position} needs four fields')
        label, identity, parents, primary = row
        identity, primary = _identity(identity), _identity(primary)
        if identity in identities:
            raise ValueError(f'duplicate category identity: {identity}')
        if not isinstance(label, str) or not isinstance(parents, str):
            raise ValueError(f'invalid category label or parent list at row {position}')
        parent_ids = [_identity(value.strip()) for value in parents.split(',')] if parents else []
        identities.add(identity)
        rows.append({'source_row': position, 'id': identity, 'label': label,
                     'parent_ids': parent_ids, 'primary_parent_id': primary, 'raw': row})
    graph = Graph()
    graph.bind('skos', SKOS)
    graph.bind('dcterms', DCTERMS)
    graph.add((SCHEME, RDF.type, SKOS.ConceptScheme))
    graph.add((SCHEME, SKOS.prefLabel, Literal('PhilPapers taxonomy', lang='en')))
    graph.add((SCHEME, SKOS.note, Literal(
        'Evaluation projection of a third-party cached category feed. Upstream version and collection date are unknown; not an adopted vocabulary.', lang='en')))
    graph.add((SCHEME, DCTERMS.description, Literal('Source category-feed field contract: ' + CONTRACT)))
    ledger = {'stage': 'evaluation-only', 'source': source,
              'provenance_status': 'third-party-cache-upstream-version-unknown',
              'field_contract': CONTRACT, 'entries': [], 'relations': [], 'issues': []}
    for row in rows:
        node = _node(row['id'])
        graph.add((node, RDF.type, SKOS.Concept))
        graph.add((node, SKOS.inScheme, SCHEME))
        graph.add((node, DCTERMS.identifier, Literal(row['id'])))
        if row['label'].strip():
            graph.add((node, SKOS.prefLabel, Literal(row['label'], lang='en')))
        else:
            ledger['issues'].append({'code': 'empty_source_label', 'source_id': row['id'],
                                     'policy': 'identity retained without manufactured label'})
        ledger['entries'].append({**row, 'resource': str(node),
                                  'primary_parent_policy': 'source metadata only; all listed parents retained'})
        if row['primary_parent_id'] not in row['parent_ids']:
            ledger['issues'].append({'code': 'primary_parent_not_in_parents',
                                     'source_id': row['id'], 'primary_parent_id': row['primary_parent_id']})
        for parent in row['parent_ids']:
            reason = None
            if parent == row['id']:
                reason = 'self_parent'
            elif parent not in identities:
                reason = 'omitted_source_root' if parent == '1' else 'missing_parent'
            if reason is None:
                graph.add((node, SKOS.broader, _node(parent)))
                graph.add((_node(parent), SKOS.narrower, node))
            elif reason == 'omitted_source_root' and set(row['parent_ids']) == {'1'}:
                graph.add((node, SKOS.topConceptOf, SCHEME))
                graph.add((SCHEME, SKOS.hasTopConcept, node))
            ledger['relations'].append({'source_row': row['source_row'], 'source_id': row['id'],
                                        'target_id': parent, 'source_field': 'parents',
                                        'status': 'held' if reason else 'mapped', 'reason': reason})
    held = Counter(x['reason'] for x in ledger['relations'] if x['status'] == 'held')
    report = {'stage': 'evaluation-only', 'source': source,
              'provenance_status': ledger['provenance_status'],
              'concepts': len(rows), 'broader_relations': len(list(graph.triples((None, SKOS.broader, None)))),
              'multi_parent_concepts': sum(len(set(row['parent_ids'])) > 1 for row in rows),
              'held_relations': dict(held), 'source_issues': ledger['issues'],
              'validation': validate_graph(graph)}
    return graph, report, ledger


def import_philpapers(source_file, output):
    """Verify the source snapshot and publish the isolated evaluation bundle."""
    from kb_vocab.bundles import publish_bundle, read_source
    raw, source = read_source(source_file)
    graph, report, ledger = project_philpapers(raw, source)
    return publish_bundle(output, graph, report, ledger, source)
