# 内容模型

知识库里一条内容单元抽象地有什么。本文形态无关：不提任何工具的字段名、文件格式或目录；那些在 `design/targets/` 各形态的映射里。字段取自 Dublin Core（ISO 15836），受控字段的值来自本库的词表。理论见[元数据](../concepts/metadata.md)。

## 内容单元

一条内容单元是知识库里最小的可独立引用、可独立打标签的东西。在 Obsidian 里是一篇笔记，在 DITA 里是一个 topic；本文只叫它“内容单元”。

## 字段

| 字段 | Dublin Core | 必填 | 值 |
|---|---|---|---|
| `identifier` | identifier | 是 | 按下文 id 规则，稳定不变 |
| `title` | title | 是 | 字面值 |
| `type` | type | 是 | [文档类型词表](#文档类型词表)的 id，恰好一个 |
| `subject` | subject | 是 | 主题词表的概念 id，一个或多个 |
| `entities` | 本库扩展，最近的 DCMI 属性是 `references` | 否 | 命名实体词表的 id，零个或多个 |
| `source` | source | 否 | 本单元派生自的内容单元或实体 id |
| `references` | references | 否 | 引用的文献、标准，实体 id |
| `created` | created | 是 | ISO 8601 日期 |
| `modified` | modified | 否 | ISO 8601 日期 |
| `status` | 本库扩展 | 是 | `draft` / `active` / `deprecated` |
| `isReplacedBy` | isReplacedBy | `deprecated` 时必填 | 替代它的内容单元 id |
| `language` | language | 否 | 默认 `zh`，与默认不同时填 |

不设 `description`：`title` 加 `subject` 已足够定位，正文本身就是说明。不设 `creator`、`publisher`、`rights`：单人库，值恒定，不记。

`entities` 是本库扩展：Dublin Core 没有“这篇内容涉及哪些具体产品”的字段，最近的是 `references`，但 `references` 的语义是“引用了”，而提到 Claude Code 不一定是引用它的文档。两个字段分开：`entities` 记涉及的实体，`references` 记引用的文献。

## 文档类型词表

`vocab/types.yaml`，`type` 字段的取值。一份术语表（Z39.19 的 list），取 Diátaxis 的四类：

| id | 首选词 | 读者来做什么 | 写法 |
|---|---|---|---|
| `tutorial` | 教程 | 学习，动手 | 带着做一遍，保证成功 |
| `how-to` | 操作指南 | 工作，动手 | 完成一个具体任务的步骤 |
| `reference` | 参考 | 工作，查阅 | 事实，克制，结构镜像对象 |
| `explanation` | 解释 | 学习，理解 | 为什么，讨论，多角度 |

DCMI Type Vocabulary 分的是媒介（Text、Image……），本库的内容单元都是 Text，不用它区分；体裁用 Diátaxis。以后需要第五类时先看能否归入四类，不能再加，加时登记来源。

## id 规则

全库三份词表和内容单元共用一套 id 规则。依据：ISO 25964-1 §2.25，标识符是在给定语境内唯一标识概念、词或其他实体的符号串；DCMI `identifier`，在给定语境内对资源的无歧义引用。

1. 小写 ASCII 字母、数字、连字符；不以连字符开头或结尾；不含其他字符
2. 从英文首选词取：`sql-injection`、`information-retrieval`。中文首选词没有通行英文名时，取 GB/T 或来源体系的英文名；都没有时用意译，不用拼音
3. 借入的概念不用来源的代码作 id（`FPL-Types` 不作 id），代码记在 `match`；id 从名称取，来源改版时代码变、id 不变
4. 一经引用不再改。名字错了，改 `label`，不改 id
5. 同名冲突加限定词后缀：`apple-company`、`apple-fruit`；限定词取自上位概念或类别
6. 长度不设上限，但不缩写：`networking-and-communication`，不写 `nc`
7. 四份表（主题、实体、类型、内容单元）各自唯一；跨表不要求唯一，引用时由字段决定查哪张表

## 与词表的关系

| 字段 | 词表 | 校验 |
|---|---|---|
| `type` | `vocab/types.yaml` | 值在表内 |
| `subject` | `vocab/topics.yaml` | 值在表内，且 `status` 不是 `deprecated`；引用 `unassigned` 的概念会把它转为 `active` |
| `entities`、`references`、`source` | `vocab/entities.yaml` 或内容单元 | 值在表内 |

内容单元对词表的引用是单向的：词表不记录哪些内容引用了它，需要时由脚本从内容反查。

## 生命周期

| status | 含义 | 进入 | 离开 |
|---|---|---|---|
| `draft` | 未完成 | 新建 | 完成 → `active` |
| `active` | 在用 | — | 被替代或过时 → `deprecated` |
| `deprecated` | 不再维护，保留 | 有替代或确认过时 | 不删 |

`deprecated` 的内容单元必有 `isReplacedBy`，指向替代它的单元；确认过时且无替代的，`isReplacedBy` 留空并在正文首段说明原因。与词表一致：不删，保留供检索。

## 形态映射的要求

每种执行形态一篇 `design/targets/<形态>.md`，固定回答：

1. 每个字段落到该形态的什么（属性名、位置）
2. 词表怎么导出到该形态（标签、枚举、subjectScheme……）
3. `subject`、`entities` 的引用在该形态里怎么表达（链接、标签）
4. 回流：从该形态抽候选词、统计引用次数怎么做
5. 该形态做不到的字段或约束，如何处理

映射不得改动本文的字段定义；本文不提任何形态的细节。

## 待定事项

- `status` 的 `draft` 是否需要：单人库可能直接写成 `active`
- 内容单元之间除 `source`、`isReplacedBy`、`references` 外是否需要 `relation`（泛关联）
- 是否收 `person` 实体：Wikidata Q5；只收公开人物（作者、维护者），不收私人
