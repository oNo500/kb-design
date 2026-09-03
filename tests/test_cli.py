from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))


class CliTests(unittest.TestCase):
    """The CLI must compose the public application flows into a stable process contract."""

    design_root = Path("/Users/xiu/code/kb-design")

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

    def _invoke(self, *arguments: str) -> tuple[int, str, str]:
        from kb_obsidian.cli import main

        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                result = main(list(arguments))
            except SystemExit as exc:
                result = exc.code
        self.assertIsInstance(result, int)
        return result, stdout.getvalue(), stderr.getvalue()

    def _assert_json_line(self, output: str) -> dict[str, object]:
        self.assertEqual(1, len(output.splitlines()))
        value = json.loads(output)
        self.assertIsInstance(value, dict)
        self.assertEqual(
            json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n",
            output,
        )
        return value

    def test_composes_init_new_content_validate_and_report_with_one_json_line_each(self) -> None:
        """A command wired to the wrong public flow or a noisy dependency must break the CLI contract."""
        with tempfile.TemporaryDirectory() as temporary:
            vault = Path(temporary) / "vault"
            code, output, error = self._invoke(
                "init",
                "--design-root",
                str(self.design.resolve()),
                "--output",
                str(vault),
            )
            self.assertEqual(0, code, error)
            self.assertEqual("", error)
            initialized = self._assert_json_line(output)
            self.assertEqual("1452cb5856fb873b21ba7a4d79651cb8cc853381", initialized["design_commit"])

            code, output, error = self._invoke(
                "new-content",
                "--design-root",
                str(self.design.resolve()),
                "--vault",
                str(vault),
                "--title",
                "CLI 集成内容",
                "--type",
                "explanation",
                "--genre",
                "analysis",
                "--subject",
                "artificial-intelligence",
                "--subject",
                "security",
                "--entity",
                "openai",
                "--entity",
                "anthropic",
                "--reference",
                "gbt-13745",
                "--reference",
                "cs2023",
                "--form",
                "narrative-text",
                "--level",
                "understand",
                "--language",
                "en",
            )
            self.assertEqual(0, code, error)
            self.assertEqual("", error)
            created = self._assert_json_line(output)
            created_path = Path(created["path"])
            self.assertTrue(created_path.is_absolute())
            self.assertEqual(vault.resolve() / "content", created_path.parent)
            self.assertTrue(created_path.is_file())

            code, output, error = self._invoke(
                "validate",
                "--design-root",
                str(self.design.resolve()),
                "--vault",
                str(vault),
            )
            self.assertEqual(0, code, error)
            self.assertEqual("", error)
            validation = self._assert_json_line(output)
            self.assertEqual(1, validation["record_count"])
            self.assertEqual(1, validation["valid_record_count"])
            self.assertEqual(0, validation["issue_count"])
            self.assertTrue(validation["is_valid"])

            code, output, error = self._invoke(
                "report",
                "--design-root",
                str(self.design.resolve()),
                "--vault",
                str(vault),
            )
            self.assertEqual(0, code, error)
            self.assertEqual("", error)
            reported = self._assert_json_line(output)
            self.assertEqual(1, reported["valid_record_count"])
            self.assertEqual(0, reported["issue_count"])
            self.assertEqual(7, len(reported["files"]))

    def test_validate_issues_are_one_prefixed_json_error_line_and_exit_one(self) -> None:
        """Sending semantic issues to success output or hiding their context breaks automation."""
        from kb_obsidian.validation import Issue, ValidationResult

        issue = Issue(
            code="content.title_mismatch",
            path=Path("Content/123e4567-e89b-42d3-a456-426614174000.md"),
            field="title",
            message="title metadata differs",
        )
        validation = ValidationResult((), (issue,))
        with patch("kb_obsidian.cli.load_design", return_value=object()), patch(
            "kb_obsidian.cli.validate_content", return_value=validation
        ):
            code, output, error = self._invoke(
                "validate",
                "--design-root",
                "/design",
                "--vault",
                "/vault",
            )

        self.assertEqual(1, code)
        self.assertEqual("", output)
        self.assertEqual(1, len(error.splitlines()))
        prefix = "KB_OBSIDIAN_ERROR: "
        self.assertTrue(error.startswith(prefix))
        summary = json.loads(error.removeprefix(prefix))
        self.assertEqual(
            {
                "is_valid": False,
                "issue_count": 1,
                "issues": [
                    {
                        "code": "content.title_mismatch",
                        "field": "title",
                        "message": "title metadata differs",
                        "path": "Content/123e4567-e89b-42d3-a456-426614174000.md",
                    }
                ],
                "record_count": 0,
                "valid_record_count": 0,
            },
            summary,
        )
        self.assertEqual(
            prefix
            + json.dumps(summary, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
            + "\n",
            error,
        )

    def test_argument_errors_use_the_one_line_application_error_contract(self) -> None:
        """Argparse usage dumps and exit code 2 would create a second incompatible error API."""
        code, output, error = self._invoke("validate", "--design-root", "/design")

        self.assertEqual(1, code)
        self.assertEqual("", output)
        self.assertEqual(1, len(error.splitlines()))
        self.assertTrue(error.startswith("KB_OBSIDIAN_ERROR: "))
        self.assertIn("--vault", error)

    def test_rejects_every_repeated_single_value_option_before_domain_work(self) -> None:
        """Silently keeping the last single-value option would accept conflicting command input."""
        cases = (
            (
                "init",
                ["init", "--design-root", "/design", "--output", "/vault"],
                ("--design-root", "--output"),
            ),
            (
                "new-content",
                [
                    "new-content",
                    "--design-root",
                    "/design",
                    "--vault",
                    "/vault",
                    "--title",
                    "title",
                    "--type",
                    "explanation",
                    "--genre",
                    "analysis",
                    "--subject",
                    "security",
                    "--form",
                    "narrative-text",
                    "--level",
                    "understand",
                    "--language",
                    "en",
                ],
                (
                    "--design-root",
                    "--vault",
                    "--title",
                    "--type",
                    "--genre",
                    "--form",
                    "--level",
                    "--language",
                ),
            ),
            (
                "validate",
                ["validate", "--design-root", "/design", "--vault", "/vault"],
                ("--design-root", "--vault"),
            ),
            (
                "report",
                ["report", "--design-root", "/design", "--vault", "/vault"],
                ("--design-root", "--vault"),
            ),
        )

        for command, arguments, options in cases:
            for option in options:
                with self.subTest(command=command, option=option):
                    index = arguments.index(option)
                    repeated = arguments[: index + 2] + arguments[index : index + 2] + arguments[index + 2 :]
                    code, output, error = self._invoke(*repeated)

                    self.assertEqual(1, code)
                    self.assertEqual("", output)
                    self.assertEqual(1, len(error.splitlines()))
                    self.assertEqual(
                        f"KB_OBSIDIAN_ERROR: argument error: argument {option}: may not be repeated\n",
                        error,
                    )

    def test_expected_file_errors_are_one_line_without_a_traceback(self) -> None:
        """An expected filesystem failure must remain a user-facing error rather than escape main."""
        missing = FileNotFoundError(2, "No such file or directory", "/missing/design")
        with patch("kb_obsidian.cli.load_design", side_effect=missing):
            code, output, error = self._invoke(
                "validate",
                "--design-root",
                "/missing/design",
                "--vault",
                "/vault",
            )

        self.assertEqual(1, code)
        self.assertEqual("", output)
        self.assertEqual(1, len(error.splitlines()))
        self.assertTrue(error.startswith("KB_OBSIDIAN_ERROR: "))
        self.assertIn("/missing/design", error)
        self.assertNotIn("Traceback", error)

    def test_module_entrypoint_propagates_an_application_failure_exit_code(self) -> None:
        """Ignoring main's return value would make a real Python module process report false success."""
        environment = os.environ.copy()
        environment["PYTHONPATH"] = "src"

        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "kb_obsidian",
                "validate",
                "--design-root",
                "/definitely/missing/design",
                "--vault",
                "/definitely/missing/vault",
            ],
            cwd=PROJECT_ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(1, completed.returncode)
        self.assertEqual("", completed.stdout)
        self.assertEqual(1, len(completed.stderr.splitlines()))
        self.assertEqual(
            "KB_OBSIDIAN_ERROR: design root does not exist: /definitely/missing/design\n",
            completed.stderr,
        )

    def test_help_exits_zero_without_using_the_error_channel(self) -> None:
        """Treating help as an application failure would make command discovery unreliable."""
        code, output, error = self._invoke("--help")

        self.assertEqual(0, code)
        self.assertIn("{init,new-content,validate,report}", output)
        self.assertEqual("", error)


if __name__ == "__main__":
    unittest.main()
