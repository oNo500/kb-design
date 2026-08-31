# 首轮维护计划 (First Maintenance Implementation Plan)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:dispatching-parallel-agents for read-only context batches, superpowers:test-driven-development for the generated status behavior, then superpowers:subagent-driven-development for tracked changes. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 完成第一次编辑审核，逐项处理当前候选、`unassigned`、`self`、来源指标和名称线索，并用真实证据校准现行阈值是否需要变化。

**Architecture:** 先从当前正式数据和动态 Markdown 清单重建稳定库存，再由互斥批次逐位置判断名称线索语境；随后按现行维护规则审核实体候选、未标引记录、断言和来源。只有有权限且证据闭合的动作才修改正式对象；本轮若没有动作，只追加指标快照、审核日期、CHANGELOG 审核记录和项目路线状态。

**Tech Stack:** Markdown、YAML、TSV、Python 3、Git。

**Spec:** [维护](../../../design/maintenance.md)、[治理](../../../design/governance.md)、[项目路线](2026-08-31-project-roadmap.md)、[证据阶段](../../../design/decisions/evidence-stage-boundary.md)

## 全局约束

- 只在 `/Users/xiu/code/kb-design` 的 `feat/terminology-governance` 分支执行，不创建 worktree，不修改 `master`。
- 本计划执行现行维护，不使来源治理、术语治理、划分特征、分面字段、概念组或 TBX 草案生效，不恢复正式严格切换。
- 名称线索按精确文件、行、列和上下文逐项阅读。字符串、标题、加粗、引号、出现次数和分类代码不能自动形成 designation、概念、违规或候选记录。
- 线索分类只允许 `not-designation`、`source-transcription`、`registered-form`、`designation-proposal` 和 `needs-human`；这些是 ignored 审查代码，不是项目术语。任何 `designation-proposal` 只进入人工决定包，不写 glossary、词表或正文。
- 17 个实体候选、692 个 `unassigned`、13 个 `self` 断言、31 个来源和 5 个旧 `candidate` 来源角色按稳定 `id` 对账；不得由总数替代逐项身份。
- `basis: self` 与后置共享 `basis` 不能机械互转。归属判断是 L2；没有新的逐项人工决定时，13 个记录保持 `candidate`，不修改 `subjects` 或 `basis`。
- 4 个没有 `self` 的实体候选仍须满足现行引用次数、`scope`、审核四问和决定门禁；应用映射未建立时，不得凭已有来源自动转为 `active`。
- 692 个 `unassigned` 是复制结构中的盲区记录。当前没有内容引用数据，也没有第二次编辑审核；不得批量转正、废弃、删除或解释为术语状态。
- 31 个来源按现行 `tier` 和 `checked` 计算到期；固定夹具、0 个到期或相对链接通过都不能证明真实内容、版本、替代、撤回和地址已经联网复核。
- 5 个旧 `candidate` 来源角色在来源草案生效前保持现状；不得在本轮迁移为 `discovery`。
- 阈值校准只使用本轮可取得的纵向和内容证据。缺少第二次审核、内容引用、应用映射、live 来源观察或治理年审起算点时，相应阈值保持不变，并在审核记录说明证据缺口；不为完成“校准”强行改数字。
- 正式写集最多为 `scripts/build-topics.py`、`tests/test_build_topics_sources.py`、`vocab/topics.yaml`、`vocab/signals.yaml`、`vocab/CHANGELOG.md` 和 `docs/superpowers/plans/2026-08-31-project-roadmap.md`。任何实体、来源、glossary、schema、其他脚本／测试、设计或决定修改都阻断本计划。
- 文档和确定性数据不使用 TDD。高价值门禁只保留身份覆盖、上下文逐项阅读、权限、快照只追加、阈值证据、主题校验、链接基线、名称线索差异和写集；不增加低价值测试或机械独立复审。
- 提交说明使用 `[L2]`，因为本轮形成维护结论并关闭路线阶段；不得推送、合并或发版。

---

### Task 1: 审核库存

**Files:**

