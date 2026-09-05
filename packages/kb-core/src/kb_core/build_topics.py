#!/usr/bin/env python3
"""从 data/inputs/topics/ 的输入生成 data/vocab/topics.yaml。设计见 docs/design/model/topics.md、docs/design/model/hierarchy.md。"""
from kb_core.repository import project_root
import json, re, sys, pathlib, yaml
from kb_core.label_adoptions import apply_adoptions, load_adoptions
ROOT = project_root()
B = ROOT / 'data/inputs/topics'
from kb_core.gbt_en import en_of

TODAY = '2026-08-23'
VERSION = '2026.08'

def slug(s):
    s = s.lower().replace('&', ' and ')
    s = re.sub(r"[^a-z0-9]+", '-', s).strip('-')
    return s

concepts = {}   # id -> dict
arrays = []

def add(cid, zh, en, broader, source, match=None, status='unassigned', arr=None, translated=None, scope=None, basis=None):
    """同一上位下同名（同 id）概念来自第二个来源时合并：加 match、加 arrays。"""
    if cid in concepts:
        c = concepts[cid]
        if c['broader'] != broader:
            cid2 = f"{cid}-{broader[0]}"
            return add(cid2, zh, en, broader, source, match, status, arr, translated, scope, basis)
        if match and match not in c['match']: c['match'].append(match)
        if arr and arr not in c['arrays']: c['arrays'].append(arr)
        return cid
    c = {'id': cid, 'label': {'zh': zh, 'en': en}, 'broader': broader, 'source': source,
         'match': [match] if match else [], 'arrays': [arr] if arr else [], 'status': status, 'added': TODAY}
    # 标签依据：translated 里的语言为本库所译（self），另一语言来自来源
    c['basis'] = basis or {'zh': 'self' if 'zh' in (translated or []) else 'source', 'en': 'self' if 'en' in (translated or []) else 'source'}
    if scope: c['scope'] = scope
    concepts[cid] = c
    return cid

# ---------- 顶层：范围决定 ----------
# 顶层：id 由范围声明决定（人定）；英文标签按译名阶梯，Wikidata 有则取，无则不给
TOPS = [
 ('mathematics','数学','mathematics','110','wikidata:Q395'),
 ('information-and-systems-science','信息科学与系统科学','','120','none'),
 ('computing','计算机科学技术','','520','none'),
 ('management','管理学','management','630','wikidata:Q2920921'),
 ('linguistics','语言学','linguistics','740','wikidata:Q8162'),
 ('journalism-and-communication','新闻学与传播学','','860','none'),
 ('library-and-information-science','图书馆、情报与文献学','','870','none'),
 ('education','教育学','pedagogy','880','wikidata:Q7922'),
]
for cid, zh, en, code, enb in TOPS:
    add(cid, zh, en, [], 'self', {'source':'gbt-13745','id':code,'rel':'exactMatch'}, status='active', basis={'zh':'gbt-13745','en':enb})

# ---------- computing：CS2023 ----------
kus = json.load(open(B/'cs2023-kus.json'))
zh = json.load(open(B/'cs2023-zh.json'))
ka_ids = {}
for ka, d in kus.items():
    cid = slug(d['name'])
    ka_ids[ka] = cid
    add(cid, zh[ka], d['name'], ['computing'], 'cs2023', {'source':'cs2023','id':ka,'rel':'exactMatch'}, translated=['zh'])
for ka, d in kus.items():
    parent = ka_ids[ka]
    arr = f"{parent}-cs2023"
    arrays.append({'id': arr, 'superordinate': parent, 'source': 'cs2023'})
    for code, name in d['kus'].items():
        add(slug(name), zh[code], name, [parent], 'cs2023', {'source':'cs2023','id':code,'rel':'exactMatch'}, arr=arr, translated=['zh'])

# ---------- 额外数组 ----------
extra = json.load(open(B/'extra-arrays.json'))
for parent, srcs in extra.items():
    if not any(a['superordinate']==parent and a['source']=='cs2023' for a in arrays):
        raise SystemExit(f'{parent} 无 cs2023 数组')
    for src, d in srcs.items():
        arr = f"{parent}-{src}"
        arrays.append({'id': arr, 'superordinate': parent, 'source': src})
        for code, en, zhn in d['items']:
            add(slug(en), zhn, en, [parent], src, {'source':src,'id':code,'rel':'exactMatch'}, arr=arr,
                translated=[] if d.get('zh_basis')=='source' else ['zh'])

# ---------- 其余七个顶层：GB/T 13745 ----------
gbt = json.load(open(B/'gbt-13745.json'))
LIS = [('870.10','图书馆学',[('870.1010','图书馆学史'),('870.1015','比较图书馆学'),('870.1020','图书馆社会学'),('870.1025','图书馆管理学'),('870.1030','图书馆建筑学'),('870.1035','图书采访学'),('870.1040','图书分类学'),('870.1045','图书编目学'),('870.1050','目录学'),('870.1055','图书馆服务学'),('870.1099','图书馆学其他学科')]),
 ('870.20','文献学',[('870.2010','文献类型学'),('870.2020','文献计量学'),('870.2030','文献检索学'),('870.2040','图书史'),('870.2050','版本学'),('870.2060','校勘学'),('870.2099','文献学其他学科')]),
 ('870.30','情报学',[('870.3010','情报学史'),('870.3015','情报社会学'),('870.3020','比较情报学'),('870.3025','情报计量学'),('870.3030','情报心理学'),('870.3035','情报管理学'),('870.3040','情报服务学'),('870.3045','情报经济学'),('870.3050','情报检索学'),('870.3055','情报系统理论'),('870.3060','情报技术'),('870.3065','科学技术情报学'),('870.3070','社会科学情报学'),('870.3099','情报学其他学科')]),
 ('870.40','档案学',[('870.4010','档案学史'),('870.4020','档案管理学'),('870.4030','档案保护技术学'),('870.4040','档案编纂学'),('870.4099','档案学其他学科')]),
 ('870.50','博物馆学',[])]
