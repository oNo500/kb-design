import copy
import pathlib
import unittest

import yaml

from kb_core.source_model import (
    open_obligation,
    resolve_obligation,
    retrigger_obligation,
    source_obligation_term_trigger,
)


ROOT = pathlib.Path(__file__).resolve().parents[3]
FIXTURE = (
    ROOT
    / "tests"
    / "fixtures"
    / "source-governance"
    / "obligations"
    / "lifecycle.yaml"
)


class SourceObligationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))

    def open_document(self):
        return open_obligation(
            self.case["document"],
            self.case["entity"],
            self.case["trigger"],
            self.case["targets"],
            self.case["opening_decisions"],
            self.case["opened"],
            self.case["obligation_id"],
        )

    def resolved_document(self):
        return resolve_obligation(
            self.open_document(),
            self.case["obligation_id"],
            self.case["resolved"],
            self.case["conclusions"],
            self.case["resolution_decisions"],
        )

    def test_open_resolve_retrigger_preserves_prior_documents_and_history(self):
        empty = copy.deepcopy(self.case["document"])
        opened = self.open_document()
        self.assertEqual(empty, self.case["document"])
        self.assertEqual(
            ("open", self.case["opened"], None, "opened"),
            (
                opened["obligations"][0]["state"],
                opened["obligations"][0]["opened"],
                opened["obligations"][0]["resolved"],
                opened["obligations"][0]["history"][0]["action"],
            ),
        )

        frozen_opened = copy.deepcopy(opened)
        resolved = resolve_obligation(
            opened,
            self.case["obligation_id"],
            self.case["resolved"],
            self.case["conclusions"],
            self.case["resolution_decisions"],
        )
        self.assertEqual(frozen_opened, opened)
        self.assertEqual("resolved", resolved["obligations"][0]["state"])
        self.assertEqual(self.case["conclusions"],
                         resolved["obligations"][0]["history"][-1]["conclusions"])
        self.assertNotIn("conclusions", resolved["obligations"][0])

        frozen_resolved = copy.deepcopy(resolved)
        retriggered = retrigger_obligation(
            resolved,
            self.case["obligation_id"],
            self.case["targets"],
            [],
            self.case["retriggered"],
            self.case["retriggered_id"],
        )
        self.assertEqual(frozen_resolved, resolved)
        self.assertEqual(frozen_resolved["obligations"][0],
                         retriggered["obligations"][0])
        self.assertEqual(
            (self.case["retriggered_id"], "open", self.case["obligation_id"]),
            tuple(retriggered["obligations"][-1][key]
                  for key in ("id", "state", "previous")),
        )

    def test_resolution_requires_a_conclusion_for_every_target(self):
        incomplete = copy.deepcopy(self.case["conclusions"])
        incomplete.pop(self.case["second_target_key"])
        with self.assertRaisesRegex(ValueError, "target conclusions"):
            resolve_obligation(
                self.open_document(),
                self.case["obligation_id"],
                self.case["resolved"],
                incomplete,
                self.case["resolution_decisions"],
            )

    def test_resolution_requires_decisions_named_by_target_conclusions(self):
        with self.assertRaisesRegex(ValueError, "required decisions"):
            resolve_obligation(
                self.open_document(),
                self.case["obligation_id"],
                self.case["resolved"],
                self.case["conclusions"],
                [],
            )

    def test_resolved_obligation_cannot_be_reused_or_resolved_again(self):
        resolved = self.resolved_document()
        with self.assertRaisesRegex(ValueError, "already exists"):
            open_obligation(
                resolved,
                self.case["entity"],
                self.case["trigger"],
                self.case["targets"],
                [],
                self.case["retriggered"],
                self.case["obligation_id"],
            )
        with self.assertRaisesRegex(ValueError, "not open"):
            resolve_obligation(
                resolved,
                self.case["obligation_id"],
                self.case["retriggered"],
                self.case["conclusions"],
                self.case["resolution_decisions"],
            )

    def test_source_to_term_bridge_contains_only_obligation_id(self):
        self.assertEqual(
            {"kind": "source_obligation", "id": self.case["obligation_id"]},
            source_obligation_term_trigger(self.case["obligation_id"]),
        )


if __name__ == "__main__":
    unittest.main()
