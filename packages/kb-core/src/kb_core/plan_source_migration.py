#!/usr/bin/env python3
from kb_core.repository import project_root
import argparse
import csv
import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path

import yaml


ROOT = project_root()

from kb_core.source_model import load_decision_patches


INVENTORIES = (
    "source-entities.tsv",
    "source-roles.tsv",
    "basis-inventory.tsv",
    "source-inventory.tsv",
    "match-inventory.tsv",
    "origin-inventory.tsv",
)
LEDGER_NAMES = {
    "source-entities.tsv": "entities",
    "source-roles.tsv": "uses",
    "basis-inventory.tsv": "basis",
    "source-inventory.tsv": "source",
    "match-inventory.tsv": "match",
    "origin-inventory.tsv": "origin",
}
EXPECTED_COUNTS = {
    "entities": 138,
    "uses": 47,
    "basis": 1501,
    "source": 726,
    "match": 756,
    "origin": 19,
}
TSV_FIELDS = (
    "文件",
    "位置",
    "对象",
    "当前值",
    "草案分类",
    "证据或上下文",
    "拟议去向",
    "决策级别",
    "状态",
)
VALID_INVENTORY_STATES = {"可机械迁移", "需要复核", "待人决定", "无需迁移"}
REQUIRED_QIDS = frozenset(f"Q{number:02d}" for number in range(1, 26))

FROZEN_HASHES = {
    "docs/superpowers/plans/2026-08-31-governance-implementation-prep.md":
        "28b936359d49f5c8618d2dff63740497a766da43931fa4f47b7ad6dd9c232ecd",
    "design/drafts/source-governance.md":
        "0bc61207215f35065652bb66f043ef2d11a807bbe0bc44465814e469b5671526",
    "design/drafts/terminology-governance.md":
        "2d48c869b8a2119346739303accaaff0cbe40418d7074f29a4a18599950767d7",
}
FROZEN_INVENTORY_HASHES = {
    "source-entities.tsv":
        "843d3606407264e8d6ccca9ae8b9f03590aa403f98101c4a53a780bab5dc37f4",
    "source-entities.md":
        "10b76c321c28d611c33e1f1a41e27cb61005cfd7f5c226b74854119e749d9f06",
    "source-roles.tsv":
        "f291027de735d21aa21fd953a7301db9d7fcc34a6ec9d266e12ceab07e030cb9",
    "source-roles.md":
        "82fe12c4685ce2cd50900110a74234b3c1a3ad37a85eb4f6d1d6393ae6fc7601",
    "basis-inventory.tsv":
        "3da438227ee676f0d2c5e31ac16c73a3bb4a5d10716b15f175fd81257642c43c",
    "basis-inventory.md":
        "ed8c041a2b180a7a94fd73d68e2e847c175f2b5cb91af4aaf9e788fcd7ef8efb",
    "source-inventory.tsv":
        "0cb9b6df2f218629eb0dedb05ac5c83030b89e4d8dbca7580a8ccfee4b323c1f",
    "source-inventory.md":
        "57e5266910356d811a906a0b4b8cec7110ec05dcf8e9ebf650bed090461bd310",
    "match-inventory.tsv":
        "3f9701f6c2ef64a5d3c5a18144fc052f91e80d11384bb4023c85c74381d5d988",
    "match-inventory.md":
        "0d634286ffa5e4b6885b21b8ad9d68c39a33723fd8be6a4d55385f629d19b1ce",
    "origin-inventory.tsv":
        "06d0df76aa5ac7bd63cfe107ac52a5e712223f251e362b3bb9a0f4d95cbd1e3d",
    "origin-inventory.md":
        "5407ac17ed5f61a08bf4b957f4dc4d9ef5fb135a789e1e73444fb577a69a604a",
    "generation-baseline.md":
        "70388f7a105e69de2397a030d2d1dfb41d6e8ef6a59a43f502fd69126b97ed2e",
    "maintenance-baseline.md":
        "494bb0e3d85700cc1860537eea8bb2e8c376619041b1277958a1544351f3383b",
    "quality-debt.md":
        "9a0bcbf0aca72283761c97750b2afbaa598fd97277e11373f151e3a18a5e2660",
}

