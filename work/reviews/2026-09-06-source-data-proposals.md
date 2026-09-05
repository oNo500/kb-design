# 来源数据提案

状态：待人采纳，不是已采纳决定。读取基线为 `633f684`，工作区的正式数据仍为旧形状。本提案集中处理现有来源的字段、用途和已知阻断；不转换正式数据，不批准事实，不以人的同意替代事实证据，也不宣称整批已具备切换条件。

## 证据范围

本轮只读取已有[联网证据](2026-09-05-source-network-evidence.md)、`build/source-verification/` 留存材料及当前词表，没有新联网或下载。下文“已核”指记录在 2026-09-05 的外部观察；本文件日期不是新的外部核对日期。[既有字段采纳](../../docs/decisions/source-field-values.md) P1–P4 的原依据日期仍为 2026-08-29，本提案不重复批准或覆盖它们。

外部 `source_status` 与项目 `status` 分开。表中“待核”是本报告的处置文字，不是建议增加的枚举值，也不能落成 `unknown` 或无依据的 `current`。版本存在、页面可访问、修订进行中和外部现行状态分别判断。部分字段有证据不等于实体全部必填值、用途和下游关系均可通过。

## 版本状态

下表穷尽现有用途对应的来源实体。保留旧值只表示不擅自换版；“旧值未核”不成为新的依据。凡建议新状态，依据限于所列发布者记录及观察日期。

