# 主题词表

`data/vocab/topics.yaml` 是本库的正式主题叙词表，也是由 `uv run kb-core build-topics` 确定生成的输出。它由概念记录、记录中的标签、概念之间的层级与相关关系，以及概念到外部词表的映射构成，用于给内容单元标引主题、检索和生成导航。知识图谱和导航是它的用法或升级方向，不是词表本身。

人工不直接编辑 `data/vocab/topics.yaml`。当前编辑源是生成脚本及其实际读取的 `data/inputs/topics/` 输入；修改输出而不修改编辑源，会在下次生成时丢失。本文规定词表范围、记录、关系、映射、生命周期、建设流程和校验。树的结构见[层级结构](hierarchy.md)，外部来源登记见[来源名称规范表](sources-registry.md)。理论依据见[受控词表](../../concepts/controlled-vocabulary.md)和[词表的建设与维护](../../concepts/vocabulary-construction.md)。

正式词表尚未完成来源 v2 迁移。下文按已采纳的[来源字段合同](../../decisions/source-v2-field-contract.md)说明目标记录和严格生成要求；工具只输出并校验新格式，缺少逐字段采纳输入时失败，不退回旧 source 或 match。主题身份、结构、语言采纳和术语未激活边界保持不变。

## 词表总览

主题词表按概念、标签、概念关系和外部映射四层表达信息。

```text
                          data/vocab/topics.yaml
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
 │                 registry 必须在 data/vocab/sources.yaml 中登记     │
 └──────────────────────────────────────────────────────────────────┘

 叙词表 ──渲染成目录──▶ 导航       概念和关系不变，只改变呈现
   │
   └──增加带类型的边──▶ 知识图谱   复用概念节点，增加关系类型
```

`label`、`alt` 和 `hidden` 都附着于同一概念记录；USE／UF 说明同一概念的等价入口，不建立两个概念。`broader` 和 `related` 连接概念。界面显示文字，不改变两类关系的主体。

主题标签的当前编辑权仍在主题生成输入。`docs/glossary.md` 是全库 designation 与中英对照的现行登记；两处须使用已经登记的同一写法。候选术语三层模式和未来委托接口虽已实现，但正式 `data/vocab/terms.yaml`、委托、消费者和切换状态均不存在，不能把标签移到第二个正式编辑位置。

映射使用 registry、item、rel 和相邻 basis；角色批准与逐条关系依据分别满足条件。旧数据仍可作为迁移输入的审计来源，不能作为严格读取的兼容格式。

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

`data/vocab/topics.yaml` 保持单文件。第 2 层不用于拆分文件：多层级概念可以同时位于不同主题分支，文件边界不能与树结构一一对应。概念达到几千个后，再考虑按顶层拆分。

`uv run kb-core build-topics` 的当前完整输入如下。

- `data/inputs/topics/cs2023-kus.json`
- `data/inputs/topics/cs2023-zh.json`
- `data/inputs/topics/extra-arrays.json`
- `data/inputs/topics/gbt-13745.json`
- `packages/kb-core/src/kb_core/gbt_en.py`
- `data/inputs/topics/label-decisions.json`
- `data/inputs/topics/label-adoptions.json`
- `data/vocab/sources.yaml`（语言依据的来源登记校验）
- `data/inputs/topics/source-references-v2.json`（逐字段来源引用采纳；也可由 `--references` 显式指定）
- `data/inputs/topics/scope-zh.json`
- `packages/kb-core/src/kb_core/build_topics.py` 中的顶层、图书馆情报与文献学分支、多层级规则、版本和日期

`data/audit/labels/label-lookup.json` 是查询清单，`data/audit/labels/label-review.md` 是人工复核材料；生成器不读取两者。旧 Wikidata 决定保存在 `label-decisions.json`，本次结构化采纳保存在 `label-adoptions.json`；两者按各自合同进入生成链。后者不覆盖前者的否决记录。`__pycache__` 也不是编辑源。

核心包中的 `label_basis` 模块统一语言依据的标准化、校验与人读字段，`label_adoptions` 模块处理采纳记录。新增输入只参与标签采纳及依据校验，树结构仍由原有输入决定。

