# 映射关系核对

状态：待审提案。2026-09-06 只读核对 24 条既有 Wikidata 映射，不含已采纳的 Obsidian。没有修改正式数据或批准关系。

## 证据范围

逐项读取固定 Q 集合的 EntityData，记录实际 Q、修订号、条目说明与 P31、P279、P178、P856、P277、P366 原始断言。未下载数据库，未展开类别树；类别 Q 值保留原样，不推断未读取的类别标签。每条的固定修订链接、响应 SHA-256、原记录和结构化建议见[逐项记录](2026-09-06-wikidata-relations.json)。

CS2023 使用现有本地完整原文，核对 FPL 前言、SE-Tools #3/#4/#7、SE-Validation #4、FPL-Types #5 与 SPD-Web #2。课程范围与产品属性是两类外部证据；本库主题归属仍是明确标注的项目判断，P31 不直接等于本库宽类。

## 映射建议

| 本库记录 | 实际条目与修订 | 对应结论 | subjects 结论 |
|---|---|---|---|
| entities/anthropic | [Q116758847 · 2537652532](https://www.wikidata.org/w/index.php?title=Q116758847&oldid=2537652532) | 建议保留 exactMatch，待采纳 | 保留原 self 判断 |
| entities/openai | [Q21708200 · 2540352658](https://www.wikidata.org/w/index.php?title=Q21708200&oldid=2540352658) | 建议保留 exactMatch，待采纳 | 保留原 self 判断 |
| entities/moonshot-ai | [Q130270266 · 2538904973](https://www.wikidata.org/w/index.php?title=Q130270266&oldid=2538904973) | 建议保留 exactMatch，待采纳 | 保留原 self 判断 |
| entities/claude-code | [Q138457287 · 2540480429](https://www.wikidata.org/w/index.php?title=Q138457287&oldid=2540480429) | 建议保留 exactMatch，待采纳 | 存在未覆盖值，整字段阻断 |
| entities/antigravity | [Q136827654 · 2540267026](https://www.wikidata.org/w/index.php?title=Q136827654&oldid=2540267026) | 建议保留 exactMatch，待采纳 | 存在未覆盖值，整字段阻断 |
| entities/openclaw | [Q137916205 · 2536755323](https://www.wikidata.org/w/index.php?title=Q137916205&oldid=2536755323) | 建议保留 exactMatch，待采纳 | 存在未覆盖值，整字段阻断 |
| entities/typescript | [Q978185 · 2532629356](https://www.wikidata.org/w/index.php?title=Q978185&oldid=2532629356) | 建议保留 exactMatch，待采纳 | 存在未覆盖值，整字段阻断 |
| entities/javascript | [Q2005 · 2527256614](https://www.wikidata.org/w/index.php?title=Q2005&oldid=2527256614) | 建议保留 exactMatch，待采纳 | 存在未覆盖值，整字段阻断 |
| entities/python | [Q28865 · 2530995293](https://www.wikidata.org/w/index.php?title=Q28865&oldid=2530995293) | 建议保留 exactMatch，待采纳 | 存在未覆盖值，整字段阻断 |
| entities/go | [Q37227 · 2539468495](https://www.wikidata.org/w/index.php?title=Q37227&oldid=2539468495) | 建议保留 exactMatch，待采纳 | 存在未覆盖值，整字段阻断 |
| entities/rust | [Q575650 · 2540091247](https://www.wikidata.org/w/index.php?title=Q575650&oldid=2540091247) | 建议保留 exactMatch，待采纳 | 存在未覆盖值，整字段阻断 |
| entities/vite | [Q111590996 · 2533730182](https://www.wikidata.org/w/index.php?title=Q111590996&oldid=2533730182) | 建议保留 exactMatch，待采纳 | 存在未覆盖值，整字段阻断 |
| entities/webpack | [Q22909730 · 2539483640](https://www.wikidata.org/w/index.php?title=Q22909730&oldid=2539483640) | 建议保留 exactMatch，待采纳 | 存在未覆盖值，整字段阻断 |
| entities/eslint | [Q55452824 · 2540376393](https://www.wikidata.org/w/index.php?title=Q55452824&oldid=2540376393) | 建议保留 exactMatch，待采纳 | 存在未覆盖值，整字段阻断 |
| entities/nextjs | [Q56062435 · 2539071850](https://www.wikidata.org/w/index.php?title=Q56062435&oldid=2539071850) | 建议保留 exactMatch，待采纳 | 整字段建议待采纳 |
| entities/react | [Q19399674 · 2531086275](https://www.wikidata.org/w/index.php?title=Q19399674&oldid=2531086275) | 建议保留 exactMatch，待采纳 | 整字段建议待采纳 |
| entities/vuejs | [Q24589705 · 2525014457](https://www.wikidata.org/w/index.php?title=Q24589705&oldid=2525014457) | 建议保留 exactMatch，待采纳 | 整字段建议待采纳 |
| entities/nestjs | [Q107015664 · 2537334085](https://www.wikidata.org/w/index.php?title=Q107015664&oldid=2537334085) | 建议保留 exactMatch，待采纳 | 整字段建议待采纳 |
| entities/ruff | [Q115911873 · 2540077635](https://www.wikidata.org/w/index.php?title=Q115911873&oldid=2540077635) | 建议保留 exactMatch，待采纳 | 整字段建议待采纳 |
| entities/pytest | [Q28975377 · 2508245902](https://www.wikidata.org/w/index.php?title=Q28975377&oldid=2508245902) | 建议保留 exactMatch，待采纳 | 整字段建议待采纳 |
| entities/pyright | [Q102522262 · 2530894696](https://www.wikidata.org/w/index.php?title=Q102522262&oldid=2530894696) | 建议保留 exactMatch，待采纳 | 整字段建议待采纳 |
| entities/pydantic | [Q107381687 · 2539015373](https://www.wikidata.org/w/index.php?title=Q107381687&oldid=2539015373) | v2 与整体范围不一致，阻断 | 保留原 self 判断 |
| entities/fastapi | [Q101119404 · 2524737798](https://www.wikidata.org/w/index.php?title=Q101119404&oldid=2524737798) | 建议保留 exactMatch，待采纳 | 整字段建议待采纳 |
| forms/cheat-sheet | [Q2309859 · 2485488116](https://www.wikidata.org/w/index.php?title=Q2309859&oldid=2485488116) | 建议保留 exactMatch，待采纳 | 不适用 |

## 归属缺口

| 记录及主题 | 原依据支持范围与缺口 |
|---|---|
| entities/claude-code · artificial-intelligence | 旧 SE-Tools #7 支持代码辅助工具，不单独证明本库 artificial-intelligence 归属；条目 AI 描述仅补充外部属性。 |
| entities/claude-code · tools-and-environments | CS2023 明列 ML-powered code assistants；条目说明为 Anthropic AI 工具，与本库编程智能体范围可对应。 |
| entities/antigravity · artificial-intelligence | AI coding tool 描述是外部属性；旧 SE-Tools 定位没有单独覆盖 AI 主题归属。 |
| entities/antigravity · tools-and-environments | 条目说明 Google AI coding tool，P31 原始值含 Q13741；结合本库 IDE 描述，可建议归于工具与环境。 |
| entities/openclaw · artificial-intelligence | 条目描述含 AI，但旧 SE-Tools #7 不是该主题归属依据；需单独归属判断。 |
| entities/openclaw · tools-and-environments | 条目表示自主 AI 助手；没有证据表明本库范围限 IDE 或编程辅助，不能把通用助手直接套入 SE-Tools #7。 |
| entities/typescript · foundations-of-programming-languages | CS2023 FPL 前言明确讨论编程语言的基础与相关概念，而不是某个具体语言；Wikidata 身份及 P31 只能说明具体语言对象。该宽类归属仍需项目判断，不能作为外部事实直接展开。 |
| entities/javascript · foundations-of-programming-languages | CS2023 FPL 前言明确讨论编程语言的基础与相关概念，而不是某个具体语言；Wikidata 身份及 P31 只能说明具体语言对象。该宽类归属仍需项目判断，不能作为外部事实直接展开。 |
| entities/python · foundations-of-programming-languages | CS2023 FPL 前言明确讨论编程语言的基础与相关概念，而不是某个具体语言；Wikidata 身份及 P31 只能说明具体语言对象。该宽类归属仍需项目判断，不能作为外部事实直接展开。 |
| entities/go · foundations-of-programming-languages | CS2023 FPL 前言明确讨论编程语言的基础与相关概念，而不是某个具体语言；Wikidata 身份及 P31 只能说明具体语言对象。该宽类归属仍需项目判断，不能作为外部事实直接展开。 |
| entities/rust · foundations-of-programming-languages | CS2023 FPL 前言明确讨论编程语言的基础与相关概念，而不是某个具体语言；Wikidata 身份及 P31 只能说明具体语言对象。该宽类归属仍需项目判断，不能作为外部事实直接展开。 |
| entities/vite · tools-and-environments | 条目说明 JavaScript module bundler；课程构建系统范围支持工具用途的归属建议。 |
| entities/vite · web-platforms | 旧 SE-Tools #4 讲过程自动化，未覆盖 Web Platforms；JavaScript bundler 也不自动等于 Web 平台或框架。 |
| entities/webpack · tools-and-environments | 条目说明 JavaScript module bundler；课程构建系统范围支持工具用途的归属建议。 |
| entities/webpack · web-platforms | 旧 SE-Tools #4 不覆盖 Web Platforms；工具所属生态不能自动变成本库平台归属。 |
| entities/eslint · tools-and-environments | 条目说明 JavaScript code analysis software；课程静态分析工具范围支持归属建议。 |
| entities/eslint · web-platforms | 旧定位支持静态分析工具，不覆盖 Web 平台归属；代码语言也不足以自动认定平台。 |
| entities/nextjs · web-platforms | 条目描述与 Web 应用或 JavaScript 框架有关，结合课程 Web platforms/frameworks/metaframeworks，可提出主题关联判断；课程没有点名该产品。 |
| entities/react · web-platforms | 条目描述 Web 应用框架或 JavaScript UI 库；结合课程 Web platforms/frameworks/metaframeworks，可提出主题关联判断。React 的本库 form=web framework 与条目 library 描述有细分差异，单列复核，不自动改字段。 |
| entities/vuejs · web-platforms | 条目描述与 Web 应用或 JavaScript 框架有关，结合课程 Web platforms/frameworks/metaframeworks，可提出主题关联判断；课程没有点名该产品。 |
| entities/nestjs · web-platforms | 条目描述与 Web 应用或 JavaScript 框架有关，结合课程 Web platforms/frameworks/metaframeworks，可提出主题关联判断；课程没有点名该产品。 |
| entities/ruff · tools-and-environments | 条目描述 Python linter/formatter；课程静态分析工具范围与 lint 用途可对应。 |
| entities/pytest · tools-and-environments | 条目描述 Python testing framework，与课程 testing tools 对应。 |
| entities/pytest · software-verification-and-validation | 条目为测试框架；课程 test kinds 支持测试领域关联建议，不表示课程点名 pytest 或框架自身验证所有测试种类。 |
| entities/pyright · tools-and-environments | 条目说明静态类型检查器，对应课程静态分析工具范围。 |
| entities/pyright · type-systems | 条目说明静态类型检查器；课程静态与动态类型的错误检测目标可支持主题关联建议，但并非类别等同。 |
| entities/fastapi · web-platforms | 条目描述与 Web 应用或 JavaScript 框架有关，结合课程 Web platforms/frameworks/metaframeworks，可提出主题关联判断；课程没有点名该产品。 |

## 采纳边界

23 条映射建议保留 exactMatch，Pydantic 的版本限定关系阻断。React 的 form 细分类别差异单列复核；名称同一性不自动批准 form。原 self 归属保持项目判断。JSON 的 after=null 表示尚无完整可执行建议，不能据此删除原关系。局部支持列表只供审阅，不得覆盖整字段造成未覆盖主题丢失。

新增关系、补全 typed subjects basis、变更 form 或 scope 均需后续明确采纳；本报告没有完成这些采纳。


## 编程工具归属

本节不是 Wikidata 取证。仅补齐 codex、kimi-code、opencode、ty 四条非 self 记录；原 24 条不重查。只使用既有项目 scope 与本地 CS2023 原文，不核产品网站、不新建来源，也不重核 scope 中关于 Wikidata 条目存在与否的旧陈述。

| 记录 | 逐值候选 | 限制 |
|---|---|---|
| codex | tools-and-environments 引 SE-Tools 通用学习成果 #6/#7；artificial-intelligence 补引 AI 前言 | CLI 与云端范围来自现有 scope；不等同 IDE，不借同名旧模型证明产品 |
| kimi-code | tools-and-environments 引 SE-Tools 通用学习成果 #6/#7；artificial-intelligence 补引 AI 前言 | “编程智能体”是沿用的项目范围，不是新核发布者事实 |
| opencode | tools-and-environments 引 SE-Tools 通用学习成果 #6/#7；artificial-intelligence 补引 AI 前言 | 终端工具不自动属于 IDE；不借同名交换平台证明身份 |
| ty | tools-and-environments 引 SE-Tools #3；type-systems 引 FPL-Types #5 | 类型检查器范围来自现有 scope；主题关联不要求课程点名 ty，但也不是发布者产品证据 |

八个主题值的 typed basis 候选见 JSON 的 additional_subject_records。AI 归属以现有“编程智能体”确指 AI 辅助编程对象为条件；若该解释尚未采纳，保留待审。旧 SE-Tools #7 的 IDE 语境不能单独覆盖所有 CLI，本次开发工具建议采用该单元的通用工具学习成果。

这些引用支持分类框架和内部归属推断，不声称课程发布者陈述了软件属性。须明确采纳后才可物化；若要求独立核实产品属性，当前缺少发布者原文。原状态与 subjects 不变。


## 归属补核

本节补核首次标出的 11 条归属缺口，不重读 24 个 Q 身份，不访问产品网站。首次记录保留在 rows，本次结果另存 subject_followup_observations，每项包含 prior_subjects_review、补核推断和精确 typed basis 候选。前面的初次统计不代表本节之后的最终候选数量。

[实体字段](../../docs/design/model/entities.md)规定 subjects 是实体与一个或多个主题的挂接，不占主题树的位置。它不是 broader，也不是把产品、语言认作学科的成员。补核按这一关系语义处理，不要求课程原文出现本库内部 ID。

| 记录 | 本次结果 | 证据与推断 |
|---|---|---|
| TypeScript、JavaScript、Python、Go、Rust | 五条均可提出完整候选 | FPL 前言说明基础原则适用于多种语言、帮助跨语言理解与选择；已捕获条目识别具体语言。关联主题并不声称课程专门教授该语言 |
| Claude Code、Antigravity | 两条均可提出完整候选 | 原工具依据与既有范围保留；另用 AI 前言的助手、智能体及生成/行动范围支持 AI 主题关联，不让 SE-Tools 独自覆盖两个值 |
| Vite、webpack、ESLint | 三条均可提出完整候选 | 复用条目明确的 JavaScript 构建/分析用途，补用 SPD-Web 的 Web 语言与平台框架范围。是开发用途关联，不声称工具本身是平台，也不只靠实现语言 P277 |
| OpenClaw | AI 值可建议；tools-and-environments 仍阻断 | 项目范围与实际 Q 身份一致，均为通用自主 AI 助手；未取得软件开发用途证据。SE-Tools 的通用学习成果也围绕软件产品开发，不能把任何软件助手都算开发工具 |

本次 10 条形成完整逐值候选，1 条仍有真实用途缺口。原 19 条非 self Wikidata 关联实体中，累计 18 条有完整归属候选；这不是 18 条已经获准。四条无 Wikidata 的补充记录仍单列。OpenClaw 的局部 AI 建议不能覆盖整字段后遗失另一主题。Pydantic 的 v2 映射粒度问题不属于本次归属补核，继续保留。
