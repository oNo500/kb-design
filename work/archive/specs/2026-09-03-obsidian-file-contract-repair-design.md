# 文件合同修正

## 设计状态

用户已批准彻底统一 Obsidian 应用的目录、文件、内部链接和报告表示。本规格冻结修正后的文件合同，供实施计划使用；在实施、验证和持久 vault 切换完成前，现行生成器与现有 `kb-vault` 仍按旧合同存在，不能把本规格描述成已经生效。

## 缺陷证据

2026-09-03 对 `/Users/xiu/code/kb-vault` 的完整扫描得到：

- 共 870 个文件；
- 858 个文件 stem 已使用小写 kebab-case；
- `Home.md` 与 `KB/Views/Topics.base`、`Entities.base`、`Sources.base` 使用 PascalCase；
- `App/Rules/README.md` 与 `App/Reports/README.md` 使用全大写约定名；
- 全库共有 2061 个 Wikilink；
- 只有 `App/Reports/README.md` 的四个入口使用 Markdown link；
- 其中 `validation.json` 与 `topic-usage.json` 不属于 Obsidian 支持的可打开格式。

Obsidian CLI 的 `links` 会把现有 JSON 路径列为已解析，`read` 也能读取 JSON bytes，但 `open` 后工作区只出现空标签页。因此“路径存在”“link graph 已解析”“CLI 能读 bytes”和“Obsidian UI 能打开”是四个不同条件，不能互相替代。

根因是两个生成链没有共享的命名与链接合同：`kb-design` 的既有导出器生成 PascalCase `KB/Views/*.base`，`kb-obsidian` 后建的应用文件使用小写 kebab-case，而入口文件又分别使用 `Home.md` 和 `README.md`。现行设计逐项列出路径，却没有建立对象职责到路径形式的完整矩阵。

## 依据边界

