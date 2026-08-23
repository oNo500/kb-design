# 概念组 (Concept Group)

## 定义

概念组是**按用途圈出的一批概念**。它不问“这是什么”，只问“谁要用”。ISO 25964-1 数据模型里是 ConceptGroup 类，可嵌套（hasSubgroup / hasSupergroup）。从大词表里圈出一个子领域给某个系统或团队用，叫**微词表**(micro-thesaurus)，是最常见的用法。

组的成员从哪来，有两种：

| 来源 | 例 | 维护 |
|---|---|---|
| 手工圈定 | “急诊科常用词”= {医生， 手术， 病房， 术前} | 人工 |
| 由[映射](vocabulary-mapping.md)派生 | “OWASP Top 10”= 所有映射到 owasp-top10 的本地概念 | 自动，从映射算出 |

第二种不需要单独登记成员，只要标明“这个外部词表派生一个组”。它让被挡在树外的外部词表（同一划分特征已有数组）仍然可以作为视图浏览。

## 和分类的区别

“急诊科常用词”= {医生， 手术， 病房， 术前}。四个概念来自四个分面，树里相距很远，凑在一起只因为急诊科要用。圈了这个组，四个概念在树里的位置一个都不变。

| | 分面 | 数组 | 概念组 |
|---|---|---|---|
| 归堆理由 | 概念本身是什么类 | 按某个划分特征 | 谁用、用在哪 |
| 一个概念属于几个 | 一个 | 每个划分特征一个 | 任意多 |
| 稳定性 | 领域不变就不变 | 随分析深入增加 | 随组织、项目变 |
| 改变树吗 | 决定有几棵树 | 决定树里怎么分叉 | 否，只是视图 |
| ISO 数据模型 | — | `ThesaurusArray` + `NodeLabel` | `ConceptGroup` |
| [SKOS](../sources/iso-25964.md) 对应 | — | `iso-thes:ThesaurusArray`(`skos:Collection` 子类） | `iso-thes:ConceptGroup`(`skos:Collection` 子类）；微词表加 `iso-thes:microThesaurusOf` |

## 在知识库中

某个项目或某个角色看到的标签子集，就是概念组。单人单项目时不需要；有多个项目或多人用同一份词表时再建。

## 权威来源

- [ISO 25964-1:2011](https://www.iso.org/standard/53657.html) §15 数据模型 ConceptGroup、ConceptGroupLabel、`conceptGroupType`
- NISO [ISO 25964 ↔ SKOS 对应表](https://www.niso.org/schemas/iso25964)
