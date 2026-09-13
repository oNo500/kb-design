"""A partial application update must never be reported as synchronized."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from rdflib import Graph


class SyncTests(unittest.TestCase):
    def test_database_failure_restores_previous_state_without_success_receipt(self):
        path=Path(__file__).resolve().parents[1]/'sync-current.py'
        spec=importlib.util.spec_from_file_location('sync_current',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);app=root/'app';app.mkdir()
            graph=Graph().parse(data='<urn:old> <urn:p> "old" .',format='turtle')
            remote=[graph.serialize(format='turtle').encode()]
            def request(method,raw=None):
                if method=='GET':return remote[0]
                remote[0]=raw
            expected=Graph().parse(data='<urn:new> <urn:p> "new" .',format='turtle')
            with patch.object(module,'fetch_or_put',side_effect=request),patch.object(module,'verify_remote',side_effect=[ValueError('mismatch'),len(graph)]):
                with self.assertRaisesRegex(ValueError,'mismatch'):
                    module.publish(app,expected,{'nodes':{},'schemes':{},'source_sha256':'x'},{'source_sha256':'x'})
            self.assertEqual(set(Graph().parse(data=remote[0],format='turtle')),set(graph))
            self.assertFalse((app/'sync-receipt.json').exists())
            self.assertNotEqual(json.loads((app/'sync-status.json').read_bytes())['state'],'complete')
