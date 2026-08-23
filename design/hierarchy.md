# 主题词表的层级结构

主题词表的树分四层以上：前三层从知识体系复制，第 4 层起本地建立。每一层按一个划分特征往下分；一个概念下按几个划分特征分，就有几个数组，每个数组有节点标签说明按什么分。本文定这棵树的分层规则、每层的划分特征、每个第 2 层概念下复制哪些数组。

概念记录的字段在[主题词表设计](topics.md)，来源的登记在[来源名称规范表](sources-registry.md)。理论依据见 [词表的层级](../concepts/vocabulary-hierarchy.md)、[知识体系](../concepts/body-of-knowledge.md)、[树按学科而非分面的决定](decisions/tree-by-discipline.md)。

## 规则

十五条，分四组。复制与分析分两层的理由见[原样复制与本地分析分层的决定](decisions/borrow-and-analyze.md)。

### 树的性质

1. 顶层按学科切，理由见[树按学科而非分面的决定](decisions/tree-by-discipline.md)。分面是概念上的横向字段，概念组是视图，都不在树里
2. 允许多层级：`broader` 是列表，顺序不赋予含义。例：“软件工程管理”同时在 `software-engineering` 和 `management` 之下

### 复制

3. **可作结构来源的**：[来源名称规范表](sources-registry.md)中 `role` 含 `structure` 的；其资格要求（tier、版本）见那里
4. **顶层由范围决定，顶层之下起步全借**：顶层概念是[范围](topics.md)声明的学科，`source: self`，各自 `match` 到 GB/T 13745；顶层之下，每个可作结构来源的在它对应的概念下全部以未标引状态建入。未标引节点多是目的——它们就是盲区地图。范围之内求完整，范围之外不存在
5. **复制的深度**：借到第 3 层，即知识体系中有稳定编号、可被引用的最深一层。CS2023 的知识单元有代码，其下的主题没有；SWEBOK 的主题有章节号，子主题没有；GB/T 13745 三级学科有代码——都落在第 3 层。再往下没有可引用的权威结构

```
从知识体系复制  第 1 层  顶层概念    computing / library-and-information-science
               第 2 层             security / networking-and-communication / information-science …
               第 3 层             input-validation / transport-layer / 情报检索学 …
本地建立        第 4 层起           sql-injection / http / facet-analysis …
```

6. **原样复制**：复制的概念作为上位的下位集合原样保留，成员、顺序按来源，不拆、不改、不配节点标签
7. **复制的记录**：概念写 `source`，并 `match` 回源头条目。`source` 说来历，`match` 说对应哪一条；改版后章节号可能变，两者不互相替代
8. **本地建立**：第 4 层起由本库按依据建立，深度不限，`source: self`。派生概念组的成员只有本库已有的概念，暴露不了盲区，不替代复制

### 数组

9. **数组是可选的**。一个概念的下位默认是一个集合；只在需要区分成几组时登记数组。数组只分组，不改概念
10. **按来源分组**：一个概念的下位来自多个来源时，每个来源的下位登记为一个数组，标识是 `source`。例：security 下 ASVS、CWE、ATT&CK 各一个
11. **按划分特征分组**：可对下位集合做分析，每个划分特征一个数组，标识是 `characteristic`。划分特征是本库自定，属零自定的例外，目前尚未开放；开放后按[划分特征治理](drafts/division-characteristics.md)（草案）登记，通过判据“A 和 B 的区别是 ___”，且完备划分
12. 一个概念在同一划分特征下只属一组，在不同划分特征下可各属一组（ISO 25964-1 数据模型 `isMemberOfArray 0..*`)
13. **同一视角只取一个来源**：两个来源对同一批东西做同一种划分时只借一个，另一个只做映射。OWASP Top 10 与 CWE 都是缺陷清单，取 CWE

### 节点标签

