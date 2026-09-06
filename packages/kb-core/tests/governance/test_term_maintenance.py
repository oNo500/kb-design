import json
import unittest
from dataclasses import asdict
from pathlib import Path

import yaml

from kb_core.governance.term_maintenance import (
    build_term_reference_index,
    open_term_obligation,
    validate_obligation_transition,
)


ROOT = Path(__file__).resolve().parents[4]
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


class CurrentTermReferenceTests(unittest.TestCase):
    def test_current_project_approvals_are_locatable_without_audit_leakage(self):
        document = {'concepts': [{'id': 'tc-fixture', 'workflow': 'active',
            'basis': {'project': {'approval': 'concept-grant'}},
            'definitions': [{'basis': {'project': {'approval': 'definition-grant'}}}],
            'languages': [{'terms': [{'id': 'tm-fixture', 'administrative_status': 'preferredTerm-admn-sts',
                'basis': {'project': {'approval': 'term-grant'}},
                'history': [{'from_value': {'basis': {'project': {'approval': 'audit-only'}}}}]}]}]}]}
        rows = build_term_reference_index(document, {'obligations': []}, {})['entries']
        decisions = {(row['target_id'], row['record'], row['field_path']) for row in rows
                     if row['target_kind'] == 'decision'}
        self.assertEqual({('concept-grant', 'concept:tc-fixture', 'basis.project.approval'),
                          ('definition-grant', 'concept:tc-fixture', 'definitions[0].basis.project.approval'),
                          ('term-grant', 'term:tm-fixture', 'basis.project.approval')}, decisions)

    def test_layout_concept_targets_are_locatable_but_original_cells_are_not_current(self):
        identity = 'tc-00000000-0000-4000-8000-000000000001'
        layout = {'groups': [], 'symbol_mappings': [{'origin_id': 'symbols', 'concept_ids': [identity]}],
                  'historical_designations': [{'origin_id': 'old-name', 'target_concept_ids': [identity]}],
                  'reference_entries': [{'id': 'explanation', 'cells': [f'[entry](#{identity})'],
                                         'original_cells': ['tc-00000000-0000-4000-8000-000000000002']}]}
        rows = build_term_reference_index({'concepts': []}, {'obligations': []}, {}, layout=layout)['entries']
        targets = {(row['target_id'], row['field_path']) for row in rows if row['target_kind'] == 'concept'}
        self.assertEqual({(identity, 'symbol_mappings[0].concept_ids[0]'),
                          (identity, 'historical_designations[0].target_concept_ids[0]'),
                          (identity, 'reference_entries[0].cells[0]')}, targets)

    def test_decision_declarations_expose_permission_targets_without_audit_targets(self):
        identity = 'tc-00000000-0000-4000-8000-000000000001'
        other = 'tc-00000000-0000-4000-8000-000000000002'
        document = {'concepts': [{'id': identity, 'workflow': 'active'}, {'id': other, 'workflow': 'active'}]}
        decision = {'answers': [{'patches': [
            {'identity': identity, 'field': 'definition_source_permission', 'value': {'before': {'identity': other}}},
            {'identity': f'terms/concepts/{identity}', 'field': 'record', 'value': {}},
            {'identity': f'terms/concepts/{identity}', 'field': 'project_basis_scope', 'value': {}},
            {'identity': 'tc-unknown', 'field': 'definition_source_permission', 'value': {}},
        ]}]}
        rows = build_term_reference_index(document, {'obligations': []},
            {'permission': 'docs/decisions/term-permission.md'},
            decision_documents={'permission': decision})['entries']
        targets = {(row['target_id'], row['field_path'], row['state']) for row in rows
                   if row['record'] == 'decision:permission' and row['target_kind'] == 'concept'}
        self.assertEqual({(identity, f'answers[0].patches[{index}].identity', 'declared')
                          for index in range(3)}, targets)


if __name__ == "__main__":
    unittest.main()
