"""Projection tests: prevent source loss and unsupported semantic changes."""

import unittest

from rdflib import BNode, Graph, Literal, Namespace
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD

from kb_vocab.normalization import normalize_sources

EX = Namespace("https://example.org/")
ISO = Namespace("http://purl.org/iso25964/skos-thes#")


class NormalizationTests(unittest.TestCase):
    def normalize(self, triples):
        graph = Graph()
        for triple in triples:
            graph.add(triple)
        before = set(graph)
        output, changes, summary = normalize_sources(
            {"fixture": {"graph": graph, "path": "fixture.ttl", "sha256": "abc"}}
        )
        self.assertEqual(set(graph), before)
        counts = summary["by_source"]["fixture"]
        self.assertEqual(sum(counts[k] for k in ("copied", "source_only", "filtered", "canonicalized")), len(graph))
        return output, changes, summary

    def test_language_filter_preserves_identity_untagged_values_and_metadata(self):
        triples = [(EX.a, RDF.type, SKOS.Concept)]
        kept = [Literal("Name", lang="EN-us"), Literal("名稱", lang="zh-Hant"), Literal("untagged")]
        triples += [(EX.a, SKOS.prefLabel, value) for value in kept]
        removed = Literal("nom", lang="fr")
        triples += [(EX.a, SKOS.prefLabel, removed), (EX.b, RDF.type, SKOS.Concept),
                    (EX.b, SKOS.prefLabel, Literal("mot", lang="fr")),
                    (EX.a, DCTERMS.identifier, Literal("01")),
                    (EX.a, DCTERMS.created, Literal("2020-01-01", datatype=XSD.date)),
                    (EX.a, DCTERMS.source, EX.source)]
        out, changes, summary = self.normalize(triples)
        expected = {triple for triple in triples if not (isinstance(triple[2], Literal) and triple[2].language == "fr")}
        self.assertEqual(set(out), expected)
        self.assertEqual(summary["filtered_languages"], {"fr": 2})
        change = next(c for c in changes if c["subject"] == str(EX.a))
        self.assertEqual(change["object"], removed.n3())
        self.assertEqual(change["action"], "filtered")

    def test_scheme_archive_preserves_collections_tasks_and_shared_notes(self):
        note = BNode("shared")
        source_only = [(EX.scheme, RDF.type, SKOS.ConceptScheme),
                       (EX.scheme, SKOS.scopeNote, note),
                       (EX.a, SKOS.inScheme, EX.scheme),
                       (EX.a, SKOS.topConceptOf, EX.scheme),
                       (EX.scheme, SKOS.hasTopConcept, EX.a)]
        kept = [(EX.a, RDF.type, SKOS.Concept), (EX.a, SKOS.scopeNote, note),
                (note, RDF.value, Literal("A note", lang="en")),
                (EX.collection, RDF.type, SKOS.Collection), (EX.collection, SKOS.member, EX.a),
                (EX.task, RDF.type, RDFS.Resource), (EX.task, DCTERMS.type, Literal("task")),
                (EX.task, RDFS.label, Literal("Task", lang="en")),
                (EX.task, DCTERMS.type, Literal("concept"))]
        out, changes, summary = self.normalize(source_only + kept + [(EX.a, DCTERMS.type, Literal("concept"))])
        self.assertEqual(set(out), set(kept))
        self.assertEqual(sum(c["action"] == "source_only" for c in changes), len(source_only))
        self.assertEqual(summary["by_source"]["fixture"]["canonicalized"], 1)

    def test_inverse_relations_materialized_without_losing_originals(self):
        originals = [(node, RDF.type, SKOS.Concept) for node in (EX.a, EX.b, EX.c)]
        originals += [(EX.a, SKOS.narrower, EX.b), (EX.c, SKOS.broader, EX.a),
                      (EX.b, SKOS.related, EX.c), (EX.group, ISO.subGroup, EX.subgroup),
                      (EX.b, DCTERMS.replaces, EX.c),
                      (EX.document, DCTERMS.replaces, EX.oldDocument)]
        out, changes, summary = self.normalize(originals)
        derived = {(EX.b, SKOS.broader, EX.a), (EX.a, SKOS.narrower, EX.c),
                   (EX.c, SKOS.related, EX.b), (EX.subgroup, ISO.superGroup, EX.group),
                   (EX.c, DCTERMS.isReplacedBy, EX.b)}
        self.assertEqual(set(out), set(originals) | derived)
        additions = [c for c in changes if c["action"] == "derived"]
        self.assertEqual(len(additions), len(derived))
        self.assertTrue(all(c["supporting_original"]["source"] == "fixture" for c in additions))

    def test_overlapping_sources_account_for_each_original_without_duplicate_derivation(self):
        graph = Graph()
        graph.add((EX.a, SKOS.related, EX.b))
        sources = {name: {"graph": graph, "path": name, "sha256": name} for name in ("a", "b")}
        out, changes, summary = normalize_sources(sources)
        self.assertEqual(summary["input_triples"], 2)
        self.assertEqual(summary["output_triples"], 2)
        self.assertEqual(summary["derived_triples"], 1)


if __name__ == "__main__":
    unittest.main()
