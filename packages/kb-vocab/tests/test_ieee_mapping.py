import unittest
import tempfile
import json
import hashlib
from pathlib import Path
from rdflib import Graph
from rdflib import Literal, RDF, SKOS, DCTERMS


def entry(id,name,form,relations):
    return {'id':id,'name':name,'form':form,'locator':{'page':3,'column':1},
            'relations':[{'predicate':p,'target':v,'source_group':g,'connector_after':c,'fragments':[]} for p,v,g,c in relations]}


def sample():
    return {'representation':'ieee-source-transcription','source':{'sha256':'a'*64,'version':'July 2025 Version 1.04','url':'https://example.org/book.pdf'},'unassigned':[],
      'entries':[entry('e1','Root','preferred',[('NT','Child','g1',None),('RT','Child','g2',None),('UF','Alias','g3',None),('UF','Mixed','g3',None),('UF','Root','g3',None)]),
                 entry('e2','Child','preferred',[('BT','Root','g4',None),('RT','Root','g5',None),('UF','Mixed','g6',None)]),
                 entry('e3','Alias','nonpreferred',[('USE','Root','g7',None)]),
                 entry('e4','Mixed','nonpreferred',[('USE','Root','g8','AND'),('USE','Child','g8',None)])]}

class IEEEMappingTests(unittest.TestCase):
    def test_labels_are_literals_and_ambiguous_groups_and_conflicts_are_held(self):
        from kb_vocab.ieee import project_ieee
        graph,ledger=project_ieee(sample())
        self.assertEqual(2,len(set(graph.subjects(RDF.type,SKOS.Concept))))
        root=next(graph.subjects(SKOS.prefLabel,Literal('Root',lang='en')))
        child=next(graph.subjects(SKOS.prefLabel,Literal('Child',lang='en')))
        self.assertIn((root,SKOS.altLabel,Literal('Alias',lang='en')),graph)
        self.assertFalse(list(graph.triples((None,SKOS.altLabel,Literal('Mixed',lang='en')))))
        self.assertFalse(list(graph.triples((None,SKOS.related,None))))
        self.assertIn((child,SKOS.broader,root),graph)
        self.assertEqual(sum(len(e['relations']) for e in sample()['entries']),len(ledger['relations']))
        self.assertTrue(any(r['reason']=='and_group' for r in ledger['relations']))
        self.assertTrue(any(r['reason']=='s27_overlap' for r in ledger['relations']))

    def test_persisted_identity_uses_exact_source_keys_across_versions(self):
        from kb_vocab.ieee import project_ieee
        old,_=project_ieee(sample());root=next(old.subjects(SKOS.prefLabel,Literal('Root',lang='en')))
        old.set((root,SKOS.prefLabel,Literal('Edited display name',lang='en')))
        new,_=project_ieee(sample(),identities=old)
        self.assertIn((root,SKOS.prefLabel,Literal('Root',lang='en')),new)
        changed=sample();changed['source']['sha256']='b'*64
        updated,_=project_ieee(changed,identities=old)
        self.assertIn((root,SKOS.prefLabel,Literal('Root',lang='en')),updated)

    def test_changed_source_record_meaning_cannot_silently_reuse_identity(self):
        from kb_vocab.ieee import project_ieee
        old,_=project_ieee(sample())
        modified=sample();modified['entries'][0]['name']='Different source heading'
        with self.assertRaisesRegex(ValueError,'identity source'):
            project_ieee(modified,identities=old)

    def test_modified_identity_keys_are_rejected_by_the_import_entrypoint(self):
        from kb_vocab.ieee import import_ieee
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source_dir=root/'source';source_dir.mkdir()
            data=sample();raw=json.dumps(data).encode();source=source_dir/'thesaurus.json';source.write_bytes(raw)
            (source_dir/'record.json').write_text(json.dumps({'source':data['source'],'outputs':{'thesaurus.json':hashlib.sha256(raw).hexdigest()}}))
            first=root/'first';import_ieee(source,first)
            ttl=first/'vocabulary.ttl';g=Graph().parse(ttl,format='turtle')
            a=next(g.subjects(SKOS.prefLabel,Literal('Root',lang='en')));b=next(g.subjects(SKOS.prefLabel,Literal('Child',lang='en')))
            ka=next(g.objects(a,DCTERMS.identifier));kb=next(g.objects(b,DCTERMS.identifier))
            g.set((a,DCTERMS.identifier,kb));g.set((b,DCTERMS.identifier,ka));g.serialize(destination=ttl,format='turtle')
            with self.assertRaisesRegex(ValueError,'identity'):
                import_ieee(source,root/'second',identity_file=ttl)
            self.assertFalse((root/'second').exists())

if __name__=='__main__':unittest.main()
