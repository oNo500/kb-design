"""Safely initialize a new, ownership-separated Obsidian vault."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from kb_core.repository import project_root

from . import __version__
from .design_source import DesignSnapshot, load_design
from .errors import ApplicationError
from .managed import build_managed_files
from .reference_export import export_reference
from .render import render_frontmatter


_USER_DIRECTORIES = (
    "inbox",
    "sources/clippings",
    "sources/references",
    "sources/files",
    "content",
    "indexes",
    "attachments",
    "app/reports",
)
_MANAGED_PREFIXES = {
    "kb/": "reference",
    "app/templates/": "template",
    "app/views/": "view",
    "app/rules/": "rule",
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
_APP_CONFIG = {"attachmentFolderPath": "attachments", "alwaysUpdateLinks": True}
_TEMPLATES_CONFIG = {"folder": "app/templates"}
_TYPES_CONFIG = {
    "types": {
        "aliases": "aliases",
        "tags": "tags",
        "kb_id": "text",
        "title": "text",
        "kb_type": "text",
        "kb_genre": "text",
        "kb_form": "text",
        "kb_level": "text",
        "kb_source": "text",
        "kb_status": "text",
        "kb_is_replaced_by": "text",
        "kb_language": "text",
        "kb_object": "text",
        "kb_label": "text",
        "kb_version": "text",
        "kb_replaced_by": "text",
        "kb_superordinate": "text",
        "kb_kind": "text",
        "kb_vendor": "text",
        "kb_tier": "text",
        "kb_entity_version": "text",
        "kb_url": "text",
        "kb_watch": "text",
        "kb_entity": "text",
        "kb_subjects": "multitext",
        "kb_entities": "multitext",
        "kb_references": "multitext",
        "kb_relation": "multitext",
        "kb_creator": "multitext",
        "kb_broader": "multitext",
        "kb_related": "multitext",
        "kb_arrays": "multitext",
        "kb_members": "multitext",
        "kb_roles": "multitext",
        "kb_created": "date",
        "kb_modified": "date",
        "kb_added": "date",
        "kb_checked": "date",
    }
}
_WIKILINK = re.compile(r"\[\[([^|#\]]+)(?:#[^|\]]+)?(?:\|[^\]]+)?\]\]")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_MANIFEST_KEYS = {"schema", "schema_version", "app_version", "design_commit", "inputs", "files"}
_FORMAL_TARGETS = (
    ("topics", "concepts", "kb/topics"),
    ("topics", "arrays", "kb/arrays"),
    ("entities", "entities", "kb/entities"),
    ("sources", "sources", "kb/sources"),
    ("types", "types", "kb/types"),
    ("genres", "genres", "kb/genres"),
    ("forms", "forms", "kb/forms"),
)


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _is_within(path: Path, directory: Path) -> bool:
    return path == directory or directory in path.parents


def _require_safe_repository_location(path: Path, design_root: Path) -> None:
    application_root = Path(__file__).resolve().parents[2]
    if _is_within(path, application_root):
        raise ApplicationError(f"protected vault target: {path}")
    repositories = {design_root}
    try:
        repositories.add(project_root(Path(__file__)))
    except (OSError, ValueError):
        pass
    for repository_root in repositories:
        output_root = repository_root / "output"
        if _is_within(path, repository_root) and not (
            path != output_root and _is_within(path, output_root)
        ):
            raise ApplicationError(f"protected vault target: {path}")


def _destination(target: Path, design_root: Path) -> Path:
    candidate = Path(target).expanduser()
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    if candidate.is_symlink():
        raise ApplicationError(f"vault target is a symbolic link: {candidate}")
    if candidate.name in {"", ".", ".."}:
        raise ApplicationError(f"protected vault target: {candidate}")
    try:
        resolved_design_root = Path(design_root).resolve(strict=True)
    except OSError as exc:
        raise ApplicationError(f"cannot resolve design root: {design_root}") from exc
    try:
        candidate = candidate.resolve(strict=False)
    except OSError as exc:
        raise ApplicationError(f"cannot resolve vault target: {target}") from exc
    _require_safe_repository_location(candidate, resolved_design_root)
    default_parent = resolved_design_root / "output"
    if candidate.parent == default_parent and not default_parent.exists():
        try:
            default_parent.mkdir()
        except OSError as exc:
            raise ApplicationError(f"cannot create vault output directory: {default_parent}") from exc
    try:
        parent = candidate.parent.resolve(strict=True)
    except OSError as exc:
        raise ApplicationError(f"vault target parent does not exist: {candidate.parent}") from exc
    if not parent.is_dir():
        raise ApplicationError(f"vault target parent is not a directory: {parent}")
    destination = parent / candidate.name
    protected = {
        Path("/").resolve(),
        Path.home().resolve(),
        resolved_design_root,
    }
    if destination in protected:
        raise ApplicationError(f"protected vault target: {destination}")
    _require_safe_repository_location(destination, resolved_design_root)
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


def _vault_root(snapshot: DesignSnapshot, vault: Path) -> Path:
    candidate = Path(vault).expanduser()
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    if candidate.is_symlink():
        raise ApplicationError(f"vault is a symbolic link: {candidate}")
    try:
        root = candidate.resolve(strict=True)
    except OSError as exc:
        raise ApplicationError(f"vault does not exist: {candidate}") from exc
    if not root.is_dir():
        raise ApplicationError(f"vault is not a directory: {root}")
    try:
        design_root = Path(snapshot.root).resolve(strict=True)
    except OSError as exc:
        raise ApplicationError(f"cannot resolve design root: {snapshot.root}") from exc
    protected = {
        Path("/").resolve(),
        Path.home().resolve(),
        design_root,
    }
    if root in protected:
        raise ApplicationError(f"protected vault root: {root}")
    _require_safe_repository_location(root, design_root)
    return root


def _relative_path(value: object, *, context: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ApplicationError(f"unsafe path in {context}: {value!r}")
    relative = PurePosixPath(value)
    if (
        relative.is_absolute()
        or "." in relative.parts
        or ".." in relative.parts
        or relative.as_posix() != value
    ):
        raise ApplicationError(f"unsafe path in {context}: {value!r}")
    return value


def _manifest_inputs(manifest_path: Path, value: object) -> dict[str, str]:
    if not isinstance(value, list):
        raise ApplicationError(f"vault manifest inputs must be a list: {manifest_path}")
    inputs: dict[str, str] = {}
    for index, entry in enumerate(value):
        context = f"{manifest_path} inputs[{index}]"
        if not isinstance(entry, Mapping) or set(entry) != {"path", "sha256"}:
            raise ApplicationError(f"vault manifest has an invalid input entry: {context}")
        path = _relative_path(entry["path"], context=context)
        digest = entry["sha256"]
        if not isinstance(digest, str) or _SHA256.fullmatch(digest) is None:
            raise ApplicationError(f"vault manifest has an invalid input hash: {path} in {manifest_path}")
        if path in inputs:
            raise ApplicationError(f"vault manifest has a duplicate input path: {path} in {manifest_path}")
        inputs[path] = digest
    return inputs


def _manifest_files(manifest_path: Path, value: object) -> dict[str, Mapping[str, object]]:
    if not isinstance(value, list):
        raise ApplicationError(f"vault manifest files must be a list: {manifest_path}")
    files: dict[str, Mapping[str, object]] = {}
    for index, entry in enumerate(value):
        context = f"{manifest_path} files[{index}]"
        if not isinstance(entry, Mapping) or set(entry) != {"path", "kind", "sha256"}:
            raise ApplicationError(f"vault manifest has an invalid file entry: {context}")
        path = _relative_path(entry["path"], context=context)
        try:
            expected_kind = _kind(path)
        except ApplicationError as exc:
            raise ApplicationError(f"vault manifest has an invalid managed path: {path} in {manifest_path}") from exc
        if entry["kind"] != expected_kind:
            raise ApplicationError(f"vault manifest has an invalid kind for {path}: {manifest_path}")
        digest = entry["sha256"]
        if not isinstance(digest, str) or _SHA256.fullmatch(digest) is None:
            raise ApplicationError(f"vault manifest has an invalid file hash for {path}: {manifest_path}")
        if path in files:
            raise ApplicationError(f"vault manifest has a duplicate file path: {path} in {manifest_path}")
        files[path] = entry
    return files


def _required_kb_targets(snapshot: DesignSnapshot) -> set[str]:
    targets: set[str] = set()
    for document_name, collection_name, directory in _FORMAL_TARGETS:
        document = snapshot.documents.get(document_name)
        if not isinstance(document, Mapping):
            raise ApplicationError(f"design document {document_name} must be a mapping")
        records = document.get(collection_name)
        if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
            raise ApplicationError(f"design collection {document_name}.{collection_name} must be a list")
        for record in records:
            if not isinstance(record, Mapping) or not isinstance(record.get("id"), str):
                raise ApplicationError(
                    f"design collection {document_name}.{collection_name} has an invalid record"
                )
            target = f"{directory}/{record['id']}.md"
            _relative_path(target, context=f"design collection {document_name}.{collection_name}")
            targets.add(target)
    return targets


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
        + "- [[app/views/inbox.base|Inbox]]\n"
        + "- [[app/views/sources.base|外部资料]]\n"
        + "- [[app/views/content.base|全部内容]]\n"
        + "- [[app/views/drafts.base|草稿内容]]\n"
        + "- [[app/views/recently-modified.base|最近修改]]\n"
        + "- [[app/views/indexes.base|人工索引]]\n\n"
        + "## 受管理入口\n\n"
        + "- [[kb/views/topics.base|正式主题]]\n"
        + "- [[kb/views/entities.base|实体]]\n"
        + "- [[kb/views/sources.base|来源用途]]\n"
        + "- [[app/reports/index|维护报告]]\n"
        + "- [[app/rules/index|应用规则]]\n"
    ).encode("utf-8")


def _reports_index_bytes() -> bytes:
    return "# 维护报告\n\n此目录保存从内容读取后生成的派生诊断结果。\n".encode("utf-8")


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
            raise ApplicationError(f"managed directory is missing or unsafe: {directory}")
        try:
            candidates = list(directory.rglob("*"))
        except OSError as exc:
            raise ApplicationError(f"cannot inspect managed directory {directory}: {exc}") from exc
        for path in candidates:
            if path.is_symlink():
                raise ApplicationError(f"vault contains a symbolic link: {path}")
            if path.is_file():
                relative_path = path.relative_to(root).as_posix()
                try:
                    files[relative_path] = path.read_bytes()
                except OSError as exc:
                    raise ApplicationError(f"cannot read managed file {path}: {exc}") from exc
    return files


def verify_vault(snapshot: DesignSnapshot, vault: Path) -> Path:
    """Verify that an initialized vault is bound to ``snapshot`` without changing bytes."""
    root = _vault_root(snapshot, vault)
    app_root = root / "app"
    if app_root.is_symlink():
        raise ApplicationError(f"vault managed directory is unsafe: {app_root}")
    content_root = root / "content"
    if content_root.is_symlink() or not content_root.is_dir():
        raise ApplicationError(f"vault content directory is missing or unsafe: {content_root}")

    manifest_path = root / "app" / "manifest.json"
    if manifest_path.is_symlink():
        raise ApplicationError(f"vault manifest is a symbolic link: {manifest_path}")
    manifest = _read_json(manifest_path)
    if not isinstance(manifest, Mapping) or set(manifest) != _MANIFEST_KEYS:
        raise ApplicationError(f"vault manifest has an invalid schema: {manifest_path}")
    if manifest["schema"] != "kb-obsidian-vault":
        raise ApplicationError(f"vault manifest schema mismatch: {manifest_path}")
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise ApplicationError(f"vault manifest schema_version mismatch: {manifest_path}")
    if manifest["app_version"] != __version__:
        raise ApplicationError(f"vault manifest app_version mismatch: {manifest_path}")
    if manifest["design_commit"] != snapshot.commit:
        raise ApplicationError(f"vault manifest design_commit mismatch: {manifest_path}")

    inputs = _manifest_inputs(manifest_path, manifest["inputs"])
    expected_inputs = dict(snapshot.input_hashes)
    if inputs != expected_inputs:
        differing = sorted(set(inputs) ^ set(expected_inputs))
        if not differing:
            differing = sorted(path for path in inputs if inputs[path] != expected_inputs[path])
        detail = differing[0] if differing else "inputs"
        raise ApplicationError(f"vault manifest input mismatch: {detail} in {manifest_path}")

    entries = _manifest_files(manifest_path, manifest["files"])
    actual_files = _managed_files_on_disk(root)
    missing = sorted(set(entries) - set(actual_files))
    if missing:
        raise ApplicationError(f"managed file listed by manifest is missing: {missing[0]}")
    unlisted = sorted(set(actual_files) - set(entries))
    if unlisted:
        raise ApplicationError(f"managed file is not listed by manifest: {unlisted[0]}")
    for path in sorted(entries):
        actual_hash = _sha256(actual_files[path])
        expected_hash = entries[path]["sha256"]
        if actual_hash != expected_hash:
            raise ApplicationError(
                f"managed file hash mismatch: {path}; expected {expected_hash}, actual {actual_hash}"
            )

    required_targets = _required_kb_targets(snapshot)
    for path in sorted(required_targets):
        entry = entries.get(path)
        target = root.joinpath(*PurePosixPath(path).parts)
        if entry is None or entry["kind"] != "reference" or target.is_symlink() or not target.is_file():
            raise ApplicationError(f"required controlled target is missing or unlisted: {path}")
    return root


def _filter_expressions(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if not isinstance(value, Mapping) or len(value) != 1:
        raise ApplicationError("generated Base has an invalid filter shape")
    operator, children = next(iter(value.items()))
    if operator not in {"and", "or", "not"} or not isinstance(children, list):
        raise ApplicationError("generated Base has an invalid filter group")
    return [expression for child in children for expression in _filter_expressions(child)]


def _verify_home_links(root: Path, home_text: str) -> None:
    targets = _WIKILINK.findall(home_text)
    if not targets:
        raise ApplicationError("Home has no internal entry links")
    for target in targets:
        path = PurePosixPath(target)
        if path.is_absolute() or ".." in path.parts:
            raise ApplicationError(f"Home has an unsafe internal link: {target}")
        destination = root.joinpath(*path.parts)
        if not path.suffix:
            destination = destination.with_suffix(".md")
        if not destination.is_file() or destination.is_symlink():
            raise ApplicationError(f"Home link target is missing: {target}")


def _verify_staged_vault(root: Path, snapshot: DesignSnapshot, expected_manifest: Mapping[str, object]) -> None:
    for relative_path in _USER_DIRECTORIES:
        if not (root / relative_path).is_dir():
            raise ApplicationError(f"user directory is missing: {relative_path}")
    home = root / "home.md"
    if not home.is_file():
        raise ApplicationError("Home is missing a required entry link")
    home_text = home.read_text(encoding="utf-8")
    _verify_home_links(root, home_text)
    _read_frontmatter(home)
    for template in (root / "app" / "templates").glob("*.md"):
        _read_frontmatter(template)
    for view in (root / "app" / "views").glob("*.base"):
        try:
            document = yaml.safe_load(view.read_text(encoding="utf-8"))
            if not isinstance(document, Mapping):
                raise ApplicationError(f"generated Base is not a mapping: {view}")
            expressions = _filter_expressions(document.get("filters"))
            if not any(expression.startswith('file.inFolder("') for expression in expressions):
                raise ApplicationError(f"generated Base has no folder filter: {view}")
            if 'file.ext == "md"' not in expressions:
                raise ApplicationError(f"generated Base has no Markdown filter: {view}")
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

    actual_manifest = _read_json(root / "app" / "manifest.json")
    if actual_manifest != expected_manifest:
        raise ApplicationError("generated manifest differs from its expected contents")
    verify_vault(snapshot, root)


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
        (staged_vault / "home.md").write_bytes(_home_bytes())
        (staged_vault / "app" / "reports" / "index.md").write_bytes(_reports_index_bytes())
        _write_configuration(staged_vault)
        manifest = _manifest(snapshot, managed_files)
        _write_files(staged_vault, {"app/manifest.json": _json_bytes(manifest)})
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
