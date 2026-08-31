# 命名实体词表设计

`vocab/entities.yaml` 是本库的名称规范表（name authority list），收软件产品、编程语言、组织、标准和文献等个体。主题词表管理概念，例如“AI 编程助手”和“关系型数据库”；命名实体词表管理个体，例如 Claude Code、PostgreSQL、Anthropic、ISO 25964-1:2011 和 Cockburn 2005 年的博文。

ISO 25964-2 §23 把名称规范表定义为为一致命名特定实体而建立的受控词表；实体是唯一的个体，不与主题概念建立等价映射。理论见[受控词表](../concepts/controlled-vocabulary.md)和[词表映射](../concepts/vocabulary-mapping.md)。

正式 `vocab/entities.yaml` 仍是现行旧形状。来源实体的新模式和维护接口已经实现，但尚未应用到正式数据；来源治理草案仍未生效。

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

## 现行记录

一般实体记录当前以 `id`、`label`、`kind`、`subjects`、`status` 和 `added` 为共同字段，并按对象需要保存 `alt`、`vendor`、`creator`、`form`、`scope`、`basis`、`match` 或 `replaced_by`。现行数据形状由正式 YAML 和现行校验链决定，本次同步不增加、删除或改名字段。

正式数据中的 Claude Code 记录如下。

```yaml
- id: claude-code
  label: { zh: Claude Code, en: Claude Code }
  kind: software
  form: command-line interface
  vendor: anthropic
  subjects: [artificial-intelligence, tools-and-environments]
  basis:
    subjects: cs2023:SE-Tools#7
  scope: Anthropic 的命令行编程智能体；不含 Claude 模型本身
  match: [{ source: wikidata, id: Q138457287, rel: exactMatch }]
  status: active
  added: 2026-08-23
```

人工赋值字段继续按[维护](maintenance.md)的现行断言规则记录依据。designation 的形式依据、概念对应依据和具体断言依据互不替代；本次同步不改变这三道门禁。

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

`standard` 和 `publication` 同时承担来源实体身份。正式记录当前仍保存 `id`、名称、类别、`tier`、版本、单个 `url`、核对日期、可选的标量 `watch`、主题关系、现行 `status` 和添加日期。来源在实体表只登记一次；[来源名称规范表](sources-registry.md)以 `entity` 指向它，只保存现行用途。

来源身份、用途资格和具体关系彼此独立。实体记录存在，不表示它具有任何未登记用途；用途记录存在，也不表示某个具体断言、实际派生或概念映射成立。

`publication` 另以 `creator` 指向一个或多个 `person` 或 `organization` 实体。`standard` 的 `version` 保存所引版本，`checked` 保存上次核对日期；`watch` 对 `de-jure` 必填，现行值是新版探测页面。单个 `url` 和标量 `watch` 都是正式旧形状，不等于后置结构化地址或真实联网探测已经可用。

### 来源分级

`tier` 对 `standard` 和 `publication` 必填，其余类别不填。分级依据来源如何变更：权威程度决定能否引用，变更方式决定复核周期；按 Z39.19 §5.3.5.2，这属于组织依据。复核周期见[维护](maintenance.md)。

| tier | 含义 | 适用 |
|---|---|---|
| `de-jure` | 有正式发布流程和版本标识，变更必出新版 | ISO、GB/T、W3C Recommendation、RFC |
| `de-facto` | 行业默认，无发布流程，或版本可无通知漂移 | CS2023、SWEBOK、ASVS、CWE、MDN、W3C 草案 |
| `vendor` | 单一厂商文档，随产品迭代 | Anthropic 文档、Neo4j 文档 |
| `archival` | 发表后内容固定 | 论文、书、博文、issue、演讲 |

同一发布方可以跨档：W3C Recommendation 是 `de-jure`，Working Draft 是 `de-facto`；Wikidata 数据是 `de-facto`，引用它的论文是 `archival`。全部现行 `tier` 值保持不变。

`tier` 当前继续承担分级和复核周期含义，但不等于来源的外部状态，也不能单独推出 `mapping`、`structure`、`group` 或发现用途。正式迁移后的用途资格由用途记录的角色决定；这项后置规则不回写当前 `tier`。

### 生命周期

一般实体记录继续使用 `candidate`、`active` 和 `deprecated`，规则见[主题词表设计](topics.md)。本表没有 `unassigned`：它不复制结构，每条记录都按实际使用或阅读依据建立。

