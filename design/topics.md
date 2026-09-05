# 主题词表设计

`vocab/topics.yaml` 是本库的正式主题叙词表，也是由 `scripts/build-topics.py` 确定生成的输出。它由概念记录、记录中的标签、概念之间的层级与相关关系，以及概念到外部词表的映射构成，用于给内容单元标引主题、检索和生成导航。知识图谱和导航是它的用法或升级方向，不是词表本身。

人工不直接编辑 `vocab/topics.yaml`。当前编辑源是生成脚本及其实际读取的 `vocab/build/` 输入；修改输出而不修改编辑源，会在下次生成时丢失。本文规定词表范围、记录、关系、映射、生命周期、建设流程和校验。树的结构见[层级结构](hierarchy.md)，外部来源登记见[来源名称规范表](sources-registry.md)。理论依据见[受控词表](../concepts/controlled-vocabulary.md)和[词表的建设与维护](../concepts/vocabulary-construction.md)。

正式词表当前保持 700 个概念、24 个数组和 8 个顶层。来源与术语的新接口已经实现，但尚未接管正式数据：语言依据采用本文的结构化合同，其他现行紧凑 `basis`、标量 `source` 和 `match.source` 继续由当前生成链消费；共享引用结构、术语三层记录、委托和生成消费者均未激活。通用 `origin` 不再是主题目标字段，本次同步不以其他字段自动填补它。

## 词表总览

主题词表按概念、标签、概念关系和外部映射四层表达信息。

```text
                          vocab/topics.yaml
 ┌──────────────────────────────────────────────────────────────────┐
 │                                                                  │
 │  概念记录                                                        │
 │     id:    sql-injection        ← 稳定引用，名称变化时不改        │
 │     label: SQL 注入 / SQL injection  ← 首选标签                  │
 │     alt:   SQLi                 ← 同一概念的替代标签              │
 │     scope: 用于……不用于……       ← 范围注释                       │
 │                                                                  │
 │  词法控制                                                        │
 │     SQLi  USE  SQL injection    ← 在同一概念记录内用 alt 表示    │
 │                                                                  │
 │  概念关系                                                        │
 │     层级  security                                               │
 │             └─ input-validation                                 │
 │                  └─ sql-injection      ← broader 字段            │
 │     相关  sql-injection ◀────▶ parameterized-query              │
 │                                      ← related 字段              │
 │                                                                  │
 │  外部映射                                                        │
 │     sql-injection ──exactMatch──▶ CWE-89                         │
 │     sql-injection ──broadMatch──▶ A03:2021                       │
 │                 现行 source 必须在 vocab/sources.yaml 中登记     │
 └──────────────────────────────────────────────────────────────────┘

 叙词表 ──渲染成目录──▶ 导航       概念和关系不变，只改变呈现
   │
   └──增加带类型的边──▶ 知识图谱   复用概念节点，增加关系类型
```

`label`、`alt` 和 `hidden` 都附着于同一概念记录；USE／UF 说明同一概念的等价入口，不建立两个概念。`broader` 和 `related` 连接概念。界面显示文字，不改变两类关系的主体。

主题标签的当前编辑权仍在主题生成输入。`concepts/glossary.md` 是全库 designation 与中英对照的现行登记；两处须使用已经登记的同一写法。候选术语三层模式和未来委托接口虽已实现，但正式 `vocab/terms.yaml`、委托、消费者和切换状态均不存在，不能把标签移到第二个正式编辑位置。

正式映射继续使用 `match: { source, id, rel }`。后置共享 `match` 已实现 `registry`、`item`、`rel` 和相邻 `basis`，但具体角色和逐条关系依据尚未批准，正式数据也未迁移。两种结构不得混写在同一现行示例中。

## 范围与用途

本节规定现有覆盖、邻近主题、排除项和使用目的；未获决定的生活主题边界继续保持待定。

### 覆盖范围

顶层概念由范围决定，不从其他体系复制。现有顶层取 GB/T 13745-2009 的 8 个一级学科，并分别 `match` 到来源代码。以下 id、中文 `label` 和代码保持不变。

