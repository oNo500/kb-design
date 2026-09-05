# 项目迁移计划

状态：迁移与验收已完成。执行依据为本计划及本次会话确认的 monorepo、uv 与输出目录要求。

目标：把现有项目整理为 monorepo，使用 uv 管理 Python 工程，支持仓库内默认产物与显式外部输出。依据为本次会话确认的目标架构；[现行架构](../../ARCHITECTURE.md)仅作为迁移前职责来源。

分支：`feat/monorepo-layout`；基线：`564bfbf`。直接使用当前 checkout，不创建额外 worktree；uv workspace 沿用已确认方案。计划编写约 5 分钟，批准后的实施粗估 45–90 分钟。

## 范围边界

- 根 `README.md` 连同禁止 AI 修改的注释逐字节保留；`ARCHITECTURE.md` 改为目标架构说明，动态导航与进度分别进入 `docs/README.md` 和 `work/roadmap.md`。
- 当前只整理现有库和应用，保留业务规则、数据身份与状态；不扩大模块拆分，不新增应用，不为旧命令和旧路径增加兼容层。
- 正式词表、编辑权、未生效草案和迁移审计的效力不变；不创建正式术语数据、不激活消费者、不发版。
- 现有外部 `kb-vault` 不搬迁、不刷新。根 `output/` 是持久应用数据，`build/` 是可清理的临时产物，两者均由 Git 忽略。

## 文件去向

| 现有位置 | 目标位置与处理 |
|---|---|
| `concepts/` | `docs/concepts/`；其中 `glossary.md` 单独进入 `docs/glossary.md`，继续作为现行登记源 |
| `design/` 根文档 | `docs/design/model/` 放模型、词表、关系与版本；`docs/design/governance/` 放方法、治理、写作和维护 |
| `design/targets/`、`decisions/`、`drafts/` | 分别进入 `docs/design/targets/`、`docs/decisions/`、`docs/drafts/` |
| `sources/` | `docs/references/` |
| `vocab/` 六份正式词表及 `CHANGELOG.md` | `data/vocab/` |
| `vocab/build/` | 实际生成输入进入 `data/inputs/topics/`；`gbt_en.py` 随核心实现迁移；回查输出与复核记录进入 `data/audit/labels/` |
| `vocab/glossary-layout.yaml` | `data/inputs/terminology/glossary-layout.yaml`，保持未启用 |
| `vocab/migrations/`、`vocab/signals.yaml` | `data/audit/migrations/`、`data/audit/maintenance/signals.yaml` |
| `scripts/` 中长期维护的数据处理与命令 | 进入 `packages/kb-core/src/kb_core/`，仅作包组织、入口和路径适配；文档检查等整仓辅助仍在 `scripts/` |
| `tools/obsidian/` | 源码、应用说明和测试整体进入 `apps/obsidian/`；`scripts/export_obsidian.py` 进入应用包的 `exporter.py` |
| 根 `tests/` | 核心测试进入 `packages/kb-core/tests/`；跨工程用例进入 `tests/integration/`；共用及冻结 `fixtures/` 留在根测试目录 |
| `docs/superpowers/` 与应用内实施计划 | 按用途进入 `work/plans/`、`work/reviews/` 或 `work/archive/`；逐项确认状态，不因日期较早自动归档 |
| `schemas/`、`.gitattributes` | 保留共享契约及冻结证据设置；必要引用随目录调整 |
| `requirements-dev.txt` | 依赖归入根开发配置或相应成员的 `pyproject.toml`，由统一 `uv.lock` 锁定 |

## 执行清单

- [x] 建立逐文件迁移对照，列明保留、迁移及派生缓存清理项；按职责搬迁，更新现行文档、代码、测试中的路径与引用。审计记录中的历史身份、路径和哈希保留原值，冻结证据不参与批量替换。
- [x] 建立根 uv workspace、统一锁文件和 `.python-version`，保留核心库与应用各自的 `pyproject.toml`；Obsidian 通过工作区依赖使用核心库，核心库不依赖应用。Python 版本按现有代码与依赖约束核实后固定，不借机升级功能。
- [x] 将现有实现归入两个工程，补齐必要的导入、命令入口、资源定位和测试路径；不重写业务算法。输入与仓库位置显式传递，不依赖执行目录。
- [x] 默认 vault 定位为 `<仓库根>/output/obsidian/`；初始化的 `--output` 与后续操作的 `--vault` 显式路径优先，支持外部绝对路径；保留 `--design-root`。目录保护允许指定产物区，继续保护源码、正式输入与用户内容；刷新写集仍限于参考区及清单。
- [x] 根 `.gitignore` 统一忽略 `/output/`、`/build/`、`.venv/` 与 Python 缓存；停止跟踪现有 `.pyc`。不建立默认 vault，不把用户数据列入构建清理对象。
- [x] 更新架构、导航、工程说明和适用治理摘要；在计划获批后新增迁移决定，记录新布局与输出边界。历史决定正文保留，旧定位以原提交解释，新导航提供当前位置。
- [x] 完成下述定向验收后整理 `[L2]` 提交；实施中发现额外范围或明显超出估时，先报告原因与新增计划，再取得批准。

## 验收依据

| 目标失败与后果 | 独有证据 |
|---|---|
| 文件遗漏、历史被改写，导致数据或追溯丢失 | 逐文件去向与 Git 写集对账；README、正式数据及冻结证据内容比对；预期路径变化单独列明 |
| 生成输入或导入失效，导致词表变化或命令不可运行 | 迁移后的核心生成与校验流程；在隔离副本生成并比较正式数据，文件头路径等机械差异明确列出 |
| 工程依赖断裂，导致应用不能消费共享数据 | uv 环境下核心与应用的既有相关测试，以及干净临时快照上的初始化、建内容、校验和报告流程 |
| 默认路径或刷新越界，导致覆盖源码或用户内容 | 临时目录内验证默认与外部输出、切换执行目录、拒绝受保护路径，以及刷新后用户文件与配置保持原样 |

只为新增默认路径行为补必要测试；文档和机械迁移直接核对。不为文件存在、常量回显或重复计数另造测试；必要回归在迁移完成边界统一运行，历史链接不强改为当前事实。

验收结果见[迁移验收](../reviews/2026-09-05-monorepo-layout.md)。

## 回退方式

迁移按可核对的批次提交；需要回退时撤回对应提交，保留分支及原始历史。未提交修改只按本次写集恢复，不使用整仓强制重置或清理。`output/`、外部 vault 和用户配置不参与代码回退。
