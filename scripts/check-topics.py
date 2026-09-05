#!/usr/bin/env python3
"""校验 vocab/ 五份词表。规则见 design/topics.md「校验规则」、design/content-model.md。"""
import yaml, pathlib, sys, re, collections
from label_basis import validate_basis
from label_adoptions import load_adoptions
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'vocab'
T = yaml.safe_load(open(ROOT/'topics.yaml'))
E = yaml.safe_load(open(ROOT/'entities.yaml'))
S = yaml.safe_load(open(ROOT/'sources.yaml'))
Y = yaml.safe_load(open(ROOT/'types.yaml'))
G = yaml.safe_load(open(ROOT/'genres.yaml'))
F = yaml.safe_load(open(ROOT/'forms.yaml'))
bad = []
ID = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')

concepts = {c['id']: c for c in T['concepts']}
arrays = {a['id']: a for a in T['arrays']}
sources = {s['id']: s for s in S['sources']}
entities = {e['id']: e for e in E['entities']}

# ids
for name, coll in [('topics', concepts), ('entities', entities), ('sources', sources), ('types', {t['id']: t for t in Y['types']}), ('genres', {g['id']: g for g in G['genres']}), ('forms', {f['id']: f for f in F['forms']})]:
    for i in coll:
        if not ID.match(i): bad.append(f'{name}: id 不合规 {i}')

# sources -> entities
for s in sources.values():
    if s['entity'] not in entities: bad.append(f"sources: entity 不存在 {s['entity']}")
    if 'structure' in s['role'] and 'mapping' not in s['role']: bad.append(f"sources: {s['id']} structure 需含 mapping")

for coll in (Y['types'], G['genres'], F['forms']):
    for x in coll:
        for m in x.get('match', []):
            if m['source'] not in sources: bad.append(f"types/genres: {x['id']} match.source 未登记 {m['source']}")

# topics
for c in concepts.values():
    for b in c['broader']:
        if b not in concepts: bad.append(f"topics: {c['id']} broader 不存在 {b}")
    if c['source'] != 'self':
        if c['source'] not in sources: bad.append(f"topics: {c['id']} source 未登记 {c['source']}")
        if not any(m['source'] == c['source'] for m in c.get('match', [])):
            bad.append(f"topics: {c['id']} 借入但无 match 回 {c['source']}")
    for m in c.get('match', []):
        if m['source'] not in sources: bad.append(f"topics: {c['id']} match.source 未登记 {m['source']}")
        if m['rel'] not in ('exactMatch','closeMatch','broadMatch','narrowMatch','relatedMatch'): bad.append(f"topics: {c['id']} rel 非法")
    for a in c.get('arrays', []):
        if a not in arrays: bad.append(f"topics: {c['id']} arrays 不存在 {a}")
        elif arrays[a]['superordinate'] not in c['broader']: bad.append(f"topics: {c['id']} 数组 {a} 的上位不在 broader 里")
    for r in c.get('related') or []:
        if r not in concepts: bad.append(f"topics: {c['id']} related 不存在 {r}")
        elif c['id'] not in (concepts[r].get('related') or []): bad.append(f"topics: {c['id']} related {r} 未互反")
        elif set(c['broader']) & set(concepts[r]['broader']): bad.append(f"topics: {c['id']} related {r} 同上位，不应加 RT")
    if c['status'] == 'deprecated' and not c.get('replaced_by'): bad.append(f"topics: {c['id']} deprecated 无 replaced_by")
    if c['status'] not in ('unassigned','candidate','active','deprecated'): bad.append(f"topics: {c['id']} status 非法")
for a in arrays.values():
    if a['superordinate'] not in concepts: bad.append(f"arrays: {a['id']} 上位不存在")
    if not (a.get('source') or a.get('characteristic')): bad.append(f"arrays: {a['id']} 无 source 也无 characteristic")
    if a.get('source') and a['source'] not in sources: bad.append(f"arrays: {a['id']} source 未登记")

