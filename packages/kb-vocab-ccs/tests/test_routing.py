import importlib
import tempfile
import unittest
from pathlib import Path
from rdflib import Graph, SKOS, URIRef, RDF, Namespace, Literal

TTL='''@prefix s: <http://www.w3.org/2004/02/skos/core#> .
@prefix x: <http://www.w3.org/2008/05/skos-xl#> .
<urn:scheme> a s:ConceptScheme; s:hasTopConcept <urn:root>,<urn:academic> .
<urn:root> a s:Concept; s:prefLabel "Names"@en; s:narrower <urn:item>,<urn:both> .
<urn:academic> a s:Concept; s:prefLabel "Computing"@en .
<urn:item> a s:Concept; s:prefLabel "Tool"@en,"工具"@zh; s:broader <urn:root>; s:related <urn:both> .
<urn:both> a s:Concept; s:prefLabel "Language"@en; s:broader <urn:root> .
'''
class RoutingTests(unittest.TestCase):
 def api(self):
  try:return importlib.import_module('kb_vocab_ccs.routing')
  except ModuleNotFoundError:self.fail('清单处理尚未实现')
 def setup_case(self):
  temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
  folder=Path(temp.name);source=folder/'input.ttl';source.write_text(TTL)
  api=self.api();plan=api.prepare(source,'urn:root');return api,folder,source,plan
 def test_unconfirmed_and_incomplete_plans_cannot_write(self):
  api,folder,source,plan=self.setup_case()
  with self.assertRaises(ValueError):api.partition(source,plan,folder/'out')
  self.assertFalse((folder/'out').exists())
  plan['confirmed']=True;plan['items'].pop()
  with self.assertRaises(ValueError):api.partition(source,plan,folder/'out')
  self.assertFalse((folder/'out').exists())
 def test_routing_preserves_identity_language_and_removes_dangling_edges(self):
  api,folder,source,plan=self.setup_case()
  for row in plan['items']:
   row['action']={'urn:root':'concept','urn:item':'entity','urn:both':'both'}[row['source_id']]
   row['kind']='software' if row['source_id']=='urn:item' else 'programming-language' if row['source_id']=='urn:both' else None
  plan['confirmed']=True
  report=api.partition(source,plan,folder/'out')
  result=Graph().parse(folder/'out/concepts.ttl')
  self.assertFalse(list(result.triples((URIRef('urn:item'),None,None))))
  self.assertFalse(list(result.triples((None,None,URIRef('urn:item')))))
  self.assertTrue(list(result.triples((URIRef('urn:both'),SKOS.prefLabel,None))))
  import json
  audit=json.loads((folder/'out/entity-audit.json').read_text())['records']
  tool=URIRef(next(r for r in audit if r['source_concept']=='urn:item')['id'])
  entities=Graph().parse(folder/'out/entities.ttl')
  self.assertEqual(set(entities.objects(tool,SKOS.prefLabel)),{Literal('Tool',lang='en'),Literal('工具',lang='zh')})
  self.assertIn((tool,RDF.type,URIRef('http://www.wikidata.org/entity/Q7397')),entities)
  self.assertNotIn((tool,RDF.type,SKOS.Concept),entities)
  xl=Namespace('http://www.w3.org/2008/05/skos-xl#')
  projected={v for name in entities.objects(tool,xl.prefLabel) for v in entities.objects(name,xl.literalForm)}
  self.assertEqual(projected,set(entities.objects(tool,SKOS.prefLabel)))
  self.assertEqual(source.read_text(),TTL)
  api.partition(source,plan,folder/'second')
  self.assertEqual((folder/'out/entities.ttl').read_bytes(),(folder/'second/entities.ttl').read_bytes())
 def test_changed_input_and_invalid_kind_are_rejected(self):
  api,folder,source,plan=self.setup_case();plan['confirmed']=True
  source.write_text(TTL+'\n# Changed snapshot\n')
  with self.assertRaises(ValueError):api.partition(source,plan,folder/'out')
  source.write_text(TTL)
  plan['items'][0].update(action='entity',kind='invented-kind')
  with self.assertRaises(ValueError):api.partition(source,plan,folder/'out')

 def test_pending_relations_cannot_be_silently_removed(self):
  api,folder,source,plan=self.setup_case();plan['confirmed']=True
  for row in plan['items']:
   if row['source_id']=='urn:root':row.update(action='entity',kind='organization')
  with self.assertRaises(ValueError):api.partition(source,plan,folder/'out')
  self.assertFalse((folder/'out').exists())
