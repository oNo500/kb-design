# 词表使用调整

目标：词表在 Obsidian 中直接支持文章选词、引用和检索；开发库是测试环境，条目不再承担完整 RDF 浏览器的职责。用户已批准解决前一轮审查指出的问题。本轮不改源词表，不写正式库，不做视觉检查。

## 实施范围

- 独立包 `apps/obsidian-rdf/` 增加按文章字段查找、读取简短详情和检索相关文章的命令。
- 新条目用可读文件名，原身份仍存 `identifier`。同名冲突用原身份派生后缀区分；刷新保留已安装身份的路径，名称更新不隐式批量改写文章。
- 页面保留名称、定义、范围、关系与简短来源；完整原值、名称身份、历史和检查仍在受管理文件中。移除每页展开的查询代码和完整源属性表。
- 重整三篇应用提案和 README，明确“受控选项”是字段的取值角色，不是与概念、实体并列的新对象类型。
- 新生成 `output/obsidian-rdf/development-usage/`，保留旧开发库及其文章。正式目标目录仍以后指定。

## 模块接口

`build.py` 在 `_records.json` 每条记录增加 `entry`：`aliases` 字符串列表；`summary` 为 `{text, language, predicate}` 或 null；`definitions`、`scope_notes`、`descriptions` 为同结构列表；`relations` 按 `broader`、`narrower`、`related` 保存 `{identity,label,path}` 列表；`notes` 保留原附着主体与说明属性；`raw_sources` 保存来源键、版本与原件路径。缺失定义不补造，不把名称说明提升成概念定义。原记录 identity/kind/path/use/trial_selectable/formal_basis/restrictions 不变。

`query.py` 提供 `search_entries(vault, *, field, query='', limit=10, include_unavailable=False)`、`get_entry(vault, *, field, reference=None, term=None, details=False)`、`find_articles(vault, *, field, reference=None, term=None, descendants=False)`；返回 JSON 可序列化对象。字段使用现有内容约束，名称只能在字段范围内精确唯一时解析，歧义返回候选并拒绝自动选择。默认不将历史或不可用对象当作新选择。

查询核验安装凭据、manifest 和身份记录摘要，报告其局部检查范围；读具体条目再核对该页摘要和身份。结构型读取不重跑全套 SHACL。文章检索读取已保存元数据，不以正文提及代替标引；下位展开只适用于 subject，按文章身份去重。

## 高值检查

- 同名不同对象、概念与文档类型混选、隐藏名误用于候选：会产生错误标引，使用真实不同身份输入验证。
- 可读路径碰撞、输入顺序改变、名称刷新造成旧链接断裂：以不同身份、Unicode／大小写碰撞和历史输入核对路径与引用。
- 查询未核凭据、过期记录或返回历史对象为可选：以被改动交付和退出记录检验拒绝行为。
- 简化页面抹去语义或伪造定义：对照原始输入、结构化条目和投影报告，保留缺失及未展示说明。

## 执行进度

- [x] 页面与路径
- [x] 字段查询
- [x] 命令与文档
- [x] 完整开发库与使用验证

## 验证记录

110 项行为测试通过。独立审查发现历史页面在同身份仍有 current 记录时错误使用当前层级，已用反例复现并修复；历史或 retained 目标不能启用当前下位展开。

完整开发库位于 `output/obsidian-rdf/development-usage/`，原开发库保留。2,365 个概念、302 个实体及现行辅助数据全部生成；SHACL structure 命中 14,428 个命名资源，Violation、Warning、Info 均为 0，未运行的事实与语义检查仍单列。

人工智能页面由 15,820 字符缩为 1,163 字符，JavaScript 实体页面由 2,516 字符缩为 1,030 字符，源身份不变。完整重建 2,814 个文件字节一致，第二次构建用时 32.99 秒，结果见 `build/obsidian-usage/rebuild-check.json`。

使用真实数据实测 search/get，耗时约 0.19–0.26 秒；按字段返回可读名称、路径和明确缺失的摘要。通过 `--subject-name` 与 `--entity-name` 创建一篇演示 draft，articles 按 JavaScript 实体找回该文，文章检查 0 错误，2 条概念／实体引用正式准用未确认。

同名文件按目录区分，同目录的“冗余”实际生成两个带 8 位身份摘要的文件，原身份分别保留。未依靠同名合并对象。未做视觉检查，未写正式库，未提交。
