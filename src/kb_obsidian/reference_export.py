"""Adapt the frozen kb-design Obsidian exporter without changing its output."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Mapping
from pathlib import Path, PurePosixPath
from typing import Any

from .design_source import DesignSnapshot, SUPPORTED_DESIGN_COMMITS, _git, _resolve_git_root
from .errors import ApplicationError


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_DIRECTORY_KINDS = {
    "topics": "topic", "arrays": "array", "entities": "entity", "sources": "source",
    "types": "type", "genres": "genre", "forms": "form",
}


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _output_destination(output: Path) -> Path:
    candidate = Path(output).expanduser()
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    if candidate.name in {"", ".", ".."}:
        raise ApplicationError(f"unsafe output directory: {output}")
    try:
        parent = candidate.parent.resolve(strict=True)
    except OSError as exc:
        raise ApplicationError(f"output parent does not exist: {candidate.parent}") from exc
    if not parent.is_dir():
        raise ApplicationError(f"output parent is not a directory: {parent}")
    return parent / candidate.name


def _require_publishable_output(destination: Path) -> None:
    if destination.is_symlink():
        raise ApplicationError(f"output directory is a symbolic link: {destination}")
    try:
        if not destination.exists():
            return
        if not destination.is_dir():
            raise ApplicationError(f"output path is not a directory: {destination}")
        if next(destination.iterdir(), None) is not None:
            raise ApplicationError(f"output directory is not empty: {destination}")
    except OSError as exc:
        raise ApplicationError(f"cannot inspect output directory: {destination}: {exc}") from exc


def _verify_snapshot_source(snapshot: DesignSnapshot) -> tuple[Path, str]:
    root = _resolve_git_root(snapshot.root)
    if root != snapshot.root or snapshot.commit not in SUPPORTED_DESIGN_COMMITS:
        raise ApplicationError("design source changed since snapshot")
    if _git(root, "rev-parse", "HEAD") != snapshot.commit:
        raise ApplicationError("design source changed since snapshot")
    if _git(root, "status", "--porcelain", "--untracked-files=no"):
        raise ApplicationError("design source changed since snapshot")
    exporter = root / "scripts" / "export_obsidian.py"
    try:
        exporter_bytes = exporter.read_bytes()
    except OSError as exc:
        raise ApplicationError(f"cannot read reference exporter: {exc}") from exc
    return exporter, _sha256(exporter_bytes)


def _read_manifest(output: Path) -> dict[str, Any]:
    try:
        manifest_bytes = (output / "manifest.json").read_bytes()
        manifest = json.loads(manifest_bytes)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ApplicationError(f"cannot read reference export manifest: {exc}") from exc
    if not isinstance(manifest, dict):
        raise ApplicationError("reference export manifest is not a mapping")
    return manifest


def _require_digest(value: object, description: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise ApplicationError(f"invalid {description}")
    return value


def _manifest_identity(relative_path: str) -> tuple[str, str]:
    path = PurePosixPath(relative_path)
    if (
        not relative_path
        or path.is_absolute()
        or relative_path != path.as_posix()
        or ".." in path.parts
    ):
        raise ApplicationError(f"unsafe manifest file path: {relative_path}")
    if relative_path == "index.md":
        return "index", path.stem
    if path.suffix == ".base" and path.parts[:2] == ("kb", "views") and len(path.parts) == 3:
        return "base", path.stem
    if len(path.parts) == 3 and path.parts[0] == "kb" and path.suffix == ".md":
        kind = _DIRECTORY_KINDS.get(path.parts[1])
        if kind is not None and _IDENTIFIER.fullmatch(path.stem):
            return kind, path.stem
    raise ApplicationError(f"unknown manifest file path: {relative_path}")


def _read_export_files(output: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    try:
        paths = list(output.rglob("*"))
    except OSError as exc:
        raise ApplicationError(f"cannot inspect reference export: {exc}") from exc
    for path in paths:
        if path.is_symlink():
            raise ApplicationError(f"reference export contains a symbolic link: {path}")
        if not path.is_file():
            continue
        relative_path = path.relative_to(output).as_posix()
        if relative_path == "manifest.json":
            continue
        try:
            files[relative_path] = path.read_bytes()
        except OSError as exc:
            raise ApplicationError(f"cannot read reference export file {relative_path}: {exc}") from exc
    return files


def _verify_input_hashes(manifest: Mapping[str, object], snapshot: DesignSnapshot) -> None:
    inputs = manifest.get("inputs")
    if not isinstance(inputs, list):
        raise ApplicationError("reference export manifest has no input hashes")
    actual_hashes: dict[str, str] = {}
    for entry in inputs:
        if not isinstance(entry, Mapping) or set(entry) != {"path", "sha256", "version"}:
            raise ApplicationError("reference export manifest has an invalid input hash")
        relative_path = entry.get("path")
        digest = entry.get("sha256")
        version = entry.get("version")
        if not isinstance(relative_path, str) or not isinstance(version, str) or not version:
            raise ApplicationError("reference export manifest has an invalid input hash")
        if relative_path in actual_hashes:
            raise ApplicationError("reference export manifest has duplicate input hashes")
        actual_hashes[relative_path] = _require_digest(digest, "manifest input hash")
    if actual_hashes != dict(snapshot.input_hashes):
        raise ApplicationError("reference export input hash mismatch")


def _verify_manifest(
    manifest: Mapping[str, object],
    output: Path,
    snapshot: DesignSnapshot,
    exporter_hash: str,
) -> None:
    if manifest.get("schema") != "kb-design-obsidian-export" or manifest.get("schema_version") != 1:
        raise ApplicationError("unsupported manifest schema")
    _verify_input_hashes(manifest, snapshot)
    if _require_digest(manifest.get("exporter_sha256"), "manifest exporter hash") != exporter_hash:
        raise ApplicationError("manifest exporter hash mismatch")

    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise ApplicationError("reference export manifest has no files")
    actual_files = _read_export_files(output)
    manifest_entries: dict[str, Mapping[str, object]] = {}
    expected_counts = {kind: 0 for kind in _DIRECTORY_KINDS.values()}
    for entry in entries:
        if not isinstance(entry, Mapping) or set(entry) != {"id", "object", "path", "sha256"}:
            raise ApplicationError("reference export manifest has an invalid file entry")
        relative_path = entry.get("path")
        object_kind = entry.get("object")
        object_id = entry.get("id")
        if not isinstance(relative_path, str) or not isinstance(object_kind, str) or not isinstance(object_id, str):
            raise ApplicationError("reference export manifest has an invalid file entry")
        expected_kind, expected_id = _manifest_identity(relative_path)
        if object_kind != expected_kind or object_id != expected_id:
            raise ApplicationError(f"manifest file identity mismatch: {relative_path}")
        if relative_path in manifest_entries:
            raise ApplicationError(f"reference export manifest has duplicate file: {relative_path}")
        manifest_entries[relative_path] = entry
        if object_kind in expected_counts:
            expected_counts[object_kind] += 1

    if set(manifest_entries) != set(actual_files):
        raise ApplicationError("reference export manifest file coverage mismatch")
    for relative_path, content in actual_files.items():
        expected_digest = _require_digest(
            manifest_entries[relative_path].get("sha256"),
            "manifest file hash",
        )
        if expected_digest != _sha256(content):
            raise ApplicationError(f"manifest file hash mismatch: {relative_path}")

    for key in ("content_files", "total_files"):
        if type(manifest.get(key)) is not int or manifest[key] < 0:
            raise ApplicationError(f"invalid manifest {key}")
    if manifest["content_files"] != len(actual_files) or manifest["total_files"] != len(actual_files) + 1:
        raise ApplicationError("reference export manifest file counts mismatch")
    digest_input = b"".join(
        f"{path}\0{_sha256(actual_files[path])}\n".encode("utf-8")
        for path in sorted(actual_files)
    )
    if _require_digest(manifest.get("content_sha256"), "manifest content hash") != _sha256(digest_input):
        raise ApplicationError("manifest content hash mismatch")
    object_counts = manifest.get("object_counts")
    if not isinstance(object_counts, Mapping) or dict(object_counts) != expected_counts:
        raise ApplicationError("manifest object counts mismatch")


def _run_exporter(exporter: Path, root: Path, output: Path) -> None:
    try:
        completed = subprocess.run(
            [
                sys.executable,
                str(exporter),
                "--repo-root",
                str(root),
                "--output",
                str(output),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise ApplicationError(f"cannot run reference exporter: {exc}") from exc
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise ApplicationError(f"reference export failed: {detail}")


def export_reference(snapshot: DesignSnapshot, output: Path) -> Mapping[str, object]:
    """Run, verify, and atomically publish only the upstream ``kb/`` tree."""
    destination = _output_destination(output)
    _require_publishable_output(destination)
    exporter, exporter_hash = _verify_snapshot_source(snapshot)
    try:
        temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}.tmp-", dir=destination.parent))
    except OSError as exc:
        raise ApplicationError(f"cannot create reference export staging directory: {exc}") from exc
    try:
        upstream_output = temporary / "upstream"
        _run_exporter(exporter, snapshot.root, upstream_output)
        _, current_exporter_hash = _verify_snapshot_source(snapshot)
        if current_exporter_hash != exporter_hash:
            raise ApplicationError("design source changed since snapshot")

        manifest = _read_manifest(upstream_output)
        _verify_manifest(manifest, upstream_output, snapshot, exporter_hash)
        source_tree = upstream_output / "kb"
        if not source_tree.is_dir() or source_tree.is_symlink():
            raise ApplicationError("reference export does not contain a kb tree")
        published = temporary / "published"
        published.mkdir()
        try:
            shutil.copytree(source_tree, published / "kb")
        except OSError as exc:
            raise ApplicationError(f"cannot publish verified kb tree: {exc}") from exc

        _require_publishable_output(destination)
        try:
            os.replace(published, destination)
        except OSError as exc:
            raise ApplicationError(f"cannot publish verified kb tree: {exc}") from exc
    finally:
        shutil.rmtree(temporary, ignore_errors=True)

    result = dict(manifest)
    result["design_commit"] = snapshot.commit
    return result
