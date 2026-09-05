# 来源主题依据

本报告覆盖 25 条已有非 self 来源实体及其 27 个 subjects 值，只提出严格归属依据。既有 subjects、项目状态与身份不变，不重新批准分类，不批准版本、用途或下游关系。25 条均有可说明主题关联的发布者材料；“建议”不是已采纳或正式切换。逐项 before、typed basis、日期、内部主题快照与推断见[结构化记录](2026-09-06-source-subjects.json)。

## 材料范围

先读已有联网、CS2023、OWASP 与文档关系报告。CS2023 复用 2026-09-05 留存官方全文，checked 保留该日；其余材料在 2026-09-06 读取。SWEBOK 特别使用网页工具返回的发布者页面索引文本，直接页面仍为 403；这不是新取得发布者响应字节，不能用来覆盖版本状态。无批量下载、Computer Use 或 OCR。

发布者不需要写出本库内部主题 ID。外部材料证明来源处理什么问题；下表的归属理由是明确的本库解释。无 scope 的主题同时检查既有父项和下位，不能悄悄补造 scope。未发现足以要求改变既有 subjects 的冲突，但这不代表每条来源关系均已核实。

## 逐项建议

| 来源与原归属 | 发布者材料与核对日期 | 范围支持与内部推断 | 限制 |
|---|---|---|---|
| cs2023 → computing | [Executive Summary；Body of Knowledge](https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm)；2026-09-05 | 报告将自身界定为计算机科学课程指南，并说明知识体系由十七个知识领域组成。 **本库推断：**computing 是本库计算机科学技术顶层；课程指南组织这一学科的知识，支持已有主题关联，不表示全部课程只属于一个主题。 | 复用本地完整原始 HTML 与文本；外部观察日期仍为 2026-09-05，本次阅读不是重新联网。 |
| swebok → software-engineering | [About SWEBoK；FAQs / Why is there a SWEBOK guide?](https://www.computer.org/education/bodies-of-knowledge/software-engineering)；2026-09-06 | 发布者说明指南整理软件工程理论与实践中的公认知识、知识领域与参考材料，界定软件工程内容及邻近学科边界。 **本库推断：**本地 software-engineering 是 computing 下的软件工程概念；来源自述的知识范围直接支持此主题。 | 本次取得的是网页工具返回的发布者页面索引文本；直接打开两次为 403。只使用 About 与 FAQ 的学科范围，不采纳索引文本中的最新版本或修订日期。 |
| acm-ccs → computing | [ACM Computing Classification System 2012；Learning Outcome 映射表 IT.1–IT.50](https://ccecc.acm.org/guidance/information-technology-applied/classification-mappings/acm-computing-classification-system-2012)；2026-09-06 | ACM 官方课程委员会页面明确采用 2012 分类，表中跨硬件、软件工程、信息系统、网络、安全及计算理论组织学习结果。 **本库推断：**computing 是广义计算机科学技术顶层；跨这些计算领域的分类应用支持已有归属，不以名称相同作唯一理由。 | ACM DL 和 class-2012 主入口失败；此为同一发布组织的官方应用表，不是全分类原文，不证明所有代码或版本状态。 |
| asvs → security | [What is the ASVS?；More Details on the ASVS](https://owasp.org/www-project-application-security-verification-standard/)；2026-09-06 | 该项目提供 Web 应用技术安全控制验证基础与安全开发要求，覆盖防止漏洞的控制。 **本库推断：**本地 security 的 scope 包含安全编码与安全工程；验证和安全开发属于这两项。 | 范围来自项目说明；章节关系与 5.0／5.0.0 对应另见 OWASP 关系报告。 |
| cwe → security | [About CWE；CWE List / Using the CWE List](https://cwe.mitre.org/about/index.html)；2026-09-06 | 枚举描述会导致漏洞的软件与硬件弱点，并服务于开发者、硬件设计者和安全架构师的消除弱点工作。 **本库推断：**弱点预防及安全架构属于本地 security 的安全编码、安全工程范围。 | 仅核来源主题范围；不批准版本状态、角色或全部下游关系。 |
| attack → security | [页首 MITRE ATT&CK 介绍；ATT&CK Matrix for Enterprise](https://attack.mitre.org/)；2026-09-06 | 知识库整理现实观察中的攻击者战术与技术，用于威胁模型和网络安全方法。 **本库推断：**本地 security 包含安全工程和数字取证，攻击行为知识与威胁分析属于其应用范围。 | 只用页首范围与 Enterprise 身份，不依据当前矩阵推导所选历史版全部技术关系。 |
| owasp-top10 → security | [OWASP Top 10:2021 开篇；The Top 10:2021 List](https://owasp.org/Top10/2021/)；2026-09-06 | 2021 文档面向开发者与 Web 应用安全，概述关键安全风险，包括访问控制、注入、配置等。 **本库推断：**本地 security 的安全编码、安全工程范围覆盖所述应用风险。 | 使用 2021 原版入口，不把 2025 首页当作旧版逐值证据。 |
| owasp-llm-top10 → artificial-intelligence, security | [2025 Top 10 Risk & Mitigations for LLMs and Gen AI Apps 开篇](https://genai.owasp.org/llm-top-10/)；2026-09-06 | 目录范围是生成式 AI 和大语言模型应用开发、部署与管理中的风险、漏洞及缓解。 **本库推断：**artificial-intelligence 对应风险作用的 AI／LLM 对象；security 对应漏洞与缓解。两值是同一已明确范围的不同主题面向，不需要发布者使用内部 ID。 | 目录足以支持来源主题，不足以批准每个风险的 exactMatch；既有 OWASP 关系阻断保持。 |
| atlas → artificial-intelligence, security | [README / MITRE ATLAS Data 开篇；ATLAS Data Format / collection.description](https://github.com/mitre-atlas/atlas-data)；2026-09-06 | 官方仓库说明其数据为针对 AI 系统的攻击者战术、技术和程序知识库。 **本库推断：**artificial-intelligence 对应 AI 系统对象，security 对应攻击与威胁分析；与本地 AI、安全领域相交。 | 官网正文为空，改读官方数据仓库；本地 ATLAS-2026.07.yaml collection.description 另确认同一范围，不据 README 当前代码批准旧版逐项内容。 |
| nist-ai-rmf → artificial-intelligence | [Overview of the AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)；2026-09-06 | 框架旨在管理 AI 对个人、组织与社会的风险，将可信性纳入 AI 产品、服务和系统的设计、开发、使用与评价。 **本库推断：**来源直接处理 AI 生命周期风险，支持 computing 下人工智能主题；不因风险字样新增 security 归属。 | 仅核来源主题范围；不批准版本状态、角色或全部下游关系。 |
| anthropic-docs → artificial-intelligence | [Choose how you build；Messages；Build](https://platform.claude.com/docs/en/home)；2026-09-06 | 平台文档说明模型调用、对话状态、工具循环以及推理、视觉、工具使用等能力的接入。 **本库推断：**以语言模型和智能体接入为主要内容，属于本地人工智能主题的应用材料；不声称它是 AI 理论定义来源。 | 只核文档当前入口范围，不采纳模型版本、产品承诺或整站发行日期。 |
| rfc-1122 → networking-and-communication | [§1 Introduction，原文第 5 页](https://www.rfc-editor.org/rfc/rfc1122.html)；2026-09-06 | 该 RFC 规定互联网协议族主机实现要求，覆盖链路、IP 和传输层，应用层由配套文档处理。 **本库推断：**本地 networking-and-communication scope 明列网络基础、路由、单跳通信等，协议实现要求属于这些范围。 | 不把主体主题判断等同所有旧条款仍有效；更新 RFC 的影响另核。 |
| rfc-9110 → networking-and-communication | [Abstract](https://www.rfc-editor.org/rfc/rfc9110.html)；2026-09-06 | HTTP 是分布式信息系统的应用层协议；文档定义共同体系结构、协议元素及跨版本语义。 **本库推断：**本地 networking-and-communication 明列网络应用；应用层通信协议属于该范围，不因同时用于 Web 改 subjects。 | 仅核来源主题范围；不批准版本状态、角色或全部下游关系。 |
| osi → networking-and-communication | [Abstract](https://www.iso.org/standard/20269.html)；2026-09-06 | 模型为系统互连标准的协调与开发提供共同参照，不是直接实现规格。 **本库推断：**系统互连参考模型支撑网络体系结构，落在本地网络与通信的网络基础范围。 | 只读免费摘要，不宣称读过收费全文或完成全部层次关系复核。 |
| mdn → specialized-platform-development | [Documentation for Web developers；Web technology references](https://developer.mozilla.org/en-US/docs/Web)；2026-09-06 | 入口提供 Web 技术实践指南与 HTML、CSS、JavaScript、Web APIs 的教程和参考，用于构建 Web 文档及应用。 **本库推断：**specialized-platform-development 的本地 scope 明确包含 Web；这些平台开发材料直接覆盖其一个既有子范围。并非要求 MDN 覆盖移动、机器人等全部 SPD 子领域。 | 不把文档一般技术范围当作获准 structure 角色或整站版本。 |
| mdn-curriculum → specialized-platform-development | [The essential skillset for new front-end developers；Modules / Core](https://developer.mozilla.org/en-US/curriculum/)；2026-09-06 | 课程组织前端开发的技能与实践，核心含 Web 标准、HTML、CSS 和 JavaScript。 **本库推断：**本地 SPD 明列 Web；前端课程属于这一平台开发范围，附带软技能不改变课程主体。 | October 2025 为页面更新标记；本判断不把它确认为固定发行版本，也不批准 group 用途。 |
| iso-25964-1 → information-science | [Abstract](https://www.iso.org/standard/53657.html)；2026-09-06 | 标准建议建立和维护供信息检索使用的叙词表，适用于多种信息资源，并提供数据模型和交换格式。 **本库推断：**本地 information-science 标签为情报学，父项为 library-and-information-science；虽无独立 scope，其既有下位含 information-retrieval、information-systems-theory、information-technology。以这些明确的检索与系统内容解释已有广义归属，不新增定义或把整个计算信息系统都归入情报学。 叙词表的检索用途与 information-retrieval 直接相接。 | 仅摘要支持主题范围，不宣称全部条款已读。 |
| iso-25964-2 → information-science | [Abstract](https://www.iso.org/standard/53658.html)；2026-09-06 | 标准处理检索用叙词表与其他词表互操作，并给出词表间映射的建立和维护建议。 **本库推断：**本地 information-science 标签为情报学，父项为 library-and-information-science；虽无独立 scope，其既有下位含 information-retrieval、information-systems-theory、information-technology。以这些明确的检索与系统内容解释已有广义归属，不新增定义或把整个计算信息系统都归入情报学。 词表互操作服务检索，是同一既有主题范围内的组织机制。 | Part 2 使用自身摘要，不复用 Part 1 的范围当作全部证明。 |
| z39-19 → information-science | [Abstract](https://www.niso.org/publications/ansiniso-z3919-2005-r2010)；2026-09-06 | 指南涉及单语受控词表的内容、显示、建设、测试和维护，用于知识组织系统中内容对象的表示。 **本库推断：**本地 information-science 标签为情报学，父项为 library-and-information-science；虽无独立 scope，其既有下位含 information-retrieval、information-systems-theory、information-technology。以这些明确的检索与系统内容解释已有广义归属，不新增定义或把整个计算信息系统都归入情报学。 受控表示支撑情报检索及情报系统中的对象组织。 | 出版摘要可支持材料范围，不用标题中的普通 information 同名推断归属。 |
| skos → information-science | [Abstract；Synopsis](https://www.w3.org/TR/skos-reference/)；2026-09-06 | SKOS 提供共享和连接叙词表、分类表及主题词系统的数据模型，表达概念、标记、层级、集合与映射。 **本库推断：**本地 information-science 标签为情报学，父项为 library-and-information-science；虽无独立 scope，其既有下位含 information-retrieval、information-systems-theory、information-technology。以这些明确的检索与系统内容解释已有广义归属，不新增定义或把整个计算信息系统都归入情报学。 这些机制针对已有知识组织工具的表示与互联；Web 技术实现不排除其情报检索组织用途。 | 不把所有 RDF 应用都认作情报学；仅判断 SKOS 明确的知识组织范围。 |
| cmu-15-445 → data-management | [课程开篇，第 1–4 段](https://15445.courses.cs.cmu.edu/fall2025/)；2026-09-06 | 课程研究数据库管理系统设计实现，列数据模型、存储、索引、事务、恢复、查询和并行体系。 **本库推断：**本地 data-management 是 computing 下 Data Management 知识领域；所列数据库机制构成数据管理核心，而非因课程标题同名推断。 | 仅 Fall 2025 范围，不转到 Fall 2026，也不声称全部课程材料已读。 |
| db-engines → data-management | [One year of DB-Engines.com，开篇与系统概览／排名段；页面站点说明](https://db-engines.com/en/blog_post/21)；2026-09-06 | 网站创办者说明其目标是提供数据库管理系统信息，内容含系统概览、比较与排名；页面站点说明也指关系型及 NoSQL 系统。 **本库推断：**本地 data-management 包含数据库管理的技术范围；介绍和比较这些系统的资料可以关联该主题，不等于排名方法是学科定义。 | 首页读取失败后读取官方 2013 回顾；仅证明网站材料主题，旧规模、访问量和排名不外推为当前事实。 |
| dita → journalism-and-communication | [Abstract；Related work / Part 2；配套 §2.7.1.6 Troubleshooting topic](https://docs.oasis-open.org/dita/dita/v1.3/os/part1-base/dita-v1.3-os-part1-base.html)；2026-09-06 | 2015 原版规范定义用于创作和组织主题信息的文档类型及其组合扩展机制；配套技术内容类型为读者表达故障症状、原因与处理。 **本库推断：**本地 journalism-and-communication 是包含传播学的宽顶层；docs/design/model/topics.md 邻近主题已经明确技术写作属传播、DITA 在此。依据支持技术内容编写与传达这一既有解释，不声称 OASIS 把 DITA 直接分类为新闻学。 | 只判断既有技术传播归属；不改变 subjects，不证明 XML 符合性，不用 Errata 02 代替 2015 原版。 |
| iptc-genre → journalism-and-communication | [Scheme Definition；genre:Analysis / Definition](https://cv.iptc.org/newscodes/genre/)；2026-09-06 | 词表说明体裁表达内容的性质、新闻或智识特征；Analysis 定义直接涉及记者对报道的深入研究。 **本库推断：**本地顶层同时包括新闻学与传播学，新闻内容体裁属于明确的新闻实践范围，不要求整个词表每条都仅属新闻。 | 只证明来源主题；Advice 的语义关系阻断及单条 modified 与整表版本区别继续保留。 |
| lom → education | [IEEE 1484.12.1-2002 标题下范围说明；Standard Committee / Learning Technology](https://standards.ieee.org/ieee/1484.12.1/3294/)；2026-09-06 | 2002 标准规定学习对象元数据实例结构，归属学习技术标准委员会。 **本库推断：**本地 education 为教育学顶层；对学习资源的描述与组织是教学技术材料的组成，不声称标准与整个教育学等同。 | 仅 2002 身份的公开范围；2020 替代及具体 educational 取值另核。 |

## 主题解释

MDN 的落点由本地 SPD scope 明列 Web 支持，不需要把整站硬称为所有专用平台。ISO 两部分、NISO、SKOS 的范围通过既有情报检索及情报系统子项解释，未将英文 information 泛化为一切信息技术。DITA 依原版的创作和组织内容范围及本库既有技术传播解释，未把它冒充新闻报道规范。

## 采纳边界

JSON 的 typed_basis 每个 values 分组明确支持对象，多值来源分别列 AI 与安全两个面向并保留同一材料依据。原紧凑字符串保存在 before；没有批量填入外部状态，也没有将发布者主张与内部归属推断混写。报告不产生已采纳决定、不改正式词表、不替代已有关系报告中的阻断。
