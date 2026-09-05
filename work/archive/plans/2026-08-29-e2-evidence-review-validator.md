# 证据复核实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 不沿用运行时间作为停止条件，重新复核 E2 的二十五个形式，修正临时审查校验器的两个已知缺口，再运行三百四十八条完整回归并把精确的删除阻断交给“基本单位”复核。

**Architecture:** 执行链只有一个顺序：先冻结完整审查表和旧 E2 材料，再按概念边界与规范名称两组重做来源复核，然后锁定新结论、独立审查并整批合并。校验器在 E2 合并后按测试先行修正；最后用结构探针与删除保护分别证明“除七个既知阻断外无错”和“七个阻断仍精确存在”。本计划只修改临时或已忽略产物，不把审查结论写入项目设计和正式术语数据。

**Tech Stack:** Markdown、Python 3 标准库、TSV、Git、标准发布机构官方页面与可重复定位的规范正文。

**Spec:** [E2 证据复核与校验设计](../specs/2026-08-29-e2-evidence-review-validator-design.md)

## 全局约束

- 必须在 `docs/terminology-governance-spec` 功能分支的独立 worktree 执行；`master` 必须保持在 `6370e647518f6b98174b84665a0b9392256892d9`，不得在 `master` 上修改。
- 本计划实施已由人在 2026-08-29 批准。批准范围是 E2 全量复核、两个校验缺口、三百四十八条回归和进入“基本单位”复核；不批准译名采用、术语准入、消费者迁移、来源改档或任何 L3 决定。
- E2 的二十五个形式全部重新复核。首轮结论在新结论锁定前不得作为判断输入，只能用于锁定后的差异对照。
- 来源复核的停止条件是预先列明的相关来源类别已实际核对，或已记录不可访问与未读边界。运行时长、上下文用量和已有结论都不是停止条件。
- 每个形式分别审查形式依据、定义依据和同组对应依据。标准身份、缩写展开、字符串相同、表格列位和机器翻译都不能单独证明定义或跨语言对应。
- 凭记忆写的外部事实不得进入决定。每个“有依据”必须带标题、链接和可重复定位位置；“无依据”或“有冲突”必须带核对日期、已检材料和未读边界。
- 来源正文不可访问时，只记录已核出版身份、不可访问范围和因此不能支持的断言，不猜测正文。来源相互冲突时同时保存各自位置，结论保持“有冲突”或延期，不按来源数量投票。
- 英文材料不能证明一个形式作为 `zh` 记录的语言形式。中文形式必须核对官方中文标准、等同采用文本或权威中文出版物；查不到时保持未证明，不自行翻译。
- 中英对应按 `design/governance.md` 的译名阶梯核对：先查等同采用国际标准的 GB 译名，再查学科权威教材或工具书中两个独立来源的一致用法，然后查 Wikidata 中文标签；均不成立时不译。E2 的审查结论只记录当前形式是否得到支持，不因搜索结果自动准入新译名。
- 校验器只校验临时十列审查表的身份、值域、完整性、分组、依据格式和删除保护。它不判断来源资格、检索是否充分、定义是否一致或译名是否成立。
- 如果失败测试或全表回归暴露出超过已批准两个缺口的新分组语义，停止修正并另提设计；不扩大本计划的校验规则。
- 修正校验器时先写失败测试，再整个重写 `validate_review()` 的分组和完整性流程；不在旧分支上叠加例外。
- 全表回归要分开两个结论：身份、值域、完整性、分组和依据格式必须全部通过；删除保护必须仅因七个已知形式非零退出。
- 执行材料保存在 `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/`，该目录由 `.superpowers/sdd/.gitignore` 忽略。正式项目文件、`concepts/`、`design/`、`sources/`、`vocab/` 和 `scripts/` 均不在本计划修改。
- 临时文件使用 `apply_patch` 创建或整体重写；原子替换审查表只使用已冻结的 `/tmp/kb-merge-review-decisions.py`。
- 每个子任务由新实施者执行，再由新审查者按规格和证据分两阶段复核。Critical 或 Important 反馈由原实施者按整个受影响决定行、整个报告小节或整个函数重写，最多五轮；仍未关闭时停止并报告。
- 忽略目录与 `/tmp` 产物不创建空提交。本计划文档和规格状态使用 `[L2]` 提交；执行后只以哈希和审查记录形成检查点。

## 文件职责

本计划的文件边界如下。表中“忽略”表示文件存在于当前 worktree，但不进入 Git 提交。

| 文件 | 操作 | 单一职责 |
|---|---|---|
| `docs/superpowers/specs/2026-08-29-e2-evidence-review-validator-design.md` | 状态同步 | 记录已获准的设计边界 |
| `docs/superpowers/plans/2026-08-29-e2-evidence-review-validator.md` | 新建 | 记录本轮可执行步骤与验收命令 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/progress.md` | 忽略新建 | 只追加记录任务、审查、修正轮次和检查点哈希 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/baseline-hashes.sha256` | 忽略新建 | 冻结审查表、校验器、合并器和旧 E2 决定的起点哈希 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-scope.tsv` | 忽略新建 | 只保存 E2 的二十五个四列身份，不包含旧结论 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-source-input.tsv` | 忽略新建 | 保存原术语表的形式、语言、原行、当前定义和当前出处，不包含审查结论 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-core-coverage.tsv` | 忽略新建 | 记录概念边界组的形式、定义与对应来源范围 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-core-decisions.tsv` | 忽略新建 | 保存概念边界组的十四个九列候选决定 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-core-report.md` | 忽略新建 | 解释概念边界组的来源范围、逐项判断与未读边界 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-names-coverage.tsv` | 忽略新建 | 记录规范名称组的形式、定义与对应来源范围 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-names-decisions.tsv` | 忽略新建 | 保存规范名称组的十一个九列候选决定 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-names-report.md` | 忽略新建 | 解释规范名称组的来源范围、语言依据与未读边界 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-new-decisions-locked.tsv` | 忽略新建 | 在读取旧结论前锁定二十五个新决定 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-old-decisions.tsv` | 忽略新建 | 只在新结论锁定后保存首轮 E2 对照副本 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-old-new.diff` | 忽略新建 | 逐行显示首轮与新一轮决定差异 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/review-pre-e2.tsv` | 忽略新建 | 冻结 E2 整批合并前的三百四十八条审查表 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/review-post-e2.tsv` | 忽略新建 | 保存 E2 整批合并后的三百四十八条审查表 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-tests.py` | 忽略新建 | 覆盖既有校验行为和两个新缺口的行为测试 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-before.py` | 忽略新建 | 冻结修正前校验器 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-after.py` | 忽略新建 | 保存通过测试与回归的校验器 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/full-regression.md` | 忽略新建 | 记录三百四十八条身份、完整性、分组、消费者和精确删除阻断结果 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/basic-unit-handoff.tsv` | 忽略新建 | 把七个已知删除阻断及其原始消费者候选交给原计划的“基本单位”语义分类 |
| `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/build-basic-unit-handoff.py` | 忽略新建 | 把七个已知阻断的分号消费者单元机械展开为一形式一位置 |

