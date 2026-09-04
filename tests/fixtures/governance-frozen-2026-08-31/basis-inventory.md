# basis 库存

## 库存范围

本库存冻结于 `feat/terminology-governance` 分支的 `9e7b411c23e890d13d70fc16d443b760313126c4`。逐值表见 [basis-inventory.tsv](basis-inventory.tsv)，其 SHA-256 为 `3da438227ee676f0d2c5e31ac16c73a3bb4a5d10716b15f175fd81257642c43c`。

库存包含三类对象：正式词表数据中实际存在的 `basis` 叶值、生成配置中直接控制 `basis` 生成的值，以及现行设计文档中作为真实字段展示的示例值。每一行都保留文件、行号、对象路径、原值形态、被支持值的上下文、缺失项、拟议去向、决策级别和状态。

逐值分类引用已接受但尚未生效的[来源治理草案](../../../design/drafts/source-governance.md)与[术语治理草案](../../../design/drafts/terminology-governance.md)。两份草案的 SHA-256 分别为 `0bc61207215f35065652bb66f043ef2d11a807bbe0bc44465814e469b5671526` 和 `2d48c869b8a2119346739303accaaff0cbe40418d7074f29a4a18599950767d7`。拟议去向不是迁移决定，库存没有使草案或字段生效。

本次没有使用新的外部事实。配置注释中的“官方译文”和核对日期只按当前文件自述记录，没有在本轮重新核验其外部正文。

## 行的身份

TSV 使用准备计划固定的九列接口。逐值身份为“文件、位置、对象路径”的组合；同一行内的 `basis.zh`、`basis.en`，以及列表中的多个 `basis` 值分别建行，不按相同字符串合并。

语义分类来自当前对象上下文，不来自目录、字符串或次数。例如，`vocab/topics.yaml` 中的 `source` 只有在逐项确认它位于标签依据路径、相邻 `source` 非 `self`、并且存在恰好一个同登记 `match` 条目后，才记为实际派生线索。相同的 `source` 字符串在生成配置中另记为生成标记。

## 库存结果

各写入位置的逐值数量如下。

| 范围 | 文件 | 逐值数 | 值的分布 |
|---|---|---:|---|
| 正式数据 | `vocab/topics.yaml` | 1400 | `source` 702；`none` 614；紧缩来源字符串 84 |
| 正式数据 | `vocab/entities.yaml` | 64 | 紧缩来源字符串 51；`self` 13 |
| 正式数据 | `vocab/forms.yaml` | 32 | `none` 16；紧缩来源字符串 16 |
| 生成配置 | `vocab/build/extra-arrays.json` | 1 | `zh_basis: source` 1 |
| 字段展示 | `design/maintenance.md` | 2 | 紧缩来源字符串 1；`self` 1 |
| 字段展示 | `design/topics.md` | 2 | 紧缩来源字符串 2 |
| 合计 | 六个文件 | 1501 | 需要复核 1487；待人决定 14 |

正式数据共有 1496 个 `basis` 叶值。按现行值形态分为 `source` 702 项、`none` 630 项、`self` 13 项和紧缩来源字符串 151 项。加上配置与文档展示后，TSV 共 1501 项，其中紧缩来源字符串 154 项、`self` 14 项，另有一个生成配置标记。

## 上下文核对

三个正式数据文件的 `basis` 映射覆盖情况是：`vocab/topics.yaml` 700／700 个概念、`vocab/entities.yaml` 61／61 个实体、`vocab/forms.yaml` 16／16 个载体概念。库存范围内没有缺失整个 `basis` 映射的记录。

逐类上下文核对得到以下结果。

- 702／702 个 `source` 都支持现存标签，记录的相邻 `source` 均非 `self`，并各有恰好一个相同来源登记的 `match` 条目。相邻条目只能提供派生与定位线索，不能替代逐值 `basis`。
- 630／630 个 `none` 都对应缺失的目标语言标签。它们是“不译或没有该值”的现行标记，不是外部依据。
- 13／13 个正式 `self` 都位于 `candidate` 实体的 `subjects` 依据路径。它们记录本库判断尚无外部依据，不能迁入草案 `basis`。
- 151／151 个正式紧缩来源字符串的来源前缀都已在 `vocab/sources.yaml` 登记。登记存在不证明定位充分、内容仍支持当前值或项目已经批准迁移。
- 配置中的一个 `zh_basis: source` 位于 `artificial-intelligence.owasp-llm-top10` 对象。它经 `scripts/build-topics.py` 生成正式 `basis.zh: source`，因此单独列出；生成后的十个字符串值已经按各自正式对象路径包含在 1400 项中，没有把配置行与生成值合并。

## 结构缺失

