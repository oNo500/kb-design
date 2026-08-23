# 术语表 (Glossary)

本库用到的术语,每条一句定义和出处。文章之间的关系见 [概念文索引](README.md)。

出处缩写:

| 缩写 | 来源 |
|---|---|
| ISO | ISO 25964-1:2011,后接条款号 |
| ISO-2 | ISO 25964-2:2013,后接条款号 |
| Z | ANSI/NISO Z39.19-2005 (R2010),后接条款号 |
| SKOS | W3C SKOS Reference,2009 |
| KG | Hogan et al., *Knowledge Graphs*, 2021 |
| 自定 | 本库自定,无外部来源 |

## 词表的类型

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 受控词表 | controlled vocabulary | 规定好的词、标题或代码列表,每项代表一个概念 | ISO 2.12;Z 4.1 |
| 术语表 / 代码表 | list, pick list | 有限的一组词,按字母或其他明显逻辑排列,无关系 | Z 5.4.1 |
| 同义词环 | synonym ring | 一组检索时视为等价的词;只用于检索,不用于标引 | Z 5.4.2 |
| 分类法 | taxonomy | 全部由首选词构成、以层级或多层级连接的受控词表 | Z 5.4.3 |
| 分类表 | classification scheme | 按分类排列的概念及先组组合的表 | ISO 2.6 |
| 叙词表 | thesaurus | 按已知顺序排列、用标准化关系指示符清楚显示词间关系的受控词表 | Z 5.4.4 |
| 本体 | ontology | 对概念化的明确规范:领域里有哪些类型的实体、允许哪些关系 | Gruber 1993 |
| 知识图谱 | knowledge graph | 以图为载体积累和传达现实世界知识的数据结构,节点为实体,边为关系 | KG |

## 基本单位

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 概念 | concept | 思维单元;独立于表达它的词而存在 | ISO 2.11 |
| 词 | term | 表达概念的词或短语 | ISO 2.61 |
| 首选词 / 叙词 | preferred term, descriptor | 标引时用来代表概念的词 | ISO 2.45 |
| 非首选词 / 非叙词 | non-preferred term | 不用于标引、只作入口的词 | ISO 2.39 |
| 入口词 | entry term, lead-in term | 引导用户找到可用词的词;叙词表里即非首选词 | ISO 2.16 |
| 隐藏标签 | hidden label | 不显示但可检索的非首选词,如拼写错误 | ISO 数据模型 `hidden`;SKOS `hiddenLabel` |
| 标识符 | identifier | 概念、词或其他实体的唯一标识 | ISO 2.25 |
| 限定词 | qualifier | 加在词后区分同形异义的定义性词,如 `Apple (company)` | Z 4.1 |
| 同形异义词 | homograph | 写法相同、意义不同的词 | ISO 2.24 |
| 准同义词 | quasi-synonym | 日常意义不同但词表中视为同一概念的词 | ISO 2.47 |
| 复合词 | compound term | 可拆成多个成分的词 | ISO 2.9 |
| 复合概念 | complex concept | 由多个简单概念组成的概念;是否拆分见 ISO §7 | ISO §7 |
| 领域 | domain | 词表覆盖的主题范围 | — |
| 内容对象 | content object | 被标引的东西:文档、图像、人、组织、实物 | Z 4.1;ISO 2.15 document |

## 关系

| 术语 | 符号 | 定义 | 出处 |
|---|---|---|---|
| 等价关系 | USE / UF | 两个词代表同一概念;一个定为首选,其余非首选 | ISO 2.18 |
| 复合等价 | USE+ / UF+ | 一个词由另一语境中两个以上词表示 | ISO 2.8 |
| 层级关系 | BT / NT | 一个概念的范围完全落在另一个之内 | ISO 2.23 |
| 属种关系 | BTG / NTG | 层级的一种:是一种 (is-a) | ISO §10.2 |
| 整部关系 | BTP / NTP | 层级的一种:是一部分 (part-of) | ISO §10.2 |
| 实例关系 | BTI / NTI | 层级的一种:是实例 (instance-of) | ISO §10.2 |
| 相关关系 | RT | 非层级但语义联系强 | ISO 2.2 |
| 自定义关系 | — | 词表自行定义的关系类型 | ISO §10.4 |
| 聚合关系 | paradigmatic | 概念固有的关系,与具体文档无关;叙词表只收这类 | ISO 2.41 |
| 组合关系 | syntagmatic | 因在某文档中同时出现而产生的关系;不进叙词表 | ISO §4.3 |
| 单层级 | monohierarchy | 每个概念只有一个直接上位 | ISO 2.34 |
| 多层级 | polyhierarchy | 一个概念可有多个直接上位 | ISO 2.42 |
| 互反 | reciprocal | 关系必须双向登记:A BT B 则 B NT A | Z 5.4.4 |

