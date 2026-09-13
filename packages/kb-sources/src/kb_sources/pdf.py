"""Text PDF extraction with pdfplumber. Layout inferences remain explicitly marked."""
from collections import Counter
from io import BytesIO
import re
import statistics

import pdfplumber
from pdfminer.pdftypes import resolve1
from pdfplumber.utils import cluster_objects

from kb_sources.download import SourceError

MARKER = re.compile(r'^((?:\d+|[a-zA-Z]|[ivxlcdm]+)[.)]|[•●○▪■–])\s+')
MSC_CODE = re.compile(r'^(\d{2}(?:-XX|-[0-9]{2}|[A-Z](?:xx|[0-9]{2})))\s+')


def box(words):
    return [round(min(w['x0'] for w in words),3), round(min(w['top'] for w in words),3),
            round(max(w['x1'] for w in words),3), round(max(w['bottom'] for w in words),3)]


def contains(b, w):
    return b[0] <= (w['x0']+w['x1'])/2 <= b[2] and b[1] <= (w['top']+w['bottom'])/2 <= b[3]


def line_of(words):
    words = sorted(words,key=lambda w:w['x0'])
    # extra_attrs splits words at font changes. Preserve adjacency instead of inserting spaces there.
    text = words[0]['text']
    for prev, w in zip(words,words[1:]):
        threshold=min(w['size'],prev['size'])*.18 if w['fontname']!=prev['fontname'] else .5
        text += (' ' if w['x0']-prev['x1'] > threshold else '') + w['text']
    return {'text': text, 'bbox': box(words), 'size': round(statistics.median(w['size'] for w in words),1),
            'bold': sum(len(w['text']) for w in words if re.search(r'Bold|CMBX|CMBX',w['fontname'],re.I)) > sum(len(w['text']) for w in words)*.6}


def ordered_lines(words, width):
    """Use pdfplumber's row clustering; order contiguous split rows column-first."""
    rows=[]
    for row in cluster_objects(words,lambda w:round(w['top'],1),3):
        row=sorted(row,key=lambda w:w['x0']);parts=[[]]
        for w in row:
            if parts[-1] and w['x0']-parts[-1][-1]['x1'] > max(45,width*.07):
                parts.append([])
            parts[-1].append(w)
        # Right-aligned page references are part of a contents line, not a second column.
        if len(parts)>1 and all(re.fullmatch(r'[\divxlc]+',line_of(p)['text'],re.I) for p in parts[1:]):
            parts=[row]
        rows.append([line_of(p) for p in parts])
    result=[];pending=[]
    def flush():
        if pending:
            for col in range(max(len(row) for row in pending)):
                result.extend(row[col] for row in pending if col<len(row))
            pending.clear()
    for row in rows:
        if len(row)>1:
            pending.append(row)
        else:
            flush();result.extend(row)
    flush()
    return result


def msc_index_lines(words, width):
    """The printed MSC overview has two independent columns with unequal line heights."""
    starts=[w['top'] for w in words if re.fullmatch(r'\d{2}',w['text'])]
    if not starts:return ordered_lines(words,width)
    top=min(starts)-2
    header=[w for w in words if w['top']<top]
    left=[w for w in words if w['top']>=top and (w['x0']+w['x1'])/2<width/2]
    right=[w for w in words if w['top']>=top and (w['x0']+w['x1'])/2>=width/2]
    return ordered_lines(header,width)+ordered_lines(left,width)+ordered_lines(right,width)


def bookmarks(pdf):
    result=[];page_ids={p.page_obj.pageid:p.page_number for p in pdf.pages}
    try:
        for level,title,dest,action,_ in pdf.doc.get_outlines():
            try:
                d=dest or resolve1(action).get('D')
                if isinstance(d,(str,bytes)):
                    d=pdf.doc.get_dest(d)
                d=resolve1(d)
                if isinstance(d,dict):d=resolve1(d.get('D'))
                page=page_ids.get(d[0].objid) if isinstance(d,list) and d and hasattr(d[0],'objid') else None
                result.append({'level':level,'text':title,'page':page})
            except (TypeError,ValueError,KeyError,AttributeError):
                result.append({'level':level,'text':title,'page':None})
    except Exception:
        # Missing or malformed outlines must not suppress page content.
        return result
    return result


def heading_level(line, body, profile):
    text,size,bold=line['text'],line['size'],line['bold']
    if profile=='cs2023' and bold and re.match(r'^[A-Z]{2,4}[-/][A-Za-z][A-Za-z0-9/-]*(?::|\s|$)',text):return 3
    if profile=='msc2020':
        m=MSC_CODE.match(text)
        if m:
            if m[1].endswith('-XX'):return 1
            if m[1].endswith('xx'):return 2
            return None
    if profile=='ifla-lis-2022':
        if re.match(r'^FKA\d+[.]?\s',text) and (bold or size>body):return 3
        if re.match(r'^G\d+[.]?\s',text) and (bold or size>body):return 2
    if profile=='tekom-teaching-2018' and (bold or size>=12):
        m=re.match(r'^(\d+(?:\.\d+)*)(?:\.)?\s+[A-Z]',text)
        if m:return min(5,len(m[1].split('.')))
        if size>=11.8:return 4
    if profile=='tekom-teaching-2018' and 98<=line['bbox'][0]<=101 and abs(size-11)<.3 and len(text)<160:
        return 5
    if size < body+.8 or len(text)>250 or not re.search('[A-Za-z]',text):return None
    if profile=='cs2023':return 1 if size>=15 else 2 if size>=13 else 3
    if profile=='cwpa-writing-4-2026':return 1 if size>=19 else 2 if size>=15 else 3
    return 1 if size>=body*1.4 else 2 if size>=body*1.2 else 3


