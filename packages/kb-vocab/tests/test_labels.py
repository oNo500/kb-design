"""Only current, explicitly adopted labels may change a published graph."""
import copy
import importlib
import json
import unittest
from rdflib import Graph, Literal, SKOS, URIRef

class LabelsTests(unittest.TestCase):
    def setUp(self):
        self.g=Graph().parse(data='''@prefix s: <http://www.w3.org/2004/02/skos/core#> .
<urn:a> a s:Concept ; s:prefLabel "A"@en ; s:scopeNote "Scope A"@en .
<urn:b> a s:Concept ; s:prefLabel "A"@en ; s:scopeNote "Different scope"@en .''',format='turtle')
    def api(self):
        try:return importlib.import_module('kb_vocab.labels')
        except ModuleNotFoundError:self.fail('shared label adoption gate is missing')
    def inputs(self):
        api=self.api();rec={'id':'fixture-adoption','accept':True,'uri':'urn:a','property':str(SKOS.prefLabel),'language':'zh','label':'甲',
            'original':api.label_context(self.g,'urn:a'),
            'basis':{'level':5,'model':{'name':'fixture-model','date':'2026-09-13','rationale':'Synthetic test only','approval':'fixture authorization'}}}
        ttl=b'@prefix s: <http://www.w3.org/2004/02/skos/core#> . <urn:a> s:prefLabel "\xe7\x94\xb2"@zh .'
        return api,ttl,{'schema_version':1,'records':[rec]}
    def test_adoption_adds_only_exact_label_and_preserves_source(self):
        api,ttl,records=self.inputs();before=set(self.g)
        delta,provenance=api.apply_labels(self.g,ttl,json.dumps(records).encode(),None)
        self.assertEqual(set(delta),{(URIRef('urn:a'),SKOS.prefLabel,Literal('甲',lang='zh'))})
        self.assertEqual(set(self.g),before);self.assertIn('外部用法未核实',provenance['records'][0]['notice'])
    def test_missing_withdrawn_stale_or_wrong_concept_adoption_is_rejected(self):
        api,ttl,records=self.inputs()
        for change in ('missing','withdrawn','scope','target','english'):
            with self.subTest(change=change):
                data=copy.deepcopy(records);g=Graph()+self.g
                if change=='missing':data['records']=[]
                if change=='withdrawn':data['records'][0]['accept']=False
                if change=='scope':g.set((URIRef('urn:a'),SKOS.scopeNote,Literal('Changed',lang='en')))
                if change=='english':g.set((URIRef('urn:a'),SKOS.prefLabel,Literal('Renamed',lang='en')))
                if change=='target':data['records'][0]['uri']='urn:b'
                with self.assertRaises(ValueError):api.apply_labels(g,ttl,json.dumps(data).encode(),None)
    def test_semantic_statements_and_inherited_names_cannot_be_overridden(self):
        api,ttl,records=self.inputs()
        for extra in (b'<urn:a> <http://www.w3.org/2004/02/skos/core#broader> <urn:b> .',
                      b'<urn:a> <http://www.w3.org/2004/02/skos/core#prefLabel> "NEW"@en .'):
            with self.assertRaises(ValueError):api.apply_labels(self.g,ttl+extra,json.dumps(records).encode(),None)
        self.g.add((URIRef('urn:a'),SKOS.prefLabel,Literal('已有中文',lang='zh')))
        with self.assertRaises(ValueError):api.apply_labels(self.g,ttl,json.dumps(records).encode(),None)
    def test_external_basis_requires_registered_references_and_level_four_independence(self):
        api,ttl,records=self.inputs();records['records'][0]['basis']={'level':4,'references':[{'source':'fixture','locator':'p1'}]}
        bib=b'schema_version: 3\nreferences:\n  - id: fixture\n    status: active\n'
        with self.assertRaises(ValueError):api.apply_labels(self.g,ttl,json.dumps(records).encode(),bib)
        records['records'][0]['basis']['level']=2
        with self.assertRaises(ValueError):api.apply_labels(self.g,ttl,json.dumps(records).encode(),None)
        _,result=api.apply_labels(self.g,ttl,json.dumps(records).encode(),bib)
        self.assertEqual(result['records'][0]['basis']['level'],2)
