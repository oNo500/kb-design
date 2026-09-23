# 词表维护 (Vocabulary Maintenance)

`kb-vocab-maintenance` 提供 RDF 字段差异、可审阅的描述属性编辑，以及现有实体资料转换。输出是独立维护产物，不代表语义采纳、正式发布或应用采用。

## 命令入口

```sh
uv run kb-vocab-maintenance diff before.ttl after.ttl
uv run kb-vocab-maintenance import-entities \
  --source data/vocab/entities.yaml \
  --registry data/inputs/vocabulary-maintenance/legacy-entities-identity.json \
  --output output/vocabulary/legacy-entities/20260923
```

实体导入固定来源原件，保存实体与名称的稳定身份对应；原状态进入交付记录，未投影字段保留原值及回查位置。它不根据旧主题 ID 推断概念关系，不把候选变为活动记录。身份登记是后续导入的必要输入，不能删除后重新生成来替代原有身份。

当前这份交付收录 35 条旧记录，保留 19 条 active 和 16 条 candidate。`entities.ttl` 是 RDF 交付；`source/entities.yaml`、`identity.json`、`unprojected.json` 和 manifest 负责原件、身份、未投影信息和版本核对。本次未将它自动加载到 Obsidian，也未改写原 YAML。后续来源变更复用同一登记，另选新的输出目录。

编辑请求是 JSON 数组，每项指定稳定主体 IRI、属性 IRI 和替换后的完整值集。例如，已有名称资源的文字修订：

```json
[
  {
    "subject": "urn:label:existing-name",
    "predicate": "http://www.w3.org/2008/05/skos-xl#literalForm",
    "after": ["\"Revised\"@en"]
  }
]
```

```sh
uv run kb-vocab-maintenance edit prepare \
  --input baseline.ttl --changes changes.json --plan plan.json \
  --reason '已审阅的文字修订理由' --authorization 'urn:decision:reviewed-change'
uv run kb-vocab-maintenance edit apply \
  --plan plan.json --input current.ttl --output build/edited-vocabulary
```

示例中的身份、文字、理由和授权引用须替换为实际已审阅内容。授权引用只作记录；工具不验证该决定的权限或效力。计划包含基准路径、字节及图哈希、逐属性 before／after、派生投影和依赖。应用时原基准仍须存在且字节未变；更换基准须另建计划。

## 编辑范围

支持现有资源的名称文字、说明、标识、来源、语言与日期等描述属性。值使用完整 IRI 或带双引号的规范 N3 字面值，不使用前缀缩写；既有语言不会被自动改标，也没有固定的中英文过滤。

采用 XL 的名称从原 Label IRI 的 `literalForm` 编辑；同一名称的全部用法共同参与投影更新，同文的不同 Label 不合并。普通投影不能独立覆盖 XL。空白节点字段、关系结构、类型、采纳状态、停用和资源建立／删除不在执行范围内；全图差异仍可显示这些字段的变化。

来源文件不会被覆盖。上游非目标改动保留在合成图中；目标旧值、资源存在性、类型或共享名称用法不符时拒绝应用。冲突以非零退出码和 JSON 输出，给出基准、当前值及计划值。合成图的名称约束冲突也会拒绝产物。

## 交付内容

编辑输出目录固定包含：

| 文件 | 内容 |
|---|---|
| `baseline.ttl` | 审阅基准的原始字节 |
| `current.ttl` | 本次上游输入的原始字节 |
| `plan.json` | 本次执行的计划原件 |
| `vocabulary.ttl` | 合成后的 RDF 图 |
| `version-diff.json` | 当前输入到编辑结果的字段差异 |
| `upstream-diff.json` | 原基准到当前输入的字段差异 |
| `manifest.json` | 输入、完整文件哈希、检查范围与未发布状态 |

相同计划和相同输入重跑时，逐文件、逐字节核对全部产物后复用；缺失、损坏、额外文件及输入漂移均拒绝覆盖。该机制只覆盖本步骤，不构成完整维护工作流的恢复能力。

## 验证范围

编辑前后检查完整合成图中的 XL 稳定身份及单一文字、普通标签投影、按完整语言标签的首选文字唯一性，以及首选／别名／隐藏名的文字互斥。检查范围写入 manifest；全图 SHACL、概念语义、外部授权有效性和上游变更采纳不由本步骤证明。

RDF 读取和比较使用 RDFLib，保留数值字面值的词法形式。RDFLib 即使关闭规范化仍会改写的值，例如含待折叠空白的 `xsd:token`，会被明确拒绝；不静默改写后宣称图相等。输入可使用 Turtle，输出使用排序后的完整 RDF 三元组，仍为有效 Turtle。

```sh
uv run --with pytest pytest packages/kb-vocab-maintenance/tests -q
uv lock --check
```
