"""Semantic validation for read-only Obsidian content records."""

from __future__ import annotations

import datetime as dt
import re
import uuid
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from .content import ContentRecord, _ParsedContent, _parse_content
from .design_source import DesignSnapshot
from .errors import ApplicationError
from .vault import verify_vault


_LEVELS = frozenset({"remember", "understand", "apply", "analyze", "evaluate", "create"})
_STATUSES = frozenset({"draft", "active", "deprecated"})
_REFERENCE_KINDS = frozenset({"standard", "publication"})
_LINK = re.compile(r"^\[\[([^\[\]|#^\r\n]+)(?:\|([^\[\]\r\n]+))?\]\]$")
_TARGET_PREFIXES = {
    "type": "kb/types/",
    "genre": "kb/genres/",
    "form": "kb/forms/",
    "topic": "kb/topics/",
    "entity": "kb/entities/",
    "content": "content/",
}


@dataclass(frozen=True)
class Issue:
    code: str
    path: Path
    field: str
    message: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", Path(self.path))


@dataclass(frozen=True)
class ValidationResult:
    records: Tuple[ContentRecord, ...]
    issues: Tuple[Issue, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "records", tuple(self.records))
        object.__setattr__(self, "issues", tuple(self.issues))

    @property
    def valid_records(self) -> Tuple[ContentRecord, ...]:
        invalid_paths = {issue.path for issue in self.issues}
        return tuple(record for record in self.records if record.path not in invalid_paths)

    @property
    def is_valid(self) -> bool:
        return not self.issues


def _entries(snapshot: DesignSnapshot, document: str, collection: str) -> dict[str, Mapping[str, object]]:
    value = snapshot.documents.get(document)
    if not isinstance(value, Mapping):
        raise ApplicationError(f"design document {document} must be a mapping")
    records = value.get(collection)
    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        raise ApplicationError(f"design collection {document}.{collection} must be a list")
    result: dict[str, Mapping[str, object]] = {}
    for record in records:
        if not isinstance(record, Mapping) or not isinstance(record.get("id"), str):
            raise ApplicationError(f"design collection {document}.{collection} has an invalid record")
        result[record["id"]] = record
    return result


def _add(issues: list[Issue], record: ContentRecord, code: str, field: str, message: str) -> None:
    issues.append(Issue(code, record.path, field, message))


def _required_text(record: ContentRecord, field: str, issues: list[Issue]) -> Optional[str]:
    value = record.properties.get(field)
    if value is None:
        _add(issues, record, "content.required", field, f"required property is missing: {field}")
        return None
    if not isinstance(value, str) or not value:
        _add(issues, record, "content.cardinality", field, f"property must be one nonempty Text value: {field}")
        return None
    return value


def _optional_text(record: ContentRecord, field: str, issues: list[Issue]) -> Optional[str]:
    if field not in record.properties:
        return None
    value = record.properties[field]
    if not isinstance(value, str) or not value:
        _add(issues, record, "content.cardinality", field, f"property must be one nonempty Text value: {field}")
        return None
    return value


def _text_list(
    record: ContentRecord,
    field: str,
    issues: list[Issue],
    *,
    required: bool,
) -> Optional[Tuple[str, ...]]:
    if field not in record.properties:
        if required:
            _add(issues, record, "content.required", field, f"required property is missing: {field}")
        return None
    value = record.properties[field]
    if not isinstance(value, tuple) or not all(isinstance(item, str) and item for item in value):
        _add(issues, record, "content.cardinality", field, f"property must be a List of nonempty Text values: {field}")
        return None
    if required and not value:
        _add(issues, record, "content.cardinality", field, f"property must contain at least one value: {field}")
        return None
    return value


def _parse_link(value: str) -> Optional[tuple[str, str]]:
    match = _LINK.fullmatch(value)
    if match is None:
        return None
    target = match.group(1)
    for kind, prefix in _TARGET_PREFIXES.items():
        if target.startswith(prefix):
            identifier = target[len(prefix) :]
            if identifier and "/" not in identifier and target == f"{prefix}{identifier}":
                return kind, identifier
    return None


