# 治理测试复现

## 设计状态

本规格经用户批准，用于关闭 `feat/terminology-governance` 合并前的既存全量测试失败。它只修复测试依赖与冻结输入边界，不改变来源或术语结论、迁移账本、正式词表、决定或现行应用设计。

## 问题边界

当前七组 tracked 测试读取被 Git 忽略的 `.superpowers/sdd/2026-08-31-*` 产物；来源迁移测试还把 2026-08-31 的冻结 hash 与持续变化的当前计划和草案比较，basis ledger 则把冻结 `old_file_sha256` 与当前词表比较。结果是干净 clone 缺少输入，长期工作区又因正常演化产生 hash mismatch。

`requirements-dev.txt` 已固定 `jsonschema==4.23.0`。未安装该文件属于测试环境缺失，不通过修改生产代码解决。

## 冻结来源

冻结提交固定为 `9e7b411c23e890d13d70fc16d443b760313126c4`，由原 `source-plan-input.md` 与 `vocab/migrations/source-v1/basis.yaml` 共同记录。测试 fixture 保存：

- 来源计划验证的三份正式文件在该提交的 bytes；
- basis ledger 涉及的六份正式文件在该提交的 bytes；
- 原六份库存 TSV、六份报告和三份基线报告；
- 术语迁移使用的 `term-glossary.tsv`；
- entities、roles、basis、source、match ledger 使用的精确 proposal、exception、blocked 与 preview 文件。

fixture 位于 `tests/fixtures/governance-frozen-2026-08-31/`，保持原相对路径层次。它是不可变测试输入，不是现行项目文档、正式编辑源或 Superpowers 审查正文。

## 测试边界

七组测试只改输入根：

- `test_source_migration.py` 用 frozen root 验证三份正式 hash，并用 fixture inventory 验证十五份库存 hash；
- `test_source_basis_ledger.py` 用 frozen root 验证六份旧文件 hash；
- 四份来源 ledger 测试读取 fixture proposals；
- 术语迁移测试读取 fixture `term-glossary.tsv`。

生产 ledger、schema、决策 fixture 和迁移实现仍从现行仓库读取。不得更新任一历史 expected hash 来迎合当前 bytes，不得从 fixture 生成正式数据。

## 验收条件

- 按 `requirements-dev.txt` 建立的新 venv 可在干净 clone 运行全量测试；
- fixture 文件逐项命中现有历史 hash；
- 当前仓库与冻结提交不同不再使历史测试失败；
- 删除 `.superpowers/sdd` 后全量测试仍可运行；
- 合并前后全量测试结果一致；
- `kb-obsidian` 最终 pin 与持久 vault manifest 更新到修复后的 `kb-design` 最终提交。
