# 受控词表 (Controlled Vocabulary)

## 定义

受控词表是一份预先规定并持续管理的名称、标目或代码列表，每一项表示一个概念。ISO 25964-1:2011 §2.12 明确把列表中的每一项与概念相连；ANSI/NISO Z39.19-2005 (R2010) 则强调列表须明确列举、消除歧义和冗余，并由指定机构维护。

受控词表控制的是概念如何被表示和关联，不是把自然语言中的每个字符串都变成独立节点。例如，`PostgreSQL` 与 `postgres` 可以表示同一个概念；概念仍只有一个，两个字符串在记录中承担不同的检索作用。

## 解决的问题

受控词表把概念判断与表示形式的处理分开，从而处理以下问题。

| 问题 | 例子 | 处理方式 |
|---|---|---|
| 同一概念有多种表示 | `PostgreSQL`、`postgres` | 选择一个首选标签，其余形式作为替代标签或入口 |
| 同一字符串可能表示不同概念 | `Apple` 可指水果，也可指公司 | 分别建立概念，并用限定说明帮助消歧 |
| 拼写、缩写或语言不同 | `USA`、`U.S.A.`、`United States` | 将已核实的形式连接到同一概念 |

表示形式只有在概念对应和形式依据均已核实后才能进入正式记录。机器识别出的字符串只提供线索，不自动成为项目采用的名称。

## 结构类型

Z39.19 区分列表、同义词环、分类法和叙词表四种受控词表结构。本体不是该标准所列的受控词表类型，但可作为结构能力的对照。结构越丰富，可表达的关系越多，维护成本也越高。

| 结构 | 组织方式 | 可表达的内容 | 知识库示例 |
|---|---|---|---|
| 列表 | 平铺列出允许值 | 成员资格 | `status` 只允许 `draft`、`review`、`published` |
| 同义词环 | 多种表示被同等用于检索 | 表示形式等价 | 搜索 `k8s` 时也检索 `Kubernetes` |
| 分类法 | 用层级关系组织概念 | 上下位关系 | `技术 > 后端 > 数据库 > PostgreSQL` |
| 叙词表 | 结合首选表示、替代表示、层级关系和相关关系 | 表示形式控制与概念关系 | `PostgreSQL` 有替代标签 `postgres`，上位概念是 `关系型数据库` |
| 本体 | 用可定义的关系类型连接实体并支持形式语义 | 超出叙词表关系的知识表示 | 服务依赖数据库，数据库由某组织维护 |

本知识库的元数据枚举适合使用列表，主题结构适合使用分类法或轻量叙词表。是否增加关系类型取决于检索用途，不由字符串数量决定。

## 关系类型

叙词表须区分表示同一概念的形式之间的等价关系，以及概念之间的层级关系和相关关系。ISO 25964-1:2011 §2.18 把等价关系连接到表示同一概念的两个 `term`；§2.23 和 §2.2 分别把层级关系和相关关系连接到概念。

### 等价关系

`USE` 从非首选表示指向首选表示，`UF` 从首选表示反向列出可作为入口的其他表示。它们连接同一概念记录内的表示形式，不连接两个概念。

```text
postgres    USE  PostgreSQL
PostgreSQL  UF   postgres
```

旧表示因改名而不再首选时，可按检索、替代和历史追踪的需要继续保留。保留旧表示不等于保留一个独立概念。

### 层级关系

`BT` 和 `NT` 是层级关系的标准指示符，关系端点是概念。Z39.19 将 `BT` 的标签展开为 `broader term`，将 `NT` 的标签展开为 `narrower term`；这些完整英文形式是标准中的来源事实，不构成本库对形式的另行准入。

```text
PostgreSQL   BT  关系型数据库
关系型数据库  NT  PostgreSQL, MySQL, SQLite
```

层级关系支持按上位概念浏览，也支持沿下位概念扩展检索。

### 相关关系

`RT` 表示两个概念之间没有层级关系，但存在强语义联系。Z39.19 将该标签展开为 `related term`，并把关系规定为对称关系；该完整英文形式同样只作为标准标签的来源事实保留。

```text
PostgreSQL  RT  pgvector
```

相关关系不是无法分类时的任意兜底。只有概念间的语义联系经核实后，才能建立该关系。

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
5. 人名、产品名和系统名由[命名实体词表](../design/model/entities.md)管理；实体记录与主题概念的关系另行维护。
6. `deprecated` 概念记录继续保留；旧表示只在既有检索、替代关系或历史追踪需要时随记录保留。只有满足既定条件的 `candidate` 概念记录可以取得删除资格，实际删除仍服从治理权限。

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
