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

## 来源表示

实体与来源用途只读取带 schema 及版本的新格式；旧字段和紧凑来源引用会报错。项目状态与外部状态分别显示，完整保留多地址、复核、观察、用途资格、外部依据、项目判断与历史记录。角色名不代表已获准，决定 ID 不伪装成不存在的笔记链接。语言依据沿用其独立合同。

## 术语表示

应用按[术语实施结构](../../docs/decisions/term-complete-structure.md)读取可选术语输入。`data/vocab/terms.yaml` 与 `data/vocab/term-cutover-state.yaml` 必须共同存在或共同缺省；只存在一份会失败。存在时从同一干净 Git 快照捕获数据、决定、schema、布局和实现，并调用核心统一校验，核对具体记录、定义来源许可、项目依据、状态、引用及发布授权。

获准概念生成 `kb/terms/<tc-id>.md` 只读参考页；`tm-id` 形式不另建概念页。页内保存语言形式、定义、范围、依据性质和出处，manifest、链接与刷新检查识别术语路径。历史纠正标签只提供查找说明，不代表当前准用；项目依据与外部依据分别显示。术语页不成为内容主题，不建立委托或回流；模型标签没有独立术语概念时不创建该页。

本批完整生成、同一干净隔离快照的临时导出与刷新、manifest、链接和内容保护验收已经通过。[术语发布](../../docs/decisions/term-complete-publication.md)与实际 state 已启用 157 个正式术语概念的只读参考消费，glossary 只读生成；内容消费者、委托与回流没有因此启用。两份术语输入共同缺省的旧快照仍导出原六份词表。外部正式 vault 未列入本轮写集，刷新写集仍为 `kb/` 与 `app/manifest.json`。

## 参考导出

只需独立词表参考 artifact 时，从仓库根调用应用包内的导出模块：

```bash
uv run python -m kb_obsidian.exporter \
  --repo-root . \
  --output /absolute/path/to/new-reference
```

目标必须不存在或为空。仓库内输出只能位于 `output/` 的子目录，也可以显式使用仓库外目录。完整 vault 使用下列 `init` 和 `refresh` 命令，不直接复制独立参考区绕过应用清单。

## 新库初始化

`uv run kb-obsidian init` 初始化默认位置；外部新库使用 `uv run kb-obsidian init --output /absolute/path/to/new-vault`。目标必须不存在或为空，不能用初始化器覆盖既有库。

初始化生成根 `AGENTS.md`、`home.md`、用户目录、正式参考区、应用文件和最低 Obsidian 配置。根规则以 `rule` 类型登记在 manifest，内容、附件、报告与配置不因此成为受管理文件。规则缺失、符号链接或漂移会使内容建立、校验及刷新失败。

旧库未登记根规则时保持原写集；同名用户文件不会自动被接管。refresh 只更新词表参考区和清单，既不新增根规则，也不更新已有规则。旧库需要该入口时，先审阅文件与 manifest 的具体迁移方案，不能直接复制后宣称已完成集成。

## 终端访问

AI 优先用原生 Obsidian CLI 与本地命令读取和搜索；工具无法完成时直接说明并交由用户处理，只有用户明确要求界面检查或操作时才使用 Computer Use。首次先运行 `obsidian vaults verbose`，按批准的绝对路径确认实例。同名 vault 不能只按名称定位；必要时只读核对本机注册信息取得 ID。macOS 本机注册信息位于 `~/Library/Application Support/obsidian/obsidian.json` 的 `vaults` 对象，按 `path` 精确选择其键；不得修改注册信息或根据列表顺序猜测 ID。

以下命令中的 `实际ID` 必须换成本机核实值，不能直接照抄。选库参数放在命令之前，每批操作前确认返回路径：

```bash
obsidian vault=实际ID vault info=path
obsidian vault=实际ID search:context query="原词" path=content limit=10 format=json
obsidian vault=实际ID read path=content/实际UUID.md
obsidian vault=实际ID base:query path=app/views/content.base format=json
```

首次最多读取三个候选；主题搜索使用 `path=kb/topics`，核对 ID、label、scope、上位、数组和来源。UUID 文件通过标题、alias、properties 和正文被找到，命中结果不自动决定正式分类。全量 Base 查询先筛选再进入上下文。

调用方为热路径设 2 秒期限，超时仅串行重试一次；冷启动用独立期限。必须同时检查退出码、stderr、错误文本及预期输出，JSON 完整解析后才能消费，实际路径必须与批准目录相同。本机已观察到错误文本伴随退出码 0，不能只凭退出码继续。失败时停止后续写入，不切换到默认库。

本项目没有新增原生 CLI 包装器，上述检查由调用方执行。新内容仍经过 `kb-obsidian new-content`；普通材料及正文修改服从任务授权，写后校验。AI 不直接更改内容 properties、稳定身份、状态或路径。详见[终端访问决定](../../docs/decisions/obsidian-agent-entry.md)。

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

默认 `output/obsidian/` 只是新的可用位置，本次迁移没有创建该 vault，也没有搬迁或刷新现有外部 `kb-vault`。来源 v2 数据已实施，首批术语参考消费已按 publication 启用；这不表示内容消费者启用，也不构成外部正式 vault 已更新或发版。相关决定见[仓库布局](../../docs/decisions/monorepo-layout.md)、[工具归属](../../docs/decisions/obsidian-tool-location.md)与[词表刷新](../../docs/decisions/obsidian-reference-refresh.md)。
