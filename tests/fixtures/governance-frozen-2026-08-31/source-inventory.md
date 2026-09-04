# 来源派生库存

## 库存边界

本库存只盘点当前正式数据和配置中直接名为 `source` 的字段，逐记录判断其实际语义。扫描覆盖 `vocab/*.yaml` 的全部 1,482 个 `source` 键：其中 726 个是本库存对象，另 756 个位于旧 `match` 项内，属于独立的 `match` 库存，不在本表重复。脚本中的字段字符串不是正式记录，只用于核对生成与校验路径。

当前身份固定为分支 `feat/terminology-governance`、HEAD `9e7b411c23e890d13d70fc16d443b760313126c4`。本库存没有新增外部事实；判断依据只来自当前正式数据、[来源治理草案](../../../design/drafts/source-governance.md)、[术语治理草案](../../../design/drafts/terminology-governance.md)、[主题词表设计](../../../design/topics.md)、[层级结构](../../../design/hierarchy.md)、[来源名称规范表](../../../design/sources-registry.md)、[内容模型](../../../design/content-model.md)、[元数据标准笔记](../../../sources/metadata-standards.md)、构建输入和脚本。外部材料的已读与未读边界沿用现有来源笔记，本次不猜未读正文。

TSV 接口严格使用准备计划规定的九列。身份键为“文件＋位置＋对象”，不得以字符串、目录或次数代替语义判断。

## 判断规则

- “实际派生”只用于当前设计和记录上下文明确说明概念从外部结构复制，且同记录存在同来源 `match` 的概念记录。`match.id` 只作为 `source.item` 候选；它不自动成为已核准的 `item` 或 `locator`。
- “来源名称”只用于现行主题数组。现行设计明确说明这种数组按来源分组并显示来源名；标量值没有草案 `source` 所需的 `item`、`locator` 和 `basis`。
- “项目 self”只用于八个由范围决定的顶层概念。项目决定与外部派生分离，不能迁入 `source`。
- 两个载体数组是本地把 LOM 单一清单拆开的分析结果，不是来源自身给出的两个数组。`forms-presentation` 还包含 Wikidata 来源的 `cheat-sheet`，因此两项都记“含义不明”，不猜成实际派生或普通参考。
- 现行 `role: structure` 只满足现行资格。草案要求角色另有 `status` 与 `decision`；当前数据没有这些字段，因此不把现行登记自动提升为草案中的 `approved` 用途。

## 盘点结果

| 分类 | 记录数 | 结论 |
|---|---:|---|
| 实际派生 | 692 | 概念复制关系明确，但全部缺 `source.locator`、`source.basis` 和草案 `approved` 用途证明，均需复核 |
| 普通参考 | 0 | 当前直接 `source` 字段中未发现；普通参考不能伪装成派生 |
| 来源名称 | 24 | 仅主题数组的来源分组标识；目标表达待人决定 |
| 项目 self | 8 | 仅八个顶层范围决定；不迁入 `source` |
| 含义不明 | 2 | 两个载体数组；本地拆分与来源字段语义不一致 |
| 合计 | 726 | 身份唯一且字段完整 |

状态分布为“需要复核” 692 条、“待人决定” 34 条、“可机械迁移” 0 条、“无需迁移” 0 条。没有任何记录因字符串相同或次数集中而取得机械迁移资格。

## 用途资格

| registry | 实际派生数 | 现行资格 | 草案缺口 |
|---|---:|---|---|
| `asvs` | 16 | `structure` | locator 与 source.basis 均缺；草案角色状态和决定未建立 |
| `atlas` | 16 | `structure` | locator 与 source.basis 均缺；草案角色状态和决定未建立 |
| `attack` | 15 | `structure` | locator 与 source.basis 均缺；草案角色状态和决定未建立 |
| `cs2023` | 178 | `structure` | locator 与 source.basis 均缺；草案角色状态和决定未建立 |
| `cwe` | 10 | `structure` | locator 与 source.basis 均缺；草案角色状态和决定未建立 |
| `gbt-13745` | 427 | `structure` | locator 与 source.basis 均缺；草案角色状态和决定未建立 |
| `owasp-llm-top10` | 10 | `structure` | locator 与 source.basis 均缺；草案角色状态和决定未建立 |
| `rfc-1122` | 4 | `structure` | locator 与 source.basis 均缺；草案角色状态和决定未建立 |
| `swebok` | 16 | `structure` | locator 与 source.basis 均缺；草案角色状态和决定未建立 |

