---
id: decision-source-data-batch
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: '2026-09-06'
level: L2
scope: source-data-batch
supersedes: []
answers:
- question: Q02
  resolution: replacement
  patches:
  - identity: '@control:schema'
    field: source_state_policy
    value:
      source_status_required: false
      missing_source_status: unverified
      version_required: true
      null_version: no-verified-version-recorded
      unversioned_de_facto_structure: false
- question: Q05
  resolution: replacement
  patches:
  - identity: entities/gbt-13745
    field: version
    value: '2009'
  - identity: entities/gbt-13745
    field: basis.version
    value:
    - entity: gbt-13745
      locator: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E；标准号与发布日期
      checked: '2026-09-05'
  - identity: entities/cs2023
    field: version
    value: 2024-01
  - identity: entities/cs2023
    field: basis.version
    value:
    - entity: cs2023
      locator: https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm；2024
        年 1 月定稿，3 月编辑
      checked: '2026-09-05'
  - identity: entities/cwe
    field: version
    value: '4.20'
  - identity: entities/cwe
    field: basis.version
    value:
    - entity: cwe
      locator: https://cwe.mitre.org/news/archives/news2026.html；4.20，2026-04-30 发布
      checked: '2026-09-05'
  - identity: entities/attack
    field: version
    value: '19.2'
  - identity: entities/attack
    field: basis.version
    value:
    - entity: attack
      locator: https://attack.mitre.org/resources/versions/；Current Version v19.2
      checked: '2026-09-05'
  - identity: entities/owasp-llm-top10
    field: version
    value: '2025'
  - identity: entities/owasp-llm-top10
    field: basis.version
    value:
    - entity: owasp-llm-top10
      locator: https://genai.owasp.org/llm-top-10/；LLM01:2025 等条目标识
      checked: '2026-09-05'
  - identity: entities/atlas
    field: version
    value: '2026.07'
  - identity: entities/atlas
    field: basis.version
    value:
    - entity: atlas
      locator: https://github.com/mitre-atlas/atlas-data/tree/main/dist/v6；ATLAS-2026.07.yaml
        文件名，blob 275c840f6e6ccc2b7be9fe8607fdc3344c242a42，仅目录元数据
      checked: '2026-09-05'
  - identity: entities/nist-ai-rmf
    field: version
    value: '1.0'
  - identity: entities/nist-ai-rmf
    field: basis.version
    value:
    - entity: nist-ai-rmf
      locator: https://www.nist.gov/itl/ai-risk-management-framework；1.0，2023-01-26
        发布
      checked: '2026-09-05'
  - identity: entities/rfc-1122
    field: version
    value: '1989'
  - identity: entities/rfc-1122
    field: basis.version
    value:
    - entity: rfc-1122
      locator: https://www.rfc-editor.org/info/rfc1122/；RFC 1122 发布年份
      checked: '2026-09-05'
  - identity: entities/rfc-9110
    field: version
    value: '2022'
  - identity: entities/rfc-9110
    field: basis.version
    value:
    - entity: rfc-9110
      locator: https://datatracker.ietf.org/doc/rfc9110/；June 2022
      checked: '2026-09-05'
  - identity: entities/osi
    field: version
    value: '1994'
  - identity: entities/osi
    field: basis.version
    value:
    - entity: osi
      locator: https://www.iso.org/standard/20269.html；ISO/IEC 7498-1:1994
      checked: '2026-09-05'
  - identity: entities/mdn-curriculum
    field: version
    value: 2025-10
  - identity: entities/mdn-curriculum
    field: basis.version
    value:
    - entity: mdn-curriculum
      locator: https://developer.mozilla.org/en-US/curriculum/；Last updated October
        2025，仅更新月份
      checked: '2026-09-05'
  - identity: entities/teachyourselfcs
    field: version
    value: '2020'
  - identity: entities/teachyourselfcs
    field: basis.version
    value:
    - entity: teachyourselfcs
      locator: https://teachyourselfcs.com/；May 2020 更新，保留年份精度
      checked: '2026-09-05'
  - identity: entities/cmu-15-445
    field: version
    value: Fall 2025
  - identity: entities/cmu-15-445
    field: basis.version
    value:
    - entity: cmu-15-445
      locator: https://15445.courses.cs.cmu.edu/fall2025/；Fall 2025 归档
      checked: '2026-09-05'
  - identity: entities/lom
    field: version
    value: '2002'
  - identity: entities/lom
    field: basis.version
    value:
    - entity: lom
      locator: https://standards.ieee.org/ieee/1484.12.1/3294/；IEEE 1484.12.1-2002
        出版身份
      checked: '2026-09-05'
  - identity: entities/schema-org
    field: version
    value: '30.0'
  - identity: entities/schema-org
    field: basis.version
    value:
    - entity: schema-org
      locator: https://schema.org/version/latest；30.0 stable release，2026-03-19
      checked: '2026-09-05'
  - identity: entities/gbt-13745
    field: source_status
    value: current
  - identity: entities/gbt-13745
    field: basis.source_status
    value:
    - entity: gbt-13745
      locator: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E；标准号与发布日期；现行状态
      checked: '2026-09-05'
  - identity: entities/attack
    field: source_status
    value: current
  - identity: entities/attack
    field: basis.source_status
    value:
    - entity: attack
      locator: https://attack.mitre.org/resources/versions/；Current Version v19.2
      checked: '2026-09-05'
  - identity: entities/owasp-top10
    field: source_status
    value: superseded
  - identity: entities/owasp-top10
    field: basis.source_status
    value:
    - entity: owasp-top10
      locator: https://owasp.org/www-project-top-ten/；current 2025 与旧版 2021，限定选用版本地位
      checked: '2026-09-05'
  - identity: entities/osi
    field: source_status
    value: current
  - identity: entities/osi
    field: basis.source_status
    value:
    - entity: osi
      locator: https://www.iso.org/standard/20269.html；仍现行，阶段 90.93
      checked: '2026-09-05'
  - identity: entities/skos
    field: source_status
    value: current
  - identity: entities/skos
    field: basis.source_status
    value:
    - entity: skos
      locator: https://www.w3.org/standards/history/skos-reference/；最新 Recommendation
        为 2009-08-18，区别被替代 SKOS Core
      checked: '2026-09-05'
  - identity: entities/lom
    field: source_status
    value: superseded
  - identity: entities/lom
    field: basis.source_status
    value:
    - entity: lom
      locator: https://standards.ieee.org/ieee/1484.12.1/3294/；Status Superseded，Superseded
        by 2020
      checked: '2026-09-05'
  - identity: entities/schema-org
    field: source_status
    value: current
  - identity: entities/schema-org
    field: basis.source_status
    value:
    - entity: schema-org
      locator: https://schema.org/version/latest；30.0 stable release，2026-03-19
      checked: '2026-09-05'
  - identity: entities/gbt-13745
    field: urls
    value:
    - role: landing
      url: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E
      primary: true
  - identity: entities/gbt-13745
    field: basis.urls
    value:
    - entity: gbt-13745
      locator: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E
      checked: '2026-09-05'
  - identity: entities/cs2023
    field: urls
    value:
    - role: landing
      url: https://csed.acm.org/final-report/
      primary: true
    - role: full_text
      url: https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm
      primary: false
  - identity: entities/cs2023
    field: basis.urls
    value:
    - entity: cs2023
      locator: https://csed.acm.org/final-report/
      checked: '2026-09-05'
    - entity: cs2023
      locator: https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm
      checked: '2026-09-05'
  - identity: entities/asvs
    field: urls
    value:
    - role: landing
      url: https://owasp.org/www-project-application-security-verification-standard/
      primary: true
  - identity: entities/asvs
    field: basis.urls
    value:
    - entity: asvs
      locator: https://owasp.org/www-project-application-security-verification-standard/
      checked: '2026-09-05'
  - identity: entities/attack
    field: urls
    value:
    - role: landing
      url: https://attack.mitre.org/resources/versions/
      primary: true
  - identity: entities/attack
    field: basis.urls
    value:
    - entity: attack
      locator: https://attack.mitre.org/resources/versions/
      checked: '2026-09-05'
  - identity: entities/owasp-top10
    field: urls
    value:
    - role: landing
      url: https://owasp.org/www-project-top-ten/
      primary: true
  - identity: entities/owasp-top10
    field: basis.urls
    value:
    - entity: owasp-top10
      locator: https://owasp.org/www-project-top-ten/
      checked: '2026-09-05'
  - identity: entities/atlas
    field: urls
    value:
    - role: landing
      url: https://github.com/mitre-atlas/atlas-data/tree/main/dist/v6
      primary: true
  - identity: entities/atlas
    field: basis.urls
    value:
    - entity: atlas
      locator: https://github.com/mitre-atlas/atlas-data/tree/main/dist/v6
      checked: '2026-09-05'
  - identity: entities/nist-ai-rmf
    field: urls
    value:
    - role: landing
      url: https://www.nist.gov/itl/ai-risk-management-framework
      primary: true
  - identity: entities/nist-ai-rmf
    field: basis.urls
    value:
    - entity: nist-ai-rmf
      locator: https://www.nist.gov/itl/ai-risk-management-framework
      checked: '2026-09-05'
  - identity: entities/anthropic-docs
    field: urls
    value:
    - role: landing
      url: https://platform.claude.com/docs/en/home
      primary: true
  - identity: entities/anthropic-docs
    field: basis.urls
    value:
    - entity: anthropic-docs
      locator: https://platform.claude.com/docs/en/home
      checked: '2026-09-05'
  - identity: entities/rfc-1122
    field: urls
    value:
    - role: landing
      url: https://www.rfc-editor.org/info/rfc1122/
      primary: true
  - identity: entities/rfc-1122
    field: basis.urls
    value:
    - entity: rfc-1122
      locator: https://www.rfc-editor.org/info/rfc1122/
      checked: '2026-09-05'
  - identity: entities/rfc-9110
    field: urls
    value:
    - role: landing
      url: https://datatracker.ietf.org/doc/rfc9110/
      primary: true
  - identity: entities/rfc-9110
    field: basis.urls
    value:
    - entity: rfc-9110
      locator: https://datatracker.ietf.org/doc/rfc9110/
      checked: '2026-09-05'
  - identity: entities/osi
    field: urls
    value:
    - role: landing
      url: https://www.iso.org/standard/20269.html
      primary: true
  - identity: entities/osi
    field: basis.urls
    value:
    - entity: osi
      locator: https://www.iso.org/standard/20269.html
      checked: '2026-09-05'
  - identity: entities/mdn
    field: urls
    value:
    - role: landing
      url: https://developer.mozilla.org/en-US/docs/Web
      primary: true
  - identity: entities/mdn
    field: basis.urls
    value:
    - entity: mdn
      locator: https://developer.mozilla.org/en-US/docs/Web
      checked: '2026-09-05'
  - identity: entities/mdn-curriculum
    field: urls
    value:
    - role: landing
      url: https://developer.mozilla.org/en-US/curriculum/
      primary: true
  - identity: entities/mdn-curriculum
    field: basis.urls
    value:
    - entity: mdn-curriculum
      locator: https://developer.mozilla.org/en-US/curriculum/
      checked: '2026-09-05'
  - identity: entities/iso-25964-1
    field: urls
    value:
    - role: landing
      url: https://www.iso.org/standard/53657.html
      primary: true
  - identity: entities/iso-25964-1
    field: basis.urls
    value:
    - entity: iso-25964-1
      locator: https://www.iso.org/standard/53657.html
      checked: '2026-09-05'
  - identity: entities/iso-25964-2
    field: urls
    value:
    - role: landing
      url: https://www.iso.org/standard/53658.html
      primary: true
  - identity: entities/iso-25964-2
    field: basis.urls
    value:
    - entity: iso-25964-2
      locator: https://www.iso.org/standard/53658.html
      checked: '2026-09-05'
  - identity: entities/z39-19
    field: urls
    value:
    - role: landing
      url: https://www.niso.org/publications/ansiniso-z3919-2005-r2010
      primary: true
    - role: doi
      url: https://doi.org/10.3789/ansi.niso.z39.19-2005R2010
      primary: false
    - role: full_text
      url: https://groups.niso.org/higherlogic/ws/public/download/12591/z39-19-2005r2010.pdf
      primary: false
  - identity: entities/z39-19
    field: basis.urls
    value:
    - entity: z39-19
      locator: https://www.niso.org/publications/ansiniso-z3919-2005-r2010
      checked: '2026-09-05'
    - entity: z39-19
      locator: https://doi.org/10.3789/ansi.niso.z39.19-2005R2010
      checked: '2026-09-05'
    - entity: z39-19
      locator: https://groups.niso.org/higherlogic/ws/public/download/12591/z39-19-2005r2010.pdf
      checked: '2026-09-05'
  - identity: entities/skos
    field: urls
    value:
    - role: canonical
      url: https://www.w3.org/TR/skos-reference/
      primary: true
  - identity: entities/skos
    field: basis.urls
    value:
    - entity: skos
      locator: https://www.w3.org/TR/skos-reference/
      checked: '2026-09-05'
  - identity: entities/roadmap-sh
    field: urls
    value:
    - role: landing
      url: https://roadmap.sh/
      primary: true
  - identity: entities/roadmap-sh
    field: basis.urls
    value:
    - entity: roadmap-sh
      locator: https://roadmap.sh/
      checked: '2026-09-05'
  - identity: entities/teachyourselfcs
    field: urls
    value:
    - role: landing
      url: https://teachyourselfcs.com/
      primary: true
  - identity: entities/teachyourselfcs
    field: basis.urls
    value:
    - entity: teachyourselfcs
      locator: https://teachyourselfcs.com/
      checked: '2026-09-05'
  - identity: entities/cmu-15-445
    field: urls
    value:
    - role: archive
      url: https://15445.courses.cs.cmu.edu/fall2025/
      primary: true
  - identity: entities/cmu-15-445
    field: basis.urls
    value:
    - entity: cmu-15-445
      locator: https://15445.courses.cs.cmu.edu/fall2025/
      checked: '2026-09-05'
  - identity: entities/lom
    field: urls
    value:
    - role: landing
      url: https://standards.ieee.org/ieee/1484.12.1/3294/
      primary: true
  - identity: entities/lom
    field: basis.urls
    value:
    - entity: lom
      locator: https://standards.ieee.org/ieee/1484.12.1/3294/
      checked: '2026-09-05'
  - identity: entities/schema-org
    field: urls
    value:
    - role: landing
      url: https://schema.org/version/latest
      primary: true
  - identity: entities/schema-org
    field: basis.urls
    value:
    - entity: schema-org
      locator: https://schema.org/version/latest
      checked: '2026-09-05'
