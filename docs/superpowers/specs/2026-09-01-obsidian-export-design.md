# Obsidian 导出设计 (Obsidian Export Design)

状态：实施规格。本文只定义从当前正式词表到 Obsidian 管理目录的一向导出，不改变内容模型、正式词表、术语编辑权或应用外规则。

## 目标

本设计解决以下问题：

- 当前正式词表怎样成为 Obsidian 中可浏览、可链接、可筛选的参考笔记；
- 稳定 `id`、显示形式、层级、数组、实体和来源怎样映射到文件、properties 与正文；
- Obsidian 无法直接表达的嵌套依据和映射怎样无损呈现；
- 导出怎样确定性重建、发现漂移并避免覆盖用户笔记；
- 当前没有正式术语数据和内容单元数据时，导出边界怎样保持诚实。

Obsidian 官方说明它把笔记保存为 vault 文件夹中的 Markdown 纯文本；Markdown 是主要笔记格式，[Bases](https://obsidian.md/help/Files%2Band%2Bfolders/Accepted%2Bfile%2Bformats)使用 `.base` 文件。因此本设计只生成普通文件，不依赖社区插件或应用数据库。

## 效力边界

- `vocab/` 中六份正式词表和当前正式主题输出是唯一数据源。
- `vocab/topics.yaml` 仍从生成输入和生成器维护；Obsidian 文件不反向编辑它。
- `concepts/glossary.md` 继续承担当前 designation 与中英对照编辑权；正式 `vocab/terms.yaml` 不存在，导出器不读取或创建它。
- 来源与术语迁移账本、未激活 schema、草案、候选诊断和 Superpowers 报告不进入导出数据。
- 本仓库没有知识库内容单元，导出器只生成词表参考区；内容笔记的字段映射只在设计文档中定义，不伪造内容。
- 本设计不导入 Obsidian 文件，不合并用户修改，不提供往返同步，不改变正式数据或发版状态。

## 官方约束

Obsidian properties 保存在文件开头的 YAML 中；同一文件内键唯一，支持文本、列表、数字、布尔值、日期、日期时间和 tags。[Properties](https://obsidian.md/help/properties)当前不支持嵌套 properties，也不渲染 property 内的 Markdown。文本和列表可以保存内部链接，但链接须加引号。

Obsidian 支持 Wikilink 和 Markdown 两种内部链接；文件夹路径从 vault 根开始，官方默认使用更紧凑的 Wikilink。[Internal links](https://obsidian.md/help/links)同时说明块引用是 Obsidian 特有语法。本设计只使用文件链接，不使用块引用，避免把正文位置变成稳定身份。

Obsidian 的 `aliases` 是 YAML 列表，用于同一笔记的缩写、别名和其他语言名称；选择 alias 时，Obsidian 仍生成指向真实文件的链接。[Aliases](https://obsidian.md/help/aliases)因此适合承载已经存在于正式数据中的多语言与替代形式，但不能补出新译名。

Bases 从 Markdown frontmatter 读取 note properties，可以按文件夹和属性筛选、排序和分组；`.base` 文件是 YAML，filter 默认作用于 vault 全部文件。[Bases syntax](https://obsidian.md/help/bases/syntax)允许用 `file.inFolder()` 限定本导出目录。本设计生成最小 table views，不使用公式或插件视图。

## 输出根

命令接收一个不存在或为空的输出目录。该目录本身可以是独立 vault，也可以在人工确认后作为一个管理目录复制进现有 vault。

导出器拒绝以下目标：

- 已存在且非空的目录；
- 仓库根、文件系统根、用户主目录或输出参数解析后的父级；
- 符号链接目标；
- 目标位于正式 `vocab/`、`design/`、`concepts/`、`sources/`、`scripts/` 或 `tests/` 内。

拒绝覆盖让每次导出保持可恢复。更新现有 vault 时，先导出到新目录，验证 manifest 后由人替换旧管理目录；导出器不删除旧目录。

## 文件布局

输出目录使用固定 ASCII 路径。

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

对象文件名固定为 `<id>.md`。标签变化不改路径，Obsidian 自动重命名链接的能力不参与稳定身份。所有内部链接使用 vault 根相对路径，例如 `[[KB/Topics/security|安全]]`。

## 公共属性

每个对象笔记使用以下公共 properties。

| Property | 类型 | 取值 |
|---|---|---|
| `kb_id` | text | 正式稳定 `id` |
| `kb_object` | text | `topic`、`array`、`entity`、`source`、`type`、`genre` 或 `form` |
| `kb_label` | text | `label.zh`、`label.en`、`id` 固定回退得到的正式显示形式 |
| `kb_status` | text | 正式记录有状态时原值；对象没有状态时省略 |
| `kb_version` | text | 来源词表的 `version.id` |
| `aliases` | list | 正式记录已有的非空显示形式，去重后按语言和原顺序排列 |
| `tags` | tags | 只保存 `kb-design/<object>`，不把主题层级复制为 tags |

property 名使用固定前缀，避免与用户已有属性碰撞。不存在的值省略，不写空字符串、空列表或 `null`。

## 主题映射

每个主题概念生成 `KB/Topics/<id>.md`。

| 正式字段 | Obsidian 表达 |
|---|---|
| `id` | `kb_id` 与文件名 |
| `label.zh`／`label.en` | 正文一级标题选择中文，否则英文；其余非空形式进入 `aliases` |
| `alt`／`hidden` | 已存在形式进入 `aliases`，正文按语言列出；不得生成新形式 |
| `status` | `kb_status` |
| `broader` | `kb_broader` list，每项是带引号的主题 Wikilink |
| `related` | `kb_related` list，每项是带引号的主题 Wikilink |
| `arrays` | `kb_arrays` list，每项是带引号的数组 Wikilink |
| `scope` | 正文“范围” |
| `basis` | 正文“形式依据”表；保持语言和值 |
| `source` | `kb_source` text link；只映射当前正式旧值，不重新解释语义 |
| `match` | 正文“外部映射”表，逐项保留 source、id、rel |
| `added` | `kb_added` date |
| `history`／`replaced_by` | 正文历史与 `kb_replaced_by` link（存在时） |

内部链接显示文本只来自目标正式标签；缺中文时使用英文，均缺失时使用 `id`。路径始终由 `id` 计算。

## 数组映射

每个数组生成 `KB/Arrays/<id>.md`。

- `kb_superordinate` 指向上位主题；
- `kb_source` 指向来源记录；
- `kb_members` 是按正式主题文件顺序排列的成员链接；
- 正文说明数组是树内分组，不把它写成概念、分面或手工概念组；
- 当前数组没有独立状态、历史或 designation，不生成对应属性。

## 实体映射

每个实体生成 `KB/Entities/<id>.md`。

| 正式字段 | Obsidian 表达 |
|---|---|
| `kind` | `kb_kind` text |
| `subjects` | `kb_subjects` list，指向主题笔记 |
| `vendor`／`creator`／`replaced_by` | 相应 entity link properties |
| `form` | `kb_form` text，保持当前正式字符串，不推断类别 |
| `tier` | `kb_tier` text |
| `version`、`url`、`watch`、`checked` | 扁平 properties；URL 保持文本 |
| `basis`、`match`、`history` | 正文表格或列表，无损保留当前值 |

实体类别草案、模型分层草案和传播范围草案均未生效；导出器只呈现现行实体字段，不采用草案推荐或创建模型记录。

## 来源映射

每个来源用途记录生成 `KB/Sources/<id>.md`。

- `kb_entity` 指向对应实体笔记；
- `kb_roles` 保存当前正式 `role` 字符串列表；
- `kb_checked` 保存现行日期；
- 正文明确这是来源用途，不是来源实体身份；
- 不把迁移账本中的 `proposed`、未来角色状态或决定写入输出。

## 受控值映射

文档类型、体裁和载体分别生成 Types、Genres、Forms 笔记。公共规则与主题相同；数组和映射按记录实际字段进入 properties 或正文。导出器不把这些值合并到一个枚举文件，避免丢失稳定 ID、范围、数组和映射。

`forms.yaml` 的两个内部数组不计入主题数组对象，也不生成第八类笔记。它们的 `id`、`superordinate` 和 `source` 必须在导出 README 的“载体数组”表完整保存；每个 form 笔记保留正式数组 ID。数组来源须解析到正式来源，`superordinate` 只允许当前受控值集合声明的根 ID，未知值阻断。

## 内容映射

未来内容笔记仍由知识库应用维护，本仓库不生成。映射约定如下。

| 内容模型字段 | Obsidian 表达 |
|---|---|
| `id` | `kb_id`；应用必须提供稳定值，不能取文件名 |
| `title` | 一级标题和可选 `title` text |
| `type` | `kb_type` link 到 Types |
| `genre` | `kb_genre` link 到 Genres |
| `form` | `kb_form` link 到 Forms |
| `cognitive_level` | `kb_cognitive_level` text；当前无独立导出词表时保持正式值 |
| `subjects` | `kb_subjects` list，链接 Topics |
| `entities` | `kb_entities` list，链接 Entities |
| `source` | `kb_source` text 或 link，按内容模型对象类型区分，不复用主题来源语义 |
| `status` | `kb_status` text |
| `created`／`modified` | date 或 datetime |
| `replaces`／`isReplacedBy` | 内容笔记 links |
| 正文 | frontmatter 后的 Markdown 正文 |

知识库实现必须校验引用目标和稳定 ID。Obsidian 文件名、标题、alias、tag、反向链接或创建时间都不能替代内容模型字段。

## 浏览视图

生成三个 `.base` 文件：Topics、Entities、Sources。每个 Base：

- 用 `file.inFolder()` 和 `file.ext == "md"` 限定对应目录；
- table view 只显示稳定 ID、显示名称、状态及该对象最重要的扁平属性；
- 不使用 backlink 聚合、公式、插件视图或写回动作；
- Base 是便捷视图，不是数据源；删除 `.base` 不影响导出的 Markdown 对象。

## Manifest

`manifest.json` 使用 canonical JSON：UTF-8、对象键排序、两个空格缩进、文件末尾换行。它包含：

- `schema: "kb-design-obsidian-export"`；
- `schema_version: 1`；
- 六份正式词表的路径、版本和 SHA-256；
- 导出器文件 SHA-256；
- 每类对象计数；
- 除 `manifest.json` 自身外，每个生成文件的 vault 相对路径、对象种类、稳定 ID 和 SHA-256；
- `total_files` 计入 manifest 自身，`content_files` 等于文件条目数，生成内容集合 SHA-256 只覆盖条目，避免自引用哈希。

Manifest 不包含生成时间、绝对路径、系统用户名或文件 mtime，保证相同输入逐字节一致。

## 生成规则

- 所有对象按 `id` 排序；数组成员保持正式主题记录顺序；YAML property 键按规格固定顺序；列表保持定义顺序并去重。
- 文本按 YAML 安全转义；内部链接整体加双引号；正文表格转义 `|` 和换行。
- 文件使用 LF 和 UTF-8，末尾恰有一个换行。
- 同一输入连续导出两次，目录逐字节一致。
- 导出前验证全部内部引用目标存在；任何悬空引用、重复输出路径、非法 ID、未知必需字段或 YAML 序列化失败都阻断整个输出。
- 先在同级临时目录完整生成和验证，再原子重命名为目标。失败时删除临时目录，目标仍不存在。

## 回流边界

本阶段不实现回流。人工在导出笔记中修改 properties、正文、aliases、链接、Base 或文件名都不会写回本仓库，也不取得项目效力。

未来回流须另行设计：保存 vault 文件、位置与上下文；识别稳定 `kb_id`；区分用户正文与生成区；报告差异；把未解析字符串交人工；完成概念、designation、权限和来源判断。不得使用文件名、alias、tag 或链接自动创建记录。

## 错误处理

- 输入文件缺失、YAML 解析失败、正式引用悬空、ID 重复或输出冲突：退出非零，不创建目标。
- 输出目录非空、是符号链接或位于禁止路径：退出非零，不修改目录。
- 某字段无法映射：在对象正文的“未映射值”区完整保存路径和值，并在 manifest 记录 warning；不能静默丢失。
- 遇到当前规格未知的新字段：默认阻断。只有明确列为可保留未知字段的对象才允许写“未映射值”。
- 用户中断或写入失败：删除本次临时目录，不触碰目标或其他 vault 文件。

## 验收条件

- 设计文档逐项回答内容模型的五个应用映射问题。
- 导出当前六份正式词表、24 个数组和全部正式记录；对象计数与输入一致。
- 所有生成 Markdown frontmatter 可由安全 YAML 解析，properties 无嵌套值，内部链接目标全部存在。
- aliases 只来自正式已有形式，没有新增译名或名称。
- Base 文件可由安全 YAML 解析，filter 只作用于各自管理目录。
- manifest 与生成目录双向一致，路径、计数和 SHA-256 无遗漏。
- 两次独立导出逐字节一致；修改任一正式输入后 manifest 和相应输出发生可解释变化。
- 非空目标、悬空引用和未知字段的失败测试通过，且失败不留下目标。
- 正式 `vocab/`、设计、概念、来源和术语所有权没有变化。
- README、设计索引和项目路线明确 Obsidian 映射已建立，TBX 与严格激活仍后置。
