import copy
import json
import unittest
from pathlib import Path

import yaml

from kb_core.governance.term_validation import (
    historical_decisions_from_documents,
    semantic_concept,
    semantic_project_basis_scope,
    semantic_term,
    validate_term_snapshot,
)
from kb_core.source_model import accepted_decisions_from_documents
from source_governance_helpers import current_reference_value


ROOT = Path(__file__).resolve().parents[4]
FIXTURE = ROOT / "tests/fixtures/terminology/valid/minimal-active.yaml"
CANDIDATE = current_reference_value(json.loads(
    (ROOT / "work/reviews/2026-09-06-term-complete-candidate.json").read_text()
))


def decision(decision_id, patches, *, status="accepted", level="L3", supersedes=None):
    return {
        "id": decision_id,
        "schema": "urn:kb-design:data:decision",
        "schema_version": 1,
        "status": status,
        "date": "2026-09-06",
        "level": level,
        "scope": "term fixture",
        "supersedes": list(supersedes or []),
        "answers": [{"question": "Q01", "resolution": "recommended", "patches": patches}],
    }


class TermValidationTests(unittest.TestCase):
    def setUp(self):
        self.value = yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))
        self.value["concepts"][0]["subject_fields"] = []
        self.concept = self.value["concepts"][0]
        self.term = self.concept["languages"][0]["terms"][0]
        self.sources = {
            "topics": {"concepts": [{"id": "computing"}]},
            "bibliography": {"references": [{
                "id": "cs2023", "kind": "standard", "tier": "de-jure",
                "version": "2023", "fixed_sha256": "0" * 64,
            }]},
            "sources": {"sources": []},
        }
        self.grant_id = "decision-term-0001"

    def grants(self, value=None):
        concept = (value or self.value)["concepts"][0]
        grant = decision(self.grant_id, [{
            "identity": f"terms/concepts/{concept['id']}",
            "field": "record",
            "value": semantic_concept(concept),
        }])
        return {grant["id"]: grant}

    def model_basis(self, approval=None):
        return {
            "level": 5,
            "model": {
                "name": "GPT-5", "date": "2026-09-06",
                "rationale": "Existing Chinese industry expression.",
                "approval": approval or self.grant_id,
            },
        }

    def extra_concept(self):
        concept = copy.deepcopy(self.value["concepts"][0])
        concept["id"] = "tc-33333333-3333-4333-8333-333333333333"
        concept["history"][0]["decision"] = "decision-extra"
        for index, term in enumerate(concept["languages"][0]["terms"], 1):
            term["id"] = f"tm-33333333-3333-4333-8333-33333333333{index}"
            term["history"][0]["decision"] = "decision-extra"
            term["history"][0]["linked_terms"] = [term["id"]]
        return concept

    def codes(self, value=None, decisions=None, previous=None, state=None,
              historical_decisions=None):
        return {issue.code for issue in validate_term_snapshot(
            value or self.value,
            source_documents=self.sources,
            accepted_decisions=decisions if decisions is not None else self.grants(value),
            previous=previous,
            state=state,
            historical_decisions=historical_decisions,
        )}

    def test_precisely_granted_active_concept_with_empty_subject_fields_is_valid(self):
        self.assertEqual(set(), self.codes())

    def test_l1_record_grant_cannot_adopt_a_term_concept(self):
        grant = next(iter(self.grants().values()))
        grant["level"] = "L1"

        codes = self.codes(decisions={grant["id"]: grant})
        self.assertIn("TERM_ADOPTION_MISSING", codes)
        self.assertIn("TERM_HISTORY_TRANSITION_INVALID", codes)

    def test_proposed_superseded_and_wrong_value_grants_do_not_authorize(self):
        exact = next(iter(self.grants().values()))
        proposed = copy.deepcopy(exact)
        proposed["status"] = "proposed"
        wrong = copy.deepcopy(exact)
        wrong["id"] = "wrong-value"
        wrong["answers"][0]["patches"][0]["value"]["definitions"][0]["text"] = "Other"
        replacement = decision("replacement", [{
            "identity": "@control:test", "field": "record", "value": True,
        }], supersedes=[exact["id"]])

        for decisions in (
            {proposed["id"]: proposed},
            {exact["id"]: exact, replacement["id"]: replacement},
            {wrong["id"]: wrong},
        ):
            with self.subTest(decisions=decisions):
                self.assertIn("TERM_ADOPTION_MISSING", self.codes(decisions=decisions))

    def test_historical_decisions_keep_append_only_superseded_acceptances_only(self):
        grant_a = next(iter(self.grants().values()))
        grant_b = decision("decision-term-0002", [{
            "identity": "@control:test", "field": "record", "value": True,
        }], supersedes=[grant_a["id"]])
        proposed = decision("proposed-history", [{
            "identity": "@control:test", "field": "record", "value": False,
        }], status="proposed")
        explicit = decision("explicit-superseded", [{
            "identity": "@control:test", "field": "record", "value": False,
        }], status="superseded")

        historical = historical_decisions_from_documents([
            grant_a, grant_b, proposed, explicit,
        ])

        self.assertEqual({grant_a["id"], grant_b["id"]}, set(historical))

    def test_other_object_and_independent_term_grants_cannot_be_borrowed(self):
        wrong_object = decision(self.grant_id, [{
            "identity": "terms/concepts/tc-99999999-9999-4999-8999-999999999999",
            "field": "record", "value": semantic_concept(self.concept),
        }])
        wrong_term = decision(self.grant_id, [{
            "identity": f"terms/terms/{self.term['id']}", "field": "record",
            "value": semantic_term(self.concept["id"], "en", self.term),
        }])

        self.assertIn("TERM_ADOPTION_MISSING", self.codes(decisions={wrong_object["id"]: wrong_object}))
        self.assertIn("TERM_ADOPTION_MISSING", self.codes(decisions={wrong_term["id"]: wrong_term}))

    def test_previous_equal_to_current_does_not_supply_authority(self):
        self.assertIn(
            "TERM_ADOPTION_MISSING",
            self.codes(previous=copy.deepcopy(self.value), decisions={}),
        )

    def test_effective_approved_concept_cannot_be_omitted_static_or_with_spoofed_previous(self):
        extra = self.extra_concept()
        decisions = self.grants()
        decisions["decision-extra"] = decision("decision-extra", [{
            "identity": f"terms/concepts/{extra['id']}",
            "field": "record", "value": semantic_concept(extra),
        }])

        for previous in (None, copy.deepcopy(self.value)):
            with self.subTest(previous=previous is not None):
                self.assertIn(
                    "TERM_APPROVED_CONCEPT_MISSING",
                    self.codes(decisions=decisions, previous=previous),
                )

    def test_superseded_historical_record_does_not_require_an_extra_member(self):
        extra = self.extra_concept()
        old = decision("decision-extra", [{
            "identity": f"terms/concepts/{extra['id']}",
            "field": "record", "value": semantic_concept(extra),
        }])
        replacement = decision("decision-extra-replacement", [{
            "identity": "@control:terms", "field": "scope", "value": True,
        }], supersedes=[old["id"]])
        current = self.grants()
        captured = {**current, old["id"]: old, replacement["id"]: replacement}

        self.assertEqual(
            set(),
            self.codes(
                decisions=accepted_decisions_from_documents(captured.values()),
                historical_decisions=captured,
            ),
        )

    def test_invalid_record_identity_or_value_does_not_create_a_required_member(self):
        extra = self.extra_concept()
        malformed = decision("malformed-extra", [
            {
                "identity": f"terms/concepts/{extra['id']}/nested",
                "field": "record", "value": semantic_concept(extra),
            },
            {
                "identity": f"terms/concepts/{extra['id']}",
                "field": "record", "value": {"id": extra["id"], "workflow": "active"},
            },
        ])

        self.assertNotIn(
            "TERM_APPROVED_CONCEPT_MISSING",
            self.codes(decisions={**self.grants(), malformed["id"]: malformed}),
        )

    def test_candidate_cannot_borrow_a_scope_grant(self):
        value = copy.deepcopy(self.value)
        value["concepts"][0]["workflow"] = "candidate"
        value["concepts"][0]["history"][0]["to_value"] = "candidate"
        scope = decision("scope-only", [{
            "identity": "@control:terms", "field": "scope",
            "value": {"structure": "approved"},
        }])

        self.assertIn(
            "TERM_ADOPTION_MISSING",
            self.codes(value=value, decisions={scope["id"]: scope}),
        )

    def test_bad_source_reference_is_rejected_despite_exact_grant(self):
        value = copy.deepcopy(self.value)
        value["concepts"][0]["definitions"][0]["basis"][0]["reference"] = "missing"

        self.assertIn("TERM_SOURCE_CONTRACT_SOURCE_ENTITY_MISSING", self.codes(value=value))

    def test_chinese_model_basis_requires_current_exact_grant_and_matching_term_history(self):
        value = copy.deepcopy(self.value)
        language = value["concepts"][0]["languages"][0]
        language["language"] = "zh-Hans"
        language["terms"][0]["text"] = "阿尔法"
        language["terms"][0]["basis"] = self.model_basis()

        self.assertEqual(set(), self.codes(value=value))

        wrong = copy.deepcopy(value)
        wrong["concepts"][0]["languages"][0]["terms"][0]["basis"] = self.model_basis(
            "scope-only"
        )
        scope = decision("scope-only", [{
            "identity": "@control:terms", "field": "scope", "value": True,
        }])
        decisions = self.grants(wrong)
        decisions[scope["id"]] = scope
        self.assertIn("TERM_MODEL_APPROVAL_INVALID", self.codes(value=wrong, decisions=decisions))

        wrong_concept = copy.deepcopy(value)
        wrong_term = wrong_concept["concepts"][0]["languages"][0]["terms"][0]
        wrong_term["basis"] = self.model_basis("wrong-concept-grant")
        wrong_term["history"][0]["decision"] = "wrong-concept-grant"
        decisions = self.grants(wrong_concept)
        unrelated = decision("wrong-concept-grant", [{
            "identity": "terms/concepts/tc-99999999-9999-4999-8999-999999999999",
            "field": "record", "value": semantic_concept(wrong_concept["concepts"][0]),
        }])
        decisions[unrelated["id"]] = unrelated
        self.assertIn(
            "TERM_MODEL_APPROVAL_INVALID",
            self.codes(value=wrong_concept, decisions=decisions),
        )

    def test_project_basis_requires_exact_l3_record_and_project_scope(self):
        concept = next(
            row for row in CANDIDATE["proposed_terms"]["concepts"]
            if row["id"] == "tc-56bf269d-a675-4fc3-a2c1-b1f38a734d81"
        )
        value = {"schema": "urn:kb-design:schema:terms:1", "version": 1,
                 "concepts": [copy.deepcopy(concept)]}
        approval = concept["basis"]["project"]["approval"]
        grant = decision(approval, [
            {"identity": f"terms/concepts/{concept['id']}", "field": "record",
             "value": semantic_concept(concept)},
            {"identity": f"terms/concepts/{concept['id']}", "field": "project_basis_scope",
             "value": semantic_project_basis_scope(concept)},
        ], level="L3")

        self.assertEqual(set(), self.codes(value=value, decisions={approval: grant}))
        grant["answers"][0]["patches"].pop()
        self.assertIn(
            "TERM_PROJECT_BASIS_UNAUTHORIZED",
            self.codes(value=value, decisions={approval: grant}),
        )

        data_driven = copy.deepcopy(value)
        changed = data_driven["concepts"][0]
        changed["id"] = "tc-77777777-7777-4777-8777-777777777777"
        changed["history"][0]["decision"] = approval
        for term in changed["languages"][0]["terms"]:
            term["id"] = "tm-77777777-7777-4777-8777-777777777777"
            term["history"][0]["decision"] = approval
        grant = decision(approval, [
            {"identity": f"terms/concepts/{changed['id']}", "field": "record",
             "value": semantic_concept(changed)},
            {"identity": f"terms/concepts/{changed['id']}", "field": "project_basis_scope",
             "value": semantic_project_basis_scope(changed)},
        ], level="L3")
        self.assertEqual(set(), self.codes(value=data_driven, decisions={approval: grant}))

    def test_de_facto_definition_requires_exact_l3_permission_and_source_version(self):
        entry = CANDIDATE["limited_definition_permission_proposal"]["entries"][0]
        concept = next(
            row for row in CANDIDATE["proposed_terms"]["concepts"]
            if row["id"] == entry["concept_id"]
        )
        value = {"schema": "urn:kb-design:schema:terms:1", "version": 1,
                 "concepts": [copy.deepcopy(concept)]}
        data_grant = decision("decision-term-data-values", [{
            "identity": f"terms/concepts/{concept['id']}", "field": "record",
            "value": semantic_concept(concept),
        }], level="L3")
        permission = decision(
            "decision-term-limited-definition-source-use",
            [entry["permission_patch"]], level="L3",
        )
        decisions = {data_grant["id"]: data_grant, permission["id"]: permission}
        self.sources["bibliography"]["references"].append({
            "id": "swebok", "kind": "standard", "tier": "de-facto",
            "version": "4.0", "fixed_sha256": "1" * 64,
        })

        self.assertEqual(set(), self.codes(value=value, decisions=decisions))
        self.sources["bibliography"]["references"][-1]["version"] = "5.0"
        self.assertIn(
            "TERM_DEFINITION_SOURCE_FORBIDDEN",
            self.codes(value=value, decisions=decisions),
        )

    def test_english_term_cannot_use_model_basis(self):
        value = copy.deepcopy(self.value)
        value["concepts"][0]["languages"][0]["terms"][0]["basis"] = self.model_basis()

        self.assertIn("TERM_MODEL_LANGUAGE_INVALID", self.codes(value=value))

    def test_external_to_model_basis_requires_exact_correction(self):
        previous = copy.deepcopy(self.value)
        previous_language = previous["concepts"][0]["languages"][0]
        previous_language["language"] = "zh-Hans"
        previous_language["terms"][0]["text"] = "阿尔法"
        current = copy.deepcopy(previous)
        concept = current["concepts"][0]
        language = concept["languages"][0]
        language["language"] = "zh-Hans"
        language["terms"][0]["text"] = "阿尔法"
        language["terms"][0]["basis"] = self.model_basis("decision-term-0002")
        for record in (concept, language["terms"][0]):
            record["history"].append({
                "date": "2026-09-06", "event": "basis-corrected",
                "decision": "decision-term-0002", "reason": "precise basis correction",
                "from_value": "sha256:external", "to_value": "sha256:model",
                "linked_terms": [],
            })
        grant = decision("decision-term-0002", [{
            "identity": f"terms/concepts/{concept['id']}",
            "field": "record", "value": semantic_concept(concept),
        }])
        old_grant = next(iter(self.grants(previous).values()))
        captured = {old_grant["id"]: old_grant, grant["id"]: grant}

        self.assertIn(
            "TERM_MODEL_BASIS_CORRECTION_MISSING",
            self.codes(
                value=current,
                decisions=accepted_decisions_from_documents(captured.values()),
                historical_decisions=captured,
            ),
        )

        self.assertIn(
            "TERM_MODEL_BASIS_CORRECTION_MISSING",
            self.codes(
                value=current,
                decisions=accepted_decisions_from_documents(captured.values()),
                historical_decisions=captured,
                previous=previous,
            ),
        )

        grant["answers"][0]["patches"].append({
            "identity": f"terms/terms/{language['terms'][0]['id']}",
            "field": "basis.correction",
            "value": {
                "before": previous_language["terms"][0]["basis"],
                "after": language["terms"][0]["basis"],
            },
        })
        effective = accepted_decisions_from_documents(captured.values())
        for old in (None, previous):
            with self.subTest(correction_present=True, previous=old is not None):
                self.assertNotIn(
                    "TERM_MODEL_BASIS_CORRECTION_MISSING",
                    self.codes(
                        value=current, decisions=effective,
                        historical_decisions=captured, previous=old,
                    ),
                )

    def test_model_update_inherits_valid_historical_external_to_model_correction(self):
        original = copy.deepcopy(self.value)
        original_language = original["concepts"][0]["languages"][0]
        original_language["language"] = "zh-Hans"
        original_language["terms"][0]["text"] = "阿尔法"
        grant_a = next(iter(self.grants(original).values()))

        adopted = copy.deepcopy(original)
        adopted_concept = adopted["concepts"][0]
        adopted_term = adopted_concept["languages"][0]["terms"][0]
        adopted_term["basis"] = self.model_basis("decision-term-0002")
        for record in (adopted_concept, adopted_term):
            record["history"].append({
                "date": "2026-09-06", "event": "basis-corrected",
                "decision": "decision-term-0002", "reason": "model adoption",
                "from_value": "sha256:external", "to_value": "sha256:model-b",
                "linked_terms": [],
            })
        grant_b = decision("decision-term-0002", [
            {
                "identity": f"terms/concepts/{adopted_concept['id']}",
                "field": "record", "value": semantic_concept(adopted_concept),
            },
            {
                "identity": f"terms/terms/{adopted_term['id']}",
                "field": "basis.correction",
                "value": {"before": original_language["terms"][0]["basis"],
                          "after": adopted_term["basis"]},
            },
        ])

        current = copy.deepcopy(adopted)
        current_concept = current["concepts"][0]
        current_term = current_concept["languages"][0]["terms"][0]
        current_term["basis"]["model"]["rationale"] = "Updated model judgment."
        current_term["basis"]["model"]["approval"] = "decision-term-0003"
        for record in (current_concept, current_term):
            record["history"].append({
                "date": "2026-09-07", "event": "basis-updated",
                "decision": "decision-term-0003", "reason": "model update",
                "from_value": "sha256:model-b", "to_value": "sha256:model-c",
                "linked_terms": [],
            })
        grant_c = decision("decision-term-0003", [{
            "identity": f"terms/concepts/{current_concept['id']}",
            "field": "record", "value": semantic_concept(current_concept),
        }], supersedes=[grant_b["id"]])
        captured = {row["id"]: row for row in (grant_a, grant_b, grant_c)}

        self.assertEqual(
            set(),
            self.codes(
                value=current,
                decisions=accepted_decisions_from_documents(captured.values()),
                historical_decisions=captured,
            ),
        )

    def test_unapproved_definition_rewrite_is_rejected(self):
        previous = copy.deepcopy(self.value)
        current = copy.deepcopy(previous)
        current["concepts"][0]["definitions"][0]["text"] = "Rewritten without grant."

        self.assertIn(
            "TERM_ADOPTION_MISSING",
            self.codes(value=current, decisions=self.grants(previous), previous=previous),
        )

    def test_changed_record_grant_must_be_recorded_in_new_history(self):
        previous = copy.deepcopy(self.value)
        current = copy.deepcopy(previous)
        current["concepts"][0]["definitions"][0]["text"] = "Precisely granted rewrite."

        self.assertIn(
            "TERM_ADOPTION_HISTORY_MISSING",
            self.codes(value=current, decisions=self.grants(current), previous=previous),
        )

    def test_semantic_change_fingerprint_event_does_not_replace_state_history(self):
        previous = copy.deepcopy(self.value)
        current = copy.deepcopy(previous)
        concept = current["concepts"][0]
        concept["definitions"][0]["text"] = "Precisely granted rewrite."
        concept["history"].append({
            "date": "2026-09-06", "event": "definition-updated",
            "decision": self.grant_id, "reason": "precise semantic update",
            "from_value": "sha256:before", "to_value": "sha256:after",
            "linked_terms": [],
        })

        self.assertEqual(
            set(),
            self.codes(value=current, decisions=self.grants(current), previous=previous),
        )

    def test_superseding_record_grant_preserves_real_initial_migration_static_and_dynamic(self):
        previous = copy.deepcopy(self.value)
        current = copy.deepcopy(previous)
        concept = current["concepts"][0]
        concept["definitions"][0]["text"] = "Precisely granted rewrite."
        concept["history"].append({
            "date": "2026-09-06", "event": "definition-updated",
            "decision": "decision-term-0002", "reason": "precise semantic update",
            "from_value": "sha256:before", "to_value": "sha256:after",
            "linked_terms": [],
        })
        grant_a = next(iter(self.grants(previous).values()))
        grant_b = decision("decision-term-0002", [{
            "identity": f"terms/concepts/{concept['id']}",
            "field": "record", "value": semantic_concept(concept),
        }], supersedes=[grant_a["id"]])
        captured = {grant_a["id"]: grant_a, grant_b["id"]: grant_b}
        effective = accepted_decisions_from_documents(captured.values())

        for old in (None, previous):
            with self.subTest(previous=old is not None):
                self.assertEqual(
                    set(),
                    self.codes(
                        value=current, decisions=effective, previous=old,
                        historical_decisions=captured,
                    ),
                )

    def test_old_grant_cannot_authorize_the_current_record(self):
        previous = copy.deepcopy(self.value)
        current = copy.deepcopy(previous)
        current["concepts"][0]["definitions"][0]["text"] = "Unapproved current value."
        grant_a = self.grants(previous)

        self.assertIn(
            "TERM_ADOPTION_MISSING",
            self.codes(
                value=current, decisions=grant_a,
                historical_decisions=grant_a,
            ),
        )

    def test_term_identity_cannot_move_between_languages(self):
        previous = copy.deepcopy(self.value)
        current = copy.deepcopy(previous)
        language = current["concepts"][0]["languages"][0]
        language["language"] = "zh-Hans"
        current["concepts"][0]["definitions"][0]["language"] = "zh-Hans"

        self.assertIn(
            "TERM_IDENTITY_CHANGED",
            self.codes(value=current, decisions=self.grants(current), previous=previous),
        )

    def test_initial_active_history_cannot_name_an_unrelated_decision(self):
        decisions = self.grants()
        grant = decisions.pop(self.grant_id)
        grant["id"] = "precise-grant"
        decisions[grant["id"]] = grant

        self.assertIn("TERM_ADOPTION_HISTORY_MISSING", self.codes(decisions=decisions))

    def test_static_snapshot_accepts_a_real_candidate_to_active_history(self):
        value = copy.deepcopy(self.value)
        concept = value["concepts"][0]
        concept["history"].insert(0, {
            "date": "2026-09-05", "event": "registered",
            "decision": "candidate-grant", "reason": "candidate registration",
            "from_value": None, "to_value": "candidate", "linked_terms": [],
        })
        concept["history"][1]["from_value"] = "candidate"
        decisions = self.grants(value)
        decisions["candidate-grant"] = decision("candidate-grant", [{
            "identity": "@control:fixture", "field": "record", "value": True,
        }])

        self.assertEqual(set(), self.codes(value=value, decisions=decisions))

    def test_static_history_state_must_match_current_concept_and_term_states(self):
        value = copy.deepcopy(self.value)
        concept = value["concepts"][0]
        concept["history"][0]["to_value"] = "deprecated"
        concept["languages"][0]["terms"][0]["history"][0][
            "to_value"
        ] = "deprecatedTerm-admn-sts"

        issues = validate_term_snapshot(
            value,
            source_documents=self.sources,
            accepted_decisions=self.grants(value),
        )
        mismatch_paths = {
            issue.path for issue in issues
            if issue.code == "TERM_HISTORY_STATE_MISMATCH"
        }

        self.assertIn("concepts[0].history", mismatch_paths)
        self.assertIn(f"terms[{self.term['id']}].history", mismatch_paths)

    def test_previous_does_not_exempt_old_history_decisions(self):
        value = copy.deepcopy(self.value)
        value["concepts"][0]["languages"][0]["terms"][0]["history"][0][
            "decision"
        ] = "missing-old-decision"

        self.assertIn(
            "TERM_DECISION_MISSING",
            self.codes(value=value, decisions=self.grants(value), previous=copy.deepcopy(value)),
        )

    def test_static_snapshot_requires_one_preferred_term_and_no_replacement_cycle(self):
        no_preferred = copy.deepcopy(self.value)
        no_preferred["concepts"][0]["languages"][0]["terms"][0][
            "administrative_status"
        ] = "admittedTerm-admn-sts"
        self.assertIn("TERM_PREFERRED_COUNT", self.codes(value=no_preferred))

        cycle = copy.deepcopy(self.value)
        terms = cycle["concepts"][0]["languages"][0]["terms"]
        for row, target in ((terms[0], terms[1]["id"]), (terms[1], terms[0]["id"])):
            row["administrative_status"] = "supersededTerm-admn-sts"
            row["replaced_by"] = target
        self.assertIn("TERM_REPLACEMENT_CYCLE", self.codes(value=cycle))

    def test_static_snapshot_rejects_missing_cross_language_and_unusable_replacements(self):
        cases = []
        missing = copy.deepcopy(self.value)
        replacement = missing["concepts"][0]["languages"][0]["terms"][1]
        replacement["administrative_status"] = "supersededTerm-admn-sts"
        replacement["replaced_by"] = "tm-99999999-9999-4999-8999-999999999999"
        cases.append((missing, "TERM_REPLACEMENT_MISSING"))

        unusable = copy.deepcopy(self.value)
        terms = unusable["concepts"][0]["languages"][0]["terms"]
        terms[0]["administrative_status"] = "supersededTerm-admn-sts"
        terms[0]["replaced_by"] = terms[1]["id"]
        terms[1]["administrative_status"] = "deprecatedTerm-admn-sts"
        cases.append((unusable, "TERM_REPLACEMENT_TARGET_STATUS"))

        cross_language = copy.deepcopy(self.value)
        terms = cross_language["concepts"][0]["languages"][0]["terms"]
        moved = terms.pop()
        cross_language["concepts"][0]["languages"].append({
            "language": "zh-Hans", "terms": [moved],
        })
        terms[0]["administrative_status"] = "supersededTerm-admn-sts"
        terms[0]["replaced_by"] = moved["id"]
        moved["administrative_status"] = "preferredTerm-admn-sts"
        cases.append((cross_language, "TERM_REPLACEMENT_LANGUAGE"))

        for value, expected in cases:
            with self.subTest(expected=expected):
                self.assertIn(expected, self.codes(value=value))

    def test_array_id_is_not_a_valid_subject_concept(self):
        value = copy.deepcopy(self.value)
        value["concepts"][0]["subject_fields"] = [{
            "topic_id": "array-only",
            "basis": [{"reference": "cs2023", "locator": "array", "checked": "2026-08-31"}],
        }]
        self.sources["topics"]["arrays"] = [{"id": "array-only"}]

        self.assertIn("TERM_SUBJECT_FIELD_UNKNOWN", self.codes(value=value))

    def test_active_state_requires_exact_l3_publication_grant_and_valid_history(self):
        state = {
            "schema": "urn:kb-design:data:term-cutover-state", "version": 1,
            "state": "active", "active_editor": "data/vocab/terms.yaml",
            "terms_mode": "active_editor", "consumers_enabled": True,
            "decision": "state-grant",
            "history": [{
                "date": "2026-09-06", "event": "activation", "decision": "state-grant",
                "reason": "fixture", "from_value": None, "to_value": "active",
                "linked_terms": [],
            }],
        }
        decisions = self.grants()
        decisions["state-grant"] = decision("state-grant", [{
            "identity": "@control:terms", "field": "publication",
            "value": {key: state[key] for key in (
                "active_editor", "state", "terms_mode", "consumers_enabled"
            )},
        }])

        self.assertEqual(set(), self.codes(decisions=decisions, state=state))
        decisions["state-grant"]["level"] = "L2"
        self.assertIn("TERM_STATE_DECISION_MISSING", self.codes(decisions=decisions, state=state))

        decisions["state-grant"]["level"] = "L3"
        unrelated = decision("unrelated-history", [{
            "identity": "@control:test", "field": "record", "value": True,
        }])
        decisions[unrelated["id"]] = unrelated
        state["history"][0]["decision"] = unrelated["id"]
        self.assertIn("TERM_STATE_HISTORY", self.codes(decisions=decisions, state=state))


if __name__ == "__main__":
    unittest.main()
