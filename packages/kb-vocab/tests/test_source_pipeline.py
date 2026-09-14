"""Refresh uses an existing importer and a verified previous identity snapshot."""
import hashlib,json,tempfile,unittest
from pathlib import Path
from rdflib import Graph,RDF,SKOS,Literal
from kb_vocab.source_pipeline import materialize
from kb_vocab.eric import import_eric
from test_eric import xml,term


class SourcePipelineTests(unittest.TestCase):
    def test_refresh_changes_content_but_preserves_prior_uri(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'source.xml';source.write_bytes(xml(term('A'),term('B')))
            first=root/'first';import_eric(source,first)
            previous=first/'vocabulary.ttl';before=Graph().parse(previous)
            source.write_bytes(xml(term('A',attributes='<Attribute name="ScopeNote">Changed</Attribute>'),term('B')))
            entry={'name':'ERIC','file':str(previous),'pipeline':{'importer':'eric','input':str(source)}}
            after,_=materialize(entry,root,root/'refresh',previous,True)
            graph=Graph().parse(after)
            self.assertEqual(set(before.subjects(RDF.type,SKOS.Concept)),set(graph.subjects(RDF.type,SKOS.Concept)))
            self.assertIn(Literal('Changed',lang='en'),set(graph.objects(None,SKOS.scopeNote)))

    def test_selection_change_keeps_latest_materialized_source(self):
        from kb_vocab.source_pipeline import declaration_digest
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);old=root/'old.ttl';latest=root/'latest.ttl'
            old.write_text('old');latest.write_text('latest')
            entry={'name':'ERIC','file':str(old),'pipeline':{'importer':'eric','input':'source.xml'}}
            cached={'file':str(latest),'declaration':declaration_digest(entry)}
            entry['selection']={'roots':['urn:root'],'descendants':True}
            path,_=materialize(entry,root,root/'work',cached=cached)
            self.assertEqual(path,latest)
