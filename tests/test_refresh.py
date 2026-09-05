from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from kb_obsidian import design_source
from kb_obsidian.design_source import DesignSnapshot
from kb_obsidian.errors import ApplicationError
from kb_obsidian.managed import _VIEWS, _yaml_bytes
from kb_obsidian.vault import _json_bytes, _manifest, _sha256, _write_files, verify_vault


class RefreshTests(unittest.TestCase):
    """Refresh must preserve user bytes and reject unsafe publication transitions."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.design = self.root / "design"
        self.design.mkdir()
        self.git("init", "--quiet")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Test")
        self.documents = {
            "topics": {"concepts": [{"id": "topic", "status": "active", "label": {"zh": "主题"}}], "arrays": []},
            "entities": {"entities": []},
            "sources": {"sources": []},
            "types": {"types": [{"id": "explanation", "status": "active", "label": {"zh": "解释"}}]},
            "genres": {"genres": [{"id": "analysis", "status": "active", "label": {"zh": "分析"}}]},
            "forms": {"forms": []},
        }
        self.old = self.snapshot("old")
        self.new = self.snapshot("new")
        self.vault = self.root / "vault"
        (self.vault / "content").mkdir(parents=True)
        self.references = {
            "kb/topics/topic.md": b"new topic\n",
            "kb/types/explanation.md": b"type\n",
            "kb/genres/analysis.md": b"genre\n",
        }
        self.original = dict(self.references)
        self.original["kb/topics/topic.md"] = b"old topic\n"
        self.original.update({
            "app/templates/inbox.md": b"template\n",
            "app/rules/index.md": b"rules\n",
            "app/views/inbox.base": _yaml_bytes(_VIEWS["app/views/inbox.base"]),
        })
        _write_files(self.vault, self.original)
        _write_files(self.vault, {"app/manifest.json": _json_bytes(_manifest(self.old, self.original))})
        from kb_obsidian.create_content import create_content
        create_content(self.old, self.vault, title="用户内容", type_id="explanation", genre_id="analysis", subjects=["topic"])
        _write_files(self.vault, {
            "home.md": b"[[kb/topics/topic|My topic]]\n",
            "inbox/note.md": b"User note\n",
            "sources/reference.md": b"External note\n",
            "indexes/index.md": b"Index\n",
            "attachments/file.bin": b"\x00\xff",
            ".obsidian/app.json": b'{"user":true}\n',
            "app/reports/data/user.json": b'{"report":true}\n',
        })

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.design), *args], check=True, capture_output=True).stdout.decode().strip()

    def snapshot(self, version):
        hashes = {}
        for name, relative in design_source._FORMAL_DOCUMENTS.items():
            path = self.design / relative
            path.parent.mkdir(exist_ok=True)
            data = yaml.safe_dump(self.documents[name]).encode() + f"# {version}\n".encode()
            path.write_bytes(data)
            hashes[relative] = _sha256(data)
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", version)
        return DesignSnapshot(self.design, self.git("rev-parse", "HEAD"), self.documents, hashes)

    def tree(self):
        return {p.relative_to(self.vault).as_posix(): p.read_bytes() for p in self.vault.rglob("*") if p.is_file()}

    def refresh(self, **kwargs):
        from kb_obsidian.refresh import refresh_vocabulary
        def export(snapshot, target):
            _write_files(target, self.references)
        with patch("kb_obsidian.refresh.load_design", return_value=self.new), patch(
            "kb_obsidian.refresh.export_reference", side_effect=export
        ), patch.object(design_source, "SUPPORTED_DESIGN_COMMITS", {self.old.commit, self.new.commit}, create=True):
            return refresh_vocabulary(self.design, self.vault, **kwargs)

    def test_refresh_changes_only_reference_and_manifest_and_keeps_backup(self):
        before = self.tree()
        result = self.refresh()
        after = self.tree()
        self.assertEqual(b"new topic\n", after["kb/topics/topic.md"])
        self.assertEqual(self.new.commit, result["design_commit"])
        self.assertEqual(1, result["changed_count"])
        self.assertEqual({k: v for k, v in before.items() if not k.startswith("kb/") and k != "app/manifest.json"},
                         {k: v for k, v in after.items() if not k.startswith("kb/") and k != "app/manifest.json"})
        backup = Path(result["backup_path"])
        self.assertEqual(before["kb/topics/topic.md"], (backup / "kb/topics/topic.md").read_bytes())
        self.assertEqual(before["app/manifest.json"], (backup / "app/manifest.json").read_bytes())
        verify_vault(self.new, self.vault)

    def test_rejects_managed_conflicts_without_writes(self):
        for path in ("kb/topics/topic.md", "app/templates/inbox.md", "app/views/inbox.base"):
            with self.subTest(path=path):
                original = (self.vault / path).read_bytes()
                (self.vault / path).write_bytes(b"semantic change\n")
                before = self.tree()
                with self.assertRaises(ApplicationError):
                    self.refresh()
                self.assertEqual(before, self.tree())
                (self.vault / path).write_bytes(original)

    def test_accepts_only_proven_formatting_drift_and_preserves_bytes(self):
        path = "app/views/inbox.base"
        data = json.dumps(_VIEWS[path], ensure_ascii=False).encode()
        (self.vault / path).write_bytes(data)
        result = self.refresh()
        self.assertEqual(data, (self.vault / path).read_bytes())
        self.assertEqual([path], result["normalized_base_formats"])
        verify_vault(self.new, self.vault)

    def test_rejects_forged_old_input_provenance(self):
        path = self.vault / "app/manifest.json"
        manifest = json.loads(path.read_bytes())
        manifest["inputs"][0]["sha256"] = "0" * 64
        path.write_bytes(_json_bytes(manifest))
        before = self.tree()
        with self.assertRaisesRegex(ApplicationError, "input"):
            self.refresh()
        self.assertEqual(before, self.tree())

    def test_manifest_publication_failure_rolls_back_both_parts(self):
        before = self.tree()
        real_replace = os.replace
        failed = False
        def failing_replace(src, dst):
            nonlocal failed
            if Path(dst) == self.vault.resolve() / "app/manifest.json" and not failed:
                failed = True
                raise OSError("injected publication failure")
            return real_replace(src, dst)
        with patch("kb_obsidian.refresh.os.replace", side_effect=failing_replace):
            with self.assertRaisesRegex(ApplicationError, "publication"):
                self.refresh()
        self.assertEqual(before, self.tree())

    def test_dry_run_leaves_all_vault_bytes_unchanged(self):
        before = self.tree()
        result = self.refresh(dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertIsNone(result["backup_path"])
        self.assertEqual(before, self.tree())

    def test_rejects_unknown_base_baseline_even_when_current_yaml_matches(self):
        path = self.vault / "app/manifest.json"
        manifest = json.loads(path.read_bytes())
        for entry in manifest["files"]:
            if entry["path"] == "app/views/inbox.base":
                entry["sha256"] = "0" * 64
        path.write_bytes(_json_bytes(manifest))
        before = self.tree()
        with self.assertRaisesRegex(ApplicationError, "hash"):
            self.refresh()
        self.assertEqual(before, self.tree())

    def test_rejects_concurrent_managed_edit_without_publishing(self):
        from kb_obsidian.refresh import _reference_files
        def read_after_edit(reference_root):
            (self.vault / "kb/topics/topic.md").write_bytes(b"concurrent user edit\n")
            return _reference_files(reference_root)
        with patch("kb_obsidian.refresh._reference_files", side_effect=read_after_edit):
            with self.assertRaisesRegex(ApplicationError, "changed during"):
                self.refresh()
        self.assertEqual(b"concurrent user edit\n", (self.vault / "kb/topics/topic.md").read_bytes())
        self.assertEqual(self.old.commit, json.loads((self.vault / "app/manifest.json").read_bytes())["design_commit"])

    def test_accepts_wikilinks_to_markdown_ids_containing_periods(self):
        self.references["kb/topics/topic.v1.md"] = b"Versioned topic\n"
        (self.vault / "inbox/note.md").write_bytes(b"[[kb/topics/topic.v1]]\n")
        result = self.refresh()
        self.assertEqual(self.new.commit, result["design_commit"])

    def test_rejects_reference_removal_that_breaks_existing_markdown(self):
        (self.vault / "inbox/note.md").write_text("[[kb/obsolete]]\n")
        before = self.tree()
        with self.assertRaisesRegex(ApplicationError, "reference"):
            self.refresh()
        self.assertEqual(before, self.tree())

    def test_rejects_content_incompatible_with_new_vocabulary(self):
        self.documents["topics"]["concepts"][0]["status"] = "deprecated"
        before = self.tree()
        with self.assertRaisesRegex(ApplicationError, "content"):
            self.refresh()
        self.assertEqual(before, self.tree())


if __name__ == "__main__":
    unittest.main()
