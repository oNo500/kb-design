"""Build a complete, deterministic reference delivery without writing a vault."""
from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from importlib import metadata, resources
import json
from pathlib import Path
import platform

from pyshacl import validate
from rdflib import BNode, Graph, Literal, RDF, URIRef
from rdflib.namespace import DCTERMS, OWL, SH, SKOS
import yaml

from kb_vocab_shacl import read_shapes
from .common import ContractError, Delivery, digest, json_bytes, reference_path, safe_relative
from .layout import KIND_DIRECTORIES, MANIFEST_VERSION, VOCABULARY
from .input import read_inputs, require
from .naming import assign_paths
from .render import (KIND_NAMES, LABEL_ROLES, NOTE_NAMES, RELATION_NAMES, XL,
                     alias_safe, display_name, frontmatter, linked, md,
                     names_for, ordered_members, render_auxiliary, render_resource,
                     FACT_NAMES, PROVENANCE_NAMES, FIELD_ROLES)


def rdf_value(value):
    if isinstance(value, URIRef):
        return {'iri': str(value)}
    if isinstance(value, Literal):
        return {'literal': str(value), 'language': value.language, 'datatype': str(value.datatype) if value.datatype else None}
    return {'blank_node_structure': True}


def classify(graph, subject, entity_classes=()):
    classes = set(graph.objects(subject, RDF.type))
    roles = set()
    if SKOS.Concept in classes:
        roles.add('concepts')
    if SKOS.ConceptScheme in classes:
        roles.add('schemes')
    if classes & {SKOS.Collection, SKOS.OrderedCollection, URIRef('http://purl.org/iso25964/skos-thes#ConceptGroup'), URIRef('http://purl.org/iso25964/skos-thes#ThesaurusArray')}:
        roles.add('collections')
    if len(roles) > 1 or roles and XL.Label in classes:
        raise ContractError(f'同一身份有冲突对象种类：{subject}')
    if roles:
        return roles.pop()
    if classes & set(entity_classes) and XL.Label not in classes:
        return 'entities'
    raise ContractError(f'无法确定对象种类：{subject}')


def navigation_subjects(source):
    selected = set(source.selected)
    graph = source.graph
    # 范围外导航只保留显式关联的体系和集合，不扩张文章可试选范围。
    schemes = {o for s in selected for p in (SKOS.inScheme, SKOS.topConceptOf) for o in graph.objects(s, p)}
    schemes |= {s for target in selected for s in graph.subjects(SKOS.hasTopConcept, target)}
    selected |= {s for s in schemes if isinstance(s, URIRef) and (s, RDF.type, SKOS.ConceptScheme) in graph}
    collections = {s for cls in (SKOS.Collection, SKOS.OrderedCollection, URIRef('http://purl.org/iso25964/skos-thes#ConceptGroup'), URIRef('http://purl.org/iso25964/skos-thes#ThesaurusArray')) for s in graph.subjects(RDF.type, cls)}
    expanded = True
    while expanded:
        expanded = False
        for collection in sorted(collections - selected, key=str):
            members = set(graph.objects(collection, SKOS.member))
            ordered = ordered_members(graph, collection)
            if ordered is not None:
                members.update(ordered)
            if members & selected or any(s in selected for s in graph.objects(collection, SKOS.inScheme)):
                require(isinstance(collection, URIRef), '导航集合缺少源 IRI')
                selected.add(collection)
                expanded = True
    return selected


def new_record(identity, kind, sources, versions, label, mode='preview'):
    return {'identity': identity, 'kind': kind, 'sources': sorted(set(sources)),
            'versions': sorted(versions, key=lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True)),
            'use': 'current', 'mode': mode, 'path': reference_path(kind, identity), 'source_state': None,
            'trial_selectable': False, 'formal_basis': None, 'restrictions': [], 'history': [], 'label': label}


def description_nodes(graph, subject):
    """Collect nodes whose statements are inlined in this resource's page.

    A link to another concept is still only a link. XL records, RDF values and
    list cells contribute descriptions, so their sources need joint consent.
    """
    expanded = {subject}
    pending = [subject]
    structural = {XL.prefLabel, XL.altLabel, XL.hiddenLabel, SKOS.memberList, RDF.rest}
    while pending:
        node = pending.pop()
        for predicate, value in graph.predicate_objects(node):
            if isinstance(value, BNode) or (isinstance(value, URIRef) and
                    (predicate in structural or any(graph.objects(value, RDF.value)))):
                if value not in expanded:
                    expanded.add(value)
                    pending.append(value)
    return expanded


