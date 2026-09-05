# 来源候选验证

状态：已物化 P1–P4 并完成兼容检查；候选不得正式切换。采纳依据为[来源字段采纳](../../docs/decisions/source-field-adoptions.md)。基础提交 `5b6f758`；候选提交 `7a4377a`，分支 `codex/source-v2-candidate`。候选在独立 worktree 中由 Git 管理，不与正式库混用。

## 实际写集

候选只修改 `data/vocab/entities.yaml` 的四条记录：`iso-25964-1`、`iso-25964-2`、`z39-19`、`skos`。应用了提案的版本与依据，两个 ISO 的候选外部状态改为 current，NISO 的旧 url 改为 urls；未选记录与文件头保持原字节，实体集合、ID 顺序和其他字段语义保持。

采用既有迁移模块 `_apply_file_rewrites` 的旧文件哈希保护，没有增加迁移或回滚框架。所有嵌套 basis 的原有其他键保留；新 checked 使用已采纳的 2026-08-29。没有填入默认 review、watch、history、replaced_by、义务或角色批准。

原文件 SHA-256：`f0391778373f7ac93fee8dbdd3b907e8448c8e8f3add89c8a9d82a639f51c874`。

候选文件 SHA-256：`075f2123713e2931ed2ff66df7290539e95b6b2f467f22cc2bb1a31e920e85f9`。

## 结构结果

复用现有 `validate_repository` 检查基线与候选。旧格式基线报告 474 项，候选报告 470 项。这不是“新增了 470 个问题”，也不能因数量减少而宣称迁移通过；当前正式旧格式本来就未满足严格 v2 合同。

| 校验对象 | 已确定的失败 | 后果 |
|---|---|---|
| 两个 ISO 记录 | 缺 history、review、replaced_by、urls；watch 仍为字符串，basis.subjects 仍为紧凑字符串 | 已采纳的版本和外部状态不能代替完整记录合同 |
| NISO 记录 | urls 已进入候选，但缺 history、review、replaced_by；active 不是外部状态枚举；旧 watch 和 basis.subjects 未迁移 | 不能把已核地址推广为整条来源已就绪 |
| SKOS 记录 | 只有版本依据获准，其他必需字段及外部状态仍未完成 | 不允许从版本或 Recommendation 自动补 current |
| 共用实体字段 | source-entities schema 不接受现有 added、checked、subjects、tier，以及部分旧 url | 必须明确字段保留与模型覆盖，不能为通过校验直接丢弃这些字段 |
| 全库合同 | 其余来源、用途和必需文档仍保持旧格式 | 不能把四个部分记录与旧表混合后声明全库 v2 生效 |

“不核对”保留为事实限制，不删除校验器的 required，不生成空义务文档冒充正式义务，也不把旧 review 日期整体升级成本轮新复核。

## 应用结果

既有 Obsidian exporter 读取候选时返回退出码 1，首个错误为：

```text
OBSIDIAN_EXPORT_ERROR data/vocab/entities.yaml: object iso-25964-1: entities[iso-25964-1].basis.status: unknown field
```

当前实体导出合同的 basis 只接受 subjects，尚未支持新的来源字段依据。不能只忽略未知字段，因为那会静默丢失已采纳依据；也不能将项目 active 与外部 current 混作同一状态。

这项失败明确了下一步需要处理的是共用字段保留与应用读取合同，不是重新检索已采纳的四项资料。适配应先确定状态与字段的表示，不通过简单放宽未知字段检查来掩盖信息损失。

## 验证边界

本轮保留三类检查：批准写集与原值对账防止越权修改；现有 schema 检查暴露不完整字段；真实 exporter 调用暴露消费者不兼容。没有运行无关应用回归或重复检查既有离线工具。原始诊断保存在工作分支 Git 忽略的 `build/source-candidate/`。

候选提交是可继续开发和比较的中间状态，不是通过门禁的发布版本。主分支仅接收采纳决定和本报告，不合并候选实体数据；正式 vault 不刷新。恢复候选使用 Git revert，未建立补偿回滚。
