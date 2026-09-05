#!/usr/bin/env python3
from kb_core.repository import project_root
import argparse
import calendar
import copy
import json
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Literal, NamedTuple, Optional, Sequence

import yaml


ReferenceKind = Literal["basis", "source", "match", "external_group"]

SCHEMA_IDS = {
    "source-entities.schema.json": "urn:kb-design:schema:source-entities:2",
    "source-uses.schema.json": "urn:kb-design:schema:source-uses:2",
    "source-obligations.schema.json": "urn:kb-design:schema:source-obligations:1",
    "source-reference-index.schema.json": "urn:kb-design:schema:source-reference-index:1",
    "source-probe.schema.json": "urn:kb-design:schema:source-probe:1",
    "source-migration.schema.json": "urn:kb-design:schema:source-migration:1",
    "decision.schema.json": "urn:kb-design:schema:decision:1",
}

ROLE_QUALIFICATIONS = {
    "basis": None,
    "source": "structure",
    "match": "mapping",
    "external_group": "structure",
}

ERROR_CODES = (
    "SOURCE_SCHEMA_INVALID",
    "SOURCE_REFERENCE_KIND_INVALID",
    "SOURCE_REFERENCE_VALUE_INVALID",
    "SOURCE_ENTITY_MISSING",
    "SOURCE_USE_MISSING",
    "SOURCE_ROLE_NOT_APPROVED",
    "SOURCE_ROLE_DECISION_MISSING",
    "SOURCE_BASIS_LOCATOR_MISSING",
    "SOURCE_BASIS_CHECKED_MISSING",
    "SOURCE_SOURCE_ITEM_MISSING",
    "SOURCE_SOURCE_LOCATOR_MISSING",
    "SOURCE_SOURCE_BASIS_MISSING",
    "SOURCE_MATCH_REL_INVALID",
    "SOURCE_MATCH_BASIS_MISSING",
    "SOURCE_STABLE_ID_CHANGED",
    "SOURCE_HISTORY_NOT_APPEND_ONLY",
    "SOURCE_OBLIGATION_REOPENED",
    "SOURCE_OBLIGATION_TARGET_MISSING",
    "SOURCE_DECISION_MISSING",
    "SOURCE_LEGACY_FIELD",
    "SOURCE_INDEX_MISMATCH",
    "SOURCE_PROBE_FORMAL_WRITE",
    "SOURCE_EXTERNAL_GROUP_ROLE_NOT_APPROVED",
    "SOURCE_CUTOVER_MANIFEST_INVALID",
    "SOURCE_DECISION_DELIVERY_MISSING",
    "SOURCE_DECISION_PATCH_CONFLICT",
)


class Issue(NamedTuple):
    code: str
    file: str
    record: str
    field_path: str
    message: str


class ReferenceUse(NamedTuple):
    kind: ReferenceKind
    file: str
    record: str
    field_path: str
    value: object


class DecisionPatch(NamedTuple):
    identity: str
    field: str
    value: object
    qid: str


def validate_references(root: Path,
                        references: Sequence[ReferenceUse]) -> List[Issue]:
    return validate_reference_documents(
        _load_yaml(root / "data/vocab/entities.yaml"),
        _load_yaml(root / "data/vocab/sources.yaml"), references,
        _load_accepted_decisions(root / "docs/decisions"),
    )


def validate_reference_documents(entities_document, uses_document, references,
                                 accepted_decisions):
    """Validate references against an already captured, normalized snapshot."""
    entities = {row["id"]: row for row in entities_document.get("entities", [])
                if isinstance(row, dict) and isinstance(row.get("id"), str)
                and row.get("kind") in {"standard", "publication"}}
    uses = {row["id"]: row for row in uses_document.get("sources", [])
            if isinstance(row, dict) and isinstance(row.get("id"), str)}
    accepted = accepted_decisions
    issues = []
    pending = list(references)
    for reference in pending:
        if reference.kind not in ROLE_QUALIFICATIONS:
            issues.append(_issue(reference, "SOURCE_REFERENCE_KIND_INVALID"))
            continue
        structural = _validate_reference_value(reference.kind, reference.value)
        if structural:
            issues.extend(_issue(reference, code) for code in structural)
            continue
        if reference.kind == "basis":
            entity = entities.get(reference.value["entity"])
            if entity is None:
                issues.append(_issue(reference, "SOURCE_ENTITY_MISSING"))
                continue
            if _content_is_mutable(entity) and not reference.value.get("checked"):
                issues.append(_issue(reference, "SOURCE_BASIS_CHECKED_MISSING"))
            continue
        registry = reference.value["registry"]
        source_use = uses.get(registry)
        if source_use is None:
            issues.append(_issue(reference, "SOURCE_USE_MISSING"))
            continue
        role_name = ROLE_QUALIFICATIONS[reference.kind]
        role = next((row for row in source_use.get("roles", [])
                     if isinstance(row, dict) and row.get("role") == role_name), None)
        role_code = ("SOURCE_EXTERNAL_GROUP_ROLE_NOT_APPROVED"
                     if reference.kind == "external_group" else "SOURCE_ROLE_NOT_APPROVED")
        if role is None or role.get("status") != "approved":
            issues.append(_issue(reference, role_code))
        elif not role_is_authorized(accepted, source_use, role):
            issues.append(_issue(reference, "SOURCE_ROLE_DECISION_MISSING"))
        entity = entities.get(source_use.get("entity"), {})
        if entity.get("tier") == "archival":
            issues.append(_issue(reference, role_code, "archival source cannot be registered for source uses"))
        elif role_name == "structure" and role is not None and role.get("status") == "approved":
            qualification = dependent_role_qualification_error(entity, source_use, accepted, "structure")
            if qualification:
                issues.append(_issue(reference, role_code, qualification))
        for index, basis in enumerate(reference.value["basis"]):
            nested = ReferenceUse(
                "basis", reference.file, reference.record,
                f"{reference.field_path}.basis[{index}]", basis,
            )
            pending.append(nested)
    return _sort_issues(set(issues))


def normalize_yaml_dates(value):
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: normalize_yaml_dates(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_yaml_dates(item) for item in value]
    return value


def _load_yaml(path: Path):
    if not path.exists():
        return {}
    return normalize_yaml_dates(yaml.safe_load(path.read_text(encoding="utf-8")) or {})


def _load_source_entities(path: Path):
    document = _load_yaml(path)
    return {
        row["id"]: row for row in document.get("entities", [])
        if isinstance(row, dict) and isinstance(row.get("id"), str) and row.get("kind") in {"standard", "publication"}
    }


def _load_source_uses(path: Path):
    return {row["id"]: row for row in _load_yaml(path).get("sources", [])
            if isinstance(row, dict) and isinstance(row.get("id"), str)}


def _front_matter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return None
    return normalize_yaml_dates(yaml.safe_load(text.split("---\n", 2)[1]))


def _load_accepted_decisions(directory: Path):
    return accepted_decisions_from_documents(
        [_front_matter(path) for path in sorted(directory.glob("source-*.md"))]
    )


