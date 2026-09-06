---
id: decision-term-complete-publication
schema: urn:kb-design:data:decision
schema_version: 1
status: proposed
date: '2026-09-06'
level: L3
scope: 条件验收通过后的术语编辑源与消费者切换，尚未激活
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

状态：拟议，尚未激活。用户已采纳条件式执行范围，但本文件中的 publication 值只在统一验收通过并由主线最终确认后生效。当前尚未创建正式 term-cutover-state，也未覆盖现行 glossary。

## 精确状态

拟议值为 active_editor 指向 data/vocab/terms.yaml、state 为 active、terms_mode 为 active_editor、consumers_enabled 为 true。届时 state 历史记录真实执行日、从 null 到 active，不把本次提案或记录登记日期伪装成切换已发生。

## 验收条件

获准 schema 与 layout、157 个完整术语记录、51 来源、六项限定定义许可、原行与名称去向、完整 glossary 生成及临时 vault 导出刷新全部通过后，主线方可把本决定改为 accepted 并写入相应正式状态。任何失败先修复，不以删旧名、降证据或另建保留源绕过。

## 执行边界

本次拟议消费者范围包括 glossary 生成与 app 术语参考读取。外部正式 vault 写入、合并到 master、发版与新增正式义务、委托或持久正式索引不包含在内。