692 条实际派生记录都有且仅有一条同来源 `match`，关系值均为现行记录实际保存的 `exactMatch`。候选 `registry/item` 组合有 689 个唯一值；`rfc-1122:1.1.3` 同时用于 `application-layer`、`transport-layer`、`internet-layer` 和 `link-layer`，当前值更像共同定位而非四个唯一条目标识，须逐项复核，不能自动填入 `source.item`。

## 生成路径

`vocab/topics.yaml` 的 700 个概念和 24 个数组由 `scripts/build-topics.py` 生成。输入分为 `cs2023-kus.json`、`gbt-13745.json`、`extra-arrays.json`，以及脚本内的 `TOPS` 和 `LIS` 常量。对 HEAD 的临时副本重新运行构建后，输出与当前 `vocab/topics.yaml` 逐字节相同，SHA-256 为 `4c746ac51b9ad585445037ee57abd34d5542a48e04f3667e3ea32866d8171993`。

生成器的 `add()` 在同一 `id` 再次出现时追加 `match` 和数组成员关系，但保留首次写入的单值 `source`。因此 `cryptography` 同时进入 ASVS 数组、`software-design` 与 `software-construction` 同时进入 SWEBOK 数组，但三条记录的 `source` 仍为 `cs2023`。本库存不凭数组和同名推断新增第二个 `source`；是否需要表达多重实际派生，须在人决定草案单值接口如何应用后处理。

`vocab/forms.yaml` 不是 `build-topics.py` 的输出。`scripts/check-topics.py` 会读取它并校验各 form 的 `match.source`，但没有校验 `forms.arrays.source`，所以两个含义不明数组目前不会被现行校验器发现。

## 完整性

- TSV 数据行：726；身份键唯一：726；重复：0。
- 九列非空：726／726；空字段：0。
- 状态值域只含“可机械迁移”“需要复核”“待人决定”“无需迁移”；实际出现 2 种，非法值：0。
- 草案分类只含任务指定的五类；实际出现 4 种，非法值：0。
- 692 条实际派生均能解析到现行 `sources.yaml`，且现行角色含 `structure`；缺失或用途不符：0。
- 692 条实际派生均有同来源 `match` 候选 item；缺失或多于一条：0。
- 当前 TSV SHA-256：`0cb9b6df2f218629eb0dedb05ac5c83030b89e4d8dbca7580a8ccfee4b323c1f`。

## 输入哈希

| 输入 | SHA-256 |
|---|---|
| `vocab/topics.yaml` | `4c746ac51b9ad585445037ee57abd34d5542a48e04f3667e3ea32866d8171993` |
| `vocab/forms.yaml` | `8343b951a7bdf6cf231aa1bac326e92be4ece7d4af3846b9a8acba11a88ac78f` |
| `vocab/sources.yaml` | `1f550993984e2ba4329828b01fcf08ddee97d7433027265207c98277173c50ff` |
| `vocab/entities.yaml` | `63020dd3edbb3a25339846943fa67d774335b866e687a7b70f8a110a3ac50ff7` |
| `scripts/build-topics.py` | `49bd7b063005a3e9a7e7213a290fcbaa6d68597e0027ff5bb33e1365dcdbcc70` |
| `scripts/check-topics.py` | `a2c4bf725736027f128e8edf3ea93565b2b060fca23f854900c6e8f76a1e2fb8` |

## 待定问题

- 草案中的 `source` 是单个对象；三个合并概念存在第二来源数组和第二来源 `match`。是否把它们解释为多重实际派生、只保留首个派生，或调整正式结构，当前草案和数据没有给出答案。
- RFC 1122 四层共用 `match.id: 1.1.3`。须确认每层的外部 `item` 与可重复 `locator`，不能把共同章节号同时当成四个唯一条目。
- 692 条实际派生都缺逐项 `locator` 和 `source.basis`；现行 `structure` 角色也没有草案所需的批准状态与决定。补证和角色批准不能合并为机械迁移。
- 24 个主题数组当前用来源名标识分组，来源治理草案没有规定来源名称型数组的目标字段。迁移前须决定保留方式，不能复用实际派生 `source` 冒充。
- 两个载体数组是本地分析分组，却填写 `source: lom`；其中呈现形式数组还混入 Wikidata 项。目标结构、成员边界和是否继续保留这两个数组均待人决定。
