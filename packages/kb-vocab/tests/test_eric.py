"""Protect status, composition and relationship meaning during ERIC conversion."""
import io
import unittest
import zipfile
from rdflib import RDF, SKOS, Literal
from kb_vocab.eric import project_eric


def xml(*terms):
    return ('<Nstein><Terms>'+''.join(terms)+'</Terms></Nstein>').encode()


def term(name, kind='Main', relations='', attributes=''):
    return f'<Term><Name>{name}</Name><Attributes><Attribute name="RecType">{kind}</Attribute>{attributes}</Attributes><Relationships>{relations}</Relationships></Term>'


def rel(kind, *targets):
    return '<Relationship type="'+kind+'">'+''.join('<Is>'+t+'</Is>' for t in targets)+'</Relationship>'


class EricTests(unittest.TestCase):
    def test_status_and_composite_do_not_become_labels(self):
        g,r,l=project_eric(xml(term('A'),term('B'),term('Alias','Synonym',rel('U','A')),term('Both','Synonym',rel('U','A','B')),term('Old','Dead'),term('Composite','Synonym',rel('U','A'),'<Attribute name="USEAND">B</Attribute>')), {'sha256':'test'})
        self.assertEqual(2,len(set(g.subjects(RDF.type,SKOS.Concept))))
        self.assertEqual({Literal('Alias',lang='en')},set(g.objects(None,SKOS.altLabel)))
        self.assertEqual(6,len(l['records']))
        self.assertEqual('isolated_multi_target_use',l['records'][3]['disposition'])
        self.assertEqual('retired_record',l['records'][4]['disposition'])
        self.assertEqual('isolated_multi_target_use',l['records'][5]['disposition'])

    def test_directions_and_s27_isolation(self):
        g,r,l=project_eric(xml(term('A',relations=rel('BT','B')+rel('RT','C')),term('B',relations=rel('BT','C')+rel('NT','A')),term('C')), {'sha256':'test'})
        nodes={str(label):node for node,label in g.subject_objects(SKOS.prefLabel)}
        self.assertIn((nodes['A'],SKOS.broader,nodes['B']),g)
        self.assertEqual(2,len(list(g.triples((None,SKOS.broader,None)))))
        self.assertFalse(list(g.triples((None,SKOS.related,None))))
        self.assertEqual(1,r['s27_isolated_pairs'])

    def test_missing_target_unknown_status_and_identity(self):
        raw=xml(term('A',relations=rel('BT','Missing')),term('Unknown','Unexpected'))
        g,r,l=project_eric(raw,{'sha256':'test'})
        g2,_,_=project_eric(raw,{'sha256':'test'})
        self.assertEqual(set(g),set(g2))
        self.assertEqual(1,len(set(g.subjects(RDF.type,SKOS.Concept))))
        self.assertFalse(list(g.objects(None,SKOS.broader)))
        self.assertTrue(l['isolated_relations'])

    def test_reject_entities_duplicates_and_ambiguous_archive(self):
        with self.assertRaises(ValueError):
            project_eric(b'<!DOCTYPE x [<!ENTITY e "boom">]><Nstein><Terms/></Nstein>',{})
        with self.assertRaises(ValueError):
            project_eric(xml(term('A'),term('A')), {})
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w') as z:
            z.writestr('a.xml',xml(term('A')));z.writestr('b.xml',xml(term('B')))
        with self.assertRaises(ValueError):
            project_eric(stream.getvalue(),{})
