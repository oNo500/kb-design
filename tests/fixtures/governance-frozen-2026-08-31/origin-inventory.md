# 旧来源字段库存

## 盘点边界

本库存绑定 `feat/terminology-governance` 分支的 `9e7b411c23e890d13d70fc16d443b760313126c4`。读取范围是该提交下的全部受 Git 跟踪文件；执行目录中的忽略产物不作为正式数据。字符串扫描只建立阅读队列，TSV 的语义结论均来自对当前位置、所在记录、现行设计、数据和消费脚本的逐项阅读。

库存表使用计划规定的九列接口。隐式身份为“文件＋位置＋对象”；19 个身份全部唯一。“拟议去向”只引用已批准边界中的 `discovery`、`basis` 和 `source`，不是迁移决定。

## 事实基线

- 受跟踪文本有 13 个文件的 38 行命中独立单词 `origin`，共 42 个单词命中。
- 完整遍历全部受跟踪 YAML 和 JSON 的解析树，键名 `origin` 为 0，标量值 `origin` 为 0。
- `vocab/topics.yaml` 共有 700 条概念和 24 个数组；700 条概念均无 `origin`。其中 8 条 `source: self` 均是 `active` 顶层，692 条是外部结构的 `unassigned`，没有 `candidate` 主题概念。
- `vocab/entities.yaml` 共有 61 个实体，其中 29 个 `standard`、2 个 `publication`；没有实体被 `origin` 引用。`design/topics.md:132` 的 `cockburn-2005-hexagonal` 只是文档示例，当前实体表中不存在该 id。
- `vocab/sources.yaml` 共有 31 条来源用途记录，现行 `candidate` 角色有 5 条。数量、角色或目录不能使任何文档位置自动变成 `discovery`。
- `scripts/build-topics.py` 不接收也不输出 `origin`；`scripts/check-topics.py` 不读取也不校验 `origin`。当前校验运行结果为 0 处问题。

## 语义分流

| 分类 | 行数 | 结论 |
|---|---:|---|
| 发现线索 | 3 | 新主题的提名文献或首次出现上下文只能成为 `discovery` 候选；具体记录形状仍待获准方案。 |
| 逐值依据 | 1 | `design/topics.md:138` 明确把旧字段称为依据，但缺少被支持的值、相邻关系和 locator；只能作为拆分成逐值 `basis` 的候选。 |
| 实际派生 | 1 | `design/topics.md:132` 的六边形架构示例表达 `source` 候选，但示例概念和实体都不在当前数据中，不构成真实迁移值。 |
| 待人决定 | 14 | 其余位置混用“源头”、“来自”、首次出现、实体目标和保留依赖，或只说明空值与实现缺口；必须保持未获准，不得由字符串批量选择去向。 |

TSV 中没有“可机械迁移”行。状态分布为“需要复核” 11 行、“待人决定” 2 行、“无需迁移” 6 行。

## 位置覆盖

| 文件 | 原始命中行 | 处理 |
|---|---|---|
| `concepts/classifying-new-subjects.md` | 47 | 进入 TSV；发现线索候选。 |
| `design/content-model.md` | 138 | 进入 TSV；目标类型冲突，待人决定。 |
| `design/drafts/terminology-governance.md` | 270 | 进入 TSV；只是迁移门禁。 |
| `design/entities.md` | 78、100 | 进入 TSV；源头文献语义缺少具体记录和定位。 |
| `design/maintenance.md` | 132 | 进入 TSV；首次出现上下文为发现线索候选。 |
| `design/principles.md` | 20 | 进入 TSV；随上游发现流程分流。 |
| `design/topics.md` | 114、127、132、136、138、190、213 | 全部进入 TSV；分别覆盖字段示例、文本定义、派生示例、与映射的分工、依据声明、校验规则和待定项。 |
| `docs/superpowers/plans/2026-08-28-terminology-concept-foundations.md` | 61、66、296–298、675、701、785、799 | 已逐位置阅读；均为旧计划的去向、检索命令或验证预期，不是正式字段值，不进入 TSV。 |
| `docs/superpowers/plans/2026-08-28-terminology-project-design.md` | 29、94、144、329、367、427 | 已逐位置阅读；均是已完成计划的迁移要求或验证项，不是正式字段值，不进入 TSV。 |
| `docs/superpowers/plans/2026-08-30-governance-drafts.md` | 23、226 | 已逐位置阅读；均是草案编写边界或验证项，不进入 TSV。 |
| `docs/superpowers/plans/2026-08-31-governance-implementation-prep.md` | 40、82、107 | 已逐位置阅读；是本库存的产物、任务和下游输入说明，不进入 TSV。 |
| `docs/superpowers/specs/2026-08-27-terminology-governance-design.md` | 33、170、178 | 33 是范围说明，不进入 TSV；170 和 178 是已批准分流边界，进入 TSV。 |
| `vocab/build/label-lookup.json` | 355 | 已读取完整 JSON 记录；该单词是外部英文描述“数学发现的起源”中的普通词，不是字段或项目关系，无需迁移。 |

