# 术语实施计划 (Terminology Schema and Generation Implementation Plan)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. 只有写集互斥且没有顺序依赖的实现任务使用 superpowers:dispatching-parallel-agents。独立审查只执行本计划保留的 T12 与 T13 两个高价值门禁。Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在来源治理原子切换完成后，继承既有术语审查结论，建立可审计的术语模式、按风险升级的决定物化、确定性生成、委托、正文诊断和维护接口，并以同时更新来源索引的原子切换启用唯一术语编辑源。

**Architecture:** 实施分为迁移前证据锁和来源切换后共享锁两个阶段。术语侧只导入 `scripts/source_model.py` 的 `Issue`、`ReferenceUse` 和 `validate_references`；schema、角色、错误码、主题、账本、Markdown 与输出从 `decision-source-0005` 绑定的 `source-cutover-handoff.json` 消费，实际应用 entries 从 handoff 绑定的 `source-cutover-payload.json` 消费。已通过 E2 与后迁移回归的 348 行结论无损进入审计账本；只有状态提升、正式准入、概念合并、多语归并或删除产生新增决定。术语切换实现先提交，再生成完整候选和 manifest，决定绑定后只应用既有候选。

**Tech Stack:** Python 3.9.6、来源计划 `requirements-dev.txt` 锁定的 PyYAML 6.0.3 与 jsonschema 4.23.0、`unittest`、JSON Schema 2020-12、Markdown、YAML、JSON、TSV、Git。

**Spec:** [术语治理设计](../specs/2026-08-27-terminology-governance-design.md)、[来源治理草案](../../../design/drafts/source-governance.md)、[术语治理草案](../../../design/drafts/terminology-governance.md)、[术语计划输入](../../../.superpowers/sdd/2026-08-31-governance-implementation-prep/terminology-plan-input.md)、[跨计划审查](../../../.superpowers/sdd/2026-08-31-governance-implementation-prep/plan-interface-review.md)

## 全局约束

- 实施分支固定为 `feat/terminology-governance`；迁移前证据提交固定为 `9e7b411c23e890d13d70fc16d443b760313126c4`。
- 旧来源草案和旧术语草案从冻结 Git 对象读取，不从来源切换后的工作树读取。ignored 库存按计划输入登记的 SHA-256 校验。
- T01–T13 都以后置的 `decision-source-0005` 为前置。该决定必须 accepted，且 front matter 的来源交付键恰为 `delivery_handoff`、`handoff_sha256`、`delivery_payload`、`payload_sha256`；handoff 路径固定为 `vocab/generated/source-cutover-handoff.json`，payload 路径固定为 `vocab/generated/source-cutover-payload.json`。
- source handoff 的顶层键恰为 `schema`、`schema_version`、`payload`、`source_contract`、`schemas`、`topics_sha256`、`migration_ledgers`、`markdown_manifest`、`outputs`、`tracked_write_set`。`payload` 恰含 `path` 与 `sha256`；source payload 的顶层键恰为 `schema`、`schema_version`、`entries`。
- 术语计划不硬编码来源 schema `$id`、版本、角色资格或错误码。`schemas/terms-v1.schema.json` 只从 handoff 顶层 `schemas` 构造本地引用；`source_contract` 只消费 `module`、`sha256`、`reference_kinds`、`role_qualifications`、`error_codes`，不嵌套 schema，也不使用 `module_sha256`。
- 来源计划与术语计划不得并行修改 `scripts/build-topics.py`、`scripts/check-topics.py`、`design/topics.md`、`design/governance.md`、`design/maintenance.md`、`design/README.md`、`AGENTS.md` 或 `README.md`。术语任务只从 `decision-source-0005` 的切换提交继续。
- 当前阶段零自定。普通叙述、来源转录、路径、代码、值、测试夹具、字符串命中、`defer`、`keep`、`remove` 和迁移处置都不取得 designation 准入资格。
- `basis`、`source`、`match` 的迁移职责留在来源计划；术语侧只把术语记录中的引用包装成 `ReferenceUse` 并交给 `validate_references`。
- `vocab/terms.yaml` 只允许 `schema`、`version`、`concepts` 三个顶层键。概念、语言、术语分层；概念工作流与术语管理状态分开；`unassigned` 不进入术语工作流。
- 同一概念、同一语言恰有一个优先术语。优先术语替换、管理状态、`replaced_by`、委托与所有权切换都按“概念身份加语言”原子验证。
- 348 个术语表身份按冻结四元身份逐行对账；946 个词表标签身份按现有所有者对账。对账只证明身份和旧结论被继承，不重新研究依据，不按字符串去重，不猜测 20 个 `und` 的语言，也不合并两个“属性”身份。
- `review-post-e2.tsv`、后迁移审查结果和 `term-glossary.tsv` 的身份、依据结论、概念对应与动作是冻结迁移输入。286 个 `defer` 进入审计，56 个 `keep` 保留原所有权，6 个 `remove` 在没有 L3 删除决定时保留；三类都不因迁移取得新效力。
- 人的新增决定只覆盖会改变既有结论或效力的升级行，通过 `vocab/migrations/term-v1/decisions.tsv` 输入，并由 `decision-term-0002` 绑定哈希。`vocab/migrations/term-v1/terms.tsv` 确定性覆盖全部 348 行；没有升级决定的行直接继承冻结结论。
- `decision-source-0005` 登记的主题文件哈希是术语起点；术语任务不得继续使用来源迁移前 `vocab/topics.yaml` 的字节哈希作为后置断言。700 个概念、24 个数组和稳定 ID 集合仍须保持，除非决定清单逐项解释变化。
- Markdown 范围永不使用固定数量。每批从 `git ls-files -z -- '*.md'` 生成路径与 SHA-256 清单；与来源后置清单和本批允许写集比较，任何未解释增删改都阻断。
- `concepts/glossary.md`、受委托标签、正文诊断、`vocab/generated/terms-v1.json`、`vocab/generated/term-reference-index.json` 与 `vocab/generated/source-reference-index.json` 必须在同一暂存根生成并验证。
- TBX、Obsidian、应用导入、往返编辑、来源改档、生活范围、实体归属、三份旁路草案生效和发版不在本计划写集。
- [证据阶段决定](../../../design/decisions/evidence-stage-boundary.md)允许当前阶段实现 T01–T11 的模式、校验、迁移、生成、委托诊断、维护和切换工具；T12 完整正式候选、T13 严格应用及真实术语准入留到来源证据下一阶段闭合后执行。当前工具实现不改变术语表所有权。
- `decision-term-0001` 与 `decision-term-0002` 分别先于其模式和真实迁移数据任务提交。`decision-term-0003`、`decision-term-0004`、`decision-term-0005` 绑定的是 T11 实现提交之后才存在的完整 candidate 与 manifest，因此只能在 T12 生成、预验并经人复核后提交；不得把这三份决定前置到 T11。
- T11 只实现并提交 `cutover_terms.py`、两份测试和夹具；真实 candidate 与真实 manifest 必须不存在。T11 只运行不需要真实 candidate、manifest 或 cutover decision 的 69 项高风险测试，其中切换侧 8 项全部使用临时 Git 夹具。
- T12 以干净的 T11 实现提交为 `implementation_commit`，生成完整 ignored candidate 与 ignored manifest，运行 71 项非决定绑定高风险测试及候选结构、哈希、来源严格校验、双索引、动态 Markdown 和草案预验；不得运行任何读取 `decision-term-0003`、`0004` 或 `0005` 的测试。人审通过后才提交这三份决定。
- T13 才运行决定绑定测试、应用已绑定 candidate，并运行 72 项计划高风险门禁。全库发现测试如另行运行，只要求全部通过，不把总数当作验收条件。base→HEAD 允许集合恰为 `design/decisions/terminology-governance-effective.md`、`design/decisions/terminology-schema-cutover.md`、`design/decisions/terminology-schema-rollback.md`；manifest 始终 ignored，不进入 Git。
- 普通实现任务可以用 `git revert` 回退自己的代码提交；正式切换不得反转删除决定、ID、义务或历史，只能按 H13、H23 创建补偿决定与处置提交。
- 只有“测试账本”保留的高风险行为测试执行 RED／GREEN；文档、静态 schema、确定性生成物和纯机械迁移使用直接解析、模式、哈希、差异或端到端门禁，不为 TDD 形式另造测试。每个任务执行定向检查、写集检查、回滚说明和提交。普通任务不派独立审查，不重复运行全库回归；完整回归只在 T03 模式闭合、T06 迁移闭合、T10 消费链闭合、T12 完整候选和 T13 正式应用五个阶段运行。
- 独立审查只保留两次：T12 审查完整候选、身份与决定增量、双索引和回退材料；T13 审查决定绑定、原子应用和正式唯一所有权。测试数量、测试通过、格式或哈希一致等机械事实由命令证明，不再交给独立代理重复确认。
- 已知两处旧 SDD 链接由 `check_known_link_failures.py` 转成“恰好匹配即退出 0”的阶段门禁，不能用会短路后续命令的 `&&` 链。
- 实施证据只写 `.superpowers/sdd/2026-08-31-terminology-schema-generation/`。本计划编写阶段不执行正式 schema、数据、脚本、迁移、决定或提交。

---

## 输入锁

输入锁分为迁移前证据、来源双文件交付和术语候选 payload 三层；后层不能改写前层。

迁移前证据锁从冻结提交读取三个 tracked blob：

| 输入 | 读取方式 | SHA-256 |
|---|---|---|
| 实施准备计划 | `git show 9e7b411c23e890d13d70fc16d443b760313126c4:docs/superpowers/plans/2026-08-31-governance-implementation-prep.md` | `28b936359d49f5c8618d2dff63740497a766da43931fa4f47b7ad6dd9c232ecd` |
| 来源治理草案 | `git show 9e7b411c23e890d13d70fc16d443b760313126c4:design/drafts/source-governance.md` | `0bc61207215f35065652bb66f043ef2d11a807bbe0bc44465814e469b5671526` |
| 术语治理草案 | `git show 9e7b411c23e890d13d70fc16d443b760313126c4:design/drafts/terminology-governance.md` | `2d48c869b8a2119346739303accaaff0cbe40418d7074f29a4a18599950767d7` |

其余十五项 ignored 库存和报告按 `terminology-plan-input.md` 的哈希读取；任何差异都要求重新集成计划输入。

来源交付锁依次验证决定、handoff、payload：

| 对象 | 固定要求 |
|---|---|
| `design/decisions/source-schema-cutover.md` | front matter 的 `id` 为 `decision-source-0005`、`status` 为 `accepted`；`delivery_handoff`、`handoff_sha256`、`delivery_payload`、`payload_sha256` 四个来源交付键齐备 |
| `delivery_handoff` | 精确为 `vocab/generated/source-cutover-handoff.json`；对应文件 SHA-256 等于 `handoff_sha256` |
| `delivery_payload` | 精确为 `vocab/generated/source-cutover-payload.json`；对应文件 SHA-256 等于 `payload_sha256` |
| `vocab/generated/source-cutover-handoff.json` | 顶层键恰为 `schema`、`schema_version`、`payload`、`source_contract`、`schemas`、`topics_sha256`、`migration_ledgers`、`markdown_manifest`、`outputs`、`tracked_write_set` |
| `payload` | 恰含 `path` 与 `sha256`；path 等于 `delivery_payload`，sha256 同时等于 payload 实际 SHA-256 与决定的 `payload_sha256` |
| `source_contract` | 恰按来源计划消费 `module`、`sha256`、`reference_kinds`、`role_qualifications`、`error_codes`；module 为 `scripts/source_model.py`，sha256 绑定该文件 |
| `schemas` | handoff 顶层恰有七项；每项给出 path、`$id`、`schema_version`、`sha256`，集合逐字覆盖来源 `SCHEMA_IDS` |
| `topics_sha256` | 等于 `vocab/topics.yaml` 的来源切换后 SHA-256；`outputs` 中唯一 `kind: topics` 项同时给出 path、同一 SHA-256、concepts=700、arrays=24 |
| `migration_ledgers` | handoff 顶层恰有六份来源账本 path／sha256 |
| `markdown_manifest` | 来源切换后的受跟踪 Markdown path／sha256，不固定数量 |
| `outputs` | 恰含 topics 与 source_index 两项；每项 path／kind／sha256 完整，topics 另含 700／24 |
| `tracked_write_set` | 排序路径集合逐字等于 source payload entries 的 path 集合 |
| `vocab/generated/source-cutover-payload.json` | 顶层键恰为 `schema`、`schema_version`、`entries`；entries 不含 handoff、payload 或先行决定，非删除项 hash 与正式文件一致 |

T01 先运行 `python3 scripts/check_sources.py --root .`，再由统一 `load_source_handoff(repo_root, handoff_path, payload_path, decision_path)` 依次验证决定、handoff 和 payload。loader 不把 schema 放进 `source_contract`，不构造 `topics` 或 `markdown_files` 别名，也不使用 `delivery_manifest`、`payload_manifest_sha256`、`module_sha256`、`tracked_paths`。术语侧不从 payload 推导富契约。

术语候选 payload 锁只在 T12 建立。T11 提交完成时，`.superpowers/sdd/2026-08-31-terminology-schema-generation/candidate-root/` 与同级 `payload-manifest.json` 都必须不存在。T12 以干净的 T11 HEAD 为 `implementation_commit`，从该提交的 Git tree 读取 tracked path 集合，再生成完整 ignored candidate 和不含自身的 ignored manifest。manifest 每项保存 path、action、before_sha256、after_sha256；Delete 的 after_sha256 为 null。manifest 另保存 base_commit、source handoff SHA-256、source payload SHA-256、动态 Markdown 清单、preserve_paths、restore_paths；manifest 路径不进入 entries。

T12 在没有 `decision-term-0003`、`0004`、`0005` 的状态下运行候选结构、逐项哈希、来源严格校验、双索引、动态 Markdown、草案核销和 71 项非绑定高风险测试。人完成候选复核后，`decision-term-0004` 才在 front matter 绑定 ignored manifest 的精确路径与 `payload_manifest_sha256`；candidate root 或 manifest 丢失、移动或任一字节变化时，旧决定失效，必须重新生成候选并新建替代决定。manifest 始终 ignored，不提交副本。

T13 以 T11 `implementation_commit` 为 base，要求 base→HEAD 的路径集合恰为三份先行决定；随后才运行决定绑定测试、应用测试和 72 项计划高风险门禁。三份允许路径固定为：

- `design/decisions/terminology-governance-effective.md`
- `design/decisions/terminology-schema-cutover.md`
- `design/decisions/terminology-schema-rollback.md`

每批开始运行：

```bash
python3 scripts/governance/check_term_inputs.py verify --frozen-commit 9e7b411c23e890d13d70fc16d443b760313126c4 --plan-input .superpowers/sdd/2026-08-31-governance-implementation-prep/terminology-plan-input.md --source-decision design/decisions/source-schema-cutover.md --source-handoff vocab/generated/source-cutover-handoff.json --source-payload vocab/generated/source-cutover-payload.json --batch-output .superpowers/sdd/2026-08-31-terminology-schema-generation/current-input-lock.json
```

预期：迁移前 18 项一致；来源决定的四个键绑定 handoff 与 payload；handoff 十个顶层键、payload 三个顶层键和所有 path／sha256 一致；当前 Markdown 差异全部属于已完成任务写集。T12 运行不读取术语 cutover decision 的 `check_term_inputs.py verify-candidate`；T13 才运行 `check_term_inputs.py verify-payload`，验证术语决定、ignored manifest 与 ignored candidate root 三方绑定。

## 决定锁

以下推荐是待批准提案。每个问题必须由可引用决定答复；会改变既有结论或效力的精确替代答案写入对应机器文件，并由任务测试验证“答案被逐字消费”。冻结结论的机械继承不制造逐行人工答复。

