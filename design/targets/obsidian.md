# Obsidian 映射

本文是 Obsidian target 的现行 `Application Profile` 与导出 artifact contract。它按[内容模型](../content-model.md)引用应用无关语义，规定 Obsidian 表示的语义选择，再单独规定所选表示怎样物化为文件。分层依据见 [Application Profile](../../concepts/application-profile.md)、[Reproducible Builds](../../concepts/reproducible-builds.md)、[方法登记](../principles.md)和[应用约束与表示分层](../decisions/application-profile-boundary.md)。

当前实现只把六份正式词表生成成单向词表参考区。内容表示只有未来应用必须遵守的约束；仓库没有知识库内容、内容导出器、内容校验器、检索记录或回流接口。

## 功能范围

当前 `Application Profile` 支持用户浏览、链接和筛选正式词表表示。

- 浏览正式对象的稳定身份、显示形式、状态、关系、范围与依据表示；
- 沿 Wikilink 查看上位、相关、数组成员、实体和来源用途之间的正式引用；
- 通过 Base 按既定 properties 排序和筛选正式词表表示；
- 为未来内容应用规定字段位置、target type、reference form、受控值引用、使用条件和允许的 loss。

未来内容 binding 只规定应用语义。当前没有内容消费者，不生成或读取知识库内容，不执行内容查询、引用统计、未匹配检索统计或回流。

生成文件、确定 file set、写入项目 manifest、post-generation validation 和 publication 不属于本节的应用功能，只由“导出合同”和“发布边界”规定。导入、既有 vault 合并、来源或术语正式激活、TBX，以及 DCAP、DCTAP、JCS、BagIt 或 reproducible build conformance 也不在当前功能范围内。

## 效力边界

- `vocab/topics.yaml`、`vocab/entities.yaml`、`vocab/sources.yaml`、`vocab/types.yaml`、`vocab/genres.yaml` 和 `vocab/forms.yaml` 是导出的正式输入。
- `vocab/topics.yaml` 的编辑路径仍由[主题词表设计](../topics.md)规定；其他正式词表仍按各自设计维护。
- 生成的 Markdown、Base 和 README 可以被 Obsidian 或文件系统工具编辑；项目 manifest 只能由文件系统工具修改。它们都不是正式词表、术语表、迁移账本或新的编辑源。
- 导出器不读取生成目录中的修改。修改不会回流本仓库，不取得 designation、概念、关系、状态或项目决定的效力；再次导出可以覆盖修改。
- 导出器不读取来源与术语迁移账本、候选记录、未激活模式、草案、诊断报告或 Superpowers 过程文件。
- `concepts/glossary.md` 继续承担 designation 与中英对照的现行编辑权；正式术语数据尚未激活。

## 模型引用

本 target 引用[内容模型](../content-model.md)的内容单元、字段语义、受控值、标识符和生命周期，引用[主题词表设计](../topics.md)、[命名实体词表设计](../entities.md)与[来源名称规范表](../sources-registry.md)的正式对象，并引用[层级结构](../hierarchy.md)的多上位和数组规则。

`Application Profile` 只为这些既定对象选择 Obsidian location、type、reference form 和允许的 loss。field／property／path binding 是同一应用内部的表示规则，不是 `metadata crosswalk`；它也不改变词表层 `crosswalk` 对概念映射的现行含义。

target binding 不得修改字段语义、基数、值域、稳定身份、对象关系或正式词表身份。Obsidian 无法直接支持某项约束时，应用保留并校验该约束，或把不能无损进入 property 的信息移到正文；不得通过放宽内容模型、改成自由 tag 或自动建立概念来绕过。

## 字段约束

“词表表示”和“内容表示”的矩阵逐个记录 source identity、必填性与基数、literal／reference、datatype 或受控值、target location／property、缺省与省略、loss 保存位置和可逆性。矩阵中的“无；未实现回流”表示生成表示没有反向写回正式 source 的接口，不能据字段看似无损就推导可逆。

词表对象只写非空 properties；`None`、空字符串和空列表省略。当前词表表示使用 Text、List、Date 和 Tags。若未来选择 Checkbox，YAML 值必须是 `true` 或 `false`；Checkbox 是 Obsidian type，boolean 是其 YAML 值形态。相同 property name 在一个 vault 中必须保持同一 Obsidian type。

## 文件布局

导出目录使用固定路径。

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

