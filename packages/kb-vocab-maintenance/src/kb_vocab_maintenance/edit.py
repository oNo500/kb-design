"""Reviewed descriptive-property edits with pinned baselines and explicit conflicts.

This is an artifact-producing maintenance step, not semantic approval or release.
Relation, lifecycle and identity changes intentionally have no execution interface.
"""
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import tempfile

from jsonschema import Draft202012Validator
from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, SKOS, URIRef
from rdflib.namespace import DCTERMS

from .diff import canonical_bytes, compare_graphs, parse_turtle, read_graph

XL = Namespace("http://www.w3.org/2008/05/skos-xl#")
ROLES = {XL.prefLabel: SKOS.prefLabel, XL.altLabel: SKOS.altLabel, XL.hiddenLabel: SKOS.hiddenLabel}
DESCRIPTIVE = {DCTERMS.title, DCTERMS.description, DCTERMS.identifier, DCTERMS.source,
               DCTERMS.language, DCTERMS.created, DCTERMS.modified, RDFS.comment, RDFS.label,
               SKOS.notation, SKOS.definition, SKOS.scopeNote, SKOS.note, SKOS.editorialNote,
               SKOS.historyNote, SKOS.changeNote, XL.literalForm, *ROLES.values()}
NAME_RULES = ["XL named identity and single literalForm", "XL ordinary-label projection",
              "prefLabel uniqueness by complete language tag", "disjoint label-role literal values"]
VALUES = {"type": "array", "items": {"type": "string"}, "uniqueItems": True}
CHANGE = {"type": "object", "additionalProperties": False,
          "required": ["subject", "predicate", "before", "after", "derived"],
          "properties": {"subject": {"type": "string"}, "predicate": {"type": "string"},
                         "before": VALUES, "after": VALUES, "derived": {"type": "boolean"}}}
PLAN_SCHEMA = {"type": "object", "additionalProperties": False,
               "required": ["format_version", "baseline", "reason", "authorization", "changes", "dependencies"],
               "properties": {"format_version": {"const": 1}, "baseline": {"type": "object", "additionalProperties": False,
                    "required": ["path", "sha256", "graph_sha256"], "properties": {
                        "path": {"type": "string"}, "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                        "graph_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}}},
                    "reason": {"type": "string", "minLength": 1}, "authorization": {"type": "string", "minLength": 1},
                    "changes": {"type": "array", "minItems": 1, "items": CHANGE}, "dependencies": {"type": "array"}}}


class EditConflict(ValueError):
    def __init__(self, conflicts: list[dict]):
        self.conflicts = conflicts
        super().__init__("Current RDF conflicts with the reviewed edit plan")


def _json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _iri(value: str) -> URIRef:
    if not isinstance(value, str) or not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value) or any(
            c.isspace() or c in '<>"{}|^`\\' for c in value):
        raise ValueError("A stable absolute IRI is required")
    return URIRef(value)


def _term(value: str):
    if not isinstance(value, str) or not value.startswith(('"', '<')):
        raise ValueError("Values require full N3 IRIs or literals; blank nodes and prefixes are unsupported")
    try:
        graph = parse_turtle(f"<urn:edit:subject> <urn:edit:predicate> {value} .")
        if len(graph) != 1:
            raise ValueError("Expected one RDF term")
        result = graph.value(URIRef("urn:edit:subject"), URIRef("urn:edit:predicate"))
    except Exception as exc:
        raise ValueError(f"Invalid N3 value: {value}") from exc
    if not isinstance(result, (URIRef, Literal)):
        raise ValueError("Only stable IRIs and literal values can be edited")
    if isinstance(result, URIRef):
        _iri(str(result))
    # N3 round-tripping refuses trailing text and ambiguous shorthand instead of ignoring it.
    if result.n3() != value:
        raise ValueError(f"Use canonical N3 for the RDF value: {result.n3()}")
    return result


