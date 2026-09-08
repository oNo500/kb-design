import copy
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

from kb_core.governance.build_terms import (
    canonical_json,
    canonical_snapshot,
    load_cutover_state,
    render_glossary,
)
from kb_core.build_source_index import build_reference_index
from kb_core.governance.term_validation import semantic_concept


ROOT = pathlib.Path(__file__).resolve().parents[4]
ACTIVE_STATE = ROOT / "tests/fixtures/terminology/states/active.yaml"
ROLLED_BACK_STATE = ROOT / "tests/fixtures/terminology/states/rolled-back.yaml"
LAYOUT = ROOT / "data/inputs/terminology/glossary-layout.yaml"


def term(term_id, text, status, replaced_by=None):
    value = {
        "id": term_id,
        "text": text,
        "administrative_status": status,
        "basis": [{"source": "fixture-source", "locator": term_id}],
        "history": [],
    }
    if replaced_by is not None:
        value["replaced_by"] = replaced_by
    return value


def concept(concept_id, workflow, subject, languages, definitions):
    return {
        "id": concept_id,
        "subject_fields": [
            {
                "topic_id": subject,
                "basis": [{"source": "fixture-source", "locator": subject}],
            }
        ],
        "definitions": definitions,
        "languages": languages,
        "basis": [{"source": "fixture-source", "locator": concept_id}],
        "source": None,
        "match": [],
        "workflow": workflow,
        "history": [],
    }


