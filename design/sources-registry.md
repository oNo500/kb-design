# 来源名称规范表

`vocab/sources.yaml`:本库引用的外部知识体系和词表,每个一条。按 ISO 25964-2 §23,它是一份名称规范表——为一致地命名特定实体的受控词表,这里的实体是各知识体系。所有词表的 `source` 和 `match.source` 只能写这里有的 id。理论见[词表映射](../concepts/vocabulary-mapping.md)、[知识体系](../concepts/body-of-knowledge.md)。

## 记录

```yaml
- id: cwe
  name: MITRE Common Weakness Enumeration
  role: [mapping, structure, group]
  version: "4.20"
  checked: 2026-08-20
  url: https://cwe.mitre.org/
```

`role` 可多选:

| role | 含义 | 条件 | 例 |
|---|---|---|---|
| `mapping` | 可作 `match` 目标 | 条目有编号或永久 URL | CWE、RFC、ASVS、SWEBOK、CS2023、ISO、MDN 页面 |
| `structure` | 可借入为数组 | 含 `mapping`,且有自己的分层,该层条目有编号或稳定名称 | CS2023 知识领域、SWEBOK 章、ASVS 章、ATT&CK 战术、CWE 顶层类别、GB/T 13745 学科 |
| `group` | 由映射派生一个概念组,组名即体系名 | 含 `mapping` | OWASP Top 10、MDN Curriculum |
| `candidate` | 只作候选词来源 | — | roadmap.sh、teachyourselfcs、CMU 15-445、DB-Engines 榜 |

`candidate` 与其余三者互斥:条目不稳定无编号,只用来发现词。

复核周期的分档见[来源分级草案](drafts/sources.md),草案生效前只记 `version` 和 `checked`。借入来源的进一步条件(分级、版本要求)留待治理方案。

## 三种用法

一个外部体系在本库可以同时有三种用法:

| 用法 | 本库里的形式 | 需要的 role | 记在哪 |
|---|---|---|---|
| 借入 | 某概念下的一个数组,成员是本地概念 | `structure` | `arrays` 登记 + 概念的 `source` |
| 映射 | 概念的 `match` 条目 | `mapping` | 概念的 `match` |
| 派生概念组 | 映射到该体系的全部概念 | `group` | 不登记,自动 |

规则:

1. 借入的概念必须映射回源头。`source: asvs` 说来历,`match: {source: asvs, id: V6, rel: exactMatch}` 说对应哪一条;改版后章节号可能变,两者不互相替代
2. 凡 `role` 含 `structure` 的来源,起步就在对应概念下全部借入,借到第 3 层,全部未标引——[层级结构](hierarchy.md)规则 3–6。同一视角只取一个来源(规则 13)
3. 派生概念组是已映射内容的视图,成员只有本库已有的概念,暴露不了盲区;它与借入并存,不能替代借入

## 映射关系

概念级映射,不在第 2 层级别做。`rel` 直接用 SKOS 的五种:

| rel | 意思 |
|---|---|
| `exactMatch` | 同一概念,可互换;传递 |
| `closeMatch` | 基本同一;不传递。拿不准时用这个 |
| `broadMatch` | 外部概念更宽 |
| `narrowMatch` | 外部概念更窄 |
| `relatedMatch` | 相关 |

`match.id` 是外部体系里的条目标识(CWE-89、RFC 9110 §8.1、ASVS V5.1),没有编号的写 URL。

## 首批来源

按[层级结构](hierarchy.md)的数组表和各概念的映射需要,首批登记的来源及拟定的 role。版本在登记时核对。

| id(拟) | 名称 | role | 用在 |
|---|---|---|---|
| gbt-13745 | GB/T 13745-2009 学科分类与代码 | mapping, structure | 顶层映射;除 computing 外七个顶层的第 2、3 层 |
| cs2023 | ACM/IEEE-CS/AAAI Computer Science Curricula 2023 | mapping, structure | computing 第 2 层(17 个知识领域)及各领域第 3 层 |
| swebok | IEEE-CS SWEBOK Guide v4.0 | mapping, structure | software-engineering 下的数组 |
| acm-ccs | ACM Computing Classification System 2012 | mapping | 映射 |
| asvs | OWASP ASVS 5.0 | mapping, structure | security 数组 |
| cwe | MITRE CWE | mapping, structure, group | security 数组;缺陷的派生组 |
| attack | MITRE ATT&CK | mapping, structure | security 数组 |
| owasp-top10 | OWASP Top 10 | mapping, group | 映射;派生组 |
| owasp-genai | OWASP GenAI / LLM Top 10 | mapping, structure | artificial-intelligence 数组(划分特征待核) |
| atlas | MITRE ATLAS | mapping, structure | artificial-intelligence 数组(划分特征待核) |
| nist-ai-rmf | NIST AI RMF 1.0 | mapping | 映射 |
| anthropic-docs | Anthropic 文档 | mapping | 映射 |
| rfc-1122 | RFC 1122 | mapping, structure | networking-and-communication 下的数组 |
| rfc-http | RFC 9110–9114 | mapping | 映射 |
| osi | ISO/IEC 7498-1 OSI 参考模型 | mapping | 映射 |
| mdn | MDN 技术参考 | mapping | 映射;Web Platforms 为第 3 层,其下不借入 |
| mdn-curriculum | MDN Curriculum | candidate | 候选词来源 |
| iso-25964 | ISO 25964-1/-2 | mapping | 映射 |
| z39-19 | ANSI/NISO Z39.19 | mapping | 映射 |
| skos | W3C SKOS | mapping | 映射 |
| roadmap-sh | roadmap.sh | candidate | 候选词来源 |
| teachyourselfcs | teachyourselfcs.com | candidate | 候选词来源 |
| cmu-15-445 | CMU 15-445 | candidate | 候选词来源 |
| db-engines | DB-Engines 排名 | candidate | 候选词来源 |

## 待定事项

- 借入来源的分级与版本要求,留待治理方案
- MDN 技术参考没有版本号,`version` 怎么记(抓取日期?);Web 内容是否需要破例借入它
- `mdn-curriculum` 标为 candidate,但它有稳定模块名,是否也给 `group`