def build_records(spec, sources, auxiliaries):
    graph, ownership = Graph(), defaultdict(list)
    for source in sources:
        graph += source.graph
        for subject in navigation_subjects(source):
            ownership[subject].append(source)
    groups = spec.get('compatible_sources', [])
    require(isinstance(groups, list) and all(isinstance(g, list) and all(isinstance(x, str) for x in g) for g in groups), 'compatible_sources 需要相容来源键列表')
    records, names, by_iri = [], {}, {}
    for subject in sorted(ownership, key=str):
        owners = ownership[subject]
        descriptions = description_nodes(graph, subject)
        actual_owners = [s for s in sources
                         if any(any(s.graph.triples((node, None, None))) for node in descriptions)]
        keys = {s.spec['key'] for s in actual_owners}
        if len(keys) > 1:
            require(any(keys <= set(group) for group in groups), f'对象及附属说明跨源组合未声明相容：{subject}：{sorted(keys)}')
        entity_classes = {URIRef(cls) for source in owners for cls in source.spec['scope'].get('entity_class_iris', [])}
        kind = classify(graph, subject, entity_classes)
        if any(s.spec['scope'].get('concept_scheme_iris') for s in owners) and subject in set().union(*(s.selected for s in owners)):
            require(kind == 'concepts', '概念体系范围选到了非概念')
        if any('entity_class_iris' in s.spec['scope'] and subject in s.selected for s in owners):
            require(kind == 'entities', '实体类别范围不能改写为概念范围')
        entry_names = names_for(graph, subject)
        label, fallback = display_name(entry_names, spec['display']['languages'], str(subject))
        record = new_record({'iri': str(subject)}, kind, list(keys), [{'source_key': s.spec['key'], 'version': s.spec['version']} for s in actual_owners], label, spec.get('mode', 'preview'))
        ownership[subject] = actual_owners
        record['label_fallback'] = fallback
        record['source_types'] = sorted(map(str, graph.objects(subject, RDF.type)))
        selection = 'selectable_subjects' if record['mode'] == 'formal' else 'trial_subjects'
        record['trial_selectable'] = kind in ('concepts', 'entities') and any(str(subject) in s.spec[selection] for s in owners)
        entity_deliveries = [s.entity_delivery for s in owners if getattr(s, 'entity_delivery', None) is not None]
        if kind == 'entities' and entity_deliveries:
            record['trial_selectable'] &= all(str(subject) in d['eligible_entity_iris'] for d in entity_deliveries)
        formal = sorted({s.spec['authority']['formal_reference'] for s in owners if s.spec['authority'].get('formal_reference')})
        record['formal_basis'] = formal or None
        state_values = list(graph.objects(subject, OWL.deprecated))
        if state_values:
            record['source_state'] = [{'predicate': str(OWL.deprecated), 'value': rdf_value(v)} for v in sorted(state_values, key=str)]
            if any(not isinstance(v, Literal) or v.datatype != URIRef('http://www.w3.org/2001/XMLSchema#boolean') for v in state_values):
                raise ContractError(f'无法解释 owl:deprecated 原状态：{subject}')
            if any(v.toPython() is True for v in state_values):
                record['trial_selectable'] = False
                record['restrictions'].append('来源明确 owl:deprecated=true，不供新选用')
        state_owners = [s for s in owners if s.spec.get('source_states', {}).get(str(subject)) is not None]
        source_states = [s.spec['source_states'][str(subject)] for s in state_owners]
        if source_states:
            record['source_state'] = {'rdf': record['source_state'], 'declared': source_states}
            # A verified entity delivery supplies the adopted use policy. Its
            # original candidate/active values remain evidence, not a new gate.
            known_policy = kind == 'entities' and all(
                getattr(s, 'entity_delivery', None) is not None
                and s.spec['source_states'][str(subject)] in [
                    original['state'] for original in s.entity_delivery['entities'][str(subject)]['sources']]
                for s in state_owners)
            if not known_policy:
                record['trial_selectable'] = False
                record['restrictions'].append('来源另有状态声明，本适配器未解释其准用合同，仅供查看')
        entity_states = [deepcopy(d['entities'][str(subject)]) for d in entity_deliveries
                         if str(subject) in d.get('entities', {})]
        if entity_states:
            if not source_states:
                record['source_state'] = {'rdf': record['source_state'], 'declared': []}
            record['source_state']['entity_delivery'] = entity_states
        if not record['trial_selectable'] and not record['restrictions']:
            record['restrictions'].append('此记录不在概念或实体的选用范围' if record['mode'] == 'formal' else '此记录不在概念或实体的预览试选范围')
        record['name_records'] = [{'iri': str(n['label']), 'role': n['role'], 'value': rdf_value(n['value'])} for n in entry_names if n['label'] is not None]
        records.append(record)
        names[str(subject)] = entry_names
        by_iri[str(subject)] = record
    auxiliary_rows = []
    identities = {json.dumps(r['identity'], sort_keys=True) for r in records}
    for item, data, raw_path in auxiliaries:
        for row in data[item['kind']]:
            require(isinstance(row, dict) and isinstance(row.get('id'), str) and bool(row['id']) and '\0' not in row['id'], '辅助记录缺少有效局部 ID')
            identity = {'catalog': item['key'], 'id': row['id']}
            key = json.dumps(identity, sort_keys=True)
            require(key not in identities, f'辅助身份重复：{identity}')
            identities.add(key)
            labels = row.get('label', {})
            require(isinstance(labels, dict) and all(isinstance(v, str) for v in labels.values()), f'辅助名称结构不符：{identity}')
            label = next((labels[lang] for lang in spec['display']['languages'] if lang in labels), row['id'])
            record = new_record(identity, item['kind'], [item['key']], [{'source_key': item['key'], 'version': item['version']}], label, spec.get('mode', 'preview'))
            record['source_state'] = {'status': row.get('status'), 'basis': row.get('basis'), 'match': row.get('match')}
            formal_reference = item['authority'].get('formal_reference')
            # 内容模型的“载体词表”保留现有成员及原状态，form 约束为表内值。
            # 不把未使用的 unassigned 改成 active，也不把它当作未采纳候选。
            registered = row.get('status') == 'active' or (item['kind'] == 'forms' and row.get('status') == 'unassigned')
            record['formal_basis'] = [formal_reference] if registered and formal_reference else None
            record['trial_selectable'] = registered and bool(record['formal_basis'])
            if not record['trial_selectable']:
                record['restrictions'].append(f'辅助记录状态为 {row.get("status", "未声明")}；未确认属于已采纳值域时不供新选用')
            records.append(record)
            auxiliary_rows.append((record, row, raw_path))
    paths = [r['path'] for r in records]
    require(len(paths) == len(set(paths)), '不同身份产生冲突参考路径')
    return graph, records, names, by_iri, ownership, auxiliary_rows


