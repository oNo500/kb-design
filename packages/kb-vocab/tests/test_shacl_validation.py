"""Behavior checks for the published vocabulary profile, using local graphs."""
import unittest
from pathlib import Path
from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, SKOS, XSD
from rdflib.namespace import DCTERMS, OWL

EX = Namespace('urn:test:')
SHAPES = Path(__file__).resolve().parents[3] / 'data/inputs/vocabulary/shapes.ttl'


def fixture():
    graph = Graph()
    graph.add((EX.scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((EX.scheme, SKOS.prefLabel, Literal('Vocabulary', lang='en')))
    graph.add((EX.scheme, SKOS.scopeNote, Literal('Test scope', lang='en')))
    graph.add((EX.a, RDF.type, SKOS.Concept))
    graph.add((EX.a, SKOS.inScheme, EX.scheme))
    graph.add((EX.a, SKOS.prefLabel, Literal('Name', lang='en')))
    return graph


class ProfileTests(unittest.TestCase):
    def validate(self, graph):
        from kb_vocab.shacl_validation import validate_profile
        return validate_profile(graph, SHAPES)

    def test_profile_accepts_collections_variants_and_resource_notes_without_mutation(self):
        graph = fixture()
        graph.add((EX.group, RDF.type, SKOS.Collection))
        graph.add((EX.group, RDF.type, EX.SourceGroup))
        graph.add((EX.group, SKOS.prefLabel, Literal('Group', lang='en')))
        graph.add((EX.group, SKOS.inScheme, EX.scheme))
        graph.add((EX.group, SKOS.member, EX.a))
        graph.add((EX.a, SKOS.prefLabel, Literal('US name', lang='en-US')))
        graph.add((EX.a, SKOS.prefLabel, Literal('GB name', lang='en-GB')))
        graph.add((EX.a, SKOS.definition, EX.external_reference))
        graph.add((EX.a, SKOS.note, BNode('note')))
        graph.add((BNode('note'), RDF.value, Literal('Explanation', lang='en')))
        graph.add((EX.a, DCTERMS.created, Literal('2020-01-01', datatype=XSD.date)))
        graph.add((EX.a, OWL.deprecated, Literal(False)))
        graph.add((EX.document, OWL.imports, EX.unavailable_ontology))
        before = set(graph)
        self.assertTrue(self.validate(graph)['conforms'])
        self.assertEqual(set(graph), before)

    def test_profile_rejects_structural_and_field_errors(self):
        bad = [
            (EX.a, SKOS.prefLabel, Literal('Duplicate', lang='EN')),
            (EX.a, SKOS.altLabel, Literal('Name', lang='en')),
            (EX.a, SKOS.hiddenLabel, EX.not_a_literal),
            (EX.a, SKOS.altLabel, Literal('Nom', lang='fr')),
            (EX.a, SKOS.inScheme, EX.missing),
            (EX.a, RDF.type, SKOS.Collection),
            (EX.a, DCTERMS.created, Literal('yesterday')),
            (EX.a, OWL.deprecated, Literal('yes')),
            (EX.a, SKOS.broader, EX.scheme),
            (EX.a, DCTERMS.isReplacedBy, EX.scheme),
            (EX.a, SKOS.exactMatch, Literal('not an IRI')),
        ]
        for triple in bad:
            with self.subTest(triple=triple):
                graph = fixture()
                graph.add(triple)
                result = self.validate(graph)
                self.assertFalse(result['conforms'])
                self.assertTrue(result['violations'])
                self.assertIn('shape', result['violations'][0])
                self.assertIn('component', result['violations'][0])

    def test_inherited_missing_names_and_filtered_local_note_are_warnings(self):
        graph = fixture()
        graph.remove((EX.a, SKOS.prefLabel, None))
        graph.add((EX.task, RDF.type, RDFS.Resource))
        graph.add((EX.task, DCTERMS.type, Literal('task')))
        graph.add((EX.task, RDFS.label, Literal('')))
        graph.add((EX.task, DCTERMS.identifier, Literal('task-id')))
        graph.add((EX.task, DCTERMS.source, EX.source))
        graph.add((EX.a, SKOS.definition, EX.note))
        graph.add((EX.note, DCTERMS.created, Literal('2020-01-01', datatype=XSD.date)))
        graph.add((EX.unrelated, RDF.type, RDFS.Resource))
        result = self.validate(graph)
        self.assertTrue(result['conforms'], result['violations'])
        nodes = {issue['node'] for issue in result['warnings']}
        self.assertTrue({str(EX.a), str(EX.task), str(EX.note)} <= nodes)
        self.assertNotIn(str(EX.unrelated), nodes)

    def test_scheme_required_information_is_a_violation(self):
        for predicate in (SKOS.prefLabel, SKOS.scopeNote):
            graph = fixture()
            graph.remove((EX.scheme, predicate, None))
            self.assertFalse(self.validate(graph)['conforms'])

    def test_generated_nodes_and_extension_languages_are_checked(self):
        from kb_vocab.shacl_validation import validate_profile
        graph = fixture()
        graph.add((EX.group, RDF.type, SKOS.Collection))
        inherited = validate_profile(graph, SHAPES)
        self.assertTrue(inherited['conforms'])
        generated = validate_profile(graph, SHAPES, generated_nodes=[EX.group])
        self.assertFalse(generated['conforms'])
        graph.add((EX.group, SKOS.prefLabel, Literal('Group', lang='en')))
        graph.add((EX.group, SKOS.inScheme, EX.scheme))
        graph.add((EX.a, EX.extension, Literal('Other', lang='fr')))
        self.assertFalse(self.validate(graph)['conforms'])

    def test_relation_subjects_and_local_mapping_types_are_checked(self):
        for predicate, target in [(SKOS.broader, EX.a), (SKOS.member, EX.a),
                                  (SKOS.exactMatch, EX.scheme)]:
            graph = fixture()
            graph.add((EX.untyped, predicate, target))
            self.assertFalse(self.validate(graph)['conforms'])
        graph = fixture()
        graph.add((EX.a, SKOS.exactMatch, EX.external_concept))
        self.assertTrue(self.validate(graph)['conforms'])

    def test_shapes_are_valid_shacl(self):
        from pyshacl import validate
        conforms, _, _ = validate(fixture(), shacl_graph=Graph().parse(SHAPES),
                                  meta_shacl=True, inference='none', do_owl_imports=False)
        self.assertTrue(conforms)
