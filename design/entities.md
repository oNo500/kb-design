# 命名实体词表设计

`vocab/entities.yaml` 是本库的第二份词表:一份名称规范表(name authority list),收软件产品、工具、编程语言、组织这类**个体**。主题词表管类(「AI 编程助手」「关系型数据库」),本表管个体(Claude Code、PostgreSQL、Anthropic)。

依据:ISO 25964-2 §23,名称规范表是「为一致地命名特定实体的受控词表」,实体是唯一的个体而不是类,不与主题概念做等价映射。理论见[受控词表](../concepts/controlled-vocabulary.md)、[词表映射](../concepts/vocabulary-mapping.md)。

## 为什么分开

| | 主题词表 | 命名实体词表 |
|---|---|---|
| 收什么 | 类:领域、概念 | 个体:产品、语言、组织 |
| 变化速度 | 几年一版 | 产品一年出十几个,死一半 |
| 结构 | 层级树 | 扁平;实体之间只有「属于哪个组织」一类关系 |
| 权威来源 | 知识体系、标准 | 厂商文档(vendor 档)、Wikidata |
| 与另一方的关系 | — | 每个实体通过 `subjects` 挂到一个或多个主题概念,不占树的位置 |

混在一棵树里,稳定的部分会被易变的部分拖着动;一个产品横跨多个主题(Claude Code 是 AI 工具也是软件工程工具)也无处安放。

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

必填:`id` `label` `kind` `subjects` `status` `added`。

### 类别 `kind`

实体的类别取 Wikidata 的类,不自定:

| kind | Wikidata | 例 |
|---|---|---|
| `software` | Q7397 software | Claude Code、PostgreSQL、Neo4j |
| `programming-language` | Q9143 programming language | Python、Rust、TypeScript |
| `organization` | Q43229 organization | Anthropic、MITRE、W3C |

需要更多类别时从 Wikidata 取,记录其 Q 号。

### 生命周期

与主题词表相同:`candidate` / `active` / `deprecated`,规则见[主题词表设计](topics.md)。没有 `unassigned`——本表不借入任何结构,每条都是按依据(用到了、读到了)本地建立的。

产品停止维护或被替代时转 `deprecated`,`replaced_by` 指向替代品(如有),不删。

## 映射

`match` 的来源只能是[来源名称规范表](sources-registry.md)登记的。实体的主要映射目标是 Wikidata:它对软件、语言、组织都有条目和稳定 Q 号,且自身记录了厂商、发布日期、官网等属性,本表不重复记。厂商文档只作 `url`,不作映射目标。

## 与主题词表的分工

- 笔记的 frontmatter 两个字段:`topics:` 填主题概念,`entities:` 填实体
- 「Rust 的所有权」:`topics: [systems-execution-and-memory]`,`entities: [rust]`。主题树里不再有「具体语言」数组
- 一个实体的 `subjects` 可以多个;主题概念不反向记录实体,需要时由脚本从实体表算出「某主题下的全部实体」

## 建设流程

1. 从现有笔记、书签、已装工具里列出实际用到的产品、语言、组织——文献依据
2. 逐条查 Wikidata,有条目的记 Q 号;没有的 `match` 留空,`candidate`
3. 填 `subjects`;填不出的说明主题树缺概念,回到主题词表补

## 校验规则

- `subjects` 指向主题词表里存在的概念
- `vendor`、`replaced_by` 指向本表存在的实体
- `kind` 在类别表内
- `label.en` 和 `alt` 全表内不重复
- `deprecated` 必有 `history`

## 待定事项

- 类别是否需要更细(工具 vs 框架 vs 服务),以及从 Wikidata 取哪些类
- 模型(Claude、GPT)算 `software` 还是另立类别
- 实体之间是否需要 `vendor` 以外的关系(依赖、兼容)——那是知识图谱的事,见[概念文](../concepts/knowledge-graph.md)
