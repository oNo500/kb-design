import copy
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

import yaml

from scripts.governance.build_terms import (
    canonical_json,
    canonical_snapshot,
    load_cutover_state,
    render_glossary,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
ACTIVE_STATE = ROOT / "tests/fixtures/terminology/states/active.yaml"
ROLLED_BACK_STATE = ROOT / "tests/fixtures/terminology/states/rolled-back.yaml"
LAYOUT = ROOT / "vocab/glossary-layout.yaml"
BUILD_TERMS = ROOT / "scripts/governance/build_terms.py"


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
            terms_path = root / "terms.yaml"
            source_index_path = root / "source-index.json"
            snapshot_path = root / "terms-v1.json"
            glossary_path = root / "glossary.md"
            terms_path.write_text(
                yaml.safe_dump(self.document, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )
            source_index_path.write_text(
                json.dumps(self.source_index, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            arguments = [
                "--terms",
                str(terms_path),
                "--state",
                str(ACTIVE_STATE),
                "--layout",
                str(LAYOUT),
                "--source-index",
                str(source_index_path),
                "--snapshot-out",
                str(snapshot_path),
                "--glossary-out",
                str(glossary_path),
            ]
            built = subprocess.run(
                [sys.executable, str(BUILD_TERMS), "build", *arguments],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, built.returncode, built.stderr)
            clean = subprocess.run(
                [sys.executable, str(BUILD_TERMS), "check", *arguments],
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
                [sys.executable, str(BUILD_TERMS), "check", *arguments],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, drifted.returncode)
            self.assertIn("TERM_OUTPUT_DRIFT", drifted.stderr)

    def test_all_consumers_share_snapshot_hash(self):
        snapshot_bytes = canonical_snapshot(
            self.document, self.source_index, self.active_state
        )
        snapshot = json.loads(snapshot_bytes)
        expected = hashlib.sha256(canonical_json(snapshot)).hexdigest()
        glossary = render_glossary(snapshot, self.layout, self.active_state)
        self.assertEqual(
            "本文件由术语记录确定生成，只读；如需修改，请编辑 `vocab/terms.yaml`。",
            glossary.splitlines()[1],
        )
        self.assertIn(f"快照 SHA-256：`{expected}`", glossary)

    def test_rolled_back_state_disables_generation(self):
        with self.assertRaisesRegex(ValueError, "TERM_CONSUMERS_DISABLED"):
            canonical_snapshot(
                self.document, self.source_index, self.rolled_back_state
            )


if __name__ == "__main__":
    unittest.main()
