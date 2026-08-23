# 笔记的类型 (Note Types)

## 定义

笔记的类型回答“这条笔记是什么性质的东西”。它不是一根轴：一条笔记同时有体裁（给读者做什么用）、作者立场（是事实还是观点）、成熟度（是随手记还是定稿）、载体（是长文还是速查表）、认知层级（理解到什么深度）。这五根轴各有来源，互不替代；把它们压成一个“类型”字段，是 Diátaxis 四类装不下学习笔记的原因。

## 解决的问题

| 问题 | 表现 | 哪根轴 |
|---|---|---|
| 读者不知道这篇能拿来做什么 | 教程和参考混在一篇 | 体裁 |
| 分不清作者在转述还是在评价 | “心得”和“原理”写在一起，读者把观点当事实 | 作者立场 |
| 半成品和定稿混在一起 | 随手记的片段被当作结论引用 | 成熟度 |
| 找速查找不到 | 一页纸的命令表埋在长文里 | 载体 |
| 不知道自己学到哪一层 | 能复述但不会用，或能用但说不出为什么 | 认知层级 |

## 体裁

体裁按读者的需求分。两套来源：

| 来源 | 取值 | 性质 |
|---|---|---|
| Diátaxis | 教程、操作指南、参考、解释 | 做事 / 认知 × 学习 / 工作的四象限 |
| DITA 1.3 技术内容 | concept、task、reference、troubleshooting、glossary entry | OASIS 标准的 topic 类型 |

两套大体对应：Diátaxis 的教程与操作指南对 DITA 的 task，解释对 concept，参考对 reference；DITA 多出 troubleshooting（排障）和 glossary entry（术语条目），Diátaxis 没有。见[写作规范](writing-conventions.md)。

## 作者立场

作者与内容的关系：转述事实、分析、评价、表达偏好。新闻业有现成的受控词表：IPTC NewsCodes 的 genre 词表，73 个取值，其中与笔记相关的：

| 取值 | IPTC 定义 |
|---|---|
| Background | 为所报事件提供背景与解释 |
| Analysis | 记者深入研究后得出的数据与结论 |
| Opinion | 反映作者观点的评论 |
| Review | 对创作活动或服务的评价 |
| Advice | 对读者个人问题的解答 |

“个人理解”是 Analysis，“心得”“偏好”是 Opinion，“这个工具好不好用”是 Review。把这根轴单独标出来，读者才知道哪些话可以引用、哪些只是作者的看法。野中郁次郎的隐性 / 显性知识是另一种切法：显性知识“正式而系统，易于交流和分享”，隐性知识“高度个人化，难以形式化”；笔记把隐性知识写成显性的过程，正是 SECI 的外化。

## 成熟度

Ahrens 按笔记在工作流里的阶段分三种：

| 类型 | Ahrens 的定义 |
|---|---|
| fleeting note 闪念笔记 | 在忙别的事时快速捕捉想法 |
| literature note 文献笔记 | 读文献时用自己的话记要点并注明出处，存在参考系统里 |
| permanent note 永久笔记 | 永不丢弃，自身包含必要信息，以永久可理解的方式写成，像为出版而写 |

这根轴和内容模型的 `status`（draft / active）相关但不同：`status` 说完成没有，成熟度说它在工作流里是哪一环。Luhmann 的卡片盒是这套方法的源头：“每条笔记只是一个元素，它的价值来自系统内链接与反向链接的网络”。Matuschak 的 evergreen notes 是对永久笔记的质量要求（原子、面向概念、密集链接），是写法不是类型。

## 载体

载体是笔记的物理形式。有出处的两种：

| 载体 | 定义 | 来源 |
|---|---|---|
| 速查表 cheat sheet | 供快速参考的简明笔记集；reference card 的子类 | Wikidata Q2309859、Q2689826；无标准级定义 |
| 札记簿 commonplace book | 把重要或熟知的段落抄录并按主题整理，作为记忆辅助或参考；常附编者自己的想法 | Harvard Library Open Collections |

