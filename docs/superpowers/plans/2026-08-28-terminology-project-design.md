# 项目治理草案

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把已经核实的外部概念转成两份职责分离、字段精确但尚未生效的项目设计草案，为来源数据和术语数据的后续实现提供唯一规则入口。

**Architecture:** 先写来源治理草案，定义来源实体、来源用途、引用对象、复核义务和失效传播；再写术语治理草案，复用同一引用接口，定义概念、语言、术语、译名、状态和委托边界。两份草案都放在 `design/drafts/`，不混入 Superpowers 审查过程，也不修改现行规则、数据或脚本。

**Tech Stack:** Markdown、YAML 模式示例、现有项目治理与写作规则、Git。

**Spec:** [术语治理设计](../specs/2026-08-27-terminology-governance-design.md)

## 前置条件

- [术语概念基础](2026-08-28-terminology-concept-foundations.md) 已全部执行、审查和校验通过。
- `sources/terminology-standards.md`、`sources/metadata-standards.md` 与 `concepts/terminology-database.md` 已存在。
- 术语表和相关概念文不再依赖未读条款、自定中文译名或混合含义的来源断言。

## 全局约束

- 必须在独立 worktree 和功能分支执行，不得在 `master` 上修改。
- 第一次写文件前，提交本计划列出的 L2 文件与小节清单；人明确批准后才创建草案。
- 两份文件是项目设计草案，不是 Superpowers 审查文档。正文只写拟议规则、外部依据、本地决定和生效条件，不写讨论过程、代理工作记录或评审意见。
- 草案开头必须写“草案，未生效”。本计划不移动草案、不并入现行设计、不改变 `design/governance.md`，因此不构成 L3 生效决定。
- 外部标准只支持概念边界。字段名、枚举、基数、工作流、权限、复核日期和阻断条件必须逐项标为“项目提案”。
- 两份草案共享引用接口，但不合并职责：来源草案治理材料和用途，术语草案治理概念及语言形式。
- `basis`、`source` 和 `match` 的名字可以出现在两份草案中，但定义只在来源草案给一次；术语草案链接引用，不复制定义。
- 旧 `origin` 只登记迁移分流，不在新方案中继续使用。
- 现有 `tier` 不在本计划中删除或改档。草案可提议它的过渡语义；任何具体来源改档仍需 L3。
- 不创建 `vocab/terms.yaml`，不改任何现有 YAML，不写模式、生成器、探测器、维护脚本或迁移代码。
- 不实现 TBX、Obsidian 或应用导出；只记录它们依赖的稳定语义。
- `scripts/check-terms.py` 只产生候选报告，不扫描术语表、标题或代码，也不以候选非零退出；本计划只用前后报告差异发现草案正文的新候选。
- 本计划仍是程序分支的中间阶段，不是可合并状态。两份草案获准、正式数据迁移和现行设计同步前不得调用分支收尾流程。
- 标题、标点、间距、整篇重写和零自定要求与仓库现行规则相同。
- 提交说明使用 `[L2]`；不得用一次草案批准覆盖后续 L3 生效或数据迁移决定。

## 文件职责

| 文件 | 操作 | 单一职责 |
|---|---|---|
| `design/drafts/source-governance.md` | 新建 | 提出来源身份、用途、引用、复核、探测和失效传播规则 |
| `design/drafts/terminology-governance.md` | 新建 | 提出术语概念、多语形式、译名、状态、委托和生成规则 |
| `design/README.md` | 整篇重写 | 把两份未生效草案加入设计索引，并保持现行设计与草案边界 |

## 接口边界

来源草案必须先定义三种共享对象，术语草案只能引用它们：

```yaml
basis:
  - entity: z39-19
    locator: "§ 11.1.4"
    checked: 2026-08-28

source:
  registry: cs2023
  item: SE
  locator: "Knowledge Area description"
  basis:
    - entity: cs2023
      locator: "SE overview"
      checked: 2026-08-28

match:
  - registry: cwe
    item: CWE-89
    rel: exactMatch
    basis:
      - entity: cwe
        locator: CWE-89
        checked: 2026-08-28
```

这些是项目提案，不宣称来自某个标准的字段名。约束如下：

