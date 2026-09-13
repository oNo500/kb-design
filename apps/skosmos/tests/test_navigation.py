import importlib.util
from pathlib import Path
import unittest
from rdflib import Graph
spec=importlib.util.spec_from_file_location('navigation',Path(__file__).parents[1]/'build-navigation.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class NavigationTests(unittest.TestCase):
    def test_cycles_and_disconnected_members_are_not_lost_or_written_as_tops(self):
        g=Graph().parse(data='''@prefix s: <http://www.w3.org/2004/02/skos/core#> .
        <urn:scheme> a s:ConceptScheme ; s:hasTopConcept <urn:root> .
        <urn:root> a s:Concept ; s:inScheme <urn:scheme> .
        <urn:a> a s:Concept ; s:inScheme <urn:scheme> ; s:broader <urn:b> .
        <urn:b> a s:Concept ; s:inScheme <urn:scheme> ; s:broader <urn:a> .
        ''',format='turtle')
        before=set(g); result=module.build_navigation(g); s=result['schemes']['urn:scheme']
        self.assertEqual(s['entries'],['urn:root']);self.assertEqual(s['unconnected'],['urn:a','urn:b'])
        self.assertEqual(set(g),before)
    def test_browse_entries_are_scoped_and_keep_multiple_parents(self):
        g=Graph().parse(data='''@prefix s: <http://www.w3.org/2004/02/skos/core#> .
        <urn:s> a s:ConceptScheme .
        <urn:outside> a s:Concept .
        <urn:a> a s:Concept ; s:inScheme <urn:s> ; s:broader <urn:outside> .
        <urn:b> a s:Concept ; s:inScheme <urn:s> .
        <urn:c> a s:Concept ; s:inScheme <urn:s> ; s:broader <urn:a>, <urn:b> .
        ''',format='turtle')
        result=module.build_navigation(g);s=result['schemes']['urn:s']
        self.assertEqual(s['entries'],['urn:a','urn:b']);self.assertFalse(s['explicit'])
        self.assertEqual(result['nodes']['urn:c']['parents'],['urn:a','urn:b'])
if __name__=='__main__': unittest.main()