14. 只有以划分特征为标识的数组写节点标签，形式 `(按 X)`,X 是名词；以来源为标识的数组显示来源名，那是标识不是节点标签。分面名 `[X]` 的形式本库暂不出现
15. 节点标签不是概念：不能标引、不进术语表、不能做 `broader` 的目标；不为分组层造复合概念（Z39.19 §7.7）

## 各概念下的来源

每个概念的下位从哪些来源复制。一个概念下多于一个来源时，各来源的下位各成一个数组（规则 10）。分析层数组目前没有。id 用描述性 slug；来源里的代码只记在 `match`。

### 顶层与第 2 层

| 概念 | 下位来源 | 借到 |
|---|---|---|
| （根） | 范围声明的八个学科，`source: self`，各 `match` GB/T 13745 一级学科 | 第 1 层 |
| computing | CS2023 17 个知识领域 | 第 2 层 |
| mathematics、information-and-systems-science、management、linguistics、journalism-and-communication、education | GB/T 13745 各自的二级学科 | 第 2 层 |
| library-and-information-science | GB/T 13745 二级学科 870.10–870.50 | 第 2 层 |

### computing 之下

CS2023 的 17 个知识领域作第 2 层；每个知识领域的知识单元作第 3 层的第一个数组；有其他可结构来源的，各加一个数组。

| 第 2 层 id | CS2023 | 知识单元数 | 其他来源数组 | 原分支 |
|---|---|---|---|---|
| algorithmic-foundations | AL | 5 | — | foundations 的一部分 |
| architecture-and-organization | AR | 11 | — | foundations 的一部分；硬件落这里 |
| artificial-intelligence | AI | 12 | ATLAS 16 战术；OWASP LLM Top 10 2025 | ai |
| data-management | DM | 13 | — | data |
| foundations-of-programming-languages | FPL | 22 | — | programming-languages |
| graphics-and-interactive-techniques | GIT | 12 | — | 无，新盲区 |
| human-computer-interaction | HCI | 6 | — | human-centered-computing |
| mathematical-and-statistical-foundations | MSF | 5 | — | foundations 的一部分；与顶层 mathematics 多层级 |
| networking-and-communication | NC | 8 | RFC 1122 四层 | network |
| operating-systems | OS | 14 | — | 无，新盲区 |
| parallel-and-distributed-computing | PDC | 5 | — | 无，新盲区 |
| security | SEC | 8 | ASVS 5.0 章；CWE 顶层类别；ATT&CK 15 战术 | security |
| society-ethics-and-the-profession | SEP | 11 | — | 无；通用职业技能另一落点 |
| software-development-fundamentals | SDF | 5 | — | 无，新盲区 |
| software-engineering | SE | 9 | SWEBOK v4 18 章 | engineering |
| specialized-platform-development | SPD | 7 | — | web 降为其下的知识单元 Web Platforms |
| systems-fundamentals | SF | 9 | — | foundations 的一部分 |

知识单元数据 CS2023 正式版（2024-01）统计，含各领域的 SEP 单元。

原 `web` 的处理：CS2023 里 Web 只是 SPD 的一个知识单元，本库不另立第 2 层。MDN 技术参考的 19 个分区在 Web Platforms 之下是第 4 层，超出复制的深度（规则 5），因此 MDN 只作映射来源，不复制；Web 相关的本地概念从内容里长。这是按 CS2023 全借的直接代价，待观察。

### library-and-information-science 之下

| 第 2 层 | GB/T 13745 | 第 3 层来源 |
|---|---|---|
| library-science 图书馆学 | 870.10 | 三级学科 870.10xx,10 个 |
| documentation 文献学 | 870.20 | 三级学科 870.20xx,6 个 |
| information-science 情报学 | 870.30 | 三级学科 870.30xx,13 个 |
| archival-science 档案学 | 870.40 | 三级学科 870.40xx,4 个 |
| museology 博物馆学 | 870.50 | 无三级学科 |

