"""Behavior checks for preserving source identities and conservative candidates."""
import hashlib
import importlib
import json
from pathlib import Path
import tempfile
import unittest

from rdflib import Graph

PREFIX = '''@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix ex: <https://example.org/> .
'''


class ReviewCatalogTests(unittest.TestCase):
    def setUp(self):
        try:
            self.api = importlib.import_module('kb_vocab.review_catalog')
        except ModuleNotFoundError as error:
            if error.name != 'kb_vocab.review_catalog':
                raise
            self.fail('review_catalog API is not implemented')

    def sources(self, **bodies):
        return {name: {'name': name, 'graph': Graph().parse(data=PREFIX + body, format='turtle')}
                for name, body in bodies.items()}

    def test_index_preserves_unlabelled_concepts_multiple_parents_and_text(self):
        index = self.api.index_concepts(self.sources(A='''
ex:child a skos:Concept; skos:broader ex:p2, ex:p1;
 skos:related ex:r; skos:hiddenLabel "secret"@en;
 skos:definition "definition"@en; skos:scopeNote "scope"@en;
 dct:description "description" .
ex:empty a skos:Concept .
ex:other skos:prefLabel "not a concept" .
'''))
        self.assertEqual(set(index), {'https://example.org/child', 'https://example.org/empty'})
        child = index['https://example.org/child']
        self.assertEqual(child['broader'], ['https://example.org/p1', 'https://example.org/p2'])
        self.assertEqual(child['related'], ['https://example.org/r'])
        self.assertEqual({x['kind'] for x in child['definitions']}, {'definition', 'scopeNote', 'description'})
        self.assertEqual(child['labels'], [{'value': 'secret', 'language': 'en', 'kind': 'hiddenLabel'}])
        self.assertEqual(index['https://example.org/empty']['labels'], [])

    def test_duplicate_uri_across_sources_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'https://example.org/x'):
            self.api.index_concepts(self.sources(A='ex:x a skos:Concept .', B='ex:x a skos:Concept .'))

    def test_candidates_are_cross_source_same_language_and_not_relations(self):
        index = self.api.index_concepts(self.sources(A='''
ex:a a skos:Concept; skos:prefLabel "  CAFÉ   science "@en; skos:altLabel "Café science"@en .
ex:same a skos:Concept; skos:prefLabel "café science"@en .
ex:hidden a skos:Concept; skos:hiddenLabel "hidden"@en .
''', B='''
ex:b a skos:Concept; skos:altLabel "café science"@en .
ex:french a skos:Concept; skos:prefLabel "café science"@fr .
ex:h a skos:Concept; skos:prefLabel "hidden"@en .
'''))
        pairs = self.api.candidate_pairs(index)
        self.assertEqual({(p['subject'], p['object']) for p in pairs}, {
            ('https://example.org/a', 'https://example.org/b'),
            ('https://example.org/b', 'https://example.org/same')})
        pair = next(p for p in pairs if p['subject'].endswith('/a'))
        self.assertEqual({e['subject_label']['value'] for e in pair['evidence']},
                         {'  CAFÉ   science ', 'Café science'})
        self.assertEqual(pairs, self.api.candidate_pairs(dict(reversed(list(index.items())))))

    def test_manifest_tampering_is_rejected_for_both_manifest_formats(self):
        for structured in (False, True):
            with self.subTest(structured=structured), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                bundle = root / 'bundle'
                bundle.mkdir()
                ttl = bundle / 'vocabulary.ttl'
                ttl.write_text(PREFIX + 'ex:a a skos:Concept .')
                sha = hashlib.sha256(ttl.read_bytes()).hexdigest()
                (bundle / 'manifest.json').write_text(json.dumps({'files': {
                    ttl.name: {'sha256': sha, 'size': ttl.stat().st_size} if structured else sha}}))
                catalog = root / 'catalog.json'
                catalog.write_text(json.dumps({'sources': [{'name': 'A', 'directory': 'bundle'}]}))
                self.api.read_catalog(catalog)
                ttl.write_text(PREFIX + 'ex:b a skos:Concept .')
                with self.assertRaisesRegex(ValueError, 'sha256'):
                    self.api.read_catalog(catalog)

    def test_duplicate_source_names_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ttl = root / 'own.ttl'
            ttl.write_text(PREFIX + 'ex:a a skos:Concept .')
            catalog = root / 'catalog.json'
            entry = {'name': 'own', 'file': 'own.ttl'}
            catalog.write_text(json.dumps({'sources': [entry]}))
            catalog.write_text(json.dumps({'sources': [entry, entry]}))
            with self.assertRaisesRegex(ValueError, 'name'):
                self.api.read_catalog(catalog)


if __name__ == '__main__':
    unittest.main()
