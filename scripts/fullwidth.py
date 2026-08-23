#!/usr/bin/env python3
"""把中文语境里的半角标点转为全角;「」→“ ”,『』→‘ ’。
跳过:代码块、行内代码、链接 URL、裸 URL、标题行。"""
import re, sys, pathlib

CJK = re.compile(r'[一-鿿　-〿＀-￯]')
MAP = {',': '，', ';': '；', ':': '：', '?': '？', '!': '！'}

def is_cjk(c): return bool(c) and bool(CJK.match(c))

def convert_text(t):
    out = []; stack = []
    i = 0; n = len(t)
    while i < n:
        c = t[i]
        prev = t[i-1] if i > 0 else ''
        nxt = t[i+1] if i+1 < n else ''
        # bare URL: copy through
        if t.startswith('http://', i) or t.startswith('https://', i):
            j = i
            while j < n and not t[j].isspace() and t[j] not in ')>]':
                j += 1
            out.append(t[i:j]); i = j; continue
        if c == '「': out.append('“'); i += 1; continue
        if c == '」': out.append('”'); i += 1; continue
        if c == '『': out.append('‘'); i += 1; continue
        if c == '』': out.append('’'); i += 1; continue
        if c == '(':
            if is_cjk(prev) or is_cjk(nxt):
                out.append('（'); stack.append(True)
            else:
                out.append('('); stack.append(False)
            i += 1; continue
        if c == ')':
            conv = stack.pop() if stack else (is_cjk(prev) or is_cjk(nxt))
            out.append('）' if conv else ')'); i += 1; continue
        if c in MAP and (is_cjk(prev) or is_cjk(nxt)):
            out.append(MAP[c]); i += 1; continue
        out.append(c); i += 1
    return ''.join(out)

def convert_line(line):
    if line.lstrip().startswith('#'): return line
    # split out inline code and link urls
    parts = re.split(r'(`[^`]*`|\]\([^)]*\)|<https?://[^>]*>)', line)
    return ''.join(p if (p.startswith('`') or p.startswith('](') or p.startswith('<http')) else convert_text(p) for p in parts)

def convert_file(path):
    src = path.read_text(encoding='utf-8')
    out = []; in_code = False
    for line in src.split('\n'):
        if line.strip().startswith('```'):
            in_code = not in_code; out.append(line); continue
        out.append(line if in_code else convert_line(line))
    new = '\n'.join(out)
    if new != src:
        path.write_text(new, encoding='utf-8'); return True
    return False

if __name__ == '__main__':
    changed = 0
    for p in sys.argv[1:]:
        if convert_file(pathlib.Path(p)): changed += 1; print('converted', p)
    print(changed, 'files changed')
