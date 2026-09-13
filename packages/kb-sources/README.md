# 来源处理 (KB Sources)

`kb-sources` 下载、校验和解析来源材料，独立于 `kb-core`、`kb-topics`。原文快照保持不变，解析结果供阅读、核对和后续建模，不直接生成正式词表。

## 使用流程

```text
来源清单 → 下载快照 → 格式与哈希校验 → 结构化数据直接读取／文档按需提取
```

从仓库根目录安装依赖：

```bash
uv sync --all-packages --locked
```

下载一份清单中的全部文件：

```bash
uv run kb-sources fetch \
  --manifest packages/kb-sources/sources/cs2023.yaml \
  --output packages/kb-sources/output/sources
```

成功时输出快照路径。离线检查该快照：

```bash
uv run kb-sources verify /absolute/path/to/snapshot
```

解析快照中的一个文件，自动选择 HTML 或 PDF 解析器：

```bash
uv run kb-sources extract /absolute/path/to/snapshot \
  --file-id full-report \
  --output packages/kb-sources/output/structures/review
```

解析全部已下载材料：

```bash
uv run kb-sources extract-all \
  --sources packages/kb-sources/output/sources \
  --output packages/kb-sources/output/structures/review-all
```

原生 `tsv`、`turtle`、`xml`、`zip`、`json` 文件下载后直接读取，无需执行 `extract`。`extract-all` 对它们记录 `native_structured` 状态和原件位置，不生成重复的文档结构；摘要中的 `native` 单列数量。ZIP 保持原始压缩包，按来源说明读取其中 XML。

输出目录必须是新目录，且不能位于任何原文快照内。同一来源有多个快照时，批量命令拒绝自动选择，改用一个或多个 `--snapshot /absolute/path/to/snapshot` 明确指定，替代 `--sources`。`extract-html` 保留为仅接受 HTML 的兼容入口，输出已升级到结构 schema_version 2。

所有命令也可通过 `python -m kb_sources` 调用；包可以独立安装，不依赖旧仓库代码。

## 认知来源

Cognitive Atlas 的列表接口仅提供基本信息。以下命令下载概念、任务列表，再按原始 ID 获取每条详情，保留定义、引用、关系类型和方向：

```bash
uv run kb-sources fetch-cognitive-atlas \
  --manifest packages/kb-sources/sources/cognitive-atlas.yaml \
  --output packages/kb-sources/output/cognitive-atlas/2026-09-13
```

每批最多 50 条，默认四路下载，可用 `--workers 1` 降低并发。目录中的 `manifests/` 保存详情清单，`snapshots/` 保存标准下载快照，`report.json` 在全部详情通过身份与结构检查后生成。快照可用 `verify` 离线校验。

相同输出目录用于续传，复用经哈希核对的列表与完整批次；中断批次重新下载。更新来源时使用新的输出目录，不在旧目录刷新远端列表。运行期间不要由其他进程写入同一目录。

范围为列表中的全部概念和任务及其详情，不另行穷举疾病、理论等对象；API 跨请求不保证同一时刻的一致快照。原生 JSON 不经过 PDF 解析。`export-cognitive-atlas <bundle> --output <new-directory>` 在逐快照校验及目录覆盖检查后输出 `source.json` 和哈希记录，供 `kb-vocab import-cognitive-atlas` 转换；不直接取得正式词表效力。

## 解析结果

每个原文件对应一个目录：

| 文件 | 内容 |
|---|---|
| `structure.json` | 标题、段落、列表、表格、链接及原文定位；PDF 还保留逐页文本、带坐标的行和已有书签 |
| `outline.md` | 标题目录，链接到原文件 |
| `reading.md` | 按提取顺序排列的正文；表格以 HTML 保留合并单元格 |
| `record.json` | 来源快照身份、原文哈希、解析库版本、实现哈希和输出文件哈希 |

批量目录按 `<source-id>/<snapshot-id>/<file-id>/` 保存各文件结果，并提供 `index.md` 和 `report.json`。报告逐文件记录状态、数量和限制；`parsed_with_warnings` 表示已提取但有明确限制，不表示内容已核准。

