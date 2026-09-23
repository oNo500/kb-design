# RDF 预览实施

目标：创建独立 `kb-obsidian-rdf` 应用包，从固定 RDF 输入生成可试写的 Obsidian 开发预览库。正式目录以后指定，本次不写正式库，不迁移旧工具或数据。

依据：[导出合同](../../docs/applications/obsidian/提案-Obsidian%20导出与导入.md)、[元数据方案](../../docs/applications/obsidian/提案-Obsidian%20元数据.md)。用户已授权实施和生成开发预览；这不批准正式内容或改变旧应用合同。

## 模块分工

- `apps/obsidian-rdf/src/kb_obsidian_rdf/build.py`：`build_delivery(input_path: Path) -> dict[str, bytes]`，返回相对 vault 路径到原字节的映射；包括 `vocab/` 及初建页面。输入中 `previous_delivery` 显式记录历史依赖。规则原严重程度不改写。
- `storage.py`：`initialize(vault, files)`、`inspect(vault, allow_pending=False)`、`refresh(vault, files, apply=False, offline=False)`、`recover(vault, offline=False)`。均返回 JSON 可序列化结果；只管理合同写集。
- `content.py`：`check_content(vault, paths=None)` 和 `new_content(vault, title, type_id, genre_id, subjects, entities=(), ...)`。身份、对象种类、准用条件和内容基数检查共用；默认新建 draft。
- `cli.py`：`prepare` 固定已有输入；`init`、`new`、`check`、`refresh`、`recover` 提供终端摘要与报告；所有写库操作显式 `--vault`。只有 preview 模式，没有通过目录名提升数据权限的 formal 开关。
- `common.py`：共用异常、固定字节编码、路径与身份方法。使用现有依赖栈，不另造 RDF、YAML 或 SHACL 引擎。

## 实施顺序

- [x] 输入与参考生成：先测试身份混淆、隐藏名称、未知字段留存、复杂说明和同一输入重建；再实现读取、投影、稳定路径与交付清单。
- [x] 安装与恢复：先测试非空目标、写集冲突、未知文件、符号链接、阶段中断；再实现锁、预写恢复记录、完整候选切换及历史保留。
- [x] 文章与入口：先测试错误对象引用、同名不同身份、旧引用与新试选、重复 UUID、受管理内容篡改；再实现字段校验、draft 建立和终端入口。
- [x] 集成验收：用完整计算机概念、实体及写作概念构建开发库，生成一篇演示文章；检查来源与名称呈现、引用查询数据、重复生成、冲突刷新及恢复。
- [x] 更新 README：简洁 ASCII 流程、完整命令、默认数据位置、指定目标目录及当前限制。审查真正影响用户数据和身份的失败，不重复机械事实检查。

## 风险与证据

源身份串用会使文章标引错误，以同名不同 IRI 和概念／实体混选的真实输入验证。刷新越界会损坏正文，以用户修改文件及目录摘要验证。崩溃期间无恢复记录会使版本混合，以目录替换阶段的故障注入验证。结构通过不能证明正式准用，在输出中单列 preview 与未核语义。

## 执行记录

隔离工作区 `codex/obsidian-rdf-preview`；此前三篇提案及索引复制到此工作区供实施核对。用户改为全新包，因此不复用旧 `kb-obsidian` 入口。现有命令不变；实现、测试与开发输出独立。

代码完成后核对目标无冲突，将新应用包、workspace 注册及锁文件同步回 `/Users/xiu/code/kb-design`。旧应用未修改，未提交。固定预览授权另存应用包的 `inputs/开发预览范围.md`，执行记录的更新不改变已冻结的授权材料。

## 验证记录

- 82 项行为测试通过；独立审查发现的跨源名称混用、复杂值顺序漂移和恢复时遗漏嵌套相对链接均已复现并修复。历史分支查询也改为固定版本路径。
- 载体原 `unassigned` 状态原样保留，按[内容模型的载体值域](../../docs/model/content/设计-内容模型.md#载体词表)和独立采用依据接受引用，不强改源状态，也不将未采纳书目候选自动转正。
- 完整开发库位于 `output/obsidian-rdf/development/`；2,365 个概念、302 个实体，以及现行辅助值域。SHACL structure 命中 14,428 个命名资源，Violation／Warning／Info 均为 0；实体事实、语义审阅及正式准用另列未确认。
- 重建 2,814 个文件全部字节一致，复建耗时 35.76 秒；摘要与结果见 `build/obsidian-rdf/rebuild-check.json`。
- 通过工具创建一篇 draft，再通过指定开发库的 Obsidian CLI 写入演示正文。文章检查 0 错误；主题和实体共 2 条正式准用未确认。Obsidian CLI 的文章列表、按主题和实体 Link 筛选均返回这篇文章。
- 用户明确不需要视觉检查；未进行视觉验收。未写正式知识库，未执行正式迁移或发布。
