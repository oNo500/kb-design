# 消费者迁移计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan continuously. Human-only decisions remain a single concentrated gate; no project migration starts before that gate is satisfied.

**Goal:** 为全部 `NFJ` 与 `NFR` 问题形成有依据的推荐，集中取得人工决定，再把已批准结果迁移到项目文档、数据和必要脚本。

**Architecture:** 第一段只在 Superpowers 执行目录中并行研究，按安全答复单元形成推荐，不修改正式项目。人工一次性批准精确决定后，第二段先生成逐文件旧节去向和迁移清单，再按文档目的整节或整篇重写；生成输入先于生成结果，脚本与规则同步。控制器只做覆盖、权限和必要验证，不增加新的全量独立复审。

**Tech Stack:** Markdown、TSV、JSON、YAML、Python 3、Git、Superpowers 子代理、标准发布机构官方材料。

**Spec:** [消费者分类设计](../specs/2026-08-30-basic-unit-consumer-classification-design.md)、[术语治理设计](../specs/2026-08-27-terminology-governance-design.md)

## 全局约束

- 在 `/Users/xiu/code/kb-design` 的 `feat/terminology-governance` 分支执行，不创建 worktree，不在 `master` 上修改。
- `design/writing.md`、`design/governance.md`、`concepts/CONVENTIONS.md` 和 `AGENTS.md` 全程适用；冲突时以前三者中更具体的规则为准。
- 当前阶段零自定。代理只能核对概念、来源和已有形式；查不到时记缺口或延期，不能造词、试用候选形式或用机器翻译代替译名依据。
- 外部事实必须实际核验并使用 `[标题](url)`。优先标准发布机构、官方规范和权威文献；PDF 无法稳定读取时记录未读边界并寻找可定位的替代材料。
- `NFJ` 的三十九个安全答复单元和 `NFR` 的八个问题全部给出推荐，但推荐不是决定。范围、规则、结构、归属、术语准入、来源改档、草案生效及删除非候选对象仍由人决定。
- 人工决定集中为一个门禁。未取得精确答复前，只能写 `.superpowers/sdd/2026-08-30-consumer-semantic-migration/` 和本计划，不得修改正式项目文件。
- 人工批准后，迁移必须按 `migration-proposal.tsv` 的五列身份追踪一百七十三个位置，并把后续新增影响列入同一清单；不能只做字符串替换。
- 文档改动涉及一节以上时，先列旧版逐节去向，再按目的整节或整篇重写。每批完成后逐项核对旧内容去向。
- `vocab/build/` 是生成输入。范围注释有批准改动时先改输入，再运行既有生成流程；正式数据不得反向手改后与输入分叉。
- 用户已要求减少测试和 review。每批不安排额外全量独立复审，只保留来源可追溯、身份覆盖、格式、既有校验器和生成幂等性检查。
- 所有受跟踪改动使用 `apply_patch` 或项目既有生成命令完成，不采用逐点补丁式写作。提交说明标注本批最高决策级别。

## 文件职责

| 文件 | 操作 | 职责 |
|---|---|---|
| `.superpowers/sdd/2026-08-30-consumer-semantic-migration/progress.md` | 新建并持续整篇整理 | 保存任务状态、代理身份、哈希、门禁和裁定 |
| `.superpowers/sdd/2026-08-30-consumer-semantic-migration/nfj-*.md` | 五个并行产物 | 保存各组上下文、依据、选项、影响和推荐 |
| `.superpowers/sdd/2026-08-30-consumer-semantic-migration/decision-recommendations.md` | 新建并整篇重写 | 汇总全部 `NFJ` 与 `NFR` 推荐，供一次性人工决定 |
| `.superpowers/sdd/2026-08-30-consumer-semantic-migration/human-decision-response.md` | 门禁后新建 | 逐个登记人工批准、拒绝或延期及授权边界 |
| `.superpowers/sdd/2026-08-30-consumer-semantic-migration/migration-map.tsv` | 门禁后生成 | 保存原五列身份、决定、目标文件、目标小节、处置和验证 |
| `.superpowers/sdd/2026-08-30-consumer-semantic-migration/section-disposition.md` | 门禁后新建 | 保存每篇受影响文档的旧节去向和整篇重写边界 |
| `.superpowers/sdd/2026-08-30-consumer-semantic-migration/verification.md` | 迁移后新建 | 保存必要命令、结果和未关闭问题 |

## 执行顺序

研究批次可以并行；决定包集成必须等待全部批次。人工门禁满足后，迁移清单先于正式项目改动；概念文先于由其导出的设计规则，生成输入先于正式数据，摘要最后同步。

### 研究分批

**Files:**

