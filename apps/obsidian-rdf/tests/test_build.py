import json
from pathlib import Path

import pytest
import yaml

from kb_obsidian_rdf.common import ContractError, digest, reference_path
from kb_obsidian_rdf import __version__
from kb_obsidian_rdf.build import build_delivery

PREFIX = '''@prefix ex: <https://example.org/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xl: <http://www.w3.org/2008/05/skos-xl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
'''


def input_file(tmp_path, data, subjects=('c',), entity_class=None, **overrides):
    raw = (PREFIX + data).encode()
    (tmp_path / 'data.ttl').write_bytes(raw)
    source = dict(key='test', path='data.ttl', format='turtle', sha256=digest(raw),
                  identity='test-source', version='v1',
                  scope={'subject_iris': ['https://example.org/' + s for s in subjects]},
                  trial_subjects=['https://example.org/' + s for s in subjects],
                  authority={'preview_reference': 'test approval', 'scope_reference': 'test scope', 'formal_reference': None})
    if entity_class:
        source['scope'] = {'entity_class_iris': ['https://example.org/' + entity_class]}
    value = dict(format_version=1, mode='preview', sources=[source], auxiliary=[],
                 display=['zh', 'en'], rules={'shacl_profiles': ['structure']},
                 producer={'name': 'kb-obsidian-rdf', 'version': __version__}, previous_delivery=None)
    value.update(overrides)
    path = tmp_path / 'input.json'
    path.write_text(json.dumps(value), encoding='utf8')
    return path


def install(vault, delivery):
    from kb_obsidian_rdf.storage import initialize
    state_root = vault.parent / 'state'
    initialize(vault, delivery, state_root=state_root)
    return state_root


def records(files):
    return json.loads(files.state_files['records.json'])['records']


def frontmatter(data):
    return yaml.safe_load(data.decode().split('---', 2)[1])


def resource_path(files, iri):
    return next(r['path'] for r in records(files) if r['identity'] == {'iri': iri} and r['use'] != 'historical')


def test_identity_hidden_labels_complex_raw_and_repeatability(tmp_path):
    path = input_file(tmp_path, '''ex:c a skos:Concept; skos:prefLabel "相同"@zh;
       skos:altLabel "Alias"@en; skos:hiddenLabel "secret-typo"@en;
       skos:definition [ rdf:value "<script>[[evil]]</script>"@en ];
       ex:unknown [ ex:child "deep" ].
       ''')
    spec = json.loads(path.read_text())
    eraw = (PREFIX + 'ex:e a ex:Software; skos:prefLabel "相同"@zh .').encode()
    (tmp_path / 'entities.ttl').write_bytes(eraw)
    entity = dict(spec['sources'][0], key='entities', path='entities.ttl', sha256=digest(eraw), scope={'entity_class_iris':['https://example.org/Software']}, trial_subjects=['https://example.org/e'])
    spec['sources'].append(entity)
    path.write_text(json.dumps(spec))
    files = build_delivery(path)
    assert files == build_delivery(path)
    by_kind = {r['kind']: r for r in records(files)}
    assert set(by_kind) == {'concepts', 'entities'}
    concept = files.vault_files[by_kind['concepts']['path']]
    assert 'secret-typo' not in frontmatter(concept)['aliases']
    assert '<script>' not in concept.decode()
    assert '[[evil]]' not in concept.decode()
    assert any(v == (tmp_path / 'data.ttl').read_bytes() for p, v in files.state_files.items() if p.startswith('inputs/'))
    entries = json.loads(files.state_files['projection.json'])['entries']
    assert any(e['predicate'] == 'https://example.org/unknown' and e['result'] == 'raw_preserved' for e in entries)
    assert by_kind['entities']['identity'] == {'iri': 'https://example.org/e'}