def text_values(graph, subject, predicate):
    """Read literal bodies without moving a Label's note onto its concept."""
    values = []
    for value in graph.objects(subject, predicate):
        bodies = [value] if isinstance(value, Literal) else graph.objects(value, RDF.value)
        for body in bodies:
            if isinstance(body, Literal):
                item = {'text': str(body), 'language': body.language, 'predicate': str(predicate)}
                if body.datatype not in (None, RDF.langString, URIRef('http://www.w3.org/2001/XMLSchema#string')):
                    item['datatype'] = str(body.datatype)
                values.append(item)
    return sorted({json.dumps(v, sort_keys=True, ensure_ascii=False): v for v in values}.values(),
                  key=lambda v: (v['language'] or '', v['text'], v['predicate']))


def preferred_summary(groups, languages):
    for values in groups:
        if not values:
            continue
        for language in languages:
            parts = language.lower().split('-')
            while parts:
                wanted = '-'.join(parts)
                selected = [v for v in values if (v['language'] or 'und').lower() == wanted]
                if selected:
                    return selected[0]
                parts.pop()
                if parts and len(parts[-1]) == 1:
                    parts.pop()
        # A detail with its actual language is more useful than an invented translation.
        return values[0]
    return None


def fill_entries(spec, graph, records, names, by_iri, ownership, aux_rows):
    for record in records:
        if 'iri' not in record['identity']:
            continue
        subject = URIRef(record['identity']['iri'])
        visible = [n for n in names[str(subject)] if n['role'] != '隐藏名']
        definitions = text_values(graph, subject, SKOS.definition)
        scopes = text_values(graph, subject, SKOS.scopeNote)
        descriptions = text_values(graph, subject, DCTERMS.description)
        relations = {}
        for key, predicate, inverse in (('broader', SKOS.broader, SKOS.narrower),
                                        ('narrower', SKOS.narrower, SKOS.broader),
                                        ('related', SKOS.related, SKOS.related)):
            targets = set(graph.objects(subject, predicate)) | set(graph.subjects(inverse, subject))
            relations[key] = []
            for target in sorted(targets, key=str):
                if not isinstance(target, URIRef):
                    continue
                other = by_iri.get(str(target))
                relations[key].append({'identity': {'iri': str(target)},
                                       'label': other['label'] if other else str(target),
                                       'path': other['path'] if other else None})
        notes = []
        attachments = [(subject, set(NOTE_NAMES) - {SKOS.definition, SKOS.scopeNote, DCTERMS.description})]
        attachments += [(label, set(NOTE_NAMES) | set(PROVENANCE_NAMES))
                        for label in sorted({n['label'] for n in visible if n['label'] is not None}, key=str)]
        for attachment, predicates in attachments:
            for predicate in sorted(predicates, key=str):
                for value in text_values(graph, attachment, predicate):
                    notes.append({'identity': {'iri': str(attachment)}, **value})
                for value in graph.objects(attachment, predicate):
                    if isinstance(value, URIRef) and not any(graph.objects(value, RDF.value)):
                        notes.append({'identity': {'iri': str(attachment)}, 'predicate': str(predicate),
                                      'text': str(value), 'language': None, 'value_kind': 'iri'})
        record['entry'] = {'aliases': sorted({str(n['value']) for n in visible if alias_safe(str(n['value']))}),
                           'summary': preferred_summary((definitions, scopes, descriptions), spec['display']['languages']),
                           'definitions': definitions, 'scope_notes': scopes, 'descriptions': descriptions,
                           'relations': relations, 'notes': sorted(notes, key=lambda n: json.dumps(n, sort_keys=True)),
                           'fields': list(FIELD_ROLES.get(record['kind'], ())),
                           'raw_sources': [{'key': s.spec['key'], 'version': s.spec['version'], 'path': s.raw_path}
                                           for s in sorted(ownership[subject], key=lambda s: s.spec['key'])]}
        if record['kind'] == 'entities':
            record['entry']['facts'] = [{'predicate': str(p), 'value': rdf_value(v)}
                                        for p, v in sorted(graph.predicate_objects(subject), key=lambda pv: (str(pv[0]), json.dumps(rdf_value(pv[1]), sort_keys=True)))
                                        if p in FACT_NAMES]
    for record, data, raw_path in aux_rows:
        def auxiliary_text(key):
            value = data.get(key)
            if isinstance(value, str):
                return [{'text': value, 'language': None, 'predicate': key}]
            if isinstance(value, dict):
                return [{'text': text, 'language': lang, 'predicate': key}
                        for lang, text in sorted(value.items()) if isinstance(text, str)]
            return []
        definitions, scopes, descriptions = (auxiliary_text(k) for k in ('definition', 'scope', 'description'))
        notes = [{'identity': record['identity'], **value} for value in auxiliary_text('note')]
        basis = data.get('basis', {})
        for language in sorted(data.get('label', {})):
            item = basis.get(language) if isinstance(basis, dict) else None
            if isinstance(item, dict) and item.get('level') == 5:
                notes.append({'identity': record['identity'], 'predicate': f'basis.{language}', 'language': 'zh',
                              'text': f'{language} 名称：模型知识 · 第 5 级，外部用法未核实。'})
        record['entry'] = {'aliases': sorted({text for text in data.get('label', {}).values() if alias_safe(text)}),
                           'summary': preferred_summary((definitions, scopes, descriptions), spec['display']['languages']),
                           'definitions': definitions, 'scope_notes': scopes, 'descriptions': descriptions,
                           'relations': {'broader': [], 'narrower': [], 'related': []}, 'notes': notes,
                           'fields': list(FIELD_ROLES.get(record['kind'], ())),
                           'raw_sources': [{'key': record['sources'][0], 'version': record['versions'][0]['version'], 'path': raw_path}]}


