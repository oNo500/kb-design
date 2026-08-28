# 术语概念基础

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重建术语治理所依赖的来源笔记、术语表和概念文，使后续项目设计只引用已经实际核对且边界明确的外部概念。

**Architecture:** 先固定官方材料的版本与实际阅读范围，再逐项审查术语表，最后按“术语数据库—受控词表—映射与溯源—组织与治理”的依赖顺序整篇重写概念文。本文档只实施 `sources/` 与 `concepts/` 的依据层，不修改项目规则、词表数据或脚本。

**Tech Stack:** Markdown、官方标准页面与可公开核对的标准正文、现有 Python 校验脚本、Git。

**Spec:** [术语治理设计](../specs/2026-08-27-terminology-governance-design.md)

## 全局约束

- 必须在独立 worktree 和功能分支执行，不得在 `master` 上修改。
- 第一次写文件前，按 `design/governance.md` 提交本计划列出的 L2 文件清单和小节清单；人明确批准后才继续。
- 本计划不授权来源改档、零自定例外、草案生效、范围改变或发版。发现这些事项时只列对象和证据，另交 L3 决定。
- `concepts/` 只解释外部概念和适用边界；项目字段、数量、期限、批准权限与迁移规则不写入概念文。
- `sources/` 只记录实际读到的材料、版本、位置和未读范围。收费正文中没有实际读到的条款不得写成已核事实。
- 没有可重复定位依据的中文译名不采用。官方材料只给英文时保留英文，并用有来源的中文解释，不自行造译名。
- 触及一节以上的旧文全部按目的重写。写前按“旧文去向”逐项登记，写后逐项核销，不做局部补丁。
- 所有标题遵守 `design/writing.md`：小节标题为 2–8 字名词短语，不加序号、冒号、字段名或参数。
- 汉字与西文、数字之间保留一个半角空格；中文句子用全角标点和“ ”。
- 外部事实在写入前重新打开官方页面核对。链接使用页面标题，不使用裸网址。
- 本计划不创建 `vocab/terms.yaml`，不改 `concepts/glossary.md` 的编辑源身份，不实现 TBX、Obsidian、生成器或迁移脚本。
- 每个提交只包含本任务列出的文件，提交说明使用 `[L1]` 或 `[L2]`。

## 文件职责

| 文件 | 操作 | 单一职责 |
|---|---|---|
| `sources/terminology-standards.md` | 新建 | 记录 ISO、GB/T 与 TBX 术语工作材料的版本、公开可核内容和未读范围 |
| `sources/metadata-standards.md` | 新建 | 记录 DCMI、PROV-O、SKOS 与 BCP 47 的实际核对范围 |
| `sources/iso-25964.md` | 整篇重写 | 记录 ISO 25964 已读材料，不从未读正文推导条款 |
| `sources/z39-19.md` | 整篇重写 | 记录 Z39.19 已核条款和修订状态 |
| `sources/iso-15489.md` | 重写“对本库的检验”一节 | 只保留正文实际支持的文件管理结论，取消对旧 `origin` 的依赖 |
| `concepts/glossary.md` | 整篇重写 | 逐条给出可定位来源；删除“自定”和空出处作为已批准依据的做法 |
| `concepts/terminology-database.md` | 新建 | 解释术语数据库、术语条目、多语层次和维护要求 |
| `concepts/controlled-vocabulary.md` | 整篇重写 | 区分概念、术语、标签、词表结构和关系层次 |
| `concepts/vocabulary-construction.md` | 整篇重写 | 区分术语工作中的依据、候选发现、建设和维护 |
| `concepts/vocabulary-mapping.md` | 整篇重写 | 解释概念映射及其证据边界，不把映射当成本地断言依据 |
| `concepts/vocabulary-hierarchy.md` | 整篇重写 | 解释层级、数组、节点标签、划分特征和多层级 |
| `concepts/metadata.md` | 整篇重写 | 区分描述性元数据、来源元数据、派生关系和本地依据 |
| `concepts/classifying-new-subjects.md` | 整篇重写 | 解释新主题分析所需的概念依据，不预设项目字段 |
| `concepts/body-of-knowledge.md` | 整篇重写 | 区分知识体系身份、受控词表身份和项目使用角色 |
| `concepts/governance.md` | 整篇重写 | 区分外部证据、项目批准、维护义务和执行角色 |
| `concepts/README.md` | 整篇重写 | 用新的概念依赖关系重建索引和阅读顺序 |