38 个原始命中行全部有去向：16 个正式规则、草案门禁或已批准规格位置进入 TSV；20 个计划与范围位置作为过程文档保留；1 个规格范围位置在上表单独保留；1 个 JSON 普通英语单词不属于字段。TSV 另加 3 行数据与脚本的“真实使用为零”证据，合计 19 行。

## 数据影响

当前没有逐记录数据迁移。这不表示文档字段可以保留：当前设计声称了一个正式字段和目标类型，但生成数据、生成输入、生成器和校验器都没有实现它。后续实施计划应把这一情况作为文档—数据接口对账，不得为填满空白而新建 origin 值或反推任何概念的去向。

内容模型的保留规则声称内容单元可被 origin 引用，但当前数据没有这种反向引用，且主题设计将目标限定为实体表的 publication 或 standard。该保留理由与旧字段的关系需在模式迁移计划中单独对账；本库存不改变保留规则。

## 脚本影响

`scripts/build-topics.py` 的概念构造函数和输出段均无 `origin`，重新生成也不会丢失任何现存 origin 值，因为当前没有这种值。这不授权用生成器自动构造 `discovery`、`basis` 或 `source`。

`scripts/check-topics.py` 未实现 `design/topics.md:190` 声称的目标类型校验。因此“0 处问题”只证明现有校验集通过，不证明旧字段的文档接口已被实现。后续应根据获准模式分别验证发现用途、逐值依据和实际派生，而不是补一个通用 origin 校验。

## 未读边界

本库存不新增外部事实。对 ANSI/NISO Z39.19-2005 (R2010) 的使用只限于当前仓库中已实际阅读并记录的 [Z39.19 阅读笔记](../../../sources/z39-19.md)：笔记说明 § 11.1.4 列举 term record 可包含所咨询的 source(s)，并明确该表述不自动定义项目字段。笔记“阅读范围”之外的正文未用于本次分类，不猜测未读正文。

对派生边界的理解只使用当前仓库中的 [元数据标准笔记](../../../sources/metadata-standards.md)：日常语言的“来自”不足以证明实际派生。笔记列出的 DCMI、PROV-O 和 SKOS 未读部分未被用来补出字段、模式或关系。

## 待定问题

1. 新主题的“提出文献”和“首次出现内容单元”是否只保留为候选发现记录；该记录的正式位置和结构尚未获准。
2. “源头文献”什么时候只支持概念身份、定义或其他具体值，什么时候证明记录实际由外部条目派生；每条真实记录需分别结论。
3. 内容单元与 publication 或 standard 实体两种目标类型如何对账；不能在模式中同时保留一个未分语义的通用目标。
4. `design/topics.md` 的字段示例、文本定义、校验规则和待定项如何在后续整节或整篇重写中分别去向 `discovery`、`basis`、`source` 或保持待人决定。
5. 内容单元的保留决定在去掉对旧 origin 引用的依赖后需何种独立支撑；本次不改变该保留决定。

## 验证基线

- 输入锚点：实施准备计划 SHA-256 为 `28b936359d49f5c8618d2dff63740497a766da43931fa4f47b7ad6dd9c232ecd`；来源治理草案为 `0bc61207215f35065652bb66f043ef2d11a807bbe0bc44465814e469b5671526`；术语治理草案为 `2d48c869b8a2119346739303accaaff0cbe40418d7074f29a4a18599950767d7`。
- 数据锚点：`vocab/topics.yaml` SHA-256 为 `4c746ac51b9ad585445037ee57abd34d5542a48e04f3667e3ea32866d8171993`；`vocab/entities.yaml` 为 `63020dd3edbb3a25339846943fa67d774335b866e687a7b70f8a110a3ac50ff7`；`vocab/sources.yaml` 为 `1f550993984e2ba4329828b01fcf08ddee97d7433027265207c98277173c50ff`。
- 脚本锚点：`scripts/build-topics.py` SHA-256 为 `49bd7b063005a3e9a7e7213a290fcbaa6d68597e0027ff5bb33e1365dcdbcc70`；`scripts/check-topics.py` 为 `a2c4bf725736027f128e8edf3ea93565b2b060fca23f854900c6e8f76a1e2fb8`。
- 现有校验：`python3 scripts/check-topics.py` 退出码为 0，输出 0 处问题、700 个概念、24 个数组、61 个实体、31 个来源。

