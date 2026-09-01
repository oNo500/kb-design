# Obsidian 官方帮助

## 材料身份

本笔记只记录 [Obsidian Help](https://obsidian.md/help/) 发布的产品帮助页面，核对日期为 2026-09-01。它们说明 Obsidian 的文件、properties、链接和 Bases 行为；不因此取得本项目数据、术语或导出规则的决策权。

## 阅读范围

本次逐页读完下列公开帮助页面的全部可见正文；表中的“完整页面”只表示实际读取该页面全部正文，不表示打开其交叉链接或未列的帮助页。

| 材料 | 实际读到的位置 |
|---|---|
| [数据存储](https://obsidian.md/help/data-storage) | 完整页面：vault、vault settings、global settings、IndexedDB 和 metadata cache |
| [Properties](https://obsidian.md/help/properties) | 完整页面：property types、not supported、YAML format、各类型格式、JSON properties 和 default properties |
| [内部链接](https://obsidian.md/help/links) | 完整页面：支持格式、文件链接、标题与块链接、显示文本和预览 |
| [Aliases](https://obsidian.md/help/aliases) | 完整页面：定义、YAML list 格式、以 alias 建立链接和未链接提及 |
| [支持格式](https://obsidian.md/help/Files%2Band%2Bfolders/Accepted%2Bfile%2Bformats) | 完整页面：支持的文件类型和 embed files |
| [Bases](https://obsidian.md/help/bases) | 完整页面：core plugin、数据位置、views 和 view types |
| [Bases 语法](https://obsidian.md/help/bases/syntax) | 完整页面：`.base`、filters、formulas、properties、summaries、views 与 note properties |
| [表格视图](https://obsidian.md/help/bases/views/table) | 完整页面：表格行列、summaries 和编辑快捷键 |

## 对象边界

- vault 是本地文件系统中的文件夹，包含其子文件夹；笔记是 Markdown 格式的纯文本文件。[数据存储](https://obsidian.md/help/data-storage)
- 官方建议不要嵌套 vault，因为内部链接属于单一 vault 且可能不能正确更新；这是建议，不是禁止。[数据存储](https://obsidian.md/help/data-storage)
- property 存在文件开头的 YAML frontmatter 中。官方列出的 property types 是 Text、List、Number、Checkbox、Date、Date & time 和 Tags；一个 property name 一经分配类型，vault 内所有同名 property 都使用该类型。[Properties](https://obsidian.md/help/properties)
- alias 是同一笔记的替代名称。`aliases` 应使用 YAML list；选择 alias 时，Obsidian 生成指向真实文件、以 alias 为显示文本的链接。[Aliases](https://obsidian.md/help/aliases)
- Base 是 core plugin，使用笔记及其 properties 建立类似数据库的 views；一个 Base 可以有多个 views。[Bases](https://obsidian.md/help/bases)

## 存储行为

Obsidian 将 vault 的变化与其本地 metadata cache 同步；外部编辑器和文件管理器可以编辑这些纯文本笔记。[数据存储](https://obsidian.md/help/data-storage) 这说明文件在应用外可以被修改，不等于本项目会读取、接受或赋予那些修改效力。

## 属性行为

Properties 以 YAML 存在文件开头。Checkbox property 的 YAML 值是 `true` 或 `false`，并在 Live Preview 显示为 checkbox；因此 boolean 是 YAML 值的形态，不是官方 property type 的名称。[Properties](https://obsidian.md/help/properties)

Obsidian 当前不支持 nested properties，并建议在 source mode 查看它们；同时，YAML 仍然能够保存嵌套结构。前者是应用的编辑与查看支持限制，后者不应被表述为 YAML 的表达限制。[Properties](https://obsidian.md/help/properties)

## 链接行为

内部链接支持 Wikilink 和 Markdown link。文件夹路径从 vault 根开始，使用正斜线；若目标笔记尚不存在，Obsidian 会在该路径创建笔记。Wikilink 可用竖线指定显示文本。[内部链接](https://obsidian.md/help/links)

Text 和 List properties 可以包含内部链接，但必须用引号包围。alias 用作链接选择时，生成的链接仍以真实文件为目标，只以 alias 显示。[Properties](https://obsidian.md/help/properties) [Aliases](https://obsidian.md/help/aliases)

## 视图行为

Bases 读取本地 Markdown 文件及其 properties，可查看、编辑、排序和筛选文件与 properties；因此 Base 不是技术上的只读对象。[Bases](https://obsidian.md/help/bases)

`.base` 文件是有效 YAML，保存 filters、formulas 和 views。默认 Base 数据集包括 vault 内全部文件，filters 可将其收窄；note properties 只适用于 Markdown 文件。[Bases 语法](https://obsidian.md/help/bases/syntax)

表格视图以文件为行、properties 为列，并提供粘贴、撤销、重做、清除单元格和切换 checkbox 等编辑操作。[表格视图](https://obsidian.md/help/bases/views/table)

## 格式范围

官方 accepted file formats 列出 Markdown 的 `.md` 与 Bases 的 `.base`，另列 JSON Canvas 的 `.canvas`、媒体和 PDF；普通 `.json` 不在该内容格式清单中。[支持格式](https://obsidian.md/help/Files%2Band%2Bfolders/Accepted%2Bfile%2Bformats) Properties 页面允许以 JSON block 写 frontmatter，且保存时会转为 YAML；这不使普通 `.json` 文件成为 Obsidian content format。[Properties](https://obsidian.md/help/properties)

## 设计差异

| 现行主张 | 结论 | 纠偏方向 |
|---|---|---|
| “布尔值”是 property type | 不精确 | 官方 type 是 Checkbox，YAML 值为 boolean |
| nested properties 无法表达 | 过强 | 改为 Obsidian 当前不支持；YAML 仍可保存嵌套结构 |
| Base 提供只读表格 | 错误 | 改为项目用作浏览入口，但 UI 可以编辑 |
| manifest 是 Obsidian 输出对象 | 需限缩 | 是同目录项目清单，不是 accepted content format |

现行映射的“不回流”是项目效力上的单向约束：导出目录中的修改不写回本库，也不取得项目效力。它不能改写 Obsidian 可以编辑 Markdown、properties 或 Base 的产品事实。

## 适用边界

官方帮助可以证明上述产品能力、格式和限制，不能决定本项目的稳定 ID、正式数据效力、designation 准入、字段基数、导出失败政策、回流、确定性或安全替换。是否将可编辑的 Obsidian 文件视为浏览入口、是否接受回流及其效力，仍须由本项目治理和应用映射决定。

## 未读范围

- 未读取本次八页所链接的交叉帮助页、版本历史、release notes、API、开发者文档、社区插件页面或外部规范。
- 未在 Obsidian 应用中建立 vault、创建 property、编辑 Base 或执行导出；本笔记只记录官方帮助页面直接陈述的能力与限制。
