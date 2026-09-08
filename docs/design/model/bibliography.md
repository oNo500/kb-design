# 参考文献目录

`data/references/bibliography.yaml` 保存为 kb-design 的模型、规则、词表结构或术语采纳提供实际依据的文献身份。软件、组织、编程语言等涉及对象由[命名实体词表](entities.md)管理；文献的获准用途由[来源用途登记](sources-registry.md)管理。目录不属于新增受控词表。

## 收录范围

每项新文献须能指出支持的具体设计对象与引用位置。标准、规范、知识体系、书籍、论文和文档按实际贡献审阅；被笔记引用、来自官网或出现在 basis 中，都不单独构成准入理由。普通笔记的参考资料直接保存标题与链接，无须先进入本目录，两者不自动导入。

已有候选、未核材料和历史采纳来源随原状态保留，供审计与后续复核；迁移不提升状态、补足证据或授予用途。本批对象及机械位置变换以[参考文献分离](../../decisions/source-bibliography-separation.md)列明范围为准。误增的 uv-docs、npm-docs、fnm-docs 不进入目录，其普通实体事实改用逐项核对的官方 URL；正文引用链接不因此删除。

## 文献身份

根键为 schema、schema_version、version、references，schema 为 `urn:kb-design:data:bibliography`。references 保存文献记录；文献 ID、名称、原添加日期和既有历史保持稳定，名称或存放位置变化不产生新身份。共同字段包括 id、label、kind、subjects、status、added；名称及别名沿用各自的准入限制，subjects 的逐值依据和项目判断按[实体归属依据](entities.md#归属依据)核对。

kind 保留原 standard／publication 值的历史语义，form 保留已有形式；不能把厂商文档的旧 standard 值自动解释为标准组织发布的技术标准。原 standard 登记的 Q317623、publication 登记的 Q591041 及下位 Q13442814、Q571、Q17928402 只保留原分类依据，不为厂商文档补作类归属结论。文献类型重新建模须另行采纳。creator 或 vendor 仅在确有对应实体时指向实体词表；不为补齐作者字段自动收录人员，人员仍受[人员收录规则](entities.md#类别)约束。replaced_by 指向本目录文献，不能指向普通实体。

这些路径、字段形状和拆表方式是本项目的表示选择，不宣称由外部标准规定。文献身份登记不等于实际设计使用已获批准；具体字段、依据与权限仍按各自决定核验。

## 文献记录

来源用途以[用途记录](sources-registry.md)的 reference 指向文献。文献记录必须有 tier、version、urls、basis、review、watch、replaced_by 和 history。source_status 可省略；[来源数据批次](../../decisions/source-data-batch.md)取代原字段合同的外部状态必填条件。必填结构不授权填写默认事实。

source_status 已填写时只取 current、superseded、withdrawn，表示发布方体系中的外部状态，必须有发布者依据与精确字段采纳；原项目 status 保留。省略只表示“外部状态未核实”，不是 current、不是“不适用”，不新增 unknown。不能删除已有合格结论逃避核验；确实依赖外部现行状态的操作在缺值时仍阻断。暂时不可访问不等于 withdrawn，普通实体不能填写 source_status。

version 必须有该键，可以为非空版本字符串或 null。null 只表示“未登记可核实版本”，不声称发布者没有版本。未经核实的旧 rolling、月份或其他版本值留在 history.before；不得用抓取日期制造版本。填写的版本值仍须对应材料与采纳范围，非空替代关系另有依据。缺外部状态不自动否定已核具体材料，但逐条引用、用途资格和关系采纳均不能省略。无版本的 de-facto 仍不能取得 structure 资格。

urls 使用 canonical、landing、doi、full_text、status、mirror、archive 七种地址角色，恰好一个 primary。旧 url 的角色须明确判断。publication 的 creator 指向作者或组织；版本与真实固定内容哈希 fixed_sha256 共同确定内容时，引用依据才可按规则省略 checked。

review 保存 checked、next_due、interval_months、grace_days、obligations。旧顶层 checked 保存在迁移 history.before，只有核对对象与范围得到确认后才能成为 review.checked；逐字段依据的 checked 独立保留。history 记录真实迁移动作、日期、字段、决定与前后值，不制造历史复核。

watch 每项包含 locator、signals、cadence_months。locator 是观察地址；signals 为 availability、redirect、version、revision、replacement、withdrawal 的非空无重复列表；cadence_months 明确 availability、redirect、content 三种周期。地址及重定向按月，内容按 de-jure／de-facto／vendor／archival 分别为 1／3／6／12 个月。旧标量 watch 不自动证明观察条目已核准；没有旧入口也不等于已批准无需观察。

## 来源分级

`tier` 对文献记录必填，普通实体不填。分级依据来源如何变更：权威程度决定能否引用，变更方式决定复核周期；按 Z39.19 §5.3.5.2，这属于组织依据。复核周期见[维护](../governance/maintenance.md)。

| tier | 含义 | 适用 |
|---|---|---|
| `de-jure` | 有正式发布流程和版本标识，变更必出新版 | ISO、GB/T、W3C Recommendation、RFC |
| `de-facto` | 行业默认，无发布流程，或版本可无通知漂移 | CS2023、SWEBOK、ASVS、CWE、MDN、W3C 草案 |
| `vendor` | 单一厂商文档，随产品迭代 | Anthropic 文档、Neo4j 文档 |
| `archival` | 发表后内容固定 | 论文、书、博文、issue、演讲 |

同一发布方可以跨档：W3C Recommendation 是 `de-jure`，Working Draft 是 `de-facto`；Wikidata 数据是 `de-facto`，引用它的论文是 `archival`。既有来源的 `tier` 不因术语迁移改变；新增来源按[术语来源采纳](../../decisions/source-term-complete-citations.md)的具体记录登记。

`tier` 当前继续承担分级和复核周期含义，但不等于来源的外部状态，也不能单独推出 `mapping`、`structure`、`group` 或发现用途。正式迁移后的用途资格由用途记录的角色决定；字段合同不改变现有 `tier`。

## 项目状态

status 使用 candidate、active、deprecated，表示本项目记录状态。source_status 表示发布方外部状态，两者独立；外部 superseded 不自动废弃记录或批准替代材料。删除、来源改档和非候选对象退出仍由人决定，历史只追加，ID 不复用。

## 引用依据

文献依据使用 reference、locator，以及按内容可变性要求的 checked。reference 只指向本目录；registry 只指向用途登记。可变材料保留真实核对日期，仅固定版本与真实内容哈希共同确定内容时可省略 checked。严格依据不接受旧 entity 或直接 URL 后备，普通实体事实的有限 URL 入口见[实体依据](entities.md#事实依据)。

逐字段依据证明指定事实，不批准文献准入、来源用途、实际派生或具体映射。语言依据 references.source 保持[独立合同](topics.md#语言依据)，不得因名称相近批量改写。

## 维护边界

来源相关六份词表与本目录使用 schema_version 3，术语概念模型版本不因此改变。严格入口拒绝旧字段和跨目录引用，不提供双格式兼容。旧决定与历史 before／after 按原 Git 基线解释；只有新采纳记录列明的机械身份与字段映射可用于解释原授权，不能扩大状态、角色、具体值或限定许可。

复核按[维护](../governance/maintenance.md)执行。观察与反向索引只提供线索，不自动回写事实；正式义务、周期任务、持久正式索引和内容消费者不因目录存在而启用。固定夹具不能确认真实外部状态，live 探测未由本次分离开放。

应用将文献输出到独立参考区域，具体路径与引用表示由 target 决定。普通刷新不扩展用户内容写集；旧内容链接只能由另行列明写集的一次性迁移调整。实现、临时导出、正式库同步和发版分别验收，不由 schema 通过推导。恢复使用明确范围的 Git；外部 vault 与 Git 忽略输出另保留备份。

## 待定事项

- 文献类型的重新建模，以及 issue、演讲等材料的具体类别。
- 未核版本、外部状态与既有候选材料的后续实质复核。
