# Obsidian 映射

本文规定现行内容模型与六份正式词表在 Obsidian 中的表达。当前实现只生成词表参考区；内容单元映射是知识库应用必须遵守的契约，仓库尚无内容单元导出器。

Obsidian 把笔记保存为 vault 中的 Markdown 纯文本文件，并从文件开头的 YAML 读取 properties。它支持文本、列表、数字、布尔值、日期、日期时间和 tags，但不支持嵌套 properties，也不在 property 中渲染 Markdown。[Obsidian 的数据存储](https://obsidian.md/help/Files%2Band%2Bfolders/How%2BObsidian%2Bstores%2Bdata)与 [properties](https://obsidian.md/help/properties)只提供应用能力依据，不改变本库字段定义。

## 效力边界

- `vocab/topics.yaml`、`vocab/entities.yaml`、`vocab/sources.yaml`、`vocab/types.yaml`、`vocab/genres.yaml` 和 `vocab/forms.yaml` 是导出的正式输入。
- `vocab/topics.yaml` 的编辑路径仍由[主题词表设计](../topics.md)规定；其他正式词表仍按各自设计维护。
- Obsidian 输出是可重建的只读参考区，不是正式词表、术语表、迁移账本或新的编辑源。
- 导出器不读取来源与术语迁移账本、候选记录、未激活模式、草案、诊断报告或 Superpowers 过程文件。
- `concepts/glossary.md` 继续承担 designation 与中英对照的现行编辑权；正式术语数据尚未激活。
- 本阶段不导入、不回流、不覆盖已有 vault，也不实现 TBX。

## 接口总表

本映射逐项回答[内容模型](../content-model.md)规定的五个接口问题。

| 接口问题 | 本应用的处理 |
|---|---|
| 字段落点 | 内容字段进入下文规定的 YAML property、一级标题或 Markdown 正文 |
| 词表导出 | 每个正式记录生成一篇稳定 ID 路径的参考笔记，另生成数组笔记、浏览视图和 manifest |
| 引用表达 | 受控值、主题、实体、来源和内容单元引用使用 vault 根相对 Wikilink |
| 回流接口 | 当前不存在；导出目录中的修改不写回，也不产生项目效力 |
| 表达缺口 | 可扁平值进入 properties；嵌套依据、映射和历史进入正文；未知字段阻断导出 |

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

对象文件名为 `<id>.md`。标签、别名和译名变化不改路径。内部链接从 vault 根开始并使用正斜线；Obsidian 官方同时支持 Wikilink 和 Markdown 链接，且文件夹路径从 vault 根开始，本映射固定使用较紧凑的 Wikilink。[内部链接](https://obsidian.md/help/links)只支持该应用语法选择，稳定身份仍由本库 ID 决定。

## 公共属性

每篇对象笔记使用下列公共 properties；不存在的值省略，不写空字符串、空列表或 `null`。

| Property | 类型 | 取值 |
|---|---|---|
| `kb_id` | text | 正式稳定 ID |
| `kb_object` | text | `topic`、`array`、`entity`、`source`、`type`、`genre` 或 `form` |
| `kb_label` | text | 中文标签、英文标签、ID 的固定回退结果 |
| `kb_status` | text | 正式记录已有的状态 |
| `kb_version` | text | 所属正式词表的版本 ID |
| `aliases` | list | 正式 `label`、`alt` 和 `hidden` 中除显示形式外的非空形式 |
| `tags` | tags | `kb-design/<object>` |

`aliases` 只保存正式数据中已经存在的形式，不翻译、不补名、不规范化出新形式。Obsidian 把 alias 定义为同一笔记的替代名称，并要求使用 YAML 列表；选择 alias 后仍链接真实文件。[Aliases](https://obsidian.md/help/aliases)支持这一载体用途，不构成 designation 准入或概念对应依据。

## 词表导出

正式对象按下列规则生成。

| 对象 | 路径 | 专有 properties | 正文保留 |
|---|---|---|---|
| 主题 | `KB/Topics/<id>.md` | `kb_broader`、`kb_related`、`kb_arrays`、`kb_source`、`kb_added`、`kb_replaced_by`；替代目标是 text link | 范围、替代形式、隐藏形式、形式依据、外部映射、历史记录 |
| 主题数组 | `KB/Arrays/<id>.md` | `kb_superordinate`、`kb_source`、`kb_members` | 数组的分组职责 |
| 实体 | `KB/Entities/<id>.md` | `kb_kind`、`kb_subjects`、`kb_vendor`、`kb_creator`、`kb_replaced_by`、`kb_form`、`kb_tier`、`kb_url`、`kb_watch`、`kb_checked`、`kb_added`、`kb_entity_version` | 范围、归属依据、外部映射、历史记录 |
| 来源用途 | `KB/Sources/<id>.md` | `kb_entity`、`kb_roles`、`kb_checked` | 来源用途与来源实体身份的区别 |
| 文档类型 | `KB/Types/<id>.md` | `kb_broader`、`kb_related`、`kb_arrays`、`kb_source`、`kb_added`、`kb_replaced_by` | 范围、已有形式、依据、映射和历史 |
| 体裁 | `KB/Genres/<id>.md` | 同文档类型 | 范围、已有形式、依据、映射和历史 |
| 载体 | `KB/Forms/<id>.md` | 同文档类型 | 范围、已有形式、依据、映射和历史 |

数组成员从正式主题记录反向构造，并保持正式主题记录顺序。主题数组只表达树内分组，不取得主题概念、分面或手工概念组的效力。

`forms.yaml` 中的载体数组不生成另一类对象笔记。导出根 README 逐项保存其 ID、上位根和来源；每篇载体笔记保存已有数组 ID。这样保留正式值而不制造第八种对象。

## 引用表达

所有对象引用都以目标稳定 ID 计算路径，以目标正式标签计算显示文本。

```md
[[KB/Topics/security|安全]]
```

显示文本缺少中文时使用英文，两者都缺少时使用 ID。显示文本不参与目标解析。主题层级、相关关系、数组成员、实体关系和来源用途必须解析到已生成目标；悬空引用阻断整个导出。

property 中的链接整体按 YAML 字符串保存。Obsidian 官方要求文本或列表 property 中的内部链接加引号；本实现不使用标题引用或块引用，避免把可变正文位置当作身份。[Properties](https://obsidian.md/help/properties)与[内部链接](https://obsidian.md/help/links)规定这些应用语法。

## 内容契约

内容单元不由当前导出器生成。知识库应用将来创建 Obsidian 内容笔记时，必须按下表映射，不得用文件名、标题、alias、tag、反向链接或文件时间替代内容模型字段。

| 内容字段 | Obsidian 表达 |
|---|---|
| `identifier` | `kb_id` text；稳定值由知识库应用提供 |
| `title` | 一级标题；需要查询时同时保存 `title` text |
| `type` | `kb_type` text link，指向 Types |
| `genre` | `kb_genre` text link，指向 Genres |
| `form` | `kb_form` text link，指向 Forms |
| `level` | `kb_level` text，保持内容模型的正式值 |
| `subject` | `kb_subjects` list，指向 Topics |
| `entities` | `kb_entities` list，指向 Entities |
| `source` | `kb_source` text link，按内容模型识别内容单元或实体目标 |
| `references` | `kb_references` list，指向作为文献或标准的 Entities |
| `created` | `kb_created` date |
| `modified` | `kb_modified` date |
| `status` | `kb_status` text |
| `isReplacedBy` | `kb_is_replaced_by` text link，指向内容笔记 |
| `relation` | `kb_relation` list，指向内容笔记 |
| `language` | `kb_language` text；默认 `zh` 时可以省略 |
| 正文 | frontmatter 后的 Markdown 正文 |

应用必须校验恰好一个 `type`、恰好一个 `genre`、至少一个 `subject`、受控值目标、内容单元引用和生命周期约束。当前仓库没有内容目录、应用校验器或内容导出命令，因此本节只确定接口，不宣称上述能力已经实现。

## 表达缺口

Obsidian properties 不支持嵌套值，也不渲染其中的 Markdown。正式记录中的 `basis`、`match` 和 `history` 因而进入正文表格或 YAML 代码块；`scope`、替代形式和隐藏形式也进入正文。正文是导出表示的一部分，但不替代正式 YAML 的编辑权。

当前导出器对每类正式记录使用显式允许字段表。遇到未知字段、非法 ID、重复 ID、无法解析的引用、重复输出路径或不能安全序列化的值时，导出失败；它不把未知值静默放入“其他”字段，也不丢弃后继续生成。

内容应用以后遇到 Obsidian 不能表达的约束时，应在应用校验器中保留约束并阻断无效内容；不得通过放宽内容模型、改成自由 tag 或自动建立概念来绕过。

## 浏览视图

导出器生成 Topics、Entities 和 Sources 三个 `.base` 文件。每个文件使用 `file.inFolder()` 和 Markdown 扩展名限制结果，提供一张只读表格；它不使用公式、反向链接聚合、插件视图或写回动作。

Obsidian 把 Bases 保存为 `.base` YAML 文件；默认数据集包含 vault 中全部文件，须用 filter 收窄。[支持格式](https://obsidian.md/help/Files%2Band%2Bfolders/Accepted%2Bfile%2Bformats)与 [Bases 语法](https://obsidian.md/help/bases/syntax)支持当前文件和过滤器选择。当前验收只证明 `.base` 按官方语法静态生成并可解析为 YAML，没有宣称已在 Obsidian 应用内运行。Base 只是浏览视图，删除它不改变对象笔记或正式数据。

## 导出清单

`manifest.json` 使用 UTF-8 canonical JSON，键排序、两个空格缩进并以换行结束。它保存：

- schema 名称与版本；
- 六份正式输入的路径、版本和 SHA-256；
- 导出器字节的 SHA-256；
- 各对象种类的计数；
- 除 manifest 自身外，每个生成文件的相对路径、对象种类、输出标识和 SHA-256；正式对象的输出标识是稳定 ID，README 与 Base 使用文件 stem 作为 manifest 内部标识；
- 内容文件数、包含 manifest 的总文件数和内容集合 SHA-256。

内容和 manifest 元数据读取同一份输入字节快照。manifest 不保存生成时间、绝对路径、用户名、输出目录或 mtime，也不把自身列入文件条目和内容集合哈希。

## 运行接口

从仓库根运行：

```bash
python3 scripts/export_obsidian.py --repo-root . --output /absolute/new/path
```

输出目录必须不存在或为空。成功时标准输出是一行排序 JSON，只含 `output`、`content_files`、`total_files` 和 `content_sha256`。参数错误、输入错误或写入错误时，标准错误以 `OBSIDIAN_EXPORT_ERROR` 开头并退出 `1`；`--help` 正常退出 `0`。

导出目录可以作为独立 vault，也可以在人工核对 manifest 后复制到现有 vault 的一个管理目录。Obsidian 不建议 vault 嵌套，因为内部链接属于单个 vault；本映射不建立嵌套 vault。[数据存储](https://obsidian.md/help/Files%2Band%2Bfolders/How%2BObsidian%2Bstores%2Bdata)提供这一应用限制。

## 安全边界

导出器在创建临时目录前拒绝非空目标、符号链接、仓库根、文件系统根、用户主目录和仓库中的正式数据、设计、概念、来源、脚本与测试目录。

全部文件先写入目标同级的新临时目录，再回读并校验文件集合、逐文件哈希、Markdown frontmatter、Base YAML、内部链接和 manifest 双向覆盖。只有校验通过才尝试目录替换；失败时只删除本次创建的临时目录，不递归删除用户目标。已有空目录在平台不支持目录替换时保持原状。

更新已有参考区时应导出到另一个新目录、核对 manifest，再由人决定替换旧目录。导出器不提供覆盖、合并或删除旧目录的参数。

## 回流边界

当前没有回流接口。人工修改导出笔记中的 properties、正文、aliases、链接、Base 或文件名，不会写回本仓库，也不取得项目效力；下次导出也不读取这些修改。

未来回流必须另行设计，并至少保存 vault 文件、位置和上下文，读取稳定 `kb_id`，区分用户正文与生成表示，报告差异，把未解析字符串交人工，分别完成概念、designation、权限和来源判断。它不得从文件名、alias、tag、链接或反向链接自动创建记录、关系或状态。

## 验收门禁

本映射的必要验收覆盖下列风险。

- 每个正式对象恰有一条稳定路径，全部正式引用都有生成目标。
- properties 可由安全 YAML 解析且不含嵌套值；正文完整保存被移出的嵌套数据。
- aliases 只来自正式已有形式，没有新增名称或译名。
- manifest 与生成目录双向一致，并证明生成内容使用的同一份输入快照。
- 相同输入的两个独立导出目录逐字节一致。
- 非空目标、空符号链接、目录替换失败和写后回读失败都不损坏目标或留下临时目录。
- 正式词表、术语编辑权、内容模型、草案状态和发版状态不因导出改变。

机械计数和哈希由导出器、测试及一次端到端导出证明，不另交第二代理重复确认。内容单元契约只有真实知识库消费者出现并实现后，才能验收内容导出和回流。

## 待定事项

- 真实知识库内容目录、文件布局和调用方出现后，实现并校验“内容契约”。
- 只有回流需求出现后，另行设计上下文保存、差异报告、人工判断和权限门禁。
- TBX 只按[未生效草案](../drafts/tbx-export.md)中的真实接收方条件重新进入设计。

## 权威来源

- [Obsidian 的数据存储](https://obsidian.md/help/Files%2Band%2Bfolders/How%2BObsidian%2Bstores%2Bdata)：vault、Markdown 纯文本和嵌套 vault 限制。
- [Obsidian properties](https://obsidian.md/help/properties)：YAML 位置、支持类型、嵌套值限制和 property 内链接。
- [Obsidian 内部链接](https://obsidian.md/help/links)：Wikilink、vault 根相对路径和显示文本。
- [Obsidian aliases](https://obsidian.md/help/aliases)：alias 列表和目标文件关系。
- [Obsidian 支持格式](https://obsidian.md/help/Files%2Band%2Bfolders/Accepted%2Bfile%2Bformats)：Markdown 与 Bases 文件扩展名。
- [Obsidian Bases 语法](https://obsidian.md/help/bases/syntax)：YAML、filters、views 和 `file.inFolder()`。
