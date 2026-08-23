# 方法登记

本库采用的每一种方法或范式，在这里登记来源和导出的规则。方法的第一原理写在对应的概念文里；没有概念文的方法标明。

准入规则：引入新方法先登记；提出新规则先看能否从已登记方法的原理推出，推不出就不加。理由见[第一原理与设计理由](../concepts/first-principles.md)。

## 登记表

| 方法 | 概念文 | 来源 | 导出的规则 |
|---|---|---|---|
| 受控词表 | [受控词表](../concepts/controlled-vocabulary.md) | Wüster, *Internationale Sprachnormung in der Technik*, 1931 博士论文；ISO 25964-1；ISO 704 | [topics.md](topics.md)：ID 与名字分离、等价关系、范围注释、生命周期 |
| 分面分析 | [分面](../concepts/facet.md) | Ranganathan（1933）；Z39.19 §5.3.4；ISO 25964-1 §11 | 分面字段草案；后组式标签；实体表的 kind / form / subjects |
| 划分特征与数组 | [词表的层级](../concepts/vocabulary-hierarchy.md) | ISO 25964-1 §2.1、§2.4、§2.38 | [hierarchy.md](hierarchy.md) 规则 9–12；`arrays` 字段 |
| 依据 warrant | [词表的建设与维护](../concepts/vocabulary-construction.md) | Hulme, *Principles of Book Classification*, Library Association Record 1911–12；Z39.19 §5.3.5 | [topics.md](topics.md)：从内容抽词、候选词、废除无引用的词；[maintenance.md](maintenance.md) 信号 |
| 借入层级求完整 | [词表的建设与维护](../concepts/vocabulary-construction.md)（自上而下、未标引词） | 本库 README；Z39.19 §11.1.3.1、§11.1.8 | [hierarchy.md](hierarchy.md) 规则 4、5；未标引状态 |
| 借入照抄与本地分析分层 | [词表的层级](../concepts/vocabulary-hierarchy.md)（数组可选、多数组归属）、[分面](../concepts/facet.md)（分析是重组）、[知识体系](../concepts/body-of-knowledge.md)（枚举、只借上层） | ISO 25964-1 数据模型；Z39.19 §8.3.5 | [decisions/borrow-and-analyze.md](decisions/borrow-and-analyze.md)；[hierarchy.md](hierarchy.md) 规则 6、9–12 |
| 知识体系作上层结构 | [知识体系](../concepts/body-of-knowledge.md) | SWEBOK / ISO/IEC TR 19759；CS2023；GB/T 13745；ISO 25964-2 §19 | [hierarchy.md](hierarchy.md)：第 2、3 层取自知识领域与知识单元 |
| 词表映射 | [词表映射](../concepts/vocabulary-mapping.md) | ISO 25964-2 §6–11；SKOS §10 | [sources-registry.md](sources-registry.md)：三种用法、`match`、默认 closeMatch |
| 名称规范表 | [词表映射](../concepts/vocabulary-mapping.md)（与各类词表互操作）、[受控词表](../concepts/controlled-vocabulary.md) | ISO 25964-2 §23 | [entities.md](entities.md) |
| 新主题的分类 | [新主题的分类](../concepts/classifying-new-subjects.md) | Ranganathan 好客准则（1957）；Hulme（1911）；Hjørland & Albrechtsen（1995）；Bowker & Star（1999、2007） | 实体表的 kind / form / subjects；本地概念 candidate + origin；[maintenance.md](maintenance.md) 剩余监控 |
| 元数据 | [元数据](../concepts/metadata.md) | Dublin Core：ISO 15836-1:2017、ISO 15836-2:2019；DCMI Metadata Terms 2020 | [content-model.md](content-model.md) |
| 第一原理与设计理由 | [第一原理与设计理由](../concepts/first-principles.md) | Aristotle；Kunz & Rittel IBIS（1970）；Nygard ADR（2011） | 本文；[decisions/](decisions/) 不删旧决定 |
| 写作规范 | [写作规范](../concepts/writing-conventions.md) | 原则：ISO 24495-1:2023；中文书面语：GB/T 15834、W3C clreq；技术写作：Google、Microsoft style guide；文档分类：Diátaxis | [writing.md](writing.md)；CLAUDE.md 为其摘要；目录划分 `concepts/` 解释、`design/` 参考；[content-model.md](content-model.md) 文档类型词表取 Diátaxis 四类 |
| 治理 | [治理](../concepts/governance.md) | ISO 37000:2021；DAMA-DMBOK 数据治理；ISO 15489-1 §6 | [governance.md](governance.md) 政策、决策权、变更控制、审计 |
| 来源分级与复核 | 无 | 分档依据为组织依据（Z39.19 §5.3.5.2）；复核周期为本库估值 | [entities.md](entities.md) `tier`；[maintenance.md](maintenance.md) 阈值表 |
| 处置决定 | [ISO 15489 笔记](../sources/iso-15489.md)（无概念文；标准不直接适用，只借其处置原则） | ISO 15489-1:2016 §3.8、§8.5 | [content-model.md](content-model.md) 处置决定；词表生命周期的“不删” |
| 断言的依据 | 无（治理规则） | Z39.19 §11.1.4；ISO 15489-1 §4 (c)；W3C PROV-O | [maintenance.md](maintenance.md) 断言一节；`check-topics.py` 判断债统计 |

## 未登记的做法

目前没有原理支撑、只是习惯的做法，要么补登记，要么删掉：

- 概念文的固定分节（定义 / 解决的问题 / 用法 / 来源）
