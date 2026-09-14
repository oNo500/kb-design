"""Desired source synchronization and local-only rebuilds with resumable status."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
from uuid import uuid4
from rdflib import Graph,RDF,SKOS,URIRef
from .edit_store import atomic,encode,lock,load
from .publication import _verify,build_versioned,_layout
from .review_catalog import read_catalog
from .source_pipeline import materialize,declaration_digest
from .local_edits import EditConflict,empty


def sha(raw):return hashlib.sha256(raw).hexdigest()

def _record(path,state):
    state['updated_at']=datetime.now(timezone.utc).isoformat()
    with (path/'events.jsonl').open('a',encoding='utf-8') as stream:stream.write(json.dumps({'state':state['state'],'at':state['updated_at']})+'\n')
    atomic(path/'status.json',encode(state));atomic(path.parent.parent/'maintenance-status.json',encode(state))

def _source_nodes(graph):return {str(s) for s in graph.subjects(RDF.type,None) if isinstance(s,URIRef)}

def maintain(config_file,root,*,mode='sync',refresh=(),applications=None,prepared_sources=None):
    config_file=Path(config_file).resolve();root=_layout(Path(root).absolute()).resolve()
    if mode not in {'sync','local'}:raise ValueError('Unknown maintenance mode')
    with lock(root/'.maintenance-lock'):
        op=root/'operations'/('op-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+uuid4().hex[:8]);op.mkdir(parents=True)
        state={'operation':op.name,'directory':str(op),'config':str(config_file),'mode':mode,'state':'preparing','applications':applications or [],'refresh':list(refresh),'prepared':{}}
        _record(op,state)
        try:
            raw=config_file.read_bytes();desired=json.loads(raw)
            atomic(op/'request-config.json',raw)
            current=(root/'current').resolve() if (root/'current').is_symlink() else None
            if current:_verify(current)
            prior=read_catalog(current/'inputs/catalog.json') if current else {}
            edits_path=(config_file.parent/desired.get('local_edits','local-edits.json')).resolve()
            edits=load(edits_path);edits_raw=encode(edits)
            oldstate=json.loads((root/'source-state.json').read_bytes()) if (root/'source-state.json').exists() else {}
            declarations={};materialized={}
            if mode=='local':
                if current is None:raise ValueError('Local-only edits need an initial synchronized build')
                config=json.loads((current/'inputs/config.json').read_bytes());config_base=current/'inputs'
                ready={name:dict(source) for name,source in prior.items()}
            else:
                config=deepcopy(desired);config_base=config_file.parent
                catalog_path=(config_file.parent/desired['catalog']).resolve();catalog_raw=catalog_path.read_bytes()
                atomic(op/'request-catalog.json',catalog_raw)
                entries=json.loads(catalog_raw)['sources']
                names=[entry['name'] for entry in entries]
                if len(set(names))!=len(names):raise ValueError('Duplicate source name')
                if set(refresh)-set(names):raise ValueError('Unknown refresh source')
                prepared=[]
                for entry in entries:
                    name=entry['name'];prior_file=prior.get(name,{}).get('path')
                    saved=(prepared_sources or {}).get(name)
                    if saved and saved['declaration']==declaration_digest(entry):
                        path=Path(saved['file']);decl=saved['declaration']
                        if sha(path.read_bytes())!=saved['sha256']:raise ValueError('Prepared source changed; start a fresh synchronization')
                    else:
                        path,decl=materialize(entry,catalog_path.parent,op/'pipelines'/sha(name.encode())[:12],prior_file,name in refresh,oldstate.get(name))
                    state['prepared'][name]={'file':str(path),'declaration':decl,'sha256':sha(path.read_bytes())};_record(op,state)
                    declarations[name]=decl;materialized[name]={'file':str(path),'declaration':decl}
                    prepared.append({'name':name,'file':str(path),'base':entry.get('base',path.as_uri()),**({'selection':entry['selection']} if 'selection' in entry else {})})
                atomic(op/'ready-catalog.json',encode({'sources':prepared}));ready=read_catalog(op/'ready-catalog.json')
                if catalog_path.read_bytes()!=catalog_raw:raise ValueError('Source list changed during synchronization')
            source_changes={'added':sorted(set(ready)-set(prior)),'removed':sorted(set(prior)-set(ready)),
                            'updated':sorted(n for n in set(ready)&set(prior) if ready[n]['sha256']!=prior[n]['sha256']),
                            'selection_changed':sorted(n for n in set(ready)&set(prior) if ready[n].get('selection')!=prior[n].get('selection'))}
            state['source_changes']=source_changes
            incoming_concepts=set().union(*(set(s['graph'].subjects(RDF.type,SKOS.Concept)) for s in ready.values()))
            incoming_nodes=set().union(*(_source_nodes(s['graph']) for s in ready.values()))
            removed_nodes=set().union(*(_source_nodes(prior[n]['graph']) for n in source_changes['removed']))-incoming_nodes
            removed_concepts=set().union(*(set(prior[n]['graph'].subjects(RDF.type,SKOS.Concept)) for n in source_changes['removed']))-incoming_concepts
            pruned=[]
            for domain in config['domains']:
                old_branches=domain.get('branches',[])
                domain['branches']=[b for b in old_branches if b['source'] in ready]
                domain['whole_sources']=[n for n in domain.get('whole_sources',[]) if n in ready]
                pruned.extend({'domain':domain['id'],**b} for b in old_branches if b['source'] not in ready)
            config['vocabulary']['top_concepts']=[u for u in config['vocabulary']['top_concepts'] if u not in removed_nodes]
            config.pop('replay_origin',None);config.pop('source_removal',None);config.pop('maintenance',None)
            config['sources']={n:s['sha256'] for n,s in ready.items()}
            # Absolute paths are only operation inputs. The builder creates its
            # existing portable replay archive and verified byte copies.
            atomic(op/'catalog.json',encode({'sources':[{'name':n,'file':s['path'],'base':s['base'],**({'selection':s['selection']} if 'selection' in s else {})} for n,s in ready.items()]}))
            config['catalog']=str(op/'catalog.json')
            config['shapes']=str((config_base/config['shapes']).resolve())
            labels={k:(config_base/v).resolve() for k,v in config.get('labels',{}).items()}
            config['labels']={k:str(v) for k,v in labels.items()} if labels else config.get('labels',{})
            if not labels:config.pop('labels',None)
            atomic(op/'local-edits.json',edits_raw);config['local_edits']=str(op/'local-edits.json')
            old_local=json.loads((current/'local-effects.json').read_bytes()).get('created_nodes',[]) if current and (current/'local-effects.json').exists() else []
            live_local={p['subject'] for p in edits['patches'] if p['op']=='create'}
            if current:
                config['maintenance']={'baseline_sha256':sha((current/'vocabulary.ttl').read_bytes()),
                    'removed_sources':source_changes['removed'],'removed_source_nodes':sorted(removed_nodes),
                    'removed_source_concepts':sorted(map(str,removed_concepts)),
                    'removed_local_nodes':sorted(set(old_local)-live_local-incoming_nodes)}
            logical={k:v for k,v in config.items() if k not in {'catalog','shapes','labels','local_edits','maintenance'}}
            fingerprint=sha(encode({'config':logical,'sources':{n:{'sha256':s['sha256'],'base':s['base'],'selection':s.get('selection')} for n,s in ready.items()},
                                  'shapes':sha(Path(config['shapes']).read_bytes()),'labels':{k:sha(p.read_bytes()) for k,p in labels.items()},
                                  'edits':sha(edits_raw),'code':{p.name:sha(p.read_bytes()) for p in Path(__file__).parent.glob('*.py')}}))
            state.update(fingerprint=fingerprint,pruned_rules=pruned)
            lastpath=root/'maintenance-success.json';last=json.loads(lastpath.read_bytes()) if lastpath.exists() else {}
            if last.get('fingerprint')==fingerprint and current and last.get('build')==str(current):
                state.update(state='unchanged',build=str(current));_record(op,state)
            else:
                atomic(op/'config.json',encode(config));state['state']='building';_record(op,state)
                if config_file.read_bytes()!=raw or encode(load(edits_path))!=edits_raw:raise ValueError('Maintenance inputs changed before building')
                def inputs_unchanged():
                    if config_file.read_bytes()!=raw or encode(load(edits_path))!=edits_raw:
                        raise ValueError('Maintenance inputs changed; completed candidate was not activated')
                    if mode=='sync' and catalog_path.read_bytes()!=catalog_raw:
                        raise ValueError('Desired source list changed; candidate was not activated')
                result=build_versioned(op/'config.json',root,op.name,before_activate=inputs_unchanged)
                state.update(state='published',build=result['publication']['output'],report=result)
                if mode=='sync':atomic(root/'source-state.json',encode(materialized))
                atomic(lastpath,encode({'fingerprint':fingerprint,'build':state['build']}))
                _record(op,state)
            if applications:
                from .maintenance_apps import synchronize
                state['state']='syncing-applications';_record(op,state)
                state['application_results']=synchronize(Path(state['build']),applications,op)
            if state['state']!='unchanged':state['state']='complete'
            _record(op,state);return state
        except EditConflict as exc:
            exc.upstream.serialize(op/'incoming.ttl',format='turtle')
            report={**exc.report,'incoming_sha256':sha((op/'incoming.ttl').read_bytes()),'edits_sha256':sha(edits_raw)}
            atomic(op/'conflicts.json',encode(report));state.update(state='conflict',conflicts=str(op/'conflicts.json'),error=str(exc));_record(op,state);return state
        except Exception as exc:
            state.update(state='application-failed' if state.get('build') else 'failed',error=str(exc));_record(op,state);return state


def resume(root,operation=None):
    root=Path(root).resolve()
    path=root/'operations'/operation/'status.json' if operation else root/'maintenance-status.json'
    state=json.loads(path.read_bytes())
    if state['state'] in {'complete','unchanged'}:return state
    if state['state']=='application-failed':
        from .maintenance_apps import synchronize
        with lock(root/'.maintenance-lock'):
            if (root/'current').resolve()!=Path(state['build']).resolve():raise ValueError('Current changed; synchronize the current build instead of resuming stale application data')
            state['application_results']=synchronize(Path(state['build']),state['applications'],Path(state['directory']))
            state['state']='complete';_record(Path(state['directory']),state);return state
    return maintain(state['config'],root,mode=state['mode'],refresh=state.get('refresh',()),applications=state.get('applications'),prepared_sources=state.get('prepared'))
