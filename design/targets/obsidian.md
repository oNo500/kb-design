# Obsidian 映射

本文规定 Obsidian 作为 `kb-design` 首个完整落地应用层的 `Application Profile`，并把现行词表参考导出的 artifact contract 保留为其中一个尚未集成的已实现子系统。本文按[内容模型](../content-model.md)引用应用无关语义，再规定 Obsidian 的功能范围、对象职责、field binding、使用方式与具体表示；artifact contract 只负责把已经选定的正式词表表示物化为文件。分层依据见 [Application Profile](../../concepts/application-profile.md)、[Reproducible Builds](../../concepts/reproducible-builds.md)、[方法登记](../principles.md)、[设计与应用分离](../decisions/form-independence.md)和[应用约束与表示分层](../decisions/application-profile-boundary.md)。

## 当前状态

完整应用设计已经建立，但没有激活。当前唯一实现是 `scripts/export_obsidian.py`：它把六份正式词表生成成单向词表参考区。仓库和外部都没有由本项目建立的真实 vault、用户内容、内容建立器、内容校验器、使用报告、查询日志或回流接口；因此内容引用计数、内容使用观察和维护反馈都没有运行证据。

target 文件、字段合同、目录设计、Base 设计、项目 manifest 或现行词表导出存在，都不能证明内容消费者已经实现、启用或读取过真实内容。完整设计也不使来源、术语、内容、消费者或正式切换自动激活。

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

本 target 引用[内容模型](../content-model.md)的内容单元、字段语义、受控值、identifier 和生命周期，引用[主题词表设计](../topics.md)、[命名实体词表设计](../entities.md)、[来源名称规范表](../sources-registry.md)和[层级结构](../hierarchy.md)的正式对象、关系、多上位与数组规则，并按[维护](../maintenance.md)保留指标、阈值、动作和决策权边界。

`Application Profile` 只为既定对象选择 Obsidian location、type、reference form 和允许的 loss。field／property／path binding 是同一应用内部的表示规则，不是 `metadata crosswalk`；它不改变词表层 `crosswalk` 的现行含义，也不得修改应用无关字段的语义、基数、值域、稳定身份或对象关系。

Obsidian 不能直接表达的约束由校验器保留，不能用自由 tag、文件夹、标题或普通链接替代。不能平坦放入 property 的正式结构进入正文表示，但正文不成为正式编辑源。

## 权属分层

一个 vault 同时保存三种权属和一类应用配置。

| 层 | 内容 | 修改者 | 项目效力 |
|---|---|---|---|
| 用户文件 | `Home.md`、`Inbox/`、`Sources/`、`Content/`、`Indexes/`、`Attachments/` | 使用者和经授权的内容工具 | 对该知识库中的实际内容有效，不直接修改 `kb-design` |
| 受管理表示 | `KB/`、`App/Templates/`、`App/Views/`、`App/Rules/`、`App/manifest.json` | 未来的 `kb-design` 生成器 | 是正式设计与数据的应用表示，不是正式编辑源 |
| 派生报告 | `App/Reports/` | 未来的内容校验器和报告生成器 | 只保存可重算事实与复核线索，可以删除和重建 |
| 应用配置 | `.obsidian/` | 初始化器给出最低基线，其余由使用者维护 | 不修改模型、正式数据或项目决定 |

受管理表示和派生报告在文件系统与 Obsidian 中可以编辑。对它们的修改不回流、不取得项目效力；受管理文件的变化只形成 manifest 漂移，派生报告不作为下一次结论的输入。用户文件不属于受管理写集，生成器不得覆盖、移动或删除。

## 文件布局

完整应用使用一个不嵌套的 vault，目录只区分稳定职责，不复制主题分类树。

```text
Home.md
Inbox/
Sources/
  Clippings/
  References/
  Files/
Content/
Indexes/
Attachments/
KB/
  Topics/
  Arrays/
  Entities/
  Sources/
  Types/
  Genres/
  Forms/
App/
  Templates/
  Views/
  Reports/
  Rules/
  manifest.json
.obsidian/
```

`Home.md` 由初始化器提供起始内容，链接到 Inbox、外部资料、全部内容、草稿入口、最近修改、常用用户索引、正式对象入口和维护报告；初始化后归使用者所有，不再由更新器覆盖。

`Inbox/` 保存尚未完成对象判断的临时文件。`Sources/Clippings/` 保存网页剪藏，`Sources/References/` 保存使用者对外部资料的阅读说明，`Sources/Files/` 保存 PDF 等原始文件。`Content/` 保存内容单元，默认不按主题、实体、类型、体裁、状态或层级建立子目录。`Indexes/` 保存个人导航壳。`Attachments/` 是用户文件引用的附件位置，不赋予附件内容单元或正式实体身份。

`KB/` 保存六份正式词表的受管理表示。`App/Templates/` 保存受管理结构片段。`App/Views/` 保存 Base 与固定查询入口，至少提供全部内容、draft 内容、active 内容、deprecated 内容、按主题、按实体、按类型与体裁、最近修改、全部正式主题、unassigned 主题、正式实体、正式来源用途和维护报告入口。`App/Reports/` 保存诊断和统计，`App/Rules/` 保存面向使用者的应用规则说明，`App/manifest.json` 保存完整应用受管理写集的项目清单。`.obsidian/` 只保存最低运行配置和用户后续配置。

完整应用布局尚未实现。现行参考导出仍保持本文后部规定的独立输出布局、根 `manifest.json` 和 `KB/Views/`；在新 vault 初始化器完成前，不把两种布局混称为已经集成。

## 对象边界

| 对象 | 所在位置 | 取得身份的条件 | 不取得的效力 |
|---|---|---|---|
| 临时文件 | `Inbox/` | 无；只要能保存捕获上下文 | 不属于内容模型，不参与正式计数 |
| 外部资料 | `Sources/` | 保存实际材料或阅读说明 | 不是内容单元、正式来源用途或正式实体 |
| 内容单元 | `Content/` | 用户执行建立动作，取得 identifier 并满足必填字段 | 不因文件存在自动成为 `active` |
| 用户索引 | `Indexes/` | 用户选择、排列和解释链接 | 不是主题、数组、概念组或正式关系 |
| 正式表示 | `KB/` 与受管理应用文件 | 从正式编辑源生成并通过 manifest 校验 | 不是正式编辑源，编辑不回流 |
| 派生报告 | `App/Reports/` | 从本次通过校验的输入重算 | 不是正式数据、决定或自动动作 |

Inbox 文件可以丢弃、合并、移入 `Sources/`，或经人工判断建立为内容单元。Inbox 中的字符串、Wikilink、tag 和语言模型输出只作上下文；它们不建立项目对象。

外部资料必须区分原文摘录和使用者批注。Web Clipper 与人工复制保存的标题、作者、发布日期、捕获日期、URL 和正文只描述捕获事实，不构成 designation、概念对应、来源资格或引用批准。能独立复用的理解另建内容单元；需要进入内容字段的文献或标准，必须先取得现行正式实体身份。

`Content/` 中每个 Markdown 文件恰好表示一个内容单元。一级标题保存 `title`，frontmatter 保存 Obsidian binding，正文保存内容。内容文件、标题、alias 和显示文本都不能反推身份。

