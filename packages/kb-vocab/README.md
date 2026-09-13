# 词表操作 (KB Vocab)

`kb-vocab` 使用 RDFLib 导入、读取、查询、校验和组织 Turtle／SKOS 数据，独立于旧核心包。`build-system` 完整保存六份来源副本，按第 3 版规范生成一份自有词表和八个领域分组，直接执行规则，不运行人工审查或 AI 分析。跨来源对应审查是独立的可选能力。正式编辑、正式采纳、YAML 切换和应用同步尚未实施。

## 来源与结果

[当前自有词表](../../output/vocabulary/current/index.md)提供稳定的数据入口；[独立来源入口](output/index.md)保留六份来源及查询状态。

| 来源 | 输入与当前结果 | 保留的限制 |
|---|---|---|
| [IEEE](output/ieee-2025-resolved/index.md) | 原文提取 JSON；7,619 个概念、4,871 个替代标签 | 固定规则排除 202 对间接祖先 RT；59 组 AND 和两项名称异常继续隔离 |
| [Cognitive Atlas](output/cognitive-atlas-2026-09-13-reviewed/index.md) | API 转录 JSON；918 个概念、857 个独立任务资源 | 1,422 条带实验条件的任务断言保留在账本 |
| [MSC2020](output/msc2020/index.md) | 官方 TSV；6,603 个概念、6,540 条直属层级、63 个顶层概念 | 原代码、名称和完整说明分开保留；交叉引用不自动变成语义关系 |
| [ERIC](output/eric-2025/index.md) | 官方 XML／ZIP；4,578 个概念、6,527 个替代标签 | 692 条多目标同义记录、132 条停用记录及有问题的关系保留在账本；52 对 S27 冲突暂隔离 |
| [PhilPapers](output/philpapers-snapshot/index.md) | 第三方 JSON；6,134 个概念、7,743 条直属层级 | 官方版本未知；主要父分类保留为来源元数据；一条空名称不补造 |
| [UNESCO](output/unesco-native/index.md) | 官方原生 Turtle；4,500 个概念、95 个集合 | 来源原图保留；7 项 S13 标签冲突仍可核对，旧报告中的 780 项工具 profile 误限已在当前校验器纠正 |

各行数字表示当前快照的处理结果，不证明领域覆盖完整或已正式采纳。知识覆盖文献 CS2023、IFLA、CWPA、tekom 暂缓处理。

## 命令用法

以下命令均从仓库根目录执行。

```bash
uv sync --all-packages --locked
uv run kb-vocab show packages/kb-vocab/output/ieee-2025-resolved/vocabulary.ttl LLM
uv run kb-vocab find packages/kb-vocab/output/msc2020/vocabulary.ttl learning --limit 10
uv run kb-vocab validate packages/kb-vocab/output/msc2020/vocabulary.ttl
```

`show` 接受完整概念 URI 或精确名称；同名多概念时要求使用 URI。`find` 不区分大小写，不合并概念。显示的关系为显式边，不自动列出全部祖先。

四个结构化来源导入命令如下。将 `SOURCE_FILE` 替换为具体快照文件路径；输入位置可从上表结果中的 `source.json` 查询。输出目录必须不存在。

```bash
uv run kb-vocab import-msc SOURCE_FILE --output packages/kb-vocab/output/msc-new
uv run kb-vocab import-eric SOURCE_FILE --output packages/kb-vocab/output/eric-new
uv run kb-vocab import-philpapers SOURCE_FILE --output packages/kb-vocab/output/philpapers-new
uv run kb-vocab import-unesco SOURCE_FILE --output packages/kb-vocab/output/unesco-new
```

输入分别是 `MSC_2020.csv`（实际为 TSV、cp1252 编码）、`ERICThesaurus2025.zip` 或解压 XML、`categories.json`、UNESCO `.ttl`。相邻存在获取凭据时核对凭据及文件哈希；没有凭据时记录为 `local-file-only`，不声称已核实来源。

IEEE 和 Cognitive Atlas 使用已生成的来源转录：

```bash
uv run kb-vocab import-ieee \
  packages/kb-sources/output/ieee-thesaurus/2025-07/thesaurus.json \
  --output packages/kb-vocab/output/ieee-new
uv run kb-vocab import-cognitive-atlas \
  packages/kb-sources/output/structures/cognitive-atlas-2026-09-13/source.json \
  --output packages/kb-vocab/output/cognitive-new
```

