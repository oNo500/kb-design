#!/usr/bin/env python3
"""校验 vocab/ 五份词表。规则见 design/topics.md「校验规则」、design/content-model.md。"""
import yaml, pathlib, sys, re, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'vocab'
T = yaml.safe_load(open(ROOT/'topics.yaml'))
E = yaml.safe_load(open(ROOT/'entities.yaml'))
S = yaml.safe_load(open(ROOT/'sources.yaml'))
Y = yaml.safe_load(open(ROOT/'types.yaml'))
bad = []
ID = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')

concepts = {c['id']: c for c in T['concepts']}
arrays = {a['id']: a for a in T['arrays']}
sources = {s['id']: s for s in S['sources']}
entities = {e['id']: e for e in E['entities']}

# ids
for name, coll in [('topics', concepts), ('entities', entities), ('sources', sources), ('types', {t['id']: t for t in Y['types']})]:
    for i in coll:
        if not ID.match(i): bad.append(f'{name}: id 不合规 {i}')

# sources -> entities
for s in sources.values():
    if s['entity'] not in entities: bad.append(f"sources: entity 不存在 {s['entity']}")
    if 'structure' in s['role'] and 'mapping' not in s['role']: bad.append(f"sources: {s['id']} structure 需含 mapping")

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
en = collections.Counter(c['label']['en'].lower() for c in concepts.values())
dups = [k for k, v in en.items() if v > 1]

# entities
for e in entities.values():
    for s in e.get('subjects', []):
        if s not in concepts: bad.append(f"entities: {e['id']} subjects 不存在 {s}")
    if e['kind'] in ('standard','publication') and not e.get('tier'): bad.append(f"entities: {e['id']} 缺 tier")
    if e['kind'] not in ('software','programming-language','organization','standard','publication'): bad.append(f"entities: {e['id']} kind 非法")
    if e.get('vendor') and e['vendor'] not in entities: bad.append(f"entities: {e['id']} vendor 不存在 {e['vendor']}")
    for m in e.get('match', []):
        if m['source'] not in sources: bad.append(f"entities: {e['id']} match.source 未登记")

# basis
selfcount = collections.Counter(); judged = collections.Counter()
for name, coll in [('entities', entities), ('topics', concepts)]:
    for x in coll.values():
        b = x.get('basis') or {}
        if name == 'entities' and x.get('subjects') and 'subjects' not in b: bad.append(f"entities: {x['id']} subjects 无 basis")
        for field, val in b.items():
            vals = val if isinstance(val, list) else [val]
            judged[(name, field)] += 1
            for v in vals:
                if v == 'self': selfcount[(name, field)] += 1
                else:
                    src = v.split(':')[0]
                    if src not in sources: bad.append(f"{name}: {x['id']} basis 来源未登记 {src}")
            if 'self' in vals and x.get('status') == 'active': bad.append(f"{name}: {x['id']} {field} basis 为 self 却 active")

# stats
by_top = collections.Counter()
def top_of(cid):
    c = concepts[cid]
    return cid if not c['broader'] else top_of(c['broader'][0])
for c in concepts.values():
    by_top[(top_of(c['id']), c['status'])] += 1

for b in bad: print(b)
print(f"{len(bad)} 处问题；{len(concepts)} 概念，{len(arrays)} 数组，{len(entities)} 实体，{len(sources)} 来源")
for k in sorted(judged): print(f'判断债 {k[0]}.{k[1]}: self {selfcount[k]} / {judged[k]}')
print('重复的英文标签（不同上位下的同名概念，允许）：', len(dups))
tops = sorted({k[0] for k in by_top})
for t in tops:
    print(f"  {t}: " + ', '.join(f"{st} {by_top[(t,st)]}" for st in ('active','unassigned','candidate','deprecated') if by_top[(t,st)]))
sys.exit(1 if bad else 0)