`Indexes/` 只保存入口说明、阅读顺序、普通链接和嵌入视图。若索引包含可独立引用并需要受控标引的实质说明，正文必须建立为 `Content/` 内容单元并使用适用的 `form: index`；`Indexes/` 只链接该内容单元或嵌入其视图，不保存第二份正文。

## 内容流程

捕获只要求保留上下文，不要求立即完成正式判断。

```text
想法、链接、网页、书籍、PDF
              |
              v
           Inbox/
              |
         人工判断去向
       /       |       \
    丢弃    Sources/   Content/
               |          ^
               +----------+
                理解与转述
```

Obsidian URI、Unique note creator 和普通新建命令只能作为 Inbox 捕获入口。Web Clipper 默认只写 `Sources/Clippings/`，可以创建或追加资料文件，但不能直接创建内容单元、正式实体、正式来源用途或词表记录。

### 内容建立

内容建立必须通过受管理模板配合建立器，或具备同等约束的工具完成。Templates 只能插入片段和日期，不能分配合法 identifier、校验受控值或保证必填性。建立器在写文件前必须取得或验证 identifier，确认目标路径不存在，让使用者选择恰好一个 `type`、恰好一个 `genre` 和至少一个非 deprecated `subject`，写入 `title`、`created` 与 `status: draft`，再回读并运行单文件校验。无法判断必填值时，材料继续留在 Inbox。

identifier 发放规则尚未决定，因此正式内容建立当前不能实施，也不能宣称已完成。该门禁不妨碍 Inbox、外部资料、词表表示和只读内容校验的后续实现。

### 内容状态

`draft` 表示尚未完成。转为 `active` 前，内容必须能够独立引用，所有必填字段和基数正确，受控引用命中正确对象种类，`subject` 不指向 deprecated 主题，内容间 `relation` 满足互反条件，外部材料与使用者陈述能够区分，并由使用者明确批准状态变化。校验器只判断机械条件，不能代替内容判断和批准。

`active` 内容因直接替代或确认过时转为 `deprecated`。直接替代且存在替代项时填写 `isReplacedBy`；确认过时且没有替代项时留空，并在正文首段说明原因。deprecated 内容保留原 identifier 和路径，不移入 Archive，也不删除。

唯一删除例外是误建且没有任何引用的内容单元。删除须按[内容模型](../content-model.md)的现行处置决定和[治理](../governance.md)的决策权执行；报告和校验器不能自动删除。

## 身份门禁

内容路径设计为 `Content/<identifier>.md`，引用按稳定 identifier 计算目标，标题变化不改 identifier 或路径。但是现行内容模型尚未回答任意内容在没有获准英文 label、来源代码或编号时怎样发放 identifier。

[标识符](../../concepts/content-identifiers.md)已经区分身份、名称、标题、路径、排序信息和时间信息；具体采用规则仍等待项目决定。本 target 不选择名称翻译、拼音、时间戳、UUID、对象前缀或其他现行形式，也不从 Unique note creator、文件名、标题或语言模型输出静默取得身份。决定批准前，内容建立流程保持未实现。

## 字段约束

词表矩阵逐个记录 source identity、必填性与基数、literal／reference、datatype 或受控值、target location／property、缺省与省略、loss 保存位置和可逆性。内容矩阵在相同语义边界上另记录建立条件、编辑条件、查询用途和无效表现。

词表对象只写非空 properties；`None`、空字符串和空列表省略。当前词表表示使用 Text、List、Date 和 Tags。相同 property name 在一个 vault 中必须保持同一 Obsidian type。引用单值使用 Text link，引用多值使用由 Text link 组成的 List，日期使用 Date，其他 scalar 使用 Text。

## Obsidian 表示

对象文件使用 UTF-8 Markdown。一级标题保存显示标签或标题；YAML frontmatter 保存可平坦表达并用于查询的 properties；范围、形式依据、归属依据、外部映射和历史记录进入正文。property 中的 Wikilink 整体按 YAML 字符串保存。

Obsidian 当前不支持在应用内查看和编辑 nested properties。本 target 不为正式对象选择 nested properties，列表元素也只使用 scalar；不能平坦表达的结构进入正文表格或 YAML 代码块。`.base` 文件使用 YAML 保存 filters 和 views。项目 manifest 的 `.json` 只服务项目校验，不是 Obsidian 内容对象。

tag 不承担主题、实体、文档类型、体裁、生命周期或正式关系。固定应用 tag 只能区分系统对象或视图范围，不能替代受控字段。

## 词表表示

现行词表表示完整保留。`kb_creator`、`kb_broader`、`kb_related`、`kb_arrays`、`kb_subjects`、`kb_members` 和 `kb_roles` 是 List；`kb_added` 与 `kb_checked` 是 Date；其余专有 properties 是 Text。下列矩阵不改变六份正式 YAML 的字段、值域或 requiredness；“无；未实现回流”表示没有反向写回正式 source 的接口，不能据表示看似无损就推导可逆。

### 文档字段

| 源身份 | 必填与基数 | 值形态 | 类型与值域 | 目标落点 | 缺省处理 | 信息保存 | 可逆性 |
|---|---|---|---|---|---|---|---|
| 六份正式文件的 `version` | 每份文件必填，恰好一个 mapping | record container，不适用 literal／reference | 只允许且必须包含 `id`、`date`、`note` | 无整体 target field；三个子字段按下列行处理 | 无；缺失或多余字段阻断导出 | mapping 结构不整体复制；子字段的保存边界见下列行 | 无；未实现回流 |
| 六份正式文件的 `version.id` | 每份文件必填，恰好一个 | literal | 非空 Text，正式词表版本 ID | 每篇对象笔记的 `kb_version`；`manifest.json` 的对应 `inputs[].version` | 无；缺失阻断导出 | 值逐字保存 | 无；未实现回流 |
| 六份正式文件的 `version.date` | 每份文件必填，恰好一个 | literal | Date | 无独立 target field；对应正式输入 bytes 的 SHA-256 进入 `manifest.json` | 无；缺失阻断导出 | 日期不在生成内容中单独呈现；输入 hash 只能发现 bytes 变化，不能恢复日期 | 无；未实现回流 |
| 六份正式文件的 `version.note` | 每份文件必填，恰好一个 | literal | 非空 Text | 无独立 target field；对应正式输入 bytes 的 SHA-256 进入 `manifest.json` | 无；缺失阻断导出 | 说明不在生成内容中单独呈现；输入 hash 只能发现 bytes 变化，不能恢复说明 | 无；未实现回流 |
| `topics.yaml` 的 `arrays`／`concepts`、`entities.yaml` 的 `entities`、`sources.yaml` 的 `sources`、`types.yaml` 的 `types`、`genres.yaml` 的 `genres`、`forms.yaml` 的 `arrays`／`forms` | 顶层 collection 必填，各为一个列表，记录数为零个或多个 | record container，不适用 literal／reference | 只接受对应 collection 的现行记录结构 | 生成对象笔记的 collection 身份产生 `kb_object` 和 `tags: kb-design/<object>`；载体数组只进入 README；生成对象数进入 manifest | 无 fallback；缺少 collection 阻断导出 | 记录内容按下列逐字段规则保存；collection 顺序不改变对象路径，主题记录顺序另用于派生数组成员顺序 | 无；未实现回流 |

### 公共字段

