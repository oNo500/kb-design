---
id: decision-term-complete-publication
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: '2026-09-06'
level: L3
scope: 依用户已批准的条件式执行，在完整临时验收通过后切换术语编辑源与参考消费者
supersedes: []
answers:
- question: Q01
  resolution: recommended
  patches:
  - identity: '@control:terms'
    field: publication
    value:
      active_editor: data/vocab/terms.yaml
      state: active
      terms_mode: active_editor
      consumers_enabled: true
---

# 术语发布条件

状态：已生效。用户已明确采纳完整字段和条件式执行范围；临时验收条件现已满足，按该授权记录本次术语编辑源与参考消费者的切换。验收证据见[基础设施验收](../../work/reviews/2026-09-06-infrastructure-acceptance.md)。

## 精确状态

active_editor 指向 data/vocab/terms.yaml，state 为 active，terms_mode 为 active_editor，consumers_enabled 为 true。状态历史记录本次真实执行日及从 null 到 active；此前提案和记录登记仍保留各自历史，不改写为此前已经切换。

## 验收条件

获准 schema、layout、157 个术语概念及其 314 个名称、51 条来源和六项限定定义许可通过共享校验。原行与名称去向已对账；完整生成通过重复生成检查。隔离快照 5f694651fb2bd45aa2a712e8267ac3ca3ad24985 完成全量初始化与旧六词表库升级：新增 208 个参考文件，157 个术语页齐全，21 个保护文件字节不变，旧引用和新术语引用均有效。刷新后的 1055 个参考文件与全量新建结果一致。

上述结果满足先验收、后切换的条件。执行中发现的权限、日期读取、夹具隔离和反向索引问题均已修复并复核；没有通过删除旧条目、降低依据要求或另建保留编辑源绕过。

## 执行边界

本次启用的消费者范围是 glossary 生成与 app 术语参考读取。结构化术语以 terms.yaml 为唯一编辑源；layout 只负责展示配置，模型标签维持原有编辑权。外部正式 vault 写入、合并到 master、发版与新增正式义务、委托或持久正式索引不包含在内。