原拟自加的“内容工程”取消：叙词表与检索语言归 870.3050 情报检索学，分类法归 870.1040 图书分类学，元数据与编目归 870.1045 图书编目学；术语学归顶层 linguistics 之下，结构化写作见[主题词表设计](topics.md)的邻近主题表。

### 其他六个顶层之下

二级、三级学科清单见 [GB/T 13745 学科分类清单](../sources/gbt-13745.md)。

| 顶层 | GB/T 13745 | 二级学科 | 三级学科 |
|---|---|---|---|
| mathematics | 110 | 25 | 142 |
| information-and-systems-science | 120 | 7 | 18 |
| management | 630 | 12 | 43 |
| linguistics | 740 | 10 | 73 |
| journalism-and-communication | 860 | 7 | 30 |
| education | 880 | 18 | 0（标准原文无三级） |

术语学在 GB/T 13745 里没有对应学科，作本地概念挂在 740.35 应用语言学之下。

## 结构预览

```
(根)                                            ← 范围声明
├─ mathematics 数学                             ← GB/T 110;25 二级 / 142 三级
├─ information-and-systems-science              ← GB/T 120;7 / 18
├─ computing 计算机科学技术                     ← GB/T 520
│   ├─ algorithmic-foundations                  ← CS2023 AL,5 个知识单元
│   ├─ architecture-and-organization            ← AR,11;硬件落这里
│   ├─ artificial-intelligence                  ← AI
│   │   [CS2023 AI 12 知识单元]
│   │   [ATLAS]                                 ← 待核
│   │   [OWASP LLM Top 10]                      ← 待核
│   ├─ data-management                          ← DM,13
│   ├─ foundations-of-programming-languages     ← FPL
│   │   [CS2023 FPL 22 知识单元]
│   │   [具体语言]                               ← 术语表:python / rust / …
│   ├─ graphics-and-interactive-techniques      ← GIT,12;新盲区
│   ├─ human-computer-interaction               ← HCI,6
│   ├─ mathematical-and-statistical-foundations ← MSF,5;与 mathematics 多层级
│   ├─ networking-and-communication             ← NC
│   │   [CS2023 NC 8 知识单元]
│   │   [RFC 1122 四层]
│   ├─ operating-systems                        ← OS,14;新盲区
│   ├─ parallel-and-distributed-computing       ← PDC,5;新盲区
│   ├─ security                                 ← SEC
│   │   [CS2023 SEC 8 知识单元]
│   │   [ASVS 5.0]
│   │   [CWE 顶层类别]
│   │   [ATT&CK 15 战术]
│   ├─ society-ethics-and-the-profession        ← SEP,11;职业技能落这里
│   ├─ software-development-fundamentals        ← SDF,5;新盲区
│   ├─ software-engineering                     ← SE
│   │   [CS2023 SE 9 知识单元]
│   │   [SWEBOK v4 18 章]                        ← 项目管理落第 9 章
│   ├─ specialized-platform-development         ← SPD,7;Web Platforms 在其中
│   └─ systems-fundamentals                     ← SF,9
├─ management 管理学                            ← GB/T 630;12 / 43
├─ linguistics 语言学                           ← GB/T 740;10 / 73;术语学挂 740.35 之下
├─ journalism-and-communication                 ← GB/T 860;7 / 30
├─ library-and-information-science              ← GB/T 870
│   ├─ library-science 图书馆学                 ← 870.10xx,10
│   ├─ documentation 文献学                     ← 870.20xx,6
│   ├─ information-science 情报学               ← 870.30xx,13;情报检索学在其中
│   ├─ archival-science 档案学                  ← 870.40xx,4
│   └─ museology 博物馆学                       ← 无三级学科
└─ education 教育学                             ← GB/T 880;18 二级,无三级

图例:「←」后是下位的来源和数量。方括号行是以来源为标识的数组,出现在一个概念下有多个来源时。
      分析层数组目前没有。第 3 层以下不预建。
```

