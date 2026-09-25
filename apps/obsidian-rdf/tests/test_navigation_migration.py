"""Migration must retain link targets, authority, frozen input and recovery ownership."""
import json
from pathlib import Path

import pytest

from kb_obsidian_rdf import storage
from kb_obsidian_rdf.common import ContractError, digest, json_bytes
from test_layout_migration import legacy, load_migration


def numbered(tmp_path, mode='preview'):
    vault, root, state, article = legacy(tmp_path)
    roots = {'inbox': '00-inbox', 'projects': '01-projects', 'areas': '02-areas',
             'resources': '03-resources', 'archives': '04-archives', 'vocabulary': '05-vocabulary',
             'views': '06-views', 'templates': '07-templates', 'attachments': '08-attachments'}
    for old, new in roots.items():
        (vault / old).rename(vault / new)
    for path in [*vault.rglob('*.md'), *vault.rglob('*.base'), vault / '.obsidian/workspace.json']:
        text = path.read_text()
        for old, new in roots.items():
            text = text.replace(old + '/', new + '/').replace('"' + old + '"', '"' + new + '"')
        path.write_text(text)
    manifest = json.loads((state / 'current/manifest.json').read_text())
    manifest.update(format_version=3, mode=mode)
    records = json.loads((state / 'current/records.json').read_text())
    for row in records['records']:
        row['path'] = row['path'].replace('vocabulary/', '05-vocabulary/')
        row['mode'] = mode
    (state / 'current/records.json').write_bytes(json_bytes(records))
    for row in manifest['files']:
        row['path'] = row['path'].replace('vocabulary/', '05-vocabulary/')
        raw = (vault / row['path']).read_bytes()
        row.update(sha256=digest(raw), size=len(raw))
    if mode == 'formal':
        evidence = b'Explicit test-only permission.\n'
        authority = {'formal_reference': (tmp_path / 'permission.md').as_uri(), 'formal_evidence_sha256': digest(evidence)}
        sources = [{'key': 'test', 'authority': authority}]
        original = json_bytes({'mode': 'formal', 'sources': sources, 'auxiliary': []})
        manifest.update(sources=sources, auxiliary=[], input_sha256=digest(original))
        for raw, ext in [(original, 'json'), (evidence, 'md')]:
            path = 'inputs/' + digest(raw) + '.' + ext
            (state / 'current' / path).write_bytes(raw)
            manifest['state_files'].append({'path': path})
    for row in manifest['state_files']:
        raw = (state / 'current' / row['path']).read_bytes()
        row.update(sha256=digest(raw), size=len(raw))
    (state / 'current/manifest.json').write_bytes(json_bytes(manifest))
    receipt = json.loads((state / 'current.json').read_text())
    receipt.update(mode=mode, manifest_sha256=digest(json_bytes(manifest)))
    (state / 'current.json').write_bytes(json_bytes(receipt))
    binding = json.loads((state / 'binding.json').read_text())
    binding['mode'] = mode
    (state / 'binding.json').write_bytes(json_bytes(binding))
    return vault, root, state