- `basis` 支持与它相邻的具体值；现行值至少一项，候选值可以处于待复核状态但不能用 `self` 伪装依据。
- `entity` 指向来源实体；`locator` 必填并使用来源自身可重复定位的章节、条目、锚点或记录标识。
- `checked` 对会变化的网页必填；对有固定版次、固定内容的出版物可省略，由来源实体的版次标识确定内容。
- `source` 只表示实际派生；`registry` 指向获准来源用途记录，`item` 指向其具体外部条目。
- `match` 只表示概念映射；`rel` 只能是 SKOS 五种 mapping property 的本地枚举名，关系自身也要有比较定义和范围的 `basis`。
- 项目批准另用决定记录引用，不写进 `basis`，也不能由 `source` 或 `match` 推出。

## 旧文去向

本计划不改下列现行文档，但两份草案必须给出它们在未来整篇重写时的精确去向，供后续计划使用：

| 现行位置 | 未来保留 | 未来迁出 |
|---|---|---|
| `design/governance.md` | 决策权、政策、变更控制和验收总则 | 术语准入、译名阶梯移入术语治理；来源用途与复核移入来源治理 |
| `design/maintenance.md` | 维护触发、指标、批次和评审总则 | 断言结构移入来源治理；术语生命周期移入术语治理；来源周期移入来源治理 |
| `design/entities.md` | 命名实体与主题概念的分工 | 来源实体字段、版本、地址、`tier` 过渡语义移入来源治理 |
| `design/sources-registry.md` | 来源名称规范表作为用途登记的目的 | 角色状态、复核、`candidate` 角色拆分和失效处理移入来源治理 |
| `design/topics.md` | 主题概念、层级和主题状态 | `basis`、`source`、`match` 的共享引用结构与旧 `origin` 分流 |
| `design/writing.md` | 通用写作、标题、标点和文档结构 | 正文术语、无译名处理和术语表一致性移入术语治理 |
| `design/versioning.md` | 发布与兼容总则 | 术语数据库和生成视图的发布对象由术语治理定义后再接入 |
| `concepts/glossary.md` | 读者视图的栏目和阅读用途 | 正式编辑职责未来交给 `vocab/terms.yaml`，本计划不实施 |

## 草案结构

`design/drafts/source-governance.md` 使用以下小节，顺序固定：

- `草案边界`
- `对象边界`
- `引用结构`
- `实体记录`
- `用途登记`
- `状态转换`
- `复核义务`
- `失效处理`
- `探测边界`
- `决策权限`
- `校验规则`
- `生效条件`
- `待定事项`

`design/drafts/terminology-governance.md` 使用以下小节，顺序固定：

- `草案边界`
- `对象边界`
- `记录层次`
- `概念记录`
- `语言记录`
- `术语记录`
- `译名准入`
- `状态转换`
- `委托关系`
- `生成边界`
- `复核义务`
- `决策权限`
- `校验规则`
- `迁移边界`
- `生效条件`
- `待定事项`

## 计划序列

全部获准范围保留在执行链中，但后续计划只能使用前一阶段已经审定的字段、状态和实测指标：

| 工作 | 本计划组的交付 | 后续关口 |
|---|---|---|
| 翻译与术语依据审查 | 前置计划重写来源、术语表和概念文；术语草案提出译名阶梯 | 草案获准后才迁移现有译名决定 |
| 术语准入流程 | 术语草案提出登记、复核、批准、废弃和维护状态 | 模式计划须以获准状态机写正反例 |
| 依据与断言 | 来源草案定义 `basis`、`source`、`match` 和旧 `origin` 分流 | 数据计划须先生成全库引用与迁移清单 |
| 来源维护 | 来源草案定义实体、用途、复核义务、探测和失效传播 | 来源模式与探测计划在草案获准后单独编写；具体改档逐项申请 L3 |
| 首轮维护 | 本计划只固定维护对象和证据边界 | 模式、迁移和校验落地后，以重新生成的候选、`unassigned`、`self` 和来源指标另写执行计划 |
| 三份草案 | 仍分别保留划分特征、分面字段、手工概念组的独立身份 | 基础治理落地后逐份写概念核对与生效审查计划，不合并作一个 L3 决定 |
| 其他设计 | 生活领域、实体类别、大语言模型归属、技术传播继续保持待定 | 每项按外部概念、项目问题、影响文件和不采用后果单独提案 |
| 应用交换 | Obsidian 映射与 TBX 交换继续后置 | 内部模型稳定且相关草案获准后分别写规格，不合并实施 |

---

### 基线核对

**Files:**