# cycles
def has_cycle():
    state = {}
    def visit(n, stack):
        if n in stack: return True
        if state.get(n): return False
        stack.add(n)
        for b in concepts[n]['broader']:
            if visit(b, stack): return True
        stack.discard(n); state[n] = True; return False
    return any(visit(n, set()) for n in concepts)
if has_cycle(): bad.append('topics: broader 有环')

# label duplicates
en = collections.Counter(c['label']['en'].lower() for c in concepts.values() if c['label'].get('en'))
dups = [k for k, v in en.items() if v > 1]

# entities
for e in entities.values():
    for s in e.get('subjects', []):
        if s not in concepts: bad.append(f"entities: {e['id']} subjects 不存在 {s}")
    if e['kind'] in ('standard','publication','person','large-language-model') and not e.get('tier'): bad.append(f"entities: {e['id']} 缺 tier")
    if e['kind'] not in ('software','programming-language','organization','standard','publication','person','large-language-model'): bad.append(f"entities: {e['id']} kind 非法")
    for cr in (e.get('creator') or []):
        if cr not in entities: bad.append(f"entities: {e['id']} creator 不存在 {cr}")
    if e.get('vendor') and e['vendor'] not in entities: bad.append(f"entities: {e['id']} vendor 不存在 {e['vendor']}")
    for m in e.get('match', []):
        if m['source'] not in sources: bad.append(f"entities: {e['id']} match.source 未登记")

# basis
selfcount = collections.Counter(); judged = collections.Counter()
adoptions = load_adoptions(ROOT.parent)
for name, coll in [('entities', entities), ('topics', concepts)]:
    for x in coll.values():
        b = x.get('basis') or {}
        if name == 'entities' and x.get('subjects') and 'subjects' not in b: bad.append(f"entities: {x['id']} subjects 无 basis")
        for field, val in b.items():
            if field in ('zh','en') and name=='topics':
                judged[(name,'label.'+field)] += 1
                if val == 'self' or isinstance(val, dict) and val.get('legacy') == 'self':
                    selfcount[(name,'label.'+field)] += 1
                    if x.get('status') == 'active': bad.append(f"topics: {x['id']} label.{field} 为自译却 active")
                bad.extend(f"topics: {x['id']} basis.{field}: {message}" for message in
                           validate_basis(val, x['label'].get(field), x, field, sources, adoptions))
                continue
            vals = val if isinstance(val, list) else [val]
            judged[(name, field)] += 1
            for v in vals:
                if v == 'self': selfcount[(name, field)] += 1
                else:
                    src = v.split(':')[0]
                    if src not in sources: bad.append(f"{name}: {x['id']} basis 来源未登记 {src}")
            if 'self' in vals and x.get('status') == 'active': bad.append(f"{name}: {x['id']} {field} basis 为 self 却 active")

for name, document in [('forms', F), ('types', Y), ('genres', G)]:
    for record in document[name]:
        for language, value in record.get('basis', {}).items():
            if language in ('zh', 'en'):
                bad.extend(f"{name}: {record['id']} basis.{language}: {message}" for message in
                           validate_basis(value, record['label'].get(language), record, language,
                                          sources, adoptions, collection=name))

# ---------- 指标表（design/maintenance.md）----------
import datetime
today = datetime.date.today()
sig = {}
by_top = collections.Counter()
def top_of(cid):
    c = concepts[cid]
    return cid if not c['broader'] else top_of(c['broader'][0])
for c in concepts.values():
    by_top[(top_of(c['id']), c['status'])] += 1
tops = sorted({k[0] for k in by_top})
for t in tops:
    tot = sum(by_top[(t, st)] for st in ('active','unassigned','candidate','deprecated'))
    sig[f'unassigned.{t}'] = f'{by_top[(t,"unassigned")]}/{tot}'
