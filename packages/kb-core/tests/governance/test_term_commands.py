import copy
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

from kb_core.governance.term_validation import semantic_concept


ROOT = pathlib.Path(__file__).resolve().parents[4]


class TermCommandTests(unittest.TestCase):
    def test_validated_index_tracks_actual_terms_but_rejects_unapproved_changes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            (root / "data/vocab").mkdir(parents=True)
            for name in ("topics", "types", "genres", "forms", "entities", "sources"):
                path = ROOT / "data/vocab" / f"{name}.yaml"
                shutil.copy2(path, root / "data/vocab" / path.name)
            # Source and label grants belong to the copied vocabulary context;
            # real term record grants would require their entire approved batch.
            (root / "docs/decisions").mkdir(parents=True)
            for path in (ROOT / "docs/decisions").glob("source-*.md"):
                shutil.copy2(path, root / "docs/decisions" / path.name)
            shutil.copytree(ROOT / "data/inputs/topics", root / "data/inputs/topics")
            document = yaml.safe_load((ROOT / "tests/fixtures/terminology/valid/minimal-active.yaml").read_text())
            concept = document["concepts"][0]
            concept["subject_fields"] = []
            # Keep this CLI fixture within the ordinary de-jure definition path;
            # it does not exercise the separately constrained source exceptions.
            concept["definitions"][0]["basis"][0]["entity"] = "gbt-13745"
            decision_id = "decision-term-command-fixture"
            for item in [concept, *concept["languages"][0]["terms"]]:
                item["history"][0]["decision"] = decision_id
            decision = {
                "id": decision_id, "schema": "urn:kb-design:data:decision", "schema_version": 1,
                "status": "accepted", "date": "2026-09-06", "level": "L3",
                "scope": "Isolated CLI fixture", "supersedes": [],
                "answers": [{"question": "Q01", "resolution": "recommended", "patches": [
                    {"identity": f"terms/concepts/{concept['id']}", "field": "record",
                     "value": semantic_concept(concept)},
                ]}],
            }
            (root / "docs/decisions/term-command-fixture.md").write_text(
                "---\n" + yaml.safe_dump(decision) + "---\n# 夹具决定\n"
            )
            term_path = root / "data/vocab/terms.yaml"
            term_path.write_text(yaml.safe_dump(document))
            output = root / "build/index.json"
            args = [sys.executable, "-m", "kb_core.governance.term_commands",
                    "index", "--root", str(root), "--output", str(output)]
            good = subprocess.run(args, text=True, capture_output=True)
            self.assertEqual(0, good.returncode, good.stderr)
            before = output.read_bytes()
            self.assertIn(concept["id"], before.decode())
            self.assertIn(decision_id, before.decode())

            state = yaml.safe_load((ROOT / "tests/fixtures/terminology/states/active.yaml").read_text())
            state["decision"] = decision_id
            state["history"][0]["decision"] = decision_id
            decision["answers"][0]["patches"].append({
                "identity": "@control:terms", "field": "publication",
                "value": {key: state[key] for key in
                          ("active_editor", "state", "terms_mode", "consumers_enabled")},
            })
            (root / "docs/decisions/term-command-fixture.md").write_text(
                "---\n" + yaml.safe_dump(decision) + "---\n# 夹具决定\n"
            )
            state_path = root / "data/vocab/term-cutover-state.yaml"
            state_path.write_text(yaml.safe_dump(state))
            (root / "docs/glossary.md").write_text(
                "| 术语 | 英文 | 定义 | 出处 |\n|---|---|---|---|\n"
                "| 旧显示 | Legacy only | 旧生成视图 | fixture |\n"
            )
            read_args = [sys.executable, "-c",
                         "import json; from kb_core.check_terms import glossary_forms; "
                         "print(json.dumps(sorted(glossary_forms())))"]
            env = {**os.environ, "KB_DESIGN_ROOT": str(root)}
            incomplete = subprocess.run(read_args, text=True, capture_output=True, env=env)
            self.assertNotEqual(0, incomplete.returncode)
            self.assertIn("glossary-layout.yaml", incomplete.stderr)
            vocabulary_form = next(row for row in yaml.safe_load(
                (root / "data/vocab/entities.yaml").read_text())["entities"]
                if row["id"] == "gbt-13745")["label"]["en"]
            layout = {
                "schema": "urn:kb-design:layout:glossary:2", "version": 2,
                "groups": [{"id": "fixture", "title": "Fixture", "order": 1, "members": [concept["id"]]}],
                "source_abbreviations": {"id": "sources", "title": "Sources", "order": 0, "entries": []},
                "standards_appendix": {"id": "standards", "title": "Standards", "order": 2, "entries": []},
                "reference_entries": [], "symbol_mappings": [],
                "historical_designations": [{"origin_id": "fixture-old", "forms": ["Legacy only", vocabulary_form],
                    "target_concept_ids": [concept["id"]], "disposition": "withdrawn", "reason": "Fixture",
                    "display": "Legacy only", "effect": "historical lookup", "approval": decision_id}],
                "model_labels": {"generation_inputs": ["topics"], "display_rule": "Fixture", "language_notice": "Fixture"},
            }
            layout_path = root / "data/inputs/terminology/glossary-layout.yaml"
            layout_path.parent.mkdir(parents=True)
            layout_path.write_text(yaml.safe_dump(layout))
            unapproved = subprocess.run(read_args, text=True, capture_output=True, env=env)
            self.assertNotEqual(0, unapproved.returncode)
            self.assertIn("TERM_LAYOUT_ADOPTION_MISSING", unapproved.stderr)
            decision["answers"][0]["patches"].append({
                "identity": "@control:terms", "field": "glossary_layout", "value": layout,
            })
            (root / "docs/decisions/term-command-fixture.md").write_text(
                "---\n" + yaml.safe_dump(decision) + "---\n# 夹具决定\n"
            )
            read = subprocess.run(read_args, text=True, capture_output=True, env=env)
            self.assertEqual(0, read.returncode, read.stderr)
            forms = json.loads(read.stdout)
            self.assertIn("alpha", forms)
            self.assertIn("beta", forms)
            self.assertNotIn("legacy only", forms)
            self.assertIn(vocabulary_form.lower(), forms)
            state["decision"] = "decision-term-infrastructure-scope"
            state_path.write_text(yaml.safe_dump(state))
            forged = subprocess.run(read_args, text=True, capture_output=True, env=env)
            self.assertNotEqual(0, forged.returncode)
            self.assertIn("TERM_STATE_DECISION_MISSING", forged.stderr)
            state["decision"] = decision_id
            state_path.write_text(yaml.safe_dump(state))

            for command in (
                ["git", "init"],
                ["git", "config", "user.email", "fixture@example.test"],
                ["git", "config", "user.name", "Fixture"],
                ["git", "add", "data/vocab/terms.yaml"],
                ["git", "commit", "-m", "terms fixture"],
            ):
                completed = subprocess.run(command, cwd=root, text=True, capture_output=True)
                self.assertEqual(0, completed.returncode, completed.stderr)

            changed = copy.deepcopy(document)
            changed["concepts"][0]["definitions"][0]["text"] = "Unapproved different meaning."
            term_path.write_text(yaml.safe_dump(changed))
            bad = subprocess.run(args, text=True, capture_output=True)

            self.assertEqual(1, bad.returncode)
            self.assertIn("TERM_ADOPTION", bad.stderr)
            self.assertEqual(before, output.read_bytes())

            moved = copy.deepcopy(document)
            moved_concept = moved["concepts"][0]
            moved_concept["languages"][0]["language"] = "zh-Hans"
            moved_concept["definitions"][0]["language"] = "zh-Hans"
            moved_concept["history"].append({
                "date": "2026-09-06", "event": "changed", "decision": decision_id,
                "reason": "Fixture current grant.", "from_value": "en",
                "to_value": "zh-Hans", "linked_terms": [],
            })
            decision["answers"][0]["patches"][0]["value"] = semantic_concept(moved_concept)
            (root / "docs/decisions/term-command-fixture.md").write_text(
                "---\n" + yaml.safe_dump(decision) + "---\n# 夹具决定\n"
            )
            term_path.write_text(yaml.safe_dump(moved))
            history_checked = subprocess.run(args, text=True, capture_output=True)
            self.assertEqual(1, history_checked.returncode)
            self.assertIn("TERM_IDENTITY_CHANGED", history_checked.stderr)
            self.assertEqual(before, output.read_bytes())


if __name__ == "__main__":
    unittest.main()
