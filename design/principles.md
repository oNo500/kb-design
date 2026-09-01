# 方法登记

本库采用的每一种方法或范式，在这里登记来源和导出的规则。方法的第一原理写在对应的概念文里；没有概念文的方法标明。

准入规则：引入新方法先登记；提出新规则先看能否从已登记方法的原理推出，推不出就不加。理由见[第一原理与设计理由](../concepts/first-principles.md)。方法登记只确定推导依据与能力边界，不使草案、接口、来源数据或符合性主张生效。

## 登记表

| 方法 | 概念文 | 来源 | 导出的规则 |
|---|---|---|---|
| 受控词表 | [受控词表](../concepts/controlled-vocabulary.md) | Wüster, *Internationale Sprachnormung in der Technik*, 1931 博士论文；ISO 25964-1；ISO 704 | [topics.md](topics.md)：ID 与名字分离、等价关系、范围注释、生命周期；来源依据不代替 designation 准入 |
| 分面分析 | [分面](../concepts/facet.md) | Ranganathan（1933）；Z39.19 §5.3.4；ISO 25964-1 §11 | 分面字段草案；后组式标签；实体表的 kind / form / subjects |
| 划分特征与数组 | [词表的层级](../concepts/vocabulary-hierarchy.md) | ISO 25964-1 §2.1、§2.4、§2.38 | [hierarchy.md](hierarchy.md) 规则 9–12；`arrays` 字段；来源数组只保存现行实际结构来源 |
| 依据 warrant | [词表的建设与维护](../concepts/vocabulary-construction.md) | Hulme, *Principles of Book Classification*, Library Association Record 1911–12；Z39.19 §5.3.5 | 从带上下文的字符串开始，经概念判断和依据核验建立 `candidate` 概念记录；发现用途和探测信号只提供待审线索；两次零引用只使该记录取得删除资格；[maintenance.md](maintenance.md) 记录相应信号 |
| 复制的层级求完整 | [词表的建设与维护](../concepts/vocabulary-construction.md)（自上而下、层级补位） | 本库 README；Z39.19 §11.1.3.1、§11.1.8 | [hierarchy.md](hierarchy.md) 规则 4、5；`unassigned` 作为概念记录状态；复制记录以 `source` 保存实际派生，本地建立不使用 `source: self` |
| 原样复制与本地分析分层 | [词表的层级](../concepts/vocabulary-hierarchy.md)（数组可选、多数组归属）、[分面](../concepts/facet.md)（分析是重组）、[知识体系](../concepts/body-of-knowledge.md)（枚举、只借上层） | ISO 25964-1 数据模型；Z39.19 §8.3.5 | [decisions/borrow-and-analyze.md](decisions/borrow-and-analyze.md)；[hierarchy.md](hierarchy.md) 规则 6、9–12；派生来源和本地分析互不替代 |
| 知识体系作上层结构 | [知识体系](../concepts/body-of-knowledge.md) | SWEBOK / ISO/IEC TR 19759；CS2023；GB/T 13745；ISO 25964-2 §19 | [hierarchy.md](hierarchy.md)：第 2、3 层取自知识领域与知识单元；现行结构来源取正式用途值，后置严格引用须经角色决定 |
| 词表映射 | [词表映射](../concepts/vocabulary-mapping.md) | ISO 25964-2 §6–11；SKOS §10 | [sources-registry.md](sources-registry.md)：来源用法、`match`、五种关系和默认 `closeMatch`；映射是概念范围判断，不由标签、用途资格、`source` 或迁移分类自动生成 |
| 名称规范表 | [词表映射](../concepts/vocabulary-mapping.md)（与各类词表互操作）、[受控词表](../concepts/controlled-vocabulary.md) | ISO 25964-2 §23 | [entities.md](entities.md) 保存来源身份；[sources-registry.md](sources-registry.md) 保存来源用途；身份、用途和具体引用互不替代 |
| 新主题的分类 | [新主题的分类](../concepts/classifying-new-subjects.md) | Ranganathan 好客准则（1957）；Hulme（1911）；Hjørland & Albrechtsen（1995）；Bowker & Star（1999、2007） | 实体表的 kind / form / subjects；本地概念 candidate；通用 `origin` 不再使用，发现观察、具体值依据、实际派生和概念映射分别处理；[maintenance.md](maintenance.md) 剩余监控 |
| 元数据 | [元数据](../concepts/metadata.md) | Dublin Core：ISO 15836-1:2017、ISO 15836-2:2019；DCMI Metadata Terms 2020 | [content-model.md](content-model.md) |
| Application Profile | [Application Profile](../concepts/application-profile.md) | [DCMI Application Profiles 阅读笔记](../sources/dcmi-application-profiles.md)；[Obsidian 官方帮助阅读笔记](../sources/obsidian-help.md) | 从 metadata／应用需求导出功能范围、模型引用、字段约束、使用指南和 encoding；不产生 DCAP conformance |
| Reproducible Builds | [Reproducible Builds](../concepts/reproducible-builds.md) | [Reproducible Builds 阅读笔记](../sources/reproducible-builds.md)；[BagIt 文件包格式阅读笔记](../sources/rfc-8493.md)；[RFC 8785 阅读笔记](../sources/rfc-8785.md)；[W3C PROV 阅读笔记](../sources/w3c-prov.md)；[Python 文件系统阅读笔记](../sources/python-filesystem.md) | 从 source／environment／instructions／artifact 导出确定性与可重建证据边界；当前只使用它限制完成声明 |
| 第一原理与设计理由 | [第一原理与设计理由](../concepts/first-principles.md) | Aristotle；Kunz & Rittel IBIS（1970）；Nygard ADR（2011） | 本文；[decisions/](decisions/) 不删旧决定；来源结构决定不代替逐项外部事实或项目决定 |
| 写作规范 | [写作规范](../concepts/writing-conventions.md) | 原则：ISO 24495-1:2023；中文书面语：GB/T 15834、W3C clreq；技术写作：Google、Microsoft style guide；文档分类：Diátaxis | [writing.md](writing.md)；`AGENTS.md` 为其摘要；目录划分 `concepts/` 解释、`design/` 参考；[content-model.md](content-model.md) 文档类型词表取 Diátaxis 四类 |
| 治理 | [治理](../concepts/governance.md) | ISO 37000:2021；DAMA-DMBOK 数据治理；ISO 15489-1 §6 | [governance.md](governance.md) 政策、决策权、变更控制、审计；来源 schema、索引、探测和迁移能力不取得正式修改权限 |
| 笔记的类型 | [笔记的类型](../concepts/note-types.md) | Diátaxis；DITA 1.3；IPTC genre；Ahrens 2017；Nonaka 1991；Bloom / Krathwohl 2002；SOLO 1982 | [content-model.md](content-model.md) `type` 的重定（待） |
| 来源分级与复核 | 无概念文；依据见[词表的建设与维护](../concepts/vocabulary-construction.md)的组织依据 | Z39.19 §5.3.5.2；复核周期为本库估值 | [entities.md](entities.md) 现行 `tier`；[maintenance.md](maintenance.md) 阈值表；固定夹具探测只提出复核范围，`--live` 禁用，正式值只由人工复核和原有权限修改 |
| 处置决定 | [ISO 15489 笔记](../sources/iso-15489.md)（无概念文；标准不直接适用，只借其处置原则） | ISO 15489-1:2016 §3.8、§8.5 | [content-model.md](content-model.md) 处置决定；词表生命周期的“不删”；来源变化和角色退役不删除历史引用 |
| 断言的依据 | 无（治理规则） | Z39.19 §11.1.4；ISO 15489-1 §4 (c)；W3C PROV-O | [maintenance.md](maintenance.md) 断言一节；`check-topics.py` 判断债统计；具体值 `basis`、实际派生 `source`、概念映射 `match` 和项目决定互不替代 |

## 效力边界

Application Profile 与 Reproducible Builds 的登记只建立推导方法和完成声明边界，不建立正式 Application Profile，也不产生 DCAP、DCAM、DCTAP、JCS、BagIt 或 reproducible build conformance。来源笔记、现行 Obsidian 设计和代码不因方法登记而改变。

来源 schema、离线校验、反向索引、固定夹具探测、历史迁移预演和复核义务接口已经存在，但正式来源数据、严格引用和角色状态尚未迁移，来源治理草案仍未生效。既有迁移账本只作历史审计，不能证明当前 HEAD 可重放，也不能把推荐值写成现行规则或数据。

## 未登记的做法

目前没有原理支撑、只是习惯的做法，要么补登记，要么删掉：

- 概念文的固定分节（定义 / 解决的问题 / 用法 / 来源）
