---
id: decision-source-0011
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: 2026-08-31
level: L2
scope: source-migration-policy
supersedes: []
answers:
  - question: Q04
    resolution: recommended
    patches:
      - {identity: "@control:identity-boundaries", field: identity_policy, value: {independent_publisher_identity: new-entity, status_page: watch, sample: locator, mirror: mirror-address, archive: archive-address, corrigendum: evidence}}
  - question: Q05
    resolution: recommended
    patches:
      - {identity: "@control:focus-identities", field: focus_policy, value: {rfc-http: retire-alias, iso-25964: two-parts, dita: one-entity-three-addresses, lom-2002: freeze, lom-2020: new-after-evidence, z39-19: one-address-chain, bcp47-rfcs: separate-entities}}
  - question: Q12
    resolution: recommended
    patches:
      - {identity: "@control:candidate-roles", field: candidate_role_policy, value: {candidate: proposed-discovery, unused-mapping: proposed, empty-group: proposed}}
  - question: Q14
    resolution: recommended
    patches:
      - {identity: "@control:multi-source", field: multi_source_policy, value: {primary_derivation: cs2023, additional_sources: array-and-match}}
  - question: Q15
    resolution: recommended
    patches:
      - {identity: "@control:external-groups", field: external_group_policy, value: {retain: true, fields: [registry, item, locator, basis], proves_member_derivation: false}}
  - question: Q16
    resolution: recommended
    patches:
      - {identity: "@control:local-analysis", field: local_analysis_policy, value: {form_arrays: isolated-local-analysis, source_reference: false, members_unchanged: true}}
  - question: Q17
    resolution: recommended
    patches:
      - {identity: "@control:rfc-source", field: rfc_policy, value: {registry: rfc-1122, layers: [link, internet, transport, application], require_per_layer_basis: true}}
  - question: Q20
    resolution: recommended
    patches:
      - {identity: "@control:unsupported-basis", field: unsupported_basis_policy, value: {none: no_external_basis, self: project_assertion, formal_basis: false, preserve_old_hash: true}}
  - question: Q23
    resolution: recommended
    patches:
      - {identity: "@control:tier", field: tier_policy, value: {changes: none, preserve_during_compatibility: true}}
  - question: Q24
    resolution: recommended
    patches:
      - {identity: "@control:term-admission", field: term_admissions, value: []}
  - question: Q25
    resolution: recommended
    patches:
      - {identity: "@control:cutover", field: cutover_sequence, value: [schema, validator, index, probe, candidate, payload, handoff, decisions, apply]}
      - {identity: "@control:cutover", field: rollback_sequence, value: {method: compensation, preserve: [decisions, ids, history, obligations, ledgers, handoff, payload]}}
      - {identity: "@control:cutover", field: release_sequence, value: separate-decision-source-0007}
---
# 来源迁移

## 背景

迁移预演必须消费 Q01 至 Q25 的规则覆盖，但规则覆盖不能被解释成 3,187 行真实数据已经获准。

## 决定

采用 front matter 中的类别、隔离和切换控制 patch。控制 patch 只定义迁移器允许表达的分类与顺序；真实实体身份、地址、状态、角色、依据、派生和映射仍须逐行决定。

## 后果

- 迁移器可以验证 25 项规则覆盖、字段所有权、identity 域和候选隔离。
- 规则控制行不计入 3,187 个库存身份，也不能关闭任何真实行的 `blocks_cutover`。
- 来源改档、术语准入和发版继续保持无变化或独立决定。
