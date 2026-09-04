# 维护基线

状态：只读基线，未执行编辑审核、来源内容复核、designation 准入、阈值校准或正式数据修改。

基线绑定 `feat/terminology-governance` 分支的 `9e7b411c23e890d13d70fc16d443b760313126c4`。核对日为 2026-08-31。本文只使用仓库现行数据、现行规则、已接受但未生效的两份治理草案和实际运行的只读脚本；没有引入新的外部事实，也没有猜测未读材料正文。

## 执行边界

- 现行规则仍由 `design/governance.md`、`design/maintenance.md`、`design/topics.md`、`design/entities.md` 和 `design/sources-registry.md` 决定。
- 来源治理和术语治理草案只提供拟议分类边界。本文引用草案已有的 `basis`、`source`、`match`、`discovery` 和术语工作流边界，不使草案生效。
- 字符串、目录、状态和次数只用于定位与排阅读顺序。本文不据此决定 designation 身份、概念对应、来源用途、归属或正式动作。
- `candidate` 分为实体记录状态、主题概念状态和来源旧角色三种现行语境；三者不得互相换算。当前主题概念没有 `candidate` 状态记录。
- `unassigned` 只统计主题词表中的复制概念。按术语治理草案，它不复制为术语概念工作流状态。
- `self` 只统计现行 `basis` 断言值。按来源治理草案，它不能机械改写为新的 `basis` 项。
- designation 扫描输出只是候选字符串线索。没有人的上下文判断时，不能把线索称为“未登记 designation”。

## 校验结果

以下命令均在仓库根目录实际运行，且没有使用会写入 `vocab/signals.yaml` 的 `--record`。

| 命令 | 结果 | 边界 |
|---|---|---|
| `python3 scripts/check-topics.py` | 退出码 0；0 处问题；700 个概念、24 个数组、61 个实体、31 个来源 | 校验正式词表结构并输出当前指标；不执行编辑审核 |
| `python3 scripts/check-terms.py --all` | 退出码 0；已登记 1242 个写法；298 个待人工判断字符串 | 报告文件集合，不保存同一文件内重复次数，不给 designation 结论 |
| `python3 -m unittest tests/test_check_terms.py` | 6 项测试通过 | 只验证候选识别器的现有行为 |
| `python3 scripts/check-links.py` | 退出码 1；2 处问题 | 两处均在既有 `.superpowers` 旧执行材料中，不是本任务写入；脚本只查相对链接，不查外部链接存活 |

两处链接问题为 `.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/agentic-plan.md:11` 的不存在文件，以及 `.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/human-decision-package.md:340` 的不存在锚点。它们不改变正式词表校验的 0 处问题结论。

## 数量总览

| 对象 | 当前数量 | 历史数量 | 分类 |
|---|---:|---:|---|
| 主题概念 | 700 | 700 | 数量 |
| `unassigned` 主题概念 | 692 | 692 | 数量 |
| `active` 主题概念 | 8 | 8 | 数量 |
| `candidate` 主题概念 | 0 | 未单列，按 700 减 692 与 8 为 0 | 数量 |
| 命名实体 | 61 | 57 | 数量 |
| `candidate` 命名实体 | 17 | 16 | 数量 |
| `active` 命名实体 | 44 | 41 | 数量 |
| `subjects: self` 命名实体 | 13/61 | 12/57 | 数量 |
| 来源登记 | 31 | 快照未记录 | 数量 |
| 旧 `candidate` 来源角色 | 5 | 快照未记录 | 数量 |
| 到期来源 | 0 | 0 | 数量 |
| 已登记写法 | 1242 | 快照未记录 | 数量 |
| 待人工判断字符串 | 298 个身份、326 个上下文位置、38 个文件 | 快照未记录 | 数量 |

唯一历史快照位于 `vocab/signals.yaml:4-14`，记录日为 2026-08-23。快照之后的四个实体是 `dita`、`iptc-genre`、`lom` 和 `schema-org`；前三个为 `active`，`schema-org` 为 `candidate` 且 `subjects: self`。这与实体总数增加 4、候选增加 1、`self` 增加 1 一致，只说明数据变化，不构成状态动作结论。

## 状态候选

当前 17 个状态候选全部位于 `vocab/entities.yaml`，主题词表中没有状态候选。位置指向记录起始行。

| 身份 | 位置 | 类别 | 当前主题 | `subjects` 依据 | 分类 | 证据说明 |
|---|---|---|---|---|---|---|
| `gbt-13745` | `vocab/entities.yaml:8` | `standard` | `library-and-information-science` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |
| `diataxis` | `vocab/entities.yaml:277` | `standard` | `software-engineering` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |
| `wikidata` | `vocab/entities.yaml:289` | `standard` | `library-and-information-science` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |
| `roadmap-sh` | `vocab/entities.yaml:301` | `standard` | `computing` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |
| `teachyourselfcs` | `vocab/entities.yaml:313` | `publication` | `computing` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |
| `schema-org` | `vocab/entities.yaml:389` | `standard` | `information-science` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |
| `anthropic` | `vocab/entities.yaml:404` | `organization` | `artificial-intelligence` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |
| `openai` | `vocab/entities.yaml:413` | `organization` | `artificial-intelligence` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |
| `moonshot-ai` | `vocab/entities.yaml:422` | `organization` | `artificial-intelligence` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |
| `astral` | `vocab/entities.yaml:431` | `organization` | `software-engineering` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |
| `codex` | `vocab/entities.yaml:452` | `software` | `artificial-intelligence`、`tools-and-environments` | `cs2023:SE-Tools#7` | 待人决定 | `subjects` 没有 `self`，但记录没有保存候选状态的审核次数和未通过原因，不能仅凭依据值自动转正 |
| `kimi-code` | `vocab/entities.yaml:474` | `software` | `artificial-intelligence`、`tools-and-environments` | `cs2023:SE-Tools#7` | 待人决定 | `subjects` 没有 `self`，但记录没有保存候选状态的审核次数和未通过原因，不能仅凭依据值自动转正 |
| `opencode` | `vocab/entities.yaml:495` | `software` | `artificial-intelligence`、`tools-and-environments` | `cs2023:SE-Tools#7` | 待人决定 | `subjects` 没有 `self`，但记录没有保存候选状态的审核次数和未通过原因，不能仅凭依据值自动转正 |
| `oxc` | `vocab/entities.yaml:559` | `software` | `tools-and-environments`、`web-platforms` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |
| `uv` | `vocab/entities.yaml:628` | `software` | `tools-and-environments` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |
| `ty` | `vocab/entities.yaml:649` | `software` | `tools-and-environments`、`type-systems` | `cs2023:SE-Tools#3`、`cs2023:FPL-Types#5` | 待人决定 | `subjects` 没有 `self`，但记录没有保存候选状态的审核次数和未通过原因，不能仅凭依据值自动转正 |
| `pydantic` | `vocab/entities.yaml:679` | `software` | `web-platforms`、`foundations-of-programming-languages` | `self` | 语义问题 | 记录有未核实归属断言，现行规则要求保持候选 |