| 来源 | version 建议 | source_status 建议 | 证据定位与尚缺事实 |
|---|---|---|---|
| gbt-13745 | `"2009"` | `current`，待采纳 | 联网证据“GB/T”行的标准平台状态、发布日期；修改单影响另见下节，现行不证明旧代码均有效 |
| cs2023 | `"2024-01"`，保留定稿月份 | 待核 | “CS2023”行与完整 HTML 的定稿过程支持月份，3 月编辑另记；最终报告存在不单独证明未被替代 |
| swebok | 保留使用版 `"4.0"`，不改成 `"4.0a"` | 待核旧版地位 | “SWEBOK”行封面核得当前文件 v4.0a、August 2026；尚缺 4.0 与 4.0a 的替代声明、差异和现有映射适用性 |
| acm-ccs | 旧 `"2012"` 未核 | 待核 | 两个发布者入口均未取得正文；失败不等于 withdrawn |
| asvs | 建议 `"5.0.0"`，须先确认旧 `"5.0"` 引用确属该版 | `current` 仅适用于已核 5.0.0 | “ASVS”行 latest stable；旧条目与正式补丁版本的对应尚待核，不能连同本地条目自动升级 |
| cwe | `"4.20"` | 待核 | “CWE”行确认 2026-04-30 发布；发行存在不证明之后无新版，逐条定义未核 |
| attack | `"19.2"` | `current`，待采纳 | “ATT&CK”行 Current Version，起始日期 2026-04-28；不批准全部战术关系 |
| owasp-top10 | 保留选用 `"2021"` | 建议 `superseded`，限定被当前 2025 版接替的版本地位 | “其余来源”及本地标准记录“安全风险”明确 current 2025／旧版 2021；不把旧版不可使用或项目 deprecated 作为结论 |
| owasp-llm-top10 | `"2025"` | 待核 | “OWASP LLM”行 LLM01:2025 等标识支持年份；目录存在不足以独立判定外部状态 |
| atlas | `"2026.07"`，限已列出的数据文件 | 待核 | `atlas-file-observation.json` 的 ATLAS-2026.07.yaml 与 blob 标识；未读取文件全部内容，不能把目录 v6 当内容版号或断言最新 |
| nist-ai-rmf | `"1.0"` | 待核，不以正在修订推断 superseded | 本地标准记录“人工智能风险”载明 2023-01-26 发布并仍提供 1.0；Profile 不是替代版本 |
| anthropic-docs | 旧 `"2026-08"` 未核，不补抓取月份 | 待定模型且缺事实 | 本地网站记录“厂商文档”只支持身份、入口重定向与逐日产品日志，未见整站发行标识 |
| rfc-1122 | `"1989"` | 待核三值状态与更新范围 | “RFC 1122”行 Internet Standard／STD 3，并有更新它的 RFC；更新不等于整份被替代，仍可引用不等于全部条款现行 |
| rfc-9110 | `"2022"` | 待核 | 本地标准记录“协议语义”载明 Internet Standard、June 2022；未列被替代关系不作为完整排除证明，勘误未核 |
| osi | `"1994"` | `current`，待采纳 | 本地标准记录“互连模型”明确仍现行、阶段 90.93；英文 1996-06 修正版另作定位，不把年份改为 1996 |
| mdn | 旧 `"2026-08-20"` 未核 | 待定模型且缺事实 | 本地网站记录“技术参考”：2025-07-29 只属入口单页，不是整站版本 |
| mdn-curriculum | `"2025-10"`，明确为显示更新月份 | 待定模型且缺事实 | 本地网站记录“前端课程” Last updated: October 2025；不是编号发行版或不可变快照 |
| iso-25964-1 | `"2011"`，沿用已采纳字段 | `current`，沿用已采纳历史观察 | P1 原日期保留；联网证据另核 Published、2011-08、90.92 待修订，不构成 withdrawn／superseded |
| iso-25964-2 | `"2013"`，沿用已采纳字段 | `current`，沿用已采纳历史观察 | P2 原日期保留；联网证据另核 Published、2013-03、90.92；不借 Part 1 代替 Part 2 |
| z39-19 | `"2005 (R2010)"`，沿用已采纳字段 | 待核 | P3 与联网出版页支持版本、DOI；Standard、发布日期或修订项目不足以独立批准外部现行状态 |
| skos | `"2009-08-18"`，沿用已采纳字段 | 建议 `current`，待采纳新依据 | 联网证据“SKOS”行发布历史最新 Recommendation 与被替代 SKOS Core 的区分；未通读勘误，不将新观察覆盖 P4 日期 |
| diataxis | 旧 `"2026-08"` 未核 | 待定模型且缺事实 | 已读 Explanation 原文是页面内容证据，没有整站月份发行版证据 |
| wikidata | 旧 `"rolling"` 暂留历史值 | 待定模型且缺全源事实 | 单个 Q 条目 revision 2530661391 不等于整个 Wikidata 的版本与状态 |
| roadmap-sh | 持续更新性质已核，`"rolling"` 的正式版本语义待定 | 待定模型且缺事实 | 本地网站记录“开发路线” Actively Maintained 与日志，不是固定发行版 |
| teachyourselfcs | `"2020"`，保留原精度，依据注明 May 2020 | 待定模型且缺事实 | 本地网站记录“自学指南”；不能据 2020 更新说明保证此后字节未变 |
| cmu-15-445 | `"Fall 2025"` | 待定学期与外部状态的对应 | 本地网站记录“数据库课程”：归档仍可读，根入口现为 Fall 2026；学期更替不自动等于原课程被撤回或被新内容替代 |
| db-engines | 旧 `"rolling"` 未核 | 待核 | 排名页与官网都未取得正文，榜期、更新机制与状态均无本轮支持 |
| dita | 保留 `"1.3"` 使用范围，整合勘误版另行选择 | 待核所选具体版 | 本地标准记录“文档架构”明确 2018 Errata 02 取代 2015 原版；不能据此证明 1.3 是全系列现行版，也不能静默把旧引用切至整合版 |
| iptc-genre | 整表旧 `"2024-02-13"` 未核 | 待核整表状态 | Analysis 的 modified=2010-12-15、retired 空只属一个条目，不外推整份词表版本／状态 |
| lom | 建议 `"2002"`，把替代说明移出版本字符串 | `superseded`，待采纳 | 联网证据“LOM”行 IEEE 2002 页明确 Superseded，2020 页明确替代；保持所用 2002 对象与取值 |
| schema-org | `"30.0"` | `current`，待采纳 | 本地标准记录“语义词表”发布列表与 stable release 独立字段，日期 2026-03-19 |

## 地址字段

以下是有现有证据支持的精确 `urls` 建议，表中每行对应一个 `{role, url, primary}` 项。同一来源列出的项共同组成建议数组；未列来源不凭旧网址字符串新增地址角色。原地址在迁移前值与 Git 中保存，不因新入口采纳而丢失历史。地址选择不批准该地址上每个条款。

