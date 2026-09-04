"""Read the exact kb-design revision accepted by this application."""

from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

import yaml

from .errors import ApplicationError


SUPPORTED_DESIGN_COMMIT = "1e7aef8a5d9dc927c1c69138e61dfbabddd84253"

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


def load_design(root: Path) -> DesignSnapshot:
    """Load the six formal documents from the supported clean design revision."""
    design_root = _resolve_git_root(root)
    commit = _git(design_root, "rev-parse", "HEAD")
    if commit != SUPPORTED_DESIGN_COMMIT:
        raise ApplicationError(f"unsupported design commit: {commit}")
    if _git(design_root, "status", "--porcelain", "--untracked-files=no"):
        raise ApplicationError("design repository has tracked changes")

    documents: dict[str, object] = {}
    input_hashes: dict[str, str] = {}
    for name, relative_path in _FORMAL_DOCUMENTS.items():
        try:
            content = (design_root / relative_path).read_bytes()
        except OSError as exc:
            raise ApplicationError(f"cannot read formal design document {relative_path}: {exc}") from exc
        input_hashes[relative_path] = hashlib.sha256(content).hexdigest()
        try:
            documents[name] = _freeze(yaml.safe_load(content))
        except yaml.YAMLError as exc:
            raise ApplicationError(f"cannot parse formal design document {relative_path}: {exc}") from exc

    return DesignSnapshot(
        root=design_root,
        commit=commit,
        documents=MappingProxyType(documents),
        input_hashes=MappingProxyType(input_hashes),
    )
