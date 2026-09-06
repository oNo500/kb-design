# 命名实体词表

`data/vocab/entities.yaml` 是本库的名称规范表（name authority list），收软件产品、编程语言、组织、标准和文献等个体。主题词表管理概念，例如“AI 编程助手”和“关系型数据库”；命名实体词表管理个体，例如 Claude Code、PostgreSQL、Anthropic、ISO 25964-1:2011 和 Cockburn 2005 年的博文。

ISO 25964-2 §23 把名称规范表定义为为一致命名特定实体而建立的受控词表；实体是唯一的个体，不与主题概念建立等价映射。理论见[受控词表](../../concepts/controlled-vocabulary.md)和[词表映射](../../concepts/vocabulary-mapping.md)。

本文采用已采纳的[来源字段合同](../../decisions/source-v2-field-contract.md)。实体记录按该合同及[来源收尾](../../decisions/source-completion.md)的逐项采纳范围实施；结构合格不表示额外事实、用途角色或正式切换已经获准。严格工具只接受新格式，旧数据由 Git 与迁移审计保留，不提供兼容读取。

## 对象分工

主题词表和命名实体词表分别管理概念与个体，不另设数据类别。

| 比较项 | 主题词表 | 命名实体词表 |
|---|---|---|
| 管理对象 | 概念 | 个体：产品、语言、组织、标准、文献 |
| 变化速度 | 几年一版 | 产品一年可发布多个版本，也可能停止维护 |
| 结构 | 层级树 | 扁平；实体之间只保留已定义的关系 |
| 外部依据 | 知识体系、标准 | 厂商文档、出版物、Wikidata |
| 相互关系 | 不记录实体 | 每个实体通过 `subjects` 挂到一个或多个主题概念，不占树的位置 |

概念与个体混在一棵树中，会让稳定结构随易变对象移动。一个产品还可能关联多个主题；`subjects` 的多值关系表达这种挂接。

## 实体记录

实体共同字段为 `id`、`label`、`kind`、`subjects`、`status` 和 `added`。`status` 继续表示项目记录状态，不能被来源外部状态覆盖。`id` 保持稳定；名称变化不改变身份。一般实体与来源实体共用同一实体文档，schema 对两者的字段均显式约束。

| 字段 | 表示与条件 |
|---|---|
| `label`、`alt`、`hidden` | 按语言保存名称与可选别名；不因迁移取得新的 designation 准入 |
| `subjects` | 无重复的主题 ID 列表，每个值均有归属依据或明确项目判断 |
| `scope`、`form` | 保留范围与已登记形式，不从缺失证据推导新类别 |
| `vendor`、`creator` | 分别为实体 ID 和实体 ID 列表；目标可以是一般实体，不限于来源 |
| `urls` | role、url、primary 条目；一般实体官网不因登记地址取得来源身份 |
| `match` | registry、item、rel、basis；具体映射与用途资格分别核对 |
| `replaced_by`、`history` | 保留替代指向和只追加历史；删除或改身份仍受决定约束 |
| `added` | 原项目添加日期，不改为迁移日期 |

### 归属依据

外部 `basis.subjects` 是条目列表，每项为 `values` 与 `references`。values 明确列出受到支持的 subjects；references 是非空的严格依据列表，每项包含 entity、locator，以及按可变性要求的 checked。同一材料支持多个值时可以共用一组 values，但不得从记录级旧字符串自动推导逐值支持范围。

原 `self` 判断保存在 `assertions.subjects`，每项包含 values、`disposition: project_assertion`、`original: self` 和 migration 审计定位。它保存项目判断，不能充当外部依据；具有这类归属判断的实体不得为 active。basis 与 assertions 的 values 合集必须覆盖 subjects，且不能包含不属于该记录的主题。

紧凑引用只在核对材料、定位和支持范围后转为严格依据。未核对原值保留在迁移审计，不能装入 assertions 冒充已处置的项目判断，也不能清空依据使正式切换通过。人工判断、designation 的形式依据和概念对应依据分别按[维护](../governance/maintenance.md)与[治理](../governance/governance.md)处理。

### 类别

`kind` 只取已登记的 Wikidata 类，不自定。

| kind | Wikidata | 例 |
|---|---|---|
| `software` | Q7397 software | Claude Code、PostgreSQL、Neo4j |
| `programming-language` | Q9143 programming language | Python、Rust、TypeScript |
| `organization` | Q43229 organization | Anthropic、MITRE、W3C |
| `standard` | Q317623 technical standard | ISO 25964-1:2011、RFC 9110、ASVS 5.0、Anthropic 文档 |
| `publication` | Q591041 scientific publication 及其下位：Q13442814 scholarly article、Q571 book、Q17928402 blog post；issue、演讲的类待核 | Hogan 2021、Aitchison 的教材、Cockburn 2005 年的博文 |
| `person` | Q5 human | Ranganathan、Wüster、Hogan、Cockburn |
| `large-language-model` | Q115305900 large language model | Claude Opus 4、GPT-4 |

