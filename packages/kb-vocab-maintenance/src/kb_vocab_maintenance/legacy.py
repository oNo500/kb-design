"""Loss-aware RDF delivery of existing entity records, without new adoption.

The registry assigns UUIDv4 identities once. Its language slots identify the
existing preferred-name records independently of their editable text. Source
fields without an adopted RDF projection remain addressable in the original
snapshot and in the unprojected-field report.
"""
from copy import deepcopy
import fcntl
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import tempfile
from uuid import UUID, uuid4

from jsonschema import Draft202012Validator, FormatChecker
from kb_core.source_model import build_schema_documents
from rdflib import DCTERMS, Graph, Literal, Namespace, RDF, RDFS, SKOS, URIRef
from rdflib.compare import isomorphic
import yaml


XL = Namespace("http://www.w3.org/2008/05/skos-xl#")
PROV = Namespace("http://www.w3.org/ns/prov#")
KIND_CLASSES = {
    "software": "http://www.wikidata.org/entity/Q7397",
    "organization": "http://www.wikidata.org/entity/Q43229",
    "programming-language": "http://www.wikidata.org/entity/Q9143",
}
CATALOG = "urn:kb-design:data:entities"
LANGUAGE = re.compile(r"[A-Za-z]+(?:-[A-Za-z0-9]+)*")
REASONS = {
    "subjects": "Legacy topic IDs have no adopted correspondence to the RDF concept vocabulary.",
    "match": "Legacy concept-style matches are retained without asserting entity identity.",
    "vendor": "No entity vendor relationship is adopted for this conversion.",
    "basis": "Original evidence and its field applicability remain in the source record.",
    "history": "Original decisions, prior values and event history remain in the source record.",
    "urls": "URL targets use rdfs:seeAlso; original roles and primary flags remain here.",
    "alt": "Alternate-name arrays lack stable expression identifiers; no continuity is inferred.",
    "status": "Project adoption state is preserved in manifest.source_states, not as an RDF type.",
}


class _UniqueKeysLoader(yaml.SafeLoader):
    """Do not let YAML duplicate keys silently discard source facts."""


def _unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError("Source mapping keys must be unique strings")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueKeysLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


def _json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def _read_source(raw):
    try:
        document = yaml.load(raw, Loader=_UniqueKeysLoader)
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid entity YAML: {error}") from error
    validator = Draft202012Validator(
        build_schema_documents()["source-entities.schema.json"],
        format_checker=FormatChecker(),
    )
    error = next(validator.iter_errors(document), None)
    if error is not None:
        raise ValueError(f"Invalid entity source at {error.json_path}: {error.message}")
    # The existing schema deliberately has open history/version objects. They
    # must still be JSON data to be copied without implicit string conversion.
    try:
        _json_bytes(document)
    except (TypeError, ValueError) as error:
        raise ValueError("Source contains values that cannot be preserved as JSON") from error
    seen = set()
    for row in document["entities"]:
        if row["id"] in seen:
            raise ValueError(f"Duplicate original entity ID: {row['id']}")
        seen.add(row["id"])
        if row["kind"] not in KIND_CLASSES:
            raise ValueError(f"No adopted class projection for entity kind: {row['kind']}")
        languages = set()
        for language, text in row["label"].items():
            if not LANGUAGE.fullmatch(language) or not text.strip():
                raise ValueError(f"Invalid preferred name for {row['id']}: {language}")
            if language.lower() in languages:
                raise ValueError(f"Duplicate case-insensitive name language for {row['id']}")
            languages.add(language.lower())
    return document


def _valid_uuid_iri(value):
    if not isinstance(value, str) or not value.startswith("urn:uuid:"):
        return False
    try:
        parsed = UUID(value.removeprefix("urn:uuid:"))
    except ValueError:
        return False
    return parsed.version == 4 and value == "urn:uuid:" + str(parsed)


def _unique_json_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Identity registry contains duplicate JSON keys")
        result[key] = value
    return result


