# 草案复核计划 (Existing Drafts Review Implementation Plan)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:dispatching-parallel-agents for the three independent reviews, then superpowers:subagent-driven-development for any tracked rewrites. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 分别核对划分特征、分面字段和手工概念组的概念依据、真实需求、现行数据影响与生效条件，并让每份草案得出独立结论。

**Architecture:** 三个只读复核并行消费各自草案和既有官方材料预核；控制器只合并共同效力边界，不合并三份决定。确有语义冲突的草案按目的整篇重写，依据不足或触发未出现的草案继续未生效；最后只更新项目路线。

**Tech Stack:** Markdown、YAML、Python 3、Git；必要外部核对只使用标准发布机构或官方材料。

**Spec:** [项目路线](2026-08-31-project-roadmap.md)、[治理](../../../design/governance.md)、[层级结构](../../../design/hierarchy.md)、[来源治理草案](../../../design/drafts/source-governance.md)、[术语治理草案](../../../design/drafts/terminology-governance.md)

## 全局约束

- 只在 `/Users/xiu/code/kb-design` 的 `feat/terminology-governance` 分支执行，不创建 worktree，不修改 `master`。
- 三份草案具有独立身份：划分特征、分面字段和手工概念组分别复核、分别结论，不用一个推荐替代三个决定。
- 既有预核报告可作为已读材料索引，但本轮必须重新打开当前草案、现行设计和受影响正式数据；旧计数、旧字段和旧结论不得直接继承。
- 外部概念只由标准发布机构、W3C、NISO 或其他官方材料支持；收费／脚本不可读正文继续标未读，不用摘要、类名、XSD 或搜索结果猜正文。
- 外部材料只支持概念边界，不自动决定项目字段、状态、基数、周期、阈值、名称、成员、消费者或生效。
- 当前来源和术语治理草案仍未生效。`basis`、`source`、`match`、designation 准入、术语委托和复核义务不能由三份旧草案另定义一套接口。
- 划分特征的零自定例外尚未开放；`candidate`、草案、示例、`basis: self` 或“分析层”不能取得试用资格。若草案继续提出例外，须明确例外对象、限制和 L3 决定，不得把它写成现行权限。
- 分面字段只有真实查询和实际概念集合试标能够触发；示例查询、零计数、目录和主题分支不能自动批准字段或分面。
- 手工概念组只有真实多项目、多角色或专题消费者能够触发；主题分支、来源数组、分面结果和映射派生视图可以满足的集合不建立手工组。
- 现行主题树、700 个概念、24 个数组、66／634 状态、实体、来源、glossary、schema、脚本、测试、决定和版本全部不修改。
- 正式写集最多为 `design/drafts/division-characteristics.md`、`design/drafts/facet-field.md`、`design/drafts/concept-groups.md` 和 `docs/superpowers/plans/2026-08-31-project-roadmap.md`。没有语义缺陷的草案保持字节不变。
- 草案生效、零自定例外、正式字段、正式文件、删除非候选对象和发版都是 L3 或另有精确门禁。本计划只可形成提案和继续草案结论，不能用用户的一般执行授权替代精确生效决定。
- 文档任务不使用 TDD。高价值门禁只保留概念对应、真实触发、职责冲突、效力、旧节去向、相对链接、候选诊断和写集；不增加低价值测试或重复机械复审。
- 提交说明使用 `[L2]`；不得推送、合并或发版。

---

### Task 1: 独立复核

**Files:**

- Create ignored: `.superpowers/sdd/2026-09-01-existing-drafts-review/division-review.md`
- Create ignored: `.superpowers/sdd/2026-09-01-existing-drafts-review/facet-review.md`
- Create ignored: `.superpowers/sdd/2026-09-01-existing-drafts-review/groups-review.md`
- Modify tracked: none

**Interfaces:**

- Consumes: 当前三份草案、现行规则、正式数据和各自既有预核材料。
- Produces: 每份草案独立的依据矩阵、冲突、真实触发、生效门禁和推荐结论。

- [ ] **Step 1: 冻结输入**

记录 HEAD、三份草案、治理、层级、主题、来源／术语草案、相关概念文、正式主题／来源数据和三个预核报告的 SHA-256。运行主题校验、链接基线和名称诊断，保存非阻断基线。

- [ ] **Step 2: 并行复核划分特征**

