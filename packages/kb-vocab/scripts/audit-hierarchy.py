"""Report concepts unreachable from declared tops without inferring relationships."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from rdflib import Graph, RDF, SKOS
from kb_vocab.review_catalog import read_catalog


def audit(build):
    build=Path(build).resolve()
    raw=(build/'vocabulary.ttl').read_bytes()
    graph=Graph().parse(data=raw,format='turtle')
    sources=read_catalog(build/'inputs/catalog.json')
    concepts=set(graph.subjects(RDF.type,SKOS.Concept))
    def parents(g,u):return set(g.objects(u,SKOS.broader))|set(g.subjects(SKOS.narrower,u))
    downward=Graph()
    for child,parent in graph.subject_objects(SKOS.broader):downward.add((parent,SKOS.narrower,child))
    for parent,child in graph.subject_objects(SKOS.narrower):downward.add((parent,SKOS.narrower,child))
    reached=set()
    for top in graph.objects(None,SKOS.hasTopConcept):reached.update(downward.transitive_objects(top,SKOS.narrower))
    missing=concepts-reached
    rows=[]
    for name,source in sources.items():
        original=source['graph'];source_missing=missing & set(original.subjects(RDF.type,SKOS.Concept))
        for node in sorted(source_missing):
            local_parents=parents(graph,node) & concepts
            original_parents=parents(original,node)
            cause=('within_unconnected_branch' if local_parents else
                   'source_parent_excluded' if original_parents else 'source_has_no_parent')
            rows.append({'uri':str(node),'source':name,'source_sha256':source['sha256'],
                         'label':str(original.value(node,SKOS.prefLabel) or ''),
                         'notation':str(original.value(node,SKOS.notation) or ''),
                         'cause':cause,'original_parents':sorted(map(str,original_parents)),
                         'current_parents':sorted(map(str,local_parents))})
    return {'schema_version':1,'build':str(build),'vocabulary_sha256':hashlib.sha256(raw).hexdigest(),
            'unconnected_concepts':len(missing),'by_source':dict(sorted(Counter(r['source'] for r in rows).items())),
            'by_cause':dict(sorted(Counter(r['cause'] for r in rows).items())),
            'records':rows,'scope':'Read-only diagnostic. Missing source parents and source gaps do not authorize new semantic links.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();result=audit(args.build)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x',encoding='utf-8') as stream:json.dump(result,stream,ensure_ascii=False,indent=2);stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},ensure_ascii=False,indent=2))
