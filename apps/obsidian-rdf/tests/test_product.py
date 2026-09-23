"""Maintenance must preserve authors' preferences and survive partial writes."""
import json
from pathlib import Path

import pytest

from kb_obsidian_rdf import storage
from kb_obsidian_rdf.common import ContractError, digest
from test_storage import delivery


def tree(root):
    return {path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob('*') if path.is_file()}


def test_maintenance_preserves_preferences_and_custom_files_and_reports_all_changes(tmp_path):
    from kb_obsidian_rdf import product
    vault = tmp_path / 'vault'
    storage.initialize(vault, delivery())
    config = vault / '.obsidian'
    config.mkdir()
    (config / 'app.json').write_text('{"attachmentFolderPath":"my-files","alwaysUpdateLinks":false,"vimMode":true}')
    (config / 'types.json').write_text('{"types":{"subject":"text","personal":"number"}}')
    (config / 'templates.json').write_text('{"folder":"my-templates"}')
    (vault / '06-views/drafts.base').write_text('views: [{type: table, name: Personal}]\n')
    (vault / '07-templates/article.md').write_text('My writing template\n')
    (vault / 'home.md').write_text('# My homepage\n')
    before = tree(vault)
    preview = product.maintain(vault)
    assert tree(vault) == before
    assert preview['status'] == 'preview'
    with pytest.raises(ContractError, match='offline'):
        product.maintain(vault, apply=True)
    result = product.maintain(vault, apply=True, offline=True)
    for name in ('.obsidian/app.json', '.obsidian/templates.json', '06-views/drafts.base',
                 '07-templates/article.md', 'home.md'):
        assert (vault / name).read_bytes() == before[name]
    types = json.loads((config / 'types.json').read_text())['types']
    assert types['subject'] == 'text' and types['personal'] == 'number'
    assert types['created'] == 'date'
    assert result['written'] == result['write_set']
    changes = {row['path']: row for row in result['changes']}
    assert changes['home.md']['action'] == 'preserve'
    assert changes['.obsidian/types.json']['preserved'][0]['property'] == 'types.subject'
    assert Path(changes['.obsidian/types.json']['backup']).read_bytes() == before['.obsidian/types.json']
    assert Path(changes['home.md']['candidate']).is_file()
    report = json.loads(Path(result['report_path']).read_text())
    assert report == result
    assert '+  "types"' in changes['.obsidian/types.json']['diff']
    after = tree(vault)
    assert product.maintain(vault, apply=True, offline=True)['written'] == []
    assert tree(vault) == after


