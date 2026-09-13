"""Review decisions must not leak, survive stale evidence, or lose history."""
import importlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from rdflib import Graph, SKOS, URIRef


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ('a', 'b', 'c'):
            (self.root / (name + '.ttl')).write_text('@prefix s: <http://www.w3.org/2004/02/skos/core#> .\n'
                + f'<urn:{name}> a s:Concept ; s:prefLabel "Shared"@en .\n')
        self.catalog = self.root / 'catalog.json'
        self.catalog.write_text(json.dumps({'sources': [{'name': n, 'file': n+'.ttl'} for n in ('a','b','c')]}))

    def api(self):
        try:
            return importlib.import_module('kb_vocab.review')
        except ModuleNotFoundError:
            self.fail('review workflow is not implemented')

    def test_authorization_required_and_single_decision_can_be_withdrawn(self):
        api = self.api(); store = self.root / 'review'
        api.scan(self.catalog, store)
        proposed = api.propose(store, 'urn:a','urn:b','exactMatch','same scope in fixture','tester',api.inspect(store)['revision'])
        with self.assertRaisesRegex(ValueError, 'authorization'):
            api.decide(store, proposed['record']['id'],'accepted','tester','','test',proposed['revision'])
        self.assertEqual(api.inspect(store)['revision'], proposed['revision'])
        approved = api.decide(store, proposed['record']['id'],'accepted','tester','fixture authorization','test',proposed['revision'])
        api.decide(store,proposed['record']['id'],'withdrawn','tester','test','test',approved['revision'])
        api.build(store,self.root/'withdrawn')
        self.assertEqual(len(Graph().parse(self.root/'withdrawn/mappings.ttl')),0)

    def test_unchanged_decision_carries_but_changed_source_needs_review(self):
        api=self.api(); store=self.root/'review'; api.scan(self.catalog,store)
        p=api.propose(store,'urn:a','urn:b','closeMatch','fixture','tester',api.inspect(store)['revision'])
        api.decide(store,p['record']['id'],'accepted','tester','fixture','fixture',p['revision'])
        api.scan(self.catalog,self.root/'same',previous=store)
        same=api.inspect(self.root/'same',p['record']['id'])['records'][0]
        self.assertEqual(same['status'],'accepted')
        (self.root/'a.ttl').write_text((self.root/'a.ttl').read_text().replace('Shared','Changed'))
        api.build(store,self.root/'stale')
        self.assertEqual(len(Graph().parse(self.root/'stale/mappings.ttl')),0)
        api.scan(self.catalog,self.root/'changed',previous=store)
        changed=api.inspect(self.root/'changed',p['record']['id'])['records'][0]
        self.assertEqual(changed['status'],'needs_review')

    def test_deferral_cannot_clear_source_recheck_requirement(self):
        api=self.api(); store=self.root/'review'; api.scan(self.catalog,store)
        p=api.propose(store,'urn:a','urn:b','closeMatch','fixture','tester',api.inspect(store)['revision'])
        api.decide(store,p['record']['id'],'accepted','tester','fixture','fixture',p['revision'])
        (self.root/'a.ttl').write_text('@prefix s: <http://www.w3.org/2004/02/skos/core#> . <urn:replacement> a s:Concept ; s:prefLabel "Changed"@en .')
        newer=self.root/'newer'; api.scan(self.catalog,newer,previous=store)
        deferred=api.decide(newer,p['record']['id'],'deferred','tester','fixture','fixture',api.inspect(newer)['revision'])
        with self.assertRaises(ValueError):
            api.decide(newer,p['record']['id'],'accepted','tester','fixture','fixture',deferred['revision'])
        api.build(newer,self.root/'no-stale')
        self.assertEqual(len(Graph().parse(self.root/'no-stale/mappings.ttl')),0)

    def test_batch_is_atomic_and_checks_combined_mapping_effect(self):
        api=self.api(); store=self.root/'review'; api.scan(self.catalog,store)
        ids=[]
        for a,b,predicate in [('urn:a','urn:b','exactMatch'),('urn:b','urn:c','exactMatch'),('urn:a','urn:c','broadMatch')]:
            p=api.propose(store,a,b,predicate,'fixture','tester',api.inspect(store)['revision']); ids.append(p['record']['id'])
        revision=api.inspect(store)['revision']
        preview=api.preview(store,[{'id':i,'decision':'accepted'} for i in ids])
        self.assertFalse(preview['ready'])
        with self.assertRaisesRegex(ValueError,'conflict'):
            api.decide_batch(store,[{'id':i,'decision':'accepted'} for i in ids],'tester','fixture','fixture',revision)
        self.assertEqual(api.inspect(store)['revision'],revision)
        preview=api.preview(store,[{'id':i,'decision':'accepted'} for i in ids[:2]])
        self.assertTrue(preview['ready'])
        self.assertEqual(len(preview['added']),2)
        self.assertEqual(api.inspect(store)['revision'],revision)
        api.decide_batch(store,[{'id':i,'decision':'accepted'} for i in ids[:2]],'tester','fixture','fixture',revision)
        api.build(store,self.root/'batch')
        self.assertEqual(len(Graph().parse(self.root/'batch/mappings.ttl')),2)

    def test_source_change_during_build_prevents_publication(self):
        api=self.api(); store=self.root/'review'; api.scan(self.catalog,store)
        p=api.propose(store,'urn:a','urn:b','closeMatch','fixture','tester',api.inspect(store)['revision'])
        api.decide(store,p['record']['id'],'accepted','tester','fixture','fixture',p['revision'])
        original=api._conflicts
        def change_then_validate(state, rows):
            (self.root/'a.ttl').write_text((self.root/'a.ttl').read_text().replace('Shared','Changed'))
            return original(state,rows)
        with patch.object(api,'_conflicts',side_effect=change_then_validate):
            with self.assertRaisesRegex(ValueError,'Source changed'):
                api.build(store,self.root/'raced')
        self.assertFalse((self.root/'raced').exists())

    def test_tampering_with_journal_is_rejected(self):
        api=self.api(); store=self.root/'review'; api.scan(self.catalog,store)
        api.propose(store,'urn:a','urn:b','exactMatch','fixture','tester',api.inspect(store)['revision'])
        event=next((store/'events').glob('*.ttl'))
        event.write_text(event.read_text().replace('fixture','changed'))
        with self.assertRaises(ValueError):
            api.inspect(store)
