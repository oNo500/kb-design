"""Source-scoped concept selection with complete original snapshots retained."""
from rdflib import Graph,RDF,SKOS,URIRef


def select_sources(sources, *, audit=True):
    kept={};excluded={};policies={};roots_report={}
    for name,source in sources.items():
        graph=source['graph'];concepts=set(graph.subjects(RDF.type,SKOS.Concept))
        policy=source.get('selection')
        if policy is None:kept[name]=concepts;excluded[name]=set();continue
        if (not isinstance(policy,dict) or set(policy)-{'roots','descendants','reason','ancestors'}
            or not isinstance(policy.get('roots'),list) or not policy['roots']
            or any(not isinstance(uri,str) for uri in policy['roots'])
            or len(set(policy['roots']))!=len(policy['roots']) or type(policy.get('descendants',True)) is not bool):
            raise ValueError('Invalid source selection policy: '+name)
        selected=set();root_counts={}
        for value in policy['roots']:
            root=URIRef(value)
            if root not in concepts:raise ValueError('Selection root is absent from source '+name+': '+value)
            visited=set();pending=[root]
            while pending:
                node=pending.pop()
                if node in visited or node not in concepts:continue
                visited.add(node)
                if policy.get('descendants',True):
                    pending.extend(graph.subjects(SKOS.broader,node));pending.extend(graph.objects(node,SKOS.narrower))
            selected|=visited;root_counts[value]=len(visited)
        ancestors=policy.get('ancestors',[])
        if not isinstance(ancestors,list) or any(not isinstance(uri,str) for uri in ancestors) or len(set(ancestors))!=len(ancestors):
            raise ValueError('Invalid explicit ancestors: '+name)
        if ancestors:
            parent_graph=Graph()
            for child,parent in graph.subject_objects(SKOS.broader):parent_graph.add((child,SKOS.broader,parent))
            for parent,child in graph.subject_objects(SKOS.narrower):parent_graph.add((child,SKOS.broader,parent))
            available=set()
            for node in selected:available.update(parent_graph.transitive_objects(node,SKOS.broader))
            requested={URIRef(uri) for uri in ancestors}
            if not requested<=(available & concepts)-selected:
                raise ValueError('Explicit ancestor is absent, already selected, or unrelated to selected concepts: '+name)
            selected|=requested
        kept[name]=selected;excluded[name]=concepts-selected;policies[name]=policy;roots_report[name]=root_counts
    raw_concepts=set().union(*(set(s['graph'].subjects(RDF.type,SKOS.Concept)) for s in sources.values()))
    selected_concepts=set().union(*kept.values());globally_excluded=raw_concepts-selected_concepts
    result={};by_source={}
    for name,source in sources.items():
        original=source['graph'];blocked=excluded[name]|globally_excluded
        removed={t for t in original if t[0] in blocked or t[2] in blocked}
        graph=original
        if removed:
            graph=Graph()
            for prefix,namespace in original.namespaces():graph.bind(prefix,namespace)
            for triple in original:
                if triple not in removed:graph.add(triple)
        result[name]={**source,'graph':graph}
        row={'sha256':source['sha256'],'input_concepts':len(kept[name])+len(excluded[name]),
             'selected_concepts':len(kept[name]),'excluded_concepts':sorted(map(str,excluded[name])),
             'removed_triples':len(removed),'policy':policies.get(name),'root_counts':roots_report.get(name,{})}
        if audit:row['removed_statements']=sorted(tuple(v.n3() for v in t) for t in removed)
        by_source[name]=row
    return result,{'schema_version':1,'verified':True,'sources':by_source,
                   'excluded_concepts':sorted(map(str,globally_excluded)),
                   'policy':'Keep declared roots, optional descendants, and explicitly listed source ancestors. Ancestors do not expand sibling branches. Never infer related links. Preserve shared identities supported by another selected source. Remove references to excluded concepts; preserve raw snapshots.'}


def verify_selection(originals,projected,report):
    """Check original statements against the selection ledger and actual projection."""
    def fail(message):raise ValueError('Source selection accounting: '+message)
    if set(originals)!=set(projected) or set(report['sources'])!=set(originals):fail('source set changed')
    raw_ids=set().union(*(set(s['graph'].subjects(RDF.type,SKOS.Concept)) for s in originals.values()))
    kept_ids=set().union(*(set(s['graph'].subjects(RDF.type,SKOS.Concept)) for s in projected.values()))
    global_excluded=raw_ids-kept_ids
    if set(report['excluded_concepts'])!=set(map(str,global_excluded)):fail('excluded identity set differs')
    for name,source in originals.items():
        old=source['graph'];new=projected[name]['graph'];row=report['sources'][name]
        if row['sha256']!=source['sha256'] or row['policy']!=source.get('selection'):fail('source or policy differs')
        old_ids=set(old.subjects(RDF.type,SKOS.Concept));new_ids=set(new.subjects(RDF.type,SKOS.Concept))
        if set(row['excluded_concepts'])!=set(map(str,old_ids-new_ids)):fail('source concept dispositions differ')
        if source.get('selection') is None and old_ids!=new_ids:fail('unfiltered source lost concepts')
        old_triples={tuple(v.n3() for v in t):t for t in old}
        removed={tuple(t) for t in row['removed_statements']}
        if len(removed)!=len(row['removed_statements']) or not removed<=set(old_triples):fail('invalid removal ledger')
        blocked=(old_ids-new_ids)|global_excluded
        if any(old_triples[t][0] not in blocked and old_triples[t][2] not in blocked for t in removed):fail('removed a statement unrelated to excluded concepts')
        if set(new)!=(set(old)-{old_triples[t] for t in removed}):fail('projection lost or added unaccounted statements')
    return True