| 源身份 | 必填与基数 | 值形态 | 类型与值域 | 目标落点 | 缺省处理 | 信息保存 | 可逆性 |
|---|---|---|---|---|---|---|---|
| `concepts`、topic `arrays`、`entities`、`sources`、`types`、`genres`、`forms` 的 collection membership | 每个生成对象恰有一个；不是独立 source field | generated literal | `topic`、`array`、`entity`、`source`、`type`、`genre` 或 `form` | `kb_object` Text；`tags` Tags 固定为 `kb-design/<object>` | 无 fallback；由 collection 唯一确定；载体数组不生成这两个 properties | 保存对象类与固定浏览 tag，不改写 source | 无；未实现回流 |
| `topics.yaml concepts[].id`、`topics.yaml arrays[].id`、`entities.yaml entities[].id`、`sources.yaml sources[].id`、`types.yaml types[].id`、`genres.yaml genres[].id`、`forms.yaml forms[].id`、`forms.yaml arrays[].id` | 每条记录必填，恰好一个 | literal identity | 小写 ASCII 字母、数字和连字符组成的稳定 ID；collection 内唯一 | 主题、主题数组、实体、来源用途、类型、体裁和载体进入 `kb_id` Text 及文件布局规定的 `<id>.md` 路径；载体数组只进入根 README | 无 fallback；非法、重复或缺失阻断导出。主题数组和来源用途没有 `label` 时，`kb_label`、一级标题固定回退到 ID | ID 逐字保存；路径由 ID 和对象类确定 | 无；未实现回流 |
| `concepts[].label`、`entities[].label`、`types[].label`、`genres[].label`、`forms[].label` | 各记录必填一个非空语言 mapping；`zh`、`en` 各至多一个 literal | literal | `zh`／`en` Text，不新增语言或翻译 | 显示值进入一级标题与 `kb_label`；其余非空形式进入 `aliases` | 显示值固定取 `zh`，再取 `en`，最后取 ID；前两项都无值时由 ID 回退 | 所有非空形式保存在标题、`kb_label` 或 `aliases`；非显示形式的语言键和原 mapping 结构不保留 | 无；未实现回流 |
| `concepts[].alt`、`entities[].alt`、`types[].alt`、`genres[].alt`、`forms[].alt` | 可选，一个语言 mapping；每种语言为一个 literal 或零个以上 literal 的列表 | literal | `zh`／`en` Text 或 Text list | 非空形式进入 `aliases`，并进入正文“替代形式”表 | 无 fallback；字段或空值省略 | 正文逐项保留语言、顺序、形式和重复次数；`aliases` 去重；source 的 scalar／list 形状和空列表不保留 | 无；未实现回流 |
| `concepts[].hidden`、`entities[].hidden`、`types[].hidden`、`genres[].hidden`、`forms[].hidden` | 可选，一个语言 mapping；每种语言为一个 literal 或零个以上 literal 的列表 | literal | `zh`／`en` Text 或 Text list | 非空形式进入 `aliases`，并进入正文“隐藏形式”表 | 无 fallback；字段或空值省略 | 正文逐项保留语言、顺序、形式和重复次数；`aliases` 不保留 hidden 角色且去重；source 的 scalar／list 形状和空列表不保留 | 无；未实现回流 |
| `concepts[].basis`、`forms[].basis`；可选的 `entities[].basis`、`types[].basis`、`genres[].basis` | 主题与载体必填一个 mapping；实体、类型和体裁可选。非实体键为 `zh`、`en`，实体键为 `subjects`；每个值为一个 literal 或零个以上 literal 的列表 | literal | Text 或 Text list；列表可以为空；仍是现行紧凑依据，不是后置共享引用 | 主题、类型、体裁和载体进入正文“形式依据”表；实体进入“归属依据”表 | 必填对象无 fallback；可选对象缺失时整节省略 | 键和值包括空列表都保留在正文表；不取得结构化 reference 或 property 查询能力 | 无；未实现回流 |
| `concepts[].scope`、`entities[].scope`、`types[].scope`、`genres[].scope`、`forms[].scope` | 类型、体裁、载体必填恰好一个；主题、实体可选零个或一个 | literal | 非空 Text | 正文“范围”节 | 无 fallback；可选缺失时整节省略 | 文本值保留；不进入 property | 无；未实现回流 |
| `concepts[].match[]`、`entities[].match[]`、`types[].match[]`、`genres[].match[]`、`forms[].match[]` | 类型、体裁、载体必填一个列表；主题、实体可选；每项恰有 `source`、`id`、`rel` | `source` 是来源用途 reference；`id`、`rel` 是 literal | `source` 必须命中正式来源用途；`rel` 取现行五种 SKOS mapping relation；`id` 为非空 Text | 正文“外部映射”表的 `source`、`id`、`rel` 三列 | 必填列表无 fallback；可选缺失时整节省略；不自动补 `closeMatch` | 三个值及行序保留；来源 reference 在正文中只保存 ID，不转为 Wikilink | 无；未实现回流 |
| `concepts[].status`、`entities[].status`、`types[].status`、`genres[].status`、`forms[].status` | 各记录必填，恰好一个 | controlled literal | Text；值域由相应正式词表的现行 lifecycle 规则决定，target 不重定义 | `kb_status` Text | 无；缺失阻断导出 | 值逐字保存 | 无；未实现回流 |
| `concepts[].added`、`entities[].added`、`types[].added`、`genres[].added`、`forms[].added` | 各记录必填，恰好一个 | literal | Date | `kb_added` Date | 无；缺失阻断导出 | 日期逐值保存 | 无；未实现回流 |
| 可选的 `concepts[].history`、`entities[].history`、`types[].history`、`genres[].history`、`forms[].history` | 零个或一个列表；每项为 mapping | literal record | YAML list of mappings；target 不增加事件 schema | 正文“历史记录”YAML 代码块 | 无 fallback；缺失时整节省略 | 值和列表顺序保存为重新序列化的 YAML；source 注释与原排版不保留 | 无；未实现回流 |

`aliases` 只消费正式数据中已经存在的形式，不翻译、不补名、不规范化出新形式。选择 alias 建立链接时，真实目标仍是稳定 ID 对应的文件。

### 主题字段

| 源身份 | 必填与基数 | 值形态 | 类型与值域 | 目标落点 | 缺省处理 | 信息保存 | 可逆性 |
|---|---|---|---|---|---|---|---|
| `vocab/topics.yaml concepts[].broader` | 必填列表，零个或多个 | topic reference | 每个 ID 必须命中正式主题；空列表表示顶层 | `kb_broader` List of Text links，指向 `KB/Topics/<id>.md` | 无 fallback；空列表时 property 省略 | 全部上位和 source 顺序保留，不选择主上位 | 无；未实现回流 |
| `vocab/topics.yaml concepts[].related` | 可选列表，零个或多个 | topic reference | 每个 ID 必须命中正式主题；互反义务仍由主题设计承担 | `kb_related` List of Text links | 无 fallback；缺失或空列表时省略 | 全部关系和顺序保留 | 无；未实现回流 |
| `vocab/topics.yaml concepts[].arrays` | 可选列表，零个或多个 | topic-array reference | 每个 ID 必须命中同文件 `arrays[]` | `kb_arrays` List of Text links，指向 `KB/Arrays/<id>.md` | 无 fallback；缺失或空列表时省略 | 数组归属和顺序保留 | 无；未实现回流 |
| `vocab/topics.yaml concepts[].source` | 可选，零个或一个 | 来源用途 reference；兼容值 `self` 是 literal | 非空 Text；非 `self` 值必须命中正式来源用途 | `kb_source` Text；来源 ID 转为 Sources Wikilink，`self` 原样保存 | 无 fallback；缺失时省略；不得由 target 补 `self` | source ID 或兼容值保存；`self` 不取得实际派生含义 | 无；未实现回流 |
| `vocab/topics.yaml concepts[].replaced_by` | 可选；直接替代的 deprecated 记录按主题 lifecycle 恰好一个 | topic reference | 必须命中正式主题 | `kb_replaced_by` Text link | 无 fallback；非适用记录省略 | 替代目标保存；生命周期理由仍由 `history` 承担 | 无；未实现回流 |

