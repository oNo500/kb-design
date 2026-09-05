# 来源联网证据

状态：本轮只读核验及工程集成进行中，不是正式切换完成。核对日期为 2026-09-05。用户已授权重要来源的联网核对，并要求整体完成前不得合并 master；本轮不撤销已有提交，不改正式 vault。

## 已补证据

| 来源 | 实际原文与定位 | 已核结论及影响 |
|---|---|---|
| Diátaxis | [Explanation](https://diataxis.fr/explanation/#admit-opinion-and-perspective)，开篇、boundaries、Admit opinion and perspective | 理解导向、讨论、观点与不同视角均有原文。本库 scope 原先缺“承认观点”的证据已补；具体关系仍与角色批准分开 |
| IPTC | [Analysis](https://cv.iptc.org/newscodes/genre/Analysis)，Concept ID、Definition、modified、retired | 条目 URI 和定义可回查；定义涉及记者对报道做深入研究后得出的结果。仍须保留与个人笔记语境的差别，不能升级为 exactMatch。modified 为 2010-12-15，retired 栏空；不把词表整体日期当条目版本 |
| Wikidata | [Q103994532 固定 revision](https://www.wikidata.org/w/index.php?title=Q103994532&oldid=2530661391)，描述、P31、P856 | 原文对应笔记与知识库软件，官网指向 obsidian.md；revision 2530661391，modified 2026-08-13。可支持软件身份核对，不单独批准 subjects 或把 P31 原始类别机械等同本库宽类 |
| Obsidian 官网 | [产品主页](https://obsidian.md/)，本地笔记、链接与知识库功能 | 与 Wikidata 软件描述及官网标识相互核对，不能替帮助文档或第三方插件取得来源身份 |
| ISO Part 1 | [53657](https://www.iso.org/standard/53657.html)，General information、Life cycle | Published，2011-08，第 1 版；当前阶段为 90.92 待修订。待修订不是已撤回或已被替代；P1 原日期不被本轮日期覆写 |
| ISO Part 2 | [53658](https://www.iso.org/standard/53658.html)，同上 | Published，2013-03，第 1 版，90.92 待修订；没有把修订计划误作新出版版本 |
| NISO | [出版页](https://www.niso.org/publications/ansiniso-z3919-2005-r2010)，Publication type 与 Front Matter | Standard、2010-05-13 与 DOI 均可核；[出版 PDF](https://groups.niso.org/higherlogic/ws/public/download/12591/z39-19-2005r2010.pdf)可取得。不据出版页直接批准全部条款或外部现行状态 |
| SKOS | [规范](https://www.w3.org/TR/skos-reference/)与[发布历史](https://www.w3.org/standards/history/skos-reference/)，版本与历史表 | 历史表最新条目为 2009-08-18 Recommendation；可区分现行规范与被替代的 SKOS Core，未通读勘误 |
| GB/T | [标准平台](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E)，状态、日期与备注；[公共服务平台](https://std.samr.gov.cn/gb/search/gbDetailedCNF?id=71F772D7D0A0D3A7E05397BE0A0AB82A) | 现行，2009-05-06 发布、2009-11-01 实施；备注存在两个修改单，不能忽略其影响 |
| CS2023 | [最终报告入口](https://csed.acm.org/final-report/)及[官方完整 HTML](https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm)，版本过程与 Knowledge Model | 完整 HTML 已取得，记载 2024 年 1 月定稿、3 月编辑。当前 178 个映射的代码与英文名称均能在对应邻近文本中找到；不由此自动批准中文 scope、归属或所有关系 |
| SWEBOK | [官方 PDF](https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf)，封面第 1 页 | 当前文件封面为 v4.0a、August 2026；仓库为 4.0。网页 403 不再作为未读结论，但没有比较全部新版内容，不能自动升级使用版本 |
| ASVS | [项目页](https://owasp.org/www-project-application-security-verification-standard/)，latest stable 与引用说明 | 当前稳定版 5.0.0；推荐在定位中包含版本。仓库 5.0 需明确与该版本的对应，不自动重写已有条目 |
| CWE | [2026 新闻](https://cwe.mitre.org/news/archives/news2026.html)，4.20 发布条目 | 4.20 在 2026-04-30 发布，提供与 4.19.1 的变更入口；不是所有 CWE 定义已逐项复核 |
| ATT&CK | [版本历史](https://attack.mitre.org/resources/versions/)，Current Version | 明确 v19.2 为当前版本，起始日期 2026-04-28；已有版本值有发布者证据 |
| OWASP LLM | [风险目录](https://genai.owasp.org/llm-top-10/)，LLM01:2025 等条目 | 已核到 2025 条目标识与公开目录；未因此批准全部中文译名或具体 scope |
| ATLAS | [官方数据目录](https://github.com/mitre-atlas/atlas-data/tree/main/dist/v6)、[发布说明](https://github.com/mitre-atlas/atlas-data/releases) | 官网正文抽取为空，改核官方 GitHub。目录 API 确认 ATLAS-2026.07.yaml 与 blob 275c840f6e6ccc2b7be9fe8607fdc3344c242a42；数据内容版本与格式版本分开，不把格式 v6 当内容版号 |
| RFC 1122 | [RFC Editor](https://www.rfc-editor.org/info/rfc1122/)，文档标题与关系区 | Internet Standard／STD 3，且有更新它的 RFC；不能把“仍可引用”解释为所有原条款都未被更新 |
| LOM | [IEEE 2002 页](https://standards.ieee.org/ieee/1484.12.1/3294/)与[2020 页](https://standards.ieee.org/ieee/1484.12.1/7699/)，Status、Superseded by／Superseding | 2002 明确为 Superseded，2020 明确替代它且为 Active Standard。2020 不是 XML binding 标准，页面下方另列的 1484.12.3 不能混读；取值差异仍未核 |

## 实质差异

[第 1 号修改单公告](https://std.sacinfo.org.cn/gnoc/queryInfo?id=A65509755454A148CB67F1D4201129E7)的公开附件文本说明：删除管理学下的 6305520，增加 6305521；并在社会学下增加对应人才学分支。本库输入和输出仍使用 `630.5520`，对象为 `talent-studies`、中文“人才学”，上位为 human-resource-development-and-management。

这不是格式空格或简单改名问题。正式处置需区分旧对象的保留、修改单中的新对象及归属变化；不能直接把旧 ID 的含义换掉。本轮没有修改该对象、删除其关系或新增概念。

[第 2 号修改单公告](https://std.sacinfo.org.cn/gnoc/queryInfo?id=81872CE7B67294119EFBB758C2292F03)可确认实施日期 2016-07-30，但附件读取失败；本轮未取得其完整修改内容，不能宣称两个修改单均已全文核对。

## 其余来源

| 来源 | 原发布者证据与结果 | 保留边界 |
|---|---|---|
| acm-ccs | [ACM DL](https://dl.acm.org/ccs)与[ACM 分类入口](https://www.acm.org/publications/class-2012)均读取失败 | 版本和状态未核，不能据旧值补 current |
| owasp-top10 | [项目页](https://owasp.org/www-project-top-ten/)明确当前 2025，2021 为旧版 | 新旧内容差异未核，不自动换版 |
| nist-ai-rmf | [NIST](https://www.nist.gov/itl/ai-risk-management-framework)仍提供 1.0，发布于 2023-01-26，正在修订 | 生成式 AI Profile 不当作替代版 |
| rfc-9110 | [IETF](https://datatracker.ietf.org/doc/rfc9110/)列 Internet Standard、June 2022 及具体废止／更新关系 | 未核勘误；部分废止范围不能扩大成全部 HTTP 标准被取代 |
| osi | [ISO 7498-1](https://www.iso.org/standard/20269.html)确认 1994 版仍现行，并列英文修正版 1996-06 | 未核收费全文 |
| dita | [1.3 最新入口](https://docs.oasis-open.org/dita/dita/v1.3/dita-v1.3-part1-base.html)为 2018 Errata 02，明确取代原 2015 版 | 1.3 分支 Latest 不证明全系列最新，2.0 状态尚未核实 |
| schema-org | [发布列表](https://schema.org/docs/releases.html)与[发布入口](https://schema.org/version/latest)给出 30.0、2026-03-19 | 不把 development 通用提示当发布版；未核全部词条 |
| anthropic-docs | [旧址](https://docs.anthropic.com/)转到[Claude Platform Docs](https://platform.claude.com/docs/en/home) | 2026-08 整站发行标识未证实；产品日志日期不是文档版号 |
| mdn | [Web 文档入口](https://developer.mozilla.org/en-US/docs/Web)可读，单页修改日为 2025-07-29 | 不支持整站版本 2026-08-20，单页日期不能外推整站 |
| mdn-curriculum | [课程页](https://developer.mozilla.org/en-US/curriculum/)写明 October 2025 更新 | 是更新月份，不是编号发行版 |
| roadmap-sh | [主页](https://roadmap.sh/)与[日志](https://roadmap.sh/changelog)支持持续维护性质 | 不把单条日志日期当整站固定版本 |
| teachyourselfcs | [主页](https://teachyourselfcs.com/)明确 May 2020 更新，[2016 版](https://teachyourselfcs.com/2016/)仍可定位 | 不能据此保证 2020 后字节未变化 |
| cmu-15-445 | 根入口现为[Fall 2026](https://15445.courses.cs.cmu.edu/fall2026/)，[Fall 2025](https://15445.courses.cs.cmu.edu/fall2025/)归档仍可读 | 所用学期与当前入口分开，不自动升级已有课程使用版本 |
| db-engines | [排名页](https://db-engines.com/en/ranking)及[官方首页](https://db-engines.com/en/)读取失败 | 无正文证据，当前榜期和更新机制未核 |

## 可复核材料

必要的原始响应及定位保存在 Git 忽略的 `build/source-verification/`：

| 材料 | 稳定标识 |
|---|---|
| Wikidata JSON | revision 2530661391；SHA-256 `a987dc92711ba001d9b4a1e101b86d74ff67d1885f087c98a69958a0e6be3fd1` |
| IPTC HTML 响应 | SHA-256 `5fc6655b6391697506cdb0dd8b41534ce3693e47437b8cbd8cfad35b90ccb0e5` |
| Diátaxis HTML | SHA-256 `3f1b0ebfd270bcc6d4e5b79d1b905e891085c9c90a3bc2ab5ab658124b489f8b` |
| CS2023 完整 HTML | 7,420,138 bytes；SHA-256 `8fc7212255af71eb4458122ccb8a93052601e6a2fff59d7c2f4e2db18081b72e` |
| CS2023 定位表 | `cs2023-code-name-pairs.tsv` 保存 178 项代码、是否邻近英文名称及归一化文本偏移；这是定位证据，不是自动采纳结果 |

首次 CS2023 响应只读到 1,500,000 bytes，已明确标记 truncated，不作为完整材料哈希。后续完整响应单独保存。其他仅经网页工具读取的材料只记录 URL、位置与结果，不伪造未取得的原始字节哈希。

## 执行状态

关键原文缺口已有实质进展，但代码和数据仍须统一合同后整批验证。未核对、访问失败、需要身份判断和已核事实分别保留。此记录不把新观察自动写成字段采纳，不升级来源、角色或概念状态，不改变已经采纳的历史日期；不合并 master。
