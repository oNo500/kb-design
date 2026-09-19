from pathlib import Path
import re, json, hashlib
from collections import Counter
from urllib.parse import urljoin
from defusedxml import ElementTree as ET
from rdflib import Graph, URIRef, Literal, RDF, SKOS
from rdflib.compare import isomorphic

root = Path(__file__).resolve().parent
meta = json.loads((root/'source.json').read_text())
raw = (root/'source.xml').read_bytes()
assert hashlib.sha256(raw).hexdigest() == meta['sha256']
text = raw.decode('utf-8')
ns = {'rdf':str(RDF), 'rdfs':'http://www.w3.org/2000/01/rdf-schema#', 'skos':str(SKOS), 'dc':'http://purl.org/dc/elements/1.1/'}
dtds = re.findall(r'<!DOCTYPE\s+rdf:RDF\s*\[(.*?)\]>', text, re.S)
assert len(dtds) == 1
expected = {k:v for k,v in re.findall(r'<!ENTITY\s+(\w+)\s+"([^"]+)"\s*>',dtds[0])}
assert expected == ns
assert not re.sub(r'<!ENTITY\s+\w+\s+"[^"]+"\s*>', '', dtds[0]).strip()
text = re.sub(r'<!DOCTYPE\s+rdf:RDF\s*\[.*?\]>', '', text, flags=re.S)
for k,v in ns.items(): text = text.replace('&'+k+';',v)
xml = ET.fromstring(text)
base = meta['download_url']
R = '{'+str(RDF)+'}'
LANG = '{http://www.w3.org/XML/1998/namespace}lang'
iri_map = {}
for node in xml.iter():
    for attr in [R+'about', R+'resource']:
        if attr in node.attrib:
            original = node.attrib[attr]
            assert not any(c.isspace() and c != ' ' for c in original)
            adapted = original.replace(' ', '%20')
            if adapted != original:
                iri_map[original] = adapted
                node.set(attr, adapted)
# Only replace exact URI attribute values, preserving all remaining XML text.
for original, adapted in iri_map.items():
    for attr in ['rdf:about', 'rdf:resource']:
        text = text.replace(attr+'="'+original+'"',attr+'="'+adapted+'"')
adapted_bytes = text.encode('utf-8')
(root/'adapted.xml').write_bytes(adapted_bytes)
g = Graph().parse(data=adapted_bytes, format='xml', publicID=base)
# Independent audit of this file's flat XML statements; not a general RDF parser.
expected_graph = Graph()
records = []
counts = Counter()
def iri(tag): return URIRef(tag[1:].replace('}', '', 1))
for node in xml:
    assert set(node.attrib) <= {R+'about', LANG}
    subject = URIRef(urljoin(base, node.attrib[R+'about']))
    expected_graph.add((subject, RDF.type, iri(node.tag)))
    fields = []
    for field in node:
        assert len(field) == 0
        assert set(field.attrib) <= {R+'resource', LANG}
        pred = iri(field.tag)
        if R+'resource' in field.attrib:
            assert not (field.text or '').strip()
            obj = URIRef(urljoin(base,field.attrib[R+'resource']))
            fields.append({'property':str(pred),'resource':str(obj)})
        else:
            lang = field.attrib.get(LANG,node.attrib.get(LANG))
            obj = Literal(field.text or '',lang=lang)
            fields.append({'property':str(pred),'value':str(obj),'language':lang})
        expected_graph.add((subject,pred,obj))
        counts[str(pred)] += 1
    records.append({'source_identifier':node.attrib[R+'about'],'resolved_iri':str(subject),'type':str(iri(node.tag)),'fields':fields})
assert set(g) == set(expected_graph)
g.bind('skos',SKOS)
g.serialize(destination=root/'ccs-2012.ttl',format='turtle',encoding='utf-8')
roundtrip = Graph().parse(root/'ccs-2012.ttl',format='turtle')
assert isomorphic(g,roundtrip)
concepts=set(g.subjects(RDF.type,SKOS.Concept))
schemes=set(g.subjects(RDF.type,SKOS.ConceptScheme))
tops=set(g.objects(next(iter(schemes)),SKOS.hasTopConcept))
dangling=[(str(s),str(p),str(o)) for p in (SKOS.broader,SKOS.narrower,SKOS.related) for s,o in g.subject_objects(p) if s not in concepts or o not in concepts]
inverse_missing=[(str(s),str(o)) for s,o in g.subject_objects(SKOS.broader) if (o,SKOS.narrower,s) not in g]
assert not dangling and not inverse_missing
# Graph traversal retains multiple parents; display repeats are references.
seen=set(); active=set(); cycles=[]; lines=[]
def label(n): return str(next(g.objects(n,SKOS.prefLabel),n))
def visit(n,depth):
    prefix='  '*depth+'- '+label(n)+' ['+str(n).split('#')[-1]+']'
    if n in active:
        cycles.append(str(n)); lines.append(prefix+' [循环引用]'); return
    if n in seen:
        lines.append(prefix+' [已在其他位置展开]'); return
    lines.append(prefix); seen.add(n); active.add(n)
    for child in sorted(g.objects(n,SKOS.narrower),key=label): visit(child,depth+1)
    active.remove(n)
for n in sorted(tops,key=label): visit(n,0)
(root/'分类树.txt').write_text('\n'.join(lines)+'\n')
report={'concepts':len(concepts),'concept_schemes':len(schemes),'top_concepts':len(tops),'triples':len(g),'xml_property_occurrences':dict(counts),'rdf_property_statements':dict(Counter(str(p) for s,p,o in g)),'source_xml_matches_adapted_graph':True,'turtle_roundtrip_isomorphic':True,'dangling_relations':dangling,'missing_broader_inverse':inverse_missing,'hierarchy_cycles':cycles,'unreachable_concepts':sorted(map(str,concepts-seen)),'multiple_parent_concepts':sum(len(set(g.objects(c,SKOS.broader)))>1 for c in concepts),'base_iri':base,'base_policy':'Pinned source document URL resolves source fragment IDs; snapshot identifiers, not official persistent concept IRIs.','iri_adaptations':iri_map,'source_sha256':meta['sha256'],'turtle_sha256':hashlib.sha256((root/'ccs-2012.ttl').read_bytes()).hexdigest(),'semantic_quality_reviewed':False,'pipeline_activated':False}
for name,data in [('conversion-report.json',report),('source-records.json',records)]:
    (root/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
assert hashlib.sha256((root/'source.xml').read_bytes()).hexdigest()==meta['sha256']
print(json.dumps(report,ensure_ascii=False,indent=2))
