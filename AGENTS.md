# kb-obsidian 项目约定

## 仓库角色

本仓库只实现 Obsidian 应用行为。概念、正式词表、内容模型和治理规则以 `kb-design` 为唯一权威；本仓库不复制、编辑或重新定义正式知识内容。

## 写集边界

用户写集包含 `Home.md`、`Inbox/`、`Sources/`、`Content/`、`Indexes/` 和 `Attachments/`。受管理写集包含 `KB/`、`App/Templates/`、`App/Views/`、`App/Rules/` 和 `App/manifest.json`。报告写集只包含 `App/Reports/`。`.obsidian/` 是配置边界。应用必须保持这些写集和边界分离，不得把管理文件、报告或配置当作用户内容。

## 内容契约

新内容使用无前缀、小写、标准连字符的 UUIDv4 作为稳定标识，并写入 `Content/<UUIDv4>.md`。`title` 同时进入一级标题、`title` Text property 和 `aliases` 中恰好一个派生值。人的检索依赖 title 与 alias 等元数据，不依赖 UUID 文件名。

## 回流边界

应用不自动把 Obsidian 中的修改回写 `kb-design` 或正式数据，也不自动返回、修复或切换任何内容。非空 vault 不作自动更新。

## 审查与测试

只为高价值行为设计测试：稳定身份、写集边界、引用语义、状态约束和正式计数。静态文件、确定性生成物和纯机械事实直接校验；低价值测试不做。

## 分支规则

实现不得在 `master` 上进行。变更前应使用专用分支，并在提交说明中标注 `[L1]`、`[L2]` 或 `[L3]` 决策级别。
