"""Checks for the explicitly typed evaluation profile, not full SKOS conformance."""
from collections import defaultdict, deque
from rdflib import BNode, Graph, Literal, RDF, SKOS, URIRef


def validate_graph(graph: Graph) -> dict:
    errors, warnings = [], []
    concepts = set(graph.subjects(RDF.type, SKOS.Concept))
    schemes = set(graph.subjects(RDF.type, SKOS.ConceptScheme))
    collections = set(graph.subjects(RDF.type, SKOS.Collection)) | set(graph.subjects(RDF.type, SKOS.OrderedCollection))

    def issue(code, subject, predicate=None, target=None):
        item = {'code': code, 'subject': str(subject)}
        if predicate is not None:
            item['predicate'] = str(predicate)
        if target is not None:
            item['object'] = str(target)
        errors.append(item)

    for node in concepts & schemes:
        issue('skos.S9.disjoint_classes', node)
    for node in collections & (concepts | schemes):
        issue('skos.S37.disjoint_collection', node)
    for node in concepts | schemes | collections:
        if not isinstance(node, (URIRef, BNode)):
            issue('profile.resource_identity', node)
    labels = defaultdict(lambda: defaultdict(set))
    for predicate in (SKOS.prefLabel, SKOS.altLabel, SKOS.hiddenLabel):
        for subject, value in graph.subject_objects(predicate):
            if subject not in concepts and subject not in schemes and subject not in collections:
                issue('profile.explicit_label_subject_type', subject, predicate)
            if not isinstance(value, Literal) or (value.datatype and str(value.datatype) != 'http://www.w3.org/2001/XMLSchema#string'):
                issue('skos.label_literal', subject, predicate, value)
                continue
            labels[subject][predicate].add((str(value), (value.language or '').lower()))
    for subject, by_property in labels.items():
        languages = defaultdict(set)
        for lexical, language in by_property[SKOS.prefLabel]:
            languages[language].add(lexical)
        for language, values in languages.items():
            if len(values) > 1:
                issue('skos.S14.prefLabel_language', subject, SKOS.prefLabel, language)
        for a, b in ((SKOS.prefLabel, SKOS.altLabel), (SKOS.prefLabel, SKOS.hiddenLabel), (SKOS.altLabel, SKOS.hiddenLabel)):
            for lexical, language in by_property[a] & by_property[b]:
                issue('skos.S13.label_disjointness', subject, a, f'{lexical}@{language}')
    for predicate, source_types, target_types in (
        (SKOS.inScheme, concepts | collections, schemes),
        (SKOS.topConceptOf, concepts, schemes),
        (SKOS.hasTopConcept, schemes, concepts),
    ):
        for subject, target in graph.subject_objects(predicate):
            if subject not in source_types:
                issue('profile.explicit_subject_type', subject, predicate)
            if target not in target_types:
                issue('profile.explicit_target_type', subject, predicate, target)
    parents = defaultdict(set)
    related = set()
    for predicate in (SKOS.broader, SKOS.narrower, SKOS.related, SKOS.broaderTransitive, SKOS.narrowerTransitive):
        for subject, target in graph.subject_objects(predicate):
            if subject not in concepts:
                issue('profile.explicit_subject_type', subject, predicate)
            if target not in concepts:
                issue('profile.explicit_target_type', subject, predicate, target)
                continue
            if subject not in concepts:
                continue
            if predicate == SKOS.related:
                related.add((subject, target))
            elif predicate in (SKOS.narrower, SKOS.narrowerTransitive):
                parents[target].add(subject)
            else:
                parents[subject].add(target)
    for a,b in sorted(related,key=lambda pair:tuple(map(str,pair))):
        if a==b:
            warnings.append({'code':'profile.self_related','subject':str(a),'message':'Self-related concepts are permitted by SKOS; review intended use.'})
    # A topological pass detects cycles without recursion or cubic closure matrices.
    indegree = dict.fromkeys(concepts, 0)
    for targets in parents.values():
        for target in targets:
            indegree[target] += 1
    queue = deque(node for node, count in indegree.items() if count == 0)
    removed = 0
    while queue:
        node = queue.popleft()
        removed += 1
        for target in parents.get(node, ()):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if removed < len(concepts):
        warnings.append({'code': 'profile.hierarchy_cycle', 'message': 'Hierarchy contains a cycle; SKOS does not forbid hierarchy cycles.'})
    # Traverse once per related endpoint, bounded by sparse graph reachability.
    checks = defaultdict(set)
    for a, b in related:
        checks[a].add(b)
        checks[b].add(a)
    conflicts = set()
    for start, targets in checks.items():
        seen, pending = set(), list(parents.get(start, ()))
        while pending:
            node = pending.pop()
            if node in seen:
                continue
            seen.add(node)
            if node in targets:
                conflicts.add(tuple(sorted((start, node), key=str)))
            pending.extend(parents.get(node, ()))
    for a, b in sorted(conflicts, key=lambda pair: tuple(map(str, pair))):
        issue('skos.S27.related_hierarchy', a, SKOS.related, b)
    errors.sort(key=lambda item: tuple(sorted(item.items())))
    return {'valid': not errors, 'errors': errors, 'warnings': warnings,
            'scope': 'Supported SKOS constraints plus explicit-type evaluation profile; no inference, no full SKOS conformance claim.'}
