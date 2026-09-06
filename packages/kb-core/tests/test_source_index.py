import json
import pathlib
import unittest
import yaml

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
    def test_term_history_and_field_evidence_are_indexed_without_audit_values(self):
        with materialized_current_layout(FIXTURE) as root:
            document = yaml.safe_load(
                (ROOT / "tests/fixtures/terminology/valid/minimal-active.yaml").read_text()
            )
            concept = document["concepts"][0]
            concept["history"][0]["before"] = {"basis": [{"entity": "audit-only", "locator": "old"}]}
            path = root / "data/vocab/terms.yaml"
            path.write_text(yaml.safe_dump(document), encoding="utf-8")
            rows = [row for row in build_reference_index(root)["entries"]
                    if row["file"] == "data/vocab/terms.yaml"]

        paths = {row["field_path"] for row in rows}
        self.assertIn("concepts[0].history[0].decision", paths)
        self.assertIn("concepts[0].languages[0].terms[0].history[0].decision", paths)
        self.assertIn("concepts[0].definitions[0].basis[0].entity", paths)
        self.assertNotIn("audit-only", {row["target_id"] for row in rows})

    def test_term_model_basis_is_not_a_source_but_external_term_basis_remains(self):
        with materialized_current_layout(FIXTURE) as root:
            document = yaml.safe_load(
                (ROOT / "tests/fixtures/terminology/valid/minimal-active.yaml").read_text()
            )
            terms = document["concepts"][0]["languages"][0]["terms"]
            terms[0]["basis"] = {
                "level": 5,
                "model": {
                    "name": "GPT-5", "date": "2026-09-06",
                    "rationale": "Existing Chinese industry expression.",
                    "approval": "decision-term-0001",
                },
            }
            path = root / "data/vocab/terms.yaml"
            path.write_text(yaml.safe_dump(document), encoding="utf-8")
            rows = [row for row in build_reference_index(root)["entries"]
                    if row["file"] == "data/vocab/terms.yaml"]

        source_paths = {
            row["field_path"] for row in rows
            if row["target_kind"] in {"source_entity", "source_use"}
        }
        self.assertNotIn("concepts[0].languages[0].terms[0].basis.level", source_paths)
        self.assertIn("concepts[0].languages[0].terms[1].basis[0].entity", source_paths)
        self.assertIn("concepts[0].definitions[0].basis[0].entity", source_paths)

    def test_project_basis_approval_is_internal_and_audit_snapshots_are_not_current(self):
        with materialized_current_layout(FIXTURE) as root:
            document = yaml.safe_load(
                (ROOT / "tests/fixtures/terminology/valid/minimal-active.yaml").read_text()
            )
            concept = document["concepts"][0]
            basis = {"project": {"approval": "decision-project-current",
                "origin": {"commit": "a" * 40, "file": "docs/project.md", "locator": "Scope"},
                "rationale": "Existing project meaning"}}
            concept["basis"] = basis
            concept["definitions"][0]["basis"] = basis
            concept["languages"][0]["terms"][0]["basis"] = basis
            concept["history"][0]["before"] = {"basis": {"project": {"approval": "audit-only"}}}
            (root / "data/vocab/terms.yaml").write_text(yaml.safe_dump(document))
            rows = [row for row in build_reference_index(root)["entries"]
                    if row["file"] == "data/vocab/terms.yaml"]
        approvals = {row["field_path"] for row in rows
                     if row["target_kind"] == "decision" and row["target_id"] == "decision-project-current"}
        self.assertEqual({"concepts[0].basis.project.approval",
                          "concepts[0].definitions[0].basis.project.approval",
                          "concepts[0].languages[0].terms[0].basis.project.approval"}, approvals)
        self.assertNotIn("audit-only", {row["target_id"] for row in rows})
        self.assertFalse(any(row["target_kind"] == "source_entity" and ".project." in row["field_path"]
                             for row in rows))

    def entries(self):
        with materialized_current_layout(FIXTURE) as root:
            return build_reference_index(root)["entries"]

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

    def test_structured_language_evidence_tracks_uses_without_model_sources(self):
        """Missing label evidence would understate a source change's actual impact."""
        with materialized_current_layout(FIXTURE) as root:
            path = root / "data/vocab/label-evidence.yaml"
            path.write_text(
                "concepts:\n"
                "  - id: reading-topic\n"
                "    basis:\n"
                "      zh: {level: 1, references: [{source: source-main, locator: '520'}]}\n"
                "      en: {level: 5, model: {name: model, rationale: existing knowledge}}\n"
                "  - id: untranslated\n"
                "    basis: {en: {legacy: none}}\n", encoding="utf-8",
            )
            entries = [row for row in build_reference_index(root)["entries"]
                       if row["file"] == "data/vocab/label-evidence.yaml"]
        self.assertEqual([{
            "target_kind": "source_use", "target_id": "source-main",
            "reference_kind": "label_basis.source", "file": "data/vocab/label-evidence.yaml",
            "record": "concepts:reading-topic", "field_path": "concepts[0].basis.zh.references[0].source",
        }], entries)

    def test_two_runs_are_byte_identical(self):
        self.assertEqual(self.entries(), self.entries())

    def test_record_decisions_are_indexed_without_audit_payload_references(self):
        with materialized_current_layout(FIXTURE) as root:
            before = index_reference_set(build_reference_index(root)['entries'])
            for filename, collection in [('entities', 'entities'), ('sources', 'sources')]:
                path = root / f'data/vocab/{filename}.yaml'
                document = load_yaml(path)
                document[collection][0]['history'] = [{
                    'decisions': [f'decision-{filename}-history'],
                    'before': {'decisions': ['audit-only-before'],
                               'match': [{'registry': 'audit-only-use'}]},
                    'after': {'decision': 'audit-only-after'},
                }]
                path.write_text(yaml.safe_dump(document), encoding='utf-8')
            (root / 'data/vocab/forms.yaml').write_text(yaml.safe_dump({'arrays': [{
                'id': 'isolated', 'local_analysis': {'state': 'isolated',
                    'legacy_source_label': 'audit-only-label', 'decision': 'decision-isolation'},
            }]}), encoding='utf-8')
            (root / 'docs/decisions/source-audit.md').write_text(
                '---\nid: decision-audit\nanswers:\n  - patches:\n'
                '      - value: {decision: audit-only-patch, match: [{registry: audit-only-use}]}\n---\n',
                encoding='utf-8')
            added = index_reference_set(build_reference_index(root)['entries']) - before
        self.assertEqual({
            ('decision', 'decision-entities-history', 'history.decision',
             'data/vocab/entities.yaml', 'entity:source-main', 'entities[0].history[0].decisions[0]'),
            ('decision', 'decision-sources-history', 'history.decision',
             'data/vocab/sources.yaml', 'source_use:use-main', 'sources[0].history[0].decisions[0]'),
            ('decision', 'decision-isolation', 'local_analysis.decision',
             'data/vocab/forms.yaml', 'arrays:isolated', 'arrays[0].local_analysis.decision'),
        }, added)

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
        rows = [row for row in self.entries() if "local_analysis" in row["field_path"]
                and row["target_kind"] in {"source_entity", "source_use"}]
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