def shape_target_nodes(graph, shape_graph):
    targets = set()
    for _, _, cls in shape_graph.triples((None, SH.targetClass, None)):
        targets.update(graph.subjects(RDF.type, cls))
    for _, _, predicate in shape_graph.triples((None, SH.targetSubjectsOf, None)):
        targets.update(graph.subjects(predicate, None))
    for _, _, predicate in shape_graph.triples((None, SH.targetObjectsOf, None)):
        targets.update(graph.objects(None, predicate))
    targets.update(shape_graph.objects(None, SH.targetNode))
    return targets


def validate_graph(graph, spec, records):
    profiles = spec['rules'].get('shacl_profiles', ['structure'])
    require(isinstance(profiles, list) and bool(profiles) and len(profiles) == len(set(profiles)) and all(p in ('structure', 'standard', 'target') for p in profiles), 'shacl_profiles 需要非空明确规则列表')
    shape_dir = resources.files('kb_vocab_shacl').joinpath('shapes')
    rule_files = {name: digest(shape_dir.joinpath(name).read_bytes()) for name in ('structure.ttl', 'skos.ttl', 'skos-xl.ttl', 'skos-thes.ttl', 'metadata.ttl', 'profile.ttl')}
    if 'shacl_sha256' in spec['rules']:
        require(spec['rules']['shacl_sha256'] == rule_files, 'SHACL 规则摘要不符')
    results, selections = [], []
    all_targets = set()
    for profile in profiles:
        shapes = Graph().parse(data=read_shapes(profile), format='turtle')
        targets = shape_target_nodes(graph, shapes)
        all_targets |= targets
        try:
            conforms, report, _ = validate(graph, shacl_graph=shapes, inference='none', inplace=False, advanced=True, allow_infos=False, allow_warnings=False)
        except Exception as exc:
            raise ContractError(f'SHACL 执行失败（{profile}）：{exc}') from exc
        if not isinstance(report, Graph):
            raise ContractError(f'SHACL 未返回有效结果（{profile}）：{report}')
        counts = Counter()
        for result in report.subjects(RDF.type, SH.ValidationResult):
            severity = report.value(result, SH.resultSeverity)
            shape = report.value(result, SH.sourceShape)
            component = report.value(result, SH.sourceConstraintComponent)
            counts[str(severity)] += 1
            # 空白节点在报告中无跨次身份，不让解析器临时编号破坏固定交付。
            messages = sorted(map(str, shapes.objects(shape, SH.message))) if shape is not None else []
            results.append({'profile': profile, 'severity': str(severity), 'focus': rdf_value(report.value(result, SH.focusNode)), 'path': rdf_value(report.value(result, SH.resultPath)) if report.value(result, SH.resultPath) is not None else None, 'value': rdf_value(report.value(result, SH.value)) if report.value(result, SH.value) is not None else None, 'shape': rdf_value(shape) if shape is not None else None, 'component': str(component), 'messages': messages or ['不符合该 SHACL 约束；按主体、属性和规则定位原值']})
        selections.append({'profile': profile, 'conforms': bool(conforms), 'target_count': len(targets), 'counts': dict(sorted(counts.items()))})
    entities = [r for r in records if r['kind'] == 'entities' and r['use'] == 'current']
    entity_targets = sum(URIRef(r['identity']['iri']) in all_targets for r in entities)
    summary = {'shacl': {'executed': True, 'profiles': selections, 'results': len(results), 'covered_named_subjects': len({s for s in all_targets if isinstance(s, URIRef)})}, 'entity_facts': {'executed': False, 'records': len(entities), 'skos_shape_targeted': entity_targets, 'reason': '现有 SKOS 结构规则不定义实体事实合同；命中共享属性不等于已校验实体事实'}, 'optional_field_inventory': {'executed': False, 'reason': '本次构建未执行全字段缺失统计'}, 'semantic_review': {'executed': False}, 'formal_use': {'confirmed': False, 'reason': '开发预览不授予正式准用'}}
    if spec.get('mode') == 'formal':
        summary['formal_use'] = {'confirmed': True, 'scope': 'application_use',
                                 'reason': '本实例应用使用授权及范围已固定；不表示实体事实或语义审阅通过'}
    implementation = {path.name: digest(path.read_bytes()) for path in sorted(Path(__file__).parent.glob('*.py'))}
    rules = dict(spec['rules']) | {'shacl_files': rule_files, 'projection_version': 3, 'metadata_version': 1, 'template_version': 3, 'implementation_sha256': implementation}
    return summary, {'format_version': 1, 'summary': summary, 'results': sorted(results, key=lambda r: json.dumps(r, ensure_ascii=False, sort_keys=True))}, rules


