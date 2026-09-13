"""Offline source conversion, provenance, and non-overwriting publication."""
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
from urllib.parse import urljoin

from kb_sources import __version__
from kb_sources.download import SourceError, verify, _validate
from kb_sources.html import parse_html
from kb_sources.render import outline, reading

HTML_PROFILES={'how-people-learn-ii-2018-outline':'nap','sep-summer-2026-outline':'sep'}


def _target(output, snapshots):
    target=Path(output).absolute()
    if target.exists() or target.is_symlink():raise SourceError('extraction output must not already exist')
    for snapshot in snapshots:
        if Path(snapshot).resolve()==target.resolve() or Path(snapshot).resolve() in target.resolve().parents:
            raise SourceError('extraction must not write inside the source snapshot')
    return target


def _resolve_links(value,url):
    if isinstance(value,dict):
        if 'href' in value:value['url']=urljoin(url,value['href'])
        for item in value.values():_resolve_links(item,url)
    elif isinstance(value,list):
        for item in value:_resolve_links(item,url)


def _validate_structure(result):
    _validate(result,'structure')
    _check_refs(result)


def _check_refs(result):
    records=result['headings']+result['blocks']+result['tables']
    by_id={r['id']:r for r in records}
    if len(by_id)!=len(records) or len({r['order'] for r in records})!=len(records):
        raise SourceError('duplicate extracted record identity or order')
    for r in records:
        for field in ('parent','section','list_parent'):
            ref=r.get(field)
            if ref and (ref not in by_id or by_id[ref]['order']>=r['order']):
                raise SourceError(f'invalid extracted {field} in {r["id"]}')
    for table in result['tables']:
        for cell in table['cells']:
            if cell.get('content'):_check_refs(cell['content'])


