# 主题词表的层级结构

主题词表的树分四层以上:前三层从知识体系借入,第 4 层起本地建立。每一层按一个划分特征往下分;一个概念下按几个划分特征分,就有几个数组,每个数组有节点标签说明按什么分。本文定这棵树的分层规则、每层的划分特征、每个第 2 层概念下借入哪些数组。

概念记录的字段在[主题词表设计](topics.md),来源的登记在[来源名称规范表](sources-registry.md)。理论依据见 [词表的层级](../concepts/vocabulary-hierarchy.md)、[知识体系](../concepts/body-of-knowledge.md)、[树按学科而非分面的决定](drafts/tree-by-discipline.md)。

## 规则

十五条,分四组。借入与分析分两层的理由见[借入照抄与本地分析分层的决定](drafts/borrow-and-analyze.md)。

### 树的性质

1. 顶层按学科切,理由见[树按学科而非分面的决定](drafts/tree-by-discipline.md)。分面是概念上的横向字段,概念组是视图,都不在树里
2. 允许多层级:`broader` 是列表,顺序不赋予含义。例:「Rust 所有权」`broader: [FPL-Systems, rust]`

### 借入

3. **可借入的来源**:[来源名称规范表](sources-registry.md)中 `role` 含 `structure` 的。分级与版本方面的进一步要求留待治理方案
4. **顶层由范围决定,顶层之下起步全借**:顶层概念是[范围](topics.md)声明的学科,`source: self`,各自 `match` 到 GB/T 13745;顶层之下,每个可借入的来源在它对应的概念下全部以未标引状态建入。未标引节点多是目的——它们就是盲区地图。范围之内求完整,范围之外不存在
5. **借入深度**:借到第 3 层,即知识体系中有稳定编号、可被引用的最深一层。CS2023 的知识单元有代码,其下的主题没有;SWEBOK 的主题有章节号,子主题没有;GB/T 13745 三级学科有代码——都落在第 3 层。再往下没有可引用的权威结构

```
从知识体系借入  第 1 层  顶层概念    computing / library-and-information-science
               第 2 层             security / network / information-science …
               第 3 层             input-validation / transport-layer / 情报检索学 …
本地建立        第 4 层起           sql-injection / http / facet-analysis …
```

6. **借入照抄**:借入的概念作为上位的下位集合原样保留,成员、顺序按来源,不拆、不改、不配节点标签
7. **借入的记录**:概念写 `source`,并 `match` 回源头条目。`source` 说来历,`match` 说对应哪一条;改版后章节号可能变,两者不互相替代
8. **本地建立**:第 4 层起由本库按依据建立,深度不限,`source: self`。派生概念组的成员只有本库已有的概念,暴露不了盲区,不替代借入

### 数组

9. **数组是可选的**。一个概念的下位默认是一个集合;只在需要区分成几组时登记数组。数组只分组,不改概念
10. **按来源分组**:一个概念的下位来自多个来源时,每个来源的下位登记为一个数组,标识是 `source`。例:security 下 ASVS、CWE、ATT&CK 各一个
11. **按划分特征分组**:可对下位集合做分析,每个划分特征一个数组,标识是 `characteristic`。划分特征是本库自定,必须按[划分特征治理](drafts/division-characteristics.md)登记,通过判据「A 和 B 的区别是 ___」,且完备划分
12. 一个概念在同一划分特征下只属一组,在不同划分特征下可各属一组(ISO 25964-1 数据模型 `isMemberOfArray 0..*`)
13. **同一视角只取一个来源**:两个来源对同一批东西做同一种划分时只借一个,另一个只做映射。OWASP Top 10 与 CWE 都是缺陷清单,取 CWE

### 节点标签

14. 只有以划分特征为标识的数组写节点标签,形式 `(按 X)`,X 是名词;以来源为标识的数组显示来源名,那是标识不是节点标签。分面名 `[X]` 的形式本库暂不出现
15. 节点标签不是概念:不能标引、不进术语表、不能做 `broader` 的目标;不为分组层造复合概念(Z39.19 §7.7)

## 各概念下的来源

每个概念的下位从哪些来源借入。一个来源一行;一个概念下多于一个来源时,各来源的下位各成一个数组(规则 10)。分析层数组目前没有。

