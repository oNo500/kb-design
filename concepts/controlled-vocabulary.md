# 受控词表 (Controlled Vocabulary)

## 定义

受控词表是一套**预先定义、受管理**的标准化术语集合，用于描述和标引信息资源。核心目的是让同一概念始终用同一个词表达，消除自然语言的歧义，从而提高检索的查全率和查准率。

ANSI/NISO Z39.19 的正式定义（意译）：受控词表是一个经过明确枚举的术语列表，每个术语必须有非歧义、不冗余的定义；词表由权威机构（registration authority）维护。

## 解决的问题

| 问题 | 例子 | 受控词表的处理 |
|---|---|---|
| 同义词 | 汽车 / 轿车 / car / automobile | 选一个**首选词 (preferred term)**，其余作为**非首选词 / 入口词**指向它 |
| 多义词 | Apple（水果）vs Apple（公司） | 加限定词：`Apple (fruit)` / `Apple (company)` |
| 拼写变体、缩写 | USA / U.S.A. / United States | 统一为一个首选形式 |

## 词表的五种结构

“形式”指的是受控词表可以长成什么样的结构。同一个“受控”的理念，按投入多少结构，有几种不同的形态：从最简单的一张平铺列表，到带层级和关系网络的叙词表。往下一行，表达能力变强，维护成本也跟着涨。

Z39.19 正式定义了前四种；本体不算受控词表本身，但是它的自然延伸，所以一起列出。

| 形式 | 结构 | 能表达什么 | 知识库里的例子 |
|---|---|---|---|
| **术语表 / 代码表** (list) | 一张平铺的词列表 | 只有“允许的值是这些” | `status` 字段只能取 `draft` / `review` / `published` |
| **同义词环** (synonym ring) | 一组互相等价的词，没有谁是“正式的” | “这几个词算一回事” | 搜 `k8s` 也命中 `Kubernetes` |
| **分类法** (taxonomy) | 树：每个词有一个父节点 | 上下位关系 | `技术 > 后端 > 数据库 > PostgreSQL` |
| **叙词表** (thesaurus) | 网：首选词 + 等价词 + 上下位 + 相关词 | 下面“三类关系”全有 | `PostgreSQL`：别名 `pg`，上位 `关系型数据库`，相关 `pgvector` |
| **本体** (ontology) | 图：关系类型自定义，可推理 | 任意关系，如“依赖于”“由谁维护” | `服务A → 依赖 → PostgreSQL → 维护者 → 张三` |

对个人知识库，通常的实际落点是：**元数据字段用代码表，标签体系用分类法或轻量叙词表**，本体一般用不上。

## 词与词的三种关系

叙词表里，词和词之间只允许三种关系。每种关系有一对标准缩写（出自 ISO 25964 / Z39.19），词表条目里就用这些缩写标注。

### 等价关系 USE / UF

- `USE`：从别名指向正式名。读作“用 ×× 代替”
- `UF` (use for)：从正式名反向列出它的所有别名。读作“代替了 ××”

```
pg          USE  PostgreSQL        ← 你写 pg,系统告诉你应该用 PostgreSQL
PostgreSQL  UF   pg, postgres      ← PostgreSQL 这个正式名收编了 pg 和 postgres
```

作用：消灭同义词。一个概念只留一个首选词，其他写法都是入口，指过去。

### 层级关系 BT / NT

- `BT` (broader term)：上位词，范围更大的那个
- `NT` (narrower term)：下位词，范围更小的那个

```
PostgreSQL   BT  关系型数据库
关系型数据库  NT  PostgreSQL, MySQL, SQLite
```

作用：支撑分类和检索扩展。搜“关系型数据库”时可以自动把所有 NT 一起搜出来。

### 相关关系 RT

- `RT` (related term)：双向，A RT B 则 B RT A

```
PostgreSQL  RT  pgvector
```

作用：提示“看这个的人可能也要看那个”。它是兜底关系：凡是有关联但塞不进前两类的，都放这里。

### SKOS 对应属性

W3C SKOS 是用 RDF 表达这套关系的标准，属性名一一对应：

| 关系 | ISO / Z39.19 | SKOS |
|---|---|---|
| 等价 | USE / UF | `skos:prefLabel`（首选词）/ `skos:altLabel`（别名） |
| 层级 | BT / NT | `skos:broader` / `skos:narrower` |
| 相关 | RT | `skos:related` |

## 在知识库中的用法

- **标签体系**：标签从词表中选，新词需审核入表，而不是随意打 tag
- **元数据枚举值**：文档类型、状态、领域等字段的取值范围
- **实体规范化**：人名、产品名、系统名的唯一标准写法，便于跨文档关联
- **检索扩展**：搜索时把入口词映射到首选词，或沿层级向下扩展

**治理是关键**：谁能新增词、怎么审核、废弃词如何处理（deprecation 与映射）。词表的价值取决于维护流程，而非初始设计。

## 权威来源

### 标准

- [ISO 25964-1:2011 — Thesauri and interoperability with other vocabularies, Part 1: Thesauri for information retrieval](https://www.iso.org/standard/53657.html)
  取代 ISO 2788 和 ISO 5964;2022 年复审确认。
  ⚠️ 正在修订中：[ISO/FDIS 25964-1](https://www.iso.org/standard/86713.html)（标题改为 "...for information retrieval, management and use"）预计 2026 年出版，数据模型扩展到知识图谱、AI 等场景。
- [ISO 25964-2:2013 — Part 2: Interoperability with other vocabularies](https://www.iso.org/standard/53658.html)
- [NISO: ISO 25964 数据模型、XML schema 与 SKOS 映射](https://www.niso.org/schemas/iso25964)
- [ANSI/NISO Z39.19-2005 (R2010) — Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies](https://www.niso.org/publications/ansiniso-z3919-2005-r2010)
  美国标准，可免费下载 PDF。list / synonym ring / taxonomy / thesaurus 四层分类出自此。
- [GB/T 13190.1-2015 信息与文献 叙词表及与其他词表的互操作 第1部分：用于信息检索的叙词表](https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D7A385D3A7E05397BE0A0AB82A)（等同采用 ISO 25964-1）
- [GB/T 13190.2-2018 第2部分：与其他词表的互操作](https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D82DD2D3A7E05397BE0A0AB82A)
- [W3C SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/skos-reference/)(2009 Recommendation)

### 教材

- Harpring, Patricia. [*Introduction to Controlled Vocabularies: Terminology for Art, Architecture, and Other Cultural Works*](https://www.getty.edu/research/publications/electronic_publications/intro_controlled_vocab/). Getty Research Institute. 在线免费版，2023 修订。
- Lancaster, F.W. *Vocabulary Control for Information Retrieval*. 2nd ed. Information Resources Press, 1986.（奠基性著作，无官方在线版）
- Aitchison, J., Gilchrist, A., Bawden, D. *Thesaurus Construction and Use: A Practical Manual*. 4th ed. Europa Publications, 2000.

### 词表实例

- [MeSH (Medical Subject Headings)](https://www.nlm.nih.gov/mesh/) —— 美国国家医学图书馆
- [LCSH (Library of Congress Subject Headings)](https://id.loc.gov/authorities/subjects.html)
- [AAT (Getty Art & Architecture Thesaurus)](https://www.getty.edu/research/tools/vocabularies/aat/)
- [《汉语主题词表》](https://ct.istic.ac.cn/) —— 中国科学技术信息研究所
