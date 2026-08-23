# 主题词表设计

本库的主题词表 `vocab/topics.yaml`:它管什么、长什么样、怎么建、怎么维护。它是一份叙词表——概念、三种关系、到外部词表的映射——不是知识图谱,也不是导航;后两者是它的用法和升级方向,见文末。

理论依据见 [受控词表](../concepts/controlled-vocabulary.md)、[词表的结构](../concepts/vocabulary-structure.md)、[词表的建设与维护](../concepts/vocabulary-construction.md)、[词表映射](../concepts/vocabulary-mapping.md)、[知识体系](../concepts/body-of-knowledge.md)。本文只用这些标准里有的术语;本库自定的术语按 CLAUDE.md 当前阶段不使用。

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
- `information-science` 信息与文献学

### 邻近主题的处理

挨着上述范围的主题,不另立顶层概念,作为某个第 2 层概念的下位收入。每项注明落点和依据,避免相关笔记无处可放。

| 主题 | 落点 | 依据 |
|---|---|---|
| 数学 | `foundations` 下的「数学与统计基础」 | CS2023 知识领域 MSF (Mathematical and Statistical Foundations) |
| 硬件、体系结构 | `foundations` 下的「体系结构与组织」 | CS2023 知识领域 AR (Architecture and Organization) |
| 项目管理 | `engineering` 下的「软件工程管理」 | SWEBOK v4 第 9 章 Software Engineering Management |
| 通用职业技能(写作、沟通、时间管理) | `engineering` 下的「软件工程职业实践」 | SWEBOK v4 第 14 章 Software Engineering Professional Practice |

### 排除范围

目前没有明确排除的主题。候选见待定事项。

### 用途

给本库的笔记打主题标签、做检索、生成导航。单人使用,中文为主,英文别名必备(文献是英文的)。不需要多语种对等,不需要印刷版式。

## 词表的层级结构

树的前三层从知识体系借入,第 4 层起由本库按依据建立。

```
从知识体系借入  第 1 层  顶层概念    computing / information-science
               第 2 层             security / network / content-engineering …
               第 3 层             input-validation / transport-layer / thesauri …
本地建立        第 4 层起           sql-injection / http / facet-analysis …
                                    └─ 可继续细分,如 second-order-sql-injection
```

| | 来源 | 要求 | 状态 |
|---|---|---|---|
| 借入的前三层 | 知识体系的分层结构 | **完整**:该范围每个主要区域都有概念,哪怕尚未用于标引 | 未标引 |
| 本地建立的概念 | 读到什么加什么,从内容抽词 | 准确,不求全 | 候选 → 在用 |

前三层求完整是为了让盲区可见:尚未标引的概念就是「这块还没碰」的提示。这是本库 README 所说「不被已知盲区带偏」的落实,也是 Z39.19 §11.1.3.1(新建词表优先自上而下)和 §11.1.8(允许为补全层级收未标引词)的做法。

### 借入层级的深度

借入的层级取到知识体系中**有稳定编号、可被引用的最深一层**为止:

| 本库的层 | 知识体系的对应层 | 例 |
|---|---|---|
| 第 1 层 | 一级学科 | GB/T 13745 一级学科 870 |
| 第 2 层 | 知识领域 KA | CS2023 17 个 KA;SWEBOK 18 个 KA;GB/T 13745 二级学科 |
| 第 3 层 | 知识单元 KU | CS2023 的 KU;SWEBOK 的 topic;GB/T 13745 三级学科 |

CS2023 的知识单元有代码(如 FPL-Types),其下的主题没有;SWEBOK 的主题有章节号,子主题没有;GB/T 13745 三级学科有代码。三者可引用的层数不同,但对应到本库都落在第 3 层,因此借入到此为止。再往下没有可引用的权威结构,只能按依据从内容里长。Z39.19 §11.1.7 从成本一面支持这条界线:边缘领域的细词让词表难管理,人工建关系的成本高;借得越深,未标引的概念越多。

同一条判据也决定了外部映射的粒度:`match` 只能指向有编号的条目,所以借入概念的映射到第 3 层为止。

本地建立的概念没有深度限制。ISO 25964-1 对层级深度不设上限,具体概念按需要细分。

### 约束

**一个概念的下位,按同一划分特征只取自一个知识体系;不同划分特征可各建一个数组。**
例:`security` 下面,ASVS 按「防御方要验证的控制项」分,CWE 按「软件缺陷类型」分,ATT&CK 按「攻击者战术」分——三个是不同的划分特征,不是同一维度的三种切法。ISO 25964-1 允许一个概念下有多个数组,每个数组前用节点标签注明划分特征:

