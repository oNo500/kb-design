"""Full-data generation must preserve sources and never guess memberships."""
import hashlib
import importlib
import json
from pathlib import Path
import tempfile
import unittest
from rdflib import Graph, RDF, SKOS, URIRef
from rdflib.compare import isomorphic


class SystemBuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        raw='''@prefix s: <http://www.w3.org/2004/02/skos/core#> .
<urn:a> a s:Concept ; s:prefLabel "A"@en .
<urn:b> a s:Concept ; s:prefLabel "B"@en ; s:broader <urn:a>, <urn:outside> .
<urn:outside> a s:Concept ; s:prefLabel "Outside"@en .
<urn:unlabelled> a s:Concept .
<urn:collection> a s:Collection ; s:prefLabel "Collection"@en ; s:member <urn:a> .
<urn:task> a <urn:Task> ; <urn:description> "not a concept" .
'''
        (self.root/'a.ttl').write_text(raw)
        (self.root/'b.ttl').write_text('@prefix s: <http://www.w3.org/2004/02/skos/core#> . <urn:other> a s:Concept ; s:prefLabel "A"@en .')
        (self.root/'catalog.json').write_text(json.dumps({'sources':[{'name':n,'file':n+'.ttl'} for n in ('a','b')]}))
        self.config={'schema_version':2,'catalog':'catalog.json',
         'languages':['en','zh'],'shapes':str(Path(__file__).resolve().parents[3]/'data/inputs/vocabulary/shapes.ttl'),
         'vocabulary':{'uri':'urn:kb-vocab:scheme:test-vocabulary','label':{'en':'Test vocabulary'},'scope':{'en':'Fixture topics only.'},'top_concepts':[]},
         'sources':{n:hashlib.sha256((self.root/(n+'.ttl')).read_bytes()).hexdigest() for n in ('a','b')},
         'domains':[{'id':'test','label':{'en':'Test'},'whole_sources':[],
                     'branches':[{'source':'a','uri':'urn:collection','mode':'inherit'},
                                 {'source':'b','uri':'urn:other','mode':'reference_only'}],
                     'uri':'urn:kb-vocab:group:test'}]}
        self.path=self.root/'config.json';self.save()

    def save(self): self.path.write_text(json.dumps(self.config))
    def api(self):
        try:return importlib.import_module('kb_vocab.system_build').build_system
        except ModuleNotFoundError:self.fail('full system builder is not implemented')

    def test_full_sources_retained_membership_does_not_rewrite_hierarchy(self):
        build=self.api();out=self.root/'out';build(self.path,out)
        graph=Graph().parse(out/'vocabulary.ttl',format='turtle')
        before=Graph().parse(self.root/'a.ttl',format='turtle')+Graph().parse(self.root/'b.ttl',format='turtle')
        self.assertTrue(set(before).issubset(set(graph)))
        scheme=URIRef('urn:kb-vocab:scheme:test-vocabulary')
        group=URIRef('urn:kb-vocab:group:test')
        self.assertEqual(set(graph.subjects(RDF.type,SKOS.ConceptScheme)),{scheme})
        self.assertEqual(set(graph.objects(group,SKOS.member)),{URIRef('urn:a'),URIRef('urn:b')})
        self.assertIn((URIRef('urn:unlabelled'),SKOS.inScheme,scheme),graph)
        self.assertIn((URIRef('urn:other'),SKOS.inScheme,scheme),graph)
        self.assertEqual(set(graph.objects(URIRef('urn:b'),SKOS.broader)),{URIRef('urn:a'),URIRef('urn:outside')})
        domain=Graph().parse(out/'domains/test.ttl',format='turtle')
        self.assertEqual(set(domain.objects(group,SKOS.member)),{URIRef('urn:a'),URIRef('urn:b')})
        self.assertIn((URIRef('urn:outside'),RDF.type,SKOS.Concept),domain)
        coverage=json.loads((out/'coverage.json').read_text())
        self.assertEqual({r['uri'] for r in coverage},{'urn:a','urn:b','urn:outside','urn:unlabelled','urn:other'})
        self.assertIn((URIRef('urn:task'),RDF.type,URIRef('urn:Task')),graph)

    def test_pinned_source_change_and_existing_output_are_rejected(self):
        build=self.api();out=self.root/'out';build(self.path,out)
        before=(out/'vocabulary.ttl').read_bytes()
        with self.assertRaises(ValueError):build(self.path,out)
        self.assertEqual((out/'vocabulary.ttl').read_bytes(),before)
        (self.root/'a.ttl').write_text((self.root/'a.ttl').read_text()+'\n<urn:new> a <urn:Type> .')
        with self.assertRaisesRegex(ValueError,'hash|fingerprint|SHA'):build(self.path,self.root/'changed')
        self.assertFalse((self.root/'changed').exists())

    def test_rebuild_preserves_identity_and_graph_semantics(self):
        build=self.api();build(self.path,self.root/'one');build(self.path,self.root/'two')
        self.assertTrue(isomorphic(Graph().parse(self.root/'one/vocabulary.ttl'),Graph().parse(self.root/'two/vocabulary.ttl')))

    def test_same_label_is_not_merged_and_whole_source_includes_unlabelled(self):
        build=self.api();self.config['domains'][0]['whole_sources']=['a','b'];self.save()
        out=self.root/'out';build(self.path,out);g=Graph().parse(out/'vocabulary.ttl')
        members=set(g.objects(URIRef('urn:kb-vocab:group:test'),SKOS.member))
        self.assertIn(URIRef('urn:a'),members);self.assertIn(URIRef('urn:other'),members)
        self.assertIn(URIRef('urn:unlabelled'),members)
        self.assertEqual(set(g.triples((None,SKOS.exactMatch,None))),set())

    def test_language_filter_keeps_identity_and_byte_exact_sources(self):
        build=self.api()
        path=self.root/'a.ttl'
        path.write_text(path.read_text()+'\n<urn:a> <http://www.w3.org/2004/02/skos/core#altLabel> "阿"@zh-Hans, "Autre"@fr .\n')
        self.config['sources']['a']=hashlib.sha256(path.read_bytes()).hexdigest();self.save()
        out=self.root/'out';report=build(self.path,out)
        g=Graph().parse(out/'vocabulary.ttl')
        self.assertTrue(all(not getattr(o,'language',None) or o.language.lower().split('-')[0] in {'en','zh'} for _,_,o in g))
        self.assertIn((URIRef('urn:a'),RDF.type,SKOS.Concept),g)
        self.assertTrue(any(getattr(o,'language',None)=='zh-Hans' for o in g.objects(URIRef('urn:a'),SKOS.altLabel)))
        provenance=json.loads((out/'provenance.json').read_text())
        self.assertEqual((out/provenance['sources']['a']['copy']).read_bytes(),path.read_bytes())
