# 主题词表设计

`vocab/topics.yaml` 是本库的主题词表:一份叙词表,由概念、概念之间的三种关系、概念到外部词表的映射构成。它给笔记打主题标签、做检索、生成导航。它不是知识图谱,也不是导航——那两者是它的用法和升级方向。

本文讲这份词表管什么、一条记录长什么样、怎么建、怎么查错。树怎么分层在[层级结构](hierarchy.md),外部来源怎么登记在[来源名称规范表](sources-registry.md)。理论依据见 [受控词表](../concepts/controlled-vocabulary.md)、[词表的建设与维护](../concepts/vocabulary-construction.md)。

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

顶层概念由范围决定,不借入。取 GB/T 13745-2009 一级学科中的八个,各自 `match` 到对应代码:

| id | 首选词 | GB/T 13745 |
|---|---|---|
| `mathematics` | 数学 | 110 |
| `information-and-systems-science` | 信息科学与系统科学 | 120 |
| `computing` | 计算机科学技术 | 520 |
| `management` | 管理学 | 630 |
| `linguistics` | 语言学 | 740 |
| `journalism-and-communication` | 新闻学与传播学 | 860 |
| `library-and-information-science` | 图书馆、情报与文献学 | 870 |
| `education` | 教育学 | 880 |

顶层之下按[层级结构](hierarchy.md)规则 4 全部借入:`computing` 取 CS2023 的 17 个知识领域,其余七个取 GB/T 13745 的二级、三级学科。

### 邻近主题的处理

原先作为邻近主题降级处理的,其中数学、管理学、语言学已升为顶层。仍按降级处理的:

| 主题 | 落点 | 依据 |
|---|---|---|
| 硬件、体系结构 | `computing` › `architecture-and-organization` | CS2023 AR |
| 项目管理 | `software-engineering` 下 SWEBOK 第 9 章「软件工程管理」,同时在 `management` 之下;多层级 | SWEBOK v4;GB/T 13745 630 |
| 通用职业技能(写作、沟通、时间管理) | `computing` › `society-ethics-and-the-profession`;写作另可挂 `journalism-and-communication` 之下 | CS2023 SEP |
| 术语学(ISO 704、1087、30042) | `linguistics` 之下,具体二级学科待核 | GB/T 13745 740 |
| Web 开发 | `specialized-platform-development` › Web Platforms;MDN 只作映射 | CS2023 SPD |
| 结构化写作(DITA) | 待定 | — |

### 排除范围

以下主题不建节点,相关笔记不进本库:

| 主题 | 说明 |
|---|---|
| 自然语言学习 | 英语、日语等语言学习笔记 |
| 课程和书的阅读进度 | 属于个人任务管理,不是知识 |

非技术的生活领域(健康、理财、旅行)尚未决定,见待定事项。

### 用途

给本库的笔记打主题标签、做检索、生成导航。单人使用,中文为主,英文别名必备(文献是英文的)。不需要多语种对等,不需要印刷版式。

## 概念记录的字段

```yaml
- id: sql-injection                      # 稳定、小写、连字符;一旦引用不改
  label: { zh: SQL 注入, en: SQL injection }
  alt: [SQLi]                            # 非首选词;可检索、可显示
  hidden: []                             # 非首选词;可检索、不显示(拼写错误等)
  broader: [input-validation, data]      # 空列表 = 顶层概念
  arrays: [security-asvs]                # 所属数组;上位只有一个来源时可省略
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

数组在文件顶部单独登记,对应 ISO 25964-1 数据模型的 ThesaurusArray 与 NodeLabel。标识二选一或都有:`source`(按来源分组)或 `characteristic`(按划分特征分组,需在 `characteristics.yaml` 登记):

```yaml
arrays:
  - id: security-asvs
    superordinate: security             # 数组所属的上位概念
    source: asvs                        # 以来源为标识
  - id: pl-by-paradigm                  # 分析层的例子,目前没有
    superordinate: programming-languages
    characteristic: paradigm            # 以划分特征为标识,显示为节点标签 (按范式)
```

一个概念的下位只有一个来源、且未做分析时,不登记数组。规则见[层级结构](hierarchy.md)。

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
- 数组的 `source` 或 `characteristic` 至少一个;`characteristic` 在 `characteristics.yaml` 里;分析层数组的成员都在上位的下位集合内,且同一划分特征下每个下位至多属一组
- `source` 不是 `self` 的概念必有一条 `match` 指向同一来源
- `label.en` 和 `alt` 在全表内不重复(重复 = 可能是同一概念建了两次)
- 统计:每个第 2 层概念下 `unassigned` 的比例(盲区地图)、`candidate` 被引用次数

## 与其他设计的关系

| 事项 | 在哪 | 关系 |
|---|---|---|
| 树怎么分层、每层按什么分、从哪借入 | [层级结构](hierarchy.md) | 本文的 `broader`、`arrays`、`source` 字段按它的规则填 |
| 外部体系怎么登记、借入 / 映射 / 派生组三种用法、`match` 怎么写 | [来源名称规范表](sources-registry.md) | 本文的 `source`、`match.source` 只能写它登记的 id |
| 分面字段 | [草案](drafts/facet-field.md) | 未生效,本文不设该字段 |
| 手工概念组 | [草案](drafts/concept-groups.md) | 未生效;派生组已随映射自动存在 |
| 导航 | — | 把树渲染成目录就是导航;树不依赖界面 |
| 知识图谱 | [概念文](../concepts/knowledge-graph.md) | 现在边只有 `broader` / `related` 两种,节点是概念不是实体。以后加带类型的边时节点复用,不重建 |
| 软件产品、语言、组织 | [命名实体词表](entities.md) | 个体不进主题树;实体通过 `subjects` 挂到主题概念 |
| 文档类型、人名 | — | 各是独立词表,有内容后按需建 |

## 待定事项

- 排除范围:非技术的生活领域(健康、理财、旅行)是否排除
- 结构化写作(DITA)的落点;术语学在 740 语言学下的具体二级学科
- 分面字段,见 [草案](drafts/facet-field.md)
- 文件格式:YAML 单文件,还是每个第 2 层概念一个文件(概念过几百条时再考虑)
- `related` 的使用规则:什么情况下加、是否要求互反
