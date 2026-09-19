# 受控词表指南 (ANSI/NISO Z39.19)

本文记录材料身份、原文位置及核读边界，供核对标准事实；项目规则的采用以相应决定为准。

## 材料身份

本记录采用 ANSI/NISO Z39.19-2005 (R2010)，英文题名为 Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies。出版页标示日期 2010-05-13，DOI 为 10.3789/ansi.niso.z39.19-2005R2010；它面向单语受控词表。[NISO 出版页](https://www.niso.org/publications/ansiniso-z3919-2005-r2010)

2026-09-19 从 NISO 官方地址取得并在内存核读的 PDF 共 184 页，原文身份与内容摘要记录在[核对记录](../../../work/reviews/2026-09-19-vocabulary-standard-boundary.json)。正文引用使用其印刷页码；没有把章节目录或本地转述当作已读正文。[官方 PDF](https://groups.niso.org/higherlogic/ws/public/download/12591/z39-19-2005r2010.pdf)

标题中的中文用于识别阅读材料，不据此登记新的中文标准名称。

## 阅读范围

核读记录按日期区分，取得全文不等于逐条读完全文。

| 日期 | 材料与实际核读范围 |
|---|---|
| 2026-08-29 | 出版页及项目出版页的身份、摘要、版本说明与入口；PDF 封面、前言、目录，§5.3.5、§5.4、§11.1.1–§11.1.8、§11.3–§11.3.2.2、§11.4.4–§11.4.5；修订状态页的项目名称 |
| 2026-09-19 | 重新核对出版页；通过官方 PDF 逐段核读 §8.3–§8.3.4，印刷页 46–50，包括条件、编码、正反例及多上位说明 |

既有选词与维护笔记保留原核读范围；本轮新增层级依据，不将没有重读的章节写成重新核验，也不据旧标准推定修订草案内容。

## 已核条款

| 条款 | 原文标题 | 本次核到的边界 |
|---|---|---|
| 5.3.5 | Using Warrant to Select Terms | 选择纳入受控词表的词时，正文列出 literary warrant、user warrant 和 organizational warrant。5.3.5.1–5.3.5.3 分别把依据落到领域内容与参考来源、使用组织偏好，以及用户请求或检索中的用法。 |
| 5.4 | Structure | 正文按结构复杂度列出 list、synonym ring、taxonomy 和 thesaurus，并说明结构用于显示词之间的不同关系。 |
| 11.1.1 | Avoid Duplicating Existing Vocabularies | 新建受控词表前，发起组织 should ascertain 现有词表是否覆盖相同或重叠领域；相关领域词表可以作为起点。 |
| 11.1.2 | Determine the Structure and Display Formats | 如条件允许，结构和显示形式 should be decided 后再收集候选词；显示形式会影响交叉引用和关系标记。 |
| 11.1.3 | Construction Methods | 11.1.3.1–11.1.3.4 分别说明委员会方法、经验方法、方法组合和机器辅助。机器可辅助识别候选词、统计标引用词和用户查询，但正文仍把受控词表建设视为需要智力判断的工作。 |
| 11.1.4 | Term Records | 每个 term 获准进入词表时，单独记录 should be created；正文列举记录可以包含 term、所咨询的 source(s)、范围注释、关系和历史注释等内容。source(s) 是原标准列举的记录内容，不由此成为本项目字段。 |
| 11.1.5 | Term Verification | 词进入词表前，词 should be validated，编制者 should also review 其层级关系，列出的权威材料 should be checked；材料包括技术词典等参考资料、现有受控词表和分类方案。 |
| 11.1.6 | Candidate Terms | candidate terms 也称 provisional terms，指尚未完成全部 acceptance procedures 的 proposed terms；这些词 should be marked，对象是在 term record 中加 special symbol 或 phrase。一旦 candidate term 获准成为 term，该 symbol 或 phrase must be deleted。与单一数据库相连的联机环境通常不向用户显示 candidate terms；其他环境 may be displayed。这里不把它转换成本项目状态。 |
| 11.1.8 | Unassigned Terms | 建立层级时，尚未用于标引、但为补全层级且本身可能具有标引价值的词，正文说 frequently admitted into the controlled vocabulary。这里不把 unassigned 转换成本项目状态。 |

## 层级依据

| 位置 | 核到的内容 | 使用边界 |
|---|---|---|
| §8.3，页 46–47 | 上下位须能按概念的基本类别作逻辑检验；区分种属、实例和整体部分，BT／NT 互反 | 学科与其研究对象不是同一种概念类别，不能仅凭研究联系建层级 |
| §8.3.1，页 47–48 | 种属采用下位全部属于上位的检验；仙人掌与多肉植物是正例，与沙漠植物的部分重叠是反例 | 不能以常见共现或只适用于部分成员的事实代替范围包含 |
| §8.3.2，页 48 | 实例连接一般类别与其具体实例 | 具体实例、种类和组成部分不能混同；专名本身不足以证明角色 |
| §8.3.3，页 49 | 整体部分涉及概念内在包含，不依赖临时情境；列出身体系统、地理及组织结构等例子 | 例子不是穷尽列表，也不表示所有部件关系都可以用层级表示 |
| §8.3.3.2，页 49 | 化油器可以属于汽车之外的机器，该词对采用相关关系 | 需与概念定义及下一节的多上位例子连读，不以父节点数量代替含义判断 |
| §8.3.4，页 49–50 | 多上位可基于种属、整体部分或不同关系类型；钢琴、生物化学、头骨分别提供例子 | 逐条联系仍须有逻辑依据；无法解释的具体边界不靠自定统一阈值补齐 |

以上为原文范围的转述。将这些业务判据用于本项目自有概念层级，是明确的采用选择；它不证明已核对 ISO 25964 全文，也不自动启用任何层级细分 RDF 扩展。项目条件见[层级判据](设计-词表数据规范.md#层级判据)。

## 维护依据

| 条款 | 原文标题 | 本次核到的边界 |
|---|---|---|
| 11.3 | Maintenance | 本节说明新增、修改和删除词的程序；term record should note 每次变更的日期并标识责任人。 |
| 11.3.1 | Updating the Vocabulary | 定期复审、新词建立和废弃词替换的政策与程序 should be established；controlled vocabulary editors should update 词表，频率取决于变更频率、数量和分发方式。 |
| 11.3.1.1 | Addition of Terms | 找不到合适 term 或 term combination 时，indexer 或 searcher should nominate 一个新 term 作为 candidate term。editor may want 使用提名表；新词和复议词 should be reviewed by the editor，preferably by an editorial board；正文列出的覆盖、注释、词形和关系决定 should be made for each term。 |
| 11.3.1.2 | Modification of Existing Terms | indexers 和 searchers should be able to propose 对现有 terms 或 relationships 的修改并提供理由与材料；提案 should be considered by the editor and board。在 term 被修改这一条件下，同时有两个分开的动作：(a) 变更日期 should be recorded in the history note；(b) USE reference should be made from the old form to the new form。词表用于 indexing system 时，旧词最后分配日期 should be included in the history note；relationships 修改时，旧关系记录 should be maintained in the history note。USE reference 不是 history note 的内容。 |
| 11.3.1.3 | Deletion of Terms | 过度使用和极少用于标引的 terms should be considered candidates for modification or deletion；正文还给出拆分过度使用词或增加更具体下位词的可能处理。 |
| 11.3.2 | Vocabulary Updates and Database Records | 词的修改或删除需要同时考虑既有数据库记录的检索影响。 |
| 11.3.2.1 | Methods for Handling of Modified or Deleted Terms | 除从未分配的词外，修改或删除对既有数据库记录检索能力的影响 must be considered。正文列出多种处理；若为检索或历史目的保留，词 must be marked，状态变更日期 must be recorded in the history note and displayed to users；另有一对一替换、可能需要人工介入的复杂替换，以及在特定条件下删除。选择取决于数据库规模、资源、变更性质与自动化能力；条款没有推出单一保留政策。 |
| 11.3.2.2 | History of Changes | 每个 term should have history note，note should also track 修改历史；废弃词保留但不再标引时，替换日期和理由 should be given。完全删除时，正文说 may be desirable 另存 deleted terms 文件以保留范围与历史，措辞不是无条件要求。 |
| 11.4.4 | Term Deletion | 删除 term 时，system should prompt for verification；system must make all relevant reciprocal deletions，对象是让所有指向和来自 deleted term 的 links 同时删除；若产生 orphan term，system should inform editor。这是系统行为要求，不是项目删除门槛。 |
| 11.4.5 | Candidate Terms | system should include 录入和标示 candidate terms 与 candidate relationships 的机制；这些 candidate terms 和 relationships 在 controlled vocabulary editors 复核并批准前不得进入 controlled vocabulary。candidate term records 的 structure should 与 term records 相同；candidate relationships should be reciprocated automatically；system should 支持这些 candidates 的检索、显示和打印。正文中的 controlled vocabulary editors 及这些规范词不自动指定本项目审批人、状态或流程。 |

上述条款描述标准中的维护活动、记录影响和系统能力。它们不自动定义本项目的字段、状态、责任角色、审批阈值、保留期限或删除政策。

## 修订状态

本记录引用的出版版本为 2005 版的 2010 年重申版。2026-08-29 曾在 NISO 页面观察到修订项目，但当时没有核到阶段编号、草案或完成日期；本轮未重新核验该项目状态。不能将这项历史观察称为修订版已出版，或以它替代当前采用正文。

## 适用边界

该标准面向单语受控词表。已读章节可以支持结构、选词依据、层级判断及维护方法；跨语言对应、RDF 表示、项目审批和交换合同各按其实际依据处理。

原文中的 candidate、unassigned、history note 等保持标准语境，不自动成为项目字段、状态、角色或阈值。§8.3 的业务条件也不等于 SKOS 的形式公理；来源转录与本地语义采用分别留痕。

## 未读范围

“阅读范围”之外的正文未在本记录中逐项核验；§11.1.7 虽已在既有阅读中打开，但未作为后续项目规则的采用依据。NISO 修订草案和未取得的 ISO 条款不据本记录补写。
