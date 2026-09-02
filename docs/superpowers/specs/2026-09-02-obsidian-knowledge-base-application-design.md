# Obsidian 知识库应用设计

状态：已批准总体架构与内容流程，等待用户审阅完整规格。本文是 Superpowers 规格，不属于项目现行设计；项目规则仍以 `concepts/`、`design/`、已采纳决定和正式数据为准。

## 问题边界

现行 Obsidian target 只把六份正式词表生成成单向参考区。它正确保存稳定身份、字段、正式关系、项目 manifest 和效力边界，但没有把 `kb-design` 落实成实际知识库应用：使用者不能按现行内容模型创建内容单元，外部资料和临时记录没有位置，正式主题不能承接实际内容，结构盲区与使用盲区也没有进入维护闭环。

Obsidian 在本项目中的职责不是词表预览。它是 `kb-design` 的首个落地应用层：使用者在其中捕获材料、保存外部资料、创建内容单元、完成标引、浏览知识结构、形成自己的索引、发现盲区并提出维护问题。`kb-design` 继续保有概念、正式词表、内容模型、治理和维护规则的编辑权。

本规格重新定义完整 Obsidian 应用，并把现有词表导出降为其中的“受管理表示”子系统。现行导出实现不因本规格自动失效；实施时按本规格整篇重写 target，再决定代码保留、拆分或重写，不在旧文档上追加补丁。

## 已定范围

用户已经批准以下范围。

- 当前仍处于调研和设计阶段，没有现成 vault 或待迁移内容。
- Obsidian 是未来主要的内容创建、写作、浏览和使用界面。
- 一个 vault 同时保存临时记录、外部资料、本人形成的知识内容和 `kb-design` 的受管理表示。
- vault 不承担任务管理和日程管理；日历、项目执行和待办系统不进入本规格。
- 文件夹只区分稳定职责，不复制主题词表的知识分类树。
- `Content/` 中的内容文件默认接近扁平；知识的多层、多上位和多语境关系由 properties、Wikilink、人工索引和派生视图表达。
- 捕获可以宽松；一旦进入 `Content/`，内容单元必须满足现行内容模型的必填字段和引用约束。
- 外部资料与本人知识分开；资料不得因导入、摘录或语言模型处理而冒充本人形成的内容。
- Obsidian 中发现的问题只形成复核线索，不能自动修改正式词表、关系、状态、术语或决定。

## 调研结论

本设计只把公开作者和公开 vault 当作使用模式证据，不把个人偏好当成项目规范来源。