状态候选身份序列 SHA-256 为 `943c88c963b0fff12a14f1b5d4a07ca3cf44222c75d33679e29ca175c7313873`。

## 来源候选

现行来源表有 5 个旧 `candidate` 角色。来源治理草案只允许其拟议迁移到 `discovery`，且不得顺带批准其他角色或把发现结果变成概念记录；草案未生效，因此当前不迁移。

| 身份 | 位置 | 实体 | 当前角色 | 草案拟议去向 | 分类 | 证据说明 |
|---|---|---|---|---|---|---|
| `mdn-curriculum` | `vocab/sources.yaml:72` | `mdn-curriculum` | `candidate` | `discovery` | 待人决定 | 只可在获准迁移批次中使用草案去向 |
| `roadmap-sh` | `vocab/sources.yaml:100` | `roadmap-sh` | `candidate` | `discovery` | 待人决定 | 只可在获准迁移批次中使用草案去向 |
| `teachyourselfcs` | `vocab/sources.yaml:104` | `teachyourselfcs` | `candidate` | `discovery` | 待人决定 | 只可在获准迁移批次中使用草案去向 |
| `cmu-15-445` | `vocab/sources.yaml:108` | `cmu-15-445` | `candidate` | `discovery` | 待人决定 | 只可在获准迁移批次中使用草案去向 |
| `db-engines` | `vocab/sources.yaml:112` | `db-engines` | `candidate` | `discovery` | 待人决定 | 只可在获准迁移批次中使用草案去向 |

## 未标引记录

692 个 `unassigned` 身份全部唯一。下表按顶层与实际 `source` 分组，位置给出该组第一个和最后一个记录的起始行；组内记录在文件中连续，每组另有按 `id@line` 计算的身份哈希。该定位既保留全部身份覆盖，又不把 692 个复制记录逐项解释为语义问题。

| 顶层 | 来源 | 数量 | 首项 | 末项 | 身份 SHA-256 | 分类 |
|---|---|---:|---|---|---|---|
| `computing` | `asvs` | 16 | `encoding-and-sanitization@2036` | `webrtc@2201` | `4564dd3588b416cd453ed964929dcc81b672ab1d7745ee902432d8a8657ac92e` | 数量 |
| `computing` | `atlas` | 16 | `reconnaissance-artificial-intelligence@2487` | `impact-artificial-intelligence@2652` | `06eaa45f32cf53b6c70a5d03837562d58f4aea6cfd2d4ecb8b76187373a31f20` | 数量 |
| `computing` | `attack` | 15 | `reconnaissance@2322` | `impact@2476` | `b51306ee431ad6b25d50862a6c20b3ea92968569660a4fb01bd99ef21a71cb59` | 数量 |
| `computing` | `cs2023` | 178 | `algorithmic-foundations@107` | `society-ethics-and-the-profession-systems-fundamentals@2025` | `b39d608901301c43998f03c9e1b1256c840d1a65eaffc90b82d16772f9e12291` | 数量 |
| `computing` | `cwe` | 10 | `improper-access-control@2212` | `improper-adherence-to-coding-standards@2311` | `db6ba92760bd14ab513529fdf0929164430cb8dbea056d422b1799e06a1edf35` | 数量 |
| `computing` | `owasp-llm-top10` | 10 | `prompt-injection@2663` | `unbounded-consumption@2753` | `da85382649dde172e5bb3bfc7c2ebc8fd4b71991aa6ff81f6e36b17557817e31` | 数量 |
| `computing` | `rfc-1122` | 4 | `application-layer@2939` | `link-layer@2972` | `12ae962789a967c61b375ad2bd7bc975ae770055d54410b0451977e4935e6509` | 数量 |
| `computing` | `swebok` | 16 | `software-requirements@2763` | `engineering-foundations@2928` | `6aa4a6120d9983b82bec7fb2b0a68b61674d127299457ea8a589685c27705ad4` | 数量 |
| `education` | `gbt-13745` | 18 | `history-of-education@6664` | `other-education@6817` | `f69eaec1722fcebca382f09e5d12e1496b64e422dc45440f5ca3d420f2f25a59` | 数量 |
| `information-and-systems-science` | `gbt-13745` | 25 | `foundations-of-information-and-systems-science@4486` | `other-information-and-systems-science@4702` | `1a83d4cdb6fae10fa578ebc23e89cb2780eb0325919018cb3e075a9645ba354c` | 数量 |
| `journalism-and-communication` | `gbt-13745` | 37 | `journalism-theory@5953` | `other-journalism-and-communication@6277` | `466f44a531a2bb561308199935b523b7b15e6e4f7685b4f78ec3cca75902e211` | 数量 |
| `library-and-information-science` | `gbt-13745` | 42 | `library-science@6286` | `museology@6655` | `ffbfc340db887f478186cdc0c7395e578c6ef5abddc41a4fdb81fda13998a28d` | 数量 |
| `linguistics` | `gbt-13745` | 83 | `general-linguistics@5206` | `other-linguistics@5944` | `2c64b57b33bcb39776379ee8d86e67bd5daa66d6d4a13ea23c423ede88307e57` | 数量 |
| `management` | `gbt-13745` | 55 | `history-of-management-thought@4711` | `other-management@5197` | `10b81a433ce2cf428cf4c08988ee78eecc757f4dd18e883cfeab1ccd7f798e96` | 数量 |
| `mathematics` | `gbt-13745` | 167 | `history-of-mathematics@2983` | `other@4477` | `5280c982e01dbcca06b8202c0ae842252566d82968eef5140f8a15dca7db81e7` | 数量 |

全部 `unassigned` 身份序列 SHA-256 为 `5c2f9655f113aa3967c02098451b4378efd70bbee03bdfd23292b20d900ab4bb`。八个顶层的数量与 2026-08-23 快照逐项相同，但只有一份已记录快照；本次只读运行不是第二次编辑审核，所以不触发“连续两次编辑审核无变化”。

## 断言现状

当前 `self` 只出现在 13 个命名实体的 `basis.subjects`。主题标签的 `basis.zh` 与 `basis.en` 均为 0/700 个 `self`。

