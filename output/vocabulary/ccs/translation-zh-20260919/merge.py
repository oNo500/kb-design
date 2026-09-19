"""一次性合并：输入固定英文词表和逐项翻译，保留原图及完整翻译记录。"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import uuid

from rdflib import Graph, Literal, Namespace, RDF, SKOS, URIRef
from rdflib.compare import isomorphic
from kb_vocab_ccs.adapter import turtle_bytes
from kb_vocab_ccs.storage import new_directory, write_json
from kb_vocab_rdf_preview.server import load_tree, render

ROOT = Path(__file__).resolve().parent
XL = Namespace('http://www.w3.org/2008/05/skos-xl#')
SOURCE = json.loads((ROOT/'source.json').read_text())
INPUT = Path(SOURCE['input'])
OUTPUT = ROOT/'result'
BATCH_ID = 'ccs-2012-zh-once-20260919'


def main():
    raw = INPUT.read_bytes()
    if sha256(raw).hexdigest() != SOURCE['sha256']:
        raise ValueError('英文词表已变化，停止合并')
    original = Graph().parse(data=raw,format='turtle')
    graph = Graph()
    for triple in original:
        graph.add(triple)
    tasks = json.loads((ROOT/'tasks.json').read_text())
    by_id = {r['id']:r for r in tasks}
    if len(by_id) != len(tasks):
        raise ValueError('重复任务编号')
    translations = {}
    batches = []
    completed_times = {}
    for i in range(1,10):
        input_path = ROOT/'batches'/f'{i:02}-input.json'
        output_path = ROOT/'batches'/f'{i:02}-output.json'
        inputs = json.loads(input_path.read_text())
        rows = json.loads(output_path.read_text())
        if len(rows) != len(inputs) or {r['id'] for r in rows} != {r['id'] for r in inputs}:
            raise ValueError(f'批次{i}编号不全或重复')
        completed = datetime.fromtimestamp(output_path.stat().st_mtime,timezone.utc).isoformat()
        batch = {
            'id':f'{BATCH_ID}/{i:02}', 'executor':f'Codex agent /root/ccs_zh_{i:02}',
            'model':'Codex 会话继承模型','exact_model_version':None,
            'model_version_note':'工具未提供实际模型的精确版本，不从配置或推测补造。',
            'completed_at':completed,'time_meaning':'该批结果文件最后写入时间，UTC',
            'method':'模型既有知识一次性初译','basis_level':5,'external_usage_verified':False,
            'input_sha256':sha256(input_path.read_bytes()).hexdigest(),
            'output_sha256':sha256(output_path.read_bytes()).hexdigest(),
            'authorization':'用户在当前任务中批准一次性批量翻译首选名称、保留记录并生成供浏览的词表。',
            'human_review_status':'not_reviewed',
        }
        batches.append(batch)
        for row in rows:
            if row['id'] in translations:
                raise ValueError('跨批次重复编号')
            if row['decision'] not in ('translated','retain_original'):
                raise ValueError('未知翻译结论')
            if row['decision']=='translated':
                if not isinstance(row['zh'],str) or not row['zh'].strip() or row['zh']==by_id[row['id']]['en']:
                    raise ValueError(f'不能把空值或原英文标作中文：{row["id"]}')
                if not any('\u3400'<=c<='\u9fff' for c in row['zh']):
                    raise ValueError(f'未含中文字的结果待核：{row["id"]}')
            elif row['zh'] is not None or not row['note'].strip():
                raise ValueError('保留原名须留原因且不能伪造中文值')
            translations[row['id']] = {**row,'batch_id':batch['id']}
            completed_times[row['id']] = completed
    if set(translations) != set(by_id):
        raise ValueError('总任务未全覆盖')
    registry = []
    records = []
    notices = '模型知识 · 第 5 级，外部用法未核实；未经人工复核。'
    for task in tasks:
        row = translations[task['id']]
        concept = URIRef(task['iri'])
        task_id = f'{BATCH_ID}/task/{task["id"]}'
        if (concept,SKOS.prefLabel,Literal(task['en'],lang=task['source_language'])) not in original:
            raise ValueError(f'原名称不匹配：{task["id"]}')
        if any(v.language and v.language.lower().startswith('zh') for v in original.objects(concept,SKOS.prefLabel)):
            raise ValueError('不覆盖已有中文')
        label = None
        if row['decision']=='translated':
            # 身份关联首次翻译任务，不由译文内容决定；同任务重试复用分配。
            label = URIRef('urn:kb-vocab-ccs:translation-label:'+str(uuid.uuid5(uuid.NAMESPACE_URL,task_id)))
            value = Literal(row['zh'],lang='zh')
            graph.add((concept,SKOS.prefLabel,value))
            graph.add((concept,XL.prefLabel,label))
            graph.add((label,RDF.type,XL.Label))
            graph.add((label,XL.literalForm,value))
            graph.add((label,SKOS.editorialNote,Literal(notices,lang='zh')))
            registry.append({'label_iri':str(label),'task_id':task_id,'concept_iri':str(concept),
                             'role':str(XL.prefLabel),'language':'zh','allocated_at':completed_times[task['id']],
                             'allocation_basis':'首次按本次翻译任务分配，重试保持相同身份。'})
        records.append({
            'task_id':task_id,'concept_id':task['id'],'concept_iri':str(concept),
            'field':str(SKOS.prefLabel),'source_text':task['en'],'source_language':task['source_language'],
            'source_version':SOURCE['sha256'],'source_parents':task['parents'],'source_notes':task['scope_notes'],
            'target_language':'zh','purpose':'自有词表的中文浏览，模型初译',
            'translation':row['zh'],'decision':row['decision'],'note':row['note'],
            'batch_id':row['batch_id'],'translated_at':completed_times[task['id']],
            'label_iri':str(label) if label else None,'basis_level':5,'basis':'模型既有知识，外部用法未核实',
            'human_review_status':'not_reviewed','human_reviewer':None,
            'source_applicability':{'version':SOURCE['sha256'],'status':'translation_input','later_version_review':None},
        })
    if not set(original)<=set(graph):
        raise ValueError('原图陈述丢失')
    for predicate in (SKOS.broader,SKOS.narrower,SKOS.related,RDF.type):
        before=set(original.subject_objects(predicate));after=set(graph.subject_objects(predicate))
        if predicate==RDF.type:
            after={p for p in after if p[1]!=XL.Label or (p[0],predicate,p[1]) in original}
        if before != after:
            raise ValueError(f'不应改变的关系或对象已变化：{predicate}')
    content=turtle_bytes(graph)
    if not isomorphic(graph,Graph().parse(data=content,format='turtle')):
        raise ValueError('回读不一致')
    duplicate_zh=defaultdict(list)
    for r in records:
        if r['translation']:
            duplicate_zh[r['translation']].append({'id':r['concept_id'],'en':r['source_text']})
    summary={
        'concepts':len(tasks),'translated':sum(r['decision']=='translated' for r in records),
        'retained_original':sum(r['decision']=='retain_original' for r in records),
        'human_reviewed':0,'source_preserved':True,'relations_unchanged':True,
        'source_sha256':SOURCE['sha256'],'vocabulary_sha256':sha256(content).hexdigest(),
        'duplicate_chinese_names':{k:v for k,v in duplicate_zh.items() if len(v)>1},
        'notes':[{'id':r['concept_id'],'en':r['source_text'],'zh':r['translation'],'note':r['note']} for r in records if r['note']],
    }
    with new_directory(OUTPUT) as stage:
        (stage/'vocabulary.multilingual.ttl').write_bytes(content)
        write_json(stage/'translations.json',records)
        write_json(stage/'batches.json',batches)
        write_json(stage/'name-registry.json',registry)
        write_json(stage/'summary.json',summary)
        preview=load_tree(stage/'vocabulary.multilingual.ttl')
        page=render(preview).replace('<main>','<p style="color:#886525;font-size:14px">中文名称为模型初译，外部用法未核实，未经人工复核。未译条目保留原文。</p><main>')
        (stage/'preview.html').write_text(page)
        write_json(stage/'manifest.json',{'files':{p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(stage.iterdir())},
                   'input_sha256':SOURCE['sha256'],'translation_task':BATCH_ID,
                   'generator_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
                   'shacl_validation_executed':False,'formal_publication':False})
    print(json.dumps({k:v for k,v in summary.items() if k not in ('notes','duplicate_chinese_names')},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
