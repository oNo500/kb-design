# 术语标准

## 阅读范围

本笔记核对以下官方页面，最近核对日期为 2026-08-31。“公开页面已读”包括页面显示的编号、标题、摘要、状态和生命周期；“正文”指标准的规范性或资料性内容，不把商品页摘要算作正文。国家标准页面所列采标关系只用于记录标准之间的采用关系，不用于推断术语、定义或条款逐项等同。

| 材料 | 版本状态 | 已读范围 | 未读范围 |
|---|---|---|---|
| [ISO 704:2022 — Terminology work — Principles and methods](https://www.iso.org/standard/79077.html) | 第 4 版，2022-07；Published，阶段 60.60 | 编号、标题、摘要、一般信息和生命周期 | 80 页正文未取得 |
| [ISO 1087:2019 — Terminology work and terminology science — Vocabulary](https://www.iso.org/standard/62330.html) | 第 2 版，2019-09；Published，2025 年确认，阶段 90.93 | 编号、标题、摘要、一般信息和生命周期 | 38 页正文未取得 |
| [术语工作及术语科学 词汇](https://std.samr.gov.cn/gb/search/gbDetailed?id=33D40F1160ED5D92E06397BE0A0A5B93) | GB/T 15237-2025，现行；等同采用 ISO 1087:2019 | 基础信息、现行状态和采标关系 | 官方文本页不提供正文 |
| [ISO 10241-1:2011 — Terminological entries in standards — Part 1](https://www.iso.org/standard/40362.html) | 第 1 版，2011-04；Published，2022 年确认，阶段 90.93 | 编号、标题、摘要、一般信息和生命周期 | 57 页正文未取得 |
| [标准起草规则 第 1 部分：术语](https://std.samr.gov.cn/gb/search/gbDetailed?id=14156507D1FC0337E06397BE0A0AE656) | GB/T 20001.1-2024，现行；非等效采用 ISO 10241-1:2011 | 基础信息、现行状态和采标关系 | 官方文本页不提供正文 |
| [ISO 26162-1:2019 — Management of terminology resources — Terminology databases — Part 1](https://www.iso.org/standard/71941.html) | 第 1 版，2019-11；Published，2025 年确认，阶段 90.93 | 编号、标题、摘要、一般信息和生命周期 | 19 页正文未取得 |
| [ISO 26162-3:2023 — Management of terminology resources — Terminology databases — Part 3](https://www.iso.org/standard/80464.html) | 第 1 版，2023-01；Published，阶段 60.60 | 编号、标题、摘要、一般信息和生命周期 | 21 页正文未取得 |
| [ISO 30042:2019 — Management of terminology resources — TermBase eXchange (TBX)](https://www.iso.org/standard/62510.html) | 第 2 版，2019-04；Published，待修订，阶段 90.92 | 编号、标题、摘要、一般信息、生命周期和后继项目链接 | 43 页正文未取得 |
| [术语资源管理 术语数据库交换（TBX）](https://std.samr.gov.cn/gb/search/gbDetailed?id=1E5A13A77F9BBC8DE06397BE0A0A87E8) | GB/T 44227-2024，现行；修改采用 ISO 30042:2019 | 基础信息、现行状态和采标关系 | 官方文本页不提供正文 |
| [ISO/TR 24633-1:2026 — Companion to TermBase eXchange (TBX) — Part 1](https://www.iso.org/standard/85521.html) | 第 1 版，2026-05；Published，阶段 60.60 | 商品页摘要；[OBP](https://www.iso.org/obp/ui?_escaped_fragment_=iso:std:iso:tr:24633:-1:ed-1:v1:en)公开的引言、第 1～3 章、第 6 章和参考文献 | OBP 未公开的正文未取得 |
| [TBX-Basic 方言版本](https://ltac-global.github.io/TBX-Basic_dialect/) | 1.2.1，2023-02-09 | 版本、变更说明和正式下载入口 | 下载包尚未纳入本库，也未固定摘要 |
| [TBX-Basic DCA 约束](https://github.com/LTAC-Global/TBX-Basic_dialect/blob/master/DCA/TBX-Basic_DCA.sch) | TBX-Basic 项目当前公开文件；发布页把 1.2.1 列为最新发行版 | 根元素约束、允许的数据类目、层次和枚举约束 | 未把 `master` 当作固定版本；实施时须绑定 1.2.1 发行包和摘要 |
| [TBX-Basic Namespace](https://www.tbxinfo.net/ns/dct/basic) | 页面未显示独立版本号 | 页面列出的层次、数据类目和取值 | 页面链接的下载包未纳入本库 |
| [TBX 开发者资源](https://www.tbxinfo.net/developer-resources/?id=2) | 页面 2023-05-26 更新 | 官方核心模式、TBX-Basic Schematron 入口和三层验证说明 | 未执行页面链接的验证资源 |

ISO/TR 24633-1:2026 的参考文献直接列出 LTAC Global 的 TBX Resources 和 TBX-Basic；TBX 开发者资源说明 DatCatInfo 由 LTAC Global／TerminOrgs 维护，并标明其 ISO/TC 37 liaison 身份。本笔记因此把上述 TBX Resources 页面和 LTAC Global 仓库作为明确的官方伴随材料，不把其他教程、厂商映射或未登记的私有方言作为设计依据。

## 基础术语

[ISO 704:2022](https://www.iso.org/standard/79077.html) 的公开摘要只确认其描述 `objects`、`concepts`、`definitions` 和 `designations` 之间的联系，并说明 `terms` 和 `proper names` 的形成原则以及 `definitions` 的撰写原则。摘要没有给出这些项目的术语条目或定义，因此本笔记只保留页面实际出现的原文，不据此扩写原则。

[ISO 1087:2019](https://www.iso.org/standard/62330.html) 的公开摘要只说明该标准给出术语工作和术语科学的基础术语及定义，并排除术语工作中计算机应用所特有的术语及定义。摘要没有展示具体术语条目。GB/T 15237-2025 的官方页面确认等同采用关系，但正文未取得；本笔记不从采标关系推断术语或定义逐项等同。

## 条目结构

[ISO 10241-1:2011](https://www.iso.org/standard/40362.html) 的公开摘要支持以下范围：标准中术语条目的起草和结构；单语、多语术语条目及其索引；`terms` 和 `other designations` 中可能出现的字母、数字、数学符号、排印符号、句法符号及标准化符号。摘要没有公开条目组成、排列次序、必选性、重复次数或具体版式规则，因此本笔记不据此制定字段结构。

GB/T 20001.1-2024 的官方页面只确认非等效采用 ISO 10241-1:2011。没有取得两份正文，不能从该关系推断条款或术语逐项对应。

## 数据库

[ISO 26162-1:2019](https://www.iso.org/standard/71941.html) 的公开摘要把范围限定为不依赖具体实现和使用场景的术语数据库设计原则，目标是支持高质量术语的创建、处理和使用。摘要说明其最大范围是分布式、多语术语管理，也可用于较小方案；没有公开数据库字段、关系、基数或实现格式。

[ISO 26162-3:2023](https://www.iso.org/standard/80464.html) 的公开摘要把范围限定为术语数据库维护中与内容有关的方面，重点包括术语数据集合的内容、数据质量评价、互操作性和持续改进；文本语料库管理和术语抽取工具不在范围内。摘要没有公开维护程序、评价指标、角色分工或验收阈值。

## 交换边界

[ISO 30042:2019](https://www.iso.org/standard/62510.html) 的公开摘要说明该标准解释基本概念，描述元模型、数据类目及 DCA、DCT 两种 XML 样式，并规定定义 TBX 方言的方法；该版详细描述 TBX-Core，并把其他行业方言排除在正文范围外。摘要支持把 TBX 作为术语数据交换框架，不支持从摘要还原全部元模型、XML 约束或一致性要求。

[ISO/TR 24633-1:2026](https://www.iso.org/obp/ui?_escaped_fragment_=iso:std:iso:tr:24633:-1:ed-1:v1:en) 把 ISO 30042:2019 称为 TBX 3.0，并说明所有 TBX 方言共享核心结构，再用数据类目模块补充不同环境所需的约束。其公开定义区分 DCA 与 DCT：DCA 把大多数数据类目写成元素的 `type` 属性值，DCT 把大多数数据类目写成 XML 元素名。该报告还把 TBX-Basic 称为用于内容生产环境的常见方言，并要求伴随资源明确其适用的 TBX 版本以及核心结构或具体方言。

这些材料没有规定本库的内部 YAML，也没有要求内部数据库采用 TBX 元素名。TBX 方言是一套受核心结构、数据类目模块和其他相关约束共同限制的交换表示；内部模型与某个方言字段相似，不能单独证明导出文件符合该方言。

## 方言材料

[TBX 方言页面](https://www.tbxinfo.net/tbx-dialects/?id=0)把方言分为公开和私有两类，并把 TBX-Basic 列为公开方言。公开方言表示维护和一般使用定位，不表示它是 ISO 30042 本身、处于公共领域、适合所有术语数据库或具有相同许可。

[TBX-Basic 方言版本](https://ltac-global.github.io/TBX-Basic_dialect/)把 1.2.1 记为 2023-02-09 的方言发行版。这个版本号属于 TBX-Basic，不是 ISO 30042 的版次，也不是 TBX 代际编号。发行说明指出 1.2.1 的 RNG 只执行核心数据模型约束，Schematron 执行全部方言特有约束。

发行页同时提供 DCA 与 DCT 材料，证明一个方言可以有两种表示样式。它不能证明本库应选择 TBX-Basic，也不能在没有接收方和交换需求时决定 DCA 或 DCT。

本轮没有取得 1.2.1 发行 ZIP 和定义 PDF 的字节，没有核定 ZIP 内清单、逐文件 SHA-256、DCT 固定资源、发行资产是否曾替换，以及各文件的复制和再分发许可。GitHub `master` 或 `main` 上的当前文件不能代替发行版锁。

## 验证范围

[TBX 开发者资源](https://www.tbxinfo.net/developer-resources/?id=2)把 XML 检查分成三层：XML 良构、TBX 核心结构、指定方言的集成约束。TBX-Basic 1.2.1 的发行说明进一步明确核心 RNG 与方言 Schematron 的职责分工。因此，声称一个文件是本设计选定的 TBX-Basic DCA 导出物，至少需要同时通过 XML 良构、固定的 TBX Core RNG 和固定的 TBX-Basic DCA Schematron；只通过 XML 解析或只匹配根元素不够。

这些外部验证只证明输出满足所绑定的 XML 与方言约束，不证明内部字段已经完整、正确地映射。字段覆盖、逐值对应、信息损失和发布快照绑定仍须由本库自己的导出契约验证，并与外部模式验证分开报告。

## 版本状态

核对日可确认的 TBX 相关状态如下。

| 材料 | 核对日状态 |
|---|---|
| ISO 30042:2019 | 第 2 版，Published；待修订，阶段 90.92 |
| ISO/CD 30042 | 拟替代 ISO 30042:2019 的第 3 版项目，Under development，阶段 30.60 |
| ISO/TR 24633-1:2026 | 第 1 版，Published，阶段 60.60 |
| ISO/WD TR 24633-2.2 | RNG schema for TBX core 项目，Under development，阶段 20.60 |
| TBX-Basic | 公开发行版 1.2.1，2023-02-09 |
| GB/T 44227-2024 | 现行，修改采用 ISO 30042:2019 |

修订项目与已发布版本必须分开。ISO/CD 30042 和 ISO/WD TR 24633-2.2 的项目页不能替代 ISO 30042:2019、ISO/TR 24633-1:2026 或本设计固定的 TBX-Basic 1.2.1 资源；后继材料发布后也不能自动改变既有导出契约。

## 未读范围

- ISO 704:2022、ISO 1087:2019、ISO 10241-1:2011、ISO 26162-1:2019、ISO 26162-3:2023 和 ISO 30042:2019 的收费正文未取得；本笔记不补写未公开条款。
- GB/T 15237-2025、GB/T 20001.1-2024 和 GB/T 44227-2024 的正文未取得；采标关系不能替代逐项核对。
- ISO/TR 24633-1:2026 的 OBP 只公开部分内容；未公开的第 4～5 章、第 7～9 章不作为本设计的条款依据。
- TBX-Basic 1.2.1 的发行包尚未纳入本库并计算摘要；实施必须固定发行包、Core RNG、DCA Schematron 及其 SHA-256 后才可验证或导出。
- 本笔记没有读取或采用私有 TBX 方言、厂商 TBX 映射、导入器行为或往返兼容性声明。