| 身份 | 位置 | 当前主题 | 当前状态 | 分类 | 证据说明 |
|---|---|---|---|---|---|
| `gbt-13745` | `vocab/entities.yaml:8` | `library-and-information-science` | `candidate` | 语义问题 | `basis.subjects: self` |
| `diataxis` | `vocab/entities.yaml:277` | `software-engineering` | `candidate` | 语义问题 | `basis.subjects: self` |
| `wikidata` | `vocab/entities.yaml:289` | `library-and-information-science` | `candidate` | 语义问题 | `basis.subjects: self` |
| `roadmap-sh` | `vocab/entities.yaml:301` | `computing` | `candidate` | 语义问题 | `basis.subjects: self` |
| `teachyourselfcs` | `vocab/entities.yaml:313` | `computing` | `candidate` | 语义问题 | `basis.subjects: self` |
| `schema-org` | `vocab/entities.yaml:389` | `information-science` | `candidate` | 语义问题 | `basis.subjects: self` |
| `anthropic` | `vocab/entities.yaml:404` | `artificial-intelligence` | `candidate` | 语义问题 | `basis.subjects: self` |
| `openai` | `vocab/entities.yaml:413` | `artificial-intelligence` | `candidate` | 语义问题 | `basis.subjects: self` |
| `moonshot-ai` | `vocab/entities.yaml:422` | `artificial-intelligence` | `candidate` | 语义问题 | `basis.subjects: self` |
| `astral` | `vocab/entities.yaml:431` | `software-engineering` | `candidate` | 语义问题 | `basis.subjects: self` |
| `oxc` | `vocab/entities.yaml:559` | `tools-and-environments`、`web-platforms` | `candidate` | 语义问题 | `basis.subjects: self` |
| `uv` | `vocab/entities.yaml:628` | `tools-and-environments` | `candidate` | 语义问题 | `basis.subjects: self` |
| `pydantic` | `vocab/entities.yaml:679` | `web-platforms`、`foundations-of-programming-languages` | `candidate` | 语义问题 | `basis.subjects: self` |

这些断言按主题聚合的最大值是 `artificial-intelligence` 下 3 个；`library-and-information-science`、`software-engineering`、`computing`、`tools-and-environments` 和 `web-platforms` 各 2 个；`information-science` 与 `foundations-of-programming-languages` 各 1 个。没有节点达到 5。身份序列 SHA-256 为 `28a5562cdb8292c8a5d8f9add62f17b0ed09e6dddc5a2f9117cf1a42c521b08e`。

## 来源复核

下表逐项列出 31 个来源登记及其实体位置。现行脚本按实体 `tier` 和实体 `checked` 计算到期；来源表自身的 `checked` 同为 2026-08-23。核对日与这些日期仍在同一个月，非 archival 来源均未到期；archival 按现行表不复核内容。

| 来源 | 来源位置 | 实体位置 | 档位 | 实体核对日 | 当前结果 | 分类 |
|---|---|---|---|---|---|---|
| `gbt-13745` | `vocab/sources.yaml:8` | `vocab/entities.yaml:8` | `de-jure` | 2026-08-23 | 0/24 月，未到期 | 数量 |
| `cs2023` | `vocab/sources.yaml:12` | `vocab/entities.yaml:21` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `swebok` | `vocab/sources.yaml:16` | `vocab/entities.yaml:34` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `acm-ccs` | `vocab/sources.yaml:20` | `vocab/entities.yaml:47` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `asvs` | `vocab/sources.yaml:24` | `vocab/entities.yaml:59` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `cwe` | `vocab/sources.yaml:28` | `vocab/entities.yaml:72` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `attack` | `vocab/sources.yaml:32` | `vocab/entities.yaml:85` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `owasp-top10` | `vocab/sources.yaml:36` | `vocab/entities.yaml:98` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `owasp-llm-top10` | `vocab/sources.yaml:40` | `vocab/entities.yaml:111` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `atlas` | `vocab/sources.yaml:44` | `vocab/entities.yaml:124` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `nist-ai-rmf` | `vocab/sources.yaml:48` | `vocab/entities.yaml:137` | `de-jure` | 2026-08-23 | 0/24 月，未到期 | 数量 |
| `anthropic-docs` | `vocab/sources.yaml:52` | `vocab/entities.yaml:150` | `vendor` | 2026-08-23 | 0/6 月，未到期 | 数量 |
| `rfc-1122` | `vocab/sources.yaml:56` | `vocab/entities.yaml:162` | `de-jure` | 2026-08-23 | 0/24 月，未到期 | 数量 |
| `rfc-9110` | `vocab/sources.yaml:60` | `vocab/entities.yaml:175` | `de-jure` | 2026-08-23 | 0/24 月，未到期 | 数量 |
| `osi` | `vocab/sources.yaml:64` | `vocab/entities.yaml:188` | `de-jure` | 2026-08-23 | 0/24 月，未到期 | 数量 |
| `mdn` | `vocab/sources.yaml:68` | `vocab/entities.yaml:201` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `mdn-curriculum` | `vocab/sources.yaml:72` | `vocab/entities.yaml:213` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `iso-25964-1` | `vocab/sources.yaml:76` | `vocab/entities.yaml:225` | `de-jure` | 2026-08-23 | 0/24 月，未到期 | 数量 |
| `iso-25964-2` | `vocab/sources.yaml:80` | `vocab/entities.yaml:238` | `de-jure` | 2026-08-23 | 0/24 月，未到期 | 数量 |
| `z39-19` | `vocab/sources.yaml:84` | `vocab/entities.yaml:251` | `de-jure` | 2026-08-23 | 0/24 月，未到期 | 数量 |
| `skos` | `vocab/sources.yaml:88` | `vocab/entities.yaml:264` | `de-jure` | 2026-08-23 | 0/24 月，未到期 | 数量 |
| `diataxis` | `vocab/sources.yaml:92` | `vocab/entities.yaml:277` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `wikidata` | `vocab/sources.yaml:96` | `vocab/entities.yaml:289` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `roadmap-sh` | `vocab/sources.yaml:100` | `vocab/entities.yaml:301` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `teachyourselfcs` | `vocab/sources.yaml:104` | `vocab/entities.yaml:313` | `archival` | 2026-08-23 | 不复核内容 | 数量 |
| `cmu-15-445` | `vocab/sources.yaml:108` | `vocab/entities.yaml:325` | `archival` | 2026-08-23 | 不复核内容 | 数量 |
| `db-engines` | `vocab/sources.yaml:112` | `vocab/entities.yaml:337` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `dita` | `vocab/sources.yaml:116` | `vocab/entities.yaml:350` | `de-jure` | 2026-08-23 | 0/24 月，未到期 | 数量 |
| `iptc-genre` | `vocab/sources.yaml:120` | `vocab/entities.yaml:363` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |
| `lom` | `vocab/sources.yaml:124` | `vocab/entities.yaml:376` | `de-jure` | 2026-08-23 | 0/24 月，未到期 | 数量 |
| `schema-org` | `vocab/sources.yaml:128` | `vocab/entities.yaml:389` | `de-facto` | 2026-08-23 | 0/12 月，未到期 | 数量 |

来源身份序列 SHA-256 为 `34cd583e4a3d83d36d5617467842870f21fe17e9951d72ef1f835827cd69c6a0`。当前只计算日程，没有联网探测来源内容、版本、替代、撤回或链接存活；现行维护文档明确说明相应探测脚本待写，因此“0 个到期”不能解释为“31 个来源内容均已实时复核”。

## 名称线索

