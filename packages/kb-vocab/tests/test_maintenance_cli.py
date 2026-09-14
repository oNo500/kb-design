"""The public CLI resolves a source-update conflict against the incoming source."""
import contextlib,io,json,unittest
from pathlib import Path
from rdflib import Graph,SKOS,URIRef,Literal
import test_system_build as fixtures
from kb_vocab.cli import main


class MaintenanceCLITests(unittest.TestCase):
    setUp=fixtures.SystemBuildTests.setUp
    save=fixtures.SystemBuildTests.save
    def command(self,*args):
        stream=io.StringIO()
        with contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):rc=main(list(args))
        return rc,json.loads(stream.getvalue())

    def test_edit_sync_conflict_resolve_and_undo(self):
        workspace=self.root/'maintenance.json';root=self.root/'published'
        workspace.write_text(json.dumps({'schema_version':1,'config':'config.json','output':'published'}))
        options=['--workspace',str(workspace)]
        self.assertEqual(self.command('sync',*options)[0],0)
        patch=self.root/'patch.json';patch.write_text(json.dumps([{'op':'set','subject':'urn:a','predicate':'skos:prefLabel','language':'en','values':['"Local"@en']}]))
        self.assertEqual(self.command('edit',*options,'apply',str(patch),'--reason','user')[0],0)
        source=self.root/'a.ttl';source.write_text(source.read_text().replace('"A"@en','"Remote"@en'))
        code,result=self.command('sync',*options);self.assertEqual(code,1)
        conflicts=json.loads(Path(result['conflicts']).read_bytes());ident=conflicts['conflicts'][0]['id']
        code,result=self.command('edit',*options,'resolve',result['conflicts'],'--id',ident,'--choice','local','--reason','user')
        self.assertEqual(code,0,result)
        self.assertIn((URIRef('urn:a'),SKOS.prefLabel,Literal('Local',lang='en')),Graph().parse(root/'current/vocabulary.ttl'))
        self.assertEqual(self.command('edit',*options,'undo',ident,'--reason','user')[0],0)
        self.assertIn((URIRef('urn:a'),SKOS.prefLabel,Literal('Remote',lang='en')),Graph().parse(root/'current/vocabulary.ttl'))