对象文件名为 `<id>.md`。标签、别名和译名变化不改路径。内部链接从 vault 根开始并使用正斜线。`manifest.json` 与 Obsidian 文件同目录发布，但普通 `.json` 不在 Obsidian accepted content formats 中；该文件是项目清单，不是 Obsidian 内容对象。

## Obsidian 表示

对象笔记使用 UTF-8 Markdown。一级标题保存显示标签；YAML frontmatter 保存可平坦表达并用于查询的 properties；范围、形式依据、归属依据、外部映射和历史记录进入正文。

Obsidian 当前不支持 nested properties，但 YAML 本身能够保存嵌套结构。本 target 为了应用编辑和查询兼容性，不在 properties 中选择嵌套值；列表元素也只使用 scalar。不能平坦表达的正式结构进入正文表格或 YAML 代码块，内容仍来自正式输入。

`.base` 文件使用 YAML 保存 filters 和 table view。`.md` 与 `.base` 是 Obsidian 支持的内容格式；项目 manifest 的 `.json` 格式只服务导出校验。

## 词表表示

引用单值使用 Text link，引用多值使用由 Text link 组成的 List；日期使用 Date，其他 scalar 使用 Text。`kb_creator`、`kb_broader`、`kb_related`、`kb_arrays`、`kb_subjects`、`kb_members` 和 `kb_roles` 是 List；`kb_added` 与 `kb_checked` 是 Date；其余专有 properties 是 Text。下列矩阵不改变正式 YAML 的字段、值域或 requiredness。

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
| `concepts[].alt`、`entities[].alt`、`types[].alt`、`genres[].alt`、`forms[].alt` | 可选，一个语言 mapping；每种语言为一个 literal 或零个以上 literal 的列表 | literal | `zh`／`en` Text 或 Text list | 非空形式进入 `aliases`，并进入正文“替代形式”表 | 无 fallback；字段或空值省略 | 正文保留语言、顺序和形式；`aliases` 去重；source 的 scalar／list 形状、空列表和重复次数不保留 | 无；未实现回流 |
| `concepts[].hidden`、`entities[].hidden`、`types[].hidden`、`genres[].hidden`、`forms[].hidden` | 可选，一个语言 mapping；每种语言为一个 literal 或零个以上 literal 的列表 | literal | `zh`／`en` Text 或 Text list | 非空形式进入 `aliases`，并进入正文“隐藏形式”表 | 无 fallback；字段或空值省略 | 正文保留语言、顺序和形式；`aliases` 不保留 hidden 角色且去重；source 的 scalar／list 形状、空列表和重复次数不保留 | 无；未实现回流 |
| `concepts[].basis`、`forms[].basis`；可选的 `entities[].basis`、`types[].basis`、`genres[].basis` | 主题与载体必填一个 mapping；实体、类型和体裁可选。非实体键为 `zh`、`en`，实体键为 `subjects`；每个值为一个或多个 literal | literal | 非空 Text 或 Text list；仍是现行紧凑依据，不是后置共享引用 | 主题、类型、体裁和载体进入正文“形式依据”表；实体进入“归属依据”表 | 必填对象无 fallback；可选对象缺失时整节省略 | 键和值保留在正文表；不取得结构化 reference 或 property 查询能力 | 无；未实现回流 |
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

内容单元不由当前导出器生成。下表是未来知识库应用必须遵守的逐字段 binding；每行的 target 均为“未实现”，不得用文件名、标题、alias、tag、反向链接或文件时间替代内容模型字段。

### 内容字段

