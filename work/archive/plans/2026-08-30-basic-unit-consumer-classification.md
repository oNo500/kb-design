# 消费者分类实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 对“基本单位”七个待删除形式的当前六百二十三条消费者候选逐条分类、全量独立复审并收敛为人工决策包，同时保持项目正文和正式数据不变。

**Architecture:** 执行链先从冻结的术语审查表刷新当前消费者身份，再按文件整体分成四个等量首轮批次，由四个代理并发读取上下文。四个未参与首轮的新代理对相同全集独立复审；控制器只按五列身份键合并，并机械分流为已关闭、迁移提案和人工判断。英文 `term`、必要新增形式和最终“基本单位”清单另做依据包，全部在迁移前交人决定。

**Tech Stack:** Markdown、Python 3 标准库、TSV、Git、Superpowers 子代理、标准发布机构官方页面与可重复定位的权威文献。

**Spec:** [消费者分类设计](../specs/2026-08-30-basic-unit-consumer-classification-design.md)

## 全局约束

- 在原项目 `/Users/xiu/code/kb-design` 的 `feat/terminology-governance` 分支执行，不创建新 worktree。`master` 必须保持在 `6370e647518f6b98174b84665a0b9392256892d9`，不得在 `master` 上修改。
- 本计划实施已由人在 2026-08-30 批准。批准范围是当前身份刷新、六百二十三条首轮分类、全量独立复审、机械分流、`term` 与必要新增形式的依据整理，以及最终清单提案；不批准项目文件迁移、术语准入、来源改档、草案生效或零自定例外。
- 执行材料全部保存在 `.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/`。该目录由 `.superpowers/sdd/.gitignore` 忽略；`concepts/`、`design/`、`sources/`、`vocab/`、`scripts/`、`AGENTS.md` 和根目录说明均保持只读。
- 本计划只提交计划文档。实施任务不创建 Git 提交，以执行目录中的输入哈希、批次哈希、代理身份和 `progress.md` 检查点形成审计追踪。
- 当前基线上的七个形式及数量是：`domain` 7、`term` 72、内容对象 3、复合概念 1、复合词 3、词 431、领域 106，总计 623。实施开始时必须重新生成；数量或身份出现未解释差异时停止分类，不把计划中的数量当作覆盖新状态的强制值。
- 分类值只允许“字符串误命中”“来源陈述”“实际消费者”和“待人判断”。这些是执行表临时值，不进入正式术语表和设计正文。
- 字符串长度、词界、目录、代码字体、文件类型和出现次数只用于安排阅读顺序，不能自动填写分类。代理必须打开冻结位置的实际上下文后作出判断。
- 首轮和复审都覆盖全部身份，不抽样。复审代理集合与首轮代理集合必须完全不相交；任何记录都不得由首轮代理复审。
- 每个批次原子交付。输出要么含该批全部合法记录，要么不进入汇总表；审查反馈涉及一个批次时，整份批次输出重新生成，不逐行打补丁。
- 控制器只按“形式、语言、小节、原行、位置”五列身份键连接。不得按文件行序、TSV 行号或数组位置覆盖记录。
- 两轮一致的“字符串误命中”和“来源陈述”只在执行产物中关闭；两轮一致的“实际消费者”只进入迁移提案。分歧和任一轮“待人判断”进入人工判断，不增加第三轮投票。
- 英文 `term`、必要新增形式和最终“基本单位”清单始终交人批准，不能由位置分类、出现数量或来源数量自动决定。
- 外部事实只在“形式依据”任务中重新联网核对。优先使用标准发布机构正文或官方页面；PDF 正文难以可靠读取时记录“来源待核实”并寻找可定位的官方 HTML、等同采用文本或更优质替代来源，不在不可解析材料上无限消耗时间。
- 新形式按 `design/governance.md` 的译名阶梯核对。没有直接形式依据、定义依据和必要概念对应依据时只记录缺口，不提出自造译名。
- 每个任务开始和结束都核对 `git rev-parse HEAD` 等于 `input-lock.md` 的冻结提交，并运行 `git diff --quiet HEAD -- .` 与 `test -z "$(git status --porcelain --untracked-files=normal)"`。任一检查失败时停止；忽略目录中的执行产物不构成工作区修改。

## 文件职责

以下文件名固定；实施者不得把同一职责拆散到临时命名文件后失去追踪。

