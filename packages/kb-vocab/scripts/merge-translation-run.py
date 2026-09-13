"""Validate completed AI batches and generate a separate bilingual vocabulary."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from rdflib import Graph, Literal, RDF, SKOS, URIRef
from rdflib.compare import isomorphic


def sha(raw):return hashlib.sha256(raw).hexdigest()

def strict_pairs(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError(f'Duplicate JSON key: {key}')
        result[key]=value
    return result

def read(path):return json.loads(path.read_bytes(),object_pairs_hook=strict_pairs)

def collect(run):
    manifest=read(run/'tasks.json');ownership=read(run/'orchestration.json')
    if ownership.get('task_manifest_sha256')!=sha((run/'tasks.json').read_bytes()):raise ValueError('Task manifest differs from dispatched baseline')
    tasks={row['id']:row for row in manifest['tasks']};seen=set();translations={};batches={};missing=[];flags=[]
    for inp in sorted((run/'small-batches').glob('*.input.json')):
        bid=inp.name.split('.')[0];items=read(inp);out=inp.with_name(bid+'.output.json')
        if not out.exists():missing.append(bid);continue
        values=read(out)
        if isinstance(values,list):
            if any(not isinstance(row,dict) or set(row)!={'id','zh'} for row in values):raise ValueError(f'Batch {bid}: invalid list format')
            if len({row['id'] for row in values})!=len(values):raise ValueError(f'Batch {bid}: duplicate IDs')
            values={row['id']:row['zh'] for row in values}
        if not isinstance(values,dict) or set(values)!={row['id'] for row in items}:raise ValueError(f'Batch {bid}: incorrect ID set')
        for row in items:
            tid=row['id'];task=tasks[tid]
            if tid in seen or row['en']!=task['en']:raise ValueError(f'Batch {bid}: stale or duplicate task')
            seen.add(tid);value=values[tid]
            if value is not None and (not isinstance(value,str) or not value.strip()):raise ValueError(f'Batch {bid}: invalid translation')
            if value and (value.startswith(('术语：','中文显示：')) or re.search(r'[A-Za-z]+(?:\s+[A-Za-z]+){3,}',value)):
                flags.append({'id':tid,'batch':bid,'en':row['en'],'zh':value})
            # Proper names/acronyms retained unchanged must not masquerade as Chinese.
            if value and not re.search(r'[\u3400-\u9fff]',value):value=None
            translations[tid]={'zh':value,'batch':bid}
        batches[bid]={'translator_type':'ai','model':ownership['model'],'reasoning_effort':ownership['reasoning_effort'],
                      'agent':ownership['owners'][bid],'output_written_at':datetime.fromtimestamp(out.stat().st_mtime,timezone.utc).isoformat(),
                      'input_sha256':sha(inp.read_bytes()),'output_sha256':sha(out.read_bytes()),'items':len(items)}
    corrected=set()
    for inp in sorted((run/'corrections').glob('*.input.json')):
        bid=inp.name.split('.')[0];items=read(inp);out=inp.with_name(bid+'.output.json')
        if not out.exists():missing.append(bid);continue
        values=read(out)
        if isinstance(values,list):
            if any(not isinstance(row,dict) or set(row)!={'id','zh'} for row in values):raise ValueError('Invalid correction format')
            if len({row['id'] for row in values})!=len(values):raise ValueError('Duplicate correction IDs')
            values={row['id']:row['zh'] for row in values}
        if set(values)!={row['id'] for row in items}:raise ValueError('Correction IDs differ from input')
        for row in items:
            tid=row['id'];value=values[tid]
            if tid not in translations or tid in corrected or row['en']!=tasks[tid]['en']:raise ValueError('Invalid correction target')
            if value is not None and (not isinstance(value,str) or not value.strip()):raise ValueError('Invalid corrected label')
            if value and not re.search(r'[\u3400-\u9fff]',value):value=None
            translations[tid]={'zh':value,'batch':bid};corrected.add(tid)
        batches[bid]={'translator_type':'ai','model':ownership['model'],'reasoning_effort':ownership['reasoning_effort'],
                      'agent':ownership['owners'][bid],'output_written_at':datetime.fromtimestamp(out.stat().st_mtime,timezone.utc).isoformat(),
                      'input_sha256':sha(inp.read_bytes()),'output_sha256':sha(out.read_bytes()),'items':len(items),'purpose':'repair English remnants'}
    flags=[]
    for tid,row in translations.items():
        value=row['zh']
        if value and (value.startswith(('术语：','中文显示：')) or re.search(r'[A-Za-z]+(?:\s+[A-Za-z]+){3,}',value)):
            flags.append({'id':tid,'batch':row['batch'],'en':tasks[tid]['en'],'zh':value})
    return manifest,translations,batches,missing,flags

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run',type=Path,required=True)
    parser.add_argument('--output',type=Path);parser.add_argument('--allow-partial',action='store_true')
    args=parser.parse_args();manifest,translations,batches,missing,flags=collect(args.run)
    status={'completed_batches':len(batches),'missing_batches':missing,'completed_items':len(translations),
            'total_items':len(manifest['tasks']),'retained_original':sum(r['zh'] is None for r in translations.values()),'flags':flags}
    (args.run/'progress.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
    if not args.output:
        print(json.dumps({**status,'missing_batches':len(missing),'flags':len(flags)},ensure_ascii=False));return
    if args.output.exists():raise ValueError('Output directory must be new')
    if missing and not args.allow_partial:raise ValueError('Not all batches are complete')
    if flags:raise ValueError('Unresolved English remnants must be checked before merging')
    raw=(Path(manifest['base'])/'vocabulary.ttl').read_bytes()
    if sha(raw)!=manifest['base_sha256']:raise ValueError('Pinned baseline changed')
    graph=Graph().parse(data=raw,format='turtle');delta=Graph();delta.bind('skos',SKOS);evidence=[]
    for task in manifest['tasks']:
        result=translations.get(task['id']);uri=URIRef(task['uri'])
        if (uri,SKOS.prefLabel,Literal(task['en'],lang=task['source_language'])) not in graph:raise ValueError('Task no longer matches its baseline')
        if not result or result['zh'] is None:continue
        if any((v.language or '').lower().split('-')[0]=='zh' for v in graph.objects(uri,SKOS.prefLabel)):raise ValueError('Existing Chinese name cannot be overwritten')
        delta.add((uri,SKOS.prefLabel,Literal(result['zh'],lang='zh')))
        evidence.append({'uri':str(uri),'property':str(SKOS.prefLabel),'language':'zh','label':result['zh'],'batch':result['batch']})
    merged=graph+delta
    if set(merged)-set(graph)!=set(delta) or not set(graph)<=set(merged):raise ValueError('Unexpected graph mutation')
    args.output.mkdir(parents=True)
    delta.serialize(args.output/'translations.zh.ttl',format='turtle')
    merged.serialize(args.output/'vocabulary.multilingual.ttl',format='turtle')
    if not isomorphic(merged,Graph().parse(args.output/'vocabulary.multilingual.ttl')):raise ValueError('Round-trip mismatch')
    meta={'schema_version':2,'target_schemes':sorted(map(str,graph.subjects(RDF.type,SKOS.ConceptScheme))),'base':manifest['base'],'base_sha256':sha(raw),'task_manifest_sha256':sha((args.run/'tasks.json').read_bytes()),
          'vocabulary_sha256':sha((args.output/'vocabulary.multilingual.ttl').read_bytes()),'batches':batches,'labels':evidence,
          'notice':'AI 翻译，仅用于展示，未核对权威中文术语','complete':not missing}
    (args.output/'label-provenance.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    (args.output/'report.json').write_text(json.dumps({**status,'added_chinese_labels':len(delta),'source_unchanged':True},ensure_ascii=False,indent=2)+'\n')
    if (Path(manifest['base'])/'vocabulary.ttl').read_bytes()!=raw:raise ValueError('Baseline changed during merge')
    (args.output/'manifest.json').write_text(json.dumps({'kind':'bilingual-display','base_sha256':sha(raw),'files':{p.name:sha(p.read_bytes()) for p in args.output.iterdir()}},indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'added_chinese_labels':len(delta),'complete':not missing},ensure_ascii=False))
if __name__=='__main__':main()