| 源身份 | 必填与基数 | 值形态 | 类型与值域 | 目标落点 | 缺省处理 | 信息保存 | 可逆性 |
|---|---|---|---|---|---|---|---|
| [内容模型](../content-model.md)的 `identifier` | 必填，恰好一个 | literal identity | 稳定 ID，遵守内容模型的标识符规则 | `kb_id` Text；内容文件路径尚未设计 | 无；缺失无效，不从文件名、标题或 alias 回填 | 未实现；约束要求完整保存稳定 ID | 无；回流未实现 |
| [内容模型](../content-model.md)的 `title` | 必填，恰好一个 | literal | Text | 一级标题；需要查询时同时保存 `title` Text | 无；缺失无效，不从文件名回填 | 未实现；一级标题保存显示值，可选 property 只服务查询 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `type` | 必填，恰好一个 | type reference | 必须命中正式文档类型词表 | `kb_type` Text link，指向 `KB/Types/<id>.md` | 无；缺失或悬空无效 | 未实现；约束要求保存稳定 ID 目标和显示链接 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `genre` | 必填，恰好一个 | genre reference | 必须命中正式体裁词表 | `kb_genre` Text link，指向 `KB/Genres/<id>.md` | 无；缺失或悬空无效 | 未实现；约束要求保存稳定 ID 目标和显示链接 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `form` | 可选，零个或一个；长文不填 | form reference | 必须命中正式载体词表 | `kb_form` Text link，指向 `KB/Forms/<id>.md` | 无 fallback；不适用时省略 | 未实现；有值时要求完整保存 reference | 无；回流未实现 |
| [内容模型](../content-model.md)的 `level` | 可选，零个或一个 | controlled literal | `remember`、`understand`、`apply`、`analyze`、`evaluate` 或 `create` | `kb_level` Text | 无 fallback；缺失时省略 | 未实现；有值时要求逐字保存 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `subject` | 必填，一个或多个 | topic reference | 必须命中非 deprecated 的正式主题 | `kb_subjects` List of Text links，指向 `KB/Topics/<id>.md` | 无；空列表或悬空无效 | 未实现；约束要求保存全部目标和 source 顺序 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `entities` | 可选，零个或多个 | entity reference | 必须命中正式实体 | `kb_entities` List of Text links，指向 `KB/Entities/<id>.md` | 无 fallback；缺失或空列表时省略 | 未实现；有值时要求保存全部目标和顺序 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `source` | 可选，零个或一个 | content-unit 或 entity reference | 必须按内容模型识别目标种类并命中对应对象 | `kb_source` Text link；实体指向 `KB/Entities/<id>.md`，内容路径未实现 | 无 fallback；缺失时省略，不用 `references` 或旧 `origin` 替代 | 未实现；目标种类和内容路径尚无消费者实现，不能宣称无损运行 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `references` | 可选，零个或多个 | entity reference | 必须命中作为文献或标准的正式实体 | `kb_references` List of Text links，指向 `KB/Entities/<id>.md` | 无 fallback；缺失或空列表时省略，不从 `entities` 推导 | 未实现；有值时要求保存全部目标和顺序 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `created` | 必填，恰好一个 | literal | ISO 8601 Date | `kb_created` Date | 无；缺失无效，不从文件时间回填 | 未实现；约束要求逐值保存 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `modified` | 可选，零个或一个 | literal | ISO 8601 Date | `kb_modified` Date | 无 fallback；缺失时省略，不从文件时间回填 | 未实现；有值时要求逐值保存 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `status` | 必填，恰好一个 | controlled literal | `draft`、`active` 或 `deprecated` | `kb_status` Text | 无；缺失无效 | 未实现；约束要求逐字保存 lifecycle 值 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `isReplacedBy` | 因直接替代而 deprecated 且有替代项时必填一个；其他情况零个 | content-unit reference | 必须命中替代内容单元 | `kb_is_replaced_by` Text link；内容路径未实现 | 无 fallback；确认过时且无替代项时省略，并在正文首段说明原因 | 未实现；reference 与无替代理由分别受字段和正文约束 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `relation` | 可选，零个或多个 | content-unit reference | 必须命中内容单元并满足互反和使用条件 | `kb_relation` List of Text links；内容路径未实现 | 无 fallback；缺失或空列表时省略 | 未实现；目标、顺序和互反校验都尚无消费者实现 | 无；回流未实现 |
| [内容模型](../content-model.md)的 `language` | 可选，零个或一个 | literal | Text；当前只规定默认值 `zh`，不另立 target 值域 | `kb_language` Text | 值为 `zh` 时可以省略；其他值原样写入；无其他 fallback | 未实现；省略只表达既定默认 `zh` | 无；回流未实现 |
| [内容模型](../content-model.md)的正文 | 可选，零个或一个 | literal content | Markdown 正文；内容模型不把它改成 metadata property | frontmatter 后的 Markdown 正文 | 无 fallback；没有正文时省略，不从 `description` 生成 | 未实现；正文值、结构和允许的 Markdown 范围尚待真实内容应用验收 | 无；回流未实现 |

未来应用必须校验恰好一个 `type`、恰好一个 `genre`、至少一个 `subject`、全部受控值目标、内容单元引用和 lifecycle 约束。当前没有内容目录、内容生成器、内容校验器或消费者；本矩阵不构成实现、启用、运行、loss 验收或回流证据。

## 引用语法

所有对象引用都以目标稳定 ID 计算路径，以目标正式标签计算显示文本。

```md
[[KB/Topics/security|安全]]
```