- Read: `design/governance.md`
- Read: `design/maintenance.md`
- Read: `design/entities.md`
- Read: `design/sources-registry.md`
- Read: `design/topics.md`
- Read: `design/writing.md`
- Read: `design/versioning.md`
- Read: 前置计划的全部交付文件
- Modify: none

**Interfaces:**

- Consumes: 已核外部概念、现行项目规则和本计划的精确提案。
- Produces: 执行基线与 L2 授权边界。

**Steps:**

- [ ] 运行 `git status --short --branch`；预期位于独立功能分支且工作区为空。
- [ ] 运行 `git rev-parse HEAD > /tmp/kb-terminology-project-design-base.sha`，再运行 `test -s /tmp/kb-terminology-project-design-base.sha`；预期退出码为 0。后续所有范围校验使用这个固定基线。
- [ ] 运行 `test -f sources/terminology-standards.md && test -f sources/metadata-standards.md && test -f concepts/terminology-database.md`；预期退出码为 0。
- [ ] 运行 `python3 scripts/check-links.py` 与 `python3 scripts/check-topics.py`；保存基线输出。再运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-project-design-terms-before.txt`，只保存候选报告。
- [ ] 运行 `test ! -e design/drafts/source-governance.md && test ! -e design/drafts/terminology-governance.md`；预期退出码为 0，证明不是覆盖未知草案。
- [ ] 向人提交精确 L2 提案：新建两份未生效项目草案，并整篇重写 `design/README.md`；附上本计划“草案结构”和“接口边界”。
- [ ] 明确说明本次批准只允许写草案，不批准字段生效、数据迁移、来源改档或草案激活。
- [ ] 等待人明确批准；未批准时停止，不创建文件。

### 来源草案

**Files:**

- Create: `design/drafts/source-governance.md`

**Interfaces:**

- Consumes: `sources/metadata-standards.md`、来源相关概念文、现行来源与实体设计。
- Produces: 共享 `basis`、`source`、`match` 引用接口和来源治理提案。

**Steps:**

- [ ] 新建文章标题 `# 来源治理`，下一行写“草案，未生效。”，再按“草案结构”建立全部小节。
- [ ] 在“草案边界”列出外部概念、本地提案、现行规则和不在本草案决定的事项；正文不提审查工具、对话或代理过程。
- [ ] 在“对象边界”区分来源实体、来源用途、逐值依据、实际派生、概念映射、项目决定和复核义务七种对象。
- [ ] 在“引用结构”完整定义本计划“接口边界”的三个对象、字段类型、必填条件和引用目标；不允许裸网址、自由文本来源名、`self` 或无位置标准号作为现行断言的完整依据。
- [ ] 在“实体记录”提出精确记录形状：`id`、`label`、`kind`、`version`、`url`、`status`、`basis`、`review`、`watch`、`replaced_by`、`history`。
- [ ] `kind` 在本草案中只复用现行 `standard` 与 `publication`；增加或改变实体类别留给独立的实体类别提案。
- [ ] 将来源实体 `status` 提议为 `current`、`superseded`、`withdrawn`；网页暂时不可访问只进入探测报告，不自动改变生命周期状态。
- [ ] 将 `review` 提议为 `checked`、`due`、`reason`；将 `watch` 提议为若干 `url` 与 `signal`，其中 `signal` 只允许 `version`、`status`、`content`。
- [ ] 在“用途登记”提出精确记录形状：`id`、`entity`、`roles`、`history`；每个角色分别保存 `status`、`basis`、`decision` 和 `review`。
- [ ] 将角色提议为 `mapping`、`structure`、`group`、`discovery`；将角色状态提议为 `proposed`、`approved`、`retired`。旧 `candidate` 角色只迁移为 `discovery`，不再兼作生命周期状态。
- [ ] 说明 `tier` 暂时保留为兼容字段，但不再单独推出角色资格或复核周期；删除字段和每个来源的去向分别留给后续 L2 模式提案与 L3 改档决定。
- [ ] 在“状态转换”分别画出来源实体和每个用途角色的转换条件；任何 `approved` 或 `retired` 角色必须引用项目决定。
- [ ] 在“复核义务”按 `basis`、`source`、`match` 三种反向引用定义影响集合；义务至少保存对象路径、触发来源、原因、建立日期和状态。
- [ ] 在“失效处理”区分地址变化、内容变化、新版、替代、撤回与暂时不可访问；任何探测结果都只建复核义务，不自动改写正式断言。
- [ ] 在“探测边界”分别定义离线校验和联网探测的输入、只读输出与禁止动作；链接存活不得等同内容继续有效。
- [ ] 在“决策权限”逐项标注 L1、L2、L3，特别保留“同一来源新地址”为 L1、“结构与角色规则”为 L2、“具体来源改档”为 L3。
- [ ] 在“校验规则”列出引用存在性、定位非空、状态组合、替代目标、决定引用、复核日期、反向引用与探测只读性。
- [ ] 在“生效条件”列出概念依据已审、模式与迁移计划获准、每项 L3 改档单独决定、正反例测试存在、现行设计同步完成。
- [ ] “待定事项”只列仍需人决定且本草案无法推出的项目选择；每项必须有决策级别和不决定时的行为，不留空白占位。
- [ ] 运行 `rg -n '^## .*[:：]|basis:[[:space:]]*self|role:[[:space:]]*candidate' design/drafts/source-governance.md`；预期无匹配。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 提交：`git add design/drafts/source-governance.md && git commit -m "[L2] 来源治理:新增项目草案"`。