def accepted_decisions_from_documents(frontmatters):
    """Select schema-valid, unique, effective decisions from captured metadata."""
    from jsonschema import Draft202012Validator, FormatChecker
    validator = Draft202012Validator(build_schema_documents()["decision.schema.json"],
                                     format_checker=FormatChecker())
    documents = {}
    for value in frontmatters:
        front = normalize_yaml_dates(value)
        if isinstance(front, dict) and front.get("status") == "accepted" and validator.is_valid(front):
            documents.setdefault(front["id"], []).append(front)
    accepted = {key: values[0] for key, values in documents.items() if len(values) == 1}
    superseded = {key for front in accepted.values() for key in front.get("supersedes", [])}
    return {key: value for key, value in accepted.items() if key not in superseded}


def _load_accepted_decision_ids(directory: Path):
    return set(_load_accepted_decisions(directory))


def decision_authorizes(decisions, decision_id, identity, field, value):
    front = decisions.get(decision_id, {})
    return any(patch.get("identity") == identity and patch.get("field") == field
               and patch.get("value") == value
               for answer in front.get("answers", []) for patch in answer.get("patches", []))


def role_is_authorized(decisions, source_use, role):
    return decision_authorizes(decisions, role.get("decision"),
                               f"sources/{source_use['id']}", "entity", source_use.get("entity")) and decision_authorizes(decisions, role.get("decision"),
                               f"sources/{source_use['id']}/roles/{role['role']}",
                               "status", role.get("status"))


def dependent_role_qualification_error(entity, source_use, accepted, role_name):
    mapping = next((role for role in source_use.get("roles", [])
                    if isinstance(role, dict) and role.get("role") == "mapping"), None)
    if not mapping or mapping.get("status") != "approved" or not role_is_authorized(accepted, source_use, mapping):
        return f"approved {role_name} requires an independently authorized approved mapping role"
    if role_name == "group":
        return None
    tier = entity.get("tier")
    if tier != "de-jure" and not (tier == "de-facto" and isinstance(entity.get("version"), str) and entity["version"].strip()):
        return "structure requires de-jure or versioned de-facto source"
    return None


def _issue(reference: ReferenceUse, code: str, message: str = ""):
    return Issue(code, reference.file, reference.record, reference.field_path, message or code)


def _sort_issues(issues):
    return sorted(issues, key=lambda item: (
        item.file, item.record, item.field_path, item.code, item.message,
    ))


def _validate_reference_value(kind, value):
    if not isinstance(value, dict):
        return ["SOURCE_REFERENCE_VALUE_INVALID"]
    allowed = {"entity", "locator", "checked"} if kind == "basis" else (
        {"registry", "item", "rel", "basis"} if kind == "match"
        else {"registry", "item", "locator", "basis"}
    )
    if set(value) - allowed:
        return ["SOURCE_REFERENCE_VALUE_INVALID"]
    if any(key in value and not isinstance(value[key], str)
           for key in ("entity", "registry", "item", "locator", "rel")):
        return ["SOURCE_REFERENCE_VALUE_INVALID"]
    if "basis" in value and not isinstance(value["basis"], list):
        return ["SOURCE_REFERENCE_VALUE_INVALID"]
    if "checked" in value:
        try:
            date.fromisoformat(value["checked"])
        except (TypeError, ValueError):
            return ["SOURCE_REFERENCE_VALUE_INVALID"]
    if kind == "basis":
        if not value.get("locator"):
            return ["SOURCE_BASIS_LOCATOR_MISSING"]
        if not value.get("entity"):
            return ["SOURCE_REFERENCE_VALUE_INVALID"]
        return []
    if not value.get("registry"):
        return ["SOURCE_REFERENCE_VALUE_INVALID"]
    issues = []
    if not value.get("item"):
        issues.append("SOURCE_SOURCE_ITEM_MISSING")
    if kind in {"source", "external_group"} and not value.get("locator"):
        issues.append("SOURCE_SOURCE_LOCATOR_MISSING")
    if not value.get("basis"):
        issues.append("SOURCE_MATCH_BASIS_MISSING" if kind == "match"
                      else "SOURCE_SOURCE_BASIS_MISSING")
    if kind == "match" and value.get("rel") not in {
        "exactMatch", "closeMatch", "broadMatch", "narrowMatch", "relatedMatch",
    }:
        issues.append("SOURCE_MATCH_REL_INVALID")
    return issues


def _content_is_mutable(entity):
    return not (isinstance(entity.get("fixed_sha256"), str)
                and re.fullmatch(r"[0-9a-f]{64}", entity["fixed_sha256"])
                and isinstance(entity.get("version"), str) and entity["version"].strip())


def add_calendar_months(value: date, months: int) -> date:
    absolute = value.year * 12 + value.month - 1 + months
    year, month0 = divmod(absolute, 12)
    month = month0 + 1
    old_last = calendar.monthrange(value.year, value.month)[1]
    new_last = calendar.monthrange(year, month)[1]
    day = new_last if value.day == old_last else min(value.day, new_last)
    return date(year, month, day)


def compute_next_due(checked: date, interval_months: Optional[int]) -> Optional[date]:
    return None if interval_months is None else add_calendar_months(checked, interval_months)


def is_review_overdue(next_due: Optional[date], today: date,
                      grace_days: int = 30) -> bool:
    return next_due is not None and today > next_due + timedelta(days=grace_days)


def _unique_obligation(document: Dict[str, object],
                       obligation_id: str) -> Dict[str, object]:
    matches = [row for row in document.get("obligations", [])
               if row.get("id") == obligation_id]
    if len(matches) != 1:
        raise ValueError("obligation id is missing or not unique")
    return matches[0]


def _latest_resolved(document: Dict[str, object], entity: str,
                     trigger: str) -> Optional[str]:
    for row in reversed(document.get("obligations", [])):
        if (row.get("entity") == entity and row.get("trigger") == trigger
                and row.get("state") == "resolved"):
            return row["id"]
    return None


def _active_same_trigger(document: Dict[str, object], entity: str,
                         trigger: str) -> bool:
    return any(row.get("entity") == entity and row.get("trigger") == trigger
               and row.get("state") == "open"
               for row in document.get("obligations", []))


def _target_key(target: Dict[str, str]) -> str:
    return ":".join(target[field] for field in ("file", "record", "field_path"))


def _require_all_target_conclusions(targets: Sequence[Dict[str, str]],
                                    conclusions: Dict[str, object]) -> None:
    expected = {_target_key(target) for target in targets}
    if set(conclusions) != expected:
        raise ValueError("target conclusions must cover every target exactly")


def _stable_union(left: Sequence[str], right: Sequence[str]) -> List[str]:
    result = list(left)
    result.extend(value for value in right if value not in result)
    return result


def _require_required_decisions(conclusions: Dict[str, object],
                                decisions: Sequence[str]) -> None:
    required = []
    for conclusion in conclusions.values():
        if not isinstance(conclusion, dict):
            raise ValueError("target conclusions must be objects")
        references = conclusion.get("decisions", [])
        if not isinstance(references, list) or not all(
                isinstance(value, str) for value in references):
            raise ValueError("target conclusion decisions must be an array of ids")
        required = _stable_union(required, references)
    missing = [value for value in required if value not in decisions]
    if missing:
        raise ValueError(f"required decisions are missing: {','.join(missing)}")


