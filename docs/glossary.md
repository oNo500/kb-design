# 术语表 (Glossary)

本库用到的术语，每条一句定义和出处。文章之间的关系见[概念文索引](concepts/README.md)。

出处缩写：

| 缩写 | 来源 |
|---|---|
| ISO | ISO 25964-1:2011，后接条款号 |
| ISO-2 | ISO 25964-2:2013，后接条款号 |
| Z | ANSI/NISO Z39.19-2005 (R2010)，后接条款号 |
| SKOS | W3C SKOS Reference,2009 |
| KG | Hogan et al., *Knowledge Graphs*, 2021 |
| 自定 | 本库自定，无外部来源 |

## 词表的类型

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 受控词表 | controlled vocabulary | 规定好的词、标题或代码列表，每项代表一个概念 | ISO 2.12;Z 4.1 |
| 术语表 / 代码表 | list, pick list | 有限的一组词，按字母或其他明显逻辑排列，无关系 | Z 5.4.1 |
| 同义词环 | synonym ring | 一组检索时视为等价的词；只用于检索，不用于标引 | Z 5.4.2 |
| 分类法 | taxonomy | 全部由首选词构成、以层级或多层级连接的受控词表 | Z 5.4.3 |
| 分类表 | classification scheme | 按分类排列的概念及先组组合的表 | ISO 2.6 |
| 叙词表 | thesaurus | 按已知顺序排列、用标准化关系指示符清楚显示词间关系的受控词表 | Z 5.4.4 |
| 本体 | ontology | 对概念化的明确规范：领域里有哪些类型的实体、允许哪些关系 | Gruber 1993 |
| 知识图谱 | knowledge graph | 以图为载体积累和传达现实世界知识的数据结构，节点为实体，边为关系 | KG |

## 基本单位

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 概念 | concept | 思维单元；独立于表达它的词而存在 | ISO 2.11 |
| 词 | term | 表达概念的词或短语 | ISO 2.61 |
| 首选词 / 叙词 | preferred term, descriptor | 标引时用来代表概念的词 | ISO 2.45 |
| 非首选词 / 非叙词 | non-preferred term | 不用于标引、只作入口的词 | ISO 2.39 |
| 入口词 | entry term, lead-in term | 引导用户找到可用词的词；叙词表里即非首选词 | ISO 2.16 |
| 隐藏标签 | hidden label | 不显示但可检索的非首选词，如拼写错误 | ISO 数据模型 `hidden`;SKOS `hiddenLabel` |
| 标识符 | identifier | 概念、词或其他实体的唯一标识 | ISO 2.25 |
| 限定词 | qualifier | 加在词后区分同形异义的定义性词，如 `Apple (company)` | Z 4.1 |
| 同形异义词 | homograph | 写法相同、意义不同的词 | ISO 2.24 |
| 准同义词 | quasi-synonym | 日常意义不同但词表中视为同一概念的词 | ISO 2.47 |
| 复合词 | compound term | 可拆成多个成分的词 | ISO 2.9 |
| 复合概念 | complex concept | 由多个简单概念组成的概念；是否拆分见 ISO §7 | ISO §7 |
| 领域 | domain | 词表覆盖的主题范围 | — |
| 元数据 | metadata | 标识文档属性的数据；首选词常作为元数据值 | ISO 2.33 |
| 内容对象 | content object | 被标引的东西：文档、图像、人、组织、实物 | Z 4.1;ISO 2.15 document |

## 关系

| 术语 | 符号 | 定义 | 出处 |
|---|---|---|---|
| 等价关系 | USE / UF | 两个词代表同一概念；一个定为首选，其余非首选 | ISO 2.18 |
| 复合等价 | USE+ / UF+ | 一个词由另一语境中两个以上词表示 | ISO 2.8 |
| 层级关系 | BT / NT | 一个概念的范围完全落在另一个之内 | ISO 2.23 |
| 属种关系 | BTG / NTG | 层级的一种：是一种 (is-a) | ISO §10.2 |
| 整部关系 | BTP / NTP | 层级的一种：是一部分 (part-of) | ISO §10.2 |
| 实例关系 | BTI / NTI | 层级的一种：是实例 (instance-of) | ISO §10.2 |
| 相关关系 | RT | 非层级但语义联系强 | ISO 2.2 |
| 自定义关系 | — | 词表自行定义的关系类型 | ISO §10.4 |
| 聚合关系 | paradigmatic | 概念固有的关系，与具体文档无关；叙词表只收这类 | ISO 2.41 |
| 组合关系 | syntagmatic | 因在某文档中同时出现而产生的关系；不进叙词表 | ISO §4.3 |
| 单层级 | monohierarchy | 每个概念只有一个直接上位 | ISO 2.34 |
| 多层级 | polyhierarchy | 一个概念可有多个直接上位 | ISO 2.42 |
| 互反 | reciprocal | 关系必须双向登记：A BT B 则 B NT A | Z 5.4.4 |