| 文件 | 操作 | 单一职责 |
|---|---|---|
| `.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/global-constraints.md` | 新建 | 复制本计划的权限、分类值域和失败门槛，供每个代理必读 |
| `.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/progress.md` | 新建并整篇重写 | 记录任务状态、代理身份、哈希、审查结论和阻断，不保存语义分类正文 |
| `artifacts/input-lock.md` | 新建并整篇重写 | 记录分支、提交、清洁状态、输入哈希和当前数量 |
| `artifacts/review-current.tsv` | 生成 | 保存刷新消费者列后的三百四十八条完整审查表 |
| `artifacts/handoff-current.tsv` | 生成 | 保存当前六百二十三条五列身份，分类与说明为空 |
| `artifacts/handoff-delta.tsv` | 生成 | 保存历史交接与当前交接的双向身份差异及解释 |
| `artifacts/classification-tools.py` | 新建 | 分批、结构校验、按键合并、代理隔离校验和结果分流 |
| `artifacts/test-classification-tools.py` | 新建 | 对结构工具执行失败先行的单元测试 |
| `artifacts/batch-manifest.tsv` | 新建并整篇重写 | 记录每批阶段、代理、输入输出、条数和 SHA-256 |
| `artifacts/primary-input-01.tsv` 至 `primary-input-04.tsv` | 生成 | 保存四个首轮空白批次 |
| `artifacts/primary-output-01.tsv` 至 `primary-output-04.tsv` | 新建并整篇重写 | 保存四个首轮完整分类批次 |
| `artifacts/primary-all.tsv` | 生成 | 保存按五列键合并的首轮全集 |
| `artifacts/review-input-01.tsv` 至 `review-input-04.tsv` | 生成 | 保存带首轮判断的四个复审批次 |
| `artifacts/review-output-01.tsv` 至 `review-output-04.tsv` | 新建并整篇重写 | 保存四个独立复审批次 |
| `artifacts/review-all.tsv` | 生成 | 保存不覆盖首轮字段的九列复审全集 |
| `artifacts/consistency-index.tsv` | 生成 | 按形式、完整命中行和相邻位置排列双轮判断，不产生建议分类 |
| `artifacts/consistency-review.md` | 新建并整篇重写 | 保存跨形式、完整写法和相邻位置的一致性审查 |
| `artifacts/closed.tsv` | 生成 | 保存两轮一致的误命中和来源陈述 |
| `artifacts/migration-proposal.tsv` | 生成 | 保存两轮一致的实际消费者，不表示迁移已批准 |
| `artifacts/human-judgment.tsv` | 生成 | 保存分类分歧和任一轮待人判断 |
| `artifacts/form-evidence.tsv` | 新建并整篇重写 | 保存 `term` 和每个必要新增形式的直接依据与未读边界 |
| `artifacts/basic-unit-proposal.tsv` | 新建并整篇重写 | 保存保留、删除和新增的最终清单提案，人工决定列为空 |
| `artifacts/human-decision-package.md` | 新建并整篇重写 | 汇总需要人决定的精确对象并链接全部审计产物 |

相对路径 `artifacts/` 均指 `.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/`。

## 数据接口

当前交接表和首轮分类表固定使用以下七列：

```text
形式	语言	小节	原行	位置	候选分类	处理说明
```

独立复审表固定追加两列，不覆盖首轮字段：

```text
形式	语言	小节	原行	位置	候选分类	处理说明	复审分类	复审说明
```

批次清单固定使用以下十列：

```text
阶段	批次	输入文件	输入条数	实施代理	输出文件	输出条数	输入哈希	输出哈希	状态
```

形式依据表固定使用以下十列：

```text
问题类型	候选形式	语言	目标概念	形式依据	定义依据	概念对应依据	依据结论	未读边界	人工问题
```

`问题类型` 只允许 `term` 和“新增形式”；`依据结论` 只允许“有依据”“无依据”和“有冲突”。没有新增形式时，表中仍保留 `term` 行，不创建虚构候选。

最终清单提案固定使用以下八列：

```text
形式	语言	当前动作	拟议动作	依据状态	消费者结果	提案理由	人工决定
```

`人工决定` 在本阶段必须为空。`拟议动作` 只允许 `keep`、`remove`、`add` 和 `defer`；它只是提案，不回写三百四十八条审查表。

## 批次分配

分批工具按位置中的文件路径分组，按“文件命中数降序、路径升序”处理每组，再把整组放入“当前条数最少、批次号最小”的四个批次。批内按五列身份键排序。同一文件不能跨批。

当前基线应生成以下四组；这是分批算法的回归预期，不是语义分类结果。

