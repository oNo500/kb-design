"""Protect source preservation, XL identity, three-way conflicts and retry integrity."""
import json
from pathlib import Path
import tempfile
import unittest

from rdflib import Graph, Literal, Namespace, RDF, SKOS, URIRef
from rdflib.namespace import DCTERMS

from kb_vocab_maintenance.diff import canonical_bytes, compare_files, compare_graphs, parse_turtle
from kb_vocab_maintenance.edit import EditConflict, apply_edit, prepare_edit

XL = Namespace("http://www.w3.org/2008/05/skos-xl#")
C = URIRef("urn:concept:one")
L = URIRef("urn:label:one")
BASE = '''@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xl: <http://www.w3.org/2008/05/skos-xl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
<urn:concept:one> a skos:Concept; skos:prefLabel "Old"@en;
    xl:prefLabel <urn:label:one>; skos:definition "Original"@en .
<urn:label:one> a xl:Label; xl:literalForm "Old"@en .
'''


class EditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "source.ttl"
        self.source.write_text(BASE)
        self.plan = self.root / "plan.json"

    def prepare(self, subject=L, predicate=XL.literalForm, after=None):
        return prepare_edit(self.source, [{"subject": str(subject), "predicate": str(predicate),
                            "after": after if after is not None else ['"New"@en']}], self.plan,
                            reason="Correct the recorded spelling", authorization="urn:decision:reviewed-edit")

    def test_rename_preserves_label_identity_and_all_shared_projections(self):
        self.source.write_text(BASE + '<urn:concept:two> a skos:Concept; xl:altLabel <urn:label:one>; skos:altLabel "Old"@en .\n')
        raw = self.source.read_bytes()
        plan = self.prepare()
        self.assertEqual(plan["changes"][0]["before"], ['"Old"@en'])
        self.assertEqual(plan["changes"][0]["after"], ['"New"@en'])
        output = self.root / "result"
        apply_edit(self.plan, self.source, output)
        graph = Graph().parse(output / "vocabulary.ttl")
        self.assertEqual(set(graph.subjects(RDF.type, XL.Label)), {L})
        self.assertEqual(set(graph.objects(L, XL.literalForm)), {Literal("New", lang="en")})
        self.assertIn((C, SKOS.prefLabel, Literal("New", lang="en")), graph)
        self.assertIn((URIRef("urn:concept:two"), SKOS.altLabel, Literal("New", lang="en")), graph)
        self.assertNotIn((C, SKOS.prefLabel, Literal("Old", lang="en")), graph)
        self.assertEqual(self.source.read_bytes(), raw)
        diff = json.loads((output / "version-diff.json").read_text())
        changed = {(node["uri"], field["predicate"]) for node in diff["changed_nodes"] for field in node["fields"]}
        self.assertEqual(changed, {(str(L), str(XL.literalForm)), (str(C), str(SKOS.prefLabel)),
                                   ("urn:concept:two", str(SKOS.altLabel))})

    def test_three_way_merge_preserves_unrelated_upstream_change(self):
        self.prepare()
        current = self.root / "current.ttl"
        current.write_text(BASE.replace('"Original"@en', '"Updated upstream"@en'))
        output = self.root / "result"
        apply_edit(self.plan, current, output)
        graph = Graph().parse(output / "vocabulary.ttl")
        self.assertIn((C, SKOS.definition, Literal("Updated upstream", lang="en")), graph)
        self.assertIn((L, XL.literalForm, Literal("New", lang="en")), graph)

    def test_changed_target_returns_three_values_without_partial_output(self):
        self.prepare()
        current = self.root / "current.ttl"
        current.write_text(BASE.replace('"Old"@en', '"Incoming"@en'))
        output = self.root / "result"
        with self.assertRaises(EditConflict) as raised:
            apply_edit(self.plan, current, output)
        field = next(row for row in raised.exception.conflicts if row["predicate"] == str(XL.literalForm))
        self.assertEqual(field["before"], ['"Old"@en'])
        self.assertEqual(field["current"], ['"Incoming"@en'])
        self.assertEqual(field["after"], ['"New"@en'])
        self.assertFalse(output.exists())
        self.assertIn('"Incoming"@en', current.read_text())

    def test_changed_shared_label_usage_requires_new_review(self):
        self.prepare()
        current = self.root / "current.ttl"
        current.write_text(BASE + '<urn:concept:two> a skos:Concept; xl:prefLabel <urn:label:one>; skos:prefLabel "Old"@en .\n')
        with self.assertRaises(EditConflict):
            apply_edit(self.plan, current, self.root / "result")

    def test_drift_in_pinned_baseline_is_rejected_even_if_target_matches(self):
        self.prepare()
        self.source.write_text(BASE + '<urn:other> dcterms:title "Changed baseline"@en .\n')
        with self.assertRaisesRegex(ValueError, "baseline"):
            apply_edit(self.plan, self.source, self.root / "result")

    def test_retry_verifies_complete_bytes_and_rejects_input_drift(self):
        self.prepare()
        current = self.root / "current.ttl"
        current.write_text(BASE)
        output = self.root / "result"
        first = apply_edit(self.plan, current, output)
        before = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in output.iterdir()}
        self.assertEqual(apply_edit(self.plan, current, output), first)
        self.assertEqual(before, {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in output.iterdir()})
        current.write_text(BASE.replace('"Original"@en', '"Drift"@en'))
        with self.assertRaises(ValueError):
            apply_edit(self.plan, current, output)
        current.write_text(BASE)
        (output / "vocabulary.ttl").write_text(BASE)
        with self.assertRaisesRegex(ValueError, "output"):
            apply_edit(self.plan, current, output)

    def test_projection_override_and_ambiguous_preferred_rename_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "XL"):
            self.prepare(subject=C, predicate=SKOS.prefLabel)
        self.source.write_text(BASE + '<urn:concept:one> xl:prefLabel <urn:label:two> .\n<urn:label:two> a xl:Label; xl:literalForm "Old"@en .\n')
        with self.assertRaisesRegex(ValueError, "prefLabel"):
            self.prepare()
        self.assertFalse(self.plan.exists())

    def test_plan_old_value_tampering_cannot_bypass_review_baseline(self):
        self.prepare()
        plan = json.loads(self.plan.read_text())
        plan["changes"][0]["before"] = ['"Incoming"@en']
        self.plan.write_text(json.dumps(plan))
        current = self.root / "current.ttl"
        current.write_text(BASE.replace('"Old"@en', '"Incoming"@en'))
        with self.assertRaisesRegex(ValueError, "baseline"):
            apply_edit(self.plan, current, self.root / "result")

    def test_literal_datatypes_and_existing_languages_are_not_rewritten(self):
        self.source.write_text(BASE + '<urn:concept:one> dcterms:title "Original"@fr; skos:notation "001" .\n')
        self.prepare(subject=C, predicate=DCTERMS.title, after=['"Nouveau"@fr'])
        output = self.root / "result"
        apply_edit(self.plan, self.source, output)
        graph = Graph().parse(output / "vocabulary.ttl")
        self.assertIn((C, DCTERMS.title, Literal("Nouveau", lang="fr")), graph)
        self.assertIn((C, SKOS.notation, Literal("001")), graph)

    def test_untyped_orphan_literal_form_cannot_escape_name_validation(self):
        self.source.write_text(BASE + '<urn:label:orphan> xl:literalForm "Orphan"@en .\n')
        with self.assertRaisesRegex(ValueError, "XL Label"):
            self.prepare()

    def test_upstream_alternate_label_cannot_collide_with_planned_name(self):
        self.prepare()
        current = self.root / "current.ttl"
        current.write_text(BASE + '<urn:concept:one> skos:altLabel "New"@en .\n')
        output = self.root / "result"
        with self.assertRaisesRegex(ValueError, "roles"):
            apply_edit(self.plan, current, output)
        self.assertFalse(output.exists())

    def test_unedited_typed_literal_keeps_lexical_form_and_diff_reports_changes(self):
        self.source.write_text(BASE + '<urn:concept:one> skos:notation "001"^^<http://www.w3.org/2001/XMLSchema#integer> .\n')
        self.prepare(subject=C, predicate=SKOS.definition, after=['"Revised"@en'])
        output = self.root / "result"
        apply_edit(self.plan, self.source, output)
        self.assertIn('"001"^^<http://www.w3.org/2001/XMLSchema#integer>', (output / "vocabulary.ttl").read_text())
        changed = self.root / "changed.ttl"
        changed.write_text(self.source.read_text().replace('"001"', '"1"'))
        diff = compare_files(self.source, changed)
        self.assertFalse(diff["graph_equal"])
        self.assertEqual(diff["changed_nodes"][0]["fields"][0]["predicate"], str(SKOS.notation))

    def test_untyped_target_deleted_upstream_cannot_be_recreated(self):
        self.source.write_text('<urn:note> <http://www.w3.org/2004/02/skos/core#definition> "Old"@en .\n')
        self.prepare(subject=URIRef("urn:note"), predicate=DCTERMS.title, after=['"New"@en'])
        current = self.root / "current.ttl"
        current.write_text("")
        with self.assertRaises(EditConflict):
            apply_edit(self.plan, current, self.root / "result")

    def test_clearing_last_property_cannot_delete_a_resource(self):
        self.source.write_text('<urn:note> <http://www.w3.org/2004/02/skos/core#definition> "Old"@en .\n')
        with self.assertRaisesRegex(ValueError, "delete"):
            self.prepare(subject=URIRef("urn:note"), predicate=SKOS.definition, after=[])


