# 治理实施准备

状态：历史计划，库存、旁路研究和两份详细子计划均已完成。当前执行顺序以[项目路线](2026-08-31-project-roadmap.md)为准。

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:dispatching-parallel-agents for independent inventories, then superpowers:writing-plans for the two implementation plans.

**Goal:** 从当前真实数据生成来源治理与术语治理的完整库存、旁路研究和实施边界，再分别编写可执行的来源模式迁移计划与术语模式生成计划。

**Architecture:** 第一波使用互斥写集并行生成十份核心库存和八份旁路报告，全部保存在本计划的 Superpowers 执行目录，不修改正式项目。第二波由两个计划代理分别消费来源和术语库存，编写两个职责独立的实施计划；控制器最后核对共享接口、文件写集、测试先后和人工门禁。

**Tech Stack:** Markdown、TSV、Python 3 只读分析、Git、Superpowers 子代理。

**Spec:** [术语治理设计](../specs/2026-08-27-terminology-governance-design.md)、[来源治理草案](../../../design/drafts/source-governance.md)、[术语治理草案](../../../design/drafts/terminology-governance.md)

## 全局约束

- 在 `feat/terminology-governance` 分支执行，不创建 worktree，不修改 `master`。
- 两份治理草案内容已经分别获人接受，但尚未生效。库存可以使用草案字段作拟议分类，不得把它们写入正式数据。
- 第一波代理不得修改任何受 Git 跟踪文件，不得提交、推送、合并或创建正式 schema、数据、脚本、决定记录和应用映射。
- 所有外部事实实际核验；优先标准发布机构和官方材料。PDF 不可稳定读取时记录未读边界并寻找可定位替代，不猜正文。
- 当前阶段零自定。库存中的“拟议去向”引用已批准草案字段；无法归类时标“待人决定”，不造字段或术语。
- 字符串、目录和出现次数只安排阅读顺序，不能自动决定 `basis`、`source`、`match`、委托、概念对应或来源用途。
- 共享接口固定由来源草案定义；术语库存和计划只引用 `basis`、`source`、`match`，不得复制定义。
- 旁路研究只形成概念依据、影响和不采用后果，不修改三份旧草案，不决定生活范围、实体类别、归属或草案生效。
- Obsidian 和 TBX 实施继续后置；TBX 旁路只允许记录交换依赖，不写导出计划。
- 每个库存逐行带当前文件位置和证据说明，不能只给计数。
- 同一正式文件可以被多个只读库存读取，但各代理只写自己的执行产物。
- 用户要求充分使用并行代理；第一波一次派发全部互不依赖任务。控制器不重复代理工作，只做身份、覆盖和接口校验。
- 第二波只写两份 Superpowers 实施计划，不执行计划中的正式变更。具体 schema、ID、周期、阈值、来源改档、范围、术语准入和草案生效仍按精确计划门禁处理。

## 执行目录

全部产物位于 `.superpowers/sdd/2026-08-31-governance-implementation-prep/`。

| 产物 | 职责 |
|---|---|
| `source-entities.tsv`、`source-entities.md` | 来源实体、版本、地址、档位和状态线索 |
| `source-roles.tsv`、`source-roles.md` | 来源用途、旧 `candidate` 和角色迁移 |
| `basis-inventory.tsv`、`basis-inventory.md` | 全库逐值依据及完整性 |
| `source-inventory.tsv`、`source-inventory.md` | 全库实际派生关系 |
| `match-inventory.tsv`、`match-inventory.md` | 全库概念映射及依据 |
| `origin-inventory.tsv`、`origin-inventory.md` | 旧 `origin` 语义分流 |
| `term-glossary.tsv`、`term-glossary.md` | 术语表、译名依据、状态和延期 |
| `term-delegation.tsv`、`term-delegation.md` | 其他词表标签、消费者和委托候选 |
| `generation-baseline.md` | 术语表、词表和生成校验基线 |
| `maintenance-baseline.md` | 候选、`unassigned`、`self`、来源和阈值基线 |
| `draft-division.md` | 划分特征概念依据预核 |
| `draft-facet.md` | 分面字段真实数据试标准备 |
| `draft-groups.md` | 手工概念组概念依据预核 |
| `design-life.md` | 生活主题范围材料 |
| `design-entities.md` | 实体类别外部类与影响 |
| `design-llm.md` | 大语言模型身份和归属材料 |
| `design-communication.md` | 技术传播概念和范围材料 |
| `quality-debt.md` | 旧标题和旧 SDD 链接只读库存 |
| `source-plan-input.md` | 来源库存集成结果 |
| `terminology-plan-input.md` | 术语库存集成结果 |
| `progress.md` | 代理、哈希、覆盖、裁定和恢复状态 |

