# 写作规范 (Writing Conventions)

## 读者与目的

写作规范约束信息的选择、组织和表达，使特定读者能够找到、理解并使用所需内容。它的依据首先是读者与用途。例如，同样介绍一种数据库，评估选型的工程师需要知道并发、部署和维护方面的取舍；执行备份的人需要明确的操作条件与恢复步骤。两种文档可以讨论同一对象，重点却不同。

ISO 24495-1:2023 的公开范围包括技术写作。标准发起组织 IPLF 将其原则概括为相关、可找到、可理解和可使用；这四项关注读者得到的结果，不限定统一文体或篇幅。标准正文未读，这里采用的是公开摘要。[标准范围](https://www.iso.org/standard/78907.html)、[IPLF 摘要](https://www.iplfederation.org/iso-standard/)

读者经验决定哪些信息可以省略，也决定哪些细节值得深入。熟悉软件工程的人仍可能不了解某个数据库的写入限制；重复解释数据库是什么会浪费时间，省略该限制又会妨碍判断。Google 的读者分析同时考虑专业角色与对具体对象的熟悉程度，不能用其中一项代替另一项。[Google Audience](https://developers.google.com/tech-writing/one/audience)

## 文档的分工

文档用途决定信息如何组织。Diátaxis 将动手学习、完成任务、查阅事实和理解原因分别交给教程、操作指南、参考与解释。解释可以讨论历史、设计选择、约束和不同观点，但应限制范围，避免吸收完整操作与参考细节。[Diátaxis Explanation](https://diataxis.fr/explanation/)

例如，一篇工具概述可以解释它为什么适合某种部署方式，并链接安装指南；把全部安装命令插入论证，会让读者在理解设计与执行任务之间来回切换。GitLab 的 Concept 文档规范也把对象及使用价值的介绍与操作任务分开。这支持职责分工，不意味着要复制 GitLab 的篇幅和导航规定。[GitLab Concept](https://docs.gitlab.com/development/documentation/topic_types/concept/)

文档用途与作者立场也不同。帮助读者理解某个对象的文章，可以转述事实，也可以比较方案。类型回答读者怎样使用内容，体裁区分作者怎样处理材料；二者的本库取值与必填要求见[内容模型](../design/model/content-model.md)，不由文体名称自动产生。

## 解释的深度

解释的深度在于揭示结论的依据及成立条件。例如，“这个方案适合离线工作”需要说明数据与计算是否依赖远端服务；“使用起来方便”本身不能支持该结论。Design Docs at Google 和 arc42 将重要设计选择与问题、目标、约束联系起来，提供了工程解释的参考方法。[设计文档实践](https://www.industrialempathy.com/posts/design-docs-at-google/)、[arc42 Solution Strategy](https://docs.arc42.org/section-4/)

第一性原理关注推理的基本出发点。Merriam-Webster 将 first principles 解释为基本或自明的原则；亚里士多德《后分析篇》第一卷第 2 节讨论作为论证起点的首要、直接前提。它与机制描述、设计目标或收益比较并非同一概念。[词典释义](https://www.merriam-webster.com/dictionary/first%20principles)、[《后分析篇》英译本](https://classics.mit.edu/Aristotle/posterior.1.i.html)

工程讨论中的需求、事实和假设需要分别说明，不能统称为自明原则。以笔记存储为例，“不依赖某厂商的服务也能读取”是使用需求；本地文本文件只是候选方案之一，不能由该需求直接证明 Markdown 是唯一选择。进一步判断需要引入格式支持、迁移和维护条件。追问这些前提可以深化理解，但不能补造前提来证明已经选定的产品。

第一性原理分析不要求文章从哲学命题开始。其价值体现在读者能够检查推理起点，而机制与取舍的解释让读者看到由此前提得到什么结论。原作者的设计理由、文档记载的行为与介绍者自己的分析应可区分；今天的功能不能证明当年的动机。

## 结构与表达

文章结构应服务读者要回答的问题。Parnas 与 Clements 批评软件文档跟随想到或执行的顺序堆积，以及多处重复同一事实；他们提出先明确文档回答的问题，再安排信息的位置。这个方法支持连贯、可维护的技术说明，而不要求读者重走作者的探索过程。[论文第 VI–VII 节](https://jpaulgibson.synology.me/~jpaulgibson/TSP/Teaching/Teaching-ReadingMaterial/ParnasClements86.pdf)

例如，部署说明直接给出当前拓扑、适用条件和故障处理；历次尝试及变更记录另有用途。整理正文时可以删除无关讨论，却不能删去决定为何成立的关键限制。Nygard 的 ADR 方法专门保留条件、决定与后果，说明必要历史有自己的文档职责。[ADR 实践](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

简洁是减少读者无须承担的工作。一个明确的版本限制比反复提醒“需要注意兼容性”更有用；准确的技术术语可以缩短表达，未经解释的临时名称则增加理解负担。Microsoft 的风格指南主张重点前置并减少冗词，这不等于专业说明越短越正确。[Microsoft 风格指南](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)

标题、段落、列表和表格各有用途。Google 按内容类型安排标题，按信息的关系选择列表或表格；它并未要求只要有三个对象就使用表格。例如，三个工具名称适合列表，而多个参数的名称、类型和含义构成二维信息。具体媒介可以有自己的版式选择，但不能把选择冒称为普遍规律。[标题指南](https://developers.google.com/style/headings)、[表格指南](https://developers.google.com/style/tables)

## 约束的层次

读者原则、文档方法、语言排版和项目约定处理不同问题。读者原则用于判断信息是否有用；文档方法规定不同用途如何分工；语言与排版规范处理具体表达；项目再根据对象、媒介和权限选择执行规则。它们可以相互支持，但上层原则不能唯一推出所有下层形式。

例如，“便于找到”支持标题明确，却不能独自推出中文标题必须为 2–8 字；中文混排中的视觉间距也不直接规定 Markdown 必须插入哪一个字符。中西文排版的外部依据与本库实现选择见[语言与版式记录](../references/writing-guides.md#语言与版式)。同样，Obsidian 文章禁用表格是用户确定的媒介要求，不是技术写作普遍禁止表格。

术语一致性与命名准入也须分开。统一使用已登记名称可以降低歧义；某个普通词出现在正文中，不表示已经成为项目术语，更不能由写作诊断自动产生概念。例如，软件的名称可以在介绍中转录，但受控实体引用仍需合法身份。[受控词表](controlled-vocabulary.md)、[治理规则](../design/governance/governance.md)

本库的规则分别由[写作规则](../design/governance/writing.md)、[概念文约定](CONVENTIONS.md)和适用的内容设计承担。概念文解释其关系，不改动术语编辑权、内容状态或草案效力。实体介绍的具体取舍另见[未生效草案](../drafts/entity-introductions.md)。

## 权威来源

- [ISO 24495-1:2023](https://www.iso.org/standard/78907.html)公开范围与 [IPLF 摘要](https://www.iplfederation.org/iso-standard/)：读者原则；标准正文未读。
- [Google Audience](https://developers.google.com/tech-writing/one/audience)、[Headings](https://developers.google.com/style/headings)、[Tables](https://developers.google.com/style/tables)及 [Microsoft Top 10](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)：读者分析与表达方式。
- [Diátaxis Explanation](https://diataxis.fr/explanation/)与 [GitLab Concept](https://docs.gitlab.com/development/documentation/topic_types/concept/)：文档用途及范围。
- [Merriam-Webster](https://www.merriam-webster.com/dictionary/first%20principles)与[亚里士多德《后分析篇》第一卷第 2 节](https://classics.mit.edu/Aristotle/posterior.1.i.html)：first principles 的释义及论证前提的原始讨论。
- [Parnas 与 Clements，1986，第 VI–VII 节](https://jpaulgibson.synology.me/~jpaulgibson/TSP/Teaching/Teaching-ReadingMaterial/ParnasClements86.pdf)：技术文档组织。
- [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)、[arc42 Solution Strategy](https://docs.arc42.org/section-4/)与 [Nygard 的 ADR 文章](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)：设计解释和决策记录的实践，按各自场景使用。

阅读位置、限制与既有语言资料见[来源笔记](../references/writing-guides.md)。这些来源提供不同层次的依据，不共同组成一套统一的实体介绍标准。