| 来源 | role | primary | url 与证据 |
|---|---|---|---|
| gbt-13745 | landing | true | `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E`；联网证据标准平台状态与备注 |
| cs2023 | landing | true | `https://csed.acm.org/final-report/`；最终报告入口 |
| cs2023 | full_text | false | `https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm`；留存完整 HTML，URL 月份不是报告版次 |
| asvs | landing | true | `https://owasp.org/www-project-application-security-verification-standard/`；latest stable 与版本引用说明 |
| attack | landing | true | `https://attack.mitre.org/resources/versions/`；Current Version，作为版本目录入口，不冒充某条战术原文 |
| owasp-top10 | landing | true | `https://owasp.org/www-project-top-ten/`；同时列当前与旧版，不能作为 2021 冻结全文定位 |
| atlas | landing | true | `https://github.com/mitre-atlas/atlas-data/tree/main/dist/v6`；官方数据目录观察；目录可变，文件 blob 单独保留 |
| nist-ai-rmf | landing | true | `https://www.nist.gov/itl/ai-risk-management-framework`；发布与修订说明 |
| anthropic-docs | landing | true | `https://platform.claude.com/docs/en/home`；旧址重定向的实测目标 |
| rfc-1122 | landing | true | `https://www.rfc-editor.org/info/rfc1122/`；标题与关系区 |
| rfc-9110 | landing | true | `https://datatracker.ietf.org/doc/rfc9110/`；IETF 文档表；本轮 RFC Editor 入口失败，不补 canonical 结论 |
| osi | landing | true | `https://www.iso.org/standard/20269.html`；General information |
| mdn | landing | true | `https://developer.mozilla.org/en-US/docs/Web`；入口标题与单页修改日 |
| mdn-curriculum | landing | true | `https://developer.mozilla.org/en-US/curriculum/`；标题与 Last updated |
| iso-25964-1 | landing | true | `https://www.iso.org/standard/53657.html`；General information／Life cycle |
| iso-25964-2 | landing | true | `https://www.iso.org/standard/53658.html`；General information／Life cycle |
| z39-19 | landing | true | `https://www.niso.org/publications/ansiniso-z3919-2005-r2010`；沿用 P3 |
| z39-19 | doi | false | `https://doi.org/10.3789/ansi.niso.z39.19-2005R2010`；沿用 P3 |
| z39-19 | full_text | false | `https://groups.niso.org/higherlogic/ws/public/download/12591/z39-19-2005r2010.pdf`；联网证据记录已取得出版 PDF |
| skos | canonical | true | `https://www.w3.org/TR/skos-reference/`；W3C Reference 与发布历史对应 |
| roadmap-sh | landing | true | `https://roadmap.sh/`；Actively Maintained |
| teachyourselfcs | landing | true | `https://teachyourselfcs.com/`；May 2020 更新与作者栏 |
| cmu-15-445 | archive | true | `https://15445.courses.cs.cmu.edu/fall2025/`；Fall 2025 与归档提示，取代会转到新学期的根入口作为所用学期主地址 |
| lom | landing | true | `https://standards.ieee.org/ieee/1484.12.1/3294/`；2002 出版身份与 Superseded |
| schema-org | landing | true | `https://schema.org/version/latest`；30.0 stable release；可变入口仍需 checked |

SWEBOK v4.0a PDF 不作为旧 4.0 的全文地址；DITA Errata 02 不作为未经选择的 2015 原版全文。Wikidata Q 条目与 IPTC Analysis 页面留在逐关系依据中，不将子条目地址充当全源身份。LOM 的旧 LICEF final draft 地址保持历史材料性质，本轮没有重新核实其字节与 2002 出版正文一致，不能升级为官方 full_text。ACM 与 DB-Engines 的失败地址不被标为已核有效。

地址表外的 `owasp-llm-top10`、`diataxis` 等来源即使有已读子页，仍需区分当前记录是整套来源还是该具体页面；不为补齐数组而扩大已核范围。所有新依据使用来源实体 ID、上述发布者位置及原观察日期；本地记录和响应路径只作审查留存，不把项目笔记当作发布者来源。

## 用途采纳

依据[用途合同](../../docs/design/model/sources-registry.md)，下表逐项给出推荐。写为“建议 approved”仅指待人批准的资格，不是当前数据值。采纳前所有原角色保持待审；批准必须引用实际批准该来源、角色及范围的决定。未使用角色保持 `proposed`、`decision: null`，不因未使用自动 retired。候选旧值转 `discovery/proposed`，不取得结构或映射资格。

实际使用证据来自当前 `topics.yaml`、`types.yaml`、`genres.yaml`、`forms.yaml`、`entities.yaml` 的具体字段。角色资格和每条关系分别采纳：结构要求同时具有 mapping、符合既有档级与版本条件；已有字段仅证明用途需求，不证明复制事实或范围等同。

