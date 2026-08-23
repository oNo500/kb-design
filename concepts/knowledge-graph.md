# 知识图谱 (Knowledge Graph)

## 定义

知识图谱是把知识表示成一张图：节点是实体，边是实体之间带类型的关系。最小单位是一个三元组“主语 — 谓语 — 宾语”：

```
(PostgreSQL) —[是一种]→    (关系型数据库)
(PostgreSQL) —[维护者]→    (PostgreSQL Global Development Group)
(pgvector)   —[扩展了]→    (PostgreSQL)
```

成千上万条三元组连起来，就是一张图。

这个词没有 ISO 那样的正式标准定义。它是 Google 2012 年推广开的工业术语，口号是“things, not strings”——搜索的对象是事物本身，不是字符串。学术界最常引用的定义来自 Hogan 等人 2021 年的综述：**知识图谱是一个以图为载体的数据结构，用于积累和传达现实世界的知识，节点代表感兴趣的实体，边代表实体之间的关系**。Ehrlinger 与 Wöß 2016 年的定义则强调它“获取信息并把信息整合进本体，再用推理器推导出新知识”——即图谱 = 数据 + 本体 + 推理。

## 解决的问题

| 问题 | 例子 | 图谱的处理 |
|---|---|---|
| 知识散在文档里，机器读不出来 | “pgvector 是 PostgreSQL 的扩展”埋在某篇笔记第三段 | 抽成三元组，机器可查询 |
| 同一事物多个名字，关联断开 | `postgres` 和 `PostgreSQL` 两个标签各挂一堆笔记 | 一个实体一个 ID，名字是属性 |
| 只知道“有关”，不知道怎么有关 | 笔记 A 链接了笔记 B | 边带类型：`依赖` / `扩展` / `维护者` |
| 回答不了跨文档的问题 | “我所有依赖 PostgreSQL 的项目有哪些” | 沿边遍历，一条查询出结果 |
| 隐含关系没人写 | 没人写过“项目 X 间接依赖 libpq” | 按规则推理出新边 |

## 构成

| 部件 | 是什么 | 例子 |
|---|---|---|
| **本体 / Schema** | 定义有哪些实体类型、允许哪些关系类型 | 类型 `Software` `Person`；关系 `maintains` `dependsOn` |
| **实体** | 节点，有唯一 ID，名字只是标签 | `Q192490` 的 prefLabel 是 PostgreSQL，别名 pg、postgres |
| **关系** | 带类型的有向边 | `pgvector —extends→ PostgreSQL` |
| **属性** | 挂在实体（或边）上的字面值 | `PostgreSQL.firstRelease = 1996` |

本体是 schema，图谱是按 schema 填进去的实例数据。本体可以很轻（几种类型、几种关系）也可以很重（完整 OWL 公理）。

## 与受控词表的关系

两者是一条连续谱上的不同位置，不是竞争关系。词表管“叫什么”，图谱管“是什么、和谁有什么关系”。

```
代码表 → 分类法 → 叙词表 → 本体 → 知识图谱
 列表      树     网(3种关系)  schema   按 schema 填的数据
```

三个具体连接点：

1. **词表是图谱的命名层**。图谱里每个实体的规范名和别名，就是词表的等价关系 USE/UF 在做的事。没有词表，图谱里会出现 `PostgreSQL` 和 `postgres` 两个节点，关系挂到不同节点上，图就断了
2. **词表的层级是图谱的分类层**。BT/NT 搬进图谱就是 `subClassOf` / `instanceOf`，其他关系挂在这个分类层上
3. **图谱把词表的 RT 拆开**。叙词表里说不清的关联都塞进“相关”；图谱把它拆成有语义的关系：`PostgreSQL RT pgvector` 变成 `pgvector —扩展了→ PostgreSQL`

ISO 25964 的数据模型已经给了过渡的口子：概念有 ID、层级关系的 `role` 必填、允许自定义关系和自定义属性。详见 [ISO 25964 阅读笔记](../sources/iso-25964.md)。2026 年修订版把知识图谱明确列入适用场景。

