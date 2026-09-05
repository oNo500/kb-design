import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from .design_fixture import create_clean_design


class VaultInitializationTests(unittest.TestCase):
    """Initialization must publish only a complete, ownership-separated vault."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.design_temporary = tempfile.TemporaryDirectory()
        cls.design = Path(cls.design_temporary.name) / "design"
        cls.design, cls.design_commit = create_clean_design(cls.design)

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

    def test_allows_default_repository_output_but_rejects_formal_data(self) -> None:
        """Repository output must be usable without exposing source or formal data to vault writes."""
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.vault import initialize_vault

        target = self.design / "output" / "obsidian"
        initialize_vault(self.design.resolve(), target)
        self.assertTrue((target / "app" / "manifest.json").is_file())

        protected = self.design / "data" / "vocab" / "vault"
        with self.assertRaisesRegex(ApplicationError, "protected"):
            initialize_vault(self.design.resolve(), protected)
        self.assertFalse(protected.exists())

    def test_protects_owning_checkout_when_selected_design_is_separate(self) -> None:
        """Selecting another design root must not expose this installation's source checkout."""
        from kb_obsidian import vault as vault_module
        from kb_obsidian.design_source import DesignSnapshot

        owning = self.root / "owning"
        (owning / "data" / "vocab").mkdir(parents=True)
        (owning / "packages").mkdir()
        (owning / "output" / "obsidian").mkdir(parents=True)
        (owning / "pyproject.toml").write_text("[project]\nname = 'owning'\n", encoding="utf-8")
        source = owning / "apps" / "obsidian" / "src" / "kb_obsidian" / "vault.py"
        selected = self.root / "selected"
        selected.mkdir()
        snapshot = DesignSnapshot(selected, "0" * 40, {}, {})

        with patch.object(vault_module, "__file__", str(source)):
            for relative_path in ("packages/new-vault", "data/new-vault"):
                target = owning / relative_path
                target.mkdir(parents=True)
                with self.subTest(flow="init", target=relative_path), self.assertRaisesRegex(
                    vault_module.ApplicationError, "protected"
                ):
                    vault_module._destination(target, selected)
                with self.subTest(flow="existing", target=relative_path), self.assertRaisesRegex(
                    vault_module.ApplicationError, "protected"
                ):
                    vault_module._vault_root(snapshot, target)
                self.assertEqual([], list(target.iterdir()))

            allowed = owning / "output" / "obsidian"
            self.assertEqual(allowed.resolve(), vault_module._destination(allowed, selected))
            self.assertEqual(allowed.resolve(), vault_module._vault_root(snapshot, allowed))

            nested_selected = owning / "packages" / "selected"
            nested_selected.mkdir()
            nested_target = nested_selected / "output" / "obsidian"
            with self.assertRaisesRegex(vault_module.ApplicationError, "protected"):
                vault_module._destination(nested_target, nested_selected)
            self.assertFalse((nested_selected / "output").exists())

    def test_builds_separate_user_managed_report_and_config_boundaries(self) -> None:
        """The manifest must exactly cover managed bytes, never user, report, or config files."""
        from kb_obsidian.vault import initialize_vault

        summary = initialize_vault(self.design.resolve(), self.target)

        self.assertEqual(self.design_commit, summary["design_commit"])
        self.assertEqual(6, len(summary["input_hashes"]))
        self.assertEqual(
            {
                "home.md", "inbox", "sources", "content", "indexes",
                "attachments", "kb", "app", ".obsidian",
            },
            {path.name for path in self.target.iterdir()},
        )
        self.assertTrue((self.target / "home.md").is_file())
        for relative_path in (
            "inbox",
            "sources/clippings",
            "sources/references",
            "sources/files",
            "content",
            "indexes",
            "attachments",
            "app/reports",
        ):
            self.assertTrue((self.target / relative_path).is_dir(), relative_path)

        manifest_path = self.target / "app" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entries = {entry["path"]: entry for entry in manifest["files"]}
        managed_files = {
            path.relative_to(self.target).as_posix()
            for root in (self.target / "kb", self.target / "app" / "templates", self.target / "app" / "views", self.target / "app" / "rules")
            for path in root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(managed_files, set(entries))
        self.assertNotIn("home.md", entries)
        self.assertFalse(any(path.startswith("app/reports/") for path in entries))
        self.assertFalse(any(path.startswith(".obsidian/") for path in entries))
        self.assertFalse(any(path.startswith(("KB/", "App/")) for path in entries))
        self.assertEqual(set(summary["managed_files"]), set(entries))
        for relative_path, entry in entries.items():
            content = (self.target / relative_path).read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), entry["sha256"])
            self.assertIn(entry["kind"], {"reference", "template", "view", "rule"})

    def test_writes_official_bases_filter_shapes(self) -> None:
        """Each application Base must use the official expression or Boolean-group filter schema."""
        from kb_obsidian.vault import initialize_vault

        initialize_vault(self.design.resolve(), self.target)
        bases = sorted((self.target / "app" / "views").glob("*.base"))
        self.assertGreaterEqual(len(bases), 8)
        for path in bases:
            document = yaml.safe_load(path.read_text(encoding="utf-8"))
            expressions = self._filter_expressions(document["filters"])
            self.assertTrue(any(expression.startswith('file.inFolder("') for expression in expressions), path)
            self.assertIn('file.ext == "md"', expressions, path)
        drafts = yaml.safe_load((self.target / "app" / "views" / "drafts.base").read_text(encoding="utf-8"))
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
        home = (self.target / "home.md").read_text(encoding="utf-8")
        targets = [
            link.split("]]", 1)[0].split("|", 1)[0].split("#", 1)[0]
            for link in home.split("[[")[1:]
        ]
        self.assertGreaterEqual(len(targets), 10)
        for target in targets:
            target_path = self.target / target
            self.assertTrue(
                target_path.is_file() or target_path.with_suffix(".md").is_file(),
                target,
            )
        self.assertTrue((self.target / "app" / "reports" / "index.md").is_file())
        self.assertTrue(all(target.startswith(("app/", "kb/")) for target in targets))
        self.assertEqual({"attachmentFolderPath": "attachments", "alwaysUpdateLinks": True}, json.loads((self.target / ".obsidian" / "app.json").read_text(encoding="utf-8")))
        self.assertEqual({"folder": "app/templates"}, json.loads((self.target / ".obsidian" / "templates.json").read_text(encoding="utf-8")))

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