## 结构

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 分面 | facet | 同一内在类别的概念分组:对象、材料、动作、地点、时间 | ISO 2.20 |
| 分面分析 | facet analysis | 把领域分解成概念、按分面分组、按划分特征细分 | ISO 2.21;Z 5.3.4 |
| 划分特征 | characteristic of division | 把一个概念细分成一组下位概念所依据的属性 | ISO 2.4 |
| 树 / 层级 | hierarchy | 按 BT/NT 排出的上下位结构 | ISO §10.2 |
| 节点 | node | 树上的一个位置 | — |
| 顶层概念 | top concept | 树的根 | ISO 数据模型 |
| 节点标签 | node label | 树里说明分组依据的标签,非词,不能标引 | ISO 2.38 |
| 数组 | array | 一组同级概念 | ISO 2.1 |
| 概念组 / 分组 | concept group | 按用途圈出的一批概念,可跨树、可嵌套 | ISO 数据模型 |
| 微词表 | micro-thesaurus | 概念组的一种:大词表的子领域切片 | ISO 数据模型 |
| 辅助表 / 复分表 | auxiliary table | 分类法中单独列出的通用维度表(地区、时间、形式),拼接到主表号后 | 分类法实践,未核原文 |
| 组配号 | synthesized notation | 主表号与辅助表号拼接而成的号码 | ISO 2.22 facet indicator |
| 先组 | pre-coordination | 建表或标引时就组合概念 | ISO 2.44 |
| 后组 | post-coordination | 检索时才组合首选词 | ISO 2.43 |
| 属性 / 维度 | attribute, dimension | 元数据层:文档的一个字段。不是词表结构,但 Z39.19 图 4 也把它叫 facet | Z 5.3.4 |

## 注释与生命周期

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 范围注释 | scope note | 说明词的覆盖范围和用法限制的注释 | ISO 5.2;Z 4.1 |
| 定义 | definition | 词的定义,ISO 中挂在词上 | ISO 数据模型 |
| 历史注释 | history note | 入表日期、变更记录、旧形式及有效期 | Z 11.3.2.2 |
| 编辑注释 | editorial note | 给编辑看的内部注释 | ISO 数据模型 |
| 候选词 | candidate term, provisional term | 提出但未走完审批的词 | Z 11.1.6 |
| 未标引词 | unassigned term | 为补全层级而收、尚未用于标引的词 | Z 11.1.8 |
| 废弃词 | deprecated term | 不再用于标引、保留供检索并指向替代词的词 | Z 11.3.2.1 |
| 孤儿词 | orphan term | 没有任何层级或相关关系的词 | Z 11.4.4 |
| 状态 | status | 词或概念的生命周期状态 | ISO 数据模型 |
| 版本历史 | version history | 词表整体的版本记录 | ISO 数据模型 |

## 建设与治理

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 依据 | warrant | 一个词有资格进词表的理由 | Z 5.3.5 |
| 文献依据 | literary warrant | 词是领域文献里实际通行的说法 | Z 5.3.5.1 |
| 组织依据 | organizational warrant | 词是使用组织偏好的形式 | Z 5.3.5.2 |
| 用户依据 | user warrant | 词是用户检索时实际用的说法 | Z 5.3.5.3 |
| 自上而下 / 自下而上 | top down / bottom up | 委员会法的两个方向;新建词表优先前者 | Z 11.1.3.1 |
| 演绎法 / 归纳法 | deductive / inductive | 经验法的两种:先收集后控制 / 从头控制 | Z 11.1.3.2 |
| 词汇控制 | vocabulary control | 让标引者和检索者对同一概念用同一个词 | ISO §4.2;Z 1.1 |
| 标引 | indexing | 分析文档主题、识别概念、分配标引词 | ISO 2.27 |
| 标引词 | index term | 分配给文档的词;keyword、tag 含义更宽 | ISO 2.26 |
| 查全率 / 查准率 | recall / precision | 检索效果的两个指标;词表对两者都有正面影响 | Z 5.3.6 |
| 互操作性 | interoperability | 系统间交换并使用信息的能力 | ISO 2.29 |
| 来源分级 | de-jure / de-facto / vendor / archival | 引证来源按变更方式分档 | 自定;[design/sources.md](../design/sources.md) |

