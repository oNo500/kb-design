"""Create one validated, user-owned Obsidian content draft without overwriting files."""

from __future__ import annotations

import datetime as dt
import os
import shutil
import tempfile
import uuid
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Callable

from .design_source import DesignSnapshot
from .errors import ApplicationError
from .render import render_frontmatter
from .validation import _LEVELS, _REFERENCE_KINDS, _entries, validate_content


_LANGUAGES = frozenset({"zh", "en"})


def _vault_content_root(vault: Path) -> Path:
    candidate = Path(vault)
    if candidate.is_symlink():
        raise ApplicationError(f"vault must not be a symbolic link: {candidate}")
    try:
        root = candidate.resolve(strict=True)
    except OSError as exc:
        raise ApplicationError(f"vault does not exist: {candidate}") from exc
    if not root.is_dir():
        raise ApplicationError(f"vault is not a directory: {root}")
    content_root = root / "Content"
    if content_root.is_symlink() or not content_root.is_dir():
        raise ApplicationError(f"vault Content directory is missing or unsafe: {content_root}")
    return content_root


def _identifier(value: object, *, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ApplicationError(f"{name} must be a nonempty identifier")
    return value


def _label(record: Mapping[str, object], language: str, *, name: str) -> str:
    labels = record.get("label")
    if not isinstance(labels, Mapping):
        raise ApplicationError(f"{name} has no display labels in the design snapshot")
    value = labels.get(language, labels.get("en"))
    if not isinstance(value, str) or not value or any(character in value for character in "[]\r\n"):
        raise ApplicationError(f"{name} has no safe display label for language {language}")
    return value


def _target(
    identifier: object,
    known: Mapping[str, Mapping[str, object]],
    prefix: str,
    language: str,
    *,
    name: str,
) -> str:
    value = _identifier(identifier, name=name)
    if "/" in value or any(character in value for character in "[]|#\r\n"):
        raise ApplicationError(f"{name} is not a safe controlled identifier: {value!r}")
    try:
        record = known[value]
    except KeyError as exc:
        raise ApplicationError(f"unknown {name}: {value}") from exc
    label = _label(record, language, name=name)
    return f"[[{prefix}{value}|{label}]]"


def _identifier_list(value: object, *, name: str, required: bool) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ApplicationError(f"{name} must be a list of identifiers")
    identifiers = tuple(_identifier(item, name=name) for item in value)
    if required and not identifiers:
        raise ApplicationError(f"{name} must contain at least one identifier")
    return identifiers


def _canonical_uuid4(value: object) -> str:
    try:
        parsed = value if isinstance(value, uuid.UUID) else uuid.UUID(str(value))
    except (TypeError, ValueError, AttributeError) as exc:
        raise ApplicationError("uuid_factory must return a UUIDv4") from exc
    identifier = str(parsed)
    if parsed.version != 4:
        raise ApplicationError("uuid_factory must return a UUIDv4")
    return identifier


def _readback(snapshot: DesignSnapshot, temporary: Path, destination: Path, identifier: str) -> None:
    try:
        with tempfile.TemporaryDirectory(prefix=".kb-obsidian-create-check-", dir=destination.parent) as directory:
            check_root = Path(directory)
            check_content = check_root / "Content"
            check_content.mkdir()
            check_note = check_content / destination.name
            shutil.copyfile(temporary, check_note)
            result = validate_content(snapshot, check_root)
    except OSError as exc:
        raise ApplicationError(f"cannot read back staged content: {exc}") from exc
    relative_path = Path("Content") / destination.name
    record = next(
        (item for item in result.valid_records if item.path == relative_path and item.identifier == identifier),
        None,
    )
    if record is None or any(issue.path == relative_path for issue in result.issues):
        raise ApplicationError("content readback validation failed")


def _write_temporary(content_root: Path, identifier: str, rendered: bytes) -> Path:
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=f".{identifier}.",
            suffix=".md",
            dir=content_root,
            delete=False,
        ) as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
            return Path(handle.name)
    except OSError as exc:
        raise ApplicationError(f"cannot stage content: {exc}") from exc


