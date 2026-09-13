"""Faults invisible to SHACL must not publish; archives must survive relocation."""
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from rdflib import Graph, SKOS, URIRef
from rdflib.compare import isomorphic
import test_system_build as fixtures
from kb_vocab.normalization import normalize_sources
from kb_vocab.publication import build_versioned
from kb_vocab.system_build import build_system


class BuildIntegrityTests(unittest.TestCase):
    setUp = fixtures.SystemBuildTests.setUp
    save = fixtures.SystemBuildTests.save

    def test_lost_relation_cannot_replace_current(self):
        root = self.root / 'published'
        build_versioned(self.path, root, 'good')
        def omit(*args, **kwargs):
            graph, changes, summary = normalize_sources(*args, **kwargs)
            graph.remove((URIRef('urn:b'), SKOS.broader, URIRef('urn:outside')))
            graph.remove((URIRef('urn:outside'), SKOS.narrower, URIRef('urn:b')))
            return graph, changes, summary
        with patch('kb_vocab.system_build.normalize_sources', side_effect=omit):
            with self.assertRaisesRegex(ValueError, 'accounting'):
                build_versioned(self.path, root, 'bad')
        self.assertEqual((root / 'current').resolve().name, 'good')

    def test_relocated_bundle_rebuilds_without_original_inputs(self):
        source = self.root / 'a.ttl'
        source.write_text(source.read_text() + '\n<#local> a <http://www.w3.org/2004/02/skos/core#Concept> .')
        self.config['sources']['a'] = hashlib.sha256(source.read_bytes()).hexdigest()
        self.save()
        build_system(self.path, self.root / 'out')
        with tempfile.TemporaryDirectory() as directory:
            archived = Path(directory) / 'archive'
            shutil.move(self.root / 'out', archived)
            for name in ('a.ttl', 'b.ttl', 'catalog.json', 'config.json'):
                (self.root / name).unlink()
            build_system(archived / 'inputs/config.json', Path(directory) / 'replayed')
            self.assertTrue(isomorphic(Graph().parse(archived / 'vocabulary.ttl'),
                                       Graph().parse(Path(directory) / 'replayed/vocabulary.ttl')))

    def test_fabricated_ledger_and_unexplained_output_are_rejected(self):
        from copy import deepcopy
        from kb_vocab.accounting import verify_normalization
        from kb_vocab.review_catalog import read_catalog
        sources = read_catalog(self.root / 'catalog.json')
        graph, changes, _ = normalize_sources(sources)
        verify_normalization(sources, graph, changes, ['en', 'zh'])
        for fault in ('false_removal', 'false_support', 'duplicate', 'extra'):
            altered = Graph() + graph
            ledger = deepcopy(changes)
            if fault == 'false_removal':
                ledger.append({'source':'a', 'path':sources['a']['path'],
                               'sha256':sources['a']['sha256'], 'subject':'urn:b',
                               'predicate':str(SKOS.broader), 'object':'<urn:a>',
                               'action':'filtered', 'reason':'language_outside_output_scope'})
            elif fault == 'false_support':
                ledger[0]['supporting_original']['object'] = '<urn:invented>'
            elif fault == 'duplicate':
                ledger.append(deepcopy(ledger[0]))
            else:
                altered.add((URIRef('urn:a'), SKOS.related, URIRef('urn:other')))
            with self.subTest(fault=fault), self.assertRaisesRegex(ValueError, 'accounting'):
                verify_normalization(sources, altered, ledger, ['en', 'zh'])

    def test_source_uri_replacement_cannot_publish_as_an_update(self):
        root=self.root/'published'
        build_versioned(self.path,root,'before')
        source=self.root/'a.ttl'
        source.write_text(source.read_text().replace('urn:outside','urn:replacement'))
        self.config['sources']['a']=hashlib.sha256(source.read_bytes()).hexdigest();self.save()
        with self.assertRaisesRegex(ValueError,'identity loss'):
            build_versioned(self.path,root,'after')
        self.assertEqual((root/'current').resolve().name,'before')