| 概念 | 下位来源 | 借到 |
|---|---|---|
| (根) | 范围声明的八个学科,`source: self`,各 `match` GB/T 13745 一级学科 | 第 1 层 |
| mathematics | GB/T 13745 二级学科 110.xx | 第 2 层 |
| information-and-systems-science | GB/T 13745 二级学科 120.xx | 第 2 层 |
| computing | 待定,见下 | 第 2 层 |
| management | GB/T 13745 二级学科 630.xx | 第 2 层 |
| linguistics | GB/T 13745 二级学科 740.xx | 第 2 层 |
| journalism-and-communication | GB/T 13745 二级学科 860.xx | 第 2 层 |
| library-and-information-science | GB/T 13745 二级学科 870.10–870.50 | 第 2 层 |
| education | GB/T 13745 二级学科 880.xx | 第 2 层 |
| 以上六个新顶层的二级学科之下 | GB/T 13745 三级学科 | 第 3 层 |
| foundations | CS2023 相关知识领域(待定,见下) | 第 3 层 |
| engineering | SWEBOK v4 18 章 | 第 3 层 |
| security | ASVS 5.0 章;CWE 顶层类别;ATT&CK 14 个战术——三个数组 | 第 3 层 |
| web | MDN 技术参考 19 个顶层分区 | 第 3 层 |
| artificial-intelligence | CS2023 AI 12 个知识单元;ATLAS 战术;OWASP LLM Top 10——三个数组,后两个待核 | 第 3 层 |
| data | CS2023 DM 13 个知识单元 | 第 3 层 |
| network | RFC 1122 四层 | 第 3 层 |
| programming-languages | CS2023 FPL 22 个知识单元 + 具体语言术语表——两个数组 | 第 3 层 |
| human-centered-computing | CS2023 HCI 6 个知识单元 | 第 3 层 |
| library-science | GB/T 13745 三级学科 870.10xx | 第 3 层 |
| documentation | GB/T 13745 三级学科 870.20xx | 第 3 层 |
| information-science | GB/T 13745 三级学科 870.30xx | 第 3 层 |
| archival-science | GB/T 13745 三级学科 870.40xx | 第 3 层 |
| museology | 无三级学科 | — |

**computing 的第 2 层是未解决的问题。** 现在的九个概念(engineering、security、web……)是本库原表里的,「借自」有 ACM CCS、CS2023、self 三种——这一层不是从某个体系整体借入的,违反规则 4 和 13;顶层之下必须全借,所以「承认为 self」不成立。剩下的选择是借哪个体系:CS2023 的 17 个知识领域(foundations 拆散,web 降为 SPD 下的知识单元,多出 OS、PDC、GIT 等盲区节点),或 GB/T 13745 520 的二级学科(与其他七个顶层一致,但 GB 对计算机的划分偏旧),或 ACM CCS 顶层类目。待定。

只作映射和候选来源、不借入的体系登记在[来源名称规范表](sources-registry.md)。

`library-and-information-science` 下的五个概念来自 [GB/T 13745-2009《学科分类与代码》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E)一级学科 870 下的二级学科,第 3 层取其三级学科。原拟自加的「内容工程」取消:叙词表与检索语言归 870.3050 情报检索学,分类法归 870.1040 图书分类学,元数据与编目归 870.1045 图书编目学;术语学与结构化写作见[主题词表设计](topics.md)的邻近主题表。

## 结构预览

```
(根)                                           ← 范围声明,八个顶层
├─ mathematics 数学                            ← GB/T 13745 110;二级、三级学科待借入
├─ information-and-systems-science 信息科学与系统科学   ← 120;待借入
├─ computing 计算机科学技术                    ← 520;第 2 层来源待定,见下
├─ management 管理学                           ← 630;待借入
├─ linguistics 语言学                          ← 740;待借入
├─ journalism-and-communication 新闻学与传播学  ← 860;待借入
├─ library-and-information-science 图书馆、情报与文献学   ← 870;见下
└─ education 教育学                            ← 880;待借入

computing 计算机科学技术                        ← GB/T 13745 520
  ├─ foundations 计算机科学基础                 ← 第 2 层来源待定
  │   ├─ 数学与统计基础                          ← CS2023 MSF;数学落这里
  │   ├─ 体系结构与组织                          ← CS2023 AR;硬件落这里
  │   └─ …
  ├─ engineering 软件工程                       ← SWEBOK v4 18 章
  │   ├─ 软件工程管理                            ← 第 9 章;项目管理落这里
  │   ├─ 软件工程职业实践                        ← 第 14 章;通用职业技能落这里
  │   └─ …
  ├─ security 信息安全
  │   [ASVS 5.0]                               ← 数组,以来源为标识
  │   [CWE 顶层类别]
  │   [ATT&CK 14 战术]
  ├─ web Web 平台                               ← MDN 技术参考 19 分区
  ├─ artificial-intelligence 人工智能
  │   [CS2023 AI 12 知识单元]
  │   [ATLAS]                                  ← 待核
  │   [OWASP LLM Top 10]                       ← 待核
  ├─ data 数据                                  ← CS2023 DM 13 知识单元
  ├─ network 网络                               ← RFC 1122 四层
  ├─ programming-languages 编程语言
  │   [CS2023 FPL 22 知识单元]
  │   [具体语言]                                ← 术语表:python / rust / …
  └─ human-centered-computing 以人为中心的计算  ← CS2023 HCI 6 知识单元

library-and-information-science 图书馆、情报与文献学   ← GB/T 13745 870
  ├─ library-science 图书馆学                   ← 870.10xx 三级学科
  │   ├─ 图书分类学                              ← 870.1040;分类法落这里
  │   ├─ 图书编目学                              ← 870.1045;元数据与编目落这里
  │   └─ …
  ├─ documentation 文献学                       ← 870.20xx
  ├─ information-science 情报学                 ← 870.30xx
  │   ├─ 情报检索学                              ← 870.3050;叙词表与检索语言落这里
  │   └─ …
  ├─ archival-science 档案学                    ← 870.40xx
  └─ museology 博物馆学                         ← 无三级学科

图例:「←」后是下位的来源。方括号行是以来源为标识的数组,出现在一个概念下有多个来源时。
      分析层数组(按划分特征)目前没有;有了才出现 (按 X) 形式的节点标签。第 3 层以下不预建。
```

