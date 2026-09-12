"""Identify document roles independently of their topic directory.

Legacy decision directories remain readable for historical snapshots and test
repositories. Current documents use role prefixes under docs topic directories.
Neither a filename nor a directory grants approval; decision schemas and their
existing acceptance rules still determine authority.
"""

from fnmatch import fnmatchcase
from pathlib import Path, PurePosixPath


def is_decision_path(path, patterns=("*.md",)):
    path = PurePosixPath(path)
    if not path.parts or path.parts[0] != "docs":
        return False
    if path.name.startswith("decision-"):
        name = path.name[len("decision-"):]
    elif path.parent == PurePosixPath("docs/decisions"):
        name = path.name
    else:
        return False
    return any(fnmatchcase(name, pattern) for pattern in patterns)


def decision_paths(directory: Path, patterns=("*.md",)):
    """Find only decision documents; do not scan copied proposal metadata."""
    directory = Path(directory)
    if directory.name == "decisions":
        # Explicit legacy snapshot/fixture directory, not all its siblings.
        return sorted(path for path in directory.glob("*.md")
                      if any(fnmatchcase(path.name, pattern) for pattern in patterns))
    return sorted(path for path in directory.rglob("*.md")
                  if is_decision_path(PurePosixPath("docs") / path.relative_to(directory), patterns))


def document_role(path):
    path = PurePosixPath(path)
    if not path.parts or path.parts[0] != "docs":
        return None
    if path.name.startswith("proposal-") or path.as_posix().startswith("docs/drafts/"):
        return "draft"
    if is_decision_path(path):
        return "history"
    if path.name.startswith("reading-") or path.as_posix().startswith("docs/references/"):
        return "source"
    return "formal"