def _values(graph: Graph, subject: URIRef, predicate: URIRef) -> list[str]:
    values = set(graph.objects(subject, predicate))
    if any(isinstance(value, BNode) for value in values):
        raise ValueError("Blank-node property values require a separate reviewed operation")
    return sorted(value.n3() for value in values)


def _set(graph: Graph, subject: URIRef, predicate: URIRef, values: list[str]):
    graph.remove((subject, predicate, None))
    for value in values:
        graph.add((subject, predicate, _term(value)))


def _check_names(graph: Graph):
    labels = set(graph.subjects(RDF.type, XL.Label)) | set(graph.subjects(XL.literalForm, None))
    resources = set()
    for role in ROLES:
        for subject, label in graph.subject_objects(role):
            labels.add(label)
            resources.add(subject)
    for label in labels:
        forms = list(graph.objects(label, XL.literalForm))
        if not isinstance(label, URIRef) or (label, RDF.type, XL.Label) not in graph:
            raise ValueError(f"XL Label requires a stable IRI and explicit type: {label}")
        if len(forms) != 1 or not isinstance(forms[0], Literal) or not str(forms[0]).strip():
            raise ValueError(f"XL Label requires one nonempty literalForm: {label}")
        if any((label, RDF.type, cls) in graph for cls in (SKOS.Concept, SKOS.ConceptScheme, SKOS.Collection, SKOS.OrderedCollection)):
            raise ValueError(f"XL Label has incompatible resource types: {label}")
    for plain in ROLES.values():
        resources.update(graph.subjects(plain, None))
    for subject in resources:
        values = {}
        for role, plain in ROLES.items():
            actual = set(graph.objects(subject, plain))
            projected = {form for label in graph.objects(subject, role) for form in graph.objects(label, XL.literalForm)}
            if any(not isinstance(value, Literal) or not str(value).strip() for value in actual):
                raise ValueError(f"{plain} requires nonempty literal values: {subject}")
            if any(graph.objects(subject, role)) and actual != projected:
                raise ValueError(f"XL projection differs from {plain}: {subject}")
            values[plain] = actual | projected
        preferred = {}
        for value in values[SKOS.prefLabel]:
            language = (value.language or "").lower()
            if language in preferred and preferred[language] != value:
                raise ValueError(f"prefLabel has conflicting values for {language}: {subject}")
            preferred[language] = value
        pref, alt, hidden = (values[plain] for plain in ROLES.values())
        if pref & alt or pref & hidden or alt & hidden:
            raise ValueError(f"Label roles have conflicting literal values: {subject}")


def _dependencies(graph: Graph, targets: set[URIRef], labels: set[URIRef]) -> list[dict]:
    result = []
    for target in sorted(targets, key=str):
        result.append({"subject": str(target), "predicate": str(RDF.type),
                       "values": _values(graph, target, RDF.type),
                       "exists": any(graph.triples((target, None, None)))})
    for label in sorted(labels, key=str):
        result.append({"label": str(label), "usages": sorted(
            [[str(subject), str(role)] for role in ROLES for subject in graph.subjects(role, label)])})
    return result


