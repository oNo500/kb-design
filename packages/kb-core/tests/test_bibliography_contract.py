import unittest
from kb_core.source_model import ReferenceUse, validate_reference_documents, decision_authorizes


class BibliographyContractTests(unittest.TestCase):
    def test_object_relationships_cannot_target_bibliography_records(self):
        import tempfile
        from pathlib import Path
        from test_source_v2_contract import write_fixture
        from kb_core.source_model import validate_source_documents
        with tempfile.TemporaryDirectory() as temporary:
            documents, decision = write_fixture(Path(temporary))
            for field, value in (("vendor", "standard"), ("creator", ["standard"]),
                                 ("replaced_by", "standard")):
                with self.subTest(field=field):
                    row = documents['entities']['entities'][0]
                    row[field] = value
                    issues = validate_source_documents(documents, {'source-approval': decision})
                    self.assertTrue(any(issue.field_path == field for issue in issues))
                    del row[field]

    def test_basis_resolves_only_bibliography(self):
        use = ReferenceUse('basis', 'data/vocab/topics.yaml', 'concepts:x', 'concepts[0].basis.scope[0]', {'reference': 'doc', 'locator': '1', 'checked': '2026-09-06'})
        self.assertEqual([], validate_reference_documents({'references': [{'id': 'doc', 'kind': 'standard'}]}, {}, [use], {}))
        self.assertTrue(validate_reference_documents({'entities': [{'id': 'doc', 'kind': 'standard'}]}, {}, [use], {}))

    def test_direct_url_requires_actual_ordinary_entity_field(self):
        value = {'url': 'https://example.org', 'locator': 'About', 'checked': '2026-09-06'}
        ordinary = {'entities': [{'id': 'tool', 'kind': 'software', 'basis': {'label': [value]}}]}
        good = ReferenceUse('basis', 'data/vocab/entities.yaml', 'entities:tool', 'entities[0].basis.label[0]', value)
        self.assertEqual([], validate_reference_documents({}, {}, [good], {}, ordinary_entities_document=ordinary))
        for bad in [good._replace(file='data/vocab/topics.yaml'), good._replace(field_path='entities[0].basis.subjects[0]'), good._replace(record='entities:missing')]:
            self.assertTrue(validate_reference_documents({}, {}, [bad], {}, ordinary_entities_document=ordinary))
        self.assertTrue(validate_reference_documents({}, {}, [good], {}))

    def test_migration_grant_cannot_widen_original_permission(self):
        before = {'identity': 'sources/use', 'field': 'entity', 'value': 'doc'}
        after = {'identity': 'sources/use', 'field': 'reference', 'value': 'doc'}
        docs = {'old': {'answers': [{'patches': [before]}]}, 'migration': {'level': 'L3', 'status': 'accepted', 'answers': [{'patches': [{'identity': '@control:bibliography', 'field': 'migration', 'value': {'base_commit': '688f2b262598a17a87230bf4298c25e12d6f216e', 'migrated_reference_ids': ['doc'], 'grants': [{'decision': 'old', 'before': before, 'after': after}]}}]}]}}
        self.assertTrue(decision_authorizes(docs, 'old', **after))
        after['value'] = 'another'
        self.assertFalse(decision_authorizes(docs, 'old', **after))

    def test_metadata_migration_does_not_authorize_a_state_change(self):
        from kb_core.governance.term_validation import _validate_state_chain
        history = [{'from_value': None, 'to_value': 'candidate', 'decision': 'old'}, {'from_value': 'candidate', 'to_value': 'candidate', 'decision': 'move', 'event': 'bibliography-reference-migration'}]
        issues = []
        _validate_state_chain(history, 'candidate', {'candidate', 'active'}, {(None, 'candidate')}, 'history', issues, migration_decisions={'move'})
        self.assertEqual([], issues)
        history[-1]['to_value'] = 'active'
        _validate_state_chain(history, 'active', {'candidate', 'active'}, {(None, 'candidate')}, 'history', issues, migration_decisions={'move'})
        self.assertTrue(issues)
