# 开发指南 (Development Guide)

本仓库是 uv workspace。以下命令都从仓库根运行，资源定位不依赖当前工作目录。

## 环境准备

```bash
uv sync --all-packages --locked
```

`.python-version` 固定当前开发环境为 Python 3.13.5；根工程与各成员包的最低版本为 Python 3.11。各成员包共享根 `uv.lock`，应用通过 workspace 依赖使用核心包。依赖已经缓存且需要离线工作时，可改用 `uv sync --all-packages --locked --offline`；本次迁移验证使用了离线模式。

## 核心命令

```bash
uv run kb-core --help
uv run kb-core build-topics
uv run kb-core check-topics
uv run kb-core check-terms
uv run kb-core check-sources --help
```

其他来源与术语维护入口见[核心工程](../../packages/kb-core/README.md)。`build-topics` 会更新正式 `data/vocab/topics.yaml`，运行前须确认修改的是 `data/inputs/topics/` 或核心生成实现。`check-sources` 要求显式 `--root`，完整 schema 校验只用于候选数据或固定测试夹具根目录；正式来源 v2 数据尚未激活。其他诊断与迁移能力也不因运行成功而取得正式数据效力。

## 应用命令

```bash
uv run kb-obsidian --help
uv run kb-obsidian init
uv run kb-obsidian refresh --dry-run
uv run kb-obsidian validate
uv run kb-obsidian report
```

不传目标路径时，应用使用 `output/obsidian/`。`init` 可用 `--output`，后续命令可用 `--vault` 指向外部目录；所有命令保留 `--design-root`。完整参数和写集边界见[Obsidian 应用](../../apps/obsidian/README.md)。

## 实时预览

```bash
uv run kb-vocab-preview
```

浏览器打开 <http://127.0.0.1:8765>，保存 `data/vocab/` 中的文件后页面自动更新。该服务读取未提交的工作区，保持只读；与 Obsidian 的已提交快照要求分开。参数与维护方式见[预览说明](../../apps/vocab-preview/README.md)。

## 整仓检查

按改动范围选择对应测试；跨工程结构调整时运行相关各组，检查共享接口、数据语义和应用写入边界。应用测试使用临时 Git 快照，不操作实际 vault。

```bash
uv run python -m unittest discover -s packages/kb-core/tests
uv run python -m unittest discover -s apps/obsidian/tests -t apps/obsidian
uv run python -m unittest discover -s tests/integration
uv run python -m unittest discover -s apps/vocab-preview/tests
```

```bash
uv run python scripts/check-links.py
```

根 `scripts/` 只保留整仓辅助。业务生成、校验和维护命令分别从 `kb-core` 或 `kb-obsidian` 进入，不再从旧脚本路径执行。

## 目录边界

`output/` 保存持久应用数据，不属于构建清理对象；`build/` 保存可清理的临时产物。两者都由 Git 忽略。正式数据位于 `data/vocab/`，生成输入位于 `data/inputs/`，审计材料位于 `data/audit/`；三者的效力不能互换。

历史决定和 `work/archive/` 按迁移前 Git 基线解释，不为了新路径改写正文。当前位置见[文档索引](../README.md)和[仓库布局](../decisions/monorepo-layout.md)。
