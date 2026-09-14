"""Selection prunes one source without destroying its snapshot or another source."""
import unittest
from rdflib import Graph,RDF,SKOS,URIRef


class SelectionTests(unittest.TestCase):
    def test_descendants_exclude_ancestors_related_and_preserve_shared_identity(self):
        from kb_vocab.selection import select_sources
        a=Graph().parse(data='''@prefix s:<http://www.w3.org/2004/02/skos/core#>.
<urn:parent> a s:Concept. <urn:root> a s:Concept;s:broader <urn:parent>;s:related <urn:related>.
<urn:child> a s:Concept;s:broader <urn:root>;s:narrower <urn:grandchild>.
<urn:grandchild> a s:Concept. <urn:related> a s:Concept.''',format='turtle')
        b=Graph().parse(data='''@prefix s:<http://www.w3.org/2004/02/skos/core#>. <urn:related> a s:Concept. <urn:other> a s:Concept;s:related <urn:parent>.''',format='turtle')
        sources={'a':{'graph':a,'sha256':'a','selection':{'roots':['urn:root'],'descendants':True}},'b':{'graph':b,'sha256':'b'}}
        before=set(a)
        selected,report=select_sources(sources)
        self.assertEqual(set(a),before)
        self.assertEqual(set(selected['a']['graph'].subjects(RDF.type,SKOS.Concept)),{URIRef('urn:root'),URIRef('urn:child'),URIRef('urn:grandchild')})
        self.assertIn((URIRef('urn:related'),RDF.type,SKOS.Concept),selected['b']['graph'])
        self.assertNotIn((URIRef('urn:other'),SKOS.related,URIRef('urn:parent')),selected['b']['graph'])
        self.assertEqual(report['excluded_concepts'],['urn:parent'])
        sources['a']['selection']['roots']=['urn:missing']
        with self.assertRaisesRegex(ValueError,'root'):select_sources(sources)
