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
| `check-terms` | 生成 Markdown designation 人工复核报告；正式切换后读取经完整验权的术语登记 |
| `check-sources` | 校验来源与引用结构 |
| `build-source-index` | 生成来源反向索引，包含结构化语言依据的来源用途引用 |
| `plan-source-migration` | 生成来源迁移预演 |
| `probe-sources` | 对固定夹具执行只读来源探测 |
| `prepare-source-evidence` | 整理首批离线来源证据与变化项，只供人工审阅 |
| `source-model` | 维护来源模式相关产物 |
| `build-terms` | 经统一术语校验与精确采纳检查构建或核对术语视图 |
| `term-data check`、`term-data index` | 校验术语数据或生成只读维护索引 |
| `migrate-terms` | 物化或校验术语迁移结果 |

使用 `uv run kb-core <命令> --help` 查看参数。命令使用显式仓库根定位资源，不要求调用者先进入包目录。

`check-sources` 要求显式传入 `--root`，来源 v2 数据与严格引用已按[来源收尾](../../docs/decisions/source-completion.md)实施。命令检查结构、引用及采纳范围，不自动启用正式义务或消费者。

## 离线证据

```bash
uv run kb-core prepare-source-evidence
```

当前只处理 `computing ↔ gbt-13745:520` 和 `explanation ↔ diataxis:explanation`，读取现行记录、来源与角色、旧账本，以及已保存的 GB/T 转载清单和 Diátaxis 阅读记录。不联网、不下载，不把阅读笔记升级为原始材料或正式依据。

默认输出到 `build/source-evidence/`。`evidence.md` 展示当前映射、旧结论、材料性质、哈希、章节、行号、原样片段和待核条件；`evidence.json` 保留完整字段。`changes.md` 只展开本次输入变化的对象，`cache.json` 是可丢弃的派生缓存，不能存放人工采纳决定。

第二次运行时，未变化对象复用片段。选定记录、来源、角色、旧账本、材料文件、适用政策或程序实现变化会使相应结果失效；材料缺失会报告缺口，不使用旧片段。缓存不会免除读取和哈希计算，节省的是重复片段处理及人工重新阅读。

`--root /absolute/checkout` 显式选择输入仓库；`--output build/other-evidence` 可选择该仓库 `build/` 下的子目录。正式目录、vault 输出区和符号链接目标不能作为输出；目标若有不属于本工具的文件，会拒绝覆盖。串行运行本命令，不与另一个调用并发替换同一输出。

待核条件来自已批准的首批审查范围。字段存在可以改变“缺失”的提示，但不会自动关闭关系判断、角色批准或其他语义门禁。当前不支持任意材料导入、PDF 解析或正式候选生成；更换检索对象或新增原始材料需要明确其路径、材料性质和定位规则。试用结果见[离线证据验收](../../work/reviews/2026-09-05-offline-source-evidence.md)。

## 术语入口

术语结构与必要取证分别按[术语实施范围](../../docs/decisions/term-infrastructure-scope.md)和[术语依据范围](../../docs/decisions/term-evidence-scope.md)实施。`governance/term_validation.py` 提供生成、维护和应用共用的完整检查：schema、来源引用、稳定身份、状态历史、精确字段采纳及切换授权分别核对。决定 ID 存在不等于覆盖具体值。

`build-terms build` 和 `build-terms check` 读取显式指定的术语、state、布局与来源索引，先校验全部输入再生成或比较快照和术语表。章节按概念 ID 编排，与可空的 `subject_fields` 分开；模型译名继续从主题、载体和原语言采纳输入生成，不创建新的术语概念。

`term-data check` 与 `term-data index` 复用同一校验；索引只定位实际引用，不把历史提案当作当前引用，也不创建正式义务。`check-terms` 在正式 terms/state 存在后核对发布授权并读取获准形式；缺失一半或授权不完整时失败，不退回旧登记来绕过检查。两者均不存在时，现行 Markdown 登记读取继续有效。

当前没有正式 `terms.yaml` 或 `term-cutover-state.yaml`。具体数据、旧登记保留源与完整生成的衔接仍待采纳和完成；入口可运行不等于编辑权已切换。

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