| 标识 | 精确问题 | 推荐选项 | 理由 | 若错误的代价 | 未批准行为 |
|---|---|---|---|---|---|
| H01 | 来源治理草案何时以哪个决定记录生效；来源计划交付给术语校验器的正式调用入口、模式版本和获准用途清单是什么？ | 只有 `decision-source-0004` 已生效，且 accepted `decision-source-0005` 用 `delivery_handoff`／`handoff_sha256` 绑定 `vocab/generated/source-cutover-handoff.json`、用 `delivery_payload`／`payload_sha256` 绑定 `vocab/generated/source-cutover-payload.json`，来源严格校验通过时才启动术语实施。handoff 顶层键恰为 `schema`、`schema_version`、`payload`、`source_contract`、`schemas`、`topics_sha256`、`migration_ledgers`、`markdown_manifest`、`outputs`、`tracked_write_set`，其中 payload 恰含 path／sha256；source payload 顶层键恰为 schema／schema_version／entries。统一调用 `load_source_handoff(repo_root, handoff_path, payload_path, decision_path)`；共享来源校验只导入 `Issue`、`ReferenceUse(kind, file, record, field_path, value)` 和 `validate_references(root, references)`。来源 Issue 显示 code 加 `TERM_SOURCE_CONTRACT_` 前缀，并保留 file、record、field_path。 | 消除来源定义双写，并让术语侧逐字消费来源计划当前双文件交付。 | 任一键、嵌套、路径或哈希分裂都会让术语 schema、错误映射、主题回归或写集无法确定。 | T01–T13 全部阻断；不得在术语侧写适配器或字段别名。 |
| H02 | `vocab/terms.yaml` 的 `schema` 与 `version` 各取什么精确值；兼容范围、升级顺序和拒绝旧版本的条件是什么？ | `schema: urn:kb-design:schema:terms:1`，`version: 1`；只接受该组合。升级固定为新增模式与迁移器、双版本只读验证、原子迁移、拒绝旧版，不做隐式升级。 | 单一组合便于离线验证和回滚。 | 下一版需要显式迁移。 | 不创建术语模式或正式数据。 |
| H03 | 术语概念 ID 与术语 ID 分别采用什么格式、由谁分配、怎样防重复、何时冻结，以及跨文件移动和形式变化时怎样保持稳定？ | 概念 ID 为 `tc-` 加小写 UUIDv4，术语 ID 为 `tm-` 加小写 UUIDv4；提案工具只为获准迁入的新记录分配，人的升级决定批准时冻结。审计行不分配新概念或术语 ID。校验器检查版本、全局唯一、账本历史未复用；路径、文本、语言和状态变化不得改 ID。 | 身份不再从标签派生，审计继承也不制造新身份。 | 人工阅读依赖账本。 | 升级行保持阻断，不分配 ID；其余行继续审计迁移。 |
| H04 | `subject_fields` 的获准值域是什么；每个概念允许多少定义；同语言定义冲突怎样保存和呈现？ | `subject_fields` 只引用 `decision-source-0005` 冻结的 700 个主题 ID，至少一项且逐值有来源引用。定义至少一项、无数值上限；active 概念每语言最多一条，candidate 可保存冲突但不发布。 | 复用稳定主题身份并保留候选分歧。 | 主题词表与适用学科可能耦合。 | 不建立概念记录。 |
| H05 | 获准的 BCP 47 规范化规则是什么；简体、繁体、文字体系和地区变体允许哪些组合；20 个 `und` 身份逐项归入哪种语言或保持不迁入？ | v1 只接受 `en`、`zh-Hans`、`zh-Hant` 的精确写法；20 个 `und` 机械继承为审计行且不迁入。只有人的升级决定要求其中某行进入正式记录时，才须给出允许标签和决定 ID。 | 阻止按字符猜语言，也避免为保持现状重复裁决。 | 地区变体推迟到模式升级。 | 相关升级行阻断；审计账本和其他任务继续。 |
| H06 | 348 个形式身份怎样进入新账本；哪些变化需要新的迁移决定？ | 348 行全部从冻结审查结果确定性继承：`defer` 为 `audit-only`，`keep` 为 `retain-owner`，`remove` 为 `retain-pending-l3`。只有转为术语记录、取得概念或术语 ID、建立多语概念、改变语言、指定优先或允许状态、合并身份或删除时，才在 `decisions.tsv` 增加升级行；获准迁入的完整记录写入 `records.yaml`。`decision-term-0002` 绑定升级决定与 records 哈希，T06 重建覆盖 348 行的 `terms.tsv`。 | 继承已验证结论，同时阻止迁移暗中扩大效力。 | 升级检测漏项会制造未经批准的准入。 | 只阻断对应升级行；未升级行继续进入审计账本。 |
| H07 | 286 个 `defer`、56 个 `keep` 和 6 个 `remove` 怎样迁移？ | 286 个 `defer` 不重新取证，进入审计；56 个 `keep` 保留原所有权，不因动作获得准入；6 个 `remove` 在没有逐项 L3 决定时保留且不删除。只有人明确要求改变其中任一结果时，才创建升级决定。 | 现行动作不冒充术语状态，也不重复已完成研究。 | 清理和正式准入推迟到真实需要出现时。 | 保持冻结结论，不生成迁入、合并或删除差异。 |
| H08 | 既有依据冲突、无依据、概念对应未确定和“同一概念”结论怎样消费？ | 60 个冲突、139 个无依据、214 个未确定和 47 个“同一概念”逐字继承为审计事实，不重新审查。只有某行准备取得正式术语效力或参与多语概念时，才分别补足形式依据、概念对应、采用和优先形式决定；未补足的升级行阻断，其他行不受影响。 | 形式、概念对应、采用和优先形式保持分门，并把人审限定在效力变化。 | 首轮正式记录可能较少。 | 对应升级行保持未迁入；不阻断审计账本或系统实现。 |
| H09 | `term_concept` 在每份词表中的精确结构、目标 ID 字段、语言集合表达、撤销程序和历史引用是什么？ | 结构固定为 `concept`、`languages`、`state`、`decision`、`history`；active 委托按概念加语言整体取得唯一编辑权，撤销时改为 revoked、恢复本地标签并追加历史。 | 单对象表达所有权和撤销。 | 五份词表增加统一结构。 | 只实现夹具，不改生产词表。 |
| H10 | `types:troubleshooting/en`、`types:troubleshooting/zh`、`forms:cheat-sheet/en` 三个候选是否分别建立委托；每项对应哪个获准术语概念 ID 和决定记录？ | 安全提案为三项都不建立。替代答案必须在 decisions.tsv 与独立委托决定中给出目标概念 ID 和语言。 | 当前三项都有未关闭门禁。 | 无生产委托试点。 | 五份词表 946 标签保持原所有权。 |
| H11 | 是否能提供仓库外内容单元和应用映射的标签消费者清单；若不能，三个候选的影响覆盖以什么明确边界获准？ | 记录仓库外消费者未知；未来 active 委托必须先提供清单或由独立决定接受仅仓库覆盖。 | 不伪造影响完整性。 | 委托继续推迟。 | active 委托校验失败。 |
| H12 | 术语表是否继续呈现当前缩写表和标准表；分组、排序、允许术语入口、历史区、缺少中文时的固定版式和只读声明具体是什么？ | 保留冻结的 15 个布局组；主表固定五列。概念按布局组与 ID，语言按 `zh-Hans`、`zh-Hant`、`en`，术语按状态与 ID；缺中文写 `—`，不补译；历史形式独立呈现；第二行固定只读声明。 | 保持读者结构并固定无中文呈现。 | 布局文件成为新维护对象。 | 只生成 JSON 预演。 |
| H13 | `concepts/glossary.md` 从人工编辑切为生成视图的生效日期、决定记录、冻结哈希和回退条件是什么？ | 生效窗口仍提议 `2026-09-15`，过期即重新决定。T11 只提交切换实现、真实阶段测试定义和夹具，真实 candidate／manifest 不存在，只跑 69 项无需真实材料的高风险测试。T12 从干净 T11 HEAD 读取 tracked paths，生成完整 ignored candidate 与无自引用 ignored manifest，跑 71 项非决定绑定高风险测试和全部预验；人复核后才提交 decision-term-0003／0004／0005。T13 才验证决定绑定、apply-only 并跑 72 项计划高风险门禁。active state 指向 vocab/terms.yaml 且 consumers_enabled true；decision-term-0006 补偿后指向 concepts/glossary.md、terms_mode audit_read_only、consumers_enabled false，并保留审计对象。 | base_commit 是已提交实现，决定绑定的是该提交之后生成并预验的完整内容。 | candidate 丢失或漂移时必须重新决定。 | 不改变所有权。 |
| H14 | `build-topics.py` 是否继续作为 `topics.yaml` 的正式写入器；若继续，受委托标签从哪个已发布术语快照读取；若退出，哪个获准组件接管当前 700／24 输出？ | v1 保留来源切换后的 `scripts/build-topics.py`；只在 term-cutover-state active 且 consumers_enabled 时读取 `vocab/generated/terms-v1.json`。 | 避免重写已验证主题链。 | 旧构建器复杂度上升。 | 不接入委托。 |
| H15 | 主题 ID 从英文标签 `slug` 稳定化的规则是什么；在 ID 稳定化前是否明确禁止任何可能改变标签的委托切换？ | 从 decision-source-0005 的 700 个 ID 与来源身份建立 `vocab/build/topic-ids.json`；构建器只从映射取 ID，新项先决定。覆盖完成前禁止标签委托。 | 切断标签与身份耦合。 | 错误来源键会固化错误。 | T04 与委托阻断。 |
| H16 | `design/topics.md` 的中文标签必填要求与当前 240 个 `basis.zh: none` 缺中文标签之间采用哪一边；这 240 项逐项是不译、待补证还是模式例外？ | 正式规则改为有依据时填写中文；无依据时保留来源语言与中文普通解释。240 项保持不译，不设例外。 | 与零自定一致。 | 中文浏览仍不完整。 | 不改 240 项。 |
| H17 | 正文一致性检查覆盖哪些正式文件和文件类型；60 份 Markdown 库存范围与 38 份现行扫描范围采用哪一个；引用、来源转录、路径、代码、值和历史材料怎样记录排除或裁定？ | 不采用数量。扫描每批当前 `git ls-files '*.md'` 的完整路径集；按现行正文、草案、决定、来源、计划、审计分类。围栏代码、行内代码、链接目标和路径为 excluded；来源转录、代码值和历史为 context-only；其余保留精确位置和裁定 ID。 | 范围随受跟踪文件演进且仍可复现。 | 每批需保存清单。 | 保留旧扫描器，不启用诊断。 |
| H18 | 正文诊断的级别、发布阻断条件、人工裁定记录位置和 298 个现有身份的首轮处置是什么；15 个标题截断噪声是否先修识别器再冻结新基线？ | 级别为 info、review、error；先修 15 个截断，再从动态 Markdown 清单生成新基线。人工裁定写 `vocab/term-usage-decisions.yaml`；只有有决定的 error 阻断。 | 先提高证据质量。 | 首轮不会自动拦截所有问题。 | 只写 ignored 报告。 |
| H19 | 术语复核义务、项目决定和迁移审计各自保存在哪个正式文件；文件模式、ID 分配、反向索引输出和只追加历史怎样验证？ | 义务写 `vocab/term-obligations.yaml`；迁移决定、结构记录与账本写 `vocab/migrations/term-v1/decisions.tsv`、`records.yaml`、`terms.tsv`；正文裁定写 `vocab/term-usage-decisions.yaml`；术语索引写 `vocab/generated/term-reference-index.json`。决定 ID 与义务 ID 的模式由相应 schema 固定，历史以前一 Git 快照作前缀比较。 | 与来源计划的顶层 vocab、迁移和索引布局一致。 | 多文件提交复杂。 | 不创建正式维护对象。 |
| H20 | 术语定期复核周期、触发阈值和首次起算日是什么；是否明确禁止继承现行 24／12／6 月、12 个月、1／3／5／10％／20 等阈值？ | v1 不设周期、阈值或起算日，只启用事件触发，并拒绝继承现有数字。 | 真实工作量尚不可得。 | 无事件的陈旧记录不会被发现。 | 维护工具不调度。 |
| H21 | 17 个实体 `candidate`、13 个 `self`、4 个非 `self` 候选和 692 个主题 `unassigned` 是否确认全部留在原对象治理，任何术语迁入都必须另作逐项决定？ | 全部留在原对象；只有实际进入术语记录的身份需要升级决定。未迁入对象只做写集保护，不创建重复复核义务。 | 防止状态换算和重复复核。 | 正式迁入数量较少。 | 迁移器只做写集保护。 |
| H22 | 模式、校验器、生成器、迁移夹具和维护材料的正式目录与精确文件名是什么；哪些是受 Git 跟踪的正式输入、生成输出和只读审计？ | 使用“文件边界”的精确路径。新增 `vocab/term-cutover-state.yaml` 与 schema；只含升级行的 decisions.tsv、records.yaml 和覆盖 348 行的物化账本受跟踪；来源索引作为共享生成输出纳入术语切换；运行证据只写 ignored 目录。 | 物理职责和原子写集可机械验证。 | 文件数量增加。 | 不创建新受跟踪路径。 |
| H23 | 每个迁移批次的决定记录、提交边界、生效顺序、可回退截止点和恢复所有权方式是什么；回退后哪些历史与义务必须继续保留？ | decision-term-0001 批准模式；0002 只绑定升级决定、records 和冻结输入，不要求 348 行重复答复；T11 提交切换实现和测试但不生成真实 candidate／manifest；T12 以 T11 HEAD 为 base_commit 生成并预验 ignored candidate／manifest，决定绑定测试仍不运行；高价值候选审查后由 0003 审批规则、0004 绑定 ignored manifest、0005 预授权回滚，提交只含这三份决定。T13 要求 base→HEAD 恰为三份决定，才运行绑定测试、apply-only 和完整回归。实际回滚以相同顺序生成补偿 candidate／manifest，再新建 0006 绑定并 apply-only，恢复人工术语表、撤销委托、停用消费者并把 terms 标为 audit_read_only。决定、ignored manifest 的绑定记录、terms、ID、义务、history、账本和快照保留。 | 消除实现提交、候选基线和决定顺序循环，同时保持 manifest ignored。 | candidate 在 apply 前必须完整保存；任何额外 base→HEAD 路径或 manifest 漂移都阻断。 | T13 不执行。 |
| H24 | 三份旧草案是否确认继续旁路：划分特征不创建分析数组、分面字段不消费 111 个试标身份、手工概念组不创建正式文件；若任一改变，应先独立设计而不是扩张术语计划吗？ | 三份旧草案继续旁路；写集检查禁止相关正式对象。 | 保持准备计划任务图。 | 旁路工作不能借本批实现。 | 任一越界差异使任务失败。 |

## 文件边界

来源侧后置依赖只读消费：

| 路径 | 职责 |
|---|---|
| `scripts/source_model.py` | 提供 `Issue`、`ReferenceUse`、`validate_references` 与来源通用访问器 |
| `schemas/source-*.schema.json` | 由 source-cutover-handoff 精确列出并提供 `$id`、版本与哈希 |
| `scripts/check_sources.py` | 执行来源严格校验 |
| `scripts/build_source_index.py` | 确定性生成来源反向索引 |
| `vocab/generated/source-reference-index.json` | 共享生成输出；术语切换必须同步更新 |
| `design/decisions/source-schema-cutover.md` | accepted 的 `decision-source-0005`，绑定 handoff 与 payload 双哈希 |
| `vocab/generated/source-cutover-handoff.json` | 来源富交付：契约、schema、topics、账本、Markdown、outputs 与 payload 指针 |
| `vocab/generated/source-cutover-payload.json` | 来源最小应用 payload：schema、版本和 entries |

术语计划获相应决定后创建：

| 路径 | 类型 | 单一职责 |
|---|---|---|
| `schemas/terms-v1.schema.json` | 正式模式 | 三层术语数据与来源 schema 引用 |
| `schemas/term-concept-v1.schema.json` | 正式模式 | 委托对象、撤销和历史 |
| `schemas/term-usage-decisions-v1.schema.json` | 正式模式 | 正文位置裁定 |
| `schemas/term-obligations-v1.schema.json` | 正式模式 | 术语义务与结清 |
| `schemas/term-cutover-state-v1.schema.json` | 正式模式 | active、rolled_back 与唯一编辑权 |
| `scripts/governance/check_term_inputs.py` | 工具 | 双阶段输入锁、动态 Markdown 清单和后置交付校验 |
| `scripts/governance/check_known_link_failures.py` | 工具 | 把恰好两处既存链接失败转成退出码 0 的门禁 |
| `scripts/governance/check_write_set.py` | 工具 | 按任务允许路径检查 Git porcelain |
| `scripts/governance/term_model.py` | 工具 | 加载和校验术语三层记录 |
| `scripts/governance/term_transitions.py` | 工具 | 校验原子状态和历史 |
| `scripts/governance/stabilize_topic_ids.py` | 工具 | 从来源后置身份冻结主题 ID |
| `scripts/governance/migrate_terms.py` | 工具 | 继承冻结审查结果并物化按风险升级的决定 |
| `scripts/governance/build_terms.py` | 工具 | 生成规范快照与术语表 |
| `scripts/governance/check_term_delegations.py` | 工具 | 校验委托和唯一编辑权 |
| `scripts/governance/check_term_usage.py` | 工具 | 动态扫描 Markdown 与精确上下文 |
| `scripts/governance/term_maintenance.py` | 工具 | 义务、决定和术语索引 |
| `scripts/governance/cutover_terms.py` | 工具 | 暂存、双索引、原子切换和补偿回滚 |
| `tests/governance/term_support.py` | 测试辅助 | 定义全部测试文件共用的 I/O、Git 与夹具函数 |
| `tests/governance/test_term_baseline.py` | 测试 | 双阶段输入锁和写集 |
| `tests/governance/test_term_model.py` | 测试 | 模式、来源契约和三层记录 |
| `tests/governance/test_term_transitions.py` | 测试 | 工作流、管理状态和历史 |
| `tests/governance/test_topic_id_stability.py` | 测试 | 来源后置主题身份 |
| `tests/governance/test_term_migration.py` | 测试 | 安全预演与 348 行身份 |
| `tests/governance/test_term_decisions.py` | 测试 | 升级决定物化与账本提交 |
| `tests/governance/test_term_generation.py` | 测试 | 快照、术语表和漂移 |
| `tests/governance/test_term_delegation.py` | 测试 | 委托与所有权 |
| `tests/governance/test_term_usage.py` | 测试 | 动态 Markdown 范围与上下文 |
| `tests/governance/test_term_maintenance.py` | 测试 | 义务和术语索引 |
| `tests/governance/test_term_cutover.py` | 测试 | 双索引切换和补偿回滚 |
| `tests/governance/test_term_activation.py` | 测试 | 草案核销与生效写集 |
| `tests/fixtures/terminology/` | 测试夹具 | 来源后置清单、术语正反例、两套决定和回滚仓库 |
| `vocab/build/topic-ids.json` | 正式输入 | 稳定主题身份映射 |
| `vocab/glossary-layout.yaml` | 正式输入 | 15 个布局组与固定版式 |
| `vocab/migrations/term-v1/decisions.tsv` | 决定输入 | 只保存改变既有结论或效力的升级行；允许零行数据 |
| `vocab/migrations/term-v1/records.yaml` | 决定输入 | 获准迁入概念的完整三层结构与来源引用 |
| `vocab/migrations/term-v1/terms.tsv` | 只读审计 | 从库存与决定确定性物化的迁移账本 |
| `vocab/term-obligations.yaml` | 正式输入 | 术语复核义务 |
| `vocab/term-usage-decisions.yaml` | 正式输入 | 正文人工裁定 |
| `vocab/term-cutover-state.yaml` | 正式输入 | 唯一编辑源、terms 模式与消费者开关 |
| `vocab/terms.yaml` | 正式或审计输入 | active 时唯一编辑源；rolled_back 时 audit_read_only |
| `vocab/generated/terms-v1.json` | 生成输出 | 共享术语快照；状态文件控制消费 |
| `vocab/generated/term-reference-index.json` | 生成输出 | 术语对象、决定和义务索引 |
| `vocab/generated/term-usage-report.tsv` | 生成输出 | 正文精确位置报告 |
| `vocab/generated/term-usage-manifest.json` | 生成输出 | 本次扫描的动态 Markdown 路径与哈希 |
| `design/terminology.md` | 正式规则 | 生效术语规则与当前所有权 |
| `design/decisions/terminology-governance-schema.md` | 决定 | `decision-term-0001` |
| `design/decisions/terminology-migration-rows.md` | 决定 | `decision-term-0002` 与 decisions.tsv 哈希 |
| `design/decisions/terminology-governance-effective.md` | 决定 | `decision-term-0003` 与草案逐节去向 |
| `design/decisions/terminology-schema-cutover.md` | 决定 | `decision-term-0004` |
| `design/decisions/terminology-schema-rollback.md` | 决定 | `decision-term-0005` 预授权 |
| `design/decisions/terminology-schema-rollback-result.md` | 补偿决定 | 实际回滚时创建 `decision-term-0006` |
| `.superpowers/sdd/2026-08-31-terminology-schema-generation/candidate-root/` | ignored 候选 | T12 从已提交 T11 实现生成 T13 的全部 Create／Modify／Delete 结果 |
| `.superpowers/sdd/2026-08-31-terminology-schema-generation/payload-manifest.json` | ignored 候选 | 对 candidate payload 计算路径、动作与前后哈希；entries 不含本文件 |

术语计划顺序修改以下共享文件：`scripts/build-topics.py`、`scripts/check-topics.py`、`scripts/check-terms.py`、`tests/test_check_terms.py`、`design/topics.md`、`design/governance.md`、`design/writing.md`、`design/maintenance.md`、`design/versioning.md`、`design/README.md`、`AGENTS.md`。T13 应用旧草案删除，decision-term-0003 逐节核销；三份旁路草案与来源正式文件保持只读。

## 接口总表

来源接口由 `scripts/source_model.py` 提供，术语实现按下列 import 使用，不在本计划给出替代实现：

```python
from scripts.source_model import Issue, ReferenceUse, validate_references
```

`ReferenceUse` 的字段顺序固定为 `kind`、`file`、`record`、`field_path`、`value`。`validate_references(root, references)` 返回 `Issue` 列表；术语显示 code 为 `TERM_SOURCE_CONTRACT_` 加 `Issue.code`，并原样保留来源文件、记录与字段路径。

所有 I02 调用都使用同一四参数形式：`load_source_handoff(ROOT, ROOT / SOURCE_HANDOFF, ROOT / SOURCE_PAYLOAD, ROOT / SOURCE_DECISION)`。`SOURCE_DECISION`、`SOURCE_HANDOFF`、`SOURCE_PAYLOAD` 只定义一次；任务代码和测试不得再定义 `SOURCE_MANIFEST`、二参数变体或字段别名。

术语侧类型固定如下。

```python
from dataclasses import dataclass
from pathlib import Path
from typing import FrozenSet, List, Literal, Mapping, Optional, Sequence

Workflow = Literal["candidate", "active", "deprecated"]
AdministrativeStatus = Literal[
    "preferredTerm-admn-sts",
    "admittedTerm-admn-sts",
    "deprecatedTerm-admn-sts",
    "supersededTerm-admn-sts",
]
LanguageTag = Literal["en", "zh-Hans", "zh-Hant"]

@dataclass(frozen=True)
class SourceHandoff:
    schema: str
    schema_version: int
    payload: Mapping[str, str]
    source_contract: Mapping[str, object]
    schemas: Sequence[Mapping[str, object]]
    topics_sha256: str
    migration_ledgers: Sequence[Mapping[str, str]]
    markdown_manifest: Sequence[Mapping[str, str]]
    outputs: Sequence[Mapping[str, object]]
    tracked_write_set: Sequence[str]

@dataclass(frozen=True)
class TermIssue:
    code: str
    origin: Literal["term", "source"]
    path: str
    message: str

@dataclass(frozen=True)
class HistoryEvent:
    date: str
    event: str
    decision: str
    reason: str
    from_value: Optional[str]
    to_value: Optional[str]
    linked_terms: Sequence[str]

@dataclass(frozen=True)
class TermRecord:
    id: str
    text: str
    administrative_status: AdministrativeStatus
    basis: Sequence[object]
    replaced_by: Optional[str]
    history: Sequence[HistoryEvent]

@dataclass(frozen=True)
class LanguageRecord:
    language: LanguageTag
    terms: Sequence[TermRecord]

@dataclass(frozen=True)
class DefinitionRecord:
    language: LanguageTag
    text: str
    basis: Sequence[object]

@dataclass(frozen=True)
class SubjectFieldRecord:
    topic_id: str
    basis: Sequence[object]

@dataclass(frozen=True)
class ConceptRecord:
    id: str
    subject_fields: Sequence[SubjectFieldRecord]
    definitions: Sequence[DefinitionRecord]
    languages: Sequence[LanguageRecord]
    basis: Sequence[object]
    source: Optional[object]
    match: Sequence[object]
    workflow: Workflow
    history: Sequence[HistoryEvent]

@dataclass(frozen=True)
class TermsDocument:
    schema: str
    version: int
    concepts: Sequence[ConceptRecord]

@dataclass(frozen=True)
class InheritedDisposition:
    legacy_identity: str
    disposition: Literal["audit-only", "retain-owner", "retain-pending-l3"]
    decision_evidence: Literal["locked-review-inheritance"]

@dataclass(frozen=True)
class MigrationDecision:
    legacy_identity: str
    operation: Literal["migrate", "merge", "change-language", "delete"]
    concept_id: Optional[str]
    language: Optional[LanguageTag]
    term_id: Optional[str]
    administrative_status: Optional[AdministrativeStatus]
    target_identity: Optional[str]
    decision_id: str
    decision_evidence: str

@dataclass(frozen=True)
class UsageHit:
    identity: str
    file: str
    line: int
    column: int
    context: Literal["excluded", "context-only", "prose"]
    raw: str
    normalized: str
    known_state: Literal["preferred", "admitted", "deprecated", "superseded", "unadmitted", "unknown"]
    severity: Literal["info", "review", "error"]
    decision: Optional[str]

@dataclass(frozen=True)
class Target:
    kind: Literal["concept", "term", "delegation", "decision", "obligation", "generated_output"]
    id: str
    field_path: str
    conclusion: Optional[str]
    reviewed: Optional[str]
    decision: Optional[str]

@dataclass(frozen=True)
class TermTrigger:
    kind: Literal["source_obligation", "concept", "term", "language", "delegation", "decision", "homograph", "schema", "generation", "rollback"]
    id: str
    previous_obligation: Optional[str]

@dataclass(frozen=True)
class TermObligation:
    id: str
    targets: Sequence[Target]
    trigger: TermTrigger
    state: Literal["open", "resolved"]
    opened: str
    closed: Optional[str]
    decision: Optional[str]
    history: Sequence[HistoryEvent]

@dataclass(frozen=True)
class TermCutoverState:
    schema: str
    version: int
    state: Literal["active", "rolled_back"]
    active_editor: Literal["vocab/terms.yaml", "concepts/glossary.md"]
    terms_mode: Literal["active_editor", "audit_read_only"]
    consumers_enabled: bool
    decision: str
    history: Sequence[HistoryEvent]

@dataclass(frozen=True)
class PayloadManifest:
    schema: str
    version: int
    source_handoff_sha256: str
    source_payload_sha256: str
    base_commit: str
    entries: Sequence[Mapping[str, object]]
    delete_paths: Sequence[str]
    preserve_paths: Sequence[str]
    restore_paths: Sequence[str]
    candidate_markdown: Sequence[Mapping[str, str]]

@dataclass(frozen=True)
class TermApplyResult:
    written: Sequence[str]
    deleted: Sequence[str]
    preserved: Sequence[str]

@dataclass(frozen=True)
class RollbackResult:
    restored_editor: str
    terms_mode: str
    consumers_enabled: bool
    preserved_paths: Sequence[str]
    regenerated_source_index: str
    compensation_decision: str
```