## 结构

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 分面 | facet | 同一内在类别的概念分组：对象、材料、动作、地点、时间 | ISO 2.20 |
| 分面分析 | facet analysis | 把领域分解成概念、按分面分组、按划分特征细分 | ISO 2.21;Z 5.3.4 |
| 划分特征 | characteristic of division | 把一个概念细分成一组下位概念所依据的属性 | ISO 2.4 |
| 树 / 层级 | hierarchy | 按 BT/NT 排出的上下位结构 | ISO §10.2 |
| 节点 | node | 树上的一个位置 | — |
| 顶层概念 | top concept | 树的根 | ISO 数据模型 |
| 节点标签 | node label | 树里说明一组兄弟按什么分的标签；内容只能是划分特征或分面名；非词，不能标引 | ISO 2.38;Z 8.3.5 |
| 数组 | array | 一组同级概念 | ISO 2.1 |
| 概念组 / 分组 | concept group | 按用途圈出的一批概念，可跨树、可嵌套 | ISO 数据模型 |
| 微词表 | micro-thesaurus | 叙词表的指定子集，可独立作为完整叙词表使用 | ISO-2 3.46;ISO 数据模型 |
| 辅助表 / 复分表 | auxiliary table | 分类法中单独列出的通用维度表（地区、时间、形式），拼接到主表号后 | 分类法实践，未核原文 |
| 组配号 | synthesized notation | 主表号与辅助表号拼接而成的号码 | ISO 2.22 facet indicator |
| 先组 | pre-coordination | 建表或标引时就组合概念 | ISO 2.44 |
| 后组 | post-coordination | 检索时才组合首选词 | ISO 2.43 |
| 属性 / 维度 | attribute, dimension | 元数据层：文档的一个字段。不是词表结构，但 Z39.19 图 4 也把它叫 facet | Z 5.3.4 |

## 注释与生命周期

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 范围注释 | scope note | 说明词的覆盖范围和用法限制的注释 | ISO 5.2;Z 4.1 |
| 定义 | definition | 词的定义，ISO 中挂在词上 | ISO 数据模型 |
| 历史注释 | history note | 入表日期、变更记录、旧形式及有效期 | Z 11.3.2.2 |
| 编辑注释 | editorial note | 给编辑看的内部注释 | ISO 数据模型 |
| 候选词 | candidate term, provisional term | 提出但未走完审批的词 | Z 11.1.6 |
| 未标引词 | unassigned term | 为补全层级而收、尚未用于标引的词 | Z 11.1.8 |
| 废弃词 | deprecated term | 不再用于标引、保留供检索并指向替代词的词 | Z 11.3.2.1 |
| 孤儿词 | orphan term | 没有任何层级或相关关系的词 | Z 11.4.4 |
| 状态 | status | 词或概念的生命周期状态 | ISO 数据模型 |
| 版本历史 | version history | 词表整体的版本记录 | ISO 数据模型 |

## 建设与治理

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 依据 | warrant | 一个词有资格进词表的理由 | Z 5.3.5 |
| 文献依据 | literary warrant | 词是领域文献里实际通行的说法 | Z 5.3.5.1 |
| 组织依据 | organizational warrant | 词是使用组织偏好的形式 | Z 5.3.5.2 |
| 用户依据 | user warrant | 词是用户检索时实际用的说法 | Z 5.3.5.3 |
| 自上而下 / 自下而上 | top down / bottom up | 委员会法的两个方向；新建词表优先前者 | Z 11.1.3.1 |
| 演绎法 / 归纳法 | deductive / inductive | 经验法的两种：先收集后控制 / 从头控制 | Z 11.1.3.2 |
| 分析综合式分类 | analytico-synthetic classification | 先把主题分析成基本范畴，再综合类号；新主题是旧面的新组合 | Ranganathan 1957 |
| 好客准则 | canon of hospitality | 分类法容纳新类目而不扰动已有类号 | Ranganathan 1957 |
| 领域分析 | domain analysis | 分类反映话语共同体的目的与立场，无唯一正确分类 | Hjørland & Albrechtsen 1995 |
| 剩余类目 | residual category | “其他”“杂项”；其大小是分类失效的信号 | Star & Bowker 2007 |
| 词汇控制 | vocabulary control | 让标引者和检索者对同一概念用同一个词 | ISO §4.2;Z 1.1 |
| 标引 | indexing | 分析文档主题、识别概念、分配标引词 | ISO 2.27 |
| 标引词 | index term | 分配给文档的词；keyword、tag 含义更宽 | ISO 2.26 |
| 查全率 / 查准率 | recall / precision | 检索效果的两个指标；词表对两者都有正面影响 | Z 5.3.6 |
| 互操作性 | interoperability | 系统间交换并使用信息的能力 | ISO 2.29 |
| 来源分级 | de-jure / de-facto / vendor / archival | 引证来源按变更方式分档；依据为组织依据 | Z 5.3.5.2；[命名实体设计](design/model/entities.md) |

