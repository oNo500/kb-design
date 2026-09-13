"""HTML document extraction; selectors describe source layout, not local concepts."""
from collections import Counter
import re
from bs4 import BeautifulSoup, Tag, NavigableString, Comment
from kb_sources.download import SourceError

HEADINGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
CONTAINERS = HEADINGS + ['p', 'li', 'dt', 'dd', 'pre', 'blockquote', 'table']


def locator(tag):
    anchors = ([tag['id']] if tag.get('id') else [])
    anchors += [a.get('id') or a.get('name') for a in tag.find_all('a') if a.get('id') or a.get('name')]
    return {'line': tag.sourceline, 'column': tag.sourcepos, 'tag': tag.name,
            'anchors': list(dict.fromkeys(anchors))}


def text_of(tag, own_list=False):
    strings = tag.strings
    if own_list:
        strings = (s for s in strings if s.find_parent('li') is tag)
    return ' '.join(''.join(str(s) for s in strings).split())


def links_of(tag, own_list=False):
    return [{'text': text_of(a), 'href': a['href']} for a in tag.find_all('a', href=True)
            if not own_list or a.find_parent('li') is tag]


def cell_text(tag):
    def walk(node):
        if isinstance(node,Comment):return ''
        if isinstance(node,NavigableString):return str(node)
        value=''.join(walk(c) for c in node.children)
        return '\n'+value+'\n' if node.name in ('p','li','div','tr','br','dt','dd') else value
    return '\n'.join(' '.join(line.split()) for line in walk(tag).splitlines() if line.strip())


def within_parent(tag, names, root):
    for parent in tag.parents:
        if parent is root:return False
        if parent.name in names:return True
    return False


def table_of(tag, table_id, order, section):
    cells, occupied = [], set()
    rows = [r for r in tag.find_all('tr') if r.find_parent('table') is tag]
    for row, tr in enumerate(rows):
        col = 0
        for td in tr.find_all(['td', 'th'], recursive=False):
            while (row, col) in occupied:
                col += 1
            try:
                rs, cs = int(td.get('rowspan', 1)), int(td.get('colspan', 1))
            except ValueError as exc:
                raise SourceError('Invalid HTML table span') from exc
            if rs == 0:
                rs = len(rows) - row
            if not (1 <= rs <= 1000 and 1 <= cs <= 1000):
                raise SourceError('HTML table span exceeds supported bounds')
            cells.append({'row': row, 'column': col, 'rowspan': rs, 'colspan': cs,
                          'text': cell_text(td), 'header': td.name == 'th',
                          'links': links_of(td), 'locator': locator(td)})
            if td.find(CONTAINERS) and cells[-1]['text']:
                cells[-1]['content']=parse_html(None,_root=td)
            occupied.update((r, c) for r in range(row, row+rs) for c in range(col, col+cs))
            col += cs
    return {'id': table_id, 'order': order, 'section': section, 'locator': locator(tag),
            'rows': max((r+1 for r, c in occupied), default=0),
            'columns': max((c+1 for r, c in occupied), default=0), 'cells': cells,
            'method': 'html-table', 'text': text_of(tag)}


