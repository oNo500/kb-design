from pathlib import Path
import unittest
from kb_sources.download import SourceError

FIXTURE = Path(__file__).parent / 'fixtures/layout.pdf'

class PdfStructureTests(unittest.TestCase):
    def test_columns_tables_lists_and_provenance(self):
        from kb_sources.pdf import parse_pdf
        r = parse_pdf(FIXTURE.read_bytes())
        text = '\n'.join(b['text'] for b in r['blocks'])
        self.assertLess(text.index('Left second'), text.index('Right first'))
        self.assertNotIn('Repeated running header', text)
        self.assertTrue(any('Repeated running header' in p['text'] for p in r['pages']))
        parent = next(b for b in r['blocks'] if b['text'].startswith('1. Parent'))
        child = next(b for b in r['blocks'] if b['text'].startswith('a. Child'))
        self.assertEqual(parent['id'], child['list_parent'])
        self.assertIn('continuation line', child['text'])
        table = r['tables'][0]
        self.assertEqual(['Code','Meaning','03B05','Logic'], [c['text'] for c in table['cells']])
        self.assertNotIn('03B05', text)
        self.assertEqual(['Topic area','Next area'], [h['text'] for h in r['headings']])
        self.assertEqual(2, len(r['pages']))
        self.assertTrue(all('bbox' in b['locator'] and b['locator']['page'] for b in r['blocks']))
        self.assertTrue(any(l['href']=='https://example.org/source' for b in r['blocks'] for l in b['links']))

    def test_staggered_msc_columns_keep_codes_separate(self):
        from kb_sources.pdf import msc_index_lines
        words=[]
        for x,y,text in [(40,160,'19'),(60,160,'K-theory'),(40,177,'20'),(60,177,'Group'),(330,161,'68'),(350,161,'Computing'),(330,180,'70'),(350,180,'Mechanics')]:
            words.append({'x0':x,'x1':x+len(text)*4,'top':y,'bottom':y+10,'text':text,'size':10,'fontname':'Regular'})
        self.assertEqual(['19 K-theory','20 Group','68 Computing','70 Mechanics'], [l['text'] for l in msc_index_lines(words,600)])

    def test_text_in_table_grid_gap_is_not_dropped(self):
        from kb_sources.pdf import parse_pdf
        r = parse_pdf((FIXTURE.parent/'incomplete-grid.pdf').read_bytes())
        text = ' '.join(b['text'] for b in r['blocks']) + ' '.join(c['text'] for t in r['tables'] for c in t['cells'])
        self.assertIn('Gap text must survive', text)

    def test_source_styles_keep_ku_and_tekom_item_boundaries(self):
        from kb_sources.pdf import parse_pdf
        raw=(FIXTURE.parent/'source-styles.pdf').read_bytes()
        cs=parse_pdf(raw,'cs2023')
        ku=next((h for h in cs['headings'] if h['text']=='AI-Search: Search'),None)
        self.assertIsNotNone(ku)
        self.assertEqual(3,ku['level'])
        tek=parse_pdf(raw,'tekom-teaching-2018')
        item=next(b for b in tek['blocks'] if b['text'].startswith('Methods of improving'))
        self.assertIn('devices, safety notes',item['text'])
        self.assertNotIn('Ressource',item['text'])
        self.assertTrue(any(b['text'].startswith('Ressource') for b in tek['blocks']))
        self.assertTrue(tek['pages'][1]['markers'])

    def test_malformed_pdf_is_not_a_successful_empty_document(self):
        from kb_sources.pdf import parse_pdf
        with self.assertRaises(SourceError):parse_pdf(b'%PDF-1.7\nnot a document\n%%EOF')

if __name__ == '__main__':unittest.main()
