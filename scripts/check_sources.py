#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.source_model import validate_repository


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--allow-legacy", action="store_true")
    args = parser.parse_args(argv)
    issues = validate_repository(args.root, args.previous, args.allow_legacy)
    if not issues:
        print("0 source governance issues")
        return 0
    for issue in issues:
        print(f"{issue.code}\t{issue.file}\t{issue.record}\t{issue.field_path}\t{issue.message}")
    print(f"{len(issues)} source governance issues")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