生产与共享函数签名固定如下。

| 标识 | 签名 | 责任 |
|---|---|---|
| I01 | `validate_references(root: Path, references: Sequence[ReferenceUse]) -> List[Issue]` | 来源侧逐引用校验 |
| I02 | `load_source_handoff(repo_root: Path, handoff_path: Path, payload_path: Path, decision_path: Path) -> SourceHandoff` | 按来源决定四个键验证 handoff 与 payload 双哈希，并返回与 handoff 十个顶层键同形的来源交付 |
| I03 | `verify_frozen_inputs(repo_root: Path, commit: str, plan_input: Path) -> Sequence[TermIssue]` | 从 Git 对象和 ignored 库存验证迁移前输入 |
| I04 | `current_markdown_manifest(repo_root: Path) -> Sequence[Mapping[str, str]]` | 动态列出 Markdown 路径与哈希 |
| I05 | `load_terms(path: Path) -> TermsDocument` | 加载术语数据 |
| I06 | `validate_terms(document: TermsDocument, source_root: Path, handoff: SourceHandoff, topic_ids: FrozenSet[str]) -> Sequence[TermIssue]` | 三层、来源、语言和身份校验 |
| I07 | `validate_transition(previous: TermsDocument, current: TermsDocument, decisions: FrozenSet[str]) -> Sequence[TermIssue]` | 原子状态和历史校验 |
| I08 | `load_topic_ids(path: Path) -> Mapping[str, str]` | 加载稳定主题身份 |
| I09 | `build_topics(output: Path, term_snapshot: Optional[Path], cutover_state: Optional[Path]) -> None` | 生成主题输出并服从消费者开关 |
| I10 | `load_migration_decisions(path: Path) -> Sequence[MigrationDecision]` | 加载零个或多个升级决定 |
| I11 | `render_migration_ledger(inventory: Path, decisions: Sequence[MigrationDecision]) -> bytes` | 先继承 348 行冻结结论，再叠加升级决定并物化 terms.tsv |
| I12 | `validate_migration(ledger: bytes, inventory_hashes: FrozenSet[str], document: TermsDocument, decisions: FrozenSet[str]) -> Sequence[TermIssue]` | 双向对账与准入门禁 |
| I12A | `build_terms_document(ledger: bytes, records_path: Optional[Path]) -> TermsDocument` | 从有正式迁入的账本与 records.yaml 建立候选文档；没有迁入时返回空候选并阻止正式发布视图，不阻止审计账本 |
| I13 | `canonical_snapshot(document: TermsDocument, source_index: Mapping[str, object], state: TermCutoverState) -> bytes` | 生成共享术语快照 |
| I14 | `render_glossary(snapshot: Mapping[str, object], layout: Mapping[str, object], state: TermCutoverState) -> str` | 生成只读术语表 |
| I15 | `validate_delegations(vocabularies: Mapping[str, object], snapshot: Mapping[str, object], state: TermCutoverState, external_consumers_known: bool) -> Sequence[TermIssue]` | 委托与唯一编辑权 |
| I16 | `resolve_delegated_label(concept_id: str, language: LanguageTag, snapshot: Mapping[str, object], state: TermCutoverState) -> str` | 读取获准标签 |
| I17 | `scan_markdown(repo_root: Path, paths: Sequence[str], snapshot: Mapping[str, object]) -> Sequence[UsageHit]` | 动态正文扫描 |
| I18 | `open_term_obligation(trigger_kind: str, trigger_id: str, targets: Sequence[Target], opened: str, decision: Optional[str]) -> TermObligation` | 建立术语义务 |
| I19 | `validate_obligation_transition(previous: TermObligation, current: TermObligation, decisions: FrozenSet[str]) -> Sequence[TermIssue]` | 义务结清和再触发 |
| I20 | `build_term_reference_index(document: TermsDocument, obligations: Mapping[str, object], decisions: FrozenSet[str]) -> Mapping[str, object]` | 生成术语索引 |
| I21 | `tracked_paths_at_commit(repo_root: Path, commit: str) -> Sequence[str]` | 从切换实现提交的 Git tree 读取 tracked 路径 |
| I22 | `build_complete_candidate(repo_root: Path, candidate_root: Path, handoff: SourceHandoff, tracked_paths: Sequence[str], implementation_commit: str) -> None` | 在实现提交后生成全部 Create／Modify／Delete 内容 |
| I23 | `candidate_markdown_manifest(candidate_root: Path, tracked_paths: Sequence[str], entries: Sequence[Mapping[str, object]]) -> Sequence[Mapping[str, str]]` | 不依赖 candidate `.git` 计算最终 Markdown 清单 |
| I24 | `build_payload_manifest(repo_root: Path, candidate_root: Path, handoff: SourceHandoff, implementation_commit: str, manifest_path: Path) -> PayloadManifest` | 从 `repo_root / SOURCE_HANDOFF` 与 handoff.payload.sha256 记录来源双锁，生成不含自身且 base_commit 为实现提交的 manifest |
| I25 | `verify_bound_payload(repo_root: Path, candidate_root: Path, manifest_path: Path, decision_path: Path) -> Sequence[TermIssue]` | 验证 candidate、manifest 与 decision-term-0004 绑定 |
| I26 | `apply_bound_candidate(repo_root: Path, candidate_root: Path, manifest_path: Path, decision_path: Path) -> TermApplyResult` | 只消费已绑定候选并原子应用，不生成内容 |
| I27 | `stage_rollback(repo_root: Path, stage_root: Path, compensation_decision: str, handoff: SourceHandoff) -> RollbackResult` | 暂存补偿回滚 |
| I28 | `verify_rollback(stage_root: Path, result: RollbackResult, handoff: SourceHandoff) -> Sequence[TermIssue]` | 验证人工编辑权和消费者停用 |
| I29 | `verify_draft_disposition(frozen_draft: bytes, decision_path: Path, formal_path: Path) -> Sequence[TermIssue]` | 逐节核销并确认旧草案移出 |

测试辅助函数全部定义在 `tests/governance/term_support.py`，不允许测试自行形成同名变体。

| 标识 | 签名 |
|---|---|
| HLP01 | `load_yaml(path: Path) -> object` |
| HLP02 | `load_json(path: Path) -> object` |
| HLP03 | `write_yaml(path: Path, value: object) -> None` |
| HLP04 | `hash_file(path: Path) -> str` |
| HLP05 | `copy_fixture_repo(name: str) -> Path` |
| HLP06 | `init_git_fixture(root: Path) -> None` |
| HLP07 | `run_cli(root: Path, argv: Sequence[str]) -> subprocess.CompletedProcess` |
| HLP08 | `load_five_vocabularies(root: Path) -> Mapping[str, object]` |

## 测试账本

计划只设计 72 个高风险测试方法；每项都对应语义效力、身份、迁移完整性、确定性、共享接口、切换或回滚风险。零升级和显式升级通过专用夹具验证，不把当前继承结果写死为唯一 GREEN 结果。既有兼容测试和其他计划的测试不计入本账本，也不以全库测试数量作为验收条件。

| 任务 | 数量 | 测试方法 |
|---|---:|---|
| T01 | 6 | `test_frozen_git_blobs_match`、`test_ignored_inventory_hashes_match`、`test_source_handoff_resolves`、`test_source_handoff_hashes_match`、`test_dynamic_markdown_delta_is_explained`、`test_write_set_guard_rejects_extra_path` |
| T02 | 8 | `test_exact_top_level_keys`、`test_rejects_duplicate_ids`、`test_basis_fields_are_nonempty_arrays`、`test_schema_refs_match_source_handoff`、`test_source_issue_code_and_path_are_preserved`、`test_accepts_only_v1_language_tags`、`test_subject_fields_resolve_to_handoff_topics`、`test_active_definition_conflicts_fail` |
| T03 | 7 | `test_requires_one_preferred_term`、`test_preferred_demotion_is_atomic`、`test_replacement_stays_in_language`、`test_replacement_cycle_fails`、`test_restoration_rechecks_admission`、`test_history_is_append_only`、`test_transition_decisions_resolve` |
| T04 | 4 | `test_topic_id_map_matches_handoff`、`test_label_change_cannot_change_topic_id`、`test_topics_hash_matches_post_source_baseline`、`test_unconsumed_inputs_stay_unchanged` |
| T05 | 8 | `test_inherited_preview_reconciles_348`、`test_defer_becomes_audit_only`、`test_keep_retains_owner_without_admission`、`test_remove_is_retained_without_l3`、`test_und_language_is_not_guessed`、`test_locked_review_fields_are_unchanged`、`test_homographic_rows_stay_distinct`、`test_inherited_preview_writes_only_ignored` |
| T06 | 6 | `test_empty_upgrades_materialize_inherited_ledger`、`test_upgrade_decisions_materialize_migrate_rows`、`test_decision_hash_must_match_adr`、`test_every_inventory_identity_has_one_ledger_row`、`test_ledger_is_byte_stable`、`test_invalid_upgrade_remains_blocked` |
| T07 | 6 | `test_generation_is_byte_stable`、`test_only_active_concepts_publish`、`test_missing_chinese_never_falls_back`、`test_manual_output_drift_fails`、`test_all_consumers_share_snapshot_hash`、`test_rolled_back_state_disables_generation` |
| T08 | 5 | `test_delegated_language_has_one_owner`、`test_inherited_rows_keep_production_undelegated`、`test_upgrade_decision_can_enable_fixture_delegation`、`test_external_consumer_boundary_blocks_switch`、`test_rolled_back_state_revokes_consumers` |
| T09 | 5 | `test_scans_dynamic_markdown_manifest`、`test_markdown_addition_requires_allowed_write`、`test_excluded_contexts_keep_precise_locations`、`test_homographs_require_concept_context`、`test_first_usage_baseline_is_report_only` |
| T10 | 6 | `test_source_obligation_bridge_uses_id_only`、`test_term_index_is_bidirectional`、`test_decision_change_opens_new_obligation`、`test_resolved_obligation_never_reopens`、`test_obligation_history_is_append_only`、`test_no_periodic_threshold_is_inherited` |
| T11 | 8 | `test_tracked_paths_come_from_implementation_commit`、`test_candidate_markdown_uses_implementation_tree_without_git`、`test_complete_candidate_contains_every_activation_change`、`test_payload_manifest_excludes_itself`、`test_payload_manifest_is_byte_stable`、`test_source_index_contains_term_references`、`test_candidate_runs_source_strict_validation`、`test_rollback_preserves_terms_ids_and_history` |
| T12 | 2 | `test_candidate_base_commit_is_implementation_commit`、`test_real_candidate_passes_prebinding_validation` |
| T13 | 1 | `test_decision_binding_and_apply_only_uses_bound_candidate` |

## 迁移批次

| 批次 | 前置 | 受跟踪写入 | 完成证据 | 回滚 |
|---|---|---|---|---|
| 旧证据锁 | 冻结提交与 18 项哈希 | T01 工具和测试 | Git 对象与 ignored 库存一致 | revert T01 实现提交；输入不动 |
| 来源后置锁 | `decision-source-0005` 已提交 | 无正式术语数据 | `delivery_handoff`／`handoff_sha256`、`delivery_payload`／`payload_sha256`、handoff 十个顶层键、payload 三个顶层键、来源模型、主题哈希、写集和 Markdown 清单一致 | 停止术语任务；不回退来源计划 |
| 模式批次 | decision-term-0001 | 五份术语 schema、模型和测试 | T02、T03 GREEN；来源契约逐字消费 | revert 代码提交；决定保留 |
| 主题身份 | H14–H16 | topic-ids、构建器与设计 | 来源后置 700／24 与主题哈希不变 | revert T04；decision-source-0005 保留 |
| 继承预演 | 冻结 348 行审查与 H06–H08 | 无正式迁移账本 | 348 行 ignored 预演逐字继承旧结论且可复现 | 删除 ignored 输出 |
| 决定物化 | decision-term-0002、零个或多个升级行与 records.yaml | decisions.tsv、records.yaml、terms.tsv | 无升级与有升级两类夹具均 GREEN；真实账本 348／348 对账 | 新决定只修订升级行并重物化；冻结输入和旧账本 Git 历史保留 |
| 生成委托 | H09–H15 | 布局、生成器、委托校验 | 快照、术语表和标签共享哈希 | revert T07/T08；正式所有权未切换 |
| 诊断维护 | H17–H20 | 扫描器、义务和索引工具 | 动态 Markdown 清单、事件义务 GREEN | revert T09/T10；裁定与决定保留 |
| 切换实现 | T01–T10 GREEN；真实 candidate／manifest 不存在 | `cutover_terms.py`、两份测试和夹具 | T11 的 69 项无需真实材料高风险测试全绿；8 项切换测试只用夹具；提交后工作树干净，真实 candidate／manifest 仍不存在 | revert T11 实现提交；decision-term-0003／0004／0005 尚未创建 |
| 完整候选 | T11 实现提交为干净 HEAD | 无受跟踪写入；ignored candidate 与 ignored manifest | T12 的 71 项非决定绑定高风险测试、candidate 结构与逐项哈希、双索引、来源 strict、动态 Markdown 和草案核销通过 | 删除精确 ignored candidate 与 manifest；决定尚未创建 |
| 决定绑定 | T12 candidate 与 manifest 已冻结并经人复核 | 只写 decision-term-0003／0004／0005 三份决定 | 决定记录 manifest path／SHA-256 和 implementation_commit；manifest 仍 ignored；尚不运行决定绑定测试 | 不删除决定；candidate 漂移则新建候选与替代决定 |
| 原子应用 | 已绑定 candidate；base→HEAD 恰为三份决定 | 只复制／删除 manifest entries | T13 先运行决定绑定与 apply-only 测试，再运行 72 项计划高风险门禁、来源严格和双索引；生成函数调用为零 | decision-term-0006 绑定补偿候选；保留 terms、ID、义务、历史、账本、ignored manifest 绑定记录和快照 |

### 双锁基线

任务标识：T01。任务只建立证据工具与测试辅助；不创建正式术语数据。

**Files:**

- Create: `scripts/governance/check_term_inputs.py`
- Create: `scripts/governance/check_known_link_failures.py`
- Create: `scripts/governance/check_write_set.py`
- Create: `tests/governance/__init__.py`
- Create: `tests/governance/term_support.py`
- Create: `tests/governance/test_term_baseline.py`
- Create: `tests/fixtures/terminology/frozen-inputs.json`
- Read: `design/decisions/source-schema-cutover.md`
- Read: `vocab/generated/source-cutover-handoff.json`
- Read: `vocab/generated/source-cutover-payload.json`
- Read from Git object: `docs/superpowers/plans/2026-08-31-governance-implementation-prep.md`、两份旧治理草案
- Read: `.superpowers/sdd/2026-08-31-governance-implementation-prep/` 的十五项 ignored 库存和报告

**Interfaces:**

- Consumes: H01 source decision 的 `delivery_handoff`／`handoff_sha256`／`delivery_payload`／`payload_sha256`、source-cutover-handoff 十个顶层键、source-cutover-payload 三个顶层键、冻结 Git 对象和术语计划输入哈希。
- Produces: I02–I04、HLP01–HLP08；私有函数 `extract_named_json_blocks(text, name)`、`unexplained_markdown_delta(previous, current, allowed)`；命令 `check_term_inputs.py verify`、`check_known_link_failures.py`、`check_write_set.py`。

- [ ] 写入 T01 的 6 个高风险失败测试。测试必须从 Git blob 读取旧草案，不能 `Path('design/drafts/source-governance.md').read_bytes()`；全部 loader 调用使用同一四参数形式。已知旧链接只保留仓库级命令门禁，不建立术语单元测试。

```python
class TermBaselineTest(unittest.TestCase):
    def test_frozen_git_blobs_match(self):
        checks = verify_frozen_inputs(ROOT, FROZEN_COMMIT, PLAN_INPUT)
        self.assertEqual([], [issue for issue in checks if issue.code.startswith("FROZEN_")])

    def test_source_handoff_resolves(self):
        handoff = load_source_handoff(
            ROOT,
            ROOT / SOURCE_HANDOFF,
            ROOT / SOURCE_PAYLOAD,
            ROOT / SOURCE_DECISION,
        )
        self.assertEqual("urn:kb-design:data:source-cutover-handoff", handoff.schema)
        self.assertEqual(1, handoff.schema_version)
        self.assertEqual({"path", "sha256"}, set(handoff.payload))
        self.assertEqual("scripts/source_model.py", handoff.source_contract["module"])
        self.assertEqual(7, len(handoff.schemas))
        self.assertEqual(set(SOURCE_HANDOFF_FIELDS), set(load_json(ROOT / SOURCE_HANDOFF)))

    def test_source_handoff_hashes_match(self):
        handoff_path = ROOT / SOURCE_HANDOFF
        payload_path = ROOT / SOURCE_PAYLOAD
        decision_path = ROOT / SOURCE_DECISION
        load_source_handoff(ROOT, handoff_path, payload_path, decision_path)
        front = load_yaml_front_matter(decision_path)
        self.assertEqual(SOURCE_HANDOFF.as_posix(), front["delivery_handoff"])
        self.assertEqual(hash_file(handoff_path), front["handoff_sha256"])
        self.assertEqual(SOURCE_PAYLOAD.as_posix(), front["delivery_payload"])
        self.assertEqual(hash_file(payload_path), front["payload_sha256"])

    def test_dynamic_markdown_delta_is_explained(self):
        handoff = load_source_handoff(
            ROOT,
            ROOT / SOURCE_HANDOFF,
            ROOT / SOURCE_PAYLOAD,
            ROOT / SOURCE_DECISION,
        )
        current = current_markdown_manifest(ROOT)
        self.assertEqual([], unexplained_markdown_delta(
            handoff.markdown_manifest, current, T01_ALLOWED,
        ))
```

  其余两个方法逐字使用测试账本中的 `test_ignored_inventory_hashes_match`、`test_write_set_guard_rejects_extra_path`；连同 `test_frozen_git_blobs_match` 合计 6 项。`test_ignored_inventory_hashes_match` 逐项核十五个 ignored 输入，不合并为目录哈希。

- [ ] 运行 RED。

运行：`python3 -m unittest tests.governance.test_term_baseline -v`

预期：退出码 1；缺少 `check_term_inputs` 与 `term_support`，不是因为来源决定或 YAML 语法损坏。

- [ ] 完整实现 `tests/governance/term_support.py`。其他测试只能导入这些函数。

```python
import hashlib
import json
import pathlib
import shutil
import subprocess
import tempfile

import yaml

VOCAB_FILES = ("topics.yaml", "entities.yaml", "types.yaml", "genres.yaml", "forms.yaml")

def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def write_yaml(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False), encoding="utf-8")

def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def copy_fixture_repo(name):
    source = pathlib.Path(__file__).resolve().parents[1] / "fixtures" / "terminology" / name
    temporary = pathlib.Path(tempfile.mkdtemp(prefix="kb-term-fixture-"))
    shutil.copytree(source, temporary, dirs_exist_ok=True)
    return temporary

def init_git_fixture(root):
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)

def run_cli(root, argv):
    return subprocess.run(list(argv), cwd=root, capture_output=True, text=True)

def load_five_vocabularies(root):
    return {name: load_yaml(root / "vocab" / name) for name in VOCAB_FILES}
```

- [ ] 在 `check_term_inputs.py` 定义接口总表中的三个 `SOURCE_*` 路径常量、两个字段元组和 `SourceHandoff`。dataclass 的字段顺序与 `SOURCE_HANDOFF_FIELDS` 十项逐字相同，不添加 decision、hash 或兼容别名；T02、T04 和 T11 只从本模块导入这些对象。