显示文本缺少中文时使用英文，两者都缺少时使用 ID。显示文本不参与目标解析。主题层级、相关关系、数组成员、实体关系和来源用途必须解析到已生成目标；悬空引用阻断整个导出。

property 中的链接整体按 YAML 字符串保存。Text 和 List property 中的内部链接加引号。本 target 不使用标题引用或块引用，避免把可变正文位置当作身份。

## 表达缺口

正式记录中的 `basis`、`match` 和 `history` 含嵌套结构，Obsidian 当前不支持把它们作为 nested properties 编辑和查看，因此进入正文表格或 YAML 代码块；`scope`、替代形式和隐藏形式也进入正文。该 loss 只发生在可查询 property 结构上，信息本身仍写入生成笔记；正文不替代正式 YAML 的编辑权。

当前导出器对每类正式记录使用显式允许字段表。遇到未知字段、非法 ID、重复 ID、无法解析的引用、重复输出路径或不能安全序列化的值时，导出失败；它不把未知值放入兜底字段，也不丢弃后继续生成。

内容应用以后遇到 Obsidian 不能表达的约束时，必须在应用校验器中保留约束并阻断无效内容。

## 浏览入口

导出器生成 Topics、Entities 和 Sources 三个 `.base` 文件。每个 Base 用 `file.inFolder()` 和 Markdown 扩展名收窄默认数据集，并提供 table view；当前不使用 formulas、反向链接聚合、插件视图或自动写回动作。

Base 是可编辑界面。Obsidian 可以通过 table view 编辑文件和 properties；本项目只把这些 Base 用作浏览、排序和筛选入口。经 Base 发生的修改与直接编辑 Markdown 一样，不回流本仓库、不取得项目效力，并可能在重新导出时被覆盖。删除或修改 `.base` 文件不改变正式数据，但经 Base 修改对象笔记会改变该份生成目录中的本地文件。

当前验收只证明 `.base` 按现行生成规则产生并可解析为 YAML，没有证明在 Obsidian 应用内完成交互测试。

## 导出合同

导出 artifact contract 从 `Application Profile` 完成语义选择后开始，只负责把已选表示由输入快照确定性物化为 bytes、文件集合和可校验发布物。它不得改变 field 的 target location、type、reference form 或允许的 loss。

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

## 清单边界

`manifest.json` 是项目 manifest，保存：

- schema 名称与版本；
- 六份正式输入的路径、版本和 SHA-256；
- 导出器 bytes 的 SHA-256；
- 各正式对象种类的动态计数；
- 除 manifest 自身外，每个生成文件的相对路径、对象种类、输出标识和 SHA-256；
- 内容文件数、包含 manifest 的总文件数和内容集合 SHA-256。

正式对象的输出标识是稳定 ID；README 与 Base 使用文件 stem 作为 manifest 内部标识。manifest 不保存生成时间、绝对路径、用户名、输出目录或 mtime，也不把自身列入文件条目和内容集合 hash。

项目 manifest 的双向文件覆盖和 checksum 只证明当前目录中的已列 bytes 与记录一致。输出没有 `bagit.txt`、`data/`、payload manifest 或 tag manifest，不是 BagIt bag，也不宣称 BagIt conformance。checksum 不证明 provenance、真实性、审批、语义正确性或可重建性。

## 发布边界

从仓库根运行：

```bash
python3 scripts/export_obsidian.py --repo-root . --output /absolute/new/path
```

输出目录必须不存在或为空。导出器拒绝符号链接、仓库根、文件系统根、用户主目录和仓库中的正式数据、设计、概念、来源、脚本与测试目录；它不提供覆盖非空目录、合并现有 vault 或删除旧目录的参数。

全部文件先写入目标同级的新临时目录，再回读并校验文件集合、逐文件 hash、Markdown frontmatter、Base YAML、内部链接和 manifest 双向覆盖。校验通过后，导出器以 `os.replace()` 尝试把临时目录放到目标目录项；失败时只删除本次创建的临时目录，不递归删除用户目标。

`os.replace()` 成功只提供目标目录项的 atomic visibility：观察者不会看到发布步骤的中间目录项状态。它可能因平台、权限、非空目标或跨文件系统等条件失败；当前实现没有 file 或 directory `fsync`，不提供 durability、掉电恢复、多文件事务、并发协调或内容正确性保证。

成功时标准输出是一行排序 JSON，只含 `output`、`content_files`、`total_files` 和 `content_sha256`。参数错误、输入错误或写入错误时，标准错误以 `OBSIDIAN_EXPORT_ERROR` 开头并退出 `1`；`--help` 正常退出 `0`。

