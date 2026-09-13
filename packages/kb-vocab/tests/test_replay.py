"""Archived inputs must survive relocation without changing RDF identities."""
import hashlib
import importlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from rdflib import RDF, SKOS, URIRef
from kb_vocab.review_catalog import read_catalog


class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.original = self.root / 'original'
        self.original.mkdir()
        (self.original / 'source.ttl').write_text(
            '@prefix s: <http://www.w3.org/2004/02/skos/core#> . '
            '<#id> a s:Concept ; s:prefLabel "A"@en .')
        self.catalog_raw = b'{"sources": [{"name": "example", "file": "source.ttl"}]}'
        (self.original / 'sources.json').write_bytes(self.catalog_raw)
        self.sources = read_catalog(self.original / 'sources.json')
        self.config = {'catalog': 'sources.json', 'shapes': 'elsewhere.ttl',
                       'sources': {'example': self.sources['example']['sha256']},
                       'vocabulary': {'uri': 'urn:scheme'}, 'languages': ['en'],
                       'domains': [{'id': 'topic'}]}
        self.raw = json.dumps(self.config, indent=4).encode()
        self.path = self.original / 'config.json'
        self.path.write_bytes(self.raw)

    def api(self):
        try:
            return importlib.import_module('kb_vocab.replay')
        except ModuleNotFoundError:
            self.fail('archived replay helpers are not implemented')

    def archive(self):
        api = self.api()
        archive = self.root / 'archive'
        api.write_replay_inputs(archive, self.raw, self.catalog_raw, b'# shapes\n',
                                self.sources, self.raw)
        catalog = json.loads((archive / 'inputs/catalog.json').read_bytes())
        for entry in catalog['sources']:
            target = archive / 'inputs' / entry['file']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.sources[entry['name']]['path'], target)
        return archive

    def test_relocated_archive_replays_after_original_inputs_are_removed(self):
        archive = self.archive()
        expected = URIRef((self.original / 'source.ttl').resolve().as_uri() + '#id')
        relocated = self.root / 'other-place' / 'archive'
        shutil.copytree(archive, relocated)
        shutil.rmtree(archive)
        shutil.rmtree(self.original)
        path = relocated / 'inputs/config.json'
        raw = path.read_bytes()
        config = json.loads(raw)
        source = read_catalog(path.parent / config['catalog'])['example']
        self.assertIn((expected, RDF.type, SKOS.Concept), source['graph'])
        self.assertEqual(self.api().configuration_origin(path, raw, config), self.raw)
        self.assertEqual((path.parent / config['shapes']).read_bytes(), b'# shapes\n')
        second = self.root / 'second'
        self.api().write_replay_inputs(second, raw, (path.parent / config['catalog']).read_bytes(),
                                       b'# shapes\n', {'example': source}, self.raw)
        next_path = second / 'inputs/config.json'
        next_raw = next_path.read_bytes()
        self.assertEqual(self.api().configuration_origin(next_path, next_raw, json.loads(next_raw)), self.raw)

    def test_origin_digest_tampering_is_rejected(self):
        archive = self.archive()
        path = archive / 'inputs/config.json'
        (path.parent / 'original-config.json').write_bytes(self.raw + b' ')
        with self.assertRaisesRegex(ValueError, 'sha256'):
            self.api().configuration_origin(path, path.read_bytes(), json.loads(path.read_bytes()))

    def test_replay_cannot_silently_change_semantic_configuration(self):
        archive = self.archive()
        path = archive / 'inputs/config.json'
        for key, replacement in [('domains', []), ('languages', ['zh']),
                                 ('vocabulary', {'uri': 'urn:changed'}), ('sources', {})]:
            config = json.loads(path.read_bytes())
            config[key] = replacement
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'configuration'):
                self.api().configuration_origin(path, json.dumps(config).encode(), config)

    def test_recursive_origin_metadata_is_rejected(self):
        archive = self.archive()
        path = archive / 'inputs/config.json'
        config = json.loads(path.read_bytes())
        origin = dict(self.config, replay_origin={'file': 'other.json', 'sha256': '0' * 64})
        raw = json.dumps(origin).encode()
        (path.parent / 'original-config.json').write_bytes(raw)
        config['replay_origin']['sha256'] = hashlib.sha256(raw).hexdigest()
        with self.assertRaisesRegex(ValueError, 'recursive'):
            self.api().configuration_origin(path, json.dumps(config).encode(), config)

    def test_relative_source_base_is_rejected(self):
        (self.original / 'sources.json').write_text(json.dumps({'sources': [
            {'name': 'example', 'file': 'source.ttl', 'base': '../original/source.ttl'}]}))
        with self.assertRaisesRegex(ValueError, 'base'):
            read_catalog(self.original / 'sources.json')