### 数组字段

| 源身份 | 必填与基数 | 值形态 | 类型与值域 | 目标落点 | 缺省处理 | 信息保存 | 可逆性 |
|---|---|---|---|---|---|---|---|
| `vocab/topics.yaml arrays[].superordinate` | 必填，恰好一个 | topic reference | 必须命中正式主题 | `kb_superordinate` Text link | 无；缺失或悬空阻断导出 | 上位 ID 和显示链接保存 | 无；未实现回流 |
| `vocab/topics.yaml arrays[].source` | 必填，恰好一个 | 来源用途 reference | 必须命中正式来源用途 | `kb_source` Text link | 无；缺失或悬空阻断导出 | 来源 ID 和显示链接保存 | 无；未实现回流 |
| `vocab/topics.yaml concepts[].arrays` 的反向成员关系 | 对每个数组确定性派生零个或多个成员；数组记录没有 `members` source field | topic reference | 成员必须是正式主题；顺序取正式主题记录顺序 | `kb_members` List of Text links | 不适用 source fallback；无成员时 property 省略 | 全部派生成员和顺序保存；不制造数组成员 source field | 无；未实现回流 |

主题数组生成 `KB/Arrays/<id>.md`。它没有 `label`、`status` 或 aliases source field：一级标题与 `kb_label` 固定使用 ID，`kb_status` 和 `aliases` 不生成。主题数组只表达树内分组，不取得主题概念、分面或手工概念组的效力。

### 实体字段

| 源身份 | 必填与基数 | 值形态 | 类型与值域 | 目标落点 | 缺省处理 | 信息保存 | 可逆性 |
|---|---|---|---|---|---|---|---|
| `vocab/entities.yaml entities[].kind` | 必填，恰好一个 | controlled literal | Text；只取实体设计登记的 Wikidata 类 slug | `kb_kind` Text | 无；缺失阻断导出 | 值逐字保存 | 无；未实现回流 |
| `vocab/entities.yaml entities[].subjects` | 必填列表，零个或多个 | topic reference | 每个 ID 必须命中正式主题 | `kb_subjects` List of Text links | 无 fallback；空列表时 property 省略 | 全部主题和顺序保留 | 无；未实现回流 |
| `vocab/entities.yaml entities[].vendor` | 可选，零个或一个 | entity reference | 必须命中正式实体 | `kb_vendor` Text link | 无 fallback；缺失时省略 | 目标 ID 和显示链接保存 | 无；未实现回流 |
| `vocab/entities.yaml entities[].creator` | 可选列表，零个或多个 | entity reference | 每个 ID 必须命中正式实体 | `kb_creator` List of Text links | 无 fallback；缺失或空列表时省略 | 全部目标和顺序保留 | 无；未实现回流 |
| `vocab/entities.yaml entities[].replaced_by` | 可选；有替代品的 deprecated 记录至多一个 | entity reference | 必须命中正式实体 | `kb_replaced_by` Text link | 无 fallback；不适用时省略 | 替代目标保存 | 无；未实现回流 |
| `vocab/entities.yaml entities[].form` | 可选，零个或一个 | controlled literal，不是 Forms reference | Text；publication 使用 Wikidata Q 号或 slug，其他现行值仍由实体设计约束 | `kb_form` Text | 无 fallback；缺失时省略 | 值逐字保存；不改成载体词表链接 | 无；未实现回流 |
| `vocab/entities.yaml entities[].tier` | `standard`／`publication` 必填，其他 kind 不填 | controlled literal | `de-jure`、`de-facto`、`vendor` 或 `archival` | `kb_tier` Text | 无 fallback；不适用时省略 | 值逐字保存 | 无；未实现回流 |
| `vocab/entities.yaml entities[].version` | 可选，零个或一个 | literal | 非空 Text，来源实体所引版本 | `kb_entity_version` Text | 无 fallback；缺失时省略 | 值逐字保存 | 无；未实现回流 |
| `vocab/entities.yaml entities[].url` | 可选，零个或一个 | literal | 非空 Text，现行标量 URL | `kb_url` Text | 无 fallback；缺失时省略 | 值逐字保存；不升级为结构化地址 | 无；未实现回流 |
| `vocab/entities.yaml entities[].watch` | 可选标量；`de-jure` 来源按实体设计必填 | literal | 非空 Text，现行观察 URL | `kb_watch` Text | 无 fallback；不适用时省略 | 值逐字保存；不证明已经联网探测 | 无；未实现回流 |
| `vocab/entities.yaml entities[].checked` | 可选，零个或一个 | literal | Date | `kb_checked` Date | 无 fallback；缺失时省略 | 日期逐值保存 | 无；未实现回流 |

### 来源字段

| 源身份 | 必填与基数 | 值形态 | 类型与值域 | 目标落点 | 缺省处理 | 信息保存 | 可逆性 |
|---|---|---|---|---|---|---|---|
| `vocab/sources.yaml sources[].entity` | 必填，恰好一个 | entity reference | 必须命中 `kind` 为 `standard` 或 `publication` 的正式实体 | `kb_entity` Text link，指向 `KB/Entities/<id>.md` | 无；缺失或悬空阻断导出 | 实体目标和显示链接保存 | 无；未实现回流 |
| `vocab/sources.yaml sources[].role` | 必填列表；现行记录为一个或多个，现行导出形状允许空列表 | controlled literal | `mapping`、`structure`、`group` 或 `candidate`；互斥与组合条件由来源设计承担 | `kb_roles` List | 无 fallback；字段缺失阻断导出，空列表时 property 省略 | 全部已有角色和顺序保留 | 无；未实现回流 |
| `vocab/sources.yaml sources[].checked` | 必填，恰好一个 | literal | Date | `kb_checked` Date | 无；缺失阻断导出 | 日期逐值保存 | 无；未实现回流 |

来源用途生成 `KB/Sources/<id>.md`。它没有 `label`、`status` 或 aliases source field：一级标题与 `kb_label` 固定使用 ID，`kb_status` 和 `aliases` 不生成；正文明确来源用途不等于来源实体身份。

### 类型字段