- [ ] 实现 `load_source_handoff()`。四个参数依次是 repo root、实际 handoff 路径、实际 payload 路径和实际 decision 路径。先验证 `decision-source-0005` 的四个来源交付键，再按 handoff 十个顶层键校验 source_model、顶层七份 schemas、`topics_sha256` 与 topics output 700／24、六份账本、`markdown_manifest`、outputs 和 `tracked_write_set`，最后验证 handoff.payload 与决定都绑定显式 payload 字节。payload 只允许 schema、schema_version、entries。缺项返回稳定 `HANDOFF_*` 错误，不补默认值。

```python
import hashlib
import json
from dataclasses import fields
from pathlib import Path

import yaml

from scripts.source_model import ERROR_CODES, ROLE_QUALIFICATIONS

SOURCE_DECISION = Path("design/decisions/source-schema-cutover.md")
SOURCE_HANDOFF = Path("vocab/generated/source-cutover-handoff.json")
SOURCE_PAYLOAD = Path("vocab/generated/source-cutover-payload.json")
SOURCE_DECISION_FIELDS = (
    "delivery_handoff", "handoff_sha256", "delivery_payload", "payload_sha256",
)
SOURCE_HANDOFF_FIELDS = (
    "schema", "schema_version", "payload", "source_contract", "schemas",
    "topics_sha256", "migration_ledgers", "markdown_manifest", "outputs",
    "tracked_write_set",
)

def extract_named_json_blocks(text, name):
    fence = chr(96) * 3
    start = f"{fence}json {name}"
    blocks = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        if lines[index] != start:
            index += 1
            continue
        end = index + 1
        while end < len(lines) and lines[end] != fence:
            end += 1
        if end == len(lines):
            raise ValueError(f"HANDOFF_FENCE_UNCLOSED {name}")
        blocks.append(json.loads("\n".join(lines[index + 1:end])))
        index = end + 1
    return blocks

def load_yaml_front_matter(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("DECISION_FRONT_MATTER_MISSING")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("DECISION_FRONT_MATTER_UNCLOSED") from error
    return yaml.safe_load("\n".join(lines[1:end]))

def load_source_handoff(repo_root, handoff_path, payload_path, decision_path):
    front = load_yaml_front_matter(decision_path)
    if front.get("id") != "decision-source-0005" or front.get("status") != "accepted":
        raise ValueError("HANDOFF_DECISION_NOT_ACCEPTED")
    missing_decision = [key for key in SOURCE_DECISION_FIELDS if key not in front]
    if missing_decision:
        raise ValueError(f"HANDOFF_DECISION_FIELDS {','.join(missing_decision)}")
    if {"delivery_manifest", "payload_manifest_sha256"} & set(front):
        raise ValueError("HANDOFF_DEPRECATED_SOURCE_DECISION_FIELDS")
    if front["delivery_handoff"] != SOURCE_HANDOFF.as_posix() \
            or handoff_path != repo_root / SOURCE_HANDOFF:
        raise ValueError("HANDOFF_PATH")
    if front["delivery_payload"] != SOURCE_PAYLOAD.as_posix() \
            or payload_path != repo_root / SOURCE_PAYLOAD:
        raise ValueError("SOURCE_PAYLOAD_PATH")
    handoff_sha256 = hashlib.sha256(handoff_path.read_bytes()).hexdigest()
    payload_sha256 = hashlib.sha256(payload_path.read_bytes()).hexdigest()
    if front.get("handoff_sha256") != handoff_sha256:
        raise ValueError("HANDOFF_SHA256")
    if front.get("payload_sha256") != payload_sha256:
        raise ValueError("SOURCE_PAYLOAD_SHA256")
    value = json.loads(handoff_path.read_text(encoding="utf-8"))
    if set(value) != set(SOURCE_HANDOFF_FIELDS):
        raise ValueError(f"HANDOFF_FIELDS {sorted(value)}")
    if value["schema"] != "urn:kb-design:data:source-cutover-handoff" \
            or value["schema_version"] != 1:
        raise ValueError("HANDOFF_SCHEMA")
    if value["payload"] != {
        "path": SOURCE_PAYLOAD.as_posix(),
        "sha256": payload_sha256,
    }:
        raise ValueError("HANDOFF_PAYLOAD_BINDING")
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    if set(payload) != {"schema", "schema_version", "entries"}:
        raise ValueError("SOURCE_PAYLOAD_KEYS")
    if payload["schema"] != "urn:kb-design:data:source-cutover-payload" \
            or payload["schema_version"] != 1:
        raise ValueError("SOURCE_PAYLOAD_SCHEMA")
    contract = value["source_contract"]
    if set(contract) != {
        "module", "sha256", "reference_kinds", "role_qualifications", "error_codes",
    }:
        raise ValueError("HANDOFF_SOURCE_CONTRACT_FIELDS")
    if contract["module"] != "scripts/source_model.py" \
            or contract["sha256"] != hash_file(repo_root / contract["module"]):
        raise ValueError("HANDOFF_SOURCE_CONTRACT_HASH")
    if contract["reference_kinds"] != ["basis", "source", "match", "external_group"] \
            or contract["role_qualifications"] != dict(ROLE_QUALIFICATIONS) \
            or contract["error_codes"] != list(ERROR_CODES):
        raise ValueError("HANDOFF_SOURCE_CONTRACT_VALUES")
    validate_schema_rows(repo_root, value["schemas"])
    topics = unique_output(value["outputs"], "topics")
    if (topics["path"] != "vocab/topics.yaml"
            or topics["sha256"] != value["topics_sha256"]
            or topics["sha256"] != hash_file(repo_root / topics["path"])
            or topics["concepts"] != 700 or topics["arrays"] != 24):
        raise ValueError("HANDOFF_TOPICS")
    validate_path_hash_rows(repo_root, value["migration_ledgers"], expected_count=6)
    validate_path_hash_rows(repo_root, value["markdown_manifest"], expected_count=None)
    validate_output_rows(repo_root, value["outputs"])
    entry_paths = {entry["path"] for entry in payload["entries"]}
    if set(value["tracked_write_set"]) != entry_paths:
        raise ValueError("HANDOFF_TRACKED_WRITE_SET")
    if {SOURCE_HANDOFF.as_posix(), SOURCE_PAYLOAD.as_posix()} & entry_paths:
        raise ValueError("SOURCE_PAYLOAD_SELF_ENTRY")
    if tuple(field.name for field in fields(SourceHandoff)) != SOURCE_HANDOFF_FIELDS:
        raise ValueError("HANDOFF_TYPE_FIELDS")
    return SourceHandoff(**value)

def unexplained_markdown_delta(previous, current, allowed):
    before = {item["path"]: item["sha256"] for item in previous}
    after = {item["path"]: item["sha256"] for item in current}
    changed = {path for path in set(before) | set(after) if before.get(path) != after.get(path)}
    return sorted(changed - set(allowed))
```

  `validate_schema_rows()` 要求恰七项、path 唯一、`$id` 唯一、`schema_version` 与 `$id` 尾部版本相同，并逐项比较正式文件 SHA-256；它不读取 `source_contract["schemas"]`。`validate_path_hash_rows()` 逐项要求恰含 path／sha256，Markdown 数量取实际值。`validate_output_rows()` 要求 outputs 恰有 topics 与 source_index 两项并比较路径和 SHA-256。`unique_output()` 对缺失或重复 kind 失败。

- [ ] 实现 `verify_frozen_inputs()`。对三个 tracked 输入分别调用 `git show 9e7b411c23e890d13d70fc16d443b760313126c4:` 加输入锁中的精确路径后计算 SHA-256；对十五项 ignored 输入读取工作树；不要求旧草案路径仍存在。实现 `current_markdown_manifest()` 为 `git ls-files -z -- '*.md'` 加逐文件 SHA-256，按路径排序。`check_term_inputs.py verify` 在 loader 成功后运行 `python3 scripts/check_sources.py --root <repo_root>`，非零即返回来源锁问题。

- [ ] 实现链接门禁。`check_known_link_failures.py` 运行 `scripts/check-links.py`，解析并排序问题行，只有与 frozen-inputs.json 的两行完全相同才退出 0；零条、第三条或文本变化都退出 1。

- [ ] 实现写集门禁。CLI 接受一个 `--base` Git 提交和一个或多个重复的 `--allow` 精确路径；T01 的完整调用见下一项。工具合并 `git diff --name-only` 与 porcelain 中未跟踪路径，规范化后与 allow 集合比较；多出或缺少路径都退出 1。ignored 证据目录永远排除。

- [ ] 运行 GREEN。

运行：`python3 -m unittest tests.governance.test_term_baseline -v`

预期：7 项通过。

- [ ] 本任务只运行 T01 定向 GREEN 与写集检查；完整回归并入 T03 模式闭合门禁。

- [ ] 运行写集门禁。

运行：`python3 scripts/governance/check_write_set.py --base HEAD --allow scripts/governance/check_term_inputs.py --allow scripts/governance/check_known_link_failures.py --allow scripts/governance/check_write_set.py --allow tests/governance/__init__.py --allow tests/governance/term_support.py --allow tests/governance/test_term_baseline.py --allow tests/fixtures/terminology/frozen-inputs.json`

预期：退出码 0，只列本任务 7 个文件。

- [ ] 记录回滚：提交后被拒绝时 `git revert --no-edit HEAD`；该提交不含来源决定、术语决定或正式数据。

- [ ] 提交本任务。

```bash
git add scripts/governance/check_term_inputs.py scripts/governance/check_known_link_failures.py scripts/governance/check_write_set.py tests/governance/__init__.py tests/governance/term_support.py tests/governance/test_term_baseline.py tests/fixtures/terminology/frozen-inputs.json
git commit -m "[L1] 术语治理：冻结双阶段输入"
```

### 模式契约

任务标识：T02。`decision-term-0001` 必须已经单独提交；T02 不创建或删除决定记录。

**Files:**

- Create: `schemas/terms-v1.schema.json`
- Create: `scripts/governance/term_model.py`
- Create: `tests/governance/test_term_model.py`
- Create: `tests/fixtures/terminology/valid/minimal-active.yaml`
- Create: `tests/fixtures/terminology/valid/two-language.yaml`
- Create: `tests/fixtures/terminology/invalid/legacy-reference-values.yaml`
- Require: `design/decisions/terminology-governance-schema.md`

**Interfaces:**

- Consumes: I01、I02、H01–H05；测试和调用者从 handoff topics output 指向的 `vocab/topics.yaml` 直接构造 `FrozenSet[str]`，不前置消费 T04 才产生的 I08。
- Produces: I05、I06；私有帮助函数 `exported_reference_uris(schemas)`、`unique_source_output(handoff, kind)`、`object_schema(required, properties, all_of)`、`local_term_definitions(refs)`、`build_terms_schema(handoff)`、`schema_issues(value, schema, source_schemas)`、`parse_terms(value)`、`collect_reference_uses(document, file)` 在本任务定义。

- [ ] 写入 T02 的 11 个失败测试。测试构造 jsonschema registry 时只使用 handoff 顶层 `schemas` 的 path、`$id`、`schema_version` 和 SHA-256；不得在测试常量复制来源 `$id`，不得从 `source_contract` 读取 schemas。

```python
SOURCE_HANDOFF_PATH = ROOT / SOURCE_HANDOFF
SOURCE_PAYLOAD_PATH = ROOT / SOURCE_PAYLOAD
SOURCE_DECISION_PATH = ROOT / SOURCE_DECISION

class TermModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handoff = load_source_handoff(
            ROOT, SOURCE_HANDOFF_PATH, SOURCE_PAYLOAD_PATH, SOURCE_DECISION_PATH,
        )
        cls.source_schemas = [load_json(ROOT / row["path"]) for row in cls.handoff.schemas]
        cls.exported = exported_reference_uris(cls.handoff.schemas)
        cls.topic_output = unique_source_output(cls.handoff, "topics")

    def test_schema_refs_match_source_handoff(self):
        handoff = load_source_handoff(
            ROOT, SOURCE_HANDOFF_PATH, SOURCE_PAYLOAD_PATH, SOURCE_DECISION_PATH,
        )
        schema = build_terms_schema(handoff)
        exported = exported_reference_uris(handoff.schemas)
        self.assertEqual(exported["basis"], schema["$defs"]["basis"]["items"]["$ref"])
        self.assertEqual(exported["source"], schema["$defs"]["source_reference"]["$ref"])
        self.assertEqual(exported["match"], schema["$defs"]["match_reference"]["$ref"])

    def test_basis_fields_are_nonempty_arrays(self):
        schema = build_terms_schema(self.handoff)
        basis = schema["$defs"]["basis"]
        self.assertEqual("array", basis["type"])
        self.assertEqual(1, basis["minItems"])
        self.assertEqual(self.exported["basis"], basis["items"]["$ref"])
        self.assertEqual("#/$defs/basis", schema["$defs"]["concept"]["properties"]["basis"]["$ref"])
        self.assertEqual("#/$defs/basis", schema["$defs"]["subject_field"]["properties"]["basis"]["$ref"])
        self.assertEqual("#/$defs/basis", schema["$defs"]["definition"]["properties"]["basis"]["$ref"])
        self.assertEqual("#/$defs/basis", schema["$defs"]["term"]["properties"]["basis"]["$ref"])

    def test_source_issue_code_and_path_are_preserved(self):
        issues = validate_terms(self.invalid_reference_document, ROOT, self.handoff, self.topic_ids)
        source_issue = next(issue for issue in issues if issue.origin == "source")
        self.assertTrue(source_issue.code.startswith("TERM_SOURCE_CONTRACT_"))
        self.assertIn(source_issue.code.removeprefix("TERM_SOURCE_CONTRACT_"),
                      self.handoff.source_contract["error_codes"])
        self.assertEqual("concepts[0].definitions[0].basis[0]", source_issue.path)

    def test_subject_fields_resolve_to_handoff_topics(self):
        self.assertEqual((700, 24),
                         (self.topic_output["concepts"], self.topic_output["arrays"]))
        self.assertEqual(self.handoff.topics_sha256, self.topic_output["sha256"])
        issues = validate_terms(self.valid_document, ROOT, self.handoff, self.topic_ids)
        self.assertNotIn("TERM_SUBJECT_FIELD_UNKNOWN", {issue.code for issue in issues})
```

  测试文件的类和方法层级按上例书写，不能把 `def test_*` 留在类外。其余七项逐字使用测试账本中的名称；全文件恰有 11 个 `test_*` 方法。

- [ ] 运行 RED。

运行：`python3 -m unittest tests.governance.test_term_model -v`

预期：退出码 1，缺少 term_model 与 terms schema。

- [ ] 实现 `build_terms_schema()`。根只允许 `schema`、`version`、`concepts`；本地 `$defs` 完整定义 history、subject_field、definition、term、language_record、concept。`basis`、`source_reference`、`match_reference` 只保存 handoff 的三个导出 URI，不展开其字段。term 与 concept ID 使用 H03 UUIDv4 正则；language 使用 H05 三值；workflow 与 administrative_status 使用草案枚举；superseded 条件要求 `replaced_by`，其他状态禁止该字段；所有记录 `additionalProperties: false`。

```python
def build_terms_schema(handoff):
    refs = exported_reference_uris(handoff.schemas)
    if set(refs) != {"basis", "source", "match"}:
        raise ValueError(f"SOURCE_EXPORT_SET {sorted(refs)}")
    defs = local_term_definitions(refs)
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:kb-design:schema:terms:1",
        "type": "object",
        "required": ["schema", "version", "concepts"],
        "additionalProperties": False,
        "properties": {
            "schema": {"const": "urn:kb-design:schema:terms:1"},
            "version": {"const": 1},
            "concepts": {"type": "array", "items": {"$ref": "#/$defs/concept"}},
        },
        "$defs": defs,
    }
```

`local_term_definitions(refs)` 必须返回测试断言的完整字段集合；测试逐项比较 required、properties、enum、pattern、minItems 与 `additionalProperties`，因此实现不能留下未定义子模式。

```python
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ADMINISTRATIVE_STATUSES = (
    "preferredTerm-admn-sts",
    "admittedTerm-admn-sts",
    "deprecatedTerm-admn-sts",
    "supersededTerm-admn-sts",
)

def exported_reference_uris(schemas):
    by_path = {contract["path"]: contract for contract in schemas}
    entity = by_path["schemas/source-entities.schema.json"]
    migration = by_path["schemas/source-migration.schema.json"]
    return {
        "basis": entity["$id"] + "#/$defs/basisItem",
        "source": migration["$id"] + "#/$defs/source",
        "match": migration["$id"] + "#/$defs/match",
    }

def unique_source_output(handoff, kind):
    matches = [row for row in handoff.outputs if row["kind"] == kind]
    if len(matches) != 1:
        raise ValueError(f"SOURCE_OUTPUT_COUNT {kind} {len(matches)}")
    return matches[0]

def object_schema(required, properties, all_of=None):
    value = {
        "type": "object",
        "required": list(required),
        "additionalProperties": False,
        "properties": properties,
    }
    if all_of is not None:
        value["allOf"] = all_of
    return value

def local_term_definitions(refs):
    concept_pattern = r"^tc-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    term_pattern = concept_pattern.replace("^tc-", "^tm-")
    language = {"enum": ["en", "zh-Hans", "zh-Hant"]}
    basis = {
        "type": "array",
        "minItems": 1,
        "items": {"$ref": refs["basis"]},
    }
    history = object_schema(
        ("date", "event", "decision", "reason", "from_value", "to_value", "linked_terms"),
        {
            "date": {"type": "string", "format": "date"},
            "event": {"type": "string", "minLength": 1},
            "decision": {"type": "string", "minLength": 1},
            "reason": {"type": "string", "minLength": 1},
            "from_value": {"type": ["string", "null"]},
            "to_value": {"type": ["string", "null"]},
            "linked_terms": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        },
    )
    term = object_schema(
        ("id", "text", "administrative_status", "basis", "history"),
        {
            "id": {"type": "string", "pattern": term_pattern},
            "text": {"type": "string", "minLength": 1},
            "administrative_status": {"enum": list(ADMINISTRATIVE_STATUSES)},
            "basis": {"$ref": "#/$defs/basis"},
            "replaced_by": {"type": "string", "pattern": term_pattern},
            "history": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/history"}},
        },
        [{
            "if": {"properties": {"administrative_status": {"const": "supersededTerm-admn-sts"}}},
            "then": {"required": ["replaced_by"]},
            "else": {"not": {"required": ["replaced_by"]}},
        }],
    )
    language_record = object_schema(
        ("language", "terms"),
        {
            "language": {"$ref": "#/$defs/language"},
            "terms": {"type": "array", "minItems": 1, "uniqueItems": True, "items": {"$ref": "#/$defs/term"}},
        },
    )
    subject_field = object_schema(("topic_id", "basis"), {"topic_id": {"type": "string"}, "basis": {"$ref": "#/$defs/basis"}})
    definition = object_schema(
        ("language", "text", "basis"),
        {"language": {"$ref": "#/$defs/language"}, "text": {"type": "string", "minLength": 1}, "basis": {"$ref": "#/$defs/basis"}},
    )
    concept = object_schema(
        ("id", "subject_fields", "definitions", "languages", "basis", "workflow", "history"),
        {
            "id": {"type": "string", "pattern": concept_pattern},
            "subject_fields": {"type": "array", "minItems": 1, "uniqueItems": True, "items": {"$ref": "#/$defs/subject_field"}},
            "definitions": {"type": "array", "minItems": 1, "uniqueItems": True, "items": {"$ref": "#/$defs/definition"}},
            "languages": {"type": "array", "minItems": 1, "uniqueItems": True, "items": {"$ref": "#/$defs/language_record"}},
            "basis": {"$ref": "#/$defs/basis"},
            "source": {"$ref": refs["source"]},
            "match": {"type": "array", "uniqueItems": True, "items": {"$ref": refs["match"]}},
            "workflow": {"enum": ["candidate", "active", "deprecated"]},
            "history": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/history"}},
        },
    )
    return {
        "language": language,
        "basis": basis,
        "history": history,
        "term": term,
        "language_record": language_record,
        "subject_field": subject_field,
        "definition": definition,
        "concept": concept,
    }

def schema_issues(value, schema, source_schemas):
    resources = [(item["$id"], Resource.from_contents(item)) for item in source_schemas]
    registry = Registry().with_resources(resources)
    validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
    return sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path))
```

`parse_terms(value)` 在 schema 零错误后按 HistoryEvent、TermRecord、LanguageRecord、DefinitionRecord、SubjectFieldRecord、ConceptRecord、TermsDocument 的字段顺序构造不可变对象；每层只读取 schema 已允许的精确键。concept、subject_field、definition、term 的 basis 都必须是非空 list，并逐项原样转为实现 `Sequence[object]` 的 tuple；单个映射在解析阶段也拒绝。日期保留 ISO 字符串，空的可选 source／replaced_by 转为 None，其余列表转 tuple。

- [ ] 实现 `collect_reference_uses()`。按概念身份、subject_fields、definitions、terms、可选 source 和每项 match 生成 `ReferenceUse`；`kind` 直接取 handoff 导出的三个 key，file、record、field_path 精确定位，value 原样传递。

