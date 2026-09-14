# ERIC 收录范围

## 采用范围

用户决定仅将以下 15 个 ERIC 概念及其全部下位概念纳入自有词表。范围由 ERIC 原始上下位关系确定，不沿相关关系扩展，不自动补入上位概念。

| 根概念 | 包含自身的分支概念数 |
|---|---:|
| Writing Processes | 4 |
| Writing (Composition) | 18 |
| Rhetoric | 3 |
| Technical Writing | 1 |
| Notetaking | 1 |
| Reading Comprehension | 1 |
| Critical Reading | 1 |
| Reading Strategies | 1 |
| Learning Strategies | 2 |
| Study Skills | 2 |
| Learning Processes | 9 |
| Metacognition | 1 |
| Information Seeking | 2 |
| Search Strategies | 1 |
| Information Literacy | 1 |

按当前 ERIC 2025 来源快照展开，分支重叠去重后共 44 个概念，其他 4,534 个 ERIC 概念不进入自有主词表。范围不代表阅读、写作和学习知识已完整覆盖。

## 数据边界

ERIC 原件和完整解析结果仍保留 4,578 个概念，不修改源文件。其他四份来源的概念收录范围不变。与被排除节点相连的关系不进入主图；两端都保留的既有关系继续保留。

领域分组按原有规则在完整来源结构中确定，再与选定概念取交集。因此，保留概念不会仅因其上位节点被过滤而丢失既有分组。本决定不额外调整领域归属。

## 执行依据

唯一当前规则位于[来源清单](../../../data/inputs/vocabulary/sources.json)中 ERIC 的 `selection`：固定根概念 URI，`descendants: true`。每次 `kb-vocab sync` 和归档重放均执行该规则，不手工修改生成的 Turtle。

`source-selection.json` 保存规则、每个分支的数量、排除的概念及三元组去向；来源副本仍按原字节保存。规则中的根概念消失时停止构建，不自动按相似名称重新对应。当前结果见[构建报告](../../../output/vocabulary/current/report.json)。