@pytest.mark.parametrize('mode', ['preview', 'formal'])
def test_moved_index_keeps_links_state_and_authority(tmp_path, mode):
    migration = load_migration()
    vault, root, state = numbered(tmp_path, mode)
    index = vault / '02-areas/topic.md'
    index.write_text('---\nidentifier: 40854ed2-0710-48aa-9785-7352a9f67f06\n---\n'
                     '[[../01-projects/article|Article]] [[/05-vocabulary/concepts/one]]\n'
                     '[Article](../01-projects/article.md#Goal)\n'
                     '[Ref][one]\n\n[one]: ../05-vocabulary/concepts/one.md\n'
                     '`[[05-vocabulary/concepts/one]]`\n')
    (vault / '01-projects/article.md').write_text('[[02-areas/topic|Topic]] [[home]]\n[Topic](../02-areas/topic.md)\n')
    (vault / '.obsidian/templates.json').write_text('{"folder":"07-templates"}')
    (vault / '.obsidian/app.json').write_text('{"attachmentFolderPath":"08-attachments"}')
    baseline = {'format_version': 1, 'files': {'home.md': {'sha256': digest((vault / 'home.md').read_bytes())},
                                             '06-views/article-list.base': {'sha256': '1' * 64}}}
    (state / 'product').mkdir()
    (state / 'product/baseline.json').write_bytes(json_bytes(baseline))
    frozen = {p.name: p.read_bytes() for p in (state / 'current/inputs').iterdir()}
    original_binding = (state / 'binding.json').read_bytes()
    result = migration.prepare(vault, root, index_notes=['02-areas/topic.md'])
    assert index.exists()
    installed = migration.apply(Path(result['plan']), offline=True)
    assert installed['status'] == 'installed'
    assert (vault / '00-indexes/topic.md').read_text() == index_text()
    assert (vault / '10-projects/article.md').read_text() == '[[00-indexes/topic|Topic]] [[00-indexes/index]]\n[Topic](../00-indexes/topic.md)\n'
    assert json.loads((vault / '.obsidian/templates.json').read_text())['folder'] == '92-templates'
    assert json.loads((vault / '.obsidian/app.json').read_text())['attachmentFolderPath'] == '93-attachments'
    snapshot = storage.inspect(vault, state_root=root)
    assert snapshot['manifest']['mode'] == mode
    assert snapshot['records']['records'][0]['identity']['iri'] == 'https://example.org/vocabulary/one'
    assert (state / 'binding.json').read_bytes() == original_binding
    assert {p.name: p.read_bytes() for p in (state / 'current/inputs').iterdir()} == frozen
    after = json.loads((state / 'product/baseline.json').read_text())['files']
    assert after['00-indexes/index.md']['sha256'] == digest((vault / '00-indexes/index.md').read_bytes())
    assert after['91-views/article-list.base']['sha256'] == '1' * 64
    assert migration.apply(Path(result['plan']), offline=True)['status'] == 'already-installed'


def index_text():
    return ('---\nidentifier: 40854ed2-0710-48aa-9785-7352a9f67f06\n---\n'
            '[[../10-projects/article|Article]] [[/90-vocabulary/concepts/one]]\n'
            '[Article](../10-projects/article.md#Goal)\n'
            '[Ref][one]\n\n[one]: ../90-vocabulary/concepts/one.md\n'
            '`[[90-vocabulary/concepts/one]]`\n')


@pytest.mark.parametrize('changed', ['binding.json', 'product/baseline.json'])
def test_prepared_plan_refuses_authority_or_product_drift(tmp_path, changed):
    migration = load_migration()
    vault, root, state = numbered(tmp_path)
    (state / 'product').mkdir()
    (state / 'product/baseline.json').write_bytes(json_bytes({'format_version': 1, 'files': {}}))
    result = migration.prepare(vault, root)
    path = state / changed
    path.write_text(path.read_text() + '\n')
    with pytest.raises(ContractError):
        migration.apply(Path(result['plan']), offline=True)
    assert (vault / '01-projects/article.md').is_file()


@pytest.mark.parametrize('failure', [1, 2, 3, 4, 5, 6])
def test_resume_preserves_complete_product_backup(tmp_path, monkeypatch, failure):
    migration = load_migration()
    vault, root, state = numbered(tmp_path)
    (state / 'product').mkdir()
    before = json_bytes({'format_version': 1, 'files': {'home.md': {'sha256': digest((vault / 'home.md').read_bytes())}}})
    (state / 'product/baseline.json').write_bytes(before)
    result = migration.prepare(vault, root)
    original = migration.move
    count = 0
    def interrupted(source, target):
        nonlocal count
        original(source, target)
        count += 1
        if count == failure:
            raise OSError('interrupted after move')
    monkeypatch.setattr(migration, 'move', interrupted)
    with pytest.raises(OSError):
        migration.apply(Path(result['plan']), offline=True)
    monkeypatch.setattr(migration, 'move', original)
    done = migration.apply(Path(result['plan']), offline=True)
    assert (Path(done['backup']) / 'product/baseline.json').read_bytes() == before
    storage.inspect(vault, state_root=root)


def test_unchanged_product_can_migrate_without_false_completion(tmp_path):
    migration = load_migration()
    vault, root, state = numbered(tmp_path)
    (state / 'product').mkdir()
    before = json_bytes({'format_version': 1, 'files': {}})
    (state / 'product/baseline.json').write_bytes(before)
    result = migration.prepare(vault, root)
    done = migration.apply(Path(result['plan']), offline=True)
    assert (state / 'product/baseline.json').read_bytes() == before
    assert (Path(done['backup']) / 'product/baseline.json').read_bytes() == before