| 来源 | 逐角色推荐 | 实际使用与限制 |
|---|---|---|
| gbt-13745 | mapping、structure 建议 approved；具体受修改单影响引用阻断 | 主题映射和下位记录派生有明确用途；顶层 source:self 不作为派生，talent-studies 单列处置 |
| cs2023 | mapping、structure 建议 approved | 主题知识单元映射、主派生及知识域数组；代码名定位不是关系证明，external_group 与记录派生分别需要依据 |
| swebok | mapping、structure 保持 proposed，先确认所用 4.0 材料 | software-requirements 等映射与数组／记录旧 source；v4.0a 不能替旧版取得资格 |
| acm-ccs | mapping 保持 proposed | 当前无 match／source；入口失败不删除来源 |
| asvs | mapping 建议 approved；structure 保持 proposed 至旧 5.0 与 5.0.0 对应明确 | security-asvs 数组及章节记录使用；没有以精度修正替代版本核对 |
| cwe | mapping、structure 建议 approved；group 保持 proposed | 弱点分类记录与 security-cwe；4.20 发行存在有证据，具体外部分组与成员派生各自待核 |
| attack | mapping、structure 建议 approved | 战术概念及 security-attack 数组；19.2 资格不批准本地中文或逐战术 rel |
| owasp-top10 | mapping、group 均保持 proposed | 当前无具体 match／source，不把新版 2025 展示变成旧 2021 的使用或批准 |
| owasp-llm-top10 | mapping、structure 建议 approved；group 保持 proposed | 2025 风险概念与数组；用途不批准全部定义、译名及分组 |
| atlas | mapping 建议 approved；structure 保持 proposed 至数据内容版与所用层次对应明确 | 战术记录与数组已引用；目录文件名不足以证明具体内容与复制层次 |
| nist-ai-rmf | mapping 保持 proposed | 当前无具体 match／source；作为阅读依据无需批准 mapping |
| anthropic-docs | mapping 保持 proposed，不新增 structure | 当前无具体 match／source，vendor 与无整站版本不能借迁移取得结构资格 |
| rfc-1122 | mapping、structure 建议 approved | 四层记录和数组；Q17 要求逐层依据，后续 RFC 更新范围另核 |
| rfc-9110 | mapping 保持 proposed | 当前无具体 match／source；标准身份不代表正在使用其映射 |
| osi | mapping 保持 proposed | 当前无具体 match／source；本次不创建 OSI 概念或结构 |
| mdn | mapping 保持 proposed，不新增 structure | 当前无具体 match／source；MDN Web 结构资格仍是独立待定事项 |
| mdn-curriculum | discovery 保持 proposed | 旧 candidate，无具体引用；不自动新增 group 或 structure |
| iso-25964-1 | mapping 保持 proposed | 当前无具体 match／source；P1 只批准字段，basis 取证不要求用途角色 |
| iso-25964-2 | mapping 保持 proposed | 同上，P2 不批准映射用途 |
| z39-19 | mapping 保持 proposed | 当前无具体 match／source；方法与条款阅读不是结构复制 |
| skos | mapping 保持 proposed | 当前无具体 match／source；用 SKOS 表达关系不等于映射到 SKOS 条目 |
| diataxis | mapping 建议 approved；structure 保持 proposed | 四个 type 的 match 有实际用途，无记录 source；月份版本未证实，不能批准 structure |
| wikidata | mapping 建议 approved | 一般实体与 cheat-sheet 的映射用途明确；软件 Q 条目核验不覆盖其他条目或词表语言依据 |
| roadmap-sh | discovery 保持 proposed | 旧 candidate；持续维护不带来结构资格 |
| teachyourselfcs | discovery 保持 proposed | 旧 candidate；课程推荐不等于本地结构复制 |
| cmu-15-445 | discovery 保持 proposed | 旧 candidate；保留所用学期，不批量引入课件结构 |
| db-engines | discovery 保持 proposed | 旧 candidate 且未取得正文，不填 group 或 mapping |
| dita | mapping 建议 approved，限既有 1.3 文档类型；structure 保持 proposed | troubleshooting、glossary-entry 有 match，无记录 source；勘误版逐值对应未核 |
| iptc-genre | mapping 建议 approved，限体裁映射用途；structure 保持 proposed | 五个 genre 的 match，无记录 source；Analysis 新证据不批准另四个关系，也不关闭 genre／体裁术语问题 |
| lom | mapping 建议 approved，限冻结 2002 取值；structure 保持 proposed | 载体 match 有用途；两个 forms 数组按 Q16 是 local_analysis，不支持外部 structure，也不构成派生概念组用途 |
| schema-org | mapping 建议 approved | Review、HowTo、TechArticle 的现有映射需求；30.0 当前发行不证明每条 rel |

