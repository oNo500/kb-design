from __future__ import annotations

import datetime as dt
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from uuid import UUID


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
TEST_DESIGN_COMMIT = "1e7aef8a5d9dc927c1c69138e61dfbabddd84253"

CONTENT_UUID = "123e4567-e89b-42d3-a456-426614174000"


class VaultBindingTests(unittest.TestCase):
    """Every mutating or consuming flow must use the initialized vault snapshot."""

    design_root = Path("/Users/xiu/code/kb-design")

    @classmethod
    def setUpClass(cls) -> None:
        from kb_obsidian.design_source import load_design
        from kb_obsidian.vault import initialize_vault

        cls.class_temporary = tempfile.TemporaryDirectory()
        cls.class_root = Path(cls.class_temporary.name)
        cls.design = cls.class_root / "design"
        subprocess.run(
            ["git", "clone", "--quiet", "--shared", str(cls.design_root), str(cls.design)],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "-C", str(cls.design), "checkout", "--quiet", TEST_DESIGN_COMMIT],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.snapshot = load_design(cls.design.resolve())
        cls.initialized = cls.class_root / "initialized"
        initialize_vault(cls.design.resolve(), cls.initialized)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.class_temporary.cleanup()

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_content_only_directory_is_rejected_before_creation_or_validation(self) -> None:
        """Checking only content or app would let an uninitialized directory consume design data."""
        from kb_obsidian.create_content import create_content
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.validation import validate_content

        fake = self.root / "fake-vault"
        (fake / "content").mkdir(parents=True)
        calls = (
            lambda: create_content(
                self.snapshot,
                fake,
                title="伪库内容",
                type_id="explanation",
                genre_id="analysis",
                subjects=["security"],
                uuid_factory=lambda: UUID(CONTENT_UUID),
                today=lambda: dt.date(2026, 9, 3),
            ),
            lambda: validate_content(self.snapshot, fake),
        )

        for call in calls:
            with self.subTest(flow=call.__code__.co_firstlineno):
                before = self._tree_bytes(fake)
                with self.assertRaisesRegex(ApplicationError, r"app/manifest\.json"):
                    call()
                self.assertEqual(before, self._tree_bytes(fake))

    def test_manifest_schema_commit_and_inputs_are_bound_to_the_snapshot(self) -> None:
        """Accepting another schema, application, commit, or input set would detach the vault snapshot."""
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.vault import verify_vault

        mutations = {
            "schema": lambda manifest: manifest.__setitem__("schema", "other-vault"),
            "schema_version": lambda manifest: manifest.__setitem__("schema_version", 2),
            "app_version": lambda manifest: manifest.__setitem__("app_version", "99.0.0"),
            "design_commit": lambda manifest: manifest.__setitem__("design_commit", "other-commit"),
            "input_hash": lambda manifest: manifest["inputs"][0].__setitem__("sha256", "0" * 64),
            "input_duplicate": lambda manifest: manifest["inputs"].append(dict(manifest["inputs"][0])),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                vault = self._copy_initialized(name)
                manifest = self._read_manifest(vault)
                mutate(manifest)
                self._write_manifest(vault, manifest)
                before = self._tree_bytes(vault)

                with self.assertRaisesRegex(ApplicationError, r"app/manifest\.json"):
                    verify_vault(self.snapshot, vault)

                self.assertEqual(before, self._tree_bytes(vault))

    def test_managed_file_hash_drift_is_rejected_for_each_owned_kind(self) -> None:
        """Skipping a managed ownership kind would leave that part of the application unaudited."""
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.vault import verify_vault

        all_entries = self._read_manifest(self.initialized)["files"]
        entries_by_kind = {}
        for entry in all_entries:
            entries_by_kind.setdefault(entry["kind"], entry)
        entries = list(entries_by_kind.values())
        self.assertEqual({"reference", "template", "view", "rule"}, set(entries_by_kind))
        vault = self._copy_initialized("managed-drift")
        for index, entry in enumerate(entries):
            with self.subTest(path=entry["path"]):
                path = vault / entry["path"]
                original = path.read_bytes()
                path.write_bytes(original + f"drift-{index}\n".encode("ascii"))
                before = self._tree_bytes(vault)

                with self.assertRaisesRegex(ApplicationError, entry["path"]):
                    verify_vault(self.snapshot, vault)

                self.assertEqual(before, self._tree_bytes(vault))
                path.write_bytes(original)

    def test_manifest_file_shape_path_kind_duplicates_and_coverage_are_strict(self) -> None:
        """Loose file entries could hide unsafe paths, wrong ownership, or unlisted managed bytes."""
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.vault import verify_vault

        mutations = {
            "shape": lambda vault, manifest: manifest["files"][0].__setitem__("extra", True),
            "unsafe_path": lambda vault, manifest: manifest["files"][0].__setitem__("path", "../outside"),
            "wrong_kind": lambda vault, manifest: manifest["files"][0].__setitem__("kind", "wrong-kind"),
            "duplicate": lambda vault, manifest: manifest["files"].append(dict(manifest["files"][0])),
            "unlisted": self._add_unlisted_managed_file,
            "missing": self._remove_listed_managed_file,
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                vault = self._copy_initialized(name)
                manifest = self._read_manifest(vault)
                mutate(vault, manifest)
                self._write_manifest(vault, manifest)

                with self.assertRaises(ApplicationError):
                    verify_vault(self.snapshot, vault)

    def test_formal_kb_target_cannot_be_removed_from_both_manifest_and_tree(self) -> None:
        """Bidirectional coverage alone must not allow a snapshot object to lose its actual target."""
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.vault import verify_vault

        vault = self._copy_initialized("missing-target")
        target = "kb/topics/security.md"
        manifest = self._read_manifest(vault)
        manifest["files"] = [entry for entry in manifest["files"] if entry["path"] != target]
        (vault / target).unlink()
        self._write_manifest(vault, manifest)
        before = self._tree_bytes(vault)

        with self.assertRaisesRegex(ApplicationError, target):
            verify_vault(self.snapshot, vault)

        self.assertEqual(before, self._tree_bytes(vault))

    def test_vault_manifest_and_managed_tree_symlinks_are_rejected(self) -> None:
        """Following a symlink would let verification and later writes escape the selected vault."""
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.vault import verify_vault

        actual = self._copy_initialized("actual")
        linked = self.root / "linked-vault"
        linked.symlink_to(actual, target_is_directory=True)
        with self.assertRaisesRegex(ApplicationError, "symbolic link"):
            verify_vault(self.snapshot, linked)

        for relative_path in ("app/manifest.json", "kb/topics/security.md"):
            with self.subTest(relative_path=relative_path):
                vault = self._copy_initialized(relative_path.replace("/", "-"))
                path = vault / relative_path
                outside = self.root / (path.name + ".outside")
                outside.write_bytes(path.read_bytes())
                path.unlink()
                path.symlink_to(outside)
                with self.assertRaisesRegex(ApplicationError, str(path)):
                    verify_vault(self.snapshot, vault)

        vault = self._copy_initialized("linked-app")
        outside_app = self.root / "outside-app"
        (vault / "app").rename(outside_app)
        (vault / "app").symlink_to(outside_app, target_is_directory=True)
        with self.assertRaisesRegex(ApplicationError, str(vault / "app")):
            verify_vault(self.snapshot, vault)

    def test_real_initialized_vault_supports_create_and_validate(self) -> None:
        """Mock-isolated unit tests cannot prove the two Task 2 public flows share the real vault gate."""
        from kb_obsidian.create_content import create_content
        from kb_obsidian.validation import validate_content

        vault = self._copy_initialized("integration")
        path = create_content(
            self.snapshot,
            vault,
            title="绑定测试",
            type_id="explanation",
            genre_id="analysis",
            subjects=["security"],
            uuid_factory=lambda: UUID(CONTENT_UUID),
            today=lambda: dt.date(2026, 9, 3),
        )
        validation = validate_content(self.snapshot, vault)
        self.assertEqual(vault.resolve() / "content" / f"{CONTENT_UUID}.md", path)
        self.assertTrue(validation.is_valid, validation.issues)
        self.assertEqual(1, len(validation.valid_records))

    def _copy_initialized(self, name: str) -> Path:
        vault = self.root / name
        shutil.copytree(self.initialized, vault)
        return vault

    @staticmethod
    def _read_manifest(vault: Path) -> dict[str, object]:
        return json.loads((vault / "app" / "manifest.json").read_text(encoding="utf-8"))

    @staticmethod
    def _write_manifest(vault: Path, manifest: dict[str, object]) -> None:
        (vault / "app" / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _tree_bytes(root: Path) -> dict[str, bytes]:
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in sorted(root.rglob("*"))
            if path.is_file() and not path.is_symlink()
        }

    @staticmethod
    def _add_unlisted_managed_file(vault: Path, manifest: dict[str, object]) -> None:
        del manifest
        (vault / "kb" / "topics" / "unlisted.md").write_bytes(b"unlisted\n")

    @staticmethod
    def _remove_listed_managed_file(vault: Path, manifest: dict[str, object]) -> None:
        del vault
        manifest["files"].pop()


if __name__ == "__main__":
    unittest.main()
