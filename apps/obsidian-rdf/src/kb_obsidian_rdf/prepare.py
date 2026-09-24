"""Pin existing deliveries and their evidence for an explicitly selected mode."""
from __future__ import annotations

import json
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


def _artifact(path: Path, name: str | None = None) -> dict:
    return {"name": name or path.name, "path": str(path),
            "sha256": digest(path.read_bytes()), "format": path.suffix.lstrip('.')}


def prepare(source_root: Path, output: Path, *, authority: Path,
            previous_vault: Path | None = None, state_root: Path | None = None,
            mode: str = 'preview', entities: Path | None = None) -> dict:
    """Create a pinned manifest without changing source status or release markers."""
    from .input import routing_states
    if mode not in ('preview', 'formal'):
        raise ContractError("输入 mode 必须为 preview 或 formal")
    if mode == 'formal' and entities is None:
        raise ContractError("正式输入必须显式提供统一实体交付目录")
    source_root = source_root.resolve(strict=True)
    authority = authority.resolve(strict=True)
    evidence = authority.read_bytes()
    if not evidence.strip():
        raise ContractError("授权记录为空")
    if output.exists() or output.is_symlink():
        raise ContractError(f"输入清单已存在，请使用新的文件名：{output}")
    permission = {
        "preview_reference": authority.as_uri(),
        "scope_reference": authority.as_uri(),
        "formal_reference": authority.as_uri() if mode == 'formal' else None,
        "evidence_sha256": digest(evidence),
    }
    if mode == 'formal':
        permission['formal_evidence_sha256'] = digest(evidence)
    selection = 'selectable_subjects' if mode == 'formal' else 'trial_subjects'
    sources = []
    for key, directory, filename, classes in _DELIVERIES:
        if key == 'ccs-entities' and entities is not None:
            continue
        base = source_root / "output/vocabulary" / directory
        path = base / filename
        raw = path.read_bytes()
        original_manifest = (base / "manifest.json").read_bytes()
        delivery_files = json.loads(original_manifest).get('files', {})
        expected = delivery_files.get(filename)
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
        item = {
            "key": key, "path": str(path), "format": "turtle",
            "sha256": digest(raw), "identity": key,
            "version": {"delivery": directory, "manifest_sha256": digest(original_manifest)},
            "scope": scope, selection: subjects,
            "authority": permission,
            "artifacts": [_artifact(base / 'manifest.json')],
        }
        if mode == 'formal' and key == 'ccs-concepts':
            routing = _artifact(base / 'plan.json')
            if routing['sha256'] != delivery_files.get('plan.json'):
                raise ContractError(f"CCS 交付分流原件摘要不符：{routing['path']}")
            states = routing_states(read_json(Path(routing['path'])), set(subjects))
            item['routing'] = routing
            item['artifacts'].append(routing)
            item['source_states'] = states
            item[selection] = [iri for iri in subjects if states.get(iri, {}).get('routing_action') != 'pending']
        sources.append(item)
    if entities is not None:
        from kb_vocab_maintenance.entities import KIND_CLASSES, validate_delivery
        # Resolve current once. Every later read uses this immutable version path.
        directory = entities.resolve(strict=True)
        try:
            entity_manifest = validate_delivery(directory)
        except (ValueError, OSError, KeyError, TypeError) as exc:
            raise ContractError(f'统一实体交付验证失败：{exc}') from exc
        if entity_manifest.get('policy') != 'basic-fields-v1':
            raise ContractError('统一实体交付缺少已准用的 basic-fields-v1 依据')
        raw = (directory/'entities.ttl').read_bytes()
        graph = Graph().parse(data=raw, format='turtle')
        classes = sorted(cls for cls in KIND_CLASSES.values() if any(graph.subjects(RDF.type, URIRef(cls))))
        manifest_hash = digest((directory/'manifest.json').read_bytes())
        sources.append({
            'key': 'entities', 'path': str(directory/'entities.ttl'), 'format': 'turtle',
            'sha256': digest(raw), 'identity': 'unified-entities',
            'version': {'delivery': str(directory), 'manifest_sha256': manifest_hash},
            'scope': {'entity_class_iris': classes},
            selection: entity_manifest['eligible_entity_iris'], 'authority': permission,
            'entity_delivery': {'directory': str(directory), 'manifest_sha256': manifest_hash},
            'artifacts': [_artifact(directory/name, name)
                          for name in sorted({*entity_manifest['files'], 'manifest.json'})],
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
            "authority": (permission if mode == 'formal' else
                          {**permission, "formal_reference": content_model.as_uri(),
                           "formal_evidence_sha256": digest(model_bytes)}),
            'artifacts': [_artifact(content_model)],
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
        "format_version": 1, "mode": mode, "sources": sources,
        "auxiliary": auxiliary, "display": {"languages": ["zh", "en"]},
        "rules": {"shacl_profiles": ["structure"]},
        "producer": {"name": "kb-obsidian-rdf", "version": __version__},
        "previous_delivery": previous,
    }
    payload = json_bytes(manifest)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        stream.write(payload)
    return {"input": str(output.resolve()), "sha256": digest(payload), "mode": mode,
            "resources": {item["key"]: len(item[selection]) for item in sources},
            "formal_use": "authorized" if mode == 'formal' else "unconfirmed"}
