# 治理测试复现实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Steps use checkbox syntax.

**Goal:** 让治理全量测试只依赖 tracked frozen fixtures，并在隔离开发环境与干净 clone 中通过后完成两个功能分支的本地合并。

**Architecture:** 从冻结提交 `9e7b411c23e890d13d70fc16d443b760313126c4` 提取正式 bytes，把所需 ignored inventory/proposal bytes复制到单一 tracked fixture；七组测试改读 fixture。测试绿色后形成新的最终 design commit，更新 `kb-obsidian` pin 与空 vault，再执行两仓库快进合并。

**Tech Stack:** Python 3.9、`requirements-dev.txt`、`unittest`、Git。

**Spec:** `docs/superpowers/specs/2026-09-04-hermetic-governance-tests-design.md`

## 全局约束

- 不修改历史 expected hash、ledger 内容、来源或术语语义。
- fixture 固定 `9e7b411c23e890d13d70fc16d443b760313126c4` 与原 ignored artifacts 的已记录 bytes。
- 不把 Superpowers 过程说明复制为现行项目文档；fixture 只保存测试实际消费的输入。
- 测试不得再引用 `.superpowers/sdd`。
- 使用 `requirements-dev.txt` 的隔离 venv，不修改系统 Python。
- 合并前后都运行两仓库全量测试；失败即停止。

### Task 1: 冻结夹具与测试路径

**Files:**
- Create: `tests/fixtures/governance-frozen-2026-08-31/**`
- Modify: `tests/test_source_basis_ledger.py`
- Modify: `tests/test_source_entities_ledger.py`
- Modify: `tests/test_source_roles_ledger.py`
- Modify: `tests/test_source_derivation_ledger.py`
- Modify: `tests/test_source_match_ledger.py`
- Modify: `tests/test_source_migration.py`
- Modify: `tests/governance/test_term_migration.py`

**Interfaces:**
- Produces: `FROZEN_FIXTURE_ROOT` and exact tracked inventory/proposal paths consumed by all seven tests.

- [ ] Copy only the files referenced by the seven tests and `FROZEN_INVENTORY_HASHES`; extract formal root files with `git show 9e7b411:<path>`.
- [ ] Change test constants from `.superpowers/sdd` and current `ROOT` frozen comparisons to the tracked fixture paths.
- [ ] Run the seven test modules first and verify all historical hashes without changing expected values.
- [ ] Search `tests/` and require zero `.superpowers` references.
- [ ] Commit `[L2] 测试:固定治理迁移夹具`.

### Task 2: 隔离全量验证

**Files:** no planned tracked changes.

- [ ] Create a temporary venv and install `requirements-dev.txt`.
- [ ] Run `python -m unittest discover -s tests` in the feature working tree.
- [ ] Clone the feature branch to a clean temporary directory without ignored `.superpowers` state and run the same full suite.
- [ ] Run `git diff --check` and confirm clean status.

### Task 3: 应用绑定与空库更新

**Files:**
- Modify in `kb-obsidian`: `src/kb_obsidian/design_source.py`, expected hashes in tests, and README exact hash.

- [ ] Commit all final `kb-design` plan/spec/fixture changes and record its exact HEAD.
- [ ] Update the `kb-obsidian` production pin and all default expected hashes to that HEAD.
- [ ] Run the application full suite and commit `[L2] 应用:固定可复现设计快照`.
- [ ] Rebuild an empty persistent vault from the new pin while retaining the previous vault in Trash or an explicit backup until verification completes.
- [ ] Verify 857/857 manifest hashes, empty content and seven reports.

### Task 4: 本地合并

**Files:** no new implementation files.

- [ ] Re-run both full suites immediately before merge.
- [ ] Fast-forward `kb-design/master` to `feat/terminology-governance` and `kb-obsidian/master` to `codex/obsidian-application`.
- [ ] Re-run both full suites on merged `master`.
- [ ] Delete the two merged local feature branches only after green merged tests.
- [ ] Report commits and keep UI-openability assigned to human acceptance.
