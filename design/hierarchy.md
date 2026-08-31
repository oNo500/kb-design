# 层级结构

主题词表的节点都是概念。顶层概念表示本库范围内的学科；一个主题分支由某个顶层概念及其传递下位概念构成。树表达学科归属和概念层级，顶层以下的起步结构从现行来源复制，更深层的概念按本库依据建立。

概念记录字段见[主题词表设计](topics.md)，来源身份和用途见[来源名称规范表](sources-registry.md)。理论依据见[词表的层级](../concepts/vocabulary-hierarchy.md)、[知识体系](../concepts/body-of-knowledge.md)和[树按学科而非分面的决定](decisions/tree-by-discipline.md)。正式主题词表仍使用旧引用形状；共享来源引用已经实现但尚未迁移。

## 结构规则

以下规则分为树的性质、结构复制、数组分组和节点标签四组。复制与分析分层的理由见[原样复制与本地分析分层的决定](decisions/borrow-and-analyze.md)。规则编号继续供其他现行设计引用。

### 树的性质

1. 顶层按学科划分。八个顶层概念及其传递下位概念形成可查询的主题分支。分面表示概念的内在类别，概念组表示按用途圈定的视图；两者都不进入树，也不改变 `broader`。
2. 允许多层级。`broader` 是列表，顺序不赋予含义。例如，“软件工程管理”可以同时位于 `software-engineering` 和 `management` 之下。

### 结构复制

3. 现行结构来源必须在正式 `vocab/sources.yaml` 的 `role` 中含 `structure`，并满足该文件已经保存的用途及本文的现行来源选择。`tier`、版本或来源身份不能单独增加结构用途。后置严格接口还要求 `structure` 角色经决定批准；该角色状态尚未应用到正式数据。
4. 顶层由范围决定，顶层以下的起步结构全部借入。八个顶层是本地建立的范围边界，并分别 `match` 到 GB/T 13745；它们没有实际派生来源。正式旧数据保留的 `source: self` 只是待后置迁移处理的兼容值，不作为实际派生解释，也不得用于新增记录。每个现行合格结构来源在对应概念下的结构全部以 `unassigned` 状态建入；这些尚未用于标引的概念记录显示范围内的盲区，不要求扩大范围。
5. 结构借到来源中有稳定编号、可引用的最深一层。CS2023 的知识单元有代码，其下主题没有；SWEBOK 的主题有章节号，子主题没有；GB/T 13745 三级学科有代码。因此，它们都落在本库第 3 层。

```text
从知识体系复制  第 1 层  顶层概念    computing / library-and-information-science
               第 2 层             security / networking-and-communication / information-science …
               第 3 层             input-validation / transport-layer / 情报检索学 …
本地建立        第 4 层起           sql-injection / http / facet-analysis …
```

6. 复制的概念作为上位概念的下位集合原样保留，成员和顺序按来源，不拆、不改，也不为来源结构另配节点标签。
7. 复制的记录写实际来源的现行 `source`，并用现行 `match` 指回来源条目。`source` 记录实际派生，`match` 记录概念对应；来源改版后代码可能变化，两者不能互相替代。
8. 第 4 层起由本库按依据建立，深度不限；没有实际派生时不填 `source`。派生概念组只包含本库已有概念，不能暴露未建概念形成的盲区，因此不替代结构复制。

### 数组分组

9. 数组是可选结构。一个概念的下位默认是一个集合；只有需要区分几组时才登记数组。数组只对概念分组，不改变概念身份或层级关系。
10. 一个概念的下位来自多个现行结构来源时，每个来源的下位登记为一个数组，标识使用现行 `source`。例如，security 下 ASVS、CWE 和 ATT&CK 分别成组。
11. 可以对下位集合按划分特征分析，每个划分特征对应一个数组，标识使用 `characteristic`。划分特征属于零自定例外，目前尚未开放；开放后按[划分特征治理](drafts/division-characteristics.md)登记，并满足草案中的判据和完备划分要求。该草案仍未生效。
12. 一个概念在同一划分特征下只属于一组，在不同划分特征下可以分别属于一组（ISO 25964-1 数据模型 `isMemberOfArray 0..*`）。
13. 两个来源只有同时位于同一主题分支、覆盖重叠主题，并对这些主题提供同一种结构划分时，才构成结构来源冲突。同一视角只取一个来源，其他来源只作映射；条件不同时可以按来源分组或承担不同用途。具体来源对是否冲突须另行判断。

### 节点标签

14. 只有以划分特征为标识的数组写节点标签，显示为 `（按 X）`，其中 X 是名词。以来源为标识的数组显示来源名，那是数组标识，不是节点标签。分面名 `[X]` 的形式当前不使用。
15. 节点标签不是概念，不能用于标引，不能进入术语表，也不能成为 `broader` 的目标。需要说明分组位置时使用节点标签，不为该位置另建概念（Z39.19 §7.7）。

## 来源接口

