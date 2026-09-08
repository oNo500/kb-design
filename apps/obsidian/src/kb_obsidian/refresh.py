"""Refresh managed vocabulary references while preserving all other vault bytes."""

from __future__ import annotations

import ast
import io
import json
import sys
import tarfile
import os
import re
import shutil
import subprocess
import tempfile
from collections.abc import Mapping
from pathlib import Path, PurePosixPath
from typing import Optional

import yaml

from . import __version__
from .design_source import DesignSnapshot, load_design
from .errors import ApplicationError
from .managed import _reference_files, _VIEWS, _yaml_bytes
from .reference_export import export_reference
from .validation import _validate_content_tree
from .vault import (
    _MANIFEST_KEYS, _WIKILINK, _json_bytes, _managed_files_on_disk,
    _manifest, _manifest_files, _manifest_inputs, _sha256, _vault_root,
    _write_files, verify_vault,
)


def _git_bytes(root: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments], capture_output=True, check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ApplicationError(f"cannot verify old design provenance: {detail}")
    return result.stdout


def _old_snapshot(snapshot: DesignSnapshot, manifest_path: Path, raw: bytes) -> DesignSnapshot:
    try:
        manifest = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise ApplicationError(f"invalid vault manifest: {manifest_path}") from exc
    if not isinstance(manifest, Mapping) or set(manifest) != _MANIFEST_KEYS:
        raise ApplicationError(f"invalid vault manifest schema: {manifest_path}")
    if (
        manifest["schema"] != "kb-obsidian-vault"
        or type(manifest["schema_version"]) is not int
        or manifest["schema_version"] != 1
        or manifest["app_version"] != __version__
    ):
        raise ApplicationError(f"unsupported vault manifest schema or app version: {manifest_path}")
    commit = manifest["design_commit"]
    if not isinstance(commit, str) or re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise ApplicationError(f"invalid old design commit in {manifest_path}: {commit!r}")
    _git_bytes(snapshot.root, "merge-base", "--is-ancestor", commit, snapshot.commit)
    inputs = _manifest_inputs(manifest_path, manifest["inputs"])
    # The ancestor owns its input contract; never interpret it with today's reader.
    source = _git_bytes(snapshot.root, "show", f"{commit}:apps/obsidian/src/kb_obsidian/design_source.py")
    contract = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in {"_FORMAL_DOCUMENTS", "_OPTIONAL_TERM_DOCUMENTS", "_TERM_LAYOUT_DOCUMENT", "_TERM_SCHEMA_FILES"}:
                contract[node.targets[0].id] = ast.literal_eval(node.value)
    required = {"_FORMAL_DOCUMENTS", "_OPTIONAL_TERM_DOCUMENTS", "_TERM_LAYOUT_DOCUMENT", "_TERM_SCHEMA_FILES"}
    if set(contract) != required:
        raise ApplicationError("ancestor design input contract is unavailable")
    allowed_input_sets = [set(contract["_FORMAL_DOCUMENTS"].values())]
    allowed_input_sets.append(
        allowed_input_sets[0]
        | set(contract["_OPTIONAL_TERM_DOCUMENTS"].values())
        | set(contract["_TERM_LAYOUT_DOCUMENT"].values())
        | set(contract["_TERM_SCHEMA_FILES"])
    )
    if set(inputs) not in allowed_input_sets:
        raise ApplicationError(f"old design input set mismatch: {manifest_path}")
    documents = {}
    selected_documents = dict(contract["_FORMAL_DOCUMENTS"])
    if set(contract["_OPTIONAL_TERM_DOCUMENTS"].values()) <= set(inputs):
        selected_documents.update(contract["_OPTIONAL_TERM_DOCUMENTS"])
        selected_documents.update(contract["_TERM_LAYOUT_DOCUMENT"])
    for name, relative in selected_documents.items():
        data = _git_bytes(snapshot.root, "show", f"{commit}:{relative}")
        if _sha256(data) != inputs[relative]:
            raise ApplicationError(f"old design input hash mismatch: {relative} in {manifest_path}")
        try:
            documents[name] = yaml.safe_load(data)
        except yaml.YAMLError as exc:
            raise ApplicationError(f"invalid old design input: {relative}") from exc
    for relative in contract["_TERM_SCHEMA_FILES"]:
        if relative not in inputs:
            continue
        data = _git_bytes(snapshot.root, "show", f"{commit}:{relative}")
        if _sha256(data) != inputs[relative]:
            raise ApplicationError(f"old design input hash mismatch: {relative} in {manifest_path}")
    return DesignSnapshot(snapshot.root, commit, documents, inputs)


