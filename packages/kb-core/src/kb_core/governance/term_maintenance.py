#!/usr/bin/env python3
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import FrozenSet, List, Mapping, Optional, Sequence


TRIGGER_KINDS = frozenset({
    "source_obligation", "concept", "term", "language", "delegation",
    "decision", "homograph", "schema", "generation", "rollback",
})
TARGET_KINDS = frozenset({
    "concept", "term", "delegation", "decision", "obligation",
    "generated_output",
})
PERIODIC_POLICY_FIELDS = frozenset({
    "interval_months", "next_due", "grace_days", "review_cycle",
    "threshold", "threshold_count", "threshold_percent", "start_date",
})


@dataclass(frozen=True)
class TermIssue:
    code: str
    origin: str
    path: str
    message: str


@dataclass(frozen=True)
class TermTrigger:
    kind: str
    id: str
    previous_obligation: Optional[str]


@dataclass(frozen=True)
class TermObligation:
    id: str
    targets: Sequence[object]
    trigger: TermTrigger
    state: str
    opened: str
    closed: Optional[str]
    decision: Optional[str]
    history: Sequence[object]


def _value(item, name, default=None):
    if isinstance(item, Mapping):
        return item.get(name, default)
    return getattr(item, name, default)


def _iso_date(value) -> str:
    if isinstance(value, date):
        return value.isoformat()
    parsed = date.fromisoformat(str(value))
    return parsed.isoformat()


def _issue(code: str, path: str, message: str = "") -> TermIssue:
    return TermIssue(code, "term", path, message or code)


def _next_obligation_id(opened: str, used_ids: Sequence[str] = ()) -> str:
    prefix = f"term-review-{opened.replace('-', '')}-"
    used = {
        int(value.removeprefix(prefix))
        for value in used_ids
        if value.startswith(prefix) and value.removeprefix(prefix).isdigit()
    }
    for sequence in range(1, 1000):
        if sequence not in used:
            return f"{prefix}{sequence:03d}"
    raise ValueError(f"TERM_OBLIGATION_ID_EXHAUSTED {opened}")


def open_term_obligation(
        trigger_kind: str,
        trigger_id: str,
        targets: Sequence[object],
        opened: str,
        decision: Optional[str],
) -> TermObligation:
    opened_value = _iso_date(opened)
    if trigger_kind not in TRIGGER_KINDS:
        raise ValueError(f"TERM_TRIGGER_KIND_INVALID {trigger_kind}")
    if not trigger_id:
        raise ValueError("TERM_TRIGGER_ID_MISSING")
    if not targets:
        raise ValueError("TERM_OBLIGATION_TARGETS_EMPTY")
    for index, target in enumerate(targets):
        if _value(target, "kind") not in TARGET_KINDS:
            raise ValueError(f"TERM_TARGET_KIND_INVALID targets[{index}]")
        if not _value(target, "id") or not _value(target, "field_path"):
            raise ValueError(f"TERM_TARGET_IDENTITY_MISSING targets[{index}]")
    linked_terms = tuple(
        _value(target, "id") for target in targets
        if _value(target, "kind") == "term"
    )
    history = ({
        "date": opened_value,
        "event": "opened",
        "decision": decision,
        "reason": f"{trigger_kind} event",
        "from_value": None,
        "to_value": "open",
        "linked_terms": linked_terms,
    },)
    return TermObligation(
        id=_next_obligation_id(opened_value),
        targets=tuple(targets),
        trigger=TermTrigger(trigger_kind, trigger_id, None),
        state="open",
        opened=opened_value,
        closed=None,
        decision=decision,
        history=history,
    )


def history_prefix(before, after):
    return tuple(after[:len(before)]) == tuple(before)


def _periodic_paths(value, path=""):
    paths = []
    if isinstance(value, Mapping):
        for key, nested in value.items():
            child = f"{path}.{key}" if path else str(key)
            if key in PERIODIC_POLICY_FIELDS:
                paths.append(child)
            paths.extend(_periodic_paths(nested, child))
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            paths.extend(_periodic_paths(nested, f"{path}[{index}]"))
    return paths


