"""Local RDFLib concept queries. No remote datasets or federated services."""
from rdflib import Graph, Literal, RDF, SKOS, URIRef
from rdflib.plugins.sparql.parser import parseQuery
from rdflib.plugins.sparql.parserutils import CompValue
from pyparsing import ParseResults


def _term(value):
    result = {'value': str(value), 'type': 'literal' if isinstance(value, Literal) else 'iri' if isinstance(value, URIRef) else 'bnode'}
    if isinstance(value, Literal):
        if value.language:
            result['language'] = value.language
        if value.datatype:
            result['datatype'] = str(value.datatype)
    return result


def _description(graph, node):
    result = {'id': str(node)}
    for name in ('prefLabel', 'altLabel', 'hiddenLabel'):
        result[name] = sorted((_term(v) for v in graph.objects(node, SKOS[name])), key=lambda v: (v['value'], v.get('language', ''), v.get('datatype', '')))
    for name in ('broader', 'narrower', 'related', 'inScheme'):
        result[name] = sorted(str(v) for v in graph.objects(node, SKOS[name]))
    result['relations_are_asserted'] = True
    return result


def describe_concept(graph: Graph, identifier_or_exact_label: str) -> dict:
    concepts = set(graph.subjects(RDF.type, SKOS.Concept))
    identified = [node for node in concepts if str(node) == identifier_or_exact_label]
    if identified:
        return _description(graph, identified[0])
    matches = {subject for predicate in (SKOS.prefLabel, SKOS.altLabel, SKOS.hiddenLabel)
               for subject, label in graph.subject_objects(predicate)
               if subject in concepts and isinstance(label, Literal) and str(label) == identifier_or_exact_label}
    if len(matches) != 1:
        raise ValueError('Concept not found' if not matches else 'Ambiguous label; use the concept identifier')
    return _description(graph, matches.pop())


def find_concepts(graph: Graph, text: str) -> list:
    concepts = set(graph.subjects(RDF.type, SKOS.Concept))
    needle = text.casefold()
    matches = {subject for predicate in (SKOS.prefLabel, SKOS.altLabel, SKOS.hiddenLabel)
               for subject, label in graph.subject_objects(predicate)
               if subject in concepts and isinstance(label, Literal) and needle in str(label).casefold()}
    return [_description(graph, node) for node in sorted(matches, key=str)]


def select_query(graph: Graph, query: str) -> dict:
    try:
        parsed = parseQuery(query)
    except Exception as exc:
        raise ValueError('Only valid local SPARQL SELECT queries are supported') from exc
    if parsed[1].name != 'SelectQuery':
        raise ValueError('Only SPARQL SELECT is supported')
    pending = [parsed]
    while pending:
        node = pending.pop()
        if isinstance(node, CompValue):
            if node.name in ('ServiceGraphPattern', 'DatasetClause'):
                raise ValueError('SERVICE and FROM are disabled; queries must use the local graph')
            pending.extend(node.values())
        elif isinstance(node, (list, tuple, ParseResults)):
            pending.extend(node)
        elif isinstance(node, dict):
            pending.extend(node.values())
    result = graph.query(query)
    variables = [str(var) for var in result.vars]
    return {'variables': variables, 'rows': [
        {name: _term(value) if value is not None else None for name, value in zip(variables, row)}
        for row in result]}
