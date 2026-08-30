# 知识体系 (Body of Knowledge)

## 定义

知识体系把编制者为明确目的选取的知识组织成结构化说明。它可以刻画一门学科或一种职业实践的边界，也可以服务课程、认证或从业参考；具体对象、适用范围和内部结构以各体系自己的声明为准，不能预设所有体系都划分同一种范围。

项目管理、业务分析、数据管理、信息安全和计算机科学都有这样的资料。本文例子偏向计算相关内容，因为本库主要在这里取结构来源，不是知识体系这个概念本身的限制。

ISO/IEC TR 19759:2015 对 SWEBOK 的说明是：刻画软件工程学科的边界，并为支撑该学科的文献提供按主题的入口。SWEBOK 选取普遍接受的知识；CS2023 则为计算机科学本科课程规定知识模型和课程设计材料。两者的编制目的不同，不能由相同的层次名称推定范围相同。

## 解决的问题

| 问题 | 例子 | 常见处理 |
|---|---|---|
| 学科或职业边界不清 | “软件工程”是否包括项目管理？ | 由编制者声明对象、边界和纳入准则 |
| 教育和认证缺少共同依据 | 两所学校的课程覆盖完全不同 | 用知识结构组织课程或考试内容 |
| 从业者不知道自己的盲区 | 只会自己做过的那部分 | 对照结构化清单检查未接触的部分 |
| 文献检索没有入口 | 不知道某主题该从哪本书或哪个标准读起 | 为主题提供参考文献或检索入口 |

## 结构

知识体系的内部层次由各自目的决定。CS2023 的知识模型采用以下层次：

```
知识领域 (knowledge area, KA)
└─ 知识单元 (knowledge unit, KU)
   └─ 主题 (topic)
```

CS2023 把主题分为 CS Core、KA Core 和 Non-core，并用布鲁姆分类标注核心主题的预期掌握层级；每个知识领域还附有相关职业素养等课程材料。SWEBOK 则按“知识领域 → 主题 → 子主题”组织，每个知识领域构成指南的一章。这里的层次名称是来源自身的结构，不能外推为所有知识体系的固定层数。

## 常见的知识体系

下表按各编制者声明的对象和用途比较这些资料，不把每一行都预设为学科划分或知识体系。

