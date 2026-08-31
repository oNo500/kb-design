# 设计同步计划 (Current Design Synchronization Implementation Plan)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让现行设计准确区分正式规则与数据、已经实现但尚未激活的来源和术语治理能力、未生效草案及后置严格切换。

**Architecture:** 按职责整篇重写现行设计，不把草案规则补进旧文章。第一批收敛来源身份、用途和引用边界，第二批收敛治理与维护职责，第三批收敛主题和内容的现行编辑路径，最后统一入口、摘要和项目路线状态。

**Tech Stack:** Markdown、YAML、Python 3、Git。

**Spec:** [项目路线](2026-08-31-project-roadmap.md)、[当前阶段](../../../design/decisions/current-stage-scope.md)、[验证投入](../../../design/decisions/verification-effort.md)、[来源治理草案](../../../design/drafts/source-governance.md)、[术语治理草案](../../../design/drafts/terminology-governance.md)

## 全局约束

- 只在 `/Users/xiu/code/kb-design` 的 `feat/terminology-governance` 分支执行，不创建 worktree，不修改 `master`。
- 本计划只同步现行设计，不修改任何 `vocab/` 正式数据、迁移账本、schema、脚本、测试、概念文、来源笔记或决定记录。
- 来源治理草案、术语治理草案和 TBX 草案继续未生效；已有 schema、校验器、索引、探测器、生成器、账本和测试只证明能力存在，不能替代草案生效、正式数据应用或发版。
- `vocab/topics.yaml` 是当前正式主题词表和确定性生成物；实际编辑路径是 `scripts/build-topics.py` 及其读取的 `vocab/build/` 输入，不直接修改生成输出。
- `concepts/glossary.md` 继续是当前术语表编辑源；不得创建或激活 `vocab/terms.yaml`，不得建立正式委托或改变其他词表的标签所有权。
- `vocab/entities.yaml`、`vocab/sources.yaml` 继续使用现行结构；六份来源账本和三百四十八条术语账本只作迁移审计，不反向赋予正式效力。
- 来源探测当前只支持固定 transport 夹具，live 明确禁用，且探测器输出与探测 schema 尚未闭合；来源迁移预演的既有账本保留审计效力，但当前冻结输入哈希已经漂移，不能宣称可从现时 HEAD 重新物化。
- 术语生成器、状态转换、正文诊断和维护索引已经实现，但仓库没有正式术语输入、切换状态、义务或消费者；三百四十八条账本只有审计和原所有者去向，不含正式术语身份或状态。
- 现行 `tier`、来源角色、主题状态、稳定 `id`、标签、关系、范围、阈值和版本全部不变；旧 `origin` 只在说明现行数据或未来迁移边界时出现，不借文档同步机械改写。
- 改动涉及一节以上时按目的整篇重写；动笔前在本计划的 ignored 执行目录列出旧节逐项去向，写完逐项核销。
- 当前阶段零自定。普通叙述、来源转录、路径、代码和值不因同步成为项目术语；未登记 designation 不进入定稿。
- 文档任务不使用 TDD。保留的必要门禁是旧节去向、草案效力边界、正式编辑源、相对链接、标题、候选扫描差异、主题数据不变和写集；不设计低价值测试或独立机械复审。
- 每个任务提交说明使用 `[L2]`；不得推送、合并、发版或调用分支收尾流程。

---

### Task 1: 来源关系

**Files:**

- Modify: `design/entities.md`
- Modify: `design/sources-registry.md`
- Modify: `design/hierarchy.md`
- Modify: `design/principles.md`

**Interfaces:**

- Consumes: 当前正式 `vocab/entities.yaml`、`vocab/sources.yaml`，来源治理基础设施和未生效来源草案。
- Produces: 当前来源身份、用途、结构资格、引用语义和未来迁移边界的唯一现行说明。

- [ ] **Step 1: 锁定旧节去向**

在 ignored 执行目录写四篇文章的逐节去向。每节只取“保留”“整节重写”“并入新节”“删除过时说明”之一，并说明去向；不得只列拟改节。

- [ ] **Step 2: 重写来源设计**

整篇重写 `entities.md` 和 `sources-registry.md`。明确实体记录仍保存现行名称、类别、档级、版本和地址，来源记录仍保存现行用途；同时说明新 schema、校验、索引、固定夹具探测、历史预演和义务接口已经存在但未应用到正式数据。不得把迁移账本中的推荐值写成现行值，不得宣称 live 探测、正式索引或当前快照预演已经可用。

- [ ] **Step 3: 重写结构关系**

