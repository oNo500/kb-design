"""Reuse packaged SHACL; reports never imply unexecuted checks have passed."""
from collections import Counter
from hashlib import sha256
from importlib.metadata import version
import json
from time import perf_counter

from kb_vocab_shacl import read_shapes
from kb_vocab_shacl.inventory import inventory
from kb_vocab_shacl.report import markdown
from kb_vocab_shacl.structure import load_structure
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, URIRef
from rdflib.namespace import SH

from .storage import new_directory, write_json

RULE = Namespace('urn:kb-vocab-shacl:')


def load_input(path):
    """A build directory carries checked evidence for generated Label targets."""
    labels = []
    if path.is_dir():
        manifest = json.loads((path/'manifest.json').read_bytes())
        required = {'source.xml','adapted.xml','source.ttl','vocabulary.ttl','config.json','adaptations.json'}
        if set(manifest['files']) != required:
            raise ValueError('构建清单写集不符合当前合同')
        for name, digest in manifest['files'].items():
            if sha256((path/name).read_bytes()).hexdigest() != digest:
                raise ValueError(f'构建文件已改变，请重新生成：{name}')
        additions = json.loads((path/'adaptations.json').read_bytes())
        labels = [URIRef(row['label']) for row in additions['labels']]
        path = path/'vocabulary.ttl'
    raw = path.read_bytes()
    data = Graph().parse(data=raw,format='turtle',publicID=path.resolve().as_uri())
    return data, raw, labels


def field_inventory(path, output=None):
    start = perf_counter()
    data, raw, labels = load_input(path)
    shapes, roots = load_structure()
    for label in labels:
        shapes.add((RULE.LocalLabel,SH.targetNode,label))
    result = inventory(data,structure=shapes,roots=roots)
    result['run'] = {'input':str(path.resolve()),'input_sha256':sha256(raw).hexdigest(),'elapsed_seconds':perf_counter()-start,
                     'shacl_validation_executed':False}
    text = markdown(result)
    if output:
        with new_directory(output) as stage:
            write_json(stage/'inventory.json',result)
            (stage/'统计-词表字段.md').write_text(text,encoding='utf-8')
    return text


def check(path, output, profile='all'):
    start = perf_counter()
    data, raw, labels = load_input(path)
    profiles = ['structure','target'] if profile == 'all' else [profile]
    summaries = {}
    combined = True
    exit_code = 0
    with new_directory(output) as stage:
        for selected in profiles:
            print(f'正在校验 {selected}…',flush=True)
            begun = perf_counter()
            rules = Graph().parse(data=read_shapes(selected),format='turtle')
            # Only generated Labels have a confirmed local origin in this bundle.
            if selected != 'standard':
                for label in labels:
                    rules.add((RULE.LocalLabel,SH.targetNode,label))
            shapes_raw = rules.serialize(format='turtle',encoding='utf-8')
            (stage/f'{selected}-shapes.ttl').write_bytes(shapes_raw)
            try:
                conforms, report, report_text = validate(
                    data,shacl_graph=rules,inference='none',advanced=False,
                    allow_infos=False,allow_warnings=False,abort_on_first=False,
                )
                if not isinstance(report,Graph):
                    raise RuntimeError(str(report))
            except Exception as error:
                summaries[selected] = {'status':'engine_error','conforms':None,'error':str(error),
                                       'seconds':round(perf_counter()-begun,3)}
                combined = False
                exit_code = 2
                break
            report.serialize(destination=stage/f'{selected}-report.ttl',format='turtle')
            (stage/f'{selected}-report.txt').write_text(report_text,encoding='utf-8')
            results = []
            for result in report.subjects(RDF.type,SH.ValidationResult):
                row = {key:report.value(result,SH[key]).n3() if report.value(result,SH[key]) is not None else None
                       for key in ('focusNode','resultPath','value')}
                row.update({key:str(report.value(result,SH[key]))
                            for key in ('sourceShape','sourceConstraintComponent','resultSeverity')})
                row['messages'] = sorted(str(v) for v in report.objects(result,SH.resultMessage))
                results.append(row)
            results.sort(key=lambda x:json.dumps(x,sort_keys=True))
            write_json(stage/f'{selected}-results.json',results)
            count = Counter((r['sourceShape'],r['resultSeverity']) for r in results)
            summaries[selected] = {
                'status':'completed','conforms':bool(conforms),'seconds':round(perf_counter()-begun,3),
                'results':len(results),'by_severity':dict(Counter(r['resultSeverity'] for r in results)),
                'by_rule':[{'rule':rule,'severity':severity,'count':number}
                           for (rule,severity),number in sorted(count.items())],
                'shapes_sha256':sha256(shapes_raw).hexdigest(),
                'local_label_targets':len(labels) if selected != 'standard' else 0,
            }
            combined = combined and bool(conforms)
            if not conforms:
                exit_code = 1
        summary = {'conforms':combined if exit_code != 2 else None,'profiles':summaries,
                   'input_sha256':sha256(raw).hexdigest(),'seconds':round(perf_counter()-start,3),
                   'inference':'none','allow_warnings':False,'allow_infos':False,
                   'other_local_conditions_executed':False,'semantic_review_executed':False,
                   'versions':{name:version(name) for name in ('rdflib','pyshacl','kb-vocab-shacl','kb-vocab-ccs')}}
        write_json(stage/'summary.json',summary)
        text = render_summary(summary)
        (stage/'校验汇总.md').write_text(text,encoding='utf-8')
    return exit_code, text


def render_summary(summary):
    status = '通过' if summary['conforms'] is True else ('未通过' if summary['conforms'] is False else '执行失败')
    lines = ['# CCS 校验结果','',f"结果：{status}。耗时 {summary['seconds']} 秒。",'',
             '| 规则组 | 状态 | 结果数 |','| --- | --- | ---: |']
    for profile, result in summary['profiles'].items():
        state = '通过' if result['conforms'] is True else ('未通过' if result['conforms'] is False else '执行失败')
        lines.append(f"| {profile} | {state} | {result.get('results','—')} |")
    lines.extend(['','## 问题汇总','','| 规则组 | 规则 | 级别 | 数量 |','| --- | --- | --- | ---: |'])
    for profile, result in summary['profiles'].items():
        for row in result.get('by_rule',[]):
            lines.append(f"| {profile} | {row['rule']} | {row['severity'].split('#')[-1]} | {row['count']} |")
        if result.get('error'):
            lines.extend(['',f"{profile} 引擎错误：{result['error']}"])
    lines.extend(['','## 检查边界','',
                  '不同规则组可能报告同一问题，不相加计算独立问题数量。所有级别按严格模式判定。',
                  '构建目录中的生成名称按 LocalLabel 检查；直接传 TTL 时不推定本地来源。其他本地条件未指定对象，未执行。',
                  '本结果不代替名称历史、采纳记录、语义审查及完整设计符合性判断。',''])
    return '\n'.join(lines)
