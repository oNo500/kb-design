"""Formal permissions, pending scope and immutable entity provenance boundaries."""
import json
from pathlib import Path

import pytest

from kb_obsidian_rdf.common import ContractError, digest, json_bytes
from kb_obsidian_rdf.input import read_inputs
from kb_obsidian_rdf.prepare import prepare


@pytest.fixture
def formal_inputs(tmp_path):
    # A candidate remains usable, an explicitly deprecated entity does not.
    from kb_vocab_maintenance.entities import build_entities
    concept = b'<urn:ready> a <http://www.w3.org/2004/02/skos/core#Concept> .\n<urn:pending> a <http://www.w3.org/2004/02/skos/core#Concept> .\n'
    for directory, filename, raw in [
        ('ccs/partitioned-20260921-rdf', 'concepts.ttl', concept),
        ('writing/expanded-20260922-final', 'vocabulary.ttl', b'<urn:writing> a <http://www.w3.org/2004/02/skos/core#Concept> .\n'),
    ]:
        base = tmp_path/'output/vocabulary'/directory
        base.mkdir(parents=True)
        (base/filename).write_bytes(raw)
        (base/'manifest.json').write_bytes(json_bytes({'files': {filename: digest(raw)}}))
    routing = tmp_path/'data/inputs/ccs/routing.json'
    routing.parent.mkdir(parents=True)
    routing.write_bytes(json_bytes({'confirmed': True, 'items': [
        {'source_id': 'urn:ready', 'action': 'both'},
        {'source_id': 'urn:pending', 'action': 'pending'}]}))
    ccs = tmp_path/'output/vocabulary/ccs/partitioned-20260921-rdf'
    (ccs/'plan.json').write_bytes(routing.read_bytes())
    manifest = json.loads((ccs/'manifest.json').read_bytes())
    manifest['files']['plan.json'] = digest(routing.read_bytes())
    (ccs/'manifest.json').write_bytes(json_bytes(manifest))
    for kind in ('types', 'genres', 'forms', 'references'):
        relative = 'data/references/bibliography.yaml' if kind == 'references' else f'data/vocab/{kind}.yaml'
        path = tmp_path/relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'{kind}: []\nschema_version: 3\nversion: test\n')
    model = tmp_path/'docs/model/content/设计-内容模型.md'
    model.parent.mkdir(parents=True)
    model.write_text('既有内容类型约束\n')
    authority = tmp_path/'approval.md'
    authority.write_text('已授权本实例正式使用当前概念及统一实体；保留原状态。\n')
    entity_authority = tmp_path/'entity-authority.md'
    entity_authority.write_text('基本字段通过可以使用，candidate 不阻断，停用不恢复。\n')
    source = tmp_path/'original-entities'
    source.mkdir()
    graph = b'''@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
<urn:candidate> a <http://www.wikidata.org/entity/Q7397>; skos:prefLabel "Tool"@en .
<urn:active> a <http://www.wikidata.org/entity/Q5>; skos:prefLabel "Person"@en .
<urn:deprecated> a <http://www.wikidata.org/entity/Q7397>; skos:prefLabel "Old"@en .
'''
    (source/'entities.ttl').write_bytes(graph)
    states = {'urn:candidate': {'status': 'candidate', 'facts_verified': False},
              'urn:active': {'status': 'active'}, 'urn:deprecated': {'status': 'deprecated'}}
    manifest = {'files': {'entities.ttl': digest(graph)}, 'entity_iris': list(states), 'source_states': states}
    (source/'manifest.json').write_bytes(json_bytes(manifest))
    config = tmp_path/'entity-config.json'
    config.write_bytes(json_bytes({'schema_version': 1, 'policy': 'basic-fields-v1',
        'authority': {'path': 'entity-authority.md', 'sha256': digest(entity_authority.read_bytes())},
        'sources': [{'key': 'legacy', 'directory': 'original-entities',
                     'manifest_sha256': digest((source/'manifest.json').read_bytes()), 'entity_file': 'entities.ttl'}]}))
    entities = tmp_path/'entities/versions/v1'
    build_entities(config, tmp_path, entities)
    current = tmp_path/'entities/current'
    current.symlink_to('versions/v1', target_is_directory=True)
    path = tmp_path/'formal.json'
    return tmp_path, authority, current, entities, path


def make_formal(fixture):
    root, authority, current, entities, path = fixture
    prepare(root, path, authority=authority, mode='formal', entities=current)
    return json.loads(path.read_bytes())


def write_spec(path, value):
    path.write_bytes(json_bytes(value))


def test_formal_retains_identity_original_states_and_every_frozen_original(formal_inputs):
    root, authority, current, entities, path = formal_inputs
    document = make_formal(formal_inputs)
    entity_spec = next(item for item in document['sources'] if item['key'] == 'entities')
    assert entity_spec['entity_delivery']['directory'] == str(entities)
    assert 'trial_subjects' not in entity_spec
    assert entity_spec['selectable_subjects'] == ['urn:active', 'urn:candidate']
    current.unlink()  # The input is independent of a later current-pointer change.
    spec, _, frozen, sources, _ = read_inputs(path)
    source = next(item for item in sources if item.spec['key'] == 'entities')
    assert set(map(str, source.selected)) == {'urn:active', 'urn:candidate', 'urn:deprecated'}
    assert source.entity_delivery['formal_release'] is False
    assert source.entity_delivery['entities']['urn:candidate']['sources'][0]['state'] == {'status': 'candidate', 'facts_verified': False}
    assert all(original.read_bytes() in frozen.values() for original in entities.rglob('*') if original.is_file())
    assert authority.read_bytes() in frozen.values()
    assert (root/'output/vocabulary/ccs/partitioned-20260921-rdf/plan.json').read_bytes() in frozen.values()
    ccs = next(item for item in sources if item.spec['key'] == 'ccs-concepts')
    assert set(map(str, ccs.selected)) == {'urn:ready', 'urn:pending'}
    assert ccs.spec['selectable_subjects'] == ['urn:ready']
    assert ccs.spec['source_states']['urn:pending'] == {'routing_action': 'pending'}
    assert 'urn:ready' not in ccs.spec['source_states']