| id | 中文 label | GB/T 13745 |
|---|---|---|
| `mathematics` | 数学 | 110 |
| `information-and-systems-science` | 信息科学与系统科学 | 120 |
| `computing` | 计算机科学技术 | 520 |
| `management` | 管理学 | 630 |
| `linguistics` | 语言学 | 740 |
| `journalism-and-communication` | 新闻学与传播学 | 860 |
| `library-and-information-science` | 图书馆、情报与文献学 | 870 |
| `education` | 教育学 | 880 |

顶层以下按[层级结构](hierarchy.md)的结构复制规则全部借入：`computing` 使用 CS2023 的 17 个 Knowledge Area，其余 7 个顶层使用 GB/T 13745 的二级和三级学科。本次同步不改变任何概念、数组、层级、标签、关系或状态。

### 邻近主题

原先作为邻近主题降级处理的内容中，数学、管理学和语言学已经升为顶层。其余内容保留以下落点和依据。

| 主题 | 落点 | 依据 |
|---|---|---|
| 硬件、体系结构 | `computing` › `architecture-and-organization` | CS2023 AR |
| 项目管理 | `software-engineering` 下 SWEBOK 第 9 章“软件工程管理”，同时在 `management` 以下；多层级 | SWEBOK v4；GB/T 13745 630 |
| 通用职业技能（写作、沟通、时间管理） | `computing` › `society-ethics-and-the-profession`；写作另可挂在 `journalism-and-communication` 以下 | CS2023 SEP |
| 术语学（ISO 704、1087、30042） | `linguistics` › 740.35 应用语言学以下，作为本地概念 | GB/T 13745 740.35 |
| Web 开发 | `specialized-platform-development` › Web Platforms；MDN 只作映射 | CS2023 SPD |
| 结构化写作（DITA） | `journalism-and-communication` 以下；DITA 标准作为实体，`subjects` 指向同一处 | GB/T 13745 860；技术写作属传播 |

### 排除范围

以下主题不建概念记录，相关内容不进入知识库。

| 主题 | 说明 |
|---|---|
| 自然语言学习 | 英语、日语等语言学习内容 |
| 课程和书的阅读进度 | 属于个人任务管理，不是知识 |

非技术的生活领域（健康、理财、旅行）尚未决定，见待定事项。

### 使用目的

主题词表用于给内容单元标引主题、检索和生成导航。它由一人使用，以中文为主，并为有依据的英文标签提供检索入口；不要求多语种对等或印刷版式。

## 生成路径

`vocab/topics.yaml` 保持单文件。第 2 层不用于拆分文件：多层级概念可以同时位于不同主题分支，文件边界不能与树结构一一对应。概念达到几千个后，再考虑按顶层拆分。

`scripts/build-topics.py` 的当前完整输入如下。

- `vocab/build/cs2023-kus.json`
- `vocab/build/cs2023-zh.json`
- `vocab/build/extra-arrays.json`
- `vocab/build/gbt-13745.json`
- `vocab/build/gbt_en.py`
- `vocab/build/label-decisions.json`
- `vocab/build/label-adoptions.json`
- `vocab/sources.yaml`（语言依据的来源登记校验）
- `vocab/build/scope-zh.json`
- `scripts/build-topics.py` 中的顶层、图书馆情报与文献学分支、多层级规则、版本和日期

`vocab/build/label-lookup.json` 是查询清单，`vocab/build/label-review.md` 是人工复核材料；生成器不读取两者。旧 Wikidata 决定保存在 `label-decisions.json`，本次结构化采纳保存在 `label-adoptions.json`；两者按各自合同进入生成链。后者不覆盖前者的否决记录。`__pycache__` 也不是编辑源。

`scripts/label_basis.py` 统一语言依据的兼容读取、校验与人读字段；`scripts/label_adoptions.py` 处理采纳记录。新增输入只参与标签采纳及依据校验，树结构仍由原有输入决定。

修改主题数据时，先修改生成脚本或上述实际输入，再重建正式输出并检查差异。应用只读取正式输出，不反向编辑它。

## 概念记录

概念记录使用以下现行结构；语言依据的内部形状按下文合同保存。

