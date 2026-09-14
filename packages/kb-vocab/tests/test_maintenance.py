"""A desired source list and persistent edits drive repeatable maintenance."""
import json
import unittest
from pathlib import Path
from rdflib import Graph,SKOS,RDF,URIRef,Literal
import test_system_build as fixtures


class MaintenanceTests(unittest.TestCase):
    setUp=fixtures.SystemBuildTests.setUp
    save=fixtures.SystemBuildTests.save

    def api(self):
        from kb_vocab.maintenance import maintain
        return maintain

    def test_source_removal_prunes_rules_and_preserves_shared_uri(self):
        maintain=self.api();root=self.root/'published'
        # A URI may be contributed by two sources without identity merging.
        path=self.root/'b.ttl';path.write_text(path.read_text()+'\n<urn:a> a <http://www.w3.org/2004/02/skos/core#Concept> .')
        first=maintain(self.path,root)
        self.assertEqual(first['state'],'complete')
        (self.root/'catalog.json').write_text(json.dumps({'sources':[{'name':'a','file':'a.ttl'}]}))
        second=maintain(self.path,root)
        graph=Graph().parse(root/'current/vocabulary.ttl')
        self.assertIn((URIRef('urn:a'),RDF.type,SKOS.Concept),graph)
        self.assertNotIn((URIRef('urn:other'),RDF.type,SKOS.Concept),graph)
        self.assertEqual(second['source_changes']['removed'],['b'])
        unchanged=maintain(self.path,root)
        self.assertEqual(unchanged['state'],'unchanged')

    def test_local_build_uses_archived_sources_and_conflicts_preserve_current(self):
        from kb_vocab.edit_store import change
        from kb_vocab.local_edits import prepare,resolve
        maintain=self.api();root=self.root/'published';maintain(self.path,root)
        self.config['local_edits']='local-edits.json';self.save()
        build=(root/'current').resolve();up=Graph().parse(build/'upstream.ttl');visible=Graph().parse(build/'vocabulary.ttl')
        change(self.root/'local-edits.json',lambda d:prepare(d,[{'op':'set','subject':'urn:a','predicate':'skos:prefLabel','language':'en','values':['"Local"@en']}],up,visible,'user'))
        # A bad desired path must not affect an edit-only rebuild.
        (self.root/'catalog.json').write_text(json.dumps({'sources':[{'name':'a','file':'missing.ttl'}]}))
        result=maintain(self.path,root,mode='local')
        self.assertEqual(result['state'],'complete')
        self.assertIn((URIRef('urn:a'),SKOS.prefLabel,Literal('Local',lang='en')),Graph().parse(root/'current/vocabulary.ttl'))
        (self.root/'catalog.json').write_text(json.dumps({'sources':[{'name':n,'file':n+'.ttl'} for n in ['a','b']]}))
        source=self.root/'a.ttl';source.write_text(source.read_text().replace('"A"@en','"Remote"@en'))
        previous=(root/'current').resolve()
        result=maintain(self.path,root)
        self.assertEqual(result['state'],'conflict');self.assertEqual((root/'current').resolve(),previous)
        conflicts=json.loads(Path(result['conflicts']).read_bytes())
        change(self.root/'local-edits.json',lambda d:resolve(d,conflicts['conflicts'][0],'local','user'))
        result=maintain(self.path,root)
        self.assertEqual(result['state'],'complete')

    def test_local_create_delete_and_revision_cas_survive_publication(self):
        from kb_vocab.edit_store import change
        from kb_vocab.local_edits import prepare,undo
        maintain=self.api();root=self.root/'published';maintain(self.path,root)
        self.config['local_edits']='local-edits.json';self.save()
        old=(root/'current').resolve();up=Graph().parse(old/'upstream.ttl');view=Graph().parse(old/'vocabulary.ttl')
        path=self.root/'local-edits.json'
        result=change(path,lambda d:prepare(d,[{'op':'create','subject':'urn:local','type':'skos:Concept','fields':{'skos:prefLabel':['"Local"@en']}},{'op':'delete','subject':'urn:b'}],up,view,'user'),0)
        with self.assertRaisesRegex(ValueError,'revision'):
            change(path,lambda d:undo(d,result['patches'][0]['id'],'user'),0)
        state=maintain(self.path,root,mode='local');self.assertEqual(state['state'],'complete',state.get('error'))
        graph=Graph().parse(root/'current/vocabulary.ttl')
        self.assertNotIn((URIRef('urn:b'),RDF.type,SKOS.Concept),graph)
        self.assertIn((URIRef('urn:local'),RDF.type,SKOS.Concept),graph)
        state=maintain(self.path,root);self.assertIn(state['state'],['complete','unchanged'])
        self.assertNotIn((URIRef('urn:b'),RDF.type,SKOS.Concept),Graph().parse(root/'current/vocabulary.ttl'))

    def test_application_retry_does_not_rebuild_published_data(self):
        from unittest.mock import patch
        from kb_vocab.maintenance import resume
        maintain=self.api();root=self.root/'published'
        with patch('kb_vocab.maintenance_apps.synchronize',side_effect=[ValueError('offline'),[]]) as app:
            first=maintain(self.path,root,applications=['unused-app'])
            self.assertEqual(first['state'],'application-failed')
            build=(root/'current').resolve()
            second=resume(root)
            self.assertEqual(second['state'],'complete');self.assertEqual((root/'current').resolve(),build)
            self.assertEqual(app.call_count,2)

    def test_resume_reuses_completed_source_preparation(self):
        from unittest.mock import patch
        from kb_vocab.maintenance import resume
        from kb_vocab.source_pipeline import materialize
        calls=[]
        def interrupted(entry,*args,**kwargs):
            calls.append(entry['name'])
            if calls==['a','b']:raise ValueError('interrupted second source')
            return materialize(entry,*args,**kwargs)
        root=self.root/'published'
        with patch('kb_vocab.maintenance.materialize',side_effect=interrupted):
            state=self.api()(self.path,root)
            self.assertEqual(state['state'],'failed')
            state=resume(root)
        self.assertEqual(state['state'],'complete')
        self.assertEqual(calls,['a','b','b'])

    def test_active_edits_replay_after_relocation(self):
        import shutil,tempfile
        from kb_vocab.edit_store import change
        from kb_vocab.local_edits import prepare
        from kb_vocab.system_build import build_system
        from rdflib.compare import isomorphic
        maintain=self.api();root=self.root/'published';maintain(self.path,root)
        self.config['local_edits']='local-edits.json';self.save()
        previous=root/'current';up=Graph().parse(previous/'upstream.ttl');visible=Graph().parse(previous/'vocabulary.ttl')
        change(self.root/'local-edits.json',lambda d:prepare(d,[{'op':'set','subject':'urn:a','predicate':'skos:prefLabel','language':'en','values':['"Local"@en']}],up,visible,'user'))
        state=maintain(self.path,root,mode='local');self.assertEqual(state['state'],'complete')
        with tempfile.TemporaryDirectory() as directory:
            archive=Path(directory)/'archive';shutil.copytree(previous.resolve(),archive)
            (self.root/'a.ttl').unlink();(self.root/'b.ttl').unlink()
            build_system(archive/'inputs/config.json',Path(directory)/'replayed')
            self.assertTrue(isomorphic(Graph().parse(archive/'vocabulary.ttl'),Graph().parse(Path(directory)/'replayed/vocabulary.ttl')))

    def test_selection_is_persistent_and_does_not_trim_source_copies(self):
        from kb_vocab.system_build import build_system
        from rdflib.compare import isomorphic
        root=self.root/'published';maintain=self.api();maintain(self.path,root)
        before=(self.root/'a.ttl').read_bytes()
        catalog=json.loads((self.root/'catalog.json').read_bytes())
        catalog['sources'][0]['selection']={'roots':['urn:b'],'descendants':True}
        (self.root/'catalog.json').write_text(json.dumps(catalog))
        result=maintain(self.path,root);self.assertEqual(result['state'],'complete',result.get('error'))
        graph=Graph().parse(root/'current/vocabulary.ttl')
        self.assertEqual(set(graph.subjects(RDF.type,SKOS.Concept)),{URIRef('urn:b'),URIRef('urn:other')})
        self.assertIn((URIRef('urn:kb-vocab:group:test'),SKOS.member,URIRef('urn:b')),graph)
        current=(root/'current').resolve();provenance=json.loads((current/'provenance.json').read_bytes())
        self.assertEqual((current/provenance['sources']['a']['copy']).read_bytes(),before)
        build_system(current/'inputs/config.json',self.root/'selection-replay')
        self.assertTrue(isomorphic(graph,Graph().parse(self.root/'selection-replay/vocabulary.ttl')))
        self.assertEqual(maintain(self.path,root)['state'],'unchanged')
        self.assertEqual(maintain(self.path,root,mode='local')['state'],'unchanged')