def open_obligation(document: Dict[str, object], entity: str, trigger: str,
                    targets: Sequence[Dict[str, str]], decisions: Sequence[str],
                    opened: str, obligation_id: str) -> Dict[str, object]:
    result = copy.deepcopy(document)
    if any(row.get("id") == obligation_id for row in result.get("obligations", [])):
        raise ValueError("obligation id already exists")
    if not targets:
        raise ValueError("obligation targets are required")
    if _active_same_trigger(result, entity, trigger):
        raise ValueError("same entity and trigger already has an open obligation")
    copied_targets = copy.deepcopy(list(targets))
    result["obligations"].append({
        "id": obligation_id,
        "entity": entity,
        "trigger": trigger,
        "targets": copied_targets,
        "decisions": list(decisions),
        "previous": _latest_resolved(result, entity, trigger),
        "state": "open",
        "opened": opened,
        "resolved": None,
        "history": [{
            "date": opened,
            "action": "opened",
            "trigger": trigger,
            "targets": copy.deepcopy(copied_targets),
        }],
    })
    return result


def resolve_obligation(document: Dict[str, object], obligation_id: str,
                       resolved: str, conclusions: Dict[str, object],
                       decisions: Sequence[str]) -> Dict[str, object]:
    result = copy.deepcopy(document)
    row = _unique_obligation(result, obligation_id)
    if row.get("state") != "open":
        raise ValueError("obligation is not open")
    _require_all_target_conclusions(row["targets"], conclusions)
    all_decisions = _stable_union(row["decisions"], decisions)
    _require_required_decisions(conclusions, all_decisions)
    row["state"] = "resolved"
    row["resolved"] = resolved
    row["decisions"] = all_decisions
    row["history"].append({
        "date": resolved,
        "action": "resolved",
        "conclusions": copy.deepcopy(conclusions),
        "decisions": list(decisions),
    })
    return result


def retrigger_obligation(document: Dict[str, object], previous_id: str,
                         targets: Sequence[Dict[str, str]],
                         decisions: Sequence[str], opened: str,
                         obligation_id: str) -> Dict[str, object]:
    previous = _unique_obligation(document, previous_id)
    if previous.get("state") != "resolved":
        raise ValueError("previous obligation is not resolved")
    if _latest_resolved(document, previous["entity"], previous["trigger"]) != previous_id:
        raise ValueError("previous obligation is not the latest resolved obligation")
    return open_obligation(
        document,
        previous["entity"],
        previous["trigger"],
        targets,
        decisions,
        opened,
        obligation_id,
    )


def source_obligation_term_trigger(obligation_id: str) -> Dict[str, str]:
    if not isinstance(obligation_id, str) or not obligation_id:
        raise ValueError("source obligation id is required")
    return {"kind": "source_obligation", "id": obligation_id}


META = "https://json-schema.org/draft/2020-12/schema"
ID = {"type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"}
DATE = {"type": "string", "format": "date"}
HASH = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
NONEMPTY = {"type": "string", "minLength": 1}


def _array(items, minimum=0):
    value = {"type": "array", "items": items}
    if minimum:
        value["minItems"] = minimum
    return value


def _closed(required, properties):
    return {
        "type": "object",
        "additionalProperties": False,
        "required": list(required),
        "properties": properties,
    }


BASIS_ITEM = _closed(
    ("entity", "locator"),
    {"entity": ID, "locator": NONEMPTY, "checked": DATE},
)
BASIS_LIST = _array({"$ref": "#/$defs/basisItem"}, 1)
SOURCE = _closed(
    ("registry", "item", "locator", "basis"),
    {"registry": ID, "item": NONEMPTY, "locator": NONEMPTY, "basis": BASIS_LIST},
)
MATCH = _closed(
    ("registry", "item", "rel", "basis"),
    {
        "registry": ID,
        "item": NONEMPTY,
        "rel": {"enum": [
            "exactMatch", "closeMatch", "broadMatch", "narrowMatch", "relatedMatch",
        ]},
        "basis": BASIS_LIST,
    },
)


SUBJECT_BASIS = _closed(("values", "references"), {
    "values": {**_array(ID, 1), "uniqueItems": True}, "references": _array(BASIS_ITEM, 1),
})
PROJECT_ASSERTION = _closed(("disposition", "original", "migration"), {
    "disposition": {"const": "project_assertion"}, "original": {"const": "self"},
    "migration": NONEMPTY,
})
SUBJECT_ASSERTION = copy.deepcopy(PROJECT_ASSERTION)
SUBJECT_ASSERTION["required"].append("values")
SUBJECT_ASSERTION["properties"]["values"] = {**_array(ID, 1), "uniqueItems": True}
ASSERTIONS = _closed((), {"subjects": _array(SUBJECT_ASSERTION, 1), "source": PROJECT_ASSERTION})
ASSERTIONS["minProperties"] = 1
LOCAL_ANALYSIS = _closed(("legacy_source_label", "state", "decision"), {
    "legacy_source_label": NONEMPTY, "state": {"const": "isolated"}, "decision": ID,
})
LOCAL_ANALYSIS_POLICY = {"form_arrays": "isolated-local-analysis", "source_reference": False,
                         "members_unchanged": True}
LANGUAGE_BASIS = {"oneOf": [
    _closed(("legacy",), {"legacy": NONEMPTY}),
    _closed(("level", "references"), {"level": {"enum": [1, 2, 3, 4]},
        "references": _array(_closed(("source", "locator"), {"source": ID, "locator": NONEMPTY}), 1)}),
    _closed(("level", "model"), {"level": {"const": 5}, "model": _closed(
        ("name", "date", "rationale", "approval"),
        {"name": NONEMPTY, "date": DATE, "rationale": NONEMPTY, "approval": NONEMPTY})}),
    _closed(("level", "reason"), {"level": {"const": 6}, "reason": NONEMPTY}),
]}


def _base_schema(name, definitions=None):
    value = {"$schema": META, "$id": SCHEMA_IDS[name]}
    if definitions:
        value["$defs"] = definitions
    return value


