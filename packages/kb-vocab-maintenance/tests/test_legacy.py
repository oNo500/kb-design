"""Legacy import protects identity, adoption state, and the source record."""
from copy import deepcopy
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from rdflib import Graph, Literal, Namespace, RDF, RDFS, SKOS, URIRef
import yaml

from kb_vocab_maintenance.legacy import import_entities


XL = Namespace("http://www.w3.org/2008/05/skos-xl#")
ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture
def source_document():
    source = yaml.safe_load((ROOT / "data/vocab/entities.yaml").read_text())
    # Real records include URL evidence, scoped meaning, old matches and history.
    source["entities"] = [deepcopy(row) for row in source["entities"]
                          if row["id"] in {"react", "obsidian"}]
    return source


def write_source(path, document):
    path.write_text(yaml.safe_dump(document, allow_unicode=True, sort_keys=False))
    return path


def by_id(manifest, original_id):
    return next(URIRef(iri) for iri, row in manifest["source_states"].items()
                if row["original_id"] == original_id)


def test_retries_and_label_edits_preserve_registered_identities(tmp_path, source_document):
    source = write_source(tmp_path / "entities.yaml", source_document)
    registry = tmp_path / "identity.json"
    output = tmp_path / "first"
    first = import_entities(source, registry, output)
    first_registry = registry.read_bytes()
    assert import_entities(source, registry, output) == first
    assert registry.read_bytes() == first_registry
    subject = by_id(first, "obsidian")
    graph = Graph().parse(output / "entities.ttl")
    name = next(label for label in graph.objects(subject, XL.prefLabel)
                if (label, XL.literalForm, Literal("Obsidian", lang="en")) in graph)

    obsidian = next(row for row in source_document["entities"] if row["id"] == "obsidian")
    obsidian["label"]["en"] = "Obsidian application"
    write_source(source, source_document)
    second = import_entities(source, registry, tmp_path / "second")
    changed = Graph().parse(tmp_path / "second/entities.ttl")
    assert by_id(second, "obsidian") == subject
    assert (subject, XL.prefLabel, name) in changed
    assert (name, XL.literalForm, Literal("Obsidian application", lang="en")) in changed
    assert registry.read_bytes() == first_registry


def test_identical_text_does_not_merge_objects_or_languages(tmp_path, source_document):
    for row in source_document["entities"]:
        row["label"] = {"en": "Same", "zh": "Same"}
    source = write_source(tmp_path / "entities.yaml", source_document)
    manifest = import_entities(source, tmp_path / "identity.json", tmp_path / "out")
    graph = Graph().parse(tmp_path / "out/entities.ttl")
    first, second = by_id(manifest, "react"), by_id(manifest, "obsidian")
    assert first != second
    first_names = set(graph.objects(first, XL.prefLabel))
    second_names = set(graph.objects(second, XL.prefLabel))
    assert first_names.isdisjoint(second_names)
    assert len(first_names) == len(second_names) == 2


def test_candidate_and_unprojected_facts_remain_explicit(tmp_path, source_document):
    source = write_source(tmp_path / "entities.yaml", source_document)
    original = source.read_bytes()
    output = tmp_path / "out"
    manifest = import_entities(source, tmp_path / "identity.json", output)
    subject = by_id(manifest, "obsidian")
    assert manifest["source_states"][str(subject)]["status"] == "candidate"
    assert str(subject) in manifest["candidate_entity_iris"]
    assert str(subject) not in manifest["active_entity_iris"]
    assert manifest["source_states"][str(by_id(manifest, "react"))]["status"] == "active"
    assert source.read_bytes() == original
    assert (output / "source/entities.yaml").read_bytes() == original
    graph = Graph().parse(output / "entities.ttl")
    assert (subject, RDF.type, URIRef("http://www.wikidata.org/entity/Q7397")) in graph
    assert (subject, RDFS.seeAlso, URIRef("https://obsidian.md/")) in graph
    scope = next(row["scope"] for row in source_document["entities"] if row["id"] == "obsidian")
    assert (subject, SKOS.scopeNote, Literal(scope)) in graph
    assert not list(graph.triples((None, SKOS.exactMatch, None)))
    assert not list(graph.triples((None, URIRef("http://www.w3.org/2002/07/owl#sameAs"), None)))
    report = json.loads((output / "unprojected.json").read_bytes())
    react = next(row for row in report["records"] if row["original_id"] == "react")
    fields = {row["field"]: row for row in react["fields"]}
    original_react = next(row for row in source_document["entities"] if row["id"] == "react")
    for field in ("basis", "history", "subjects", "match"):
        assert fields[field]["value"] == original_react[field]
        assert fields[field]["pointer"].endswith("/" + field)


