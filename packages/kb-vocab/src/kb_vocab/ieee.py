"""Conservative IEEE-to-SKOS evaluation projection with a complete source ledger."""
from collections import Counter, defaultdict, deque
from importlib.resources import files
import hashlib
import json
import os
from pathlib import Path
import tempfile

from rdflib import Graph, Literal, RDF, SKOS, DCTERMS, OWL, URIRef
from rdflib.namespace import PROV
from kb_vocab.validation import validate_graph


def _import_key(entry):
    return entry['id']+'@'+hashlib.sha256(entry['name'].encode('utf-8')).hexdigest()


def _identity(source, preferred, previous):
    from .identity import align, mint
    scheme=mint('ieee','__scheme__');old={}
    if previous is not None:
        schemes=list(previous.subjects(RDF.type,SKOS.ConceptScheme))
        if len(schemes)!=1 or (schemes[0],SKOS.prefLabel,Literal('IEEE Thesaurus',lang='en')) not in previous:
            raise ValueError('identity source must contain one IEEE scheme')
        scheme=schemes[0]
        for node in previous.subjects(RDF.type,SKOS.Concept):
            keys=list(previous.objects(node,DCTERMS.identifier))
            if len(keys)!=1 or '@' not in str(keys[0]):raise ValueError('identity source missing import key')
            key=str(keys[0]).rsplit('@',1)[1]
            if key in old:raise ValueError('identity source contains duplicate name keys')
            old[key]=node
    keys={name:hashlib.sha256(name.encode()).hexdigest() for name in preferred}
    aligned=align('ieee',keys.values(),old)
    return scheme,{name:aligned[key] for name,key in keys.items()}


def _path(parents,start,target):
    todo=deque([(start,[start])]);seen={start}
    while todo:
        node,path=todo.popleft()
        for parent in sorted(parents.get(node,())):
            if parent==target:return path+[parent]
            if parent not in seen:seen.add(parent);todo.append((parent,path+[parent]))
    return None


