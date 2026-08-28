# 项目治理草案

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把已经核实的外部概念转成两份职责分离、字段精确但尚未生效的项目设计草案，为来源数据和术语数据的后续实现提供唯一规则入口。

**Architecture:** 先写来源治理草案，定义来源实体、来源用途、引用对象、复核义务和失效传播；再写术语治理草案，复用同一引用接口，定义概念、语言、术语、译名、状态和委托边界。两份草案都放在 `design/drafts/`，不混入 Superpowers 审查过程，也不修改现行规则、数据或脚本。

**Tech Stack:** Markdown、YAML 模式示例、现有项目治理与写作规则、Git。

**Spec:** [术语治理设计](../specs/2026-08-27-terminology-governance-design.md)

## 前置条件

- [术语概念基础](2026-08-28-terminology-concept-foundations.md) 已全部执行、审查和校验通过。
- `sources/terminology-standards.md`、`sources/metadata-standards.md` 与 `concepts/terminology-database.md` 已存在。
- 术语表全表审查已经完成，“基本单位”整节已经批准并取得可定位依据；其余每个问题及活跃消费者只在临时审查清单中标为“术语迁移”，表示明确延期，不表示迁移已经获准。后续迁移仍须单独提交 L2 提案。
- `/tmp/kb-terminology-glossary-review.tsv` 必须随执行交接保留；新会话无法取得时，从 `git merge-base master HEAD` 取出分支起点的术语表，重新执行前一计划“术语审查”的全部固定批次，并与当前术语表逐项比较后交人复核，不能凭摘要重建。

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

### 审查重建

**Files:**

- Read: 分支起点的 `concepts/glossary.md`
- Read: 当前 `concepts/glossary.md`
- Read: 前置计划完成后的 `sources/` 与 `concepts/`
- Modify: none

**Interfaces:**

- Consumes: 前置计划定义的固定提取器、348 个起点形式和当前术语表。
- Produces: 临时审查表丢失时可重新取得的人审结果；不产生项目设计或迁移授权。

**Steps:**

