#!/usr/bin/env python3
import argparse
import csv
import hashlib
import io
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, NamedTuple, Sequence, Tuple


INVENTORY_FIELDS = (
    "对象",
    "语言",
    "文件",
    "位置",
    "当前形式或值",
    "概念身份",
    "依据状态",
    "消费者或所有者",
    "拟议去向",
    "决策级别",
    "状态",
)
INHERITED_FIELDS = (
    "legacy_identity",
    "disposition",
    "decision_evidence",
)
LEDGER_FIELDS = (
    "legacy_identity",
    *INVENTORY_FIELDS,
    "original_line",
    "section",
    "review_line",
    "current_action",
    "processing_stage",
    "disposition",
    "decision_evidence",
    "blocks_cutover",
)
ACTION_DISPOSITIONS = {
    "defer": "audit-only",
    "keep": "retain-owner",
    "remove": "retain-pending-l3",
}
DECISION_EVIDENCE = "locked-review-inheritance"
EXPECTED_IDENTITIES = 348

LOCATION_PATTERN = re.compile(
    r"第 ([1-9][0-9]*) 行；小节=([^；\r\n]+)；后草案审查表第 ([1-9][0-9]*) 行"
)


class Location(NamedTuple):
    line: int
    section: str
    review_line: int


@dataclass(frozen=True)
class InventoryRow:
    raw: Mapping[str, str]
    original_line: int
    section: str
    review_line: int
    current_action: str
    processing_stage: str
    legacy_identity: str


@dataclass(frozen=True)
class InheritedDisposition:
    legacy_identity: str
    disposition: str
    decision_evidence: str = DECISION_EVIDENCE


def parse_location(value: str) -> Location:
    match = LOCATION_PATTERN.fullmatch(value)
    if match is None:
        raise ValueError(f"TERM_INVENTORY_LOCATION {value}")
    return Location(int(match.group(1)), match.group(2), int(match.group(3)))


def _parse_exact_fragment(value: str, field: str, error_code: str) -> str:
    matches = re.findall(rf"(?:^|；){re.escape(field)}=([^；\r\n]+)", value)
    if len(matches) != 1:
        raise ValueError(f"{error_code} {value}")
    return matches[0]


def parse_exact_action(value: str) -> str:
    action = _parse_exact_fragment(value, "当前动作", "TERM_INVENTORY_ACTION")
    if action not in ACTION_DISPOSITIONS:
        raise ValueError(f"TERM_INVENTORY_ACTION {value}")
    return action


def parse_processing_stage(value: str) -> str:
    return _parse_exact_fragment(value, "处理阶段", "TERM_INVENTORY_STAGE")


def legacy_identity(row: InventoryRow) -> str:
    parts = (
        row.raw["文件"],
        str(row.original_line),
        row.section,
        row.raw["语言"],
        row.raw["当前形式或值"],
    )
    return hashlib.sha256("\0".join(parts).encode("utf-8")).hexdigest()


def parse_inventory(path: Path) -> Sequence[InventoryRow]:
    rows = []
    with Path(path).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if tuple(reader.fieldnames or ()) != INVENTORY_FIELDS:
            raise ValueError("TERM_INVENTORY_HEADER")
        for line_number, raw in enumerate(reader, start=2):
            if None in raw or any(raw[field] == "" for field in INVENTORY_FIELDS):
                raise ValueError(f"TERM_INVENTORY_CELL {line_number}")
            location = parse_location(raw["位置"])
            row = InventoryRow(
                raw=dict(raw),
                original_line=location.line,
                section=location.section,
                review_line=location.review_line,
                current_action=parse_exact_action(raw["拟议去向"]),
                processing_stage=parse_processing_stage(raw["拟议去向"]),
                legacy_identity="",
            )
            rows.append(
                InventoryRow(
                    raw=row.raw,
                    original_line=row.original_line,
                    section=row.section,
                    review_line=row.review_line,
                    current_action=row.current_action,
                    processing_stage=row.processing_stage,
                    legacy_identity=legacy_identity(row),
                )
            )

    identities = {row.legacy_identity for row in rows}
    review_lines = {row.review_line for row in rows}
    if (
        len(rows) != EXPECTED_IDENTITIES
        or len(identities) != EXPECTED_IDENTITIES
        or review_lines != set(range(2, EXPECTED_IDENTITIES + 2))
    ):
        raise ValueError("TERM_INVENTORY_IDENTITY_COUNT")
    return tuple(rows)


def inherited_decision(row: InventoryRow) -> InheritedDisposition:
    return InheritedDisposition(
        legacy_identity=row.legacy_identity,
        disposition=ACTION_DISPOSITIONS[row.current_action],
    )


def _render_rows(fieldnames: Tuple[str, ...], rows: Sequence[Mapping[str, object]]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def render_inherited_decisions(inventory: Path) -> bytes:
    rows = []
    for item in parse_inventory(inventory):
        decision = inherited_decision(item)
        rows.append(
            {
                "legacy_identity": decision.legacy_identity,
                "disposition": decision.disposition,
                "decision_evidence": decision.decision_evidence,
            }
        )
    return _render_rows(INHERITED_FIELDS, rows)


def render_migration_ledger(inventory: Path) -> bytes:
    rows = []
    for item in parse_inventory(inventory):
        decision = inherited_decision(item)
        row = {
            "legacy_identity": item.legacy_identity,
            **item.raw,
            "original_line": item.original_line,
            "section": item.section,
            "review_line": item.review_line,
            "current_action": item.current_action,
            "processing_stage": item.processing_stage,
            "disposition": decision.disposition,
            "decision_evidence": decision.decision_evidence,
            "blocks_cutover": "false",
        }
        rows.append(row)
    return _render_rows(LEDGER_FIELDS, rows)


def _atomic_write(path: Path, value: bytes) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(value)
    temporary.replace(path)


def materialize(inventory: Path, output: Path, inherited_output: Path = None) -> None:
    _atomic_write(output, render_migration_ledger(inventory))
    if inherited_output is not None:
        _atomic_write(inherited_output, render_inherited_decisions(inventory))


def validate(inventory: Path, ledger: Path) -> None:
    if Path(ledger).read_bytes() != render_migration_ledger(inventory):
        raise ValueError("TERM_LEDGER_DRIFT")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    materialize_parser = subparsers.add_parser("materialize")
    materialize_parser.add_argument("--inventory", type=Path, required=True)
    materialize_parser.add_argument("--output", type=Path, required=True)
    materialize_parser.add_argument("--inherited-output", type=Path)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--inventory", type=Path, required=True)
    validate_parser.add_argument("--ledger", type=Path, required=True)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "materialize":
            materialize(args.inventory, args.output, args.inherited_output)
        else:
            validate(args.inventory, args.ledger)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
