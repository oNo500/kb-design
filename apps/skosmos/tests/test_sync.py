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

    def test_mismatched_label_provenance_is_rejected(self):
        path=Path(__file__).resolve().parents[1]/'sync-current.py'
        spec=importlib.util.spec_from_file_location('sync_labels',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'label-provenance.json').write_text(json.dumps({'schema_version':1,'records':[],'vocabulary_sha256':'wrong'}))
            self.assertTrue(hasattr(module,'label_provenance'),'shared evidence must enter the verified sync path')
            with self.assertRaises(ValueError):module.label_provenance(root,b'vocabulary')

    def test_late_failure_rolls_back_label_evidence_with_database(self):
        path=Path(__file__).resolve().parents[1]/'sync-current.py'
        spec=importlib.util.spec_from_file_location('sync_late',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);label=root/'labels/label-provenance.json';label.parent.mkdir();label.write_bytes(b'old evidence')
            old=Graph().parse(data='<urn:old> <urn:p> "old" .',format='turtle');remote=[old.serialize(format='turtle').encode()]
            def request(method,raw=None):
                if method=='GET':return remote[0]
                remote[0]=raw
            original_write=module.write
            def fail_receipt(path,raw):
                if path.name=='sync-receipt.json':raise OSError('receipt write failed')
                original_write(path,raw)
            new=Graph().parse(data='<urn:new> <urn:p> "new" .',format='turtle')
            with patch.object(module,'fetch_or_put',side_effect=request),patch.object(module,'write',side_effect=fail_receipt):
                with self.assertRaises(OSError):module.publish(root,new,{}, {'source_sha256':'test'},b'new evidence')
            self.assertEqual(label.read_bytes(),b'old evidence')
            self.assertEqual(set(Graph().parse(data=remote[0],format='turtle')),set(old))
