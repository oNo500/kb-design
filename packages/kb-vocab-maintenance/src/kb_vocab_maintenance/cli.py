"""Public commands for independent vocabulary maintenance artifacts."""
import argparse
import json
from pathlib import Path
import sys

from .diff import compare_files
from .edit import EditConflict, apply_edit, prepare_edit


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="kb-vocab-maintenance", description="Compare and prepare independent RDF vocabulary artifacts; does not publish or update consumers.")
    commands = parser.add_subparsers(dest="command", required=True)
    diff = commands.add_parser("diff", help="Compare all RDF properties, ignoring serialization and blank-node names")
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)
    edit = commands.add_parser("edit", help="Review or apply descriptive-property replacements")
    actions = edit.add_subparsers(dest="action", required=True)
    prepare = actions.add_parser("prepare", help="Create a pinned plan containing before/after values and XL projections")
    prepare.add_argument("--input", type=Path, required=True)
    prepare.add_argument("--changes", type=Path, required=True, help="JSON list of subject/predicate/after property replacements; values use full N3")
    prepare.add_argument("--plan", type=Path, required=True)
    prepare.add_argument("--reason", required=True)
    prepare.add_argument("--authorization", required=True, help="Reference to the applicable authorization; validity requires human review")
    apply = actions.add_parser("apply", help="Check the baseline and conflicts, then write a new artifact directory")
    apply.add_argument("--plan", type=Path, required=True)
    apply.add_argument("--input", type=Path, required=True, help="Current RDF; unrelated upstream changes are retained")
    apply.add_argument("--output", type=Path, required=True)
    entities = commands.add_parser("import-entities", help="Freeze and convert legacy entity records without changing their status")
    entities.add_argument("--source", type=Path, required=True)
    entities.add_argument("--registry", type=Path, required=True)
    entities.add_argument("--output", type=Path, required=True)
    build = commands.add_parser("build-entities", help="Build one entity vocabulary from pinned source deliveries")
    build.add_argument("--config", type=Path, required=True)
    build.add_argument("--source-root", type=Path, required=True)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--current", type=Path, help="Explicitly create or replace only a current symlink after full delivery validation")
    args = parser.parse_args(argv)
    try:
        if args.command == "diff":
            result = compare_files(args.before, args.after)
        elif args.command == "import-entities":
            from .legacy import import_entities
            result = import_entities(args.source, args.registry, args.output)
        elif args.command == "build-entities":
            from .entities import build_entities, set_current
            result = build_entities(args.config, args.source_root, args.output)
            if args.current is not None:
                set_current(args.output, args.current)
        elif args.action == "prepare":
            operations = json.loads(args.changes.read_bytes())
            if args.plan.resolve() == args.changes.resolve():
                raise ValueError("The plan must not overwrite the change request")
            result = prepare_edit(args.input, operations, args.plan, reason=args.reason, authorization=args.authorization)
        else:
            result = apply_edit(args.plan, args.input, args.output)
    except EditConflict as exc:
        print(json.dumps({"error": str(exc), "conflicts": exc.conflicts}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    except (ValueError, OSError, SyntaxError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
