# 来源字段方案

状态：已采纳，实施中。用户已批准整套方案，模型决定见[来源字段合同](../../docs/decisions/source-v2-field-contract.md)，外部状态与版本缺值按后续已采纳的[来源数据批次](../../docs/decisions/source-data-batch.md)执行。方案盘点基线为 `633f684`，工作区为 `codex/source-v2-prep`；代码、schema、生成与消费者正在按已采纳合同适配。本文仍是实施计划，不证明必需事实、用途角色、具体关系或正式切换已经完成。全部迁移与消费者验收完成前不得合并 `master`，不操作正式知识库。

## 方案目的

让现有来源记录、一般实体、用途登记及下游引用能够整批转入一个明确的严格格式，同时保留项目状态、归属判断、历史核对日期和现有身份。schema 能表示一条记录与该记录具有足够证据是两件事；P1–P4 只覆盖四份来源的少数字段，不能代替整条记录的准入。

采用保留项目 `status`、新增外部 `source_status` 的方案。项目判断与未核对材料分别保留，不进入严格外部 `basis`。来源引用使用现有 `entity` 或 `registry` 两种对象身份，所有角色和每条派生、映射、外部分组分别满足现行证据条件。切换只接受新格式，不设置双读、降级读取或 unknown-fields 豁免。

本文依据[来源模式](../../docs/decisions/source-governance-schema.md)、[来源校验](../../docs/decisions/source-validation-policy.md)、[来源迁移](../../docs/decisions/source-migration-policy.md)、[来源执行](../../docs/decisions/source-execution-boundary.md)、[来源核对取舍](../../docs/decisions/source-evidence-priority.md)、[来源字段采纳](../../docs/decisions/source-field-adoptions.md)与本基线代码。重要外部事实可按本轮用户授权只读联网核对；不存在足够材料时保留阻断，不制造事实。

## 现有字段

本轮通过结构化读取六份 `data/vocab/*.yaml` 盘点实际键，未运行测试。`entities.yaml` 有 62 条记录：31 条来源实体、31 条一般实体；`sources.yaml` 有 31 条用途登记。schema 不能只给来源增加字段后就算完成，一般实体也位于同一受校验文档。

| 范围 | 全部实际字段及出现记录数 |
|---|---|
| 来源实体 | `id`、`label`、`kind`、`tier`、`version`、`checked`、`url`、`subjects`、`basis`、`status`、`added` 各 31；`watch` 20 |
| 一般实体 | `id`、`label`、`kind`、`subjects`、`basis`、`status`、`added` 各 31；`match` 24；`scope` 12；`form` 16；`vendor` 6；`url` 1 |
| 用途登记 | `id`、`entity`、`role`、`checked` 各 31 |
| 主题 | 700 条；`id`、`label`、`basis`、`broader`、`source`、`match`、`status`、`added` 各 700；`scope` 240；`arrays` 248 |
| 主题数组 | 24 条；`id`、`superordinate`、`source` 各 24 |
| 类型与体裁 | 类型 6 条、体裁 5 条；各记录均有 `id`、`label`、`scope`、`match`、`status`、`added` |
| 载体及数组 | 载体 16 条，均有 `id`、`label`、`basis`、`arrays`、`match`、`scope`、`status`、`added`；数组 2 条，均有 `id`、`superordinate`、`source` |

各文档现有顶层 `version` 的 `id`、`date`、`note` 保留，不因 `schema_version: 2` 改写发行版本。实体 `basis.subjects` 共 62 个，其中 14 个为 `self`，其余为紧凑引用字符串或字符串列表。按值分配依据时必须保留原次序与原始内容；一个记录级字符串不能自动解释为对所有 subjects 的逐值证明。

## 状态区分