## 人工智能与编程语言

### 人工智能

CS2023 知识领域 AI 的 12 个知识单元：Introduction、Search、KRR、LRR、Probability、ML、NLP、Agents、Planning、Vision、Robotics、SEP。它偏学术——机器人、规划与本库侧重的 LLM 应用工程距离较远——但它是唯一有编号的人工智能知识体系；未标引的单元是盲区标记，不是负担。id 用 `artificial-intelligence`，侧重体现在内容里，不体现在知识体系的边界上。

LLM 应用相关的外部体系按规则 3、4、10 处理：ATLAS(2026.07 版，16 个战术，`AML.TA0000`–`AML.TA0015`）和 OWASP LLM Top 10(2025 版，`LLM01:2025`–`LLM10:2025`）有稳定编号，各自复制为一个以来源为标识的数组；NIST AI RMF 的四个功能是治理职能不是知识划分，只作映射；Anthropic 文档随产品迭代，只作映射。

### 编程语言

编程语言有跨语言的通识——类型系统、内存模型、求值与并发模型、范式——具体语言只是这些概念的不同取舍。`foundations-of-programming-languages`(CS2023 FPL)的下位是 22 个知识单元；具体语言（Python、Rust）是个体，不在主题树里，收在[命名实体词表](entities.md):

```
foundations-of-programming-languages   id 从英文首选词取，代码记在 match
  ├─ object-oriented-programming                                    FPL-OOP
  ├─ functional-programming                                         FPL-Functional
  ├─ logic-programming                                              FPL-Logic
  ├─ shell-scripting                                                FPL-Scripting
  ├─ event-driven-and-reactive-programming                          FPL-Event-Driven
  ├─ parallel-and-distributed-computing-foundations-of-programming-languages FPL-Parallel
  ├─ aspect-oriented-programming                                    FPL-Aspect
  ├─ type-systems                                                   FPL-Types
  ├─ systems-execution-and-memory-model                             FPL-Systems
  ├─ language-translation-and-execution                             FPL-Translation
  ├─ syntax-analysis                                                FPL-Syntax
  ├─ compiler-semantic-analysis                                     FPL-Semantics
  ├─ program-analysis-and-analyzers                                 FPL-Analysis
  ├─ code-generation                                                FPL-Code
  ├─ run-time-behavior-and-systems                                  FPL-Run-Time
  ├─ advanced-programming-constructs                                FPL-Constructs
  ├─ language-pragmatics                                            FPL-Pragmatics
  ├─ formal-semantics                                               FPL-Formalism
  ├─ formal-development-methodologies                               FPL-Methodologies
  ├─ design-principles-of-programming-languages                     FPL-Design
  ├─ society-ethics-and-the-profession-foundations-of-programming-languages FPL-SEP
  └─ program-abstraction-and-representation                         FPL-Abstraction
```

slug 为本库拟定，英文原名和代码为准；22 个知识单元全部以未标引状态建入，预期多数长期如此，这正是规则 4 的目的。

语言特性的内容单元主题挂通识节点，语言记在实体字段：“Rust 的所有权”`subject: [systems-execution-and-memory-model]`，`entities: [rust]`。按通识检索时它与 GC、引用计数并列；按语言检索时由实体表算出。

## 待定事项

- Web 相关内容失去复制结构后是否够用，观察后决定是否在 Web Platforms 下破例复制 MDN
- 多层级时 `broader` 列表的顺序暂不赋予含义；应用映射需要主上位时再定，记决定
- 分析层数组何时启用，见[划分特征治理](drafts/division-characteristics.md)
- 技术传播（技术写作、结构化写作）在树上没有节点，候选落点 `communication-studies` 下、依据 Wikidata Q1068718；暂缓，等 DITA 2.0 定稿、确定采用后再议（2026-08-23）
