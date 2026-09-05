---
id: decision-source-fields-p1-p4
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: '2026-09-06'
level: L2
scope: source-fields-p1-p4
supersedes: []
answers:
- question: Q05
  resolution: recommended
  patches:
  - identity: entities/iso-25964-1
    field: version
    value: '2011'
  - identity: entities/iso-25964-1
    field: source_status
    value: current
  - identity: entities/iso-25964-1
    field: basis.version
    value:
    - entity: iso-25964-1
      locator: https://www.iso.org/standard/53657.html；ISO 25964-1:2011，第 1 版，2011-08
      checked: '2026-08-29'
  - identity: entities/iso-25964-1
    field: basis.source_status
    value:
    - entity: iso-25964-1
      locator: https://www.iso.org/standard/53657.html；现行版本与 2022 年复审确认信息
      checked: '2026-08-29'
  - identity: entities/iso-25964-2
    field: version
    value: '2013'
  - identity: entities/iso-25964-2
    field: source_status
    value: current
  - identity: entities/iso-25964-2
    field: basis.version
    value:
    - entity: iso-25964-2
      locator: https://www.iso.org/standard/53658.html；ISO 25964-2:2013，第 1 版，2013-03
      checked: '2026-08-29'
  - identity: entities/iso-25964-2
    field: basis.source_status
    value:
    - entity: iso-25964-2
      locator: https://www.iso.org/standard/53658.html；现行版本与 2023 年复审确认信息
      checked: '2026-08-29'
  - identity: entities/z39-19
    field: version
    value: 2005 (R2010)
  - identity: entities/z39-19
    field: urls
    value:
    - role: landing
      url: https://www.niso.org/publications/ansiniso-z3919-2005-r2010
      primary: true
    - role: doi
      url: https://doi.org/10.3789/ansi.niso.z39.19-2005R2010
      primary: false
  - identity: entities/z39-19
    field: basis.version
    value:
    - entity: z39-19
      locator: https://www.niso.org/publications/ansiniso-z3919-2005-r2010；出版标题；项目出版页的
        2005 edition / 2010 reaffirmation version of record 说明
      checked: '2026-08-29'
  - identity: entities/z39-19
    field: basis.urls
    value:
    - entity: z39-19
      locator: https://www.niso.org/publications/ansiniso-z3919-2005-r2010；出版页地址及
        DOI 栏
      checked: '2026-08-29'
  - identity: entities/skos
    field: version
    value: '2009-08-18'
  - identity: entities/skos
    field: basis.version
    value:
    - entity: skos
      locator: https://www.w3.org/TR/skos-reference/；文档状态及 W3C Recommendation 日期
      checked: '2026-08-29'
---
# 来源字段值

本记录结构化承接用户已采纳的 P1–P4，依据见[原采纳记录](source-field-adoptions.md)与[字段合同](source-v2-field-contract.md)。记录日期为 2026-09-06，原外部阅读日期仍为 2026-08-29；不是本轮全面复核或新的外部事实采纳。

## 作用范围

patch 的 identity、field、value 必须精确一致。它只批准所列实体的所列字段及依据，不批准 source_use 的角色，不批准全部映射、不更改项目状态或主题归属，不补齐缺失的 review、watch、history、source_status 或替代关系。
