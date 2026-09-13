"""Project the official MSC2020 tabular export without inferring cross-references."""
import csv
import io
import re
from uuid import NAMESPACE_URL, uuid5

from rdflib import DCTERMS, Graph, Literal, RDF, SKOS, URIRef

SOURCE_URL = 'https://msc2020.org/MSC_2020.csv'
# These are local deterministic identifiers, not identifiers published by MSC.
_ID_NAMESPACE = uuid5(NAMESPACE_URL, 'kb-vocab:msc2020:local-code-mapping:v1')


def _identity(code):
    return URIRef('urn:uuid:' + str(uuid5(_ID_NAMESPACE, code)))


def _parent(code):
    if re.fullmatch(r'[0-9]{2}-XX', code):
        return None
    if re.fullmatch(r'[0-9]{2}(?:[A-Z]xx|-[0-9]{2})', code):
        return code[:2] + '-XX'
    if re.fullmatch(r'[0-9]{2}[A-Z][0-9]{2}', code):
        return code[:3] + 'xx'
    raise ValueError(f'Unrecognized MSC2020 code: {code!r}')


def project_msc(raw, source):
    """Return graph, report, ledger; preserve every source row and description."""
    reader = csv.reader(io.StringIO(raw.decode('cp1252'), newline=''), delimiter='\t', strict=True)
    if next(reader, None) != ['code', 'text', 'description']:
        raise ValueError('MSC2020 needs code/text/description TSV columns')
    rows = {}
    for row_number, values in enumerate(reader, 2):
        if len(values) != 3 or not all(value.strip() for value in values):
            raise ValueError(f'Invalid MSC2020 record at row {row_number}')
        code, label, description = values
        if code in rows:
            raise ValueError(f'Duplicate MSC2020 code {code!r}')
        parent = _parent(code)
        rows[code] = {'code': code, 'text': label, 'description': description,
                      'source_row': row_number, 'parent': parent}
    if not rows:
        raise ValueError('Empty MSC2020 source')
    graph = Graph()
    graph.bind('skos', SKOS)
    graph.bind('dcterms', DCTERMS)
    scheme = _identity('__scheme__')
    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((scheme, SKOS.prefLabel, Literal('2020 Mathematics Subject Classification', lang='en')))
    graph.add((scheme, DCTERMS.source, URIRef(SOURCE_URL)))
    graph.add((scheme, DCTERMS.identifier, Literal('MSC2020')))
    graph.add((scheme, SKOS.note, Literal(
        'Evaluation projection of the official tabular export. URNs are local UUIDv5 identifiers '
        'based on source edition and classification code, not publisher-issued identifiers. '
        'Cross-reference text is preserved without inferred semantic relations.', lang='en')))
    ledger = {'stage': 'evaluation-only', 'source': source, 'entries': [], 'held': [],
              'identity_policy': {'kind': 'local-uuid5-code-mapping', 'namespace': str(_ID_NAMESPACE),
                                  'name': 'exact source code; __scheme__ identifies scheme',
                                  'publisher_issued': False},
              'hierarchy_policy': {
                  'NN-XX': 'top concept', 'NNLxx': 'broader NN-XX',
                  'NN-dd': 'broader NN-XX', 'NNLdd': 'broader NNLxx',
                  'evidence': 'Official MSC2020 PDF pages 1, 3, 4; classification code structure. '
                              'Page 3 distinguishes cross-references from classification placement.'},
              'cross_reference_policy': 'Description retained verbatim; See/For references are not broader/related assertions.'}
    for code, row in sorted(rows.items()):
        node = _identity(code)
        graph.add((node, RDF.type, SKOS.Concept))
        graph.add((node, SKOS.inScheme, scheme))
        graph.add((node, SKOS.notation, Literal(code)))
        graph.add((node, DCTERMS.identifier, Literal(code)))
        graph.add((node, SKOS.prefLabel, Literal(row['text'], lang='en')))
        graph.add((node, DCTERMS.description, Literal(row['description'], lang='en')))
        graph.add((node, DCTERMS.source, URIRef(SOURCE_URL)))
        parent = row['parent']
        if parent is None:
            graph.add((node, SKOS.topConceptOf, scheme))
            graph.add((scheme, SKOS.hasTopConcept, node))
            disposition = 'top_concept'
        elif parent in rows:
            graph.add((node, SKOS.broader, _identity(parent)))
            disposition = 'direct_broader'
        else:
            disposition = 'held'
            ledger['held'].append({'code': code, 'parent': parent, 'reason': 'missing_parent',
                                   'source_row': row['source_row']})
        ledger['entries'].append({**row, 'resource': str(node), 'disposition': disposition})
    report = {'source_kind': 'msc2020', 'stage': 'evaluation-only',
              'counts': {'records': len(rows), 'concepts': len(rows),
                         'broader': len(list(graph.triples((None, SKOS.broader, None)))),
                         'top_concepts': len(list(graph.triples((None, SKOS.topConceptOf, None)))),
                         'held': len(ledger['held'])},
              'limitations': ['Local UUIDv5 identities, not publisher-issued URIs.',
                              'Source text and description are preserved separately; duplicate display labels are not merged.',
                              'Cross-references remain description text, not SKOS semantic relations.',
                              'Evaluation output does not replace the formal project vocabulary.']}
    return graph, report, ledger


def import_msc(source_file, output):
    from kb_vocab.bundles import publish_bundle, read_source
    raw, source = read_source(source_file)
    graph, report, ledger = project_msc(raw, source)
    return publish_bundle(output, graph, report, ledger, source)