## 人工智能与编程语言

### 人工智能

取 CS2023 知识领域 AI 的 12 个知识单元:Introduction、Search、KRR、LRR、Probability、ML、NLP、Agents、Planning、Vision、Robotics、SEP。它偏学术——机器人、规划与本库侧重的 LLM 应用工程距离较远——但它是唯一有编号的人工智能知识体系;未标引的单元是盲区标记,不是负担。首选词用「人工智能」而不是原拟的「AI 应用工程」:侧重体现在内容里,不体现在知识体系的边界上。

LLM 应用相关的外部体系按规则 3、4、10 处理:ATLAS 的战术、OWASP LLM Top 10 的编号条目有稳定结构,各自借入为一个以来源为标识的数组,结构待核;NIST AI RMF 的四个功能是治理职能不是知识划分,只作映射;Anthropic 文档随产品迭代,只作映射。

### 编程语言

编程语言有跨语言的通识——类型系统、内存模型、求值与并发模型、范式——具体语言只是这些概念的不同取舍。因此 `programming-languages` 的下位不是语言的术语表,而是 [CS2023](https://ieeecs-media.computer.org/media/education/reports/CS2023.pdf) 知识领域 FPL (Foundations of Programming Languages) 的 22 个知识单元,再加一个「具体语言」作为其中唯一的术语表:

```
programming-languages
├─ FPL-OOP          面向对象编程
├─ FPL-Functional   函数式编程
├─ FPL-Logic        逻辑编程
├─ FPL-Scripting    Shell 脚本
├─ FPL-Event-Driven 事件驱动与响应式编程
├─ FPL-Parallel     并行与分布式计算
├─ FPL-Aspect       面向切面编程
├─ FPL-Types        类型系统
├─ FPL-Systems      系统执行与内存模型
├─ FPL-Translation  语言翻译与执行
├─ FPL-Syntax       语法分析
├─ FPL-Semantics    编译器语义分析
├─ FPL-Analysis     程序分析与分析器
├─ FPL-Code         代码生成
├─ FPL-Run-Time     运行时行为与系统
├─ FPL-Abstraction  程序抽象与表示
├─ FPL-Constructs   高级程序构造
├─ FPL-Pragmatics   语言语用
├─ FPL-Formalism    形式语义
├─ FPL-Design       编程语言设计原则
├─ FPL-Methodologies 形式化开发方法
├─ FPL-SEP          社会、伦理与职业
└─ languages        具体语言(术语表)
    ├─ python
    ├─ typescript
    ├─ rust
    └─ go
```

中文译名为本库所加,英文原名和代码为准。22 个知识单元全部以未标引状态建入,预期多数长期如此(形式语义、逻辑编程等),这正是规则 4 的目的。

语言特性的笔记用多层级挂两处:通识节点和具体语言。例如「Rust 的所有权」的 `broader` 为 `[FPL-Systems, rust]`。按通识检索时它与 GC、引用计数并列;按语言检索时与 Rust 的其他特性并列。

不把语言做成分面字段(`lang: rust`)而做成树节点,是因为语言本身也需要别名(TS / TypeScript)、范围注释和映射,作为概念更合适。

## 待定事项

- computing 的第 2 层来源:CS2023 17 个知识领域、GB/T 13745 520 二级学科、ACM CCS 顶层类目,三选一
- 六个新顶层(110、120、630、740、860、880)的二级、三级学科清单待从 GB/T 13745 取
- artificial-intelligence 下 ATLAS、OWASP LLM Top 10 的结构核对
- 多层级时 `broader` 列表的顺序是否赋予含义(显示、排序)
- 分析层数组何时启用,见[划分特征治理](drafts/division-characteristics.md)
