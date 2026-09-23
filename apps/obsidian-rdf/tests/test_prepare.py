import json
from pathlib import Path
import tempfile
import unittest

from kb_obsidian_rdf.common import ContractError, digest, json_bytes


class PrepareTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory, filenames in [
            ('ccs/partitioned-20260921-rdf', ['concepts.ttl', 'entities.ttl']),
            ('writing/expanded-20260922-final', ['vocabulary.ttl']),
        ]:
            base = self.root/'output/vocabulary'/directory
            base.mkdir(parents=True)
            manifest = {'files': {}}
            for name in filenames:
                cls = ('http://www.wikidata.org/entity/Q7397' if name == 'entities.ttl'
                       else 'http://www.w3.org/2004/02/skos/core#Concept')
                data = f'<urn:{name}> a <{cls}> .\n'.encode()
                (base/name).write_bytes(data)
                manifest['files'][name] = digest(data)
            (base/'manifest.json').write_bytes(json_bytes(manifest))
        for name in ('types','genres','forms'):
            p = self.root/f'data/vocab/{name}.yaml'; p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(f'{name}: []\nversion: test\n')
        p = self.root/'data/references/bibliography.yaml'; p.parent.mkdir(parents=True)
        p.write_text('references: []\nschema_version: 3\nversion: test\n')
        self.authority = self.root/'approval.md'; self.authority.write_text('开发预览授权\n')
        model = self.root/'docs/model/content/设计-内容模型.md'
        model.parent.mkdir(parents=True); model.write_text('已采用的测试类型与体裁\n')

    def test_fixed_input_preserves_original_identity_without_approving_formal_use(self):
        from kb_obsidian_rdf.prepare import prepare
        path=self.root/'build/development.json'
        prepare(self.root,path,authority=self.authority)
        data=json.loads(path.read_text())
        self.assertEqual(data['mode'],'preview')
        self.assertEqual(data['sources'][0]['scope']['subject_iris'],['urn:concepts.ttl'])
        self.assertEqual(data['sources'][1]['trial_subjects'],['urn:entities.ttl'])
        self.assertIsNone(data['sources'][0]['authority']['formal_reference'])

    def test_changed_generated_source_is_rejected_before_manifest_is_written(self):
        from kb_obsidian_rdf.prepare import prepare
        p=self.root/'output/vocabulary/ccs/partitioned-20260921-rdf/concepts.ttl'
        p.write_text(p.read_text()+'<urn:extra> a <http://www.w3.org/2004/02/skos/core#Concept> .\n')
        with self.assertRaises(ContractError):
            prepare(self.root,self.root/'bad.json',authority=self.authority)
        self.assertFalse((self.root/'bad.json').exists())