| 名称 | 对象与用途 | 编制者 | 结构 | 版本或状态 |
|---|---|---|---|---|
| [SWEBOK Guide v4.0](https://www.computer.org/education/bodies-of-knowledge/software-engineering) | 软件工程学科边界和支撑文献入口 | IEEE Computer Society；ISO/IEC TR 19759 采纳 v3 | 18 个知识领域 | 2024 年发布 |
| [CS2023](https://csed.acm.org/cs2023/) | 计算机科学本科课程指南 | ACM、IEEE-CS、AAAI 联合工作组 | 17 个知识领域，下分知识单元和主题；另有能力模型 | 2024 年定稿并获三家机构认可 |
| [ACM Computing Classification System](https://dl.acm.org/ccs) | 计算文献的分类、标引和检索 | ACM | 多层级分类树 | 2012 版 |
| [GB/T 13745-2009《学科分类与代码》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E) | 学科分类与代码 | 国家标准 | 一级、二级和三级学科，带代码 | 现行 |
| [BABOK Guide v3](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/) | 业务分析实践 | IIBA | 6 个知识领域 | 第 3 版 |
| [DAMA-DMBOK](https://dama.org/learning-resources/dama-data-management-body-of-knowledge-dmbok/) | 数据管理职业实践和组织参考 | DAMA | 本文未核对结构 | 第 2 版修订本；第 3 版项目进行中 |
| [CISSP Exam Outline](https://www.isc2.org/certifications/cissp/cissp-certification-exam-outline) | 信息安全专业认证考试范围 | ISC2 | 8 个考试范围 | 当前考试大纲 |
| [PMBOK Guide](https://www.pmi.org/standards/pmbok) | 项目管理实践 | PMI | 7 个 `performance domain` | 第 8 版，2025 年发布 |

本文核到的图书情报材料是 [ALA Core Competences](https://www.ala.org/educationcareers/2022-update-alas-core-competences-librarianship) 这样的职业能力清单，以及 GB/T 13745 的学科分类；它们的名称、对象和用途都不能改写成一份并不存在的同名知识体系。

ACM CCS 和 GB/T 13745 是分类体系，ALA 材料是职业能力清单，SWEBOK、CS2023、BABOK、DAMA-DMBOK 和 PMBOK 也各有自己的编制目的。它们都可能为本库提供结构、映射或核对材料，但这些用途不表示它们在语义上等价。能复用哪一部分，须分别依据来源声明的目的、对象和纳入准则判断。

## 与受控词表的关系

知识体系通常不是为受控标引和检索而编制的。以下比较说明本篇所列知识体系与叙词表的主要差异；具体结构仍以各来源为准。

| | 知识体系 | 叙词表 |
|---|---|---|
| 目的 | 说明知识边界，服务教育、认证或实践 | 标引和检索 |
| 单位 | 主题（一段描述加参考文献） | 概念（有 ID、首选词、别名） |
| 关系 | 以来源规定的包含层次为主 | 等价、层级、相关三种 |
| 同义控制 | 通常不承担 | 承担 |
| 更新 | 按来源版本更新 | 可以持续维护 |

因此，知识体系不能不经转换直接当作叙词表使用；它通常缺少叙词表所需的同义控制、范围注释和相关关系。它的上层结构可以成为自上而下建设的来源，但只有两个来源同时覆盖同一主题树分支内的重叠主题，并对这些主题提供同一种结构划分时，才构成结构来源冲突。只因来源名称或宽泛适用范围相近，不能推出冲突。

ISO 25964-2:2013 第 19 章讨论 taxonomy 与叙词表的互操作。这个来源支持结构转换和映射的方向，不替本库决定具体来源的角色，也不把分类体系、知识体系和能力清单合并成同一类资料。

## 在知识库中的用法

1. 按来源角色取用。知识体系的上层结构可以作为结构候选，分类体系和能力清单也可以用于核对或映射；具体用途按来源声明和本库既有准入规则判断，不由表面相似的层次名称决定。
2. 冲突时只取一个结构来源。两个来源只有在同一主题树分支内覆盖重叠主题，并提供同一种结构划分时才冲突；冲突时选定一个结构来源，其他来源只作映射。条件不同时，可以按来源分组或承担不同用途。
3. 保留原编码。`FPL-Types`、`870.30` 这类代码写进概念的 `match`，日后来源改版时仍可回查。
4. 用空节点显示盲区。来源列出而本库没有内容的单元，可以显示尚未覆盖的部分；这不自动要求新增内容或扩大范围。
5. 先确定项目范围再判断缺口。分别依据每个来源明示的目的、对象和纳入准则判断其覆盖。只有项目范围已经由人确定，项目需要而该来源没有覆盖的主题，才构成相对于该来源的缺口；不能自定一条统一的前沿或专门内容边界。

## 权威来源

- IEEE Computer Society. [*Guide to the Software Engineering Body of Knowledge (SWEBOK Guide), Version 4.0*](https://www.computer.org/education/bodies-of-knowledge/software-engineering). 2024. 18 个知识领域清单已核对
- [ISO/IEC TR 19759:2015](https://www.iso.org/standard/67604.html). Software Engineering — Guide to the software engineering body of knowledge (SWEBOK). 对应 SWEBOK v3
- ACM、IEEE-CS、AAAI. [*Computer Science Curricula 2023*](https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm). 2024. 知识模型一节已核对
- ACM. [*The 2012 ACM Computing Classification System*](https://dl.acm.org/ccs)
- [GB/T 13745-2009《学科分类与代码》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E)
- IIBA. [*A Guide to the Business Analysis Body of Knowledge*](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/)
- DAMA International. [*DAMA Data Management Body of Knowledge*](https://dama.org/learning-resources/dama-data-management-body-of-knowledge-dmbok/)
- ISC2. [*CISSP Certification Exam Outline*](https://www.isc2.org/certifications/cissp/cissp-certification-exam-outline)
- ALA. [*2022 Update to ALA's Core Competences of Librarianship*](https://www.ala.org/educationcareers/2022-update-alas-core-competences-librarianship)
- PMI. [*PMBOK Guide*](https://www.pmi.org/standards/pmbok)
- [ISO 25964-2:2013](https://www.iso.org/standard/53658.html) 第 19 章 Taxonomies