Q_FIELD_OWNERSHIP = {
    "Q01": frozenset(("paths",)),
    "Q02": frozenset(("schema_versions", "compatibility")),
    "Q03": frozenset(("proposed_id", "id_policy")),
    "Q04": frozenset(("identity_policy", "identity_class")),
    "Q05": frozenset(("focus_policy", "identity_resolution", "operation", "disposition", "new_value", "blocks_cutover")),
    "Q06": frozenset(("url_policy", "new_value.urls")),
    "Q07": frozenset(("review_policy", "new_value.review")),
    "Q08": frozenset(("watch_policy", "new_value.watch")),
    "Q09": frozenset(("new_value.unavailability_policy", "release_block_policy")),
    "Q10": frozenset(("status_policy", "new_value.status", "new_value.replaced_by", "operation", "disposition", "blocks_cutover")),
    "Q11": frozenset(("role_policy", "new_role", "new_status", "decision", "operation", "disposition", "blocks_cutover")),
    "Q12": frozenset(("candidate_role_policy", "new_role", "new_status", "decision", "operation", "disposition", "blocks_cutover")),
    "Q13": frozenset(("source_policy", "operation", "disposition", "new_value", "blocks_cutover")),
    "Q14": frozenset(("multi_source_policy", "operation", "disposition", "new_value", "blocks_cutover")),
    "Q15": frozenset(("external_group_policy", "operation", "disposition", "new_value", "blocks_cutover")),
    "Q16": frozenset(("local_analysis_policy", "operation", "disposition", "new_value", "blocks_cutover")),
    "Q17": frozenset(("rfc_policy", "operation", "disposition", "new_value", "blocks_cutover")),
    "Q18": frozenset(("match_policy", "operation", "disposition", "new_value", "blocks_cutover")),
    "Q19": frozenset(("basis_policy", "operation", "disposition", "new_value", "blocks_cutover")),
    "Q20": frozenset(("unsupported_basis_policy", "operation", "disposition", "new_value", "blocks_cutover")),
    "Q21": frozenset(("origin_policy", "operation", "disposition", "new_value", "blocks_cutover")),
    "Q22": frozenset(("source_term_bridge",)),
    "Q23": frozenset(("tier_policy", "tier_change")),
    "Q24": frozenset(("term_admissions",)),
    "Q25": frozenset(("cutover_sequence", "rollback_sequence", "release_sequence")),
}
Q_CONTROL_IDENTITIES = {
    "Q01": frozenset(("@control:paths",)),
    "Q02": frozenset(("@control:schema",)),
    "Q03": frozenset(("@control:ids",)),
    "Q04": frozenset(("@control:identity-boundaries",)),
    "Q05": frozenset(("@control:focus-identities",)),
    "Q06": frozenset(("@control:addresses",)),
    "Q07": frozenset(("@control:review",)),
    "Q08": frozenset(("@control:watch",)),
    "Q09": frozenset(("@control:unavailability",)),
    "Q10": frozenset(("@control:external-status",)),
    "Q11": frozenset(("@control:roles",)),
    "Q12": frozenset(("@control:candidate-roles",)),
    "Q13": frozenset(("@control:source",)),
    "Q14": frozenset(("@control:multi-source",)),
    "Q15": frozenset(("@control:external-groups",)),
    "Q16": frozenset(("@control:local-analysis",)),
    "Q17": frozenset(("@control:rfc-source",)),
    "Q18": frozenset(("@control:match",)),
    "Q19": frozenset(("@control:basis",)),
    "Q20": frozenset(("@control:unsupported-basis",)),
    "Q21": frozenset(("@control:origin",)),
    "Q22": frozenset(("@control:obligation-bridge",)),
    "Q23": frozenset(("@control:tier",)),
    "Q24": frozenset(("@control:term-admission",)),
    "Q25": frozenset(("@control:cutover",)),
}
ROW_DOMAINS = {
    "entities": frozenset(("Q03", "Q04", "Q05", "Q06", "Q07", "Q08", "Q09", "Q10", "Q23")),
    "uses": frozenset(("Q03", "Q11", "Q12")),
    "basis": frozenset(("Q19", "Q20")),
    "source": frozenset(("Q13", "Q14", "Q15", "Q16", "Q17")),
    "match": frozenset(("Q17", "Q18")),
    "origin": frozenset(("Q21",)),
}


