"""RDF-aware version comparison; serialization and blank-node names are ignored."""
import hashlib
from pathlib import Path
from collections import defaultdict
from rdflib import Graph, BNode, RDF, SKOS
from rdflib.compare import to_canonical_graph


def compare_graphs(before, after):
    def triples(graph):
        if any(isinstance(x,BNode) for t in graph for x in t):
            graph=to_canonical_graph(graph)
        return set(graph)
    old,new=triples(before),triples(after)
    added,removed=new-old,old-new
    nodes=defaultdict(lambda:defaultdict(lambda:{'added':[],'removed':[]}))
    for action,rows in [('added',added),('removed',removed)]:
        for s,p,o in rows:nodes[str(s)][str(p)][action].append(o.n3())
    old_ids=set(before.subjects(RDF.type,SKOS.Concept))
    new_ids=set(after.subjects(RDF.type,SKOS.Concept))
    return {'graph_equal':not added and not removed,
            'triples':{'added':len(added),'removed':len(removed)},
            'concepts':{'added':sorted(map(str,new_ids-old_ids)),'removed':sorted(map(str,old_ids-new_ids))},
            'changed_nodes':[{'uri':node,'fields':[{'predicate':p,**{k:sorted(v) for k,v in values.items()}}
                             for p,values in sorted(fields.items())]} for node,fields in sorted(nodes.items())]}


def compare_files(before,after):
    before,after=Path(before).resolve(),Path(after).resolve()
    old_raw,new_raw=before.read_bytes(),after.read_bytes()
    result=compare_graphs(Graph().parse(data=old_raw,format='turtle',publicID=before.as_uri()),
                          Graph().parse(data=new_raw,format='turtle',publicID=after.as_uri()))
    result['inputs']={name:{'path':str(path),'sha256':hashlib.sha256(raw).hexdigest()}
                      for name,path,raw in [('before',before,old_raw),('after',after,new_raw)]}
    return result