## 数据接口

完整审查表固定为十列：

```text
形式	语言	小节	原行	依据结论	依据位置	概念对应	全库引用	动作	处理阶段
```

E2 候选决定固定为九列，不包含由审查表保护的“全库引用”：

```text
形式	语言	小节	原行	依据结论	依据位置	概念对应	动作	处理阶段
```

来源范围表是临时审计产物，不是正式术语模式。每个形式至少覆盖“形式”、“定义”和“对应”三个断言单元；每个实际核对的材料占一行：

```text
形式	语言	小节	原行	断言单元	来源类别	来源标题	来源网址	已核位置	核对结果	未读边界
```

“核对结果”只记录材料对当前断言的支持、冲突、未直接支持或不可访问，不用来代替九列决定。一个材料同时支持多个断言时，分行记录它分别支持什么。

E2 的固定身份范围如下。子任务不得增删、改语言或改原行：

| 原行 | 概念边界组 | 规范名称组 |
|---|---|---|
| 209 | `triple` (`en`）、`三元组` (`zh`) | — |
| 210 | `entity` (`en`）、`实体` (`zh`) | — |
| 211 | `edge` (`en`）、`relation` (`en`）、`关系` (`zh`) | — |
| 212 | `property` (`en`）、`属性` (`zh`) | — |
| 213 | `schema` (`en`）、`Schema` (`zh`) | — |
| 214 | `reasoning` (`en`）、`inference` (`en`）、`推理` (`zh`) | — |
| 215 | — | `Resource Description Framework` (`en`）、`RDF` (`zh`) |
| 216 | — | `RDFS` (`zh`）、`OWL` (`zh`) |
| 217 | — | `SPARQL` (`zh`) |
| 218 | — | `Simple Knowledge Organization System` (`en`）、`SKOS` (`zh`) |
| 219 | — | `property graph` (`en`）、`属性图` (`zh`) |
| 220 | — | `Cypher` (`zh`）、`GQL` (`zh`) |

研究输入中的“当前定义”和“当前出处”必须逐字取自以下原术语表行，再与上表的每个形式展开组合：

| 原行 | 当前定义 | 当前出处 |
|---|---|---|
| 209 | 主语 — 谓语 — 宾语，图的最小单位 | W3C RDF 1.1 |
| 210 | 图的节点，有唯一 ID | KG |
| 211 | 带类型的有向边 | KG |
| 212 | 挂在实体或边上的字面值 | KG |
| 213 | 本体在工程语境的叫法：类型与关系的定义 | — |
| 214 | 按规则从已有边推出新边 | KG |
| 215 | W3C 的三元组数据模型 | W3C RDF 1.1 |
| 216 | RDF 上的 schema 语言 / 本体语言 | W3C |
| 217 | RDF 查询语言 | W3C SPARQL 1.1 |
| 218 | 用 RDF 表达词表的 W3C 标准 | W3C SKOS |
| 219 | 节点和边都可带属性的图模型 | ISO/IEC 39075 |
| 220 | 属性图查询语言；GQL 是 2024 年的 ISO 标准 | ISO/IEC 39075:2024 |

下文所有命令默认从 worktree 根目录执行。命令中的产物使用 `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/` 完整路径；任务文字中只写文件名时，也指该唯一路径。

## 执行顺序

---

### 基线冻结

**Files:**

- Read: `design/writing.md`
- Read: `design/governance.md`
- Read: `docs/superpowers/specs/2026-08-29-e2-evidence-review-validator-design.md`
- Read: `docs/superpowers/plans/2026-08-28-terminology-concept-foundations.md`
- Read: `concepts/glossary.md:205`
- Read: `.superpowers/sdd/2026-08-28-terminology-concept-foundations/task-5-artifacts/task-5-batch-e2-decisions.tsv`，但只由控制者冻结，研究子代理不得读取
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/progress.md`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/baseline-hashes.sha256`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-scope.tsv`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-source-input.tsv`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/review-pre-e2.tsv`

**Interfaces:**

- Consumes: 当前功能分支、已完成的三百四十八条审查表、临时校验器和原子合并器。
- Produces: 不含旧决定的 E2 研究输入、可验证的哈希基线和后续子任务的精确身份集。

- [ ] 运行 `git status --short --branch`；预期分支为 `docs/terminology-governance-spec` 且工作区为空。
- [ ] 运行 `test "$(git rev-parse master)" = "6370e647518f6b98174b84665a0b9392256892d9"`；预期退出码为 0。再在主检出目录 `/Users/xiu/code/kb-design` 运行 `git status --short --branch`；预期 `master` 无修改。
- [ ] 运行 `mkdir -p .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts`，再运行 `git check-ignore -q .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts`；预期退出码为 0。
- [ ] 运行 `shasum -a 256 /tmp/kb-terminology-glossary-review.tsv /tmp/kb-extract-glossary-forms.py /tmp/kb-merge-review-decisions.py`；预期依次为 `ef69112774d66d9626b8e1c107f1bced1e93dc9784c21d62cd7aae55bd91f092`、`fda1181d06c931c500a54e66574a1edbef7f1173b3031409db5b6e1c6e120e81`、`f4b286ae8d13f62d20e2e05e1aa976406fef8006817dbfbf898a908cafec7959`。
- [ ] 如果审查表或校验器丢失，分别从 `.superpowers/sdd/2026-08-28-terminology-concept-foundations/task-5-artifacts/task-5-batch-e3-review-post.tsv` 和 `.superpowers/sdd/2026-08-28-terminology-concept-foundations/task-5-artifacts/kb-extract-glossary-forms.py` 恢复后重跑哈希检查。合并器没有旧镜像；它丢失或哈希不同时立即停止，不重写另一个合并器。
- [ ] 运行 `shasum -a 256 .superpowers/sdd/2026-08-28-terminology-concept-foundations/task-5-artifacts/task-5-batch-e2-decisions.tsv`；预期为 `c85e0687e2cba37572fb8850423a877e84290989762f70d3df93b5e097e1eb3d`。控制者只把该哈希写入 `baseline-hashes.sha256`，新结论锁定前不复制文件。
- [ ] 用 `apply_patch` 创建 `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-scope.tsv`，首行为“形式、语言、小节、原行”四列，其后按本计划“数据接口”的固定范围写入二十五行。
- [ ] 运行 `awk -F'\t' 'NR > 1 && $3 == "知识图谱" && $4 >= 209 && $4 <= 220 {print $1 "\t" $2 "\t" $3 "\t" $4}' /tmp/kb-terminology-glossary-review.tsv | sort > /tmp/e2-canonical-scope.tsv`，再将 `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-scope.tsv` 除表头外的行排序后与它比较；预期二十五行且无差异。
- [ ] 用 `apply_patch` 创建 `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-source-input.tsv`，列为“形式、语言、小节、原行、当前定义、当前出处”。前四列取本计划的固定身份表，后两列按“当前定义”表与原行做等值组合。该文件不读取审查表的第五至第十列。
- [ ] 运行 `test "$(tail -n +2 .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-source-input.tsv | wc -l | tr -d ' ')" = 25`，再将前四列排序后与 `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-scope.tsv` 比较；预期无差异。
- [ ] 把 `/tmp/kb-terminology-glossary-review.tsv`、`/tmp/kb-extract-glossary-forms.py` 和 `/tmp/kb-merge-review-decisions.py` 分别镜像到 `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/review-pre-e2.tsv`、`.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-before.py` 和 `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/kb-merge-review-decisions.py`，再记录四个文件的 SHA-256。镜像后重跑哈希，不得只记录路径。
- [ ] 运行 `awk -F'\t' 'NR > 1 {count++; key=$1 FS $2 FS $3 FS $4; if (seen[key]++) dup++; if ($5 == "" && $6 == "" && $7 == "" && $9 == "" && $10 == "") blank++; else if ($5 == "" || $6 == "" || $7 == "" || $9 == "" || $10 == "") half++} END {print "count=" count, "duplicate=" dup+0, "blank=" blank+0, "half=" half+0; exit !(count == 348 && dup == 0 && blank == 0 && half == 0)}' /tmp/kb-terminology-glossary-review.tsv`；预期输出 `count=348 duplicate=0 blank=0 half=0`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`，保存标准错误和退出码；预期非零，且形式集精确为 `domain`、`term`、`内容对象`、`复合概念`、`复合词`、`词` 和`领域`。
- [ ] 用 `apply_patch` 创建 `progress.md` 并记录分支、`HEAD`、`master` 哈希、四个基线哈希、二十五个身份数、三百四十八条完整性和七个既知阻断。
- [ ] 请求一个新审查者只核对基线哈希、固定身份、不含旧决定的研究输入和 `master` 未改；所有 Critical 与 Important 关闭后在 `progress.md` 记录完成。

---

### 核心概念

**Files:**

- Read: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-source-input.tsv`
- Read: `concepts/glossary.md:209`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-core-coverage.tsv`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-core-decisions.tsv`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-core-report.md`

**Interfaces:**

- Consumes: 原行 209–214 的十四个固定身份、原术语表定义和当前出处；不消费旧 E2 决定。
- Produces: 每个形式的三类断言来源范围、十四个完整候选决定和可独立复核的报告。

- [ ] 实施者开始前运行 `test ! -e .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-old-decisions.tsv`；预期退出码为 0。实施者的允许输入只有本任务列出的文件和外部材料，不得打开首轮 E2 决定、报告或当前审查表的决定列。
- [ ] 从 `e2-source-input.tsv` 提取原行 209–214，核对身份集精确为 `triple`、`三元组`、`entity`、`实体`、`edge`、`relation`、`关系`、`property`、`属性`、`schema`、`Schema`、`reasoning`、`inference` 和`推理`；预期十四个且无重复。
- [ ] 在检索前把每个原行所需来源类别写入 `e2-core-report.md` 的“来源范围”：当前列明来源、相关官方规范正文、中文形式所需的官方或权威中文材料、用于区分概念边界的原始论文，以及正文不可访问时的官方出版记录。
- [ ] 打开并核对 [RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/)的 RDF triple、IRI、literal、blank node 和 entailment 位置，以及 [RDF 1.1 Semantics](https://www.w3.org/TR/rdf11-mt/) 的 entailment rules 位置。只记录实际打开的小节和锚点。
- [ ] 打开并核对 [OWL 2 Web Ontology Language Document Overview](https://www.w3.org/TR/owl2-overview/) 中 semantics、inference 和 reasoning task 的实际位置；不把 reasoning、inference 和 entailment 自动当作同义形式。
- [ ] 打开并核对 [GB/T 42131-2022 官方在线预览](https://openstd.samr.gov.cn/bzgk/std/showGb?type=online&hcno=7A66CBA23AB56C22019DE17B44E1C27D&request_locale=zh) 的“实体 entity”、“图式 schema”、“属性 attribute”和“关系 relation”条目。记录它支持的精确形式与定义，不把 `attribute` 改写为 `property`，不把“图式”改写为 `Schema` `zh` 形式。
- [ ] 打开并核对 Hogan 等的 [Knowledge Graphs](https://arxiv.org/abs/2003.02320) 及其 PDF 中的知识图谱定义、directed edge-labelled graph、schema 和 property graph 位置。分别记录 node/entity、edge/relation 和 property/value 的原文边界，不因同一段并列出现就判为同一概念。
- [ ] 为 `三元组`、`实体`、`关系`、`属性`、`Schema` 和`推理` 分别搜索并打开相关官方中文标准或权威中文出版物。已知候选包括 IFLA 官方中文出版物；只把实际读到的形式、定义或对应记入来源范围表。
- [ ] 用 `apply_patch` 整体写入 `e2-core-coverage.tsv`。每个形式必须同时有“形式”、“定义”和“对应”三类断言记录；无直接依据时仍保留已核材料、核对日期和未读边界。
- [ ] 运行 `awk -F'\t' 'NR > 1 {key=$1 FS $2 FS $3 FS $4; if (!keys[key]++) forms++; unit[key FS $5]=1; if (NF != 11 || $7 == "" || $8 == "" || $9 == "" || $10 == "") bad=1} END {for (key in keys) if (!unit[key FS "形式"] || !unit[key FS "定义"] || !unit[key FS "对应"]) bad=1; print "forms=" forms; exit !(forms == 14 && !bad)}' .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-core-coverage.tsv`；预期输出 `forms=14` 且退出码为 0。
- [ ] 根据完成的来源范围表，用 `apply_patch` 整体写入 `e2-core-decisions.tsv`。对每个形式重新判断“依据结论”、“依据位置”、“概念对应”、“动作”和“处理阶段”；非“基本单位”只允许 `keep / 已核` 或 `defer / 术语迁移`。
- [ ] 运行九列表机械检查：表头精确、十四个唯一四列键、键集等于原行 209–214 范围、值域合法；“有依据”必须有带标题的锚定链接，其他结论必须以“检索记录：2026-08-29”开头并含链接。
- [ ] 用 `apply_patch` 整体写入 `e2-core-report.md`，小节依次为“复核范围”、“来源范围”、“逐项结论”、“未读边界”和“机械检查”。报告必须明确说明六个原行为什么完成，不得使用运行时长作理由。
- [ ] 请求新审查者对十四个形式全量复核，逐项检查来源位置、当前定义边界、语言归属、同组对应和未读边界。不以抽样代替全量复核，不读旧 E2 决定。
- [ ] 关闭审查反馈后，记录三个产物的 SHA-256 和十四个结论的 `keep` / `defer` 计数；不合并审查表，不创建 Git 提交。

---

### 规范名称

**Files:**

- Read: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-source-input.tsv`
- Read: `concepts/glossary.md:215`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-names-coverage.tsv`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-names-decisions.tsv`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-names-report.md`

**Interfaces:**

- Consumes: 原行 215–220 的十一个固定身份、原术语表定义和当前出处；不消费旧 E2 决定。
- Produces: 每个形式的规范身份、语言形式、定义和对应来源范围，以及十一个完整候选决定。

- [ ] 实施者开始前运行 `test ! -e .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-old-decisions.tsv`；预期退出码为 0。实施者不得打开首轮 E2 决定、报告或当前审查表的决定列。
- [ ] 从 `e2-source-input.tsv` 提取原行 215–220，核对身份集精确为 `Resource Description Framework`、`RDF`、`RDFS`、`OWL`、`SPARQL`、`Simple Knowledge Organization System`、`SKOS`、`property graph`、`属性图`、`Cypher` 和 `GQL`；预期十一个且无重复。
- [ ] 在检索前把每个原行所需来源类别写入 `e2-names-report.md` 的“来源范围”：当前列明来源、发布机构的官方规范正文、中文记录所需的官方或权威中文材料、原始论文，以及正文不可访问时的官方出版记录。
- [ ] 分别打开并核对 [RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/)、[RDF Schema 1.1](https://www.w3.org/TR/rdf-schema/)、[OWL 2 Web Ontology Language Document Overview](https://www.w3.org/TR/owl2-overview/)、[SPARQL 1.1 Overview](https://www.w3.org/TR/sparql11-overview/) 和 [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/skos-reference/)。规范标题或缩写展开只能支持相应形式与身份，不自动支持当前定义或 `zh` 语言归属。
- [ ] 为 `RDF`、`RDFS`、`OWL`、`SPARQL` 和 `SKOS` 分别搜索并打开权威中文材料。已知候选包括 IFLA 官方中文出版物；每个形式分别记录它是正文用语、术语表形式、缩写还是未出现，不从其他缩写类推。
- [ ] 打开并核对 Hogan 等 [Knowledge Graphs](https://arxiv.org/abs/2003.02320) 的 property graph 定义，再搜索并打开可直接支持“属性图”与 `property graph` 对应的官方中文标准或权威中文文献。英文论文只能支持英文形式和概念边界。
- [ ] 打开并核对 [ISO/IEC 39075:2024 官方记录](https://www.iso.org/standard/76120.html) 及其官方可访问样张，分别记录标准身份、GQL 名称、property graph 范围和未取得正文。官方记录不能代替未读正文中的定义。
- [ ] 打开并核对 [openCypher](https://opencypher.org/) 对 Cypher、openCypher 和 GQL 的实际陈述。将发布者英文页面与 ISO 标准身份分开，不把它们当作 `Cypher` 或 `GQL` 作为 `zh` 记录的直接依据。
- [ ] 为 `Cypher` 和 `GQL` 逐项搜索并打开官方中文标准、官方中文出版页或权威中文文献。只有材料在中文语境中直接使用形式并能定位时，才能支持 `zh` 形式；查不到时写明已核范围，不回用英文页面。
- [ ] 用 `apply_patch` 整体写入 `e2-names-coverage.tsv`。每个形式必须同时有“形式”、“定义”和“对应”三类断言记录；每个中文记录要明示它的中文材料核对结果。
- [ ] 运行 `awk -F'\t' 'NR > 1 {key=$1 FS $2 FS $3 FS $4; if (!keys[key]++) forms++; unit[key FS $5]=1; if (NF != 11 || $7 == "" || $8 == "" || $9 == "" || $10 == "") bad=1} END {for (key in keys) if (!unit[key FS "形式"] || !unit[key FS "定义"] || !unit[key FS "对应"]) bad=1; print "forms=" forms; exit !(forms == 11 && !bad)}' .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-names-coverage.tsv`；预期输出 `forms=11` 且退出码为 0。
- [ ] 根据完成的来源范围表，用 `apply_patch` 整体写入 `e2-names-decisions.tsv`。非“基本单位”只允许 `keep / 已核` 或 `defer / 术语迁移`；规范身份成立但当前定义或语言归属未得支持时，不得用 `keep`。
- [ ] 运行九列表机械检查：表头精确、十一个唯一四列键、键集等于原行 215–220 范围、值域和依据格式合法。另加断言：任何 `zh` 形式的“有依据”不得只引用英文 W3C、ISO、openCypher 或英文论文。
- [ ] 用 `apply_patch` 整体写入 `e2-names-report.md`，小节依次为“复核范围”、“来源范围”、“语言依据”、“逐项结论”、“未读边界”和“机械检查”。
- [ ] 请求新审查者对十一个形式全量复核，逐项检查规范身份与定义依据是否被混用、缩写是否被错当中文依据、同组概念对应是否直接成立，以及未读正文是否被写成已核事实。
- [ ] 关闭审查反馈后，记录三个产物的 SHA-256 和十一个结论的 `keep` / `defer` 计数；不合并审查表，不创建 Git 提交。

---

### 整批复核

**Files:**

- Read: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-core-coverage.tsv`
- Read: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-core-decisions.tsv`
- Read: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-names-coverage.tsv`
- Read: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-names-decisions.tsv`
- Read after lock only: `.superpowers/sdd/2026-08-28-terminology-concept-foundations/task-5-artifacts/task-5-batch-e2-decisions.tsv`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-new-decisions-locked.tsv`
- Create after lock: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-old-decisions.tsv`
- Create after lock: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-old-new.diff`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/review-post-e2.tsv`
- Modify: `/tmp/kb-terminology-glossary-review.tsv`

**Interfaces:**

- Consumes: 两个已审查来源范围表、二十五个候选决定、冻结的完整审查表和原子合并器。
- Produces: 二十五个独立复核后的锁定决定、新旧差异记录和只替换 E2 决定列的完整审查表。

- [ ] 将两个九列决定表去除重复表头后整合为 `e2-new-decisions-locked.tsv`；使用 `apply_patch` 整体写入，不在已有文件尾部追加。
- [ ] 运行机械检查：表头精确、二十五个唯一四列键、与 `e2-scope.tsv` 的键集无差异、与两个输入决定的行内容无差异。
- [ ] 对锁定决定按“小节、原行”建组，只计算 `keep` 形式：零个时不检查保留对应，一个时要求“有依据 / 不适用”，两个以上时无论语言种数都要求每个为“有依据 / 同一概念”。预期没有违规组。
- [ ] 运行 `shasum -a 256 .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-new-decisions-locked.tsv > .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-new-decisions-locked.sha256`，再运行 `test ! -e .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-old-decisions.tsv`；预期退出码为 0。这个哈希是新结论不沿用旧结论的时序证据。
- [ ] 请求一个没有参与两个研究任务的新审查者，仅使用原术语表、两个来源范围表、两个报告和锁定决定，对全部二十五个形式逐项审查。审查者不得读取旧 E2 决定。
- [ ] 审查者必须分别回答：形式语言是否直接成立，当前定义是否落在来源边界内，同原行保留形式是否有直接同概念依据，以及来源类别是否已核或明示不可访问。
- [ ] 任何 Critical 或 Important 反馈都交回原组实施者，整体重写受影响的来源范围行、九列决定行和报告的“逐项结论”小节。每轮后重建整个锁定表、更新哈希并再审，最多五轮。
- [ ] 独立审查无 Critical 或 Important 后，才把首轮 E2 决定复制为 `e2-old-decisions.tsv`，并再次验证其 SHA-256 为 `c85e0687e2cba37572fb8850423a877e84290989762f70d3df93b5e097e1eb3d`。
- [ ] 分别按四列键排序新旧九列表，运行 `diff -u` 并把结果写入 `e2-old-new.diff`。`diff` 的 0 或 1 都是有效结果；大于 1 时停止。
- [ ] 对新旧每个变化的四列键，在对应组报告的“逐项结论”中增加“旧结论、新结论、变化依据”。没有变化的键也要有本轮新查材料位置，不得用“同旧版”代替。
- [ ] 在合并前把 `/tmp/kb-terminology-glossary-review.tsv` 与 `review-pre-e2.tsv` 做 SHA-256 比较；预期相同。任何中间变化都必须停止并查明。
- [ ] 运行 `python3 /tmp/kb-merge-review-decisions.py .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/e2-new-decisions-locked.tsv /tmp/kb-terminology-glossary-review.tsv 25`；预期输出 `merged=25 preserved=323 total=348`。
- [ ] 把合并后审查表镜像为 `review-post-e2.tsv`。用前四列键过滤 E2 后，比较 `review-pre-e2.tsv` 和 `review-post-e2.tsv`；预期三百二十三个非 E2 行逐字节相同。
- [ ] 分别从合并前后文件提取“形式、语言、小节、原行、全库引用”并排序比较；预期三百四十八个消费者单元全部相同。
- [ ] 重跑完整性检查；预期仍为 `count=348 duplicate=0 blank=0 half=0`。运行 `guard-removals`；预期仍只报七个已知“基本单位”形式。
- [ ] 记录新锁定决定、新完整审查表、两个来源范围表和新旧差异的 SHA-256；在 `progress.md` 记录新结论计数和审查轮次。
- [ ] 请求最后一个范围审查：只有 E2 的二十五个决定单元变化，非 E2 行与所有消费者不变，没有项目文件或 Git 提交。关闭反馈后才进入校验器。

---

### 校验修正

**Files:**

- Read: `/tmp/kb-extract-glossary-forms.py`
- Read: `.superpowers/sdd/2026-08-28-terminology-concept-foundations/task-5-artifacts/task-5-validate-review-tests.py`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-tests.py`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-red.out`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-green.out`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-regression.md`
- Modify: `/tmp/kb-extract-glossary-forms.py`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-after.py`

**Interfaces:**

- Consumes: 已整批合并的 E2 审查表、冻结校验器和八个既有行为测试。
- Produces: 按保留形式数量校验概念对应、按完整分组校验未完成状态的临时校验器，以及覆盖正反例的测试集。

- [ ] 把既有八个行为测试整体复制到 `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-tests.py`，将 `SCRIPT` 保持为 `/tmp/kb-extract-glossary-forms.py`。运行 `python3 .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-tests.py`；预期八个测试全部通过。
- [ ] 整体重写 `ValidateReviewBehaviorTests` 类，保留原八个测试，并加入以下六个方法；测试数固定为十四个：

```python
    def test_single_survivor_rejects_same_concept(self) -> None:
        fixture = HEADER + (
            "alpha-label\ten\t基本单位\t33\t有依据\t[Authority alpha](https://authority.example/spec#alpha)\t同一概念\t无引用\tkeep\t基本单位\n"
        )
        self.assert_invalid(fixture, "single survivor requires 不适用")

    def test_same_language_survivors_reject_not_applicable(self) -> None:
        fixture = HEADER + (
            "alpha-label\ten\t基本单位\t33\t有依据\t[Authority alpha](https://authority.example/spec#alpha)\t不适用\t无引用\tkeep\t基本单位\n"
            "alpha-name\ten\t基本单位\t33\t有依据\t[Authority alpha](https://authority.example/spec#name)\t不适用\t无引用\tkeep\t基本单位\n"
        )
        self.assert_invalid(fixture, "multiple survivors require 同一概念")

    def test_same_language_survivors_with_same_concept_pass(self) -> None:
        fixture = HEADER + (
            "alpha-label\ten\t基本单位\t33\t有依据\t[Authority alpha](https://authority.example/spec#alpha)\t同一概念\t无引用\tkeep\t基本单位\n"
            "alpha-name\ten\t基本单位\t33\t有依据\t[Authority alpha](https://authority.example/spec#name)\t同一概念\t无引用\tkeep\t基本单位\n"
        )
        self.assert_valid(fixture)

    def test_wholly_unreviewed_group_passes_when_allowed(self) -> None:
        fixture = HEADER + (
            "alpha-label\ten\t建设与治理\t106\t\t\t\t无引用\t\t\n"
            "甲项\tzh\t建设与治理\t106\t\t\t\t无引用\t\t\n"
        )
        self.assert_valid(fixture, "--allow-incomplete")

    def test_mixed_complete_and_unreviewed_group_fails_when_allowed(self) -> None:
        fixture = HEADER + (
            "alpha-label\ten\t建设与治理\t106\t有依据\t[Authority alpha](https://authority.example/spec#alpha)\t不适用\t无引用\tkeep\t已核\n"
            "甲项\tzh\t建设与治理\t106\t\t\t\t无引用\t\t\n"
        )
        self.assert_invalid(
            fixture,
            "mixes complete and unreviewed members",
            "--allow-incomplete",
        )

    def test_partially_filled_row_fails_when_incomplete_is_allowed(self) -> None:
        fixture = HEADER + (
            "pending-label\ten\t建设与治理\t106\t有依据\t\t\t无引用\t\t\n"
        )
        self.assert_invalid(
            fixture,
            "partially filled decision columns",
            "--allow-incomplete",
        )
```

- [ ] 运行 `python3 .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-tests.py > .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-red.out 2>&1`；预期非零，新增的单保留形式、同语言多保留形式和混合完整分组用例失败，测试框架没有导入或语法错误。
- [ ] 在修正前冻结非 `validate-review` 行为：分别运行 `extract`、`extract-forms`、`audit-consumers`、`refresh-consumers` 和 `guard-removals`，把输出、标准错误与退出码保存到 `artifacts/validator-baseline-*`。
- [ ] 整个重写 `/tmp/kb-extract-glossary-forms.py` 的 `validate_review()` 函数。在读取每行时，先完成十列、身份、消费者和重复键检查，再按五个决定单元计算状态：

```python
        decisions = [cells[index] for index in decision_indexes]
        filled = sum(value != "" for value in decisions)
        if filled == len(decisions):
            state = "complete"
        elif filled == 0:
            state = "unreviewed"
        else:
            state = "partial"
        rows.append((line_number, cells, state))

        if state == "partial":
            incomplete += 1
            errors.append(
                f"review row {line_number} has partially filled decision columns"
            )
            continue
        if state == "unreviewed":
            incomplete += 1
            if not allow_incomplete:
                errors.append(
                    f"review row {line_number} has incomplete decision columns"
                )
            continue
```

- [ ] 保留现有完成行的值域、依据格式、新增身份、删除消费者、“基本单位”和处理阶段检查；这些检查只对 `state == "complete"` 的行执行。
- [ ] 在所有行读取后，用全部 `rows` 建立分组，不先丢弃未审行。按以下代码先校验分组状态：

```python
    groups = {}
    for line_number, cells, state in rows:
        groups.setdefault((cells[2], cells[3]), []).append(
            (line_number, cells, state)
        )

    for group, members in groups.items():
        states = {state for _, _, state in members}
        if "partial" in states:
            continue
        if states == {"unreviewed"}:
            continue
        if states == {"complete", "unreviewed"}:
            errors.append(
                f"entry group {group!r} mixes complete and unreviewed members"
            )
            continue
        if states != {"complete"}:
            continue
```

- [ ] 在同一分组循环中，只对全部完成的分组计算 `keep` 或 `add` 保留形式。以保留形式数量取代语言种数：

```python
        survivors = [
            (line_number, cells)
            for line_number, cells, _ in members
            if cells[8] in {"keep", "add"}
        ]
        if not survivors:
            continue
        expected_correspondence = (
            "不适用" if len(survivors) == 1 else "同一概念"
        )
        for line_number, cells in survivors:
            if cells[4] != "有依据":
                errors.append(
                    f"review row {line_number} entry group {group!r} "
                    "survivor requires 有依据"
                )
            if cells[6] != expected_correspondence:
                if len(survivors) == 1:
                    errors.append(
                        f"review row {line_number} entry group {group!r} "
                        "single survivor requires 不适用"
                    )
                else:
                    errors.append(
                        f"review row {line_number} entry group {group!r} "
                        "multiple survivors require 同一概念"
                    )
```

- [ ] 保留默认模式下未审行失败的现有行为。`--allow-incomplete` 只使整组 `unreviewed` 通过；完成与未审混合必须失败，任何 `partial` 必须失败。
- [ ] 运行 `python3 .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-tests.py > .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/validator-green.out 2>&1`；预期十四个测试全部通过。
- [ ] 建立两个反向变异检查：把同语言两个保留形式的“同一概念”改为“不适用”，把混合分组的空行拆成新原行。前者必须失败，后者在 `--allow-incomplete` 下必须通过，证明失败来自准确分组而不是“存在空行”的粗糙规则。
- [ ] 重跑 `extract`、`extract-forms`、`audit-consumers`、`refresh-consumers` 和 `guard-removals`，与 `validator-baseline-*` 逐字节比较输出、标准错误和退出码；预期全部相同。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py validate-review /tmp/kb-terminology-glossary-review.tsv`；预期非零且只包含七个已知 `remove` 消费者错误，不得包含保留形式数量或混合分组错误。
- [ ] 把修正后脚本镜像为 `validator-after.py`，记录 SHA-256，并整体写入 `validator-regression.md`。报告小节为“失败复现”、“完整状态”、“保留形式”、“既有行为”和“适用边界”；“适用边界”明记校验器不替代来源研究。
- [ ] 请求新审查者先核对规格规则与十四个测试，再审查整个 `validate_review()` 函数。重点检查空行是否在建组前被丢弃、相同语言是否仍成为豁免条件，以及是否新增了来源充分性启发式。
- [ ] 关闭反馈后，用 SHA-256 确认 `/tmp/kb-extract-glossary-forms.py` 与 `validator-after.py` 相同，在 `progress.md` 记录十四个测试、两个反向变异和五种既有模式的结果。

---

### 全表回归

**Files:**

- Read: `concepts/glossary.md`
- Read: `/tmp/kb-terminology-glossary-review.tsv`
- Read: `/tmp/kb-extract-glossary-forms.py`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/full-regression.md`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/full-identities.tsv`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/full-consumers.tsv`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/full-structural-probe.tsv`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/removal-blockers.txt`

**Interfaces:**

- Consumes: 已合并 E2 新结论的完整审查表和已通过行为测试的校验器。
- Produces: 三百四十八条身份、值域、完整性、分组和依据格式全部通过的证据，以及仅由七个已知形式组成的删除保护失败集。

- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py extract-forms concepts/glossary.md .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/full-identities.tsv`；预期除表头外三百四十八行、四列键无重复。
- [ ] 从 `/tmp/kb-terminology-glossary-review.tsv` 提取前四列并排序，与 `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/full-identities.tsv` 排序后比较；预期无差异。这一步证明审查表仍完整对应当前术语表，不用旧的 348 数量单独代替身份比较。
- [ ] 运行 `refresh-consumers` 生成临时刷新表，分别比较刷新前后的四列键和五个决定单元；预期全部相同。再用刷新表原子替换 `/tmp/kb-terminology-glossary-review.tsv`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py audit-consumers /tmp/kb-terminology-glossary-review.tsv .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/full-consumers.tsv`，再将它与审查表的“形式、语言、小节、原行、全库引用”排序比较；预期无差异。
- [ ] 运行完整性检查；预期 `count=348 duplicate=0 blank=0 half=0`。另外统计九列决定值域；预期没有空值或超出已批准临时值域的值。
- [ ] 用 `awk -F'\t' 'BEGIN {OFS="\t"} NR == 1 {print; next} $9 == "remove" && $8 != "无引用" {$8="无引用"} {print}' /tmp/kb-terminology-glossary-review.tsv > .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/full-structural-probe.tsv` 生成结构探针。该探针只在副本中屏蔽已登记删除阻断，不改动动作、依据、概念对应或处理阶段。
- [ ] 在建立探针前，从真实审查表提取 `$9 == "remove" && $8 != "无引用"` 的形式，排序后与下列固定集比较：`domain`、`term`、`内容对象`、`复合概念`、`复合词`、`词`、`领域`。预期七个且无差异；不允许探针自动屏蔽新形式。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py validate-review .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/full-structural-probe.tsv`；预期退出码为 0。这证明身份、值域、完整性、依据格式和分组除已知删除保护外全部通过。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py validate-review /tmp/kb-terminology-glossary-review.tsv`，保存标准输出、标准错误和退出码；预期非零。错误只能是上述七个行的 `remove still has consumers`，不得有其他诊断。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv 2> .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/removal-blockers.txt`；预期非零。从标准错误中提取冒号前形式，与固定七形式集比较；预期无差异。
- [ ] 比较 `review-post-e2.tsv` 和刷新后审查表的四列键、依据结论、依据位置、概念对应、动作和处理阶段；预期无差异。只有消费者列允许因当前 `HEAD` 发生可解释的刷新。
- [ ] 整体写入 `full-regression.md`，小节为“身份集合”、“完整状态”、“依据分组”、“消费者”、“删除保护”和“进入复核”。报告必须把“结构探针通过”与“真实删除保护预期失败”分开陈述。
- [ ] 记录审查表、完整身份、消费者、结构探针、删除阻断和回归报告的 SHA-256。
- [ ] 请求新审查者复核三百四十八个身份对应、探针只屏蔽固定七形式、真实校验只有固定七错误、E2 外决定不变和 `master` 未改。反馈关闭后才标记回归完成。

---

### 基本单位

**Files:**

- Read: `/tmp/kb-terminology-glossary-review.tsv`
- Read: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/full-consumers.tsv`
- Read: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/removal-blockers.txt`
- Read: `.superpowers/sdd/2026-08-28-terminology-concept-foundations/progress.md`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/build-basic-unit-handoff.py`
- Create: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/basic-unit-handoff.tsv`
- Modify: `.superpowers/sdd/2026-08-28-terminology-concept-foundations/progress.md`
- Modify: `.superpowers/sdd/2026-08-29-e2-evidence-review-validator/progress.md`

**Interfaces:**

- Consumes: 已通过结构回归的三百四十八条审查表、七个精确删除阻断和高召回消费者候选。
- Produces: 原计划 Task 5 可以直接接管的“基本单位”复核输入，不提前完成语义分类、迁移或术语准入。

- [ ] 从真实审查表提取七个固定阻断的四列键、当前决定和原始消费者单元。形式集必须再次精确等于 `domain`、`term`、`内容对象`、`复合概念`、`复合词`、`词` 和`领域`。
- [ ] 用 `apply_patch` 创建 `build-basic-unit-handoff.py`，内容精确为以下脚本：

```python
#!/usr/bin/env python3
import csv
from pathlib import Path
import sys


BLOCKERS = {
    "domain",
    "term",
    "内容对象",
    "复合概念",
    "复合词",
    "词",
    "领域",
}
HEADER = [
    "形式",
    "语言",
    "小节",
    "原行",
    "位置",
    "候选分类",
    "处理说明",
]


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: build-basic-unit-handoff.py REVIEW_TSV OUTPUT_TSV")
    review_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    rows = []
    found = set()
    with review_path.open("r", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            if row["动作"] != "remove" or row["全库引用"] == "无引用":
                continue
            form = row["形式"]
            found.add(form)
            for location in row["全库引用"].split(";"):
                rows.append(
                    [
                        form,
                        row["语言"],
                        row["小节"],
                        row["原行"],
                        location,
                        "",
                        "",
                    ]
                )
    if found != BLOCKERS:
        raise SystemExit(
            f"unexpected removal blockers: expected={sorted(BLOCKERS)!r} "
            f"actual={sorted(found)!r}"
        )
    rows.sort(key=lambda row: (row[0], row[4]))
    with output_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(HEADER)
        writer.writerows(rows)
    print(f"blockers={len(found)} candidates={len(rows)}")


if __name__ == "__main__":
    main()
```

- [ ] 运行 `python3 .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/build-basic-unit-handoff.py /tmp/kb-terminology-glossary-review.tsv .superpowers/sdd/2026-08-29-e2-evidence-review-validator/artifacts/basic-unit-handoff.tsv`。当前预期输出 `blockers=7 candidates=623`；数量不同时不直接判失败，先用 `full-consumers.tsv` 与当前 `HEAD` 解释新增或消失位置，并把差异记入交接报告。
- [ ] 核对 `basic-unit-handoff.tsv` 表头精确为“形式、语言、小节、原行、位置、候选分类、处理说明”。前五列必须全部完整，后两列必须全部为空，因为它们是原计划的待审决定单元，不在本计划里预填。
- [ ] 将 `basic-unit-handoff.tsv` 的前四列与审查表中七个阻断键比较，并将每个“形式、位置”重新聚合为分号单元与原审查表比较；预期没有丢失、新增或重复候选。
- [ ] 在原计划 `progress.md` 追加交接记录：E2 二十五个形式已重新复核，校验器两个缺口已经测试修正，三百四十八条结构回归通过，删除保护精确阻断七个形式，“基本单位”复核现在进入消费者语义分类。
- [ ] 在交接记录中保留两个既有开放问题：英文 `term` 是否应以单语形式保留或重建，以及必要的新增形式如何取得直接依据。两者都不在交接时自动作结论。
- [ ] 明确原计划的候选分类值仍为“字符串误命中”、“来源陈述”、“实际消费者”和“待人判断”。原始高召回检测仍作为无漏记输入，校验器不根据字符串自动分类。
- [ ] 记录 `basic-unit-handoff.tsv`、最终审查表、最终校验器、E2 锁定决定和全表回归报告的 SHA-256。
- [ ] 请求新审查者核对交接的七形式集、所有原始位置、未预填的分类单元、两个开放问题和原计划的处理边界。
- [ ] 关闭反馈后，在两个 `progress.md` 中将本计划标记为完成、将原计划 Task 5 的“基本单位”标记为进行中。下一个子代理从语义分类开始，不再重做 E2 研究或校验器设计。
- [ ] 运行 `git status --short --branch`；预期没有执行产物进入 Git。再检查 `/Users/xiu/code/kb-design` 的 `master` 状态和哈希；预期仍无修改且为 `6370e647518f6b98174b84665a0b9392256892d9`。

---

## 验收标准

本实施计划完成时，以下条件必须同时成立：

- E2 二十五个形式全部有形式、定义和概念对应的来源范围记录，没有因运行时长停止研究。
- 新 E2 结论在读取旧结论前已用 SHA-256 锁定，旧结论只出现在锁定后的差异对照中。
- 二十五个 E2 决定经过全量独立复核和原子合并，三百二十三个非 E2 行与三百四十八个消费者单元在合并时不变。
- 单个保留形式只能使用“不适用”；两个以上保留形式无论语言是否相同都只能使用“同一概念”，且每个保留形式都必须有直接依据。
- `--allow-incomplete` 只允许整组完全未审；同组完成与未审混合失败，任何半填行失败。
- 十四个校验器行为测试、两个反向变异检查和五种既有模式回归全部符合预期。
- 完整审查表与当前术语表仍为三百四十八个唯一身份，没有空白或半填决定。
- 结构探针通过；真实校验和删除保护仅报告 `domain`、`term`、`内容对象`、`复合概念`、`复合词`、`词` 和`领域`，不报告其他错误。
- “基本单位”收到包含七个阻断及全部原始消费者候选的交接表，原计划 Task 5 已转入消费者语义分类，但没有在本计划中预批准分类、迁移、新增形式或术语准入。
- 功能分支没有新的项目文件变更，`master` 仍无修改且保持固定哈希。