def _controlled_scalar(
    record: ContentRecord,
    field: str,
    expected_kind: str,
    known: Mapping[str, Mapping[str, object]],
    issues: list[Issue],
    *,
    required: bool,
) -> Optional[str]:
    value = _required_text(record, field, issues) if required else _optional_text(record, field, issues)
    if value is None:
        return None
    parsed = _parse_link(value)
    if parsed is None or parsed[0] != expected_kind:
        _add(
            issues,
            record,
            "content.reference_kind",
            field,
            f"property must use an exact {_TARGET_PREFIXES[expected_kind]}<id> Wikilink",
        )
        return None
    identifier = parsed[1]
    if identifier not in known:
        _add(issues, record, "content.reference_missing", field, f"controlled target does not exist: {identifier}")
        return None
    return identifier


def _controlled_list(
    record: ContentRecord,
    field: str,
    expected_kind: str,
    known: Mapping[str, Mapping[str, object]],
    issues: list[Issue],
    *,
    required: bool,
) -> Tuple[str, ...]:
    values = _text_list(record, field, issues, required=required)
    if values is None:
        return ()
    identifiers: list[str] = []
    for value in values:
        parsed = _parse_link(value)
        if parsed is None or parsed[0] != expected_kind:
            _add(
                issues,
                record,
                "content.reference_kind",
                field,
                f"property must use exact {_TARGET_PREFIXES[expected_kind]}<id> Wikilinks: {value}",
            )
            continue
        identifier = parsed[1]
        if identifier not in known:
            _add(issues, record, "content.reference_missing", field, f"controlled target does not exist: {identifier}")
            continue
        identifiers.append(identifier)
    return tuple(identifiers)


def _date_value(record: ContentRecord, field: str, issues: list[Issue], *, required: bool) -> None:
    if field not in record.properties:
        if required:
            _add(issues, record, "content.required", field, f"required property is missing: {field}")
        return
    value = record.properties[field]
    if isinstance(value, dt.datetime):
        valid = False
    elif isinstance(value, dt.date):
        valid = True
    elif isinstance(value, str):
        try:
            valid = dt.date.fromisoformat(value).isoformat() == value
        except ValueError:
            valid = False
    else:
        valid = False
    if not valid:
        _add(issues, record, "content.invalid_date", field, f"property must be an ISO 8601 date: {field}")


def _is_canonical_uuid4(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError):
        return False
    return parsed.version == 4 and str(parsed) == value


def _has_valid_content_identity(record: ContentRecord) -> bool:
    return _is_canonical_uuid4(record.identifier) and record.path.stem == record.identifier


def _validate_identity(record: ContentRecord, heading: Optional[str], issues: list[Issue]) -> None:
    identifier = _required_text(record, "kb_id", issues)
    if identifier is not None:
        if not _is_canonical_uuid4(identifier):
            _add(issues, record, "content.invalid_id", "kb_id", "kb_id must be canonical lowercase UUIDv4")
        if record.path.stem != identifier:
            _add(issues, record, "content.path_mismatch", "kb_id", "content filename stem must equal kb_id")

    title = record.properties.get("title")
    aliases = record.properties.get("aliases")
    title_matches = (
        isinstance(title, str)
        and bool(title)
        and heading == title
        and isinstance(aliases, tuple)
        and aliases == (title,)
    )
    if heading is not None and not title_matches:
        _add(
            issues,
            record,
            "content.title_mismatch",
            "title",
            "title, first-level heading, and the single derived alias must match exactly",
        )


