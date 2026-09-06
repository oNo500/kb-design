"""Source evidence must remain distinct from project assertions in the export."""
import copy
import json
from unittest.mock import patch
import datetime as dt
import unittest
import tempfile
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

from kb_obsidian.exporter import ExportError, build_content_files, load_repository, write_export, _read_repository_inputs


def documents_v2():
    day = dt.date(2026, 9, 5)
    version = {"id": "fixture", "date": day, "note": "synthetic"}
    evidence = {"entity": "standard", "locator": "https://example.invalid/status", "checked": day}
    assertion = {"disposition": "project_assertion", "original": "self", "migration": "audit/fixture#source"}
    source = {"registry": "registry", "item": "item-one", "locator": "https://example.invalid/item", "basis": [evidence]}
    topic = {"id": "topic", "label": {"en": "Topic"}, "basis": {"zh": {"legacy": "none"}, "en": {"level": 1, "references": [{"source": "registry", "locator": "https://example.invalid/item"}]}},
             "broader": [], "status": "candidate", "added": day, "source": source,
             "match": [{"registry": "registry", "item": "external-one", "rel": "closeMatch", "basis": [evidence]}]}
    entity = {"id": "standard", "label": {"en": "Standard"}, "kind": "standard", "subjects": ["topic"],
              "status": "active", "source_status": "current", "added": day, "version": "1", "tier": "de-jure",
              "urls": [{"role": "canonical", "url": "https://example.invalid/", "primary": True},
                       {"role": "mirror", "url": "https://mirror.invalid/", "primary": False}],
              "basis": {"version": [evidence], "source_status": [evidence], "subjects": [{"values": ["topic"], "references": [evidence]}]},
              "review": {"checked": day, "next_due": dt.date(2028, 9, 5), "interval_months": 24, "grace_days": 30, "obligations": []},
              "watch": [{"locator": "https://example.invalid/changes", "signals": ["availability", "revision"],
                         "cadence_months": {"availability": 1, "redirect": 1, "content": 1}}],
              "replaced_by": None,
              "history": [{"date": day, "action": "migration", "fields": ["checked", "version", "source_status"], "decisions": ["source-fixture-decision"], "before": {"checked": "2001-01-01"}}]}
    general = {"id": "organization", "label": {"en": "Organization"}, "kind": "organization", "subjects": ["topic"],
               "status": "candidate", "added": day, "assertions": {"subjects": [{**assertion, "values": ["topic"]}]}}
    roles = [{"role": role, "status": "approved", "decision": "source-fixture-decision"} for role in ("mapping", "structure")]
    result = {"topics": {"version": version, "concepts": [topic], "arrays": []},
              "entities": {"schema": "urn:kb-design:data:entities", "schema_version": 2, "version": version, "entities": [entity, general]},
              "sources": {"schema": "urn:kb-design:data:source-uses", "schema_version": 2, "version": version,
                          "sources": [{"id": "registry", "entity": "standard", "roles": roles, "history": [{"date": day, "action": "migration", "fields": ["roles"], "decisions": []}]}]}}
    for name in ("types", "genres", "forms"):
        result[name] = {"version": version, name: []}
    result["forms"]["arrays"] = [{"id": "local", "superordinate": "forms", "assertions": {"source": assertion}}]
    result["forms"]["arrays"].append({"id": "isolated-form", "superordinate": "forms",
        "local_analysis": {"legacy_source_label": "lom", "state": "isolated", "decision": "decision-source-0011"}})
    for document in result.values():
        document["schema_version"] = 2
    return result


def decision_v2():
    patches = [{"identity": "sources/registry", "field": "entity", "value": "standard"}]
    patches += [{"identity": "sources/registry/roles/" + role, "field": "status", "value": "approved"}
                for role in ("mapping", "structure")]
    patches += [{"identity": "entities/standard", "field": field, "value": value}
                for field, value in (("version", "1"), ("source_status", "current"))]
    return {"id": "source-fixture-decision", "schema": "urn:kb-design:data:decision", "schema_version": 1,
            "status": "accepted", "date": "2026-09-05", "level": "L3", "scope": "synthetic application test",
            "supersedes": [], "answers": [{"question": "Q01", "resolution": "recommended", "patches": patches}]}


def decision_bytes(decision):
    return ("---\n" + yaml.safe_dump(decision) + "---\n# 合成采纳\n").encode()


def migration_policy_bytes():
    return (Path(__file__).resolve().parents[3] / "docs/decisions/source-migration-policy.md").read_bytes()


