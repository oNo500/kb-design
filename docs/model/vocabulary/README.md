# 主题词表

主题词表为内容提供主题标引、检索和导航所需的概念及关系。内容通过概念 ID 引用主题，名称用于显示和查找；软件、组织、编程语言等具体对象由[命名实体词表](../entities/entities.md)管理。

例如，“Rust 的所有权”在内容中使用 `subject: [systems-execution-and-memory-model]` 表达主题，用 `entities: [rust]` 表达涉及的语言。按主题和按具体语言查找内容，分别使用这两类信息。

## 现行设计

| 文章 | 规定内容 |
|---|---|
| [主题词表设计](topics.md) | 覆盖范围、概念记录、语言依据、关系、生命周期与生成路径 |
| [层级结构](hierarchy.md) | 按学科组织的上层结构、多上位关系、数组和结构来源 |

正式数据是 [topics.yaml](../../../data/vocab/topics.yaml)，编辑入口是主题生成输入与核心实现。数据怎样修改和重建，按主题词表设计中的生成路径执行。

## 概念解释

| 需要理解的问题 | 文章 |
|---|---|
| 概念、名称和概念关系怎样分开？ | [受控词表](controlled-vocabulary.md) |
| 上下位关系、数组和节点标签分别表示什么？ | [词表的层级](vocabulary-hierarchy.md) |
| 本地概念怎样与外部词表对应？ | [词表映射](vocabulary-mapping.md) |
| 什么材料支持概念的收录和维护？ | [词表的建设与维护](vocabulary-construction.md) |
| 外部体系能提供什么结构依据？ | [知识体系](body-of-knowledge.md) |
| 没有现成位置的主题怎样判断？ | [新主题的分类](classifying-new-subjects.md) |
| 按类别分析与按用途分组有什么区别？ | [分面](facet.md)、[概念组](concept-group.md) |
| 增加关系类型会带来什么变化？ | [知识图谱](knowledge-graph.md) |

概念文解释一般含义；本项目采用哪些结构及其适用范围，以现行设计和具体采纳决定为准。

## 设计依据

| 材料 | 查阅用途 |
|---|---|
| [ISO 25964 叙词表标准](reading-iso-25964.md) | 已阅读的概念、关系和模型材料 |
| [ANSI/NISO Z39.19 受控词表指南](reading-z39-19.md) | 已阅读的词表建设、表示与维护要求 |
| [GB/T 13745 学科分类清单](reading-gbt-13745.md) | 本库相关学科的来源条目 |

阅读笔记分别记录材料范围和核对边界；具体派生与映射仍需各自的依据。

## 相关决定

- [树按学科而非分面的决定](decision-tree-by-discipline.md)：上层结构的选择理由。
- [原样复制与本地分析分层的决定](decision-borrow-and-analyze.md)：借入结构与本地分析的职责划分。
- [来源收尾决定](../sources/decision-source-completion.md)：既有数组成员、顺序和未核映射的具体处置；阅读前两项决定时需结合这些后续采纳。

名称与语言依据另见[语言依据结构](../terminology/decision-structured-label-basis.md)，文献身份与引用位置见[参考文献分离](../sources/decision-source-bibliography-separation.md)。

## 待议方案

以下提案均未生效，列出它们是为了说明当前仍在讨论的问题。

| 问题 | 提案 |
|---|---|
| 是否增加横向分类字段？ | [分面字段草案](proposal-facet-field.md) |
| 怎样批准分析数组的划分特征？ | [划分特征草案](proposal-division-characteristics.md) |
| 是否建立手工维护的概念集合？ | [概念组草案](proposal-concept-groups.md) |
| 生活相关知识是否纳入范围？ | [生活领域范围](proposal-life-scope.md) |
| 传播学科相关范围怎样组织？ | [传播学科范围](proposal-communication-scope.md) |

## 相邻主题

内容如何引用主题，见[内容模型](../content/content-model.md)；词表的维护与版本规则，见[维护](../../governance/maintenance/maintenance.md)和[词表版本](../../governance/maintenance/versioning.md)。

工作区浏览见[词表预览](../../applications/vocab-preview/vocab-preview.md)，知识库中的具体表示见[Obsidian 映射](../../applications/obsidian/obsidian.md)。返回[项目文档](../../README.md)。