def _validate_content_targets(
    records: Tuple[ContentRecord, ...],
    issues: list[Issue],
    duplicate_identifiers: set[str],
) -> None:
    by_path = {record.path.as_posix(): record for record in records}
    relation_targets: dict[Path, set[Path]] = defaultdict(set)

    def resolve(record: ContentRecord, field: str, value: str) -> Optional[ContentRecord]:
        parsed = _parse_link(value)
        if parsed is None or parsed[0] != "content":
            _add(
                issues,
                record,
                "content.reference_kind",
                field,
                "property must use an exact content/<UUIDv4> Wikilink",
            )
            return None
        if not _is_canonical_uuid4(parsed[1]):
            _add(
                issues,
                record,
                "content.reference_invalid_identity",
                field,
                f"content target is not a canonical UUIDv4: {parsed[1]}",
            )
            return None
        target_path = f"content/{parsed[1]}.md"
        target = by_path.get(target_path)
        if target is None:
            _add(issues, record, "content.reference_missing", field, f"content target does not exist: {parsed[1]}")
            return None
        if (
            target.identifier != parsed[1]
            or not _has_valid_content_identity(target)
            or parsed[1] in duplicate_identifiers
        ):
            _add(
                issues,
                record,
                "content.reference_invalid_identity",
                field,
                f"content target does not have one unique path-consistent identity: {parsed[1]}",
            )
            return None
        if target.path == record.path:
            _add(issues, record, "content.self_reference", field, f"property must not reference itself: {field}")
            return None
        return target

    for record in records:
        source = record.properties.get("kb_source")
        if isinstance(source, str):
            parsed_source = _parse_link(source)
            if parsed_source is not None and parsed_source[0] == "content":
                resolve(record, "kb_source", source)

        replacement = record.properties.get("kb_is_replaced_by")
        status = record.properties.get("kb_status")
        if replacement is not None:
            if status != "deprecated":
                _add(
                    issues,
                    record,
                    "content.invalid_lifecycle",
                    "kb_is_replaced_by",
                    "kb_is_replaced_by is allowed only for deprecated content",
                )
            if isinstance(replacement, str):
                resolve(record, "kb_is_replaced_by", replacement)
        elif status == "deprecated" and not record.body.strip():
            _add(
                issues,
                record,
                "content.invalid_lifecycle",
                "kb_status",
                "deprecated content without a replacement needs a reason in its first body paragraph",
            )

        relation = record.properties.get("kb_relation")
        if isinstance(relation, tuple):
            for value in relation:
                if not isinstance(value, str):
                    continue
                target = resolve(record, "kb_relation", value)
                if target is not None:
                    relation_targets[record.path].add(target.path)

    checked_pairs: set[tuple[str, str]] = set()
    for source_path, targets in relation_targets.items():
        for target_path in sorted(targets, key=lambda path: path.as_posix()):
            pair = tuple(sorted((source_path.as_posix(), target_path.as_posix())))
            if pair in checked_pairs:
                continue
            checked_pairs.add(pair)
            if source_path not in relation_targets.get(target_path, set()):
                for path in (source_path, target_path):
                    record = by_path[path.as_posix()]
                    _add(
                        issues,
                        record,
                        "content.relation_not_reciprocal",
                        "kb_relation",
                        f"relation is not reciprocal between {source_path} and {target_path}",
                    )


