import hashlib
import json
import pathlib
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[3]
FROZEN_FIXTURE_ROOT = (
    ROOT / "tests" / "fixtures" / "governance-frozen-2026-08-31"
)
PARALLEL = FROZEN_FIXTURE_ROOT / "parallel" / "entities"
PREVIEW = FROZEN_FIXTURE_ROOT / "plan" / "entities.yaml"
LEDGER = ROOT / "data" / "audit" / "migrations" / "source-v1" / "entities.yaml"
EXISTING = PARALLEL / "existing-proposals.yaml"
UNREGISTERED = PARALLEL / "unregistered-proposals.yaml"
SCHEMA = ROOT / "schemas" / "source-migration.schema.json"

INPUT_HASHES = {
    EXISTING: "c9954fc215c2432ae103182a2636e700d004c634f09d9f4c7507ff6b0821bc56",
    UNREGISTERED: "74314bfb21f759407abb8deec70d7964d5ffabc50d6f8627a847c5552a9998e8",
    PREVIEW: "b6ea58589040e6f8c1ef43842bfd3bee9f408b850b6951a73c891a9a3e17cb12",
}

AMBIGUOUS_IDENTITIES = {
    "source-entities.tsv:41",
    "source-entities.tsv:77",
    "source-entities.tsv:78",
    "source-entities.tsv:79",
    "source-entities.tsv:80",
    "source-entities.tsv:81",
    "source-entities.tsv:82",
    "source-entities.tsv:83",
    "source-entities.tsv:85",
    "source-entities.tsv:99",
    "source-entities.tsv:100",
    "source-entities.tsv:102",
    "source-entities.tsv:110",
    "source-entities.tsv:114",
    "source-entities.tsv:128",
    "source-entities.tsv:139",
}


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def formal_row(identity, disposition):
    return {
        "identity": identity,
        "operation": "keep",
        "disposition": disposition,
        "new_value": None,
        "decision_trace": [],
        "blocks_cutover": True,
    }


class SourceEntitiesLedgerTests(unittest.TestCase):
    def ledger(self):
        self.assertTrue(LEDGER.is_file(), f"missing entities ledger: {LEDGER}")
        return load_yaml(LEDGER)

    def proposals(self):
        return (
            load_yaml(EXISTING)["proposals"],
            load_yaml(UNREGISTERED)["proposals"],
        )

    def test_ledger_consumes_frozen_proposals_and_real_preview(self):
        self.assertEqual(
            {str(path): expected for path, expected in INPUT_HASHES.items()},
            {str(path): sha256(path) for path in INPUT_HASHES},
        )
        existing, unregistered = self.proposals()
        expected_rows = [
            *(formal_row(row["identity"], "unresolved_external_status")
              for row in existing),
            *(formal_row(row["identity"], "retain_legacy")
              for row in unregistered),
        ]
        preview_identities = [row["identity"] for row in load_yaml(PREVIEW)["rows"]]

        self.assertEqual(preview_identities, [row["identity"] for row in expected_rows])
        self.assertEqual(
            {
                "schema": "urn:kb-design:data:source-migration",
                "schema_version": 1,
                "rows": expected_rows,
            },
            self.ledger(),
        )

    def test_all_138_inventory_identities_close_once_in_frozen_order(self):
        rows = self.ledger()["rows"]
        identities = [row["identity"] for row in rows]

        self.assertEqual(138, len(rows))
        self.assertEqual(138, len(set(identities)))
        self.assertEqual(
            [f"source-entities.tsv:{line}" for line in range(2, 140)],
            identities,
        )

    def test_31_existing_ids_stay_frozen_with_external_status_unresolved(self):
        existing, _ = self.proposals()
        rows = {row["identity"]: row for row in self.ledger()["rows"]}

        self.assertEqual(31, len(existing))
        self.assertTrue(all(row["old_id"] == row["proposed_id"] for row in existing))
        self.assertTrue(
            all(
                row["conclusion"]["external_status"] == "unresolved"
                and row["conclusion"]["replaced_by"] == "unresolved"
                for row in existing
            )
        )
        self.assertTrue(
            all(
                rows[row["identity"]]
                == formal_row(row["identity"], "unresolved_external_status")
                for row in existing
            )
        )

    def test_107_unregistered_identities_receive_no_new_id(self):
        _, unregistered = self.proposals()
        rows = {row["identity"]: row for row in self.ledger()["rows"]}

        self.assertEqual(107, len(unregistered))
        self.assertTrue(
            all(
                row["conclusion"]["disposition"] == "unresolved"
                and row["conclusion"]["proposed_id"] is None
                for row in unregistered
            )
        )
        self.assertTrue(
            all(
                rows[row["identity"]]
                == formal_row(row["identity"], "retain_legacy")
                for row in unregistered
            )
        )

    def test_16_identity_ambiguities_remain_explicit_and_blocked(self):
        _, unregistered = self.proposals()
        actual = {
            row["identity"] for row in unregistered if row["identity_ambiguous"]
        }
        ledger_rows = {row["identity"]: row for row in self.ledger()["rows"]}

        self.assertEqual(AMBIGUOUS_IDENTITIES, actual)
        self.assertTrue(
            all(
                ledger_rows[identity]["disposition"] == "retain_legacy"
                and ledger_rows[identity]["blocks_cutover"] is True
                for identity in AMBIGUOUS_IDENTITIES
            )
        )

    def test_ledger_uses_the_exact_source_migration_row_interface(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        ledger = self.ledger()
        row_schema = schema["$defs"]["row"]
        allowed_dispositions = set(row_schema["properties"]["disposition"]["enum"])

        self.assertEqual(set(schema["required"]), set(ledger))
        self.assertEqual(set(row_schema["required"]), set(row_schema["properties"]))
        self.assertTrue(
            all(set(row) == set(row_schema["required"]) for row in ledger["rows"])
        )
        self.assertTrue(
            all(row["disposition"] in allowed_dispositions for row in ledger["rows"])
        )


if __name__ == "__main__":
    unittest.main()
