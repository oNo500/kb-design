#!/usr/bin/env python3
import difflib
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED = (
    ".superpowers/sdd/2026-08-30-basic-unit-consumer-classification/agentic-plan.md:11: "
    "文件不存在 ../specs/2026-08-30-basic-unit-consumer-classification-design.md\n"
    ".superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/"
    "human-decision-package.md:340: 锚点不存在 ../../../../design/sources-registry.md#L68\n"
    "2 处问题\n"
)


def main() -> int:
    result = subprocess.run(
        [sys.executable, "scripts/check-links.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode == 1 and result.stdout == EXPECTED and not result.stderr:
        print("KNOWN_LINK_BASELINE_OK count=2")
        return 0
    sys.stdout.writelines(difflib.unified_diff(
        EXPECTED.splitlines(True),
        result.stdout.splitlines(True),
        fromfile="expected-link-baseline",
        tofile="actual-link-baseline",
    ))
    if result.stderr:
        sys.stderr.write(result.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
