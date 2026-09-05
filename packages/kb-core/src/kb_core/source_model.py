#!/usr/bin/env python3
from kb_core.repository import project_root
import argparse
import calendar
import copy
import json
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
    entities = _load_source_entities(root / "data/vocab/entities.yaml")
    uses = _load_source_uses(root / "data/vocab/sources.yaml")
    accepted = _load_accepted_decision_ids(root / "docs/decisions")
    issues = []
    for reference in references:
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
                     if row.get("role") == role_name), None)
        role_code = ("SOURCE_EXTERNAL_GROUP_ROLE_NOT_APPROVED"
                     if reference.kind == "external_group" else "SOURCE_ROLE_NOT_APPROVED")
        if role is None or role.get("status") != "approved":
            issues.append(_issue(reference, role_code))
        elif role.get("decision") not in accepted:
            issues.append(_issue(reference, "SOURCE_ROLE_DECISION_MISSING"))
        for index, basis in enumerate(reference.value["basis"]):
            nested = ReferenceUse(
                "basis", reference.file, reference.record,
                f"{reference.field_path}.basis[{index}]", basis,
            )
            issues.extend(validate_references(root, [nested]))
    return _sort_issues(issues)


def _load_yaml(path: Path):
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_source_entities(path: Path):
    document = _load_yaml(path)
    return {
        row["id"]: row for row in document.get("entities", [])
        if row.get("kind") in {"standard", "publication"}
    }


def _load_source_uses(path: Path):
    return {row["id"]: row for row in _load_yaml(path).get("sources", [])}


def _front_matter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return None
    return yaml.safe_load(text.split("---\n", 2)[1])


def _load_accepted_decision_ids(directory: Path):
    result = set()
    if not directory.exists():
        return result
    for path in directory.glob("source-*.md"):
        front = _front_matter(path)
        if front and front.get("status") == "accepted" and front.get("id"):
            result.add(front["id"])
    return result


def _issue(reference: ReferenceUse, code: str, message: str = ""):
    return Issue(code, reference.file, reference.record, reference.field_path, message or code)


def _sort_issues(issues):
    return sorted(issues, key=lambda item: (
        item.file, item.record, item.field_path, item.code, item.message,
    ))


