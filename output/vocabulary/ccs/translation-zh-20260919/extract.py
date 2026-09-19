from pathlib import Path
from rdflib import Graph,RDF,SKOS
from hashlib import sha256
import json
root=Path('/Users/xiu/code/kb-design/output/vocabulary/ccs/translation-zh-20260919')
source=Path('/Users/xiu/code/kb-design/output/vocabulary/ccs/build-48644c2ed653/vocabulary.ttl')
g=Graph().parse(source)
concepts=set(g.subjects(RDF.type,SKOS.Concept))
def name(n): return str(next(g.objects(n,SKOS.prefLabel)))
proper=next(n for n in concepts if str(n).endswith('#10011641'))
proper_set=set(); stack=[proper]
while stack:
 n=stack.pop()
 if n in proper_set:continue
 proper_set.add(n);stack.extend(g.objects(n,SKOS.narrower))
records=[]
for n in sorted(concepts,key=str):
 labels=list(g.objects(n,SKOS.prefLabel));assert len(labels)==1
 records.append({'id':str(n).split('#')[-1],'iri':str(n),'en':str(labels[0]),'source_language':labels[0].language,'parents':sorted(name(p) for p in g.objects(n,SKOS.broader)),'scope_notes':[str(v) for v in g.objects(n,SKOS.scopeNote)],'proper_noun_branch':n in proper_set})
(root/'tasks.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
normal=[r for r in records if not r['proper_noun_branch']];proper_records=[r for r in records if r['proper_noun_branch']]
batches=[normal[i:i+240] for i in range(0,len(normal),240)]+[proper_records]
for i,rows in enumerate(batches,1):
 (root/'batches'/f'{i:02}-input.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(root/'source.json').write_text(json.dumps({'input':str(source),'sha256':sha256(source.read_bytes()).hexdigest(),'scope':'Concept skos:prefLabel only','target_language':'zh','count':len(records),'batch_counts':[len(b) for b in batches]},indent=2)+'\n')
print(len(records),[len(b) for b in batches])
