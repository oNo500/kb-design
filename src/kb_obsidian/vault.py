"""Safely initialize a new, ownership-separated Obsidian vault."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from collections.abc import Mapping
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from . import __version__
from .design_source import DesignSnapshot, load_design
from .errors import ApplicationError
from .managed import build_managed_files
from .reference_export import export_reference
from .render import render_frontmatter


_USER_DIRECTORIES = (
    "Inbox",
    "Sources/Clippings",
    "Sources/References",
    "Sources/Files",
    "Content",
    "Indexes",
    "Attachments",
    "App/Reports",
)
_MANAGED_PREFIXES = {
    "KB/": "reference",
    "App/Templates/": "template",
    "App/Views/": "view",
    "App/Rules/": "rule",
}
_CORE_PLUGINS = {
    "file-explorer": True,
    "global-search": True,
    "switcher": True,
    "graph": True,
    "backlink": True,
    "page-preview": True,
    "templates": True,
    "command-palette": True,
    "outline": True,
    "file-recovery": True,
    "canvas": True,
    "properties": True,
    "bookmarks": True,
    "bases": True,
}
_APP_CONFIG = {"attachmentFolderPath": "Attachments", "alwaysUpdateLinks": True}
_TEMPLATES_CONFIG = {"folder": "App/Templates"}
_TYPES_CONFIG = {
    "types": {
        "aliases": "aliases",
        "tags": "tags",
        "created": "date",
        "updated": "date",
        "kb_id": "text",
        "title": "text",
        "status": "text",
        "type": "text",
        "genre": "text",
        "form": "text",
        "level": "text",
        "language": "text",
        "subjects": "multitext",
        "entities": "multitext",
        "references": "multitext",
        "relations": "multitext",
    }
}


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _destination(target: Path, design_root: Path) -> Path:
    candidate = Path(target).expanduser()
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    if candidate.is_symlink():
        raise ApplicationError(f"vault target is a symbolic link: {candidate}")
    if candidate.name in {"", ".", ".."}:
        raise ApplicationError(f"protected vault target: {candidate}")
    try:
        parent = candidate.parent.resolve(strict=True)
    except OSError as exc:
        raise ApplicationError(f"vault target parent does not exist: {candidate.parent}") from exc
    if not parent.is_dir():
        raise ApplicationError(f"vault target parent is not a directory: {parent}")
    destination = parent / candidate.name
    try:
        resolved_design_root = Path(design_root).resolve(strict=True)
    except OSError as exc:
        raise ApplicationError(f"cannot resolve design root: {design_root}") from exc
    protected = {
        Path("/").resolve(),
        Path.home().resolve(),
        Path(__file__).resolve().parents[2],
        resolved_design_root,
    }
    if destination in protected:
        raise ApplicationError(f"protected vault target: {destination}")
    return destination


def _require_empty_target(destination: Path) -> None:
    if destination.is_symlink():
        raise ApplicationError(f"vault target is a symbolic link: {destination}")
    try:
        if not destination.exists():
            return
        if not destination.is_dir():
            raise ApplicationError(f"vault target is not a directory: {destination}")
        if next(destination.iterdir(), None) is not None:
            raise ApplicationError(f"vault target is not empty: {destination}")
    except OSError as exc:
        raise ApplicationError(f"cannot inspect vault target {destination}: {exc}") from exc


def _kind(relative_path: str) -> str:
    for prefix, kind in _MANAGED_PREFIXES.items():
        if relative_path.startswith(prefix):
            return kind
    raise ApplicationError(f"unknown managed file path: {relative_path}")


def _manifest(snapshot: DesignSnapshot, managed_files: Mapping[str, bytes]) -> dict[str, object]:
    return {
        "schema": "kb-obsidian-vault",
        "schema_version": 1,
        "app_version": __version__,
        "design_commit": snapshot.commit,
        "inputs": [
            {"path": path, "sha256": digest}
            for path, digest in sorted(snapshot.input_hashes.items())
        ],
        "files": [
            {"path": path, "kind": _kind(path), "sha256": _sha256(content)}
            for path, content in sorted(managed_files.items())
        ],
    }


def _write_files(root: Path, files: Mapping[str, bytes]) -> None:
    for relative_path, content in files.items():
        relative = PurePosixPath(relative_path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ApplicationError(f"unsafe generated file path: {relative_path}")
        path = root.joinpath(*relative.parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def _home_bytes() -> bytes:
    return (
        render_frontmatter({"aliases": ["主页"], "tags": ["home"]})
        + "# 主页\n\n"
        + "## 资料与内容\n\n"
        + "- Inbox：`Inbox/`\n"
        + "- 外部资料：`Sources/`\n"
        + "- [[App/Views/content.base|全部内容与最近修改]]\n"
        + "- [[App/Views/drafts.base|草稿内容]]\n"
        + "- 人工索引：`Indexes/`\n\n"
        + "## 受管理入口\n\n"
        + "- [[KB/README|正式主题、实体和来源用途]]\n"
        + "- [[App/Views/formal-topics.base|正式主题视图]]\n"
        + "- [[App/Views/unassigned-topics.base|未分配主题视图]]\n"
        + "- 维护报告：`App/Reports/`\n"
        + "- [[App/Rules/README|应用规则]]\n"
    ).encode("utf-8")


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ApplicationError(f"cannot read generated JSON {path}: {exc}") from exc


def _read_frontmatter(path: Path) -> Mapping[str, object]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ApplicationError(f"cannot read generated Markdown {path}: {exc}") from exc
    if not text.startswith("---\n"):
        raise ApplicationError(f"generated Markdown has no frontmatter: {path}")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ApplicationError(f"generated Markdown has invalid frontmatter: {path}")
    try:
        properties = yaml.safe_load(text[4:end])
    except (ValueError, yaml.YAMLError) as exc:
        raise ApplicationError(f"cannot parse generated frontmatter {path}: {exc}") from exc
    if not isinstance(properties, Mapping):
        raise ApplicationError(f"generated frontmatter is not a mapping: {path}")
    return properties


def _managed_files_on_disk(root: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for prefix in _MANAGED_PREFIXES:
        directory = root / prefix.rstrip("/")
        if not directory.is_dir() or directory.is_symlink():
            raise ApplicationError(f"managed directory is missing: {prefix}")
        for path in directory.rglob("*"):
            if path.is_symlink():
                raise ApplicationError(f"generated vault contains a symbolic link: {path}")
            if path.is_file():
                files[path.relative_to(root).as_posix()] = path.read_bytes()
    return files


def _verify_staged_vault(root: Path, snapshot: DesignSnapshot, expected_manifest: Mapping[str, object]) -> None:
    for relative_path in _USER_DIRECTORIES:
        if not (root / relative_path).is_dir():
            raise ApplicationError(f"user directory is missing: {relative_path}")
    home = root / "Home.md"
    required_home_links = {
        "[[App/Views/content.base|全部内容与最近修改]]",
        "[[App/Views/drafts.base|草稿内容]]",
        "[[KB/README|正式主题、实体和来源用途]]",
        "[[App/Views/formal-topics.base|正式主题视图]]",
        "[[App/Views/unassigned-topics.base|未分配主题视图]]",
        "[[App/Rules/README|应用规则]]",
    }
    if not home.is_file():
        raise ApplicationError("Home is missing a required entry link")
    home_text = home.read_text(encoding="utf-8")
    if any(link not in home_text for link in required_home_links):
        raise ApplicationError("Home is missing a required entry link")
    _read_frontmatter(home)
    for template in (root / "App" / "Templates").glob("*.md"):
        _read_frontmatter(template)
    for view in (root / "App" / "Views").glob("*.base"):
        try:
            if not isinstance(yaml.safe_load(view.read_text(encoding="utf-8")), Mapping):
                raise ApplicationError(f"generated Base is not a mapping: {view}")
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            raise ApplicationError(f"cannot parse generated Base {view}: {exc}") from exc
    if _read_json(root / ".obsidian" / "app.json") != _APP_CONFIG:
        raise ApplicationError("generated app configuration differs from the required configuration")
    if _read_json(root / ".obsidian" / "templates.json") != _TEMPLATES_CONFIG:
        raise ApplicationError("generated template configuration differs from the required configuration")
    if _read_json(root / ".obsidian" / "types.json") != _TYPES_CONFIG:
        raise ApplicationError("generated property configuration differs from the required configuration")
    if _read_json(root / ".obsidian" / "core-plugins.json") != _CORE_PLUGINS:
        raise ApplicationError("generated core plugin configuration differs from the required configuration")

    actual_manifest = _read_json(root / "App" / "manifest.json")
    if actual_manifest != expected_manifest:
        raise ApplicationError("generated manifest differs from its expected contents")
    if not isinstance(actual_manifest, Mapping) or not isinstance(actual_manifest.get("files"), list):
        raise ApplicationError("generated manifest has no file list")
    actual_files = _managed_files_on_disk(root)
    entries = actual_manifest["files"]
    paths = [entry.get("path") for entry in entries if isinstance(entry, Mapping)]
    if len(paths) != len(entries) or set(paths) != set(actual_files):
        raise ApplicationError("generated manifest file set mismatch")
    for entry in entries:
        if not isinstance(entry, Mapping) or set(entry) != {"path", "kind", "sha256"}:
            raise ApplicationError("generated manifest has an invalid file entry")
        path = entry["path"]
        if not isinstance(path, str) or entry["kind"] != _kind(path) or entry["sha256"] != _sha256(actual_files[path]):
            raise ApplicationError(f"generated manifest file hash mismatch: {path}")


def _write_configuration(root: Path) -> None:
    configuration = {
        ".obsidian/app.json": _json_bytes(_APP_CONFIG),
        ".obsidian/templates.json": _json_bytes(_TEMPLATES_CONFIG),
        ".obsidian/types.json": _json_bytes(_TYPES_CONFIG),
        ".obsidian/core-plugins.json": _json_bytes(_CORE_PLUGINS),
    }
    _write_files(root, configuration)


def initialize_vault(design_root: Path, target: Path) -> Mapping[str, object]:
    """Initialize ``target`` atomically from the frozen design snapshot."""
    destination = _destination(target, design_root)
    _require_empty_target(destination)
    snapshot = load_design(Path(design_root))
    try:
        temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}.tmp-", dir=destination.parent))
    except OSError as exc:
        raise ApplicationError(f"cannot create vault staging directory: {exc}") from exc
    try:
        staged_vault = temporary / "vault"
        staged_vault.mkdir()
        reference_root = temporary / "reference"
        export_reference(snapshot, reference_root)
        managed_files = build_managed_files(snapshot, reference_root)
        _write_files(staged_vault, managed_files)
        for relative_path in _USER_DIRECTORIES:
            (staged_vault / relative_path).mkdir(parents=True, exist_ok=True)
        (staged_vault / "Home.md").write_bytes(_home_bytes())
        _write_configuration(staged_vault)
        manifest = _manifest(snapshot, managed_files)
        _write_files(staged_vault, {"App/manifest.json": _json_bytes(manifest)})
        _verify_staged_vault(staged_vault, snapshot, manifest)
        _require_empty_target(destination)
        try:
            os.replace(staged_vault, destination)
        except OSError as exc:
            raise ApplicationError(f"cannot publish initialized vault: {exc}") from exc
    except OSError as exc:
        raise ApplicationError(f"cannot initialize vault: {exc}") from exc
    finally:
        shutil.rmtree(temporary, ignore_errors=True)
    return {
        "app_version": __version__,
        "design_commit": snapshot.commit,
        "input_hashes": dict(snapshot.input_hashes),
        "managed_files": [entry["path"] for entry in manifest["files"]],
    }