- question: Q11
  resolution: replacement
  patches:
  - identity: sources/gbt-13745
    field: entity
    value: gbt-13745
  - identity: sources/gbt-13745/roles/mapping
    field: status
    value: approved
  - identity: sources/gbt-13745/roles/structure
    field: status
    value: approved
  - identity: sources/cs2023
    field: entity
    value: cs2023
  - identity: sources/cs2023/roles/mapping
    field: status
    value: approved
  - identity: sources/cs2023/roles/structure
    field: status
    value: approved
  - identity: sources/asvs
    field: entity
    value: asvs
  - identity: sources/asvs/roles/mapping
    field: status
    value: approved
  - identity: sources/cwe
    field: entity
    value: cwe
  - identity: sources/cwe/roles/mapping
    field: status
    value: approved
  - identity: sources/cwe/roles/structure
    field: status
    value: approved
  - identity: sources/attack
    field: entity
    value: attack
  - identity: sources/attack/roles/mapping
    field: status
    value: approved
  - identity: sources/attack/roles/structure
    field: status
    value: approved
  - identity: sources/owasp-llm-top10
    field: entity
    value: owasp-llm-top10
  - identity: sources/owasp-llm-top10/roles/mapping
    field: status
    value: approved
  - identity: sources/owasp-llm-top10/roles/structure
    field: status
    value: approved
  - identity: sources/atlas
    field: entity
    value: atlas
  - identity: sources/atlas/roles/mapping
    field: status
    value: approved
  - identity: sources/rfc-1122
    field: entity
    value: rfc-1122
  - identity: sources/rfc-1122/roles/mapping
    field: status
    value: approved
  - identity: sources/rfc-1122/roles/structure
    field: status
    value: approved
  - identity: sources/diataxis
    field: entity
    value: diataxis
  - identity: sources/diataxis/roles/mapping
    field: status
    value: approved
  - identity: sources/wikidata
    field: entity
    value: wikidata
  - identity: sources/wikidata/roles/mapping
    field: status
    value: approved
  - identity: sources/dita
    field: entity
    value: dita
  - identity: sources/dita/roles/mapping
    field: status
    value: approved
  - identity: sources/iptc-genre
    field: entity
    value: iptc-genre
  - identity: sources/iptc-genre/roles/mapping
    field: status
    value: approved
  - identity: sources/lom
    field: entity
    value: lom
  - identity: sources/lom/roles/mapping
    field: status
    value: approved
  - identity: sources/schema-org
    field: entity
    value: schema-org
  - identity: sources/schema-org/roles/mapping
    field: status
    value: approved
