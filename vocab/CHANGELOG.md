# 词表变更记录

每版一节，按词表分列。只追加，不改旧节。规则见 [design/versioning.md](../design/versioning.md)。

## 2026.08

初版，2026-08-23。五份词表共用版本号。

### topics.yaml

- 新增 700 个概念、24 个数组。八个顶层 `active`，其余 `unassigned`
- 顶层：范围声明的八个 GB/T 13745 一级学科
- computing 之下：CS2023 17 个知识领域、161 个知识单元
- security 之下另有三个数组：ASVS 5.0 的 17 章、CWE-1000 的 10 个 pillar、ATT&CK v19.2 的 15 个战术；`cryptography` 同时属于 CS2023 与 ASVS 数组
- artificial-intelligence 之下另有两个数组：ATLAS 2026.07 的 16 个战术、OWASP LLM Top 10 2025
- software-engineering 之下另有 SWEBOK v4 的 18 章；`software-design`、`software-construction` 同时属于 CS2023 与 SWEBOK 数组
- networking-and-communication 之下另有 RFC 1122 的四层
- 其余七个顶层之下：GB/T 13745 的二级、三级学科，共 427 个；英文标签为本库所译（`translated: [en]`）
- 多层级：`mathematical-and-statistical-foundations` 同时在 computing 与 mathematics 之下；`software-engineering-management` 同时在 software-engineering 与 management 之下
- 标签的译名依据：每个概念带 `basis.zh`、`basis.en`；CS2023 的 265 个中文标签、GB/T 13745 的 427 个英文标签为本库所译（`self`），待按译名阶梯追溯；四个顶层的英文取自 Wikidata，四个无英文
- 同名概念的处理：跨上位同名加上位后缀（各知识领域的“社会、伦理与职业”知识单元；ATLAS 与 ATT&CK 同名战术）

### entities.yaml

- 新增 27 个实体，均为作为词表来源的标准、知识体系与参考资料；`kind` 为 standard 或 publication，带 `tier`
- 第二批 30 个：4 个组织、6 个 AI 编程工具、5 种语言、15 个 JS/TS 与 Python 生态的框架和工具；`form` 记 Wikidata 的 instance of
- 全部实体的 `subjects` 加 `basis`：第一批以标准自身的范围声明为依据（`<id>:scope`），第二批 23 个核到 CS2023 知识单元的主题条目，7 个为 `self`；`basis` 含 `self` 的实体一律 `candidate`（第一批 5 个、第二批 7 个）

### sources.yaml

- 新增 27 个来源，`role` 按 [sources-registry.md](../design/sources-registry.md)

### types.yaml

- 新增 Diátaxis 四类
- 加 DITA 1.3 的排障、术语条目两类

### genres.yaml

- 新增：IPTC genre 的五类（背景、分析、观点、评价、建议），closeMatch 到 IPTC URI

### forms.yaml

- 新增：IEEE LOM §5.2 的 15 个取值分两个数组（呈现形式、教学活动），加速查表（Wikidata）；中文标签为本库所译

### entities.yaml、sources.yaml

- 加 dita、iptc-genre、lom、schema-org 四个来源；types、genres 加 schema.org 映射

### 治理

- 2026-08-23：首次记录指标快照（`signals.yaml`）。未标引 692/700；self 断言 12/57；候选 16；来源复核到期 0
- 2026-08-23：决策权首批边界采纳，见决定记录；已入库 57 个实体的 `subjects` 追溯豁免