def build_schema_documents() -> Dict[str, object]:
    url = _closed(
        ("role", "url", "primary"),
        {
            "role": {"enum": [
                "canonical", "landing", "doi", "full_text", "status", "mirror", "archive",
            ]},
            "url": {"type": "string", "format": "uri"},
            "primary": {"type": "boolean"},
        },
    )
    review = _closed(
        ("checked", "next_due", "interval_months", "grace_days", "obligations"),
        {
            "checked": {"oneOf": [DATE, {"type": "null"}]},
            "next_due": {"oneOf": [DATE, {"type": "null"}]},
            "interval_months": {"oneOf": [{"enum": [6, 12, 24]}, {"type": "null"}]},
            "grace_days": {"const": 30},
            "obligations": _array(ID),
        },
    )
    history = _closed(
        ("date", "action", "fields", "decisions"),
        {
            "date": DATE,
            "action": NONEMPTY,
            "fields": _array(NONEMPTY),
            "decisions": _array(ID),
            "basis": _array(BASIS_ITEM),
            "before": {},
            "after": {},
        },
    )
    entity = _closed(
        ("id", "label", "kind", "subjects", "status", "added"),
        {
            "id": ID,
            "label": {"type": "object", "minProperties": 1,
                      "additionalProperties": {"type": "string"}},
            "kind": {"enum": ["software", "programming-language", "organization", "standard", "publication", "person", "large-language-model"]},
            "version": {"oneOf": [NONEMPTY, {"type": "null"}]},
            "urls": _array(url, 1),
            "status": {"enum": ["candidate", "active", "deprecated"]},
            "source_status": {"enum": ["current", "superseded", "withdrawn"]},
            "subjects": {**_array(ID), "uniqueItems": True},
            "added": DATE,
            "tier": {"enum": ["de-jure", "de-facto", "vendor", "archival"]},
            "scope": NONEMPTY, "form": NONEMPTY, "vendor": ID,
            "creator": {**_array(ID), "uniqueItems": True},
            "alt": {"type": "object", "additionalProperties": _array(NONEMPTY)},
            "hidden": {"type": "object", "additionalProperties": _array(NONEMPTY)},
            "fixed_sha256": HASH,
            "match": _array(MATCH),
            "assertions": ASSERTIONS,
            "basis": _closed((), {
                **{field: _array(BASIS_ITEM, 1) for field in (
                    "label", "kind", "version", "urls", "tier", "scope", "form",
                    "vendor", "creator", "source_status", "replaced_by", "fixed_sha256", "watch")},
                "subjects": _array(SUBJECT_BASIS, 1),
                "zh": LANGUAGE_BASIS, "en": LANGUAGE_BASIS,
            }),
            "review": review,
            "watch": _array(_closed(("locator", "signals", "cadence_months"), {
                "locator": {"type": "string", "format": "uri"},
                "signals": {**_array({"enum": ["availability", "redirect", "version", "revision", "replacement", "withdrawal"]}, 1), "uniqueItems": True},
                "cadence_months": _closed(("availability", "redirect", "content"), {
                    "availability": {"const": 1}, "redirect": {"const": 1},
                    "content": {"enum": [1, 3, 6, 12]},
                }),
            })),
            "replaced_by": {"oneOf": [ID, {"type": "null"}]},
            "history": _array(history, 1),
        },
    )
    entity["allOf"] = [{
        "if": {"properties": {"kind": {"enum": ["standard", "publication"]}},
               "required": ["kind"]},
        "then": {"required": [
            "version", "urls", "tier", "basis", "review", "watch", "replaced_by", "history",
        ]},
    }]
    entities = _base_schema("source-entities.schema.json", {"basisItem": BASIS_ITEM})
    entities.update(_closed(
        ("schema", "schema_version", "version", "entities"),
        {
            "schema": {"const": "urn:kb-design:data:entities"},
            "schema_version": {"const": 2},
            "version": {"type": "object"},
            "entities": _array(entity, 1),
        },
    ))

    role = _closed(
        ("role", "status", "decision"),
        {
            "role": {"enum": ["mapping", "structure", "group", "discovery"]},
            "status": {"enum": ["proposed", "approved", "retired"]},
            "decision": {"oneOf": [ID, {"type": "null"}]},
        },
    )
    role["allOf"] = [
        {"if": {"properties": {"status": {"enum": ["approved", "retired"]}}},
         "then": {"properties": {"decision": ID}}},
        {"if": {"properties": {"status": {"const": "proposed"}}},
         "then": {"properties": {"decision": {"type": "null"}}}},
    ]
    use = _closed(
        ("id", "entity", "roles", "history"),
        {"id": ID, "entity": ID, "roles": _array(role, 1), "history": _array(history)},
    )
    uses = _base_schema("source-uses.schema.json")
    uses.update(_closed(
        ("schema", "schema_version", "version", "sources"),
        {
            "schema": {"const": "urn:kb-design:data:source-uses"},
            "schema_version": {"const": 2},
            "version": {"type": "object"},
            "sources": _array(use, 1),
        },
    ))

    target = _closed(
        ("kind", "file", "record", "field_path"),
        {
            "kind": {"enum": ["basis", "source", "match", "use_role", "decision", "obligation"]},
            "file": NONEMPTY,
            "record": NONEMPTY,
            "field_path": NONEMPTY,
        },
    )
    obligation = _closed(
        ("id", "entity", "trigger", "targets", "decisions", "previous", "state",
         "opened", "resolved", "history"),
        {
            "id": ID,
            "entity": ID,
            "trigger": NONEMPTY,
            "targets": _array(target, 1),
            "decisions": _array(ID),
            "previous": {"oneOf": [ID, {"type": "null"}]},
            "state": {"enum": ["open", "resolved"]},
            "opened": DATE,
            "resolved": {"oneOf": [DATE, {"type": "null"}]},
            "history": _array({"type": "object"}, 1),
        },
    )
    obligation["allOf"] = [
        {"if": {"properties": {"state": {"const": "open"}}},
         "then": {"properties": {"resolved": {"type": "null"}}}},
        {"if": {"properties": {"state": {"const": "resolved"}}},
         "then": {"properties": {"resolved": DATE}}},
    ]
    obligations = _base_schema("source-obligations.schema.json")
    obligations.update(_closed(
        ("schema", "schema_version", "obligations"),
        {
            "schema": {"const": "urn:kb-design:data:source-obligations"},
            "schema_version": {"const": 1},
            "obligations": _array(obligation),
        },
    ))

    index_entry = _closed(
        ("target_kind", "target_id", "reference_kind", "file", "record", "field_path"),
        {key: NONEMPTY for key in (
            "target_kind", "target_id", "reference_kind", "file", "record", "field_path",
        )},
    )
    index = _base_schema("source-reference-index.schema.json")
    index.update(_closed(
        ("schema", "schema_version", "entries"),
        {
            "schema": {"const": "urn:kb-design:data:source-reference-index"},
            "schema_version": {"const": 1},
            "entries": _array(index_entry),
        },
    ))

    observation = _closed(
        ("id", "observed_at", "entity", "endpoint", "request", "response", "signals",
         "previous", "errors"),
        {
            "id": ID,
            "observed_at": {"type": "string", "format": "date-time"},
            "entity": ID,
            "endpoint": {"type": "string", "format": "uri"},
            "request": _closed(("method",), {"method": {"enum": ["HEAD", "GET"]}}),
            "response": {"type": "object"},
            "signals": _array(NONEMPTY),
            "previous": {"oneOf": [ID, {"type": "null"}]},
            "errors": _array(NONEMPTY),
        },
    )
    probe = _base_schema("source-probe.schema.json")
    probe.update(_closed(
        ("schema", "schema_version", "observations"),
        {
            "schema": {"const": "urn:kb-design:data:source-probe"},
            "schema_version": {"const": 1},
            "observations": _array(observation),
        },
    ))

    dispositions = [
        "register", "merge_address", "merge_locator", "retain_legacy",
        "not_migrated_missing_locator", "no_external_basis", "project_assertion",
        "blocked_unread_material", "unresolved_external_status", "proposed_role",
        "approved_role", "retired_role", "not_in_scope", "isolated_local_analysis",
    ]
    trace = _closed(
        ("qid", "field", "value_sha256"),
        {"qid": {"pattern": "^Q(?:0[1-9]|1[0-9]|2[0-5])$"},
         "field": NONEMPTY, "value_sha256": HASH},
    )
    row = _closed(
        ("identity", "operation", "disposition", "new_value", "decision_trace", "blocks_cutover"),
        {
            "identity": NONEMPTY,
            "operation": {"enum": ["keep", "set", "delete", "isolate"]},
            "disposition": {"enum": dispositions},
            "new_value": {},
            "decision_trace": _array(trace),
            "blocks_cutover": {"type": "boolean"},
        },
    )
    payload_entry = _closed(
        ("path", "after_sha256"),
        {
            "path": {"allOf": [NONEMPTY, {"not": {"enum": [
                "build/source-cutover-payload.json",
                "build/source-cutover-handoff.json",
            ]}}]},
            "after_sha256": {"oneOf": [HASH, {"type": "null"}]},
        },
    )
    cutover = _closed(
        ("schema", "schema_version", "entries"),
        {
            "schema": {"const": "urn:kb-design:data:source-cutover-payload"},
            "schema_version": {"const": 1},
            "entries": {
                "type": "array", "minItems": 1, "uniqueItems": True,
                "items": payload_entry,
                "contains": _closed(
                    ("path", "after_sha256"),
                    {"path": {"const": "data/vocab/topics.yaml"}, "after_sha256": HASH},
                ),
            },
        },
    )
    path_hash = _closed(("path", "sha256"), {"path": NONEMPTY, "sha256": HASH})
    schema_hash = _closed(
        ("path", "$id", "schema_version", "sha256"),
        {"path": NONEMPTY, "$id": NONEMPTY,
         "schema_version": {"type": "integer", "minimum": 1}, "sha256": HASH},
    )
    source_contract = _closed(
        ("module", "sha256", "reference_kinds", "role_qualifications", "error_codes"),
        {
            "module": {"const": "packages/kb-core/src/kb_core/source_model.py"},
            "sha256": HASH,
            "reference_kinds": {"type": "array", "minItems": 4, "maxItems": 4,
                                "uniqueItems": True,
                                "items": {"enum": ["basis", "source", "match", "external_group"]}},
            "role_qualifications": _closed(
                ("basis", "source", "match", "external_group"),
                {"basis": {"type": "null"}, "source": {"const": "structure"},
                 "match": {"const": "mapping"}, "external_group": {"const": "structure"}},
            ),
            "error_codes": {"type": "array", "minItems": 26, "maxItems": 26,
                            "uniqueItems": True, "items": NONEMPTY},
        },
    )
    output = _closed(
        ("path", "kind", "sha256"),
        {"path": NONEMPTY, "kind": {"enum": ["topics", "source_index"]},
         "sha256": HASH, "concepts": {"type": "integer"}, "arrays": {"type": "integer"}},
    )
    handoff = _closed(
        ("schema", "schema_version", "payload", "source_contract", "schemas",
         "topics_sha256", "migration_ledgers", "markdown_manifest", "outputs",
         "tracked_write_set"),
        {
            "schema": {"const": "urn:kb-design:data:source-cutover-handoff"},
            "schema_version": {"const": 1},
            "payload": path_hash,
            "source_contract": source_contract,
            "schemas": {"type": "array", "minItems": 7, "maxItems": 7,
                        "uniqueItems": True, "items": schema_hash},
            "topics_sha256": HASH,
            "migration_ledgers": {"type": "array", "minItems": 6, "maxItems": 6,
                                  "uniqueItems": True, "items": path_hash},
            "markdown_manifest": _array(path_hash, 1),
            "outputs": {"type": "array", "minItems": 2, "maxItems": 2,
                        "uniqueItems": True, "items": output},
            "tracked_write_set": _array(NONEMPTY, 1),
        },
    )
    migration = _base_schema(
        "source-migration.schema.json",
        {"basisItem": BASIS_ITEM, "source": SOURCE, "match": MATCH, "row": row,
         "cutoverPayloadManifest": cutover, "sourceCutoverHandoff": handoff},
    )
    migration.update(_closed(
        ("schema", "schema_version", "rows"),
        {"schema": {"const": "urn:kb-design:data:source-migration"},
         "schema_version": {"const": 1}, "rows": _array(row)},
    ))

    patch = _closed(
        ("identity", "field", "value"),
        {"identity": NONEMPTY, "field": NONEMPTY, "value": {}},
    )
    answer = _closed(
        ("question", "resolution", "patches"),
        {"question": {"pattern": "^Q(?:0[1-9]|1[0-9]|2[0-5])$"},
         "resolution": {"enum": ["recommended", "replacement"]},
         "patches": _array(patch, 1)},
    )
    decision = _base_schema("decision.schema.json")
    decision.update(_closed(
        ("id", "schema", "schema_version", "status", "date", "level", "scope",
         "supersedes", "answers"),
        {
            "id": ID,
            "schema": {"const": "urn:kb-design:data:decision"},
            "schema_version": {"const": 1},
            "status": {"enum": ["proposed", "accepted", "superseded", "overturned"]},
            "date": DATE,
            "level": {"enum": ["L1", "L2", "L3"]},
            "scope": NONEMPTY,
            "supersedes": _array(ID),
            "answers": _array(answer, 1),
        },
    ))

    return {
        "source-entities.schema.json": entities,
        "source-uses.schema.json": uses,
        "source-obligations.schema.json": obligations,
        "source-reference-index.schema.json": index,
        "source-probe.schema.json": probe,
        "source-migration.schema.json": migration,
        "decision.schema.json": decision,
    }