def _prepare_changes(graph: Graph, operations: list[dict]) -> tuple[list[dict], list[dict]]:
    if not isinstance(operations, list) or not operations:
        raise ValueError("At least one property replacement is required")
    _check_names(graph)
    changes = []
    touched = set()
    labels = set()
    targets = set()
    proposed = graph + Graph()
    for operation in operations:
        if not isinstance(operation, dict) or set(operation) != {"subject", "predicate", "after"}:
            raise ValueError("Each replacement requires subject, predicate and after only")
        subject, predicate = _iri(operation["subject"]), _iri(operation["predicate"])
        if predicate not in DESCRIPTIVE:
            raise ValueError("Only descriptive properties are supported; identity, structure and status changes are excluded")
        if not any(graph.triples((subject, None, None))):
            raise ValueError(f"Edit target does not exist: {subject}")
        if (subject, predicate) in touched:
            raise ValueError("Each resource property must appear only once in the plan")
        after = operation["after"]
        if not isinstance(after, list) or any(not isinstance(value, str) for value in after):
            raise ValueError("after must be a list of N3 values")
        terms = [_term(value) for value in after]
        if len(set(terms)) != len(terms):
            raise ValueError("Duplicate property values are not allowed")
        if predicate in ROLES.values() and any(any(graph.objects(subject, role)) for role in ROLES):
            raise ValueError("Edit XL literalForm instead of overriding its ordinary-label projection")
        if predicate == XL.literalForm or predicate in ROLES.values():
            if any(not isinstance(value, Literal) or not str(value).strip() or not value.language for value in terms):
                raise ValueError("Edited names require nonempty language-tagged literal values")
        if predicate == XL.literalForm:
            if (subject, RDF.type, XL.Label) not in graph or len(terms) != 1:
                raise ValueError("XL literalForm edits require one existing Label and one literal value")
            labels.add(subject)
        before = _values(graph, subject, predicate)
        after = sorted(value.n3() for value in terms)
        if before == after:
            raise ValueError("The proposed property value is unchanged")
        changes.append({"subject": str(subject), "predicate": str(predicate), "before": before, "after": after, "derived": False})
        _set(proposed, subject, predicate, after)
        touched.add((subject, predicate))
        targets.add(subject)
    # Recompute each affected projection from every Label still carrying that role.
    projections = {(subject, role) for label in labels for role in ROLES for subject in graph.subjects(role, label)}
    for subject, role in sorted(projections, key=lambda pair: (str(pair[0]), str(pair[1]))):
        plain = ROLES[role]
        after = sorted({form.n3() for label in proposed.objects(subject, role) for form in proposed.objects(label, XL.literalForm)})
        before = _values(graph, subject, plain)
        if before != after:
            changes.append({"subject": str(subject), "predicate": str(plain), "before": before, "after": after, "derived": True})
            _set(proposed, subject, plain, after)
        targets.add(subject)
    _check_names(proposed)
    if any(not any(proposed.triples((target, None, None))) for target in targets):
        raise ValueError("Descriptive-property edits cannot delete a resource")
    return changes, _dependencies(graph, targets, labels)


def prepare_edit(source: Path, operations: list[dict], plan: Path, *, reason: str, authorization: str) -> dict:
    if not isinstance(reason, str) or not reason.strip() or not isinstance(authorization, str) or not authorization.strip():
        raise ValueError("A reason and authorization reference are required")
    source, plan = Path(source).resolve(), Path(plan).absolute()
    if plan.resolve() == source:
        raise ValueError("The plan must not overwrite its source")
    raw, graph = read_graph(source)
    changes, dependencies = _prepare_changes(graph, operations)
    result = {"format_version": 1, "baseline": {"path": str(source), "sha256": sha256(raw).hexdigest(),
              "graph_sha256": sha256(canonical_bytes(graph)).hexdigest()}, "reason": reason, "authorization": authorization,
              "changes": changes, "dependencies": dependencies}
    encoded = _json_bytes(result)
    if plan.exists() or plan.is_symlink():
        if plan.is_symlink() or not plan.is_file() or plan.read_bytes() != encoded:
            raise ValueError("Existing plan differs; choose a new plan path")
    else:
        plan.parent.mkdir(parents=True, exist_ok=True)
        with plan.open("xb") as target:
            target.write(encoded)
    return result