来源引用输入记录准确旧值、目标新值和对应采纳决定；缺失输入或未覆盖的引用阻断生成，不能原样输出旧字段。`--output` 可以将候选写到 build 下或外部临时目录；不把临时生成当作正式切换。修改主题数据时先改生成脚本或实际输入，再重建并检查差异；应用只读取输出，不反向编辑。

## 概念记录

概念记录必填 id、label.zh、broader、status、added、basis.zh 和 basis.en。label、alt、hidden 附着于同一稳定概念；broader 和 related 连接概念，arrays 指向数组，scope 说明适用范围，history 保留真实变更。label.en 按[译名规则](../governance/governance.md)取得；未采用时按语言依据记录原因，不造新名称。

| 字段 | 合同 |
|---|---|
| basis.zh／en | 独立语言依据结构；外部等级、模型判断、未采用和历史值分开 |
| source | registry、item、locator、basis；只表达实际派生，要求获准 structure 角色 |
| match | registry、item、rel、basis 列表；每条关系要求获准 mapping 角色及相邻依据 |
| assertions.source | disposition: project_assertion、original: self、migration；保留原本地建立判断，不形成外部派生 |
| status | 项目概念状态，不表示来源外部状态或单个标签状态 |

[来源数据批次](../../decisions/source-data-batch.md)允许来源 source_status 省略，含义为外部状态未核实；来源 version 必有但可为 null，含义为未登记可核实版本。这两项不影响主题 status，也不自动批准派生或映射。实际引用仍须逐条材料、定位、真实核对日期、角色资格与精确采纳；无版本 de-facto 不能取得 structure，依赖外部现行状态的操作在缺状态时继续阻断。

source 与 assertions.source 互斥。本地建立且没有实际派生时不填 source；旧 self 仅在明确迁移审计定位下转入项目判断，不作为新增记录的外部依据。语言依据不能代替概念对应、派生或映射证明；人工赋值断言仍按[维护](../governance/maintenance.md)处理。

通用 origin 不是目标字段；旧库存按原基线审计，不自动变成 basis、source 或 match。alt／hidden、broader、related 与 scope 的既有标准对应不变，来源字段结构变更不改变概念或层级。

数组在文件顶部单独登记，保留 id 与 superordinate。外部数组使用 external_group，结构为 registry、item、locator、basis，要求获准 structure 角色；这只证明分组本身，成员的实际派生另以 source 核对。已批准的分析数组可以使用已登记 characteristic，不能通过迁移新建划分特征。

