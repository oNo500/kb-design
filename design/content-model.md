# 内容模型

知识库的内容模型定义一条内容单元具有哪些字段、受控值和约束。本文与应用无关：不提工具字段名、文件格式或目录；应用落地分别写在 `design/targets/` 中。字段取自 Dublin Core（ISO 15836），受控字段的值来自本库现行词表。理论见[元数据](../concepts/metadata.md)。

来源与术语的新模式、校验、生成和诊断接口已经实现，但尚未接管正式数据。本文继续规定现行内容字段、值域、标识符、生命周期和应用映射；不新增术语字段，不把候选术语身份写入内容，不改变任何现行值。

## 内容单元

内容单元是知识库中可独立引用、可独立标引的最小单位：有标题，只讲一个主题。DITA 1.3 §2.2.1 把 topic 规定为写作与复用的基本单位，包含标题和可选正文，每个 topic 只含一个主题；本文对该定义作与应用无关的转述。在 Obsidian 中可以是一篇笔记，在 DITA 中是一个 topic。本文统一称为“内容单元”。

术语迁移账本和正文诊断不改变这个定义。账本只保存冻结审查与消费者去向，诊断只产生 `report-only` 人工复核线索；两者都不修改内容单元、字段或受控值。

## 字段

内容单元使用以下现行字段。

