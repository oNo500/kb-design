"""Build a read-only Skosmos navigation view using RDFLib; never write RDF."""
import hashlib
import json
import sys
from pathlib import Path
from rdflib import Graph, RDF, SKOS, DCTERMS, RDFS


def build_navigation(graph):
    concepts = set(graph.subjects(RDF.type, SKOS.Concept))
    narrower = Graph()
    for parent, child in graph.subject_objects(SKOS.narrower):
        if parent in concepts and child in concepts:
            narrower.add((parent, SKOS.narrower, child))
    for child, parent in graph.subject_objects(SKOS.broader):
        if parent in concepts and child in concepts:
            narrower.add((parent, SKOS.narrower, child))

    def labels(subject):
        result = {}
        for prop in (SKOS.prefLabel, DCTERMS.title, RDFS.label):
            for label in sorted(graph.objects(subject, prop), key=str):
                if str(label).strip():
                    result.setdefault(label.language or '', str(label))
        return result

    nodes = {
        str(c): {'labels': labels(c),
                 'notation': str(graph.value(c, SKOS.notation) or ''),
                 'children': sorted(map(str, narrower.objects(c, SKOS.narrower))),
                 'parents': sorted(map(str, narrower.subjects(SKOS.narrower, c)))}
        for c in sorted(concepts)
    }
    schemes = {}
    for scheme in sorted(set(graph.subjects(RDF.type, SKOS.ConceptScheme))):
        tops = set(graph.objects(scheme, SKOS.hasTopConcept)) | set(graph.subjects(SKOS.topConceptOf, scheme))
        members = (set(graph.subjects(SKOS.inScheme, scheme)) | tops) & concepts
        scoped = Graph()
        for parent in members:
            for child in narrower.objects(parent, SKOS.narrower):
                if child in members:
                    scoped.add((parent, SKOS.narrower, child))
        explicit = tops & members
        # These are navigation entries, not new topConceptOf assertions.
        entries = explicit or {c for c in members if not any(scoped.subjects(SKOS.narrower, c))}
        reachable = set()
        for entry in entries:
            reachable.update(scoped.transitive_objects(entry, SKOS.narrower))
        unconnected = members - reachable
        schemes[str(scheme)] = {
            'labels': labels(scheme), 'members': sorted(map(str, members)),
            'entries': sorted(map(str, entries)), 'explicit': bool(explicit),
            'unconnected': sorted(map(str, unconnected))}
    return {'nodes': nodes, 'schemes': schemes}


if __name__ == '__main__':
    source = Path(sys.argv[1])
    raw = source.read_bytes()
    nav = build_navigation(Graph().parse(data=raw, format='turtle'))
    nav['source_sha256'] = hashlib.sha256(raw).hexdigest()
    output = Path(__file__).parent / 'output/navigation/navigation.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    pending = output.with_suffix('.tmp')
    pending.write_text(json.dumps(nav, ensure_ascii=False, separators=(',', ':')) + '\n')
    pending.replace(output)
    print(json.dumps({s: {'members': len(v['members']), 'entries': len(v['entries']),
                          'unconnected': len(v['unconnected'])} for s, v in nav['schemes'].items()}))
