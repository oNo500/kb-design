import csv
import hashlib
import json
import pathlib
import unittest
from collections import Counter

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
FROZEN_FIXTURE_ROOT = (
    ROOT / "tests" / "fixtures" / "governance-frozen-2026-08-31"
)
INVENTORY = FROZEN_FIXTURE_ROOT / "basis-inventory.tsv"
LEDGER = ROOT / "vocab" / "migrations" / "source-v1" / "basis.yaml"
PARALLEL_BASIS = FROZEN_FIXTURE_ROOT / "parallel" / "basis"
INVENTORY_SHA256 = (
    "3da438227ee676f0d2c5e31ac16c73a3bb4a5d10716b15f175fd81257642c43c"
)


def load_ledger():
    return yaml.safe_load(LEDGER.read_text(encoding="utf-8"))


def value_sha256(value):
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def inventory_rows():
    with INVENTORY.open(encoding="utf-8", newline="") as stream:
        rows = {}
        for row in csv.DictReader(stream, delimiter="\t"):
            identity = "|".join((row["文件"], row["位置"], row["对象"]))
            raw = row["当前值"].split(";", 1)[0]
            if not raw.startswith("raw="):
                raise AssertionError(identity)
            rows[identity] = {
                "file": row["文件"],
                "position": int(row["位置"]),
                "field_path": row["对象"],
                "old_value": raw.removeprefix("raw="),
            }
        return rows


class SourceBasisLedgerTests(unittest.TestCase):
    def test_ledger_closes_every_frozen_identity_once(self):
        ledger = load_ledger()
        rows = ledger["rows"]
        identities = [row["identity"] for row in rows]

        self.assertEqual(INVENTORY_SHA256, ledger["input"]["inventory_sha256"])
        self.assertEqual(1501, len(rows))
        self.assertEqual(1501, len(set(identities)))
        self.assertEqual(set(inventory_rows()), set(identities))
        self.assertEqual(
            {
                "rows": 1501,
                "mechanical": 643,
                "exceptions": 858,
                "no_external_basis": 630,
                "project_assertion": 13,
                "formal_basis": 0,
            },
            ledger["counts"],
        )
        self.assertEqual(
            {"formal": 1496, "generator": 1, "documentation": 4},
            ledger["partitions"],
        )

    def test_ledger_consumes_each_frozen_parallel_basis_result(self):
        ledger = load_ledger()
        rows = {row["identity"]: row for row in ledger["rows"]}
        proposal_path = PARALLEL_BASIS / "basis-proposals.yaml"
        exception_path = PARALLEL_BASIS / "exceptions.tsv"

        self.assertEqual(
            hashlib.sha256(proposal_path.read_bytes()).hexdigest(),
            ledger["input"]["mechanical_proposals_sha256"],
        )
        self.assertEqual(
            hashlib.sha256(exception_path.read_bytes()).hexdigest(),
            ledger["input"]["exceptions_sha256"],
        )

        proposals = yaml.safe_load(proposal_path.read_text(encoding="utf-8"))[
            "proposals"
        ]
        for source in proposals:
            final = rows[source["identity"]]
            self.assertEqual("mechanical", final["class"])
            self.assertEqual(
                {
                    key: source[key]
                    for key in (
                        "operation",
                        "disposition",
                        "new_basis",
                        "decision_trace",
                        "blocks_cutover",
                    )
                },
                {
                    key: final[key]
                    for key in (
                        "operation",
                        "disposition",
                        "new_basis",
                        "decision_trace",
                        "blocks_cutover",
                    )
                },
            )

        with exception_path.open(encoding="utf-8", newline="") as stream:
            exceptions = list(csv.DictReader(stream, delimiter="\t"))
        for source in exceptions:
            final = rows[source["身份"]]
            self.assertEqual("exception", final["class"])
            self.assertEqual(source["拟议处置"], final["disposition"])
            self.assertEqual(source["阻断切换"] == "true", final["blocks_cutover"])

    def test_mechanical_rows_only_remove_none_and_self_markers(self):
        rows = [row for row in load_ledger()["rows"] if row["class"] == "mechanical"]

        self.assertEqual(
            Counter(
                {
                    ("none", "no_external_basis"): 630,
                    ("self", "project_assertion"): 13,
                }
            ),
            Counter((row["old_value"], row["disposition"]) for row in rows),
        )
        self.assertTrue(all(row["scope"] == "formal" for row in rows))
        self.assertTrue(all(row["operation"] == "delete" for row in rows))
        self.assertTrue(all(row["new_basis"] is None for row in rows))
        self.assertTrue(all(not row["blocks_cutover"] for row in rows))
        self.assertTrue(
            all(
                row["decision_trace"]
                == [
                    {
                        "decision": "decision-source-0011",
                        "question": "Q20",
                        "field": "unsupported_basis_policy",
                    }
                ]
                for row in rows
            )
        )

    def test_exceptions_do_not_create_formal_basis(self):
        ledger = load_ledger()
        rows = [row for row in ledger["rows"] if row["class"] == "exception"]

        self.assertEqual(858, len(rows))
        self.assertEqual(
            Counter(
                {
                    "blocked_unread_material": 830,
                    "not_migrated_missing_locator": 23,
                    "retain_legacy": 1,
                    "not_in_scope": 4,
                }
            ),
            Counter(row["disposition"] for row in rows),
        )
        self.assertEqual(853, sum(row["scope"] == "formal" for row in rows))
        self.assertEqual(0, ledger["counts"]["formal_basis"])
        self.assertFalse(any(row["disposition"] == "register" for row in rows))
        self.assertTrue(all(row["new_basis"] is None for row in rows))

    def test_old_values_and_hashes_match_frozen_inputs(self):
        expected = inventory_rows()
        rows = load_ledger()["rows"]
        file_hashes = {
            relative: hashlib.sha256(
                (FROZEN_FIXTURE_ROOT / relative).read_bytes()
            ).hexdigest()
            for relative in {row["file"] for row in rows}
        }

        for row in rows:
            frozen = expected[row["identity"]]
            self.assertEqual(frozen, {key: row[key] for key in frozen})
            self.assertEqual(value_sha256(frozen["old_value"]), row["old_value_sha256"])
            self.assertEqual(file_hashes[row["file"]], row["old_file_sha256"])


if __name__ == "__main__":
    unittest.main()