需要更多类别时从 Wikidata 取，并记录 Q 号。`publication` 的具体形式记在 `form`，值是 Wikidata Q 号或其 slug。

`person` 只收在相关主题或活动中有显著公开角色的公众人物（public figure，*Gertz v. Robert Welch* 1974 的意义）：已发表作品的作者、公开项目的维护者或方法的提出者，并且有 Wikidata 条目或可引用的公开出处。相关主题或活动只限定公开角色的判断范围，不形成新的数据类别。不收私人、同事或联系人。文献实体用 `creator` 指向人，软件实体的个人维护者用 `vendor` 指向人。

### 来源记录

`standard` 和 `publication` 承担来源实体身份，来源用途以[用途记录](sources-registry.md)的 entity 指向它。来源实体还必须有 tier、version、urls、basis、review、watch、replaced_by 和 history。source_status 可省略；[来源数据批次](../../decisions/source-data-batch.md)取代原字段合同的外部状态必填条件。必填结构不授权填写默认事实。

source_status 已填写时只取 current、superseded、withdrawn，表示发布方体系中的外部状态，必须有发布者依据与精确字段采纳；原项目 status 保留。省略只表示“外部状态未核实”，不是 current、不是“不适用”，不新增 unknown。不能删除已有合格结论逃避核验；确实依赖外部现行状态的操作在缺值时仍阻断。暂时不可访问不等于 withdrawn，一般实体不能填写 source_status。

version 必须有该键，可以为非空版本字符串或 null。null 只表示“未登记可核实版本”，不声称发布者没有版本。未经核实的旧 rolling、月份或其他版本值留在 history.before；不得用抓取日期制造版本。填写的版本值仍须对应材料与采纳范围，非空替代关系另有依据。缺外部状态不自动否定已核具体材料，但逐条引用、用途资格和关系采纳均不能省略。无版本的 de-facto 仍不能取得 structure 资格。

urls 使用 canonical、landing、doi、full_text、status、mirror、archive 七种地址角色，恰好一个 primary。旧 url 的角色须明确判断。publication 的 creator 指向作者或组织；版本与真实固定内容哈希 fixed_sha256 共同确定内容时，引用依据才可按规则省略 checked。

review 保存 checked、next_due、interval_months、grace_days、obligations。旧顶层 checked 保存在迁移 history.before，只有核对对象与范围得到确认后才能成为 review.checked；逐字段依据的 checked 独立保留。history 记录真实迁移动作、日期、字段、决定与前后值，不制造历史复核。

watch 每项包含 locator、signals、cadence_months。locator 是观察地址；signals 为 availability、redirect、version、revision、replacement、withdrawal 的非空无重复列表；cadence_months 明确 availability、redirect、content 三种周期。地址及重定向按月，内容按 de-jure／de-facto／vendor／archival 分别为 1／3／6／12 个月。旧标量 watch 不自动证明观察条目已核准；没有旧入口也不等于已批准无需观察。

### 来源分级

`tier` 对 `standard` 和 `publication` 必填，其余类别不填。分级依据来源如何变更：权威程度决定能否引用，变更方式决定复核周期；按 Z39.19 §5.3.5.2，这属于组织依据。复核周期见[维护](../governance/maintenance.md)。

| tier | 含义 | 适用 |
|---|---|---|
| `de-jure` | 有正式发布流程和版本标识，变更必出新版 | ISO、GB/T、W3C Recommendation、RFC |
| `de-facto` | 行业默认，无发布流程，或版本可无通知漂移 | CS2023、SWEBOK、ASVS、CWE、MDN、W3C 草案 |
| `vendor` | 单一厂商文档，随产品迭代 | Anthropic 文档、Neo4j 文档 |
| `archival` | 发表后内容固定 | 论文、书、博文、issue、演讲 |

同一发布方可以跨档：W3C Recommendation 是 `de-jure`，Working Draft 是 `de-facto`；Wikidata 数据是 `de-facto`，引用它的论文是 `archival`。全部现行 `tier` 值保持不变。

`tier` 当前继续承担分级和复核周期含义，但不等于来源的外部状态，也不能单独推出 `mapping`、`structure`、`group` 或发现用途。正式迁移后的用途资格由用途记录的角色决定；字段合同不改变现有 `tier`。

### 生命周期

全部实体的 status 使用 candidate、active、deprecated，规则见[主题词表](topics.md)。实体不使用 unassigned，因为它不为补全复制结构建立。

