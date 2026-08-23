# 主题词表设计

本库的主题词表 `vocab/topics.yaml`:它管什么、长什么样、怎么建、怎么维护。它是一份叙词表——概念、三种关系、到外部词表的映射——不是知识图谱,也不是导航;后两者是它的用法和升级方向,见文末。

理论依据见 [受控词表](../concepts/controlled-vocabulary.md)、[词表的层级](../concepts/vocabulary-hierarchy.md)、[分面](../concepts/facet.md)、[词表的建设与维护](../concepts/vocabulary-construction.md)、[词表映射](../concepts/vocabulary-mapping.md)、[知识体系](../concepts/body-of-knowledge.md)。本文只用这些标准里有的术语;本库自定的术语按 CLAUDE.md 当前阶段不使用。

## 词表的构成总览

```
                          vocab/topics.yaml
 ┌──────────────────────────────────────────────────────────────────┐
 │                                                                  │
 │  概念 = 一个节点,有 ID,名字只是标签                                │
 │                                                                  │
 │     ┌─────────────────────────────┐                              │
 │     │ id:    sql-injection        │ ← 引用用这个,永不改            │
 │     │ label: SQL 注入 / SQL injection   ← 首选词                  │
 │     │ alt:   SQLi                 │ ← 非首选词                     │
 │     │ scope: 用于… 不用于…        │ ← 范围注释                     │
 │     └─────────────────────────────┘                              │
 │                                                                  │
 │  三种关系 = 节点之间的边,只有这三种                                 │
 │                                                                  │
 │     ① 等价  USE/UF     SQLi ──────────▶ sql-injection             │
 │                        (别名指向首选词;在记录内用 alt 表示)          │
 │                                                                  │
 │     ② 层级  BT/NT      security                                  │
 │                          └─ input-validation                     │
 │                               └─ sql-injection   (broader 字段)  │
 │                                                                  │
 │     ③ 相关  RT         sql-injection ◀────▶ parameterized-query  │
 │                        (有关,但说不清怎么有关;related 字段)         │
 │                                                                  │
 │  映射 = 从本地概念指向外部词表的概念                                 │
 │                                                                  │
 │     sql-injection ──exactMatch──▶ CWE-89        (在 cwe 里)       │
 │     sql-injection ──broadMatch──▶ A03:2021      (在 owasp-top10 里)│
 │                        │                                         │
 │                        └── source 必须是 vocab/sources.yaml 的 id  │
 └──────────────────────────────────────────────────────────────────┘

 这份文件 = 叙词表。它能变成什么:

   叙词表 ──渲染成目录──▶ 导航        边不变,只是画成侧边栏 / 面包屑
     │
     └──加带类型的边──▶ 知识图谱      节点复用;边从 2 种变成 N 种:
                                      sql-injection ──mitigated_by──▶ parameterized-query
                                      sql-injection ──instance_of───▶ CVE-2024-xxxx
```

读法:方框里是**一个节点长什么样**;①②③ 是**节点之间允许的全部边**;映射是**节点往外指**;最下面是**这份文件的两个去向**——去向不改节点,只改边。

## 范围与用途

### 覆盖范围

两个顶层概念:

- `computing` 计算与信息技术
- `library-and-information-science` 图书馆、情报与文献学(GB/T 13745 一级学科 870 的名称)

### 邻近主题的处理

挨着上述范围的主题,不另立顶层概念,作为某个第 2 层概念的下位收入。每项注明落点和依据,避免相关笔记无处可放。

| 主题 | 落点 | 依据 |
|---|---|---|
| 数学 | `foundations` 下的「数学与统计基础」 | CS2023 知识领域 MSF (Mathematical and Statistical Foundations) |
| 硬件、体系结构 | `foundations` 下的「体系结构与组织」 | CS2023 知识领域 AR (Architecture and Organization) |
| 项目管理 | `engineering` 下的「软件工程管理」 | SWEBOK v4 第 9 章 Software Engineering Management |
| 通用职业技能(写作、沟通、时间管理) | `engineering` 下的「软件工程职业实践」 | SWEBOK v4 第 14 章 Software Engineering Professional Practice |
| 术语学(ISO 704、1087、30042) | 待定:GB/T 13745 把术语学归语言学(740),本库无此顶层 | — |
| 结构化写作(DITA) | 待定:`engineering` 或 `web` 下某知识单元 | — |

