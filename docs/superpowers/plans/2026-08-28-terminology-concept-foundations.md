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
- `scripts/check-terms.py` 只产生候选报告，不扫描术语表、标题或代码，也不以候选非零退出；任何任务都不得把它单独当作术语验收。
- 本计划不创建 `vocab/terms.yaml`，不改 `concepts/glossary.md` 的编辑源身份，不实现 TBX、Obsidian、生成器或迁移脚本。
- 本计划是程序分支的中间阶段，不是可合并状态。术语表删除无依据写法后，现行设计中的引用要留给后续项目设计与迁移计划处理；全部引用同步前不得使用分支收尾流程。
- 每个提交只包含本任务列出的文件，提交说明使用 `[L1]` 或 `[L2]`。

## 文件职责

| 文件 | 操作 | 单一职责 |
|---|---|---|
| `sources/terminology-standards.md` | 新建 | 记录 ISO、GB/T 与 TBX 术语工作材料的版本、公开可核内容和未读范围 |
| `sources/metadata-standards.md` | 新建 | 记录 DCMI、PROV-O、SKOS 与 BCP 47 的实际核对范围 |
| `sources/iso-25964.md` | 整篇重写 | 记录 ISO 25964 已读材料，不从未读正文推导条款 |
| `sources/z39-19.md` | 整篇重写 | 记录 Z39.19 已核条款和修订状态 |
| `sources/iso-15489.md` | 将“对本库的检验”整节重写为“适用边界” | 只记录正文实际支持的文件管理概念，不替项目作保留决定 |
| `concepts/glossary.md` | 全表只读审查；整节重写“基本单位” | 全表问题进入执行检查点；本计划只准入新概念文必需且已有依据的基础术语，不提前迁移活跃设计用语 |
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
| `concepts/glossary.md` | 全表逐行审查；“基本单位”整节中有依据的术语保留并重写 | 其他小节的“自定”、空出处、未读条款和未经核对中英对应只登记问题，留给术语数据与活跃设计原子迁移 |
| `controlled-vocabulary.md` | 定义、用途、结构形态、等价关系、层级关系、相关关系 | “词与词的三种关系”改为术语关系与概念关系；产品实例移出主题概念树；SKOS 映射细节交给映射文 |
| `vocabulary-construction.md` | 文献依据、组织依据、用户依据、候选发现、建设与维护 | `warrant` 不再等同项目逐值 `basis`；项目状态和字段交给项目设计 |
| `vocabulary-mapping.md` | 映射类型、结构模型、互操作用途 | 删除“借来权威性”和默认 `closeMatch`；任何映射都改为按双方定义与范围判断 |
| `vocabulary-hierarchy.md` | 层级类型、数组、节点标签、划分特征、多层级 | 删除个人实例和“加入几个数组即多层级”的混用；不把数组一律简化为一个划分特征 |
| `metadata.md` | Dublin Core 基础、元数据与词表分工 | `dcterms:source`、PROV 派生和本地断言依据分开，不再用“标识文档属性”概括全部元数据 |
| `classifying-new-subjects.md` | 分析综合、文献依据、剩余监控 | 项目 `origin` 字段及分面结论移出概念文；本文只一般性区分发现、证据与派生 |
| `body-of-knowledge.md` | BOK 的定义、结构与实例 | 不再把 BOK、分类表和 taxonomy 当同义词；“只借上两层”等本地参数移出概念文 |
| `governance.md` | 治理与维护、角色和复核 | 外部材料只证明概念，不能代替本地批准；具体权限和流程移交项目设计 |
| `sources/iso-25964.md` | 实际读到的定义、公开数据模型材料、免费材料清单 | 删除无损 RDF 映射等过度断言；未读条款不再用确定语气；更新两个部分的修订状态 |
| `sources/z39-19.md` | 已读全文中的候选、建设、维护和来源字段条款 | 现行标准与修订项目分开记录，不推测修订稿内容 |
| `sources/iso-15489.md` | 已读正文支持的 record 与 disposition 概念 | 删除由旧 `origin` 字段反推“不删”的循环论证；项目保留规则交后续设计；未核的 GB 采标关系不写 |
| `concepts/README.md` | 概念图和阅读顺序 | 删除个人作为概念、标点违规标题和已经纠正的三种外部用法简化 |

## 小节去向

以下映射在执行前已经确定。任务只逐项核销，不再现场决定目的地。

