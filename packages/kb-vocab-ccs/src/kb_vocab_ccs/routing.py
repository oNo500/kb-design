"""Explicit, human-confirmed routing; source graphs and identities remain traceable."""
from collections import Counter
from hashlib import sha256
import json
import uuid

from rdflib import Graph, Literal, RDF, SKOS, URIRef, RDFS, Namespace
from rdflib.compare import isomorphic

from .adapter import XL, turtle_bytes
from .storage import new_directory, write_json, json_bytes

ACTIONS = {'concept','entity','both','pending'}
KIND_CLASSES = {
    'software':'Q7397', 'programming-language':'Q9143',
    'organization':'Q43229', 'person':'Q5', 'large-language-model':'Q115305900',
}
KINDS = set(KIND_CLASSES)
PROV = Namespace('http://www.w3.org/ns/prov#')
ROLES = (SKOS.prefLabel,SKOS.altLabel,SKOS.hiddenLabel)
XL_ROLES = (XL.prefLabel,XL.altLabel,XL.hiddenLabel)


def read_graph(path):
    raw = path.read_bytes()
    return raw, Graph().parse(data=raw,format='turtle',publicID=path.resolve().as_uri())


def branch(graph, root):
    concepts = set(graph.subjects(RDF.type,SKOS.Concept))
    if root not in concepts:
        raise ValueError('找不到指定的专名分支')
    visited, pending = set(), [root]
    while pending:
        node = pending.pop()
        if node in visited:
            continue
        if node not in concepts:
            raise ValueError('分支包含未声明为 Concept 的对象')
        visited.add(node)
        pending.extend(graph.objects(node,SKOS.narrower))
        pending.extend(graph.subjects(SKOS.broader,node))
    return visited


def prepare(path, root=None):
    raw, graph = read_graph(path)
    if root is None:
        found = [s for s in graph.subjects(RDF.type,SKOS.Concept) if str(s).endswith('#10011641')]
        if len(found)!=1:
            raise ValueError('无法唯一定位 CCS 专名分支')
        root = str(found[0])
    nodes = branch(graph,URIRef(root))
    return {'format_version':1,'input_sha256':sha256(raw).hexdigest(),
            'root':root,'confirmed':False,
            'items':[{'source_id':str(node),'action':'pending','kind':None} for node in sorted(nodes,key=str)]}


def validate_plan(graph, raw, plan, require_confirmation=False):
    if plan.get('format_version')!=1 or type(plan.get('confirmed')) is not bool:
        raise ValueError('清单版本或确认状态无效')
    if require_confirmation and plan['confirmed'] is not True:
        raise ValueError('清单尚未人工确认；不能生成分流结果')
    if plan['input_sha256']!=sha256(raw).hexdigest():
        raise ValueError('词表版本与清单不符，请重新核对')
    expected = {str(n) for n in branch(graph,URIRef(plan['root']))}
    ids = [r['source_id'] for r in plan['items']]
    if len(ids)!=len(set(ids)) or set(ids)!=expected:
        raise ValueError('清单须逐项覆盖整个分支，不能重复、漏项或包含分支外条目')
    for row in plan['items']:
        if row['action'] not in ACTIONS:
            raise ValueError('未知处理方式')
        if row['action'] in ('entity','both'):
            if row['kind'] not in KINDS:
                raise ValueError('实体类别尚未采用；保留 pending，不能自行扩展')
        elif row['kind'] is not None:
            raise ValueError('保留概念或未决条目不填写实体类别')


def review_markdown(graph, plan):
    def display(node):
        values = [v for v in graph.objects(node,SKOS.prefLabel) if isinstance(v,Literal)]
        values.sort(key=lambda v:(0 if v.language=='zh' else 1 if v.language=='en' else 2,str(v)))
        return str(values[0]) if values else str(node)
    def escape(text):
        return text.replace('|','\\|').replace('\n',' ')
    actions={'concept':'保留概念','entity':'建立实体','both':'两者保留','pending':'尚未确定'}
    counts=Counter(r['action'] for r in plan['items'])
    lines=['# 专名处理清单','',
           '状态：'+('已确认' if plan['confirmed'] else '待人工确认；建议不等于已采纳的归属或实体事实。'),'',
           '；'.join(f'{actions[k]} {counts[k]} 项' for k in ('concept','entity','both','pending'))+'。','',
           '来源版本固定在 plan.json；生成概念与实体两份 Turtle 词表，不直接写入现行实体库。',
           '建立实体会从概念输出移除该条目及其引用边，移除陈述单独留档；不重新挂接下级。若影响未决条目的关系则停止。',
           '来源分组节点的保留不表示它们是学科域；本步骤不重写导航分组。','',
           '| 来源 ID | 名称 | 处理方式 | 实体类别 |','| --- | --- | --- | --- |']
    for row in plan['items']:
        lines.append(f"| {escape(row['source_id'].rsplit('#',1)[-1])} | {escape(display(URIRef(row['source_id'])))} | {actions[row['action']]} | {row['kind'] or '—'} |")
    return '\n'.join(lines)+'\n'


