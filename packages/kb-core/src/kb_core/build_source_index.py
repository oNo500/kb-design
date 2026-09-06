#!/usr/bin/env python3
from kb_core.repository import project_root
import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Sequence

import yaml


ROOT = project_root()

from kb_core.source_model import ReferenceUse, collect_reference_uses


FORMAL_SUFFIXES = {".yaml", ".yml", ".json"}
EXCLUDED_PARTS = {"generated", "migrations", ".superpowers", "tests"}
INDEX_KEYS = (
    "target_kind", "target_id", "reference_kind", "file", "record", "field_path",
)


def discover_formal_documents(root: Path) -> Sequence[Path]:
    return tuple(sorted(
        path for path in (root / "data/vocab").rglob("*")
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
    path = root / "data/vocab/sources.yaml"
    if not path.exists():
        return []
    document = load_yaml_or_json(path)
    rows = []
    for use_index, source_use in enumerate(document.get("sources", [])):
        record = f"source_use:{source_use['id']}"
        rows.append(index_row(
            "source_entity", source_use["entity"], "use.entity",
            "data/vocab/sources.yaml", record, f"sources[{use_index}].entity",
        ))
        for role_index, role in enumerate(source_use.get("roles", [])):
            if role.get("decision"):
                rows.append(index_row(
                    "decision", role["decision"], "role.decision",
                    "data/vocab/sources.yaml", record,
                    f"sources[{use_index}].roles[{role_index}].decision",
                ))
    return rows


def visit_replacements(root: Path) -> List[Dict[str, str]]:
    path = root / "data/vocab/entities.yaml"
    if not path.exists():
        return []
    document = load_yaml_or_json(path)
    return [
        index_row(
            "source_entity", entity["replaced_by"], "entity.replaced_by",
            "data/vocab/entities.yaml", f"entity:{entity['id']}",
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


def visit_record_decisions(relative: Path, document: object) -> List[Dict[str, str]]:
    """Index declared decisions without treating audit snapshots as current data."""
    if not isinstance(document, dict):
        return []
    if str(relative) == "data/vocab/terms.yaml":
        return visit_term_decisions(relative, document)
    contexts = {
        "data/vocab/entities.yaml": ("entities", "entity"),
        "data/vocab/sources.yaml": ("sources", "source_use"),
        "data/vocab/forms.yaml": ("arrays", "arrays"),
    }
    context = contexts.get(str(relative))
    if context is None:
        return []
    collection, record_kind = context
    rows = []
    for index, record in enumerate(document.get(collection, [])):
        if not isinstance(record, dict):
            continue
        if collection == "arrays":
            local = record.get("local_analysis")
            if not isinstance(local, dict):
                continue
            references = [(f"local_analysis.{path}", decision, "local_analysis.decision")
                          for path, decision in walk_decision_ids({"decision": local.get("decision")})]
        else:
            references = [(path, decision, "history.decision")
                          for path, decision in walk_decision_ids({"history": record.get("history", [])})]
        for field_path, decision_id, reference_kind in references:
            rows.append(index_row(
                "decision", decision_id, reference_kind, relative,
                f"{record_kind}:{record.get('id', index)}", f"{collection}[{index}].{field_path}",
            ))
    return rows


def visit_term_decisions(relative: Path, document: dict) -> List[Dict[str, str]]:
    """Index current approvals and history decisions, never nested audit values."""
    from kb_core.governance.term_maintenance import current_basis_decisions
    rows = []
    for concept_index, concept in enumerate(document.get("concepts", [])):
        concept_path = f"concepts[{concept_index}]"
        records = [(concept, f"concept:{concept.get('id')}", concept_path)]
        for language_index, language in enumerate(concept.get("languages", [])):
            for term_index, term in enumerate(language.get("terms", [])):
                records.append((
                    term, f"term:{term.get('id')}",
                    f"{concept_path}.languages[{language_index}].terms[{term_index}]",
                ))
        for record, identity, prefix in records:
            for path, decision in current_basis_decisions(record):
                rows.append(index_row(
                    "decision", decision, "basis.approval", relative, identity, f"{prefix}.{path}",
                ))
            for path, decision in walk_decision_ids({"history": record.get("history", [])}):
                rows.append(index_row(
                    "decision", decision, "history.decision", relative, identity,
                    f"{prefix}.{path}",
                ))
    return rows


def visit_decisions(root: Path) -> List[Dict[str, str]]:
    directory = root / "docs/decisions"
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
    path = root / "data/vocab/source-obligations.yaml"
    if not path.exists():
        return []
    document = load_yaml_or_json(path)
    rows = []
    for index, obligation in enumerate(document.get("obligations", [])):
        record = f"source_obligation:{obligation['id']}"
        for decision_index, decision in enumerate(obligation.get("decisions", [])):
            rows.append(index_row(
                "decision", decision, "obligation.decisions",
                "data/vocab/source-obligations.yaml", record,
                f"obligations[{index}].decisions[{decision_index}]",
            ))
        if obligation.get("previous"):
            rows.append(index_row(
                "source_obligation", obligation["previous"], "obligation.previous",
                "data/vocab/source-obligations.yaml", record,
                f"obligations[{index}].previous",
            ))
        for target_index, target in enumerate(obligation.get("targets", [])):
            rows.append(index_row(
                target["kind"], target_identity(target), "obligation.target",
                "data/vocab/source-obligations.yaml", record,
                f"obligations[{index}].targets[{target_index}]",
            ))
    return rows


def visit_language_basis(relative: Path, document: object) -> List[Dict[str, str]]:
    """Index source-use references in the current structured language evidence."""
    rows = []
    if not isinstance(document, dict):
        return rows
    for collection, records in document.items():
        if not isinstance(records, list):
            continue
        for index, record in enumerate(records):
            if not isinstance(record, dict) or not isinstance(record.get("basis"), dict):
                continue
            for language in ("zh", "en"):
                basis = record["basis"].get(language)
                if not isinstance(basis, dict) or type(basis.get("level")) is not int:
                    continue
                if not 1 <= basis["level"] <= 4:
                    continue
                references = basis.get("references", [])
                if not isinstance(references, list):
                    continue
                for ref_index, reference in enumerate(references):
                    if not isinstance(reference, dict) or not isinstance(reference.get("source"), str):
                        continue
                    rows.append(index_row(
                        "source_use", reference["source"], "label_basis.source", relative,
                        f"{collection}:{record.get('id', index)}",
                        f"{collection}[{index}].basis.{language}.references[{ref_index}].source",
                    ))
    return rows


def unique_entries(entries):
    by_key = {tuple(row[key] for key in INDEX_KEYS): row for row in entries}
    return list(by_key.values())


def build_reference_index(root: Path) -> Dict[str, object]:
    entries = []
    for path in discover_formal_documents(root):
        document = load_yaml_or_json(path)
        relative = path.relative_to(root)
        entries.extend(visit_language_basis(relative, document))
        entries.extend(visit_record_decisions(relative, document))
        entries.extend(
            visit_reference_use(use)
            for use in collect_reference_uses(relative, document)
            if isinstance(use.value, dict) and isinstance(use.value.get("entity" if use.kind == "basis" else "registry"), str)
            and use.value.get("entity" if use.kind == "basis" else "registry")
        )
    entries.extend(visit_uses(root))
    entries.extend(visit_replacements(root))
    entries.extend(visit_decisions(root))
    entries.extend(visit_obligations(root))
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
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    from kb_core.source_model import validate_repository
    issues = validate_repository(args.root)
    if issues:
        for issue in issues:
            print(f"{issue.code}\t{issue.file}\t{issue.field_path}\t{issue.message}", file=sys.stderr)
        return 1
    document = build_reference_index(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
