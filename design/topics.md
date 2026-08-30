# 主题词表设计

`vocab/topics.yaml` 是本库的主题叙词表。它由概念记录、记录中的词法标签、概念之间的层级与相关关系，以及概念到外部词表的映射构成，用于给内容单元标引主题、检索和生成导航。知识图谱和导航是它的用法或升级方向，不是词表本身。

本文规定词表范围、概念记录、关系、映射、生命周期、建设流程和校验。树的结构见[层级结构](hierarchy.md)，外部来源登记见[来源名称规范表](sources-registry.md)。理论依据见[受控词表](../concepts/controlled-vocabulary.md)和[词表的建设与维护](../concepts/vocabulary-construction.md)。

## 词表总览

主题词表按概念、标签、概念关系和外部映射四层表达信息。

```text
                          vocab/topics.yaml
 ┌──────────────────────────────────────────────────────────────────┐
 │                                                                  │
 │  概念记录                                                        │
 │     id:    sql-injection        ← 稳定引用，名称变化时不改        │
 │     label: SQL 注入 / SQL injection  ← 首选标签                  │
 │     alt:   SQLi                 ← 同一概念的替代标签              │
 │     scope: 用于……不用于……       ← 范围注释                       │
 │                                                                  │
 │  词法控制                                                        │
 │     SQLi  USE  SQL injection    ← 在同一概念记录内用 alt 表示    │
 │                                                                  │
 │  概念关系                                                        │
 │     层级  security                                               │
 │             └─ input-validation                                 │
 │                  └─ sql-injection      ← broader 字段            │
 │     相关  sql-injection ◀────▶ parameterized-query              │
 │                                      ← related 字段              │
 │                                                                  │
 │  外部映射                                                        │
 │     sql-injection ──exactMatch──▶ CWE-89                         │
 │     sql-injection ──broadMatch──▶ A03:2021                       │
 │                         source 必须在 vocab/sources.yaml 中登记   │
 └──────────────────────────────────────────────────────────────────┘

 叙词表 ──渲染成目录──▶ 导航       概念和关系不变，只改变呈现
   │
   └──增加带类型的边──▶ 知识图谱   复用概念节点，增加关系类型
```

`label`、`alt` 和 `hidden` 都附着于同一概念记录；USE／UF 说明同一概念的等价入口，不建立两个概念。`broader` 和 `related` 连接概念。界面都显示文字，不改变两类关系的主体。

## 范围与用途

本节规定现有覆盖、邻近主题、排除项和使用目的；未获决定的生活主题边界继续保持待定。

### 覆盖范围

顶层概念由范围决定，不从其他体系复制。现有顶层取 GB/T 13745-2009 的八个一级学科，并分别 `match` 到来源代码。以下 id、中文 `label` 和代码保持不变。

| id | 中文 label | GB/T 13745 |
|---|---|---|
| `mathematics` | 数学 | 110 |
| `information-and-systems-science` | 信息科学与系统科学 | 120 |
| `computing` | 计算机科学技术 | 520 |
| `management` | 管理学 | 630 |
| `linguistics` | 语言学 | 740 |
| `journalism-and-communication` | 新闻学与传播学 | 860 |
| `library-and-information-science` | 图书馆、情报与文献学 | 870 |
| `education` | 教育学 | 880 |

顶层以下按[层级结构](hierarchy.md)的结构复制规则全部借入：`computing` 使用 CS2023 的 17 个 Knowledge Area，其余七个顶层使用 GB/T 13745 的二级和三级学科。

### 邻近主题的处理

原先作为邻近主题降级处理的内容中，数学、管理学和语言学已经升为顶层。其余内容保留以下落点和依据。

| 主题 | 落点 | 依据 |
|---|---|---|
| 硬件、体系结构 | `computing` › `architecture-and-organization` | CS2023 AR |
| 项目管理 | `software-engineering` 下 SWEBOK 第 9 章“软件工程管理”，同时在 `management` 以下；多层级 | SWEBOK v4；GB/T 13745 630 |
| 通用职业技能（写作、沟通、时间管理） | `computing` › `society-ethics-and-the-profession`；写作另可挂在 `journalism-and-communication` 以下 | CS2023 SEP |
| 术语学（ISO 704、1087、30042） | `linguistics` › 740.35 应用语言学以下，作为本地概念 | GB/T 13745 740.35 |
| Web 开发 | `specialized-platform-development` › Web Platforms；MDN 只作映射 | CS2023 SPD |
| 结构化写作（DITA） | `journalism-and-communication` 以下；DITA 标准作为实体，`subjects` 指向同一处 | GB/T 13745 860；技术写作属传播 |

### 排除范围

以下主题不建概念记录，相关内容不进入知识库。

