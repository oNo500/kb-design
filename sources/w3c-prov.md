# W3C PROV

## 材料身份

本笔记记录 [PROV-DM: The PROV Data Model](https://www.w3.org/TR/prov-dm/) 与 [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/) 中 Entity、Activity、Usage、Generation 和 Derivation 的关系边界，核对日期为 2026-09-01。PROV 用来表达 provenance 关系，不自动认证关系记录或关系中的对象。

## 阅读范围

| 材料 | 实际读到的位置 |
|---|---|
| PROV-DM | 第 2.1 节 `PROV Core Structures`、第 2.1.1 节 `Entity and Activity`、第 2.1.2 节 `Derivation`、第 5.1.1 节 `Entity`、第 5.1.2 节 `Activity`、第 5.1.3 节 `Generation`、第 5.1.4 节 `Usage` |
| PROV-O | starting-point classes 与 properties 中的 `prov:Entity`、`prov:Activity`、`prov:used`、`prov:wasGeneratedBy`、`prov:wasDerivedFrom`，以及对应 qualified relations 的说明 |

## 核心对象

| PROV 对象 | 规范边界 |
|---|---|
| Entity | 具有某些固定方面的物理、数字、概念或其他对象，可以是真实或想象对象 |
| Activity | 在一段时间内发生并作用于或伴随 Entity 的活动，可以消费、处理、转换、修改、移动、使用或生成 Entity |
| Usage | Activity 开始利用某个 Entity 的时点；在该 Usage 之前，该 Activity 尚未开始利用该 Entity，也不可能已受其影响 |
| Generation | Activity 完成产生新 Entity 的时点；该 Entity 此前不存在，并在 Generation 后可被使用 |
| Derivation | 一个 Entity 转换成另一个 Entity、更新后产生新 Entity，或基于既有 Entity 构造新 Entity；它要求生成对象受到所用对象的某种影响 |

## 关系边界

输入被 Activity 使用，应表达为 Usage；输出由 Activity 生成，应表达为 Generation。某个 Activity 同时使用一个输入并生成一个输出，只能建立相应 Usage 和 Generation，不能证明该输入实际影响该输出，也不自动建立 Derivation。[PROV-DM 第 2.1.2 节](https://www.w3.org/TR/prov-dm/#term-Derivation) 明确说明，usage 与 generation 的链是 Derivation 的必要条件，但并不充分；还需要某种 influence。

PROV-O 用 `prov:used`、`prov:wasGeneratedBy` 和 `prov:wasDerivedFrom` 表达相应二元关系，并可用 qualified relations 补充关系细节。二元关系或 qualified relation 的存在只表达记录中的 provenance 关系，不能证明记录本身真实。

## 证明边界

W3C PROV 能表达 Entity、Activity 及其 Usage、Generation 和 Derivation，不能证明记录真实性、数字签名、输出的字节确定性或任何一方可重建输出。provenance 关系不等于 checksum 校验、JCS serialization、deterministic behavior 或 reproducible build。

## 项目边界

项目文件中出现输入路径、输出路径、hash 或生成时间，不自动构成符合 W3C PROV 的记录；即使另行记录 Usage 和 Generation，也不能据此断言输入影响输出。只有项目明确表达并满足相应关系时，才能使用对应 PROV 关系描述。

## 未读范围

- 未通读 PROV-DM 与 PROV-O 的其余组件、约束、示例、附录和勘误记录。
- 未读取 PROV-N、PROV-XML、PROV-JSON、PROV-CONSTRAINTS 等其他 PROV 文档，也未建立本项目的 PROV serialization 或 validation。
