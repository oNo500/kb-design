"""Local changes must survive refreshes without overwriting conflicting upstream edits."""
import unittest
from rdflib import Graph,URIRef,Literal,SKOS,RDF


def graph():
    return Graph().parse(data='''@prefix s:<http://www.w3.org/2004/02/skos/core#>.
<urn:a> a s:Concept;s:prefLabel "A"@en;s:broader <urn:b>.
<urn:b> a s:Concept;s:prefLabel "B"@en;s:narrower <urn:a>.
<urn:g> a s:Collection;s:member <urn:a>.''',format='turtle')


class LocalEditTests(unittest.TestCase):
    def api(self):
        from kb_vocab.local_edits import prepare, apply, empty
        return prepare,apply,empty

    def test_three_way_conflict_preserves_intent(self):
        prepare,apply,empty=self.api();base=graph()
        doc=prepare(empty(),[{'op':'set','subject':'urn:a','predicate':'skos:prefLabel','language':'en','values':['"Local"@en']}],base,base,'user')
        rendered,report=apply(base,doc)
        self.assertIn((URIRef('urn:a'),SKOS.prefLabel,Literal('Local',lang='en')),rendered)
        incoming=graph();incoming.set((URIRef('urn:b'),SKOS.prefLabel,Literal('Elsewhere',lang='en')))
        self.assertFalse(apply(incoming,doc)[1]['conflicts'])
        incoming.set((URIRef('urn:a'),SKOS.prefLabel,Literal('Upstream',lang='en')))
        _,report=apply(incoming,doc)
        self.assertEqual(report['conflicts'][0]['code'],'field_changed')
        self.assertEqual(doc['patches'][0]['values'],['"Local"@en'])

    def test_relation_edit_updates_inverse_and_node_deletion_is_persistent(self):
        prepare,apply,empty=self.api();base=graph()
        doc=prepare(empty(),[{'op':'remove','subject':'urn:a','predicate':'skos:broader','values':['<urn:b>']}],base,base,'user')
        result,report=apply(base,doc)
        self.assertNotIn((URIRef('urn:b'),SKOS.narrower,URIRef('urn:a')),result)
        doc=prepare(doc,[{'op':'delete','subject':'urn:a'}],base,result,'user')
        result,report=apply(base,doc)
        self.assertFalse(any(URIRef('urn:a') in t for t in result))
        self.assertFalse(any(URIRef('urn:a') in t for t in apply(base,doc)[0]))

    def test_local_creation_survives_source_removal_but_dangling_relation_conflicts(self):
        prepare,apply,empty=self.api();base=graph()
        create={'op':'create','subject':'urn:local','type':'skos:Concept','fields':{'skos:prefLabel':['"Local"@en']}}
        doc=prepare(empty(),[create],base,base,'user')
        result,report=apply(Graph(),doc)
        self.assertIn((URIRef('urn:local'),RDF.type,SKOS.Concept),result)
        doc=prepare(doc,[{'op':'add','subject':'urn:local','predicate':'skos:broader','values':['<urn:a>']}],base,apply(base,doc)[0],'user')
        self.assertTrue(apply(Graph(),doc)[1]['conflicts'])

    def test_conflict_resolution_rebases_or_discards_patch(self):
        from kb_vocab.local_edits import resolve
        prepare,apply,empty=self.api();base=graph()
        doc=prepare(empty(),[{'op':'set','subject':'urn:a','predicate':'skos:prefLabel','language':'en','values':['"Local"@en']}],base,base,'user')
        incoming=graph();incoming.set((URIRef('urn:a'),SKOS.prefLabel,Literal('New',lang='en')))
        conflict=apply(incoming,doc)[1]['conflicts'][0]
        kept=resolve(doc,conflict,'local','user')
        self.assertFalse(apply(incoming,kept)[1]['conflicts'])
        dropped=resolve(doc,conflict,'source','user')
        self.assertIn((URIRef('urn:a'),SKOS.prefLabel,Literal('New',lang='en')),apply(incoming,dropped)[0])

    def test_local_reference_is_not_silently_lost_by_target_deletion(self):
        prepare,apply,empty=self.api();base=graph()
        doc=prepare(empty(),[{'op':'add','subject':'urn:b','predicate':'skos:related','values':['<urn:a>']}],base,base,'user')
        with self.assertRaisesRegex(ValueError,'conflicts'):
            prepare(doc,[{'op':'delete','subject':'urn:a'}],base,apply(base,doc)[0],'user')

    def test_add_and_remove_keep_other_values_of_local_creation(self):
        prepare,apply,empty=self.api();base=graph()
        doc=prepare(empty(),[{'op':'create','subject':'urn:local','type':'skos:Concept','fields':{'skos:prefLabel':['"Local"@en'],'skos:altLabel':['"A"@en','"C"@en']}}],base,base,'user')
        doc=prepare(doc,[{'op':'add','subject':'urn:local','predicate':'skos:altLabel','values':['"B"@en']}],base,apply(base,doc)[0],'user')
        self.assertEqual(set(apply(base,doc)[0].objects(URIRef('urn:local'),SKOS.altLabel)),{Literal(x,lang='en') for x in ['A','B','C']})
        doc=prepare(doc,[{'op':'remove','subject':'urn:local','predicate':'skos:altLabel','values':['"B"@en']}],base,apply(base,doc)[0],'user')
        self.assertEqual(set(apply(base,doc)[0].objects(URIRef('urn:local'),SKOS.altLabel)),{Literal(x,lang='en') for x in ['A','C']})

    def test_successive_adds_merge_with_unrelated_source_additions(self):
        prepare,apply,empty=self.api();base=graph();base.add((URIRef('urn:a'),SKOS.altLabel,Literal('A',lang='en')))
        doc=empty()
        for value in ['B','C']:
            doc=prepare(doc,[{'op':'add','subject':'urn:a','predicate':'skos:altLabel','values':[f'"{value}"@en']}],base,apply(base,doc)[0],'user')
        remote=base+Graph();remote.add((URIRef('urn:a'),SKOS.altLabel,Literal('D',lang='en')))
        result,report=apply(remote,doc)
        self.assertFalse(report['conflicts'])
        self.assertEqual(set(result.objects(URIRef('urn:a'),SKOS.altLabel)),{Literal(x,lang='en') for x in ['A','B','C','D']})

    def test_removing_inverse_of_created_relation_is_not_reintroduced(self):
        prepare,apply,empty=self.api();base=graph()
        doc=prepare(empty(),[{'op':'create','subject':'urn:local','type':'skos:Concept','fields':{'skos:prefLabel':['"Local"@en'],'skos:broader':['<urn:b>']}}],base,base,'user')
        doc=prepare(doc,[{'op':'remove','subject':'urn:b','predicate':'skos:narrower','values':['<urn:local>']}],base,apply(base,doc)[0],'user')
        result,report=apply(base,doc)
        self.assertFalse(report['conflicts'])
        self.assertNotIn((URIRef('urn:local'),SKOS.broader,URIRef('urn:b')),result)
        self.assertNotIn((URIRef('urn:b'),SKOS.narrower,URIRef('urn:local')),result)

    def test_target_can_be_deleted_after_its_local_inverse_is_removed(self):
        prepare,apply,empty=self.api();base=graph()
        doc=prepare(empty(),[{'op':'create','subject':'urn:local','type':'skos:Concept','fields':{'skos:prefLabel':['"Local"@en'],'skos:broader':['<urn:b>']}}],base,base,'user')
        doc=prepare(doc,[{'op':'remove','subject':'urn:b','predicate':'skos:narrower','values':['<urn:local>']}],base,apply(base,doc)[0],'user')
        doc=prepare(doc,[{'op':'delete','subject':'urn:b'}],base,apply(base,doc)[0],'user')
        result,report=apply(base,doc)
        self.assertFalse(report['conflicts'])
        self.assertFalse(any(URIRef('urn:b') in t for t in result))
        self.assertIn((URIRef('urn:local'),RDF.type,SKOS.Concept),result)
