---
id: decision-source-0009
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: 2026-08-31
level: L2
scope: source-validation-policy
supersedes: []
answers:
  - question: Q09
    resolution: recommended
    patches:
      - identity: "@control:unavailability"
        field: release_block_policy
        value:
          minimum_distinct_failures: 3
          minimum_span_days: 14
          require_human_unreproducible: true
          evidence_priority: [publisher-status, doi-or-landing, archive, mirror]
          single_failure_changes_status: false
  - question: Q10
    resolution: recommended
    patches:
      - identity: "@control:external-status"
        field: status_policy
        value:
          values: [current, superseded, withdrawn]
          publisher_evidence_required: true
          temporary_unavailability_is_status: false
          unresolved_blocks_formal_cutover: true
          replacement_requires_evidence: true
  - question: Q11
    resolution: recommended
    patches:
      - identity: "@control:roles"
        field: role_policy
        value:
          inherited_default: proposed
          proposed_decision: null
          approved_requires_decision: true
          retired_requires_decision: true
          consumers_do_not_approve_role: true
  - question: Q13
    resolution: recommended
    patches:
      - identity: "@control:source"
        field: source_policy
        value:
          required_fields: [registry, item, locator, basis]
          required_role: structure
          role_status: approved
          rendered_locator_saved_per_row: true
          template_allowed: true
  - question: Q18
    resolution: recommended
    patches:
      - identity: "@control:match"
        field: match_policy
        value:
          relations: [exactMatch, closeMatch, broadMatch, narrowMatch, relatedMatch]
          required_role: mapping
          role_status: approved
          adjacent_basis_required: true
          old_relation_is_not_approval: true
  - question: Q19
    resolution: recommended
    patches:
      - identity: "@control:basis"
        field: basis_policy
        value:
          required_fields: [entity, locator]
          mutable_content_requires_checked: true
          fixed_version_and_hash_may_omit_checked: true
          repeat_per_value: true
          yaml_anchor_default_forbidden: true
          missing_locator_disposition: not_migrated_missing_locator
---
# 来源校验

## 背景

离线校验器需要先取得外部状态、角色、依据、实际派生和概念映射的结构规则，但不能在实现规则时伪造真实来源结论。本决定只固定校验政策，真实实体和逐值关系仍由后续迁移决定处理。

## 决定

采用 front matter 中 Q09、Q10、Q11、Q13、Q18、Q19 的控制 patch。控制 patch 只回答“什么结构和证据才能通过”，不回答任何具体来源当前是什么状态、哪个角色获准、哪条派生或映射成立。

## 后果

- 离线校验器可以实现稳定错误码、状态边界、角色资格、逐值依据和关系完整性检查。
- 31 个来源外部状态继续 unresolved，不从本决定生成 `current`、`superseded` 或 `withdrawn`。
- 47 个角色默认只保持 `proposed`；正式 `source` 和 `match` 仍须引用逐项获准的角色和关系。
- 缺 locator、缺 checked、旧 `source` 或旧 `match` 只形成阻断或审计，不自动升级。