正式 `vocab/topics.yaml` 当前继续使用旧形状：`source` 是用途记录 id；`match` 含 `source`、`id` 和 `rel`；来源数组的 `source` 也是用途记录 id。现行生成与校验在正式迁移前继续消费该形状。本文只收紧字段语义，不修改正式数据、id、层级、数组、来源选择或关系值。

共享严格接口已经实现。后置 `source` 含 `registry`、`item`、`locator` 和相邻 `basis`，只用于实际派生；后置 `match` 含 `registry`、`item`、`rel` 和相邻 `basis`，只用于概念映射。`registry` 分别要求经决定批准的 `structure` 或 `mapping` 角色。用途记录 v2、角色状态和逐条关系依据均未应用到正式数据，所以这些结构只是后置迁移边界。

反向索引可以定位当前旧引用和后置共享引用，但正式索引尚未生成，索引结果也不能决定实际派生或概念映射。六份迁移账本只保存历史库存、分类和阻断；当前 HEAD 已不能按原冻结哈希重放既有预演，不能把账本的推荐值写成现行关系。

## 结构来源

以下各节记录每个概念的下位当前从哪些来源复制。一个概念下有多个来源时，各来源的下位分别形成数组。当前没有分析层数组。id 使用正式数据已有的描述性 slug，来源代码只记在现行 `match`；本次不形成新 id 或来源关系。

### 顶层来源

| 概念 | 下位来源 | 借到 |
|---|---|---|
| （根） | 范围声明的八个本地顶层；各 `match` 到 GB/T 13745 一级学科 | 第 1 层 |
| computing | CS2023 的 17 个知识领域 | 第 2 层 |
| mathematics、information-and-systems-science、management、linguistics、journalism-and-communication、education | GB/T 13745 各自的二级学科 | 第 2 层 |
| library-and-information-science | GB/T 13745 二级学科 870.10―870.50 | 第 2 层 |

### 计算机分支

CS2023 的 17 个 Knowledge Area 作为第 2 层，每个 Knowledge Area 的知识单元作为第 3 层的第一个数组；另有现行结构来源时，再增加来源数组。

| 第 2 层 id | CS2023 | 知识单元数 | 其他来源数组 | 原分支 |
|---|---|---:|---|---|
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
| society-ethics-and-the-profession | SEP | 11 | — | 无；通用职业技能的另一个落点 |
| software-development-fundamentals | SDF | 5 | — | 无，新盲区 |
| software-engineering | SE | 9 | SWEBOK v4 18 章 | engineering |
| specialized-platform-development | SPD | 7 | — | web 降为其下的知识单元 Web Platforms |
| systems-fundamentals | SF | 9 | — | foundations 的一部分 |

知识单元数量来自 CS2023 正式版（2024-01），含每个 Knowledge Area 的 SEP 单元。

原 `web` 的处理保持不变：Web 在 CS2023 中只是 SPD 的一个知识单元，本库不另立第 2 层。MDN 技术参考的 19 个分区位于 Web Platforms 以下，超出结构复制深度，因此 MDN 当前只作映射来源，不复制。Web 相关本地概念从内容中形成，使用效果继续观察。

### 图书情报学科

| 第 2 层 | GB/T 13745 | 第 3 层来源 |
|---|---|---|
| library-science 图书馆学 | 870.10 | 三级学科 870.10xx，10 个 |
| documentation 文献学 | 870.20 | 三级学科 870.20xx，6 个 |
| information-science 情报学 | 870.30 | 三级学科 870.30xx，13 个 |
| archival-science 档案学 | 870.40 | 三级学科 870.40xx，4 个 |
| museology 博物馆学 | 870.50 | 无三级学科 |

原拟自加的“内容工程”取消：叙词表与检索语言归 870.3050 情报检索学，分类法归 870.1040 图书分类学，元数据与编目归 870.1045 图书编目学；术语学归顶层 linguistics 以下，结构化写作见[主题词表设计](topics.md)的邻近主题表。

### 其他学科来源

二级和三级学科清单见 [GB/T 13745 学科分类清单](../sources/gbt-13745.md)。

| 顶层 | GB/T 13745 | 二级学科 | 三级学科 |
|---|---|---:|---:|
| mathematics | 110 | 25 | 142 |
| information-and-systems-science | 120 | 7 | 18 |
| management | 630 | 12 | 43 |
| linguistics | 740 | 10 | 73 |
| journalism-and-communication | 860 | 7 | 30 |
| education | 880 | 18 | 0（标准原文无三级） |

术语学在 GB/T 13745 中没有对应学科，作为现行本地概念挂在 740.35 应用语言学以下。

## 结构预览

以下预览只说明当前结构，不作为生成输入，也不批准任何后置来源角色。