def project_ieee(data, *, identities=None, indirect_rt_policy=None):
    if data.get('representation')!='ieee-source-transcription':raise ValueError('expected IEEE source transcription')
    if data.get('unassigned'):raise ValueError('source has unassigned lines; resolve extraction before projection')
    policy_applies=bool(indirect_rt_policy and indirect_rt_policy.get('rule')=='exclude_indirect_ancestor_rt'
        and indirect_rt_policy.get('source_sha256')==data['source']['sha256']
        and indirect_rt_policy.get('source_data_sha256')==hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest())
    entries=data['entries'];by_name={e['name']:e for e in entries}
    if len(by_name)!=len(entries) or len({e['id'] for e in entries})!=len(entries):raise ValueError('duplicate source names or record IDs')
    preferred={e['name']:e for e in entries if e['form']=='preferred'}
    if any(e['form'] not in ('preferred','nonpreferred') for e in entries):raise ValueError('unknown source form')
    for e in entries:
        for r in e['relations']:
            if r['predicate'] not in ('BT','NT','RT','USE','UF'):raise ValueError('unknown source predicate')
    if not preferred:raise ValueError('no preferred source entries')
    scheme,ids=_identity(data['source'],preferred,identities)
    graph=Graph()
    for prefix,ns in [('skos',SKOS),('dcterms',DCTERMS),('prov',PROV),('owl',OWL)]:graph.bind(prefix,ns)
    graph.add((scheme,RDF.type,SKOS.ConceptScheme))
    graph.add((scheme,SKOS.prefLabel,Literal('IEEE Thesaurus',lang='en')))
    graph.add((scheme,DCTERMS.identifier,Literal('sha256:'+data['source']['sha256'])))
    graph.add((scheme,DCTERMS.source,URIRef(data['source']['url'])))
    graph.add((scheme,OWL.versionInfo,Literal(data['source']['version'])))
    graph.add((scheme,SKOS.note,Literal('Evaluation projection, not adopted project vocabulary. Local import keys are not IEEE identifiers. Held source statements remain in mapping-ledger.json.',lang='en')))
    for name,e in preferred.items():
        node=ids[name];graph.add((node,RDF.type,SKOS.Concept));graph.add((node,SKOS.inScheme,scheme))
        graph.add((node,SKOS.prefLabel,Literal(name,lang='en')));graph.add((node,DCTERMS.identifier,Literal(_import_key(e))))
        graph.add((node,PROV.wasDerivedFrom,URIRef(data['source']['url']+'#page='+str(e['locator']['page']))))
    ambiguous={e['name'] for e in entries if any(r.get('connector_after') for r in e['relations'])}
    aliases={}
    for e in entries:
        if e['form']!='nonpreferred' or e['name'] in ambiguous:continue
        rels=e['relations']
        if len(rels)!=1 or rels[0]['predicate']!='USE':continue
        target=rels[0]['target']
        if target not in preferred:continue
        if any(r['predicate']=='UF' and r['target']==e['name'] for r in preferred[target]['relations']):aliases[e['name']]=target
    parents=defaultdict(set)
    for e in preferred.values():
        for r in e['relations']:
            if r['target'] not in preferred:continue
            if r['predicate']=='BT':parents[e['name']].add(r['target'])
            if r['predicate']=='NT':parents[r['target']].add(e['name'])
    reach={}
    for name in preferred:
        seen=set();pending=list(parents.get(name,()))
        while pending:
            other=pending.pop()
            if other in seen:continue
            seen.add(other);pending.extend(parents.get(other,()))
        reach[name]=seen
    ledger={'source':data['source'],'scheme':str(scheme),'identity_policy':'Persistent UUID URIs; reuse this Turtle with --identities across snapshots by exact source name. Missing prior names block replacement; extraction ordinals are not stable identities.',
            'projection_policy':'Keep source hierarchy; hold S27-conflicting related pairs for review. This does not declare the source wrong or adopt permanent hierarchy precedence.',
            'entries':[],'relations':[]}
    ledger['applied_projection_policy']=indirect_rt_policy if policy_applies else None
    if policy_applies:
        ledger['projection_policy']='For this pinned source, indirect ancestor RT is excluded by authorized projection policy. Hierarchy and source evidence are unchanged; other ambiguous cases remain held.'
    for e in entries:
        node=ids.get(e['name']) or ids.get(aliases.get(e['name']))
        ledger['entries'].append({'source_entry_id':e['id'],'source_name':e['name'],'source_form':e['form'],
            'concept':str(node) if node else None,'status':'represented' if node else 'held','locator':e['locator']})
        for index,r in enumerate(e['relations']):
            name,target,predicate=e['name'],r['target'],r['predicate'];triple=None;reason=None;path=None
            if predicate in ('USE','UF'):
                alias,preferred_name=(name,target) if predicate=='USE' else (target,name)
                if alias in ambiguous:reason='and_group'
                elif aliases.get(alias)==preferred_name:triple=(ids[preferred_name],SKOS.altLabel,Literal(alias,lang='en'))
                else:reason='source_alias_conflict'
            elif name not in preferred or target not in preferred:reason='nonpreferred_semantic_endpoint'
            elif predicate=='RT' and (target in reach[name] or name in reach[target]):
                reason='s27_overlap';path=_path(parents,name,target) if target in reach[name] else _path(parents,target,name)
            else:triple=(ids[name],{'BT':SKOS.broader,'NT':SKOS.narrower,'RT':SKOS.related}[predicate],ids[target])
            row={'source_entry_id':e['id'],'source_relation_index':index,'subject':name,'source_relation':r,
                 'status':'emitted' if triple else 'held','reason':reason}
            if path:
                row['hierarchy_path']=path
                direct=target in parents[name] or name in parents[target]
                if policy_applies and not direct and name!=target:
                    row['status']='excluded_by_policy';row['policy_id']=indirect_rt_policy['id']
            if triple:
                graph.add(triple);row['triple']=' '.join(x.n3() for x in triple)+' .'
            ledger['relations'].append(row)
    return graph,ledger