def _verify_old_vault(snapshot: DesignSnapshot, vault: Path) -> None:
    """Run the ancestor's vault contract in an isolated, disposable source tree."""
    archive = _git_bytes(snapshot.root, "archive", snapshot.commit, "apps/obsidian/src", "packages/kb-core/src")
    with tempfile.TemporaryDirectory(prefix="kb-obsidian-ancestor-") as directory:
        root = Path(directory)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            for member in bundle.getmembers():
                if not member.isfile() and not member.isdir():
                    raise ApplicationError("ancestor implementation contains unsupported filesystem entries")
                target = PurePosixPath(member.name)
                if target.is_absolute() or ".." in target.parts:
                    raise ApplicationError("ancestor implementation contains unsafe paths")
                destination = root.joinpath(*target.parts)
                if member.isdir():
                    destination.mkdir(parents=True, exist_ok=True)
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with bundle.extractfile(member) as stream:
                        destination.write_bytes(stream.read())
        script = """import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
sys.path[:0] = [str(root / 'apps/obsidian/src'), str(root / 'packages/kb-core/src')]
from kb_obsidian.design_source import DesignSnapshot
from kb_obsidian.vault import verify_vault
value = json.load(sys.stdin)
snapshot = DesignSnapshot(pathlib.Path(value['root']), value['commit'], value['documents'], value['inputs'])
verify_vault(snapshot, pathlib.Path(sys.argv[2]))
"""
        completed = subprocess.run([sys.executable, "-c", script, str(root), str(vault)],
            input=json.dumps({"root": str(snapshot.root), "commit": snapshot.commit,
                              "documents": snapshot.documents, "inputs": snapshot.input_hashes},
                             default=lambda value: value.isoformat()), capture_output=True, text=True)
        if completed.returncode:
            detail = completed.stderr.strip().splitlines()
            raise ApplicationError(f"ancestor vault verification failed: {detail[-1] if detail else 'unknown failure'}")


def _check_managed(
    root: Path, raw: bytes, actual: dict[str, bytes], references: Mapping[str, bytes],
) -> list[str]:
    path = root / "app/manifest.json"
    entries = _manifest_files(path, json.loads(raw)["files"])
    if set(entries) != set(actual):
        differing = sorted(set(entries) ^ set(actual))
        raise ApplicationError(f"managed file set mismatch: {differing[0]}")
    formats = []
    for relative, data in sorted(actual.items()):
        expected = entries[relative]["sha256"]
        if _sha256(data) == expected:
            continue
        view = _VIEWS.get(relative)
        equivalent = False
        baseline = _yaml_bytes(view) if view is not None else None
        if relative.startswith("kb/views/") and relative.endswith(".base"):
            baseline = references.get(relative)
        if baseline is not None and _sha256(baseline) == expected:
            try:
                equivalent = yaml.safe_load(data) == yaml.safe_load(baseline)
            except (ValueError, UnicodeError, yaml.YAMLError):
                pass
        if not equivalent:
            raise ApplicationError(f"managed file hash mismatch: {relative}")
        formats.append(relative)
    return formats


def _markdown_bytes(root: Path) -> dict[str, bytes]:
    """Read retained Markdown without following symbolic links outside the vault."""
    result = {}
    def walk_error(error):
        raise error
    for directory, children, names in os.walk(root, followlinks=False, onerror=walk_error):
        base = Path(directory)
        if base == root:
            children[:] = [name for name in children if name != "kb"]
        for name in names:
            path = base / name
            if path.suffix.lower() != ".md":
                continue
            if path.is_symlink():
                raise ApplicationError(f"cannot validate symbolic-link Markdown: {path}")
            result[path.relative_to(root).as_posix()] = path.read_bytes()
    return result


def _check_content(snapshot: DesignSnapshot, root: Path, references: Mapping[str, bytes], markdown: Mapping[str, bytes]) -> None:
    result = _validate_content_tree(snapshot, root / "content")
    if not result.is_valid:
        issue = result.issues[0]
        raise ApplicationError(f"content is incompatible with refreshed vocabulary: {issue.path}: {issue.message}")
    for path, data in markdown.items():
        try:
            text = data.decode("utf-8")
        except UnicodeError as exc:
            raise ApplicationError(f"cannot validate Markdown references: {path}") from exc
        for target in _WIKILINK.findall(text.replace("\\|", "|")):
            if not target.startswith("kb/"):
                continue
            relative = PurePosixPath(target)
            if relative.is_absolute() or ".." in relative.parts or "\\" in target:
                raise ApplicationError(f"unsafe vocabulary reference in {path}: {target}")
            if target not in references and target + ".md" not in references:
                raise ApplicationError(f"unresolved vocabulary reference in {path}: {target}")


