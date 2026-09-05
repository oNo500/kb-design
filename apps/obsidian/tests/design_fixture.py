from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
FORMAL_PATHS = (
    "data/vocab/topics.yaml",
    "data/vocab/entities.yaml",
    "data/vocab/sources.yaml",
    "data/vocab/types.yaml",
    "data/vocab/genres.yaml",
    "data/vocab/forms.yaml",
)
IMPLEMENTATION_PATHS = (
    "apps/obsidian/src/kb_obsidian/exporter.py",
    "packages/kb-core/src/kb_core/__init__.py",
    "packages/kb-core/src/kb_core/label_basis.py",
    "packages/kb-core/src/kb_core/repository.py",
)


def create_clean_design(destination: Path) -> tuple[Path, str]:
    """Copy current formal inputs and their reader into a clean temporary repository."""
    for relative_path in (*FORMAL_PATHS, *IMPLEMENTATION_PATHS):
        source = REPOSITORY_ROOT / relative_path
        target = destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    subprocess.run(["git", "init", "--quiet", str(destination)], check=True)
    subprocess.run(
        ["git", "-C", str(destination), "config", "user.email", "test@example.invalid"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(destination), "config", "user.name", "Test"],
        check=True,
    )
    subprocess.run(["git", "-C", str(destination), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(destination), "commit", "--quiet", "-m", "current layout fixture"],
        check=True,
    )
    commit = subprocess.run(
        ["git", "-C", str(destination), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return destination, commit
