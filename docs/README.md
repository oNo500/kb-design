# 文档索引 (Documentation Index)

这里是项目的动态导航。根 [README](../README.md) 保留项目入口，[项目架构](../ARCHITECTURE.md)只说明职责与数据流，[项目路线](../work/roadmap.md)记录当前工作、完成状态和后置门禁。

## 效力层次

| 层次 | 位置 | 当前作用 |
|---|---|---|
| 现行设计 | `docs/design/` | 规定当前模型、治理、维护和应用映射 |
| 正式数据 | `data/vocab/` | 保存六份现行正式词表 |
| 已采纳决定 | `docs/decisions/` | 记录已由人批准的规则与范围，只追加不回写 |
| 项目草案 | `docs/drafts/` | 保存未生效提案及其触发条件 |
| 审计材料 | `data/audit/` | 保存迁移账本、维护记录和复核材料，不批准正式值 |
| 执行记录 | `work/` | 保存路线、计划、复核与历史过程材料，不属于项目设计 |

当前基础边界见[当前阶段](decisions/current-stage-scope.md)。monorepo 的目录、包和输出边界见[仓库布局](decisions/monorepo-layout.md)。

## 设计入口

| 范围 | 入口 | 读完知道 |
|---|---|---|
| 概念 | [概念索引](concepts/README.md) | 项目采用的理论及各概念之间的关系 |
| 方法 | [方法登记](design/governance/principles.md) | 哪些方法已登记及其适用边界 |
| 主题 | [主题词表](design/model/topics.md) | 正式主题词表、生成路径与校验规则 |
| 层级 | [层级结构](design/model/hierarchy.md) | 树、多层级、数组与结构来源 |
| 实体 | [命名实体](design/model/entities.md) | 个体、来源实体和现行数据边界 |
| 来源 | [来源登记](design/model/sources-registry.md) | 正式来源用途与未激活基础的边界 |
| 内容 | [内容模型](design/model/content-model.md) | 内容单元字段、状态、身份与引用 |
| 治理 | [治理规则](design/governance/governance.md) | 对象效力、决策权、变更与验收 |
| 维护 | [维护规则](design/governance/maintenance.md) | 指标、触发、动作、复核与审计 |
| 写作 | [写作规则](design/governance/writing.md) | 全库文档与 designation 规则 |
| 预览 | [词表预览](design/targets/vocab-preview.md) | 工作区只读表示与自动更新 |
| 应用 | [Obsidian 映射](design/targets/obsidian.md) | 首个完整应用 target 的语义与表示 |
| 版本 | [词表版本](design/model/versioning.md) | 发版时机和变更记录 |

[术语表](glossary.md)继续承担 designation 与中英对照的现行编辑权；文章约定见[概念文约定](concepts/CONVENTIONS.md)。

## 数据入口

六份正式词表位于 `data/vocab/`：`topics.yaml`、`entities.yaml`、`sources.yaml`、`types.yaml`、`genres.yaml` 和 `forms.yaml`。主题词表由 `data/inputs/topics/` 与核心实现确定生成；其余正式词表按各自设计直接维护。版本记录见[词表变更](../data/vocab/CHANGELOG.md)。

`data/inputs/terminology/glossary-layout.yaml` 仍未启用，仓库没有正式 `data/vocab/terms.yaml`。迁移账本和诊断输出位于 `data/audit/`，只供审计与人工复核。

## 工程入口

| 工程 | 说明 | 常用入口 |
|---|---|---|
| 核心包 | [kb-core](../packages/kb-core/README.md) | `uv run kb-core --help` |
| Obsidian 应用 | [kb-obsidian](../apps/obsidian/README.md) | `uv run kb-obsidian --help` |
| 词表预览 | [kb-vocab-preview](../apps/vocab-preview/README.md) | `uv run kb-vocab-preview` |
| 开发说明 | [开发指南](guides/development.md) | uv workspace、常用命令与目录边界 |
| 整仓检查 | `scripts/` | `uv run python scripts/check-links.py` |

根目录使用统一 uv workspace、`uv.lock` 和 `.python-version`。开发环境的固定版本是 Python 3.13.5，成员包最低支持 Python 3.11。

## 决定入口

已采纳决定只追加不重写。阅读新布局时先看[仓库布局](decisions/monorepo-layout.md)，再看[预览归属](decisions/vocab-preview-location.md)，按主题查看[应用约束](decisions/application-profile-boundary.md)、[工具归属](decisions/obsidian-tool-location.md)、[词表刷新](decisions/obsidian-reference-refresh.md)、[当前阶段](decisions/current-stage-scope.md)和[验证投入](decisions/verification-effort.md)。

迁移前决定中的旧路径按该决定形成时的 Git 基线解释；目录变化不修改原决定正文，也不改变其语义效力。当前位置由本索引与仓库布局决定提供。

## 草案入口

`drafts/` 中的项目文件全部未生效，包括来源治理、术语治理、TBX、划分特征、分面字段、概念组、生活范围、实体类别、模型对象和传播学科范围。阅读、引用、部分实现或迁入新目录都不构成采纳。

## 工作入口

[项目路线](../work/roadmap.md)是当前状态入口，[迁移计划](../work/plans/2026-09-05-monorepo-layout.md)记录本次已批准实施范围。`work/archive/` 保存历史执行材料；其中未勾选的步骤和旧路径只属于当时记录，不自动成为当前待办。
