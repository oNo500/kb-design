"""Build the application-owned files that accompany a verified reference export."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import yaml

from .design_source import DesignSnapshot
from .errors import ApplicationError
from .render import render_frontmatter


def _yaml_bytes(value: object) -> bytes:
    return yaml.safe_dump(
        value,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).encode("utf-8")


_TEMPLATES = {
    "app/templates/inbox.md": render_frontmatter({"tags": ["inbox"]}) + "# 收件箱\n",
    "app/templates/reference.md": render_frontmatter({"aliases": [], "tags": ["reference"]}) + "# 参考\n",
}


def _base(
    name: str, *filters: str,
    order: tuple[str, ...] = ("file.link", "file.mtime"),
) -> dict[str, object]:
    return {
        "filters": {"and": list(filters)},
        "views": [{"type": "table", "name": name, "order": list(order)}],
    }


_CONTENT_FILTERS = ('file.inFolder("content")', 'file.ext == "md"')
_CONTENT_COLUMNS = ("file.link", "title", "kb_type", "kb_subjects", "kb_status")
_TOPIC_COLUMNS = ("file.link", "kb_label", "kb_status", "kb_broader")
_VIEWS = {
    "app/views/inbox.base": _base("Inbox", 'file.inFolder("inbox")', 'file.ext == "md"'),
    "app/views/sources.base": _base("外部资料", 'file.inFolder("sources")', 'file.ext == "md"'),
    "app/views/content.base": _base("全部内容", *_CONTENT_FILTERS, order=_CONTENT_COLUMNS),
    "app/views/drafts.base": _base("草稿", *_CONTENT_FILTERS, 'kb_status == "draft"', order=_CONTENT_COLUMNS),
    "app/views/recently-modified.base": _base(
        "最近修改", *_CONTENT_FILTERS, order=(*_CONTENT_COLUMNS, "file.mtime", "kb_modified"),
    ),
    "app/views/indexes.base": _base("人工索引", 'file.inFolder("indexes")', 'file.ext == "md"'),
    "app/views/formal-topics.base": _base(
        "正式主题", 'file.inFolder("kb/topics")', 'file.ext == "md"', order=_TOPIC_COLUMNS,
    ),
    "app/views/unassigned-topics.base": _base(
        "未分配主题",
        'file.inFolder("kb/topics")',
        'file.ext == "md"',
        'kb_status == "unassigned"',
        order=_TOPIC_COLUMNS,
    ),
}

_RULES = {"app/rules/index.md": "# 应用规则\n\n`kb/` 与 `app/` 由应用管理；用户内容不回流到设计源。\n"}


def _reference_files(reference_root: Path) -> dict[str, bytes]:
    kb_root = reference_root / "kb"
    if not kb_root.is_dir() or kb_root.is_symlink():
        raise ApplicationError("verified reference export has no kb directory")
    files: dict[str, bytes] = {}
    try:
        candidates = list(kb_root.rglob("*"))
    except OSError as exc:
        raise ApplicationError(f"cannot inspect verified reference export: {exc}") from exc
    for path in candidates:
        if path.is_symlink():
            raise ApplicationError(f"verified reference export contains a symbolic link: {path}")
        if not path.is_file():
            continue
        relative_path = path.relative_to(reference_root).as_posix()
        try:
            files[relative_path] = path.read_bytes()
        except OSError as exc:
            raise ApplicationError(f"cannot read verified reference file {relative_path}: {exc}") from exc
    if not files:
        raise ApplicationError("verified reference export is empty")
    return files


def build_managed_files(snapshot: DesignSnapshot, reference_root: Path) -> Mapping[str, bytes]:
    """Combine Task 2's verified ``kb/`` tree with application-managed files."""
    del snapshot  # The snapshot's authority is established by ``export_reference``.
    files = _reference_files(reference_root)
    files.update({path: text.encode("utf-8") for path, text in _TEMPLATES.items()})
    files.update({path: _yaml_bytes(view) for path, view in _VIEWS.items()})
    files.update({path: text.encode("utf-8") for path, text in _RULES.items()})
    return dict(sorted(files.items()))
