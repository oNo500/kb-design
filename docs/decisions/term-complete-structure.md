---
id: decision-term-complete-structure
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: '2026-09-06'
level: L3
scope: 所列项目basis、glossary布局和条件式执行范围；publication仍待验收
supersedes: []
answers:
- question: Q01
  resolution: recommended
  patches:
  - identity: '@control:terms'
    field: project_basis_extension
    value:
      concept_and_definition_ids:
      - tc-56bf269d-a675-4fc3-a2c1-b1f38a734d81
      - tc-9db2bd8b-938e-4752-865f-bec2da9c4083
      - tc-549c1bed-5db4-4073-aaab-bf23c9be47ac
      term_basis_forms:
      - concept_id: tc-9db2bd8b-938e-4752-865f-bec2da9c4083
        term_id: tm-657b1a85-79d5-44c1-b355-f37b4e7aff07
        language: en
        text: assertion
      - concept_id: tc-549c1bed-5db4-4073-aaab-bf23c9be47ac
        term_id: tm-1facfe30-6843-4a4a-989d-a7d8338cf57f
        language: en
        text: threshold
      basis_shape:
        project:
          approval: decision-term-data-values
          origin:
            commit: existing pre-migration Git commit
            file: existing project source path
            locator: specific existing rule or registration
          rationale: inherit only the listed existing project meaning
      require_exact_l3_record_and_project_basis_scope: true
      chinese_model_basis_separate: true
      arbitrary_external_evidence_fallback: false
      arbitrary_english_model_basis: false
