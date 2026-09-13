import unittest
from kb_sources.cognitive_atlas import detail_files, validate_detail
from kb_sources.download import SourceError

class CognitiveAtlasTests(unittest.TestCase):
    def test_wrong_or_incomplete_detail_is_rejected(self):
        valid = {'id': 'trm_abc', 'type': 'concept', 'relationships': []}
        validate_detail(valid, 'trm_abc', 'concept')
        validate_detail({'id': 'trm_task', 'type': 'task', 'concepts': [], 'contrasts': [], 'conditions': []}, 'trm_task', 'task')
        for bad in ({**valid, 'id': 'trm_other'}, {'id': 'trm_abc'}, {**valid, 'relationships': {}}):
            with self.assertRaises(SourceError):
                validate_detail(bad, 'trm_abc', 'concept')

    def test_duplicate_or_unsafe_source_ids_cannot_form_download_plan(self):
        for rows in ([{'id': 'trm_a'}, {'id': 'trm_a'}], [{'id': '../outside'}]):
            with self.assertRaises(SourceError):
                detail_files(rows, 'concept')

    def test_resume_requires_intact_snapshots_and_never_redownloads_them(self):
        import io
        import json
        from pathlib import Path
        import tempfile
        from unittest.mock import patch
        import yaml
        from kb_sources.cognitive_atlas import acquire

        class Response(io.BytesIO):
            status = 200
            def __init__(self, url, value):
                body = json.dumps(value).encode()
                super().__init__(body)
                self.url = url
                self.headers = {'Content-Length': str(len(body))}
            def geturl(self):
                return self.url

        def response(request, timeout):
            url = request.full_url
            kind = 'task' if '/task' in url else 'concept'
            identity = 'tsk_b' if kind == 'task' else 'trm_a'
            value = [{'id': identity}]
            if '?id=' in url:
                value = {'id': identity, 'type': kind, 'relationships': [], 'concepts': [], 'contrasts': [], 'conditions': []}
            return Response(url, value)

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = root / 'source.yaml'
            manifest.write_text(yaml.safe_dump({'schema_version': 1, 'id': 'atlas', 'title': 'Atlas', 'version': 'test', 'files': [
                {'id': kind+'s', 'filename': kind+'s.json', 'format': 'json', 'url': 'https://www.cognitiveatlas.org/api/v-alpha/'+kind}
                for kind in ['concept', 'task']]}))
            output = root / 'output'
            with patch('kb_sources.download.build_opener') as factory:
                factory.return_value.open.side_effect = response
                first = acquire(manifest, output, workers=1)
            from kb_sources.cognitive_atlas import export_source
            export_source(output, root / 'export')
            report_path = output / 'report.json'
            complete = report_path.read_bytes()
            incomplete = json.loads(complete)
            incomplete['batches'] = incomplete['batches'][:1]
            report_path.write_text(json.dumps(incomplete))
            with self.assertRaises(SourceError):
                export_source(output, root / 'incomplete-export')
            self.assertFalse((root / 'incomplete-export').exists())
            report_path.write_bytes(complete)
            with patch('kb_sources.download.build_opener', side_effect=AssertionError('unexpected network')):
                second = acquire(manifest, output, workers=1)
                self.assertEqual(first['batches'], second['batches'])
                detail = next((output / first['batches'][0]['snapshot']).glob('trm_*.json'))
                detail.write_text('{}')
                with self.assertRaises(SourceError):
                    acquire(manifest, output, workers=1)
