# 来源证据结论

状态：首批四份来源的离线准备全部完成。基线为 `9cd63b5`；本报告是 AI 的证据审查与处置建议，不是人工采纳决定。范围承接[首批盘点](2026-09-05-source-v2-preparation.md)；[离线工具](2026-09-05-offline-source-evidence.md)仅覆盖原有两个试用对象，本轮不扩展工具。

## 完成范围

本批已经给出四个直接映射对象、四份来源的字段与外部状态、七个用途角色，以及正文十七个独立链接的处置结论。没有未经处理就留给“下一批”的首批对象；需要外部材料或人工决定的项目在本文明确保留条件，不混入已完成项。

正式 v2 可直接采纳的完整来源记录为零。此结论不撤销现行旧形状记录，也不把缺少本轮独立证据说成原值必然错误。正式数据、角色、旧账本、软件代码和 vault 均不因本报告而变化。

## 结论概览

| 对象 | 现有材料可支持 | 不能支持 | 本批处置 |
|---|---|---|---|
| `types[explanation] → diataxis:explanation` | 学习与理解、背景与取舍的一般用途相符 | 全部本地 scope 与外部概念完全一致；新的严格 exactMatch 依据 | 保留现值；具体原段落与相邻 basis 尚待补足 |
| `concepts[computing] → gbt-13745:520` | 本地代码、名称与语言定位一致 | 原始标准及修改单已经核实；顶层范围完全等同 | 保留名称、既有语言采纳、映射及 source 兼容值 |
| `genres[analysis] → iptc-genre:Analysis` | 项目材料明确说明从新闻语境适配到笔记语境，存在本地使用理由 | 本地个人理解与新闻 Analysis 完全等价；中文形式和全部 genre 范围已完成术语采纳 | 保留 closeMatch；不升级关系，不批量关闭相关术语问题 |
| `entities[obsidian] → wikidata:Q103994532` | 项目已登记软件本体、官网地址、候选状态和外部条目号 | Q 条目在具体版本上与软件身份一致；软件主题归属获准 | 保留新增旧形状记录，身份对应与 subjects 判断分别保留条件 |

## 类型对应