def test_formal_mode_string_does_not_replace_local_pinned_authority(formal_inputs):
    document = make_formal(formal_inputs)
    path = formal_inputs[-1]
    document['sources'][0]['authority']['formal_reference'] = None
    document['sources'][0]['authority'].pop('formal_evidence_sha256')
    write_spec(path, document)
    with pytest.raises(ContractError, match='正式'):
        read_inputs(path)


@pytest.mark.parametrize('change', ['mixed-selection', 'pending-selected', 'incomplete-entity-scope', 'ineligible-selected'])
def test_formal_rejects_scope_expansion_and_incomplete_identity(formal_inputs, change):
    document = make_formal(formal_inputs)
    path = formal_inputs[-1]
    ccs = next(item for item in document['sources'] if item['key'] == 'ccs-concepts')
    entities = next(item for item in document['sources'] if item['key'] == 'entities')
    if change == 'mixed-selection':
        ccs['trial_subjects'] = ['urn:ready']
    elif change == 'pending-selected':
        ccs['selectable_subjects'].append('urn:pending')
    elif change == 'incomplete-entity-scope':
        entities['scope'] = {'entity_class_iris': ['http://www.wikidata.org/entity/Q7397']}
        entities['selectable_subjects'] = ['urn:candidate']
    else:
        entities['selectable_subjects'].append('urn:deprecated')
    write_spec(path, document)
    with pytest.raises(ContractError):
        read_inputs(path)


def test_frozen_original_drift_cannot_be_hidden_by_an_unchanged_entity_graph(formal_inputs):
    make_formal(formal_inputs)
    entities, path = formal_inputs[-2:]
    source = entities/'sources/legacy/manifest.json'
    value = json.loads(source.read_bytes())
    value['source_states']['urn:candidate']['status'] = 'active'
    source.write_bytes(json_bytes(value))
    with pytest.raises(ContractError):
        read_inputs(path)


def test_self_declared_eligibility_is_rebuilt_from_originals(formal_inputs):
    document = make_formal(formal_inputs)
    entities, path = formal_inputs[-2:]
    manifest_path = entities/'manifest.json'
    manifest = json.loads(manifest_path.read_bytes())
    manifest['eligible_entity_iris'].append('urn:deprecated')
    manifest_path.write_bytes(json_bytes(manifest))
    item = next(item for item in document['sources'] if item['key'] == 'entities')
    item['entity_delivery']['manifest_sha256'] = digest(manifest_path.read_bytes())
    for artifact in item['artifacts']:
        if artifact['name'] == 'manifest.json':
            artifact['sha256'] = digest(manifest_path.read_bytes())
    item['selectable_subjects'].append('urn:deprecated')
    write_spec(path, document)
    with pytest.raises(ContractError):
        read_inputs(path)


def test_new_workspace_routing_cannot_change_old_delivery_selection(formal_inputs):
    root = formal_inputs[0]
    routing = root/'data/inputs/ccs/routing.json'
    value = json.loads(routing.read_bytes())
    value['items'][1]['action'] = 'concept'
    routing.write_bytes(json_bytes(value))
    document = make_formal(formal_inputs)
    ccs = next(item for item in document['sources'] if item['key'] == 'ccs-concepts')
    assert ccs['selectable_subjects'] == ['urn:ready']
    assert ccs['source_states']['urn:pending'] == {'routing_action': 'pending'}
    read_inputs(formal_inputs[-1])


def test_prepare_rejects_delivery_plan_drift_before_writing_input(formal_inputs):
    root = formal_inputs[0]
    plan = root/'output/vocabulary/ccs/partitioned-20260921-rdf/plan.json'
    value = json.loads(plan.read_bytes())
    value['items'][1]['action'] = 'concept'
    plan.write_bytes(json_bytes(value))
    with pytest.raises(ContractError, match='摘要'):
        make_formal(formal_inputs)
    assert not formal_inputs[-1].exists()


def test_reader_rejects_self_consistent_plan_from_a_different_delivery(formal_inputs):
    document = make_formal(formal_inputs)
    root, _, _, _, path = formal_inputs
    ccs = next(item for item in document['sources'] if item['key'] == 'ccs-concepts')
    new_plan = root/'newer-plan.json'
    value = json.loads(Path(ccs['routing']['path']).read_bytes())
    value['items'][1]['action'] = 'concept'
    new_plan.write_bytes(json_bytes(value))
    replacement = {**ccs['routing'], 'path': str(new_plan), 'sha256': digest(new_plan.read_bytes())}
    ccs['artifacts'] = [replacement if item['name'] == ccs['routing']['name'] else item
                        for item in ccs['artifacts']]
    ccs['routing'] = replacement
    ccs['source_states'] = {}
    ccs['selectable_subjects'].append('urn:pending')
    write_spec(path, document)
    with pytest.raises(ContractError, match='交付'):
        read_inputs(path)