| 批次 | 条数 | 文件 |
|---|---:|---|
| `01` | 156 | `concepts/vocabulary-construction.md`、`design/topics.md`、`concepts/README.md`、`sources/metadata-standards.md`、`design/principles.md`、`concepts/facet.md`、`concepts/first-principles.md`、`concepts/CONVENTIONS.md`、`scripts/check-terms.py`、`concepts/note-types.md`、`sources/gbt-13745.md`、`concepts/governance.md`、`scripts/build-topics.py`、`vocab/forms.yaml` |
| `02` | 156 | `sources/z39-19.md`、`design/maintenance.md`、`design/governance.md`、`sources/terminology-standards.md`、`design/hierarchy.md`、`concepts/metadata.md`、`README.md`、`design/versioning.md`、`sources/writing-guides.md`、`concepts/classifying-new-subjects.md`、`design/decisions/form-independence.md`、`vocab/build/gbt-13745.json`、`scripts/check-topics.py`、`vocab/genres.yaml` |
| `03` | 156 | `concepts/controlled-vocabulary.md`、`vocab/topics.yaml`、`vocab/build/scope-zh.json`、`sources/iso-25964.md`、`concepts/knowledge-graph.md`、`design/sources-registry.md`、`concepts/concept-group.md`、`vocab/CHANGELOG.md`、`concepts/writing-conventions.md`、`vocab/entities.yaml`、`scripts/lookup-labels.py`、`vocab/build/gbt_en.py`、`vocab/build/extra-arrays.json`、`vocab/types.yaml` |
| `04` | 155 | `design/content-model.md`、`concepts/body-of-knowledge.md`、`concepts/vocabulary-mapping.md`、`design/README.md`、`design/entities.md`、`concepts/vocabulary-hierarchy.md`、`design/drafts/facet-field.md`、`design/writing.md`、`design/decisions/tree-by-discipline.md`、`AGENTS.md`、`design/decisions/borrow-and-analyze.md`、`sources/iso-15489.md`、`design/drafts/concept-groups.md`、`vocab/build/label-lookup.json` |

复审沿用相同身份分组，但输入是 `primary-all.tsv`，实施者必须是四个新的代理。这样可以证明每条身份由不同代理处理，也使复审者能连续读取同一文件。

## 执行顺序

输入冻结先于任何语义判断；结构工具通过测试后才分批；首轮全集合并后才启动复审；复审全集通过后才机械分流；形式依据只研究分流结果实际提出的问题；人工决策包完成后停止，不启动迁移。

---

### 输入冻结

**Files:**

- Read: `/tmp/kb-terminology-glossary-review.tsv`
- Read: `/tmp/kb-extract-glossary-forms.py`
- Read: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/build-basic-unit-handoff.py`
- Read: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/basic-unit-handoff.tsv`
- Create: `global-constraints.md`
- Create: `progress.md`
- Create: `artifacts/input-lock.md`
- Create: `artifacts/review-current.tsv`
- Create: `artifacts/handoff-current.tsv`
- Create: `artifacts/handoff-delta.tsv`

**Interfaces:**

- Consumes: 已关闭 E2 的三百四十八条审查表、消费者提取器、交接生成器、历史交接快照和当前 Git 树。
- Produces: 可重复生成且已解释历史差异的当前六百二十三条身份集。

**Steps:**