候选识别器报告 298 个未匹配写法。按同一抽取规则逐项重放并打开命中行，得到 326 个上下文位置，分布为标题 201、加粗 41、中文引号 84，共 38 个文件。

这些数只能作数量基线。当前可确认的 designation 结论为 0 个；298 个身份全部保持“待人决定”。其中 15 个是带英文括注的文章标题被正则截去右括号后的字符串，7 个截去括注后的中文基础形式已经登记。这是候选识别器的机械噪声，不是未登记 designation 证据。脚本还把同一文件的重复命中折叠为文件集合，因此现有正式输出不能提供维护规则要求的“总出现次数”；326 是本次按同一抽取位置只读重放得到的上下文数，不是新的正式指标字段。

候选字符串身份与文件集合 SHA-256 为 `95daf65cee4ae9e10af99c03b39eefae9c49d27e97c61eff3d9e7cbf8422e2c2`。逐项位置见“名称附录”。

## 阈值触发

| 现行指标 | 当前值 | 阈值 | 结果 | 分类 | 证据或边界 |
|---|---|---|---|---|---|
| `unassigned` 转 `active` | 引用次数不可得 | 1 次或有下位 | 不可判定 | 待人决定 | 首个应用映射未落地，现行规则规定引用次数不触发 |
| `candidate` 转 `active` | 引用次数、`scope` 审核四问和审核历史未形成统一输入 | ≥ 3 次并满足其余门禁 | 不可判定 | 待人决定 | 不能从 17 个状态或 4 个非 `self` 候选直接批准 |
| 状态候选删除资格 | 连续审核引用次数不可得 | 0 次且连续两次编辑审核 | 不可判定 | 待人决定 | 只有一份指标快照，且没有应用引用计数 |
| 编辑审核数量触发 | 17 | ≥ 20 | 未触发 | 数量 | 当前少 3 个 |
| 编辑审核时间触发 | `last_candidate_review: null` | 满 12 个月 | 不可判定 | 待人决定 | 没有起算日期；脚本未实现该条件 |
| 节点下 `self` | 最大 3 | ≥ 5 | 未触发 | 数量 | `artificial-intelligence` 为 3 |
| 节点下状态候选 | 主题概念为 0 | ≥ 5 | 未触发 | 数量 | 现行脚本只统计主题概念候选，不统计实体候选 |
| “其他”类目下位 | 脚本识别的直接下位计数均为 0 | ≥ 3 | 未触发 | 数量 | 只按中文标签以“其他学科”结尾识别 |
| 顶层未标引长期不变 | 当前值与唯一快照相同 | 连续两次编辑审核无变化 | 未触发 | 数量 | 当前运行未记录为第二次编辑审核 |
| 来源定期复核 | 0 个到期 | 按档位 24、12、6 月 | 未触发 | 数量 | archival 不复核内容 |
| 来源新版事件 | 未运行联网探测 | 发布新版 | 不可判定 | 待人决定 | 新版探测脚本待写 |
| 外部链接存活 | 未运行外部链接存活检查 | 3 个月 | 不可判定 | 待人决定 | `check-links.py` 只查仓库相对链接 |
| 过度使用概念 | 内容引用总数不可得 | 单概念占全部引用 ≥ 10% | 不可判定 | 待人决定 | 首个应用映射未落地 |
| 治理年审 | `governance_reviewed: null` | 12 个月 | 不可判定 | 待人决定 | 没有起算日期，脚本也不独立显示该空值 |
| 首轮阈值校准 | 首轮维护尚未登记完成 | 首次编辑审核完成后 | 等待人工决定 | 待人决定 | 所有标“本库”的数字须由人校准，本文不改阈值 |

本次没有可据现行数据直接执行的正式动作。未触发不等于问题已解决；不可判定项缺少应用映射、审核日期、探测器或人的语义判断。

## 历史指标

| 指标 | 2026-08-23 快照 | 2026-08-31 只读值 | 变化 | 解释边界 |
|---|---:|---:|---:|---|
| `candidates` | 16 | 17 | +1 | 快照后增加 `schema-org` 候选；本次不写快照 |
| `self.entities.subjects` | 12/57 | 13/61 | +1/+4 | 快照后增加四个实体，其中 `schema-org` 为 `self` |
| `unassigned.computing` | 265/266 | 265/266 | 0 | 只有一份已记录快照，不构成连续两次审核 |
| `unassigned.education` | 18/19 | 18/19 | 0 | 同上 |
| `unassigned.information-and-systems-science` | 25/26 | 25/26 | 0 | 同上 |
| `unassigned.journalism-and-communication` | 37/38 | 37/38 | 0 | 同上 |
| `unassigned.library-and-information-science` | 42/43 | 42/43 | 0 | 同上 |
| `unassigned.linguistics` | 83/84 | 83/84 | 0 | 同上 |
| `unassigned.management` | 55/56 | 55/56 | 0 | 同上 |
| `unassigned.mathematics` | 167/168 | 167/168 | 0 | 同上 |
| `last_candidate_review` | `null` | `null` | 0 | 没有编辑审核起算日 |
| `governance_reviewed` | `null` | `null` | 0 | 没有治理年审起算日 |

## 语义问题

- `check-topics.py` 读取历史快照时用内部键计算未标引触发，却用显示名称查找“上次值”，所以八行均显示“—”。触发计算本身使用了正确键；显示仍不能作为历史值证据。
- 脚本没有实现编辑审核的 12 个月条件、候选经过的审核次数、候选删除资格、引用驱动转正、过度使用、治理年审空值提示、外部链接存活和来源新版探测。
- 17 个实体候选中有 4 个 `subjects` 已非 `self`，但现行记录没有候选审核次数和保持候选的理由。状态不能靠字段缺失反推，也不能机械转正。
- 候选字符串输出按文件集合去重，不能给出同一文件内的总出现次数；标题正则还会截断英文括注，造成至少 15 个标题形态噪声。
- 31 个来源的“到期 0”只说明按当前日期和档位周期未到期，不说明内容、版本、替代、撤回或地址已经实时核验。
- 现行 `basis: self` 与草案 `basis` 结构语义不同。迁移前必须逐项分类、补证或保持未获准，不能把字符串 `self` 自动包装为草案字段。

## 人工决定

- 决定何时完成第一次编辑审核，并给 `last_candidate_review` 建立可审计起算点；本报告不把只读运行冒充编辑审核。
- 首轮编辑审核完成后，逐项校准现行阈值表中标为“本库”的数字；阈值变更按现行权限提案，由人决定。
- 对 298 个候选字符串逐项判断当前上下文是否确实把它用作可复用项目概念名称。只有被人判为拟用 designation 的项目，才进入现行准入阶梯；其余标题、普通叙述、来源转录和示例不登记。
- 对 4 个非 `self` 的状态候选分别核对其保持候选的原因和审核门禁；不因 `basis` 有来源便自动批准。
- 对 13 个 `self` 归属断言逐项核对来源文字。归属判断仍是二级事项；不能用长期存在或聚集数量代替语义依据。
- 旧来源 `candidate` 角色是否在来源治理草案生效后的获准迁移批次转为 `discovery`，保持相应生效与迁移门禁。
- 应用映射、外部链接存活检查、新版探测器和正式审核记录位置未形成前，引用次数、过度使用、删除资格和事件触发继续标为不可判定。