Cognitive Atlas 转录由 `kb-sources export-cognitive-atlas` 从其已校验的 API 快照生成，源包的 [README](../kb-sources/README.md) 提供用法。

## 词表构建

[组织配置](../../data/inputs/vocabulary/knowledge-system.json)、[来源清单](../../data/inputs/vocabulary/sources.json)与 [SHACL 规则](../../data/inputs/vocabulary/shapes.ttl)分别规定组织选择、来源文件及字段约束。配置版本为 2，字段规范版本为 3；生成结果不再建立八个领域 ConceptScheme。

构建器保留全部来源概念的 IRI，将它们统一纳入 `urn:kb-vocab:scheme:kb-design`。八个领域使用 `urn:kb-vocab:group:<领域标识>` 的 Collection，依据原配置的完整来源或分支规则生成 member。reference_only 只记录依据，不产生分组成员；未分组概念仍属于自有词表。

从仓库根目录执行：

```bash
uv run kb-vocab build-system \
  --config data/inputs/vocabulary/knowledge-system.json \
  --output-root output/vocabulary
```

每次创建新的 `output/vocabulary/versions/<构建标识>/`，完成来源对账、图校验、SHACL、Turtle 往返与哈希核对后，原子切换 `current`。`--build-id` 可指定未使用的版本名；`--output NEW_DIRECTORY` 只生成独立版本，与 `--output-root` 互斥。失败保留旧入口，历史版本不删除。

| 内容 | 路径或文件 |
|---|---|
| 当前完整词表 | `output/vocabulary/current/vocabulary.ttl` |
| 组织声明 | `organization.ttl`：一个 Scheme、八个 Collection、统一 inScheme 和分组 member |
| 领域分图 | `domains/*.ttl`：同一词表的分组子集及必要引用上下文 |
| 未分组数据 | `unassigned.ttl`：仍属于自有词表的未分组概念 |
| 概念与分组对账 | `coverage.json`：来源、唯一词表、分组和命中的规则 |
| 字段转换 | `transformation-ledger.jsonl`：被归档、过滤、归一和派生的三元组及依据 |
| 独立语句对账 | `accounting.json`：独立核对来源语句、转换记录和实际投影，不使用生成器计数代替证明 |
| 版本差异 | `version-diff.json`：与上一版本比较的概念增删及逐节点字段变化；首次构建标明无基线 |
| 环境恢复 | `recovery/`：实际工具代码、项目元数据、运行依赖版本、环境信息及恢复入口 |
| 转换统计 | `normalization.json`：逐源去向数量、语言过滤和反向关系派生数量 |
| 结构迁移 | `migration.json`：旧领域 Scheme 到独立 Collection 的对应，不使用 exactMatch |
| 自动校验 | `validation.json`、`shacl-report.ttl`、`warnings.json` |
| 来源及构建指纹 | `provenance.json`、`manifest.json`、`inputs/` 和 `sources/` |

主图只保留英文、中文及合法语言变体的文字。未标语言的原值、代码、日期和标识保留，不自动猜测语言。六份来源原字节副本完整保留；来源 Scheme 元数据、旧 inScheme、旧顶层以及其他语言文字的去向逐项记录，不能声称主图仍包含全部原始三元组。

broader／narrower、related 对称关系以及已有来源分组互反关系由规则归一，不做领域含义判断。冗余的概念类别文字 concept 不再重复输出；任务标识 task 继续保留。历史、停用、替代和映射只保留有依据的值，缺少时省略，不制造新历史或语义决定。

SHACL 使用 pySHACL，对本地 Graph 运行；不加载 imports、不联网、不推理、不运行 JavaScript。来源无名称概念、空任务名和过滤后无正文的本地说明资源作为警告保留；生成的自有词表与领域分组必须有名称。自有词表范围由配置明确，同名概念只作提示，不自动合并。

领域成员必须按对应 Collection 的 member 统计。边界引用可以带有 Concept 类型和同一词表的 inScheme，但不因此成为该领域成员；各领域数量也不能直接相加。完整主图执行 SHACL 和图约束，领域分图使用相同的已校验字段值，并另作关系引用校验；独立分图不代表整份词表完整性。

