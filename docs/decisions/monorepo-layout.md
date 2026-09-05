# 仓库布局

状态：已采纳，2026-09-05。用户批准把现有设计、核心能力和 Obsidian 应用整理为同一 monorepo，并使用 uv workspace 管理 Python 工程。

## 组织范围

本次只调整现有文件的目录、Python 包组织、命令入口和默认输出位置，不重构业务规则。现有概念、正式词表、内容模型、治理规则、稳定身份、记录状态、未生效草案和决策权保持不变。

根 `README.md` 保留为稳定入口，不承担动态导航。`docs/README.md` 是现行文档导航，`ARCHITECTURE.md` 只说明目标架构，`work/roadmap.md` 记录当前工作、状态和后置门禁。

## 目录职责

- `docs/` 保存概念、现行设计、已采纳决定、未生效草案、术语表和来源笔记；
- `data/vocab/` 保存六份正式词表；
- `data/inputs/` 保存主题生成输入与未启用术语配置；
- `data/audit/` 保存迁移账本、维护记录和标签复核材料；
- `schemas/` 保存跨工程共享契约；
- `packages/kb-core/` 保存应用无关的生成、校验、来源与术语维护能力；
- `apps/obsidian/` 保存 Obsidian 应用；
- `scripts/` 保存整仓辅助；
- `work/` 保存当前路线、实施计划、复核和历史过程材料；
- `output/` 保存被 Git 忽略的持久应用数据，`build/` 保存被 Git 忽略的可清理临时产物。

`data/vocab/topics.yaml` 继续是正式主题词表和确定性生成物。`docs/glossary.md` 继续是 designation 与中英对照的现行编辑源。目录迁移不把生成输入、审计记录、schema、测试或应用输出提升为正式数据。

## 工程关系

仓库根目录使用统一的 uv workspace、`uv.lock` 和 `.python-version`。`apps/obsidian/` 通过 workspace 依赖使用 `packages/kb-core/`；核心包不依赖具体应用。成员包最低支持 Python 3.11，当前开发环境固定为 Python 3.13.5。

核心命令统一从仓库根以 `uv run kb-core <命令>` 调用，原脚本名中的下划线在命令名中改为连字符。Obsidian 命令以 `uv run kb-obsidian <命令>` 调用。整仓辅助以 `uv run python scripts/<文件>` 调用。不为旧脚本路径或旧目录增加兼容层。

## 输出边界

Obsidian 默认持久 vault 位于 `output/obsidian/`。`init` 的 `--output` 和后续命令的 `--vault` 可以显式指向其他目录，包括仓库外的绝对路径；`--design-root` 保留。

`output/` 不属于构建清理对象，`build/` 可以清理和重建。刷新写集继续只包括 vault 的 `kb/` 与 `app/manifest.json`；用户内容、附件、配置、模板、视图和规则保持既有保护边界。

## 历史解释

迁移前的已采纳决定和历史执行材料保持原文字节。它们记载的路径按形成该记录时的基线 Git 快照解释；当前位置由本决定、`docs/README.md` 和逐文件迁移对照说明。路径变化不重授旧决定的权力，也不改变其适用语义。

## 阶段边界

本决定不搬迁或刷新现有外部 `kb-vault`，不创建默认 vault，不批准正式来源 v2 数据、正式术语数据、正式义务、正式索引、委托、消费者、回流、正式切换或发版。应用实现和默认输出位置存在仍不等于消费者激活。

## 决定关系

[工具归属](obsidian-tool-location.md)中把工具定位为 `tools/obsidian/`、并以“实际 vault 不迁入设计仓库”排除仓库内默认持久输出的布局条款，由本决定的 `apps/obsidian/` 与 `output/obsidian/` 取代。该决定关于语义分层、干净 Git 快照、实际提交与输入哈希、旧 vault 验证、刷新写集及不构成正式激活或发版的其他边界继续有效；现有外部 vault 仍不在本次迁移中搬迁或刷新。

[设计与应用分离](form-independence.md)、[应用约束与表示分层](application-profile-boundary.md)、[词表参考刷新](obsidian-reference-refresh.md)和[当前阶段](current-stage-scope.md)继续有效。本决定只改变这些规则在 monorepo 中的文件位置、工程依赖和默认输出位置，不改变其语义权威。
