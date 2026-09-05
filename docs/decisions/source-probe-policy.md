---
id: decision-source-0010
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: 2026-08-31
level: L2
scope: source-probe-policy
supersedes: []
answers:
  - question: Q08
    resolution: recommended
    patches:
      - identity: "@control:watch"
        field: watch_policy
        value:
          availability_months: 1
          redirect_months: 1
          content_months:
            de-jure: 1
            de-facto: 3
            vendor: 6
            archival: 12
          signals: [availability, redirect, version, revision, replacement, withdrawal]
          content_priority: [publisher-version-metadata, normalized-locator-fragment, whole-page-low-confidence]
          false_positive_append_only: true
          formal_write: forbidden
---
# 来源探测

## 背景

只读探测器需要统一的信号、频率和误报记录规则，但不能据此修改来源实体、依据、角色或关系。

## 决定

采用 Q08 推荐的探测政策：地址可用性和重定向按月观察，内容信号按来源类型分频率；内容优先使用发布方版本元数据，其次使用获准定位片段，整页摘要只作低置信线索。误报只追加到 ignored 观察流。

## 后果

- 探测器可以使用固定 transport 夹具实现和验证六类信号。
- 观察只创建复核范围，不写回正式状态、核对日期、依据、角色、派生或映射。
- 每个真实实体的 `watch` 值仍由后续迁移决定形成，本决定不批量填值。