现行 [types.yaml](../../data/vocab/types.yaml) 保存 `explanation`，范围为“读者为了理解为什么；讨论，多角度，承认观点”，并以 `exactMatch` 指向 Diátaxis 的 `explanation`。[内容模型](../../docs/design/model/content-model.md#文档类型词表)把该类型用于学习、理解；这说明本库采用意图，不充当外部证据。

[写作阅读记录](../../docs/references/writing-guides.md#读者与目的)保存了 Explanation 页面以及 `Explanation and its boundaries`、`Writing good explanation` 两处阅读位置。其摘要涉及背景、联系、原因、替代方式、取舍，以及与操作和参考内容的边界。

| 本地含义 | 离线记录支持程度 | 本轮判断 |
|---|---|---|
| 理解为什么 | 已有原因、背景与联系的阅读摘要 | 可支持一般用途相符的判断 |
| 讨论与多角度 | 摘要提到替代方式与取舍 | 有相关支持，但不足以独立证明具体定义范围完全一致 |
| 承认观点 | 当前摘要未直接记录相应表述与上下文 | 尚缺具体原段落，不能据模型记忆补成已核事实 |
| `exactMatch` | 现值表达项目已有选择；摘要没有逐项完成双方范围比较 | 本轮不新批准严格关系依据，也不自动改为其他关系 |

需要补充的材料仅限：已保存的 Explanation 页面或相关原文段落，包含上述两个小节、获取日期，以及对讨论、视角或观点的实际表述。日期和哈希分别标识取得时间与文件版本，不把来源实体的 `version: 2026-08` 当作网页发布版本。取得材料后只补核上表未覆盖的范围，不重查已经明确的一般用途。


## 学科对应

[本地分类清单](../../docs/references/gbt-13745.md)明确记载材料来自第三方转载站，并包含 `520 计算机科学技术` 标题。[生成器](../../packages/kb-core/src/kb_core/build_topics.py)的顶层配置把 `computing`、中文名称和 `520` 绑定。两者可证明项目当前对应关系有可追溯的本地来源，但生成代码不是外部概念等同证据。

现行 `basis.zh` 已保存第 1 级语言依据和定位 `520`。[语言依据决定](../../docs/decisions/structured-label-basis.md)明确这次结构迁移保留原采纳，不宣称新做外部核验。因此旧账本的“缺定位”不能继续描述当前语言字段，也不能反过来说明本轮已核标准原文。

[层级规则](../../docs/design/model/hierarchy.md#结构复制)说明顶层是本地建立的范围边界，分别映射到 GB/T，顶层没有实际派生来源。computing 下位采用 CS2023 是组织方式的选择：下位集合不同不能单独证明或否定顶层概念的 exactMatch。当前没有独立 scope，不能从本地现有下位集合擅自补写概念范围。

需要补充的材料为：GB/T 13745-2009 原始材料中涵盖 520 的页或完整相关条目，以及适用修改单是否影响该代码、名称或范围的材料。原有冻结记录提及两个修改单，但本轮没有核查其正文。若修改单不影响 520，应保存可回查的判断依据，不为全标准所有条目展开无关审查。

在补件前保留中文采纳、`exactMatch` 和现行 `source: self` 兼容值；后者不新增为实际派生，也不改成 `source: gbt-13745`。


## 体裁对应

现行 [genres.yaml](../../data/vocab/genres.yaml) 的 `analysis.scope` 为“个人理解、比较、推断”，以 `closeMatch` 指向 `http://cv.iptc.org/newscodes/genre/Analysis`。[笔记类型说明](../../docs/concepts/note-types.md#作者立场)把所引 IPTC 定义转述为“记者深入研究后得出的数据与结论”；[内容模型](../../docs/design/model/content-model.md#体裁词表)明确把新闻中的“记者”“事件”按笔记语境理解。

这两份材料支持“项目进行了语境适配”的判断，不足以独立证明每种个人理解都符合外部 Analysis 定义。例如，本地 scope 没有单独要求深入研究，也没有新闻对象限制；这些差异解释了为什么本批不能将 closeMatch 自动升级为 exactMatch。它们也不是新增 closeMatch 批准的充分条件。

冻结 [match-inventory.tsv](../../tests/fixtures/governance-frozen-2026-08-31/match-inventory.tsv) 第 42 行保存了曾读取五个 IPTC 目标条目的记录；[映射账本](../../data/audit/migrations/source-v1/match.yaml) 对 `match-inventory.tsv:42` 仍标记 `blocked_unread_material`。准确结论是有历史阅读记录，但没有足以在本轮独立回查的原条目及相邻关系依据，不能解释成“原材料从未读过”。

所需补件为 Analysis 条目的已保存定义、URI、版本或取得日期，以及本地适配范围的明确判断。字段里的 `version: 2024-02-13` 不单独证明所读条目的版本，也不保证其未被更新或退役。本批不替换 URI 的 HTTP 协议或大小写，不因网页展示地址不同改变条目身份。

关联的术语问题须分开保留。[术语审计](../../data/audit/migrations/term-v1/terms.tsv) 中 `review_line=248` 的 genre 记录为“有冲突”，`review_line=253` 的“体裁”为“无依据”，两者 `current_action=defer`、`disposition=audit-only`。它们的 `blocks_cutover=false` 表示审计分类没有阻断当时那一步机械交付，不表示术语已获准。此项不直接证明 Analysis 的中文标签错误，也不自动撤销现行内容字段或关系；不得利用本次来源梳理提前关闭术语范围与中英对应问题。

## 实体对应

`obsidian` 已由 `61d0487` 登记为 `software`，scope 明确指应用本身，不单独表示配套服务或社区插件；当前 `subjects: [computing]`、`basis.subjects: self`、`status: candidate`。该提交确立现行项目记录，并不代替外部 Q 条目证据。

本轮材料只提供 `Q103994532` 和本地软件描述；既有离线范围内没有对应 Q 条目的 revision、描述、类型语句或标识符内容。因此本批不根据名称相同或模型知识确认实体等同，也不借其他 Wikidata 条目的旧审查结论批准这个新增映射。

| 问题 | 可用信息 | 缺口与处置 |
|---|---|---|
| 是否指同一个软件 | 本地 scope、官网 URL、既有 Q 号 | 需要 Q 条目具体 revision 的描述、类型与标识信息；分别核对产品、发布版本、厂商和配套服务是否被混为同一对象 |
| 是否挂接 computing | 本地软件身份、当前 computing 主题和 self 断言 | Q 条目身份即使成立，也不证明主题归属；由主题覆盖与具体归属依据单独形成 L2 提案 |
| 是否可以作为正文来源 | 本地记录是软件本体 | 不用软件 ID 代替帮助文档、访谈或插件项目；正文材料仍按各自身份处理 |
| 是否受旧账本覆盖 | 冻结实体集合不含 obsidian | 保留新增对象差异，不伪造旧库存行或把新记录回填到冻结审计 |

所需补件限于该 Q 条目的已保存内容与 revision 定位，以及软件范围和主题关系的独立依据。Wikidata 的 `version: rolling` 与某个 Q 条目的具体 revision 是不同信息，不能互相替代。本批不改变实体状态、类别或外部映射。

## 用途结论

[用途账本](../../data/audit/migrations/source-v1/uses.yaml) 中这七项均为 `proposed`、`decision: null`。以下列出每项的实际关联与所需决定，不用四个具体关系批量批准整份来源。

| 来源与角色 | 冻结身份 | 本批关联与影响 | 处置及恢复条件 |
|---|---|---|---|
| GB/T mapping | `source-roles.tsv:2` | 本批对应 computing；当前全源有 435 条 topic 映射 | 保留 proposed；角色用途批准与 520 的具体关系采纳分别提交，其余映射不随之获准 |
| GB/T structure | `source-roles.tsv:3` | 全源有 427 条 topic 实际来源字段；computing 顶层无实际派生来源 | 本批不恢复结构迁移；有具体结构迁移需求时再绑定条目、定位和派生依据 |
| Diátaxis mapping | `source-roles.tsv:35` | 本批对应 explanation；全源有 4 条 type 映射 | 保留 proposed；明确文档类型映射用途后再逐值采纳，不以一项关系批准另三项 |
| Diátaxis structure | `source-roles.tsv:36` | 现行用途已登记；本批选定的 type 记录只有 match，没有严格 source 对象 | 没有该对象的结构迁移交付，本批不批准；不得把 match 或“取自”叙述机械改为实际派生字段 |
| Wikidata mapping | `source-roles.tsv:37` | 本批为新增 Obsidian 关系；全源有 24 条 entity 映射及 1 条 form 映射 | 保留 proposed；用途批准不核实 Q 条目，各条身份关系仍分别需要证据 |
| IPTC mapping | `source-roles.tsv:44` | 本批对应 analysis；全源有 5 条 genre 映射 | 保留 proposed；先明确映射用途与适配边界，不联动术语采纳或其他四个关系 |
| IPTC structure | `source-roles.tsv:45` | 现行用途已登记；本批 analysis 没有严格 source 对象 | 本批不批准；发生具体派生迁移需求后再提供结构、item、locator 与 basis |

[来源校验决定](../../docs/decisions/source-validation-policy.md) Q11 和 Q18 明确角色状态、决定与关系依据各自成立。登记用途、代码读取成功、出现一次内容引用都不替代批准。表中引用数量是字段库存，不能作为角色或关系的采纳证据。

## 来源字段

| 来源 | 保留的旧值 | 外部状态结论 | 应补材料 |
|---|---|---|---|
| GB/T | kind=standard；tier=de-jure；version=2009；status=candidate；checked=2026-08-23 | `source-entities.tsv:2` 仍 unresolved；candidate 不是外部状态 | 发布方的标准身份、状态及适用修改单；地址与 watch 的定位；各具体值依据 |
| Diátaxis | kind=standard；tier=de-facto；version=2026-08；status=candidate；checked=2026-08-23 | `source-entities.tsv:23` 仍 unresolved；年月不能自动解释为发布版本 | 所引页面的材料版本与时间、外部状态证据；kind 适用性与观察入口仍需分别核对 |
| Wikidata | kind=standard；tier=de-facto；version=rolling；status=candidate；checked=2026-08-23 | `source-entities.tsv:24` 仍 unresolved；rolling 不等于 current | 数据集身份与状态材料；具体 Q 引用另有 revision；kind 与观察入口不能由全站网址推导 |
| IPTC genre | kind=standard；tier=de-facto；version=2024-02-13；status=active；checked=2026-08-23 | `source-entities.tsv:30` 仍 unresolved；项目 active 不等于外部 current | 词表与条目版本、状态或退役说明；字段依据和观察入口 |

四项均保留当前 id、名称、地址、版本、档级和核对日期作为现行旧值，不把这次离线审查日期回填为外部 `checked`。旧值有明确记录不代表满足新合同；字段何以成立仍需要相邻依据。

地址：GB/T 的旧 watch 与旧 url 相同，其余三项未登记 watch。不能直接从这些字符串构造已批准的结构化 urls、地址角色和 watch。`review` 不能机械由旧 checked 生成已完成义务；没有替代证据不能断言“已无替代项”。`history` 和具体字段批准也不能用本报告补造。

归属：GB/T、Diátaxis、Wikidata 的 `basis.subjects` 为 self；IPTC 为紧凑 `iptc-genre:scope`。全部按原值保持，不升格为已核外部依据。Obsidian 软件的 self 归属另列，不增加到四份来源的外部状态批次中。

## 正文处置

[首批盘点的正文材料表](2026-09-05-source-v2-preparation.md#正文材料)已逐一覆盖 17 个 URL，本轮沿用其固定笔记快照，不扫描其他并行工作中的新内容，也不把这份盘点冒充当前 vault 的完整来源清单。

已有具体阅读记录的存储、Properties、Bases、内部链接和反向链接可作为后续取证入口；需要优先补件的具体事实包括访谈起源、共享限制和插件权限。入口页、社区目录、个人示例和插件仓库保持普通引用，没有具体正式采用需求时不强制发放实体或用途 ID。

这已完成本批每个链接的处置，不表示所有外部网页事实都已经核实。缺件不再重复展开成新的执行批次；材料到位或正式采用需求明确时，只恢复对应对象。

## 恢复条件

本批准备工作没有剩余的机械整理任务；以下是恢复后续采纳所需的条件，不是等待 AI 继续重复盘点的待办。

| 条件 | 对象 | 后续动作与权限 |
|---|---|---|
| 原始条目、段落或 revision 可回查 | Explanation、520、Analysis、Q103994532 | 补核本报告指出的具体范围；相邻依据和关系按现行 L2 规则提案 |
| 来源身份、版本与外部状态材料明确 | 四份来源实体 | 提交逐字段依据，不自动改档；tier 变更仍由人作相应 L3 决定 |
| 具体用途与决定范围明确 | 七个角色中实际要启用的项目 | 逐角色采纳，不以用途批准替代具体关系判断 |
| 关联术语或一般实体模型边界需要进入正式数据 | genre／体裁、Obsidian 等一般实体 | 分别按术语与实体治理处理，不由来源准备顺带决定 |
| 正式激活阶段被另行开放 | 严格来源与术语切换 | 才恢复完整候选、绑定、原子应用、补偿回滚和正式切换；发版仍是独立决定 |

来源探测输出与 schema 的差异、草案与 Q09 阈值文字不同步，继续保留在[首批盘点](2026-09-05-source-v2-preparation.md#后置缺口)中。本批不扩大为探测工具修复；模式、索引、校验或离线工具可运行，也不能使材料与批准条件自动满足。

## 完成证据

本批写集只有审查材料与项目路线，正式词表、旧账本、schema、核心与应用代码、vault 均未修改。已按记录身份核对四个直接关系、七个角色和四个外部状态库存；正文 URL 处置沿用初次快照。原有两个对象结论在整篇重写中保留，新增 IPTC、Wikidata、字段、角色、术语关联及统一恢复条件，避免另留“随后再审”的小批次。

独立语义审查未发现 Important 或 Critical 问题；审查覆盖 IPTC 语境适配、术语审计效力、软件身份与来源分工以及完成声明边界。角色与外部状态身份对账、文档链接和 Git 差异格式检查通过。本轮只有文档变更，没有重复执行已通过的工具或应用测试。