def write_schema_documents(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for name, document in build_schema_documents().items():
        (directory / name).write_text(
            json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )


def load_decision_patches(paths: Sequence[Path]) -> List[DecisionPatch]:
    patches = []
    for path in paths:
        front = _front_matter(path)
        if front is None:
            raise ValueError(f"SOURCE_SCHEMA_INVALID {path}")
        if front.get("status") != "accepted":
            raise ValueError(f"SOURCE_DECISION_MISSING {path}")
        for answer in front.get("answers", []):
            qid = answer.get("question")
            for value in answer.get("patches", []):
                patches.append(DecisionPatch(
                    value["identity"], value["field"], value["value"], qid,
                ))
    return sorted(patches, key=lambda patch: (
        patch.qid, patch.identity, patch.field,
        json.dumps(patch.value, ensure_ascii=False, sort_keys=True),
    ))


def collect_reference_uses(file: Path, document: object) -> List[ReferenceUse]:
    return list(_walk_reference_uses(file, document))


def _format_reference_path(parts) -> str:
    value = ""
    for part in parts:
        value += (f"[{part}]" if isinstance(part, int)
                  else (("." if value else "") + part))
    return value


def _has_exact_keys(value, required) -> bool:
    return isinstance(value, dict) and required <= set(value)


def _walk_reference_uses(file: Path, value: object, path=(), record: str = "document"):
    """Discover constrained positions first; malformed values must not disappear.

    Historical before/after payloads and project assertions are audit data.
    Language evidence has its separately adopted validator and index visitor.
    """
    if isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_reference_uses(file, child, path + (index,), record)
    elif isinstance(value, dict):
        if isinstance(value.get("id"), str):
            collection = ".".join(str(part) for part in path[:-1]) or "root"
            record = f"{collection}:{value['id']}"
        def ref(kind, child_path, item):
            return ReferenceUse(kind, str(file), record, _format_reference_path(child_path), item)
        for key, nested in value.items():
            child = path + (key,)
            if key in {"assertions", "local_analysis", "before", "after"}:
                continue
            if key in {"source", "external_group"}:
                yield ref(key, child, nested)
                if isinstance(nested, dict) and "basis" in nested:
                    yield from _walk_reference_uses(file, {"basis": nested["basis"]}, child, record)
            elif key == "match":
                if not isinstance(nested, list):
                    yield ref("match", child, nested)
                else:
                    for index, item in enumerate(nested):
                        yield ref("match", child + (index,), item)
                        if isinstance(item, dict) and "basis" in item:
                            yield from _walk_reference_uses(file, {"basis": item["basis"]}, child + (index,), record)
            elif key == "basis":
                fields = nested.items() if isinstance(nested, dict) else [(None, nested)]
                for field, items in fields:
                    base = child if field is None else child + (field,)
                    if field in {"zh", "en"}:
                        continue
                    if field == "subjects" and isinstance(items, list):
                        for index, group in enumerate(items):
                            group_path = base + (index,)
                            if not isinstance(group, dict) or set(group) != {"values", "references"} or not isinstance(group.get("references"), list) or not group["references"]:
                                yield ref("basis", group_path, group)
                            else:
                                for ri, reference in enumerate(group["references"]):
                                    yield ref("basis", group_path + ("references", ri), reference)
                    elif isinstance(items, list):
                        for index, item in enumerate(items):
                            yield ref("basis", base + (index,), item)
                    else:
                        yield ref("basis", base, items)
            else:
                yield from _walk_reference_uses(file, nested, child, record)


def _schema_issues(root: Path, relative: str, schema_name: str):
    from jsonschema import Draft202012Validator, FormatChecker
    path = root / relative
    if not path.exists():
        return [Issue("SOURCE_SCHEMA_INVALID", relative, "document", "$", "missing file")]
    document = _load_yaml(path)
    schema = json.loads((project_root(__file__) / "schemas" / schema_name)
                        .read_text(encoding="utf-8"))
    return [Issue("SOURCE_SCHEMA_INVALID", relative, "document",
                  ".".join(str(part) for part in error.path), error.message)
            for error in Draft202012Validator(
                schema, format_checker=FormatChecker()
            ).iter_errors(document)]


def _history_prefix(previous, current):
    return current[:len(previous)] == previous


def _entity_semantic_issues(topics_doc, entities_doc, uses_doc, obligations_doc, accepted):
    issues = []
    records = entities_doc.get("entities", [])
    if not isinstance(records, list):
        return issues
    records = [row for row in records if isinstance(row, dict)]
    entities = {row.get("id"): row for row in records if isinstance(row.get("id"), str)}
    topics = {row.get("id") for row in topics_doc.get("concepts", []) if isinstance(row, dict)}
    obligations = {row.get("id") for row in obligations_doc.get("obligations", []) if isinstance(row, dict)}
    def issue(row, field, message, code="SOURCE_SCHEMA_INVALID"):
        issues.append(Issue(code, "data/vocab/entities.yaml", str(row.get("id", "")), field, message))
    if len(entities) != len(records):
        issues.append(Issue("SOURCE_STABLE_ID_CHANGED", "data/vocab/entities.yaml", "document", "entities", "entity IDs must be unique"))
    for row in records:
        basis = row.get("basis") if isinstance(row.get("basis"), dict) else {}
        assertions = row.get("assertions") if isinstance(row.get("assertions"), dict) else {}
        subjects = row.get("subjects", [])
        subjects = subjects if isinstance(subjects, list) and all(isinstance(v, str) for v in subjects) else []
        covered = set()
        for field, groups in (("basis.subjects", basis.get("subjects", [])),
                              ("assertions.subjects", assertions.get("subjects", []))):
            if not isinstance(groups, list):
                continue
            for group in groups:
                if not isinstance(group, dict) or not isinstance(group.get("values"), list):
                    continue
                values = group["values"]
                if not all(isinstance(value, str) for value in values):
                    continue
                covered.update(values)
                if not set(values) <= set(subjects):
                    issue(row, field, "evidence values must be a subset of subjects")
        if set(subjects) != covered:
            issue(row, "basis.subjects", "evidence and assertions must cover every subject value")
        for subject in subjects:
            if subject not in topics:
                issue(row, "subjects", f"unknown topic {subject}")
        if assertions.get("subjects") and row.get("status") == "active":
            issue(row, "assertions.subjects", "project self judgment cannot have active status")
        for field in ("vendor", "replaced_by"):
            target = row.get(field)
            if isinstance(target, str) and target not in entities:
                issue(row, field, f"unknown entity {target}", "SOURCE_ENTITY_MISSING")
        for target in row.get("creator", []) if isinstance(row.get("creator", []), list) else []:
            if isinstance(target, str) and target not in entities:
                issue(row, "creator", f"unknown entity {target}", "SOURCE_ENTITY_MISSING")
        urls = row.get("urls")
        if isinstance(urls, list) and sum(isinstance(url, dict) and url.get("primary") is True for url in urls) != 1:
            issue(row, "urls", "exactly one primary URL is required")
        if row.get("fixed_sha256") and not row.get("version"):
            issue(row, "fixed_sha256", "fixed content requires an identified version")
        if row.get("kind") not in {"standard", "publication"}:
            if "source_status" in row:
                issue(row, "source_status", "external source status applies only to source entities")
            continue
        for field in ("version", "source_status", "replaced_by"):
            if row.get(field) is None:
                continue
            if not basis.get(field):
                issue(row, "basis." + field, f"publisher evidence is required for {field}")
            decisions = [decision for event in row.get("history", []) if isinstance(event, dict)
                         for decision in event.get("decisions", [])]
            if not any(decision_authorizes(accepted, decision, f"entities/{row['id']}", field, row[field]) for decision in decisions):
                issue(row, field, "accepted decision must adopt this exact entity field and value", "SOURCE_DECISION_MISSING")
        target = row.get("replaced_by")
        if target in entities and entities[target].get("kind") not in {"standard", "publication"}:
            issue(row, "replaced_by", "source replacement must target a source entity")
        review = row.get("review")
        if isinstance(review, dict):
            expected = {"de-jure": 24, "de-facto": 12, "vendor": 6, "archival": None}.get(row.get("tier"))
            if review.get("interval_months") != expected:
                issue(row, "review.interval_months", "review interval must follow tier policy")
            checked = review.get("checked")
            try:
                due = compute_next_due(date.fromisoformat(checked), expected) if checked else None
                if review.get("next_due") != (due.isoformat() if due else None):
                    issue(row, "review.next_due", "next_due must follow checked and calendar interval")
            except (TypeError, ValueError):
                pass  # Shape/date validation reports this independently.
            for obligation in review.get("obligations", []):
                if obligation not in obligations:
                    issue(row, "review.obligations", "referenced obligation is missing; no lifecycle is implied")
        for watch in row.get("watch", []) if isinstance(row.get("watch", []), list) else []:
            if isinstance(watch, dict) and isinstance(watch.get("cadence_months"), dict):
                content = {"de-jure": 1, "de-facto": 3, "vendor": 6, "archival": 12}.get(row.get("tier"))
                if watch["cadence_months"].get("content") != content:
                    issue(row, "watch", "watch content cadence must follow tier policy")
    for start in entities:
        seen = set()
        current = start
        while isinstance(current, str) and current in entities:
            if current in seen:
                issue(entities[start], "replaced_by", "replacement cycle")
                break
            seen.add(current)
            current = entities[current].get("replaced_by")
    uses = uses_doc.get("sources", [])
    seen_ids, seen_entities = set(), set()
    for use in uses if isinstance(uses, list) else []:
        if not isinstance(use, dict):
            continue
        uid, entity = use.get("id"), use.get("entity")
        if not isinstance(uid, str) or not isinstance(entity, str):
            continue
        if uid in seen_ids or entity in seen_entities:
            issues.append(Issue("SOURCE_SCHEMA_INVALID", "data/vocab/sources.yaml", uid, "id", "use IDs and entity registrations must be unique"))
        seen_ids.add(uid); seen_entities.add(entity)
        if entity not in entities or entities[entity].get("kind") not in {"standard", "publication"}:
            issues.append(Issue("SOURCE_ENTITY_MISSING", "data/vocab/sources.yaml", uid, "entity", "use must reference a source entity"))
        source_entity = entities.get(entity, {})
        if source_entity.get("tier") == "archival":
            issues.append(Issue("SOURCE_SCHEMA_INVALID", "data/vocab/sources.yaml", uid, "entity",
                                "archival source cannot be registered for source uses"))
        for role in use.get("roles", []):
            if isinstance(role, dict) and role.get("role") in {"structure", "group"} and role.get("status") == "approved":
                qualification = dependent_role_qualification_error(source_entity, use, accepted, role["role"])
                if qualification:
                    issues.append(Issue("SOURCE_ROLE_NOT_APPROVED", "data/vocab/sources.yaml", uid, "roles", qualification))
        names = [role.get("role") for role in use.get("roles", []) if isinstance(role, dict)]
        if len(names) != len(set(names)):
            issues.append(Issue("SOURCE_SCHEMA_INVALID", "data/vocab/sources.yaml", uid, "roles", "roles must be unique"))
    return issues


def _record_evidence_issues(relative, document, sources, adoptions, accepted):
    from jsonschema import Draft202012Validator, FormatChecker
    from kb_core.label_basis import validate_basis
    assertion_validator = Draft202012Validator(ASSERTIONS, format_checker=FormatChecker())
    issues = []
    if not isinstance(document, dict):
        return issues
    for collection, records in document.items():
        if not isinstance(records, list):
            continue
        for record in records:
            if not isinstance(record, dict):
                continue
            identity = str(record.get("id", "document"))
            if "local_analysis" in record:
                local = record["local_analysis"]
                validator = Draft202012Validator(LOCAL_ANALYSIS)
                messages = [error.message for error in validator.iter_errors(local)]
                if str(relative) != "data/vocab/forms.yaml" or collection != "arrays":
                    messages.append("Q16 isolation applies only to forms arrays")
                if "source" in record or "external_group" in record:
                    messages.append("isolated display metadata must not retain an external source or group")
                if isinstance(local, dict) and not decision_authorizes(
                        accepted, local.get("decision"), "@control:local-analysis",
                        "local_analysis_policy", LOCAL_ANALYSIS_POLICY):
                    messages.append("effective Q16 isolation policy decision required")
                issues.extend(Issue("SOURCE_SCHEMA_INVALID", str(relative), identity,
                                    "local_analysis", message) for message in messages)
            assertions = record.get("assertions")
            if assertions is not None:
                for error in assertion_validator.iter_errors(assertions):
                    issues.append(Issue("SOURCE_SCHEMA_INVALID", str(relative), identity,
                                        "assertions", error.message))
                if "source" in record and isinstance(assertions, dict) and "source" in assertions:
                    issues.append(Issue("SOURCE_SCHEMA_INVALID", str(relative), identity,
                                        "assertions.source", "external derivation and local source assertion are mutually exclusive"))
            basis = record.get("basis")
            if not isinstance(basis, dict):
                continue
            for language in ("zh", "en"):
                if language not in basis:
                    continue
                value = basis[language]
                if not isinstance(value, dict):
                    messages = ["language evidence must use the adopted structured contract"]
                else:
                    messages = validate_basis(value, (record.get("label") or {}).get(language),
                                              record, language, sources, adoptions,
                                              collection="topics" if collection == "concepts" else collection)
                issues.extend(Issue("SOURCE_SCHEMA_INVALID", str(relative), identity,
                                    "basis." + language, message) for message in messages)
    return issues


def validate_source_documents(documents, accepted_decisions, obligations_document=None,
                              adoptions=None) -> List[Issue]:
    """Validate a captured vocabulary snapshot without reading its backing files.

    ``documents`` maps vocabulary names (entities, sources, topics, types,
    genres, forms; additional consumers are allowed) to parsed root documents.
    Decisions must already be schema-validated and effective. Missing obligations
    do not activate a lifecycle; actual unresolved references are still errors.
    """
    from jsonschema import Draft202012Validator, FormatChecker
    documents = normalize_yaml_dates(documents)
    accepted = normalize_yaml_dates(accepted_decisions)
    entities_doc = documents.get("entities", {})
    uses_doc = documents.get("sources", {})
    obligations_doc = normalize_yaml_dates(obligations_document) if obligations_document is not None else {}
    issues = []
    schemas = build_schema_documents()
    for name in ("topics", "types", "genres", "forms"):
        if name in documents and (not isinstance(documents[name], dict)
                                  or type(documents[name].get("schema_version")) is not int
                                  or documents[name]["schema_version"] != 2):
            issues.append(Issue("SOURCE_SCHEMA_INVALID", f"data/vocab/{name}.yaml", "document",
                                "schema_version", "present vocabulary must declare schema_version: 2"))
    cases = [("entities", entities_doc, "source-entities.schema.json"),
             ("sources", uses_doc, "source-uses.schema.json")]
    if obligations_document is not None:
        cases.append(("source-obligations", obligations_doc, "source-obligations.schema.json"))
    for name, document, schema_name in cases:
        validator = Draft202012Validator(schemas[schema_name], format_checker=FormatChecker())
        issues.extend(Issue("SOURCE_SCHEMA_INVALID", f"data/vocab/{name}.yaml", "document",
                            ".".join(str(part) for part in error.path), error.message)
                      for error in validator.iter_errors(document))
    # Schema has already rejected these shapes; semantic passes only consume
    # records whose containers can be traversed safely.
    for document, key in ((entities_doc, "entities"), (uses_doc, "sources"),
                          (obligations_doc, "obligations")):
        if not isinstance(document, dict) or not isinstance(document.get(key, []), list):
            return _sort_issues(issues)
        for row in document.get(key, []):
            if not isinstance(row, dict):
                return _sort_issues(issues)
            for field in ("roles", "watch", "history", "creator"):
                if field in row and not isinstance(row[field], list):
                    return _sort_issues(issues)
            for field in ("basis", "review", "assertions"):
                if field in row and not isinstance(row[field], dict):
                    return _sort_issues(issues)

    for row in entities_doc.get("entities", []):
        if row.get("temporary_unavailable") and row.get("source_status") == "withdrawn":
            issues.append(Issue(
                "SOURCE_SCHEMA_INVALID", "data/vocab/entities.yaml", row.get("id", ""),
                "status", "temporary unavailability cannot set withdrawn",
            ))
        for field in ("origin", "url"):
            if field in row:
                issues.append(Issue(
                    "SOURCE_LEGACY_FIELD", "data/vocab/entities.yaml", row.get("id", ""),
                    field, f"legacy field {field}",
                ))

    issues.extend(_entity_semantic_issues(documents.get("topics", {}), entities_doc, uses_doc, obligations_doc, accepted))

    for use in uses_doc.get("sources", []):
        for index, role in enumerate(use.get("roles", [])):
            if not isinstance(role, dict):
                continue
            if role.get("status") in {"approved", "retired"} and not role_is_authorized(accepted, use, role):
                issues.append(Issue(
                    "SOURCE_ROLE_DECISION_MISSING", "data/vocab/sources.yaml", use.get("id", ""),
                    f"roles[{index}].decision", "accepted role decision required",
                ))

    uses = {row["id"]: row for row in uses_doc.get("sources", []) if isinstance(row.get("id"), str)}
    for name, document in documents.items():
        relative = Path(f"data/vocab/{name}.yaml")
        issues.extend(_record_evidence_issues(relative, document, uses, adoptions, accepted))
        references = collect_reference_uses(relative, document)
        issues.extend(validate_reference_documents(entities_doc, uses_doc, references, accepted))
    if obligations_document is not None:
        references = collect_reference_uses(Path("data/vocab/source-obligations.yaml"), obligations_doc)
        issues.extend(validate_reference_documents(entities_doc, uses_doc, references, accepted))
    return _sort_issues(set(issues))


def validate_repository(root: Path, previous_root: Optional[Path] = None) -> List[Issue]:
    from kb_core.label_adoptions import load_adoptions
    documents = {path.stem: _load_yaml(path) for path in sorted((root / "data/vocab").glob("*.yaml"))
                 if path.stem != "source-obligations"}
    obligation_path = root / "data/vocab/source-obligations.yaml"
    obligations_doc = _load_yaml(obligation_path) if obligation_path.exists() else None
    issues = validate_source_documents(documents, _load_accepted_decisions(root / "docs/decisions"),
                                       obligations_doc, load_adoptions(root))
    entities_doc = documents.get("entities", {})
    uses_doc = documents.get("sources", {})
    obligations_doc = obligations_doc or {}
    if not isinstance(entities_doc, dict) or not isinstance(entities_doc.get("entities", []), list):
        return issues
    if any(not isinstance(row, dict) for row in entities_doc.get("entities", [])):
        return issues
    if previous_root is not None:
        old_forms = _load_yaml(previous_root / "data/vocab/forms.yaml")
        current_forms = documents.get("forms", {})
        old_arrays = {row["id"]: row for row in old_forms.get("arrays", [])}
        for row in current_forms.get("arrays", []):
            if "local_analysis" not in row:
                continue
            old = old_arrays.get(row.get("id"))
            old_members = [form["id"] for form in old_forms.get("forms", []) if row["id"] in form.get("arrays", [])]
            current_members = [form["id"] for form in current_forms.get("forms", []) if row["id"] in form.get("arrays", [])]
            original = old.get("source") if old else None
            if old and "local_analysis" in old:
                original = old["local_analysis"].get("legacy_source_label")
            if (not old or old.get("superordinate") != row.get("superordinate")
                    or old.get("members") != row.get("members") or old_members != current_members
                    or original != row["local_analysis"].get("legacy_source_label")):
                issues.append(Issue("SOURCE_SCHEMA_INVALID", "data/vocab/forms.yaml", row.get("id", ""),
                                    "local_analysis", "Q16 must preserve the original display string, parent and ordered members"))
        previous_entities = _load_yaml(previous_root / "data/vocab/entities.yaml").get("entities", [])
        current_entities = entities_doc.get("entities", [])
        current_by_id = {row["id"]: row for row in current_entities}
        for old in previous_entities:
            current = current_by_id.get(old.get("id"))
            if current is None:
                issues.append(Issue(
                    "SOURCE_STABLE_ID_CHANGED", "data/vocab/entities.yaml", old.get("id", ""),
                    "id", "previous stable ID is missing",
                ))
            if current and not _history_prefix(old.get("history", []), current.get("history", [])):
                issues.append(Issue(
                    "SOURCE_HISTORY_NOT_APPEND_ONLY", "data/vocab/entities.yaml", old.get("id", ""),
                    "history", "history must retain the previous prefix",
                ))

        previous_uses = _load_source_uses(previous_root / "data/vocab/sources.yaml")
        current_uses = _load_source_uses(root / "data/vocab/sources.yaml")
        for uid, old in previous_uses.items():
            current = current_uses.get(uid)
            if current is None or current.get("entity") != old.get("entity"):
                issues.append(Issue("SOURCE_STABLE_ID_CHANGED", "data/vocab/sources.yaml", uid,
                                    "entity", "previous registry identity or its source entity changed"))
            if current and not _history_prefix(old.get("history", []), current.get("history", [])):
                issues.append(Issue("SOURCE_HISTORY_NOT_APPEND_ONLY", "data/vocab/sources.yaml", uid,
                                    "history", "history must retain the previous prefix"))

        previous_obligations = {
            row["id"]: row for row in _load_yaml(
                previous_root / "data/vocab/source-obligations.yaml"
            ).get("obligations", [])
        }
        for row in obligations_doc.get("obligations", []):
            old = previous_obligations.get(row.get("id"))
            if old and old.get("state") == "resolved" and row.get("state") != "resolved":
                issues.append(Issue(
                    "SOURCE_OBLIGATION_REOPENED", "data/vocab/source-obligations.yaml",
                    row.get("id", ""), "state", "resolved obligation cannot reopen",
                ))
    return _sort_issues(issues)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    schemas = subparsers.add_parser("write-schemas")
    schemas.add_argument("--directory", type=Path, required=True)
    decisions = subparsers.add_parser("decisions")
    decisions.add_argument("--directory", type=Path, required=True)
    decisions.add_argument("--require", required=True)
    args = parser.parse_args(argv)
    if args.command == "write-schemas":
        write_schema_documents(args.directory)
        return 0
    paths = sorted(args.directory.glob("source-*.md"))
    patches = load_decision_patches(paths)
    required = set(args.require.split(","))
    seen = {patch.qid for patch in patches}
    missing = sorted(required - seen)
    if missing:
        raise SystemExit(f"SOURCE_DECISION_DELIVERY_MISSING {','.join(missing)}")
    for qid in sorted(required):
        print(f"{qid} patch_count={sum(patch.qid == qid for patch in patches)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