导出目录可以作为独立 vault，也可以在人工核对项目 manifest 后复制到现有 vault 的一个管理目录。更新已有参考区时应导出到另一个新目录、核对项目 manifest，再由人决定替换旧目录。

## 回流边界

当前没有回流接口。人工直接或经 Base 修改导出笔记中的 properties、正文、aliases、链接、文件名或 `.base`，都不会写回本仓库，也不取得项目效力；下次导出不读取这些修改。

未来回流必须另行设计，并至少保存 vault 文件、位置和上下文，读取稳定 `kb_id`，区分用户正文与生成表示，报告差异，把未解析字符串交人工，分别完成概念、designation、权限和来源判断。它不得从文件名、alias、tag、链接或反向链接自动创建记录、关系或状态。

target 文件、内容字段契约、生成目录或 Base 存在都不等于真实内容消费者启用。引用次数和未匹配检索次数必须等待消费者提供可审计的内容与检索记录。

## 验收门禁

本映射保留下列具有独有风险证据的验收。

- `Application Profile` 的功能范围、模型引用、字段约束、使用条件和 encoding 与内容模型一致；target binding 没有改写字段语义。
- 每个正式对象恰有一条稳定路径，全部正式引用都有生成目标，全部 `broader` 均被保留。
- properties 可由安全 YAML 解析且只有 scalar 或 scalar list；正文完整保存未进入 properties 的嵌套数据。
- aliases 只来自正式已有形式，没有新增名称或译名。
- 项目 manifest 与生成目录双向一致，并证明生成内容和 manifest 使用同一输入快照。
- 相同输入在同一受控环境中的两个独立导出目录逐字节一致；该证据只支持确定性。
- 非空目标、符号链接、目录替换失败和写后回读失败不损坏用户目标；成功替换只宣称 atomic visibility。
- 正式词表、术语编辑权、内容模型、草案状态和发版状态不因导出或 Obsidian 编辑改变。
- 能力说明不宣称 DCAP、DCTAP、JCS、BagIt 或 reproducible build conformance。

机械计数和 hash 由导出器、测试及一次端到端导出证明，不另交第二代理重复确认。内容表示只有真实知识库消费者实现后，才能验收内容生成、引用统计和回流。

## 待定事项

- 真实知识库内容目录、文件布局和调用方出现后，实现并校验内容表示、使用指南和消费者接口。
- 只有回流需求出现后，另行设计上下文保存、差异报告、人工判断和权限门禁。
- 若未来需要 reproducible build 主张，另行界定 specified artifacts、source、environment 和 instructions，并取得 independent rebuild 证据。
- 若未来需要 durability，另行设计 file 与 directory `fsync`、故障模型和恢复验证；不从当前原子可见性推导。
- TBX 只按[未生效草案](../drafts/tbx-export.md)中的真实接收方条件重新进入设计。

## 权威来源

- [Application Profile](../../concepts/application-profile.md)：功能范围、模型、字段约束、使用指南、encoding 和 target binding 的分层。
- [Reproducible Builds](../../concepts/reproducible-builds.md)：确定性、独立重建、manifest、JCS、BagIt、原子可见性和 durability 的边界。
- [应用约束与表示分层](../decisions/application-profile-boundary.md)：本 target 的已采纳职责、消费者、编辑效力和符合性边界。
- [设计与应用分离](../decisions/form-independence.md)：应用无关模型与 target 分离、正式词表单向导出的现行决定。
- [Obsidian 官方帮助阅读笔记](../../sources/obsidian-help.md)：vault、properties、Checkbox、nested properties、links、aliases、accepted formats 和 Bases 行为。
- [DCMI Application Profiles 阅读笔记](../../sources/dcmi-application-profiles.md)：Application Profile 组件、`metadata crosswalk`、历史材料状态与项目边界。
- [Reproducible Builds 阅读笔记](../../sources/reproducible-builds.md)：确定性与 reproducible build 的证据边界。
- [BagIt 文件包格式阅读笔记](../../sources/rfc-8493.md)：项目 manifest 与 BagIt 的边界。
- [RFC 8785 阅读笔记](../../sources/rfc-8785.md)：现行 JSON 参数与 JCS 条件的差异。
- [Python 文件系统阅读笔记](../../sources/python-filesystem.md)：`os.replace()`、atomic visibility、`fsync` 与 durability 的边界。
