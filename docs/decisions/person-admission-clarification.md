---
id: decision-person-admission-clarification
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: '2026-09-06'
level: L3
scope: 公众人物法律判断与人员收录例子的区分，保留隐私门槛
supersedes: []
answers:
- question: Q01
  resolution: recommended
  patches:
  - identity: '@control:entities'
    field: person_admission
    value:
      target: docs/design/model/entities.md 人员收录段；docs/glossary.md L178 的项目规则部分
      text: person 只收在相关主题或活动中有显著公开角色、且符合公众人物判断依据的人。已发表作品的作者、公开项目的维护者和方法的提出者只作为可能的收录对象，不因该身份、Wikidata 条目或公开出处自动取得公众人物资格；须分别说明一般公众人物依据，或相关公共争议中的突出角色及适用范围，并提供可引用的公开出处。不收私人、同事或联系人。文献实体用
        creator 指向人，软件实体的个人维护者用 vendor 指向人。
      effect: 撤去例子自动充分的推导；保留公众人物门槛与私人、同事、联系人排除，不扩大隐私边界，不自动删改现有实体。
      existing_entities_unchanged: true
---

# 公众人物边界

用户于 2026-09-06 采纳完整包单列的人员规则纠正。Gertz 判决中发表专业作品并不足以取得公众人物地位，因此作者、维护者和方法提出者只能作为可能对象，不能自动满足法律判断条件。

## 收录规则

person 只收在相关主题或活动中有显著公开角色、且符合公众人物判断依据的人。已发表作品的作者、公开项目的维护者和方法的提出者只作为可能的收录对象，不因该身份、Wikidata 条目或公开出处自动取得公众人物资格；须分别说明一般公众人物依据，或相关公共争议中的突出角色及适用范围，并提供可引用的公开出处。不收私人、同事或联系人。文献实体用 creator 指向人，软件实体的个人维护者用 vendor 指向人。

## 适用边界

本决定保留原公众人物门槛，以及私人、同事和联系人排除；不因这次规则澄清自动删除、重新分类或修改已有实体。若今后希望以公开专业角色而非法律公众人物身份设定规则，仍须另作明确决定，不能由术语定义默默放宽。
