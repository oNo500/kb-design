#!/usr/bin/env python3
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


REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[2]
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
    "本文件由术语记录确定生成，只读；如需修改，请编辑 `vocab/terms.yaml`。"
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
) -> Mapping[str, Any]:
    return {
        "schema": _get(document, "schema"),
        "version": _get(document, "version"),
        "source_index_sha256": hashlib.sha256(
            canonical_json(source_index)
        ).hexdigest(),
        "cutover_decision": _get(state, "decision"),
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
) -> bytes:
    _ensure_consumers_enabled(state)
    active = tuple(
        concept
        for concept in _get(document, "concepts")
        if _get(concept, "workflow") == "active"
    )
    return canonical_json(
        _snapshot_value(document, active, source_index, state)
    )


def ordered_concepts(document: Any, layout: Mapping[str, object]) -> Tuple[Any, ...]:
    groups = sorted(
        layout["groups"], key=lambda group: (group["order"], group["id"])
    )
    group_order = {
        group["id"]: index for index, group in enumerate(groups)
    }

    def concept_key(concept: Any) -> Tuple[int, str]:
        group_indexes = sorted(
            group_order[_get(field, "topic_id")]
            for field in _get(concept, "subject_fields")
            if _get(field, "topic_id") in group_order
        )
        if not group_indexes:
            raise ValueError(
                "TERM_LAYOUT_GROUP_MISSING " + _get(concept, "id")
            )
        return group_indexes[0], _get(concept, "id")

    return tuple(sorted(_get(document, "concepts"), key=concept_key))


def _preferred_texts(concept: Any) -> Mapping[str, str]:
    preferred = {}
    for language in _get(concept, "languages"):
        terms = [
            term
            for term in _get(language, "terms")
            if _get(term, "administrative_status") == PREFERRED
        ]
        if len(terms) != 1:
            raise ValueError(
                "TERM_PREFERRED_TERM_COUNT "
                + _get(concept, "id")
                + " "
                + _get(language, "language")
            )
        preferred[_get(language, "language")] = _get(terms[0], "text")
    return preferred


def _definition_text(concept: Any) -> str:
    definitions = sorted(
        _get_optional(concept, "definitions", ()),
        key=lambda definition: (
            LANGUAGE_ORDER[_get(definition, "language")],
            _get(definition, "text"),
        ),
    )
    return _get(definitions[0], "text") if definitions else "—"


def _admitted_texts(concept: Any) -> str:
    values = []
    for language in _get(concept, "languages"):
        language_tag = _get(language, "language")
        for term in _get(language, "terms"):
            if _get(term, "administrative_status") == ADMITTED:
                values.append(
                    (
                        LANGUAGE_ORDER[language_tag],
                        _get(term, "id"),
                        language_tag + "：" + _get(term, "text"),
                    )
                )
    return "；".join(value[2] for value in sorted(values)) or "—"


def _markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _concept_row(concept: Any) -> str:
    preferred = _preferred_texts(concept)
    chinese = "；".join(
        preferred[language]
        for language in ("zh-Hans", "zh-Hant")
        if language in preferred
    ) or "—"
    english = preferred.get("en", "—")
    cells = (
        chinese,
        english,
        _definition_text(concept),
        _admitted_texts(concept),
        _get(concept, "id"),
    )
    return "| " + " | ".join(_markdown_cell(cell) for cell in cells) + " |"


def _historical_rows(concepts: Sequence[Any]) -> Sequence[str]:
    rows = []
    for concept in concepts:
        for language in _get(concept, "languages"):
            for term in _get(language, "terms"):
                status = _get(term, "administrative_status")
                if status not in HISTORICAL:
                    continue
                cells = (
                    _get(term, "text"),
                    _get(language, "language"),
                    status,
                    _get_optional(term, "replaced_by", "—"),
                    _get(concept, "id"),
                )
                rows.append(
                    (
                        _get(concept, "id"),
                        LANGUAGE_ORDER[_get(language, "language")],
                        STATUS_ORDER[status],
                        _get(term, "id"),
                        "| "
                        + " | ".join(_markdown_cell(cell) for cell in cells)
                        + " |",
                    )
                )
    return tuple(row[4] for row in sorted(rows))


def render_glossary(
    snapshot: Mapping[str, object],
    layout: Mapping[str, object],
    state: Any,
) -> str:
    _ensure_consumers_enabled(state)
    active_snapshot = {
        "concepts": [
            concept
            for concept in snapshot["concepts"]
            if concept["workflow"] == "active"
        ]
    }
    concepts = ordered_concepts(active_snapshot, layout)
    snapshot_sha256 = hashlib.sha256(canonical_json(snapshot)).hexdigest()
    lines = [
        "# 术语表 (Glossary)",
        READ_ONLY_DECLARATION,
        "",
        "快照 SHA-256：`" + snapshot_sha256 + "`。",
        "",
        "## " + layout["source_abbreviations"]["title"],
        "",
        "出处名称与定位从同一快照绑定的来源索引读取。",
    ]
    groups = sorted(
        layout["groups"], key=lambda group: (group["order"], group["id"])
    )
    for group in groups:
        group_concepts = [
            concept
            for concept in concepts
            if group["id"]
            in {
                _get(field, "topic_id")
                for field in _get(concept, "subject_fields")
            }
        ]
        lines.extend(
            [
                "",
                "## " + group["title"],
                "",
                "| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |",
                "|---|---|---|---|---|",
            ]
        )
        lines.extend(_concept_row(concept) for concept in group_concepts)

    history_rows = _historical_rows(concepts)
    lines.extend(["", "## 历史形式", ""])
    if history_rows:
        lines.extend(
            [
                "| 形式 | 语言 | 状态 | 替代术语 ID | 概念 ID |",
                "|---|---|---|---|---|",
                *history_rows,
            ]
        )
    else:
        lines.append("无。")
    lines.extend(
        [
            "",
            "## " + layout["standards_appendix"]["title"],
            "",
            "标准与文献引用从术语记录和来源索引读取。",
            "",
        ]
    )
    return "\n".join(lines)


def _load_yaml(path: pathlib.Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _outputs(arguments: argparse.Namespace) -> Tuple[bytes, bytes]:
    document = _load_yaml(arguments.terms)
    state = load_cutover_state(arguments.state)
    layout = _load_yaml(arguments.layout)
    source_index = _load_json(arguments.source_index)
    snapshot = canonical_snapshot(document, source_index, state)
    glossary = render_glossary(json.loads(snapshot), layout, state).encode("utf-8")
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
        subparser.add_argument("--terms", required=True, type=pathlib.Path)
        subparser.add_argument("--state", required=True, type=pathlib.Path)
        subparser.add_argument("--layout", required=True, type=pathlib.Path)
        subparser.add_argument("--source-index", required=True, type=pathlib.Path)
        subparser.add_argument("--snapshot-out", required=True, type=pathlib.Path)
        subparser.add_argument("--glossary-out", required=True, type=pathlib.Path)
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