def parse_html(raw, profile='generic', *, _root=None):
    soup = _root if _root is not None else BeautifulSoup(raw, 'html.parser')
    warnings = []
    if soup.contains_replacement_characters:
        warnings.append('Character decoding introduced replacement characters; inspect the source.')
    if _root is not None:
        roots=[_root]
    elif profile == 'nap':
        roots = soup.select('#openbook-html .page-html')
    elif profile == 'sep':
        roots = soup.select('#content')
    else:
        roots = [soup.body or soup]
    if not roots:
        raise SourceError(f'Expected HTML body selector missing for profile {profile}')
    for tag in soup.select('nav, script, style, header, footer, form'):
        tag.decompose()
    for br in soup.find_all('br'):
        br.replace_with('\n')
    for tag in soup.find_all(class_=lambda c: c and c.startswith('MsoToc')):
        tag.decompose()
    # SEP jump links are navigation, not part of alphabetical heading labels.
    if profile == 'sep':
        for a in soup.find_all('a'):
            if 'jump to top' in a.get_text():
                a.decompose()
    headings, blocks, tables, stack, word_stack, li_ids = [], [], [], [], [], {}
    order = 0
    unresolved = {}

    def section():
        return stack[-1]['id'] if stack else None

    for root in roots:
        for tag in root.descendants:
            if not isinstance(tag, Tag) or tag.name not in CONTAINERS:
                continue
            if within_parent(tag, ['table'], root):
                continue
            if tag.name != 'li' and within_parent(tag, CONTAINERS, root):
                continue
            value = text_of(tag, tag.name == 'li')
            if not value:
                continue
            order += 1
            if tag.name == 'table':
                tables.append(table_of(tag, f't{len(tables)+1}', order, section()))
                word_stack.clear()
                continue
            if tag.name in HEADINGS:
                level = int(tag.name[1])
                while stack and stack[-1]['level'] >= level:
                    stack.pop()
                h = {'id': f'h{len(headings)+1}', 'order': order, 'level': level, 'text': value,
                     'parent': section(), 'locator': locator(tag), 'links': links_of(tag), 'method': 'html-heading'}
                headings.append(h);stack.append(h);word_stack.clear()
                continue
            b = {'id': f'b{len(blocks)+1}', 'order': order, 'kind': 'paragraph', 'text': value,
                 'section': section(), 'locator': locator(tag), 'links': links_of(tag, tag.name == 'li'),
                 'in_table': False}
            style = tag.get('style', '')
            if style:
                b['source_style'] = style
            word = re.search(r'mso-list:\s*(l\d+)\s+level(\d+)\s+(lfo\d+)', style)
            following = tag.find_next_sibling()
            printed = re.match(r'^(\d+[.)])\s+', value) if tag.name=='p' and 'MsoNormal' in tag.get('class',[]) else None
            follows_word_child = following is not None and re.search(r'mso-list:.*level[2-9] ', following.get('style',''))
            if printed and not word and follows_word_child:
                word_stack.clear()
                b.update(kind='list-item', list_depth=1, list_parent=None, marker=printed[1], method='printed-number-context')
                word_stack.append(b)
            elif word:
                depth = int(word[2])
                while word_stack and word_stack[-1]['list_depth'] >= depth:
                    word_stack.pop()
                marker_tag = tag.find(style=re.compile(r'mso-list:\s*Ignore', re.I))
                b.update(kind='list-item', list_depth=depth, list_parent=word_stack[-1]['id'] if word_stack else None,
                         marker=text_of(marker_tag) if marker_tag else '', list_id=f'{word[1]}-{word[3]}', method='word-list-style')
                if depth > 1 and not word_stack:
                    key=(word[1],word[3],section())
                    first,count=unresolved.get(key,(tag.sourceline,0));unresolved[key]=(first,count+1)
                word_stack.append(b)
            elif tag.name == 'li':
                parent = tag.find_parent('li')
                container = tag.find_parent(['ol', 'ul'])
                marker = '•'
                if container and container.name == 'ol':
                    index = int(container.get('start', 1))
                    for sibling in container.find_all('li', recursive=False):
                        index = int(sibling.get('value', index))
                        if sibling is tag:
                            break
                        index += 1
                    marker = f'{index}.'
                b.update(kind='list-item', list_depth=len(tag.find_parents(['ol', 'ul'])),
                         list_parent=li_ids.get(id(parent)), marker=marker, method='html-list')
                li_ids[id(tag)] = b['id'];word_stack.clear()
            else:
                indent = re.search(r'margin-left:\s*([.\d]+)(in|pt|px)', style)
                if not indent or float(indent[1]) == 0:
                    word_stack.clear()
            blocks.append(b)
    warnings += [f'Word list {key[0]}-{key[1]} at HTML line {first}: {count} items have no explicit parent; original depth retained.' for key,(first,count) in unresolved.items()]
    anchors = Counter(a for h in headings for a in h['locator']['anchors'])
    warnings += [f'Duplicate heading anchor {a!r}; use source line and column.' for a, n in anchors.items() if n > 1]
    if not headings and _root is None:
        warnings.append('No explicit HTML headings; content retained without an invented hierarchy.')
    if not (headings or blocks or tables):
        raise SourceError('No extractable HTML content in the selected body')
    return {'encoding': soup.original_encoding, 'profile': profile, 'headings': headings,
            'blocks': blocks, 'tables': tables, 'pages': [], 'bookmarks': [], 'warnings': warnings}
