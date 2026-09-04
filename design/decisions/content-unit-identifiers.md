# 内容单元标识符

状态：已采纳，2026-09-03。

## 背景

现行词表 id 从已有且有依据的英文 label、来源代码或编号取得。这套规则不能为任意中文内容稳定发放身份：内容标题可以修改，也可能没有获准英文 label、来源代码或编号。若从标题机翻、拼音、文件名或创建时间取得身份，会把可变显示信息或未经准入的形式带进永久引用。

[标识符](../../concepts/content-identifiers.md)已经区分资源身份、名称、标题、路径、排序和时间。[RFC 9562 阅读笔记](../../sources/rfc-9562.md)说明 UUID 不需要中央登记，UUIDv4 使用随机或伪随机位，标准文本表示为以连字符分组的十六进制字符串；UUID 不提供真实性、完整性或访问控制。

Obsidian 的 Quick Switcher 按文件名或 alias 查找笔记，Search 可以检索正文和 properties。人的查找不需要依赖 identifier，应用可以分别设计稳定身份和可读检索表示。

## 决定

新内容单元的 `identifier` 使用符合 RFC 9562 的 UUIDv4 标准文本表示：

- 字母使用小写；
- 保留标准连字符；
- 不增加对象前缀；
- 唯一语境是一个知识库中的全部内容单元；
- 建立时生成，写入前检查现有内容 identifier 和目标路径；发生重复时废弃该值并重新生成；
- 一经写入且被引用后永久不变；
- 不从 title、alias、文件名、语言、时间、排序位置或语言模型输出派生。

Obsidian 内容路径使用 `content/<UUIDv4>.md`。路径是该 target 的确定性表示，不改变 identifier 与 path 的概念边界。

人的检索使用元数据和正文：`title` 同时进入一级标题与 Text property，并作为 Obsidian `aliases` 中恰好一个由应用派生的当前标题。Quick Switcher 通过 alias 查找，Search 检索标题、正文和 properties，Bases 按受控字段筛选。标题修改时同时更新一级标题、`title` 和派生 alias，不修改 UUID 或路径。

## 后果

- 同名内容、多语言标题和标题修正不造成身份或路径冲突。
- 文件浏览器显示 UUID，不承担人的主题浏览和标题检索；Home、Indexes、Bases、Search、Quick Switcher 和链接显示文本承担这些职责。
- 内容校验器必须检查 UUIDv4 格式、小写、无前缀、知识库内唯一、文件 stem 与 `kb_id` 相同，以及一级标题、`title` 和派生 alias 一致。
- 派生 alias 只是 Obsidian 查找 binding，不形成术语形式、同义关系或内容模型新字段，也不进入正式使用计数。
- UUID 不能作为密码、权限、真实性或不可猜测性证明。
- 本决定只完成设计规则；内容建立器、校验器和真实 vault 仍未实现或激活。

## 后续状态

2026-09-04，独立 `kb-obsidian` 应用已经实现内容建立器和校验器，并已建立本地持久 vault。该实施满足本决定的身份与查找 binding；实际用户内容和正式消费者仍未激活。