## 两条技术路线

| | RDF 路线（语义网） | 属性图路线（工程） |
|---|---|---|
| 数据模型 | 三元组；边不能直接带属性（需具体化或 RDF-star） | 节点和边都可带任意属性 |
| Schema | RDFS / OWL，形式化，可推理 | 通常无强制 schema，或用约束 |
| 查询语言 | SPARQL(W3C 标准) | Cypher;ISO/IEC 39075 GQL(2024 年发布的国际标准) |
| 标识 | 全球唯一 IRI，天然可跨库链接 | 库内 ID |
| 代表 | Wikidata、DBpedia、schema.org | Neo4j 及各类图数据库 |
| 与词表衔接 | 直接：SKOS 就是 RDF | 需自行映射 |

两条路线可以互转，选择取决于是否需要跨系统链接与形式推理（RDF）还是开发便利与性能（属性图）。

## 在知识库中的用法

诚实地说，完整的知识图谱对个人知识库通常是过度设计。实际有价值的是中间地带，而且不是全有或全无：

1. **先做词表**：实体有唯一 ID 和规范名、别名、分类。这是后面一切的前提，无论如何要做
2. **给链接加类型**:元数据里写 `depends_on: [PostgreSQL]` 而不是只在正文 `[[PostgreSQL]]`。这已经是图谱的最小形态——Obsidian 式的双链是一张只有“链接”一种边的图，加类型就是升级
3. **关系类型从少到多**：先定 3–5 种最常问的（依赖、属于、维护者、参考），用一段时间，看是否真的回答出了泛链接回答不了的问题，有再加
4. **推理最后考虑**：传递闭包（“间接依赖”）之类简单规则可以用脚本做；OWL 级推理对个人 KB 几乎用不上

治理提醒：关系类型和实体类型一样需要受控——谁能新增关系类型、定义写在哪、废弃怎么处理。否则 `depends_on` / `dependsOn` / `依赖` 三种写法并存，图又断了。

## 权威来源

### 定义与综述

- Singhal, A. [*Introducing the Knowledge Graph: things, not strings*](https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/). Google Blog, 2012-05-16. 这个词流行起来的源头
- Hogan, A. et al. [*Knowledge Graphs*](https://arxiv.org/abs/2003.02320). ACM Computing Surveys 54(4), 2021. [DOI 10.1145/3447772](https://dl.acm.org/doi/10.1145/3447772). 目前最常引用的学术综述，arXiv 版免费
- Ehrlinger, L., Wöß, W. [*Towards a Definition of Knowledge Graphs*](https://ceur-ws.org/Vol-1695/paper4.pdf). SEMANTiCS 2016, CEUR Vol-1695. 梳理了各家定义并提出“本体 + 推理”的定义

### 标准

- [W3C RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/)(2014 Recommendation)。RDF 1.2 正在制定，目前为 [Candidate Recommendation](https://www.w3.org/TR/rdf12-concepts/)(2026-04)，主要增加 RDF-star 三元组项
- [W3C OWL 2 Web Ontology Language Overview](https://www.w3.org/TR/owl2-overview/)(2012 Recommendation, 2nd ed.)
- [W3C SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)(2013 Recommendation)
- [ISO/IEC 39075:2024 — Database languages — GQL](https://www.iso.org/standard/76120.html)。属性图查询语言国际标准，2024-04 发布，是 1987 年 SQL 之后 ISO 发布的第一个新数据库语言
- [ISO 25964-2:2013](https://www.iso.org/standard/53658.html)。叙词表与本体等其他词表的互操作，词表通往图谱的标准接口

### 图谱实例

- [Wikidata](https://www.wikidata.org/wiki/Wikidata:Introduction) —— 维基媒体的开放知识图谱，RDF 路线，实体 ID 形如 `Q192490`
- [schema.org](https://schema.org/) —— Google、Microsoft 等共同维护的网页结构化数据词表，是一个广泛使用的轻量本体
