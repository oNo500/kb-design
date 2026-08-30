# 治理草案计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to execute this plan continuously. The source and terminology drafts may be written in parallel only because this plan freezes their shared interface.

**Goal:** 把已批准的术语治理规格转成两份职责分离、字段精确但尚未生效的项目原生草案，并在设计索引中清楚登记其状态。

**Architecture:** 来源治理草案唯一地定义 `basis`、`source`、`match`、来源实体、用途与复核传播；术语治理草案引用这些对象，定义概念、语言、表示形式、译名、状态、委托与生成边界。两份草案写集互斥，可基于本计划冻结的共享接口并行起草；接口核对通过后再整篇同步设计索引。

**Tech Stack:** Markdown、Git、现有项目校验脚本、Superpowers 子代理。

**Spec:** [术语治理设计](../specs/2026-08-27-terminology-governance-design.md)

## 全局约束

- 在 `/Users/xiu/code/kb-design` 的 `feat/terminology-governance` 分支执行，不创建 worktree，不修改 `master`。
- 本计划实施已由人在 2026-08-30 批准。批准范围是新建两份未生效项目草案、同步设计索引、执行接口与文档校验并提交；不批准草案生效、模式、正式数据、生成器、来源改档、术语准入、发版、推送或合并。
- 两份草案是项目正文，不是 Superpowers 审查文档。正文不得出现代理、评审对话、执行工具、临时表或 Superpowers 过程。
- 每份草案第二行固定写 `状态：草案，未生效。`。本计划不移动草案，不把内容并入现行设计，不创建正式 YAML 或脚本。
- 外部标准只支持概念边界。字段名、枚举、基数、工作流、权限、复核期限和阻断条件均明确为项目提案。
- 当前阶段零自定继续适用。外部概念使用现有来源笔记中已核的原语言名称；没有合格中文形式时使用有来源的原语言名称和普通解释，不造译名。
- 来源草案唯一地定义 `basis`、`source` 和 `match`；术语草案只能链接引用，不复制或改变定义。
- `basis` 支持具体值，`source` 表示实际派生，`match` 表示概念映射，项目决定与外部证据分开。旧 `origin` 只出现在迁移边界，不继续使用。
- `tier` 只保留过渡语义，不在本计划删除或改档。具体来源改档仍是 L3。
- `vocab/terms.yaml`、TBX、Obsidian、导入和往返编辑均不实施；TBX 只记录未来单向交换边界。
- 现行 `design/`、`concepts/`、`sources/`、`vocab/` 和 `scripts/` 除 `design/README.md` 外保持不变。
- 修改文章不做补丁式补写。两份新草案整体成文；`design/README.md` 按旧节去向整篇重写。
- 新扫描器会检查标题、加粗和中文引号。草案新增候选必须逐项判断是项目提案字段、来源原名、普通说明还是未准入名称，不能以扫描器退出码替代语义复核。
- 全库链接脚本当前有两个被忽略的旧 SDD 问题。正式写集相对链接必须为 0 问题；全库结果只能保持相同两项，不能新增。
- 用户已要求减少额外 review。本计划只安排代理自查、控制器机械门禁和一次跨草案接口核对，不增加重复的全量独立复审。
- 提交说明标注最高级别 `[L2]`；不调用分支收尾流程。

## 共享接口

来源草案唯一拥有以下对象的定义。字段名与结构是已批准的项目提案，不宣称来自某个标准。

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

- `basis.entity` 指向来源实体；`locator` 必填；会变化的网页要求 `checked`。
- `source.registry` 指向已批准用途登记，`item` 定位外部条目；它只表示实际派生。
- `match.rel` 使用 SKOS 五种 mapping property 的本地枚举；关系自身需要比较定义和范围的 `basis`。
- 项目批准另用决定记录，不进入以上三种外部证据对象。

## 文件职责

