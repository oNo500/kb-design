import pathlib
import unittest
from contextlib import ExitStack
from datetime import date

import yaml

import kb_core.source_model as model
from source_governance_helpers import (
    approved_and_unapproved_role_references,
    materialized_current_layout,
    unapproved_external_group_reference,
)


ROOT = pathlib.Path(__file__).resolve().parents[3]
FIXTURES = ROOT / "tests" / "fixtures" / "source-governance"


class CheckSourcesTests(unittest.TestCase):
    def require(self, name):
        value = getattr(model, name, None)
        if value is None:
            self.fail(f"offline source validator is missing: {name}")
        return value

    def issues(self, name, previous=None, allow_legacy=False):
        with ExitStack() as stack:
            current = stack.enter_context(materialized_current_layout(FIXTURES / name))
            old = (
                stack.enter_context(materialized_current_layout(FIXTURES / previous))
                if previous
                else None
            )
            return self.require("validate_repository")(current, old, allow_legacy)

    def reference_issues(self, references):
        with materialized_current_layout(FIXTURES / "reference-contract") as root:
            return self.require("validate_references")(root, references)

    def test_valid_repository_has_no_issues(self):
        self.assertEqual([], self.issues("valid"))

    def test_stable_id_change_is_rejected(self):
        self.assertIn("SOURCE_STABLE_ID_CHANGED",
                      {issue.code for issue in self.issues("current", "previous")})

    def test_history_deletion_and_reordering_are_rejected(self):
        self.assertIn("SOURCE_HISTORY_NOT_APPEND_ONLY",
                      {issue.code for issue in self.issues("current", "previous")})

    def test_role_decision_and_registry_role_are_checked(self):
        codes = {issue.code for issue in self.issues("current")}
        self.assertTrue({"SOURCE_ROLE_DECISION_MISSING", "SOURCE_ROLE_NOT_APPROVED"} <= codes)

    def test_mutable_basis_requires_checked(self):
        self.assertIn("SOURCE_BASIS_CHECKED_MISSING",
                      {issue.code for issue in self.issues("current")})

    def test_temporary_failure_cannot_withdraw_entity(self):
        self.assertIn("SOURCE_SCHEMA_INVALID",
                      {issue.code for issue in self.issues("current")})

    def test_resolved_obligation_retrigger_gets_new_id(self):
        self.assertIn("SOURCE_OBLIGATION_REOPENED",
                      {issue.code for issue in self.issues("current", "previous")})

    def test_strict_mode_rejects_legacy_fields(self):
        self.assertIn("SOURCE_LEGACY_FIELD",
                      {issue.code for issue in self.issues("current")})

    def test_basis_reference_needs_existing_entity(self):
        reference = model.ReferenceUse(
            "basis", "data/vocab/terms.yaml", "concept:tc-1",
            "definitions[0].basis[0]",
            {"entity": "missing", "locator": "§ 1"},
        )
        issues = self.reference_issues([reference])
        self.assertTrue(issues, "missing source entity must produce an issue")
        self.assertEqual("SOURCE_ENTITY_MISSING", issues[0].code)

    def test_source_and_match_consume_distinct_approved_roles(self):
        issues = self.reference_issues(approved_and_unapproved_role_references())
        self.assertEqual(["SOURCE_ROLE_NOT_APPROVED"], [issue.code for issue in issues])

    def test_external_group_requires_approved_structure_role(self):
        issues = self.reference_issues([unapproved_external_group_reference()])
        self.assertEqual(["SOURCE_EXTERNAL_GROUP_ROLE_NOT_APPROVED"],
                         [issue.code for issue in issues])

    def test_next_due_uses_calendar_months(self):
        compute = self.require("compute_next_due")
        self.assertEqual(date(2028, 2, 29), compute(date(2026, 2, 28), 24))
        self.assertEqual(date(2027, 8, 31), compute(date(2026, 8, 31), 12))
        self.assertEqual(date(2027, 2, 28), compute(date(2026, 8, 31), 6))

    def test_archival_review_has_no_content_due_date(self):
        self.assertIsNone(self.require("compute_next_due")(date(2026, 8, 31), None))

    def test_review_grace_boundary_is_exact(self):
        overdue = self.require("is_review_overdue")
        self.assertFalse(overdue(date(2026, 8, 31), date(2026, 9, 30)))
        self.assertTrue(overdue(date(2026, 8, 31), date(2026, 10, 1)))

    def test_replacement_decision_patches_are_returned_verbatim(self):
        patches = self.require("load_decision_patches")([
            FIXTURES / "reference-contract" / "replacement-decision.md"
        ])
        expected = [model.DecisionPatch(**row) for row in yaml.safe_load(
            (FIXTURES / "reference-contract" / "replacement-patches.yaml").read_text(
                encoding="utf-8"
            )
        )]
        self.assertEqual(expected, list(patches))


if __name__ == "__main__":
    unittest.main()
