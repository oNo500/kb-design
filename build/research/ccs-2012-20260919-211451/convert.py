"""Convert the pinned ACM XML snapshot with RDFLib; keep source bytes intact."""
from pathlib import Path
from urllib.parse import urljoin
from collections import Counter
from hashlib import sha256
from datetime import datetime, timezone
from importlib.metadata import version
import json

from defusedxml import ElementTree as ET
from rdflib import Graph, Literal, RDF, SKOS, URIRef
from rdflib.compare import isomorphic

base = Path(__file__).resolve().parent
source = json.loads((base / 'source.json').read_text())
raw_path = base / 'acm-ccs2012.original.xml'
raw = raw_path.read_bytes()
if sha256(raw).hexdigest() != source['sha256']:
    raise ValueError('Source snapshot changed; review before converting')
output = base / 'converted'
if output.exists():
    raise ValueError('Output exists; preserve the previous conversion')

ns = {'rdf': str(RDF), 'skos': str(SKOS)}
# ElementTree uses expanded XML names, not RDF URI strings.
about_attr = '{' + str(RDF) + '}about'
resource_attr = '{' + str(RDF) + '}resource'
root = ET.fromstring(raw)
concepts = root.findall('skos:Concept', ns)
labels = [p for c in concepts for p in c.findall('skos:prefLabel', ns)]
old, new = b'<skos:prefLabel lang="en">', b'<skos:prefLabel xml:lang="en">'
if not labels or raw.count(old) != len(labels) or any(p.attrib != {'lang': 'en'} for p in labels):
    raise ValueError('Language attributes differ from reviewed snapshot')
adapted = raw.replace(old, new)
if adapted.replace(new, old) != raw:
    raise ValueError('Unexpected byte change')

# This base is required: the upstream file contains relative node identifiers.
# Keep the full identifier, including all path segments.
base_uri = source['resolved_url']
graph = Graph().parse(data=adapted, format='xml', publicID=base_uri)
expected = Graph()
records = []
schemes = []
for element in root:
    identifier = element.get(about_attr)
    if not identifier or element.tag not in ('{' + str(SKOS) + '}Concept', '{' + str(SKOS) + '}ConceptScheme'):
        raise ValueError('Unexpected node structure')
    subject = URIRef(urljoin(base_uri, identifier))
    expected.add((subject, RDF.type, URIRef(element.tag[1:].replace('}', ''))))
    record = {'id': identifier, 'resolved_iri': str(subject), 'labels': [], 'broader': [], 'narrower': [], 'top_concept_of': []}
    for prop in element:
        predicate = URIRef(prop.tag[1:].replace('}', ''))
        if resource_attr in prop.attrib:
            if set(prop.attrib) != {resource_attr}:
                raise ValueError('Unexpected relation attributes')
            value = URIRef(urljoin(base_uri, prop.get(resource_attr)))
        elif predicate == SKOS.prefLabel and prop.attrib == {'lang': 'en'} and prop.text is not None:
            value = Literal(prop.text, lang=prop.get('lang'))
        else:
            raise ValueError('Unaccounted property: ' + prop.tag)
        expected.add((subject, predicate, value))
        if predicate == SKOS.prefLabel:
            record['labels'].append({'text': prop.text, 'language_attribute': dict(prop.attrib)})
        for relation, key in ((SKOS.broader, 'broader'), (SKOS.narrower, 'narrower'), (SKOS.topConceptOf, 'top_concept_of')):
            if predicate == relation:
                record[key].append(prop.get(resource_attr))
    if element.tag.endswith('}Concept'):
        records.append(record)
    else:
        schemes.append({'id': identifier, 'top_concepts': [p.get(resource_attr) for p in element.findall('skos:hasTopConcept', ns)]})
if set(graph) != set(expected):
    raise ValueError('RDF differs from explicitly accounted XML records')
if len({r['id'] for r in records}) != len(records):
    raise ValueError('Duplicate full identifiers in source')
lookup = {r['id']: r for r in records}
tops = [n for s in schemes for n in s['top_concepts']]
forward = {(r['id'], n) for r in records for n in r['narrower']}
reverse = {(p, r['id']) for r in records for p in r['broader']}
if forward != reverse or any(a not in lookup or b not in lookup for a, b in forward):
    raise ValueError('Hierarchy references require review')

outline, full_tree, visited, depths = [], [], set(), Counter()
def walk(identifier, depth, ancestors):
    if identifier in ancestors:
        raise ValueError('Cycle in source hierarchy')
    record = lookup[identifier]
    text = ' / '.join(x['text'] for x in record['labels'])
    line = '  ' * depth + '- ' + text + ' [' + identifier + ']'
    full_tree.append(line)
    if depth <= 1:
        outline.append(line)
    visited.add(identifier)
    depths[depth + 1] += 1
    for child in record['narrower']:
        walk(child, depth + 1, ancestors | {identifier})
for top in tops:
    walk(top, 0, set())
if visited != set(lookup):
    raise ValueError('Unreachable records need separate representation')

turtle = graph.serialize(format='turtle')
reloaded = Graph().parse(data=turtle, format='turtle')
if not isomorphic(graph, reloaded):
    raise ValueError('Turtle round-trip changed the RDF graph')
if sha256(raw_path.read_bytes()).hexdigest() != source['sha256']:
    raise ValueError('Original file changed')
summary = {
    'source_sha256': source['sha256'], 'converted_at': datetime.now(timezone.utc).isoformat(),
    'base_uri_for_relative_identifiers': base_uri,
    'language_attribute_changes': len(labels), 'language_source': 'original lang=en attribute, not inferred from text',
    'concept_records': len(records), 'concept_schemes': len(schemes), 'top_concepts': len(tops),
    'narrower_edges': len(forward), 'broader_edges': len(reverse), 'depth_counts': dict(sorted(depths.items())),
    'max_depth': max(depths), 'rdf_triples': len(graph),
    'unique_identifier_last_segments': len({r['id'].split('.')[-1] for r in records}),
    'identifier_segments_merged': False,
    'properties': dict(sorted(Counter(str(p) for _, p, _ in graph).items())),
    'checks': {'original_unchanged': True, 'only_declared_byte_adaptation': True,
               'xml_records_match_rdf': True, 'all_hierarchy_endpoints_present': True,
               'broader_narrower_inverse': True, 'all_records_reachable': True,
               'turtle_roundtrip_isomorphic': True},
    'libraries': {'rdflib': version('rdflib'), 'defusedxml': version('defusedxml')},
    'status': 'evaluation_only', 'formal_adoption': False,
}
output.mkdir()
(output / 'acm-ccs2012.adapted.xml').write_bytes(adapted)
(output / 'ccs-2012.ttl').write_text(turtle, encoding='utf-8')
(output / 'source-records.json').write_text(json.dumps({'schemes': schemes, 'concepts': records}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
header = 'ACM CCS 2012 — English labels copied from the official XML. Full path identifiers preserved.\n\n'
(output / '大纲.txt').write_text(header + '\n'.join(outline) + '\n', encoding='utf-8')
(output / '完整分类树.txt').write_text(header + '\n'.join(full_tree) + '\n', encoding='utf-8')
summary['files'] = {p.name: sha256(p.read_bytes()).hexdigest() for p in sorted(output.iterdir()) if p.is_file()}
(output / 'conversion-report.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in summary.items() if k not in ('files', 'properties')}, ensure_ascii=False, indent=2))
print('OUTPUT=' + str(output))
