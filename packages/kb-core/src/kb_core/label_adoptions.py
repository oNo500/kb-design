"""Apply authorized language-label records without changing concept semantics."""
from __future__ import annotations

import copy
import json
from pathlib import Path

try:
    from .label_basis import normalize_basis, validate_basis
except ImportError:
    from kb_core.label_basis import normalize_basis, validate_basis


# This implementation applies the specific missing-Chinese-label batch approved
# by the user. A later batch must declare its scope explicitly, not merely supply
# an arbitrary decision-looking string in data.
SUPPORTED_AUTHORIZATION = "design/decisions/structured-label-basis.md#批次授权"


def load_adoptions(root: Path) -> dict:
    path = root / "data/inputs/topics/label-adoptions.json"
    if not path.exists():
        return {}
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("records"), dict):
        raise ValueError("label adoptions must contain a records mapping")
    if document.get("authorization") != SUPPORTED_AUTHORIZATION:
        raise ValueError("unsupported label adoption authorization")
    for key, record in document["records"].items():
        parts = key.split("/")
        if len(parts) != 3 or parts[0] not in ("topics", "forms") or parts[2] != "zh":
            raise ValueError(f"target outside authorized Chinese-label batch: {key}")
        if not isinstance(record, dict):
            raise ValueError(f"invalid label adoption: {key}")
        if record.get("accept") is True:
            basis = record.get("basis")
            if (not isinstance(basis, dict) or basis.get("level") != 5 or not isinstance(basis.get("model"), dict)
                    or basis["model"].get("approval") != document["authorization"]):
                raise ValueError(f"label adoption authorization mismatch: {key}")
    return document["records"]


def apply_adoptions(records, collection: str, adoptions: dict, sources) -> None:
    index = {record["id"]: record for record in records}
    for key, decision in adoptions.items():
        if not key.startswith(collection + "/"):
            continue
        parts = key.split("/")
        if len(parts) != 3 or parts[2] not in ("zh", "en") or parts[1] not in index:
            raise ValueError(f"unknown label adoption target: {key}")
        if decision.get("accept") is not True:
            continue
        record = index[parts[1]]
        language = parts[2]
        original = decision.get("original", {})
        if original.get("en") != record["label"].get("en") or original.get("scope") != record.get("scope"):
            raise ValueError(f"stale original name or scope: {key}")
        label = decision.get("label")
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"empty adopted label: {key}")
        if record["label"].get(language) and record["label"][language] != label:
            raise ValueError(f"adoption would replace an existing label: {key}")
        if (record["label"].get(language)
                and normalize_basis(record["basis"].get(language), record, language) != decision.get("basis")):
            raise ValueError(f"adoption would replace an existing label basis: {key}")
        candidate = copy.deepcopy(record)
        candidate["label"][language] = label
        candidate["basis"][language] = copy.deepcopy(decision.get("basis"))
        errors = validate_basis(candidate["basis"][language], label, candidate, language,
                                sources, adoptions, collection=collection)
        if errors:
            raise ValueError(f"{key}: {'; '.join(errors)}")
        record["label"][language] = label
        record["basis"][language] = candidate["basis"][language]

    for record in records:
        for language, value in list(record.get("basis", {}).items()):
            if language not in ("zh", "en"):
                continue
            value = normalize_basis(value, record, language)
            errors = validate_basis(value, record["label"].get(language), record,
                                    language, sources, adoptions, collection=collection)
            if errors:
                raise ValueError(f"{collection}/{record['id']}/{language}: {'; '.join(errors)}")
            record["basis"][language] = value