def test_invalid_source_cannot_leave_output_or_allocate_ids(tmp_path, source_document):
    source_document["entities"][0]["label"]["en"] = ["not a string"]
    source = write_source(tmp_path / "entities.yaml", source_document)
    registry, output = tmp_path / "identity.json", tmp_path / "out"
    with pytest.raises(ValueError):
        import_entities(source, registry, output)
    assert not registry.exists()
    assert not output.exists()


def test_existing_output_drift_is_rejected_without_overwrite(tmp_path, source_document):
    source = write_source(tmp_path / "entities.yaml", source_document)
    registry, output = tmp_path / "identity.json", tmp_path / "out"
    import_entities(source, registry, output)
    identity = registry.read_bytes()
    (output / "entities.ttl").write_text("tampered\n")
    with pytest.raises(ValueError):
        import_entities(source, registry, output)
    assert (output / "entities.ttl").read_text() == "tampered\n"
    assert registry.read_bytes() == identity


def test_duplicate_registry_keys_cannot_silently_replace_identity(tmp_path, source_document):
    source = write_source(tmp_path / "entities.yaml", source_document)
    registry = tmp_path / "identity.json"
    import_entities(source, registry, tmp_path / "first")
    original = registry.read_text()
    # Standard JSON parsing would accept the later field and hide corruption.
    damaged = original.replace('"entity_iri":', '"entity_iri": "urn:uuid:8cc50a90-ecf5-4d2a-b535-63f60c5de885", "entity_iri":', 1)
    registry.write_text(damaged)
    with pytest.raises(ValueError):
        import_entities(source, registry, tmp_path / "second")
    assert not (tmp_path / "second").exists()
    assert registry.read_text() == damaged


def test_late_write_failure_never_publishes_partial_directory(tmp_path, source_document, monkeypatch):
    source = write_source(tmp_path / "entities.yaml", source_document)
    registry, output = tmp_path / "identity.json", tmp_path / "out"
    write = Path.write_bytes

    def disk_full(path, data):
        if path.name == "unprojected.json":
            raise OSError("simulated disk full")
        return write(path, data)

    monkeypatch.setattr(Path, "write_bytes", disk_full)
    with pytest.raises(OSError):
        import_entities(source, registry, output)
    assert not output.exists()
    assert not registry.exists()


def test_another_process_cannot_allocate_while_registry_directory_is_locked(tmp_path, source_document):
    source = write_source(tmp_path / "entities.yaml", source_document)
    registry, output = tmp_path / "identity.json", tmp_path / "out"
    descriptor = os.open(tmp_path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        script = """from pathlib import Path
import sys
from kb_vocab_maintenance.legacy import import_entities
try:
    import_entities(*(Path(value) for value in sys.argv[1:]))
except ValueError as error:
    print(error)
    sys.exit(23)
"""
        completed = subprocess.run([sys.executable, "-c", script, str(source), str(registry), str(output)],
                                   capture_output=True, text=True, timeout=15)
        assert completed.returncode == 23, completed.stderr
        assert "lock" in completed.stdout.lower()
        assert not registry.exists()
        assert not output.exists()
    finally:
        os.close(descriptor)
    import_entities(source, registry, output)


@pytest.mark.parametrize("destination", ["registry", "output"])
def test_symlink_ancestors_cannot_redirect_import_writes(tmp_path, source_document, destination):
    source = write_source(tmp_path / "entities.yaml", source_document)
    outside = tmp_path / "outside"
    outside.mkdir()
    alias = tmp_path / "alias"
    alias.symlink_to(outside, target_is_directory=True)
    registry = (alias if destination == "registry" else tmp_path) / "identity.json"
    output = (alias if destination == "output" else tmp_path) / "out"
    with pytest.raises(ValueError):
        import_entities(source, registry, output)
    assert not registry.exists()
    assert not output.exists()
    assert list(outside.iterdir()) == []


def test_publication_failure_retains_allocated_identities_for_retry(tmp_path, source_document, monkeypatch):
    source = write_source(tmp_path / "entities.yaml", source_document)
    registry, output = tmp_path / "identity.json", tmp_path / "out"
    rename = Path.rename

    def fail_publish(path, target):
        if target == output:
            raise OSError("simulated failed publication")
        return rename(path, target)

    with monkeypatch.context() as context:
        context.setattr(Path, "rename", fail_publish)
        with pytest.raises(OSError):
            import_entities(source, registry, output)
    assigned = registry.read_bytes()
    assert not output.exists()
    import_entities(source, registry, output)
    assert registry.read_bytes() == assigned
    assert (output / "identity.json").read_bytes() == assigned
