"""RDFLib-based differences by resource and property, independent of legacy workflows."""
from collections import defaultdict
from decimal import Decimal
from hashlib import sha256
from pathlib import Path

from rdflib import Graph, Literal
from rdflib.compare import graph_diff, to_canonical_graph, to_isomorphic
from rdflib.namespace import XSD
from rdflib.plugins.parsers.notation3 import (
    RDFSink, SinkParser, decimal_syntax, exponent_syntax, integer_syntax, sfloat,
)


class _LexicalSink(RDFSink):
    def newLiteral(self, value, datatype, language):
        literal = Literal(value, datatype=datatype, lang=language, normalize=False)
        if str(literal) != value:
            raise ValueError(f"RDFLib cannot preserve this datatype's lexical form: {datatype}")
        return literal


class _LexicalParser(SinkParser):
    def nodeOrLiteral(self, source, offset, result):
        # RDFLib recognizes Turtle syntax; retain numeric tokens before the
        # parser's Python-number conversion can canonicalize their lexical form.
        previous = len(result)
        end = super().nodeOrLiteral(source, offset, result)
        if end < 0 or len(result) == previous or isinstance(result[-1], bool):
            return end
        value = result[-1]
        if isinstance(value, int):
            syntax, datatype = integer_syntax, XSD.integer
        elif isinstance(value, Decimal):
            syntax, datatype = decimal_syntax, XSD.decimal
        elif isinstance(value, (float, sfloat)):
            syntax, datatype = exponent_syntax, XSD.double
        else:
            return end
        tokens = [match.group() for match in syntax.finditer(source, offset, end) if match.end() == end]
        if not tokens:
            raise ValueError("Cannot preserve the RDF numeric token")
        result[-1] = Literal(tokens[-1], datatype=datatype, normalize=False)
        return end


def parse_turtle(raw: bytes | str, *, public_id: str = "urn:kb-vocab-maintenance:input") -> Graph:
    """Use RDFLib's Turtle parser with lexical-preserving literal construction.

    No global RDFLib normalization setting is changed, including in concurrent
    callers. Syntax, escaping, relative-IRI resolution and datatypes stay with
    RDFLib; the two hooks only preserve lexical forms it normally normalizes.
    """
    graph = Graph()
    parser = _LexicalParser(_LexicalSink(graph), baseURI=public_id, turtle=True)
    parser.loadBuf(raw)
    return graph


def canonical_bytes(graph: Graph) -> bytes:
    canonical = to_canonical_graph(graph)
    return ("\n".join(sorted(f"{s.n3()} {p.n3()} {o.n3()} ." for s, p, o in canonical)) + "\n").encode("utf-8")


def read_graph(path: Path) -> tuple[bytes, Graph]:
    path = Path(path).resolve()
    raw = path.read_bytes()
    return raw, parse_turtle(raw, public_id=path.as_uri())


def compare_graphs(before: Graph, after: Graph) -> dict:
    _, removed, added = graph_diff(to_isomorphic(before), to_isomorphic(after))
    old, new = to_canonical_graph(before), to_canonical_graph(after)
    fields = defaultdict(set)
    for s, p, _ in set(removed) | set(added):
        fields[s].add(p)
    nodes = []
    for subject, predicates in sorted(fields.items(), key=lambda item: item[0].n3()):
        rows = []
        for predicate in sorted(predicates, key=str):
            old_values = {o.n3() for o in old.objects(subject, predicate)}
            new_values = {o.n3() for o in new.objects(subject, predicate)}
            rows.append({"predicate": str(predicate), "before": sorted(old_values), "after": sorted(new_values),
                         "added": sorted(new_values - old_values), "removed": sorted(old_values - new_values)})
        nodes.append({"uri": str(subject), "fields": rows})
    return {"graph_equal": not added and not removed,
            "triples": {"added": len(added), "removed": len(removed)}, "changed_nodes": nodes}


def compare_files(before: Path, after: Path) -> dict:
    old_raw, old = read_graph(before)
    new_raw, new = read_graph(after)
    result = compare_graphs(old, new)
    result["inputs"] = {name: {"path": str(Path(path).resolve()), "sha256": sha256(raw).hexdigest()}
                        for name, path, raw in [("before", before, old_raw), ("after", after, new_raw)]}
    return result