```python
def collect_reference_uses(document, file):
    uses = []
    for concept_index, concept in enumerate(document.concepts):
        record = concept.id
        for basis_index, basis in enumerate(concept.basis):
            uses.append(ReferenceUse("basis", file, record, f"concepts[{concept_index}].basis[{basis_index}]", basis))
        for index, field in enumerate(concept.subject_fields):
            for basis_index, basis in enumerate(field.basis):
                path = f"concepts[{concept_index}].subject_fields[{index}].basis[{basis_index}]"
                uses.append(ReferenceUse("basis", file, record, path, basis))
        for index, definition in enumerate(concept.definitions):
            for basis_index, basis in enumerate(definition.basis):
                path = f"concepts[{concept_index}].definitions[{index}].basis[{basis_index}]"
                uses.append(ReferenceUse("basis", file, record, path, basis))
        for language_index, language in enumerate(concept.languages):
            for term_index, term in enumerate(language.terms):
                for basis_index, basis in enumerate(term.basis):
                    path = f"concepts[{concept_index}].languages[{language_index}].terms[{term_index}].basis[{basis_index}]"
                    uses.append(ReferenceUse("basis", file, record, path, basis))
        if concept.source is not None:
            uses.append(ReferenceUse("source", file, record, f"concepts[{concept_index}].source", concept.source))
        for index, match in enumerate(concept.match):
            uses.append(ReferenceUse("match", file, record, f"concepts[{concept_index}].match[{index}]", match))
    return uses
```

- [ ] 实现 `validate_terms()`。先用 registry 校验完整 schema，再检查全局概念／术语 ID、语言唯一、同语言 text 唯一、active 每语言一条定义、subject_fields 属于来源后置主题 ID；主题基线从 `unique_source_output(handoff, "topics")` 的 700／24 与 handoff.topics_sha256 取得，不读取 `handoff.topics`。随后调用 `validate_references`。来源 `Issue` 映射时 code 写 `TERM_SOURCE_CONTRACT_` 加原 code、origin 写 source、path 写 `Issue.field_path`，file 与 record 加入 message，不改来源结论。

- [ ] 运行 GREEN。

运行：`python3 -m unittest tests.governance.test_term_model -v`

预期：8 项高风险模式测试通过。

- [ ] 本任务只运行 T02 定向 GREEN 与写集检查；完整回归并入 T03 模式闭合门禁。

- [ ] 运行写集门禁。

运行：`python3 scripts/governance/check_write_set.py --base HEAD --allow schemas/terms-v1.schema.json --allow scripts/governance/term_model.py --allow tests/governance/test_term_model.py --allow tests/fixtures/terminology/valid/minimal-active.yaml --allow tests/fixtures/terminology/valid/two-language.yaml --allow tests/fixtures/terminology/invalid/legacy-reference-values.yaml`

预期：退出码 0，只列本任务 6 个创建文件；`design/decisions/terminology-governance-schema.md` 已在基线提交且不出现在差异中。

- [ ] 记录回滚：`git revert --no-edit HEAD` 只移除模式、模型、夹具和测试；`decision-term-0001` 保留。回滚后重跑来源严格校验。

- [ ] 提交本任务。

```bash
git add schemas/terms-v1.schema.json scripts/governance/term_model.py tests/governance/test_term_model.py tests/fixtures/terminology/valid/minimal-active.yaml tests/fixtures/terminology/valid/two-language.yaml tests/fixtures/terminology/invalid/legacy-reference-values.yaml
git commit -m "[L2] 术语治理：建立来源消费模式"
```

### 状态转换

任务标识：T03。任务实现全部状态路径，不形成语义决定。

**Files:**

- Create: `scripts/governance/term_transitions.py`
- Create: `tests/governance/test_term_transitions.py`
- Create: `tests/fixtures/terminology/invalid/status-and-replacement.yaml`
- Modify: `scripts/governance/term_model.py`

**Interfaces:**

- Consumes: I05、I06、H06–H08。
- Produces: I07；私有函数 `index_terms(document)`、`history_is_prefix(before, after)`、`replacement_cycles(document)` 在本任务定义。

- [ ] 写入 T03 的 7 个高风险失败测试，覆盖唯一优先、原子升降、同语言替代、环、恢复准入、历史前缀和决定解析；同状态 no-op 由状态转换实现直接拒绝，不单设测试。

```python
def test_preferred_demotion_is_atomic(self):
    issues = validate_transition(self.before, self.demoted_without_replacement, self.decisions)
    self.assertEqual({"TERM_PREFERRED_COUNT", "TERM_ATOMIC_LANGUAGE_CHANGE"}, {item.code for item in issues})
```

- [ ] 运行 RED：`python3 -m unittest tests.governance.test_term_transitions -v`。预期缺少 term_transitions。

- [ ] 实现完整转换集合。

```python
CONCEPT_TRANSITIONS = {
    (None, "candidate"),
    ("candidate", "active"),
    ("active", "deprecated"),
    ("deprecated", "active"),
}

TERM_TRANSITIONS = {
    (None, "preferredTerm-admn-sts"),
    (None, "admittedTerm-admn-sts"),
    (None, "deprecatedTerm-admn-sts"),
    (None, "supersededTerm-admn-sts"),
    ("preferredTerm-admn-sts", "admittedTerm-admn-sts"),
    ("preferredTerm-admn-sts", "deprecatedTerm-admn-sts"),
    ("preferredTerm-admn-sts", "supersededTerm-admn-sts"),
    ("admittedTerm-admn-sts", "preferredTerm-admn-sts"),
    ("admittedTerm-admn-sts", "deprecatedTerm-admn-sts"),
    ("admittedTerm-admn-sts", "supersededTerm-admn-sts"),
    ("deprecatedTerm-admn-sts", "preferredTerm-admn-sts"),
    ("deprecatedTerm-admn-sts", "admittedTerm-admn-sts"),
    ("deprecatedTerm-admn-sts", "supersededTerm-admn-sts"),
    ("supersededTerm-admn-sts", "preferredTerm-admn-sts"),
    ("supersededTerm-admn-sts", "admittedTerm-admn-sts"),
    ("supersededTerm-admn-sts", "deprecatedTerm-admn-sts"),
}
```

未登记直入废弃／被替代只允许迁移决定携带旧证据；恢复优先／允许必须有新决定。每个概念语言前后恰有一个优先；preferred 离开和进入必须在同一快照处置另一术语。

- [ ] 实现替代图：只允许同概念同语言目标，目标状态为 preferred 或 admitted；深度优先遍历检测环。非 superseded 禁止 replaced_by。

- [ ] 实现历史前缀：`after[:len(before)] == before`；新增转换事件必须包含 date、decision、reason、from_value、to_value、全部 linked_terms；decision 必须在传入集合。

```python
def index_terms(document):
    result = {}
    for concept in document.concepts:
        for language in concept.languages:
            for term in language.terms:
                result[term.id] = (concept.id, language.language, term)
    return result

def history_is_prefix(before, after):
    return tuple(after[:len(before)]) == tuple(before)

def replacement_cycles(document):
    terms = index_terms(document)
    edges = {term_id: term.replaced_by for term_id, (_, _, term) in terms.items() if term.replaced_by is not None}
    cycles = []
    visiting = set()
    visited = set()
    def visit(term_id, path):
        if term_id in visiting:
            start = path.index(term_id)
            cycles.append(tuple(path[start:] + [term_id]))
            return
        if term_id in visited:
            return
        visiting.add(term_id)
        target = edges.get(term_id)
        if target is not None:
            visit(target, path + [target])
        visiting.remove(term_id)
        visited.add(term_id)
    for term_id in sorted(edges):
        visit(term_id, [term_id])
    return cycles
```

- [ ] 运行 GREEN：`python3 -m unittest tests.governance.test_term_model tests.governance.test_term_transitions -v`。预期 15 项高风险测试通过。

- [ ] 运行 T03 模式闭合阶段的完整回归。

运行：`python3 -m unittest discover -s tests -p 'test_*.py' -v`

预期：全部测试通过。

运行：`python3 scripts/check-topics.py`

预期：0 问题。

运行：`python3 scripts/check_sources.py --root .`

预期：来源严格校验 0 问题。

运行：`python3 scripts/governance/check_known_link_failures.py`

预期：`KNOWN_LINK_FAILURES_OK count=2`。

运行：`git diff --check`

预期：无输出。

- [ ] 运行写集门禁。

运行：`python3 scripts/governance/check_write_set.py --base HEAD --allow scripts/governance/term_transitions.py --allow tests/governance/test_term_transitions.py --allow tests/fixtures/terminology/invalid/status-and-replacement.yaml --allow scripts/governance/term_model.py`

预期：退出码 0，只列本任务 4 个路径。

- [ ] 记录回滚：revert T03 提交；T02 模式与 decision-term-0001 保留；重跑 T02 测试和来源严格校验。

- [ ] 提交本任务。

```bash
git add scripts/governance/term_transitions.py scripts/governance/term_model.py tests/governance/test_term_transitions.py tests/fixtures/terminology/invalid/status-and-replacement.yaml
git commit -m "[L2] 术语治理：约束原子状态转换"
```

### 主题身份

任务标识：T04。只在来源后置基线上冻结身份；不得与来源计划并行。

**Files:**

- Create: `scripts/governance/stabilize_topic_ids.py`
- Create: `tests/governance/test_topic_id_stability.py`
- Create: `tests/fixtures/terminology/topic-id/`
- Create: `vocab/build/topic-ids.json`
- Modify: `scripts/build-topics.py`
- Modify: `scripts/check-topics.py`
- Modify: `design/topics.md`

**Interfaces:**

- Consumes: I02、H14–H16、source-cutover-handoff 顶层 `topics_sha256` 与 `outputs` 中唯一 topics 项；现行主题构建输入是被改造对象，不把本任务才产生的 I08／I09 当作前置。
- Produces: I08、I09；私有函数 `topic_identity(record)`、`build_topic_id_map(topics, handoff)` 在本任务定义；复用 T02 的 `unique_source_output()`，不定义第二个 topics 解析器。

- [ ] 写入 T04 的 4 个高风险失败测试。测试从 handoff 读取基线哈希和稳定 ID，不嵌入来源迁移前文件哈希；700／24 计数已由 handoff 哈希和 ID 闭合覆盖，不单设重复计数测试。

```python
def test_topics_hash_matches_post_source_baseline(self):
    handoff = load_source_handoff(
        ROOT,
        ROOT / SOURCE_HANDOFF,
        ROOT / SOURCE_PAYLOAD,
        ROOT / SOURCE_DECISION,
    )
    output = unique_source_output(handoff, "topics")
    self.assertEqual("vocab/topics.yaml", output["path"])
    self.assertEqual(handoff.topics_sha256, output["sha256"])
    self.assertEqual(handoff.topics_sha256, hash_file(ROOT / output["path"]))

def test_label_change_cannot_change_topic_id(self):
    root = copy_fixture_repo("topic-id")
    before = build_topics_to_memory(root)
    replace_fixture_label(root, "Software Engineering", "Software Engineering Practice")
    after = build_topics_to_memory(root)
    self.assertEqual(before, after)
```

`build_topics_to_memory()` 与 `replace_fixture_label()` 在测试模块按以下代码定义；topic-id 夹具包含最小 `scripts/build-topics.py`、`vocab/build/labels.json`、`topic-ids.json` 和空 state。

```python
def build_topics_to_memory(root):
    output = root / "build-result.yaml"
    result = run_cli(root, ["python3", "scripts/build-topics.py", "--output", str(output)])
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    value = load_yaml(output)
    return tuple(record["id"] for record in value["concepts"])

def replace_fixture_label(root, old, new):
    path = root / "vocab/build/labels.json"
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise AssertionError(f"fixture label count {text.count(old)}")
    path.write_text(text.replace(old, new), encoding="utf-8")
```

- [ ] 运行 RED：`python3 -m unittest tests.governance.test_topic_id_stability -v`。预期缺少稳定映射和可指定输出的 I09。

- [ ] 实现 `topic_identity()`。来源派生概念使用 source.registry、冒号、source.item；同一外部条目出现多个本地概念时再拼接 `@` 与冻结的当前 ID。没有 source 的本地概念使用 `local:` 加当前 ID。该算法只计算映射键，不重新分配现有 ID。

```python
def topic_identity(record):
    source = record.get("source")
    if isinstance(source, dict) and source.get("registry") and source.get("item"):
        return f"{source['registry']}:{source['item']}"
    return f"local:{record['id']}"

def build_topic_id_map(topics, handoff):
    output = unique_source_output(handoff, "topics")
    if output["path"] != "vocab/topics.yaml" \
            or output["sha256"] != handoff.topics_sha256:
        raise ValueError("SOURCE_TOPIC_HASH")
    if output["concepts"] != 700 or output["arrays"] != 24:
        raise ValueError("SOURCE_TOPIC_COUNTS")
    records = topics["concepts"]
    if len(records) != output["concepts"] or len(topics["arrays"]) != output["arrays"]:
        raise ValueError("TOPIC_ID_SET_CHANGED")
    grouped = {}
    for record in records:
        grouped.setdefault(topic_identity(record), []).append(record)
    entries = []
    for identity, values in sorted(grouped.items()):
        for record in sorted(values, key=lambda item: item["id"]):
            key = identity if len(values) == 1 else f"{identity}@{record['id']}"
            entries.append({"identity": key, "id": record["id"]})
    return entries
```

- [ ] 写入 `topic-ids.json`，根固定为 schema、version、source_cutover_handoff_sha256、entries；handoff 哈希直接取 `hash_file(ROOT / SOURCE_HANDOFF)`，并已由 I02 验证等于 `decision-source-0005.handoff_sha256`。entries 恰 700 且 ID 不重复；不得读取不存在的 `handoff.handoff_sha256` 字段。

- [ ] 重构 `build-topics.py` 为 I09。每个 `add()` 调用显式提供 identity；只从 topic-ids 映射取 ID，缺键退出 1，不回退 slug。`term_snapshot` 仅在 cutover_state 为 active 且 consumers_enabled 时读取；rolled_back 时忽略快照并使用本地标签。

- [ ] 整节重写 `design/topics.md` 的“概念记录的字段”“建设流程”“校验规则”，落实稳定 ID、来源后置接口和 240 项不译；先列旧节每条规则去向并在审查证据中核销。

- [ ] 运行 GREEN：`python3 -m unittest tests.governance.test_topic_id_stability -v`，预期 5 项通过。随后用 I09 连续生成两份 ignored `topics.yaml`，两份与当前文件逐字节相同，哈希等于 `handoff.topics_sha256`，且等于唯一 topics output 的 sha256。

- [ ] 本任务只运行定向 GREEN 与写集检查；完整回归并入下一阶段门禁。

- [ ] 运行写集门禁。

运行：`python3 scripts/governance/check_write_set.py --base HEAD --allow scripts/governance/stabilize_topic_ids.py --allow tests/governance/test_topic_id_stability.py --allow tests/fixtures/terminology/topic-id --allow vocab/build/topic-ids.json --allow scripts/build-topics.py --allow scripts/check-topics.py --allow design/topics.md`

预期：退出码 0，只列本任务 7 个路径；`vocab/topics.yaml` 零差异。

- [ ] 记录回滚：revert T04 实现提交；恢复来源后置构建器和 design/topics.md，decision-source-0005 与术语决定保留；重跑来源索引与严格校验。

- [ ] 提交本任务。

```bash
git add scripts/governance/stabilize_topic_ids.py tests/governance/test_topic_id_stability.py tests/fixtures/terminology/topic-id vocab/build/topic-ids.json scripts/build-topics.py scripts/check-topics.py design/topics.md
git commit -m "[L2] 主题词表：冻结来源后置身份"
```

### 继承预演

任务标识：T05。只生成 ignored 继承预演；不创建受跟踪 decisions.tsv、records.yaml 或 terms.tsv。预演消费冻结审查结论，不重新研究 348 行。

**Files:**

- Create: `scripts/governance/migrate_terms.py`
- Create: `tests/governance/test_term_migration.py`
- Create: `tests/fixtures/terminology/decisions/inherited.tsv`
- Read: `term-glossary.tsv`、`frozen-inputs.json`
- Write ignored: `.superpowers/sdd/2026-08-31-terminology-schema-generation/inherited-preview/`

**Interfaces:**

- Consumes: I05–I07、H05–H08、H21。
- Produces: I10–I12；私有函数 `legacy_identity(row)`、`inherited_decision(row)`、`parse_inventory(path)` 在本任务定义。

- [ ] 写入 T05 的 8 个失败测试。测试证明冻结字段逐字继承，并证明升级决定仍可在 T06 覆盖；不得重新评价依据充分性或概念对应。

```python
def test_inherited_preview_reconciles_348(self):
    ledger = render_migration_ledger(INVENTORY, [])
    rows = parse_ledger(ledger)
    self.assertEqual(348, len(rows))
    self.assertEqual(348, len({row["legacy_identity"] for row in rows}))

def test_inherited_preview_writes_only_ignored(self):
    root = copy_fixture_repo("migration-inherited")
    result = run_cli(root, ["python3", "scripts/governance/migrate_terms.py", "preview", "--output", str(root / ".superpowers/preview")])
    self.assertEqual(2, result.returncode)
    self.assertEqual([], tracked_changes(root))
```

`parse_ledger()` 和 `tracked_changes()` 在测试模块完整定义。

```python
def parse_ledger(value):
    return list(csv.DictReader(io.StringIO(value.decode("utf-8")), delimiter="\t"))

def tracked_changes(root):
    result = run_cli(root, ["git", "status", "--porcelain"])
    return sorted(line[3:] for line in result.stdout.splitlines() if ".superpowers/" not in line)
```

- [ ] 运行 RED：`python3 -m unittest tests.governance.test_term_migration -v`。预期缺少 migrate_terms。

- [ ] 实现库存解析。legacy_identity 是 `sha256(file + NUL + original_line + NUL + section + NUL + language + NUL + text)`；file、line、section、language、text 和 current_action 按 plan-input 中精确列与片段读取。缺失、重复或未知动作退出 1。

```python
import csv
import hashlib
import io
from typing import NamedTuple

class InventoryRow(NamedTuple):
    file: str
    original_line: int
    section: str
    language: str
    text: str
    current_action: str
    legacy_identity: str

def legacy_identity(row):
    parts = (row.file, str(row.original_line), row.section, row.language, row.text)
    return hashlib.sha256("\0".join(parts).encode("utf-8")).hexdigest()

def parse_inventory(path):
    rows = []
    with path.open(encoding="utf-8", newline="") as stream:
        for raw in csv.DictReader(stream, delimiter="\t"):
            location = parse_location(raw["位置"])
            action = parse_exact_action(raw["拟议去向"])
            row = InventoryRow(
                file=raw["文件"],
                original_line=location.line,
                section=location.section,
                language=raw["语言"],
                text=raw["当前形式或值"],
                current_action=action,
                legacy_identity="",
            )
            rows.append(row._replace(legacy_identity=legacy_identity(row)))
    if len(rows) != 348 or len({row.legacy_identity for row in rows}) != 348:
        raise ValueError("TERM_INVENTORY_IDENTITY_COUNT")
    return rows
```

`parse_location()` 只接受“第 N 行；小节=文本；”片段且恰一次；`parse_exact_action()` 只接受 `当前动作=defer`、`keep`、`remove` 中恰一个。两者在 migrate_terms.py 定义并有负例测试。

```python
def inherited_decision(row):
    disposition = {
        "defer": "audit-only",
        "keep": "retain-owner",
        "remove": "retain-pending-l3",
    }[row.current_action]
    return InheritedDisposition(
        legacy_identity=row.legacy_identity,
        disposition=disposition,
        decision_evidence="locked-review-inheritance",
    )
```

- [ ] 实现 inherited.tsv 精确表头：`legacy_identity disposition decision_evidence`，内容由冻结库存确定性生成，只作夹具和审计预演。T06 的 `load_migration_decisions()` 另读取稀疏升级表，拒绝重复身份、未知 operation、空 decision_id 和无效字段组合。

- [ ] 实现 `render_migration_ledger()`。按冻结库存顺序 inner join 348 个决定，输出旧 file、line、section、language、text、action，加决定 8 字段和 `blocks_cutover`。audit-only 本身不阻断；defer、keep、remove 的语义条件由 `validate_migration()` 判断。输出 UTF-8、制表符、LF、末尾换行。

```python
def render_migration_ledger(inventory, decisions):
    rows = parse_inventory(inventory)
    by_identity = {item.legacy_identity: item for item in decisions}
    inventory_ids = {row.legacy_identity for row in rows}
    if len(by_identity) != len(decisions) or not set(by_identity) <= inventory_ids:
        raise ValueError("TERM_DECISION_IDENTITY_SET")
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=LEDGER_FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        inherited = inherited_decision(row)
        writer.writerow(ledger_row(row, inherited, by_identity.get(row.legacy_identity)))
    return output.getvalue().encode("utf-8")
```

`ledger_row()` 在同文件定义，先逐字段复制 InventoryRow 与 InheritedDisposition，再叠加可选 MigrationDecision；None 一律写单个连字符，blocks_cutover 只取 `decision_blocks_cutover(row, upgrade)` 的布尔结果。无升级行时永远不因冻结的 `defer`、`keep`、`remove` 阻断账本；有升级行时按 H05–H08 校验效力变化，不读取全局推荐计数。

