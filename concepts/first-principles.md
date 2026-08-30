# 第一原理与设计理由 (First Principles and Design Rationale)

本文解释第一原理、设计理由及两者的关系，并说明它们在知识库中的用途。

## 定义

**第一原理**是一门学科中适合作为论证起点的基本命题。这类命题必须真实、居先、直接且不可证明，比结论更可知，并且是结论成立的原因。亚里士多德在《后分析篇》中指出：如果每项知识都依赖证明，而证明的前提又需要证明，论证就会陷入无限倒退或循环；证明链因此必须终止于无需证明的直接起点。他用 `ἀρχή`（archē，本原）指称这样的起点。

作为方法，“从第一原理出发”是在同一学科内找到适当起点，再从这些起点推导结论，而不是仅凭其他场景的做法进行类比。

**设计理由**（design rationale）记录为什么作出一个决定，而不只记录决定的内容。第一原理可以成为设计理由追溯到的最深一层：它说明一条理由最终依赖该学科中的哪些适当起点。

## 解决的问题

第一原理提供推导规则的起点，设计理由保存推导和决定的过程。两者处理的问题如下。

| 问题 | 例子 | 处理方式 |
|---|---|---|
| 规则靠症状堆出来，彼此无关 | 标题出问题就加一条标题规则，用语出问题就加一条用语规则 | 找到共同起点，例如为读者写，再从起点推导规则 |
| 无法判断新规则该不该加 | “要不要禁止加粗内容充当标题？” | 能从已有原理推出就加，推不出就不加 |
| 决定的理由随时间丢失 | 半年后不知道当初为什么把时间降级为元数据字段 | 把理由与决定一起记录 |
| 后来者面对旧决定只能盲从或盲改 | 不知道复制的层级为什么要求完整，随手删了未标引的概念 | 先查理由，再判断原有前提是否仍成立 |
| 方法来自类比，不知道它在新场景是否成立 | 照抄图书馆的做法到个人知识库 | 回到适用学科及其起点，检查前提在新场景中是否成立 |

## 设计理由的传统

IBIS 和 ADR 分别保存论证过程与决定记录，共同说明设计理由可以如何留存。

### IBIS

Kunz 与 Rittel 在 1970 年提出 IBIS，用于处理定义不清、没有唯一正解且存在多方视角冲突的棘手问题（wicked problem）。它用三类节点记录论证：

```
议题 (issue)              要回答的问题
└─ 立场 (position)        对议题的一个回答
   ├─ 支持论据 (argument pro)
   └─ 反对论据 (argument con)
```

IBIS 保存提出过的立场、支持与反对论据以及最终选择，因此记录的是论证过程，不只是结论。

### ADR

Nygard 在 2011 年提出架构决策记录（Architecture Decision Record，ADR），把设计理由落实为每个决定一份短记录。记录包含以下内容：

| 字段 | 内容 |
|---|---|
| 标题 | 名词短语 |
| 状态 | 提议、采纳、废弃或被替代 |
| 背景 | 中立描述当时的技术、组织和项目约束 |
| 决定 | 用主动语态写明采取的方案 |
| 后果 | 记录正面、负面和中性的结果 |

过去的决定记录不删除。决定被推翻时，原记录保留并标为“被替代”，再指向新记录。这样既能看到现行决定，也能追溯旧决定保护过什么、后来为什么改变。

Nygard 的动机是保存决定背后的理由。没有这些记录，后来者容易在环境变化后仍盲从旧决定，或在不了解原有约束时盲目改动。

## 原理与理由

```
设计理由             为什么这样决定
│
├─ 直接理由           因为要解决 X 问题
├─ 更早的理由         因为 X 问题来自 Y 约束
└─ 第一原理           同一学科中适当、直接且不可证明的起点
```

ADR 通常记录直接理由和当时约束。继续追溯可以检查这些理由最终依赖哪些第一原理。这样做的作用不是增加哲学说明，而是提供判据：新规则只有能从已登记的原理推出，才有加入的理由。

## 在知识库中的用法

1. 采用一种方法前，先确认它要解决的问题、适用的学科和来源，再寻找该学科中支撑它的适当起点。
2. 追溯在同一学科内到适当、直接且不可证明的起点为止。一个命题是否被广泛接受，或本次论证是否继续展开，都不能单独构成停止条件。
3. 本库的设计文档记录规则及其理由；决定记录只追加。决定被推翻时保留原记录，并用新的决定记录建立替代关系。
4. 新规则应能从已登记的原理推出。推不出时，要么现有原理存在需要另行处理的缺口，要么不加入这条规则。

## 权威来源

- Aristotle. [*Posterior Analytics*](https://classics.mit.edu/Aristotle/posterior.1.i.html) I.2–3、I.6–7。本次读取这些部分关于适当、直接、不可证明的基本命题，以及无限倒退、循环证明和学科边界的论述
- Aristotle. [*Posterior Analytics*](https://classics.mit.edu/Aristotle/posterior.2.ii.html) II.19。本次读取直接起点如何由归纳而为人所知的论述
- Mendell, H. [*Aristotle and Mathematics*](https://plato.stanford.edu/entries/aristotle-mathematics/), Stanford Encyclopedia of Philosophy, §2。本次读取第一原理与各门学科论证结构的说明
- Smith, R. [*Aristotle's Logic*](https://seop.illc.uva.nl/entries/aristotle-logic/), Stanford Encyclopedia of Philosophy, §6.1–6.4（官方镜像；主站 `plato.stanford.edu` 同文）
- Kunz, W., Rittel, H. W. J. [*Issues as Elements of Information Systems*](https://cognexus.org/IBIS-A_Tool_for_All_Reasons.pdf). Working Paper 131, UC Berkeley, 1970（链接为 Conklin 对 IBIS 的综述，含原文引用；原文 PDF 地址本次未能访问）
- Nygard, M. [*Documenting Architecture Decisions*](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions). Cognitect, 2011-11-15
- [adr.github.io](https://adr.github.io/)：ADR 的模板与工具汇总
