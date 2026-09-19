"""Source loss, identity drift and false-success are the retained failure risks."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from rdflib import Graph, Literal, Namespace, RDF, SKOS, URIRef

XL = Namespace('http://www.w3.org/2008/05/skos-xl#')
PACKAGE = Path(__file__).resolve().parents[1]
XML = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:skos="http://www.w3.org/2004/02/skos/core#" xmlns:dc="http://purl.org/dc/elements/1.1/">
<skos:ConceptScheme rdf:about="https://example.org/Test scheme"><dc:title>Test</dc:title><skos:hasTopConcept rdf:resource="#1"/><skos:hasTopConcept rdf:resource="#2"/></skos:ConceptScheme>
<skos:Concept rdf:about="#1" xml:lang="en"><skos:prefLabel>First</skos:prefLabel><skos:inScheme rdf:resource="https://example.org/Test scheme"/><skos:topConceptOf rdf:resource="https://example.org/Test scheme"/><skos:narrower rdf:resource="#3"/></skos:Concept>
<skos:Concept rdf:about="#2" xml:lang="en"><skos:prefLabel>Second</skos:prefLabel><skos:inScheme rdf:resource="https://example.org/Test scheme"/><skos:topConceptOf rdf:resource="https://example.org/Test scheme"/><skos:narrower rdf:resource="#3"/></skos:Concept>
<skos:Concept rdf:about="#3" xml:lang="en"><skos:prefLabel>Shared</skos:prefLabel><skos:altLabel>λ &amp; quotes " here</skos:altLabel><skos:hiddenLabel>shraed</skos:hiddenLabel><skos:scopeNote>Keep this note.</skos:scopeNote><skos:inScheme rdf:resource="https://example.org/Test scheme"/><skos:broader rdf:resource="#1"/><skos:broader rdf:resource="#2"/></skos:Concept>
</rdf:RDF>'''


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root/'source.xml'
        self.source.write_text(XML)
        self.config = {
            'schema_version':1,
            'source': {'repository':'https://github.com/cli99/acm-ccs',
                       'commit':'a'*40,'path':'source.xml',
                       'sha256':hashlib.sha256(self.source.read_bytes()).hexdigest()},
            'identity_base_iri':'https://example.org/identity.xml',
            'scheme': {'name':{'value':'Test','language':'en'},
                       'scope_note':{'value':'Test scope.','language':'en'},
                       'basis':'Approved test fixture'},
        }
        self.config_path=self.root/'config.json'
        self.save_config()

    def save_config(self):
        self.config_path.write_text(json.dumps(self.config))

    def run_cli(self,*args):
        env=dict(os.environ)
        env['PYTHONPATH']=str(PACKAGE/'src')+os.pathsep+env.get('PYTHONPATH','')
        return subprocess.run([sys.executable,'-m','kb_vocab_ccs',*map(str,args)],env=env,text=True,capture_output=True)

    def build(self,name='built'):
        out=self.root/name
        result=self.run_cli('build','--source',self.source,'--config',self.config_path,'--output',out)
        self.assertEqual(result.returncode,0,result.stderr)
        return out

    def test_preserves_source_and_xl_roles_with_multiple_parents(self):
        out=self.build()
        source=Graph().parse(out/'source.ttl')
        data=Graph().parse(out/'vocabulary.ttl')
        self.assertTrue(set(source)<=set(data))
        child=URIRef('https://example.org/identity.xml#3')
        self.assertEqual(set(data.objects(child,SKOS.broader)),{URIRef('https://example.org/identity.xml#1'),URIRef('https://example.org/identity.xml#2')})
        for role,value in [(SKOS.prefLabel,'Shared'),(SKOS.altLabel,'λ & quotes " here'),(SKOS.hiddenLabel,'shraed')]:
            labels=list(data.objects(child,XL[str(role).split('#')[-1]]))
            self.assertEqual(len(labels),1)
            self.assertIn((labels[0],XL.literalForm,Literal(value,lang='en')),data)
            self.assertIn((labels[0],RDF.type,XL.Label),data)
        self.assertEqual(self.source.read_text(),XML)

    def test_rebuild_and_commit_update_preserve_identity(self):
        a=self.build('a'); b=self.build('b')
        for name in ('vocabulary.ttl','source.ttl','manifest.json','adaptations.json'):
            self.assertEqual((a/name).read_bytes(),(b/name).read_bytes(),name)
        self.config['source']['commit']='b'*40
        self.save_config()
        c=self.build('c')
        self.assertEqual((a/'vocabulary.ttl').read_bytes(),(c/'vocabulary.ttl').read_bytes())

    def test_hash_mismatch_and_existing_output_are_rejected(self):
        out=self.build()
        before=(out/'vocabulary.ttl').read_bytes()
        result=self.run_cli('build','--source',self.source,'--config',self.config_path,'--output',out)
        self.assertEqual(result.returncode,2)
        self.assertEqual((out/'vocabulary.ttl').read_bytes(),before)
        self.source.write_text(XML.replace('Shared','Changed'))
        result=self.run_cli('build','--source',self.source,'--config',self.config_path,'--output',self.root/'bad')
        self.assertEqual(result.returncode,2)
        self.assertFalse((self.root/'bad').exists())

    def test_external_entity_is_rejected_before_output(self):
        self.source.write_text(XML.replace('<rdf:RDF','<!DOCTYPE rdf:RDF [<!ENTITY leak SYSTEM "file:///etc/passwd">]>\n<rdf:RDF',1))
        self.config['source']['sha256']=hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.save_config()
        result=self.run_cli('build','--source',self.source,'--config',self.config_path,'--output',self.root/'bad')
        self.assertEqual(result.returncode,2)
        self.assertFalse((self.root/'bad').exists())

    def test_validation_reports_failure_and_success_with_real_engine(self):
        out=self.build()
        good=self.run_cli('check',out/'vocabulary.ttl','--profile','all','--output',self.root/'good-report')
        self.assertEqual(good.returncode,0,good.stderr)
        summary=json.loads((self.root/'good-report/summary.json').read_text())
        self.assertTrue(summary['conforms'])
        missing=self.run_cli('check',out/'source.ttl','--profile','target','--output',self.root/'source-report')
        self.assertEqual(missing.returncode,1,missing.stderr)
        source_summary=json.loads((self.root/'source-report/summary.json').read_text())
        self.assertIn('urn:kb-vocab-shacl:ConceptXLNames',
                      {r['rule'] for r in source_summary['profiles']['target']['by_rule']})
        g=Graph().parse(out/'vocabulary.ttl')
        g.add((URIRef('https://example.org/identity.xml#3'),SKOS.altLabel,Literal('Shared',lang='en')))
        g.serialize(destination=self.root/'bad.ttl',format='turtle')
        bad=self.run_cli('check',self.root/'bad.ttl','--profile','target','--output',self.root/'bad-report')
        self.assertEqual(bad.returncode,1,bad.stderr)
        summary=json.loads((self.root/'bad-report/summary.json').read_text())
        self.assertFalse(summary['conforms'])
        self.assertGreater(summary['profiles']['target']['results'],0)


    def test_inventory_and_check_share_generated_label_scope(self):
        out=self.build()
        result=self.run_cli('inventory',out,'--output',self.root/'inventory')
        self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads((self.root/'inventory/inventory.json').read_text())
        local=next(c for c in report['conditions'] if c['shape']=='urn:kb-vocab-shacl:LocalLabel')
        self.assertEqual(local['scope_status'],'specified')
        self.assertEqual(local['selected_objects'],6)
        self.assertFalse(local['validation_executed'])

if __name__=='__main__':
    unittest.main()
