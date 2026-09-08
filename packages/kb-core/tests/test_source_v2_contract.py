import copy
import tempfile
import unittest
from pathlib import Path
import yaml
from kb_core.source_model import validate_repository, collect_reference_uses, validate_references


def write_fixture(root):
    directory = root / 'data/vocab'
    directory.mkdir(parents=True)
    ref = {'reference': 'standard', 'locator': 'publisher status', 'checked': '2026-09-05'}
    history = [{'date': '2026-09-05', 'action': 'migration', 'fields': [], 'decisions': ['source-approval']}]
    entity = {'id': 'standard', 'label': {'en': 'Standard'}, 'kind': 'standard',
              'status': 'candidate', 'source_status': 'current', 'version': '1',
              'tier': 'de-jure', 'added': '2026-08-01', 'subjects': ['topic'],
              'basis': {'source_status': [ref], 'version': [ref],
                        'subjects': [{'values': ['topic'], 'references': [ref]}]},
              'urls': [{'role': 'canonical', 'url': 'https://example.org', 'primary': True}],
              'review': {'checked': '2026-09-05', 'next_due': '2028-09-05',
                         'interval_months': 24, 'grace_days': 30, 'obligations': []},
              'watch': [], 'replaced_by': None, 'history': history}
    documents = {
        'entities': {'schema': 'urn:kb-design:data:entities', 'schema_version': 3,
                     'version': {}, 'entities': [{'id': 'tool', 'label': {'en': 'Tool'},
                         'kind': 'software', 'subjects': [], 'status': 'candidate', 'added': '2026-09-06'}]},
        'bibliography': {'schema': 'urn:kb-design:data:bibliography', 'schema_version': 3,
                         'version': {}, 'references': [entity]},
        'sources': {'schema': 'urn:kb-design:data:source-uses', 'schema_version': 3,
                    'version': {}, 'sources': [{'id': 'registry', 'reference': 'standard',
                    'roles': [{'role': name, 'status': 'approved', 'decision': 'source-approval'} for name in ('structure', 'mapping')],
                    'history': history}]},
        'topics': {'schema_version': 3, 'concepts': [{'id': 'topic'}]},
    }
    for name, document in documents.items():
        target = root / 'data/references/bibliography.yaml' if name == 'bibliography' else directory / f'{name}.yaml'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(yaml.safe_dump(document))
    decisions = root / 'docs/decisions'
    decisions.mkdir(parents=True)
    front = {'id': 'source-approval', 'schema': 'urn:kb-design:data:decision', 'schema_version': 1,
             'status': 'accepted', 'date': '2026-09-05', 'level': 'L3', 'scope': 'synthetic test',
             'supersedes': [], 'answers': [{'question': 'Q01', 'resolution': 'recommended',
             'patches': [{'identity': 'sources/registry/roles/structure', 'field': 'status', 'value': 'approved'}, {'identity': 'sources/registry', 'field': 'reference', 'value': 'standard'}]}]}
    front['answers'][0]['patches'].append({'identity': 'sources/registry/roles/mapping', 'field': 'status', 'value': 'approved'})
    front['answers'][0]['patches'].extend([{'identity': 'references/standard', 'field': field, 'value': entity[field]} for field in ('version', 'source_status')])
    (decisions / 'source-approval.md').write_text('---\n' + yaml.safe_dump(front) + '---\n')
    return documents, front


