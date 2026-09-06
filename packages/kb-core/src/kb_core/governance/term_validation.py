import copy
from pathlib import Path
from typing import Mapping

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from kb_core.governance.term_model import (
    TermIssue,
    collect_reference_uses,
    parse_terms,
    schema_issues,
    term_basis_kind,
    validate_term_document,
)
from kb_core.governance.term_transitions import (
    CONCEPT_TRANSITIONS,
    TERM_TRANSITIONS,
    validate_replacements,
    validate_transition,
)
from kb_core.source_model import (
    accepted_decisions_from_documents,
    build_schema_documents,
    decision_authorizes,
    normalize_yaml_dates,
    validate_reference_documents,
)


def _without_history(value):
    if isinstance(value, dict):
        return {
            key: _without_history(item)
            for key, item in value.items()
            if key != "history"
        }
    if isinstance(value, list):
        return [_without_history(item) for item in value]
    return copy.deepcopy(value)


def semantic_concept(concept: Mapping[str, object]) -> dict[str, object]:
    """Return the exact adoptable concept value, excluding all history."""
    return _without_history(dict(concept))


def semantic_term(concept_id: str, language: str,
                  term: Mapping[str, object]) -> dict[str, object]:
    """Return the exact independently adoptable term value."""
    return {
        "concept": concept_id,
        "language": language,
        **_without_history(dict(term)),
    }


def semantic_project_basis_scope(concept: Mapping[str, object]) -> dict[str, object]:
    definitions = [
        copy.deepcopy(row) for row in concept.get("definitions", [])
        if term_basis_kind(row.get("basis")) == "project"
    ]
    terms = [
        semantic_term(concept["id"], language, term)
        for _, language, term in _term_rows({"concepts": [concept]})
        if term_basis_kind(term.get("basis")) == "project"
    ]
    concept_basis = concept.get("basis")
    return {
        "concept_basis": copy.deepcopy(concept_basis)
        if term_basis_kind(concept_basis) == "project" else None,
        "definitions": definitions,
        "terms": terms,
    }


def _issue(code, path, message, origin="term"):
    return TermIssue(code, origin, path, message)


def _accepted(values):
    if not isinstance(values, Mapping):
        return {}
    return accepted_decisions_from_documents(list(values.values()))


def historical_decisions_from_documents(frontmatters) -> dict[str, dict[str, object]]:
    """Select unique schema-valid frontmatters that still record accepted status."""
    schema = build_schema_documents()["decision.schema.json"]
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    documents = {}
    for value in frontmatters:
        front = normalize_yaml_dates(value)
        if (
            isinstance(front, dict)
            and front.get("status") == "accepted"
            and validator.is_valid(front)
        ):
            documents.setdefault(front["id"], []).append(front)
    return {
        decision_id: values[0]
        for decision_id, values in documents.items()
        if len(values) == 1
    }


def _patch_decision_ids(decisions, identity, field, value, *, level=None, levels=None):
    result = set()
    for decision_id, front in decisions.items():
        if level is not None and front.get("level") != level:
            continue
        if levels is not None and front.get("level") not in levels:
            continue
        if decision_authorizes(decisions, decision_id, identity, field, value):
            result.add(decision_id)
    return result


def _topic_ids(document):
    values = document.get("concepts", []) if isinstance(document, Mapping) else []
    return frozenset(
        row["id"] for row in values
        if isinstance(row, Mapping) and isinstance(row.get("id"), str)
    )


def _convert_source_issues(issues):
    return [
        _issue(
            "TERM_SOURCE_CONTRACT_" + issue.code,
            issue.field_path,
            f"{issue.file}:{issue.record}:{issue.field_path}: {issue.message}",
            "source",
        )
        for issue in issues
    ]


def _history_decisions(value):
    return {
        event.get("decision")
        for event in value.get("history", [])
        if isinstance(event, Mapping) and isinstance(event.get("decision"), str)
    }


def _term_rows(value):
    for concept in value.get("concepts", []):
        for language in concept.get("languages", []):
            for term in language.get("terms", []):
                yield concept, language.get("language"), term


