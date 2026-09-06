#!/usr/bin/env python3
from kb_core.repository import project_root
import argparse
import dataclasses
import hashlib
import json
import pathlib
import sys
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence, Tuple

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from kb_core.governance.term_model import TermsSchemaError, schema_issues
from kb_core.governance.term_model import parse_terms
from kb_core.build_source_index import visit_record_decisions, visit_reference_use
from kb_core.label_adoptions import validate_adoptions
from kb_core.governance.term_validation import load_term_decision_sets, validate_term_snapshot
from kb_core.label_basis import validate_basis
from kb_core.governance.term_rendering import (
    render_glossary as _render_glossary,
    render_term_markdown,
)
from kb_core.governance.term_git import captured_previous_terms
from kb_core.source_model import collect_reference_uses, validate_source_documents


REPOSITORY_ROOT = project_root(__file__)
LANGUAGE_ORDER = {"zh-Hans": 0, "zh-Hant": 1, "en": 2}
STATUS_ORDER = {
    "preferredTerm-admn-sts": 0,
    "admittedTerm-admn-sts": 1,
    "deprecatedTerm-admn-sts": 2,
    "supersededTerm-admn-sts": 3,
}
PREFERRED = "preferredTerm-admn-sts"
ADMITTED = "admittedTerm-admn-sts"
HISTORICAL = frozenset(
    ("deprecatedTerm-admn-sts", "supersededTerm-admn-sts")
)
READ_ONLY_DECLARATION = (
    "本文件由术语记录确定生成，只读；如需修改，请编辑 `data/vocab/terms.yaml`。"
)


@dataclass(frozen=True)
class HistoryEvent:
    date: str
    event: str
    decision: str
    reason: str
    from_value: Optional[str]
    to_value: Optional[str]
    linked_terms: Sequence[str]


@dataclass(frozen=True)
class TermCutoverState:
    schema: str
    version: int
    state: str
    active_editor: str
    terms_mode: str
    consumers_enabled: bool
    decision: str
    history: Sequence[HistoryEvent]


def _get(value: Any, key: str) -> Any:
    if isinstance(value, Mapping):
        return value[key]
    return getattr(value, key)


def _get_optional(value: Any, key: str, default: Any = None) -> Any:
    if isinstance(value, Mapping):
        return value.get(key, default)
    return getattr(value, key, default)


