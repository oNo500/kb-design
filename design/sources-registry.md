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
2. 凡 `role` 含 `structure` 的来源,起步就在对应概念下借入一个数组,借到第 3 层,全部未标引——这是[层级结构](hierarchy.md)规则 9。同一划分特征只取一个来源
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

## 待登记的来源

按[层级结构](hierarchy.md)的数组表和映射来源,首批需要登记的:CS2023、SWEBOK v4、ACM CCS、GB/T 13745、ASVS、CWE、ATT&CK、OWASP Top 10、OWASP GenAI、ATLAS、NIST AI RMF、Anthropic 文档、RFC 1122、RFC 9110–9114、OSI、MDN 技术参考、MDN Curriculum、ISO 25964、Z39.19、SKOS、roadmap.sh、teachyourselfcs、CMU 15-445、DB-Engines。每条要核对当前版本。