- [ ] 实现 `validate_migration()`：继承行必须逐字保留冻结的身份、依据结论、依据位置、概念对应、动作和处理阶段；`audit-only`、`retain-owner`、`retain-pending-l3` 不携带新 ID、语言或管理状态，也不阻断账本形成。只有 T06 提供的升级行才检查正式迁入、合并、语言变更或删除条件。错误只由身份漂移或升级内容产生，不重新评价冻结语义。

- [ ] 运行 GREEN：`python3 -m unittest tests.governance.test_term_migration -v`，预期 8 项通过。运行 preview，预期退出码 0，输出 348 行继承账本，只写 ignored 目录；另输出升级候选清单，但候选清单不产生决定或阻断系统实现。

- [ ] 本任务只运行定向 GREEN 与写集检查；完整回归并入下一阶段门禁。

- [ ] 运行写集门禁。

运行：`python3 scripts/governance/check_write_set.py --base HEAD --allow scripts/governance/migrate_terms.py --allow tests/governance/test_term_migration.py --allow tests/fixtures/terminology/decisions/inherited.tsv`

预期：退出码 0，只列本任务 3 个路径；`vocab/migrations/term-v1/` 没有受跟踪差异。

- [ ] 记录回滚：revert T05 代码与夹具提交；ignored 预演可删除；冻结审查材料和人的决定均未改变。

- [ ] 提交本任务。

```bash
git add scripts/governance/migrate_terms.py tests/governance/test_term_migration.py tests/fixtures/terminology/decisions/inherited.tsv
git commit -m "[L2] 术语治理：建立审查继承预演"
```

### 决定物化

任务标识：T06。任务先把冻结审查结论确定性物化为 348 行受跟踪账本，再只叠加人的升级决定。它不要求人重复回答保持现状的行。

**Files:**

- Create: `vocab/migrations/term-v1/decisions.tsv`
- Create conditionally for approved migrations: `vocab/migrations/term-v1/records.yaml`
- Create: `design/decisions/terminology-migration-rows.md`
- Create or Modify: `vocab/migrations/term-v1/terms.tsv`
- Create: `tests/governance/test_term_decisions.py`
- Create: `tests/fixtures/terminology/decisions/upgrade.tsv`
- Create: `tests/fixtures/terminology/decisions/invalid.tsv`

**Interfaces:**

- Consumes: I10–I12、decision-term-0002、H05–H10、H21。
- Produces: I12A、只含升级行的 decisions.tsv 与覆盖全部 348 个冻结身份的 terms.tsv。

- [ ] 写入 T06 的 6 个高风险失败测试。零升级与显式升级两套输入都必须 GREEN；invalid 只验证具体效力变化错误。写集由专用命令门禁证明，不再用单元测试重复断言。

```python
def test_upgrade_decisions_materialize_migrate_rows(self):
    decisions = load_migration_decisions(UPGRADE_DECISIONS)
    ledger = render_migration_ledger(INVENTORY, decisions)
    rows = parse_ledger(ledger)
    migrated = [row for row in rows if row["disposition"] == "migrate"]
    self.assertEqual(EXPECTED_UPGRADE_IDENTITIES, {row["legacy_identity"] for row in migrated})

def test_decision_hash_must_match_adr(self):
    expected_decisions = read_machine_value(DECISION_ADR, "decisions_sha256")
    expected_records = read_machine_value(DECISION_ADR, "records_sha256")
    self.assertEqual(expected_decisions, hash_file(DECISIONS))
    self.assertEqual(expected_records, hash_file(RECORDS))
```

`EXPECTED_UPGRADE_IDENTITIES` 来自 upgrade.tsv 中显式标记的夹具行；`read_machine_value()` 在测试模块按以下代码定义，不读取普通 prose。

```python
def read_machine_value(path, key):
    blocks = extract_named_json_blocks(path.read_text(encoding="utf-8"), "terminology_migration_decision")
    if len(blocks) != 1 or key not in blocks[0]:
        raise AssertionError(f"decision machine value {key}")
    return blocks[0][key]
```

测试模块从 `scripts.governance.check_term_inputs` 导入已经在 T01 完整实现的 `extract_named_json_blocks`，不定义第二个解析器。

- [ ] 运行 RED：`python3 -m unittest tests.governance.test_term_decisions -v`。预期缺少 terms.tsv、升级覆盖算法或决定哈希不匹配。

- [ ] 从 T05 升级候选生成 `vocab/migrations/term-v1/decisions.tsv`，表头固定为 `legacy_identity operation concept_id language term_id administrative_status target_identity decision_id decision_evidence`。保持现状时文件只有表头；只有 `migrate`、`merge`、`change-language` 或 `delete` 才增加数据行。每个升级身份至多一次；`delete` 必须引用逐项 L3 决定，其他升级必须引用 L2 决定。对 `migrate`、`merge` 或 `change-language` 涉及的记录在 `records.yaml` 写完整 TermsDocument，并通过 T02、T03。

- [ ] 创建 `design/decisions/terminology-migration-rows.md`。`decision-term-0002` 登记冻结术语表哈希、decisions.tsv 哈希、records.yaml 的可选哈希、升级行数、各 operation 计数和批准日期。决定明确批准的是升级行，不重新批准或推翻未列出的冻结结论。

- [ ] 将决定输入单独提交，不能与生成账本或代码提交合并。

```bash
git add vocab/migrations/term-v1/decisions.tsv design/decisions/terminology-migration-rows.md
test ! -e vocab/migrations/term-v1/records.yaml || git add vocab/migrations/term-v1/records.yaml
git commit -m "[L2] 术语治理：批准迁移升级决定"
```

- [ ] 运行物化命令。

运行：`python3 scripts/governance/migrate_terms.py materialize --inventory .superpowers/sdd/2026-08-31-governance-implementation-prep/term-glossary.tsv --decisions vocab/migrations/term-v1/decisions.tsv --output vocab/migrations/term-v1/terms.tsv --decision design/decisions/terminology-migration-rows.md`

预期：退出码 0；terms.tsv 348 行、身份一一对应、冻结字段不变、升级行逐项带决定引用，哈希和计数写入 ignored 验证输出。没有升级行时仍成功物化 348 行继承账本。

- [ ] 实现 I12A：解析 terms.tsv 中 migrate 行，加载 records.yaml 为 TermsDocument；每个 migrate concept_id／language／term_id 必须在 records 中恰好解析，每个 records 术语必须反向对应至少一行 migrate，未使用记录或缺行都失败。返回文档后立即运行 I06、I07。

```python
def build_terms_document(ledger, records_path):
    rows = parse_ledger_bytes(ledger)
    document = load_terms(records_path)
    expected = {
        (row["concept_id"], row["language"], row["term_id"])
        for row in rows
        if row["disposition"] == "migrate"
    }
    actual = {
        (concept.id, language.language, term.id)
        for concept in document.concepts
        for language in concept.languages
        for term in language.terms
    }
    if expected != actual:
        raise ValueError(f"TERM_RECORD_COVERAGE missing={sorted(expected - actual)} extra={sorted(actual - expected)}")
    return document
```

`parse_ledger_bytes()` 在 migrate_terms.py 用与测试 parse_ledger 相同的 DictReader 实现，并把单个连字符转为 None。

- [ ] 运行 GREEN：`python3 -m unittest tests.governance.test_term_migration tests.governance.test_term_decisions -v`，预期 14 项高风险测试通过。

- [ ] 运行 `migrate_terms.py validate`。账本验证只要求 348／348 身份闭合、冻结字段不变和所有升级合法；未升级的 `defer`、`keep`、`remove` 不构成账本阻断。正式唯一术语编辑源的 T12／T13 另检查候选是否具有足够 active 记录重现获准发布视图，不能把该发布条件倒灌成 348 行重复审查。

- [ ] 运行 T06 迁移闭合阶段的完整回归。

运行：`python3 -m unittest discover -s tests -p 'test_*.py' -v`

预期：全部测试通过。

运行：`python3 scripts/check-topics.py`

预期：0 问题。

运行：`python3 scripts/check_sources.py --root .`

预期：来源严格校验 0 问题。

运行：`python3 scripts/governance/check_known_link_failures.py`

预期：`KNOWN_LINK_FAILURES_OK count=2`。

运行：`git diff --check`

预期：无输出。

- [ ] 运行两次写集门禁。人的决定提交前，允许路径恰为 `vocab/migrations/term-v1/decisions.tsv`、`records.yaml` 和决定文；该提交完成后，把 HEAD 作为物化基线，再运行：

运行：`python3 scripts/governance/check_write_set.py --base HEAD --allow vocab/migrations/term-v1/terms.tsv --allow tests/governance/test_term_decisions.py --allow tests/fixtures/terminology/decisions/upgrade.tsv --allow tests/fixtures/terminology/decisions/invalid.tsv`

预期：退出码 0，只列物化提交 4 个路径；decisions.tsv、records.yaml 和决定文不在第二次差异中。

- [ ] 记录回滚：不能 revert 删除 decision-term-0002 或 decisions.tsv。若物化算法错误，revert 仅物化提交并修复后重生 terms.tsv；若升级答案改变，新增决定修订对应升级行，再物化新账本，旧提交保留。未升级的冻结行不进入重新裁决。

- [ ] 提交物化任务。

```bash
git add vocab/migrations/term-v1/terms.tsv tests/governance/test_term_decisions.py tests/fixtures/terminology/decisions/upgrade.tsv tests/fixtures/terminology/decisions/invalid.tsv
git commit -m "[L2] 术语治理：物化继承迁移账本"
```

### 确定生成

任务标识：T07。只用夹具和 ignored 输出开发；正式输出由 T12 候选生成并在 T13 应用。

**Files:**

- Create: `schemas/term-cutover-state-v1.schema.json`
- Create: `scripts/governance/build_terms.py`
- Create: `tests/governance/test_term_generation.py`
- Create: `vocab/glossary-layout.yaml`
- Create: `tests/fixtures/terminology/states/active.yaml`
- Create: `tests/fixtures/terminology/states/rolled-back.yaml`

**Interfaces:**

- Consumes: I05–I07、H12、H13；I13／I14 由本任务实现，不作前置。
- Produces: I13、I14；私有函数 `canonical_json(value)`、`load_cutover_state(path)`、`ordered_concepts(document, layout)` 在本任务定义。

- [ ] 写入 T07 的 6 个高风险失败测试，active 和 rolled_back 状态都必须覆盖。固定布局由候选输出审查和漂移检查覆盖，不单设结构测试。

```python
def test_generation_is_byte_stable(self):
    first = canonical_snapshot(self.document, self.source_index, self.active_state)
    second = canonical_snapshot(self.document, self.source_index, self.active_state)
    self.assertEqual(first, second)
    self.assertTrue(first.endswith(b"\n"))

def test_rolled_back_state_disables_generation(self):
    with self.assertRaisesRegex(ValueError, "TERM_CONSUMERS_DISABLED"):
        canonical_snapshot(self.document, self.source_index, self.rolled_back_state)
```

- [ ] 运行 RED：`python3 -m unittest tests.governance.test_term_generation -v`。预期缺少 build_terms、state schema 和布局。

- [ ] 写入完整 cutover-state schema。根只含 schema、version、state、active_editor、terms_mode、consumers_enabled、decision、history。使用两个 `oneOf`：active 必须是 vocab/terms.yaml、active_editor、true；rolled_back 必须是 concepts/glossary.md、audit_read_only、false。history 至少一项且 additionalProperties false。

- [ ] 写入 `vocab/glossary-layout.yaml`。根只含 schema、version、groups、source_abbreviations、standards_appendix；13 个主题组加两个附录组总数 15。组 ID、显示标题与顺序来自冻结 glossary；布局不保存术语形式。

- [ ] 实现 canonical JSON。

```python
def canonical_json(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

def canonical_snapshot(document, source_index, state):
    if not state.consumers_enabled or state.terms_mode != "active_editor":
        raise ValueError("TERM_CONSUMERS_DISABLED")
    active = [concept for concept in document.concepts if concept.workflow == "active"]
    value = snapshot_value(active, source_index)
    return canonical_json(value)
```

`snapshot_value()` 在本文件完整定义：概念按 ID，语言按 zh-Hans、zh-Hant、en，术语按 preferred、admitted、deprecated、superseded 后按 ID；只复制记录值，不读取当前日期、环境语言、文件遍历或网络；附带 terms schema、data version、source index hash 和 cutover decision。

```python
import json

import yaml
from jsonschema import Draft202012Validator, FormatChecker

LANGUAGE_ORDER = {"zh-Hans": 0, "zh-Hant": 1, "en": 2}
STATUS_ORDER = {
    "preferredTerm-admn-sts": 0,
    "admittedTerm-admn-sts": 1,
    "deprecatedTerm-admn-sts": 2,
    "supersededTerm-admn-sts": 3,
}

def load_cutover_state(path):
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    schema = json.loads((REPOSITORY_ROOT / "schemas/term-cutover-state-v1.schema.json").read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value))
    if errors:
        raise ValueError(f"TERM_CUTOVER_STATE_SCHEMA {errors[0].json_path}")
    return TermCutoverState(
        schema=value["schema"],
        version=value["version"],
        state=value["state"],
        active_editor=value["active_editor"],
        terms_mode=value["terms_mode"],
        consumers_enabled=value["consumers_enabled"],
        decision=value["decision"],
        history=tuple(HistoryEvent(**item) for item in value["history"]),
    )

def ordered_concepts(document, layout):
    group_order = {group["id"]: index for index, group in enumerate(layout["groups"])}
    def concept_key(concept):
        groups = sorted(group_order[field.topic_id] for field in concept.subject_fields if field.topic_id in group_order)
        if not groups:
            raise ValueError(f"TERM_LAYOUT_GROUP_MISSING {concept.id}")
        return groups[0], concept.id
    return tuple(sorted(document.concepts, key=concept_key))
```

- [ ] 实现 `render_glossary()`：先检查 state active；只发布 active；每语言唯一 preferred 为主形式；admitted 进入允许形式；deprecated／superseded 只进历史区；缺中文写 `—`；第二行固定只读声明。布局组不存在的 active 概念返回 `TERM_LAYOUT_GROUP_MISSING`，不自动归类。

- [ ] CLI 固定为 `build --terms --state --layout --source-index --snapshot-out --glossary-out` 和 `check` 同参数。所有输出必须显式指定；`check` 重生并 cmp，漂移退出 1，不自动覆盖。

- [ ] 运行 GREEN：`python3 -m unittest tests.governance.test_term_generation -v`，预期 7 项通过。连续生成两个 ignored 目录并 `diff -ru`，预期无差异。

- [ ] 本任务只运行定向 GREEN 与写集检查；完整回归并入 T10 消费链闭合门禁。

- [ ] 运行写集门禁。

运行：`python3 scripts/governance/check_write_set.py --base HEAD --allow schemas/term-cutover-state-v1.schema.json --allow scripts/governance/build_terms.py --allow tests/governance/test_term_generation.py --allow vocab/glossary-layout.yaml --allow tests/fixtures/terminology/states/active.yaml --allow tests/fixtures/terminology/states/rolled-back.yaml`

预期：退出码 0，只列本任务 6 个文件；`concepts/glossary.md` 和 `vocab/generated/` 零差异。

- [ ] 记录回滚：revert T07 实现提交；decision-term-0002、decisions.tsv、terms.tsv 保留；重跑迁移与来源严格校验。

- [ ] 提交本任务。

```bash
git add schemas/term-cutover-state-v1.schema.json scripts/governance/build_terms.py tests/governance/test_term_generation.py vocab/glossary-layout.yaml tests/fixtures/terminology/states/active.yaml tests/fixtures/terminology/states/rolled-back.yaml
git commit -m "[L2] 术语治理：建立状态化确定生成"
```

### 委托所有权

任务标识：T08。继承结果保持生产零委托；升级决定夹具证明 active 分支可达。

**Files:**

- Create: `schemas/term-concept-v1.schema.json`
- Create: `scripts/governance/check_term_delegations.py`
- Create: `tests/governance/test_term_delegation.py`
- Create: `tests/fixtures/terminology/delegation/active.yaml`
- Create: `tests/fixtures/terminology/delegation/revoked.yaml`
- Modify: `scripts/build-topics.py`
- Modify: `scripts/check-topics.py`

**Interfaces:**

- Consumes: I09、I13、terms.tsv、独立委托决定、H09–H15；I15／I16 由本任务实现，不作前置。
- Produces: I15、I16；私有函数 `iter_delegations(vocabularies)`、`local_label_fields(record, language)` 在本任务定义。

- [ ] 写入 T08 的 5 个高风险失败测试。生产测试从真实 terms.tsv 的获准迁入行和独立委托决定得出预期，不硬编码“三项永远不委托”；夹具分别覆盖 active 与 revoked。局部对象形状交给 schema，不重复建立单元测试。

```python
def test_inherited_rows_keep_production_undelegated(self):
    expected = approved_delegations(load_migration_ledger(TERMS_LEDGER), DELEGATION_DECISIONS)
    actual = list(iter_delegations(load_five_vocabularies(ROOT)))
    self.assertEqual(expected, delegation_identities(actual))

def test_rolled_back_state_revokes_consumers(self):
    issues = validate_delegations(self.vocabularies, self.snapshot, self.rolled_back_state, True)
    self.assertIn("TERM_DELEGATION_ACTIVE_DURING_ROLLBACK", {issue.code for issue in issues})
```

`approved_delegations()` 和 `delegation_identities()` 在测试模块完整定义，只读取 terms.tsv 中有升级决定的迁入身份及独立委托决定的 concept_id、language 和 decision_id；继承行不能建立委托。

- [ ] 运行 RED：`python3 -m unittest tests.governance.test_term_delegation -v`。预期缺少 schema 和委托模块。

- [ ] 写入完整 term-concept schema。对象只含 concept、languages、state、decision、history；concept 用 H03 正则，languages 非空唯一且只取 H05，state 为 active／revoked，history 至少一项。active 和 revoked 都必须有决定。

- [ ] 实现 `iter_delegations()`：遍历五份词表各自正式记录集合，返回文件、记录 ID、term_concept。不得递归扫描任意同名键。实现 `local_label_fields()` 为各词表现有 label、alt、hidden 结构的显式映射。

```python
COLLECTIONS = {
    "topics.yaml": "concepts",
    "entities.yaml": "entities",
    "types.yaml": "types",
    "genres.yaml": "genres",
    "forms.yaml": "forms",
}

def iter_delegations(vocabularies):
    for filename, collection in COLLECTIONS.items():
        for record in vocabularies[filename].get(collection, []):
            value = record.get("term_concept")
            if value is not None:
                yield filename, record["id"], value

def local_label_fields(record, language):
    values = []
    label = record.get("label", {})
    if isinstance(label, dict) and language in label:
        values.append(("label", label[language]))
    for field in ("alt", "hidden"):
        value = record.get(field, {})
        if isinstance(value, dict) and language in value:
            values.append((field, value[language]))
    return tuple(values)
```

- [ ] 实现 I15。active 委托要求 snapshot active 概念、language 获准、external_consumers_known=true、原词表同语言没有可写本地 label／alt／hidden；revoked 要求本地标签已恢复。state rolled_back 时任何 active 委托返回错误。

- [ ] 实现 I16。只有 state active 且 consumers_enabled、概念 active、语言存在时返回唯一 preferred text；其他情况抛稳定错误，绝不回退另一语言。

- [ ] 修改 I09：加载 term-cutover-state；active 时按 active 委托读取 snapshot；rolled_back 时拒绝 snapshot 并使用恢复的本地标签。输出 ID 始终来自 topic-ids。

- [ ] 运行 GREEN：`python3 -m unittest tests.governance.test_term_delegation tests.governance.test_topic_id_stability -v`，预期 9 项高风险测试通过。生成 post-source topics，继承结果下逐字节等于 handoff 哈希；升级夹具只改变决定列明标签，不改 ID。

- [ ] 本任务只运行定向 GREEN 与写集检查；完整回归并入 T10 消费链闭合门禁。

- [ ] 运行写集门禁。

运行：`python3 scripts/governance/check_write_set.py --base HEAD --allow schemas/term-concept-v1.schema.json --allow scripts/governance/check_term_delegations.py --allow tests/governance/test_term_delegation.py --allow tests/fixtures/terminology/delegation/active.yaml --allow tests/fixtures/terminology/delegation/revoked.yaml --allow scripts/build-topics.py --allow scripts/check-topics.py`

预期：退出码 0，只列本任务 7 个路径；五份生产词表零差异。

- [ ] 记录回滚：revert T08；恢复 T04 build-topics/check-topics；决定与迁移账本保留。

- [ ] 提交本任务。

```bash
git add schemas/term-concept-v1.schema.json scripts/governance/check_term_delegations.py tests/governance/test_term_delegation.py tests/fixtures/terminology/delegation/active.yaml tests/fixtures/terminology/delegation/revoked.yaml scripts/build-topics.py scripts/check-topics.py
git commit -m "[L2] 术语治理：约束委托唯一所有权"
```

### 正文诊断

任务标识：T09。扫描范围来自当前 Git 清单，不固定文件数量。

