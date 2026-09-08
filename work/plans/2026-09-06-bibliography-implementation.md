# 书目迁移实施

依据：[已批准方案](2026-09-06-bibliography-separation.md)。用户已回复“执行吧”。使用 subagent-driven-development 分工实施，协调者负责数据、采纳记录、集成与正式库迁移。

## 共同合同

正式书目文件为 `data/references/bibliography.yaml`，根键 `schema`、`schema_version`、`version`、`references`；schema 为 `urn:kb-design:data:bibliography`。来源相关七份数据统一使用 schema_version 3；terms 的概念模式版本不随来源引用表示机械提升。

文献依据使用 `reference`、`locator`、`checked`；来源用途以 `reference` 指向书目。普通实体 label、urls、kind、scope、vendor 字段的直接官方依据使用互斥的 `url`、`locator`、`checked`。subjects、术语和映射不接受直接 URL 旁路。文献 ID 保持；普通实体表不保留 standard／publication。

旧采纳决定不改写。新的迁移采纳记录显式映射身份及依据字段形状，验证时只对列明的机械位置变换解释旧授权，不扩大状态、角色、内容值或许可。

## 核心引用

- [ ] 修改 `packages/kb-core/src/kb_core/source_model.py` 与 `schemas/source-*.schema.json`，拆分文献和普通实体并拒绝混用及 URL 越权。
- [ ] 更新核心生成、索引、术语校验、许可、渲染与测试夹具；历史迁移工具仅保留历史职责，不提供正式兼容入口。
- [ ] 用跨目录、权限、历史授权和受限 URL 反例验证，失败意味着错误材料或扩大权限进入正式数据。

## 应用引用

- [ ] 更新 `apps/obsidian/src/kb_obsidian/` 的快照、导出、建立器、校验、manifest 和参考刷新；书目输出到 `kb/references/`。
- [ ] 普通 refresh 保留原写集；旧祖先快照用旧实现验证，不把旧数据转成新数据后冒充原基线。
- [ ] 更新 `apps/vocab-preview/`，将书目与实体分开显示、读取和刷新。
- [ ] 用临时快照和 vault 检查新建、引用解析、刷新保护与失败恢复；不写正式库。

## 数据与治理

- [ ] 列出逐文献贡献、依赖和迁移去向；对无设计贡献但有历史引用者明确保留审计状态，不自行删除。
- [ ] 搬迁书目记录，保持 ID、事实、状态和历史；三条误增文档撤回，普通事实转官方 URL。
- [ ] 更新主题生成输入及其他现行引用；重建主题和术语生成页，核对对象语义与历史完整。
- [ ] 增加具体采纳记录，重写当前实体、书目、来源用途和内容引用文档，保持历史决定原文。

## 集成与同步

- [ ] 运行来源与术语门禁、生成核对，以及涉及的高风险行为回归。
- [ ] 临时 vault 迁移内容引用，确认 UUID、标题、状态和无关正文不变；记录完整写集。
- [ ] 提交干净快照，正式库备份后按核对过的写集迁移，原生 Obsidian CLI 回读并运行内容校验。
- [ ] 记录结果与恢复路径，不执行推送、发版或启用新消费者。
