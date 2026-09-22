"""Collect existing source snapshots; serialize reviewed records without inferring concepts."""
from contextlib import contextmanager
from hashlib import sha256
from importlib.resources import files
import json
import os
from pathlib import Path
import tempfile

from bs4 import BeautifulSoup
from jsonschema import Draft202012Validator, FormatChecker
from kb_sources.download import fetch, verify
from kb_sources.structure import extract_file
from rdflib import BNode, Graph, Literal, Namespace, RDF, SKOS, URIRef
from rdflib.namespace import DCTERMS
from rdflib.compare import isomorphic

XL=Namespace('http://www.w3.org/2008/05/skos-xl#')
PROV=Namespace('http://www.w3.org/ns/prov#')
ROLES={'preferred':(SKOS.prefLabel,XL.prefLabel),'alternative':(SKOS.altLabel,XL.altLabel),'hidden':(SKOS.hiddenLabel,XL.hiddenLabel)}
NOTES={'definition':SKOS.definition,'scope':SKOS.scopeNote,'guidance':SKOS.note,'example':SKOS.example,'editorial':SKOS.editorialNote}


def read_json(path):
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result:raise ValueError(f'重复 JSON 键：{key}')
            result[key]=value
        return result
    return json.loads(path if isinstance(path,bytes) else path.read_bytes(),object_pairs_hook=unique)


