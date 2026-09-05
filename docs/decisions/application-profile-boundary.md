# 应用约束与表示分层

状态：已采纳，2026-09-01。

## 背景

现行内容模型保持应用无关，Obsidian 映射同时记载应用语义、具体表示和导出物化。若不区分这些职责，target 的载体限制会反向改写共同语义，局部序列化或完整性证据也可能被扩大成消费者启用或外部符合性声明。

[设计与应用分离](form-independence.md)已经确定应用无关层与应用相关层分开，并规定 `vocab/` 是应用导出的源。该决定继续有效；本决定补充 `Application Profile`、导出 artifact contract 和真实消费者之间的边界。

## 决定

### 模型边界

保留应用无关内容模型；每个 target 另写功能范围、模型引用、字段约束、使用指南和具体表示。`Application Profile` 负责具体表示的语义选择与约束，即哪个字段使用哪个 target location、type 和 reference form，以及允许何种 loss。

### 表示关系

Obsidian field／property／path 关系称普通 binding／表示规则，不称 `metadata crosswalk`；本项只排除这一 metadata 用语，不改变现行词表层 `crosswalk`。

### 导出职责

导出 artifact contract 与 `Application Profile` 分开。`Application Profile` 负责语义层的 target 表示选择与约束，即哪个字段使用哪个 target location、type 和 reference form，以及允许何种 loss；导出 artifact contract 负责已选表示的确定性物化及其输入边界，即输入快照、byte serialization、order、quoting、newlines、file set、manifest、post-generation validation 和 publication。

### 消费门禁

target 文件存在不等于内容消费者启用；引用统计和回流须等待真实消费者。

### 编辑效力

生成文件可以在 Obsidian 中编辑，但修改不回流、不取得项目效力。

### 符合性边界

当前不宣称 DCAP、DCTAP、JCS、BagIt 或 reproducible build conformance。

### 决定关系

`design/decisions/form-independence.md` 的核心分层继续有效；新决定补充应用约束和消费者门禁，不修改旧文件。

## 后果

- 每个 target 都要分别维护功能范围、模型引用、字段约束、使用指南和具体表示；跨 target 同步成本随之增加。
- `Application Profile` 与导出 artifact contract 要在同一 target 设计中相互引用，但两者不得越过语义选择与字节物化的交接点。
- Obsidian 文件和 Base 的可编辑性与项目效力分开；本项目不导入这些修改，重新导出可以覆盖它们。
- 静态 target 文件、内容字段契约、词表导出、同环境双跑、项目 manifest、checksum 和目录替换都不能单独证明真实消费者、外部标准符合性或正式激活。
- [设计与应用分离](form-independence.md)保持原文和已采纳状态，不因本决定修改或被替代。
- 仓库仍没有真实内容消费者、内容引用统计、检索统计或回流接口。
- 六份正式词表、正式数据形状、`vocab/topics.yaml` 的生成路径和 `concepts/glossary.md` 的 designation 与中英对照编辑权保持不变；正式术语数据仍未激活。
