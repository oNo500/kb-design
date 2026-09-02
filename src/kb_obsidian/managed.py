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
    "App/Templates/inbox.md": render_frontmatter({"tags": ["inbox"]}) + "# 收件箱\n",
    "App/Templates/reference.md": render_frontmatter({"aliases": [], "tags": ["reference"]}) + "# 参考\n",
}


def _base(name: str, *filters: str, order: tuple[str, ...] = ()) -> dict[str, object]:
    return {
        "filters": {"and": list(filters)},
        "views": [{"type": "table", "name": name, "order": list(order)}],
    }


_CONTENT_FILTERS = ('file.inFolder("Content")', 'file.ext == "md"')
_VIEWS = {
    "App/Views/inbox.base": _base("Inbox", 'file.inFolder("Inbox")', 'file.ext == "md"'),
    "App/Views/sources.base": _base("外部资料", 'file.inFolder("Sources")', 'file.ext == "md"'),
    "App/Views/content.base": _base("全部内容", *_CONTENT_FILTERS),
    "App/Views/drafts.base": _base("草稿", *_CONTENT_FILTERS, 'kb_status == "draft"'),
    "App/Views/recently-modified.base": _base("最近修改", *_CONTENT_FILTERS, order=("kb_modified",)),
    "App/Views/indexes.base": _base("人工索引", 'file.inFolder("Indexes")', 'file.ext == "md"'),
    "App/Views/formal-topics.base": _base("正式主题", 'file.inFolder("KB/Topics")', 'file.ext == "md"'),
    "App/Views/unassigned-topics.base": _base(
        "未分配主题",
        'file.inFolder("KB/Topics")',
        'file.ext == "md"',
        'kb_status == "unassigned"',
    ),
}

_RULES = {
    "App/Rules/README.md": "# 应用规则\n\n`KB/` 与 `App/` 由应用管理；用户内容不回流到设计源。\n",
}


def _reference_files(reference_root: Path) -> dict[str, bytes]:
    kb_root = reference_root / "KB"
    if not kb_root.is_dir() or kb_root.is_symlink():
        raise ApplicationError("verified reference export has no KB directory")
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
    """Combine Task 2's verified ``KB/`` tree with application-managed files."""
    del snapshot  # The snapshot's authority is established by ``export_reference``.
    files = _reference_files(reference_root)
    files.update({path: text.encode("utf-8") for path, text in _TEMPLATES.items()})
    files.update({path: _yaml_bytes(view) for path, view in _VIEWS.items()})
    files.update({path: text.encode("utf-8") for path, text in _RULES.items()})
    return dict(sorted(files.items()))
