# 命名实体词表设计

`vocab/entities.yaml` 是本库的名称规范表（name authority list），收软件产品、编程语言、组织、标准和文献等个体。主题词表管理概念，例如“AI 编程助手”“关系型数据库”和“六边形架构”；命名实体词表管理个体，例如 Claude Code、PostgreSQL、Anthropic、ISO 25964-1:2011 和 Cockburn 2005 年的博文。

ISO 25964-2 §23 把名称规范表定义为为一致命名特定实体而建立的受控词表；实体是唯一的个体，不与主题概念建立等价映射。理论见[受控词表](../concepts/controlled-vocabulary.md)和[词表映射](../concepts/vocabulary-mapping.md)。

## 对象分工

主题词表和命名实体词表分别管理概念与个体，不另设数据类别。

| 比较项 | 主题词表 | 命名实体词表 |
|---|---|---|
| 管理对象 | 概念 | 个体：产品、语言、组织、标准、文献 |
| 变化速度 | 几年一版 | 产品一年可发布多个版本，也可能停止维护 |
| 结构 | 层级树 | 扁平；实体之间只保留已定义的关系 |
| 权威来源 | 知识体系、标准 | 厂商文档（vendor 档）、Wikidata |
| 相互关系 | 不记录实体 | 每个实体通过 `subjects` 挂到一个或多个主题概念，不占树的位置 |

概念与个体混在一棵树中，会让稳定结构随易变对象移动。一个产品还可能关联多个主题；例如，Claude Code 同时关联人工智能和软件工程相关概念，`subjects` 的多值关系可以表达这种挂接。

## 记录

实体记录使用以下结构；本批不增加或改名字段。

```yaml
- id: claude-code                        # 稳定、小写、连字符
  label: { zh: Claude Code, en: Claude Code }
  alt: [claude code cli]
  kind: software                         # 见下
  vendor: anthropic                      # 指向本表另一条实体，可省略
  subjects: [artificial-intelligence, software-engineering]   # 主题概念 id，至少一个
  scope: >
    Anthropic 的命令行编程助手；不含 Claude 模型本身（另一条实体）。
  match:
    - { source: wikidata, id: Q138457287, rel: exactMatch }
  status: active
  added: 2026-08-23
  history: []
```

必填字段是 `id`、`label`、`kind`、`subjects`、`status` 和 `added`。人工赋值字段按[维护](maintenance.md)的断言规则记录 `basis`；含 `self` 的记录保持 `candidate`。

### 类别

`kind` 只取已登记的 Wikidata 类，不自定。

| kind | Wikidata | 例 |
|---|---|---|
| `software` | Q7397 software | Claude Code、PostgreSQL、Neo4j |
| `programming-language` | Q9143 programming language | Python、Rust、TypeScript |
| `organization` | Q43229 organization | Anthropic、MITRE、W3C |
| `standard` | Q317623 technical standard | ISO 25964-1:2011、RFC 9110、ASVS 5.0、Anthropic 文档 |
| `publication` | Q591041 scientific publication 及其下位：Q13442814 scholarly article、Q571 book、Q17928402 blog post；issue、演讲的类待核 | Hogan 2021、Aitchison 的教材、Cockburn 2005 年的博文 |
| `person` | Q5 human | Ranganathan、Wüster、Hogan、Cockburn |
| `large-language-model` | Q115305900 large language model | Claude Opus 4、GPT-4 |

需要更多类别时从 Wikidata 取，并记录 Q 号。`publication` 的具体形式记在 `form` 字段，值是 Wikidata Q 号或其 slug。

`person` 只收在相关主题或活动中有显著公开角色的公众人物（public figure，*Gertz v. Robert Welch* 1974 的意义）：已发表作品的作者、公开项目的维护者或方法的提出者，并且有 Wikidata 条目或可引用的公开出处。相关主题或活动只限定公开角色的判断范围，不形成新的数据类别。不收私人、同事或联系人。文献实体用 `creator` 指向人，软件实体的个人维护者用 `vendor` 指向人。

### 分级

`tier` 对 `standard` 和 `publication` 必填，其余类别不填。分级依据来源如何变更：权威程度决定能否引用，变更方式决定复核周期；按 Z39.19 §5.3.5.2，这属于组织依据。复核周期、链接检查和新版探测见[维护](maintenance.md)。