def _validate_content_tree(snapshot: DesignSnapshot, content_root: Path) -> ValidationResult:
    """Validate one content directory without asserting that its parent is a complete vault."""
    if content_root.is_symlink() or not content_root.is_dir():
        raise ApplicationError(f"vault content directory is missing or unsafe: {content_root}")

    topics = _entries(snapshot, "topics", "concepts")
    entities = _entries(snapshot, "entities", "entities")
    types = _entries(snapshot, "types", "types")
    genres = _entries(snapshot, "genres", "genres")
    forms = _entries(snapshot, "forms", "forms")

    parsed_files: list[_ParsedContent] = []
    issues: list[Issue] = []
    try:
        paths = sorted(content_root.glob("*.md"), key=lambda path: path.name)
    except OSError as exc:
        raise ApplicationError(f"cannot inspect vault content: {exc}") from exc
    for path in paths:
        relative_path = Path("content") / path.name
        parsed = _parse_content(path, relative_path)
        parsed_files.append(parsed)
        issues.extend(Issue(issue.code, relative_path, issue.field, issue.message) for issue in parsed.issues)

    records = tuple(parsed.record for parsed in parsed_files if parsed.record is not None)
    headings = {
        parsed.record.path: parsed.heading
        for parsed in parsed_files
        if parsed.record is not None
    }
    for record in records:
        _validate_identity(record, headings[record.path], issues)
        _controlled_scalar(record, "kb_type", "type", types, issues, required=True)
        _controlled_scalar(record, "kb_genre", "genre", genres, issues, required=True)
        _controlled_scalar(record, "kb_form", "form", forms, issues, required=False)

        level = _optional_text(record, "kb_level", issues)
        if level is not None and level not in _LEVELS:
            _add(issues, record, "content.controlled_value", "kb_level", f"unknown cognitive level: {level}")

        subject_ids = _controlled_list(record, "kb_subjects", "topic", topics, issues, required=True)
        for identifier in subject_ids:
            if topics[identifier].get("status") == "deprecated":
                _add(
                    issues,
                    record,
                    "content.deprecated_subject",
                    "kb_subjects",
                    f"subject is deprecated: {identifier}",
                )
        _controlled_list(record, "kb_entities", "entity", entities, issues, required=False)

        source = _optional_text(record, "kb_source", issues)
        if source is not None:
            parsed_source = _parse_link(source)
            if parsed_source is None or parsed_source[0] not in {"content", "entity"}:
                _add(
                    issues,
                    record,
                    "content.reference_kind",
                    "kb_source",
                    "kb_source must be an exact content or kb/entities Wikilink",
                )
            elif parsed_source[0] == "entity" and parsed_source[1] not in entities:
                _add(
                    issues,
                    record,
                    "content.reference_missing",
                    "kb_source",
                    f"source entity does not exist: {parsed_source[1]}",
                )

        reference_ids = _controlled_list(
            record,
            "kb_references",
            "entity",
            entities,
            issues,
            required=False,
        )
        for identifier in reference_ids:
            if entities[identifier].get("kind") not in _REFERENCE_KINDS:
                _add(
                    issues,
                    record,
                    "content.reference_entity_kind",
                    "kb_references",
                    f"references target must be a standard or publication: {identifier}",
                )

        _date_value(record, "kb_created", issues, required=True)
        _date_value(record, "kb_modified", issues, required=False)

        status = _required_text(record, "kb_status", issues)
        if status is not None and status not in _STATUSES:
            _add(issues, record, "content.controlled_value", "kb_status", f"unknown content status: {status}")

        _optional_text(record, "kb_is_replaced_by", issues)
        _text_list(record, "kb_relation", issues, required=False)
        _optional_text(record, "kb_language", issues)

    owners: dict[str, list[ContentRecord]] = defaultdict(list)
    for record in records:
        if record.identifier:
            owners[record.identifier].append(record)
    duplicate_identifiers = {identifier for identifier, owner_records in owners.items() if len(owner_records) > 1}
    for identifier, duplicate_records in owners.items():
        if len(duplicate_records) > 1:
            for record in duplicate_records:
                _add(issues, record, "content.duplicate_id", "kb_id", f"duplicate content identifier: {identifier}")

    _validate_content_targets(records, issues, duplicate_identifiers)
    ordered_records = tuple(sorted(records, key=lambda record: record.path.as_posix()))
    ordered_issues = tuple(
        sorted(
            issues,
            key=lambda issue: (issue.path.as_posix(), issue.field, issue.code, issue.message),
        )
    )
    return ValidationResult(ordered_records, ordered_issues)


def validate_content(snapshot: DesignSnapshot, vault: Path) -> ValidationResult:
    """Verify a vault binding, then read and validate direct ``content/*.md`` children."""
    root = verify_vault(snapshot, vault)
    return _validate_content_tree(snapshot, root / "content")