def _validate_reference_value(kind, value):
    if not isinstance(value, dict):
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
    return not (entity.get("fixed_sha256") and entity.get("version"))


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
        ("id", "label", "kind"),
        {
            "id": ID,
            "label": {"type": "object", "minProperties": 1,
                      "additionalProperties": {"type": "string"}},
            "kind": NONEMPTY,
            "version": {"oneOf": [NONEMPTY, {"type": "null"}]},
            "urls": _array(url, 1),
            "status": {"enum": ["current", "superseded", "withdrawn"]},
            "basis": {"type": "object", "minProperties": 1,
                      "additionalProperties": _array(BASIS_ITEM, 1)},
            "review": review,
            "watch": _array({"type": "object"}),
            "replaced_by": {"oneOf": [ID, {"type": "null"}]},
            "history": _array(history, 1),
        },
    )
    entity["allOf"] = [{
        "if": {"properties": {"kind": {"enum": ["standard", "publication"]}},
               "required": ["kind"]},
        "then": {"required": [
            "version", "urls", "status", "basis", "review", "watch", "replaced_by", "history",
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


def _walk_reference_uses(file: Path, value: object, path=(),
                         record: str = "document"):
    if isinstance(value, dict):
        current_record = record
        if isinstance(value.get("id"), str):
            collection = ".".join(str(part) for part in path[:-1]) or "root"
            current_record = f"{collection}:{value['id']}"
        for key, nested in value.items():
            child = path + (key,)
            if key == "basis" and isinstance(nested, list):
                for index, item in enumerate(nested):
                    if _has_exact_keys(item, {"entity", "locator"}):
                        yield ReferenceUse(
                            "basis", str(file), current_record,
                            _format_reference_path(child + (index,)), item,
                        )
            elif key == "basis" and isinstance(nested, dict):
                for basis_key, values in nested.items():
                    if not isinstance(values, list):
                        continue
                    for index, item in enumerate(values):
                        if _has_exact_keys(item, {"entity", "locator"}):
                            yield ReferenceUse(
                                "basis", str(file), current_record,
                                _format_reference_path(child + (basis_key, index)), item,
                            )
            elif key == "source" and _has_exact_keys(
                    nested, {"registry", "item", "locator", "basis"}):
                yield ReferenceUse(
                    "source", str(file), current_record,
                    _format_reference_path(child), nested,
                )
            elif key == "match" and isinstance(nested, list):
                for index, item in enumerate(nested):
                    if _has_exact_keys(item, {"registry", "item", "rel", "basis"}):
                        yield ReferenceUse(
                            "match", str(file), current_record,
                            _format_reference_path(child + (index,)), item,
                        )
            elif key == "external_group" and _has_exact_keys(
                    nested, {"registry", "item", "locator", "basis"}):
                yield ReferenceUse(
                    "external_group", str(file), current_record,
                    _format_reference_path(child), nested,
                )
            yield from _walk_reference_uses(file, nested, child, current_record)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            yield from _walk_reference_uses(file, nested, path + (index,), record)


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


def validate_repository(root: Path, previous_root: Optional[Path] = None,
                        allow_legacy: bool = False) -> List[Issue]:
    issues = []
    for relative, schema_name in (
        ("data/vocab/entities.yaml", "source-entities.schema.json"),
        ("data/vocab/sources.yaml", "source-uses.schema.json"),
        ("data/vocab/source-obligations.yaml", "source-obligations.schema.json"),
    ):
        issues.extend(_schema_issues(root, relative, schema_name))

    entities_doc = _load_yaml(root / "data/vocab/entities.yaml")
    uses_doc = _load_yaml(root / "data/vocab/sources.yaml")
    obligations_doc = _load_yaml(root / "data/vocab/source-obligations.yaml")
    accepted = _load_accepted_decision_ids(root / "docs/decisions")

    for row in entities_doc.get("entities", []):
        if row.get("temporary_unavailable") and row.get("status") == "withdrawn":
            issues.append(Issue(
                "SOURCE_SCHEMA_INVALID", "data/vocab/entities.yaml", row.get("id", ""),
                "status", "temporary unavailability cannot set withdrawn",
            ))
        for field in ("origin", "url"):
            if field in row and not allow_legacy:
                issues.append(Issue(
                    "SOURCE_LEGACY_FIELD", "data/vocab/entities.yaml", row.get("id", ""),
                    field, f"legacy field {field}",
                ))

    for use in uses_doc.get("sources", []):
        for index, role in enumerate(use.get("roles", [])):
            if role.get("status") in {"approved", "retired"} and role.get("decision") not in accepted:
                issues.append(Issue(
                    "SOURCE_ROLE_DECISION_MISSING", "data/vocab/sources.yaml", use.get("id", ""),
                    f"roles[{index}].decision", "accepted role decision required",
                ))

    for path in sorted((root / "data/vocab").glob("*.yaml")):
        references = collect_reference_uses(
            Path(path.relative_to(root)), _load_yaml(path)
        )
        issues.extend(validate_references(root, references))

    if previous_root is not None:
        previous_entities = _load_yaml(previous_root / "data/vocab/entities.yaml").get("entities", [])
        current_entities = entities_doc.get("entities", [])
        current_by_label = {
            json.dumps(row.get("label"), ensure_ascii=False, sort_keys=True): row
            for row in current_entities
        }
        for old in previous_entities:
            current = current_by_label.get(json.dumps(
                old.get("label"), ensure_ascii=False, sort_keys=True
            ))
            if current and current.get("id") != old.get("id"):
                issues.append(Issue(
                    "SOURCE_STABLE_ID_CHANGED", "data/vocab/entities.yaml", old.get("id", ""),
                    "id", f"changed to {current.get('id')}",
                ))
            if current and not _history_prefix(old.get("history", []), current.get("history", [])):
                issues.append(Issue(
                    "SOURCE_HISTORY_NOT_APPEND_ONLY", "data/vocab/entities.yaml", old.get("id", ""),
                    "history", "history must retain the previous prefix",
                ))

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
