# 主题词表的层级结构

`vocab/topics.yaml` 的树怎么分层、每层按什么分、从哪借入。整棵树是[层级](../concepts/vocabulary-hierarchy.md)的结果:每一层按一个划分特征往下分。字段、生命周期、流程见[主题词表设计](topics.md);外部来源的登记与用法见[来源名称规范表](sources-registry.md)。

## 规则

十二条,分四组。

### 树的性质

1. 顶层按学科切,理由见[树按学科而非分面的决定](drafts/tree-by-discipline.md)。分面是概念上的横向字段,概念组是视图,都不在树里
2. 允许多层级:`broader` 是列表,顺序不赋予含义。例:「Rust 所有权」`broader: [FPL-Systems, rust]`

### 借入与本地

3. 前三层从知识体系借入,全部以未标引状态建入;第 4 层起由本库按依据建立,深度不限
4. 借入的概念写 `source`,并 `match` 回源头条目——`source` 说来历,`match` 说对应哪一条,改版后章节号可能变,两者不互相替代;本地建立的写 `source: self`

```
从知识体系借入  第 1 层  顶层概念    computing / library-and-information-science
               第 2 层             security / network / information-science …
               第 3 层             input-validation / transport-layer / 情报检索学 …
本地建立        第 4 层起           sql-injection / http / facet-analysis …
```

前三层为什么止于三:借入取到知识体系中**有稳定编号、可被引用的最深一层**。CS2023 的知识单元有代码,其下的主题没有;SWEBOK 的主题有章节号,子主题没有;GB/T 13745 三级学科有代码。三者可引用的层数不同,但都落在第 3 层。再往下没有可引用的权威结构,只能按依据从内容里长。同一条判据决定了 `match` 的粒度:只能指向有编号的条目。

### 数组与划分特征

5. 每个有下位的概念都登记数组,每个数组写节点标签
6. 划分特征必须是兄弟之间的区别属性。判据:能填进「A 和 B 的区别是 ___」。`(按年龄)`:儿童和成人的区别是年龄;`(按知识单元)`:ML 和 NLP 的区别是知识单元——不成立,不是划分特征
7. 划分特征不得是来源名(CS2023)、来源的层级名(知识单元、三级学科)或知识体系名;来源写在数组登记的 `source`
8. 一个数组只有一个划分特征。来源混用了多个特征的,拆成多个数组各自登记。例:SWEBOK 的 18 章混了「工程活动」15 章和「基础学科」3 章,拆两个数组
9. 同一划分特征只取一个来源:OWASP Top 10 和 CWE 都按缺陷分,只取 CWE,Top 10 只做映射。不同划分特征的来源,凡 `role` 含 `mapping` 且有稳定结构的,**起步就各借入一个数组**,借到第 3 层,全部未标引。未标引节点多是目的:它们就是盲区地图。借入来源的进一步条件(分级、版本)留待治理方案
10. 派生概念组是已映射内容的视图,成员只有本库已有的概念,暴露不了盲区;它与借入并存,不能替代借入

### 节点标签写法

11. 划分特征写 `(按 X)`,X 是名词;分面名写 `[X]`,本库的树没有分面层,此形式暂不出现
12. 节点标签不是概念:不能标引、不进术语表、不能做 `broader` 的目标;不为分组层造复合概念(Z39.19 §7.7)

## 各层的划分特征

按规则 6 逐层核过:

| 位置 | 数组 | 来源 |
|---|---|---|
| 顶层之下 | `(按学科门类)` | GB/T 13745 一级学科 |
| computing 之下 | `(按子领域)` | CS2023 / SWEBOK / ACM CCS 的知识领域 |
| library-and-information-science 之下 | `(按子领域)` | GB/T 13745 二级学科 |
| foundations、artificial-intelligence、data、programming-languages、human-centered-computing 之下 | `(按子领域)` | CS2023 各知识领域的知识单元 |
| engineering 之下 | `(按工程活动)`;`(按基础学科)` | SWEBOK v4 第 1–15 章;第 16–18 章 |
| security 之下 | `(按验证要求)`;`(按缺陷类型)`;`(按攻击战术)` | ASVS 5.0 章;CWE 顶层类别;ATT&CK 14 个战术 |
| network 之下 | `(按协议层)` | RFC 1122 四层 |
| web 之下 | `(按技术规范)` | MDN 技术参考 19 个顶层分区 |
| 五个图书情报学科之下 | `(按子领域)` | GB/T 13745 三级学科 |

