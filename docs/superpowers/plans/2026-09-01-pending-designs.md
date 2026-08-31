# 待定设计计划 (Pending Designs Implementation Plan)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:dispatching-parallel-agents for four independent evidence reviews, then superpowers:subagent-driven-development for project-native drafts and shared design synchronization. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为生活范围、实体类别、大语言模型归属和传播范围分别形成有概念依据、项目问题、影响与生效条件的项目原生草案，并关闭原路线中的待定设计阶段。

**Architecture:** 四个只读证据复核并行消费现有研究材料与当前仓库；一个整合任务分别写四份未生效草案，不合并决定。共享层级文随后整篇重写，修正已核 CS2023 Security 数量并只登记仍未生效的设计入口；最后同步设计索引和项目路线。

**Tech Stack:** Markdown、YAML、Python 3、Git；外部事实只使用标准发布机构、官方规范、官方分类或原始论文。

**Spec:** [项目路线](2026-08-31-project-roadmap.md)、[主题设计](../../../design/topics.md)、[实体设计](../../../design/entities.md)、[层级结构](../../../design/hierarchy.md)、[治理](../../../design/governance.md)

## 全局约束

- 只在 `/Users/xiu/code/kb-design` 的 `feat/terminology-governance` 分支执行，不创建 worktree，不修改 `master`。
- 四项分别设计、分别结论。相同文件影响只在共享同步阶段合并写入，不把范围、实体模型、概念归属和传播领域合成一个决定。
- 既有研究报告只作材料索引；本轮必须重新打开当前正式数据、现行设计和报告引用的官方材料。具体页面、版本或学科范围若不稳定且会改变结论，实际联网核对；收费／不可读正文标未读，不猜。
- 外部分类、论文、规范或产品文档只支持其自身概念边界，不自动成为项目来源用途、映射、上位概念、实体类别、字段或范围决定。
- 当前八个顶层和按学科建树的决定继续生效。健康、个人理财、旅行等生活内容是否纳入是 L3 范围决定；本计划不得新增顶层、修改范围、生成输入或正式主题数据。
- 实体 `kind` 继续取已登记外部类。类别、载体、主题归属、来源身份、产品系列和具体对象分别判断；不能用目录、名称后缀、厂商、模型能力或现有字符串自动决定。
- 大语言模型须分别判断概念类、模型家族、版本化模型、产品和软件实体；归属、多个上位、designation、`id`、`basis`、`source` 和 `match` 都不得从“LLM”字符串或产品文档目录自动生成。
- 传播领域须区分完整学科、专业实践、技术写作、产品信息、结构化写作和内容类型；DITA、IEEE PCS、ISO／IEC 规范、NCES CIP 和 GB/T 13745 的对象与用途不得混用。
- 四份输出均为项目草案、未生效。没有精确人工决定时，不修改正式概念、实体、标签、范围、关系、来源、内容类型、生成器、schema 或版本。
- 当前 73 个开放 designation 不在本计划中批量准入。四份草案拟采用的名称必须有直接形式依据；没有合格形式时用描述性问题标题，并把名称决定保留为 L2 门禁。
- `design/hierarchy.md` 的 CS2023 Security 知识单元数按官方最终报告和正式生成输入修正为 7。因为该事实出现在多个小节，整篇重写层级文并逐节核销；除事实修正和草案入口边界外，现行树、来源选择、数量、id、数组和规则不变。
- 正式写集最多为四份新草案、`design/hierarchy.md`、`design/README.md` 和 `docs/superpowers/plans/2026-08-31-project-roadmap.md`。若确需同步其他现行设计，先记录计划缺口，不顺手打补丁。
- 文档任务不使用 TDD。高价值门禁只保留外部概念对应、名称依据、范围／归属权限、正式数据不变、旧节去向、链接、候选诊断、主题校验和写集；不增加低价值测试或机械复审。
- 提交说明使用 `[L2]`；不得推送、合并、发版或使草案生效。

---

### Task 1: 独立证据

**Files:**

- Create ignored: `.superpowers/sdd/2026-09-01-pending-designs/life-review.md`
- Create ignored: `.superpowers/sdd/2026-09-01-pending-designs/entity-review.md`
- Create ignored: `.superpowers/sdd/2026-09-01-pending-designs/llm-review.md`
- Create ignored: `.superpowers/sdd/2026-09-01-pending-designs/communication-review.md`
- Modify tracked: none

**Interfaces:**

- Consumes: 当前项目、四份既有研究报告及其官方材料。
- Produces: 四项独立的概念边界、项目选择、推荐、替代、不采用后果、影响和权限门禁。

- [ ] **Step 1: 复核生活范围**

核对健康、个人／家庭理财、旅行／旅游与现行八学科顶层、既有排除和任务记录的关系。分别给出保持范围、按学科扩大范围和改变顶层划分三类路径；不能把三个主题合成天然共同根。推荐必须说明官方全文未读、真实消费者和内容样本边界。

- [ ] **Step 2: 复核实体类别**

核对现行 61 个实体的 `kind`、`form`、`subjects`、`vendor`、来源实体和外部类依据；区分类别、载体、归属和产品关系。列出错误或含糊样本，但没有逐项 L2 决定时不改数据。形成可供未来整篇实体设计使用的模型边界。

