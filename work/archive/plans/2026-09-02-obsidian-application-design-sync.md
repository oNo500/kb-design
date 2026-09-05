# Obsidian 应用设计同步计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 Obsidian 从单向词表参考导出重新定义为 `kb-design` 的完整落地应用层，同时保持内容消费者、正式回流和 vault 实现未激活。

**Architecture:** 项目正文按应用无关模型、Obsidian `Application Profile`、受管理表示、用户内容和派生报告分层。现有词表导出作为应用中的受管理表示保留；新的内容、导航、盲区和维护合同进入 target 设计，但不因设计存在而宣称已有 vault、内容或运行消费者。

**Tech Stack:** Markdown、YAML 字段合同、Obsidian 官方帮助、DCMI `Application Profile`、现有 Python 文档检查脚本。

**Spec:** `docs/superpowers/specs/2026-09-02-obsidian-knowledge-base-application-design.md`

## 全局约束

- 当前只执行设计同步，不修改 `scripts/`、`tests/`、`schemas/` 或 `vocab/`。
- `design/targets/obsidian.md` 按新目的整篇重写，不追加补充小节。
- Superpowers 规格、计划和审查材料不复制进项目正文。
- 项目正文只采用已有登记 designation；作者经验只作使用模式证据，不形成项目术语。
- 外部资料、临时文件和人工索引不得被写成正式内容单元、主题、数组或概念组。
- 现有词表导出、manifest、稳定路径、无回流和确定性边界保留。
- 新 target 不宣称真实 vault、内容文件、内容消费者、引用统计、查询日志、回流或发版已经存在。
- 内容 identifier 发放规则未批准前，不选择机翻 slug、拼音、时间戳、UUID 或其他形式作为现行规则。
- 文档、静态配置和确定性事实使用直接校验；不为本计划增加 TDD 测试。
- 只运行链接基线、术语 report、标题与写集检查；不运行与代码无关的全量回归。

---

### Task 1: 内容身份依据

**Files:**
- Create: `sources/rfc-9562.md`
- Create: `concepts/content-identifiers.md`
- Create: `.superpowers/sdd/2026-09-02-obsidian-application-design/content-identifier-proposal.md`

**Interfaces:**
- Consumes: `design/content-model.md` 的现行 identifier 规则、DCMI `identifier`、RFC 9562。
- Produces: target 和内容模型可以引用的身份概念边界，以及一份不取得正式效力的推荐提案。

- [ ] **Step 1: 核对来源范围**

读取 RFC 9562 的 UUID 定义、文本表示、UUIDv4、UUIDv7、opacity、sorting 和 security 条款；读取 DCMI `identifier` 的定义。记录实际读到的小节、适用问题和不能证明的事项。

- [ ] **Step 2: 写来源笔记**

`sources/rfc-9562.md` 只记录以下事实：

```text
UUID 是 128-bit identifier，不需要中央登记；
UUIDv4 由随机或伪随机位生成；
UUIDv7 包含 Unix Epoch 时间并支持时间排序；
标准文本表示是 hex-and-dash；
唯一性、不可猜测性、排序和不透明性是不同要求；
RFC 9562 不决定本项目应使用哪一版 UUID，也不批准 cu- 前缀。
```

- [ ] **Step 3: 写概念文**

`concepts/content-identifiers.md` 解释资源 identifier 与名称、标题、路径、排序信息和时间信息的边界。文章不得把 UUID 翻译成未经核实的中文 designation，也不得写入项目选择。

- [ ] **Step 4: 写决定提案**

提案比较三项：沿用名称 slug、UUIDv4、UUIDv7。推荐 UUIDv4，理由固定为：不依赖内容名称、无需中央登记、不暴露创建时间语义、Python 标准库直接支持。提案同时说明：是否增加对象前缀、前缀形式和正式采用仍由人决定。

- [ ] **Step 5: 运行文档检查**

Run:

```bash
python3 scripts/check_link_baseline.py
python3 scripts/check-terms.py --all
git diff --check
```

Expected: 链接基线仍为既有 `count=2`；术语脚本退出 0 且只报告人工候选；差异检查无输出。

- [ ] **Step 6: 提交依据**

```bash
git add sources/rfc-9562.md concepts/content-identifiers.md
git commit -m '[L2] 内容身份:补充标识符概念依据'
```

`.superpowers/` 提案保持过程文件，不进入提交。

### Task 2: Obsidian 来源

**Files:**
- Rewrite: `sources/obsidian-help.md`

**Interfaces:**
- Consumes: Obsidian 官方 Properties、Bases、Search、Backlinks、Graph、Bookmarks、Templates、Unique note creator、Web Clipper、Web Clipper Templates、Variables 和 Internal links 文档。
- Produces: `design/targets/obsidian.md` 的应用能力事实和限制。

- [ ] **Step 1: 重写阅读范围**