def parse_pdf(raw, profile='generic'):
    try:
        return _parse_pdf(raw,profile)
    except SourceError:raise
    except Exception as exc:
        raise SourceError(f'PDF parsing failed: {type(exc).__name__}: {exc}') from exc


def _parse_pdf(raw, profile):
    pages=[];sizes=Counter();edge_counts=Counter();warnings=[]
    with pdfplumber.open(BytesIO(raw),unicode_norm='NFC') as pdf:
        outline=bookmarks(pdf)
        for page in pdf.pages:
            words=page.extract_words(x_tolerance=1,x_tolerance_ratio=.07,y_tolerance=3,
                                     extra_attrs=['size','fontname'],expand_ligatures=True)
            sorter=msc_index_lines if profile=='msc2020' and page.page_number==1 else ordered_lines
            raw_lines=sorter(words,page.width) if words else []
            for w in words:sizes[round(w['size'],1)]+=len(w['text'])
            found=[]
            for table in page.find_tables():
                if len(table.rows)<2 or len(table.columns)<2:continue
                xs=sorted(set(x for c in table.cells for x in (c[0],c[2])))
                ys=sorted(set(y for c in table.cells for y in (c[1],c[3])))
                cells=[]
                for c in sorted(table.cells,key=lambda b:(b[1],b[0])):
                    cell_words=[w for w in words if contains(c,w)]
                    lines=ordered_lines(cell_words,page.width) if cell_words else []
                    cells.append({'row':ys.index(c[1]),'column':xs.index(c[0]),
                                  'rowspan':ys.index(c[3])-ys.index(c[1]),'colspan':xs.index(c[2])-xs.index(c[0]),
                                  'text':'\n'.join(l['text'] for l in lines),'header':False,'links':[],
                                  'locator':{'page':page.page_number,'bbox':list(c)}})
                if sum(bool(c['text'].strip()) for c in cells)<2:
                    continue  # A bordered text box is not a multi-cell data table.
                uncovered=[w for w in words if contains(table.bbox,w) and not any(contains(c,w) for c in table.cells)]
                if uncovered:
                    warnings.append(f'PDF page {page.page_number}: incomplete detected table grid; retained as positioned text to avoid losing words.')
                    continue
                found.append({'bbox':list(table.bbox),'rows':len(ys)-1,'columns':len(xs)-1,'cells':cells})
            outside=[w for w in words if not any(contains(c['locator']['bbox'],w) for t in found for c in t['cells'])]
            marker_words=[w for w in outside if profile=='tekom-teaching-2018' and w['size']<=2 and w['x0']<100 and re.fullmatch(r'[\uf0b7•·]|\(cid:\d+\)',w['text'])]
            content_words=[w for w in outside if w not in marker_words]
            lines=sorter(content_words,page.width) if content_words else []
            for l in lines:
                if l['bbox'][1]<page.height*.085 or l['bbox'][3]>page.height*.92:
                    edge_counts[re.sub(r'\d+','#',l['text'])]+=1
            links=[{'text':'','href':l['uri'],'bbox':[l['x0'],l['top'],l['x1'],l['bottom']]}
                   for l in page.hyperlinks if l.get('uri')]
            pages.append({'page':page.page_number,'width':page.width,'height':page.height,
                          'text':'\n'.join(l['text'] for l in raw_lines),'lines':raw_lines,
                          'image_count':len(page.images),'links':links,'markers':[line_of([w]) for w in marker_words],'_lines':lines,'_tables':found})
            if not words:
                warnings.append(f'PDF page {page.page_number}: no text layer; blank or image-only page, OCR not performed.')
            page.close()
    if not pages or not sizes:raise SourceError('PDF has no extractable text layer; OCR is not enabled')
    body=sizes.most_common(1)[0][0]
    headings=[];blocks=[];tables=[];stack=[];list_stack=[];order=0
    def section():return stack[-1]['id'] if stack else None
    for p in pages:
        previous=None
        events=[('line',l) for l in p.pop('_lines')]+[('table',t) for t in p.pop('_tables')]
        # Keep column-first line order; insert each table before the first line below it.
        line_events=[e for e in events if e[0]=='line']
        for e in (e for e in events if e[0]=='table'):
            pos=next((i for i,(_,l) in enumerate(line_events) if l['bbox'][1]>=e[1]['bbox'][1]),len(line_events))
            line_events.insert(pos,e)
        for kind,line in line_events:
            loc={'page':p['page'],'bbox':line['bbox']}
            if kind=='table':
                order+=1;tables.append({'id':f't{len(tables)+1}','order':order,'section':section(),'locator':loc,
                    'rows':line['rows'],'columns':line['columns'],'cells':line['cells'],
                    'method':'pdfplumber-ruled-table','text':'\n'.join(c['text'] for c in line['cells'])})
                previous=None;list_stack.clear();continue
            text=line['text'];bbox=line['bbox']
            if profile=='tekom-teaching-2018' and line['size']<=2 and bbox[0]<100 and re.fullmatch(r'[\uf0b7•·]',text):
                p['markers'].append(line)
                continue
            at_edge=bbox[1]<p['height']*.085 or bbox[3]>p['height']*.92
            if at_edge and ((len(pages)>1 and edge_counts[re.sub(r'\d+','#',text)]>=max(2,len(pages)*.4)) or re.fullmatch(r'\d+|[ivxlc]+',text,re.I)):
                continue
            level=heading_level(line,body,profile)
            code=MSC_CODE.match(text) if profile=='msc2020' else None
            if profile=='msc2020' and p['page']==1:
                code=re.match(r'^(\d{2})\s+',text)
            if profile=='cognitive-science-contents' and p['page']>=2:
                if re.fullmatch(r'[ivxlc]+ Contents',text,re.I):continue
                level=1 if text=='Contents' else 2 if re.match(r'^Part [IVX]+ ',text) else None
                code=re.match(r'^(\d{1,2})\s+',text)

            marker=MARKER.match(text) if not code else None
            links=[{'text':text,'href':l['href']} for l in p['links'] if l['bbox'][0]<bbox[2] and l['bbox'][2]>bbox[0] and l['bbox'][1]<bbox[3] and l['bbox'][3]>bbox[1]]
            if level:
                # Wrapped headings keep one identity and their complete source text.
                if previous and previous.get('_heading') and previous['level']==level and not code and not re.match(r'^\d+[.]?\s',text) and 0<=bbox[1]-previous['locator']['bbox'][3]<line['size']*.6:
                    previous['text']+=' '+text;previous['locator']['bbox'][2]=max(previous['locator']['bbox'][2],bbox[2]);previous['locator']['bbox'][3]=bbox[3];continue
                while stack and stack[-1]['level']>=level:stack.pop()
                order+=1;h={'id':f'h{len(headings)+1}','order':order,'text':text,'level':level,'parent':section(),
                           'locator':loc,'links':links,'method':'pdf-source-code' if code else 'pdf-layout-inferred'}
                headings.append(h);stack.append(h);previous=h;h['_heading']=True;list_stack.clear();continue
            tekom_item=profile=='tekom-teaching-2018' and line['bold'] and abs(line['size']-10)<.3 and bbox[0]>115
            is_list=bool(marker or code or tekom_item)
            if previous and not previous.get('_heading') and not is_list and previous['locator']['page']==p['page']:
                pb=previous['locator']['bbox'];gap=bbox[1]-pb[3]
                if -.5<=gap<=body*.85 and abs(bbox[0]-pb[0])<25 and abs(line['size']-previous['_size'])<.5 and line['bold']==previous['_bold'] and not text.startswith('Ressource:'):
                    previous['text']+='\n'+text;pb[2]=max(pb[2],bbox[2]);pb[3]=bbox[3];previous['links']+=links;continue
            order+=1;b={'id':f'b{len(blocks)+1}','order':order,'text':text,'section':section(),'locator':loc,
                       'kind':'list-item' if is_list else 'paragraph','links':links,'in_table':False,'_size':line['size'],'_bold':line['bold']}
            if is_list:
                while list_stack and list_stack[-1]['locator']['bbox'][0]>=bbox[0]-3:list_stack.pop()
                b.update(marker=code[1] if code else marker[1] if marker else '•',list_depth=len(list_stack)+1,
                         list_parent=list_stack[-1]['id'] if list_stack else None,method='pdf-source-code' if code else 'tekom-entry-style' if tekom_item else 'pdf-indentation-inferred')
                list_stack.append(b)
            else:list_stack.clear()
            blocks.append(b);previous=b
    for h in headings:h.pop('_heading',None)
    for b in blocks:
        b.pop('_size',None);b.pop('_bold',None)
    if profile=='tekom-teaching-2018':
        warnings.append('Tiny bullet glyphs are retained in page markers, not mixed into entry text. Graphical level symbols are not interpreted.')
    if profile=='cognitive-science-contents':
        warnings.append('Scanned contents has OCR artifacts in its existing text layer (for example printed page numbers). No OCR correction is applied; verify against page images.')
    warnings.append('PDF heading/list hierarchy is inferred from typography, source numbering and indentation; verify before vocabulary use.')
    warnings.append('Only ruled table grids are reconstructed. Borderless tables and cross-page continuations remain in positioned text; no automatic merge.')
    warnings.append('PDF text is extracted from embedded characters, not OCR. Figures and formula layout are not reconstructed; raw page lines remain available.')
    return {'profile':profile,'encoding':None,'headings':headings,'blocks':blocks,'tables':tables,
            'pages':pages,'bookmarks':outline,'warnings':warnings}
