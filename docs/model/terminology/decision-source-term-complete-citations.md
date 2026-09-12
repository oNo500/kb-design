---
id: decision-source-term-complete-citations
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: '2026-09-06'
level: L3
scope: 51个术语引证来源的完整实体及精确版本字段；不新增来源用途
supersedes: []
answers:
- question: Q01
  resolution: recommended
  patches:
  - identity: entities/gruber-official
    field: record
    value:
      id: gruber-official
      label:
        en: Ontology
      kind: publication
      version: '2008'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://tomgruber.org/writing/definition-of-ontology/
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: gruber-official
          locator: 页面正文书目信息：Tom Gruber (2008), Ontology；正文说明其更新 1993 ontology definition
          checked: '2026-09-06'
        kind:
        - entity: gruber-official
          locator: 页面正文书目信息：Tom Gruber (2008), Ontology；正文说明其更新 1993 ontology definition
          checked: '2026-09-06'
        urls:
        - entity: gruber-official
          locator: 页面正文书目信息：Tom Gruber (2008), Ontology；正文说明其更新 1993 ontology definition
          checked: '2026-09-06'
        version:
        - entity: gruber-official
          locator: 页面正文书目信息：Tom Gruber (2008), Ontology；正文说明其更新 1993 ontology definition
          checked: '2026-09-06'
      watch:
      - locator: https://tomgruber.org/writing/definition-of-ontology/
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/hogan-paper
    field: record
    value:
      id: hogan-paper
      label:
        en: Knowledge Graphs
      kind: publication
      version: arXiv v6
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: full_text
        url: https://arxiv.org/pdf/2003.02320v6
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: hogan-paper
          locator: https://export.arxiv.org/api/query?id_list=2003.02320；entry title Knowledge Graphs；entry id 指向 2003.02320v6
          checked: '2026-09-06'
        kind:
        - entity: hogan-paper
          locator: https://export.arxiv.org/api/query?id_list=2003.02320；arXiv entry、authors、journal_ref 与 DOI
          checked: '2026-09-06'
        urls:
        - entity: hogan-paper
          locator: https://export.arxiv.org/api/query?id_list=2003.02320；PDF link https://arxiv.org/pdf/2003.02320v6
          checked: '2026-09-06'
        version:
        - entity: hogan-paper
          locator: https://export.arxiv.org/api/query?id_list=2003.02320；entry id 2003.02320v6；updated 2021-09-11T21:36:53Z；abs
            submission history v6
          checked: '2026-09-06'
      watch:
      - locator: https://arxiv.org/pdf/2003.02320v6
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/rdf11
    field: record
    value:
      id: rdf11
      label:
        en: RDF 1.1 Concepts and Abstract Syntax
      kind: standard
      version: '2014-02-25'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.w3.org/TR/rdf11-concepts/
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: rdf11
          locator: 文档头：RDF 1.1 Concepts and Abstract Syntax；W3C Recommendation 25 February 2014；版本化 URI /TR/2014/REC-rdf11-concepts-20140225/
          checked: '2026-09-06'
        kind:
        - entity: rdf11
          locator: 文档头：RDF 1.1 Concepts and Abstract Syntax；W3C Recommendation 25 February 2014；版本化 URI /TR/2014/REC-rdf11-concepts-20140225/
          checked: '2026-09-06'
        urls:
        - entity: rdf11
          locator: 文档头：RDF 1.1 Concepts and Abstract Syntax；W3C Recommendation 25 February 2014；版本化 URI /TR/2014/REC-rdf11-concepts-20140225/
          checked: '2026-09-06'
        version:
        - entity: rdf11
          locator: 文档头：RDF 1.1 Concepts and Abstract Syntax；W3C Recommendation 25 February 2014；版本化 URI /TR/2014/REC-rdf11-concepts-20140225/
          checked: '2026-09-06'
      watch:
      - locator: https://www.w3.org/TR/rdf11-concepts/
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/rdfs11
    field: record
    value:
      id: rdfs11
      label:
        en: RDF Schema 1.1
      kind: standard
      version: '2014-02-25'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.w3.org/TR/rdf-schema/
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: rdfs11
          locator: 文档头：RDF Schema 1.1；版本化 URI /TR/2014/REC-rdf-schema-20140225/
          checked: '2026-09-06'
        kind:
        - entity: rdfs11
          locator: 文档头：RDF Schema 1.1；版本化 URI /TR/2014/REC-rdf-schema-20140225/
          checked: '2026-09-06'
        urls:
        - entity: rdfs11
          locator: 文档头：RDF Schema 1.1；版本化 URI /TR/2014/REC-rdf-schema-20140225/
          checked: '2026-09-06'
        version:
        - entity: rdfs11
          locator: 文档头：RDF Schema 1.1；版本化 URI /TR/2014/REC-rdf-schema-20140225/
          checked: '2026-09-06'
      watch:
      - locator: https://www.w3.org/TR/rdf-schema/
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/owl2
    field: record
    value:
      id: owl2
      label:
        en: OWL 2 Web Ontology Language Document Overview (Second Edition)
      kind: standard
      version: '2012-12-11'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.w3.org/TR/owl2-overview/
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: owl2
          locator: 文档头：OWL 2 Web Ontology Language Document Overview (Second Edition)；W3C Recommendation 11 December 2012
          checked: '2026-09-06'
        kind:
        - entity: owl2
          locator: 文档头：OWL 2 Web Ontology Language Document Overview (Second Edition)；W3C Recommendation 11 December 2012
          checked: '2026-09-06'
        urls:
        - entity: owl2
          locator: 文档头：OWL 2 Web Ontology Language Document Overview (Second Edition)；W3C Recommendation 11 December 2012
          checked: '2026-09-06'
        version:
        - entity: owl2
          locator: 文档头：OWL 2 Web Ontology Language Document Overview (Second Edition)；W3C Recommendation 11 December 2012
          checked: '2026-09-06'
      watch:
      - locator: https://www.w3.org/TR/owl2-overview/
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/sparql11
    field: record
    value:
      id: sparql11
      label:
        en: SPARQL 1.1 Query Language
      kind: standard
      version: '2013-03-21'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.w3.org/TR/sparql11-query/
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: sparql11
          locator: 文档头：SPARQL 1.1 Query Language；W3C Recommendation 21 March 2013
          checked: '2026-09-06'
        kind:
        - entity: sparql11
          locator: 文档头：SPARQL 1.1 Query Language；W3C Recommendation 21 March 2013
          checked: '2026-09-06'
        urls:
        - entity: sparql11
          locator: 文档头：SPARQL 1.1 Query Language；W3C Recommendation 21 March 2013
          checked: '2026-09-06'
        version:
        - entity: sparql11
          locator: 文档头：SPARQL 1.1 Query Language；W3C Recommendation 21 March 2013
          checked: '2026-09-06'
      watch:
      - locator: https://www.w3.org/TR/sparql11-query/
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/dcmi-metadata-terms
    field: record
    value:
      id: dcmi-metadata-terms
      label:
        en: DCMI Metadata Terms
      kind: standard
      version: '2020-01-20'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: dcmi-metadata-terms
          locator: 文档头：DCMI Metadata Terms；Date Issued 2020-01-20；DCMI Recommendation
          checked: '2026-09-06'
        kind:
        - entity: dcmi-metadata-terms
          locator: 文档头：DCMI Metadata Terms；Date Issued 2020-01-20；DCMI Recommendation
          checked: '2026-09-06'
        urls:
        - entity: dcmi-metadata-terms
          locator: 文档头：DCMI Metadata Terms；Date Issued 2020-01-20；DCMI Recommendation
          checked: '2026-09-06'
        version:
        - entity: dcmi-metadata-terms
          locator: 文档头：DCMI Metadata Terms；Date Issued 2020-01-20；DCMI Recommendation
          checked: '2026-09-06'
      watch:
      - locator: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/dcmi-singapore-framework
    field: record
    value:
      id: dcmi-singapore-framework
      label:
        en: The Singapore Framework for Dublin Core™ Application Profiles
      kind: publication
      version: '2008-01-14'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.dublincore.org/specifications/dublin-core/singapore-framework/
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: dcmi-singapore-framework
          locator: 文档头：The Singapore Framework for Dublin Core™ Application Profiles；Date Issued 2008-01-14；docs/references/dcmi-application-profiles.md
            已核状态为 past、note
          checked: '2026-09-06'
        kind:
        - entity: dcmi-singapore-framework
          locator: 文档头：The Singapore Framework for Dublin Core™ Application Profiles；Date Issued 2008-01-14；docs/references/dcmi-application-profiles.md
            已核状态为 past、note
          checked: '2026-09-06'
        urls:
        - entity: dcmi-singapore-framework
          locator: 文档头：The Singapore Framework for Dublin Core™ Application Profiles；Date Issued 2008-01-14；docs/references/dcmi-application-profiles.md
            已核状态为 past、note
          checked: '2026-09-06'
        version:
        - entity: dcmi-singapore-framework
          locator: 文档头：The Singapore Framework for Dublin Core™ Application Profiles；Date Issued 2008-01-14；docs/references/dcmi-application-profiles.md
            已核状态为 past、note
          checked: '2026-09-06'
      watch:
      - locator: https://www.dublincore.org/specifications/dublin-core/singapore-framework/
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/ahrens-zettelkasten-interview
    field: record
    value:
      id: ahrens-zettelkasten-interview
      label:
        en: 'Zettelkasten "Super" Notes: with Dr Sönke Ahrens'
      kind: publication
      version: null
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://examstudyexpert.com/zettelkasten/
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: ahrens-zettelkasten-interview
          locator: 页面标题；公开播客访谈逐字稿 L91-L106；work/reviews/2026-09-06-term-ahrens-evidence.json
          checked: '2026-09-06'
        kind:
        - entity: ahrens-zettelkasten-interview
          locator: 页面标题；公开播客访谈逐字稿 L91-L106；work/reviews/2026-09-06-term-ahrens-evidence.json
          checked: '2026-09-06'
        urls:
        - entity: ahrens-zettelkasten-interview
          locator: 页面标题；公开播客访谈逐字稿 L91-L106；work/reviews/2026-09-06-term-ahrens-evidence.json
          checked: '2026-09-06'
      watch:
      - locator: https://examstudyexpert.com/zettelkasten/
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/iso-15489-1
    field: record
    value:
      id: iso-15489-1
      label:
        en: 'Information and documentation — Records management — Part 1: Concepts and principles'
      kind: standard
      version: '2016'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://www.iso.org/standard/62542.html
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: iso-15489-1
          locator: 'iTeh 免费样章封面：ISO 15489-1，Second edition，2016-04-15；题名 Information and documentation — Records management
            — Part 1: Concepts and principles'
          checked: '2026-09-06'
        kind:
        - entity: iso-15489-1
          locator: 'iTeh 免费样章封面：ISO 15489-1，Second edition，2016-04-15；题名 Information and documentation — Records management
            — Part 1: Concepts and principles'
          checked: '2026-09-06'
        urls:
        - entity: iso-15489-1
          locator: 'iTeh 免费样章封面：ISO 15489-1，Second edition，2016-04-15；题名 Information and documentation — Records management
            — Part 1: Concepts and principles'
          checked: '2026-09-06'
        version:
        - entity: iso-15489-1
          locator: 'iTeh 免费样章封面：ISO 15489-1，Second edition，2016-04-15；题名 Information and documentation — Records management
            — Part 1: Concepts and principles'
          checked: '2026-09-06'
      watch:
      - locator: https://www.iso.org/standard/62542.html
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/juran-1974-non-pareto
    field: record
    value:
      id: juran-1974-non-pareto
      label:
        en: The Non-Pareto Principle; Mea Culpa
      kind: publication
      version: '1974'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: full_text
        url: https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: juran-1974-non-pareto
          locator: PDF 题名 The Non-Pareto Principle; Mea Culpa；正文与文件身份标示 1974；候选已核 PDF page index 0-2
          checked: '2026-09-06'
        kind:
        - entity: juran-1974-non-pareto
          locator: PDF 题名 The Non-Pareto Principle; Mea Culpa；正文与文件身份标示 1974；候选已核 PDF page index 0-2
          checked: '2026-09-06'
        urls:
        - entity: juran-1974-non-pareto
          locator: PDF 题名 The Non-Pareto Principle; Mea Culpa；正文与文件身份标示 1974；候选已核 PDF page index 0-2
          checked: '2026-09-06'
        version:
        - entity: juran-1974-non-pareto
          locator: PDF 题名 The Non-Pareto Principle; Mea Culpa；正文与文件身份标示 1974；候选已核 PDF page index 0-2
          checked: '2026-09-06'
      watch:
      - locator: https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/will-2012-iso-data-model
    field: record
    value:
      id: will-2012-iso-data-model
      label:
        en: The ISO 25964 data model for the structure of an information retrieval thesaurus
      kind: publication
      version: '2012'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: will-2012-iso-data-model
          locator: https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413；Compound Equivalence L94–101；Version
            History L145–147；实际取证见 work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: will-2012-iso-data-model
          locator: https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413；Compound Equivalence L94–101；Version
            History L145–147；实际取证见 work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: will-2012-iso-data-model
          locator: https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413；Compound Equivalence L94–101；Version
            History L145–147；实际取证见 work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: will-2012-iso-data-model
          locator: https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413；Compound Equivalence L94–101；Version
            History L145–147；实际取证见 work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/iso-1087-2019
    field: record
    value:
      id: iso-1087-2019
      label:
        en: Terminology work and terminology science — Vocabulary
      kind: standard
      version: '2019'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: full_text
        url: https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: iso-1087-2019
          locator: https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf；§3.1.4 PDF7/印刷1；§3.3.1
            PDF12/印刷6；§3.4.21 https://gso-sims-preview-doc-aws.s3-eu-west-1.amazonaws.com/iso-1087-2019-en.html；实际取证见 work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: iso-1087-2019
          locator: https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf；§3.1.4 PDF7/印刷1；§3.3.1
            PDF12/印刷6；§3.4.21 https://gso-sims-preview-doc-aws.s3-eu-west-1.amazonaws.com/iso-1087-2019-en.html；实际取证见 work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: iso-1087-2019
          locator: https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf；§3.1.4 PDF7/印刷1；§3.3.1
            PDF12/印刷6；§3.4.21 https://gso-sims-preview-doc-aws.s3-eu-west-1.amazonaws.com/iso-1087-2019-en.html；实际取证见 work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: iso-1087-2019
          locator: https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf；§3.1.4 PDF7/印刷1；§3.3.1
            PDF12/印刷6；§3.4.21 https://gso-sims-preview-doc-aws.s3-eu-west-1.amazonaws.com/iso-1087-2019-en.html；实际取证见 work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/iso25964-xsd-1-4
    field: record
    value:
      id: iso25964-xsd-1-4
      label:
        en: ISO 25964-1 XML Schema
      kind: standard
      version: '1.4'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: iso25964-xsd-1-4
          locator: https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd；role；topConcept；EditorialNote；ThesaurusConceptStruct/status与ThesaurusTerm/status；实际取证见
            work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: iso25964-xsd-1-4
          locator: https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd；role；topConcept；EditorialNote；ThesaurusConceptStruct/status与ThesaurusTerm/status；实际取证见
            work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: iso25964-xsd-1-4
          locator: https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd；role；topConcept；EditorialNote；ThesaurusConceptStruct/status与ThesaurusTerm/status；实际取证见
            work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: iso25964-xsd-1-4
          locator: https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd；role；topConcept；EditorialNote；ThesaurusConceptStruct/status与ThesaurusTerm/status；实际取证见
            work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/mazzocchi-knowledge-organization-system
    field: record
    value:
      id: mazzocchi-knowledge-organization-system
      label:
        en: Knowledge organization system
      kind: publication
      version: null
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://www.isko.org/cyclo/kos
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: mazzocchi-knowledge-organization-system
          locator: https://www.isko.org/cyclo/kos；§5.1 paradigmatic/syntagmatic；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: mazzocchi-knowledge-organization-system
          locator: https://www.isko.org/cyclo/kos；§5.1 paradigmatic/syntagmatic；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: mazzocchi-knowledge-organization-system
          locator: https://www.isko.org/cyclo/kos；§5.1 paradigmatic/syntagmatic；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.isko.org/cyclo/kos
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/nist-dads-tree
    field: record
    value:
      id: nist-dads-tree
      label:
        en: 'Dictionary of Algorithms and Data Structures: tree'
      kind: publication
      version: '2017-12-15'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://xlinux.nist.gov/dads/HTML/tree.html
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: nist-dads-tree
          locator: https://xlinux.nist.gov/dads/HTML/tree.html；Definition(1)与Formal Definition；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: nist-dads-tree
          locator: https://xlinux.nist.gov/dads/HTML/tree.html；Definition(1)与Formal Definition；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: nist-dads-tree
          locator: https://xlinux.nist.gov/dads/HTML/tree.html；Definition(1)与Formal Definition；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: nist-dads-tree
          locator: https://xlinux.nist.gov/dads/HTML/tree.html；Definition(1)与Formal Definition；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://xlinux.nist.gov/dads/HTML/tree.html
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/nist-dads-node
    field: record
    value:
      id: nist-dads-node
      label:
        en: 'Dictionary of Algorithms and Data Structures: node'
      kind: publication
      version: '2004-12-17'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://xlinux.nist.gov/dads/HTML/node.html
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: nist-dads-node
          locator: https://xlinux.nist.gov/dads/HTML/node.html；Definition(1)；实际取证见 work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: nist-dads-node
          locator: https://xlinux.nist.gov/dads/HTML/node.html；Definition(1)；实际取证见 work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: nist-dads-node
          locator: https://xlinux.nist.gov/dads/HTML/node.html；Definition(1)；实际取证见 work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: nist-dads-node
          locator: https://xlinux.nist.gov/dads/HTML/node.html；Definition(1)；实际取证见 work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://xlinux.nist.gov/dads/HTML/node.html
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/w3c-udc-use-case
    field: record
    value:
      id: w3c-udc-use-case
      label:
        en: Universal Decimal Classification
      kind: publication
      version: null
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.w3.org/2006/07/SWD/wiki/EucUDC
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: w3c-udc-use-case
          locator: https://www.w3.org/2006/07/SWD/wiki/EucUDC；L22 special auxiliaries；L56–57 common auxiliaries/tables；L68–80组配例；实际取证见
            work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: w3c-udc-use-case
          locator: https://www.w3.org/2006/07/SWD/wiki/EucUDC；L22 special auxiliaries；L56–57 common auxiliaries/tables；L68–80组配例；实际取证见
            work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: w3c-udc-use-case
          locator: https://www.w3.org/2006/07/SWD/wiki/EucUDC；L22 special auxiliaries；L56–57 common auxiliaries/tables；L68–80组配例；实际取证见
            work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.w3.org/2006/07/SWD/wiki/EucUDC
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/hearst-2009-search-user-interfaces
    field: record
    value:
      id: hearst-2009-search-user-interfaces
      label:
        en: Search User Interfaces
      kind: publication
      version: '2009'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://searchuserinterfaces.com/book/sui_ch8_navigation_and_search.html
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: hearst-2009-search-user-interfaces
          locator: https://searchuserinterfaces.com/book/sui_ch8_navigation_and_search.html；§8.3 attribute/dimension同例；§8.6
            facet/dimension/feature type；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: hearst-2009-search-user-interfaces
          locator: https://searchuserinterfaces.com/book/sui_ch8_navigation_and_search.html；§8.3 attribute/dimension同例；§8.6
            facet/dimension/feature type；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: hearst-2009-search-user-interfaces
          locator: https://searchuserinterfaces.com/book/sui_ch8_navigation_and_search.html；§8.3 attribute/dimension同例；§8.6
            facet/dimension/feature type；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: hearst-2009-search-user-interfaces
          locator: https://searchuserinterfaces.com/book/sui_ch8_navigation_and_search.html；§8.3 attribute/dimension同例；§8.6
            facet/dimension/feature type；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://searchuserinterfaces.com/book/sui_ch8_navigation_and_search.html
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/hjorland-facet-analysis
    field: record
    value:
      id: hjorland-facet-analysis
      label:
        en: Facet analysis
      kind: publication
      version: null
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://www.isko.org/cyclo/facet_analysis
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: hjorland-facet-analysis
          locator: https://www.isko.org/cyclo/facet_analysis；§3 Basic principles of facet analysis；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: hjorland-facet-analysis
          locator: https://www.isko.org/cyclo/facet_analysis；§3 Basic principles of facet analysis；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: hjorland-facet-analysis
          locator: https://www.isko.org/cyclo/facet_analysis；§3 Basic principles of facet analysis；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.isko.org/cyclo/facet_analysis
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/kaula-1980-canons
    field: record
    value:
      id: kaula-1980-canons
      label:
        en: Canons in Analytico-Synthetic Classification
      kind: publication
      version: '1980'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: full_text
        url: https://article.imrpress.com/journal/KO/7/3/10.5771/0943-7444-1980-3-118/4a183d5ac38a2c528b0133c11817a7a7.pdf
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: kaula-1980-canons
          locator: https://article.imrpress.com/journal/KO/7/3/10.5771/0943-7444-1980-3-118/4a183d5ac38a2c528b0133c11817a7a7.pdf；§2印刷118；§7/7.1/7.2印刷125；实际取证见
            work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: kaula-1980-canons
          locator: https://article.imrpress.com/journal/KO/7/3/10.5771/0943-7444-1980-3-118/4a183d5ac38a2c528b0133c11817a7a7.pdf；§2印刷118；§7/7.1/7.2印刷125；实际取证见
            work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: kaula-1980-canons
          locator: https://article.imrpress.com/journal/KO/7/3/10.5771/0943-7444-1980-3-118/4a183d5ac38a2c528b0133c11817a7a7.pdf；§2印刷118；§7/7.1/7.2印刷125；实际取证见
            work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: kaula-1980-canons
          locator: https://article.imrpress.com/journal/KO/7/3/10.5771/0943-7444-1980-3-118/4a183d5ac38a2c528b0133c11817a7a7.pdf；§2印刷118；§7/7.1/7.2印刷125；实际取证见
            work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://article.imrpress.com/journal/KO/7/3/10.5771/0943-7444-1980-3-118/4a183d5ac38a2c528b0133c11817a7a7.pdf
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/hjorland-domain-analysis
    field: record
    value:
      id: hjorland-domain-analysis
      label:
        en: Domain analysis
      kind: publication
      version: '2024-09-02'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://www.isko.org/cyclo/domain_analysis
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: hjorland-domain-analysis
          locator: https://www.isko.org/cyclo/domain_analysis；§1.1/1.2/1.4/2.1/4.7/7；实际取证见 work/reviews/2026-09-06-term-resolution-iso-relations.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: hjorland-domain-analysis
          locator: https://www.isko.org/cyclo/domain_analysis；§1.1/1.2/1.4/2.1/4.7/7；实际取证见 work/reviews/2026-09-06-term-resolution-iso-relations.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: hjorland-domain-analysis
          locator: https://www.isko.org/cyclo/domain_analysis；§1.1/1.2/1.4/2.1/4.7/7；实际取证见 work/reviews/2026-09-06-term-resolution-iso-relations.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: hjorland-domain-analysis
          locator: https://www.isko.org/cyclo/domain_analysis；§1.1/1.2/1.4/2.1/4.7/7；实际取证见 work/reviews/2026-09-06-term-resolution-iso-relations.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.isko.org/cyclo/domain_analysis
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/star-bowker-2007-enacting-silence
    field: record
    value:
      id: star-bowker-2007-enacting-silence
      label:
        en: Enacting silence
      kind: publication
      version: '2007'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://link.springer.com/article/10.1007/s10676-007-9141-7
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: star-bowker-2007-enacting-silence
          locator: https://link.springer.com/article/10.1007/s10676-007-9141-7；Abstract；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-iso-relations.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: star-bowker-2007-enacting-silence
          locator: https://link.springer.com/article/10.1007/s10676-007-9141-7；Abstract；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-iso-relations.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: star-bowker-2007-enacting-silence
          locator: https://link.springer.com/article/10.1007/s10676-007-9141-7；Abstract；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-iso-relations.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: star-bowker-2007-enacting-silence
          locator: https://link.springer.com/article/10.1007/s10676-007-9141-7；Abstract；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-iso-relations.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://link.springer.com/article/10.1007/s10676-007-9141-7
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/will-2009-skos-iso
    field: record
    value:
      id: will-2009-skos-iso
      label:
        en: Differences between SKOS and ISO standards
      kind: publication
      version: '2009-02-13'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: will-2009-skos-iso
          locator: https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html；Mapping between thesauri a–c，L131–140；实际取证见
            work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: will-2009-skos-iso
          locator: https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html；Mapping between thesauri a–c，L131–140；实际取证见
            work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: will-2009-skos-iso
          locator: https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html；Mapping between thesauri a–c，L131–140；实际取证见
            work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: will-2009-skos-iso
          locator: https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html；Mapping between thesauri a–c，L131–140；实际取证见
            work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/dnb-marc-2014-05
    field: record
    value:
      id: dnb-marc-2014-05
      label:
        en: MARC Proposal 2014-05
      kind: publication
      version: '2014'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://wwws.loc.gov/marc/mac/2014/2014-05.html
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: dnb-marc-2014-05
          locator: https://wwws.loc.gov/marc/mac/2014/2014-05.html；§1 BACKGROUND Table1 EQ/BM/NM/RM；§2 DISCUSSION；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: dnb-marc-2014-05
          locator: https://wwws.loc.gov/marc/mac/2014/2014-05.html；§1 BACKGROUND Table1 EQ/BM/NM/RM；§2 DISCUSSION；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: dnb-marc-2014-05
          locator: https://wwws.loc.gov/marc/mac/2014/2014-05.html；§1 BACKGROUND Table1 EQ/BM/NM/RM；§2 DISCUSSION；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: dnb-marc-2014-05
          locator: https://wwws.loc.gov/marc/mac/2014/2014-05.html；§1 BACKGROUND Table1 EQ/BM/NM/RM；§2 DISCUSSION；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://wwws.loc.gov/marc/mac/2014/2014-05.html
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/clarke-information-retrieval-thesaurus
    field: record
    value:
      id: clarke-information-retrieval-thesaurus
      label:
        en: The Information Retrieval Thesaurus
      kind: publication
      version: null
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://www.isko.org/cyclo/thesaurus
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: clarke-information-retrieval-thesaurus
          locator: https://www.isko.org/cyclo/thesaurus；§3.2/Figure3；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: clarke-information-retrieval-thesaurus
          locator: https://www.isko.org/cyclo/thesaurus；§3.2/Figure3；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: clarke-information-retrieval-thesaurus
          locator: https://www.isko.org/cyclo/thesaurus；§3.2/Figure3；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.isko.org/cyclo/thesaurus
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/zeng-interoperability
    field: record
    value:
      id: zeng-interoperability
      label:
        en: Interoperability
      kind: publication
      version: '2019'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://www.isko.org/cyclo/interoperability
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: zeng-interoperability
          locator: https://www.isko.org/cyclo/interoperability；§5.2/Table2期刊p138；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: zeng-interoperability
          locator: https://www.isko.org/cyclo/interoperability；§5.2/Table2期刊p138；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: zeng-interoperability
          locator: https://www.isko.org/cyclo/interoperability；§5.2/Table2期刊p138；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: zeng-interoperability
          locator: https://www.isko.org/cyclo/interoperability；§5.2/Table2期刊p138；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.isko.org/cyclo/interoperability
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/aristotle-posterior-analytics-mure
    field: record
    value:
      id: aristotle-posterior-analytics-mure
      label:
        en: Posterior Analytics
      kind: publication
      version: null
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://classics.mit.edu/Aristotle/posterior.1.i.html
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: aristotle-posterior-analytics-mure
          locator: https://classics.mit.edu/Aristotle/posterior.1.i.html；BookI Part2/3；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: aristotle-posterior-analytics-mure
          locator: https://classics.mit.edu/Aristotle/posterior.1.i.html；BookI Part2/3；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: aristotle-posterior-analytics-mure
          locator: https://classics.mit.edu/Aristotle/posterior.1.i.html；BookI Part2/3；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://classics.mit.edu/Aristotle/posterior.1.i.html
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/aristotle-metaphysics-ross
    field: record
    value:
      id: aristotle-metaphysics-ross
      label:
        en: Metaphysics
      kind: publication
      version: null
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://classics.mit.edu/Aristotle/metaphysics.1.i.html
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: aristotle-metaphysics-ross
          locator: https://classics.mit.edu/Aristotle/metaphysics.1.i.html；BookI Part2/7；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: aristotle-metaphysics-ross
          locator: https://classics.mit.edu/Aristotle/metaphysics.1.i.html；BookI Part2/7；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: aristotle-metaphysics-ross
          locator: https://classics.mit.edu/Aristotle/metaphysics.1.i.html；BookI Part2/7；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://classics.mit.edu/Aristotle/metaphysics.1.i.html
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/buckingham-shum-1995-design-rationale
    field: record
    value:
      id: buckingham-shum-1995-design-rationale
      label:
        en: Design Argumentation as Design Rationale
      kind: publication
      version: KMI-95-14
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://kmi.open.ac.uk/publications/techreport/kmi-95-14
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: buckingham-shum-1995-design-rationale
          locator: https://kmi.open.ac.uk/publications/techreport/kmi-95-14；摘要首句；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: buckingham-shum-1995-design-rationale
          locator: https://kmi.open.ac.uk/publications/techreport/kmi-95-14；摘要首句；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: buckingham-shum-1995-design-rationale
          locator: https://kmi.open.ac.uk/publications/techreport/kmi-95-14；摘要首句；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: buckingham-shum-1995-design-rationale
          locator: https://kmi.open.ac.uk/publications/techreport/kmi-95-14；摘要首句；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://kmi.open.ac.uk/publications/techreport/kmi-95-14
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/nygard-2011-architecture-decisions
    field: record
    value:
      id: nygard-2011-architecture-decisions
      label:
        en: Documenting Architecture Decisions
      kind: publication
      version: '2011-11-15'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: nygard-2011-architecture-decisions
          locator: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions；superseded与保留旧决定正文；实际取证见 work/reviews/2026-09-06-term-governance-coverage.json、work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: nygard-2011-architecture-decisions
          locator: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions；superseded与保留旧决定正文；实际取证见 work/reviews/2026-09-06-term-governance-coverage.json、work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: nygard-2011-architecture-decisions
          locator: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions；superseded与保留旧决定正文；实际取证见 work/reviews/2026-09-06-term-governance-coverage.json、work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: nygard-2011-architecture-decisions
          locator: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions；superseded与保留旧决定正文；实际取证见 work/reviews/2026-09-06-term-governance-coverage.json、work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/w3c-xml-1-0
    field: record
    value:
      id: w3c-xml-1-0
      label:
        en: Extensible Markup Language (XML) 1.0 (Fifth Edition)
      kind: standard
      version: '2008-11-26'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.w3.org/TR/REC-xml/
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: w3c-xml-1-0
          locator: https://www.w3.org/TR/REC-xml/；§3.2.1 Element Content；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: w3c-xml-1-0
          locator: https://www.w3.org/TR/REC-xml/；§3.2.1 Element Content；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: w3c-xml-1-0
          locator: https://www.w3.org/TR/REC-xml/；§3.2.1 Element Content；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: w3c-xml-1-0
          locator: https://www.w3.org/TR/REC-xml/；§3.2.1 Element Content；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.w3.org/TR/REC-xml/
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/hjorland-knowledge-organization
    field: record
    value:
      id: hjorland-knowledge-organization
      label:
        en: Knowledge organization (KO)
      kind: publication
      version: null
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://www.isko.org/cyclo/knowledge_organization
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: hjorland-knowledge-organization
          locator: https://www.isko.org/cyclo/knowledge_organization；§1末两段，KOP/KOS；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: hjorland-knowledge-organization
          locator: https://www.isko.org/cyclo/knowledge_organization；§1末两段，KOP/KOS；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: hjorland-knowledge-organization
          locator: https://www.isko.org/cyclo/knowledge_organization；§1末两段，KOP/KOS；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.isko.org/cyclo/knowledge_organization
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/gertz-1974
    field: record
    value:
      id: gertz-1974
      label:
        en: Gertz v. Robert Welch, Inc., 418 U.S. 323
      kind: publication
      version: '1974-06-25'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://www.law.cornell.edu/supremecourt/text/418/323
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: gertz-1974
          locator: https://www.law.cornell.edu/supremecourt/text/418/323；345、351–352；原作者发表仍非public figure；一般/特定争议两类；实际取证见
            work/reviews/2026-09-06-term-governance-coverage.json、work/reviews/2026-09-06-term-resolution-final-semantics.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: gertz-1974
          locator: https://www.law.cornell.edu/supremecourt/text/418/323；345、351–352；原作者发表仍非public figure；一般/特定争议两类；实际取证见
            work/reviews/2026-09-06-term-governance-coverage.json、work/reviews/2026-09-06-term-resolution-final-semantics.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: gertz-1974
          locator: https://www.law.cornell.edu/supremecourt/text/418/323；345、351–352；原作者发表仍非public figure；一般/特定争议两类；实际取证见
            work/reviews/2026-09-06-term-governance-coverage.json、work/reviews/2026-09-06-term-resolution-final-semantics.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: gertz-1974
          locator: https://www.law.cornell.edu/supremecourt/text/418/323；345、351–352；原作者发表仍非public figure；一般/特定争议两类；实际取证见
            work/reviews/2026-09-06-term-governance-coverage.json、work/reviews/2026-09-06-term-resolution-final-semantics.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.law.cornell.edu/supremecourt/text/418/323
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/owl2-primer
    field: record
    value:
      id: owl2-primer
      label:
        en: OWL 2 Web Ontology Language Primer (Second Edition)
      kind: standard
      version: '2012-12-11'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.w3.org/TR/owl2-primer/
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: owl2-primer
          locator: https://www.w3.org/TR/owl2-primer/；§3/4.1/4.7 individuals；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: owl2-primer
          locator: https://www.w3.org/TR/owl2-primer/；§3/4.1/4.7 individuals；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: owl2-primer
          locator: https://www.w3.org/TR/owl2-primer/；§3/4.1/4.7 individuals；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: owl2-primer
          locator: https://www.w3.org/TR/owl2-primer/；§3/4.1/4.7 individuals；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.w3.org/TR/owl2-primer/
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/cornell-cs3110-2012-partition
    field: record
    value:
      id: cornell-cs3110-2012-partition
      label:
        en: CS 3110 Recitation 14
      kind: publication
      version: 2012 Fall
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://www.cs.cornell.edu/courses/cs3110/2012fa/recitations/rec14.html
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: cornell-cs3110-2012-partition
          locator: https://www.cs.cornell.edu/courses/cs3110/2012fa/recitations/rec14.html；首段partition定义；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: cornell-cs3110-2012-partition
          locator: https://www.cs.cornell.edu/courses/cs3110/2012fa/recitations/rec14.html；首段partition定义；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: cornell-cs3110-2012-partition
          locator: https://www.cs.cornell.edu/courses/cs3110/2012fa/recitations/rec14.html；首段partition定义；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: cornell-cs3110-2012-partition
          locator: https://www.cs.cornell.edu/courses/cs3110/2012fa/recitations/rec14.html；首段partition定义；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.cs.cornell.edu/courses/cs3110/2012fa/recitations/rec14.html
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/nonaka-toyama-konno-managing-industrial-knowledge
    field: record
    value:
      id: nonaka-toyama-konno-managing-industrial-knowledge
      label:
        en: Managing Industrial Knowledge, Chapter 1
      kind: publication
      version: null
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: full_text
        url: https://api.pageplace.de/preview/DT0400.9781847876621_A23446119/preview-9781847876621_A23446119.pdf
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: nonaka-toyama-konno-managing-industrial-knowledge
          locator: https://api.pageplace.de/preview/DT0400.9781847876621_A23446119/preview-9781847876621_A23446119.pdf；PDF22署名；PDF24/印刷16
            tacit/explicit；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-knowledge-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: nonaka-toyama-konno-managing-industrial-knowledge
          locator: https://api.pageplace.de/preview/DT0400.9781847876621_A23446119/preview-9781847876621_A23446119.pdf；PDF22署名；PDF24/印刷16
            tacit/explicit；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-knowledge-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: nonaka-toyama-konno-managing-industrial-knowledge
          locator: https://api.pageplace.de/preview/DT0400.9781847876621_A23446119/preview-9781847876621_A23446119.pdf；PDF22署名；PDF24/印刷16
            tacit/explicit；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-knowledge-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://api.pageplace.de/preview/DT0400.9781847876621_A23446119/preview-9781847876621_A23446119.pdf
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/stern-fragment-whole
    field: record
    value:
      id: stern-fragment-whole
      label:
        en: The Fragment and the Whole
      kind: publication
      version: null
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://takenote.library.harvard.edu/fragment-and-whole
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: stern-fragment-whole
          locator: https://takenote.library.harvard.edu/fragment-and-whole；正文6–8段，L133–138 commonplace books；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-knowledge-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: stern-fragment-whole
          locator: https://takenote.library.harvard.edu/fragment-and-whole；正文6–8段，L133–138 commonplace books；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-knowledge-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: stern-fragment-whole
          locator: https://takenote.library.harvard.edu/fragment-and-whole；正文6–8段，L133–138 commonplace books；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-knowledge-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://takenote.library.harvard.edu/fragment-and-whole
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/krathwohl-2002-taxonomy
    field: record
    value:
      id: krathwohl-2002-taxonomy
      label:
        en: 'A Revision of Bloom’s Taxonomy: An Overview'
      kind: publication
      version: '2002'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: full_text
        url: https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: krathwohl-2002-taxonomy
          locator: https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf；PDF index2–5/印刷214–217 Cognitive
            Process dimension；实际取证见 work/reviews/2026-09-06-term-content-coverage.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: krathwohl-2002-taxonomy
          locator: https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf；PDF index2–5/印刷214–217 Cognitive
            Process dimension；实际取证见 work/reviews/2026-09-06-term-content-coverage.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: krathwohl-2002-taxonomy
          locator: https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf；PDF index2–5/印刷214–217 Cognitive
            Process dimension；实际取证见 work/reviews/2026-09-06-term-content-coverage.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: krathwohl-2002-taxonomy
          locator: https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf；PDF index2–5/印刷214–217 Cognitive
            Process dimension；实际取证见 work/reviews/2026-09-06-term-content-coverage.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/iso-37000-2021
    field: record
    value:
      id: iso-37000-2021
      label:
        en: Governance of organizations — Guidance
      kind: standard
      version: '2021'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: full_text
        url: https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: iso-37000-2021
          locator: https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf；§3.1.1
            PDF9/印刷1；§3.2.9 PDF12/印刷4；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: iso-37000-2021
          locator: https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf；§3.1.1
            PDF9/印刷1；§3.2.9 PDF12/印刷4；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: iso-37000-2021
          locator: https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf；§3.1.1
            PDF9/印刷1；§3.2.9 PDF12/印刷4；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: iso-37000-2021
          locator: https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf；§3.1.1
            PDF9/印刷1；§3.2.9 PDF12/印刷4；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/oecd-2024-evaluation-glossary-en-zh
    field: record
    value:
      id: oecd-2024-evaluation-glossary-en-zh
      label:
        en: Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition),
          English/Chinese
      kind: publication
      version: Second edition, 2024, EN-ZH
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: full_text
        url: https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: oecd-2024-evaluation-glossary-en-zh
          locator: https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf；Monitoring
            PDF39；Evaluation PDF29；Indicator PDF35；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-knowledge-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: oecd-2024-evaluation-glossary-en-zh
          locator: https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf；Monitoring
            PDF39；Evaluation PDF29；Indicator PDF35；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-knowledge-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: oecd-2024-evaluation-glossary-en-zh
          locator: https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf；Monitoring
            PDF39；Evaluation PDF29；Indicator PDF35；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-knowledge-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: oecd-2024-evaluation-glossary-en-zh
          locator: https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf；Monitoring
            PDF39；Evaluation PDF29；Indicator PDF35；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-knowledge-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/w3c-rdf-semantics-2004
    field: record
    value:
      id: w3c-rdf-semantics-2004
      label:
        en: RDF Semantics
      kind: standard
      version: '2004-02-10'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.w3.org/TR/rdf-mt/
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: w3c-rdf-semantics-2004
          locator: https://www.w3.org/TR/rdf-mt/；AppendixB Inference；L1282；实际取证见 work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: w3c-rdf-semantics-2004
          locator: https://www.w3.org/TR/rdf-mt/；AppendixB Inference；L1282；实际取证见 work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: w3c-rdf-semantics-2004
          locator: https://www.w3.org/TR/rdf-mt/；AppendixB Inference；L1282；实际取证见 work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: w3c-rdf-semantics-2004
          locator: https://www.w3.org/TR/rdf-mt/；AppendixB Inference；L1282；实际取证见 work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.w3.org/TR/rdf-mt/
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/iso-39075-2024
    field: record
    value:
      id: iso-39075-2024
      label:
        en: Information technology — Database languages — GQL
      kind: standard
      version: '2024'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://www.iso.org/standard/76120.html
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: iso-39075-2024
          locator: https://www.iso.org/standard/76120.html；Abstract，Edition1，2024-04；实际取证见 work/reviews/2026-09-06-term-resolution-summary.json、work/reviews/2026-09-06-term-resolution-web.json
          checked: '2026-09-06'
        kind:
        - entity: iso-39075-2024
          locator: https://www.iso.org/standard/76120.html；Abstract，Edition1，2024-04；实际取证见 work/reviews/2026-09-06-term-resolution-summary.json、work/reviews/2026-09-06-term-resolution-web.json
          checked: '2026-09-06'
        urls:
        - entity: iso-39075-2024
          locator: https://www.iso.org/standard/76120.html；Abstract，Edition1，2024-04；实际取证见 work/reviews/2026-09-06-term-resolution-summary.json、work/reviews/2026-09-06-term-resolution-web.json
          checked: '2026-09-06'
        version:
        - entity: iso-39075-2024
          locator: https://www.iso.org/standard/76120.html；Abstract，Edition1，2024-04；实际取证见 work/reviews/2026-09-06-term-resolution-summary.json、work/reviews/2026-09-06-term-resolution-web.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.iso.org/standard/76120.html
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/iso-24495-1
    field: record
    value:
      id: iso-24495-1
      label:
        en: 'Plain language — Part 1: Governing principles and guidelines'
      kind: standard
      version: '2023'
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: full_text
        url: https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: iso-24495-1
          locator: https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf；免费样章
            PDF p. 9（印刷 p. 3），§4 Governing principles；PDF pp. 9–11（印刷 pp. 3–5），§5.1 与 §5.2.1–§5.2.3。；实际取证见 work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: iso-24495-1
          locator: https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf；免费样章
            PDF p. 9（印刷 p. 3），§4 Governing principles；PDF pp. 9–11（印刷 pp. 3–5），§5.1 与 §5.2.1–§5.2.3。；实际取证见 work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: iso-24495-1
          locator: https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf；免费样章
            PDF p. 9（印刷 p. 3），§4 Governing principles；PDF pp. 9–11（印刷 pp. 3–5），§5.1 与 §5.2.1–§5.2.3。；实际取证见 work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: iso-24495-1
          locator: https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf；免费样章
            PDF p. 9（印刷 p. 3），§4 Governing principles；PDF pp. 9–11（印刷 pp. 3–5），§5.1 与 §5.2.1–§5.2.3。；实际取证见 work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/francis-et-al-2018-cypher
    field: record
    value:
      id: francis-et-al-2018-cypher
      label:
        en: 'Cypher: An Evolving Query Language for Property Graphs'
      kind: publication
      version: '2018'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: full_text
        url: https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: francis-et-al-2018-cypher
          locator: https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf；作者稿 PDF p. 2（论文 p. 1433），Abstract
            与 §1；PDF p. 3（论文 p. 1434），§2 The Cypher Language。；实际取证见 work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: francis-et-al-2018-cypher
          locator: https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf；作者稿 PDF p. 2（论文 p. 1433），Abstract
            与 §1；PDF p. 3（论文 p. 1434），§2 The Cypher Language。；实际取证见 work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: francis-et-al-2018-cypher
          locator: https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf；作者稿 PDF p. 2（论文 p. 1433），Abstract
            与 §1；PDF p. 3（论文 p. 1434），§2 The Cypher Language。；实际取证见 work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: francis-et-al-2018-cypher
          locator: https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf；作者稿 PDF p. 2（论文 p. 1433），Abstract
            与 §1；PDF p. 3（论文 p. 1434），§2 The Cypher Language。；实际取证见 work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/lamb-zacchiroli-2021-reproducible-builds
    field: record
    value:
      id: lamb-zacchiroli-2021-reproducible-builds
      label:
        en: 'Reproducible Builds: Increasing the Integrity of Software Supply Chains'
      kind: publication
      version: arXiv v1
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: full_text
        url: https://arxiv.org/pdf/2104.06020v1
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: lamb-zacchiroli-2021-reproducible-builds
          locator: https://arxiv.org/pdf/2104.06020v1；arXiv:2104.06020v1，PDF p. 2，Reproducible Builds，Definition 1。；实际取证见
            work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        kind:
        - entity: lamb-zacchiroli-2021-reproducible-builds
          locator: https://arxiv.org/pdf/2104.06020v1；arXiv:2104.06020v1，PDF p. 2，Reproducible Builds，Definition 1。；实际取证见
            work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        urls:
        - entity: lamb-zacchiroli-2021-reproducible-builds
          locator: https://arxiv.org/pdf/2104.06020v1；arXiv:2104.06020v1，PDF p. 2，Reproducible Builds，Definition 1。；实际取证见
            work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
        version:
        - entity: lamb-zacchiroli-2021-reproducible-builds
          locator: https://arxiv.org/pdf/2104.06020v1；arXiv:2104.06020v1，PDF p. 2，Reproducible Builds，Definition 1。；实际取证见
            work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
          checked: '2026-09-06'
      watch:
      - locator: https://arxiv.org/pdf/2104.06020v1
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/dunn-bourcier-nomenclature
    field: record
    value:
      id: dunn-bourcier-nomenclature
      label:
        en: Nomenclature for Museum Cataloging
      kind: publication
      version: null
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: landing
        url: https://www.isko.org/cyclo/nomenclature.htm
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: dunn-bourcier-nomenclature
          locator: https://www.isko.org/cyclo/nomenclature.htm；§6 Limitations：monohierarchical classification system each
            term only one immediate broader；同段 monohierarchy 回指；实际取证见 work/reviews/2026-09-06-term-complete-candidate.json
          checked: '2026-09-06'
        kind:
        - entity: dunn-bourcier-nomenclature
          locator: https://www.isko.org/cyclo/nomenclature.htm；§6 Limitations：monohierarchical classification system each
            term only one immediate broader；同段 monohierarchy 回指；实际取证见 work/reviews/2026-09-06-term-complete-candidate.json
          checked: '2026-09-06'
        urls:
        - entity: dunn-bourcier-nomenclature
          locator: https://www.isko.org/cyclo/nomenclature.htm；§6 Limitations：monohierarchical classification system each
            term only one immediate broader；同段 monohierarchy 回指；实际取证见 work/reviews/2026-09-06-term-complete-candidate.json
          checked: '2026-09-06'
      watch:
      - locator: https://www.isko.org/cyclo/nomenclature.htm
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/nist-sp-800-53r5
    field: record
    value:
      id: nist-sp-800-53r5
      label:
        en: Security and Privacy Controls for Information Systems and Organizations
      kind: standard
      version: Revision 5 (updates 2020-12-10)
      tier: de-jure
      subjects: []
      status: candidate
      urls:
      - role: doi
        url: https://doi.org/10.6028/NIST.SP.800-53r5
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: nist-sp-800-53r5
          locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；封面：Revision 5，September 2020，includes
            updates as of 2020-12-10；PDF p. 422，Appendix A p. 395，audit 与 audit trail
          checked: '2026-09-06'
        kind:
        - entity: nist-sp-800-53r5
          locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；封面：Revision 5，September 2020，includes
            updates as of 2020-12-10；PDF p. 422，Appendix A p. 395，audit 与 audit trail
          checked: '2026-09-06'
        urls:
        - entity: nist-sp-800-53r5
          locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；封面：Revision 5，September 2020，includes
            updates as of 2020-12-10；PDF p. 422，Appendix A p. 395，audit 与 audit trail
          checked: '2026-09-06'
        version:
        - entity: nist-sp-800-53r5
          locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；封面：Revision 5，September 2020，includes
            updates as of 2020-12-10；PDF p. 422，Appendix A p. 395，audit 与 audit trail
          checked: '2026-09-06'
      watch:
      - locator: https://doi.org/10.6028/NIST.SP.800-53r5
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 1
      review:
        checked: null
        next_due: null
        interval_months: 24
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/american-heritage-dictionary-5-cheat-sheet
    field: record
    value:
      id: american-heritage-dictionary-5-cheat-sheet
      label:
        en: The American Heritage Dictionary of the English Language, Fifth Edition
      kind: publication
      version: Fifth Edition (2022)
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: american-heritage-dictionary-5-cheat-sheet
          locator: 官方 AHD 条目 cheat sheet；义项 2；页面明确标注 The American Heritage Dictionary of the English Language, Fifth Edition
            copyright ©2022 by HarperCollins Publishers
          checked: '2026-09-06'
        kind:
        - entity: american-heritage-dictionary-5-cheat-sheet
          locator: 官方 AHD 条目 cheat sheet；义项 2；页面明确标注 The American Heritage Dictionary of the English Language, Fifth Edition
            copyright ©2022 by HarperCollins Publishers
          checked: '2026-09-06'
        urls:
        - entity: american-heritage-dictionary-5-cheat-sheet
          locator: 官方 AHD 条目 cheat sheet；义项 2；页面明确标注 The American Heritage Dictionary of the English Language, Fifth Edition
            copyright ©2022 by HarperCollins Publishers
          checked: '2026-09-06'
        version:
        - entity: american-heritage-dictionary-5-cheat-sheet
          locator: 官方 AHD 条目 cheat sheet；义项 2；页面明确标注 The American Heritage Dictionary of the English Language, Fifth Edition
            copyright ©2022 by HarperCollins Publishers
          checked: '2026-09-06'
      watch:
      - locator: https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/dnd-caf-data-governance
    field: record
    value:
      id: dnd-caf-data-governance
      label:
        en: DND/CAF (Department of National Defence and the Canadian Armed Forces) Data Governance Framework
      kind: publication
      version: '2022-07-28'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.canada.ca/en/department-national-defence/corporate/reports-publications/data-governance.html
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: dnd-caf-data-governance
          locator: 独立政府框架全文；Page details 2022-07-28；Appendix B data governance；§6.4.2 Chief Data Officer；§6.4.3.1 Data Governors
          checked: '2026-09-06'
        kind:
        - entity: dnd-caf-data-governance
          locator: 独立政府框架全文；Page details 2022-07-28；Appendix B data governance；§6.4.2 Chief Data Officer；§6.4.3.1 Data Governors
          checked: '2026-09-06'
        urls:
        - entity: dnd-caf-data-governance
          locator: 独立政府框架全文；Page details 2022-07-28；Appendix B data governance；§6.4.2 Chief Data Officer；§6.4.3.1 Data Governors
          checked: '2026-09-06'
        version:
        - entity: dnd-caf-data-governance
          locator: 独立政府框架全文；Page details 2022-07-28；Appendix B data governance；§6.4.2 Chief Data Officer；§6.4.3.1 Data Governors
          checked: '2026-09-06'
      watch:
      - locator: https://www.canada.ca/en/department-national-defence/corporate/reports-publications/data-governance.html
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
  - identity: entities/dfe-external-governance-reviews
    field: record
    value:
      id: dfe-external-governance-reviews
      label:
        en: 'External governance reviews: guide for FE college corporations and designated institutions'
      kind: publication
      version: '2026-08-11'
      tier: archival
      subjects: []
      status: candidate
      urls:
      - role: canonical
        url: https://www.gov.uk/guidance/external-governance-reviews-guide-for-fe-college-corporations-and-designated-institutions
        primary: true
      added: '2026-09-06'
      basis:
        label:
        - entity: dfe-external-governance-reviews
          locator: Department for Education guidance；Published 2022-05-20；所读版 Last updated 2026-08-11；Updates to this page
            记录该版变更；Benefits of an external governance review；Setting the scope and objectives
          checked: '2026-09-06'
        kind:
        - entity: dfe-external-governance-reviews
          locator: Department for Education guidance；Published 2022-05-20；所读版 Last updated 2026-08-11；Updates to this page
            记录该版变更；Benefits of an external governance review；Setting the scope and objectives
          checked: '2026-09-06'
        urls:
        - entity: dfe-external-governance-reviews
          locator: Department for Education guidance；Published 2022-05-20；所读版 Last updated 2026-08-11；Updates to this page
            记录该版变更；Benefits of an external governance review；Setting the scope and objectives
          checked: '2026-09-06'
        version:
        - entity: dfe-external-governance-reviews
          locator: Department for Education guidance；Published 2022-05-20；所读版 Last updated 2026-08-11；Updates to this page
            记录该版变更；Benefits of an external governance review；Setting the scope and objectives
          checked: '2026-09-06'
      watch:
      - locator: https://www.gov.uk/guidance/external-governance-reviews-guide-for-fe-college-corporations-and-designated-institutions
        signals:
        - availability
        - redirect
        cadence_months:
          availability: 1
          redirect: 1
          content: 12
      review:
        checked: null
        next_due: null
        interval_months: null
        grace_days: 30
        obligations: []
      replaced_by: null