def fixture_inputs(documents):
    return {**{name: yaml.safe_dump(doc).encode() for name, doc in documents.items()},
            "_support:docs/decisions/source-fixture-decision.md": decision_bytes(decision_v2()),
            "_support:docs/decisions/source-migration-policy.md": migration_policy_bytes()}


def load(documents):
    return load_repository(Path("/synthetic"), input_bytes=fixture_inputs(documents))


class SourceV2ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "design"
        (self.root / "data/vocab").mkdir(parents=True)
        (self.root / "docs/decisions").mkdir(parents=True)
        self.documents = documents_v2()
        self.decision = decision_v2()
        self.save()

    def save(self):
        for name, document in self.documents.items():
            (self.root / "data/vocab" / (name + ".yaml")).write_text(yaml.safe_dump(document))
        (self.root / "docs/decisions/source-fixture-decision.md").write_bytes(decision_bytes(self.decision))
        (self.root / "docs/decisions/source-migration-policy.md").write_bytes(migration_policy_bytes())

    def test_role_decision_scope_cannot_be_borrowed(self):
        self.decision["answers"][0]["patches"][0]["value"] = "another-entity"
        self.save()
        with self.assertRaisesRegex(ExportError, "SOURCE_ROLE_(DECISION_MISSING|NOT_APPROVED)"):
            load_repository(self.root)

    def test_captured_support_bytes_do_not_reread_changed_files(self):
        captured = _read_repository_inputs(self.root)
        self.decision["answers"][0]["patches"] = []
        self.save()
        self.assertTrue(load_repository(self.root, input_bytes=captured))
        with self.assertRaises(ExportError):
            load_repository(self.root)

    def test_scope_correction_uses_captured_exact_authority(self):
        topic = self.documents["topics"]["concepts"][0]
        topic["label"]["zh"] = "主题"
        topic["scope"] = "Corrected scope"
        approval = "design/decisions/structured-label-basis.md#批次授权"
        topic["basis"]["zh"] = {"level": 5, "model": {
            "name": "GPT-6", "date": "2026-09-05", "rationale": "按既有概念的模型知识译名", "approval": approval}}
        adoption = {"authorization": approval, "records": {"topics/topic/zh": {
            "accept": True, "label": "主题", "basis": copy.deepcopy(topic["basis"]["zh"]),
            "original": {"en": "Topic", "scope": "Original scope"}}}}
        patches = self.decision["answers"][0]["patches"]
        patches.extend([
            {"identity": "topics/concepts/topic", "field": "scope", "value": "Corrected scope"},
            {"identity": "topics/concepts/topic", "field": "scope.correction",
             "value": {"before": "Original scope", "after": "Corrected scope"}},
        ])
        self.save()
        path = self.root / "data/inputs/topics/label-adoptions.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(adoption))
        captured = _read_repository_inputs(self.root)
        patches[-1]["value"]["before"] = "Forged original scope"
        self.save()
        with patch.object(Path, "read_bytes", side_effect=AssertionError("semantic reread")), \
             patch.object(Path, "read_text", side_effect=AssertionError("semantic reread")):
            files = build_content_files(self.root, input_bytes=captured)
        self.assertIn("Corrected scope", files["kb/topics/topic.md"].decode())
        with self.assertRaisesRegex(ExportError, "scope"):
            load_repository(self.root)

    def test_unverified_source_status_and_version_are_not_fabricated(self):
        entity = self.documents["entities"]["entities"][0]
        del entity["source_status"]
        del entity["basis"]["source_status"]
        entity["version"] = None
        del entity["basis"]["version"]
        self.save()
        output = Path(self.temp.name) / "unverified-export"
        write_export(self.root, output)
        text = (output / "kb/entities/standard.md").read_text()
        properties = yaml.safe_load(text.split("---")[1])
        self.assertNotIn("kb_source_status", properties)
        self.assertNotIn("kb_entity_version", properties)
        self.assertEqual("active", properties["kb_status"])
        self.assertIn("外部状态未核实", text)
        self.assertIn("未登记可核实版本", text)
        general = (output / "kb/entities/organization.md").read_text()
        self.assertNotIn("外部状态未核实", general)
        self.assertNotIn("未登记可核实版本", general)

    def test_clean_design_export_tracks_support_file_bytes(self):
        from kb_obsidian.design_source import _IMPLEMENTATION_FILES, load_design
        from kb_obsidian.reference_export import export_reference
        from kb_obsidian.errors import ApplicationError
        repository = Path(__file__).resolve().parents[3]
        for relative in _IMPLEMENTATION_FILES:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(repository / relative, target)
        for args in (("init", "--quiet"), ("config", "user.name", "Fixture"),
                     ("config", "user.email", "fixture@example.invalid"), ("add", "."),
                     ("commit", "--quiet", "-m", "synthetic source v2 fixture")):
            subprocess.run(["git", "-C", str(self.root), *args], check=True)
        snapshot = load_design(self.root)
        result = export_reference(snapshot, Path(self.temp.name) / "reference")
        self.assertEqual(snapshot.commit, result["design_commit"])
        decision_path = "docs/decisions/source-fixture-decision.md"
        subprocess.run(["git", "-C", str(self.root), "update-index", "--skip-worktree", decision_path], check=True)
        self.decision["answers"][0]["patches"] = []
        self.save()
        with self.assertRaisesRegex(ApplicationError, "differs from commit"):
            load_design(self.root)

    def test_cli_rejects_wrong_field_approval_review_and_watch(self):
        from kb_obsidian import exporter
        def run(output):
            return subprocess.run([sys.executable, str(Path(exporter.__file__)), "--repo-root", str(self.root),
                                   "--output", str(output)], capture_output=True, text=True)
        output = Path(self.temp.name) / "valid-export"
        result = run(output)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((output / "manifest.json").is_file())
        for field, value, error_path in (
            ("source_status", "withdrawn", "source_status"),
            ("review", {**self.documents["entities"]["entities"][0]["review"], "next_due": None}, "review.next_due"),
            ("watch", [{"locator": "https://example.invalid/changes", "signals": ["revision"],
                        "cadence_months": {"availability": 1, "redirect": 1, "content": 6}}], "watch")):
            with self.subTest(field=field):
                self.documents = documents_v2()
                self.documents["entities"]["entities"][0][field] = value
                self.save()
                output = Path(self.temp.name) / ("invalid-" + field)
                result = run(output)
                self.assertNotEqual(0, result.returncode)
                self.assertIn(error_path, result.stderr)
                self.assertFalse(output.exists())

    def test_evidence_assertions_roles_and_history_survive_rendering(self):
        files = build_content_files(Path("/synthetic"), input_bytes=fixture_inputs(documents_v2()))
        entity = files["kb/entities/standard.md"].decode()
        self.assertEqual(yaml.safe_load(entity.split("---")[1])["kb_status"], "active")
        self.assertEqual(yaml.safe_load(entity.split("---")[1])["kb_source_status"], "current")
        for text in ("https://mirror.invalid/", "2001-01-01", "revision", "24", "kb/entities/standard", "kb/topics/topic"):
            self.assertIn(text, entity)
        general = files["kb/entities/organization.md"].decode()
        self.assertIn("## 项目判断", general)
        self.assertNotIn("## 外部依据", general)
        topic = files["kb/topics/topic.md"].decode()
        for text in ("item-one", "external-one", "closeMatch", "https://example.invalid/status", "kb/sources/registry"):
            self.assertIn(text, topic)
        use = files["kb/sources/registry.md"].decode()
        self.assertIn("kb_approved_roles", use)
        self.assertIn("source-fixture-decision", use)
        self.assertNotIn("[[fixture-decision", use)
        index = files["index.md"].decode()
        self.assertIn("audit/fixture#source", index)
        for value in ("隔离记录", "lom", "isolated", "decision-source-0011"):
            self.assertIn(value, index)
        self.assertNotIn("[[kb/sources/lom", index)
        self.assertNotIn("[[decision-source-0011", index)

    def test_written_export_resolves_table_links_and_covers_manifest(self):
        result = write_export(self.root, Path(self.temp.name) / "export")
        self.assertGreater(result["content_files"], 0)

    def test_old_shape_unknown_keys_and_unapproved_roles_are_rejected(self):
        for change in (lambda d: d["entities"].pop("schema"),
                       lambda d: d["forms"]["arrays"][1]["local_analysis"].update(state="active"),
                       lambda d: d["forms"]["arrays"][1]["local_analysis"].update(decision="source-fixture-decision"),
                       lambda d: d["forms"]["arrays"][1]["local_analysis"].update(source="lom"),
                       lambda d: d["topics"]["concepts"][0]["source"]["basis"][0].pop("checked"),
                       lambda d: d["topics"]["concepts"][0].update(source="registry"),
                       lambda d: d["topics"]["concepts"][0]["source"].update(extra="lost"),
                       lambda d: d["sources"]["sources"][0]["roles"][1].update(status="proposed", decision=None),
                       lambda d: d["topics"]["concepts"][0]["source"]["basis"][0].update(entity="missing")):
            documents = copy.deepcopy(documents_v2())
            change(documents)
            with self.assertRaises(ExportError):
                load(documents)