| 文件 | 操作 | 职责 |
|---|---|---|
| `design/drafts/source-governance.md` | 新建 | 来源身份、用途、引用、状态、复核、探测与失效传播提案 |
| `design/drafts/terminology-governance.md` | 新建 | 概念、语言、表示形式、译名、状态、委托与生成提案 |
| `design/README.md` | 整篇重写 | 区分现行设计与两份未生效草案并提供阅读入口 |
| `.superpowers/sdd/2026-08-30-governance-drafts/progress.md` | 新建 | 保存执行状态、代理、哈希、裁定和验证 |
| `.superpowers/sdd/2026-08-30-governance-drafts/field-matrix.tsv` | 新建 | 核对共享字段的唯一定义、使用位置、引用目标和失效动作 |
| `.superpowers/sdd/2026-08-30-governance-drafts/verification.md` | 新建 | 保存草案阶段的实际门禁结果与人工批准边界 |

## 草案结构

来源治理草案固定使用以下小节：

- 草案边界
- 对象边界
- 引用结构
- 实体记录
- 用途登记
- 状态转换
- 复核义务
- 失效处理
- 探测边界
- 决策权限
- 校验规则
- 生效条件
- 待定事项

术语治理草案固定使用以下小节：

- 草案边界
- 对象边界
- 记录层次
- 概念记录
- 语言记录
- 术语记录
- 译名准入
- 状态转换
- 委托关系
- 生成边界
- 复核义务
- 决策权限
- 校验规则
- 迁移边界
- 生效条件
- 待定事项

## 执行顺序

输入锁定后，两份草案并行起草；跨草案接口核对完成后，设计索引才能消费两份稳定草案。最终验证后停止在人工逐份批准门禁，不启动模式实施。

### 输入锁定

**Files:**

