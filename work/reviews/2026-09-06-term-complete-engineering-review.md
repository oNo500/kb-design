# 术语完整包复审

## 审查范围

2026-09-06 对完整包新增的 project 依据、限定定义来源许可、布局与名称边界、应用快照捕获作集成复审。依据为已采纳的 term-complete-structure、term-data-values、term-limited-definition-source-use 与迁移记录。本次不重复数据逐项机械对账、语义全文阅读或全量回归。

## 权限缺口

发现一项 Important：`packages/kb-core/src/kb_core/governance/build_terms.py` 的 `validate_glossary_layout` 只检查完整布局值的精确授权，没有检查决定级别。实际布局中的历史名称处置包含原因、效力和采纳引用，不只是排版参数。

最小反例在内存中修改实际布局第一条历史名称的 reason，以 schema 有效、accepted、L1 的决定精确授权整个改后布局，再经 `accepted_decisions_from_documents` 解析后送入布局校验；结果为空错误集。普通工程级决定因此能够更改历史名称处置，而术语 record 已要求至少 L2。应用和生成共用该入口，均受影响。

建议为完整布局授权增加明确级别要求。当前完整布局同时承载已采纳 L3 结构和历史名称处置，最小修复可统一要求 L3；不能把排版微调的可逆性当作名称效力变更的权限。本结论记录的是此次检查时的实现，不代替后续修复复审。

## 保护证据

project 校验同时要求当前完整 concept record、准确 project_basis_scope 与对应 concept 或 term 的 history 指向同一个 L3 approval。定义和形式的 project 内容进入精确 scope，不能仅借 scope 或另一对象的 record 使用项目依据。已采纳结构仅开放列明的既有对象，本次没有扩大该范围。

对定义来源许可作内存最小反例：缺许可时返回 `TERM_DEFINITION_SOURCE_FORBIDDEN`；精确许可通过；修改来源版本、来源身份、完整定义值或把许可 identity 换成另一概念，均拒绝。该检查不把六项已批准例外推成所有 de-facto 或 vendor 来源的普遍资格。

应用源码核对确认：layout 与术语、state 同次捕获；布局 schema 通过捕获字节传入；选定提交的术语 previous 由 Git helper 取得；实现清单包含本次新增共享模块和 schema。显式 input_bytes 路径继续使用捕获值。现行主题、实体和类型词表的 label、alt、hidden 从已校验的同次词表捕获补入诊断已知名称；布局说明与历史名称不成为当前术语准入源。

## 发布边界

term-complete-publication 在此次复审时仍为 proposed。当前 term record 的 active 与发布消费者状态分开，拟议 publication 不进入有效决定集合。本复审没有激活 publication，没有写正式 state、现行 glossary 或外部 vault。

实际数据与已采纳具体值的机械一致性由迁移对账负责，本次不重复宣称独立完成全部对账。主线全量 core 与 app 回归尚在其验收流程内，本报告的限定反例不能替代该结果或条件式切换的最终确认。

## 修复复审

同日限定复审确认，上述唯一 Important 已关闭。`validate_glossary_layout` 现在同时要求 L3 和完整布局值精确授权。重放实际布局历史名称改写的内存反例，L1 返回 `TERM_LAYOUT_ADOPTION_MISSING`；仅将同一决定改为 L3 后通过。

应用日期修复未发现新增可信高风险问题。`_date_value` 仅接受原生 date 或有效、规范的 YYYY-MM-DD 字符串；实际验证闰日字符串与原生 date 得到同一 date 值，非法日历日期、非规范字符串及 datetime 均拒绝。源码确认 version.date、added、checked 使用同一转换；转换发生在捕获字节解析后的内存文档，不改写原始输入或其哈希。

本次只重放上述权限反例与日期边界，不重复全量测试。工程复审不再保留开放 Important，主线仍须完成提交后的同一干净快照验收与条件式 publication 最终确认。

## 索引增量

同日静态复审确认，限定定义许可的反向索引新增边只读取决定 patch.identity，接受当前术语集中实际存在的裸概念身份或 terms/concepts 路径身份；不递归解释 patch.value 或历史审计内容。边明确使用 `decision.declared_concept` 与 `state: declared`，只表示决定声明的目标，不表示该决定已精确批准目标的某个值。实际授权继续由独立校验器判定。

维护 CLI 将 `read_term_data` 返回的同次有效决定集合传入 `decision_documents`；新增语义边没有另读磁盘决定内容。此次增量未发现新的可信高风险问题，未重复测试或许可边计数。