按能力分别记录 URL、已读小节、核对日期、可用行为、限制和本项目用途。保留现有已核实的 vault、properties、aliases、links、accepted formats 和 Bases 事实。

- [ ] **Step 2: 补充创建能力**

明确记录：

```text
Templates 只能插入片段、标题和日期变量，不能校验受控值；
Unique note creator 使用时间名称，不能自动成为项目内容 identifier；
Web Clipper 能把页面内容和 preset variables 保存到 vault；
prompt variables 需要外部模型，存在速度、成本和隐私差异；
Web Clipper 模板可以创建或追加文件，但不产生项目效力。
```

- [ ] **Step 3: 补充导航能力**

明确记录 Bases 可编辑、排序和筛选 Markdown properties；Search 能查询正文、路径和 properties，但官方文档没有给出本项目可审计的搜索事件接口；Backlinks、Graph 和 Bookmarks 是导航或探索能力，不证明正式关系。

- [ ] **Step 4: 检查并提交**

```bash
python3 scripts/check_link_baseline.py
python3 scripts/check-terms.py --all
git diff --check
git add sources/obsidian-help.md
git commit -m '[L1] Obsidian:重写应用能力来源'
```

Expected: 检查退出 0；提交只包含来源笔记。

### Task 3: 应用映射重写

**Files:**
- Rewrite: `design/targets/obsidian.md`

**Interfaces:**
- Consumes: 已批准规格、现行内容模型、六份正式词表、应用分层决定、Task 1 身份边界、Task 2 Obsidian 事实。
- Produces: 完整但未激活的 Obsidian `Application Profile`，供关联设计和未来实施计划引用。

- [ ] **Step 1: 重写定位与状态**

开篇必须说明：Obsidian 是首个落地应用层；当前只有词表参考导出实现；用户内容、内容建立、内容校验、使用统计和回流没有实现。不得继续把“映射完成”等同于完整应用完成。

- [ ] **Step 2: 写功能范围**

功能范围包含捕获、外部资料、内容写作、正式对象引用、人工索引、Base 浏览、结构盲区、使用盲区和维护反馈；明确排除任务日程、既有 vault 迁移、查询日志、自动回流、社区插件硬依赖和正式激活。

- [ ] **Step 3: 写权属与布局**

写入一个 vault、用户内容、受管理表示、派生结果和 `.obsidian` 配置四类边界，并固定下列职责布局：

```text
Home.md
Inbox/
Sources/{Clippings,References,Files}/
Content/
Indexes/
Attachments/
KB/{Topics,Arrays,Entities,Sources,Types,Genres,Forms}/
App/{Templates,Views,Reports,Rules}/
App/manifest.json
.obsidian/
```

- [ ] **Step 4: 写对象与流程**

明确 Inbox、外部资料、内容单元、应用索引、正式表示和派生报告的不同效力。内容流程必须覆盖进入、建立、draft、active、deprecated、替代和误建删除例外。

- [ ] **Step 5: 保留字段矩阵**

把现行正式词表逐字段矩阵完整保留并核对，不删减已修正的 `basis` 空列表和 `alt`／`hidden` 重复保存事实。把未来内容矩阵改为“已设计、未实现”，补充创建条件、编辑条件、查询用途和失败表现，不改变字段名、基数和值域。

- [ ] **Step 6: 写导航与盲区**

区分正式主题树、人工索引、Base、Search、Backlinks 和 Graph。写入结构盲区、使用盲区、直接引用计数、分支聚合计数和 report-only 未解析线索；明确聚合计数不增加上位 subject。

- [ ] **Step 7: 写维护与失败**

写入单向反馈流程、报告写集、决策权门禁、manifest 漂移、无效内容、悬空引用、重复 ID、relation 不互反、Clipper 提取错误和插件缺失的处理。

- [ ] **Step 8: 写能力边界**

逐项说明 File Explorer、Properties、Templates、Unique note creator、Web Clipper、Internal links、Backlinks、Bases、Search、Bookmarks、Graph 和 Canvas 的用途与不能承担的职责。

- [ ] **Step 9: 写身份门禁**

明确记录内容 identifier 发放仍等待决定。target 不选择机翻 slug、拼音、时间戳、UUID 或前缀；在决定批准前，不宣称内容建立已可实施。

- [ ] **Step 10: 运行结构检查**

```bash
python3 scripts/check_link_baseline.py
python3 scripts/check-terms.py --all
git diff --check
```

另以 `rg -Fq` 检查 target 同时包含：`Inbox/`、`Sources/`、`Content/`、`Indexes/`、`App/Reports/`、`结构盲区`、`使用盲区`、`identifier`、`Web Clipper`、`Backlinks`、`Bookmarks`。

- [ ] **Step 11: 提交 target**

```bash
git add design/targets/obsidian.md
git commit -m '[L2] Obsidian:重写知识库应用设计'
```

