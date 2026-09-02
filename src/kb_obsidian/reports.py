"""Build deterministic diagnostics and publish only the report write set."""

from __future__ import annotations

import ctypes
import json
import os
import re
import shutil
import sys
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .design_source import DesignSnapshot
from .errors import ApplicationError
from .validation import ValidationResult
from .vault import verify_vault


_REPORT_PREFIX = "App/Reports/"
_REPORT_NAMES = frozenset(
    {
        "README.md",
        "topic-coverage.md",
        "topic-usage.json",
        "unassigned-topics.md",
        "validation.json",
    }
)
_SUBJECT_LINK = re.compile(r"^\[\[KB/Topics/([^/|\]#^\r\n]+)(?:\|[^\[\]\r\n]+)?\]\]$")
_OVERUSE_THRESHOLD = 0.1
_AT_FDCWD = -2
_RENAME_SWAP = 0x00000002


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _topic_records(snapshot: DesignSnapshot) -> dict[str, dict[str, object]]:
    document = snapshot.documents.get("topics")
    if not isinstance(document, Mapping):
        raise ApplicationError("design document topics must be a mapping")
    concepts = document.get("concepts")
    if not isinstance(concepts, Sequence) or isinstance(concepts, (str, bytes)):
        raise ApplicationError("design collection topics.concepts must be a list")

    topics: dict[str, dict[str, object]] = {}
    for concept in concepts:
        if not isinstance(concept, Mapping):
            raise ApplicationError("design collection topics.concepts has an invalid record")
        identifier = concept.get("id")
        status = concept.get("status")
        source = concept.get("source")
        broader = concept.get("broader")
        if not isinstance(identifier, str) or not identifier:
            raise ApplicationError("formal topic has an invalid id")
        if identifier in topics:
            raise ApplicationError(f"formal topic id is duplicated: {identifier}")
        if not isinstance(status, str) or not isinstance(source, str):
            raise ApplicationError(f"formal topic metadata is invalid: {identifier}")
        if (
            not isinstance(broader, Sequence)
            or isinstance(broader, (str, bytes))
            or not all(isinstance(parent, str) and parent for parent in broader)
        ):
            raise ApplicationError(f"formal topic broader relation is invalid: {identifier}")
        topics[identifier] = {
            "id": identifier,
            "status": status,
            "source": source,
            "broader": tuple(broader),
        }

    known = set(topics)
    for identifier, topic in topics.items():
        unknown = set(topic["broader"]) - known
        if unknown:
            raise ApplicationError(
                f"formal topic broader target does not exist: {identifier} -> {sorted(unknown)[0]}"
            )
    return topics


def _ancestor_sets(topics: Mapping[str, Mapping[str, object]]) -> dict[str, frozenset[str]]:
    cache: dict[str, frozenset[str]] = {}
    active: set[str] = set()

    def visit(identifier: str) -> frozenset[str]:
        if identifier in cache:
            return cache[identifier]
        if identifier in active:
            raise ApplicationError(f"formal topic broader relation contains a cycle: {identifier}")
        active.add(identifier)
        ancestors: set[str] = set()
        try:
            for parent in topics[identifier]["broader"]:
                ancestors.add(parent)
                ancestors.update(visit(parent))
        finally:
            active.remove(identifier)
        cache[identifier] = frozenset(ancestors)
        return cache[identifier]

    for identifier in sorted(topics):
        visit(identifier)
    return cache


def _subject_ids(validation: ValidationResult, topics: Mapping[str, object]) -> list[str]:
    identifiers: list[str] = []
    for record in validation.valid_records:
        values = record.properties.get("kb_subjects")
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            raise ApplicationError(f"valid record has invalid kb_subjects: {record.path}")
        for value in values:
            if not isinstance(value, str):
                raise ApplicationError(f"valid record has invalid kb_subjects: {record.path}")
            match = _SUBJECT_LINK.fullmatch(value)
            if match is None or match.group(1) not in topics:
                raise ApplicationError(f"valid record has invalid kb_subjects: {record.path}")
            identifiers.append(match.group(1))
    return identifiers


def _usage(snapshot: DesignSnapshot, validation: ValidationResult) -> dict[str, object]:
    topics = _topic_records(snapshot)
    ancestors = _ancestor_sets(topics)
    direct = {identifier: 0 for identifier in sorted(topics)}
    for identifier in _subject_ids(validation, topics):
        direct[identifier] += 1

    aggregate = dict(direct)
    for identifier, count in direct.items():
        for ancestor in ancestors[identifier]:
            aggregate[ancestor] += count

    total_direct = sum(direct.values())
    topic_rows = [
        {
            "id": identifier,
            "status": topics[identifier]["status"],
            "source": topics[identifier]["source"],
            "broader": list(topics[identifier]["broader"]),
            "direct": direct[identifier],
            "aggregate": aggregate[identifier],
        }
        for identifier in sorted(topics)
    ]
    signals = {
        "overuse": [
            identifier
            for identifier in sorted(topics)
            if total_direct and direct[identifier] / total_direct >= _OVERUSE_THRESHOLD
        ],
        "unassigned": [
            identifier
            for identifier in sorted(topics)
            if topics[identifier]["status"] == "unassigned"
        ],
        "zero_reference": [identifier for identifier in sorted(topics) if direct[identifier] == 0],
    }
    return {
        "schema": "kb-obsidian-topic-usage",
        "schema_version": 1,
        "design_commit": snapshot.commit,
        "valid_content_count": len(validation.valid_records),
        "total_direct_references": total_direct,
        "overuse_threshold": _OVERUSE_THRESHOLD,
        "direct": direct,
        "aggregate": aggregate,
        "topics": topic_rows,
        "signals": signals,
    }


