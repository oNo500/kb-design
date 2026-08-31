#!/usr/bin/env python3
import json
import re
import shutil
from copy import deepcopy
from pathlib import Path
from typing import NamedTuple, Sequence

import yaml


class ApplyResult(NamedTuple):
    written: Sequence[str]
    blocked: Sequence[str]


PATH_TOKEN = re.compile(r"([A-Za-z_][A-Za-z0-9_-]*)|\[(\d+)\]")


def parse_field_path(value):
    tokens = []
    for key, index in PATH_TOKEN.findall(value):
        tokens.append(int(index) if index else key)
    if not tokens:
        raise ValueError(f"invalid field path: {value}")
    return tokens


def locate_parent(document, field_path):
    tokens = parse_field_path(field_path)
    current = document
    for token in tokens[:-1]:
        current = current[token]
    return current, tokens[-1]


def apply_row(document, row):
    parent, key = locate_parent(document, row["field_path"])
    actual = parent[key]
    if actual != row["old_value"]:
        raise ValueError(f"old value mismatch: {row['identity']}")
    operation = row["operation"]
    if operation == "keep":
        return False
    if operation == "set":
        parent[key] = deepcopy(row["new_value"])
    elif operation == "delete":
        del parent[key]
    elif operation == "isolate":
        if not isinstance(actual, str):
            raise ValueError(f"isolate expects scalar: {row['identity']}")
        del parent[key]
        parent["local_analysis"] = deepcopy(row["new_value"])
    else:
        raise ValueError(f"unknown operation: {operation}")
    return True


def _load_yaml_or_json(path):
    text = Path(path).read_text(encoding="utf-8")
    if Path(path).suffix == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def _write_yaml_or_json(path, document):
    path = Path(path)
    if path.suffix == ".json":
        path.write_text(
            json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        path.write_text(
            yaml.safe_dump(document, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )


def load_and_validate_ledgers(plan_dir):
    plan_dir = Path(plan_dir)
    plan_path = plan_dir / "plan.yaml"
    if not plan_path.is_file():
        raise ValueError(f"missing migration plan: {plan_path}")
    plan = yaml.safe_load(plan_path.read_text(encoding="utf-8"))
    if not isinstance(plan, dict) or plan.get("schema_version") != 1:
        raise ValueError("invalid migration plan")
    rows = plan.get("rows")
    if not isinstance(rows, list):
        raise ValueError("invalid migration rows")
    identities = [row.get("identity") for row in rows]
    if len(identities) != len(set(identities)):
        raise ValueError("duplicate migration identity")
    return plan


def _safe_relative(value):
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"non-formal path: {value}")
    return path


def group_rows_by_file(rows):
    grouped = {}
    seen = set()
    for row in rows:
        relative = _safe_relative(row["old_file"])
        key = (str(relative), row["field_path"])
        if key in seen:
            raise ValueError(f"duplicate migration field: {key}")
        seen.add(key)
        grouped.setdefault(str(relative), []).append(row)
    return grouped


def _apply_file_rewrites(candidate_root, rewrites, changed):
    for rewrite in rewrites:
        relative = str(_safe_relative(rewrite["path"]))
        path = candidate_root / relative
        if "old_sha256" in rewrite:
            import hashlib
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != rewrite["old_sha256"]:
                raise ValueError(f"old file hash mismatch: {relative}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rewrite["content"], encoding="utf-8")
        changed.add(relative)


def _validate_candidate_files(candidate_root, changed):
    for relative in sorted(changed):
        path = candidate_root / relative
        if path.suffix in {".json", ".yaml", ".yml"}:
            _load_yaml_or_json(path)


def write_candidate_tree(root, plan, output_root):
    blockers = sorted(
        row["identity"] for row in plan["rows"] if row.get("blocks_cutover")
    )
    if blockers:
        return ApplyResult((), tuple(blockers))
    if output_root.exists():
        raise ValueError("candidate output must be absent")
    temporary = output_root.with_name(output_root.name + ".building")
    if temporary.exists():
        shutil.rmtree(temporary)
    try:
        shutil.copytree(
            root,
            temporary,
            ignore=shutil.ignore_patterns(".git", ".superpowers", "__pycache__"),
        )
        changed = set()
        for relative, rows in sorted(group_rows_by_file(plan["rows"]).items()):
            path = temporary / relative
            document = _load_yaml_or_json(path)
            for row in sorted(
                rows,
                key=lambda item: (
                    item.get("old_record", ""),
                    item["field_path"],
                    item["identity"],
                ),
            ):
                if apply_row(document, row):
                    changed.add(relative)
            if relative in changed:
                _write_yaml_or_json(path, document)
        _apply_file_rewrites(
            temporary, plan.get("file_rewrites", []), changed
        )
        _validate_candidate_files(temporary, changed)
        temporary.rename(output_root)
        return ApplyResult(tuple(sorted(changed)), ())
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise


def apply_migration(root, plan_dir, output_root):
    root = Path(root).resolve()
    output_root = Path(output_root).resolve()
    if output_root == root or root in output_root.parents:
        raise ValueError("output_root must be outside formal root")
    plan = load_and_validate_ledgers(plan_dir)
    return write_candidate_tree(root, plan, output_root)
