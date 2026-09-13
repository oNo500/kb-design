"""Merge a small AI-translated batch against its pinned English baseline."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from rdflib import Graph, Literal, SKOS, URIRef
from rdflib.compare import isomorphic


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',type=Path,required=True)
    parser.add_argument('--batch',required=True)
    parser.add_argument('--limit',type=int,default=5)
    parser.add_argument('--model',required=True)
    parser.add_argument('--agent',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.limit<1 or args.output.exists():raise ValueError('Positive limit and new output directory required')
    taskraw=(args.run/'tasks.json').read_bytes();manifest=json.loads(taskraw)
    source=Path(manifest['base'])/'vocabulary.ttl';raw=source.read_bytes()
    if sha(raw)!=manifest['base_sha256']:raise ValueError('English baseline changed')
    batch=args.run/'small-batches'/f'{args.batch}.input.json'
    result=args.run/'small-batches'/f'{args.batch}.output.json'
    inputs=json.loads(batch.read_bytes());outputs=json.loads(result.read_bytes())
    expected={row['id'] for row in inputs}
    if len(expected)!=len(inputs) or set(outputs)!=expected:raise ValueError('Missing, extra or duplicate task IDs')
    if any(v is not None and (not isinstance(v,str) or not v.strip()) for v in outputs.values()):raise ValueError('Invalid translation value')
    tasks={row['id']:row for row in manifest['tasks']}
    graph=Graph().parse(data=raw,format='turtle');delta=Graph();delta.bind('skos',SKOS)
    selected=[]
    for row in inputs[:args.limit]:
        task=tasks[row['id']]
        if row['en']!=task['en']:raise ValueError('Batch source text differs from task manifest')
        uri=URIRef(task['uri']);original=Literal(task['en'],lang=task['source_language'])
        if (uri,SKOS.prefLabel,original) not in graph:raise ValueError('Source label does not match baseline node')
        if any((v.language or '').lower().split('-')[0]=='zh' for v in graph.objects(uri,SKOS.prefLabel)):
            raise ValueError('Cannot overwrite existing Chinese label')
        translation=outputs[row['id']]
        if translation is not None:delta.add((uri,SKOS.prefLabel,Literal(translation,lang='zh')))
        selected.append(dict(task,zh=translation))
    merged=graph+delta
    # Exact write-set proof: only these Chinese labels were added.
    if set(merged)-set(graph)!=set(delta) or not set(graph)<=set(merged):raise ValueError('Unexpected graph mutation')
    args.output.mkdir(parents=True)
    delta.serialize(args.output/'translations.zh.ttl',format='turtle')
    merged.serialize(args.output/'vocabulary.multilingual.ttl',format='turtle')
    if not isomorphic(Graph().parse(args.output/'vocabulary.multilingual.ttl'),merged):raise ValueError('Turtle round-trip changed data')
    metadata={'schema_version':1,'translator_type':'ai','model':args.model,'agent':args.agent,
              'output_written_at':datetime.fromtimestamp(result.stat().st_mtime,timezone.utc).isoformat(),
              'metadata_recorded_at':datetime.now(timezone.utc).isoformat(),
              'base':manifest['base'],'base_sha256':sha(raw),'task_manifest_sha256':sha(taskraw),
              'batch':args.batch,'batch_input_sha256':sha(batch.read_bytes()),'batch_output_sha256':sha(result.read_bytes()),
              'task_ids':[row['id'] for row in selected],'notice':'AI 翻译，仅用于展示，未核对权威中文术语',
              'translated':len(delta),'retained_original':len(selected)-len(delta),
              'files':{name:sha((args.output/name).read_bytes()) for name in ('translations.zh.ttl','vocabulary.multilingual.ttl')}}
    (args.output/'batch-metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    (args.output/'sample.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
    if source.read_bytes()!=raw:raise ValueError('Baseline changed during merge')
    print(json.dumps({'translated':len(delta),'source_unchanged':True,'output':str(args.output),'sample':[(r['en'],r['zh']) for r in selected]},ensure_ascii=False))

if __name__=='__main__':main()
