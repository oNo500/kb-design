"""Extract missing Chinese preferred names from a pinned vocabulary snapshot."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
from rdflib import Graph,Literal,RDF,SKOS,URIRef

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('source',type=Path,help='immutable vocabulary.ttl baseline')
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--batch-size',type=int,default=200)
parser.add_argument('--model',required=True,help='model the dispatcher will explicitly select')
args=parser.parse_args()
if args.output.exists() or args.batch_size<1:raise ValueError('Use a new output directory and positive batch size')
source=args.source.resolve();raw=source.read_bytes();graph=Graph().parse(data=raw,format='turtle');rows=[]
priorities=[set(graph.objects(URIRef('urn:kb-vocab:group:'+name),SKOS.member)) for name in ('computer-science','cognitive-science','philosophy')]
objects=set(graph.subjects(RDF.type,SKOS.Concept))|set(graph.subjects(RDF.type,SKOS.Collection))|set(graph.subjects(RDF.type,SKOS.ConceptScheme))
for uri in objects:
    names=list(graph.objects(uri,SKOS.prefLabel))
    if any(isinstance(v,Literal) and (v.language or '').lower().split('-')[0]=='zh' for v in names):continue
    en=sorted((v for v in names if isinstance(v,Literal) and (v.language or '').lower().split('-')[0]=='en'),key=lambda v:((v.language or '').lower()!='en',str(v)))
    if not en:continue
    name=en[0];priority=next((i for i,group in enumerate(priorities) if uri in group),3)
    hints=sorted({str(v) for parent in graph.objects(uri,SKOS.broader) for v in graph.objects(parent,SKOS.prefLabel) if isinstance(v,Literal) and v.language=='en'})[:2]
    rows.append({'uri':str(uri),'en':str(name),'source_language':name.language,'priority':priority,'hint':'; '.join(hints)})
rows.sort(key=lambda row:(row['priority'],row['en'].casefold(),row['uri']))
for i,row in enumerate(rows):row['id']=f't{i:05d}'
manifest={'base':str(source.parent),'base_sha256':hashlib.sha256(raw).hexdigest(),'created_at':datetime.now(timezone.utc).isoformat(),'predicate':str(SKOS.prefLabel),'tasks':rows}
args.output.mkdir(parents=True);(args.output/'small-batches').mkdir()
task_raw=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode();(args.output/'tasks.json').write_bytes(task_raw)
for i,start in enumerate(range(0,len(rows),args.batch_size)):
    batch=[{k:v for k,v in row.items() if k in ('id','en','hint') and v} for row in rows[start:start+args.batch_size]]
    (args.output/'small-batches'/f'large{i:03d}.input.json').write_text(json.dumps(batch,ensure_ascii=False,separators=(',',':')))
(args.output/'orchestration.json').write_text(json.dumps({'model':args.model,'reasoning_effort':'low','translator_type':'ai','batch_size':args.batch_size,'task_manifest_sha256':hashlib.sha256(task_raw).hexdigest(),'owners':{}},indent=2)+'\n')
print(json.dumps({'tasks':len(rows),'batches':(len(rows)+args.batch_size-1)//args.batch_size,'output':str(args.output)}))
