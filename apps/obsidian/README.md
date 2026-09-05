# Obsidian 应用 (Obsidian Application)

`kb-obsidian` 是本 monorepo 的 Obsidian 应用，提供新 vault 初始化、词表参考刷新、内容建立、只读校验和派生报告。概念、正式词表、内容模型和治理规则仍以仓库中的现行编辑源为权威；应用输出不回流，也不取得项目效力。

## 环境准备

从仓库根目录同步 workspace：

```bash
uv sync --all-packages --locked
uv run kb-obsidian --help
```

仓库 `.python-version` 固定当前开发环境为 Python 3.13.5，应用最低支持 Python 3.11。应用通过 workspace 依赖使用 `kb-core`，不需要在本目录单独安装。依赖已经缓存且需要离线工作时，可改用 `uv sync --all-packages --locked --offline`；本次迁移验证使用了离线模式。

## 路径规则

不传目标路径时，命令使用仓库内的 `output/obsidian/`。该目录保存持久 vault，由 Git 忽略，不属于可清理的 `build/` 临时产物。

`init` 可用 `--output /absolute/path` 指定其他新 vault；`refresh`、`new-content`、`validate` 和 `report` 可用 `--vault /absolute/path` 指定既有 vault。显式路径优先，允许位于仓库外。所有命令保留 `--design-root /path/to/kb-design`，用于显式指定设计来源。

设计来源必须是干净的 Git checkout 根目录。应用核对正式输入，以及该提交中的导出实现与核心依赖；来源不完整、文件未提交或校验失败时，命令失败。manifest 记录实际提交与输入哈希，不把未提交工作目录当作已提交快照。

本版本使用 `data/vocab/` 输入路径，不自动转换迁移前采用 `vocab/` 路径的 vault 清单。既有外部 `kb-vault` 保持原样，其迁移另行安排。

## 参考导出

只需独立词表参考 artifact 时，从仓库根调用应用包内的导出模块：

```bash
uv run python -m kb_obsidian.exporter \
  --repo-root . \
  --output /absolute/path/to/new-reference
```

目标必须不存在或为空。仓库内输出只能位于 `output/` 的子目录，也可以显式使用仓库外目录。完整 vault 使用下列 `init` 和 `refresh` 命令，不直接复制独立参考区绕过应用清单。

## 新库初始化

默认初始化仓库内 vault：

```bash
uv run kb-obsidian init
```

显式初始化外部 vault：

```bash
uv run kb-obsidian init --output /absolute/path/to/new-vault
```

目标目录必须不存在或为空。命令创建 `home.md`，用户写集 `inbox/`、`sources/`、`content/`、`indexes/` 和 `attachments/`，正式参考表示 `kb/`，应用文件 `app/`，以及最低限度的 `.obsidian/` 配置。受管理 manifest 不把用户内容、报告或 Obsidian 配置声明为受管理知识文件。

## 内容建立

以下命令在默认 vault 中创建一条 `draft` 内容。`--subject` 至少出现一次；`--subject`、`--entity` 和 `--reference` 可以重复。`--form`、`--level` 和 `--language` 可选，语言默认是 `zh`。

```bash
uv run kb-obsidian new-content \
  --title '内容标题' \
  --type explanation \
  --genre analysis \
  --subject artificial-intelligence \
  --subject security \
  --entity openai \
  --reference gbt-13745 \
  --form narrative-text \
  --level understand \
  --language en
```

外部 vault 在命令中增加 `--vault /absolute/path/to/vault`。内容保存为 `content/<uuidv4>.md`。文件名承担稳定身份；一级标题、`title` property 和唯一派生 alias 使用同一标题，人的检索不依赖 UUID 文件名。

## 内容校验

校验只读取 `content/*.md`，不改写或修复内容：

```bash
uv run kb-obsidian validate
```

没有 issue 时，命令向 stdout 写一行排序紧凑 JSON 并返回 0。有 issue 时，stdout 为空，stderr 写一行 `KB_OBSIDIAN_ERROR: <排序紧凑 JSON 摘要>` 并返回 1；摘要包含每个 issue 的 `path`、`field`、`code` 和 `message`。

## 使用报告

报告命令先执行同一内容校验，再用有效内容刷新派生报告：

```bash
uv run kb-obsidian report
```

报告只原子替换 `app/reports/`。`index.md`、`validation.md`、`topic-usage.md`、`topic-coverage.md` 和 `unassigned-topics.md` 是 Obsidian 中的人读导航；`data/validation.json` 与 `data/topic-usage.json` 是机器表示。无效内容不进入正式计数，命令不修改用户内容、参考区、模板、视图、规则、设计来源或正式数据。

## 词表刷新

以下命令显式更新默认 vault 的词表参考区与清单：

```bash
uv run kb-obsidian refresh
```

加 `--dry-run` 只检查并预览变化；外部 vault 增加 `--vault /absolute/path/to/vault`。命令先验证旧 manifest、祖先提交中的旧版输入与受管理写集，再生成并校验新 `kb/`，检查内容引用和指向参考区的链接。

刷新只替换 `kb/` 与 `app/manifest.json`。用户内容、附件、配置、模板、视图和规则保持不变，派生报告另由 `report` 更新。受管理文件发生语义修改时拒绝覆盖；发布异常时回滚参考区和清单。

## 命令输出

各命令成功时只向 stdout 写一个排序、紧凑的单行 JSON object，并以 LF 结束。预期的参数、设计来源、文件系统或解析错误只向 stderr 写一行以 `KB_OBSIDIAN_ERROR: ` 开头的消息，并返回 1；`--help` 返回 0。

## 应用边界

应用不自动改写用户内容或配置，不自动返回、修复或切换任何内容。内容回流、自动修复、查询日志、社区插件和 Obsidian GUI 自动化未实现。Quick Switcher 的交互、Bases 的实际显示和视觉布局仍需在 Obsidian 中人工验收；解析 YAML、JSON 或 Base 文件只证明生成文件合同。

默认 `output/obsidian/` 只是新的可用位置，本次迁移没有创建该 vault，也没有搬迁或刷新现有外部 `kb-vault`。应用存在和命令可运行仍不构成正式消费者、来源或术语激活，也不构成发版。相关决定见[仓库布局](../../docs/decisions/monorepo-layout.md)、[工具归属](../../docs/decisions/obsidian-tool-location.md)与[词表刷新](../../docs/decisions/obsidian-reference-refresh.md)。