| 字段 | Dublin Core | 必填 | 值 |
|---|---|---|---|
| `identifier` | identifier | 是 | 按下文标识符规则，稳定不变 |
| `title` | title | 是 | 字面值 |
| `type` | type | 是 | 文档类型：[文档类型词表](#文档类型词表)的概念 id，恰好一个 |
| `genre` | 本库扩展，依据 IPTC genre | 是 | 作者立场：[体裁词表](#体裁词表)的概念 id，恰好一个 |
| `form` | 本库扩展，依据 IEEE LOM | 否 | 载体：[载体词表](#载体词表)的概念 id；长文不填 |
| `level` | 本库扩展 | 否 | 认知层级：Bloom 修订版六级之一，见下 |
| `subject` | subject | 是 | 主题词表的概念 id，一个或多个 |
| `entities` | 本库扩展，最近的 DCMI 属性是 `references` | 否 | 命名实体词表的 id，零个或多个 |
| `source` | source | 否 | 本单元派生自的内容单元或实体 id |
| `references` | references | 否 | 引用的文献、标准，实体 id |
| `created` | created | 是 | ISO 8601 日期 |
| `modified` | modified | 否 | ISO 8601 日期 |
| `status` | 本库扩展 | 是 | `draft`／`active`／`deprecated` |
| `isReplacedBy` | isReplacedBy | 因直接替代而废弃且存在替代项时必填 | 替代它的内容单元 id |
| `relation` | relation | 否 | 有关但不属前述关系的内容单元 id；必须互反，只在两者主题不同且常被一起阅读时添加 |
| `language` | language | 否 | 默认 `zh`，与默认不同时填 |

不设 `description`：`title` 加 `subject` 已足够定位，正文本身就是说明。不设 `creator`、`publisher`、`rights`：本库由一人使用，这些值恒定。

`entities` 是本库扩展。Dublin Core 没有表示内容涉及哪些具体产品的字段，最近的是 `references`，但 `references` 表示引用；内容提到 Claude Code 不等于引用其文档。`entities` 记录涉及的实体，`references` 记录引用的文献。

`status` 也是本库扩展。DCMI 有 `valid` 和 `isReplacedBy`，没有表示当前是否在用的状态字段。`isReplacedBy` 只覆盖直接替代这一种离开方式：因直接替代而废弃且存在替代项时必填；确认过时且没有替代项时留空，并在正文首段说明原因。草稿与定稿的区分、无替代的过时，都由状态表达。取值与词表生命周期对齐，见下文。

内容单元 `source`、主题旧 `origin` 和来源治理共享引用具有不同职责。

| 对象 | 职责 | 当前效力 |
|---|---|---|
| 内容单元 `source` | 按 Dublin Core 表示本内容单元实际派生自另一内容单元或实体 | 现行字段和值不变 |
| 主题旧 `origin` | 曾用于陈述本地概念的源头文献 | 不再是主题目标字段；历史库存只在迁移账本中审计 |
| 后置共享 `source` | 用 `registry`、`item`、`locator` 和相邻 `basis` 表示记录或结构的实际派生 | 接口已实现，正式来源数据、角色和引用尚未迁移 |

三者不能互相替代。内容单元引用文献用 `references`，涉及实体用 `entities`，具体字段值的依据按[维护](maintenance.md)记录；这些关系也不能仅因来源、索引或诊断命中自动生成。本次同步不修改任何内容 `source` 值，也不为旧 `origin` 补写新关系。

## 文档类型词表

`vocab/types.yaml` 中每条记录表示一个文档类型概念；`type` 保存概念 id，`label` 提供显示形式。类型按读者要做什么区分，取 Diátaxis 的 4 类，加 DITA 1.3 技术内容中 Diátaxis 没有的 2 类。以下 6 个数据值和来源保持不变。

| id | 中文 label | 读者来做什么 | 来源 |
|---|---|---|---|
| `tutorial` | 教程 | 学习，动手 | Diátaxis |
| `how-to` | 操作指南 | 工作，动手 | Diátaxis |
| `reference` | 参考 | 工作，查阅 | Diátaxis |
| `explanation` | 解释 | 学习，理解 | Diátaxis |
| `troubleshooting` | 排障 | 工作，纠正 | DITA 1.3 §2.7.1.6 |
| `glossary-entry` | 术语条目 | 查阅一个术语的一个义项 | DITA 1.3 §2.7.1.7 |

一条内容单元恰好关联一个文档类型概念，这是 Diátaxis 的核心主张。DCMI Type Vocabulary 区分的是媒介（Text、Image 等）；本库内容单元都是 Text，不用它区分文档类型。

## 体裁词表

`vocab/genres.yaml` 中每条记录表示一个作者立场概念；`genre` 保存概念 id，`label` 提供显示形式。取 IPTC NewsCodes genre 词表的子集，每条 `match` 到 IPTC 的 URI。以下 5 个数据值、定义和本地说明保持不变。

| id | 中文 label | IPTC 定义 | 笔记里的意思 |
|---|---|---|---|
| `background` | 背景 | 为所报事件提供背景与解释 | 转述事实、原理，不评价 |
| `analysis` | 分析 | 深入研究后得出的数据与结论 | 个人理解、比较、推断 |
| `opinion` | 观点 | 反映作者观点的评论 | 心得、偏好、立场 |
| `review` | 评价 | 对创作活动或服务的评价 | 工具、书、课程好不好 |
| `advice` | 建议 | 对个人问题的解答 | 给自己或他人的操作建议 |

IPTC 词表为新闻设计，定义中的“记者”“事件”按笔记语境理解；映射使用 `closeMatch`。理论见[笔记的类型](../concepts/note-types.md)。

## 载体词表

`vocab/forms.yaml` 中每条记录表示一个载体概念；`form` 保存概念 id。取 IEEE 1484.12.1-2002（LOM）§5.2 Learning Resource Type 的 15 个取值，每条 `match` 到 LOM。LOM 清单混合两个划分特征，按[层级结构](hierarchy.md)的数组规则分开保存。

| 数组 | 取值 |
|---|---|
| 呈现形式 | diagram、figure、graph、index、slide、table、narrative text |
| 教学活动 | exercise、simulation、questionnaire、exam、experiment、problem statement、self assessment、lecture |

速查表（cheat sheet）不在 LOM 中，据 Wikidata Q2309859 加入呈现形式数组。这些取值按译名阶梯查无中文译名：LOM 没有中文等同标准，普通名词的 Wikidata 标签不足以提供可靠依据。因此标签只保留英文，`scope` 给出中文解释。

不取 DITA 1.3 Learning and Training 的 5 种学习 topic：DITA 2.0 已把它们移出基础规范（DITA TC 2018-03-13 决议），不作为稳定来源。ISO 5127:2017 对文献类型有系统划分（3.4―3.5），条款在收费部分，核到后再引。

## 认知层级

`level` 取 Bloom 修订版 6 级（Anderson 与 Krathwohl 2001，据 Krathwohl 2002），表示作者对自己理解深度的评估，可选。

| id | 层级 | 含义 |
|---|---|---|
| `remember` | 记忆 | 从长期记忆中提取 |
| `understand` | 理解 | 确定材料的含义 |
| `apply` | 应用 | 在给定情境中执行或使用程序 |
| `analyze` | 分析 | 拆成部分并确定部分之间、与整体的关系 |
| `evaluate` | 评价 | 基于标准做判断 |
| `create` | 创造 | 把元素组合成新的整体 |

成熟度（Ahrens 的闪念笔记、文献笔记和永久笔记）不另设字段，由 `status` 的 `draft`／`active` 表达；文献笔记的特征由 `references` 非空表达。

## 标识符规则

标识符是在给定语境内对概念或资源的无歧义引用，依据 ISO 25964-1 §2.25 和 DCMI `identifier`。名称、显示标题、位置、排序和时间信息都不替代该身份。

现行词表的 id 继续使用已经登记的规则：只用小写 ASCII 字母、数字和连字符，且不以连字符开头或结尾；优先从有依据的英文 `label` 取得，无法取得英文时从来源代码或编号取得，不用拼音或自造英文。复制概念不以可变的来源代码作 id；同形异义以限定说明区分；不使用缩写。id 一经引用不改，各词表内唯一，跨表是否区分仍由字段决定。上述规则只说明现行词表既有 id 的语义，不为内容单元发放身份。

内容单元的 `identifier` 仍为必填且恰好一个的稳定身份。内容字段表、基数、值域和引用关系均不因此改变；`source`、`relation` 与 `isReplacedBy` 中的内容引用仍须指向该身份，而标题改变不改变它。

内容标识符的发放方式、唯一语境、表示形式和碰撞处理尚未取得项目决定。这是完整内容应用实现前的门禁，详见[标识符](../concepts/content-identifiers.md)。在决定批准前，不选择 UUID、对象前缀、时间戳、名称翻译、拼音或其他派生规则，也不从标题、显示文本、文件名、排序位置、时间值或应用表示静默取得身份。

候选术语接口中已有的身份只服务该未激活接口；它不适用于现行主题、实体、类型、体裁、载体、来源或内容单元，也不改变它们的现行身份语义。正式术语数据、委托和消费者仍未激活。

## 词表关系

字段与受控值来源之间的现行校验关系如下。

| 字段 | 词表 | 校验 |
|---|---|---|
| `type` | `vocab/types.yaml` | 值在表内 |
| `genre` | `vocab/genres.yaml` | 值在表内 |
| `form` | `vocab/forms.yaml` | 值在表内 |
| `level` | 本文认知层级表 | 值在表内 |
| `subject` | `vocab/topics.yaml` | 值在表内，且 `status` 不是 `deprecated`；引用对概念状态的影响见[主题词表设计](topics.md)的生命周期 |
| `entities`、`references`、`source` | `vocab/entities.yaml` 或内容单元 | 值在对应对象内 |

内容单元对词表的引用是单向的：词表不记录哪些内容引用了它，需要时由脚本从内容反查。

正式 `vocab/terms.yaml`、术语委托和术语消费者不存在。候选术语快照、术语表生成能力和仓库 Markdown 诊断不参与上表的现行引用校验，也不把主题标签或内容字段改成术语概念身份。

## 生命周期

内容单元使用以下生命周期。

| status | 含义 | 进入 | 离开 |
|---|---|---|---|
| `draft` | 未完成 | 新建 | 完成后转为 `active` |
| `active` | 在用 | — | 被替代或过时后转为 `deprecated` |
| `deprecated` | 不再维护，保留 | 有替代或确认过时 | 不删 |

3 个状态是本库扩展，没有外部标准直接规定内容单元的生命周期；取值与词表生命周期对齐，依据 Z39.19 §11.3 的新增、修改和废弃。内容单元不是 ISO 15489 意义上的文件，因为它不是业务证据；该标准不直接适用。但其处置原则可以借用：每类对象的保留和销毁要有书面决定和理由（ISO 15489-1 §3.8、§8.5），见[ISO 15489 笔记](../sources/iso-15489.md)。

`deprecated` 内容单元因直接替代而废弃且存在替代项时，`isReplacedBy` 必须指向替代单元；确认过时且没有替代项时，`isReplacedBy` 留空，并在正文首段说明原因。

### 处置决定

内容单元永久保留，不删。内容单元可能被其他内容单元引用，过时内容也记录了当时的理解；保留可维持现行引用和历史追踪。唯一例外是误建且没有任何引用的内容单元可以销毁。这是按 ISO 15489 的方式写下的处置决定，不是照搬词表规则。

旧主题 `origin` 不再是保留内容单元的依据，也不再是主题目标字段。该字段的去向不改变上述处置决定。

## 应用映射

每种应用都以一篇 target 设计引用本文和其他应用无关模型，并按 [Application Profile](../concepts/application-profile.md) 和适用的已采纳决定说明其约束。应用只为既定对象选择表示位置、类型、引用形式和允许的信息损失；这些 binding 不修改本文的字段语义、基数、值域、稳定身份或对象关系，也不是词表层的 `crosswalk`。

每篇 target 设计必须说明功能范围、模型引用、字段约束、使用条件、编码规则、失败处理和未实现边界。具体路径、property、引用语法和界面能力只属于 target，留在该处是为了不把一个应用的表示选择写成所有应用的模型规则。

导出 artifact contract 与 `Application Profile` 分开。前者只在语义选择完成后规定输入快照、字节序列化、文件集合、项目清单、生成后校验和发布；它不得反向修改 target binding 或本文字段。

回流中的未解析字符串只交人工判断，不自动建立概念、关系或状态记录。target 设计、字段合同、生成物或浏览入口存在，都不等于内容消费者已经实现并启用；只有消费者实际读取已校验的内容字段或可审计检索记录后，内容引用统计和回流才成立。

[Obsidian 映射](targets/obsidian.md)是当前唯一的 target 设计。其完整内容应用已经设计，但尚未实现；现有实现仍只生成六份正式词表的单向参考表示，不建立或读取内容单元，也不提供内容引用统计、检索记录或回流。

仓库 Markdown 正文诊断不是外部知识库回流。未来术语快照和术语表生成器也不是现行应用的正式输入；正式术语数据、委托、消费者和切换状态未激活，任何应用消费这些后置对象前仍须另行取得正式激活决定。

## 权威来源

- [ISO 15836-1:2017](https://www.iso.org/standard/71339.html)、[ISO 15836-2:2019](https://www.iso.org/standard/71341.html)、[DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)：字段
- [DITA 1.3 §2.2.1 DITA topics](https://docs.oasis-open.org/dita/dita/v1.3/os/part1-base/archSpec/base/topicover.html)：内容单元的定义参照
- [Diátaxis](https://diataxis.fr/)、[DITA 1.3 §2.7.1](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/archSpec/technicalContent/dita-technicalContent-InformationTypes.html)：文档类型
- [IPTC NewsCodes Genre](https://cv.iptc.org/newscodes/genre/)：体裁
- IEEE 1484.12.1-2002 LOM §5.2，[LICEF 镜像的 final draft](https://github.com/LICEF/lompad/blob/master/documentation/LOM_1484_12_1_v1_Final_Draft.pdf)；[2020 版](https://standards.ieee.org/ieee/1484.12.1/7699/)已发布，取值变动未核：载体
- [schema.org 30.0](https://schema.org/)：HowTo、TechArticle、Review 作映射目标
- OASIS DITA TC，[移除 Learning and Training 的决议](https://github.com/oasis-tcs/dita/pull/111)，2018
- Krathwohl, D. R. [*A Revision of Bloom's Taxonomy: An Overview*](https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf), 2002：认知层级
- ANSI/NISO Z39.19-2005 §6.2.1 Homographs：限定说明；§11.3 Maintenance：生命周期
- [ISO 15489-1:2016](https://www.iso.org/standard/62542.html) §3.8 disposition、§8.5 disposition authorities：处置决定的写法，见[笔记](../sources/iso-15489.md)
- ISO 25964-1:2011 §2.25 identifier
- ISO 5127:2017 的文献类型条款（3.4―3.5）核到后，载体词表是否据其调整
