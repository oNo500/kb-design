# 元数据 (Metadata)

## 定义

元数据是**标识一份资源的属性的数据**（ISO 25964-1 §2.33）：这份东西叫什么、谁写的、讲什么、什么类型、什么时候、从哪来。它的用途是定位、发现、评价和选择资源——不打开内容就能判断要不要打开。

公认的元数据元素集是 **Dublin Core**：1995 年在俄亥俄州 Dublin 的研讨会上定出的 15 个核心元素，后成为国际标准 ISO 15836。它故意做得很小：任何资源——文本、图像、数据集、软件——都能用这 15 个元素描述，所以叫“核心”。

## 解决的问题

| 问题 | 例子 | 元数据的处理 |
|---|---|---|
| 不打开内容不知道是什么 | 一千篇笔记，只有文件名 | 每份资源带标题、主题、类型、日期 |
| 各人各系统描述资源的字段不同，无法交换 | 一个系统叫 `author`，另一个叫 `creator`，第三个叫 `by` | 用公认的元素集，字段名和含义统一 |
| 主题描述用自由文本，检索不可靠 | `subject: 数据库相关` | `subject` 的值从受控词表取 |
| 资源之间的关系没人记 | 这篇是那篇的新版、这篇引用了那篇 | `relation` 及其细分：`isVersionOf`、`replaces`、`references` |

## Dublin Core 的十五个核心元素

ISO 15836-1:2017，即 DCMI 的 `/elements/1.1/` 命名空间：

| 元素 | 含义 |
|---|---|
| title | 资源的名称 |
| creator | 主要责任者 |
| subject | 资源的主题 |
| description | 对资源内容的说明 |
| publisher | 发布者 |
| contributor | 其他贡献者 |
| date | 资源生命周期中某个事件的日期 |
| type | 资源的性质或体裁 |
| format | 文件格式、物理介质或尺寸 |
| identifier | 在给定语境内对资源的无歧义引用 |
| source | 本资源派生自的资源 |
| language | 资源的语言 |
| relation | 相关资源 |
| coverage | 资源的空间或时间范围 |
| rights | 权利信息 |

每个元素都可选、可重复、无顺序。

## DCMI Metadata Terms

十五个元素之外，DCMI 又发布了几十个更细的属性和类，2019 年成为 ISO 15836-2。对知识库最有用的几个：

| 属性 | 含义 |
|---|---|
| `isVersionOf` / `hasVersion` | 本资源是某资源的一个版本 / 有版本 |
| `replaces` / `isReplacedBy` | 本资源替代某资源 / 被替代 |
| `references` / `isReferencedBy` | 本资源引用某资源 / 被引用 |
| `isPartOf` / `hasPart` | 部分与整体 |
| `created` / `modified` / `issued` | `date` 的细分：创建、修改、发布 |
| `subject` | 同核心元素；推荐值取自受控词表 |

**DCMI Type Vocabulary** 是 `type` 的推荐取值，12 个：Collection、Dataset、Event、Image、InteractiveResource、MovingImage、PhysicalObject、Service、Software、Sound、StillImage、Text。它分的是资源的**媒介性质**，不是内容的体裁——一篇教程和一篇参考都是 Text。体裁要另取词表。

## 与受控词表的关系

两者是同一件事的两面：元数据定义**有哪些字段**，受控词表定义**字段能取哪些值**。ISO 25964-1 §2.33 的注说得直接：标引时选定的首选词通常就作为元数据值。

| 元数据字段 | 值从哪来 |
|---|---|
| `subject` | 主题叙词表 |
| `type` | 文档类型的代码表（DCMI Type Vocabulary 或自定） |
| `creator`、`publisher` | 名称规范表 |
| `identifier` | id 规则 |
| `title`、`description`、`date` | 字面值，不受控 |

所以“内容模型”这个设计，本质上是：取 Dublin Core 的字段，给每个受控字段指定一份词表。

## 在知识库中

- 内容单元的字段按 Dublin Core 取，不自造字段名；本库没有的概念（如“状态”）用 DCMI Terms 里最近的属性或明确标为本库扩展
- `subject` 的值只能是主题词表的概念 id；`type` 的值只能是文档类型词表的 id；引用的文献和工具通过实体 id
- 元数据是形态无关的：Obsidian 的 properties、DITA 的 prolog 都是它的一种落地，字段含义不随工具变

## 权威来源

- [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)，DCMI Recommendation，2020-01-20
- [ISO 15836-1:2017 Information and documentation — The Dublin Core metadata element set — Part 1: Core elements](https://www.iso.org/standard/71339.html)
- [ISO 15836-2:2019 — Part 2: DCMI Properties and classes](https://www.iso.org/standard/71341.html)。DCMI Usage Board 是 ISO 15836 的维护机构
- ISO 25964-1:2011 §2.33 metadata，见 [ISO 25964 阅读笔记](../sources/iso-25964.md)
