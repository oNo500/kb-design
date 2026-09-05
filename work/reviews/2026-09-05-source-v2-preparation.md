# 来源迁移准备

状态：本文件保留初次盘点。首批四份来源的完整离线处置已汇入[来源证据结论](2026-09-05-source-evidence-conclusions.md)，后续不以本文件的阶段性选择清单作为未执行待办。基线为 `7cc97b5`，工作分支为 `codex/source-v2-prep`。本文是[项目路线](../roadmap.md)下的审查材料，不是来源数据、角色批准、外部事实采纳或正式切换决定。

## 本批结论

实际内容已能指出优先对象，但首批没有可以直接写入正式 v2 的完整来源记录。当前可交付的是可复用证据、旧账本与现值的差异，以及逐项处置建议。

- 正文链接与正式字段引用不是同一集合。笔记的 17 个独立 URL 没有因此取得来源实体或用途登记身份。
- 实际字段涉及 `gbt-13745`、`diataxis`、`iptc-genre` 和 `wikidata` 四份既有来源。其旧迁移账本仍有外部状态、用途批准和逐值关系依据的阻断。
- `computing.basis.zh` 已有语言依据定位 `520`，不能继续把旧“缺定位”结论当成现值；它仍不是 `match` 的关系依据。
- `obsidian` 软件实体为后续新增对象，旧库存和账本不覆盖它。其旧形状登记已经由提交 `61d0487` 完成，不因本次梳理而撤回；v2 适用范围、映射依据和归属判断仍分别处理。
- 本次不新建来源实体或用途，不修改角色、状态、档级、内容字段和旧账本，不恢复候选、交付绑定、原子应用或回滚实现。

## 输入范围

本批 CLI 文本快照 SHA-256 为 `dc170d201c785715e0a82fd3a9ad741e518898f871e9f6409b1edd14930f9ce7`，它标识本次读取输出，不冒充磁盘原文件哈希。原始快照与 URL 位置表保留在 Git 忽略的 `build/source-v2-prep/`。

正式库为 `/Users/xiu/Documents/kb-vault/`。通过 Obsidian CLI 确认实际路径后读取 `content/f732bcb2-c30c-478a-9377-8bfe709ee76b.md`，标题为 `Obsidian`，状态为 `draft`。核查范围是该文件、其直接受控引用、这些对象的来源关系，以及仓库已有阅读记录和冻结库存。

| 内容字段 | 当前对象 | 本次追溯 |
|---|---|---|
| `kb_entities` | `obsidian` | 软件实体的 `subjects`、`basis.subjects` 与 Wikidata 映射 |
| `kb_subjects` | `computing` | 中文语言依据、`source: self` 与 GB/T 代码映射 |
| `kb_type` | `explanation` | Diátaxis 映射 |
| `kb_genre` | `analysis` | IPTC genre 映射 |
| `kb_source`、`kb_references` | 均未填写 | 不从正文链接补造派生关系或正式参考文献引用 |

CS2023 组织 computing 下位结构，但本篇只选择顶层 computing；本批不扩张为 CS2023 全部知识单元的迁移审查。四份来源的其他下游记录只记录影响范围，不逐条采纳。

离线检索覆盖本 checkout 的 `docs/`、正式词表与生成输入、六份迁移账本、tracked 冻结库存，并在主 checkout 的 `.superpowers/` 查询相关历史材料路径。没有联网、下载或读取浏览器历史；“未找到离线原文”只描述这些查找范围，不声称整台电脑没有材料。

## 引用分工

| 对象 | 本篇实例 | 处置边界 |
|---|---|---|
| 被介绍的软件 | `entities[obsidian]` | `kind: software`；不把其 ID 复用于帮助站、访谈、社区目录或插件项目 |
| 具体事实的依据 | 本地存储说明、创始人访谈 | 先识别具体材料及位置；只有拟正式采用时才审阅身份、依据和适用字段 |
| 概念映射 | `computing → gbt-13745:520` | 需要双方范围与关系证据；同名和已有语言依据不能替代 |
| 实际派生 | 当前 `computing.source: self` | 保持本地建立事实，不改成 GB/T 派生；参考过某页不等于从该页复制了记录 |
| 用途登记 | `sources[wikidata].role: [mapping]` | 现行用途不等于 v2 的逐角色 `approved`；也不批准具体 Q 条目关系 |
| 普通正文链接 | 示例 vault、作者博客、插件仓库 | 可以继续作为阅读入口，不强制为每个 URL 创建正式实体或 `discovery` 角色 |

