import unittest
from rdflib import DCTERMS, RDF, SKOS
from kb_vocab.cognitive_atlas import project_cognitive


def record(identity, kind='concept', relations=()):
    return {'id': identity, 'kind': kind, 'source_url': 'https://example.org/'+identity,
            'detail': {'id': identity, 'name': identity, 'definition_text': 'Definition',
                       'relationships': list(relations), 'concepts': []}}


class CognitiveProjectionTests(unittest.TestCase):
    def test_relation_direction_and_part_whole_are_not_conflated(self):
        data = {'records': [record('a', relations=[{'id': 'b', 'relationship': 'KINDOF', 'direction': 'parent'},
                                                  {'id': 'c', 'relationship': 'PARTOF', 'direction': 'child'}]),
                            record('b', relations=[{'id': 'a', 'relationship': 'KINDOF', 'direction': 'child'}]),
                            record('c'), record('task', 'task')]}
        graph, ledger = project_cognitive(data)
        ids = {str(key): node for node, key in graph.subject_objects(DCTERMS.identifier)}
        self.assertIn((ids['a'], SKOS.broader, ids['b']), graph)
        self.assertIn((ids['c'], DCTERMS.isPartOf, ids['a']), graph)
        self.assertNotIn((ids['c'], SKOS.broader, ids['a']), graph)
        self.assertNotIn((ids['task'], RDF.type, SKOS.Concept), graph)
        again, _ = project_cognitive(data, identities=graph)
        self.assertEqual(set(graph), set(again))

    def test_cycles_self_edges_and_missing_targets_are_held(self):
        data = {'records': [record('a', relations=[{'id': 'a', 'relationship': 'KINDOF', 'direction': 'parent'},
                                                   {'id': 'absent', 'relationship': 'KINDOF', 'direction': 'parent'}])]}
        graph, ledger = project_cognitive(data)
        self.assertEqual(list(graph.triples((None, SKOS.broader, None))), [])
        self.assertEqual(len(ledger['relations']), 2)
        self.assertTrue(all(r['status']=='held' for r in ledger['relations']))

    def test_review_exclusion_is_pinned_and_does_not_resolve_other_holds(self):
        import hashlib, json
        data = {'records': [record('a', relations=[{'id': 'a', 'relationship': 'KINDOF', 'direction': 'parent'},
                                                  {'id': 'missing', 'relationship': 'KINDOF', 'direction': 'parent'}])]}
        digest = hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
        policy = {'id':'review', 'source_data_sha256':digest, 'exclusions':[{'source_id':'a','field':'relationships','index':0,'reason':'self_relation'}]}
        graph, ledger = project_cognitive(data, exclusion_policy=policy)
        self.assertEqual([r['status'] for r in ledger['relations']], ['excluded_by_review','held'])
        _, other = project_cognitive(data, exclusion_policy={**policy,'source_data_sha256':'different'})
        self.assertTrue(all(r['status']=='held' for r in other['relations']))
