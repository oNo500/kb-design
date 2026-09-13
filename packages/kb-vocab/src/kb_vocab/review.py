"""Auditable mapping proposals, operator decisions and bounded automatic reuse.

Review Turtle describes statements; only build emits accepted mapping triples.
This local CLI records authorization supplied by its operator, not authentication.
"""
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
from uuid import NAMESPACE_URL, uuid5, uuid4

from rdflib import Graph, Literal, Namespace, RDF, SKOS, URIRef, XSD
from .review_catalog import read_catalog, index_concepts, candidate_pairs
from .validation import validate_graph

REV = Namespace('urn:kb-vocab:review:')
PROV = Namespace('http://www.w3.org/ns/prov#')
RELATIONS = {str(SKOS[name]) for name in ('exactMatch','closeMatch','broadMatch','narrowMatch','relatedMatch')}
STATUSES = {'pending','accepted','deferred','rejected','withdrawn','needs_review'}
RULES = {'version': 1, 'candidate_detection': 'same-language NFC whitespace-folded casefold prefLabel/altLabel; no semantic adoption',
         'automatic_reuse': 'same endpoint URIs, same complete source file hashes, same rules; retain prior decisions',
         'automatic_new_mapping_adoption': False,
         'source_change': 'needs_review; no stale mapping emission',
         'authorization': 'Session-approved complete indexing, candidate preparation and unchanged-decision reuse only'}


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _value(graph, subject, predicate, default=None):
    values = list(graph.objects(subject, predicate))
    if len(values) > 1:
        raise ValueError(f'Ambiguous review property: {predicate}')
    return str(values[0]) if values else default


def _record_graph(records):
    graph = Graph(); graph.bind('review', REV); graph.bind('rdf', RDF); graph.bind('skos', SKOS)
    for record in records.values():
        node=URIRef(record['id']); graph.add((node,RDF.type,REV.MappingReview))
        graph.add((node,RDF.subject,URIRef(record['subject'])))
        graph.add((node,RDF.object,URIRef(record['object'])))
        if record.get('predicate'):
            graph.add((node,RDF.predicate,URIRef(record['predicate'])))
        graph.add((node,REV.status,Literal(record['status'])))
        graph.add((node,REV.evidenceCurrent,Literal(record.get('evidence_current',True))))
        graph.add((node,REV.evidence,Literal(_json(record.get('evidence',[])))))
        graph.add((node,REV.reason,Literal(record.get('reason',''))))
        if record.get('carried_from'):
            graph.add((node,PROV.wasDerivedFrom,Literal(record['carried_from'])))
    return graph


def _records(graph):
    records={}
    for node in graph.subjects(RDF.type,REV.MappingReview):
        row={'id':str(node),'subject':_value(graph,node,RDF.subject), 'object':_value(graph,node,RDF.object),
             'predicate':_value(graph,node,RDF.predicate),'status':_value(graph,node,REV.status),
             'evidence_current':_value(graph,node,REV.evidenceCurrent,'true')=='true',
             'evidence':json.loads(_value(graph,node,REV.evidence,'[]')),'reason':_value(graph,node,REV.reason,'')}
        if not row['subject'] or not row['object'] or row['status'] not in STATUSES:
            raise ValueError('Invalid review record')
        if row['predicate'] and row['predicate'] not in RELATIONS:
            raise ValueError('Unsupported mapping predicate')
        records[row['id']]=row
    return records


