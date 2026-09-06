import pathlib
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[3]
LEDGER = ROOT / "data" / "audit" / "migrations" / "source-v1" / "origin.yaml"

EXPECTED_IDENTITIES = {
    "concepts/classifying-new-subjects.md:47",
    "design/content-model.md:138",
    "design/drafts/terminology-governance.md:270",
    "design/entities.md:78",
    "design/entities.md:100",
    "design/maintenance.md:132",
    "design/principles.md:20",
    "design/topics.md:114",
    "design/topics.md:127",
    "design/topics.md:132",
    "design/topics.md:136",
    "design/topics.md:138",
    "design/topics.md:190",
    "design/topics.md:213",
    "docs/superpowers/specs/2026-08-27-terminology-governance-design.md:170",
    "docs/superpowers/specs/2026-08-27-terminology-governance-design.md:178",
    "vocab/topics.yaml:1-6825（全文件）",
    "scripts/build-topics.py:132-156",
    "scripts/check-topics.py:34-58",
}

EXPECTED_FORMAL_DOCUMENTS = {
    "concepts/classifying-new-subjects.md",
    "design/content-model.md",
    "design/entities.md",
    "design/maintenance.md",
    "design/principles.md",
    "design/topics.md",
}


def load_ledger():
    assert LEDGER.is_file(), f"missing origin ledger: {LEDGER}"
    return yaml.safe_load(LEDGER.read_text(encoding="utf-8"))


class SourceDocsTests(unittest.TestCase):
    def test_origin_ledger_closes_exactly_the_frozen_identities(self):
        ledger = load_ledger()
        rows = ledger["rows"]
        identities = [row["identity"] for row in rows]

        self.assertEqual(19, len(rows))
        self.assertEqual(19, len(set(identities)))
        self.assertEqual(EXPECTED_IDENTITIES, set(identities))
        self.assertTrue(all(row["closure_status"] == "closed" for row in rows))

    def test_document_dispositions_cover_every_identity_once(self):
        ledger = load_ledger()
        dispositions = ledger["document_dispositions"]
        covered = [
            identity
            for disposition in dispositions
            for identity in disposition["origin_identities"]
        ]

        self.assertEqual(14, len(dispositions))
        self.assertEqual(19, len(covered))
        self.assertEqual(19, len(set(covered)))
        self.assertEqual(EXPECTED_IDENTITIES, set(covered))
        self.assertTrue(
            all(disposition["closure_status"] == "closed" for disposition in dispositions)
        )

    def test_document_dispositions_preserve_the_formal_write_boundary(self):
        ledger = load_ledger()
        dispositions = ledger["document_dispositions"]
        formal = [row for row in dispositions if row["future_formal_write"]]

        self.assertFalse(ledger["formal_write"])
        self.assertEqual([], ledger["formal_document_write_set"])
        self.assertEqual(9, len(formal))
        self.assertEqual(EXPECTED_FORMAL_DOCUMENTS, {row["file"] for row in formal})

    def test_frozen_debt_stays_outside_the_document_write_set(self):
        debt = load_ledger()["frozen_debt"]

        self.assertEqual(31, debt["title_debt"]["identities"])
        self.assertEqual(8, debt["title_debt"]["files"])
        self.assertEqual(8, debt["append_only_titles"]["identities"])
        self.assertEqual("vocab/CHANGELOG.md", debt["append_only_titles"]["file"])
        self.assertEqual(2, debt["legacy_sdd_links"]["identities"])
        self.assertTrue(all(not item["write_set"] for item in debt.values()))


if __name__ == "__main__":
    unittest.main()