## 词表间映射

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 映射 | mapping | 一个词表中的概念与另一个词表中一个或多个概念之间的关系；通常有方向 | ISO-2 3.41 |
| 映射簇 | mapping cluster | 三个以上词表之间协调维护的一组映射 | ISO-2 3.42 |
| 名称规范表 | name authority list | 为一致地命名特定个体而设的受控词表 | ISO-2 3.50 |
| 对照表 | crosswalk | 两个以上词表之间概念映射的表 | ISO-2 3.21 |
| 源词表 / 目标词表 | source / target vocabulary | 映射的起点 / 终点 | ISO-2 §3（条款号在样章之外） |
| 等价映射 | equivalence mapping | 目标概念与源概念范围相同 | ISO-2 3.27 |
| 精确 / 不精确 / 部分等价 | exact / inexact / partial equivalence | 等价的三个程度 | ISO-2 §11 |
| 层级映射 | hierarchical mapping | 目标概念比源概念宽或窄 | ISO-2 §9 |
| 相关映射 | associative mapping | 有关但非等价非层级 | ISO-2 §10 |
| 区分式映射 | differentiated mapping | 标明映射类型和等价程度的映射方法 | ISO-2 3.23 |
| 中心辐射 | hub structure | 所有词表映射到一个中心词表的结构模型 | ISO-2 §6 |
| exactMatch / closeMatch | — | SKOS 的精确 / 不精确等价；前者传递，后者不传递 | SKOS §10 |
| broadMatch / narrowMatch / relatedMatch | — | SKOS 的层级 / 相关映射 | SKOS §10 |

## 知识体系

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 知识体系 | body of knowledge, BoK | 一个学科或职业公认知识范围的结构化清单 | SWEBOK;ISO/IEC TR 19759 |
| 知识领域 | knowledge area, KA | 知识体系的主要区域 | SWEBOK;CS2023 |
| 知识单元 | knowledge unit, KU | 知识领域内的主题簇 | CS2023 |
| 主题 | topic | 知识单元内的具体知识点，标核心或选修 | CS2023 |
| 普遍接受的知识 | generally accepted knowledge | 多数项目多数时候适用且广泛认同的知识；知识体系只收这类 | SWEBOK |

## 元数据

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| Dublin Core | Dublin Core Metadata Element Set | 十五个核心元数据元素，任何资源都可用 | ISO 15836-1:2017 |
| DCMI Metadata Terms | — | Dublin Core 的扩展属性与类 | ISO 15836-2:2019；DCMI 2020 |
| DCMI Type Vocabulary | — | `type` 的推荐取值，按媒介性质分 12 类 | DCMI |
| 资源 | resource | 被描述的东西：文档、图像、数据集、软件 | DCMI |
| 内容单元 | — | 知识库里最小的可独立引用、可独立打标签的东西；参照 DITA topic | 本库，参照 DITA 1.3 §2.2.1 |

## 应用与生成

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| Application Profile | Application Profile | 为特定应用规定 metadata term、约束、使用与编码语法的文档集合 | DCMI Singapore Framework；中文查无高阶正文依据 |
| Reproducible Builds | Reproducible Builds | 使任何一方在相同 source、environment 和 instructions 下重建逐字节相同 artifacts 的实践 | Reproducible Builds definition |

