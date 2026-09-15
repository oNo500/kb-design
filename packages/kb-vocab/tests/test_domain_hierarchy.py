"""Explicit domain roots must preserve source identities and isolated concepts."""
import unittest
from rdflib import Graph, RDF, SKOS, URIRef
import test_system_build as fixtures
from kb_vocab.system_build import build_system


class DomainHierarchyTests(unittest.TestCase):
    setUp = fixtures.SystemBuildTests.setUp
    save = fixtures.SystemBuildTests.save

    def configure(self):
        self.config['domains'][0]['hierarchy'] = {'uri': 'urn:domain:test', 'roots': ['urn:a']}
        self.config['vocabulary']['top_concepts'] = ['urn:domain:test']
        self.save()

    def test_explicit_roots_preserve_source_edges_and_do_not_adopt_isolated_nodes(self):
        self.configure()
        build_system(self.path, self.root / 'out')
        g = Graph().parse(self.root / 'out/vocabulary.ttl')
        domain = URIRef('urn:domain:test')
        self.assertIn((domain, RDF.type, SKOS.Concept), g)
        self.assertNotIn((domain, RDF.type, SKOS.Collection), g)
        self.assertIn((URIRef('urn:a'), SKOS.broader, domain), g)
        self.assertIn((URIRef('urn:b'), SKOS.broader, URIRef('urn:a')), g)
        self.assertFalse(list(g.objects(domain, SKOS.broader)))
        self.assertNotIn((URIRef('urn:unlabelled'), SKOS.broader, domain), g)
        self.assertIn((URIRef('urn:kb-vocab:group:test'), RDF.type, SKOS.Collection), g)

    def test_absent_or_outside_group_root_is_rejected(self):
        self.configure()
        for root in ['urn:absent', 'urn:other']:
            self.config['domains'][0]['hierarchy']['roots'] = [root]
            self.save()
            with self.subTest(root=root), self.assertRaisesRegex(ValueError, 'Hierarchy root'):
                build_system(self.path, self.root / 'bad')