- [ ] 运行 `test -s /tmp/kb-terminology-glossary-review.tsv && test -s /tmp/kb-extract-glossary-forms.py`；如果通过，记录“无需重建”并转到“基线核对”；如果失败，继续本任务，项目草案保持未创建。
- [ ] 运行 `awk 'BEGIN{f=sprintf("%c%c%c",96,96,96)} $0 == f "python" {capture=1; next} $0 == f {if (capture) exit} capture' docs/superpowers/plans/2026-08-28-terminology-concept-foundations.md > /tmp/kb-extract-glossary-forms.py`，再运行 `python3 -m py_compile /tmp/kb-extract-glossary-forms.py`；预期通过，且脚本逐字来自前置计划的固定代码块。
- [ ] 运行 `git show "$(git merge-base master HEAD):concepts/glossary.md" > /tmp/kb-terminology-glossary-branch-base.md`；预期取得分支起点的术语表，不读取当前已重写的“基本单位”。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py extract /tmp/kb-terminology-glossary-branch-base.md /tmp/kb-terminology-glossary-forms-before.tsv /tmp/kb-terminology-glossary-consumers-before.tsv`；预期退出码为 0。
- [ ] 运行 `test "$(tail -n +2 /tmp/kb-terminology-glossary-forms-before.tsv | wc -l | tr -d ' ')" = 348` 与 `test "$(tail -n +2 /tmp/kb-terminology-glossary-consumers-before.tsv | wc -l | tr -d ' ')" = 348`；预期均通过。
- [ ] 运行 `awk -F'\t' 'BEGIN{OFS="\t"} NR == 1 {print $1,$2,$3,$4,"依据结论","依据位置","概念对应",$5,"动作","处理阶段"; next} {print $1,$2,$3,$4,"","","",$5,"",""}' /tmp/kb-terminology-glossary-consumers-before.tsv > /tmp/kb-terminology-glossary-review.tsv`；建立十列重建清单。
- [ ] 依据结论只用 `有依据`、`无依据`、`有冲突`；概念对应只用 `同一概念`、`不同概念`、`未确定`、`不适用`；动作只用 `keep`、`add`、`remove`、`defer`；处理阶段只用 `基本单位`、`已核`、`术语迁移`。
- [ ] 有依据时，“依据位置”至少填写一个带标题和锚点的 Markdown 链接；无依据或有冲突时，以“检索记录：”开头，填写本次核对日期和实际检索过的带标题链接。
- [ ] 审查起点第 9–14 行的出处缩写并填写清单。
- [ ] 审查起点第 20–24 行的“词表的类型”第一批并填写清单。
- [ ] 审查起点第 25–27 行并完成“词表的类型”。
- [ ] 审查起点第 33–37 行的“基本单位”第一批并填写清单。
- [ ] 审查起点第 38–42 行的“基本单位”第二批并填写清单。
- [ ] 审查起点第 43–47 行并完成“基本单位”。
- [ ] 审查起点第 53–57 行的“关系”第一批并填写清单。
- [ ] 审查起点第 58–62 行的“关系”第二批并填写清单。
- [ ] 审查起点第 63–65 行并完成“关系”。
- [ ] 审查起点第 71–75 行的“结构”第一批并填写清单。
- [ ] 审查起点第 76–80 行的“结构”第二批并填写清单。
- [ ] 审查起点第 81–85 行并完成“结构”。
- [ ] 审查起点第 91–95 行的“注释与生命周期”第一批并填写清单。
- [ ] 审查起点第 96–100 行并完成“注释与生命周期”。
- [ ] 审查起点第 106–110 行的“建设与治理”第一批并填写清单。
- [ ] 审查起点第 111–115 行的“建设与治理”第二批并填写清单。
- [ ] 审查起点第 116–121 行并完成“建设与治理”。
- [ ] 审查起点第 127–131 行的“词表间映射”第一批并填写清单。
- [ ] 审查起点第 132–136 行的“词表间映射”第二批并填写清单。
- [ ] 审查起点第 137–139 行并完成“词表间映射”。
- [ ] 审查起点第 145–149 行并完成“知识体系”。
- [ ] 审查起点第 155–159 行并完成“元数据”。
- [ ] 审查起点第 165–169 行的“写作与设计方法”第一批并填写清单。
- [ ] 审查起点第 170–173 行并完成“写作与设计方法”。
- [ ] 审查起点第 179–183 行的“笔记的类型”第一批并填写清单。
- [ ] 审查起点第 184–186 行并完成“笔记的类型”。
- [ ] 审查起点第 192–196 行的“治理与维护”第一批并填写清单。
- [ ] 审查起点第 197–201 行的“治理与维护”第二批并填写清单。
- [ ] 审查起点第 202–204 行并完成“治理与维护”。
- [ ] 审查起点第 209–213 行的“知识图谱”第一批并填写清单。
- [ ] 审查起点第 214–218 行的“知识图谱”第二批并填写清单。
- [ ] 审查起点第 219–220 行并完成“知识图谱”。
- [ ] 审查起点第 226–230 行的“引用的标准与文献”第一批并填写清单。
- [ ] 审查起点第 231–235 行的“引用的标准与文献”第二批并填写清单。
- [ ] 审查起点第 236–239 行并完成“引用的标准与文献”。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py extract-forms concepts/glossary.md /tmp/kb-terminology-glossary-forms-current.tsv`，再运行 `diff -u /tmp/kb-terminology-glossary-forms-before.tsv /tmp/kb-terminology-glossary-forms-current.tsv > /tmp/kb-terminology-glossary-rebuild.diff || true`；逐项把当前新增形式登记为 `add` 与“新增”原行，把当前已移除形式登记为 `remove`，不得从差异猜测依据。
- [ ] 运行 `awk '/^## 基本单位$/{skip=1; next} /^## /{skip=0} !skip{print}' /tmp/kb-terminology-glossary-branch-base.md > /tmp/kb-terminology-glossary-nonbasic-before.md` 与 `awk '/^## 基本单位$/{skip=1; next} /^## /{skip=0} !skip{print}' concepts/glossary.md > /tmp/kb-terminology-glossary-nonbasic-current.md`，再运行 `diff -u /tmp/kb-terminology-glossary-nonbasic-before.md /tmp/kb-terminology-glossary-nonbasic-current.md`；预期无差异，证明前置计划没有改其他小节。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv`，再运行 `python3 /tmp/kb-extract-glossary-forms.py audit-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-consumers-reviewed.tsv`。
- [ ] 运行 `tail -n +2 /tmp/kb-terminology-glossary-forms-before.tsv | sort > /tmp/kb-terminology-glossary-before.keys`，再运行 `awk -F'\t' 'NR > 1 && $9 != "add" {print $1 "\t" $2 "\t" $3 "\t" $4}' /tmp/kb-terminology-glossary-review.tsv | sort > /tmp/kb-terminology-glossary-reviewed.keys` 和 `diff -u /tmp/kb-terminology-glossary-before.keys /tmp/kb-terminology-glossary-reviewed.keys`；预期无差异。
- [ ] 运行 `test -z "$(tail -n +2 /tmp/kb-terminology-glossary-review.tsv | cut -f1-4 | sort | uniq -d)"`；预期退出码为 0。
- [ ] 运行 `tail -n +2 /tmp/kb-terminology-glossary-consumers-reviewed.tsv | sort > /tmp/kb-terminology-glossary-consumers-actual.keys`，再运行 `awk -F'\t' 'NR > 1 {print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $8}' /tmp/kb-terminology-glossary-review.tsv | sort > /tmp/kb-terminology-glossary-consumers-recorded.keys` 和 `diff -u /tmp/kb-terminology-glossary-consumers-actual.keys /tmp/kb-terminology-glossary-consumers-recorded.keys`；预期无差异。
- [ ] 运行 `awk -F'\t' 'NR > 1 && (NF != 10 || $1 == "" || $2 == "" || $3 == "" || $4 == "" || $5 == "" || $6 == "" || $7 == "" || $8 == "" || $9 == "" || $10 == "") {bad=1} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 运行 `awk -F'\t' 'NR > 1 && ($5 !~ /^(有依据|无依据|有冲突)$/ || $7 !~ /^(同一概念|不同概念|未确定|不适用)$/ || $9 !~ /^(keep|add|remove|defer)$/ || $10 !~ /^(基本单位|已核|术语迁移)$/) {bad=1} NR > 1 && $5 == "有依据" && $6 !~ /\[[^]]+\]\([^)]*#[^)]+\)/ {bad=1} NR > 1 && $5 != "有依据" && ($6 !~ /^检索记录：/ || $6 !~ /[0-9]{4}-[0-9]{2}-[0-9]{2}/ || $6 !~ /\[[^]]+\]\([^)]+\)/) {bad=1} NR > 1 && $2 == "und" && $7 != "不适用" {bad=1} NR > 1 && $2 != "und" && $7 == "不适用" {bad=1} NR > 1 && $9 == "add" && ($4 != "新增" || $5 != "有依据" || $7 != "同一概念") {bad=1} NR > 1 && $9 != "add" && $4 !~ /^[0-9]+$/ {bad=1} NR > 1 && $9 == "remove" && $8 != "无引用" {bad=1} NR > 1 && $3 == "基本单位" && ($10 != "基本单位" || $9 !~ /^(keep|add|remove)$/) {bad=1} NR > 1 && $3 != "基本单位" && !(($9 == "keep" && $10 == "已核") || ($9 == "defer" && $10 == "术语迁移")) {bad=1} NR > 1 && $10 == "已核" && ($5 != "有依据" || $7 !~ /^(同一概念|不适用)$/) {bad=1} NR > 1 && $10 == "基本单位" && $9 == "keep" && ($5 != "有依据" || $7 != "同一概念") {bad=1} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 运行 `awk -F'\t' 'NR > 1 && $2 != "und" {key=$3 SUBSEP $4; if (key in seen && seen[key] != $7) bad=1; seen[key]=$7} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv` 与 `python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期均通过，且无待移除形式仍有消费者。
- [ ] 运行 `awk -F'\t' 'NR > 1 && $9 ~ /^(keep|defer|add)$/ {print $1 "\t" $2 "\t" $3}' /tmp/kb-terminology-glossary-review.tsv | sort > /tmp/kb-terminology-glossary-expected-current.keys`，再运行 `tail -n +2 /tmp/kb-terminology-glossary-forms-current.tsv | cut -f1-3 | sort > /tmp/kb-terminology-glossary-actual-current.keys` 和 `diff -u /tmp/kb-terminology-glossary-expected-current.keys /tmp/kb-terminology-glossary-actual-current.keys`；预期无差异。
- [ ] 将重建后的全表问题和“基本单位”清单交人复核；人确认重建结果后才转到“基线核对”，该确认不批准“术语迁移”。

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
- [ ] 运行 `test -s /tmp/kb-terminology-glossary-review.tsv && test -s /tmp/kb-extract-glossary-forms.py`；预期退出码为 0。失败时停止本任务并执行“审查重建”，不得在本步骤内合并处理。
- [ ] 运行 `awk -F'\t' 'NR > 1 && (NF != 10 || $5 == "" || $6 == "" || $7 == "" || $8 == "" || $9 == "" || $10 == "") {bad=1} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0，证明依据结论、依据位置、概念对应、全库引用、动作和处理阶段均已填写。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期通过，并把消费者位置刷新到本计划基线。
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
- [ ] 运行 `git add design/drafts/source-governance.md`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 提交：`git commit -m "[L2] 来源治理:新增项目草案"`。

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
- [ ] 运行 `git add design/drafts/terminology-governance.md`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 提交：`git commit -m "[L2] 术语治理:新增项目草案"`。

### 接口复核

**Files:**

- Modify: `design/drafts/source-governance.md`
- Modify: `design/drafts/terminology-governance.md`

**Interfaces:**

- Consumes: 两份草案的全部字段、状态和交叉链接。
- Produces: 一个定义位置、两个清楚职责、无循环推导的项目提案。

**Steps:**

- [ ] 在 `/tmp/kb-terminology-field-matrix.tsv` 建立“字段、定义文件、使用文件、引用目标、失效动作”五列标题；该文件不加入仓库。
- [ ] 填写 `basis` 一行；定义位置只能是来源草案“引用结构”。
- [ ] 填写 `source` 一行；定义位置只能是来源草案“引用结构”。
- [ ] 填写 `match` 一行；定义位置只能是来源草案“引用结构”。
- [ ] 填写 `decision` 一行；明确它与外部证据分开。
- [ ] 填写 `review` 一行；明确来源复核与术语复核的使用位置。
- [ ] 填写 `history` 一行；明确只追加约束和两份草案的使用位置。
- [ ] 填写 `status` 一行；分别列来源实体、来源用途、概念工作流和术语管理状态，不合并枚举。
- [ ] 运行 `test "$(tail -n +2 /tmp/kb-terminology-field-matrix.tsv | wc -l | tr -d ' ')" = 7`；预期退出码为 0。
- [ ] 运行 `awk -F'\t' 'NR > 1 && (NF != 5 || $1 == "" || $2 == "" || $3 == "" || $4 == "" || $5 == "") {bad=1} END {exit bad ? 1 : 0}' /tmp/kb-terminology-field-matrix.tsv`；预期退出码为 0。
- [ ] 运行 `for field_name in basis source match decision review history status; do test "$(awk -F'\t' -v wanted="$field_name" 'NR > 1 && $1 == wanted {n++} END {print n+0}' /tmp/kb-terminology-field-matrix.tsv)" = 1 || exit 1; done`；预期退出码为 0，任何缺失或重复字段都会立即失败。
- [ ] 确认每个共享字段只在来源草案定义；术语草案只链接，不复制或改写定义。
- [ ] 确认来源用途批准不能推出概念映射，概念映射不能推出译名，外部依据不能推出项目批准，项目批准不能替代外部依据。
- [ ] 确认 `candidate` 只作概念工作流状态，`discovery` 只作来源用途，`unassigned` 不进入两份草案的数据模型。
- [ ] 确认所有状态都有进入、退出、替代、复核和历史条件，没有只能进入不能处置的状态。
- [ ] 确认 `origin` 在两份草案中只有迁移说明，没有新记录形状或新增用法。
- [ ] 如发现跨节冲突，整节重写受影响小节并重新核对旧内容去向，不追加“例外说明”补丁。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。再运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-project-design-terms-interface.txt` 和 `diff -u /tmp/kb-terminology-project-design-terms-before.txt /tmp/kb-terminology-project-design-terms-interface.txt || true`；逐项处理草案正文新增候选，不把脚本退出码当作验收。
- [ ] 如有修改，运行 `git add design/drafts/source-governance.md design/drafts/terminology-governance.md`；无修改则保持暂存区为空。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 暂存区有修改时提交：`git commit -m "[L2] 治理草案:统一共享接口"`；无修改时不创建空提交。

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
- [ ] 运行 `git add design/README.md`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 提交：`git commit -m "[L2] 设计索引:登记治理草案"`。

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