## 旧文去向

| 旧文 | 保留并重写 | 移出或纠正 |
|---|---|---|
| `concepts/glossary.md` | 有可定位权威来源的术语、英文形式和定义 | “自定”、空出处、未读 ISO 条款号、未经核对的中英对应不得继续作为批准依据 |
| `controlled-vocabulary.md` | 定义、用途、结构形态、等价关系、层级关系、相关关系 | “词与词的三种关系”改为术语关系与概念关系；产品实例移出主题概念树；SKOS 映射细节交给映射文 |
| `vocabulary-construction.md` | 文献依据、组织依据、用户依据、候选发现、建设与维护 | `warrant` 不再等同项目逐值 `basis`；项目状态和字段交给项目设计 |
| `vocabulary-mapping.md` | 映射类型、结构模型、互操作用途 | 删除“借来权威性”和默认 `closeMatch`；任何映射都改为按双方定义与范围判断 |
| `vocabulary-hierarchy.md` | 层级类型、数组、节点标签、划分特征、多层级 | 删除个人实例和“加入几个数组即多层级”的混用；不把数组一律简化为一个划分特征 |
| `metadata.md` | Dublin Core 基础、元数据与词表分工 | `dcterms:source`、PROV 派生和本地断言依据分开，不再用“标识文档属性”概括全部元数据 |
| `classifying-new-subjects.md` | 分析综合、文献依据、剩余监控 | 旧 `origin` 按发现、依据、派生三种语义解释；项目分面和字段结论移出概念文 |
| `body-of-knowledge.md` | BOK 的定义、结构与实例 | 不再把 BOK、分类表和 taxonomy 当同义词；“只借上两层”等本地参数移出概念文 |
| `governance.md` | 治理与维护、角色和复核 | 外部材料只证明概念，不能代替本地批准；具体权限和流程移交项目设计 |
| `sources/iso-25964.md` | 实际读到的定义、公开数据模型材料、免费材料清单 | 删除无损 RDF 映射等过度断言；未读条款不再用确定语气；更新两个部分的修订状态 |
| `sources/z39-19.md` | 已读全文中的候选、建设、维护和来源字段条款 | 现行标准与修订项目分开记录，不推测修订稿内容 |
| `sources/iso-15489.md` | 已读正文支持的 record、disposition 和保留边界 | 删除由旧 `origin` 字段反推“不删”的循环论证；未核的 GB 采标关系不写 |
| `concepts/README.md` | 概念图和阅读顺序 | 删除个人作为概念、标点违规标题和已经纠正的三种外部用法简化 |

## 执行顺序

来源基线先于术语表；术语表先于概念文；概念文按引用方向从基础对象写到项目用途。任何一步发现需要项目规则才能作结论时，将结论留给下一份“项目治理草案”计划，不在本计划补写。

---

### 基线核对

**Files:**

- Read: `design/governance.md`
- Read: `design/writing.md`
- Read: `concepts/CONVENTIONS.md`
- Read: 本计划“文件职责”和“旧文去向”列出的全部旧文
- Modify: none

**Interfaces:**

- Consumes: 获准规格、现行决策权、现行写作规则。
- Produces: 执行基线、精确 L2 提案和旧文核销表。

**Steps:**

