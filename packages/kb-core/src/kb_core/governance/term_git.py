"""Capture the prior formal terminology value from Git history."""

from __future__ import annotations

import subprocess
from pathlib import Path


TERMS_PATH = "data/vocab/terms.yaml"


class TermGitError(ValueError):
    """Raised when available Git history cannot be queried reliably."""


def _run(root: Path, *arguments: str, allow_non_repository: bool = False):
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise TermGitError(f"cannot inspect term Git history: {exc}") from exc
    if completed.returncode:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        if allow_non_repository and "not a git repository" in detail.lower():
            return None
        raise TermGitError(f"cannot inspect term Git history: {detail or arguments[0]}")
    return completed.stdout


def _tree_bytes(root: Path, commit: str) -> bytes | None:
    paths = _run(root, "ls-tree", "-r", "--name-only", commit, "--", TERMS_PATH)
    listed = paths.decode("utf-8").splitlines()
    if not listed:
        return None
    if listed != [TERMS_PATH]:
        raise TermGitError("cannot resolve committed term input")
    return _run(root, "show", f"{commit}:{TERMS_PATH}")


def captured_previous_terms(
    root: Path,
    current_bytes: bytes,
    *,
    commit: str | None = None,
) -> bytes | None:
    """Return the preceding committed terms bytes, if a preceding value exists."""
    repository = Path(root)
    if commit is None:
        inside = _run(
            repository,
            "rev-parse",
            "--is-inside-work-tree",
            allow_non_repository=True,
        )
        if inside is None:
            return None
        selected = _run(repository, "rev-parse", "HEAD").decode("ascii").strip()
        head_bytes = _tree_bytes(repository, selected)
        if head_bytes is None:
            return None
        if head_bytes != current_bytes:
            return head_bytes
    else:
        selected = commit
        _run(repository, "rev-parse", "--verify", f"{selected}^{{commit}}")
        committed = _tree_bytes(repository, selected)
        if committed is None:
            raise TermGitError(f"{TERMS_PATH} is absent from selected commit")
        if committed != current_bytes:
            raise TermGitError(f"{TERMS_PATH} differs from selected commit")

    data_commit = _run(
        repository,
        "log",
        "-1",
        "--format=%H",
        selected,
        "--",
        TERMS_PATH,
    ).decode("ascii").strip()
    if not data_commit:
        raise TermGitError("cannot locate committed term input history")
    lineage = _run(
        repository, "rev-list", "--parents", "-n", "1", data_commit
    ).decode("ascii").split()
    if not lineage or lineage[0] != data_commit:
        raise TermGitError("cannot inspect committed term input history")
    if len(lineage) == 1:
        return None
    return _tree_bytes(repository, lineage[1])
