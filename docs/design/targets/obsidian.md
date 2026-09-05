# Obsidian 映射

本文规定 Obsidian 作为 `kb-design` 首个完整落地应用层的 `Application Profile`。现行词表参考导出的 artifact contract 是上游物化子系统，`apps/obsidian/` 中的 `kb-obsidian` 工具从干净的设计提交消费其结果并建立完整 vault。本文按[内容模型](../model/content-model.md)引用应用无关语义，再规定 Obsidian 的功能范围、对象职责、field binding、使用方式与具体表示；artifact contract 只负责把已经选定的正式词表表示物化为文件。分层依据见 [Application Profile](../../concepts/application-profile.md)、[Reproducible Builds](../../concepts/reproducible-builds.md)、[方法登记](../governance/principles.md)、[设计与应用分离](../../decisions/form-independence.md)和[应用约束与表示分层](../../decisions/application-profile-boundary.md)。

## 当前状态

完整应用设计和实现已经建立：参考导出器生成六份正式词表的单向表示；`kb-obsidian` 从干净设计快照初始化完整 vault，建立 UUIDv4 `draft` 内容，校验内容字段与引用，并生成派生报告。语言依据按[语言依据结构](../../decisions/structured-label-basis.md)显示等级和真实依据性质。

工具按[工具归属](../../decisions/obsidian-tool-location.md)和[仓库布局](../../decisions/monorepo-layout.md)同仓维护，默认读取所在仓库，也接受显式 `--design-root`；manifest 记录实际提交与输入哈希，不使用提交白名单。命令默认输出仍为 `output/obsidian/`，正式知识库为仓库外的 `~/Documents/kb-vault/`，操作正式库时必须显式指定。

2026-09-05 的只读核查确认正式库已有《了解 Obsidian》一条 draft 内容，标题与正文搜索、Base 查询和内容校验通过。该观察替代“没有实际用户内容”的旧实例状态，不表示正式消费者、来源或术语切换已激活，也不证明正文外部事实或完整界面验收。

按[终端访问](../../decisions/obsidian-agent-entry.md)，新库生成受管理的根 `AGENTS.md`。现有正式库未安装该入口；本次只提供差异，不更新其规则、清单或用户内容。当前没有可审计查询日志和自动回流接口。

## 功能范围

完整应用负责以下工作：

- 捕获尚未判断去向的想法、链接、摘录和文件；
- 保存网页、书籍、论文、标准和原始文件等外部资料；
- 建立、写作、修改、废弃和引用内容单元；
- 通过受控字段引用正式主题、实体、来源用途、文档类型、体裁和载体；
- 建立不改变正式结构的用户索引和阅读路径；
- 通过 Base、Search、内部链接和 Obsidian 导航能力浏览内容与正式表示；
- 显示正式知识结构中的空分支与未覆盖项，并报告实际写作和检索中的分类困难、未解析字符串与过度集中；
- 形成只读统计、诊断和带上下文的维护线索，再交人工复核。

本设计明确排除任务与日程管理、既有 vault 迁移、可审计查询日志、自动回流、社区插件硬依赖、非空 vault 的自动更新和正式激活。它也不从正文、tag、alias、文件名、Backlinks、Graph、索引成员或语言模型输出自动建立概念、designation、关系、状态或正式引用。

## 模型边界

本 target 引用[内容模型](../model/content-model.md)的内容单元、字段语义、受控值、identifier 和生命周期，引用[主题词表设计](../model/topics.md)、[命名实体词表设计](../model/entities.md)、[来源名称规范表](../model/sources-registry.md)和[层级结构](../model/hierarchy.md)的正式对象、关系、多上位与数组规则，并按[维护](../governance/maintenance.md)保留指标、阈值、动作和决策权边界。

`Application Profile` 只为既定对象选择 Obsidian location、type、reference form 和允许的 loss。field／property／path binding 是同一应用内部的表示规则，不是 `metadata crosswalk`；它不改变词表层 `crosswalk` 的现行含义，也不得修改应用无关字段的语义、基数、值域、稳定身份或对象关系。

Obsidian 不能直接表达的约束由校验器保留，不能用自由 tag、文件夹、标题或普通链接替代。不能平坦放入 property 的正式结构进入正文表示，但正文不成为正式编辑源。

## 权属分层

一个 vault 同时保存三种权属和一类应用配置。

| 层 | 内容 | 修改者 | 项目效力 |
|---|---|---|---|
| 用户文件 | `home.md`、`inbox/`、`sources/`、`content/`、`indexes/`、`attachments/` | 使用者和经授权的内容工具 | 对该知识库中的实际内容有效，不直接修改 `kb-design` |
| 受管理表示 | 新库根 `AGENTS.md`、`kb/`、`app/templates/`、`app/views/`、`app/rules/`、`app/manifest.json` | `kb-obsidian` 初始化器；词表表示来自 `kb-design` 导出器 | 是正式设计与数据的应用表示，不是正式编辑源 |
| 派生报告 | `app/reports/` | `kb-obsidian` 校验和报告命令 | 只保存可重算事实与复核线索，可以删除和重建 |
| 应用配置 | `.obsidian/` | 初始化器给出最低基线，其余由使用者维护 | 不修改模型、正式数据或项目决定 |

受管理表示和派生报告中的所有文件都可以由文件系统工具修改；只有 Obsidian 支持的 Markdown 和 Base 文件可以在 Obsidian 中编辑，普通 JSON manifest 不是 Obsidian 内容格式。对这些文件的修改不回流、不取得项目效力；受管理文件的变化只形成 manifest 漂移，派生报告不作为下一次结论的输入。用户文件不属于受管理写集，生成器不得覆盖、移动或删除。


根规则只在 manifest 明确登记时属于受管理写集。旧库中未登记的同名文件保持原权属；校验和刷新均不自动接管。已登记规则的缺失、符号链接或字节漂移必须阻断后续内容与刷新操作。

## 文件布局

完整应用使用一个不嵌套的 vault，目录只区分稳定职责，不复制主题分类树。新库根 `AGENTS.md` 是固定代理入口，以 `rule` 类型纳入 manifest，是应用小写命名约定的精确例外。旧库不会因运行校验或词表刷新自动获得该文件。

```text
AGENTS.md
home.md
inbox/
sources/
  clippings/
  references/
  files/
content/
indexes/
attachments/
kb/
  topics/
  arrays/
  entities/
  sources/
  types/
  genres/
  forms/
  views/
    topics.base
    entities.base
    sources.base
app/
  templates/
  views/
  reports/
  rules/
  manifest.json
.obsidian/
```

`home.md` 由初始化器提供起始内容，链接到 `inbox/`、外部资料、全部内容、草稿入口、最近修改、常用用户索引、正式主题、正式实体、正式来源用途和维护报告；初始化后归使用者所有，不再由更新器覆盖。

