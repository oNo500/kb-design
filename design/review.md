# 来源复核

本库引用的每一条事实都要能追到来源;来源会过时,过时的速度取决于它怎么变。实体的 `tier` 记录变更方式(见[命名实体词表](entities.md)),本文定按 `tier` 的复核周期、链接检查、新版探测和复核流程。

## 复核周期

| tier | 内容复核 | 触发 |
|---|---|---|
| `de-jure` | 24 个月 | 新版发布,需登记探测方式 |
| `de-facto` | 12 个月 | — |
| `vendor` | 定义类 6 个月;接口类 3 个月,或不引 | 产品大版本 |
| `archival` | 不复核内容 | — |

说明:

- 组织类型不决定档位。W3C Recommendation 有正式流程和版本,归 de-jure;W3C Working Draft 和 Candidate Recommendation 尚未定稿,归 de-facto
- vendor 档区分引的是定义(厂商对某概念的解释,变得慢)还是接口(API、配置、UI,变得快)。接口类原则上不进概念文和设计文档
- de-facto 和 vendor 只作入口和例证,不作定义来源。定义来源只取 de-jure 和 archival

## 链接存活与内容有效

两件事分开查:

| 检查 | 内容 | 周期 | 方式 |
|---|---|---|---|
| 链接存活 | URL 可达,且未重定向到无关页 | 3 个月 | 脚本,所有档一样 |
| 内容有效 | 引用的事实仍成立,是否已有新版 | 按上表 | 人工 |

链接失效时优先找官方新地址,其次 DOI / arXiv,最后 archive.org 快照。archival 档写入时就用 DOI、arXiv 或带日期的永久链接。

## de-jure 的新版探测

「新版触发」要有探测手段。每个 de-jure 实体登记一个可脚本化的探测点,记在实体的 `watch` 字段:

| 发布方 | 探测点 | 看什么 |
|---|---|---|
| ISO | `https://www.iso.org/standard/<id>.html` | 状态字段(Published / Under review / Withdrawn)和「将被替代」提示。iso.org 对脚本返回 403,带浏览器 UA 或改用 iTeh 镜像页 |
| GB/T | `std.samr.gov.cn` 详情页 | 标准状态(现行 / 废止)、替代标准 |
| W3C | `https://www.w3.org/TR/<shortname>/` | "This version" 日期和 "Latest published version" 链接 |
| IETF | `https://www.rfc-editor.org/info/rfc<n>` | Obsoleted by / Updated by |
| NISO | `https://www.niso.org/publications/<id>` | 状态与年份 |

探测脚本每月跑一次,状态变化即报警。

## 复核流程

1. 打开来源,确认引用的事实仍在且未改
2. 有新版:读变更说明,判断是否影响本库引用的部分;影响则改正文,不影响则只更新实体的 `version` 和 `checked`
3. 来源被撤销或替代:找替代来源,改引用;找不到则把断言标为「来源已失效」,不删
4. 更新 `checked`

## 与收词依据的关系

本文讲「事实从哪来、凭什么信」;词表建设里平行的问题是「词从哪来、凭什么收」,即 warrant,见[词表的建设与维护](../concepts/vocabulary-construction.md)。分级本身的依据是组织依据——本库获取与信任知识的方式,见[命名实体词表](entities.md)。

## 待办事项

- 链接存活脚本 `scripts/check-links`,3 个月跑一次
- de-jure 探测脚本,每月跑一次
- 概念文和笔记里引用的文献登记为实体,引用处改为实体 id