`kb-vocab validate FILE` 保留原有的基础图校验用途；本规范的完整发布门禁在 build-system 内执行，结果及规则快照随版本保存。源图的真实错误另行报告；原先将 Collection 名称及 inScheme 拒绝的 profile 限制已经纠正，不再产生那批工具错误。

读取或回退：

```bash
uv run kb-vocab show output/vocabulary/current/vocabulary.ttl LLM
uv run kb-vocab activate-system --output-root output/vocabulary --version BUILD_ID
```

应用一次读取多个文件时先解析 current 的目标目录，避免跨版本混读。切换重新验证产物文件集、哈希和发布门禁；旧格式构建仍按其原合同验证以支持回退。写锁和符号链接替换提供同文件系统的原子可见性，不宣称崩溃持久性。

## 归档重放

新构建的 `inputs/config.json` 只引用包内 `catalog.json`、`shapes.ttl` 与 `sources/` 副本，整个版本目录可以移动后重建：

```bash
uv run kb-vocab build-system \
  --config output/vocabulary/current/inputs/config.json \
  --output packages/kb-vocab/build/replayed-vocabulary
```

输出目录必须尚不存在。`inputs/original-config.json` 保存最初组织配置；`invocation-config.json` 保存本次调用配置；`original-catalog.json` 保存本次清单。可重放配置只调整文件位置，原配置摘要与领域、名称、语言及来源指纹必须一致。组织声明引用最初配置摘要，来源解析基准由清单的 `base` 保留。版本比较的上一份主图保存在 `inputs/previous.ttl`，首次构建没有该文件。

独立对账核对来源语句、转换记录和实际投影，拒绝遗漏、伪造去向、重复派生和无依据新增值。构建清单版本 4 将对账、版本差异和环境恢复材料纳入文件哈希及切换门禁；旧构建仍按原合同支持回退。

## 身份更新

来源更新时，ERIC、IEEE 和 Cognitive Atlas 使用 `--identities OLD_SOURCE/vocabulary.ttl` 指定上一份来源词表及其相邻 manifest，不使用合并主图代替来源身份依据。原 URI 继续保留，新条目使用来源命名空间内的确定性 UUID5，不把整份文件哈希或 PDF 条目序号作为概念身份。

| 来源 | 明确对应的依据 | 自动更新的边界 |
|---|---|---|
| ERIC | 原文中的准确首选名称 | 修改说明不换 ID；旧名称消失时停止，不猜测改名或删除 |
| IEEE | 原文名称的哈希，不使用页内编号 | 条目重新编号不换 ID；旧名称消失时停止 |
| Cognitive Atlas | 原有来源 ID | 新增记录允许；旧 ID 消失或概念与任务类型改变时停止 |
| UNESCO、PhilPapers、MSC2020 | 继续沿用原生 IRI、分类 ID 或本版分类代码 | 不新增语义匹配规则 |

旧名称准确匹配只是已采用的工程对应规则，不证明定义变化必然保持同一含义。拆分、合并和无法明确判断的改名不自动处理。已批准的固定来源冲突规则仍受原指纹限制，不自动套用到新版。

```bash
uv run kb-vocab import-eric NEW_XML_OR_ZIP \
  --identities OLD_SOURCE/vocabulary.ttl --output NEW_SOURCE_DIRECTORY
uv run kb-vocab diff OLD_BUILD/vocabulary.ttl NEW_BUILD/vocabulary.ttl
```

`build-system --output-root` 自动与当前版本比较。上一版概念 URI 出现丢失时拒绝自动切换；差异命令仍可独立检查两个候选文件。更新会保留已有身份，不自动把新 ID 当成旧 ID 的替代。首次创建独立来源不携带旧身份，不得把它冒充既有来源的连续更新。

## 环境恢复

新构建保存 `recovery/tool/` 中的实际代码和项目元数据、`requirements.txt` 中的完整运行依赖版本，以及 Python 和平台信息。在仓库或前次归档可取得时，也保留 `uv.lock`。恢复不依赖原工作区的可编辑安装。

```bash
python3 output/vocabulary/current/recovery/restore.py /tmp/kb-vocab-restored
/tmp/kb-vocab-restored/bin/python output/vocabulary/current/recovery/run.py \
  build-system --config output/vocabulary/current/inputs/config.json \
  --output /tmp/kb-vocab-rebuilt
```