class SourceV2ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.docs, self.decision = write_fixture(self.root)

    def save(self, name):
        target = self.root / 'data/references/bibliography.yaml' if name == 'bibliography' else self.root / f'data/vocab/{name}.yaml'
        target.write_text(yaml.safe_dump(self.docs[name]))

    def issues(self):
        return validate_repository(self.root)

    def test_invalid_collection_shapes_report_issues_instead_of_crashing(self):
        for name, key, value in [('entities', 'entities', None), ('sources', 'sources', [None]), ('sources', 'sources', [{'id': 'x', 'roles': 3}])]:
            with self.subTest(name=name, value=value):
                original = copy.deepcopy(self.docs[name])
                self.docs[name][key] = value
                self.save(name)
                try:
                    self.assertTrue(self.issues())
                finally:
                    self.docs[name] = original
                    self.save(name)

    def test_captured_documents_enforce_full_semantics_without_disk_reads(self):
        from kb_core import source_model
        documents = copy.deepcopy(self.docs)
        decisions = {'source-approval': self.decision}
        self.assertEqual([], source_model.validate_source_documents(documents, decisions))
        cases = [('source_status', 'withdrawn', 'source_status'),
                 ('review', {**documents['bibliography']['references'][0]['review'], 'next_due': '2029-09-05'}, 'review.next_due'),
                 ('watch', [{'locator': 'https://example.org', 'signals': ['version'],
                             'cadence_months': {'availability': 1, 'redirect': 1, 'content': 6}}], 'watch')]
        for field, value, path in cases:
            with self.subTest(field=field):
                changed = copy.deepcopy(documents)
                changed['bibliography']['references'][0][field] = value
                self.assertIn(path, {issue.field_path for issue in source_model.validate_source_documents(changed, decisions)})
        # Missing obligations are harmless until a real reference exists.
        changed = copy.deepcopy(documents)
        changed['bibliography']['references'][0]['review']['obligations'] = ['missing']
        self.assertIn('review.obligations', {issue.field_path for issue in source_model.validate_source_documents(changed, decisions)})

    def test_present_vocabulary_requires_v2_root(self):
        from kb_core.source_model import validate_source_documents
        documents = copy.deepcopy(self.docs)
        documents['forms'] = {'forms': [], 'arrays': []}
        self.assertTrue(any(i.file == 'data/vocab/forms.yaml' and i.field_path == 'schema_version'
                            for i in validate_source_documents(documents, {'source-approval': self.decision})))

    def test_q16_isolation_requires_exact_policy_and_forms_array_position(self):
        from kb_core.source_model import validate_source_documents, _front_matter
        policy = _front_matter(Path(__file__).resolve().parents[3] / 'docs/decisions/source-migration-policy.md')
        decisions = {'source-approval': self.decision, policy['id']: policy}
        isolated = {'legacy_source_label': 'lom', 'state': 'isolated', 'decision': policy['id']}
        documents = copy.deepcopy(self.docs)
        documents['forms'] = {'schema_version': 3, 'forms': [], 'arrays': [
            {'id': 'format', 'superordinate': 'original-parent', 'members': ['original-member'], 'local_analysis': isolated}]}
        self.assertEqual([], validate_source_documents(documents, decisions))
        self.assertEqual([], collect_reference_uses(Path('forms.yaml'), documents['forms']))
        for mutation in ('wrong-decision', 'unknown-key', 'wrong-position'):
            changed = copy.deepcopy(documents)
            local = changed['forms']['arrays'][0]['local_analysis']
            if mutation == 'wrong-decision': local['decision'] = 'source-approval'
            elif mutation == 'unknown-key': local['source'] = 'lom'
            else: changed['topics']['concepts'][0]['local_analysis'] = changed['forms']['arrays'][0].pop('local_analysis')
            self.assertTrue(any(i.field_path == 'local_analysis' for i in validate_source_documents(changed, decisions)), mutation)

    def test_q16_migration_preserves_parent_and_members(self):
        from kb_core.source_model import _front_matter
        policy_path = Path(__file__).resolve().parents[3] / 'docs/decisions/source-migration-policy.md'
        policy = _front_matter(policy_path)
        (self.root / 'docs/decisions/source-migration-policy.md').write_text(policy_path.read_text())
        with tempfile.TemporaryDirectory() as temporary:
            previous = Path(temporary)
            write_fixture(previous)
            old = {'schema_version': 3, 'forms': [{'id': 'member', 'arrays': ['group']}],
                   'arrays': [{'id': 'group', 'superordinate': 'old-parent', 'source': 'lom'}]}
            (previous / 'data/vocab/forms.yaml').write_text(yaml.safe_dump(old))
            current = copy.deepcopy(old)
            array = current['arrays'][0]
            array.pop('source')
            array['superordinate'] = 'changed-parent'
            array['local_analysis'] = {'legacy_source_label': 'lom', 'state': 'isolated', 'decision': policy['id']}
            current['forms'][0]['arrays'] = []
            (self.root / 'data/vocab/forms.yaml').write_text(yaml.safe_dump(current))
            self.assertTrue(any(i.file == 'data/vocab/forms.yaml' and i.field_path == 'local_analysis'
                                for i in validate_repository(self.root, previous)))

    def test_structure_qualification_preserves_existing_scope(self):
        from kb_core.source_model import validate_source_documents
        decisions = {'source-approval': self.decision}
        for mutation in ('missing-mapping', 'vendor', 'archival', 'unversioned-de-facto'):
            changed = copy.deepcopy(self.docs)
            entity = changed['bibliography']['references'][0]
            if mutation == 'missing-mapping':
                changed['sources']['sources'][0]['roles'] = [role for role in changed['sources']['sources'][0]['roles'] if role['role'] != 'mapping']
            else:
                entity['tier'] = 'de-facto' if mutation == 'unversioned-de-facto' else mutation
                interval = {'vendor': 6, 'archival': None, 'unversioned-de-facto': 12}[mutation]
                entity['review'].update(interval_months=interval, next_due={6:'2027-03-05',12:'2027-09-05',None:None}[interval])
                if mutation == 'unversioned-de-facto': entity['version'] = None
            self.assertTrue(any(issue.file == 'data/vocab/sources.yaml' for issue in validate_source_documents(changed, decisions)), mutation)

    def test_archival_preserves_only_proposed_discovery_without_use_qualification(self):
        from kb_core.source_model import validate_source_documents, validate_reference_documents, ReferenceUse
        documents = copy.deepcopy(self.docs)
        decisions = {'source-approval': copy.deepcopy(self.decision)}
        entity = documents['bibliography']['references'][0]
        entity['tier'] = 'archival'
        entity['review'].update(interval_months=None, next_due=None)
        use = documents['sources']['sources'][0]
        discovery = {'role': 'discovery', 'status': 'proposed', 'decision': None}
        use['roles'] = [discovery]
        self.assertEqual([], validate_source_documents(documents, decisions))

        for role in ('mapping', 'structure', 'group', 'discovery'):
            with self.subTest(role=role):
                changed = copy.deepcopy(documents)
                status = 'approved' if role == 'discovery' else 'proposed'
                changed['sources']['sources'][0]['roles'] = [
                    {'role': role, 'status': status,
                     'decision': 'source-approval' if status == 'approved' else None}]
                decisions['source-approval']['answers'][0]['patches'].append(
                    {'identity': f'sources/registry/roles/{role}', 'field': 'status', 'value': status})
                self.assertTrue(any(issue.code == 'SOURCE_SCHEMA_INVALID' and
                                    issue.file == 'data/vocab/sources.yaml'
                                    for issue in validate_source_documents(changed, decisions)))
                changed['sources']['sources'][0]['roles'].append(discovery)
                self.assertTrue(any(issue.code == 'SOURCE_SCHEMA_INVALID' and
                                    issue.file == 'data/vocab/sources.yaml'
                                    for issue in validate_source_documents(changed, decisions)))

        basis = [{'reference': 'standard', 'locator': 'section 1', 'checked': '2026-09-05'}]
        for kind in ('source', 'match', 'external_group'):
            with self.subTest(reference=kind):
                value = {'registry': 'registry', 'item': '1', 'basis': basis}
                value.update({'rel': 'exactMatch'} if kind == 'match' else {'locator': 'section 1'})
                issues = validate_reference_documents(documents['bibliography'], documents['sources'],
                    [ReferenceUse(kind, 'data/vocab/topics.yaml', 'topic', kind, value)], decisions)
                expected = 'SOURCE_EXTERNAL_GROUP_ROLE_NOT_APPROVED' if kind == 'external_group' else 'SOURCE_ROLE_NOT_APPROVED'
                self.assertIn(expected, {issue.code for issue in issues})

    def test_group_requires_its_own_authorized_mapping(self):
        from kb_core.source_model import validate_source_documents
        for mutation in ('missing', 'borrowed'):
            with self.subTest(mutation=mutation):
                documents = copy.deepcopy(self.docs)
                decisions = {'source-approval': copy.deepcopy(self.decision)}
                use = documents['sources']['sources'][0]
                use['roles'] = [{'role': 'group', 'status': 'approved', 'decision': 'source-approval'}]
                patches = decisions['source-approval']['answers'][0]['patches']
                patches.append({'identity': 'sources/registry/roles/group', 'field': 'status', 'value': 'approved'})
                if mutation == 'borrowed':
                    use['roles'].append({'role': 'mapping', 'status': 'approved', 'decision': 'source-approval'})
                    for patch in patches:
                        if patch['identity'] == 'sources/registry/roles/mapping': patch['identity'] = 'sources/other/roles/mapping'
                self.assertTrue(any(issue.code == 'SOURCE_ROLE_NOT_APPROVED' and issue.field_path == 'roles'
                                    for issue in validate_source_documents(documents, decisions)))

    def test_unverified_external_status_can_be_absent_but_not_defaulted(self):
        from kb_core.source_model import validate_source_documents
        documents = copy.deepcopy(self.docs)
        entity = documents['bibliography']['references'][0]
        entity.pop('source_status')
        entity['basis'].pop('source_status')
        entity['version'] = None
        entity['basis'].pop('version')
        before = copy.deepcopy(documents)
        self.assertEqual([], validate_source_documents(documents, {'source-approval': self.decision}))
        self.assertEqual(before, documents)
        for invalid in (None, 'unknown', 'not-applicable'):
            with self.subTest(invalid=invalid):
                entity['source_status'] = invalid
                self.assertTrue(validate_source_documents(documents, {'source-approval': self.decision}))
        entity['source_status'] = 'current'
        self.assertTrue(any(issue.field_path == 'basis.source_status'
                            for issue in validate_source_documents(documents, {'source-approval': self.decision})))
        entity.pop('source_status')
        entity.pop('version')
        self.assertTrue(validate_source_documents(documents, {'source-approval': self.decision}))

    def test_grouped_subject_evidence_is_valid_and_indexed(self):
        self.assertEqual([], self.issues())
        refs = collect_reference_uses(Path('bibliography.yaml'), self.docs['bibliography'])
        self.assertTrue(any(r.field_path.endswith('subjects[0].references[0]') for r in refs))

    def test_role_approval_cannot_be_borrowed_from_another_registry(self):
        self.decision['answers'][0]['patches'][0]['identity'] = 'sources/other/roles/structure'
        (self.root / 'docs/decisions/source-approval.md').write_text('---\n' + yaml.safe_dump(self.decision) + '---\n')
        self.assertTrue(any(i.code == 'SOURCE_ROLE_DECISION_MISSING' for i in self.issues()))

    def test_registry_retargeting_cannot_reuse_role_approval(self):
        other = copy.deepcopy(self.docs['bibliography']['references'][0])
        other['id'] = 'other'
        self.docs['bibliography']['references'].append(other)
        self.docs['sources']['sources'][0]['reference'] = 'other'
        self.save('bibliography'); self.save('sources')
        self.assertTrue(any(i.code == 'SOURCE_ROLE_DECISION_MISSING' for i in self.issues()))

    def test_all_subject_values_need_scoped_evidence(self):
        self.docs['bibliography']['references'][0]['subjects'].append('uncovered')
        self.save('bibliography')
        self.assertTrue(any('subjects' in i.field_path and 'cover' in i.message for i in self.issues()))

    def test_old_strings_and_wrong_shapes_cannot_disappear(self):
        for data in ({'source': 'self'}, {'match': [{'source': 'registry', 'item': 'x'}]},
                     {'basis': {'subjects': 'self'}}, {'external_group': []}):
            with self.subTest(data=data):
                refs = collect_reference_uses(Path('topics.yaml'), {'concepts': [{'id': 'x', **data}]})
                self.assertTrue(validate_references(self.root, refs))

    def test_label_and_id_change_cannot_hide_identity_loss(self):
        with tempfile.TemporaryDirectory() as old:
            previous = Path(old)
            write_fixture(previous)
            self.docs['bibliography']['references'][0]['id'] = 'changed'
            self.docs['bibliography']['references'][0]['label'] = {'en': 'Changed'}
            self.save('bibliography')
            self.assertIn('SOURCE_STABLE_ID_CHANGED', {i.code for i in validate_repository(self.root, previous)})

    def test_project_assertion_is_not_an_external_reference(self):
        data = {'entities': [{'id': 'project', 'assertions': {'subjects': [
            {'values': ['topic'], 'disposition': 'project_assertion', 'original': 'self', 'migration': 'audit#project'}]}}]}
        self.assertEqual([], collect_reference_uses(Path('entities.yaml'), data))

    def test_duplicate_primary_and_missing_external_evidence_fail(self):
        entity = self.docs['bibliography']['references'][0]
        entity['urls'].append({'role': 'landing', 'url': 'https://example.net', 'primary': True})
        del entity['basis']['source_status']
        self.save('bibliography')
        paths = {i.field_path for i in self.issues()}
        self.assertIn('urls', paths)
        self.assertIn('basis.source_status', paths)