- [ ] 运行 `git status --short --branch`、`git rev-parse HEAD` 和 `git rev-parse master`。预期分支为 `feat/terminology-governance`、工作区为空、`master` 为 `6370e647518f6b98174b84665a0b9392256892d9`；把实际功能分支提交写入 `input-lock.md`。
- [ ] 核对四个既有输入的 SHA-256：完整审查表 `8592ccd5545124f6ab0562372e329fbf7fc9e5e02a05f72dc1251536dd770961`，提取器 `121e791bc7e33b7dcab8533a944d3123ffaaacc237d0a227e6c6a4c99439acb9`，交接生成器 `0b0dc7718d04b6ad0462c746b0bf720a6df3c89e32efabca9084edd6b717ee28`，历史交接 `2665233f84719d89084a5c57178b0045531856f05db56215ea62e957ca6475ab`。任一不符时停止并追查来源。
- [ ] 对完整审查表运行 `awk -F'\t' 'NR > 1 {count++; key=$1 FS $2 FS $3 FS $4; if (seen[key]++) dup++; if ($5 == "" && $6 == "" && $7 == "" && $9 == "" && $10 == "") blank++; else if ($5 == "" || $6 == "" || $7 == "" || $9 == "" || $10 == "") half++} END {print "count=" count, "duplicate=" dup+0, "blank=" blank+0, "half=" half+0; exit !(count == 348 && dup == 0 && blank == 0 && half == 0)}' /tmp/kb-terminology-glossary-review.tsv`；预期输出 `count=348 duplicate=0 blank=0 half=0`。
- [ ] 对完整审查表运行 `validate-review` 和 `guard-removals`；两者都应非零退出。`validate-review` 只能有七条 `remove still has consumers`，不得有其他诊断；`guard-removals` 报告的形式必须精确为 `domain`、`term`、内容对象、复合概念、复合词、词和领域。这证明结构规则已通过，而真实删除保护仍精确阻断七个形式。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv .superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/review-current.tsv`。对刷新表重跑完整性、`validate-review` 和 `guard-removals` 三项检查；预期仍为三百四十八条完整记录，且校验器仍只报告相同七个删除阻断。
- [ ] 运行 `python3 .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/build-basic-unit-handoff.py .superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/review-current.tsv .superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/handoff-current.tsv`；当前预期输出 `blockers=7 candidates=623`。
- [ ] 机械检查 `handoff-current.tsv`：表头精确，五列身份无空值，分类与说明均为空，“形式、位置”无重复；每个位置文件和行号存在，原行按大小写折叠后仍含目标形式；七个形式的数量分别为 7、72、3、1、3、431 和 106。
- [ ] 以完整七列行作集合比较，生成 `handoff-delta.tsv`。当前预期旧表删除十一条、现表增加十一条：三条 `CLAUDE.md` 位置对应三条 `AGENTS.md` 位置，`design/README.md` 的八条 `词` 和一条 `领域` 只发生已知行号移动；不得把路径或行号变化静默忽略。
- [ ] 核对刷新表和交接表当前 SHA-256 分别为 `6b5d57da3534dc8d6c769db9e97ae113b6a0009f76925886eb71bcf4a54b79d3` 与 `20445f3e39edffe9e2ce93bd960e80d58abfc9c68e73b4935054d9f033896a90`。若计划提交后的当前树产生不同哈希，先证明差异是否只来自项目文件变化；不能证明时停止。
- [ ] 整篇写入 `global-constraints.md` 和 `progress.md`，记录批准范围、禁止动作、当前提交、五个输入哈希、七类分布和十一对位置差异。后续代理开始前必须先读这两个文件。
- [ ] 请求一个未参与后续分类的新审查者核对输入来源、哈希、当前扫描、历史差异和项目只读状态。Critical 与 Important 问题全部关闭后，才把“输入冻结”记为完成。

---

### 工具测试

**Files:**

- Read: `artifacts/handoff-current.tsv`
- Create: `artifacts/test-classification-tools.py`
- Create: `artifacts/classification-tools.py`
- Create: `artifacts/primary-input-01.tsv` 至 `artifacts/primary-input-04.tsv`
- Create: `artifacts/batch-manifest.tsv`

**Interfaces:**

- Consumes: 冻结的七列空白交接表。
- Produces: 经过失败先行测试的分批、校验、合并、代理隔离和分流工具，以及四个首轮输入。

**Steps:**

- [ ] 整体新建 `test-classification-tools.py`，先写以下测试：合法交接可分成四批；同一文件不会跨批；四批并集与输入五列键精确相同；重复键、空身份、非空预填分类、非法分类、空说明、身份变化、首轮字段被复审覆盖、复审代理复用首轮代理、缺批和三个分流集合不完备都必须失败。
- [ ] 在测试夹具中加入四种分类各一行和两轮组合矩阵，明确派生规则：两轮相同且为误命中或来源陈述进入已关闭；两轮均为实际消费者进入迁移提案；其余组合进入人工判断。断言三个集合互斥且并集等于输入。
- [ ] 运行 `python3 .superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/test-classification-tools.py`；预期因 `classification-tools.py` 尚不存在而失败。把失败输出记入 `progress.md`，证明测试先行。
- [ ] 整体新建 `classification-tools.py`，只使用 Python 3 标准库，并实现七个子命令：`split-primary`、`validate-primary`、`merge-primary`、`split-review`、`validate-review`、`build-consistency-index` 和 `derive-results`。所有 TSV 都用 `csv` 模块以制表符读写，不能用字符串拼接破坏原行中的引号或制表符。
- [ ] `split-primary` 必须按“批次分配”中的确定性算法按文件分组，输出四个七列表；每行分类与说明为空。工具不得读取原行语义、生成分类建议或根据字符串特征分组。
- [ ] `validate-primary` 必须校验表头、五列键、固定值域、非空具体说明和身份集合；说明等于分类值，或只含“明显”“见上下文”“不是消费者”这类无具体写法与语义角色的短语时失败。
- [ ] `merge-primary` 必须从四个已验证输出按五列键连接到冻结交接表，拒绝重复、缺失、新增和键变化；输出按“形式、位置、语言、小节、原行”稳定排序。
- [ ] `split-review` 必须保留首轮七列，把同一文件分配到与首轮相同的四个批次并追加空的“复审分类”“复审说明”。
- [ ] `validate-review` 必须校验九列表头、首轮七列逐字不变、复审值域、非空具体说明、身份全集和 `batch-manifest.tsv` 中首轮代理集合与复审代理集合完全不相交。
- [ ] `build-consistency-index` 必须从冻结项目文件读取每个位置的完整原行，把记录按形式、原行文本、文件和行号稳定排列，并保留两轮字段；它只提供横向阅读顺序，不输出建议或自动改变分类。
- [ ] `derive-results` 必须从已验证复审全集生成 `closed.tsv`、`migration-proposal.tsv` 和 `human-judgment.tsv`；三个输出保留九列审计字段，按固定集合规则分流，拒绝任何遗漏或重叠。
- [ ] 运行全部单元测试；预期通过。再用 `handoff-current.tsv` 运行 `split-primary`，预期批次数为四、条数为 156、156、156 和 155，文件分配与“批次分配”表完全相同。
- [ ] 整体新建只有表头的 `batch-manifest.tsv`，记录四个首轮输入的条数和 SHA-256；实施代理、输出文件、输出条数、输出哈希和状态在原子交付后由控制器整篇重写补齐，分类代理不得并发修改清单。
- [ ] 请求新审查者检查测试是否覆盖所有规格门槛、实现是否只做结构判断、分流是否机械且没有隐藏语义规则。Critical 与 Important 问题涉及实现时，整份工具和测试一并重写后重跑全部测试。

---

### 首轮分类

**Files:**

- Read: `global-constraints.md`
- Read: `progress.md`
- Read: `artifacts/review-current.tsv`
- Read: `artifacts/primary-input-01.tsv` 至 `artifacts/primary-input-04.tsv`
- Read: 冻结提交中四批列出的项目文件
- Create: `artifacts/primary-output-01.tsv` 至 `artifacts/primary-output-04.tsv`
- Modify: `artifacts/batch-manifest.tsv`
- Modify: `progress.md`

**Interfaces:**

- Consumes: 四个空白身份批次、七个形式的当前审查结论和冻结项目上下文。
- Produces: 六百二十三条具有具体上下文说明的首轮分类，不修改输入与项目文件。

**Steps:**

- [ ] 控制器调用 `superpowers:dispatching-parallel-agents`，同时启动四个首轮代理；每个代理只处理一个编号相同的 `primary-input`，四个代理身份必须互不相同。
- [ ] 每个代理先读规格、本计划的“全局约束”“数据接口”和“批次分配”、执行目录的两个约束文件，以及 `review-current.tsv` 中七个形式的定义与依据结论。不得打开其他首轮代理的输出。
- [ ] 对输入中的每条身份，代理打开“位置”指向的冻结文件，至少读取命中行、所属段落或表格和判断所需的相邻小节。固定行窗不足时扩大范围；文件名、目录和代码样式不能代替语义判断。
- [ ] 代理按规格顺序识别实际命中字符串、完整写法、句段话语角色和目标概念用途。较长写法仍承担目标概念作用时记“实际消费者”；准确登记外部来源说法且未作为本库表达时才记“来源陈述”；存在两个合理解释时记“待人判断”。
- [ ] “处理说明”写出该位置中的完整写法和它为何属于所选语义角色。不得只写分类名、词界结论、目录推断、“明显”“见上下文”或“不是消费者”。
- [ ] 每个代理整体新建对应 `primary-output`，保持七列表头、五列身份和批内排序完全不变。所有 155 或 156 行必须一次完整交付，不把中途部分写入汇总表。
- [ ] 控制器对每个输出分别运行 `validate-primary`，再核对输入输出五列键逐项相同。失败批次不登记完成；负责代理必须从该批输入整体重写输出，无法继续时丢弃整批并由新的代理从空白输入重做。
- [ ] 四批均通过后，控制器整体重写 `batch-manifest.tsv`，写入四个首轮代理身份、输入输出条数、输入输出 SHA-256 和“首轮通过”状态；并在 `progress.md` 记录四类分类的批内计数，不解释为最终结论。
- [ ] 核对 `git diff --quiet HEAD -- .` 与普通工作区状态。项目文件有任何变化时停止并丢弃受污染批次，不能把项目改动夹带为分类成果。

---

### 首轮合并

**Files:**

- Read: `artifacts/handoff-current.tsv`
- Read: `artifacts/primary-output-01.tsv` 至 `artifacts/primary-output-04.tsv`
- Read: `artifacts/batch-manifest.tsv`
- Create: `artifacts/primary-all.tsv`
- Create: `artifacts/review-input-01.tsv` 至 `artifacts/review-input-04.tsv`
- Modify: `progress.md`

**Interfaces:**

- Consumes: 四个原子通过的首轮批次。
- Produces: 与冻结身份逐键相同的首轮全集和四个复审输入。

**Steps:**

- [ ] 运行 `merge-primary` 生成 `primary-all.tsv`；预期六百二十三个唯一五列键，无空分类、无空说明、无新增和无遗漏。
- [ ] 分别按形式和分类统计数量，确认各形式总数仍为 7、72、3、1、3、431 和 106；任何数量变化都视为身份连接错误，不通过重排掩盖。
- [ ] 用 `split-review` 生成四个复审输入；预期条数仍为 156、156、156 和 155，首轮七列逐字等于 `primary-all.tsv` 中相同身份，新增两列均为空。
- [ ] 记录 `primary-all.tsv` 和四个复审输入的 SHA-256。锁定后不得回写首轮判断；后续修正必须回到受影响的完整首轮批次，重建全集和所有下游输入。
- [ ] 请求一个未参与首轮的结构审查者核对键连接、四批原子性、说明完整性和无项目修改。该审查只决定能否进入复审，不替代下一任务的逐条语义复审。

---

### 独立复审

**Files:**

- Read: `global-constraints.md`
- Read: `progress.md`
- Read: `artifacts/review-current.tsv`
- Read: `artifacts/review-input-01.tsv` 至 `artifacts/review-input-04.tsv`
- Read: 冻结提交中四批列出的项目文件
- Create: `artifacts/review-output-01.tsv` 至 `artifacts/review-output-04.tsv`
- Modify: `artifacts/batch-manifest.tsv`
- Modify: `progress.md`

**Interfaces:**

- Consumes: 带首轮判断的四个复审批次和同一冻结上下文。
- Produces: 六百二十三条不覆盖首轮字段的第二个完整判断。

**Steps:**

- [ ] 控制器再次调用 `superpowers:dispatching-parallel-agents`，同时启动四个新复审代理。复审代理集合与首轮四个代理集合必须完全不相交；不满足时不发任务。
- [ ] 每个复审代理只处理一个编号相同的 `review-input`。代理可以看到首轮分类和说明，但必须对每条身份重新打开冻结文件上下文，不能只审格式、只读首轮说明或只复核高风险记录。
- [ ] 复审代理使用与首轮相同的四值判据，在“复审分类”和“复审说明”中形成自己的判断。说明必须写出实际完整写法和语义角色；与首轮不同是正常结果，不要求统一。
- [ ] 每个代理整体新建对应 `review-output`，保持首轮七列逐字不变，一次完整填写本批 155 或 156 条复审字段。不得回写首轮列、其他批次或项目文件。
- [ ] 控制器分别运行 `validate-review`，并核对清单中的代理隔离。失败批次整份重做；不能通过修改首轮列使复审看似一致。
- [ ] 四批均通过后，控制器整体重写 `batch-manifest.tsv`，补齐四个复审代理身份、输入输出条数、SHA-256 和“复审通过”状态。清单必须能从每条身份所属文件追溯到两个不同代理。
- [ ] 核对 Git 树和普通工作区仍无变化；发现项目文件修改时停止，不合并受污染输出。

---

### 复审合并

**Files:**

- Read: `artifacts/primary-all.tsv`
- Read: `artifacts/review-output-01.tsv` 至 `artifacts/review-output-04.tsv`
- Read: `artifacts/batch-manifest.tsv`
- Create: `artifacts/review-all.tsv`
- Create: `artifacts/consistency-index.tsv`
- Create: `artifacts/consistency-review.md`
- Modify: `progress.md`

**Interfaces:**

- Consumes: 四个独立复审原子批次和首轮锁定全集。
- Produces: 九列双轮全集及跨记录一致性审查。

**Steps:**

- [ ] 按五列身份键合并四个复审输出为 `review-all.tsv`。运行 `validate-review`，预期六百二十三个唯一身份、九列完整、首轮字段与 `primary-all.tsv` 逐字相同、复审值域合法、代理集合隔离。
- [ ] 运行 `build-consistency-index` 生成 `consistency-index.tsv`。索引只排列原文、两轮分类和说明，不给出建议分类，也不改变 `review-all.tsv`。
- [ ] 请求一个未参与两轮分类的新审查者全量检查聚合索引：同一完整写法在相同语义角色下是否出现无解释的不同分类，来源话语与本库话语是否被混用，较长写法是否因词界被一律误判，以及相邻重复位置是否遗漏上下文差异。
- [ ] 审查者整体写入 `consistency-review.md`，每个问题列出身份键、两轮原判断、实际上下文和问题级别，只报告 Critical、Important 和无阻断结论，不直接改分类。
- [ ] Critical 或 Important 问题交回对应首轮和复审批次。受影响的每份批次整体重写，随后重建 `primary-all.tsv`、四个复审输入、受影响复审输出和 `review-all.tsv`，更新全部哈希后再次全量一致性审查。若上下文仍存在两个合理解释，分类者据实使用“待人判断”；若四值本身不足以表达情况，停止该类记录并返回设计，不临时增加第五种值。
- [ ] 一致性审查无 Critical 或 Important 后，锁定 `review-all.tsv` 的 SHA-256 并在 `progress.md` 记录两轮分类矩阵。锁定后任何变化都使后续分流和决策包失效，必须重建。

---

### 结果分流

**Files:**

- Read: `artifacts/review-all.tsv`
- Create: `artifacts/closed.tsv`
- Create: `artifacts/migration-proposal.tsv`
- Create: `artifacts/human-judgment.tsv`
- Modify: `progress.md`

**Interfaces:**

- Consumes: 已锁定的双轮分类全集。
- Produces: 互斥且完备的三个机械集合，不作迁移或术语决定。

**Steps:**

- [ ] 运行 `derive-results` 生成三个九列表：两轮同为“字符串误命中”或同为“来源陈述”进入 `closed.tsv`；两轮同为“实际消费者”进入 `migration-proposal.tsv`；其他记录进入 `human-judgment.tsv`。
- [ ] 验证三个文件的五列身份交集为空，并集逐键等于 `review-all.tsv`；各文件内部无重复，三者条数之和精确为 623。
- [ ] 生成按形式、首轮分类、复审分类和分流集合的计数矩阵。计数只用于核对与收敛，不把多数分类改写成少数记录的判断。
- [ ] 对 `migration-proposal.tsv` 按文件和相邻位置聚合，只合并展示，不丢失逐行身份与两轮说明。文件仍称“提案”，不生成替换文本、不修改消费者。
- [ ] 对 `human-judgment.tsv` 为每条记录增加决策包中的稳定引用编号；编号只用于展示，五列身份仍是唯一连接键。
- [ ] 请求新审查者从 `review-all.tsv` 重新计算三个集合并逐键比较。任何差异视为机械错误，整体重建三个输出，不人工移动记录。

---

### 形式依据

**Files:**

- Read: `design/governance.md`
- Read: `design/entities.md`
- Read: `design/maintenance.md`
- Read: `sources/terminology-standards.md`
- Read: `sources/iso-25964.md`
- Read: `sources/z39-19.md`
- Read: `artifacts/review-current.tsv`
- Read: `artifacts/migration-proposal.tsv`
- Read: `artifacts/human-judgment.tsv`
- Create: `artifacts/form-evidence.tsv`
- Create: `artifacts/basic-unit-proposal.tsv`
- Modify: `progress.md`

**Interfaces:**

- Consumes: 已复审消费者结果、现行译名阶梯、来源分级和七个形式的当前依据。
- Produces: `term`、实际需要的新增形式和最终清单的依据提案，不批准任何形式。

**Steps:**

- [ ] 从七十二条 `term` 身份中汇总四类位置分类、两轮一致的实际消费者、分歧和典型完整写法。位置分类只回答使用角色，不把 `term` 的高频或低频解释为保留依据。
- [ ] 为 `term` 重新打开当前直接来源、相关术语标准的官方页面或可访问正文，以及能够支持语言形式、定义和概念边界的材料。分别记录英文形式依据、当前定义依据和它与同组中文形式的概念对应依据；三类依据不得互相替代。
- [ ] 从迁移提案逐项判断删除现有形式后是否确实需要一个未登记形式。只有实际消费者无法通过已有且已批准形式表达时才登记新增形式问题；迁移方便、字符串替换或代理偏好不构成新增必要性。
- [ ] 对每个新增问题先写目标概念和所需语言，再按译名阶梯核对：等同采用国际标准的 GB 译名；两个独立的学科权威教材或工具书一致用法；Wikidata 中文标签。前一层成立后停止下探，均不成立时不译。
- [ ] 每个候选分别核对形式、定义和同组对应。官方英文材料不能证明中文形式；标准标题、缩写展开、机器翻译和同表并列不能单独证明概念对应。
- [ ] PDF 教材无法稳定提取或定位时，把材料、页码尝试和不可读范围记入“未读边界”，将该来源标为待核实，并优先查找发布机构 HTML、官方预览、等同采用标准或可定位的权威替代材料。未实际读到的正文不写成依据。
- [ ] 整体写入 `form-evidence.tsv`。至少有一条 `term` 记录；新增形式为零时不造占位行。每个“有依据”必须有标题、链接和可重复定位位置；“无依据”或“有冲突”必须列核对日期、已检材料和未读边界。
- [ ] 整体写入 `basic-unit-proposal.tsv`，逐项列出七个当前形式和每个有直接依据的新增候选。`人工决定` 全部为空；没有足够依据的候选只能 `defer`，不能以建议写法进入 `add`。
- [ ] `term` 的拟议动作、任何 `add`、七个形式的最终保留或删除都保持为人审提案。分类代理和来源代理不得把结论回写 `review-current.tsv` 或 `concepts/glossary.md`。
- [ ] 分别请求两个独立审查者：一个全量复核 `term` 的形式、定义与对应依据；另一个全量复核所有新增候选的必要性、译名阶梯和来源可读边界。Critical 与 Important 反馈涉及一类问题时，整体重写该类依据行和清单提案后再审。

---

### 决策包

**Files:**

- Read: `artifacts/input-lock.md`
- Read: `artifacts/batch-manifest.tsv`
- Read: `artifacts/review-all.tsv`
- Read: `artifacts/closed.tsv`
- Read: `artifacts/migration-proposal.tsv`
- Read: `artifacts/human-judgment.tsv`
- Read: `artifacts/form-evidence.tsv`
- Read: `artifacts/basic-unit-proposal.tsv`
- Create: `artifacts/human-decision-package.md`
- Modify: `progress.md`

**Interfaces:**

- Consumes: 冻结输入、双轮审计、三个分流集合和形式依据。
- Produces: 人可以逐项批准或拒绝的收敛决定包；不产生迁移授权。

**Steps:**

- [ ] 整体新建 `human-decision-package.md`，小节依次为“输入身份”“分类结果”“迁移提案”“判断事项”“英文形式”“新增形式”“清单提案”“已关闭项”和“审计位置”。标题不写数量、字段名或文件名。
- [ ] “输入身份”写冻结提交、七个形式分布、六百二十三条总数和十一对历史位置变化；“分类结果”写两轮分类矩阵、三个集合的数量及其互斥完备验证。
- [ ] “迁移提案”按文件列两轮一致的实际消费者，保留每条稳定身份和两轮说明链接，并明确它们尚未批准、没有替换文本。
- [ ] “判断事项”逐项列分类分歧和任一轮待人判断，展示两轮意见、实际上下文和需要人回答的单一问题，不要求人在六百二十三条已一致记录上重复审查。
- [ ] “英文形式”单列 `term` 的消费者分布、形式依据、定义依据、概念对应依据、未读边界和保留或重建问题；不能用其他七个形式的分类代替该决定。
- [ ] “新增形式”只列已经证明必要性的候选及三类依据；没有合格候选时明确写“本轮没有取得可准入的新增形式”，并保留查无记录。
- [ ] “清单提案”逐项展示 `basic-unit-proposal.tsv` 的当前动作、拟议动作、依据状态和消费者结果，所有人工决定保持空白；要求人明确批准精确清单，不把批准扩展到迁移正文。
- [ ] “已关闭项”只给数量、分类分布和 `closed.tsv` 链接，不把全量低风险记录塞入人审正文；“审计位置”链接首轮、复审、批次清单、一致性审查和输入哈希。
- [ ] 请求一个没有参与分类、复审或形式研究的新审查者进行最终全量审查：六百二十三条是否全部可追溯，三集合是否完备，代理是否隔离，`term` 与新增形式是否有独立依据，人工权限是否被保留，项目文件是否未改。
- [ ] Critical 或 Important 反馈按产物职责返回上游；受影响产物整份重写并重建所有下游文件，不能只改决策包措辞掩盖上游缺口。最终审查无阻断后，锁定全部产物 SHA-256。
- [ ] 运行 `python3 .superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/test-classification-tools.py`，重新运行全部结构校验和三个集合验证，再核对冻结提交、`git diff --quiet HEAD -- .` 与普通工作区清洁状态；全部通过后在 `progress.md` 记为“等待人工决定”。
- [ ] 向人提交决策包及精确问题列表后停止。本阶段不修改项目文件、不回写三百四十八条审查表、不启动消费者迁移，也不调用分支收尾流程。
