import unittest


def line(text,x=0,style='regular',page=3,column=1,y=80):
    return {'text':text,'x':x,'style':style,'locator':{'page':page,'column':column,'bbox':[72+x,y,260,y+10]}}


class IEEEThesaurusTests(unittest.TestCase):
    def test_cross_column_and_page_relationship_continuations(self):
        from kb_sources.ieee_thesaurus import parse_lines
        lines=[line('Machine learning',style='preferred'),line('NT: Convolutional',45,y=92),
            line('neural networks',y=104),line('Deep learning',91,page=3,column=2),
            line('Reinforcement learning',91,page=4,column=1),line('ML',style='nonpreferred',page=4,y=110),
            line('USE: Machine learning',45,page=4,y=122)]
        r=parse_lines(lines);a,b=r['entries']
        self.assertEqual('Machine learning',a['name'])
        self.assertEqual(['Convolutional neural networks','Deep learning','Reinforcement learning'],[x['target'] for x in a['relations']])
        self.assertEqual([3,3],[x['locator']['page'] for x in a['relations'][0]['fragments']])
        self.assertEqual('nonpreferred',b['form'])
        self.assertEqual('USE',b['relations'][0]['predicate'])
        self.assertFalse(r['unassigned'])

    def test_wrapped_title_and_unexpected_lines_are_retained(self):
        from kb_sources.ieee_thesaurus import parse_lines
        r=parse_lines([line('orphan continuation'),line('Long concept',style='preferred'),
                       line('name',style='preferred',y=92),line('BT: Root',45,y=104),line('ZZ: Unexpected',45,y=116)])
        self.assertEqual('Long concept name',r['entries'][0]['name'])
        self.assertEqual(2,len(r['unassigned']))
        self.assertEqual('Root',r['entries'][0]['relations'][0]['target'])

    def test_source_and_group_is_not_flattened_into_independent_synonyms(self):
        from kb_sources.ieee_thesaurus import parse_lines
        r=parse_lines([line('Acoustic metamaterials',style='nonpreferred'),line('USE: Acoustic materials AND',45),line('Metamaterials',91)])
        a,b=r['entries'][0]['relations']
        self.assertEqual('Acoustic materials',a['target'])
        self.assertEqual('Acoustic materials AND',a['raw_target'])
        self.assertEqual('AND',a['connector_after'])
        self.assertEqual(a['source_group'],b['source_group'])

    def test_hyphen_wrap_does_not_insert_space_or_drop_hyphen(self):
        from kb_sources.ieee_thesaurus import parse_lines
        r=parse_lines([line('BPR',style='nonpreferred'),line('USE: Business process re-',45),line('engineering')])
        relation=r['entries'][0]['relations'][0]
        self.assertEqual('Business process re-engineering',relation['target'])
        self.assertEqual('engineering',relation['fragments'][1]['text'])

    def test_diagnostics_do_not_invent_missing_inverse_relations(self):
        from kb_sources.ieee_thesaurus import parse_lines, diagnose
        r=parse_lines([line('A',style='preferred'),line('BT: B',45),line('B',style='preferred',y=140),line('RT: Missing',45,y=152)])
        checks=diagnose(r['entries'])
        self.assertTrue(checks['missing_inverse'])
        self.assertTrue(checks['unresolved_targets'])
        self.assertEqual(1,len(r['entries'][1]['relations']))

if __name__=='__main__':unittest.main()
