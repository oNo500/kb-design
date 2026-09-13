import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import yaml

from kb_sources.download import SourceError
from kb_sources.structure import extract_html, parse_html


class StructureTests(unittest.TestCase):
    def test_inline_formatting_does_not_split_words(self):
        result = parse_html(b'<html><h1>F<span>oundations</span> of Programming</h1><p>A s<b>imple</b> example<br>Next line</p></html>')
        self.assertEqual('Foundations of Programming', result['headings'][0]['text'])
        self.assertEqual('A simple example Next line', result['blocks'][0]['text'])

    def test_headings_lists_and_source_locations_are_preserved(self):
        raw = b'''<html><body><nav><h1>Navigation</h1></nav>
<p class="MsoToc1">TOC duplicate</p>
<h1 id="area">Artificial Intelligence (AI)</h1>
<h3><a name="unit"></a>AI-ML: Machine Learning</h3>
<p>CS Core:</p><ol><li>Models<ol><li>Evaluation</li></ol></li></ol>
<p style="mso-list:l1 level2 lfo1">Word list item</p>
<h2>References</h2><p>Source citation</p></body></html>'''
        result = parse_html(raw)
        hs = result['headings']
        self.assertEqual(['Artificial Intelligence (AI)', 'AI-ML: Machine Learning', 'References'], [h['text'] for h in hs])
        self.assertEqual(hs[0]['id'], hs[1]['parent'])
        self.assertEqual(hs[0]['id'], hs[2]['parent'])
        self.assertEqual('unit', hs[1]['locator']['anchors'][0])
        self.assertEqual(4, hs[1]['locator']['line'])
        items = [b for b in result['blocks'] if b['kind'] == 'list-item']
        self.assertEqual(['Models', 'Evaluation', 'Word list item'], [b['text'] for b in items])
        self.assertEqual([1, 2, 2], [b['list_depth'] for b in items])
        self.assertTrue(all(b['section'] == hs[1]['id'] for b in items))
        self.assertTrue(any(b.get('source_style') == 'mso-list:l1 level2 lfo1' for b in result['blocks']))

    def test_duplicate_anchor_and_headingless_text_are_visible(self):
        r = parse_html(b'<html><h1 id="a">One</h1><h2 id="a">Two</h2></html>')
        self.assertTrue(r['warnings'])
        r = parse_html(b'<html><p>No document headings</p></html>')
        self.assertEqual('No document headings', r['blocks'][0]['text'])
        self.assertTrue(r['warnings'])

    def test_word_list_parent_and_original_marker(self):
        r = parse_html(b'''<h1>Area</h1>
<p style="mso-list:l8 level1 lfo2"><span style="mso-list:Ignore">3. </span>Models</p>
<p style="mso-list:l8 level2 lfo2"><span style="mso-list:Ignore">a. </span>Linear</p>
<p style="mso-list:l8 level1 lfo2"><span style="mso-list:Ignore">4. </span>Evaluation</p>''')
        a,b,c = r['blocks']
        self.assertEqual('a.', b['marker'])
        self.assertEqual(a['id'], b['list_parent'])
        self.assertIsNone(c['list_parent'])
        self.assertEqual('a. Linear', b['text'])

    def test_word_depth_survives_word_list_id_changes(self):
        r = parse_html(b'<h1>Area</h1><p style="mso-list:l1 level1 lfo1">1. Parent</p><p style="mso-list:l2 level2 lfo2">a. Child</p>')
        self.assertEqual(r['blocks'][0]['id'], r['blocks'][1]['list_parent'])

    def test_indented_continuation_does_not_break_word_list(self):
        r = parse_html(b'<h1>Area</h1><p style="margin-left:.25in;mso-list:l1 level1 lfo1">1. Models</p><p style="margin-left:.25in">One of these:</p><p style="margin-left:.5in;mso-list:l2 level2 lfo2">a. Actor</p>')
        self.assertEqual(r['blocks'][0]['id'], r['blocks'][2]['list_parent'])

    def test_printed_parent_before_word_children(self):
        r = parse_html(b'<h1>Area</h1><p class="MsoNormal">7. Techniques</p><p style="mso-list:l2 level2 lfo2">a. Research</p>')
        self.assertEqual(r['blocks'][0]['id'],r['blocks'][1]['list_parent'])

    def test_table_spans_do_not_duplicate_or_lose_content(self):
        r = parse_html(b'''<h1>Table</h1><table><tr><th rowspan="2">Area</th>
<th colspan="2">Hours</th></tr><tr><td>Core</td><td>Optional</td></tr>
<tr><td><p>AI</p></td><td>3</td><td><a href="units/ai">6</a></td></tr></table><p>After</p>''')
        table = r['tables'][0]
        self.assertEqual((3,3), (table['rows'],table['columns']))
        self.assertEqual((2,1), (table['cells'][0]['rowspan'],table['cells'][0]['colspan']))
        self.assertEqual(['Area','Hours','Core','Optional','AI','3','6'], [c['text'] for c in table['cells']])
        self.assertEqual('units/ai', table['cells'][-1]['links'][0]['href'])
        self.assertEqual(['After'], [b['text'] for b in r['blocks']])

    def test_lists_and_paragraph_boundaries_survive_inside_cells(self):
        r = parse_html(b'<h1>Area</h1><table><tr><td><p>First point</p><p>Second point</p><p style="mso-list:l1 level1 lfo1">2. Object-oriented design</p><p style="mso-list:l1 level2 lfo1">a. Decomposition</p></td></tr></table>')
        cell=r['tables'][0]['cells'][0]
        self.assertIn('First point\nSecond point',cell['text'])
        parts=cell['content']['blocks']
        self.assertEqual(parts[2]['id'],parts[3]['list_parent'])

    def test_native_lists_keep_parent_and_links_without_parent_text_duplication(self):
        r = parse_html(b'<h1>A</h1><ol start="4"><li><a href="entry/a">Alpha</a><ul><li>Child</li></ul></li><li>Beta</li></ol>')
        a,b,c=r['blocks']
        self.assertEqual('4.', a['marker'])
        self.assertEqual('5.', c['marker'])
        self.assertEqual(a['id'], b['list_parent'])
        self.assertEqual('Alpha', a['text'])
        self.assertEqual('entry/a', a['links'][0]['href'])

    def test_source_body_selector_keeps_only_book_content(self):
        r = parse_html(b'<h1>Account</h1><div id="openbook-html"><div class="page-html"><h1>Summary</h1><p>Book</p></div></div><footer>Site</footer>', profile='nap')
        self.assertEqual(['Summary'], [h['text'] for h in r['headings']])
        self.assertEqual(['Book'], [b['text'] for b in r['blocks']])

    def make_snapshot(self, root):
        html = b'<html><h1 id="a">Area</h1><h2>Unit</h2><p>Topic text</p></html>'
        spec = {'schema_version': 1, 'id': 'sample', 'title': 'Sample', 'version': '1',
                'files': [{'id': 'report', 'filename': 'report.html', 'format': 'html', 'url': 'https://example.org/report.html'}]}
        source = yaml.safe_dump(spec).encode()
        receipt = {'schema_version': 1, 'source': {'id': 'sample', 'title': 'Sample', 'requested_version': '1'},
                   'acquired_at': '2026-09-12T00:00:00Z', 'request_sha256': hashlib.sha256(source).hexdigest(),
                   'tool': {'name': 'kb-sources', 'version': '0.1.0'},
                   'files': [{**spec['files'][0], 'final_url': spec['files'][0]['url'],
                              'sha256': hashlib.sha256(html).hexdigest(), 'size': len(html), 'content_type': 'text/html'}]}
        raw = json.dumps(receipt).encode()
        snap = root / hashlib.sha256(raw).hexdigest();snap.mkdir()
        (snap / 'receipt.json').write_bytes(raw);(snap / 'source.yaml').write_bytes(source);(snap / 'report.html').write_bytes(html)
        return snap

    def test_extraction_is_repeatable_and_does_not_overwrite_or_trust_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp);snap = self.make_snapshot(root)
            first, second = root / 'first', root / 'second'
            extract_html(snap, 'report', first);extract_html(snap, 'report', second)
            a = json.loads((first/'structure.json').read_text())
            b = json.loads((second/'structure.json').read_text())
            self.assertEqual(a, b)
            self.assertEqual(snap.name, a['source']['snapshot_id'])
            with self.assertRaises(SourceError):extract_html(snap, 'report', first)
            with self.assertRaises(SourceError):extract_html(snap, 'report', snap / 'derived')
            (snap/'report.html').write_text('<html>altered</html>')
            with self.assertRaises(SourceError):extract_html(snap, 'report', root/'bad')
            self.assertFalse((root/'bad').exists())


if __name__ == '__main__':unittest.main()
