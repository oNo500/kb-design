# 受控词表 (Controlled Vocabulary)

## 定义

受控词表是一份预先规定并持续管理的名称、标目或代码列表，每一项表示一个概念。ISO 25964-1:2011 §2.12 明确把列表中的每一项与概念相连；ANSI/NISO Z39.19-2005 (R2010) 则强调列表须明确列举、消除歧义和冗余，并由指定机构维护。

受控词表控制概念如何被表示和关联，不把自然语言中的每个字符串都变成独立节点。例如，本库“关系数据库”与 `Relational Databases` 是同一主题概念的中英文标签，概念 ID 只有一个。中文标签采用模型知识第 5 级，外部用法未核实；英文标签有已登记的外部依据。产品 PostgreSQL 则由名称规范表管理其具体身份；统一产品名称与组织主题概念具有不同的收录职责。

## 解决的问题

受控词表把概念判断与表示形式的处理分开，从而处理以下问题。

| 问题 | 例子 | 处理方式 |
|---|---|---|
| 同一概念有多种语言表示 | 关系数据库、`Relational Databases` | 分语言保存已采纳的标签及各自依据，共用概念 ID |
| 同一字符串可能表示不同概念 | “模型”在数据组织与机器学习语境中指向不同问题 | 结合上下文、范围和限定说明消歧 |
| 检索写法与标签不同 | 英文查询的大小写与 `Relational Databases` 不同 | 检索时规范化写法，正式表示仍按依据管理 |

表示形式进入正式记录须具备概念对应依据，并按现行语言依据规则取得采纳。已授权的第 5 级译名须保留模型判断及外部用法未核实的说明；采纳不等于外部核实。机器识别出的字符串只提供线索，不自动成为项目采用的名称。

## 结构类型

Z39.19 区分列表、同义词环、分类法和叙词表四种受控词表结构。本体不是该标准所列的受控词表类型，但可作为结构能力的对照。结构越丰富，可表达的关系越多，维护成本也越高。

| 结构 | 组织方式 | 可表达的内容 | 知识库示例 |
|---|---|---|---|
| 列表 | 平铺列出允许值 | 成员资格 | 内容状态只允许 `draft`、`active`、`deprecated` |
| 同义词环 | 多种表示被同等用于检索 | 表示形式等价 | 检索某概念的已核实名称时，同时检索其其他等价表示 |
| 分类法 | 用层级关系组织概念 | 上下位关系 | 本库主题中的“数据管理 → 关系数据库” |
| 叙词表 | 结合首选表示、替代表示、层级关系和相关关系 | 表示形式控制与概念关系 | 在主题层级之外，管理同一概念的已核表示及概念间的相关关系 |
| 本体 | 用可定义的关系类型连接实体并支持形式语义 | 超出叙词表关系的知识表示 | 服务依赖数据库，数据库由某组织维护 |

本知识库的元数据枚举适合使用列表，主题结构适合使用分类法或轻量叙词表。是否增加关系类型取决于检索用途，不由字符串数量决定。

## 关系类型

叙词表须区分表示同一概念的形式之间的等价关系，以及概念之间的层级关系和相关关系。ISO 25964-1:2011 §2.18 把等价关系连接到表示同一概念的两个 `term`；§2.23 和 §2.2 分别把层级关系和相关关系连接到概念。

### 等价关系

`USE` 从非首选表示指向首选表示，`UF` 从首选表示反向列出可作为入口的其他表示。它们连接同一概念记录内的表示形式，不连接两个概念。

```text
非首选表示  USE  首选表示
首选表示    UF   非首选表示
```

例如，本库“关系数据库”的中英文标签共用一个概念 ID，各语言的首选状态分别管理；若某语言另有经过核实的非首选名，再使用相应的形式关系。两个语言标签不能仅因共用概念就被误写成两个概念之间的关系。旧表示因改名而不再首选时，可按检索、替代和历史追踪的需要继续保留，不另建概念。

### 层级关系

`BT` 和 `NT` 是层级关系的标准指示符，关系端点是概念。Z39.19 将 `BT` 的标签展开为 `broader term`，将 `NT` 的标签展开为 `narrower term`；这些完整英文形式是标准中的来源事实，不构成本库对形式的另行准入。

```text
关系数据库  BT  数据管理
数据管理    NT  关系数据库
```

此例沿用本库的主题组织，层级关系支持按上位概念浏览和向下扩展检索。PostgreSQL 是具体软件，不因讨论关系数据库就自动成为本库主题树的下位概念；产品与主题的关联另行表达。

### 相关关系

`RT` 表示两个概念之间没有层级关系，但存在强语义联系。Z39.19 将该标签展开为 `related term`，并把关系规定为对称关系；该完整英文形式同样只作为标准标签的来源事实保留。

```text
关系数据库  RT  数据建模
```

此例只说明两个主题概念之间的关系记法，不表示本库已登记该条 RT。相关关系不能作为无法分类时的任意后备，只有语义联系经核实后才能建立。PostgreSQL 与某个扩展的联系属于具体对象关系，不能直接借用主题概念的 RT 代替。