def extract_file(snapshot, file_id, output, *, expected_format=None):
    snapshot=Path(snapshot).absolute();target=_target(output,[snapshot])
    receipt=verify(snapshot)
    candidates=[f for f in receipt['files'] if f['id']==file_id]
    if len(candidates)!=1:raise SourceError('file-id must identify one file in the snapshot')
    item=candidates[0]
    if item['format'] not in ('html','pdf'):
        raise SourceError('native structured source: read the verified snapshot file directly; no document extraction is needed')
    if expected_format and item['format']!=expected_format:raise SourceError(f'file-id must identify one {expected_format.upper()} file')
    source_path=snapshot/item['filename'];raw=source_path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=item['sha256']:raise SourceError('source changed after snapshot verification')
    if item['format']=='html':
        parsed=parse_html(raw,HTML_PROFILES.get(receipt['source']['id'],'generic'))
        extractor={'name':'beautifulsoup4','version':version('beautifulsoup4'),'backend':'html.parser','profile':'html-structure-v2'}
    else:
        from kb_sources.pdf import parse_pdf
        pdf_profile='cognitive-science-contents' if receipt['source']['id']=='cognitive-science-2012-outline' and file_id=='contents-and-title-page' else receipt['source']['id']
        parsed=parse_pdf(raw,pdf_profile)
        extractor={'name':'pdfplumber','version':version('pdfplumber'),'pdfminer_version':version('pdfminer.six'),
                   'profile':'pdf-layout-v2','ocr':False,'images':False,'x_tolerance':1,'x_tolerance_ratio':.07,'y_tolerance':3}
    implementation=hashlib.sha256()
    for name in ('html.py','pdf.py','render.py','structure.py','schemas/structure.json'):
        implementation.update(name.encode()+b'\0'+Path(__file__).parent.joinpath(name).read_bytes())
    extractor['implementation_sha256']=implementation.hexdigest()
    result={'schema_version':2,'representation':'source-document-structure',
            'source':{**receipt['source'],'snapshot_id':snapshot.name,'file_id':file_id,'file_path':str(source_path),
                      'sha256':item['sha256'],'url':item['final_url']},
            'extractor':{**extractor,'python_version':platform.python_version(),'package_version':__version__},**parsed}
    _resolve_links(result,item['final_url']);_validate_structure(result)
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.extracting-',dir=target.parent) as tmp:
        stage=Path(tmp)/'result';stage.mkdir()
        (stage/'structure.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        (stage/'outline.md').write_text(outline(result));(stage/'reading.md').write_text(reading(result))
        record={'source':result['source'],'extractor':result['extractor'],
                'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(stage.iterdir())}}
        (stage/'record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
        # A source that changed during conversion cannot publish a result under its old identity.
        verify(snapshot)
        if target.exists() or target.is_symlink():raise SourceError('extraction output appeared while processing; refusing to replace it')
        os.rename(stage,target)
    return result


def extract_html(snapshot,file_id,output):
    """Compatibility entry point; the output format is now schema_version 2."""
    return extract_file(snapshot,file_id,output,expected_format='html')


def discover_snapshots(root):
    root=Path(root)
    paths=sorted(p.parent for p in root.glob('*/*/receipt.json'))
    if not paths:raise SourceError('no snapshots found under source root')
    names=[p.parent.name for p in paths]
    if len(set(names))!=len(names):raise SourceError('multiple snapshots for one source; use repeated --snapshot arguments to choose explicitly')
    return paths


def extract_all(snapshots, output):
    snapshots=[Path(s).absolute() for s in snapshots]
    if not snapshots:raise SourceError('at least one snapshot is required')
    target=_target(output,snapshots)
    if len(set(snapshots))!=len(snapshots):raise SourceError('duplicate snapshot input')
    # Establish the batch from verified receipts before creating any output.
    inputs=[(s,verify(s)) for s in snapshots]
    keys=[(r['source']['id'],s.name) for s,r in inputs]
    if len(set(keys))!=len(keys):raise SourceError('duplicate source/snapshot identities')
    report={'schema_version':1,'parsed':0,'native':0,'failed':0,'files':[]}
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.batch-',dir=target.parent) as tmp:
        stage=Path(tmp)/'result';stage.mkdir()
        for snapshot,receipt in inputs:
            sid=receipt['source']['id']
            for item in receipt['files']:
                rel=Path(sid)/snapshot.name/item['id']
                entry={'source_id':sid,'snapshot_id':snapshot.name,'file_id':item['id'],'format':item['format'],'output':str(rel)}
                if item['format'] not in ('html','pdf'):
                    entry.update(status='native_structured',output=None,source_file=str(snapshot/item['filename']),sha256=item['sha256'],warnings=[])
                    report['native']+=1;report['files'].append(entry)
                    continue
                print(f'Parsing {sid}/{item["id"]} ({item["format"]})',file=sys.stderr,flush=True)
                try:
                    result=extract_file(snapshot,item['id'],stage/rel)
                    entry.update(status='parsed_with_warnings' if result['warnings'] else 'parsed',
                        headings=len(result['headings']),blocks=len(result['blocks']),tables=len(result['tables']),
                        pages=len(result['pages']),warnings=result['warnings'])
                    report['parsed']+=1
                except (SourceError,OSError,ValueError) as exc:
                    entry.update(status='failed',error=str(exc));report['failed']+=1
                report['files'].append(entry)
        (stage/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        lines=['# 解析结果','','解析完成表示已取得结构化输出，不代表词表或内容已经核准。详细限制见各文件的 warnings。','',
               '| 来源 | 文件 | 结果 | 预览 |','|---|---|---|---|']
        for e in report['files']:
            preview=f'[正文](<{e["output"]}/reading.md>) · [结构](<{e["output"]}/structure.json>)' if e['status']!='failed' else escape_error(e['error'])
            if e['status']=='native_structured':preview=f'[原始结构化数据](<{e["source_file"]}>)'
            lines.append(f'| {e["source_id"]} | {e["file_id"]} | {e["status"]} | {preview} |')
        (stage/'index.md').write_text('\n'.join(lines)+'\n')
        if target.exists() or target.is_symlink():raise SourceError('batch output appeared while processing')
        os.rename(stage,target)
    return report


def escape_error(text):
    return text.replace('|','\\|').replace('\n',' ')