```yaml
- id: sql-injection                      # 稳定、小写、连字符；一经引用不改
  label: { zh: SQL 注入, en: SQL injection }
  basis:                                # 标签的形式依据
    zh: { level: 3, references: [{ source: wikidata, locator: Q506059 }] }
    en: { level: 2, references: [{ source: cwe, locator: CWE-89 }] }
  alt: [SQLi]                            # 替代标签；可检索、可显示
  hidden: []                             # 隐藏标签；可检索、不显示
  broader: [input-validation, data]      # 空列表表示顶层概念
  arrays: [security-asvs]                # 所属数组；上位只有一个来源时可省略
  related: []                            # 必须互反；仅在不同上位且内容常同时涉及两概念时添加
  scope: >                               # 范围注释：用于……不用于……
    指通过拼接用户输入改变 SQL 语义的攻击及对应缺陷；
    参数化查询等防御手段不在此。
  # 本地建立且没有实际派生来源时不填 source
  match:                                 # 现行外部概念映射
    - { source: cwe, id: CWE-89, rel: exactMatch }
    - { source: owasp-top10, id: "A03:2021", rel: broadMatch }
  status: active                         # 概念记录的生命周期状态
  added: 2026-08-20
  history: []                            # 日期、变更内容和理由
```

必填字段是 `id`、`label.zh`、`broader`、`status`、`added`、`basis.zh` 和 `basis.en`。`label.en` 按[治理](governance.md)中的译名阶梯取得；完成当前判断仍未采用时不填，并写 `basis.en: { level: 6, reason: 未采用原因 }`；未重新分级的旧 `none` 保留为 `legacy: none`。其余字段按需使用。本地概念强烈建议填写 `scope`，以明确适用和不适用的边界。

`basis` 中的语言项记录标签的准入根据。外部依据、第 5 级模型判断、第 6 级未采用和未重新分级的历史值分别保存，见下文“语言依据”。语言依据不能代替概念对应判断，也不能代替其他字段值或关系的断言依据。人工赋值的具体断言按[维护](maintenance.md)的断言规则记录依据。

语言项使用结构化 `basis.zh`／`basis.en`；其他断言仍使用现行紧凑 `basis`，派生与映射仍使用标量 `source` 和 `match.source`。复制记录的现行 `source` 填写真实来源，并用 `match` 指回相应外部条目；本地建立、综合判断或只受材料支持的记录没有实际派生来源时不填 `source`。正式库存中的 `source: self` 只是待迁移兼容值，不作为实际派生解释，也不得用于新增记录。后置共享 `basis`、`source` 和 `match` 只有在正式迁移、角色批准和消费者切换后才接管相应记录。

当前 `scripts/build-topics.py` 要求每条记录都提供 `source`，并总是输出该字段，尚不能表达本地记录省略 `source`。这是现行生成路径的待迁移缺口；缺口关闭前，不能用 `source: self` 绕过，也不能通过这条路径把没有实际派生来源的新建本地记录写入正式输出。

通用 `origin` 不是目标字段。旧 `origin` 的库存和逐项去向保存在来源迁移账本中；删除旧设计定义不批准任何新的 `basis`、`source` 或 `match`，也不把发现观察、具体值依据、实际派生和概念映射合并。

字段与标准的现行对应关系保持不变：`alt`／`hidden` 对应 SKOS `altLabel`／`hiddenLabel`；`broader`、`related` 对应 SKOS 同名属性；`arrays` 对应 ISO 25964-1 数据模型的 ThesaurusArray；`scope` 对应范围注释；`history` 对应历史注释；`status` 对应数据模型的 `status`；`match` 保存跨词表概念映射。

数组在文件顶部单独登记，对应 ISO 25964-1 数据模型的 ThesaurusArray 与 NodeLabel。数组至少使用 `source` 或 `characteristic` 之一作为标识；`characteristic` 还须在 `characteristics.yaml` 登记。

```yaml
arrays:
  - id: security-asvs
    superordinate: security             # 数组所属的上位概念
    source: asvs                        # 以来源为标识
  - id: pl-by-paradigm                  # 分析层示例，当前没有
    superordinate: programming-languages
    characteristic: paradigm            # 以划分特征为标识，显示为节点标签（按范式）
```

