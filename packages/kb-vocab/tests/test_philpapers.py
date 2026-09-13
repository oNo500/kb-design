import json
import unittest

from rdflib import DCTERMS, Literal, RDF, SKOS, URIRef
from kb_vocab.philpapers import project_philpapers


class PhilPapersTests(unittest.TestCase):
    def project(self, rows):
        return project_philpapers(json.dumps(rows).encode(), {'sha256': 'test'})

    def test_all_parents_retained_primary_not_exclusive(self):
        graph, report, ledger = self.project([
            ['Branch A', 2, '1', 1], ['Branch B', 3, '1', 1],
            ['Shared concept', 4, '2,3', 3]])
        node = URIRef('urn:kb-vocab:philpapers:category:4')
        self.assertEqual(set(graph.objects(node, SKOS.broader)), {
            URIRef('urn:kb-vocab:philpapers:category:2'),
            URIRef('urn:kb-vocab:philpapers:category:3')})
        self.assertEqual(ledger['entries'][2]['primary_parent_id'], '3')
        self.assertEqual(len(set(graph.subjects(RDF.type, SKOS.Concept))), 3)

    def test_missing_parent_isolated_without_losing_existing_parent(self):
        graph, report, ledger = self.project([
            ['Existing', 2, '1', 1], ['Child', 4, '2,999', 999]])
        child = URIRef('urn:kb-vocab:philpapers:category:4')
        self.assertEqual(list(graph.objects(child, SKOS.broader)),
                         [URIRef('urn:kb-vocab:philpapers:category:2')])
        self.assertNotIn((URIRef('urn:kb-vocab:philpapers:category:999'), RDF.type, SKOS.Concept), graph)
        self.assertTrue(any(x['reason'] == 'missing_parent' for x in ledger['relations']))
        self.assertNotIn((child, SKOS.topConceptOf, None), graph)

    def test_identity_stable_across_label_change_and_duplicates_rejected(self):
        a, _, _ = self.project([['Old name', 2, '1', 1]])
        b, _, _ = self.project([['New name', 2, '1', 1]])
        self.assertEqual(set(a.subjects(DCTERMS.identifier, Literal('2'))),
                         set(b.subjects(DCTERMS.identifier, Literal('2'))))
        with self.assertRaises(ValueError):
            self.project([['A', 2, '1', 1], ['B', 2, '1', 1]])

    def test_empty_source_name_preserves_identity_without_inventing_label(self):
        graph, report, ledger = self.project([['', 2, '1', 1]])
        node = URIRef('urn:kb-vocab:philpapers:category:2')
        self.assertIn((node, RDF.type, SKOS.Concept), graph)
        self.assertEqual(list(graph.objects(node, SKOS.prefLabel)), [])
        self.assertTrue(any(x['code'] == 'empty_source_label' for x in ledger['issues']))

    def test_primary_parent_not_added_to_broader(self):
        graph, _, ledger = self.project([
            ['A', 2, '1', 1], ['B', 3, '1', 1], ['C', 4, '2', 3]])
        self.assertNotIn((URIRef('urn:kb-vocab:philpapers:category:4'), SKOS.broader,
                          URIRef('urn:kb-vocab:philpapers:category:3')), graph)
        self.assertTrue(any(x['code'] == 'primary_parent_not_in_parents' for x in ledger['issues']))


if __name__ == '__main__':
    unittest.main()