| 方案 | 含义及影响 | 判断 |
|---|---|---|
| 保留 `status`，增加 `source_status` | `status` 继续表示 candidate、active、deprecated 等项目状态；`source_status` 专指 current、superseded、withdrawn。通用字段、维护指标和 `kb_status` 不改变含义 | 推荐；只修改尚未正式激活的来源 v2 外部状态字段及相关规则 |
| 项目状态改为 `record_status`，外部状态使用 `status` | 所有实体项目状态需要改名；通用导出、指标、筛选、文档和已有阅读习惯同步调整；同一 `status` 在其他词表仍为项目含义 | 可以实现，但迁移范围更大，增加同名字段跨词表歧义 |

此项已随整套方案采纳。实施时，P1、P2 的外部 current 写入 `source_status`，其 `basis.status` 在候选转换中对应 `basis.source_status`；原项目 active 保留。P1–P4 的事实、locator 与日期不变，实施说明必须逐项记录字段名转换，不能重写原采纳决定来假装它原本采用新名字。

[来源数据批次](../../docs/decisions/source-data-batch.md)已经替代原方案的 source_status 必填条件。该字段可省略，缺值只表示“外部状态未核实”，不是 current、不是“不适用”，不新增 unknown；导出与预览必须明示缺口。已填写值仍须发布者依据和精确字段采纳，不删除或覆盖 P1、P2 等已有合格结论。状态不能由项目 active、Recommendation、地址可访问、版本号或日期推导；暂时不可访问只是探测信号。

version 继续必有该键，可为 null，含义只限“未登记可核实版本”，不声称发布者根本没有版本。旧 rolling、月份等未核值保留 history.before，不以抓取月份造版本。省略状态或使用空版本不批准任何关系；具体材料、逐条依据、用途资格和关系采纳继续独立检查。确实依赖外部现行状态的操作在缺值时阻断，无版本 de-facto 不能取得 structure。

## 实体字段

| 现有字段 | 目标表示及保留规则 | 准入与检查 |
|---|---|---|
| `id` | 原值保留 | 按 ID 比较全体身份及引用；禁止复用、删掉或因 label 变化遗漏身份检查 |
| `label` | 语言键及字符串原值保留 | 本次不创造译名，不从外部状态采纳推导名称采纳 |
| `kind` | 原值保留；来源条件继续适用于现有 standard、publication | 不因字段缺口改变对象类别；一般实体不要求来源外部状态 |
| `status` | 原项目状态保留 | 项目状态与未获依据的归属限制仍有效，不自动提升 candidate |
| `subjects` | 现有主题 ID 列表保留 | 逐值指向现有主题；项目归属与来源外部事实分开审阅 |
| `basis` | 外部依据部分改为逐字段、逐值严格引用；非外部部分按下一节分流 | 禁止紧凑字符串、self、none、空列表冒充外部证明 |
| `tier` | 保留 de-jure、de-facto、vendor 等已登记值 | 不借 schema 迁移改档；复核周期仍取已采纳政策 |
| `version` | 必有该键；采纳的可核版本为字符串，未登记可核实版本为 null | 旧未核值保留 history.before；null 不表示发布者无版本，不解除 de-facto 的 structure 版本门禁 |
| `checked` | 历史值进入迁移 history 的 before；仅在可证明核对对象和范围时映射至 `review.checked` | 旧日期不是当前全面复核；字段依据的 `checked` 独立保存，禁止机械回填今天 |
| `url` | 来源转换为 `urls` 中明确角色的地址；一般实体官网也统一转换为 `urls` | 旧字符串本身不足以确定 canonical、landing 或其他角色；一般实体官网须明确其非证据用途，不能伪称 source basis |
| `watch` | 原字符串进入迁移 history；经审阅的观察对象写为明确结构的 `watch` 条目 | 保留原 URL，不凭当前字符串填齐信号、频率或已核状态；无旧 watch 不等于已批准无需观察 |
| `added` | 原日期保留 | 表示项目添加时间，不改成迁移日或外部发布日期 |
| `match` | 转为 `registry`、`item`、`rel`、`basis` | 每条映射单独依据；保留旧 rel 不等于批准其真值 |
| `scope` | 原文字保留 | 不把现行范围文字自动用作来源发布方依据 |
| `form` | 原值保留 | 按现行定义校验，不能看到字符串便误作新分类 |
| `vendor` | 原实体引用保留 | 校验一般实体存在性，不按来源实体过滤 |

