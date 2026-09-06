# 完整来源候选

本提案严格覆盖完整术语候选实际引用的 51 个待提案来源。它复用旧术语来源候选中的 11 条，另列 40 条新增来源实体；8 个已有正式实体只复用，不重复建立。全部记录尚未采纳，不改正式数据、来源用途、术语数据或规则。

## 来源边界

来源实体按实际材料身份分档。固定作者论文、归档案例、历史邮件、判决和固定机构出版物使用 archival；ISO 标准与 W3C Recommendation 使用 de-jure；未锁定固定发表版本的持续网页保持 de-facto。archival 只表示所引内容固定，不表示过时。

subjects 保持空数组，source_status 在未逐项核实当前外部状态时省略，review 不制造复核结论或义务。非空 version 均有对应 basis.version 和未来决定精确 patch；版本线索不足的记录保持 null。

## 来源收敛

原 5 个 de-facto 定义根已经闭合。audit 与 audit trail 改指固定的 NIST SP 800-53 Revision 5；cheat sheet 改指 The American Heritage Dictionary 第五版；DND 框架按 2022-07-28 独立发表版登记；DfE 指导按所读 2026-08-11 更新版登记。旧聚合页不再承担定义 basis，也没有修改旧页面 tier 或开放规则例外。

JSON 的 fixed_definition_source_resolution 保留本轮改指审计，四份替代值均已并入主 items。最终主数组与术语 dependency 的 51 个来源一一对齐。

这仅处理了新增来源部分。完整包仍有 6 条定义复用正式的 de-facto 实体：SWEBOK 的知识体系与普遍接受的知识、CS2023 的知识领域／知识单元／主题、IPTC 的体裁。原档级保持不变；所列定义使用须按[完整提案](2026-09-06-term-complete-candidate.md)明确采纳限定许可。新增来源检查通过不等于整包定义准入通过。

## 采纳边界

未来来源采纳决定建议使用 decision-source-term-complete-citations。该决定尚不存在，当前 history 引用只表示未来采纳标识。schema 与 51 项引用覆盖检查不能替代人工采纳，也不创建 structure、mapping 或其他来源用途角色。
