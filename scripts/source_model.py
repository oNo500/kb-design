#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Dict, List, Literal, NamedTuple, Sequence

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
    return []


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
                "vocab/generated/source-cutover-payload.json",
                "vocab/generated/source-cutover-handoff.json",
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
                    {"path": {"const": "vocab/topics.yaml"}, "after_sha256": HASH},
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
            "module": {"const": "scripts/source_model.py"},
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
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            raise ValueError(f"SOURCE_SCHEMA_INVALID {path}")
        front = yaml.safe_load(text.split("---\n", 2)[1])
        if front.get("status") != "accepted":
            raise ValueError(f"SOURCE_DECISION_MISSING {path}")
        for answer in front.get("answers", []):
            qid = answer.get("question")
            for value in answer.get("patches", []):
                patches.append(DecisionPatch(
                    value["identity"], value["field"], value["value"], qid,
                ))
    return patches


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
