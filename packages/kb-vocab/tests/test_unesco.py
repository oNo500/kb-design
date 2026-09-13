"""Native source ingestion must preserve meaning and expose diagnostic failures."""
from pathlib import Path
import tempfile
import unittest

from rdflib import Graph
from rdflib.compare import isomorphic

from kb_vocab.unesco import import_unesco


SOURCE = '''@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix ex: <https://publisher.example/> .
ex:scheme a skos:ConceptScheme ; skos:prefLabel "Catalogue"@en .
ex:a a skos:Concept ; skos:inScheme ex:scheme ;
 skos:prefLabel "Learning"@en, "Apprentissage"@fr ; skos:broader ex:b .
ex:b a skos:Concept ; skos:inScheme ex:scheme ; skos:prefLabel "Education"@en .
ex:group a skos:Collection ; skos:prefLabel "Topics"@en ; skos:member ex:a .
'''


class UnescoImportTests(unittest.TestCase):
    def test_preserves_true_label_conflict_and_reports_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source.ttl'
            raw = SOURCE + '\nex:a skos:altLabel "Learning"@en .\n'
            source.write_text(raw, encoding='utf-8')
            report = import_unesco(source, root / 'out')
            self.assertEqual((root / 'out/source-original.ttl').read_bytes(), source.read_bytes())
            self.assertEqual(report['status'], 'source-graph-preserved')
            self.assertFalse(report['validation']['valid'])
            self.assertEqual([x['code'] for x in report['validation']['errors']],
                             ['skos.S13.label_disjointness'])
            self.assertTrue(isomorphic(Graph().parse(data=raw, format='turtle'),
                                       Graph().parse(root / 'out/vocabulary.ttl', format='turtle')))


if __name__ == '__main__':
    unittest.main()
