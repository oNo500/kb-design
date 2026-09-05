---
id: decision-source-v2-fields
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: '2026-09-06'
level: L2
scope: source-v2-field-contract
supersedes: []
answers:
- question: Q02
  resolution: replacement
  patches:
  - identity: '@control:schema'
    field: compatibility
    value:
      formal_format: v2-only
      project_status: status
      external_status: source_status
      project_assertions: assertions
      subject_basis: values-and-references
      watch: locator-signals-cadence_months
      recovery: git-revert
      merge_before_complete: false
---
# 来源字段合同

状态：已采纳。用户明确回复“采纳整套方案，继续整批实施”。本记录把[完整方案](../../work/plans/2026-09-05-source-v2-field-contract.md)作为本次模型合同；实际来源事实、具体关系及用途角色仍需各自采纳，不由本模型决定代替。

## 字段语义

保留 status 的项目含义，外部状态使用 source_status。全部一般实体字段保留；self 项目判断使用 assertions，外部 basis 仍只放可核依据。subjects 的依据按 values 与 references 逐值关联。watch 复用 locator、signals 与 cadence_months，不新建观察结构或回滚框架。

## 采纳衔接

P1、P2 原提案的外部 status 对应 source_status，basis.status 对应 basis.source_status；事实值与原 checked 不变，原项目 active 恢复并保留。该字段名转换不改写历史提案。其余 P1–P4 字段按[既有采纳](source-field-adoptions.md)保留，机器作用域由[字段采纳记录](source-field-values.md)明确承接。

## 执行边界

本合同取代未激活来源 schema 将项目状态与外部状态放在同名 status 的安排，保留来源校验政策的事实、角色、映射权限分离。正式切换只接受新格式，不建立旧格式兼容；冻结旧材料仍作为审计保存。全部数据与消费者验证完成前不得合并 master；不撤销已有提交，不操作正式 vault。