**Files:**

- Create: `schemas/term-usage-decisions-v1.schema.json`
- Create: `scripts/governance/check_term_usage.py`
- Create: `tests/governance/test_term_usage.py`
- Modify: `scripts/check-terms.py`
- Modify: `tests/test_check_terms.py`
- Create in T12 candidate, apply in T13: `vocab/term-usage-decisions.yaml`
- Generate in T12 candidate, apply in T13: `vocab/generated/term-usage-report.tsv`
- Generate in T12 candidate, apply in T13: `vocab/generated/term-usage-manifest.json`

**Interfaces:**

- Consumes: I04、I13、H17、H18；I17 由本任务实现，不作前置。
- Produces: I17；私有函数 `classify_markdown_path(path)`、`scan_line(line, line_number, context)`、`manifest_delta(previous, current, allowed)` 在本任务定义。

- [ ] 写入 T09 的 5 个高风险失败测试。夹具在测试中新增和删除 Markdown，断言只有允许写集变化通过；不断言总数。括注标题的单一解析边角不单设 TDD，若真实回归再次出现再补最小测试。

```python
def test_scans_dynamic_markdown_manifest(self):
    paths = [entry["path"] for entry in current_markdown_manifest(self.root)]
    hits = scan_markdown(self.root, paths, self.snapshot)
    self.assertEqual(set(paths), scanned_or_classified_paths(hits, paths))
```

`scanned_or_classified_paths()` 在测试模块内返回命中路径加明确零命中清单，确保每个输入路径有扫描状态。

- [ ] 运行 RED：`python3 -m unittest tests.governance.test_term_usage -v`。预期缺少动态扫描模块。

- [ ] 写入完整 usage decisions schema。根只含 schema、version、decisions；每项只含 id、identity、file、line、column、severity、conclusion、decided、decision、history；severity 三值，history 至少一项，additionalProperties false。

- [ ] 实现动态清单：调用 I04，保存每个 path、sha256、classification、scan_state。`classify_markdown_path()` 按根文档、concepts、design 正式、drafts、decisions、sources、docs/superpowers、vocab 明确分类；未知目录仍扫描并标 review，不跳过。

```python
def classify_markdown_path(path):
    value = path.as_posix()
    if value in {"AGENTS.md", "README.md"}:
        return "formal"
    if value.startswith("concepts/"):
        return "generated" if value == "concepts/glossary.md" else "formal"
    if value.startswith("design/drafts/"):
        return "draft"
    if value.startswith("design/decisions/"):
        return "history"
    if value.startswith("design/"):
        return "formal"
    if value.startswith("sources/"):
        return "source"
    if value.startswith("docs/superpowers/"):
        return "audit"
    if value.startswith("vocab/"):
        return "history"
    return "review"

def manifest_delta(previous, current, allowed):
    before = {item["path"]: item["sha256"] for item in previous}
    after = {item["path"]: item["sha256"] for item in current}
    changed = {path for path in set(before) | set(after) if before.get(path) != after.get(path)}
    return sorted(changed - set(allowed))
```

- [ ] 实现上下文解析。围栏代码、行内代码、链接目标和路径为 excluded；来源转录、代码值、决定历史为 context-only；正文为 prose。每个 UsageHit 保存行列；同形不合并。中英括注只在完整右括号存在时分离，不完整形式保留 review。

```python
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
PARENTHESIZED_ENGLISH = re.compile(r"^(?P<zh>.*[一-鿿])\s+\([A-Za-z][^()]*\)$")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
CHINESE_QUOTE = re.compile(r"“([^”]+)”")

def scan_line(line, line_number, context):
    visible = remove_inline_code_and_link_targets(line)
    values = []
    heading = HEADING.match(visible)
    if heading:
        raw = heading.group(1)
        match = PARENTHESIZED_ENGLISH.match(raw)
        values.append((raw, match.group("zh") if match else raw, "heading"))
    values.extend((value, value, "bold") for value in BOLD.findall(visible))
    values.extend((value, value, "quote") for value in CHINESE_QUOTE.findall(visible))
    hits = []
    for raw, normalized, kind in values:
        column = line.find(raw) + 1
        hits.append((line_number, column, context, kind, raw, normalized.strip()))
    return hits
```

`remove_inline_code_and_link_targets()` 在同文件按当前 check-terms 的明确正则实现；围栏状态由 scan_markdown 在逐行循环中维护，围栏内整行标 excluded。路径 classification 为 source／history／audit 时命中 context-only，formal／review 为 prose；generated glossary 不扫描 designation，只校验漂移。

- [ ] 修改旧入口：`scripts/check-terms.py` 只做 CLI 包装，保留 `--all`，新增 `--format`、`--output`、`--snapshot`、`--state`、`--decisions`；现有 6 测试继续通过，输出仍称待人工判断。

- [ ] 运行 GREEN：`python3 -m unittest tests.governance.test_term_usage tests.test_check_terms -v`。预期新增 5 项高风险诊断测试和既有兼容测试全部通过；不以全库固定总数验收。运行 ignored 扫描，输出 manifest 中的 count 取实际清单长度，不与常量比较。

- [ ] 本任务只运行定向 GREEN 与写集检查；完整回归并入 T10 消费链闭合门禁。

- [ ] 运行写集门禁。

运行：`python3 scripts/governance/check_write_set.py --base HEAD --allow schemas/term-usage-decisions-v1.schema.json --allow scripts/governance/check_term_usage.py --allow tests/governance/test_term_usage.py --allow scripts/check-terms.py --allow tests/test_check_terms.py`

预期：退出码 0，只列本任务 5 个文件；三个正式输出不出现。

- [ ] 记录回滚：revert T09；恢复旧 check-terms 和 tests；决定、账本与术语工具保留。

- [ ] 提交本任务。

```bash
git add schemas/term-usage-decisions-v1.schema.json scripts/governance/check_term_usage.py tests/governance/test_term_usage.py scripts/check-terms.py tests/test_check_terms.py
git commit -m "[L2] 术语治理：建立动态正文诊断"
```

### 维护索引

任务标识：T10。术语义务只引用来源义务 ID；来源义务字段和状态不复制。

**Files:**

- Create: `schemas/term-obligations-v1.schema.json`
- Create: `scripts/governance/term_maintenance.py`
- Create: `tests/governance/test_term_maintenance.py`
- Create in T12 candidate, apply in T13: `vocab/term-obligations.yaml`
- Generate in T12 candidate, apply in T13: `vocab/generated/term-reference-index.json`

**Interfaces:**

- Consumes: I05–I07、来源义务 ID、H19、H20；I18–I20 由本任务实现，不作前置。
- Produces: I18–I20；私有函数 `decision_index(root)`、`obligation_index(value)`、`history_prefix(before, after)` 在本任务定义。

- [ ] 写入 T10 的 6 个失败测试。

```python
def test_source_obligation_bridge_uses_id_only(self):
    obligation = open_term_obligation(
        "source_obligation",
        "source-review-20260831-001",
        (self.target,),
        "2026-09-15",
        None,
    )
    self.assertEqual("source-review-20260831-001", obligation.trigger.id)
    self.assertFalse(hasattr(obligation.trigger, "source_state"))
```

- [ ] 运行 RED：`python3 -m unittest tests.governance.test_term_maintenance -v`。预期缺少 schema 和模块。

- [ ] 写入完整 obligations schema。根只含 schema、version、obligations；义务只含 id、targets、trigger、state、opened、closed、decision、history。ID 为 `term-review-YYYYMMDD-NNN` 的正则，open 要求 closed null，resolved 要求 closed date；targets 非空；history 至少一项。

- [ ] 实现 I18。新义务 ID 由 opened 去连字符日期加当日未用三位序号；trigger 只保存 kind、id、previous_obligation。来源桥接不加载或复制来源义务内容。

- [ ] 实现 I19。open 到 resolved 要求每个 target 有 conclusion／reviewed，必要 decision 存在，closed 不早于 opened，history 前缀保持；resolved 不得重开，再触发新 ID 并指向 previous。

- [ ] 实现 I20。索引键覆盖概念、术语、委托、决定、义务和 generated_output；每项保存 target_kind、target_id、reference_kind、file、record、field_path、state。按稳定元组排序。索引只含术语治理对象，不复制来源 index；来源引用由 T11 调用来源生成器发现。

```python
def history_prefix(before, after):
    return tuple(after[:len(before)]) == tuple(before)

def decision_index(root):
    result = {}
    for path in sorted((root / "design/decisions").glob("*.md")):
        for block in extract_all_decision_json(path.read_text(encoding="utf-8")):
            decision_id = block["id"]
            if decision_id in result:
                raise ValueError(f"TERM_DECISION_DUPLICATE {decision_id}")
            result[decision_id] = path.relative_to(root).as_posix()
    return result

def obligation_index(value):
    result = {}
    for obligation in value["obligations"]:
        if obligation["id"] in result:
            raise ValueError(f"TERM_OBLIGATION_DUPLICATE {obligation['id']}")
        result[obligation["id"]] = obligation
    return result
```

`extract_all_decision_json()` 复用 T01 的围栏解析器，接受来源和术语决定块的已登记名称集合；未知决定块不进入机器索引但保留文档。I20 从 TermsDocument、iter_delegations、decision_index 和 obligation_index 四个显式访问器收集条目，不递归猜字段。

- [ ] 明确无调度：代码中不存在月份、次数、百分比阈值；检测到旧维护阈值字段返回 `TERM_PERIODIC_POLICY_NOT_APPROVED`。

- [ ] 运行 GREEN：`python3 -m unittest tests.governance.test_term_maintenance -v`，预期 6 项通过。双跑术语索引夹具字节相同。

- [ ] 运行 T10 消费链闭合阶段的完整回归。

运行：`python3 -m unittest discover -s tests -p 'test_*.py' -v`

预期：全部测试通过。

运行：`python3 scripts/check-topics.py`

预期：0 问题。

运行：`python3 scripts/check_sources.py --root .`

预期：来源严格校验 0 问题。

运行：`python3 scripts/governance/check_known_link_failures.py`

预期：`KNOWN_LINK_FAILURES_OK count=2`。

运行：`git diff --check`

预期：无输出。

- [ ] 运行写集门禁。

运行：`python3 scripts/governance/check_write_set.py --base HEAD --allow schemas/term-obligations-v1.schema.json --allow scripts/governance/term_maintenance.py --allow tests/governance/test_term_maintenance.py`

预期：退出码 0，只列本任务 3 个文件；正式义务和索引不出现。

- [ ] 记录回滚：revert T10；义务正式文件尚未创建，人的决定与迁移账本保留。

- [ ] 提交本任务。

```bash
git add schemas/term-obligations-v1.schema.json scripts/governance/term_maintenance.py tests/governance/test_term_maintenance.py
git commit -m "[L2] 术语治理：建立义务与术语索引"
```

### 切换实现

任务标识：T11。任务只实现并提交切换代码、真实阶段测试定义和夹具；真实 candidate 与真实 manifest 必须在本任务开始、测试、审查和提交完成时都不存在。

**Files:**

- Create: `scripts/governance/cutover_terms.py`
- Create: `tests/governance/test_term_cutover.py`
- Create: `tests/governance/test_term_activation.py`
- Create: `tests/fixtures/terminology/cutover/active/`
- Create: `tests/fixtures/terminology/cutover/rolled-back/`
- Write ignored: `.superpowers/sdd/2026-08-31-terminology-schema-generation/implementation-dry-run/`

**Interfaces:**

- Consumes: I02、I05–I20、H13、H23。
- Produces: I21–I29；私有函数 `verify_candidate_payload(repo_root, candidate_root, manifest_path, implementation_commit, allow_head_descendant=False)`、`run_source_index(root)`、`run_source_strict(root)`、`require_zero(result, code)`、`diff_entries(repo_root, candidate_root)`、`canonical_payload_bytes(value)`、`apply_approved_delegations(root, ledger)`、`render_cutover_state(mode, decision, history)` 在本任务定义。

- [ ] 确认真实材料不存在。

  Run: `test ! -e .superpowers/sdd/2026-08-31-terminology-schema-generation/candidate-root && test ! -e .superpowers/sdd/2026-08-31-terminology-schema-generation/payload-manifest.json`

  Expected: 退出码 0。存在任一路径即停止；不得把旧 candidate 当作 T11 测试夹具。

- [ ] 写入 T11 的 8 个失败测试。八项都属于 `tests.governance.test_term_cutover.TermCutoverFixtureTests`，只使用 `tests/fixtures/terminology/cutover/` 下的临时 Git fixture；fixture 先提交实现基线，再在临时目录生成 candidate，candidate 明确没有 `.git`。

```python
class TermCutoverFixtureTests(unittest.TestCase):
    def test_candidate_markdown_uses_implementation_tree_without_git(self):
        implementation_commit = git_head(self.repo)
        tracked = tracked_paths_at_commit(self.repo, implementation_commit)
        build_complete_candidate(
            self.repo, self.candidate, self.handoff, tracked, implementation_commit,
        )
        self.assertFalse((self.candidate / ".git").exists())
        entries = diff_entries(self.repo, self.candidate)
        manifest = candidate_markdown_manifest(self.candidate, tracked, entries)
        self.assertEqual(
            expected_candidate_markdown(self.repo, self.candidate, tracked, entries),
            manifest,
        )

    def test_payload_manifest_excludes_itself(self):
        implementation_commit = git_head(self.repo)
        tracked = tracked_paths_at_commit(self.repo, implementation_commit)
        build_complete_candidate(
            self.repo, self.candidate, self.handoff, tracked, implementation_commit,
        )
        manifest = build_payload_manifest(
            self.repo, self.candidate, self.handoff, implementation_commit,
            self.manifest_path,
        )
        self.assertNotIn(
            self.manifest_path.as_posix(),
            {entry["path"] for entry in manifest.entries},
        )
        self.assertEqual(implementation_commit, manifest.base_commit)

    def test_source_index_contains_term_references(self):
        implementation_commit = git_head(self.repo)
        tracked = tracked_paths_at_commit(self.repo, implementation_commit)
        build_complete_candidate(
            self.repo, self.candidate, self.handoff, tracked, implementation_commit,
        )
        entries = load_json(
            self.candidate / "vocab/generated/source-reference-index.json",
        )["entries"]
        actual = {
            entry["field_path"] for entry in entries
            if entry["file"] == "vocab/terms.yaml"
        }
        self.assertEqual(
            expected_term_reference_paths(self.candidate / "vocab/terms.yaml"),
            actual,
        )
```

  其余五项逐字使用测试账本中的 T11 名称。测试模块完整定义 `git_head()`、`expected_candidate_markdown()` 与 `expected_term_reference_paths()`；后者调用 T02 `collect_reference_uses()`。fixture handoff 使用来源计划十个顶层键，fixture payload 使用三个顶层键。

- [ ] 写入 T12 与 T13 的真实阶段测试定义，但本任务不运行它们。`tests/governance/test_term_activation.py` 只定义两个类：`TermCandidatePrebindingTests` 包含 T12 两项，`TermBoundApplicationTests` 包含 T13 一项。路径从显式环境变量读取；缺变量立即失败，不 skip，不回退到夹具或默认决定。

```python
def required_path(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"TERM_PHASE_PATH_MISSING {name}")
    return pathlib.Path(value)

class TermCandidatePrebindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = required_path("KB_TERM_REPO_ROOT")
        cls.candidate_root = required_path("KB_TERM_CANDIDATE_ROOT")
        cls.manifest_path = required_path("KB_TERM_MANIFEST")
        cls.implementation_commit = required_text("KB_TERM_IMPLEMENTATION_COMMIT")

    def test_candidate_base_commit_is_implementation_commit(self):
        manifest = load_payload_manifest(self.manifest_path)
        self.assertEqual(self.implementation_commit, manifest.base_commit)
        self.assertEqual(
            tuple(tracked_paths_at_commit(self.repo_root, manifest.base_commit)),
            tuple(manifest_tracked_basis(manifest)),
        )

    def test_real_candidate_passes_prebinding_validation(self):
        allow_descendant = os.environ.get("KB_TERM_ALLOW_HEAD_DESCENDANT") == "1"
        self.assertEqual([], verify_candidate_payload(
            self.repo_root,
            self.candidate_root,
            self.manifest_path,
            self.implementation_commit,
            allow_head_descendant=allow_descendant,
        ))

class TermBoundApplicationTests(unittest.TestCase):
    def test_decision_binding_and_apply_only_uses_bound_candidate(self):
        repo_root = required_path("KB_TERM_REPO_ROOT")
        candidate_root = required_path("KB_TERM_CANDIDATE_ROOT")
        manifest_path = required_path("KB_TERM_MANIFEST")
        decision_path = required_path("KB_TERM_CUTOVER_DECISION")
        self.assertEqual([], verify_bound_payload(
            repo_root, candidate_root, manifest_path, decision_path,
        ))
        sandbox = copy_application_sandbox(repo_root, candidate_root, manifest_path)
        forbidden = (
            "build_complete_candidate", "build_payload_manifest", "build_terms",
            "build_topics", "rewrite_activation_documents", "run_source_index",
            "run_source_strict",
        )
        with forbid_cutover_functions(forbidden), mock.patch(
            "scripts.governance.cutover_terms.verify_bound_payload", return_value=(),
        ):
            result = apply_bound_candidate(
                sandbox.repo_root, sandbox.candidate_root,
                sandbox.manifest_path, decision_path,
            )
        self.assertEqual(
            expected_manifest_paths(manifest_path),
            set(result.written) | set(result.deleted),
        )
        self.assertEqual(sandbox.side_project_hashes,
                         hash_side_projects(sandbox.repo_root))
```

  `required_text()`、`manifest_tracked_basis()`、`copy_application_sandbox()`、`forbid_cutover_functions()`、`expected_manifest_paths()` 和 `hash_side_projects()` 在同一测试模块完整定义。sandbox 从 manifest.base_commit 的 Git blobs 重建 entries 的 before 树，再复制 candidate 字节和三份旁路草案；它不复制或修改真实工作树。决定绑定先在真实路径只读验证，apply-only 再在 sandbox 验证。

- [ ] 运行 RED：`python3 -m unittest tests.governance.test_term_cutover.TermCutoverFixtureTests -v`。预期缺少 cutover_terms；不得运行 `tests/governance/test_term_activation.py`。

- [ ] 实现 I21。

```python
def tracked_paths_at_commit(repo_root, commit):
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "-z", commit],
        cwd=repo_root, check=True, capture_output=True,
    ).stdout
    return tuple(sorted(path.decode("utf-8") for path in result.split(b"\0") if path))
```

- [ ] 实现 I22。复制参数 `implementation_commit` 的 Git tree 到不存在的 candidate，排除 `.git`／`.superpowers`；不能复制调用时未提交的工作树。生成 terms、state、维护起点、委托、术语输出、topics、source index、term index、usage 输出、design/terminology、旧草案删除和全部共享文档重写；运行 source index 双跑、source strict、术语校验和草案核销。函数不生成 payload manifest。

- [ ] 实现 I23，不在 candidate 调用 Git。

```python
def candidate_markdown_manifest(candidate_root, tracked_paths, entries):
    paths = {path for path in tracked_paths if path.endswith(".md")}
    for entry in entries:
        path = entry["path"]
        if not path.endswith(".md"):
            continue
        if entry["action"] == "delete":
            paths.discard(path)
        else:
            paths.add(path)
    rows = []
    for path in sorted(paths):
        target = candidate_root / path
        if not target.is_file():
            raise ValueError(f"CANDIDATE_MARKDOWN_MISSING {path}")
        rows.append({"path": path, "sha256": sha256_path(target)})
    return tuple(rows)
```

- [ ] 实现 I24。manifest 位于 candidate 外；entries 不含 manifest 或三份决定；base_commit 必须等于参数 implementation_commit；candidate_markdown 只调用 I23。source handoff SHA-256 从 `repo_root / SOURCE_HANDOFF` 的实际字节计算；source payload SHA-256 取 `handoff.payload["sha256"]`，并验证 `handoff.payload["path"] == SOURCE_PAYLOAD.as_posix()` 及 `hash_file(repo_root / SOURCE_PAYLOAD)` 相等。

```python
def build_payload_manifest(repo_root, candidate_root, handoff, implementation_commit, manifest_path):
    if git_head(repo_root) != implementation_commit:
        raise ValueError("IMPLEMENTATION_COMMIT_NOT_HEAD")
    if handoff.payload != {
        "path": SOURCE_PAYLOAD.as_posix(),
        "sha256": hash_file(repo_root / SOURCE_PAYLOAD),
    }:
        raise ValueError("SOURCE_PAYLOAD_BINDING")
    entries = diff_entries(repo_root, candidate_root)
    value = {
        "schema": "urn:kb-design:data:term-cutover-payload",
        "version": 1,
        "source_handoff_sha256": hash_file(repo_root / SOURCE_HANDOFF),
        "source_payload_sha256": handoff.payload["sha256"],
        "base_commit": implementation_commit,
        "entries": entries,
        "delete_paths": sorted(row["path"] for row in entries if row["action"] == "delete"),
        "preserve_paths": sorted(PRESERVE_PATHS),
        "restore_paths": sorted(RESTORE_PATHS),
        "candidate_markdown": candidate_markdown_manifest(
            candidate_root,
            tracked_paths_at_commit(repo_root, implementation_commit),
            entries,
        ),
    }
    data = canonical_payload_bytes(value)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_bytes(data)
    return PayloadManifest(**value)
```