def sha256_path(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_frozen_hashes(root, inventory_dir):
    checked = []
    for relative, expected in FROZEN_HASHES.items():
        path = Path(root) / relative
        if not path.is_file() or sha256_path(path) != expected:
            raise ValueError(f"frozen hash mismatch: {relative}")
        checked.append(relative)
    for name, expected in FROZEN_INVENTORY_HASHES.items():
        path = Path(inventory_dir) / name
        if not path.is_file() or sha256_path(path) != expected:
            raise ValueError(f"frozen hash mismatch: {name}")
        checked.append(name)
    return tuple(sorted(checked))


def load_inventory_rows(inventory_dir, names=INVENTORIES):
    inventories = {}
    identities = set()
    for name in names:
        path = Path(inventory_dir) / name
        with path.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream, delimiter="\t")
            if tuple(reader.fieldnames or ()) != TSV_FIELDS:
                raise ValueError(f"invalid inventory header: {name}")
            rows = []
            for line_number, raw in enumerate(reader, start=2):
                if any(raw[field] == "" for field in TSV_FIELDS):
                    raise ValueError(f"empty inventory cell: {name}:{line_number}")
                if raw["状态"] not in VALID_INVENTORY_STATES:
                    raise ValueError(f"invalid inventory state: {name}:{line_number}")
                identity = f"{name}:{line_number}"
                if identity in identities:
                    raise ValueError(f"duplicate inventory identity: {identity}")
                identities.add(identity)
                row = dict(raw)
                row["identity"] = identity
                rows.append(row)
            inventories[LEDGER_NAMES[name]] = rows
    return inventories


def assert_inventory_counts(inventories):
    counts = {name: len(rows) for name, rows in inventories.items()}
    if counts != EXPECTED_COUNTS:
        raise ValueError(f"inventory count mismatch: {counts}")
    return counts