批量命令先校验输入快照。某个文件解析失败时，其他文件继续处理，失败文件不发布半成品，最终报告保留错误并以退出码 1 结束。全部文件解析成功时退出码为 0；仍需阅读警告和核对内容。

结构输出由 [structure.json](src/kb_sources/schemas/structure.json) 校验，并检查内部引用和顺序。哈希只能核对相对于记录的字节一致性，不能证明语义准确性或发布者身份。

## 解析方法

HTML 使用 Beautiful Soup。保留原始标题层级、链接和原文行列；识别原生列表、Word 列表样式和表格合并单元格。Word 内部列表 ID 变化不直接切断层级；少量手写编号仅在紧邻 Word 子列表时作为上级项处理。国家科学院网页限定到书籍正文区域，SEP 限定到内容区域。

PDF 使用 pdfplumber／pdfminer.six，读取文本层、字体、坐标和表格线。MSC2020 首页按两个独立目录栏处理；认知科学手册目录按印刷分部和章节编号组织，其他标题和列表层级依据排版推定。CS2023 的带代码知识单元标题和 tekom 的文字分组采用来源样式规则；tekom 的微小项目符号另存为页内标记，避免夹进条目正文。每条标题的 `method` 说明依据；原始逐页文本和行坐标始终保留。

以下内容仍需人工核对：

- Word 原文中缺少明确上级的列表，保留原始层级及空父引用，按列表报告；表格单元格内的段落、列表和嵌套表格另存于 `content`，其引用在单元格内容范围内解析。
- PDF 的标题及列表层级属于排版推定；无框表格、跨页表格和跨页段落保留为带坐标的内容，不自动合并。检测网格存在文字空洞时不按表格外框删除文字，而是保留为位置文本并报告。
- 认知科学扫描目录的既有文本层带有识别错误，例如页码和个别字符；保留原样并提示核对，不自动纠正。
- 不执行 OCR、不提取图片、不重建公式排版。无文本层的整份 PDF 会失败；个别空白或无文本页会明确记录。

## 工具试验

本批使用实际材料比较了以下本地转换路径，没有调用云端解析服务。

| 工具 | 样本中的问题 |
|---|---|
| Docling 2.126.0 | CS2023 Word 列表被摊平，部分单词出现空格；MSC2020 双栏目录误作表格并合并条目 |
| Unstructured 0.27.5 | CS2023 列表文字保留，但多级条目的父引用指向同一个标题 |
| MinerU 3.4.5，pipeline／txt | MSC2020 双栏顺序改善，但部分连字丢失，合并文本的位置框不完整 |
| Marker 2.0.0，fast | MSC2020 首页分类编号丢失，目录条目合成段落 |

这些是指定版本和配置在本批样本上的结果，不是工具的通用排名。依照本次授权，采用上面的回退解析方法。试验原生输出、版本和问题记录保存在包内 `output/docling-trial/`、`output/alternative-trials/`；未将这些大型转换工具加入正式依赖。

## IEEE 词表

完整 IEEE Thesaurus 的词条提取使用专用入口，读取原文明确的 BT／NT／RT／USE／UF，不从目录缩进推断词汇关系。当前只支持已核对版式的 July 2025 Version 1.04 PDF。

```bash
uv run kb-sources extract-ieee \
  --acquisition packages/kb-sources/output/manual/ieee-thesaurus-2025-07/acquisition.json \
  --output packages/kb-sources/output/ieee-thesaurus/new-run
```

可选加入已保存的第三方对照文件，两个参数须一起提供：

```bash
uv run kb-sources extract-ieee \
  --acquisition packages/kb-sources/output/manual/ieee-thesaurus-2025-07/acquisition.json \
  --reference-csv packages/kb-sources/output/ieee-thesaurus/2025-07/reference-inputs/ieee-thesaurus-2023.csv \
  --reference-taxonomy packages/kb-sources/output/ieee-thesaurus/2025-07/reference-inputs/ieee-taxonomy-2025.txt \
  --output packages/kb-sources/output/ieee-thesaurus/new-run-with-reference
```

