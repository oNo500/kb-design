"""Shared field inventory and SHACL checks with visible scope and approval state."""
from collections import Counter
from hashlib import sha256
from importlib.metadata import version
from time import perf_counter

from kb_vocab_shacl import read_shapes
from kb_vocab_shacl.structure import load_structure
from kb_vocab_shacl.inventory import inventory
from kb_vocab_shacl.report import markdown
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, SKOS, URIRef
from rdflib.namespace import SH

from .workflow import XL, read_json, write_json, output_directory

RULE=Namespace('urn:kb-vocab-shacl:')
RESOURCE=Namespace('urn:kb-vocab-shacl:resource:')


def read_bundle(path):
    manifest=read_json(path/'manifest.json')
    expected={'vocabulary.ttl','input.json','sources.json','evidence.json','source-receipts.json','审阅清单.md'}
    if manifest.get('format_version')!=1 or set(manifest['files'])!=expected:raise ValueError('构建清单无效')
    for name,digest in manifest['files'].items():
        if sha256((path/name).read_bytes()).hexdigest()!=digest:raise ValueError(f'生成文件已改变：{name}，请从输入重建')
    data=Graph().parse(data=(path/'vocabulary.ttl').read_bytes(),format='turtle')
    for key,cls in [('concepts',SKOS.Concept),('labels',XL.Label),('collections',SKOS.Collection)]:
        if set(map(str,data.subjects(RDF.type,cls)))!=set(manifest[key]):raise ValueError(f'{key} 与构建登记不一致')
    return data,manifest


def local_targets(shapes,manifest,structure=False):
    for key,shape in [('concepts',RULE.LocalConcept),('labels',RULE.LocalLabel),('collections',RULE.LocalCollection),('notes',RULE.LocalNote)]:
        for node in manifest[key]:shapes.add((shape,SH.targetNode,URIRef(node)))
    if structure:
        # Applicability is a description on a note; reuse the existing literal constraint.
        shapes.add((RESOURCE.Note,SH.property,RULE.TextMetadata_dcterms_description))
        shapes.add((RESOURCE.Note,SH.node,URIRef('urn:kb-vocab-shacl:common:Notes')))
        for node in manifest['notes']:shapes.add((RESOURCE.Note,SH.targetNode,URIRef(node)))


def inspect_bundle(path,output,*,run_checks=False):
    start=perf_counter();data,manifest=read_bundle(path)
    shapes,roots=load_structure();local_targets(shapes,manifest,structure=True)
    stats=inventory(data,structure=shapes,roots=roots)
    stats['run']={'input':str((path/'vocabulary.ttl').resolve()),'input_sha256':manifest['files']['vocabulary.ttl'],
                  'elapsed_seconds':perf_counter()-start,'shacl_validation_executed':False}
    uncovered=sorted(set(stats['unclassified_subjects'])-set(manifest['auxiliary_resources']))
    unlisted=sorted(set(map(str,data.predicates()))-{r['field'] for r in stats['fields']})
    report={'input_sha256':manifest['files']['vocabulary.ttl'],'input_approved':manifest['input_approved'],'published':False,
            'semantic_review_executed':False,'conforms':None,'coverage':{'uncovered_subjects':uncovered,'unlisted_predicates':unlisted,
            'resources':{r['type']:r['objects'] for r in stats['resources']},
            'auxiliary_sources':len(manifest['auxiliary_resources']),
            'local_conditions_executed':['LocalConcept','LocalLabel','LocalCollection','LocalNote'] if run_checks else [],
            'not_checked':['语义、译名及关系是否准确','依据是否足以批准采用','本地日期条件','完整语言标签登记有效性']},
            'field_summary':[{'type':r['type'],'label':r['label'],'objects':r['objects'],'fields':len(r['fields']),
                'fully_present':sum(f['absent']==0 for f in r['fields']),
                'partly_missing':sum(0<f['absent']<r['objects'] for f in r['fields']),
                'fully_absent':sum(f['present']==0 for f in r['fields'])}
                for r in stats['resources'] if r['objects']],
            'profiles':{},'versions':{name:version(name) for name in ('kb-vocab-writing','kb-vocab-shacl','rdflib','pyshacl')}}
    with output_directory(output) as stage:
        write_json(stage/'inventory.json',stats);(stage/'字段统计.md').write_text(markdown(stats),encoding='utf-8')
        if run_checks:
            conforms_all=not uncovered and not unlisted and bool(manifest['concepts'])
            for profile in ('structure','target'):
                rules=Graph().parse(data=read_shapes(profile),format='turtle');local_targets(rules,manifest,structure=profile=='structure')
                raw=rules.serialize(format='turtle',encoding='utf-8');(stage/f'{profile}-shapes.ttl').write_bytes(raw)
                print(f'校验 {profile}…',flush=True)
                conforms,result,text=validate(data,shacl_graph=rules,inference='none',allow_infos=False,allow_warnings=False,abort_on_first=False)
                if not isinstance(result,Graph):raise ValueError(str(result))
                result.serialize(destination=stage/f'{profile}-report.ttl',format='turtle')
                (stage/f'{profile}-report.txt').write_text(text,encoding='utf-8')
                counts=Counter(str(result.value(node,SH.resultSeverity)).rsplit('#',1)[-1] for node in result.subjects(RDF.type,SH.ValidationResult))
                report['profiles'][profile]={'conforms':bool(conforms),'counts':dict(counts),
                    'declared_warning_shapes':len(set(rules.subjects(SH.severity,SH.Warning))),
                    'declared_info_shapes':len(set(rules.subjects(SH.severity,SH.Info))),
                    'shapes_sha256':sha256(raw).hexdigest()}
                conforms_all=conforms_all and bool(conforms)
            report['conforms']=conforms_all
        report['seconds']=round(perf_counter()-start,3)
        write_json(stage/'report.json',report)
        (stage/'检查摘要.md').write_text(summary_text(report),encoding='utf-8')
    return report


def summary_text(report):
    lines=['# 写作词表检查','',f"输入确认：{'已确认' if report['input_approved'] else '未确认，审阅样稿'}。机械检查不会批准概念或写作规则。",'']
    lines.extend(['| 对象 | 数量 | 字段种类 | 全部填写 | 部分缺失 | 全部缺失 |',
                  '| --- | ---: | ---: | ---: | ---: | ---: |'])
    for row in report['field_summary']:
        lines.append(f"| {row['label']} | {row['objects']} | {row['fields']} | {row['fully_present']} | {row['partly_missing']} | {row['fully_absent']} |")
    lines.append('')
    if report['conforms'] is None:lines.append('本次仅统计字段，未运行 SHACL。')
    else:
        lines.extend(['| 规则组 | 通过 | 错误 | 警告 | 提示 |','| --- | --- | ---: | ---: | ---: |'])
        for key,value in report['profiles'].items():
            c=value['counts'];lines.append(f"| {key} | {value['conforms']} | {c.get('Violation',0)} | {c.get('Warning',0)} | {c.get('Info',0)} |")
    lines.extend(['',f"未覆盖主体：{len(report['coverage']['uncovered_subjects'])}；结构未列出的属性：{len(report['coverage']['unlisted_predicates'])}；辅助来源：{report['coverage']['auxiliary_sources']}。",'',
                  '未检查：'+'；'.join(report['coverage']['not_checked'])+'。','',
                  '可选字段未填也会出现在字段统计中，不自动算错误；两个规则组结果可能重叠。',''])
    return '\n'.join(lines)