一个概念的下位只有一个来源且未做分析时，不登记数组。规则见[层级结构](hierarchy.md)。分面字段暂不设置，见[分面字段草案](drafts/facet-field.md)；草案仍未生效。

## 语言依据

[语言依据结构](decisions/structured-label-basis.md)规定 `basis.zh`／`basis.en` 的现行合同，替代旧字符串模型标记。语言依据与来源 v2 的共享引用是两个合同；本次不改变其他 `basis` 项、`source` 或 `match`。

| 依据性质 | 结构 | 条件 |
|---|---|---|
| 外部依据 | `{level: 1..4, references: [{source, locator}]}` | 标签非空；每个来源命中现行 `sources.yaml`，定位非空；第 4 级至少有两个不同来源 |
| 模型知识 | `{level: 5, model: {name, date, rationale, approval}}` | 标签非空，模型、日期、逐条判断及实际采纳授权齐备；外部用法未核实 |
| 明确未采用 | `{level: 6, reason}` | 对应语言标签为空，原因非空；原名在另一语言保留 |
| 历史依据 | `{legacy: 旧值}` | 保存未重新分级的 `none`、`self` 或旧外部引用，不推定新等级 |

等级的译名含义见[治理](governance.md#译名)。来源原名可以继续沿用；本批按已登记类别将既有来源依据明确归级，并保留其来源和原定位：`gbt-13745`、`lom`、`rfc-1122` 为第 1 级，`wikidata` 为第 3 级，`cs2023`、`asvs`、`cwe`、`attack`、`atlas`、`swebok`、`owasp-llm-top10` 为第 2 级。这是既有记录的结构迁移，不表示新做了外部核验，也不能将网站整体类别作为新增译名的准入证明。未知历史引用保持未分级。旧 `source` 按记录原来源及已有映射定位展开；已映射来源缺少定位时由校验报错，不编造定位；映射表外的旧引用保持历史值。

旧字符串仍可读取，新生成的语言依据使用上述结构。历史 `none` 只说明当时没有采用，不证明前四级已查尽，也不自动变为第 6 级。旧 `self` 不自动变为模型知识，其不得为 `active` 的规则继续适用。第 5 级既不使概念转正，也不要求概念退出 `active`。

外部 `references` 只保存已登记来源；多个不同来源 ID 只能由校验器证明引用不同，不能证明真实独立性、用法一致或概念对应。第 4 级仍须按治理规则作实质判断。模型标识不是来源 ID，不创建同名实体或来源用途，也不用于派生、映射、关系或其他断言。

### 模型标记

第 5 级使用完整的 `model` 对象，保留模型、日期、判断与授权，不再写单独的 `basis.zh: model` 字符串。这个历史章节锚点继续保留；当前依据形状以上表为准，模型信息不作为来源实体或来源用途。

### 采纳记录

结构化采纳独立保存在 `vocab/build/label-adoptions.json` 的 `records` 下，键为 `topics/<id>/<语言>` 或 `forms/<id>/<语言>`。每条记录保存 `accept`、准确的 `label`、完整 `basis`，以及 `original: {en, scope}`。本批模型记录的 `approval` 固定指向 `design/decisions/structured-label-basis.md#批次授权`；`date` 使用真实的 `YYYY-MM-DD` 日期，`name` 使用实际可得模型标识，`rationale` 说明所选表达与原概念的对应。模型输出不能给自己授权。

主题生成器先完成原有生成，再应用采纳并标准化语言依据；载体按现行人工编辑路径应用同一合同。加载器只接受已明确支持的本批授权，并校验输入声明与每条模型授权一致，不能凭一个形似决定文件的路径取得权限。已存在标签只允许名称和依据均相同的幂等应用，不能借同名译法覆盖外部依据。已采纳模型输出必须与对应输入中的标签和依据一致，原英文与范围也必须仍与快照相符；缺失、未采纳或过期记录阻断生成及校验。旧 Wikidata 的 Q 号、采纳和否决仍保存在 `label-decisions.json`，不被新记录覆盖。旧报告中的建议与辅助材料保留作复核上下文，不冒充已登记的多来源依据。

该文件保存已授权形式的生成采纳，不替代 `concepts/glossary.md` 的现行中英对照编辑权。输出中的模型判断自包含，离线表示不依赖私人报告；完整原名及范围快照由采纳输入承担。以后获得并采纳外部依据时，保留原模型判断与采纳历史，再更新当前依据。

### 人读表示

HTML 在名称旁直接显示“模型知识 · 第 5 级”，并注明“外部用法未核实”；详情保留模型、日期、判断与授权。Obsidian 把语言依据作为可读正文，显示等级、外部来源和定位，或模型声明及记录字段，不写嵌套 frontmatter。历史值明确显示未重新分级，不能冒充第 6 级结论。

关系图只从外部 `references` 建立来源关联，模型和历史标记不生成外部证据连线。不能解析新结构的使用方不得静默丢弃依据后继续发布。名称覆盖、外部依据覆盖和模型采纳分别统计；表示支持不等于正式消费者激活，也不证明既有 vault 已更新。

## 生命周期

`status` 只表示现行概念记录状态，不给单个字符串或标签建立独立生命周期。

| status | 来源 | 含义 | 进入 | 离开 |
|---|---|---|---|---|
| `unassigned` | Z39.19 §11.1.8 | 为补全层级而收入、尚未用于内容标引的概念记录 | 复制知识体系层级时 | 达到既有阈值后转为 `active` |
| `candidate` | Z39.19 §11.1.6 | 已完成概念判断和初步依据核验、尚未完成接受程序的概念记录 | 需要建立本地概念时 | 达到既有阈值且通过审核后转为 `active`；长期无引用时可以取得删除资格 |
| `active` | — | 在用的概念记录 | 审核通过 | 被替代后转为 `deprecated` |
| `deprecated` | Z39.19 §11.3.2.1 | 不再用于新标引、为检索和历史保留的概念记录 | 合并、拆分或替代时 | 不删；必须有 `replaced_by` 和 `history` |

`deprecated` 概念记录保留，必要的旧表示形式随记录保留，以维持既有检索、替代关系和历史追踪。只有满足既定门禁的 `candidate` 概念记录可以取得删除资格；资格不等于批准，实际删除仍按治理权限执行。`unassigned`、`active`、`deprecated` 和单个表示形式都不继承该资格。

复制的概念可以长期保持 `unassigned`，因为它们用于显示盲区。确认不需要时在 `scope` 中说明有意不覆盖及理由，仍保留记录。

候选术语接口另有三种工作流状态和四种管理状态，但尚未激活。它们不接管主题 `status`，不把主题 `candidate` 变成术语候选，也不把 `unassigned`、迁移账本中的 `defer` 或任何报告命中机械映射为术语状态。

## 建设流程

1. 写明“范围与用途”的排除项。
2. 逐个核对各数组来源的当前版本和条目，并登记到 `sources.yaml`。
3. 按[层级结构](hierarchy.md)的来源表复制第 3 层，记录全部使用 `unassigned`，填写现行 `source`，并用现行 `match` 指回来源条目。
4. 把现有约 90 个概念挂到树上：来源已有的第 3 层概念并入复制结构；本地概念先建立 `candidate` 记录，没有实际派生来源时不填 `source`。当前生成器不能省略该字段，因此在缺口关闭前不得用 `source: self` 新增这类记录。
5. 自下而上校正时，从现有内容、书签和文献识别带来源上下文的字符串或名词短语，先与已登记的 `label`、`alt` 和 `hidden` 匹配。匹配后按概念 id 与树比较；未解析项只交人工判断，不自动建立概念或关系。
6. 分批补充 `scope` 和 `match`，逐个第 2 层概念处理，不要求一次完成。

第 3 步由当前生成链产生确定输出，结果须经人工审核。来源迁移账本和反向索引可以定位旧引用，后置严格校验可以检查新结构；这些能力均不批准实际派生或映射，也不能在正式迁移前改写当前数据。

`scripts/check-terms.py` 的正文诊断已经实现。它从 Git 取得动态 Markdown 清单，检查标题、加粗内容和中文引号，排除代码围栏、行内代码、链接目标和路径；默认与现行 `concepts/glossary.md`、`vocab/topics.yaml`、`vocab/entities.yaml` 和 `vocab/types.yaml` 中的已登记写法比较。输出保留精确位置和上下文，模式为 `report-only`。命中只供人工判断，不形成 designation、概念、关系、违规、阻断或候选记录。

## 校验规则

每次修改主题生成脚本或实际输入并重建 `vocab/topics.yaml` 后，运行 `scripts/check-topics.py`。现行校验继续检查以下规则。

- 所有 `broader` 指向存在的 id，且不存在环。
- 现行 `source`、`match.source` 和语言依据的外部 `references[].source` 在 `sources.yaml` 中。
- 主题与载体的语言依据满足等级、标签、来源定位及模型授权条件；模型输出与采纳记录、原英文和范围一致。历史 `none` 不误判为第 6 级，旧 `self` 仍不能支持 `active`。
- `deprecated` 必有 `replaced_by`。
- `arrays` 指向存在的数组，且数组的 `superordinate` 位于本概念的 `broader` 中。
- 数组至少有 `source` 或 `characteristic`；`characteristic` 在 `characteristics.yaml` 中。分析层数组的成员位于上位概念的下位集合内，同一划分特征下每个下位概念至多属于一组。
- `source` 不是 `self` 的概念记录有一条 `match` 指向同一来源。
- `label.en` 和 `alt` 在全表内不重复；重复可能表示同一概念被建立两次。
- 统计每个第 2 层概念下 `unassigned` 的比例，以及 `candidate` 概念记录的引用次数。

现行 `check-topics.py` 不消费通用 `origin`，也不读取迁移账本。共享引用校验只检查已经进入后置严格形状的数据；正式主题数据尚未切换，因此它不替代当前校验链。候选识别报告与主题结构校验分开，报告数量非零不构成主题错误。

## 设计分工

| 事项 | 文档 | 关系 |
|---|---|---|
| 树的分层、划分和复制来源 | [层级结构](hierarchy.md) | 本文的 `broader`、`arrays`、现行 `source` 按其规则填写 |
| 外部体系登记、复制、映射和派生组 | [来源名称规范表](sources-registry.md) | 现行兼容层与后置共享接口的唯一职责说明；本文不自行批准角色或关系 |
| 主题标签 | 本文与生成输入 | `label`、`alt`、`hidden` 继续附着于现行主题概念；写法须已在现行 glossary 登记 |
| designation 登记 | [治理](governance.md)与 `concepts/glossary.md` | glossary 仍是现行登记和中英对照的编辑源；正文诊断只供人工判断 |
| 术语基础 | [术语治理草案](drafts/terminology-governance.md) | 三层模式、状态、生成、诊断和维护接口已实现；草案、正式数据、委托和消费者未激活 |
| 分面字段 | [分面字段草案](drafts/facet-field.md) | 草案未生效；本文不设置该字段 |
| 手工概念组 | [概念组草案](drafts/concept-groups.md) | 草案未生效；派生组可以从映射计算 |
| 导航 | — | 渲染主题树得到导航，树不依赖界面 |
| 知识图谱 | [概念文](../concepts/knowledge-graph.md) | 当前概念关系只有 `broader` 和 `related`；增加带类型的关系时复用概念节点 |
| 软件产品、语言、组织 | [命名实体词表](entities.md) | 个体不进入主题树，通过 `subjects` 挂到主题概念 |
| 文档类型、人名 | [内容模型](content-model.md)与[命名实体词表](entities.md) | 文档类型使用独立词表；人名属于命名实体词表 |

## 待定事项

- 生活领域（健康、理财、旅行等）要记，按范围声明加顶层：健康对应 GB/T 13745 医学门类（310―360），理财对应 790 经济学；具体哪些顶层待列。
- 分面字段，见[草案](drafts/facet-field.md)。
- 大语言模型作为本地概念挂在 `artificial-intelligence` 的哪个知识单元下（NLP 或 ML）。
- 术语正式编辑源、主题标签委托、消费者和切换状态何时激活；当前不得建立相应正式数据。
- 来源共享引用何时正式迁移，以及每条实际派生和映射怎样取得批准；旧 `origin` 去向不能替代这些判断。