| 主题 | 说明 |
|---|---|
| 自然语言学习 | 英语、日语等语言学习内容 |
| 课程和书的阅读进度 | 属于个人任务管理，不是知识 |

非技术的生活领域（健康、理财、旅行）尚未决定，见待定事项。

### 用途

主题词表用于给内容单元标引主题、检索和生成导航。它由一人使用，以中文为主，并为有依据的英文标签提供检索入口；不要求多语种对等或印刷版式。

## 文件布局

`vocab/topics.yaml` 保持单文件。起步约 650 个概念、8000 行，对 grep 和 Git 不是负担。第 2 层不用于拆分文件：多层级概念可以同时位于不同主题分支，文件边界不能与树结构一一对应。概念达到几千个后，再考虑按顶层拆分。

## 概念记录的字段

概念记录使用以下结构；本批不增加、删除或改名字段。

```yaml
- id: sql-injection                      # 稳定、小写、连字符；一经引用不改
  label: { zh: SQL 注入, en: SQL injection }
  basis: { zh: wikidata:Q506059, en: cwe:CWE-89 }   # label 的形式依据，见治理“译名”
  alt: [SQLi]                            # 替代 label；可检索、可显示
  hidden: []                             # 隐藏 label；可检索、不显示
  broader: [input-validation, data]      # 空列表表示顶层概念
  arrays: [security-asvs]                # 所属数组；上位只有一个来源时可省略
  related: []                            # 必须互反；仅在不同上位且内容常同时涉及两概念时添加
  scope: >                               # 范围注释：用于……不用于……
    指通过拼接用户输入改变 SQL 语义的攻击及对应缺陷；
    参数化查询等防御手段不在此。
  source: self                           # 复制概念记录来源；本地建立为 self
  origin: []                             # 本地概念的源头文献：实体表中的 publication 或 standard id
  match:                                 # 到外部词表概念的映射
    - { source: cwe, id: CWE-89, rel: exactMatch }
    - { source: owasp-top10, id: "A03:2021", rel: broadMatch }
  status: active                         # 概念记录的生命周期状态
  added: 2026-08-20
  history: []                            # 日期、变更内容和理由
```

必填字段是 `id`、`label.zh`、`broader`、`status`、`added`、`basis.zh` 和 `basis.en`。`label.en` 按译名阶梯取得；没有依据时不填，并写 `basis.en: none`。其余字段按需使用。本地概念强烈建议填写 `scope`，以明确适用和不适用的边界。

`basis` 中的语言项记录 `label` 的形式依据。它只回答该表示形式能否被项目采用，不能代替其他字段值或关系的断言依据；人工赋值的具体断言仍按[维护](maintenance.md)的断言规则记录依据。本批不改变字段结构。

`origin` 记录本地概念最早在哪篇文献中提出或定型。例如：

```yaml
- id: hexagonal-architecture
  broader: [software-design]
  origin: [cockburn-2005-hexagonal]      # 实体表中的 publication，tier 为 archival
  source: self
```

`origin` 消费 Z39.19 §11.1.4 所列的来源信息，但来源标准中的记录名称只是来源陈述，不自动成为本项目采用的名称。`origin` 也不是 `match`：前者指向源头文献，后者指向外部词表条目。按 `origin` 反查，可以区分概念来自标准、论文还是博文。

字段与标准的对应关系保持不变：`alt`／`hidden` 对应 SKOS `altLabel`／`hiddenLabel`；`broader`、`related` 对应 SKOS 同名属性；`arrays` 对应 ISO 25964-1 数据模型的 ThesaurusArray；`scope` 对应范围注释；`history` 对应历史注释；`status` 对应数据模型的 `status`。`origin` 取 Z39.19 §11.1.4 的 source 信息作为依据，`match` 则保存跨词表概念映射。

数组在文件顶部单独登记，对应 ISO 25964-1 数据模型的 ThesaurusArray 与 NodeLabel。数组至少使用 `source` 或 `characteristic` 之一作为标识；`characteristic` 还须在 `characteristics.yaml` 登记。

```yaml
arrays:
  - id: security-asvs
    superordinate: security             # 数组所属的上位概念
    source: asvs                        # 以来源为标识
  - id: pl-by-paradigm                  # 分析层示例，当前没有
    superordinate: programming-languages
    characteristic: paradigm            # 以划分特征为标识，显示为节点标签（按范式）
```

一个概念的下位只有一个来源且未做分析时，不登记数组。规则见[层级结构](hierarchy.md)。分面字段暂不设置，见[分面字段草案](drafts/facet-field.md)；草案仍未生效。

## 生命周期

`status` 只表示概念记录状态，不给单个字符串或标签建立独立生命周期。