- question: Q13
  resolution: replacement
  patches:
  - identity: topics/concepts/mathematics
    field: assertions
    value:
      source:
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/topics.yaml#concepts/mathematics.source
  - identity: topics/concepts/information-and-systems-science
    field: assertions
    value:
      source:
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/topics.yaml#concepts/information-and-systems-science.source
  - identity: topics/concepts/computing
    field: assertions
    value:
      source:
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/topics.yaml#concepts/computing.source
  - identity: topics/concepts/management
    field: assertions
    value:
      source:
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/topics.yaml#concepts/management.source
  - identity: topics/concepts/linguistics
    field: assertions
    value:
      source:
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/topics.yaml#concepts/linguistics.source
  - identity: topics/concepts/journalism-and-communication
    field: assertions
    value:
      source:
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/topics.yaml#concepts/journalism-and-communication.source
  - identity: topics/concepts/library-and-information-science
    field: assertions
    value:
      source:
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/topics.yaml#concepts/library-and-information-science.source
  - identity: topics/concepts/education
    field: assertions
    value:
      source:
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/topics.yaml#concepts/education.source
- question: Q16
  resolution: replacement
  patches:
  - identity: forms/arrays/forms-presentation
    field: local_analysis
    value:
      legacy_source_label: lom
      state: isolated
      decision: decision-source-0011
  - identity: forms/arrays/forms-activity
    field: local_analysis
    value:
      legacy_source_label: lom
      state: isolated
      decision: decision-source-0011
