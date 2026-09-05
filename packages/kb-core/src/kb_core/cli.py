"""Expose the existing core commands from the installed workspace package."""

import argparse
import runpy
import sys


COMMANDS = {
    "build-topics": "build_topics",
    "check-topics": "check_topics",
    "check-terms": "check_terms",
    "check-sources": "check_sources",
    "build-source-index": "build_source_index",
    "plan-source-migration": "plan_source_migration",
    "probe-sources": "probe_sources",
    "source-model": "source_model",
    "build-terms": "governance.build_terms",
    "migrate-terms": "governance.migrate_terms",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Knowledge data maintenance commands")
    parser.add_argument("command", choices=COMMANDS)
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command in {"build-topics", "check-topics"}:
        # These existing scripts execute at module load; validate intent before
        # importing them so help or a typo cannot trigger a data write.
        command_parser = argparse.ArgumentParser(prog=f"kb-core {args.command}")
        if args.command == "check-topics":
            command_parser.add_argument("--record", action="store_true",
                                        help="append a maintenance snapshot")
        command_parser.parse_args(args.arguments)
    sys.argv = [f"kb-core {args.command}", *args.arguments]
    runpy.run_module(f"kb_core.{COMMANDS[args.command]}", run_name="__main__")


if __name__ == "__main__":
    main()