for k in judged: sig[f'self.{k[0]}.{k[1]}'] = f'{selfcount[k]}/{judged[k]}'
cand = [x for coll in (concepts, entities) for x in coll.values() if x['status'] == 'candidate']
sig['candidates'] = len(cand)
# 每个上位下的候选数、self 数：两个独立阈值（阈值表）
cand_per_parent = collections.Counter(); self_per_parent = collections.Counter()
for c in concepts.values():
    if c['status'] == 'candidate':
        for b in c['broader']: cand_per_parent[b] += 1
for e in entities.values():
    if (e.get('basis') or {}).get('subjects') == 'self':
        for sj in e.get('subjects', []): self_per_parent[sj] += 1
others = [c['id'] for c in concepts.values() if c['label'].get('zh','').endswith('其他学科')]
other_kids = collections.Counter()
for c in concepts.values():
    for b in c['broader']:
        if b in others: other_kids[b] += 1
TIER_MONTHS = {'de-jure': 24, 'de-facto': 12, 'vendor': 6}   # 与 maintenance.md 阈值表一致
due = []
for e in entities.values():
    if e.get('checked') and e.get('tier') in TIER_MONTHS:
        d = e['checked'] if isinstance(e['checked'], datetime.date) else datetime.date.fromisoformat(str(e['checked']))
        months = (today.year - d.year) * 12 + today.month - d.month
        if months >= TIER_MONTHS[e['tier']]: due.append(e['id'])

lp = ROOT / 'signals.yaml'
hist = (yaml.safe_load(open(lp)) or {}) if lp.exists() else {}
snaps = hist.get('snapshots', [])
last = snaps[-1] if snaps else {}
def line(name, cur, thr, trig):
    print(f"  {name:<48} 当前 {cur!s:<10} 上次 {last.get(name, '—')!s:<10} 阈值 {thr:<16} {'触发' if trig else ''}")

for b in bad: print(b)
print(f"{len(bad)} 处问题；{len(concepts)} 概念，{len(arrays)} 数组，{len(entities)} 实体，{len(sources)} 来源")
print('指标表：')
for t in tops: line(f'未标引 {t}', sig[f'unassigned.{t}'], '两次审核无变化', len(snaps) >= 2 and all(sn.get(f'unassigned.{t}') == sig[f'unassigned.{t}'] for sn in snaps[-2:]))
for k in judged: line(f'self 断言 {k[0]}.{k[1]}', sig[f'self.{k[0]}.{k[1]}'], '—', False)
line('候选总数', len(cand), '≥ 20 审核', len(cand) >= 20)
for k, v in cand_per_parent.items():
    if v >= 5: line(f'节点下候选 {k}', v, '≥ 5 拆分', True)
for k, v in self_per_parent.items():
    if v >= 5: line(f'节点下 self {k}', v, '≥ 5 拆分', True)
for k, v in other_kids.items():
    if v >= 3: line(f'其他类目下位 {k}', v, '≥ 3 拆分', True)
line('来源复核到期', len(due), '按 tier', bool(due))
if due: print('    ' + ', '.join(due))
if hist.get('last_candidate_review'): print(f"  上次候选审核 {hist['last_candidate_review']}；治理年审 {hist.get('governance_reviewed', '—')}")
print('重复的英文标签（不同上位下的同名概念，允许）：', len(dups))

if '--record' in sys.argv:
    snap = dict(sig); snap['recorded'] = str(today)
    snaps.append(snap)
    hist['snapshots'] = snaps
    hist.setdefault('last_candidate_review', None); hist.setdefault('governance_reviewed', None)
    with open(lp, 'w') as stream:
        stream.write('# 词表维护指标的只追加快照，不是正式词表数据。\n')
        stream.write('# 运行 python3 scripts/check-topics.py --record 时追加。\n')
        yaml.safe_dump(hist, stream, allow_unicode=True)
    print('已追加快照到 vocab/signals.yaml')
sys.exit(1 if bad else 0)