def projection_entries(sources, by_iri, displayed):
    result = []
    # 所有输入三元组按原主体登记；无稳定主体的结构以文件级记录说明。
    for source in sources:
        named = sorted({s for s in source.graph.subjects() if isinstance(s, URIRef)}, key=str)
        for subject in named:
            for predicate in sorted(set(source.graph.predicates(subject)), key=str):
                values = list(source.graph.objects(subject, predicate))
                blanks = [v for v in values if isinstance(v, BNode)]
                nonblanks = sorted((v for v in values if not isinstance(v, BNode)), key=lambda v: json.dumps(rdf_value(v), sort_keys=True))
                record = by_iri.get(str(subject))
                for value in nonblanks:
                    location = displayed.get((subject, predicate, value))
                    reason = '页面展示此值的文字或链接；完整结构仍以原件为准' if location else '未在页面展开；完整陈述与附属结构保留在原件，可由身份回查'
                    state = 'displayed' if location else 'raw_preserved'
                    if predicate in (SKOS.hiddenLabel, XL.hiddenLabel):
                        state, reason = 'raw_preserved', '隐藏名称不作为链接别名或推荐文字'
                    entry = {'identity': {'iri': str(subject)}, 'source_key': source.spec['key'], 'predicate': str(predicate), 'value': rdf_value(value), 'location': location if state == 'displayed' else source.raw_path, 'result': state, 'reason': reason}
                    result.append(entry)
                    if predicate in (SKOS.prefLabel, SKOS.altLabel) and isinstance(value, Literal) and not alias_safe(str(value)):
                        result.append(entry | {'location': record['path'] if record else source.raw_path, 'result': 'alias_excluded', 'reason': '文字不能安全进入 Obsidian 链接别名；名称正文和原件仍保留'})
                if blanks:
                    result.append({'identity': {'iri': str(subject)}, 'source_key': source.spec['key'], 'predicate': str(predicate), 'value': {'blank_node_structure': True, 'node_count': len(blanks)}, 'location': source.raw_path, 'result': 'raw_preserved', 'reason': '复杂结构原件回查；页面局部文字不冒充完整结构'})
        blank_triples = sum(isinstance(s, BNode) for s, _, _ in source.graph)
        if blank_triples:
            result.append({'identity': None, 'source_key': source.spec['key'], 'predicate': None, 'value': {'blank_node_structure': True, 'triple_count': blank_triples, 'input_sha256': source.spec['sha256']}, 'location': source.raw_path, 'result': 'raw_preserved', 'reason': '输入内空白节点三元组完整保留，不分配跨版本身份'})
    return sorted(result, key=lambda r: json.dumps(r, ensure_ascii=False, sort_keys=True))


