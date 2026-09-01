# Obsidian 概念纠偏设计 (Obsidian Concept Correction Design)

状态：已批准设计，等待实施计划。本文是 Superpowers 规格，只规定纠偏目标、概念边界、来源和实施约束；项目现行规则仍由 `concepts/`、`design/`、已采纳决定和正式数据承担。

## 问题边界

Obsidian 阶段已经完成官方功能核对、应用映射、确定性导出、安全写入和测试，但执行顺序跳过了项目要求的“概念文—方法登记—设计规则”。现有资料直接从 Obsidian 官方功能进入设计，不能回答以下问题：

- 应用无关内容模型与应用专用表示之间是什么既有方法关系；
- 字段约束、使用指南和编码语法是否属于同一层；
- 应用 binding 与 metadata crosswalk 的边界；
- 两次输出相同、manifest 完整、生成关系和安全发布分别证明什么；
- `canonical JSON`、只读 Base、原子发布和可重现性是否被准确陈述；
- 现有实现应当保留、改写还是撤回。

本次允许概念结论推翻现有设计和实现。不得把现有代码当作结论，再寻找来源为其补写理由。

## 纠偏目标

本次建立可以独立支撑 Obsidian 映射的概念链，并据此重新验收现有实现。

1. 用 DCMI 的 Application Profile 相关概念说明应用无关模型、应用约束和具体表示之间的分层。
2. 用 Reproducible Builds、RFC 8493、W3C PROV 和文件系统接口说明确定性、完整性、溯源、可重建性和发布可见性的不同职责。
3. 用 Obsidian 官方帮助记录目标应用的真实对象、能力和限制。
4. 按译名阶梯核对所有拟采用 designation；查不到时保留英文，不自译。
5. 建立概念文和方法登记，再重写应用映射及关联设计。
6. 只实现概念结论要求的代码修正，不引入无消费者的标准和基础设施。

## 来源层次

来源按用途分开，任何一类不能替代另一类。

| 来源 | 回答的问题 | 不能证明 |
|---|---|---|
| DCMI Application Profile、Singapore Framework、DCAM、DCTAP | metadata application 怎样记录功能、模型、字段约束、使用和编码语法 | 当前项目符合正式 DCAP、DCAM、DSP 或 DCTAP |
| Obsidian 官方帮助 | vault、property、alias、internal link、Base 和支持格式的实际应用行为 | 稳定 ID、正式效力、designation 准入、导出安全和回流政策 |
| Reproducible Builds | source、environment、instructions、artifact 和逐字节复建的关系 | manifest 完整、来源真实性或语义正确 |
| RFC 8493 | BagIt payload manifest 的路径、checksum、complete 和 valid 边界 | 本项目是 BagIt、输出可复建或来源可信 |
| RFC 8785 | JSON Canonicalization Scheme 的规范字节表示 | 普通 key sorting 或 pretty-printed JSON 是 JCS |
| W3C PROV | Entity、Activity、Usage、Generation 和 Derivation 的表达 | provenance 记录真实、已签名或可重建 |
| Python 与 POSIX 文件接口 | `os.replace()`、rename、fsync 和跨文件系统失败边界 | 多文件事务、掉电持久性或内容正确 |

来源笔记必须记录实际打开的页面、已读小节、核对日期、适用边界和未读范围。搜索摘要只作入口，不能进入概念结论。

## 术语边界

### 应用方法

DCMI 把 Application Profile 用于记录特定 metadata application 的功能、领域模型、term 使用与约束、使用指南和编码语法。它支撑本项目的三层结构，但不自动使本项目成为正式 DCAP。

中文候选“应用纲要”只有在 GB/T 25100.2―2025 或其他更高阶正文中核到对应 designation 后才能登记。若只能核到参考文献题名、起草稿或二手论文，概念文标题和正文采用 `Application Profile`，中文只作解释，不作名称。

以下 designation 不合并：

- `Application Profile`：特定应用中的 metadata 使用和约束；
- `Encoding Syntax Guidelines`：整个 metadata record 的具体表示；
- `Syntax Encoding Scheme`：单个值的 lexical form 或 datatype；
- `metadata crosswalk`：两个独立 metadata standard、schema 或 profile 之间的对应；
- application binding：本项目对字段落点和路径规则的普通描述，在取得 designation 依据前不登记为独立方法。

当前 Obsidian properties 和路径是本项目选择的具体表示，不是 Obsidian 提供的独立 semantic schema。因此现有字段表不是 metadata crosswalk，也不能把 Wikilink 称为 DCAM value URI。

### 构建边界

Reproducible Builds 项目要求：给定相同 source code、build environment 和 build instructions，任何一方能够重建全部指定 artifact 的逐字节相同副本。

当前两次本机导出相同只证明已声明输入和当前环境下的确定性行为。没有独立第三方、完整环境声明和跨环境复建时，不使用 `reproducible build` 作为完成结论。若没有权威中文 designation，项目保留英文。