`inbox/` 保存尚未完成对象判断的临时文件。`sources/clippings/` 保存网页剪藏，`sources/references/` 保存使用者对外部资料的阅读说明，`sources/files/` 保存 PDF 等原始文件。`content/` 保存内容单元，默认不按主题、实体、类型、体裁、状态或层级建立子目录。`indexes/` 保存个人导航壳。`attachments/` 是用户文件引用的附件位置，不赋予附件内容单元或正式实体身份。

`kb/` 保存六份正式词表的受管理表示；其中 `kb/views/` 保存三个参考 Base。`app/templates/` 保存受管理结构片段。`app/views/` 保存完整应用的 Base 与固定查询入口，至少提供全部内容、draft 内容、active 内容、deprecated 内容、按主题、按实体、按类型与体裁、最近修改、全部正式主题、unassigned 主题、正式实体、正式来源用途和维护报告入口。`app/reports/` 保存诊断和统计，`app/rules/` 保存面向使用者的应用规则说明，`app/manifest.json` 保存完整应用受管理写集的项目清单。`.obsidian/` 只保存最低运行配置和用户后续配置。

完整应用布局由 `kb-obsidian` 初始化器建立，词表参考表示、应用文件、用户目录和最低 Obsidian 配置在发布前共同回读校验。`kb-design` 的独立参考导出仍只生成本文后部规定的根 `index.md`、`kb/` 和根 `manifest.json`；它是初始化器的上游输入，不单独冒充完整 vault。

## 终端访问

