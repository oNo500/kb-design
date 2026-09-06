"""Validate terminology data and build its read-only maintenance index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from kb_core.repository import project_root
from kb_core.source_model import normalize_yaml_dates
from kb_core.governance.build_terms import capture_validation_context, load_glossary_layout
from kb_core.governance.term_maintenance import build_term_reference_index, decision_index
from kb_core.governance.term_model import ROOT as SCHEMA_ROOT
from kb_core.governance.term_git import captured_previous_terms
from kb_core.governance.term_validation import validate_term_snapshot


def _load(path):
    return normalize_yaml_dates(yaml.safe_load(path.read_text(encoding="utf-8")))


def read_term_data(root, *, terms=None, state=None, previous=None, require_publication=False):
    """Use the same source and admission checks as the generation path."""
    root = Path(root).resolve()
    term_path = Path(terms) if terms is not None else root / "data/vocab/terms.yaml"
    state_path = Path(state) if state is not None else root / "data/vocab/term-cutover-state.yaml"
    term_bytes = term_path.read_bytes()
    value = normalize_yaml_dates(yaml.safe_load(term_bytes))
    state_value = _load(state_path) if state_path.exists() else None
    if require_publication and state_value is None:
        raise ValueError("TERM_PUBLICATION_MISSING")
    sources, decisions, adoptions, historical = capture_validation_context(root, with_history=True)
    git_previous_bytes = captured_previous_terms(root, term_bytes)
    git_previous = (
        normalize_yaml_dates(yaml.safe_load(git_previous_bytes))
        if git_previous_bytes is not None else None
    )
    issues = list(validate_term_snapshot(
        value, source_documents=sources, accepted_decisions=decisions,
        previous=git_previous,
        state=state_value,
        historical_decisions=historical,
    ))
    if previous is not None:
        issues.extend(validate_term_snapshot(
            value, source_documents=sources, accepted_decisions=decisions,
            previous=_load(Path(previous)), historical_decisions=historical,
        ))
    if issues:
        raise ValueError("\n".join(f"{item.code} {item.path}: {item.message}" for item in issues))
    if state_value is not None:
        read_term_layout(root, value, decisions)
    return value, state_value, sources, decisions, adoptions


def read_term_layout(root, document, decisions):
    return load_glossary_layout(
        Path(root) / "data/inputs/terminology/glossary-layout.yaml",
        concept_ids={row["id"] for row in document["concepts"] if row["workflow"] == "active"},
        accepted_decisions=decisions,
    )


def registered_term_forms(root):
    """Read only available forms after explicit publication has been validated."""
    value, _, sources, decisions, adoptions = read_term_data(root, require_publication=True)
    from kb_core.governance.build_terms import build_model_label_rows
    forms = {
        term["text"]
        for concept in value["concepts"] if concept["workflow"] == "active"
        for language in concept["languages"]
        for term in language["terms"]
        if term["administrative_status"] in {"preferredTerm-admn-sts", "admittedTerm-admn-sts"}
    }
    for row in build_model_label_rows(sources["topics"], sources["forms"], adoptions, decisions):
        forms.update((row["zh"], row["en"]))
    # Preserve the diagnostic's existing vocabulary ownership, using the same
    # validated capture rather than reopening potentially changed YAML files.
    for name, collection in (("topics", "concepts"), ("entities", "entities"), ("types", "types")):
        for record in sources[name].get(collection, []):
            for field in ("label", "alt", "hidden"):
                forms.update(_strings(record.get(field)))
    return forms


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from _strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _strings(nested)


def _obligations(root):
    path = root / "data/vocab/term-obligations.yaml"
    if not path.exists():
        return {"obligations": []}
    value = _load(path)
    schema = json.loads((SCHEMA_ROOT / "schemas/term-obligations-v1.schema.json").read_text())
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value))
    if errors:
        raise ValueError("TERM_OBLIGATION_SCHEMA_INVALID " + errors[0].json_path)
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "index"))
    parser.add_argument("--root", type=Path, default=project_root())
    parser.add_argument("--terms", type=Path)
    parser.add_argument("--state", type=Path)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        value, state, _, decisions, _ = read_term_data(
            root, terms=args.terms, state=args.state, previous=args.previous,
        )
        if args.command == "check":
            print("术语数据校验通过；" + ("发布状态已核对。" if state else "尚无发布状态。"))
            return 0
        obligations = _obligations(root)
        referenced_decisions = set(decisions)
        for concept in value["concepts"]:
            records = [concept, *(term for language in concept["languages"] for term in language["terms"])]
            referenced_decisions.update(event["decision"] for record in records for event in record["history"])
        paths = {key: path for key, path in decision_index(root).items() if key in referenced_decisions}
        layout = read_term_layout(root, value, decisions) if state is not None else None
        index = build_term_reference_index(
            value, obligations, paths, layout=layout, decision_documents=decisions,
        )
        output = args.output or root / "build/terms/term-reference-index.json"
        destination = output.resolve()
        protected = [root / name for name in ("data", "docs", "schemas", "packages", "apps")]
        inputs = [Path(path).resolve() for path in (args.terms, args.state, args.previous) if path]
        if destination in inputs or any(destination.is_relative_to(path) for path in protected):
            raise ValueError("TERM_INDEX_OUTPUT_OVERLAPS_INPUT")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(index, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
        print(str(output))
        return 0
    except (ValueError, OSError, yaml.YAMLError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
