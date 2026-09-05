"""Protect evidence type and adoption authority at the label boundary."""
from __future__ import annotations

import copy
import unittest

from kb_core import label_basis as basis


class LabelBasisTests(unittest.TestCase):
    def setUp(self):
        self.record = {
            'id': 'networking', 'source': 'cs2023', 'status': 'active',
            'label': {'en': 'Networking', 'zh': '网络'}, 'scope': 'Network concepts',
            'match': [{'source': 'cs2023', 'id': 'NC', 'rel': 'exactMatch'}],
        }
        self.sources = {'cs2023', 'wikidata', 'gbt-13745', 'lom'}
        self.model = {'level': 5, 'model': {
            'name': 'GPT-6', 'date': '2026-09-05',
            'rationale': '按既有概念的模型知识译名',
            'approval': 'design/decisions/structured-label-basis.md#批次授权',
        }}
        self.adoptions = {'topics/networking/zh': {
            'accept': True, 'label': '网络', 'basis': copy.deepcopy(self.model),
            'original': {'en': 'Networking', 'scope': 'Network concepts'},
        }}

    def validate(self, value, label='网络', decisions=None):
        return basis.validate_basis(value, label, self.record, 'zh', self.sources, decisions)

    def test_legacy_normalization_preserves_source_locator_and_record(self):
        before = copy.deepcopy(self.record)
        self.assertEqual(basis.normalize_basis('source', self.record, 'en'), {
            'level': 2, 'references': [{'source': 'cs2023', 'locator': 'NC'}]})
        self.assertEqual(basis.normalize_basis('wikidata:Q395', self.record, 'en'), {
            'level': 3, 'references': [{'source': 'wikidata', 'locator': 'Q395'}]})
        self.assertEqual(self.record, before)
        self.assertEqual(self.validate('source'), [])

    def test_history_none_is_ungraded_and_never_adopted_as_level_six(self):
        normalized = basis.normalize_basis('none', self.record, 'zh')
        self.assertEqual(normalized, {'legacy': 'none'})
        self.assertEqual(self.validate(normalized, label=None), [])
        self.assertTrue(self.validate(normalized))
        self.assertTrue(self.validate({'level': 6}, label=None))
        self.assertEqual(self.validate({'level': 6, 'reason': '概念含义尚未解决'}, label=None), [])
        self.assertTrue(self.validate({'level': 6, 'reason': '尚未解决'}))
        self.assertIn('未重新分级', str(basis.basis_rows(normalized)))

    def test_unknown_history_does_not_acquire_an_invented_grade(self):
        self.assertEqual(basis.normalize_basis('old-book:12', self.record, 'zh'),
                         {'legacy': 'old-book:12'})
        self.assertTrue(self.validate('old-book:12'))
        self.sources.add('old-book')
        self.assertEqual(self.validate('old-book:12'), [])
        self.assertTrue(self.validate('self'))
        self.assertTrue(self.validate('model'))

    def test_external_evidence_requires_actual_registered_distinct_sources(self):
        valid = {'level': 4, 'references': [
            {'source': 'cs2023', 'locator': 'NC'},
            {'source': 'wikidata', 'locator': 'Q123'}]}
        self.assertEqual(self.validate(valid), [])
        duplicate = copy.deepcopy(valid)
        duplicate['references'][1] = {'source': 'cs2023', 'locator': 'SF'}
        self.assertTrue(self.validate(duplicate))
        for source in ('model', 'none', 'self', 'unknown'):
            bad = copy.deepcopy(valid)
            bad['references'][1]['source'] = source
            with self.subTest(source=source):
                self.assertTrue(self.validate(bad))
        for invalid in ({'level': True, 'references': valid['references']},
                        {'level': 2, 'references': []},
                        {'level': 2, 'references': [{'source': 'cs2023', 'locator': ' '}]},
                        {'level': 3, 'references': 'wikidata:Q123'}):
            with self.subTest(invalid=invalid):
                self.assertTrue(self.validate(invalid))
        self.assertTrue(self.validate(valid, label='  '))

    def test_model_metadata_cannot_be_external_evidence(self):
        self.assertEqual(self.validate(self.model, decisions=self.adoptions), [])
        for extra in ({'references': []}, {'q': 'Q123'}, {'external_verified': True}):
            bad = dict(self.model, **extra)
            with self.subTest(extra=extra):
                self.assertTrue(self.validate(bad))
        for key, value in (('date', '2026-02-30'), ('date', '2026-9-5'),
                           ('name', []), ('rationale', ' '), ('approval', 'other.md')):
            bad = copy.deepcopy(self.model)
            bad['model'][key] = value
            with self.subTest(key=key, value=value):
                self.assertTrue(self.validate(bad))
        self.assertTrue(self.validate({'level': 5, 'model': 'GPT-6'}))
        self.assertTrue(self.validate(self.model, label=''))

    def test_known_source_cannot_be_relabelled_as_a_higher_grade(self):
        for level, source, locator in ((1, 'wikidata', 'Q395'), (1, 'cs2023', 'NC'),
                                       (3, 'cs2023', 'NC'), (3, 'wikidata', 'not-a-q-id')):
            with self.subTest(level=level, source=source):
                self.assertTrue(self.validate({'level': level, 'references': [
                    {'source': source, 'locator': locator}]}))

    def test_structural_validation_can_precede_source_registry_loading(self):
        evidence = {'level': 2, 'references': [{'source': 'future-source', 'locator': '12'}]}
        self.assertEqual(basis.validate_basis(evidence, '网络', self.record, 'zh', None), [])
        self.assertTrue(self.validate(evidence))
        malformed = {'level': 2, 'references': [{'source': 'model', 'locator': '12'}]}
        self.assertTrue(basis.validate_basis(malformed, '网络', self.record, 'zh', None))

    def test_future_batch_links_still_require_matching_adoption(self):
        future = copy.deepcopy(self.model)
        future['model']['approval'] = 'design/decisions/next-label-batch-2027.md#译名授权'
        self.assertEqual(self.validate(future), [])
        self.assertTrue(self.validate(future, decisions=self.adoptions))
        adopted = copy.deepcopy(self.adoptions)
        adopted['topics/networking/zh']['basis'] = copy.deepcopy(future)
        self.assertEqual(self.validate(future, decisions=adopted), [])
        for invalid in ('/design/decisions/batch.md#授权',
                        'design/decisions/../batch.md#授权',
                        'design/decisions/batch.md',
                        'design/decisions/batch.md#',
                        'https://example.org/design/decisions/batch.md#授权',
                        'other/batch.md#授权',
                        'design/decisions/Bad_Name.md#授权',
                        'design/decisions/batch.md#bad anchor'):
            bad = copy.deepcopy(future)
            bad['model']['approval'] = invalid
            with self.subTest(approval=invalid):
                self.assertTrue(self.validate(bad))

    def test_model_adoption_requires_matching_snapshot_and_explicit_acceptance(self):
        self.assertTrue(self.validate(self.model, decisions={}))
        for key, value in (('accept', 1), ('accept', False), ('label', '另一个译名'),
                           ('basis', {'level': 5, 'model': {}}),
                           ('original', {'en': 'Changed', 'scope': 'Network concepts'}),
                           ('original', {'en': 'Networking', 'scope': 'Changed'}),
                           ('original', {'en': 'Networking'})):
            decisions = copy.deepcopy(self.adoptions)
            decisions['topics/networking/zh'][key] = value
            with self.subTest(key=key, value=value):
                self.assertTrue(self.validate(self.model, decisions=decisions))
        before = copy.deepcopy((self.model, self.record, self.adoptions))
        self.assertEqual(self.validate(self.model, decisions=self.adoptions), [])
        self.assertEqual((self.model, self.record, self.adoptions), before)
        forms = {'forms/networking/zh': self.adoptions['topics/networking/zh']}
        self.assertEqual(basis.validate_basis(self.model, '网络', self.record, 'zh',
                                            self.sources, forms, collection='forms'), [])

    def test_display_and_reference_extraction_do_not_turn_model_into_source(self):
        rows = basis.basis_rows(self.model)
        self.assertIn('外部用法未核实', str(rows))
        self.assertIn('GPT-6', str(rows))
        self.assertIn('2026-09-05', str(rows))
        self.assertEqual(basis.source_references(self.model), [])
        forged = dict(self.model, references=[{'source': 'wikidata', 'locator': 'Q123'}])
        self.assertEqual(basis.source_references(forged), [])
        for marker in ('none', 'self', 'model', {'legacy': 'none'}):
            self.assertEqual(basis.source_references(marker, self.record), [])
        self.assertEqual(basis.source_references('source', self.record),
                         [{'source': 'cs2023', 'locator': 'NC'}])
        self.assertEqual(basis.source_references('wikidata:Q395'),
                         [{'source': 'wikidata', 'locator': 'Q395'}])


if __name__ == '__main__':
    unittest.main()
