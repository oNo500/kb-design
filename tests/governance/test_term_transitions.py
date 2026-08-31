import copy
import unittest
from pathlib import Path

import yaml

from scripts.governance.term_model import parse_terms
from scripts.governance.term_transitions import validate_transition


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "fixtures" / "terminology"
ALPHA = "tm-11111111-1111-4111-8111-111111111111"
BETA = "tm-22222222-2222-4222-8222-222222222222"
GAMMA = "tm-44444444-4444-4444-8444-444444444444"
DECISIONS = frozenset({"decision-term-0002"})


def load_yaml(relative):
    return yaml.safe_load((FIXTURES / relative).read_text(encoding="utf-8"))


def term(value, term_id):
    for concept in value["concepts"]:
        for language in concept["languages"]:
            for row in language["terms"]:
                if row["id"] == term_id:
                    return row
    raise AssertionError(f"missing fixture term {term_id}")


def append_transition(row, before, after, decision="decision-term-0002", linked=None):
    row["history"].append({
        "date": "2026-09-01",
        "event": "status-changed",
        "decision": decision,
        "reason": "Fixture transition.",
        "from_value": before,
        "to_value": after,
        "linked_terms": list(linked or [row["id"]]),
    })


class TermTransitionTests(unittest.TestCase):
    def setUp(self):
        self.before_value = load_yaml("valid/minimal-active.yaml")
        self.before = parse_terms(self.before_value)

    def test_requires_one_preferred_term(self):
        current_value = copy.deepcopy(self.before_value)
        alpha = term(current_value, ALPHA)
        alpha["administrative_status"] = "admittedTerm-admn-sts"
        append_transition(alpha, "preferredTerm-admn-sts", "admittedTerm-admn-sts")

        issues = validate_transition(
            self.before, parse_terms(current_value), DECISIONS,
        )

        self.assertIn("TERM_PREFERRED_COUNT", {issue.code for issue in issues})

    def test_preferred_demotion_is_atomic(self):
        current_value = copy.deepcopy(self.before_value)
        alpha = term(current_value, ALPHA)
        alpha["administrative_status"] = "admittedTerm-admn-sts"
        append_transition(alpha, "preferredTerm-admn-sts", "admittedTerm-admn-sts")

        issues = validate_transition(
            self.before, parse_terms(current_value), DECISIONS,
        )

        self.assertEqual(
            {"TERM_PREFERRED_COUNT", "TERM_ATOMIC_LANGUAGE_CHANGE"},
            {issue.code for issue in issues},
        )

    def test_replacement_stays_in_language(self):
        current_value = load_yaml("invalid/status-and-replacement.yaml")
        previous_value = copy.deepcopy(current_value)
        beta = term(previous_value, BETA)
        beta["administrative_status"] = "admittedTerm-admn-sts"
        beta.pop("replaced_by")
        beta["history"].pop()

        issues = validate_transition(
            parse_terms(previous_value), parse_terms(current_value), DECISIONS,
        )

        self.assertEqual(
            ["TERM_REPLACEMENT_LANGUAGE"],
            [issue.code for issue in issues],
        )

    def test_replacement_cycle_fails(self):
        current_value = copy.deepcopy(self.before_value)
        beta = term(current_value, BETA)
        beta["administrative_status"] = "supersededTerm-admn-sts"
        beta["replaced_by"] = GAMMA
        append_transition(beta, "admittedTerm-admn-sts", "supersededTerm-admn-sts")
        gamma = copy.deepcopy(beta)
        gamma["id"] = GAMMA
        gamma["text"] = "Gamma"
        gamma["replaced_by"] = BETA
        gamma["history"] = [{
            "date": "2026-09-01",
            "event": "migrated",
            "decision": "decision-term-0002",
            "reason": "Fixture migration.",
            "from_value": None,
            "to_value": "supersededTerm-admn-sts",
            "linked_terms": [GAMMA, BETA],
        }]
        current_value["concepts"][0]["languages"][0]["terms"].append(gamma)

        issues = validate_transition(
            self.before, parse_terms(current_value), DECISIONS,
        )

        self.assertIn("TERM_REPLACEMENT_CYCLE", {issue.code for issue in issues})

    def test_restoration_rechecks_admission(self):
        previous_value = copy.deepcopy(self.before_value)
        previous_beta = term(previous_value, BETA)
        previous_beta["administrative_status"] = "deprecatedTerm-admn-sts"
        previous_beta["history"][0]["to_value"] = "deprecatedTerm-admn-sts"
        current_value = copy.deepcopy(previous_value)
        current_beta = term(current_value, BETA)
        current_beta["administrative_status"] = "admittedTerm-admn-sts"
        append_transition(
            current_beta,
            "deprecatedTerm-admn-sts",
            "admittedTerm-admn-sts",
            decision="decision-term-0001",
        )

        issues = validate_transition(
            parse_terms(previous_value),
            parse_terms(current_value),
            frozenset({"decision-term-0001"}),
        )

        self.assertIn("TERM_RESTORATION_REVIEW", {issue.code for issue in issues})

    def test_history_is_append_only(self):
        current_value = copy.deepcopy(self.before_value)
        term(current_value, ALPHA)["history"][0]["reason"] = "Rewritten history."

        issues = validate_transition(
            self.before, parse_terms(current_value), DECISIONS,
        )

        self.assertEqual(
            ["TERM_HISTORY_NOT_APPEND_ONLY"],
            [issue.code for issue in issues],
        )

    def test_transition_decisions_resolve(self):
        current_value = copy.deepcopy(self.before_value)
        beta = term(current_value, BETA)
        beta["administrative_status"] = "deprecatedTerm-admn-sts"
        append_transition(
            beta,
            "admittedTerm-admn-sts",
            "deprecatedTerm-admn-sts",
            decision="decision-term-missing",
        )

        issues = validate_transition(
            self.before, parse_terms(current_value), DECISIONS,
        )

        self.assertIn("TERM_DECISION_MISSING", {issue.code for issue in issues})


if __name__ == "__main__":
    unittest.main()