现有合同允许但本基线未出现的 `alt`、`hidden`、`creator`、`replaced_by`、`history` 也必须由 schema 显式表达，按现行定义约束，不能用允许任意键替代。`creator` 等一般实体引用与严格来源 basis 的实体范围不同。`fixed_sha256` 已被 `_content_is_mutable()` 使用但未被当前实体 schema 接纳：须明确为有真实固定内容时才允许的 SHA-256 字段，并要求它与版本共同指认所引用内容；没有固定材料不得生成该字段。

新增来源治理字段的处理如下：

| 字段 | 目标合同 |
|---|---|
| `urls` | 条目仅允许 role、url、primary；来源按已采纳七种角色，恰好一个主地址；地址用途和重定向事实分别核实 |
| `source_status` | 可省略表示外部状态未核实；填值只允许三个已采纳枚举，并要求发布者依据与精确字段采纳；替换关系另有依据 |
| `review` | checked、next_due、interval_months、grace_days、obligations 语义分别校验；null 只表示合同已允许的缺值，不作为通过全面复核的证据 |
| `watch` | 显式约束观察 URL、适用信号与周期；采用既有探测政策，不保留当前宽泛 object 作为正式合同 |
| `replaced_by` | 保留既有项目替代语义与来源外部替代之间的区分；来源使用时须证据并检验目标存在及循环，不由 superseded 自动填写 |
| `history` | 仅追加真实迁移事件及已采纳决定；迁移前值与原日期可据 Git 基线填写，不能伪造历史复核事件 |

watch 沿用现有探测器读取的 `locator`、`signals`、`cadence_months`，不另造一套结构：locator 是明确的观察 URL；signals 使用已采纳信号；cadence_months 保存 availability、redirect、content 三类周期并按既有政策校验。schema 对这些键闭合，不再接受任意 object。旧 watch 字符串没有证明的信号和周期不自动填值；只有对应取值已获明确类别规则或具体授权时才可物化。HTTP 方法、响应与观察时间仍放在探测输出，不作为来源事实。

`replaced_by` 若在通用实体中同时承担项目对象替代与外部出版物替代，必须在字段说明中明确依 kind 的适用语义；若真实数据出现二者同时存在，先提出单独字段方案，本次不创建无实例的第二套关系字段。

## 依据处置

推荐增加实现字段 `assertions`，用于显式保存现有项目判断，而不改变严格外部 `basis` 的定义。这是已随整套方案采纳的新字段结构；“项目判断”沿用来源迁移 Q20 已有含义，不创设新的术语或准入等级。

建议 `assertions.subjects` 使用条目列表，每项包含 `values`（既有主题 ID）、`disposition: project_assertion`、`original`（原值）与 `migration`（指向本次审计记录的稳定定位）。只表达原记录确实有这些值及 self 判断，不表达归属已批准；`status` 保留原值。旧 self 覆盖范围只能继承其原来附着的 subjects 集合，不能生成多个看似独立的证据。schema 对上述键、值型和引用范围闭合校验，禁止作为任意备注容器。

