"""Extract IEEE's printed terms and explicit relation codes; never invent inverses or RDF identities."""
from collections import Counter, defaultdict
import csv
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import re
import tempfile

import pdfplumber
from pdfplumber.utils import cluster_objects
from kb_sources.download import SourceError, _validate

PREDICATES={'BT','NT','RT','USE','UF'}
RELATION=re.compile(r'^(BT|NT|RT|USE|UF):\s*(.*)$')


def pdf_lines(path):
    """July 2025 print layout: two columns, name / predicate / value indents."""
    lines=[];page_counts=[]
    with pdfplumber.open(path) as doc:
        cover=doc.pages[0].extract_text() or ''
        if not all(x in cover for x in ('2025','1.04','JULY','Thesaurus')):
            raise SourceError('this extraction profile requires July 2025 IEEE Thesaurus Version 1.04')
        for page in doc.pages[2:]:
            start=len(lines)
            all_words=page.extract_words(x_tolerance=1,y_tolerance=2,extra_attrs=['fontname','size'])
            for col,(left,right,base) in enumerate([(0,306,72),(306,612,323.7)],1):
                words=[w for w in all_words if left<=w['x0']<right and w['top']>=60]
                # Footer text is smaller; section banner lies above this crop.
                words=[w for w in words if w['size']>=9]
                for row in cluster_objects(words,'top',2):
                    row=sorted(row,key=lambda w:w['x0']);text=row[0]['text']
                    for a,b in zip(row,row[1:]):text+=(' ' if b['x0']-a['x1']>.6 else '')+b['text']
                    count=sum(len(w['text']) for w in row)
                    bold=sum(len(w['text']) for w in row if 'Bold' in w['fontname'])
                    italic=sum(len(w['text']) for w in row if 'Italic' in w['fontname'])
                    x=row[0]['x0']-base
                    style='preferred' if x<20 and bold>count*.6 else 'nonpreferred' if x<20 and italic>count*.6 else 'regular'
                    lines.append({'text':text,'x':round(x,2),'style':style,
                        'locator':{'page':page.page_number,'column':col,'bbox':[round(min(w['x0'] for w in row),2),round(min(w['top'] for w in row),2),round(max(w['x1'] for w in row),2),round(max(w['bottom'] for w in row),2)]}})
            page_counts.append({'page':page.page_number,'lines':len(lines)-start});page.close()
    return lines,{'page_count':len(page_counts)+2,'body_pages':page_counts,'cover':cover}


def parse_lines(lines):
    entries=[];unassigned=[];current=None;relation=None;last=None;last_was_heading=False;active_predicate=None;group=0
    for index,line in enumerate(lines,1):
        fragment={'line_id':index,**line};text=line['text'];heading=line['style']!='regular'
        if heading:
            same_flow=last and (last['locator']['page'],last['locator']['column'])==(line['locator']['page'],line['locator']['column'])
            gap=line['locator']['bbox'][1]-last['locator']['bbox'][3] if last else 100
            continuation=current and last_was_heading and current['form']==line['style'] and not current['relations'] and (not same_flow or 0<=gap<9)
            if continuation:
                current['name']+=('' if current['name'].endswith('-') else ' ')+text;current['name_fragments'].append(fragment)
            else:
                current={'id':f'e{len(entries)+1}','name':text,'form':line['style'],'locator':line['locator'],
                         'name_fragments':[fragment],'relations':[]};entries.append(current)
            relation=None;active_predicate=None;last_was_heading=True
        else:
            match=RELATION.match(text)
            if current and match:
                active_predicate=match[1];group+=1;relation={'predicate':match[1],'target':match[2],'source_group':f'g{group}','fragments':[fragment]}
                current['relations'].append(relation)
            elif current and relation and active_predicate and not re.match(r'^[A-Z]+:',text):
                if line['x']>=65 and relation['target']:
                    relation={'predicate':active_predicate,'target':text,'source_group':f'g{group}','fragments':[fragment]};current['relations'].append(relation)
                elif line['x']<25 or not relation['target']:
                    relation['target']=(relation['target']+('' if relation['target'].endswith('-') else ' ')+text).strip();relation['fragments'].append(fragment)
                else:
                    unassigned.append({'reason':'unexpected relation indentation','entry_id':current['id'],'fragment':fragment})
                    relation=None;active_predicate=None
            else:
                unassigned.append({'reason':'no recognized entry/relation context','entry_id':current['id'] if current else None,'fragment':fragment})
                relation=None;active_predicate=None
            last_was_heading=False
        last=line
    for e in entries:
        for r in e['relations']:
            r['raw_target']=r['target']
            r['connector_after']=None
            if r['predicate']=='USE' and r['target'].endswith(' AND'):
                r['target']=r['target'][:-4];r['connector_after']='AND'
    return {'entries':entries,'unassigned':unassigned,'input_lines':len(lines)}


