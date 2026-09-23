"""Freeze this project's existing deliveries for the authorized development preview."""
from __future__ import annotations

from pathlib import Path

from rdflib import Graph, RDF, SKOS, URIRef
import yaml

from . import __version__
from .common import ContractError, digest, json_bytes, read_json


_DELIVERIES = (
    ("ccs-concepts", "ccs/partitioned-20260921-rdf", "concepts.ttl", {SKOS.Concept}),
    ("ccs-entities", "ccs/partitioned-20260921-rdf", "entities.ttl", {
        URIRef("http://www.wikidata.org/entity/" + key)
        for key in ("Q5", "Q43229", "Q7397", "Q9143")
    }),
    ("writing-concepts", "writing/expanded-20260922-final", "vocabulary.ttl", {SKOS.Concept}),
)


def prepare(source_root: Path, output: Path, *, authority: Path,
            previous_vault: Path | None = None, state_root: Path | None = None) -> dict:
    """Create a pinned manifest, never mutate or approve its input data."""
    source_root = source_root.resolve(strict=True)
    authority = authority.resolve(strict=True)
    evidence = authority.read_bytes()
    if not evidence.strip():
        raise ContractError("预览授权记录为空")
    if output.exists() or output.is_symlink():
        raise ContractError(f"输入清单已存在，请使用新的文件名：{output}")
    permission = {
        "preview_reference": authority.as_uri(),
        "scope_reference": authority.as_uri(),
        "formal_reference": None,
        "evidence_sha256": digest(evidence),
    }
    sources = []
    for key, directory, filename, classes in _DELIVERIES:
        base = source_root / "output/vocabulary" / directory
        path = base / filename
        raw = path.read_bytes()
        original_manifest = (base / "manifest.json").read_bytes()
        expected = read_json(base / "manifest.json").get("files", {}).get(filename)
        if expected != digest(raw):
            raise ContractError(f"源交付摘要不符，须先核对生成结果：{path}")
        graph = Graph().parse(data=raw, format="turtle")
        subjects = sorted({str(node) for cls in classes
                           for node in graph.subjects(RDF.type, cls)
                           if isinstance(node, URIRef)})
        if not subjects:
            raise ContractError(f"没有可辨认的范围主体：{path}")
        scope = ({"entity_class_iris": sorted(str(cls) for cls in classes
                                             if any(graph.subjects(RDF.type, cls)))}
                 if key == "ccs-entities" else {"subject_iris": subjects})
        sources.append({
            "key": key, "path": str(path), "format": "turtle",
            "sha256": digest(raw), "identity": key,
            "version": {"delivery": directory, "manifest_sha256": digest(original_manifest)},
            "scope": scope, "trial_subjects": subjects,
            "authority": permission,
        })
    auxiliary = []
    content_model = source_root / "docs/model/content/设计-内容模型.md"
    model_bytes = content_model.read_bytes()
    for kind in ("types", "genres", "forms", "references"):
        relative = ("data/references/bibliography.yaml" if kind == "references"
                    else f"data/vocab/{kind}.yaml")
        path = source_root / relative
        raw = path.read_bytes()
        value = yaml.safe_load(raw)
        if not isinstance(value, dict) or not isinstance(value.get(kind), list):
            raise ContractError(f"辅助值域结构不符：{path}")
        auxiliary.append({
            "key": kind, "kind": kind, "path": str(path), "format": "yaml",
            "schema_version": value.get("schema_version", "unknown"), "sha256": digest(raw),
            "version": value.get("version", "unknown"),
            "authority": {**permission, "formal_reference": content_model.as_uri(),
                          "formal_evidence_sha256": digest(model_bytes)},
        })
    previous = None
    if previous_vault is not None:
        from .storage import read_state, state_directory
        previous_vault = previous_vault.resolve(strict=True)
        installed = read_state(previous_vault, state_root=state_root)
        previous = {"path": str(previous_vault),
                    "state_root": str(state_directory(previous_vault, state_root=state_root).parent),
                    "sha256": installed["manifest_sha256"]}
    manifest = {
        "format_version": 1, "mode": "preview", "sources": sources,
        "auxiliary": auxiliary, "display": {"languages": ["zh", "en"]},
        "rules": {"shacl_profiles": ["structure"]},
        "producer": {"name": "kb-obsidian-rdf", "version": __version__},
        "previous_delivery": previous,
    }
    payload = json_bytes(manifest)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        stream.write(payload)
    return {"input": str(output.resolve()), "sha256": digest(payload), "mode": "preview",
            "resources": {item["key"]: len(item["trial_subjects"]) for item in sources},
            "formal_use": "unconfirmed"}
