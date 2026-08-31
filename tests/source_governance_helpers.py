from pathlib import Path

import yaml

from scripts.source_model import ReferenceUse


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def approved_and_unapproved_role_references():
    basis = [{"entity": "cs2023", "locator": "SE overview", "checked": "2026-08-31"}]
    return [
        ReferenceUse(
            "source", "vocab/terms.yaml", "concept:tc-1", "source",
            {"registry": "mapping-only", "item": "SE", "locator": "SE", "basis": basis},
        ),
        ReferenceUse(
            "match", "vocab/terms.yaml", "concept:tc-1", "match[0]",
            {"registry": "mapping-only", "item": "SE", "rel": "exactMatch", "basis": basis},
        ),
    ]


def unapproved_external_group_reference():
    return ReferenceUse(
        "external_group", "vocab/topics.yaml", "array:security-asvs",
        "arrays[0].external_group",
        {
            "registry": "mapping-only",
            "item": "V11",
            "locator": "ASVS chapter V11",
            "basis": [{"entity": "asvs", "locator": "V11", "checked": "2026-08-31"}],
        },
    )
