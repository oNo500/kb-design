# CCS 词表适配 (CCS Vocabulary Adapter)

把选定的 CCS 原件生成可供本项目使用的 SKOS／SKOS-XL 词表。原件、配置是输入，`.ttl` 是生成物；修改输入后重建，不手工改词表。

这是工程实践子包，复用 `kb-vocab-shacl` 的结构与规则，不改目标设计，也未接入旧 `kb-vocab` 发布流程。

## 来源选择

采用 [cli99/acm-ccs 的固定提交](https://github.com/cli99/acm-ccs/tree/48644c2ed653833115515c5e59bf2cb2452f1830) 中的 [SKOS XML](https://raw.githubusercontent.com/cli99/acm-ccs/48644c2ed653833115515c5e59bf2cb2452f1830/ACMComputingClassificationSystemSKOSTaxonomy.xml)。

选它的原因是：文件本身已有可解析的 SKOS，分类、名称、关系和说明可以一起保留，无需从网页或 PDF 重建。已核对的文件包含：

| 内容 | 数量 |
| --- | ---: |
| 顶层概念 | 14 |
| 概念 | 2,299 |
| 首选名称 | 2,299 |
| 别名 | 6,787 |
| 隐藏名称 | 27 |
| 直接上位关系 | 2,390 |
| 相关关系声明 | 192 |
| 范围说明 | 41 |

98 个概念有多个上位概念。第十四个分支是“人物、技术与公司”，整个分支按来源保存；这不表示它们都属于学科类别，也不自动建立项目普通实体记录。上位、下位是同一层级关系的两个方向，不能把各 2,390 条相加解释为独立关系数。

本次取得的 [ACM 官网 XML](https://dl.acm.org/pb-assets/dl_ccs/acm_ccs2012-1626988337597.xml) 没有别名、隐藏名和范围说明，因此选用这个字段更丰富的文件。这个比较只针对已经取得的两个文件，不表示官方没有其他导出，更不表示 GitHub 副本最新或全面优于官方。

[仓库 README](https://github.com/cli99/acm-ccs/blob/48644c2ed653833115515c5e59bf2cb2452f1830/README.md) 的参考链接指向解析库，没有说明 XML 最初的下载地址。上游获取链和数据许可仍未核实；不能把代码许可当作数据许可。来源选择由用户在本任务中确认。

## 处理流程

下图包含本次实际执行的一次性翻译和分流。默认 build 只做格式与结构适配，完整保留来源概念；翻译由本次脚本执行，分流由 partition 按已确认清单执行。

```text
GitHub 固定版本 XML
      │
      下载
      │
 核对哈希并缓存原件
      │
CCS 原始词表
      │
 格式与 SKOS-XL 适配
      │
 脚本提取英文首选名称及分类语境
      │
 一次性批量翻译（疑难项保留原名）
      │
 保存译文、执行者、批次及名称登记
      │
 合并中英文名称并校验
      │
      ├─ 13 个学科分支 ───────────→ 概念词表
      │
      └─ 专名分支
            │
         逐项判断
            │
         处理清单
            │
         人工确认
            │
         脚本处理（保留已有中英文名称）
            ├─ 保留概念 ─────────→ 概念词表
            ├─ 建立实体 ─────────→ 实体记录
            ├─ 两者保留 ─────────→ 概念词表＋实体记录
            └─ 尚未确定 ─────────→ 保留原样，待处理
```

“两者保留”用于同时需要主题标引和对象事实管理的情形：概念记录组织相关资料，实体记录保存官网、开发商等属性，两者分别维护身份并关联。原件始终保留；后续修改处理清单，再由脚本生成。

中文是本次模型初译，未经人工复核；分流不会重新翻译。译文与批次记录见[中文初译说明](../../output/vocabulary/ccs/translation-zh-20260919/说明.md)。最终维护概念词表和实体词表，翻译输入及原分流输入只作重建和追溯材料。

## 分流操作

当前分流结果位于 `output/vocabulary/ccs/partitioned-20260921-rdf/`：`concepts.ttl` 保存 2,053 个概念，`entities.ttl` 保存 302 条实体记录。56 项同时保留概念与实体，48 个未决条目保留原样。其他文件是输入快照、处理对应和审计记录，不作为第三份词表维护。

处理清单的编辑源是 `data/inputs/ccs/routing.json`，每项只维护来源 ID、处理方式和实体类别；来源版本与 `confirmed` 在清单级记录。判断说明在同目录 `routing-notes.json`，只是建议依据，不是已核实的实体事实。

```sh
# 阅读现有中文词表和处理建议，校验完整性并生成可读清单。
uv run kb-vocab-ccs review output/vocabulary/ccs/translation-zh-20260919/result/vocabulary.multilingual.ttl --plan data/inputs/ccs/routing.json --output build/ccs-review

# 人工确认清单、将其 confirmed 记为 true 后才可执行。
uv run kb-vocab-ccs partition output/vocabulary/ccs/translation-zh-20260919/result/vocabulary.multilingual.ttl --plan data/inputs/ccs/routing.json --output output/vocabulary/ccs/partitioned

# 对新概念图单独校验；生成成功不等于校验通过。
uv run kb-vocab-ccs check output/vocabulary/ccs/partitioned/concepts.ttl --output build/ccs-partition-check
```

省略 review 的 `--plan` 会提取一份全部为 pending 的清单，不自动判断实体性质。未确认、输入版本变化、重复或遗漏条目、未采用类别都会阻止分流。

`partition` 的两份词表输出为 `concepts.ttl` 和 `entities.ttl`；`routing.json`、`entity-audit.json`、输入快照、清单、移除陈述及哈希仅作处理和审计记录。实体标识按来源概念稳定分配；不同来源编号不自动合并为同一实体。已有中英文名称随记录保留，不重新翻译。

实体采用已有 kind 对应的 Wikidata 类 IRI 作为 `rdf:type`，用 SKOS／SKOS-XL 保存名称；这是本包的 RDF 表示绑定，不是到 Wikidata 个体的身份映射，也不把实体声明为 `skos:Concept`。名称记录保留来源 Label 的派生引用及初译提示；来源条目用 `rdfs:seeAlso` 提供回查入口。

分流确认和事实核实分别记录，不再把实体一律标成 candidate。实体的独立 RDF 输出不等于已导入现行 `entities.yaml`，也不代替事实核对及人员收录条件。`routing.json` 只说明哪个来源条目生成了哪个实体，不声明 sameAs、exactMatch 或已采纳的主题专指关系。

转为实体的条目从概念输出移除，其入边和出边一并留档，不重新挂接下级；若会改变 pending 条目的关系则停止。分组节点是否另作导航、候选实体的事实补全及正式登记分别处理，不能因本命令运行成功视为完成。

## 使用命令

在仓库根目录执行。以下每个输出目录必须尚不存在；重复运行时改用新目录，例如 `run-2`。

```sh
# 获取固定提交的原件；已有缓存会复核哈希并直接使用。
uv run kb-vocab-ccs fetch

# 只读取缓存和配置生成词表，不联网、不运行 SHACL。
uv run kb-vocab-ccs build --output output/vocabulary/ccs/run-1

# 按共享 SHACL 结构统计字段，终端和文件均显示结果。
uv run kb-vocab-ccs inventory output/vocabulary/ccs/run-1 --output build/ccs-inventory-1

# 默认依次运行 structure 和 target；终端显示汇总，文件保留明细。
uv run kb-vocab-ccs check output/vocabulary/ccs/run-1 --output build/ccs-check-1
```

`build --source /绝对路径/source.xml` 可直接使用已有原件，仍须符合配置中的哈希。`fetch --offline` 只核对本地缓存。`inventory` 和 `check` 也接受单个 TTL 文件。

`check --profile structure` 只运行字段结构检查；`--profile target` 运行目标规则，包含名称和关系冲突；`--profile standard` 只运行包内已有标准规则。默认 `all` 为 `structure` 与 `target`，不另跑已包含于 target 的 standard。

本次固定数据实测：字段结构校验约 21 秒，完整目标校验约 353 秒，两组合计约 6 分 15 秒；均为 0 条问题。耗时随环境变化，字段统计不运行这些检查。

退出码：`0` 表示命令成功，`1` 表示校验不符合，`2` 表示输入或引擎执行失败。`build` 和 `inventory` 成功不表示 SHACL 通过。校验按严格模式处理 Violation、Warning、Info，不修改严重程度以取得通过。

## 适配步骤

| 步骤 | 程序处理 | 保留依据 |
| --- | --- | --- |
| 来源锁定 | 下载指定提交，核对 SHA-256；哈希不符立即停止 | 配置和原件 |
| XML 读取 | 只展开已核对的四个内部命名空间常量，不加载外部实体 | 原 XML 与适配 XML |
| URI 适配 | 将词表 URI 的空格写为 `%20`；按固定身份基准解析相对编号 | 原值、有效 IRI 对照 |
| 来源保留 | 核对 XML 字段与 RDF 图一致，不按同名合并概念，不改变层级 | `source.ttl` |
| 本地补充 | 从配置添加词表首选名称、范围说明，已有相同陈述不重复添加 | 补充正文、语言和采纳依据 |
| XL 表示 | 按普通名称生成 Label、literalForm 和对应角色的引用，保留普通标签 | 名称身份与来源标签对应 |
| 输出核对 | 核对来源陈述全部保留，Turtle 回读后图同构 | manifest 和文件哈希 |

补充配置使用原标题 “The ACM Computing Classification System (CCS)” 作为英文首选名称；范围说明为“收录计算机领域的分类主题，以及人物、技术、公司和组织名称。”后者是用户批准的本地说明，不冒充来源原文。

默认适配结果有 2,299 个概念、9,114 条 XL 名称记录：原有名称 9,113 条，词表名称 1 条。没有补译名、定义或来源缺失的关系。所有说明保留其原来描述的对象。

## 文件职责

| 位置 | 维护内容 |
| --- | --- |
| `src/kb_vocab_ccs/config/ccs.json` | 默认来源提交、哈希、身份基准、标题、范围说明和采纳依据 |
| `storage.py` | 配置读取、来源缓存和新目录写入 |
| `adapter.py` | XML／RDF 转换、XL 适配及确定性输出 |
| `routing.py` | 清单完整性、确认门禁及概念／实体分流 |
| `validation.py` | 共享结构统计、SHACL 调用和报告 |
| `cli.py` | 命令入口 |
| `tests/` | 数据保真、身份稳定、写入保护、统计范围及失败退出行为 |

构建目录包含：

| 文件 | 用途 |
| --- | --- |
| `source.xml` | 未修改的原件 |
| `adapted.xml` | 格式适配后的 XML |
| `source.ttl` | 仅格式转换的来源图 |
| `vocabulary.ttl` | 加入本地元数据和 XL 名称的词表 |
| `config.json` | 本次配置快照，只读 |
| `adaptations.json` | URI 对照、名称对应和本地新增陈述 |
| `manifest.json` | 文件哈希、数量与已执行的机械检查 |

生成的 `.ttl` 使用 N-Triples 子集：每条语句一行，由 RDFLib 序列化后排序，是合法 Turtle。其用途是稳定交换与程序读取；不依靠自写 RDF 序列化规则。原件、配置、适配清单与词表在相同依赖环境下可重复生成相同字节；带耗时和引擎空白节点的校验报告不承诺字节一致。

构建 manifest 只记录构建阶段，不回写后续校验状态；是否通过应读取与词表哈希对应的校验报告。

校验报告目录中的 `summary.json` 和 `校验汇总.md` 供汇总阅读，`*-results.json` 保留具体对象、字段和值，`*-report.ttl`／`*.txt` 保留引擎报告，`*-shapes.ttl` 固定实际运行的规则。不同规则组可能报告同一问题，不能相加解释为独立问题数。

## 更新方式

更新来源时，修改源配置中的 `source.commit` 和 `source.sha256`，核对差异后重新获取、构建与校验。也可通过 `--config 配置路径` 使用另一份经确认的配置。新增 XML 结构会停止转换，不能静默丢弃。

`identity_base_iri` 与下载版本分开。默认沿用首次转换采用的文档基准，仅用于解析源编号，不宣称为官方永久 IRI。更新下载提交时保持此值；改它属于身份迁移，不能当成普通来源更新。

XL 标识由所指对象、名称角色、文字、语言及数据类型确定。同一名称重建或更新下载提交时标识不变；更改这些内容会产生新的名称记录。本包不自动认定新旧名称是更名关系，也不完成退出及历史登记。持续维护须按[词表维护设计](../../docs/model/vocabulary/设计-词表维护.md)处理。

标题或范围变化通过配置维护，并更新依据。需要删减分支、合并概念或改关系时，应先形成相应采纳，再实施转换规则；不能直接改生成结果或放宽 SHACL 规则。

## 校验边界

传入构建目录时，先核对 manifest 的文件哈希；统计与校验都将清单中的生成名称指定给 `LocalLabel`。仅传 TTL 时无法确认来源，不猜测本地身份。其他本地新增概念、集合、日期及说明条件未指定对象，不表示已经通过。

规则、元数据和更完整的管理要求以[数据规范](../../docs/model/vocabulary/设计-词表数据规范.md)和[规则覆盖](../kb-vocab-shacl/COVERAGE.md)为准。SHACL 通过不等于逐条语义正确、来源许可已核实、维护历史完整或正式发布。

开发验证：

```sh
uv run python -m unittest discover -s packages/kb-vocab-ccs/tests -v
```

依赖复用项目已有 RDFLib、defusedxml、pySHACL 和 `kb-vocab-shacl`；本次没有新增第三方库或升级既有库。
