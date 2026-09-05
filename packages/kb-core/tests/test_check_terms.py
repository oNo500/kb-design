import ast
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[3]
SCRIPT = REPOSITORY_ROOT / "packages/kb-core/src/kb_core/check_terms.py"


class CheckTermsTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temporary_directory.name)
        for directory in (
            "docs/concepts",
            "docs/decisions",
            "data/vocab",
        ):
            (self.root / directory).mkdir(parents=True)
        (self.root / "docs" / "glossary.md").write_text(
            """# 术语表 (Glossary)

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 已登记表项 | registered entry | 固定夹具中的登记写法 | test |
""",
            encoding="utf-8",
        )
        (self.root / "data" / "vocab" / "topics.yaml").write_text(
            """concepts:
  - id: registered-labels
    label: { zh: 已登记首选, en: Registered preferred }
    alt: [已登记别名]
    hidden: [已登记隐藏]
""",
            encoding="utf-8",
        )
        (self.root / "data" / "vocab" / "entities.yaml").write_text(
            "entities: []\n", encoding="utf-8"
        )
        (self.root / "data" / "vocab" / "types.yaml").write_text(
            "types: []\n", encoding="utf-8"
        )
        (self.root / "docs" / "concepts" / "fixture.md").write_text(
            """# 标题候选

正文包含 **加粗候选** 和“引号候选”。

# 已登记表项

**已登记首选**、**已登记别名**和“已登记隐藏”都不应报告。
**已登记首选项**不是已批准变体，应保留供人工判断。

`**行内代码候选**` 不应报告。

```markdown
# 围栏标题候选
**围栏加粗候选**
“围栏引号候选”
```

[链接文字](https://example.test/“链接目标”)
""",
            encoding="utf-8",
        )
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def run_script(self):
        completed = subprocess.run(
            [sys.executable, "-m", "kb_core.check_terms", "--all"],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
            env={**os.environ, "KB_DESIGN_ROOT": str(self.root)},
        )
        return completed.stdout

    def candidate_strings(self, output):
        prefix = "  候选字符串："
        marker = "  出现文件数："
        return {
            line.removeprefix(prefix).split(marker, 1)[0]
            for line in output.splitlines()
            if line.startswith(prefix) and marker in line
        }

    def test_includes_approved_candidate_positions(self):
        candidates = self.candidate_strings(self.run_script())

        self.assertTrue({"标题候选", "加粗候选", "引号候选"} <= candidates)

    def test_excludes_code_and_link_targets(self):
        candidates = self.candidate_strings(self.run_script())

        self.assertTrue(
            {
                "行内代码候选",
                "围栏标题候选",
                "围栏加粗候选",
                "围栏引号候选",
                "链接目标",
            }.isdisjoint(candidates)
        )

    def test_excludes_registered_labels_without_guessing_variants(self):
        candidates = self.candidate_strings(self.run_script())

        self.assertTrue(
            {"已登记表项", "已登记首选", "已登记别名", "已登记隐藏"}.isdisjoint(
                candidates
            )
        )
        self.assertIn("已登记首选项", candidates)

    def test_reports_pending_human_judgment_without_term_verdict(self):
        output = self.run_script()

        self.assertIn("待人工判断的候选字符串", output)
        self.assertNotIn("未登记术语", output)
        self.assertNotIn("未登记的候选", output)

    def test_preserves_frozen_term_identities(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        term_loop = any(
            isinstance(node, ast.For)
            and isinstance(node.target, ast.Tuple)
            and any(
                isinstance(element, ast.Name) and element.id == "term"
                for element in node.target.elts
            )
            for node in ast.walk(tree)
        )
        term_placeholder = any(
            isinstance(node, ast.FormattedValue)
            and isinstance(node.value, ast.Name)
            and node.value.id == "term"
            for node in ast.walk(tree)
        )

        self.assertTrue(term_loop)
        self.assertTrue(term_placeholder)

    def test_same_fixture_is_deterministic(self):
        self.assertEqual(self.run_script(), self.run_script())

    def test_json_report_keeps_report_only_state_and_precise_location(self):
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "kb_core.check_terms",
                "--all",
                "--format",
                "json",
            ],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
            env={**os.environ, "KB_DESIGN_ROOT": str(self.root)},
        )
        report = __import__("json").loads(completed.stdout)
        hit = next(
            item for item in report["hits"] if item["normalized"] == "加粗候选"
        )

        self.assertEqual("report-only", report["mode"])
        self.assertEqual(3, hit["line"])
        self.assertEqual(8, hit["column"])
        self.assertNotIn("verdict", hit)


if __name__ == "__main__":
    unittest.main()
