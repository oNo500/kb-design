"""Safe Obsidian projection; source text is never treated as Markdown code."""
from __future__ import annotations

import html
import json
import re
from urllib.parse import quote, urlsplit

import yaml
from rdflib import BNode, Literal, RDF, URIRef
from rdflib.namespace import DCTERMS, OWL, RDFS, SKOS, XSD, Namespace

from .common import ContractError

XL = Namespace('http://www.w3.org/2008/05/skos-xl#')
LABEL_ROLES = ((SKOS.prefLabel, XL.prefLabel, '首选名'), (SKOS.altLabel, XL.altLabel, '替代名'), (SKOS.hiddenLabel, XL.hiddenLabel, '隐藏名'))
NOTE_NAMES = {SKOS.definition: '定义', SKOS.scopeNote: '范围说明', DCTERMS.description: '一般描述', SKOS.note: '说明', SKOS.example: '示例', SKOS.editorialNote: '编辑说明', SKOS.historyNote: '历史说明', SKOS.changeNote: '变更说明'}
RELATION_NAMES = {SKOS.broader: '上位概念', SKOS.narrower: '下位概念', SKOS.related: '相关概念', SKOS.inScheme: '所属体系', SKOS.hasTopConcept: '顶层概念', SKOS.topConceptOf: '顶层归属', SKOS.member: '集合成员', SKOS.exactMatch: '精确映射', SKOS.closeMatch: '接近映射', SKOS.broadMatch: '上位映射', SKOS.narrowMatch: '下位映射', SKOS.relatedMatch: '相关映射'}
KIND_NAMES = {'concepts': '概念', 'entities': '实体', 'schemes': '概念体系', 'collections': '集合', 'types': '文档类型', 'genres': '体裁', 'forms': '载体', 'references': '参考文献'}
FIELD_ROLES = {'concepts': ('subject',), 'entities': ('entities', 'source'),
               'types': ('type',), 'genres': ('genre',), 'forms': ('form',),
               'references': ('references', 'source')}
PROVENANCE_NAMES = {DCTERMS.creator: '创建者（creator）', DCTERMS.contributor: '贡献者',
                    DCTERMS.source: '来源', DCTERMS.created: '创建时间', DCTERMS.modified: '修改时间',
                    URIRef('http://www.w3.org/ns/prov#wasDerivedFrom'): '派生来源',
                    URIRef('http://www.w3.org/ns/prov#wasAttributedTo'): '归属者',
                    URIRef('http://www.w3.org/ns/prov#wasGeneratedBy'): '生成活动'}
FACT_NAMES = {RDF.type: '来源类型'}
for _namespace in ('https://schema.org/', 'http://schema.org/'):
    FACT_NAMES.update({URIRef(_namespace + key): title for key, title in {
        'url': '网址', 'sameAs': '外部身份', 'author': '作者', 'creator': '创建者',
        'developer': '开发者', 'publisher': '发布者', 'manufacturer': '制造者',
        'founder': '创办者', 'parentOrganization': '上级组织', 'memberOf': '所属组织',
        'programmingLanguage': '编程语言', 'operatingSystem': '操作系统',
        'softwareVersion': '软件版本', 'license': '许可', 'description': '描述',
    }.items()})
SOURCE_NAMES = {DCTERMS.source: '来源', RDFS.seeAlso: '另见', DCTERMS.license: '许可',
                DCTERMS.rights: '权利说明', URIRef('http://www.w3.org/ns/prov#wasDerivedFrom'): '派生来源'}


def md(value):
    value = html.escape(str(value), quote=True)
    return ''.join(f'&#{ord(c)};' if c in '\\`*_{}[]()#+.!|~^%=' else c for c in value).replace('\r', '⏎').replace('\n', '⏎')


def alias_safe(value):
    return bool(value) and not any(char in value for char in ('\n', '\r', '#', '|', '^', '%%', '[[', ']]')) and not any(ord(char) < 32 for char in value)


def literal_key(value):
    return (str(value), (value.language or '').lower(), str(value.datatype or ''))


