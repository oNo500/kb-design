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
TEST_DESIGN_COMMIT = "1e7aef8a5d9dc927c1c69138e61dfbabddd84253"


class DesignSourceTests(unittest.TestCase):
    """The adapter must only publish exports from its exact frozen inputs."""

    design_root = Path("/Users/xiu/code/kb-design")

    def clone_design(self, destination: Path) -> Path:
        subprocess.run(
            ["git", "clone", "--quiet", "--shared", str(self.design_root), str(destination)],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "-C", str(destination), "checkout", "--quiet", TEST_DESIGN_COMMIT],
            check=True,
            capture_output=True,
            text=True,
        )
        return destination

    def test_rejects_an_unsupported_design_head(self) -> None:
        """A different Git HEAD must not be treated as the frozen design."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "design"
            subprocess.run(["git", "init", "--quiet", str(root)], check=True)
            (root / "marker").write_text("unsupported\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "marker"], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.invalid",
                    "commit",
                    "--quiet",
                    "-m",
                    "fixture",
                ],
                check=True,
            )

            with self.assertRaisesRegex(ApplicationError, "unsupported design commit"):
                load_design(root.resolve())

    def test_rejects_tracked_changes_in_a_supported_design(self) -> None:
        """A tracked edit must prevent a stale snapshot from being accepted."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            topics = root / "vocab" / "topics.yaml"
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
        from kb_obsidian.design_source import SUPPORTED_DESIGN_COMMIT, load_design
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()

            snapshot = load_design(root.resolve())
            manifest = export_reference(snapshot, output)

            self.assertEqual(SUPPORTED_DESIGN_COMMIT, manifest["design_commit"])
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
            incorrect_hashes["vocab/topics.yaml"] = "0" * 64
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
            exporter = root / "scripts" / "export_obsidian.py"
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
            exporter = root / "scripts" / "export_obsidian.py"
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