Cornell 笔记法（Pauk，《How to Study in College》1962）规定的是页面分区和五步（record、reduce、recite、reflect、review），是记法不是载体。

## 认知层级

笔记反映作者对主题理解到什么深度。两套来源：

| 来源 | 层级 |
|---|---|
| Bloom 修订版（Anderson & Krathwohl 2001） | 记忆、理解、应用、分析、评价、创造 |
| SOLO（Biggs & Collis 1982） | 前结构、单点结构、多点结构、关联结构、抽象拓展 |

CS2023 自己用 Bloom 标注每个主题的预期掌握层级。帕累托原则（Juran 1951 年命名为 Pareto principle：“关键的少数与琐碎的多数”）是选材法则，决定先记哪二成，不是笔记的属性。

## 五根轴的关系

一条笔记在每根轴上各取一个值，轴之间不互斥：一篇“FastAPI 依赖注入”的笔记可以是参考（体裁）、Background（立场）、永久笔记（成熟度）、速查表（载体）、应用（认知层级）。

不是每根轴都要标。体裁和作者立场影响读者怎么用，必标；成熟度和 `status` 重叠，可合并；载体只在非长文时标；认知层级是作者对自己的评估，可选。

## 在知识库中的用法

内容模型现在只有一个 `type` 字段取 Diátaxis 四类，它只覆盖体裁。按本文，`type` 应拆成至少两个受控字段——体裁（Diátaxis 或 DITA）和作者立场（IPTC genre 的子集）——加可选的载体和认知层级。具体拆法是设计，见[内容模型](../design/content-model.md)待定事项。

## 权威来源

- Diátaxis：[diataxis.fr](https://diataxis.fr/)
- OASIS [DITA 1.3 Part 2 技术内容 §2.7.1](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/archSpec/technicalContent/dita-technicalContent-InformationTypes.html)：concept、task、reference、troubleshooting、glossary entry
- IPTC [NewsCodes Genre](https://cv.iptc.org/newscodes/genre/) 受控词表
- Nonaka, I. [*The Knowledge-Creating Company*](https://hbr.org/2007/07/the-knowledge-creating-company). Harvard Business Review, 1991（2007 重印）
- Ahrens, S. *How to Take Smart Notes*. 2017, ISBN 9781542866507。三种笔记的定义据 [Zettelkasten 论坛转引](https://forum.zettelkasten.de/)，fleeting 与 permanent 有页码，literature 为转述
- Luhmann, N. *Kommunikation mit Zettelkästen*, 1981；英译 [Communicating with Slip Boxes](https://luhmann.surge.sh/communicating-with-slip-boxes)
- Matuschak, A. [Evergreen notes](https://notes.andymatuschak.org/Evergreen_notes)，博文
- Wikidata [cheat sheet Q2309859](https://www.wikidata.org/wiki/Q2309859)、[reference card Q2689826](https://www.wikidata.org/wiki/Q2689826)
- Harvard Library, [Commonplace Books](https://web.archive.org/web/2015/http://ocp.hul.harvard.edu/reading/commonplace.html)（Wayback 存档）
- Cornell Learning Strategies Center, [The Cornell Note Taking System](https://lsc.cornell.edu/how-to-study/taking-notes/cornell-note-taking-system/)；五步据 [UNE 的材料](https://www.une.edu/sites/default/files/Cornell-Note-Taking-System-041311-PDF-4.pdf)
- Krathwohl, D. R. [*A Revision of Bloom's Taxonomy: An Overview*](https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf). Theory Into Practice 41(4), 2002
- Biggs, J. B., Collis, K. F. *Evaluating the Quality of Learning: The SOLO Taxonomy*. Academic Press, 1982；五级名称据 [Springer 百科条目](https://link.springer.com/rwe/10.1007/978-3-319-77487-9_182-4)
- Juran, J. M. [*The Non-Pareto Principle; Mea Culpa*](https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf), 1974：命名经过的自述
