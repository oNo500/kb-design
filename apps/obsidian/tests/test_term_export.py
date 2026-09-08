"""High-risk contracts for optional approved terminology references."""

import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml

from kb_core.governance.term_validation import semantic_concept, semantic_project_basis_scope
from kb_obsidian.exporter import ExportError, build_content_files, build_manifest, load_repository

from .test_source_v2_export import decision_bytes, documents_v2, fixture_inputs
from .design_fixture import create_clean_design


ROOT = Path(__file__).resolve().parents[3]
TERM_FIXTURE = ROOT / "tests/fixtures/terminology/valid/minimal-active.yaml"
STATE_FIXTURE = ROOT / "tests/fixtures/terminology/states/active.yaml"


def _decision(decision_id, patches):
    return {
        "id": decision_id,
        "schema": "urn:kb-design:data:decision",
        "schema_version": 1,
        "status": "accepted",
        "date": "2026-09-06",
        "level": "L3",
        "scope": "synthetic Obsidian terminology test",
        "supersedes": [],
        "answers": [{"question": "Q01", "resolution": "recommended", "patches": patches}],
    }


def term_inputs(*, precise=True, bilingual=False, reverse_languages=False, project_basis=False):
    documents = documents_v2()
    inputs = fixture_inputs(documents)
    terms = yaml.safe_load(TERM_FIXTURE.read_text(encoding="utf-8"))
    state = yaml.safe_load(STATE_FIXTURE.read_text(encoding="utf-8"))
    concept = terms["concepts"][0]
    concept["subject_fields"] = []
    if project_basis:
        concept["basis"] = {"project": {
            "approval": "decision-term-0001",
            "origin": {
                "commit": "1" * 40,
                "file": "docs/design/model/fixture.md",
                "locator": "项目定义",
            },
            "rationale": "该定义属于已采纳的项目合同。",
        }}
    for definition in concept["definitions"]:
        for basis in definition["basis"]:
            basis["reference"] = "standard"
    if isinstance(concept["basis"], list):
        for basis in concept["basis"]:
            basis["reference"] = "standard"
    for language in concept["languages"]:
        for term in language["terms"]:
            for basis in term["basis"]:
                basis["reference"] = "standard"
    if bilingual:
        concept["definitions"].append({
            "language": "zh-Hans",
            "text": "合成概念。",
            "basis": [{"reference": "standard", "locator": "definition", "checked": "2026-08-31"}],
        })
        concept["languages"].append({
            "language": "zh-Hans",
            "terms": [{
                "id": "tm-33333333-3333-4333-8333-333333333333",
                "text": "阿尔法",
                "administrative_status": "preferredTerm-admn-sts",
                "basis": [{"reference": "standard", "locator": "preferred term", "checked": "2026-08-31"}],
                "history": [{
                    "date": "2026-08-31",
                    "event": "registered",
                    "decision": "decision-term-0001",
                    "reason": "Fixture registration.",
                    "from_value": None,
                    "to_value": "preferredTerm-admn-sts",
                    "linked_terms": ["tm-33333333-3333-4333-8333-333333333333"],
                }],
            }, {
                "id": "tm-44444444-4444-4444-8444-444444444444",
                "text": "旧阿尔法",
                "administrative_status": "deprecatedTerm-admn-sts",
                "basis": [{"reference": "standard", "locator": "deprecated term", "checked": "2026-08-31"}],
                "history": [{
                    "date": "2026-08-31",
                    "event": "registered",
                    "decision": "decision-term-0001",
                    "reason": "Fixture registration.",
                    "from_value": None,
                    "to_value": "deprecatedTerm-admn-sts",
                    "linked_terms": ["tm-44444444-4444-4444-8444-444444444444"],
                }],
            }],
        })
        if reverse_languages:
            concept["languages"].reverse()
    concept_grant = semantic_concept(concept)
    if not precise:
        concept_grant = copy.deepcopy(concept_grant)
        concept_grant["definitions"][0]["text"] = "Wrong grant value."
    adoption_patches = [{
        "identity": f"terms/concepts/{concept['id']}",
        "field": "record",
        "value": concept_grant,
    }]
    if project_basis:
        adoption_patches.append({
            "identity": f"terms/concepts/{concept['id']}",
            "field": "project_basis_scope",
            "value": semantic_project_basis_scope(concept),
        })
    adoption = _decision("decision-term-0001", adoption_patches)
    state_grant = _decision("decision-term-fixture-active", [{
        "identity": "@control:terms",
        "field": "publication",
        "value": {key: state[key] for key in (
            "active_editor", "state", "terms_mode", "consumers_enabled"
        )},
    }])
    inputs.update({
        "terms": yaml.safe_dump(terms).encode(),
        "term_state": yaml.safe_dump(state).encode(),
        "_support:docs/decisions/term-fixture-adoption.md": decision_bytes(adoption),
        "_support:docs/decisions/term-fixture-activation.md": decision_bytes(state_grant),
    })
    concept_id = concept["id"]
    layout = {
        "schema": "urn:kb-design:layout:glossary:2",
        "version": 2,
        "groups": [{
            "id": "fixture", "title": "合成分组", "order": 1,
            "members": [concept_id],
        }],
        "source_abbreviations": {
            "id": "source-abbreviations", "title": "出处缩写", "order": 0,
            "entries": [],
        },
        "standards_appendix": {
            "id": "cited-standards", "title": "引用的标准与文献", "order": 2,
            "entries": [],
        },
        "reference_entries": [],
        "symbol_mappings": [{
            "origin_id": "fixture-symbol", "symbols": ["FX"],
            "concept_ids": [concept_id], "role": "relationship_indicator",
            "display_note": "仅作关系指示符，不是当前术语形式。",
        }],
        "historical_designations": [{
            "origin_id": "fixture-history", "forms": ["旧称列表"],
            "target_concept_ids": [concept_id], "disposition": "withdrawn",
            "reason": "名称已退出。", "display": "旧称列表仅供检索纠正。",
            "effect": "不作为当前准用名称。", "approval": "decision-term-0001",
        }],
        "model_labels": {
            "generation_inputs": ["data/vocab/topics.yaml"],
            "display_rule": "只展示既有对象标签。",
            "language_notice": "模型知识，第 5 级，外部用法未核实。",
        },
    }
    inputs["term_layout"] = yaml.safe_dump(layout).encode()
    layout_grant = _decision("decision-term-fixture-layout", [{
        "identity": "@control:terms",
        "field": "glossary_layout",
        "value": layout,
    }])
    inputs["_support:docs/decisions/term-fixture-layout.md"] = decision_bytes(layout_grant)
    for relative in (
        "schemas/terms-v1.schema.json",
        "schemas/term-cutover-state-v1.schema.json",
        "schemas/glossary-layout-v2.schema.json",
    ):
        inputs["_support:" + relative] = (ROOT / relative).read_bytes()
    return inputs