def _validation_report(snapshot: DesignSnapshot, validation: ValidationResult) -> dict[str, object]:
    issues = sorted(
        validation.issues,
        key=lambda issue: (issue.path.as_posix(), issue.field, issue.code, issue.message),
    )
    return {
        "schema": "kb-obsidian-validation",
        "schema_version": 1,
        "design_commit": snapshot.commit,
        "is_valid": validation.is_valid,
        "record_count": len(validation.records),
        "valid_record_count": len(validation.valid_records),
        "issue_count": len(issues),
        "issues": [
            {
                "code": issue.code,
                "path": issue.path.as_posix(),
                "field": issue.field,
                "message": issue.message,
            }
            for issue in issues
        ],
    }


def _markdown_value(value: object) -> str:
    if isinstance(value, (list, tuple)):
        text = ", ".join(str(item) for item in value) or "—"
    else:
        text = str(value)
    return text.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _coverage_markdown(usage: Mapping[str, Any]) -> bytes:
    lines = [
        "# 主题覆盖",
        "",
        "本报告是从通过校验的受控内容字段重算的派生结果，仅供人工复核；它不会自动修改内容或正式主题。",
        "",
        "| 主题 ID | 状态 | 来源 | 上位 | 直接计数 | 分支聚合 |",
        "|---|---|---|---|---:|---:|",
    ]
    for topic in usage["topics"]:
        lines.append(
            "| "
            + " | ".join(
                _markdown_value(topic[key])
                for key in ("id", "status", "source", "broader", "direct", "aggregate")
            )
            + " |"
        )
    return ("\n".join(lines) + "\n").encode("utf-8")


def _signal_section(
    title: str,
    identifiers: Sequence[str],
    by_id: Mapping[str, Mapping[str, object]],
    *,
    total_direct: int,
) -> list[str]:
    lines = [f"## {title}", ""]
    if not identifiers:
        return lines + ["无。", ""]
    lines.extend(
        (
            "| 主题 ID | 状态 | 来源 | 上位 | 直接计数 | 分支聚合 | 引用占比 |",
            "|---|---|---|---|---:|---:|---:|",
        )
    )
    for identifier in identifiers:
        topic = by_id[identifier]
        ratio = topic["direct"] / total_direct if total_direct else 0
        values = (
            topic["id"],
            topic["status"],
            topic["source"],
            topic["broader"],
            topic["direct"],
            topic["aggregate"],
            f"{ratio:.1%}",
        )
        lines.append("| " + " | ".join(_markdown_value(value) for value in values) + " |")
    lines.append("")
    return lines


def _signals_markdown(usage: Mapping[str, Any]) -> bytes:
    by_id = {topic["id"]: topic for topic in usage["topics"]}
    signals = usage["signals"]
    lines = [
        "# 主题复核",
        "",
        "本报告是可删除、可重算的派生线索，仅供人工复核；阈值命中不会自动批准、废弃、删除、拆分或修改正式数据。",
        "",
    ]
    lines.extend(
        _signal_section(
            "未分配主题",
            signals["unassigned"],
            by_id,
            total_direct=usage["total_direct_references"],
        )
    )
    lines.extend(
        _signal_section(
            "零引用主题",
            signals["zero_reference"],
            by_id,
            total_direct=usage["total_direct_references"],
        )
    )
    lines.extend(
        [
            "## 过度使用",
            "",
            "现行复核阈值为单个主题的直接引用占全部直接引用至少 10%。",
            "",
        ]
    )
    overuse = signals["overuse"]
    if overuse:
        lines.extend(
            _signal_section(
                "阈值命中",
                overuse,
                by_id,
                total_direct=usage["total_direct_references"],
            )
        )
    else:
        lines.extend(["无。", ""])
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def _readme_markdown() -> bytes:
    return (
        "# 维护报告\n\n"
        "此目录只保存从本次输入重算的派生报告，仅供人工复核；报告不会自动修改内容、正式数据、状态或决定。\n\n"
        "- [内容校验](validation.json)\n"
        "- [主题使用](topic-usage.json)\n"
        "- [主题覆盖](topic-coverage.md)\n"
        "- [主题复核](unassigned-topics.md)\n"
    ).encode("utf-8")