### 排除范围

以下主题不建节点,相关笔记不进本库:

| 主题 | 说明 |
|---|---|
| 自然语言学习 | 英语、日语等语言学习笔记 |
| 课程和书的阅读进度 | 属于个人任务管理,不是知识 |

非技术的生活领域(健康、理财、旅行)尚未决定,见待定事项。

### 用途

给本库的笔记打主题标签、做检索、生成导航。单人使用,中文为主,英文别名必备(文献是英文的)。不需要多语种对等,不需要印刷版式。

## 词表的层级结构

整棵树是[层级](../concepts/vocabulary-hierarchy.md)的结果:每一层按一个划分特征往下分。规则十二条,分四组。

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

### 各层的划分特征

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

「按子领域」出现在多数层:学科树的本质就是逐层按子领域分。artificial-intelligence 下 OWASP GenAI、ATLAS、NIST AI RMF 的划分特征待核后补。

### 结构预览

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

### 第 2 层概念

| id | 首选词 | 第 3 层取自(拟) | 其余映射来源 | 借自 |
|---|---|---|---|---|
| engineering | 软件工程 | SWEBOK v4 知识领域 | roadmap.sh(候选来源) | ACM CCS |
| security | 信息安全 | ASVS 5.0 章节 | CWE、ATT&CK、OWASP Top 10 | ACM CCS |
| web | Web 平台 | MDN 技术参考顶层分区(19 项) | MDN Curriculum(候选来源、派生组)、roadmap.sh | self |
| artificial-intelligence | 人工智能 | CS2023 AI 知识单元(12 个) | Anthropic 文档、OWASP GenAI、ATLAS、NIST AI RMF | CS2023 |
| data | 数据 | CS2023 DM 知识单元(13 个) | CMU 15-445、DB-Engines(候选来源)、roadmap.sh | CS2023 |
| network | 网络 | RFC 1122 四层 | OSI、RFC 9110–9114 | ACM CCS |
| foundations | 计算机科学基础 | CS2023 知识领域 | ACM CCS、teachyourselfcs | CS2023 |
| programming-languages | 编程语言 | CS2023 FPL 知识单元;其中「具体语言」为术语表 | — | CS2023 |
| human-centered-computing | 以人为中心的计算 | CS2023 HCI | ACM CCS、roadmap.sh | ACM CCS |
| library-science | 图书馆学 | GB/T 13745 三级学科(870.10xx) | — | GB/T 13745 870.10 |
| documentation | 文献学 | GB/T 13745 三级学科(870.20xx) | — | GB/T 13745 870.20 |
| information-science | 情报学 | GB/T 13745 三级学科(870.30xx) | ISO 25964、Z39.19、SKOS | GB/T 13745 870.30 |
| archival-science | 档案学 | GB/T 13745 三级学科(870.40xx) | — | GB/T 13745 870.40 |
| museology | 博物馆学 | GB/T 13745 无三级学科 | — | GB/T 13745 870.50 |

「借自」一列区分哪些概念有外部依据、哪些是本库自加的。

`library-and-information-science` 下的五个概念来自 [GB/T 13745-2009《学科分类与代码》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E)一级学科 870 下的二级学科,第 3 层取其三级学科。原拟自加的「内容工程」取消:叙词表与检索语言归 870.3050 情报检索学,分类法归 870.1040 图书分类学,元数据与编目归 870.1045 图书编目学;术语学与结构化写作见邻近主题表。

### 人工智能的下位结构

取 CS2023 知识领域 AI 的 12 个知识单元:Introduction、Search、KRR、LRR、Probability、ML、NLP、Agents、Planning、Vision、Robotics、SEP。它偏学术——机器人、规划与本库侧重的 LLM 应用工程距离较远——但它是唯一有编号的人工智能知识体系;未标引的单元是盲区标记,不是负担。Anthropic 文档、OWASP GenAI、ATLAS、NIST AI RMF 全部作映射来源和派生组,不进树。首选词用「人工智能」而不是原拟的「AI 应用工程」:侧重体现在内容里,不体现在知识体系的边界上。

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

