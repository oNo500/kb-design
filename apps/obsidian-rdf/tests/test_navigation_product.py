"""Navigation maintenance must respect authorship and application boundaries."""
import json

import pytest
import yaml

from kb_obsidian_rdf import product, storage
from kb_obsidian_rdf.common import digest, json_bytes
from kb_obsidian_rdf.layout import RESOURCES, TEMPLATES, VIEWS, VOCABULARY
from test_storage import delivery


INDEX_PATH = '00-indexes/index.md'


def initialize(vault):
    files = delivery()
    files.vault_files.update(product.initial_files())
    storage.initialize(vault, files)


@pytest.mark.parametrize('baseline_location', [INDEX_PATH, 'home.md', None])
def test_navigation_update_requires_its_own_matching_baseline(tmp_path, baseline_location):
    """An old homepage hash must not grant authority over the new index."""
    vault = tmp_path / 'vault'
    initialize(vault)
    index = vault / INDEX_PATH
    index.parent.mkdir(exist_ok=True)
    original = b'# Earlier navigation\n'
    index.write_bytes(original)
    baseline_path = storage.state_directory(vault) / 'product/baseline.json'
    baseline = json.loads(baseline_path.read_bytes())
    baseline['files'].pop(INDEX_PATH, None)
    if baseline_location:
        baseline['files'][baseline_location] = {'sha256': digest(original)}
    baseline_path.write_bytes(json_bytes(baseline))

    result = product.maintain(vault, apply=True, offline=True)
    row = next((row for row in result['changes'] if row['path'] == INDEX_PATH), None)

    assert row is not None, 'The navigation index must participate in maintenance'
    if baseline_location == INDEX_PATH:
        assert row['action'] == 'update'
        assert index.read_bytes() != original
        assert INDEX_PATH in result['written']
        assert json.loads(baseline_path.read_bytes())['files'][INDEX_PATH]['sha256'] == digest(index.read_bytes())
    else:
        assert row['action'] == 'preserve'
        assert index.read_bytes() == original
        assert INDEX_PATH not in result['written']
    assert 'home.md' not in result['write_set']


def test_maintenance_preserves_private_navigation_content_and_view_preferences(tmp_path):
    """Filling native settings must not adopt private indexes or alter data."""
    vault = tmp_path / 'vault'
    initialize(vault)
    index = vault / INDEX_PATH
    index.parent.mkdir(exist_ok=True)
    index.write_text('# 我的入口\n\n- [[personal|自己的阅读顺序]]\n')
    article = vault / RESOURCES / 'personal.md'
    article.write_text(f'# 我的内容\n\n[[{VOCABULARY}/concepts/one]]\n')
    view = vault / VIEWS / 'resources.base'
    base = yaml.safe_load(view.read_bytes())
    base['views'][0]['sort'] = [{'property': 'file.name', 'direction': 'ASC'}]
    base['views'][0]['columnSize'] = {'formula.title': 280}
    view.write_text(yaml.safe_dump(base, allow_unicode=True, sort_keys=False))
    template = vault / TEMPLATES / 'project.md'
    template.write_text('# {{title}}\n\nMy project template\n')
    config = vault / '.obsidian/app.json'
    config.write_text('{"attachmentFolderPath":"personal-files","alwaysUpdateLinks":false,"vimMode":true}')
    types = vault / '.obsidian/types.json'
    types.write_text('{"types":{"subject":"text","personal":"number"}}')
    protected = [index, article, view, template, config,
                 *list((vault / VOCABULARY).rglob('*.md')),
                 storage.state_directory(vault) / 'current.json']
    before = {path: path.read_bytes() for path in protected}

    result = product.maintain(vault, apply=True, offline=True)

    assert {path: path.read_bytes() for path in protected} == before
    assert result['written'] == ['.obsidian/types.json']
    updated_types = json.loads(types.read_bytes())['types']
    assert updated_types['subject'] == 'text'
    assert updated_types['personal'] == 'number'
    assert updated_types['created'] == 'date'
    row = next(row for row in result['changes'] if row['path'] == INDEX_PATH)
    assert row['action'] == 'preserve'