### Task 4: 关联设计同步

**Files:**
- Modify by whole-section rewrite: `design/content-model.md`
- Modify by whole-section rewrite: `design/maintenance.md`
- Modify by whole-section rewrite: `design/principles.md`

**Interfaces:**
- Consumes: Task 3 target 职责和未激活边界。
- Produces: 应用无关设计对完整 Obsidian target 的正确引用，不复制 target 实现细节。

- [ ] **Step 1: 同步内容模型**

重写“应用映射”和 identifier 相关段落：保留现行字段、基数和值域；说明 Obsidian target 已设计完整内容应用但尚未实现；登记内容 identifier 发放缺口，不在本文提前选择 UUID。

- [ ] **Step 2: 同步维护设计**

重写引用 Obsidian 的指标、触发和消费者边界：未来消费者从通过校验的 `Content/` 受控字段计算计数；普通 Wikilink、Backlinks、Indexes 和 Graph 不进入正式计数；查询日志继续未实现。

- [ ] **Step 3: 同步方法登记**

在现有 `Application Profile` 行中补充捕获、内容使用、导航、诊断和反馈属于 target 功能范围与 usage 的推导，不新增方法名称，不把作者经验写成规范来源。

- [ ] **Step 4: 检查并提交**

```bash
python3 scripts/check_link_baseline.py
python3 scripts/check-terms.py --all
git diff --check
git add design/content-model.md design/maintenance.md design/principles.md
git commit -m '[L2] 内容应用:同步模型与维护边界'
```

### Task 5: 项目入口同步

**Files:**
- Rewrite affected sections: `README.md`
- Rewrite affected sections: `design/README.md`
- Rewrite affected sections: `AGENTS.md`
- Rewrite affected sections: `docs/superpowers/plans/2026-08-31-project-roadmap.md`

**Interfaces:**
- Consumes: Tasks 1–4 的现行设计状态。
- Produces: 对外入口、会话摘要和路线状态使用同一完成口径。

- [ ] **Step 1: 更新根入口**

README 必须把 Obsidian 表述为首个完整应用 target，并准确说明：完整应用设计已建立；当前代码仍只有词表参考导出；没有真实 vault、内容或运行消费者。

- [ ] **Step 2: 更新设计索引**

`design/README.md` 的效力层次、现行设计、应用映射、当前状态和阅读顺序同步新 target。不得登记 Superpowers 规格为项目设计。

- [ ] **Step 3: 更新会话摘要**

AGENTS 只保留稳定边界：Obsidian 是落地应用层；当前仅参考导出实现；内容应用设计存在不等于消费者启用；内容 identifier 决定仍未完成。

- [ ] **Step 4: 更新路线状态**

路线记录本次设计同步产物、未激活代码范围和内容 identifier 决策门禁。不得把后续代码实施写成已完成。

- [ ] **Step 5: 检查并提交**

```bash
python3 scripts/check_link_baseline.py
python3 scripts/check-terms.py --all
git diff --check
git add README.md design/README.md AGENTS.md docs/superpowers/plans/2026-08-31-project-roadmap.md
git commit -m '[L2] 项目入口:同步 Obsidian 应用定位'
```

### Task 6: 设计验收

**Files:**
- Create: `.superpowers/sdd/2026-09-02-obsidian-application-design/verification.md`

**Interfaces:**
- Consumes: Tasks 1–5 的全部提交。
- Produces: 当前设计阶段的验收记录和下一阶段门禁。

- [ ] **Step 1: 核对写集**

从执行基点到 HEAD 的 tracked 写集只能包含本计划列出的来源、概念、target、关联设计和入口文件。`scripts/`、`tests/`、`schemas/` 和 `vocab/` 必须无差异。

- [ ] **Step 2: 核对状态声明**

以下陈述必须在 target、设计索引、根 README、AGENTS 和路线中一致：

```text
Obsidian 是落地应用层；
现行实现只有词表参考导出；
内容应用尚未实现和启用；
真实 vault 与内容不存在；
内容 identifier 决定未完成；
报告和视图不能自动修改正式数据。
```

- [ ] **Step 3: 运行最终检查**

```bash
python3 scripts/check_link_baseline.py
python3 scripts/check-terms.py --all
git diff --check
git status --short
```

Expected: 链接 baseline 仍只有两个既有 Superpowers 历史问题；术语输出保持 report-only；差异检查无输出；tracked 工作区干净。

- [ ] **Step 4: 写验收记录**

`verification.md` 记录执行基点、提交、写集、命令输出、内容 identifier 提案状态和未实施代码边界。该文件留在 `.superpowers/`，不进入项目正文。

- [ ] **Step 5: 停在决定门禁**

向用户提交 UUIDv4 推荐及是否增加对象前缀的决定请求。只有用户明确批准后，才可新建正式决定、修改现行 identifier 规则并编写 vault 实施计划。
