# 新主题的分类 (Classifying New Subjects)

## 定义

新主题是文献里已经出现、但任何知识体系或标准里还没有位置的东西：一种新工具、一个刚起名的做法、一篇博文提出的架构。给它分类的问题不是“它该放哪个格子”，而是“分类法怎样容纳它而不重建”。这个问题在分类理论里有一百年的积累，四条原则各管一件事。

## 解决的问题

| 问题 | 表现 | 原则 |
|---|---|---|
| 树上没有它的格子 | 标准按学科分，新工具横跨几个学科 | 分析综合 |
| 不知道该不该给它立类目 | 一篇博文就立一个节点，树很快失控；不立又没处放 | 文献依据 |
| 几种分法争不出对错 | AI 编程工具归 AI 还是归软件工程 | 实用主义 |
| 放不进的东西堆在“其他” | “其他”越来越大，没人管 | 剩余监控 |

## 分析综合

枚举式分类（杜威那种）给每个主题预先分配一个号，新主题出现就得改表。Ranganathan 在 1930 年代面对学科快速增长，提出**分析综合式分类**：先把主题分析成几个基本范畴——人物、物质、能量、空间、时间（PMEST）——再把各范畴的类号综合起来。新主题是旧面的新组合，不需要表上有它的格子。

他把这条写进了分类的准则。**好客准则**（Canon of Hospitality，《Prolegomena》第二版）：类号的构造要允许在数组里无限加入新的同级类号、在链的末端无限加入新类号，而不扰动已有类号。

对知识库的意思：新东西先拆成已有的面。Claude Code 不是树上一个节点，是 `kind: software` + `form: 命令行界面` + `subjects: [人工智能, 工具与环境]` + `vendor: Anthropic`，每个值都是已有的；vibe coding 是“编程”这个动作加上“LLM 智能体”这个施动者，也不需要新格子。见[分面](facet.md)。

## 文献依据

Hulme 1911 年的原则：类目存在的理由是已经有文献需要它，不是逻辑上应该有。推论是分类跟着文献走，不跑到文献前面。一个新主题在文献积累到一定量之前不该有自己的类目；它先作为本地概念挂在最近的借入节点之下，标候选，记下源头文献；引用够了才转正，下位多了才成为类目。

所以“标准里没有它”不是缺陷：标准等文献。本库的词表比标准快一步，但不跑到文献前面。见[词表的建设与维护](vocabulary-construction.md)。

## 实用主义

Hjørland 和 Albrechtsen 1995 年提出领域分析：知识领域是思想或话语共同体，分类反映该共同体的认识论立场和使用目的；换一个目的，分法就该换。没有唯一正确的分类，只有对某个目的好用的分类。

推论有两条。其一，“归 AI 还是归软件工程”没有正确答案，只有“查的时候希望它在哪出现”——多层级和多个 `subjects` 让人不必二选一。其二，分类的质量由检索是否好用判定，不由逻辑是否完美判定；本库按引用计数决定概念去留，是这条原则的实现。见[回流](../design/feedback.md)。

## 剩余监控

Bowker 和 Star 在《Sorting Things Out》（1999）里研究国际疾病分类、种族分类等大型系统，指出每个分类都有“其他”，而且分类一旦运转就变得不可见，没人再问它为什么这样分。Star 和 Bowker 2007 年进一步把**剩余类目**（residual category）——“其他”“杂项”“未分类”——作为分类失效的信号：剩余类目的大小和增长，就是分类需要修订的体温计。

GB/T 13745 每个学科都有“其他学科”类目，不是偷懒，是这个原则的标准做法。治理上的推论：不要消灭“其他”，要监控它——某个节点下的剩余聚集到一定量，就是该拆出新类目的时候，而且那时已经有了文献依据。本库的盲区地图和判断债统计就是剩余监控。见[断言的依据](../design/assertions.md)。

## 在知识库中

四条原则合起来，“标准里没有它怎么办”有一个固定答案：

1. **拆**：先看它能不能由已有的面描述——kind、form、subjects、vendor；多数新工具到此为止，不进主题树
2. **挂**：确实是新主题的，作为本地概念挂在最近的借入节点之下，`status: candidate`，`origin` 指向提出它的文献
3. **等**：按回流的引用计数转正；不因为它热就提前立类目
4. **看**：定期看剩余——`self` 断言、未标引节点、某节点下堆积的候选——聚集处就是下一个类目

## 权威来源

- Ranganathan, S. R. *Prolegomena to Library Classification*, 2nd ed., 1957。好客准则的原文据 [Denton 的摘要](https://www.miskatonic.org/library/prolegomena.html)；PMEST 出自 *Colon Classification*，本文未核原版
- Hulme, E. W. *Principles of Book Classification*, Library Association Record, 1911–12
- Hjørland, B., Albrechtsen, H. [*Toward a new horizon in information science: domain-analysis*](https://asistdl.onlinelibrary.wiley.com/doi/abs/10.1002/(SICI)1097-4571(199507)46:6%3C400::AID-ASI2%3E3.0.CO;2-Y). JASIS 46(6), 1995
- Bowker, G. C., Star, S. L. [*Sorting Things Out: Classification and Its Consequences*](https://mitpress.mit.edu/9780262522953/sorting-things-out/). MIT Press, 1999
- Star, S. L., Bowker, G. C. [*Enacting silence: Residual categories as a challenge for ethics, information systems, and communication*](https://link.springer.com/article/10.1007/s10676-007-9141-7). Ethics and Information Technology 9, 2007
