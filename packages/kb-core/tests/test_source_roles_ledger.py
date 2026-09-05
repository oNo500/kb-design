import pathlib
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[3]
FROZEN_FIXTURE_ROOT = (
    ROOT / "tests" / "fixtures" / "governance-frozen-2026-08-31"
)
ROLE_PROPOSALS = (
    FROZEN_FIXTURE_ROOT
    / "parallel"
    / "roles"
    / "role-proposals.yaml"
)
ROLE_LEDGER = ROOT / "data" / "audit" / "migrations" / "source-v1" / "uses.yaml"
RESULT_FIELDS = (
    "inventory_identity",
    "use_id",
    "entity",
    "old_role",
    "new_role",
    "new_status",
    "decision",
    "operation",
    "disposition",
    "classification",
    "rule_refs",
)


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def result_signature(row):
    return tuple(row[field] for field in RESULT_FIELDS)


class SourceRolesLedgerTests(unittest.TestCase):
    def test_ledger_consumes_all_approved_role_proposals(self):
        proposals = load_yaml(ROLE_PROPOSALS)["proposals"]
        if not ROLE_LEDGER.is_file():
            self.fail("source role ledger has not been written")
        roles = load_yaml(ROLE_LEDGER)["roles"]

        self.assertEqual(47, len(roles))
        self.assertEqual(
            [result_signature(row) for row in proposals],
            [result_signature(row) for row in roles],
        )

        same_name = [row for row in roles if row["old_role"] == row["new_role"]]
        discoveries = [row for row in roles if row["new_role"] == "discovery"]
        self.assertEqual(42, len(same_name))
        self.assertEqual(5, len(discoveries))
        self.assertTrue(
            all(
                row["old_role"] == "candidate"
                and row["new_status"] == "proposed"
                for row in discoveries
            )
        )
        self.assertEqual({"proposed"}, {row["new_status"] for row in roles})
        self.assertTrue(all(row["decision"] is None for row in roles))


if __name__ == "__main__":
    unittest.main()