def _publish_without_overwrite(temporary: Path, destination: Path) -> bool:
    try:
        os.link(temporary, destination)
    except FileExistsError:
        return False
    except OSError as exc:
        raise ApplicationError(f"cannot publish content: {exc}") from exc
    try:
        os.replace(temporary, destination)
    except OSError as exc:
        try:
            if os.path.samestat(temporary.stat(), destination.stat()):
                destination.unlink()
        except FileNotFoundError:
            pass
        except OSError as cleanup_error:
            raise ApplicationError(f"cannot clean failed content publication: {cleanup_error}") from cleanup_error
        raise ApplicationError(f"cannot finalize content publication: {exc}") from exc
    return True


def create_content(
    snapshot: DesignSnapshot,
    vault: Path,
    *,
    title: str,
    type_id: str,
    genre_id: str,
    subjects: Sequence[str],
    form: str | None = None,
    level: str | None = None,
    entities: Sequence[str] = (),
    references: Sequence[str] = (),
    language: str = "zh",
    uuid_factory: Callable[[], uuid.UUID] = uuid.uuid4,
    today: Callable[[], dt.date] = dt.date.today,
) -> Path:
    """Create one canonical UUIDv4 draft after validating all controlled inputs."""
    content_root = _vault_content_root(vault)
    if not isinstance(title, str) or not title.strip() or "\r" in title or "\n" in title:
        raise ApplicationError("title must be nonempty single-line text")
    if language not in _LANGUAGES:
        raise ApplicationError(f"unsupported content language: {language!r}")
    if not callable(uuid_factory) or not callable(today):
        raise ApplicationError("uuid_factory and today must be callable")

    topics = _entries(snapshot, "topics", "concepts")
    entities_by_id = _entries(snapshot, "entities", "entities")
    types = _entries(snapshot, "types", "types")
    genres = _entries(snapshot, "genres", "genres")
    forms = _entries(snapshot, "forms", "forms")

    subject_ids = _identifier_list(subjects, name="subjects", required=True)
    entity_ids = _identifier_list(entities, name="entities", required=False)
    reference_ids = _identifier_list(references, name="references", required=False)
    for subject in subject_ids:
        if topics.get(subject, {}).get("status") == "deprecated":
            raise ApplicationError(f"subject is deprecated: {subject}")

    properties: dict[str, object] = {
        "title": title,
        "aliases": [title],
        "kb_type": _target(type_id, types, "KB/Types/", language, name="type"),
        "kb_genre": _target(genre_id, genres, "KB/Genres/", language, name="genre"),
        "kb_subjects": [
            _target(subject, topics, "KB/Topics/", language, name="subject") for subject in subject_ids
        ],
    }
    if form is not None:
        properties["kb_form"] = _target(form, forms, "KB/Forms/", language, name="form")
    if level is not None:
        if not isinstance(level, str) or level not in _LEVELS:
            raise ApplicationError(f"unknown cognitive level: {level!r}")
        properties["kb_level"] = level
    if entity_ids:
        properties["kb_entities"] = [
            _target(entity, entities_by_id, "KB/Entities/", language, name="entity") for entity in entity_ids
        ]
    if reference_ids:
        for reference in reference_ids:
            record = entities_by_id.get(reference)
            if record is None:
                raise ApplicationError(f"unknown reference: {reference}")
            if record.get("kind") not in _REFERENCE_KINDS:
                raise ApplicationError(f"reference must target a standard or publication: {reference}")
        properties["kb_references"] = [
            _target(reference, entities_by_id, "KB/Entities/", language, name="reference")
            for reference in reference_ids
        ]
    try:
        created = today()
    except Exception as exc:
        raise ApplicationError(f"cannot determine content creation date: {exc}") from exc
    if not isinstance(created, dt.date) or isinstance(created, dt.datetime):
        raise ApplicationError("today must return a date")
    properties["kb_created"] = created.isoformat()
    properties["kb_status"] = "draft"
    properties["kb_language"] = language

    while True:
        identifier = _canonical_uuid4(uuid_factory())
        destination = content_root / f"{identifier}.md"
        if os.path.lexists(destination):
            continue
        rendered_properties = {"kb_id": identifier, **properties}
        rendered = (render_frontmatter(rendered_properties) + f"# {title}\n").encode("utf-8")
        temporary = _write_temporary(content_root, identifier, rendered)
        try:
            _readback(snapshot, temporary, destination, identifier)
            if _publish_without_overwrite(temporary, destination):
                return destination
        finally:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass
            except OSError as exc:
                raise ApplicationError(f"cannot clean staged content: {exc}") from exc
