# 词表副本对照 (CCS 2012)

官网 XML 是较精简的分类树导出；第三方副本提供较多检索用名称和附加信息。它们不是同一份文件的等价副本，不能直接相互覆盖。

## 对照范围

- 官网：已保存的原始 XML，以及保留其完整路径标识的转换副本。
- CRAN：逐项提取全部编号、首选名称、上位和下位关系。
- VocabularyServer：取得全部 2,299 个首选名称和常规字母、数字、点号索引中的 6,814 条别名；首选名称全集与 CRAN 一致。
- VocabularyServer 的全部层级边、相关关系和说明尚未逐项导出；对应统计来自其说明页，不能据计数一致推断所有关系相同。

## 内容统计

| 内容 | 官网文件 | 第三方副本 |
|---|---:|---|
| 顶层入口 | 13 | 14 |
| 分类记录 | 2,113 个完整路径节点 | 2,299 个分类编号及首选名称 |
| 对照用编号 | 路径末段共有 1,928 种 | CRAN 共有 2,299 种 |
| 别名 | 0 | VocabularyServer 索引中取得 6,814 条 |
| 相关关系 | 0 | VocabularyServer 公开统计 192 |
| 范围说明 | 0 | VocabularyServer 公开统计 41 |

官网节点按完整路径区分；将末段编号作为对照键，只服务于本次比较，不用于合并节点或决定概念身份。不能直接用 2,299 减去 2,113 得出语义缺失数量。

## 编号与层级

- 官网与 CRAN 共有 1,907 个编号。
- 在共有编号范围内，两边的直接上下位关系一致，没有发现不同的边。
- 共有编号中有一处首选文字差异：`10011068` 在官网是 `Software as a service orchestration system`，CRAN 与 VocabularyServer 为末尾带 s 的 `systems`。
- CRAN 多出的 392 个编号全部位于 `Proper nouns: People, technologies and companies` 分支。不能据此把这些实体都当作计算机学科分类。
- 官网有 21 个 CRAN 没有的编号，见下表。编号差异不直接证明主题含义新增；例如副本已有另一个编号的 `Simulated annealing`。

| 官网独有编号 | 官网首选名称 |
|---|---|
| `10011782` | Automatic programming |
| `10011784` | Search-based software engineering |
| `10011795` | Random search heuristics |
| `10011796` | Theory of randomized search heuristics |
| `10011797` | Optimization with randomized search heuristics |
| `10011798` | Simulated annealing |
| `10011799` | Evolutionary algorithms |
| `10011800` | Tabu search |
| `10011801` | Randomized local search |
| `10011803` | Bio-inspired optimization |
| `10011804` | Non-parametric optimization |
| `10011807` | Artificial immune systems |
| `10011809` | Bio-inspired approaches |
| `10011810` | Artificial life |
| `10011811` | Evolvable hardware |
| `10011812` | Genetic algorithms |
| `10011813` | Genetic programming |
| `10011814` | Evolutionary robotics |
| `10011815` | Generative and developmental approaches |
| `10011817` | Multi-criterion optimization and decision-making |
| `10011818` | Developmental representations |

## 接口差异

VocabularyServer 的常规索引取得 6,814 条别名，与其公开统计吻合；但单条 `fetchAlt` 接口还返回了索引中未取得的写法，例如 `λ-calculus`。按希腊字母查询的 letter 接口返回 invalid input。接口范围或记录状态需要继续核对，不能把索引计数吻合当作所有可查询写法已完全覆盖。

## 使用判断

- 官网文件可作为当前已固定的分类骨架，但不提供完整的别名、范围说明和相关关系材料。
- 第三方可作为补充材料和浏览参照；其独有分支、旧编号及附加名称应保持来源标记。
- 如需使用第三方别名，应先核对所指分类、名称角色和版本；本次没有补入现有词表，也没有按同名合并。

## 来源与明细

- [ACM 官网原文件](https://dl.acm.org/pb-assets/dl_ccs/acm_ccs2012-1626988337597.xml)
- [CRAN 分类表](https://cran.r-project.org/web/classifications/ACM-2012.html)
- [VocabularyServer 说明页](https://vocabularyserver.com/acm/12/sobre.php)
- [官网与 CRAN 逐项差异](cran-comparison.json)
- [VocabularyServer 名称对照](tematres-comparison.json)
- [首选名称](tematres-terms.json)、[索引别名及所指词条](tematres-aliases.json)
- [请求与摘要记录](comparison-manifest.json)