依据为[来源治理草案](../../docs/drafts/source-governance.md#对象边界)、[现行来源登记](../../docs/design/model/sources-registry.md)与[来源校验决定](../../docs/decisions/source-validation-policy.md)。本报告不使草案生效。内容层 `source` 表示内容派生，与词表层来源结构有不同引用合同，也不能机械互换。

## 正文材料

原笔记共有 22 次外部链接引用，合并相同 URL 后为 17 个。下表只是原笔记引用的离线处置，不宣称这些页面当前可访问或本轮已核对原文。笔记末尾的“资料核对：2026-09-05”是已有作者声明，不能替代本轮独立核实，也不能自动成为正式 `checked`。

| 原笔记材料 | 实际用途 | 已有离线证据 | 本次结论与缺口 |
|---|---|---|---|
| [官方帮助](https://obsidian.md/help) | 产品介绍与生态入口 | [帮助阅读记录](../../docs/references/obsidian-help.md)说明阅读范围 | 入口不能为每项产品或插件事实提供定位；优先追到具体页面，不把整个帮助站作为万能依据 |
| [创始人访谈](https://nesslabs.com/obsidian-featured-tool) | 起源、开发动机、插件设计 | 本篇有两处引用；检索范围内未找到可独立回查的访谈原文或逐段阅读记录 | 保留引用，起源与动机尚不能在本批升级为正式逐值依据；需现有离线原文及作者、日期、位置 |
| [文件存储](https://obsidian.md/help/Files%2Band%2Bfolders/How%2BObsidian%2Bstores%2Bdata) | Markdown、文件夹、缓存与外部编辑 | 帮助记录“vault 存储”行保存全文阅读范围及缓存结论 | 可复用既有阅读记录；仍需区分具体主张对应位置与材料版本，不从历史阅读推出当前版本状态 |
| [内部链接](https://obsidian.md/help/links) | 文件、标题、块链接和格式边界 | 帮助记录“内部链接”行有相应说明，记录的 URL 使用另一条旧路径 | 可复用行为阅读记录；旧新 URL 的等同与重定向本轮未核实，不批量替换地址 |
| [反向链接](https://obsidian.md/help/plugins/backlinks) | linked mentions 与反向导航 | 帮助记录 Backlinks 行保存明确阅读小节；记录路径大小写与原笔记不同 | 语义线索可复用；地址身份与当前行为仍需具体材料支持 |
| [Bases](https://obsidian.md/help/bases) | 文件属性、视图与回写 | 帮助记录 Bases 行保存编辑、筛选、文件与 properties 边界 | 可复用阅读记录；本批不把它登记为结构复制或概念映射来源 |
| [Properties](https://obsidian.md/help/properties) | 嵌套 YAML 与编辑限制 | 帮助记录 Properties 行保存 Not supported 等小节 | 可复用字段行为记录，不把软件属性编辑限制当作本库字段准入规则 |
| [社区目录](https://community.obsidian.md/) | 社区生态入口 | 原笔记只有入口链接 | 不是 Dataview、Excalidraw 等每个项目能力的逐值依据；不以目录统一批准项目事实 |
| [CLI](https://obsidian.md/cli) | 应用运行条件与自动化 | 旧终端规格有本机观察，但引用的是 help/cli；本轮有本机只读调用 | 本机调用不能证明所有平台与冷启动条件，两个地址也未在本轮核实等同；不新建 live 观察 |
| [共享库](https://obsidian.md/help/sync/collaborate) | 实时编辑与协作者权限限制 | 原笔记有具体链接；帮助阅读记录未包含该页 | 高于普通生态入口的事实缺口；需离线原页与具体小节，不能从其他帮助页面推导 |
| [插件权限](https://obsidian.md/help/plugin-security) | 文件与网络权限 | 原笔记有具体链接；帮助阅读记录未包含该页 | 保留引用；正式采用前需要原页与范围，不把一般安全经验冒充产品事实 |
| [kepano 示例库](https://github.com/kepano/kepano-obsidian) | 模板属性与 Base 示例 | 原笔记明确示例未实测；本轮未找到可独立核对的仓库快照 | 保留为示例入口；若用于设计依据，需要具体 commit、文件和实际观察 |
| [作者用法](https://stephango.com/vault) | 个人使用方法 | 现有笔记链接，未找到对应离线原文 | 作者经验不能自动变成产品保证或本库规则；需要具体引用段落再考虑采用 |
| [Habits Map](https://blog.linkingyourthinking.com/notes/habits-map) | 专题组织示例 | 现有笔记链接，未找到对应离线页面 | 保留导航入口，不声明已验收其结构 |
| [整理示例](https://blog.linkingyourthinking.com/notes/habits-moc---collide) | 内容拆分与合并示例 | 现有笔记链接，未找到对应离线页面 | 与 Habits Map 分别保留材料身份，不因为同站或同作者合并成一份证据 |
| [Excalidraw](https://github.com/zsviczian/obsidian-excalidraw-plugin) | 图文关联实现 | 现有笔记链接，未找到项目快照 | 不把项目名当作实现依据；采用具体能力时需 commit、README 或相应实现位置 |
| [ExcaliBrain](https://github.com/zsviczian/excalibrain) | 推导关系与人工关系的区别 | 原笔记有此判断，未找到其离线规则原文 | “父子关系可能推导”需要相应规则与版本；不把图的表示直接映射为正式关系 |

当前正式实体和来源登记没有与上述帮助材料、访谈或示例一一对应的材料记录。`obsidian` 的软件身份不填补这项差异。是否把具体材料提升为正式引用取决于真实采用需求，不以本表行数作为必须登记的对象数。

## 词表依据

本节的字段值来自当前正式词表。`candidate`、`active` 是现行项目状态，不是 v2 的外部 `current`、`superseded` 或 `withdrawn`。

| 来源与使用位置 | 现值与可复用材料 | v2 尚缺条件 | 建议 |
|---|---|---|---|
| `gbt-13745`；`concepts[computing].basis.zh` 与 `match[0]` | 中文依据是 `level: 1`，`references` 已保存 `source: gbt-13745`、`locator: 520`；映射为 `exactMatch`。本地 [GB/T 清单](../../docs/references/gbt-13745.md)记录转载来源，computing 顶层与 520 的对应也保存在生成器 | 原始标准及修改单对该值的适用证据；映射相邻依据；v2 外部状态与 mapping 角色决定。语言依据的 source/locator 不能直接当作严格 basis 的 entity/locator/checked | 优先准备 520 单项证据，不重做全部 435 条映射；保留当前语言采纳，单独列映射缺口 |
| `diataxis`；`types[explanation].match[0]` | `exactMatch` 到 `explanation`；scope 为“读者为了理解为什么；讨论，多角度，承认观点”。[写作阅读记录](../../docs/references/writing-guides.md)保存 Explanation 页面和小节 | 双方概念范围与关系的相邻依据；可变页面的核对记录与具体材料身份；外部状态、角色决定。既有 `version: 2026-08` 不能单独证明发布版本 | 最适合先整理一项可复用阅读依据，但在关系和角色获准前不写正式 match.basis |
| `iptc-genre`；`genres[analysis].match[0]` | `closeMatch` 到 `http://cv.iptc.org/newscodes/genre/Analysis`；[内容模型](../../docs/design/model/content-model.md#体裁词表)保存 IPTC 定义与本地笔记含义的区别，冻结库存也记录曾读目标条目 | 可复查的原定义、条目版本及关系定位；相邻 basis；角色与外部状态决定。新闻语境到个人笔记的改写不能被 closeMatch 字符串自动证明 | 保留 closeMatch 与既有本地解释；先补清原定义到本地范围的差异说明 |
| `wikidata`；`entities[obsidian].match[0]` | 当前映射为 `Q103994532`、`exactMatch`；登记提交 `61d0487` 明确软件本体 scope | 本轮没有 Q 条目的离线描述、语句、revision 或相邻依据；旧账本不含该映射；Wikidata 外部状态与 mapping 角色未获 v2 批准 | 单列新增项；不把旧 Wikidata 映射复核结论套用到 Obsidian，也不因关系已在旧形状登记而撤销现值 |

四份来源各自实体字段也有遗留：`gbt-13745`、`diataxis`、`wikidata` 的 `basis.subjects` 仍为 `self`，不是外部依据；`iptc-genre` 使用紧凑 `iptc-genre:scope`，旧账本仍阻断严格迁移。这些归属问题和本篇内容是否选对主题是不同决定，不随 mapping 角色一起批准。新增软件实体 `obsidian.basis.subjects: self` 同样单独保持。

当前直接影响范围为：GB/T 有 435 条 topic 映射和 427 条 topic 派生来源；Diátaxis 有 4 条 type 映射；IPTC 有 5 条 genre 映射；Wikidata 有 24 条 entity 映射和 1 条 form 映射。这是字段引用库存，不表示这些关系已验证，也不表示本篇同时使用了全部条目。

## 账本差异

历史账本按原基线解释，不改其 identity、旧路径、哈希或结论。下列定位中的行号是冻结 TSV 身份，不是当前 YAML 行号。

| 原审计位置 | 历史结论 | 本批现状与去向 |
|---|---|---|
| `entities.yaml` 的 `source-entities.tsv:2/23/24/30` | 四份来源均为 `unresolved_external_status`，`blocks_cutover: true` | 本轮没有取得新外部状态材料，保留阻断；现行实体 active/candidate 不参与外部状态推导 |
| `uses.yaml` 的 `source-roles.tsv:2/3/35/36/37/44/45` | 四份来源共七个角色均为 proposed、decision=null | 本篇仅明确用到四个 mapping 关系链；不能顺带批准三个 structure 角色，也不能用这一个内容样本批准全部关系 |
| `basis.yaml` 的 `vocab/topics.yaml\|55\|concepts[computing].basis.zh` | 紧凑值 `gbt-13745`，`not_migrated_missing_locator` | 现值已有 520 语言定位；旧行保留，新准备材料记录差异，不伪称缺口全部关闭 |
| `basis.yaml` 的 computing 英文依据 | `none`，`no_external_basis` | 现为 `{legacy: none}`；不机械转第 6 级或外部依据 |
| `match.yaml` 的 `match-inventory.tsv:49/755/42` | computing、explanation、analysis 均为 `blocked_unread_material` | 冻结明细已有部分阅读结论，最新写作阅读记录也可复用；必须逐项说明实际缺口，不把这个粗分类理解成所有原文从未读过 |
| 新 `entities[obsidian]` 与其映射 | 冻结正式实体库存没有该对象 | 原正式实体集合到当前仅新增 obsidian；本批记录新增项，不替它补造旧库存身份、Q 条目证据或 accepted patch |

审计入口：[实体账本](../../data/audit/migrations/source-v1/entities.yaml)、[角色账本](../../data/audit/migrations/source-v1/uses.yaml)、[依据账本](../../data/audit/migrations/source-v1/basis.yaml)、[映射账本](../../data/audit/migrations/source-v1/match.yaml)。冻结身份与上下文保存在 [source-entities.tsv](../../tests/fixtures/governance-frozen-2026-08-31/source-entities.tsv)、[source-roles.tsv](../../tests/fixtures/governance-frozen-2026-08-31/source-roles.tsv)、[match-inventory.tsv](../../tests/fixtures/governance-frozen-2026-08-31/match-inventory.tsv)。

## 人工处置

以下是提案，不是决定采纳。外部事实不足时，人的同意也不代替事实依据。

| 顺序 | 待决定事项 | 推荐与替代 | 影响与权限 |
|---|---|---|---|
| 先行 | 是否优先给当前笔记的起源、协作限制和插件权限补足可回查的离线材料 | 推荐先提供已保存的具体页面或摘录；若暂无材料，保持正文引用及“本批未独立核实”，不新增正式来源记录 | 只整理材料可按现行授权进行；内容改写、来源身份登记和正式引用转换分别提案。本轮不提出联网请求 |
| 先行 | 是否以 Diátaxis explanation 和 GB/T 520 为首批逐值依据对象 | 推荐先做这两项，因为已有阅读记录或语言定位；替代是先处理实际产生争议的 Analysis 映射 | 只准备单项关系证据，角色、具体关系及实体字段按 L2 或对应权限另案批准；不联动整源所有下游 |
| 随后 | 帮助文档、访谈等材料是否需要独立正式实体身份 | 推荐只对准备正式引用的具体材料提案；替代是继续作为普通正文链接 | 不复用软件 obsidian 身份，不在本批发放新 ID、designation、类别或用途角色 |
| 随后 | Obsidian 与 Wikidata 条目的关系及软件 subjects 归属 | 推荐取得 Q 条目材料后把身份对应与主题归属拆成两个问题；替代是保持现行 candidate 与旧映射 | 既有 L2 登记保持；新的严格依据、归属与关系需各自证据，不覆盖旧提交 |
| 后置 | 正式来源 v2 数据、角色批准、切换及发布 | 继续执行当前阶段的冻结边界 | 完整候选、绑定、原子应用、回滚及发版不进入本批；按[当前阶段](../../docs/decisions/current-stage-scope.md)另行开放 |

## 后置缺口

现有来源探测输出尚不能当作已符合 schema 的正式运行产物。[实现](../../packages/kb-core/src/kb_core/probe_sources.py)追加 `observations.jsonl`，逐行使用 `endpoint`、单数 `signal` 和日期；[schema](../../schemas/source-probe.schema.json)要求含 `observations` 的文档、`request`、复数 `signals`、`errors` 与 date-time。`--live` 明确拒绝运行。这与[草案探测边界](../../docs/drafts/source-governance.md#探测边界)一致，本批只登记缺口，不重复验证固定夹具，也不修复探测器。

草案“持续不可访问的期限和阻断阈值尚未决定”与已采纳[来源校验决定](../../docs/decisions/source-validation-policy.md)的 Q09 控制值存在文字不同步：决定已经给出三次不同失败、至少十四天及人工不可复现等条件。此项只说明文档状态，不证明任何真实来源失效；正式激活前需同步草案表述，本批不改写决定。

## 核查证据

本批只保留与结论可信度有关的核查，不运行应用或治理回归。

| 目标失败与后果 | 独有证据 |
|---|---|
| 正文材料遗漏或普通链接被冒充正式引用 | CLI 内容快照逐行提取：22 处引用、17 个 URL；逐行读正文并核对受控字段，字段与正文集合分开 |
| 旧账本结论被套用于已变化或新增对象 | 当前 YAML 与冻结 TSV 按记录身份、字段和映射目标对照，保留原账本身份；明确 computing 语言依据迁移和新增软件对象 |
| 阅读笔记被冒充新原文核验或 v2 采纳 | 每行标明可复用记录、尚缺材料、拟议处置及权限；本批无联网、角色批准或正式写入 |
| 审查越界改变数据、实现或 vault | Git 写集仅为本报告和项目路线；正式词表、schema、账本、应用与核心实现无差异；vault 内容仍由 CLI 只读访问 |

可复核结论依赖上述基线和笔记版本。笔记、词表或决定变化后只刷新受影响项，不重跑已关闭的应用验收，不把来源准备变成另一轮空库或样本数量验收。

独立语义审查未发现 Important 或 Critical 问题；审查只核对证据性质、对象分工和批准边界，没有重复运行机械检查。正文 URL 集合与提取结果逐项一致，文档链接与 Git 差异格式检查通过。
