# 写作词表处理 (Writing Vocabulary)

收集写作资料，把带出处的概念输入生成 SKOS／SKOS-XL Turtle 词表。收集不自动建立概念，原文建议不自动成为定义或项目规则。

下载、原件校验与文档提取复用 `kb-sources`；字段统计和规则复用 `kb-vocab-shacl`。本包只处理写作专题输入与表示，不依赖 CCS，也不接入正式知识库或发布流程。

## 数据流程

指定来源 → 原文快照及阅读材料 → 人工整理概念输入 → 审阅样稿 → 确认具体输入 → 生成词表 → 字段统计与校验。

最终词表为 `vocabulary.ttl`。输入 JSON 是编辑材料，来源、依据与 manifest 是追溯记录，不是另建一份正式词表。

## 当前产物

本次在原 99 个概念上新增 213 个，为 11 个既有概念追加说明或依据，保留原 ID、名称和旧说明。当前共 312 个概念、596 个名称、311 条定义、88 条写作建议和 10 个浏览分组。各组允许重叠，成员数量不能相加作为概念总数。

| 浏览分组 | 成员数 |
| --- | ---: |
| 文档类型 | 4 |
| 内容与目的 | 37 |
| 文章组织 | 71 |
| 语言表达 | 47 |
| 风格与语气 | 12 |
| 版式与呈现 | 66 |
| 质量与修改 | 25 |
| 交际与语义 | 19 |
| 文本标记与语义 | 43 |
| 阅读与认知 | 16 |

文档类型组采用 Diátaxis 的四种形式；其余分组供浏览，不代表来源共同规定了一套分类体系，也不生成概念上下位关系。

从仓库根目录查看：

- 词表：`output/vocabulary/writing/expanded-20260922-final/vocabulary.ttl`。
- 阅读版：同目录 `审阅清单.md`，逐项列出名称、定义、建议、关系和来源。
- 编辑输入：`data/inputs/writing/vocabulary.json`；缺口清单：同目录 `coverage.json`。
- 来源锁定：`output/vocabulary/writing/extension-sources-20260922/sources.json`。
- 检查报告：`build/reports/writing-expanded-check-20260922/检查摘要.md`；完整缺失统计和未决说明：同目录 `字段统计.md`、`补充摘要.md`。

当前 284 个概念有中文首选名，28 个暂时仅有英文。Cornell Note-Taking System 有范围说明，缺少经本次材料支持的定义；其他证据不足的候选和来源差异在 `coverage.json` 保留。英文名称不复制成中文标签，不为了检查通过而补写。

本次输入记录了补充与生成授权；不代表逐项人工语义审阅或正式发布。原完整版本保留在 `output/vocabulary/writing/full-20260922-final/`，四概念小样保留在 `data/inputs/writing/sample.json`。

## 来源范围

有效来源锁保存 82 份原文绑定，词表实际引用其中 81 份。原有 Diátaxis、Google、Microsoft、W3C 中文排版、Purdue、UNC、ERIC 等资料继续保留；新增以下来源：

- CommonMark、GFM、WHATWG HTML、CSS、Unicode 与 GitHub 文档：标记含义、视觉形式及具体实现的支持范围。
- BYU 修辞资料、OpenStax、RST、Manchester 与 GMU 写作资料：修辞、展开方法、文本关系、限定表达和信息衔接。
- WCAG、W3C COGA、Wilson 与 Sperber、NSW 教育资料及软件视频教学研究：可访问性、交际理解与认知机制。
- Adobe 字体设计资料、Vega-Lite 图例说明：限定排印和数据可视化语境的可辨识性、可读性与图例。

简明语言原则依据 IPLF 的公开介绍，未宣称读过 ISO 标准全文。来源包含标准组织材料、机构指南和作者方法，各自的适用范围随概念说明保存，不能一律称为标准要求。

采集异常保留在来源目录的 `acquisition-report.json`：原 Google self-editing 页面返回 404；本轮修辞页面按官网实际链接恢复；RST 原件可用，但通用正文提取失败，依据直接定位原始 HTML。Sweller 论文的响应实际是验证页面，已排除有效来源锁，未用作概念依据。替代资料的教学或软件视频研究范围分别说明。

## 使用命令

在仓库根目录运行。输出目录必须尚不存在；以下使用 `run-1`，重跑请换新目录。

```sh
# 保存原件、哈希、版本与阅读材料；生成 sources.json 锁定清单。
uv run kb-vocab-writing collect --manifest data/inputs/writing/sources.yaml --output output/vocabulary/writing/run-1-sources

# 从完整输入和固定来源生成词表。
uv run kb-vocab-writing build data/inputs/writing/vocabulary.json --sources output/vocabulary/writing/extension-sources-20260922/sources.json --output output/vocabulary/writing/run-1

# 只统计字段是否填写。
uv run kb-vocab-writing inventory output/vocabulary/writing/run-1 --output build/writing-inventory-1

# 统计字段，并运行 structure、target 两组已有规则。
uv run kb-vocab-writing check output/vocabulary/writing/run-1 --output build/writing-check-1
```