## 概念记录的字段

```yaml
- id: sql-injection                      # 稳定、小写、连字符;一旦引用不改
  label: { zh: SQL 注入, en: SQL injection }
  alt: [SQLi]                            # 非首选词;可检索、可显示
  hidden: []                             # 非首选词;可检索、不显示(拼写错误等)
  broader: [input-validation, data]      # 空列表 = 顶层概念
  arrays: [security-by-requirement]      # 所属数组
  related: []                            # RT
  scope: >                               # 范围注释:用于……不用于……
    指通过拼接用户输入改变 SQL 语义的攻击及对应缺陷;
    参数化查询等防御手段不在此。
  source: self                           # 借入的概念:借自哪个知识体系;本地建立:self
  match:                                 # 到外部词表的映射
    - { source: cwe, id: CWE-89, rel: exactMatch }
    - { source: owasp-top10, id: "A03:2021", rel: broadMatch }
  status: active                         # 生命周期
  added: 2026-08-20
  history: []                            # 历史注释:日期、改了什么、为什么
```

必填:`id` `label.zh` `label.en` `broader` `status` `added`。其余按需。`scope` 对本地建立的概念强烈建议填——它比定义更实用,能防止同一概念被两个人(或半年后的自己)理解成两样。

字段名与标准的对应:`alt` / `hidden` 对应 SKOS `altLabel` / `hiddenLabel`;`broader` `related` 对应 SKOS 同名属性;`arrays` 对应 ISO 25964-1 数据模型的 ThesaurusArray;`scope` 对应 ISO 25964-1 范围注释;`history` 对应历史注释;`status` 对应 ISO 25964-1 数据模型的 `status`。

数组在文件顶部单独登记,对应 ISO 25964-1 数据模型的 ThesaurusArray 与 NodeLabel:

```yaml
arrays:
  - id: security-by-requirement
    superordinate: security             # 数组所属的上位概念
    label: 按验证要求                    # 节点标签:划分特征;不是概念,不能标引
    source: asvs
```

每个有下位的概念都登记数组并写 `label`,哪怕只有一组;规则见「节点标签」。

分面字段暂不设,见 [分面字段草案](drafts/facet-field.md)。

## 生命周期

`status` 的取值全部来自 Z39.19:

| status | Z39.19 | 含义 | 进入 | 离开 |
|---|---|---|---|---|
| `unassigned` | §11.1.8 未标引词 | 为补全层级收入、尚未用于标引 | 借入知识体系的层级时 | 被笔记引用或有下位 → `active` |
| `candidate` | §11.1.6 候选词 | 提出但未审 | 任何时候 | 被 ≥ 3 篇笔记引用且有 scope → `active`;长期无引用 → 删除(候选词可以删) |
| `active` | — | 在用 | 审核通过 | 被替代 → `deprecated` |
| `deprecated` | §11.3.2.1 | 不再用于新标引,保留供检索 | 合并、拆分、改名时 | 不删。必须有 `replaced_by` 和 `history` |

按 Z39.19 §11.3.2:`deprecated` 的词**不删**,旧引用靠它还能找到;只有误建且无任何引用的才物理删除。借入的概念长期 `unassigned` 不删——那是盲区标记;确认不需要时在 `scope` 注明「有意不覆盖」及原因,仍保留。

## 外部知识体系的用法

一个外部知识体系在本库可以有三种用法(理论见[词表映射](../concepts/vocabulary-mapping.md)):

| 用法 | 本库里的形式 | 条件 | 记在哪 |
|---|---|---|---|
| 借入 | 某概念下的一个数组,成员是本地概念,`source` 记来历 | 划分特征与该概念已有数组不同 | `arrays` 登记 + 概念的 `source` |
| 映射 | 概念的 `match` 条目 | 外部有稳定条目 | 概念的 `match` |
| 派生概念组 | 映射到该体系的全部概念 | 已有映射 | `sources.yaml` 的 `role` 含 `group` |

规则:

1. **借入的概念必须映射回源头**。`source: asvs` 只说来历;`match: {source: asvs, id: V6, rel: exactMatch}` 说对应哪一条。改版后章节号可能变,两者不互相替代
2. **映射总是有,借入看需要**。起步每个概念下只借入一个数组;其余体系只映射
3. **升级路径**:映射 → 派生组 → 数组。触发条件:派生组被反复打开、或需要按它的划分特征浏览时,才借入成数组