- [ ] **Step 3: 复核大模型归属**

核对“large language model”的概念和形式依据、当前主题树、AI／ML／NLP 外部结构，以及现有组织、产品和软件实体。分别提出概念类、模型家族、具体模型版本、应用产品的记录位置和多重归属选项；没有概念对应与 designation 决定时不新增记录。

- [ ] **Step 4: 复核传播范围**

核对技术传播、技术写作、专业沟通、产品信息、DITA 技术内容类型和现行传播学分支。判断是在现有 `communication-studies` 范围内补充下位还是改变范围；同步记录 CS2023 Security 7 项官方事实，但不让它决定传播模型。

- [ ] **Step 5: 报告门禁**

每份报告分别列官方依据、未读边界、当前数据、名称依据、项目问题、2–3 个方案、推荐、替代、不采用后果、影响文件、L2／L3 门禁和错误代价；四份不得互相代替决定。受跟踪写集保持为空。

### Task 2: 项目草案

**Files:**

- Create: `design/drafts/life-scope.md`
- Create: `design/drafts/entity-categories.md`
- Create: `design/drafts/large-language-models.md`
- Create: `design/drafts/communication-scope.md`
- Create ignored: `.superpowers/sdd/2026-09-01-pending-designs/conclusions.md`
- Create ignored: `.superpowers/sdd/2026-09-01-pending-designs/decision-package.md`

**Interfaces:**

- Consumes: Task 1 四份独立报告。
- Produces: 四份项目原生草案和四项独立决定边界。

- [ ] **Step 1: 核对名称与身份**

只使用已有合格形式依据的标题和对象名称。没有直接依据的中文或英文形式不得因文件名、研究报告或用户问题自动准入；草案用描述性问题标题并在名称门禁中记录候选。

- [ ] **Step 2: 写生活范围草案**

写明现行范围、三个主题分别的边界、重叠、选择路径、推荐、不采用后果、完整借入影响和精确 L3 决定。没有范围决定时推荐保持现状，不预设顶层、来源或记录数量。

- [ ] **Step 3: 写实体类别草案**

写明外部类、载体、主题归属、产品／系列／版本和来源实体的职责；说明当前数据疑虑、逐项复核方式、迁移影响和 L2／L3 门禁。不创建新 `kind`、默认类或数据迁移。

- [ ] **Step 4: 写大模型草案**

写明概念类、模型家族、具体模型、产品和软件实体分层；列 AI／ML／NLP 归属方案、推荐、同一身份多处检索方式、designation 与数据门禁。不创建占位概念、模型实体或映射。

- [ ] **Step 5: 写传播范围草案**

写明学科、专业实践、技术写作、产品信息、结构化写作和内容类型分工；列现行传播学落点、DITA 和外部体系角色、推荐、不采用后果及 L2／L3 门禁。不修改内容类型或实体归属。

- [ ] **Step 6: 提交四份草案**

四份均以“状态：草案，未生效”开头，列独立生效条件且无未经授权的 L3 结论。运行链接、候选和写集门禁后提交：

```bash
git add design/drafts/life-scope.md design/drafts/entity-categories.md design/drafts/large-language-models.md design/drafts/communication-scope.md
git commit -m "[L2] 待定设计:新增四项项目草案"
```

### Task 3: 共享同步

**Files:**

- Modify: `design/hierarchy.md`
- Modify: `design/README.md`
- Modify: `docs/superpowers/plans/2026-08-31-project-roadmap.md`

**Interfaces:**

- Consumes: Task 2 四份草案和当前正式结构。
- Produces: 准确的现行层级、草案索引和下一阶段路线。

- [ ] **Step 1: 锁定层级旧节去向**

列出 `design/hierarchy.md` 全部旧节去向。整篇重写时保留现行八个顶层、来源选择、复制深度、数组、id、数量和待定归属；只把 CS2023 Security 改为 7，并把四份草案作为未生效问题入口。

- [ ] **Step 2: 重写层级设计**

整篇重写 `design/hierarchy.md`，逐项核销旧内容。不得把四项草案推荐写成现行范围、实体类别、模型归属或传播节点；不得修改正式生成输入或数据。

- [ ] **Step 3: 重写设计索引**

整篇重写 `design/README.md`，登记四份新草案并保持现行设计、已采纳决定、未激活基础、迁移审计和既有草案边界；更新草案数量说明，不把 Superpowers 报告列为项目设计。

- [ ] **Step 4: 更新项目路线**

整行同步原始目标第 7 项和“执行顺序”：四项设计标为当前范围完成并列出开放决定，应用映射成为下一阶段；后置严格激活与 TBX 边界不变。

- [ ] **Step 5: 运行阶段门禁**

运行：

```bash
git diff --check
python3 scripts/check_link_baseline.py
python3 scripts/check-topics.py
python3 scripts/check-terms.py --all
git status --short
```

核对正式数据、生成器、schema、测试和决定零差异；四份草案均未生效；Security 两处均为 7；层级旧节有去向；路线下一阶段为应用映射。

- [ ] **Step 6: 提交共享同步**

```bash
git add design/hierarchy.md design/README.md docs/superpowers/plans/2026-08-31-project-roadmap.md
git commit -m "[L2] 项目设计:同步待定设计边界"
```
