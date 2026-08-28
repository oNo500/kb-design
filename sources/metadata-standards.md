# 元数据标准

## 阅读范围

本笔记只记录实际打开的标准发布者页面与正文范围，核对日期均为 2026-08-29。表中的“正文已读”不表示通读整份规范。本笔记保留规范中的英文术语和属性名；中文说明不登记中英对照术语。

| 材料 | 版本状态 | 正文已读 | 未读 |
|---|---|---|---|
| [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) | 标识版本日期为 2020-01-20；DCMI Recommendation | 文档元数据；第 1 节对术语属性的说明；第 2 节 `dcterms:source` 条目 | 其余术语条目、版本历史、链接的 RDF schema 和 `More details` 页面 |
| [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/) | W3C Recommendation，2013-04-30；页面说明英文版是唯一规范性版本 | 文档状态；`prov:wasDerivedFrom`、`prov:hadPrimarySource`、`prov:wasRevisionOf`、`prov:invalidatedAtTime` 和 `prov:wasInvalidatedBy` 的属性条目及其列出的关系 | 其余类、属性、示例和附录；PROV 系列其他文档；勘误页 |
| [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/skos-reference/) | W3C Recommendation，2009-08-18 | 文档状态与摘要；第 10.1 至 10.4 节；第 10.6.1、10.6.3、10.6.7 和 10.6.8 节中与映射属性边界有关的内容 | 第 10 节其余说明和非目标示例；其他各章、SKOS Primer、SKOS-XL 与勘误页 |
| [BCP 47](https://www.rfc-editor.org/info/bcp47/) | RFC Editor 当前页面列出 RFC 4647 与 RFC 5646，两者状态均为 Best Current Practice | BCP 信息页；[RFC 5646: Tags for Identifying Languages](https://www.rfc-editor.org/rfc/rfc5646.html) 的标题、摘要、第 1 节、第 2 节、第 2.1 节、第 2.1.1 节及第 2.2 节中与 subtag 类型和顺序有关的段落；[RFC 4647: Matching of Language Tags](https://www.rfc-editor.org/rfc/rfc4647.html) 的标题、摘要、第 1 节、第 2 节中 `language-range` 的语法边界，以及第 3 节和第 3.1 节的 matching 概览 | 两份 RFC 的其余正文、附录和勘误记录；IANA Language Subtag Registry 的实际记录 |

## 元数据来源

[DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) 将 `dcterms:source` 标识为属性，URI 为 `http://purl.org/dc/terms/source`。定义原文是“A related resource from which the described resource is derived.”。条目说明，被描述的资源可以全部或部分派生自相关资源；该属性拟用于非字面值，并建议用 URI 或符合正式标识系统的字符串标识相关资源。

`dcterms:source` 条目没有列出 Domain 或 Range。页面第 1 节说明 Domain 和 Range 只在适用时列为附加属性，因此不能为该条目补出页面没有提供的定义域或值域。条目实际列出的关系是：`dcterms:source` 是 `dc:source`（`http://purl.org/dc/elements/1.1/source`）和 `dcterms:relation` 的 subproperty。

这些内容界定的是被描述资源与派生所据相关资源之间的属性语义。它们没有把 `dcterms:source` 定义为逐值证据记录，也没有规定本项目应为哪些值保存何种依据。

## 派生关系

[PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/) 对目标关系给出以下边界。

| PROV-O 术语 | 规范中的边界 | 形式关系 |
|---|---|---|
| `prov:wasDerivedFrom` | derivation 包括一个 Entity 到另一个 Entity 的 transformation、产生新 Entity 的 update，或基于已有 Entity 构造新 Entity | Domain 和 Range 都是 `prov:Entity`；是 `prov:wasInfluencedBy` 的 subproperty；更具体的 subproperty 包括 `prov:hadPrimarySource`、`prov:wasQuotedFrom` 和 `prov:wasRevisionOf` |
| `prov:wasRevisionOf` | resulting Entity 是 original Entity 的 revised version，并含有 original 的 substantial content；revision 是 derivation 的特例 | Domain 和 Range 都是 `prov:Entity`；是 `prov:wasDerivedFrom` 的 subproperty |
| `prov:hadPrimarySource` | 对某一 topic，相关 Entity 由在研究发生时对该 topic 有 direct experience and knowledge 的 Agent 产生，且不借助 hindsight；规范同时说明判定可能依赖解释，并应遵守应用领域接受的惯例 | 从 secondary `prov:Entity` 指向 earlier primary `prov:Entity`；是 `prov:wasDerivedFrom` 的 subproperty |
| `prov:wasInvalidatedBy` | invalidation 是 Activity 使既有 Entity 开始 destruction、cessation 或 expiry；此后该 Entity 不再可用，任何 generation 或 usage 都先于 invalidation | Domain 是 `prov:Entity`，Range 是 `prov:Activity`；是 `prov:wasInfluencedBy` 的 subproperty |

`prov:invalidatedAtTime` 记录 Entity 被 invalidated 的时间；它与 `prov:wasInvalidatedBy` 一样采用上述 invalidation 边界。PROV-O 没有把 `prov:wasInvalidatedBy` 列为 `prov:wasDerivedFrom` 的 subproperty，也不能由“页面打不开”“来源有新版”或本地状态值直接推出 invalidation。

日常的“来自”没有说明是否发生了 transformation、产生新 Entity 的 update 或基于已有 Entity 的 construction；日常的“更新”也没有说明 resulting Entity 是否保留 original 的 substantial content。只有实际关系满足规范边界时，才能用相应 PROV-O 属性描述。

## 概念映射

[SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/skos-reference/) 第 10 节列出 `skos:closeMatch`、`skos:exactMatch`、`skos:broadMatch`、`skos:narrowMatch` 和 `skos:relatedMatch`。这些属性用于表示不同 concept scheme 中 SKOS Concept 之间、内在于双方含义的 mapping link；第 10.6.1 节把“用于不同 concept scheme”说明为惯例。

各属性的语义边界如下。

- `skos:broadMatch` 与 `skos:narrowMatch` 表示 hierarchical mapping link，二者互为 inverse。
- `skos:relatedMatch` 表示 associative mapping link。
- `skos:closeMatch` 表示两个 Concept 足够相似，可在某些 information retrieval application 中互换；它没有被声明为 transitive。
- `skos:exactMatch` 表示有高度把握认为两个 Concept 可在广泛的 information retrieval application 中互换；它是 `skos:closeMatch` 的 subproperty。

形式上，`skos:mappingRelation` 是 `skos:semanticRelation` 的 subproperty；`skos:closeMatch`、`skos:broadMatch`、`skos:narrowMatch` 和 `skos:relatedMatch` 是 `skos:mappingRelation` 的 subproperty。`skos:broadMatch`、`skos:narrowMatch`、`skos:relatedMatch` 还分别是 `skos:broader`、`skos:narrower`、`skos:related` 的 subproperty。

`skos:relatedMatch`、`skos:closeMatch` 和 `skos:exactMatch` 是 symmetric property；只有 `skos:exactMatch` 被声明为 transitive。`skos:exactMatch` 与 `skos:broadMatch`、`skos:relatedMatch` disjoint；结合 symmetry 与 broad/narrow 的 inverse 关系，它也与 `skos:narrowMatch` disjoint。SKOS 没有为 `skos:exactMatch` 或 `skos:closeMatch` 规定把它们同 broad 或 related mapping 串接起来的 subproperty chain，因此这种串接不产生新的 broad 或 related mapping。

这些属性描述 Concept 之间的关系及其形式后果。词形相同、译文相似、两个记录都被项目采用，或一个标准采用另一个标准，都不会由 SKOS 自动推出任何一种 mapping property。

## 语言标签

[RFC 5646: Tags for Identifying Languages](https://www.rfc-editor.org/rfc/rfc5646.html) 是 2009-09 发布的 Best Current Practice，并取代 RFC 4646。它规定 language tag 的 structure、content、construction 和 semantics，用于需要指明 information object 所用语言的场景。第 2 节把用途限定为帮助标识人类交流中的 spoken、written、signed 或其他方式表达的语言；programming language 不在该范围内。

第 2.1 节的 ABNF 把 `Language-Tag` 分为普通 `langtag`、`privateuse` 和 `grandfathered` 三种。普通 `langtag` 以 `language` 开始；`language` 内可带 `extlang`，其后依次可有 `script`、`region`、一个或多个 `variant`、一个或多个 `extension`，最后可有 `privateuse`。subtag 以连字符 `-` 分隔，只使用 ASCII 字母或数字；单个 subtag 最长 8 个字符，tag 中不允许空白。tag 与 subtag 的比较不区分大小写，大小写惯例本身不携带含义。

RFC 5646 还区分 well-formed 与 valid：符合第 2.1 节 ABNF 只构成 well-formed；valid 还要求 grandfathered tag 在固定清单中，或其中的 primary language、extended language、script、region 和 variant subtag 出现在特定日期的 IANA Language Subtag Registry，并满足重复项等条件。这个区别没有规定本库应允许哪些 tag，也没有规定保存 tag 的字段形状。

[BCP 47](https://www.rfc-editor.org/info/bcp47/) 同时包含 [RFC 4647: Matching of Language Tags](https://www.rfc-editor.org/rfc/rfc4647.html)。RFC 4647 中的 `language-range` 用于表达语言偏好并同 language tag 比较，不是 information object 上的 language tag。basic `language-range` 使用与 RFC 3066 language tag 相同的语法，或整体为通配符 `*`；extended `language-range` 可以在 subtag 位置使用 `*`。basic `language-range` 也不要求本身是 well-formed 或经 IANA Registry 验证的 language tag。matching 中，filtering 返回零个或多个 language tag，lookup 返回一个结果；Basic Filtering、Extended Filtering 和 Lookup 是不同机制。RFC 5646 的 tag 构造与 RFC 4647 的 range 和 matching 回答不同问题，两份 RFC 不提供把它们视为同一对象或同一判断的依据。

## 适用边界

外部词汇能提供关系语义和形式特性，不能替本项目作以下决定。

| 项目问题 | 外部材料不能决定的内容 |
|---|---|
| `basis` | DCMI 和 PROV-O 没有定义本项目的 `basis`，也不决定某个具体值为何成立、依据应放在哪里或如何重复定位 |
| 来源充分性 | `dcterms:source` 与 PROV-O 关系不决定一项断言需要几份来源、何种来源、何种定位粒度或何时证据充分 |
| `source` 选择 | 相关、引用、派生、revision 和 primary source 不是同义关系；外部定义不替项目判断某个实际对象满足哪一关系 |
| `match` 选择 | SKOS 规定属性语义和形式后果，但不根据词形、翻译、来源身份或项目采用状态自动选择 exact、close、broad、narrow 或 related match |
| 批准状态 | 外部关系成立不表示项目已经批准采用；标准之间的采用关系也不自动证明具体术语或 Concept 等同 |
| 字段结构 | 四份材料都不规定本地 YAML 的字段名、嵌套、基数、引用形状、必填性或存储位置 |
| 语言政策 | RFC 5646 不决定本库允许的 tag 集合、默认语言或 fallback；RFC 4647 也不替项目选择 matching 机制 |
| 失效流程 | PROV-O 的 invalidation 语义不等于链接故障、来源换版或项目废弃状态，也不规定复核、批准、替代、阻断或历史保留流程 |

## 未读范围

- DCMI 页面除文档元数据、第 1 节术语属性说明和 `dcterms:source` 条目外未核对；版本历史、RDF schema 与 `More details` 页面未读。
- PROV-O 除文档状态和本笔记列出的目标属性条目外未通读；PROV-DM、PROV-CONSTRAINTS、PROV-DC 等 PROV 系列文档及 PROV-O 勘误页未读。
- SKOS Reference 除文档状态、摘要和本笔记列出的第 10 节范围外未通读；SKOS Primer、SKOS-XL、其他章节和勘误页未读。
- RFC 5646 只读到本笔记记录的用途、ABNF、格式、subtag 顺序和 well-formed/valid 边界；注册流程、维护程序、完整使用指南、canonicalization、安全章节、附录和勘误记录未读。
- RFC 4647 只读到 `language-range` 语法边界与 matching 机制概览；各 matching 算法的完整步骤、默认值、协议考虑、安全章节、参考文献和勘误记录未读。
- IANA Language Subtag Registry 的实际记录未核对；本笔记不据 RFC 示例声明任何具体 language tag 或 subtag 当前有效。
