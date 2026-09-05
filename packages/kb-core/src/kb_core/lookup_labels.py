#!/usr/bin/env python3
"""为 topics.yaml 里 basis 为 self 的标签查 Wikidata（译名阶梯第 3 级）。
只接受：对方语言标签与本库名称完全一致，且描述像学科/概念；中文优先 zh-hans/zh-cn，繁体经 OpenCC 转简并注明。
结果写 data/inputs/topics/label-lookup.json 作为清单交人审，不改词表。用 `uvx --from opencc-python-reimplemented --with pyyaml python scripts/lookup-labels.py` 运行。"""
from kb_core.repository import project_root
import json, urllib.request, urllib.parse, time, pathlib, re, yaml, sys
try:
    import opencc; T2S = opencc.OpenCC('t2s').convert
except ImportError:
    T2S = None
ROOT = project_root()
H = {'User-Agent': 'kb-design/0.1 (gxagenta@gmail.com)'}
OUT = ROOT / 'data/audit/labels/label-lookup.json'
res = json.load(open(OUT)) if OUT.exists() else {}
def get(u):
    for i in range(6):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=30))
        except Exception as e:
            time.sleep(4 * (i + 1))
    return None
FIELDY = re.compile(r'branch|field|study|theory|science|discipline|mathematic|linguistic|subfield|area of|概念|学科|领域|理论|研究|分支', re.I)
BAD = re.compile(r'article|paper|journal|book|film|album|song|person|human|company|village|city|river|station|surname|given name|family name|episode|painting|species|genus|protein|gene', re.I)
T = yaml.safe_load(open(ROOT / 'data/vocab' / 'topics.yaml'))
todo = []
for c in T['concepts']:
    b = c.get('basis', {})
    def legacy_self(value):
        return value == 'self' or isinstance(value, dict) and value.get('legacy') == 'self'
    if legacy_self(b.get('zh')) and c['label'].get('en'): todo.append((c['id'], 'zh', c['label']['en'], 'en'))
    if legacy_self(b.get('en')) and c['label'].get('zh'): todo.append((c['id'], 'en', c['label']['zh'], 'zh'))
print(len(todo), '个待查', file=sys.stderr)
for n, (cid, want, name, have) in enumerate(todo):
    key = f'{cid}.{want}'
    if key in res: continue
    q = urllib.parse.quote(name)
    d = get(f'https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language={have}&uselang={have}&limit=5&search={q}')
    hit = None
    for x in (d or {}).get('search', []):
        desc = x.get('description', '')
        if BAD.search(desc) and not FIELDY.search(desc): continue
        e = get(f'https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=labels|descriptions&languages=en|zh|zh-hans|zh-cn&ids={x["id"]}')
        if not e: continue
        ent = e['entities'][x['id']]
        labels = {k: v['value'] for k, v in ent.get('labels', {}).items()}
        have_label = labels.get(have) or labels.get('zh-hans') or labels.get('zh-cn')
        if not have_label or have_label.strip().lower() != name.strip().lower(): continue
        descs = ent.get('descriptions', {})
        dtext = ' '.join(v['value'] for v in descs.values())
        if not FIELDY.search(dtext): continue          # 描述必须像学科或概念
        if BAD.search(dtext): continue
        note = ''
        if want == 'zh':
            want_label = labels.get('zh-hans') or labels.get('zh-cn')
            if not want_label and labels.get('zh'):
                want_label = labels['zh']
                if T2S and T2S(want_label) != want_label:
                    want_label = T2S(want_label); note = 'zh 标签为繁体，OpenCC 转简'
        else:
            want_label = labels.get('en')
        if not want_label: continue
        hit = {'q': x['id'], 'label': want_label, 'desc': dtext[:80], 'note': note}
        break
    res[key] = hit
    if n % 20 == 0:
        json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=1)
        print(n, key, hit, file=sys.stderr)
    time.sleep(1.2)
json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=1)
found = sum(1 for v in res.values() if v)
print(f'{found}/{len(res)} 查到', file=sys.stderr)