载体数组按 Q16 使用 local_analysis 保存 legacy_source_label、state: isolated、decision，保留原父项与成员，不改为外部来源引用。该对象与 assertions.source 的原 self 判断不同；两者都不产生外部证据边。具体规则见[来源用途登记](sources-registry.md#本地结构)。

一个概念的下位只有一个来源且未做分析时，不登记数组。层级规则见[层级结构](hierarchy.md)；[分面字段草案](../../drafts/facet-field.md)未生效。

## 语言依据

[语言依据结构](../../decisions/structured-label-basis.md)规定 `basis.zh`／`basis.en` 的现行合同，替代旧字符串模型标记。语言依据与来源 v2 的共享引用是两个合同；来源迁移不改变既有语言等级、模型授权或采纳记录。

| 依据性质 | 结构 | 条件 |
|---|---|---|
| 外部依据 | `{level: 1..4, references: [{source, locator}]}` | 标签非空；每个来源命中现行 `sources.yaml`，定位非空；第 4 级至少有两个不同来源 |
| 模型知识 | `{level: 5, model: {name, date, rationale, approval}}` | 标签非空，模型、日期、逐条判断及实际采纳授权齐备；外部用法未核实 |
| 明确未采用 | `{level: 6, reason}` | 对应语言标签为空，原因非空；原名在另一语言保留 |
| 历史依据 | `{legacy: 旧值}` | 保存未重新分级的 `none`、`self` 或旧外部引用，不推定新等级 |

等级的译名含义见[治理](../governance/governance.md#译名)。来源原名可以继续沿用；本批按已登记类别将既有来源依据明确归级，并保留其来源和原定位：`gbt-13745`、`lom`、`rfc-1122` 为第 1 级，`wikidata` 为第 3 级，`cs2023`、`asvs`、`cwe`、`attack`、`atlas`、`swebok`、`owasp-llm-top10` 为第 2 级。这是既有记录的结构迁移，不表示新做了外部核验，也不能将网站整体类别作为新增译名的准入证明。未知历史引用保持未分级。旧 `source` 按记录原来源及已有映射定位展开；已映射来源缺少定位时由校验报错，不编造定位；映射表外的旧引用保持历史值。

生成输入中的旧语言值按已采纳规则标准化，新格式输出使用上述结构；正式严格输出不保留裸字符串语言依据。历史 `none` 只说明当时没有采用，不证明前四级已查尽，也不自动变为第 6 级。旧 `self` 不自动变为模型知识，其不得为 `active` 的规则继续适用。第 5 级既不使概念转正，也不要求概念退出 `active`。

外部 `references` 只保存已登记来源；多个不同来源 ID 只能由校验器证明引用不同，不能证明真实独立性、用法一致或概念对应。第 4 级仍须按治理规则作实质判断。模型标识不是来源 ID，不创建同名实体或来源用途，也不用于派生、映射、关系或其他断言。

### 模型标记

第 5 级使用完整的 `model` 对象，保留模型、日期、判断与授权，不再写单独的 `basis.zh: model` 字符串。这个历史章节锚点继续保留；当前依据形状以上表为准，模型信息不作为来源实体或来源用途。

### 采纳记录

结构化采纳独立保存在 `data/inputs/topics/label-adoptions.json` 的 `records` 下，键为 `topics/<id>/<语言>` 或 `forms/<id>/<语言>`。每条记录保存 `accept`、准确的 `label`、完整 `basis`，以及 `original: {en, scope}`。本批模型记录的 `approval` 固定指向 `docs/decisions/structured-label-basis.md#批次授权`；`date` 使用真实的 `YYYY-MM-DD` 日期，`name` 使用实际可得模型标识，`rationale` 说明所选表达与原概念的对应。模型输出不能给自己授权。

主题生成器先完成原有生成，再应用采纳并标准化语言依据；载体按现行人工编辑路径应用同一合同。加载器只接受已明确支持的本批授权，并校验输入声明与每条模型授权一致，不能凭一个形似决定文件的路径取得权限。已存在标签只允许名称和依据均相同的幂等应用，不能借同名译法覆盖外部依据。已采纳模型输出必须与对应输入中的标签和依据一致，原英文与范围也必须仍与快照相符；缺失、未采纳或过期记录阻断生成及校验。旧 Wikidata 的 Q 号、采纳和否决仍保存在 `label-decisions.json`，不被新记录覆盖。旧报告中的建议与辅助材料保留作复核上下文，不冒充已登记的多来源依据。

该文件保存已授权形式的生成采纳，不替代 `docs/glossary.md` 的现行中英对照编辑权。输出中的模型判断自包含，离线表示不依赖私人报告；完整原名及范围快照由采纳输入承担。以后获得并采纳外部依据时，保留原模型判断与采纳历史，再更新当前依据。

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
3. 按[层级结构](hierarchy.md)的来源表复制第 3 层，记录全部使用 `unassigned`，填写严格 `source`，并用具有独立依据的 `match` 指回来源条目。
4. 把现有约 90 个概念挂到树上：来源已有的第 3 层概念并入复制结构；本地概念先建立 `candidate` 记录，没有实际派生来源时不填 `source`。生成器按已采纳引用输入表示本地建立事实，不以 `source: self` 回退。
5. 自下而上校正时，从现有内容、书签和文献识别带来源上下文的字符串或名词短语，先与已登记的 `label`、`alt` 和 `hidden` 匹配。匹配后按概念 id 与树比较；未解析项只交人工判断，不自动建立概念或关系。
6. 分批补充 `scope` 和 `match`，逐个第 2 层概念处理，不要求一次完成。

第 3 步由当前生成链产生确定输出，结果须经人工审核。来源迁移账本定位旧引用，严格校验检查新结构，反向索引定位正式引用；这些能力均不批准实际派生或映射，也不能在正式迁移前改写当前数据。

`uv run kb-core check-terms` 的正文诊断已经实现。它从 Git 取得动态 Markdown 清单，检查标题、加粗内容和中文引号，排除代码围栏、行内代码、链接目标和路径；默认与现行 `docs/glossary.md`、`data/vocab/topics.yaml`、`data/vocab/entities.yaml` 和 `data/vocab/types.yaml` 中的已登记写法比较。输出保留精确位置和上下文，模式为 `report-only`。命中只供人工判断，不形成 designation、概念、关系、违规、阻断或候选记录。

## 校验规则

修改生成器或实际输入后，用 `uv run kb-core build-topics` 生成，再由 `uv run kb-core check-topics` 校验。缺少来源逐字段采纳材料时应保留失败，不改正式输出消除错误。

- broader 指向现有 id 且无环；related 的既有对称与范围规则保持。
- source、match、external_group 使用严格形状与获准用途；角色决定须对应实际对象和作用范围，旧字段或畸形值不能被跳过。
- 实际派生的概念记录须有一条 match 指回同一来源；派生依据与映射依据仍独立，本地判断不伪装成派生。
- 语言依据满足等级、定位与模型授权合同；历史 none 不冒充第 6 级，legacy: self 不得支持 active。
- deprecated 保留 replaced_by；身份、关系与历史不得因序列化改变。
- arrays 指向存在的数组，superordinate 与概念 broader 对应；外部分组、本地判断和 Q16 本地分析分别检查，不临时创造 characteristic。
- label.en 和 alt 的现有全表唯一性规则保留；统计每个第 2 层概念下 unassigned 比例，候选引用计数依赖正式消费者的可审计输入。
- 分析数组的成员位于上位下位集合内，同一已登记 characteristic 下每个下位概念至多属于一组；自定断言指标不因字段形状变化取消。

正式数据未迁移时，严格命令失败说明尚有迁移缺口，不意味着允许恢复旧格式。候选识别仍为 report-only，不形成新概念或关系。

## 设计分工

| 事项 | 文档 | 关系 |
|---|---|---|
| 树的分层、划分和复制来源 | [层级结构](hierarchy.md) | 本文的 `broader`、`arrays`、现行 `source` 按其规则填写 |
| 外部体系登记、复制、映射和派生组 | [来源名称规范表](sources-registry.md) | 用途资格与严格共享引用的职责说明；本文不自行批准角色或关系 |
| 主题标签 | 本文与生成输入 | `label`、`alt`、`hidden` 继续附着于现行主题概念；写法须已在现行 glossary 登记 |
| designation 登记 | [治理](../governance/governance.md)与 `docs/glossary.md` | glossary 仍是现行登记和中英对照的编辑源；正文诊断只供人工判断 |
| 术语基础 | [术语治理草案](../../drafts/terminology-governance.md) | 三层模式、状态、生成、诊断和维护接口已实现；草案、正式数据、委托和消费者未激活 |
| 分面字段 | [分面字段草案](../../drafts/facet-field.md) | 草案未生效；本文不设置该字段 |
| 手工概念组 | [概念组草案](../../drafts/concept-groups.md) | 草案未生效；派生组可以从映射计算 |
| 导航 | — | 渲染主题树得到导航，树不依赖界面 |
| 知识图谱 | [概念文](../../concepts/knowledge-graph.md) | 当前概念关系只有 `broader` 和 `related`；增加带类型的关系时复用概念节点 |
| 软件产品、语言、组织 | [命名实体词表](entities.md) | 个体不进入主题树，通过 `subjects` 挂到主题概念 |
| 文档类型、人名 | [内容模型](content-model.md)与[命名实体词表](entities.md) | 文档类型使用独立词表；人名属于命名实体词表 |

## 待定事项

- 生活领域（健康、理财、旅行等）要记，按范围声明加顶层：健康对应 GB/T 13745 医学门类（310―360），理财对应 790 经济学；具体哪些顶层待列。
- 分面字段，见[草案](../../drafts/facet-field.md)。
- 大语言模型作为本地概念挂在 `artificial-intelligence` 的哪个知识单元下（NLP 或 ML）。
- 术语正式编辑源、主题标签委托、消费者和切换状态何时激活；当前不得建立相应正式数据。
- 来源共享引用何时正式迁移，以及每条实际派生和映射怎样取得批准；旧 `origin` 去向不能替代这些判断。
