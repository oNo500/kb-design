"""Execute the vocabulary SHACL profile entirely against supplied local graphs."""
from pathlib import Path

from pyshacl import validate
from rdflib import BNode, Graph, Literal, Namespace, RDF, SKOS, URIRef
from rdflib.namespace import DCTERMS, SH
from rdflib.collection import Collection

PROFILE = Namespace('urn:kb:shacl:')
NOTE_PROPERTIES = (SKOS.definition, SKOS.scopeNote, SKOS.note, SKOS.editorialNote,
                   SKOS.historyNote, SKOS.changeNote)


def validate_profile(graph: Graph, shapes_path: Path, *, generated_nodes=None) -> dict:
    """Return structured SHACL results without imports, inference or graph changes.

    Local note targets are resolved from existing subjects, so external references
    are never mistaken for incomplete local records or dereferenced.
    """
    if not isinstance(graph, Graph):
        raise TypeError('graph must be an already loaded rdflib Graph')
    shapes = Graph().parse(data=Path(shapes_path).read_text(encoding='utf-8'), format='turtle')
    for task in graph.subjects(DCTERMS.type, Literal("task")):
        shapes.add((PROFILE.TaskName, SH.targetNode, task))
    for node in generated_nodes or ():
        shapes.add((PROFILE.GeneratedName, SH.targetNode, node))
        if (node, RDF.type, SKOS.Collection) in graph:
            shapes.add((PROFILE.GeneratedCollection, SH.targetNode, node))
    # Extension properties are open, but language filtering applies to all literals.
    # Add constraints only for offending properties; no per-node SPARQL is needed.
    unsupported = {predicate for _, predicate, value in graph
                   if isinstance(value, Literal) and value.language
                   and value.language.lower().split('-')[0] not in ('en', 'zh')}
    for predicate in unsupported:
        shape = URIRef(str(PROFILE) + 'OutputLanguage/' + str(predicate))
        shapes.add((shape, RDF.type, SH.NodeShape))
        shapes.add((shape, SH.targetSubjectsOf, predicate))
        constraint = BNode()
        shapes.add((shape, SH.property, constraint))
        shapes.add((constraint, SH.path, predicate))
        # sh:languageIn also rejects untagged values; qualified values are selected
        # via an OR permitting everything except non-English/Chinese lang strings.
        choices, nonlanguage, language = BNode(), BNode(), BNode()
        Collection(shapes, choices, [nonlanguage, language])
        shapes.add((constraint, SH['or'], choices))
        typed = BNode()
        shapes.add((nonlanguage, SH['not'], typed))
        shapes.add((typed, SH.datatype, RDF.langString))
        allowed = BNode()
        Collection(shapes, allowed, [Literal('en'), Literal('zh')])
        shapes.add((language, SH.languageIn, allowed))
    subjects = set(graph.subjects())
    for predicate in (SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch,
                      SKOS.narrowMatch, SKOS.relatedMatch):
        for value in graph.objects(None, predicate):
            if value in subjects:
                shapes.add((PROFILE.LocalMappingTarget, SH.targetNode, value))
    for predicate in NOTE_PROPERTIES:
        for value in graph.objects(None, predicate):
            if value in subjects:
                shapes.add((PROFILE.LocalNote, SH.targetNode, value))
    conforms, report, _ = validate(
        data_graph=graph, shacl_graph=shapes, inference='none',
        do_owl_imports=False, advanced=False, js=False, inplace=False,
        meta_shacl=False, allow_infos=True, allow_warnings=True,
        abort_on_first=False,
    )
    if not isinstance(report, Graph):
        raise ValueError(f'SHACL validation did not produce a report graph: {report}')
    violations, warnings = [], []
    fields = {'node': SH.focusNode, 'path': SH.resultPath, 'value': SH.value,
              'shape': SH.sourceShape, 'component': SH.sourceConstraintComponent,
              'severity': SH.resultSeverity}
    for result in report.subjects(RDF.type, SH.ValidationResult):
        issue = {key: str(value) for key, predicate in fields.items()
                 if (value := report.value(result, predicate)) is not None}
        value = report.value(result, SH.value)
        if value is not None:
            issue['value_n3'] = value.n3()
        issue['message'] = '; '.join(sorted(str(value) for value in report.objects(result, SH.resultMessage)))
        destination = warnings if report.value(result, SH.resultSeverity) in (SH.Warning, SH.Info) else violations
        destination.append(issue)
    for issues in (violations, warnings):
        issues.sort(key=lambda issue: tuple(issue.get(key, '') for key in ('node', 'path', 'component', 'value_n3', 'message')))
    return {'conforms': bool(conforms), 'violations': violations,
            'warnings': warnings, 'report_graph': report}
