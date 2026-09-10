# 命名实体词表

`data/vocab/entities.yaml` 是本库的名称规范表（name authority list），收软件产品、编程语言、组织等个体。主题词表管理概念，例如“AI 编程助手”和“关系型数据库”；命名实体词表管理个体，例如 Claude Code、PostgreSQL 和 Anthropic。

ISO 25964-2 §23 把名称规范表定义为为一致命名特定实体而建立的受控词表；实体是唯一的个体，不与主题概念建立等价映射。理论见[受控词表](../../concepts/controlled-vocabulary.md)和[词表映射](../../concepts/vocabulary-mapping.md)。

本文按[参考文献分离](../../decisions/source-bibliography-separation.md)划分普通实体与设计文献。标准、出版物和设计依据文档的身份进入[参考文献目录](bibliography.md)，用途权限仍由独立登记控制。来源相关数据统一使用 schema_version 3；严格工具不接受旧引用形状，旧决定与历史按原基线及列明的机械迁移映射解释。

## 对象分工

“实体词表”是本项目名称规范表的收录范围，不是对广义实体的穷尽定义。文献可以是[知识图谱中的对象](../../concepts/knowledge-graph.md#对象与表示)，其设计依据身份由参考文献目录维护；普通笔记引用的资料不自动进入任何一个目录。

主题词表管理概念，实体词表统一产品、组织等涉及对象的名称与身份，参考文献目录管理设计依据文献。以下比较主题与涉及对象的组织方式。

| 比较项 | 主题词表 | 命名实体词表 |
|---|---|---|
| 管理对象 | 概念 | 个体：产品、语言、组织等 |
| 变化速度 | 几年一版 | 产品一年可发布多个版本，也可能停止维护 |
| 结构 | 层级树 | 扁平；实体之间只保留已定义的关系 |
| 外部依据 | 知识体系、标准 | 厂商文档、出版物、Wikidata |
| 相互关系 | 不记录实体 | 每个实体通过 `subjects` 挂到一个或多个主题概念，不占树的位置 |

概念与个体混在一棵树中，会让稳定结构随易变对象移动。一个产品还可能关联多个主题；`subjects` 的多值关系表达这种挂接。

## 实体记录

实体共同字段为 `id`、`label`、`kind`、`subjects`、`status` 和 `added`。`status` 继续表示项目记录状态，不能被来源外部状态覆盖。`id` 保持稳定；名称变化不改变身份。本表不保存 standard／publication，也不接受文献专有的 tier、source_status、review 或 watch。

| 字段 | 表示与条件 |
|---|---|
| `label`、`alt`、`hidden` | 按语言保存名称与可选别名；不因迁移取得新的 designation 准入 |
| `subjects` | 无重复的主题 ID 列表，每个值均有归属依据或明确项目判断 |
| `scope`、`form` | 保留范围与已登记形式，不从缺失证据推导新类别 |
| `vendor`、`creator` | 分别为实体 ID 和实体 ID 列表；目标仅为本表普通实体 |
| `urls` | role、url、primary 条目；官网地址不因登记取得书目准入或用途资格 |
| `match` | registry、item、rel、basis；具体映射与用途资格分别核对 |
| `replaced_by`、`history` | 保留替代指向和只追加历史；删除或改身份仍受决定约束 |
| `added` | 原项目添加日期，不改为迁移日期 |

### 归属依据

外部 `basis.subjects` 是条目列表，每项为 `values` 与 `references`。values 明确列出受到支持的 subjects；references 是非空的严格依据列表，每项包含 reference、locator，以及按可变性要求的 checked。同一材料支持多个值时可以共用一组 values，但不得从记录级旧字符串自动推导逐值支持范围。

原 `self` 判断保存在 `assertions.subjects`，每项包含 values、`disposition: project_assertion`、`original: self` 和 migration 审计定位。它保存项目判断，不能充当外部依据；具有这类归属判断的实体不得为 active。basis 与 assertions 的 values 合集必须覆盖 subjects，且不能包含不属于该记录的主题。

紧凑引用只在核对材料、定位和支持范围后转为严格依据。未核对原值保留在迁移审计，不能装入 assertions 冒充已处置的项目判断，也不能清空依据使正式切换通过。人工判断、designation 的形式依据和概念对应依据分别按[维护](../governance/maintenance.md)与[治理](../governance/governance.md)处理。

### 事实依据

普通实体的 basis.label、basis.kind、basis.urls、basis.scope、basis.vendor 可保存严格文献依据，也可直接保存官方页面的 url、locator、checked。两种形状互斥，不得同时填写 reference 与 url；直接 URL 必须有真实核对日期和能说明支持该项事实的定位。读取失败保留未核结论，不能补造 checked。

此入口不适用于 subjects、术语定义、语言形式、映射或结构派生，不授予 mapping、structure 或 group 资格。名称事实的官方出处不替代 designation 准入；相同名称和搜索命中也不证明同一实体。subjects 继续按逐值依据或明确项目判断处理。上述键名是项目表示选择，不是外部标准规定。

### 类别

`kind` 只取已登记的 Wikidata 类，不自定。

| kind | Wikidata | 例 |
|---|---|---|
| `software` | Q7397 software | Claude Code、PostgreSQL、Neo4j |
| `programming-language` | Q9143 programming language | Python、Rust、TypeScript |
| `organization` | Q43229 organization | Anthropic、MITRE、W3C |
| `person` | Q5 human | Ranganathan、Wüster、Hogan、Cockburn |
| `large-language-model` | Q115305900 large language model | Claude Opus 4、GPT-4 |

需要更多类别时从 Wikidata 取，并记录 Q 号。文献种类及形式另见[参考文献目录](bibliography.md)。

`person` 只收在相关主题或活动中有显著公开角色、且符合公众人物判断依据的人。已发表作品的作者、公开项目的维护者和方法的提出者只作为可能的收录对象，不因该身份、Wikidata 条目或公开出处自动取得公众人物资格；须分别说明一般公众人物依据，或相关公共争议中的突出角色及适用范围，并提供可引用的公开出处。不收私人、同事或联系人。文献记录用 `creator` 指向已收录人员，软件实体的个人维护者用 `vendor` 指向人。该规则由[人员收录澄清](../../decisions/person-admission-clarification.md)采纳；不扩大隐私边界，不自动删改现有实体。

### 生命周期

全部实体的 status 使用 candidate、active、deprecated，规则见[主题词表](topics.md)。实体不使用 unassigned，因为它不为补全复制结构建立。

产品停止维护或被替代时，项目是否废弃记录按现行决定权限处理；有替代对象时记录 replaced_by，历史记录不删。文献的外部状态由参考文献目录独立管理，不传递为普通实体的项目状态。

## 映射关系

实体的主要映射目标是 Wikidata；厂商文档可作为地址或具体事实依据，不因此成为映射目标。严格 match 使用 registry、item、rel、basis，registry 指向获准 mapping 角色的用途记录，item 保存外部标识或永久地址，basis 与每条关系相邻。

旧 match.source／id 不在严格读取中保留。旧关系名称、相同标签和用途存在均不能代替具体身份或概念对应证据。未核关系原则上阻断相应正式转换。[来源收尾](../../decisions/source-completion.md)明确采纳的 17 条隔离关系除外：旧关系、来源、旧值与结论保存在该决定的隔离清单和 Git 历史，不进入正式 match；对象、标签、项目状态和其他关系保留。该例外不为其补造依据，也不授权其他关系静默省略。

Pydantic 保持同一软件实体，scope 描述软件身份；version: "2" 单独表示项目选用的主要版本，不将版本范围当作另一个软件身份。OpenClaw 的 subjects 按[来源收尾](../../decisions/source-completion.md)只保留 artificial-intelligence；这是本批依据支持范围的取舍，不表示它不能编程，也不改变实体或 active 状态。

## 主题职责

- 内容单元的 `subject` 填主题概念，`entities` 填实体，见[内容模型](content-model.md)。
- “Rust 的所有权”使用 `subject: [systems-execution-and-memory-model]` 和 `entities: [rust]`；具体语言不进入主题树。
- 一个实体的 `subjects` 可以有多个；主题概念不反向记录实体，需要时由脚本计算某主题下的全部实体。
- 设计标准和文献在参考文献目录中查找，不通过本表 kind 或主题分面字段查询。
- 通用 `origin` 不再是主题目标字段。文献记录只提供可解析身份；发现观察、具体值依据、实际派生和概念映射各自记录，互不替代。

## 实施边界

schema、共享校验、索引及应用适配使用同一来源 v3 合同。未知键、旧字段、错误形状和跨目录引用必须报错；不能跳过不完整依据。完整记录的结构合格不批准事实、归属或关系。原来源数据批次、来源收尾及术语采纳的权限保持，仅按本次决定列明的机械位置变换解释。

未核映射继续隔离；候选、诊断及历史账本不产生正式数据效力。临时导出不表示正式库同步、发版或内容消费者启用。恢复使用 Git，不设置长期兼容层。

## 建设流程

1. 从实际使用、阅读和已登记材料中列出需要一致命名的个体，并保留相应依据。
2. 逐条核对 Wikidata；有可核条目的记录现行映射，没有的保持空缺，不伪造映射。
3. 填写 `subjects`；无法挂接时回到主题词表判断是否缺少概念，不用来源字段替代归属判断。
4. 事实依据可使用已登记文献，或在事实依据限定字段使用直接官方链接。材料确实贡献设计且满足准入时，另按参考文献目录审阅，不为了记录官网地址建立书目。

## 校验规则

- subjects 指向现有主题，每个值由严格文献依据或项目判断覆盖；仍有归属项目判断的实体不得 active。vendor、creator、replaced_by 指向本表实体。
- id 按稳定身份比较，不以 label 代替，不复用 ID；历史只追加，原 added 不改为迁移日期。
- kind 使用已登记普通实体类别；来源专有字段不得进入本表。地址角色沿用已登记值，存在 urls 时有且仅有一个主项。
- 直接 URL 只适用于明确列出的事实字段，并与 reference 形式互斥；定位、真实核对日期与字段支持范围分别核对。
- match 指向获准 mapping 用途，依据只接受文献引用；决定必须对应实际对象、角色和状态，不只检查决定 ID 存在。
- 结构校验不批准外部事实、归属或关系；正式数据与消费者验收完成前不得合并，历史账本只作审计。

## 待定事项

- 类别是否需要更细，例如工具、框架和服务，以及应取哪些 Wikidata 类。
- 实体之间是否需要 `vendor` 以外的关系，例如依赖和兼容；这属于知识图谱问题，见[概念文](../../concepts/knowledge-graph.md)。