def import_ieee(source_file,output, *, identity_file=None):
    source_file=Path(source_file).resolve();raw=source_file.read_bytes();data=json.loads(raw)
    receipt_path=source_file.parent/'record.json';receipt=json.loads(receipt_path.read_text())
    if receipt['outputs'].get(source_file.name)!=hashlib.sha256(raw).hexdigest():raise ValueError('source extraction hash mismatch')
    if receipt['source']!=data['source']:raise ValueError('source extraction metadata mismatch')
    target=Path(output).absolute()
    if target.exists() or target.is_symlink():raise ValueError('output must be a new directory')
    if source_file.parent==target.resolve() or source_file.parent in target.resolve().parents:raise ValueError('output cannot be inside source extraction directory')
    identity_bytes=Path(identity_file).read_bytes() if identity_file else None
    if identity_file:
        identity_path=Path(identity_file)
        try:
            identity_manifest=json.loads((identity_path.parent/'manifest.json').read_text())
        except (OSError,ValueError) as exc:
            raise ValueError('identity source requires its evaluation manifest') from exc
        if identity_manifest.get('files',{}).get(identity_path.name)!=hashlib.sha256(identity_bytes).hexdigest():
            raise ValueError('identity source differs from its recorded evaluation; edited imports require review')

    identities=Graph().parse(data=identity_bytes.decode(),format='turtle',publicID=Path(identity_file).absolute().as_uri()) if identity_bytes else None
    policy=json.loads(files('kb_vocab').joinpath('policies','ieee-2025-07.json').read_text())
    graph,ledger=project_ieee(data,identities=identities,indirect_rt_policy=policy);validation=validate_graph(graph)
    if not validation['valid']:raise ValueError('projection failed supported SKOS/profile checks: '+json.dumps(validation['errors'][:5]))
    counts=Counter(row['reason'] or 'emitted' for row in ledger['relations'])
    summary={'stage':'evaluation-only','concepts':len(set(graph.subjects(RDF.type,SKOS.Concept))),
        'alternative_labels':len(list(graph.triples((None,SKOS.altLabel,None)))),
        'triples':len(graph),'source_relation_dispositions':dict(counts),'validation':validation,
        'source_json_sha256':hashlib.sha256(raw).hexdigest(),
        'identity_source_sha256':hashlib.sha256(identity_bytes).hexdigest() if identity_bytes else None}
    summary['relation_statuses']=dict(Counter(row['status'] for row in ledger['relations']))
    summary['resolved_indirect_rt_pairs']=len({tuple(sorted((row['subject'],row['source_relation']['target']))) for row in ledger['relations'] if row['status']=='excluded_by_policy'})
    summary['applied_projection_policy']=policy['id'] if ledger['applied_projection_policy'] else None
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.import-',dir=target.parent) as tmp:
        stage=Path(tmp)/'result';stage.mkdir()
        graph.serialize(destination=stage/'vocabulary.ttl',format='turtle',encoding='utf-8')
        reloaded=Graph().parse(stage/'vocabulary.ttl',format='turtle')
        from rdflib.compare import isomorphic
        if not isomorphic(graph,reloaded):raise ValueError('Turtle round-trip changed the RDF graph')
        for name,value in [('mapping-ledger.json',ledger),('report.json',summary),('validation.json',validation)]:
            (stage/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
        if ledger['applied_projection_policy']:
            (stage/'projection-policy.json').write_text(json.dumps(ledger['applied_projection_policy'],ensure_ascii=False,indent=2)+'\n')
        (stage/'index.md').write_text('# 词表评估\n\nIEEE 来源的 SKOS 评估投影，不是已采纳的正式词表。\n\n'
            +f'{summary["concepts"]} 个概念、{summary["alternative_labels"]} 个替代标签。\n\n'
            +'[Turtle 词表](vocabulary.ttl) · [映射账本](mapping-ledger.json) · [运行报告](report.json) · [校验结果](validation.json)\n\n'
            +('间接祖先 RT 已按[固定来源投影规则](projection-policy.json)排除，不再逐对挂起；原文证据完整保留。AND 分组及来源名称异常继续隔离，不阻塞其他来源处理。\n' if ledger['applied_projection_policy'] else 'AND 分组、来源名称异常与 S27 冲突关系保留在账本中，未经审查不写入确定语义。原始数据不变。\n'))
        from importlib.metadata import version
        manifest={'source_file':str(source_file),'source_json_sha256':summary['source_json_sha256'],
            'identity_source':str(Path(identity_file).resolve()) if identity_file else None,'identity_source_sha256':summary['identity_source_sha256'],
            'rdflib':version('rdflib'),'tool':{'name':'kb-vocab','version':'0.1.0','profile':'ieee-skos-evaluation-v1','implementation_sha256':hashlib.sha256(Path(__file__).read_bytes()+Path(__file__).with_name('validation.py').read_bytes()).hexdigest()},'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(stage.iterdir())}}
        (stage/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        if source_file.read_bytes()!=raw:raise ValueError('source changed during import')
        if identity_file and Path(identity_file).read_bytes()!=identity_bytes:raise ValueError('identity source changed during import')
        if target.exists() or target.is_symlink():raise ValueError('output appeared during import')
        os.rename(stage,target)
    return summary
