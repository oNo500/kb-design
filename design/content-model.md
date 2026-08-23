# 内容模型

知识库里一条内容单元抽象地有什么。本文与应用无关：不提任何工具的字段名、文件格式或目录；那些在 `design/targets/` 各应用的映射里。字段取自 Dublin Core（ISO 15836），受控字段的值来自本库的词表。理论见[元数据](../concepts/metadata.md)。

## 内容单元

一条内容单元是知识库里最小的可独立引用、可独立打标签的东西：有标题，讲一个主题。这是对 DITA 1.3 §2.2.1 对 topic 的定义（“写作与复用的基本单位……有标题和可选的正文……每个 topic 只含一个主题”）的与应用无关转述；在 Obsidian 里它是一篇笔记，在 DITA 里就是一个 topic。本文只叫它“内容单元”。

## 字段

| 字段 | Dublin Core | 必填 | 值 |
|---|---|---|---|
| `identifier` | identifier | 是 | 按下文 id 规则，稳定不变 |
| `title` | title | 是 | 字面值 |
| `type` | type | 是 | 体裁：[文档类型词表](#文档类型词表)的 id，恰好一个 |
| `genre` | 本库扩展，依据 IPTC genre | 是 | 作者立场：[体裁词表](#体裁词表)的 id，恰好一个 |
| `form` | 本库扩展，依据 IEEE LOM | 否 | 载体：[载体词表](#载体词表)的 id；长文不填 |
| `level` | 本库扩展 | 否 | 认知层级：Bloom 修订版六级之一，见下 |
| `subject` | subject | 是 | 主题词表的概念 id，一个或多个 |
| `entities` | 本库扩展，最近的 DCMI 属性是 `references` | 否 | 命名实体词表的 id，零个或多个 |
| `source` | source | 否 | 本单元派生自的内容单元或实体 id |
| `references` | references | 否 | 引用的文献、标准，实体 id |
| `created` | created | 是 | ISO 8601 日期 |
| `modified` | modified | 否 | ISO 8601 日期 |
| `status` | 本库扩展 | 是 | `draft` / `active` / `deprecated` |
| `isReplacedBy` | isReplacedBy | `deprecated` 时必填 | 替代它的内容单元 id |
| `relation` | relation | 否 | 有关但不属前述关系的内容单元 id；约束同主题词表的 RT：必须互反，只在两者主题不同、且常被一起读时加 |
| `language` | language | 否 | 默认 `zh`，与默认不同时填 |

不设 `description`：`title` 加 `subject` 已足够定位，正文本身就是说明。不设 `creator`、`publisher`、`rights`：单人库，值恒定，不记。

`entities` 是本库扩展：Dublin Core 没有“这篇内容涉及哪些具体产品”的字段，最近的是 `references`，但 `references` 的语义是“引用了”，而提到 Claude Code 不一定是引用它的文档。两个字段分开：`entities` 记涉及的实体，`references` 记引用的文献。

`status` 也是本库扩展：DCMI 有 `valid`（有效期）和 `isReplacedBy`，没有“当前是否在用”的状态字段。`isReplacedBy` 只覆盖被替代这一种离开方式；草稿与定稿的区分、无替代的过时，都需要状态。取值与词表的生命周期对齐，见下文。

## 文档类型词表

`vocab/types.yaml`，`type` 字段的取值：体裁，按读者来做什么分。一份术语表（Z39.19 的 list），取 Diátaxis 的四类，加 DITA 1.3 技术内容里 Diátaxis 没有的两类：

| id | 首选词 | 读者来做什么 | 来源 |
|---|---|---|---|
| `tutorial` | 教程 | 学习，动手 | Diátaxis |
| `how-to` | 操作指南 | 工作，动手 | Diátaxis |
| `reference` | 参考 | 工作，查阅 | Diátaxis |
| `explanation` | 解释 | 学习，理解 | Diátaxis |
| `troubleshooting` | 排障 | 工作，纠正 | DITA 1.3 §2.7.1.6 |
| `glossary-entry` | 术语条目 | 查阅一个术语的一个义项 | DITA 1.3 §2.7.1.7 |

一条内容单元恰好一类，这是 Diátaxis 的核心主张。DCMI Type Vocabulary 分的是媒介（Text、Image……），本库的内容单元都是 Text，不用它区分。

## 体裁词表

`vocab/genres.yaml`，`genre` 字段的取值：作者立场，按作者与内容的关系分。取 IPTC NewsCodes genre 词表的子集，每条 `match` 到 IPTC 的 URI：

| id | 首选词 | IPTC 定义 | 笔记里的意思 |
|---|---|---|---|
| `background` | 背景 | 为所报事件提供背景与解释 | 转述事实、原理，不评价 |
| `analysis` | 分析 | 深入研究后得出的数据与结论 | 个人理解、比较、推断 |
| `opinion` | 观点 | 反映作者观点的评论 | 心得、偏好、立场 |
| `review` | 评价 | 对创作活动或服务的评价 | 工具、书、课程好不好 |
| `advice` | 建议 | 对个人问题的解答 | 给自己或他人的操作建议 |

IPTC 的词表是为新闻设计的，定义里的“记者”“事件”按笔记语境理解；映射用 `closeMatch`。理论见[笔记的类型](../concepts/note-types.md)。

## 载体词表

`vocab/forms.yaml`，`form` 字段的取值：载体，内容单元的呈现形式。取 IEEE 1484.12.1-2002（LOM）§5.2 Learning Resource Type 的 15 个取值，每条 `match` 到 LOM。LOM 的清单混了两个划分特征，按[层级结构](hierarchy.md)规则 8 拆成两个数组：

| 数组 | 取值 |
|---|---|
| 呈现形式 | diagram、figure、graph、index、slide、table、narrative text |
| 教学活动 | exercise、simulation、questionnaire、exam、experiment、problem statement、self assessment、lecture |

速查表（cheat sheet）LOM 没有，据 Wikidata Q2309859 加入呈现形式数组。这些取值按译名阶梯查无中文译名（LOM 无中文等同标准，值是普通名词，Wikidata 不可靠），按第 4 级不译：标签只有英文，`scope` 给一句中文解释。

不取 DITA 1.3 Learning and Training 的五种学习 topic：DITA 2.0 已把它们移出基础规范（DITA TC 2018-03-13 决议），不作为稳定来源。ISO 5127:2017 对文献类型有系统划分（3.4–3.5），条款在收费部分，核到后再引。

## 认知层级

`level` 的取值，Bloom 修订版（Anderson & Krathwohl 2001，据 Krathwohl 2002）六级，作者对自己理解深度的评估，可选：

| id | 层级 | 含义 |
|---|---|---|
| `remember` | 记忆 | 从长期记忆中提取 |
| `understand` | 理解 | 确定材料的含义 |
| `apply` | 应用 | 在给定情境中执行或使用程序 |
| `analyze` | 分析 | 拆成部分并确定部分之间、与整体的关系 |
| `evaluate` | 评价 | 基于标准做判断 |
| `create` | 创造 | 把元素组合成新的整体 |

成熟度（Ahrens 的闪念 / 文献 / 永久笔记）不另设字段，由 `status` 的 `draft` / `active` 表达；文献笔记的特征由 `references` 非空表达。

## id 规则

全库三份词表和内容单元共用一套 id 规则。依据：ISO 25964-1 §2.25，标识符是在给定语境内唯一标识概念、词或其他实体的符号串；DCMI `identifier`，在给定语境内对资源的无歧义引用。

1. 小写 ASCII 字母、数字、连字符；不以连字符开头或结尾；不含其他字符
2. 从英文首选词取：`sql-injection`、`information-retrieval`。英文首选词按译名阶梯（[治理](governance.md)“译名”）取：来源体系自带的英文名；GB 等同采用标准的译名；Wikidata 英文标签；都没有时不给英文，id 从来源的代码或编号取（如 GB/T 13745 的 `870-3050`），并在 `label` 只留中文。不用拼音，不自造英文
3. 复制的概念不用来源的代码作 id（`FPL-Types` 不作 id），代码记在 `match`；id 从名称取，来源改版时代码变、id 不变
4. 一经引用不再改。名字错了，改 `label`，不改 id
5. 同形异义的概念用限定词区分。Z39.19 §6.2.1：限定词是附在词上、使含义无歧义的词，用括号标在词后——`cranes (lifting equipment)`、`cranes (birds)`；能用自然语言里的复合词就不用限定词。本库 `label` 按此写括号形式；id 是 ASCII，限定词编码为后缀：`cranes-lifting-equipment`、`cranes-birds`。限定词取自上位概念或类别
6. 长度不设上限，但不缩写：`networking-and-communication`，不写 `nc`
7. 四份表（主题、实体、类型、内容单元）各自唯一；跨表不要求唯一，引用时由字段决定查哪张表

## 与词表的关系

| 字段 | 词表 | 校验 |
|---|---|---|
| `type` | `vocab/types.yaml` | 值在表内 |
| `genre` | `vocab/genres.yaml` | 值在表内 |
| `form` | `vocab/forms.yaml` | 值在表内 |
| `level` | 本文认知层级表 | 值在表内 |
| `subject` | `vocab/topics.yaml` | 值在表内，且 `status` 不是 `deprecated`。引用对概念状态的影响见[主题词表设计](topics.md)生命周期 |
| `entities`、`references`、`source` | `vocab/entities.yaml` 或内容单元 | 值在表内 |

内容单元对词表的引用是单向的：词表不记录哪些内容引用了它，需要时由脚本从内容反查。

## 生命周期

| status | 含义 | 进入 | 离开 |
|---|---|---|---|
| `draft` | 未完成 | 新建 | 完成 → `active` |
| `active` | 在用 | — | 被替代或过时 → `deprecated` |
| `deprecated` | 不再维护，保留 | 有替代或确认过时 | 不删 |

三个状态是本库扩展，没有外部标准直接规定内容单元的生命周期；取值与词表的生命周期对齐（Z39.19 §11.3 的加、改、废）。内容单元不是 ISO 15489 意义上的文件（它不是业务证据），该标准不直接适用；但它的处置原则可借：每类东西的保留和销毁要有书面的决定和理由（ISO 15489-1 §3.8、§8.5），见 [ISO 15489 笔记](../sources/iso-15489.md)。

`deprecated` 的内容单元必有 `isReplacedBy`，指向替代它的单元；确认过时且无替代的，`isReplacedBy` 留空并在正文首段说明原因。

### 处置决定

内容单元永久保留，不删。理由：内容单元被其他内容单元和概念的 `origin` 引用，删除断链；过时的内容记录了当时的理解，本身是信息。唯一例外：误建且没有任何引用的内容单元可以销毁。这是按 ISO 15489 的方式写下的处置决定，不是照搬词表的规则。

## 应用映射的要求

每种应用一篇 `design/targets/<应用>.md`。以下五个问题是本库的接口约定，无外部依据；它们保证映射层不改动本文：

1. 每个字段落到该应用的什么（属性名、位置）
2. 词表怎么导出到该应用（标签、枚举、subjectScheme……）
3. `subject`、`entities` 的引用在该应用里怎么表达（链接、标签）
4. 回流：从该应用抽候选词、统计引用次数怎么做
5. 该应用做不到的字段或约束，如何处理

映射不得改动本文的字段定义；本文不提任何应用的细节。

## 待定事项


## 权威来源

- [ISO 15836-1:2017](https://www.iso.org/standard/71339.html)、[ISO 15836-2:2019](https://www.iso.org/standard/71341.html)、[DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)：字段
- [DITA 1.3 §2.2.1 DITA topics](https://docs.oasis-open.org/dita/dita/v1.3/os/part1-base/archSpec/base/topicover.html)：内容单元的定义参照
- [Diátaxis](https://diataxis.fr/)、[DITA 1.3 §2.7.1](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/archSpec/technicalContent/dita-technicalContent-InformationTypes.html)：文档类型
- [IPTC NewsCodes Genre](https://cv.iptc.org/newscodes/genre/)：体裁
- IEEE 1484.12.1-2002 LOM §5.2，[LICEF 镜像的 final draft](https://github.com/LICEF/lompad/blob/master/documentation/LOM_1484_12_1_v1_Final_Draft.pdf)；2020 版[已发布](https://standards.ieee.org/ieee/1484.12.1/7699/)，取值变动未核：载体
- [schema.org 30.0](https://schema.org/)：HowTo、TechArticle、Review 作映射目标
- OASIS DITA TC，[移除 Learning and Training 的决议](https://github.com/oasis-tcs/dita/pull/111)，2018
- Krathwohl, D. R. [*A Revision of Bloom's Taxonomy: An Overview*](https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf), 2002：认知层级
- ANSI/NISO Z39.19-2005 §6.2.1 Homographs：限定词；§11.3 Maintenance：生命周期
- [ISO 15489-1:2016](https://www.iso.org/standard/62542.html) §3.8 disposition、§8.5 disposition authorities：处置决定的写法，见[笔记](../sources/iso-15489.md)
- ISO 25964-1:2011 §2.25 identifier
- ISO 5127:2017 的文献类型条款（3.4–3.5）核到后，载体词表是否据其调整
