"""Protect acquisition evidence and prevent publishing rejected projections."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from rdflib import Graph
from kb_vocab.bundles import read_source, publish_bundle


class BundleTests(unittest.TestCase):
    def test_tampered_snapshot_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw, request = b'source', b'request'
            receipt = json.dumps({'source': {'id': 'example'}, 'request_sha256': hashlib.sha256(request).hexdigest(),
                'acquired_at': 'test', 'files': [{'filename': 'input', 'sha256': hashlib.sha256(raw).hexdigest(),
                    'size': len(raw), 'final_url': 'https://example.org/input'}]}).encode()
            snapshot = root / hashlib.sha256(receipt).hexdigest()
            snapshot.mkdir()
            (snapshot / 'receipt.json').write_bytes(receipt)
            (snapshot / 'source.yaml').write_bytes(request)
            path = snapshot / 'input'
            path.write_bytes(raw)
            read_source(path)
            path.write_bytes(b'edited')
            with self.assertRaisesRegex(ValueError, 'bytes'):
                read_source(path)

    def test_rejected_graph_never_publishes_and_existing_output_survives(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = {'path': str(root / 'input')}
            output = root / 'out'
            graph = Graph().parse(data='''@prefix s: <http://www.w3.org/2004/02/skos/core#> .
                <urn:test:a> a s:Concept ; s:prefLabel "A"@en ; s:altLabel "A"@en .''', format='turtle')
            with self.assertRaisesRegex(ValueError, 'validation'):
                publish_bundle(output, graph, {}, {}, source)
            self.assertFalse(output.exists())
            output.mkdir()
            (output / 'keep').write_text('existing data')
            with self.assertRaisesRegex(ValueError, 'exists'):
                publish_bundle(output, Graph(), {}, {}, source)
            self.assertEqual((output / 'keep').read_text(), 'existing data')