```text
（根）                                           ← 范围声明，本地建立
├─ mathematics 数学                             ← GB/T 110；25 个二级／142 个三级
├─ information-and-systems-science              ← GB/T 120；7／18
├─ computing 计算机科学技术                     ← GB/T 520
│   ├─ algorithmic-foundations                  ← CS2023 AL，5 个知识单元
│   ├─ architecture-and-organization            ← AR，11；硬件落这里
│   ├─ artificial-intelligence                  ← AI
│   │   [CS2023 AI 12 个知识单元]
│   │   [ATLAS]                                 ← 正式旧值；后置角色未批准
│   │   [OWASP LLM Top 10]                      ← 正式旧值；后置角色未批准
│   ├─ data-management                          ← DM，13
│   ├─ foundations-of-programming-languages     ← FPL
│   │   [CS2023 FPL 22 个知识单元]
│   ├─ graphics-and-interactive-techniques      ← GIT，12；新盲区
│   ├─ human-computer-interaction               ← HCI，6
│   ├─ mathematical-and-statistical-foundations ← MSF，5；与 mathematics 多层级
│   ├─ networking-and-communication             ← NC
│   │   [CS2023 NC 8 个知识单元]
│   │   [RFC 1122 四层]
│   ├─ operating-systems                        ← OS，14；新盲区
│   ├─ parallel-and-distributed-computing       ← PDC，5；新盲区
│   ├─ security                                 ← SEC
│   │   [CS2023 SEC 8 个知识单元]
│   │   [ASVS 5.0]
│   │   [CWE 顶层类别]
│   │   [ATT&CK 15 战术]
│   ├─ society-ethics-and-the-profession        ← SEP，11；职业技能落这里
│   ├─ software-development-fundamentals        ← SDF，5；新盲区
│   ├─ software-engineering                     ← SE
│   │   [CS2023 SE 9 个知识单元]
│   │   [SWEBOK v4 18 章]                       ← 项目管理落第 9 章
│   ├─ specialized-platform-development         ← SPD，7；Web Platforms 在其中
│   └─ systems-fundamentals                     ← SF，9
├─ management 管理学                            ← GB/T 630；12／43
├─ linguistics 语言学                           ← GB/T 740；10／73；术语学挂 740.35 以下
├─ journalism-and-communication                 ← GB/T 860；7／30
├─ library-and-information-science              ← GB/T 870
│   ├─ library-science 图书馆学                 ← 870.10xx，10
│   ├─ documentation 文献学                     ← 870.20xx，6
│   ├─ information-science 情报学               ← 870.30xx，13；情报检索学在其中
│   ├─ archival-science 档案学                  ← 870.40xx，4
│   └─ museology 博物馆学                       ← 无三级学科
└─ education 教育学                             ← GB/T 880；18 个二级，无三级

图例：箭头后是下位概念的来源和数量。方括号行是以来源为标识的数组，
      只在一个概念下存在多个来源时显示。当前没有分析层数组，
      第 3 层以下不预建。
```

## 重点分支

人工智能和编程语言分支补充说明现行结构来源与个体分工，不改变前述共同规则，也不形成新的来源角色或关系。

### 人工智能

CS2023 的 AI Knowledge Area 有 12 个知识单元：Introduction、Search、KRR、LRR、Probability、ML、NLP、Agents、Planning、Vision、Robotics、SEP。它偏学术，机器人和规划与本库侧重的 LLM 应用工程距离较远，但它是现行有稳定编号的人工智能结构来源。尚未用于标引的概念记录是盲区标记，不是负担。id 使用 `artificial-intelligence`；本库侧重体现在内容中，不改变来源体系边界。

LLM 应用相关外部体系继续按现行结构规则处理。ATLAS（2026.07 版，16 个战术，`AML.TA0000`―`AML.TA0015`）和 OWASP LLM Top 10（2025 版，`LLM01:2025`―`LLM10:2025`）分别保留为现行来源数组。NIST AI RMF 的四个功能是治理职能，不是知识划分，当前只作映射；Anthropic 文档随产品迭代，也只作映射。本次不重新判断这些选择。

### 编程语言

编程语言有跨语言的通识概念，例如类型系统、内存模型、求值与并发模型和范式；具体语言是个体，不进入主题树，收在[命名实体词表](entities.md)。`foundations-of-programming-languages`（CS2023 FPL）的下位继续是以下 22 个知识单元。

```text
foundations-of-programming-languages   现行 id 取自已有且有依据的英文 label，代码记在 match
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

这些 slug、英文原名、代码和 `unassigned` 状态均为现行值；22 个知识单元全部保留，预期多数会长期保持该状态。本次不选择新写法或改变数据。

语言特性的内容单元挂到通识概念，具体语言记在实体字段。例如，“Rust 的所有权”使用 `subject: [systems-execution-and-memory-model]` 和 `entities: [rust]`。按通识概念检索时，它与 GC 和引用计数并列；按语言检索时，由实体表计算结果。

## 待定事项

- Web 相关内容失去复制结构后是否够用，观察后决定是否在 Web Platforms 下破例复制 MDN。
- 多层级时 `broader` 列表的顺序暂不赋予含义；应用映射需要主上位时再定，并记录决定。
- 分析层数组何时启用，见[划分特征治理](drafts/division-characteristics.md)。
- 技术传播（技术写作、结构化写作）在树上没有节点，候选落点为 `communication-studies` 以下，依据 Wikidata Q1068718；暂缓，等 DITA 2.0 定稿并确定采用后再议（2026-08-23）。
