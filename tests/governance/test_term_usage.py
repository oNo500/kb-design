import json
import pathlib
import subprocess
import tempfile
import unittest

from scripts.governance.check_term_usage import (
    current_markdown_manifest,
    manifest_delta,
    scan_markdown,
)


REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMA = REPOSITORY_ROOT / "schemas" / "term-usage-decisions-v1.schema.json"


class TermUsageTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temporary_directory.name)
        self._write(
            "README.md",
            "# 项目说明\n\n普通说明。\n",
        )
        self._write(
            "concepts/glossary.md",
            "# 术语表 (Glossary)\n\n| 术语 | 定义 |\n|---|---|\n",
        )
        self._write(
            "concepts/current.md",
            "# 术语正文 (Term Prose)\n\n"
            "`同形词` 和 **同形词**。\n\n"
            "```markdown\n**围栏同形词**\n```\n",
        )
        self._write(
            "concepts/no-hits.md",
            "普通正文没有指定抽取位置。\n",
        )
        self._write(
            "sources/reference.md",
            "# 来源记录\n\n来源原文称“同形词”。\n",
        )
        self._write(
            "design/decisions/history.md",
            "# 历史决定\n\n旧决定使用 **同形词**。\n",
        )
        self._write(
            "notes/review.md",
            "# 未知目录标题\n",
        )
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        self.snapshot = {
            "concepts": [
                {
                    "id": "concept-a",
                    "languages": [
                        {
                            "language": "zh-Hans",
                            "terms": [{"id": "term-a", "text": "同形词"}],
                        }
                    ],
                },
                {
                    "id": "concept-b",
                    "languages": [
                        {
                            "language": "zh-Hans",
                            "terms": [{"id": "term-b", "text": "同形词"}],
                        }
                    ],
                },
            ]
        }

    def tearDown(self):
        self.temporary_directory.cleanup()

    def _write(self, relative_path, text):
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _scan(self):
        manifest = current_markdown_manifest(self.root)
        paths = [entry["path"] for entry in manifest]
        return manifest, scan_markdown(self.root, paths, self.snapshot)

    def test_scans_dynamic_markdown_manifest(self):
        manifest, result = self._scan()

        self.assertEqual(
            {entry["path"] for entry in manifest},
            {entry["path"] for entry in result.manifest},
        )
        self.assertEqual(
            "classified-only",
            next(
                entry["scan_state"]
                for entry in result.manifest
                if entry["path"] == "concepts/glossary.md"
            ),
        )
        self.assertEqual(
            "scanned",
            next(
                entry["scan_state"]
                for entry in result.manifest
                if entry["path"] == "concepts/no-hits.md"
            ),
        )
        self.assertEqual(
            "review",
            next(
                entry["classification"]
                for entry in result.manifest
                if entry["path"] == "notes/review.md"
            ),
        )

    def test_markdown_addition_requires_allowed_write(self):
        previous = current_markdown_manifest(self.root)
        self._write("design/new-diagnostic.md", "# 新增诊断\n")
        subprocess.run(
            ["git", "add", "design/new-diagnostic.md"], cwd=self.root, check=True
        )
        current = current_markdown_manifest(self.root)

        self.assertEqual(
            ["design/new-diagnostic.md"],
            manifest_delta(previous, current, allowed=()),
        )
        self.assertEqual(
            [],
            manifest_delta(
                previous, current, allowed=("design/new-diagnostic.md",)
            ),
        )

        (self.root / "sources/reference.md").unlink()
        subprocess.run(
            ["git", "add", "sources/reference.md"], cwd=self.root, check=True
        )
        after_deletion = current_markdown_manifest(self.root)
        self.assertEqual(
            ["sources/reference.md"],
            manifest_delta(
                current,
                after_deletion,
                allowed=("design/new-diagnostic.md",),
            ),
        )

    def test_excluded_contexts_keep_precise_locations(self):
        _, result = self._scan()
        current_hits = [
            hit
            for hit in result
            if hit.file == "concepts/current.md" and hit.normalized == "同形词"
        ]
        source_hit = next(
            hit
            for hit in result
            if hit.file == "sources/reference.md" and hit.normalized == "同形词"
        )
        history_hit = next(
            hit
            for hit in result
            if hit.file == "design/decisions/history.md"
            and hit.normalized == "同形词"
        )

        self.assertEqual([(3, 11, "prose", "bold")], [
            (hit.line, hit.column, hit.context, hit.kind) for hit in current_hits
        ])
        self.assertEqual((3, 7, "context-only", "quote"), (
            source_hit.line,
            source_hit.column,
            source_hit.context,
            source_hit.kind,
        ))
        self.assertEqual("context-only", history_hit.context)
        self.assertFalse(any(hit.raw == "围栏同形词" for hit in result))

    def test_homographs_require_concept_context(self):
        _, result = self._scan()
        hits = [
            hit
            for hit in result
            if hit.normalized == "同形词" and hit.context == "prose"
        ]

        self.assertEqual(1, len(hits))
        self.assertEqual(("concept-a", "concept-b"), hits[0].concept_ids)
        self.assertEqual("review", hits[0].severity)
        self.assertEqual("concept-context-required", hits[0].conclusion)

    def test_first_usage_baseline_is_report_only(self):
        _, result = self._scan()

        self.assertEqual("report-only", result.mode)
        self.assertEqual((), result.blocking_hits)
        self.assertTrue(all(hit.verdict is None for hit in result))

        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        document = {
            "schema": "urn:kb-design:data:term-usage-decisions",
            "version": 1,
            "decisions": [
                {
                    "id": "term-usage-0001",
                    "identity": "concepts/current.md:3:11",
                    "file": "concepts/current.md",
                    "line": 3,
                    "column": 11,
                    "severity": "review",
                    "conclusion": "concept-context-required",
                    "decided": "2026-08-31",
                    "decision": "decision-term-usage-0001",
                    "history": [
                        {
                            "decided": "2026-08-31",
                            "severity": "review",
                            "conclusion": "concept-context-required",
                            "decision": "decision-term-usage-0001",
                        }
                    ],
                }
            ],
        }
        decision_schema = schema["properties"]["decisions"]["items"]
        self.assertEqual(set(document), set(schema["required"]))
        self.assertEqual(
            set(document["decisions"][0]), set(decision_schema["required"])
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertFalse(decision_schema["additionalProperties"])
        self.assertNotIn("verdict", decision_schema["properties"])


if __name__ == "__main__":
    unittest.main()
