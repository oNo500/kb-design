"""Load self-contained resource shapes and their existing shared constraints."""
from importlib.resources import files

from rdflib import BNode, Graph, RDF, URIRef
from rdflib.namespace import DCTERMS, SH

TARGETS = (SH.targetClass, SH.targetNode, SH.targetSubjectsOf, SH.targetObjectsOf, SH.target)


def load_structure() -> tuple[Graph, list]:
    directory = files("kb_vocab_shacl").joinpath("shapes")
    source = Graph().parse(data=directory.joinpath("structure.ttl").read_text(), format="turtle")
    roots = sorted(
        (node for node in source.subjects(RDF.type, SH.NodeShape) if source.value(node, SH.name)),
        key=str,
    )
    for name in ("skos.ttl", "skos-xl.ttl", "skos-thes.ttl", "metadata.ttl", "profile.ttl"):
        source.parse(data=directory.joinpath(name).read_text(), format="turtle")
    result = Graph()
    for prefix, namespace in source.namespaces():
        result.bind(prefix, namespace)
    result.bind("skosxl", "http://www.w3.org/2008/05/skos-xl#", replace=True)
    result.bind("iso-thes", "http://purl.org/iso25964/skos-thes#", replace=True)
    pending, visited = list(roots), set()
    while pending:
        node = pending.pop()
        if node in visited:
            continue
        visited.add(node)
        for _, predicate, value in source.triples((node, None, None)):
            # A referenced rule runs through its parent. Its old standalone
            # targets must not also activate unrelated legacy checks.
            if node not in roots and predicate in TARGETS:
                continue
            result.add((node, predicate, value))
            if isinstance(value, BNode) or any(
                (value, RDF.type, kind) in source for kind in (SH.NodeShape, SH.PropertyShape)
            ):
                pending.append(value)
    return result, roots


def fields_for(graph: Graph, root) -> dict:
    """Follow sh:node composition; count each direct property only once."""
    fields, visited = {}, set()

    def visit(node):
        if node in visited:
            raise ValueError(f"Cyclic resource composition: {node}")
        if (node, RDF.type, SH.NodeShape) not in graph:
            raise ValueError(f"Undefined resource composition: {node}")
        visited.add(node)
        for shape in graph.objects(node, SH.property):
            paths = list(graph.objects(shape, SH.path))
            if len(paths) != 1 or isinstance(paths[0], BNode):
                raise ValueError(f"Inventory requires one direct field IRI: {shape}")
            if not isinstance(paths[0], URIRef):
                raise ValueError(f"Field path is not an IRI: {shape}")
            fields.setdefault(paths[0], set()).add(shape)
        for parent in graph.objects(node, SH.node):
            visit(parent)
        visited.remove(node)

    visit(root)
    return fields


def conditions_for(graph: Graph, root) -> set:
    """Collect explicit condition links, including inherited resource groups."""
    result, visited, pending = set(), set(), [root]
    while pending:
        node = pending.pop()
        if node in visited:
            continue
        visited.add(node)
        for condition in graph.objects(node, DCTERMS.relation):
            if not any((condition, RDF.type, kind) in graph for kind in (SH.NodeShape, SH.PropertyShape)):
                raise ValueError(f"Undefined conditional shape: {condition}")
            result.add(condition)
        pending.extend(graph.objects(node, SH.node))
    return result