def _read_registry(raw):
    if raw is None:
        return {"schema_version": 1, "source_catalog": CATALOG, "entities": {}}
    try:
        registry = json.loads(raw, object_pairs_hook=_unique_json_pairs)
    except (ValueError, UnicodeDecodeError) as error:
        raise ValueError("Invalid entity identity registry JSON") from error
    if (not isinstance(registry, dict)
            or set(registry) != {"schema_version", "source_catalog", "entities"}
            or registry["schema_version"] != 1
            or registry["source_catalog"] != CATALOG
            or not isinstance(registry["entities"], dict)):
        raise ValueError("Invalid entity identity registry structure or source catalog")
    identities = set()
    for original_id, row in registry["entities"].items():
        if (not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", original_id)
                or not isinstance(row, dict) or set(row) != {"entity_iri", "labels"}
                or not isinstance(row["labels"], dict) or not row["labels"]):
            raise ValueError(f"Invalid identity registration for {original_id}")
        for language in row["labels"]:
            if not LANGUAGE.fullmatch(language):
                raise ValueError(f"Invalid registered language for {original_id}")
        for iri in [row["entity_iri"], *row["labels"].values()]:
            if not _valid_uuid_iri(iri) or iri in identities:
                raise ValueError("Identity registry contains invalid or shared UUIDv4 identities")
            identities.add(iri)
    return registry


def _allocate(document, registry):
    result = deepcopy(registry)
    rows = result["entities"]
    missing = set(rows) - {row["id"] for row in document["entities"]}
    if missing:
        raise ValueError("Registered entities disappeared; explicit handling is required: " + ", ".join(sorted(missing)))
    for source in document["entities"]:
        if source["id"] not in rows:
            rows[source["id"]] = {"entity_iri": "urn:uuid:" + str(uuid4()), "labels": {}}
        row = rows[source["id"]]
        if set(row["labels"]) - set(source["label"]):
            raise ValueError(f"Registered name languages disappeared for {source['id']}")
        for language in source["label"]:
            if language not in row["labels"]:
                row["labels"][language] = "urn:uuid:" + str(uuid4())
    # Check collisions across newly assigned and previously registered names.
    _read_registry(_json_bytes(result))
    return result


def _build(document, raw, registry, registry_raw):
    digest = sha256(raw).hexdigest()
    source_iri = URIRef("urn:sha256:" + digest)
    graph = Graph()
    graph.add((source_iri, RDF.type, PROV.Entity))
    graph.add((source_iri, DCTERMS.isPartOf, URIRef(CATALOG)))
    source_states, reports = {}, []
    for index, row in enumerate(document["entities"]):
        identity = registry["entities"][row["id"]]
        entity = URIRef(identity["entity_iri"])
        pointer = f"/entities/{index}"
        graph.add((entity, RDF.type, URIRef(KIND_CLASSES[row["kind"]])))
        graph.add((entity, DCTERMS.identifier, Literal(row["id"])))
        graph.add((entity, PROV.wasDerivedFrom, source_iri))
        for language, text in row["label"].items():
            name = URIRef(identity["labels"][language])
            literal = Literal(text, lang=language)
            graph.add((entity, SKOS.prefLabel, literal))
            graph.add((entity, XL.prefLabel, name))
            graph.add((name, RDF.type, XL.Label))
            graph.add((name, XL.literalForm, literal))
            graph.add((name, PROV.wasDerivedFrom, source_iri))
        if "scope" in row:
            # The legacy scalar has no language tag; do not infer one.
            graph.add((entity, SKOS.scopeNote, Literal(row["scope"])))
        for url in row.get("urls", []):
            graph.add((entity, RDFS.seeAlso, URIRef(url["url"])))
        source_states[str(entity)] = {
            "status": row["status"], "original_id": row["id"],
            "original_kind": row["kind"], "source_catalog": CATALOG,
            "source_pointer": pointer,
            "record_sha256": sha256(_json_bytes(row)).hexdigest(),
        }
        fields = []
        for field in sorted(set(row) - {"id", "kind", "label", "scope"}):
            fields.append({"field": field, "pointer": pointer + "/" + field,
                           "value": row[field], "reason": REASONS.get(field,
                               "No RDF property projection is adopted for this legacy field.")})
        reports.append({"original_id": row["id"], "entity_iri": str(entity),
                        "source_pointer": pointer, "fields": fields})
    # Sorted N-Triples are also valid Turtle. RDFLib owns escaping and lexical
    # serialization; sorting removes graph iteration order from delivered bytes.
    turtle = b"\n".join(sorted(graph.serialize(format="nt", encoding="utf-8").splitlines())) + b"\n"
    if not isomorphic(graph, Graph().parse(data=turtle, format="turtle")):
        raise ValueError("RDF serialization changed the imported graph")
    files = {
        "entities.ttl": turtle, "source/entities.yaml": raw, "identity.json": registry_raw,
        "unprojected.json": _json_bytes({"schema_version": 1, "source_sha256": digest,
                                        "records": reports}),
    }
    manifest = {
        "schema_version": 1, "operation": "legacy-entities-import", "formal_release": False,
        "source": {"catalog": CATALOG, "sha256": digest, "snapshot": "source/entities.yaml",
                   "version": document["version"], "schema_version": document["schema_version"]},
        "identity_registry_sha256": sha256(registry_raw).hexdigest(),
        "entity_iris": sorted(source_states),
        "entity_class_iris": sorted({KIND_CLASSES[row["kind"]] for row in document["entities"]}),
        "source_states": source_states,
        "files": {name: sha256(content).hexdigest() for name, content in files.items()},
    }
    for status in ("active", "candidate", "deprecated"):
        manifest[status + "_entity_iris"] = sorted(iri for iri, row in source_states.items() if row["status"] == status)
    files["manifest.json"] = _json_bytes(manifest)
    return manifest, files


