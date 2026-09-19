"""Semantic acceptance examples for the independent vocabulary shapes.

The fixtures exercise false acceptance, false rejection, graph paths and
severity isolation. They do not run source conversion or mutate a vocabulary.
"""
import unittest

from pyshacl import validate
from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, SKOS, XSD
from rdflib.collection import Collection
from rdflib.namespace import DCTERMS, SH

EX = Namespace("https://example.org/test/")
XL = Namespace("http://www.w3.org/2008/05/skos-xl#")
ISO = Namespace("http://purl.org/iso25964/skos-thes#")
RULE = Namespace("urn:kb-vocab-shacl:")


def fixture():
    graph = Graph()
    graph.add((EX.scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((EX.scheme, SKOS.prefLabel, Literal("Example", lang="en")))
    graph.add((EX.scheme, SKOS.scopeNote, Literal("Example scope", lang="en")))
    for node in (EX.a, EX.b, EX.c):
        label = EX[str(node).rsplit("/", 1)[1] + "Label"]
        graph.add((node, RDF.type, SKOS.Concept))
        graph.add((node, SKOS.inScheme, EX.scheme))
        graph.add((node, XL.prefLabel, label))
        graph.add((label, RDF.type, XL.Label))
        text = Literal(str(node).rsplit("/", 1)[1], lang="en")
        graph.add((label, XL.literalForm, text))
        graph.add((node, SKOS.prefLabel, text))
    return graph


class ShapeTests(unittest.TestCase):
    def run_shapes(self, graph, profile="target", targets=(), mutate_shapes=None):
        try:
            from kb_vocab_shacl import read_shapes
        except ImportError:
            self.fail("The independent SHACL rule package has not been created")
        shapes = Graph().parse(data=read_shapes(profile), format="turtle")
        for shape, node in targets:
            shapes.add((shape, SH.targetNode, node))
        if mutate_shapes:
            mutate_shapes(shapes)
        before = set(graph)
        conforms, report, _ = validate(
            graph, shacl_graph=shapes, inference="none", do_owl_imports=False,
            inplace=False, allow_infos=False, allow_warnings=False,
        )
        self.assertEqual(set(graph), before)
        rows = [
            {key: report.value(result, prop) for key, prop in (
                ("shape", SH.sourceShape), ("node", SH.focusNode),
                ("severity", SH.resultSeverity), ("path", SH.resultPath),
            )}
            for result in report.subjects(RDF.type, SH.ValidationResult)
        ]
        return conforms, rows

    def assert_rule(self, graph, rule, **kwargs):
        _, rows = self.run_shapes(graph, **kwargs)
        self.assertIn(rule, {row["shape"] for row in rows}, rows)

    def test_valid_xl_and_shared_text_do_not_merge_or_conflict(self):
        graph = fixture()
        graph.add((EX.a, XL.prefLabel, EX.second))
        graph.add((EX.second, RDF.type, XL.Label))
        graph.add((EX.second, XL.literalForm, Literal("a", lang="EN")))
        graph.add((EX.a, XL.prefLabel, EX.french))
        graph.add((EX.french, RDF.type, XL.Label))
        graph.add((EX.french, XL.literalForm, Literal("français", lang="fr")))
        graph.add((EX.a, SKOS.prefLabel, Literal("français", lang="fr")))
        conforms, rows = self.run_shapes(graph)
        self.assertTrue(conforms, rows)

    def test_each_label_has_one_plain_literal_and_incompatible_type_is_rejected(self):
        for triple, rule in (
            ((EX.aLabel, XL.literalForm, Literal("another", lang="en")), RULE.LabelLiteralForm),
            ((EX.aLabel, RDF.type, SKOS.Concept), RULE.LabelTypeDisjoint),
        ):
            with self.subTest(rule=rule):
                graph = fixture(); graph.add(triple)
                self.assert_rule(graph, rule)
        graph = fixture(); graph.set((EX.aLabel, XL.literalForm, Literal(12)))
        self.assert_rule(graph, RULE.LabelLiteralForm)

    def test_preferred_text_checks_direct_and_xl_paths(self):
        graph = fixture()
        graph.add((EX.a, XL.prefLabel, EX.second))
        graph.add((EX.second, RDF.type, XL.Label))
        graph.add((EX.second, XL.literalForm, Literal("another", lang="en")))
        self.assert_rule(graph, RULE.PreferredTextUnique)

    def test_role_conflict_is_detected_across_distinct_label_records(self):
        graph = fixture()
        graph.add((EX.a, XL.altLabel, EX.alias))
        graph.add((EX.alias, RDF.type, XL.Label))
        graph.add((EX.alias, XL.literalForm, Literal("a", lang="en")))
        self.assert_rule(graph, RULE.LabelRoleDisjoint)

    def test_plain_skos_remains_standard_valid_but_does_not_meet_target_xl(self):
        graph = fixture(); graph.remove((EX.a, XL.prefLabel, None))
        self.assertTrue(self.run_shapes(graph, "standard")[0])
        self.assert_rule(graph, RULE.ConceptXLNames)

    def test_projection_is_required_by_target_without_changing_data(self):
        graph = fixture(); graph.remove((EX.a, SKOS.prefLabel, None))
        self.assertTrue(self.run_shapes(graph, "standard")[0])
        self.assert_rule(graph, RULE.XLProjection)

    def test_scheme_membership_and_empty_graph_cannot_pass_target(self):
        self.assert_rule(Graph(), RULE.SingleScheme)
        graph = fixture(); graph.remove((EX.a, SKOS.inScheme, None))
        self.assert_rule(graph, RULE.ConceptSchemeMembership)
        graph = fixture(); graph.add((EX.a, SKOS.inScheme, EX.missing))
        self.assert_rule(graph, RULE.ConceptSchemeMembership)

    def test_mapping_conflict_uses_symmetric_transitive_exact_match(self):
        graph = fixture()
        graph.add((EX.b, SKOS.exactMatch, EX.a))
        graph.add((EX.b, SKOS.exactMatch, EX.c))
        graph.add((EX.a, SKOS.broadMatch, EX.c))
        self.assert_rule(graph, RULE.ExactMappingConflict)

    def test_hierarchy_conflict_includes_inverse_and_mapping_paths(self):
        graph = fixture()
        graph.add((EX.b, SKOS.narrower, EX.a))
        graph.add((EX.b, SKOS.broadMatch, EX.c))
        graph.add((EX.c, SKOS.relatedMatch, EX.a))
        self.assert_rule(graph, RULE.RelatedHierarchyConflict)

    def test_two_close_matches_do_not_imply_exact_or_hierarchy(self):
        graph = fixture()
        graph.add((EX.a, SKOS.closeMatch, EX.b))
        graph.add((EX.b, SKOS.closeMatch, EX.c))
        graph.add((EX.a, SKOS.broadMatch, EX.c))
        self.assertTrue(self.run_shapes(graph)[0])

    def test_source_self_relation_is_diagnostic_not_a_standard_violation(self):
        graph = fixture(); graph.add((EX.a, SKOS.related, EX.a))
        self.assertTrue(self.run_shapes(graph, "standard")[0])
        _, rows = self.run_shapes(graph)
        self.assertEqual({(r["shape"], r["severity"]) for r in rows},
                         {(RULE.SelfRelatedDiagnostic, SH.Warning)})

    def test_quality_diagnostics_do_not_turn_every_source_cycle_into_a_standard_error(self):
        graph = fixture()
        graph.add((EX.a, SKOS.broader, EX.b)); graph.add((EX.b, SKOS.broader, EX.a))
        self.assertTrue(self.run_shapes(graph, "standard")[0])
        _, rows = self.run_shapes(graph)
        self.assertEqual({r["severity"] for r in rows}, {SH.Warning})
        self.assertIn(RULE.HierarchyCycleDiagnostic, {r["shape"] for r in rows})

    def test_ordered_collection_list_and_projection(self):
        graph = fixture(); head = BNode()
        graph.add((EX.group, RDF.type, SKOS.OrderedCollection))
        Collection(graph, head, [EX.a, EX.b])
        graph.add((EX.group, SKOS.memberList, head))
        graph.add((EX.group, SKOS.member, EX.a))
        graph.add((EX.group, SKOS.member, EX.b))
        self.assertTrue(self.run_shapes(graph)[0])
        graph.remove((head, RDF.first, None))
        self.assert_rule(graph, RULE.OrderedListStructure)

    def test_ordered_list_cycle_and_extra_member_are_detected(self):
        graph = fixture(); head = BNode()
        graph.add((EX.group, RDF.type, SKOS.OrderedCollection))
        graph.add((EX.group, SKOS.memberList, head))
        graph.add((head, RDF.first, EX.a)); graph.add((head, RDF.rest, head))
        graph.add((EX.group, SKOS.member, EX.a))
        self.assert_rule(graph, RULE.OrderedListStructure)
        graph.set((head, RDF.rest, RDF.nil))
        graph.add((EX.group, SKOS.member, EX.b))
        self.assert_rule(graph, RULE.OrderedMembersProjection)

    def test_empty_collection_is_info_and_no_name_is_required(self):
        graph = fixture(); graph.add((EX.group, RDF.type, SKOS.OrderedCollection))
        graph.add((EX.group, SKOS.memberList, RDF.nil))
        _, rows = self.run_shapes(graph)
        self.assertTrue(rows)
        self.assertEqual({(r["shape"], r["severity"]) for r in rows},
                         {(RULE.EmptyCollection, SH.Info)})

    def test_group_array_disjointness_and_transitive_member_inclusion(self):
        graph = fixture()
        for node in (EX.g1, EX.g2, EX.g3):
            graph.add((node, RDF.type, ISO.ConceptGroup))
            graph.add((node, RDF.type, SKOS.Collection))
            graph.add((node, SKOS.member, EX.b))
        graph.add((EX.g1, ISO.superGroup, EX.g2))
        graph.add((EX.g2, ISO.superGroup, EX.g3))
        graph.add((EX.g1, SKOS.member, EX.a))
        graph.add((EX.g2, SKOS.member, EX.a))
        self.assert_rule(graph, RULE.GroupMemberInclusion)
        graph.add((EX.g3, SKOS.member, EX.a))
        self.assertTrue(self.run_shapes(graph)[0])
        graph.add((EX.g1, RDF.type, ISO.ThesaurusArray))
        self.assert_rule(graph, RULE.GroupArrayDisjoint)

    def test_local_requirements_need_explicit_targets_not_uri_guessing(self):
        graph = fixture(); graph.add((EX.inherited, RDF.type, SKOS.Concept))
        graph.add((EX.inherited, SKOS.inScheme, EX.scheme))
        _, rows = self.run_shapes(graph)
        self.assertEqual({r["severity"] for r in rows}, {SH.Warning})
        self.assert_rule(graph, RULE.LocalConceptName,
                         targets=[(RULE.LocalConcept, EX.inherited)])
        graph = fixture()
        graph.add((EX.a, DCTERMS.created, Literal("2020-01-01", datatype=XSD.date)))
        graph.add((EX.a, DCTERMS.created, Literal("2021-01-01", datatype=XSD.date)))
        self.assertTrue(self.run_shapes(graph)[0])
        self.assert_rule(graph, RULE.LocalCreated,
                         targets=[(RULE.LocalDates, EX.a)])

    def test_metadata_keeps_legal_literals_resources_and_note_references(self):
        graph = fixture()
        graph.add((EX.scheme, DCTERMS.language, Literal("en")))
        graph.add((EX.a, DCTERMS.type, EX.controlledType))
        graph.add((EX.a, DCTERMS.format, Literal("text/plain")))
        graph.add((EX.a, DCTERMS.subject, Literal("subject text")))
        graph.add((EX.a, SKOS.definition, EX.external_document))
        graph.add((EX.a, SKOS.note, BNode("source-note")))
        graph.add((BNode("source-note"), RDF.value, Literal("one", lang="en")))
        graph.add((BNode("source-note"), RDF.value, Literal("二", lang="zh")))
        self.assertTrue(self.run_shapes(graph)[0])

    def test_severity_is_set_on_each_rule_and_not_lost_in_execution(self):
        graph = fixture(); graph.add((EX.aLabel, XL.literalForm, Literal("another")))
        graph.add((EX.a, SKOS.exactMatch, EX.b))
        graph.add((EX.a, SKOS.broadMatch, EX.b))
        for severity in (SH.Violation, SH.Warning, SH.Info):
            with self.subTest(severity=severity):
                def change(shapes):
                    shapes.set((RULE.LabelLiteralForm, SH.severity, severity))
                _, rows = self.run_shapes(graph, "standard", mutate_shapes=change)
                matched = [r for r in rows if r["shape"] == RULE.LabelLiteralForm]
                self.assertTrue(matched)
                self.assertEqual({r["severity"] for r in matched}, {severity})
                others = [r for r in rows if r["shape"] == RULE.ExactMappingConflict]
                self.assertTrue(others)
                self.assertEqual({r["severity"] for r in others}, {SH.Violation})

    def test_source_untagged_text_is_a_warning_and_local_language_is_required(self):
        graph = fixture()
        graph.set((EX.aLabel, XL.literalForm, Literal("a")))
        graph.set((EX.a, SKOS.prefLabel, Literal("a")))
        _, rows = self.run_shapes(graph)
        self.assertEqual({r["severity"] for r in rows}, {SH.Warning})
        self.assert_rule(graph, RULE.LocalLabelLanguage,
                         targets=[(RULE.LocalLabel, EX.aLabel)])

    def test_language_variants_are_distinct_and_shared_label_roles_are_local(self):
        graph = fixture()
        for suffix, language in (("us", "en-US"), ("gb", "en-GB")):
            label = EX[suffix]
            text = Literal(suffix, lang=language)
            graph.add((EX.a, XL.prefLabel, label))
            graph.add((label, RDF.type, XL.Label))
            graph.add((label, XL.literalForm, text))
            graph.add((EX.a, SKOS.prefLabel, text))
        graph.add((EX.b, XL.altLabel, EX.aLabel))
        graph.add((EX.b, SKOS.altLabel, Literal("a", lang="en")))
        self.assertTrue(self.run_shapes(graph)[0])

    def test_no_extra_collection_name_requirement_and_no_missing_list_exemption(self):
        graph = fixture()
        graph.add((EX.group, RDF.type, SKOS.Collection))
        graph.add((EX.group, SKOS.member, EX.a))
        graph.add((EX.group, SKOS.inScheme, EX.scheme))
        graph.add((EX.group, SKOS.scopeNote, Literal("Example group", lang="en")))
        self.assertTrue(self.run_shapes(graph, targets=[(RULE.LocalCollection, EX.group)])[0])
        graph.add((EX.group, RDF.type, SKOS.OrderedCollection))
        self.assert_rule(graph, RULE.OrderedListRequired)
        graph.add((EX.group, SKOS.memberList, RDF.nil))
        other = BNode(); Collection(graph, other, [EX.a])
        graph.add((EX.group, SKOS.memberList, other))
        self.assert_rule(graph, RULE.OrderedListRequired)

    def test_known_structural_domains_and_ranges_participate_in_type_conflicts(self):
        triples = (
            (EX.aLabel, SKOS.topConceptOf, EX.scheme),
            (EX.a, SKOS.member, EX.b),
            (EX.aLabel, SKOS.inScheme, EX.a),
            (EX.a, SKOS.hasTopConcept, EX.b),
            (EX.aLabel, SKOS.member, EX.b),
        )
        for triple in triples:
            with self.subTest(triple=triple):
                graph = fixture(); graph.add(triple)
                self.assertFalse(self.run_shapes(graph, "standard")[0])
        graph = fixture()
        graph.add((EX.untyped, SKOS.member, EX.b))
        graph.add((EX.untyped, XL.literalForm, Literal("name", lang="en")))
        self.assertFalse(self.run_shapes(graph, "standard")[0])
        graph = fixture(); graph.add((EX.aLabel, SKOS.inScheme, EX.scheme))
        self.assertTrue(self.run_shapes(graph)[0])

    def test_source_xml_note_is_not_forced_to_plain_text(self):
        graph = fixture()
        graph.add((EX.a, SKOS.note, Literal('<p xmlns="http://www.w3.org/1999/xhtml">Text</p>', datatype=RDF.XMLLiteral)))
        self.assertTrue(self.run_shapes(graph)[0])

    def test_two_equal_lists_are_not_a_standard_inconsistency(self):
        graph = fixture(); graph.add((EX.group, RDF.type, SKOS.OrderedCollection))
        for _ in range(2):
            head = BNode(); Collection(graph, head, [EX.a])
            graph.add((EX.group, SKOS.memberList, head))
        graph.add((EX.group, SKOS.member, EX.a))
        self.assertTrue(self.run_shapes(graph, "standard")[0])
        self.assert_rule(graph, RULE.OrderedListRequired)

    def test_target_explicit_types_are_not_satisfied_only_by_subclass_membership(self):
        for node, base_type, subclass in (
            (EX.a, SKOS.Concept, EX.SpecialConcept),
            (EX.aLabel, XL.Label, EX.SpecialLabel),
            (EX.scheme, SKOS.ConceptScheme, EX.SpecialScheme),
        ):
            with self.subTest(base_type=base_type):
                graph = fixture(); graph.remove((node, RDF.type, base_type))
                graph.add((subclass, RDFS.subClassOf, base_type))
                graph.add((node, RDF.type, subclass))
                self.assertTrue(self.run_shapes(graph, "standard")[0])
                self.assertFalse(self.run_shapes(graph)[0])
                graph.add((node, RDF.type, base_type))
                self.assertTrue(self.run_shapes(graph)[0])
        graph = fixture()
        graph.add((EX.group, RDF.type, EX.SpecialCollection))
        graph.add((EX.SpecialCollection, RDFS.subClassOf, SKOS.Collection))
        graph.add((EX.group, SKOS.member, EX.a))
        self.assertTrue(self.run_shapes(graph, "standard")[0])
        self.assertFalse(self.run_shapes(graph)[0])
        graph.add((EX.group, RDF.type, SKOS.Collection))
        self.assertTrue(self.run_shapes(graph)[0])

    def test_local_note_requirement_does_not_target_every_external_reference(self):
        graph = fixture(); graph.add((EX.a, SKOS.definition, EX.reference))
        self.assertTrue(self.run_shapes(graph)[0])
        graph.add((EX.note, RDF.value, Literal("one", lang="en")))
        graph.add((EX.note, RDF.value, Literal("二", lang="zh")))
        self.assertTrue(self.run_shapes(graph)[0])
        self.assert_rule(graph, RULE.LocalNoteBody, targets=[(RULE.LocalNote, EX.note)])

    def test_structural_records_cannot_avoid_explicit_types(self):
        graph = fixture()
        graph.remove((EX.a, RDF.type, SKOS.Concept))
        graph.add((EX.a, SKOS.topConceptOf, EX.scheme))
        self.assertTrue(self.run_shapes(graph, "standard")[0])
        self.assert_rule(graph, RULE.DeclaredConceptType)
        graph = fixture()
        graph.add((EX.group, SKOS.member, EX.a))
        self.assertTrue(self.run_shapes(graph, "standard")[0])
        self.assert_rule(graph, RULE.DeclaredCollectionType)
        graph.add((EX.group, RDF.type, SKOS.Collection))
        self.assertTrue(self.run_shapes(graph)[0])
        graph.add((EX.group, SKOS.memberList, RDF.nil))
        self.assert_rule(graph, RULE.DeclaredOrderedCollectionType)


if __name__ == "__main__":
    unittest.main()
