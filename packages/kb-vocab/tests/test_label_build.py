"""Labels must survive domain export/replay and fail before publication."""
import json
import shutil
import unittest
from pathlib import Path
from rdflib import Graph, SKOS, URIRef, Literal
from rdflib.compare import isomorphic
import test_system_build as fixtures
from kb_vocab.system_build import build_system
from kb_vocab.labels import label_context

class LabelBuildTests(unittest.TestCase):
    setUp=fixtures.SystemBuildTests.setUp
    save=fixtures.SystemBuildTests.save
    def prepare(self):
        baseline=self.root/'baseline';build_system(self.path,baseline)
        context=label_context(Graph().parse(baseline/'vocabulary.ttl'),'urn:a')
        (self.root/'labels.zh.ttl').write_text('<urn:a> <'+str(SKOS.prefLabel)+'> "甲"@zh .')
        self.adoptions={'schema_version':1,'records':[{'id':'fixture','accept':True,'uri':'urn:a','property':str(SKOS.prefLabel),
            'language':'zh','label':'甲','original':context,'basis':{'level':5,'model':{'name':'test-model','date':'2026-09-13','rationale':'fixture','approval':'test-only'}}}]}
        graph=Graph().parse(baseline/'vocabulary.ttl')
        extra=[('urn:other','乙'),('urn:kb-vocab:group:test','测试分组'),('urn:kb-vocab:scheme:test-vocabulary','测试词表')]
        for i,(uri,label) in enumerate(extra):
            record=dict(self.adoptions['records'][0],id=f'fixture-extra-{i}',uri=uri,label=label,original=label_context(graph,uri))
            self.adoptions['records'].append(record)
        with (self.root/'labels.zh.ttl').open('a') as stream:
            for uri,label in extra:stream.write(f'\n<{uri}> <{SKOS.prefLabel}> "{label}"@zh .')
        self.adoption_file=self.root/'adoptions.json';self.adoption_file.write_text(json.dumps(self.adoptions))
        self.config['labels']={'file':'labels.zh.ttl','adoptions':'adoptions.json'};self.save()
    def test_published_views_and_moved_replay_keep_the_same_labels_and_evidence(self):
        self.prepare();out=self.root/'labelled';build_system(self.path,out)
        expected=(URIRef('urn:a'),SKOS.prefLabel,Literal('甲',lang='zh'))
        for filename in ('vocabulary.ttl','domains/test.ttl'):
            self.assertIn(expected,Graph().parse(out/filename))
        self.assertIn((URIRef('urn:other'),SKOS.prefLabel,Literal('乙',lang='zh')),Graph().parse(out/'unassigned.ttl'))
        for filename in ('organization.ttl','domains/test.ttl'):
            self.assertIn((URIRef('urn:kb-vocab:group:test'),SKOS.prefLabel,Literal('测试分组',lang='zh')),Graph().parse(out/filename))
        records=json.loads((out/'label-provenance.json').read_text())['records']
        self.assertEqual(records[0]['basis']['model']['name'],'test-model')
        moved=self.root/'moved';shutil.copytree(out,moved)
        (self.root/'labels.zh.ttl').unlink();self.adoption_file.unlink()
        replay=self.root/'replayed';build_system(moved/'inputs/config.json',replay)
        self.assertTrue(isomorphic(Graph().parse(out/'vocabulary.ttl'),Graph().parse(replay/'vocabulary.ttl')))
        self.assertEqual(json.loads((replay/'label-provenance.json').read_text())['records'],records)
    def test_invalid_labels_do_not_switch_current(self):
        self.prepare()
        from kb_vocab.publication import build_versioned
        root=self.root/'published';build_versioned(self.path,root,'good')
        self.adoptions['records'][0]['accept']=False;self.adoption_file.write_text(json.dumps(self.adoptions))
        with self.assertRaises(ValueError):build_versioned(self.path,root,'bad')
        self.assertEqual((root/'current').resolve().name,'good');self.assertFalse((root/'versions/bad').exists())
