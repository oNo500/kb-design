# 文档迁移验收

## 变更范围

基线提交：`407d50da1ac8f83131cac26a95a94cbf352825ac`。实现提交：`de438f9b246b0f6d6f7abcae4cb362564ada62d1`。分支：`docs/topic-organization`。

原 docs 的 103 份文档和根 ARCHITECTURE 按[迁移清单](../plans/2026-09-12-docs-topic-files.json)处理；根 README 保留。概念、设计、来源、决定和提案按主题关联，新增主题首页、概述、架构和已采纳术语设计的说明。正式数据及生成输入保持原字节。

## 内容去向

| 原内容 | 当前去向 |
|---|---|
| 概念索引的跨主题导航 | 文档首页、知识模型首页及各主题首页；概念正文均保留 |
| 根架构的目录与工程说明 | docs/architecture.md；根文件保留入口 |
| 内容模型中的共同适配合同 | docs/applications/shared/requirements.md；内容模型保留引用和语义边界 |
| 主题设计中的具体界面表示 | 应用设计承接；主题正文保留依据必须可读的共同要求 |
| 治理与维护中的历史库数量、执行进度 | 从长期规则正文移出，原证据仍由既有决定、执行记录和 Git 保留 |
| glossary 旧本地阅读链接 | 生成器调整表示目标；已采纳布局输入不改写 |

## 校验结果

| 检查 | 结果 |
|---|---|
| 迁移完整性与效力分类 | 全部目标存在；当前分类与原分类一致 |
| 既有决定保护 | 41 份决定逐字节不变；来源有效决定、术语有效及历史决定全集与基线一致 |
| 数据保护 | data/ 全部原文件逐字节不变 |
| 主题确定性 | 候选生成与正式 topics.yaml 逐字节一致 |
| 术语校验与生成 | term-data check、build-terms check 通过；glossary 仅一处本地链接变化 |
| 文档导航 | 相对链接与锚点校验通过；历史决定保留原路径语境 |
| 核心测试 | 292 项通过 |
| Obsidian 测试 | 非术语 115 项通过；术语 12 项修正临时夹具的目录与重复策略后重跑通过 |
| 预览测试 | 9 项通过 |
| 路径与快照语义审查 | 未发现高／中风险阻断问题；未重复机械计数和哈希校验 |
| 完整应用验收 | 新干净提交初始化系统临时库成功，1072 个受管理文件，其中 157 个术语页 |

Obsidian 禁止以仓库 build 目录作为知识库目标，首次调用被保护规则拒绝。随后使用系统临时目录，未绕过保护规则，未操作默认 output 库或外部正式知识库。

## 基线失败

集成测试共 23 项，当前为 16 项失败、6 项错误。对迁移前提交的独立本地副本执行相同测试，失败数量及全部失败条目完全一致，没有新增失败条目。原因包括旧计数断言和缺少书目、采纳材料的旧夹具；本次不改写其测试目标，也不宣称全量测试通过。

详细运行输出保存在 Git 忽略的 build/docs-migration/：core-final.txt、obsidian-tests.txt、term-export-tests.txt、preview-tests.txt、integration-tests.txt、integration-before.txt、integration-comparison.json、links-final.txt、term-check.txt、terms-generation-check.txt 和 vault-init.txt。临时库位置记录在 temp-vault-path.txt。

## 验证命令

```bash
uv run python -m unittest discover -s packages/kb-core/tests
uv run python -m unittest discover -s apps/obsidian/tests -t apps/obsidian
uv run python -m unittest discover -s apps/obsidian/tests -t apps/obsidian -p test_term_export.py
uv run python -m unittest discover -s apps/vocab-preview/tests
uv run python -m unittest discover -s tests/integration
uv run python scripts/check-links.py
uv run kb-core term-data check --root .
uv run kb-core build-topics --output build/docs-migration/topics.yaml
```

完整初始化以实际提交为输入，使用 --design-root 指向本仓库、--output 指向系统临时目录。它只证明该快照下的完整读取与初始化，不证明外部正式库同步、查询日志或内容消费者启用。
