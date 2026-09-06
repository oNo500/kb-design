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
from kb_core.governance.term_git import TermGitError, captured_previous_terms
from kb_core.repository import project_root

from .errors import ApplicationError


_FORMAL_DOCUMENTS = {
    "topics": "data/vocab/topics.yaml",
    "entities": "data/vocab/entities.yaml",
    "sources": "data/vocab/sources.yaml",
    "types": "data/vocab/types.yaml",
    "genres": "data/vocab/genres.yaml",
    "forms": "data/vocab/forms.yaml",
}
_OPTIONAL_TERM_DOCUMENTS = {
    "terms": "data/vocab/terms.yaml",
    "term_state": "data/vocab/term-cutover-state.yaml",
}
_TERM_SCHEMA_FILES = (
    "schemas/terms-v1.schema.json",
    "schemas/term-cutover-state-v1.schema.json",
)
_IMPLEMENTATION_FILES = (
    "pyproject.toml",
    "apps/obsidian/src/kb_obsidian/exporter.py",
    "packages/kb-core/src/kb_core/__init__.py",
    "packages/kb-core/src/kb_core/label_basis.py",
    "packages/kb-core/src/kb_core/source_model.py",
    "packages/kb-core/src/kb_core/label_adoptions.py",
    "packages/kb-core/src/kb_core/repository.py",
    "packages/kb-core/src/kb_core/governance/__init__.py",
    "packages/kb-core/src/kb_core/governance/term_model.py",
    "packages/kb-core/src/kb_core/governance/term_git.py",
    "packages/kb-core/src/kb_core/governance/term_transitions.py",
    "packages/kb-core/src/kb_core/governance/term_validation.py",
    "packages/kb-core/src/kb_core/governance/term_rendering.py",
    "schemas/terms-v1.schema.json",
    "schemas/term-cutover-state-v1.schema.json",
)


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
    try:
        return _resolve_git_root(project_root(Path(__file__)))
    except (OSError, ValueError) as exc:
        raise ApplicationError("cannot locate owning design checkout; use --design-root") from exc


def _verify_snapshot_implementation(root: Path, commit: str) -> Mapping[str, bytes]:
    """Return selected implementation bytes only when Git and the worktree agree."""
    verified: dict[str, bytes] = {}
    decision_paths = tuple(path for path in _git(root, "ls-tree", "-r", "--name-only", commit, "--", "docs/decisions").splitlines()
                           if Path(path).parent.as_posix() == "docs/decisions"
                           and (Path(path).match("source-*.md") or Path(path).match("term-*.md")))
    actual_decisions = {
        path.relative_to(root).as_posix()
        for pattern in ("source-*.md", "term-*.md")
        for path in (root / "docs/decisions").glob(pattern)
    }
    if actual_decisions != set(decision_paths):
        raise ApplicationError("source decision file set differs from commit")
    optional_paths = tuple(path for path in (
        "data/inputs/topics/label-adoptions.json", "data/vocab/source-obligations.yaml")
        if path in _git(root, "ls-tree", "-r", "--name-only", commit, "--", path).splitlines())
    actual_optional = {path for path in ("data/inputs/topics/label-adoptions.json", "data/vocab/source-obligations.yaml")
                       if (root / path).exists()}
    if actual_optional != set(optional_paths):
        raise ApplicationError("source support file set differs from commit")
    for relative_path in (*_IMPLEMENTATION_FILES, *decision_paths, *optional_paths):
        try:
            current = (root / relative_path).read_bytes()
            committed = subprocess.run(
                ["git", "-C", str(root), "show", f"{commit}:{relative_path}"],
                capture_output=True,
                check=False,
            )
        except OSError as exc:
            raise ApplicationError(
                f"cannot read selected design implementation {relative_path}: {exc}"
            ) from exc
        if committed.returncode:
            raise ApplicationError(
                f"selected design implementation is not tracked: {relative_path}"
            )
        if current != committed.stdout:
            raise ApplicationError(
                f"selected design implementation differs from commit: {relative_path}"
            )
        verified[relative_path] = current
    return MappingProxyType(verified)


def _validate_formal_inputs(root: Path, inputs: Mapping[str, bytes]) -> None:
    """Reuse the checkout's exporter contract against exactly the captured bytes."""
    script = (
        "import json, pathlib, runpy, sys; "
        "root = pathlib.Path(sys.argv[1]); "
        "sys.path.insert(0, str(root / 'packages/kb-core/src')); "
        "sys.path.insert(0, str(root / 'apps/obsidian/src')); "
        "exporter = runpy.run_path(str(root / 'apps/obsidian/src/kb_obsidian/exporter.py')); "
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
    _verify_snapshot_implementation(design_root, commit)

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
    optional_paths = set(_OPTIONAL_TERM_DOCUMENTS.values())
    committed_optional = set(
        _git(
            design_root,
            "ls-tree",
            "-r",
            "--name-only",
            commit,
            "--",
            *_OPTIONAL_TERM_DOCUMENTS.values(),
        ).splitlines()
    )
    disk_optional = {
        relative_path
        for relative_path in _OPTIONAL_TERM_DOCUMENTS.values()
        if (design_root / relative_path).exists()
    }
    if len(committed_optional) == 1 or len(disk_optional) == 1:
        raise ApplicationError(
            "data/vocab/terms.yaml and data/vocab/term-cutover-state.yaml "
            "must either both exist or both be absent"
        )
    if committed_optional != disk_optional:
        raise ApplicationError("term input file set differs from commit")
    optional_present = disk_optional == optional_paths
    formal_documents = dict(_FORMAL_DOCUMENTS)
    if optional_present:
        formal_documents.update(_OPTIONAL_TERM_DOCUMENTS)
        for name, relative_path in _OPTIONAL_TERM_DOCUMENTS.items():
            try:
                content = (design_root / relative_path).read_bytes()
            except OSError as exc:
                raise ApplicationError(f"cannot read formal design document {relative_path}: {exc}") from exc
            captured[name] = content
            input_hashes[relative_path] = hashlib.sha256(content).hexdigest()
        try:
            previous_terms = captured_previous_terms(
                design_root,
                captured["terms"],
                commit=commit,
            )
        except TermGitError as exc:
            raise ApplicationError(str(exc)) from exc
        if previous_terms is not None:
            captured["_support:previous-terms.yaml"] = previous_terms
    # Capture decision, obligation and language-adoption bytes from the same
    # verified commit. The reader consumes these bytes, never a later disk read.
    support = _verify_snapshot_implementation(design_root, commit)
    captured.update({"_support:" + path: content for path, content in support.items()
                     if path.startswith("docs/decisions/") or path.startswith("data/")
                     or (optional_present and path in _TERM_SCHEMA_FILES)})
    if optional_present:
        for relative_path in _TERM_SCHEMA_FILES:
            input_hashes[relative_path] = hashlib.sha256(support[relative_path]).hexdigest()
    _validate_formal_inputs(design_root, captured)
    for name, content in captured.items():
        if name.startswith("_support:"):
            continue
        try:
            documents[name] = _freeze(yaml.safe_load(content))
        except (UnicodeError, yaml.YAMLError) as exc:
            raise ApplicationError(f"cannot parse formal design document {formal_documents[name]}: {exc}") from exc
    if (_git(design_root, "rev-parse", "HEAD") != commit
            or _git(design_root, "status", "--porcelain", "--untracked-files=no")):
        raise ApplicationError("design source changed while loading snapshot")
    _verify_snapshot_implementation(design_root, commit)
    # Git status alone can miss skip-worktree edits or untracked replacements.
    for name, relative_path in formal_documents.items():
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
