# DCMI Application Profiles

本文记录 DCMI Application Profile 相关材料的身份、概念职责和项目适用边界。核对日期为 2026-09-01。

## 材料身份

| 材料 | 版本或日期 | 官方状态 |
|---|---|---|
| [Dublin Core™ Application Profile Guidelines](https://www.dublincore.org/specifications/dublin-core/application-profile-guidelines/) | 2005-09-03 | DCMI 状态表列为 past、note |
| [The Singapore Framework for Dublin Core™ Application Profiles](https://www.dublincore.org/specifications/dublin-core/singapore-framework/) | 2008-01-14 | DCMI 状态表列为 past、note |
| [Guidelines for Dublin Core™ Application Profiles](https://www.dublincore.org/specifications/dublin-core/profile-guidelines/) | 2009-05-18 | DCMI 状态表列为 past、draft |
| [DCMI Abstract Model](https://www.dublincore.org/specifications/dublin-core/abstract-model/) | 2007-06-04 | DCMI 状态表列为 past、recommendation |
| [DCTAP](https://www.dublincore.org/specifications/dctap/) | 汇总页未标版本和发布日期 | 项目入口；下属文档分别记录状态 |
| [DC Tabular Application Profiles Primer](https://www.dublincore.org/specifications/dctap/primer/) | 2023-09-26 | DCMI Community Specification |
| [Elements for DC Tabular Application Profiles](https://www.dublincore.org/specifications/dctap/elements/) | 2022-12-16 | Draft - Request for Comments |
| [Dublin Core™ 规范状态表](https://www.dublincore.org/specifications/dublin-core/) | 页面未标发布日期 | 区分 current 与 past，并为 past 材料标示 recommendation、note 或 draft |
| [DCMI Glossary](https://www.dublincore.org/specifications/dublin-core/usageguide/glossary/) | 2005-11-07；正文标明最后修订于 2004-04 | DCMI Recommended Resource；状态表另将其所属 Using Dublin Core 列为 past、note |
| [GB/T 25100.2―2025 官方信息页](https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D38CB6AE06397BE0A0A601F) | 2025-12-02 发布，2026-07-01 实施 | 推荐性国家标准，现行；修改采用 ISO 15836-2:2019 |

表中的 DCMI 状态以规范状态表为准，而不是以材料正文中的历史自称为准。历史 Recommendation、Note 和 Draft 只支持概念来源与文档结构分析，不支持当前 conformance 声明。

## 阅读范围

| 材料 | 实际读到的位置 |
|---|---|
| Dublin Core™ Application Profile Guidelines | 文档头、Introduction、1 Scope、2 Definitions、4 Attributes of a Term Usage、5 Discussion 中与约束、外部来源和分组结构有关的小节 |
| Singapore Framework | 文档头、1 Introduction、2 Background、3.1 Application Profile、3.2 Components、3.3 Domain Standards and Foundation Standards、4 Examples、References |
| Guidelines for Dublin Core™ Application Profiles | 文档头、目录、2 Framework、3 Functional Requirements、4 Domain Model、5 Metadata Terms、6 Description Set Profile、7 Usage Guidelines、8 Syntax Guidelines |
| DCMI Abstract Model | 文档头、1 Introduction、2.1 Resource Model、2.2 Description Set Model、2.3 Vocabulary Model、3 Descriptions、6 Encoding Guidelines、7 Terminology 中的 syntax encoding scheme |
| DCTAP | 汇总页的简介、项目文档、实现入口和 Background work |
| DCTAP Primer | 文档身份、About this specification、Profile overview、Using a TAP、Statement templates、Shapes |
| DCTAP Elements | 文档身份、Introduction、DCTAP Elements、Concept definitions、Element definitions |
| DCMI 规范状态表 | 页面说明、Specifications of Current Interest、Past Specifications 中本文涉及的各行 |
| DCMI Glossary | 文档身份、application profile、Crosswalk、DCAPS、encoding scheme |
| GB/T 25100.2―2025 官方材料 | 全国标准信息公共服务平台的标准状态、基础信息、采标情况；国家标准全文公开通知中的标准条目 |

## 概念职责

| Designation | 职责边界 | 不是 |
|---|---|---|
| `Application Profile` | 为特定应用选择已有 metadata term，规定使用约束并说明应用语境；可以组合多个词汇表中的 term | 两个 schema 的 metadata crosswalk |
| `DCAP` | DCMI 历史材料中的 Dublin Core Application Profile；在 DCMI 模型内声明使用哪些 metadata term，以及如何作应用特定的约束、编码或解释 | 任意字段配置的别名，也不是本项目已经取得的符合性身份 |
| `Functional Requirements` | 说明 Application Profile 支持的功能及排除在范围外的功能，并为一致性评价提供边界 | 实现清单 |
| `Domain Model` | 说明 metadata 描述的对象及对象之间的基本关系，为 Application Profile 划定基本范围 | YAML layout |
| `Description Set Profile`／`DSP` | 约束 description set 中可描述的 resource、可用 property、value 的引用方式，以及 property 和 value 的结构约束 | 版本管理、词汇定义或面向人的使用说明 |
| `Usage Guidelines` | 在 application context 中说明 metadata 创建者如何以及为何使用 property，并解释创建记录时的选择 | 改变来源 term 的语义 |
| `Encoding Syntax Guidelines` | 说明整个 metadata record 如何用具体 machine-readable syntax 表达 | 单个 value 的 datatype |
| `Syntax Encoding Scheme` | 规定一组字符串到一组 resource 的映射规则；在 DCAM 中属于 literal 的 class，可由 URI 标识 | Markdown、YAML、目录或整份 record 的编码格式 |
| `metadata crosswalk` | 表达两个或更多独立 metadata standard、schema 或 profile 之间的关系与等价对应 | 同一应用内部把一个 field 绑定到一个 property |

Application Profile 使用 term 时不取得改写其定义的权力。Singapore Framework 明确把 term 的语义放在独立于 Application Profile 的来源定义中；Application Profile 负责选择、规则、约束和说明。

## 分层关系

Singapore Framework 把材料分成三个层次。Application Profile 的文档组件位于应用层，包括必需的 Functional Requirements、Domain Model、Description Set Profile，以及可选的 Usage Guidelines 和 Encoding Syntax Guidelines。Domain standards 层提供可复用的 metadata vocabulary、domain model、DCAM 和具体编码规范。RDF 与 RDFS 位于 foundation standards 层。

这些层次不能折叠。Domain Model 先界定被描述对象和关系；Description Set Profile 再约束依据该模型形成的 description、property 和 value；Usage Guidelines 面向创建者解释如何使用；Encoding Syntax Guidelines 才说明整个 record 的具体语法。Syntax Encoding Scheme 位于 value string 层，不能替代 record 编码指南。

DCTAP 是较新的表格化 Application Profile 模型。Primer 的 Community Specification 身份只覆盖该文档自身；Elements 仍是 Draft - Request for Comments。二者不能回溯性地把 Singapore Framework、DSP 或 DCAM 变成当前规范，也不能让任意表格自动获得 DCTAP conformance。

## 规范状态

DCMI 当前状态表只列出少量 current specifications，并明确说明很多 metadata model、usage guideline 和 encoding syntax 材料已经被 superseded。本文涉及的 2005 Application Profile Guidelines、2008 Singapore Framework、2009 Profile Guidelines 和 2007 DCAM 均在 past specifications 中。

因此，2005 Application Profile Guidelines 的 Note、2008 Singapore Framework 的 Note、2009 Profile Guidelines 的 Draft，以及 2007 DCAM 的 Recommendation，只作为历史概念和文档结构依据。本文不据这些材料宣称任何当前 DCAP、DCAM 或 DSP conformance。

DCTAP 必须逐文档记录状态。2023-09-26 Primer 是 DCMI Community Specification；2022-12-16 Elements 是 Draft - Request for Comments。汇总页本身没有给出统一状态，不能把 Primer 的状态扩大到全部 DCTAP 材料。

## 译名依据

结论：`UNVERIFIED`。

GB/T 25100.2―2025 官方信息页直接证明标准号、名称、现行状态、发布日期、实施日期和修改采用 ISO 15836-2:2019。国家标准全文公开通知也列出该标准，但本次未取得可阅读的正式正文，因而没有定位到 `Application Profile` 的对应文字、页码、条款和原句位置。

检索摘要、参考文献题名、起草稿和二手论文都不足以完成正文核验。项目保留 `Application Profile`，不登记中文名称，也不把 `Dublin Core Application Profile`、`Description Set Profile`、`Encoding Syntax Guidelines` 或 `metadata crosswalk` 自动套用同一中文译名。

## 项目边界

当前 kb-design 只能借用 Application Profile 的职责分解和分层框架，用来区分功能边界、描述对象、字段约束、使用说明和值与 record 的编码层次。本文没有建立正式 Application Profile，也不使任何草案、映射或表格生效。

kb-design 不宣称 DCAP、DCAM 或 DCTAP conformance。使用历史 DCMI 材料安排文档结构，不等于满足相应历史规范；使用表格记录 property 或约束，也不等于采用 DCTAP。

Obsidian field binding 是本项目内部把 field 绑定到 property 或其他既定对象的应用映射，不是 metadata crosswalk。只有在两个独立 metadata standard、schema 或 profile 之间记录关系与等价对应时，才进入 metadata crosswalk 的职责范围。

## 未读范围

- GB/T 25100.2―2025 正式正文未取得，未读其引言、范围、条款、附录和参考文献；官方信息页与全文公开通知不能替代正文。
- Application Profile Guidelines、Profile Guidelines 和 DCAM 没有逐字通读示例、附录与全部参考文献，只采用“阅读范围”列出的相关小节。
- Singapore Framework 的图只按正文说明理解，没有据图增加正文未说明的关系。
- DCTAP Primer 与 Elements 只读了本项目所需小节；Cookbook、下载模板、程序实现和 GitHub 工作记录未读。
- DCMI Glossary 最后修订于 2004-04，只用来界定历史 Crosswalk 与 Application Profile 用法，不作为当前规范状态依据。

## 权威来源

- [Dublin Core™ Application Profile Guidelines](https://www.dublincore.org/specifications/dublin-core/application-profile-guidelines/)
- [The Singapore Framework for Dublin Core™ Application Profiles](https://www.dublincore.org/specifications/dublin-core/singapore-framework/)
- [Guidelines for Dublin Core™ Application Profiles](https://www.dublincore.org/specifications/dublin-core/profile-guidelines/)
- [DCMI Abstract Model](https://www.dublincore.org/specifications/dublin-core/abstract-model/)
- [DCTAP](https://www.dublincore.org/specifications/dctap/)
- [DC Tabular Application Profiles Primer](https://www.dublincore.org/specifications/dctap/primer/)
- [Elements for DC Tabular Application Profiles](https://www.dublincore.org/specifications/dctap/elements/)
- [Dublin Core™ 规范状态表](https://www.dublincore.org/specifications/dublin-core/)
- [DCMI Glossary](https://www.dublincore.org/specifications/dublin-core/usageguide/glossary/)
- [GB/T 25100.2―2025 官方信息页](https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D38CB6AE06397BE0A0A601F)
- [国家标准全文公开通知](https://openstd.samr.gov.cn/bzgk/std/nd?no=2602)
