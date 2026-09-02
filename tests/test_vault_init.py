import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))


class VaultInitializationTests(unittest.TestCase):
    """Initialization must publish only a complete, ownership-separated vault."""

    design_root = Path(os.environ.get("KB_DESIGN_ROOT", "/Users/xiu/code/kb-design"))

    @classmethod
    def setUpClass(cls) -> None:
        cls.design_temporary = tempfile.TemporaryDirectory()
        cls.design = Path(cls.design_temporary.name) / "design"
        subprocess.run(
            ["git", "clone", "--quiet", "--shared", str(cls.design_root), str(cls.design)],
            check=True,
            capture_output=True,
            text=True,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.design_temporary.cleanup()

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.target = self.root / "vault"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_refuses_nonempty_target_without_changing_user_files(self) -> None:
        """An accidental nonempty destination must retain its exact user bytes."""
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.vault import initialize_vault

        self.target.mkdir()
        marker = self.target / "keep.txt"
        marker.write_bytes(b"keep these bytes\\n")

        with self.assertRaisesRegex(ApplicationError, "empty"):
            initialize_vault(self.design.resolve(), self.target)

        self.assertEqual(b"keep these bytes\\n", marker.read_bytes())
        self.assertEqual(["keep.txt"], sorted(path.name for path in self.target.iterdir()))

    def test_refuses_symbolic_link_target_without_following_it(self) -> None:
        """A symlinked destination must never redirect vault writes elsewhere."""
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.vault import initialize_vault

        actual = self.root / "actual"
        actual.mkdir()
        marker = actual / "keep.txt"
        marker.write_bytes(b"outside target\\n")
        self.target.symlink_to(actual, target_is_directory=True)

        with self.assertRaisesRegex(ApplicationError, "symbolic link"):
            initialize_vault(self.design.resolve(), self.target)

        self.assertTrue(self.target.is_symlink())
        self.assertEqual(b"outside target\\n", marker.read_bytes())
        self.assertEqual(["keep.txt"], sorted(path.name for path in actual.iterdir()))

    def test_refuses_protected_targets_before_building(self) -> None:
        """Root, home, application source, and design source are never vault targets."""
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.vault import initialize_vault

        for target in (Path("/"), Path.home(), PROJECT_ROOT, self.design):
            with self.subTest(target=target), self.assertRaisesRegex(ApplicationError, "protected"):
                initialize_vault(self.design.resolve(), target)

    def test_builds_separate_user_managed_report_and_config_boundaries(self) -> None:
        """The manifest must exactly cover managed bytes, never user, report, or config files."""
        from kb_obsidian.vault import initialize_vault

        summary = initialize_vault(self.design.resolve(), self.target)

        self.assertEqual("356f02bc0a61d28c045139b2dc5f41bf40291a78", summary["design_commit"])
        self.assertEqual(6, len(summary["input_hashes"]))
        self.assertTrue((self.target / "Home.md").is_file())
        for relative_path in (
            "Inbox",
            "Sources/Clippings",
            "Sources/References",
            "Sources/Files",
            "Content",
            "Indexes",
            "Attachments",
            "App/Reports",
        ):
            self.assertTrue((self.target / relative_path).is_dir(), relative_path)

        manifest_path = self.target / "App" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entries = {entry["path"]: entry for entry in manifest["files"]}
        managed_files = {
            path.relative_to(self.target).as_posix()
            for root in (self.target / "KB", self.target / "App" / "Templates", self.target / "App" / "Views", self.target / "App" / "Rules")
            for path in root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(managed_files, set(entries))
        self.assertNotIn("Home.md", entries)
        self.assertFalse(any(path.startswith("App/Reports/") for path in entries))
        self.assertFalse(any(path.startswith(".obsidian/") for path in entries))
        self.assertEqual(set(summary["managed_files"]), set(entries))
        for relative_path, entry in entries.items():
            content = (self.target / relative_path).read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), entry["sha256"])
            self.assertIn(entry["kind"], {"reference", "template", "view", "rule"})

    def test_writes_official_bases_filter_shapes(self) -> None:
        """Each application Base must use the official expression or Boolean-group filter schema."""
        from kb_obsidian.vault import initialize_vault

        initialize_vault(self.design.resolve(), self.target)
        bases = sorted((self.target / "App" / "Views").glob("*.base"))
        self.assertGreaterEqual(len(bases), 8)
        for path in bases:
            document = yaml.safe_load(path.read_text(encoding="utf-8"))
            expressions = self._filter_expressions(document["filters"])
            self.assertTrue(any(expression.startswith('file.inFolder("') for expression in expressions), path)
            self.assertIn('file.ext == "md"', expressions, path)
        drafts = yaml.safe_load((self.target / "App" / "Views" / "drafts.base").read_text(encoding="utf-8"))
        self.assertIn('kb_status == "draft"', self._filter_expressions(drafts["filters"]))

    def test_registers_only_actual_content_and_formal_property_bindings(self) -> None:
        """Property types must name only the content contract and Task 2 formal export bindings."""
        from kb_obsidian.vault import initialize_vault

        initialize_vault(self.design.resolve(), self.target)
        types = json.loads((self.target / ".obsidian" / "types.json").read_text(encoding="utf-8"))["types"]
        expected = {
            "aliases": "aliases",
            "title": "text",
            "kb_id": "text",
            "kb_type": "text",
            "kb_genre": "text",
            "kb_form": "text",
            "kb_level": "text",
            "kb_source": "text",
            "kb_status": "text",
            "kb_is_replaced_by": "text",
            "kb_language": "text",
            "kb_object": "text",
            "kb_label": "text",
            "kb_version": "text",
            "kb_replaced_by": "text",
            "kb_superordinate": "text",
            "kb_kind": "text",
            "kb_vendor": "text",
            "kb_tier": "text",
            "kb_entity_version": "text",
            "kb_url": "text",
            "kb_watch": "text",
            "kb_entity": "text",
            "kb_subjects": "multitext",
            "kb_entities": "multitext",
            "kb_references": "multitext",
            "kb_relation": "multitext",
            "kb_creator": "multitext",
            "kb_broader": "multitext",
            "kb_related": "multitext",
            "kb_arrays": "multitext",
            "kb_members": "multitext",
            "kb_roles": "multitext",
            "kb_created": "date",
            "kb_modified": "date",
            "kb_added": "date",
            "kb_checked": "date",
            "tags": "tags",
        }
        self.assertEqual(expected, types)

    def test_links_every_home_entry_to_an_existing_internal_file(self) -> None:
        """Every Home entry must resolve to a generated Base, formal view, or report file."""
        from kb_obsidian.vault import initialize_vault

        initialize_vault(self.design.resolve(), self.target)
        home = (self.target / "Home.md").read_text(encoding="utf-8")
        targets = [
            link.split("]]", 1)[0].split("|", 1)[0].split("#", 1)[0]
            for link in home.split("[[")[1:]
        ]
        self.assertGreaterEqual(len(targets), 10)
        for target in targets:
            self.assertTrue((self.target / target).is_file(), target)
        self.assertTrue((self.target / "App" / "Reports" / "README.md").is_file())

    @staticmethod
    def _filter_expressions(value: object) -> list[str]:
        if isinstance(value, str):
            return [value]
        if not isinstance(value, dict) or len(value) != 1:
            raise AssertionError(f"invalid filter shape: {value!r}")
        operator, children = next(iter(value.items()))
        if operator not in {"and", "or", "not"} or not isinstance(children, list):
            raise AssertionError(f"invalid filter group: {value!r}")
        return [expression for child in children for expression in VaultInitializationTests._filter_expressions(child)]


if __name__ == "__main__":
    unittest.main()
