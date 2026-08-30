# 设计文档索引

`design/` 是本库的规则：词表怎么建、怎么分层、外部来源怎么用、方法怎么登记。理论在 `concepts/`，文献笔记在 `sources/`。没有外部依据、尚未生效的设计在 `drafts/`。

## 文章的关系

```
方法登记 principles.md          本库采用的每个方法:来源、概念文、导出的规则在哪
│
├─ 写作规则 writing.md          全库写作规则,按 ISO 24495-1 四原则组织;AGENTS.md 是其摘要
│
├─ 主题词表 topics.md           一条概念记录长什么样、生命周期、建设流程、校验
│   ├─ 层级结构 hierarchy.md    树怎么分层、复制规则、各概念下的来源、结构预览
│   └─ 来源名称规范表 sources-registry.md   外部体系作为词表来源怎么用、match 怎么写
│
├─ 命名实体词表 entities.md     产品、语言、组织、标准、文献:个体不进主题树,通过 subjects 挂主题
│
├─ 内容模型 content-model.md    一条内容单元有什么字段、文档类型词表、id 规则、应用映射的要求
│   ├─ 词表版本 versioning.md    版本块、变更记录
│   └─ targets/                  各应用的映射(待建)
│
├─ 治理 governance.md           对象范围、政策、决策权、变更控制、质量与验收、审计、风险
│   └─ 维护 maintenance.md  对象、信号、阈值、触发、动作、记录、周期；来源复核、编辑审核、断言依据、剩余监控
│
├─ decisions/                    决定记录,只追加不修改
│   ├─ tree-by-discipline.md     顶层为什么按学科不按分面
│   ├─ borrow-and-analyze.md     原样复制为底、本地分析在上
│   ├─ form-independence.md      设计与应用分离
│   ├─ decision-rights-defaults.md  决策权的首批边界；首次越权事件
│   └─ project-instructions-entry.md 项目约定的文件入口
│
└─ drafts/                       未生效,各自写明触发条件
    ├─ division-characteristics.md   零自定的唯一例外:划分特征的治理
    ├─ facet-field.md            分面字段:取值、触发条件
    └─ concept-groups.md         手工概念组:登记、规则
```

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
| — | [decisions/](decisions/) | 已采纳决定及其后果 |
| — | [drafts/](drafts/) | 按需 |