### 术语草案

**Files:**

- Create: `design/drafts/terminology-governance.md`

**Interfaces:**

- Consumes: `concepts/terminology-database.md`、`sources/terminology-standards.md`、来源治理草案的共享引用对象。
- Produces: 精确但未生效的术语记录、译名、状态、委托与生成提案。

**Steps:**

- [ ] 新建文章标题 `# 术语治理`，下一行写“草案，未生效。”，再按“草案结构”建立全部小节。
- [ ] 在“草案边界”区分外部术语工作概念、本地 YAML 提案、现行零自定政策和不在本草案实现的 TBX、Obsidian、导入及往返编辑。
- [ ] 在“对象边界”定义术语概念、语言组、术语形式、定义、适用领域、工作流记录和生成视图；与主题概念、命名实体和枚举词表分开。
- [ ] 在“记录层次”提出唯一编辑源 `vocab/terms.yaml` 的精确顶层：`schema`、`version`、`concepts`；明确该文件在草案激活前不得创建。
- [ ] 在“概念记录”提出字段：`id`、`subject_fields`、`definitions`、`languages`、`basis`、`workflow`、`history`。`id` 沿用小写字母、数字和连字符的稳定标识规则。
- [ ] 将 `subject_fields` 的每项定义为 `topic` 与相邻 `basis`；将 `definitions` 的每项定义为 `lang`、`text` 与相邻 `basis`。
- [ ] 在“语言记录”把每项定义为 `lang` 与 `terms`；`lang` 使用 BCP 47，简体和繁体分别使用能够准确表示书写系统的标签，不自动互转。
- [ ] 在“术语记录”把每项定义为 `id`、`text`、`administrative_status`、`basis`、`replaced_by`；同一概念同一语言恰有一个 `preferredTerm-admn-sts`，其余只允许 TBX-Basic 已核的 `admittedTerm-admn-sts`、`deprecatedTerm-admn-sts`、`supersededTerm-admn-sts`。
- [ ] 规定 `supersededTerm-admn-sts` 必须以 `replaced_by` 指向同一概念下的术语 id；其他状态不得填写该字段。
- [ ] 将 `workflow` 定义为 `status`、`added`、`approved`、`review`、`replaced_by`；概念状态只允许 `candidate`、`active`、`deprecated`，术语概念不使用 `unassigned`。
- [ ] 定义 `approved` 为决定记录引用与日期，`review` 复用来源草案的 `checked`、`due`、`reason`；`history` 只追加，不回写旧决定。
- [ ] 在“译名准入”写出固定阶梯：同一官方双语术语条目；逐项核对后的等同采标术语；同一权威主体明确对应的双语形式；两种单语形式加独立概念一致性证据；以上都没有则不译。
- [ ] 明确修改采用、非等效采用、Wikidata、搜索数量、机器翻译和拼写相似只能用于发现或补充检查，不能单独批准译名；现有阶梯中相反的内容列入迁移清单。
- [ ] 在“状态转换”分别定义概念工作流和术语管理状态；概念批准不自动改变每个术语的管理状态，术语废弃也不自动废弃概念。
- [ ] 在“委托关系”提出既有词表字段 `term_concept`：只有概念一致性获准且影响清单完成后才能出现；出现后该记录不再拥有同语言术语的独立编辑权。
- [ ] 规定同一概念同一语言的术语只存在于一个正式编辑位置；同形异义词允许位于不同概念记录，但必须由不同定义和范围区分。
- [ ] 在“生成边界”规定 `concepts/glossary.md` 只由 `active` 概念确定性生成，显示各语言优先术语、允许术语、定义、来源和状态；生成物不得产生原记录没有的译名或状态。
- [ ] 明确 TBX 只可能从获准发布快照单向导出；本草案不定义方言、导入或往返一致性。
- [ ] 在“复核义务”定义术语、定义、概念一致性、来源和正文一致性的触发条件；来源变化复用来源草案的反向引用规则。
- [ ] 在“决策权限”规定检索和校验为 L1，术语准入、译名采用、状态规则和委托为 L2，零自定例外、草案生效和发版为 L3。
- [ ] 在“校验规则”列出 id、BCP 47、唯一优先术语、状态组合、替代引用、逐值依据、决定引用、同形异义、委托唯一性、确定性生成和正文一致性。
- [ ] 在“迁移边界”列出旧 `zh_basis`、`en_basis`、紧缩 `basis`、`source`、`none`、`self`、旧 `origin` 与手工术语表的逐项分类；明确不能机械字符串替换。
- [ ] 在“生效条件”列出两份草案共同获准、模式和数据迁移计划通过、现有引用清单完成、生成与校验测试存在、现行设计整篇同步、L3 草案生效决定完成。
- [ ] “待定事项”只保留确实要由后续样本或人决定的事项，并给出默认保持未生效的行为。
- [ ] 运行 `rg -n '^## .*[:：]|status:[[:space:]]*unassigned|basis:[[:space:]]*self' design/drafts/terminology-governance.md`；预期无匹配。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 提交：`git add design/drafts/terminology-governance.md && git commit -m "[L2] 术语治理:新增项目草案"`。

