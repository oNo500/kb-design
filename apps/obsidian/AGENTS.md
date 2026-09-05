# kb-obsidian 项目约定

## 工具角色

本目录只实现 Obsidian 应用行为，并遵守仓库根 [AGENTS.md](../../AGENTS.md)。概念、正式词表、内容模型和治理规则以仓库中的现行编辑源为唯一权威；应用不复制、编辑或重新定义正式知识内容。

应用通过 uv workspace 依赖 `packages/kb-core/`。命令从显式仓库根定位资源，不依赖调用时的工作目录。默认 vault 位于 `output/obsidian/`；显式 `--output`、`--vault` 和 `--design-root` 优先，并允许外部绝对路径。

设计来源必须是干净的 Git 快照。manifest 记录实际提交与输入哈希，不使用提交白名单。旧 vault 刷新仍须验证祖先提交与旧输入哈希，见[工具归属](../../docs/decisions/obsidian-tool-location.md)。

## 写集边界

用户写集包含 `home.md`、`inbox/`、`sources/`、`content/`、`indexes/` 和 `attachments/`。受管理写集包含 `kb/`、`app/templates/`、`app/views/`、`app/rules/` 和 `app/manifest.json`。报告写集只包含 `app/reports/`，`.obsidian/` 是配置边界。应用必须保持这些写集分离。

`app/reports/index.md` 只导航人读 Markdown 报告；`app/reports/data/` 下的 JSON 供终端和程序读取。报告发布时必须原子替换整棵 `app/reports/`，不得让 Markdown 与 JSON 分属不同版本。

## 内容契约

新内容使用无前缀、小写、标准连字符的 UUIDv4 作为稳定标识，并写入 `content/<UUIDv4>.md`。`title` 同时进入一级标题、`title` Text property 和 `aliases` 中恰好一个派生值。人的检索依赖 title 与 alias 等元数据，不依赖 UUID 文件名。

## 回流边界

应用不自动把 Obsidian 修改回写正式数据，也不自动返回、修复或切换内容。非空 vault 只通过用户明确调用的 `refresh` 更新 `kb/` 与 `app/manifest.json`，不更新用户内容、配置、模板、视图或规则。初始化仍只接受空目录。

`output/` 保存持久应用数据，不属于构建清理对象；`build/` 才是可清理的临时产物。本次迁移不得创建默认 vault，也不得搬迁或刷新现有外部 `kb-vault`。

## 审查与测试

只为高价值行为设计测试：稳定身份、写集边界、引用语义、状态约束和正式计数。静态文件、确定性生成物和纯机械事实直接校验；低价值测试不做。

## 分支规则

实现不得在 `master` 上进行。变更前使用专用分支，提交说明标注 `[L1]`、`[L2]` 或 `[L3]` 决策级别。