`thesaurus.json` 保存首选与非首选词条、原始关系、逐行文本及页码／栏位／坐标；`relations.csv` 提供方便读取的关系清单。`terms.md` 是词条索引，`samples.md` 展示 AI 等代表词条。输出 schema 见 [ieee-thesaurus.json](src/kb_sources/schemas/ieee-thesaurus.json)。词条 ID 仅标识本次来源记录，不是正式概念身份。

提取跨页、跨栏延续词条。换行文字以空格连接；行尾已有连字符时连接下一行而不额外插空格，原始分行保留在 `fragments`。原文 USE 中的 `AND` 写法保留为同一 `source_group` 及 `connector_after`，`raw_target` 保留连接符，暂不解释为多个独立同义关系或组合等价。

`diagnostics.json` 列出未解析目标、缺少反向对应、形式异常等；不自动补关系、改拼写或合并名称。未归属的正文行保留在 `unassigned`，出现此情况退出码为 2；输入损坏或执行失败退出码为 1。退出码 0 只表示提取完成，仍需查看诊断，不代表正式数据已批准。正文行分配核对也不能代替逐词语义审查。

`references.json` 和 `comparison.json` 分开保存第三方 2023 Thesaurus CSV、2025 Taxonomy 层级文本及对照结果；来源文件复制到 `reference-inputs/`，记录哈希。层级文本按每次出现保留直接父节点，不把全部祖先写成直接上位。对照只区分精确匹配、仅空白差异和未匹配，不改变大小写，不把跨版本差异回填新版。