```
security
  (按验证要求)  ← 数组,来源 ASVS
    认证 / 会话管理 / 输入验证 / …
  (按缺陷类型)  ← 数组,来源 CWE
    注入类缺陷 / 内存安全缺陷 / …
  (按攻击战术)  ← 数组,来源 ATT&CK
    初始访问 / 权限提升 / …
```

`sql-injection` 同时属于「输入验证」和「注入类缺陷」,靠多层级挂在两处;概念仍是一个。
反例:OWASP Top 10 和 CWE 都按缺陷分,Top 10 是 CWE 的子集重组——这是同一划分特征的两种切法,只取一个进树,另一个只做映射。
限制:第二个及以后的数组不默认建。起步每个概念下只建一个数组,其余知识体系只做映射;当确实需要从另一个视角浏览或检索时再建。每多一个数组就多一套未标引概念和一批多层级挂载。

**每个借入的概念注明借自哪里。**
例:

```yaml
- id: FPL-Types
  source: cs2023        # 抄自 CS2023
- id: sql-injection
  source: self          # 本库自己加的
```

`source` 只能是 `vocab/sources.yaml` 里登记过的 id,或 `self`。
用处:CS2023 改版时,查 `source: cs2023` 就知道哪些概念要复核。

**允许多层级。**
例:「Rust 所有权」既属于内存模型又属于 Rust,写 `broader: [FPL-Systems, rust]`。ISO 25964 允许一个概念有多个上位。
列表顺序目前不赋予含义:`[FPL-Systems, rust]` 和 `[rust, FPL-Systems]` 没有区别。以后做导航需要「默认显示在哪个上位下」时再定规则,见待定事项。

### 结构预览

```
computing 计算与信息技术
├─ foundations 计算机科学基础                 ← CS2023
│   ├─ 数学与统计基础                          ← 数学落这里(CS2023 MSF)
│   ├─ 体系结构与组织                          ← 硬件落这里(CS2023 AR)
│   └─ … 其余 CS2023 知识领域
├─ engineering 软件工程                       ← SWEBOK v4
│   ├─ 软件工程管理                            ← 项目管理落这里(第 9 章)
│   ├─ 软件工程职业实践                        ← 通用职业技能落这里(第 14 章)
│   └─ … 其余 SWEBOK 知识领域
├─ security 信息安全                          ← ASVS 5.0
├─ web Web 平台                               ← 待定
├─ ai AI 应用工程                             ← 待定
├─ data 数据                                  ← 待定
├─ network 网络                               ← RFC 1122
├─ programming-languages 编程语言             ← CS2023 FPL
│   ├─ 类型系统、内存与执行模型、范式……         ← 跨语言通识,FPL 知识单元
│   └─ 具体语言                                ← 唯一的术语表:python / rust / …
└─ human-centered-computing 以人为中心的计算  ← CS2023 HCI

information-science 信息与文献学              ← GB/T 13745 一级学科 870
├─ library-science 图书馆学                   ← 870.10  未标引
├─ documentation 文献学                       ← 870.20  未标引
├─ information-science 情报学                 ← 870.30  未标引  ⚠ 与顶层概念 id 冲突
├─ archival-science 档案学                    ← 870.40  未标引
├─ museology 博物馆学                         ← 870.50  未标引
└─ content-engineering 内容工程               ← 本库自加

图例:第 1 层顶层概念,第 2 层,第 3 层(只画了已定的)。
      「←」后是该层取自的知识体系;第 3 层以下不预建。
```

### 第 2 层概念

