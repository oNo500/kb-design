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
| `check-terms` | 生成 Markdown designation 人工复核报告；读取经完整验权的正式术语登记 |
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

术语结构与语言依据分别按[术语实施范围](../../docs/decisions/term-infrastructure-scope.md)和[术语依据范围](../../docs/decisions/term-evidence-scope.md)实施；完整记录、有限规则和布局分别见[术语具体采纳](../../docs/decisions/term-data-values.md)、[限定定义许可](../../docs/decisions/term-limited-definition-source-use.md)与[术语实施结构](../../docs/decisions/term-complete-structure.md)。`governance/term_validation.py` 为生成、维护与应用共用入口，分别核对 schema、来源、完整记录采纳、稳定身份、状态历史和发布授权。

定义依据默认拒绝 de-facto／vendor；只有本批六个概念的完整 definition_source_permission 与同一概念的 L3 许可、record grant 精确匹配时例外放行，不改变来源 tier 或其他用途。project basis 只用于内容单元、断言、阈值的概念和定义，以及 assertion、threshold 两个既有英文形式，中文语言依据独立；其他缺外部依据的条目不能套用。

`build-terms build` 和 `build-terms check` 读取显式术语、state、布局与来源索引，先校验全部输入再生成或比较快照和术语表。布局 v2 按概念身份编排，领域未定时 `subject_fields` 可以为空；普通说明、缩写、文献说明、符号和历史纠正标签在布局维护。主题、载体的模型标签仍从原词表与语言采纳输入生成，不创建术语概念或委托。历史标签只用于纠正说明与查找，不自动成为准用形式。

`term-data check` 与 `term-data index` 复用同一校验；索引只定位实际引用，不把提案和历史值当作现行引用，不创建正式义务。`check-terms` 完整核对正式 terms/state，再读取获准现行形式；缺失一半或授权不完整时失败，不回退旧登记来绕过检查。报告仍不批准术语或形成正文违规结论。

在仓库根目录重建已获准的视图：

```bash
uv run kb-core term-data check --root .
uv run kb-core build-source-index --root . --output build/terms/source-reference-index.json
uv run kb-core build-terms build --design-root . \
  --terms data/vocab/terms.yaml --state data/vocab/term-cutover-state.yaml \
  --layout data/inputs/terminology/glossary-layout.yaml \
  --source-index build/terms/source-reference-index.json \
  --snapshot-out build/terms/terms.snapshot.json --glossary-out docs/glossary.md
```

把最后一条的 `build` 改为 `check` 可检查输出漂移；使用 `uv run kb-core term-data index --root .` 生成可清理的维护索引。

## 数据边界

主题输入位于 `data/inputs/topics/`，`build-topics` 重建 `data/vocab/topics.yaml`。本批 157 个正式术语概念与 51 个新增来源已实施，publication 已完成规定验收并生效；这不构成发版。

[术语发布](../../docs/decisions/term-complete-publication.md)与实际 state 已启用术语唯一编辑源及首批参考消费。terms 维护概念、定义和现行形式，`data/inputs/terminology/glossary-layout.yaml` 维护展示，glossary 是完整只读生成页；主题和载体模型标签继续由 topics／forms／adoptions 维护。没有 retained-glossary 编辑源，不把审计账本作为长期生产输入。

迁移审计保留原行、旧值与去向；正式义务、委托、持久正式索引和 TBX 不因本批术语迁移启用。外部正式 vault 写入、合并与发版不在本轮条件式执行范围内。

## 开发检查

核心测试从仓库根运行：

```bash
uv run python -m unittest discover -s packages/kb-core/tests
```

整仓链接检查仍由根辅助脚本负责：

```bash
uv run python scripts/check-links.py
```