| 源身份 | 必填与基数 | 值形态 | 类型与值域 | 目标落点 | 缺省处理 | 信息保存 | 可逆性 |
|---|---|---|---|---|---|---|---|
| `vocab/types.yaml types[].broader` | 可选列表，零个或多个 | type reference | 每个 ID 必须命中正式文档类型 | `kb_broader` List of Text links | 无 fallback；缺失或空列表时省略 | 全部上位和顺序保留 | 无；未实现回流 |
| `vocab/types.yaml types[].related` | 可选列表，零个或多个 | type reference | 每个 ID 必须命中正式文档类型 | `kb_related` List of Text links | 无 fallback；缺失或空列表时省略 | 全部关系和顺序保留 | 无；未实现回流 |
| `vocab/types.yaml types[].arrays` | 可选列表，零个或多个 | literal array ID；当前没有类型数组对象 | Text list | `kb_arrays` List，不生成 array link | 无 fallback；缺失或空列表时省略 | ID 和顺序保存；数组语义没有独立 target object | 无；未实现回流 |
| `vocab/types.yaml types[].source` | 可选，零个或一个 | 来源用途 reference | 必须命中正式来源用途 | `kb_source` Text literal，不生成 Wikilink | 无 fallback；缺失时省略 | 来源 ID 保存；reference 的可点击形式不保留 | 无；未实现回流 |
| `vocab/types.yaml types[].replaced_by` | 可选，零个或一个 | type reference | 必须命中正式文档类型 | `kb_replaced_by` Text link | 无 fallback；不适用时省略 | 替代目标保存 | 无；未实现回流 |

### 体裁字段

| 源身份 | 必填与基数 | 值形态 | 类型与值域 | 目标落点 | 缺省处理 | 信息保存 | 可逆性 |
|---|---|---|---|---|---|---|---|
| `vocab/genres.yaml genres[].broader` | 可选列表，零个或多个 | genre reference | 每个 ID 必须命中正式体裁 | `kb_broader` List of Text links | 无 fallback；缺失或空列表时省略 | 全部上位和顺序保留 | 无；未实现回流 |
| `vocab/genres.yaml genres[].related` | 可选列表，零个或多个 | genre reference | 每个 ID 必须命中正式体裁 | `kb_related` List of Text links | 无 fallback；缺失或空列表时省略 | 全部关系和顺序保留 | 无；未实现回流 |
| `vocab/genres.yaml genres[].arrays` | 可选列表，零个或多个 | literal array ID；当前没有体裁数组对象 | Text list | `kb_arrays` List，不生成 array link | 无 fallback；缺失或空列表时省略 | ID 和顺序保存；数组语义没有独立 target object | 无；未实现回流 |
| `vocab/genres.yaml genres[].source` | 可选，零个或一个 | 来源用途 reference | 必须命中正式来源用途 | `kb_source` Text literal，不生成 Wikilink | 无 fallback；缺失时省略 | 来源 ID 保存；reference 的可点击形式不保留 | 无；未实现回流 |
| `vocab/genres.yaml genres[].replaced_by` | 可选，零个或一个 | genre reference | 必须命中正式体裁 | `kb_replaced_by` Text link | 无 fallback；不适用时省略 | 替代目标保存 | 无；未实现回流 |

### 载体字段

| 源身份 | 必填与基数 | 值形态 | 类型与值域 | 目标落点 | 缺省处理 | 信息保存 | 可逆性 |
|---|---|---|---|---|---|---|---|
| `vocab/forms.yaml forms[].broader` | 可选列表，零个或多个 | form reference | 每个 ID 必须命中正式载体 | `kb_broader` List of Text links | 无 fallback；缺失或空列表时省略 | 全部上位和顺序保留 | 无；未实现回流 |
| `vocab/forms.yaml forms[].related` | 可选列表，零个或多个 | form reference | 每个 ID 必须命中正式载体 | `kb_related` List of Text links | 无 fallback；缺失或空列表时省略 | 全部关系和顺序保留 | 无；未实现回流 |
| `vocab/forms.yaml forms[].arrays` | 必填列表；现行记录各有一个，现行导出形状允许零个或多个 | form-array reference | 每个已有 ID 必须命中同文件 `arrays[]` | `kb_arrays` List of literal IDs；不生成 array link | 无 fallback；字段缺失阻断导出，空列表时 property 省略 | 全部已有数组 ID 和顺序保留 | 无；未实现回流 |
| `vocab/forms.yaml forms[].source` | 可选，零个或一个 | 来源用途 reference | 必须命中正式来源用途 | `kb_source` Text literal，不生成 Wikilink | 无 fallback；缺失时省略 | 来源 ID 保存；reference 的可点击形式不保留 | 无；未实现回流 |
| `vocab/forms.yaml forms[].replaced_by` | 可选，零个或一个 | form reference | 必须命中正式载体 | `kb_replaced_by` Text link | 无 fallback；不适用时省略 | 替代目标保存 | 无；未实现回流 |
| `vocab/forms.yaml arrays[].id` | 必填，恰好一个 | literal identity | 稳定 ID；collection 内唯一 | 导出根 README 的“载体数组”表 | 无；缺失或重复阻断导出 | ID 逐字保存；不生成第八类对象笔记 | 无；未实现回流 |
| `vocab/forms.yaml arrays[].superordinate` | 必填，恰好一个 | controlled literal | 固定为 `forms` | 导出根 README 的“载体数组”表 | 无；其他值阻断导出 | 值逐字保存 | 无；未实现回流 |
| `vocab/forms.yaml arrays[].source` | 必填，恰好一个 | 来源用途 reference | 必须命中正式来源用途 | 导出根 README 的“载体数组”表，以 literal ID 保存 | 无；缺失或悬空阻断导出 | 来源 ID 保存；不生成 Wikilink | 无；未实现回流 |

`forms.yaml` 的载体数组不生成另一类对象笔记。根 README 保存其 ID、上位根和来源，每篇载体笔记保存已有数组 ID；该表示保留正式值，不制造第八种对象。

## 内容表示

内容字段已经设计但尚未实现。下表保留[内容模型](../content-model.md)的 16 个字段、基数和值域，并规定未来内容应用的创建、编辑、查询和失败行为。表中路径与 properties 是 target binding，不是 identifier 发放规则，也不是运行证据。

### 内容字段

