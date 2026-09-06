# 术语数据提案

本包是具体值建议，未采纳、未发布。tc-/tm- UUIDv4 仅为提案身份；现行 glossary 与模型标签继续有效。

## 记录去向

143 个原定义行逐行保留。其中 56 行形成 65 个完整概念建议，3 行作为项目字段或 SKOS 属性说明，84 行保留现行登记待核。6 条出处缩写、14 条文献说明完整保留；231 条模型译名仍对应既有 256 个模型目标，不新增 TC。具体记录、原字符串、来源定位和定义前后值见同名 JSON。

## 概念边界

mapping 仅保留原登记 §3.41 的关系产物，不因样章另有过程义而新增概念。词表层 crosswalk 保留原登记待核，不能换成 DCMI metadata crosswalk。实体和属性仍引用原 Hogan 来源：将实体明确为由节点表示的对象，将属性限定为属性图中的键值信息。原定义的节点／对象、属性／值混淆以 before/after 明示纠正，待人采纳，不当作新增概念。被撤下的提案身份仅保留审阅审计，不复用、不计入候选。

查全率与查准率、原行已列的建设方法、四项 plain language 原则、三种 Ahrens 笔记、RDFS 与 OWL 分别建模。逗号和斜杠不自动证明同义。USE、UF、BT、NT、RT 保留为关系符号，不作英文术语。

单层级与多层级建议改用已核英文名称 monohierarchical structure 与 polyhierarchical structure，旧英文保留待核，名称变更须人决定。受控词表定义采用标目（headings），纠正标题这一泛译，不新增 designation。认知层级、Schema、relation/edge 等冲突项仍待核。内容单元与断言保留本库定义效力，不以外部 basis 伪装。

## 证据边界

ISO 已核定义继承实际阅读记录。ISO 15489 处置定义于 2026-09-06 直接重读同一免费样章第 10 页（印刷第 2 页）§3.8，概念、定义和英文形式三处 basis 均记录实际 checked。中文模型依据逐项说明行业表达，均为第 5 级建议，不冒充官方译名。

proposed_terms 可作 schema 与引用预检输入；缺失来源在 dependencies 明列 proposed_entity_id、URL 与材料身份。未来 decision-term-data-values 必须逐记录采纳具体值；history 日期是提案形成日期。workflow active 及首选／准用都是建议值。未声明 source/match，不以缺乏对应判据的来源身份凑齐字段。

## 旧项编辑源

建议同批采纳一个普通 Markdown 编辑源 `data/inputs/terminology/retained-glossary.md`。从现行 glossary 原样搬入 84 待核定义、3 说明、6 出处缩写、14 文献说明，共 107 行，保持章节、原值和引用含义。它是继续维护的现行登记源，明确继承旧效力；inventory、旧账本和 Git 仍只作审计与恢复，生产生成器不能从它们长期取有效值。

另有 11 个已迁移原行包含尚未采纳的形式或符号：术语表／代码表、叙词／descriptor、非叙词、USE／UF、BT／NT、RT、monohierarchy、polyhierarchy、分组、RDF、SKOS。JSON 已逐行列出，它们在保留源中保留原登记或参考说明，不自动变为准用词；已采纳定义不在保留源复制为第二份可编辑正文。

完整生成页继续使用 `docs/glossary.md`。按原章节展示正式术语记录和现行保留登记，说明两者依据状态；出处、文献和模型译名均继续显示。每个对象只有一个编辑源：65 概念与形式归 terms.yaml，107 保留行及上述残余形式归保留 Markdown，模型标签维持现有来源，章节归 layout。整页只读声明必须逐类指向这些来源。任何原行或残余形式未分配，均阻断覆盖现行 glossary。

## 来源对接

本包 13 项依赖逐项对应来源候选包：gruber-official、hogan-paper、rdf11、rdfs11、owl2、sparql11、dcmi-metadata-terms、dcmi-singapore-framework、reproducible-builds、iplf-plain-language、ahrens-zettelkasten-interview、iso-15489-1、juran-1974-non-pareto。DCMI 已使用具体材料身份的新 ID；JSON 保存每项来源候选位置、版本、URL 与引用它的概念列表。13 项仍未采纳，不新增来源用途角色。

## 切换具体值

同一次采纳包括 `data/vocab/term-cutover-state.yaml`：`state: active`、`active_editor: data/vocab/terms.yaml`、`terms_mode: active_editor`、`consumers_enabled: true`，决定为 `decision-term-data-values`。这些是未生效的建议值，history 写真实执行日期。控制范围仅为 65 个结构化术语概念及形式，不能吞并保留登记或模型标签的编辑权。

同一次采纳明确保留 Markdown 的现行编辑权。`check-terms` 同时读正式术语数据、保留源、布局、模型输入及采纳决定；对正式术语执行严格依据与状态校验，对保留源识别既有 designation、检查连续性和重复所有权，不补造 TC 或外部 basis。不能因没有 tc-id 将旧登记判为未登记。迁移 inventory 只用于初次对账，不成为日常有效源。

开启的消费者包括完整 glossary 生成和 Obsidian 术语参考消费。批准后完成必要实现和数据迁移，以同一隔离、干净 Git 快照生成完整 glossary，并在临时 vault 统一验收导出、刷新、链接、manifest 和内容保留；不写正式 vault。

## 写集与门槛

本次实际只改候选 JSON 和本文。获准后的数据写集为 entities.yaml 的 13 条来源、首次 terms.yaml、保留 Markdown、glossary-layout.yaml、完整 glossary、精确 cutover state，以及具体来源／术语采纳决定。必要实现限核心保留源读取、生成与校验、Obsidian 快照和术语参考合同及直接验证；临时产物位于 build/。JSON 列明路径、动作、转换事件和控制范围。

唯一尚缺的人工门槛，是一次明确采纳集中包的具体数据、保留编辑源及效力、精确切换值，并授权必要实现、迁移和临时 vault 验收。批准后预计 1–2 小时。生成完整性、引用、编辑权和端到端检查属于批准后完成的工程门槛，不再留未知控制字段等待下一轮提案。84 项证据缺口通过保留源延续现行效力，不被宣称已正式术语化。

正式 `~/Documents/kb-vault/` 写入、合并到 master、发版，以及新增正式义务、委托或持久正式索引不在写集。glossary 与 app 的术语参考消费者启用包含在本次采纳范围内。
