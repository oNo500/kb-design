# 写作规范阅读笔记

核对日期：2026-09-05。本文保存来源、实际阅读位置及可支持的结论，供[写作规范](../concepts/writing-conventions.md)解释使用。外部方法、实例与项目选择分开；阅读记录不使规则生效，也不改变正式来源登记。

## 读者与目的

以下资料支持根据读者所需信息选择内容，不支持把所有陌生对象的介绍都写成初学者教程。

| 原始资料与性质 | 实际阅读位置 | 支持的结论 | 使用边界 |
|---|---|---|---|
| [ISO 24495-1:2023](https://www.iso.org/standard/78907.html)，标准信息页；[IPLF 摘要](https://www.iplfederation.org/iso-standard/)，标准发起组织的说明 | ISO Abstract；IPLF Part 1、Based on research and consensus | 标准适用于包括技术写作在内的文档；IPLF 概括相关、可找到、可理解、可使用四原则 | ISO 付费正文未读，四原则的表述据 IPLF，不据摘要声称全文符合性；不能推出固定篇幅或模板 |
| [Google Audience](https://developers.google.com/tech-writing/one/audience)，技术写作课程 | Define your audience、Determine what your audience needs to learn、Vocabulary and concepts、Curse of knowledge | 内容取决于已有知识与目标；专业角色相同不表示熟悉同一技术对象 | 既不能重复读者已知常识，也不能省略对象特有的必要概念 |
| [Diátaxis Explanation](https://diataxis.fr/explanation/)，Daniele Procida 的文档方法 | Explanation and its boundaries、Writing good explanation | 围绕有边界的问题解释背景、联系、原因、替代方式及取舍；防止吸收操作与参考细节 | 不规定统一的实体介绍章节，不要求每篇完成哲学推导 |
| [GitLab Concept](https://docs.gitlab.com/development/documentation/topic_types/concept/)，产品文档规范 | 开篇、Format、Concept topic titles | 聚焦一个对象或概念，说明是什么、为什么使用；与任务说明分工 | 一两段、名词标题及任务链接安排属于 GitLab 场景，不整套外推 |

## 解释与组织

这些资料解释如何使技术文档有长期价值；其原场景决定了可借鉴的范围。

| 原始资料与性质 | 实际阅读位置 | 支持的结论 | 使用边界 |
|---|---|---|---|
| [Parnas 与 Clements，1986](https://jpaulgibson.synology.me/~jpaulgibson/TSP/Teaching/Teaching-ReadingMaterial/ParnasClements86.pdf)，软件工程论文，学术镜像原文 | 第 VI 节 A、B；第 VII 节 | 批评按想到或执行的顺序堆积文档及反复陈述；按必须回答的问题组织内容，使文档准确且可维护 | 讨论软件设计文档；不据此禁止有明确用途的执行记录，不允许虚构设计理由；未通读所引其他论文 |
| [Malte Ubl，Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)，作者对工程实践的说明 | Context and scope、The actual design、Alternatives considered、When not to write a design doc | 背景可假定已有知识；重点是约束下的选择与取舍；完整 API、schema 和实现细节可链接 | 非 Google 官方统一标准；项目方案提案不等于实体介绍，也不是第一性原理的定义 |
| [arc42 Solution Strategy](https://docs.arc42.org/section-4/)，架构文档方法 | Contents、Motivation、Form | 简述关键设计选择，并关联问题、质量目标和约束 | 不要求所有实体介绍包含完整架构、组织决策或表格；本节不是哲学定义 |
| [Michael Nygard，Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)，ADR 实践说明 | Context、Decision、Consequences | 有价值的决定记录保留条件、理由及正负后果 | ADR 的历史职责应保留；文章去掉讨论流水账不等于删除决策证据 |
| [Appropriate Uses For SQLite](https://sqlite.org/whentouse.html)，产品方说明 | 开篇；Client/Server Applications、High Concurrency；选择检查表 | 示例把本地存储、网络访问与写并发条件连接到采用建议 | 只作技术解释实例；不把产品方建议或性能数值当作本库实测结果 |
| [Dan McKinley，Choose Boring Technology](https://mcfunley.com/choose-boring-technology)，工程经验 | Optimize Globally、Choose New Technology, Sometimes | 技术选择需要考虑已有工具、整体运维成本和新增依赖 | 不是写作模板，也不证明成熟技术永远优于新技术 |

## 原理的含义

[Merriam-Webster 的 first principles 条目](https://www.merriam-webster.com/dictionary/first%20principles)将其解释为基本或自明的原则。[亚里士多德《后分析篇》英译本](https://classics.mit.edu/Aristotle/posterior.1.i.html)第一卷第 2 节讨论论证的首要、直接前提，并区分前提与由此前提出的结论。这里只读取相关段落，不概括其全部认识论。

这支持区分推理的起点与后续论证。机制说明、因果解释和方案取舍不能单独充当“第一性原理”的定义。工程论证可以从明确的事实、约束和假设出发，但所选前提不因此成为自明真理。例如，“需要脱离厂商服务读取数据”是某次选择的需求；“所以只能采用 Markdown”并不能由该需求单独推出。

本库要求实体介绍保留第一性原理分析，是用户确定的深度要求。落实为追问关键结论依赖的基本前提，并说明推导；这是项目应用，不是上述词典或工程资料规定的通用文档模板。Cambridge 对应条目本次返回 403，未将其计为已读依据。

## 语言与版式

以下保留原有语言与格式依据，同时限定实际支持范围。

| 来源与阅读位置 | 已核结论或保留记录 | 不能据此推出 |
|---|---|---|
| [Google Highlights](https://developers.google.com/style/highlights)，Tone and content、Language and grammar、Formatting | 主动语态、第二人称、条件先于指令；描述性链接、句首式大小写、代码字体与界面加粗；按序列与数据关系选择列表 | 英文用法不直接规定中文标点；“三个以上对象”不等于必须使用表格 |
| [Google Headings](https://developers.google.com/style/headings)，Heading and title text、Heading and title format | 标题反映内容与用途；概念型标题用名词短语，任务型标题用动词；有层级，不空置，不用视觉格式冒充层级 | 中文标题的 2–8 字限制、全部标题只用名词短语是项目选择，不是原文通则 |
| [Google Tables](https://developers.google.com/style/tables)，List or table、Places not to use tables、Introductory sentences | 表格适合每项包含多份相关数据的二维信息；引导句说明用途；单行场景有例外，单列宜用列表 | 不支持“任意三项信息必须成表”，也不支持 Obsidian 文章禁用表格 |
| [Google Future features](https://developers.google.com/style/future)，正文 | 不提前发布未获其法律顾问批准的未来产品或功能信息 | 不是禁止文章中的全部前瞻导航、自我说明或未来时态 |
| [Microsoft Top 10](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)，全文条目 | 重点前置、减少多余文字、句首式大小写、简化弱表达 | 品牌语气中的简短优先和动词开头，不是所有专业文档的绝对句式 |
| [clreq](https://www.w3.org/TR/2026/DNOTE-clreq-20260901/)，状态、中文与西文混排相关段落 | Group Note Draft；中文正文原则上采用中文标点，混排讨论字距与空白 | 排版尺寸不等于要求源码插入一个固定字符；本库半角空格是实现约定 |
| [GB/T 15834-2011](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=22EA6D162E4110E752259661E1A0D0A8)，旧记录定位 §4.8–4.14 | 保留旧记录对引号、括号、破折号、省略号、连接号和间隔号的阅读范围；本次未重读原文 | 不把旧摘要当作本次全文核实，不用它新增“某种引号在所有情境均禁止”等结论 |

旧概念文所引 [ISO 12616-1:2021](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso%3A12616%3A-1%3Aed-1%3Av1%3Aen)公开术语读取记录继续保留，付费正文未读，本次未重新核对。项目中的 designation、术语抽取与准入分工以现行治理文档为准，不由本次写作资料更新转移编辑权。旧文提到的 Plain English Campaign 和 Plain Writing Act 属于历史背景，对当前推导无必要性，正文不再展开。

## 项目应用

本次规则来源必须分别表述：

- 读者适配、解释边界、按问题组织和说明取舍有上述方法支持；将它们组合为实体介绍规则属于项目推导。
- 资深程序员读者、必须保留第一性原理分析、个人偏好可省略、实体名称作标题及 Obsidian 文章不用表格，来自用户要求。
- 类型、体裁、载体、稳定身份、术语准入和决定权限，来自现行模型与治理，不冒充外部写作规范。

旧笔记中的错误复盘不再承担依据。可核规则进入对应来源说明，其他情况仍由 Git 历史追溯。本文不修改现行治理规则；原文与现行摘要的差异须在适用范围内解释，不能静默扩张为新义务。