「按子领域」出现在多数层:学科树的本质就是逐层按子领域分。

## 结构预览

```
(按学科门类)                                  ← GB/T 13745
computing 计算与信息技术
  (按子领域)                                  ← CS2023 / SWEBOK / ACM CCS
  ├─ foundations 计算机科学基础
  │   (按子领域)                              ← CS2023
  │   ├─ 数学与统计基础                        ← 数学落这里(MSF)
  │   ├─ 体系结构与组织                        ← 硬件落这里(AR)
  │   └─ … 其余 CS2023 知识单元
  ├─ engineering 软件工程
  │   (按工程活动)                            ← SWEBOK v4 第 1–15 章
  │   ├─ 软件工程管理                          ← 项目管理落这里(第 9 章)
  │   ├─ 软件工程职业实践                      ← 通用职业技能落这里(第 14 章)
  │   └─ …
  │   (按基础学科)                            ← SWEBOK v4 第 16–18 章
  │   └─ 计算基础 / 数学基础 / 工程基础
  ├─ security 信息安全
  │   (按验证要求)                            ← ASVS 5.0
  │   (按缺陷类型)                            ← CWE 顶层类别
  │   (按攻击战术)                            ← ATT&CK 14 战术
  ├─ web Web 平台
  │   (按技术规范)                            ← MDN 技术参考
  ├─ artificial-intelligence 人工智能
  │   (按子领域)                              ← CS2023 AI
  │   (待核)                                  ← ATLAS、OWASP GenAI
  ├─ data 数据
  │   (按子领域)                              ← CS2023 DM
  ├─ network 网络
  │   (按协议层)                              ← RFC 1122
  ├─ programming-languages 编程语言
  │   (按子领域)                              ← CS2023 FPL
  │   ├─ 类型系统、内存与执行模型、范式……
  │   └─ 具体语言                              ← 唯一的术语表:python / rust / …
  └─ human-centered-computing 以人为中心的计算
      (按子领域)                              ← CS2023 HCI

library-and-information-science 图书馆、情报与文献学
  (按子领域)                                  ← GB/T 13745 二级学科
  ├─ library-science 图书馆学
  │   (按子领域)                              ← GB/T 13745 三级学科
  │   ├─ 图书分类学                            ← 870.1040,分类法落这里
  │   ├─ 图书编目学                            ← 870.1045,元数据与编目落这里
  │   └─ …
  ├─ documentation 文献学
  │   (按子领域)
  ├─ information-science 情报学
  │   (按子领域)
  │   ├─ 情报检索学                            ← 870.3050,叙词表与检索语言落这里
  │   └─ …
  ├─ archival-science 档案学
  │   (按子领域)
  └─ museology 博物馆学                       ← 无三级学科

图例:括号行是节点标签,写划分特征;「←」后是该数组取自的知识体系,记在数组登记的 source。
      第 3 层以下不预建。
```

## 第 2 层概念及其数组

每个第 2 层概念下起步借入的数组。「借自」指该概念本身来自哪个知识体系;数组一列是「划分特征 ← 来源」。

