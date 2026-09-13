"""Independent postconditions over source statements, ledger and projection.

This verifier neither reruns the converter nor trusts its counters. Rule
constants are shared; evidence and actual RDF statements are checked here.
"""
from collections import Counter
from rdflib import Literal, RDF, SKOS, DCTERMS
from .normalization import SCHEME_RELATIONS, INVERSES, INVERSE_INPUTS, REPLACEMENTS


def _key(triple):
    s, p, o = triple
    return str(s), str(p), o.n3()


def verify_normalization(sources, projection, changes, languages):
    def fail(message):
        raise ValueError('Source accounting: ' + message)

    concepts = set().union(*(set(s['graph'].subjects(RDF.type, SKOS.Concept)) for s in sources.values()))
    schemes = set().union(*(set(s['graph'].subjects(RDF.type, SKOS.ConceptScheme)) for s in sources.values()))
    allowed = set(languages)
    originals = {name: {_key(t): t for t in source['graph']} for name, source in sources.items()}

    def inverse(t):
        s, p, o = t
        if p in REPLACEMENTS and not (s in concepts and o in concepts):
            return None
        return (o, INVERSES[p], s) if p in INVERSES else None

    def disposition(t):
        s, p, o = t
        if s in schemes or p in SCHEME_RELATIONS:
            return 'source_only', 'source_scheme_statement', False
        if isinstance(o, Literal) and o.language and o.language.lower().split('-')[0] not in allowed:
            return 'filtered', 'language_outside_output_scope', False
        if s in concepts and p == DCTERMS.type and o == Literal('concept'):
            return 'canonicalized', 'redundant_concept_category', False
        if p in INVERSE_INPUTS and inverse(t) is not None:
            return 'canonicalized', 'inverse_input_retained_with_canonical_direction', True
        return 'copied', None, True

    def evidence(record):
        name = record.get('source')
        source = sources.get(name)
        if source is None or record.get('sha256') != source['sha256'] or record.get('path') != str(source['path']):
            fail('unknown source or mismatched evidence')
        key = tuple(record.get(k) for k in ('subject', 'predicate', 'object'))
        triple = originals[name].get(key)
        if triple is None:
            fail('ledger references a nonexistent source statement')
        return name, key, triple

    records = {}
    derived = set()
    for record in changes:
        if record.get('action') == 'derived':
            name, _, support = evidence(record.get('supporting_original', {}))
            if any(record.get(k) != record['supporting_original'].get(k) for k in ('source', 'path', 'sha256')):
                fail('derived statement has mismatched source evidence')
            result = inverse(support)
            if (record.get('reason') != 'inverse_relation' or not disposition(support)[2]
                    or result is None or _key(result) != tuple(record.get(k) for k in ('subject', 'predicate', 'object'))):
                fail('unsupported derivation')
            if result in derived:
                fail('duplicate derived statement')
            derived.add(result)
        else:
            name, key, triple = evidence(record)
            action, reason, _ = disposition(triple)
            if action == 'copied' or (record.get('action'), record.get('reason')) != (action, reason):
                fail('invalid disposition for source statement')
            if (name, key) in records:
                fail('duplicate source disposition')
            records[name, key] = record

    retained = set()
    by_source = {}
    for name, indexed in originals.items():
        counts = Counter()
        for key, triple in indexed.items():
            action, _, keep = disposition(triple)
            if action != 'copied' and (name, key) not in records:
                fail('missing disposition for changed source statement')
            counts[action] += 1
            if keep:
                retained.add(triple)
        by_source[name] = dict(input_triples=len(indexed), **dict(counts))
    if retained & derived:
        fail('existing source statement incorrectly declared derived')
    expected = retained | derived
    actual = set(projection)
    if actual != expected:
        fail(f'projection differs: {len(expected-actual)} missing, {len(actual-expected)} unsupported statements')
    for triple in retained:
        required = inverse(triple)
        if required is not None and required not in actual:
            fail('missing required inverse relation')
    return {'verified': True, 'by_source': by_source,
            'input_triples': sum(len(g) for g in originals.values()),
            'retained_unique_triples': len(retained), 'derived_triples': len(derived),
            'projection_triples': len(actual)}