### 接口复核

**Files:**

- Modify: `design/drafts/source-governance.md`
- Modify: `design/drafts/terminology-governance.md`

**Interfaces:**

- Consumes: 两份草案的全部字段、状态和交叉链接。
- Produces: 一个定义位置、两个清楚职责、无循环推导的项目提案。

**Steps:**

- [ ] 建立字段矩阵，逐项列 `basis`、`source`、`match`、`decision`、`review`、`history`、`status` 的定义文件、使用文件、引用目标和失效动作。
- [ ] 确认每个共享字段只在来源草案定义；术语草案只链接，不复制或改写定义。
- [ ] 确认来源用途批准不能推出概念映射，概念映射不能推出译名，外部依据不能推出项目批准，项目批准不能替代外部依据。
- [ ] 确认 `candidate` 只作概念工作流状态，`discovery` 只作来源用途，`unassigned` 不进入两份草案的数据模型。
- [ ] 确认所有状态都有进入、退出、替代、复核和历史条件，没有只能进入不能处置的状态。
- [ ] 确认 `origin` 在两份草案中只有迁移说明，没有新记录形状或新增用法。
- [ ] 如发现跨节冲突，整节重写受影响小节并重新核对旧内容去向，不追加“例外说明”补丁。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。再运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-project-design-terms-interface.txt` 和 `diff -u /tmp/kb-terminology-project-design-terms-before.txt /tmp/kb-terminology-project-design-terms-interface.txt || true`；逐项处理草案正文新增候选，不把脚本退出码当作验收。
- [ ] 如有修改，提交：`git add design/drafts/source-governance.md design/drafts/terminology-governance.md && git commit -m "[L2] 治理草案:统一共享接口"`；无修改则不提交。

### 设计索引

**Files:**

- Modify: `design/README.md`

**Interfaces:**

- Consumes: 两份未生效草案和现行设计文档。
- Produces: 清楚标识现行规则与候选草案的设计索引。

**Steps:**

- [ ] 核对旧索引的确切去向：“文章的关系”重写为现行链与未生效草案分支，“词表一览”保留现行编辑源，“阅读顺序”增加草案入口；再建立完整标题骨架。
- [ ] 在文章关系中保留现行设计链；另建清楚标注“未生效”的草案分支，分别链接来源治理和术语治理。
- [ ] 在词表一览中保持现有正式编辑源不变；不得把尚未创建的 `vocab/terms.yaml` 写成现行文件。
- [ ] 在阅读顺序末尾加入“项目草案”入口，并说明阅读草案不等于规则生效。
- [ ] 不把 Superpowers 规格或计划列为项目设计组成部分；它们仍只存在于 `docs/superpowers/`。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 提交：`git add design/README.md && git commit -m "[L2] 设计索引:登记治理草案"`。

### 最终校验

**Files:**

- Verify: `design/drafts/source-governance.md`
- Verify: `design/drafts/terminology-governance.md`
- Verify: `design/README.md`
- Modify: only a whole section or whole index when a listed acceptance check fails

**Interfaces:**

- Consumes: 本计划全部提交。
- Produces: 可交给人逐份评审、但不会自行生效的两份项目草案。

**Steps:**

- [ ] 按“旧文去向”逐项确认两份草案已经为后续现行文档重写指定唯一目的地，没有把旧规则静默丢弃。
- [ ] 运行 `rg -n '^#{2,6} .*[:：]|^#{2,6} [0-9一二三四五六七八九十]' design/drafts/source-governance.md design/drafts/terminology-governance.md design/README.md`；预期无标题违规。
- [ ] 人工核对全部小节标题为 2–8 字名词短语。
- [ ] 运行 `rg -n '^# 来源治理$' design/drafts/source-governance.md`、`rg -n '^# 术语治理$' design/drafts/terminology-governance.md` 和 `rg -n '^# 设计文档索引$' design/README.md`；预期各恰好一处。
- [ ] 运行 `rg -n '草案，未生效' design/drafts/source-governance.md design/drafts/terminology-governance.md`；预期恰好两处，每篇一处。
- [ ] 运行 `rg -n 'Superpowers|评审对话|代理记录' design/drafts/source-governance.md design/drafts/terminology-governance.md`；预期无匹配。
- [ ] 运行 `python3 scripts/check-links.py`；预期“全部链接有效”。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-project-design-terms-final.txt`，再运行 `diff -u /tmp/kb-terminology-project-design-terms-before.txt /tmp/kb-terminology-project-design-terms-final.txt || true`；预期差异中没有两份草案正文新增的无依据术语，且该结论经逐项人工复核。
- [ ] 运行 `python3 scripts/check-topics.py`；预期与基线同样通过，证明没有修改正式数据。
- [ ] 运行 `git diff --check "$(cat /tmp/kb-terminology-project-design-base.sha)"..HEAD`；预期无错误，并覆盖全部已提交改动。
- [ ] 运行 `git diff --name-only "$(cat /tmp/kb-terminology-project-design-base.sha)"..HEAD`；预期本计划只改变三份“文件职责”所列文件。
- [ ] 阅读最终 diff，确认现行 `design/*.md`、`vocab/`、`scripts/`、`concepts/` 和 `sources/` 未被本计划修改。
- [ ] 确认执行记录明确写着“程序分支不可合并”，不得在两份草案尚未获准或正式迁移尚未完成时调用分支收尾技能。
- [ ] 使用 `superpowers:requesting-code-review` 分别审查来源草案和术语草案，再做一次跨文档接口审查；反馈涉及一节以上时整节或整篇重写。
- [ ] 重新运行全部校验；有收口修改时提交 `[L2] 治理草案:完成设计复核`，无修改时不创建空提交。

## 完成条件

- 来源治理和术语治理是两份项目原生草案，不是 Superpowers 审查文档。
- `basis`、`source`、`match`、项目决定和复核义务各有唯一职责和引用目标。
- 来源实体、来源用途和两类状态分开；旧 `candidate` 角色有明确迁移方向，`tier` 没有被越权删除或改档。
- 术语概念、语言和术语分层；工作流状态与 TBX-Basic 术语管理状态分开。
- 译名阶梯、无译名行为、逐项依据、委托和确定性生成边界都已写成精确项目提案。
- 两份草案都列出决策权限、校验规则、生效条件和确切的未决定行为。
- 设计索引明确标出草案未生效，正式数据和现行设计保持不变。
- 当前程序分支明确不可合并；两份草案只是后续实现的规则提案。

## 后续入口

两份草案完成后先交人逐份评审。只有人明确接受草案内容后，才分别编写以下实施计划：来源模式与迁移、术语模式与生成、现行设计整篇同步、首轮维护、三份既有草案复核、其他设计待定项。草案激活、具体来源改档和发版仍在相应执行阶段单独申请 L3 决定。
