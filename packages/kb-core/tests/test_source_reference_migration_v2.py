import copy
import tempfile
import unittest
from pathlib import Path

import yaml
from kb_core import apply_source_migration as migration


def decision_document(identifier, patches):
    return {'id': identifier, 'schema': 'urn:kb-design:data:decision', 'schema_version': 1,
            'status': 'accepted', 'date': '2026-09-05', 'level': 'L3', 'scope': 'Synthetic test fixture',
            'supersedes': [], 'answers': [{'question': 'Q20', 'resolution': 'replacement', 'patches': patches}]}


class ReferenceMigrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.original = {'version': {'id': 'old'}, 'concepts': [
            {'id': 'alpha', 'label': {'en': 'Alpha'}, 'status': 'active',
             'broader': ['parent'], 'basis': {'en': {'legacy': 'none'}},
             'source': 'self', 'match': []}]}
        self.after = {'assertions': {'source': {
            'disposition': 'project_assertion', 'original': 'self',
            'migration': 'data/audit/example.yaml#alpha'}}, 'match': []}
        self.inputs = {'schema_version': 2, 'records': {'topics/concepts/alpha': {
            'before': {'source': 'self', 'match': []}, 'after': self.after,
            'evidence': {'assertions': {'reviewed': True, 'decision': 'fixture'}}}}}
        path = self.root / 'docs/decisions/source-fixture.md'
        path.parent.mkdir(parents=True)
        path.write_text('---\n' + yaml.safe_dump(decision_document('fixture', [{'identity': 'topics/concepts/alpha',
                'field': 'assertions', 'value': self.after['assertions']}])) + '---\n')
        vocab = self.root / 'data/vocab'
        vocab.mkdir(parents=True)
        (vocab / 'entities.yaml').write_text('schema_version: 2\nentities: []\n')
        (vocab / 'sources.yaml').write_text('schema_version: 2\nsources: []\n')

    def test_explicit_local_migration_preserves_identity_and_other_fields(self):
        result = migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)
        expected = copy.deepcopy(self.original)
        expected['schema_version'] = 2
        expected['concepts'][0].pop('source')
        expected['concepts'][0].update(self.after)
        self.assertEqual(expected, result)
        self.assertEqual('self', self.original['concepts'][0]['source'])

    def test_unreviewed_or_missing_input_reports_target_and_never_guesses(self):
        for inputs in ({'schema_version': 2, 'records': {}}, copy.deepcopy(self.inputs)):
            if inputs['records']:
                inputs['records']['topics/concepts/alpha']['evidence']['assertions']['reviewed'] = False
            with self.assertRaisesRegex(ValueError, 'topics/concepts/alpha'):
                migration.migrate_reference_document(self.root, 'topics', self.original, inputs)

    def test_accepted_decision_cannot_be_reused_for_other_field_value(self):
        self.inputs['records']['topics/concepts/alpha']['after']['assertions']['source']['migration'] = 'other'
        with self.assertRaisesRegex(ValueError, 'topics/concepts/alpha.*assertions'):
            migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)

    def test_frozen_candidate_copy_excludes_user_and_environment_trees(self):
        for name in ('output/private.md', '.venv/token', 'build/stale', 'data/vocab/keep.yaml'):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('private' if name != 'data/vocab/keep.yaml' else 'keep: true')
        with tempfile.TemporaryDirectory() as target:
            output = Path(target) / 'candidate'
            migration.write_candidate_tree(self.root, {'rows': [{'identity': 'keep', 'old_file': 'data/vocab/keep.yaml',
                'field_path': 'keep', 'old_value': True, 'operation': 'keep'}]}, output)
            self.assertFalse((output / 'output').exists())
            self.assertFalse((output / '.venv').exists())
            self.assertFalse((output / 'build').exists())
            self.assertTrue((output / 'data/vocab/keep.yaml').exists())

    def test_external_references_are_explicit_and_deterministic(self):
        basis = [{'entity': 'publisher', 'locator': 'fixture section 1', 'checked': '2026-09-05'}]
        old = {'concepts': [{'id': 'alpha', 'source': 'register',
                            'match': [{'source': 'register', 'id': 'A', 'rel': 'exactMatch'}]}],
               'arrays': [{'id': 'group', 'superordinate': 'alpha', 'source': 'register'}]}
        source = {'registry': 'register', 'item': 'A', 'locator': 'fixture section 1', 'basis': basis}
        match = {'registry': 'register', 'item': 'A', 'rel': 'exactMatch', 'basis': basis}
        records = {
            'topics/concepts/alpha': {'before': copy.deepcopy(old['concepts'][0]),
                                      'after': {'source': source, 'match': [match]}},
            'topics/arrays/group': {'before': {'source': 'register'},
                                    'after': {'external_group': source}},
        }
        records['topics/concepts/alpha']['before'].pop('id')
        patches = []
        for identity, row in records.items():
            row['evidence'] = {}
            for field, value in row['after'].items():
                row['evidence'][field] = {'decision': 'external', 'reviewed': True}
                patches.append({'identity': identity, 'field': field, 'value': value})
        patches.append({'identity': 'sources/register', 'field': 'entity', 'value': 'publisher'})
        for role in ('structure', 'mapping'):
            patches.append({'identity': f'sources/register/roles/{role}', 'field': 'status', 'value': 'approved'})
        (self.root / 'docs/decisions/source-external.md').write_text('---\n' + yaml.safe_dump(decision_document('external', patches)) + '---\n')
        (self.root / 'data/vocab/entities.yaml').write_text(yaml.safe_dump({'schema_version': 2, 'entities': [
            {'id': 'publisher', 'kind': 'publication', 'tier': 'de-jure'}]}))
        (self.root / 'data/vocab/sources.yaml').write_text(yaml.safe_dump({'schema_version': 2, 'sources': [
            {'id': 'register', 'entity': 'publisher', 'roles': [
                {'role': role, 'status': 'approved', 'decision': 'external'} for role in ('structure', 'mapping')]}]}))
        inputs = {'schema_version': 2, 'records': records}
        first = migration.migrate_reference_document(self.root, 'topics', old, inputs)
        second = migration.migrate_reference_document(self.root, 'topics', old, inputs)
        self.assertEqual(yaml.safe_dump(first), yaml.safe_dump(second))
        self.assertEqual(source, first['concepts'][0]['source'])
        self.assertEqual([match], first['concepts'][0]['match'])
        self.assertEqual(source, first['arrays'][0]['external_group'])
        self.assertNotIn('source', first['arrays'][0])
        records['topics/concepts/alpha']['after']['source']['basis'] = []
        with self.assertRaisesRegex(ValueError, 'alpha.*source'):
            migration.migrate_reference_document(self.root, 'topics', old, inputs)

    def test_reference_candidate_write_isolated_and_blocked_before_directory_creation(self):
        source = self.root / 'data/vocab/topics.yaml'
        source.write_text(yaml.safe_dump(self.original))
        original_bytes = source.read_bytes()
        inputs = self.root / 'references.yaml'
        inputs.write_text(yaml.safe_dump(self.inputs))
        output = self.root / 'build/candidate/topics.yaml'
        migration.write_reference_candidate(self.root, 'topics', output, inputs)
        self.assertEqual(original_bytes, source.read_bytes())
        self.assertEqual(self.after['assertions'], yaml.safe_load(output.read_text())['concepts'][0]['assertions'])
        with self.assertRaisesRegex(ValueError, 'under root/build'):
            migration.write_reference_candidate(self.root, 'topics', source, inputs)
        blocked = self.root / 'build/blocked/topics.yaml'
        with self.assertRaisesRegex(ValueError, 'topics/concepts/alpha'):
            migration.write_reference_candidate(self.root, 'topics', blocked)
        self.assertFalse(blocked.parent.exists())

    def test_local_form_array_preserves_q16_object_and_never_creates_reference(self):
        from kb_core.source_model import collect_reference_uses
        old = {'arrays': [{'id': 'forms-presentation', 'superordinate': 'forms',
                           'members': ['diagram'], 'source': 'lom'}]}
        local = {'legacy_source_label': 'lom', 'state': 'isolated', 'decision': 'decision-source-0011'}
        identity = 'forms/arrays/forms-presentation'
        patches = [{'identity': identity, 'field': 'local_analysis', 'value': local}]
        decision = self.root / 'docs/decisions/source-local.md'
        decision.write_text('---\n' + yaml.safe_dump(decision_document('decision-source-0011', patches)) + '---\n')
        inputs = {'schema_version': 2, 'records': {identity: {'before': {'source': 'lom'},
            'after': {'local_analysis': local},
            'evidence': {'local_analysis': {'reviewed': True, 'decision': 'decision-source-0011'}}}}}
        result = migration.migrate_reference_document(self.root, 'forms', old, inputs)
        self.assertEqual({'id': 'forms-presentation', 'superordinate': 'forms', 'members': ['diagram'],
                          'local_analysis': local}, result['arrays'][0])
        self.assertEqual([], collect_reference_uses(Path('data/vocab/forms.yaml'), result))
        for wrong in ({**local, 'legacy_source_label': 'other'}, {**local, 'state': 'approved'},
                      {**local, 'locator': 'fake'}, {**local, 'decision': 'unknown'}):
            inputs['records'][identity]['after']['local_analysis'] = wrong
            patches[0]['value'] = wrong
            decision.write_text('---\n' + yaml.safe_dump(decision_document('decision-source-0011', patches)) + '---\n')
            with self.assertRaisesRegex(ValueError, 'local_analysis'):
                migration.migrate_reference_document(self.root, 'forms', old, inputs)

    def test_non_v1_reference_fields_cannot_be_deleted_by_empty_after(self):
        cases = [
            ('source', {'registry': 'register', 'item': 'A', 'locator': 'section', 'basis': []}),
            ('source', None), ('source', []), ('source', ''),
            ('match', [{'registry': 'register', 'item': 'A', 'rel': 'exactMatch', 'basis': []}]),
            ('match', 'invalid'), ('match', None), ('match', [{}]), ('match', []),
            ('assertions', {'source': {'original': 'self'}}),
            ('external_group', {'registry': 'register'}),
            ('local_analysis', {'legacy_source_label': 'lom', 'state': 'isolated', 'decision': 'decision-source-0011'}),
        ]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                original = {'concepts': [{'id': 'alpha', field: value}]}
                inputs = {'schema_version': 2, 'records': {'topics/concepts/alpha': {
                    'before': {field: value}, 'after': {}, 'evidence': {}}}}
                with self.assertRaisesRegex(ValueError, f'topics/concepts/alpha.{field}'):
                    migration.migrate_reference_document(self.root, 'topics', original, inputs)
                self.assertEqual(value, original['concepts'][0][field])

    def completion_fixture(self, isolate=False, correct=False):
        identity = 'topics/concepts/alpha'
        old = [{'source': 'register', 'id': item, 'rel': 'exactMatch'} for item in ('A', 'B')]
        new = [{'registry': 'register', 'item': item, 'rel': 'exactMatch',
                'basis': [{'entity': 'publisher', 'locator': 'section', 'checked': '2026-09-05'}]}
               for item in ('A', 'B')]
        self.original['concepts'][0]['match'] = old
        entry = self.inputs['records'][identity]
        entry['before']['match'] = copy.deepcopy(old)
        if isolate:
            new = new[1:]
        if correct:
            new[0]['item'] = 'corrected'
            new[0]['rel'] = 'closeMatch'
        entry['after']['match'] = new
        entry['evidence']['match'] = {'reviewed': True, 'decision': 'completion'}
        patches = [{'identity': identity, 'field': 'match', 'value': copy.deepcopy(new)}]
        if isolate:
            entry['evidence']['match']['isolated'] = [0]
            patches.append({'identity': identity, 'field': 'match[0].isolation', 'value': copy.deepcopy(old[0])})
        if correct:
            patches.append({'identity': identity, 'field': 'match[0].correction',
                            'value': {'before': copy.deepcopy(old[0]), 'after': copy.deepcopy(new[0])}})
        patches.extend([{'identity': 'sources/register', 'field': 'entity', 'value': 'publisher'},
                        {'identity': 'sources/register/roles/mapping', 'field': 'status', 'value': 'approved'}])
        (self.root / 'data/vocab/entities.yaml').write_text(yaml.safe_dump({'schema_version': 2,
            'entities': [{'id': 'publisher', 'kind': 'publication', 'tier': 'de-jure'}]}))
        (self.root / 'data/vocab/sources.yaml').write_text(yaml.safe_dump({'schema_version': 2,
            'sources': [{'id': 'register', 'entity': 'publisher', 'roles': [
                {'role': 'mapping', 'status': 'approved', 'decision': 'completion'}]}]}))
        self.write_completion(patches)
        return entry, patches

    def write_completion(self, patches, identifier='completion', status='accepted'):
        decision = decision_document(identifier, patches)
        decision['status'] = status
        (self.root / f'docs/decisions/source-{identifier}.md').write_text('---\n' + yaml.safe_dump(decision) + '---\n')

    def test_isolation_preserves_retained_mapping_and_requires_exact_same_decision(self):
        entry, patches = self.completion_fixture(isolate=True)
        result = migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)
        self.assertEqual(entry['after']['match'], result['concepts'][0]['match'])
        self.assertEqual(2, len(self.original['concepts'][0]['match']))
        self.write_completion([p for p in patches if p['field'] != 'match[0].isolation'])
        self.write_completion([p for p in patches if p['field'] == 'match[0].isolation'], 'borrowed')
        with self.assertRaisesRegex(ValueError, 'isolation'):
            migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)

    def test_isolation_rejects_forgery_bad_indices_and_unapproved_deletion(self):
        entry, patches = self.completion_fixture(isolate=True)
        for indices in ([True], [0, 0], [-1], [2], ['0'], None, []):
            with self.subTest(indices=indices):
                entry['evidence']['match']['isolated'] = indices
                with self.assertRaises(ValueError):
                    migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)
        entry['evidence']['match']['isolated'] = [0]
        patches[1]['value']['id'] = 'forged'
        self.write_completion(patches)
        with self.assertRaisesRegex(ValueError, 'isolation'):
            migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)

    def test_correction_requires_exact_before_after_permission(self):
        entry, patches = self.completion_fixture(correct=True)
        result = migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)
        self.assertEqual(entry['after']['match'], result['concepts'][0]['match'])
        patches[1]['value']['before']['id'] = 'stale'
        self.write_completion(patches)
        with self.assertRaisesRegex(ValueError, 'mapping identity'):
            migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)

    def test_scope_correction_preserves_language_history_and_refuses_stale_scope(self):
        entry = self.inputs['records']['topics/concepts/alpha']
        entry['before']['scope'] = None
        entry['after']['scope'] = 'Corrected scope'
        entry['evidence']['scope'] = {'reviewed': True, 'decision': 'completion'}
        self.write_completion([{'identity': 'topics/concepts/alpha', 'field': 'scope', 'value': 'Corrected scope'}])
        result = migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)
        self.assertEqual('Corrected scope', result['concepts'][0]['scope'])
        self.assertEqual(self.original['concepts'][0]['basis'], result['concepts'][0]['basis'])
        self.original['concepts'][0]['scope'] = 'Changed since approval'
        with self.assertRaisesRegex(ValueError, 'stale'):
            migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)

    def test_complete_isolation_retains_empty_match_and_needs_whole_field_grant(self):
        entry, patches = self.completion_fixture(isolate=True)
        entry['evidence']['match']['isolated'] = [0, 1]
        entry['after']['match'] = []
        patches[0]['value'] = []
        patches.append({'identity': 'topics/concepts/alpha', 'field': 'match[1].isolation',
                        'value': copy.deepcopy(entry['before']['match'][1])})
        self.write_completion(patches)
        result = migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)
        self.assertEqual([], result['concepts'][0]['match'])
        self.write_completion(patches[1:])
        with self.assertRaisesRegex(ValueError, 'missing reviewed field adoption'):
            migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)
        self.write_completion(patches)
        del entry['after']['match']
        with self.assertRaisesRegex(ValueError, 'mapping identity'):
            migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)

    def test_whole_field_grant_cannot_reorder_retained_matches_or_approve_invalid_reference(self):
        entry, patches = self.completion_fixture()
        entry['after']['match'].reverse()
        patches[0]['value'] = copy.deepcopy(entry['after']['match'])
        self.write_completion(patches)
        with self.assertRaisesRegex(ValueError, 'mapping identity'):
            migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)
        entry['after']['match'].reverse()
        entry['after']['match'][0]['basis'] = []
        patches[0]['value'] = copy.deepcopy(entry['after']['match'])
        self.write_completion(patches)
        with self.assertRaisesRegex(ValueError, 'match'):
            migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)

    def test_isolation_draft_and_borrowed_target_grants_are_not_authority(self):
        entry, patches = self.completion_fixture(isolate=True)
        self.write_completion(patches, status='draft')
        with self.assertRaisesRegex(ValueError, 'isolation'):
            migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)
        patches[1]['identity'] = 'topics/concepts/other'
        self.write_completion(patches)
        with self.assertRaisesRegex(ValueError, 'isolation'):
            migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)

    def test_scope_correction_requires_own_exact_field_adoption(self):
        entry = self.inputs['records']['topics/concepts/alpha']
        entry['before']['scope'] = None
        entry['after']['scope'] = 'Corrected scope'
        entry['evidence']['scope'] = {'reviewed': True, 'decision': 'completion'}
        self.write_completion([{'identity': 'topics/concepts/alpha', 'field': 'scope', 'value': 'Other scope'}])
        with self.assertRaisesRegex(ValueError, 'scope: missing reviewed field adoption'):
            migration.migrate_reference_document(self.root, 'topics', self.original, self.inputs)
