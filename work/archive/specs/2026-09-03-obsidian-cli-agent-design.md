# 终端访问

## 设计状态

本规格记录 Obsidian 原生命令行接口作为终端中 AI 的应用入口。它是待人审阅的实施规格，不修改现行正式设计，不使新的消费者、回流、自动分类或写入权限生效。

文件合同已将项目控制路径统一为小写 kebab-case。终端访问只消费这一合同；历史 vault 的旧路径不能作为新生成物的兼容输入。持久 vault 的切换、根 `AGENTS.md` 的建立与终端规格的正式生效仍各自需要书面审阅，不因本规格同步而自动发生。

## 问题范围

`kb-vault` 包含正式词表表示、用户内容区、应用视图和报告。终端中的 AI 需要快速查找正式主题、读取概念上下文并管理授权的用户内容；直接扫描全部 Markdown 会消耗不必要的上下文，直接以文件系统写入又会绕过 UUID、必填字段、受控引用、manifest 和决策权。

目标是复用 Obsidian 已提供并在本机运行的 CLI，不建立第二套检索引擎、索引格式或远程接口。项目路径、内部链接和报告表示以 [文件合同修正](2026-09-03-obsidian-file-contract-repair-design.md) 为准。

## 依据边界

[Obsidian CLI 官方说明](https://obsidian.md/help/cli)把 CLI 定义为脚本、自动化和外部工具控制 Obsidian 的命令行接口，提供 vault 定位、搜索、上下文搜索、文件读取、properties、links、backlinks、Bases 查询和文件操作。官方要求使用 Obsidian 1.12.7 或更新 installer；CLI 连接运行中的 Obsidian，应用未运行时首条命令会启动应用。

2026-09-03 在本机 Obsidian 1.13.7 与 `/Users/xiu/code/kb-vault` 上完成只读验证：

- `obsidian version` 返回 `1.13.7 (installer 1.13.7)`；
- `obsidian vaults verbose` 正确登记 `kb-vault` 及其绝对路径；
- 主题目录的 `files` 返回 700；
- `search:context` 同时命中文件名、property 和正文范围；
- `read`、`property:read`、`backlinks` 与 `base:query` 返回可解析结果；
- 100 次上下文搜索的中位数为 6.6 ms、P95 为 8.8 ms；100 次单文件读取的中位数为 4.5 ms、P95 为 5.3 ms；五次 700 行 Base 查询的中位数为 15.7 ms，但一次输出约 167 KB。

这些观察证明已运行 Obsidian 的 CLI 协议和本机热路径；它们不证明历史 vault 已符合本次小写文件合同。候选 vault 必须以 `kb/topics/`、`content/`、`app/` 和报告分层重新验收。

一次无超时的长混合基准出现单次 `read` 挂起，后续 200 次带 2 秒超时的搜索和读取没有复现。因此上述数字只证明应用已运行且 vault 已加载时的本机热路径，不证明冷启动、其他平台、并发或无限等待安全。

## 方案选择

Obsidian CLI 是终端 AI 的首选读取、搜索和 Obsidian 状态接口。`kb-obsidian` 继续负责受内容模型约束的建立、校验和报告。`kb-design` 继续负责正式词表编辑、治理和发版。

当前不采用 Copilot、Smart Connections、Local REST API、MCP、向量数据库或自建检索器。若原生搜索在真实内容中出现可复现的召回失败，再以该失败、查询和期望目标为依据另行评估语义检索；不能仅因存在插件而建立依赖。

## 职责分层

| 职责 | 接口 | 当前边界 |
|---|---|---|
| vault、文件和工作区状态 | Obsidian CLI | 读取 Obsidian 当前解析结果；不产生正式判断 |
| 关键词与上下文搜索 | `search`、`search:context` | 返回候选；排序和命中不是概念对应结论 |
| 结构读取 | `read`、`property:read`、`links`、`backlinks`、`outline` | 读取 label、scope、上位、数组和来源 |
| 结构化列表 | `base:query` | 只在需要确定集合时使用；不把全量结果默认送入 AI 上下文 |
| 普通用户材料 | Obsidian CLI | 只在授权的用户写集建立或追加，不取得正式内容身份 |
| 正式内容建立 | `kb-obsidian new-content` | 生成 UUIDv4，校验必填字段和受控引用后发布 |
| 内容与 vault 校验 | `kb-obsidian validate` | 只读报告，不自动修复或改状态 |
| 使用报告 | `kb-obsidian report` | 原子替换 `app/reports/`；人读 Markdown 只作人工复核线索，JSON 只供终端和程序读取 |
| 正式词表变更 | `kb-design` | 服从现行治理、维护、来源和发版规则 |

## 查找流程

AI 每次显式指定 `vault=kb-vault`，不依赖当前终端目录或活动 vault。官方语法把 `vault=<name>` 放在命令之前。

主题查找依次执行：

1. 使用 `search:context` 在 `kb/topics` 搜索使用者原词，JSON 结果上限为 10；
2. 无充分结果时，从原文提取已有中文、英文或来源中的 designation 再检索，不形成新 designation；
3. 读取不超过三个候选文件；
4. 读取候选的 `kb_id`、`kb_label`、`kb_status`、`kb_broader`、`kb_arrays`、`kb_source` 与“范围”；
5. 用 `backlinks` 检查下位入口，用 `links` 或数组文件检查相邻结构；
6. 返回候选、命中位置、范围证据和不确定性；没有充分覆盖时明确返回“未找到”，不强行选择最相近项。

示例：

```bash
obsidian vault=kb-vault search:context \
  query="向量数据库" path=kb/topics limit=10 format=json

obsidian vault=kb-vault read \
  path=kb/topics/semi-structured-and-unstructured-databases.md

obsidian vault=kb-vault property:read \
  name=kb_broader \
  path=kb/topics/semi-structured-and-unstructured-databases.md
```

文件名是检索信号之一，不是唯一入口。`content/<uuidv4>.md` 依靠 H1、`title`、`aliases`、正文和受控 properties 被发现；`kb/<collection>/<stable-id>.md` 的文件名继续承担正式对象稳定 ID。

## 输出合同

AI 的主题候选至少包括：

- vault 相对路径；
- `kb_id` 与现行 label；
- 命中的文件位置和原文；
- scope 覆盖判断；
- 上位、数组和来源；
- 可能匹配与可能不匹配的理由；
- 是否需要人工判断或词表维护。

搜索分数、文件名相似、正文共词、Backlinks 数量和 AI 判断都不能证明两个 designation 表示同一概念，也不能自动产生 `subject`、候选、关系或状态变化。

人读报告只从 `app/reports/index.md` 导航到 `validation.md`、`topic-usage.md`、`topic-coverage.md` 和 `unassigned-topics.md`。终端 AI 与程序可以读取 `app/reports/data/validation.json` 和 `app/reports/data/topic-usage.json`，但 JSON 不是 Obsidian UI 的人读入口；终端读取 JSON 也不替代读取对应 Markdown 的派生边界和人工复核说明。

## 写入边界

AI 默认只读取 `home.md`、`inbox/`、`sources/`、`content/`、`indexes/`、`kb/`、`app/rules/` 和人读 `app/reports/`。`.obsidian/`、附件 bytes、受管理模板、受管理视图和 manifest 只在相应诊断明确需要时读取，不能作为普通检索范围。默认写入只限 `inbox/`、`sources/`、`content/` 和 `indexes/`，且仍服从具体操作的决策权。

| 对象 | 允许接口 | 禁止事项 |
|---|---|---|
| `inbox/` | `create`、`append`、`read` | 不得把临时材料声明为正式内容或概念依据 |
| `sources/` | `create`、`append`、`read` | 不得因保存来源而批准来源资格、designation 或概念对应 |
| `indexes/` | `create`、`append`、`read` | 不得把人工索引反写为正式主题关系 |
| `content/` 新对象 | `kb-obsidian new-content` | 不得用 `obsidian create` 绕过 UUID 和必填字段 |
| `content/` 正文 | 经明确任务授权后使用 `append` 或整文件编辑，再运行校验 | 不得用 `prepend` 把内容放到 H1 之前；不得覆盖未知 bytes |
| `content/` properties | 当前只读 | 不得直接修改 `kb_*`、`title` 或 `aliases`；受治理更新接口尚未设计 |
| `kb/` | 只读 | 不得创建、修改、移动或删除；变更回到 `kb-design` |
| 受管理 `app/` | 只读 | 只有对应生成器可写；报告命令只写 `app/reports/` |
| `.obsidian/` | 只读，除非人明确要求配置变更 | 不得把个人配置作为正式模型或项目决定 |

`obsidian create overwrite`、`delete permanent`、`move`、`rename` 和 `property:remove` 默认禁止。删除、稳定路径变化、状态变化和受控字段变化必须取得现行决策权要求的批准，不能因 CLI 提供命令而降级权限。

## 代理入口

终端访问规格另行获批并实施时，才在 vault 根建立应用管理的 `AGENTS.md`，使 Codex 自动读取 vault 角色、命令顺序、写集、禁止操作和校验义务。它只摘要现行正式设计，不建立新政策；冲突时以 `kb-design` 正文和 `app/rules/index.md` 为准。

根 `AGENTS.md` 进入应用受管理 manifest。使用者内容、搜索结果和报告不能自动修改它。当前不复制 `CLAUDE.md`；其他 AI 若不能读取 `AGENTS.md`，由调用方显式提供同一规则入口，不复制多份可能漂移的正文。

## 运行约束

- 要求 Obsidian installer 1.12.7 以上；当前验证版本为 1.13.7；
- Obsidian CLI 依赖运行中的桌面应用；冷启动耗时尚未验证；
- 单次搜索、读取或 Base 查询使用 2 秒热路径超时；超时后只串行重试一次；
- 冷启动允许调用方给出更长的独立启动期限，不能把冷启动并入普通查询重试；
- AI 不并发轰击同一 Obsidian 实例；
- 默认结果上限为 10，默认读取候选不超过三个；
- 全量 Base 结果先在进程外筛选，不能把 700 行、约 167 KB 的结果直接作为普通提示上下文；
- JSON 输出必须解析成功后才能消费；混入警告、截断或非零退出码时不得继续写入；
- CLI 不可用时停止 Obsidian 状态相关操作，不自动改用未经校验的写入路径。

## 失败处理

| 失败 | 处理 |
|---|---|
| vault 未登记或路径不符 | 停止并报告 `vaults verbose` 结果，不猜测其他 vault |
| Obsidian 未运行 | 允许首条命令启动应用，等待独立冷启动期限后重试一次 |
| 查询超时 | 终止本次命令，串行重试一次；再次超时则报告，不无限等待 |
| JSON 不可解析 | 保存命令、退出码和 stderr，不把部分输出当作候选 |
| 无充分候选 | 材料保留在 `inbox/`，报告搜索词和检查过的候选 |
| 写后校验失败 | 不继续追加修改；保留失败证据并请求人工处置，不自动修复 |
| managed 漂移 | `kb-obsidian` 门禁阻断后续流程；回到正式生成路径，不在 vault 修补 |

## 验收范围

实施只保留以下高价值验证：

- 原生 CLI 能识别 `kb-vault` 并返回正确绝对路径；
- UUID 文件名不含查询词时，搜索仍能通过 H1、property 或正文找到内容；
- `search:context` 能从主题 scope 找到文件名不含原查询的候选；
- AI 从候选读取 ID、label、scope、上位、数组和来源，不把搜索命中当作概念结论；
- 根 `AGENTS.md` 获批建立后，被初始化器纳入受管理 manifest；
- `content/` 新建仍只能经过 `kb-obsidian new-content`；
- native CLI 对 disposable vault 的允许写入后，`kb-obsidian validate` 仍能发现结构漂移；
- 超时、非零退出、截断或不可解析输出不会触发后续写入；
- `kb/`、受管理 `app/`、manifest 和 `kb-design` hashes 在 AI 用户内容操作前后不变；
- 人读导航不打开 JSON，终端 JSON 读取只限 `app/reports/data/`，且与对应 Markdown 同属一次报告发布。

不为 CLI 帮助中的固定命令、常量回显、文件存在或已经由 manifest 覆盖的机械事实另造测试。首次实施不验证社区插件、MCP、语义向量、自动分类、正式词表回流或内容删除。

## 设计影响

本规格获批后，实施计划需要覆盖：

- 把 Obsidian CLI 终端入口与写入边界同步到 `design/targets/obsidian.md`；
- 在 `kb-obsidian` 初始化器中生成根 `AGENTS.md` 并纳入 manifest；
- 更新应用 README，提供 AI 的只读查找和受治理写入示例；
- 在 disposable vault 验证原生 CLI 的读取、允许写入、超时与校验组合；
- 在持久 `kb-vault` 重新初始化前只报告差异，不覆盖现有非空 vault；非空更新仍不在当前实现范围。

本规格不批准自动更新现有 vault。现有 `kb-vault` 的根 `AGENTS.md` 如何落地，必须在非空 vault 更新设计完成前由人选择人工建立、重建新 vault 或继续后置。
