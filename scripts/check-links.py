#!/usr/bin/env python3
"""检查仓库内 Markdown 的相对链接与锚点是否存在。外部 URL 不查。"""
import json, os, re, sys, pathlib, unicodedata

root = pathlib.Path(__file__).resolve().parent.parent
# Historical decisions and the frozen README retain their original path context.
migration = json.loads((root / 'work/plans/2026-09-05-monorepo-files.json').read_text())
historical = {'README.md'} | {
    row['new'] for row in migration['files']
    if row['new'] and (row['old'].startswith('design/decisions/')
                       or row['old'] == 'vocab/CHANGELOG.md')
}
excluded_dirs = {'.git', '.venv', '.superpowers', '__pycache__', 'output', 'build'}
files = []
for directory, children, names in os.walk(root):
    children[:] = [name for name in children if name not in excluded_dirs]
    relative = pathlib.Path(directory).relative_to(root).as_posix()
    if relative.startswith(('tests/fixtures', 'work/archive', 'data/audit')):
        children[:] = []
        continue
    files.extend(pathlib.Path(directory) / name for name in names if name.endswith('.md'))

def slug(h):
    h = h.strip().lower()
    h = re.sub(r'[`*_]', '', h)
    h = re.sub(r'[^\w\s一-鿿-]', '', h)
    return re.sub(r'\s+', '-', h)

headings = {}
for p in files:
    hs = set()
    in_code = False
    for line in p.read_text(encoding='utf-8').split('\n'):
        if line.strip().startswith('```'): in_code = not in_code; continue
        if not in_code and line.startswith('#'):
            hs.add(slug(line.lstrip('#')))
    headings[p] = hs

bad = 0
link = re.compile(r'\[[^\]]*\]\(([^)\s]+)\)')
for p in files:
    if p.relative_to(root).as_posix() in historical:
        continue
    in_code = False
    for n, line in enumerate(p.read_text(encoding='utf-8').split('\n'), 1):
        if line.strip().startswith('```'): in_code = not in_code; continue
        if in_code: continue
        line = re.sub(r'`[^`]*`', '', line)
        for m in link.finditer(line):
            t = m.group(1)
            if t.startswith(('http://', 'https://', 'mailto:')): continue
            path, _, anchor = t.partition('#')
            target = (p.parent / path).resolve() if path else p
            if path and not target.exists():
                print(f'{p.relative_to(root)}:{n}: 文件不存在 {t}'); bad += 1; continue
            if anchor and target.suffix == '.md' and anchor not in headings.get(target, set()):
                print(f'{p.relative_to(root)}:{n}: 锚点不存在 {t}'); bad += 1
print(f'{bad} 处问题' if bad else '全部链接有效')
sys.exit(1 if bad else 0)
