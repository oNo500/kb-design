import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class CoreCliSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        vocabulary = self.root / "data" / "vocab"
        vocabulary.mkdir(parents=True)
        (vocabulary / "topics.yaml").write_text("sentinel\n", encoding="utf-8")
        self.command = Path(sys.executable).with_name("kb-core")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def snapshot(self):
        return {
            str(path.relative_to(self.root)): path.read_bytes()
            for path in sorted(self.root.rglob("*"))
            if path.is_file()
        }

    def run_cli(self, *arguments):
        return subprocess.run(
            [self.command, "build-topics", *arguments],
            cwd=self.root,
            capture_output=True,
            text=True,
            env={**os.environ, "KB_DESIGN_ROOT": str(self.root)},
        )

    def test_build_topics_help_exits_without_generation(self):
        before = self.snapshot()

        completed = self.run_cli("--help")

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("usage:", completed.stdout)
        self.assertIn("build-topics", completed.stdout)
        self.assertEqual(before, self.snapshot())

    def test_build_topics_rejects_unknown_arguments_before_generation(self):
        before = self.snapshot()

        completed = self.run_cli("--unsupported")

        self.assertNotEqual(0, completed.returncode)
        self.assertIn("unrecognized arguments: --unsupported", completed.stderr)
        self.assertEqual(before, self.snapshot())


if __name__ == "__main__":
    unittest.main()