整篇重写 `hierarchy.md`，保留八个顶层、复制深度、数组和现有来源选择；把 `source`、`match`、来源用途和现行紧缩值写成当前接口，把新的共享引用结构写成后置迁移边界，不使用 `source: self` 冒充实际派生。

- [ ] **Step 4: 重写方法登记**

整篇重写 `principles.md`，逐行保持已登记方法和来源；更新来源治理、断言依据、实际派生、概念映射和复核的导出规则，不新增方法或 designation。

- [ ] **Step 5: 运行定向校验**

运行：

```bash
git diff --check
python3 scripts/check_link_baseline.py
python3 scripts/check-topics.py
python3 scripts/check-terms.py --all
```

预期：格式通过；链接保持已知两项基线；主题仍为零问题且身份计数不变；候选报告只用于人工查看，不因数量非零失败。核对差异只含四个目标文件。

- [ ] **Step 6: 提交来源批次**

```bash
git add design/entities.md design/sources-registry.md design/hierarchy.md design/principles.md
git commit -m "[L2] 现行设计:同步来源关系"
```

### Task 2: 治理维护

**Files:**

- Modify: `design/governance.md`
- Modify: `design/maintenance.md`

**Interfaces:**

- Consumes: Task 1 的来源职责，当前三级决策权、验证投入决定、来源和术语基础设施。
- Produces: 正式效力、管理动作、复核义务、指标和后置激活的统一边界。

- [ ] **Step 1: 锁定旧节去向**

在 ignored 执行目录列两篇文章全部旧节去向。保留三级决策权、零自定、现行维护阈值和只追加审计；明确哪些旧 `basis`、`source`、`match`、`origin`、译名和来源复核说明需要重写。

- [ ] **Step 2: 重写治理规则**

整篇重写 `governance.md`。对象范围中分别列正式数据、未激活基础设施、迁移审计和草案；保留现行 designation 准入与译名规则，明确三百四十八条账本不构成正式准入；写清 schema 或工具完成不改变决策权和效力。

- [ ] **Step 3: 重写维护规则**

整篇重写 `maintenance.md`。保留现行候选、`unassigned`、`self`、来源档级、指标和阈值；加入已实现的来源／术语复核义务接口及其未激活边界；区分固定夹具观察、来源变化、术语变化、正式修改和后置严格切换，不让观察、索引或义务自动改写目标。

- [ ] **Step 4: 运行定向校验**

运行 Task 1 的四条命令。另用 `rg` 确认不存在把 `vocab/terms.yaml`、术语委托或新共享引用结构写成现行正式数据的句子。核对差异只含两个目标文件。

- [ ] **Step 5: 提交治理批次**

```bash
git add design/governance.md design/maintenance.md
git commit -m "[L2] 现行设计:同步治理维护"
```

### Task 3: 主题内容

**Files:**

- Modify: `design/topics.md`
- Modify: `design/content-model.md`
- Modify: `design/writing.md`

**Interfaces:**

- Consumes: Task 1 的来源边界、Task 2 的效力和准入边界、当前主题生成链与术语表所有权。
- Produces: 当前主题与内容编辑路径、现行字段语义和写作时的阶段边界。

- [ ] **Step 1: 锁定旧节去向**

在 ignored 执行目录列三篇文章全部旧节去向，特别登记 `topics.yaml` 的生成路径、旧 `origin`、旧紧缩依据、术语表所有权、内容 `source` 与概念来源的不同职责。

- [ ] **Step 2: 重写主题设计**

整篇重写 `topics.md`。保持七百个概念、二十四个数组、八个顶层、现行字段和生命周期不变；准确说明 `topics.yaml` 是正式生成物、生成输入是编辑源、旧字段仍属当前数据、新 schema 和术语委托尚未激活。

- [ ] **Step 3: 重写内容模型**

整篇重写 `content-model.md`。保持内容字段、六个文档类型、五个体裁、载体值、标识符、生命周期和应用映射五问不变；区分内容单元 `source`、概念 `origin` 旧字段和来源治理共享引用的未来迁移，不改变数据值。

- [ ] **Step 4: 重写写作边界**

整篇重写 `writing.md`，保留四项写作原则和所有现行标点／标题规则；把术语写作规则与当前 `concepts/glossary.md` 所有权、候选扫描只供人工判断及未激活术语基础设施对齐，不采用草案中的未来状态或委托规则。

- [ ] **Step 5: 验证生成不变**

先在 ignored 临时目录连续生成两次主题文件，比较两次结果及当前 `vocab/topics.yaml`。再运行 Task 1 的四条命令。预期三份主题输出逐字节一致，正式数据无差异，目标文件外没有受跟踪改动。

- [ ] **Step 6: 提交主题批次**

```bash
git add design/topics.md design/content-model.md design/writing.md
git commit -m "[L2] 现行设计:同步主题内容"
```