def _decision_references(obligation):
    references = []
    if _value(obligation, "decision"):
        references.append(("decision", _value(obligation, "decision")))
    for index, target in enumerate(_value(obligation, "targets", ())):
        if _value(target, "decision"):
            references.append((f"targets[{index}].decision", _value(target, "decision")))
    for index, event in enumerate(_value(obligation, "history", ())):
        if _value(event, "decision"):
            references.append((f"history[{index}].decision", _value(event, "decision")))
    return references


def _resolution_issues(current):
    issues = []
    opened = _value(current, "opened")
    closed = _value(current, "closed")
    if not closed:
        issues.append(_issue("TERM_OBLIGATION_CLOSED_MISSING", "closed"))
    else:
        try:
            if date.fromisoformat(str(closed)) < date.fromisoformat(str(opened)):
                issues.append(_issue(
                    "TERM_OBLIGATION_CLOSED_BEFORE_OPENED", "closed"
                ))
        except ValueError:
            issues.append(_issue("TERM_OBLIGATION_DATE_INVALID", "closed"))
    for index, target in enumerate(_value(current, "targets", ())):
        if not _value(target, "conclusion") or not _value(target, "reviewed"):
            issues.append(_issue(
                "TERM_OBLIGATION_TARGET_INCOMPLETE", f"targets[{index}]"
            ))
    return issues


def validate_obligation_transition(
        previous: TermObligation,
        current: TermObligation,
        decisions: FrozenSet[str],
) -> List[TermIssue]:
    issues = [
        _issue("TERM_PERIODIC_POLICY_NOT_APPROVED", path)
        for path in _periodic_paths(current)
    ]
    previous_id = _value(previous, "id")
    current_id = _value(current, "id")
    same_identity = previous_id == current_id
    previous_state = _value(previous, "state")
    current_state = _value(current, "state")
    previous_decision = _value(previous, "decision")
    current_decision = _value(current, "decision")

    if same_identity:
        if previous_state == "resolved" and current_state != "resolved":
            issues.append(_issue("TERM_OBLIGATION_REOPENED", "state"))
        if previous_decision != current_decision:
            issues.append(_issue(
                "TERM_OBLIGATION_REPLACEMENT_REQUIRED", "decision"
            ))
        if not history_prefix(
                _value(previous, "history", ()), _value(current, "history", ())
        ):
            issues.append(_issue(
                "TERM_OBLIGATION_HISTORY_NOT_APPEND_ONLY", "history"
            ))
    else:
        prior = _value(_value(current, "trigger", {}), "previous_obligation")
        if prior != previous_id:
            issues.append(_issue(
                "TERM_OBLIGATION_PREVIOUS_MISSING", "trigger.previous_obligation"
            ))
        if previous_state != "resolved":
            issues.append(_issue(
                "TERM_OBLIGATION_PREVIOUS_OPEN", "trigger.previous_obligation"
            ))
        if previous_decision == current_decision:
            issues.append(_issue(
                "TERM_OBLIGATION_REPLACEMENT_TRIGGER_MISSING", "trigger"
            ))

    if current_state == "open" and _value(current, "closed") is not None:
        issues.append(_issue("TERM_OBLIGATION_OPEN_HAS_CLOSED", "closed"))
    elif current_state == "resolved":
        issues.extend(_resolution_issues(current))
    elif current_state != "open":
        issues.append(_issue("TERM_OBLIGATION_STATE_INVALID", "state"))

    for path, decision_id in _decision_references(current):
        if decision_id not in decisions:
            issues.append(_issue(
                "TERM_DECISION_MISSING", path, f"TERM_DECISION_MISSING {decision_id}"
            ))
    return sorted(issues, key=lambda item: (item.path, item.code, item.message))


def obligation_index(value):
    periodic = _periodic_paths(value)
    if periodic:
        raise ValueError(f"TERM_PERIODIC_POLICY_NOT_APPROVED {periodic[0]}")
    result = {}
    for obligation in _value(value, "obligations", ()):
        obligation_id = _value(obligation, "id")
        if obligation_id in result:
            raise ValueError(f"TERM_OBLIGATION_DUPLICATE {obligation_id}")
        result[obligation_id] = obligation
    return result