def _load(store):
    store=Path(store).absolute()
    raw=(store/'manifest.json').read_bytes(); manifest=json.loads(raw)
    for filename,digest in manifest['files'].items():
        if Path(filename).name!=filename or _sha((store/filename).read_bytes())!=digest:
            raise ValueError('Review snapshot hash mismatch')
    if json.loads((store/'rules.json').read_text())!=RULES:
        raise ValueError('Review rules differ; explicit migration required')
    revision=_sha(raw)
    graph=Graph().parse(store/'review.ttl',format='turtle'); records=_records(graph)
    index=json.loads((store/'concepts.json').read_text()); sources=json.loads((store/'sources.json').read_text())
    history=Graph().parse(store/'history.ttl',format='turtle')
    events=sorted((store/'events').glob('*.ttl'))
    head=json.loads((store/'head.json').read_text())
    if head['sequence']!=len(events):
        raise ValueError('Review journal is incomplete; recover before proceeding')
    for sequence,path in enumerate(events,1):
        data=path.read_bytes(); digest=_sha(data)
        if path.name!=f'{sequence:08d}-{digest}.ttl':
            raise ValueError('Review event hash or sequence mismatch')
        event_graph=Graph().parse(data=data,format='turtle')
        nodes=list(event_graph.subjects(RDF.type,PROV.Activity))
        if len(nodes)!=1:
            raise ValueError('Invalid review event')
        event=nodes[0]
        if _value(event_graph,event,REV.previousRevision)!=revision:
            raise ValueError('Review journal revision mismatch')
        record_id=_value(event_graph,event,REV.record)
        action=_value(event_graph,event,REV.action)
        actor=_value(event_graph,event,PROV.wasAssociatedWith)
        reason=_value(event_graph,event,REV.reason)
        if not actor or not reason:
            raise ValueError('Review event missing actor or reason')
        if action=='propose':
            subject=_value(event_graph,event,RDF.subject); obj=_value(event_graph,event,RDF.object)
            predicate=_value(event_graph,event,RDF.predicate)
            if predicate not in RELATIONS or subject not in index or obj not in index:
                raise ValueError('Invalid proposal endpoints or predicate')
            prior=records.get(record_id,{})
            records[record_id]={'id':record_id,'subject':subject,'object':obj,'predicate':predicate,
                                'status':'pending','reason':reason,'evidence_current':True,'evidence':prior.get('evidence',[])}
        elif action in ('decide','decide_batch'):
            if not _value(event_graph,event,REV.authorization):
                raise ValueError('Missing decision authorization')
            choices = ([{'id':record_id,'decision':_value(event_graph,event,REV.status)}] if action=='decide'
                       else json.loads(_value(event_graph,event,REV.decisions,'[]')))
            if not choices or len({c['id'] for c in choices})!=len(choices):
                raise ValueError('Empty or duplicate batch decisions')
            for choice in choices:
                key,status=choice['id'],choice['decision']
                if key not in records or status not in STATUSES-{'pending','needs_review'}:
                    raise ValueError('Invalid decision')
                if status=='accepted' and (not records[key].get('predicate') or not records[key].get('evidence_current',True)):
                    raise ValueError('Cannot accept without a current proposal')
                records[key].update(status=status,reason=reason)
        else:
            raise ValueError('Unknown review action')
        history+=event_graph
        revision=_sha((revision+digest).encode())
    if revision!=head['revision']:
        raise ValueError('Review journal head mismatch')
    changed=[]
    for name,source in sources.items():
        try:
            same=_sha(Path(source['path']).read_bytes())==source['sha256']
        except OSError:
            same=False
        if not same: changed.append(name)
    return {'store':store,'revision':revision,'sequence':len(events),'records':records,'index':index,
            'sources':sources,'changed':changed,'history':history}


def _effective(state,row):
    row=dict(row)
    changed=any(state['index'].get(row[end],{}).get('source') in state['changed'] for end in ('subject','object'))
    if changed:
        row['previous_status']=row['status']; row['status']='needs_review'; row['evidence_current']=False
    return row


def _stage(output,writer):
    output=Path(output).absolute()
    if output.exists(): raise ValueError(f'Output exists: {output}')
    output.parent.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.review-',dir=output.parent))
    try:
        writer(stage)
        if output.exists(): raise ValueError('Output appeared during publication')
        stage.rename(output)
    finally:
        if stage.exists(): shutil.rmtree(stage)