def write_json(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')


@contextmanager
def output_directory(path):
    path=Path(path)
    if path.exists() or path.is_symlink():raise ValueError(f'输出已存在：{path}')
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.writing-',dir=path.parent) as temporary:
        stage=Path(temporary)/'result';stage.mkdir()
        yield stage
        if path.exists() or path.is_symlink():raise ValueError(f'输出已存在：{path}')
        stage.rename(path)


def collect(output,*,manifest=None,snapshot=None):
    """kb-sources owns acquisition, verification and extraction; no heading-to-concept inference."""
    output=Path(output).resolve()
    if bool(manifest)==bool(snapshot):raise ValueError('指定一份 manifest 或一个已有 snapshot')
    if output.exists():raise ValueError('收集输出目录已存在')
    if snapshot and Path(snapshot).resolve() in (output,*output.parents):
        raise ValueError('不能把提取结果写进原件快照')
    output.mkdir(parents=True)
    try:
        snapshot=Path(snapshot).resolve() if snapshot else fetch(manifest,output/'raw')
        receipt=verify(snapshot)
        bindings=[]
        for item in receipt['files']:
            bindings.append({'key':item['id'],'snapshot':os.path.relpath(snapshot,output),'file_id':item['id'],
                             'sha256':item['sha256'],'url':item['final_url'],'format':item['format']})
            if item['format'] in ('html','pdf'):
                extract_file(snapshot,item['id'],output/'reading'/item['id'])
        result={'format_version':1,'files':bindings}
        write_json(output/'sources.json',result)
        return result
    except Exception as error:
        write_json(output/'incomplete.json',{'status':'incomplete','error':str(error)})
        raise


def load_sources(lock_path,lock=None):
    lock=read_json(lock_path) if lock is None else lock
    if lock.get('format_version')!=1 or not lock.get('files'):raise ValueError('来源锁定文件无效')
    result={};receipts={}
    for row in lock['files']:
        if row['key'] in result:raise ValueError('来源键重复')
        snapshot=(lock_path.parent/row['snapshot']).resolve()
        if snapshot not in receipts:receipts[snapshot]=verify(snapshot)
        receipt=receipts[snapshot]
        selected=[item for item in receipt['files'] if item['id']==row['file_id']]
        if len(selected)!=1:raise ValueError('来源 file_id 不唯一或不存在')
        item=selected[0]
        if any(row[k]!=item[actual] for k,actual in [('sha256','sha256'),('url','final_url'),('format','format')]):
            raise ValueError('来源锁定值与原件凭据不符')
        raw=(snapshot/item['filename']).read_bytes()
        if sha256(raw).hexdigest()!=item['sha256']:raise ValueError('原文在读取期间发生变化')
        result[row['key']]={**row,'title':receipt['source']['title'],'receipt':receipt,'raw':raw,
                            'snapshot_iri':'urn:kb-vocab-writing:snapshot:'+item['sha256'],
                            'soup':BeautifulSoup(raw,'html.parser') if item['format']=='html' else None}
    return result


def approval_digest(spec):
    payload={key:value for key,value in spec.items() if key not in ('approved','approval')}
    return sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()


def build(input_path,lock_path,output,*,preview=False):
    input_path,lock_path=Path(input_path),Path(lock_path)
    input_raw=input_path.read_bytes();lock_raw=lock_path.read_bytes()
    spec=read_json(input_raw)
    schema=json.loads(files('kb_vocab_writing').joinpath('schemas/input.json').read_text())
    Draft202012Validator(schema,format_checker=FormatChecker()).validate(spec)
    if spec['approved'] and not spec['approval']:raise ValueError('已确认输入必须记录确认人和依据')
    if spec['approved'] and spec['approval']['content_sha256']!=approval_digest(spec):raise ValueError('输入已改变，原确认不再匹配；请重新审阅')
    if not preview and not spec['approved']:raise ValueError('输入尚未确认；只允许 --preview 生成审阅样稿')
    if spec['source_lock_sha256']!=sha256(lock_raw).hexdigest():raise ValueError('来源锁定文件已变化，须重新核对输入')
    sources=load_sources(lock_path,read_json(lock_raw))
    graph=Graph();identities={};evidence=[];note_ids=[];label_ids=[];used_sources=set()
    concepts={row['id'] for row in spec['concepts']}
    collections={row['id'] for row in spec['collections']}
    if len(concepts)!=len(spec['concepts']) or len(collections)!=len(spec['collections']):raise ValueError('对象 ID 重复')
    def claim(identity,kind,payload=None):
        previous=identities.get(identity)
        current=(kind,payload)
        if previous is not None and (kind!='label' or previous!=current):raise ValueError(f'身份碰撞：{identity}')
        identities[identity]=current
        return URIRef(identity)
    def literal(value):return Literal(value['text'],lang=value['language'])
    def annotate_basis(node,basis):
        if basis is None:return
        methods={'source':'来源表达','model':'模型翻译或归纳','user':'用户提供'}
        message=f"{methods[basis['method']]}；本地整理者：{basis['executor']}；记录时间：{basis['recorded_at']}；"
        if basis['method']=='model':message+=f"模型精确版本：{basis['model_version'] or '未提供'}；"
        message+=basis['note']
        graph.add((node,SKOS.editorialNote,Literal(message,lang='zh')))
    def support(subject,refs):
        for ref in refs:
            source=sources.get(ref['source'])
            if source is None:raise ValueError(f'未知来源：{ref["source"]}')
            if source['soup'] is None:raise ValueError('首版概念依据定位仅支持 HTML；其他格式原件可保存，不能冒充已定位')
            matches=source['soup'].select(ref['selector'])
            if len(matches)!=1:raise ValueError(f'来源定位未唯一命中：{ref["selector"]}')
            quote=' '.join(ref['quote'].split())
            text=' '.join(matches[0].get_text(' ',strip=True).split())
            if quote not in text:raise ValueError('引文在指定原文位置不存在')
            node=URIRef(source['snapshot_iri']);used_sources.add(ref['source'])
            graph.add((subject,DCTERMS.source,node))
            evidence.append({'subject':str(subject),**ref,'source_sha256':source['sha256'],'source_url':source['url']})
    scheme=claim(spec['scheme']['id'],'scheme')
    graph.add((scheme,RDF.type,SKOS.ConceptScheme))
    graph.add((scheme,SKOS.prefLabel,literal(spec['scheme']['label'])))
    graph.add((scheme,SKOS.scopeNote,literal(spec['scheme']['scope'])))
    for top in spec['scheme']['top_concepts']:
        if top not in concepts:raise ValueError('顶层引用不在本次概念输入中')
        graph.add((scheme,SKOS.hasTopConcept,URIRef(top)));graph.add((URIRef(top),SKOS.topConceptOf,scheme))
    for row in spec['concepts']:
        subject=claim(row['id'],'concept')
        graph.add((subject,RDF.type,SKOS.Concept));graph.add((subject,SKOS.inScheme,scheme))
        support(subject,row['evidence'])
        for name in row['labels']:
            node=claim(name['id'],'label',(name['text'],name['language']))
            direct,xl=ROLES[name['role']]
            graph.add((subject,direct,literal(name)));graph.add((subject,xl,node))
            graph.add((node,RDF.type,XL.Label));graph.add((node,XL.literalForm,literal(name)))
            label_ids.append(str(node))
            annotate_basis(node,name.get('basis'))
            if name.get('basis'):support(node,row['evidence'])
        for statement in row['statements']:
            node=claim(statement['id'],'note');note_ids.append(str(node))
            graph.add((subject,NOTES[statement['kind']],node));graph.add((node,RDF.value,literal(statement)))
            if statement.get('applicability'):graph.add((node,DCTERMS.description,Literal(statement['applicability'],lang=statement['language'])))
            support(node,statement['evidence'])
            annotate_basis(node,statement.get('basis'))
        for key,predicate,reverse in [('broader',SKOS.broader,SKOS.narrower),('related',SKOS.related,SKOS.related)]:
            for relation in row[key]:
                if relation['target'] not in concepts:raise ValueError('关系引用不在本次概念输入中')
                graph.add((subject,predicate,URIRef(relation['target'])))
                graph.add((URIRef(relation['target']),reverse,subject))
                count=len(evidence);support(subject,relation['evidence'])
                for item in evidence[count:]:item.update(predicate=str(predicate),target=relation['target'])
    for row in spec['collections']:
        node=claim(row['id'],'collection')
        graph.add((node,RDF.type,SKOS.Collection));graph.add((node,SKOS.inScheme,scheme))
        graph.add((node,SKOS.prefLabel,literal(row['label'])));graph.add((node,SKOS.scopeNote,literal(row['scope'])))
        for member in row['members']:
            if member not in concepts|collections:raise ValueError('集合成员不存在')
            graph.add((node,SKOS.member,URIRef(member)))
    auxiliary=[]
    for key in sorted(used_sources):
        source=sources[key];node=URIRef(source['snapshot_iri'])
        if str(node) in identities:raise ValueError('对象与来源快照身份冲突')
        auxiliary.append(str(node))
        graph.add((node,RDF.type,PROV.Entity));graph.add((node,DCTERMS.source,URIRef(source['url'])))
        graph.add((node,DCTERMS.title,Literal(source['title'])));graph.add((node,DCTERMS.identifier,Literal('sha256:'+source['sha256'])))
    if any(isinstance(t,BNode) for triple in graph for t in triple):raise ValueError('输出出现未分配身份的空白节点')
    ttl=('# 程序生成；编辑输入后重建。\n'+ ('# 审阅样稿，未自动采纳或发布。\n' if preview else '')+'\n'.join(sorted(graph.serialize(format='nt').splitlines()))+'\n').encode()
    if not isomorphic(graph,Graph().parse(data=ttl,format='turtle')):raise ValueError('Turtle 回读不一致')
    manifest={'format_version':1,'approval_payload_sha256':approval_digest(spec),'input_approved':spec['approved'],'mode':'preview' if preview else 'build','published':False,
              'concepts':sorted(concepts),'labels':sorted(set(label_ids)),'collections':sorted(collections),'notes':sorted(note_ids),
              'auxiliary_resources':sorted(set(auxiliary)),'source_lock_sha256':spec['source_lock_sha256'],'source_lock_location':str(lock_path.resolve()),
              'shacl_validation_executed':False,'semantic_review_executed':False}
    with output_directory(output) as stage:
        (stage/'vocabulary.ttl').write_bytes(ttl)
        (stage/'input.json').write_bytes(input_raw);(stage/'sources.json').write_bytes(lock_raw)
        write_json(stage/'evidence.json',evidence)
        write_json(stage/'source-receipts.json',{key:{k:v for k,v in value.items() if k not in ('raw','soup')} for key,value in sources.items()})
        (stage/'审阅清单.md').write_text(review_text(spec,sources),encoding='utf-8')
        manifest['files']={p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(stage.iterdir())}
        write_json(stage/'manifest.json',manifest)
    return manifest


def review_text(spec,sources=None):
    import html
    def escape(value):return html.escape(value).replace('|','\\|').replace('\n',' ')
    lines=['# 写作概念审阅','',
           '生成授权：'+('已记录' if spec['approved'] else '未确认')+'；机械检查不代表逐项人工语义审阅。','',
           '| 概念 ID | 名称 | 定义数 | 建议数 | 来源 |','| --- | --- | ---: | ---: | --- |']
    for row in spec['concepts']:
        lines.append('| '+escape(row['id'])+' | '+escape(' / '.join(f"{n['text']}@{n['language']}" for n in row['labels']))+
                     f" | {sum(n['kind']=='definition' for n in row['statements'])} | {sum(n['kind']=='guidance' for n in row['statements'])} | "+
                     escape(', '.join(sorted({r['source'] for r in row['evidence']})))+' |')
    lines.extend(['','## 概念内容',''])
    kinds={'definition':'定义','scope':'范围','guidance':'建议','example':'示例','editorial':'编辑说明'}
    for row in spec['concepts']:
        names=' / '.join(n['text'] for n in row['labels'] if n['role']=='preferred')
        lines.extend(['**'+escape(names)+'**','',f"ID：`{row['id']}`",''])
        for statement in row['statements']:
            lines.append(f"- {kinds[statement['kind']]}：{escape(statement['text'])}")
            if statement.get('applicability'):lines.append(f"  适用说明：{escape(statement['applicability'])}")
        for relation in ('broader','related'):
            if row[relation]:lines.append(f"- {relation}："+', '.join('`'+r['target']+'`' for r in row[relation]))
        if sources:
            keys=sorted({r['source'] for r in row['evidence']})
            lines.append('- 来源：'+'、'.join(f"[{key}]({sources[key]['url']})" for key in keys))
        lines.append('')
    return '\n'.join(lines)+'\n'
