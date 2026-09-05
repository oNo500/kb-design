import json
import pathlib
import unittest

from kb_core.build_source_index import build_reference_index
from kb_core.source_model import collect_reference_uses
from source_governance_helpers import load_yaml, materialized_current_layout


ROOT = pathlib.Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "tests" / "fixtures" / "source-governance" / "index-root"
EXPECTED = ROOT / "tests" / "fixtures" / "source-governance" / "index-expected.json"


def reference_key(row):
    return tuple(row[key] for key in
                 ("target_kind", "target_id", "reference_kind", "file", "record", "field_path"))


def formal_reference_set(root):
    del root
    rows = json.loads(EXPECTED.read_text(encoding="utf-8"))
    for row in rows:
        if row["file"].startswith("vocab/"):
            row["file"] = "data/" + row["file"]
        elif row["file"].startswith("design/decisions/"):
            row["file"] = "docs/decisions/" + row["file"].removeprefix(
                "design/decisions/"
            )
    return {reference_key(row) for row in rows}


def index_reference_set(entries):
    return {reference_key(row) for row in entries}


def reference_use_index_key(use):
    if use.kind == "basis":
        return ("source_entity", use.value["entity"], "basis.entity", use.file,
                use.record, use.field_path + ".entity")
    return ("source_use", use.value["registry"], f"{use.kind}.registry", use.file,
            use.record, use.field_path + ".registry")


class SourceIndexTests(unittest.TestCase):
    def entries(self, legacy=False):
        with materialized_current_layout(FIXTURE) as root:
            return build_reference_index(root, include_legacy=legacy)["entries"]

    def test_index_covers_all_required_reference_kinds(self):
        kinds = {row["reference_kind"] for row in self.entries()}
        required = {"basis.entity", "source.registry", "match.registry", "use.entity",
                    "entity.replaced_by", "role.decision", "obligation.decisions",
                    "obligation.previous", "history.decision", "obligation.target"}
        self.assertTrue(required <= kinds)

    def test_every_reference_has_stable_record_and_field_path(self):
        self.assertTrue(all(row["record"] and row["field_path"] for row in self.entries()))

    def test_index_and_formal_references_are_bidirectionally_equal(self):
        self.assertEqual(formal_reference_set(FIXTURE), index_reference_set(self.entries()))

    def test_legacy_mode_includes_generator_and_array_inputs(self):
        legacy_kinds = {
            "legacy.basis", "legacy.source", "legacy.match", "legacy.array_source"
        }
        with materialized_current_layout(FIXTURE) as root:
            input_directory = root / "data" / "inputs" / "topics"
            input_directory.mkdir(parents=True)
            (root / "data/vocab/legacy.yaml").replace(
                input_directory / "legacy.yaml"
            )

            default_entries = build_reference_index(root)["entries"]
            legacy_entries = build_reference_index(root, include_legacy=True)["entries"]

        self.assertTrue(legacy_kinds.isdisjoint(
            {row["reference_kind"] for row in default_entries}
        ))
        self.assertTrue(legacy_kinds <= {
            row["reference_kind"] for row in legacy_entries
        })
        self.assertEqual(
            {"data/inputs/topics/legacy.yaml"},
            {
                row["file"]
                for row in legacy_entries
                if row["reference_kind"] in legacy_kinds
            },
        )

    def test_two_runs_are_byte_identical(self):
        self.assertEqual(self.entries(), self.entries())

    def test_repository_outputs_are_outside_formal_document_discovery(self):
        with materialized_current_layout(FIXTURE) as root:
            expected = build_reference_index(root)
            output = root / "output" / "obsidian" / "shadow.yaml"
            output.parent.mkdir(parents=True)
            output.write_text(
                "records:\n"
                "  - id: shadow\n"
                "    basis:\n"
                "      - {entity: source-main, locator: generated-output}\n",
                encoding="utf-8",
            )

            self.assertEqual(expected, build_reference_index(root))

    def test_future_terms_consumer_is_found_without_new_visitor(self):
        fixture = ROOT / "tests/fixtures/source-governance/future-consumer"
        with materialized_current_layout(fixture) as root:
            entries = build_reference_index(root)["entries"]
        paths = {
            row["field_path"]
            for row in entries
            if row["file"] == "data/vocab/terms.yaml"
        }
        self.assertEqual({"concepts[0].basis[0].entity", "concepts[0].source.registry",
                          "concepts[0].match[0].registry",
                          "concepts[0].terms[0].basis[0].entity"}, paths)

    def test_isolated_local_analysis_is_not_a_source_reference(self):
        rows = [row for row in self.entries() if "local_analysis" in row["field_path"]]
        self.assertEqual([], rows)

    def test_external_group_is_indexed_as_structure_use(self):
        rows = [row for row in self.entries()
                if row["reference_kind"] == "external_group.registry"]
        self.assertEqual(24, len(rows))
        self.assertTrue(all(row["target_kind"] == "source_use" for row in rows))

    def test_index_shared_rows_equal_public_collector_rows(self):
        document_path = FIXTURE / "vocab/topics.yaml"
        uses = collect_reference_uses(
            pathlib.Path("data/vocab/topics.yaml"), load_yaml(document_path)
        )
        expected = {reference_use_index_key(use) for use in uses}
        actual = {reference_key(row) for row in self.entries()
                  if row["reference_kind"] in {"basis.entity", "source.registry",
                                                "match.registry", "external_group.registry"}
                  and row["file"] == "data/vocab/topics.yaml"}
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
