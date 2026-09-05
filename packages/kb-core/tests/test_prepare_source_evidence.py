"""Offline evidence preparation must preserve provenance and invalidate stale results."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml


class SourceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / 'build/evidence'
        self.write('data/vocab/topics.yaml', {'concepts': [{
            'id': 'computing', 'label': {'zh': '计算机科学技术'}, 'source': 'self',
            'basis': {'zh': {'level': 1, 'references': [{'source': 'gbt-13745', 'locator': '520'}]}},
            'match': [{'source': 'gbt-13745', 'id': '520', 'rel': 'exactMatch'}],
        }]})
        self.write('data/vocab/types.yaml', {'types': [{
            'id': 'explanation', 'scope': '理解原因',
            'match': [{'source': 'diataxis', 'id': 'explanation', 'rel': 'exactMatch'}],
        }]})
        self.write('data/vocab/entities.yaml', {'entities': [
            {'id': 'gbt-13745', 'version': '2009'}, {'id': 'diataxis', 'version': '2026-08'},
        ]})
        self.write('data/vocab/sources.yaml', {'sources': [
            {'id': key, 'entity': key, 'role': ['mapping']} for key in ['gbt-13745', 'diataxis']
        ]})
        self.write('data/audit/migrations/source-v1/match.yaml', {'rows': [
            {'identity': key, 'disposition': 'blocked_unread_material', 'blocks_cutover': True}
            for key in ['match-inventory.tsv:49', 'match-inventory.tsv:755']
        ]})
        self.write('data/audit/migrations/source-v1/basis.yaml', {'rows': [{
            'field_path': 'concepts[computing].basis.zh', 'old_value': 'gbt-13745',
            'disposition': 'not_migrated_missing_locator',
        }]})
        self.write('data/audit/migrations/source-v1/uses.yaml', {'roles': [
            {'use_id': key, 'new_role': 'mapping', 'new_status': 'proposed', 'decision': None}
            for key in ['gbt-13745', 'diataxis']
        ]})
        self.text('docs/references/gbt-13745.md', '# 分类清单\n\n转载清单，非原始 PDF。\n\n## 520 计算机科学技术\n\n条目说明。\n')
        self.text('docs/references/writing-guides.md', '# 阅读记录\n\n## 用途\n\n[Diátaxis Explanation](https://diataxis.fr/explanation/)：解释原因。\n')
        for path in ['current-stage-scope', 'source-validation-policy']:
            self.text(f'docs/decisions/{path}.md', '# 阶段规则\n\n不自动采纳。\n')

    def text(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def write(self, relative, data):
        self.text(relative, yaml.safe_dump(data, allow_unicode=True))

    def run_prepare(self):
        from kb_core.prepare_source_evidence import prepare
        return prepare(self.root, self.output)

    def report(self):
        return json.loads((self.output / 'evidence.json').read_text())

    def test_cli_produces_located_review_material_without_changing_inputs(self):
        """A usable command must retain exact source positions without upgrading reading notes."""
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = subprocess.run([sys.executable, '-m', 'kb_core.cli', 'prepare-source-evidence',
                                 '--root', str(self.root), '--output', str(self.output)],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        data = self.report()
        item = next(x for x in data['items'] if x['id'] == 'computing-gbt-520')
        snippet = item['materials'][0]['snippets'][0]
        self.assertEqual(5, snippet['line'])
        self.assertEqual('## 520 计算机科学技术', snippet['text'])
        self.assertEqual('transcription', item['materials'][0]['kind'])
        self.assertEqual('review_required', item['review_state'])
        self.assertTrue(item['missing_conditions'])
        for path, content in before.items():
            self.assertEqual(content, (self.root / path).read_bytes(), path)

    def test_unchanged_inputs_reuse_extraction_but_do_not_approve(self):
        """Repeated work should reuse derived excerpts while leaving the decision unresolved."""
        self.run_prepare()
        from unittest.mock import patch
        with patch('kb_core.prepare_source_evidence.extract_snippets', side_effect=AssertionError('unneeded extraction')):
            summary = self.run_prepare()
        self.assertEqual(2, summary['reused'])
        self.assertEqual([], summary['changed'])
        self.assertTrue(all(x['review_state'] == 'review_required' for x in self.report()['items']))

    def test_material_and_record_changes_invalidate_only_affected_item(self):
        """Changing evidence or the supported value must never retain its old cached result."""
        self.run_prepare()
        p = self.root / 'docs/references/gbt-13745.md'
        p.write_text(p.read_text().replace('520 计算机科学技术', '520 计算机科学技术 修订'))
        summary = self.run_prepare()
        self.assertEqual(['computing-gbt-520'], summary['changed'])
        self.assertEqual(1, summary['reused'])
        p = self.root / 'data/vocab/types.yaml'
        data = yaml.safe_load(p.read_text()); data['types'][0]['scope'] = '新的范围'
        self.write('data/vocab/types.yaml', data)
        summary = self.run_prepare()
        self.assertEqual(['explanation-diataxis'], summary['changed'])
        self.assertEqual('新的范围', self.report()['items'][1]['current']['record']['scope'])
        data['types'][0]['match'][0]['basis'] = [{'entity': 'diataxis', 'locator': 'Explanation'}]
        self.write('data/vocab/types.yaml', data)
        self.run_prepare()
        conditions = self.report()['items'][1]['missing_conditions']
        self.assertNotIn('adjacent_match_basis', conditions)
        self.assertIn('adjacent_basis_review', conditions)
        self.assertEqual('review_required', self.report()['items'][1]['review_state'])

    def test_missing_material_discards_old_excerpts_and_retains_gap(self):
        """A removed offline material must be reported as missing rather than served from cache."""
        self.run_prepare()
        (self.root / 'docs/references/writing-guides.md').unlink()
        self.run_prepare()
        item = self.report()['items'][1]
        self.assertEqual('missing', item['materials'][0]['availability'])
        self.assertEqual([], item['materials'][0]['snippets'])
        self.assertIn('offline_material_missing', item['missing_conditions'])

    def test_changed_ledger_or_policy_invalidates_cached_review(self):
        """Historical conclusions and decision boundaries are dependencies, not timeless cache data."""
        self.run_prepare()
        p = self.root / 'data/audit/migrations/source-v1/match.yaml'
        data = yaml.safe_load(p.read_text()); data['rows'][1]['disposition'] = 'changed_conclusion'
        self.write('data/audit/migrations/source-v1/match.yaml', data)
        self.assertEqual(['explanation-diataxis'], self.run_prepare()['changed'])
        self.text('docs/decisions/current-stage-scope.md', '# 新阶段\n新边界\n')
        self.assertEqual(2, len(self.run_prepare()['changed']))

    def test_rejects_output_over_formal_data_and_symlinked_build(self):
        """Output path choices must not turn a read-only preparation into source or vault overwrite."""
        from kb_core.prepare_source_evidence import prepare
        before = (self.root / 'data/vocab/topics.yaml').read_bytes()
        with self.assertRaises(ValueError):
            prepare(self.root, self.root / 'data/vocab')
        external = self.root / 'external'; external.mkdir()
        (self.root / 'build').symlink_to(external, target_is_directory=True)
        with self.assertRaises(ValueError):
            prepare(self.root, self.root / 'build/evidence')
        self.assertEqual(before, (self.root / 'data/vocab/topics.yaml').read_bytes())
        self.assertEqual([], list(external.iterdir()))


if __name__ == '__main__':
    unittest.main()