| 源字段 | 必填与基数 | 值形态与值域 | 目标落点 | 创建条件 | 编辑条件 | 查询用途 | 无效表现与 loss |
|---|---|---|---|---|---|---|---|
| `identifier` | 必填，恰好一个 | literal identity；稳定 ID，具体发放规则待决定 | `kb_id` Text；`Content/<identifier>.md` | 只有发放决定批准且值在内容语境唯一时才能建立 | 一经引用不修改；标题变化不改值或路径 | 精确定位内容与解析 content-unit reference | 缺失、重复或路径冲突阻断建立；不从标题、文件名、alias 或时间回填；回流未实现 |
| `title` | 必填，恰好一个 | Text | 一级标题；需要 Base 查询时同时保存 `title` Text | 建立时由使用者给出 | 可修正显示标题，不改 identifier | 显示、全文检索和可选 Base 排序 | 缺失无效；一级标题与 property 不一致时报告；不从文件名回填；回流未实现 |
| `type` | 必填，恰好一个 | type reference；命中正式文档类型词表 | `kb_type` Text link，指向 `KB/Types/<id>.md` | 建立前由使用者选择一个 | 改值须重新校验引用与内容用途 | 按文档类型筛选与统计 | 缺失、多值、悬空或对象种类错误时无效；完整 reference 尚未实现 |
| `genre` | 必填，恰好一个 | genre reference；命中正式体裁词表 | `kb_genre` Text link，指向 `KB/Genres/<id>.md` | 建立前由使用者选择一个 | 改值须重新校验作者立场 | 按体裁筛选与统计 | 缺失、多值、悬空或对象种类错误时无效；完整 reference 尚未实现 |
| `form` | 可选，零个或一个；长文不填 | form reference；命中正式载体词表 | `kb_form` Text link，指向 `KB/Forms/<id>.md` | 只有内容采用该载体时填写 | 载体改变时可修改或省略 | 按载体筛选 | 多值、悬空或对象种类错误时无效；省略不产生替代值；回流未实现 |
| `level` | 可选，零个或一个 | controlled literal；`remember`、`understand`、`apply`、`analyze`、`evaluate` 或 `create` | `kb_level` Text | 建立时可由作者评估 | 理解深度改变时可修改 | 按认知层级筛选 | 多值或域外值无效；缺失时省略；回流未实现 |
| `subject` | 必填，一个或多个 | topic reference；命中非 deprecated 正式主题 | `kb_subjects` List of Text links，指向 `KB/Topics/<id>.md` | 建立前至少选择一个 | 内容主题改变时人工修改并重新校验 | 正式主题直接计数、主题入口和 Base 筛选 | 空列表、悬空、对象种类错误或 deprecated 目标使内容无效；顺序与全部目标须保存；回流未实现 |
| `entities` | 可选，零个或多个 | entity reference；命中正式实体 | `kb_entities` List of Text links，指向 `KB/Entities/<id>.md` | 内容涉及正式实体时填写 | 涉及对象改变时人工修改 | 实体涉及计数与实体入口 | 悬空或对象种类错误时无效；缺失或空列表省略；全部目标与顺序须保存；回流未实现 |
| `source` | 可选，零个或一个 | content-unit 或 entity reference；必须识别目标种类 | `kb_source` Text link；内容指向 `Content/<id>.md`，实体指向 `KB/Entities/<id>.md` | 内容实际派生自一个内容单元或实体时填写 | 派生判断改变时人工修改，不用 `references` 或旧 `origin` 替代 | 分开查询内容派生与实体派生 | 多值、悬空或对象种类错误时无效；目标种类必须保留；回流未实现 |
| `references` | 可选，零个或多个 | entity reference；命中作为文献或标准的正式实体 | `kb_references` List of Text links，指向 `KB/Entities/<id>.md` | 内容引用已取得正式实体身份的文献或标准时填写 | 引用变化时人工修改，不从 `entities` 推导 | 正式引用计数与参考资料入口 | 悬空、对象种类或实体 kind 错误时无效；缺失或空列表省略；回流未实现 |
| `created` | 必填，恰好一个 | ISO 8601 Date | `kb_created` Date | 建立内容单元时写入 | 不随普通编辑改变 | 按建立日期排序和筛选 | 缺失、格式错误或多值无效；不从文件时间回填；回流未实现 |
| `modified` | 可选，零个或一个 | ISO 8601 Date | `kb_modified` Date | 建立时可以省略 | 内容发生受记录的修改时更新 | 最近修改视图 | 格式错误或多值无效；缺失时省略，不从文件时间回填；回流未实现 |
| `status` | 必填，恰好一个 | controlled literal；`draft`、`active` 或 `deprecated` | `kb_status` Text | 新建固定为 `draft` | 只有通过适用校验并经使用者批准才能转换 | 草稿、在用和废弃内容视图 | 缺失、多值、域外值或不合法转换无效；校验器不自动降级或升级；回流未实现 |
| `isReplacedBy` | 因直接替代而 deprecated 且有替代项时必填一个；其他情况零个 | content-unit reference | `kb_is_replaced_by` Text link，指向 `Content/<id>.md` | 新建 draft 不填 | 直接替代并转为 deprecated 时填写；无替代过时时省略并在正文首段说明 | 沿替代链导航 | 条件必填时缺失、目标悬空或对象种类错误时无效；回流未实现 |
| `relation` | 可选，零个或多个 | content-unit reference；满足内容模型的使用条件并互反 | `kb_relation` List of Text links，指向 `Content/<id>.md` | 仅在主题不同且常被一起阅读时填写 | 任一端改变时同时复核两端 | 查询正式内容间 relation | 悬空、对象种类错误或不互反时报告无效；不从正文链接或 Backlinks 推导；回流未实现 |
| `language` | 可选，零个或一个 | Text；默认 `zh` | `kb_language` Text | 默认语言为 `zh` 时可省略，其他值填写 | 主要语言改变时修改 | 按语言筛选 | 多值无效；省略只表示既定默认 `zh`；不另立 target 值域；回流未实现 |

正文位于 frontmatter 后，使用 Markdown，可为空；它不是 metadata property，也不从 `description` 生成。正文允许范围和安全校验尚待内容实现，但正文中的 Wikilink、tag、字符串和 unlinked mention 都不替代上述字段。

## 引用语法

所有引用都以目标稳定 ID 计算路径，以当前标题或正式 label 计算显示文本。

```md
[[Content/<identifier>|内容标题]]
[[KB/Topics/security|安全]]
[[KB/Entities/obsidian|Obsidian]]
```

显示文本缺少中文时使用英文，两者都缺少时使用 ID。显示文本不参与目标解析。property 中的链接整体按 YAML 字符串保存，Text 和 List property 中的内部链接加引号。正式对象引用必须解析到正确种类的生成目标；内容引用必须解析到内容单元。本 target 不使用标题引用或块引用承担身份。

## 导航分工

| 入口 | 回答的问题 | 不能承担 |
|---|---|---|
| 正式主题树 | 正式知识范围、上位、下位、相关、数组、状态和依据是什么 | 用户阅读顺序、自动补主题或内容目录分类 |
| 用户索引 | 使用者怎样理解、选择和进入一组内容 | `broader`、`related`、数组、分面或概念组效力 |
| Bases | 哪些文件满足已声明的 property 条件，怎样排序与浏览 | 只读权限、正式审批、编辑源或回流 |
| Search | 正文、路径、tag 或 property 当前匹配什么 | 可审计的查询事件和未匹配查询统计 |
| Backlinks | 哪些文件链接或提及当前文件 | 正式引用计数、relation 或概念判断 |
| Graph | 现有内部链接形成什么文件网络 | 正式主题结构、关系证明或盲区计量 |

`Home.md` 是全库入口；Bookmarks 可以固定 Home、Inbox、常用索引、草稿视图和维护报告，但只是个人快捷入口。`App/Views/` 的基线使用 Obsidian Bases，不把 Dataview 或其他社区插件作为必要条件。Base 可以编辑文件及 properties，因此受管理 Base 只表示生成权和项目效力，不表示 UI 权限。

### 主题入口

主题入口同时显示上位、下位、相关、数组、scope、依据、状态、外部映射、直接使用该主题的内容列表和仅作统计的下位分支聚合计数。`unassigned` 和零引用主题继续可见。分支聚合不能给内容增加更宽的 `subject`，也不能改变主题引用语义或状态。

实体入口分开显示 `kb_entities`、`kb_references` 和适用的 `kb_source` 所形成的内容列表。正文提及、Backlinks 和普通链接不能与这些正式字段合并成一种关系。

## 正式主题

应用必须完整呈现已借入的知识体系。`status: unassigned` 的正式主题即使没有内容也必须保留和浏览；应用不得隐藏空分支、删除零引用主题或用已有内容反向裁剪正式结构。