上面的收集命令使用原三页面清单演示采集，不会替换完整输入绑定的快照。完整批次的逐源清单位于 `data/inputs/writing/sources/`；重新下载得到的是新快照，须重新核对正文与来源锁定值。HTTP 成功和哈希通过不证明响应是所需正文。

`collect --snapshot 已有快照 --output 新目录` 可离线复用经核对的 `kb-sources` 快照。首次收集支持其既有格式；首版概念依据定位只支持 HTML 的 CSS 选择器与引文匹配，其他格式不冒充已定位。

换一份采集结果后，须核对 `sources.json` 及内容变化，并更新输入绑定的 `source_lock_sha256`，不能直接覆盖旧快照或继续沿用旧确认。收集失败会留下 `incomplete.json` 和已取得的原件，不生成完整来源锁定清单。

## 输入维护

输入格式见包内 `schemas/input.json`，JSON Schema 只约束输入结构；RDF 字段语义继续由共享 SHACL 检查。

`vocabulary.json` 是完整编辑输入；`sections/` 保存分组整理材料，生成器不自动合并这些文件。修改输入后重建 TTL，不直接编辑生成物。

| 输入 | 内容与要求 |
| --- | --- |
| `scheme` | 词表身份、名称、范围及明确选择的顶层概念；不按无上位自动指定顶层 |
| `concepts` | 稳定概念 ID、带身份的名称及依据 |
| `statements` | 分开保存 definition、scope、guidance、example、editorial；每条有稳定身份 |
| `broader`、`related` | 目标概念 ID 与关系依据；不从网页标题层级或同文推断 |
| `collections` | 浏览分组、范围和成员；成员关系不生成概念上下位 |
| `evidence` | 来源键、唯一命中的 CSS 位置及原文片段；位置和片段均核对 |
| `basis` | 名称或说明来自原文、模型还是用户；记录执行者、时间及模型版本可用性 |
| `approved`、`approval` | 是否确认，以及确认人、依据和具体输入摘要；不等于正式发布 |

名称 ID 由输入维护，修改文字不会自动换 ID。相同文字不同 ID 不合并；同一名称 ID 对应矛盾文字时拒绝生成。输入内重复 ID、悬空引用、源文件变动、错误定位及已有输出目录都会阻止生成。

guidance 写入 `skos:note`，definition 写入 `skos:definition`；说明正文使用独立资源的 `rdf:value`，携带来源及适用条件。普通名称和 XL 表达一起生成。依据明细在 `evidence.json`，不以词表级的一个来源链接代替逐项定位。

原文已有中文与模型译写分别记录。模型名称注明外部用法未核实，说明注明翻译或归纳；无法取得精确模型版本时保存 null，不猜填版本。执行记录保留在输入快照，并写入对应名称或说明的 `skos:editorialNote`。

## 确认与生成

普通 `build` 拒绝未确认输入；`--preview` 明确生成待审样稿。确认后，记录 `approval.by`、`approval.reference`，把样稿 manifest 中的 `approval_payload_sha256` 填入 `approval.content_sha256`，再将 `approved` 设为 true 并运行不带 `--preview` 的 build。确认记录须说明授权范围，批量生成授权不改写为逐项语义审阅。

修改概念、文字、关系、分组或来源锁定值后，旧确认摘要不再匹配；应恢复待审状态或重新确认。摘要只是防止误用旧确认，不认证人的身份，也不替代项目的具体采纳记录。

同样输入、固定来源及相同依赖环境可重复生成相同 RDF 字节。输出使用 RDFLib 的 N-Triples 序列化再排序，是合法 Turtle 子集。源锁定文件按原字节存档；其中相对路径以 manifest 的 `source_lock_location` 为解析基准。

## 检查范围

报告同时显示：字段填写情况、每组规则的错误／警告／提示、未覆盖主体、结构未列出的属性、输入是否确认，以及未执行的检查。声明为已生成的概念、名称、集合和说明分别指定给现有 LocalConcept、LocalLabel、LocalCollection、LocalNote；不以 URI 前缀猜测对象来历。

缺少可选字段只计入缺失，不自动判错。结构通过不证明定义、译名、关系或建议准确，来源片段存在也不证明它足以支持采纳。语言登记有效性、本地日期条件和语义审阅尚未执行，报告明确列出。

`inventory` 不运行 SHACL。`check` 按严格模式检查，不忽略 Warning／Info；未覆盖主体或结构未列出的属性会阻止总体通过。输出的 JSON 报告保留规则快照及哈希，避免把未检查误写成通过。

退出码：0 为命令成功，1 为校验未通过，2 为输入、来源或执行失败。样稿机械检查成功仍保持未确认状态。

## 开发验证

```sh
uv run python -m unittest discover -s packages/kb-vocab-writing/tests -v
```

测试覆盖来源漂移、错误定位、未确认及过期确认、稳定身份、重复生成、缺失引用，以及真实 SHACL 对首选名称冲突的检出。未新增第三方库，依赖沿用 workspace 的现有版本。
