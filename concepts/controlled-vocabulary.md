# 受控词表 (Controlled Vocabulary)

## 定义

受控词表是一套**预先定义、受管理**的标准化术语集合,用于描述和标引信息资源。核心目的是让同一概念始终用同一个词表达,消除自然语言的歧义,从而提高检索的查全率和查准率。

ANSI/NISO Z39.19 的正式定义(意译):受控词表是一个经过明确枚举的术语列表,每个术语必须有非歧义、不冗余的定义;词表由权威机构(registration authority)维护。

## 解决什么问题

| 问题 | 例子 | 受控词表的处理 |
|---|---|---|
| 同义词 | 汽车 / 轿车 / car / automobile | 选一个**首选词 (preferred term)**,其余作为**非首选词 / 入口词**指向它 |
| 多义词 | Apple(水果)vs Apple(公司) | 加限定词:`Apple (fruit)` / `Apple (company)` |
| 拼写变体、缩写 | USA / U.S.A. / United States | 统一为一个首选形式 |

## 形式(按结构复杂度递增)

Z39.19 把受控词表分为四个层级,本体虽不在其范围内但常作为延伸列出:

| 类型 | 特点 | 例子 |
|---|---|---|
| 术语表 / 代码表 (list) | 扁平列表,无层级 | ISO 3166 国家代码、字段枚举值 |
| 同义词环 (synonym ring) | 一组等价词,无首选词 | 搜索引擎同义扩展 |
| 分类法 (taxonomy) | 树形层级(上位 / 下位) | 图书分类法、电商类目树 |
| 叙词表 (thesaurus) | 层级 + 等价 + 相关三类关系 | MeSH、AAT、《汉语主题词表》 |
| 本体 (ontology) | 任意自定义关系 + 推理规则 | SNOMED CT、schema.org |

## 三类关系(ISO 25964 / Z39.19 的标准符号)

- **等价关系**:`USE` / `UF` (use for) —— 非首选词 → 首选词
- **层级关系**:`BT` (broader term) / `NT` (narrower term)
- **相关关系**:`RT` (related term) —— 相关但非层级

在 W3C SKOS 里对应为 `skos:prefLabel` / `skos:altLabel`、`skos:broader` / `skos:narrower`、`skos:related`。

## 在知识库设计中的体现

- **标签体系**:标签从词表中选,新词需审核入表,而不是随意打 tag
- **元数据枚举值**:文档类型、状态、领域等字段的取值范围
- **实体规范化**:人名、产品名、系统名的唯一标准写法,便于跨文档关联
- **检索扩展**:搜索时把入口词映射到首选词,或沿层级向下扩展

**治理是关键**:谁能新增词、怎么审核、废弃词如何处理(deprecation 与映射)。词表的价值取决于维护流程,而非初始设计。

## 权威来源

### 标准

- [ISO 25964-1:2011 — Thesauri and interoperability with other vocabularies, Part 1: Thesauri for information retrieval](https://www.iso.org/standard/53657.html)
  取代 ISO 2788 和 ISO 5964;2022 年复审确认。
  ⚠️ 正在修订中:[ISO/FDIS 25964-1](https://www.iso.org/standard/86713.html)(标题改为 "...for information retrieval, management and use")预计 2026 年出版,数据模型扩展到知识图谱、AI 等场景。
- [ISO 25964-2:2013 — Part 2: Interoperability with other vocabularies](https://www.iso.org/standard/53658.html)
- [NISO: ISO 25964 数据模型、XML schema 与 SKOS 映射](https://www.niso.org/schemas/iso25964)
- [ANSI/NISO Z39.19-2005 (R2010) — Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies](https://www.niso.org/publications/ansiniso-z3919-2005-r2010)
  美国标准,可免费下载 PDF。list / synonym ring / taxonomy / thesaurus 四层分类出自此。
- [GB/T 13190.1-2015 信息与文献 叙词表及与其他词表的互操作 第1部分:用于信息检索的叙词表](https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D7A385D3A7E05397BE0A0AB82A)(等同采用 ISO 25964-1)
- [GB/T 13190.2-2018 第2部分:与其他词表的互操作](https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D82DD2D3A7E05397BE0A0AB82A)
- [W3C SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/skos-reference/)(2009 Recommendation)

### 教材 / 参考资料

- Harpring, Patricia. [*Introduction to Controlled Vocabularies: Terminology for Art, Architecture, and Other Cultural Works*](https://www.getty.edu/research/publications/electronic_publications/intro_controlled_vocab/). Getty Research Institute. 在线免费版,2023 修订。
- Lancaster, F.W. *Vocabulary Control for Information Retrieval*. 2nd ed. Information Resources Press, 1986.(奠基性著作,无官方在线版)
- Aitchison, J., Gilchrist, A., Bawden, D. *Thesaurus Construction and Use: A Practical Manual*. 4th ed. Europa Publications, 2000.

### 实际词表范例

- [MeSH (Medical Subject Headings)](https://www.nlm.nih.gov/mesh/) —— 美国国家医学图书馆
- [LCSH (Library of Congress Subject Headings)](https://id.loc.gov/authorities/subjects.html)
- [AAT (Getty Art & Architecture Thesaurus)](https://www.getty.edu/research/tools/vocabularies/aat/)
- [《汉语主题词表》](https://ct.istic.ac.cn/) —— 中国科学技术信息研究所