def test_resume_rejects_replaced_receipt_instead_of_overwriting_it(tmp_path, monkeypatch):
    migration = load_migration()
    vault, root, state = numbered(tmp_path)
    result = migration.prepare(vault, root)
    original = migration.move
    def interrupted(source, target):
        original(source, target)
        raise OSError('interrupted after move')
    monkeypatch.setattr(migration, 'move', interrupted)
    with pytest.raises(OSError):
        migration.apply(Path(result['plan']), offline=True)
    monkeypatch.setattr(migration, 'move', original)
    receipt = (state / 'current.json').read_bytes() + b'\n'
    (state / 'current.json').write_bytes(receipt)
    with pytest.raises(ContractError):
        migration.apply(Path(result['plan']), offline=True)
    assert (state / 'current.json').read_bytes() == receipt


def test_special_link_forms_keep_their_targets_and_other_vaults(tmp_path):
    migration = load_migration()
    vault, root, _ = numbered(tmp_path)
    (vault / '03-resources/a(b).md').write_text('target\n')
    note = vault / '02-areas/topic.md'
    absolute = str(vault / '01-projects/article.md')
    note.write_text('[Escaped](../03-resources/a\\(b\\).md#Part)\n'
                    '<a href="../01-projects/article.md#Goal">Article</a>\n'
                    f'[[{absolute}]]\n[Absolute]({absolute}#Goal)\n'
                    f'[File]({vault.as_uri()}/01-projects/article.md)\n'
                    '[Open](obsidian://open?vault=vault&file=02-areas%2Ftopic)\n'
                    '<obsidian://open?vault=old-vault&file=02-areas%2Ftopic>\n'
                    '<obsidian://open?vault=old-vault&file=02-areas/topic>\n'
                    '[Other](https://example.org/?file=02-areas/topic)\n'
                    '<obsidian://open?vault=vault&file=home>\n')
    plan = migration.prepare(vault, root, index_notes=['02-areas/topic.md'])
    migrated = (Path(plan['plan']).parent / 'candidate-vault/00-indexes/topic.md').read_text()
    assert '[Escaped](../30-resources/a%28b%29.md#Part)' in migrated
    assert '<a href="../10-projects/article.md#Goal">Article</a>' in migrated
    assert f'[[{vault}/10-projects/article.md]]' in migrated
    assert f'[Absolute]({vault}/10-projects/article.md#Goal)' in migrated
    assert f'[File]({vault.as_uri()}/10-projects/article.md)' in migrated
    assert '[Open](obsidian://open?vault=vault&file=00-indexes%2Ftopic)' in migrated
    assert '<obsidian://open?vault=old-vault&file=02-areas%2Ftopic>' in migrated
    assert '<obsidian://open?vault=old-vault&file=02-areas/topic>' in migrated
    assert '[Other](https://example.org/?file=02-areas/topic)' in migrated
    assert '<obsidian://open?vault=vault&file=00-indexes%2Findex>' in migrated


def test_cli_path_arguments_migrate_without_rewriting_url_query_parameters(tmp_path):
    migration = load_migration()
    vault, root, _ = numbered(tmp_path)
    (vault / '02-areas/topic.md').write_text('index\n')
    original = ('```sh\n'
                'obsidian vault=knowledge-base base:query path=06-views/projects.base format=json\n'
                'obsidian open file="02-areas/topic.md"\n'
                'folder=03-resources\n'
                'curl "https://example.org/?path=06-views/projects.base"\n'
                '```\n')
    note = vault / '01-projects/commands.md'
    note.write_text(original)
    plan = migration.prepare(vault, root, index_notes=['02-areas/topic.md'])
    candidate = (Path(plan['plan']).parent / 'candidate-vault/10-projects/commands.md').read_text()
    assert candidate == ('```sh\n'
                         'obsidian vault=knowledge-base base:query path=91-views/projects.base format=json\n'
                         'obsidian open file="00-indexes/topic.md"\n'
                         'folder=30-resources\n'
                         'curl "https://example.org/?path=06-views/projects.base"\n'
                         '```\n')
    assert note.read_text() == original