### 对应属性

SKOS 把概念与词法标签分开，也把概念体系内部的语义关系与跨概念体系的映射分开。

| 作用 | ISO 25964／Z39.19 | SKOS |
|---|---|---|
| 首选与替代表示 | `USE`／`UF` | `skos:prefLabel`／`skos:altLabel` |
| 概念层级 | `BT`／`NT` | `skos:broader`／`skos:narrower` |
| 概念相关 | `RT` | `skos:related` |

标签属性附着于概念；层级和相关属性连接概念。两类属性不能因为界面上都显示文字而合并成同一种关系。

## 知识库用法

本知识库按以下边界使用受控词表。

1. 机器或人工先识别带上下文的字符串，再与已登记的首选、替代和隐藏标签比较；未解析字符串等待人工判断。
2. 只有完成概念判断和依据核验后，才建立或更新 `candidate` 概念记录。`candidate` 是概念记录状态，不是字符串的独立生命周期。
3. 内容的主题范围继续由现有 `subject` 字段表达；允许值是主题词表中存在且状态不是 `deprecated` 的概念 ID，可取一个或多个。
4. 搜索先把已登记标签解析到概念 ID，再沿等价表示或概念关系扩展。未解析字符串不直接进入主题树。
5. 产品、组织等涉及对象的名称与身份由[命名实体词表](../design/model/entities.md)管理；人物仍受人员准入约束。对象与主题的关联另行维护，不因名称出现就建立记录或主题节点。
6. 为模型、规则或词表提供依据的文献进入独立[参考文献目录](../design/model/bibliography.md)，获准用途由[来源用途登记](../design/model/sources-registry.md)管理。文献可以是广义实体，但不因此属于本项目的实体词表；普通笔记参考链接也不自动进入设计目录。
7. `deprecated` 概念记录继续保留；旧表示只在既有检索、替代关系或历史追踪需要时随记录保留。只有满足既定条件的 `candidate` 概念记录可以取得删除资格，实际删除仍服从治理权限。

这些用法的正式字段、状态和维护动作分别见[主题词表](../design/model/topics.md)、[内容模型](../design/model/content-model.md)和[维护](../design/governance/maintenance.md)。

## 权威来源

以下标准、教材和实例分别支持定义、结构、关系模型与实际用途。

### 标准

- [ISO 25964-1:2011 — Thesauri and interoperability with other vocabularies, Part 1: Thesauri for information retrieval](https://www.iso.org/standard/53657.html)。2022 年复审确认；[ISO/FDIS 25964-1](https://www.iso.org/standard/86713.html) 修订项目仍在进行，正文未取得，不预测发布日期或内容
- [ISO 25964-2:2013 — Part 2: Interoperability with other vocabularies](https://www.iso.org/standard/53658.html)。2023 年复审确认；[ISO/AWI 25964-2](https://www.iso.org/standard/92117.html) 修订项目正文未取得。材料身份和阅读边界见 [ISO 25964 阅读笔记](../references/iso-25964.md)
- [NISO 的 ISO 25964 数据模型、XML Schema 与 SKOS 对应材料](https://www.niso.org/schemas/iso25964)
- [ANSI/NISO Z39.19-2005 (R2010) — Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies](https://www.niso.org/publications/ansiniso-z3919-2005-r2010)。列表、同义词环、分类法和叙词表四种结构出自该标准
- [GB/T 13190.1-2015 信息与文献 叙词表及与其他词表的互操作 第 1 部分：用于信息检索的叙词表](https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D7A385D3A7E05397BE0A0AB82A)，等同采用 ISO 25964-1
- [GB/T 13190.2-2018 第 2 部分：与其他词表的互操作](https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D82DD2D3A7E05397BE0A0AB82A)
- [W3C SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/skos-reference/)，2009 Recommendation

### 教材

- Harpring, Patricia. [*Introduction to Controlled Vocabularies: Terminology for Art, Architecture, and Other Cultural Works*](https://www.getty.edu/research/publications/electronic_publications/intro_controlled_vocab/). Getty Research Institute. 在线版，2023 修订
- Lancaster, F. W. *Vocabulary Control for Information Retrieval*. 2nd ed. Information Resources Press, 1986
- Aitchison, J., Gilchrist, A., Bawden, D. *Thesaurus Construction and Use: A Practical Manual*. 4th ed. Europa Publications, 2000

### 词表实例

- [MeSH (Medical Subject Headings)](https://www.nlm.nih.gov/mesh/)，美国国家医学图书馆
- [LCSH (Library of Congress Subject Headings)](https://id.loc.gov/authorities/subjects.html)
- [AAT (Getty Art & Architecture Thesaurus)](https://www.getty.edu/research/tools/vocabularies/aat/)
- [《汉语主题词表》](https://ct.istic.ac.cn/)，中国科学技术信息研究所