### 映射关系

概念级映射,不是第 2 层级别的。`rel` 直接用 SKOS 的五种:

| rel | 意思 |
|---|---|
| `exactMatch` | 同一概念,可互换;传递 |
| `closeMatch` | 基本同一;不传递。拿不准时用这个 |
| `broadMatch` | 外部概念更宽 |
| `narrowMatch` | 外部概念更窄 |
| `relatedMatch` | 相关 |

`source` 必须是 `vocab/sources.yaml` 里的 id。`id` 是外部体系里的条目标识(CWE-89、RFC 9110 §8.1、ASVS V5.1),没有编号的写 URL。

## 来源名称规范表

`vocab/sources.yaml`,每个知识体系或外部词表一条。按 ISO 25964-2 §23,它是一份名称规范表:为一致地命名特定实体(这里是各知识体系)的受控词表。`source` 和 `match.source` 只能写这里有的 id。

```yaml
- id: cwe
  name: MITRE Common Weakness Enumeration
  role: [mapping, group]         # 见下
  version: "4.20"
  checked: 2026-08-20
  url: https://cwe.mitre.org/
```

`role` 可多选:

- **mapping**:有稳定、可引用的条目,可作 `match` 目标(CWE、RFC、ASVS、ACM CCS、SWEBOK、ISO、MDN 页面)
- **group**:由映射派生一个概念组,组名即体系名。前提是 `mapping`
- **candidate**:学习路线、排行榜、课程大纲(roadmap.sh、teachyourselfcs、DB-Engines 榜)。条目不稳定无编号,只用来发现词,不作映射目标

复核周期的分档见 [来源分级草案](drafts/sources.md),草案生效前只记 `version` 和 `checked`。

## 建设流程

1. 写「范围与用途」的排除项
2. 逐个核对第 3 层取自的知识体系的当前版本与条目
3. 从该知识体系摘第 3 层,全部 `unassigned`,`source` 注明
4. 把现有约 90 个概念挂到树上:分清哪些其实是第 3 层(并入借入的层级)、哪些是本地概念;本地概念先 `candidate`
5. 建 `sources.yaml`,分 role
6. 校正(自下而上):从现有笔记、书签、文献抽词算频率,和树比对——落不进任何节点的说明借入的层级有缺;某节点下本地概念爆炸说明该细分
7. 分批补 `scope` 和 `match`,逐个第 2 层概念来,不求一次填完

第 3 步由脚本辅助生成初版,人工审。

## 校验规则

`scripts/check-topics`,每次改 `topics.yaml` 后跑:

- 所有 `broader` 指向存在的 id;无环
- `source` 和 `match.source` 在 `sources.yaml` 里
- `deprecated` 必有 `replaced_by`
- `arrays` 指向存在的数组,且该数组的 `superordinate` 在本概念的 `broader` 里
- `label.en` 和 `alt` 在全表内不重复(重复 = 可能是同一概念建了两次)
- 统计:每个第 2 层概念下 `unassigned` 的比例(盲区地图)、`candidate` 被引用次数

## 与导航和知识图谱的关系

| | 关系 |
|---|---|
| 导航 | 把树渲染成目录就是导航;树不依赖界面 |
| 知识图谱 | 现在边只有 `broader` / `related` 两种,节点是概念不是实体,无事实性断言。以后加带类型的边(`depends_on`、`mitigates`)时,节点复用,不重建 |
| 文档类型 `type`、人名、项目名 | 各是独立词表,不进这棵树。有内容后按需建 |

## 待定事项

- 排除范围:非技术的生活领域(健康、理财、旅行)是否排除
- 术语学、结构化写作(DITA)的落点
- 多层级时 `broader` 列表的顺序是否赋予含义(显示、排序)
- `security` 是否建第二、第三个数组(CWE、ATT&CK),以及触发条件
- 分面字段,见 [草案](drafts/facet-field.md)
- 文件格式:YAML 单文件,还是每个第 2 层概念一个文件(概念过几百条时再考虑)
- `related` 的使用规则:什么情况下加、是否要求互反