## 身份校验

| 集合 | 行数 | 重复身份 | 空身份 | 状态或角色值域 |
|---|---:|---:|---:|---|
| `vocab/topics.yaml` 概念 | 700 | 0 | 0 | `active` 8、`unassigned` 692；均在现行值域 |
| `vocab/entities.yaml` 实体 | 61 | 0 | 0 | `active` 44、`candidate` 17；均在现行值域 |
| `vocab/sources.yaml` 来源 | 31 | 0 | 0 | `mapping` 26、`structure` 13、`group` 3、`candidate` 5；均在现行值域 |
| 状态候选库存 | 17 | 0 | 0 | 全部能回到实体记录 |
| `unassigned` 库存 | 692 | 0 | 0 | 全部能回到主题概念记录 |
| `self` 库存 | 13 | 0 | 0 | 全部能回到实体 `basis.subjects` |
| 来源复核库存 | 31 | 0 | 0 | 全部能回到来源和实体记录 |
| 名称线索库存 | 298 | 0 | 0 | 全部保持“待人决定”，未写 designation 结论 |

本文各 Markdown 表格没有空单元格。分类列只使用“数量”“语义问题”“待人决定”。草案拟议去向只使用草案已有的 `discovery`；没有新建字段、schema、ID、周期、阈值、范围或来源档位。

## 输入哈希

| 输入 | SHA-256 |
|---|---|
| `AGENTS.md` | `ff6bd1a063bdf45010986febfb944943520a8c64188e47e0e469087808b740b5` |
| 实施准备计划 | `28b936359d49f5c8618d2dff63740497a766da43931fa4f47b7ad6dd9c232ecd` |
| 来源治理草案 | `0bc61207215f35065652bb66f043ef2d11a807bbe0bc44465814e469b5671526` |
| 术语治理草案 | `2d48c869b8a2119346739303accaaff0cbe40418d7074f29a4a18599950767d7` |
| `design/maintenance.md` | `d2c6addd7c55a034a5c554c32b63bf6cff0ccc4e741d6ed06d3e66d820f88aa5` |
| `design/governance.md` | `cf7b97872df8486dfb6fab40e3de7478b7ea2265e6242c3b484c39cd256bd01c` |
| `design/topics.md` | `2a2e5cc17dbc2b310c9705722f8137de4623078afb0e0bd9db042583c52b59b4` |
| `design/entities.md` | `8e5541984d502606fa9d2a9b74bb2499749abc908dff3779f83119998c766ecc` |
| `design/sources-registry.md` | `29994bef02cfa101924fc0bbcf6247be7c844d6e9338fdb42b20cd490c92a21b` |
| `concepts/glossary.md` | `7d60a1da6ec8257115eb1fb0b09059504b867f8c167dfcc639a95d48ff572d39` |
| `scripts/check-topics.py` | `a2c4bf725736027f128e8edf3ea93565b2b060fca23f854900c6e8f76a1e2fb8` |
| `scripts/check-terms.py` | `87f03c09c17781344df7a7f1f61ab6db0b2509de40aae29494f852c8fb0d9af9` |
| `vocab/topics.yaml` | `4c746ac51b9ad585445037ee57abd34d5542a48e04f3667e3ea32866d8171993` |
| `vocab/entities.yaml` | `63020dd3edbb3a25339846943fa67d774335b866e687a7b70f8a110a3ac50ff7` |
| `vocab/sources.yaml` | `1f550993984e2ba4329828b01fcf08ddee97d7433027265207c98277173c50ff` |
| `vocab/signals.yaml` | `aa832bf456260fad927b47cdede104f2fe3f7488a46391c2d6e8fcf06920d0c8` |

## 名称附录

以下 298 行逐项绑定候选字符串身份、上下文次数和精确位置。位置类型只说明抽取入口，不决定语义。全部条目状态均为“待人决定”。

