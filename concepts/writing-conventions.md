# 写作规范 (Writing Conventions)

## 定义

写作规范是一组约定，目的是让读者能找到、理解、使用写出来的东西。它的第一原理是“为读者写”——作者知道的比读者多，写的时候要站到读者那一边。

这条原理有国际标准的表述。ISO 24495-1:2023 把 plain language 定义为：措辞、结构和设计清楚到目标读者能轻易找到所需、理解所找到的、并使用这些信息的交流。它给出四条原则：

| 原则 | 含义 |
|---|---|
| 相关 relevant | 读者得到他们需要的 |
| 可找到 findable | 读者能轻易找到需要的 |
| 可理解 understandable | 读者能轻易理解找到的 |
| 可使用 usable | 读者能轻易使用这些信息 |

这四条是 25 个国家、19 种语言的专家共识，本文之下的一切规则都能归到其中之一。

## 解决的问题

| 问题 | 表现 | 原则 |
|---|---|---|
| 找不到 | 标题不说明内容；一节塞几件事；该在文末的待办混在正文 | 可找到 |
| 读不懂 | 生造的词、同一概念几种写法、长句、半角标点夹在中文里 | 可理解 |
| 用不上 | 一篇文档又解释又规定，读者不知道哪句是规则；条件写在指令后面 | 可使用 |
| 给错了 | 写作者想讲的不是读者要的；预告将来的内容 | 相关 |

根因是同一个：作者在写的时候站在自己这边，而不是读者那边。

## 规范的层次

写作规范不是一份清单，是几层约束叠在一起。上层给判据，下层给做法；下层的每条规则都能归到上层的某条原则。

| 层 | 管什么 | 依据 |
|---|---|---|
| 原则 | 为读者写；四原则作为一切规则的判据 | ISO 24495-1:2023 |
| 中文书面语 | 符号怎么写：标点的形式、中西文混排的间距 | GB/T 15834-2011;W3C《中文排版需求》 |
| 技术写作 | 句、段、标题、列表、表格、链接怎么写 | Google、Microsoft 的风格指南 |
| 文档分类 | 一篇文档是什么类型，各类型怎么写、为什么不能混 | Diátaxis |

中文书面语这一层是语言相关的：换一种语言，标点和排版规则换，原则和技术写作规则不换。文档分类是最上面的结构决定：先定一篇是解释还是参考，再谈句段。

## 规则的推导

规则不是拍脑袋定的，是从原则推出来的。每条原则下举本库的规则：

**可找到**
- 标题单看能知道这节讲什么；名词短语；不写参数和实现细节——参数会变，标题跟着变就找不到了
- 有顺序用编号列表，无顺序用项目列表；三个以上相关数据用表格
- 链接文字描述目标

**可理解**
- 术语从标准取，不生造；同一概念全库一种写法
- 中文句子用全角标点，引号用“ ”
- 汉字与西文、数字之间留间距
- 主动语态，说清谁在做；不用口语强调（“一句话”“说白了”），直接陈述

**可使用**
- 参考类文档只陈述，不掺观点和指导；解释类文档才讨论
- 条件放在指令前面
- 表格前一句话说明用途

**相关**
- 一篇文档只服务一类需求
- 不预告；待办放文末，不混进正文

反过来，推不出的规则不该有。“句子不超过二十字”推不出——它可能来自某个组织的经验，但四原则里没有一条能导出这个数字。

## 与受控词表的关系

“同一概念全库一种写法”是可理解原则的一部分，而它的实现手段就是[受控词表](controlled-vocabulary.md)：一概念一首选词，其他写法作入口。写作规范和词表在这一点上汇合——写作规范说“要一致”，词表说“怎么一致”。

## 在知识库中

- `CLAUDE.md` 的标题规则、术语规则，是可找到和可理解的落实
- `concepts/CONVENTIONS.md` 的分节，是相关和可使用的落实
- 目录按 Diátaxis 划分：`concepts/` 解释，`design/` 参考，`sources/` 参考
- 本库另有一条过程规则“改文章不打补丁，整节重写并核对旧版”。它管的是写作过程，不是文本，四原则推不出它；它的依据是本库的实践——补丁让缺口和临时术语带着文章活下去，重写才会暴露它们。记在 `CLAUDE.md`“整篇重写”
- 四原则的完整展开是 `design/writing.md`

## 权威来源

- [ISO 24495-1:2023 Plain language — Part 1: Governing principles and guidelines](https://www.iso.org/standard/78907.html)。正文未读，定义与四原则据 [International Plain Language Federation 的摘要](https://www.iplfederation.org/iso-standard/)
- [GB/T 15834-2011《标点符号用法》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=22EA6D162E4110E752259661E1A0D0A8) §4
- W3C [《中文排版需求》Requirements for Chinese Text Layout](https://www.w3.org/TR/clreq/) §6.3.3,Group Note Draft 2026-08-04
- [Google developer documentation style guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)
- [Diátaxis](https://diataxis.fr/),Daniele Procida
- Plain language 运动的两个节点：英国 [Plain English Campaign](https://www.plainenglish.co.uk/) 1979 年由 Chrissie Maher 创立；美国 [Plain Writing Act of 2010](https://www.govinfo.gov/app/details/PLAW-111publ274),Public Law 111-274
- 阅读笔记：[写作规范阅读笔记](../sources/writing-guides.md)