def _publish(root: Path, stage: Path, backup: Path) -> None:
    """Restore both managed parts after an ordinary publication failure.

    This is process-level rollback, not a claim of multi-file crash durability.
    """
    (backup / "app").mkdir()
    shutil.copyfile(root / "app/manifest.json", backup / "app/manifest.json")
    moved_old = False
    published_kb = False
    published_manifest = False
    try:
        os.replace(root / "kb", backup / "kb")
        moved_old = True
        os.replace(stage / "kb", root / "kb")
        published_kb = True
        os.replace(stage / "app/manifest.json", root / "app/manifest.json")
        published_manifest = True
    except BaseException as exc:
        try:
            if published_manifest:
                shutil.copyfile(backup / "app/manifest.json", root / "app/manifest.json")
            if published_kb:
                shutil.rmtree(root / "kb")
            if moved_old:
                os.replace(backup / "kb", root / "kb")
        except OSError as rollback_error:
            raise ApplicationError(
                f"refresh publication failed and rollback failed; recovery backup: {backup}: {rollback_error}"
            ) from exc
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            raise
        raise ApplicationError(f"refresh publication failed; original vault restored: {exc}") from exc


def refresh_vocabulary(design_root: Path, vault: Path, *, dry_run: bool = False) -> Mapping[str, object]:
    """Replace only ``kb/`` and ``app/manifest.json`` after provenance checks.

    A sibling lock excludes other refresh calls. Other editors must remain idle
    during publication; files are rechecked immediately before the first write.
    The successful backup retains the previous reference tree and manifest.
    """
    snapshot = load_design(Path(design_root))
    root = _vault_root(snapshot, vault)
    manifest_path = root / "app/manifest.json"
    if (root / "app").is_symlink() or manifest_path.is_symlink():
        raise ApplicationError(f"unsafe vault manifest path: {manifest_path}")
    lock = root.parent / f".{root.name}.refresh.lock"
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise ApplicationError(f"vault refresh lock already exists: {lock}") from exc
    except OSError as exc:
        raise ApplicationError(f"cannot acquire vault refresh lock: {exc}") from exc
    temporary: Optional[Path] = None
    try:
        raw = manifest_path.read_bytes()
        old = _old_snapshot(snapshot, manifest_path, raw)
        entries = _manifest_files(manifest_path, json.loads(raw)["files"])
        actual = _managed_files_on_disk(root, entries)
        markdown = _markdown_bytes(root)
        temporary = Path(tempfile.mkdtemp(prefix=f".{root.name}.refresh-stage-", dir=root.parent))
        reference_root = temporary / "reference"
        export_reference(snapshot, reference_root)
        references = _reference_files(reference_root)
        formats = _check_managed(root, raw, actual, references)
        for relative in formats:
            if relative in references:
                references[relative] = actual[relative]
        staged = temporary / "vault"
        (staged / "content").mkdir(parents=True)
        _write_files(staged, actual)
        # Only demonstrably equivalent Base formatting may change old hashes.
        old_manifest = json.loads(raw)
        for entry in old_manifest["files"]:
            if entry["path"] in formats:
                entry["sha256"] = _sha256(actual[entry["path"]])
        _write_files(staged, {"app/manifest.json": _json_bytes(old_manifest)})
        _verify_old_vault(old, staged)

        _check_content(snapshot, root, references, markdown)
        managed = {path: data for path, data in actual.items() if not path.startswith("kb/")}
        managed.update(references)
        shutil.rmtree(staged / "kb")
        _write_files(staged, references)
        _write_files(staged, {"app/manifest.json": _json_bytes(_manifest(snapshot, managed))})
        verify_vault(snapshot, staged)
        changed = sum(actual.get(path) != references.get(path) for path in set(references) | {p for p in actual if p.startswith("kb/")})
        if (
            root.is_symlink()
            or (root / "app").is_symlink()
            or manifest_path.is_symlink()
            or manifest_path.read_bytes() != raw
            or _managed_files_on_disk(root, entries) != actual
            or _markdown_bytes(root) != markdown
        ):
            raise ApplicationError("vault changed during refresh preparation; no publication performed")
        backup = None
        if not dry_run:
            backup = Path(tempfile.mkdtemp(prefix=f".{root.name}.refresh-backup-", dir=root.parent))
            _publish(root, staged, backup)
        return {
            "design_commit": snapshot.commit,
            "previous_design_commit": old.commit,
            "changed_count": changed,
            "normalized_base_formats": formats,
            "backup_path": str(backup) if backup is not None else None,
            "dry_run": dry_run,
        }
    except OSError as exc:
        raise ApplicationError(f"cannot refresh vocabulary: {exc}") from exc
    finally:
        if temporary is not None:
            shutil.rmtree(temporary, ignore_errors=True)
        lock.rmdir()
