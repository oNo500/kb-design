import hashlib
import json
import pathlib
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[3]
FROZEN_FIXTURE_ROOT = (
    ROOT / "tests" / "fixtures" / "governance-frozen-2026-08-31"
)
PARALLEL = (
    FROZEN_FIXTURE_ROOT
    / "parallel"
    / "source"
    / "source-proposals.yaml"
)
LEDGER = ROOT / "data" / "audit" / "migrations" / "source-v1" / "source.yaml"
SCHEMA = ROOT / "schemas" / "source-migration.schema.json"
PROPOSALS_SHA256 = (
    "145a5f377359f3c9979e17f3ef53fc2355171a097b1eb773a7aa0cd2c22e22ab"
)


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class SourceDerivationLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proposals = load_yaml(PARALLEL)
        cls.ledger = load_yaml(LEDGER)
        cls.proposal_rows = {
            row["identity"]: row for row in cls.proposals["rows"]
        }
        cls.ledger_rows = {
            row["identity"]: row for row in cls.ledger["rows"]
        }

    def test_ledger_closes_each_proposal_identity_once(self):
        self.assertEqual(PROPOSALS_SHA256, sha256(PARALLEL))
        self.assertEqual(726, len(self.proposals["rows"]))
        self.assertEqual(726, len(self.ledger["rows"]))
        self.assertEqual(726, len(self.proposal_rows))
        self.assertEqual(726, len(self.ledger_rows))
        self.assertEqual(
            [row["identity"] for row in self.proposals["rows"]],
            [row["identity"] for row in self.ledger["rows"]],
        )

    def test_four_partitions_keep_their_category_dispositions(self):
        expected = {
            ("derivation", "retain_legacy"): 692,
            ("array_label", "retain_legacy"): 17,
            ("array_label", "not_migrated_missing_locator"): 7,
            ("project_assertion", "project_assertion"): 8,
            ("local_analysis", "isolated_local_analysis"): 2,
        }
        actual = {}
        for identity, proposal in self.proposal_rows.items():
            key = (proposal["partition"], self.ledger_rows[identity]["disposition"])
            actual[key] = actual.get(key, 0) + 1
        self.assertEqual(expected, actual)

    def test_only_seven_manual_rows_are_locator_exceptions(self):
        routes = {}
        for row in self.proposals["rows"]:
            routes[row["review_route"]] = routes.get(row["review_route"], 0) + 1
        self.assertEqual({"batch": 719, "manual": 7}, routes)
        expected = {
            row["identity"]
            for row in self.proposals["rows"]
            if row["review_route"] == "manual"
        }
        actual = {
            row["identity"]
            for row in self.ledger["rows"]
            if row["disposition"] == "not_migrated_missing_locator"
        }
        self.assertEqual(7, len(expected))
        self.assertEqual(expected, actual)

    def test_category_processing_does_not_upgrade_legacy_source(self):
        for identity, row in self.ledger_rows.items():
            with self.subTest(identity=identity):
                self.assertEqual("keep", row["operation"])
                self.assertEqual(
                    self.proposal_rows[identity]["old_value"], row["new_value"]
                )
                self.assertEqual([], row["decision_trace"])
                self.assertTrue(row["blocks_cutover"])

    def test_ledger_satisfies_the_existing_migration_schema(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        row_schema = schema["$defs"]["row"]
        allowed_dispositions = set(
            row_schema["properties"]["disposition"]["enum"]
        )

        self.assertEqual(set(schema["required"]), set(self.ledger))
        self.assertEqual("urn:kb-design:data:source-migration", self.ledger["schema"])
        self.assertEqual(1, self.ledger["schema_version"])
        self.assertTrue(
            all(
                set(row) == set(row_schema["required"])
                and row["disposition"] in allowed_dispositions
                for row in self.ledger["rows"]
            )
        )


if __name__ == "__main__":
    unittest.main()