external_group 使用 structure 资格，其分组依据与成员的实际派生分别核对；旧数组 source 不自动成为批准。已有 group 仅供从本库现有映射确定性计算派生概念组，并继续要求 mapping；CWE、OWASP Top 10 与 OWASP LLM Top 10 的该角色均保持 proposed。本提案不新增角色。若现有范围最终采用本地结构而非外部分组，须有对应判断，不能靠改字段名避开依据。所有拟 approved 资格只有在来源实体及引用满足完整合同后才能用于正式快照；角色采纳不消除上表状态缺口。

## 关系处置

[本次迁移库存](2026-09-06-source-migration-inventory.json)保存六份输入哈希与 846 条记录的迁移相关旧值，当前范围为 757 条 match、692 条外部 source 和 24 个 external_group。它是审阅材料，不是生成器输入；现有映射整体仍未逐项核实，本提案不把这些关系或新增对象写成已核。已补实质证据的少数对象作以下集中建议，其余按现值及具体缺口保留，不机械生成相邻 basis。

| 对象 | 可建议的处置 | 尚未成立的结论 |
|---|---|---|
| explanation → Diátaxis explanation | 保留 exactMatch，原页开篇、boundaries、Admit opinion and perspective 可进入逐值依据提案 | 不由此批准另三个文档类型或整站版本 |
| analysis → IPTC Analysis | 保留 closeMatch，Concept ID、Definition 与本地“个人理解、比较、推断”分别呈现 | 新闻语境与笔记语境不完全等同；不是 exactMatch，也不证明全部个人理解可互换 |
| obsidian → Wikidata Q103994532 | 软件身份 exactMatch 可进入采纳提案；固定 revision 2530661391、P31、P856 与官网相互核对 | 不单独批准 subjects:computing；软件本体不成为帮助页或插件材料身份 |
| computing → GB/T 520 | 保留原中文语言采纳和映射待审值 | 现行标准身份不补齐 520 范围与修改单适用证据 |
| CS2023 知识单元 | 使用完整 HTML 及 `cs2023-code-name-pairs.tsv` 的邻近偏移作为取证定位 | 代码与英文名称同现不证明每条 exactMatch、中文 scope、归属或派生层次 |

## 模型卡点

当前合同要求每个来源都有 source_status，且只允许 current、superseded、withdrawn。持续更新的网站未必具有与这三个值相对应的发布状态。逐条引用有证据，并不能证明整站“现行”；反过来，尚未核实整站状态也不自动否定一个固定条目的事实。这个问题至少影响 anthropic-docs、mdn、diataxis、wikidata、roadmap-sh、db-engines，并影响课程和归档的状态解释。

推荐单独采纳以下模型调整，收到明确采纳前不修改 schema 或放宽当前门禁：

- source_status 改为可省略。缺值只表示“外部状态未核实”，不是 current、不是“不适用”，也不新增 unknown 枚举；导出与预览必须明确显示这个缺口。
- 已填写的 source_status 继续要求发布者依据和精确字段采纳，不能因字段可省略而覆盖 P1、P2 已有合格结论。任何确实依赖外部现行状态的操作，在缺值时继续阻断。
- 来源是否可以支持某条关系，仍由所选材料、逐条依据、用途资格和关系采纳决定；不把“没有整源现行状态”当作所有历史或固定材料不可引用的通用理由。
- version 继续必有该键；无法确认已登记版本时允许 null，含义限定为“未登记可核实版本”。旧 rolling、月份或其他旧值留在 history.before，不把 null 宣称为发布者根本没有版本。实际引用仍须明确条目位置及真实核对日期；无版本 de-facto 不能取得 structure 资格。

这是对已采纳方案中强制外部状态条件的修订提案，不是实施授权已经包含的例外。它不允许把未核对关系写入 basis，不删除稳定身份，不恢复旧格式兼容。替代方案是保持现有强制字段，并在全部来源都取得适用的三值状态及必要版本证据之前暂缓整批切换；不能用批准代替取不到的外部事实。

IPTC 单条 modified 和 Wikidata 单条 revision 不能填入整源 version。第二号 GB/T 修改单缺文、具体关系未核及来源角色未采纳也不因上述模型调整而自动解决。

## 稳定身份

