import subprocess
import tempfile
import unittest
from pathlib import Path


class TermGitTests(unittest.TestCase):
    def git(self, root, *arguments):
        return subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=True,
            capture_output=True,
        ).stdout

    def repository(self, directory):
        root = Path(directory) / "design"
        path = root / "data/vocab/terms.yaml"
        path.parent.mkdir(parents=True)
        self.git(root.parent, "init", "--quiet", str(root))
        self.git(root, "config", "user.email", "test@example.invalid")
        self.git(root, "config", "user.name", "Test")
        (root / "README.md").write_text("fixture\n")
        self.git(root, "add", ".")
        self.git(root, "commit", "--quiet", "-m", "baseline")
        return root, path

    def commit_terms(self, root, path, content, message):
        path.write_bytes(content)
        self.git(root, "add", "data/vocab/terms.yaml")
        self.git(root, "commit", "--quiet", "-m", message)

    def test_non_git_independent_input_has_no_claimed_previous_value(self):
        from kb_core.governance.term_git import captured_previous_terms

        with tempfile.TemporaryDirectory() as temporary:
            self.assertIsNone(captured_previous_terms(Path(temporary), b"current\n"))

    def test_uncommitted_independent_current_value_uses_head_as_previous(self):
        from kb_core.governance.term_git import captured_previous_terms

        with tempfile.TemporaryDirectory() as temporary:
            root, path = self.repository(temporary)
            self.commit_terms(root, path, b"A\n", "A")

            self.assertEqual(b"A\n", captured_previous_terms(root, b"B\n"))

    def test_committed_current_value_uses_latest_data_commit_first_parent(self):
        from kb_core.governance.term_git import captured_previous_terms

        with tempfile.TemporaryDirectory() as temporary:
            root, path = self.repository(temporary)
            self.commit_terms(root, path, b"A\n", "A")
            self.commit_terms(root, path, b"B\n", "B")
            (root / "README.md").write_text("docs only\n")
            self.git(root, "add", "README.md")
            self.git(root, "commit", "--quiet", "-m", "docs")
            head = self.git(root, "rev-parse", "HEAD").decode().strip()

            self.assertEqual(
                b"A\n",
                captured_previous_terms(root, b"B\n", commit=head),
            )

    def test_invalid_explicit_commit_is_not_treated_as_no_history(self):
        from kb_core.governance.term_git import TermGitError, captured_previous_terms

        with tempfile.TemporaryDirectory() as temporary:
            root, _ = self.repository(temporary)
            with self.assertRaises(TermGitError):
                captured_previous_terms(root, b"current\n", commit="0" * 40)


if __name__ == "__main__":
    unittest.main()
