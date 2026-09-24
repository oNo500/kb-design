"""Formal use changes selection, never source status or an existing binding."""
from copy import deepcopy
import json
from types import SimpleNamespace

import pytest
from rdflib import Graph, URIRef

from kb_obsidian_rdf import build, storage
from kb_obsidian_rdf.common import ContractError, Delivery, digest, json_bytes
from kb_obsidian_rdf.query import _available


@pytest.fixture(autouse=True)
def external_state(tmp_path, monkeypatch):
    monkeypatch.setenv('KB_OBSIDIAN_STATE_ROOT', str(tmp_path / 'state'))


def fixture_delivery(mode='preview', *, previous=None):
    evidence = '明确允许本实例使用；事实核验未执行。'.encode()
    authority = {'formal_reference': 'file:///fixture/adoption.md',
                 'formal_evidence_sha256': digest(evidence)}
    source = {'key': 'fixture', 'mode': mode, 'authority': authority}
    original = json_bytes({'mode': mode, 'sources': [source], 'auxiliary': []})
    state = {'records.json': json_bytes({'format_version': 1, 'records': []}),
             'projection.json': json_bytes({'format_version': 1, 'entries': []}),
             f'inputs/{digest(original)}.json': original,
             f'inputs/{digest(evidence)}.md': evidence}
    files = {'05-vocabulary/concepts/one.md': b'fixed page'}
    entries = lambda values: [{'path': p, 'size': len(raw), 'sha256': digest(raw)}
                              for p, raw in values.items()]
    manifest = {'format_version': 3, 'mode': mode, 'sources': [source], 'auxiliary': [],
                'input_sha256': digest(original), 'files': entries(files),
                'state_files': entries(state), 'previous_delivery': previous}
    state['manifest.json'] = json_bytes(manifest)
    return Delivery(files, state)


def source_fixture(verified=True):
    iri = 'urn:fixture:entity'
    graph = Graph().parse(data='<urn:fixture:entity> a <urn:fixture:Software> .', format='turtle')
    spec = {'key': 'entities', 'mode': 'formal', 'version': 'fixture',
            'scope': {'entity_class_iris': ['urn:fixture:Software']},
            'selectable_subjects': [iri], 'trial_subjects': [iri],
            'authority': {'formal_reference': 'file:///fixture/adoption.md'},
            'source_states': {iri: {'status': 'candidate', 'facts_verified': False}}}
    return SimpleNamespace(spec=spec, graph=graph, selected={URIRef(iri)}, raw_path='inputs/original.ttl',
                           entity_delivery={'eligible_entity_iris': [iri], 'entities': {
                               iri: {'sources': [{'key': 'original', 'state': {'status': 'candidate', 'facts_verified': False}}]}
                           }} if verified else None)


def test_verified_candidate_is_selectable_without_rewriting_source_status():
    source = source_fixture()
    original = deepcopy(source.spec['source_states'])
    _, records, *_ = build.build_records({'mode': 'formal', 'display': {'languages': ['en']}}, [source], [])
    assert _available(records[0])
    assert records[0]['source_state']['declared'] == [original['urn:fixture:entity']]
    assert source.spec['source_states'] == original
    assert records[0]['mode'] == 'formal'


def test_unknown_declared_state_is_not_granted_by_candidate_string():
    source = source_fixture(verified=False)
    _, records, *_ = build.build_records({'mode': 'formal', 'display': {'languages': ['en']}}, [source], [])
    assert not _available(records[0])


def test_extra_unverified_state_cannot_borrow_validated_entity_policy():
    source = source_fixture()
    source.spec['source_states']['urn:fixture:entity']['unverified_restriction'] = 'pending review'
    _, records, *_ = build.build_records({'mode': 'formal', 'display': {'languages': ['en']}}, [source], [])
    assert not _available(records[0])


def test_verified_entity_source_audit_is_preserved_without_spec_state_duplication():
    source = source_fixture()
    del source.spec['source_states']
    original = {'sources': [{'key': 'original', 'record': 'sources/original/entities.yaml#/entities/0',
                             'state': {'status': 'candidate', 'facts_verified': False}}],
                'eligible': True, 'diagnostics': [], 'ineligible_reasons': []}
    source.entity_delivery['entities'] = {'urn:fixture:entity': original}
    _, records, *_ = build.build_records({'mode': 'formal', 'display': {'languages': ['en']}}, [source], [])
    assert _available(records[0])
    assert records[0]['source_state']['entity_delivery'] == [original]


@pytest.mark.parametrize('old_mode,new_mode', [('preview', 'formal'), ('formal', 'preview')])
def test_refresh_cannot_switch_an_installed_mode(tmp_path, old_mode, new_mode):
    vault = tmp_path / 'vault'
    installed = storage.initialize(vault, fixture_delivery(old_mode))
    candidate = fixture_delivery(new_mode, previous={'sha256': installed['manifest_sha256']})
    with pytest.raises(ContractError, match='模式'):
        storage.refresh(vault, candidate, apply=True, offline=True)
    assert storage.inspect(vault)['manifest']['mode'] == old_mode


def test_formal_read_requires_the_frozen_authority_even_without_full_scan(tmp_path):
    vault = tmp_path / 'vault'
    storage.initialize(vault, fixture_delivery('formal'))
    state = storage.state_directory(vault)
    assert storage.read_state(vault)['manifest']['mode'] == 'formal'
    authority = next((state / 'current/inputs').glob('*.md'))
    authority.write_text('changed permission')
    with pytest.raises(ContractError, match='摘要|变化'):
        storage.read_state(vault)


def test_changing_only_binding_never_grants_formal_use(tmp_path):
    vault = tmp_path / 'vault'
    storage.initialize(vault, fixture_delivery())
    path = storage.state_directory(vault) / 'binding.json'
    binding = json.loads(path.read_bytes())
    binding['mode'] = 'formal'
    path.write_bytes(json_bytes(binding))
    with pytest.raises(ContractError, match='模式'):
        storage.read_state(vault)


def test_changing_manifest_mode_cannot_override_the_frozen_preview_input(tmp_path):
    fake = fixture_delivery()
    manifest = json.loads(fake.state_files['manifest.json'])
    manifest['mode'] = 'formal'
    fake.state_files['manifest.json'] = json_bytes(manifest)
    with pytest.raises(ContractError, match='正式|模式'):
        storage.initialize(tmp_path / 'vault', fake)


def test_recovery_rejects_a_changed_mode_before_moving_files(tmp_path, monkeypatch):
    vault = tmp_path / 'vault'
    with monkeypatch.context() as patch:
        patch.setattr(storage, '_receipt', lambda *a: (_ for _ in ()).throw(OSError('receipt interrupted')))
        with pytest.raises(ContractError, match='恢复'):
            storage.initialize(vault, fixture_delivery())
    state = storage.state_directory(vault)
    binding = json.loads((state / 'binding.json').read_bytes())
    binding['mode'] = 'formal'
    (state / 'binding.json').write_bytes(json_bytes(binding))
    with pytest.raises(ContractError, match='模式'):
        storage.recover(vault, offline=True)
    assert (state / 'recovery.json').exists()
    assert (vault / '05-vocabulary/concepts/one.md').read_bytes() == b'fixed page'


def test_history_never_imports_records_from_another_mode():
    old = fixture_delivery()
    previous = ('old-hash', old.state_files['manifest.json'], {}, [], {})
    with pytest.raises(ContractError, match='模式'):
        build.preserve_history({'mode': 'formal', 'previous_delivery': {'path': 'unused'}}, {}, {}, [], previous)