- [ ] 确认执行记录明确写着“程序分支不可合并”，不得在两份草案尚未获准或正式迁移尚未完成时调用分支收尾技能。
- [ ] 使用 `superpowers:requesting-code-review` 分别审查来源草案和术语草案，再做一次跨文档接口审查；反馈涉及一节以上时整节或整篇重写。
- [ ] 逐项处理审查反馈；有内容修正时运行 `git add design/drafts/source-governance.md design/drafts/terminology-governance.md design/README.md`，无修改时保持暂存区为空。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 暂存区有审查修正时提交：`git commit -m "[L2] 治理草案:完成设计复核"`；无修改时不创建空提交。
- [ ] 从下一项开始执行最终验收；任何一项失败时，整节或整篇重写受影响内容，运行任务校验并提交，再重新请求三部分审查，随后从本项重新执行全部最终验收。
- [ ] 按“旧文去向”逐项确认两份草案已经为后续现行文档重写指定唯一目的地，没有把旧规则静默丢弃。
- [ ] 从审查后的两份草案重新填写 `/tmp/kb-terminology-field-matrix.tsv` 七行；每行的定义文件、使用文件、引用目标和失效动作必须与当前正文一致。
- [ ] 运行 `test "$(tail -n +2 /tmp/kb-terminology-field-matrix.tsv | wc -l | tr -d ' ')" = 7`；预期退出码为 0。
- [ ] 运行 `awk -F'\t' 'NR > 1 && (NF != 5 || $1 == "" || $2 == "" || $3 == "" || $4 == "" || $5 == "") {bad=1} END {exit bad ? 1 : 0}' /tmp/kb-terminology-field-matrix.tsv`；预期退出码为 0。
- [ ] 运行 `for field_name in basis source match decision review history status; do test "$(awk -F'\t' -v wanted="$field_name" 'NR > 1 && $1 == wanted {n++} END {print n+0}' /tmp/kb-terminology-field-matrix.tsv)" = 1 || exit 1; done`；预期退出码为 0。
- [ ] 确认 `basis`、`source`、`match` 只在来源草案“引用结构”定义；术语草案只链接，不复制定义，`decision` 不进入外部证据对象。
- [ ] 确认来源用途批准不能推出概念映射，概念映射不能推出译名，外部依据不能推出项目批准，项目批准不能替代外部依据。
- [ ] 确认 `candidate` 只作概念工作流状态，`discovery` 只作来源用途，`unassigned` 不进入两份草案的数据模型。
- [ ] 确认每类状态都有进入、退出、替代、复核和历史条件，`origin` 只出现在迁移说明中。
- [ ] 运行 `rg -n '^#{2,6} .*[:：]|^#{2,6} [0-9一二三四五六七八九十]' design/drafts/source-governance.md design/drafts/terminology-governance.md design/README.md`；预期无标题违规。
- [ ] 人工核对全部小节标题为 2–8 字名词短语，且不含字段名、文件名、数量或实现参数。
- [ ] 运行 `test "$(head -n 1 design/drafts/source-governance.md)" = '# 来源治理' && test "$(head -n 1 design/drafts/terminology-governance.md)" = '# 术语治理' && test "$(head -n 1 design/README.md)" = '# 设计文档索引'`；预期退出码为 0。
- [ ] 运行 `test "$(rg -c '^草案，未生效。$' design/drafts/source-governance.md)" = 1 && test "$(rg -c '^草案，未生效。$' design/drafts/terminology-governance.md)" = 1`；预期退出码为 0。
- [ ] 运行 `rg -n 'Superpowers|评审对话|代理记录|审查工具|执行过程' design/drafts/source-governance.md design/drafts/terminology-governance.md`；预期无匹配，证明 Superpowers 审查过程没有混入项目草案。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv`，再运行 `python3 /tmp/kb-extract-glossary-forms.py audit-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-consumers-reviewed.tsv`；两份新草案中的消费者必须进入临时清单。
- [ ] 运行 `tail -n +2 /tmp/kb-terminology-glossary-consumers-reviewed.tsv | sort > /tmp/kb-terminology-glossary-consumers-actual.keys`，再运行 `awk -F'\t' 'NR > 1 {print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $8}' /tmp/kb-terminology-glossary-review.tsv | sort > /tmp/kb-terminology-glossary-consumers-recorded.keys` 和 `diff -u /tmp/kb-terminology-glossary-consumers-actual.keys /tmp/kb-terminology-glossary-consumers-recorded.keys`；预期无差异。
- [ ] 运行 `awk -F'\t' 'NR > 1 && (NF != 10 || $1 == "" || $2 == "" || $3 == "" || $4 == "" || $5 == "" || $6 == "" || $7 == "" || $8 == "" || $9 == "" || $10 == "") {bad=1} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 运行 `awk -F'\t' 'NR > 1 && ($5 !~ /^(有依据|无依据|有冲突)$/ || $7 !~ /^(同一概念|不同概念|未确定|不适用)$/ || $9 !~ /^(keep|add|remove|defer)$/ || $10 !~ /^(基本单位|已核|术语迁移)$/) {bad=1} NR > 1 && $5 == "有依据" && $6 !~ /\[[^]]+\]\([^)]*#[^)]+\)/ {bad=1} NR > 1 && $5 != "有依据" && ($6 !~ /^检索记录：/ || $6 !~ /[0-9]{4}-[0-9]{2}-[0-9]{2}/ || $6 !~ /\[[^]]+\]\([^)]+\)/) {bad=1} NR > 1 && $2 == "und" && $7 != "不适用" {bad=1} NR > 1 && $2 != "und" && $7 == "不适用" {bad=1} NR > 1 && $9 == "add" && ($4 != "新增" || $5 != "有依据" || $7 != "同一概念") {bad=1} NR > 1 && $9 != "add" && $4 !~ /^[0-9]+$/ {bad=1} NR > 1 && $9 == "remove" && $8 != "无引用" {bad=1} NR > 1 && $3 == "基本单位" && ($10 != "基本单位" || $9 !~ /^(keep|add|remove)$/) {bad=1} NR > 1 && $3 != "基本单位" && !(($9 == "keep" && $10 == "已核") || ($9 == "defer" && $10 == "术语迁移")) {bad=1} NR > 1 && $10 == "已核" && ($5 != "有依据" || $7 !~ /^(同一概念|不适用)$/) {bad=1} NR > 1 && $10 == "基本单位" && $9 == "keep" && ($5 != "有依据" || $7 != "同一概念") {bad=1} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 运行 `awk -F'\t' 'NR > 1 && $2 != "und" {key=$3 SUBSEP $4; if (key in seen && seen[key] != $7) bad=1; seen[key]=$7} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv` 与 `python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期均通过。
- [ ] 运行 `python3 scripts/check-links.py`；预期输出“全部链接有效”。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-project-design-terms-final.txt`，再运行 `diff -u /tmp/kb-terminology-project-design-terms-before.txt /tmp/kb-terminology-project-design-terms-final.txt || true`；逐项人工复核，预期两份草案正文没有新增无依据术语。
- [ ] 运行 `python3 scripts/check-topics.py`；预期与基线同样通过，证明没有修改正式数据。
- [ ] 运行 `git diff --check "$(cat /tmp/kb-terminology-project-design-base.sha)"..HEAD`；预期无错误，并覆盖审查修正后的全部提交。
- [ ] 运行 `test "$(git diff --name-only "$(cat /tmp/kb-terminology-project-design-base.sha)"..HEAD | sort)" = $'design/README.md\ndesign/drafts/source-governance.md\ndesign/drafts/terminology-governance.md'`；预期退出码为 0。
- [ ] 阅读 `git diff "$(cat /tmp/kb-terminology-project-design-base.sha)"..HEAD`，确认除 `design/README.md` 外的现行 `design/*.md`，以及全部 `vocab/`、`scripts/`、`concepts/` 和 `sources/` 未被本计划修改。
- [ ] 运行 `git status --short`；预期无输出，证明审查修正和最终验收修正都已提交。

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
