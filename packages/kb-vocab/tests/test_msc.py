"""Preserve MSC identity and hierarchy without turning references into parents."""
import csv
import io
import unittest
from rdflib import DCTERMS, Literal, RDF, SKOS
from kb_vocab.msc import project_msc


def source_bytes(rows):
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, delimiter='\t')
    writer.writerow(['code', 'text', 'description'])
    writer.writerows(rows)
    return stream.getvalue().encode('cp1252')


class MscProjectionTests(unittest.TestCase):
    def test_direct_hierarchy_identity_and_reference_preservation(self):
        rows = [('00A07', 'Problem books', r'Problem books \{For open problems, see 00A27\}'),
                ('00-01', 'Introductory exposition', 'Introductory exposition'),
                ('00-XX', 'General topics', 'General topics'),
                ('00Axx', 'General topics', 'General topics'),
                ('00A27', 'Lists of open problems', 'Lists of open problems')]
        graph, report, ledger = project_msc(source_bytes(rows), {})
        ids = {str(code): node for node, code in graph.subject_objects(SKOS.notation)}
        self.assertEqual(set(graph.objects(ids['00A07'], SKOS.broader)), {ids['00Axx']})
        self.assertEqual(set(graph.objects(ids['00-01'], SKOS.broader)), {ids['00-XX']})
        self.assertNotIn((ids['00A07'], SKOS.related, ids['00A27']), graph)
        self.assertIn((ids['00A07'], DCTERMS.description, Literal(rows[0][2], lang='en')), graph)
        again, _, _ = project_msc(source_bytes(list(reversed(rows))), {})
        self.assertEqual(set(graph), set(again))
        self.assertEqual(len(ledger['entries']), len(rows))
        self.assertEqual(report['counts']['broader'], 4)

    def test_missing_parent_is_held_not_fabricated_or_promoted(self):
        graph, report, ledger = project_msc(source_bytes([('68T05', 'Learning', 'Learning')]), {})
        self.assertEqual(len(set(graph.subjects(RDF.type, SKOS.Concept))), 1)
        self.assertFalse(list(graph.triples((None, SKOS.broader, None))))
        self.assertFalse(list(graph.triples((None, SKOS.topConceptOf, None))))
        self.assertEqual(ledger['held'][0]['reason'], 'missing_parent')

    def test_malformed_or_duplicate_source_fails_without_silent_loss(self):
        for rows in [[], [('68T05', 'Learning', 'Learning')] * 2,
                     [('bad', 'Learning', 'Learning')], [('68T05', '', 'Learning')]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                project_msc(source_bytes(rows), {})
        with self.assertRaises(ValueError):
            project_msc(b'code\ttext\tdescription\n68T05\tLearning\n', {})


if __name__ == '__main__':
    unittest.main()