产品停止维护或被替代时转为 `deprecated`，`replaced_by` 在有替代品时指向替代实体；记录不删。来源实体正式数据当前也继续使用这套旧 `status` 形状；后置接口中的外部状态不能提前写入正式记录。

## 映射关系

实体的主要映射目标是 Wikidata：它为软件、语言、组织、标准和出版物提供稳定 Q 号，并记录厂商、发布日期、官网和 DOI 等属性，本表不重复保存。厂商文档只作为地址或断言依据，不因此成为映射目标。

正式记录当前继续使用 `match: [{ source, id, rel }]`，其中 `source` 必须是正式来源名称规范表中具有现行 `mapping` 用途的 id。没有可核映射时不伪造条目，`match` 留空并按现行生命周期处理。

共享 `match` 的严格结构已经实现，后置字段为 `registry`、`item`、`rel` 和相邻 `basis`，并要求对应用途记录具有经决定批准的 `mapping` 角色。正式数据尚未迁移，具体角色和逐条映射依据也尚未批准；因此严格结构不能当作当前正式记录示例。

## 主题职责

- 内容单元的 `subject` 填主题概念，`entities` 填实体，见[内容模型](content-model.md)。
- “Rust 的所有权”使用 `subject: [systems-execution-and-memory-model]` 和 `entities: [rust]`；具体语言不进入主题树。
- 一个实体的 `subjects` 可以有多个；主题概念不反向记录实体，需要时由脚本计算某主题下的全部实体。
- 全库标准或全库文献由本表按 `kind` 查询，不需要主题词表的分面字段。
- 通用 `origin` 不再是主题目标字段。来源实体只提供可解析身份；发现观察、具体值依据、实际派生和概念映射各自记录，互不替代。

## 后置接口

来源实体 v2 模式已经区分结构化地址、外部状态、字段级 `basis`、`review`、结构化 `watch`、`replaced_by` 和只追加 `history`。外部状态只描述发布方体系中的 `current`、`superseded` 或 `withdrawn`，不描述项目是否批准使用；暂时不可访问也不等于撤回。

该模式、离线校验和反向索引已经存在，但尚未应用到正式 `vocab/entities.yaml`。真实地址、外部状态、复核日期、观察入口、替代关系和逐字段依据仍须逐项决定。`source-entities` schema 对一般实体已有的 `alt`、`subjects`、`vendor`、`scope`、`creator`、`form` 和 `added` 等字段尚未形成覆盖整个正式实体文件的闭合契约；在该边界解决前，不能把它写成全表已经可以严格切换。

固定夹具探测只能读取后置 `watch` 和地址结构，生成复核信号，不修改正式字段。`--live` 禁用，探测输出与探测 schema 尚未闭合；没有真实来源状态因此得到确认。

## 建设流程

1. 从实际使用、阅读和已登记材料中列出需要一致命名的个体，并保留相应依据。
2. 逐条核对 Wikidata；有可核条目的记录现行映射，没有的保持空缺，不伪造映射。
3. 填写 `subjects`；无法挂接时回到主题词表判断是否缺少概念，不用来源字段替代归属判断。
4. 对作为来源使用的 `standard` 或 `publication`，先在实体表保存身份，再在来源名称规范表保存现行用途；不由身份、`tier` 或地址自动推出用途。

## 校验规则

- 现行主题链继续检查 `subjects` 指向正式主题概念，`vendor` 和 `replaced_by` 指向本表实体，`kind` 属于已登记类别，标签与别名不重复，以及废弃记录保留历史。
- 现行 `match.source` 必须指向正式用途记录；无法确认外部概念时不建立映射。
- 来源 schema、共享引用校验和反向索引只验证已经进入严格形状的结构与引用，不修改来源事实，也不替代人工判断。
- `check_sources.py` 尚未成为当前正式旧数据的通过门禁；不能把模式能力写成正式实体文件已经切换。
- 迁移账本只保存历史库存、分类和阻断，不把推荐值应用到正式实体；当前 HEAD 也不能重放原冻结快照的预演结果。

## 待定事项

- 类别是否需要更细，例如工具、框架和服务，以及应取哪些 Wikidata 类。
- `publication` 中 issue 和演讲对应的 Wikidata 类。
- 实体之间是否需要 `vendor` 以外的关系，例如依赖和兼容；这属于知识图谱问题，见[概念文](../concepts/knowledge-graph.md)。
