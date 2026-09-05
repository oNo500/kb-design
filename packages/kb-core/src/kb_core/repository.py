"""Locate project data without interpreting the caller's working directory."""

from __future__ import annotations

import os
from pathlib import Path


def project_root(start: Path | str | None = None) -> Path:
    """Return the owning checkout, or an explicitly selected data root.

    KB_DESIGN_ROOT lets repository-bound core commands operate on a selected
    input tree. Passing a source location explicitly always finds its owner.
    """
    if start is None and os.environ.get("KB_DESIGN_ROOT"):
        root = Path(os.environ["KB_DESIGN_ROOT"]).expanduser().resolve(strict=True)
        if not (root / "data/vocab").is_dir():
            raise ValueError(f"not a project data root: {root}")
        return root
    location = Path(start) if start is not None else Path(__file__)
    location = location.resolve()
    for candidate in (location, *location.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "data/vocab").is_dir():
            return candidate
    raise ValueError("cannot locate owning project; set KB_DESIGN_ROOT explicitly")
