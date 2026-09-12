---
id: decision-term-evidence-scope
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: '2026-09-06'
level: L3
scope: 既有术语的语言依据表达及冻结登记范围内的必要取证
supersedes: []
answers:
  - question: Q01
    resolution: recommended
    patches:
      - identity: '@control:terms'
        field: model_language_basis
        value:
          level: 5
          existing_concepts_only: true
          languages: [zh-Hans, zh-Hant]
          separate_from_external_references: true
          preserves_qualified_external_basis: true
---

# 术语依据范围

用户于 2026-09-06 明确“采纳补充，整批继续”，采纳[术语依据补充](../../work/reviews/2026-09-06-term-evidence-supplement.md)。本决定扩展必要取证及机器表达能力，不批准尚未给出的具体词条值或正式发布状态。

## 语言依据

将现行[模型知识译名](model-knowledge-translation.md)第 5 级接入术语形式：仅处理已有、含义明确的概念的中文名称，保留实际模型、日期、判断理由及精确采纳引用，并明确外部中文用法未核实。现有合格前级依据不能被自动替换。

外部引用保持严格原格式；模型依据不得与外部引用混成同一种已核证据。该例外只解决中文形式的语言依据，不替代概念、定义、领域或外部关系依据，也不授权新增概念、类别、划分特征或任意名称。

既有名称默认保留；实质冲突、不能确认的形式与拟议改名集中进入具体采纳包。保存模型判断、通过 schema 或存在本范围决定，都不授予词条可用状态。

## 资料范围

允许对[冻结的现行登记](../../work/reviews/2026-09-06-term-inventory.json)已经引用的必要来源，以及现行译名阶梯内这些既有名称所需的术语资料进行只读原文核对。优先复用已有材料和有效核对记录，不因文件缺少本轮副本就否认此前阅读。

不新增持久下载、不做 OCR、不绕过登录或付费限制、不扩展新知识主题或建设资料平台。高价值且影响迁移的缺口优先；材料不可取得时保留准确限制，不以模型回答代替原文。

## 采纳边界

此前[术语实施范围](term-infrastructure-scope.md)继续有效。具体名称、定义、来源实体、状态及编辑权切换仍以准确差异的数据采纳包为准；本决定不授权任何 `record` 或 `publication` 值。

整批工程和资料工作继续在隔离分支完成。统一验收前不写正式 vault，整体未完成前不合并 master；版本管理继续使用 Git，不新增兼容或补偿体系。