| 文件 | 旧节 | 确切去向 |
|---|---|---|
| `sources/iso-25964.md` | 这个标准是什么 | `材料身份` |
| `sources/iso-25964.md` | 适用范围 | `适用边界` |
| `sources/iso-25964.md` | 章节结构 | `阅读范围` 与 `未读范围` |
| `sources/iso-25964.md` | 关键定义 | `已核定义` |
| `sources/iso-25964.md` | 概念与词的分离 | `已核定义` |
| `sources/iso-25964.md` | 三类关系的定义 | `关系模型` |
| `sources/iso-25964.md` | 结构类术语 | `已核定义` |
| `sources/iso-25964.md` | 过程类术语 | `已核定义`；未读定义删除 |
| `sources/iso-25964.md` | 数据模型 | `数据材料` |
| `sources/iso-25964.md` | 数据模型的类 | `数据材料` |
| `sources/iso-25964.md` | 数据模型的关系 | `数据材料` |
| `sources/iso-25964.md` | 对知识图谱设计的含义 | 项目推论删除；公开模型事实并入 `数据材料` |
| `sources/iso-25964.md` | 与 SKOS 的对应 | 公开材料事实并入 `数据材料`，限制并入 `适用边界` |
| `sources/iso-25964.md` | 2026 修订版 | `修订状态` |
| `sources/iso-25964.md` | 免费材料清单 | `阅读范围` |
| `sources/iso-25964.md` | 阅读范围说明 | `阅读范围` 与 `未读范围` |
| `sources/z39-19.md` | 这个标准是什么 | `材料身份` |
| `sources/z39-19.md` | 核过的条款 | `已核条款` 与 `维护依据` |
| `sources/z39-19.md` | 未读的部分 | `未读范围` |
| `sources/iso-15489.md` | 这个标准是什么、关键定义、第 4 章原则、章节结构、免费材料 | 本计划不改，逐节原样保留 |
| `sources/iso-15489.md` | 对本库的检验 | 整节改为 `适用边界` |
| `sources/iso-15489.md` | 内容单元是不是 record | 项目判断删除；实际读到的 record 边界并入 `适用边界` |
| `sources/iso-15489.md` | “不删”有没有依据 | 项目判断删除；disposition 事实并入 `适用边界` |
| `sources/iso-15489.md` | 其他对应 | 标准事实并入 `适用边界`；项目对应删除 |
| `concepts/glossary.md` | 出处缩写 | 全表审查；不在本计划修改 |
| `concepts/glossary.md` | 词表的类型 | 全表审查；留给术语迁移 |
| `concepts/glossary.md` | 基本单位 | 本计划唯一整节重写的术语表小节 |
| `concepts/glossary.md` | 关系、结构、注释与生命周期 | 全表审查；留给术语迁移 |
| `concepts/glossary.md` | 建设与治理、词表间映射、知识体系 | 全表审查；留给术语迁移 |
| `concepts/glossary.md` | 元数据、写作与设计方法、笔记的类型 | 全表审查；留给术语迁移 |
| `concepts/glossary.md` | 治理与维护、知识图谱、引用的标准与文献 | 全表审查；留给术语迁移 |
| `concepts/controlled-vocabulary.md` | 定义、解决的问题 | 同名新节 |
| `concepts/controlled-vocabulary.md` | 词表的五种结构 | `结构形态` |
| `concepts/controlled-vocabulary.md` | 词与词的三种关系 | 拆入 `术语关系` 与 `概念关系` |
| `concepts/controlled-vocabulary.md` | 等价关系 USE / UF | `术语关系` |
| `concepts/controlled-vocabulary.md` | 层级关系 BT / NT、相关关系 RT | `概念关系` |
| `concepts/controlled-vocabulary.md` | SKOS 对应属性 | 映射文 `关系类型`；本文只保留链接 |
| `concepts/controlled-vocabulary.md` | 在知识库中的用法 | `本库用途` |
| `concepts/controlled-vocabulary.md` | 权威来源、标准、教材、词表实例 | `权威来源`；未实际使用的来源删除 |
| `concepts/vocabulary-construction.md` | 定义 | 同名新节 |
| `concepts/vocabulary-construction.md` | `词从哪来:三种依据` | `依据类型` |
| `concepts/vocabulary-construction.md` | 候选词的来源、候选词与层级补位 | `候选发现`；层级状态推论删除 |
| `concepts/vocabulary-construction.md` | `怎么建:两组方法` | `建设方法` |
| `concepts/vocabulary-construction.md` | `委员会法:专家列词`、`经验法:从内容对象抽词`、分面分析是第三条路 | `建设方法` |
| `concepts/vocabulary-construction.md` | 每个词的记录 | `条目内容` |
| `concepts/vocabulary-construction.md` | `维护:加、改、废` | `维护活动` |
| `concepts/vocabulary-construction.md` | 加词(§11.3.1.1)、改词(§11.3.1.2)、废词(§11.3.1.3, §11.3.2) | `维护活动`；标题中的条款号移入正文 |
| `concepts/vocabulary-construction.md` | 在知识库中的用法 | `本库用途` |
| `concepts/vocabulary-construction.md` | 与本库来源分级的关系 | 概念推论删除；项目部分留给来源治理草案 |
| `concepts/vocabulary-construction.md` | 权威来源 | 同名新节 |
| `concepts/vocabulary-mapping.md` | 定义、解决的问题 | 同名新节 |
| `concepts/vocabulary-mapping.md` | 映射的类型 | `关系类型` |
| `concepts/vocabulary-mapping.md` | 映射的结构模型 | `映射模型` |
| `concepts/vocabulary-mapping.md` | 与各类词表的互操作性 | `互操作边界` |
| `concepts/vocabulary-mapping.md` | 外部词表的三种用法 | 外部概念并入 `互操作边界`；本地角色值留给来源治理草案 |
| `concepts/vocabulary-mapping.md` | 在知识库中的用法 | `本库用途` |
| `concepts/vocabulary-mapping.md` | 权威来源 | 同名新节 |
| `concepts/vocabulary-hierarchy.md` | 定义 | 同名新节 |
| `concepts/vocabulary-hierarchy.md` | 一个概念下面怎么分 | `层级类型` |
| `concepts/vocabulary-hierarchy.md` | 每个划分特征分出一组兄弟 | `划分特征` 与 `数组` |
| `concepts/vocabulary-hierarchy.md` | 组前面写上按什么分 | `节点标签` |
| `concepts/vocabulary-hierarchy.md` | 一个概念可以同时在几个组里 | `多层级`，并区分展示分组 |
| `concepts/vocabulary-hierarchy.md` | 在知识库中 | `本库用途` |
| `concepts/vocabulary-hierarchy.md` | 权威来源 | 同名新节 |
| `concepts/metadata.md` | 定义、解决的问题 | 同名新节 |
| `concepts/metadata.md` | Dublin Core 的十五个核心元素 | `核心元素` |
| `concepts/metadata.md` | DCMI Metadata Terms | `术语体系` |
| `concepts/metadata.md` | 与受控词表的关系 | `词表关系` |
| `concepts/metadata.md` | 在知识库中 | `本库用途` |
| `concepts/metadata.md` | 权威来源 | 同名新节 |
| `concepts/classifying-new-subjects.md` | 定义、解决的问题 | 同名新节 |
| `concepts/classifying-new-subjects.md` | 分析综合 | `分析综合` |
| `concepts/classifying-new-subjects.md` | 文献依据 | `依据类型` |
| `concepts/classifying-new-subjects.md` | 实用主义 | `概念判定` 与 `适用边界` |
| `concepts/classifying-new-subjects.md` | 剩余监控 | 同名新节 |
| `concepts/classifying-new-subjects.md` | 在知识库中 | `本库用途`；项目字段推论删除 |
| `concepts/classifying-new-subjects.md` | 权威来源 | 同名新节 |
| `concepts/body-of-knowledge.md` | 定义、解决的问题 | 同名新节 |
| `concepts/body-of-knowledge.md` | 结构 | `组成` |
| `concepts/body-of-knowledge.md` | 常见的知识体系 | `常见实例` |
| `concepts/body-of-knowledge.md` | 与受控词表的关系 | `词表关系` |
| `concepts/body-of-knowledge.md` | 在知识库中的用法 | `使用角色` 与 `本库用途`；本地参数删除 |
| `concepts/body-of-knowledge.md` | 权威来源 | 同名新节 |
| `concepts/governance.md` | 定义、解决的问题 | 同名新节 |
| `concepts/governance.md` | 治理与维护的分层 | `治理层次` 与 `维护边界` |
| `concepts/governance.md` | 单人加 AI 的治理 | `执行角色` |
| `concepts/governance.md` | 在知识库中的用法 | `本库用途` |
| `concepts/governance.md` | 权威来源 | 同名新节 |
| `concepts/README.md` | 文章的关系 | 同名新节 |
| `concepts/README.md` | 词表结构总览 | 同名新节，全部示意重画 |
| `concepts/README.md` | 阅读顺序 | 同名新节 |

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
- [ ] 运行 `git rev-parse HEAD > /tmp/kb-terminology-foundation-base.sha`，再运行 `test -s /tmp/kb-terminology-foundation-base.sha`；预期退出码为 0。后续所有范围校验使用这个固定基线。
- [ ] 运行 `python3 scripts/check-links.py`；预期输出“全部链接有效”。
- [ ] 运行 `python3 scripts/check-topics.py`；保存概念、数组、实体、来源、候选和 `self` 的基线输出，不修改数据。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-before.txt`，再读第一行和全部涉及待重写文件的行；保存基线，明确该脚本当前只报告、不扫描术语表本身。
- [ ] 运行 `rg -n '^#{1,4} ' sources/iso-25964.md sources/z39-19.md sources/iso-15489.md concepts/glossary.md concepts/controlled-vocabulary.md concepts/vocabulary-construction.md concepts/vocabulary-mapping.md concepts/vocabulary-hierarchy.md concepts/metadata.md concepts/classifying-new-subjects.md concepts/body-of-knowledge.md concepts/governance.md concepts/README.md`；逐项与“小节去向”核对。
- [ ] 向人提交精确 L2 提案：新建两份来源笔记和一份概念文，整篇重写 ISO 25964、Z39.19 两份来源笔记、八份概念文与概念索引，整节重写 ISO 15489 的“适用边界”和术语表“基本单位”；明确不改 `design/`、`vocab/`、`scripts/`。
- [ ] 等待人明确批准该文件清单和小节清单；未批准时停止，不创建文件。

### 术语来源

**Files:**

- Create: `sources/terminology-standards.md`

**Interfaces:**

- Consumes: ISO 704、ISO 1087、GB/T 15237、ISO 10241-1、GB/T 20001.1、ISO 26162-1、ISO 26162-3、ISO 30042、GB/T 44227、TBX-Basic 的官方页面。
- Produces: 可供术语表和术语数据库概念文引用的阅读边界。

**Steps:**

- [ ] 运行 `test ! -e sources/terminology-standards.md`；预期退出码为 0。
- [ ] 打开 ISO 704、ISO 1087 与 GB/T 15237 官方页面，记录编号、版次、状态、采标页面能确认的范围和核对日期。
- [ ] 打开 ISO 10241-1 与 GB/T 20001.1 官方页面，记录同样信息；不从采标关系推断术语逐条等同。
- [ ] 打开 ISO 26162-1 与 ISO 26162-3 官方页面，分别记录数据库设计和内容维护的公开范围。
- [ ] 打开 ISO 30042、GB/T 44227 与 TBX-Basic 官方页面，分别记录交换标准、采标关系和公开数据类目。
- [ ] 对每项材料分别标明“公开页面已读”“可访问正文已读”“付费或未取得正文”，不把摘要扩写成条款。
- [ ] 新建标题 `# 术语标准`，并建立 `阅读范围`、`基础术语`、`条目结构`、`数据库`、`交换边界`、`版本状态`、`未读范围` 七个小节。
- [ ] 重写“阅读范围”；逐项写已读页面、正文与未取得正文。
- [ ] 重写“基础术语”；中文只使用实际读到的 GB/T 术语条目，没有条目时不反译。
- [ ] 重写“条目结构”；限制在 ISO 10241-1 官方材料实际支持的范围。
- [ ] 重写“数据库”；限制在 ISO 26162 官方材料实际支持的范围。
- [ ] 重写“交换边界”；记录 ISO 30042 的公开范围和 TBX-Basic 页面列出的层次与数据类目，明确它们不规定本库内部 YAML。
- [ ] 重写“版本状态”；现行标准与修订项目分开，不推测后继文本。
- [ ] 重写“未读范围”；逐项列出不能据以作答的内容。
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

