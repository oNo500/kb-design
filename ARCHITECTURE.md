# 项目架构 (Project Architecture)

本仓库同时保存应用无关的知识设计、正式词表、共享 Python 能力和 Obsidian 应用。monorepo 只统一工程组织与依赖管理，不改变既有业务规则、数据身份、对象状态或决策权。

## 职责分层

| 层次 | 职责 | 位置 |
|---|---|---|
| 知识设计 | 概念、现行模型、治理规则、决定、草案与来源笔记 | `docs/` |
| 正式数据 | 六份正式词表 | `data/vocab/` |
| 生成输入 | 主题生成输入与未启用术语配置 | `data/inputs/` |
| 审计材料 | 迁移账本、维护记录与标签复核材料 | `data/audit/` |
| 共享契约 | 跨工程使用的 JSON Schema | `schemas/` |
| 核心工程 | 生成、校验、来源与术语维护能力 | `packages/kb-core/` |
| 应用工程 | Obsidian 初始化、导出、刷新、内容校验与报告 | `apps/obsidian/` |
| 整仓辅助 | 链接、格式等仓库级检查 | `scripts/` |
| 执行记录 | 当前路线、实施计划、复核与历史过程材料 | `work/` |
| 应用数据 | 默认持久 vault 与其他本地产物 | `output/` |
| 临时产物 | 可重新生成并清理的中间文件 | `build/` |

知识设计与应用表示继续分层。[内容模型](docs/design/model/content-model.md)和正式词表不依赖 Obsidian；[Obsidian 映射](docs/design/targets/obsidian.md)选择具体表示；应用代码物化并维护该表示。生成文件中的修改不回流，也不取得项目效力。

## 工程关系

根目录是 uv workspace，使用统一的 `uv.lock` 和 `.python-version`。当前开发环境固定为 Python 3.13.5，成员包声明的最低版本为 Python 3.11。

```text
kb-design
├── packages/kb-core
└── apps/obsidian ──depends on──> packages/kb-core
```

`kb-core` 不依赖具体应用。`kb-obsidian` 通过 workspace 依赖使用核心包。源码、输入和 schema 都从显式仓库根定位，不依赖调用命令时的工作目录。

## 数据权威

正式词表只有 `data/vocab/` 中的六份 YAML。`data/vocab/topics.yaml` 同时是正式主题词表和确定性生成物；人工修改 `data/inputs/topics/` 及核心实现后，以 `uv run kb-core build-topics` 重建，再运行 `uv run kb-core check-topics`。

[术语表](docs/glossary.md)继续承担 designation 与中英对照的现行编辑权。`data/inputs/terminology/glossary-layout.yaml` 仍未启用，仓库仍没有正式 `data/vocab/terms.yaml`。`data/audit/` 只保存审计与复核材料，不批准正式值，也不反向修改正式数据。

## 应用输出

Obsidian 应用默认使用仓库内被 Git 忽略的 `output/obsidian/` 作为持久 vault。`init` 可用 `--output` 指向其他目录，后续命令可用 `--vault` 指向仓库内或外部 vault；`--design-root` 继续用于显式指定设计来源。

`output/` 不属于构建清理对象。`build/` 只保存可丢弃的临时产物。刷新写集仍限于 vault 的 `kb/` 与 `app/manifest.json`，用户内容、附件、配置、模板、视图和规则按既有边界保留。

## 效力边界

目录、包、schema、命令、应用实现和输出位置只提供结构与机械能力。它们不使审计材料成为正式数据，不使草案生效，也不自动建立正式来源、术语、消费者、查询日志、回流、切换或发版状态。完整效力边界见[当前阶段](docs/decisions/current-stage-scope.md)，布局变化见[仓库布局](docs/decisions/monorepo-layout.md)。
