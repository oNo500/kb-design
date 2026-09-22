"""Retained risks: evidence drift, rule/definition confusion and unauthorized output."""
import importlib
import json
from hashlib import sha256
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import tempfile
import threading
import unittest

from rdflib import Graph,Namespace,RDF,SKOS,URIRef


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                body=b'<!doctype html><html><body><h1>Writing</h1><p id="meaning">A paragraph is a unit of text.</p><h2 id="advice">Focus each paragraph on one topic.</h2></body></html>'
                self.send_response(200);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
            def log_message(self,*args):pass
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        threading.Thread(target=server.serve_forever,daemon=True).start()
        self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
        manifest={'schema_version':1,'id':'writing-test','title':'Writing test','version':'fixture',
                  'files':[{'id':'paragraphs','url':f'http://127.0.0.1:{server.server_port}/page','filename':'page.html','format':'html'}]}
        self.manifest=self.root/'source.yaml';self.manifest.write_text(json.dumps(manifest))
        try:self.api=importlib.import_module('kb_vocab_writing.workflow')
        except ModuleNotFoundError:self.fail('写作词表工作流尚未实现')
        self.bundle=self.root/'collected'
        self.api.collect(self.bundle,manifest=self.manifest)
        self.lock=self.bundle/'sources.json'
        evidence={'source':'paragraphs','selector':'#meaning','quote':'A paragraph is a unit of text.'}
        self.spec={'schema_version':1,'approved':False,'approval':None,
                   'source_lock_sha256':sha256(self.lock.read_bytes()).hexdigest(),
                   'scheme':{'id':'urn:test:writing','label':{'text':'Writing','language':'en'},'scope':{'text':'Test scope','language':'en'},'top_concepts':['urn:test:paragraph']},
                   'concepts':[{'id':'urn:test:paragraph','labels':[{'id':'urn:test:paragraph-label','role':'preferred','text':'Paragraph','language':'en'}],
                                'evidence':[evidence], 'statements':[
                                    {'id':'urn:test:definition','kind':'definition','text':'A paragraph is a unit of text.','language':'en','evidence':[evidence]},
                                    {'id':'urn:test:guidance','kind':'guidance','text':'Focus each paragraph on one topic.','language':'en','applicability':'Technical documentation','evidence':[{'source':'paragraphs','selector':'#advice','quote':'Focus each paragraph on one topic.'}]}],
                                'broader':[],'related':[]}],
                   'collections':[{'id':'urn:test:group','label':{'text':'Writing group','language':'en'},'scope':{'text':'Test grouping','language':'en'},'members':['urn:test:paragraph']}]}
        self.input=self.root/'input.json'
        self.save()
    def save(self):self.input.write_text(json.dumps(self.spec))
    def test_preview_keeps_guidance_separate_and_build_requires_confirmation(self):
        with self.assertRaises(ValueError):self.api.build(self.input,self.lock,self.root/'unapproved')
        self.assertFalse((self.root/'unapproved').exists())
        self.api.build(self.input,self.lock,self.root/'preview',preview=True)
        graph=Graph().parse(self.root/'preview/vocabulary.ttl')
        self.assertIn((URIRef('urn:test:paragraph'),SKOS.note,URIRef('urn:test:guidance')),graph)
        self.assertNotIn((URIRef('urn:test:paragraph'),SKOS.definition,URIRef('urn:test:guidance')),graph)
        self.assertFalse(json.loads((self.root/'preview/manifest.json').read_text())['input_approved'])
    def test_source_changes_and_wrong_locator_stop_before_writes(self):
        self.spec['concepts'][0]['evidence'][0]['selector']='#missing';self.save()
        with self.assertRaises(ValueError):self.api.build(self.input,self.lock,self.root/'bad',preview=True)
        self.assertFalse((self.root/'bad').exists())
        lock=json.loads(self.lock.read_text());snapshot=(self.lock.parent/lock['files'][0]['snapshot']).resolve()
        (snapshot/'page.html').write_text('<html>Changed</html>')
        with self.assertRaises(ValueError):self.api.build(self.input,self.lock,self.root/'changed',preview=True)
    def test_confirmed_build_is_repeatable_and_preserves_ids_when_text_changes(self):
        self.spec['approved']=True;self.spec['approval']={'by':'test-user','reference':'fixture approval','content_sha256':self.api.approval_digest(self.spec)};self.save()
        self.api.build(self.input,self.lock,self.root/'one');self.api.build(self.input,self.lock,self.root/'two')
        self.assertEqual((self.root/'one/vocabulary.ttl').read_bytes(),(self.root/'two/vocabulary.ttl').read_bytes())
        self.spec['concepts'][0]['labels'][0]['text']='Paragraph revised';self.save()
        with self.assertRaises(ValueError):self.api.build(self.input,self.lock,self.root/'stale')
        self.spec['approved']=False;self.spec['approval']=None;self.save()
        self.api.build(self.input,self.lock,self.root/'three',preview=True)
        graph=Graph().parse(self.root/'three/vocabulary.ttl')
        xl=Namespace('http://www.w3.org/2008/05/skos-xl#')
        self.assertIn((URIRef('urn:test:paragraph'),xl.prefLabel,URIRef('urn:test:paragraph-label')),graph)
    def test_missing_reference_and_identity_collision_are_rejected(self):
        self.spec['collections'][0]['members']=['urn:test:missing'];self.save()
        with self.assertRaises(ValueError):self.api.build(self.input,self.lock,self.root/'missing',preview=True)
        self.spec['collections'][0]['members']=['urn:test:paragraph']
        self.spec['concepts'][0]['labels'][0]['id']='urn:test:paragraph';self.save()
        with self.assertRaises(ValueError):self.api.build(self.input,self.lock,self.root/'collision',preview=True)
    def test_inventory_and_check_do_not_claim_semantic_approval(self):
        self.api.build(self.input,self.lock,self.root/'preview',preview=True)
        validation=importlib.import_module('kb_vocab_writing.validation')
        result=validation.inspect_bundle(self.root/'preview',self.root/'report',run_checks=True)
        self.assertTrue(result['conforms'])
        self.assertFalse(result['input_approved'])
        self.assertFalse(result['semantic_review_executed'])
        self.assertEqual(result['coverage']['uncovered_subjects'],[])
        self.assertEqual(result['coverage']['unlisted_predicates'],[])
        stats=json.loads((self.root/'report/inventory.json').read_text())
        notes=next(r for r in stats['resources'] if r['type']=='Note')
        descriptions=[f for f in notes['fields'] if f['field']=='http://purl.org/dc/terms/description']
        self.assertEqual(len(descriptions),1)
        self.assertEqual(descriptions[0]['present'],1)
        graph=Graph().parse(self.root/'preview/vocabulary.ttl')
        xl=Namespace('http://www.w3.org/2008/05/skos-xl#')
        graph.remove((URIRef('urn:test:paragraph-label'),xl.literalForm,None))
        # Forging a manifest after editing generated files is not treated as approved input.
        graph.serialize(destination=self.root/'preview/vocabulary.ttl',format='turtle')
        with self.assertRaises(ValueError):validation.inspect_bundle(self.root/'preview',self.root/'bad-report',run_checks=True)


    def test_loaded_rules_reject_conflicting_preferred_names(self):
        self.spec['concepts'][0]['labels'].append({'id':'urn:test:second-label','role':'preferred','text':'Conflicting name','language':'en'})
        self.save();self.api.build(self.input,self.lock,self.root/'conflict',preview=True)
        validation=importlib.import_module('kb_vocab_writing.validation')
        report=validation.inspect_bundle(self.root/'conflict',self.root/'conflict-report',run_checks=True)
        self.assertFalse(report['conforms'])
        self.assertGreater(report['profiles']['target']['counts'].get('Violation',0),0)


    def test_name_provenance_is_preserved_without_fabricating_model_version(self):
        self.spec['concepts'][0]['labels'][0]['basis']={
            'method':'model','executor':'test-agent','model_version':None,
            'recorded_at':'2026-09-21T00:00:00Z','note':'Model translation, not human reviewed.'}
        self.save();self.api.build(self.input,self.lock,self.root/'provenance',preview=True)
        graph=Graph().parse(self.root/'provenance/vocabulary.ttl')
        notes=[str(v) for v in graph.objects(URIRef('urn:test:paragraph-label'),SKOS.editorialNote)]
        self.assertEqual(len(notes),1)
        self.assertIn('test-agent',notes[0])
        self.assertIn('未提供',notes[0])
        self.assertEqual(json.loads((self.root/'provenance/input.json').read_text())['concepts'][0]['labels'][0]['basis']['model_version'],None)

if __name__=='__main__':unittest.main()