- question: Q02
  resolution: recommended
  patches:
  - identity: entities/gruber-official
    field: version
    value: '2008'
  - identity: entities/gruber-official
    field: basis.version
    value:
    - entity: gruber-official
      locator: 页面正文书目信息：Tom Gruber (2008), Ontology；正文说明其更新 1993 ontology definition
      checked: '2026-09-06'
  - identity: entities/hogan-paper
    field: version
    value: arXiv v6
  - identity: entities/hogan-paper
    field: basis.version
    value:
    - entity: hogan-paper
      locator: https://export.arxiv.org/api/query?id_list=2003.02320；entry id 2003.02320v6；updated 2021-09-11T21:36:53Z；abs
        submission history v6
      checked: '2026-09-06'
  - identity: entities/rdf11
    field: version
    value: '2014-02-25'
  - identity: entities/rdf11
    field: basis.version
    value:
    - entity: rdf11
      locator: 文档头：RDF 1.1 Concepts and Abstract Syntax；W3C Recommendation 25 February 2014；版本化 URI /TR/2014/REC-rdf11-concepts-20140225/
      checked: '2026-09-06'
  - identity: entities/rdfs11
    field: version
    value: '2014-02-25'
  - identity: entities/rdfs11
    field: basis.version
    value:
    - entity: rdfs11
      locator: 文档头：RDF Schema 1.1；版本化 URI /TR/2014/REC-rdf-schema-20140225/
      checked: '2026-09-06'
  - identity: entities/owl2
    field: version
    value: '2012-12-11'
  - identity: entities/owl2
    field: basis.version
    value:
    - entity: owl2
      locator: 文档头：OWL 2 Web Ontology Language Document Overview (Second Edition)；W3C Recommendation 11 December 2012
      checked: '2026-09-06'
  - identity: entities/sparql11
    field: version
    value: '2013-03-21'
  - identity: entities/sparql11
    field: basis.version
    value:
    - entity: sparql11
      locator: 文档头：SPARQL 1.1 Query Language；W3C Recommendation 21 March 2013
      checked: '2026-09-06'
  - identity: entities/dcmi-metadata-terms
    field: version
    value: '2020-01-20'
  - identity: entities/dcmi-metadata-terms
    field: basis.version
    value:
    - entity: dcmi-metadata-terms
      locator: 文档头：DCMI Metadata Terms；Date Issued 2020-01-20；DCMI Recommendation
      checked: '2026-09-06'
  - identity: entities/dcmi-singapore-framework
    field: version
    value: '2008-01-14'
  - identity: entities/dcmi-singapore-framework
    field: basis.version
    value:
    - entity: dcmi-singapore-framework
      locator: 文档头：The Singapore Framework for Dublin Core™ Application Profiles；Date Issued 2008-01-14；docs/references/dcmi-application-profiles.md
        已核状态为 past、note
      checked: '2026-09-06'
  - identity: entities/iso-15489-1
    field: version
    value: '2016'
  - identity: entities/iso-15489-1
    field: basis.version
    value:
    - entity: iso-15489-1
      locator: 'iTeh 免费样章封面：ISO 15489-1，Second edition，2016-04-15；题名 Information and documentation — Records management —
        Part 1: Concepts and principles'
      checked: '2026-09-06'
  - identity: entities/juran-1974-non-pareto
    field: version
    value: '1974'
  - identity: entities/juran-1974-non-pareto
    field: basis.version
    value:
    - entity: juran-1974-non-pareto
      locator: PDF 题名 The Non-Pareto Principle; Mea Culpa；正文与文件身份标示 1974；候选已核 PDF page index 0-2
      checked: '2026-09-06'
  - identity: entities/will-2012-iso-data-model
    field: version
    value: '2012'
  - identity: entities/will-2012-iso-data-model
    field: basis.version
    value:
    - entity: will-2012-iso-data-model
      locator: https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413；Compound Equivalence L94–101；Version
        History L145–147；实际取证见 work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/iso-1087-2019
    field: version
    value: '2019'
  - identity: entities/iso-1087-2019
    field: basis.version
    value:
    - entity: iso-1087-2019
      locator: https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf；§3.1.4 PDF7/印刷1；§3.3.1
        PDF12/印刷6；§3.4.21 https://gso-sims-preview-doc-aws.s3-eu-west-1.amazonaws.com/iso-1087-2019-en.html；实际取证见 work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/iso25964-xsd-1-4
    field: version
    value: '1.4'
  - identity: entities/iso25964-xsd-1-4
    field: basis.version
    value:
    - entity: iso25964-xsd-1-4
      locator: https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd；role；topConcept；EditorialNote；ThesaurusConceptStruct/status与ThesaurusTerm/status；实际取证见
        work/reviews/2026-09-06-term-resolution-iso-basic.json、work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/nist-dads-tree
    field: version
    value: '2017-12-15'
  - identity: entities/nist-dads-tree
    field: basis.version
    value:
    - entity: nist-dads-tree
      locator: https://xlinux.nist.gov/dads/HTML/tree.html；Definition(1)与Formal Definition；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/nist-dads-node
    field: version
    value: '2004-12-17'
  - identity: entities/nist-dads-node
    field: basis.version
    value:
    - entity: nist-dads-node
      locator: https://xlinux.nist.gov/dads/HTML/node.html；Definition(1)；实际取证见 work/reviews/2026-09-06-term-resolution-project.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/hearst-2009-search-user-interfaces
    field: version
    value: '2009'
  - identity: entities/hearst-2009-search-user-interfaces
    field: basis.version
    value:
    - entity: hearst-2009-search-user-interfaces
      locator: https://searchuserinterfaces.com/book/sui_ch8_navigation_and_search.html；§8.3 attribute/dimension同例；§8.6 facet/dimension/feature
        type；实际取证见 work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/kaula-1980-canons
    field: version
    value: '1980'
  - identity: entities/kaula-1980-canons
    field: basis.version
    value:
    - entity: kaula-1980-canons
      locator: https://article.imrpress.com/journal/KO/7/3/10.5771/0943-7444-1980-3-118/4a183d5ac38a2c528b0133c11817a7a7.pdf；§2印刷118；§7/7.1/7.2印刷125；实际取证见
        work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/hjorland-domain-analysis
    field: version
    value: '2024-09-02'
  - identity: entities/hjorland-domain-analysis
    field: basis.version
    value:
    - entity: hjorland-domain-analysis
      locator: https://www.isko.org/cyclo/domain_analysis；§1.1/1.2/1.4/2.1/4.7/7；实际取证见 work/reviews/2026-09-06-term-resolution-iso-relations.json、work/reviews/2026-09-06-term-resolution-semantic-repairs.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/star-bowker-2007-enacting-silence
    field: version
    value: '2007'
  - identity: entities/star-bowker-2007-enacting-silence
    field: basis.version
    value:
    - entity: star-bowker-2007-enacting-silence
      locator: https://link.springer.com/article/10.1007/s10676-007-9141-7；Abstract；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-iso-relations.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/will-2009-skos-iso
    field: version
    value: '2009-02-13'
  - identity: entities/will-2009-skos-iso
    field: basis.version
    value:
    - entity: will-2009-skos-iso
      locator: https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html；Mapping between thesauri a–c，L131–140；实际取证见
        work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/dnb-marc-2014-05
    field: version
    value: '2014'
  - identity: entities/dnb-marc-2014-05
    field: basis.version
    value:
    - entity: dnb-marc-2014-05
      locator: https://wwws.loc.gov/marc/mac/2014/2014-05.html；§1 BACKGROUND Table1 EQ/BM/NM/RM；§2 DISCUSSION；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/zeng-interoperability
    field: version
    value: '2019'
  - identity: entities/zeng-interoperability
    field: basis.version
    value:
    - entity: zeng-interoperability
      locator: https://www.isko.org/cyclo/interoperability；§5.2/Table2期刊p138；实际取证见 work/reviews/2026-09-06-term-resolution-difficult.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/buckingham-shum-1995-design-rationale
    field: version
    value: KMI-95-14
  - identity: entities/buckingham-shum-1995-design-rationale
    field: basis.version
    value:
    - entity: buckingham-shum-1995-design-rationale
      locator: https://kmi.open.ac.uk/publications/techreport/kmi-95-14；摘要首句；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/nygard-2011-architecture-decisions
    field: version
    value: '2011-11-15'
  - identity: entities/nygard-2011-architecture-decisions
    field: basis.version
    value:
    - entity: nygard-2011-architecture-decisions
      locator: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions；superseded与保留旧决定正文；实际取证见 work/reviews/2026-09-06-term-governance-coverage.json、work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/w3c-xml-1-0
    field: version
    value: '2008-11-26'
  - identity: entities/w3c-xml-1-0
    field: basis.version
    value:
    - entity: w3c-xml-1-0
      locator: https://www.w3.org/TR/REC-xml/；§3.2.1 Element Content；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/gertz-1974
    field: version
    value: '1974-06-25'
  - identity: entities/gertz-1974
    field: basis.version
    value:
    - entity: gertz-1974
      locator: https://www.law.cornell.edu/supremecourt/text/418/323；345、351–352；原作者发表仍非public figure；一般/特定争议两类；实际取证见 work/reviews/2026-09-06-term-governance-coverage.json、work/reviews/2026-09-06-term-resolution-final-semantics.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/owl2-primer
    field: version
    value: '2012-12-11'
  - identity: entities/owl2-primer
    field: basis.version
    value:
    - entity: owl2-primer
      locator: https://www.w3.org/TR/owl2-primer/；§3/4.1/4.7 individuals；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/cornell-cs3110-2012-partition
    field: version
    value: 2012 Fall
  - identity: entities/cornell-cs3110-2012-partition
    field: basis.version
    value:
    - entity: cornell-cs3110-2012-partition
      locator: https://www.cs.cornell.edu/courses/cs3110/2012fa/recitations/rec14.html；首段partition定义；实际取证见 work/reviews/2026-09-06-term-resolution-concepts.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/krathwohl-2002-taxonomy
    field: version
    value: '2002'
  - identity: entities/krathwohl-2002-taxonomy
    field: basis.version
    value:
    - entity: krathwohl-2002-taxonomy
      locator: https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf；PDF index2–5/印刷214–217 Cognitive
        Process dimension；实际取证见 work/reviews/2026-09-06-term-content-coverage.json、work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/iso-37000-2021
    field: version
    value: '2021'
  - identity: entities/iso-37000-2021
    field: basis.version
    value:
    - entity: iso-37000-2021
      locator: https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf；§3.1.1 PDF9/印刷1；§3.2.9
        PDF12/印刷4；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/oecd-2024-evaluation-glossary-en-zh
    field: version
    value: Second edition, 2024, EN-ZH
  - identity: entities/oecd-2024-evaluation-glossary-en-zh
    field: basis.version
    value:
    - entity: oecd-2024-evaluation-glossary-en-zh
      locator: https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf；Monitoring
        PDF39；Evaluation PDF29；Indicator PDF35；实际取证见 work/reviews/2026-09-06-term-resolution-governance.json、work/reviews/2026-09-06-term-resolution-knowledge-governance.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/w3c-rdf-semantics-2004
    field: version
    value: '2004-02-10'
  - identity: entities/w3c-rdf-semantics-2004
    field: basis.version
    value:
    - entity: w3c-rdf-semantics-2004
      locator: https://www.w3.org/TR/rdf-mt/；AppendixB Inference；L1282；实际取证见 work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/iso-39075-2024
    field: version
    value: '2024'
  - identity: entities/iso-39075-2024
    field: basis.version
    value:
    - entity: iso-39075-2024
      locator: https://www.iso.org/standard/76120.html；Abstract，Edition1，2024-04；实际取证见 work/reviews/2026-09-06-term-resolution-summary.json、work/reviews/2026-09-06-term-resolution-web.json
      checked: '2026-09-06'
  - identity: entities/iso-24495-1
    field: version
    value: '2023'
  - identity: entities/iso-24495-1
    field: basis.version
    value:
    - entity: iso-24495-1
      locator: https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf；免费样章 PDF
        p. 9（印刷 p. 3），§4 Governing principles；PDF pp. 9–11（印刷 pp. 3–5），§5.1 与 §5.2.1–§5.2.3。；实际取证见 work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/francis-et-al-2018-cypher
    field: version
    value: '2018'
  - identity: entities/francis-et-al-2018-cypher
    field: basis.version
    value:
    - entity: francis-et-al-2018-cypher
      locator: https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf；作者稿 PDF p. 2（论文 p. 1433），Abstract 与 §1；PDF
        p. 3（论文 p. 1434），§2 The Cypher Language。；实际取证见 work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/lamb-zacchiroli-2021-reproducible-builds
    field: version
    value: arXiv v1
  - identity: entities/lamb-zacchiroli-2021-reproducible-builds
    field: basis.version
    value:
    - entity: lamb-zacchiroli-2021-reproducible-builds
      locator: https://arxiv.org/pdf/2104.06020v1；arXiv:2104.06020v1，PDF p. 2，Reproducible Builds，Definition 1。；实际取证见 work/reviews/2026-09-06-term-definition-source-resolution.json、work/reviews/2026-09-06-term-resolution-summary.json
      checked: '2026-09-06'
  - identity: entities/nist-sp-800-53r5
    field: version
    value: Revision 5 (updates 2020-12-10)
  - identity: entities/nist-sp-800-53r5
    field: basis.version
    value:
    - entity: nist-sp-800-53r5
      locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；封面：Revision 5，September 2020，includes
        updates as of 2020-12-10；PDF p. 422，Appendix A p. 395，audit 与 audit trail
      checked: '2026-09-06'
  - identity: entities/american-heritage-dictionary-5-cheat-sheet
    field: version
    value: Fifth Edition (2022)
  - identity: entities/american-heritage-dictionary-5-cheat-sheet
    field: basis.version
    value:
    - entity: american-heritage-dictionary-5-cheat-sheet
      locator: 官方 AHD 条目 cheat sheet；义项 2；页面明确标注 The American Heritage Dictionary of the English Language, Fifth Edition copyright
        ©2022 by HarperCollins Publishers
      checked: '2026-09-06'
  - identity: entities/dnd-caf-data-governance
    field: version
    value: '2022-07-28'
  - identity: entities/dnd-caf-data-governance
    field: basis.version
    value:
    - entity: dnd-caf-data-governance
      locator: 独立政府框架全文；Page details 2022-07-28；Appendix B data governance；§6.4.2 Chief Data Officer；§6.4.3.1 Data Governors
      checked: '2026-09-06'
  - identity: entities/dfe-external-governance-reviews
    field: version
    value: '2026-08-11'
  - identity: entities/dfe-external-governance-reviews
    field: basis.version
    value:
    - entity: dfe-external-governance-reviews
      locator: Department for Education guidance；Published 2022-05-20；所读版 Last updated 2026-08-11；Updates to this page 记录该版变更；Benefits
        of an external governance review；Setting the scope and objectives
      checked: '2026-09-06'
---

# 术语来源采纳

用户于 2026-09-06 采纳[完整来源提案](../../work/reviews/2026-09-06-term-complete-source-candidate.md)及其逐项实体值。本决定登记 51 条来源，复用的既有来源保持原值；不新建 structure、mapping 或其他来源用途记录。

## 版本与历史

Q01 采纳完整实体值，Q02 精确采纳非空 version 及其 basis.version。source-registration 历史记录本次真实登记，added 记录实际建立日期；材料 checked、出版版本与原阅读判断不因登记而重写。review.checked 为空的项目仍保持未进行整体周期复核，不编造复核日期或义务。

NIST 审计与审计追踪使用同一固定 SP800-53 Rev.5 底本，速查表使用 AHD 第五版固定词典条目；DND／CAF 和 DfE 引用实际核到的独立发表版。它们的材料身份与版次见完整记录，不通过给动态门户改档取得定义资格。

## 用途边界

来源登记不是 publication 授权。现行 swebok、cs2023 和 iptc-genre 的 tier 及版本不改变；六条术语定义的例外见[限定定义许可](term-limited-definition-source-use.md)。官方摘要、作者文章、配套工件与标准完整正文的核对范围保持区分，不把实际未读材料变成已核依据。