def write_review(path, output, plan_path=None):
    raw, graph = read_graph(path)
    plan = json.loads(plan_path.read_bytes()) if plan_path else prepare(path)
    validate_plan(graph,raw,plan)
    with new_directory(output) as stage:
        write_json(stage/'plan.json',plan)
        (stage/'处理清单.md').write_text(review_markdown(graph,plan),encoding='utf-8')
    return Counter(r['action'] for r in plan['items'])


def partition(path, plan, output):
    raw, source = read_graph(path)
    validate_plan(source,raw,plan,require_confirmation=True)
    result = Graph()
    for triple in source:
        result.add(triple)
    removed = {URIRef(r['source_id']) for r in plan['items'] if r['action']=='entity'}
    pending = {URIRef(r['source_id']) for r in plan['items'] if r['action']=='pending'}
    if any((subject in removed and obj in pending) or (subject in pending and obj in removed)
           for subject, predicate, obj in source):
        raise ValueError('转为实体会改变未决条目的关系；请先确认这些关联条目的处理')
    affected_labels = {label for node in removed for role in XL_ROLES for label in source.objects(node,role)}
    for node in removed:
        result.remove((node,None,None))
        result.remove((None,None,node))
    # A name shared with a retained resource must remain available.
    for label in affected_labels:
        if not any(result.triples((None,None,label))):
            result.remove((label,None,None))
    entities, links = [], []
    entity_graph = Graph()
    for row in sorted(plan['items'],key=lambda r:r['source_id']):
        if row['action'] not in ('entity','both'):
            continue
        concept=URIRef(row['source_id'])
        entity='urn:kb-vocab-ccs:entity:'+str(uuid.uuid5(uuid.NAMESPACE_URL,str(concept)))
        entity_node=URIRef(entity)
        entity_graph.add((entity_node,RDF.type,URIRef('http://www.wikidata.org/entity/'+KIND_CLASSES[row['kind']])))
        entity_graph.add((entity_node,RDFS.seeAlso,concept))
        entity_graph.add((entity_node,SKOS.editorialNote,Literal('分流已确认；实体事实尚未逐项核实。',lang='zh')))
        for role, xl_role in zip(ROLES,XL_ROLES):
            for value in source.objects(concept,role):
                if not isinstance(value,Literal):
                    raise ValueError('实体名称必须为文字，不能强制转换')
                name_id=sha256(json_bytes([entity,str(role),value.n3()])).hexdigest()
                name=URIRef('urn:kb-vocab-ccs:entity-label:'+name_id)
                entity_graph.add((entity_node,role,value))
                entity_graph.add((entity_node,xl_role,name))
                entity_graph.add((name,RDF.type,XL.Label))
                entity_graph.add((name,XL.literalForm,value))
                for source_name in source.objects(concept,xl_role):
                    if (source_name,XL.literalForm,value) in source:
                        entity_graph.add((name,PROV.wasDerivedFrom,source_name))
                        for note in source.objects(source_name,SKOS.editorialNote):
                            entity_graph.add((name,SKOS.editorialNote,note))
        entities.append({'id':entity,'kind':row['kind'],'source_concept':str(concept),
                         'routing_confirmed':True,'facts_verified':False})
        links.append({'source_concept':str(concept),'entity':entity,'action':row['action']})
    # This is a generation correspondence, not owl:sameAs or skos:exactMatch.
    report={'concepts':len(set(result.subjects(RDF.type,SKOS.Concept))),
            'entity_records':len(entities),'removed_concepts':len(removed),
            'pending':sum(r['action']=='pending' for r in plan['items']),
            'source_sha256':sha256(raw).hexdigest(),'shacl_validation_executed':False,
            'formal_entity_import':False}
    concept_bytes=turtle_bytes(result)
    entity_bytes=turtle_bytes(entity_graph)
    if not isomorphic(entity_graph,Graph().parse(data=entity_bytes,format='turtle')):
        raise ValueError('实体词表回读不一致')
    with new_directory(output) as stage:
        (stage/'input.ttl').write_bytes(raw)
        (stage/'concepts.ttl').write_bytes(concept_bytes)
        (stage/'entities.ttl').write_bytes(entity_bytes)
        write_json(stage/'entity-audit.json',{'purpose':'分流确认及核实状态，仅作审计','records':entities})
        write_json(stage/'routing.json',links)
        write_json(stage/'plan.json',plan)
        write_json(stage/'report.json',report)
        (stage/'removed-statements.ttl').write_bytes(turtle_bytes(source-result))
        write_json(stage/'manifest.json',{'files':{p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(stage.iterdir())}})
    return report