def _validate_adoption(value, previous, decisions, issues):
    previous_concepts = {
        row["id"]: row for row in (previous or {}).get("concepts", [])
        if isinstance(row, Mapping) and isinstance(row.get("id"), str)
    }
    previous_terms = {
        row["id"]: (concept["id"], language, row)
        for concept, language, row in _term_rows(previous or {})
    }
    current_concept_ids = {
        row.get("id") for row in value.get("concepts", []) if isinstance(row, Mapping)
    }
    approved_concept_ids = set()
    for front in decisions.values():
        if front.get("level") not in {"L2", "L3"}:
            continue
        for answer in front.get("answers", []):
            for patch in answer.get("patches", []):
                identity = patch.get("identity")
                if not isinstance(identity, str) or not identity.startswith("terms/concepts/"):
                    continue
                concept_id = identity.removeprefix("terms/concepts/")
                if (
                    "/" not in concept_id
                    and _complete_historical_record(patch.get("value"), concept_id)
                ):
                    approved_concept_ids.add(concept_id)
    for missing in sorted(approved_concept_ids - current_concept_ids):
        issues.append(_issue(
            "TERM_APPROVED_CONCEPT_MISSING", f"concepts[{missing}]",
            "an effectively approved term concept is missing from the canonical snapshot",
        ))
    for removed in sorted(set(previous_concepts) - current_concept_ids):
        issues.append(_issue(
            "TERM_CONCEPT_ID_REMOVED", f"concepts[{removed}]",
            "term concept identities cannot be deleted",
        ))

    for concept_index, concept in enumerate(value.get("concepts", [])):
        concept_id = concept["id"]
        identity = f"terms/concepts/{concept_id}"
        concept_grants = _patch_decision_ids(
            decisions, identity, "record", semantic_concept(concept),
            levels={"L2", "L3"},
        )
        old = previous_concepts.get(concept_id)
        if not concept_grants:
            issues.append(_issue(
                "TERM_ADOPTION_MISSING", f"concepts[{concept_index}]",
                "concept lacks an exact current record grant",
            ))
        elif not concept_grants & _history_decisions(concept):
            issues.append(_issue(
                "TERM_ADOPTION_HISTORY_MISSING", f"concepts[{concept_index}].history",
                "concept history does not record its exact current grant",
            ))
        elif old is not None and semantic_concept(old) != semantic_concept(concept):
            new_history = concept.get("history", [])[len(old.get("history", [])):]
            if not concept_grants & _history_decisions({"history": new_history}):
                issues.append(_issue(
                    "TERM_ADOPTION_HISTORY_MISSING", f"concepts[{concept_index}].history",
                    "changed concept history does not record its exact current grant",
                ))

        for language in concept.get("languages", []):
            language_tag = language["language"]
            for term in language.get("terms", []):
                term_id = term["id"]
                old_entry = previous_terms.get(term_id)
                if old_entry is not None and old_entry[:2] != (concept_id, language_tag):
                    issues.append(_issue(
                        "TERM_IDENTITY_CHANGED", f"terms[{term_id}]",
                        "a term identity cannot move between concepts or languages",
                    ))


def _historical_record_basis(front, concept_id, term_id):
    values = []
    if front.get("level") not in {"L2", "L3"}:
        return None
    for answer in front.get("answers", []):
        for patch in answer.get("patches", []):
            record = patch.get("value")
            if (
                patch.get("identity") != f"terms/concepts/{concept_id}"
                or patch.get("field") != "record"
                or not _complete_historical_record(record, concept_id)
            ):
                continue
            for _, _, term in _term_rows({"concepts": [record]}):
                if term.get("id") == term_id:
                    values.append(term.get("basis"))
    return values[0] if len(values) == 1 else None


def _historical_basis_sequence(concept, term_id, historical):
    sequence = []
    for event in concept.get("history", []):
        decision_id = event.get("decision")
        basis = _historical_record_basis(
            historical.get(decision_id, {}), concept["id"], term_id,
        )
        if basis is None:
            continue
        if not sequence or sequence[-1] != (decision_id, basis):
            sequence.append((decision_id, basis))
    return sequence