| 原依据 | 正式外部 basis | 保留位置与后果 |
|---|---|---|
| `self` | 不生成 | 原判断及 subjects 保存在明确 assertions 中，原值与基线定位另存审计；继续纳入 self 指标及 active 限制 |
| `none` | 不生成 | 记录 no_external_basis 处置；无外部依据不等于语言第 6 级，不自动改变既有语言依据 |
| `cs2023:scope` 等紧凑引用 | 只在材料与定位经核对后生成 entity、locator、必要 checked | 原串保留审计，不把冒号后任意文本当作已核 locator；材料不足则对应字段维持“不核对”并阻断正式迁移 |
| 字符串列表 | 每条引用分别核实，明确支持哪些值 | 保留整个原列表及顺序；不能把记录级列表自动乘以每个 subjects |
| P1–P4 结构化依据 | 逐字复用已采纳事实与日期；按新字段名做明确映射 | 其余 basis 键必须另外处置；不能覆盖、丢弃旧 subjects 判断 |
| 语言 `basis.zh`／`basis.en` | 继续使用已采纳语言依据合同 | 保留 level、references、model、legacy 及采纳记录；不把模型第 5 级转换为来源 basis，不取消语言 legacy 的已采纳语义 |

未核对的外部引用只留在迁移审计和未合格候选中，不作为正式 assertions 掩盖来源事实缺口。整批切换要求这些必要引用获得证据；若材料最终无法取得，必须将“保留原正式关系且不放宽严格证据”与“完成切换”之间的冲突交给人决定。未经决定不能删关系、删实体或清空 basis 使校验通过。

逐值依据推荐在 schema 中显式关联被支持的字段值，避免 `basis.subjects` 列表对多个主题的范围不明。具体可在 subjects 的 basis 条目上增加 `values`，并让其引用严格 `references` 列表；单值字段继续使用严格 BASIS_ITEM 列表。该区别是需要采纳的模型点，采纳后收集器、索引与渲染统一处理，不保留两种 subjects 表示同时可用。

## 用途与引用

旧用途 `id` 与 `entity` 保留一对一关系。`role` 字符串数组整体转换为 `roles` 对象数组：role、status、decision 三项齐备，candidate 转为 proposed discovery；现有 mapping、structure、group 默认只转为 proposed。没有逐项决定不能写 approved 或 retired；不能从实际引用、原 checked 或一条关系的证据推导角色获批。用途旧 checked 保存在迁移 history.before，不作为批准日期或实体 review 日期。

| 引用位置 | 对象身份与角色 | 必需内容 |
|---|---|---|
| 外部 `basis` | 指向来源实体 `entity`；不要求用途角色 | 非空 locator；可变内容有真实 checked；固定版本及内容哈希满足规则时才可省略 checked |
| 实际派生 `source` | `registry` 指向用途登记，structure 已 approved | item、逐行保存的 locator、非空相邻 basis；使用模板也必须保存最终定位 |
| 外部 `match` | `registry` 指向用途登记，mapping 已 approved | item、五种已采纳 rel 之一、逐条相邻 basis；语言相同或名称对应不能替代关系证据 |
| 外部数组分组 | `external_group` 指向用途登记，structure 已 approved | registry、item、locator、basis；只证明分组本身，不证明每个成员的派生 |
| discovery | 发现材料的用途，不取得上述三种资格 | 无实际使用不构成批准；不用它绕过 structure、mapping 或 group |
| 本地结构 | 不写外部来源引用 | `source: self` 的本地建立事实及 form arrays 的本地分析按已采纳 Q16、Q20 隔离保存；原成员、父项和顺序不变 |

本地 `source: self` 推荐在新的 `assertions.source` 中保留 project_assertion 与审计定位，正式 source 字段仅表达外部派生；这属于模型点，不能机械删除 self 后宣称无损。主题数组的外部 source 转为 external_group（沿用现有 structure 资格；由映射派生概念组的 group 角色不与它混用），载体数组依已有 Q16 保存本地分析与原 superordinate／members，不能把字符串 RFC 一律转为外部分组。RFC 层次依据按 Q17 每层分别核对；主派生 CS2023 和补充来源、映射保持 Q14 区分。

严格引用收集必须先识别受约束字段位置，再验证形状。基线 `_walk_reference_uses()` 要求必需键齐全才收集，缺键对象可能被漏掉；多余键虽会被收集，但基线字段校验没有拒绝它们。本工作区已针对这些结构化引用缺陷完成定向修复，迁移后必须报错，不能因为没有被识别而消失。语言依据 references 的 source 是其既有独立合同，由 label_basis 校验，不与旧 source 字符串混同。

