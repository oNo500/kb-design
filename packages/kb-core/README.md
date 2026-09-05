# 核心工程 (KB Core)

`kb-core` 保存应用无关的数据生成、校验、来源与术语维护能力。它读取仓库中的正式数据、生成输入和 schema，不依赖 Obsidian 或其他具体应用。

## 环境准备

从仓库根目录同步整个 workspace：

```bash
uv sync --all-packages --locked
```

仓库 `.python-version` 固定当前开发环境为 Python 3.13.5；根工程与两个成员包的最低版本为 Python 3.11。依赖由根 `uv.lock` 统一锁定。依赖已经缓存且需要离线工作时，可改用 `uv sync --all-packages --locked --offline`；本次迁移验证使用了离线模式。

## 命令入口

从仓库根目录查看完整命令：

```bash
uv run kb-core --help
```

当前入口如下。

| 命令 | 职责 |
|---|---|
| `build-topics` | 从生成输入重建正式主题词表 |
| `check-topics` | 校验正式主题词表及其关系 |
| `check-terms` | 生成 Markdown designation 人工复核报告 |
| `check-sources` | 校验来源与引用结构 |
| `build-source-index` | 生成来源反向索引 |
| `plan-source-migration` | 生成来源迁移预演 |
| `probe-sources` | 对固定夹具执行只读来源探测 |
| `source-model` | 维护来源模式相关产物 |
| `build-terms` | 构建或核对未激活术语视图 |
| `migrate-terms` | 物化或校验术语迁移结果 |

使用 `uv run kb-core <命令> --help` 查看参数。命令使用显式仓库根定位资源，不要求调用者先进入包目录。

`check-sources` 要求显式传入 `--root`，完整 schema 校验面向候选数据或固定测试夹具根目录。正式来源 v2 数据尚未激活，不能把该命令可运行写成现行正式数据已经就绪。

## 数据边界

`data/vocab/` 中只有六份现行正式词表。`build-topics` 可以更新 `data/vocab/topics.yaml`；其他生成、诊断、索引和迁移输出不因命令成功而成为正式数据。

主题生成输入位于 `data/inputs/topics/`。`docs/glossary.md` 继续是 designation 与中英对照的现行编辑源；`data/inputs/terminology/glossary-layout.yaml` 仍未启用，仓库没有正式 `data/vocab/terms.yaml`。迁移账本与复核材料位于 `data/audit/`，只作审计。

## 开发检查

核心测试从仓库根运行：

```bash
uv run python -m unittest discover -s packages/kb-core/tests
```

整仓链接检查仍由根辅助脚本负责：

```bash
uv run python scripts/check-links.py
```