### JSON 表示

RFC 8785 JCS 规定 I-JSON、ECMAScript primitive serialization、UTF-16 code unit 属性排序、无 token 间空白和 UTF-8 输出。当前实现使用 Python `json.dumps()` 的 key sorting 与固定缩进，不符合 JCS。

项目文档和代码不得继续使用 `canonical JSON`。改用序列化参数事实：UTF-8、键排序、固定缩进、固定换行和末尾换行。只有实现并通过 RFC 8785 conformance tests 后才能使用 JCS designation；当前没有该需求。

### 清单边界

本项目的 `manifest.json` 是项目自有输出清单。它保存相对路径、摘要、输入版本和输出覆盖，用于发现遗漏、额外文件和字节漂移。

它不是 BagIt payload manifest，也不取得 BagIt `complete` 或 `valid` 状态。checksum 不能证明 publisher、generator、source、审批、语义、可重建性或真实性；项目没有主动攻击威胁时不引入签名、TUF 或 attestation。

### 只读边界

“只读参考区”是项目效力边界：导出文件的修改不回流、不改变正式数据、不取得决定效力，下次生成可以覆盖这些修改。

它不是 Obsidian 权限保证。Bases 可以编辑文件及其 properties；当前设计不得再把 Base 称为技术上的只读表格，也不得把“不使用自定义写回动作”当作不能编辑的证据。

### 发布边界

`os.replace()` 成功时提供单个目录项的原子替换语义；它可能因非空目录、权限、平台和跨文件系统而失败。当前实现先在目标同级目录生成和验证，再尝试一次替换，可以控制发布可见性。

这不证明掉电后的持久性、多目录事务或对抗性真实性。当前没有要求抵抗掉电，因此不增加逐文件 fsync 和父目录同步；文档只陈述已经实现和验证的可见性边界。

## 分层模型

纠偏后的设计使用三层，不压成一张“映射表”。

| 层 | 职责 | 当前项目对象 |
|---|---|---|
| 应用无关模型 | 定义资源、字段、值域、身份、关系和生命周期 | `design/content-model.md` 与六份正式词表 |
| 应用约束 | 说明功能范围、模型复用、字段约束、使用和不能表达的内容 | `design/targets/obsidian.md` 的 profile 部分 |
| 具体表示 | 说明 property、标题、正文、Wikilink、路径、Base 和文件格式 | `design/targets/obsidian.md` 的 Obsidian 表示部分 |

导出 artifact contract 独立于上述 metadata 三层：它定义输入快照、输出集合、序列化、清单、校验和发布。Application Profile 不能替代 serializer、validator、manifest 或安全发布。

## 应用结构

重写后的 Obsidian 文档至少包含以下职责。

### 功能范围

- 支持六份正式词表的浏览、链接和筛选；
- 保存未来内容字段的应用落点；
- 不生成知识库内容，不消费正式术语数据，不回流；
- 不提供 UI 只读权限，不宣称 Obsidian runtime 验证。

### 模型引用

- 直接引用现行内容模型和正式词表，不复制或重定义其语义；
- 说明七类导出对象与内容单元的关系；
- 把稳定 identifier 与 path、label、alias、tag 分开。

### 字段约束

每个字段记录 source identity、必填性、基数、literal／reference、datatype 或受控值、目标位置、缺省、省略、fallback、不可表达值的保存位置和可逆性。

现行内容模型的五个问题继续作为项目操作检查表，但放入 Application Profile 的功能、约束、语法和 loss 边界中，不再自称没有概念依据的完整方法。

### 表示规则

- property 的官方类型名按 Text、List、Number、Checkbox、Date、Date & time、Tags 记录；
- nested properties 是 Obsidian 当前不支持的应用能力，不是 YAML 无法表达；
- internal link 只作 Obsidian reference syntax；
- Base 是本项目用于浏览的可编辑视图，不是数据源；
- `.json` manifest 是同目录项目文件，不是 Obsidian accepted content format。

### 导出合同

- 输入、生成器和输出集合明确列出；
- 内容和清单读取同一输入字节快照；
- 输出序列化参数逐项固定，不使用 `canonical JSON`；
- manifest/checksum、生成关系和双跑比较各自陈述证据边界；
- 失败只清理本次临时目录，不删除用户目标；
- 生成目录的“只读”只说明项目效力和无回流。

## 项目产物

概念阶段至少产生以下项目原生内容：

- DCMI Application Profile 来源笔记；
- Obsidian 官方帮助来源笔记；
- Reproducible Builds、RFC 8493／8785、W3C PROV 和 Python／POSIX 文件接口来源笔记；
- Application Profile 概念文；
- Reproducible Builds 概念文；
- 方法登记中的相应方法、来源、适用边界和导出规则；
- 一条新的决定记录，采纳三层结构并明确应用映射存在不等于消费者启用；旧决定记录不修改；
- 重写后的 Obsidian 应用设计及受影响入口。

