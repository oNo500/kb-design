"""Prevent missing schema fields, incorrect denominators and silent omissions."""
import contextlib
import io
import json
from pathlib import Path
import re
import tempfile
import unittest

from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, SKOS
from rdflib.namespace import SH

from kb_vocab_shacl import read_shapes
from kb_vocab_shacl.cli import main
from kb_vocab_shacl.inventory import inventory
from kb_vocab_shacl.report import markdown
from kb_vocab_shacl.structure import fields_for, load_structure

EX = Namespace("https://example.org/inventory/")
RESOURCE = Namespace("urn:kb-vocab-shacl:resource:")


class InventoryTests(unittest.TestCase):
    def test_structure_rejects_empty_name_values_in_each_role(self):
        from pyshacl import validate
        xl = Namespace("http://www.w3.org/2008/05/skos-xl#")
        example = Path(__file__).resolve().parents[1] / "examples/valid.ttl"
        for predicate in (SKOS.prefLabel, SKOS.altLabel, SKOS.hiddenLabel, xl.literalForm):
            with self.subTest(predicate=predicate):
                data = Graph().parse(example, format="turtle")
                node = next(data.subjects(RDF.type, xl.Label if predicate == xl.literalForm else SKOS.Concept))
                data.set((node, predicate, Literal("", lang="en")))
                shapes, _ = load_structure()
                conforms, report, _ = validate(data, shacl_graph=shapes)
                self.assertFalse(conforms)
                self.assertIn(predicate, set(report.objects(None, SH.resultPath)))

    def test_structural_properties_select_records_missing_their_type(self):
        from pyshacl import validate
        xl = Namespace("http://www.w3.org/2008/05/skos-xl#")
        iso = Namespace("http://purl.org/iso25964/skos-thes#")
        example = Path(__file__).resolve().parents[1] / "examples/valid.ttl"
        cases = (
            ("Label", xl.literalForm, Literal("orphan", lang="en")),
            ("Collection", SKOS.member, Namespace("https://example.org/vocab/").concept),
            ("OrderedCollection", SKOS.memberList, RDF.nil),
            ("Concept", SKOS.broader, Namespace("https://example.org/vocab/").concept),
            ("ConceptScheme", SKOS.hasTopConcept, Namespace("https://example.org/vocab/").concept),
            ("ConceptGroup", iso.superGroup, EX.parent),
        )
        for kind, predicate, value in cases:
            with self.subTest(kind=kind):
                data = Graph().parse(example, format="turtle")
                data.add((EX.untyped, predicate, value))
                shapes, roots = load_structure()
                group = inventory(data, structure=shapes, roots=roots, resource_type=kind)["resources"][0]
                self.assertEqual(group["status"], "counted")
                field = next(r for r in group["fields"] if r["field"] == str(RDF.type))
                self.assertGreaterEqual(field["absent"], 1)
                conforms, report, _ = validate(data, shacl_graph=shapes)
                self.assertFalse(conforms)
                failures = [r for r in report.subjects(SH.focusNode, EX.untyped)
                            if report.value(r, SH.resultPath) == RDF.type]
                self.assertTrue(failures)

    def test_condition_scopes_are_explicit_and_never_claim_inventory_validates(self):
        rules = Namespace("urn:kb-vocab-shacl:")
        data = Graph()
        data.add((EX.a, RDF.type, SKOS.OrderedCollection))
        shapes, roots = load_structure()
        result = inventory(data, structure=shapes, roots=roots, resource_type="OrderedCollection")
        self.assertIn("conditions", result)
        dates = next(r for r in result["conditions"] if r["shape"] == str(rules.LocalDates))
        self.assertEqual(dates["scope_status"], "unspecified")
        self.assertIsNone(dates["selected_objects"])
        self.assertFalse(dates["validation_executed"])
        self.assertIn("未指定", markdown(result))
        shapes.add((rules.LocalDates, SH.targetNode, EX.a))
        result = inventory(data, structure=shapes, roots=roots, resource_type="OrderedCollection")
        dates = next(r for r in result["conditions"] if r["shape"] == str(rules.LocalDates))
        self.assertEqual(dates["scope_status"], "specified")
        self.assertEqual(dates["selected_objects"], 1)
        self.assertFalse(dates["validation_executed"])
        self.assertIn("未执行校验", markdown(result))
        shapes.add((rules.LocalDates, SH.deactivated, Literal(True)))
        result = inventory(data, structure=shapes, roots=roots, resource_type="OrderedCollection")
        dates = next(r for r in result["conditions"] if r["shape"] == str(rules.LocalDates))
        self.assertEqual(dates["scope_status"], "deactivated")

    def test_presence_counts_subjects_not_values_and_optional_fields_remain_visible(self):
        data = Graph()
        for node in (EX.a, EX.b):
            data.add((node, RDF.type, SKOS.Concept))
        data.add((EX.a, SKOS.definition, Literal("one")))
        data.add((EX.a, SKOS.definition, Literal("two")))
        data.add((EX.a, SKOS.prefLabel, Literal("")))
        result = inventory(data, resource_type="Concept")
        group = result["resources"][0]
        fields = {row["field"]: row for row in group["fields"]}
        self.assertEqual(set(fields), {row["field"] for row in result["fields"]})
        self.assertEqual(group["objects"], 2)
        self.assertEqual((fields[str(SKOS.definition)]["present"], fields[str(SKOS.definition)]["absent"], fields[str(SKOS.definition)]["statements"]), (1, 1, 2))
        self.assertEqual(fields[str(SKOS.prefLabel)]["empty_values"], 1)
        self.assertEqual(fields[str(SKOS.example)]["absent"], 2)

    def test_no_objects_differs_from_missing_fields_and_unknown_scope(self):
        groups = {r["type"]: r for r in inventory(Graph())["resources"]}
        self.assertEqual(groups["Label"]["status"], "no_objects")
        self.assertEqual(groups["Label"]["objects"], 0)
        self.assertTrue(all(r["absent"] is None for r in groups["Label"]["fields"]))
        self.assertEqual(groups["Note"]["status"], "scope_required")
        self.assertIsNone(groups["Note"]["objects"])

    def test_fields_come_from_shapes_and_untyped_resources_are_not_lost(self):
        shapes, roots = load_structure()
        field = EX.extraField
        shapes.add((RESOURCE.Concept, SH.property, field))
        shapes.add((field, SH.path, EX.extra))
        data = Graph()
        data.add((EX.a, RDF.type, SKOS.Concept))
        data.add((EX.a, EX.extra, Literal("value")))
        data.add((EX.untyped, EX.extra, Literal("auxiliary")))
        result = inventory(data, structure=shapes, roots=roots, resource_type="Concept")
        row = next(r for r in result["resources"][0]["fields"] if r["field"] == str(EX.extra))
        self.assertEqual(row["present"], 1)
        self.assertIn(str(EX.untyped), result["unclassified_subjects"])
        self.assertEqual(next(r for r in result["fields"] if r["field"] == str(EX.extra))["present_subjects"], 2)

    def test_duplicate_shared_fields_do_not_duplicate_counts_and_subclasses_are_selected(self):
        data = Graph()
        data.add((EX.SubConcept, RDFS.subClassOf, SKOS.Concept))
        data.add((EX.a, RDF.type, EX.SubConcept))
        data.add((EX.a, SKOS.note, Literal("note")))
        group = inventory(data, resource_type="Concept")["resources"][0]
        self.assertEqual(group["objects"], 1)
        notes = [r for r in group["fields"] if r["field"] == str(SKOS.note)]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["present"], 1)

    def test_unsupported_path_and_unknown_resource_selection_fail_explicitly(self):
        shapes, roots = load_structure()
        bad = EX.bad
        shapes.add((RESOURCE.Concept, SH.property, bad))
        shapes.add((bad, SH.path, BNode()))
        with self.assertRaises(ValueError):
            inventory(Graph(), structure=shapes, roots=roots)
        with self.assertRaises(ValueError):
            inventory(Graph(), resource_type="Typo")
        shapes, roots = load_structure()
        shapes.add((RESOURCE.Concept, SH.node, EX.missingComposition))
        with self.assertRaises(ValueError):
            inventory(Graph(), structure=shapes, roots=roots)

    def test_design_field_tables_are_covered_for_each_resource(self):
        shapes, roots = load_structure()
        prefixes = {str(k): str(v) for k, v in shapes.namespaces()}
        prefixes.update(skosxl="http://www.w3.org/2008/05/skos-xl#", **{"iso-thes": "http://purl.org/iso25964/skos-thes#"})
        doc = Path(__file__).resolve().parents[3] / "docs/model/vocabulary/设计-词表数据规范.md"
        if not doc.exists():
            self.skipTest("Design document is checked in the repository, not distributed in the wheel")
        sections, section = {}, ""
        for line in doc.read_text().splitlines():
            if line.startswith("##"):
                section = line.lstrip("#").strip()
            if line.startswith("|"):
                for field in re.findall(r"`([a-z-]+:[A-Za-z]+)`", line.split("|")[1]):
                    prefix, name = field.split(":")
                    sections.setdefault(section, set()).add(prefixes[prefix] + name)
        all_declared = {str(p) for root in roots for p in fields_for(shapes, root)}
        for section, required in sections.items():
            self.assertFalse(required - all_declared, (section, required - all_declared))
        for name, section in (("Concept", "概念字段"), ("ConceptScheme", "词表字段"), ("Label", "名称字段"), ("Collection", "集合字段")):
            declared = {str(p) for p in fields_for(shapes, RESOURCE[name])}
            required = sections[section] | sections["来源兼容字段"] | (sections["说明字段"] - {str(RDF.value)})
            self.assertFalse(required - declared, (name, required - declared))

    def test_structure_is_executable_and_reuses_existing_field_constraints(self):
        from pyshacl import validate
        example = Path(__file__).resolve().parents[1] / "examples/valid.ttl"
        data = Graph().parse(example, format="turtle")
        shapes = Graph().parse(data=read_shapes("structure"), format="turtle")
        self.assertTrue(validate(data, shacl_graph=shapes, meta_shacl=True)[0])
        XL = Namespace("http://www.w3.org/2008/05/skos-xl#")
        label = next(data.subjects(RDF.type, XL.Label))
        data.add((label, XL.literalForm, Literal("another")))
        conforms, report, _ = validate(data, shacl_graph=shapes)
        self.assertFalse(conforms)
        self.assertIn(Namespace("urn:kb-vocab-shacl:").LabelLiteralForm, set(report.objects(None, SH.sourceShape)))

    def test_cli_counts_relative_iris_preserves_input_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "input.ttl"
            source.write_text('@prefix skos: <http://www.w3.org/2004/02/skos/core#> . <concept> a skos:Concept .')
            original = source.read_bytes()
            output = root / "report"
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(["inventory", str(source), "--type", "Concept", "--output", str(output)]), 0)
                first = (output / "inventory.json").read_bytes()
                self.assertEqual(main(["inventory", str(source), "--output", str(output)]), 2)
                self.assertEqual((output / "inventory.json").read_bytes(), first)
            self.assertEqual(source.read_bytes(), original)
            result = json.loads(first)
            self.assertEqual(result["resources"][0]["objects"], 1)
            self.assertFalse(result["run"]["shacl_validation_executed"])


if __name__ == "__main__":
    unittest.main()
