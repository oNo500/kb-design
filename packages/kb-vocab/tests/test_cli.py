import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from kb_vocab.cli import main

class LocalTurtleTests(unittest.TestCase):
    def test_relative_concept_iri_uses_document_location(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'vocab.ttl'
            path.write_text('@prefix skos: <http://www.w3.org/2004/02/skos/core#> . <#a> a skos:Concept; skos:prefLabel "A"@en .')
            output=io.StringIO()
            with contextlib.redirect_stdout(output),contextlib.redirect_stderr(io.StringIO()):
                status=main(['show',str(path),path.as_uri()+'#a'])
            self.assertEqual(0,status)
            self.assertEqual(path.as_uri()+'#a',json.loads(output.getvalue())['id'])

if __name__=='__main__':unittest.main()
