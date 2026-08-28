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
- [ ] 重写“阅读范围”和“基础术语”；中文只使用实际读到的 GB/T 术语条目，没有条目时不反译。
- [ ] 重写“条目结构”和“数据库”；分别限制在 ISO 10241-1 与 ISO 26162 官方材料实际支持的范围。
- [ ] 重写“交换边界”；记录 ISO 30042 的公开范围和 TBX-Basic 页面列出的层次与数据类目，明确它们不规定本库内部 YAML。
- [ ] 重写“版本状态”和“未读范围”；现行标准与修订项目分开，不推测后继文本。
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
- [ ] 重写“阅读范围”和“元数据来源”；只说明 DCMI `source` 的定义域和值域，不把它扩写成本地逐值证据规则。
- [ ] 重写“派生关系”；分别记录 PROV-O 的 derivation、revision、primary source 和 invalidation，不把日常“来自”自动映射为这些关系。
- [ ] 重写“概念映射”和“语言标签”；记录 SKOS 映射边界与 RFC 5646 用途，不自行规定本库字段形状。
- [ ] 重写“适用边界”和“未读范围”；逐项指出外部词汇不能替项目决定什么。
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
- [ ] 重写“材料身份”和“阅读范围”；每项材料记录版次、来源、核对日期和可读范围。
- [ ] 重写“已核定义”和“关系模型”；每条定义记录实际材料和位置，免费样本范围之外不引用编号。
- [ ] 重写“数据材料”；删除“ISO 模型可无损映射 RDF”等没有材料直接支持的结论，SKOS 对应只保留公开材料能够确认的内容。
- [ ] 重写“修订状态”；现行版与后继项目分开，不推测后继文本。
- [ ] 重写“适用边界”和“未读范围”；不得从未读正文推出项目规则。
- [ ] 运行 `rg -n '可以无损落到 RDF|后继版本将' sources/iso-25964.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 提交：`git add sources/iso-25964.md && git commit -m "[L1] 来源:重写 ISO 25964 阅读笔记"`。
- [ ] 按“小节去向”核对 `sources/z39-19.md` 的三项映射，再建立 `材料身份`、`阅读范围`、`已核条款`、`维护依据`、`修订状态`、`适用边界`、`未读范围` 七个小节。
- [ ] 重写 Z39.19 的“材料身份”“阅读范围”和“已核条款”；每个条款号必须存在于已读正文。
- [ ] 重写 Z39.19 的“维护依据”“修订状态”“适用边界”和“未读范围”；修订项目只记录官方项目页可确认的状态。
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

**Steps:**

- [ ] 运行 `awk -F'|' 'NF == 6 {s=$5; gsub(/^ +| +$/, "", s); if (s == "" || s == "—" || s == "自定" || s ~ /^本库/) print NR ":" $0}' concepts/glossary.md`，再运行 `rg -n '^\| 自定 \|' concepts/glossary.md`；预期命中当前问题，证明通用术语报告不能代替逐行来源审查。
- [ ] 在 `/tmp/kb-terminology-glossary-review.tsv` 建立“形式、语言、小节、依据位置、概念对应、全库引用、处理阶段”七列临时清单；一行只放一个语言中的一个形式，表格单元格中的 `/`、`、` 或英文逗号形式分别成行；该文件不加入仓库。
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
- [ ] 运行 `tail -n +2 /tmp/kb-terminology-glossary-review.tsv | while IFS=$'\t' read -r form language section locator correspondence consumers phase; do rg -n -F -- "$form" concepts design || true; done`；把每个形式的全部消费者写回对应临时行。
- [ ] 任何消费者位于活跃 `design/` 或本计划未列出的概念文时，将该形式的处理阶段记为“术语迁移”，本计划不得修改或删除对应术语表行。
- [ ] 只有新 `concepts/terminology-database.md` 必需、来源与中英对应均已核清、且不会删除活跃消费者写法的条目，处理阶段才能记为“基本单位”。
- [ ] 如果“基本单位”现有任一行无法取得依据且删除或改名会影响未授权消费者，停止本计划并提交扩大迁移范围的 L2 提案；不得只改其余行形成半套小节。
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
- [ ] 重写“定义”和“解决的问题”；区分 terminological data collection、terminological entry、concept、designation 与 term，没有已核中文形式时保留英文。
- [ ] 重写“记录层次”；解释概念层、语言层、术语层为何分开，不给出 YAML 字段或基数。
- [ ] 重写“多语对应”；说明两种语言形式进入同一概念需要概念一致性证据，字符串相似和机器翻译不构成证据。
- [ ] 重写“状态层次”和“维护要求”；区分术语管理状态与项目工作流，只引用 TBX-Basic 与 ISO 26162-3 已核范围。
- [ ] 重写“本库用途”和“权威来源”；明确 YAML、周期和生成规则属于后续本地决定。
- [ ] 按获准“基本单位”清单整节重写 `concepts/glossary.md` 的“基本单位”；其他小节逐字保持，不处理活跃设计消费者。
- [ ] 运行 `awk -F'|' '/^## 基本单位$/{inside=1; next} /^## /{inside=0} inside && NF == 6 {s=$5; gsub(/^ +| +$/, "", s); if (s == "" || s == "—" || s == "自定" || s ~ /^本库/) print NR ":" $0}' concepts/glossary.md`；预期无输出。
- [ ] 逐行人工确认“基本单位”每个来源单元格同时包含带标题链接和可重复定位位置；中文与英文不是同一来源直接对应时，分别列出两项证据。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-database.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-before.txt /tmp/kb-terminology-foundation-terms-after-database.txt || true`；该命令只生成正文候选报告，不证明术语表正确。逐项复核差异，预期新概念文没有新增未登记候选。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 提交：`git add concepts/terminology-database.md concepts/glossary.md && git commit -m "[L2] 概念:新增术语数据库依据"`。

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
- [ ] 重写受控词表的“定义”“解决的问题”和“结构形态”。
- [ ] 重写“术语关系”“概念关系”和“标签表示”；SKOS 跨体系映射只链接映射文。
- [ ] 重写“本库用途”和“权威来源”；个体实例不进入主题概念层级。
- [ ] 运行 `rg -n '^#{2,4} .*[:：]|权威性.*借|PostgreSQL' concepts/controlled-vocabulary.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-controlled.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-database.txt /tmp/kb-terminology-foundation-terms-after-controlled.txt || true`；逐项复核该文新增候选。
- [ ] 提交：`git add concepts/controlled-vocabulary.md && git commit -m "[L2] 概念:重写受控词表边界"`。
- [ ] 为建设文建立 `定义`、`依据类型`、`候选发现`、`建设方法`、`条目内容`、`维护活动`、`本库用途`、`权威来源` 八个小节。
- [ ] 重写建设文的“定义”“依据类型”和“候选发现”；三种 warrant 不等同支持具体值的 `basis`。
- [ ] 重写“建设方法”“条目内容”和“维护活动”；不把主题概念、未标引概念和术语候选混成一种状态。
- [ ] 重写“本库用途”和“权威来源”；项目字段与状态只指向后续设计。
- [ ] 运行 `rg -n '^#{2,4} .*[:：]|候选词.*unassigned' concepts/vocabulary-construction.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-construction.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-controlled.txt /tmp/kb-terminology-foundation-terms-after-construction.txt || true`；逐项复核该文新增候选。
- [ ] 提交：`git add concepts/vocabulary-construction.md && git commit -m "[L2] 概念:重写词表建设依据"`。

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
- [ ] 重写映射文的“定义”“解决的问题”和“关系类型”；mapping relation 连接概念，不连接字符串。
- [ ] 重写“映射模型”“证据要求”和“互操作边界”；每种关系比较定义和范围，拿不准不自动选择 `closeMatch`。
- [ ] 重写“本库用途”和“权威来源”；映射不替本地标签、层级、归属和批准提供依据。
- [ ] 运行 `rg -n '权威性借过来|拿不准时用.*closeMatch|映射总是有' concepts/vocabulary-mapping.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-mapping.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-construction.txt /tmp/kb-terminology-foundation-terms-after-mapping.txt || true`；逐项复核该文新增候选。
- [ ] 提交：`git add concepts/vocabulary-mapping.md && git commit -m "[L2] 概念:重写词表映射边界"`。
- [ ] 为元数据文建立 `定义`、`解决的问题`、`核心元素`、`术语体系`、`来源属性`、`派生关系`、`词表关系`、`本库用途`、`权威来源` 九个小节。
- [ ] 重写元数据文的“定义”“解决的问题”“核心元素”和“术语体系”。
- [ ] 重写“来源属性”“派生关系”和“词表关系”；分别解释 DCMI `source` 与 PROV-O derivation。
- [ ] 重写“本库用途”和“权威来源”；本地 `basis` 只作为后续设计问题，不伪装成 DCMI 或 PROV 要求。
- [ ] 人工逐节确认字符串、DCMI `source`、PROV-O derivation 和本地 `basis` 没有被写成同一种关系。
- [ ] 运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。再运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-metadata.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-mapping.txt /tmp/kb-terminology-foundation-terms-after-metadata.txt || true`；逐项复核该文新增候选。
- [ ] 提交：`git add concepts/metadata.md && git commit -m "[L2] 概念:重写元数据来源边界"`。

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
- [ ] 重写层级文的“定义”“层级类型”“划分特征”和“数组”；例子只使用概念。
- [ ] 重写“节点标签”“多层级”和“适用边界”；分别解释多个上位与多个展示分组。
- [ ] 重写“本库用途”和“权威来源”；不写项目数组字段或数量。
- [ ] 运行 `rg -n '张三' concepts/vocabulary-hierarchy.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-hierarchy.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-metadata.txt /tmp/kb-terminology-foundation-terms-after-hierarchy.txt || true`；逐项复核该文新增候选。
- [ ] 提交：`git add concepts/vocabulary-hierarchy.md && git commit -m "[L2] 概念:重写词表层级边界"`。
- [ ] 为新主题分类文建立 `定义`、`解决的问题`、`分析综合`、`依据类型`、`概念判定`、`剩余监控`、`适用边界`、`本库用途`、`权威来源` 九个小节。
- [ ] 重写新主题分类文的“定义”“解决的问题”“分析综合”和“依据类型”。
- [ ] 重写“概念判定”；只解释一般概念判定，不出现项目字段。
- [ ] 重写“剩余监控”和“适用边界”；一般性区分候选发现、逐项证据与实际派生，不出现项目字段。
- [ ] 重写“本库用途”和“权威来源”；具体迁移交项目设计。
- [ ] 运行 `rg -n 'origin' concepts/classifying-new-subjects.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-classifying.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-hierarchy.txt /tmp/kb-terminology-foundation-terms-after-classifying.txt || true`；逐项复核该文新增候选。
- [ ] 提交：`git add concepts/classifying-new-subjects.md && git commit -m "[L2] 概念:重写新主题分类依据"`。
- [ ] 为知识体系文建立 `定义`、`解决的问题`、`组成`、`常见实例`、`词表关系`、`使用角色`、`适用边界`、`本库用途`、`权威来源` 九个小节。
- [ ] 重写知识体系文的“定义”“解决的问题”“组成”和“常见实例”。
- [ ] 重写“词表关系”；不把 BOK、分类表和 taxonomy 当同义词。
- [ ] 重写“使用角色”和“适用边界”；材料身份与映射、结构、分组、发现用途分开，删除“只借上两层”等参数。
- [ ] 重写“本库用途”和“权威来源”；项目角色值只留给设计草案。
- [ ] 运行 `rg -n '只借.*层' concepts/body-of-knowledge.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-bok.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-classifying.txt /tmp/kb-terminology-foundation-terms-after-bok.txt || true`；逐项复核该文新增候选。
- [ ] 提交：`git add concepts/body-of-knowledge.md && git commit -m "[L2] 概念:重写知识体系边界"`。
- [ ] 为治理文建立 `定义`、`解决的问题`、`治理层次`、`证据边界`、`批准边界`、`维护边界`、`执行角色`、`本库用途`、`权威来源` 九个小节。
- [ ] 重写治理文的“定义”“解决的问题”和“治理层次”。
- [ ] 重写“证据边界”“批准边界”和“维护边界”；外部依据、项目批准和复核义务互不替代。
- [ ] 重写“执行角色”“本库用途”和“权威来源”；具体权限不写进概念文。
- [ ] 运行 `rg -n '单人加 AI' concepts/governance.md`；预期无匹配。再运行 `python3 scripts/check-links.py` 与 `git diff --check`；预期均通过。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-after-governance.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-after-bok.txt /tmp/kb-terminology-foundation-terms-after-governance.txt || true`；逐项复核该文新增候选。
- [ ] 提交：`git add concepts/governance.md && git commit -m "[L2] 概念:重写治理概念边界"`。

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
- [ ] 运行 `rg -n '^#{2,6} .*[:：]|^#{2,6} [0-9一二三四五六七八九十]' sources/terminology-standards.md sources/metadata-standards.md sources/iso-25964.md sources/z39-19.md sources/iso-15489.md concepts/glossary.md concepts/terminology-database.md concepts/controlled-vocabulary.md concepts/vocabulary-construction.md concepts/vocabulary-mapping.md concepts/vocabulary-hierarchy.md concepts/metadata.md concepts/classifying-new-subjects.md concepts/body-of-knowledge.md concepts/governance.md concepts/README.md`；预期无匹配。
- [ ] 人工核对每个小节标题是 2–8 字名词短语，且不含字段、文件名、数量或实现参数。
- [ ] 运行 `rg -n '^# 术语数据库 \(Terminology Database\)$' concepts/terminology-database.md`；预期恰好一处。
- [ ] 运行 `rg -n '^# 术语标准$' sources/terminology-standards.md` 与 `rg -n '^# 元数据标准$' sources/metadata-standards.md`；预期各恰好一处。
- [ ] 运行 `python3 scripts/check-links.py`；预期输出“全部链接有效”。
- [ ] 运行 `python3 scripts/check-terms.py --all > /tmp/kb-terminology-foundation-terms-final.txt` 和 `diff -u /tmp/kb-terminology-foundation-terms-before.txt /tmp/kb-terminology-foundation-terms-final.txt || true`；逐项人工复核差异，预期本计划改动的概念文没有新增无依据术语，全表审查中延期的项目用语仍明确留给后续迁移。
- [ ] 运行 `python3 scripts/check-topics.py`；预期与基线同样通过，证明本计划未改词表数据。
- [ ] 运行 `git diff --check "$(cat /tmp/kb-terminology-foundation-base.sha)"..HEAD`；预期无错误，并覆盖全部已提交改动。
- [ ] 运行 `git diff --name-only "$(cat /tmp/kb-terminology-foundation-base.sha)"..HEAD`；预期只出现“文件职责”中的 `sources/` 与 `concepts/` 文件。
- [ ] 阅读最终 `git diff`，确认没有 `design/` 规则、YAML 字段、阈值、Obsidian 或 TBX 实现混入概念层。
- [ ] 确认执行记录明确写着“程序分支不可合并”，直到项目草案、数据迁移和现行设计同步完成；不得在本计划后调用分支收尾技能。
- [ ] 如校验修正了内容，按文件职责提交一笔 `[L1]` 来源或 `[L2]` 概念收口提交；没有修正则不制造空提交。
- [ ] 使用 `superpowers:requesting-code-review` 审查来源可定位性、术语准入、目录职责和旧文去向；处理反馈后重新运行全部校验。

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