class TermGenerationTests(unittest.TestCase):
    def setUp(self):
        preferred_en = "00000000-0000-4000-8000-000000000011"
        self.document = {
            "schema": "urn:kb-design:schema:terms:1",
            "version": 1,
            "concepts": [
                concept(
                    "00000000-0000-4000-8000-000000000002",
                    "active",
                    "basic-unit",
                    [
                        {
                            "language": "en",
                            "terms": [
                                term(
                                    "00000000-0000-4000-8000-000000000013",
                                    "Old English",
                                    "supersededTerm-admn-sts",
                                    preferred_en,
                                ),
                                term(
                                    "00000000-0000-4000-8000-000000000012",
                                    "Allowed English",
                                    "admittedTerm-admn-sts",
                                ),
                                term(
                                    preferred_en,
                                    "Preferred English",
                                    "preferredTerm-admn-sts",
                                ),
                            ],
                        },
                        {
                            "language": "zh-Hans",
                            "terms": [
                                term(
                                    "00000000-0000-4000-8000-000000000014",
                                    "首选中文",
                                    "preferredTerm-admn-sts",
                                )
                            ],
                        },
                    ],
                    [
                        {
                            "language": "en",
                            "text": "An English definition.",
                            "basis": [
                                {"source": "fixture-source", "locator": "definition-en"}
                            ],
                        }
                    ],
                ),
                concept(
                    "00000000-0000-4000-8000-000000000003",
                    "active",
                    "basic-unit",
                    [
                        {
                            "language": "en",
                            "terms": [
                                term(
                                    "00000000-0000-4000-8000-000000000021",
                                    "English only",
                                    "preferredTerm-admn-sts",
                                )
                            ],
                        }
                    ],
                    [
                        {
                            "language": "en",
                            "text": "No approved Chinese form.",
                            "basis": [
                                {"source": "fixture-source", "locator": "definition-only-en"}
                            ],
                        }
                    ],
                ),
                concept(
                    "00000000-0000-4000-8000-000000000001",
                    "candidate",
                    "basic-unit",
                    [
                        {
                            "language": "en",
                            "terms": [
                                term(
                                    "00000000-0000-4000-8000-000000000001",
                                    "Candidate only",
                                    "preferredTerm-admn-sts",
                                )
                            ],
                        }
                    ],
                    [],
                ),
            ],
        }
        self.source_index = {
            "schema": "urn:kb-design:data:source-reference-index",
            "version": 1,
            "targets": {"fixture-source": ["terms"]},
        }
        self.active_state = load_cutover_state(ACTIVE_STATE)
        self.rolled_back_state = load_cutover_state(ROLLED_BACK_STATE)
        self.layout = yaml.safe_load(LAYOUT.read_text(encoding="utf-8"))
        for group in self.layout["groups"]:
            group["members"] = []
        self.layout["groups"][1]["members"] = [
            "00000000-0000-4000-8000-000000000002",
            "00000000-0000-4000-8000-000000000003",
        ]

    def test_generation_is_byte_stable(self):
        first = canonical_snapshot(
            self.document, self.source_index, self.active_state
        )
        reordered = copy.deepcopy(self.document)
        reordered["concepts"].reverse()
        reordered_active = next(
            item
            for item in reordered["concepts"]
            if item["id"] == "00000000-0000-4000-8000-000000000002"
        )
        reordered_active["languages"].reverse()
        for language in reordered_active["languages"]:
            language["terms"].reverse()
        second = canonical_snapshot(reordered, self.source_index, self.active_state)
        self.assertEqual(first, second)
        self.assertTrue(first.endswith(b"\n"))

    def test_only_active_concepts_publish(self):
        snapshot = json.loads(
            canonical_snapshot(
                self.document, self.source_index, self.active_state
            )
        )
        self.assertEqual(
            [
                "00000000-0000-4000-8000-000000000002",
                "00000000-0000-4000-8000-000000000003",
            ],
            [item["id"] for item in snapshot["concepts"]],
        )
        glossary = render_glossary(snapshot, self.layout, self.active_state)
        self.assertNotIn("Candidate only", glossary)

    def test_missing_chinese_never_falls_back(self):
        snapshot = json.loads(
            canonical_snapshot(
                self.document, self.source_index, self.active_state
            )
        )
        glossary = render_glossary(snapshot, self.layout, self.active_state)
        self.assertIn("| — | English only |", glossary)
        self.assertNotIn("| English only | English only |", glossary)

    def test_manual_output_drift_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            design_root = root / "design"
            (design_root / "data/vocab").mkdir(parents=True)
            shutil.copytree(ROOT / "data/references", design_root / "data/references")
            for name in ("topics", "types", "genres", "forms", "entities", "sources"):
                shutil.copy2(ROOT / f"data/vocab/{name}.yaml", design_root / f"data/vocab/{name}.yaml")
            (design_root / "data/inputs/topics").mkdir(parents=True)
            shutil.copy2(ROOT / "data/inputs/topics/label-adoptions.json",
                         design_root / "data/inputs/topics/label-adoptions.json")
            (design_root / "docs/decisions").mkdir(parents=True)
            for path in (ROOT / "docs/decisions").glob("source-*.md"):
                shutil.copy2(path, design_root / "docs/decisions" / path.name)
            (design_root / "schemas").mkdir()
            shutil.copy2(ROOT / "schemas/glossary-layout-v2.schema.json",
                         design_root / "schemas/glossary-layout-v2.schema.json")
            terms_path = design_root / "data/vocab/terms.yaml"
            source_index_path = root / "source-index.json"
            snapshot_path = root / "terms-v1.json"
            glossary_path = root / "glossary.md"
            valid = yaml.safe_load(
                (ROOT / "tests/fixtures/terminology/valid/minimal-active.yaml").read_text()
            )
            valid["concepts"][0]["subject_fields"] = []
            fixture_concept = valid["concepts"][0]
            for reference in fixture_concept["basis"]:
                reference["reference"] = "gbt-13745"
            for definition in fixture_concept["definitions"]:
                for reference in definition["basis"]:
                    reference["reference"] = "gbt-13745"
            for language in fixture_concept["languages"]:
                for term_value in language["terms"]:
                    if isinstance(term_value["basis"], list):
                        for reference in term_value["basis"]:
                            reference["reference"] = "gbt-13745"
            terms_path.write_text(
                yaml.safe_dump(valid, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )
            layout_path = root / "layout.yaml"
            layout = {
                "schema": "urn:kb-design:layout:glossary:2", "version": 2,
                "groups": [{"id": "fixture", "title": "生成测试", "order": 1,
                            "members": [valid["concepts"][0]["id"]]}],
                "source_abbreviations": {"id": "sources", "title": "出处缩写",
                                         "order": 0, "entries": []},
                "standards_appendix": {"id": "standards", "title": "引用文献",
                                       "order": 2, "entries": []},
                "reference_entries": [], "symbol_mappings": [],
                "historical_designations": [],
                "model_labels": {"generation_inputs": ["data/vocab/topics.yaml"],
                    "display_rule": "按中英形式合并并保留身份。",
                    "language_notice": "模型知识 · 第 5 级，外部用法未核实"},
            }
            layout_path.write_text(yaml.safe_dump(layout, allow_unicode=True), encoding="utf-8")
            concept_grant = {
                "id": "decision-term-0001", "schema": "urn:kb-design:data:decision",
                "schema_version": 1, "status": "accepted", "date": "2026-09-06", "level": "L3",
                "scope": "fixture", "supersedes": [], "answers": [{"question": "Q01",
                "resolution": "recommended", "patches": [{"identity": f"terms/concepts/{valid['concepts'][0]['id']}",
                "field": "record", "value": semantic_concept(valid["concepts"][0])}]}],
            }
            concept_grant["answers"][0]["patches"].append({
                "identity": "@control:terms", "field": "glossary_layout", "value": layout,
            })
            state_value = yaml.safe_load(ACTIVE_STATE.read_text())
            publication = {key: state_value[key] for key in
                           ("active_editor", "state", "terms_mode", "consumers_enabled")}
            state_grant = {"id": state_value["decision"], "schema": "urn:kb-design:data:decision",
                "schema_version": 1, "status": "accepted", "date": "2026-09-06", "level": "L3",
                "scope": "fixture", "supersedes": [], "answers": [{"question": "Q01",
                "resolution": "recommended", "patches": [{"identity": "@control:terms",
                "field": "publication", "value": publication}]}]}
            for name, decision_value in (("term-fixture-record.md", concept_grant),
                                         ("term-fixture-state.md", state_grant)):
                (design_root / "docs/decisions" / name).write_text(
                    "---\n" + yaml.safe_dump(decision_value, allow_unicode=True, sort_keys=False) + "---\n",
                    encoding="utf-8")
            source_index_path.write_text(
                json.dumps(build_reference_index(design_root), ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            arguments = [
                "--design-root", str(design_root),
                "--terms",
                str(terms_path),
                "--state",
                str(ACTIVE_STATE),
                "--layout",
                str(layout_path),
                "--source-index",
                str(source_index_path),
                "--snapshot-out",
                str(snapshot_path),
                "--glossary-out",
                str(glossary_path),
            ]
            built = subprocess.run(
                [sys.executable, "-m", "kb_core.governance.build_terms", "build", *arguments],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, built.returncode, built.stderr)
            clean = subprocess.run(
                [sys.executable, "-m", "kb_core.governance.build_terms", "check", *arguments],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, clean.returncode, clean.stderr)
            glossary_path.write_text(
                glossary_path.read_text(encoding="utf-8") + "manual drift\n",
                encoding="utf-8",
            )
            drifted = subprocess.run(
                [sys.executable, "-m", "kb_core.governance.build_terms", "check", *arguments],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, drifted.returncode)
            self.assertIn("TERM_OUTPUT_DRIFT", drifted.stderr)

    def test_invalid_input_cannot_replace_existing_outputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            invalid = yaml.safe_load(
                (ROOT / "tests/fixtures/terminology/valid/minimal-active.yaml").read_text()
            )
            invalid["concepts"][0]["id"] = "invalid-concept-id"
            invalid["concepts"][0]["subject_fields"][0]["topic_id"] = "basic-unit"
            terms_path = root / "terms.yaml"
            terms_path.write_text(yaml.safe_dump(invalid), encoding="utf-8")
            index_path = root / "index.json"
            index_path.write_text("{}", encoding="utf-8")
            snapshot_path = root / "snapshot.json"
            glossary_path = root / "glossary.md"
            snapshot_path.write_bytes(b"previous snapshot")
            glossary_path.write_bytes(b"previous glossary")

            result = subprocess.run(
                [sys.executable, "-m", "kb_core.governance.build_terms", "build",
                 "--terms", str(terms_path), "--state", str(ACTIVE_STATE),
                 "--layout", str(LAYOUT), "--source-index", str(index_path),
                 "--snapshot-out", str(snapshot_path), "--glossary-out", str(glossary_path)],
                cwd=ROOT, capture_output=True, text=True,
            )

            self.assertEqual(1, result.returncode)
            self.assertIn("TERM_SCHEMA_INVALID", result.stderr)
            self.assertEqual(b"previous snapshot", snapshot_path.read_bytes())
            self.assertEqual(b"previous glossary", glossary_path.read_bytes())

    def test_all_consumers_share_snapshot_hash(self):
        snapshot_bytes = canonical_snapshot(
            self.document, self.source_index, self.active_state
        )
        snapshot = json.loads(snapshot_bytes)
        expected = hashlib.sha256(canonical_json(snapshot)).hexdigest()
        glossary = render_glossary(snapshot, self.layout, self.active_state)
        self.assertIn("本文件只读", glossary.splitlines()[1])
        self.assertIn("data/vocab/terms.yaml", glossary.splitlines()[1])
        self.assertIn(f"快照 SHA-256：`{expected}`", glossary)

    def test_rolled_back_state_disables_generation(self):
        with self.assertRaisesRegex(ValueError, "TERM_CONSUMERS_DISABLED"):
            canonical_snapshot(
                self.document, self.source_index, self.rolled_back_state
            )


if __name__ == "__main__":
    unittest.main()
