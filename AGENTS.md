# kb-design 项目约定

本文是 [docs/design/governance/writing.md](docs/design/governance/writing.md)、[docs/design/governance/governance.md](docs/design/governance/governance.md)、[docs/design/governance/maintenance.md](docs/design/governance/maintenance.md) 和[主题生成路径](docs/design/model/topics.md#生成路径)的会话摘要，每次会话加载；冲突时以各正文职责范围内的规则为准。

## 标题

适用于本仓库所有 Markdown 文件，硬规则。

- 标题单看能知道这节讲什么
- 2–8 字的名词短语，不用冒号，不写成句子，不用动词短语
- 主语由文章标题隐含，小节标题只说“什么的什么”，不重复主语
- 不加序号
- 指向对象，不写参数和实现细节：数量、字段名、文件名会变，标题不跟着变
- 文章标题格式：`# 中文名 (English Name)`；设计文档和笔记可只写中文名

好：`词表的五种结构`、`词与词的三种关系`、`概念记录的字段`
差：`形式`（没主语）、`一图看懂`（动词短语，不知讲什么）、`四层树结构`（把参数写进标题）、`分面字段 kind`（把字段名写进标题）、`受控词表有哪几种结构形态:从平铺列表到叙词表`（太长，有冒号）

## 整篇重写

- 改文章不打补丁。补丁让缺口和临时术语带着文章活下去；改动涉及一节以上时，整节或整篇按目的重写，重写时核对旧版逐项去向
- 重写是发现空缺的手段：补丁掩盖的缺口会在重写时暴露，暴露了就补，直到文章自洽

## 术语

- **当前阶段零自定**：通常禁止 AI 主动形成或选定无准入依据的 designation；现已由人开放[模型知识译名](docs/decisions/model-knowledge-translation.md)例外，仅允许为既有概念按译名第 5 级使用模型既有知识中的行业表达，并登记为模型判断、外部用法未核实。该例外不授权新建概念、类别或划分特征
- 拟作项目术语而未登记的 designation 不得进入定稿。普通叙述、来源转录、文件路径、代码和值中的任意字符串不因出现而自动成为术语；候选、`defer`、草案、占位和示例不能替代形式依据与概念对应依据，也不能取得试用资格
- 原翻译批次的离线范围保持；本次冻结登记的必要只读原文核对按[术语依据范围](docs/decisions/term-evidence-scope.md)开放，不新增持久下载、OCR 或资料平台。译名第 4 级保留多个独立来源与概念对应要求；资料不足时可按已授权第 5 级登记模型判断。已有合格前级依据不被模型判断覆盖，实质含义冲突未解决时保留原名。名称、身份和状态的实际变更分别依具体采纳，不因生成或模式扩展自动发生
- `basis.zh`／`basis.en` 使用[语言依据](docs/design/model/topics.md#语言依据)：外部等级与 `references`、第 5 级 `model`、第 6 级未采用原因、未重新分级的 `legacy` 分开。旧 `none` 不自动变第 6 级，旧 `self` 不自动变模型判断。模型输出关联 `data/inputs/topics/label-adoptions.json` 的采纳记录并显示“模型知识 · 第 5 级，外部用法未核实”；[本次批次授权](docs/decisions/structured-label-basis.md#批次授权)只覆盖原有缺失中文及语言依据结构迁移，不改变身份、关系或状态
- 正式术语按[具体采纳](docs/decisions/term-data-values.md)及[实施结构](docs/decisions/term-complete-structure.md)管理。项目依据目前只批准内容单元、断言、阈值的概念和定义，以及 assertion、threshold 两个既有英文形式；须有有效 L3 完整记录、精确项目 scope 和历史。六条 de-facto 定义使用依[限定许可](docs/decisions/term-limited-definition-source-use.md)逐对象、来源版本和具体值核对，不改变档级或放宽其他对象。历史退出名不作为当前准用形式，同名的其他合法对象不被全局删除

## 标点与间距

- 中文句子用全角标点；引号用“ ”，不用 `「」`（GB/T 15834 §4.8）
- 汉字与西文字母、数字之间加一个半角空格；与全角标点之间不加（clreq §6.3.3）

## 决策权

按 [docs/design/governance/governance.md](docs/design/governance/governance.md) 的三级：不改规则且可逆的直接做；改规则、改结构、改文件布局、术语准入、归属判断、候选删除的先提案；范围、零自定例外的开放、决定的采纳与推翻、删除非候选对象、发版、草案生效、来源改档只有人能定。提案先给小节清单或改动说明，人回复后再动文件。提交说明标注级别 `[L1]` `[L2]` `[L3]`。

## 审查与测试

- 每项审查或测试先说明要发现的失败、失败后果和独有证据；没有可信高风险失败，或已由更强门禁覆盖时，不设计、不执行
- 保留语义效力、决策权、稳定身份、迁移完整性、生成确定性、共享接口、删除、正式切换和回滚检查
- 文件存在、常量回显、重复计数、包装函数透传、实现细节和已由 schema、哈希、写集或端到端检查覆盖的事实，不单独测试或独立复审
- TDD 只用于保留的行为测试；文档、静态配置、确定性生成物和纯机械迁移使用直接校验，不为 RED／GREEN 形式另造测试
- 全量回归只在风险阶段边界运行；机械事实由命令证明，不交给第二代理重复确认

## 阶段边界

- 迁移账本只作审计，候选和诊断输出只供人工复核，schema、索引、探测、生成和维护能力只证明机械能力；它们都不等于正式数据、草案生效、正式切换或发版
- 来源与术语基础的原范围见[当前阶段](docs/decisions/current-stage-scope.md)，后续以具体已采纳决定为准。六份词表已按[来源收尾](docs/decisions/source-completion.md)完成来源 v2 迁移；17 条未核映射继续保留审查，不重开或提升为有效映射。完整术语数据、限定准入、生成与维护已实施，[术语发布](docs/decisions/term-complete-publication.md)在临时验收通过后启用结构化术语唯一编辑源及首批术语参考消费。正式义务、持久正式索引、委托、内容消费者、查询日志及回流仍未启用
- Obsidian 是应用层，也是首个完整应用 target；`apps/obsidian/` 中的 `kb-obsidian` 工具读取所在设计仓库的干净 Git 快照，保留显式 `--design-root`，不使用提交白名单，见[工具归属](docs/decisions/obsidian-tool-location.md)。默认持久 vault 位于 Git 忽略的 `output/obsidian/`，也支持显式外部 vault；应用实现和输出目录存在仍不等于消费者激活
- `kb-obsidian` 已实现新 vault 初始化、显式词表及术语参考刷新、内容建立、内容校验和派生报告；刷新只更新 `kb/` 与 `app/manifest.json`，保留用户内容与配置，见[词表参考刷新](docs/decisions/obsidian-reference-refresh.md)。本轮只在临时 vault 完成完整数据验收，未写入外部正式库；过去空库或单条 draft 的观察不能作为当前内容计数，实际内容消费者、查询日志与回流仍未激活
- 新内容单元使用无前缀、小写 UUIDv4，UUID 文件名承担稳定路径，title 与派生 alias 等元数据承担人的检索；建立器只创建通过当前约束校验的 `draft`，不批准内容状态或正式分类
- 来源 v2 与术语参考的正式数据和严格读取已经实施，不等于内容消费者启用、外部 vault 同步或发版。archival 在来源用途记录中只可保留 proposed discovery，不具备 approved 用途；作为具体定义或语言材料的 basis 按独立合同核对。TBX 继续后置为无真实接收方的未生效草案

## 应用分层

- [Application Profile](docs/concepts/application-profile.md)与 [Reproducible Builds](docs/concepts/reproducible-builds.md)是已登记方法；项目保留 English `Application Profile`，不采用未经核实的中文 designation
- 应用无关模型、`Application Profile` 的 target location／type／reference form／loss 语义选择、导出 artifact contract 的 byte serialization／file set／manifest／validation／publication 分开；后两者不得反向修改前者
- field／property／path binding 不是 `metadata crosswalk`，不改变词表层 `crosswalk`；新 target 必须引用概念文、[方法登记](docs/design/governance/principles.md)和适用的已采纳决定
- 生成文件与 Base 可以在 Obsidian 中编辑，但修改不回流、不取得项目效力；完整应用设计、target 文件或参考导出存在都不等于内容消费者启用
- 当前只宣称同环境确定性、项目 manifest 完整性与成功目录替换的 atomic visibility；不宣称 DCAP、DCTAP、JCS、BagIt、reproducible build conformance 或 durability
- 上述边界由[应用约束与表示分层](docs/decisions/application-profile-boundary.md)固定；旧[设计与应用分离](docs/decisions/form-independence.md)决定继续有效且不修改

## 工程路径

- 根目录是 uv workspace，使用统一 `uv.lock`；`.python-version` 固定当前开发环境为 Python 3.13.5，成员包最低支持 Python 3.11
- `apps/obsidian/` 通过 workspace 依赖使用 `packages/kb-core/`，核心包不依赖具体应用；核心入口是 `uv run kb-core <命令>`，应用入口是 `uv run kb-obsidian <命令>`
- `apps/vocab-preview/` 提供 `uv run kb-vocab-preview`，只读展示工作区六份词表并自动更新；不要求提交，不写回词表，不代表数据已批准，见[预览归属](docs/decisions/vocab-preview-location.md)
- `output/` 保存 Git 忽略的持久应用数据，不属于构建清理对象；`build/` 保存 Git 忽略的可清理临时产物
- 迁移前决定与 `work/archive/` 的旧路径按原 Git 基线解释，不重写历史正文；当前位置见[仓库布局](docs/decisions/monorepo-layout.md)

## 编辑路径

- `data/vocab/topics.yaml` 是正式主题词表和确定性生成物，不直接编辑；修改 `data/inputs/topics/` 或核心生成实现，以 `uv run kb-core build-topics` 重建，再运行 `uv run kb-core check-topics`
- `data/vocab/terms.yaml` 是结构化术语概念、定义与现行名称的唯一编辑源；`docs/glossary.md` 是只读生成页。布局、说明、符号与已批准历史名称展示在 `data/inputs/terminology/glossary-layout.yaml` 维护；模型标签仍属于主题生成输入、`data/vocab/forms.yaml` 与既有语言采纳记录。使用 `kb-core term-data` 校验和定位引用、`build-terms` 生成与核对；正文诊断不产生准入决定

## 其他约定

- `docs/concepts/` 下的文章另按 [docs/concepts/CONVENTIONS.md](docs/concepts/CONVENTIONS.md)
- 全部政策见 [docs/design/governance/governance.md](docs/design/governance/governance.md)；来源分级见 [docs/design/model/entities.md](docs/design/model/entities.md)，复核按 [docs/design/governance/maintenance.md](docs/design/governance/maintenance.md)
- 外部事实须核对原文后才提交；本阶段未取得的外部事实如实标为未核实。译名第 5 级按模型知识例外登记，不冒充已核外部事实；链接用 `[标题](url)`


## 规则

每次执行我需要执行概要和时间，在我批准后才可以执行
正式知识库位于仓库外的 ~/Documents/kb-vault/，本仓库维护模型、规则、词表和应用工具。AI 检查和验证知识库时优先使用 Obsidian CLI，避免使用 Computer Use。
避免自造词汇，使用业界术语或者业界惯例用词用语

- **目的优先，整体一致**：约束做事方式，避免局部修补不断累积，破坏整体。
- **直接表达，面向读者**：约束表达方式，避免把构思过程、修改历史和任务要求写进成品。
- **言之有物**：陈述具体事实、机制、条件或后果；评价必须有依据。删除没有新增信息的价值宣称、受众称呼和重复总结。
- **内容先于篇数**：写作前明确读者的问题、相较原始资料新增的价值和文档类型；说不清楚就不建文章，不用泛泛建议冒充操作指南。
- **组织依据明确**：优先使用现有主题、实体、文档类型和载体；索引明确收录范围和查找依据。模型不足先提出设计缺口，不临时创造分类。
- **入库前审阅**：检查内容价值、类型符合性、组织合理性和元数据有效性，字段校验不能代替内容审阅。批量写作先完成一篇样稿及索引示例，经用户确认后再扩展。