- [ ] 运行 `git status --short --branch`；预期位于独立功能分支且工作区为空。
- [ ] 运行 `python3 scripts/check-links.py`；预期输出“全部链接有效”。
- [ ] 运行 `python3 scripts/check-topics.py`；保存概念、数组、实体、来源、候选和 `self` 的基线输出，不修改数据。
- [ ] 运行 `python3 scripts/check-terms.py --all`；保存现有未登记候选数量，明确该脚本当前只报告、不作为零候选承诺。
- [ ] 用 `rg -n '^#{1,4} '` 列出全部待重写文件标题，逐项复制到执行清单。
- [ ] 向人提交精确 L2 提案：新建两份来源笔记和一份概念文，整篇重写本计划列出的来源笔记、术语表、八份概念文与概念索引；明确不改 `design/`、`vocab/`、`scripts/`。
- [ ] 等待人明确批准该文件清单和小节清单；未批准时停止，不创建文件。

### 术语来源

**Files:**

- Create: `sources/terminology-standards.md`

**Interfaces:**

- Consumes: ISO 704、ISO 1087、GB/T 15237、ISO 10241-1、GB/T 20001.1、ISO 26162-1、ISO 26162-3、ISO 30042、GB/T 44227、TBX-Basic 的官方页面。
- Produces: 可供术语表和术语数据库概念文引用的阅读边界。

**Steps:**

- [ ] 再次打开规格“概念依据”中的每个官方页面，记录标准编号、版次、现行状态、采标关系页面原文能够确认的范围和核对日期。
- [ ] 对每个标准分别记录“公开页面已读”“可访问正文已读”“付费或未取得正文”三种范围，不把摘要扩写成条款。
- [ ] 建立标题骨架：`阅读范围`、`基础术语`、`条目结构`、`数据库`、`交换边界`、`版本状态`、`未读范围`。
- [ ] 写“基础术语”时只使用 GB/T 15237 或实际读到的 ISO 1087 表述；没有读到中文术语条目时不反译。
- [ ] 写“条目结构”和“数据库”时分别限制在 ISO 10241-1 与 ISO 26162 官方页面实际支持的范围。
- [ ] 写“交换边界”时记录 ISO 30042 的元模型、数据类目和 XML 表示范围，以及 TBX-Basic 页面列出的层次与数据类目；明确它们不规定本库内部 YAML。
- [ ] 运行 `python3 scripts/check-links.py`；预期“全部链接有效”。
- [ ] 运行 `git diff --check`；预期无空白错误。
- [ ] 提交：`git add sources/terminology-standards.md && git commit -m "[L1] 来源:记录术语标准阅读边界"`。

### 元数据来源

**Files:**

- Create: `sources/metadata-standards.md`

**Interfaces:**

- Consumes: DCMI Metadata Terms、PROV-O、SKOS Reference、BCP 47 官方文本。
- Produces: `source`、`match`、语言标签和元数据概念的外部边界。

**Steps:**

