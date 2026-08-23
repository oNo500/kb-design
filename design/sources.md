# 来源分级与复核

知识库里每一条事实性断言都要能追到来源。来源会过时,过时的速度取决于它的变更方式,所以按变更方式分档,各档定不同的复核周期。

本文是设计正文,约束仓库内所有内容。各目录的写作约定(如 `concepts/CONVENTIONS.md`)只引用本文,不另定规则。

## 分档

分档依据是**来源如何变更**,不是来源的权威程度。权威程度决定能不能引,变更方式决定多久要回头看。

| 档 | 判据 | 例子 | 内容复核 | 触发 |
|---|---|---|---|---|
| **de-jure** | 有正式发布流程和版本标识,变更必出新版 | ISO、GB/T、W3C Recommendation、IETF RFC | 24 个月 | 新版发布(需登记探测方式) |
| **de-facto** | 行业默认,无发布流程,可无通知漂移 | schema.org、Wikidata 数据、社区 wiki、Wikipedia | 12 个月 | — |
| **vendor** | 单一厂商文档,随产品迭代 | Neo4j 文档、Obsidian 文档 | 定义类 6 个月;接口类 3 个月或不引 | 产品大版本 |
| **archival** | 发表后内容固定 | 论文、已出版的书、带日期的博文 | 不复核内容 | — |

分档说明:

- 组织类型不决定档位。W3C 不是标准化组织,但 Recommendation 有正式流程和版本,归 de-jure;W3C Working Draft 和 Candidate Recommendation 尚未定稿,归 de-facto
- 同一网站可能跨档。Wikidata 的数据模型文档是 de-facto,某个具体实体(如 Q192490)的数据是 de-facto,但引用它的论文是 archival
- vendor 档要区分引的是**定义**(厂商对某概念的解释,变得慢)还是**接口**(API、配置、UI,变得快)。接口类原则上不进概念文和设计正文
- de-facto 和 vendor 只作入口和例证,不作定义来源。定义来源只取 de-jure 和 archival

## 链接存活与内容有效分开查

两件事不同,周期不同:

| 检查 | 内容 | 周期 | 方式 |
|---|---|---|---|
| 链接存活 | URL 是否可达、是否重定向到无关页 | 3 个月 | 脚本,所有档一样 |
| 内容有效 | 引用的事实是否仍成立、是否已有新版 | 按档 | 人工,按上表 |

链接失效时优先找官方新地址,其次 DOI / arXiv,最后 archive.org 快照。archival 档写入时就应优先使用 DOI、arXiv 或带日期的永久链接。

## 来源记录的字段

每条来源在引用处附带:

| 字段 | 必填 | 说明 |
|---|---|---|
| `tier` | 是 | de-jure / de-facto / vendor / archival |
| `version` | de-jure、vendor 必填 | 引的是哪一版:`ISO 25964-1:2011`、`SKOS 2009-08-18`、`Neo4j 5.x` |
| `checked` | 是 | 上次核对内容的日期,ISO 8601 |
| `watch` | de-jure 必填 | 探测新版的方式,见下节 |
| `status` | 否 | 已知的变更动态,如「修订中,FDIS,预计 2026」 |

写法:对标体系集中登记在 `vocab/sources.yaml`(结构见 [design/topics.md §7](topics.md));概念文和笔记里引用的文献暂按文末表标注。

## de-jure 来源的探测方式

「事件触发」要有探测手段,否则是愿望。每个 de-jure 来源登记一个可脚本化的探测点:

| 来源 | 探测点 | 看什么 |
|---|---|---|
| ISO | `https://www.iso.org/standard/<id>.html` | 页面状态字段(Published / Under review / Withdrawn),以及「将被替代」提示。注意 iso.org 对脚本返回 403,需带浏览器 UA 或改用 iTeh 镜像页 |
| GB/T | 全国标准信息公共服务平台 `std.samr.gov.cn` 详情页 | 标准状态(现行 / 废止)、替代标准 |
| W3C | `https://www.w3.org/TR/<shortname>/` | 页头的 "This version" 日期和 "Latest published version" 链接 |
| IETF | `https://www.rfc-editor.org/info/rfc<n>` | Obsoleted by / Updated by |
| NISO | `https://www.niso.org/publications/<id>` | 状态与年份 |

探测脚本每月跑一次,状态字段变化即报警。脚本尚未写,见待办。

## 复核时做什么

1. 打开来源,确认引用的事实仍在且未改
2. 有新版:读变更说明,判断是否影响本库引用的部分;影响则改正文,不影响则只更新 `version` 和 `checked`
3. 来源被撤销或替代:找替代来源,改引用;找不到则把断言标为「来源已失效」,不删
4. 更新 `checked`

## 与收词依据的关系

本文讲「事实从哪来、凭什么信」。词表建设里还有一个平行问题「词从哪来、凭什么收」,即 ISO 25964 / Z39.19 说的 warrant(文献依据、用户依据、组织依据)。两者都是「依据」,分别在本文和词表治理文档里处理;后者待写。

## 待办

- 链接存活脚本(`scripts/check-links`),3 个月跑一次
- de-jure 探测脚本,每月跑一次
- 给 `concepts/` 和 `sources/` 已有文章的来源补 `tier` 和 `checked`
- 定来源记录的写法(行内 / 文末表 / 独立登记文件)
- `concepts/CONVENTIONS.md` 的「链接与引用」节改为引用本文