GB/T 第 1 号修改单的已读附件指出删除 6305520、增加 6305521，并在社会学下增加人才学分支；第 2 号修改单正文尚未取得。当前 `talent-studies` 保持旧 `630.5520`、名称“人才学”与 human-resource-development-and-management 上位关系，不能只替换代码就继续使用相同 ID 表达新概念。

建议保留该 ID 的既有身份与迁移前内容，明确阻断这条映射及相关派生进入严格新值；先比较修改单中各新旧对象的名称、范围与归属。只有同一概念得到证实，才能提案更新外部代码；如果范围不同，需人决定新概念身份、旧对象去向与反向引用处置。本文不删旧对象，不自动 deprecated，不发放新 ID，不将结构位置变化写成同义。第二修改单缺文也不能由第一个附件补足。

## 旧版选用

LOM 继续执行 Q05 的 2002 freeze；新核 `superseded` 是外部版本状态，不把项目记录改为 deprecated，不替换 15 个载体取值，不改变 Q16 的本地数组。2020 Active Standard 的已核事实只支持替代关系存在，尚未满足新实体全部字段与取值比较；本轮不创建 2020 实体，不伪造 replaced_by ID。若严格模型必须用已存在实体表达非空替代关系而不能保存外部替代事实，应先提交这一表示问题，不能填空声称无替代或创建空壳让校验通过。

SWEBOK 4.0 与 OWASP Top 10 2021 是目前选用版本，最新出版物与项目换版分别决定。建议保留选用版及其引用，确认新旧内容后再判断迁移；不得将 v4.0a 封面或 2025 首页附到旧条目旁，声称旧版全部定义已获证。DITA 的 2015 原版与 2018 Errata 02 同样需要明确引用对象，不能只保留“1.3”掩盖内容替换。CMU 的 Fall 2025 则保留归档地址，不随根入口自动改成 Fall 2026。

## 本地保留

[本次迁移库存](2026-09-06-source-migration-inventory.json)的 `proposed_local_fields` 给出 24 项精确保留值，当前 `adoption` 全为 pending。建议按以下完整集合集中采纳其表示迁移，不要求逐条重复发起开始许可；采纳记录应明确覆盖该库存基线、字段及原值，不顺带批准外部事实。

| 批次 | 完整对象集合 | 建议值与保留边界 |
|---|---|---|
| subjects 项目判断 | gbt-13745、diataxis、wikidata、roadmap-sh、teachyourselfcs、schema-org、anthropic、openai、moonshot-ai、astral、oxc、uv、pydantic、obsidian | 14 项旧 basis.subjects:self 转为 assertions.subjects；values 逐项沿用库存，disposition:project_assertion、original:self 与原 Git 字段定位保留。全部原 candidate 不升 active，不把既有判断批准为外部归属证据 |
| 本地建立事实 | mathematics、information-and-systems-science、computing、management、linguistics、journalism-and-communication、library-and-information-science、education | 8 项 source:self 转为 assertions.source，保存 disposition:project_assertion、original:self 与库存 migration 定位；不保留外部 source，不改变概念、关系或原 active |
| 载体本地数组 | forms-presentation、forms-activity | 2 项按 Q16 保存 local_analysis：legacy_source_label:lom、state:isolated、decision:decision-source-0011；原父项与成员不变，不产生 external_group 或 structure 资格 |

这些字段保存的是原项目判断与本地分析，不是新做归属或分类。任何集合外对象、values 改动或状态提升都不在这个保留批次中。24 项的 pending 只有在明确采纳后才可更新；库存存在不等于人工已 reviewed，也不解除相邻外部关系的阻断。

## 采纳写集

采纳应分别列明来源字段、角色及具体关系；本报告的结论范围可以集中审阅，但不能用“同意整批”补足明示缺失的事实。已采纳 P1–P4 保持原作用域，其余本文件内容均是提案。

后续可能受影响的是 `data/vocab/entities.yaml`、`data/vocab/sources.yaml`、主题生成输入、类型／体裁／载体与一般实体中的具体关系，以及字段采纳决定。`topics.yaml` 必须通过输入与生成器重建，不直接编辑。所有旧账本保持历史身份、哈希与结论；形式迁移、项目 assertions 与外部 basis 分开。review、watch、history 和真实替代关系仍须各自完成，不能由本文表格默认生成。

本提案本身只新增本文。正式 vault、术语切换、补偿回滚与发版不在写集；正式 v2 数据和消费者完整通过之前，不合并 master。无法表达或缺少必需证据的对象形成明确阻断，不删除对象来制造整批通过，也不发布旧新混合快照。