def test_maintenance_resumes_from_actual_partial_writes_and_retains_backups(tmp_path, monkeypatch):
    from kb_obsidian_rdf import product
    vault = tmp_path / 'vault'
    storage.initialize(vault, delivery())
    (vault / '.obsidian').mkdir()
    app = vault / '.obsidian/app.json'
    app.write_text('{"attachmentFolderPath":"personal"}')
    original = app.read_bytes()
    write = product._write

    def fail(path, data, **kwargs):
        if path.parent == vault / '06-views':
            raise OSError('interrupted write')
        return write(path, data, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(product, '_write', fail)
        with pytest.raises(ContractError, match='report') as failure:
            product.maintain(vault, apply=True, offline=True)
    reports = list((storage.state_directory(vault) / 'product/operations').glob('*/report.json'))
    failed = json.loads(reports[0].read_text())
    assert failed['status'] == 'failed'
    assert '.obsidian/app.json' in failed['written']
    assert failed['changes'][0]['actual_sha256'] == digest(app.read_bytes())
    assert str(reports[0]) in str(failure.value)
    backup = next(row['backup'] for row in failed['changes'] if row['path'] == '.obsidian/app.json')
    assert Path(backup).read_bytes() == original
    app.write_text('{"attachmentFolderPath":"changed-after-failure","alwaysUpdateLinks":false}')
    repaired = product.maintain(vault, apply=True, offline=True)
    assert '.obsidian/app.json' not in repaired['written']
    assert json.loads(app.read_text())['alwaysUpdateLinks'] is False
    assert Path(backup).read_bytes() == original
    assert (vault / '06-views/drafts.base').is_file()


def test_home_update_requires_matching_external_baseline(tmp_path):
    from kb_obsidian_rdf import product
    vault = tmp_path / 'vault'
    storage.initialize(vault, delivery())
    baseline = storage.state_directory(vault) / 'product/baseline.json'
    assert baseline.is_file()
    first = product.maintain(vault, apply=True, offline=True)
    assert 'home.md' in first['written']
    home = vault / 'home.md'
    assert '[[06-views/drafts.base|' in home.read_text()
    home.write_text(home.read_text() + '\nMy additional content\n')
    raw = home.read_bytes()
    result = product.maintain(vault, apply=True, offline=True)
    assert 'home.md' not in result['written']
    assert home.read_bytes() == raw


def test_refresh_does_not_replace_config_or_product_baseline(tmp_path):
    from kb_obsidian_rdf import product
    vault = tmp_path / 'vault'
    old = delivery()
    old.vault_files.update(product.initial_files())
    storage.initialize(vault, old)
    config = vault / '.obsidian/app.json'
    config.write_text('{"alwaysUpdateLinks": false}')
    baseline = storage.state_directory(vault) / 'product/baseline.json'
    before = {name: raw for name, raw in tree(vault).items() if not name.startswith('05-vocabulary/')}
    baseline_bytes = baseline.read_bytes()
    candidate = delivery('after')
    candidate.vault_files.update(product.initial_files())
    result = storage.refresh(vault, candidate, apply=True, offline=True)
    assert {name: raw for name, raw in tree(vault).items() if not name.startswith('05-vocabulary/')} == before
    assert baseline.read_bytes() == baseline_bytes
    assert all(name.startswith('05-vocabulary/') for name in result['receipt']['written'])


def test_semantically_equal_view_is_not_reformatted_or_adopted(tmp_path):
    from kb_obsidian_rdf import product
    import yaml
    vault = tmp_path / 'vault'
    storage.initialize(vault, delivery())
    view = vault / '06-views/recently-modified.base'
    content = yaml.safe_load(product.initial_files()['06-views/recently-modified.base'])
    view.write_text('# Hand formatted\n' + yaml.safe_dump(content, sort_keys=True))
    before = view.read_bytes()
    result = product.maintain(vault, apply=True, offline=True)
    assert view.read_bytes() == before
    change = next(row for row in result['changes'] if row['path'] == '06-views/recently-modified.base')
    assert change['action'] == 'equivalent'
    assert str(view.relative_to(vault)) not in result['written']


def test_interrupted_new_file_write_does_not_publish_partial_target(tmp_path, monkeypatch):
    from kb_obsidian_rdf import product
    vault = tmp_path / 'vault'
    storage.initialize(vault, delivery())
    target = vault / '.obsidian/app.json'
    write = product._write

    def interrupt_write(path, data, **kwargs):
        if path.parent == target.parent:
            write(path, data[:7], **kwargs)
            raise OSError('disk full during new file write')
        return write(path, data, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(product, '_write', interrupt_write)
        with pytest.raises(ContractError, match='disk full'):
            product.maintain(vault, apply=True, offline=True)
    assert not target.exists()
    assert not list(target.parent.iterdir())
    reports = list((storage.state_directory(vault) / 'product/operations').glob('*/report.json'))
    failed = json.loads(reports[0].read_text())
    assert failed['status'] == 'failed'
    assert '.obsidian/app.json' not in failed['written']
    retried = product.maintain(vault, apply=True, offline=True)
    assert '.obsidian/app.json' in retried['written']
    assert json.loads(target.read_text())['alwaysUpdateLinks'] is True