- Read: `docs/superpowers/specs/2026-08-27-terminology-governance-design.md`
- Read: `docs/superpowers/plans/2026-08-28-terminology-project-design.md`
- Read: 当前治理、维护、来源、术语概念文和来源笔记
- Read: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/post-migration-review.tsv`
- Create: `.superpowers/sdd/2026-08-30-governance-drafts/progress.md`

**Steps:**

- [ ] 锁定当前分支、HEAD、三份目标文件不存在或现状、现行链接问题、主题数据状态和候选扫描基线。
- [ ] 核对旧计划与当前 HEAD 的差异：原项目目录分支替代 worktree；新扫描器包含标题；后迁移 348 表替代已删除的 `/tmp` 临时表。
- [ ] 确认本计划只有三份受跟踪写入目标，其他正式项目文件保持只读。

### 来源草案

**Files:**

- Create: `design/drafts/source-governance.md`
- Create: `.superpowers/sdd/2026-08-30-governance-drafts/source-report.md`

**Steps:**

- [ ] 整篇新建固定标题和小节，第二行标明未生效。
- [ ] 区分来源实体、来源用途、逐值依据、实际派生、概念映射、项目决定和复核义务。
- [ ] 在“引用结构”唯一地定义共享接口的字段、必填条件、引用目标和禁止替代关系。
- [ ] 实体记录提出 `id`、`label`、`kind`、`version`、`url`、`status`、`basis`、`review`、`watch`、`replaced_by`、`history`；`kind` 只复用 `standard` 和 `publication`。
- [ ] 实体状态提出 `current`、`superseded`、`withdrawn`；暂时不可访问只产生探测结果和复核义务。
- [ ] 用途记录提出 `id`、`entity`、`roles`、`history`；角色为 `mapping`、`structure`、`group`、`discovery`，角色状态为 `proposed`、`approved`、`retired`。
- [ ] 旧 `candidate` 角色只迁移到 `discovery`，`tier` 暂作兼容字段；不作具体来源改档。
- [ ] 定义状态转换、反向引用、失效类型、离线校验、联网探测、L1/L2/L3 权限、校验规则、生效条件和默认未生效行为。
- [ ] 自查没有 `basis: self`、`role: candidate`、无定位依据、自动改写正式数据或 Superpowers 过程。

### 术语草案

**Files:**

- Create: `design/drafts/terminology-governance.md`
- Create: `.superpowers/sdd/2026-08-30-governance-drafts/terminology-report.md`

**Steps:**

- [ ] 整篇新建固定标题和小节，第二行标明未生效。
- [ ] 区分术语概念、语言记录、术语记录、定义、适用学科、工作流、生成视图及其他词表标签。
- [ ] 提出未来唯一编辑源 `vocab/terms.yaml` 的 `schema`、`version`、`concepts` 顶层，但明确草案生效前不得创建。
- [ ] 概念记录提出稳定 `id`、`subject_fields`、`definitions`、`languages`、`basis`、`workflow`、`history`；逐值依据引用来源草案。
- [ ] 语言记录使用 BCP 47；简体与繁体不自动互转。术语记录提出 `id`、`text`、`administrative_status`、`basis`、`replaced_by`。
- [ ] 同一概念同一语言恰有一个优先术语；允许、废弃和被替代状态只采用已核 TBX-Basic 管理状态，被替代状态必须指向同概念术语。
- [ ] 概念工作流提出 `candidate`、`active`、`deprecated`；术语概念不使用 `unassigned`，概念状态与术语管理状态互不代替。
- [ ] 译名阶梯按同一双语条目、逐项核对的等同采标、同一权威主体明确对应、两种单语形式加独立概念一致性证据、不译的顺序表达。
- [ ] 明确 Wikidata、机器翻译、拼写相似、搜索数量、修改采用和非等效采用不能单独批准译名。
- [ ] 定义状态转换、`term_concept` 委托、唯一编辑权、同形异义、确定性生成、TBX 单向导出边界、复核义务、权限、校验、迁移、生效条件和默认未生效行为。
- [ ] 只链接来源草案的 `basis`、`source`、`match` 定义，不复制字段语义；自查没有 `status: unassigned`、`basis: self`、术语准入结论或 Superpowers 过程。

### 接口核对

**Files:**

- Read: 两份草案
- Create: `.superpowers/sdd/2026-08-30-governance-drafts/field-matrix.tsv`
- Create: `.superpowers/sdd/2026-08-30-governance-drafts/interface-report.md`

**Steps:**

- [ ] 对 `basis`、`source`、`match`、`decision`、`review`、`history`、`status` 建立七行矩阵，列定义文件、使用文件、引用目标和失效动作。
- [ ] 确认前三项只在来源草案定义；术语草案只链接。
- [ ] 确认用途批准不能推出概念映射，映射不能推出译名，外部依据不能推出项目批准，项目批准不能代替外部依据。
- [ ] 确认 `candidate` 只作概念工作流状态，`discovery` 只作来源用途，`unassigned` 不进入两份草案模型。
- [ ] 确认各状态有进入、退出、替代、复核和历史条件，`origin` 只有迁移说明。
- [ ] 接口冲突返回对应草案整节或整篇重写，不追加例外段落。

### 设计索引

**Files:**

- Modify: `design/README.md`
- Create: `.superpowers/sdd/2026-08-30-governance-drafts/index-report.md`

**Steps:**

- [ ] 列出旧索引“文章的关系”“词表一览”“阅读顺序”的逐项去向，再按索引目的整篇重写。
- [ ] 保留现行设计链，另建明确标注“未生效”的草案分支，链接两份治理草案。
- [ ] 保持现有正式编辑源不变，不把 `vocab/terms.yaml` 写成现行文件。
- [ ] 阅读顺序增加项目草案入口，明确阅读不等于生效；不把 Superpowers 规格或计划列入项目设计组成部分。

### 必要验证

**Files:**

- Create: `.superpowers/sdd/2026-08-30-governance-drafts/verification.md`

**Steps:**

- [ ] 核对两份草案标题、小节顺序、未生效状态、项目提案标识和三文件写集。
- [ ] 核对七行字段矩阵完整、唯一且与正文一致。
- [ ] 运行增强标题门禁、`git diff --check`、正式写集相对链接检查、`scripts/check-terms.py --all` 前后差异和 `scripts/check-topics.py`。
- [ ] 用后迁移校验器刷新 348 条审查表到本计划执行目录，保持决定列不变，并验证删除证据和结构门禁。
- [ ] 全库链接检查只允许两个既有旧 SDD 问题，不得新增正式项目问题。
- [ ] 核对没有 `vocab/`、`scripts/`、`concepts/`、`sources/` 或其他现行设计差异，没有草案生效、来源改档、术语准入、发版、推送或合并。
- [ ] 分别提交计划、来源草案、术语草案和设计索引；接口修正按实际受影响文件提交，不创建空提交。
- [ ] 向人提交两份草案及哈希后停止。后续模式、迁移、生成和现行设计同步仍等待逐份明确批准。