- question: Q18
  resolution: replacement
  patches:
  - identity: types/types/explanation
    field: match
    value:
    - registry: diataxis
      item: explanation
      rel: exactMatch
      basis:
      - entity: diataxis
        locator: https://diataxis.fr/explanation/#admit-opinion-and-perspective；开篇、boundaries
          与观点范围
        checked: '2026-09-05'
  - identity: genres/genres/analysis
    field: match
    value:
    - registry: iptc-genre
      item: http://cv.iptc.org/newscodes/genre/Analysis
      rel: closeMatch
      basis:
      - entity: iptc-genre
        locator: https://cv.iptc.org/newscodes/genre/Analysis；Concept ID 与 Definition，保留新闻语境和本地个人理解范围之差
        checked: '2026-09-05'
  - identity: entities/entities/obsidian
    field: match
    value:
    - registry: wikidata
      item: Q103994532
      rel: exactMatch
      basis:
      - entity: wikidata
        locator: https://www.wikidata.org/w/index.php?title=Q103994532&oldid=2530661391；软件身份、P31、P856；与
          https://obsidian.md/ 产品身份交叉核对
        checked: '2026-09-05'
- question: Q20
  resolution: replacement
  patches:
  - identity: entities/gbt-13745
    field: assertions
    value:
      subjects:
      - values:
        - library-and-information-science
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/gbt-13745.basis.subjects
  - identity: entities/diataxis
    field: assertions
    value:
      subjects:
      - values:
        - software-engineering
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/diataxis.basis.subjects
  - identity: entities/wikidata
    field: assertions
    value:
      subjects:
      - values:
        - library-and-information-science
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/wikidata.basis.subjects
  - identity: entities/roadmap-sh
    field: assertions
    value:
      subjects:
      - values:
        - computing
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/roadmap-sh.basis.subjects
  - identity: entities/teachyourselfcs
    field: assertions
    value:
      subjects:
      - values:
        - computing
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/teachyourselfcs.basis.subjects
  - identity: entities/schema-org
    field: assertions
    value:
      subjects:
      - values:
        - information-science
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/schema-org.basis.subjects
  - identity: entities/anthropic
    field: assertions
    value:
      subjects:
      - values:
        - artificial-intelligence
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/anthropic.basis.subjects
  - identity: entities/openai
    field: assertions
    value:
      subjects:
      - values:
        - artificial-intelligence
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/openai.basis.subjects
  - identity: entities/moonshot-ai
    field: assertions
    value:
      subjects:
      - values:
        - artificial-intelligence
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/moonshot-ai.basis.subjects
  - identity: entities/astral
    field: assertions
    value:
      subjects:
      - values:
        - software-engineering
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/astral.basis.subjects
  - identity: entities/oxc
    field: assertions
    value:
      subjects:
      - values:
        - tools-and-environments
        - web-platforms
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/oxc.basis.subjects
  - identity: entities/uv
    field: assertions
    value:
      subjects:
      - values:
        - tools-and-environments
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/uv.basis.subjects
  - identity: entities/pydantic
    field: assertions
    value:
      subjects:
      - values:
        - web-platforms
        - foundations-of-programming-languages
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/pydantic.basis.subjects
  - identity: entities/obsidian
    field: assertions
    value:
      subjects:
      - values:
        - computing
        disposition: project_assertion
        original: self
        migration: git:633f6842be6c7aac1683dbf517b87d3d76447f69:data/vocab/entities.yaml#entities/obsidian.basis.subjects