def scan(catalog,output,previous=None):
    sources=read_catalog(Path(catalog)); index=index_concepts(sources)
    output=Path(output).absolute()
    for source in sources.values():
        if (Path(source['path']).parent/'manifest.json').exists() and output.resolve().is_relative_to(Path(source['path']).resolve().parent):
            raise ValueError('Review output must be outside source directories')
    records={row['id']:dict(row,status='pending',predicate=None,reason='Shared label only; semantic correspondence unreviewed') for row in candidate_pairs(index)}
    history=Graph(); reused=0; invalidated=0
    if previous:
        old=_load(previous); history=old['history']
        pairs={frozenset((row['subject'],row['object'])):key for key,row in records.items()}
        for key,row in old['records'].items():
            pair=frozenset((row['subject'],row['object']))
            current_key=pairs.get(pair)
            evidence=records[current_key]['evidence'] if current_key else row.get('evidence',[])
            if current_key: del records[current_key]
            same=all(uri in index and uri in old['index'] and index[uri]['source']==old['index'][uri]['source']
                     and sources[index[uri]['source']]['sha256']==old['sources'][old['index'][uri]['source']]['sha256']
                     for uri in (row['subject'],row['object']))
            copied=dict(row,evidence=evidence,carried_from=f'{Path(previous).absolute()} @ {old["revision"]}')
            if not same:
                copied['status']='needs_review'; copied['evidence_current']=False; invalidated+=1
            elif row['status']!='pending': reused+=1
            records[key]=copied
    clean_sources={name:{k:v for k,v in source.items() if k!='graph'} for name,source in sources.items()}
    def write(stage):
        (stage/'sources.json').write_text(_json(clean_sources))
        (stage/'concepts.json').write_text(_json(index))
        (stage/'rules.json').write_text(_json(RULES))
        _record_graph(records).serialize(stage/'review.ttl',format='turtle')
        history.serialize(stage/'history.ttl',format='turtle')
        (stage/'events').mkdir()
        manifest={'version':1,'files':{p.name:_sha(p.read_bytes()) for p in sorted(stage.iterdir()) if p.is_file()}}
        raw=_json(manifest).encode(); (stage/'manifest.json').write_bytes(raw)
        (stage/'head.json').write_text(_json({'sequence':0,'revision':_sha(raw)}))
    _stage(output,write)
    result=inspect(output,limit=0)
    result.update(automatically_reused=reused,requires_recheck=invalidated)
    return result


def _groups(state,rows):
    groups={}
    for row in rows:
        names=tuple(sorted({state['index'].get(row[end],{}).get('source','missing-source') for end in ('subject','object')}))
        alternatives=any(e.get(side,{}).get('kind')=='altLabel' for e in row.get('evidence',[]) for side in ('subject_label','object_label'))
        reason=('source_changed' if not row.get('evidence_current',True) else
                'explicit_proposal' if row.get('predicate') else
                'alternative_label_match' if alternatives else 'preferred_label_match')
        key=(names,row['status'],reason)
        group=groups.setdefault(key,{'sources':list(names),'status':row['status'],'reason':reason,'records':[]})
        group['records'].append(row['id'])
    return [dict(group,count=len(group['records'])) for key,group in sorted(groups.items())]


def inspect(store,record_id=None,status=None,limit=20):
    if limit<0: raise ValueError('limit must be nonnegative')
    if status and status not in STATUSES: raise ValueError('Unknown review status')
    state=_load(store)
    rows=[_effective(state,row) for _,row in sorted(state['records'].items())]
    counts=dict(Counter(row['status'] for row in rows))
    groups=[{k:v for k,v in group.items() if k!='records'} for group in _groups(state,rows)]
    if record_id:
        rows=[r for r in rows if r['id']==record_id]
        if not rows: raise ValueError('Review record not found')
    if status: rows=[r for r in rows if r['status']==status]
    result={'revision':state['revision'],'concepts':len(state['index']),'total':len(rows),'statuses':counts,
            'changed_sources':state['changed'],'groups':groups,'records':rows if record_id else rows[:limit]}
    if record_id:
        row=rows[0]
        result['endpoints']={end:state['index'].get(row[end]) for end in ('subject','object')}
        result['history']=[]
        for event in state['history'].subjects(RDF.type,PROV.Activity):
            direct=_value(state['history'],event,REV.record)==record_id
            batch=json.loads(_value(state['history'],event,REV.decisions,'[]'))
            if direct or any(choice['id']==record_id for choice in batch):
                result['history'].append({str(p):str(o) for p,o in state['history'].predicate_objects(event)})
        result['history'].sort(key=lambda e:e.get(str(PROV.endedAtTime),''))
    return result


