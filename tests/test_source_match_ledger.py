import csv
import pathlib
import unittest
from collections import Counter

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
PARALLEL = (
    ROOT
    / ".superpowers"
    / "sdd"
    / "2026-08-31-source-schema-migration"
    / "parallel"
    / "match"
)
LEDGER = ROOT / "vocab" / "migrations" / "source-v1" / "match.yaml"
PROPOSALS = PARALLEL / "match-proposals.yaml"
BLOCKED = PARALLEL / "blocked.tsv"


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_tsv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


class SourceMatchLedgerTests(unittest.TestCase):
    def ledger(self):
        self.assertTrue(LEDGER.is_file(), f"missing match ledger: {LEDGER}")
        return load_yaml(LEDGER)

    def test_ledger_consumes_parallel_proposals_without_reclassification(self):
        self.assertEqual(load_yaml(PROPOSALS), self.ledger())

    def test_all_756_inventory_identities_close_once(self):
        ledger_rows = self.ledger()["rows"]
        proposal_rows = load_yaml(PROPOSALS)["rows"]
        blocked_rows = load_tsv(BLOCKED)
        expected = {f"match-inventory.tsv:{line}" for line in range(2, 758)}

        self.assertEqual(756, len(ledger_rows))
        self.assertEqual(expected, {row["identity"] for row in ledger_rows})
        self.assertEqual(expected, {row["identity"] for row in proposal_rows})
        self.assertEqual(expected, {row["identity"] for row in blocked_rows})

    def test_all_rows_remain_blocked_and_none_are_registered(self):
        rows = self.ledger()["rows"]
        dispositions = Counter(row["disposition"] for row in rows)

        self.assertEqual(
            {"blocked_unread_material": 756},
            dict(dispositions),
        )
        self.assertEqual(0, dispositions["register"])
        self.assertTrue(
            all(
                row["operation"] == "keep"
                and row["new_value"] is None
                and row["decision_trace"] == []
                and row["blocks_cutover"] is True
                for row in rows
            )
        )

    def test_q17_and_q18_blocked_domains_do_not_overlap(self):
        rows = load_tsv(BLOCKED)
        qids = Counter(row["qid"] for row in rows)

        self.assertEqual({"Q17": 4, "Q18": 752}, dict(qids))
        self.assertEqual(
            {
                "SOURCE_ROLE_NOT_APPROVED",
                "SOURCE_MATCH_BASIS_MISSING",
                "SOURCE_DECISION_MISSING",
            },
            {
                code
                for row in rows
                for code in row["阻断代码"].split(";")
            },
        )
        self.assertTrue(
            all(
                row["处置"] == "blocked_unread_material"
                and row["阻断切换"] == "true"
                for row in rows
            )
        )

    def test_old_relations_remain_audit_only(self):
        audit_rows = load_tsv(BLOCKED)
        old_relations = Counter(row["当前 rel"] for row in audit_rows)

        self.assertEqual({"exactMatch": 748, "closeMatch": 8}, dict(old_relations))
        self.assertTrue(all(row["new_value"] is None for row in self.ledger()["rows"]))


if __name__ == "__main__":
    unittest.main()