```text
001 生效条件 | 3 | design/drafts/facet-field.md:46:标题; design/drafts/source-governance.md:242:标题; design/drafts/terminology-governance.md:277:标题
002 知识库用法 | 3 | concepts/controlled-vocabulary.md:83:标题; concepts/vocabulary-construction.md:142:标题; concepts/vocabulary-hierarchy.md:101:标题
003 一句话 | 2 | concepts/writing-conventions.md:64:引号; design/writing.md:60:引号
004 其他学科 | 2 | concepts/classifying-new-subjects.md:40:引号; design/maintenance.md:70:引号
005 决策权限 | 2 | design/drafts/source-governance.md:203:标题; design/drafts/terminology-governance.md:219:标题
006 复核义务 | 2 | design/drafts/source-governance.md:152:标题; design/drafts/terminology-governance.md:179:标题
007 对象边界 | 2 | design/drafts/source-governance.md:12:标题; design/drafts/terminology-governance.md:12:标题
008 待写 | 2 | design/governance.md:132:引号; design/writing.md:25:引号
009 整篇重写 | 2 | concepts/writing-conventions.md:90:引号; design/writing.md:75:引号
010 点这里 | 2 | concepts/CONVENTIONS.md:63:引号; design/writing.md:41:引号
011 状态转换 | 3 | design/drafts/source-governance.md:131:标题; design/drafts/terminology-governance.md:106:标题; design/drafts/terminology-governance.md:243:引号
012 草案边界 | 2 | design/drafts/source-governance.md:4:标题; design/drafts/terminology-governance.md:4:标题
013 记录层次 | 2 | concepts/terminology-database.md:23:标题; design/drafts/terminology-governance.md:28:标题
014 说白了 | 2 | concepts/writing-conventions.md:64:引号; design/writing.md:60:引号
015 软件工程管理 | 2 | design/hierarchy.md:14:引号; design/topics.md:72:引号
016 #位置 | 1 | design/maintenance.md:214:引号
017 AI 提案，人定 | 1 | design/governance.md:62:加粗
018 AI 直接做 | 1 | design/governance.md:61:加粗
019 Dublin Core 的十五个核心元素 | 1 | concepts/metadata.md:18:标题
020 一篇一个问题 | 1 | design/writing.md:49:引号
021 一节一件事 | 1 | concepts/CONVENTIONS.md:39:加粗
022 下位集合 | 1 | design/decisions/borrow-and-analyze.md:23:加粗
023 不预告 | 1 | design/writing.md:24:引号
024 与分面字段的分工 | 1 | design/drafts/concept-groups.md:39:标题
025 东西的种类 | 1 | concepts/facet.md:75:引号
026 两种来源 | 1 | design/drafts/concept-groups.md:5:标题
027 个人理解 | 1 | concepts/note-types.md:40:引号
028 为读者写 | 1 | concepts/writing-conventions.md:7:引号
029 主题职责 | 1 | design/entities.md:94:标题
030 主题词表设计 | 1 | design/topics.md:1:标题
031 事件 | 1 | design/content-model.md:65:引号
032 五根轴的关系 | 1 | concepts/note-types.md:79:标题
033 什么的什么 | 1 | concepts/CONVENTIONS.md:27:引号
034 以下各节 | 1 | design/writing.md:38:引号
035 体裁词表 | 1 | design/content-model.md:53:标题
036 作者立场 | 1 | concepts/note-types.md:28:标题
037 依据分工 | 1 | concepts/vocabulary-construction.md:155:标题
038 修改流程 | 1 | concepts/vocabulary-construction.md:114:标题
039 候选的产生 | 1 | design/maintenance.md:124:标题
040 候选的审核 | 1 | design/maintenance.md:136:标题
041 候选识别 | 1 | concepts/vocabulary-construction.md:25:标题
042 偏好 | 1 | concepts/note-types.md:40:引号
043 元数据 (Metadata | 1 | concepts/metadata.md:1:标题
044 先做词表 | 1 | concepts/knowledge-graph.md:72:加粗
045 先大白话，再术语 | 1 | concepts/CONVENTIONS.md:35:加粗
046 六边形架构 | 1 | design/entities.md:3:引号
047 关于 | 1 | design/writing.md:13:引号
048 关系型数据库 | 1 | design/entities.md:3:引号
049 关系类型 | 1 | concepts/controlled-vocabulary.md:35:标题
050 关系类型从少到多 | 1 | concepts/knowledge-graph.md:74:加粗
051 其他学科来源 | 1 | design/hierarchy.md:99:标题
052 其实就是 | 1 | design/writing.md:60:引号
053 内容单元与版本 | 1 | design/versioning.md:22:标题
054 内容工程 | 1 | design/hierarchy.md:97:引号
055 写作规则 | 1 | design/writing.md:1:标题
056 写作规范 (Writing Conventions | 1 | concepts/writing-conventions.md:1:标题
057 决定记录 | 1 | concepts/first-principles.md:42:标题
058 决策权的首批边界 | 1 | design/decisions/decision-rights-defaults.md:1:标题
059 准入 | 1 | design/drafts/division-characteristics.md:21:标题
060 准入依据 | 1 | concepts/vocabulary-construction.md:11:标题
061 准入对象 | 2 | design/governance.md:76:引号; design/governance.md:86:标题
062 分两层 | 1 | design/decisions/borrow-and-analyze.md:21:加粗
063 分析综合 | 1 | concepts/classifying-new-subjects.md:16:标题
064 分级 | 1 | design/entities.md:61:标题
065 分组说明 | 1 | concepts/vocabulary-hierarchy.md:29:标题
066 分面 (Facet | 1 | concepts/facet.md:1:标题
067 分面与层级的分工 | 1 | concepts/facet.md:33:标题
068 分面字段草案 | 1 | design/drafts/facet-field.md:1:标题
069 分面组合 | 1 | concepts/facet.md:59:标题
070 划分方法 | 1 | concepts/vocabulary-hierarchy.md:9:标题
071 划分特征的自定治理 | 1 | design/drafts/division-characteristics.md:1:标题
072 剩余监控 | 1 | concepts/classifying-new-subjects.md:36:标题
073 加粗词 | 1 | design/writing.md:37:加粗
074 医生 | 1 | concepts/facet.md:29:引号
075 单人加 AI 的治理 | 1 | concepts/governance.md:36:标题
076 即将支持 | 1 | design/writing.md:23:引号
077 原样复制与本地分析分层的决定 | 1 | design/decisions/borrow-and-analyze.md:1:标题
078 原理 | 1 | concepts/note-types.md:12:引号
079 原理与理由 | 1 | concepts/first-principles.md:58:标题
080 发版时机 | 1 | design/versioning.md:18:标题
081 受控词表 (Controlled Vocabulary | 1 | concepts/controlled-vocabulary.md:1:标题
082 变更控制 | 1 | design/governance.md:69:标题
083 变更记录 | 1 | design/versioning.md:26:标题
084 只有人定 | 1 | design/governance.md:63:加粗
085 叫什么 | 1 | concepts/knowledge-graph.md:40:引号
086 同一内在类别的概念分组 | 1 | concepts/facet.md:5:加粗
087 同一概念 | 1 | concepts/terminology-database.md:37:引号
088 后面会讲 | 1 | design/writing.md:23:引号
089 命名实体词表设计 | 1 | design/entities.md:1:标题
090 和分类的区别 | 1 | concepts/concept-group.md:16:标题
091 图书情报学科 | 1 | design/hierarchy.md:87:标题
092 图谱实例 | 1 | concepts/knowledge-graph.md:95:标题
093 图谱把词表的 RT 拆开 | 1 | concepts/knowledge-graph.md:51:加粗
094 处置决定 | 1 | design/content-model.md:136:标题
095 复制 | 1 | concepts/vocabulary-mapping.md:97:引号
096 复制看需要 | 1 | concepts/vocabulary-mapping.md:94:加粗
097 复核 | 1 | design/drafts/division-characteristics.md:38:标题
098 外部词表用法 | 1 | concepts/vocabulary-mapping.md:67:标题
099 多语对应 | 1 | concepts/terminology-database.md:35:标题
100 多项并列用表格 | 1 | concepts/CONVENTIONS.md:37:加粗
101 大致相等 | 1 | concepts/vocabulary-mapping.md:40:引号
102 失效处理 | 1 | design/drafts/source-governance.md:174:标题
103 委员会法 | 1 | concepts/vocabulary-construction.md:44:标题
104 委托关系 | 1 | design/drafts/terminology-governance.md:151:标题
105 媒介性质 | 1 | concepts/metadata.md:55:加粗
106 字段能取哪些值 | 1 | concepts/metadata.md:59:加粗
107 完备划分 | 1 | design/drafts/division-characteristics.md:24:加粗
108 定义与综述 | 1 | concepts/knowledge-graph.md:81:标题
109 定位 | 1 | design/drafts/facet-field.md:5:标题
110 定期复审 | 1 | design/maintenance.md:181:标题
111 实体记录 | 1 | design/drafts/source-governance.md:75:标题
112 实用主义 | 1 | concepts/classifying-new-subjects.md:30:标题
113 对应哪一条 | 1 | concepts/vocabulary-mapping.md:93:引号
114 对应属性 | 1 | concepts/controlled-vocabulary.md:71:标题
115 对管理的管理 | 1 | concepts/governance.md:5:加粗
116 对象与状态 | 1 | design/maintenance.md:11:标题
117 对象分工 | 1 | design/entities.md:7:标题
118 对象范围 | 1 | design/governance.md:7:标题
119 将被替代 | 1 | design/maintenance.md:161:引号
120 层级结构 | 1 | design/hierarchy.md:1:标题
121 展示格式用代码块 | 1 | concepts/CONVENTIONS.md:38:加粗
122 常见的知识体系 | 1 | concepts/body-of-knowledge.md:32:标题
123 应用映射 | 1 | design/content-model.md:140:标题
124 应用映射的分工 | 1 | design/maintenance.md:198:标题
125 废弃 | 1 | design/drafts/division-characteristics.md:34:标题
126 废弃流程 | 1 | concepts/vocabulary-construction.md:120:标题
127 建树前的归类 | 1 | concepts/facet.md:7:标题
128 建设方法 | 1 | concepts/vocabulary-construction.md:40:标题
129 引用结构 | 1 | design/drafts/source-governance.md:30:标题
130 心得 | 2 | concepts/note-types.md:12:引号; concepts/note-types.md:40:引号
131 急诊科常用词 | 2 | concepts/concept-group.md:11:引号; concepts/concept-group.md:18:引号
132 成熟度 | 1 | concepts/note-types.md:42:标题
133 我们 | 1 | design/writing.md:56:引号
134 所有标准 | 1 | design/decisions/tree-by-discipline.md:24:引号
135 所有缺陷 | 1 | design/decisions/tree-by-discipline.md:24:引号
136 手术 | 1 | concepts/facet.md:29:引号
137 技术路线 | 1 | concepts/knowledge-graph.md:55:标题
138 抄自哪 | 1 | concepts/vocabulary-mapping.md:93:引号
139 护理 | 2 | concepts/facet.md:61:引号; concepts/facet.md:66:引号
140 指导、监督并被问责 | 1 | concepts/governance.md:9:加粗
141 指标表 | 1 | design/maintenance.md:194:标题
142 按学科 | 1 | design/decisions/tree-by-discipline.md:26:引号
143 按用途圈出的一批概念 | 1 | concepts/concept-group.md:5:加粗
144 排除范围 | 1 | design/topics.md:78:标题
145 探测边界 | 1 | design/drafts/source-governance.md:191:标题
146 推理最后考虑 | 1 | concepts/knowledge-graph.md:75:加粗
147 收录依据 | 1 | design/maintenance.md:202:标题
148 政策与职责 | 1 | concepts/governance.md:27:引号
149 故意不传递 | 1 | concepts/vocabulary-mapping.md:40:加粗
150 教材 | 1 | concepts/controlled-vocabulary.md:110:标题
151 数据模型依据 | 1 | design/decisions/borrow-and-analyze.md:29:标题
152 数组分组 | 1 | design/hierarchy.md:33:标题
153 数组结构 | 1 | concepts/vocabulary-hierarchy.md:21:标题
154 文件布局 | 1 | design/topics.md:93:标题
155 文档类型 | 1 | design/writing.md:7:标题
156 文档类型词表 | 1 | design/content-model.md:38:标题
157 文章关系 | 1 | concepts/README.md:5:标题
158 断言有来源 | 1 | concepts/CONVENTIONS.md:40:加粗
159 新主题的分类 (Classifying New Subjects | 1 | concepts/classifying-new-subjects.md:1:标题
160 新增流程 | 1 | concepts/vocabulary-construction.md:103:标题
161 方法登记 | 1 | design/principles.md:1:标题
162 映射关系 | 1 | design/sources-registry.md:47:标题
163 映射总是有 | 1 | concepts/vocabulary-mapping.md:93:加粗
164 映射的类型 | 1 | concepts/vocabulary-mapping.md:20:标题
165 映射的结构模型 | 1 | concepts/vocabulary-mapping.md:44:标题
166 是什么类 | 1 | design/drafts/concept-groups.md:41:引号
167 有例子才算讲清楚 | 1 | concepts/CONVENTIONS.md:36:加粗
168 有哪些字段 | 1 | concepts/metadata.md:59:加粗
169 有对应 | 1 | concepts/vocabulary-mapping.md:42:引号
170 未分类 | 1 | concepts/classifying-new-subjects.md:38:引号
171 未定事项 | 1 | concepts/CONVENTIONS.md:69:标题
172 未归 | 1 | design/drafts/division-characteristics.md:24:引号
173 未核对 | 1 | design/governance.md:149:引号
174 未登记的做法 | 1 | design/principles.md:30:标题
175 本体 / Schema | 1 | concepts/knowledge-graph.md:31:加粗
176 本库用途 | 1 | concepts/terminology-database.md:65:标题
177 术后 | 2 | concepts/facet.md:61:引号; concepts/facet.md:66:引号
178 术后护理 | 2 | concepts/facet.md:61:引号; concepts/facet.md:66:引号
179 术语数据库 (Terminology Database | 1 | concepts/terminology-database.md:1:标题
180 术语治理 | 1 | design/drafts/terminology-governance.md:1:标题
181 术语记录 | 1 | design/drafts/terminology-governance.md:64:标题
182 杂项 | 1 | concepts/classifying-new-subjects.md:38:引号
183 权威与控制的行使 | 1 | concepts/governance.md:10:加粗
184 来源名称规范表 | 1 | design/sources-registry.md:1:标题
185 来源已失效 | 1 | design/maintenance.md:151:引号
186 来源治理 | 1 | design/drafts/source-governance.md:1:标题
187 来源用法 | 1 | design/sources-registry.md:31:标题
188 来源的复核 | 1 | design/maintenance.md:147:标题
189 来源职责 | 1 | design/entities.md:90:标题
190 构成 | 1 | concepts/knowledge-graph.md:27:标题
191 枚举 | 1 | design/decisions/borrow-and-analyze.md:7:加粗
192 标准里没有它 | 1 | concepts/classifying-new-subjects.md:28:引号
193 标识一份资源的属性的数据 | 1 | concepts/metadata.md:5:加粗
194 标识符规则 | 1 | design/content-model.md:95:标题
195 标题的默认规则 | 1 | concepts/CONVENTIONS.md:22:标题
196 树按学科而非分面的决定 | 1 | design/decisions/tree-by-discipline.md:1:标题
197 树的性质 | 1 | design/hierarchy.md:11:标题
198 核心 | 1 | concepts/metadata.md:7:引号
199 概念文写作约定 | 1 | concepts/CONVENTIONS.md:1:标题
200 概念文索引 | 1 | concepts/README.md:1:标题
201 概念组 (Concept Group | 1 | concepts/concept-group.md:1:标题
202 概念组草案 | 1 | design/drafts/concept-groups.md:1:标题
203 概念记录 | 1 | design/drafts/terminology-governance.md:36:标题
204 概念记录的字段 | 1 | design/topics.md:97:标题
205 模型职责 | 1 | design/drafts/facet-field.md:23:标题
206 每节的默认规则 | 1 | concepts/CONVENTIONS.md:32:标题
207 治理 (Governance | 1 | concepts/governance.md:1:标题
208 治理与维护的分层 | 1 | concepts/governance.md:25:标题
209 派生组是升级的中间态 | 1 | concepts/vocabulary-mapping.md:95:加粗
210 版本块 | 1 | design/versioning.md:5:标题
211 状态与粒度 | 1 | concepts/vocabulary-construction.md:89:标题
212 状态层次 | 1 | concepts/terminology-database.md:47:标题
213 生成边界 | 1 | design/drafts/terminology-governance.md:161:标题
214 用法边界 | 1 | concepts/facet.md:46:标题
215 用过一段时间 | 1 | design/drafts/division-characteristics.md:45:引号
216 用途 | 1 | design/topics.md:89:标题
217 用途登记 | 1 | design/drafts/source-governance.md:101:标题
218 登记 | 1 | design/drafts/division-characteristics.md:5:标题
219 登记文件 | 1 | design/drafts/concept-groups.md:20:标题
220 登记表 | 1 | design/principles.md:7:标题
221 监控 | 1 | design/maintenance.md:9:引号
222 看得懂、信得过 | 1 | concepts/CONVENTIONS.md:7:加粗
223 知识体系 (Body of Knowledge | 1 | concepts/body-of-knowledge.md:1:标题
224 知识图谱 (Knowledge Graph | 1 | concepts/knowledge-graph.md:1:标题
225 破坏性变更 | 1 | design/versioning.md:16:引号
226 硬规则 | 2 | concepts/CONVENTIONS.md:9:加粗; concepts/CONVENTIONS.md:14:标题
227 笔记的类型 (Note Types | 1 | concepts/note-types.md:1:标题
228 第一原理与设计理由 (First Principles and Design Rationale | 1 | concepts/first-principles.md:1:标题
229 第一句回答标题 | 1 | concepts/CONVENTIONS.md:34:加粗
230 类别 | 1 | design/entities.md:43:标题
231 类型 | 1 | concepts/note-types.md:5:引号
232 索引位置 | 1 | concepts/CONVENTIONS.md:55:标题
233 约束的边界 | 1 | concepts/CONVENTIONS.md:5:标题
234 经验法 | 1 | concepts/vocabulary-construction.md:55:标题
235 结构 | 1 | concepts/body-of-knowledge.md:20:标题
236 结构复制 | 1 | design/hierarchy.md:16:标题
237 结构性变更 | 1 | design/governance.md:177:引号
238 结构来源 | 1 | design/hierarchy.md:46:标题
239 结构类型 | 1 | concepts/controlled-vocabulary.md:21:标题
240 结构规则 | 1 | design/hierarchy.md:7:标题
241 结构预览 | 1 | design/hierarchy.md:114:标题
242 给链接加类型 | 1 | concepts/knowledge-graph.md:73:加粗
243 维护 | 1 | design/maintenance.md:1:标题
244 维护要求 | 1 | concepts/terminology-database.md:57:标题
245 编程 | 1 | concepts/classifying-new-subjects.md:22:引号
246 编程语言 | 1 | design/hierarchy.md:178:标题
247 节末给落点 | 1 | concepts/CONVENTIONS.md:41:加粗
248 范围 | 1 | design/drafts/division-characteristics.md:30:标题
249 范围与用途 | 2 | design/topics.md:44:标题; design/topics.md:171:引号
250 覆盖范围 | 1 | design/topics.md:48:标题
251 规则的推导 | 1 | concepts/writing-conventions.md:48:标题
252 规范的层次 | 1 | concepts/writing-conventions.md:35:标题
253 计算机分支 | 1 | design/hierarchy.md:59:标题
254 记录结构 | 1 | concepts/vocabulary-construction.md:72:标题
255 记者 | 1 | design/content-model.md:65:引号
256 论证过程 | 1 | concepts/first-principles.md:29:标题
257 设计与应用分离 | 1 | design/decisions/form-independence.md:1:标题
258 设计分工 | 1 | design/topics.md:196:标题
259 设计文档索引 | 1 | design/README.md:1:标题
260 设计理由的传统 | 1 | concepts/first-principles.md:25:标题
261 词表一览 | 1 | design/README.md:36:标题
262 词表互操作 | 1 | concepts/vocabulary-mapping.md:56:标题
263 词表关系 | 1 | design/content-model.md:107:标题
264 词表实例 | 1 | concepts/controlled-vocabulary.md:116:标题
265 词表总览 | 1 | design/topics.md:7:标题
266 词表映射 (Vocabulary Mapping | 1 | concepts/vocabulary-mapping.md:1:标题
267 词表是图谱的命名层 | 1 | concepts/knowledge-graph.md:49:加粗
268 词表版本 | 1 | design/versioning.md:1:标题
269 词表的层级 (Hierarchy | 1 | concepts/vocabulary-hierarchy.md:1:标题
270 词表的层级是图谱的分类层 | 1 | concepts/knowledge-graph.md:50:加粗
271 词表的建设与维护 (Vocabulary Construction and Maintenance | 1 | concepts/vocabulary-construction.md:1:标题
272 词表结构总览 | 1 | concepts/README.md:31:标题
273 译名 | 1 | design/governance.md:106:标题
274 译名准入 | 1 | design/drafts/terminology-governance.md:92:标题
275 语言记录 | 1 | design/drafts/terminology-governance.md:56:标题
276 谁在用 | 1 | design/drafts/concept-groups.md:41:引号
277 谁要用 | 1 | concepts/concept-group.md:5:引号
278 质量与验收 | 3 | design/governance.md:18:引号; design/governance.md:25:引号; design/governance.md:125:标题
279 载体 | 1 | concepts/note-types.md:54:标题
280 载体词表 | 1 | design/content-model.md:67:标题
281 迁移边界 | 1 | design/drafts/terminology-governance.md:261:标题
282 过程 | 1 | design/writing.md:73:标题
283 这是什么 | 1 | concepts/concept-group.md:5:引号
284 适用性研究 | 1 | design/drafts/facet-field.md:17:标题
285 邻近主题的处理 | 1 | design/topics.md:65:标题
286 重点分支 | 1 | design/hierarchy.md:168:标题
287 链接 | 1 | concepts/knowledge-graph.md:73:引号
288 链接规则 | 1 | concepts/CONVENTIONS.md:59:标题
289 间接依赖 | 1 | concepts/knowledge-graph.md:75:引号
290 需要复核 | 1 | design/drafts/source-governance.md:199:引号
291 顶层按学科 | 1 | design/decisions/tree-by-discipline.md:18:加粗
292 顶层来源 | 1 | design/hierarchy.md:50:标题
293 项目约定入口 | 1 | design/decisions/project-instructions-entry.md:1:标题
294 风险 | 1 | design/governance.md:155:标题
295 首批来源 | 1 | design/sources-registry.md:61:标题
296 首轮后校准 | 1 | concepts/governance.md:23:引号
297 默认做法 | 1 | concepts/CONVENTIONS.md:10:加粗
298 默认分节 | 1 | concepts/CONVENTIONS.md:43:标题
```