def _validate_model_basis(value, previous, decisions, historical, issues):
    previous_terms = {
        row["id"]: row for _, _, row in _term_rows(previous or {})
    }
    for concept, language, term in _term_rows(value):
        basis = term.get("basis")
        if term_basis_kind(basis) != "model":
            continue
        path = f"terms[{term['id']}].basis"
        if language not in {"zh-Hans", "zh-Hant"}:
            issues.append(_issue(
                "TERM_MODEL_LANGUAGE_INVALID", path,
                "model basis is limited to Chinese term forms",
            ))
        approval = basis["model"]["approval"]
        concept_grants = _patch_decision_ids(
            decisions, f"terms/concepts/{concept['id']}", "record",
            semantic_concept(concept), levels={"L2", "L3"},
        )
        if approval not in concept_grants or approval not in _history_decisions(term):
            issues.append(_issue(
                "TERM_MODEL_APPROVAL_INVALID", f"{path}.model.approval",
                "model basis approval must grant the current concept and occur in term history",
            ))
        sequence = _historical_basis_sequence(concept, term["id"], historical)
        for (_, before), (new_decision, after) in zip(sequence, sequence[1:]):
            if (
                term_basis_kind(before) == "external"
                and term_basis_kind(after) == "model"
                and not decision_authorizes(
                    historical, new_decision, f"terms/terms/{term['id']}",
                    "basis.correction", {"before": before, "after": after},
                )
            ):
                issues.append(_issue(
                    "TERM_MODEL_BASIS_CORRECTION_MISSING", path,
                    "external basis cannot be replaced by model basis without an exact correction",
                ))
        old = previous_terms.get(term["id"])
        if (
            old is not None
            and term_basis_kind(old.get("basis")) == "external"
            and not decision_authorizes(
                decisions, approval, f"terms/terms/{term['id']}",
                "basis.correction", {"before": old["basis"], "after": basis},
            )
        ):
            issues.append(_issue(
                "TERM_MODEL_BASIS_CORRECTION_MISSING", path,
                "external basis cannot be replaced by model basis without an exact correction",
            ))


def _validate_project_basis(value, decisions, issues):
    for concept in value.get("concepts", []):
        concept_id = concept["id"]
        scope = semantic_project_basis_scope(concept)
        record_grants = _patch_decision_ids(
            decisions, f"terms/concepts/{concept_id}", "record",
            semantic_concept(concept), level="L3",
        )
        scope_grants = _patch_decision_ids(
            decisions, f"terms/concepts/{concept_id}", "project_basis_scope",
            scope, level="L3",
        )
        uses = []
        if term_basis_kind(concept.get("basis")) == "project":
            uses.append((concept["basis"], f"concepts[{concept_id}].basis",
                         concept.get("history", [])))
        for index, definition in enumerate(concept.get("definitions", [])):
            if term_basis_kind(definition.get("basis")) == "project":
                uses.append((definition["basis"], f"concepts[{concept_id}].definitions[{index}].basis",
                             concept.get("history", [])))
        for _, _, term in _term_rows({"concepts": [concept]}):
            if term_basis_kind(term.get("basis")) == "project":
                uses.append((term["basis"], f"terms[{term['id']}].basis",
                             term.get("history", [])))
        for basis, path, history in uses:
            approval = basis["project"]["approval"]
            if (
                approval not in record_grants
                or approval not in scope_grants
                or approval not in _history_decisions({"history": history})
            ):
                issues.append(_issue(
                    "TERM_PROJECT_BASIS_UNAUTHORIZED", path,
                    "project basis lacks its exact L3 record and scope authorization",
                ))


def _validate_definition_sources(value, source_documents, decisions, issues):
    entities = {
        row.get("id"): row
        for row in source_documents.get("entities", {}).get("entities", [])
        if isinstance(row, Mapping)
    }
    for concept in value.get("concepts", []):
        concept_id = concept["id"]
        l3_records = _patch_decision_ids(
            decisions, f"terms/concepts/{concept_id}", "record",
            semantic_concept(concept), level="L3",
        )
        for definition in concept.get("definitions", []):
            if term_basis_kind(definition.get("basis")) != "external":
                continue
            for reference in definition["basis"]:
                entity = entities.get(reference.get("entity"), {})
                if entity.get("tier") not in {"de-facto", "vendor"}:
                    continue
                permitted = False
                for decision_id, front in decisions.items():
                    if front.get("level") != "L3" or not l3_records:
                        continue
                    for answer in front.get("answers", []):
                        for patch in answer.get("patches", []):
                            permission = patch.get("value")
                            if (
                                patch.get("identity") == concept_id
                                and patch.get("field") == "definition_source_permission"
                                and isinstance(permission, Mapping)
                                and set(permission) == {
                                    "source_entity", "registered_tier", "registered_version",
                                    "read_material", "checked", "concept_basis", "definitions",
                                }
                                and permission.get("source_entity") == entity.get("id")
                                and permission.get("registered_tier") == entity.get("tier")
                                and permission.get("registered_version") == entity.get("version")
                                and permission.get("concept_basis") == concept.get("basis")
                                and permission.get("definitions") == [definition]
                                and isinstance(permission.get("read_material"), str)
                                and permission["read_material"].strip()
                                and permission.get("checked") == reference.get("checked")
                            ):
                                permitted = True
                if not permitted:
                    issues.append(_issue(
                        "TERM_DEFINITION_SOURCE_FORBIDDEN",
                        f"concepts[{concept_id}].definitions",
                        "de-facto and vendor definition sources require an exact L3 permission",
                    ))