def decision_index(root: Path):
    result = {}
    directory = root / "docs/decisions"
    if not directory.exists():
        return result
    for path in sorted(directory.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "---":
            continue
        try:
            end = lines.index("---", 1)
        except ValueError:
            continue
        decision_id = next((
            line.split(":", 1)[1].strip()
            for line in lines[1:end] if line.startswith("id:")
        ), None)
        if not decision_id:
            continue
        if decision_id in result:
            raise ValueError(f"TERM_DECISION_DUPLICATE {decision_id}")
        result[decision_id] = path.relative_to(root).as_posix()
    return result


def _index_entry(target_kind, target_id, reference_kind, file, record,
                 field_path, state):
    return {
        "target_kind": str(target_kind),
        "target_id": str(target_id),
        "reference_kind": str(reference_kind),
        "file": str(file),
        "record": str(record),
        "field_path": str(field_path),
        "state": str(state),
    }


def _decision_paths(decisions):
    if isinstance(decisions, Mapping):
        return {str(key): str(value) for key, value in decisions.items()}
    return {str(value): "docs/decisions" for value in decisions}


def build_term_reference_index(document, obligations, decisions):
    entries = []
    decision_paths = _decision_paths(decisions)
    states = {}
    concepts = _value(document, "concepts", ())

    for concept_index, concept in enumerate(concepts):
        concept_id = _value(concept, "id")
        concept_state = _value(concept, "workflow", "unknown")
        concept_record = f"concept:{concept_id}"
        states[("concept", concept_id)] = concept_state
        entries.append(_index_entry(
            "concept", concept_id, "self", "data/vocab/terms.yaml",
            concept_record, "id", concept_state,
        ))
        for language_index, language in enumerate(_value(concept, "languages", ())):
            for term_index, term in enumerate(_value(language, "terms", ())):
                term_id = _value(term, "id")
                term_state = _value(term, "administrative_status", "unknown")
                term_record = f"term:{term_id}"
                states[("term", term_id)] = term_state
                term_path = f"languages[{language_index}].terms[{term_index}]"
                entries.extend((
                    _index_entry(
                        "term", term_id, "self", "data/vocab/terms.yaml",
                        term_record, "id", term_state,
                    ),
                    _index_entry(
                        "concept", concept_id, "term.concept", "data/vocab/terms.yaml",
                        term_record, "concept", term_state,
                    ),
                    _index_entry(
                        "term", term_id, "concept.term", "data/vocab/terms.yaml",
                        concept_record, term_path, concept_state,
                    ),
                ))
                for history_index, event in enumerate(_value(term, "history", ())):
                    decision_id = _value(event, "decision")
                    if decision_id:
                        entries.extend(_decision_relation(
                            "term", term_id, term_state, term_record,
                            f"history[{history_index}].decision",
                            decision_id, decision_paths,
                        ))
        for history_index, event in enumerate(_value(concept, "history", ())):
            decision_id = _value(event, "decision")
            if decision_id:
                entries.extend(_decision_relation(
                    "concept", concept_id, concept_state, concept_record,
                    f"history[{history_index}].decision", decision_id,
                    decision_paths,
                ))

    for delegation in _value(document, "delegations", ()):
        delegation_id = _value(delegation, "id")
        state = _value(delegation, "state", "unknown")
        file = _value(delegation, "file", "data/vocab/topics.yaml")
        record = _value(delegation, "record", delegation_id)
        field_path = _value(delegation, "field_path", "term_concept")
        concept_id = _value(delegation, "concept")
        states[("delegation", delegation_id)] = state
        entries.append(_index_entry(
            "delegation", delegation_id, "self", file, record, field_path, state
        ))
        if concept_id:
            entries.extend((
                _index_entry(
                    "concept", concept_id, "delegation.concept", file, record,
                    f"{field_path}.concept", state,
                ),
                _index_entry(
                    "delegation", delegation_id, "concept.delegation",
                    "data/vocab/terms.yaml", f"concept:{concept_id}", "delegations",
                    states.get(("concept", concept_id), "unknown"),
                ),
            ))
        decision_id = _value(delegation, "decision")
        if decision_id:
            entries.extend(_decision_relation(
                "delegation", delegation_id, state, record,
                f"{field_path}.decision", decision_id, decision_paths, file,
            ))

    indexed_obligations = obligation_index(obligations)
    for obligation_id, obligation in indexed_obligations.items():
        state = _value(obligation, "state", "unknown")
        record = f"obligation:{obligation_id}"
        states[("obligation", obligation_id)] = state
        entries.append(_index_entry(
            "obligation", obligation_id, "self", "data/vocab/term-obligations.yaml",
            record, "id", state,
        ))
        for target_index, target in enumerate(_value(obligation, "targets", ())):
            target_kind = _value(target, "kind")
            target_id = _value(target, "id")
            if target_kind not in TARGET_KINDS:
                continue
            entries.extend((
                _index_entry(
                    target_kind, target_id, "obligation.target",
                    "data/vocab/term-obligations.yaml", record,
                    f"targets[{target_index}].id", state,
                ),
                _index_entry(
                    "obligation", obligation_id, f"{target_kind}.obligation",
                    _target_file(target_kind, target_id),
                    f"{target_kind}:{target_id}", "obligations",
                    states.get((target_kind, target_id), state),
                ),
            ))
        trigger = _value(obligation, "trigger", {})
        previous_id = _value(trigger, "previous_obligation")
        if previous_id:
            entries.extend((
                _index_entry(
                    "obligation", previous_id, "obligation.previous",
                    "data/vocab/term-obligations.yaml", record,
                    "trigger.previous_obligation", state,
                ),
                _index_entry(
                    "obligation", obligation_id, "obligation.next",
                    "data/vocab/term-obligations.yaml",
                    f"obligation:{previous_id}", "next_obligation", state,
                ),
            ))
        for path, decision_id in _decision_references(obligation):
            entries.extend(_decision_relation(
                "obligation", obligation_id, state, record, path,
                decision_id, decision_paths, "data/vocab/term-obligations.yaml",
            ))

    for output in _value(document, "generated_outputs", ()):
        output_id = _value(output, "id")
        state = _value(output, "state", "unknown")
        states[("generated_output", output_id)] = state
        record = f"generated_output:{output_id}"
        entries.append(_index_entry(
            "generated_output", output_id, "self", output_id, record, "id", state
        ))
        for index, concept_id in enumerate(_value(output, "concepts", ())):
            entries.extend((
                _index_entry(
                    "concept", concept_id, "generated_output.concept", output_id,
                    record, f"concepts[{index}]", state,
                ),
                _index_entry(
                    "generated_output", output_id, "concept.generated_output",
                    "data/vocab/terms.yaml", f"concept:{concept_id}",
                    "generated_outputs", states.get(("concept", concept_id), "unknown"),
                ),
            ))

    for decision_id, path in decision_paths.items():
        entries.append(_index_entry(
            "decision", decision_id, "self", path,
            f"decision:{decision_id}", "id", "accepted",
        ))

    unique = {
        tuple(row[key] for key in (
            "target_kind", "target_id", "reference_kind", "file", "record",
            "field_path", "state",
        )): row
        for row in entries
    }
    return {
        "schema": "urn:kb-design:data:term-reference-index",
        "version": 1,
        "entries": [unique[key] for key in sorted(unique)],
    }


def _decision_relation(kind, identity, state, record, field_path, decision_id,
                       decision_paths, file="data/vocab/terms.yaml"):
    decision_file = decision_paths.get(decision_id, "docs/decisions")
    return (
        _index_entry(
            "decision", decision_id, f"{kind}.decision", file, record,
            field_path, state,
        ),
        _index_entry(
            kind, identity, f"decision.{kind}", decision_file,
            f"decision:{decision_id}", "targets", "accepted",
        ),
    )


def _target_file(kind, identity):
    if kind == "obligation":
        return "data/vocab/term-obligations.yaml"
    if kind == "decision":
        return "docs/decisions"
    if kind == "generated_output":
        return identity
    return "data/vocab/terms.yaml"
