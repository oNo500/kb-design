import copy
import unittest

from kb_core.label_basis import validate_basis
from kb_core.label_adoptions import apply_adoptions
from kb_core.source_model import _record_evidence_issues


class LabelScopeContextTests(unittest.TestCase):
    def setUp(self):
        self.basis = {'level': 5, 'model': {
            'name': 'model', 'date': '2026-09-05', 'rationale': 'existing industry usage',
            'approval': 'design/decisions/structured-label-basis.md#批次授权'}}
        self.record = {'id': 'topic', 'label': {'en': 'Topic', 'zh': '主题'},
                       'scope': 'corrected scope', 'basis': {'zh': self.basis}}
        self.adoptions = {'topics/topic/zh': {'accept': True, 'label': '主题',
                         'basis': copy.deepcopy(self.basis),
                         'original': {'en': 'Topic', 'scope': None}}}
        self.patches = [
            {'identity': 'topics/concepts/topic', 'field': 'scope', 'value': 'corrected scope'},
            {'identity': 'topics/concepts/topic', 'field': 'scope.correction',
             'value': {'before': None, 'after': 'corrected scope'}}]
        self.accepted = {'source-completion': {'answers': [{'patches': self.patches}]}}

    def errors(self, accepted):
        return validate_basis(self.basis, self.record['label']['zh'], self.record, 'zh', {},
                              self.adoptions, accepted_decisions=accepted)

    def test_exact_correction_preserves_snapshot_and_reaches_source_validation(self):
        before = copy.deepcopy(self.adoptions)
        self.assertEqual(self.errors(self.accepted), [])
        self.assertEqual(_record_evidence_issues('data/vocab/topics.yaml',
                         {'concepts': [self.record]}, {}, self.adoptions, self.accepted), [])
        self.assertEqual(self.adoptions, before)
        with self.assertRaisesRegex(ValueError, 'stale original name or scope'):
            apply_adoptions([copy.deepcopy(self.record)], 'topics', self.adoptions, {})

    def test_unauthorized_scope_changes_remain_invalid(self):
        variants = [None, {}, {'source-completion': {'answers': [{'patches': self.patches[:1]}]}}]
        for changed in ('identity', 'before', 'after'):
            grant = copy.deepcopy(self.accepted)
            patch = grant['source-completion']['answers'][0]['patches'][1]
            if changed == 'identity':
                patch['identity'] = 'topics/concepts/another-topic'
            else:
                patch['value'][changed] = 'forged'
            variants.append(grant)
        variants.append({'first': {'answers': [{'patches': self.patches[:1]}]},
                         'second': {'answers': [{'patches': self.patches[1:]}]}})
        for accepted in variants:
            with self.subTest(accepted=accepted):
                self.assertTrue(any('scope' in error for error in self.errors(accepted)))

    def test_scope_correction_does_not_expand_label_adoption(self):
        for field in ('en', 'zh'):
            with self.subTest(field=field):
                record = copy.deepcopy(self.record)
                record['label'][field] = 'forged'
                errors = validate_basis(self.basis, record['label']['zh'], record, 'zh', {},
                                        self.adoptions, accepted_decisions=self.accepted)
                self.assertTrue(errors)
        altered = copy.deepcopy(self.basis)
        altered['model']['rationale'] = 'forged'
        self.assertTrue(validate_basis(altered, '主题', self.record, 'zh', {}, self.adoptions,
                                       accepted_decisions=self.accepted))