环境与输出目录必须尚不存在，环境必须建在构建归档之外。恢复需要 `uv`、指定 Python 及依赖下载或本地缓存；不包含操作系统镜像和完全离线安装包。`run.py` 禁止向归档写入字节码缓存。

同一输入、规则和工具版本的词表 RDF 图可重建，不承诺 Turtle 字节或诊断空白节点标识完全一致。本轮不迁移旧 YAML 消费者，也不以工程校验证明八个领域知识覆盖完整。

## 查询接口

SPARQL 查询文件示例：

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?parentLabel WHERE {
  ?concept skos:prefLabel "Large language models"@en ;
           skos:broader ?parent .
  ?parent skos:prefLabel ?parentLabel .
}
ORDER BY ?parentLabel
```

```bash
uv run kb-vocab query packages/kb-vocab/output/ieee-2025-resolved/vocabulary.ttl --query-file query.rq
```

也支持 `--sparql 'SELECT …'`。仅允许本地 SELECT，拒绝 UPDATE、SERVICE 和 FROM。所有命令输出 JSON；执行失败或 `validate` 不通过时退出码为 1。UNESCO 导入成功仅表示原图已接入，其 `validation.valid` 仍为 `false`。独立安装后也可调用 `kb-vocab` 或 `python -m kb_vocab`。

## 对应审查

本节是可选的跨来源对应工作流，不属于 `build-system` 的前置条件或执行步骤。

审查从来源目录中的全部显式 `skos:Concept` 建立索引，保留无名称概念及来源中的停用概念。同语言的首选名、替代名经 Unicode NFC、空白和大小写归一后，相同名称产生跨来源候选；标签相同不证明概念等价，候选也不预选 `exactMatch`。名称不同的关系可以用 `propose` 提交。

在 `packages/kb-vocab/catalog.json` 中列出参与审查的来源。路径相对目录文件解析；`directory` 读取其中的 `vocabulary.ttl`，也可用 `file` 指向本地 Turtle：

```json
{
  "sources": [
    {"name": "ieee", "directory": "output/ieee-2025-resolved"},
    {"name": "cognitive-atlas", "directory": "output/cognitive-atlas-2026-09-13-reviewed"},
    {"name": "msc2020", "directory": "output/msc2020"},
    {"name": "eric", "directory": "output/eric-2025"},
    {"name": "philpapers", "directory": "output/philpapers-snapshot"},
    {"name": "unesco", "directory": "output/unesco-native"}
  ]
}
```

先扫描，再列出候选和生成全量报告。以下输出目录必须尚不存在；已有结果使用 `list`、`show` 阅读，重跑时换新目录：

```bash
uv run kb-vocab review scan \
  --catalog packages/kb-vocab/catalog.json \
  --output packages/kb-vocab/output/review-new
uv run kb-vocab review list packages/kb-vocab/output/review-new --status pending --limit 20
uv run kb-vocab review show packages/kb-vocab/output/review-new RECORD_ID
uv run kb-vocab review build packages/kb-vocab/output/review-new \
  --output packages/kb-vocab/output/review-new-report
```

`show` 提供双方的名称、定义、层级和审查历史。`list`、`show` 返回当前 `revision`；修改命令须把读到的值作为 `--expected-revision`，过期值拒绝写入。将下例的 URI、记录 ID、版本值、理由、操作员和授权说明替换为实际值：

```bash
uv run kb-vocab review propose packages/kb-vocab/output/review-new \
  --subject SUBJECT_URI --object OBJECT_URI --relation relatedMatch \
  --reason '具体关系依据' --actor '操作员' --expected-revision REVISION
uv run kb-vocab review decide packages/kb-vocab/output/review-new RECORD_ID \
  --decision accepted --reason '具体采纳理由' --actor '操作员' \
  --authorization '本项决定的实际授权' --expected-revision REVISION