[Obsidian 内部链接](https://obsidian.md/help/links)同时支持 Wikilink 与 Markdown link，默认生成 Wikilink；指向 vault 内文件时可以使用从 vault 根开始的正斜线路径。两种语法都合法，但一个受管理生成合同应只选择一种，避免编码和校验分叉。

[Obsidian 支持格式](https://obsidian.md/help/file-formats)包括 Markdown、Base、JSON Canvas、图片、音频、视频和 PDF，不包括普通 JSON。JSON 可以作为终端和程序读取的机器 artifact，但不能作为 Obsidian UI 的人读入口。

[Obsidian 设置](https://obsidian.md/help/settings)允许选择最短路径、相对路径或 vault 绝对路径，也允许选择 Wikilink 或 Markdown link。项目需要跨目录生成确定目标，因此选择 vault 根路径 Wikilink，不依赖当前文件位置或最短路径消歧。

小写 kebab-case 不是 Obsidian 强制规则，而是本项目经人批准的文件合同选择。依据是现行正式 ID 已经使用小写 ASCII 与连字符，858 个生成文件已采用该形状，并且统一小写路径可以避免两个生成器继续产生大小写分叉。人的显示名称继续由 H1、label、title 和 alias 承担，不由路径大小写承担。

## 命名范围

规则只约束项目生成、管理或稳定引用的路径，不限制使用者在 `inbox/`、`sources/`、`indexes/` 和 `attachments/` 中自行建立的普通文件名。`content/` 文件继续由应用生成 UUIDv4，使用者不能自行命名。

| 对象 | 路径规则 | 示例 |
|---|---|---|
| 项目目录 | 小写 kebab-case | `app/`、`kb/`、`sources/references/` |
| 正式对象 | 稳定 ID 加 `.md` | `kb/topics/machine-learning.md` |
| 内容单元 | 小写标准 UUIDv4 加 `.md` | `content/<uuidv4>.md` |
| Base | 小写 kebab-case 加 `.base` | `kb/views/topics.base` |
| 人读报告 | 小写 kebab-case 加 `.md` | `app/reports/topic-usage.md` |
| 机器报告 | 与人读报告同 stem，加 `.json` | `app/reports/data/topic-usage.json` |
| 目录入口 | 固定 `index.md` | `app/reports/index.md` |
| 根入口 | 固定 `home.md` | `home.md` |
| Obsidian 配置 | 产品固定名称 | `.obsidian/` |
| Codex 规则 | 产品固定名称 | `AGENTS.md` |

除 `.obsidian` 与未来另经批准建立的根 `AGENTS.md` 外，项目控制路径不得包含大写 ASCII、空格、下划线、重复连字符、前后连字符或平台路径分隔差异。扩展名固定小写。

## 目标布局

```text
kb-vault/
├── home.md
├── inbox/
├── sources/
│   ├── clippings/
│   ├── references/
│   └── files/
├── content/
├── indexes/
├── attachments/
├── kb/
│   ├── topics/
│   ├── arrays/
│   ├── entities/
│   ├── sources/
│   ├── types/
│   ├── genres/
│   ├── forms/
│   └── views/
│       ├── topics.base
│       ├── entities.base
│       └── sources.base
├── app/
│   ├── templates/
│   │   ├── inbox.md
│   │   └── reference.md
│   ├── views/
│   ├── reports/
│   │   ├── index.md
│   │   ├── validation.md
│   │   ├── topic-usage.md
│   │   ├── topic-coverage.md
│   │   ├── unassigned-topics.md
│   │   └── data/
│   │       ├── validation.json
│   │       └── topic-usage.json
│   ├── rules/
│   │   └── index.md
│   └── manifest.json
└── .obsidian/
```

根 `AGENTS.md` 属于已批准方向但尚未批准生效的终端访问规格。本次文件合同为其保留大写例外；是否在本次实施建立该文件，仍由终端访问规格的书面审阅决定，不能被命名修正顺带激活。

## 链接规则

全部项目生成的 vault 内部导航与正式引用使用 vault 根路径 Wikilink：

```md
[[app/reports/validation|内容校验]]
[[app/views/content.base|全部内容]]
[[kb/topics/machine-learning|机器学习]]
[[content/<uuidv4>|内容标题]]
```

规则如下：

- Markdown 目标省略 `.md`；
- Base 与其他 Obsidian 支持的非 Markdown 格式保留扩展名；
- 显示文本位于 `|` 后，不参与目标解析；
- 外部 `https://` 来源继续使用 Markdown link；
- JSON、manifest 和其他不受 Obsidian UI 支持的文件不得出现在人读导航中；
- 生成器不得混用相对路径、最短路径和 vault 根路径；
- link graph 已解析不能替代目标格式允许检查；
- 自动校验必须同时检查语法、路径、目标存在、目标种类和 UI 格式资格。

## 报告分层

报告同时服务 Obsidian 使用者和终端程序，必须分开表示而不是让一个 JSON 文件承担两种职责。

| 事实 | 人读表示 | 机器表示 |
|---|---|---|
| 内容校验 | `app/reports/validation.md` | `app/reports/data/validation.json` |
| 主题使用 | `app/reports/topic-usage.md` | `app/reports/data/topic-usage.json` |
| 主题覆盖 | `app/reports/topic-coverage.md` | 可由主题使用 JSON 重算，不新增 JSON |
| 主题复核 | `app/reports/unassigned-topics.md` | 可由主题使用 JSON 重算，不新增 JSON |

`app/reports/index.md` 只链接四份人读 Markdown，不链接 `data/`。JSON 继续使用确定 UTF-8、排序键、两空格缩进、LF 和末尾换行；Markdown 必须完整呈现对应结论、数据来源、派生边界和人工复核说明。

整个 `app/reports/` 继续作为一次原子替换的报告集合。把 `data/` 放在该目录内，避免人读和机器表示跨两个目录出现不同版本。

## 生成边界

`kb-design` 继续拥有正式对象 ID、字段、关系与表示选择；其 Obsidian exporter 改为生成小写 `kb/` 布局和小写 Base 路径。`kb-obsidian` 消费该导出，并生成小写用户区域、应用区域、配置与报告。

两个仓库都必须把同一目标布局写成显式常量与验证规则，但不能复制互相矛盾的说明。`kb-design` 的正式 target 文档是规范源；`kb-obsidian` 的 `AGENTS.md` 与 README 只摘要实现职责。manifest 保存修正后的精确路径与 hashes，旧大小写路径不得作为兼容别名同时生成。

本次是合同替换，不保留新旧双写，不生成大小写重复目录，不建立符号链接，不让 Obsidian 自动更新链接承担迁移正确性。

## 迁移方式

现有持久 `kb-vault` 不做逐文件原地改名。实施按以下方式切换：

1. 在切换前重新盘点用户写集；
2. 若 `inbox/`、`sources/`、`content/`、`indexes/` 或 `attachments/` 出现用户文件，停止自动切换并生成迁移清单；
3. 若用户写集仍为空，在同一父目录生成一个完整候选 vault；
4. 对候选运行 manifest、命名、链接、支持格式、Base、CLI、内容建立、校验和报告验收；
5. 保留旧 vault 为可恢复备份，不递归删除；
6. 在 Obsidian 未写入目标时切换目录，并重新登记或打开 vault；
7. 验证 UI 入口、CLI vault 路径和新建内容后，才把旧 vault 标记为可清理对象；
8. 删除备份必须由人另行明确批准。

`.obsidian/` 是用户配置边界。候选 vault 从修正后的初始化器生成最低配置；旧 workspace、appearance 或其他个人状态不自动复制。需要保留时先列出差异，由人选择具体文件。

## 验收门禁

只保留能发现高风险失败的检查：

- 所有项目控制目录与文件符合命名矩阵，例外集合精确；
- 不存在仅大小写不同的路径对；
- 生成 Markdown 的内部入口全部使用 vault 根路径 Wikilink；
- 人读入口不链接 JSON 或其他不支持格式；
- `obsidian links` 无悬空目标；
- `obsidian open` 打开每个人读入口后产生对应 Markdown 或 Base 视图，不出现空标签页；
- 四份人读报告与两份 JSON 使用同一次输入，计数与 issue 身份一致；
- `app/reports/` 原子发布失败保留旧集合；
- manifest 双向覆盖修正后的 managed 写集；
- `kb-obsidian new-content` 在小写 `content/` 建立 UUIDv4 文件，校验、报告和 CLI 使用同一路径；
- `kb-design` 与 `kb-obsidian` 的完整回归在风险阶段边界通过；
- 持久 vault 切换前后用户写集 bytes 不被覆盖、移动或删除。

不为常量回显、固定文件存在、重复计数或已由 manifest、命名 validator、链接 validator 和端到端验收覆盖的事实另造测试。机械事实由命令证明，不交给第二代理重复复核。

## 影响范围

实施计划至少覆盖：

- `kb-design/design/targets/obsidian.md` 的文件布局、链接、报告和 artifact contract 相关整节重写；
- `kb-design/scripts/export_obsidian.py` 及其高价值回归；
- `kb-obsidian` 的 managed、vault、reference export、content、validation、reports、CLI 与 README；
- 两个仓库中所有绑定旧大小写路径的测试和示例；
- 2026-09-03 终端访问规格中的路径与命令同步；
- disposable vault 和持久 `kb-vault` 的分阶段验收。

本规格不改变正式概念、designation、词表 ID、内容字段语义、决策权、来源结论或术语状态，也不引入插件、MCP、语义索引、自动分类、回流和非空 vault 通用更新能力。