def _read_plan(plan: Path):
    plan_raw = Path(plan).read_bytes()
    document = json.loads(plan_raw)
    errors = sorted(Draft202012Validator(PLAN_SCHEMA).iter_errors(document), key=lambda error: str(error.path))
    if errors:
        raise ValueError(f"Invalid edit plan: {errors[0].message}")
    if not document["reason"].strip() or not document["authorization"].strip():
        raise ValueError("A reason and authorization reference are required")
    baseline = document["baseline"]
    raw, graph = read_graph(Path(baseline["path"]))
    if sha256(raw).hexdigest() != baseline["sha256"] or sha256(canonical_bytes(graph)).hexdigest() != baseline["graph_sha256"]:
        raise ValueError("Pinned baseline has changed")
    operations = [{key: change[key] for key in ("subject", "predicate", "after")}
                  for change in document["changes"] if not change["derived"]]
    changes, dependencies = _prepare_changes(graph, operations)
    if changes != document["changes"] or dependencies != document["dependencies"]:
        raise ValueError("Plan old values or dependencies differ from the pinned baseline")
    return plan_raw, document, raw, graph


def apply_edit(plan: Path, current: Path, output: Path) -> dict:
    plan, current, output = Path(plan).resolve(), Path(current).resolve(), Path(output).absolute()
    if output.is_symlink():
        raise ValueError("The output must not be a symbolic link")
    plan_raw, document, baseline_raw, baseline_graph = _read_plan(plan)
    current_raw, graph = read_graph(current)
    conflicts = []
    for change in document["changes"]:
        actual = _values(graph, _iri(change["subject"]), _iri(change["predicate"]))
        if actual not in (change["before"], change["after"]):
            conflicts.append({**change, "current": actual, "code": "field_changed"})
    for expected in document["dependencies"]:
        if "label" in expected:
            actual = _dependencies(graph, set(), {_iri(expected["label"])})[0]
        else:
            actual = _dependencies(graph, {_iri(expected["subject"])}, set())[0]
        if actual != expected:
            conflicts.append({"code": "dependency_changed", "before": expected, "current": actual})
    if conflicts:
        raise EditConflict(conflicts)
    _check_names(graph)
    result = graph + Graph()
    for change in document["changes"]:
        _set(result, _iri(change["subject"]), _iri(change["predicate"]), change["after"])
    # Unrelated upstream changes remain present, and all names in the combined graph are checked.
    _check_names(result)
    if any(not any(result.triples((_iri(change["subject"]), None, None))) for change in document["changes"]):
        raise ValueError("Descriptive-property edits cannot delete a resource")
    files = {"baseline.ttl": baseline_raw, "current.ttl": current_raw, "plan.json": plan_raw,
             "vocabulary.ttl": canonical_bytes(result), "version-diff.json": _json_bytes(compare_graphs(graph, result)),
             "upstream-diff.json": _json_bytes(compare_graphs(baseline_graph, graph))}
    manifest = {"format_version": 1, "operation": "descriptive-property-edit", "published": False,
                "semantic_approval_verified": False, "upstream_changes_approved": False,
                "inputs": {"plan": {"path": str(plan), "sha256": sha256(plan_raw).hexdigest()},
                           "current": {"path": str(current), "sha256": sha256(current_raw).hexdigest()},
                           "baseline": document["baseline"]},
                "validation": {"checked": NAME_RULES, "not_checked": ["full-graph SHACL", "semantic correctness", "authorization validity"]},
                "graph_sha256": sha256(files["vocabulary.ttl"]).hexdigest(),
                "files": {name: sha256(raw).hexdigest() for name, raw in files.items()}}
    files["manifest.json"] = _json_bytes(manifest)
    if output.exists():
        if not output.is_dir() or {path.name for path in output.iterdir()} != set(files):
            raise ValueError("Existing output is incomplete or belongs to different inputs")
        for name, raw in files.items():
            path = output / name
            if path.is_symlink() or not path.is_file() or path.read_bytes() != raw:
                raise ValueError(f"Existing output is damaged or differs from this plan and input: {name}")
        return manifest
    for source in (plan, current, Path(document["baseline"]["path"])):
        if source.is_relative_to(output.resolve()):
            raise ValueError("The output must not contain an input")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        for name, raw in files.items():
            (stage / name).write_bytes(raw)
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return manifest
