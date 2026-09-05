# 项目架构 (Project Architecture)

本项目维护知识体系的设计、词表和配套程序，提供工作区词表的实时预览，并通过 Obsidian 应用建立可使用的知识库。这些内容放在同一个 Git 仓库中，按 monorepo 组织；Python 工程使用 uv 管理。

## 文件组织

下面列出主要目录和文件。`output/` 与 `build/` 是运行时按需创建的目录，不进入 Git。

```text
kb-design/
├── README.md                  # 保留的项目原始说明，禁止 AI 修改
├── ARCHITECTURE.md            # 项目组织、文件树与工程关系
├── AGENTS.md                  # AI 的工作规则
├── pyproject.toml            # uv 工作区与共用开发配置
├── uv.lock                   # Python 依赖锁定
├── .python-version           # 开发使用的 Python 版本
├── .gitignore                # 不进入 Git 的文件与目录
│
├── docs/                     # 知识体系的说明与设计
│   ├── README.md             # 文档导航
│   ├── glossary.md           # 现行术语登记与中英对照
│   ├── concepts/             # 概念与方法的解释
│   ├── design/
│   │   ├── model/            # 内容模型、词表结构、关系与版本
│   │   ├── governance/       # 治理、写作与维护规则
│   │   └── targets/          # 各应用怎样表示和使用这些知识
│   ├── decisions/            # 已采纳的决定
│   ├── drafts/               # 尚未生效的设计
│   ├── references/           # 标准与文献的阅读记录
│   └── guides/               # 开发和操作指南
│
├── data/
│   ├── vocab/                # 正式词表与变更记录
│   ├── inputs/
│   │   ├── topics/           # 生成主题词表所需的输入
│   │   └── terminology/      # 尚未启用的术语生成配置
│   └── audit/
│       ├── labels/           # 译名回查与复核记录
│       ├── migrations/       # 数据迁移账本
│       └── maintenance/      # 维护记录与指标
│
├── schemas/                  # 供程序校验数据结构的规则
│
├── packages/
│   └── kb-core/              # 应用无关的数据处理程序
│       ├── README.md         # 核心程序的使用说明
│       ├── pyproject.toml    # 包依赖与命令入口
│       ├── src/kb_core/      # 生成、校验和维护代码
│       └── tests/            # 核心程序的测试
│
├── apps/
│   ├── obsidian/             # Obsidian 应用程序
│   │   ├── README.md         # 应用的使用说明
│   │   ├── AGENTS.md         # 应用开发的补充规则
│   │   ├── pyproject.toml    # 应用依赖与命令入口
│   │   ├── src/kb_obsidian/  # 导出、初始化、刷新及内容操作
│   │   └── tests/            # 应用测试
│   └── vocab-preview/        # 只读实时词表预览
│       ├── README.md         # 启动和维护说明
│       ├── pyproject.toml    # 应用依赖与命令入口
│       ├── src/kb_vocab_preview/ # 本地服务与页面模板
│       └── tests/            # 更新、恢复和只读边界测试
│
├── tests/
│   ├── integration/          # 核心程序与应用的联合测试
│   └── fixtures/             # 共用测试数据与冻结证据
│
├── scripts/                  # 整仓辅助脚本
├── work/
│   ├── roadmap.md            # 当前进度与后续工作
│   ├── plans/                # 实施计划
│   ├── reviews/              # 审查与验收记录
│   └── archive/              # 历史过程材料
│
├── output/                   # 持久应用产物，Git 忽略
│   └── obsidian/             # 默认的实际 Obsidian vault
└── build/                    # 可清理的临时产物，Git 忽略
```

## 工程关系

工作区包括核心包、Obsidian 应用和词表预览应用。各工程分别保存源码、依赖声明和测试，共用根目录的 uv 工作区与锁文件。

核心包负责词表生成、数据校验和来源、术语维护。Obsidian 应用依赖核心包，复用语言依据处理和仓库定位能力，自己负责 Markdown、Properties、Base 等具体表示，以及 vault 的初始化、刷新和内容操作。词表预览应用读取当前工作区，负责浏览、搜索与关系展示。两个应用均依赖核心包，核心包不依赖具体应用。

[内容模型](docs/design/model/content-model.md)规定应用无关的内容结构；[Obsidian 映射](docs/design/targets/obsidian.md)规定这些内容和词表怎样在 Obsidian 中表示；应用程序按该设计生成文件。具体命令与环境配置见[开发指南](docs/guides/development.md)。

## 数据与输出

正式词表位于 `data/vocab/`。其中，`topics.yaml` 由主题生成输入和核心程序共同生成；修改其输入或生成实现后，需要重建并校验。其他正式词表按各自规则直接维护。[术语表](docs/glossary.md)仍是术语登记与中英对照的现行编辑源，`data/inputs/terminology/` 中的配置尚未启用。

Obsidian 应用读取选定仓库的干净 Git 快照，把正式词表生成到 vault 的参考区，并提供笔记建立、内容校验与报告功能。默认 vault 位于该仓库的 `output/obsidian/`；初始化可用 `--output` 指定其他位置，后续操作可用 `--vault` 指定既有实例，也支持仓库外路径。`--design-root` 用于选择设计来源。

vault 中的笔记是用户内容；生成的词表参考区是项目数据的应用表示。刷新只更新参考区 `kb/` 与 `app/manifest.json`，保留用户内容与配置。对生成文件的修改不回流到正式词表，也不取得项目效力。

`output/` 保存持久应用数据，不参与构建清理；`build/` 保存可以重新生成和清理的临时文件。

词表预览通过本地 HTTP 服务读取工作区，包括尚未提交的修改。保存后页面自动重载，错误时保留上一次有效表示并提示；它不修改词表，也不生成需要人工刷新的静态文件。该用途与 Obsidian 的已提交快照导出分开，见[预览设计](docs/design/targets/vocab-preview.md)。

从仓库根目录启动预览：

```bash
uv run kb-vocab-preview
```

浏览器访问 <http://127.0.0.1:8765>，在运行命令的终端按 `Ctrl+C` 停止。服务已经运行时直接访问页面即可；其他端口与维护方式见[预览说明](apps/vocab-preview/README.md)。

## 维护入口

| 工作 | 入口 |
|---|---|
| 阅读概念与设计 | [文档导航](docs/README.md) |
| 修改主题词表 | [主题生成与校验规则](docs/design/model/topics.md) |
| 实时预览词表 | [预览说明](apps/vocab-preview/README.md) |
| 开发核心程序 | [核心工程说明](packages/kb-core/README.md) |
| 使用或开发 Obsidian 应用 | [应用说明](apps/obsidian/README.md) |
| 查看当前工作与后续安排 | [项目路线](work/roadmap.md) |

审计记录和历史计划保留追溯用途；草案、schema、程序或产物的存在不代表正式生效、消费者激活或发版。具体边界由[当前阶段](docs/decisions/current-stage-scope.md)和[仓库布局](docs/decisions/monorepo-layout.md)规定。