def test_invalid_hash_and_scope_stop_before_output(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept .')
    spec = json.loads(path.read_text())
    spec['sources'][0]['sha256'] = '0' * 64
    path.write_text(json.dumps(spec))
    with pytest.raises(ContractError, match='摘要'):
        build_delivery(path)
    spec['sources'][0]['sha256'] = digest((tmp_path / 'data.ttl').read_bytes())
    spec['sources'][0]['trial_subjects'].append('https://example.org/missing')
    path.write_text(json.dumps(spec))
    with pytest.raises(ContractError, match='范围'):
        build_delivery(path)


def test_relative_identity_requires_source_base(tmp_path):
    path = input_file(tmp_path, '<relative> a skos:Concept .')
    with pytest.raises(ContractError, match='base_iri'):
        build_delivery(path)


def test_conflicting_xl_names_and_role_conflicts_stop(tmp_path):
    path = input_file(tmp_path, '''ex:c a skos:Concept; skos:prefLabel "First"@en; xl:prefLabel ex:name.
       ex:name a xl:Label; xl:literalForm "Second"@en .''')
    with pytest.raises(ContractError, match='首选'):
        build_delivery(path)
    path = input_file(tmp_path, 'ex:c a skos:Concept; skos:prefLabel "same"@en; skos:hiddenLabel "same"@en .')
    with pytest.raises(ContractError, match='角色'):
        build_delivery(path)


def test_source_disappearance_preserves_original_link_and_version(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept; skos:prefLabel "Old"@en .')
    old = build_delivery(path)
    vault = tmp_path / 'vault'
    state_root = install(vault, old)
    old_hash = digest(old.state_files['manifest.json'])
    path = input_file(tmp_path, 'ex:d a skos:Concept; skos:prefLabel "New"@en .', ('d',),
                      previous_delivery={'path': str(vault), 'state_root': str(state_root), 'sha256': old_hash})
    new = build_delivery(path)
    old_path = resource_path(old, 'https://example.org/c')
    record = next(r for r in records(new) if r['path'] == old_path)
    assert record['use'] == 'retained'
    assert not record['trial_selectable']
    assert frontmatter(new.vault_files[old_path]).get('aliases', []) == []
    assert any(r['use'] == 'historical' for r in records(new))
    assert old_hash in new.vault_files[old_path].decode()
    assert new == build_delivery(path)
    (vault / old_path).write_text('changed')
    with pytest.raises(ContractError, match='摘要|改动'):
        build_delivery(path)


def test_ordered_collection_preserves_order_duplicates_and_rejects_cycles(tmp_path):
    path = input_file(tmp_path, '''ex:c a skos:Concept; skos:prefLabel "C"@en.
    ex:d a skos:Concept; skos:prefLabel "D"@en.
    ex:list a skos:OrderedCollection; skos:memberList (ex:d ex:c ex:d).''', ('c', 'd'))
    files = build_delivery(path)
    resource = next(r for r in json.loads(files.state_files['resources.json'])['resources'] if r['identity'] == {'iri': 'https://example.org/list'})
    assert resource['ordered_members'] == [{'iri': 'https://example.org/d'}, {'iri': 'https://example.org/c'}, {'iri': 'https://example.org/d'}]
    assert all(r['kind'] not in ('collections', 'schemes') for r in records(files))
    assert not any('/collections/' in name or '/schemes/' in name for name in files.vault_files)
    path = input_file(tmp_path, '''ex:c a skos:Concept .
    ex:list a skos:OrderedCollection; skos:memberList _:loop.
    _:loop rdf:first ex:c; rdf:rest _:loop.''')
    with pytest.raises(ContractError, match='列表'):
        build_delivery(path)


def test_known_deprecated_cannot_be_reactivated_by_trial_list(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept; owl:deprecated true .')
    record = records(build_delivery(path))[0]
    assert not record['trial_selectable']
    assert record['source_state']


def test_entity_coverage_not_mistaken_for_skos_validation(tmp_path):
    path = input_file(tmp_path, 'ex:c a ex:Software; skos:prefLabel "Software"@en .', entity_class='Software')
    manifest = json.loads(build_delivery(path).state_files['manifest.json'])
    assert manifest['validation']['entity_facts']['executed'] is False
    assert manifest['validation']['shacl']['executed'] is True


def test_unknown_source_types_do_not_become_entities(tmp_path):
    path = input_file(tmp_path, 'ex:c a rdf:Property .')
    with pytest.raises(ContractError, match='对象种类'):
        build_delivery(path)


def test_out_of_scope_duplicate_statements_cannot_override_selected_identity(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept; skos:prefLabel "Name"@en .')
    spec = json.loads(path.read_text())
    raw = (PREFIX + 'ex:d a skos:Concept . ex:c skos:prefLabel "Changed"@zh .').encode()
    (tmp_path / 'second.ttl').write_bytes(raw)
    source = dict(spec['sources'][0], key='second', path='second.ttl', sha256=digest(raw), scope={'subject_iris':['https://example.org/d']}, trial_subjects=['https://example.org/d'])
    spec['sources'].append(source)
    path.write_text(json.dumps(spec))
    with pytest.raises(ContractError, match='跨源组合'):
        build_delivery(path)


def test_short_page_uses_relationships_without_large_embedded_query(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept; skos:prefLabel "Parent"@en . ex:d a skos:Concept; skos:broader ex:c; skos:prefLabel "Child"@en .', ('c','d'))
    files = build_delivery(path)
    page = files.vault_files[resource_path(files, 'https://example.org/c')].decode()
    assert '```base' not in page
    assert resource_path(files, 'https://example.org/d')[:-3] in page
    assert not any(name.startswith('notes/') for name in files.vault_files)


def test_numeric_label_is_not_a_safe_text_projection(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept; skos:prefLabel 123 .')
    with pytest.raises(ContractError, match='文字字面值'):
        build_delivery(path)


def test_xl_translation_creator_is_visible_on_its_label(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept; xl:prefLabel ex:name . ex:name a xl:Label; xl:literalForm "名称"@zh; <http://purl.org/dc/terms/creator> ex:translator .')
    files = build_delivery(path)
    page = files.vault_files[resource_path(files, 'https://example.org/c')].decode()
    assert 'creator' in page and 'translator' in page
    assert page.index('## 名称说明') < page.index('creator')


def test_auxiliary_active_requires_separate_adoption_and_retains_it(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept .')
    spec = json.loads(path.read_text())
    raw = yaml.safe_dump({'schema_version':3, 'types':[{'id':'tutorial','label':{'zh':'教程'},'status':'active'}]}).encode()
    (tmp_path / 'types.yaml').write_bytes(raw)
    authority = dict(spec['sources'][0]['authority'])
    item = {'key':'types','kind':'types','path':'types.yaml','format':'yaml','sha256':digest(raw),'schema_version':3,'version':'v1','authority':authority}
    spec['auxiliary']=[item]
    path.write_text(json.dumps(spec))
    row = next(r for r in records(build_delivery(path)) if r['kind']=='types')
    assert not row['trial_selectable'] and row['formal_basis'] is None
    evidence = tmp_path / 'adoption.md'
    evidence.write_text('Existing active values are approved.')
    authority.update(formal_reference=evidence.as_uri(), formal_evidence_sha256=digest(evidence.read_bytes()))
    path.write_text(json.dumps(spec))
    files=build_delivery(path)
    row = next(r for r in records(files) if r['kind']=='types')
    assert row['trial_selectable'] and row['formal_basis']==[evidence.as_uri()]
    assert row['path'] == 'vocabulary/document-types/教程.md'
    assert evidence.read_bytes() in files.state_files.values()
    evidence.write_text('Modified after input was pinned')
    with pytest.raises(ContractError, match='摘要'):
        build_delivery(path)


def test_cross_source_label_definition_requires_compatibility_and_provenance(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept; xl:prefLabel ex:name .')
    spec = json.loads(path.read_text())
    raw = (PREFIX + 'ex:d a skos:Concept . ex:name a xl:Label; xl:literalForm "From B"@en .').encode()
    (tmp_path/'second.ttl').write_bytes(raw)
    spec['sources'].append(dict(spec['sources'][0], key='second', path='second.ttl',
                                sha256=digest(raw), scope={'subject_iris':['https://example.org/d']},
                                trial_subjects=['https://example.org/d']))
    path.write_text(json.dumps(spec))
    with pytest.raises(ContractError, match='跨源组合'):
        build_delivery(path)
    spec['compatible_sources']=[['test','second']]
    path.write_text(json.dumps(spec))
    row=next(r for r in records(build_delivery(path)) if r['identity']=={'iri':'https://example.org/c'})
    assert row['label']=='From B'
    assert row['sources']==['second','test']


def test_blank_node_display_order_is_repeatable(tmp_path):
    path=input_file(tmp_path, 'ex:c a skos:Concept; skos:prefLabel "C"@en; '
                    'ex:unknown [rdf:value "A"], [rdf:value "B"], [rdf:value "C"], '
                    '[rdf:value "same"@en, "same"@zh] .')
    files = build_delivery(path)
    page=resource_path(files, 'https://example.org/c')
    hashes={digest(build_delivery(path).vault_files[page]) for _ in range(3)}
    assert len(hashes)==1


def test_historical_relation_uses_fixed_version_paths(tmp_path):
    path=input_file(tmp_path, 'ex:c a skos:Concept . ex:d a skos:Concept; skos:broader ex:c .', ('c','d'))
    old=build_delivery(path)
    vault=tmp_path/'old'
    state_root = install(vault, old)
    old_hash=digest(old.state_files['manifest.json'])
    path=input_file(tmp_path, 'ex:c a skos:Concept .', previous_delivery={'path':str(vault),'state_root':str(state_root),'sha256':old_hash})
    files=build_delivery(path)
    parent=resource_path(old, 'https://example.org/c')
    child=resource_path(old, 'https://example.org/d')
    history='vocabulary/history/'+old_hash+'/'+parent.removeprefix('vocabulary/')
    assert f'[[{child[:-3]}|' not in files.vault_files[history].decode()
    assert f'[[vocabulary/history/{old_hash}/{child.removeprefix("vocabulary/")[:-3]}|' in files.vault_files[history].decode()


def test_registered_form_preserves_unassigned_state_without_losing_its_value_domain(tmp_path):
    path=input_file(tmp_path,'ex:c a skos:Concept .')
    spec=json.loads(path.read_text())
    raw=yaml.safe_dump({'schema_version':3,'forms':[{'id':'diagram','label':{'en':'Diagram'},'status':'unassigned'}]}).encode()
    (tmp_path/'forms.yaml').write_bytes(raw)
    permission={**spec['sources'][0]['authority'],'formal_reference':'Content model retains this form value'}
    spec['auxiliary']=[{'key':'forms','kind':'forms','path':'forms.yaml','format':'yaml',
                        'schema_version':3,'sha256':digest(raw),'version':'v1','authority':permission}]
    path.write_text(json.dumps(spec))
    form=next(r for r in records(build_delivery(path)) if r['kind']=='forms')
    assert form['source_state']['status']=='unassigned'
    assert form['trial_selectable']


def test_new_paths_are_readable_and_same_name_identities_stay_distinct(tmp_path):
    path = input_file(tmp_path, '''ex:c a skos:Concept; skos:prefLabel "网络"@zh .
    ex:d a skos:Concept; skos:prefLabel "重复"@zh .
    ex:e a skos:Concept; skos:prefLabel "重复"@zh .''', ('c', 'd', 'e'))
    rows = {r['identity']['iri']: r for r in records(build_delivery(path))}
    assert rows['https://example.org/c']['path'] == 'vocabulary/concepts/网络.md'
    assert rows['https://example.org/d']['path'].startswith('vocabulary/concepts/重复-')
    assert rows['https://example.org/e']['path'].startswith('vocabulary/concepts/重复-')
    assert len({r['path'] for r in rows.values()}) == 3
    assert rows['https://example.org/d']['label'] == rows['https://example.org/e']['label'] == '重复'


def test_entry_preserves_note_attachment_and_reports_undisplayed_values(tmp_path):
    path = input_file(tmp_path, '''ex:c a skos:Concept; xl:prefLabel ex:label;
        skos:scopeNote "概念适用范围"@zh; skos:hiddenLabel "错拼"@zh;
        ex:unknown "unprojected" .
    ex:label a xl:Label; xl:literalForm "名称"@zh;
        skos:definition "这是名称说明，不是概念定义"@zh;
        skos:editorialNote "模型译名，外部用法未核实"@zh .''')
    files = build_delivery(path)
    record = records(files)[0]
    entry = record.get('entry')
    assert entry is not None
    assert entry['definitions'] == []
    assert entry['summary'] == {'text': '概念适用范围', 'language': 'zh', 'predicate': 'http://www.w3.org/2004/02/skos/core#scopeNote'}
    assert '错拼' not in entry['aliases']
    assert any(n['identity'] == {'iri': 'https://example.org/label'} and n['text'] == '这是名称说明，不是概念定义' for n in entry['notes'])
    page = files.vault_files[record['path']].decode()
    assert '外部用法未核实' in page
    assert '## 定义' not in page
    assert 'unprojected' not in page
    assert '```base' not in page
    projected = json.loads(files.state_files['projection.json'])['entries']
    assert any(e['predicate'] == 'https://example.org/unknown' and e['result'] == 'raw_preserved' for e in projected)


def test_entry_relations_use_explicit_skos_inverse_without_reclassifying_subjects(tmp_path):
    path = input_file(tmp_path, '''ex:c a skos:Concept; skos:prefLabel "Parent"@en;
    skos:related ex:e . ex:d a skos:Concept; skos:prefLabel "Child"@en; skos:broader ex:c .
    ex:e a skos:Concept; skos:prefLabel "Related"@en .''', ('c', 'd', 'e'))
    files = build_delivery(path)
    rows = {r['identity']['iri']: r for r in records(files)}
    parent, child, related = (rows['https://example.org/' + suffix] for suffix in ('c', 'd', 'e'))
    assert parent.get('entry', {}).get('relations', {}).get('narrower') == [{'identity': child['identity'], 'label': 'Child', 'path': child['path']}]
    assert child['entry']['relations']['broader'] == [{'identity': parent['identity'], 'label': 'Parent', 'path': parent['path']}]
    assert related['entry']['relations']['related'] == [{'identity': parent['identity'], 'label': 'Parent', 'path': parent['path']}]
    assert not any(name.startswith('notes/') for name in files.vault_files)


@pytest.mark.parametrize('labels', [('Foo', 'foo'), ('é', 'e\u0301'), ('x/y', 'x:y'), ('字' * 150, '字' * 150 + '长')])
def test_file_collisions_are_portable_and_do_not_change_original_names(tmp_path, labels):
    import unicodedata
    data = '\n'.join(f'ex:{name} a skos:Concept; skos:prefLabel {json.dumps(label)}@en .' for name, label in zip(('c', 'd'), labels))
    path = input_file(tmp_path, data, ('c', 'd'))
    rows = records(build_delivery(path))
    assert all(Path(r['path']).stem.startswith(label.lower().split('/')[0][:1]) for r, label in zip(sorted(rows, key=lambda r: r['identity']['iri']), labels))
    assert {r['label'] for r in rows} == set(labels)
    assert len({unicodedata.normalize('NFC', r['path']).casefold() for r in rows}) == 2
    assert all(len(Path(r['path']).name.encode()) <= 255 for r in rows)
    assert all(not any(c in Path(r['path']).name for c in ':/*?<>|#^[]') for r in rows)


def test_windows_device_label_is_escaped_only_in_path(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept; skos:prefLabel "CON"@en .')
    record = records(build_delivery(path))[0]
    assert Path(record['path']).name.lower() != 'con.md'
    assert 'con' in Path(record['path']).name
    assert record['label'] == 'CON'


def test_short_auxiliary_page_keeps_model_translation_warning(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept .')
    spec = json.loads(path.read_text())
    raw = yaml.safe_dump({'schema_version': 3, 'forms': [{'id': 'diagram', 'label': {'zh': '示意图'},
        'scope': '图示结构', 'status': 'unassigned', 'basis': {'zh': {'level': 5, 'model': {'name': 'test-model'}}}}]}, allow_unicode=True).encode()
    (tmp_path / 'forms.yaml').write_bytes(raw)
    authority = {**spec['sources'][0]['authority'], 'formal_reference': 'Existing form contract'}
    spec['auxiliary'] = [{'key': 'forms', 'kind': 'forms', 'path': 'forms.yaml', 'format': 'yaml',
        'schema_version': 3, 'sha256': digest(raw), 'version': 'v1', 'authority': authority}]
    path.write_text(json.dumps(spec))
    files = build_delivery(path)
    row = next(r for r in records(files) if r['kind'] == 'forms')
    assert '外部用法未核实' in files.vault_files[row['path']].decode()
    assert any('外部用法未核实' in n['text'] for n in row['entry']['notes'])


def test_historical_structured_relations_follow_historical_paths(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept; skos:prefLabel "Parent"@en. ex:d a skos:Concept; skos:prefLabel "Child"@en; skos:broader ex:c .', ('c', 'd'))
    old = build_delivery(path)
    vault = tmp_path / 'old'
    state_root = install(vault, old)
    old_hash = digest(old.state_files['manifest.json'])
    path = input_file(tmp_path, 'ex:c a skos:Concept; skos:prefLabel "Updated"@en .', previous_delivery={'path': str(vault), 'state_root': str(state_root), 'sha256': old_hash})
    files = build_delivery(path)
    current = next(r for r in records(files) if r['identity'] == {'iri': 'https://example.org/c'} and r['use'] == 'current')
    historical = next(r for r in records(files) if r['identity'] == current['identity'] and r['use'] == 'historical')
    assert current['path'] == resource_path(old, 'https://example.org/c')
    assert historical['entry']['relations']['narrower'][0]['path'].startswith(f'vocabulary/history/{old_hash}/')


def test_refresh_preserves_old_hash_path_after_label_change(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept; skos:prefLabel "Before"@en .')
    old = build_delivery(path)
    old_path = resource_path(old, 'https://example.org/c')
    hashed = reference_path('concepts', {'iri': 'https://example.org/c'}).replace('vocab/', 'vocabulary/', 1)
    legacy_records = json.loads(old.state_files['records.json'])
    legacy_records['records'][0]['path'] = hashed
    from kb_obsidian_rdf.common import json_bytes
    old.state_files['records.json'] = json_bytes(legacy_records)
    old.vault_files[hashed] = old.vault_files.pop(old_path)
    manifest = json.loads(old.state_files['manifest.json'])
    for item in manifest['files']:
        if item['path'] == old_path:
            item['path'] = hashed
        item['size'] = len(old.vault_files[item['path']])
        item['sha256'] = digest(old.vault_files[item['path']])
    for item in manifest['state_files']:
        item['size'] = len(old.state_files[item['path']])
        item['sha256'] = digest(old.state_files[item['path']])
    old.state_files['manifest.json'] = json_bytes(manifest)
    vault = tmp_path / 'old'
    state_root = install(vault, old)
    path = input_file(tmp_path, 'ex:c a skos:Concept; skos:prefLabel "After"@en .', previous_delivery={'path': str(vault), 'state_root': str(state_root), 'sha256': digest(old.state_files['manifest.json'])})
    files = build_delivery(path)
    assert resource_path(files, 'https://example.org/c') == hashed
    assert frontmatter(files.vault_files[hashed])['title'] == 'After'


def test_para_delivery_keeps_engineering_inputs_outside_vault(tmp_path):
    path = input_file(tmp_path, 'ex:c a skos:Concept; skos:prefLabel "Model_Context Protocol"@en .')
    files = build_delivery(path)
    assert set(files.vault_files) == {'home.md', 'views/article-list.base', 'templates/article.md', 'vocabulary/concepts/model-context-protocol.md'}
    assert all(name == name.lower() and '_' not in name and ' ' not in name for name in files.vault_files)
    assert {'records.json', 'projection.json', 'validation.json', 'resources.json', 'manifest.json'} <= set(files.state_files)
    assert any(name.startswith('inputs/') for name in files.state_files)
    page = files.vault_files['vocabulary/concepts/model-context-protocol.md']
    assert frontmatter(page)['title'] == 'Model_Context Protocol'
    assert frontmatter(page)['identifier'] == 'https://example.org/c'
    assert '[[inputs/' not in page.decode() and '[[vocab/' not in page.decode()
    home = files.vault_files['home.md'].decode()
    assert all(root in home for root in ('inbox', 'projects', 'areas', 'resources', 'archives'))
    manifest = json.loads(files.state_files['manifest.json'])
    assert manifest['format_version'] == 2
    assert all(row['path'].startswith('vocabulary/') for row in manifest['files'])
    assert 'manifest.json' not in {row['path'] for row in manifest['state_files']}


def test_lowercase_filename_never_changes_case_sensitive_rdf_identity(tmp_path):
    path = input_file(tmp_path, 'ex:CaseKey a skos:Concept; skos:prefLabel "Model_Context Protocol"@en .', ('CaseKey',))
    files = build_delivery(path)
    row = records(files)[0]
    assert row['identity'] == {'iri': 'https://example.org/CaseKey'}
    assert row['label'] == 'Model_Context Protocol'
    assert row['path'] == 'vocabulary/concepts/model-context-protocol.md'
    assert frontmatter(files.vault_files[row['path']])['identifier'] == 'https://example.org/CaseKey'


def test_spaces_underscores_and_hyphens_collide_without_merging_objects(tmp_path):
    labels = ['Model Context', 'model_context', 'model--context']
    data = '\n'.join(f'ex:{name} a skos:Concept; skos:prefLabel {json.dumps(label)}@en .' for name, label in zip(('c', 'd', 'e'), labels))
    path = input_file(tmp_path, data, ('c', 'd', 'e'))
    rows = records(build_delivery(path))
    assert {row['label'] for row in rows} == set(labels)
    assert len({row['path'] for row in rows}) == 3
    assert all(Path(row['path']).stem.startswith('model-context-') and '--' not in row['path'] for row in rows)


def test_old_vault_internal_state_is_not_implicitly_migrated(tmp_path):
    old_vault = tmp_path / 'old-vault'
    old_vault.mkdir()
    (old_vault / 'vocab').mkdir()
    (old_vault / 'vocab' / '_manifest.json').write_text('{"format_version": 1, "mode": "preview"}')
    path = input_file(tmp_path, 'ex:c a skos:Concept .', previous_delivery={'path': str(old_vault), 'sha256': digest((old_vault / 'vocab' / '_manifest.json').read_bytes())})
    with pytest.raises(ContractError, match='旧库内清单不自动迁移'):
        build_delivery(path)