def names_for(graph, subject):
    names = []
    role_values = {}
    for plain, xl, role in LABEL_ROLES:
        values = []
        for value in graph.objects(subject, plain):
            if not isinstance(value, Literal) or value.datatype not in (None, XSD.string, RDF.langString):
                raise ContractError(f'普通名称不是文字字面值：{subject} {plain}')
            values.append((value, None, plain))
        for label in graph.objects(subject, xl):
            if not isinstance(label, URIRef):
                raise ContractError(f'XL 名称缺少 IRI：{subject}')
            literals = list(graph.objects(label, XL.literalForm))
            if len(literals) != 1 or not isinstance(literals[0], Literal) or literals[0].datatype not in (None, XSD.string, RDF.langString):
                raise ContractError(f'XL 名称须有一个 literalForm：{label}')
            values.append((literals[0], label, xl))
        role_values[role] = {literal_key(value) for value, _, _ in values}
        names.extend({'role': role, 'value': value, 'label': label, 'predicate': predicate} for value, label, predicate in values)
    for left, right in (('首选名', '替代名'), ('首选名', '隐藏名'), ('替代名', '隐藏名')):
        if role_values[left] & role_values[right]:
            raise ContractError(f'名称角色冲突：{subject}：{left} 与 {right}')
    preferred = {}
    for value, language, datatype in role_values['首选名']:
        preferred.setdefault(language, set()).add((value, datatype))
    if any(len(values) > 1 for values in preferred.values()):
        raise ContractError(f'同一语言有冲突首选名：{subject}')
    # 普通实体及集合也允许来源直接使用 rdfs:label/schema:name；它们不是 SKOS 首选角色。
    for predicate in (RDFS.label, URIRef('https://schema.org/name'), URIRef('http://schema.org/name')):
        for value in graph.objects(subject, predicate):
            if isinstance(value, Literal):
                names.append({'role': '来源名称', 'value': value, 'label': None, 'predicate': predicate})
    return sorted(names, key=lambda n: (n['role'], literal_key(n['value']), str(n['label'] or ''), str(n['predicate'])))


def display_name(names, languages, fallback):
    preferred = [n['value'] for n in names if n['role'] == '首选名']
    if not preferred:
        preferred = [n['value'] for n in names if n['role'] == '来源名称']
    for language in languages:
        parts = language.lower().split('-')
        while parts:
            request = '-'.join(parts)
            matches = [v for v in preferred if (v.language or '').lower() == request]
            if matches:
                return str(sorted(matches, key=literal_key)[0]), False
            parts.pop()
            if parts and len(parts[-1]) == 1:
                parts.pop()
    untagged = [v for v in preferred if not v.language]
    # 不带语言的来源名称有自己的原文身份；只在显式请求 und 时选用。
    if 'und' in languages and untagged:
        return str(sorted(untagged, key=literal_key)[0]), False
    return fallback, True


def linked(identity, by_iri, label=None):
    record = by_iri.get(str(identity))
    if not record:
        return md(identity)
    text = label or record['label']
    path = record['path'][:-3]
    return f'[[{path}|{text}]]' if alias_safe(text) and not any(c in text for c in '<>*_`[]{}()!\\') else f'[[{path}]]（{md(text)}）'


def term_text(graph, value, by_iri, *, show_note=True):
    if isinstance(value, Literal):
        suffix = f' @{md(value.language)}' if value.language else (f'（datatype：{md(value.datatype)}）' if value.datatype else '')
        return md(value) + suffix
    if isinstance(value, URIRef):
        result = linked(value, by_iri)
        body = list(graph.objects(value, RDF.value)) if show_note else []
        if body:
            result += '；正文：' + '；'.join(sorted(term_text(graph, v, by_iri, show_note=False) if not isinstance(v, BNode) else '嵌套结构，原件回查' for v in body))
            result += '；附着对象及来源见原件'
        return result
    bodies = list(graph.objects(value, RDF.value)) if show_note else []
    if bodies:
        literal_bodies = [v for v in bodies if not isinstance(v, BNode)]
        texts = sorted(term_text(graph, v, by_iri, show_note=False) for v in literal_bodies)
        if len(literal_bodies) != len(bodies):
            texts.append('嵌套结构，原件回查')
        return '本输入的独立说明：' + '；'.join(texts) + '；完整结构和来源见原件'
    return '空白节点结构，原件回查'


def source_text(graph, value, by_iri):
    if isinstance(value, URIRef) and str(value) not in by_iri and urlsplit(str(value)).scheme in ('http', 'https'):
        # Explicit source URLs stay usable; encode Markdown delimiters, not the source identity.
        target = quote(str(value), safe=":/?#@!$&'*+,;=%~.-_")
        return f'[{md(value)}](<{target}>)'
    return term_text(graph, value, by_iri)


