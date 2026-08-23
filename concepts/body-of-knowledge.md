# 知识体系 (Body of Knowledge)

## 定义

知识体系是一个学科或职业**公认的知识范围的结构化清单**：这个领域有哪些知识区域、每个区域包含哪些主题、从业者应掌握到什么程度。它由行业组织或标准机构编制，目的是划定学科边界、统一教育和认证的口径。

这是各行业通用的做法，项目管理、业务分析、数据管理、信息安全都有自己的知识体系。本文例子偏向计算领域，因为本库的分支在那里，不是概念本身的限制。

ISO/IEC TR 19759:2015（即 SWEBOK 指南）对自己的描述：**刻画软件工程学科的边界，并为支撑该学科的文献提供按主题的入口**。SWEBOK 强调收录的是“普遍接受的”（generally accepted）知识——大多数项目在大多数时候适用、且被广泛认同的——不收前沿研究和专门领域。

## 解决的问题

| 问题 | 例子 | 知识体系的处理 |
|---|---|---|
| 学科边界不清，各说各话 | “软件工程”包不包括项目管理？ | 明确列出知识领域，在内的就在内 |
| 教育和认证没有统一依据 | 两所学校的课程覆盖完全不同 | 课程按知识体系设计，认证按它考 |
| 从业者不知道自己的盲区 | 只会自己做过的那部分 | 对照清单，没碰过的一目了然 |
| 文献检索没有入口 | 不知道某主题该从哪本书、哪个标准读起 | 每个主题附参考文献 |

## 结构

知识体系通常是三层：

```
知识领域 (knowledge area, KA)       学科的主要区域,十几个
└─ 知识单元 (knowledge unit, KU)    领域内的主题簇,每领域几个到二十几个
    └─ 主题 (topic)                 具体知识点;常标核心 / 选修,以及掌握层级
```

CS2023 的表述：知识领域 = {知识单元} + {职业素养}；每个主题属于核心或选修，并用布鲁姆分类标注预期掌握层级。SWEBOK 用“知识领域 → 主题 → 子主题”，每个知识领域是指南的一章。

## 常见的知识体系

| 名称 | 领域 | 编制者 | 结构 | 状态 |
|---|---|---|---|---|
| [SWEBOK Guide v4.0](https://www.computer.org/education/bodies-of-knowledge/software-engineering) | 软件工程 | IEEE Computer Society;ISO/IEC TR 19759 采纳（目前为 2015 版，对应 v3） | 18 个知识领域 | 2024 年发布 |
| [CS2023](https://csed.acm.org/cs2023/) | 计算机科学本科课程 | ACM、IEEE-CS、AAAI 联合工作组 | 17 个知识领域，下分知识单元和主题；另有能力模型 | 2024 年 1 月发布 |
| [ACM Computing Classification System](https://dl.acm.org/ccs) | 计算领域文献分类 | ACM | 多层级分类树，用于论文标引 | 2012 版 |
| [GB/T 13745-2009《学科分类与代码》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E) | 全部学科 | 国家标准 | 一级 / 二级 / 三级学科，带代码 | 现行 |
| [BABOK Guide v3](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/) | 业务分析 | IIBA | 6 个知识领域 | 现行 |
| [DAMA-DMBOK](https://dama.org/learning-resources/dama-data-management-body-of-knowledge-dmbok/) | 数据管理 | DAMA | 本文未核对结构 | 第 2 版 |
| [CISSP CBK](https://www.isc2.org/certifications/cissp) | 信息安全 | (ISC)² | 8 个领域（domain），本文未核对 | 现行 |
| PMBOK Guide | 项目管理 | PMI | 本文未核对；官网对脚本返回 403 | 第 7 版 |

图书情报领域没有一份叫“知识体系”的文件，对应物是学会的核心能力清单（如 [ALA Core Competences](https://www.ala.org/educationcareers/careers/corecomp/corecompetences)）和 GB/T 13745 的学科划分。

严格说 ACM CCS 和 GB/T 13745 是**分类法**而不是知识体系——前者为标引文献、后者为统计和管理而编，不描述“从业者应掌握什么”。但三者都给出了一个领域的公认划分，在本库的用途上等价。

## 与受控词表的关系

知识体系不是为检索设计的，它是课程大纲和学科地图。和叙词表相比：

| | 知识体系 | 叙词表 |
|---|---|---|
| 目的 | 划定学科、指导教学 | 标引和检索 |
| 单位 | 主题（一段描述加参考文献） | 概念（有 ID、首选词、别名） |
| 关系 | 只有包含（领域 ⊃ 单元 ⊃ 主题） | 等价、层级、相关三种 |
| 同义控制 | 无 | 有 |
| 更新 | 每几年一版 | 持续 |

所以知识体系不能直接当词表用——它没有别名、没有范围注释、没有跨领域的相关关系。但它的前两层是一个领域**被公认的划分**，这正是自上而下建词表上层结构时最需要的东西：拿来就有依据，不必自己发明分法。ISO 25964-2 第 19 章把这类“为组织知识而建的层级”归入 taxonomy，并给出了与叙词表互操作的建议。

## 在知识库中的用法

1. **只借上层，不借底层**。取知识领域和知识单元作为词表的第 2、3 层；主题层不预建，等内容来了再长
2. **一个分支一个知识体系**。两个体系对同一领域的划分必然重叠错位，混用就打架；其他体系只做映射
3. **保留原编码**。`FPL-Types`、`870.30` 这类代码写进概念的 `match`，日后体系改版能对上
4. **空节点是盲区地图**。知识体系列了而你没有内容的单元，就是你不知道自己不知道的地方——这是用知识体系而不是用自己的笔记建上层结构的全部理由
5. **注意适用范围**。CS2023 是本科课程，深度到“毕业生应知”为止；SWEBOK 只收普遍接受的知识。前沿和专门领域不在里面，那部分上层结构要靠别的来源

## 权威来源

- IEEE Computer Society. [*Guide to the Software Engineering Body of Knowledge (SWEBOK Guide), Version 4.0*](https://www.computer.org/education/bodies-of-knowledge/software-engineering). 2024. 18 个知识领域清单已核对
- [ISO/IEC TR 19759:2015](https://www.iso.org/standard/67604.html). Software Engineering — Guide to the software engineering body of knowledge (SWEBOK). 对应 SWEBOK v3
- ACM / IEEE-CS / AAAI. [*Computer Science Curricula 2023*](https://ieeecs-media.computer.org/media/education/reports/CS2023.pdf). 2024. 知识模型一节（第 29 页起）已核对
- ACM. [*The 2012 ACM Computing Classification System*](https://dl.acm.org/ccs)
- [GB/T 13745-2009《学科分类与代码》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E)
- [ISO 25964-2:2013](https://www.iso.org/standard/53658.html) 第 19 章 Taxonomies