逐节核对数组、划分特征、节点标签、本地分析和来源数组的概念边界；核对当前 24 个数组和生成／校验能力；判断 `basis: self`、完备划分、判据句、节点标签、生命周期和复核规则是否与当前治理接口一致。结论只取“保持草案”“整篇重写后继续草案”“提交 L3 生效提案”之一。

- [ ] **Step 3: 并行复核分面字段**

逐节核对主题分支、概念集合、分面、概念组和映射视图的职责；寻找当前是否已有真实查询消费者和可试标概念集合，复核既有试标设计是否实际执行。没有真实试标时不得批准字段。结论使用同一三值集合。

- [ ] **Step 4: 并行复核概念组**

逐节核对 ISO ConceptGroup、SKOS Collection、叙词表数组和映射派生视图；重新计算当前 `group` 角色和视图是否物化，寻找真实多项目／多角色／专题消费者；核对身份、成员依据、生命周期、删除、生成和空组边界。结论使用同一三值集合。

- [ ] **Step 5: 覆盖门禁**

三个报告各自列出：当前草案每节去向、外部依据、未读边界、正式数据事实、真实触发、影响文件、不采用后果、L2／L3 门禁和推荐。三份报告不得互相复制结论；当前受跟踪写集保持为空。

### Task 2: 草案结论

**Files:**

- Create ignored: `.superpowers/sdd/2026-09-01-existing-drafts-review/conclusions.md`
- Create ignored: `.superpowers/sdd/2026-09-01-existing-drafts-review/decision-package.md`
- Modify conditionally: `design/drafts/division-characteristics.md`
- Modify conditionally: `design/drafts/facet-field.md`
- Modify conditionally: `design/drafts/concept-groups.md`

**Interfaces:**

- Consumes: Task 1 三份独立报告。
- Produces: 每份草案的最终复核结论，以及必要的整篇重写。

- [ ] **Step 1: 核对三份推荐**

对每份草案分别判断推荐是否由其自身证据推出。共同的来源／术语接口和权限边界只作一致性检查，不能改变某份草案的真实触发结论。

- [ ] **Step 2: 锁定旧节去向**

仅对推荐“整篇重写后继续草案”的文件列全部旧节去向。每节只取保留、整节重写、并入新节或删除过时说明之一；无缺陷草案不建立虚假重写任务。

- [ ] **Step 3: 重写有缺陷草案**

整篇重写每个必要文件，保留有效概念和不采用后果，删除与现行接口冲突或夸大已实现／已生效状态的说明。草案开头继续写“草案，未生效”；不得创建正式字段、文件、schema、数据或脚本。

- [ ] **Step 4: 形成决定包**

每份草案单独列稳定身份、当前状态、依据、推荐、替代、不采用后果、影响文件、错误代价和级别。推荐继续草案不伪装成 L3 决定；只有证据闭合且确实建议生效时才列精确 L3 请求。

- [ ] **Step 5: 提交草案结论**

只提交实际变化的草案，提交说明为：

```bash
git commit -m "[L2] 既有草案:落实独立复核"
```

若三份均无需修改，则本任务不制造空提交。

### Task 3: 路线记录

**Files:**

- Modify: `docs/superpowers/plans/2026-08-31-project-roadmap.md`

**Interfaces:**

- Consumes: Task 2 三份独立结论和实际草案写集。
- Produces: 草案复核阶段关闭，四项待定设计成为下一阶段。

- [ ] **Step 1: 更新原始目标**

整行同步原始目标表第 6 项：列出三份结论及仍开放的精确生效门禁，不把继续草案写成已生效。

- [ ] **Step 2: 更新执行顺序**

整节重写“执行顺序”：草案复核标为当前范围完成，待定设计标为下一阶段；其他顺序、后置门禁和范围排除不变。

- [ ] **Step 3: 运行阶段门禁**

运行：

```bash
git diff --check
python3 scripts/check_link_baseline.py
python3 scripts/check-topics.py
python3 scripts/check-terms.py --all
git status --short
```

逐项核对三份结论、草案状态、旧节去向、正式数据零差异和路线一致性；写集只含必要草案和项目路线。

- [ ] **Step 4: 提交路线记录**

```bash
git add docs/superpowers/plans/2026-08-31-project-roadmap.md
git commit -m "[L2] 项目路线:关闭草案复核"
```