## 写作与设计方法

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 相关 / 可找到 / 可理解 / 可使用 | relevant / findable / understandable / usable | plain language 的四条原则 | ISO 24495-1:2023 |
| 第一原理 | first principle | 不能再从别的命题推出、只能作为起点的命题 | Aristotle, *Posterior Analytics* |
| 设计理由 | design rationale | 记录“为什么这样决定”而不只是“决定了什么” | Kunz & Rittel 1970；Nygard 2011 |
| 被替代 | superseded | 决定记录被新决定取代后的状态 | Nygard ADR 2011 |
| 内容模型 | content model | 内容单元允许有哪些组成部分及其结构 | SGML（ISO 8879）、DITA 沿用 |
| 知识组织 | knowledge organization | 对知识进行描述、分类和排序的活动与系统；KOS 即知识组织系统 | ISO 25964；SKOS |
| 公众人物 | public figure | 在社会事务中担任显著角色、或主动进入公共争议的人；本库 `person` 实体只收此类，具体为已发表作品的作者、公开项目的维护者、方法的提出者 | 美国判例法 *Gertz v. Robert Welch* (1974)，见 [Cornell LII](https://www.law.cornell.edu/wex/public_figure) |
| 个体 | individual | 名称规范表所收的对象：唯一的个体，而非类 | ISO-2 3.50 注 |
| 划分 | partition | 把一个集合分成互不重叠、合起来是全集的几组 | 数学通用术语 |

## 笔记的类型

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 体裁 | genre | 按读者需求或内容性质划分的文本类别 | IPTC genre；Diátaxis |
| 排障 | troubleshooting | DITA 的 topic 类型：纠正性操作信息 | DITA 1.3 §2.7.1.6 |
| 闪念笔记 / 文献笔记 / 永久笔记 | fleeting / literature / permanent note | 按工作流阶段分的三种笔记 | Ahrens 2017 |
| 隐性知识 / 显性知识 | tacit / explicit knowledge | 难以形式化的个人知识 / 正式而系统、易于交流的知识 | Nonaka 1991 |
| 速查表 | cheat sheet | 供快速参考的简明笔记集 | Wikidata Q2309859 |
| 札记簿 | commonplace book | 抄录重要段落并按主题整理的本子 | Harvard Library |
| 认知层级 | cognitive level | 对主题理解的深度：记忆到创造六级 | Bloom 修订版，Krathwohl 2002 |
| 帕累托原则 | Pareto principle | 关键的少数与琐碎的多数；选材法则 | Juran 1951 命名 |

## 治理与维护

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 治理 | governance | 组织借以被指导、监督并被问责的系统；对管理的管理 | ISO 37000:2021 |
| 政策 | policy | 治理主体定下的、管理必须遵守的规则 | ISO 15489-1 §6.2 |
| 决策权 | decision rights | 谁有权对哪类事项做决定 | DAMA-DMBOK 数据治理 |
| 监控与评价 | monitoring and evaluation | 对管理过程及其结果的持续检查与定期评估 | ISO 15489-1 §6.4 |
| 审计追踪 | audit trail | 记录谁在何时做了什么变更的连续记录 | ISO 15489-1 元数据要求 |
| 治理评审 | governance review | 治理主体对治理本身的定期评审 | ISO 37000:2021 |
| 审计 | audit | 对记录与过程是否符合规则的检查 | ISO 15489-1 §6.4 |
| 处置 | disposition | 执行保留、销毁或移交决定的过程 | ISO 15489-1 §3.8 |
| 断言 | assertion | 人判断而非抄自来源的字段值 | 本库用法；溯源依据 W3C PROV-O |
| 指标 | indicator | 脚本能算出或外部能通知、用于监控的量 | ISO 15489-1 §6.4 的监控对象 |
| 阈值 | threshold | 指标触发动作的界值 | 通用 |
| 批准 | approve | 候选词审核通过转为正式词 | Z 11.1.6 |

## 知识图谱

| 术语 | 英文 | 定义 | 出处 |
|---|---|---|---|
| 三元组 | triple | 主语 — 谓语 — 宾语，图的最小单位 | W3C RDF 1.1 |
| 实体 | entity | 图的节点，有唯一 ID | KG |
| 关系 | relation, edge | 带类型的有向边 | KG |
| 属性 | property | 挂在实体或边上的字面值 | KG |
| Schema | schema | 本体在工程语境的叫法：类型与关系的定义 | — |
| 推理 | reasoning, inference | 按规则从已有边推出新边 | KG |
| RDF | Resource Description Framework | W3C 的三元组数据模型 | W3C RDF 1.1 |
| RDFS / OWL | — | RDF 上的 schema 语言 / 本体语言 | W3C |
| SPARQL | — | RDF 查询语言 | W3C SPARQL 1.1 |
| SKOS | Simple Knowledge Organization System | 用 RDF 表达词表的 W3C 标准 | W3C SKOS |
| 属性图 | property graph | 节点和边都可带属性的图模型 | ISO/IEC 39075 |
| Cypher / GQL | — | 属性图查询语言；GQL 是 2024 年的 ISO 标准 | ISO/IEC 39075:2024 |

## 引用的标准与文献

| 名称 | 是什么 |
|---|---|
| ISO 25964-1:2011 / -2:2013 | 叙词表国际标准，见 [笔记](references/iso-25964.md) |
| GB/T 13190.1-2015 / .2-2018 | 等同采用 ISO 25964 的国标 |
| ANSI/NISO Z39.19-2005 (R2010) | 美国受控词表标准，全文免费 |
| ISO 704 | 术语工作原则与方法，Wüster 理论的标准化版本；未核对 |
| W3C SKOS / RDF / OWL / SPARQL | 语义网标准族 |
| ISO/IEC 39075:2024 GQL | 属性图查询语言标准 |
| Cutter (1876) | 字典式目录规则，主题标目“一主题一词”的源头；未核对 |
| Hulme (1911) | *Principles of Book Classification*,Library Association Record 连载；文献依据的源头 |
| Dewey (1876) | 十进分类法；未核对 |
| Ranganathan (1933) | 冒号分类法，分面分析的源头；经 Z39.19 §5.3.4 转述 |
| Wüster (1931) | 斯图加特博士论文 *Internationale Sprachnormung in der Technik*；术语学奠基，ISO/TC 37 1936 年由此成立 |
| Gruber (1993) | 计算机领域本体的定义；未核对 |
| Hogan et al. (2021) | 知识图谱综述，[arXiv](https://arxiv.org/abs/2003.02320) |
| Ehrlinger & Wöß (2016) | 知识图谱定义梳理，[CEUR](https://ceur-ws.org/Vol-1695/paper4.pdf) |

## 模型译名

以下中英形式依据译名第 5 级登记：模型既有知识，外部用法未核实。对应概念及范围沿用现行词表，不形成新概念；逐条判断与原范围保存在[译名采纳输入](../data/inputs/topics/label-adoptions.json)，本批授权见[结构化语言依据](decisions/structured-label-basis.md#批次授权)。同一中英形式覆盖多个既有记录时合并展示，稳定身份仍分别保留。

| 中文形式 | 英文形式 | 对应记录 |
|---|---|---|
| 可访问性与包容性设计 | Accessibility and Inclusive Design | `topics/accessibility-and-inclusive-design` |
| 设计中的问责与责任 | Accountability and Responsibility in Design | `topics/accountability-and-responsibility-in-design` |
| 高级文件系统 | Advanced File systems | `topics/advanced-file-systems` |
| 高级程序设计构造 | Advanced Programming Constructs | `topics/advanced-programming-constructs` |
| 智能体与认知系统 | Agents and Cognitive Systems | `topics/agents-and-cognitive-systems` |
| AI 攻击准备 | AI Attack Staging | `topics/ai-attack-staging` |
| AI 模型访问 | AI Model Access | `topics/ai-model-access` |
| 算法基础 | Algorithmic Foundations | `topics/algorithmic-foundations` |
| 算法策略 | Algorithmic Strategies | `topics/algorithmic-strategies` |
| 算法 | Algorithms | `topics/algorithms-software-development-fundamentals` |
| 并行与分布式算法 | Algorithms | `topics/algorithms` |
| API 与 Web 服务 | API and Web Service | `topics/api-and-web-service` |
| 应用层 | Application Layer | `topics/application-layer` |
| 应用与社会影响 | Applications and Societal Impact | `topics/applications-and-societal-impact` |
| 渲染应用与技术 | Applied Rendering and Techniques | `topics/applied-rendering-and-techniques` |
| 体系结构与组织 | Architecture and Organization | `topics/architecture-and-organization` |
| 面向切面程序设计 | Aspect-Oriented Programming | `topics/aspect-oriented-programming` |
| 汇编级机器组织 | Assembly Level Machine Organization | `topics/assembly-level-machine-organization` |
| 身份认证 | Authentication | `topics/authentication` |
| 授权 | Authorization | `topics/authorization` |
| 基本概念 | Basic Concepts | `topics/basic-concepts` |
| 速查表 | Cheat sheet | `forms/cheat-sheet` |
| 代码生成 | Code Generation | `topics/code-generation` |
| 收集 | Collection | `topics/collection-artificial-intelligence`, `topics/collection` |
| 命令与控制 | Command and Control | `topics/command-and-control-artificial-intelligence`, `topics/command-and-control` |
| 共同方面与共同关注点 | Common Aspects/Shared Concerns | `topics/common-aspects-shared-concerns` |
| 沟通 | Communication | `topics/communication-society-ethics-and-the-profession` |
| 通信 | Communication | `topics/communication` |
| 编译器语义分析 | Compiler Semantic Analysis | `topics/compiler-semantic-analysis` |
| 复杂度 | Complexity | `topics/complexity` |
| 计算模型与形式语言 | Computational Models and Formal Languages | `topics/computational-models-and-formal-languages` |
| 计算机动画 | Computer Animation | `topics/computer-animation` |
| 计算基础 | Computing Foundations | `topics/computing-foundations` |
| 计算史 | Computing History | `topics/computing-history` |
| 并发 | Concurrency | `topics/concurrency` |
| 配置 | Configuration | `topics/configuration` |
| 协调 | Coordination | `topics/coordination` |
| 数据库系统核心概念 | Core Database System Concepts | `topics/core-database-system-concepts` |
| 凭据访问 | Credential Access | `topics/credential-access-artificial-intelligence`, `topics/credential-access` |
| 数据分析 | Data Analytics | `topics/data-analytics` |
| 数据建模 | Data Modeling | `topics/data-modeling` |
| 数据保护 | Data Protection | `topics/data-protection` |
| 数据安全与隐私 | Data Security and Privacy | `topics/data-security-and-privacy` |
| 数据库管理系统内部机制 | DBMS Internals | `topics/dbms-internals` |
| 防御规避 | Defense Evasion | `topics/defense-evasion` |
| 防御削弱 | Defense Impairment | `topics/defense-impairment` |
| 程序设计语言的设计原则 | Design Principles of Programming Languages | `topics/design-principles-of-programming-languages` |
| 设备管理 | Device management | `topics/device-management` |
| 示意图 | Diagram | `forms/diagram` |
| 数字逻辑与数字系统 | Digital Logic and Digital Systems | `topics/digital-logic-and-digital-systems` |
| 发现 | Discovery | `topics/discovery-artificial-intelligence`, `topics/discovery` |
| 分布式数据库与云计算 | Distributed Databases/Cloud Computing | `topics/distributed-databases-cloud-computing` |
| 多样性、公平、包容与可访问性 | Diversity, Equity, Inclusion, and Accessibility | `topics/diversity-equity-inclusion-and-accessibility` |
| 计算经济 | Economies of Computing | `topics/economies-of-computing` |
| 嵌入式平台 | Embedded Platforms | `topics/embedded-platforms` |
| 新兴主题 | Emerging Topics | `topics/emerging-topics` |
| 编码与净化 | Encoding and Sanitization | `topics/encoding-and-sanitization` |
| 工程基础 | Engineering Foundations | `topics/engineering-foundations` |
| 设计评估 | Evaluating the Design | `topics/evaluating-the-design` |
| 评估 | Evaluation | `topics/evaluation` |
| 事件驱动与响应式程序设计 | Event-Driven and Reactive Programming | `topics/event-driven-and-reactive-programming` |
| 考试 | Exam | `forms/exam` |
| 执行 | Execution | `topics/execution-artificial-intelligence`, `topics/execution` |
| 练习 | Exercise | `forms/exercise` |
| 数据外传 | Exfiltration | `topics/exfiltration-artificial-intelligence`, `topics/exfiltration` |
| 实验 | Experiment | `forms/experiment` |
| 容错 | Fault tolerance | `topics/fault-tolerance` |
| 图像 | Figure | `forms/figure` |
| 文件处理 | File Handling | `topics/file-handling` |
| 文件系统接口与实现 | File Systems API and Implementation | `topics/file-systems-api-and-implementation` |
| 形式化开发方法 | Formal Development Methodologies | `topics/formal-development-methodologies` |
| 形式语义 | Formal Semantics | `topics/formal-semantics` |
| 基础数据结构与算法 | Foundational Data Structures and Algorithms | `topics/foundational-data-structures-and-algorithms` |
| 安全基础 | Foundational Security | `topics/foundational-security` |
| 程序设计语言基础 | Foundations of Programming Languages | `topics/foundations-of-programming-languages` |
| 功能组织 | Functional Organization | `topics/functional-organization` |
| 函数式程序设计 | Functional Programming | `topics/functional-programming` |
| 基本概念 | Fundamental Concepts | `topics/fundamental-concepts` |
| 基础数据结构 | Fundamental Data Structures | `topics/fundamental-data-structures` |
| 基本问题 | Fundamental Issues | `topics/fundamental-issues` |
| 知识表示与推理基础 | Fundamental Knowledge Representation and Reasoning | `topics/fundamental-knowledge-representation-and-reasoning` |
| 程序设计基本概念与实践 | Fundamental Programming Concepts and Practices | `topics/fundamental-programming-concepts-and-practices` |
| 网络基础 | Fundamentals | `topics/fundamentals` |
| 游戏平台 | Game Platforms | `topics/game-platforms` |
| 几何建模 | Geometric Modeling | `topics/geometric-modeling` |
| 图表 | Graph | `forms/graph` |
| 图形学与互动技术 | Graphics and Interactive Techniques | `topics/graphics-and-interactive-techniques` |
| 异构体系结构 | Heterogeneous Architectures | `topics/heterogeneous-architectures` |
| 人机交互 | Human-Computer Interaction | `topics/human-computer-interaction` |
| 图像处理 | Image Processing | `topics/image-processing` |
| 沉浸 | Immersion | `topics/immersion` |
| 影响 | Impact | `topics/impact-artificial-intelligence`, `topics/impact` |
| 访问控制不当 | Improper Access Control | `topics/improper-access-control` |
| 编码规范遵循不当 | Improper Adherence to Coding Standards | `topics/improper-adherence-to-coding-standards` |
| 异常状况检查或处理不当 | Improper Check or Handling of Exceptional Conditions | `topics/improper-check-or-handling-of-exceptional-conditions` |
| 资源生命周期控制不当 | Improper Control of a Resource Through its Lifetime | `topics/improper-control-of-a-resource-through-its-lifetime` |
| 多个行为正确实体间的交互不当 | Improper Interaction Between Multiple Correctly-Behaving Entities | `topics/improper-interaction-between-multiple-correctly-behaving-entities` |
| 中和处理不当 | Improper Neutralization | `topics/improper-neutralization` |
| 计算错误 | Incorrect Calculation | `topics/incorrect-calculation` |
| 比较错误 | Incorrect Comparison | `topics/incorrect-comparison` |
| 索引 | Index | `forms/index` |
| 初始访问 | Initial Access | `topics/initial-access-artificial-intelligence`, `topics/initial-access` |
| 控制流管理不足 | Insufficient Control Flow Management | `topics/insufficient-control-flow-management` |
| 知识产权 | Intellectual Property | `topics/intellectual-property` |
| 交互 | Interaction | `topics/interaction` |
| 交互式计算平台 | Interactive Computing Platforms | `topics/interactive-computing-platforms` |
| 接口与通信 | Interfacing and Communication | `topics/interfacing-and-communication` |
| 网际层 | Internet Layer | `topics/internet-layer` |
| 语言语用 | Language Pragmatics | `topics/language-pragmatics` |
| 语言翻译与执行 | Language Translation and Execution | `topics/language-translation-and-execution` |
| 横向移动 | Lateral Movement | `topics/lateral-movement-artificial-intelligence`, `topics/lateral-movement` |
| 讲授 | Lecture | `forms/lecture` |
| 链路层 | Link Layer | `topics/link-layer` |
| 逻辑程序设计 | Logic Programming | `topics/logic-programming` |
| 逻辑表示与推理 | Logical Representation and Reasoning | `topics/logical-representation-and-reasoning` |
| 机器级数据表示 | Machine-Level Data Representation | `topics/machine-level-data-representation` |
| 数学和统计基础 | Mathematical and Statistical Foundations | `topics/mathematical-and-statistical-foundations` |
| 数学基础 | Mathematical Foundations | `topics/mathematical-foundations` |
| 存储层次 | Memory Hierarchy | `topics/memory-hierarchy` |
| 内存管理 | Memory Management | `topics/memory-management` |
| 伦理分析方法 | Methods for Ethical Analysis | `topics/methods-for-ethical-analysis` |
| 移动平台 | Mobile Platforms | `topics/mobile-platforms` |
| 移动性 | Mobility | `topics/mobility` |
| 叙述性文本 | Narrative text | `forms/narrative-text` |
| 网络安全 | Network Security | `topics/network-security` |
| 网络应用 | Networked Applications | `topics/networked-applications` |
| 网络与通信 | Networking and Communication | `topics/networking-and-communication` |
| NoSQL 系统 | NoSQL Systems | `topics/nosql-systems` |
| OAuth 与 OIDC | OAuth and OIDC | `topics/oauth-and-oidc` |
| 操作系统 | Operating Systems | `topics/operating-systems` |
| 计算机系统概览 | Overview of Computer Systems | `topics/overview-of-computer-systems` |
| 并行与分布式计算 | Parallel and Distributed Computing | `topics/parallel-and-distributed-computing-foundations-of-programming-languages`, `topics/parallel-and-distributed-computing` |
| 感知与计算机视觉 | Perception and Computer Vision | `topics/perception-and-computer-vision` |
| 性能与能效 | Performance and Energy Efficiency | `topics/performance-and-energy-efficiency` |
| 性能评估 | Performance Evaluation | `topics/performance-evaluation` |
| 持久化 | Persistence | `topics/persistence-artificial-intelligence`, `topics/persistence` |
| 规划 | Planning | `topics/planning` |
| 操作系统原理 | Principles of Operating System | `topics/principles-of-operating-system` |
| 隐私与公民自由 | Privacy and Civil Liberties | `topics/privacy-and-civil-liberties` |
| 权限提升 | Privilege Escalation | `topics/privilege-escalation-artificial-intelligence`, `topics/privilege-escalation` |
| 概率表示与推理 | Probabilistic Representation and Reasoning | `topics/probabilistic-representation-and-reasoning` |
| 问题陈述 | Problem statement | `forms/problem-statement` |
| 进程模型 | Process Model | `topics/process-model` |
| 产品需求 | Product Requirements | `topics/product-requirements` |
| 职业伦理 | Professional Ethics | `topics/professional-ethics` |
| 程序抽象与表示 | Program Abstraction and Representation | `topics/program-abstraction-and-representation` |
| 程序分析与分析器 | Program Analysis and Analyzers | `topics/program-analysis-and-analyzers` |
| 并行与分布式程序 | Programs | `topics/programs` |
| 保护与安全 | Protection and Safety | `topics/protection-and-safety` |
| 保护机制失效 | Protection Mechanism Failure | `topics/protection-mechanism-failure` |
| 量子体系结构 | Quantum Architectures | `topics/quantum-architectures` |
| 查询构造 | Query Construction | `topics/query-construction` |
| 查询处理 | Query Processing | `topics/query-processing` |
| 问卷 | Questionnaire | `forms/questionnaire` |
| 实时与嵌入式系统 | Real-time and Embedded Systems | `topics/real-time-and-embedded-systems` |
| 侦察 | Reconnaissance | `topics/reconnaissance-artificial-intelligence`, `topics/reconnaissance` |
| 重构与代码演化 | Refactoring and Code Evolution | `topics/refactoring-and-code-evolution` |
| 关系数据库 | Relational Databases | `topics/relational-databases` |
| 可靠性支持 | Reliability Support | `topics/reliability-support` |
| 资源开发 | Resource Development | `topics/resource-development-artificial-intelligence`, `topics/resource-development` |
| 资源管理 | Resource Management | `topics/resource-management` |
| 机器人平台 | Robot Platforms | `topics/robot-platforms` |
| 机器人学 | Robotics | `topics/robotics` |
| 操作系统的作用与目的 | Role and Purpose of Operating Systems | `topics/role-and-purpose-of-operating-systems` |
| 路由与转发 | Routing and Forwarding | `topics/routing-and-forwarding` |
| 运行时行为与系统 | Run-time Behavior and Systems | `topics/run-time-behavior-and-systems` |
| 调度 | Scheduling | `topics/scheduling` |
| 搜索 | Search | `topics/search` |
| 安全编码 | Secure Coding | `topics/secure-coding` |
| 安全编码与体系结构 | Secure Coding and Architecture | `topics/secure-coding-and-architecture` |
| 安全通信 | Secure Communication | `topics/secure-communication` |
| 安全处理器体系结构 | Secure Processor Architectures | `topics/secure-processor-architectures` |
| 安全 | Security | `topics/security` |
| 安全分析、设计与工程 | Security Analysis, Design, and Engineering | `topics/security-analysis-design-and-engineering` |
| 安全治理 | Security Governance | `topics/security-governance` |
| 安全日志记录与错误处理 | Security Logging and Error Handling | `topics/security-logging-and-error-handling` |
| 安全政策、法律与计算机犯罪 | Security Policies, Laws and Computer Crimes | `topics/security-policies-laws-and-computer-crimes` |
| 自我评估 | Self assessment | `forms/self-assessment` |
| 自包含令牌 | Self-contained Tokens | `topics/self-contained-tokens` |
| 半结构化与非结构化数据库 | Semi-structured and Unstructured Databases | `topics/semi-structured-and-unstructured-databases` |
| 会话管理 | Session Management | `topics/session-management` |
| 着色与高级渲染 | Shading and Advanced Rendering | `topics/shading-and-advanced-rendering` |
| Shell 脚本编程 | Shell Scripting | `topics/shell-scripting` |
| 仿真 | Simulation | `forms/simulation`, `topics/simulation` |
| 单跳通信 | Single Hop Communication | `topics/single-hop-communication` |
| 幻灯片 | Slide | `forms/slide` |
| 社会情境 | Social Context | `topics/social-context` |
| 社会、伦理与职业 | Society, Ethics, and the Profession | `topics/society-ethics-and-the-profession-algorithmic-foundations`, `topics/society-ethics-and-the-profession-data-management`, `topics/society-ethics-and-the-profession-foundations-of-programming-languages`, `topics/society-ethics-and-the-profession-graphics-and-interactive-techniques`, `topics/society-ethics-and-the-profession-human-computer-interaction`, `topics/society-ethics-and-the-profession-operating-systems`, `topics/society-ethics-and-the-profession-security`, `topics/society-ethics-and-the-profession-software-development-fundamentals`, `topics/society-ethics-and-the-profession-systems-fundamentals`, `topics/society-ethics-and-the-profession` |
| 软件体系结构 | Software Architecture | `topics/software-architecture` |
| 软件配置管理 | Software Configuration Management | `topics/software-configuration-management` |
| 软件设计 | Software Design | `topics/software-design` |
| 软件开发基础 | Software Development Fundamentals | `topics/software-development-fundamentals` |
| 软件开发实践 | Software Development Practices | `topics/software-development-practices` |
| 软件工程经济学 | Software Engineering Economics | `topics/software-engineering-economics` |
| 软件工程管理 | Software Engineering Management | `topics/software-engineering-management` |
| 软件工程模型与方法 | Software Engineering Models and Methods | `topics/software-engineering-models-and-methods` |
| 软件工程运维 | Software Engineering Operations | `topics/software-engineering-operations` |
| 软件工程过程 | Software Engineering Process | `topics/software-engineering-process` |
| 软件工程职业实践 | Software Engineering Professional Practice | `topics/software-engineering-professional-practice` |
| 软件维护 | Software Maintenance | `topics/software-maintenance` |
| 软件质量 | Software Quality | `topics/software-quality` |
| 软件可靠性 | Software Reliability | `topics/software-reliability` |
| 软件需求 | Software Requirements | `topics/software-requirements` |
| 软件安全 | Software Security | `topics/software-security` |
| 软件测试 | Software Testing | `topics/software-testing` |
| 软件验证与确认 | Software Verification and Validation | `topics/software-verification-and-validation` |
| 专用平台开发 | Specialized Platform Development | `topics/specialized-platform-development` |
| 隐蔽 | Stealth | `topics/stealth` |
| 可持续性 | Sustainability | `topics/sustainability` |
| 可持续性议题 | Sustainability Issues | `topics/sustainability-issues` |
| 语法分析 | Syntax Analysis | `topics/syntax-analysis` |
| 系统设计 | System Design | `topics/system-design-systems-fundamentals`, `topics/system-design` |
| 系统性能 | System Performance | `topics/system-performance` |
| 系统可靠性 | System Reliability | `topics/system-reliability` |
| 系统安全 | System Security | `topics/system-security` |
| 系统执行与内存模型 | Systems Execution and Memory Model | `topics/systems-execution-and-memory-model` |
| 系统基础 | Systems Fundamentals | `topics/systems-fundamentals` |
| 表格 | Table | `forms/table` |
| 实体与物理计算 | Tangible/Physical Computing | `topics/tangible-physical-computing` |
| 团队协作 | Teamwork | `topics/teamwork` |
| 数据的作用与生命周期 | The Role of Data and the Data Life Cycle | `topics/the-role-of-data-and-the-data-life-cycle` |
| 工具与环境 | Tools and Environments | `topics/tools-and-environments` |
| 传输层 | Transport Layer | `topics/transport-layer` |
| 类型系统 | Type Systems | `topics/type-systems` |
| 用户理解及个体目标与人际交互 | Understanding the User: Individual goals and interactions with others | `topics/understanding-the-user-individual-goals-and-interactions-with-others` |
| 验证与业务逻辑 | Validation and Business Logic | `topics/validation-and-business-logic` |
| 虚拟化 | Virtualization | `topics/virtualization` |
| 可视化 | Visualization | `topics/visualization` |
| Web 前端安全 | Web Frontend Security | `topics/web-frontend-security` |
| Web 平台 | Web Platforms | `topics/web-platforms` |
| Web 实时通信 | WebRTC | `topics/webrtc` |