def diagnose(entries):
    names=defaultdict(list)
    for entry in entries:names[entry['name']].append(entry['id'])
    normalized=defaultdict(list)
    for name in names:normalized[' '.join(name.casefold().split())].append(name)
    triples={(e['name'],r['predicate'],r['target']) for e in entries for r in e['relations']}
    unresolved=[];inverse=[];form_issues=[]
    reverse={'BT':'NT','NT':'BT','RT':'RT','USE':'UF','UF':'USE'}
    for e in entries:
        if e['form']=='nonpreferred' and not any(r['predicate']=='USE' for r in e['relations']):form_issues.append({'entry_id':e['id'],'reason':'nonpreferred entry without USE'})
        if e['form']=='preferred' and any(r['predicate']=='USE' for r in e['relations']):form_issues.append({'entry_id':e['id'],'reason':'preferred-style heading with USE'})
        for r in e['relations']:
            if r['target'] not in names:
                unresolved.append({'entry_id':e['id'],'subject':e['name'],'predicate':r['predicate'],'target':r['target'],
                    'normalized_candidates':normalized.get(' '.join(r['target'].casefold().split()),[])})
            if (r['target'],reverse[r['predicate']],e['name']) not in triples:
                inverse.append({'entry_id':e['id'],'subject':e['name'],'predicate':r['predicate'],'target':r['target']})
    return {'unresolved_targets':unresolved,'missing_inverse':inverse,'form_issues':form_issues,
            'source_groups_with_connectors':[{'entry_id':e['id'],'subject':e['name'],'group':group,'targets':[r['target'] for r in e['relations'] if r['source_group']==group],'note':'Source AND syntax retained; semantic interpretation not adopted.'} for e in entries for group in sorted({r['source_group'] for r in e['relations'] if r.get('connector_after')})],
            'duplicate_names':{name:ids for name,ids in names.items() if len(ids)>1},
            'empty_relations':[{'entry_id':e['id'],'predicate':r['predicate']} for e in entries for r in e['relations'] if not r['target']]}