| id | 首选词 | 第 3 层取自(拟) | 其余映射来源 | 借自 |
|---|---|---|---|---|
| engineering | 软件工程 | SWEBOK v4 知识领域 | roadmap.sh(候选来源) | ACM CCS |
| security | 信息安全 | ASVS 5.0 章节 | CWE、ATT&CK、OWASP Top 10 | ACM CCS |
| web | Web 平台 | 待定:MDN 技术参考的顶层分区 | MDN Curriculum、roadmap.sh | self |
| ai | AI 应用工程 | 待定 | Anthropic 文档、OWASP GenAI、ATLAS、NIST AI RMF | self |
| data | 数据 | 待定:CMU 15-445 大纲或 DB-Engines 类别 | roadmap.sh | ACM CCS |
| network | 网络 | RFC 1122 四层 | OSI、RFC 9110–9114 | ACM CCS |
| foundations | 计算机科学基础 | CS2023 知识领域 | ACM CCS、teachyourselfcs | CS2023 |
| programming-languages | 编程语言 | CS2023 FPL 知识单元;其中「具体语言」为术语表 | — | CS2023 |
| human-centered-computing | 以人为中心的计算 | CS2023 HCI | ACM CCS、roadmap.sh | ACM CCS |
| library-science | 图书馆学 | 待定 | — | GB/T 13745 870.10 |
| documentation | 文献学 | 待定 | — | GB/T 13745 870.20 |
| information-science | 情报学 | 待定 | — | GB/T 13745 870.30 |
| archival-science | 档案学 | 待定 | — | GB/T 13745 870.40 |
| museology | 博物馆学 | 待定 | — | GB/T 13745 870.50 |
| content-engineering | 内容工程 | 待定:按标准族分(术语 / 叙词表 / 元数据 / 结构化写作) | ISO 704、1087、25964、30042、Z39.19、SKOS、DCMI、DITA | self |

「借自」一列区分哪些概念有外部依据、哪些是本库自加的。标「待定」的需要逐个看该知识体系的当前结构后再定。

`information-science` 下的五个概念来自 [GB/T 13745-2009《学科分类与代码》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E)一级学科 870 下的二级学科,全部未标引;`content-engineering` 是本库自加的第六个。顶层概念与其中一个下位同名(information-science / 情报学),id 冲突,待定事项里记了。

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
  arrays: [security-by-requirement]      # 所属数组;上位只有一个数组时可省略
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

一个概念下只有一个数组时可以不登记,下位直接挂 `broader`。

分面字段暂不设,见 [分面字段草案](drafts/kind.md)。

## 生命周期

`status` 的取值全部来自 Z39.19:

| status | Z39.19 | 含义 | 进入 | 离开 |
|---|---|---|---|---|
| `unassigned` | §11.1.8 未标引词 | 为补全层级收入、尚未用于标引 | 借入知识体系的层级时 | 被笔记引用或有下位 → `active` |
| `candidate` | §11.1.6 候选词 | 提出但未审 | 任何时候 | 被 ≥ 3 篇笔记引用且有 scope → `active`;长期无引用 → 删除(候选词可以删) |
| `active` | — | 在用 | 审核通过 | 被替代 → `deprecated` |
| `deprecated` | §11.3.2.1 | 不再用于新标引,保留供检索 | 合并、拆分、改名时 | 不删。必须有 `replaced_by` 和 `history` |

按 Z39.19 §11.3.2:`deprecated` 的词**不删**,旧引用靠它还能找到;只有误建且无任何引用的才物理删除。借入的概念长期 `unassigned` 不删——那是盲区标记;确认不需要时在 `scope` 注明「有意不覆盖」及原因,仍保留。

## 外部映射

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
  role: [mapping]                # mapping = 可作 match 目标;candidate = 只作候选词来源
  version: "4.20"
  checked: 2026-08-20
  url: https://cwe.mitre.org/
```

`role` 区分两类:

- **mapping**:有稳定、可引用的条目(CWE、RFC、ASVS、ACM CCS、SWEBOK、ISO、MDN 页面)
- **candidate**:学习路线、排行榜、课程大纲(roadmap.sh、teachyourselfcs、DB-Engines 榜)。能告诉你什么重要,但条目不稳定无编号,只用来发现词,不作映射目标

复核周期的分档见 [来源分级草案](drafts/sources.md),草案生效前只记 `version` 和 `checked`。

## 建设流程

1. 写「范围与用途」的排除项
2. 逐个确定第 3 层取自的知识体系(表中「待定」的),联网核对其当前结构
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

- 排除范围:候选有自然语言学习、非技术的生活领域;需要确认是否明确排除
- `information-science` 既是顶层概念 id 又是「情报学」的自然译名,二者需区分:顶层改为 `library-and-information-science`,或下位改为 `informatics`
- 第 2 层表中五个「待定」的第 3 层来源
- 多层级时 `broader` 列表的顺序是否赋予含义(显示、排序)
- `security` 是否建第二、第三个数组(CWE、ATT&CK),以及触发条件
- 分面字段,见 [草案](drafts/kind.md)
- 文件格式:YAML 单文件,还是每个第 2 层概念一个文件(概念过几百条时再考虑)
- `related` 的使用规则:什么情况下加、是否要求互反
