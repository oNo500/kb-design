"""Source updates must retain unrelated identities and explain version changes."""
import unittest
from copy import deepcopy
from rdflib import Graph, RDF, SKOS, Literal, URIRef, DCTERMS
from test_eric import xml, term
from test_ieee_mapping import sample, entry
from test_cognitive_atlas import record
from kb_vocab.eric import project_eric
from kb_vocab.ieee import project_ieee
from kb_vocab.cognitive_atlas import project_cognitive


class UpdateTests(unittest.TestCase):
    def test_eric_note_change_keeps_b_and_adopts_existing_ids(self):
        first, _, _ = project_eric(xml(term('A'),term('B')), {})
        edited = xml(term('A',attributes='<Attribute name="ScopeNote">New note</Attribute>'), term('B'))
        fresh, _, _ = project_eric(edited, {})
        b = next(first.subjects(SKOS.prefLabel,Literal('B',lang='en')))
        self.assertIn((b,RDF.type,SKOS.Concept), fresh)
        legacy = URIRef('urn:legacy:b')
        for s,p,o in list(first):
            if s == b or o == b:
                first.remove((s,p,o));first.add((legacy if s==b else s,p,legacy if o==b else o))
        updated, _, _ = project_eric(edited, {}, identities=first)
        self.assertIn((legacy,RDF.type,SKOS.Concept),updated)
        with self.assertRaisesRegex(ValueError,'identity'):
            project_eric(xml(term('A'),term('Renamed')),{},identities=first)

    def test_ieee_cross_snapshot_and_reordered_entry_ids_preserve_uris(self):
        data=sample(); old,_=project_ieee(data)
        data['source']['sha256']='b'*64
        data['entries'][0]['id']='renumbered'
        data['entries'].append(entry('new','New','preferred',[]))
        graph,_=project_ieee(data,identities=old)
        self.assertTrue(set(old.subjects(RDF.type,SKOS.Concept)) <= set(graph.subjects(RDF.type,SKOS.Concept)))

    def test_cognitive_addition_preserves_existing_and_rejects_kind_change(self):
        data={'records':[record('a'),record('task','task')]}
        old,_=project_cognitive(data)
        data['records'].append(record('b'))
        graph,_=project_cognitive(data,identities=old)
        self.assertEqual(graph.value(None,DCTERMS.identifier,Literal('a')),old.value(None,DCTERMS.identifier,Literal('a')))
        data['records'][0]['kind']='task'
        with self.assertRaisesRegex(ValueError,'identity'):
            project_cognitive(data,identities=old)

    def test_diff_explains_fields_and_ignores_blank_node_ids(self):
        from kb_vocab.version_diff import compare_graphs
        a=Graph().parse(data='@prefix s:<http://www.w3.org/2004/02/skos/core#>. <urn:a> a s:Concept;s:prefLabel "A"@en;s:note [ <urn:value> "note" ].',format='turtle')
        b=Graph().parse(data=a.serialize(format='turtle'),format='turtle')
        self.assertTrue(compare_graphs(a,b)['graph_equal'])
        b.set((URIRef('urn:a'),SKOS.prefLabel,Literal('B',lang='en')))
        delta=compare_graphs(a,b)
        self.assertFalse(delta['graph_equal'])
        self.assertEqual(delta['concepts']['added'],[])
        self.assertEqual(delta['changed_nodes'][0]['uri'],'urn:a')
        self.assertEqual(delta['changed_nodes'][0]['fields'][0]['predicate'],str(SKOS.prefLabel))