class DifferenceTests(unittest.TestCase):
    def test_turtle_numeric_tokens_are_not_normalized_by_python_number_conversion(self):
        graph = parse_turtle('<urn:item> <urn:integer> +001; <urn:decimal> 01.20; <urn:double> 1e+00 .')
        encoded = canonical_bytes(graph).decode()
        self.assertIn('"+001"^^<http://www.w3.org/2001/XMLSchema#integer>', encoded)
        self.assertIn('"01.20"^^<http://www.w3.org/2001/XMLSchema#decimal>', encoded)
        self.assertIn('"1e+00"^^<http://www.w3.org/2001/XMLSchema#double>', encoded)

    def test_datatype_normalization_that_cannot_be_disabled_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "lexical"):
            parse_turtle('<urn:item> <urn:value> "  x  "^^<http://www.w3.org/2001/XMLSchema#token> .')

    def test_blank_node_renaming_is_ignored_but_fields_keep_all_values(self):
        before = Graph().parse(data='<urn:item> <urn:note> [ <urn:value> "A" ] ; <urn:title> "Old"@en, "旧"@zh .', format="turtle")
        reordered = Graph().parse(data='_:different <urn:value> "A" . <urn:item> <urn:title> "旧"@zh, "Old"@en; <urn:note> _:different .', format="turtle")
        self.assertTrue(compare_graphs(before, reordered)["graph_equal"])
        reordered.remove((URIRef("urn:item"), URIRef("urn:title"), Literal("Old", lang="en")))
        reordered.add((URIRef("urn:item"), URIRef("urn:title"), Literal("New", lang="en")))
        fields = compare_graphs(before, reordered)["changed_nodes"]
        self.assertEqual(fields, [{"uri": "urn:item", "fields": [{"predicate": "urn:title", "before": ['"Old"@en', '"旧"@zh'],
            "after": ['"New"@en', '"旧"@zh'], "added": ['"New"@en'], "removed": ['"Old"@en']}]}])


if __name__ == "__main__":
    unittest.main()
