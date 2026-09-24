# 词表维护 (Vocabulary Maintenance)

`kb-vocab-maintenance` 提供 RDF 字段差异、可审阅的描述属性编辑、旧实体资料转换与统一实体词表构建。使用资格按显式配置及其固定决定计算；构建不改写来源状态，不代表正式发版或应用加载。

## 命令入口

```sh
uv run kb-vocab-maintenance diff before.ttl after.ttl
uv run kb-vocab-maintenance import-entities \
  --source data/vocab/entities.yaml \
  --registry data/inputs/vocabulary-maintenance/legacy-entities-identity.json \
  --output output/vocabulary/legacy-entities/20260923
```

## 实体收录

`import-entities` 固定旧 YAML 原件，保存实体与名称的稳定身份对应。身份登记是后续导入的必要输入，不能删除后重新生成来替代原有身份；未投影字段保留原值及回查位置。旧资料交付收录 35 条记录，原有 19 条 active 与 16 条 candidate 均保留，不根据旧主题 ID 推断概念关系。

`build-entities` 将配置所列实体交付合为一份 `entities.ttl`，保留全部 RDF 字段、实体与名称 IRI、字面值词法形式及完整原件。实体清单只来自来源 manifest 或实体审计记录，不把 PROV 来源资源及 XL Label 当作实体。

```sh
uv run kb-vocab-maintenance build-entities \
  --config data/inputs/vocabulary-maintenance/entities.json \
  --source-root . \
  --output output/vocabulary/entities/versions/2026-09-24-r1
```

配置使用 `schema_version: 1`、`policy: basic-fields-v1`，并固定决定文件及各来源 manifest 的 SHA-256。`authority.path` 和 `sources[].directory` 相对 `--source-root`；来源声明 `key`、`manifest_sha256`、`entity_file`，有实体审计时再声明 `audit_file`。来源 manifest 必须完整列出交付内每份原件的文件哈希，额外文件、缺失、符号链接、内容漂移及重名 JSON 键均拒绝。

实体须有稳定绝对 IRI、明确的既有实体类别、非空可用首选名及可定位的固定来源。普通首选名与完整 XL 首选名均可，保留实际语言，未标语言另列诊断。缺项记录保留并说明不可用原因；明确停用记录不重新启用。candidate、`facts_verified: false` 不单独阻止先用，也不被改写为 active。主题、定义、厂商与外部映射不作为附加必填项。

名称相同的不同 IRI 不合并，manifest 列出同名提示。共享 IRI 的主体及可达描述必须一致；冲突的名称、投影或描述直接拒绝。完整同构来源图可重复引用；部分重叠来源图若包含共享空白节点描述，须另作明确处理，本命令拒绝自动合并。

名称检查复用维护包既有规则。仅检查用临时图补足 XL 蕴含的普通标签，交付图不增加这些隐含字段。缺失或空白的 XL 名称保留原图，逐项报告，并使引用它的实体不可用；这些记录从临时冲突检查图排除，因此检查通过不等于原图完整符合。既存普通投影与 XL 文字矛盾、多 literalForm、同语言冲突首选名及跨名称角色文字冲突仍拒绝。

统一交付包含一份供消费的 `entities.ttl`、构建配置、`build-context.json` 中固定的原来源根目录、决定原件、`sources/<key>/` 下各来源完整原件及 manifest。统一 manifest 记录逐实体来源状态、基本字段检查、可用与不可用清单、具体原因和同名提示；这些 JSON 是管理记录。验证时从固定配置与构建上下文重算来源路径、RDF 解析基准及其他来源元数据，逐字段拒绝 manifest 中的不一致；本地哈希核对不证明外部来源真实性。空白节点诊断使用规范化图中的标识，保证同输入重试一致。构建期间再次核对输入，发布到新版本目录；相同输入重跑逐文件核对字节后复用，不覆盖受损、缺失或额外内容。

显式添加 `--current output/vocabulary/entities/current` 可在完整交付复验后创建或替换符号链接。入口必须位于交付目录外，已存在的普通目录或文件会被拒绝；命令不调用 Obsidian 刷新，不修改文章或原 YAML。

## 字段编辑

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
