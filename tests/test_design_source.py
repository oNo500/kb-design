import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))


class DesignSourceTests(unittest.TestCase):
    """The adapter must only publish exports from its exact frozen inputs."""

    design_root = Path(os.environ.get("KB_DESIGN_ROOT", "/Users/xiu/code/kb-design"))

    def clone_design(self, destination: Path) -> Path:
        subprocess.run(
            ["git", "clone", "--quiet", "--shared", str(self.design_root), str(destination)],
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

    def test_exports_the_current_design_as_only_a_verified_kb_tree(self) -> None:
        """A valid snapshot must publish KB without leaking upstream artifacts."""
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
            self.assertTrue((output / "KB").is_dir())
            self.assertEqual(["KB"], sorted(path.name for path in output.iterdir()))

    def test_rejects_export_when_manifest_inputs_differ_from_the_snapshot(self) -> None:
        """A post-snapshot source edit must not be exported under old hashes."""
        from kb_obsidian.design_source import load_design
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reference_export import export_reference

        with tempfile.TemporaryDirectory() as temporary:
            root = self.clone_design(Path(temporary) / "design")
            output = Path(temporary) / "output"
            output.mkdir()
            snapshot = load_design(root.resolve())
            topics = root / "vocab" / "topics.yaml"
            topics.write_bytes(topics.read_bytes() + b"\n")

            with self.assertRaisesRegex(ApplicationError, "input hash mismatch"):
                export_reference(snapshot, output)

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


if __name__ == "__main__":
    unittest.main()
