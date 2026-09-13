import tempfile
import unittest
from pathlib import Path

from kb_sources.ieee_reference import load_reference


class IEEEReferenceTests(unittest.TestCase):
    def load(self, taxonomy, csv='subject,predicate,object\nChild,BT,Root\n'):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'terms.csv').write_text(csv, encoding='utf-8')
            (root / 'tree.txt').write_text(taxonomy, encoding='utf-8')
            return load_reference(root / 'terms.csv', root / 'tree.txt')

    def test_direct_parent_and_multiple_occurrences_are_preserved(self):
        result = self.load('Root\n....Branch\n........Shared\n....Other\n........Shared\n')
        nodes = result['taxonomy']['occurrences']
        self.assertEqual([None, nodes[0]['id'], nodes[1]['id'], nodes[0]['id'], nodes[3]['id']],
                         [node['parent'] for node in nodes])
        self.assertEqual([0, 1, 2, 1, 2], [node['depth'] for node in nodes])
        self.assertEqual('Shared', nodes[2]['label'])
        self.assertEqual('Shared', nodes[4]['label'])
        self.assertNotEqual(nodes[2]['id'], nodes[4]['id'])

    def test_csv_preserves_names_predicates_and_physical_line_locations(self):
        result = self.load('Root\n', 'subject,predicate,object\n"Multi\nline",UF,"A,  B"\nChild,BT,Root\n')
        rows = result['thesaurus']['relations']
        self.assertEqual(('Multi\nline', 'UF', 'A,  B', 2, 3),
                         tuple(rows[0][k] for k in ('subject', 'predicate', 'object', 'line', 'end_line')))
        self.assertEqual(4, rows[1]['line'])

    def test_invalid_depth_does_not_invent_missing_parent(self):
        with self.assertRaisesRegex(ValueError, 'line 2'):
            self.load('Root\n........Skipped\n')


if __name__ == '__main__':
    unittest.main()