```

`propose` 只登记待审关系，支持 `exactMatch`、`closeMatch`、`broadMatch`、`narrowMatch`、`relatedMatch`。`decide` 支持采纳 `accepted`、暂缓 `deferred`、拒绝 `rejected`、撤回 `withdrawn`；采纳要求先明确关系及依据，通过关系冲突检查。审查记录不会直接成为 SKOS 映射，只有 `build` 输出当前有效的已采纳关系。

多项决定可放入一个 JSON 数组，每项包含 `id` 和 `decision`，例如 `[{"id":"RECORD_ID","decision":"deferred"}]`。批次共享操作员、授权和理由；整批校验通过才追加一个事件，一项失败则整批不写入：

```bash
uv run kb-vocab review decide-batch packages/kb-vocab/output/review-new \
  --decisions-file decisions.json --actor '操作员' \
  --authorization '本批决定的实际授权' --reason '本批共同理由' \
  --expected-revision REVISION
```

批次提交前可以只读预览：

```bash
uv run kb-vocab review preview packages/kb-vocab/output/review-2026-09-13 --decisions-file decisions.json
```

结果包含当前 `revision`、批次指纹、新增和移除的映射；冲突时返回 `ready: false`，不写入事件。机械检查通过不等于取得采纳授权。批次仍使用明确列出的记录和当前 revision，一项失败整批拒绝。

`review.ttl` 保存初始审查记录，`events/` 追加 Turtle 事件；`rdf:subject`、`rdf:predicate`、`rdf:object` 仅描述提议，不直接断言对应关系。`urn:kb-vocab:review:` 是本包的工作流元数据扩展，不冒称 SKOS 内置属性。来源指纹与操作员声明随事件保留；追加事件采用序号、哈希链、写锁及版本检查，检测并发和不完整写入，不提供身份认证或文件系统外的防篡改保证。

来源变更后的重新提案要求独立于审查状态保存，暂缓或拒绝不能清除它。构建使用已核哈希的来源字节，并在发布前再次核对涉及来源。校验只阻止新增的映射冲突，来源已有的诊断仍保留；不宣称完整 SKOS 推理或符合性。

新扫描可通过 `scan --previous PREVIOUS_STORE` 沿用旧决定。沿用要求双方 URI、相关来源的完整文件哈希和规则不变；来源变化使旧记录进入 `needs_review`，旧映射停止输出。当前批准的自动规则仅覆盖完整索引、候选准备和未变旧决定的沿用，第一批新跨来源关系没有自动采纳规则。操作员及授权字段是本地声明记录，不是身份认证，也不自动赋予正式项目效力。

[当前审查库](output/review-2026-09-13/)保留来源、完整概念索引、规则、审查记录及事件；[当前审查报告](output/review-2026-09-13-report/index.md)提供映射、例外及全量对账。`coverage.json` 为每个来源概念分别记录是否有审查记录、是否有已采纳映射；`exceptions.json` 列出待审、暂缓和需要重新审查的记录；`exception-groups.json` 按来源组合及原因归组，入口页显示分组数量；拒绝和撤回记录仍可通过 `list` 查询。来源原有诊断继续保留在各来源结果中。

映射数为零可以表示候选已准备但尚未采纳，不能据此判断扫描未完成或来源缺少内容。来源概念持续保留，审查完整性由来源索引和逐概念对账判断，不由已采纳映射数量代替。

## 概念身份

| 来源 | 当前身份策略 |
|---|---|
| IEEE、Cognitive Atlas | 首次分配 UUID；同源重建通过 `--identities` 复用已有 Turtle，并核对其清单与来源哈希 |
| MSC2020 | 固定本地命名空间、MSC2020 版次和原代码生成 UUIDv5；文件顺序及名称改变不改变该代码的 URI |
| ERIC | 按 XML 内容哈希与原始名称生成 UUIDv5；快照变化后必须另外核对身份衔接 |
| PhilPapers | 本地 URN 包含原分类 ID，不冒称官方概念 URI |
| UNESCO | 保留官方 URI，不分配本地替代身份 |

IEEE 同源重建示例：

```bash
uv run kb-vocab import-ieee \
  packages/kb-sources/output/ieee-thesaurus/2025-07/thesaurus.json \
  --identities packages/kb-vocab/output/ieee-2025-resolved/vocabulary.ttl \
  --output packages/kb-vocab/output/ieee-rebuilt
