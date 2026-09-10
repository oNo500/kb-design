# 知识图谱 (Knowledge Graph)

## 图谱的定义

知识图谱是用于积累和传达现实世界知识的图数据结构，节点表示感兴趣的实体，边表示实体之间的关系。本库采用 Hogan 等人的这一概括，不把本体和推理引擎作为所有知识图谱的必要组成。

例如，可以用节点表示 PostgreSQL、pgvector 和 PostgreSQL Global Development Group，再用边表示扩展和维护关系。这里的对象、对象之间的关系及图中的节点和边分别属于语义与表示，不能把它们当作无条件同义的术语。

RDF 使用主语、谓语、宾语组成的三元组表示陈述；属性图则允许节点和边携带属性值对。说明图谱的具体结构时，需要先说明采用哪种图模型，不能把 RDF 的三元组约束直接套给所有知识图谱。

## 解决的问题

| 问题 | 例子 | 图谱的处理 |
|---|---|---|
| 知识散在文档里，机器读不出来 | “pgvector 是 PostgreSQL 的扩展”埋在某篇笔记第三段 | 抽成三元组，机器可查询 |
| 同一事物多个名字，关联断开 | `postgres` 和 `PostgreSQL` 两个标签各挂一堆笔记 | 一个实体一个 ID，名字是属性 |
| 只知道“有关”，不知道怎么有关 | 笔记 A 链接了笔记 B | 边带类型：`依赖` / `扩展` / `维护者` |
| 回答不了跨文档的问题 | “我所有依赖 PostgreSQL 的项目有哪些” | 沿边遍历，一条查询出结果 |
| 隐含关系没人写 | 没人写过“项目 X 间接依赖 libpq” | 按已确定的规则取得蕴涵答案；是否写回图另行选择 |

## 对象与表示

实体是图谱所描述的对象，节点是所选图模型中的表示。关系是对象之间的语义联系，边是图中的连接结构。例如，pgvector 扩展 PostgreSQL 是所表达的关系；用带标签的有向边连接两个节点，是这种关系的一种表示。

文献也可以是被描述的对象。RDF 1.1 Primer 将文献、人物、物理对象和抽象概念都列为资源的例子；能够表示某个对象，不决定它应当进入哪个项目目录。例如，PostgreSQL 软件与描述它的一份手册可以分别具有身份，手册被引用一次，也不意味着需要建立受管理的书目记录。

本库的“实体词表”具有具体的收录职责：统一内容涉及的软件、组织等对象的名称与身份。为模型、规则或词表提供依据的文献，由参考文献目录管理；普通笔记参考资料可只保留标题与链接。文献的这种分工不否定它可以作为图谱中的实体，也不要求把所有可描述对象都收入实体词表。

属性的含义取决于图模型。在属性图中，节点和边可以带属性值对；值不能单独与属性名称混为一物。在 RDF 中，property 表示资源之间的关系，也不只表示字面值。`firstRelease` 和 `1996` 分别是属性名称与值的示例。

schema 描述图谱的高层结构，Hogan 区分语义、验证和涌现的 schema。本体可以参与表达语义结构，但 schema 不是本体在所有工程场景下的别名，也不必都采用 OWL。

推理依据已有知识及本体或规则中的条件取得进一步知识，或者判定蕴涵是否成立。例如，从某个对象属于 A、A 是 B 的子类，可以按规则判断该对象也属于 B。结果可以物化到图中，也可以通过查询重写取得；“新增一条边”不是推理的必要条件。

## 词表与图谱

列表、分类法和叙词表提供不同的词表组织方式，知识图谱提供图式知识表示。两者可以结合，但不是一条必须逐级升级的路线。

平铺的列表控制允许值；分类法和叙词表还组织概念之间的联系。知识图谱可以使用这些值与结构，但词表概念不能未经判断就变成现实对象，形式之间的 USE／UF 也不能直接当作任意实体别名关系。

例如，`PostgreSQL` 与 `postgres` 是否指同一对象，应由身份依据确定；词表中的上下位关系是否能表示为子类或实例关系，应按原关系含义判断。RT 表示相关关系，不能仅凭两个概念相关就推导出某种特定依赖、扩展或维护关系。

本库的[受控词表](controlled-vocabulary.md)和[词表映射](vocabulary-mapping.md)分别约束内部关系与跨体系对应。使用图模型不绕过这些语义与准入边界。

