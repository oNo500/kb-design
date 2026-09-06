---
id: decision-term-infrastructure-scope
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: '2026-09-06'
level: L3
scope: 术语基础实施范围、结构与必要取证；不批准具体术语值或正式切换
supersedes: []
answers:
  - question: Q01
    resolution: recommended
    patches:
      - identity: '@control:terms'
        field: implementation
        value:
          empty_subject_fields: true
          layout_members: concept_ids
          reference_path: kb/terms/<tc-id>.md
          model_labels_create_concepts: false
          preserve_existing_registrations: true
          preserve_pending_legacy_entries: true
---

# 术语实施范围

用户于 2026-09-06 采纳[集中提案](../../work/reviews/2026-09-06-term-adoption-proposal.md)中的字段、旧项保留和应用读取方案，并授权 NISO、IPLF、ISO 相关公开条目及 Ahrens 必要原文的只读核对。本决定只记录这些已发生的采纳，不批准尚未形成的具体字段值。

## 结构与归属

继续采用概念、语言、术语三层结构及既有稳定身份格式。领域归属未定时允许 `subject_fields` 为空；章节按概念 ID 明确编排，不把章节名称当主题 ID。语言按实际形式与依据确定，第一列纯英文不生成中文副本；关系指示符和来源枚举不自动成为独立术语概念。

旧登记保持既有效力，未核材料不进入已核外部依据。旧账本明确的 6 条待 L3 记录保留，不删除、不自动转为模型译名。原登记与迁移前状态按冻结输入和 Git 保留，不补造历史批准或候选日期。

模型译名继续属于现行主题、载体词表及语言采纳输入；生成区按中英形式合并展示但保留全部对象身份。不得据此建立术语委托、重新分配概念身份、修改原范围快照或提升外部依据等级。

## 应用读取

获准术语概念的 Obsidian 只读页使用 `kb/terms/<tc-id>.md`，所有者为 `data/vocab/terms.yaml`。形式身份与概念身份分开；术语页不自动成为主题或内容分类。

模型、正式输入、采纳决定与实现从同一干净 Git 快照读取，核心校验由术语表和应用共用。刷新仍只涉及 `kb/` 和 `app/manifest.json`，用户内容与配置不纳入写集。

## 取证范围

允许对本批定义、形式及对应关系的必要原文进行只读联网核对；优先 NISO 官方正文、IPLF 官方说明、ISO 公开条目或既有样本入口，以及作者公开讲述。辅助资料与标准正文、作者原文与他人转述必须区分。

不新增持久下载、不使用 OCR、不绕过付费或登录限制、不扩展为资料平台。取证结果用于具体值提案，不因原文可读自动取得术语准入或来源改档许可。

## 生效边界

本决定使已列结构和实施范围生效，不使术语草案整体生效，不创建正式术语实例、义务、委托或消费者状态。完整字段采纳、正式数据迁移、唯一编辑源切换和实际消费者启用仍以相应具体结果与决定为准。

工程继续在隔离分支整批推进，完成前不合并到 master；统一验收之前不写正式 vault。Git 承担版本恢复，不新增旧格式兼容、交付包、handoff 或专用补偿回滚。