AI 优先使用原生 CLI 与本地命令；工具无法完成时直接说明并交由用户处理，只有用户明确要求界面检查或操作时才使用 Computer Use。流程为确认目标绝对路径、显式选库、有限搜索、读取上下文，再按授权处理。使用 `obsidian vault=<目标ID> vault info=path` 确认实际路径；名称重复时按本机注册信息取得 ID，不使用默认活动库。ID 在命令之前，不能移到命令之后。完整示例见[应用说明](../../../apps/obsidian/README.md#终端访问)。

搜索初始上限为 10，初次读取最多三个候选；核对 ID、label、scope、上位、数组和来源。正文、文件名、alias、命中次数或 Base 行都不能直接批准 subject 或概念关系。UUID 内容使用标题、alias 和正文检索。

调用方检查超时、退出码、错误文本、JSON 结构和路径匹配。退出码 0 不等于成功；失败、截断或超时不得触发后续写入。热路径设 2 秒期限，仅串行重试一次，冷启动期限单独处理。AI 写入边界以[终端访问决定](../../decisions/obsidian-agent-entry.md)和生成的根规则为准；本阶段没有新的 CLI 包装器、自动分类或属性更新接口。

## 对象边界

| 对象 | 所在位置 | 取得身份的条件 | 不取得的效力 |
|---|---|---|---|
| 临时文件 | `inbox/` | 无；只要能保存捕获上下文 | 不属于内容模型，不参与正式计数 |
| 外部资料 | `sources/` | 保存实际材料或阅读说明 | 不是内容单元、正式来源用途或正式实体 |
| 内容单元 | `content/` | 用户执行建立动作，取得 identifier 并满足必填字段 | 不因文件存在自动成为 `active` |
| 用户索引 | `indexes/` | 用户选择、排列和解释链接 | 不是主题、数组、概念组或正式关系 |
| 正式表示 | `kb/` 与受管理应用文件 | 从正式编辑源生成并通过 manifest 校验 | 不是正式编辑源，编辑不回流 |
| 派生报告 | `app/reports/` | 从本次通过校验的输入重算 | 不是正式数据、决定或自动动作 |

`inbox/` 文件可以丢弃、合并、移入 `sources/`，或经人工判断建立为内容单元。`inbox/` 中的字符串、Wikilink、tag 和语言模型输出只作上下文；它们不建立项目对象。

外部资料必须区分原文摘录和使用者批注。Web Clipper 与人工复制保存的标题、作者、发布日期、捕获日期、URL 和正文只描述捕获事实，不构成 designation、概念对应、来源资格或引用批准。能独立复用的理解另建内容单元；需要进入内容字段的文献或标准，必须先取得现行正式实体身份。

`content/` 中每个 Markdown 文件恰好表示一个内容单元。文件 stem 与 `kb_id` 使用同一个无前缀、小写 UUIDv4；一级标题和 `title` property 保存内容标题，`aliases` 保存由应用从当前标题派生的一个查找形式，正文保存内容。标题、alias 和显示文本都不能反推身份。

`indexes/` 只保存入口说明、阅读顺序、普通链接和嵌入视图。若索引包含可独立引用并需要受控标引的实质说明，正文必须建立为 `content/` 内容单元并使用适用的 `form: index`；`indexes/` 只链接该内容单元或嵌入其视图，不保存第二份正文。

## 内容流程

捕获只要求保留上下文，不要求立即完成正式判断。

```text
想法、链接、网页、书籍、PDF
              |
              v
           inbox/
              |
         人工判断去向
       /       |       \
    丢弃    sources/   content/
               |          ^
               +----------+
                理解与转述
```

Obsidian URI、Unique note creator 和普通新建命令只能作为 `inbox/` 捕获入口。Web Clipper 默认只写 `sources/clippings/`，可以创建或追加资料文件，但不能直接创建内容单元、正式实体、正式来源用途或词表记录。

### 内容建立

内容建立必须通过受管理模板配合建立器，或具备同等约束的工具完成。Templates 只能插入片段和日期，不能生成并检查合法 identifier、校验受控值或保证必填性。建立器生成无前缀、小写 UUIDv4，检查现有 identifier 和目标路径没有重复，让使用者选择恰好一个 `type`、恰好一个 `genre` 和至少一个非 deprecated `subject`，写入一级标题、`title`、由标题派生的 `aliases`、`created` 与 `status: draft`，再回读并运行单文件校验。无法判断必填值时，材料继续留在 `inbox/`。

identifier 规则已经由[内容单元标识符](../../decisions/content-unit-identifiers.md)决定，`kb-obsidian new-content` 已实现上述受约束的 `draft` 建立路径。建立器可用只证明应用行为存在；新文件仍须由使用者提供内容和受控选择，建立动作也不批准 `active` 状态或激活正式消费者。

### 内容状态

`draft` 表示尚未完成。转为 `active` 前，内容必须能够独立引用，所有必填字段和基数正确，受控引用命中正确对象种类，`subject` 不指向 deprecated 主题，内容间 `relation` 满足互反条件，外部材料与使用者陈述能够区分，并由使用者明确批准状态变化。校验器只判断机械条件，不能代替内容判断和批准。

`active` 内容因直接替代或确认过时转为 `deprecated`。直接替代且存在替代项时填写 `isReplacedBy`；确认过时且没有替代项时留空，并在正文首段说明原因。deprecated 内容保留原 identifier 和路径，不移入 Archive，也不删除。

唯一删除例外是误建且没有任何引用的内容单元。删除须按[内容模型](../model/content-model.md)的现行处置决定和[治理](../governance/governance.md)的决策权执行；报告和校验器不能自动删除。

## 身份规则

内容路径是 `content/<uuidv4>.md`。`identifier` 和文件 stem 使用同一个符合 RFC 9562 标准文本表示的 UUIDv4：小写、保留连字符、不加对象前缀。唯一语境是一个知识库中的全部内容单元；建立时检查现有 identifier 和路径，重复时重新生成。一经写入且被引用后，identifier 和路径不随标题变化。

[标识符](../../concepts/content-identifiers.md)区分身份、名称、标题、路径、排序信息和时间信息。UUIDv4 不从 Unique note creator、文件名、标题、名称翻译、拼音、时间戳或语言模型输出派生，也不充当密码、权限、真实性或完整性证明。路径包含 UUID 是 Obsidian 的确定性 binding，不把 path 与 identifier 重新定义为同一概念。

## 字段约束

词表矩阵逐个记录 source identity、必填性与基数、literal／reference、datatype 或受控值、target location／property、缺省与省略、loss 保存位置和可逆性。内容矩阵在相同语义边界上另记录建立条件、编辑条件、查询用途和无效表现。

词表对象只写非空 properties；`None`、空字符串和空列表省略。当前词表表示使用 Text、List、Date 和 Tags。相同 property name 在一个 vault 中必须保持同一 Obsidian type。引用单值使用 Text link，引用多值使用由 Text link 组成的 List，日期使用 Date，其他 scalar 使用 Text。

## Obsidian 表示

对象文件使用 UTF-8 Markdown。一级标题保存显示标签或标题；YAML frontmatter 保存可平坦表达并用于查询的 properties；范围、语言依据、外部依据、项目判断、外部映射和历史记录进入正文。property 中的 Wikilink 整体按 YAML 字符串保存。

Obsidian 当前不支持 nested properties，官方建议在 Source mode 中查看它们。本 target 不为正式对象选择 nested properties，列表元素也只使用 scalar；不能平坦表达的结构进入正文表格或 YAML 代码块。`.base` 文件使用 YAML 保存 filters 和 views。项目 manifest 的 `.json` 只服务项目校验，不是 Obsidian 内容对象。

tag 不承担主题、实体、文档类型、体裁、生命周期或正式关系。固定应用 tag 只能区分系统对象或视图范围，不能替代受控字段。

## 词表表示

输入只接受现行严格格式。六份词表均要求 `schema_version: 2`；实体与来源用途文档另要求各自的 `schema`，所有文档保留 `version` 和集合；旧 `url`、`checked`、`role`、紧凑来源引用及未知字段阻断导出。语言依据继续使用独立的已采纳合同，包括语言 `legacy`，不与外部来源依据混用。

下表指定 location、type、reference form 与 loss。所有表示均无回流接口。缺失的可选值和空列表不生成 property；正文保留结构所需的空值。实体与来源用途的形状使用核心生成 schema，内部引用必须存在，实际来源使用须具备对应 approved 角色；导出对捕获的词表、决定、义务和语言采纳字节调用完整核心语义检查，覆盖字段精准采纳、复核周期、观察政策和语言依据，不重新读取这些输入。通过检查仍不等于发布或正式消费者激活。

### 文档字段

| 源字段 | 目标落点与类型 | 引用与信息保存 |
|---|---|---|
| `schema`、`schema_version` | 输入门禁；不另设 property | 只接受对应文档新格式，不回退 |
| `version.id` | `kb_version` Text 与 manifest 输入版本 | 原值保存 |
| `version.date`、`version.note` | manifest 的原始输入 SHA-256 | 不在笔记独立呈现；哈希不能恢复文字 |
| 六份词表的集合 | 对象路径、`kb_object` Text、固定 Tags 和 manifest 数量 | ID 决定路径，集合次序不改变身份；主题顺序用于数组成员次序 |
| 载体数组 | 根 `index.md` 的数组表及各数组完整正文 | 不生成独立笔记或 property；保存本地项目判断或完整外部分组 |

### 公共字段

| 源字段 | 目标落点与类型 | 引用与信息保存 |
|---|---|---|
| `id` | `<id>.md`、`kb_id` Text | 稳定 ID 原值保留，非法、重复及悬空身份阻断 |
| `label` | 一级标题、`kb_label` Text、`aliases` List | 显示次序为中文、英文、ID；所有非空形式保存，非显示形式的语言键不保留 |
| `alt`、`hidden` | aliases 与正文“替代形式”“隐藏形式” | 正文保存语言、顺序、重复；aliases 去重，不保存原 scalar／list 差别和空列表 |
| `status` | `kb_status` Text | 始终表示项目生命周期，不受来源外部状态覆盖 |
| `added` | `kb_added` Date | 原日期保存 |
| `scope` | 正文“范围” | 原文保存，不生成 property |
| `basis.zh`、`basis.en` | 正文“形式依据” | 按[语言依据](../model/topics.md#语言依据)保存等级、来源、定位，或模型、日期、判断、授权与未核实声明；不改变语言 legacy 的性质 |
| 外部 `basis.subjects` | 正文“外部依据”表 | 逐组保留 values 主题 Wikilinks、references 来源实体 Wikilinks、locator、checked；不把记录级依据乘成逐值独立证明 |
| 其他外部 `basis` | 正文“外部依据”表 | 每条保存字段、来源实体 Wikilink、locator 与可选 checked |
| `assertions.subjects`、`assertions.source` | 正文“项目判断”表 | 保存适用主题 Wikilinks、project_assertion、原 self 与审计定位；不产生外部依据链接 |
| `source` | `kb_source` Text link 与正文“派生来源”表 | registry 投影为来源用途 Wikilink；正文另保存 item、locator 及每条相邻依据的实体 Wikilink、locator、checked |
| `match` | 正文“外部映射”表 | 每条保存 registry Wikilink、item、rel 与完整相邻依据；不默认补关系 |
| `history` | 正文“历史记录”YAML 代码块 | 保存真实日期、动作、字段、决定、前后值、依据及次序；注释和原排版不保留，历史 checked 不冒充当前 review.checked |

### 关系字段

| 源字段 | 目标落点与类型 | 引用与信息保存 |
|---|---|---|
| 主题、类型、体裁、载体 `broader`、`related` | `kb_broader`、`kb_related` List | 同类对象 Wikilinks，全部关系与次序保留 |
| 主题 `arrays` | `kb_arrays` List | 主题数组 Wikilinks，保留次序 |
| 类型、体裁、载体 `arrays` | `kb_arrays` List | 原数组 ID 保存；载体数组只在根索引呈现，不伪造笔记链接 |
| 主题数组 `superordinate` | `kb_superordinate` Text link | 指向真实主题 |
| 主题数组的派生成员 | `kb_members` List | 主题 Wikilinks，顺序取正式主题记录，不生成新的 source 字段 |
| 载体数组 `local_analysis` | 根索引“隔离记录”表 | 逐字保存 legacy_source_label、isolated 状态与真实决定 ID；仅为历史隔离，不生成来源链接或有效本地分析 |
| 数组 `external_group` | `kb_source` Text link 与正文“外部分组” | registry 需要 structure approved；完整保存 item、locator、相邻依据，不推导成员派生 |
| 主题、类型、体裁、载体 `replaced_by` | `kb_replaced_by` Text link | 指向同类正式对象，历史理由在 history 保存 |

### 实体字段

| 源字段 | 目标落点与类型 | 引用与信息保存 |
|---|---|---|
| `kind`、`tier`、`form` | `kb_kind`、`kb_tier`、`kb_form` Text | 原值保存；实体 form 是既定 literal，不伪造载体词表链接 |
| `subjects` | `kb_subjects` List | 真实主题 Wikilinks，原次序保留 |
| `vendor`、`creator` | `kb_vendor` Text link、`kb_creator` List | 指向所有实体，包括一般实体 |
| `replaced_by` | `kb_replaced_by` Text link | 一般实体为项目替代；来源实体为有依据的外部替代，空值不推导替代目标 |
| `version`、`fixed_sha256` | `kb_entity_version`、`kb_fixed_sha256` Text | 原值保存，不生成固定内容声明；来源 version 为 null 时省略版本 property，正文显示“未登记可核实版本” |
| `source_status` | `kb_source_status` Text 与正文“外部状态” | 有值只表示 current／superseded／withdrawn；来源缺值时省略 property，正文显示“外部状态未核实”，不推导 current；一般实体不显示该缺口 |
| `urls` | 主地址投影为 `kb_url` Text；正文“来源地址” | 完整列 role、url、primary，保留所有非主地址；一般实体地址不自动取得证据用途 |
| `review.checked`、`review.next_due` | `kb_checked`、`kb_next_due` Date | 只保存当前 review 值；null 不推导日期 |
| `review.interval_months`、`review.grace_days` | `kb_interval_months`、`kb_grace_days` Number | 原周期保存 |
| 完整 `review` | 正文“复核安排” | 全字段保留，包括 obligations 的真实 ID；未导出的义务不伪造 Wikilink |
| `watch` | 地址列表投影为 `kb_watch` List；正文“观察对象” | 完整列 locator、signals、availability／redirect／content 周期；属性投影不代表完整观察合同或实际探测 |

### 用途字段

| 源字段 | 目标落点与类型 | 引用与信息保存 |
|---|---|---|
| `entity` | `kb_entity` Text link | 指向真实来源实体，保持用途与实体身份不同 |
| `roles` | `kb_roles` List 与正文“用途资格” | 属性只列角色名，正文逐项列 role、proposed／approved／retired、decision；真实决定 ID 作为文本，不伪造不存在的 vault 链接 |
| `roles` 中 approved 项 | `kb_approved_roles` List | 专用于资格筛选，不从 kb_roles 推导批准 |

来源用途和主题数组无 label、status、aliases 字段时，以 ID 显示标题和 kb_label，不生成 kb_status 或 aliases。所有 aliases 只消费既有形式，不翻译、不补名，链接目标仍是稳定 ID 文件。

## 内容表示

内容字段已经由 `kb-obsidian` 的建立器和只读校验器实现。建立器只负责新建时可安全取得的字段；其余字段可以由使用者编辑，并在校验时按下表检查。下表保留[内容模型](../model/content-model.md)的 16 个字段、基数和值域，并规定创建、编辑、查询和失败行为。表中路径与 properties 是 target binding，不改变 identifier 发放规则，也不证明消费者已经读取真实内容。

### 内容字段

| 源字段 | 必填与基数 | 值形态与值域 | 目标落点 | 创建条件 | 编辑条件 | 查询用途 | 无效表现与 loss |
|---|---|---|---|---|---|---|---|
| `identifier` | 必填，恰好一个 | literal identity；无前缀、小写、保留标准连字符的 UUIDv4；在一个知识库的内容单元中唯一 | `kb_id` Text；`content/<uuidv4>.md`，文件 stem 与值相同 | 建立器生成后检查现有 identifier 和路径；重复时重新生成 | 一经写入且被引用后不修改；标题变化不改值或路径 | 精确定位内容与解析 content-unit reference | 缺失、格式错误、前缀、大小写错误、重复、stem 不同或路径冲突使内容无效；不从标题、alias 或时间回填；回流未实现 |
| `title` | 必填，恰好一个 | Text | 一级标题与 `title` Text；Obsidian `aliases` List 中恰好包含一个由应用派生的当前标题 | 建立时由使用者给出，并同步写入三个位置 | 修改标题时同时更新一级标题、`title` 和派生 alias，不改 identifier | 显示、全文与 property 检索、Base 排序，并通过 alias 供 Quick Switcher 和链接补全 | 任一位置缺失、三者不一致、alias 多值或重复时无效；不从文件名回填；回流未实现 |
| `type` | 必填，恰好一个 | type reference；命中正式文档类型词表 | `kb_type` Text link，指向 `kb/types/<id>.md` | 建立前由使用者选择一个 | 改值须重新校验引用与内容用途 | 按文档类型筛选与统计 | 缺失、多值、悬空或对象种类错误时无效；回流未实现 |
| `genre` | 必填，恰好一个 | genre reference；命中正式体裁词表 | `kb_genre` Text link，指向 `kb/genres/<id>.md` | 建立前由使用者选择一个 | 改值须重新校验作者立场 | 按体裁筛选与统计 | 缺失、多值、悬空或对象种类错误时无效；回流未实现 |
| `form` | 可选，零个或一个；长文不填 | form reference；命中正式载体词表 | `kb_form` Text link，指向 `kb/forms/<id>.md` | 只有内容采用该载体时填写 | 载体改变时可修改或省略 | 按载体筛选 | 多值、悬空或对象种类错误时无效；省略不产生替代值；回流未实现 |
| `level` | 可选，零个或一个 | controlled literal；`remember`、`understand`、`apply`、`analyze`、`evaluate` 或 `create` | `kb_level` Text | 建立时可由作者评估 | 理解深度改变时可修改 | 按认知层级筛选 | 多值或域外值无效；缺失时省略；回流未实现 |
| `subject` | 必填，一个或多个 | topic reference；命中非 deprecated 正式主题 | `kb_subjects` List of Text links，指向 `kb/topics/<id>.md` | 建立前至少选择一个 | 内容主题改变时人工修改并重新校验 | 正式主题直接计数、主题入口和 Base 筛选 | 空列表、悬空、对象种类错误或 deprecated 目标使内容无效；顺序与全部目标须保存；回流未实现 |
| `entities` | 可选，零个或多个 | entity reference；命中正式实体 | `kb_entities` List of Text links，指向 `kb/entities/<id>.md` | 内容涉及正式实体时填写 | 涉及对象改变时人工修改 | 实体涉及计数与实体入口 | 悬空或对象种类错误时无效；缺失或空列表省略；全部目标与顺序须保存；回流未实现 |
| `source` | 可选，零个或一个 | content-unit 或 entity reference；必须识别目标种类 | `kb_source` Text link；内容指向 `content/<uuidv4>.md`，实体指向 `kb/entities/<id>.md` | 内容实际派生自一个内容单元或实体时填写 | 派生判断改变时人工修改，不用 `references` 或旧 `origin` 替代 | 分开查询内容派生与实体派生 | 多值、悬空或对象种类错误时无效；目标种类必须保留；回流未实现 |
| `references` | 可选，零个或多个 | entity reference；命中作为文献或标准的正式实体 | `kb_references` List of Text links，指向 `kb/entities/<id>.md` | 内容引用已取得正式实体身份的文献或标准时填写 | 引用变化时人工修改，不从 `entities` 推导 | 正式引用计数与参考资料入口 | 悬空、对象种类或实体 kind 错误时无效；缺失或空列表省略；回流未实现 |
| `created` | 必填，恰好一个 | ISO 8601 Date | `kb_created` Date | 建立内容单元时写入 | 不随普通编辑改变 | 按建立日期排序和筛选 | 缺失、格式错误或多值无效；不从文件时间回填；回流未实现 |
| `modified` | 可选，零个或一个 | ISO 8601 Date | `kb_modified` Date | 建立时可以省略 | 内容发生受记录的修改时更新 | 最近修改视图 | 格式错误或多值无效；缺失时省略，不从文件时间回填；回流未实现 |
| `status` | 必填，恰好一个 | controlled literal；`draft`、`active` 或 `deprecated` | `kb_status` Text | 新建固定为 `draft` | 只有通过适用校验并经使用者批准才能转换 | 草稿、在用和废弃内容视图 | 缺失、多值、域外值或不合法转换无效；校验器不自动降级或升级；回流未实现 |
| `isReplacedBy` | 因直接替代而 deprecated 且有替代项时必填一个；其他情况零个 | content-unit reference | `kb_is_replaced_by` Text link，指向 `content/<uuidv4>.md` | 新建 draft 不填 | 直接替代并转为 deprecated 时填写；无替代过时时省略并在正文首段说明 | 沿替代链导航 | 条件必填时缺失、目标悬空或对象种类错误时无效；回流未实现 |
| `relation` | 可选，零个或多个 | content-unit reference；满足内容模型的使用条件并互反 | `kb_relation` List of Text links，指向 `content/<uuidv4>.md` | 仅在主题不同且常被一起阅读时填写 | 任一端改变时同时复核两端 | 查询正式内容间 relation | 悬空、对象种类错误或不互反时报告无效；不从正文链接或 Backlinks 推导；回流未实现 |
| `language` | 可选，零个或一个 | Text；默认 `zh` | `kb_language` Text | 默认语言为 `zh` 时可省略，其他值填写 | 主要语言改变时修改 | 按语言筛选 | 多值无效；省略只表示既定默认 `zh`；不另立 target 值域；回流未实现 |

正文位于 frontmatter 和唯一一级标题后，使用 Markdown，可为空；它不是 metadata property，也不从 `description` 生成。校验器检查 frontmatter、一级标题和受控字段边界，不从正文推导正式字段；正文中的 Wikilink、tag、字符串和 unlinked mention 都不替代上述字段。

## 引用语法

所有引用都以目标稳定 ID 计算路径，以当前标题或正式 label 计算显示文本。

```md
[[content/<uuidv4>|内容标题]]
[[kb/topics/security|安全]]
[[kb/entities/obsidian|Obsidian]]
```

显示文本缺少中文时使用英文，两者都缺少时使用 ID。显示文本不参与目标解析。property 中的链接整体按 YAML 字符串保存，Text 和 List property 中的内部链接加引号。正式对象引用必须解析到正确种类的生成目标；内容引用必须解析到内容单元。本 target 不使用标题引用或块引用承担身份。

内容 `aliases` 是从当前 `title` 派生的 Obsidian 查找表示，不是内容模型新字段、术语形式或同义关系。基线不自动保存旧标题或增加其他 alias。Quick Switcher 按 alias 查找 UUID 文件；Search 检索标题、正文和 properties；Bases 按内容字段筛选。人的查找不依赖 UUID。

## 导航分工

| 入口 | 回答的问题 | 不能承担 |
|---|---|---|
| 正式主题树 | 正式知识范围、上位、下位、相关、数组、状态和依据是什么 | 用户阅读顺序、自动补主题或内容目录分类 |
| 用户索引 | 使用者怎样理解、选择和进入一组内容 | `broader`、`related`、数组、分面或概念组效力 |
| Bases | 哪些文件满足已声明的 property 条件，怎样排序与浏览 | 只读权限、正式审批、编辑源或回流 |
| Search | 正文、路径、tag 或 property 当前匹配什么 | 可审计的查询事件和未匹配查询统计 |
| Quick Switcher | 按内容 title 派生的 alias 查找并打开 UUID 文件 | identifier 发放、正式分类或完整字段检索 |
| Backlinks | 哪些文件链接或提及当前文件 | 正式引用计数、relation 或概念判断 |
| Graph | 现有内部链接形成什么文件网络 | 正式主题结构、关系证明或盲区计量 |

`home.md` 是全库入口；Bookmarks 可以固定 `home.md`、`inbox/`、常用索引、草稿视图和维护报告，但只是个人快捷入口。`app/views/` 的基线使用 Obsidian Bases，不把 Dataview 或其他社区插件作为必要条件。Base 可以编辑文件及 properties，因此受管理 Base 只表示生成权和项目效力，不表示 UI 权限。

### 主题入口

主题入口同时显示上位、下位、相关、数组、scope、依据、状态、外部映射、直接使用该主题的内容列表和仅作统计的下位分支聚合计数。`unassigned` 和零引用主题继续可见。分支聚合不能给内容增加更宽的 `subject`，也不能改变主题引用语义或状态。

实体入口分开显示 `kb_entities`、`kb_references` 和适用的 `kb_source` 所形成的内容列表。正文提及、Backlinks 和普通链接不能与这些正式字段合并成一种关系。

## 正式主题

应用必须完整呈现已借入的知识体系。`status: unassigned` 的正式主题即使没有内容也必须保留和浏览；应用不得隐藏空分支、删除零引用主题或用已有内容反向裁剪正式结构。

对应视图至少显示主题 ID、label、上位、来源、状态、直接内容数和分支聚合内容数。视图只呈现事实，不把 `unassigned` 自动改为 `active`。

## 内容与检索

实际写作和检索中，报告需要呈现无法选择合适正式主题、正文反复出现未登记字符串、宽主题吸收过多内容、内容集中在正式结构的小部分、同一实体或来源被不一致表示，以及用户索引反复需要正式结构没有稳定入口等现象。

核心 Search 没有提供本项目可审计的 search-event interface，因此不能计算“没有匹配任何概念的检索次数”。近期查询 UI 或 Search 存在不能冒充查询日志。正文未解析字符串只进入 `app/reports/`，并保留文件、位置和上下文；它是 report-only 线索，不自动创建候选、designation、概念、关系、状态或违规结论。

## 使用计数

正式使用计数只读取 `content/` 中通过校验的受控字段：

- 主题使用读取 `kb_subjects`；
- 实体涉及读取 `kb_entities`；
- 正式引用读取 `kb_references`；
- 派生来源按目标种类读取 `kb_source`。

主题直接引用计数只计字段中明确出现的该主题。分支聚合计数沿正式下位关系汇总，只服务覆盖观察；它不把上位主题写入内容，也不改变直接计数。

正文 Wikilink、Backlinks、用户索引成员、aliases、unlinked mentions 和 Graph edges 都不进入正式计数。它们可以提供人工探索线索，不能替代受控字段语义。正式库已观察到一条 draft；实际报告须按当次有效内容计算。内容存在不自动启用正式消费者，也不能把历史空库报告当作当前计数。

## 维护反馈

应用只提供单向反馈，不自动回流。

```text
内容与资料
    |
    v
机械校验与统计
    |
    v
app/reports/ 带上下文线索
    |
    v
人工复核与决策权判断
    |
    v
修改 kb-design 正式编辑源
    |
    v
重新生成受管理表示
    |
    v
重新校验内容与报告
```

报告写集只能位于 `app/reports/` 的本次临时目录和成功发布的报告集合。报告生成器不读取旧报告作为新结论输入，也不能写 `content/`、`indexes/`、`kb/`、`app/templates/`、`app/views/`、`app/rules/`、`.obsidian/` 或仓库正式编辑源。

报告命中[维护](../governance/maintenance.md)阈值时，只能提出适用动作并给出位置与上下文。批准、废弃、删除、拆分、合并、找依据、复核来源、注明不覆盖和发版仍按[治理](../governance/governance.md)的决策权执行。报告永远不能修改内容状态、词表状态、概念、关系、designation、来源、决定或发版状态。

## 能力边界

| Obsidian 能力 | 本项目用途 | 不用于 |
|---|---|---|
| File Explorer | 浏览稳定职责目录和文件 | 主题树、多上位、状态或正式关系 |
| Properties | 保存内容 binding 和可查询的平坦事实 | nested formal structures、自动语义判断或完整校验 |
| Properties view | 已启用的 core plugin，用于观察并维护同名 property type 一致性 | 正式 schema、基数、引用种类和生命周期校验 |
| Templates | 插入合法结构片段、标题和日期 | 分配有依据的 ID、选择受控值或保证完整性 |
| Unique note creator | 快速建立 `inbox/` 临时文件 | 正式内容 identifier 或内容建立 |
| Web Clipper | 把网页正文、URL 和页面变量保存到 `sources/clippings/` | 直接建立内容单元、正式实体、术语或来源资格 |
| Internal links | 表达 target reference syntax 和普通阅读链接 | 自动取得项目关系效力或反推身份 |
| Backlinks | 查看 linked／unlinked mentions 和人工上下文 | 正式引用计数、relation 或概念判断 |
| Bases | 查看、排序、筛选和编辑文件及 properties | 权限只读、正式审批、数据源或回流 |
| Search | 查询正文、路径、tag 和 properties | 可审计的未匹配查询日志 |
| Quick Switcher | 按文件名或 alias 快速打开笔记；内容 title 作为派生 alias | 完整元数据检索、identifier 发放或正式关系 |
| Bookmarks | 固定个人常用入口 | 项目导航真值、正式分类或关系 |
| Graph | 探索现有文件链接 | 正式主题树、关系证明或盲区计量 |
| Canvas | 临时整理和讨论 | 正式结构、内容模型、统计输入或编辑源 |

Web Clipper 基线只使用 preset variables；Interpreter 和 prompt variables 默认禁用。它们需要外部模型并带来速度、成本与隐私差异，输出也不取得正式效力。Templates 和 Web Clipper 模板可以创建或追加文件，但文件存在不等于对象合法。

基线不安装社区插件。未来引入插件前，必须说明它解决的真实失败、退出路径、数据位置、对 Markdown 的影响和缺失时的降级行为；普通 Markdown、核心 Base、Search 和报告入口必须继续可用。

## 配置边界

初始化器只给出应用运行所需的最低 `.obsidian/` 配置：使用 Properties 保存内容 binding 和可查询事实，并启用 Properties view、Templates、Bases、Search、Quick Switcher、Backlinks、Bookmarks 和适用的 core plugin；把 `app/templates/` 设为模板目录，把 `attachments/` 设为附件目录；启用内部链接随 Obsidian 内移动和改名更新；登记项目 property types。初始化只接受不存在或为空的目标，不更新非空 vault，也不覆盖后续用户选择。

主题、字体、窗口布局、快捷键、移动端布局、Sync、Publish 和个人插件归使用者。`app/manifest.json` 不把这些用户配置变化报告为受管理表示漂移。

## 失败处理

| 失败 | 处理 |
|---|---|
| 正式词表或受管理表示无效 | 阻断新 vault 初始化，不创建目标 vault |
| 目标目录非空、是符号链接或受保护路径 | 阻断，不修改目标 |
| manifest 与受管理文件不一致 | 报告路径、期望 hash 和实际 hash；不把本地修改回写正式数据 |
| 内容 ID 重复或路径冲突 | 内容校验失败，报告全部冲突位置，不改名或覆盖 |
| active 内容缺少必填字段或引用无效 | 报告阻断问题，不自动降为 draft |
| draft 内容字段、基数或引用无效 | 报告问题并保留用户文件，不自动改写 |
| 受控引用悬空或对象种类错误 | 报告源文件、字段、值和期望目标种类 |
| relation 不互反 | 报告两端，不自动补关系 |
| Web Clipper 提取缺失或错误 | 保留 URL 与原始上下文，交人工修正，不建立正式对象 |
| 报告生成中断 | 保留用户内容和受管理表示，不发布临时报告目录 |
| 可选社区插件缺失 | 基线功能不受影响；增强视图不可用但保留普通入口 |

任何诊断失败都不得删除、移动、降级或改写用户内容。自动修复不在当前设计范围内。网页、PDF、摘录和外部 vault 内容属于不受信任输入；捕获器不得执行其中的命令、代码或提示。

## 现行导出

`apps/obsidian/src/kb_obsidian/exporter.py` 是完整应用的上游参考导出器。它只读取六份正式词表，生成单向参考区：根 `index.md`、`kb/` 和根 `manifest.json`。完整应用的初始化与刷新通过应用包内部调用该导出器；独立参考 artifact 可用 `uv run python -m kb_obsidian.exporter` 生成。导出器不读取或生成 `home.md`、`inbox/`、`sources/`、`content/`、`indexes/`、`attachments/`、`app/` 或 `.obsidian/`，回流仍未实现。

### 现行布局

现行独立输出是完整、独立的参考 artifact；旧的大写布局不是有效输出，也不保留别名或兼容目录。

```text
index.md
manifest.json
kb/
  topics/
  arrays/
  entities/
  sources/
  types/
  genres/
  forms/
  views/
    topics.base
    entities.base
    sources.base
```

对象文件名为 `<id>.md`。标签、别名和译名变化不改路径。除根 `index.md` 和根 `manifest.json` 外，项目控制文件都位于 `kb/`，路径、目录、Base 文件名和扩展名均为小写 kebab-case；不得包含大写 ASCII、空格、下划线或重复连字符。内部链接一律为以 `kb/` 开始的 vault 根路径 Wikilink；普通 Markdown link 只用于外部 URL。普通 `.json` 不在 Obsidian accepted content formats 中；根 `manifest.json` 是独立参考导出的项目清单，不是内容对象，也不能替代完整 vault 的 `app/manifest.json`。

### 浏览入口

现行导出生成 `topics.base`、`entities.base` 和 `sources.base` 三个 `.base` 文件。每个 Base 用 `file.inFolder()` 和 Markdown 扩展名收窄默认数据集，并提供 table view；不使用 formulas、Backlinks 聚合、插件视图或自动写回动作。

Base 是可编辑界面。经 Base 修改对象笔记与直接编辑 Markdown 一样，不回流、不取得项目效力，并可能在再次导出时被覆盖。当前验收只证明 `.base` 按现行规则产生并可解析为 YAML，没有 Obsidian 应用内交互证据。

### 表达缺口

正式记录中的 `basis`、`match` 和 `history` 含嵌套结构，因此进入正文表格或 YAML 代码块；`scope`、替代形式和隐藏形式也进入正文。该 loss 只发生在可查询 property 结构上，信息本身仍写入生成笔记。

语言依据按新结构生成可读正文，外部来源与定位逐项显示；第 5 级明确显示“模型知识 · 第 5 级，外部用法未核实”及模型、日期、判断和授权。第 6 级显示未采用原因，`legacy` 显示历史未重新分级；模型及历史标记不成为来源链接。语言依据历史 list 值按独立语言合同保留；严格外部依据不接受旧字符串或空列表。`alt` 和 `hidden` 的正文表逐行保留语言、顺序、形式与重复次数；`aliases` 汇集非显示形式并去重，因此不保留重复次数，且不保留 hidden 角色。source 的 scalar／list 形状和空列表也不能从 aliases 恢复。

导出器对每类正式记录使用显式允许字段表。未知字段、非法或重复 ID、无法解析的引用、重复输出路径和不能安全序列化的值都会阻断导出；导出器不把未知值放入兜底字段，也不丢弃后继续生成。

### 导出合同

artifact contract 从 `Application Profile` 完成正式词表表示选择后开始，只负责把所选表示由输入快照确定性物化为 bytes、文件集合和可校验发布物。它不得改变 field 的 target location、type、reference form 或允许的 loss。

现行物化规则包括：

- 一次读取六份正式输入的原始 bytes，同一快照同时用于内容和 manifest；
- 按对象稳定 ID 和固定路径排序生成文件，数组成员保持正式记录顺序；
- Markdown、Base 和 JSON 使用 UTF-8，生成文本使用 LF，生成文件以换行结束；
- frontmatter 的 property 顺序由生成器固定，字符串按 JSON quoting 写入 YAML scalar，列表逐项写入；
- Base 由固定 mapping 顺序生成 YAML；
- 项目 manifest 使用 `json.dumps(ensure_ascii=False, indent=2, sort_keys=True)` 并以换行结束；
- 全部文件写入后回读，完成 post-generation validation，再进入发布步骤。

同一受控 source 和当前 environment 下的双跑逐字节一致，只证明现行条件下的 deterministic behavior。项目没有发布可供任何一方独立重建的完整 environment 与 instructions，也没有 independent rebuild 证据，因此不宣称 reproducible build。

固定 JSON 参数不满足 JCS 的全部条件。现行 pretty-printed JSON 有 token 间 whitespace，且没有证明 I-JSON、ECMAScript primitive serialization 或 UTF-16 code unit 排序；当前不宣称 JCS conformance。

### 清单边界

现行 `manifest.json` 保存：

- schema 名称与版本；
- 六份正式输入的路径、版本和 SHA-256；
- 导出器 bytes 的 SHA-256；
- 各正式对象种类的动态计数；
- 除 manifest 自身外，每个生成文件的相对路径、对象种类、输出标识和 SHA-256；
- 内容文件数、包含 manifest 的总文件数和内容集合 SHA-256。

正式对象的输出标识是稳定 ID；`index.md` 与 Base 使用文件 stem 作为 manifest 内部标识。manifest 只接受根 `index.md`、`kb/<collection>/<id>.md` 和 `kb/views/<name>.base` 的小写路径；它不保存生成时间、绝对路径、用户名、输出目录或 mtime，也不把自身列入文件条目和内容集合 hash。

项目 manifest 的双向文件覆盖和 checksum 只证明当前目录中的已列 bytes 与记录一致。输出没有 `bagit.txt`、`data/`、payload manifest 或 tag manifest，不是 BagIt bag，也不宣称 BagIt conformance。checksum 不证明 provenance、真实性、审批、语义正确性、消费者存在、正式激活或可重建性。

### 发布边界

从仓库根运行：

```bash
uv run python -m kb_obsidian.exporter \
  --repo-root . \
  --output /absolute/new/path
```

输出目录必须不存在或为空。导出器拒绝符号链接、仓库根、文件系统根和用户主目录；仓库内目标只允许位于 `output/` 的子目录，也可以显式使用仓库外目录。它不提供覆盖非空目录、合并现有 vault 或删除旧目录的参数。

全部文件先写入目标同级的新临时目录，再回读并校验文件集合、逐文件 hash、Markdown frontmatter、Base YAML、项目控制路径、`kb/` 根路径 Wikilink 及其 Markdown 或 Base 目标和 manifest 双向覆盖。校验通过后，导出器以 `os.replace()` 尝试把临时目录放到目标目录项；失败时只删除本次创建的临时目录，不递归删除用户目标。

`os.replace()` 成功只提供目标目录项的 atomic visibility。它可能因平台、权限、非空目标或跨文件系统等条件失败；当前实现没有 file 或 directory `fsync`，不提供 durability、掉电恢复、多文件事务、并发协调或内容正确性保证。

成功时标准输出是一行排序 JSON，只含 `output`、`content_files`、`total_files` 和 `content_sha256`。参数错误、输入错误或写入错误时，标准错误以 `OBSIDIAN_EXPORT_ERROR` 开头并退出 `1`；`--help` 正常退出 `0`。

导出目录可以作为独立参考 vault。独立参考区的人工替换仍须先导出到新目录、核对项目 manifest 并由人决定；完整应用的既有 vault 使用下文“词表刷新”，同步 `kb/` 与应用清单，不能只复制文件后宣称应用版本已经更新。

## 回流边界

当前没有任何回流接口。人工直接或经 Base 修改正式表示中的 properties、正文、aliases、链接、文件名或 `.base`，都不会写回本仓库，也不取得项目效力；现行导出器不读取这些修改。

未来若提出回流，必须另行设计并保存 vault 文件、位置和上下文，读取稳定 `kb_id`，区分用户内容与生成表示，报告差异，把未解析字符串交人工，再分别完成概念、designation、权限和来源判断。它不得从文件名、alias、tag、Wikilink、Backlinks、索引或 Graph 自动创建记录、关系或状态。

报告形成与回流不同。`app/reports/` 的单向线索只能经人工复核进入 `kb-design` 正式编辑流程；在决定、实现和运行证据齐备前，不存在自动 return interface。

## 验收门禁

- 功能范围、模型引用、字段约束、使用条件和 encoding 与应用无关设计一致，target binding 没有改写字段语义。
- 完整应用的用户文件、受管理表示、派生报告和配置权属分开，受管理写集不覆盖用户内容。
- 每个正式对象恰有一条稳定路径，全部正式引用都有生成目标，全部 `broader` 均被保留。
- properties 可由安全 YAML 解析且只有 scalar 或 scalar list；正文完整保存未进入 properties 的嵌套数据。
- 正式对象 aliases 只来自正式已有形式并去重；内容 aliases 恰好包含由当前 title 派生的一个查找形式，不形成术语或同义关系；`alt` 和 `hidden` 正文仍保留重复行，`basis` 空列表仍可保存。
- 内容矩阵保持 16 个现行字段的字段名、基数和值域；无效 active 与 draft 内容均报告而不改写。
- 正式计数只读取通过校验的 `content/` 受控字段；普通链接与 Obsidian 探索能力不进入计数。
- 报告写集不能修改用户内容、正式表示、正式编辑源、状态、关系、designation、来源或决定。
- 项目 manifest 与现行导出目录双向一致，并证明生成内容和 manifest 使用同一输入快照。
- 相同输入在同一受控环境中的两个独立导出目录逐字节一致；该证据只支持确定性。
- 非空目标、符号链接、目录替换失败和写后回读失败不损坏用户目标；成功替换只宣称 atomic visibility。
- 能力说明不宣称 DCAP、DCTAP、JCS、BagIt、reproducible build、durability、真实消费者或正式激活。

机械计数和 hash 由导出器、应用测试及端到端初始化证明，不另作低价值重复检查。应用实现和本地持久 vault 已经证明内容建立、校验与报告路径存在；实际内容使用、正式消费者和维护反馈仍须由真实运行证据证明，回流仍须另立决定。

## 词表刷新

`apps/obsidian/` 中的工具提供显式 `refresh`，按[词表参考刷新](../../decisions/obsidian-reference-refresh.md)及[工具归属](../../decisions/obsidian-tool-location.md)更新既有 vault 的 `kb/` 与 `app/manifest.json`。初始化和独立导出仍只接受空目标；用户内容、配置、应用模板、视图和规则保持不变，派生报告另由 `report` 更新。

刷新验证旧清单版本、旧设计提交属于当前 Git 历史、旧输入哈希与该提交的字节一致，再核对受管理写集，检查新词表对内容受控引用及显式 `kb/` Wikilink 的影响。Base 仅有 YAML 排版差异、原清单哈希能由生成模板证明且内容语义相同时，保留实际字节并记录其哈希；实质变化仍拒绝覆盖。

新参考区在 vault 外生成并校验，发布前再次核对文件，普通发布异常回滚并保留备份。刷新不实现完整 Obsidian 短链接解析，也不宣称多文件崩溃一致性或断电持久性。工具版本仍为 `0.1.0`，清单 schema 仍为 `1`；迁入不构成发版或正式激活。

## 待定事项

- 正式库已有一条 draft；多份真实材料的完整使用验收、正式消费者及维护反馈仍未闭合。
- 可审计查询日志等待真实查询消费者或明确接口；Search UI 不满足该条件。
- 参考区以外的非空 vault 更新、自动回流、自动修复和社区插件增强继续后置。
- 若未来需要 reproducible build 主张，另行界定 specified artifacts、source、environment 和 instructions，并取得 independent rebuild 证据。
- 若未来需要 durability，另行设计 file 与 directory `fsync`、故障模型和恢复验证；不从当前 atomic visibility 推导。
- TBX 只按[未生效草案](../../drafts/tbx-export.md)中的真实接收方条件重新进入设计。

## 权威来源

- [内容模型](../model/content-model.md)：内容单元、16 个字段、基数、值域、生命周期和处置决定。
- [维护](../governance/maintenance.md)：指标、阈值、单向触发、人工动作和消费者门禁。
- [Application Profile](../../concepts/application-profile.md)：功能范围、模型引用、字段约束、使用指南、encoding 和 target binding 的分层。
- [标识符](../../concepts/content-identifiers.md)：身份、名称、标题、路径、排序和时间的边界。
- [内容单元标识符](../../decisions/content-unit-identifiers.md)：无前缀 UUIDv4、唯一语境、碰撞处理、稳定路径和元数据检索决定。
- [Reproducible Builds](../../concepts/reproducible-builds.md)：确定性、独立重建、manifest、JCS、BagIt、atomic visibility 和 durability 的边界。
- [应用约束与表示分层](../../decisions/application-profile-boundary.md)：本 target 的已采纳职责、消费者、编辑效力和符合性边界。
- [设计与应用分离](../../decisions/form-independence.md)：应用无关模型与 target 分离、正式词表单向导出的现行决定。
- [当前阶段](../../decisions/current-stage-scope.md)：设计同步与正式激活的阶段边界。
- [Obsidian 官方帮助阅读笔记](../../references/obsidian-help.md)：vault、properties、links、aliases、accepted formats、Bases、Search、Quick Switcher、Backlinks、Graph、Bookmarks、Templates、Unique note creator 和 Web Clipper 的行为。
- [DCMI Application Profiles 阅读笔记](../../references/dcmi-application-profiles.md)：Application Profile 组件、`metadata crosswalk`、历史材料状态与项目边界。
- [Reproducible Builds 阅读笔记](../../references/reproducible-builds.md)：确定性与 reproducible build 的证据边界。
- [BagIt 文件包格式阅读笔记](../../references/rfc-8493.md)：项目 manifest 与 BagIt 的边界。
- [RFC 8785 阅读笔记](../../references/rfc-8785.md)：现行 JSON 参数与 JCS 条件的差异。
- [Python 文件系统阅读笔记](../../references/python-filesystem.md)：`os.replace()`、atomic visibility、`fsync` 与 durability 的边界。
