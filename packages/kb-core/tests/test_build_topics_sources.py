"""The generator must preserve existing semantics and fail closed without adoptions."""
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

import yaml
from kb_core.build_topics import _assemble_topics, topic_output_path
from kb_core.apply_source_migration import REFERENCE_FIELDS, load_reference_inputs
from kb_core.source_model import _load_accepted_decisions, decision_authorizes

ROOT = pathlib.Path(__file__).resolve().parents[3]


class BuildTopicsSourceTests(unittest.TestCase):
    def test_assembly_preserves_existing_identity_and_non_reference_fields(self):
        frozen = yaml.safe_load((ROOT / 'data/vocab/topics.yaml').read_text())
        assembled = _assemble_topics(ROOT)
        inputs = load_reference_inputs(ROOT)['records']
        decisions = _load_accepted_decisions(ROOT / 'docs/decisions')
        for section in ('arrays', 'concepts'):
            self.assertEqual([row['id'] for row in frozen[section]],
                             [row['id'] for row in assembled[section]])
            for current, original in zip(frozen[section], assembled[section]):
                with self.subTest(section=section, identity=original['id']):
                    protected_current = {key: value for key, value in current.items()
                                         if key not in REFERENCE_FIELDS}
                    protected_original = {key: value for key, value in original.items()
                                          if key not in REFERENCE_FIELDS}
                    identity = f"topics/{section}/{original['id']}"
                    entry = inputs.get(identity, {})
                    if 'scope' in entry.get('after', {}):
                        self.assertEqual(original.get('scope'), entry['before']['scope'])
                        evidence = entry['evidence']['scope']
                        self.assertIs(evidence.get('reviewed'), True)
                        self.assertTrue(decision_authorizes(decisions, evidence.get('decision'),
                                                            identity, 'scope', entry['after']['scope']))
                        protected_original['scope'] = entry['after']['scope']
                    self.assertEqual(protected_original, protected_current)
        self.assertEqual(frozen['version'], assembled['version'])

    def test_output_cannot_target_formal_data_or_source_files(self):
        for relative in ('data/vocab/entities.yaml', 'packages/kb-core/src/kb_core/build_topics.py'):
            target = ROOT / relative
            before = target.read_bytes()
            result = subprocess.run([sys.executable, '-m', 'kb_core.build_topics', '--output', str(target)],
                                    env={**os.environ, 'KB_DESIGN_ROOT': str(ROOT)}, text=True, capture_output=True)
            self.assertNotEqual(0, result.returncode)
            self.assertIn('output must', result.stderr)
            self.assertEqual(before, target.read_bytes())

    def test_candidate_path_rejects_symlinks_and_existing_external_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary)
            root = base / 'repo'
            (root / 'data/vocab').mkdir(parents=True)
            outside = base / 'external'
            outside.mkdir()
            (root / 'build').symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'symlink'):
                topic_output_path(root, root / 'build/topics.yaml')
            existing = outside / 'existing.yaml'
            existing.write_text('user data')
            with self.assertRaisesRegex(ValueError, 'absent'):
                topic_output_path(root, existing)
            self.assertEqual('user data', existing.read_text())
            self.assertEqual((outside / 'new.yaml').resolve(), topic_output_path(root, outside / 'new.yaml'))

    def test_missing_field_adoptions_block_generation_without_writing_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = pathlib.Path(temporary) / 'candidate/topics.yaml'
            references = pathlib.Path(temporary) / 'empty-references.json'
            references.write_text('{"schema_version": 2, "records": {}}\n')
            completed = subprocess.run(
                [sys.executable, '-m', 'kb_core.build_topics', '--output', str(output),
                 '--references', str(references)],
                env={**os.environ, 'KB_DESIGN_ROOT': str(ROOT)},
                text=True, capture_output=True)
            self.assertNotEqual(0, completed.returncode)
            self.assertIn('topics/concepts/computing.match', completed.stderr)
            self.assertIn('topics/arrays/', completed.stderr)
            self.assertFalse(output.parent.exists())


if __name__ == '__main__':
    unittest.main()
