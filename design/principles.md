# 方法登记

本库采用的每一种方法或范式，在这里登记来源和导出的规则。方法的第一原理写在对应的概念文里；没有概念文的方法标「待写」。

准入规则：引入新方法先登记；提出新规则先看能否从已登记方法的原理推出，推不出就不加。理由见 [第一原理与设计理由](../concepts/first-principles.md)。

## 登记表

| 方法 | 概念文 | 来源 | 导出的规则 |
|---|---|---|---|
| 受控词表 | [受控词表](../concepts/controlled-vocabulary.md) | Wüster, *Internationale Sprachnormung in der Technik*, 1931 博士论文；ISO 25964-1；ISO 704 | [topics.md](topics.md)：ID 与名字分离、等价关系、范围注释、生命周期 |
| 分面分析 | [分面](../concepts/facet.md) | Ranganathan（1933）；Z39.19 §5.3.4；ISO 25964-1 §11 | [topics.md](topics.md)：`kind` 与树正交、后组式标签 |
| 依据 warrant | [词表的建设与维护](../concepts/vocabulary-construction.md) | Hulme, *Principles of Book Classification*, Library Association Record 1911–12；Z39.19 §5.3.5 | [topics.md](topics.md)：从内容抽词、候选词、废除无引用的词 |
| 借入层级求完整 | [词表的建设与维护](../concepts/vocabulary-construction.md)（自上而下、未标引词） | 本库 README；Z39.19 §11.1.3.1、§11.1.8 | [hierarchy.md](hierarchy.md)：规则 4、5；未标引状态 |
| 第一原理与设计理由 | [第一原理与设计理由](../concepts/first-principles.md) | Aristotle；Kunz & Rittel IBIS（1970）；Nygard ADR（2011） | 本文；设计文档不删旧决定 |
| 写作规范 | 待写：一篇「写作规范」，层次为写作规范 → 技术写作规范 → 文档分类 | 为读者写：Plain language 运动；技术写作：Google style guide、Microsoft style guide、阮一峰、GB/T 15834；文档分类：Diátaxis | `writing.md`（待写）；CLAUDE.md 标题与完整性规则；目录划分 `concepts/` 解释、`design/` 参考 |
| 知识体系作上层结构 | [知识体系](../concepts/body-of-knowledge.md) | SWEBOK / ISO/IEC TR 19759；CS2023；GB/T 13745；ISO 25964-2 §19 | [hierarchy.md](hierarchy.md)：第 2、3 层取自知识领域与知识单元 |
| 词表映射 | [词表映射](../concepts/vocabulary-mapping.md) | ISO 25964-2 §6–11；SKOS §10 | [sources-registry.md](sources-registry.md)：三种用法、`match`、默认 closeMatch |
| 借入照抄与本地分析分层 | [词表的层级](../concepts/vocabulary-hierarchy.md)（数组可选、多数组归属）、[分面](../concepts/facet.md)（分析是重组）、[知识体系](../concepts/body-of-knowledge.md)（枚举、只借上层） | ISO 25964-1 数据模型；Z39.19 §8.3.5 | [decisions/borrow-and-analyze.md](decisions/borrow-and-analyze.md)；[hierarchy.md](hierarchy.md) 规则 6、9–12 |
| 来源分级 | 无 | **本库自定，无外部来源** | [review.md](review.md) |

## 未登记的做法

目前没有原理支撑、只是习惯的做法，要么补登记，要么删掉：

- 概念文的固定分节（定义 / 解决的问题 / 用法 / 来源）
- 分面字段的取值，见 [drafts/facet-field.md](drafts/facet-field.md)

## 待办

- 写概念文「写作规范」（含技术写作规范、文档分类两层），把第一原理从本文旧版移过去
