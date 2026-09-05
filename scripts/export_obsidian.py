#!/usr/bin/env python3
"""Build the in-memory Obsidian representation of the formal vocabularies."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil
import sys
import tempfile
from collections import OrderedDict
from typing import Any, Iterable, Mapping, Sequence

import yaml

try:
    from .label_basis import basis_rows, validate_basis
except ImportError:
    from label_basis import basis_rows, validate_basis


class ExportError(ValueError):
    """Raised when formal input cannot be mapped without loss."""


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ExportError(message)


_FILES = OrderedDict(
    (
        ("topics", ("vocab/topics.yaml", {"version", "arrays", "concepts"})),
        ("entities", ("vocab/entities.yaml", {"version", "entities"})),
        ("sources", ("vocab/sources.yaml", {"version", "sources"})),
        ("types", ("vocab/types.yaml", {"version", "types"})),
        ("genres", ("vocab/genres.yaml", {"version", "genres"})),
        ("forms", ("vocab/forms.yaml", {"version", "arrays", "forms"})),
    )
)
_COLLECTION_FIELDS = {
    ("topics", "arrays"): {"id", "superordinate", "source"},
    ("topics", "concepts"): {
        "id",
        "label",
        "alt",
        "hidden",
        "basis",
        "broader",
        "related",
        "arrays",
        "scope",
        "source",
        "match",
        "status",
        "added",
        "history",
        "replaced_by",
    },
    ("entities", "entities"): {
        "id",
        "label",
        "alt",
        "hidden",
        "kind",
        "subjects",
        "vendor",
        "creator",
        "replaced_by",
        "form",
        "tier",
        "version",
        "url",
        "watch",
        "checked",
        "basis",
        "match",
        "history",
        "scope",
        "status",
        "added",
    },
    ("sources", "sources"): {"id", "entity", "role", "checked"},
    ("types", "types"): {
        "id",
        "label",
        "alt",
        "hidden",
        "basis",
        "broader",
        "related",
        "arrays",
        "scope",
        "source",
        "match",
        "status",
        "added",
        "history",
        "replaced_by",
    },
    ("genres", "genres"): {
        "id",
        "label",
        "alt",
        "hidden",
        "basis",
        "broader",
        "related",
        "arrays",
        "scope",
        "source",
        "match",
        "status",
        "added",
        "history",
        "replaced_by",
    },
    ("forms", "arrays"): {"id", "superordinate", "source"},
    ("forms", "forms"): {
        "id",
        "label",
        "alt",
        "hidden",
        "basis",
        "broader",
        "related",
        "arrays",
        "scope",
        "source",
        "match",
        "status",
        "added",
        "history",
        "replaced_by",
    },
}
_REQUIRED_FIELDS = {
    ("topics", "arrays"): {"id", "superordinate", "source"},
    ("topics", "concepts"): {
        "id",
        "label",
        "basis",
        "broader",
        "status",
        "added",
    },
    ("entities", "entities"): {
        "id",
        "label",
        "kind",
        "subjects",
        "status",
        "added",
    },
    ("sources", "sources"): {"id", "entity", "role", "checked"},
    ("types", "types"): {"id", "label", "scope", "match", "status", "added"},
    ("genres", "genres"): {"id", "label", "scope", "match", "status", "added"},
    ("forms", "arrays"): {"id", "superordinate", "source"},
    ("forms", "forms"): {
        "id",
        "label",
        "basis",
        "arrays",
        "scope",
        "match",
        "status",
        "added",
    },
}
_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_KIND_DIRECTORIES = {
    "topic": "topics",
    "array": "arrays",
    "entity": "entities",
    "source": "sources",
    "type": "types",
    "genre": "genres",
    "form": "forms",
}
_DIRECTORY_KINDS = {directory: kind for kind, directory in _KIND_DIRECTORIES.items()}
_WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]")


def _error(relative_path: str, object_id: str, field_path: str, message: str) -> ExportError:
    return ExportError(f"{relative_path}: object {object_id}: {field_path}: {message}")


def _check_keys(
    relative_path: str,
    object_id: str,
    field_path: str,
    value: Any,
    allowed: set[str],
) -> None:
    if not isinstance(value, Mapping):
        raise _error(relative_path, object_id, field_path, "expected mapping")
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise _error(
            relative_path,
            object_id,
            f"{field_path}.{unknown[0]}",
            "unknown field",
        )


def _check_required_keys(
    relative_path: str,
    object_id: str,
    field_path: str,
    value: Mapping[str, Any],
    required: set[str],
) -> None:
    missing = sorted(required - set(value))
    if missing:
        raise _error(
            relative_path,
            object_id,
            f"{field_path}.{missing[0]}",
            "missing required field",
        )


def _check_string(relative_path: str, object_id: str, field_path: str, value: Any) -> None:
    if not isinstance(value, str) or not value:
        raise _error(relative_path, object_id, field_path, "expected non-empty string")


def _check_string_list(relative_path: str, object_id: str, field_path: str, value: Any) -> None:
    if not isinstance(value, list):
        raise _error(relative_path, object_id, field_path, "expected list")
    for index, item in enumerate(value):
        _check_string(relative_path, object_id, f"{field_path}[{index}]", item)


def _check_language_forms(
    relative_path: str,
    object_id: str,
    field_path: str,
    value: Any,
    lists_allowed: bool,
) -> None:
    _check_keys(relative_path, object_id, field_path, value, {"zh", "en"})
    if not value:
        raise _error(relative_path, object_id, field_path, "expected non-empty mapping")
    for language, forms in value.items():
        path = f"{field_path}.{language}"
        if lists_allowed and isinstance(forms, list):
            _check_string_list(relative_path, object_id, path, forms)
        else:
            _check_string(relative_path, object_id, path, forms)


def _validate_record(
    name: str,
    relative_path: str,
    collection: str,
    record: Mapping[str, Any],
) -> None:
    object_id = str(record.get("id", "<missing-id>"))
    record_path = f"{collection}[{object_id}]"
    _check_required_keys(
        relative_path,
        object_id,
        record_path,
        record,
        _REQUIRED_FIELDS[(name, collection)],
    )

    string_fields = {
        "id",
        "superordinate",
        "source",
        "entity",
        "kind",
        "vendor",
        "replaced_by",
        "form",
        "tier",
        "version",
        "url",
        "watch",
        "scope",
        "status",
    }
    for field in string_fields & set(record):
        _check_string(relative_path, object_id, f"{record_path}.{field}", record[field])

    list_fields = {"broader", "related", "arrays", "subjects", "creator", "role"}
    for field in list_fields & set(record):
        _check_string_list(relative_path, object_id, f"{record_path}.{field}", record[field])

    for field in ("added", "checked"):
        if field in record and not isinstance(record[field], datetime.date):
            raise _error(relative_path, object_id, f"{record_path}.{field}", "expected date")

    if "label" in record:
        label_path = f"{record_path}.label"
        _check_language_forms(relative_path, object_id, label_path, record["label"], False)
    for field in ("alt", "hidden"):
        if field in record:
            _check_language_forms(relative_path, object_id, f"{record_path}.{field}", record[field], True)

    if "basis" in record:
        allowed_basis = {"subjects"} if collection == "entities" else {"zh", "en"}
        _check_keys(
            relative_path,
            object_id,
            f"{collection}[{object_id}].basis",
            record["basis"],
            allowed_basis,
        )
        _check_required_keys(
            relative_path,
            object_id,
            f"{record_path}.basis",
            record["basis"],
            allowed_basis,
        )
        for field, basis in record["basis"].items():
            path = f"{record_path}.basis.{field}"
            if basis == "model" or isinstance(basis, list) and "model" in basis:
                raise _error(relative_path, object_id, path, "model requires structured language evidence")
            if collection != "entities" and field in ("zh", "en") and isinstance(basis, dict):
                errors = validate_basis(basis, record.get("label", {}).get(field), record,
                                        field, None, collection=name)
                if errors:
                    raise _error(relative_path, object_id, path, "; ".join(errors))
            elif isinstance(basis, list):
                _check_string_list(relative_path, object_id, path, basis)
            else:
                _check_string(relative_path, object_id, path, basis)

    if "match" in record:
        if not isinstance(record["match"], list):
            raise _error(
                relative_path,
                object_id,
                f"{collection}[{object_id}].match",
                "expected list",
            )
        for index, match in enumerate(record["match"]):
            _check_keys(
                relative_path,
                object_id,
                f"{collection}[{object_id}].match[{index}]",
                match,
                {"source", "id", "rel"},
            )
            match_path = f"{record_path}.match[{index}]"
            _check_required_keys(
                relative_path,
                object_id,
                match_path,
                match,
                {"source", "id", "rel"},
            )
            for field in ("source", "id", "rel"):
                _check_string(
                    relative_path,
                    object_id,
                    f"{match_path}.{field}",
                    match[field],
                )

    if "history" in record:
        history_path = f"{record_path}.history"
        if not isinstance(record["history"], list):
            raise _error(relative_path, object_id, history_path, "expected list")
        for index, event in enumerate(record["history"]):
            if not isinstance(event, Mapping):
                raise _error(
                    relative_path,
                    object_id,
                    f"{history_path}[{index}]",
                    "expected mapping",
                )


def _read_repository_inputs(repo_root: pathlib.Path) -> dict[str, bytes]:
    root = pathlib.Path(repo_root)
    inputs: dict[str, bytes] = {}
    for name, (relative_path, _) in _FILES.items():
        try:
            inputs[name] = (root / relative_path).read_bytes()
        except OSError as exc:
            raise ExportError(
                f"{relative_path}: object <document>: document: {exc}"
            ) from exc
    return inputs


def load_repository(
    repo_root: pathlib.Path,
    *,
    input_bytes: Mapping[str, bytes] | None = None,
) -> dict:
    """Load and validate the six formal vocabulary documents."""

    snapshot = input_bytes if input_bytes is not None else _read_repository_inputs(repo_root)
    documents: dict[str, dict] = {}
    for name, (relative_path, allowed_top) in _FILES.items():
        try:
            document = yaml.safe_load(snapshot[name].decode("utf-8"))
        except (KeyError, UnicodeError, yaml.YAMLError) as exc:
            raise ExportError(f"{relative_path}: object <document>: document: {exc}") from exc
        _check_keys(relative_path, "<document>", "document", document, allowed_top)
        _check_keys(relative_path, "<version>", "version", document.get("version"), {"id", "date", "note"})
        _check_required_keys(
            relative_path,
            "<version>",
            "version",
            document["version"],
            {"id", "date", "note"},
        )
        _check_string(relative_path, "<version>", "version.id", document["version"]["id"])
        if not isinstance(document["version"]["date"], datetime.date):
            raise _error(relative_path, "<version>", "version.date", "expected date")
        _check_string(relative_path, "<version>", "version.note", document["version"]["note"])
        for collection in allowed_top - {"version"}:
            records = document.get(collection)
            if not isinstance(records, list):
                raise _error(relative_path, "<document>", collection, "expected list")
            seen: set[str] = set()
            for index, record in enumerate(records):
                record_path = f"{collection}[{index}]"
                if not isinstance(record, Mapping):
                    raise _error(relative_path, "<missing-id>", record_path, "expected mapping")
                object_id = str(record.get("id", "<missing-id>"))
                _check_keys(
                    relative_path,
                    object_id,
                    f"{collection}[{object_id}]",
                    record,
                    _COLLECTION_FIELDS[(name, collection)],
                )
                if not _ID.fullmatch(object_id):
                    raise _error(relative_path, object_id, f"{collection}[{object_id}].id", "invalid stable ID")
                if object_id in seen:
                    raise _error(relative_path, object_id, f"{collection}[{object_id}].id", "duplicate stable ID")
                seen.add(object_id)
                _validate_record(name, relative_path, collection, record)
        documents[name] = document

    _validate_references(documents)
    return documents


def _index(records: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(record["id"]): record for record in records}


def _references(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _require_targets(
    relative_path: str,
    collection: str,
    record: Mapping[str, Any],
    field: str,
    targets: Mapping[str, Any],
) -> None:
    for index, target in enumerate(_references(record.get(field))):
        if target not in targets:
            suffix = f"[{index}]" if isinstance(record.get(field), list) else ""
            raise _error(
                relative_path,
                str(record["id"]),
                f"{collection}[{record['id']}].{field}{suffix}",
                f"missing reference {target}",
            )


def _validate_references(documents: Mapping[str, dict]) -> None:
    topics = _index(documents["topics"]["concepts"])
    arrays = _index(documents["topics"]["arrays"])
    entities = _index(documents["entities"]["entities"])
    sources = _index(documents["sources"]["sources"])
    form_arrays = _index(documents["forms"]["arrays"])

    for record in topics.values():
        for field in ("broader", "related", "replaced_by"):
            _require_targets("vocab/topics.yaml", "concepts", record, field, topics)
        _require_targets("vocab/topics.yaml", "concepts", record, "arrays", arrays)
        if record.get("source") != "self":
            _require_targets("vocab/topics.yaml", "concepts", record, "source", sources)
    for record in arrays.values():
        _require_targets("vocab/topics.yaml", "arrays", record, "superordinate", topics)
        _require_targets("vocab/topics.yaml", "arrays", record, "source", sources)
    for record in entities.values():
        _require_targets("vocab/entities.yaml", "entities", record, "subjects", topics)
        for field in ("vendor", "creator", "replaced_by"):
            _require_targets("vocab/entities.yaml", "entities", record, field, entities)
    for record in sources.values():
        _require_targets("vocab/sources.yaml", "sources", record, "entity", entities)
    for record in documents["forms"]["forms"]:
        _require_targets("vocab/forms.yaml", "forms", record, "arrays", form_arrays)
    for record in form_arrays.values():
        _require_targets("vocab/forms.yaml", "arrays", record, "source", sources)
        if record["superordinate"] != "forms":
            raise _error(
                "vocab/forms.yaml",
                str(record["id"]),
                f"arrays[{record['id']}].superordinate",
                f"unknown controlled-value root {record['superordinate']}",
            )
    for name, collection in (("types", "types"), ("genres", "genres"), ("forms", "forms")):
        records = _index(documents[name][collection])
        relative_path = _FILES[name][0]
        for record in records.values():
            for field in ("broader", "related", "replaced_by"):
                _require_targets(relative_path, collection, record, field, records)
            if record.get("source"):
                _require_targets(relative_path, collection, record, "source", sources)
    for name, collection in (
        ("topics", "concepts"),
        ("entities", "entities"),
        ("types", "types"),
        ("genres", "genres"),
        ("forms", "forms"),
    ):
        relative_path = _FILES[name][0]
        for record in documents[name][collection]:
            if collection != "entities":
                for language, basis in record.get("basis", {}).items():
                    if language in ("zh", "en") and isinstance(basis, dict):
                        errors = validate_basis(basis, record["label"].get(language), record,
                                                language, sources, collection=name)
                        if errors:
                            raise _error(relative_path, str(record["id"]),
                                         f"{collection}[{record['id']}].basis.{language}", "; ".join(errors))
            for index, match in enumerate(record.get("match", [])):
                if match.get("source") not in sources:
                    raise _error(
                        relative_path,
                        str(record["id"]),
                        f"{collection}[{record['id']}].match[{index}].source",
                        f"missing reference {match.get('source')}",
                    )


def display_label(record: Mapping[str, Any]) -> str:
    labels = record.get("label") or {}
    return str(labels.get("zh") or labels.get("en") or record["id"])


def _form_values(value: Any) -> list[str]:
    values = value if isinstance(value, list) else [value]
    return [str(item) for item in values if item is not None and str(item).strip()]


def aliases(record: Mapping[str, Any]) -> list[str]:
    main = display_label(record)
    language_maps = [record.get(field) or {} for field in ("label", "alt", "hidden")]
    languages = ["zh", "en"]
    languages.extend(
        language
        for values in language_maps
        for language in values
        if language not in languages
    )
    result: list[str] = []
    for language in languages:
        for values in language_maps:
            for value in _form_values(values.get(language)):
                if value != main and value not in result:
                    result.append(value)
    return result


def link(kind: str, object_id: str, label: str) -> str:
    singular = kind.lower().rstrip("s")
    try:
        directory = _KIND_DIRECTORIES[singular]
    except KeyError as exc:
        raise ExportError(f"unknown link kind: {kind}") from exc
    return f"[[kb/{directory}/{object_id}|{label}]]"


def _yaml_scalar(value: Any) -> str:
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    if isinstance(value, datetime.date):
        return value.isoformat()
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    raise ExportError(f"nested or unsupported property value: {value!r}")


def _frontmatter(properties: Mapping[str, Any]) -> str:
    lines = ["---"]
    for key, value in properties.items():
        if value is None or value == "" or value == []:
            continue
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {_yaml_scalar(item)}")
        else:
            lines.append(f"{key}: {_yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines)


def _table_cell(value: Any) -> str:
    if isinstance(value, (dict, list)):
        text = yaml.safe_dump(
            value,
            allow_unicode=True,
            default_flow_style=True,
            sort_keys=False,
            width=10_000,
        ).strip()
    elif isinstance(value, (datetime.date, datetime.datetime)):
        text = value.isoformat()
    else:
        text = str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\r\n", "<br>").replace("\n", "<br>")


def _table(title: str, headers: Sequence[str], rows: Iterable[Sequence[Any]]) -> str:
    materialized = list(rows)
    if not materialized:
        return ""
    lines = [f"## {title}", "", "| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(_table_cell(value) for value in row) + " |" for row in materialized)
    return "\n".join(lines)


def _form_rows(record: Mapping[str, Any], field: str) -> list[tuple[str, str]]:
    values = record.get(field) or {}
    return [
        (language, form)
        for language in ("zh", "en")
        for form in _form_values(values.get(language))
    ]


def _common_properties(record: Mapping[str, Any], object_kind: str, version: str) -> OrderedDict:
    properties = OrderedDict()
    properties["kb_id"] = record["id"]
    properties["kb_object"] = object_kind
    properties["kb_label"] = display_label(record)
    properties["kb_status"] = record.get("status")
    properties["kb_version"] = version
    properties["aliases"] = aliases(record) if "label" in record else []
    properties["tags"] = [f"kb-design/{object_kind}"]
    return properties


def _common_body(
    record: Mapping[str, Any],
    *,
    basis_title: str = "形式依据",
) -> list[str]:
    sections = [f"# {display_label(record)}"]
    if any(isinstance(value, dict) and value.get("level") == 5
           for language, value in (record.get("basis") or {}).items() if language in ("zh", "en")):
        sections.extend(("", "模型知识 · 第 5 级；外部用法未核实。"))
    if record.get("scope"):
        sections.extend(("", "## 范围", "", str(record["scope"])))
    for field, title in (("alt", "替代形式"), ("hidden", "隐藏形式")):
        table = _table(title, ("语言", "形式"), _form_rows(record, field))
        if table:
            sections.extend(("", table))
    basis = record.get("basis") or {}
    evidence_rows = []
    for language, value in basis.items():
        if language in ("zh", "en") and isinstance(value, dict):
            evidence_rows.extend((f"{language} · {title}", detail) for title, detail in basis_rows(value))
        else:
            evidence_rows.append((language, value))
    table = _table(basis_title, ("字段", "值"), evidence_rows)
    if table:
        sections.extend(("", table))
    matches = record.get("match") or []
    table = _table(
        "外部映射",
        ("source", "id", "rel"),
        ((item.get("source", ""), item.get("id", ""), item.get("rel", "")) for item in matches),
    )
    if table:
        sections.extend(("", table))
    if "history" in record:
        history = yaml.safe_dump(record["history"], allow_unicode=True, sort_keys=False).rstrip()
        sections.extend(("", "## 历史记录", "", "```yaml", history, "```"))
    return sections


def _note(properties: Mapping[str, Any], body_sections: Sequence[str]) -> bytes:
    text = _frontmatter(properties) + "\n" + "\n".join(body_sections).rstrip() + "\n"
    return text.replace("\r\n", "\n").encode("utf-8")


def _labels(index: Mapping[str, Mapping[str, Any]]) -> dict[str, str]:
    return {object_id: display_label(record) for object_id, record in index.items()}


def _render_topic(
    record: Mapping[str, Any],
    version: str,
    topic_labels: Mapping[str, str],
    array_labels: Mapping[str, str],
    source_labels: Mapping[str, str],
) -> bytes:
    properties = _common_properties(record, "topic", version)
    properties["kb_broader"] = [link("topic", item, topic_labels[item]) for item in record.get("broader", [])]
    properties["kb_related"] = [link("topic", item, topic_labels[item]) for item in record.get("related", [])]
    properties["kb_arrays"] = [link("array", item, array_labels[item]) for item in record.get("arrays", [])]
    if record.get("source"):
        source = str(record["source"])
        properties["kb_source"] = (
            link("source", source, source_labels[source])
            if source in source_labels
            else source
        )
    properties["kb_added"] = record.get("added")
    replaced = _references(record.get("replaced_by"))
    properties["kb_replaced_by"] = (
        link("topic", replaced[0], topic_labels[replaced[0]]) if replaced else None
    )
    return _note(properties, _common_body(record))


def _render_array(
    record: Mapping[str, Any],
    version: str,
    members: Sequence[str],
    topic_labels: Mapping[str, str],
    source_labels: Mapping[str, str],
) -> bytes:
    properties = _common_properties(record, "array", version)
    parent = str(record["superordinate"])
    source = str(record["source"])
    properties["kb_superordinate"] = link("topic", parent, topic_labels[parent])
    properties["kb_source"] = link("source", source, source_labels[source])
    properties["kb_members"] = [link("topic", item, topic_labels[item]) for item in members]
    body = [
        f"# {record['id']}",
        "",
        "## 分组说明",
        "",
        "本记录表示主题树内的分组，不改变成员主题的概念身份。",
    ]
    return _note(properties, body)


def _render_entity(
    record: Mapping[str, Any],
    version: str,
    topic_labels: Mapping[str, str],
    entity_labels: Mapping[str, str],
) -> bytes:
    properties = _common_properties(record, "entity", version)
    properties["kb_kind"] = record.get("kind")
    properties["kb_subjects"] = [link("topic", item, topic_labels[item]) for item in record.get("subjects", [])]
    for field in ("vendor", "creator", "replaced_by"):
        values = _references(record.get(field))
        links = [link("entity", item, entity_labels[item]) for item in values]
        properties[f"kb_{field}"] = links if isinstance(record.get(field), list) else (links[0] if links else None)
    for field in ("form", "tier", "url", "watch", "checked", "added"):
        properties[f"kb_{field}"] = record.get(field)
    properties["kb_entity_version"] = record.get("version")
    return _note(properties, _common_body(record, basis_title="归属依据"))


def _render_source(
    record: Mapping[str, Any],
    version: str,
    entity_labels: Mapping[str, str],
) -> bytes:
    properties = _common_properties(record, "source", version)
    entity = str(record["entity"])
    properties["kb_entity"] = link("entity", entity, entity_labels[entity])
    properties["kb_roles"] = list(record.get("role", []))
    properties["kb_checked"] = record.get("checked")
    body = [
        f"# {record['id']}",
        "",
        "## 用途说明",
        "",
        "本记录表示来源用途，不表示来源实体身份。",
    ]
    return _note(properties, body)


def _render_controlled(
    record: Mapping[str, Any],
    object_kind: str,
    version: str,
    labels: Mapping[str, str],
) -> bytes:
    properties = _common_properties(record, object_kind, version)
    properties["kb_broader"] = [link(object_kind, item, labels[item]) for item in record.get("broader", [])]
    properties["kb_related"] = [link(object_kind, item, labels[item]) for item in record.get("related", [])]
    properties["kb_arrays"] = list(record.get("arrays", []))
    properties["kb_source"] = record.get("source")
    properties["kb_added"] = record.get("added")
    replaced = _references(record.get("replaced_by"))
    properties["kb_replaced_by"] = (
        link(object_kind, replaced[0], labels[replaced[0]]) if replaced else None
    )
    return _note(properties, _common_body(record))


def _base(directory: str, name: str, order: Sequence[str]) -> bytes:
    document = {
        "filters": {
            "and": [f'file.inFolder("kb/{directory}")', 'file.ext == "md"']
        },
        "views": [
            {
                "type": "table",
                "name": name,
                "order": list(order),
            }
        ],
    }
    return yaml.safe_dump(
        document,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    ).encode("utf-8")


def _insert(files: dict[str, bytes], path: str, content: bytes) -> None:
    if path in files:
        raise ExportError(f"duplicate output path: {path}")
    files[path] = content


def _root_index(form_arrays: Sequence[Mapping[str, Any]]) -> bytes:
    table = _table(
        "载体数组",
        ("id", "superordinate", "source"),
        (
            (record["id"], record["superordinate"], record["source"])
            for record in form_arrays
        ),
    )
    return (
        "# 词表参考区\n\n"
        "本目录由 kb-design 的六份正式词表确定性生成，只提供 Obsidian 浏览与链接。\n\n"
        "对象路径使用稳定 ID；这里的修改不会回流正式词表。\n\n"
        f"{table}\n"
    ).encode("utf-8")


def build_content_files(
    repo_root: pathlib.Path,
    *,
    input_bytes: Mapping[str, bytes] | None = None,
) -> dict[str, bytes]:
    """Return deterministic vault-relative content without writing to disk."""

    documents = load_repository(repo_root, input_bytes=input_bytes)
    topics = _index(documents["topics"]["concepts"])
    arrays = _index(documents["topics"]["arrays"])
    entities = _index(documents["entities"]["entities"])
    sources = _index(documents["sources"]["sources"])
    types = _index(documents["types"]["types"])
    genres = _index(documents["genres"]["genres"])
    forms = _index(documents["forms"]["forms"])

    topic_labels = _labels(topics)
    entity_labels = _labels(entities)
    source_labels = {source_id: entity_labels[record["entity"]] for source_id, record in sources.items()}
    array_labels = {array_id: array_id for array_id in arrays}
    files: dict[str, bytes] = {}

    topic_version = str(documents["topics"]["version"]["id"])
    for object_id in sorted(topics):
        _insert(
            files,
            f"kb/topics/{object_id}.md",
            _render_topic(topics[object_id], topic_version, topic_labels, array_labels, source_labels),
        )

    members = {array_id: [] for array_id in arrays}
    for record in documents["topics"]["concepts"]:
        for array_id in record.get("arrays", []):
            members[array_id].append(str(record["id"]))
    for object_id in sorted(arrays):
        _insert(
            files,
            f"kb/arrays/{object_id}.md",
            _render_array(arrays[object_id], topic_version, members[object_id], topic_labels, source_labels),
        )

    entity_version = str(documents["entities"]["version"]["id"])
    for object_id in sorted(entities):
        _insert(
            files,
            f"kb/entities/{object_id}.md",
            _render_entity(entities[object_id], entity_version, topic_labels, entity_labels),
        )

    source_version = str(documents["sources"]["version"]["id"])
    for object_id in sorted(sources):
        _insert(
            files,
            f"kb/sources/{object_id}.md",
            _render_source(sources[object_id], source_version, entity_labels),
        )

    for object_kind, index in (("type", types), ("genre", genres), ("form", forms)):
        name = object_kind + "s"
        version = str(documents[name]["version"]["id"])
        directory = _KIND_DIRECTORIES[object_kind]
        labels = _labels(index)
        for object_id in sorted(index):
            _insert(
                files,
                f"kb/{directory}/{object_id}.md",
                _render_controlled(index[object_id], object_kind, version, labels),
            )

    _insert(files, "kb/views/topics.base", _base("topics", "topics", ("kb_id", "kb_label", "kb_status", "kb_broader")))
    _insert(files, "kb/views/entities.base", _base("entities", "entities", ("kb_id", "kb_label", "kb_status", "kb_kind")))
    _insert(files, "kb/views/sources.base", _base("sources", "sources", ("kb_id", "kb_label", "kb_entity", "kb_roles")))
    _insert(
        files,
        "index.md",
        _root_index(documents["forms"]["arrays"]),
    )
    return dict(sorted(files.items()))


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _deterministic_json(document: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    ).encode("utf-8")


def _manifest_identity(relative_path: str) -> tuple[str, str]:
    path = pathlib.PurePosixPath(relative_path)
    if path.is_absolute() or relative_path != path.as_posix() or ".." in path.parts:
        raise ExportError(f"unsafe output path: {relative_path}")
    if (
        relative_path != relative_path.lower()
        or any(character in relative_path for character in (" ", "_"))
        or "--" in relative_path
    ):
        raise ExportError(f"invalid output path casing: {relative_path}")
    if path.suffix not in {".md", ".base"}:
        raise ExportError(f"invalid output extension: {relative_path}")
    if relative_path == "index.md":
        return "index", path.stem
    if path.suffix == ".base" and path.parts[:2] == ("kb", "views"):
        return "base", path.stem
    if len(path.parts) == 3 and path.parts[0] == "kb" and path.suffix == ".md":
        try:
            object_kind = _DIRECTORY_KINDS[path.parts[1]]
        except KeyError as exc:
            raise ExportError(f"unknown output directory: {relative_path}") from exc
        if not _ID.fullmatch(path.stem):
            raise ExportError(f"invalid output ID: {relative_path}")
        return object_kind, path.stem
    raise ExportError(f"unknown output path: {relative_path}")


def build_manifest(
    repo_root: pathlib.Path,
    files: Mapping[str, bytes],
    *,
    input_bytes: Mapping[str, bytes] | None = None,
    exporter_bytes: bytes | None = None,
) -> bytes:
    """Build the deterministic manifest for generated content files."""

    snapshot = input_bytes if input_bytes is not None else _read_repository_inputs(repo_root)
    entries = []
    counts = {kind: 0 for kind in _KIND_DIRECTORIES}
    digest_input = bytearray()
    for relative_path, content in sorted(files.items()):
        if relative_path == "manifest.json":
            raise ExportError("manifest.json must not list itself")
        if not isinstance(content, bytes):
            raise ExportError(f"output content is not bytes: {relative_path}")
        object_kind, object_id = _manifest_identity(relative_path)
        content_sha256 = _sha256(content)
        entries.append(
            {
                "id": object_id,
                "object": object_kind,
                "path": relative_path,
                "sha256": content_sha256,
            }
        )
        if object_kind in counts:
            counts[object_kind] += 1
        digest_input.extend(
            f"{relative_path}\0{content_sha256}\n".encode("utf-8")
        )

    inputs = []
    for name, (relative_path, _) in _FILES.items():
        try:
            content = snapshot[name]
            document = yaml.safe_load(content.decode("utf-8"))
            version = document["version"]["id"]
        except (UnicodeError, yaml.YAMLError, KeyError, TypeError) as exc:
            raise ExportError(f"{relative_path}: cannot build manifest: {exc}") from exc
        inputs.append(
            {
                "path": relative_path,
                "sha256": _sha256(content),
                "version": str(version),
            }
        )

    if exporter_bytes is None:
        try:
            exporter_bytes = pathlib.Path(__file__).read_bytes()
        except OSError as exc:
            raise ExportError(f"cannot hash exporter: {exc}") from exc
    exporter_sha256 = _sha256(exporter_bytes)

    return _deterministic_json(
        {
            "content_files": len(entries),
            "content_sha256": _sha256(bytes(digest_input)),
            "exporter_sha256": exporter_sha256,
            "files": entries,
            "inputs": inputs,
            "object_counts": counts,
            "schema": "kb-design-obsidian-export",
            "schema_version": 1,
            "total_files": len(entries) + 1,
        }
    )


def _is_within(path: pathlib.Path, directory: pathlib.Path) -> bool:
    return path == directory or directory in path.parents


def _validate_output_path(repo_root: pathlib.Path, output: pathlib.Path) -> pathlib.Path:
    candidate = pathlib.Path(output).expanduser()
    if candidate.name in {"", ".", ".."}:
        raise ExportError(f"unsafe output path: {output}")
    if candidate.is_symlink():
        raise ExportError(f"output is a symbolic link: {output}")
    try:
        resolved = candidate.resolve(strict=False)
        root = pathlib.Path(repo_root).resolve(strict=True)
        home = pathlib.Path.home().resolve(strict=False)
    except OSError as exc:
        raise ExportError(f"cannot resolve output path: {exc}") from exc

    filesystem_root = pathlib.Path(resolved.anchor)
    if resolved in {root, home, filesystem_root}:
        raise ExportError(f"forbidden output path: {resolved}")
    for relative_path in ("vocab", "design", "concepts", "sources", "scripts", "tests"):
        if _is_within(resolved, root / relative_path):
            raise ExportError(f"output is inside protected directory: {resolved}")

    parent = resolved.parent
    if not parent.exists() or not parent.is_dir():
        raise ExportError(f"output parent is not an existing directory: {parent}")
    if resolved.exists():
        if not resolved.is_dir():
            raise ExportError(f"output exists and is not a directory: {resolved}")
        try:
            if next(resolved.iterdir(), None) is not None:
                raise ExportError(f"output directory is not empty: {resolved}")
        except OSError as exc:
            raise ExportError(f"cannot inspect output directory: {exc}") from exc
    return resolved


def _parse_frontmatter(relative_path: str, content: bytes) -> Mapping[str, Any]:
    try:
        text = content.decode("utf-8")
        if not text.startswith("---\n"):
            raise ExportError(f"missing frontmatter: {relative_path}")
        _, frontmatter, _ = text.split("---\n", 2)
        properties = yaml.safe_load(frontmatter)
    except (UnicodeError, ValueError, yaml.YAMLError) as exc:
        raise ExportError(f"invalid frontmatter: {relative_path}: {exc}") from exc
    if not isinstance(properties, Mapping):
        raise ExportError(f"invalid frontmatter mapping: {relative_path}")
    return properties


def _validate_written_export(
    directory: pathlib.Path,
    content_files: Mapping[str, bytes],
    manifest_bytes: bytes,
) -> dict[str, Any]:
    expected = dict(content_files)
    expected["manifest.json"] = manifest_bytes
    actual_paths = {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if path.is_file()
    }
    if actual_paths != set(expected):
        missing = sorted(set(expected) - actual_paths)
        extra = sorted(actual_paths - set(expected))
        raise ExportError(f"written file set mismatch: missing={missing}, extra={extra}")

    readback = {}
    for relative_path, expected_content in sorted(expected.items()):
        path = directory / relative_path
        if path.is_symlink():
            raise ExportError(f"written file is a symbolic link: {relative_path}")
        try:
            actual_content = path.read_bytes()
        except OSError as exc:
            raise ExportError(f"cannot read written file {relative_path}: {exc}") from exc
        if _sha256(actual_content) != _sha256(expected_content):
            raise ExportError(f"written file hash mismatch: {relative_path}")
        readback[relative_path] = actual_content

    for relative_path, content in readback.items():
        if relative_path.endswith(".md"):
            if relative_path == "index.md":
                try:
                    content.decode("utf-8")
                except UnicodeError as exc:
                    raise ExportError(f"invalid Markdown: {relative_path}: {exc}") from exc
            else:
                _parse_frontmatter(relative_path, content)
        elif relative_path.endswith(".base"):
            try:
                document = yaml.safe_load(content)
            except yaml.YAMLError as exc:
                raise ExportError(f"invalid Base YAML: {relative_path}: {exc}") from exc
            if not isinstance(document, Mapping):
                raise ExportError(f"invalid Base mapping: {relative_path}")

    unresolved = []
    for relative_path, content in readback.items():
        if not relative_path.endswith(".md"):
            continue
        for target in _WIKILINK.findall(content.decode("utf-8")):
            if not target.startswith("kb/"):
                raise ExportError(
                    f"written link is not vault-root kb path: {relative_path} -> {target}"
                )
            target_path = target if target.endswith(".base") else f"{target}.md"
            if target_path not in content_files:
                unresolved.append((relative_path, target))
    if unresolved:
        raise ExportError(f"unresolved written link: {unresolved[0][0]} -> {unresolved[0][1]}")

    try:
        manifest = json.loads(readback["manifest.json"])
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ExportError(f"invalid manifest JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise ExportError("invalid manifest mapping")
    if _deterministic_json(manifest) != manifest_bytes:
        raise ExportError(
            "manifest does not use the required deterministic JSON serialization"
        )
    manifest_paths = {entry.get("path") for entry in manifest.get("files", [])}
    if manifest_paths != set(content_files):
        raise ExportError("manifest file coverage mismatch")
    for entry in manifest["files"]:
        relative_path = entry["path"]
        if entry.get("sha256") != _sha256(readback[relative_path]):
            raise ExportError(f"manifest file hash mismatch: {relative_path}")
    if manifest.get("content_files") != len(content_files):
        raise ExportError("manifest content count mismatch")
    if manifest.get("total_files") != len(readback):
        raise ExportError("manifest total count mismatch")
    digest_input = b"".join(
        f"{path}\0{_sha256(readback[path])}\n".encode("utf-8")
        for path in sorted(content_files)
    )
    if manifest.get("content_sha256") != _sha256(digest_input):
        raise ExportError("manifest content hash mismatch")
    return manifest


def write_export(repo_root: pathlib.Path, output: pathlib.Path) -> dict:
    """Write a validated export by replacing only a new or empty directory."""

    destination = _validate_output_path(repo_root, output)
    input_bytes = _read_repository_inputs(repo_root)
    try:
        exporter_bytes = pathlib.Path(__file__).read_bytes()
    except OSError as exc:
        raise ExportError(f"cannot hash exporter: {exc}") from exc
    content_files = build_content_files(repo_root, input_bytes=input_bytes)
    manifest_bytes = build_manifest(
        repo_root,
        content_files,
        input_bytes=input_bytes,
        exporter_bytes=exporter_bytes,
    )
    temporary = None
    try:
        temporary = pathlib.Path(
            tempfile.mkdtemp(
                prefix=f".{destination.name}.tmp-",
                dir=destination.parent,
            )
        )
        for relative_path, content in content_files.items():
            path = temporary / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        (temporary / "manifest.json").write_bytes(manifest_bytes)
        manifest = _validate_written_export(temporary, content_files, manifest_bytes)
        os.replace(temporary, destination)
        temporary = None
    except BaseException:
        if temporary is not None and temporary.exists():
            shutil.rmtree(temporary)
        raise

    return {
        "content_files": manifest["content_files"],
        "content_sha256": manifest["content_sha256"],
        "output": str(destination),
        "total_files": manifest["total_files"],
    }


def main(argv=None) -> int:
    parser = _ArgumentParser(description="Export formal vocabularies for Obsidian")
    parser.add_argument("--repo-root", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    try:
        arguments = parser.parse_args(argv)
        summary = write_export(arguments.repo_root, arguments.output)
    except Exception as exc:
        print(f"OBSIDIAN_EXPORT_ERROR {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            summary,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
