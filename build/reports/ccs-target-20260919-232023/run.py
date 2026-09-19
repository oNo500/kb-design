from pathlib import Path
import json, hashlib, time
from datetime import datetime
from collections import Counter, defaultdict
from rdflib import Graph, Namespace
from pyshacl import validate
from kb_vocab_shacl import read_shapes
SH=Namespace('http://www.w3.org/ns/shacl#')
source=Path('/Users/xiu/code/kb-design/output/vocabulary/sources/ccs-2012/cli99-48644c2ed653/ccs-2012.ttl')
out=Path('/Users/xiu/code/kb-design/build/reports')/('ccs-target-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
out.mkdir(parents=True,exist_ok=False)
Path('/tmp/ccs-target-report-path').write_text(str(out))
raw=source.read_bytes(); shapes=read_shapes('target')
(out/'shapes.ttl').write_text(shapes)
start=time.monotonic()
print('Report directory:',out,flush=True)
data=Graph().parse(data=raw,format='turtle',publicID=source.as_uri())
rules=Graph().parse(data=shapes,format='turtle')
try:
    conforms,report,report_text=validate(data,shacl_graph=rules,inference='none',advanced=False,allow_infos=False,allow_warnings=False,abort_on_first=False)
except Exception as exc:
    (out/'error.json').write_text(json.dumps({'error':repr(exc),'seconds':time.monotonic()-start},indent=2))
    raise
report.serialize(destination=out/'report.ttl',format='turtle')
(out/'report.txt').write_text(report_text)
results=[]
for r in report.subjects(None,SH.ValidationResult):
    row={k:str(report.value(r,SH[k])) if report.value(r,SH[k]) is not None else None for k in ['sourceShape','sourceConstraintComponent','resultSeverity','focusNode','resultPath','value']}
    row['messages']=[str(x) for x in report.objects(r,SH.resultMessage)]
    results.append(row)
counts=Counter((r['sourceShape'],r['resultSeverity']) for r in results)
summary={'conforms':bool(conforms),'profile':'target','seconds':round(time.monotonic()-start,3),'source':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),'shapes_sha256':hashlib.sha256(shapes.encode()).hexdigest(),'inference':'none','conditional_targets_added':False,'results':len(results),'by_severity':dict(Counter(r['resultSeverity'] for r in results)),'by_rule':[{'rule':k[0],'severity':k[1],'count':v,'focus_nodes':len({r['focusNode'] for r in results if r['sourceShape']==k[0] and r['resultSeverity']==k[1]}),'samples':[r for r in results if r['sourceShape']==k[0] and r['resultSeverity']==k[1]][:2]} for k,v in sorted(counts.items())]}
assert source.read_bytes()==raw
(out/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
