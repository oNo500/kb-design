# 命名实体词表设计

`vocab/entities.yaml` 是本库的第二份词表：一份名称规范表（name authority list），收软件产品、编程语言、组织、标准、文献这类**个体**。主题词表管类（“AI 编程助手”“关系型数据库”“六边形架构”），本表管个体（Claude Code、PostgreSQL、Anthropic、ISO 25964-1:2011、Cockburn 2005 年那篇博文）。

依据：ISO 25964-2 §23，名称规范表是“为一致地命名特定实体的受控词表”，实体是唯一的个体而不是类，不与主题概念做等价映射。理论见[受控词表](../concepts/controlled-vocabulary.md)、[词表映射](../concepts/vocabulary-mapping.md)。

## 为什么分开

| | 主题词表 | 命名实体词表 |
|---|---|---|
| 收什么 | 类：领域、概念 | 个体：产品、语言、组织、标准、文献 |
| 变化速度 | 几年一版 | 产品一年出十几个，死一半 |
| 结构 | 层级树 | 扁平；实体之间只有“属于哪个组织”一类关系 |
| 权威来源 | 知识体系、标准 | 厂商文档（vendor 档）、Wikidata |
| 与另一方的关系 | — | 每个实体通过 `subjects` 挂到一个或多个主题概念，不占树的位置 |

混在一棵树里，稳定的部分会被易变的部分拖着动；一个产品横跨多个主题（Claude Code 是 AI 工具也是软件工程工具）也无处安放。

## 记录

```yaml
- id: claude-code                        # 稳定、小写、连字符
  label: { zh: Claude Code, en: Claude Code }
  alt: [claude code cli]
  kind: software                         # 见下
  vendor: anthropic                      # 指向本表另一条实体,可省略
  subjects: [artificial-intelligence, software-engineering]   # 主题词表里的概念 id,至少一个
  scope: >
    Anthropic 的命令行编程助手;不含 Claude 模型本身(另一条实体)。
  match:
    - { source: wikidata, id: Q138457287, rel: exactMatch }
  status: active
  added: 2026-08-23
  history: []
```

必填：`id` `label` `kind` `subjects` `status` `added`。

### 类别

`kind` 取 Wikidata 的类，不自定：

| kind | Wikidata | 例 |
|---|---|---|
| `software` | Q7397 software | Claude Code、PostgreSQL、Neo4j |
| `programming-language` | Q9143 programming language | Python、Rust、TypeScript |
| `organization` | Q43229 organization | Anthropic、MITRE、W3C |
| `standard` | Q317623 technical standard | ISO 25964-1:2011、RFC 9110、ASVS 5.0、Anthropic 文档 |
| `publication` | Q591041 scientific publication 及其下位：Q13442814 scholarly article、Q571 book、Q17928402 blog post;issue、演讲的类待核 | Hogan 2021、Aitchison 的教材、Cockburn 2005 的博文 |

需要更多类别时从 Wikidata 取，记录其 Q 号。`publication` 的具体形式记在 `form` 字段，值是 Wikidata 的 Q 号或其 slug。

### 分级

`tier` 对 `standard` 和 `publication` 必填，其余类别不填。分档依据是来源如何变更——权威程度决定能不能引，变更方式决定多久要回头看；分档本身的依据是本库获取与信任知识的方式，按 Z39.19 §5.3.5.2 属于组织依据。复核周期、链接检查、新版探测见[来源复核](review.md)。

| tier | 含义 | 适用 |
|---|---|---|
| `de-jure` | 有正式发布流程和版本标识，变更必出新版 | ISO、GB/T、W3C Recommendation、RFC |
| `de-facto` | 行业默认，无发布流程，或版本可无通知漂移 | CS2023、SWEBOK、ASVS、CWE、MDN、W3C 草案 |
| `vendor` | 单一厂商文档，随产品迭代 | Anthropic 文档、Neo4j 文档 |
| `archival` | 发表后内容固定 | 论文、书、博文、issue、演讲 |

同一发布方可能跨档：W3C 的 Recommendation 是 de-jure,Working Draft 是 de-facto;Wikidata 的数据是 de-facto，引用它的论文是 archival。

`standard` 类的实体另有三个字段：`version`（引的是哪一版，如 `ISO 25964-1:2011`、`ASVS 5.0`）、`checked`（上次核对日期）、`watch`(de-jure 必填，探测新版的页面)。

前沿概念的权威来源常常是一篇固定的文本——一篇博文、一篇论文、一个 issue——而不是任何会更新的规范：六边形架构来自 Cockburn 2005 年的博文，洋葱架构来自 Palermo 2008 年的博文，Transformer 来自 Vaswani 等 2017 年的论文。它们都是 `publication` + `archival`，权威性来自被引用和被采纳。主题词表里的本地概念通过 `origin` 字段指向它的源头文献，见[主题词表设计](topics.md)。

### 生命周期

与主题词表相同：`candidate` / `active` / `deprecated`，规则见[主题词表设计](topics.md)。没有 `unassigned`——本表不借入任何结构，每条都是按依据（用到了、读到了）本地建立的。

产品停止维护或被替代时转 `deprecated`,`replaced_by` 指向替代品（如有），不删。

## 映射

`match` 的来源只能是[来源名称规范表](sources-registry.md)登记的。实体的主要映射目标是 Wikidata：它对软件、语言、组织、标准、出版物都有条目和稳定 Q 号，且自身记录了厂商、发布日期、官网、DOI 等属性，本表不重复记。厂商文档只作 `url`，不作映射目标。

## 与来源名称规范表的分工

作为词表来源使用的标准和知识体系（CS2023、ASVS、GB/T 13745……）同时是本表的实体。两处不重复登记：本表记它是什么（名称、类别、分级、版本、URL、映射）；[来源名称规范表](sources-registry.md)只记它作为词表来源怎么用（`role`、借入位置），并以 `entity` 字段指向本表。

## 与主题词表的分工

- 内容单元的 `subject` 字段填主题概念，`entities` 字段填实体，见[内容模型](content-model.md)
- “Rust 的所有权”：`subject: [systems-execution-and-memory-model]`，`entities: [rust]`。主题树里不再有“具体语言”数组
- 一个实体的 `subjects` 可以多个；主题概念不反向记录实体，需要时由脚本从实体表算出“某主题下的全部实体”
- “全库所有标准”“全库所有文献”= 本表按 `kind` 的查询，不需要主题词表的分面字段
- 本地概念的源头文献通过概念的 `origin` 指向本表

## 建设流程

1. 从现有笔记、书签、已装工具里列出实际用到的产品、语言、组织——文献依据
2. 逐条查 Wikidata，有条目的记 Q 号；没有的 `match` 留空，`candidate`
3. 填 `subjects`；填不出的说明主题树缺概念，回到主题词表补

## 校验规则

- `subjects` 指向主题词表里存在的概念
- `vendor`、`replaced_by` 指向本表存在的实体
- `kind` 在类别表内
- `label.en` 和 `alt` 全表内不重复
- `deprecated` 必有 `history`

## 待定事项

- 类别是否需要更细（工具 vs 框架 vs 服务），以及从 Wikidata 取哪些类
- 模型（Claude、GPT）算 `software` 还是另立类别
- `publication` 中 issue、演讲对应的 Wikidata 类
- 实体之间是否需要 `vendor` 以外的关系（依赖、兼容）——那是知识图谱的事，见[概念文](../concepts/knowledge-graph.md)
