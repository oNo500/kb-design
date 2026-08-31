import json
import unittest
from dataclasses import asdict
from pathlib import Path

import yaml

from scripts.governance.term_maintenance import (
    build_term_reference_index,
    open_term_obligation,
    validate_obligation_transition,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests/fixtures/terminology/maintenance"


def load_yaml(name):
    return yaml.safe_load((FIXTURES / name).read_text(encoding="utf-8"))


def issue_codes(issues):
    return {issue.code for issue in issues}


class TermMaintenanceTests(unittest.TestCase):
    def test_source_obligation_bridge_uses_id_only(self):
        value = load_yaml("source-obligation-bridge.yaml")
        obligation = open_term_obligation(
            value["trigger"]["kind"],
            value["trigger"]["id"],
            tuple(value["targets"]),
            value["opened"],
            value["decision"],
        )

        self.assertEqual("source-review-20260831-001", obligation.trigger.id)
        self.assertEqual(
            {"kind", "id", "previous_obligation"},
            set(asdict(obligation.trigger)),
        )
        self.assertNotIn("source_state", json.dumps(asdict(obligation)))

    def test_term_index_is_bidirectional(self):
        value = load_yaml("index-input.yaml")
        first = build_term_reference_index(
            value["document"], value["obligations"], value["decisions"]
        )
        second = build_term_reference_index(
            value["document"], value["obligations"], value["decisions"]
        )
        entries = {
            (
                row["target_kind"], row["target_id"], row["reference_kind"],
                row["record"], row["field_path"], row["state"],
            )
            for row in first["entries"]
        }

        self.assertIn(
            (
                "concept", "tc-00000000-0000-4000-8000-000000000001",
                "term.concept", "term:tm-00000000-0000-4000-8000-000000000001",
                "concept", "preferredTerm-admn-sts",
            ),
            entries,
        )
        self.assertIn(
            (
                "term", "tm-00000000-0000-4000-8000-000000000001",
                "concept.term", "concept:tc-00000000-0000-4000-8000-000000000001",
                "languages[0].terms[0]", "active",
            ),
            entries,
        )
        self.assertEqual(
            json.dumps(first, ensure_ascii=False, sort_keys=True),
            json.dumps(second, ensure_ascii=False, sort_keys=True),
        )

    def test_decision_change_opens_new_obligation(self):
        value = load_yaml("decision-change.yaml")
        accepted = frozenset(value["accepted_decisions"])

        self.assertEqual(
            [],
            validate_obligation_transition(
                value["previous"], value["replacement"], accepted
            ),
        )
        self.assertIn(
            "TERM_OBLIGATION_REPLACEMENT_REQUIRED",
            issue_codes(validate_obligation_transition(
                value["previous"], value["same_id_rewrite"], accepted
            )),
        )

    def test_resolved_obligation_never_reopens(self):
        value = load_yaml("resolved-reopened.yaml")

        self.assertIn(
            "TERM_OBLIGATION_REOPENED",
            issue_codes(validate_obligation_transition(
                value["previous"], value["current"],
                frozenset(value["accepted_decisions"]),
            )),
        )

    def test_obligation_history_is_append_only(self):
        value = load_yaml("history-rewrite.yaml")

        self.assertIn(
            "TERM_OBLIGATION_HISTORY_NOT_APPEND_ONLY",
            issue_codes(validate_obligation_transition(
                value["previous"], value["current"],
                frozenset(value["accepted_decisions"]),
            )),
        )

    def test_no_periodic_threshold_is_inherited(self):
        value = load_yaml("periodic-policy.yaml")

        self.assertIn(
            "TERM_PERIODIC_POLICY_NOT_APPROVED",
            issue_codes(validate_obligation_transition(
                value["previous"], value["current"], frozenset()
            )),
        )


if __name__ == "__main__":
    unittest.main()
