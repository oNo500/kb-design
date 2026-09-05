# 设计文档索引

`design/` 中的现行设计规定本库当前使用的规则；已采纳决定保存规则形成与阶段边界，未激活基础只提供机器能力，迁移账本只保存审计，项目草案全部未生效。理论在 `concepts/`，文献笔记在 `sources/`。项目执行计划和 Superpowers 报告是过程记录，不属于项目设计，也不进入本索引的效力层次。

## 效力层次

| 层次 | 当前效力 | 不能替代 |
|---|---|---|
| 现行设计与正式数据 | 规定当前规则、编辑权和数据形状 | 不能被草案、迁移推荐值或测试夹具覆盖 |
| `Application Profile` | 规定 target 的功能范围、模型引用、字段约束、使用和具体表示 | 不能修改应用无关模型，也不能成为正式数据编辑源、消费者运行记录或激活证据 |
| 导出 artifact contract | 规定已选表示的输入快照、字节物化、文件集合、清单、校验和发布 | 不能修改 `Application Profile` 的语义选择，也不能扩大确定性或完整性证据 |
| 已采纳决定 | 约束已批准的规则、机器契约和阶段范围 | 不自动填写来源事实，不使草案或正式数据切换生效 |
| 未激活基础 | 提供 schema、校验、索引、探测、生成、诊断和维护接口 | 不构成正式数据、义务、委托、消费者、切换或发版 |
| 迁移审计 | 保存冻结身份、旧位置、分类、去向和阻断 | 不批准新值，不回写正式数据，不取得术语准入或删除权限 |
| 项目草案 | 保存拟议规则、问题边界和生效条件 | 阅读、引用、推荐或部分实现不等于规则生效 |

当前阶段以[当前阶段](decisions/current-stage-scope.md)为基础边界，以[项目路线](../docs/superpowers/plans/2026-08-31-project-roadmap.md)记录完成状态。来源与术语基础、现行设计同步、首轮维护、草案复核和待定设计均已完成各自当前范围；Obsidian 完整应用 target、词表参考导出和同仓工具实现已经建立，并已初始化本地持久 vault。实际用户内容、正式消费者、查询日志、回流、严格来源切换、术语正式激活、草案生效和发版都没有发生。

## 现行设计

- [方法登记](principles.md)：登记本库采用的方法、概念依据和导出的规则。
  - [Application Profile](../concepts/application-profile.md)：解释功能范围、模型、字段约束、使用与具体表示的职责分层；项目保留 English designation。
  - [Reproducible Builds](../concepts/reproducible-builds.md)：区分确定性、独立重建、manifest、provenance、原子可见性与 durability 的证据。
  - [写作规则](writing.md)：规定全库写作规则；`AGENTS.md` 是其会话摘要。
  - [主题词表设计](topics.md)：规定正式主题词表的范围、记录、关系、生命周期、生成路径和校验。
    - [层级结构](hierarchy.md)：规定树的分层、结构复制、数组和结构来源。
    - [来源名称规范表](sources-registry.md)：规定现行来源登记及未激活共享接口的职责边界。
  - [命名实体词表设计](entities.md)：规定产品、语言、组织、标准和文献等个体的记录方式。
  - [内容模型](content-model.md)：规定内容单元字段、受控值、标识符、生命周期和应用映射接口。
    - [Obsidian 映射](targets/obsidian.md)：按 `Application Profile` 规定首个完整应用 target，并分开现有词表参考导出的 artifact contract。
    - [词表版本](versioning.md)：规定版本块、发版时机和变更记录。
  - [治理](governance.md)：规定对象效力、政策、决策权、变更控制、验收、验证投入和审计。
    - [维护](maintenance.md)：规定现行对象、指标、阈值、触发、动作、审计追踪和复审。

## 已采纳决定

`design/decisions/` 只追加不修改。以下决定共同约束现行设计与当前阶段。

