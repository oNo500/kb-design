from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile

import yaml

from kb_core.source_model import ReferenceUse


@contextmanager
def materialized_current_layout(source: Path):
    """Copy an immutable legacy-layout fixture into the current repository layout."""
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        mappings = (
            (source / "vocab", root / "data" / "vocab"),
            (source / "design" / "decisions", root / "docs" / "decisions"),
        )
        for old, new in mappings:
            if old.exists():
                shutil.copytree(old, new)
        yield root


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def approved_and_unapproved_role_references():
    basis = [{"entity": "cs2023", "locator": "SE overview", "checked": "2026-08-31"}]
    return [
        ReferenceUse(
            "source", "data/vocab/terms.yaml", "concept:tc-1", "source",
            {"registry": "mapping-only", "item": "SE", "locator": "SE", "basis": basis},
        ),
        ReferenceUse(
            "match", "data/vocab/terms.yaml", "concept:tc-1", "match[0]",
            {"registry": "mapping-only", "item": "SE", "rel": "exactMatch", "basis": basis},
        ),
    ]


def unapproved_external_group_reference():
    return ReferenceUse(
        "external_group", "data/vocab/topics.yaml", "array:security-asvs",
        "arrays[0].external_group",
        {
            "registry": "mapping-only",
            "item": "V11",
            "locator": "ASVS chapter V11",
            "basis": [{"entity": "asvs", "locator": "V11", "checked": "2026-08-31"}],
        },
    )