- Read: `.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/nfj-grouped-decision-package.md`
- Read: `.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/human-decision-package.md`
- Read: `.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/form-evidence.tsv`
- Create: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/nfj-object-terminology.md`
- Create: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/nfj-principles-tree.md`
- Create: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/nfj-lifecycle-system.md`
- Create: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/nfj-life-detection-annotations.md`
- Create: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/nfr-recommendations.md`

**Interfaces:**

- Consumes: 三十九个安全答复单元、八个新增形式问题、已批准的 `term/en keep` 和十项清单动作。
- Produces: 每个单元独立的上下文、概念依据、选项、影响和推荐，不产生人工决定。

**Steps:**

- [ ] 四个独立代理分别覆盖“对象方法与术语治理”“第一原理与树面模型”“生命周期与体系范围”“生活范围、检测实现与注释数据”，第五个代理覆盖全部 `NFR`。
- [ ] 每个代理打开冻结位置和相关概念文；共同问题可以共享依据，但每个安全答复单元必须单独给出推荐。
- [ ] 外部来源只采用实际读到且可定位的内容。每项区分外部概念事实、项目已有规则和仍需人定的项目选择。
- [ ] 每份报告整体写成完整文档，自查编号覆盖、标题、标点、链接和零自定边界。
- [ ] 控制器核对 `AU-001` 至 `AU-039` 与 `NFR-001` 至 `NFR-008` 各出现一次；缺失、重复或越权推荐阻止集成。

### 决定集成

**Files:**

- Read: 本计划五份研究报告
- Create: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/decision-recommendations.md`
- Modify: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/progress.md`

**Interfaces:**

- Consumes: 四十七个决策支持结果。
- Produces: 一份可以一次性批准的精确推荐清单。

**Steps:**

- [ ] 按原九个讨论组排列三十九个 `AU`，另列八个 `NFR`；不把共享讨论组写成共享批准。
- [ ] 每项只保留决定所需的概念依据、推荐、替代方案代价、影响文件和权限级别，并链接完整研究报告。
- [ ] 为每项设置稳定答复编号，明确“批准推荐”“拒绝并采用指定方案”或“延期”三种合法答复。
- [ ] 机械核对四十七个答复单位的唯一性、原 `NFJ` 四十八项覆盖和八个 `NFR` 覆盖。
- [ ] 向人提交整包后等待一次集中答复。不得把“执行全部阶段”解释为对未展示语义选项的自动批准。

### 决定登记

**Files:**

- Read: `decision-recommendations.md`
- Create: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/human-decision-response.md`

**Interfaces:**

- Consumes: 人对全部稳定答复编号的精确决定。
- Produces: 后续迁移唯一可以消费的决定记录。

**Steps:**

- [ ] 逐项登记人工原话和规范化动作；未回答项保持未决定，不由代理补齐。
- [ ] 区分语义决定、术语研究继续与否、术语准入、迁移批准、来源改档和草案生效，禁止权限外推。
- [ ] 计算决定记录的 SHA-256，并在迁移清单中锁定该哈希。

### 迁移编排

**Files:**

- Read: `.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/migration-proposal.tsv`
- Read: `human-decision-response.md`
- Create: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/migration-map.tsv`
- Create: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/section-disposition.md`

**Interfaces:**

- Consumes: 一百七十三个冻结消费者身份和全部人工决定。
- Produces: 逐位置处置、逐节去向、实施批次和验证方法。

**Steps:**

- [ ] 重新定位每个冻结身份；原行移动但内容身份唯一时记录新位置，无法唯一定位时停止该项而不猜。
- [ ] 把每个位置标成“保留且澄清”“按批准概念重写”“移除无效表述”“延期不改”或“生成结果随输入更新”，并记录决定编号。
- [ ] 为三十个当前受影响文件列旧节去向。文档按概念文、设计文档、决定记录、草案、摘要、来源笔记、脚本、生成输入和正式数据分批。
- [ ] 检查批准决定产生的新影响；新增位置加入清单，不用一百七十三条上限掩盖漏项。
- [ ] 迁移清单和旧节去向全部闭合后才修改正式项目。

### 正式迁移

**Files:**

- Modify: `concepts/` 中迁移清单列出的概念文
- Modify: `design/` 中迁移清单列出的设计文档、决定记录和草案
- Modify: `scripts/check-terms.py`、`scripts/lookup-labels.py`（仅在决定要求行为变化时）
- Modify: `vocab/build/scope-zh.json`（仅按已批准的数据含义）
- Generate: `vocab/topics.yaml`（仅由批准后的输入生成）
- Modify: `AGENTS.md` 与相关索引摘要

**Interfaces:**

- Consumes: 锁定的决定记录、迁移清单和旧节去向。
- Produces: 自洽的正式文档、输入数据、生成结果和必要脚本。

**Steps:**

- [ ] 先重写概念文，逐项核对旧节去向；概念依据缺失的决定保持草案或延期，不写成已生效事实。
- [ ] 再重写由概念导出的设计文档；规则变化需要决定记录时新建记录，不回改旧决定。
- [ ] 脚本只实现已批准的检测语义；先写能证明旧行为不符决定的测试，再整体修改相关逻辑。
- [ ] 数据改动先重写生成输入，再运行既有生成命令并逐项检查正式结果；不得把生成结果作为编辑源。
- [ ] 最后同步 `AGENTS.md`、索引和交叉链接。应用映射与 Obsidian 导出仍不在本计划范围。
- [ ] 每批使用符合最高权限级别的提交说明；不推送、不合并、不发布。

### 必要验证

**Files:**

- Create: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/verification.md`
- Modify: `.superpowers/sdd/2026-08-30-consumer-semantic-migration/progress.md`

**Interfaces:**

- Consumes: 全部分批提交和迁移清单。
- Produces: 可复现的完成证据与未关闭项。

**Steps:**

- [ ] 核对迁移清单每行都有决定编号、目标位置、处置和验证结果，且所有非延期项都已关闭。
- [ ] 运行受影响脚本的单元测试、现有词表校验、链接检查和生成幂等性检查；只记录实际命令和结果。
- [ ] 扫描已批准移除的形式和未准入候选，人工检查剩余命中是否属于来源陈述、专名、代码或明确延期项。
- [ ] 核对标题、中文标点、汉字与西文间距、术语表与正文一致性，以及概念文索引。
- [ ] 写入 `verification.md`，列出通过项、失败项和仍需人的决定；失败不包装成完成。
- [ ] 展示 Git 差异与建议提交，不推送、不合并、不发版，也不启动 Obsidian 映射和导出。