```

IEEE 导入键包含来源记录 ID 和名称指纹，不是官方编号。不传 `--identities` 就会分配一组新 UUID。IEEE 与 Cognitive Atlas 均拒绝对已修改的身份文件或变化的来源自动复用；不会合并用户对旧评估图的编辑。这些策略服务于来源评估，尚未统一为正式项目身份方案。

## 映射边界

IEEE 首选条目映射为概念；具有反向 UF 的单目标 USE 映射为替代标签。BT／NT 保留直接层级，RT 表达为 `related`。AND 分组及反向 UF 不猜成同义词；标签异常继续保留原文。概念页通过 `prov:wasDerivedFrom` 关联，逐条证据在账本。

[IEEE 固定规则](src/kb_vocab/policies/ieee-2025-07.json)对本次来源的 202 对间接层级重叠关系排除 404 条原始 RT，记为 `excluded_by_policy`，不再逐对待审。规则绑定 PDF 哈希与提取指纹，不自动用于新版；直接层级冲突、自关系等未覆盖情况仍按原规则处理。此举是项目投影取舍，不是修正 IEEE 原文。

Cognitive Atlas 的 `KINDOF` 按方向映射为 `broader`，`PARTOF` 使用 `dcterms:isPartOf`。实验任务是独立 RDF 资源，不放入认知概念层级。六条已核异常记录按固定来源规则排除；别名不猜分隔符，任务测量断言及其条件留在账本。[审查记录](../kb-sources/output/reviews/cognitive-anomalies/审查结果.md)保留取舍依据；显示名称和定义解码 HTML 字符实体，原串保留。

MSC 保留原 `text` 和 `description`，即使不同代码同名也不合并。ERIC 区分现行词、同义记录和停用记录，组合 USE、缺失端点及冲突关系隔离；这次隔离不自动取得 IEEE 排除规则的永久效力。PhilPapers 保留全部已列父分类，不用主要父分类替换多父关系；来源省略的根记录不补造。

## 来源结果

| 文件 | 内容 |
|---|---|
| `vocabulary.ttl` | 评估 RDF 图；UNESCO 为原生图的等价序列化 |
| `mapping-ledger.json` | 来源记录、字段去向、映射与隔离原因；原生图接入不另造逐词映射 |
| `report.json`、`validation.json` | 统计、限制、校验范围和问题 |
| `manifest.json` | 输出文件哈希；具体来源和身份输入按导入器记录 |
| `index.md` | 阅读入口 |
| `source.json` | 四个结构化来源的获取依据；IEEE、Cognitive Atlas 依据在其清单及账本 |
| `source-original.ttl` | UNESCO 输入的原始字节副本 |

先完成来源读取、映射、校验与 Turtle 往返，再发布到新目录。UNESCO 明确保留带诊断的原图，不通过删除内容迎合本包 profile。输出不覆盖既有目录，不能写入已验证来源快照内；哈希一致不等于签名认证或正式采纳。

`output/` 是需要备份的持久评估数据，`build/` 是可清理试验材料，均由 Git 忽略。领域组织及完整词表构建已实现；正式主题词表的目标是 Turtle 唯一编辑格式、JSON-LD 按需派生，正式编辑源位置、YAML 切换和 JSON-LD 导出尚未实施。

## 校验范围

节点与字段合同见[词表数据规范](../../docs/model/vocabulary/设计-词表数据规范.md)。该文覆盖当前字段并集，并单列中英文过滤、名称统一及 SHACL 的实现差距；下面描述的是目前代码实际提供的检查。

当前检查概念与体系类别互斥、文字标签、同语言首选名唯一、标签属性互斥，以及相关关系与层级路径重叠。环和自相关作为质量警告，不自动删除；不宣称完整 SKOS conformance，也不判断领域知识正确性。

`profile.*` 是工具的显式类型要求，不是 SKOS 普遍要求。旧 UNESCO 报告中的 780 项集合类型误限已在当前代码纠正；原图的七项 S13 标签冲突仍可核对。新主词表经过语言与结构转换后单独执行图校验和 SHACL，不把历史报告的 787 项诊断直接当作当前输出结果。

## 开发验证

```bash
uv run python -m unittest discover -s packages/kb-vocab/tests -v
```

行为验证覆盖身份稳定与漂移拒绝、名称及关系映射、异常隔离、离线查询、来源篡改拒绝和失败不覆盖。真实来源结果另作记录与关系对账；通过校验不代表正式迁移或发布。