---
# 来源批次采纳

状态：已采纳。用户对[集中提案](../../work/reviews/2026-09-06-source-data-proposals.md)明确回复“采纳上述建议，继续整批实施”。本记录列出本次可执行的精确字段、角色与关系；不把提案中“待核”或附有尚未满足条件的值写成已采纳事实。

## 状态规则

source_status 可省略，缺值表示外部状态未核实，不是 current、不适用或 unknown；有值仍要求发布者依据与精确采纳。version 键保留，null 仅表示未登记可核实版本，不宣称发布者没有版本。无版本 de-facto 仍不能取得 structure。此规则仅取代[字段合同](source-v2-field-contract.md)及方案中外部状态必填的要求，其余严格引用、权限及保留规则继续有效。依赖现行状态的操作不得把缺值当作满足。

## 值的范围

front matter 承接明确有证据的版本、状态与地址，以及提案明确推荐批准的用途。ASVS 的版本精度尚有条件，SWEBOK 与 DITA 换版、未核版本和替代实体身份均未因此批准。P1–P4 继续按[既有字段记录](source-field-values.md)生效，原证据日期不覆盖；同一字段有本次新观察时明确保留两次历史，而非改写旧记录。

24 项本地保留采用[逐记录库存](../../work/reviews/2026-09-06-source-migration-inventory.json)中的原值和 Git 定位：14 项 subjects 项目判断、8 项 source:self、2 项载体数组。原 ID、subjects 值、父项、成员与项目状态不变；项目判断不成为外部事实。决定没有把相邻尚未核实的映射一并批准。

本次仅批准 explanation、analysis、obsidian 的三条明确关系及其列出的依据。其余映射、派生与外部分组仍逐项取证；CS2023 代码名定位不替代关系证明。角色许可不替代实体完整性或具体关系许可。

## 执行边界

这不是正式切换或发版决定。当前未核字段、GB/T 修改单影响、watch 与全面 review 等仍按实际证据处置，不造默认事实，不删除对象使校验通过。使用 Git 保存隔离分支；全部数据与消费者验收完成前不合并 master，不修改正式 vault。
