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


def create_clean_design(destination: Path) -> tuple[Path, str]:
    """Copy current formal inputs and their reader into a clean temporary repository."""
    decisions = tuple(
        path.relative_to(REPOSITORY_ROOT).as_posix()
        for pattern in ("source-*.md", "term-*.md")
        for path in (REPOSITORY_ROOT / "docs/decisions").glob(pattern)
    )
    support = tuple(path for path in ("data/inputs/topics/label-adoptions.json", "data/vocab/source-obligations.yaml")
                    if (REPOSITORY_ROOT / path).exists())
    for relative_path in (*FORMAL_PATHS, *IMPLEMENTATION_PATHS, *decisions, *support):
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
