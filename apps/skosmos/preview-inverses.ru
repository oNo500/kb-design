PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
# Materialize standard SKOS inverses within the current preview graph only.
INSERT { GRAPH <urn:kb-design:preview:current> { ?b skos:narrower ?a } }
WHERE { GRAPH <urn:kb-design:preview:current> { ?a skos:broader ?b } } ;
INSERT { GRAPH <urn:kb-design:preview:current> { ?b skos:broader ?a } }
WHERE { GRAPH <urn:kb-design:preview:current> { ?a skos:narrower ?b } } ;
INSERT { GRAPH <urn:kb-design:preview:current> { ?scheme skos:hasTopConcept ?concept } }
WHERE { GRAPH <urn:kb-design:preview:current> { ?concept skos:topConceptOf ?scheme } } ;
INSERT { GRAPH <urn:kb-design:preview:current> { ?concept skos:topConceptOf ?scheme } }
WHERE { GRAPH <urn:kb-design:preview:current> { ?scheme skos:hasTopConcept ?concept } }