def _verify_existing(output, files):
    if output.is_symlink() or not output.is_dir():
        raise ValueError("Existing output is not an import directory")
    paths = list(output.rglob("*"))
    if any(path.is_symlink() for path in paths):
        raise ValueError("Existing output contains symbolic links")
    if {path.relative_to(output).as_posix() for path in paths if path.is_file()} != set(files):
        raise ValueError("Existing output has a different file set")
    for name, expected in files.items():
        if (output / name).read_bytes() != expected:
            raise ValueError(f"Existing output differs from the source, registry or complete delivery: {name}")


def _write_path(path):
    absolute = Path(path).absolute()
    if any(part.is_symlink() for part in (absolute, *absolute.parents)):
        raise ValueError(f"Import write paths cannot contain symbolic links: {path}")
    return absolute.resolve()


def _import_locked(source, registry, output):
    raw = source.read_bytes()
    document = _read_source(raw)
    old_registry = registry.read_bytes() if registry.exists() else None
    original = _read_registry(old_registry)
    identities = _allocate(document, original)
    identity_raw = old_registry if identities == original and old_registry is not None else _json_bytes(identities)
    manifest, files = _build(document, raw, identities, identity_raw)
    if output.exists() or output.is_symlink():
        _verify_existing(output, files)
        return manifest
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".entity-import-", dir=output.parent) as temporary:
        stage = Path(temporary) / "result"
        stage.mkdir()
        for name, content in files.items():
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        if source.read_bytes() != raw or (registry.read_bytes() if registry.exists() else None) != old_registry:
            raise ValueError("Source or identity registry changed during import")
        _write_path(registry)
        _write_path(output)
        if output.exists() or output.is_symlink():
            raise ValueError("Output appeared during import")
        if identity_raw != old_registry:
            registry.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary_registry = tempfile.mkstemp(prefix=".entity-identity-", dir=registry.parent)
            try:
                with os.fdopen(descriptor, "wb") as stream:
                    stream.write(identity_raw)
                os.replace(temporary_registry, registry)
            finally:
                Path(temporary_registry).unlink(missing_ok=True)
        stage.rename(output)
    return manifest


def import_entities(source: Path, registry: Path, output: Path) -> dict:
    """Convert a validated snapshot to RDF and preserve persistent local IDs.

    Existing output may only be reused when every byte matches the current
    source and registry. New results are staged before publication. Once an
    identity registry is written it is retained even if final publication fails,
    so a retry cannot silently allocate replacement identities.

    A nonblocking exclusive lock on the registry's parent directory serializes
    imports using that directory without creating a mutable lock sidecar. The
    directory inode remains stable when the registry is atomically replaced.
    """
    source = Path(source).resolve()
    registry, output = _write_path(registry), _write_path(output)
    if source == registry or any(
        path == output or output in path.parents or path in output.parents
        for path in (source, registry)
    ):
        raise ValueError("Source and identity registry must be distinct and outside the output")
    registry.parent.mkdir(parents=True, exist_ok=True)
    _write_path(registry)
    descriptor = os.open(registry.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ValueError("Entity identity registry lock is held by another import") from error
        return _import_locked(source, registry, output)
    finally:
        os.close(descriptor)