来源笔记可按来源职责合并，但不得把 DCMI、Obsidian vendor facts 和软件生成完整性混成一种依据。概念文名称在译名核验前保持英文占位，不提前自译。

## 实现审查

概念和决定冻结后才检查代码。当前已知的必要候选修正是：

- 把 `_canonical_json` 等内部命名改为准确的确定性 JSON 描述；
- 保持当前 JSON 字节行为，除非概念审查发现实际不确定输入；
- 保持项目 manifest，不实现 JCS 或 BagIt；
- 保持同级临时目录、回读校验和 `os.replace()`，但收窄原子性和只读主张；
- 保持 Bases 文件，不增加权限控制；
- 只在真实行为合同变化时新增或修改测试。

代码审查发现其他概念冲突时，先补入设计差异表，再修改实现。不得顺手增加 RDF、SHACL、DCTAP、SLSA、TUF、数字签名、fsync 链或内容回流。

## 决定边界

本次用户已经批准概念结论可以推翻现有 Obsidian 设计和实现。实施仍按项目决策权分层：

- 来源摘录、阅读范围、机械差异和同义错误修正为 L1；
- 概念文、方法登记、设计结构、字段契约和实现行为变化为 L2；
- 新决定的采纳、旧决定的替代、范围、正式数据、发版和草案生效为 L3。

新的决定记录在写入后须由用户明确采纳；在此之前可以作为提议，不能把三层方法写成已生效政策。

## 验证投入

只保留具有独有风险证据的检查。

| 风险 | 必要证据 |
|---|---|
| designation 或译名无依据 | 逐级来源记录与查无记录；概念文和 glossary 对账 |
| Application Profile、crosswalk 和 binding 混淆 | 概念文反例与项目层次逐项对照 |
| JCS、BagIt、可重现或只读能力误报 | 标准条款与实际序列化／应用行为对照 |
| 设计与实现不一致 | 字段、路径、Base、manifest 和 CLI 的端到端差异表 |
| 确定性回归 | 同一冻结输入双跑逐字节比较 |
| 安全写入回归 | 现有非空目标、symlink、替换失败和回读失败测试 |
| 当前效力误报 | 写集、决定状态、正式数据和消费者存在性检查 |

文档不为 RED／GREEN 形式新增测试。现有导出行为没有改变时，不重写测试；完整 17 项回归只在代码或共享合同完成后运行一次。链接和术语检查在文档阶段运行；低价值重复复审不执行。

## 完成口径

概念纠偏完成须同时满足：

- 所有拟采用概念和译名有来源或明确查无记录；
- Application Profile、应用 binding、metadata crosswalk 和编码语法职责分开；
- 确定性、可重现性、manifest 完整性、provenance、原子可见性和持久性没有互相替代；
- Obsidian 官方事实有独立来源笔记，Base 可编辑性和 nested properties 边界准确；
- 方法登记能够逐条推出保留的设计规则；
- 新决定得到用户采纳，或设计明确保持提议状态；
- 项目正文、规格、实现和测试使用相同能力边界；
- 没有引入无消费者的 RDF、SHACL、DCTAP、JCS、BagIt、签名或回流基础；
- 最终明确报告现有 Obsidian 阶段是通过、部分通过还是撤回。

## 权威来源

- [DCMI Application Profile Guidelines](https://www.dublincore.org/specifications/dublin-core/application-profile-guidelines/)
- [DCMI Singapore Framework](https://www.dublincore.org/specifications/dublin-core/singapore-framework/)
- [DCMI Profile Guidelines](https://www.dublincore.org/specifications/dublin-core/profile-guidelines/)
- [DCMI Abstract Model](https://www.dublincore.org/specifications/dublin-core/abstract-model/)
- [DCMI DCTAP](https://www.dublincore.org/specifications/dctap/)
- [Obsidian 数据存储](https://obsidian.md/help/data-storage)
- [Obsidian Properties](https://obsidian.md/help/properties)
- [Obsidian Internal links](https://obsidian.md/help/links)
- [Obsidian Aliases](https://obsidian.md/help/aliases)
- [Obsidian Bases](https://obsidian.md/help/bases)
- [Obsidian Bases syntax](https://obsidian.md/help/bases/syntax)
- [Reproducible Builds definition](https://reproducible-builds.org/docs/definition/)
- [RFC 8493 BagIt](https://www.rfc-editor.org/rfc/rfc8493.html)
- [RFC 8785 JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html)
- [W3C PROV-DM](https://www.w3.org/TR/prov-dm/)
- [Python JSON](https://docs.python.org/3/library/json.html#json.dump)
- [Python `os.replace`](https://docs.python.org/3/library/os.html#os.replace)
