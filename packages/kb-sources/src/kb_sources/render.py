"""Readable previews of extracted source structure, with original-file links."""
import html
import re
from urllib.parse import quote


def escape(text):
    return re.sub(r'([\\`*\[\]<>|])', r'\\\1', text)


def source_link(item, source):
    loc = item['locator']
    target = source['file_path']
    if loc.get('anchors'):
        target += '#' + quote(loc['anchors'][0], safe='=_-')
    elif loc.get('page'):
        target += f'#page={loc["page"]}'
    return f'[{escape(item["text"])}](<{target}>)'


def outline(document):
    lines = ['# 来源目录', '', '以下为来源文档的标题层级。推定层级和未解析部分见提取记录，不等于本地分类。', '']
    for h in document['headings']:
        lines.append('  ' * (h['level']-1) + '- ' + source_link(h, document['source']))
    return '\n'.join(lines)+'\n'


def table_html(table):
    lines = ['<table>']
    for row in range(table['rows']):
        lines.append('<tr>')
        for c in sorted((c for c in table['cells'] if c['row'] == row), key=lambda c: c['column']):
            tag = 'th' if c.get('header') else 'td'
            cell_body=cell_html(c['content']) if c.get('content') else html.escape(c['text']).replace(chr(10), '<br>')
            lines.append(f'<{tag} rowspan="{c["rowspan"]}" colspan="{c["colspan"]}">{cell_body}</{tag}>')
        lines.append('</tr>')
    lines.append('</table>')
    return '\n'.join(lines)


def reading(document):
    lines = ['# 来源正文', '', '按来源顺序展示提取结果；原文快照及定位信息保存在 JSON 中。', '']
    source = document['source']
    for item in sorted(document['headings']+document['blocks']+document['tables'], key=lambda x:x['order']):
        if item['id'].startswith('h'):
            lines += ['**'+source_link(item, source)+'**', '']
        elif item['id'].startswith('t'):
            lines += [table_html(item), '']
        else:
            value=escape(item['text'])
            if item['kind']=='list-item':
                value='  '*max(0,item.get('list_depth',1)-1)+'- '+value
            lines += [value, '']
    return '\n'.join(lines)+'\n'


def cell_html(content):
    parts=[]
    for item in sorted(content['headings']+content['blocks']+content['tables'],key=lambda x:x['order']):
        if item['id'].startswith('t'):
            parts.append(table_html(item))
        elif item['id'].startswith('h'):
            parts.append('<strong>'+html.escape(item['text'])+'</strong>')
        else:
            indent=max(0,item.get('list_depth',1)-1)*1.5
            parts.append(f'<div style="margin-left:{indent}em">'+html.escape(item['text'])+'</div>')
    return ''.join(parts)
