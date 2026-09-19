"""一次性验收：共享 SHACL，明确指定已生成名称的 LocalLabel 范围。"""
from pathlib import Path
from collections import Counter
from hashlib import sha256
from importlib.metadata import version
import json
from time import perf_counter
from rdflib import Graph,Namespace,RDF,URIRef
from rdflib.namespace import SH
from pyshacl import validate
from kb_vocab_shacl import read_shapes
from kb_vocab_ccs.storage import new_directory,write_json

ROOT=Path(__file__).resolve().parent
XL=Namespace('http://www.w3.org/2008/05/skos-xl#')
RULE=Namespace('urn:kb-vocab-shacl:')
source=json.loads((ROOT/'source.json').read_text())
raw=(ROOT/'result/vocabulary.multilingual.ttl').read_bytes()
data=Graph().parse(data=raw,format='turtle')
original_labels=json.loads((Path(source['input']).parent/'adaptations.json').read_text())['labels']
new_labels=json.loads((ROOT/'result/name-registry.json').read_text())
labels={URIRef(r['label']) for r in original_labels}|{URIRef(r['label_iri']) for r in new_labels}
assert labels==set(data.subjects(RDF.type,XL.Label))
profiles={};start=perf_counter()
with new_directory(ROOT/'validation') as out:
 for profile in ['structure','target']:
  print('正在运行',profile,flush=True);begun=perf_counter()
  rules=Graph().parse(data=read_shapes(profile),format='turtle')
  for label in labels:rules.add((RULE.LocalLabel,SH.targetNode,label))
  shape_raw=rules.serialize(format='turtle',encoding='utf-8');(out/f'{profile}-shapes.ttl').write_bytes(shape_raw)
  try:
   conforms,report,text=validate(data,shacl_graph=rules,inference='none',allow_warnings=False,allow_infos=False,abort_on_first=False)
   if not isinstance(report,Graph):raise ValueError(str(report))
  except Exception as exc:
   write_json(out/'error.json',{'profile':profile,'error':str(exc),'conforms':None})
   profiles[profile]={'conforms':None,'error':str(exc)}
   break
  report.serialize(destination=out/f'{profile}-report.ttl',format='turtle')
  (out/f'{profile}-report.txt').write_text(text)
  results=[]
  for r in report.subjects(RDF.type,SH.ValidationResult):
   results.append({key:str(report.value(r,SH[key])) for key in ['sourceShape','resultSeverity','focusNode','resultPath','value']})
  write_json(out/f'{profile}-results.json',results)
  profiles[profile]={'conforms':bool(conforms),'results':len(results),'seconds':round(perf_counter()-begun,3),
                    'local_label_targets':len(labels),'shapes_sha256':sha256(shape_raw).hexdigest(),
                    'by_rule':dict(Counter(r['sourceShape'] for r in results))}
  print(profile,profiles[profile],flush=True)
 summary={'conforms':len(profiles)==2 and all(r['conforms'] is True for r in profiles.values()),'profiles':profiles,
          'input_sha256':sha256(raw).hexdigest(),'seconds':round(perf_counter()-start,3),
          'generated_label_scope':'英文原构建名称登记与本次中文名称登记的并集，全部明确指定为 LocalLabel',
          'other_local_conditions_executed':False,'human_semantic_review':False,
          'versions':{n:version(n) for n in ['rdflib','pyshacl','kb-vocab-shacl']}}
 write_json(out/'summary.json',summary)
 lines=['# 中文词表校验','','| 规则组 | 通过 | 问题数 |','| --- | --- | ---: |']
 for key,r in profiles.items():lines.append(f"| {key} | {r['conforms']} | {r.get('results','未完成')} |")
 lines+=['',f"耗时 {summary['seconds']} 秒。",'',
         '名称登记中的全部生成名称按 LocalLabel 检查；其他本地条件未指定对象，未执行。',
         '机械校验不证明译文准确；所有中文译名仍为模型知识初译，未经过人工审核。','']
 (out/'校验汇总.md').write_text('\n'.join(lines))
 print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
if not summary['conforms']:
 raise SystemExit(2 if any(r['conforms'] is None for r in profiles.values()) else 1)
