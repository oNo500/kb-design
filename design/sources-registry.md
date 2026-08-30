# 来源名称规范表

`vocab/sources.yaml` 登记本库引用的外部知识体系和词表，每个外部实体一条记录。按 ISO 25964-2 §23，它是一份名称规范表：用一致名称标识特定实体；这里的实体是各外部体系。所有词表的 `source` 和 `match.source` 只能使用已登记 id。理论见[词表映射](../concepts/vocabulary-mapping.md)和[知识体系](../concepts/body-of-knowledge.md)。

## 记录

```yaml
- id: cwe
  entity: cwe                    # 实体表中的 standard；名称、分级、版本和 URL 记在那里
  role: [mapping, structure, group]
  checked: 2026-08-20            # 上次核对作为来源使用的条目与版本
```

名称、`tier`、`version` 和 `url` 记在[命名实体词表](entities.md)，本表不重复。`entity` 必须指向 `kind` 为 `standard` 或 `publication` 的实体。

`role` 可以多选。

| role | 含义 | 条件 | 例 |
|---|---|---|---|
| `mapping` | 可作 `match` 目标 | 条目有编号或永久 URL | CWE、RFC、ASVS、SWEBOK、CS2023、ISO、MDN 页面 |
| `structure` | 可复制为数组 | 含 `mapping`，有自己的分层，且该层条目有编号或稳定名称 | CS2023 知识领域、SWEBOK 章、ASVS 章、ATT&CK 战术、CWE 顶层类别、GB/T 13745 学科 |
| `group` | 由映射派生概念组，组名使用体系名 | 含 `mapping` | OWASP Top 10、MDN Curriculum |
| `candidate` | 只用于发现待审字符串或表达线索 | — | roadmap.sh、teachyourselfcs、CMU 15-445、DB-Engines 榜 |

`candidate` 与其余三个角色互斥。这个角色只说明来源可用于发现待审表达，不赋予字符串形式依据、概念身份或 `candidate` 状态；概念判断、依据核验和记录建档由后续维护流程完成。

复核周期按实体的 `tier` 执行，见[维护](maintenance.md)。

`role` 含 `structure` 时，来源实体的 `tier` 必须是 de-jure，或为有版本号的 de-facto。没有版本号的 de-facto 只作映射；vendor 只作映射；archival 不作来源。依据是组织依据：本库只把有发布流程或版本标识的体系作为结构来源。

## 来源用法

一个外部体系可以在本库同时承担以下用法。

| 用法 | 本库形式 | 所需 role | 记录位置 |
|---|---|---|---|
| 复制 | 某概念下的一个数组，成员为本地概念 | `structure` | `arrays` 登记和概念的 `source` |
| 映射 | 概念的一条 `match` | `mapping` | 概念的 `match` |
| 派生概念组 | 映射到该体系的全部本地概念 | `group` | 不登记，自动计算 |

规则如下。

1. 复制的概念必须映射回来源条目。`source: asvs` 记录来历，`match: {source: asvs, id: V6, rel: exactMatch}` 记录对应条目。来源改版后章节号可能变化，来历与对应关系不能互相替代。
2. `role` 含 `structure` 的来源在对应概念下完整复制到第 3 层，初始状态均为 `unassigned`，见[层级结构](hierarchy.md)规则 3–6。同一视角只取一个来源，见规则 13。
3. 派生概念组是已映射内容的视图，成员只来自本库已有概念，不能显示尚未建立或映射的缺口。它可以与复制并存，不能替代复制。

## 映射关系

映射落在概念层，不在第 2 层级别建立。`rel` 直接使用 SKOS 的五种关系。

| rel | 含义 |
|---|---|
| `exactMatch` | 同一概念，可以互换；传递 |
| `closeMatch` | 基本同一；不传递。不能确认完全一致时使用 |
| `broadMatch` | 外部概念更宽 |
| `narrowMatch` | 外部概念更窄 |
| `relatedMatch` | 相关 |

`match.id` 是外部体系中的条目标识，例如 CWE-89、RFC 9110 §8.1、ASVS V5.1；没有编号时写永久 URL。

## 首批来源

下表按[层级结构](hierarchy.md)的数组表和各概念映射需求列出首批来源及拟定 role。版本在登记时核对。

| id（拟） | 名称 | role | 用在 |
|---|---|---|---|
| gbt-13745 | GB/T 13745-2009 学科分类与代码 | mapping, structure | 顶层映射；除 computing 外七个顶层的第 2、3 层 |
| cs2023 | ACM／IEEE-CS／AAAI Computer Science Curricula 2023 | mapping, structure | computing 第 2 层，即 17 个知识领域；各知识领域的第 3 层 |
| swebok | IEEE-CS SWEBOK Guide v4.0 | mapping, structure | software-engineering 下的数组 |
| acm-ccs | ACM Computing Classification System 2012 | mapping | 映射 |
| asvs | OWASP ASVS 5.0 | mapping, structure | security 数组 |
| cwe | MITRE CWE | mapping, structure, group | security 数组；缺陷的派生组 |
| attack | MITRE ATT&CK（v19.2，Enterprise，15 个战术） | mapping, structure | security 数组 |
| owasp-top10 | OWASP Top 10 | mapping, group | 映射；派生组 |
| owasp-llm-top10 | OWASP Top 10 for LLM Applications 2025 | mapping, structure, group | artificial-intelligence 数组 |
| atlas | MITRE ATLAS（2026.07，16 个战术；按月发布） | mapping, structure | artificial-intelligence 数组 |
| nist-ai-rmf | NIST AI RMF 1.0 | mapping | 映射 |
| anthropic-docs | Anthropic 文档 | mapping | 映射 |
| rfc-1122 | RFC 1122 | mapping, structure | networking-and-communication 下的数组 |
| rfc-http | RFC 9110–9114 | mapping | 映射 |
| osi | ISO/IEC 7498-1 OSI 参考模型 | mapping | 映射 |
| mdn | MDN 技术参考 | mapping | 映射；Web Platforms 为第 3 层，其下不复制 |
| mdn-curriculum | MDN Curriculum | candidate | 发现待审表达 |
| iso-25964 | ISO 25964-1／-2 | mapping | 映射 |
| z39-19 | ANSI/NISO Z39.19 | mapping | 映射 |
| skos | W3C SKOS | mapping | 映射 |
| roadmap-sh | roadmap.sh | candidate | 发现待审表达 |
| teachyourselfcs | teachyourselfcs.com | candidate | 发现待审表达 |
| cmu-15-445 | CMU 15-445 | candidate | 发现待审表达 |
| db-engines | DB-Engines 排名 | candidate | 发现待审表达 |
| wikidata | Wikidata | mapping | 命名实体词表的主要映射目标 |

## 待定事项

- MDN 技术参考没有版本号，`version` 怎样记录（抓取日期？）；Web 内容是否需要例外复制
- `mdn-curriculum` 当前为 `candidate`，但有稳定模块名；是否同时赋予 `group`
