"""CLI for source synchronization and revisioned, fine-grained local edits."""
import json
from pathlib import Path
from rdflib import Graph
from .maintenance import maintain,resume
from .edit_store import load,change,lock
from .local_edits import prepare,undo,resolve
from .publication import _verify


def configure(commands):
    sync=commands.add_parser('sync',help='synchronize the desired source list, preserve local edits and update configured applications')
    sync.add_argument('--workspace',type=Path,default=Path('data/inputs/vocabulary/maintenance.json'))
    sync.add_argument('--local',action='store_true',help='rebuild only from previously archived sources; no fetch or source parsing')
    sync.add_argument('--refresh-source',action='append',default=[],help='refresh a named source through its registered pipeline')
    sync.add_argument('--no-apps',action='store_true')
    status=commands.add_parser('status',help='last maintenance operation and pending local edit revision')
    status.add_argument('--workspace',type=Path,default=Path('data/inputs/vocabulary/maintenance.json'))
    cont=commands.add_parser('resume',help='retry failed maintenance or only unfinished application synchronization')
    cont.add_argument('--workspace',type=Path,default=Path('data/inputs/vocabulary/maintenance.json'));cont.add_argument('--operation')
    edit=commands.add_parser('edit',help='record local RDF edits without resynchronizing external sources')
    edit.add_argument('--workspace',type=Path,default=Path('data/inputs/vocabulary/maintenance.json'))
    actions=edit.add_subparsers(dest='edit_action',required=True)
    actions.add_parser('list')
    apply=actions.add_parser('apply');apply.add_argument('file',type=Path,help='JSON list of set/add/remove/create/delete operations')
    apply.add_argument('--dry-run',action='store_true')
    revoke=actions.add_parser('undo');revoke.add_argument('id')
    resolution=actions.add_parser('resolve');resolution.add_argument('file',type=Path,help='operation conflicts.json');resolution.add_argument('--id',required=True);resolution.add_argument('--choice',choices=['local','source'],required=True)
    for command in (apply,revoke,resolution):
        command.add_argument('--reason',required=True);command.add_argument('--expected-revision',type=int)
        command.add_argument('--record-only',action='store_true',help='save edit intent; publish later with sync --local')
        command.add_argument('--no-apps',action='store_true')


def workspace(path):
    path=Path(path).resolve();data=json.loads(path.read_bytes())
    if data.get('schema_version')!=1 or set(data)-{'schema_version','config','output','applications'}:raise ValueError('Invalid maintenance workspace')
    config=(path.parent/data['config']).resolve();root=(path.parent/data['output']).resolve()
    apps=[]
    for entry in data.get('applications',[]):
        apps.append({**entry,'directory':str((path.parent/entry['directory']).resolve())})
    return config,root,apps


def execute(args):
    config,root,apps=workspace(args.workspace)
    if args.command=='sync':return maintain(config,root,mode='local' if args.local else 'sync',refresh=args.refresh_source,applications=[] if args.no_apps else apps)
    if args.command=='resume':return resume(root,args.operation)
    settings=json.loads(config.read_bytes());edits=(config.parent/settings.get('local_edits','local-edits.json')).resolve()
    if args.command=='status':
        state=json.loads((root/'maintenance-status.json').read_bytes()) if (root/'maintenance-status.json').exists() else {'state':'not_started'}
        document=load(edits);published_path=root/'current/local-effects.json'
        published=json.loads(published_path.read_bytes())['revision'] if published_path.exists() else 0 if (root/'current').exists() else None
        return {'operation':state,'local_edits':str(edits),'local_revision':document['revision'],'published_local_revision':published,'pending_edits':document['revision']!=published if published is not None else bool(document['patches'])}
    if args.edit_action=='list':return load(edits)
    if edits.is_relative_to(root/'versions'):raise ValueError('Local edit storage must be outside immutable build versions')
    with lock(root/'.maintenance-lock'):
        current=(root/'current').resolve();_verify(current)
        visible=Graph().parse(current/'vocabulary.ttl')
        upstream=Graph().parse(current/('upstream.ttl' if (current/'upstream.ttl').exists() else 'vocabulary.ttl'))
        if args.edit_action=='apply':
            operations=json.loads(args.file.read_bytes())
            transform=lambda d:prepare(d,operations,upstream,visible,args.reason)
        elif args.edit_action=='undo':transform=lambda d:undo(d,args.id,args.reason)
        else:
            report=json.loads(args.file.read_bytes())
            matches=[c for c in report['conflicts'] if c['id']==args.id]
            if len(matches)!=1:raise ValueError('Select one conflict ID')
            transform=lambda d:resolve(d,matches[0],args.choice,args.reason)
        if getattr(args,'dry_run',False):
            candidate=transform(load(edits));return {'state':'preview','revision':candidate['revision'],'patches':candidate['patches']}
        doc=change(edits,transform,args.expected_revision)
    if args.record_only:return {'state':'recorded','revision':doc['revision'],'published':False}
    if args.edit_action=='resolve':
        status_file=args.file.resolve().parent/'status.json'
        prior=json.loads(status_file.read_bytes()) if status_file.exists() else {}
        return maintain(config,root,mode=prior.get('mode','sync'),refresh=prior.get('refresh',()),prepared_sources=prior.get('prepared'),applications=[] if args.no_apps else apps)
    return maintain(config,root,mode='local',applications=[] if args.no_apps else apps)
