import unittest
from rdflib import Graph, Literal, Namespace, RDF, SKOS, URIRef
from kb_vocab.validation import validate_graph
from kb_vocab.query import describe_concept, find_concepts, select_query

EX = Namespace('urn:test:')

def fixture():
    g = Graph()
    g.add((EX.scheme, RDF.type, SKOS.ConceptScheme))
    for name in ('a', 'b', 'c'):
        g.add((EX[name], RDF.type, SKOS.Concept))
        g.add((EX[name], SKOS.inScheme, EX.scheme))
        g.add((EX[name], SKOS.prefLabel, Literal(name, lang='en')))
    return g

class ValidationTests(unittest.TestCase):
    def test_rejects_wrong_node_kinds_and_untyped_references(self):
        g = fixture()
        g.add((EX.a, SKOS.altLabel, EX.label))
        g.add((EX.a, SKOS.broader, Literal('b')))
        g.add((EX.b, SKOS.related, EX.missing))
        g.add((EX.a, SKOS.inScheme, EX.missing_scheme))
        before = set(g)
        result = validate_graph(g)
        self.assertFalse(result['valid'])
        self.assertGreaterEqual(len(result['errors']), 4)
        self.assertEqual(set(g), before)

    def test_labels_conflict_but_multilingual_labels_do_not(self):
        g = fixture()
        g.add((EX.a, SKOS.prefLabel, Literal('甲', lang='zh')))
        self.assertTrue(validate_graph(g)['valid'])
        g.add((EX.a, SKOS.prefLabel, Literal('another', lang='EN')))
        g.add((EX.a, SKOS.hiddenLabel, Literal('a', lang='en')))
        self.assertFalse(validate_graph(g)['valid'])

    def test_transitive_hierarchy_conflict_and_cycles_are_distinct(self):
        g = fixture()
        g.add((EX.a, SKOS.broader, EX.b))
        g.add((EX.c, SKOS.narrower, EX.b))
        g.add((EX.c, SKOS.related, EX.a))
        self.assertFalse(validate_graph(g)['valid'])
        g.remove((EX.c, SKOS.related, EX.a))
        g.add((EX.c, SKOS.broader, EX.a))
        result = validate_graph(g)
        self.assertTrue(result['valid'])
        self.assertTrue(result['warnings'])

class QueryTests(unittest.TestCase):
    def test_lookup_preserves_language_relations_and_ambiguity(self):
        g = fixture()
        g.add((EX.a, SKOS.altLabel, Literal('Alpha', lang='en')))
        g.add((EX.a, SKOS.broader, EX.b))
        self.assertEqual(describe_concept(g, 'Alpha')['id'], str(EX.a))
        self.assertEqual(find_concepts(g, 'alp')[0]['id'], str(EX.a))
        self.assertIn(str(EX.b), describe_concept(g, str(EX.a))['broader'])
        g.add((EX.b, SKOS.altLabel, Literal('Alpha', lang='en')))
        with self.assertRaises(ValueError):
            describe_concept(g, 'Alpha')
        with self.assertRaises(ValueError):
            describe_concept(g, 'absent')

    def test_select_is_local_read_only_and_serializable(self):
        g = fixture()
        result = select_query(g, 'SELECT ?s WHERE { ?s a <http://www.w3.org/2004/02/skos/core#Concept> } ORDER BY ?s')
        self.assertEqual(len(result['rows']), 3)
        for query in (
            'DELETE WHERE { ?s ?p ?o }',
            'SELECT * WHERE { SERVICE <https://example.org/> { ?s ?p ?o } }',
            'SELECT * FROM <https://example.org/data> WHERE { ?s ?p ?o }',
        ):
            with self.subTest(query=query), self.assertRaises(ValueError):
                select_query(g, query)