def ordered_members(graph, subject):
    heads = list(graph.objects(subject, SKOS.memberList))
    if not heads:
        return None
    if len(heads) != 1:
        raise ContractError(f'有序集合有多个 memberList：{subject}')
    node, seen, result = heads[0], set(), []
    while node != RDF.nil:
        if node in seen:
            raise ContractError(f'RDF 列表存在循环：{subject}')
        seen.add(node)
        first, rest = list(graph.objects(node, RDF.first)), list(graph.objects(node, RDF.rest))
        if len(first) != 1 or len(rest) != 1 or not isinstance(rest[0], (BNode, URIRef)):
            raise ContractError(f'RDF 列表节点缺失或数量冲突：{subject}')
        result.append(first[0])
        node = rest[0]
    return result


def frontmatter(value):
    return '---\n' + yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=1000).rstrip() + '\n---\n'


def render_resource(record, graph, names, by_iri, source_info, *, projection=None):
    subject = URIRef(record['identity']['iri'])
    entry = record['entry']
    metadata = {'title': record['label'], 'identifier': str(subject), 'aliases': entry['aliases'],
                'record_kind': record['kind'], 'fields': entry['fields'], 'preview': record.get('mode', 'preview') == 'preview',
                'trial_selectable': record['trial_selectable'], 'selectable': record['trial_selectable']}
    result = [frontmatter(metadata), f'# {md(record["label"])}', '']
    if entry['fields']:
        result.extend(['适用字段：' + '、'.join(f'`{field}`' for field in entry['fields']) + '。', ''])
    if record.get('label_fallback'):
        result.extend(['显示请求未匹配首选名称，当前以原身份显示。', ''])
    if record['restrictions']:
        result.extend(['## 使用限制', '', *[f'- {md(v)}' for v in record['restrictions']], ''])
    if not record['formal_basis']:
        result.extend(['开发试用；正式准用未确认。' if record.get('mode', 'preview') == 'preview' else '未获本实例选用授权。', ''])
    elif record.get('mode') == 'formal' and record['kind'] == 'entities':
        result.extend(['本实例可按已固定范围引用；来源原状态保留，实体事实与语义审阅尚未执行。', ''])

    def mark(attachment, predicate, value):
        if projection is not None and not isinstance(value, BNode):
            projection[(attachment, predicate, value)] = record['path']

    visible_names = [n for n in names if n['role'] != '隐藏名']
    if visible_names:
        result.extend(['## 名称', ''])
        seen = set()
        for name in visible_names:
            key = (name['role'], literal_key(name['value']))
            if key not in seen:
                result.append(f'- {name["role"]}：{term_text(graph, name["value"], by_iri)}')
                seen.add(key)
            if name['label'] is None:
                mark(subject, name['predicate'], name['value'])
            else:
                mark(name['label'], XL.literalForm, name['value'])
        result.append('')

    for predicate, heading in NOTE_NAMES.items():
        values = list(graph.objects(subject, predicate))
        if values:
            result.extend([f'## {heading}', ''])
            for value in sorted(values, key=lambda v: term_text(graph, v, by_iri)):
                result.append('- ' + term_text(graph, value, by_iri))
                mark(subject, predicate, value)
            result.append('')

    # The attachment is always the Label, even when this is the concept page.
    label_ids = sorted({n['label'] for n in visible_names if n['label'] is not None}, key=str)
    label_notes = [(label, predicate, value) for label in label_ids
                   for predicate, value in graph.predicate_objects(label)
                   if predicate in NOTE_NAMES or predicate in PROVENANCE_NAMES]
    if label_notes:
        result.extend(['## 名称说明', ''])
        for label, predicate, value in sorted(label_notes, key=lambda x: (str(x[0]), str(x[1]), term_text(graph, x[2], by_iri))):
            label_text = next(n['value'] for n in visible_names if n['label'] == label)
            heading = NOTE_NAMES.get(predicate, PROVENANCE_NAMES.get(predicate))
            result.append(f'- 名称 {term_text(graph, label_text, by_iri)} 的{heading}：{term_text(graph, value, by_iri)}')
            mark(label, predicate, value)
        result.append('')

    if record['kind'] == 'entities':
        state = record.get('source_state')
        originals = state.get('entity_delivery', []) if isinstance(state, dict) else []
        if originals:
            result.extend(['## 来源状态', ''])
            for original in originals:
                for source in original['sources']:
                    result.append(f'- {md(source["key"])}：{md(json.dumps(source["state"], ensure_ascii=False, sort_keys=True))}。')
                if original.get('ineligible_reasons'):
                    result.append('- 不可选原因：' + '、'.join(md(reason) for reason in original['ineligible_reasons']) + '。')
            result.append('')
        facts = [(p, v) for p, v in graph.predicate_objects(subject) if p in FACT_NAMES]
        if facts:
            result.extend(['## 来源事实', ''])
            for predicate, value in sorted(facts, key=lambda pv: (str(pv[0]), term_text(graph, pv[1], by_iri))):
                result.append(f'- {FACT_NAMES[predicate]}：{term_text(graph, value, by_iri)}')
                mark(subject, predicate, value)
            result.append('')

    for key, heading in (('broader', '上位概念'), ('narrower', '下位概念'), ('related', '相关概念')):
        values = entry['relations'][key]
        if values:
            result.extend([f'## {heading}', ''])
            for relation in values[:12]:
                target = URIRef(relation['identity']['iri'])
                result.append('- ' + linked(target, by_iri))
                direct = (subject, SKOS[key], target)
                inverse = (target, SKOS[{'broader': 'narrower', 'narrower': 'broader', 'related': 'related'}[key]], subject)
                if projection is not None:
                    for triple in (direct, inverse):
                        if triple in graph:
                            projection[triple] = record['path']
            if len(values) > 12:
                result.append(f'- 另有 {len(values) - 12} 条；用详情查询或完整原件读取。')
            result.append('')

    for predicate, heading in RELATION_NAMES.items():
        if predicate in (SKOS.broader, SKOS.narrower, SKOS.related):
            continue
        values = sorted(graph.objects(subject, predicate), key=lambda v: term_text(graph, v, by_iri))
        if values:
            result.extend([f'## {heading}', ''])
            for value in values[:12]:
                result.append('- ' + term_text(graph, value, by_iri))
                mark(subject, predicate, value)
            if len(values) > 12:
                result.append(f'- 另有 {len(values) - 12} 条保留于完整原件。')
            result.append('')
    members = ordered_members(graph, subject)
    if members is not None:
        result.extend(['## 成员顺序', ''])
        result.extend(f'{position}. {term_text(graph, member, by_iri)}' for position, member in enumerate(members, 1))
        if not members:
            result.append('原列表为空。')
        result.append('')

    result.extend(['## 来源', ''])
    for predicate, value in sorted(graph.predicate_objects(subject), key=lambda pv: (str(pv[0]), term_text(graph, pv[1], by_iri))):
        if predicate in SOURCE_NAMES:
            result.append(f'- {SOURCE_NAMES[predicate]}：{source_text(graph, value, by_iri)}')
            mark(subject, predicate, value)
    for source in source_info:
        version = json.dumps(source.spec['version'], ensure_ascii=False, sort_keys=True) if isinstance(source.spec['version'], dict) else source.spec['version']
        result.append(f'- {md(source.spec["key"])}，版本：{md(version)}。')
    result.extend(['', '完整原件保留在本知识库对应的库外维护记录中，可按来源名称、版本和条目身份回查。', ''])
    return '\n'.join(result).encode('utf8')


