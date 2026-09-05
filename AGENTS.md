# kb-obsidian 项目约定

## 仓库角色

本仓库只实现 Obsidian 应用行为。概念、正式词表、内容模型和治理规则以 `kb-design` 为唯一权威；本仓库不复制、编辑或重新定义正式知识内容。

## 写集边界

用户写集包含 `home.md`、`inbox/`、`sources/`、`content/`、`indexes/` 和 `attachments/`。受管理写集包含 `kb/`、`app/templates/`、`app/views/`、`app/rules/` 和 `app/manifest.json`。报告写集只包含 `app/reports/`。`.obsidian/` 是配置边界。应用必须保持这些写集和边界分离，不得把管理文件、报告或配置当作用户内容。

`app/reports/index.md` 只导航人读 Markdown 报告；`app/reports/data/` 下的 JSON 是终端和程序读取的机器表示，不是 Obsidian 的人读入口。报告发布时必须原子替换整棵 `app/reports/`，不得让 Markdown 与 JSON 分属不同版本。

## 内容契约

新内容使用无前缀、小写、标准连字符的 UUIDv4 作为稳定标识，并写入 `content/<UUIDv4>.md`。`title` 同时进入一级标题、`title` Text property 和 `aliases` 中恰好一个派生值。人的检索依赖 title 与 alias 等元数据，不依赖 UUID 文件名。

## 回流边界

应用不自动把 Obsidian 中的修改回写 `kb-design` 或正式数据，也不自动返回、修复或切换任何内容。非空 vault 只通过用户明确调用的 `refresh` 更新 `kb/` 与 `app/manifest.json`，不更新内容、配置、模板、视图或规则；格式差异须与原生成语义一致才可接受，真实修改作为冲突处理。初始化仍只接受空目录。

## 审查与测试

只为高价值行为设计测试：稳定身份、写集边界、引用语义、状态约束和正式计数。静态文件、确定性生成物和纯机械事实直接校验；低价值测试不做。

## 分支规则

实现不得在 `master` 上进行。变更前应使用专用分支，并在提交说明中标注 `[L1]`、`[L2]` 或 `[L3]` 决策级别。