def _row_sha256(row):
    encoded = json.dumps(
        row, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_base_rows(inventories):
    base_rows = {}
    for ledger, rows in inventories.items():
        for raw in rows:
            identity = raw["identity"]
            if identity in base_rows:
                raise ValueError(f"duplicate inventory identity: {identity}")
            old_value = raw["当前值"]
            base_rows[identity] = {
                "identity": identity,
                "ledger": ledger,
                "class": raw["草案分类"],
                "old_file": raw["文件"],
                "old_record": raw["对象"],
                "field_path": raw["位置"],
                "old_value": old_value,
                "frozen_row_sha256": _row_sha256(raw),
                "decision_domains": sorted(ROW_DOMAINS[ledger]),
                "operation": "keep",
                "disposition": "retain_legacy",
                "new_value": deepcopy(old_value),
                "blocks_cutover": True,
                "decision_trace": [],
            }
    return base_rows


def decision_patch_sha256(patch):
    encoded = json.dumps(
        patch.value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def deep_set(target, field, value):
    parts = field.split(".")
    current = target
    for part in parts[:-1]:
        nested = current.setdefault(part, {})
        if not isinstance(nested, dict):
            raise ValueError(f"SOURCE_DECISION_PATCH_CONFLICT non-object field {field}")
        current = nested
    current[parts[-1]] = value


def validate_patch_ownership(final_rows, patch):
    ownership = Q_FIELD_OWNERSHIP.get(patch.qid)
    if ownership is None or patch.field not in ownership:
        raise ValueError(f"SOURCE_DECISION_PATCH_CONFLICT {patch.qid} {patch.field}")
    if patch.identity.startswith("@control:"):
        if patch.identity not in Q_CONTROL_IDENTITIES.get(patch.qid, frozenset()):
            raise ValueError(
                f"SOURCE_DECISION_PATCH_CONFLICT {patch.qid} {patch.identity}"
            )
        return
    row = final_rows.get(patch.identity)
    if row is None or patch.qid not in row["decision_domains"]:
        raise ValueError(
            f"SOURCE_DECISION_PATCH_CONFLICT {patch.qid} {patch.identity}"
        )


def _validate_final_rows(final_rows):
    for identity, row in final_rows.items():
        if row["identity"] != identity:
            raise ValueError(f"identity changed: {identity}")
        if row["operation"] not in {"keep", "set", "delete", "isolate"}:
            raise ValueError(f"invalid operation: {identity}")
        if not isinstance(row["blocks_cutover"], bool):
            raise ValueError(f"invalid blocker: {identity}")


def materialize_decision_patches(base_rows, patches):
    final_rows = {identity: deepcopy(row) for identity, row in base_rows.items()}
    controls = {}
    seen = set()
    for patch in sorted(patches, key=lambda row: (row.qid, row.identity, row.field)):
        key = (patch.identity, patch.field)
        if key in seen:
            raise ValueError(f"SOURCE_DECISION_PATCH_CONFLICT {key}")
        seen.add(key)
        validate_patch_ownership(final_rows, patch)
        if patch.identity.startswith("@control:"):
            target = controls.setdefault(patch.identity, {"decision_trace": []})
        else:
            target = final_rows[patch.identity]
        deep_set(target, patch.field, deepcopy(patch.value))
        target["decision_trace"].append({
            "qid": patch.qid,
            "field": patch.field,
            "value_sha256": decision_patch_sha256(patch),
        })
    _validate_final_rows(final_rows)
    return final_rows, controls


def validate_q_coverage(patches):
    actual = {patch.qid for patch in patches}
    if actual != REQUIRED_QIDS:
        missing = sorted(REQUIRED_QIDS - actual)
        unknown = sorted(actual - REQUIRED_QIDS)
        raise ValueError(
            f"SOURCE_DECISION_DELIVERY_MISSING missing={missing} unknown={unknown}"
        )


def validate_identity_coverage(base_rows, final_rows):
    if set(final_rows) != set(base_rows) or len(final_rows) != 3187:
        raise ValueError("migration identity coverage mismatch")


def summarize_ledgers(final_rows, controls, verified_hash_count, inventories):
    ledgers = {}
    for ledger in EXPECTED_COUNTS:
        rows = [deepcopy(row) for row in final_rows.values() if row["ledger"] == ledger]
        rows.sort(key=lambda row: int(row["identity"].rsplit(":", 1)[1]))
        ledgers[ledger] = {
            "schema": "urn:kb-design:data:source-migration",
            "schema_version": 1,
            "rows": rows,
        }
    entity_rows = inventories["entities"]
    source_classes = {
        name: 0 for name in ("实际派生", "来源名称", "项目 self", "含义不明")
    }
    for row in inventories["source"]:
        source_classes[row["草案分类"]] += 1
    return {
        "verified_hash_count": verified_hash_count,
        "counts": dict(EXPECTED_COUNTS),
        "entity_partitions": (
            sum(row["文件"] == "vocab/entities.yaml" for row in entity_rows),
            sum(row["文件"] != "vocab/entities.yaml" for row in entity_rows),
        ),
        "source_partitions": tuple(source_classes[name] for name in source_classes),
        "blocked_identity_ambiguities": sum(
            row["草案分类"] == "待人决定" for row in entity_rows
        ),
        "ledgers": ledgers,
        "controls": {key: controls[key] for key in sorted(controls)},
    }


def _write_plan(output_dir, plan):
    output_dir = Path(output_dir)
    if output_dir.exists():
        raise ValueError(f"output already exists: {output_dir}")
    output_dir.mkdir(parents=True)
    for name, ledger in plan["ledgers"].items():
        (output_dir / f"{name}.yaml").write_text(
            yaml.safe_dump(ledger, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
    combined_rows = [
        row
        for name in sorted(plan["ledgers"])
        for row in plan["ledgers"][name]["rows"]
    ]
    combined = {
        "schema": "urn:kb-design:data:source-migration-plan",
        "schema_version": 1,
        "summary": {
            "verified_hash_count": plan["verified_hash_count"],
            "counts": plan["counts"],
            "entity_partitions": list(plan["entity_partitions"]),
            "source_partitions": list(plan["source_partitions"]),
            "blocked_identity_ambiguities": plan["blocked_identity_ambiguities"],
        },
        "controls": plan["controls"],
        "rows": combined_rows,
        "file_rewrites": [],
    }
    (output_dir / "plan.yaml").write_text(
        yaml.safe_dump(combined, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )


def build_migration_plan(root, inventory_dir, decision_dir, output_dir=None):
    verified = verify_frozen_hashes(root, inventory_dir)
    inventories = load_inventory_rows(inventory_dir)
    assert_inventory_counts(inventories)
    base_rows = build_base_rows(inventories)
    patches = load_decision_patches(sorted(Path(decision_dir).glob("source-*.md")))
    final_rows, controls = materialize_decision_patches(base_rows, patches)
    validate_identity_coverage(base_rows, final_rows)
    validate_q_coverage(patches)
    plan = summarize_ledgers(final_rows, controls, len(verified), inventories)
    if output_dir is not None:
        _write_plan(output_dir, plan)
    return plan


def main():
    parser = argparse.ArgumentParser(description="Plan the frozen source migration")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--inventory-dir", type=Path, required=True)
    parser.add_argument("--decision-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = build_migration_plan(
        args.root, args.inventory_dir, args.decision_dir, args.output
    )
    print(json.dumps({
        "verified_hash_count": plan["verified_hash_count"],
        "counts": plan["counts"],
        "qids": sorted({
            trace["qid"]
            for control in plan["controls"].values()
            for trace in control["decision_trace"]
        }),
        "blocked": sum(
            row["blocks_cutover"]
            for ledger in plan["ledgers"].values()
            for row in ledger["rows"]
        ),
        "output": str(args.output),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