当前正式数据没有任何一项使用草案提出的结构化 `basis.entity`、`basis.locator` 或 `basis.checked`。1496 个正式叶值的结构化定位数为 0，逐值 `checked` 数为 0。

151 个正式紧缩来源字符串中，23 项只有来源 id，没有位置线索；128 项在字符串中还带有条目或位置线索，其中包括 77 个 Wikidata 条目、25 个 `scope` 线索和 21 个带 `#` 的位置线索。条目号、`scope` 或 `#` 后文本只记作当前线索；库存没有把它们自动认定为可重复定位的草案 `locator`。`vocab/sources.yaml` 或来源实体上的 `checked` 也没有被当作具体值的 `basis.checked`。

`source`、`none` 和 `self` 共 1345 个正式值都不是草案允许的完整 `basis` 项。`source` 还缺实际派生关系自己的 `source.locator` 与 `source.basis`；`none` 和 `self` 则没有可迁入 `basis` 的来源实体与定位。

## 拟议去向

逐值表只使用草案已经提出的字段与记录层次，未填写任何具体 schema、id、周期、阈值、范围或来源改档。

| 当前形态 | 拟议去向 | 状态 |
|---|---|---|
| 紧缩来源字符串 | 保留现有来源线索；实际复核后拆为 `basis.entity`、`basis.locator` 和按条件需要的 `basis.checked`；无法定位时交人决定 | 需要复核 |
| `source` | 先确认真实派生；成立时迁入 `source.registry`、`source.item`、`source.locator`、`source.basis`，并为被支持的具体值另补 `basis` | 需要复核 |
| `none` | 不迁入 `basis`；不为缺失形式建立空术语记录；将来需要该语言形式时重新取得逐值依据 | 需要复核 |
| `self` | 不迁入 `basis`，保持未获准；取得外部依据和定位后再提案 | 待人决定 |
| 生成配置标记 | 迁移生成链时停止把 `source` 写成 `basis`；按逐值复核结果分别生成 `source` 与 `basis` | 需要复核 |

所有拟议去向均为二级事项。没有一项标成“可机械迁移”，也没有因来源字符串已登记、条目号存在或相同值重复而自动提升状态。

## 文档边界

`design/maintenance.md` 的 `eslint` 与 `uv` 示例，以及 `design/topics.md` 的 `sql-injection` 示例，明确展示现行 `basis` 字段和值，因此四个叶值进入 TSV。它们与正式数据身份分开；文档示例不能替代正式记录的证据。

以下内容只在本报告列为边界，没有混入逐值 TSV：

- 普通 prose 中对 `basis` 字段、规则、计数或历史的讨论，包括治理、维护、决定记录、概念文、来源笔记和 `vocab/CHANGELOG.md`；
- `design/drafts/source-governance.md` 中尚未生效的结构化目标示例；
- `design/drafts/division-characteristics.md` 中指向尚不存在正式文件的草案示例；
- Superpowers 规格与计划中的接口示例、命令和验收文字；
- `scripts/build-topics.py`、`scripts/check-topics.py` 与 `scripts/lookup-labels.py` 中没有独立当前对象身份的变量、分支和输出模板。

脚本虽然不另建逐值行，但它们会生成或校验正式值。后续实施若只迁移 `vocab/topics.yaml` 而不同时处理生成逻辑，重新生成会恢复 `source`、`none` 和紧缩字符串；这是实施计划必须显式处理的写集风险。

## 库存疑虑

- `source` 的相邻 `match` 条目可以帮助找到外部对象，但当前没有逐值定位和核对日期；不能据此直接生成完整 `source` 或 `basis`。
- `none` 当前占用 `basis` 语言项表达“不译”。草案目标是不建立没有形式的术语记录；旧对象与新记录之间的逐项对账仍须在迁移计划中明确，不能靠删除 `none` 完成。
- `self` 的正式对象都处于 `candidate`，但“保持未获准”不决定后续补证、保留或其他处置；这些对象继续待人判断。
- 紧缩字符串中的 `scope`、条目号和 `#` 位置粒度不一致。是否能重复定位支持当前具体值，只能逐项打开来源确认。
- `vocab/forms.yaml` 没有相邻记录级 `source`，只有 `match`。库存把 `match` 作为上下文而非派生结论，未替它补造 `source`。
- 现行字段展示与正式数据存在重复对象或纯示例对象。实施时须同步文档，但不能把示例行计入正式数据迁移数量。

## 自查结果

TSV 有 1501 个数据行、九列；对象身份重复 0，空字段 0。状态值只有“需要复核”和“待人决定”，均在准备计划允许的值域内。库存只写本目录的 `basis-inventory.tsv` 与 `basis-inventory.md`，没有修改受 Git 跟踪文件。
