"""Loss-accounted source projection for vocabulary data specification v3.

Source graphs remain untouched. The returned graph excludes source scheme
statements and out-of-scope languages, and materializes supported inverses.
"""

from collections import Counter

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import DCTERMS, RDF, SKOS

ISO_THES = Namespace("http://purl.org/iso25964/skos-thes#")
SCHEME_RELATIONS = {SKOS.inScheme, SKOS.topConceptOf, SKOS.hasTopConcept}
INVERSES = {
    SKOS.broader: SKOS.narrower,
    SKOS.narrower: SKOS.broader,
    SKOS.related: SKOS.related,
    ISO_THES.superGroup: ISO_THES.subGroup,
    ISO_THES.subGroup: ISO_THES.superGroup,
    DCTERMS.isReplacedBy: DCTERMS.replaces,
    DCTERMS.replaces: DCTERMS.isReplacedBy,
}
INVERSE_INPUTS = {SKOS.narrower, ISO_THES.subGroup, DCTERMS.replaces}
REPLACEMENTS = {DCTERMS.isReplacedBy, DCTERMS.replaces}


def _triple_record(triple):
    subject, predicate, obj = triple
    return {"subject": str(subject), "predicate": str(predicate), "object": obj.n3()}


def normalize_sources(sources, languages=("en", "zh")):
    """Return ``(projection, changes, summary)`` with per-source dispositions.

    Each source record contains ``graph``, ``path`` and ``sha256``. Changes store
    exact original objects in RDF N3 notation; additions cite a retained source
    statement. A copied disposition means the statement is unchanged; an
    inverse input is canonicalized while remaining present in the output.
    """
    output = Graph()
    changes = []
    by_source = {}
    filtered_languages = Counter()
    allowed = {language.lower() for language in languages}
    concepts = set()
    schemes = set()
    for source in sources.values():
        concepts.update(source["graph"].subjects(RDF.type, SKOS.Concept))
        schemes.update(source["graph"].subjects(RDF.type, SKOS.ConceptScheme))

    # Process originals completely before adding inverses so an existing edge
    # in any source is never falsely reported as a derived statement.
    supported = {}
    for name in sorted(sources):
        source = sources[name]
        graph = source["graph"]
        for prefix, namespace in graph.namespaces():
            output.bind(prefix, namespace)
        counts = dict(input_triples=len(graph), copied=0, source_only=0,
                      filtered=0, canonicalized=0)
        by_source[name] = counts
        for triple in sorted(graph, key=lambda t: tuple(term.n3() for term in t)):
            subject, predicate, obj = triple
            action, reason = "copied", None
            inverse = INVERSES.get(predicate)
            if predicate in REPLACEMENTS and not (subject in concepts and obj in concepts):
                inverse = None
            if subject in schemes or predicate in SCHEME_RELATIONS:
                action, reason = "source_only", "source_scheme_statement"
            elif isinstance(obj, Literal) and obj.language and obj.language.lower().split("-", 1)[0] not in allowed:
                action, reason = "filtered", "language_outside_output_scope"
                filtered_languages[obj.language.lower()] += 1
            elif subject in concepts and predicate == DCTERMS.type and obj == Literal("concept"):
                action, reason = "canonicalized", "redundant_concept_category"
            else:
                output.add(triple)
                if inverse is not None:
                    supported.setdefault(triple, {
                        "source": name, "path": str(source["path"]),
                        "sha256": source["sha256"], **_triple_record(triple),
                    })
                    if predicate in INVERSE_INPUTS:
                        action, reason = "canonicalized", "inverse_input_retained_with_canonical_direction"
            counts[action] += 1
            if action != "copied":
                changes.append({"source": name, "path": str(source["path"]),
                                "sha256": source["sha256"], "action": action,
                                "reason": reason, **_triple_record(triple)})

    derived_count = 0
    for original, evidence in supported.items():
        subject, predicate, obj = original
        derived = (obj, INVERSES[predicate], subject)
        if derived not in output:
            output.add(derived)
            derived_count += 1
            changes.append({"source": evidence["source"], "path": evidence["path"],
                            "sha256": evidence["sha256"], "action": "derived",
                            "reason": "inverse_relation", **_triple_record(derived),
                            "supporting_original": evidence})

    summary = {
        "by_source": by_source,
        "filtered_languages": dict(sorted(filtered_languages.items())),
        "input_triples": sum(counts["input_triples"] for counts in by_source.values()),
        "output_triples": len(output),
        "derived_triples": derived_count,
        "source_concepts_preserved": concepts <= set(output.subjects(RDF.type, SKOS.Concept)),
        "source_accounting_complete": all(
            counts["input_triples"] == sum(counts[action] for action in
                                           ("copied", "source_only", "filtered", "canonicalized"))
            for counts in by_source.values()
        ),
    }
    return output, changes, summary