- [树按学科而非分面的决定](decisions/tree-by-discipline.md)
- [原样复制与本地分析分层的决定](decisions/borrow-and-analyze.md)
- [设计与应用分离](decisions/form-independence.md)
- [应用约束与表示分层](decisions/application-profile-boundary.md)：固定 `Application Profile`、target binding、导出 artifact contract、消费者和编辑效力边界；不修改前一决定。
- [Obsidian 工具归属](decisions/obsidian-tool-location.md)：工具迁入 `tools/obsidian/`，默认使用所在设计仓库的干净 Git 快照，保留旧 vault 刷新兼容与独立实例。
- [内容单元标识符](decisions/content-unit-identifiers.md)：规定新内容单元使用无前缀、小写 UUIDv4，并把稳定身份与元数据检索分开。
- [决策权的首批边界](decisions/decision-rights-defaults.md)
- [项目约定入口](decisions/project-instructions-entry.md)
- [来源模式](decisions/source-governance-schema.md)：批准来源机器结构与迁移规则，不批准具体来源事实。
- [来源校验](decisions/source-validation-policy.md)：固定来源离线校验政策，真实状态、角色和逐值关系继续未决。
- [来源探测](decisions/source-probe-policy.md)：固定只读信号与频率，观察不得回写正式数据。
- [来源迁移](decisions/source-migration-policy.md)：固定迁移分类与顺序，不批准账本中的推荐值。
- [证据阶段](decisions/evidence-stage-boundary.md)：把高成本证据限制在会改变正式结果的范围。
- [当前阶段](decisions/current-stage-scope.md)：完成来源与术语基础和现行设计同步，把正式激活整体后置。
- [验证投入](decisions/verification-effort.md)：按目标失败、后果和独有证据配置审查与测试。
- [译名依据扩展](decisions/industry-translation-basis.md)：在不译之前纳入有证据的业界用法，区分名称变更与概念变更；不批量采纳既有标签。
- [译名检索来源](decisions/translation-reference-resources.md)：优先成批查固定术语库，按条目判断证据等级，复用查询结果并区分实际命中与采纳建议。
- [模型知识译名](decisions/model-knowledge-translation.md)：已有离线资料不足时，允许按新增译名第 5 级使用模型既有行业知识；与已核实外部来源分开，不改变概念身份。
- [模型译名标记](decisions/model-translation-marker.md)：保留早期字符串标记决定，其表示与输入位置已由后续决定替代。
- [语言依据结构](decisions/structured-label-basis.md)：采纳外部、模型、未采用与历史依据的结构化合同及当前中文补全批次；生成、校验与人读导出共同保留依据性质。

## 正式词表

当前正式数据只有下列六份词表。

| 词表 | 文件 | 职责 | 设计 |
|---|---|---|---|
| 主题词表 | `vocab/topics.yaml` | 概念、标签、层级、相关关系和外部映射 | [主题词表设计](topics.md)、[层级结构](hierarchy.md) |
| 命名实体词表 | `vocab/entities.yaml` | 产品、语言、组织、标准和文献等个体 | [命名实体词表设计](entities.md) |
| 来源名称规范表 | `vocab/sources.yaml` | 外部知识体系与词表的现行登记 | [来源名称规范表](sources-registry.md) |
| 文档类型词表 | `vocab/types.yaml` | 内容单元的文档类型 | [内容模型](content-model.md) |
| 体裁词表 | `vocab/genres.yaml` | 内容单元的作者立场 | [内容模型](content-model.md) |
| 载体词表 | `vocab/forms.yaml` | 内容单元的呈现形式与教学活动 | [内容模型](content-model.md) |

版本和维护动作见 [`vocab/CHANGELOG.md`](../vocab/CHANGELOG.md)。入口不复制会随正式文件变化的记录数量。

## 主题生成

`vocab/topics.yaml` 既是正式主题词表，也是 `scripts/build-topics.py` 的确定性输出；人工不直接编辑。当前编辑源是生成脚本及其实际读取的下列输入。

