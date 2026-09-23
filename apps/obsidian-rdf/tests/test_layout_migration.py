"""Explicit legacy migration must preserve identities and survive interrupted moves."""
import importlib.util
import json
from pathlib import Path
from uuid import uuid4

import pytest

from kb_obsidian_rdf.common import ContractError, digest, json_bytes
from kb_obsidian_rdf import storage


def load_migration():
    path = Path(__file__).parents[1] / 'scripts/migrate-numbered-layout.py'
    spec = importlib.util.spec_from_file_location('numbered_migration', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def legacy(tmp_path):
    vault, root = tmp_path / 'vault', tmp_path / 'state'
    for name in ('inbox', 'projects', 'areas', 'resources', 'archives', 'vocabulary/concepts', 'views', 'templates', 'attachments', '.obsidian'):
        (vault / name).mkdir(parents=True, exist_ok=True)
    page = '---\ntitle: One\niri: https://example.org/vocabulary/one\n---\n[[vocabulary/concepts/one|One]]\n'
    (vault / 'vocabulary/concepts/one.md').write_text(page)
    article = '---\nidentifier: 92656834-ef9a-4220-ac46-37f0a5b5eada\nsubject: ["[[vocabulary/concepts/one|One]]"]\n---\n正文保持不变。\n'
    (vault / 'projects/article.md').write_text(article)
    (vault / 'home.md').write_text('`inbox/` [[views/article-list.base|文章列表]]\n')
    (vault / 'views/article-list.base').write_text('filters:\n  or:\n    - file.inFolder("projects")\nviews: []\n')
    (vault / '.obsidian/workspace.json').write_text(json.dumps({'file': 'projects/article.md', 'lastOpenFiles': ['vocabulary/concepts/one.md']}))
    state = storage.state_directory(vault, root)
    current = state / 'current'
    current.mkdir(parents=True)
    records = {'format_version': 1, 'records': [{'kind': 'concepts', 'use': 'current', 'identity': {'iri': 'https://example.org/vocabulary/one'}, 'path': 'vocabulary/concepts/one.md', 'label': 'One'}]}
    raw = {'records.json': json_bytes(records), 'projection.json': json_bytes({'format_version': 1, 'entries': [{'location': 'vocabulary/concepts/one.md', 'value': {'literal': 'vocabulary/original'}}]}), 'inputs/raw.ttl': b'<urn:one> <urn:predicate> "vocabulary/original" .\n'}
    for name, data in raw.items():
        path = current / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    manifest = {'format_version': 2, 'mode': 'preview', 'files': [{'path': 'vocabulary/concepts/one.md', 'sha256': digest(page.encode()), 'size': len(page.encode()), 'role': 'reference'}], 'state_files': [{'path': p, 'sha256': digest(b), 'size': len(b)} for p, b in raw.items()]}
    (current / 'manifest.json').write_bytes(json_bytes(manifest))
    vault_id = str(uuid4())
    (state / 'binding.json').write_bytes(json_bytes({'format_version': 1, 'tool': storage.TOOL, 'vault_id': vault_id, 'vault': str(vault), 'state_dir': str(state), 'mode': 'preview'}))
    (state / 'current.json').write_bytes(json_bytes({'vault_id': vault_id, 'target': str(vault), 'result': 'installed', 'manifest_sha256': digest(json_bytes(manifest))}))
    return vault, root, state, article


def test_layout_plan_preserves_source_then_applies_identity_and_links(tmp_path):
    migration = load_migration()
    vault, root, state, article = legacy(tmp_path)
    plan = migration.prepare(vault, root)
    assert (vault / 'projects/article.md').read_text() == article
    result = migration.apply(Path(plan['plan']), offline=True)
    assert result['status'] == 'installed'
    assert not (vault / 'projects').exists()
    assert (vault / '01-projects/article.md').read_text() == article.replace('[[vocabulary/', '[[05-vocabulary/')
    assert 'file.inFolder("01-projects")' in (vault / '06-views/article-list.base').read_text()
    snapshot = storage.inspect(vault, state_root=root)
    assert snapshot['records']['records'][0]['identity']['iri'] == 'https://example.org/vocabulary/one'
    assert snapshot['records']['records'][0]['path'] == '05-vocabulary/concepts/one.md'
    assert (state / 'current/inputs/raw.ttl').read_bytes() == b'<urn:one> <urn:predicate> "vocabulary/original" .\n'
    assert json.loads((state / 'current/projection.json').read_text())['entries'][0]['value']['literal'] == 'vocabulary/original'
    assert json.loads((vault / '.obsidian/workspace.json').read_text())['lastOpenFiles'] == ['05-vocabulary/concepts/one.md']
    assert (Path(result['backup']) / 'vault/projects/article.md').read_text() == article
    assert migration.apply(Path(plan['plan']), offline=True)['status'] == 'already-installed'


def test_layout_refuses_changed_note_or_destination_collision(tmp_path):
    migration = load_migration()
    vault, root, _, _ = legacy(tmp_path)
    (vault / '01-projects').mkdir()
    with pytest.raises(ContractError):
        migration.prepare(vault, root)
    (vault / '01-projects').rmdir()
    plan = migration.prepare(vault, root)
    (vault / 'projects/article.md').write_text('new user text')
    with pytest.raises(ContractError):
        migration.apply(Path(plan['plan']), offline=True)
    assert (vault / 'projects/article.md').read_text() == 'new user text'


@pytest.mark.parametrize('content', [
    '[One](../vocabulary/concepts/one.md)',
    '`[[vocabulary/concepts/one]]`',
    '```text\n[[vocabulary/concepts/one]]\n```',
])
def test_layout_refuses_unhandled_markdown_without_changing_the_note(tmp_path, content):
    migration = load_migration()
    vault, root, _, _ = legacy(tmp_path)
    note = vault / 'projects/article.md'
    note.write_text(content)
    with pytest.raises(ContractError):
        migration.prepare(vault, root)
    assert note.read_text() == content


def test_layout_refuses_new_empty_folder_after_preparation(tmp_path):
    migration = load_migration()
    vault, root, _, _ = legacy(tmp_path)
    plan = migration.prepare(vault, root)
    (vault / 'projects/new-empty-folder').mkdir()
    with pytest.raises(ContractError):
        migration.apply(Path(plan['plan']), offline=True)
    assert (vault / 'projects/new-empty-folder').is_dir()


def test_layout_detects_late_edit_after_first_move(tmp_path, monkeypatch):
    migration = load_migration()
    vault, root, _, _ = legacy(tmp_path)
    plan = migration.prepare(vault, root)
    original = migration.move
    def edited(source, target):
        original(source, target)
        if source == vault:
            (target / 'projects/article.md').write_text('late user edit')
    monkeypatch.setattr(migration, 'move', edited)
    with pytest.raises(ContractError):
        migration.apply(Path(plan['plan']), offline=True)
    assert (Path(plan['plan']).parent / 'backup/vault/projects/article.md').read_text() == 'late user edit'


@pytest.mark.parametrize('failure', [1, 2, 3, 4])
def test_layout_resumes_each_directory_move_without_repeating_edits(tmp_path, monkeypatch, failure):
    migration = load_migration()
    vault, root, state, article = legacy(tmp_path)
    plan = migration.prepare(vault, root)
    original = migration.move
    calls = 0
    def interrupted(source, target):
        nonlocal calls
        original(source, target)
        calls += 1
        if calls == failure:
            raise OSError('interrupted after rename')
    monkeypatch.setattr(migration, 'move', interrupted)
    with pytest.raises(OSError):
        migration.apply(Path(plan['plan']), offline=True)
    assert (state / 'recovery.json').exists()
    monkeypatch.setattr(migration, 'move', original)
    assert migration.apply(Path(plan['plan']), offline=True)['status'] == 'installed'
    assert (vault / '01-projects/article.md').read_text() == article.replace('[[vocabulary/', '[[05-vocabulary/')
    storage.inspect(vault, state_root=root)