def _validate_static_relations(document, issues):
    for concept in document.concepts:
        for language in concept.languages:
            preferred = [
                term for term in language.terms
                if term.administrative_status == "preferredTerm-admn-sts"
            ]
            if len(preferred) != 1:
                issues.append(_issue(
                    "TERM_PREFERRED_COUNT",
                    f"concepts[{concept.id}].languages[{language.language}]",
                    "each language record must contain exactly one preferred term",
                ))
    issues.extend(validate_replacements(document))


def _validate_state_chain(history, current, states, transitions, path, issues,
                          direct_active_grants=frozenset()):
    state = None
    found = False
    for index, event in enumerate(history):
        before = event.get("from_value")
        after = event.get("to_value")
        if after not in states:
            continue
        found = True
        allowed = (before, after) in transitions
        if (
            before is None
            and after == "active"
            and event.get("decision") in direct_active_grants
        ):
            allowed = True
        if before != state or not allowed:
            issues.append(_issue(
                "TERM_HISTORY_TRANSITION_INVALID", f"{path}[{index}]",
                f"history contains an invalid state transition {before} -> {after}",
            ))
        state = after
    if not found or state != current:
        issues.append(_issue(
            "TERM_HISTORY_STATE_MISMATCH", path,
            f"history state {state} does not match current state {current}",
        ))


def _complete_historical_record(value, concept_id, workflow=None):
    if not isinstance(value, Mapping) or value.get("id") != concept_id:
        return False
    restored = copy.deepcopy(dict(value))
    if (
        "history" in restored
        or workflow is not None and restored.get("workflow") != workflow
    ):
        return False
    event = {
        "date": "2000-01-01", "event": "schema-check",
        "decision": "historical-schema-check", "reason": "schema check",
        "from_value": None, "to_value": restored.get("workflow"), "linked_terms": [],
    }
    restored["history"] = [event]
    languages = restored.get("languages")
    if not isinstance(languages, list):
        return False
    for language in languages:
        if not isinstance(language, dict) or not isinstance(language.get("terms"), list):
            return False
        for term in language["terms"]:
            if not isinstance(term, dict) or "history" in term:
                return False
            term["history"] = [{**event, "to_value": term.get("administrative_status")}]
    document = {
        "schema": "urn:kb-design:schema:terms:1", "version": 1,
        "concepts": [restored],
    }
    return not schema_issues(document)


def _historical_active_grants(decisions, concept_id):
    identity = f"terms/concepts/{concept_id}"
    result = set()
    for decision_id, front in decisions.items():
        if front.get("level") not in {"L2", "L3"}:
            continue
        for answer in front.get("answers", []):
            for patch in answer.get("patches", []):
                if (
                    patch.get("identity") == identity
                    and patch.get("field") == "record"
                    and _complete_historical_record(patch.get("value"), concept_id, "active")
                ):
                    result.add(decision_id)
    return result


def _validate_all_history(value, effective_decisions, historical_decisions, issues):
    for concept_index, concept in enumerate(value.get("concepts", [])):
        concept_grants = _patch_decision_ids(
            effective_decisions, f"terms/concepts/{concept['id']}", "record",
            semantic_concept(concept),
            levels={"L2", "L3"},
        )
        concept_path = f"concepts[{concept_index}].history"
        for index, event in enumerate(concept.get("history", [])):
            if event.get("decision") not in historical_decisions:
                issues.append(_issue(
                    "TERM_DECISION_MISSING", f"{concept_path}[{index}].decision",
                    "concept history decision is not a captured accepted decision",
                ))
        _validate_state_chain(
            concept.get("history", []), concept.get("workflow"),
            {"candidate", "active", "deprecated"}, CONCEPT_TRANSITIONS,
            concept_path, issues,
            _historical_active_grants(historical_decisions, concept["id"]),
        )
        for _, _, term in _term_rows({"concepts": [concept]}):
            term_path = f"terms[{term['id']}].history"
            for index, event in enumerate(term.get("history", [])):
                if event.get("decision") not in historical_decisions:
                    issues.append(_issue(
                        "TERM_DECISION_MISSING", f"{term_path}[{index}].decision",
                        "term history decision is not a captured accepted decision",
                    ))
            _validate_state_chain(
                term.get("history", []), term.get("administrative_status"),
                {
                    "preferredTerm-admn-sts", "admittedTerm-admn-sts",
                    "deprecatedTerm-admn-sts", "supersededTerm-admn-sts",
                }, TERM_TRANSITIONS, term_path, issues,
            )