## 应用表示

[Obsidian target](../../docs/design/targets/obsidian.md)须先明确每字段的 location、type、reference form、loss，再修改导出；不把嵌套对象直接塞入原字符串属性，也不以 `str(dict)` 展示。实体与来源笔记仍沿用原 ID 路径，不修改正式内容 UUID。

| 元数据 | Obsidian 表示 |
|---|---|
| 项目 status、kind、tier、added、version | 保持对应属性的含义；version: null 在正文显示“未登记可核实版本”，不改成抓取日期或“发布者无版本” |
| 外部 source_status | `kb_source_status` 只表示已填实际值；缺省时正文明确“外部状态未核实”，不展示 current、不适用或 unknown，不覆盖 kb_status |
| subjects、vendor、creator、replaced_by | 按现有对象类型生成 Wikilinks；涉及来源外部替换时正文说明适用含义 |
| urls | 主地址投影至 `kb_url` 供访问；正文完整地址表保存角色、地址、primary，不能丢弃 DOI、镜像等非主地址 |
| review | 日期、周期作为独立可筛选属性；正文列全 review 字段及义务链接。`kb_checked` 若继续使用，只表示 review.checked，历史日期显示于 history |
| watch | 正文观察对象表完整显示地址、信号、周期；如需可筛选地址列表，在 target 中明确是投影，不能冒充完整 watch |
| roles | `kb_roles` 可列角色名以延续查找，但正文必须逐角色显示 proposed／approved／retired 和决定；另提供获准角色列表供实际资格筛选，不能把 kb_roles 当批准结果 |
| basis 与 assertions | 分表显示“外部依据”和“项目判断”；逐值显示目标、来源实体、locator、checked 或 project_assertion；未核对候选不作为正式参考导出 |
| source、match、external_group | 保存用途链接、外部 item、关系或定位、完整相邻依据；不能只输出一个 registry 链接而丢 item 和证明 |
| history | 按日期显示真实动作、字段、决定、前后值与依据；旧 checked 可以在这里查回 |

`apps/vocab-preview/` 同步读取新结构，既显示项目状态又显示外部状态，完整展示来源角色资格及依据分流；只读属性不变。正式 vault `~/Documents/kb-vault/` 不属于本次设计写集。实施验收先导出至 `build/` 临时目录；正式刷新属于独立实际操作，须遵守用户批准范围，不能以本方案批准代替。

## 工程顺序

整批工作按下面依赖顺序推进，不将每一个字段变成重复申请开始的小任务。中途提交可保存工作，但不得把未完成代码或候选混入 `master`。