@contextmanager
def _lock(store):
    lock=Path(store)/'.write-lock'
    try: lock.mkdir()
    except FileExistsError: raise ValueError('Review writer is active; retry or inspect stale lock')
    try: yield
    finally: lock.rmdir()


def _event(state,action,record,actor,reason,**fields):
    if not actor.strip() or not reason.strip(): raise ValueError('Actor and reason are required')
    graph=Graph(); graph.bind('review',REV); graph.bind('rdf',RDF); graph.bind('prov',PROV)
    event=URIRef('urn:uuid:'+str(uuid4()))
    for predicate,value in [(RDF.type,PROV.Activity),(REV.action,Literal(action)),(REV.record,URIRef(record)),
                            (REV.previousRevision,Literal(state['revision'])),(PROV.wasAssociatedWith,URIRef('urn:uuid:'+str(uuid5(NAMESPACE_URL,'review-actor:'+actor)))),
                            (REV.actorName,Literal(actor)),
                            (REV.reason,Literal(reason)),(PROV.endedAtTime,Literal(datetime.now(timezone.utc).isoformat(),datatype=XSD.dateTime))]:
        graph.add((event,predicate,value))
    for name,source in state['sources'].items():
        snapshot=URIRef('urn:sha256:'+source['sha256'])
        graph.add((event,PROV.used,snapshot))
        graph.add((snapshot,REV.sourceName,Literal(name)))
        graph.add((snapshot,REV.sourcePath,Literal(source['path'])))
    for name,value in fields.items():
        predicate={'subject':RDF.subject,'object':RDF.object,'predicate':RDF.predicate}.get(name,REV[name])
        graph.add((event,predicate,URIRef(value) if name in ('subject','object','predicate') else Literal(value)))
    raw=graph.serialize(format='turtle',encoding='utf-8'); digest=_sha(raw)
    sequence=state['sequence']+1; path=state['store']/'events'/f'{sequence:08d}-{digest}.ttl'
    revision=_sha((state['revision']+digest).encode())
    head=state['store']/('.head-'+str(uuid4()))
    try:
        with path.open('xb') as file: file.write(raw)
        head.write_text(_json({'sequence':sequence,'revision':revision}))
        os.replace(head,state['store']/'head.json')
    except BaseException:
        if path.exists(): path.unlink()
        raise
    finally:
        if head.exists(): head.unlink()
    return revision


def propose(store,subject,object,predicate,reason,actor,expected_revision):
    predicate=str(SKOS[predicate]) if predicate in ('exactMatch','closeMatch','broadMatch','narrowMatch','relatedMatch') else predicate
    if predicate not in RELATIONS: raise ValueError('Unsupported mapping relation')
    with _lock(store):
        state=_load(store)
        if state['revision']!=expected_revision: raise ValueError('Stale review revision')
        if subject==object or subject not in state['index'] or object not in state['index']:
            raise ValueError('Mapping needs two distinct indexed concept URIs')
        if state['index'][subject]['source']==state['index'][object]['source']:
            raise ValueError('Mapping review requires different sources')
        if any(state['index'][uri]['source'] in state['changed'] for uri in (subject,object)):
            raise ValueError('Source changed; rescan before proposing')
        pair=frozenset((subject,object))
        existing=next((r for r in state['records'].values() if frozenset((r['subject'],r['object']))==pair),None)
        if existing and existing['status']=='accepted':
            raise ValueError('Withdraw the accepted decision before replacing its proposal')
        record=existing['id'] if existing else 'urn:uuid:'+str(uuid5(NAMESPACE_URL,'review-pair:'+ '\0'.join(sorted(pair))))
        revision=_event(state,'propose',record,actor,reason,subject=subject,object=object,predicate=predicate)
    return {'revision':revision,'record':inspect(store,record)['records'][0]}


def _active(state,override=None):
    rows={key:_effective(state,row) for key,row in state['records'].items()}
    if override: rows[override['id']]=override
    return [row for row in rows.values() if row['status']=='accepted' and row.get('evidence_current',True)
            and all(row[end] in state['index'] for end in ('subject','object'))]