def extract_ieee(acquisition,output, *, references=None):
    acquisition=Path(acquisition).resolve();acquisition_bytes=acquisition.read_bytes();record=json.loads(acquisition_bytes)
    filename=record.get('file','')
    if not filename or Path(filename).name!=filename:raise SourceError('acquisition file must name one local file')
    pdf=acquisition.parent/filename
    if pdf.is_symlink():raise SourceError('source PDF may not be a symbolic link')
    digest=hashlib.sha256(pdf.read_bytes()).hexdigest()
    if digest!=record.get('sha256'):raise SourceError('source PDF hash differs from acquisition record')
    target=Path(output).absolute()
    if target.exists() or target.is_symlink():raise SourceError('output must be a new directory')
    if acquisition.parent==target.resolve() or acquisition.parent in target.resolve().parents:raise SourceError('output cannot be inside the acquisition directory')
    lines,pages=pdf_lines(pdf);parsed=parse_lines(lines);checks=diagnose(parsed['entries'])
    assigned=sum(len(e['name_fragments'])+sum(len(r['fragments']) for r in e['relations']) for e in parsed['entries'])
    if assigned+len(parsed['unassigned'])!=len(lines):raise SourceError('source line accounting mismatch')
    result={'schema_version':1,'representation':'ieee-source-transcription','adoption':'not-adopted',
        'source':{'file':str(pdf),'sha256':digest,'version':record.get('observed_version'),'url':record.get('source_url'),
                  'acquisition_record':str(acquisition),'acquisition_sha256':hashlib.sha256(acquisition_bytes).hexdigest()},
        'extractor':{'profile':'ieee-july-2025-v1','pdfplumber':version('pdfplumber'),'pdfminer.six':version('pdfminer.six'),
                     'body_start_y':60,'minimum_font_size':9,'column_boundary_x':306,
                     'implementation_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        **pages,**parsed}
    _validate(result,'ieee-thesaurus')
    summary={'entries':len(parsed['entries']),'forms':dict(Counter(e['form'] for e in parsed['entries'])),
             'relations':dict(Counter(r['predicate'] for e in parsed['entries'] for r in e['relations'])),
             'input_lines':len(lines),'unassigned_lines':len(parsed['unassigned']),
             'diagnostics':{k:len(v) for k,v in checks.items()},'review_status':'requires-source-review',
             'note':'Diagnostics do not repair, merge or infer source relationships; counts do not prove semantic completeness.'}
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.ieee-',dir=target.parent) as tmp:
        stage=Path(tmp)/'result';stage.mkdir()
        for name,data in [('thesaurus.json',result),('diagnostics.json',checks),('report.json',summary)]:
            (stage/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        with (stage/'relations.csv').open('w',newline='') as f:
            writer=csv.writer(f);writer.writerow(['subject','predicate','object','entry_id','page','column','source_group','connector_after','raw_object'])
            for e in parsed['entries']:
                for r in e['relations']:
                    loc=r['fragments'][0]['locator'];writer.writerow([e['name'],r['predicate'],r['target'],e['id'],loc['page'],loc['column'],r['source_group'],r['connector_after'] or '',r['raw_target']])
        if references is not None:
            from kb_sources.ieee_reference import compare_reference
            (stage/'reference-inputs').mkdir()
            for key,name in [('thesaurus','ieee-thesaurus-2023.csv'),('taxonomy','ieee-taxonomy-2025.txt')]:
                source=references[key]['source'];raw=Path(source['path']).read_bytes()
                if hashlib.sha256(raw).hexdigest()!=source['sha256']:raise SourceError('reference input changed after reading')
                (stage/'reference-inputs'/name).write_bytes(raw);source['local_copy']='reference-inputs/'+name
            (stage/'references.json').write_text(json.dumps(references,ensure_ascii=False,indent=2)+'\n')
            comparison=compare_reference(parsed['entries'],references)
            (stage/'comparison.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2)+'\n')
        write_previews(stage,result,summary)
        receipt={'source':result['source'],'extractor':result['extractor'],'outputs':{str(p.relative_to(stage)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(stage.rglob('*')) if p.is_file()}}
        (stage/'record.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
        if acquisition.read_bytes()!=acquisition_bytes:raise SourceError('acquisition record changed during extraction')
        if hashlib.sha256(pdf.read_bytes()).hexdigest()!=digest:raise SourceError('source changed during extraction')
        if target.exists() or target.is_symlink():raise SourceError('output appeared during extraction')
        os.rename(stage,target)
    return summary


def write_previews(stage,result,summary):
    source=result['source']['file']
    lines=['# 词条索引','','以下是 IEEE 原文的首选与非首选词条记录，不是已采纳的本地概念。关系诊断见 diagnostics.json。','',
           '| 原文名称 | 原文形式 | 关系数 | 位置 |','|---|---|---|---|']
    for e in result['entries']:
        loc=e['locator'];name=e['name'].replace('|','\\|')
        lines.append(f'| {name} | {e["form"]} | {len(e["relations"])} | [第 {loc["page"]} 页，第 {loc["column"]} 栏](<{source}#page={loc["page"]}>) |')
    (stage/'terms.md').write_text('\n'.join(lines)+'\n')
    samples=['# 关系样例','','按原始关系符号展示；不添加反向关系，不解释为已采纳的本地上下位或同义关系。','']
    for name in ['Generative AI','Large language models','Retrieval augmented generation','Machine learning','Natural language processing','Acoustic metamaterials','CIM']:
        es=[e for e in result['entries'] if e['name']==name]
        for e in es:
            samples += ['**'+name+'**', '', f'[原文第 {e["locator"]["page"]} 页](<{source}#page={e["locator"]["page"]}>)','', '| 关系 | 目标 | 原文连接符 |','|---|---|---|']
            for r in e['relations']:samples.append(f'| {r["predicate"]} | {r["target"]} | {r["connector_after"] or ""} |')
            samples.append('')
    (stage/'samples.md').write_text('\n'.join(samples)+'\n')
    (stage/'index.md').write_text('# 词表提取结果\n\n'
        +f'原文版本：{result["source"]["version"]}；{summary["entries"]} 条词条记录。数量不是独立概念数，提取不表示正式采纳。\n\n'
        +'[词条索引](terms.md) · [关系样例](samples.md) · [完整数据](thesaurus.json) · [关系 CSV](relations.csv) · [诊断](diagnostics.json) · [运行报告](report.json)\n\n'
        +('对照材料：[旧版与层级文本](references.json) · [不同版本对照](comparison.json)。未匹配不直接证明提取错误。\n\n' if (stage/'references.json').exists() else '')
        +'原文 AND 写法保留在 source_group 与 connector_after 中，未解释其语义。未解析目标、缺少反向关系等均保留诊断，不自动改写原文。\n')
