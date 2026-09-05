"""Read a verified clean kb-design checkout and its formal inputs."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

import yaml

from .errors import ApplicationError


_FORMAL_DOCUMENTS = {
    "topics": "vocab/topics.yaml",
    "entities": "vocab/entities.yaml",
    "sources": "vocab/sources.yaml",
    "types": "vocab/types.yaml",
    "genres": "vocab/genres.yaml",
    "forms": "vocab/forms.yaml",
}


@dataclass(frozen=True)
class DesignSnapshot:
    root: Path
    commit: str
    documents: Mapping[str, object]
    input_hashes: Mapping[str, str]


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _git(root: Path, *arguments: str) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise ApplicationError(f"cannot inspect design repository: {exc}") from exc
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise ApplicationError(f"cannot inspect design repository: {detail}")
    return completed.stdout.strip()


def _resolve_git_root(root: Path) -> Path:
    candidate = Path(root)
    if not candidate.is_absolute():
        raise ApplicationError("design root must be absolute")
    try:
        candidate = candidate.resolve(strict=True)
    except OSError as exc:
        raise ApplicationError(f"design root does not exist: {root}") from exc
    if not candidate.is_dir():
        raise ApplicationError(f"design root is not a directory: {candidate}")
    repository_root = Path(_git(candidate, "rev-parse", "--show-toplevel"))
    try:
        repository_root = repository_root.resolve(strict=True)
    except OSError as exc:
        raise ApplicationError(f"cannot resolve design repository root: {repository_root}") from exc
    if candidate != repository_root:
        raise ApplicationError("design root must be the Git repository root")
    return candidate


def default_design_root() -> Path:
    """Find the checkout owning this source installation, independent of cwd."""
    source = Path(__file__).resolve()
    for candidate in source.parents:
        if (candidate / "tools/obsidian/src/kb_obsidian/design_source.py") == source:
            return _resolve_git_root(candidate)
    raise ApplicationError("cannot locate owning design checkout; use --design-root")


def _validate_formal_inputs(root: Path, inputs: Mapping[str, bytes]) -> None:
    """Reuse the checkout's exporter contract against exactly the captured bytes."""
    script = (
        "import json, pathlib, runpy, sys; "
        "root = pathlib.Path(sys.argv[1]); "
        "sys.path.insert(0, str(root / 'scripts')); "
        "exporter = runpy.run_path(str(root / 'scripts/export_obsidian.py')); "
        "inputs = {name: bytes.fromhex(value) for name, value in json.load(sys.stdin).items()}; "
        "exporter['load_repository'](root, input_bytes=inputs)"
    )
    try:
        completed = subprocess.run(
            [sys.executable, "-c", script, str(root)],
            input=json.dumps({name: content.hex() for name, content in inputs.items()}),
            capture_output=True, text=True, check=False,
        )
    except OSError as exc:
        raise ApplicationError(f"cannot validate formal design: {exc}") from exc
    if completed.returncode:
        detail = completed.stderr.strip().splitlines()
        raise ApplicationError(f"invalid formal design: {detail[-1] if detail else 'validation failed'}")


def load_design(root: Path) -> DesignSnapshot:
    """Load and validate the six formal documents from a clean Git snapshot."""
    design_root = _resolve_git_root(root)
    commit = _git(design_root, "rev-parse", "HEAD")
    if _git(design_root, "status", "--porcelain", "--untracked-files=no"):
        raise ApplicationError("design repository has tracked changes")

    documents: dict[str, object] = {}
    input_hashes: dict[str, str] = {}
    captured: dict[str, bytes] = {}
    for name, relative_path in _FORMAL_DOCUMENTS.items():
        try:
            content = (design_root / relative_path).read_bytes()
        except OSError as exc:
            raise ApplicationError(f"cannot read formal design document {relative_path}: {exc}") from exc
        captured[name] = content
        input_hashes[relative_path] = hashlib.sha256(content).hexdigest()
    _validate_formal_inputs(design_root, captured)
    for name, content in captured.items():
        try:
            documents[name] = _freeze(yaml.safe_load(content))
        except (UnicodeError, yaml.YAMLError) as exc:
            raise ApplicationError(f"cannot parse formal design document {_FORMAL_DOCUMENTS[name]}: {exc}") from exc
    if (_git(design_root, "rev-parse", "HEAD") != commit
            or _git(design_root, "status", "--porcelain", "--untracked-files=no")):
        raise ApplicationError("design source changed while loading snapshot")
    # Git status alone can miss skip-worktree edits or untracked replacements.
    for name, relative_path in _FORMAL_DOCUMENTS.items():
        try:
            committed = subprocess.run(
                ["git", "-C", str(design_root), "show", f"{commit}:{relative_path}"],
                capture_output=True, check=False,
            )
            current = (design_root / relative_path).read_bytes()
        except OSError as exc:
            raise ApplicationError(f"cannot verify formal design document {relative_path}: {exc}") from exc
        if committed.returncode or captured[name] != committed.stdout or current != captured[name]:
            raise ApplicationError(f"design source changed while loading snapshot: {relative_path}")

    return DesignSnapshot(
        root=design_root,
        commit=commit,
        documents=MappingProxyType(documents),
        input_hashes=MappingProxyType(input_hashes),
    )
