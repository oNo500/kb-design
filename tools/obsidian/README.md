# Obsidian 应用 (Obsidian Application)

`kb-obsidian` 是 `kb-design` 的 Obsidian 配套工具，位于 `tools/obsidian/`，提供新 vault 初始化、词表参考刷新、内容建立、只读校验和派生报告。概念、正式词表、内容模型和治理规则仍以设计仓库的正式编辑源为唯一权威；实际知识内容保存在仓库外的用户 vault。

## 运行方式

本工具需要 Python 3.9+、Git 和 PyYAML。以下源码命令均从本目录 `tools/obsidian/` 运行：

```bash
PYTHONPATH=src python3 -m kb_obsidian --help
```

也可从本目录安装，再使用 `kb-obsidian` 命令：

```bash
python3 -m pip install .
kb-obsidian --help
```

开发时如需可编辑安装，使用 `python3 -m pip install -e .`。普通安装把包放到设计仓库之外时，运行命令需显式传入 `--design-root /path/to/kb-design`。

## 设计来源

工具默认定位自身所在的设计仓库，各命令都保留可选的 `--design-root`。来源目录必须是干净的 Git checkout 根目录；tracked 文件有修改、传入的不是仓库根目录或正式输入校验失败时，命令会失败。运行时路径不写入生成内容。

按[工具归属](../../design/decisions/obsidian-tool-location.md)，设计提交不再使用白名单。每次运行读取实际提交，manifest 记录该提交与输入哈希，不把未提交工作目录当作已提交快照。旧 vault 刷新验证原提交属于当前 Git 历史，并核对清单输入哈希与该提交中的字节；取消白名单不免除来源验证。

Python 包名和命令保持不变，工具版本仍为 `0.1.0`，清单 schema 仍为 `1`。原独立应用仓库保留作迁移备份，实际 vault 不迁入设计仓库；本次迁入不构成发版或正式消费者激活。

## 新库初始化

目标目录必须不存在或为空。初始化不会更新非空 vault，也不会合并或覆盖其中的用户文件。

```bash
PYTHONPATH=src python3 -m kb_obsidian init \
  --output /path/to/new-vault
```

命令创建 `home.md`、用户写集 `inbox/`、`sources/`、`content/`、`indexes/` 和 `attachments/`、`kb/` 正式参考表示、`app/` 受管理文件和最低限度的 `.obsidian/` 配置。受管理 manifest 不把用户内容、报告或 Obsidian 配置声明为受管理知识文件。

## 内容建立

词表变更后的既有 vault 更新见下文“词表刷新”；初始化仍只接受空目标。

以下命令创建一条 `draft` 内容。`--subject` 至少出现一次；`--subject`、`--entity` 和 `--reference` 都可以重复。`--form`、`--level` 和 `--language` 是可选参数，语言默认是 `zh`。

```bash
PYTHONPATH=src python3 -m kb_obsidian new-content \
  --vault /path/to/new-vault \
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

内容保存为 `content/<uuidv4>.md`。成功 JSON 的 `path` 是新文件的绝对路径。文件名承担稳定身份；一级标题、`title` property 和唯一派生 alias 使用同一标题。Quick Switcher 可通过 alias 按标题打开 UUID 文件，Search 和 Bases 用于按 properties 查询，用户不需要记忆 UUID。

## 内容校验

校验只读取 `content/*.md`，不改写或修复内容：

```bash
PYTHONPATH=src python3 -m kb_obsidian validate \
  --vault /path/to/new-vault
```

没有 issue 时，命令向 stdout 写一行排序紧凑 JSON 并返回 0。有 issue 时，stdout 为空，stderr 写一行 `KB_OBSIDIAN_ERROR: <排序紧凑 JSON 摘要>` 并返回 1；摘要包含每个 issue 的 `path`、`field`、`code` 和 `message`。

## 使用报告

报告命令先执行同一内容校验，再用有效内容刷新派生报告：

```bash
PYTHONPATH=src python3 -m kb_obsidian report \
  --vault /path/to/new-vault
```

报告只原子替换 `app/reports/`。`index.md` 与 `validation.md`、`topic-usage.md`、`topic-coverage.md`、`unassigned-topics.md` 是 Obsidian 中的人读导航；`data/validation.json` 与 `data/topic-usage.json` 是同一批结果的机器表示，只供终端和程序读取，不进入人读导航。无效内容不进入正式计数；命令不会修改 `content/`、`kb/`、模板、视图、规则、设计来源或正式数据，也不会根据报告自动返回、修复或切换任何内容。

## 词表刷新

`refresh` 显式更新既有 vault 的词表参考区及清单：

```bash
PYTHONPATH=src python3 -m kb_obsidian refresh --vault /path/to/existing-vault
```

加 `--dry-run` 可只检查和预览变化。命令先验证旧 manifest、祖先提交中的旧版输入与受管理写集，再生成并校验新 `kb/`，检查内容引用和指向参考区的链接。只替换 `kb/` 与 `app/manifest.json`；用户内容、附件、配置及应用模板、视图和规则保持不变，派生报告另由 `report` 更新。

受管理文件有语义修改时拒绝覆盖。Base 仅有 YAML 排版变化、且旧哈希能与原生成模板核实时，保留实际文件并在清单中记录其哈希。发生发布异常时回滚参考区和清单，成功后保留 vault 外备份。两个路径的替换不构成断电或进程被强制终止时的事务保证。

## 命令输出

各命令成功时只向 stdout 写一个排序、紧凑的单行 JSON object，并以 LF 结束。预期的参数、设计源、文件系统或解析错误只向 stderr 写一行以 `KB_OBSIDIAN_ERROR: ` 开头的消息，并返回 1；`--help` 返回 0。

## 应用边界

本应用通过显式 `refresh` 更新非空 vault 的参考区，不自动改写用户内容或配置。内容回流、自动修复、查询日志、社区插件和 Obsidian GUI 自动化未实现。Quick Switcher 的交互、Bases 的实际显示和视觉布局需要在 Obsidian 中人工验收；解析 YAML、JSON 或 Base 文件只证明生成文件合同，不替代 GUI 验收。
