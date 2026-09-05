"""Command-line composition for the kb-obsidian application flows."""

from __future__ import annotations

import argparse
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Mapping, Optional, Sequence

import yaml

from .create_content import create_content
from .design_source import load_design
from .errors import ApplicationError
from .reports import write_reports
from .validation import ValidationResult, validate_content
from .vault import initialize_vault


_ERROR_PREFIX = "KB_OBSIDIAN_ERROR: "
_SEEN_SINGLE_OPTIONS = "_kb_obsidian_seen_single_options"


class _StoreOnce(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: object,
        option_string: Optional[str] = None,
    ) -> None:
        seen = getattr(namespace, _SEEN_SINGLE_OPTIONS, None)
        if seen is None:
            seen = set()
            setattr(namespace, _SEEN_SINGLE_OPTIONS, seen)
        if self.dest in seen:
            parser.error(f"argument {option_string or self.dest}: may not be repeated")
        seen.add(self.dest)
        setattr(namespace, self.dest, values)


class _ArgumentParser(argparse.ArgumentParser):
    def add_argument(self, *args: object, **kwargs: object) -> argparse.Action:
        kwargs.setdefault("action", _StoreOnce)
        return super().add_argument(*args, **kwargs)

    def error(self, message: str) -> None:
        raise ApplicationError(f"argument error: {message}")


def _parser() -> argparse.ArgumentParser:
    parser = _ArgumentParser(prog="kb-obsidian")
    commands = parser.add_subparsers(dest="command", required=True)

    initialize = commands.add_parser("init", help="initialize a new empty vault")
    initialize.add_argument("--design-root", required=True, type=Path)
    initialize.add_argument("--output", required=True, type=Path)

    refresh = commands.add_parser("refresh", help="refresh vocabulary references in an existing vault")
    refresh.add_argument("--design-root", required=True, type=Path)
    refresh.add_argument("--vault", required=True, type=Path)
    refresh.add_argument("--dry-run", action="store_true", help="validate and show changes without modifying the vault")

    new_content = commands.add_parser("new-content", help="create one validated draft")
    new_content.add_argument("--design-root", required=True, type=Path)
    new_content.add_argument("--vault", required=True, type=Path)
    new_content.add_argument("--title", required=True)
    new_content.add_argument("--type", required=True, dest="type_id")
    new_content.add_argument("--genre", required=True, dest="genre_id")
    new_content.add_argument("--subject", required=True, action="append", dest="subjects")
    new_content.add_argument("--entity", action="append", default=[], dest="entities")
    new_content.add_argument("--reference", action="append", default=[], dest="references")
    new_content.add_argument("--form")
    new_content.add_argument("--level")
    new_content.add_argument("--language", default="zh")

    validate = commands.add_parser("validate", help="validate content metadata and references")
    validate.add_argument("--design-root", required=True, type=Path)
    validate.add_argument("--vault", required=True, type=Path)

    report = commands.add_parser("report", help="refresh derived usage reports")
    report.add_argument("--design-root", required=True, type=Path)
    report.add_argument("--vault", required=True, type=Path)

    return parser


def _validation_summary(validation: ValidationResult) -> Mapping[str, object]:
    return {
        "is_valid": validation.is_valid,
        "issue_count": len(validation.issues),
        "issues": [
            {
                "code": issue.code,
                "field": issue.field,
                "message": issue.message,
                "path": issue.path.as_posix(),
            }
            for issue in validation.issues
        ],
        "record_count": len(validation.records),
        "valid_record_count": len(validation.valid_records),
    }


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _error(message: str) -> None:
    detail = " ".join(message.splitlines()).strip() or "unknown application error"
    sys.stderr.write(f"{_ERROR_PREFIX}{detail}\n")


def _run(arguments: argparse.Namespace) -> tuple[Mapping[str, object], bool]:
    if arguments.command == "init":
        return initialize_vault(arguments.design_root, arguments.output), False
    if arguments.command == "refresh":
        from .refresh import refresh_vocabulary
        return refresh_vocabulary(arguments.design_root, arguments.vault, dry_run=arguments.dry_run), False

    snapshot = load_design(arguments.design_root)
    if arguments.command == "new-content":
        path = create_content(
            snapshot,
            arguments.vault,
            title=arguments.title,
            type_id=arguments.type_id,
            genre_id=arguments.genre_id,
            subjects=arguments.subjects,
            form=arguments.form,
            level=arguments.level,
            entities=arguments.entities,
            references=arguments.references,
            language=arguments.language,
        )
        return {"path": str(path.resolve(strict=True))}, False

    validation = validate_content(snapshot, arguments.vault)
    if arguments.command == "validate":
        return _validation_summary(validation), not validation.is_valid
    if arguments.command == "report":
        return write_reports(snapshot, validation, arguments.vault), False
    raise ApplicationError(f"unknown command: {arguments.command}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Parse arguments, invoke one public flow, and emit the stable CLI contract."""
    try:
        arguments = _parser().parse_args(argv)
        with redirect_stdout(io.StringIO()):
            payload, failed = _run(arguments)
    except (ApplicationError, OSError, UnicodeError, yaml.YAMLError, json.JSONDecodeError) as exc:
        _error(str(exc))
        return 1

    encoded = _json(payload)
    if failed:
        _error(encoded)
        return 1
    sys.stdout.write(encoded + "\n")
    return 0
