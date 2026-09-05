# 写作规范 (Writing Conventions)

本文解释写作规范的原则、层次和推导方式，以及它与受控词表和本库规则的关系。

## 定义

写作规范是一组面向读者的约定，目的是让读者能找到、理解和使用写出来的内容。它的第一原理是“为读者写”：作者拥有读者尚不知道的背景，写作时要按读者的需要组织信息。

ISO 24495-1:2023 用 plain language 表达这项目标：交流的措辞、结构和设计应让目标读者容易找到所需信息、理解找到的信息并加以使用。标准给出四条原则：

| 原则 | 含义 |
|---|---|
| 相关 relevant | 读者得到需要的信息 |
| 可找到 findable | 读者能轻易找到需要的信息 |
| 可理解 understandable | 读者能轻易理解找到的信息 |
| 可使用 usable | 读者能轻易使用这些信息 |

这四条原则来自 25 个国家、19 种语言的专家共识。本文说明的写作规则都应能归入其中一条。

## 解决的问题

四条原则分别处理读者获取、理解和使用信息时遇到的问题。

| 问题 | 表现 | 原则 |
|---|---|---|
| 找不到 | 标题不说明内容；一节塞进几件事；该在文末的待办混在正文 | 可找到 |
| 读不懂 | 用无准入依据的 designation 命名项目概念；同一概念的项目写法不一致；句子过长；中文标点混用 | 可理解 |
| 用不上 | 一篇文档既解释又规定，读者不知道哪句是规则；条件写在指令后面 | 可使用 |
| 给错了 | 写作者想讲的不是读者需要的；正文预告尚未发生的内容 | 相关 |

项目命名和普通叙述承担不同职责。一个字符串不会仅因首次出现在正文中，就成为项目采用的概念名称；脚本识别到它也只提供复核线索。拟用一个 designation 作为可复用的项目概念名称时，才需要核对准入依据并按治理规则登记。

这些问题的共同根因是作者按自己的知识组织内容，没有按读者完成任务所需的信息组织内容。

## 规范的层次

写作规范由多层约束共同组成。上层给出判据，下层给出做法；下层规则应能归到上层原则。

| 层 | 管什么 | 依据 |
|---|---|---|
| 原则 | 为读者写；用四原则判断规则是否必要 | ISO 24495-1:2023 |
| 中文书面语 | 标点形式和中西文混排间距 | GB/T 15834-2011；W3C《中文排版需求》 |
| 技术写作 | 句、段、标题、列表、表格和链接 | Google、Microsoft 的风格指南 |
| 文档分类 | 文档服务哪类需求，以及不同类型如何分工 | Diátaxis |

中文书面语这一层随语言变化：改用其他语言时，标点和排版规则会变化，面向读者的原则和技术写作约束仍然适用。文档分类先确定一篇文章是解释还是参考，再由其他层约束句段和版式。

## 规则的推导

规则应从原则和读者需要推出。以下各节列出本库中的对应做法。

### 可找到

- 标题单看能知道这节讲什么，采用名词短语，不写参数和实现细节；参数变化不应迫使标题变化
- 有顺序的内容用编号列表，无顺序的内容用项目列表，三个以上相关数据用表格
- 链接文字描述链接目标

### 可理解

- 拟用 designation 命名项目概念时，先核对准入依据；没有依据的形式不采用
- 同一概念采用已登记的首选形式；其他登记形式用于识别和检索，不与概念混为一层
- 普通叙述中的字符串和脚本命中只作为复核线索，不因首次出现而自动取得项目命名身份
- 中文句子使用全角标点，引号使用“ ”，汉字与西文、数字之间保留间距
- 使用主动语态并说清谁在做，删去“一句话”“说白了”等口语强调

### 可使用

- 参考类文档陈述规则和事实，解释类文档讨论概念和理由
- 条件写在指令前面
- 表格前用一句完整的话说明用途

### 相关

- 一篇文档只服务一类需求
- 不预告尚未发生的内容，待办统一放在文末

反过来，从原则和读者需要推不出的规则不应加入。例如，“句子不超过二十字”可能来自某个组织的经验，但四原则不能导出这个固定数字。

## 与受控词表的关系

写作规范要求同一概念的项目命名保持一致；[受控词表](controlled-vocabulary.md)把概念与用于表示概念的形式分开管理。项目采用某个 designation 前，先核对它的准入依据，再把获准的首选形式和其他登记形式关联到相应概念。普通叙述即使出现相同字符串，也不会自动取得这层命名身份。

两者在一致性问题上汇合，但职责不同：写作规范说明为什么要保持一致，受控词表说明概念和登记形式如何支持一致的写作与检索。

## 在知识库中

- `AGENTS.md` 摘要标题和项目命名要求，分别落实可找到与可理解原则
- `docs/concepts/CONVENTIONS.md` 规定概念文的分节和例子，落实相关与可使用原则
- 目录按 Diátaxis 分工：`docs/concepts/` 用于解释，`docs/design/` 和 `docs/references/` 用于参考
- 本库另有“改文章不打补丁，整节重写并核对旧版”的过程规则。它约束写作过程，不是从四原则直接推出的文本规则；依据是本库的实践：局部补丁会让缺口和临时说法继续存在，整节或整篇重写才能暴露并处理它们。该规则记录在 `AGENTS.md` 的“整篇重写”一节
- 四原则的正式展开见 [写作规则](../design/governance/writing.md)

## 权威来源

- [ISO 24495-1:2023 Plain language — Part 1: Governing principles and guidelines](https://www.iso.org/standard/78907.html)。正文未读；定义与四原则据 [International Plain Language Federation 的摘要](https://www.iplfederation.org/iso-standard/)
- [ISO 12616-1:2021 Terminology work in support of multilingual communication — Part 1: Fundamentals of translation-oriented terminography](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso%3A12616%3A-1%3Aed-1%3Av1%3Aen)。本次读取公开的术语和定义，确认概念、designation、term extraction 结果与后续选择相互区分；标准正文未读
- [GB/T 15834-2011《标点符号用法》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=22EA6D162E4110E752259661E1A0D0A8) §4
- W3C [《中文排版需求》Requirements for Chinese Text Layout](https://www.w3.org/TR/clreq/) §6.3.3，Group Note Draft 2026-08-04
- [Google developer documentation style guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)
- [Diátaxis](https://diataxis.fr/)，Daniele Procida
- Plain language 运动的两个节点：英国 [Plain English Campaign](https://www.plainenglish.co.uk/) 于 1979 年由 Chrissie Maher 创立；美国 [Plain Writing Act of 2010](https://www.govinfo.gov/app/details/PLAW-111publ274)，Public Law 111-274
- 阅读笔记：[写作规范阅读笔记](../references/writing-guides.md)
