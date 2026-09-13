"""Admit the publisher's native SKOS graph without altering source semantics."""
from collections import Counter
from pathlib import Path

from rdflib import Graph, RDF, SKOS

from kb_vocab.validation import validate_graph


def project_unesco(raw: bytes, source: dict):
    """Read native RDF without rewriting it to the local evaluation profile."""
    graph = Graph().parse(data=raw, format='turtle')
    if not any(graph.subjects(RDF.type, SKOS.Concept)):
        raise ValueError('UNESCO source contains no explicitly typed SKOS concepts')
    validation = validate_graph(graph)
    skos_errors = [issue for issue in validation['errors'] if not issue['code'].startswith('profile.')]
    profile_errors = [issue for issue in validation['errors'] if issue['code'].startswith('profile.')]
    report = {
        'source_id': 'unesco-thesaurus',
        'status': 'source-graph-preserved',
        'stage': 'source-evaluation-only',
        'summary': {
            'triples': len(graph),
            'concepts': len(set(graph.subjects(RDF.type, SKOS.Concept))),
            'schemes': len(set(graph.subjects(RDF.type, SKOS.ConceptScheme))),
            'collections': len(set(graph.subjects(RDF.type, SKOS.Collection))),
            'languages': sorted({value.language for predicate in (SKOS.prefLabel, SKOS.altLabel, SKOS.hiddenLabel)
                                 for value in graph.objects(None, predicate) if getattr(value, 'language', None)}),
        },
        'validation': validation,
        'diagnostics': {
            'skos_errors': skos_errors,
            'profile_errors': profile_errors,
            'error_counts': dict(sorted(Counter(item['code'] for item in validation['errors']).items())),
            'interpretation': 'Profile errors express importer expectations, not SKOS invalidity. SKOS errors remain unresolved in the unmodified publisher graph; no full conformance claim.',
        },
        'policy': 'Preserve all publisher IRIs, labels, language tags, classes and relations. No identity minting, deletion, inference or semantic correction.',
    }
    ledger = {
        'stage': 'source-evaluation-only',
        'source': source,
        'policy': report['policy'],
        'entries': [],
        'note': 'No term-level mapping is performed. source-original.ttl preserves the exact input; vocabulary.ttl represents the same RDF graph.',
        'unresolved': skos_errors,
    }
    return graph, report, ledger


def import_unesco(source_file: Path, output: Path) -> dict:
    """Preserve native RDF, including reported conflicts and non-profile classes."""
    from kb_vocab.bundles import publish_bundle, read_source

    raw, source = read_source(Path(source_file))
    graph, report, ledger = project_unesco(raw, source)
    return publish_bundle(Path(output), graph, report, ledger, source,
                          extras={'source-original.ttl': raw}, allow_invalid=True)