| id | 首选词 | 借自 | 数组 |
|---|---|---|---|
| foundations | 计算机科学基础 | CS2023 | (按子领域) ← CS2023 各知识领域 |
| engineering | 软件工程 | ACM CCS | (按工程活动) ← SWEBOK v4 第 1–15 章;(按基础学科) ← 第 16–18 章 |
| security | 信息安全 | ACM CCS | (按验证要求) ← ASVS 5.0;(按缺陷类型) ← CWE 顶层类别;(按攻击战术) ← ATT&CK 14 战术 |
| web | Web 平台 | self | (按技术规范) ← MDN 技术参考 19 分区 |
| artificial-intelligence | 人工智能 | CS2023 | (按子领域) ← CS2023 AI 12 知识单元;其余待核,见下 |
| data | 数据 | CS2023 | (按子领域) ← CS2023 DM 13 知识单元 |
| network | 网络 | ACM CCS | (按协议层) ← RFC 1122 四层 |
| programming-languages | 编程语言 | CS2023 | (按子领域) ← CS2023 FPL 22 知识单元 + 具体语言术语表 |
| human-centered-computing | 以人为中心的计算 | ACM CCS | (按子领域) ← CS2023 HCI 6 知识单元 |
| library-science | 图书馆学 | GB/T 13745 870.10 | (按子领域) ← 三级学科 870.10xx |
| documentation | 文献学 | GB/T 13745 870.20 | (按子领域) ← 三级学科 870.20xx |
| information-science | 情报学 | GB/T 13745 870.30 | (按子领域) ← 三级学科 870.30xx |
| archival-science | 档案学 | GB/T 13745 870.40 | (按子领域) ← 三级学科 870.40xx |
| museology | 博物馆学 | GB/T 13745 870.50 | 无:GB/T 13745 无三级学科 |

只作映射和候选来源、不借入的体系(OWASP Top 10、MDN Curriculum、roadmap.sh、CMU 15-445、DB-Engines、teachyourselfcs、OSI、RFC 9110–9114、ISO 25964、Z39.19、SKOS)登记在[来源名称规范表](sources-registry.md),不在此表。

`library-and-information-science` 下的五个概念来自 [GB/T 13745-2009《学科分类与代码》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E)一级学科 870 下的二级学科,第 3 层取其三级学科。原拟自加的「内容工程」取消:叙词表与检索语言归 870.3050 情报检索学,分类法归 870.1040 图书分类学,元数据与编目归 870.1045 图书编目学;术语学与结构化写作见[主题词表设计](topics.md)的邻近主题表。

### 人工智能的下位结构

取 CS2023 知识领域 AI 的 12 个知识单元:Introduction、Search、KRR、LRR、Probability、ML、NLP、Agents、Planning、Vision、Robotics、SEP。它偏学术——机器人、规划与本库侧重的 LLM 应用工程距离较远——但它是唯一有编号的人工智能知识体系;未标引的单元是盲区标记,不是负担。首选词用「人工智能」而不是原拟的「AI 应用工程」:侧重体现在内容里,不体现在知识体系的边界上。

OWASP GenAI、ATLAS、NIST AI RMF 按规则 9 处理:有稳定结构的(ATLAS 的战术、OWASP LLM Top 10 的编号条目)各自借入一个数组,划分特征待核后补;Anthropic 文档随产品迭代、无稳定结构,只作映射来源。

### 编程语言的下位结构

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

中文译名为本库所加,英文原名和代码为准。22 个知识单元全部以未标引状态建入,预期多数长期如此(形式语义、逻辑编程等),这是求完整的代价。

语言特性的笔记用多层级挂两处:通识节点和具体语言。例如「Rust 的所有权」的 `broader` 为 `[FPL-Systems, rust]`。按通识检索时它与 GC、引用计数并列;按语言检索时与 Rust 的其他特性并列。

不把语言做成分面字段(`lang: rust`)而做成树节点,是因为语言本身也需要别名(TS / TypeScript)、范围注释和映射,作为概念更合适。

## 待定事项

- artificial-intelligence 下 ATLAS、OWASP GenAI 数组的划分特征
- network 数组的节点标签「按协议层」是本库对 RFC 1122 分层的概括,待核
- 多层级时 `broader` 列表的顺序是否赋予含义(显示、排序)