## 词表间映射

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 映射 | mapping | 一个词表中的概念与另一个词表中一个或多个概念之间的关系;通常有方向 | ISO-2 3.41 |
| 对照表 | crosswalk | 两个以上词表之间概念映射的表 | ISO-2 3.24 |
| 源词表 / 目标词表 | source / target vocabulary | 映射的起点 / 终点 | ISO-2 3.72, 3.82 |
| 等价映射 | equivalence mapping | 目标概念与源概念范围相同 | ISO-2 3.29 |
| 精确 / 不精确 / 部分等价 | exact / inexact / partial equivalence | 等价的三个程度 | ISO-2 §11 |
| 层级映射 | hierarchical mapping | 目标概念比源概念宽或窄 | ISO-2 §9 |
| 相关映射 | associative mapping | 有关但非等价非层级 | ISO-2 §10 |
| 区分式映射 | differentiated mapping | 标明映射类型和等价程度的映射方法 | ISO-2 3.26 |
| 中心辐射 | hub structure | 所有词表映射到一个中心词表的结构模型 | ISO-2 §6 |
| exactMatch / closeMatch | — | SKOS 的精确 / 不精确等价;前者传递,后者不传递 | SKOS §10 |
| broadMatch / narrowMatch / relatedMatch | — | SKOS 的层级 / 相关映射 | SKOS §10 |

## 知识体系

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 知识体系 | body of knowledge, BoK | 一个学科或职业公认知识范围的结构化清单 | SWEBOK;ISO/IEC TR 19759 |
| 知识领域 | knowledge area, KA | 知识体系的主要区域 | SWEBOK;CS2023 |
| 知识单元 | knowledge unit, KU | 知识领域内的主题簇 | CS2023 |
| 主题 | topic | 知识单元内的具体知识点,标核心或选修 | CS2023 |
| 普遍接受的知识 | generally accepted knowledge | 多数项目多数时候适用且广泛认同的知识;知识体系只收这类 | SWEBOK |

## 知识图谱

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 三元组 | triple | 主语 — 谓语 — 宾语,图的最小单位 | W3C RDF 1.1 |
| 实体 | entity | 图的节点,有唯一 ID | KG |
| 关系 | relation, edge | 带类型的有向边 | KG |
| 属性 | property | 挂在实体或边上的字面值 | KG |
| Schema | schema | 本体在工程语境的叫法:类型与关系的定义 | — |
| 推理 | reasoning, inference | 按规则从已有边推出新边 | KG |
| RDF | Resource Description Framework | W3C 的三元组数据模型 | W3C RDF 1.1 |
| RDFS / OWL | — | RDF 上的 schema 语言 / 本体语言 | W3C |
| SPARQL | — | RDF 查询语言 | W3C SPARQL 1.1 |
| SKOS | Simple Knowledge Organization System | 用 RDF 表达词表的 W3C 标准 | W3C SKOS |
| 属性图 | property graph | 节点和边都可带属性的图模型 | ISO/IEC 39075 |
| Cypher / GQL | — | 属性图查询语言;GQL 是 2024 年的 ISO 标准 | ISO/IEC 39075:2024 |

## 引用的标准与文献

| 名称 | 是什么 |
|---|---|
| ISO 25964-1:2011 / -2:2013 | 叙词表国际标准,见 [笔记](../sources/iso-25964.md) |
| GB/T 13190.1-2015 / .2-2018 | 等同采用 ISO 25964 的国标 |
| ANSI/NISO Z39.19-2005 (R2010) | 美国受控词表标准,全文免费 |
| ISO 704 | 术语工作原则与方法,Wüster 理论的标准化版本;未核对 |
| W3C SKOS / RDF / OWL / SPARQL | 语义网标准族 |
| ISO/IEC 39075:2024 GQL | 属性图查询语言标准 |
| Cutter (1876) | 字典式目录规则,主题标目「一主题一词」的源头;未核对 |
| Dewey (1876) | 十进分类法;未核对 |
| Ranganathan (1933) | 冒号分类法,分面分析的源头;经 Z39.19 §5.3.4 转述 |
| Wüster (1931) | 普通术语学理论,「概念先于词」;未核对 |
| Gruber (1993) | 计算机领域本体的定义;未核对 |
| Hogan et al. (2021) | 知识图谱综述,[arXiv](https://arxiv.org/abs/2003.02320) |
| Ehrlinger & Wöß (2016) | 知识图谱定义梳理,[CEUR](https://ceur-ws.org/Vol-1695/paper4.pdf) |