产品停止维护或被替代时，项目是否废弃记录按现行决定权限处理；有替代对象时记录 replaced_by，历史记录不删。来源实体的 source_status 与这套项目状态独立。外部 superseded 不自动把项目记录转为 deprecated，也不自动批准替代来源。

## 映射关系

实体的主要映射目标是 Wikidata；厂商文档可作为地址或具体事实依据，不因此成为映射目标。严格 match 使用 registry、item、rel、basis，registry 指向获准 mapping 角色的用途记录，item 保存外部标识或永久地址，basis 与每条关系相邻。

旧 match.source／id 不在严格读取中保留。旧关系名称、相同标签和用途存在均不能代替具体身份或概念对应证据。未核关系原则上阻断相应正式转换。[来源收尾](../../decisions/source-completion.md)明确采纳的 17 条隔离关系除外：旧关系、来源、旧值与结论保存在该决定的隔离清单和 Git 历史，不进入正式 match；对象、标签、项目状态和其他关系保留。该例外不为其补造依据，也不授权其他关系静默省略。

Pydantic 保持同一软件实体，scope 描述软件身份；version: "2" 单独表示项目选用的主要版本，不将版本范围当作另一个软件身份。OpenClaw 的 subjects 按[来源收尾](../../decisions/source-completion.md)只保留 artificial-intelligence；这是本批依据支持范围的取舍，不表示它不能编程，也不改变实体或 active 状态。

## 主题职责

- 内容单元的 `subject` 填主题概念，`entities` 填实体，见[内容模型](content-model.md)。
- “Rust 的所有权”使用 `subject: [systems-execution-and-memory-model]` 和 `entities: [rust]`；具体语言不进入主题树。
- 一个实体的 `subjects` 可以有多个；主题概念不反向记录实体，需要时由脚本计算某主题下的全部实体。
- 全库标准或全库文献由本表按 `kind` 查询，不需要主题词表的分面字段。
- 通用 `origin` 不再是主题目标字段。来源实体只提供可解析身份；发现观察、具体值依据、实际派生和概念映射各自记录，互不替代。

## 实施边界

来源字段合同已经采纳，schema、共享校验、索引及应用适配按同一 v2 合同实施。工具发现旧字段、未知键、错误形状或未获准引用时必须报错，不能因为引用形状不完整而跳过。

完整记录与逐条引用的采纳范围由来源数据批次和[来源收尾](../../decisions/source-completion.md)分别限定。P1–P4 只采纳列明字段，不能作为完整来源合格的证明；来源 v2 数据与严格读取已实施，但生成与临时导出不表示合并、发版或正式消费者启用。正式义务、持久正式索引和消费者不能由接口存在推导。

固定夹具探测提供观察证据，不确认真实外部状态；live 探测与正式周期运行不由字段合同开放。恢复使用 Git，不设置补偿回滚或长期兼容层。

## 建设流程

1. 从实际使用、阅读和已登记材料中列出需要一致命名的个体，并保留相应依据。
2. 逐条核对 Wikidata；有可核条目的记录现行映射，没有的保持空缺，不伪造映射。
3. 填写 `subjects`；无法挂接时回到主题词表判断是否缺少概念，不用来源字段替代归属判断。
4. 对作为来源使用的 `standard` 或 `publication`，先在实体表保存身份，再在来源名称规范表保存现行用途；不由身份、`tier` 或地址自动推出用途。

## 校验规则

- subjects 指向现有主题，其每个值被严格依据或项目判断覆盖；vendor、creator、replaced_by 指向本表实体。
- id 按稳定身份比较，不能以 label 代替身份；历史只追加，禁止复用 ID。
- kind 使用已登记类别；status 与 source_status 分开；一般实体不要求来源字段，也不接受外部状态。
- 地址有且仅有一个主项；依据定位、核对日期、字段支持范围和角色决定分别检查。外部状态缺省与 version: null 分别保留明确的未核实含义；已填写状态和版本继续核对依据及精确采纳。
- 严格 match 指向获准 mapping 用途，角色决定必须对应实际对象、角色与状态，不能只检查决定 ID 存在。
- 全表新格式校验通过不等于外部事实或归属判断已获采纳；未知字段和旧结构不得放宽。
- 正式数据迁移与消费者验收完成前不得合并主分支；历史账本只作审计。

## 待定事项

- 类别是否需要更细，例如工具、框架和服务，以及应取哪些 Wikidata 类。
- `publication` 中 issue 和演讲对应的 Wikidata 类。
- 实体之间是否需要 `vendor` 以外的关系，例如依赖和兼容；这属于知识图谱问题，见[概念文](../../concepts/knowledge-graph.md)。
