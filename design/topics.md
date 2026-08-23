# 主题词表设计

本库的主题词表 `vocab/topics.yaml`:它管什么、长什么样、怎么建、怎么维护。它是一份叙词表——概念、三种关系、到外部词表的映射——不是知识图谱,也不是导航;后两者是它的用法和升级方向,见文末。

理论依据见 [受控词表](../concepts/controlled-vocabulary.md)、[词表的层级](../concepts/vocabulary-hierarchy.md)、[分面](../concepts/facet.md)、[词表的建设与维护](../concepts/vocabulary-construction.md)、[词表映射](../concepts/vocabulary-mapping.md)、[知识体系](../concepts/body-of-knowledge.md)。树的分层规则单独成篇:[层级结构](hierarchy.md);外部来源的登记与用法:[来源名称规范表](sources-registry.md)。本文只用这些标准里有的术语;本库自定的术语按 CLAUDE.md 当前阶段不使用。

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

见[主题词表的层级结构](hierarchy.md):十二条规则、各层的划分特征、结构预览、每个第 2 层概念下借入的数组。

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

每个有下位的概念都登记数组并写 `label`,哪怕只有一组;规则见[层级结构](hierarchy.md)规则 5–12。

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

见[来源名称规范表](sources-registry.md):`vocab/sources.yaml` 的结构、`role` 的取值、借入 / 映射 / 派生组三种用法、映射关系的五种 `rel`。

## 建设流程

1. 写「范围与用途」的排除项
2. 逐个核对各数组来源的当前版本与条目,登记进 `sources.yaml`
3. 按[层级结构](hierarchy.md)的数组表,从各来源摘第 3 层,全部 `unassigned`,`source` 注明,并 `match` 回源头
4. 把现有约 90 个概念挂到树上:分清哪些其实是第 3 层(并入借入的层级)、哪些是本地概念;本地概念先 `candidate`
5. 校正(自下而上):从现有笔记、书签、文献抽词算频率,和树比对——落不进任何节点的说明借入的层级有缺;某节点下本地概念爆炸说明该细分
6. 分批补 `scope` 和 `match`,逐个第 2 层概念来,不求一次填完

第 3 步由脚本辅助生成初版,人工审。

## 校验规则

`scripts/check-topics`,每次改 `topics.yaml` 后跑:

- 所有 `broader` 指向存在的 id;无环
- `source` 和 `match.source` 在 `sources.yaml` 里
- `deprecated` 必有 `replaced_by`
- `arrays` 指向存在的数组,且该数组的 `superordinate` 在本概念的 `broader` 里
- 每个有下位的概念至少登记一个数组,每个数组有 `label`
- `source` 不是 `self` 的概念必有一条 `match` 指向同一来源
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
- 分面字段,见 [草案](drafts/facet-field.md)
- 文件格式:YAML 单文件,还是每个第 2 层概念一个文件(概念过几百条时再考虑)
- `related` 的使用规则:什么情况下加、是否要求互反