def _validate_state(state, decisions, historical_decisions, issues):
    state_schema_path = Path(__file__).resolve().parents[5] / "schemas/term-cutover-state-v1.schema.json"
    schema = __import__("json").loads(state_schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in validator.iter_errors(state):
        issues.append(_issue("TERM_STATE_SCHEMA_INVALID", "state", error.message))
    expected = {
        "active_editor": "data/vocab/terms.yaml",
        "state": "active",
        "terms_mode": "active_editor",
        "consumers_enabled": True,
    }
    if any(state.get(key) != item for key, item in expected.items()):
        issues.append(_issue(
            "TERM_STATE_INACTIVE", "state",
            "term publication state is not active",
        ))
    decision_id = state.get("decision")
    if not (
        isinstance(decision_id, str)
        and decision_id in decisions
        and decisions[decision_id].get("level") == "L3"
        and decision_authorizes(
            decisions, decision_id, "@control:terms", "publication", expected,
        )
    ):
        issues.append(_issue(
            "TERM_STATE_DECISION_MISSING", "state.decision",
            "active publication state lacks an exact L3 grant",
        ))
    for index, event in enumerate(state.get("history", [])):
        if event.get("decision") not in historical_decisions:
            issues.append(_issue(
                "TERM_DECISION_MISSING", f"state.history[{index}].decision",
                "state history decision is not a captured accepted decision",
            ))
    if not any(
        event.get("decision") == decision_id
        and event.get("from_value") is None
        and event.get("to_value") == "active"
        for event in state.get("history", [])
    ):
        issues.append(_issue(
            "TERM_STATE_HISTORY", "state.history",
            "active publication history does not record its exact grant",
        ))


def validate_term_snapshot(value, *, source_documents, accepted_decisions,
                           previous=None, state=None,
                           historical_decisions=None) -> tuple[TermIssue, ...]:
    """Validate a captured term snapshot without reading repository data."""
    decisions = _accepted(accepted_decisions)
    historical_input = (
        accepted_decisions if historical_decisions is None else historical_decisions
    )
    historical = historical_decisions_from_documents(
        list(historical_input.values())
        if isinstance(historical_input, Mapping)
        else []
    )
    issues = list(schema_issues(value))
    if issues:
        return tuple(sorted(set(issues), key=lambda item: (item.path, item.code, item.message)))
    document = parse_terms(value)
    issues.extend(validate_term_document(document, _topic_ids(source_documents.get("topics", {}))))
    _validate_static_relations(document, issues)
    references = collect_reference_uses(document)
    source_issues = validate_reference_documents(
        source_documents.get("entities", {}),
        source_documents.get("sources", {}),
        references,
        decisions,
    )
    issues.extend(_convert_source_issues(source_issues))
    _validate_adoption(value, previous, decisions, issues)
    _validate_model_basis(value, previous, decisions, historical, issues)
    _validate_project_basis(value, decisions, issues)
    _validate_definition_sources(value, source_documents, decisions, issues)
    _validate_all_history(value, decisions, historical, issues)
    if previous is not None:
        previous_schema = schema_issues(previous)
        if previous_schema:
            issues.extend(previous_schema)
        else:
            issues.extend(validate_transition(
                parse_terms(previous), document, frozenset(historical),
            ))
    if state is not None:
        _validate_state(state, decisions, historical, issues)
    return tuple(sorted(set(issues), key=lambda item: (
        item.path, item.code, item.message,
    )))


def _front_matter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return None
    return normalize_yaml_dates(yaml.safe_load(text.split("---\n", 2)[1]))


def load_term_decision_sets(
    root: Path,
) -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    """Load effective and historical decisions from one frontmatter capture."""
    directory = root / "docs/decisions"
    documents = [
        _front_matter(path)
        for pattern in ("term-*.md", "source-*.md")
        for path in sorted(directory.glob(pattern))
    ]
    return (
        accepted_decisions_from_documents(documents),
        historical_decisions_from_documents(documents),
    )


def load_term_decisions(root: Path) -> dict[str, dict[str, object]]:
    """Load effective structured term and source decisions from a repository."""
    return load_term_decision_sets(root)[0]