def build_reports(
    snapshot: DesignSnapshot,
    validation: ValidationResult,
    vault: Path,
) -> Mapping[str, bytes]:
    """Build reports without reading vault links, indexes, aliases, or prior reports."""
    del vault
    usage = _usage(snapshot, validation)
    return {
        "App/Reports/README.md": _readme_markdown(),
        "App/Reports/topic-coverage.md": _coverage_markdown(usage),
        "App/Reports/topic-usage.json": _json_bytes(usage),
        "App/Reports/unassigned-topics.md": _signals_markdown(usage),
        "App/Reports/validation.json": _json_bytes(_validation_report(snapshot, validation)),
    }


def _verify_report_tree(root: Path, reports: Mapping[str, bytes]) -> None:
    try:
        children = list(root.iterdir())
    except OSError as exc:
        raise ApplicationError(f"cannot inspect staged reports: {exc}") from exc
    actual_names = {path.name for path in children if path.is_file() and not path.is_symlink()}
    if len(children) != len(_REPORT_NAMES) or actual_names != _REPORT_NAMES:
        raise ApplicationError("generated report file set mismatch")
    for relative_path, expected in reports.items():
        name = relative_path.removeprefix(_REPORT_PREFIX)
        path = root / name
        try:
            actual = path.read_bytes()
        except OSError as exc:
            raise ApplicationError(f"cannot read generated report {path}: {exc}") from exc
        if actual != expected:
            raise ApplicationError(f"generated report bytes differ: {relative_path}")


def _rename_swap(first: Path, second: Path) -> None:
    """Atomically exchange two existing paths on the current Darwin platform."""
    if sys.platform != "darwin":
        raise ApplicationError(
            f"atomic report directory exchange is unavailable on platform: {sys.platform}"
        )
    try:
        renameatx_np = ctypes.CDLL(None, use_errno=True).renameatx_np
    except (AttributeError, OSError) as exc:
        raise ApplicationError("atomic report directory exchange is unavailable") from exc
    renameatx_np.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    renameatx_np.restype = ctypes.c_int
    ctypes.set_errno(0)
    result = renameatx_np(
        _AT_FDCWD,
        os.fsencode(first),
        _AT_FDCWD,
        os.fsencode(second),
        _RENAME_SWAP,
    )
    if result != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), f"{first} <-> {second}")


def write_reports(
    snapshot: DesignSnapshot,
    validation: ValidationResult,
    vault: Path,
) -> Mapping[str, object]:
    """Replace ``App/Reports`` only after a same-parent staged tree verifies."""
    root = verify_vault(snapshot, vault)
    generated = build_reports(snapshot, validation, vault)
    app = root / "App"
    reports_root = app / "Reports"
    if root.is_symlink() or not root.is_dir():
        raise ApplicationError(f"vault is missing or unsafe: {root}")
    if app.is_symlink() or not app.is_dir():
        raise ApplicationError(f"vault App directory is missing or unsafe: {app}")
    if reports_root.is_symlink() or (reports_root.exists() and not reports_root.is_dir()):
        raise ApplicationError(f"vault Reports directory is unsafe: {reports_root}")

    try:
        temporary = Path(tempfile.mkdtemp(prefix=".reports-tmp-", dir=app))
    except OSError as exc:
        raise ApplicationError(f"cannot create report staging directory: {exc}") from exc
    staged = temporary / "new"
    had_old = reports_root.exists()
    cleanup_temporary = True
    try:
        staged.mkdir()
        for relative_path, content in generated.items():
            name = relative_path.removeprefix(_REPORT_PREFIX)
            if name not in _REPORT_NAMES or "/" in name:
                raise ApplicationError(f"unsafe generated report path: {relative_path}")
            (staged / name).write_bytes(content)
        _verify_report_tree(staged, generated)

        if had_old:
            try:
                _rename_swap(staged, reports_root)
            except (ApplicationError, OSError) as exc:
                raise ApplicationError(f"cannot publish reports: {exc}") from exc
            try:
                _verify_report_tree(reports_root, generated)
            except (ApplicationError, OSError) as exc:
                try:
                    _rename_swap(staged, reports_root)
                except (ApplicationError, OSError) as restore_exc:
                    cleanup_temporary = False
                    raise ApplicationError(
                        "cannot restore old reports after publication failure: "
                        f"{restore_exc}; old reports preserved at {staged.resolve()}"
                    ) from exc
                raise ApplicationError(f"cannot publish reports: {exc}") from exc
        else:
            os.replace(staged, reports_root)
            try:
                _verify_report_tree(reports_root, generated)
            except (ApplicationError, OSError) as exc:
                try:
                    os.replace(reports_root, staged)
                except OSError as restore_exc:
                    cleanup_temporary = False
                    raise ApplicationError(
                        "cannot retract new reports after publication failure: "
                        f"{restore_exc}; generated reports remain at {reports_root.resolve()}"
                    ) from exc
                raise ApplicationError(f"cannot publish reports: {exc}") from exc
    except ApplicationError:
        raise
    except OSError as exc:
        raise ApplicationError(f"cannot publish reports: {exc}") from exc
    finally:
        if cleanup_temporary:
            shutil.rmtree(temporary, ignore_errors=True)

    return {
        "design_commit": snapshot.commit,
        "files": sorted(generated),
        "issue_count": len(validation.issues),
        "valid_record_count": len(validation.valid_records),
    }
