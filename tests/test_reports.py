from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

UUID_A = "123e4567-e89b-42d3-a456-426614174000"
UUID_B = "223e4567-e89b-42d3-a456-426614174001"


class ReportTests(unittest.TestCase):
    """Reports must count only validated semantics and publish only report bytes."""

    def setUp(self) -> None:
        from kb_obsidian.content import ContentRecord
        from kb_obsidian.design_source import DesignSnapshot
        from kb_obsidian.validation import Issue, ValidationResult

        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.design = self.root / "design"
        self.vault = self.root / "vault"
        self.design.mkdir()
        for relative in (
            "Content",
            "Indexes",
            "KB/Topics",
            "App/Templates",
            "App/Views",
            "App/Rules",
            "App/Reports",
        ):
            (self.vault / relative).mkdir(parents=True, exist_ok=True)

        self.snapshot = DesignSnapshot(
            root=self.design,
            commit="design-commit",
            documents={
                "topics": {
                    "concepts": (
                        {
                            "id": "unassigned-branch",
                            "status": "unassigned",
                            "source": "cs2023",
                            "broader": ("security",),
                        },
                        {
                            "id": "security",
                            "status": "active",
                            "source": "cs2023",
                            "broader": ("computing",),
                        },
                        {
                            "id": "computing",
                            "status": "active",
                            "source": "gbt-13745",
                            "broader": (),
                        },
                        {
                            "id": "artificial-intelligence",
                            "status": "active",
                            "source": "cs2023",
                            "broader": ("computing",),
                        },
                        {
                            "id": "application-security",
                            "status": "active",
                            "source": "self",
                            "broader": ("security",),
                        },
                    )
                }
            },
            input_hashes={"vocab/topics.yaml": "topic-hash"},
        )
        valid = ContentRecord(
            identifier=UUID_A,
            title="有效内容",
            path=Path(f"Content/{UUID_A}.md"),
            properties={
                "aliases": ("[[KB/Topics/artificial-intelligence|人工智能]]",),
                "kb_subjects": ("[[KB/Topics/application-security|应用安全]]",),
            },
            body="正文链接 [[KB/Topics/artificial-intelligence|人工智能]]。\n",
        )
        invalid = ContentRecord(
            identifier=UUID_B,
            title="无效内容",
            path=Path(f"Content/{UUID_B}.md"),
            properties={
                "aliases": ("无效内容",),
                "kb_subjects": ("[[KB/Topics/artificial-intelligence|人工智能]]",),
            },
            body="",
        )
        invalid_issue = Issue(
            code="content.title_mismatch",
            path=invalid.path,
            field="title",
            message="title metadata differs",
        )
        self.validation = ValidationResult((invalid, valid), (invalid_issue,))

        (self.vault / "Content" / f"{UUID_A}.md").write_text(valid.body, encoding="utf-8")
        (self.vault / "Content" / f"{UUID_B}.md").write_text(invalid.body, encoding="utf-8")
        (self.vault / "Indexes" / "ai.md").write_text(
            "[[KB/Topics/artificial-intelligence|人工智能]]\n",
            encoding="utf-8",
        )
        self._write_boundaries()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_counts_only_valid_controlled_subjects_and_aggregates_descendants(self) -> None:
        """Scanning non-controlled links or promoting ancestors to direct use would corrupt usage facts."""
        from kb_obsidian.reports import build_reports

        before_content = self._tree_hashes(self.vault / "Content")
        reports = build_reports(self.snapshot, self.validation, self.vault)
        usage = json.loads(reports["App/Reports/topic-usage.json"])

        self.assertEqual(1, usage["direct"]["application-security"])
        self.assertEqual(0, usage["direct"]["security"])
        self.assertEqual(0, usage["direct"]["computing"])
        self.assertEqual(0, usage["direct"]["artificial-intelligence"])
        self.assertEqual(1, usage["aggregate"]["application-security"])
        self.assertEqual(1, usage["aggregate"]["security"])
        self.assertEqual(1, usage["aggregate"]["computing"])
        self.assertEqual(0, usage["aggregate"]["artificial-intelligence"])
        self.assertEqual(before_content, self._tree_hashes(self.vault / "Content"))
        self.assertEqual(
            ("[[KB/Topics/application-security|应用安全]]",),
            self.validation.valid_records[0].properties["kb_subjects"],
        )

    def test_usage_includes_every_formal_topic_and_review_signals(self) -> None:
        """Dropping empty formal branches or treating threshold matches as actions would hide review evidence."""
        from kb_obsidian.reports import build_reports

        usage = json.loads(build_reports(self.snapshot, self.validation, self.vault)["App/Reports/topic-usage.json"])

        self.assertEqual(
            [
                "application-security",
                "artificial-intelligence",
                "computing",
                "security",
                "unassigned-branch",
            ],
            [topic["id"] for topic in usage["topics"]],
        )
        security = next(topic for topic in usage["topics"] if topic["id"] == "security")
        self.assertEqual(
            {
                "id": "security",
                "status": "active",
                "source": "cs2023",
                "broader": ["computing"],
                "direct": 0,
                "aggregate": 1,
            },
            security,
        )
        self.assertEqual(["unassigned-branch"], usage["signals"]["unassigned"])
        self.assertIn("artificial-intelligence", usage["signals"]["zero_reference"])
        self.assertEqual(["application-security"], usage["signals"]["overuse"])
        self.assertEqual(0.1, usage["overuse_threshold"])

    def test_output_is_deterministic_canonical_and_explicitly_report_only(self) -> None:
        """Input iteration order and platform newlines must not alter the published report set."""
        from kb_obsidian.design_source import DesignSnapshot
        from kb_obsidian.reports import build_reports
        from kb_obsidian.validation import ValidationResult

        first = build_reports(self.snapshot, self.validation, self.vault)
        reversed_snapshot = DesignSnapshot(
            root=self.snapshot.root,
            commit=self.snapshot.commit,
            documents={"topics": {"concepts": tuple(reversed(self.snapshot.documents["topics"]["concepts"]))}},
            input_hashes=self.snapshot.input_hashes,
        )
        reversed_validation = ValidationResult(
            tuple(reversed(self.validation.records)),
            tuple(reversed(self.validation.issues)),
        )
        second = build_reports(reversed_snapshot, reversed_validation, self.vault)

        self.assertEqual(first, second)
        self.assertEqual(
            {
                "App/Reports/README.md",
                "App/Reports/topic-coverage.md",
                "App/Reports/topic-usage.json",
                "App/Reports/unassigned-topics.md",
                "App/Reports/validation.json",
            },
            set(first),
        )
        for path, content in first.items():
            self.assertTrue(content.endswith(b"\n"), path)
            self.assertNotIn(b"\r", content, path)
            text = content.decode("utf-8")
            if path.endswith(".json"):
                parsed = json.loads(text)
                expected = json.dumps(parsed, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
                self.assertEqual(expected, text)
            else:
                self.assertIn("派生", text)
                self.assertIn("人工复核", text)
                self.assertIn("不会自动", text)

        validation = json.loads(first["App/Reports/validation.json"])
        self.assertEqual(2, validation["record_count"])
        self.assertEqual(1, validation["valid_record_count"])
        self.assertEqual(1, validation["issue_count"])
        self.assertEqual(f"Content/{UUID_B}.md", validation["issues"][0]["path"])

    def test_successful_publication_changes_only_reports(self) -> None:
        """A successful report refresh must not write user, KB, managed App, or design-source bytes."""
        from kb_obsidian.reports import write_reports

        (self.vault / "App" / "Reports" / "old.md").write_bytes(b"old report\n")
        before = self._protected_hashes()

        summary = write_reports(self.snapshot, self.validation, self.vault)

        self.assertEqual(before, self._protected_hashes())
        self.assertEqual(
            [
                "App/Reports/README.md",
                "App/Reports/topic-coverage.md",
                "App/Reports/topic-usage.json",
                "App/Reports/unassigned-topics.md",
                "App/Reports/validation.json",
            ],
            summary["files"],
        )
        self.assertFalse((self.vault / "App" / "Reports" / "old.md").exists())
        self.assertEqual(5, len(list((self.vault / "App" / "Reports").iterdir())))
        self.assertEqual([], list((self.vault / "App").glob(".reports-tmp-*")))

    def test_failed_publication_restores_old_reports_and_cleans_only_own_temp(self) -> None:
        """A failed final directory switch must retain every pre-existing boundary and report byte."""
        from kb_obsidian.errors import ApplicationError
        from kb_obsidian.reports import write_reports

        old_report = self.vault / "App" / "Reports" / "old.md"
        old_report.write_bytes(b"old report must survive\n")
        unrelated_temp = self.vault / "App" / ".reports-tmp-unrelated"
        unrelated_temp.mkdir()
        (unrelated_temp / "keep").write_bytes(b"not ours\n")
        before = self._protected_hashes(include_reports=True)
        real_replace = os.replace
        failed = False

        def fail_new_report_publish(source: object, destination: object) -> None:
            nonlocal failed
            source_path = Path(source)
            destination_path = Path(destination)
            if not failed and source_path.name == "new" and destination_path.name == "Reports":
                failed = True
                raise OSError("injected report publication failure")
            real_replace(source, destination)

        with patch("kb_obsidian.reports.os.replace", side_effect=fail_new_report_publish):
            with self.assertRaisesRegex(ApplicationError, "publish reports"):
                write_reports(self.snapshot, self.validation, self.vault)

        self.assertEqual(before, self._protected_hashes(include_reports=True))
        self.assertEqual(b"old report must survive\n", old_report.read_bytes())
        self.assertEqual(b"not ours\n", (unrelated_temp / "keep").read_bytes())
        self.assertEqual([unrelated_temp], list((self.vault / "App").glob(".reports-tmp-*")))

    def _write_boundaries(self) -> None:
        for relative, content in {
            "Home.md": b"user home\n",
            "KB/Topics/security.md": b"formal topic\n",
            "App/Templates/content.md": b"managed template\n",
            "App/Views/content.base": b"managed view\n",
            "App/Rules/README.md": b"managed rules\n",
            "App/manifest.json": b"managed manifest\n",
            "design/topics.yaml": b"formal design source\n",
        }.items():
            path = self.root / relative if relative.startswith("design/") else self.vault / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)

    @staticmethod
    def _tree_hashes(root: Path) -> dict[str, str]:
        return {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def _protected_hashes(self, *, include_reports: bool = False) -> dict[str, dict[str, str]]:
        roots = {
            "Content": self.vault / "Content",
            "Indexes": self.vault / "Indexes",
            "KB": self.vault / "KB",
            "Templates": self.vault / "App" / "Templates",
            "Views": self.vault / "App" / "Views",
            "Rules": self.vault / "App" / "Rules",
            "Design": self.design,
        }
        if include_reports:
            roots["Reports"] = self.vault / "App" / "Reports"
        return {name: self._tree_hashes(root) for name, root in roots.items()}


if __name__ == "__main__":
    unittest.main()