- Create ignored: `.superpowers/sdd/2026-09-01-first-maintenance/usage-hits.tsv`
- Create ignored: `.superpowers/sdd/2026-09-01-first-maintenance/usage-review.tsv`
- Create ignored: `.superpowers/sdd/2026-09-01-first-maintenance/object-review.tsv`
- Create ignored: `.superpowers/sdd/2026-09-01-first-maintenance/batch-manifest.tsv`
- Modify tracked: none

**Interfaces:**

- Consumes: 当前 Git Markdown 清单、`concepts/glossary.md`、正式词表、`vocab/signals.yaml` 和现行维护规则。
- Produces: 每个扫描位置和维护对象都有结论的只读审核库存。

- [ ] **Step 1: 冻结输入**

记录 HEAD、计划、维护规则、治理规则、glossary、三份正式数据、signals 和两个检查脚本的 SHA-256。运行 `check-topics.py`、链接基线和 `check-terms.py --all`，保存原始输出；不得使用 `--record`。

- [ ] **Step 2: 导出逐位置线索**

运行：

```bash
python3 scripts/check-terms.py --all --format tsv --output .superpowers/sdd/2026-09-01-first-maintenance/usage-hits.tsv
```

保留文件、行、列、上下文、种类、原文、规范化值、概念 id、严重度和现有结论。按完整位置身份排序，重复身份失败。

- [ ] **Step 3: 并行判断语境**

按文件路径和行范围把全部位置拆成互斥批次，一次派发全部批次。每行必须实际打开当前上下文，只填分类与一条可核对说明；字符串边界、标题类型和文件目录只能安排阅读顺序，不能自动分类。合并后位置身份与 `usage-hits.tsv` 完全相同，无缺失、无新增、无重复。

- [ ] **Step 4: 审核维护对象**

为 17 个实体候选、692 个 `unassigned`、13 个 `self` 断言、31 个来源和 5 个旧来源角色分别建立稳定身份行。每行保存当前位置、现行状态、触发条件、可取得证据、结论、允许动作、阻断原因和决策级别。集合重叠对象分别保存职责，不互相覆盖。

- [ ] **Step 5: 汇总待定项**

只把 `designation-proposal`、`needs-human`、4 个非 `self` 候选的审核缺口、13 个 `self` 归属判断和确实触发的来源／阈值项目列入决定包。没有具体动作的 692 个 `unassigned` 和未到期来源按身份集合关闭，不展开成虚假语义结论。

### Task 2: 维护结论

**Files:**

- Create ignored: `.superpowers/sdd/2026-09-01-first-maintenance/maintenance-conclusions.md`
- Create ignored: `.superpowers/sdd/2026-09-01-first-maintenance/decision-package.md`
- Modify tracked: none

**Interfaces:**

- Consumes: Task 1 全量库存和现行阈值。
- Produces: 可以直接执行、必须保持、条件不足和需要人决定的精确结论。

- [ ] **Step 1: 核对触发条件**

逐项判断候选总数、节点候选、节点 `self`、“其他”下位、顶层未标引、来源到期、来源新版、链接存活、引用次数、过度使用、治理年审和首次阈值校准。每项必须写当前证据、缺失证据、是否触发和允许动作。

- [ ] **Step 2: 校准阈值**

对维护表中每个“本库”数字给出“保持”或“提议修改”。保持也必须说明样本为什么支持保持或为什么证据不足而不得修改；提议修改必须给真实数据影响和 L2 决定请求。术语接口没有现行阈值，不进入本轮校准。

- [ ] **Step 3: 形成决定包**

决定包只列会改变正式结果的项目。每项包含稳定身份、当前值、依据、建议、替代选项、影响文件、错误代价和决策级别；不得把“继续保持候选”“无法取得引用数据”包装成必须修改的决定。

- [ ] **Step 4: 阻断检查**

任何 designation 准入、概念归属、状态提升、角色迁移、阈值改变、删除、来源改档或发版没有精确人工授权时，正式对象写集保持为空。若决定包有此类开放项，Task 3 只记录审核和未执行边界，不应用开放项。

### Task 3: 状态生成

**Files:**

- Modify: `tests/test_build_topics_sources.py`
- Modify: `scripts/build-topics.py`
- Generate: `vocab/topics.yaml`

**Interfaces:**