def superseded_term_inputs(*, current_grant=True):
    inputs = term_inputs()
    terms = yaml.safe_load(inputs["terms"])
    concept = terms["concepts"][0]
    concept["definitions"][0]["text"] = "Precisely granted rewrite."
    concept["history"].append({
        "date": "2026-09-06",
        "event": "definition-updated",
        "decision": "decision-term-0002",
        "reason": "precise semantic update",
        "from_value": "sha256:before",
        "to_value": "sha256:after",
        "linked_terms": [],
    })
    grant_value = semantic_concept(concept)
    if not current_grant:
        grant_value = copy.deepcopy(grant_value)
        grant_value["definitions"][0]["text"] = "Different value."
    decision = _decision("decision-term-0002", [{
        "identity": f"terms/concepts/{concept['id']}",
        "field": "record",
        "value": grant_value,
    }])
    decision["supersedes"] = ["decision-term-0001"]
    inputs["terms"] = yaml.safe_dump(terms).encode()
    inputs["_support:docs/decisions/term-fixture-update.md"] = decision_bytes(decision)
    return inputs


def commit_inputs(root, inputs, message):
    for path in (root / "docs/decisions").glob("term-*.md"):
        path.unlink()
    for name, relative in {
        "topics": "data/vocab/topics.yaml",
        "entities": "data/vocab/entities.yaml",
        "bibliography": "data/references/bibliography.yaml",
        "sources": "data/vocab/sources.yaml",
        "types": "data/vocab/types.yaml",
        "genres": "data/vocab/genres.yaml",
        "forms": "data/vocab/forms.yaml",
        "terms": "data/vocab/terms.yaml",
        "term_state": "data/vocab/term-cutover-state.yaml",
        "term_layout": "data/inputs/terminology/glossary-layout.yaml",
    }.items():
        (root / relative).write_bytes(inputs[name])
    for key, content in inputs.items():
        if key.startswith("_support:docs/decisions/"):
            (root / key.removeprefix("_support:")).write_bytes(content)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "--quiet", "-m", message], check=True)


