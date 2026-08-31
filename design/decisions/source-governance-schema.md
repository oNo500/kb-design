---
id: decision-source-0001
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: 2026-08-31
level: L2
scope: source-governance-schema
supersedes: []
answers:
  - question: Q01
    resolution: recommended
    patches:
      - identity: "@control:paths"
        field: paths
        value:
          entities: vocab/entities.yaml
          uses: vocab/sources.yaml
          decisions: design/decisions/source-*.md
          obligations: vocab/source-obligations.yaml
          reference_index: vocab/generated/source-reference-index.json
          probes: .superpowers/sdd/2026-08-31-source-schema-migration/probes/
  - question: Q02
    resolution: recommended
    patches:
      - identity: "@control:schema"
        field: schema_versions
        value:
          entities: 2
          source_uses: 2
          source_obligations: 1
          source_reference_index: 1
          source_probe: 1
          source_migration: 1
          decision: 1
      - identity: "@control:schema"
        field: compatibility
        value:
          order:
            - schema-and-dual-read-validator
            - approved-candidate
            - atomic-strict-cutover
          reject_after_cutover:
            - compact-basis
            - legacy-source
            - legacy-match-source
            - legacy-origin
            - role-string-arrays
          release_version_unchanged: "2026.08"
  - question: Q03
    resolution: recommended
    patches:
      - identity: "@control:ids"
        field: id_policy
        value:
          existing_ids: frozen
          entity_pattern: "^[a-z0-9]+(?:-[a-z0-9]+)*$"
          use_id: same-as-one-to-one-entity
          decision_pattern: decision-source-NNNN
          obligation_pattern: source-review-YYYYMMDD-NNN
          collision: fail
          reuse: forbidden
  - question: Q06
    resolution: recommended
    patches:
      - identity: "@control:addresses"
        field: url_policy
        value:
          roles:
            - canonical
            - landing
            - doi
            - full_text
            - status
            - mirror
            - archive
          identity_priority:
            - canonical
            - doi
            - landing
            - full_text
            - status
            - archive
            - mirror
          probe_priority:
            - status
            - canonical
            - landing
            - full_text
          primary_count: 1
  - question: Q07
    resolution: recommended
    patches:
      - identity: "@control:review"
        field: review_policy
        value:
          intervals_months:
            de-jure: 24
            de-facto: 12
            vendor: 6
          archival_content_due: null
          archival_address_probe_months: 12
          grace_days: 30
          checked_source: human-confirmed-only
          tier_changes: none
  - question: Q21
    resolution: recommended
    patches:
      - identity: "@control:origin"
        field: origin_policy
        value:
          formal_origin_field: forbidden
          observations: .superpowers/sdd/2026-08-31-source-schema-migration/discovery/observations.tsv
          content_identity_separate_from_source_entity: true
          retention_rule: design/content-model.md
  - question: Q22
    resolution: recommended
    patches:
      - identity: "@control:obligation-bridge"
        field: source_term_bridge
        value:
          kind: source_obligation
          field: id
          copy_trigger: false
          copy_targets: false
          copy_state: false
          copy_conclusion: false
---
# 来源模式

## 背景

来源治理实施需要先固定正式路径、模式版本、标识规则、地址结构、复核结构、旧字段分流和来源义务到术语义务的衔接。人的决定已批准治理决定包当前推荐；真实来源状态、具体地址、人工核对日期和逐值来源关系仍由后续迁移决定处理。

## 决定

采用 front matter 中 Q01、Q02、Q03、Q06、Q07、Q21、Q22 的控制 patch。控制 patch 只批准结构和迁移规则，不为任何来源实体填写地址、外部状态、核对日期、依据、派生或映射结论。

## 后果

- 模式契约任务可以建立七份 schema 和共享来源模型。
- 现行 31 个来源 ID 保持冻结，新增身份仍须逐项决定。
- 真实实体的 `urls`、`review`、外部 `status` 和 `replaced_by` 继续在迁移账本中阻断，不能从本决定推导。
- 旧 `origin` 不成为正式字段；来源义务传给术语义务时只传稳定 ID。