- [ ] 实现无决定预验。`verify_candidate_payload(repo_root, candidate_root, manifest_path, implementation_commit, allow_head_descendant=False)` 默认要求当前 HEAD 恰为 implementation_commit；只有 I25 与 T13 完整回归显式允许 HEAD 为其后代。manifest base_commit 必须相同，manifest 字节规范且不含自身，entries 的 before 哈希从 manifest.base_commit 的 Git blobs 计算，after 哈希从 candidate 计算，Create／Modify／Delete 集合逐项相等；source handoff／payload 双哈希仍匹配，candidate Markdown、preserve／restore、双索引、source strict、术语校验和草案核销都通过。函数没有 decision 参数，也不读取三份未来决定。

- [ ] 实现 I25／I26。I25 先调用同一候选预验核心，但允许当前 HEAD 为 implementation_commit 的后代；随后要求 base→HEAD 路径集合恰为三份决定，验证 `decision-term-0004` 的 ignored manifest 路径与 `payload_manifest_sha256`。I26 只 copy／delete entries，禁止调用 I22、I24 或任一生成函数，失败时从 backup 恢复。

```python
BOUND_DECISION_PATHS = frozenset({
    "design/decisions/terminology-governance-effective.md",
    "design/decisions/terminology-schema-cutover.md",
    "design/decisions/terminology-schema-rollback.md",
})

def verify_bound_payload(repo_root, candidate_root, manifest_path, decision_path):
    manifest = load_payload_manifest(manifest_path)
    issues = list(verify_candidate_payload(
        repo_root, candidate_root, manifest_path, manifest.base_commit,
        allow_head_descendant=True,
    ))
    actual = frozenset(committed_paths_between(
        repo_root, manifest.base_commit, git_head(repo_root),
    ))
    if actual != BOUND_DECISION_PATHS:
        issues.append(term_issue("TERM_BOUND_COMMIT_PATHS", sorted(actual)))
    front = load_yaml_front_matter(decision_path)
    if (front.get("id") != "decision-term-0004"
            or front.get("status") != "accepted"
            or front.get("delivery_manifest") != manifest_path.as_posix()
            or front.get("payload_manifest_sha256") != hash_file(manifest_path)
            or front.get("base_commit") != manifest.base_commit):
        issues.append(term_issue("TERM_PAYLOAD_DECISION_BINDING", str(decision_path)))
    return tuple(sorted(issues))
```

  `verify_candidate_payload(..., allow_head_descendant=False)` 是 T12 的默认；只有 I25 显式传 true。`committed_paths_between()` 使用 `git diff --name-only --diff-filter=ACDMRTUXB <base>..<head>`，返回规范化相对路径；manifest、candidate 和 ignored 证据不会进入集合。

- [ ] 实现 I27／I28 回滚候选和验证；实现 I29 草案逐节核销。回滚也使用“实现先提交、候选后生成、决定绑定、apply-only”顺序。

- [ ] 运行 GREEN：`python3 -m unittest tests.governance.test_term_cutover.TermCutoverFixtureTests -v`。预期 T11 的 8 项夹具测试通过；测试候选不写正式树。只运行 `python3 -m py_compile tests/governance/test_term_activation.py` 验证真实阶段测试语法，不执行其中 3 项。

- [ ] 运行 69 项无真实材料高风险门禁。命令显式列 T01–T10 十个测试模块和 `tests.governance.test_term_cutover.TermCutoverFixtureTests`；不得使用会发现 `test_term_activation.py` 的 `unittest discover`。

  Run: `python3 -m unittest tests.governance.test_term_baseline tests.governance.test_term_model tests.governance.test_term_transitions tests.governance.test_topic_id_stability tests.governance.test_term_migration tests.governance.test_term_decisions tests.governance.test_term_generation tests.governance.test_term_delegation tests.governance.test_term_usage tests.governance.test_term_maintenance tests.governance.test_term_cutover.TermCutoverFixtureTests -v`

  Expected: 69 tests PASS；没有测试读取真实 candidate、manifest 或 decision-term-0003／0004／0005。

- [ ] 逐条运行其余回归：check-topics、check-sources strict、known-link wrapper、git diff --check。预期全绿或已知链接恰两条。

- [ ] 写集门禁只允许 cutover_terms.py、两个测试文件和两个 fixture 目录；ignored dry-run 不计。门禁后再次运行真实材料不存在命令，确认正式 candidate／manifest 未生成。

- [ ] 记录回滚：revert T11 实现提交只移除实现和测试；决定与既有账本保留。

- [ ] 提交切换实现。

```bash
git add scripts/governance/cutover_terms.py tests/governance/test_term_cutover.py tests/governance/test_term_activation.py tests/fixtures/terminology/cutover/active tests/fixtures/terminology/cutover/rolled-back
git commit -m "[L2] 术语治理：完成切换实现与测试"
```

### 候选冻结

任务标识：T12。任务从干净的 T11 实现提交生成并预验最终 ignored candidate 与 ignored manifest，再完成人类先行决定；不运行决定绑定测试，不应用 payload。

**Files:**

- Write ignored: `.superpowers/sdd/2026-08-31-terminology-schema-generation/candidate-root/`
- Write ignored: `.superpowers/sdd/2026-08-31-terminology-schema-generation/payload-manifest.json`
- Create after review: `design/decisions/terminology-governance-effective.md`
- Create after review: `design/decisions/terminology-schema-cutover.md`
- Create after review: `design/decisions/terminology-schema-rollback.md`

**Interfaces:**

- Consumes: I21–I24、`verify_candidate_payload()`、decision-term-0002、source handoff／payload。
- Produces: 完整 ignored candidate、无自引用 manifest、decision-term-0003／0004／0005 的先行审计提交。

- [ ] 验证实现基线和真实材料初态。工作树必须干净，`git rev-parse HEAD` 必须是 T11 “[L2] 术语治理：完成切换实现与测试”；把该值写入 ignored `implementation-commit.txt`。candidate、manifest 和三份 cutover 决定在生成前都必须不存在。

- [ ] 用 I21 从 implementation_commit 读取 tracked path 集合；把排序路径和集合 SHA-256 写入 ignored 验证证据。禁止从 candidate 根调用 Git。

- [ ] 运行 I22 生成完整 candidate。candidate 包含 T13 全部 Create／Modify／Delete，包括 formal design、旧草案删除、共享文档、维护起点、terms／state、委托、输出、topics 和双索引。

- [ ] 运行 I24 两次，分别写两个 ignored 临时 manifest。两者逐字节相等后，把第一份原子重命名为 `payload-manifest.json` 并删除第二份；base_commit 固定为 implementation_commit，manifest 不含自身或三份未来决定。

- [ ] 运行 `verify_candidate_payload()`；预期零问题。该调用只接收 repo、candidate、manifest、implementation_commit，不接收或读取任何 cutover decision。

- [ ] 运行 T12 两项真实预验测试。

  Run: `KB_TERM_REPO_ROOT=/Users/xiu/code/kb-design KB_TERM_CANDIDATE_ROOT=/Users/xiu/code/kb-design/.superpowers/sdd/2026-08-31-terminology-schema-generation/candidate-root KB_TERM_MANIFEST=/Users/xiu/code/kb-design/.superpowers/sdd/2026-08-31-terminology-schema-generation/payload-manifest.json KB_TERM_IMPLEMENTATION_COMMIT=$(git rev-parse HEAD) python3 -m unittest tests.governance.test_term_activation.TermCandidatePrebindingTests -v`

  Expected: 2 tests PASS；只验证 base_commit、Git tree basis、candidate 结构、逐项哈希与无决定预验。

- [ ] 运行 71 项非决定绑定高风险门禁。使用 T11 的 69 项显式命令，再追加 `tests.governance.test_term_activation.TermCandidatePrebindingTests`；不得运行 `TermBoundApplicationTests` 或 `unittest discover`。

  Run: `KB_TERM_REPO_ROOT=/Users/xiu/code/kb-design KB_TERM_CANDIDATE_ROOT=/Users/xiu/code/kb-design/.superpowers/sdd/2026-08-31-terminology-schema-generation/candidate-root KB_TERM_MANIFEST=/Users/xiu/code/kb-design/.superpowers/sdd/2026-08-31-terminology-schema-generation/payload-manifest.json KB_TERM_IMPLEMENTATION_COMMIT=$(git rev-parse HEAD) python3 -m unittest tests.governance.test_term_baseline tests.governance.test_term_model tests.governance.test_term_transitions tests.governance.test_topic_id_stability tests.governance.test_term_migration tests.governance.test_term_decisions tests.governance.test_term_generation tests.governance.test_term_delegation tests.governance.test_term_usage tests.governance.test_term_maintenance tests.governance.test_term_cutover.TermCutoverFixtureTests tests.governance.test_term_activation.TermCandidatePrebindingTests -v`

  Expected: 71 tests PASS；真实 candidate 与 manifest 被读取，decision-term-0003／0004／0005 仍不存在。

- [ ] 运行 candidate 其余预验：source strict、source index 双跑、term index 双跑、topics、usage、draft disposition、动态 Markdown 与 T13 action 集合。所有命令只读正式树或写 ignored 证据；受跟踪差异仍为零。

- [ ] 人复核 candidate 与 ignored manifest；manifest 保持原路径和字节，不创建受跟踪副本。

- [ ] 使用 `superpowers:requesting-code-review` 审查 implementation_commit、tracked path 集合、无 Git Markdown 算法、candidate 完整性、manifest 字节稳定、71 项非绑定高风险门禁和所有预验。审查输入不得包含 cutover decision，也不得声称决定绑定通过。APPROVED 后交人作三份决定。

- [ ] 人创建 decision-term-0003／0004／0005。`decision-term-0004.delivery_manifest` 写 ignored manifest 精确路径，`payload_manifest_sha256` 等于该文件 SHA-256，`base_commit` 等于 implementation_commit；0003 绑定 candidate formal design 与草案去向；0005 绑定 restore／preserve 路径。

- [ ] 先行提交三份决定，不包含 candidate 或 manifest。

```bash
git add design/decisions/terminology-governance-effective.md design/decisions/terminology-schema-cutover.md design/decisions/terminology-schema-rollback.md
git commit -m "[L3] 术语治理：批准完整切换候选"
```

- [ ] 只运行路径集合门禁：`git diff --name-only <implementation_commit>..HEAD` 排序后必须恰为三份决定路径；manifest、candidate 和任何正式 payload entry 都不得受跟踪。此步骤不读取决定字段、不比较决定哈希、不调用 I25，也不运行决定绑定测试。

- [ ] 若 candidate 或 manifest 漂移，停止并新建候选与替代决定；不得沿用旧 decision-term-0004。

### 正式应用

任务标识：T13。任务只消费 T12 已绑定 candidate 与 manifest；不生成或重写任何内容。

**Files:**

- Apply from candidate: `vocab/terms.yaml`、`vocab/term-cutover-state.yaml`、`vocab/term-obligations.yaml`、`vocab/term-usage-decisions.yaml`
- Apply from candidate: `vocab/generated/terms-v1.json`、`term-reference-index.json`、`term-usage-report.tsv`、`term-usage-manifest.json`
- Apply from candidate: Modify `vocab/generated/source-reference-index.json`、`vocab/topics.yaml`
- Apply from candidate if approved: Modify `vocab/entities.yaml`、`vocab/types.yaml`、`vocab/genres.yaml`、`vocab/forms.yaml`
- Apply from candidate: Create `design/terminology.md`、Delete `design/drafts/terminology-governance.md`
- Apply from candidate: Modify `concepts/glossary.md`、`design/governance.md`、`design/writing.md`、`design/maintenance.md`、`design/versioning.md`、`design/README.md`、`AGENTS.md`
- Create only on actual rollback: `design/decisions/terminology-schema-rollback-result.md`

**Interfaces:**

- Consumes: I25、I26、I28、I29、T12 的 71 项 GREEN、T12 candidate／manifest 与先行审计提交。
- Produces: active 正式链，或实际回滚时 decision-term-0006 补偿链。

- [ ] 运行 T13 的决定绑定与 apply-only 测试。

  Run: `KB_TERM_REPO_ROOT=/Users/xiu/code/kb-design KB_TERM_CANDIDATE_ROOT=/Users/xiu/code/kb-design/.superpowers/sdd/2026-08-31-terminology-schema-generation/candidate-root KB_TERM_MANIFEST=/Users/xiu/code/kb-design/.superpowers/sdd/2026-08-31-terminology-schema-generation/payload-manifest.json KB_TERM_CUTOVER_DECISION=/Users/xiu/code/kb-design/design/decisions/terminology-schema-cutover.md python3 -m unittest tests.governance.test_term_activation.TermBoundApplicationTests.test_decision_binding_and_apply_only_uses_bound_candidate -v`

  Expected: 1 test PASS；真实决定绑定只读通过，sandbox apply-only 不调用任何生成或预验生成函数，三份旁路草案哈希不变。

- [ ] 运行 I25；manifest.base_commit 必须是当前 HEAD 祖先，base→HEAD 路径集合恰为三份决定；candidate、manifest 和决定哈希逐项一致。任何额外路径、candidate 漂移或决定哈希不符都停止。禁止调用 I22／I24。

- [ ] 用 T13 已通过的 mock 证据确认 I26 不调用 build_complete_candidate、build_payload_manifest、build_terms、build_topics、文档重写、source index 或 source strict。

- [ ] 运行 I26 原子复制／删除 entries。复制前保存 backup，失败时恢复；apply 返回 written／deleted／preserved。

- [ ] 运行 72 项计划高风险门禁。现在真实 candidate、manifest 和三份决定都存在；T12 的预验测试显式允许 HEAD 为 implementation_commit 后代，仍从 base_commit Git blobs 复核 before 哈希。命令显式列出计划测试，不使用全库 discover。

  Run: `KB_TERM_REPO_ROOT=/Users/xiu/code/kb-design KB_TERM_CANDIDATE_ROOT=/Users/xiu/code/kb-design/.superpowers/sdd/2026-08-31-terminology-schema-generation/candidate-root KB_TERM_MANIFEST=/Users/xiu/code/kb-design/.superpowers/sdd/2026-08-31-terminology-schema-generation/payload-manifest.json KB_TERM_IMPLEMENTATION_COMMIT=$(<.superpowers/sdd/2026-08-31-terminology-schema-generation/implementation-commit.txt) KB_TERM_CUTOVER_DECISION=/Users/xiu/code/kb-design/design/decisions/terminology-schema-cutover.md KB_TERM_ALLOW_HEAD_DESCENDANT=1 python3 -m unittest tests.governance.test_term_baseline tests.governance.test_term_model tests.governance.test_term_transitions tests.governance.test_topic_id_stability tests.governance.test_term_migration tests.governance.test_term_decisions tests.governance.test_term_generation tests.governance.test_term_delegation tests.governance.test_term_usage tests.governance.test_term_maintenance tests.governance.test_term_cutover.TermCutoverFixtureTests tests.governance.test_term_activation.TermCandidatePrebindingTests tests.governance.test_term_activation.TermBoundApplicationTests -v`

  Expected: 72 项计划高风险门禁通过。随后逐条运行 check-topics、build_terms check、usage 输出比较、source index 重建比较、source strict、known links、git diff --check。全库发现测试如另行运行，只要求全部通过，不断言固定数量。

- [ ] 写集门禁从 ignored payload manifest entries 读取允许集合；三份先行决定已在 base，不出现在 apply 差异。

- [ ] 使用 `superpowers:requesting-code-review` 审查决定绑定测试、base→HEAD 三路径集合、apply-only、草案核销、双索引、source strict、动态 Markdown、72 项计划高风险门禁和唯一所有权。APPROVED 后提交。

- [ ] 提交 apply payload，不包含新决定或生成步骤。

```bash
python3 scripts/governance/cutover_terms.py pathspec --manifest .superpowers/sdd/2026-08-31-terminology-schema-generation/payload-manifest.json | git add --pathspec-from-file=- --pathspec-file-nul
git commit -m "[L3] 术语治理：应用已批准切换候选"
```

- [ ] 实际回滚同样先用已提交实现生成完整 compensation candidate／manifest，再由 decision-term-0006 绑定，最后 apply-only；保留 terms、ID、义务、history、账本与 manifest。

- [ ] 回滚后验证人工 glossary 唯一编辑、terms audit_read_only、消费者 false、active 委托 0、双索引重建、source strict 0；不使用 git revert 删除决定。

## 规格覆盖

| 要求 | 决定与任务 |
|---|---|
| 来源契约唯一消费 | H01、输入锁、I01–I06、T01、T02 |
| 冻结旧草案与后置共享锁 | 全局约束、输入锁、T01 |
| 三层模型和译名 | H02–H08、T02、T03、T06 |
| 冻结结论继承与升级决定 | H05–H10、T05、T06 |
| 主题稳定身份 | H14–H16、T04、T08 |
| 确定生成和委托 | H09–H15、T07、T08 |
| 动态正文范围 | H17、H18、T09 |
| 首轮维护接口 | H19、H20、T10 |
| source index 同步 | 文件边界、T12、T13 |
| 草案移出与逐节核销 | H13、T12、T13、I29 |
| 原子切换和补偿回滚 | H13、H23、T11–T13 |
| 不准入与旁路隔离 | 全局约束、H21、H24、T05、T13 |

## 自查命令

```bash
python3 - <<'PY'
from pathlib import Path
import re

path = Path('docs/superpowers/plans/2026-08-31-terminology-schema-generation.md')
text = path.read_text(encoding='utf-8')
lines = text.splitlines()

decision_rows = [line for line in lines if re.match(r'^\| H[0-9]{2} \|', line)]
if len(decision_rows) != 24:
    raise SystemExit(f'DECISION_COUNT {len(decision_rows)}')

tasks = re.findall(r'^任务标识：T[0-9]{2}', text, re.M)
if len(tasks) != 13:
    raise SystemExit(f'TASK_COUNT {len(tasks)}')

tests = set(re.findall(r'`(test_[a-z0-9_]+)`', text))
if len(tests) != 72:
    raise SystemExit(f'TEST_COUNT {len(tests)}')

interfaces = [line for line in lines if re.match(r'^\| I[0-9]+[A-Z]? \|', line)]
helpers = [line for line in lines if re.match(r'^\| HLP[0-9]+ \|', line)]

in_fence = False
checkboxes = 0
for line in lines:
    if line.startswith('```'):
        in_fence = not in_fence
        continue
    if not in_fence and line.startswith('- [ ]'):
        checkboxes += 1

for pattern in ('T' + 'BD', 'T' + 'ODO', 'implement ' + 'later', 'fill in ' + 'details', 'similar to ' + 'Task', '类似' + '前任务'):
    if pattern in text:
        raise SystemExit(f'PLACEHOLDER {pattern}')

print(f'PLAN_COUNTS lines={len(lines)} tasks={len(tasks)} checkboxes={checkboxes} tests={len(tests)} interfaces={len(interfaces)} helpers={len(helpers)} decisions={len(decision_rows)}')
PY
```

```bash
python3 - <<'PY'
from pathlib import Path
import re

text = Path('docs/superpowers/plans/2026-08-31-terminology-schema-generation.md').read_text(encoding='utf-8')
for number, line in enumerate(text.splitlines(), 1):
    if line.startswith('##'):
        title = line.lstrip('#').strip()
        if ':' in title or '：' in title or re.match(r'^[0-9]', title):
            raise SystemExit(f'HEADING {number} {title}')
print('HEADINGS_OK')
PY
```

```bash
git diff --check
```

预期：无输出。最终报告必须使用第一条命令的实际 checkbox 数，不从文本中的旧计数继承。

## 已知疑虑

- 当前来源计划仍需完成 source-cutover-handoff／source-cutover-payload 双文件交付；在来源实现完成、`decision-source-0005` 用 `delivery_handoff`／`handoff_sha256` 与 `delivery_payload`／`payload_sha256` 完成双绑定，且 handoff 十个顶层键、payload 三个顶层键和来源严格校验全部通过前，术语实施全部阻断。
- 348 行冻结结论由 T05／T06 自动继承，不再等待人的重复答案。decisions.tsv 可以只有表头，records.yaml 只在存在获准升级行时创建；T12／T13 仅在候选不足以重现获准发布视图，或某项升级缺少决定时停止。
- `2026-09-15` 生效窗口可能在计划获批前失效；失效后必须新建决定，不补写过去日期。
- 仓库外标签消费者仍未知；没有独立风险接受决定时 active 委托阻断。
- T11 提交后到 T13 应用前，完整 ignored candidate 与 manifest 必须持续存在且字节不变；任一丢失或漂移都要求回到 T12 重新生成、预验并取得替代决定，不能只重算哈希。
- 来源计划与术语计划共享多个文件，必须严格按来源切换后、T01–T10、T11 实现、T12 候选与决定、T13 应用的顺序执行，不能并行落地。
- 两处旧 SDD 链接失败仍是冻结基线；任何变化都要求重新判断，不能把零失败或第三条失败视作同一基线。
