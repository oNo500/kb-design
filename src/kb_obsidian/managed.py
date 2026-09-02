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

_VIEWS = {
    "App/Views/content.base": {
        "views": [{"type": "table", "name": "内容", "filters": [{"file.folder": "Content"}]}]
    },
    "App/Views/drafts.base": {
        "views": [{"type": "table", "name": "草案", "filters": [{"status": "draft"}]}]
    },
    "App/Views/formal-topics.base": {
        "views": [{"type": "table", "name": "正式主题", "filters": [{"file.folder": "KB/Topics"}]}]
    },
    "App/Views/unassigned-topics.base": {
        "views": [{"type": "table", "name": "未分配主题", "filters": [{"subjects": ""}]}]
    },
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