- `vocab/build/cs2023-kus.json`
- `vocab/build/cs2023-zh.json`
- `vocab/build/extra-arrays.json`
- `vocab/build/gbt-13745.json`
- `vocab/build/gbt_en.py`
- `vocab/build/label-decisions.json`
- `vocab/build/label-adoptions.json`
- `vocab/sources.yaml`（语言依据的来源登记校验）
- `vocab/build/scope-zh.json`
- `scripts/build-topics.py` 中的顶层、图书馆情报与文献学分支、多层级规则、版本和日期

`vocab/build/label-lookup.json` 是查询清单，`vocab/build/label-review.md` 是人工复核材料，`__pycache__` 是运行生成物；生成器不读取它们。结构化采纳由独立的 `label-adoptions.json` 保存，旧 `label-decisions.json` 的 Wikidata 采纳与否决保留。来源登记只供新增依据校验，不改变树结构输入。修改主题数据时先改真实输入，再重建正式输出并运行主题校验。应用只读取正式输出，不反向编辑。

## 术语编辑

`concepts/glossary.md` 仍是全库 designation 与中英对照的现行编辑源。术语三层 schema、状态校验、确定性生成器、正文诊断和维护接口已经实现，但仓库当前没有正式 `vocab/terms.yaml`，编辑权没有转移。

`vocab/glossary-layout.yaml` 只是未来术语生成基础设施的布局配置，不是现行词表，也不是当前术语表编辑源。正文诊断输出只提供人工复核线索，不形成术语、概念、违规或阻断结论。

## 应用映射

[Obsidian 映射](targets/obsidian.md)是当前唯一项目原生 target 文件，也是首个完整应用 target 的设计。它引用 [Application Profile](../concepts/application-profile.md)和 [Reproducible Builds](../concepts/reproducible-builds.md)两种已登记方法，并受[应用约束与表示分层](decisions/application-profile-boundary.md)约束。应用无关模型、`Application Profile` 的语义选择和导出 artifact contract 分开；field／property／path binding 不是 `metadata crosswalk`，也不改变词表层 `crosswalk`。

完整设计规定内容捕获、外部资料、内容单元、正式受控引用、用户索引、导航和维护线索的应用边界；它不是内容消费者运行记录。实现分为 `kb-design` 中的 `scripts/export_obsidian.py` 和 `tools/obsidian/` 中的 `kb-obsidian` 工具：前者从现行正式词表生成单向参考区，后者从干净的设计提交初始化新 vault、建立 `draft` 内容、校验内容与正式引用并重算派生报告。实施验收已经建立本地持久 vault，证明完整布局和应用命令能够作用于实际目录。

持久 vault 当前没有实际用户内容，内容消费者没有正式激活，也没有查询日志或回流接口；空库报告不能充当内容使用观察。内容标识符使用无前缀、小写 UUIDv4，title、派生 alias、正文和其他元数据承担人的检索。Obsidian 与 Base 可以编辑生成文件，但修改不回流、不取得项目效力。普通 `.json` 不是 Obsidian 内容格式，项目 manifest 不是 BagIt；同环境双跑只证明确定性，目录项替换只证明成功时的原子可见性，项目不宣称 JCS、BagIt、reproducible build 或 durability。TBX 仍是没有真实接收方的未生效草案。

## 未激活基础

来源基础包括 schema、共享模型、离线校验、反向索引、固定夹具探测、迁移预演和复核义务接口；术语基础包括候选 schema、状态转换校验、确定性生成、正文诊断、维护索引和复核义务接口。

这些能力没有接管正式数据。仓库没有正式来源 v2 数据、正式来源或术语义务、正式索引、正式术语数据、委托、消费者或切换状态；固定夹具也不证明真实来源状态。基础能力、测试夹具和 ignored 输出都不能使治理草案生效或形成发版。

## 迁移审计