def _plain(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {
            field.name: _plain(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(
            _plain(value),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def _ensure_consumers_enabled(state: Any) -> None:
    if (
        not _get(state, "consumers_enabled")
        or _get(state, "terms_mode") != "active_editor"
        or _get(state, "state") != "active"
    ):
        raise ValueError("TERM_CONSUMERS_DISABLED")


def load_cutover_state(path: pathlib.Path) -> TermCutoverState:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    schema = json.loads(
        (
            REPOSITORY_ROOT
            / "schemas/term-cutover-state-v1.schema.json"
        ).read_text(encoding="utf-8")
    )
    errors = sorted(
        Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(value),
        key=lambda error: error.json_path,
    )
    if errors:
        raise ValueError(
            "TERM_CUTOVER_STATE_SCHEMA " + errors[0].json_path
        )
    return TermCutoverState(
        schema=value["schema"],
        version=value["version"],
        state=value["state"],
        active_editor=value["active_editor"],
        terms_mode=value["terms_mode"],
        consumers_enabled=value["consumers_enabled"],
        decision=value["decision"],
        history=tuple(HistoryEvent(**item) for item in value["history"]),
    )


def _ordered_languages(concept: Any) -> Sequence[Any]:
    return tuple(
        sorted(
            _get(concept, "languages"),
            key=lambda language: (
                LANGUAGE_ORDER[_get(language, "language")],
                _get(language, "language"),
            ),
        )
    )


def _ordered_terms(language: Any) -> Sequence[Any]:
    return tuple(
        sorted(
            _get(language, "terms"),
            key=lambda term: (
                STATUS_ORDER[_get(term, "administrative_status")],
                _get(term, "id"),
            ),
        )
    )


def _snapshot_concept(concept: Any) -> Mapping[str, Any]:
    value = _plain(concept)
    value["languages"] = []
    for language in _ordered_languages(concept):
        language_value = _plain(language)
        language_value["terms"] = [
            _plain(term) for term in _ordered_terms(language)
        ]
        value["languages"].append(language_value)
    if "definitions" in value:
        value["definitions"] = sorted(
            value["definitions"],
            key=lambda definition: (
                LANGUAGE_ORDER[definition["language"]],
                definition["text"],
            ),
        )
    return value


def _snapshot_value(
    document: Any,
    active_concepts: Sequence[Any],
    source_index: Mapping[str, object],
    state: Any,
    *,
    source_entities: Optional[Mapping[str, object]] = None,
    model_labels: Optional[Sequence[Mapping[str, object]]] = None,
) -> Mapping[str, Any]:
    return {
        "schema": _get(document, "schema"),
        "version": _get(document, "version"),
        "source_index_sha256": hashlib.sha256(
            canonical_json(source_index)
        ).hexdigest(),
        "cutover_decision": _get(state, "decision"),
        "source_entities": [
            _plain(value) for _, value in sorted((source_entities or {}).items())
        ],
        "model_labels": sorted(
            (_plain(row) for row in (model_labels or ())),
            key=lambda row: (row.get("zh", ""), row.get("en", ""), row.get("targets", [])),
        ),
        "concepts": [
            _snapshot_concept(concept)
            for concept in sorted(
                active_concepts, key=lambda item: _get(item, "id")
            )
        ],
    }


def canonical_snapshot(
    document: Any,
    source_index: Mapping[str, object],
    state: Any,
    *,
    source_entities: Optional[Mapping[str, object]] = None,
    model_labels: Optional[Sequence[Mapping[str, object]]] = None,
) -> bytes:
    _ensure_consumers_enabled(state)
    active = tuple(
        concept
        for concept in _get(document, "concepts")
        if _get(concept, "workflow") == "active"
    )
    return canonical_json(
        _snapshot_value(document, active, source_index, state,
                        source_entities=source_entities, model_labels=model_labels)
    )


def ordered_concepts(document: Any, layout: Mapping[str, object]) -> Tuple[Any, ...]:
    groups = sorted(
        layout["groups"], key=lambda group: (group["order"], group["id"])
    )
    concepts = {_get(concept, "id"): concept for concept in _get(document, "concepts")}
    seen = set()
    ordered = []
    for group in groups:
        local = set()
        for concept_id in group.get("members", []):
            if concept_id in local:
                raise ValueError("TERM_LAYOUT_MEMBER_DUPLICATE " + concept_id)
            local.add(concept_id)
            if concept_id not in concepts:
                raise ValueError("TERM_LAYOUT_MEMBER_UNKNOWN " + concept_id)
            if concept_id not in seen:
                ordered.append(concepts[concept_id])
                seen.add(concept_id)
    missing = sorted(set(concepts) - seen)
    if missing:
        raise ValueError("TERM_LAYOUT_MEMBER_MISSING " + " ".join(missing))
    return tuple(ordered)


def build_model_label_rows(topics, forms, adoptions, accepted_decisions) -> list:
    """Render current adopted level-5 labels without changing adoption records."""
    rows = {}
    for collection, document in (("topics", topics), ("forms", forms)):
        records = document.get("concepts", document.get("forms", []))
        current_level5 = set()
        for record in records:
            value = record.get("basis", {}).get("zh")
            if not isinstance(value, Mapping) or value.get("level") != 5:
                continue
            key = f"{collection}/{record['id']}/zh"
            current_level5.add(key)
            adoption = adoptions.get(key)
            if not isinstance(adoption, Mapping) or adoption.get("accept") is not True:
                raise ValueError("MODEL_LABEL_ADOPTION_MISSING " + key)
            label = record.get("label", {}).get("zh")
            if adoption.get("label") != label or adoption.get("basis") != value:
                raise ValueError("MODEL_LABEL_ADOPTION_STALE " + key)
            errors = validate_basis(value, label, record, "zh", sources=None,
                                    decisions=adoptions, collection=collection,
                                    accepted_decisions=accepted_decisions)
            if errors:
                raise ValueError("; ".join(errors))
            english = record.get("label", {}).get("en")
            identity = (label, english)
            row = rows.setdefault(identity, {"zh": label, "en": english,
                                              "targets": [], "target_models": []})
            target = f"{collection}/{record['id']}"
            row["targets"].append(target)
            model = _plain(value["model"])
            row["target_models"].append({"target": target, "model": model})
        invalid_targets = sorted(
            key for key, adoption in adoptions.items()
            if key.startswith(collection + "/") and key.endswith("/zh")
            and isinstance(adoption, Mapping) and adoption.get("accept") is True
            and isinstance(adoption.get("basis"), Mapping)
            and adoption["basis"].get("level") == 5 and key not in current_level5
        )
        if invalid_targets:
            raise ValueError("MODEL_LABEL_TARGET_INVALID " + " ".join(invalid_targets))
    return sorted(rows.values(), key=lambda row: tuple(row["targets"]))


def render_glossary(
    snapshot: Mapping[str, object],
    layout: Mapping[str, object],
    state: Any,
    source_entities: Optional[Mapping[str, object]] = None,
) -> str:
    return _render_glossary(snapshot, layout, _plain(state), source_entities)


def _load_yaml(path: pathlib.Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def capture_validation_context(root: pathlib.Path, *, with_history: bool = False):
    """Capture and validate every repository input shared by term consumers."""
    documents = {
        name: _load_yaml(root / "data/vocab" / f"{name}.yaml")
        for name in ("topics", "types", "genres", "forms", "entities", "sources")
    }
    decisions, historical_decisions = load_term_decision_sets(root)
    adoptions = validate_adoptions(
        _load_json(root / "data/inputs/topics/label-adoptions.json")
    )
    obligations_path = root / "data/vocab/source-obligations.yaml"
    obligations = _load_yaml(obligations_path) if obligations_path.is_file() else None
    issues = validate_source_documents(
        documents, decisions, obligations_document=obligations, adoptions=adoptions,
    )
    if issues:
        raise ValueError("\n".join(
            f"{issue.code} {issue.file} {issue.field_path} {issue.message}"
            for issue in issues
        ))
    result = (documents, decisions, adoptions)
    return result + (historical_decisions,) if with_history else result


def _source_catalog(document: Any, entities_document: Mapping[str, object]) -> Mapping[str, object]:
    active_document = {
        "schema": document["schema"], "version": document["version"],
        "concepts": [row for row in document.get("concepts", [])
                     if row.get("workflow") == "active"],
    }
    referenced = {
        use.value["entity"] for use in collect_reference_uses(
            pathlib.Path("data/vocab/terms.yaml"), active_document)
        if use.kind == "basis" and isinstance(use.value, Mapping) and use.value.get("entity")
    }
    return {
        row["id"]: {
            "id": row["id"], "label": row.get("label", {}),
            "version": row.get("version"), "urls": row.get("urls", []),
        }
        for row in entities_document.get("entities", []) if row.get("id") in referenced
    }


def _validate_source_index(document: Any, source_index: Mapping[str, object]) -> None:
    relative = pathlib.Path("data/vocab/terms.yaml")
    expected = [visit_reference_use(use) for use in collect_reference_uses(relative, document)]
    expected.extend(visit_record_decisions(relative, document))
    expected_keys = {canonical_json(row) for row in expected}
    actual = source_index.get("entries", []) if isinstance(source_index, Mapping) else []
    actual_terms = [row for row in actual if isinstance(row, Mapping)
                    and row.get("file") == "data/vocab/terms.yaml"]
    actual_keys = {canonical_json(row) for row in actual_terms}
    if actual_keys != expected_keys or len(actual_terms) != len(actual_keys):
        raise ValueError("TERM_SOURCE_INDEX_MISMATCH")


def _outputs(arguments: argparse.Namespace) -> Tuple[bytes, bytes]:
    root = arguments.design_root.resolve()
    terms_bytes = arguments.terms.read_bytes()
    document = yaml.safe_load(terms_bytes)
    state_value = _load_yaml(arguments.state)
    state = load_cutover_state(arguments.state)
    layout = _load_yaml(arguments.layout)
    source_index = _load_json(arguments.source_index)
    captured, decisions, adoptions, historical_decisions = capture_validation_context(
        root, with_history=True,
    )
    git_previous_bytes = captured_previous_terms(root, terms_bytes)
    git_previous = yaml.safe_load(git_previous_bytes) if git_previous_bytes is not None else None
    issues = list(validate_term_snapshot(document, source_documents=captured,
                                    accepted_decisions=decisions, previous=git_previous,
                                    state=state_value,
                                    historical_decisions=historical_decisions))
    if arguments.previous:
        explicit_previous = _load_yaml(arguments.previous)
        issues.extend(validate_term_snapshot(
            document, source_documents=captured, accepted_decisions=decisions,
            previous=explicit_previous, historical_decisions=historical_decisions,
        ))
    if issues:
        raise ValueError("\n".join(f"{issue.code} {issue.path} {issue.message}" for issue in issues))
    active = {row["id"]: row for row in document.get("concepts", []) if row.get("workflow") == "active"}
    ordered_concepts({"concepts": list(active.values())}, layout)
    _validate_source_index(document, source_index)
    model_labels = build_model_label_rows(captured["topics"], captured["forms"], adoptions, decisions)
    sources = _source_catalog(document, captured["entities"])
    snapshot = canonical_snapshot(document, source_index, state,
                                  source_entities=sources, model_labels=model_labels)
    glossary = render_glossary(json.loads(snapshot), layout, state, sources).encode("utf-8")
    return snapshot, glossary


def _write_output(path: pathlib.Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def _build(arguments: argparse.Namespace) -> int:
    snapshot, glossary = _outputs(arguments)
    _write_output(arguments.snapshot_out, snapshot)
    _write_output(arguments.glossary_out, glossary)
    return 0


def _check(arguments: argparse.Namespace) -> int:
    snapshot, glossary = _outputs(arguments)
    drift = []
    for path, expected in (
        (arguments.snapshot_out, snapshot),
        (arguments.glossary_out, glossary),
    ):
        if not path.is_file() or path.read_bytes() != expected:
            drift.append(path)
    if drift:
        for path in drift:
            print("TERM_OUTPUT_DRIFT " + str(path), file=sys.stderr)
        return 1
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("build", "check"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--design-root", type=pathlib.Path, default=REPOSITORY_ROOT)
        subparser.add_argument("--terms", required=True, type=pathlib.Path)
        subparser.add_argument("--state", required=True, type=pathlib.Path)
        subparser.add_argument("--layout", required=True, type=pathlib.Path)
        subparser.add_argument("--source-index", required=True, type=pathlib.Path)
        subparser.add_argument("--snapshot-out", required=True, type=pathlib.Path)
        subparser.add_argument("--glossary-out", required=True, type=pathlib.Path)
        subparser.add_argument("--previous", type=pathlib.Path)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "build":
            return _build(arguments)
        return _check(arguments)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
