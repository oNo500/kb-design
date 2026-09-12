# 来源字段采纳

状态：已采纳，2026-09-05。用户在收到[字段提案](../../work/reviews/2026-09-05-source-adoption-proposals.md)及“是否采纳 P1–P4，作为后续候选的字段依据”的确认请求后回复“继续”。本决定只采纳这四项列明的字段，不批准完整实体、用途角色或正式切换。

## 采纳范围

| 对象 | 采纳字段 | 证据日期与边界 |
|---|---|---|
| iso-25964-1 | version 保持 2011；候选外部 status 为 current；增加提案所列 basis.version 和 basis.status | 仅基于 2026-08-29 的已留存官方状态阅读记录，不解释为本轮重新核实 |
| iso-25964-2 | version 保持 2013；候选外部 status 为 current；增加提案所列 basis.version 和 basis.status | 同上，Part 2 依据独立于 Part 1 |
| z39-19 | version 保持 2005 (R2010)；单 url 在候选中改为提案所列 landing 主地址和 DOI 非主地址；增加 basis.version 和 basis.urls | 依据为提案中冻结的 NISO 阅读记录；外部 status 未获新赋值 |
| skos | version 保持 2009-08-18；增加提案所列 basis.version | 只采纳版本依据；不从 Recommendation 推出 current |

完整字符串、locator、地址和 checked 使用字段提案中的 P1–P4 YAML 片段，逐字保留；提案的本地材料哈希继续作为审阅输入。原有 basis 的其他键保持。除 NISO 旧 url 由 urls 替代以及两个 ISO 外部状态外，不删除或重释原字段。

## 候选边界

这些字段先进入独立 Git 候选分支。原项目 active 与外部 current 语义不同，不能在主分支的旧格式实体表中直接混写。候选保留未完成字段的真实形状，不补默认 review、watch、history、replaced_by 或来源义务，也不把“不核对”改为已通过。

原核对日期不改为今天。没有被 P1–P4 点名的字段、其他来源事实、角色与映射保持原有审批状态；本决定不撤销旧账本，不创建新义务或发版记录。

## 版本与验证

依照[来源执行](source-execution-boundary.md)，候选以 Git 提交保存，恢复使用明确提交范围的 revert，不实现补偿回滚。只核对批准写集、原值、未选记录保留、现有 schema 与消费者兼容；完整切换仍须基于真实校验结果，失败不得以修改正式输入或弱化 schema 消除。