对应视图至少显示主题 ID、label、上位、来源、状态、直接内容数和分支聚合内容数。视图只呈现事实，不把 `unassigned` 自动改为 `active`。

## 内容与检索

实际写作和检索中，报告需要呈现无法选择合适正式主题、正文反复出现未登记字符串、宽主题吸收过多内容、内容集中在正式结构的小部分、同一实体或来源被不一致表示，以及用户索引反复需要正式结构没有稳定入口等现象。

核心 Search 没有提供本项目可审计的 search-event interface，因此不能计算“没有匹配任何概念的检索次数”。近期查询 UI 或 Search 存在不能冒充查询日志。正文未解析字符串只进入 `App/Reports/`，并保留文件、位置和上下文；它是 report-only 线索，不自动创建候选、designation、概念、关系、状态或违规结论。

## 使用计数

正式使用计数只读取 `Content/` 中通过校验的受控字段：

- 主题使用读取 `kb_subjects`；
- 实体涉及读取 `kb_entities`；
- 正式引用读取 `kb_references`；
- 派生来源按目标种类读取 `kb_source`。

主题直接引用计数只计字段中明确出现的该主题。分支聚合计数沿正式下位关系汇总，只服务覆盖观察；它不把上位主题写入内容，也不改变直接计数。

正文 Wikilink、Backlinks、用户索引成员、aliases、unlinked mentions 和 Graph edges 都不进入正式计数。它们可以提供人工探索线索，不能替代受控字段语义。当前没有真实 `Content/` 或消费者，所有内容计数都未启用。

## 维护反馈

应用只提供单向反馈，不自动回流。

```text
内容与资料
    |
    v
机械校验与统计
    |
    v
App/Reports/ 带上下文线索
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

报告写集只能位于 `App/Reports/` 的本次临时目录和成功发布的报告集合。报告生成器不读取旧报告作为新结论输入，也不能写 `Content/`、`Indexes/`、`KB/`、`App/Templates/`、`App/Views/`、`App/Rules/`、`.obsidian/` 或仓库正式编辑源。

报告命中[维护](../maintenance.md)阈值时，只能提出适用动作并给出位置与上下文。批准、废弃、删除、拆分、合并、找依据、复核来源、注明不覆盖和发版仍按[治理](../governance.md)的决策权执行。报告永远不能修改内容状态、词表状态、概念、关系、designation、来源、决定或发版状态。

## 能力边界

| Obsidian 能力 | 本项目用途 | 不用于 |
|---|---|---|
| File Explorer | 浏览稳定职责目录和文件 | 主题树、多上位、状态或正式关系 |
| Properties | 保存内容 binding 和可查询的平坦事实 | nested formal structures、自动语义判断或完整校验 |
| Properties view | 观察并维护同名 property type 一致性 | 正式 schema、基数、引用种类和生命周期校验 |
| Templates | 插入合法结构片段、标题和日期 | 分配有依据的 ID、选择受控值或保证完整性 |
| Unique note creator | 快速建立 Inbox 临时文件 | 正式内容 identifier 或内容建立 |
| Web Clipper | 把网页正文、URL 和页面变量保存到 `Sources/Clippings/` | 直接建立内容单元、正式实体、术语或来源资格 |
| Internal links | 表达 target reference syntax 和普通阅读链接 | 自动取得项目关系效力或反推身份 |
| Backlinks | 查看 linked／unlinked mentions 和人工上下文 | 正式引用计数、relation 或概念判断 |
| Bases | 查看、排序、筛选和编辑文件及 properties | 权限只读、正式审批、数据源或回流 |
| Search | 查询正文、路径、tag 和 properties | 可审计的未匹配查询日志 |
| Bookmarks | 固定个人常用入口 | 项目导航真值、正式分类或关系 |
| Graph | 探索现有文件链接 | 正式主题树、关系证明或盲区计量 |
| Canvas | 临时整理和讨论 | 正式结构、内容模型、统计输入或编辑源 |

Web Clipper 基线只使用 preset variables；Interpreter 和 prompt variables 默认禁用。它们需要外部模型并带来速度、成本与隐私差异，输出也不取得正式效力。Templates 和 Web Clipper 模板可以创建或追加文件，但文件存在不等于对象合法。

基线不安装社区插件。未来引入插件前，必须说明它解决的真实失败、退出路径、数据位置、对 Markdown 的影响和缺失时的降级行为；普通 Markdown、核心 Base、Search 和报告入口必须继续可用。

## 配置边界

未来初始化器只给出应用运行所需的最低 `.obsidian/` 配置：启用 Properties、Templates、Bases、Search、Backlinks、Bookmarks 和适用的核心能力；把 `App/Templates/` 设为模板目录，把 `Attachments/` 设为附件目录；启用内部链接随 Obsidian 内移动和改名更新；登记项目 property types；提供 excluded files 与 Bookmarks 建议，但不强制覆盖用户选择。

主题、字体、窗口布局、快捷键、移动端布局、Sync、Publish 和个人插件归使用者。`App/manifest.json` 不把这些用户配置变化报告为受管理表示漂移。

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

`scripts/export_obsidian.py` 是完整应用中唯一已经实现的部分。它仍只读取六份正式词表，生成单向参考区；不读取或生成 `Home.md`、`Inbox/`、`Sources/`、`Content/`、`Indexes/`、`Attachments/`、`App/` 或 `.obsidian/`，也不提供内容建立、校验、统计或回流。

### 现行布局

现行独立输出布局保持不变。

```text
README.md
manifest.json
KB/
  Topics/
  Arrays/
  Entities/
  Sources/
  Types/
  Genres/
  Forms/
  Views/
    Topics.base
    Entities.base
    Sources.base
