"""Local Turtle/SKOS evaluation import, queries and validation."""
import argparse
import json
from pathlib import Path
import sys

from rdflib import Graph
from rdflib.plugins.parsers.notation3 import BadSyntax
from kb_vocab.query import describe_concept, find_concepts, select_query
from kb_vocab.validation import validate_graph


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    from kb_vocab.review_cli import configure, execute
    configure(commands)
    importer=commands.add_parser('import-ieee',help='create a new evaluation projection; does not update formal data')
    importer.add_argument('source',type=Path)
    importer.add_argument('--output',type=Path,required=True)
    importer.add_argument('--identities',type=Path,help='verified prior source Turtle; preserve concept URIs across snapshots')
    cognitive=commands.add_parser('import-cognitive-atlas',help='convert verified Cognitive Atlas transcription to evaluation RDF/SKOS')
    cognitive.add_argument('source',type=Path)
    cognitive.add_argument('--output',type=Path,required=True)
    cognitive.add_argument('--identities',type=Path)
    for name in ('msc', 'eric', 'philpapers', 'unesco'):
        command = commands.add_parser('import-' + name, help='create an independent evaluation bundle')
        command.add_argument('source', type=Path)
        command.add_argument('--output', type=Path, required=True)
        if name=='eric':command.add_argument('--identities',type=Path)
    system=commands.add_parser('build-system',help='generate complete source-preserving domain vocabularies without review')
    system.add_argument('--config',type=Path,required=True)
    destination=system.add_mutually_exclusive_group(required=True)
    destination.add_argument('--output',type=Path,help='create a standalone build without switching current')
    destination.add_argument('--output-root',type=Path,help='create a version and atomically switch current')
    system.add_argument('--build-id',help='optional version directory name, requires --output-root')
    diff=commands.add_parser('diff',help='compare RDF versions by concept and field')
    diff.add_argument('before',type=Path);diff.add_argument('after',type=Path)
    activation=commands.add_parser('activate-system',help='verify and switch current to a retained version')
    activation.add_argument('--output-root',type=Path,required=True)
    activation.add_argument('--version',required=True)
    check=commands.add_parser('validate',help='supported SKOS checks and explicit-type profile')
    check.add_argument('file',type=Path)
    context=commands.add_parser('label-context',help='read the exact context snapshot for a proposed label; does not approve it')
    context.add_argument('file',type=Path);context.add_argument('uri')
    show=commands.add_parser('show',help='describe one concept by URI or exact label')
    show.add_argument('file',type=Path);show.add_argument('concept')
    find=commands.add_parser('find',help='search labels in the local graph')
    find.add_argument('file',type=Path);find.add_argument('text');find.add_argument('--limit',type=int,default=20)
    query=commands.add_parser('query',help='local read-only SPARQL SELECT; no SERVICE/FROM/UPDATE')
    query.add_argument('file',type=Path)
    text=query.add_mutually_exclusive_group(required=True)
    text.add_argument('--sparql');text.add_argument('--query-file',type=Path)
    args=parser.parse_args(argv)
    try:
        if args.command == 'build-system':
            from kb_vocab.system_build import build_system
            if args.output_root:
                from kb_vocab.publication import build_versioned
                result = build_versioned(args.config,args.output_root,args.build_id)
            else:
                if args.build_id: raise ValueError('--build-id requires --output-root')
                result = build_system(args.config,args.output)
        elif args.command == 'diff':
            from kb_vocab.version_diff import compare_files
            result=compare_files(args.before,args.after)
        elif args.command == 'activate-system':
            from kb_vocab.publication import activate_version
            result = activate_version(args.output_root,args.version)
        elif args.command == 'review':
            result = execute(args)
        elif args.command in ('import-msc', 'import-eric', 'import-philpapers', 'import-unesco'):
            from importlib import import_module
            name = args.command.removeprefix('import-')
            result = getattr(import_module('kb_vocab.' + name), 'import_' + name)(args.source, args.output, **({'identity_file':args.identities} if name=='eric' else {}))
        elif args.command=='import-cognitive-atlas':
            from kb_vocab.cognitive_atlas import import_cognitive
            result=import_cognitive(args.source,args.output,args.identities)
        elif args.command=='import-ieee':
            from kb_vocab.ieee import import_ieee
            result=import_ieee(args.source,args.output,identity_file=args.identities)
        else:
            graph=Graph().parse(data=args.file.read_text(),format='turtle',publicID=args.file.absolute().as_uri())
            if args.command=='label-context':
                from kb_vocab.labels import label_context
                result=label_context(graph,args.uri)
            elif args.command=='validate':result=validate_graph(graph)
            elif args.command=='show':result=describe_concept(graph,args.concept)
            elif args.command=='find':
                if args.limit<1:raise ValueError('limit must be positive')
                rows=find_concepts(graph,args.text);result={'matches':len(rows),'concepts':rows[:args.limit]}
            else:
                result=select_query(graph,args.sparql if args.sparql is not None else args.query_file.read_text())
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 1 if args.command=='validate' and not result['valid'] else 0
    except (OSError,ValueError,KeyError,BadSyntax) as exc:
        print(json.dumps({'error':str(exc)},ensure_ascii=False),file=sys.stderr)
        return 1