- `vocab/migrations/source-v1/` 下的六份账本保存来源迁移审计。账本中的推荐值、`proposed`、处置和阻断不修改正式来源数据。
- `vocab/migrations/term-v1/terms.tsv` 保存冻结审查身份和消费者去向。`audit-only`、`retain-owner`、`retain-pending-l3`、旧 `keep`、`defer` 和 `remove` 都不构成 designation 准入、术语候选、删除许可或正式状态。

迁移账本只作审计，不是正式词表、义务、委托、消费者、决定或切换状态。

## 项目草案

以下十份草案全部未生效。只有 `design/drafts/` 中的项目文件在此登记；研究报告、审查报告、决定包和其他 Superpowers 过程文件不因此成为项目设计。

- [来源治理](drafts/source-governance.md)：提出来源身份、用途、引用、复核和失效处理规则；部分前置机器契约已经完成。
- [术语治理](drafts/terminology-governance.md)：提出术语概念、多语形式、状态、委托和生成边界；基础接口完成未改变 glossary 编辑权。
- [TBX 导出](drafts/tbx-export.md)：记录术语交换的后置触发条件；当前无接收方，不选择方言或实施导出。
- [划分特征的自定治理](drafts/division-characteristics.md)：提出划分特征的登记与复核；该草案的自定例外尚未开放，已开放的模型知识译名不扩及划分特征。
- [分面字段草案](drafts/facet-field.md)：记录分面研究、模型职责和生效条件；现行主题记录没有该字段。
- [概念组草案](drafts/concept-groups.md)：提出手工概念组的登记和规则；现行数据没有手工概念组。
- [生活领域范围](drafts/life-scope.md)：分别保存健康相关内容、个人或家庭财务、旅行或旅游的范围问题；推荐保持现状，开放决定未改变正式范围。
- [实体类别职责](drafts/entity-categories.md)：提出实体类别与相邻字段的职责方案；推荐方案和身份疑虑均未改变正式实体数据。
- [模型对象分层](drafts/large-language-models.md)：提出四层记录及 ML、NLP 双上位方向；开放决定不批准概念、名称、关系或记录。
- [传播学科范围](drafts/communication-scope.md)：提出完整学科位于 `communication-studies` 下的方向；中文 designation 仍阻断实施。

阅读或引用草案、实现部分 schema 或工具，都不等于规则生效。草案只有满足各自条件并取得人工决定后，才可能并入现行设计。

## 阅读顺序

| 顺序 | 文章 | 读完知道 |
|---|---|---|
| 1 | [当前阶段](decisions/current-stage-scope.md) | 哪些基础已经完成，哪些正式激活仍后置 |
| 2 | [方法登记](principles.md) | 本库采用哪些方法，各自依据是什么 |
| 3 | [主题词表设计](topics.md) | 正式主题词表和当前生成路径 |
| 4 | [层级结构](hierarchy.md) | 树怎样分层、复制和组织数组，以及哪些问题仍未生效 |
| 5 | [来源名称规范表](sources-registry.md) | 现行来源登记与未激活共享接口的边界 |
| 6 | [命名实体词表设计](entities.md) | 个体怎样记录、分档和引用 |
| 7 | [治理](governance.md) | 对象效力、决策权、变更控制和验证投入 |
| 8 | [维护](maintenance.md) | 指标、阈值、动作、复核和审计追踪 |
| 9 | [写作规则](writing.md) | 写任何文件前要遵守的规则 |
| 10 | [内容模型](content-model.md) | 内容单元字段、稳定身份和应用映射接口 |
| 11 | [Obsidian 映射](targets/obsidian.md) | 首个完整应用 target 的语义表示、应用实现，以及尚未激活的运行边界 |
| 12 | [词表版本](versioning.md) | 何时发版、怎样记录变化 |
| — | [决定记录](decisions/) | 已采纳决定及其后果 |
| — | [项目草案](drafts/) | 十份未生效提案、开放问题及其触发条件 |