def commit_term_fixture(root):
    commit_inputs(root, term_inputs(), "term fixture")


class TermExportTests(unittest.TestCase):
    def test_one_optional_term_input_without_the_other_is_rejected(self):
        inputs = fixture_inputs(documents_v2())
        inputs["terms"] = TERM_FIXTURE.read_bytes()

        with self.assertRaisesRegex(ExportError, "terms.yaml.*term-cutover-state.yaml"):
            load_repository(Path("/synthetic"), input_bytes=inputs)

    def test_active_terms_require_exact_concept_and_publication_grants(self):
        with self.assertRaisesRegex(ExportError, "TERM_ADOPTION_MISSING"):
            load_repository(Path("/synthetic"), input_bytes=term_inputs(precise=False))

    def test_active_terms_require_the_captured_v2_layout(self):
        inputs = term_inputs()
        del inputs["term_layout"]

        with self.assertRaisesRegex(ExportError, "glossary-layout.yaml"):
            load_repository(Path("/synthetic"), input_bytes=inputs)

    def test_superseded_grant_remains_history_but_not_current_authority(self):
        documents = load_repository(
            Path("/synthetic"), input_bytes=superseded_term_inputs()
        )
        self.assertEqual(
            "Precisely granted rewrite.",
            documents["terms"]["concepts"][0]["definitions"][0]["text"],
        )

        with self.assertRaisesRegex(ExportError, "TERM_ADOPTION_MISSING"):
            load_repository(
                Path("/synthetic"),
                input_bytes=superseded_term_inputs(current_grant=False),
            )

    def test_same_snapshot_active_terms_export_one_concept_page(self):
        inputs = term_inputs()
        files = build_content_files(Path("/synthetic"), input_bytes=inputs)
        concept_id = "tc-11111111-1111-4111-8111-111111111111"
        path = f"kb/terms/{concept_id}.md"

        self.assertIn(path, files)
        text = files[path].decode()
        self.assertIn(f'kb_id: "{concept_id}"', text)
        self.assertIn('kb_object: "term"', text)
        self.assertIn("# Alpha", text)
        self.assertIn("tm-11111111-1111-4111-8111-111111111111", text)
        self.assertIn("tm-22222222-2222-4222-8222-222222222222", text)
        self.assertIn("Standard · 1", text)
        self.assertIn("旧称列表仅供检索纠正", text)
        self.assertIn("不作为当前准用名称", text)
        self.assertIn("[[kb/topics/topic|Topic]]", files["kb/references/standard.md"].decode())

        manifest = json.loads(build_manifest(Path("/synthetic"), files, input_bytes=inputs))
        self.assertEqual(1, manifest["object_counts"]["term"])
        term_input = next(row for row in manifest["inputs"] if row["path"] == "data/vocab/terms.yaml")
        self.assertEqual("1", term_input["version"])
        layout_input = next(
            row for row in manifest["inputs"]
            if row["path"] == "data/inputs/terminology/glossary-layout.yaml"
        )
        self.assertEqual("2", layout_input["version"])

    def test_project_basis_is_rendered_as_project_evidence(self):
        files = build_content_files(
            Path("/synthetic"), input_bytes=term_inputs(project_basis=True)
        )
        text = files[
            "kb/terms/tc-11111111-1111-4111-8111-111111111111.md"
        ].decode()

        self.assertIn("项目决定依据，不是外部来源", text)
        self.assertIn("采纳决定：decision-term-0001", text)
        self.assertIn("docs/design/model/fixture.md", text)

    def test_bilingual_page_identity_is_stable_when_input_language_order_changes(self):
        forward = build_content_files(
            Path("/synthetic"), input_bytes=term_inputs(bilingual=True)
        )
        reversed_files = build_content_files(
            Path("/synthetic"),
            input_bytes=term_inputs(bilingual=True, reverse_languages=True),
        )
        path = "kb/terms/tc-11111111-1111-4111-8111-111111111111.md"
        forward_properties = yaml.safe_load(forward[path].decode().split("---\n", 2)[1])
        reversed_properties = yaml.safe_load(reversed_files[path].decode().split("---\n", 2)[1])

        self.assertEqual("阿尔法", forward_properties["kb_label"])
        self.assertEqual(["Alpha", "Beta", "旧阿尔法"], forward_properties["aliases"])
        self.assertEqual(forward_properties, reversed_properties)
        self.assertEqual(1, forward_properties["kb_schema_version"])
        self.assertNotIn("kb_version", forward_properties)

    def test_clean_git_snapshot_captures_and_exports_active_terms(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, _ = create_clean_design(Path(temporary) / "design")
            commit_term_fixture(root)

            from kb_obsidian.design_source import load_design
            from kb_obsidian.reference_export import export_reference
            snapshot = load_design(root.resolve())
            output = Path(temporary) / "reference"
            manifest = export_reference(snapshot, output)

            self.assertIn("data/vocab/terms.yaml", snapshot.input_hashes)
            self.assertEqual(1, manifest["object_counts"]["term"])
            self.assertTrue((output / "kb/terms/tc-11111111-1111-4111-8111-111111111111.md").is_file())

    def test_committed_term_inputs_cannot_be_hidden_by_skip_worktree_deletion(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, _ = create_clean_design(Path(temporary) / "design")
            commit_term_fixture(root)
            relative_paths = (
                "data/vocab/terms.yaml",
                "data/vocab/term-cutover-state.yaml",
            )
            subprocess.run(
                ["git", "-C", str(root), "update-index", "--skip-worktree", *relative_paths],
                check=True,
            )
            for relative in relative_paths:
                (root / relative).unlink()
            self.assertEqual(
                "",
                subprocess.run(
                    ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout,
            )

            from kb_obsidian.design_source import load_design
            from kb_obsidian.errors import ApplicationError
            with self.assertRaisesRegex(ApplicationError, "term input file set differs from commit"):
                load_design(root.resolve())

    def test_docs_only_commit_cannot_hide_a_term_history_rewrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, _ = create_clean_design(Path(temporary) / "design")
            commit_inputs(root, term_inputs(), "A initial term")
            commit_inputs(root, superseded_term_inputs(), "B granted definition update")

            from kb_obsidian.design_source import load_design
            self.assertEqual(
                "Precisely granted rewrite.",
                load_design(root.resolve()).documents["terms"]["concepts"][0]["definitions"][0]["text"],
            )

            current = yaml.safe_load((root / "data/vocab/terms.yaml").read_text())
            current["concepts"][0]["history"] = [{
                "date": "2026-09-06",
                "event": "registered",
                "decision": "decision-term-0002",
                "reason": "rewritten initial history",
                "from_value": None,
                "to_value": "active",
                "linked_terms": [],
            }]
            (root / "data/vocab/terms.yaml").write_text(yaml.safe_dump(current))
            subprocess.run(["git", "-C", str(root), "add", "data/vocab/terms.yaml"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "--quiet", "-m", "C rewrite history"], check=True)
            (root / "docs/decisions/term-docs-only.md").write_text("# 历史保护\n")
            subprocess.run(["git", "-C", str(root), "add", "docs/decisions/term-docs-only.md"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "--quiet", "-m", "D docs only"], check=True)

            from kb_obsidian.errors import ApplicationError
            with self.assertRaisesRegex(ExportError, "TERM_HISTORY_NOT_APPEND_ONLY"):
                load_repository(root)
            with self.assertRaisesRegex(ApplicationError, "TERM_HISTORY_NOT_APPEND_ONLY"):
                load_design(root.resolve())

    def test_manifest_rejects_a_term_form_id_as_a_page_identity(self):
        files = build_content_files(Path("/synthetic"), input_bytes=term_inputs())
        content = files.pop("kb/terms/tc-11111111-1111-4111-8111-111111111111.md")
        files["kb/terms/tm-11111111-1111-4111-8111-111111111111.md"] = content

        with self.assertRaisesRegex(ExportError, "invalid output ID"):
            build_manifest(Path("/synthetic"), files, input_bytes=term_inputs())

    def test_unknown_term_wikilink_is_rejected(self):
        files = build_content_files(Path("/synthetic"), input_bytes=term_inputs())
        files["index.md"] += b"\n[[kb/terms/tc-99999999-9999-4999-8999-999999999999]]\n"

        # The written-export validator is exercised by write_export; this small
        # assertion keeps the failure at the application boundary.
        from kb_obsidian.exporter import _validate_written_export
        import tempfile
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            for relative, content in files.items():
                target = output / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            manifest = build_manifest(Path("/synthetic"), files, input_bytes=term_inputs())
            (output / "manifest.json").write_bytes(manifest)
            with self.assertRaisesRegex(ExportError, "unresolved written link"):
                _validate_written_export(output, files, manifest)


if __name__ == "__main__":
    unittest.main()
