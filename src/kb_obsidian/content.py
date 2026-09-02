"""Read immutable content records from Obsidian Markdown without rewriting them."""

from __future__ import annotations

import datetime as dt
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Optional, Tuple

import yaml


CONTENT_PROPERTIES = frozenset(
    {
        "kb_id",
        "title",
        "aliases",
        "kb_type",
        "kb_genre",
        "kb_form",
        "kb_level",
        "kb_subjects",
        "kb_entities",
        "kb_source",
        "kb_references",
        "kb_created",
        "kb_modified",
        "kb_status",
        "kb_is_replaced_by",
        "kb_relation",
        "kb_language",
    }
)

_HEADING = re.compile(r"^#[ \t]+(.+?)[ \t]*$")


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


@dataclass(frozen=True)
class ContentRecord:
    identifier: str
    title: str
    path: Path
    properties: Mapping[str, object]
    body: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", Path(self.path))
        object.__setattr__(self, "properties", _freeze(self.properties))


@dataclass(frozen=True)
class _ParseIssue:
    code: str
    field: str
    message: str


@dataclass(frozen=True)
class _ParsedContent:
    record: Optional[ContentRecord]
    heading: Optional[str]
    issues: Tuple[_ParseIssue, ...]


class _DuplicateProperty(yaml.YAMLError):
    def __init__(self, key: object) -> None:
        super().__init__(f"duplicate property: {key}")
        self.key = key


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in result
        except TypeError as exc:
            raise yaml.YAMLError(f"unhashable property name: {key!r}") from exc
        if duplicate:
            raise _DuplicateProperty(key)
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _is_scalar(value: object) -> bool:
    return value is None or isinstance(value, (str, int, float, bool, dt.date))


def _property_shape_issues(properties: Mapping[object, object]) -> list[_ParseIssue]:
    issues: list[_ParseIssue] = []
    for key, value in properties.items():
        field = str(key)
        if not isinstance(key, str):
            issues.append(_ParseIssue("content.property_shape", field, "property names must be text"))
            continue
        if key.startswith("kb_") and key not in CONTENT_PROPERTIES:
            issues.append(_ParseIssue("content.unknown_property", key, f"unknown content property: {key}"))
        if _is_scalar(value):
            continue
        if isinstance(value, list) and all(_is_scalar(item) for item in value):
            continue
        issues.append(
            _ParseIssue(
                "content.property_shape",
                key,
                "frontmatter properties must be flat scalars or lists of scalars",
            )
        )
    return issues


def _parse_content(path: Path, relative_path: Path) -> _ParsedContent:
    issues: list[_ParseIssue] = []
    if path.is_symlink():
        return _ParsedContent(
            None,
            None,
            (_ParseIssue("content.read", "", "content files must not be symbolic links"),),
        )
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return _ParsedContent(None, None, (_ParseIssue("content.read", "", f"cannot read content: {exc}"),))
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return _ParsedContent(None, None, (_ParseIssue("content.encoding", "", f"content is not UTF-8: {exc}"),))

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        return _ParsedContent(
            None,
            None,
            (_ParseIssue("content.frontmatter", "", "content must start with YAML frontmatter"),),
        )
    closing = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.rstrip("\r\n") == "---"),
        None,
    )
    if closing is None:
        return _ParsedContent(
            None,
            None,
            (_ParseIssue("content.frontmatter", "", "leading YAML frontmatter is not closed"),),
        )

    frontmatter = "".join(lines[1:closing])
    try:
        loaded = yaml.load(frontmatter, Loader=_UniqueKeyLoader)
    except _DuplicateProperty as exc:
        return _ParsedContent(
            None,
            None,
            (_ParseIssue("content.duplicate_property", str(exc.key), str(exc)),),
        )
    except yaml.YAMLError as exc:
        return _ParsedContent(None, None, (_ParseIssue("content.frontmatter", "", f"invalid YAML: {exc}"),))
    if not isinstance(loaded, Mapping):
        return _ParsedContent(
            None,
            None,
            (_ParseIssue("content.frontmatter", "", "frontmatter must be a property mapping"),),
        )
    issues.extend(_property_shape_issues(loaded))

    markdown_lines = lines[closing + 1 :]
    first_nonblank = next((index for index, line in enumerate(markdown_lines) if line.strip()), None)
    if first_nonblank is not None and markdown_lines[first_nonblank].rstrip("\r\n") == "---":
        issues.append(
            _ParseIssue(
                "content.frontmatter",
                "",
                "content must have exactly one leading YAML frontmatter block",
            )
        )
    headings = [
        (index, match.group(1))
        for index, line in enumerate(markdown_lines)
        if (match := _HEADING.fullmatch(line.rstrip("\r\n")))
    ]
    heading: Optional[str] = None
    body = "".join(markdown_lines)
    if len(headings) != 1 or first_nonblank is None or headings[0][0] != first_nonblank:
        issues.append(
            _ParseIssue(
                "content.heading",
                "title",
                "content must have exactly one first-level heading as its first Markdown content",
            )
        )
    else:
        heading_index, heading = headings[0]
        body = "".join(markdown_lines[heading_index + 1 :])

    identifier = loaded.get("kb_id")
    title = loaded.get("title")
    record = ContentRecord(
        identifier=identifier if isinstance(identifier, str) else "",
        title=title if isinstance(title, str) else "",
        path=relative_path,
        properties=loaded,
        body=body,
    )
    return _ParsedContent(record, heading, tuple(issues))
