import importlib
from pathlib import Path
import tempfile
import unittest


class TreeTests(unittest.TestCase):
    def api(self):
        try:
            return importlib.import_module('kb_vocab_rdf_preview.server')
        except ModuleNotFoundError:
            self.fail('分类树预览尚未实现')

    def test_multiple_parents_and_unreachable_cycles_remain_visible(self):
        api=self.api()
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'data.ttl'
            raw='''@prefix s: <http://www.w3.org/2004/02/skos/core#> .
@prefix e: <https://example.org/> .
e:a a s:Concept; s:prefLabel "A"; s:narrower e:c .
e:b a s:Concept; s:prefLabel "B" .
e:c a s:Concept; s:prefLabel "C"; s:broader e:b .
e:x a s:Concept; s:broader e:y .
e:y a s:Concept; s:broader e:x .
'''
            path.write_text(raw)
            data=api.load_tree(path)
            self.assertIn('https://example.org/c',data['nodes']['https://example.org/a']['children'])
            self.assertIn('https://example.org/c',data['nodes']['https://example.org/b']['children'])
            seen=set(); pending=list(data['roots'])
            while pending:
                node=pending.pop()
                if node not in seen:
                    seen.add(node); pending.extend(data['nodes'][node]['children'])
            self.assertEqual(seen,set(data['nodes']))
            self.assertEqual(path.read_text(),raw)

    def test_xl_labels_and_html_text_are_preserved_safely(self):
        api=self.api()
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'data.ttl'
            path.write_text('''@prefix s: <http://www.w3.org/2004/02/skos/core#> .
@prefix xl: <http://www.w3.org/2008/05/skos-xl#> .
<urn:c> a s:Concept; xl:prefLabel <urn:label> .
<urn:label> a xl:Label; xl:literalForm "</script><img src=x onerror=alert(1)>"@en .
''')
            data=api.load_tree(path)
            self.assertEqual(data['nodes']['urn:c']['label'],'</script><img src=x onerror=alert(1)>')
            html=api.render(data)
            self.assertNotIn('</script><img',html)
            self.assertIn('\\u003c/script',html)

if __name__=='__main__':
    unittest.main()