| status | 来源 | 含义 | 进入 | 离开 |
|---|---|---|---|---|
| `unassigned` | Z39.19 §11.1.8 | 为补全层级而收入、尚未用于内容标引的概念记录 | 复制知识体系层级时 | 达到既有阈值后转为 `active` |
| `candidate` | Z39.19 §11.1.6 | 已完成概念判断和初步依据核验、尚未完成接受程序的概念记录 | 需要建立本地概念时 | 达到既有阈值且通过审核后转为 `active`；长期无引用时可以取得删除资格 |
| `active` | — | 在用的概念记录 | 审核通过 | 被替代后转为 `deprecated` |
| `deprecated` | Z39.19 §11.3.2.1 | 不再用于新标引、为检索和历史保留的概念记录 | 合并、拆分或替代时 | 不删；必须有 `replaced_by` 和 `history` |

`deprecated` 概念记录保留，必要的旧表示形式随记录保留，以维持既有检索、替代关系和历史追踪。只有满足既定门禁的 `candidate` 概念记录可以取得删除资格；资格不等于批准，实际删除仍按治理权限执行。`unassigned`、`active`、`deprecated` 和单个表示形式都不继承该资格。

复制的概念可以长期保持 `unassigned`，因为它们用于显示盲区。确认不需要时在 `scope` 中说明有意不覆盖及理由，仍保留记录。

## 建设流程

1. 写明“范围与用途”的排除项。
2. 逐个核对各数组来源的当前版本和条目，并登记到 `sources.yaml`。
3. 按[层级结构](hierarchy.md)的来源表复制第 3 层，记录全部使用 `unassigned`，填写 `source`，并用 `match` 指回来源条目。
4. 把现有约 90 个概念挂到树上：来源已有的第 3 层概念并入复制结构；本地概念先建立 `candidate` 记录。
5. 自下而上校正时，从现有内容、书签和文献识别带来源上下文的字符串或名词短语，先与已登记的 `label`、`alt` 和 `hidden` 匹配。匹配后按概念 id 与树比较；未解析项只交人工判断，不自动建立概念或关系。
6. 分批补充 `scope` 和 `match`，逐个第 2 层概念处理，不要求一次完成。

第 3 步由脚本辅助生成初版，结果须经人工审核。

## 校验规则

每次修改 `vocab/topics.yaml` 后运行 `scripts/check-topics.py`，检查以下规则。

- 所有 `broader` 指向存在的 id，且不存在环。
- `source` 和 `match.source` 在 `sources.yaml` 中。
- `deprecated` 必有 `replaced_by`。
- `arrays` 指向存在的数组，且数组的 `superordinate` 位于本概念的 `broader` 中。
- 数组至少有 `source` 或 `characteristic`；`characteristic` 在 `characteristics.yaml` 中。分析层数组的成员位于上位概念的下位集合内，同一划分特征下每个下位概念至多属于一组。
- `source` 不是 `self` 的概念记录有一条 `match` 指向同一来源。
- `origin` 指向实体表中 `kind` 为 `publication` 或 `standard` 的实体。
- `label.en` 和 `alt` 在全表内不重复；重复可能表示同一概念被建立两次。
- 统计每个第 2 层概念下 `unassigned` 的比例，以及 `candidate` 概念记录的引用次数。

术语检查脚本的命中只作为候选识别结果，不把扫描命中直接裁定为违规；脚本行为由后续实现批次处理。

## 设计分工

| 事项 | 文档 | 关系 |
|---|---|---|
| 树的分层、划分和复制来源 | [层级结构](hierarchy.md) | 本文的 `broader`、`arrays`、`source` 按其规则填写 |
| 外部体系登记、复制、映射和派生组 | [来源名称规范表](sources-registry.md) | `source`、`match.source` 只使用已登记 id |
| 分面字段 | [分面字段草案](drafts/facet-field.md) | 草案未生效；本文不设置该字段 |
| 手工概念组 | [概念组草案](drafts/concept-groups.md) | 草案未生效；派生组可以从映射计算 |
| 导航 | — | 渲染主题树得到导航，树不依赖界面 |
| 知识图谱 | [概念文](../concepts/knowledge-graph.md) | 当前概念关系只有 `broader` 和 `related`；增加带类型的关系时复用概念节点 |
| 软件产品、语言、组织 | [命名实体词表](entities.md) | 个体不进入主题树，通过 `subjects` 挂到主题概念 |
| 文档类型、人名 | — | 分别属于独立词表，有内容后按需建立 |

## 待定事项

- 生活领域（健康、理财、旅行等）要记，按范围声明加顶层：健康对应 GB/T 13745 医学门类（310–360），理财对应 790 经济学；具体哪些顶层待列
- 分面字段，见[草案](drafts/facet-field.md)。
- 大语言模型作为本地概念挂在 `artificial-intelligence` 的哪个知识单元下（NLP 或 ML），以及术语的 `origin`。
