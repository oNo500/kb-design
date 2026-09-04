# 来源角色库存

## 范围

本库存以 [来源登记](../../../vocab/sources.yaml) 的 31 个来源记录为身份集，逐项读取当前 `role`、来源实体、`source`、`match`、数组结构、生成输入和校验脚本。逐行结果见 [source-roles.tsv](source-roles.tsv)。

库存只处理来源用途和角色。`basis` 逐值依据、来源实体状态、版本与地址分别由其他库存负责。本库存没有联网补充外部事实，也没有根据字符串、目录或出现次数推定语义。

## 口径

当前角色按 [现行来源设计](../../../design/sources-registry.md) 记录；草案分类只使用 [来源治理草案](../../../design/drafts/source-governance.md) 已列出的 `mapping`、`structure`、`group` 和 `discovery`。当前 `candidate` 只列为 `candidate` 向 `discovery` 的迁移候选，不将任何发现结果当成形式依据、概念身份、候选记录或项目准入。

TSV 中每个“来源 ID × 当前用途”只出现一次。“当前材料”记录现行设计或正式数据中可定位的用途声明；“消费者”记录实际数据、生成输入或校验器。当前只有角色声明而没有实际消费者时，明确记为未发现，不倒推用途已发生。

## 计数

| 项目 | 数量 |
|---|---:|
| 来源记录 | 31 |
| 来源用途行 | 47 |
| 当前 `mapping` | 26 |
| 当前 `structure` | 13 |
| 当前 `group` | 3 |
| 当前 `candidate` | 5 |
| 草案 `discovery` 候选 | 5 |
| 实际 `match` | 756 |
| 主题记录的外部 `source` | 692 |
| 来源数组 | 26 |

756 条 `match` 分布于 15 个来源；另有 11 个 `mapping` 角色尚无实际 `match`。692 条主题外部 `source` 分布于 9 个来源。26 个来源数组包括主题词表的 24 个数组和载体词表的 2 个 LOM 数组。

## 消费者

`mapping` 的实际消费者是 `vocab/topics.yaml`、`vocab/entities.yaml`、`vocab/types.yaml`、`vocab/genres.yaml` 和 `vocab/forms.yaml` 中的 `match`。`structure` 的实际消费者是主题或载体数组、主题记录的外部 `source`、`vocab/build/` 的生成输入以及 `scripts/build-topics.py`。`scripts/check-topics.py` 校验来源身份、结构角色必须同时有映射角色、`source` 和 `match.source` 的引用完整性，但它不校验实际消费者是否符合该角色的语义。

`group` 的现行规则是从已有映射确定性计算，不持久化。CWE 和 OWASP LLM Top 10 分别有 10 个可计算成员，OWASP Top 10 当前为 0 个成员；未发现派生组生成脚本或持久化数据。

5 个旧 `candidate` 来源都没有发现正式概念、`match`、外部 `source` 或结构消费者。它们只能进入 `discovery` 迁移候选，且迁移不能顺带授予其他角色。

## 迁移边界

当前 `mapping`、`structure` 和 `group` 的名称可以直接对应草案角色，旧 `candidate` 只对应 `discovery`。这种名称对应不等于可以填写草案的角色状态和决定引用。

来源治理草案规定 `approved` 和 `retired` 角色必须引用项目决定。本次在 `design/decisions/`、现行来源设计和数据中没有找到能为 47 个角色逐项提供稳定引用的独立决定记录。因此，TSV 只记录现行材料和草案分类；不把任何一行预填为 `approved`，不发明决定 ID，也不改变任何来源的 `tier`。

## 疑虑

- `diataxis`、`dita` 和 `iptc-genre` 现在都有 `structure` 角色，且现行内容模型确实声明相应记录集取自这些来源；但它们没有数组或记录级 `source`，与现行设计将 `structure` 限为“可复制为数组”的写法不完全对应。是否保留为草案中的“记录实际派生”用途，待人逐项决定。
- `swebok` 数组有 18 个成员，但 `software-design` 和 `software-construction` 因与 CS2023 记录合并而保留 `source: cs2023`；`asvs` 数组的 `cryptography` 也保留 `source: cs2023`。它们有相应数组成员身份和外部 `match`，但当前单值 `source` 无法完整表达多来源实际派生。
- `rfc-9110` 的正式数据 ID 与现行来源设计表中的旧合集名 `rfc-http` 不同；`iso-25964-1` 和 `iso-25964-2` 也在正式数据中分开，而设计表合写为 `iso-25964`。本库存保留正式数据身份，不猜测设计表的身份去向。
- 11 个 `mapping` 角色没有实际 `match`；`owasp-top10` 因而也只有空的派生组视图。角色是保留未用资格、改为 `proposed` 还是不迁移，草案和现行数据都不能代替人的逐项决定。
- `vocab/sources.yaml` 的版本注记仍写“27 个来源”，实际有 31 条。这是另一库存的版本与身份问题，本任务没有修改正式数据。

## 校验

库存验证项包括：TSV 恰有九列；47 个对象身份唯一；所有单元格非空；草案分类只取 `mapping`、`structure`、`group`、`discovery`；状态只取“需要复核”和“待人决定”；当前来源身份与 31 个来源记录逐项对账；受 Git 跟踪文件差异为 0。
