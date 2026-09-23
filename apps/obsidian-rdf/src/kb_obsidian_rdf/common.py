"""Small shared representations; RDF and YAML parsing remain library-owned."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


class ContractError(ValueError):
    """An input, identity, reference or managed-file contract failed."""


@dataclass(frozen=True)
class Delivery:
    """Public knowledge files and external engineering state are separate."""

    vault_files: dict[str, bytes]
    state_files: dict[str, bytes]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def read_json(path: Path) -> dict:
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict):
        raise ContractError(f"需要 JSON 对象：{path}")
    return value


def reference_path(kind: str, identity: dict) -> str:
    if set(identity) == {"iri"}:
        value = identity["iri"]
    elif set(identity) == {"catalog", "id"}:
        if any("\0" in identity[key] for key in ("catalog", "id")):
            raise ContractError("局部身份不能包含 NUL")
        value = identity["catalog"] + "\0" + identity["id"]
    else:
        raise ContractError("身份需要 iri 或 catalog 与 id")
    if kind not in {"concepts", "entities", "schemes", "collections", "types", "genres", "forms", "references", "labels", "notes"}:
        raise ContractError(f"未知参考对象类型：{kind}")
    return f"vocab/{kind}/{digest(value.encode('utf-8'))}.md"


def safe_relative(value: str) -> str:
    path = PurePosixPath(value)
    if (not value or path.is_absolute() or ".." in path.parts or "\\" in value
            or "\0" in value or path.as_posix() != value or value == "."):
        raise ContractError(f"不安全的相对路径：{value!r}")
    return value
