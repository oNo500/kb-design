# 分面字段草案

状态:草案,未生效。`topics.yaml` 目前不设 `kind` 字段。

## 要解决的问题

主题词表的树按学科分,一个概念在树里的位置回答「它属于哪个领域」,不回答「它是什么类的东西」。以下查询需要后者:

- 某个知识单元下所有的**实践**(而不是技术制品)
- 全库所有的**标准和规范**
- 全库所有的**缺陷和攻击**

这是分面分析的典型场景:按内在类别横切学科树。

## 标准给了什么

ISO 25964-1 §2.20 定义分面为「同一内在类别的概念分组」,注里给的高层类别**示例**:objects(对象)、materials(材料)、agents(施动者)、actions(动作)、places(地点)、times(时间)。措辞是 examples,不是封闭集合。来源是 Ranganathan 的 PMEST 经分类研究小组扩展。

套到本库的领域:

| ISO 示例 | 本库对应 | 贴合 |
|---|---|---|
| objects | PostgreSQL、HTTP/2、React 等技术制品 | 是 |
| actions | 部署、调优、威胁建模、code review | 是 |
| agents | 人、组织、团队 | 是,量少 |
| materials | 数据、代码 | 勉强 |
| places | 运行环境 | 勉强 |
| times | 版本、时期 | 通常降为元数据字段 |

ISO 示例覆盖不到的:理论与原理(CAP 定理、OSI 模型)、缺陷与攻击(SQL 注入)、标准与规范(ASVS、RFC 9110)。而这三类恰恰是最需要横切查询的。

## 曾经的自定方案

第一版设计里设过六个值:technology、practice、theory、weakness、standard、category。其中 technology ≈ objects、practice ≈ actions 有 ISO 对应;theory、weakness、standard 无;category 用于骨架节点,已由 Z39.19 的「未标引」状态替代。按「当前阶段零自定」的决定撤回。

## 生效前需要

1. 自定分面的治理方案:谁能加值、定义写在哪、怎么废弃
2. 决定扩展方式:在 ISO 示例上加 theory / weakness / standard 并注明自定,还是找到已有这三类的外部分面体系(候选:CWE 本身是 weakness 的分类;ACM CCS 有 "General and reference → Document types" 之类的横切类目,待核)
3. 用现有约 90 个概念试标一遍,看分布是否均匀、是否有概念无法归类

## 相关

- [分面](../../concepts/facet.md)
- [主题词表设计](../topics.md)