- Consumes: Task 2 锁定的 58 个有直接下位且仍为 `unassigned` 的稳定 id，以及现行“有下位即可 `active`”规则。
- Produces: 生成器按最终层级确定这些记录状态，正式主题输出只有精确 58 个 `status` 发生变化。

- [ ] **Step 1: 写入失败测试**

在现有真实生成器测试中增加一个行为：生成结果中不得存在仍为 `unassigned` 的父节点。测试从完整临时生成结果取得反向 `broader` 集合，断言集合为空；它防止删除状态提升逻辑后再次出现本轮 58 项缺陷，不硬编码实现函数。

- [ ] **Step 2: 运行 RED**

运行：

```bash
python3 -m unittest tests.test_build_topics_sources -v
```

预期新增测试失败，准确报告 58 个仍为 `unassigned` 的父节点；既有依据保持测试继续通过。测试必须因生成器缺少状态提升而失败，不得因导入、路径或夹具错误失败。

- [ ] **Step 3: 实现最小状态提升**

在所有概念、层级和多层级关系建立完成后、输出前，从最终 `broader` 反向集合取得父节点。只把其中仍为 `unassigned` 的记录改为 `active`；顶层现有 `active` 不重复修改，其他状态不改变。更新生成文件的版本注释，使其不再声称除八个顶层外全部未标引；版本 id 和日期不变，本任务不发版。

- [ ] **Step 4: 运行 GREEN**

运行同一 unittest，预期全部通过且输出无警告。随后在两个独立临时根连续生成，预期逐字节一致。

- [ ] **Step 5: 重建并核对正式输出**

从生成输入重建 `vocab/topics.yaml`。逐项证明：变化身份恰为 Task 2 的 58 个 id；全部由 `unassigned` 变为 `active`；状态总数为 66／634；除 `status` 和版本注释外的概念字段及全部数组逐项不变；`check-topics.py` 返回零问题。

- [ ] **Step 6: 提交状态批次**

```bash
git add tests/test_build_topics_sources.py scripts/build-topics.py vocab/topics.yaml
git commit -m "[L1] 主题维护:批准有下位记录"
```

### Task 4: 审核记录

**Files:**

- Modify: `vocab/signals.yaml`
- Modify: `vocab/CHANGELOG.md`
- Modify: `docs/superpowers/plans/2026-08-31-project-roadmap.md`

**Interfaces:**

- Consumes: Tasks 1–2 的全量审核、开放决定包和 Task 3 已执行的 58 个 L1 动作。
- Produces: 第一次编辑审核的只追加快照、审核记录和下一阶段路线。

- [ ] **Step 1: 追加指标快照**

从干净 HEAD 运行 `python3 scripts/check-topics.py --record` 恰好一次。确认只在 `snapshots` 末尾追加 2026-09-01 当前指标，反映 66 个 `active` 和 634 个 `unassigned`，不修改旧快照；把 `last_candidate_review` 从 null 设为 `2026-09-01`，`governance_reviewed` 保持 null。

- [ ] **Step 2: 追加维护记录**

只在 CHANGELOG 当前版“治理”节末尾追加 2026-09-01 首轮维护记录：审核集合、58 个状态动作、保持项、阈值校准结论、73 个名称形式、13 个归属、4 个候选接受条件和后置证据边界。明确状态批次尚未取得 L3 发版决定；不得改旧条目或重新描述整个词表。

- [ ] **Step 3: 更新项目路线**

整节重写项目路线的“执行顺序”：首轮维护标为当前范围完成，草案复核标为下一阶段；其余顺序和后置门禁不变。

- [ ] **Step 4: 运行阶段门禁**

运行：

```bash
git diff --check
python3 scripts/check_link_baseline.py
python3 scripts/check-topics.py
python3 scripts/check-terms.py --all
git status --short
```

确认第二次不带 `--record` 的主题检查不会修改 signals；当前快照与脚本输出一致；旧快照字节保持；本任务写集恰为三份允许文件；实体、来源和 glossary 字节不变。整个计划的六文件写集与各任务提交边界一致。

- [ ] **Step 5: 提交维护记录**

```bash
git add vocab/signals.yaml vocab/CHANGELOG.md docs/superpowers/plans/2026-08-31-project-roadmap.md
git commit -m "[L2] 首轮维护:记录审核结论"
```