## 库存接口

六个来源相关 TSV 使用下列固定列。

```text
文件	位置	对象	当前值	草案分类	证据或上下文	拟议去向	决策级别	状态
```

两个术语相关 TSV 使用下列固定列。

```text
对象	语言	文件	位置	当前形式或值	概念身份	依据状态	消费者或所有者	拟议去向	决策级别	状态
```

`状态` 只允许“可机械迁移”“需要复核”“待人决定”“无需迁移”。拟议去向不是批准决定。

## 核心库存

以下十项并行执行：

1. 来源实体、版本、地址、`tier`、现行状态和复核信息。
2. 来源用途、角色、旧 `candidate` 和批准材料。
3. 全库 `basis` 及紧缩值、`self`、`none`、定位和日期完整性。
4. 全库 `source` 的实际派生语义、外部条目和用途资格。
5. 全库 `match` 的关系、外部概念、逐项依据和同名风险。
6. 全库旧 `origin` 的发现、依据或派生语义分流。
7. 术语表和后迁移审查表中的形式、语言、译名依据、动作和延期。
8. 其他词表标签、正文消费者、概念身份和 `term_concept` 委托候选。
9. 术语表、词表、构建脚本、校验器和确定性输出基线。
10. 候选、`unassigned`、`self`、来源复核、未登记名称和阈值指标基线。

每项必须读取当前文件上下文并核对身份唯一；不得用字符串自动填写草案分类。

## 旁路研究

以下八项与核心库存并行，但不阻塞两个模式计划：

1. 划分特征与 ISO 25964 数组、节点标签、划分属性的概念边界。
2. 分面字段的真实概念集合、查询需求、试标输入和结果接口。
3. 手工概念组与 SKOS 集合、叙词表数组、映射视图的区别。
4. 健康、理财、旅行等生活主题的范围材料和顶层选择后果。
5. 实体类别的外部类、实例判据和现有记录影响。
6. 大语言模型作为概念或个体的身份、上位概念和多重归属材料。
7. 技术传播的学科范围、专业实践、内容类型和现有节点影响。
8. 未改受跟踪 Markdown 的标题债务和两个旧 SDD 链接的精确位置、类型与处理权限。

## 集成边界

核心库存完成后分别生成两个计划输入：

- `source-plan-input.md` 汇总来源实体、用途、`basis`、`source`、`match`、`origin`、探测和复核义务的文件分布、迁移类别、正反例和人类决定。
- `terminology-plan-input.md` 汇总术语记录、译名、委托、消费者、生成基线、维护基线、迁移类别、正反例和人类决定。

两个输入共同列出共享接口和交叉依赖，但不得互相复制职责。

## 计划输出

库存集成后并行编写：

- `docs/superpowers/plans/2026-08-31-source-schema-migration.md`；
- `docs/superpowers/plans/2026-08-31-terminology-schema-generation.md`。

每份计划必须给出精确文件、模式、测试、迁移批次、回滚、提交和人工门禁；不能含占位符，不能把待人决定写成默认值。

## 验证门禁

- 十个核心库存的当前身份覆盖完整，无重复、无空字段，状态值合法。
- 八份旁路报告分别列外部概念、项目问题、影响文件、不采用后果、未读边界和决策级别。
- 两个计划输入逐项链接全部核心库存并登记哈希。
- 两份实施计划分别通过规格覆盖、占位符、接口一致性、文件写集和测试先后自查。
- 两份计划的共享接口与已批准来源草案逐字一致；术语计划不得定义第二套来源引用结构。
- 最终只提交本准备计划和两份实施计划，不提交执行目录库存。
- 向人提交两份实施计划和精确待定问题后停止；未获对应计划批准前不修改正式 schema、数据或脚本。