- [ ] 运行 `test ! -e sources/metadata-standards.md`；预期退出码为 0。
- [ ] 打开 [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) 与 [PROV-O](https://www.w3.org/TR/prov-o/)，记录版本、状态、实际阅读位置和核对日期。
- [ ] 打开 [SKOS Reference](https://www.w3.org/TR/skos-reference/) 与 [BCP 47](https://www.rfc-editor.org/info/bcp47/)，记录版本、状态、实际阅读位置和核对日期。
- [ ] 新建标题 `# 元数据标准`，并建立 `阅读范围`、`元数据来源`、`派生关系`、`概念映射`、`语言标签`、`适用边界`、`未读范围` 七个小节。
- [ ] 重写“阅读范围”；逐项记录四份规范实际读到的位置。
- [ ] 重写“元数据来源”；只说明 DCMI `source` 的定义域和值域，不把它扩写成本地逐值证据规则。
- [ ] 重写“派生关系”；分别记录 PROV-O 的 derivation、revision、primary source 和 invalidation，不把日常“来自”自动映射为这些关系。
- [ ] 重写“概念映射”；记录 SKOS 映射关系的概念边界。
- [ ] 重写“语言标签”；记录 RFC 5646 用途，不自行规定本库字段形状。
- [ ] 重写“适用边界”；逐项指出外部词汇不能替项目决定什么。
- [ ] 重写“未读范围”；只列实际没有核对的内容。
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

- [ ] 运行 `rg -n 'ISO 25964|Z39\.19|ISO 15489' concepts design > /tmp/kb-terminology-source-consumers.txt || true`；逐行标出本计划会重写的概念文和后续项目迁移消费者，任何未授权消费者都不得在本任务修改。
- [ ] 运行 `rg -n '可以无损落到 RDF' sources/iso-25964.md`；预期先命中旧过度断言，作为失败基线。
- [ ] 按“小节去向”逐行核对 `sources/iso-25964.md` 的十六项映射；预期每个现有标题恰有一个去向或删除理由。
- [ ] 为 ISO 25964 笔记建立 `材料身份`、`阅读范围`、`已核定义`、`关系模型`、`数据材料`、`修订状态`、`适用边界`、`未读范围` 八个小节。
- [ ] 重写“材料身份”；记录两个部分及公开材料的身份。
- [ ] 重写“阅读范围”；每项材料记录版次、来源、核对日期和可读范围。
- [ ] 重写“已核定义”；每条定义记录实际材料和位置，免费样本范围之外不引用编号。
- [ ] 重写“关系模型”；只保留已读材料支持的关系。
- [ ] 重写“数据材料”；删除“ISO 模型可无损映射 RDF”等没有材料直接支持的结论，SKOS 对应只保留公开材料能够确认的内容。
- [ ] 重写“修订状态”；现行版与后继项目分开，不推测后继文本。
- [ ] 重写“适用边界”；不得从来源事实直接推出项目规则。
- [ ] 重写“未读范围”；列出没有实际读取的条款。
- [ ] 运行 `rg -n '可以无损落到 RDF|后继版本将' sources/iso-25964.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 提交：`git add sources/iso-25964.md && git commit -m "[L1] 来源:重写 ISO 25964 阅读笔记"`。
- [ ] 按“小节去向”核对 `sources/z39-19.md` 的三项映射，再建立 `材料身份`、`阅读范围`、`已核条款`、`维护依据`、`修订状态`、`适用边界`、`未读范围` 七个小节。
- [ ] 重写 Z39.19 的“材料身份”。
- [ ] 重写 Z39.19 的“阅读范围”。
- [ ] 重写 Z39.19 的“已核条款”；每个条款号必须存在于已读正文。
- [ ] 重写 Z39.19 的“维护依据”；只保留正文实际支持的活动。
- [ ] 重写 Z39.19 的“修订状态”；只记录官方项目页可确认的状态。
- [ ] 重写 Z39.19 的“适用边界”。
- [ ] 重写 Z39.19 的“未读范围”。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 提交：`git add sources/z39-19.md && git commit -m "[L1] 来源:重写 Z39.19 阅读笔记"`。
- [ ] 运行 `rg -n '内容单元不删|一律不删|origin' sources/iso-15489.md`；预期先命中旧项目结论，作为失败基线。
- [ ] 将 `sources/iso-15489.md` 的“对本库的检验”整节重写为“适用边界”；只解释已读正文中的 record 与 disposition，不给项目作保留决定，也不再引用旧 `origin`。
- [ ] 运行 `rg -n 'origin|本库.*不删' sources/iso-15489.md`；预期无匹配。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 提交：`git add sources/iso-15489.md && git commit -m "[L1] 来源:重写 ISO 15489 适用边界"`。

### 术语审查

**Files:**

- Read: `concepts/glossary.md`
- Modify: none

**Interfaces:**

- Consumes: 三份新旧来源笔记以及每行术语能够重复定位的官方材料。
- Produces: 全表逐行审查结果，以及“基本单位”整节可安全准入的术语清单；审查过程只留在执行会话，不改变正式文件。

**Temporary extractor:** 把下列固定脚本保存为 `/tmp/kb-extract-glossary-forms.py`。脚本读取 Git 已跟踪和未忽略的未跟踪文本文件，以不区分大小写的固定字符串查找消费者；术语表自身、`docs/superpowers/` 和二进制文件不计作项目消费者。脚本只生成临时审查表，不修改仓库文件。

```python
from pathlib import Path
import re
import subprocess
import sys

_PROJECT_TEXT_FILES = None

def forms(value, language):
    value = re.sub(r"[`*]", "", value).strip()
    if value in {"", "—"}:
        return []
    pattern = r"\s*/\s*|、" if language == "zh" else r"\s*/\s*|,\s*"
    return [item.strip() for item in re.split(pattern, value) if item.strip()]

def glossary_rows(source):
    section = ""
    rows = []
    for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] in {"术语", "缩写", "名称", "---"}:
            continue
        if len(cells) == 2:
            form = re.sub(r"[`*]", "", cells[0]).strip()
            if form:
                rows.append((form, "und", section or "出处缩写", str(line_number)))
            continue
        if len(cells) != 4:
            continue
        for language, value in (("zh", cells[0]), ("en", cells[1])):
            for form in forms(value, language):
                rows.append((form, language, section, str(line_number)))
    rows.sort(key=lambda row: (row[2], row[1], row[0], int(row[3])))
    return rows

def project_text_files():
    global _PROJECT_TEXT_FILES
    if _PROJECT_TEXT_FILES is not None:
        return _PROJECT_TEXT_FILES
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        check=True,
        capture_output=True,
    )
    files = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        name = raw_path.decode("utf-8")
        if name == "concepts/glossary.md" or name.startswith("docs/superpowers/"):
            continue
        path = Path(name)
        if not path.is_file():
            continue
        data = path.read_bytes()
        if b"\0" in data:
            continue
        try:
            lines = data.decode("utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        files.append((name, lines))
    _PROJECT_TEXT_FILES = files
    return files

def consumer_locations(form):
    needle = form.casefold()
    locations = []
    for name, lines in project_text_files():
        for line_number, line in enumerate(lines, 1):
            if needle in line.casefold():
                locations.append(f"{name}:{line_number}")
    return ";".join(locations) or "无引用"

def write_forms(rows, target):
    forms_text = "形式\t语言\t小节\t原行\n" + "\n".join("\t".join(row) for row in rows) + "\n"
    target.write_text(forms_text, encoding="utf-8")

def extract(source, forms_target, consumers_target):
    rows = glossary_rows(source)
    write_forms(rows, forms_target)
    consumer_rows = [row + (consumer_locations(row[0]),) for row in rows]
    consumers_text = "形式\t语言\t小节\t原行\t全库引用\n" + "\n".join("\t".join(row) for row in consumer_rows) + "\n"
    consumers_target.write_text(consumers_text, encoding="utf-8")

def extract_forms(source, target):
    write_forms(glossary_rows(source), target)

def audit_consumers(review, target):
    rows = []
    for line_number, line in enumerate(review.read_text(encoding="utf-8").splitlines(), 1):
        if line_number == 1:
            continue
        cells = line.split("\t")
        if len(cells) != 10:
            raise SystemExit(f"review row {line_number} does not have 10 columns")
        rows.append(tuple(cells[:4]) + (consumer_locations(cells[0]),))
    rows.sort()
    text = "形式\t语言\t小节\t原行\t全库引用\n" + "\n".join("\t".join(row) for row in rows) + "\n"
    target.write_text(text, encoding="utf-8")

def refresh_consumers(review, target):
    lines = review.read_text(encoding="utf-8").splitlines()
    output = [lines[0]]
    for line_number, line in enumerate(lines[1:], 2):
        cells = line.split("\t")
        if len(cells) != 10:
            raise SystemExit(f"review row {line_number} does not have 10 columns")
        cells[7] = consumer_locations(cells[0])
        output.append("\t".join(cells))
    target.write_text("\n".join(output) + "\n", encoding="utf-8")

def guard_removals(review):
    violations = []
    for line_number, line in enumerate(review.read_text(encoding="utf-8").splitlines(), 1):
        if line_number == 1:
            continue
        cells = line.split("\t")
        if len(cells) != 10:
            raise SystemExit(f"review row {line_number} does not have 10 columns")
        if cells[8] == "remove" and cells[7] != "无引用":
            violations.append(f"{cells[0]}: {cells[7]}")
    if violations:
        raise SystemExit("removed forms still have consumers:\n" + "\n".join(violations))

if sys.argv[1] == "extract" and len(sys.argv) == 5:
    extract(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
elif sys.argv[1] == "extract-forms" and len(sys.argv) == 4:
    extract_forms(Path(sys.argv[2]), Path(sys.argv[3]))
elif sys.argv[1] == "audit-consumers" and len(sys.argv) == 4:
    audit_consumers(Path(sys.argv[2]), Path(sys.argv[3]))
elif sys.argv[1] == "refresh-consumers" and len(sys.argv) == 4:
    refresh_consumers(Path(sys.argv[2]), Path(sys.argv[3]))
elif sys.argv[1] == "guard-removals" and len(sys.argv) == 3:
    guard_removals(Path(sys.argv[2]))
else:
    raise SystemExit(
        "usage: extract SOURCE FORMS_TSV CONSUMERS_TSV | "
        "extract-forms SOURCE FORMS_TSV | "
        "audit-consumers REVIEW_TSV CONSUMERS_TSV | "
        "refresh-consumers REVIEW_TSV REFRESHED_TSV | "
        "guard-removals REVIEW_TSV"
    )
```

**Steps:**

- [ ] 保存临时提取器后运行 `python3 /tmp/kb-extract-glossary-forms.py extract concepts/glossary.md /tmp/kb-terminology-glossary-forms-before.tsv /tmp/kb-terminology-glossary-consumers-before.tsv`；预期退出码为 0 且两个输出文件非空。
- [ ] 运行 `test "$(tail -n +2 /tmp/kb-terminology-glossary-forms-before.tsv | wc -l | tr -d ' ')" = 348` 与 `test "$(tail -n +2 /tmp/kb-terminology-glossary-consumers-before.tsv | wc -l | tr -d ' ')" = 348`；预期均通过，固定本计划起点的完整形式数。
- [ ] 运行 `awk '/^## 基本单位$/{skip=1; next} /^## /{skip=0} !skip{print}' concepts/glossary.md > /tmp/kb-terminology-glossary-nonbasic-before.md`；保存术语表中本计划无权修改的全部内容。
- [ ] 运行 `awk -F'|' 'NF == 6 {s=$5; gsub(/^ +| +$/, "", s); if (s == "" || s == "—" || s == "自定" || s ~ /^本库/) print NR ":" $0}' concepts/glossary.md`，再运行 `rg -n '^\| 自定 \|' concepts/glossary.md`；预期命中当前问题，证明通用术语报告不能代替逐行来源审查。
- [ ] 运行基本单位来源检查 `awk -F'|' '/^## 基本单位$/{inside=1; next} /^## /{inside=0} inside && NF == 6 && $2 !~ /^(术语|---)$/ {source=$5; if (source !~ /\[[^]]+\]\([^)]*#[^)]+\)/) bad=1} END {exit bad ? 1 : 0}' concepts/glossary.md`；预期退出码为 1，证明现状缺少带标题、带锚点的可重复定位来源。
- [ ] 运行 `awk -F'\t' 'BEGIN{OFS="\t"} NR == 1 {print $1,$2,$3,$4,"依据结论","依据位置","概念对应",$5,"动作","处理阶段"; next} {print $1,$2,$3,$4,"","","",$5,"",""}' /tmp/kb-terminology-glossary-consumers-before.tsv > /tmp/kb-terminology-glossary-review.tsv`；建立十列临时清单并自动带入所有现有形式和库内引用。
- [ ] 明确临时值域：依据结论只用 `有依据`、`无依据`、`有冲突`；概念对应只用 `同一概念`、`不同概念`、`未确定`、`不适用`；动作只用 `keep`、`add`、`remove`、`defer`；处理阶段只用 `基本单位`、`已核`、`术语迁移`。这些值只服务本次审查，不进入项目设计或正式术语记录。
- [ ] 有依据时，“依据位置”至少填写一个带标题和锚点的 Markdown 链接；无依据或有冲突时，以“检索记录：”开头，填写核对日期和实际检索过的带标题链接，不把“未找到”伪装成支持依据。
- [ ] 审查第 9–14 行的出处缩写并写入临时清单；缩写不得掩盖版次、条款或“自定”。
- [ ] 审查第 20–24 行并写入临时清单；只处理“词表的类型”前五个条目。
- [ ] 审查第 25–27 行并写入临时清单；完成“词表的类型”。
- [ ] 审查第 33–37 行并写入临时清单；只处理“基本单位”第一批。
- [ ] 审查第 38–42 行并写入临时清单；只处理“基本单位”第二批。
- [ ] 审查第 43–47 行并写入临时清单；完成“基本单位”。
- [ ] 审查第 53–57 行并写入临时清单；术语关系与概念关系分别判断。
- [ ] 审查第 58–62 行并写入临时清单；继续核对关系层次。
- [ ] 审查第 63–65 行并写入临时清单；完成“关系”。
- [ ] 审查第 71–75 行并写入临时清单；只处理“结构”第一批。
- [ ] 审查第 76–80 行并写入临时清单；只处理“结构”第二批。
- [ ] 审查第 81–85 行并写入临时清单；完成“结构”。
- [ ] 审查第 91–95 行并写入临时清单；外部活动不改写成本地状态。
- [ ] 审查第 96–100 行并写入临时清单；完成“注释与生命周期”。
- [ ] 审查第 106–110 行并写入临时清单；只处理“建设与治理”第一批。
- [ ] 审查第 111–115 行并写入临时清单；只处理“建设与治理”第二批。
- [ ] 审查第 116–121 行并写入临时清单；完成“建设与治理”。
- [ ] 审查第 127–131 行并写入临时清单；映射关系与材料身份分开。
- [ ] 审查第 132–136 行并写入临时清单；继续核对映射关系。
- [ ] 审查第 137–139 行并写入临时清单；完成“词表间映射”。
- [ ] 审查第 145–149 行并写入临时清单；完成“知识体系”。
- [ ] 审查第 155–159 行并写入临时清单；项目规则不得伪装成标准术语。
- [ ] 审查第 165–169 行并写入临时清单；只处理“写作与设计方法”第一批。
- [ ] 审查第 170–173 行并写入临时清单；完成“写作与设计方法”。
- [ ] 审查第 179–183 行并写入临时清单；只处理“笔记的类型”第一批。
- [ ] 审查第 184–186 行并写入临时清单；完成“笔记的类型”。
- [ ] 审查第 192–196 行并写入临时清单；本地角色名不作为外部术语批准依据。
- [ ] 审查第 197–201 行并写入临时清单；继续核对“治理与维护”。
- [ ] 审查第 202–204 行并写入临时清单；完成“治理与维护”。
- [ ] 审查第 209–213 行并写入临时清单；只处理“知识图谱”第一批。
- [ ] 审查第 214–218 行并写入临时清单；只处理“知识图谱”第二批。
- [ ] 审查第 219–220 行并写入临时清单；完成“知识图谱”。
- [ ] 审查第 226–230 行并写入临时清单；标准版次与 `sources/` 一致。
- [ ] 审查第 231–235 行并写入临时清单；未核材料不得继续支持术语。
- [ ] 审查第 236–239 行并写入临时清单；完成“引用的标准与文献”。
- [ ] 新增形式另加一行，“原行”写 `新增`，“全库引用”暂留空；全部新增行登记后，由临时提取器的 `refresh-consumers` 模式统一填入精确消费者值。
- [ ] 非“基本单位”小节的现有形式，有依据且中英概念对应明确时记为 `keep` 与“已核”；其余一律记为 `defer` 与“术语迁移”，本计划不修改对应行。
- [ ] “基本单位”的现有形式只有在形式保留、依据可定位且中英概念对应明确时才能记为 `keep`；没有消费者的无依据或冲突形式可提请 `remove`，新形式只有取得依据后才能提请 `add`。
- [ ] “基本单位”的 `remove` 形式只要在术语表外有消费者，就停止本计划并提交扩大消费者迁移范围的 L2 提案；不得留下无依据形式，也不得只改其余行形成半套小节。
- [ ] 只有新 `concepts/terminology-database.md` 必需、来源与中英对应均已核清、且不会删除活跃消费者写法的条目，处理阶段才能记为“基本单位”。
- [ ] 运行 `tail -n +2 /tmp/kb-terminology-glossary-forms-before.tsv | sort > /tmp/kb-terminology-glossary-before.keys`，再运行 `awk -F'\t' 'NR > 1 && $9 != "add" {print $1 "\t" $2 "\t" $3 "\t" $4}' /tmp/kb-terminology-glossary-review.tsv | sort > /tmp/kb-terminology-glossary-reviewed.keys` 和 `diff -u /tmp/kb-terminology-glossary-before.keys /tmp/kb-terminology-glossary-reviewed.keys`；预期无差异，证明没有漏审现有形式。
- [ ] 运行 `test -z "$(tail -n +2 /tmp/kb-terminology-glossary-review.tsv | cut -f1-4 | sort | uniq -d)"`；预期退出码为 0，证明审查行没有重复。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv`，再运行 `python3 /tmp/kb-extract-glossary-forms.py audit-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-consumers-reviewed.tsv`；消费者清单必须覆盖已跟踪和未忽略的未跟踪文本，二进制构建物不作为正文消费者。
- [ ] 运行 `tail -n +2 /tmp/kb-terminology-glossary-consumers-reviewed.tsv | sort > /tmp/kb-terminology-glossary-consumers-actual.keys`，再运行 `awk -F'\t' 'NR > 1 {print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $8}' /tmp/kb-terminology-glossary-review.tsv | sort > /tmp/kb-terminology-glossary-consumers-recorded.keys` 和 `diff -u /tmp/kb-terminology-glossary-consumers-actual.keys /tmp/kb-terminology-glossary-consumers-recorded.keys`；预期无差异，证明除术语表、Superpowers 文档和二进制构建物外，其余 Git 已跟踪及未忽略的未跟踪文本消费者没有漏记。
- [ ] 运行 `awk -F'\t' 'NR > 1 && (NF != 10 || $1 == "" || $2 == "" || $3 == "" || $4 == "" || $5 == "" || $6 == "" || $7 == "" || $8 == "" || $9 == "" || $10 == "") {bad=1} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0，证明十列均已填写。
- [ ] 运行 `awk -F'\t' 'NR > 1 && ($5 !~ /^(有依据|无依据|有冲突)$/ || $7 !~ /^(同一概念|不同概念|未确定|不适用)$/ || $9 !~ /^(keep|add|remove|defer)$/ || $10 !~ /^(基本单位|已核|术语迁移)$/) {bad=1} NR > 1 && $5 == "有依据" && $6 !~ /\[[^]]+\]\([^)]*#[^)]+\)/ {bad=1} NR > 1 && $5 != "有依据" && ($6 !~ /^检索记录：/ || $6 !~ /[0-9]{4}-[0-9]{2}-[0-9]{2}/ || $6 !~ /\[[^]]+\]\([^)]+\)/) {bad=1} NR > 1 && $2 == "und" && $7 != "不适用" {bad=1} NR > 1 && $2 != "und" && $7 == "不适用" {bad=1} NR > 1 && $9 == "add" && ($4 != "新增" || $5 != "有依据" || $7 != "同一概念") {bad=1} NR > 1 && $9 != "add" && $4 !~ /^[0-9]+$/ {bad=1} NR > 1 && $9 == "remove" && $8 != "无引用" {bad=1} NR > 1 && $3 == "基本单位" && ($10 != "基本单位" || $9 !~ /^(keep|add|remove)$/) {bad=1} NR > 1 && $3 != "基本单位" && !(($9 == "keep" && $10 == "已核") || ($9 == "defer" && $10 == "术语迁移")) {bad=1} NR > 1 && $10 == "已核" && ($5 != "有依据" || $7 !~ /^(同一概念|不适用)$/) {bad=1} NR > 1 && $10 == "基本单位" && $9 == "keep" && ($5 != "有依据" || $7 != "同一概念") {bad=1} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0；“基本单位”不得以 `defer` 绕过整节准入，其他小节不得使用 `add` 或 `remove`。
- [ ] 运行 `awk -F'\t' 'NR > 1 && $2 != "und" {key=$3 SUBSEP $4; if (key in seen && seen[key] != $7) bad=1; seen[key]=$7} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0，证明同一原行拆出的中英形式没有互相矛盾的概念对应结论。
- [ ] 将全表问题和“基本单位”准入清单交人复核；人只批准“基本单位”清单，不以此批准其余术语迁移。

### 数据库概念

**Files:**

- Create: `concepts/terminology-database.md`
- Modify: `concepts/glossary.md` 的“基本单位”整节

**Interfaces:**

- Consumes: ISO 704、ISO 1087、ISO 10241-1、ISO 26162、ISO 30042、TBX-Basic、BCP 47 的已核范围。
- Produces: 项目术语治理设计可引用的对象与层次，不产生字段方案。

**Steps:**

- [ ] 运行 `test ! -e concepts/terminology-database.md`；预期退出码为 0。
- [ ] 新建标题 `# 术语数据库 (Terminology Database)`，并建立 `定义`、`解决的问题`、`记录层次`、`多语对应`、`状态层次`、`维护要求`、`本库用途`、`权威来源` 八个小节。
- [ ] 重写“定义”；区分 terminological data collection、terminological entry、concept、designation 与 term，没有已核中文形式时保留英文。
- [ ] 重写“解决的问题”；只说明为何需要按概念、语言和术语分层。
- [ ] 重写“记录层次”；解释概念层、语言层、术语层为何分开，不给出 YAML 字段或基数。
- [ ] 重写“多语对应”；说明两种语言形式进入同一概念需要概念一致性证据，字符串相似和机器翻译不构成证据。
- [ ] 重写“状态层次”；区分术语管理状态与项目工作流，只引用 TBX-Basic 已核范围。
- [ ] 重写“维护要求”；只引用 ISO 26162-3 已核范围。
- [ ] 重写“本库用途”；明确 YAML、周期和生成规则属于后续本地决定。
- [ ] 重写“权威来源”；每项来源链接到实际阅读笔记或官方位置。
- [ ] 按获准“基本单位”清单整节重写 `concepts/glossary.md` 的“基本单位”；其他小节逐字保持，不处理活跃设计消费者。
- [ ] 运行 `awk '/^## 基本单位$/{skip=1; next} /^## /{skip=0} !skip{print}' concepts/glossary.md > /tmp/kb-terminology-glossary-nonbasic-after.md` 和 `diff -u /tmp/kb-terminology-glossary-nonbasic-before.md /tmp/kb-terminology-glossary-nonbasic-after.md`；预期无差异。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py extract-forms concepts/glossary.md /tmp/kb-terminology-glossary-forms-after.tsv`；预期退出码为 0。
- [ ] 运行 `awk -F'\t' 'NR > 1 && $9 ~ /^(keep|defer|add)$/ {print $1 "\t" $2 "\t" $3}' /tmp/kb-terminology-glossary-review.tsv | sort > /tmp/kb-terminology-glossary-expected-after.keys`，再运行 `tail -n +2 /tmp/kb-terminology-glossary-forms-after.tsv | cut -f1-3 | sort > /tmp/kb-terminology-glossary-actual-after.keys` 和 `diff -u /tmp/kb-terminology-glossary-expected-after.keys /tmp/kb-terminology-glossary-actual-after.keys`；预期无差异。
- [ ] 运行 `diff -u /tmp/kb-terminology-glossary-forms-before.tsv /tmp/kb-terminology-glossary-forms-after.tsv > /tmp/kb-terminology-glossary-forms.diff || true`；逐项确认差异只对应人批准的 `add` 或 `remove` 行。
- [ ] 运行 `awk -F'|' '/^## 基本单位$/{inside=1; next} /^## /{inside=0} inside && NF == 6 && $2 !~ /^(术语|---)$/ {source=$5; if (source !~ /\[[^]]+\]\([^)]*#[^)]+\)/) bad=1} END {exit bad ? 1 : 0}' concepts/glossary.md`；预期退出码为 0，证明每个保留行至少有一个带标题、带锚点的来源链接。
- [ ] 逐行人工确认“基本单位”每个来源单元格中的锚点确实落到支持该定义或形式的位置；中文与英文不是同一来源直接对应时，分别列出两项证据。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-database.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-before.txt /tmp/kb-terminology-foundation-terms-after-database.txt || true`；该命令只生成正文候选报告，不证明术语表正确。逐项复核差异，预期新概念文没有新增未登记候选。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `git add concepts/terminology-database.md concepts/glossary.md`；只暂存本任务的两个文件。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv`，再运行 `python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0，证明新建但尚未提交的概念文没有重新引用待移除形式。
- [ ] 提交：`git commit -m "[L2] 概念:新增术语数据库依据"`。

### 词表概念

**Files:**

- Modify: `concepts/controlled-vocabulary.md`
- Modify: `concepts/vocabulary-construction.md`

**Interfaces:**

- Consumes: 术语表、ISO 25964 与 Z39.19 已核笔记、术语数据库概念文。
- Produces: 清楚区分概念、术语、词表关系、建设依据和维护活动的两篇概念文。

**Steps:**

- [ ] 按“小节去向”逐项核对 `concepts/controlled-vocabulary.md`；预期全部旧标题和旧例子有确切处置。
- [ ] 按“小节去向”逐项核对 `concepts/vocabulary-construction.md`；预期全部旧标题和旧例子有确切处置。
- [ ] 运行 `rg -n '词与词的三种关系|PostgreSQL|词从哪来:|候选词与层级补位' concepts/controlled-vocabulary.md concepts/vocabulary-construction.md`；预期先命中旧标题或旧例，作为失败基线。
- [ ] 为受控词表文建立 `定义`、`解决的问题`、`结构形态`、`术语关系`、`概念关系`、`标签表示`、`本库用途`、`权威来源` 八个小节。
- [ ] 重写受控词表的“定义”。
- [ ] 重写受控词表的“解决的问题”。
- [ ] 重写受控词表的“结构形态”。
- [ ] 重写“术语关系”；只处理同一概念的语言形式。
- [ ] 重写“概念关系”；只处理层级与相关关系。
- [ ] 重写“标签表示”；SKOS 跨体系映射只链接映射文。
- [ ] 重写“本库用途”；个体实例不进入主题概念层级。
- [ ] 重写“权威来源”；只列正文实际使用的来源。
- [ ] 运行 `rg -n '^#{2,4} .*[:：]|权威性.*借|PostgreSQL' concepts/controlled-vocabulary.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-controlled.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-database.txt /tmp/kb-terminology-foundation-terms-after-controlled.txt || true`；逐项复核该文新增候选。
- [ ] 运行 `git add concepts/controlled-vocabulary.md`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 提交：`git commit -m "[L2] 概念:重写受控词表边界"`。
- [ ] 为建设文建立 `定义`、`依据类型`、`候选发现`、`建设方法`、`条目内容`、`维护活动`、`本库用途`、`权威来源` 八个小节。
- [ ] 重写建设文的“定义”。
- [ ] 重写“依据类型”；三种 warrant 不等同支持具体值的 `basis`。
- [ ] 重写“候选发现”；不把主题概念、未标引概念和术语候选混成一种状态。
- [ ] 重写“建设方法”。
- [ ] 重写“条目内容”。
- [ ] 重写“维护活动”。
- [ ] 重写“本库用途”；项目字段与状态只指向后续设计。
- [ ] 重写“权威来源”。
- [ ] 运行 `rg -n '^#{2,4} .*[:：]|候选词.*unassigned' concepts/vocabulary-construction.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-construction.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-controlled.txt /tmp/kb-terminology-foundation-terms-after-construction.txt || true`；逐项复核该文新增候选。
- [ ] 运行 `git add concepts/vocabulary-construction.md`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 提交：`git commit -m "[L2] 概念:重写词表建设依据"`。

### 映射概念

**Files:**

- Modify: `concepts/vocabulary-mapping.md`
- Modify: `concepts/metadata.md`

**Interfaces:**

- Consumes: SKOS、DCMI、PROV-O 来源笔记与重写后的受控词表概念。
- Produces: `basis`、派生来源和概念映射可在项目设计中分开的概念边界。

**Steps:**

- [ ] 按“小节去向”逐项核对 `concepts/vocabulary-mapping.md`；预期全部旧标题有确切处置。
- [ ] 按“小节去向”逐项核对 `concepts/metadata.md`；预期全部旧标题有确切处置。
- [ ] 运行 `rg -n '权威性.*借|拿不准时.*closeMatch|映射总是有' concepts/vocabulary-mapping.md`；预期先命中旧结论，作为失败基线。
- [ ] 为映射文建立 `定义`、`解决的问题`、`关系类型`、`映射模型`、`证据要求`、`互操作边界`、`本库用途`、`权威来源` 八个小节。
- [ ] 重写映射文的“定义”；mapping relation 连接概念，不连接字符串。
- [ ] 重写映射文的“解决的问题”。
- [ ] 重写“关系类型”；分别说明五种 SKOS 映射关系。
- [ ] 重写“映射模型”。
- [ ] 重写“证据要求”；每种关系比较定义和范围，拿不准不自动选择 `closeMatch`。
- [ ] 重写“互操作边界”。
- [ ] 重写“本库用途”；映射不替本地标签、层级、归属和批准提供依据。
- [ ] 重写“权威来源”。
- [ ] 运行 `rg -n '权威性借过来|拿不准时用.*closeMatch|映射总是有' concepts/vocabulary-mapping.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-mapping.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-construction.txt /tmp/kb-terminology-foundation-terms-after-mapping.txt || true`；逐项复核该文新增候选。
- [ ] 运行 `git add concepts/vocabulary-mapping.md`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 提交：`git commit -m "[L2] 概念:重写词表映射边界"`。
- [ ] 为元数据文建立 `定义`、`解决的问题`、`核心元素`、`术语体系`、`来源属性`、`派生关系`、`词表关系`、`本库用途`、`权威来源` 九个小节。
- [ ] 重写元数据文的“定义”。
- [ ] 重写元数据文的“解决的问题”。
- [ ] 重写“核心元素”。
- [ ] 重写“术语体系”。
- [ ] 重写“来源属性”；解释 DCMI `source`。
- [ ] 重写“派生关系”；解释 PROV-O derivation。
- [ ] 重写“词表关系”。
- [ ] 重写“本库用途”；本地 `basis` 只作为后续设计问题，不伪装成 DCMI 或 PROV 要求。
- [ ] 重写“权威来源”。
- [ ] 人工逐节确认字符串、DCMI `source`、PROV-O derivation 和本地 `basis` 没有被写成同一种关系。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。再运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-metadata.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-mapping.txt /tmp/kb-terminology-foundation-terms-after-metadata.txt || true`；逐项复核该文新增候选。
- [ ] 运行 `git add concepts/metadata.md`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 提交：`git commit -m "[L2] 概念:重写元数据来源边界"`。

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

- [ ] 按“小节去向”逐项核对 `concepts/vocabulary-hierarchy.md`；预期全部旧标题有确切处置。
- [ ] 按“小节去向”逐项核对 `concepts/classifying-new-subjects.md`；预期项目字段全部移出。
- [ ] 按“小节去向”逐项核对 `concepts/body-of-knowledge.md`；预期项目参数全部移出。
- [ ] 按“小节去向”逐项核对 `concepts/governance.md`；预期具体权限全部移出。
- [ ] 运行 `rg -n '张三|只借.*层|origin|单人加 AI' concepts/vocabulary-hierarchy.md concepts/classifying-new-subjects.md concepts/body-of-knowledge.md concepts/governance.md`；预期先命中旧例、旧参数或旧混用，作为失败基线。
- [ ] 为层级文建立 `定义`、`层级类型`、`划分特征`、`数组`、`节点标签`、`多层级`、`适用边界`、`本库用途`、`权威来源` 九个小节。
- [ ] 重写层级文的“定义”。
- [ ] 重写“层级类型”；例子只使用概念。
- [ ] 重写“划分特征”。
- [ ] 重写“数组”。
- [ ] 重写“节点标签”。
- [ ] 重写“多层级”；分别解释多个上位与多个展示分组。
- [ ] 重写“适用边界”。
- [ ] 重写“本库用途”；不写项目数组字段或数量。
- [ ] 重写“权威来源”。
- [ ] 运行 `rg -n '张三' concepts/vocabulary-hierarchy.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-hierarchy.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-metadata.txt /tmp/kb-terminology-foundation-terms-after-hierarchy.txt || true`；逐项复核该文新增候选。
- [ ] 运行 `git add concepts/vocabulary-hierarchy.md`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 提交：`git commit -m "[L2] 概念:重写词表层级边界"`。
- [ ] 为新主题分类文建立 `定义`、`解决的问题`、`分析综合`、`依据类型`、`概念判定`、`剩余监控`、`适用边界`、`本库用途`、`权威来源` 九个小节。
- [ ] 重写新主题分类文的“定义”。
- [ ] 重写“解决的问题”。
- [ ] 重写“分析综合”。
- [ ] 重写“依据类型”。
- [ ] 重写“概念判定”；只解释一般概念判定，不出现项目字段。
- [ ] 重写“剩余监控”。
- [ ] 重写“适用边界”；一般性区分候选发现、逐项证据与实际派生，不出现项目字段。
- [ ] 重写“本库用途”；具体迁移交项目设计。
- [ ] 重写“权威来源”。
- [ ] 运行 `rg -n 'origin' concepts/classifying-new-subjects.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-classifying.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-hierarchy.txt /tmp/kb-terminology-foundation-terms-after-classifying.txt || true`；逐项复核该文新增候选。
- [ ] 运行 `git add concepts/classifying-new-subjects.md`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 提交：`git commit -m "[L2] 概念:重写新主题分类依据"`。
- [ ] 为知识体系文建立 `定义`、`解决的问题`、`组成`、`常见实例`、`词表关系`、`使用角色`、`适用边界`、`本库用途`、`权威来源` 九个小节。
- [ ] 重写知识体系文的“定义”。
- [ ] 重写“解决的问题”。
- [ ] 重写“组成”。
- [ ] 重写“常见实例”。
- [ ] 重写“词表关系”；不把 BOK、分类表和 taxonomy 当同义词。
- [ ] 重写“使用角色”；材料身份与映射、结构、分组、发现用途分开。
- [ ] 重写“适用边界”；删除“只借上两层”等项目参数。
- [ ] 重写“本库用途”；项目角色值只留给设计草案。
- [ ] 重写“权威来源”。
- [ ] 运行 `rg -n '只借.*层' concepts/body-of-knowledge.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-bok.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-classifying.txt /tmp/kb-terminology-foundation-terms-after-bok.txt || true`；逐项复核该文新增候选。
- [ ] 运行 `git add concepts/body-of-knowledge.md`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 提交：`git commit -m "[L2] 概念:重写知识体系边界"`。
- [ ] 为治理文建立 `定义`、`解决的问题`、`治理层次`、`证据边界`、`批准边界`、`维护边界`、`执行角色`、`本库用途`、`权威来源` 九个小节。
- [ ] 重写治理文的“定义”。
- [ ] 重写“解决的问题”。
- [ ] 重写“治理层次”。
- [ ] 重写“证据边界”；外部依据不等于项目批准。
- [ ] 重写“批准边界”；项目批准不代替外部依据。
- [ ] 重写“维护边界”；复核义务不代替前两者。
- [ ] 重写“执行角色”；具体权限不写进概念文。
- [ ] 重写“本库用途”。
- [ ] 重写“权威来源”。
- [ ] 运行 `rg -n '单人加 AI' concepts/governance.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-governance.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-bok.txt /tmp/kb-terminology-foundation-terms-after-governance.txt || true`；逐项复核该文新增候选。
- [ ] 运行 `git add concepts/governance.md`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 提交：`git commit -m "[L2] 概念:重写治理概念边界"`。

### 概念索引

**Files:**

- Modify: `concepts/README.md`

**Interfaces:**

- Consumes: 本计划完成后的全部概念文。
- Produces: 与真实引用方向一致的概念索引。

**Steps:**

- [ ] 按“小节去向”核对旧索引的“文章的关系”“词表结构总览”“阅读顺序”，再建立完整的新标题骨架。
- [ ] 重写“文章的关系”；把术语数据库置于术语与词表概念之前，把元数据、映射、层级和治理按引用方向连接。
- [ ] 重写“词表结构总览”；示意只使用概念实例，不使用具体个人，不把复制、映射和派生组说成同一关系。
- [ ] 重写“阅读顺序”；顺序按真实依赖排列，表中只回答每篇文章的概念问题。
- [ ] 检查索引中的每个链接与文章标题一致。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `git add concepts/README.md`。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv && python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 提交：`git commit -m "[L2] 概念:重写概念文索引"`。

### 最终校验

**Files:**

- Verify: 本计划“文件职责”列出的全部文件
- Modify: only files that fail a listed acceptance check, by rewriting the affected whole section

**Interfaces:**

- Consumes: 全部任务提交。
- Produces: 可交付给项目治理草案计划的稳定依据层。

**Steps:**

- [ ] 确认执行记录明确写着“程序分支不可合并”，直到项目草案、数据迁移和现行设计同步完成；不得在本计划后调用分支收尾技能。
- [ ] 使用 `superpowers:requesting-code-review` 审查来源可定位性、术语准入、概念示例、目录职责和旧文去向。
- [ ] 逐项处理审查反馈；每次涉及内容的修正按整节或整篇规则完成并提交，反馈全部关闭后再继续。无修改时不创建空提交。
- [ ] 从下一项开始执行最终验收；任何一项失败时，重写受影响的完整小节或文章，运行对应任务校验并提交，再重新请求审查，随后从本项重新执行全部最终验收。
- [ ] 按“旧文去向”逐行核销；每项必须标为“保留重写”“移入指定文档”或“删除并有理由”，不得留下无去向事项。
- [ ] 运行 `rg -n '^#{2,6} .*[:：]|^#{2,6} [0-9一二三四五六七八九十]' sources/terminology-standards.md sources/metadata-standards.md sources/iso-25964.md sources/z39-19.md sources/iso-15489.md concepts/glossary.md concepts/terminology-database.md concepts/controlled-vocabulary.md concepts/vocabulary-construction.md concepts/vocabulary-mapping.md concepts/vocabulary-hierarchy.md concepts/metadata.md concepts/classifying-new-subjects.md concepts/body-of-knowledge.md concepts/governance.md concepts/README.md`；预期无匹配。
- [ ] 人工核对每个小节标题是 2–8 字名词短语，且不含字段、文件名、数量或实现参数。
- [ ] 运行 `for entry in 'sources/terminology-standards.md|# 术语标准' 'sources/metadata-standards.md|# 元数据标准' 'sources/iso-25964.md|# ISO 25964 叙词表标准' 'sources/z39-19.md|# ANSI/NISO Z39.19 受控词表指南' 'sources/iso-15489.md|# ISO 15489 文件管理标准' 'concepts/glossary.md|# 术语表 (Glossary)' 'concepts/terminology-database.md|# 术语数据库 (Terminology Database)' 'concepts/README.md|# 概念文索引'; do file=${entry%%|*}; title=${entry#*|}; test "$(head -n 1 "$file")" = "$title" || exit 1; done`；预期退出码为 0。
- [ ] 运行 `for file in concepts/controlled-vocabulary.md concepts/vocabulary-construction.md concepts/vocabulary-mapping.md concepts/vocabulary-hierarchy.md concepts/metadata.md concepts/classifying-new-subjects.md concepts/body-of-knowledge.md concepts/governance.md; do head -n 1 "$file" | rg -q '^# [^()]+ \([^()]+\)$' || exit 1; done`；预期退出码为 0。再逐篇核对中英文标题的术语形式与全表审查依据，不为保持旧标题而保留无依据译名。
- [ ] 按 `concepts/CONVENTIONS.md` 人工逐节核对：每个抽象概念至少一个本库场景例子，每条事实断言能在“权威来源”定位，链接文字是来源标题。
- [ ] 运行 `awk '/^## 基本单位$/{skip=1; next} /^## /{skip=0} !skip{print}' concepts/glossary.md > /tmp/kb-terminology-glossary-nonbasic-final.md` 和 `diff -u /tmp/kb-terminology-glossary-nonbasic-before.md /tmp/kb-terminology-glossary-nonbasic-final.md`；预期无差异。
- [ ] 运行 `awk -F'|' '/^## 基本单位$/{inside=1; next} /^## /{inside=0} inside && NF == 6 && $2 !~ /^(术语|---)$/ {source=$5; if (source !~ /\[[^]]+\]\([^)]*#[^)]+\)/) bad=1} END {exit bad ? 1 : 0}' concepts/glossary.md`；预期退出码为 0，并人工确认每个锚点支持该形式、定义和中英对应。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py refresh-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-review-refreshed.tsv && mv /tmp/kb-terminology-glossary-review-refreshed.tsv /tmp/kb-terminology-glossary-review.tsv`，再运行 `python3 /tmp/kb-extract-glossary-forms.py audit-consumers /tmp/kb-terminology-glossary-review.tsv /tmp/kb-terminology-glossary-consumers-reviewed.tsv`；消费者位置对应审查后的 `HEAD`。
- [ ] 运行 `tail -n +2 /tmp/kb-terminology-glossary-forms-before.tsv | sort > /tmp/kb-terminology-glossary-before.keys`，再运行 `awk -F'\t' 'NR > 1 && $9 != "add" {print $1 "\t" $2 "\t" $3 "\t" $4}' /tmp/kb-terminology-glossary-review.tsv | sort > /tmp/kb-terminology-glossary-reviewed.keys` 和 `diff -u /tmp/kb-terminology-glossary-before.keys /tmp/kb-terminology-glossary-reviewed.keys`；预期无差异。
- [ ] 运行 `test -z "$(tail -n +2 /tmp/kb-terminology-glossary-review.tsv | cut -f1-4 | sort | uniq -d)"`；预期退出码为 0。
- [ ] 运行 `tail -n +2 /tmp/kb-terminology-glossary-consumers-reviewed.tsv | sort > /tmp/kb-terminology-glossary-consumers-actual.keys`，再运行 `awk -F'\t' 'NR > 1 {print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $8}' /tmp/kb-terminology-glossary-review.tsv | sort > /tmp/kb-terminology-glossary-consumers-recorded.keys` 和 `diff -u /tmp/kb-terminology-glossary-consumers-actual.keys /tmp/kb-terminology-glossary-consumers-recorded.keys`；预期无差异。
- [ ] 运行 `awk -F'\t' 'NR > 1 && (NF != 10 || $1 == "" || $2 == "" || $3 == "" || $4 == "" || $5 == "" || $6 == "" || $7 == "" || $8 == "" || $9 == "" || $10 == "") {bad=1} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 运行 `awk -F'\t' 'NR > 1 && ($5 !~ /^(有依据|无依据|有冲突)$/ || $7 !~ /^(同一概念|不同概念|未确定|不适用)$/ || $9 !~ /^(keep|add|remove|defer)$/ || $10 !~ /^(基本单位|已核|术语迁移)$/) {bad=1} NR > 1 && $5 == "有依据" && $6 !~ /\[[^]]+\]\([^)]*#[^)]+\)/ {bad=1} NR > 1 && $5 != "有依据" && ($6 !~ /^检索记录：/ || $6 !~ /[0-9]{4}-[0-9]{2}-[0-9]{2}/ || $6 !~ /\[[^]]+\]\([^)]+\)/) {bad=1} NR > 1 && $2 == "und" && $7 != "不适用" {bad=1} NR > 1 && $2 != "und" && $7 == "不适用" {bad=1} NR > 1 && $9 == "add" && ($4 != "新增" || $5 != "有依据" || $7 != "同一概念") {bad=1} NR > 1 && $9 != "add" && $4 !~ /^[0-9]+$/ {bad=1} NR > 1 && $9 == "remove" && $8 != "无引用" {bad=1} NR > 1 && $3 == "基本单位" && ($10 != "基本单位" || $9 !~ /^(keep|add|remove)$/) {bad=1} NR > 1 && $3 != "基本单位" && !(($9 == "keep" && $10 == "已核") || ($9 == "defer" && $10 == "术语迁移")) {bad=1} NR > 1 && $10 == "已核" && ($5 != "有依据" || $7 !~ /^(同一概念|不适用)$/) {bad=1} NR > 1 && $10 == "基本单位" && $9 == "keep" && ($5 != "有依据" || $7 != "同一概念") {bad=1} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv`；预期退出码为 0。
- [ ] 运行 `awk -F'\t' 'NR > 1 && $2 != "und" {key=$3 SUBSEP $4; if (key in seen && seen[key] != $7) bad=1; seen[key]=$7} END {exit bad ? 1 : 0}' /tmp/kb-terminology-glossary-review.tsv` 与 `python3 /tmp/kb-extract-glossary-forms.py guard-removals /tmp/kb-terminology-glossary-review.tsv`；预期均通过。
- [ ] 运行 `python3 /tmp/kb-extract-glossary-forms.py extract-forms concepts/glossary.md /tmp/kb-terminology-glossary-forms-final.tsv`，再运行 `awk -F'\t' 'NR > 1 && $9 ~ /^(keep|defer|add)$/ {print $1 "\t" $2 "\t" $3}' /tmp/kb-terminology-glossary-review.tsv | sort > /tmp/kb-terminology-glossary-expected-final.keys`、`tail -n +2 /tmp/kb-terminology-glossary-forms-final.tsv | cut -f1-3 | sort > /tmp/kb-terminology-glossary-actual-final.keys` 和 `diff -u /tmp/kb-terminology-glossary-expected-final.keys /tmp/kb-terminology-glossary-actual-final.keys`；预期无差异。
- [ ] 运行 `python3 scripts/check-links.py`；预期输出“全部链接有效”。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-final.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-before.txt /tmp/kb-terminology-foundation-terms-final.txt || true`；逐项人工复核差异，预期本计划改动的概念文没有新增无依据术语，延期用语没有被写成已经批准。
- [ ] 运行 `python3 scripts/check-topics.py`；预期与基线同样通过，证明本计划未改词表数据。
- [ ] 运行 `git diff --check "$(cat /tmp/kb-terminology-foundation-base.sha)"..HEAD`；预期无错误，并覆盖审查修正后的全部提交。
- [ ] 运行 `test "$(git diff --name-only "$(cat /tmp/kb-terminology-foundation-base.sha)"..HEAD | sort)" = "$(printf '%s\n' concepts/README.md concepts/body-of-knowledge.md concepts/classifying-new-subjects.md concepts/controlled-vocabulary.md concepts/glossary.md concepts/governance.md concepts/metadata.md concepts/terminology-database.md concepts/vocabulary-construction.md concepts/vocabulary-hierarchy.md concepts/vocabulary-mapping.md sources/iso-15489.md sources/iso-25964.md sources/metadata-standards.md sources/terminology-standards.md sources/z39-19.md | sort)"`；预期退出码为 0，证明交付文件无遗漏且没有越界文件。
- [ ] 阅读 `git diff "$(cat /tmp/kb-terminology-foundation-base.sha)"..HEAD`，确认没有 `design/` 规则、YAML 字段、阈值、Obsidian 或 TBX 实现混入概念层。
- [ ] 运行 `git status --short`；预期无输出，证明审查修正和最终验收修正都已提交。

## 完成条件

- 两份新来源笔记清楚区分已读、未读、现行版与修订项目。
- ISO 25964、Z39.19 和 ISO 15489 笔记不再超出实际阅读范围。
- 术语表每一行都有审查结论和消费者清单；“基本单位”整节的保留条目都有可重复定位依据，其他小节的问题未被伪装成已解决并留给原子迁移。
- 新术语数据库概念文只讲外部概念，不预写项目 YAML。
- 八份概念文各守单一职责，`basis`、派生来源和概念映射不再混用。
- 旧节逐项有去向，标题、标点和链接检查通过；术语候选报告已逐项人工复核，没有被误称为完整术语校验。
- `design/`、`vocab/`、`scripts/` 保持不变。
- 当前程序分支明确不可合并；这不是对现行设计与数据已经完成迁移的声明。

## 后续入口

本计划完成并通过审查后，执行 [项目治理草案](2026-08-28-terminology-project-design.md)。项目草案获准前，不编写数据迁移、生成器、来源探测、首轮维护或草案生效计划。