| 顺序 | 具体文件 | 实施内容与交付 |
|---|---|---|
| 模型定稿 | `docs/design/model/entities.md`、`docs/design/model/sources-registry.md`、`docs/design/model/topics.md`、`docs/design/governance/maintenance.md`、新的已采纳决定 | 固定状态命名、assertions、逐值 subjects 依据、watch 结构、一般实体适用性及本地 source 表示；旧决定按职责注明新决定取代范围，不改冻结历史 |
| 当前库存 | 本方案、`work/reviews/` 当前批次材料、`data/inputs/topics/` | 基于当前全量字段及引用形成字段级 old/new/evidence/未核范围/影响路径；与冻结 source-v1 账本按身份关联，新增 Obsidian 实体和变化后的语言依据单列，不覆盖旧账本 |
| 证据与采纳 | `docs/decisions/source-field-adoptions.md` 所引用 P1–P4、后续字段采纳决定 | 复用已采纳值；一次覆盖剩余必需字段、47 个既有用途角色及实际引用。状态缺省与版本 null 按已采纳合同记录，其他必需证据缺口继续阻断；角色批准与关系批准分开 |
| 核心合同 | `packages/kb-core/src/kb_core/source_model.py`、`schemas/source-entities.schema.json`、`schemas/source-uses.schema.json`、`schemas/source-reference-index.schema.json` 及实际受影响 schema | 在 build_schema_documents 源头增加全部通用字段与正式新表示，再确定性生成 schema；封闭对象，不只手改 JSON。增加地址主项唯一性、跨引用、角色决定作用域、状态依据、逐值依据及稳定身份语义校验 |
| 严格入口 | `packages/kb-core/src/kb_core/check_sources.py`、`source_model.py`、`cli.py` | 移除正式路径 allow_legacy；正式读取缺失／错误 schema 版本即失败；按字段位置发现非法形状。不存在义务文件时依据未激活边界明确处理，不创建虚假义务来满足统一循环 |
| 生成与检查 | `packages/kb-core/src/kb_core/build_topics.py`、`check_topics.py`、`label_basis.py`、`data/inputs/topics/`、六份 `data/vocab/` | 将 source、match、external_group、assertions 写入确定性生成输入和序列化；保留语言采纳合同；check_topics 改用严格引用语义和新归属结构，保留项目状态、自定比例、subjects 指标及复核到期行为。topics 只由生成器重建 |
| 索引与维护 | `build_source_index.py`、`plan_source_migration.py`、`prepare_source_evidence.py`、`apply_source_migration.py`、`probe_sources.py`、`governance/term_maintenance.py` | 正式索引去掉 legacy 读取，覆盖严格依据、用途、语言引用、外部分组、决定和替代；项目判断不产生外部引用边。旧迁移器仅可读取冻结材料作审计，不作为正式兼容层。替换依赖新状态字段及日期位置；不启用 live 探测或术语切换，不扩展补偿框架 |
| 应用适配 | `docs/design/targets/obsidian.md`、`docs/design/targets/vocab-preview.md`、`apps/obsidian/src/kb_obsidian/exporter.py`、`reference_export.py`、`refresh.py`、`managed.py`、`validation.py`、`apps/vocab-preview/src/kb_vocab_preview/server.py`、`template.html` | 更新根字段白名单、记录键、类型检查、跨引用、属性与正文表格；manifest 的覆盖合同随实际文件集更新；刷新仍只管理 kb/ 与 app/manifest.json，不触及内容和配置 |
| 整批候选 | 独立候选分支及其全部新格式数据 | 接入同一严格代码与所有新数据，不保留 P1–P4 混合状态作为可发布形状；旧格式受跟踪快照由 Git 保存 |
| 验收与切换 | 现有核心和应用行为测试、临时输出、差异报告 | 下节门禁完成，明确全量未核范围为零或经独立决定合法处置；由人批准正式切换。未通过不合并，不以计划完成替代实施完成 |

校验器还须纠正现有不足：`validate_repository()` 目前按 label 寻找历史记录，会漏掉标签与 ID 同时变化；应按旧 ID 全集核对存在性、关系和允许的决定，不把名称作为身份。目前 P1–P4 的采纳决定为正文记录，而 `_load_accepted_decision_ids()` 只读取带 front matter 的 source 决定。新实施必须给实际被机器引用的决定补齐经批准的稳定 ID、schema 与结构化作用范围，或在新决定中明确承接原正文采纳；禁止把未被读取的正文当作角色批准，也不为过检查编造一个 accepted ID。角色 decision 当前只验证“ID 属于 accepted”，还需确认决定确实批准了该实体的该角色与对应状态。basis.entity 存在并有 checked 不足以证明实体外部状态值由发布方支持，应对状态、版本、替换字段分别检查所需依据与采纳范围。

## 验收依据

以下为实施验收门禁，列出命令不表示已经执行或通过；实际结果以本轮验收记录为准。每项先说明要发现的失败、后果和独有证据；不为字段存在、常量回显或包装函数另写测试。