- question: Q02
  resolution: recommended
  patches:
  - identity: '@control:terms'
    field: glossary_layout
    value:
      schema: urn:kb-design:layout:glossary:2
      version: 2
      groups:
      - id: vocabulary-types
        title: 词表的类型
        order: 1
        members:
        - tc-6908a022-5a5a-43e0-b895-4414bba97169
        - tc-94e9bdfe-cefd-445c-9a12-f276bfe75e63
        - tc-c5f2ed53-7f7e-40a1-8c89-a07dac98107b
        - tc-c6190e59-1353-4f22-8a93-b3077b486884
        - tc-4f002e0f-1fe2-41e5-a15c-3cdb436b1763
        - tc-5c7a2951-c99c-4597-baa5-c6eb7fd7c5e4
        - tc-9d793546-528c-4b51-8a37-801df07342f3
        - tc-c7d6f1d5-2139-4d42-857d-7c16fa507b31
      - id: basic-unit
        title: 基本单位
        order: 2
        members:
        - tc-c960c1a6-3e65-4075-801a-876b1d3b2f57
        - tc-84906e82-1b72-4118-951c-33416d9d9bf7
        - tc-c1473abd-3fc6-4570-bf19-cbb27b944fc2
        - tc-75fa8baa-d6ec-400e-b90f-5039371a2d57
        - tc-c5ee911a-276c-4bc1-81e7-f651972b0830
        - tc-57a8d816-05c4-4aa9-b3da-277b5d23cc4e
        - tc-dc59744d-a530-44b7-9de8-77e2766710e7
        - tc-26a41c49-f435-4527-b419-de688657db90
        - tc-d58d9afb-92ca-46c1-b928-e6ea6c2a11a6
        - tc-adbb6019-db11-4d1e-a9b2-4e7a8fedd0a5
        - tc-a977c939-c9fe-477b-a154-a0ccd97aa3d6
        - tc-b0214996-65e1-4d37-a055-b7356a776ac0
        - tc-6a20995f-a6b2-492a-88e9-a554c8364fe2
        - tc-a8e5c450-33ff-42e5-a352-1bbb21fcd0b5
        - tc-7f29a362-cc5b-481a-87df-67ff11c9c068
      - id: relations
        title: 关系
        order: 3
        members:
        - tc-75e8012c-351f-4303-b8c0-523454b9b730
        - tc-ad90ba40-f5b0-44e7-9f59-fa2783d837b3
        - tc-278494cf-719c-43f9-b954-2a54c61e5c45
        - tc-54e74c2d-103e-4935-aab7-fb44a129af69
        - tc-818463b8-0d48-4ddf-98fb-228ef4591308
        - tc-9fde9fd8-eb29-4477-acc1-295f9de9adf5
        - tc-589f6145-5330-4773-b2dd-27eeeaa6bc84
        - tc-a529619b-cbcb-4545-901d-54f72971e76f
        - tc-df2d8160-1717-4372-a38f-db96925ac980
        - tc-1b0b91bc-d29e-44d4-854c-cddd05aebc13
        - tc-39065fa2-767d-4606-840c-aaffa5182661
        - tc-025cc053-edb1-4def-a58f-1de00a8424a4
        - tc-b10cded9-f3ab-4cdd-b218-edb279779c33
      - id: structure
        title: 结构
        order: 4
        members:
        - tc-1fa87658-bf07-4540-a863-a4e98a2fa888
        - tc-99e3245e-2f51-45d0-ba40-800d645f7f1f
        - tc-a5b2fb0f-5cea-4d47-8629-04694918cbf9
        - tc-af0edf3d-0500-4fc7-bad0-39127321295c
        - tc-7d9ce2a6-2d92-49c3-8d22-c771cdaae4c3
        - tc-2cc8c45b-bf02-4b54-bbfc-86286dbd50d7
        - tc-6d0b88b7-c403-48bf-9579-b2d94dbf9502
        - tc-6e6f7a15-910d-483e-b06c-3e3938aed39b
        - tc-c09e918a-cc3f-423c-bbca-c40c6766ef28
        - tc-6ce2328c-e952-40b8-b7d5-fd8dd958d0b7
        - tc-6bd16590-fd5e-4cee-9c8b-881051af3706
        - tc-81fc1070-a33d-4692-b613-751819cecc3b
        - tc-2f3dc564-3adc-46d7-ba3c-4051eaaa434c
        - tc-a4f76dad-bbea-4cf0-b322-1c689c380d95
        - tc-7fd3d9b0-be29-4f3c-a5a6-7817f26d9391
        - tc-7cee3db8-8807-48b2-9fe8-7f0fe0539272
      - id: annotations-lifecycle
        title: 注释与生命周期
        order: 5
        members:
        - tc-74b2becc-3bbe-45b5-8d42-bda67dcc17f8
        - tc-549f2d8d-7ddd-4bd3-b6e1-74e815f9feb2
        - tc-e7c36840-9dc5-45d1-a371-920c28af2a00
        - tc-d6a34d9f-e8f9-4170-9d62-e5b3676e71d9
        - tc-155c651f-9cb6-4e89-b394-9b843b268148
        - tc-a17e54a7-07e9-459e-86cc-bd0c12e4d58b
        - tc-82db3b46-353e-405f-8a8d-fd6fee70bdb5
        - tc-88088c7a-5aaf-458c-a55c-23ff38463ee0
        - tc-504af76c-f69e-469e-8e73-239f2fd3da99
        - tc-f4802cd3-fba8-4bb1-89a0-121eebbf1fc6
      - id: construction-governance
        title: 建设与治理
        order: 6
        members:
        - tc-d529a566-45fc-44f0-8b92-0eca58807137
        - tc-6cb09f56-afea-40d2-a986-c0d80d376363
        - tc-1ad36b83-83d4-4174-8cc0-a6189b8ce11b
        - tc-60cd4ded-814a-46d1-9bd6-360f1b725ca0
        - tc-ddf950fe-a885-4424-82f9-cfbb5d4ab330
        - tc-6f960f39-1a53-4215-932e-a89f837ac06c
        - tc-208354ed-1338-4152-be98-ca93504c3355
        - tc-c9b65491-09a6-4765-b208-6601af494f31
        - tc-8b56b1d2-7fd1-499b-8085-a9dd926e4c28
        - tc-b888a0b9-0011-4e55-b6a5-bb01e56b79aa
        - tc-f91d813f-7dfd-4aae-9198-756996799dd3
        - tc-b96d261a-9203-4f68-8b78-92e2667818ea
        - tc-60ca56e9-0bf5-4e06-86c4-b6941a9adc6e
        - tc-d123d909-3897-427f-9e04-e31d9072176c
        - tc-7e07c6f9-8677-4b87-8e32-e23d72dbfe64
        - tc-dfe493d2-f173-4a9e-ace9-b9ffad3f0f0f
        - tc-11e8d232-85f8-4e00-98a0-d8bdd7adf639
        - tc-98d2d330-cabe-493f-8453-104822e92a0d
      - id: vocabulary-mapping
        title: 词表间映射
        order: 7
        members:
        - tc-b544dcf4-e88e-4456-bb9e-824b74d7abc8
        - tc-c96ff99a-aef7-4d8d-b4d5-2c3e2835a64b
        - tc-c47ee168-3ad4-4489-bc26-1cc64f94407f
        - tc-dc56c863-cea8-485d-afcd-c606ce2a8a4b
        - tc-14b64c1a-938e-4d43-8e05-e18e0dd4e4f3
        - tc-b98ed928-3bbd-42a8-8f7f-b447c735b4c7
        - tc-405390d9-57dc-47ca-9317-0120d5aa86eb
        - tc-5d5225be-ab9d-44e4-866b-e321c998d766
        - tc-11c76a96-ef73-4369-9650-0f044c8eb0e7
        - tc-531f3821-4ee7-4345-831e-778371f56302
        - tc-4d6508b0-a334-4017-aa7d-205469ae902e
        - tc-64b64810-6aef-4db4-b09f-aa169129c448
        - tc-eb9e1973-6b39-47f1-8b3e-845798b14ba4
        - tc-bf5e9356-ac91-49ae-9be3-8196dd66167c
      - id: body-of-knowledge
        title: 知识体系
        order: 8
        members:
        - tc-e340f2b4-4515-4203-b5d1-8bafee5af81a
        - tc-3945b496-c4ac-4553-81ad-4c6dab62d81c
        - tc-89c27e71-9c5a-4e5e-a588-15c0ae59345d
        - tc-c5f9771f-7271-4128-854d-88b12df9f7ed
        - tc-fbe9f215-a5f4-4292-92fa-b734f6c4b3ee
      - id: metadata
        title: 元数据
        order: 9
        members:
        - tc-42c4b942-41ba-486e-903d-1f2f18e37e45
        - tc-99ace251-fdee-4ab9-93e8-a016e7e98127
        - tc-3f06d868-d7d2-4612-ad2b-35614912ba40
        - tc-30abb1cd-3364-4b41-a0e9-e0b8338aa348
        - tc-56bf269d-a675-4fc3-a2c1-b1f38a734d81
      - id: application-generation
        title: 应用与生成
        order: 10
        members:
        - tc-cb8ba91f-0bce-4b3d-ac6a-26bfca9ab7c9
        - tc-224b9f45-d624-4543-bc81-f64d02f81aa0
      - id: writing-design-methods
        title: 写作与设计方法
        order: 11
        members:
        - tc-2cdb43fb-ad5e-4aec-ad71-56eb596b78eb
        - tc-2938e52c-9172-4bc1-b3ea-a1c0476fe909
        - tc-973e68b6-1e0f-47a9-9ab7-0660d591969c
        - tc-9985f5e9-89cc-4fe1-849f-c2be99f97727
        - tc-327c7d8a-74ac-42b2-9022-da47959a339e
        - tc-fd033cdd-75b1-455c-9b39-431d1b9f3747
        - tc-a64c6780-fab4-4422-86ce-d8590dae3e52
        - tc-c484ee2c-a757-4f0f-9113-d2eda506c1bf
        - tc-c99988e5-3f77-492b-bd6e-aeca8e11ff6f
        - tc-2cc8a5dc-aa02-43fd-9cd7-f7fd9f3c3382
        - tc-9e03d16f-3787-4d16-9316-c46a686e0c03
        - tc-ceeab73a-dc10-4197-8bc0-8074a1eaba15
      - id: note-types
        title: 笔记的类型
        order: 12
        members:
        - tc-9e701a8f-b994-4a0d-8eab-3ea769ae1b6c
        - tc-1f71845d-b74c-4a84-84c8-3976145bd5f6
        - tc-e5c11065-dc49-4ac8-b297-aadb2edd1196
        - tc-80512a5e-8cde-40f7-8abe-896d973ee851
        - tc-5a5c6042-effa-4ebe-8a85-4560468e3adc
        - tc-2eb24dc0-1754-4f0b-a8c9-7239f29c1943
        - tc-78034548-e62f-4b31-9921-5b22e661d1ff
        - tc-505c5536-a7dd-4100-999a-fe0472b66b1c
        - tc-066aff06-6bef-4b2d-9870-f6ff7551db7f
        - tc-b49a8de0-d20e-42da-b7f0-f8d09ce44dc2
        - tc-9706ac56-d951-4eb6-9f27-cf7baa983a81
      - id: governance-maintenance
        title: 治理与维护
        order: 13
        members:
        - tc-aadb304c-3ed0-4f60-94cf-c968953d838c
        - tc-24c3f7b9-c6a2-4e1c-91f2-b3ee234219c8
        - tc-e61924e8-88b7-4c88-aaf2-5dad229a89ed
        - tc-09ff3cd6-f825-4e90-b401-4ef25c2cc084
        - tc-f881797d-c9ff-4f57-9523-b6a1c01c8b2c
        - tc-36a1e0f4-8fe1-459a-9083-b31022a1bda1
        - tc-9ebb317b-d01a-4852-a71f-463f595a50a4
        - tc-ec453431-dede-440d-87aa-40b745fea33a
        - tc-362abd86-fd94-42b4-8f6e-aaca8aa3660b
        - tc-9db2bd8b-938e-4752-865f-bec2da9c4083
        - tc-0aa7aa33-d7af-4c82-ad56-6efe59c4138c
        - tc-549c1bed-5db4-4073-aaab-bf23c9be47ac
        - tc-ab1c42d3-59d8-49db-9aa9-eebc09a98d6c
      - id: knowledge-graph
        title: 知识图谱
        order: 14
        members:
        - tc-589ad410-5fc7-4f1b-ba5a-fd06c366016f
        - tc-79c1fd4b-5f06-4d1e-a8d8-cd323c441939
        - tc-4aa4867f-ea92-4a56-a56f-e8ffe45c1f91
        - tc-95d07268-89f1-4c7f-86b0-98f60eeeef52
        - tc-605b0308-57af-486b-81ba-81e18b993b07
        - tc-daa1c79a-56f0-4d62-a360-ddaa9b332d0f
        - tc-e0ddd60c-cecf-4652-8b9d-2234f194a7a1
        - tc-acd244b6-0d82-4366-ac25-3fb7260c6473
        - tc-a07a37d8-13b6-4a9d-b86c-ba96f0c080b4
        - tc-b4f8bca4-b3cf-405b-8cf1-ea45112783d2
        - tc-e638bec2-4c85-4eed-9721-8175f5417f6d
        - tc-2633b390-938e-4c0b-9bec-deebf8f65e8b
        - tc-5c59be76-71b8-4e7e-8bd7-3763d8058473
        - tc-1141d95e-3a9c-4955-bb15-2e7ff25b4cf2
        - tc-5a533328-0f05-496f-b0dd-0436c4ef63b0
      source_abbreviations:
        id: source-abbreviations
        title: 出处缩写
        order: 0
        entries:
        - id: glossary-L0009
          cells:
          - ISO
          - ISO 25964-1:2011，后接条款号
          meaning: 来源缩写及展开，只作引用说明，不是术语概念。
          source_entity_ids:
          - iso-25964-1
        - id: glossary-L0010
          cells:
          - ISO-2
          - ISO 25964-2:2013，后接条款号
          meaning: 来源缩写及展开，只作引用说明，不是术语概念。
          source_entity_ids:
          - iso-25964-2
        - id: glossary-L0011
          cells:
          - Z
          - ANSI/NISO Z39.19-2005 (R2010)，后接条款号
          meaning: 来源缩写及展开，只作引用说明，不是术语概念。
          source_entity_ids:
          - z39-19
        - id: glossary-L0012
          cells:
          - SKOS
          - W3C SKOS Reference,2009
          meaning: 来源缩写及展开，只作引用说明，不是术语概念。
          source_entity_ids:
          - skos
        - id: glossary-L0013
          cells:
          - KG
          - Hogan et al., *Knowledge Graphs*, 2021
          meaning: 来源缩写及展开，只作引用说明，不是术语概念。
          source_entity_ids:
          - hogan-paper
        - id: glossary-L0014
          cells:
          - 自定
          - 本库自定，无外部来源
          meaning: 来源缩写及展开，只作引用说明，不是术语概念。
          source_entity_ids: []
          scope_note: 仅保留原出处缩写的项目用法说明，不自动给任何对象自定资格；3项目定义按精确project basis提案另处理。
      standards_appendix:
        id: cited-standards
        title: 引用的标准与文献
        order: 15
        entries:
        - id: glossary-L0233
          cells:
          - ISO 25964-1:2011 / -2:2013
          - 叙词表国际标准，见 [笔记](references/iso-25964.md)
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - ISO 25964-1:2011 / -2:2013
          - 叙词表国际标准，见 [笔记](references/iso-25964.md)
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0234
          cells:
          - GB/T 13190.1-2015 / .2-2018
          - 等同采用 ISO 25964 的国标
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - GB/T 13190.1-2015 / .2-2018
          - 等同采用 ISO 25964 的国标
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0235
          cells:
          - ANSI/NISO Z39.19-2005 (R2010)
          - 美国受控词表标准，全文免费
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - ANSI/NISO Z39.19-2005 (R2010)
          - 美国受控词表标准，全文免费
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0236
          cells:
          - ISO 704
          - 术语工作原则与方法，Wüster 理论的标准化版本；未核对
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - ISO 704
          - 术语工作原则与方法，Wüster 理论的标准化版本；未核对
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0237
          cells:
          - W3C SKOS / RDF / OWL / SPARQL
          - 语义网标准族
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - W3C SKOS / RDF / OWL / SPARQL
          - 语义网标准族
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0238
          cells:
          - ISO/IEC 39075:2024 GQL
          - 属性图查询语言标准
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - ISO/IEC 39075:2024 GQL
          - 属性图查询语言标准
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0239
          cells:
          - Cutter (1876)
          - 字典式目录规则，主题标目“一主题一词”的源头；未核对
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - Cutter (1876)
          - 字典式目录规则，主题标目“一主题一词”的源头；未核对
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0240
          cells:
          - Hulme (1911)
          - '*Principles of Book Classification*,Library Association Record 连载；文献依据的源头'
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - Hulme (1911)
          - '*Principles of Book Classification*,Library Association Record 连载；文献依据的源头'
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0241
          cells:
          - Dewey (1876)
          - 十进分类法；未核对
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - Dewey (1876)
          - 十进分类法；未核对
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0242
          cells:
          - Ranganathan (1933)
          - 冒号分类法，分面分析的源头；经 Z39.19 §5.3.4 转述
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - Ranganathan (1933)
          - 冒号分类法，分面分析的源头；经 Z39.19 §5.3.4 转述
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0243
          cells:
          - Wüster (1931)
          - 斯图加特博士论文 Internationale Sprachnormung in der Technik；术语学历史资料。旧登记的机构起源说明本批未核，不作为已核事实展示。
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - Wüster (1931)
          - 斯图加特博士论文 *Internationale Sprachnormung in der Technik*；术语学奠基，ISO/TC 37 1936 年由此成立
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0244
          cells:
          - Gruber (1993)
          - 计算机领域本体的定义；未核对
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - Gruber (1993)
          - 计算机领域本体的定义；未核对
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0245
          cells:
          - Hogan et al. (2021)
          - 知识图谱综述，[arXiv](https://arxiv.org/abs/2003.02320)
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - Hogan et al. (2021)
          - 知识图谱综述，[arXiv](https://arxiv.org/abs/2003.02320)
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
        - id: glossary-L0246
          cells:
          - Ehrlinger & Wöß (2016)
          - 知识图谱定义梳理，[CEUR](https://ceur-ws.org/Vol-1695/paper4.pdf)
          verification: 继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
          link_base: docs/glossary.md
          original_cells:
          - Ehrlinger & Wöß (2016)
          - 知识图谱定义梳理，[CEUR](https://ceur-ws.org/Vol-1695/paper4.pdf)
          display_notice: 既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
      reference_entries:
      - id: glossary-L0121
        section: 建设与治理
        cells:
        - 来源分级
        - de-jure / de-facto / vendor / archival
        - 来源记录的分档值，影响可用引用用途与复核周期；具体分档、用途限制和变更须遵循现行来源规则。Z39.19的组织依据说明项目选择的依据，不定义这四个档次。
        - docs/design/model/entities.md；docs/design/model/sources-registry.md；docs/design/governance/maintenance.md
        content_role: reference_explanation
        scope: 来源tier枚举的治理说明，de-jure/de-facto/vendor/archival不因出现而成为四个术语概念。
        link_base: docs/glossary.md
        original_cells:
        - 来源分级
        - de-jure / de-facto / vendor / archival
        - 引证来源按变更方式分档；依据为组织依据
        - Z 5.3.5.2；[命名实体设计](design/model/entities.md)
        basis_note: 本库字段说明，引用现行项目规则，不伪装外部四档术语定义。
      - id: glossary-L0138
        section: 词表间映射
        cells:
        - exactMatch / closeMatch
        - —
        - skos:exactMatch 表示概念可在广泛的信息检索应用中高可信地互换使用；skos:closeMatch 表示概念在某些信息检索应用中足够相近、可互换使用。exactMatch 具有传递性；closeMatch 不声明传递性，不据此作传递推断。
        - W3C SKOS Reference §10.4、§10.6
        content_role: reference_explanation
        scope: 跨concept scheme的映射属性；不将closeMatch当作ISO inexact equivalence的无条件同义表示，也不把未声明传递性误写成反传递。
        link_base: docs/glossary.md
        original_cells:
        - exactMatch / closeMatch
        - —
        - SKOS 的精确 / 不精确等价；前者传递，后者不传递
        - SKOS §10
        basis:
        - entity: skos
          locator: §10 Mapping Properties；exactMatch/closeMatch定义与S38–S46
          checked: '2026-09-06'
      - id: glossary-L0139
        section: 词表间映射
        cells:
        - broadMatch / narrowMatch / relatedMatch
        - —
        - skos:broadMatch 从源概念指向含义较宽的目标概念；skos:narrowMatch 指向含义较窄的目标概念；skos:relatedMatch 表示概念间的相关映射。它们是SKOS跨概念方案映射属性，不是本库新增关系类别。
        - W3C SKOS Reference §10
        content_role: reference_explanation
        scope: SKOS broadMatch/narrowMatch/relatedMatch为映射属性标识，按W3C映射语义引用，不造三个TC。
        link_base: docs/glossary.md
        original_cells:
        - broadMatch / narrowMatch / relatedMatch
        - —
        - SKOS 的层级 / 相关映射
        - SKOS §10
        basis:
        - entity: skos
          locator: §10 Mapping Properties；broadMatch/narrowMatch/relatedMatch定义及属性关系
          checked: '2026-09-06'
      symbol_mappings:
      - origin_id: glossary-L0053
        symbols:
        - USE
        - UF
        concept_ids:
        - tc-75e8012c-351f-4303-b8c0-523454b9b730
        role: relationship_indicator
        display_note: 关系指示符，参考所链接的关系概念；不作为英文术语形式。
      - origin_id: glossary-L0054
        symbols:
        - USE+
        - UF+
        concept_ids:
        - tc-ad90ba40-f5b0-44e7-9f59-fa2783d837b3
        role: relationship_indicator
        display_note: 关系指示符，参考所链接的关系概念；不作为英文术语形式。
      - origin_id: glossary-L0055
        symbols:
        - BT
        - NT
        concept_ids:
        - tc-278494cf-719c-43f9-b954-2a54c61e5c45
        role: relationship_indicator
        display_note: 关系指示符，参考所链接的关系概念；不作为英文术语形式。
      - origin_id: glossary-L0056
        symbols:
        - BTG
        - NTG
        concept_ids:
        - tc-54e74c2d-103e-4935-aab7-fb44a129af69
        role: relationship_indicator
        display_note: 关系指示符，参考所链接的关系概念；不作为英文术语形式。
      - origin_id: glossary-L0057
        symbols:
        - BTP
        - NTP
        concept_ids:
        - tc-818463b8-0d48-4ddf-98fb-228ef4591308
        role: relationship_indicator
        display_note: 关系指示符，参考所链接的关系概念；不作为英文术语形式。
      - origin_id: glossary-L0058
        symbols:
        - BTI
        - NTI
        concept_ids:
        - tc-9fde9fd8-eb29-4477-acc1-295f9de9adf5
        role: relationship_indicator
        display_note: 关系指示符，参考所链接的关系概念；不作为英文术语形式。
      - origin_id: glossary-L0059
        symbols:
        - RT
        concept_ids:
        - tc-589f6145-5330-4773-b2dd-27eeeaa6bc84
        role: relationship_indicator
        display_note: 关系指示符，参考所链接的关系概念；不作为英文术语形式。
      historical_designations:
      - origin_id: glossary-L0021
        forms:
        - 术语表
        - 代码表
        target_concept_ids:
        - tc-94e9bdfe-cefd-445c-9a12-f276bfe75e63
        reason: 原行实际概念为NISO§5.4.1 list；术语表容易指带定义的glossary，代码表指代码及取值清单，两者不能无条件作为一般list同义名。建议采用列表；不为代码表另建code-list概念。
        display: 原称术语表／代码表，现用列表；两旧称仅供历史检索与解释，不作为此概念的准用名称。
        approval: decision-term-data-values
        disposition: withdraw_from_current_designations_of_this_concept
        effect: 名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
      - origin_id: glossary-L0061
        forms:
        - paradigmatic
        target_concept_ids:
        - tc-df2d8160-1717-4372-a38f-db96925ac980
        reason: 原单独形容词省略relationship；采用已核ISO完整名称，旧省略写法不再作独立当前designation。
        display: 原英文paradigmatic，完整名称为paradigmatic relationship。
        approval: decision-term-data-values
        disposition: replace_elliptical_adjective_with_attested_full_term
        effect: 名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
      - origin_id: glossary-L0062
        forms:
        - syntagmatic
        target_concept_ids:
        - tc-1b0b91bc-d29e-44d4-854c-cddd05aebc13
        reason: 原单独形容词未完整表示关系名称，按作者用法补足relationship。
        display: 原英文syntagmatic，完整名称为syntagmatic relationship。
        approval: decision-term-data-values
        disposition: replace_elliptical_adjective_with_attested_full_term
        effect: 名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
      - origin_id: glossary-L0192
        forms:
        - 认知层级
        - cognitive level
        target_concept_ids:
        - tc-b49a8de0-d20e-42da-b7f0-f8d09ce44dc2
        reason: Krathwohl原名称是Cognitive Process dimension，旧名称将维度简化为单一深度。作为外部概念名称建议纠正；本库level字段可选和自评用途仍按现行模型，不由名称纠正更改。
        display: 旧称认知层级／cognitive level；来源概念名称为认知过程维度／cognitive process dimension。
        approval: decision-term-data-values
        disposition: replace_inaccurate_source_designations
        effect: 名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
      - origin_id: glossary-L0200
        forms:
        - 政策
        - policy
        target_concept_ids:
        - tc-24c3f7b9-c6a2-4e1c-91f2-b3ee234219c8
        reason: 采用实际原词头governance policy与治理政策；不无条件把一般policy作为同义。旧项目政策规则的约束效力按governance文档保持，术语改名不取消实际义务。
        display: 原政策／policy在本行治理语境明确为治理政策／governance policy。
        approval: decision-term-data-values
        disposition: replace_overgeneral_designations_in_governance_context
        effect: 名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
      - origin_id: glossary-L0202
        forms:
        - 监控与评价
        - monitoring and evaluation
        target_concept_ids:
        - tc-09ff3cd6-f825-4e90-b401-4ef25c2cc084
        - tc-f881797d-c9ff-4f57-9523-b6a1c01c8b2c
        reason: 原组合是两种活动，不是一个同义名称；采用OECD已核监测/评估，旧中文组合仅保留迁移前检索，不自动作为单概念准用词。
        display: 原组合监控与评价；分别见监测（monitoring）与评估（evaluation）。
        approval: decision-term-data-values
        disposition: split_combination_and_replace_chinese_by_verified_forms
        effect: 名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
      model_labels:
        generation_inputs:
        - data/vocab/topics.yaml
        - data/vocab/forms.yaml
        - data/inputs/topics/label-adoptions.json
        display_rule: 按中英形式合并展示但保留全部256对象身份；不新增TC/TM，标签继续按已有编辑源与语言采纳规则生成。
        language_notice: 模型知识 · 第5级，外部用法未核实
- question: Q03
  resolution: recommended
  patches:
  - identity: '@control:terms'
    field: conditional_execution_scope
    value:
      requested_scope: 供人选择的条件式授权：采纳具体值、schema/layout、单列人员规则及六项限定定义许可后，才实施并验收；通过后才写正式切换状态。当前组包不构成授权。
      publication_grant:
        decision_id: decision-term-complete-publication
        level: L3
        identity: '@control:terms'
        field: publication
        value:
          active_editor: data/vocab/terms.yaml
          state: active
          terms_mode: active_editor
          consumers_enabled: true
      state_fields_after_acceptance:
        path: data/vocab/term-cutover-state.yaml
        schema: urn:kb-design:data:term-cutover-state
        version: 1
        active_editor: data/vocab/terms.yaml
        state: active
        terms_mode: active_editor
        consumers_enabled: true
        decision: decision-term-complete-publication
      state_history_rule:
        date: 实际执行日，由执行时记录，不伪造为本次提案日期
        event: activate_term_publication
        decision: decision-term-complete-publication
        reason: 获准157个结构化术语及完整glossary/app参考消费通过全量内容与工程验收后切换
        from_value: null
        to_value: active
        linked_terms: []
      ordered_stages:
      - stage: 落实已采纳结构
        actions:
        - 先落实六条de-facto定义根的精确L3限定许可及默认拒绝/精确匹配保护；未获准不得进入全量迁移。
        - 实现仅3概念/定义及2英文形式的project basis分支和精确grant保护。
        - 实现layout v2展示输入，check-terms区分当前形式、历史纠正线索、符号及模型标签；不让layout变为术语定义源。
        - 将获准的公众人物规则纠正独立写入指定规则文，保留原对象不自动删改。
      - stage: 全量数据验收
        actions:
        - 按实际获准值建立157概念、全部术语、51来源及精确决定，保留全部原记录与身份去向。
        - 在隔离构建输入中投影拟议publication/state，不先改变现行编辑源；核对完整glossary的所有定义、3说明、6缩写、14文献、符号、历史纠正与231模型行。
        - 校验定义/语言/来源/完整grant、历史链、同环境生成确定性与引用闭包；失败继续修复，不通过删旧名、降证据或移入保留源取巧。
        - 按明确的concept/term绑定同步改正实际使用已退出designation的引用；仅普通叙述、来源转录、路径或字段标签同文不批量替换。认知level可选与政策权力规则不因名称纠正改变。
      - stage: 临时应用验收
        actions:
        - 以同一干净隔离Git快照，在build/term-complete-acceptance/vault/临时vault验收术语导出、manifest、链接与刷新保护；旧用户内容/配置保护也验证。
        - 临时快照可包含所提精确state用于测试消费者，但不构成正式编辑源切换；临时产物不写外部正式vault。
      - stage: 条件成立后的切换
        actions:
        - 只有前述验收通过且条件式授权已明确采纳，才写term-cutover-state.yaml的精确值与真实history。
        - 将data/vocab/terms.yaml设为结构化术语唯一编辑源，并生成完整docs/glossary.md；layout仅展示说明及已明确历史处置，topics/forms维持原所有权。
        - 启用glossary生成与kb-obsidian术语参考读取；消费者启用不等于外部正式vault同步、合并或发布。
      failure_rule: 验收不通过则不得切换；保留实际失败证据，按Git恢复需要恢复的已授权隔离改动，不用额外保留编辑源绕过。
      proposed_write_set:
      - schemas/terms-v1.schema.json及直接对应模型/校验/渲染实现
      - data/vocab/terms.yaml
      - data/vocab/entities.yaml
      - data/inputs/terminology/glossary-layout.yaml
      - docs/decisions/term-data-values.md
      - docs/decisions/source-term-complete-citations.md
      - docs/decisions/term-complete-publication.md
      - docs/decisions/person-admission-clarification.md
      - docs/design/model/entities.md及必要合同说明
      - docs/glossary.md
      - data/vocab/term-cutover-state.yaml（仅通过后）
      - build/term-complete-acceptance/临时快照、glossary及vault
      - docs/decisions/term-limited-definition-source-use.md及对应最小适用规则说明/严格引用门禁
      excluded:
      - ~/Documents/kb-vault/正式库写入
      - 合并到master
      - 发版
      - 新增正式义务、委托或持久正式索引
      - 未在本包列出的词汇/概念或其他项目功能
      time_estimate_after_explicit_approval: 预计2–3小时：项目basis和layout扩展、全量实际记录/决定落地、完整glossary与临时vault验收。来源与语义核对已形成材料，不重新全面研究。
      human_gate: 一次选择是否采纳157记录、51来源、名称处置、schema/layout扩展、人员规则、六条限定定义许可及条件式执行范围；均为明确值或规则，不预设批准。
      authorization: accepted_conditional_execution
      publication_activation: 验收通过后由主线单独确认并激活，不因本范围决定直接取得publication grant。
---

# 术语结构采纳

用户于 2026-09-06 采纳完整包的最小结构方案和条件式执行范围。概念、定义及现行形式的唯一数据所有者仍是 terms.yaml；layout 只承载布局、引用说明、符号与明确历史名称处置，不新增保留术语编辑源。

## 项目依据

project 分支仅用于 Q01 列明的三个既有概念与定义，以及 assertion、threshold 两个英文形式。origin 引用已有 Git 提交和实际模型或登记位置；中文模型依据独立。每条实际记录须在 term-data-values 中同时取得完整 record 与精确 project_basis_scope 授权，不开放任意外部缺证对象或英文模型回退。

## 展示输入

Q02 精确采纳实际 layout v2：157 概念按原章节编排；3 项说明、6 个出处缩写、14 项文献、关系指示符、历史名称和 231 模型行各按既定性质显示。真实 designation 不得靠 layout 中的普通说明继续取得未核使用资格；明确历史名称可检索，但不等于当前准用形式。

## 条件式执行

先落实获准结构和数据，完成原行、名称、身份、来源及完整生成对账，再以同一干净隔离快照验收临时 vault。全部通过后，publication 才由主线最终确认。正式 term-cutover-state 和 glossary 在该门槛前保持不写；外部正式 vault 写入、合并与发版排除。
