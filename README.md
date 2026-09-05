# 新的 KB 设计

本仓库用于设计一套独立的知识体系，保存研究、概念、设计和正式词表数据。知识库中的笔记与内容在别处维护。

## 项目缘起

独立仓库让设计不受既有知识结构牵引，也避免把既有内容中的误差直接带入规则。这一边界来自此前几次失败的经验。

## 设计原则

设计阶段保留充分探索空间，但定稿以已有规范、事实标准、项目现行设计和已采纳决定为依据。未经准入依据的 designation 不进入项目定稿；应用设计另按 [Application Profile](concepts/application-profile.md)与 [Reproducible Builds](concepts/reproducible-builds.md)两种已登记方法限制语义和完成声明。具体规则见[方法登记](design/principles.md)、[治理](design/governance.md)与[写作规则](design/writing.md)。

## 项目边界

本库只有研究、概念、设计和词表数据。知识库本身——笔记、内容——不在这里；应用形态通过独立映射落地。

| 层 | 内容 | 位置 |
|---|---|---|
| 与应用无关 | 概念、词表、内容模型、治理和维护规则 | `concepts/`、`design/`、`vocab/` |
| 应用约束 | 每个 target 的功能范围、模型引用、字段约束、使用和允许的 loss | `design/targets/` |
| 具体表示 | target location、type、reference form 和 encoding syntax | `design/targets/` |

与应用无关层不使用具体工具的字段名和文件格式定义自身；应用约束和具体表示不改动应用无关层的定义。导出 artifact contract 另负责把已选表示物化为稳定 bytes、文件集合、项目 manifest 和发布物，不取得修改语义选择的权力。六份正式词表是应用消费的源，各应用从正式词表导出，不反向编辑。主题词表虽是生成物，应用仍只读取正式输出；它的编辑路径见[主题词表设计](design/topics.md)。分层与消费者门禁见[应用约束与表示分层](design/decisions/application-profile-boundary.md)。

## 项目目录

| 目录或文件 | 职责 | 入口 |
|---|---|---|
| `concepts/` | 理论：每种方法是什么、为什么成立 | [概念索引](concepts/README.md) |
| `design/` | 现行规则、已采纳决定、应用映射和未生效草案 | [设计索引](design/README.md) |
| `design/decisions/` | 已采纳决定，只追加不修改 | [决定记录](design/decisions/) |
| `design/drafts/` | 十份尚未生效的项目草案 | [项目草案](design/README.md#项目草案) |
| `design/targets/` | 各应用的映射 | [Obsidian 映射](design/targets/obsidian.md) |
| `sources/` | 标准和文献的阅读笔记与抓取清单 | — |
| `vocab/` | 六份正式词表、主题生成输入、迁移审计和未激活配置 | [变更记录](vocab/CHANGELOG.md) |
| `scripts/` | 生成、校验、诊断、迁移预演、维护和应用导出能力 | — |
| `AGENTS.md` | 每次会话加载的写作与治理摘要 | [项目约定](AGENTS.md) |

`vocab/topics.yaml` 是正式主题词表和确定性生成输出；人工修改 `scripts/build-topics.py` 或其实际读取的 `vocab/build/` 输入后重建，不直接编辑输出。其余五份正式词表直接维护并校验。`vocab/migrations/` 只保存审计账本，不给正式数据反向赋予效力。

`concepts/glossary.md` 仍是 designation 与中英对照的现行编辑源。`vocab/glossary-layout.yaml` 是未激活的未来术语生成配置，不属于六份正式词表；仓库当前没有正式 `vocab/terms.yaml`。

## Obsidian 应用

[Obsidian 映射](design/targets/obsidian.md)是本库首个完整应用 target。它以应用无关内容模型为基础，规定 Obsidian 的功能范围、内容和词表的表示、使用边界与维护接口；导出 artifact contract 仍与这些语义选择分开。

实现分为两个仓库。`kb-design` 的 `scripts/export_obsidian.py` 把现行六份正式词表物化为单向参考区；独立的 `kb-obsidian` 从固定且干净的 `kb-design` 提交初始化新 vault，建立 UUIDv4 `draft` 内容，校验内容字段和正式引用，并生成只读使用报告。初始化器已用于建立和验证本地持久 vault 实例，实例包含正式参考表示、模板、Base、规则、报告入口、manifest 和最低 Obsidian 配置。

应用能力和运行效力继续分开。当前持久实例尚无实际用户内容，内容消费者没有正式激活，也没有可审计查询日志或回流接口；空库报告只证明报告路径可运行，不证明发生过内容使用。内容标识符使用无前缀、小写 UUIDv4，人的检索使用 title、派生 alias、正文和其他元数据。

生成文件和 Base 可以在 Obsidian 中编辑，但修改不回流、不取得 `kb-design` 项目效力。项目 manifest 不是 Obsidian 内容格式或 BagIt；同环境双跑和目录项替换也不产生 reproducible build 或 durability 主张。

完整 vault 的 `init`、`refresh`、`new-content`、`validate` 和 `report` 命令由独立 `kb-obsidian` 仓库提供。`refresh` 按[词表参考刷新](design/decisions/obsidian-reference-refresh.md)显式更新既有 vault 的 `kb/` 与清单，保留用户文件和配置。本仓库只直接提供词表参考导出，从仓库根运行：

```bash
python3 scripts/export_obsidian.py --repo-root . --output /absolute/new/path
```

独立导出的输出目标必须不存在或为空；非空目录、符号链接和受保护的仓库目录会被拒绝。完整应用的既有 vault 使用 `kb-obsidian refresh`，仍须传入已验证的干净设计快照；不直接复制文件绕过应用清单。

## 当前状态

- 最初七项治理与设计目标均已完成当前范围，并在[项目路线](docs/superpowers/plans/2026-08-31-project-roadmap.md)逐项记录产物和开放边界。
- 来源与术语基础已经实现，但没有正式来源 v2 数据、正式术语数据、正式义务、委托、消费者或切换状态。
- 首轮维护已经完成本轮可执行动作；开放的 designation、归属、候选接受和发版决定没有被自动应用。
- 三份既有草案与四份待定设计均已形成项目草案并保持未生效。
- Obsidian 完整应用 target、词表参考导出和独立应用实现已经建立，并已初始化本地持久 vault；实际用户内容、正式消费者、查询日志、回流和正式激活尚未发生。
- TBX 没有真实接收方，继续保留为触发式草案；严格来源或术语激活只在真实切换需求出现后另立计划。

项目执行计划记录过程与顺序，不属于项目设计组成；现行规则仍以 `design/` 正文、已采纳决定、应用映射和正式数据为准。