gbt['870'] = ['图书馆、情报与文献学', LIS]
top_of = {code: cid for cid,_,_,code,_ in TOPS}
for code in ['110','120','630','740','860','870','880']:
    top = top_of[code]
    _, subs = gbt[code]
    for sc, sn, thirds in subs:
        zh2 = re.sub(r'[（(].*', '', sn).strip()
        en2 = en_of(sn)
        c2 = add(slug(en2), zh2, en2, [top], 'gbt-13745', {'source':'gbt-13745','id':sc,'rel':'exactMatch'}, translated=['en'])
        for tc, tn in thirds:
            zh3 = re.sub(r'[（(].*', '', tn).strip()
            en3 = en_of(tn)
            add(slug(en3), zh3, en3, [c2], 'gbt-13745', {'source':'gbt-13745','id':tc,'rel':'exactMatch'}, translated=['en'])

# ---------- 邻近主题的多层级 ----------
# 软件工程管理同时在 management 之下（docs/design/model/topics.md 邻近主题）
sem = slug('Software Engineering Management')
if sem in concepts and 'management' not in concepts[sem]['broader']:
    concepts[sem]['broader'].append('management')
# 数学与统计基础与顶层 mathematics 多层级
msf = slug('Mathematical and Statistical Foundations')
if msf in concepts: concepts[msf]['broader'].append('mathematics')

# ---------- 有下位的概念按现行维护规则批准 ----------
parent_ids = {parent for c in concepts.values() for parent in c['broader']}
for parent_id in parent_ids:
    if concepts[parent_id]['status'] == 'unassigned':
        concepts[parent_id]['status'] = 'active'

# ---------- 译名回查：本库自译的标签按译名阶梯处理 ----------
# data/inputs/topics/label-decisions.json 是 lookup-labels.py 结果经人工审核后的决定（治理“译名”第 3 级）。
# 本段保留原有 Wikidata 采纳结果与否决；其余先记 none，不证明新阶梯已穷尽。
# 结构化译名采纳在 scope 生成后独立应用，不覆盖历史 Q 号记录。
decisions = json.load(open(B/'label-decisions.json'))
for c in concepts.values():
    for lang in ('zh','en'):
        if c['basis'][lang] != 'self': continue
        dec = decisions.get(f"{c['id']}.{lang}")
        if dec and dec['accept']:
            c['label'][lang] = dec['label']; c['basis'][lang] = f"wikidata:{dec['q']}"
        else:
            c['label'][lang] = ''; c['basis'][lang] = 'none'

# ---------- 不译概念的范围注释 ----------
# 当前无已消费译名时给解释；不等于已穷尽扩展后的译名阶梯。键为 来源:条目编号。
scopes = json.load(open(B/'scope-zh.json'))
for c in concepts.values():
    if c.get('scope') or c['label'].get('zh'): continue
    for m in c['match']:
        sc = scopes.get(f"{m['source']}:{m['id']}:{c['label']['en']}") or scopes.get(f"{m['source']}:{m['id']}")
        if sc: c['scope'] = sc; break

# ---------- 已授权译名与语言依据 ----------
# 在范围说明生成后应用，避免补上中文时丢失原有 scope。
sources_document = yaml.safe_load((ROOT/'data/vocab'/'sources.yaml').read_text(encoding='utf-8'))
source_index = {record['id']: record for record in sources_document['sources']}
apply_adoptions(list(concepts.values()), 'topics', load_adoptions(ROOT), source_index)

# ---------- 输出 ----------
def q(s): return '"' + s.replace('"', '\\"') + '"'
out = ['# 主题词表。由 uv run kb-core build-topics 从 data/inputs/topics/ 生成；人工修改后不要重跑覆盖，改输入再生成。',
       '# 设计见 docs/design/model/topics.md、docs/design/model/hierarchy.md。', 'version:', f'  id: "{VERSION}"', f'  date: {TODAY}',
       f'  note: 初版：{len(concepts)} 个概念，{len(arrays)} 个数组', '', 'arrays:']
for a in arrays:
    out.append(f"  - {{ id: {a['id']}, superordinate: {a['superordinate']}, source: {a['source']} }}")
out += ['', 'concepts:']
for c in concepts.values():
    out.append(f"  - id: {c['id']}")
    labs = ', '.join(f"{l}: {q(c['label'][l])}" for l in ('zh','en') if c['label'][l])
    assert labs, c['id']
    out.append(f"    label: {{ {labs} }}")
    basis_yaml = yaml.safe_dump(c['basis'], allow_unicode=True, sort_keys=False, width=10000).rstrip()
    out.append('    basis:')
    out.extend('      ' + line for line in basis_yaml.splitlines())
    out.append(f"    broader: [{', '.join(c['broader'])}]")
    if c['arrays']: out.append(f"    arrays: [{', '.join(c['arrays'])}]")
    if c.get('scope'): out.append(f"    scope: {q(c['scope'])}")
    out.append(f"    source: {c['source']}")
    if c['match']:
        out.append('    match:')
        for m in c['match']:
            out.append(f"      - {{ source: {m['source']}, id: {q(m['id'])}, rel: {m['rel']} }}")
    out.append(f"    status: {c['status']}")
    out.append(f"    added: {c['added']}")
(ROOT/'data/vocab'/'topics.yaml').write_text('\n'.join(out)+'\n', encoding='utf-8')
print(len(concepts), '个概念，', len(arrays), '个数组')
