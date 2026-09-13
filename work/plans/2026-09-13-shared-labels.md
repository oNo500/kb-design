# 中文标签实施

目标：在 kb-vocab 现有生成管线中接入独立中文 Turtle 与采纳记录，应用消费同一发布版本的标签和依据。本计划落实本会话已确认方案；不授权批量译名采纳，不改来源文件或旧 YAML。

## 标签合同

- `data/inputs/vocabulary/labels.zh.ttl` 只保存现有 Concept、Collection、ConceptScheme 的中文 prefLabel、altLabel、hiddenLabel。
- `label-adoptions.json` 的 records 保存 id、accept、uri、property、language、label、original、basis。original 由 label-context 命令生成，绑定英文标签与范围说明；accept=false 的历史保留，不进入输出。
- 有效中文三元组和有效采纳记录一一对应；不存在对象、过期依据、冲突及来源已有同值标签均阻断，禁止隐式覆盖。
- 外部依据核对现有书目 ID；模型依据保存真实模型名称、日期、理由和明确授权，输出携带固定未核实提示。

## 生成接入

- label_context(graph, uri) 返回规范化上下文快照；apply_labels(graph, ttl_bytes, adoption_bytes, bibliography_bytes) 返回增量图与有效依据，不修改输入图。
- system_build 在完整自有结构生成后、校验前合并标签；所有分图使用合并结果。
- replay 固定三份输入及书目快照；manifest 增加标签合同版本，发布验证继续检查完整写集。
- 仅复用已有 RDFLib、SHACL、JSON 与项目已锁定 PyYAML，不新增运行服务。

## 应用接入

- Skosmos 读取同版本 label-provenance.json；模型标签在名称旁注明依据性质，中文缺失回退英文。
- 原来有中文的领域名称保留原编辑归属；不将其搬到补充标签文件。
- 未接入 RDF 的旧 Obsidian 消费者不做正式迁移；共享发布产物提供未来消费者读取合同。

## 实施步骤

- [x] 增加未采纳、上下文过期、语义写入与标签冲突的失败测试。
- [x] 实现标签读取与 label-context CLI，复用现有书目解析库。
- [x] 接入生成、分图、依据输出、版本与离线重放；测试坏输入不切换 current。
- [x] 接入 Skosmos 的依据提示，并验证无标签时不影响原展示。
- [x] 核对当前完整来源构建，执行相关回归，更新使用说明；不提交其他在途修改。