def _mapping_graph(rows):
    graph=Graph(); graph.bind('skos',SKOS)
    for row in rows:
        if row['predicate'] not in RELATIONS: raise ValueError('Accepted mapping lacks supported predicate')
        graph.add((URIRef(row['subject']),URIRef(row['predicate']),URIRef(row['object'])))
    return graph


def _conflicts(state,rows):
    """Check incremental relation conflicts, preserving existing source diagnostics."""
    base=Graph()
    for name,source in state['sources'].items():
        if name not in state['changed']:
            raw=Path(source['path']).read_bytes()
            if _sha(raw)!=source['sha256']: raise ValueError('Source changed during validation; retry after rescan')
            base.parse(data=raw,format='turtle',publicID=source.get('base',Path(source['path']).as_uri()))
    combined=base+_mapping_graph(rows)
    def check(graph):
        projected=Graph()
        for triple in graph: projected.add(triple)
        for a,b in graph.subject_objects(SKOS.broadMatch): projected.add((a,SKOS.broader,b))
        for a,b in graph.subject_objects(SKOS.narrowMatch): projected.add((b,SKOS.broader,a))
        for a,b in graph.subject_objects(SKOS.relatedMatch): projected.add((a,SKOS.related,b))
        errors=validate_graph(projected)['errors']
        parents={}
        def find(x):
            parents.setdefault(x,x)
            while parents[x]!=x:
                parents[x]=parents[parents[x]];x=parents[x]
            return x
        for a,b in graph.subject_objects(SKOS.exactMatch): parents[find(a)]=find(b)
        for predicate in (SKOS.broadMatch,SKOS.narrowMatch,SKOS.relatedMatch):
            for a,b in graph.subject_objects(predicate):
                if a in parents and b in parents and find(a)==find(b):
                    errors.append({'code':'skos.S46.exact_mapping_conflict','subject':str(a),'object':str(b)})
        return {_json(e) for e in errors}
    return [json.loads(e) for e in sorted(check(combined)-check(base))]


def _decisions(state,decisions):
    if not isinstance(decisions,list) or not decisions:
        raise ValueError('A nonempty decisions list is required')
    if any(not isinstance(c,dict) or set(c)!={'id','decision'} for c in decisions):
        raise ValueError('Each batch item needs id and decision only')
    if len({c['id'] for c in decisions})!=len(decisions):
        raise ValueError('Duplicate batch record')
    proposed={key:_effective(state,row) for key,row in state['records'].items()}
    for choice in decisions:
        key,decision=choice['id'],choice['decision']
        if decision not in {'accepted','deferred','rejected','withdrawn'}: raise ValueError('Unsupported decision')
        if key not in proposed: raise ValueError('Review record not found')
        row=proposed[key]
        if row['status']=='accepted' and decision!='withdrawn':
            raise ValueError('Withdraw an existing accepted decision before changing it')
        if decision=='accepted':
            if row['status']=='needs_review' or not row.get('evidence_current',True):
                raise ValueError('Updated evidence requires a new proposal before acceptance')
            if not row.get('predicate'): raise ValueError('Propose a mapping predicate before acceptance')
            endpoints=[state['index'].get(row[end]) for end in ('subject','object')]
            if not all(endpoints) or endpoints[0]['source']==endpoints[1]['source']:
                raise ValueError('Mapping endpoints must exist in different current sources')
        row['status']=decision
    active=[r for r in proposed.values() if r['status']=='accepted']
    if any(c['decision']=='accepted' for c in decisions):
        errors=_conflicts(state,active)
        if errors: raise ValueError('Mapping conflict: '+_json(errors[:5]))
    return proposed


def preview(store,decisions):
    state=_load(store)
    try:
        proposed=_decisions(state,decisions)
    except ValueError as exc:
        return {'revision':state['revision'],'ready':False,'reason':str(exc)}
    before=set(_mapping_graph(_active(state)))
    after=set(_mapping_graph([r for r in proposed.values() if r['status']=='accepted']))
    return {'revision':state['revision'],'ready':True,
            'decisions_sha256':_sha(_json(decisions).encode()),
            'added':sorted([list(map(str,t)) for t in after-before]),
            'removed':sorted([list(map(str,t)) for t in before-after]),
            'note':'Mechanical preview only; does not authorize semantic adoption'}


