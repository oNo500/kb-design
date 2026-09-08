from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile
import copy

import yaml

from kb_core.source_model import ReferenceUse


def current_reference_value(value):
    """Build current synthetic references from frozen historical fixture data."""
    if isinstance(value, list):
        return [current_reference_value(item) for item in value]
    if not isinstance(value, dict):
        return value
    result = {("reference" if key == "entity" else key):
              (copy.deepcopy(item) if key in {"before", "after", "history"}
               else current_reference_value(item)) for key, item in value.items()}
    if isinstance(result.get("identity"), str) and result["identity"].startswith("entities/"):
        result["identity"] = "references/" + result["identity"][9:]
    if result.get("field") == "entity":
        result["field"] = "reference"
    if "source_entity" in result:
        result["source_reference"] = result.pop("source_entity")
    if result.get("schema_version") == 2:
        result["schema_version"] = 3
    return result


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
        entity_path = root / "data/vocab/entities.yaml"
        if entity_path.exists():
            document = current_reference_value(load_yaml(entity_path))
            rows = document.get("entities", [])
            references = [row for row in rows if row.get("kind", "standard") in {"standard", "publication"}]
            document["entities"] = [row for row in rows if row.get("kind", "standard") not in {"standard", "publication"}]
            if not document["entities"]:
                document["entities"] = [{"id": "fixture-tool", "label": {"en": "Fixture tool"},
                    "kind": "software", "subjects": [], "status": "candidate", "added": "2026-09-06"}]
            entity_path.write_text(yaml.safe_dump(document))
            target = root / "data/references/bibliography.yaml"
            target.parent.mkdir(parents=True)
            target.write_text(yaml.safe_dump({"schema": "urn:kb-design:data:bibliography",
                "schema_version": 3, "version": document.get("version", {}), "references": references}))
        for path in (root / "data/vocab").glob("*.yaml"):
            if path != entity_path and path.name != "source-obligations.yaml":
                path.write_text(yaml.safe_dump(current_reference_value(load_yaml(path))))
        for path in (root / "docs/decisions").glob("*.md"):
            text = path.read_text()
            if text.startswith("---\n"):
                _, front, body = text.split("---\n", 2)
                path.write_text("---\n" + yaml.safe_dump(current_reference_value(yaml.safe_load(front))) + "---\n" + body)
        yield root


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def approved_and_unapproved_role_references():
    basis = [{"reference": "cs2023", "locator": "SE overview", "checked": "2026-08-31"}]
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
            "basis": [{"reference": "asvs", "locator": "V11", "checked": "2026-08-31"}],
        },
    )
