"""Adapt the frozen kb-design Obsidian exporter without changing its output."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Mapping
from pathlib import Path

from .design_source import DesignSnapshot
from .errors import ApplicationError


def _require_empty_output(output: Path) -> Path:
    destination = Path(output)
    try:
        destination = destination.resolve(strict=True)
    except OSError as exc:
        raise ApplicationError(f"output directory does not exist: {output}") from exc
    if not destination.is_dir():
        raise ApplicationError(f"output path is not a directory: {destination}")
    try:
        if next(destination.iterdir(), None) is not None:
            raise ApplicationError(f"output directory is not empty: {destination}")
    except OSError as exc:
        raise ApplicationError(f"cannot inspect output directory: {destination}: {exc}") from exc
    return destination


def _read_manifest(output: Path) -> dict[str, object]:
    try:
        manifest_bytes = (output / "manifest.json").read_bytes()
        manifest = json.loads(manifest_bytes)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ApplicationError(f"cannot read reference export manifest: {exc}") from exc
    if not isinstance(manifest, dict):
        raise ApplicationError("reference export manifest is not a mapping")
    return manifest


def _verify_input_hashes(manifest: Mapping[str, object], snapshot: DesignSnapshot) -> None:
    inputs = manifest.get("inputs")
    if not isinstance(inputs, list):
        raise ApplicationError("reference export manifest has no input hashes")
    actual_hashes: dict[str, str] = {}
    for entry in inputs:
        if not isinstance(entry, Mapping):
            raise ApplicationError("reference export manifest has an invalid input hash")
        relative_path = entry.get("path")
        digest = entry.get("sha256")
        if not isinstance(relative_path, str) or not isinstance(digest, str):
            raise ApplicationError("reference export manifest has an invalid input hash")
        if relative_path in actual_hashes:
            raise ApplicationError("reference export manifest has duplicate input hashes")
        actual_hashes[relative_path] = digest
    if actual_hashes != dict(snapshot.input_hashes):
        raise ApplicationError("reference export input hash mismatch")


def export_reference(snapshot: DesignSnapshot, output: Path) -> Mapping[str, object]:
    """Run the upstream exporter and publish only its verified ``KB/`` tree."""
    destination = _require_empty_output(output)
    exporter = snapshot.root / "scripts" / "export_obsidian.py"
    if not exporter.is_file():
        raise ApplicationError(f"reference exporter does not exist: {exporter}")

    with tempfile.TemporaryDirectory(prefix="kb-obsidian-reference-") as temporary:
        upstream_output = Path(temporary) / "export"
        try:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(exporter),
                    "--repo-root",
                    str(snapshot.root),
                    "--output",
                    str(upstream_output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError as exc:
            raise ApplicationError(f"cannot run reference exporter: {exc}") from exc
        if completed.returncode:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise ApplicationError(f"reference export failed: {detail}")

        manifest = _read_manifest(upstream_output)
        _verify_input_hashes(manifest, snapshot)
        source_tree = upstream_output / "KB"
        if not source_tree.is_dir() or source_tree.is_symlink():
            raise ApplicationError("reference export does not contain a KB tree")
        try:
            shutil.copytree(source_tree, destination / "KB")
        except OSError as exc:
            shutil.rmtree(destination / "KB", ignore_errors=True)
            raise ApplicationError(f"cannot publish verified KB tree: {exc}") from exc

    result = dict(manifest)
    result["design_commit"] = snapshot.commit
    return result
