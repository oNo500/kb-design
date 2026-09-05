import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from .design_fixture import REPOSITORY_ROOT, create_clean_design


class DesignSourceTests(unittest.TestCase):
    """The adapter must only publish exports from its exact frozen inputs."""

    def clone_design(self, destination: Path) -> Path:
        root, self.fixture_commit = create_clean_design(destination)
        return root

    @staticmethod
    def commit(root: Path, message: str) -> str:
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        subprocess.run(
            ["git", "-C", str(root), "commit", "--quiet", "-m", message],
            check=True,
        )
        return subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def test_rejects_missing_or_untracked_selected_helper(self) -> None:
        """A selected snapshot must not silently import the installed checkout's helper."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError

        for state in ("missing", "untracked"):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as temporary:
                root = self.clone_design(Path(temporary) / "design")
                helper = root / "packages" / "kb-core" / "src" / "kb_core" / "label_basis.py"
                if state == "missing":
                    helper.unlink()
                    self.commit(root, "remove selected helper")
                else:
                    subprocess.run(
                        ["git", "-C", str(root), "rm", "--quiet", "--cached", str(helper)],
                        check=True,
                    )
                    subprocess.run(
                        ["git", "-C", str(root), "commit", "--quiet", "-m", "untrack selected helper"],
                        check=True,
                    )

                with self.assertRaisesRegex(ApplicationError, "implementation"):
                    load_design(root.resolve())

    def test_executes_the_committed_selected_helper(self) -> None:
        """A differing committed helper must execute from the selected checkout, not the installation."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            helper = root / "packages" / "kb-core" / "src" / "kb_core" / "label_basis.py"
            helper.write_text('raise RuntimeError("SELECTED_HELPER_SENTINEL")\n', encoding="utf-8")
            self.commit(root, "replace selected helper")

            with self.assertRaisesRegex(ApplicationError, "SELECTED_HELPER_SENTINEL"):
                load_design(root.resolve())

    def test_manual_snapshot_export_still_requires_selected_implementation(self) -> None:
        """A manually assembled snapshot must not bypass selected implementation provenance."""
        from kb_obsidian.design_source import DesignSnapshot, load_design
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            baseline = load_design(root.resolve())
            helper = root / "packages" / "kb-core" / "src" / "kb_core" / "label_basis.py"
            helper.unlink()
            commit = self.commit(root, "remove selected helper")
            manual = DesignSnapshot(
                root=baseline.root,
                commit=commit,
                documents=baseline.documents,
                input_hashes=baseline.input_hashes,
            )

            with self.assertRaisesRegex(ApplicationError, "implementation"):
                export_reference(manual, Path(temporary) / "output")

    def test_accepts_a_new_clean_design_commit(self) -> None:
        """New commits must remain usable without an application whitelist update."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.reference_export import export_reference
        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            subprocess.run(["git", "-C", str(root), "-c", "user.name=Test",
                            "-c", "user.email=test@example.invalid", "commit",
                            "--quiet", "--allow-empty", "-m", "new design"], check=True)
            snapshot = load_design(root.resolve())
            self.assertNotEqual(self.fixture_commit, snapshot.commit)
            manifest = export_reference(snapshot, Path(temporary) / "output")
            self.assertEqual(snapshot.commit, manifest["design_commit"])

    def test_default_root_uses_tool_location_independent_of_cwd(self) -> None:
        """Running elsewhere must not silently select another design checkout."""
        from kb_obsidian.design_source import default_design_root
        with mock.patch("pathlib.Path.cwd", return_value=Path("/unrelated")):
            self.assertEqual(REPOSITORY_ROOT, default_design_root())

    def test_rejects_committed_invalid_formal_input(self) -> None:
        """Removing the whitelist must not turn malformed formal data into a snapshot."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError
        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            (root / "data/vocab/topics.yaml").write_text("[]\n")
            subprocess.run(["git", "-C", str(root), "add", "data/vocab/topics.yaml"], check=True)
            subprocess.run(["git", "-C", str(root), "-c", "user.name=Test",
                            "-c", "user.email=test@example.invalid", "commit",
                            "--quiet", "-m", "invalid fixture"], check=True)
            with self.assertRaisesRegex(ApplicationError, "invalid formal design"):
                load_design(root.resolve())

    def test_rejects_tracked_changes_in_a_supported_design(self) -> None:
        """A tracked edit must prevent a stale snapshot from being accepted."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            topics = root / "data" / "vocab" / "topics.yaml"
            topics.write_bytes(topics.read_bytes() + b"\n")

            with self.assertRaisesRegex(ApplicationError, "tracked changes"):
                load_design(root.resolve())

    def test_deeply_freezes_loaded_documents(self) -> None:
        """Nested source mappings and lists must not be mutable through a snapshot."""
        from kb_obsidian.design_source import load_design

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            snapshot = load_design(root.resolve())

            with self.assertRaises(TypeError):
                snapshot.documents["topics"]["version"]["id"] = "changed"
            with self.assertRaises(AttributeError):
                snapshot.documents["topics"]["concepts"].append({"id": "changed"})

    def test_exports_the_current_design_as_only_a_verified_kb_tree(self) -> None:
        """A valid snapshot must publish kb without leaking upstream artifacts."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()

            snapshot = load_design(root.resolve())
            manifest = export_reference(snapshot, output)

            self.assertEqual(self.fixture_commit, manifest["design_commit"])
            self.assertEqual({"topics", "entities", "sources", "types", "genres", "forms"}, set(snapshot.documents))
            self.assertEqual(6, len(snapshot.input_hashes))
            self.assertTrue((output / "kb").is_dir())
            self.assertEqual(["kb"], sorted(path.name for path in output.iterdir()))

    def test_rejects_export_when_manifest_inputs_differ_from_the_snapshot(self) -> None:
        """A post-snapshot source edit must not be exported under old hashes."""
        from types import MappingProxyType

        from kb_obsidian.design_source import DesignSnapshot, load_design
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()
            snapshot = load_design(root.resolve())
            incorrect_hashes = dict(snapshot.input_hashes)
            incorrect_hashes["data/vocab/topics.yaml"] = "0" * 64
            mismatched_snapshot = DesignSnapshot(
                root=snapshot.root,
                commit=snapshot.commit,
                documents=snapshot.documents,
                input_hashes=MappingProxyType(incorrect_hashes),
            )

            with self.assertRaisesRegex(ApplicationError, "input hash mismatch"):
                export_reference(mismatched_snapshot, output)

            self.assertEqual([], list(output.iterdir()))

    def test_rejects_a_nonempty_output_directory(self) -> None:
        """A caller's existing output must not be mixed with the reference tree."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()
            (output / "existing.txt").write_text("keep\n", encoding="utf-8")

            with self.assertRaisesRegex(ApplicationError, "output directory is not empty"):
                export_reference(load_design(root.resolve()), output)

    def test_rejects_a_manifest_with_an_unsupported_schema(self) -> None:
        """A manifest with the wrong schema must not publish its kb tree."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()
            snapshot = load_design(root.resolve())
            real_run = subprocess.run

            def write_wrong_schema(*arguments, **keywords):
                completed = real_run(*arguments, **keywords)
                command = arguments[0]
                if command[0] == sys.executable:
                    manifest_path = Path(command[-1]) / "manifest.json"
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                    manifest["schema"] = "other-schema"
                    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                return completed

            with mock.patch("kb_obsidian.reference_export.subprocess.run", side_effect=write_wrong_schema):
                with self.assertRaisesRegex(ApplicationError, "unsupported manifest schema"):
                    export_reference(snapshot, output)

            self.assertEqual([], list(output.iterdir()))

    def test_rejects_a_manifest_that_does_not_cover_the_export_files(self) -> None:
        """A manifest omitting an actual export file must prevent publication."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()
            snapshot = load_design(root.resolve())
            real_run = subprocess.run

            def omit_export_file(*arguments, **keywords):
                completed = real_run(*arguments, **keywords)
                command = arguments[0]
                if command[0] == sys.executable:
                    manifest_path = Path(command[-1]) / "manifest.json"
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                    manifest["files"].pop()
                    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                return completed

            with mock.patch("kb_obsidian.reference_export.subprocess.run", side_effect=omit_export_file):
                with self.assertRaisesRegex(ApplicationError, "file coverage mismatch"):
                    export_reference(snapshot, output)

            self.assertEqual([], list(output.iterdir()))

    def test_rejects_a_manifest_file_hash_that_differs_from_its_bytes(self) -> None:
        """A manifest file digest must match the bytes produced by the exporter."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()
            snapshot = load_design(root.resolve())
            real_run = subprocess.run

            def write_wrong_file_hash(*arguments, **keywords):
                completed = real_run(*arguments, **keywords)
                command = arguments[0]
                if command[0] == sys.executable:
                    manifest_path = Path(command[-1]) / "manifest.json"
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                    manifest["files"][0]["sha256"] = "0" * 64
                    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                return completed

            with mock.patch("kb_obsidian.reference_export.subprocess.run", side_effect=write_wrong_file_hash):
                with self.assertRaisesRegex(ApplicationError, "manifest file hash mismatch"):
                    export_reference(snapshot, output)

            self.assertEqual([], list(output.iterdir()))

    def test_preserves_empty_output_when_staging_copy_fails(self) -> None:
        """A failed staging copy must not leave a partial tree in the final output."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()

            with mock.patch("kb_obsidian.reference_export.shutil.copytree", side_effect=OSError("copy blocked")):
                with self.assertRaisesRegex(ApplicationError, "cannot publish verified kb tree"):
                    export_reference(load_design(root.resolve()), output)

            self.assertEqual([], list(output.iterdir()))
            self.assertEqual([], list(Path(temporary).glob(".output.tmp-*")))

    def test_preserves_empty_output_when_directory_replacement_fails(self) -> None:
        """A failed publish replacement must leave the existing output untouched."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()

            with mock.patch("os.replace", side_effect=OSError("replace blocked")):
                with self.assertRaisesRegex(ApplicationError, "cannot publish verified kb tree"):
                    export_reference(load_design(root.resolve()), output)

            self.assertEqual([], list(output.iterdir()))
            self.assertEqual([], list(Path(temporary).glob(".output.tmp-*")))

    def test_preserves_competing_output_written_before_publish(self) -> None:
        """A competing writer must win over publication rather than be overwritten."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()
            real_copytree = shutil.copytree

            def copy_then_compete(source, destination, *arguments, **keywords):
                result = real_copytree(source, destination, *arguments, **keywords)
                (output / "competitor.txt").write_text("preserve\n", encoding="utf-8")
                return result

            with mock.patch("kb_obsidian.reference_export.shutil.copytree", side_effect=copy_then_compete):
                with self.assertRaisesRegex(ApplicationError, "output directory is not empty"):
                    export_reference(load_design(root.resolve()), output)

            self.assertEqual("preserve\n", (output / "competitor.txt").read_text(encoding="utf-8"))
            self.assertEqual(["competitor.txt"], sorted(path.name for path in output.iterdir()))

    def test_rejects_an_exporter_changed_after_the_snapshot(self) -> None:
        """A tracked exporter edit after loading must not reach publication."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()
            snapshot = load_design(root.resolve())
            exporter = root / "apps" / "obsidian" / "src" / "kb_obsidian" / "exporter.py"
            exporter.write_bytes(exporter.read_bytes() + b"\n")

            with self.assertRaisesRegex(ApplicationError, "design source changed since snapshot"):
                export_reference(snapshot, output)

            self.assertEqual([], list(output.iterdir()))

    def test_rechecks_the_design_after_the_exporter_finishes(self) -> None:
        """A source edit during export must prevent its completed tree from publishing."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()
            snapshot = load_design(root.resolve())
            exporter = root / "apps" / "obsidian" / "src" / "kb_obsidian" / "exporter.py"
            real_run = subprocess.run

            def edit_after_export(*arguments, **keywords):
                completed = real_run(*arguments, **keywords)
                command = arguments[0]
                if command[0] == sys.executable:
                    exporter.write_bytes(exporter.read_bytes() + b"\n")
                return completed

            with mock.patch("kb_obsidian.reference_export.subprocess.run", side_effect=edit_after_export):
                with self.assertRaisesRegex(ApplicationError, "design source changed since snapshot"):
                    export_reference(snapshot, output)

            self.assertEqual([], list(output.iterdir()))


if __name__ == "__main__":
    unittest.main()