## 技术路线

| | RDF 路线（语义网） | 属性图路线（工程） |
|---|---|---|
| 数据模型 | 三元组；边不能直接带属性（需具体化或 RDF-star） | 节点和边都可带任意属性 |
| Schema | RDFS / OWL，形式化，可推理 | 通常无强制 schema，或用约束 |
| 查询语言 | SPARQL(W3C 标准) | Cypher;ISO/IEC 39075 GQL(2024 年发布的国际标准) |
| 标识 | 全球唯一 IRI，天然可跨库链接 | 库内 ID |
| 代表 | Wikidata、DBpedia、schema.org | Neo4j 及各类图数据库 |
| 与词表衔接 | 直接：SKOS 就是 RDF | 需自行映射 |

两条路线可以互转，选择取决于是否需要跨系统链接与形式推理（RDF）还是开发便利与性能（属性图）。

## 知识库用法

本库按实际检索与维护需要选择对象和关系。产品名称进入[实体词表](../design/model/entities.md)，设计依据文献进入[参考文献目录](../design/model/bibliography.md)，文献的获准用途由[来源用途登记](../design/model/sources-registry.md)管理。每个目录都有自己的准入条件；一个对象能够成为图谱节点，不构成收录理由。

工具与厂商或维护方的关联先沿用已定义的 `vendor`，例如 `uv` 的记录指向 `astral`。普通链接表示可跳转到另一份内容，不能据此推出开发、隶属、依赖或维护关系；这些关系需要分别明确含义和证据。遇到现有字段不能回答的实际问题时，再提出关系扩展，不预先规定必须增加多少种关系。

稳定 ID 与名称控制支持后续关联；关系类型的新增、适用对象和维护规则仍按项目决策权采纳。需要计算间接关系时，先明确已有事实、推导规则和结果用途，再决定是否使用脚本、查询或推理工具。是否采用本体或推理引擎取决于问题，不能由实体数量或目录分离自动推出。

## 权威来源

### 定义与综述

- Singhal, A. [*Introducing the Knowledge Graph: things, not strings*](https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/). Google Blog, 2012-05-16. 这个词流行起来的源头
- Hogan, A. et al. [*Knowledge Graphs*](https://arxiv.org/abs/2003.02320). ACM Computing Surveys 54(4), 2021. [DOI 10.1145/3447772](https://dl.acm.org/doi/10.1145/3447772). 本轮核对其 §2 图模型、§3.1 schema、§4.3 推理；[固定作者稿正文](https://arxiv.org/html/2003.02320v6)
- Ehrlinger, L., Wöß, W. [*Towards a Definition of Knowledge Graphs*](https://ceur-ws.org/Vol-1695/paper4.pdf). SEMANTiCS 2016, CEUR Vol-1695. 梳理了各家定义并提出“本体 + 推理”的定义

- [W3C RDF 1.1 Primer](https://www.w3.org/TR/rdf11-primer/)。§1、§3.1–3.2 说明可描述的资源包括文献，以及资源、关系和标识的分工；2026-09-08 核对。项目目录的收录边界见[参考文献分离决定](../decisions/source-bibliography-separation.md)，不由 RDF 规定。

### 标准

- [W3C RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/)(2014 Recommendation)。RDF 1.2 正在制定，目前为 [Candidate Recommendation](https://www.w3.org/TR/rdf12-concepts/)(2026-04)，主要增加 RDF-star 三元组项
- [W3C OWL 2 Web Ontology Language Overview](https://www.w3.org/TR/owl2-overview/)(2012 Recommendation, 2nd ed.)
- [W3C SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)(2013 Recommendation)
- [ISO/IEC 39075:2024 — Database languages — GQL](https://www.iso.org/standard/76120.html)。属性图查询语言国际标准，2024-04 发布，是 1987 年 SQL 之后 ISO 发布的第一个新数据库语言
- [ISO 25964-2:2013](https://www.iso.org/standard/53658.html)。叙词表与本体等其他词表的互操作，词表通往图谱的标准接口

### 图谱实例

- [Wikidata](https://www.wikidata.org/wiki/Wikidata:Introduction) —— 维基媒体的开放知识图谱，RDF 路线，实体 ID 形如 `Q192490`
- [schema.org](https://schema.org/) —— Google、Microsoft 等共同维护的网页结构化数据词表，是一个广泛使用的轻量本体
