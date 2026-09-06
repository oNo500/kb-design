# 术语来源候选

本提案覆盖术语数据候选当前 13 条来源依赖，形成 13 份完整 source entity v2 候选记录。它只供人工审阅，不改变现有 62 个正式实体、31 条来源用途，不新增 structure、mapping 或其他角色，也不批准术语数据。

## 来源范围

主线确认后的 13 条依赖均有候选记录。既有提案中的 `iplf-iso-standard` 不在当前 dependency 清单，未纳入本包。每条记录保留原文可核英文题名、材料身份、支持字段、未知字段和 tier 理由；subjects 为空，source_status 省略，review 不造复核结论或义务。

## 待定事项

主线已确认 DCMI Metadata Terms 的技术 ID 为 `dcmi-metadata-terms`，并负责同步术语候选 references 与 dependency。本提案已使用该 ID。

未来来源采纳决定建议统一使用 `decision-source-term-citations`。JSON 已列出所有非空 version 及 basis.version 的精确 patch。该决定尚不存在，因此当前引用对齐检查应报告待采纳 blocker，而不能用假的 accepted 决定让校验通过。

## 机械检查

应将 `items[].proposed_record` 投影为 source entities v2 文档后做 schema 校验，并核对 13 个 dependency ID 一一覆盖。采纳前的预期问题是未来决定不存在；记录不应产生其他缺项或多余依赖。


Hogan 论文引用已锁定为 `arXiv v6`，使用版本化 PDF 地址；期刊年份只保留在材料身份说明中，不作为该 PDF 的版本值。
