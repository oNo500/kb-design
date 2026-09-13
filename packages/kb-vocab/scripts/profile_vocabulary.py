"""Inventory all RDF subject fields without changing or inferring vocabulary data."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from rdflib import BNode, Graph, Literal, RDF, SKOS, URIRef


def term(value):
    result={'value':str(value),'kind':'iri' if isinstance(value,URIRef) else 'blank_node' if isinstance(value,BNode) else 'literal'}
    if isinstance(value,Literal):
        result.update(language=value.language,datatype=str(value.datatype) if value.datatype else None)
    return result


def profile(path):
    requested=Path(path).absolute();actual=requested.resolve(strict=True)
    raw=actual.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    manifest=actual.parent/'manifest.json'
    if manifest.exists():
        entry=json.loads(manifest.read_bytes()).get('files',{}).get(actual.name)
        expected=entry.get('sha256') if isinstance(entry,dict) else entry
        if expected!=sha:raise ValueError('Input hash differs from its build manifest')
    graph=Graph().parse(data=raw,format='turtle',publicID=actual.as_uri())
    subjects=defaultdict(lambda:defaultdict(list))
    resources=set()
    for subject,predicate,value in graph:
        subjects[subject][predicate].append(value)
        resources.add(subject)
        if isinstance(value,(URIRef,BNode)):resources.add(value)
    types={subject:set(properties.get(RDF.type,[])) for subject,properties in subjects.items()}
    categories=defaultdict(list);explicit_types=defaultdict(list)
    for subject in sorted(subjects,key=str):
        found=types[subject]
        # Exclusive display groups; every explicitly stated RDF type is also
        # independently profiled below, so multi-typing is not discarded.
        if SKOS.Concept in found:category='Concept'
        elif SKOS.OrderedCollection in found:category='OrderedCollection'
        elif SKOS.Collection in found:category='Collection'
        elif SKOS.ConceptScheme in found:category='ConceptScheme'
        elif found:category='Other typed resources'
        else:category='Untyped subjects'
        categories[category].append(subject)
        for value in found:explicit_types[str(value)].append(subject)

    def fields(nodes):
        predicates=sorted({p for subject in nodes for p in subjects[subject]},key=str)
        result=[]
        for predicate in predicates:
            present=[subject for subject in nodes if predicate in subjects[subject]]
            cardinality=Counter(len(subjects[s].get(predicate,[])) for s in nodes)
            kinds=Counter();languages=Counter();datatypes=Counter();object_types=Counter()
            empty=0;samples=[];references_without_type=0
            for subject in present:
                for value in sorted(subjects[subject][predicate],key=str):
                    if isinstance(value,Literal):
                        kinds['literal']+=1;languages[value.language or '(none)']+=1
                        datatypes[str(value.datatype) if value.datatype else '(implicit)']+=1
                        if not str(value).strip():empty+=1
                    else:
                        kinds['iri' if isinstance(value,URIRef) else 'blank_node']+=1
                        target_types=types.get(value,set())
                        if not target_types:references_without_type+=1
                        object_types.update(str(t) for t in target_types)
                    if len(samples)<3:samples.append({'subject':str(subject),'value':term(value)})
            missing=[str(s) for s in nodes if predicate not in subjects[s]]
            result.append({'predicate':str(predicate),'subjects_with_field':len(present),'subjects_without_field':len(missing),
                'coverage_percent':round(100*len(present)/len(nodes),4),'triple_count':sum(n*c for n,c in cardinality.items()),
                'cardinality_histogram':dict(sorted(cardinality.items())), 'max_values_per_subject':max(cardinality),
                'value_kinds':dict(kinds),'literal_languages':dict(sorted(languages.items())),
                'literal_datatypes':dict(sorted(datatypes.items())), 'empty_literal_count':empty,
                'referenced_explicit_types':dict(sorted(object_types.items())),
                'resource_values_without_explicit_type':references_without_type,
                'missing_subject_examples':missing[:10],'value_examples':samples})
        return result

    all_fields=fields(list(subjects))
    # Mechanical completeness check: profiling must account for every input triple.
    if sum(row['triple_count'] for row in all_fields)!=len(graph):raise ValueError('Field inventory lost triples')
    grouped={name:{'subjects':len(nodes),'fields':fields(nodes)} for name,nodes in categories.items()}
    typed={name:{'subjects':len(nodes),'fields':fields(nodes)} for name,nodes in sorted(explicit_types.items())}
    property_names={row['predicate']:graph.namespace_manager.normalizeUri(URIRef(row['predicate'])) for row in all_fields}
    return {'input':{'requested_path':str(requested),'resolved_path':str(actual),'sha256':sha},
        'summary':{'triples':len(graph),'subjects':len(subjects),'iri_subjects':sum(isinstance(s,URIRef) for s in subjects),
                   'blank_node_subjects':sum(isinstance(s,BNode) for s in subjects),
                   'resource_nodes_in_subject_or_object':len(resources),'object_only_resources':len(resources-set(subjects)),
                   'distinct_predicates':len(all_fields),'explicit_rdf_types':len(typed),
                   'subjects_with_multiple_types':sum(len(t)>1 for t in types.values())},
        'scope':'All stored triples, no inference. Field-bearing nodes are RDF subjects; object-only references are counted separately. Missing fields and untyped external references are observations, not violations.',
        'namespaces':{prefix:str(namespace) for prefix,namespace in graph.namespaces() if any(name.startswith(prefix+':') for name in property_names.values())},
        'property_names':property_names,'all_fields':all_fields,'exclusive_groups':grouped,'by_explicit_type':typed}


def markdown(report):
    summary=report['summary'];names=report['property_names']
    lines=['# 字段盘点','','统计当前词表中全部 RDF 主语的字段；不推断类型，不修改数据，不预先设定必填项。',
           '',f"输入快照：`{report['input']['resolved_path']}`。",'',
           f"共 {summary['triples']:,} 条三元组、{summary['subjects']:,} 个有字段的节点、{summary['distinct_predicates']} 种属性。另有 {summary['object_only_resources']:,} 个仅作为对象出现的资源引用，不把它们当作缺少字段的词条。",'',
           '## 节点类型','','| 互斥展示分类 | 节点数 | 字段数 |','|---|---:|---:|']
    for name,group in report['exclusive_groups'].items():lines.append(f"| {name} | {group['subjects']:,} | {len(group['fields'])} |")
    lines+=['',f"另按全部 {summary['explicit_rdf_types']} 种显式 RDF 类型分别统计，详见 JSON；{summary['subjects_with_multiple_types']} 个节点有多个类型，类型统计不能相加。",'',
            '## 字段并集','','| 属性 | 有值节点数 | 三元组数 | 值类型 | 单节点最多值数 |','|---|---:|---:|---|---:|']
    for row in report['all_fields']:
        lines.append(f"| `{names[row['predicate']]}` | {row['subjects_with_field']:,} | {row['triple_count']:,} | {', '.join(row['value_kinds'])} | {row['max_values_per_subject']} |")
    headings={'Concept':'概念字段','Collection':'集合字段','OrderedCollection':'有序集合字段','ConceptScheme':'词表字段','Other typed resources':'其他资源字段','Untyped subjects':'未定类型字段'}
    for name,group in report['exclusive_groups'].items():
        lines+=['','## '+headings[name],'','| 属性 | 有值／节点总数 | 缺项数 | 覆盖率 | 值类型 | 单节点最多值数 |','|---|---:|---:|---:|---|---:|']
        for row in group['fields']:
            lines.append(f"| `{names[row['predicate']]}` | {row['subjects_with_field']:,}／{group['subjects']:,} | {row['subjects_without_field']:,} | {row['coverage_percent']}% | {', '.join(row['value_kinds'])} | {row['max_values_per_subject']} |")
    lines+=['','## 属性命名空间','','| 前缀 | URI |','|---|---|']
    for prefix,uri in sorted(report['namespaces'].items()):lines.append(f'| `{prefix}` | `{uri}` |')
    lines+=['','## 数据边界','','零值字段不会出现在对应节点上。缺项是否构成错误，需要后续字段规范决定；当前统计不将它们自动判为无效。',
            '值类型、语言、数据类型、每节点值数量分布、引用对象类型和缺项样例保存在 [详细结果](profile.json)。样例有数量限制，统计覆盖全部数据。',
            '全局字段并集不能直接用作每种节点的统一必填字段表；同一概念类型的来源字段差异也需在规范中保留其含义。','']
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();output=args.output.absolute()
    if output.exists():raise ValueError('Output directory already exists')
    report=profile(args.file)
    if output.resolve().is_relative_to(Path(report['input']['resolved_path']).parent):
        raise ValueError('Profile output must be outside the immutable build')
    output.parent.mkdir(parents=True,exist_ok=True);stage=Path(tempfile.mkdtemp(prefix='.profile-',dir=output.parent))
    try:
        (stage/'profile.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (stage/'index.md').write_text(markdown(report),encoding='utf-8')
        if hashlib.sha256(Path(report['input']['resolved_path']).read_bytes()).hexdigest()!=report['input']['sha256']:
            raise ValueError('Input changed while profiling')
        if output.exists():raise ValueError('Output appeared while profiling')
        stage.rename(output)
    finally:
        if stage.exists():shutil.rmtree(stage)
    print(json.dumps({'output':str(output),**report['summary'],
          'groups':{name:group['subjects'] for name,group in report['exclusive_groups'].items()}},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