- [ ] 打开 [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)、[PROV-O](https://www.w3.org/TR/prov-o/)、[SKOS Reference](https://www.w3.org/TR/skos-reference/) 和 [BCP 47](https://www.rfc-editor.org/info/bcp47/)，记录版本、状态和核对日期。
- [ ] 建立标题骨架：`阅读范围`、`元数据来源`、`派生关系`、`概念映射`、`语言标签`、`适用边界`、`未读范围`。
- [ ] 在“元数据来源”中只说明 DCMI `source` 的定义域和值域，不把它扩写成本地逐值证据规则。
- [ ] 在“派生关系”中分别记录 PROV-O 的 derivation、revision、primary source 和 invalidation；不把日常“来自”自动映射为这些关系。
- [ ] 在“概念映射”中记录 SKOS 五种 mapping property 的关系边界；明确标签相同不证明概念映射。
- [ ] 在“语言标签”中记录 RFC 5646 对信息对象语言标识的用途；不自行规定本库字段形状。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 提交：`git add sources/metadata-standards.md && git commit -m "[L1] 来源:记录元数据标准边界"`。

### 词表标准

**Files:**

- Modify: `sources/iso-25964.md`
- Modify: `sources/z39-19.md`
- Modify: `sources/iso-15489.md`

**Interfaces:**

- Consumes: 已取得的 ISO 25964 免费材料、Z39.19 正文、ISO 15489 正文和三个标准组织的现行状态页面。
- Produces: 词表、映射、维护和文件管理概念文可引用的逐项证据。

**Steps:**

- [ ] 先把 `sources/iso-25964.md` 每个旧节标成“保留重写”“并入新节”或“删除并说明原因”，覆盖“旧文去向”表中的全部事项。
- [ ] 整篇重写 ISO 25964 笔记，使用 `材料身份`、`阅读范围`、`已核定义`、`关系模型`、`数据材料`、`修订状态`、`适用边界`、`未读范围` 八个小节。
- [ ] 对 ISO 25964 每条定义记录实际材料和位置；免费样本只到某一编号时，不引用样本外编号。
- [ ] 将 2026 年修订状态写成“现行版状态”和“后继项目状态”两项；不推测后继文本内容。
- [ ] 删除“ISO 模型可无损映射 RDF”等没有材料直接支持的结论；SKOS 对应只保留公开映射材料能够确认的内容。
- [ ] 先为 `sources/z39-19.md` 建立旧节去向，再整篇重写为 `材料身份`、`阅读范围`、`已核条款`、`维护依据`、`修订状态`、`适用边界`、`未读范围`。
- [ ] 核对 Z39.19 每个条款号确实存在于已读正文；NISO 修订项目只记录官方项目页可确认的状态。
- [ ] 只重写 `sources/iso-15489.md` 的“对本库的检验”整节：由 disposition 概念说明处置需经决定，不再以旧 `origin` 字段作为保留依据。
- [ ] 运行 `rg -n '无损|完全对应|后继版本将|origin.*不删' sources/iso-25964.md sources/z39-19.md sources/iso-15489.md`；预期没有未经限定的断言。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 提交：`git add sources/iso-25964.md sources/z39-19.md sources/iso-15489.md && git commit -m "[L1] 来源:重写词表标准笔记"`。

### 术语审查

**Files:**

- Modify: `concepts/glossary.md`

**Interfaces:**

- Consumes: 三份新旧来源笔记以及每行术语能够重复定位的官方材料。
- Produces: 后续概念文唯一可用的已核术语清单；仍不改变其当前手工编辑身份。

**Steps:**

- [ ] 导出术语表每一行的“中文、英文、定义、出处”，按现有小节建立逐行核对清单；不新增项目文件保存临时清单。
- [ ] 将出处缩写改为带标题的来源笔记链接和精确位置；同一缩写指向多个版次时拆开。
- [ ] 逐行核对“词表的类型”“基本单位”“关系”“结构”，删除未读条款号；概念关系不得再写成词与词关系。
- [ ] 逐行核对“注释与生命周期”“建设与治理”“词表间映射”“知识体系”，把外部工作流状态与本地状态分开。
- [ ] 逐行核对“元数据”“写作与设计方法”“笔记的类型”“治理与维护”“知识图谱”，没有权威来源的项目专用表达从术语表移回相应设计说明。
- [ ] 逐行核对“引用的标准与文献”，标准版次、标题和状态与 `sources/` 一致。
- [ ] 删除“自定”作为可批准出处的缩写；遇到没有来源但正文仍使用的术语，先删除或改写正文用语，不能给它补一个本库定义。
- [ ] 核对每个中英对照确实来自双语条目或同一概念的两项独立证据；只核到英文时，中文列留空并给有来源的解释。
- [ ] 将 TBX-Basic 的 `preferredTerm-admn-sts`、`admittedTerm-admn-sts`、`deprecatedTerm-admn-sts`、`supersededTerm-admn-sts` 保留为原值；中文只能作为解释，不宣称是标准译名。
- [ ] 运行 `python3 scripts/check-terms.py --all`；检查本文件重写没有引入新的未登记中文术语。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 提交：`git add concepts/glossary.md && git commit -m "[L2] 术语:重写术语依据表"`。

### 数据库概念

**Files:**

- Create: `concepts/terminology-database.md`

**Interfaces:**

- Consumes: ISO 704、ISO 1087、ISO 10241-1、ISO 26162、ISO 30042、TBX-Basic、BCP 47 的已核范围。
- Produces: 项目术语治理设计可引用的对象与层次，不产生字段方案。

**Steps:**

- [ ] 建立标题骨架：`定义`、`解决的问题`、`记录层次`、`多语对应`、`状态层次`、`维护要求`、`本库用途`、`权威来源`。
- [ ] 在“定义”中区分 terminological data collection、terminological entry、concept、designation 与 term；没有已核中文形式的概念保留英文。
- [ ] 在“记录层次”中解释概念层、语言层、术语层为何分开，不给出 YAML 字段或基数。
- [ ] 在“多语对应”中说明两种语言形式进入同一概念需要概念一致性证据，字符串相似和机器翻译不构成证据。
- [ ] 在“状态层次”中区分术语管理状态与项目记录工作流状态；只列 TBX-Basic 已核的术语状态。
- [ ] 在“维护要求”中只引用 ISO 26162-3 可确认的内容维护和质量范围，不预设本库周期。
- [ ] 在“本库用途”中只说明它将为项目设计提供概念依据，明确 YAML 和生成规则属于后续本地决定。
- [ ] 运行 `python3 scripts/check-links.py`、`python3 scripts/check-terms.py --all` 和 `git diff --check`；检查新文术语均已在术语表登记或保留原语言。
- [ ] 提交：`git add concepts/terminology-database.md && git commit -m "[L2] 概念:新增术语数据库依据"`。

### 词表概念

**Files:**

- Modify: `concepts/controlled-vocabulary.md`
- Modify: `concepts/vocabulary-construction.md`

**Interfaces:**

- Consumes: 术语表、ISO 25964 与 Z39.19 已核笔记、术语数据库概念文。
- Produces: 清楚区分概念、术语、词表关系、建设依据和维护活动的两篇概念文。

**Steps:**

- [ ] 分别为两篇旧文逐节登记去向，确认旧标题和旧例子全部有处置。
- [ ] 将受控词表文整篇重写为 `定义`、`解决的问题`、`结构形态`、`术语关系`、`概念关系`、`标签表示`、`本库用途`、`权威来源`。
- [ ] “术语关系”只解释同一概念的优先与非优先形式；“概念关系”解释层级与相关；SKOS 跨体系映射只链接映射文。
- [ ] 删除把 PostgreSQL 等个体直接放进主题概念层级的例子，改用标准材料中明确属于概念关系的例子。
- [ ] 将建设文整篇重写为 `定义`、`依据类型`、`候选发现`、`建设方法`、`条目内容`、`维护活动`、`本库用途`、`权威来源`。
- [ ] 将 literary warrant、organizational warrant、user warrant 保持为词表建设依据；明确它们不等同项目记录中支持一个具体值的 `basis`。
- [ ] 候选发现只描述标准中的活动，不把主题概念的 `candidate`、`unassigned` 或术语工作流混成一种状态。
- [ ] 运行 `rg -n '^#{2,4} .*[:：]|权威性.*借|PostgreSQL|候选词.*unassigned' concepts/controlled-vocabulary.md concepts/vocabulary-construction.md`；预期无旧混用。
- [ ] 运行三项文档校验；预期链接有效、术语无新增未登记项、`git diff --check` 通过。
- [ ] 提交：`git add concepts/controlled-vocabulary.md concepts/vocabulary-construction.md && git commit -m "[L2] 概念:重写受控词表基础"`。

### 映射概念

**Files:**

- Modify: `concepts/vocabulary-mapping.md`
- Modify: `concepts/metadata.md`

**Interfaces:**

- Consumes: SKOS、DCMI、PROV-O 来源笔记与重写后的受控词表概念。
- Produces: `basis`、派生来源和概念映射可在项目设计中分开的概念边界。

**Steps:**

- [ ] 分别为两篇旧文逐节登记去向。
- [ ] 将映射文整篇重写为 `定义`、`解决的问题`、`关系类型`、`映射模型`、`证据要求`、`互操作边界`、`本库用途`、`权威来源`。
- [ ] 明确 mapping relation 连接概念，不连接字符串；每种关系都要求比较定义和范围，拿不准不自动选择 `closeMatch`。
- [ ] 删除“映射把权威性借过来”；改为映射只声明概念关系，本地标签、层级、归属和批准各需自己的证据。
- [ ] 将元数据文整篇重写为 `定义`、`解决的问题`、`核心元素`、`术语体系`、`来源属性`、`派生关系`、`词表关系`、`本库用途`、`权威来源`。
- [ ] 在元数据文分别解释 DCMI `source` 与 PROV-O derivation；本地 `basis` 只在“本库用途”说明为后续设计问题，不伪装成 DCMI 或 PROV 要求。
- [ ] 运行 `rg -n '权威性.*借|默认.*closeMatch|字符串.*映射|source.*basis.*同' concepts/vocabulary-mapping.md concepts/metadata.md`；逐项确认没有旧结论或新的混同。
- [ ] 运行三项文档校验；预期均通过。
- [ ] 提交：`git add concepts/vocabulary-mapping.md concepts/metadata.md && git commit -m "[L2] 概念:重写映射与元数据边界"`。

### 组织概念

**Files:**

- Modify: `concepts/vocabulary-hierarchy.md`
- Modify: `concepts/classifying-new-subjects.md`
- Modify: `concepts/body-of-knowledge.md`
- Modify: `concepts/governance.md`

**Interfaces:**

- Consumes: 重写后的术语表、词表、映射、元数据概念文和对应来源笔记。
- Produces: 后续来源与术语项目草案所需的组织、分析和治理概念。

**Steps:**

- [ ] 为四篇旧文逐节登记去向，特别标出所有项目参数、字段和归属结论。
- [ ] 将层级文整篇重写为 `定义`、`层级类型`、`划分特征`、`数组`、`节点标签`、`多层级`、`适用边界`、`本库用途`、`权威来源`。
- [ ] 使用概念而非个人实例说明层级；分别解释“一个概念有多个上位”和“一个概念出现在多个展示分组”。
- [ ] 将新主题分类文整篇重写为 `定义`、`分析综合`、`依据类型`、`概念判定`、`剩余监控`、`适用边界`、`本库用途`、`权威来源`。
- [ ] 旧 `origin` 只作为当前项目混用案例出现，明确它可能表示候选发现、逐值依据或实际派生，具体迁移交项目设计。
- [ ] 将知识体系文整篇重写为 `定义`、`组成`、`常见实例`、`词表关系`、`使用角色`、`适用边界`、`本库用途`、`权威来源`。
- [ ] 分开“材料本身是什么”与“项目把它用于映射、结构、分组或发现”；删除“只借上两层”等本地参数。
- [ ] 将治理文整篇重写为 `定义`、`解决的问题`、`治理层次`、`证据边界`、`批准边界`、`维护边界`、`执行角色`、`本库用途`、`权威来源`。
- [ ] 明确外部来源支持事实或概念，项目批准允许采用，复核义务维持有效；三者互不替代。
- [ ] 运行 `rg -n '张三|只借.*层|origin.*来源|外部.*批准'` 检查四篇文件；旧例和混同应消失，必要的 `origin` 讨论必须带“旧字段”限定。
- [ ] 运行三项文档校验；预期均通过。
- [ ] 提交：`git add concepts/vocabulary-hierarchy.md concepts/classifying-new-subjects.md concepts/body-of-knowledge.md concepts/governance.md && git commit -m "[L2] 概念:重写组织与治理依据"`。

### 概念索引

**Files:**

- Modify: `concepts/README.md`

**Interfaces:**

- Consumes: 本计划完成后的全部概念文。
- Produces: 与真实引用方向一致的概念索引。

**Steps:**

- [ ] 为旧索引的“文章的关系”“词表结构总览”“阅读顺序”分别登记去向，再整篇重写。
- [ ] 在文章关系中把术语数据库置于术语与词表概念之前，把元数据、映射、层级和治理按引用方向连接。
- [ ] 重画文本示意时只使用概念实例，不使用具体个人充当概念；不把复制、映射和派生组说成同一关系。
- [ ] 阅读顺序使用连续的文章关系，不使用 `5a`、`8a` 等参数化序号；表中只回答每篇文章的概念问题。
- [ ] 检查索引中的每个链接与文章标题一致。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 提交：`git add concepts/README.md && git commit -m "[L2] 概念:重写概念文索引"`。

### 最终校验

**Files:**

- Verify: 本计划“文件职责”列出的全部文件
- Modify: only files that fail a listed acceptance check, by rewriting the affected whole section

**Interfaces:**

- Consumes: 全部任务提交。
- Produces: 可交付给项目治理草案计划的稳定依据层。

**Steps:**

- [ ] 按“旧文去向”逐行核销；每项必须标为“保留重写”“移入指定文档”或“删除并有理由”，不得留下无去向事项。
- [ ] 运行 `rg -n '^#{2,6} .*[:：]|^#{2,6} [0-9一二三四五六七八九十]'` 覆盖本计划改动的 Markdown；预期无标题违规。
- [ ] 人工核对每个小节标题是 2–8 字名词短语，且不含字段、文件名、数量或实现参数。
- [ ] 运行 `python3 scripts/check-links.py`；预期输出“全部链接有效”。
- [ ] 运行 `python3 scripts/check-terms.py --all`；把结果与基线比较，预期改动文件没有新增无依据术语，已审术语不再以“自定”或空出处获准。
- [ ] 运行 `python3 scripts/check-topics.py`；预期与基线同样通过，证明本计划未改词表数据。
- [ ] 运行 `git diff --check`；预期无错误。
- [ ] 以“基线核对”记录的提交 SHA 为左端运行 `git diff --name-only`；预期只出现“文件职责”中的 `sources/` 与 `concepts/` 文件。
- [ ] 阅读最终 `git diff`，确认没有 `design/` 规则、YAML 字段、阈值、Obsidian 或 TBX 实现混入概念层。
- [ ] 如校验修正了内容，按文件职责提交一笔 `[L1]` 来源或 `[L2]` 概念收口提交；没有修正则不制造空提交。
- [ ] 使用 `superpowers:requesting-code-review` 审查来源可定位性、术语准入、目录职责和旧文去向；处理反馈后重新运行全部校验。

## 完成条件

- 两份新来源笔记清楚区分已读、未读、现行版与修订项目。
- ISO 25964、Z39.19 和 ISO 15489 笔记不再超出实际阅读范围。
- 术语表每个保留条目都有可重复定位的外部依据；没有依据的中文译名未被采用。
- 新术语数据库概念文只讲外部概念，不预写项目 YAML。
- 八份概念文各守单一职责，`basis`、派生来源和概念映射不再混用。
- 旧节逐项有去向，标题、标点、链接和术语检查通过。
- `design/`、`vocab/`、`scripts/` 保持不变。

## 后续入口

本计划完成并通过审查后，执行 [项目治理草案](2026-08-28-terminology-project-design.md)。项目草案获准前，不编写数据迁移、生成器、来源探测、首轮维护或草案生效计划。