def decide(store,record_id,decision,actor,authorization,reason,expected_revision):
    if not authorization.strip(): raise ValueError('Explicit authorization reference is required')
    with _lock(store):
        state=_load(store)
        if state['revision']!=expected_revision: raise ValueError('Stale review revision')
        _decisions(state,[{'id':record_id,'decision':decision}])
        revision=_event(state,'decide',record_id,actor,reason,status=decision,authorization=authorization)
    return {'revision':revision,'record':inspect(store,record_id)['records'][0]}


def decide_batch(store,decisions,actor,authorization,reason,expected_revision):
    if not authorization.strip(): raise ValueError('Explicit authorization reference is required')
    with _lock(store):
        state=_load(store)
        if state['revision']!=expected_revision: raise ValueError('Stale review revision')
        _decisions(state,decisions)
        revision=_event(state,'decide_batch','urn:uuid:'+str(uuid4()),actor,reason,
                        decisions=_json(decisions),authorization=authorization)
    return {'revision':revision,'decisions':decisions}


def build(store,output):
    state=_load(store); rows=_active(state); graph=_mapping_graph(rows)
    if rows:
        errors=_conflicts(state,rows)
        if errors: raise ValueError('Mapping conflict: '+_json(errors[:5]))
    accepted_uris={r[end] for r in rows for end in ('subject','object')}
    candidates={r[end] for r in state['records'].values() for end in ('subject','object')}
    coverage=[{'concept':uri,'source':value['source'],'has_accepted_mapping':uri in accepted_uris,
               'has_review_record':uri in candidates} for uri,value in sorted(state['index'].items())]
    report={'review_revision':state['revision'],'concepts':len(state['index']),'review_records':len(state['records']),
            'accepted_mappings':len(graph),'changed_sources':state['changed'],
            'statuses':dict(Counter(_effective(state,r)['status'] for r in state['records'].values())),
            'without_accepted_mapping':sum(not r['has_accepted_mapping'] for r in coverage),
            'scope':'Mapping evaluation only; no concept merge, source deletion, content coverage claim or full SKOS conformance claim'}
    exceptions=[_effective(state,row) for _,row in sorted(state['records'].items()) if _effective(state,row)['status'] in {'pending','deferred','needs_review'}]
    def write(stage):
        graph.serialize(stage/'mappings.ttl',format='turtle')
        (stage/'report.json').write_text(_json(report)); (stage/'coverage.json').write_text(_json(coverage))
        (stage/'exceptions.json').write_text(_json(exceptions))
        (stage/'exception-groups.json').write_text(_json(_groups(state,exceptions)))
        reason_labels={'preferred_label_match':'首选名相同，含义待核对', 'alternative_label_match':'涉及替代名称，归并规则待核对',
                       'explicit_proposal':'已有关系提议', 'source_changed':'来源变化，需要重新提案'}
        group_rows=['| 来源组合 | 原因 | 数量 |','|---|---|---:|']
        for group in _groups(state,exceptions):
            group_rows.append('| '+' / '.join(group['sources'])+' | '+reason_labels[group['reason']]+' | '+str(group['count'])+' |')
        (stage/'index.md').write_text('# 对应审查\n\n'
            f'来源概念 {len(coverage):,} 条；审查记录 {len(state["records"]):,} 条；已采纳映射 {len(graph):,} 条。\n\n'
            '- [映射](mappings.ttl)\n- [例外分组](exception-groups.json)\n- [例外清单](exceptions.json)\n- [全量对账](coverage.json)\n- [报告](report.json)\n\n'
            + '\n'.join(group_rows)+'\n\n无映射不等于缺少内容；所有来源概念继续保留。\n'
            '分组是审查安排，不是已确定的对应关系。候选发现只覆盖同语言相同名称，不保证找出所有语义交叉。\n')
        (stage/'manifest.json').write_text(_json({'files':{p.name:_sha(p.read_bytes()) for p in sorted(stage.iterdir())}}))
        for name in {state['index'][uri]['source'] for uri in accepted_uris}:
            source=state['sources'][name]
            if _sha(Path(source['path']).read_bytes())!=source['sha256']:
                raise ValueError('Source changed before publication; no mapping output published')
    _stage(output,write)
    return report