def render_auxiliary(record, data, raw_path):
    entry = record['entry']
    metadata = {'title': record['label'], 'identifier': record['identity']['id'],
                'catalog': record['identity']['catalog'], 'aliases': entry['aliases'],
                'record_kind': record['kind'], 'fields': entry['fields'],
                'preview': record.get('mode', 'preview') == 'preview',
                'trial_selectable': record['trial_selectable'], 'selectable': record['trial_selectable']}
    lines = [frontmatter(metadata), f'# {md(record["label"])}', '',
             '适用字段：' + '、'.join(f'`{field}`' for field in entry['fields']) + '。', '']
    if record['restrictions']:
        lines.extend(['## 使用限制', '', *[f'- {md(v)}' for v in record['restrictions']], ''])
    for key, heading in (('definitions', '定义'), ('scope_notes', '范围说明'), ('descriptions', '一般描述')):
        values = entry[key]
        if values:
            lines.extend([f'## {heading}', ''])
            lines.extend('- ' + md(v['text']) + (f' @{md(v["language"])}' if v['language'] else '') for v in values)
            lines.append('')
    if entry['notes']:
        lines.extend(['## 名称与说明', '', *['- ' + md(n['text']) for n in entry['notes']], ''])
    lines.extend(['## 来源', '', f'来源：{md(record["sources"][0])}；版本：{md(record["versions"][0]["version"])}。完整原件由库外维护记录保存，可按来源和原 ID 回查。', ''])
    return '\n'.join(lines).encode('utf8')
