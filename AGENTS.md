# kb-design 项目约定

本文是 [design/writing.md](design/writing.md)、[design/governance.md](design/governance.md)、[design/maintenance.md](design/maintenance.md) 和[主题生成路径](design/topics.md#生成路径)的会话摘要，每次会话加载；冲突时以各正文职责范围内的规则为准。

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

- **当前阶段零自定**：规则对象是未经准入依据、被用来命名概念的 designation。项目拟采用的 designation 必须按 [design/governance.md](design/governance.md) 的准入阶梯取得依据并登记；AI 不得主动形成或选定无准入依据的 designation 作为可复用的项目概念名称
- 拟作项目术语而未登记的 designation 不得进入定稿。普通叙述、来源转录、文件路径、代码和值中的任意字符串不因出现而自动成为术语；候选、`defer`、草案、占位和示例不能替代形式依据与概念对应依据，也不能取得试用资格

## 标点与间距

- 中文句子用全角标点；引号用“ ”，不用 `「」`（GB/T 15834 §4.8）
- 汉字与西文字母、数字之间加一个半角空格；与全角标点之间不加（clreq §6.3.3）

## 决策权

按 [design/governance.md](design/governance.md) 的三级：不改规则且可逆的直接做；改规则、改结构、改文件布局、术语准入、归属判断、候选删除的先提案；范围、零自定例外的开放、决定的采纳与推翻、删除非候选对象、发版、草案生效、来源改档只有人能定。提案先给小节清单或改动说明，人回复后再动文件。提交说明标注级别 `[L1]` `[L2]` `[L3]`。

## 审查与测试

- 每项审查或测试先说明要发现的失败、失败后果和独有证据；没有可信高风险失败，或已由更强门禁覆盖时，不设计、不执行
- 保留语义效力、决策权、稳定身份、迁移完整性、生成确定性、共享接口、删除、正式切换和回滚检查
- 文件存在、常量回显、重复计数、包装函数透传、实现细节和已由 schema、哈希、写集或端到端检查覆盖的事实，不单独测试或独立复审
- TDD 只用于保留的行为测试；文档、静态配置、确定性生成物和纯机械迁移使用直接校验，不为 RED／GREEN 形式另造测试
- 全量回归只在风险阶段边界运行；机械事实由命令证明，不交给第二代理重复确认

## 阶段边界

- 迁移账本只作审计，候选和诊断输出只供人工复核，schema、索引、探测、生成和维护能力只证明机械能力；它们都不等于正式数据、草案生效、正式切换或发版
- 来源与术语基础的当前范围见[当前阶段](design/decisions/current-stage-scope.md)。仓库当前没有正式来源 v2 数据、正式术语数据、正式义务、正式索引、委托、消费者或切换状态，不得因接口存在而创建或宣称存在
- Obsidian 是应用层，也是首个完整应用 target 的设计；当前唯一实现仍是现行正式词表的单向参考导出。完整内容应用设计不等于消费者激活
- 仓库没有由本项目建立的真实 vault、内容数据、内容建立器、内容校验器、运行消费者、报告、查询日志或回流接口；新内容单元使用无前缀、小写 UUIDv4，UUID 文件名承担稳定路径，title 与派生 alias 等元数据承担人的检索
- 来源和术语正式激活均未发生；TBX 继续后置为无真实接收方的未生效草案

## 应用分层

- [Application Profile](concepts/application-profile.md)与 [Reproducible Builds](concepts/reproducible-builds.md)是已登记方法；项目保留 English `Application Profile`，不采用未经核实的中文 designation
- 应用无关模型、`Application Profile` 的 target location／type／reference form／loss 语义选择、导出 artifact contract 的 byte serialization／file set／manifest／validation／publication 分开；后两者不得反向修改前者
- field／property／path binding 不是 `metadata crosswalk`，不改变词表层 `crosswalk`；新 target 必须引用概念文、[方法登记](design/principles.md)和适用的已采纳决定
- 生成文件与 Base 可以在 Obsidian 中编辑，但修改不回流、不取得项目效力；完整应用设计、target 文件或参考导出存在都不等于内容消费者启用
- 当前只宣称同环境确定性、项目 manifest 完整性与成功目录替换的 atomic visibility；不宣称 DCAP、DCTAP、JCS、BagIt、reproducible build conformance 或 durability
- 上述边界由[应用约束与表示分层](design/decisions/application-profile-boundary.md)固定；旧[设计与应用分离](design/decisions/form-independence.md)决定继续有效且不修改

## 编辑路径

- `vocab/topics.yaml` 是正式主题词表和确定性生成物，不直接编辑；修改 `scripts/build-topics.py` 或其实际读取的 `vocab/build/` 输入，重建后运行主题校验
- `concepts/glossary.md` 仍是 designation 与中英对照的现行编辑源；仓库当前没有正式 `vocab/terms.yaml`，生成能力不转移编辑权

## 其他约定

- `concepts/` 下的文章另按 [concepts/CONVENTIONS.md](concepts/CONVENTIONS.md)
- 全部政策见 [design/governance.md](design/governance.md)；来源分级见 [design/entities.md](design/entities.md)，复核按 [design/maintenance.md](design/maintenance.md)
- 凭记忆写的内容联网核对后才提交；链接用 `[标题](url)`
