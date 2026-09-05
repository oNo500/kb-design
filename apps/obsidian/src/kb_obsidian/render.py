"""Render the small, deterministic Markdown fragments owned by the application."""

from __future__ import annotations

from collections.abc import Mapping

import yaml


def render_frontmatter(properties: Mapping[str, object]) -> str:
    """Render YAML frontmatter with stable input order and UTF-8-safe text."""
    document = yaml.safe_dump(
        dict(properties),
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )
    return f"---\n{document}---\n"