这次复用了[研究者仓库](https://github.com/angelosalatino/ieee-taxonomy-thesaurus-rdf/tree/43089caa37b2bd62912d6fa2cda9004cf944a29d)的现成对照数据。没有执行其 Notebook，没有沿用有争议的 RDF 标签映射，也没有进行 RDF 导出。所有结果仍是来源评估数据，CS2023 继续用于知识覆盖核对。

## 来源清单

领域、主输入与覆盖依据见[项目简报](项目简报.md)。本轮改用三份官方结构化来源，原有 PDF 和指南保留：

| 用途 | 主输入清单 | 文件格式 |
|---|---|---|
| 数学分类 | [MSC2020](sources/msc2020.yaml) | 官方文件名为 CSV，实际 TSV，cp1252，三列 code/text/description |
| 教育、学习、阅读与写作主题 | [ERIC Thesaurus](sources/eric-thesaurus.yaml) | 官方 ZIP 内的完整 XML |

实际文件、版本、哈希和读取核对见[结构化来源](output/reviews/source-switch/index.md)。同一来源的旧快照不会删除；例如 MSC2020 已有旧 PDF 与新表格快照，批量处理时使用 `--snapshot` 明确选择，不能按目录顺序自动挑选版本。

IEEE 完整词表及 CS2023 的分工保持：[2025 年 IEEE 清单](sources/ieee-thesaurus-2025-07.yaml)对应已通过浏览器保存的 673 页原文，[2023 年旧版](sources/ieee-thesaurus-2023.yaml)仅供对照；[CS2023](sources/cs2023.yaml)用于知识覆盖。IEEE 官方最新版本仍未确认。

IFLA、CWPA、tekom、How People Learn、认知科学手册和 SEP 的原清单保留为覆盖或阅读依据，不再要求所有文档都充当词表的机器主输入。新增结构化材料不新增顶层领域，也不改变正式数据的准入。

每份清单指定来源 ID、标题、期望版本及文件 ID、URL、文件名和格式。格式支持 `pdf`、`html`、`tsv`、`turtle`、`xml`、`zip`、`json`，可选 `sha256` 固定字节；见 [source.json](src/kb_sources/schemas/source.json)。一份清单是一组有明确范围的材料，不等于完整领域词表。

`version` 保存为 `requested_version`，不自动证明正文版本。URL 不接受凭据或片段；文件名不能含目录路径或与保留名冲突。Turtle 用 RDFLib 校验语法，TSV 用标准库检查行列，XML 拒绝 DTD／实体声明和 HTML 访问页；ZIP 流式检查 CRC，限制 10,000 个成员和总解压量 256 MiB，不自动解包落盘。这些检查不证明词表语义完整。

本包复用 workspace 已有并完成依赖评估的 RDFLib，不引入新的 RDF 解析实现。PDF／HTML 的既有接收检查保持原范围。

## 下载记录

```text
packages/kb-sources/
  sources/                 可执行下载清单
  output/
    sources/               不可变原文快照
      <source-id>/
        <receipt-sha256>/
          source.yaml      清单原件
          receipt.json     下载时间、地址、大小、哈希和工具版本
          ...              原始文件
    structures/            解析结果及阅读预览
    models/                本地工具试验的模型缓存
  build/                   可清理的试验环境、日志与临时结果
```

`output/`、`build/` 均由包内 `.gitignore` 忽略。需要另外备份无法重新取得的材料；Git 中的清单和代码不能替代原件。

下载器在临时目录接收文件，全部成功后才发布快照。目录名是 `receipt.json` 的 SHA-256；快照包含本次清单字节、下载记录及原文件。每次下载产生新时间记录，即使远端内容相同，也会建立新快照；尚无内容去重或断点续传。

重定向不能离开原主机名，不能从 HTTPS 降级。常规错误或可处理的中断清理临时文件；进程被强制终止时可能留下 `.receiving-*` 目录，不视为发布成功。

| 参数 | 默认值 | 作用 |
|---|---|---|
| `--timeout` | 30 秒 | 每次网络读取的超时，不是整次下载的截止时间 |
| `--max-bytes` | 67108864 | 每个文件最多 64 MiB |
| `--retries` | 1 | 瞬时网络错误等的额外重试次数，允许 0–3 |

`verify` 离线检查记录身份、清单哈希、精确文件集合、大小、内容哈希、基本格式及符号链接。下载记录 schema 见 [receipt.json](src/kb_sources/schemas/receipt.json)。它只校验 PDF 文件头／结束标记及 HTML 基本特征；可完整解析与否由后续解析步骤判断。

HTML 附属图片、样式不自动下载；正文下载不等于完整网页离线归档。下载检查也不能识别所有伪装成正文的登录页。必须固定具体快照身份，并结合内容核对使用。

## 手动材料

当前公开目录、导言和摘要可用于初步结构研究；后续需要相应正文时，由用户通过账号或机构权限取得。尚未实现手动文件导入。

| 材料 | 需要的版本与范围 | 入口 |
|---|---|---|
| The Cambridge Handbook of the Learning Sciences | 第 3 版，2022；全书或完整章节集合 | [出版社](https://www.cambridge.org/core/books/cambridge-handbook-of-the-learning-sciences/7C81E0DD3BB25810E14CFBD4DD92A89E/listing) |
| How People Learn II | 2018；完整 PDF 或余下正文 | [National Academies](https://www.nationalacademies.org/projects/DBASSE-BBCSS-13-06/publication/24783) |
| The Cambridge Handbook of Cognitive Science | 2012；目录与导言之外的正文 | [出版社](https://www.cambridge.org/core/books/cambridge-handbook-of-cognitive-science/F9996E61AF5E8C0B096EBFED57596B42) |

2023 年计算认知科学手册是另一部书，不替代上述 2012 年手册。SEP 会员 PDF 为可选形式，公开固定版 HTML 不以购买会员为前提。

## 开发验证

```bash
uv run python -m unittest discover -s packages/kb-sources/tests -v
```

行为测试覆盖下载失败与旧快照保护、解析失败不发布半成品、批量失败报告、原文改动拒绝、同环境重复输出、列表父子关系、分栏顺序、表格单元格及定位信息。真实材料另作原文抽查；测试通过不能替代内容验收。

解析不改变来源取得范围。IEEE 对照仅覆盖指定材料；OCR、正式分类构建和项目词表生成均未包含在本包中。

## 来源退出

UNESCO 已退出当前来源，下载清单与当前离线文件已移除。现有五份来源仍全量保留；历史构建只用于回溯，不作为下载或导入入口。