### Task 4: 草案状态

**Files:**

- Modify: `design/drafts/source-governance.md`
- Modify: `design/drafts/terminology-governance.md`
- Modify: `design/drafts/division-characteristics.md`

**Interfaces:**

- Consumes: Tasks 1–3 已同步的现行效力边界和当前已经实现的机器契约。
- Produces: 仍未生效但不再把已完成前置能力写成“未来待建”的治理草案，以及准确的零自定例外状态。

- [ ] **Step 1: 锁定旧节去向**

在 ignored 执行目录列两份治理草案全部旧节去向，并单列划分特征草案开篇状态说明。保留所有尚未满足的语义、生效、正式数据、消费者和发版门禁。

- [ ] **Step 2: 重写来源草案**

整篇重写 `source-governance.md`。保持“草案，未生效”，把 schema、校验、索引、固定夹具探测、迁移审计和义务接口标为已另经决定建立；把正式数据、具体角色、外部状态、真实地址、逐值依据、live 探测、严格切换和发版保留为未完成。不得掩盖探测输出契约和当前预演重放尚未闭合。

- [ ] **Step 3: 重写术语草案**

整篇重写 `terminology-governance.md`。保持现行 glossary 编辑权和草案未生效；把三层 schema、状态校验、三百四十八条审计继承、确定性生成、正文诊断和维护索引标为已建立；把术语准入、概念对应、正式身份、委托、正式数据、切换状态、消费者和发版保留为未完成。

- [ ] **Step 4: 修正例外状态**

整节重写 `division-characteristics.md` 的开篇状态说明，明确它只提出零自定例外，例外尚未开放；正文拟议规则和后续独立复核边界保持不变。

- [ ] **Step 5: 运行定向校验**

运行 Task 1 的四条命令。核对三份草案仍明确未生效，`vocab/terms.yaml` 仍不存在，任何已实现能力都没有被写成具体数据或语义批准。差异只含三个目标文件。

- [ ] **Step 6: 提交草案批次**

```bash
git add design/drafts/source-governance.md design/drafts/terminology-governance.md design/drafts/division-characteristics.md
git commit -m "[L2] 治理草案:同步基础状态"
```

### Task 5: 项目入口

**Files:**

- Modify: `design/README.md`
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `docs/superpowers/plans/2026-08-31-project-roadmap.md`

**Interfaces:**

- Consumes: Tasks 1–4 的现行设计、草案状态、当前正式编辑源、未激活边界和项目路线。
- Produces: 面向读者、会话代理和后续阶段的统一入口；首轮维护成为唯一下一阶段。

- [ ] **Step 1: 锁定旧节去向**

在 ignored 执行目录列三个入口文档全部旧节去向。旧计数只在可由正式文件直接验证且不会与只追加版本记录冲突时保留；否则链接到事实来源。

- [ ] **Step 2: 重写设计索引**

整篇重写 `design/README.md`。现行设计、已采纳决定、未激活基础设施、迁移审计和六份草案分别列出；明确六份现行词表、主题生成输入／输出、当前术语编辑源和未来术语生成配置，不把 Superpowers 计划列为项目设计组成部分。

- [ ] **Step 3: 重写项目入口**

整篇重写 `README.md`。保留应用无关与应用相关两层；更新目录职责和现状，删除易漂移的旧计数，明确当前路线、未激活边界和 Obsidian 后置顺序。

- [ ] **Step 4: 重写会话入口**

整篇重写 `AGENTS.md`。保持它仍是写作与治理摘要；加入迁移账本、候选输出和生成能力不等于正式效力的阶段边界，以及主题生成物和术语表的当前编辑路径；不复制详细 schema 或脚本接口。

- [ ] **Step 5: 更新项目路线**

整节重写项目路线的“执行顺序”：把设计同步标为完成，把首轮维护标为下一阶段；其余顺序、后置门禁和范围排除不变。

- [ ] **Step 6: 运行阶段门禁**

运行：

```bash
git diff --check
python3 scripts/check_link_baseline.py
python3 scripts/check-topics.py
python3 scripts/check-terms.py --all
git status --short
```

再从当前 `HEAD` 连续生成两份主题输出并与正式文件比较。逐项核销执行目录中的旧节去向；检查受跟踪写集恰为本计划十五个现行入口／设计／草案文件和一份项目路线，没有数据、schema、脚本、测试、概念、来源或决定差异。

- [ ] **Step 7: 提交入口批次**

```bash
git add design/README.md README.md AGENTS.md docs/superpowers/plans/2026-08-31-project-roadmap.md
git commit -m "[L2] 项目入口:完成设计同步"
```
