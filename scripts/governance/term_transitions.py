from collections import defaultdict

from scripts.governance.term_model import TermIssue


CONCEPT_TRANSITIONS = {
    (None, "candidate"),
    ("candidate", "active"),
    ("active", "deprecated"),
    ("deprecated", "active"),
}

TERM_TRANSITIONS = {
    (None, "preferredTerm-admn-sts"),
    (None, "admittedTerm-admn-sts"),
    (None, "deprecatedTerm-admn-sts"),
    (None, "supersededTerm-admn-sts"),
    ("preferredTerm-admn-sts", "admittedTerm-admn-sts"),
    ("preferredTerm-admn-sts", "deprecatedTerm-admn-sts"),
    ("preferredTerm-admn-sts", "supersededTerm-admn-sts"),
    ("admittedTerm-admn-sts", "preferredTerm-admn-sts"),
    ("admittedTerm-admn-sts", "deprecatedTerm-admn-sts"),
    ("admittedTerm-admn-sts", "supersededTerm-admn-sts"),
    ("deprecatedTerm-admn-sts", "preferredTerm-admn-sts"),
    ("deprecatedTerm-admn-sts", "admittedTerm-admn-sts"),
    ("deprecatedTerm-admn-sts", "supersededTerm-admn-sts"),
    ("supersededTerm-admn-sts", "preferredTerm-admn-sts"),
    ("supersededTerm-admn-sts", "admittedTerm-admn-sts"),
    ("supersededTerm-admn-sts", "deprecatedTerm-admn-sts"),
}

RESTORED_FROM = {"deprecatedTerm-admn-sts", "supersededTerm-admn-sts"}
RESTORED_TO = {"preferredTerm-admn-sts", "admittedTerm-admn-sts"}
USABLE_REPLACEMENTS = {"preferredTerm-admn-sts", "admittedTerm-admn-sts"}


def index_terms(document):
    result = {}
    for concept in document.concepts:
        for language in concept.languages:
            for term in language.terms:
                result[term.id] = (concept.id, language.language, term)
    return result


def history_is_prefix(before, after):
    return tuple(after[:len(before)]) == tuple(before)


def replacement_cycles(document):
    terms = index_terms(document)
    edges = {
        term_id: term.replaced_by
        for term_id, (_, _, term) in terms.items()
        if term.replaced_by is not None
    }
    cycles = []
    visiting = []
    visited = set()

    def visit(term_id):
        if term_id in visiting:
            start = visiting.index(term_id)
            cycles.append(tuple(visiting[start:] + [term_id]))
            return
        if term_id in visited:
            return
        visiting.append(term_id)
        target = edges.get(term_id)
        if target in edges:
            visit(target)
        visiting.pop()
        visited.add(term_id)

    for term_id in sorted(edges):
        visit(term_id)
    return tuple(cycles)


def _issue(code, path, message):
    return TermIssue(code, "term", path, message)


def _language_groups(document):
    return {
        (concept.id, language.language): language
        for concept in document.concepts
        for language in concept.languages
    }


def _preferred_ids(language):
    return {
        term.id for term in language.terms
        if term.administrative_status == "preferredTerm-admn-sts"
    }


def _new_events(before, after):
    return tuple(after[len(before):])


def _validate_history(before, after, path, decisions, issues):
    if not history_is_prefix(before, after):
        issues.append(_issue(
            "TERM_HISTORY_NOT_APPEND_ONLY", path, "history is not append-only",
        ))
        return ()
    events = _new_events(before, after)
    for index, event in enumerate(events, start=len(before)):
        if event.decision not in decisions:
            issues.append(_issue(
                "TERM_DECISION_MISSING",
                f"{path}[{index}].decision",
                f"unresolved transition decision {event.decision}",
            ))
        if event.from_value == event.to_value:
            issues.append(_issue(
                "TERM_TRANSITION_NOOP",
                f"{path}[{index}]",
                "a state transition cannot keep the same state",
            ))
    return events


def _validate_concepts(previous, current, decisions, issues):
    previous_by_id = {concept.id: concept for concept in previous.concepts}
    for concept_index, concept in enumerate(current.concepts):
        old = previous_by_id.get(concept.id)
        before_history = () if old is None else old.history
        events = _validate_history(
            before_history,
            concept.history,
            f"concepts[{concept_index}].history",
            decisions,
            issues,
        )
        before_status = None if old is None else old.workflow
        if before_status == concept.workflow:
            continue
        if (before_status, concept.workflow) not in CONCEPT_TRANSITIONS:
            issues.append(_issue(
                "TERM_CONCEPT_TRANSITION_INVALID",
                f"concepts[{concept_index}].workflow",
                f"invalid concept transition {before_status} -> {concept.workflow}",
            ))
        if not events or (
            events[-1].from_value != before_status
            or events[-1].to_value != concept.workflow
        ):
            issues.append(_issue(
                "TERM_TRANSITION_HISTORY",
                f"concepts[{concept_index}].history",
                "concept transition lacks a matching history event",
            ))


