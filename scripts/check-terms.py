#!/usr/bin/env python3
"""扫 concepts/ 与 design/ 正文里像术语的东西（加粗、引号），列出不在术语表里的。
只报告，不改。规则见 design/governance.md「术语准入」。"""
import re, pathlib, collections, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
gl = (ROOT / 'concepts' / 'glossary.md').read_text(encoding='utf-8')
known = set()
for line in gl.split('\n'):
    if line.startswith('| ') and not line.startswith('| 术语') and not line.startswith('|---'):
        cells = [c.strip() for c in line.strip('|').split('|')]
        for c in cells[:2]:
            for part in re.split(r'\s*/\s*|、|，|,', c):
                part = re.sub(r'[`*]', '', part).strip()
                if part: known.add(part.lower())
STOP = {'本库', '例', '待定', '来源', '规则', '例子', '说明', '其他', '注', '字段', '文件', '内容', '问题', '定义', '对象',
        '权威来源', '待定事项', '待办事项', '解决的问题', '在知识库中的用法', '在知识库中', '与受控词表的关系', '背景', '决定', '后果',
        '何时重新考虑', '文章的关系', '阅读顺序', '建设流程', '校验规则', '触发条件', '生命周期', '触发与动作', '记录', '相关', '标准'}
# 词表里的标签算已知
import yaml
for f in ('topics.yaml', 'entities.yaml', 'types.yaml'):
    d = yaml.safe_load(open(ROOT / 'vocab' / f))
    for x in d.get('concepts', []) + d.get('entities', []) + d.get('types', []):
        for v in x['label'].values(): known.add(v.lower())

hits = collections.defaultdict(set)
files = [p for p in list((ROOT/'concepts').glob('*.md')) + list((ROOT/'design').rglob('*.md')) if p.name not in ('glossary.md',)]
for p in files:
    in_code = False
    for line in p.read_text(encoding='utf-8').split('\n'):
        if line.strip().startswith('```'): in_code = not in_code; continue
        if in_code: continue
        text = re.sub(r'`[^`]*`', '', line)
        text = re.sub(r'\]\([^)]*\)', ']', text)
        cands = re.findall(r'\*\*([^*]{2,14})\*\*', text)
        cands += [q for q in re.findall(r'“([^”]{2,10})”', text) if not re.search(r'[、，。？！……：；]', q) and len(q) <= 6]
        if text.startswith('#'): continue   # 节名不是术语
        for c in cands:
            c = c.strip('：:，,。；;（）() ')
            if not re.search(r'[一-鿿]', c): continue
            if c.lower() in known or c in STOP: continue
            if re.fullmatch(r'[按由在与和或的是不有]?.{0,1}', c): continue
            hits[c].add(str(p.relative_to(ROOT)))

rows = sorted(hits.items(), key=lambda kv: (-len(kv[1]), kv[0]))
print(f'术语表已收 {len(known)} 个写法；扫到 {len(rows)} 个未登记的候选（按出现文件数排）')
for term, fs in rows:
    if len(fs) >= (2 if '--all' not in sys.argv else 1):
        print(f'  {term:<18} {len(fs):>2}  {", ".join(sorted(fs))[:90]}')
