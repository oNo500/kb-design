#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Sequence

import yaml


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.source_model import ReferenceUse, collect_reference_uses


FORMAL_SUFFIXES = {".yaml", ".yml", ".json"}
EXCLUDED_PARTS = {"generated", "migrations", ".superpowers", "tests"}
INDEX_KEYS = (
    "target_kind", "target_id", "reference_kind", "file", "record", "field_path",
)


def discover_formal_documents(root: Path) -> Sequence[Path]:
    return tuple(sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.suffix in FORMAL_SUFFIXES
        and not EXCLUDED_PARTS.intersection(path.relative_to(root).parts)
    ))


def load_yaml_or_json(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    return yaml.safe_load(text) or {}


def load_front_matter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return {}
    return yaml.safe_load(text.split("---\n", 2)[1]) or {}


def index_row(target_kind, target_id, reference_kind, file, record, field_path):
    return {
        "target_kind": target_kind,
        "target_id": target_id,
        "reference_kind": reference_kind,
        "file": str(file),
        "record": record,
        "field_path": field_path,
    }


def visit_reference_use(use: ReferenceUse) -> Dict[str, str]:
    if use.kind == "basis":
        return index_row(
            "source_entity", use.value["entity"], "basis.entity",
            use.file, use.record, use.field_path + ".entity",
        )
    return index_row(
        "source_use", use.value["registry"], f"{use.kind}.registry",
        use.file, use.record, use.field_path + ".registry",
    )


def visit_uses(root: Path) -> List[Dict[str, str]]:
    path = root / "vocab/sources.yaml"
    if not path.exists():
        return []
    document = load_yaml_or_json(path)
    rows = []
    for use_index, source_use in enumerate(document.get("sources", [])):
        record = f"source_use:{source_use['id']}"
        rows.append(index_row(
            "source_entity", source_use["entity"], "use.entity",
            "vocab/sources.yaml", record, f"sources[{use_index}].entity",
        ))
        for role_index, role in enumerate(source_use.get("roles", [])):
            if role.get("decision"):
                rows.append(index_row(
                    "decision", role["decision"], "role.decision",
                    "vocab/sources.yaml", record,
                    f"sources[{use_index}].roles[{role_index}].decision",
                ))
    return rows


def visit_replacements(root: Path) -> List[Dict[str, str]]:
    path = root / "vocab/entities.yaml"
    if not path.exists():
        return []
    document = load_yaml_or_json(path)
    return [
        index_row(
            "source_entity", entity["replaced_by"], "entity.replaced_by",
            "vocab/entities.yaml", f"entity:{entity['id']}",
            f"entities[{index}].replaced_by",
        )
        for index, entity in enumerate(document.get("entities", []))
        if entity.get("replaced_by")
    ]


def _decision_values(value, field_path):
    if isinstance(value, str):
        return [(field_path, value)]
    if isinstance(value, list):
        return [(f"{field_path}[{index}]", item)
                for index, item in enumerate(value) if isinstance(item, str)]
    return []


def walk_decision_ids(front):
    rows = []
    for key in ("decision", "decisions", "supersedes"):
        rows.extend(_decision_values(front.get(key), key))
    for history_index, history in enumerate(front.get("history", [])):
        if not isinstance(history, dict):
            continue
        for key in ("decision", "decisions", "supersedes"):
            rows.extend(_decision_values(
                history.get(key), f"history[{history_index}].{key}",
            ))
    return rows


def visit_decisions(root: Path) -> List[Dict[str, str]]:
    directory = root / "design/decisions"
    if not directory.exists():
        return []
    rows = []
    for path in sorted(directory.glob("source-*.md")):
        front = load_front_matter(path)
        if not front.get("id"):
            continue
        record = f"decision:{front['id']}"
        for field_path, decision_id in walk_decision_ids(front):
            if decision_id != front["id"]:
                rows.append(index_row(
                    "decision", decision_id, "history.decision",
                    str(path.relative_to(root)), record, field_path,
                ))
    return rows


def target_identity(target) -> str:
    if target["kind"] == "decision" and target["record"].startswith("decision:"):
        return target["record"].split(":", 1)[1]
    if target["kind"] == "obligation" and ":" in target["record"]:
        return target["record"].split(":", 1)[1]
    return "#".join((target["file"], target["record"], target["field_path"]))


def visit_obligations(root: Path) -> List[Dict[str, str]]:
    path = root / "vocab/source-obligations.yaml"
    if not path.exists():
        return []
    document = load_yaml_or_json(path)
    rows = []
    for index, obligation in enumerate(document.get("obligations", [])):
        record = f"source_obligation:{obligation['id']}"
        for decision_index, decision in enumerate(obligation.get("decisions", [])):
            rows.append(index_row(
                "decision", decision, "obligation.decisions",
                "vocab/source-obligations.yaml", record,
                f"obligations[{index}].decisions[{decision_index}]",
            ))
        if obligation.get("previous"):
            rows.append(index_row(
                "source_obligation", obligation["previous"], "obligation.previous",
                "vocab/source-obligations.yaml", record,
                f"obligations[{index}].previous",
            ))
        for target_index, target in enumerate(obligation.get("targets", [])):
            rows.append(index_row(
                target["kind"], target_identity(target), "obligation.target",
                "vocab/source-obligations.yaml", record,
                f"obligations[{index}].targets[{target_index}]",
            ))
    return rows


def _legacy_record_rows(relative, collection, record_path, record):
    record_id = record.get("id", record_path)
    stable_record = f"{collection}:{record_id}"
    rows = []
    source = record.get("source")
    if isinstance(source, str):
        kind = "legacy.array_source" if collection == "arrays" else "legacy.source"
        rows.append(index_row(
            "source_entity", source, kind, relative, stable_record,
            f"{record_path}.source",
        ))
    basis = record.get("basis")
    if isinstance(basis, dict):
        for basis_key, basis_value in basis.items():
            values = basis_value if isinstance(basis_value, list) else [basis_value]
            for index, value in enumerate(values):
                if not isinstance(value, str) or value in {"none", "self"}:
                    continue
                target = source if value == "source" and isinstance(source, str) else value.split(":", 1)[0]
                suffix = f"[{index}]" if isinstance(basis_value, list) else ""
                rows.append(index_row(
                    "source_entity", target, "legacy.basis", relative, stable_record,
                    f"{record_path}.basis.{basis_key}{suffix}",
                ))
    match = record.get("match")
    if isinstance(match, list):
        for index, item in enumerate(match):
            if isinstance(item, dict) and isinstance(item.get("source"), str):
                rows.append(index_row(
                    "source_entity", item["source"], "legacy.match", relative,
                    stable_record, f"{record_path}.match[{index}].source",
                ))
    return rows


def visit_legacy_references(root: Path) -> List[Dict[str, str]]:
    rows = []
    for path in discover_formal_documents(root):
        relative = str(path.relative_to(root))
        document = load_yaml_or_json(path)
        if not isinstance(document, dict):
            continue
        for collection, records in document.items():
            if isinstance(records, list):
                for index, record in enumerate(records):
                    if isinstance(record, dict):
                        rows.extend(_legacy_record_rows(
                            relative, collection, f"{collection}[{index}]", record,
                        ))
            elif isinstance(records, dict):
                for key, record in records.items():
                    if isinstance(record, dict):
                        rows.extend(_legacy_record_rows(
                            relative, collection, f"{collection}.{key}", record,
                        ))
    return rows


def unique_entries(entries):
    by_key = {tuple(row[key] for key in INDEX_KEYS): row for row in entries}
    return list(by_key.values())


def build_reference_index(root: Path, include_legacy: bool = False) -> Dict[str, object]:
    entries = []
    for path in discover_formal_documents(root):
        document = load_yaml_or_json(path)
        relative = path.relative_to(root)
        entries.extend(
            visit_reference_use(use)
            for use in collect_reference_uses(relative, document)
        )
    entries.extend(visit_uses(root))
    entries.extend(visit_replacements(root))
    entries.extend(visit_decisions(root))
    entries.extend(visit_obligations(root))
    if include_legacy:
        entries.extend(visit_legacy_references(root))
    entries = unique_entries(entries)
    entries.sort(key=lambda row: tuple(row[key] for key in INDEX_KEYS))
    return {
        "schema": "urn:kb-design:data:source-reference-index",
        "schema_version": 1,
        "entries": entries,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--include-legacy", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    document = build_reference_index(args.root, args.include_legacy)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