def read_previous(previous):
    require(isinstance(previous, dict) and set(previous) == {'path', 'state_root', 'sha256'},
            'previous_delivery 需要 path、state_root 和 sha256；旧库内清单不自动迁移')
    vault, state_root = Path(previous['path']), Path(previous['state_root'])
    require(vault.is_absolute() and vault.is_dir() and state_root.is_absolute(),
            '上次交付与状态根目录须为现有绝对位置')
    from .storage import inspect, safe_path, vault_lock
    with vault_lock(vault, state_root=state_root):
        installed = inspect(vault, state_root=state_root)
        require(installed['manifest_sha256'] == previous['sha256'], '上次交付 manifest 摘要不符')
        require(installed['manifest'].get('format_version') == MANIFEST_VERSION,
                '旧版交付不自动迁移')
        state_dir = Path(installed['state_dir']) / 'current'
        raw = safe_path(state_dir, 'manifest.json').read_bytes()
        require(digest(raw) == previous['sha256'], '读取时上次交付 manifest 已变化')

        def pinned_bytes(directory, entries):
            values = {}
            for name, entry in entries.items():
                value = safe_path(directory, name).read_bytes()
                require(len(value) == entry['size'] and digest(value) == entry['sha256'],
                        f'读取时上次交付已改动：{name}')
                values[name] = value
            return values

        files = pinned_bytes(vault, installed['files'])
        state_files = pinned_bytes(state_dir, installed['state_files'])
        return previous['sha256'], raw, files, installed['records']['records'], state_files