| 失败与后果 | 独有证据与实施门禁 |
|---|---|
| 项目 active 被替换成 current，旧字段或实体丢失 | 迁移前后按 ID 和字段合同逐值比对；所有旧字段均有新位置或审计位置，未批准状态不变；人工审阅语义差异 |
| 缺状态被显示为 current，或空版本被当作固定版本 | 省略与 null 的合同检查及人读表示；已填状态的发布者依据与精确采纳、状态依赖操作及 de-facto structure 门禁分别检查 |
| 未核紧凑引用或 self 被当作外部 basis | 严格引用行为测试覆盖 self、缺定位、缺 checked、错误字段、多余字段和无批准角色；所有来源引用路径均被发现，语言合同按其独立规则处理 |
| 角色决定串用、失效或只批准一条关系却被用于全角色 | accepted 决定内容与角色对象／状态／范围的行为检查；证据采纳矩阵逐行对照 |
| 生成器再次输出旧 source/match 或改变稳定身份 | `uv run kb-core build-topics` 后执行 `uv run kb-core check-topics`，在相同环境重建一次比较字节；与迁移前身份及关系完整性对照 |
| 一般实体被来源 schema 拒绝，或者正式索引漏引用 | 在完整 62 实体和六份词表的新快照上执行严格 `check-sources --root ... --previous ...`；索引生成消费同一遍历器，比较正式引用集合与预期引用身份，禁止 legacy 计入成功 |
| Obsidian 导出静默丢字段、改变内容路径或刷新越界 | 临时完整参考导出的字段表示比对、链接验证和 manifest 写集；阅读来源／一般实体／项目判断／多地址样本；必要的刷新行为测试证明保留 content 与配置 |
| 历史账本被重新解释成当前批准，Git 恢复不完整 | 已采纳决定与候选写集对应；历史审计无改写；提交前后受跟踪差异明确且正式 vault 不在其中 |

按风险阶段边界运行一次相应全量核心与应用回归，具体命令使用仓库当前测试入口；不在每个字段之后重复全量回归。导出机械成功与 Obsidian 可读性分开；若需实际应用验收优先 Obsidian CLI，不为查看几张表使用 Computer Use。不得把本方案中的命令描述报告为已经通过。

## 人的决定

状态字段命名、assertions、subjects 逐值依据、本地隔离与 watch 合同已随整套方案采纳；[来源数据批次](../../docs/decisions/source-data-batch.md)进一步采纳外部状态可省略与版本必有但可 null 的条件，替代原方案对应的强制字段要求。该决定不是所有事实或关系均已核实的声明。

具体字段、归属、用途角色和关系仅在决定实际列明的对象、值与范围内有效。已有合格状态依据不能因字段变为可省略而删除；未列关系仍需逐条材料、定位与采纳。缺状态不再成为全源一律不能引用的理由，但依赖外部现行状态的操作保持阻断，无版本 de-facto 不得取得 structure。

已获批准范围内的 schema、生成、校验、索引、表示与必要验证继续整批实施；正式切换仍须完整新数据与消费者验收。计划及模型采纳不替代执行结果，不把本批字段采纳外推为正式发版、术语激活或 vault 刷新。

## 切换边界

正式新数据、严格读取、生成输入与实现、核心检查、索引、维护指标及应用导出在同一可用 Git 快照中完成。各阶段可以在隔离分支保存提交，但不得将 schema 先合并而正式数据和消费者留旧，也不得先发布部分候选制造混合状态。仅设计完成、schema 能生成、四项字段通过或临时导出可读，均不构成正式切换完成。

恢复只使用明确提交范围的 `git revert`。不实现 payload／handoff 状态机、补偿回滚或长期兼容分支；旧迁移冻结材料作为历史审计保留。revert 前检查未知用户修改，受跟踪模型与数据可以由 Git 恢复，正式 vault 和 Git 忽略输出不在承诺范围。迁移切换不自动发版、不激活术语、不启用正式消费者，也不触发正式 vault 刷新。