| tier | 含义 | 适用 |
|---|---|---|
| `de-jure` | 有正式发布流程和版本标识，变更必出新版 | ISO、GB/T、W3C Recommendation、RFC |
| `de-facto` | 行业默认，无发布流程，或版本可无通知漂移 | CS2023、SWEBOK、ASVS、CWE、MDN、W3C 草案 |
| `vendor` | 单一厂商文档，随产品迭代 | Anthropic 文档、Neo4j 文档 |
| `archival` | 发表后内容固定 | 论文、书、博文、issue、演讲 |

同一发布方可以跨档：W3C Recommendation 是 `de-jure`，Working Draft 是 `de-facto`；Wikidata 数据是 `de-facto`，引用它的论文是 `archival`。本批不改变任何来源档级。

`publication` 实体另有 `creator` 字段，值是 `person` 或 `organization` 实体的 id，可以有多个。

`standard` 实体另有三个字段：`version` 记录所引版本，例如 `ISO 25964-1:2011`、`ASVS 5.0`；`checked` 记录上次核对日期；`watch` 对 `de-jure` 必填，指向新版探测页面。

前沿概念的权威来源常是一篇内容固定的博文、论文或 issue，而不是持续更新的规范。六边形架构来自 Cockburn 2005 年的博文，洋葱架构来自 Palermo 2008 年的博文，Transformer 来自 Vaswani 等人 2017 年的论文。它们都是 `publication` 加 `archival`，权威性来自被引用和采纳。主题词表中的本地概念通过 `origin` 指向源头文献，见[主题词表设计](topics.md)。

### 生命周期

实体记录使用 `candidate`、`active` 和 `deprecated`，规则见[主题词表设计](topics.md)。本表没有 `unassigned`：它不复制结构，每条记录都按实际使用或阅读依据在本地建立。

产品停止维护或被替代时转为 `deprecated`，`replaced_by` 在有替代品时指向替代实体；记录不删。

## 映射

`match` 的来源只能是[来源名称规范表](sources-registry.md)已登记的来源。实体的主要映射目标是 Wikidata：它为软件、语言、组织、标准和出版物提供稳定 Q 号，并记录厂商、发布日期、官网和 DOI 等属性，本表不重复保存。厂商文档只作为 `url`，不作为映射目标。

## 来源职责

作为词表来源使用的标准和知识体系，例如 CS2023、ASVS 和 GB/T 13745，同时也是本表中的实体。两处不重复登记：本表记录其名称、类别、分级、版本、URL 和映射；[来源名称规范表](sources-registry.md)只记录它作为词表来源的 `role` 和复制位置，并以 `entity` 指向本表。

## 主题职责

- 内容单元的 `subject` 填主题概念，`entities` 填实体，见[内容模型](content-model.md)。
- “Rust 的所有权”使用 `subject: [systems-execution-and-memory-model]` 和 `entities: [rust]`；具体语言不进入主题树。
- 一个实体的 `subjects` 可以有多个；主题概念不反向记录实体，需要时由脚本计算某主题下的全部实体。
- 全库标准或全库文献由本表按 `kind` 查询，不需要主题词表的分面字段。
- 本地概念的源头文献通过概念记录的 `origin` 指向本表。

## 建设流程

1. 从现有笔记、书签和已装工具中列出实际使用的产品、语言和组织，并保留文献依据。
2. 逐条核对 Wikidata；有条目的记录 Q 号，没有的将 `match` 留空并保持 `candidate`。
3. 填写 `subjects`；无法挂接时回到主题词表判断是否缺少概念。

## 校验规则

- `subjects` 指向主题词表中存在的概念。
- `vendor`、`replaced_by` 指向本表中存在的实体。
- `kind` 在类别表内。
- `label.en` 和 `alt` 在全表内不重复。
- `deprecated` 必有 `history`。

## 待定事项

- 类别是否需要更细，例如工具、框架和服务，以及应取哪些 Wikidata 类。
- `publication` 中 issue 和演讲对应的 Wikidata 类。
- 实体之间是否需要 `vendor` 以外的关系，例如依赖和兼容；这属于知识图谱问题，见[概念文](../concepts/knowledge-graph.md)。
