---
id: decision-term-limited-definition-source-use
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: '2026-09-06'
level: L3
scope: 仅六个列明概念的精确de-facto定义来源许可，不改变来源tier或其他用途
supersedes: []
answers:
- question: Q01
  resolution: recommended
  patches:
  - identity: tc-e340f2b4-4515-4203-b5d1-8bafee5af81a
    field: definition_source_permission
    value:
      source_entity: swebok
      registered_tier: de-facto
      registered_version: '4.0'
      read_material: SWEBOK官网Focus on Generally Accepted Knowledge，知识总和与Guide范围说明
      checked: '2026-09-06'
      concept_basis:
      - entity: swebok
        locator: 官方页面Focus on Generally Accepted Knowledge；实际urllib读取
        checked: '2026-09-06'
      definitions:
      - language: zh-Hans
        text: 一个学科或职业领域内的知识总和。
        basis:
        - entity: swebok
          locator: 官方页面Focus on Generally Accepted Knowledge；实际urllib读取
          checked: '2026-09-06'
  - identity: tc-fbe9f215-a5f4-4292-92fa-b734f6c4b3ee
    field: definition_source_permission
    value:
      source_entity: swebok
      registered_tier: de-facto
      registered_version: '4.0'
      read_material: SWEBOK官网FAQ How do you define generally accepted knowledge?
      checked: '2026-09-06'
      concept_basis:
      - entity: swebok
        locator: 官方FAQ How do you define generally accepted knowledge?；实际urllib读取
        checked: '2026-09-06'
      definitions:
      - language: zh-Hans
        text: 在大多数项目的大多数情况下适用，且其价值和作用获得广泛共识的知识。
        basis:
        - entity: swebok
          locator: 官方FAQ How do you define generally accepted knowledge?；实际urllib读取
          checked: '2026-09-06'
  - identity: tc-3945b496-c4ac-4553-81ad-4c6dab62d81c
    field: definition_source_permission
    value:
      source_entity: cs2023
      registered_tier: de-facto
      registered_version: 2024-01
      read_material: CS2023 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
      checked: '2026-09-06'
      concept_basis:
      - entity: cs2023
        locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
        checked: '2026-09-06'
      definitions:
      - language: zh-Hans
        text: CS2023知识模型中一组相互关联的知识单元。
        basis:
        - entity: cs2023
          locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
          checked: '2026-09-06'
  - identity: tc-89c27e71-9c5a-4e5e-a588-15c0ae59345d
    field: definition_source_permission
    value:
      source_entity: cs2023
      registered_tier: de-facto
      registered_version: 2024-01
      read_material: CS2023 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
      checked: '2026-09-06'
      concept_basis:
      - entity: cs2023
        locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
        checked: '2026-09-06'
      definitions:
      - language: zh-Hans
        text: CS2023知识模型中一组相关主题以及这些主题的学习成果。
        basis:
        - entity: cs2023
          locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
          checked: '2026-09-06'
  - identity: tc-c5f9771f-7271-4128-854d-88b12df9f7ed
    field: definition_source_permission
    value:
      source_entity: cs2023
      registered_tier: de-facto
      registered_version: 2024-01
      read_material: CS2023 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
      checked: '2026-09-06'
      concept_basis:
      - entity: cs2023
        locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
        checked: '2026-09-06'
      definitions:
      - language: zh-Hans
        text: CS2023知识单元内的知识主题，按课程模型标为核心或选修。
        basis:
        - entity: cs2023
          locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
          checked: '2026-09-06'
  - identity: tc-9e701a8f-b994-4a0d-8eab-3ea769ae1b6c
    field: definition_source_permission
    value:
      source_entity: iptc-genre
      registered_tier: de-facto
      registered_version: null
      read_material: IPTC NewsCodes Guidelines §1.1，Genre整体说明
      checked: '2026-09-06'
      concept_basis:
      - entity: iptc-genre
        locator: NewsCodes Guidelines §1.1 Descriptive NewsCodes，Genre整体说明
        checked: '2026-09-06'
      definitions:
      - language: zh-Hans
        text: 按内容性质及其新闻或知识表达特征区分的文本类别。
        basis:
        - entity: iptc-genre
          locator: NewsCodes Guidelines §1.1 Descriptive NewsCodes，Genre整体说明
          checked: '2026-09-06'
---

# 限定定义许可

用户于 2026-09-06 明确采纳完整包中的六条限定定义许可。本决定是维护规则中 de-facto 定义禁令的有限例外，仅覆盖 frontmatter 逐 TC 列明的概念 basis、定义文本、来源、定位和核对日期，不是按来源名称泛放行。

## 许可对象

知识体系与普遍接受的知识使用 swebok 登记版本 4.0；知识领域、知识单元、主题使用 cs2023 登记版本 2024-01；体裁使用未登记版本的 iptc-genre。登记版本与实际网页 revision 不同，空版本不补造。具体材料与已核范围以各 patch 为准。

## 许可条件

有效 L3 决定中的 definition_source_permission 必须精确匹配相同 concept_id 及全部值，并同时存在当前完整 record grant。其他概念、同来源其他定义、旧定义或只存在决定文件，均不取得许可。改变列明值须重新按具体值权限处理。

三个来源的 tier、version、status 以及结构、映射和其他来源用途保持不变；vendor 与其他 de-facto 定义根仍受现行规则限制。本许可不自动创建正式义务、委托、消费者或发布状态。
