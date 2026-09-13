import copy
import hashlib
import json
import unittest
from rdflib.compare import isomorphic
from test_ieee_mapping import entry,sample
from kb_vocab.ieee import project_ieee

class ProjectionPolicyTests(unittest.TestCase):
    def test_only_reviewed_indirect_rt_is_resolved_without_changing_graph(self):
        data=sample()
        data['entries']=[entry('e1','Root','preferred',[('NT','Middle','g1',None),('RT','Leaf','g2',None),('RT','Middle','g3',None)]),
          entry('e2','Middle','preferred',[('BT','Root','g4',None),('NT','Leaf','g5',None),('RT','Root','g6',None)]),
          entry('e3','Leaf','preferred',[('BT','Middle','g7',None),('RT','Root','g8',None)])]
        policy={'id':'test','rule':'exclude_indirect_ancestor_rt','source_sha256':data['source']['sha256'],
          'source_data_sha256':hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()}
        old,_=project_ieee(data)
        new,ledger=project_ieee(data,identities=old,indirect_rt_policy=policy)
        self.assertTrue(isomorphic(old,new))
        excluded=[r for r in ledger['relations'] if r['status']=='excluded_by_policy']
        self.assertEqual({('Root','Leaf'),('Leaf','Root')},{(r['subject'],r['source_relation']['target']) for r in excluded})
        self.assertTrue(all(r['policy_id']=='test' for r in excluded))
        self.assertTrue(any(r['status']=='held' and r['subject']=='Middle' for r in ledger['relations']))
        changed=copy.deepcopy(data);changed['entries'][0]['relations'].append({'predicate':'RT','target':'Root','source_group':'g9','connector_after':None,'fragments':[]})
        _,later=project_ieee(changed,indirect_rt_policy=policy)
        self.assertFalse(any(r['status']=='excluded_by_policy' for r in later['relations']))

if __name__=='__main__':unittest.main()
