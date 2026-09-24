"""Protect identity, original evidence, permissive candidate use, and publication."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from rdflib import Literal, RDF, SKOS, URIRef
from rdflib.namespace import XSD

from kb_vocab_maintenance import entities
from kb_vocab_maintenance.diff import parse_turtle

PREFIX = '''@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xl: <http://www.w3.org/2008/05/skos-xl#> .
@prefix wd: <http://www.wikidata.org/entity/> .
'''


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


class EntityBuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.config = self.root / 'config.json'
        self.output = self.root / 'result'
        (self.root / 'decision.md').write_text('# 实体收录\n')
        self.document = {'schema_version': 1, 'policy': 'basic-fields-v1',
                         'authority': {'path': 'decision.md', 'sha256': sha256((self.root / 'decision.md').read_bytes()).hexdigest()},
                         'sources': []}

    def source(self, key, turtle, states, *, audit=False):
        folder = self.root / key
        folder.mkdir()
        files = {'entities.ttl': (PREFIX + turtle).encode(), 'original.txt': b'unchanged original\n'}
        if audit:
            files['entity-audit.json'] = encoded({'records': states})
            manifest = {}
        else:
            manifest = {'entity_iris': sorted(states), 'source_states': states}
        manifest['files'] = {name: sha256(raw).hexdigest() for name, raw in files.items()}
        for name, raw in files.items():
            (folder / name).write_bytes(raw)
        (folder / 'manifest.json').write_bytes(encoded(manifest))
        item = {'key': key, 'directory': key, 'manifest_sha256': sha256(encoded(manifest)).hexdigest(), 'entity_file': 'entities.ttl'}
        if audit:
            item['audit_file'] = 'entity-audit.json'
        self.document['sources'].append(item)
        self.config.write_bytes(encoded(self.document))
        return folder

    def build(self):
        return entities.build_entities(self.config, self.root, self.output)

    def test_candidate_and_unverified_records_are_usable_without_status_promotion(self):
        self.source('legacy', '<urn:e:one> a wd:Q7397; skos:prefLabel "Same"@en .',
                    {'urn:e:one': {'status': 'candidate', 'original_id': 'old-one', 'original_kind': 'software', 'source_pointer': '/entities/0'}})
        self.source('ccs', '<urn:e:two> a wd:Q7397; skos:prefLabel "Same"@en .',
                    [{'id': 'urn:e:two', 'kind': 'software', 'facts_verified': False}], audit=True)
        result = self.build()
        self.assertEqual(result['eligible_entity_iris'], ['urn:e:one', 'urn:e:two'])
        records = result['entities']
        self.assertEqual(records['urn:e:one']['sources'][0]['state']['status'], 'candidate')
        self.assertFalse(records['urn:e:two']['sources'][0]['state']['facts_verified'])
        self.assertEqual(result['same_name_candidates'][0]['entity_iris'], ['urn:e:one', 'urn:e:two'])
        self.assertEqual((self.output / 'sources/ccs/original.txt').read_bytes(), b'unchanged original\n')
        self.assertEqual(len(set(parse_turtle((self.output / 'entities.ttl').read_bytes()).subjects(RDF.type, URIRef('http://www.wikidata.org/entity/Q7397')))), 2)

    def test_missing_fields_and_deprecated_entities_are_retained_with_reasons(self):
        self.source('legacy', '<urn:e:missing> skos:scopeNote "No name" .\n<urn:e:old> a wd:Q7397; skos:prefLabel "Old"@en .',
                    {'urn:e:missing': {'status': 'candidate'}, 'urn:e:old': {'status': 'deprecated'}})
        result = self.build()
        self.assertEqual(result['eligible_entity_iris'], [])
        self.assertIn('category', result['entities']['urn:e:missing']['ineligible_reasons'])
        self.assertIn('preferred_name', result['entities']['urn:e:missing']['ineligible_reasons'])
        self.assertIn('deprecated', result['entities']['urn:e:old']['ineligible_reasons'])
        self.assertIn((URIRef('urn:e:old'), SKOS.prefLabel, Literal('Old', lang='en')), parse_turtle((self.output / 'entities.ttl').read_bytes()))

    def test_same_iri_with_different_description_or_label_closure_is_rejected(self):
        for change in ('skos:scopeNote "Different"@en;', 'xl:prefLabel <urn:label:shared>;'):
            with self.subTest(change=change):
                self.setUp()
                self.source('a', '<urn:e:one> a wd:Q7397; skos:prefLabel "One"@en .', {'urn:e:one': {'status': 'active'}})
                more = '<urn:label:shared> a xl:Label; xl:literalForm "One"@en .' if 'xl:' in change else ''
                self.source('b', '<urn:e:one> a wd:Q7397; ' + change + ' skos:prefLabel "One"@en .\n' + more, {'urn:e:one': {'status': 'candidate'}})
                with self.assertRaisesRegex(ValueError, 'IRI.*conflict|conflict.*IRI'):
                    self.build()
                self.assertFalse(self.output.exists())

    def test_xl_only_names_and_lexical_values_preserve_original_graph(self):
        turtle = '<urn:e:one> a wd:Q7397; xl:prefLabel <urn:l:one>; <urn:count> 01; <urn:detail> [ <urn:text> "原文"@zh ]; <urn:url> <https://example.org/a%2Fb> .\n<urn:l:one> a xl:Label; xl:literalForm "Name"@en-GB .'
        self.source('a', turtle, {'urn:e:one': {'status': 'candidate'}})
        result = self.build()
        graph = parse_turtle((self.output / 'entities.ttl').read_bytes())
        self.assertEqual(result['eligible_entity_iris'], ['urn:e:one'])
        self.assertIn((URIRef('urn:e:one'), URIRef('urn:count'), Literal('01', datatype=XSD.integer, normalize=False)), graph)
        self.assertFalse(list(graph.objects(URIRef('urn:e:one'), SKOS.prefLabel)))
        self.assertEqual(len(graph), len(parse_turtle(PREFIX + turtle)))

    def test_projection_and_independent_label_conflicts_are_rejected(self):
        self.source('a', '<urn:e:one> a wd:Q7397; skos:prefLabel "Wrong"@en; xl:prefLabel <urn:l:one> .\n<urn:l:one> a xl:Label; xl:literalForm "Right"@en .', {'urn:e:one': {'status': 'candidate'}})
        with self.assertRaisesRegex(ValueError, 'projection'):
            self.build()
        self.assertFalse(self.output.exists())

    def test_original_drift_and_corrupt_retry_never_overwrite_delivery(self):
        source = self.source('a', '<urn:e:one> a wd:Q7397; skos:prefLabel "One"@en .', {'urn:e:one': {'status': 'candidate'}})
        result = self.build()
        before = {p.relative_to(self.output): (p.read_bytes(), p.stat().st_mtime_ns) for p in self.output.rglob('*') if p.is_file()}
        self.assertEqual(self.build(), result)
        self.assertEqual(before, {p.relative_to(self.output): (p.read_bytes(), p.stat().st_mtime_ns) for p in self.output.rglob('*') if p.is_file()})
        (source / 'original.txt').write_text('changed original')
        with self.assertRaisesRegex(ValueError, 'hash|sha256'):
            self.build()
        (source / 'original.txt').write_bytes(b'unchanged original\n')
        (self.output / 'entities.ttl').write_text('corrupt')
        with self.assertRaisesRegex(ValueError, 'output|delivery'):
            self.build()
        self.assertEqual((self.output / 'entities.ttl').read_text(), 'corrupt')

    def test_incomplete_xl_blocks_users_even_with_another_valid_plain_name(self):
        self.source('a', '<urn:e:one> a wd:Q7397; skos:prefLabel "One"@en; xl:altLabel <urn:l:missing> .\n<urn:l:missing> a xl:Label .', {'urn:e:one': {'status': 'candidate'}})
        result = self.build()
        self.assertEqual(result['eligible_entity_iris'], [])
        self.assertIn('incomplete_xl_name', result['entities']['urn:e:one']['ineligible_reasons'])
        self.assertEqual(result['validation']['incomplete_xl_names'][0]['label'], 'urn:l:missing')
        graph = parse_turtle((self.output / 'entities.ttl').read_bytes())
        self.assertIn((URIRef('urn:l:missing'), RDF.type, entities.XL.Label), graph)

    def test_category_conflict_is_retained_without_becoming_usable(self):
        self.source('a', '<urn:e:one> a wd:Q7397, skos:Concept; skos:prefLabel "One"@en .', {'urn:e:one': {'status': 'candidate'}})
        result = self.build()
        self.assertEqual(result['eligible_entity_iris'], [])
        self.assertIn('category', result['entities']['urn:e:one']['ineligible_reasons'])

    def test_untagged_name_is_usable_with_language_diagnostic(self):
        self.source('a', '<urn:e:one> a wd:Q7397; skos:prefLabel "One" .', {'urn:e:one': {'status': 'candidate'}})
        result = self.build()
        self.assertEqual(result['eligible_entity_iris'], ['urn:e:one'])
        self.assertEqual(result['entities']['urn:e:one']['diagnostics'], ['preferred_name_without_language'])

    def test_shared_label_description_conflict_is_rejected(self):
        for key, description in [('a', 'First'), ('b', 'Different')]:
            self.source(key, '<urn:e:' + key + '> a wd:Q7397; xl:prefLabel <urn:l:shared> .\n<urn:l:shared> a xl:Label; xl:literalForm "Shared"@en; <urn:details> [ <urn:text> "' + description + '" ] .', {'urn:e:' + key: {'status': 'candidate'}})
        with self.assertRaisesRegex(ValueError, 'IRI conflict'):
            self.build()

    def test_identical_shared_iri_with_isomorphic_blank_closure_reuses_identity(self):
        for key, blank in [('a', 'one'), ('b', 'two')]:
            self.source(key, '<urn:e:one> a wd:Q7397; skos:prefLabel "One"@en; <urn:detail> _:' + blank + ' .\n_:' + blank + ' <urn:text> "same" .', {'urn:e:one': {'status': 'candidate'}})
        result = self.build()
        self.assertEqual(result['entity_iris'], ['urn:e:one'])
        graph = parse_turtle((self.output / 'entities.ttl').read_bytes())
        self.assertEqual(len(list(graph.objects(URIRef('urn:e:one'), URIRef('urn:detail')))), 1)

    def test_blank_xl_identity_diagnostics_are_stable_across_validation_and_retry(self):
        self.source('a', '<urn:e:one> a wd:Q7397; xl:prefLabel [ a xl:Label; xl:literalForm "One"@en ] .', {'urn:e:one': {'status': 'candidate'}})
        first = self.build()
        original = (self.output / 'manifest.json').read_bytes()
        self.assertEqual(first['eligible_entity_iris'], [])
        self.assertEqual(entities.validate_delivery(self.output), first)
        self.assertEqual(self.build(), first)
        self.assertEqual((self.output / 'manifest.json').read_bytes(), original)
        self.assertEqual(len(first['validation']['incomplete_xl_names']), 1)
        self.assertEqual(first['validation']['incomplete_xl_names'][0]['subjects'], ['urn:e:one'])

    def test_source_metadata_tampering_blocks_validation_and_current_switch(self):
        self.source('a', '<urn:e:one> a wd:Q7397; skos:prefLabel "One"@en .', {'urn:e:one': {'status': 'candidate'}})
        first = self.build()
        original = (self.output / 'manifest.json').read_bytes()
        changes = {'key': 'another', 'directory': 'elsewhere', 'entity_file': 'other.ttl',
                   'manifest_sha256': '0' * 64, 'public_id': 'file:///different/root/a/entities.ttl',
                   'audit_file': 'invented.json'}
        for field, value in changes.items():
            with self.subTest(field=field):
                altered = deepcopy(first)
                altered['sources']['a'][field] = value
                (self.output / 'manifest.json').write_bytes(encoded(altered))
                with self.assertRaises(ValueError):
                    entities.validate_delivery(self.output)
                with self.assertRaises(ValueError):
                    entities.set_current(self.output, self.root / 'current')
                self.assertFalse((self.root / 'current').is_symlink())
        altered = deepcopy(first)
        altered['sources']['unexpected'] = deepcopy(first['sources']['a'])
        (self.output / 'manifest.json').write_bytes(encoded(altered))
        with self.assertRaises(ValueError):
            entities.validate_delivery(self.output)
        (self.output / 'manifest.json').write_bytes(original)
        self.assertEqual(entities.validate_delivery(self.output), first)

    def test_drift_during_assembly_prevents_publication(self):
        source = self.source('a', '<urn:e:one> a wd:Q7397; skos:prefLabel "One"@en .', {'urn:e:one': {'status': 'candidate'}})
        original = entities.canonical_bytes
        def mutate(graph):
            (source / 'original.txt').write_text('changed while building')
            return original(graph)
        with patch.object(entities, 'canonical_bytes', side_effect=mutate):
            with self.assertRaisesRegex(ValueError, 'changed|hash|sha256'):
                self.build()
        self.assertFalse(self.output.exists())

    def test_current_switch_rejects_real_paths_and_damaged_delivery(self):
        self.source('a', '<urn:e:one> a wd:Q7397; skos:prefLabel "One"@en .', {'urn:e:one': {'status': 'candidate'}})
        self.build()
        current = self.root / 'current'
        current.mkdir()
        with self.assertRaises(ValueError):
            entities.set_current(self.output, current)
        current.rmdir()
        entities.set_current(self.output, current)
        self.assertEqual(current.resolve(), self.output)
        (self.output / 'sources/a/original.txt').write_text('corrupt')
        with self.assertRaises(ValueError):
            entities.set_current(self.output, self.root / 'other-current')
        self.assertFalse((self.root / 'other-current').exists())


if __name__ == '__main__':
    unittest.main()
