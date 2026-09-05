import csv
import io
import pathlib
import subprocess
import sys
import tempfile
import unittest

from kb_core.governance.migrate_terms import (
    INHERITED_FIELDS,
    LEDGER_FIELDS,
    parse_exact_action,
    parse_inventory,
    parse_location,
    render_inherited_decisions,
    render_migration_ledger,
)


ROOT = pathlib.Path(__file__).resolve().parents[4]
FROZEN_FIXTURE_ROOT = (
    ROOT / "tests" / "fixtures" / "governance-frozen-2026-08-31"
)
INVENTORY = FROZEN_FIXTURE_ROOT / "term-glossary.tsv"
INHERITED = ROOT / "tests" / "fixtures" / "terminology" / "decisions" / "inherited.tsv"
TERMS = ROOT / "data" / "audit" / "migrations" / "term-v1" / "terms.tsv"


def parse_tsv(value):
    return list(csv.DictReader(io.StringIO(value.decode("utf-8")), delimiter="\t"))


def read_tsv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


class TermMigrationTests(unittest.TestCase):
    def test_inherited_ledger_closes_all_348_identities(self):
        rows = parse_tsv(render_migration_ledger(INVENTORY))
        self.assertEqual(348, len(rows))
        self.assertEqual(348, len({row["legacy_identity"] for row in rows}))

    def test_frozen_actions_map_to_inherited_dispositions(self):
        rows = parse_tsv(render_migration_ledger(INVENTORY))
        counts = {}
        for row in rows:
            key = (row["current_action"], row["disposition"])
            counts[key] = counts.get(key, 0) + 1
        self.assertEqual(
            {
                ("defer", "audit-only"): 286,
                ("keep", "retain-owner"): 56,
                ("remove", "retain-pending-l3"): 6,
            },
            counts,
        )

    def test_ledger_preserves_every_frozen_inventory_cell(self):
        source_rows = read_tsv(INVENTORY)
        ledger_rows = parse_tsv(render_migration_ledger(INVENTORY))
        self.assertEqual(len(source_rows), len(ledger_rows))
        for source, ledger in zip(source_rows, ledger_rows):
            self.assertEqual(source, {field: ledger[field] for field in source})

    def test_ledger_carries_no_formal_term_identity_or_status(self):
        forbidden = {
            "concept_id",
            "term_id",
            "workflow",
            "administrative_status",
            "language_override",
        }
        self.assertTrue(forbidden.isdisjoint(LEDGER_FIELDS))
        self.assertEqual(
            (
                "legacy_identity",
                "disposition",
                "decision_evidence",
            ),
            INHERITED_FIELDS,
        )

    def test_tracked_ledger_and_inherited_fixture_are_deterministic(self):
        self.assertEqual(TERMS.read_bytes(), render_migration_ledger(INVENTORY))
        self.assertEqual(INHERITED.read_bytes(), render_inherited_decisions(INVENTORY))

    def test_location_parser_rejects_non_frozen_shapes(self):
        location = parse_location("第 155 行；小节=元数据；后草案审查表第 2 行")
        self.assertEqual((155, "元数据"), (location.line, location.section))
        for value in (
            "155；小节=元数据；后草案审查表第 2 行",
            "第 155 行；元数据；后草案审查表第 2 行",
            "第 155 行；小节=元数据；",
            "第 155 行；小节=元数据；小节=别处；后草案审查表第 2 行",
        ):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "TERM_INVENTORY_LOCATION"):
                    parse_location(value)

    def test_action_parser_rejects_missing_unknown_or_duplicate_actions(self):
        self.assertEqual("defer", parse_exact_action("当前动作=defer；处理阶段=术语迁移"))
        for value in (
            "处理阶段=术语迁移",
            "当前动作=admit；处理阶段=术语迁移",
            "当前动作=defer；当前动作=keep；处理阶段=术语迁移",
        ):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "TERM_INVENTORY_ACTION"):
                    parse_exact_action(value)

    def test_cli_materializes_exact_outputs_and_validation_detects_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = pathlib.Path(tmp) / "terms.tsv"
            inherited = pathlib.Path(tmp) / "inherited.tsv"
            command = [
                sys.executable,
                "-m",
                "kb_core.governance.migrate_terms",
                "materialize",
                "--inventory",
                str(INVENTORY),
                "--output",
                str(output),
                "--inherited-output",
                str(inherited),
            ]
            result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(TERMS.read_bytes(), output.read_bytes())
            self.assertEqual(INHERITED.read_bytes(), inherited.read_bytes())

            validate = command[:3] + [
                "validate",
                "--inventory",
                str(INVENTORY),
                "--ledger",
                str(output),
            ]
            result = subprocess.run(validate, cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr)

            output.write_bytes(output.read_bytes().replace(b"audit-only", b"retain-owner", 1))
            result = subprocess.run(validate, cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(1, result.returncode)
            self.assertIn("TERM_LEDGER_DRIFT", result.stderr)


if __name__ == "__main__":
    unittest.main()