```

对象文件名为 `<id>.md`。标签、别名和译名变化不改路径。内部链接从输出根开始并使用正斜线。普通 `.json` 不在 Obsidian accepted content formats 中；根 `manifest.json` 是现行导出的项目清单，不是内容对象，也不是未来完整 vault 的 `App/manifest.json` 已实现证据。

### 浏览入口

现行导出生成 Topics、Entities 和 Sources 三个 `.base` 文件。每个 Base 用 `file.inFolder()` 和 Markdown 扩展名收窄默认数据集，并提供 table view；不使用 formulas、Backlinks 聚合、插件视图或自动写回动作。

Base 是可编辑界面。经 Base 修改对象笔记与直接编辑 Markdown 一样，不回流、不取得项目效力，并可能在再次导出时被覆盖。当前验收只证明 `.base` 按现行规则产生并可解析为 YAML，没有 Obsidian 应用内交互证据。

### 表达缺口

正式记录中的 `basis`、`match` 和 `history` 含嵌套结构，因此进入正文表格或 YAML 代码块；`scope`、替代形式和隐藏形式也进入正文。该 loss 只发生在可查询 property 结构上，信息本身仍写入生成笔记。

`basis` 的 list 值允许为空，空列表仍保存在正文依据表。`alt` 和 `hidden` 的正文表逐行保留语言、顺序、形式与重复次数；`aliases` 汇集非显示形式并去重，因此不保留重复次数，且不保留 hidden 角色。source 的 scalar／list 形状和空列表也不能从 aliases 恢复。

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

正式对象的输出标识是稳定 ID；README 与 Base 使用文件 stem 作为 manifest 内部标识。manifest 不保存生成时间、绝对路径、用户名、输出目录或 mtime，也不把自身列入文件条目和内容集合 hash。

项目 manifest 的双向文件覆盖和 checksum 只证明当前目录中的已列 bytes 与记录一致。输出没有 `bagit.txt`、`data/`、payload manifest 或 tag manifest，不是 BagIt bag，也不宣称 BagIt conformance。checksum 不证明 provenance、真实性、审批、语义正确性、消费者存在、正式激活或可重建性。

### 发布边界

从仓库根运行：

```bash
python3 scripts/export_obsidian.py --repo-root . --output /absolute/new/path
```

输出目录必须不存在或为空。导出器拒绝符号链接、仓库根、文件系统根、用户主目录和仓库中的正式数据、设计、概念、来源、脚本与测试目录；它不提供覆盖非空目录、合并现有 vault 或删除旧目录的参数。

全部文件先写入目标同级的新临时目录，再回读并校验文件集合、逐文件 hash、Markdown frontmatter、Base YAML、内部链接和 manifest 双向覆盖。校验通过后，导出器以 `os.replace()` 尝试把临时目录放到目标目录项；失败时只删除本次创建的临时目录，不递归删除用户目标。

`os.replace()` 成功只提供目标目录项的 atomic visibility。它可能因平台、权限、非空目标或跨文件系统等条件失败；当前实现没有 file 或 directory `fsync`，不提供 durability、掉电恢复、多文件事务、并发协调或内容正确性保证。

成功时标准输出是一行排序 JSON，只含 `output`、`content_files`、`total_files` 和 `content_sha256`。参数错误、输入错误或写入错误时，标准错误以 `OBSIDIAN_EXPORT_ERROR` 开头并退出 `1`；`--help` 正常退出 `0`。

导出目录可以作为独立参考 vault，也可以在人工核对项目 manifest 后复制到现有 vault 的管理位置。更新已有参考区时应导出到另一个新目录、核对项目 manifest，再由人决定替换旧目录。该人工路径不是完整应用的非空 vault 自动更新合同。

## 回流边界

当前没有任何回流接口。人工直接或经 Base 修改正式表示中的 properties、正文、aliases、链接、文件名或 `.base`，都不会写回本仓库，也不取得项目效力；现行导出器不读取这些修改。

未来若提出回流，必须另行设计并保存 vault 文件、位置和上下文，读取稳定 `kb_id`，区分用户内容与生成表示，报告差异，把未解析字符串交人工，再分别完成概念、designation、权限和来源判断。它不得从文件名、alias、tag、Wikilink、Backlinks、索引或 Graph 自动创建记录、关系或状态。

报告形成与回流不同。`App/Reports/` 的单向线索只能经人工复核进入 `kb-design` 正式编辑流程；在决定、实现和运行证据齐备前，不存在自动 return interface。

## 验收门禁

- 功能范围、模型引用、字段约束、使用条件和 encoding 与应用无关设计一致，target binding 没有改写字段语义。
- 完整应用的用户文件、受管理表示、派生报告和配置权属分开，受管理写集不覆盖用户内容。
- 每个正式对象恰有一条稳定路径，全部正式引用都有生成目标，全部 `broader` 均被保留。
- properties 可由安全 YAML 解析且只有 scalar 或 scalar list；正文完整保存未进入 properties 的嵌套数据。
- aliases 只来自正式已有形式并去重；`alt` 和 `hidden` 正文仍保留重复行，`basis` 空列表仍可保存。
- 内容矩阵保持 16 个现行字段的字段名、基数和值域；无效 active 与 draft 内容均报告而不改写。
- 正式计数只读取通过校验的 `Content/` 受控字段；普通链接与 Obsidian 探索能力不进入计数。
- 报告写集不能修改用户内容、正式表示、正式编辑源、状态、关系、designation、来源或决定。
- 项目 manifest 与现行导出目录双向一致，并证明生成内容和 manifest 使用同一输入快照。
- 相同输入在同一受控环境中的两个独立导出目录逐字节一致；该证据只支持确定性。
- 非空目标、符号链接、目录替换失败和写后回读失败不损坏用户目标；成功替换只宣称 atomic visibility。
- 能力说明不宣称 DCAP、DCTAP、JCS、BagIt、reproducible build、durability、真实消费者或正式激活。

机械计数和 hash 由导出器、测试及端到端导出证明，不另作低价值重复检查。内容设计只有在真实 vault、内容建立器、内容校验器和消费者实现后，才能验收内容创建、使用统计和报告；回流仍须另立决定。

## 待定事项

- 内容 identifier 的发放方式、唯一语境、形式和碰撞处理等待项目决定；本文不选名称翻译、拼音、时间戳、UUID 或对象前缀。
- 完整新 vault 的初始化、内容建立、内容校验、使用统计、报告和 `App/manifest.json` 尚未实现。
- 可审计查询日志等待真实查询消费者或明确接口；Search UI 不满足该条件。
- 非空 vault 更新、自动回流、自动修复和社区插件增强继续后置。
- 若未来需要 reproducible build 主张，另行界定 specified artifacts、source、environment 和 instructions，并取得 independent rebuild 证据。
- 若未来需要 durability，另行设计 file 与 directory `fsync`、故障模型和恢复验证；不从当前 atomic visibility 推导。
- TBX 只按[未生效草案](../drafts/tbx-export.md)中的真实接收方条件重新进入设计。

## 权威来源

- [内容模型](../content-model.md)：内容单元、16 个字段、基数、值域、生命周期和处置决定。
- [维护](../maintenance.md)：指标、阈值、单向触发、人工动作和消费者门禁。
- [Application Profile](../../concepts/application-profile.md)：功能范围、模型引用、字段约束、使用指南、encoding 和 target binding 的分层。
- [标识符](../../concepts/content-identifiers.md)：身份、名称、标题、路径、排序和时间的边界，以及现行选择未决。
- [Reproducible Builds](../../concepts/reproducible-builds.md)：确定性、独立重建、manifest、JCS、BagIt、atomic visibility 和 durability 的边界。
- [应用约束与表示分层](../decisions/application-profile-boundary.md)：本 target 的已采纳职责、消费者、编辑效力和符合性边界。
- [设计与应用分离](../decisions/form-independence.md)：应用无关模型与 target 分离、正式词表单向导出的现行决定。
- [当前阶段](../decisions/current-stage-scope.md)：设计同步与正式激活的阶段边界。
- [Obsidian 官方帮助阅读笔记](../../sources/obsidian-help.md)：vault、properties、links、aliases、accepted formats、Bases、Search、Backlinks、Graph、Bookmarks、Templates、Unique note creator 和 Web Clipper 的行为。
- [DCMI Application Profiles 阅读笔记](../../sources/dcmi-application-profiles.md)：Application Profile 组件、`metadata crosswalk`、历史材料状态与项目边界。
- [Reproducible Builds 阅读笔记](../../sources/reproducible-builds.md)：确定性与 reproducible build 的证据边界。
- [BagIt 文件包格式阅读笔记](../../sources/rfc-8493.md)：项目 manifest 与 BagIt 的边界。
- [RFC 8785 阅读笔记](../../sources/rfc-8785.md)：现行 JSON 参数与 JCS 条件的差异。
- [Python 文件系统阅读笔记](../../sources/python-filesystem.md)：`os.replace()`、atomic visibility、`fsync` 与 durability 的边界。