def historical_bytes(raw, replacements):
    text = raw.decode('utf8')
    pieces = text.split('---', 2)
    require(len(pieces) == 3 and pieces[0] == '', '历史参考页缺少 frontmatter')
    props = yaml.safe_load(pieces[1])
    props['aliases'] = []
    props['trial_selectable'] = False
    props['selectable'] = False
    props['historical'] = True
    text = frontmatter(props) + '\n固定历史版本，只供读取旧引用，不供新选用。\n' + pieces[2]
    for original, target in sorted(replacements.items(), key=lambda item: -len(item[0])):
        text = text.replace('[[' + original[:-3] + '|', '[[' + target[:-3] + '|').replace('[[' + original[:-3] + ']]', '[[' + target[:-3] + ']]')
        text = text.replace('link(' + json.dumps(original[:-3]) + ')',
                            'link(' + json.dumps(target[:-3]) + ')')
    return text.encode()


def preserve_history(spec, files, state_files, records, previous_data=None):
    previous = spec.get('previous_delivery')
    if previous is None:
        return
    version, old_manifest, old_files, old_records, old_state_files = previous_data or read_previous(previous)
    require(json.loads(old_manifest)['mode'] == spec['mode'], '历史交付模式不一致，不能混用 preview 与 formal')
    for name, value in old_files.items():
        if name.startswith(f'{VOCABULARY}/history/'):
            require(name not in files or files[name] == value, f'历史文件冲突：{name}')
            files[name] = value
    for name, value in old_state_files.items():
        if name.startswith('inputs/'):
            require(name not in state_files or state_files[name] == value, f'历史原件冲突：{name}')
            state_files[name] = value
    state_files[f'inputs/{version}.json'] = old_manifest
    current_by_identity = {json.dumps(r['identity'], sort_keys=True): r for r in records}
    all_paths = {r['path'] for r in records}
    old_active = [r for r in old_records if r['use'] != 'historical']
    replacements = {r['path']: f'{VOCABULARY}/history/{version}/' + r['path'].removeprefix(VOCABULARY + '/') for r in old_active if r['use'] == 'current'}
    replacements.update({r['path']: r['history'][-1]['path'] for r in old_active if r['use'] == 'retained' and r['history']})
    for old in old_records:
        if old['use'] == 'historical' and old['path'] not in all_paths:
            records.append(old)
            all_paths.add(old['path'])
    for old in old_active:
        require(old['path'] in old_files, '历史记录没有对应受管理页面')
        key = json.dumps(old['identity'], sort_keys=True)
        history = list(old.get('history', []))
        if old['use'] == 'current':
            path = replacements[old['path']]
            files[path] = historical_bytes(old_files[old['path']], replacements)
            snapshot = deepcopy(old) | {'use': 'historical', 'path': path, 'trial_selectable': False, 'restrictions': ['固定历史版本，仅用于读取旧引用'], 'history': []}
            for relations in snapshot.get('entry', {}).get('relations', {}).values():
                for relation in relations:
                    relation['path'] = replacements.get(relation['path'], relation['path'])
            records.append(snapshot)
            history.append({'version': version, 'path': path})
        if key in current_by_identity:
            require(current_by_identity[key]['kind'] == old['kind'] and current_by_identity[key]['path'] == old['path'], '同一身份刷新后改变对象种类或稳定路径')
            current_by_identity[key]['history'] = history
            continue
        retained = dict(old) | {'use': 'retained', 'trial_selectable': False, 'history': history, 'restrictions': ['当前输入未包含该身份；原因未记录，旧入口只供历史查阅']}
        records.append(retained)
        fm = {'identifier': old['identity'].get('iri', old['identity'].get('id')), 'aliases': [], 'record_kind': old['kind'], 'preview': spec['mode'] == 'preview', 'trial_selectable': False, 'selectable': False, 'retained': True}
        target = history[-1]['path'] if history else None
        require(target is not None and target in files, '旧引用缺少固定历史文件')
        files[old['path']] = (frontmatter(fm) + f'\n# {md(old["label"])}\n\n当前输入未包含此身份。本入口仅供历史查阅，不供新选用。来源未说明缺席原因，不能据此认定停用或后继。\n\n原身份：{md(json.dumps(old["identity"], ensure_ascii=False, sort_keys=True))}\n\n最后可用描述：[[{target[:-3]}|固定历史版本]]。\n').encode()


def initial_pages(records):
    from .product import initial_files
    return initial_files()