def _validate_terms(previous, current, decisions, issues):
    previous_terms = index_terms(previous)
    current_terms = index_terms(current)
    changed_by_language = defaultdict(set)

    for term_id, (concept_id, language, term) in current_terms.items():
        old_entry = previous_terms.get(term_id)
        old_term = None if old_entry is None else old_entry[2]
        before_history = () if old_term is None else old_term.history
        events = _validate_history(
            before_history,
            term.history,
            f"terms[{term_id}].history",
            decisions,
            issues,
        )
        before_status = None if old_term is None else old_term.administrative_status
        after_status = term.administrative_status
        if before_status == after_status:
            continue
        changed_by_language[(concept_id, language)].add(term_id)
        if (before_status, after_status) not in TERM_TRANSITIONS:
            issues.append(_issue(
                "TERM_TRANSITION_INVALID",
                f"terms[{term_id}].administrative_status",
                f"invalid term transition {before_status} -> {after_status}",
            ))
        if not events or (
            events[-1].from_value != before_status
            or events[-1].to_value != after_status
        ):
            issues.append(_issue(
                "TERM_TRANSITION_HISTORY",
                f"terms[{term_id}].history",
                "term transition lacks a matching history event",
            ))
        if (
            before_status in RESTORED_FROM
            and after_status in RESTORED_TO
            and events
            and events[-1].decision in {event.decision for event in before_history}
        ):
            issues.append(_issue(
                "TERM_RESTORATION_REVIEW",
                f"terms[{term_id}].history",
                "restoration must use a new admission decision",
            ))

    previous_groups = _language_groups(previous)
    current_groups = _language_groups(current)
    all_groups = sorted(set(previous_groups) | set(current_groups))
    for concept_id, language in all_groups:
        before = previous_groups.get((concept_id, language))
        after = current_groups.get((concept_id, language))
        before_preferred = set() if before is None else _preferred_ids(before)
        after_preferred = set() if after is None else _preferred_ids(after)
        group_path = f"concepts[{concept_id}].languages[{language}]"
        if len(before_preferred) != 1 or len(after_preferred) != 1:
            issues.append(_issue(
                "TERM_PREFERRED_COUNT",
                group_path,
                "each snapshot must contain exactly one preferred term",
            ))
        if before_preferred != after_preferred:
            changed = changed_by_language[(concept_id, language)]
            linked = set()
            for term_id in changed:
                current_term = current_terms.get(term_id)
                if current_term is not None:
                    old_term = previous_terms.get(term_id)
                    old_history = () if old_term is None else old_term[2].history
                    for event in _new_events(old_history, current_term[2].history):
                        linked.update(event.linked_terms)
            required = before_preferred | after_preferred
            if (
                len(before_preferred) != 1
                or len(after_preferred) != 1
                or not required <= changed
                or not changed <= linked
            ):
                issues.append(_issue(
                    "TERM_ATOMIC_LANGUAGE_CHANGE",
                    group_path,
                    "preferred-term changes must include every linked term atomically",
                ))


def _validate_replacements(current, issues):
    terms = index_terms(current)
    for term_id, (concept_id, language, term) in terms.items():
        path = f"terms[{term_id}].replaced_by"
        if term.administrative_status != "supersededTerm-admn-sts":
            if term.replaced_by is not None:
                issues.append(_issue(
                    "TERM_REPLACEMENT_STATE", path,
                    "only superseded terms may have a replacement",
                ))
            continue
        target_entry = terms.get(term.replaced_by)
        if target_entry is None:
            issues.append(_issue(
                "TERM_REPLACEMENT_MISSING", path,
                f"replacement target does not exist: {term.replaced_by}",
            ))
            continue
        target_concept, target_language, target = target_entry
        if (target_concept, target_language) != (concept_id, language):
            issues.append(_issue(
                "TERM_REPLACEMENT_LANGUAGE", path,
                "replacement must stay in the same concept and language",
            ))
        if target.administrative_status not in USABLE_REPLACEMENTS:
            issues.append(_issue(
                "TERM_REPLACEMENT_TARGET_STATUS", path,
                "replacement target must be preferred or admitted",
            ))
    for cycle in replacement_cycles(current):
        issues.append(_issue(
            "TERM_REPLACEMENT_CYCLE",
            f"terms[{cycle[0]}].replaced_by",
            "replacement cycle: " + " -> ".join(cycle),
        ))


def validate_transition(previous, current, decisions):
    issues = []
    _validate_concepts(previous, current, decisions, issues)
    _validate_terms(previous, current, decisions, issues)
    _validate_replacements(current, issues)
    return tuple(sorted(issues, key=lambda issue: (
        issue.path, issue.code, issue.message,
    )))