| 样本 | 观察 | 本项目取舍 |
|---|---|---|
| [Steph Ango](https://stephango.com/vault) 与 [Kepano Vault](https://github.com/kepano/kepano-obsidian) | 少量职责目录、可组合模板、跨类别 properties、Category 页面、Bases、大量内部链接 | 采用职责目录、类型一致的 properties、对象入口与 Base 组合；不采用标题身份、个人评分或 Base 写回正式数据 |
| [Nick Milo](https://blog.linkingyourthinking.com/notes/mocs-overview) | 人工索引随理解演化，同一内容可以进入多个语境 | 人工索引用于解释和阅读路径，不替代正式主题树，也不产生正式关系 |
| [Nicole van der Hoeven](https://notes.nicolevanderhoeven.com/system/cards/How%2BI%2Bstructure%2Bmy%2BObsidian%2Bvault%2B%28Obsidian%2BTour%2B2023%29) | 少用文件夹，以链接、结构笔记、metadata、查询和 Bookmarks 导航 | 主题归属不放进目录；保留多入口导航，但不把 Dataview 设为基线依赖 |
| [Eleanor Konik](https://www.eleanorkonik.com/p/yet-another-hot-take-on-folders-versus-tags) 与 [Jason Heppler](https://jasonheppler.org/2024/07/15/how-i-use-obsidian/) | 文件夹适合跨工具的稳定位置，索引和查询承担多语境关系 | 文件夹表示权属、来源和文件职责，不表示主题、实体、状态或文档类型 |
| [Obsidian Help Vault](https://github.com/obsidianmd/obsidian-help) | 单一来源、稳定发布身份、人工入口、脚本校验和派生发布分开 | 正式 YAML、Obsidian 表示和派生视图分层；机械校验不代替语义复核 |
| [Obsidian Hub](https://github.com/community-archive/obsidian-hub) | 入口页、领域索引、模板、待处理入口和贡献规则并存 | 采用查重、模板和显式入口；不采用数字目录或自由 tag 生命周期 |
| [Swyx’s Second Brain](https://github.com/swyxio/brain) | 低摩擦原始笔记、归档和纯 Markdown 可以长期运行 | 允许未整理材料，但未整理材料不取得内容单元身份 |
| [The Public Mind](https://github.com/Stefanuk12/ThePublicMind) | metadata 与动态查询能生成强导航，但会形成插件运行依赖 | 动态查询只可作为增强，不能成为唯一入口、正式数据或发布合同 |

这些样本没有给出一种通用目录树。它们共同支持一种职责分层：文件夹提供稳定位置，properties 保存可查询事实，链接表达关系，人工索引承载解释，自动视图提供筛选，原始文件保证退出能力。

## 设计目标

完整应用必须让下列工作成立。

1. 低摩擦捕获想法、链接、摘录和文件，不要求捕获时完成正式判断。
2. 外部材料保留来源地址、标题、作者、发布日期、捕获时间和原始上下文，不与本人知识混淆。
3. 使用者按现行内容模型创建、修改、废弃和引用内容单元。
4. 内容单元通过稳定引用使用正式主题、实体、类型、体裁和载体。
5. 使用者既能按正式主题结构浏览，也能建立不改变正式结构的个人索引和阅读路径。
6. 应用能显示结构盲区、内容覆盖、无效引用、过度集中和未解析线索。
7. 维护问题带位置和上下文交给人工，再按项目决策权修改 `kb-design`。
8. 受管理表示、用户内容和派生报告有明确权属，更新不覆盖用户内容。
9. 基线依赖普通 Markdown、Obsidian 核心能力和官方 Web Clipper；社区插件只可增强。

## 排除范围

本规格不设计或宣称下列能力。

- 任务、日程、习惯、项目执行或团队协作管理；
- 现有 vault 导入、合并和内容迁移；
- 自动从正文、tag、alias、文件名、反向链接或语言模型输出建立正式概念、关系、状态或 designation；
- Obsidian 文件向正式词表或项目设计的直接回写；
- 搜索查询日志的自动捕获；Obsidian 核心 Search 没有提供本项目可审计的查询事件接口；
- Dataview、Templater、QuickAdd、Buttons 或其他社区插件的硬依赖；
- TBX、正式术语激活、正式来源 v2 切换、外部标准符合性、独立复建或 durability 主张；
- 首轮实施对非空 vault 的自动更新；更新能力须另过写入和回滚门禁。

## 权属分层

一个 vault 包含三种权属和一类配置。

| 层 | 内容 | 修改者 | 项目效力 |
|---|---|---|---|
| 用户内容 | `Home.md`、`Inbox/`、`Sources/`、`Content/`、`Indexes/`、`Attachments/` | 使用者和经授权的内容工具 | 只对实际知识库内容有效，不直接修改 `kb-design` |
| 受管理表示 | `KB/`、`App/Templates/`、`App/Views/`、`App/Rules/`、`App/manifest.json` | `kb-design` 生成器 | 是正式设计与数据的应用表示，但不是编辑源 |
| 派生结果 | `App/Reports/` | 内容校验器和报告生成器 | 只作诊断与复核线索，可以删除和重建 |
| 应用配置 | `.obsidian/` | 最低基线由初始化器给出，其余由使用者维护 | 不修改模型和正式数据 |

受管理表示可以在 Obsidian 中被编辑，但编辑不取得项目效力，并会造成 manifest 漂移。首轮实现只初始化新的空 vault，不实现对既有受管理表示的覆盖更新，因此不需要在当前阶段补完整 handoff、payload、原子应用和补偿回滚。

## 文件布局

初始 vault 使用下列固定职责。

```text
Home.md
Inbox/
Sources/
  Clippings/
  References/
  Files/
Content/
Indexes/
Attachments/
KB/
  Topics/
  Arrays/
  Entities/
  Sources/
  Types/
  Genres/
  Forms/
App/
  Templates/
  Views/
  Reports/
  Rules/
  manifest.json
.obsidian/
```

`Home.md` 在初始化时给出起始内容，初始化后归使用者所有，不再由更新器覆盖。它链接到 Inbox、最近内容、常用人工索引、受管理对象入口和维护报告。

`Content/` 不按主题、实体、类型、体裁、状态或知识层级建立子目录。内容文件路径固定为 `Content/<identifier>.md`。未来只有出现实际文件系统或 Obsidian 性能问题，并有测量证据时，才可按稳定 ID 前缀机械分片；分片不得表达语义，也不得改变 identifier。

`Sources/` 保存实际外部材料。它与 `KB/Sources/` 的正式来源用途表示完全不同。目录和页面必须在入口说明中明确这种差异。

`Indexes/` 保存使用者人工选择、排列和解释的链接。索引可以覆盖多个主题，也可以对同一内容形成多个入口；它不取得 `broader`、`related`、数组、分面或概念组效力。

`App/Views/` 保存项目提供的 Base 和固定查询入口；`App/Reports/` 保存实际读取内容后生成的诊断。二者都不能成为正式数据编辑源。

## 对象边界

### 临时文件

`Inbox/` 中的文件尚未进入应用无关内容模型。它们可以没有稳定 ID、标题、主题、类型或体裁，不参与内容引用统计，也不影响词表状态。

临时文件可以被丢弃、合并、移入外部资料或经判断建立为内容单元。只有用户明确执行建立动作后，工具才分配稳定内容 ID 并要求内容模型必填值。Inbox 中出现的字符串、Wikilink、tag 和语言模型输出只作上下文，不形成项目对象。

### 外部资料

`Sources/Clippings/` 保存 Web Clipper 或人工复制的网页材料；`Sources/References/` 保存使用者对书籍、论文、标准、网页和其他资料的阅读说明；`Sources/Files/` 保存 PDF 等原始文件。

这些文件不是内容单元，也不是正式来源用途或正式实体。Web Clipper 可以把官方 preset variables `title`、`author`、`published`、`date`、`url`、`content` 等写入输出；这些值只是捕获事实，不构成 designation、概念对应、来源资格或引用批准。Interpreter prompt variables 在基线模板中禁用，避免把外部模型输出混入原始捕获事实。

资料笔记必须在正文中区分原文摘录和使用者批注。独立形成、能够复用的理解另建 `Content/` 内容单元，并通过正文链接或现行 `source`／`references` 关系回到已经取得正式身份的内容单元或实体。

需要进入内容单元 `references` 或 `source` 字段的文献、标准等对象，必须先在正式实体词表中取得稳定身份。普通网页 URL 可以留在资料文件或正文中，但不能冒充受控 `references` 值。

### 内容单元

`Content/` 中每个 Markdown 文件恰好表示一个现行内容单元。路径由 `identifier` 决定，一级标题保存 `title`，frontmatter 保存 Obsidian binding。文件名、标题、alias 和显示文本不能反推 identifier。

建立内容单元时必须取得以下值：

- `identifier`；
- `title`；
- 恰好一个 `type`；
- 恰好一个 `genre`；
- 至少一个非 deprecated `subject`；
- `created`；
- 初始 `status: draft`。

`form`、`level`、`entities`、`source`、`references`、`modified`、`isReplacedBy`、`relation` 和非默认 `language` 按现行内容模型的条件填写。工具不得为了创建速度降低必填性；不能判断必填值时，材料继续留在 Inbox。

### 人工索引

`Indexes/` 中的应用索引是使用者维护的导航文件，不是内容单元、主题概念、数组或正式概念组。它只保存入口说明、排序、阅读路径、嵌入 Base 和普通链接；其中的成员关系不能进入内容字段，也不能被维护工具自动转换成正式关系。

现行载体词表另有 `form: index`。若一篇索引包含可以独立引用、需要受控标引的实质说明，它必须建立为 `Content/` 内容单元并使用适用的 `form: index`；`Indexes/` 只链接该内容单元或嵌入其视图，不保存第二份正文。这样把应用导航壳与正式内容载体分开。

### 正式表示

`KB/` 继续由六份正式词表生成。全部现行主题、数组、实体、来源用途、类型、体裁和载体导出能力保留。正式对象按稳定 ID 路径生成，包含现有 labels、aliases、状态、关系、依据和正文 loss 表示。

正式对象页面新增面向内容使用者的派生入口时，只能读取 `Content/` 的受控引用并显示结果；不得把反向引用写回正式 YAML 或对象页的正式字段。首轮实现可以把内容使用入口放在独立 Base 或报告中，不必重写每个对象页。

### 派生结果

报告只保存可重算事实和带上下文线索。每次生成覆盖 `App/Reports/` 的受管理报告集合，不读取旧报告作为新结论输入。

报告至少包括：

- 内容校验结果；
- 主题直接引用计数；
- 主题分支聚合计数；
- `unassigned` 主题及其引用情况；
- 无效或 deprecated 受控引用；
- 重复内容 ID；
- 内容关系互反缺失；
- 内容正文中未解析字符串的 report-only 线索；
- 维护阈值命中的复核事项。

报告不能自动修改内容状态、主题状态、正式词表、术语、来源或决定。

## 内容流程

### 资料进入

```text
随手记录、链接、网页、书籍、PDF
                |
                v
             Inbox
                |
           人工判断去向
          /       |       \
       丢弃    Sources    Content
                  |          ^
                  +----------+
                   理解与转述
```

Obsidian URI、Unique note creator 和普通新建命令只可作为 Inbox 捕获入口。Unique note creator 的时间名称不是正式内容 identifier。

Web Clipper 默认只写 `Sources/Clippings/`。它可以创建或追加资料文件，但不能直接创建 `Content/` 文件、正式实体、正式来源用途或词表记录。

### 内容建立

内容建立必须通过受管理模板或同等创建工具完成。核心 Templates 只能插入文本和日期，不能保证稳定 ID、受控值或必填性，因此“插入模板”本身不构成合法建立。首轮应用需要一个内容建立命令，在写文件前完成：

1. 取得或验证 identifier；
2. 检查目标路径不存在；
3. 让使用者选择 type、genre 和至少一个 subject；
4. 写入 title、created 和 `status: draft`；
5. 生成完整 frontmatter 与一级标题；
6. 写后回读并运行单文件校验。

命令可以先以仓库脚本提供，再通过 Obsidian URI、命令面板集成或未来插件缩短交互；不得因 UI 尚未实现而使用空字段模板建立无效内容。

### 内容成熟

`draft` 转为 `active` 前必须满足：

- 文件能够独立引用，主要讲一个明确问题；
- 所有必填字段存在且基数正确；
- 所有受控引用解析到正确对象种类；
- subject 不指向 deprecated 主题；
- 内容间 relation 满足互反条件；
- 外部材料、原文摘录、使用者转述和个人判断能够区分；
- 未核实字符串没有被自动写成主题、实体或术语；
- 使用者明确批准状态变化。

校验器只报告是否满足机械条件。内容是否已经形成可用理解，以及引用是否支持陈述，由使用者判断；脚本、Base、反向链接和语言模型都不能替代该判断。

### 内容废弃

内容单元转为 `deprecated` 后保持原 identifier 和路径，不移入 Archive，不删除。因直接替代且有替代项时填写 `isReplacedBy`；确认过时且无替代项时在正文首段说明原因。只有误建且没有任何引用的内容单元，才可按现行处置决定销毁。

## 字段表示

内容 binding 沿用现行 target 已核对的字段矩阵：`kb_id`、`kb_type`、`kb_genre`、`kb_form`、`kb_level`、`kb_subjects`、`kb_entities`、`kb_source`、`kb_references`、`kb_created`、`kb_modified`、`kb_status`、`kb_is_replaced_by`、`kb_relation` 和 `kb_language`。

本次重写不得改变应用无关字段语义、基数和值域。实现必须把“尚未实现”的内容矩阵转为实际内容合同，并为每个字段补齐：创建条件、编辑条件、解析目标、显示、查询、错误和 loss 验收。

同名 property 在一个 vault 中保持同一 Obsidian type。引用单值使用 Text link，引用多值使用 List of Text links；日期使用 Date；受控 literal 使用 Text。`title` 保存在一级标题，需要 Base 查询时可同时保存 Text property，但一级标题和 property 不一致必须报告。

tag 不承担主题、实体、文档类型、体裁或生命周期语义。固定应用 tag 只能用于区分系统对象或视图范围，不可替代受控字段。

## 身份路径

内容文件使用 `Content/<identifier>.md`。引用以稳定 ID 计算路径，以当前标题或正式 label 计算显示文本。

```md
[[Content/<identifier>|内容标题]]
[[KB/Topics/security|安全]]
[[KB/Entities/obsidian|Obsidian]]
```

显示文本不参与解析。内容标题修改不改 identifier 和路径。若内容 identifier 已被其他内容引用，不能修改；错误名称通过 title 和正文修正。

正文中的普通内部链接可以表达阅读关系，但只有 `kb_relation` 承担现行内容模型的互反 relation。反向链接、共同出现和图中邻近都不能自动建立 `kb_relation`。

## 模型缺口

现行内容模型把内容单元纳入与词表概念共用的 identifier 规则：优先从已有且有依据的英文 label 取得，没有时使用来源代码或编号，不使用拼音或自造英文。该规则适合正式词表对象，却没有完整回答一篇任意中文内容在没有获准英文 label、来源代码或编号时怎样取得 identifier。

Obsidian target 无权自行补出一种正式 ID。内容建立器不得默认把标题机翻成 slug，也不得把 Unique note creator 的时间名称、随机 UUID、文件名或语言模型输出静默升级为现行 identifier。

因此实施前必须先在应用无关内容模型中完成内容 identifier 发放规则的概念研究和决定。候选方案可以包括与显示名称无关的不透明身份，但本规格不预先选择形式。该规则未批准前，可以实现 Inbox、Sources、词表表示和只读内容校验，不能宣称正式内容建立流程已经完成。

## 导航结构

### 全库入口

`Home.md` 是使用者入口，初始化后不再由项目覆盖。初始内容至少链接：Inbox、外部资料、全部内容、草稿、最近修改、人工索引、正式主题、实体、来源用途和维护报告。

Bookmarks 可以固定 Home、Inbox、常用索引、草稿视图和维护报告。Bookmarks 是个人快捷入口，不属于项目正式数据；初始化器可以给出建议，不能覆盖用户后续布局。

### 人工索引

人工索引负责“怎样理解和进入一组内容”。它可以选择内容、解释关系、安排阅读顺序和嵌入 Base。一个内容可以进入多个索引，索引也可以互相链接。

索引不得把自己的层级和成员反写为正式主题关系。若索引长期暴露新的稳定分类需要，维护报告保存位置和上下文，由人工判断是否应提出正式主题、数组、分面或概念组变更。

### 自动视图

`App/Views/` 的基线使用 Obsidian Bases，不使用 Dataview。至少提供：

- 全部内容；
- 草稿内容；
- active 内容；
- deprecated 内容；
- 按主题；
- 按实体；
- 按类型与体裁；
- 最近修改；
- 全部正式主题；
- `unassigned` 主题；
- 正式实体；
- 正式来源用途；
- 维护报告入口。

Base 可以编辑文件和 properties，因此“受管理视图”只表示项目效力和生成权，不表示 UI 权限。首轮实现不得依赖 Base 编辑来执行状态批准、正式关系修改或词表维护。

### 主题入口

正式主题树继续回答知识范围和结构。主题入口必须同时提供：

- 上位、下位、相关和数组导航；
- 正式 scope、依据、状态和外部映射；
- 直接使用该主题的内容列表；
- 仅作统计的下位分支聚合计数；
- `unassigned` 和零引用提示。

分支聚合只用于覆盖观察，不自动把下位内容的 subject 增加为上位主题，也不改变主题引用语义。

### 实体入口

实体入口显示正式身份、kind、subject、来源信息和涉及该实体的内容。内容列表必须从 `kb_entities`、`kb_references` 和适用的 `kb_source` 分开计算，不能把正文提及、反向链接和正式字段合成一种关系。

## 盲区观察

### 结构盲区

结构盲区来自已借入的完整知识体系。`status: unassigned` 的正式主题即使没有内容也必须保留并可浏览。应用不得隐藏空分支、删除零引用主题或用已有内容反向裁剪正式结构。

结构盲区视图至少显示主题 ID、label、上位、来源、状态、直接内容数和分支聚合内容数。应用只显示事实，不自动把 `unassigned` 改为 `active`。

### 使用盲区

使用盲区来自实际写作和检索，包括：

- 内容无法选择合适的正式主题；
- 正文出现反复使用但未登记的字符串；
- 某个宽主题吸收过多内容；
- 内容实际集中在正式结构的一小部分；
- 同一实体、来源或主题被不一致地表示；
- 用户建立索引时反复需要正式结构没有的稳定入口。

核心 Search 可以全文和 property 查询，也能显示近期查询，但没有本项目可审计的搜索事件接口，因此当前不能计算“未匹配检索次数”。该指标继续等待真实查询消费者或明确的日志接口，不能用 Search UI 存在冒充实现。

未解析字符串诊断必须保存文件、位置和上下文。它只形成 report-only 线索，不自动创建候选、designation、概念、关系或违规结论。

### 使用计数

正式使用计数只读取 `Content/` 中通过校验的受控字段：

- 主题使用读取 `kb_subjects`；
- 实体涉及读取 `kb_entities`；
- 引用读取 `kb_references`；
- 派生来源按目标种类读取 `kb_source`。

正文 Wikilink、反向链接、alias 命中、unlinked mentions、索引成员和 graph edge 不进入正式使用计数。它们可以提供人工探索线索，但不能替代字段语义。

## 维护反馈

应用反馈按下列单向流程处理。

```text
内容和资料
    |
    v
机械校验与统计
    |
    v
App/Reports 带上下文线索
    |
    v
人工复核与决策权判断
    |
    v
修改 kb-design 的正式编辑源
    |
    v
重新生成受管理表示
    |
    v
重新校验内容与报告
```

报告命中维护阈值时，只提出适用动作：批准、废弃、删除、拆分、合并、找依据、复核来源、注明不覆盖或发版。报告不能执行这些动作，也不能把 L2 或 L3 决定降为工具动作。

主题引用使 `unassigned` 具备转为 `active` 的现行触发条件时，报告列出内容位置和主题；正式状态只有经过项目决策后才改变。过度使用、长期零覆盖和“其他”类目同样只触发复核。

## 能力使用

| Obsidian 能力 | 本项目用途 | 不能承担 |
|---|---|---|
| File Explorer | 浏览稳定职责目录和文件 | 主题树、多上位、状态和正式关系 |
| Properties | 保存内容 binding 和可查询事实 | nested formal structures、自动语义判断 |
| Properties view | 维护同名 property type 一致性 | 正式 schema 与完整校验 |
| Templates | 插入合法结构片段和日期 | 分配有依据的 ID、选择受控值、保证完整性 |
| Unique note creator | 快速建立 Inbox 临时文件 | 正式内容 identifier |
| Web Clipper | 本地保存网页内容、URL 和页面变量 | 直接建立内容单元、正式实体、术语或来源资格 |
| Internal links | 表达 target reference syntax 和普通阅读链接 | 自动取得项目关系效力 |
| Backlinks | 查看 linked／unlinked mentions 和人工上下文 | 正式引用计数、relation 或概念判断 |
| Bases | 查看、排序、筛选和编辑文件及 properties | 权限只读、正式审批、数据源或回流 |
| Search | 全文、路径、tag 和 property 查询 | 可审计的未匹配查询日志 |
| Bookmarks | 固定个人常用入口 | 项目导航真值 |
| Graph | 探索现有文件链接 | 正式主题树、关系证明或盲区计量 |
| Canvas | 临时整理和讨论 | 正式结构、内容模型或编辑源 |

基线不安装社区插件。未来引入插件前必须说明它解决的真实失败、退出路径、数据位置、对 Markdown 的影响和缺失时的降级行为。Dataview 可以作为增强查询，但普通 Markdown、Base 和报告必须继续提供核心入口。

## 配置边界

初始化器只设置应用运行所需的最低配置：

- 启用 Properties、Templates、Bases、Search、Backlinks、Bookmarks 和适用的核心能力；
- 指定 `App/Templates/` 为模板目录；
- 指定 `Attachments/` 为附件目录；
- 启用内部链接随 Obsidian 内移动和改名更新；
- 登记项目 property types；
- 为用户提供建议的 excluded files 和 Bookmarks，不强制覆盖个人选择。

主题、字体、窗口布局、快捷键、移动端布局、Sync、Publish 和个人插件属于用户配置。项目 manifest 不应把这些变化误报为正式表示漂移。

## 生成结构

现有 `scripts/export_obsidian.py` 继续作为六份正式词表表示的事实基线，但完整应用不再由一个承担全部职责的大脚本实现。实施计划应按边界拆分：

- 正式对象表示构建器；
- 新 vault 初始化器；
- 内容建立器；
- 内容校验器；
- 使用统计与报告生成器；
- 受管理文件 manifest；
- CLI 入口。

模块之间通过内存对象或明确文件合同协作。初始化器只接受不存在或为空的目标目录，构建完整新 vault 后回读校验，再发布。当前不实现对非空 vault 的更新，因此不会删除、覆盖或移动用户内容。

## 失败处理

| 失败 | 处理 |
|---|---|
| 正式词表或受管理表示无效 | 阻断初始化，不创建目标 vault |
| 目标目录非空、是符号链接或受保护路径 | 阻断，不修改目标 |
| 内容 ID 重复或路径冲突 | 内容校验失败，报告全部冲突位置 |
| active 内容缺少必填字段 | 报告为阻断问题，不自动降为 draft |
| draft 内容字段无效 | 报告问题，保留用户文件，不自动改写 |
| 受控引用悬空或对象种类错误 | 报告源文件、字段、值和目标期望 |
| relation 不互反 | 报告两端，不自动补关系 |
| 受管理文件被用户修改 | manifest 报告漂移，不把修改回写正式数据 |
| Web Clipper 提取缺失或错误 | 保留 URL 与原始上下文，交人工修正，不建立正式对象 |
| 报告生成中断 | 保留用户内容和受管理表示；临时报告目录不发布 |
| 社区插件缺失 | 基线功能不受影响；增强视图不可用但有普通入口 |

任何诊断失败都不得删除、移动、降级或改写用户内容。自动修复能力不在首轮范围。

## 安全边界

网页、PDF、摘录和外部 vault 内容属于不受信任输入。捕获器保存内容时不得执行其中的命令、代码或提示。Web Clipper Interpreter 基线禁用；未来启用时必须单独说明模型提供方、传输内容、隐私、成本和输出的非正式效力。

Markdown 中的 HTML、脚本、data URI、嵌入和附件路径需要在实现计划中建立允许范围。Obsidian 能显示某种内容不等于项目应接受其进入 active 内容。

## 实施阶段

完整应用分三阶段，不把未实现能力写成当前状态。

### 设计同步

- 重写 `design/targets/obsidian.md`，把词表参考导出放入完整应用架构；
- 核对 `design/content-model.md`、`design/maintenance.md`、`design/README.md`、根 README 和 AGENTS 摘要；
- 更新 Obsidian 官方来源笔记，补 Web Clipper、Bookmarks、Unique note creator、内容创建和查询限制；
- 若完整应用职责改变已采纳决定的边界，先提交 L3 决定提案，不静默改写旧决定。

设计同步仍不代表消费者启用。

### 新库生成

- 拆分正式表示、初始化、内容建立、校验和报告组件；
- 生成新的空 vault；
- 提供最低配置、模板、Base、规则说明、报告入口和 manifest；
- 只验收新目录生成，不处理非空 vault 更新。

新库生成完成后，内容消费者代码存在，但只有实际创建并读取内容时才取得运行证据。

### 使用验收

- 用小型、非正式样本完成捕获、资料保存、内容建立、draft 校验、active 批准、主题浏览、盲区报告和反馈全过程；
- 样本不进入正式知识库，也不自动修改正式词表；
- 根据真实使用校准布局、创建交互和报告可读性；
- 只有这一阶段通过后，才决定是否设计非空 vault 更新、回流、查询日志或插件。

## 验收门禁

只保留能发现高风险失败且有独有证据的检查。

| 风险 | 必要证据 |
|---|---|
| 用户内容被生成器覆盖 | 初始化目标限制、受管理写集检查和端到端用户路径不写入证明 |
| 临时材料冒充内容单元 | Inbox／Sources 与 Content 的模型和校验差异 |
| 内容字段改写应用无关模型 | 内容字段矩阵逐项对照 |
| 稳定身份被标题或文件名替代 | rename、显示文本变化和引用解析检查 |
| 受控引用悬空或串表 | 内容 validator 的目标种类与路径检查 |
| 报告修改正式数据 | 报告写集和正式输入 hash 对照 |
| 盲区计数把普通链接当正式引用 | 只读取受控字段的统计检查 |
| Base 或反向链接被误当审批 | 文档、视图和状态转换行为对照 |
| 未解析字符串自动建立对象 | report-only 输出与正式写集对照 |
| 正式对象导出回归 | 现有 exporter 高价值回归与冻结输出比较 |
| 新 vault 缺少必要入口 | 一次端到端新库生成与可解析文件集合检查 |

不为文件存在、常量回显、包装透传、重复计数或已经由端到端写集覆盖的事实增加测试。文档和静态配置使用直接校验；只有保留的行为风险使用 TDD。完整回归只在阶段边界运行一次。

## 完成口径

设计完成必须满足：

- Obsidian 明确成为 `kb-design` 的落地应用层，而不是词表预览器；
- 用户内容、受管理表示和派生结果权属分开；
- 临时捕获、外部资料和内容单元不混淆；
- 内容建立、生命周期、字段、身份、引用和失败处理完整；
- 正式主题树、人工索引和自动视图职责分开；
- 结构盲区、使用盲区、使用计数和维护反馈有可执行数据流；
- Obsidian 核心能力的用途和不能承担的职责明确；
- 社区插件、搜索日志、更新、回流和自动修复保持后置；
- 现有词表导出被保留为子系统，不再代表完整应用完成；
- 没有因设计文件存在而宣称真实 vault、内容消费者、内容数据或运行证据已经存在。

## 实施写集

用户批准本规格后，实施计划至少覆盖以下项目文件；具体写集由计划逐项冻结。

- `design/targets/obsidian.md` 整篇重写；
- `sources/obsidian-help.md` 整篇同步实际读到的官方能力；
- `design/content-model.md`、`design/maintenance.md` 和适用决定的必要整节同步；
- `design/README.md`、根 `README.md` 与 `AGENTS.md` 状态同步；
- Obsidian 生成、初始化、内容建立、校验和报告脚本；
- 只覆盖高风险行为的测试和固定样本；
- 现有 exporter 的保留、拆分或替代迁移说明。

项目正文按目的整节或整篇重写，不追加“完整应用补充”小节，不把本 Superpowers 规格复制进项目设计。

## 权威来源

- [Obsidian Properties](https://obsidian.md/help/properties)：property 类型、全 vault 同名类型、YAML、internal link 和 nested properties 限制。
- [Obsidian Bases](https://obsidian.md/help/bases)：本地 Markdown 与 properties 上的可编辑、排序和筛选视图。
- [Obsidian Search](https://obsidian.md/help/plugins/search)：全文、路径、tag、property 查询和近期查询的 UI 边界。
- [Obsidian Backlinks](https://obsidian.md/help/plugins/backlinks)：linked 与 unlinked mentions。
- [Obsidian Graph](https://obsidian.md/help/plugins/graph)：文件链接图、筛选、orphans 和 local graph。
- [Obsidian Bookmarks](https://obsidian.md/help/plugins/bookmarks)：文件、目录、搜索、图、标题、块和链接快捷入口。
- [Obsidian Templates](https://obsidian.md/help/plugins/templates)：模板目录、标题和日期变量、property 合并及 Source mode 注意事项。
- [Obsidian Unique note creator](https://obsidian.md/help/plugins/unique-note)：时间名称、冲突处理和模板入口。
- [Obsidian Web Clipper](https://obsidian.md/help/web-clipper)：本地网页捕获、highlights、Reader 和模板入口。
- [Web Clipper Templates](https://obsidian.md/help/web-clipper/templates)：创建、追加、模板触发和 JSON 导入导出。
- [Web Clipper Variables](https://obsidian.md/help/web-clipper/variables)：title、author、content、published、date、url、schema 和 prompt variables。
- [Obsidian Internal links](https://obsidian.md/help/links)：文件、标题、块链接和改名更新行为。
- [DCMI Application Profile Guidelines](https://www.dublincore.org/specifications/dublin-core/application-profile-guidelines/)：功能范围、模型引用、字段约束、使用和表示职责。

## 复核问题

用户审阅本规格时只需确认以下架构问题；具体字段和路径差异在实施计划中冻结。

1. 一个 vault 与三种权属是否继续成立？
2. Inbox 和外部资料不属于内容模型是否符合使用预期？
3. Content 必填值在建立前完成，而不是允许残缺内容文件，是否可以接受？
4. 人工索引只作个人导航、不取得正式关系效力，是否符合预期？
5. 首轮只初始化新 vault、不实现非空 vault 更新，是否符合当前阶段？
6. 社区插件和 Web Clipper Interpreter 不作为基线，是否符合可治理目标？
