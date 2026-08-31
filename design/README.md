# 设计文档索引

`design/` 中的现行设计规定本库当前使用的规则：词表怎样建立和分层、外部来源怎样使用、方法怎样登记、内容怎样建模。理论在 `concepts/`，文献笔记在 `sources/`。项目草案集中在 `design/drafts/`，全部未生效。

## 文章的关系

现行设计与项目草案分属两条分支。

- 现行设计
  - [方法登记](principles.md)：登记本库采用的方法、概念依据和导出的规则。
    - [写作规则](writing.md)：规定全库写作规则；`AGENTS.md` 是其摘要。
    - [主题词表设计](topics.md)：规定概念记录、关系、生命周期、建设流程和校验。
      - [层级结构](hierarchy.md)：规定树的分层、结构复制、数组和结构来源。
      - [来源名称规范表](sources-registry.md)：规定外部体系的登记、复制、映射和派生概念组。
    - [命名实体词表设计](entities.md)：规定产品、语言、组织、标准和文献等个体的记录方式。
    - [内容模型](content-model.md)：规定内容单元字段、受控值、标识符和应用映射接口。
      - [词表版本](versioning.md)：规定版本块、发版时机和变更记录。
      - 应用映射尚无可索引的项目文件；接口要求保留在内容模型中。
    - [治理](governance.md)：规定对象范围、政策、决策权、变更控制、验收、验证投入和审计。
      - [维护](maintenance.md)：规定对象、指标、阈值、触发、动作、审计追踪和复审。
  - [决定记录](decisions/)：保存已采纳决定，只追加不修改。
    - [树按学科而非分面的决定](decisions/tree-by-discipline.md)
    - [原样复制与本地分析分层的决定](decisions/borrow-and-analyze.md)
    - [设计与应用分离](decisions/form-independence.md)
    - [决策权的首批边界](decisions/decision-rights-defaults.md)
    - [项目约定入口](decisions/project-instructions-entry.md)
- 项目草案（未生效）
  - [来源治理](drafts/source-governance.md)：提出来源身份、用途、引用、复核和失效处理规则。
  - [术语治理](drafts/terminology-governance.md)：提出术语概念、多语形式、状态、委托和生成边界。
  - [划分特征的自定治理](drafts/division-characteristics.md)：提出划分特征的登记与复核；零自定例外尚未开放。
  - [分面字段草案](drafts/facet-field.md)：记录分面研究、模型职责和生效条件。
  - [概念组草案](drafts/concept-groups.md)：提出手工概念组的登记和规则。

草案分支中的文件全部未生效。阅读或引用草案不等于规则生效；现行规则仍以现行设计分支和正式数据为准。

## 词表一览

| 词表 | 文件 | 管什么 | 设计 |
|---|---|---|---|
| 主题词表 | `vocab/topics.yaml` | 概念；顶层概念可表示学科，概念之间构成层级树 | topics.md、hierarchy.md |
| 命名实体词表 | `vocab/entities.yaml` | 个体：产品、语言、组织、标准、文献 | entities.md |
| 来源名称规范表 | `vocab/sources.yaml` | 外部知识体系与词表 | sources-registry.md |
| 文档类型词表 | `vocab/types.yaml` | 内容单元的体裁，六类 | content-model.md |
| 体裁词表 | `vocab/genres.yaml` | 作者立场，IPTC genre 五类 | content-model.md |
| 载体词表 | `vocab/forms.yaml` | 呈现形式与教学活动，IEEE LOM 15 项加速查表 | content-model.md |
| 划分特征登记 | `vocab/characteristics.yaml`（未建） | 分析层数组的划分特征；草案，例外尚未开放 | drafts/division-characteristics.md |
| 手工概念组 | `vocab/groups.yaml`（未建） | 按用途圈的视图；草案 | drafts/concept-groups.md |

`vocab/` 初版 2026.08 已建，见 [CHANGELOG](../vocab/CHANGELOG.md)；`vocab/build/` 是生成输入，`scripts/build-topics.py` 生成，`scripts/check-topics.py` 校验。

## 阅读顺序

| 顺序 | 文章 | 读完知道 |
|---|---|---|
| 1 | [方法登记](principles.md) | 本库用了哪些方法，各自的依据 |
| 2 | [主题词表设计](topics.md) | 主题词表是什么、一条记录怎么写 |
| 3 | [层级结构](hierarchy.md) | 树怎么分层、从哪复制、借多深 |
| 4 | [来源名称规范表](sources-registry.md) | 外部体系怎么登记、三种用法 |
| 5 | [命名实体词表设计](entities.md) | 产品、语言、标准、文献为什么另立词表；分级 |
| 6 | [治理](governance.md) | 谁决定、按什么政策、怎么审计 |
| 6a | [维护](maintenance.md) | 信号、阈值、动作、周期：词表和内容怎么随时间保持可信 |
| 7 | [写作规则](writing.md) | 写任何文件前要遵守什么 |
| 8 | [内容模型](content-model.md) | 一条内容单元有什么、id 怎么取 |
| 9 | [词表版本](versioning.md) | 什么时候发版、记什么 |
| — | [决定记录](decisions/) | 已采纳决定及其后果 |
| — | 项目草案：[来源治理](drafts/source-governance.md)、[术语治理](drafts/terminology-governance.md)、[划分特征的自定治理](drafts/division-characteristics.md)、[分面字段草案](drafts/facet-field.md)、[概念组草案](drafts/concept-groups.md) | 五份均未生效；阅读草案不等于规则生效 |
