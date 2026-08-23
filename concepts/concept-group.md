# 概念组 (Concept Group)

## 定义

概念组是**按用途圈出的一批概念**。它不问「这是什么」,只问「谁要用」。ISO 25964-1 数据模型里是 ConceptGroup 类;从大词表里圈出一个子领域给某个系统或团队用,叫微词表(micro-thesaurus),是最常见的用法。

## 和分类的区别

「急诊科常用词」= {医生, 手术, 病房, 术前}。四个概念来自四个分面,树里相距很远,凑在一起只因为急诊科要用。圈了这个组,四个概念在树里的位置一个都不变。

| | 层级和分面 | 概念组 |
|---|---|---|
| 问的问题 | 它是什么 | 谁要用 |
| 一个概念属于几个 | 层级里一个位置(多层级可多个),分面一个 | 任意多 |
| 稳定性 | 领域不变就不变 | 随组织、项目变 |
| 改变树吗 | 是 | 否,只是视图 |

组可以嵌套(ISO 数据模型 hasSubgroup / hasSupergroup)。

## 在知识库中

某个项目或某个角色看到的标签子集,就是概念组。单人单项目时不需要;有多个项目或多人用同一份词表时再建。

## 权威来源

- [ISO 25964-1:2011](https://www.iso.org/standard/53657.html) §15 数据模型 ConceptGroup、ConceptGroupLabel
- NISO [ISO 25964 ↔ SKOS 对应表](https://www.niso.org/schemas/iso25964):ConceptGroup 映射为 `iso-thes:ConceptGroup`,`skos:Collection` 的子类;微词表用 `iso-thes:microThesaurusOf`