def resource_catalog(graph, sources, page_records):
    """Keep nonpage resources and ordered members outside the authoring vault.

    Input bytes are authoritative for all statements, including blank-node
    structures; this inventory does not mint identities for those structures.
    """
    page_identities = {r['identity'].get('iri') for r in page_records}
    rows = []
    for subject in sorted({s for s in graph.subjects() if isinstance(s, URIRef)}, key=str):
        if str(subject) in page_identities:
            continue
        owners = [source for source in sources if any(source.graph.triples((subject, None, None)))]
        row = {'identity': {'iri': str(subject)},
               'source_types': sorted(map(str, graph.objects(subject, RDF.type))),
               'sources': sorted(source.spec['key'] for source in owners),
               'raw_sources': [{'key': source.spec['key'], 'version': source.spec['version'], 'path': source.raw_path}
                               for source in sorted(owners, key=lambda s: s.spec['key'])],
               'statements': [{'predicate': str(predicate), 'value': rdf_value(value)}
                              for predicate, value in sorted(graph.predicate_objects(subject),
                                  key=lambda pv: (str(pv[0]), json.dumps(rdf_value(pv[1]), sort_keys=True)))]}
        members = ordered_members(graph, subject)
        if members is not None:
            row['ordered_members'] = [rdf_value(member) for member in members]
        rows.append(row)
    return {'format_version': 1, 'resources': rows}


def build_delivery(input_path: Path) -> Delivery:
    """Build separate knowledge pages and external state without writing either."""
    spec, input_hash, state_files, sources, auxiliaries = read_inputs(Path(input_path))
    graph, all_records, names, by_iri, ownership, aux_rows = build_records(spec, sources, auxiliaries)
    records = [r for r in all_records if r['kind'] in KIND_DIRECTORIES]
    by_iri = {iri: record for iri, record in by_iri.items() if record['kind'] in KIND_DIRECTORIES}
    previous_data = read_previous(spec['previous_delivery']) if spec.get('previous_delivery') else None
    if previous_data:
        require(json.loads(previous_data[1])['mode'] == spec['mode'], '上次交付模式不一致，不能混用 preview 与 formal')
    assign_paths(records, previous_data[3] if previous_data else ())
    fill_entries(spec, graph, records, names, by_iri, ownership, aux_rows)
    files, displayed = {}, {}
    for record in records:
        if 'iri' in record['identity']:
            iri = record['identity']['iri']
            files[record['path']] = render_resource(record, graph, names[iri], by_iri, ownership[URIRef(iri)], projection=displayed)
    for record, row, raw_path in aux_rows:
        files[record['path']] = render_auxiliary(record, row, raw_path)
    validation, full_validation, rules = validate_graph(graph, spec, records)
    state_files['validation.json'] = json_bytes(full_validation)
    state_files['projection.json'] = json_bytes({'format_version': 1, 'entries': projection_entries(sources, by_iri, displayed)})
    state_files['resources.json'] = json_bytes(resource_catalog(graph, sources, records))
    preserve_history(spec, files, state_files, records, previous_data)
    records.sort(key=lambda r: r['path'])
    state_files['records.json'] = json_bytes({'format_version': 1, 'records': records})
    environment = {'python': platform.python_version(), 'dependencies': {name: metadata.version(name) for name in ('rdflib', 'PyYAML', 'pyshacl', 'kb-vocab-shacl', 'markdown-it-py', 'mdurl')}}
    manifest = {'format_version': MANIFEST_VERSION, 'mode': spec['mode'], 'input_sha256': input_hash,
                'sources': [{**source.spec, 'raw_path': source.raw_path} for source in sources],
                'auxiliary': [{**item, 'raw_path': raw_path} for item, _, raw_path in auxiliaries],
                'display': spec['display'], 'rules': rules, 'producer': spec['producer'],
                'environment': environment, 'previous_delivery': spec.get('previous_delivery'),
                'validation': validation,
                'files': [{'path': p, 'role': 'history' if p.startswith(f'{VOCABULARY}/history/') else 'reference',
                           'size': len(value), 'sha256': digest(value)} for p, value in sorted(files.items())],
                'state_files': [{'path': p, 'role': 'raw_input' if p.startswith('inputs/') else 'metadata',
                                 'size': len(value), 'sha256': digest(value)} for p, value in sorted(state_files.items())]}
    state_files['manifest.json'] = json_bytes(manifest)
    files.update(initial_pages(records))
    return Delivery(files, state_files)
