# 术语设计

本项目的术语记录区分概念、定义、语言和具体名称，各自保存身份、依据、状态与历史。现行结构来自[术语结构采纳](decision-term-complete-structure.md)和[术语具体值](decision-term-data-values.md)，编辑源及参考消费按[术语发布条件](decision-term-complete-publication.md)启用。概念解释见[术语数据库](terminology-database.md)。

## 对象分工

| 对象 | 职责 |
|---|---|
| 术语概念 | 共享概念身份、定义、适用学科、工作流与历史 |
| 语言记录 | 在同一概念内按语言组织具体术语 |
| 术语形式 | 具体名称、管理状态、依据及替代关系 |
| 展示布局 | 章节、引用说明、符号和已批准历史名称的展示 |
| 生成参考 | 面向读者呈现已登记名称、定义及依据 |

主题标签和载体标签仍由其原编辑源维护。术语记录不复制全部词表标签，同形名称不证明概念相同，也不产生委托。术语身份不进入现行内容模型的主题受控值。

## 记录结构

`data/vocab/terms.yaml` 是概念、定义与术语形式的唯一编辑源，顶层为 `schema`、`version` 和 `concepts`。

| 字段 | 含义 |
|---|---|
| `id` | 术语概念的稳定身份，采用 `tc-*` UUIDv4 |
| `subject_fields` | 适用学科及逐值依据 |
| `definitions` | 带语言的定义及其依据 |
| `languages` | 语言分组，每组包含 `language` 和 `terms` |
| `basis` | 概念身份和多语对应的依据 |
| `source`、`match` | 可选的实际派生与外部映射，服从共享来源合同 |
| `workflow`、`history` | 概念工作流及只追加的真实变更 |

语言值域限于当前 schema 的 `en`、`zh-Hans`、`zh-Hant`。每个术语形式有独立的 `tm-*` UUIDv4、`text`、`administrative_status`、`basis`、条件使用的 `replaced_by` 和历史。身份一经采纳保留，重建不重新分配；并列的多语记录仍需概念对应依据。

## 状态与依据

概念工作流与术语管理状态分别判断。现行术语管理状态包括 `preferredTerm-admn-sts`、`admittedTerm-admn-sts`、`deprecatedTerm-admn-sts` 和 `supersededTerm-admn-sts`；历史形式保留不等于当前准用。状态合法不代表已取得转换或准入授权。

外部概念、定义、学科归属和语言形式分别核对。六个概念的限定定义依据按[限定定义许可](decision-term-limited-definition-source-use.md)逐项处理，不扩大为其他概念或来源的一般许可。

项目依据只覆盖内容单元、断言、阈值的既有概念与定义，以及 assertion、threshold 两个既有英文形式。每项须有有效 L3 完整记录及精确范围，历史位置不构成第二编辑源。模型知识译名须保留模型判断、实际采纳和“外部用法未核实”声明。

## 编辑与生成

概念、定义和名称在 `terms.yaml` 修改；`data/inputs/terminology/glossary-layout.yaml` 管理展示。主题和载体的模型标签仍由各自输入及 `label-adoptions.json` 管理，名称相同不转移所有权。

`kb-core term-data` 校验记录并定位引用；`build-terms` 按已校验快照生成与核对参考。`docs/glossary.md` 只读，不能直接编辑。命令参数见[核心工具](../../../packages/kb-core/README.md)。

## 消费边界

现行启用范围是 glossary 生成与首批应用术语参考读取。它不新增内容术语字段，不启用词表标签委托、正式复核义务、持久正式索引或 TBX，也不自动写入外部正式知识库。正文诊断仅提供人工复核线索。

未来委托与复核问题见[术语治理提案](proposal-terminology-governance.md)，交换需求见[术语交换提案](proposal-tbx-export.md)。提案未整体生效。
