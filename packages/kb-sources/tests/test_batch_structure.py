import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import yaml
from kb_sources.download import SourceError


def snapshot(root, source_id, content, fmt):
    spec={'schema_version':1,'id':source_id,'title':source_id,'version':'1','files':[
        {'id':'report','filename':'report.'+fmt,'format':fmt,'url':'https://example.org/report.'+fmt}]}
    src=yaml.safe_dump(spec).encode();f=spec['files'][0]
    receipt={'schema_version':1,'source':{'id':source_id,'title':source_id,'requested_version':'1'},
       'acquired_at':'2026-09-13T00:00:00Z','request_sha256':hashlib.sha256(src).hexdigest(),
       'tool':{'name':'kb-sources','version':'0.1.0'},'files':[{**f,'final_url':f['url'],
       'sha256':hashlib.sha256(content).hexdigest(),'size':len(content),'content_type':'application/pdf' if fmt=='pdf' else 'text/html'}]}
    raw=json.dumps(receipt).encode();p=root/source_id/hashlib.sha256(raw).hexdigest();p.mkdir(parents=True)
    (p/'receipt.json').write_bytes(raw);(p/'source.yaml').write_bytes(src);(p/f['filename']).write_bytes(content)
    return p


class BatchTests(unittest.TestCase):
    def test_invalid_pdf_is_reported_without_publishing_fake_success_or_losing_html(self):
        from kb_sources.structure import extract_all
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);good=snapshot(root,'good',b'<html><h1>Source</h1><p>Content</p></html>','html')
            bad=snapshot(root,'bad',b'%PDF-1.7\nfake body\n%%EOF','pdf')
            out=root/'output';r=extract_all([good,bad],out)
            self.assertEqual(1,r['failed']);self.assertEqual(1,r['parsed'])
            self.assertTrue((out/'good'/good.name/'report'/'structure.json').exists())
            self.assertFalse((out/'bad'/bad.name/'report').exists())
            self.assertEqual('failed', next(x for x in r['files'] if x['source_id']=='bad')['status'])
            with self.assertRaises(SourceError):extract_all([good],out)
            with self.assertRaises(SourceError):extract_all([good],good/'derived')

    def test_native_table_is_retained_without_document_parser(self):
        from kb_sources.structure import extract_all
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=snapshot(root,'table',b'code\tlabel\n01\tHistory\n','tsv')
            result=extract_all([source],root/'result')
            self.assertEqual(1,result['native'])
            self.assertEqual(0,result['failed'])
            row=result['files'][0]
            self.assertEqual('native_structured',row['status'])
            self.assertEqual(str(source/'report.tsv'),row['source_file'])
            self.assertIsNone(row['output'])

    def test_two_formats_share_protected_repeatable_publication(self):
        from kb_sources.structure import extract_file
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=snapshot(root,'pdf',(Path(__file__).parent/'fixtures/layout.pdf').read_bytes(),'pdf')
            extract_file(p,'report',root/'a');extract_file(p,'report',root/'b')
            self.assertEqual((root/'a/structure.json').read_bytes(),(root/'b/structure.json').read_bytes())
            (p/'report.pdf').write_bytes(b'changed')
            with self.assertRaises(SourceError):extract_file(p,'report',root/'c')
            self.assertFalse((root/'c').exists())

if __name__=='__main__':unittest.main()
