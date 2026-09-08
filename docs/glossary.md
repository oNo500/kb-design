# 术语表 (Glossary)
本文件只读。概念、定义和术语形式由 `data/vocab/terms.yaml` 管理；章节编排、说明、关系符号和历史名称展示由 `data/inputs/terminology/glossary-layout.yaml` 管理；模型标签继续由各自现行编辑源（`data/inputs/topics/`、`data/vocab/forms.yaml`）及 `data/inputs/topics/label-adoptions.json` 的既有采纳记录管理。

本页按应用章节编排，并由同一已校验快照确定生成。

快照 SHA-256：`dae25adc8f87e984643dbe70468c744871b09a8d88930925cf1ed3424dd9fe8c`。

## 出处缩写

- ISO｜ISO 25964-1:2011，后接条款号
  - 性质：来源缩写及展开，只作引用说明，不是术语概念。
- ISO-2｜ISO 25964-2:2013，后接条款号
  - 性质：来源缩写及展开，只作引用说明，不是术语概念。
- Z｜ANSI/NISO Z39.19-2005 (R2010)，后接条款号
  - 性质：来源缩写及展开，只作引用说明，不是术语概念。
- SKOS｜W3C SKOS Reference,2009
  - 性质：来源缩写及展开，只作引用说明，不是术语概念。
- KG｜Hogan et al., *Knowledge Graphs*, 2021
  - 性质：来源缩写及展开，只作引用说明，不是术语概念。
- 自定｜本库自定，无外部来源
  - 性质：来源缩写及展开，只作引用说明，不是术语概念。
  - 范围：仅保留原出处缩写的项目用法说明，不自动给任何对象自定资格；3项目定义按精确project basis提案另处理。

## 词表的类型

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| 受控词表 | controlled vocabulary | zh-Hans：预先规定的词、标目（headings）或代码列表，每项表示一个概念。 | — | tc-6908a022-5a5a-43e0-b895-4414bba97169 |
| 列表 | list | zh-Hans：有限的一组词，按字母或其他明显逻辑排列，无关系 | en：pick list | tc-94e9bdfe-cefd-445c-9a12-f276bfe75e63 |
| 同义词环 | synonym ring | zh-Hans：一组检索时视为等价的词；只用于检索，不用于标引 | — | tc-c5f2ed53-7f7e-40a1-8c89-a07dac98107b |
| 分类法 | taxonomy | zh-Hans：全部由首选词构成、以层级或多层级连接的受控词表 | — | tc-c6190e59-1353-4f22-8a93-b3077b486884 |
| 分类表 | classification scheme | zh-Hans：按分类排列的概念及先组组合的表。 | — | tc-4f002e0f-1fe2-41e5-a15c-3cdb436b1763 |
| 叙词表 | thesaurus | zh-Hans：按已知顺序排列、用标准化关系指示符清楚显示词间关系的受控词表 | — | tc-5c7a2951-c99c-4597-baa5-c6eb7fd7c5e4 |
| 本体 | ontology | zh-Hans：对概念化的明确规范，包括用于描述领域的类、属性和关系及其含义与约束。 | — | tc-9d793546-528c-4b51-8a37-801df07342f3 |
| 知识图谱 | knowledge graph | zh-Hans：用于积累和传达现实世界知识的图数据；节点表示实体，边表示实体间关系，数据图可采用有向边标记图、属性图等模型。 | — | tc-c7d6f1d5-2139-4d42-857d-7c16fa507b31 |

**受控词表**（`tc-6908a022-5a5a-43e0-b895-4414bba97169`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.12；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

预先规定的词、标目（headings）或代码列表，每项表示一个概念。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.12；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 受控词表（`tm-e92e1633-a6e8-4eaa-91cd-fc1abd2d7cd3`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：受控词表是信息组织领域对预定且受管理的词汇列表的通行表达；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- controlled vocabulary（`tm-67cf1d57-71a5-4e5a-8294-ca5d0a931222`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.12；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**列表**（`tc-94e9bdfe-cefd-445c-9a12-f276bfe75e63`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.1；印刷 p.17 · 核对日期 2026-09-06

**定义**

**简体中文定义**

有限的一组词，按字母或其他明显逻辑排列，无关系

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.1；印刷 p.17 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 列表（`tm-74a9e0b7-478f-48e1-9b61-00ca7b63bd12`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：列表是有限术语按明确顺序排列这一既有概念的行业表达；避免把glossary或code list的专门名称作为无条件同义词；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- list（`tm-18e3b5c1-b6c5-4ddd-9b60-64435812ef57`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.1；印刷 p.17 · 核对日期 2026-09-06
- pick list（`tm-42bb0163-eaa8-4a85-9cbe-f4968c0dcd2d`；admittedTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.1；印刷 p.17 · 核对日期 2026-09-06

**历史形式**

无。

**同义词环**（`tc-c5f2ed53-7f7e-40a1-8c89-a07dac98107b`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.2；PDF page index 28-29 · 核对日期 2026-09-06

**定义**

**简体中文定义**

一组检索时视为等价的词；只用于检索，不用于标引

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.2；PDF page index 28-29 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 同义词环（`tm-fc11144d-35cd-472b-a85d-23bc72f9e6c2`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：同义词环指检索时视为等价的一组词，名称突出检索扩展而非标引选词；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- synonym ring（`tm-28740536-c0a9-499e-b167-e47449e37cff`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.2；PDF page index 28-29 · 核对日期 2026-09-06

**历史形式**

无。

**分类法**（`tc-c6190e59-1353-4f22-8a93-b3077b486884`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.3；PDF page index 29 · 核对日期 2026-09-06

**定义**

**简体中文定义**

全部由首选词构成、以层级或多层级连接的受控词表

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.3；PDF page index 29 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 分类法（`tm-fc044200-56a9-4783-b4df-a6c1fc3f51e4`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：分类法是知识组织中 taxonomy 的既有行业译名；此处限于首选词的层级受控词表；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- taxonomy（`tm-3fbb53ad-04df-4f9d-b94f-58cecc7d80b8`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.3；PDF page index 29 · 核对日期 2026-09-06

**历史形式**

无。

**分类表**（`tc-4f002e0f-1fe2-41e5-a15c-3cdb436b1763`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.6，免费样章印刷p.2 · 核对日期 2026-09-06

**定义**

**简体中文定义**

按分类排列的概念及先组组合的表。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.6，免费样章印刷p.2 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 分类表（`tm-4011c8e8-cd44-497e-85f0-1667007d53c7`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：分类表指按分类组织的概念表，不替换成taxonomy或一般分类操作。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- classification scheme（`tm-29e4f758-6d4f-4411-b474-e1f08b3213ae`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.6，免费样章印刷p.2 · 核对日期 2026-09-06

**历史形式**

无。

**叙词表**（`tc-5c7a2951-c99c-4597-baa5-c6eb7fd7c5e4`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.4；PDF page index 29 · 核对日期 2026-09-06

**定义**

**简体中文定义**

按已知顺序排列、用标准化关系指示符清楚显示词间关系的受控词表

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.4；PDF page index 29 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 叙词表（`tm-8b27bf95-89c5-4e8b-a033-e0defb04a51c`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：叙词表是信息检索领域对具有规范关系的受控词表的传统名称；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- thesaurus（`tm-baf0b11a-4d8a-415b-83d9-0f6d64662d6a`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.4；PDF page index 29 · 核对日期 2026-09-06

**历史形式**

无。

**本体**（`tc-9d793546-528c-4b51-8a37-801df07342f3`）


**概念依据**

- [Ontology · 2008](https://tomgruber.org/writing/definition-of-ontology/) · L14-L24；英文形式 ontology；作者定义为 explicit specification of a conceptualization；代表原语包括 classes、attributes、relationships 及其约束（L15-L16） · 核对日期 2026-09-06

**定义**

**简体中文定义**

对概念化的明确规范，包括用于描述领域的类、属性和关系及其含义与约束。

依据：
- [Ontology · 2008](https://tomgruber.org/writing/definition-of-ontology/) · L14-L24；英文形式 ontology；作者定义为 explicit specification of a conceptualization；代表原语包括 classes、attributes、relationships 及其约束（L15-L16） · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 本体（`tm-f1d2d279-3d8f-4f39-b490-8f0c211d15b9`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：本体是知识表示领域 ontology 的通行译名，限于概念化规范；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- ontology（`tm-3f32ff2e-2739-4982-9971-ff06c324a402`；preferredTerm-admn-sts）
  - 依据：[Ontology · 2008](https://tomgruber.org/writing/definition-of-ontology/) · L14-L24；英文形式 ontology；作者定义为 explicit specification of a conceptualization；代表原语包括 classes、attributes、relationships 及其约束（L15-L16） · 核对日期 2026-09-06

**历史形式**

无。

**知识图谱**（`tc-c7d6f1d5-2139-4d42-857d-7c16fa507b31`）


**概念依据**

- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · P1 L68-L89；P6 L277-L328；P1 L71-L83 直接支持现实世界知识、实体节点、实体间关系、图数据模型及可用本体/规则表达量化知识 · 核对日期 2026-09-06

**定义**

**简体中文定义**

用于积累和传达现实世界知识的图数据；节点表示实体，边表示实体间关系，数据图可采用有向边标记图、属性图等模型。

依据：
- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · P1 L68-L89；P6 L277-L328；P1 L71-L83 直接支持现实世界知识、实体节点、实体间关系、图数据模型及可用本体/规则表达量化知识 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 知识图谱（`tm-60f284eb-71a8-490b-be2a-b6fabcb92d8b`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：知识图谱表述以图积累和传达知识的数据组织；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- knowledge graph（`tm-2d4a0c3e-052f-4110-b3c6-9f08982cbb34`；preferredTerm-admn-sts）
  - 依据：[Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · P1 L68-L89；P6 L277-L328；P1 L71-L83 直接支持现实世界知识、实体节点、实体间关系、图数据模型及可用本体/规则表达量化知识 · 核对日期 2026-09-06

**历史形式**

无。

## 基本单位

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| 概念 | concept | zh-Hans：思维单元；独立于表达它的词而存在。 | — | tc-c960c1a6-3e65-4075-801a-876b1d3b2f57 |
| 词 | term | zh-Hans：表示一个概念的一个或多个词。 | — | tc-84906e82-1b72-4118-951c-33416d9d9bf7 |
| 首选词 | preferred term | zh-Hans：标引时用来表示概念的词。 | zh-Hans：叙词；en：descriptor | tc-c1473abd-3fc6-4570-bf19-cbb27b944fc2 |
| 非首选词 | non-preferred term | zh-Hans：不分配给文档、但作为叙词表或索引入口的词。 | zh-Hans：非叙词 | tc-75fa8baa-d6ec-400e-b90f-5039371a2d57 |
| 入口词 | entry term | zh-Hans：不直接用于元数据、而引导用户找到另一可用词的受控词表术语；在叙词表中通常称非首选词。 | en：lead-in term | tc-c5ee911a-276c-4bc1-81e7-f651972b0830 |
| 隐藏标签 | hidden label | zh-Hans：可供基于文本的检索使用，但不供用户直接显示的标签。 | — | tc-57a8d816-05c4-4aa9-b3da-277b5d23cc4e |
| 标识符 | identifier | zh-Hans：在确定的语境或资源内，为唯一识别概念、词或其他实体而使用的一组符号。 | — | tc-dc59744d-a530-44b7-9de8-77e2766710e7 |
| 限定词 | qualifier | zh-Hans：加在词后区分同形异义的定义性词，如 `Apple (company)` | — | tc-26a41c49-f435-4527-b419-de688657db90 |
| 同形异义词 | homograph | zh-Hans：写法相同而意义不同的词。 | — | tc-d58d9afb-92ca-46c1-b928-e6ea6c2a11a6 |
| 准同义词 | quasi-synonym | zh-Hans：通常意义不同，但在特定受控词表中可作为同一概念标签的词。 | — | tc-adbb6019-db11-4d1e-a9b2-4e7a8fedd0a5 |
| 复合词 | compound term | zh-Hans：可按形态拆成独立成分的术语；可以由一个词或多个词组成。 | — | tc-a977c939-c9fe-477b-a154-a0ccd97aa3d6 |
| 复合概念 | complex concept | zh-Hans：可由两个或更多较简单概念组合表示的概念。 | — | tc-b0214996-65e1-4d37-a055-b7356a776ac0 |
| 领域 | domain | zh-Hans：专门知识的范围。 | — | tc-6a20995f-a6b2-492a-88e9-a554c8364fe2 |
| 元数据 | metadata | zh-Hans：识别文档属性，通常支持定位、发现、记录、评价或选择的数据。 | — | tc-a8e5c450-33ff-42e5-a352-1bbb21fcd0b5 |
| 内容对象 | content object | zh-Hans：可被组织或分类以供检索的项目，包括文档、图像、人、组织和实物；本条限于 NISO 内容对象语境。 | — | tc-7f29a362-cc5b-481a-87df-67ff11c9c068 |

**概念**（`tc-c960c1a6-3e65-4075-801a-876b1d3b2f57`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.11；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

思维单元；独立于表达它的词而存在。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.11；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 概念（`tm-1c54182a-deb7-427a-8426-68bd35811502`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：概念对应思维单元而非字符串，是术语学与知识组织的基本表达；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- concept（`tm-0cad325d-695d-4f83-a05a-9ba8cb422e8a`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.11；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**词**（`tc-84906e82-1b72-4118-951c-33416d9d9bf7`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1 Glossary，term · 核对日期 2026-09-06

**定义**

**简体中文定义**

表示一个概念的一个或多个词。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1 Glossary，term · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 词（`tm-868a4b9a-45b4-4d9f-b359-8de7a44f060f`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：NISO已核term意义与原概念一致；英文名称保留，中文词在本条也包含多词表达，不冒称ISO§2.61已读。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- term（`tm-6d783441-c3df-409b-8202-742ff6b3bfa4`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1 Glossary，term · 核对日期 2026-09-06

**历史形式**

无。

**首选词**（`tc-c1473abd-3fc6-4570-bf19-cbb27b944fc2`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.45；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

标引时用来表示概念的词。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.45；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 首选词（`tm-d7a0c93f-489a-4385-93ce-a934df56a82f`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：首选词突出标引时优先采用的名称；旧并列叙词暂不凭逗号加入同义形式；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values
- 叙词（`tm-b662786b-e53c-4ed0-9cc8-35346e4c6e20`；admittedTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：叙词是图书情报与叙词表实践中descriptor的既有中文名称；本条限定标引时代表概念的首选词，不泛指任意词；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- preferred term（`tm-6819b288-3cb6-4479-9516-e2a25acf1618`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.45；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29
- descriptor（`tm-b13a05dd-249c-4d95-b82d-d575249ffd1f`；admittedTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.45 preferred term / descriptor；免费样章印刷p.9，本次直接重读 · 核对日期 2026-09-06

**历史形式**

无。

**非首选词**（`tc-75fa8baa-d6ec-400e-b90f-5039371a2d57`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.39；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

不分配给文档、但作为叙词表或索引入口的词。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.39；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 非首选词（`tm-cd530576-f163-4651-b468-3dbf8af5f014`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：非首选词与首选词形成名称使用地位的对照；非叙词保留原登记待独立判断；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values
- 非叙词（`tm-3866b74f-a77b-46e9-95bc-f4b16fefd182`；admittedTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：非叙词对应ISO§2.39同时列出的non-descriptor，在此指不用作直接标引而提供入口的词；与非首选词同范围；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- non-preferred term（`tm-1996dfd0-ddc6-437f-808f-5ad8ff4f2b81`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.39；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**入口词**（`tc-c5ee911a-276c-4bc1-81e7-f651972b0830`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.16，免费样章印刷p.4 · 核对日期 2026-09-06

**定义**

**简体中文定义**

不直接用于元数据、而引导用户找到另一可用词的受控词表术语；在叙词表中通常称非首选词。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.16，免费样章印刷p.4 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 入口词（`tm-c15bae24-b66d-4da9-bb5b-cd84d38fd50c`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：入口词强调通向可用术语的检索入口，不等于所有标引词。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- entry term（`tm-ba65904c-7386-439b-9b62-d2fbb3024a94`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.16，免费样章印刷p.4 · 核对日期 2026-09-06
- lead-in term（`tm-87280583-a819-4fba-a27d-83bfb9035805`；admittedTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.16，免费样章印刷p.4 · 核对日期 2026-09-06

**历史形式**

无。

**隐藏标签**（`tc-57a8d816-05c4-4aa9-b3da-277b5d23cc4e`）


**概念依据**

- [W3C SKOS 参考 / W3C SKOS Simple Knowledge Organization System Reference · 2009-08-18](https://www.w3.org/TR/skos-reference/) · §5 Lexical Labels；skos:hiddenLabel及示例 · 核对日期 2026-09-06

**定义**

**简体中文定义**

可供基于文本的检索使用，但不供用户直接显示的标签。

依据：
- [W3C SKOS 参考 / W3C SKOS Simple Knowledge Organization System Reference · 2009-08-18](https://www.w3.org/TR/skos-reference/) · §5 Lexical Labels；skos:hiddenLabel及示例 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 隐藏标签（`tm-3c495c32-6257-4fc1-8ecf-e60a823d33da`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：隐藏标签对应可检索但不直接显示的词汇标签；ISO hidden布尔输出标志只作模型背景，不声称两个接口完全等价。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- hidden label（`tm-9c6430b5-c331-4cf0-943a-5cae137ca58d`；preferredTerm-admn-sts）
  - 依据：[W3C SKOS 参考 / W3C SKOS Simple Knowledge Organization System Reference · 2009-08-18](https://www.w3.org/TR/skos-reference/) · §5 Lexical Labels；skos:hiddenLabel及示例 · 核对日期 2026-09-06

**历史形式**

无。

**标识符**（`tc-dc59744d-a530-44b7-9de8-77e2766710e7`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.25；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

在确定的语境或资源内，为唯一识别概念、词或其他实体而使用的一组符号。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.25；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 标识符（`tm-a596d0b5-6739-41d4-a914-5171aa299fb5`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：标识符用于识别对象而非描述对象，译名保留识别语义；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- identifier（`tm-de3b29f2-97c9-489a-be7a-0c77c1368e29`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.25；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**限定词**（`tc-26a41c49-f435-4527-b419-de688657db90`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§6.2.1；PDF page index 19；31-32 · 核对日期 2026-09-06

**定义**

**简体中文定义**

加在词后区分同形异义的定义性词，如 `Apple (company)`

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§6.2.1；PDF page index 19；31-32 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 限定词（`tm-d3e0ce32-0761-40d2-b0ca-4bf9dbf7a110`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：限定词用于限制名称解释范围并区分同形异义；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- qualifier（`tm-d9b07ebb-8bba-4a1b-8b14-350fda733371`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§6.2.1；PDF page index 19；31-32 · 核对日期 2026-09-06

**历史形式**

无。

**同形异义词**（`tc-d58d9afb-92ca-46c1-b928-e6ea6c2a11a6`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.24，免费样章印刷p.6 · 核对日期 2026-09-06

**定义**

**简体中文定义**

写法相同而意义不同的词。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.24，免费样章印刷p.6 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 同形异义词（`tm-d4d7539d-7a93-487d-ba5b-d94d3b3fdbf0`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：同形异义词同时保留相同字形与不同意义这两个判据。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- homograph（`tm-c9a7fa2f-a37c-4f88-83bd-aed4e2b88613`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.24，免费样章印刷p.6 · 核对日期 2026-09-06

**历史形式**

无。

**准同义词**（`tc-adbb6019-db11-4d1e-a9b2-4e7a8fedd0a5`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.47，免费样章印刷p.9 · 核对日期 2026-09-06

**定义**

**简体中文定义**

通常意义不同，但在特定受控词表中可作为同一概念标签的词。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.47，免费样章印刷p.9 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 准同义词（`tm-b56a70b0-92c7-460b-a1ca-9d5d5cf27dcb`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：准同义词是特定词表中的约定等价，非日常语言完全同义。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- quasi-synonym（`tm-3cd0a683-a19a-4073-8f06-87e6540ec09c`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.47，免费样章印刷p.9 · 核对日期 2026-09-06

**历史形式**

无。

**复合词**（`tc-a977c939-c9fe-477b-a154-a0ccd97aa3d6`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.9，免费样章印刷p.3 · 核对日期 2026-09-06

**定义**

**简体中文定义**

可按形态拆成独立成分的术语；可以由一个词或多个词组成。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.9，免费样章印刷p.3 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 复合词（`tm-2d65f52c-42b6-464f-9208-f4cb567df8db`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：复合词按形态可拆分确定，不仅是有空格的多词短语。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- compound term（`tm-427e5a68-a3c5-4be6-9337-f84962686067`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.9，免费样章印刷p.3 · 核对日期 2026-09-06

**历史形式**

无。

**复合概念**（`tc-b0214996-65e1-4d37-a055-b7356a776ac0`）


**概念依据**

- [The ISO 25964 data model for the structure of an information retrieval thesaurus · 2012](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413) · Compound Equivalence，L94–101，coal mining同例compound concept与complex concept回指 · 核对日期 2026-09-06

**定义**

**简体中文定义**

可由两个或更多较简单概念组合表示的概念。

依据：
- [The ISO 25964 data model for the structure of an information retrieval thesaurus · 2012](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413) · Compound Equivalence，L94–101，coal mining同例compound concept与complex concept回指 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 复合概念（`tm-f33000a3-3b8c-467d-9731-9a83c28bfe76`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：复合概念的旧英文complex concept在作者同段直接出现，意义与原组合概念一致，不自动新增coal mining等示例概念。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- complex concept（`tm-bb629eab-c872-4e13-a921-7c7577afb769`；preferredTerm-admn-sts）
  - 依据：[The ISO 25964 data model for the structure of an information retrieval thesaurus · 2012](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413) · Compound Equivalence，L94–101，coal mining同例compound concept与complex concept回指 · 核对日期 2026-09-06

**历史形式**

无。

**领域**（`tc-6a20995f-a6b2-492a-88e9-a554c8364fe2`）


**概念依据**

- [Terminology work and terminology science — Vocabulary · 2019](https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf) · §3.1.4，PDFp.7/印刷p.1，注释续p.8 · 核对日期 2026-09-06

**定义**

**简体中文定义**

专门知识的范围。

依据：
- [Terminology work and terminology science — Vocabulary · 2019](https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf) · §3.1.4，PDFp.7/印刷p.1，注释续p.8 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 领域（`tm-8fc9be24-693d-4905-a110-353c793cf283`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：领域是专门知识范围的行业名称；本库用于说明词表覆盖范围，应用用法另说明，不等于网络域。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- domain（`tm-d1b26431-6581-44bf-929d-095b69ca660f`；preferredTerm-admn-sts）
  - 依据：[Terminology work and terminology science — Vocabulary · 2019](https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf) · §3.1.4，PDFp.7/印刷p.1，注释续p.8 · 核对日期 2026-09-06

**历史形式**

无。

**元数据**（`tc-a8e5c450-33ff-42e5-a352-1bbb21fcd0b5`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.33，免费样章印刷p.6 · 核对日期 2026-09-06

**定义**

**简体中文定义**

识别文档属性，通常支持定位、发现、记录、评价或选择的数据。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.33，免费样章印刷p.6 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 元数据（`tm-92599d5f-6dad-4f51-a4b9-379f8e14ac85`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：元数据保留文档属性描述的原语境；首选词可作元数据值是来源补充说明。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- metadata（`tm-067d0bdf-9db2-490f-a6a8-301b3ec0ee1f`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.33，免费样章印刷p.6 · 核对日期 2026-09-06

**历史形式**

无。

**内容对象**（`tc-7f29a362-cc5b-481a-87df-67ff11c9c068`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§5.2.2；PDF page index 15；22-23 · 核对日期 2026-09-06

**定义**

**简体中文定义**

可被组织或分类以供检索的项目，包括文档、图像、人、组织和实物；本条限于 NISO 内容对象语境。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§5.2.2；PDF page index 15；22-23 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 内容对象（`tm-26d027c7-af05-417b-a6b5-6c1523e04613`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：内容对象表明被组织和检索的对象，不自动等同本库内容单元；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- content object（`tm-2b91ad37-5e29-4f00-90f7-6fc791205905`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§5.2.2；PDF page index 15；22-23 · 核对日期 2026-09-06

**历史形式**

无。

## 关系

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| 等价关系 | — | zh-Hans：叙词表中两个词表示同一个概念的关系。 | — | tc-75e8012c-351f-4303-b8c0-523454b9b730 |
| 复合等价 | — | zh-Hans：一个语境中的术语或概念在另一语境中由两个或更多术语或概念表示的关系或映射。 | — | tc-ad90ba40-f5b0-44e7-9f59-fa2783d837b3 |
| 层级关系 | — | zh-Hans：两个概念之间，一个概念的范围完全包含在另一个概念范围内的关系。 | — | tc-278494cf-719c-43f9-b954-2a54c61e5c45 |
| 属种关系 | — | zh-Hans：类与子类之间的层级关系：子类的每个成员均属于上位类，而上位类还包含该子类以外的成员。 | — | tc-54e74c2d-103e-4935-aab7-fb44a129af69 |
| 整部关系 | — | zh-Hans：整体与其组成部分之间的层级关系。 | — | tc-818463b8-0d48-4ddf-98fb-228ef4591308 |
| 实例关系 | — | zh-Hans：一般类或类型与其个别实例之间的层级关系。 | — | tc-9fde9fd8-eb29-4477-acc1-295f9de9adf5 |
| 相关关系 | — | zh-Hans：两个概念没有层级关系，但具有强语义联系的关系。 | — | tc-589f6145-5330-4773-b2dd-27eeeaa6bc84 |
| 自定义关系 | — | zh-Hans：在既有关系类型下，由词表管理者进一步规定的关系类型。 | — | tc-a529619b-cbcb-4545-901d-54f72971e76f |
| 聚合关系 | paradigmatic relationship | zh-Hans：概念自身固有、可独立于特定文档语境在结构化词表中表达的关系。 | — | tc-df2d8160-1717-4372-a38f-db96925ac980 |
| 组合关系 | syntagmatic relationship | zh-Hans：依赖特定表达或文献语境而形成的概念关系。 | — | tc-1b0b91bc-d29e-44d4-854c-cddd05aebc13 |
| 单层级 | monohierarchical structure | zh-Hans：每个概念在直接上一级只能有一个上位概念的层级安排。 | en：monohierarchy | tc-39065fa2-767d-4606-840c-aaffa5182661 |
| 多层级 | polyhierarchical structure | zh-Hans：每个概念可以有多个上位概念的层级安排。 | en：polyhierarchy | tc-025cc053-edb1-4def-a58f-1de00a8424a4 |
| 互反 | reciprocal | zh-Hans：一种关系与其反向关系相互配对，如A以BT指向B时，B以NT反向指向A。 | — | tc-b10cded9-f3ab-4cdd-b218-edb279779c33 |

**等价关系**（`tc-75e8012c-351f-4303-b8c0-523454b9b730`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.18；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

叙词表中两个词表示同一个概念的关系。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.18；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 等价关系（`tm-1192a98f-d6b3-44ee-a68f-d2c60cad8464`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：等价关系在此连接两个表示形式，不混作跨词表映射；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**历史形式**

无。

**复合等价**（`tc-ad90ba40-f5b0-44e7-9f59-fa2783d837b3`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.8，免费样章印刷p.2 · 核对日期 2026-09-06

**定义**

**简体中文定义**

一个语境中的术语或概念在另一语境中由两个或更多术语或概念表示的关系或映射。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.8，免费样章印刷p.2 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 复合等价（`tm-2295a8c2-8677-4bf0-97fc-b962cad6bc4a`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：复合等价指一对多的概念或名称表示；USE+/UF+是符号，不造英文术语。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**历史形式**

无。

**层级关系**（`tc-278494cf-719c-43f9-b954-2a54c61e5c45`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.23；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

两个概念之间，一个概念的范围完全包含在另一个概念范围内的关系。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.23；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 层级关系（`tm-649ce784-1d46-4f8a-8d77-b093d37b085a`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：层级关系表示范围包含，保留与等价和相关关系的区别；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**历史形式**

无。

**属种关系**（`tc-54e74c2d-103e-4935-aab7-fb44a129af69`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §8.3.1与§8.3.2，印刷pp.47–48，PDFindex58–59 · 核对日期 2026-09-06

**定义**

**简体中文定义**

类与子类之间的层级关系：子类的每个成员均属于上位类，而上位类还包含该子类以外的成员。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §8.3.1与§8.3.2，印刷pp.47–48，PDFindex58–59 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 属种关系（`tm-0e54e5ec-61e2-412f-8e2a-1ac13804a53f`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：属种关系是类与子类的全部/部分关系，不把个别实例属于类混入；原BTG/NTG只作关系指示符。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**历史形式**

无。

**整部关系**（`tc-818463b8-0d48-4ddf-98fb-228ef4591308`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §8.3.3 Whole-Part Relationships，印刷p.49 · 核对日期 2026-09-06

**定义**

**简体中文定义**

整体与其组成部分之间的层级关系。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §8.3.3 Whole-Part Relationships，印刷p.49 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 整部关系（`tm-4a9bb6d7-1099-41e8-be65-a9da97d0073a`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：整部关系保留整体/部分机制，不能把任意关联解释为部分；原BTP/NTP为符号。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**历史形式**

无。

**实例关系**（`tc-9fde9fd8-eb29-4477-acc1-295f9de9adf5`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §8.3.2 Instance Relationships，印刷p.48 · 核对日期 2026-09-06

**定义**

**简体中文定义**

一般类或类型与其个别实例之间的层级关系。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §8.3.2 Instance Relationships，印刷p.48 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 实例关系（`tm-64b1efd6-53a5-4b7e-827c-0edfdadd6ba2`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：实例关系的两端是类与个体，不是类与子类；原BTI/NTI为符号。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**历史形式**

无。

**相关关系**（`tc-589f6145-5330-4773-b2dd-27eeeaa6bc84`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.2；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

两个概念没有层级关系，但具有强语义联系的关系。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.2；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 相关关系（`tm-97b3a73e-ff28-43f8-a01a-be24595a7b24`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：相关关系是叙词表中非层级的语义关联；RT 保留为关系符号；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**历史形式**

无。

**自定义关系**（`tc-a529619b-cbcb-4545-901d-54f72971e76f`）


**概念依据**

- [ISO 25964-1 XML Schema · 1.4](https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd) · HierarchicalRelationship/role文档注记；AssociativeRelationship/role · 核对日期 2026-09-06

**定义**

**简体中文定义**

在既有关系类型下，由词表管理者进一步规定的关系类型。

依据：
- [ISO 25964-1 XML Schema · 1.4](https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd) · HierarchicalRelationship/role文档注记；AssociativeRelationship/role · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 自定义关系（`tm-dd400c8e-6f1f-4f2b-a787-1b9290e16e7d`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：自定义关系表达类型细分机制，依据为配套工件而非未读ISO§10.4；不授权本库实际新增任何关系类型。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**历史形式**

无。

**聚合关系**（`tc-df2d8160-1717-4372-a38f-db96925ac980`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.41 paradigmatic relationship / a priori relationship，印刷p.8 · 核对日期 2026-09-06

**定义**

**简体中文定义**

概念自身固有、可独立于特定文档语境在结构化词表中表达的关系。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.41 paradigmatic relationship / a priori relationship，印刷p.8 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 聚合关系（`tm-d5659ae3-56dd-4e82-ac4e-cc45fcce05a5`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：聚合关系保留概念内在语义，区别随文档语境形成的组合关系。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- paradigmatic relationship（`tm-572d4ac7-3aae-4823-83e3-fddeedba662e`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.41 paradigmatic relationship / a priori relationship，印刷p.8 · 核对日期 2026-09-06

**历史形式**

无。

**组合关系**（`tc-1b0b91bc-d29e-44d4-854c-cddd05aebc13`）


**概念依据**

- [Knowledge organization system](https://www.isko.org/cyclo/kos) · §5.1 a priori/a posteriori与paradigmatic/syntagmatic段 · 核对日期 2026-09-06

**定义**

**简体中文定义**

依赖特定表达或文献语境而形成的概念关系。

依据：
- [Knowledge organization system](https://www.isko.org/cyclo/kos) · §5.1 a priori/a posteriori与paradigmatic/syntagmatic段 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 组合关系（`tm-3dc5c513-2684-4789-b88b-2a74897fb869`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：组合关系依语境建立，不等于同篇出现就必有语义关系；不把作者说明写成已读ISO§4.3。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- syntagmatic relationship（`tm-ccdfadf2-0216-4f91-aa21-d7a4d1f5b8bd`；preferredTerm-admn-sts）
  - 依据：[Knowledge organization system](https://www.isko.org/cyclo/kos) · §5.1 a priori/a posteriori与paradigmatic/syntagmatic段 · 核对日期 2026-09-06

**历史形式**

无。

**单层级**（`tc-39065fa2-767d-4606-840c-aaffa5182661`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.34；docs/references/iso-25964.md 已核定义表 · 核对日期 2026-08-29

**定义**

**简体中文定义**

每个概念在直接上一级只能有一个上位概念的层级安排。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.34；docs/references/iso-25964.md 已核定义表 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 单层级（`tm-9ae59983-3054-4e4b-9e59-e400bd6bffdf`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：单层级在词表领域表示每个概念只有一个直接上位概念，而非只有一层深度；仅为既有概念的模型知识译名判断，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- monohierarchical structure（`tm-b3f9d941-2f49-425c-9e98-6b4e61b4444c`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.34；docs/references/iso-25964.md 已核定义表 · 核对日期 2026-08-29
- monohierarchy（`tm-7b60cc0e-5b50-4047-b76b-91ff8a4cbdac`；admittedTerm-admn-sts）
  - 依据：[Nomenclature for Museum Cataloging](https://www.isko.org/cyclo/nomenclature.htm) · §6 Limitations：monohierarchical classification system每词只有一个直接broader，随后monohierarchy回指 · 核对日期 2026-09-06

**历史形式**

无。

**多层级**（`tc-025cc053-edb1-4def-a58f-1de00a8424a4`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.42；docs/references/iso-25964.md 已核定义表 · 核对日期 2026-08-29

**定义**

**简体中文定义**

每个概念可以有多个上位概念的层级安排。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.42；docs/references/iso-25964.md 已核定义表 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 多层级（`tm-e4c630f1-5986-4325-93a0-bc9710a3bab1`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：多层级在此表示概念允许多个上位概念，而非树的深度较大；仅为既有概念的模型知识译名判断，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- polyhierarchical structure（`tm-57b80a57-9a91-4320-854d-e326cb9d52fa`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.42；docs/references/iso-25964.md 已核定义表 · 核对日期 2026-08-29
- polyhierarchy（`tm-e2104559-047a-41be-84e5-dbe80f7d052f`；admittedTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.4.3 taxonomy；§8.3.4 Polyhierarchical Relationships及Examples109–111 · 核对日期 2026-09-06

**历史形式**

无。

**互反**（`tc-b10cded9-f3ab-4cdd-b218-edb279779c33`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1 reciprocal；§5.4.4 relationship indicators reciprocally；§8.3 · 核对日期 2026-09-06

**定义**

**简体中文定义**

一种关系与其反向关系相互配对，如A以BT指向B时，B以NT反向指向A。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1 reciprocal；§5.4.4 relationship indicators reciprocally；§8.3 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 互反（`tm-2509c694-0529-422a-8c8c-16b9cc377310`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：互反表示反向关系配对；不把关系概念直接变成本库必须物理双写的实现规则。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- reciprocal（`tm-34ed6873-0990-469c-b505-518e69018077`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1 reciprocal；§5.4.4 relationship indicators reciprocally；§8.3 · 核对日期 2026-09-06

**历史形式**

无。

## 结构

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| 分面 | facet | zh-Hans：属于同一固有类别的概念分组。 | — | tc-1fa87658-bf07-4540-a863-a4e98a2fa888 |
| 分面分析 | facet analysis | zh-Hans：把主题领域分析为概念，按分面分组，并按划分特征细分概念。 | — | tc-99e3245e-2f51-45d0-ba40-800d645f7f1f |
| 划分特征 | characteristic of division | zh-Hans：用来把一个概念细分为一组下位概念的属性；组内各概念具有该属性的不同值。 | — | tc-a5b2fb0f-5cea-4d47-8629-04694918cbf9 |
| 层级 | hierarchy | zh-Hans：按上位与下位关系组织的概念结构，可含单上位或多上位安排。 | — | tc-af0edf3d-0500-4fc7-bad0-39127321295c |
| 树 | tree | zh-Hans：由根节点及其子树递归组成的节点结构。 | — | tc-7d9ce2a6-2d92-49c3-8d22-c771cdaae4c3 |
| 节点 | node | zh-Hans：图或树数据结构中的一个顶点。 | — | tc-2cc8c45b-bf02-4b54-bbfc-86286dbd50d7 |
| 顶层概念 | top concept | zh-Hans：在层级顶端、没有上位概念的概念。 | — | tc-6d0b88b7-c403-48bf-9579-b2d94dbf9502 |
| 节点标签 | node label | zh-Hans：插入层级或分类显示、说明词如何安排的标签；它既不是首选词，也不是非首选词。 | — | tc-6e6f7a15-910d-483e-b06c-3e3938aed39b |
| 数组 | array | zh-Hans：一组兄弟概念。 | — | tc-c09e918a-cc3f-423c-bbca-c40c6766ef28 |
| 概念组 | concept group | zh-Hans：按指定准则选择的一组概念。 | zh-Hans：分组 | tc-6ce2328c-e952-40b8-b7d5-fd8dd958d0b7 |
| 微词表 | microthesaurus | zh-Hans：叙词表中指定的、能够作为完整叙词表运行的子集。 | en：micro-thesaurus | tc-6bd16590-fd5e-4cee-9c8b-881051af3706 |
| 辅助表 | auxiliary table | zh-Hans：分类体系中为可重复适用的特征设置、与主表类号配合使用的表；其适用范围可为通用或限于指定主类。 | zh-Hans：复分表 | tc-81fc1070-a33d-4692-b613-751819cecc3b |
| 组配号 | synthesized notation | zh-Hans：按分类体系规则组合主号、辅助号或多个主号，以表达复合主题的记号。 | — | tc-2f3dc564-3adc-46d7-ba3c-4051eaaa434c |
| 先组 | pre-coordination | zh-Hans：在建表阶段或标引、分类阶段组合受控词表中的概念、类或术语。 | — | tc-a4f76dad-bbea-4cf0-b322-1c689c380d95 |
| 后组 | post-coordination | zh-Hans：在检索时组合受控词表的首选词。 | — | tc-7fd3d9b0-be29-4f3c-a5a6-7817f26d9391 |
| 属性 | attribute | zh-Hans：在元数据检索语境中，用于描述、排序或筛选内容对象的一项特性，通过字段及其值表示。 | zh-Hans：维度；en：dimension | tc-7cee3db8-8807-48b2-9fe8-7f0fe0539272 |

**分面**（`tc-1fa87658-bf07-4540-a863-a4e98a2fa888`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.20；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

属于同一固有类别的概念分组。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.20；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 分面（`tm-7dbccdb3-ab81-4d56-95cc-7b55b1e3d83a`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：分面是分面分类法对共同固有类别分组的传统译名；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- facet（`tm-960f6e22-a8fe-426c-b6ea-7f92f697d188`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.20；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**分面分析**（`tc-99e3245e-2f51-45d0-ba40-800d645f7f1f`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.21；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

把主题领域分析为概念，按分面分组，并按划分特征细分概念。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.21；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 分面分析（`tm-31f1451a-6a7e-4415-b0e4-02c445d722c9`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：分面分析表示上述分析和分组方法，不是给文档加多个字段；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- facet analysis（`tm-b60105ff-8590-4f3e-82dd-41b3e6f9d933`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.21；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**划分特征**（`tc-a5b2fb0f-5cea-4d47-8629-04694918cbf9`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.4；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

用来把一个概念细分为一组下位概念的属性；组内各概念具有该属性的不同值。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.4；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 划分特征（`tm-58a4412c-5306-4b39-99dc-ab139550b589`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：划分特征突出同级细分所依据的属性，避免把属性值本身叫特征；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- characteristic of division（`tm-e992d008-5b21-4068-891d-6a4bbd30561d`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.4；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**层级**（`tc-af0edf3d-0500-4fc7-bad0-39127321295c`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §8.3与§8.3.4，印刷pp.47–50 · 核对日期 2026-09-06

**定义**

**简体中文定义**

按上位与下位关系组织的概念结构，可含单上位或多上位安排。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §8.3与§8.3.4，印刷pp.47–50 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 层级（`tm-a8384214-a207-4a7c-9fd0-4313fdb5b353`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：层级是上下位安排，允许多上位；不能与严格树结构无条件同义。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- hierarchy（`tm-bbbe8ecb-22ce-4f7d-a526-5b051b058056`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §8.3与§8.3.4，印刷pp.47–50 · 核对日期 2026-09-06

**历史形式**

无。

**树**（`tc-7d9ce2a6-2d92-49c3-8d22-c771cdaae4c3`）


**概念依据**

- [Dictionary of Algorithms and Data Structures: tree · 2017-12-15](https://xlinux.nist.gov/dads/HTML/tree.html) · Definition(1)及Formal Definition，2017-12-15 · 核对日期 2026-09-06

**定义**

**简体中文定义**

由根节点及其子树递归组成的节点结构。

依据：
- [Dictionary of Algorithms and Data Structures: tree · 2017-12-15](https://xlinux.nist.gov/dads/HTML/tree.html) · Definition(1)及Formal Definition，2017-12-15 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 树（`tm-083afbe6-20c8-47c6-9d23-a51bdd0c2549`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：树保留原中文独立结构概念，按NIST定义区别于可有多上位的一般层级；英文tree为源有依据的补充形式。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- tree（`tm-3b55a969-53ac-4622-ab97-d7774a558335`；preferredTerm-admn-sts）
  - 依据：[Dictionary of Algorithms and Data Structures: tree · 2017-12-15](https://xlinux.nist.gov/dads/HTML/tree.html) · Definition(1)及Formal Definition，2017-12-15 · 核对日期 2026-09-06

**历史形式**

无。

**节点**（`tc-2cc8c45b-bf02-4b54-bbfc-86286dbd50d7`）


**概念依据**

- [Dictionary of Algorithms and Data Structures: node · 2004-12-17](https://xlinux.nist.gov/dads/HTML/node.html) · Definition(1)，2004-12-17 · 核对日期 2026-09-06

**定义**

**简体中文定义**

图或树数据结构中的一个顶点。

依据：
- [Dictionary of Algorithms and Data Structures: node · 2004-12-17](https://xlinux.nist.gov/dads/HTML/node.html) · Definition(1)，2004-12-17 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 节点（`tm-abffcb75-f9c9-43fa-bf71-798a140d5b48`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：节点在本行限于图/树结构；本库以节点表示概念是应用说明，不进入NIST定义。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- node（`tm-17074702-584d-4331-acfa-2c2e88627670`；preferredTerm-admn-sts）
  - 依据：[Dictionary of Algorithms and Data Structures: node · 2004-12-17](https://xlinux.nist.gov/dads/HTML/node.html) · Definition(1)，2004-12-17 · 核对日期 2026-09-06

**历史形式**

无。

**顶层概念**（`tc-6d0b88b7-c403-48bf-9579-b2d94dbf9502`）


**概念依据**

- [ISO 25964-1 XML Schema · 1.4](https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd) · ThesaurusConceptStruct/topConcept documentation · 核对日期 2026-09-06

**定义**

**简体中文定义**

在层级顶端、没有上位概念的概念。

依据：
- [ISO 25964-1 XML Schema · 1.4](https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd) · ThesaurusConceptStruct/topConcept documentation · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 顶层概念（`tm-30908171-1a13-4cb7-b754-48b0014eea6f`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：顶层概念按没有broader确定，不是显示窗口中暂时最上的节点。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- top concept（`tm-2c29e44a-28e1-430a-bc45-252c6f067a30`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1 XML Schema · 1.4](https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd) · ThesaurusConceptStruct/topConcept documentation · 核对日期 2026-09-06

**历史形式**

无。

**节点标签**（`tc-6e6f7a15-910d-483e-b06c-3e3938aed39b`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.38；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

插入层级或分类显示、说明词如何安排的标签；它既不是首选词，也不是非首选词。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.38；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 节点标签（`tm-3e5b4977-db0a-413a-8556-f8f4b34fd5bc`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：节点标签在词表显示中说明排列，不是普通图节点的名称；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- node label（`tm-cf8405c5-923a-4e3c-9ebc-fd08013905af`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.38；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**数组**（`tc-c09e918a-cc3f-423c-bbca-c40c6766ef28`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.1；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

一组兄弟概念。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.1；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 数组（`tm-70716b70-18a1-43d7-829a-1f174ebfc953`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：数组在此限于叙词表的一组兄弟概念，与程序存储数组同形但不同义；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- array（`tm-d8924442-07c0-4937-b3d3-3b198a24d8aa`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.1；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**概念组**（`tc-6ce2328c-e952-40b8-b7d5-fd8dd958d0b7`）


**概念依据**

- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.18；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

按指定准则选择的一组概念。

依据：
- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.18；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 概念组（`tm-96cb412b-bb9d-4f29-93f4-4e1b9bac16c3`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：概念组直指按准则选出的概念集合；过宽的分组暂保留原登记；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values
- 分组（`tm-5627bc80-145c-48a0-ba62-f54c7ac3b83c`；admittedTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：分组在中文可指动作或结果；本条严格指按准则选定的概念集合，作为概念组的简短称呼，不表示分组操作或任意数据集合；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- concept group（`tm-83940a42-c171-42dd-b8db-84d62d19f2c6`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.18；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**微词表**（`tc-6bd16590-fd5e-4cee-9c8b-881051af3706`）


**概念依据**

- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.46，PDFindex13/印刷p.8 · 核对日期 2026-09-06

**定义**

**简体中文定义**

叙词表中指定的、能够作为完整叙词表运行的子集。

依据：
- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.46，PDFindex13/印刷p.8 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 微词表（`tm-39d989b6-114d-4482-823a-e6d505597c0c`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：微词表强调子集可独立作为完整叙词表运行；是否实际建立子库不由词条采纳决定。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- microthesaurus（`tm-4b576cd0-ac19-4ef6-883b-72e82977549c`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.46，PDFindex13/印刷p.8 · 核对日期 2026-09-06
- micro-thesaurus（`tm-c6e74d84-b72d-47ae-9b25-bc9896c878ca`；admittedTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.46，PDFindex13/印刷p.8 · 核对日期 2026-09-06

**历史形式**

无。

**辅助表**（`tc-81fc1070-a33d-4692-b613-751819cecc3b`）


**概念依据**

- [Universal Decimal Classification](https://www.w3.org/2006/07/SWD/wiki/EucUDC) · L22 special auxiliaries；L56–57 common auxiliaries及tables，L68–80组合案例 · 核对日期 2026-09-06

**定义**

**简体中文定义**

分类体系中为可重复适用的特征设置、与主表类号配合使用的表；其适用范围可为通用或限于指定主类。

依据：
- [Universal Decimal Classification](https://www.w3.org/2006/07/SWD/wiki/EucUDC) · L22 special auxiliaries；L56–57 common auxiliaries及tables，L68–80组合案例 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 辅助表（`tm-1db6403d-e157-42c0-9d03-d9c6bafaef9e`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：辅助表说明复用分类特征机制；原只通用维度、只尾部拼接过窄，固定作者案例同时展示专用与通用。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values
- 复分表（`tm-b4a8055d-5598-4ea1-bc76-e35428986632`；admittedTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：复分表是分类实践中以可重复特征进一步细分类号的既有中文称呼；本条与辅助表同限配合主表使用的分类表，不泛指任意再次划分。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- auxiliary table（`tm-3fd9be57-3134-4fdb-83ac-4e4288f39ab5`；preferredTerm-admn-sts）
  - 依据：[Universal Decimal Classification](https://www.w3.org/2006/07/SWD/wiki/EucUDC) · L22 special auxiliaries；L56–57 common auxiliaries及tables，L68–80组合案例 · 核对日期 2026-09-06

**历史形式**

无。

**组配号**（`tc-2f3dc564-3adc-46d7-ba3c-4051eaaa434c`）


**概念依据**

- [Universal Decimal Classification](https://www.w3.org/2006/07/SWD/wiki/EucUDC) · L56–80组合通用辅助号/主号与复合主题；参ISO25964-1§2.22上下文 · 核对日期 2026-09-06

**定义**

**简体中文定义**

按分类体系规则组合主号、辅助号或多个主号，以表达复合主题的记号。

依据：
- [Universal Decimal Classification](https://www.w3.org/2006/07/SWD/wiki/EucUDC) · L56–80组合通用辅助号/主号与复合主题；参ISO25964-1§2.22上下文 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 组配号（`tm-23343b8e-95df-4574-a499-8cdf75d77e8c`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：组配号是组合所得分类记号，区别标示分面开始的facet indicator；原ISO条目错位明确纠正。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- synthesized notation（`tm-c465bee5-b846-4fc6-879b-26642d41fca3`；preferredTerm-admn-sts）
  - 依据：[Universal Decimal Classification](https://www.w3.org/2006/07/SWD/wiki/EucUDC) · L56–80组合通用辅助号/主号与复合主题；参ISO25964-1§2.22上下文 · 核对日期 2026-09-06

**历史形式**

无。

**先组**（`tc-a4f76dad-bbea-4cf0-b322-1c689c380d95`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.44，免费样章印刷p.9 · 核对日期 2026-09-06

**定义**

**简体中文定义**

在建表阶段或标引、分类阶段组合受控词表中的概念、类或术语。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.44，免费样章印刷p.9 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 先组（`tm-72449164-9665-4eed-bd23-9198392d3432`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：先组按组合发生在构建/标引阶段界定，不把多词形式自动等同先组。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- pre-coordination（`tm-3b1cb85c-480e-4e19-a3ef-5b868cd6a3cb`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.44，免费样章印刷p.9 · 核对日期 2026-09-06

**历史形式**

无。

**后组**（`tc-7fd3d9b0-be29-4f3c-a5a6-7817f26d9391`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.43，免费样章印刷p.9 · 核对日期 2026-09-06

**定义**

**简体中文定义**

在检索时组合受控词表的首选词。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.43，免费样章印刷p.9 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 后组（`tm-dd7d2f60-4b07-447c-bc5f-f06d5724fa19`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：后组的区别在检索时组合，与先组作时点对照。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- post-coordination（`tm-3b58953d-02b2-4956-947e-b60779dfca0d`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.43，免费样章印刷p.9 · 核对日期 2026-09-06

**历史形式**

无。

**属性**（`tc-7cee3db8-8807-48b2-9fe8-7f0fe0539272`）


**概念依据**

- [Search User Interfaces · 2009](https://searchuserinterfaces.com/book/sui_ch8_navigation_and_search.html) · §8.3 attribute/dimension同例；§8.6 facet/dimension/feature type · 核对日期 2026-09-06

**定义**

**简体中文定义**

在元数据检索语境中，用于描述、排序或筛选内容对象的一项特性，通过字段及其值表示。

依据：
- [Search User Interfaces · 2009](https://searchuserinterfaces.com/book/sui_ch8_navigation_and_search.html) · §8.3 attribute/dimension同例；§8.6 facet/dimension/feature type · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 属性（`tm-67e8828c-7806-42b2-a9f1-b0053cf14a54`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：属性是内容对象的特性，不是存储字段本身；与知识图谱property另一个概念分开。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values
- 维度（`tm-2c3da61d-f341-4d0d-9614-aefc3c6f7a3f`；admittedTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：维度在本条仅指描述或检索内容对象的特性方面，与attribute同一受限范围；不等同所有数学维度或分面结构。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- attribute（`tm-16a66968-e1b1-4709-9f46-a3dd2964c067`；preferredTerm-admn-sts）
  - 依据：[Search User Interfaces · 2009](https://searchuserinterfaces.com/book/sui_ch8_navigation_and_search.html) · §8.3 attribute/dimension同例；§8.6 facet/dimension/feature type · 核对日期 2026-09-06
- dimension（`tm-a7e2d2bf-bd4f-42c6-a0dd-39cc88a90373`；admittedTerm-admn-sts）
  - 依据：[Search User Interfaces · 2009](https://searchuserinterfaces.com/book/sui_ch8_navigation_and_search.html) · §8.3 attribute/dimension同例；§8.6 facet/dimension/feature type · 核对日期 2026-09-06

**历史形式**

无。

## 注释与生命周期

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| 范围注释 | scope note | zh-Hans：说明词的覆盖范围和用法限制的注释 | — | tc-74b2becc-3bbe-45b5-8d42-bda67dcc17f8 |
| 定义 | definition | zh-Hans：用来描述一个概念并将其与相关概念区别开的表达。 | — | tc-549f2d8d-7ddd-4bd3-b6e1-74e815f9feb2 |
| 历史注释 | history note | zh-Hans：入表日期、变更记录、旧形式及有效期 | — | tc-e7c36840-9dc5-45d1-a371-920c28af2a00 |
| 编辑注释 | editorial note | zh-Hans：供叙词表编辑者在编辑过程中使用的注释。 | — | tc-d6a34d9f-e8f9-4170-9d62-e5b3676e71d9 |
| 候选词 | candidate term | zh-Hans：提出但未走完审批的词 | en：provisional term | tc-155c651f-9cb6-4e89-b394-9b843b268148 |
| 未标引词 | unassigned term | zh-Hans：为补全层级而收、尚未用于标引的词 | — | tc-a17e54a7-07e9-459e-86cc-bd0c12e4d58b |
| 废弃词 | deprecated term | zh-Hans：与首选术语同义，但在可接受性评价中被列为不宜使用的术语。 | — | tc-82db3b46-353e-405f-8a8d-fd6fee70bdb5 |
| 孤儿词 | orphan term | zh-Hans：没有任何层级或相关关系的词 | — | tc-88088c7a-5aaf-458c-a55c-23ff38463ee0 |
| 状态 | status | zh-Hans：表示概念或术语在管理过程中所处阶段的属性。 | — | tc-504af76c-f69e-469e-8e73-239f2fd3da99 |
| 版本历史 | version history | zh-Hans：词表已发布或提供的各个版本的记录，说明版本间的区别以及各版本是否仍为现行。 | — | tc-f4802cd3-fba8-4bb1-89a0-121eebbf1fc6 |

**范围注释**（`tc-74b2becc-3bbe-45b5-8d42-bda67dcc17f8`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§6.2.2；PDF page index 20；33 · 核对日期 2026-09-06

**定义**

**简体中文定义**

说明词的覆盖范围和用法限制的注释

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§6.2.2；PDF page index 20；33 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 范围注释（`tm-a1591f11-abf4-440c-865b-2b448311b1c3`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：范围注释说明名称采用的含义与使用边界；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- scope note（`tm-00cb8d21-abc0-4676-8a07-bafda70bd0cb`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§6.2.2；PDF page index 20；33 · 核对日期 2026-09-06

**历史形式**

无。

**定义**（`tc-549f2d8d-7ddd-4bd3-b6e1-74e815f9feb2`）


**概念依据**

- [Terminology work and terminology science — Vocabulary · 2019](https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf) · §3.3.1，PDFp.12/印刷p.6 · 核对日期 2026-09-06

**定义**

**简体中文定义**

用来描述一个概念并将其与相关概念区别开的表达。

依据：
- [Terminology work and terminology science — Vocabulary · 2019](https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf) · §3.3.1，PDFp.12/印刷p.6 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 定义（`tm-7ecbf405-7181-4a27-ae54-3cc83dafd16e`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：定义的意义由ISO1087支持；ISO25964的Definition类只是存放位置说明，不替代一般概念。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- definition（`tm-4b5fc7e6-51b3-47af-8068-ea2df1fca97a`；preferredTerm-admn-sts）
  - 依据：[Terminology work and terminology science — Vocabulary · 2019](https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf) · §3.3.1，PDFp.12/印刷p.6 · 核对日期 2026-09-06

**历史形式**

无。

**历史注释**（`tc-e7c36840-9dc5-45d1-a371-920c28af2a00`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§6.2.3；§11.3.2.2；PDF page index 19；33-34；108 · 核对日期 2026-09-06

**定义**

**简体中文定义**

入表日期、变更记录、旧形式及有效期

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§6.2.3；§11.3.2.2；PDF page index 19；33-34；108 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 历史注释（`tm-d1bad412-4998-412f-9e3a-0fdf3c1e3740`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：历史注释记录术语的时间变化，与说明概念含义的范围注释区别；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- history note（`tm-d6b7cf59-38bf-4400-a676-04b7e516cdc1`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§6.2.3；§11.3.2.2；PDF page index 19；33-34；108 · 核对日期 2026-09-06

**历史形式**

无。

**编辑注释**（`tc-d6a34d9f-e8f9-4170-9d62-e5b3676e71d9`）


**概念依据**

- [ISO 25964-1 XML Schema · 1.4](https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd) · EditorialNote documentation · 核对日期 2026-09-06

**定义**

**简体中文定义**

供叙词表编辑者在编辑过程中使用的注释。

依据：
- [ISO 25964-1 XML Schema · 1.4](https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd) · EditorialNote documentation · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 编辑注释（`tm-50a8107f-fb70-4df7-be97-59c8f5ac72e8`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：编辑注释服务编辑过程，区别供用户理解概念范围的注释。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- editorial note（`tm-7595b7a0-4cc9-4006-8158-8e6e21dc605d`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1 XML Schema · 1.4](https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd) · EditorialNote documentation · 核对日期 2026-09-06

**历史形式**

无。

**候选词**（`tc-155c651f-9cb6-4e89-b394-9b843b268148`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§11.1.6；PDF page index 19；104 · 核对日期 2026-09-06

**定义**

**简体中文定义**

提出但未走完审批的词

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§11.1.6；PDF page index 19；104 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 候选词（`tm-e7b7cd31-246e-4986-b5d3-d2fa7cb059b0`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：候选词表示尚未完成收录审批的名称，而非来源实体状态；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- candidate term（`tm-8ec912e8-3242-45f7-bf32-97bd40f61efe`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§11.1.6；PDF page index 19；104 · 核对日期 2026-09-06
- provisional term（`tm-e995203f-bdd8-4c79-8368-d199e049c0d2`；admittedTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§11.1.6；PDF page index 19；104 · 核对日期 2026-09-06

**历史形式**

无。

**未标引词**（`tc-a17e54a7-07e9-459e-86cc-bd0c12e4d58b`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.8；PDF page index 104 · 核对日期 2026-09-06

**定义**

**简体中文定义**

为补全层级而收、尚未用于标引的词

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.8；PDF page index 104 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 未标引词（`tm-3d5a2c5e-8990-4a32-9a37-6a6b18d8f1e9`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：未标引词强调尚未实际分配给内容对象，不表示禁止使用；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- unassigned term（`tm-3f9dbaa9-c7b6-40d6-b4d1-8c83221df19b`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.8；PDF page index 104 · 核对日期 2026-09-06

**历史形式**

无。

**废弃词**（`tc-82db3b46-353e-405f-8a8d-fd6fee70bdb5`）


**概念依据**

- [Terminology work and terminology science — Vocabulary · 2019](https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf) · §3.4.21，GSO公开HTML预览；对照§3.4.22 obsolete term · 核对日期 2026-09-06

**定义**

**简体中文定义**

与首选术语同义，但在可接受性评价中被列为不宜使用的术语。

依据：
- [Terminology work and terminology science — Vocabulary · 2019](https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf) · §3.4.21，GSO公开HTML预览；对照§3.4.22 obsolete term · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 废弃词（`tm-e1b7439c-738a-4056-9c53-8e96b4b7d5ef`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：废弃词指不宜使用的名称评价，不自动包含删除、保留或替代链的项目操作；与不再常用的obsolete区别。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- deprecated term（`tm-5ec44c1d-1d30-4952-8a28-d82bc54f7669`；preferredTerm-admn-sts）
  - 依据：[Terminology work and terminology science — Vocabulary · 2019](https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf) · §3.4.21，GSO公开HTML预览；对照§3.4.22 obsolete term · 核对日期 2026-09-06

**历史形式**

无。

**孤儿词**（`tc-88088c7a-5aaf-458c-a55c-23ff38463ee0`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§11.4.4；PDF page index 19；112 · 核对日期 2026-09-06

**定义**

**简体中文定义**

没有任何层级或相关关系的词

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§11.4.4；PDF page index 19；112 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 孤儿词（`tm-d6b4f6d9-8e3f-4d8c-b418-79688e2cc5df`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：孤儿词是缺乏层级和相关联系的词表维护用语；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- orphan term（`tm-4311cc75-0005-46aa-a296-0c6c9aa89900`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §4.1；§11.4.4；PDF page index 19；112 · 核对日期 2026-09-06

**历史形式**

无。

**状态**（`tc-504af76c-f69e-469e-8e73-239f2fd3da99`）


**概念依据**

- [ISO 25964-1 XML Schema · 1.4](https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd) · ThesaurusConceptStruct/status与ThesaurusTerm/status文档注记 · 核对日期 2026-09-06

**定义**

**简体中文定义**

表示概念或术语在管理过程中所处阶段的属性。

依据：
- [ISO 25964-1 XML Schema · 1.4](https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd) · ThesaurusConceptStruct/status与ThesaurusTerm/status文档注记 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 状态（`tm-f9159807-4154-4be9-8a5c-4039896902fa`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：状态是阶段属性，来源示例值不覆盖本库状态机。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- status（`tm-da14faa1-b603-4b39-9e6c-37a797c42b2b`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1 XML Schema · 1.4](https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd) · ThesaurusConceptStruct/status与ThesaurusTerm/status文档注记 · 核对日期 2026-09-06

**历史形式**

无。

**版本历史**（`tc-f4802cd3-fba8-4bb1-89a0-121eebbf1fc6`）


**概念依据**

- [The ISO 25964 data model for the structure of an information retrieval thesaurus · 2012](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413) · Version History，L145–147，自然英文version history直接出现 · 核对日期 2026-09-06

**定义**

**简体中文定义**

词表已发布或提供的各个版本的记录，说明版本间的区别以及各版本是否仍为现行。

依据：
- [The ISO 25964 data model for the structure of an information retrieval thesaurus · 2012](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413) · Version History，L145–147，自然英文version history直接出现 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 版本历史（`tm-9ac2e455-f438-460f-ad02-baf7377a105d`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：版本历史记录词表整体版次，非单条术语的变更历史；不再依靠CamelCase拆词推断形式。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- version history（`tm-ec43572b-e2e5-4c4a-8fb1-6be8931c3635`；preferredTerm-admn-sts）
  - 依据：[The ISO 25964 data model for the structure of an information retrieval thesaurus · 2012](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413) · Version History，L145–147，自然英文version history直接出现 · 核对日期 2026-09-06

**历史形式**

无。

## 建设与治理

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| 依据 | warrant | zh-Hans：选择一个词进入受控词表的理由或支持。 | — | tc-d529a566-45fc-44f0-8b92-0eca58807137 |
| 文献依据 | literary warrant | zh-Hans：词是领域文献里实际通行的说法 | — | tc-6cb09f56-afea-40d2-a986-c0d80d376363 |
| 组织依据 | organizational warrant | zh-Hans：词是使用组织偏好的形式 | — | tc-1ad36b83-83d4-4174-8cc0-a6189b8ce11b |
| 用户依据 | user warrant | zh-Hans：词是用户检索时实际用的说法 | — | tc-60cd4ded-814a-46d1-9bd6-360f1b725ca0 |
| 自上而下 | top down | zh-Hans：委员会建设词表时先识别最宽泛的词，再选择下位词达到所需具体程度，并建立层级和关系。 | — | tc-ddf950fe-a885-4424-82f9-cfbb5d4ab330 |
| 自下而上 | bottom up | zh-Hans：委员会建设词表时从内容对象语料得到的词开始，由范围最窄的词向更一般的词组织层级。 | — | tc-6f960f39-1a53-4215-932e-a89f837ac06c |
| 演绎法 | deductive | zh-Hans：词表经验建设方法：先从内容对象收集足够数量的词，再由专家确定关系并从宽到窄组织层级。 | — | tc-208354ed-1338-4152-be98-ca93504c3355 |
| 归纳法 | inductive | zh-Hans：词表经验建设方法：遇到词时即选择纳入，从一开始实施词汇控制，并持续将词放入较宽类别。 | — | tc-c9b65491-09a6-4765-b208-6601af494f31 |
| 分析综合式分类 | analytico-synthetic classification | zh-Hans：先把主题分析为基本概念或分面，再依规定组合次序综合表示主题的分类方法。 | — | tc-8b56b1d2-7fd1-499b-8085-a9dd926e4c28 |
| 好客准则 | canon of hospitality | zh-Hans：要求分类法能够在数组和链中容纳新增类目及类号，并保持既有安排的准则。 | — | tc-b888a0b9-0011-4e55-b6a5-bb01e56b79aa |
| 领域分析 | domain analysis | zh-Hans：把知识领域作为社会中的思想或话语共同体，结合社会学和认识论立场研究其知识组织过程与系统的方法。 | — | tc-f91d813f-7dfd-4aae-9198-756996799dd3 |
| 剩余类目 | residual category | zh-Hans：给定分类系统中无法得到正式表示的类目。 | — | tc-b96d261a-9203-4f68-8b78-92e2667818ea |
| 词汇控制 | vocabulary control | zh-Hans：通过控制同义词、区分同形异义词并建立词间关系，使标引者和检索者能够一致表达概念的过程。 | — | tc-60ca56e9-0bf5-4e06-86c4-b6941a9adc6e |
| 标引 | indexing | zh-Hans：分析文档主题、识别概念，并分配相应标引词以便检索的活动。 | — | tc-d123d909-3897-427f-9e04-e31d9072176c |
| 标引词 | index term | zh-Hans：在标引过程中分配给文档的术语。 | — | tc-7e07c6f9-8677-4b87-8e32-e23d72dbfe64 |
| 查全率 | recall | zh-Hans：检索系统检出集合中全部相关内容对象的能力；通常以检出的相关内容对象数除以集合中全部相关内容对象数计算百分比。高查全率意味着更全面，但也可能增加检出不相关内容对象的风险。 | — | tc-dfe493d2-f173-4a9e-ace9-b9ffad3f0f0f |
| 查准率 | precision | zh-Hans：检索系统只检出相关内容对象的能力；通常以检出的相关内容对象数除以检出的内容对象总数计算百分比。高查准率提高结果相关性，但可能漏掉部分相关对象。 | — | tc-11e8d232-85f8-4e00-98a0-d8bdd7adf639 |
| 互操作性 | interoperability | zh-Hans：两个或更多系统或组件交换并使用所交换信息的能力。 | — | tc-98d2d330-cabe-493f-8453-104822e92a0d |

**依据**（`tc-d529a566-45fc-44f0-8b92-0eca58807137`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.3.5 Warrant，印刷p.16 · 核对日期 2026-09-06

**定义**

**简体中文定义**

选择一个词进入受控词表的理由或支持。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.3.5 Warrant，印刷p.16 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 依据（`tm-f188b119-c518-45fa-986c-67d6f6801238`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：依据在此限定收词选择，不泛化成任意字段basis。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- warrant（`tm-1bf1d191-63fe-4c9e-9761-a2543c13f382`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.3.5 Warrant，印刷p.16 · 核对日期 2026-09-06

**历史形式**

无。

**文献依据**（`tc-6cb09f56-afea-40d2-a986-c0d80d376363`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.3.5.1；PDF page index 27 · 核对日期 2026-09-06

**定义**

**简体中文定义**

词是领域文献里实际通行的说法

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.3.5.1；PDF page index 27 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 文献依据（`tm-dfed1194-5cd6-48d1-8667-a5c47ebb30bb`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：文献依据以领域文献中的实际使用作为收词理由；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- literary warrant（`tm-2bcd97cb-cdf8-4d28-b8ab-7e688f8d1d7e`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.3.5.1；PDF page index 27 · 核对日期 2026-09-06

**历史形式**

无。

**组织依据**（`tc-1ad36b83-83d4-4174-8cc0-a6189b8ce11b`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.3.5.2；PDF page index 27 · 核对日期 2026-09-06

**定义**

**简体中文定义**

词是使用组织偏好的形式

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.3.5.2；PDF page index 27 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 组织依据（`tm-b7475d7a-e888-4f21-ac57-b1801222311e`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：组织依据突出采用组织偏好的名称形式；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- organizational warrant（`tm-7046ee19-1db6-4df4-9664-aa85f07387fb`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.3.5.2；PDF page index 27 · 核对日期 2026-09-06

**历史形式**

无。

**用户依据**（`tc-60cd4ded-814a-46d1-9bd6-360f1b725ca0`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.3.5.3；PDF page index 27 · 核对日期 2026-09-06

**定义**

**简体中文定义**

词是用户检索时实际用的说法

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.3.5.3；PDF page index 27 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 用户依据（`tm-dcdba69e-639f-4ce6-b2ab-bea261846a7f`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：用户依据反映检索用户实际使用的表达；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- user warrant（`tm-e4155133-bdc6-4af2-9231-29ac5963363d`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §5.3.5.3；PDF page index 27 · 核对日期 2026-09-06

**历史形式**

无。

**自上而下**（`tc-ddf950fe-a885-4424-82f9-cfbb5d4ab330`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json · 核对日期 2026-09-06

**定义**

**简体中文定义**

委员会建设词表时先识别最宽泛的词，再选择下位词达到所需具体程度，并建立层级和关系。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 自上而下（`tm-713d5d4c-9326-478f-8e94-b0e5f690c812`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：自上而下保留从宽到窄的词表建设方向；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- top down（`tm-486daf92-5ede-4f80-a324-75c113c41708`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json · 核对日期 2026-09-06

**历史形式**

无。

**自下而上**（`tc-6f960f39-1a53-4215-932e-a89f837ac06c`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json · 核对日期 2026-09-06

**定义**

**简体中文定义**

委员会建设词表时从内容对象语料得到的词开始，由范围最窄的词向更一般的词组织层级。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 自下而上（`tm-a3a9225d-75eb-41bb-b912-c8b01a442062`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：自下而上保留从具体语料词向一般词组织的方向；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- bottom up（`tm-7bf170bd-f546-4f38-aa43-51e301cc2976`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json · 核对日期 2026-09-06

**历史形式**

无。

**演绎法**（`tc-208354ed-1338-4152-be98-ca93504c3355`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json · 核对日期 2026-09-06

**定义**

**简体中文定义**

词表经验建设方法：先从内容对象收集足够数量的词，再由专家确定关系并从宽到窄组织层级。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 演绎法（`tm-3f18476e-cd74-4c14-a5d1-94361a9c6bc8`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：演绎法在此是 NISO 词表建设方法的既有表达，不外推到逻辑学推理定义；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- deductive（`tm-fc3bf25c-4cd0-4393-9aca-20543b39de42`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json · 核对日期 2026-09-06

**历史形式**

无。

**归纳法**（`tc-c9b65491-09a6-4765-b208-6601af494f31`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json · 核对日期 2026-09-06

**定义**

**简体中文定义**

词表经验建设方法：遇到词时即选择纳入，从一开始实施词汇控制，并持续将词放入较宽类别。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 归纳法（`tm-31f1c425-6625-40c3-9f7d-a23b93e495fe`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：归纳法在此突出从一开始控制和逐项组织词汇，不与普通逻辑学定义混同；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- inductive（`tm-bd7ee62c-43b5-4878-8023-dfdfc68f03d2`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json · 核对日期 2026-09-06

**历史形式**

无。

**分析综合式分类**（`tc-8b56b1d2-7fd1-499b-8085-a9dd926e4c28`）


**概念依据**

- [Facet analysis](https://www.isko.org/cyclo/facet_analysis) · §3 Basic principles of facet analysis · 核对日期 2026-09-06

**定义**

**简体中文定义**

先把主题分析为基本概念或分面，再依规定组合次序综合表示主题的分类方法。

依据：
- [Facet analysis](https://www.isko.org/cyclo/facet_analysis) · §3 Basic principles of facet analysis · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 分析综合式分类（`tm-5a5ad88a-778f-4cb4-ae7f-3e586fc400a2`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：分析综合式分类保留先分析后综合机制；作者后续原文可作定义依据，不伪报已读Ranganathan1957。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- analytico-synthetic classification（`tm-9c96c16a-7bfc-4949-8ebb-1d44e3ae2d49`；preferredTerm-admn-sts）
  - 依据：[Facet analysis](https://www.isko.org/cyclo/facet_analysis) · §3 Basic principles of facet analysis · 核对日期 2026-09-06

**历史形式**

无。

**好客准则**（`tc-b888a0b9-0011-4e55-b6a5-bb01e56b79aa`）


**概念依据**

- [Canons in Analytico-Synthetic Classification · 1980](https://article.imrpress.com/journal/KO/7/3/10.5771/0943-7444-1980-3-118/4a183d5ac38a2c528b0133c11817a7a7.pdf) · §2，印刷p.118；§7/7.1/7.2，印刷p.125 · 核对日期 2026-09-06

**定义**

**简体中文定义**

要求分类法能够在数组和链中容纳新增类目及类号，并保持既有安排的准则。

依据：
- [Canons in Analytico-Synthetic Classification · 1980](https://article.imrpress.com/journal/KO/7/3/10.5771/0943-7444-1980-3-118/4a183d5ac38a2c528b0133c11817a7a7.pdf) · §2，印刷p.118；§7/7.1/7.2，印刷p.125 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 好客准则（`tm-4fa46a60-3253-406e-b720-84673ef1bdc4`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：好客准则在分类学中指容纳新类目的能力，保留数组和链两个方面，不新增两种概念。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- canon of hospitality（`tm-80141b21-b90d-4ca3-8735-7a022c1a88b1`；preferredTerm-admn-sts）
  - 依据：[Canons in Analytico-Synthetic Classification · 1980](https://article.imrpress.com/journal/KO/7/3/10.5771/0943-7444-1980-3-118/4a183d5ac38a2c528b0133c11817a7a7.pdf) · §2，印刷p.118；§7/7.1/7.2，印刷p.125 · 核对日期 2026-09-06

**历史形式**

无。

**领域分析**（`tc-f91d813f-7dfd-4aae-9198-756996799dd3`）


**概念依据**

- [Domain analysis · 2024-09-02](https://www.isko.org/cyclo/domain_analysis) · §1.1/1.2/1.4/2.1/4.7/7；作者实际网页正文 · 核对日期 2026-09-06

**定义**

**简体中文定义**

把知识领域作为社会中的思想或话语共同体，结合社会学和认识论立场研究其知识组织过程与系统的方法。

依据：
- [Domain analysis · 2024-09-02](https://www.isko.org/cyclo/domain_analysis) · §1.1/1.2/1.4/2.1/4.7/7；作者实际网页正文 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 领域分析（`tm-aa71dcf0-b589-4daf-8125-e27672bebe75`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：领域分析保留LIS中的共同体、专门知识与认识论机制；不换成软件工程domain analysis，不将没有唯一正确分类写成绝对定律。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- domain analysis（`tm-5efaa936-a3bb-4f9a-b5c9-e2a3d64af7de`；preferredTerm-admn-sts）
  - 依据：[Domain analysis · 2024-09-02](https://www.isko.org/cyclo/domain_analysis) · §1.1/1.2/1.4/2.1/4.7/7；作者实际网页正文 · 核对日期 2026-09-06

**历史形式**

无。

**剩余类目**（`tc-b96d261a-9203-4f68-8b78-92e2667818ea`）


**概念依据**

- [Enacting silence · 2007](https://link.springer.com/article/10.1007/s10676-007-9141-7) · 原作者论文Abstract，Ethics and Information Technology9(2007)273–280 · 核对日期 2026-09-06

**定义**

**简体中文定义**

给定分类系统中无法得到正式表示的类目。

依据：
- [Enacting silence · 2007](https://link.springer.com/article/10.1007/s10676-007-9141-7) · 原作者论文Abstract，Ethics and Information Technology9(2007)273–280 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 剩余类目（`tm-ef7fbfce-26f3-4f02-aa2d-ec9380f73b15`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：剩余类目以分类无法正式表示为边界；旧其他/杂项是例子，大小必然说明失效的断言没有随定义采纳。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- residual category（`tm-135147b0-7149-4c14-9d10-d4863a83edf2`；preferredTerm-admn-sts）
  - 依据：[Enacting silence · 2007](https://link.springer.com/article/10.1007/s10676-007-9141-7) · 原作者论文Abstract，Ethics and Information Technology9(2007)273–280 · 核对日期 2026-09-06

**历史形式**

无。

**词汇控制**（`tc-60ca56e9-0bf5-4e06-86c4-b6941a9adc6e`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §1.2；§4.1；PDF page index 12；21 · 核对日期 2026-09-06

**定义**

**简体中文定义**

通过控制同义词、区分同形异义词并建立词间关系，使标引者和检索者能够一致表达概念的过程。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §1.2；§4.1；PDF page index 12；21 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 词汇控制（`tm-614c6eb9-c481-41b5-8374-d4be3d62b4d5`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：词汇控制是协调同义、异义和关系以使标引检索一致的行业表达；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- vocabulary control（`tm-1492b91e-ee09-46b6-b487-6d769897554e`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §1.2；§4.1；PDF page index 12；21 · 核对日期 2026-09-06

**历史形式**

无。

**标引**（`tc-d123d909-3897-427f-9e04-e31d9072176c`）


**概念依据**

- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.36，PDFp.12，原始读取L470–486 · 核对日期 2026-09-06

**定义**

**简体中文定义**

分析文档主题、识别概念，并分配相应标引词以便检索的活动。

依据：
- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.36，PDFp.12，原始读取L470–486 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 标引（`tm-8d8dd91c-4bfe-42e2-84b3-f30e00b13677`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：标引既有主题分析又有分配术语；引用实际已读Part2定义，不把原Part1定位伪称重读。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- indexing（`tm-f8d9b426-d08f-4ea6-a77d-ca28e4261912`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.36，PDFp.12，原始读取L470–486 · 核对日期 2026-09-06

**历史形式**

无。

**标引词**（`tc-7e07c6f9-8677-4b87-8e32-e23d72dbfe64`）


**概念依据**

- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.35，PDFp.12，L470–473 · 核对日期 2026-09-06

**定义**

**简体中文定义**

在标引过程中分配给文档的术语。

依据：
- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.35，PDFp.12，L470–473 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 标引词（`tm-f997b0b2-4bfa-4973-90c8-dc07241e3d22`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：标引词由分配行为和文档对象界定；keyword/tag宽泛比较单列而不当必要定义。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- index term（`tm-0a9be29e-5fb3-4d41-b287-80801423734c`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.35，PDFp.12，L470–473 · 核对日期 2026-09-06

**历史形式**

无。

**查全率**（`tc-dfe493d2-f173-4a9e-ace9-b9ffad3f0f0f`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 947-955 · 核对日期 2026-09-06

**定义**

**简体中文定义**

检索系统检出集合中全部相关内容对象的能力；通常以检出的相关内容对象数除以集合中全部相关内容对象数计算百分比。高查全率意味着更全面，但也可能增加检出不相关内容对象的风险。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 947-955 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 查全率（`tm-119ca7ee-aa9d-4d04-b352-b214e2ea3962`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：查全率是信息检索中对全部相关对象检出程度的行业名称；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- recall（`tm-35a8bfd4-703e-41ec-bb76-9b05e048608c`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 947-955 · 核对日期 2026-09-06

**历史形式**

无。

**查准率**（`tc-11e8d232-85f8-4e00-98a0-d8bdd7adf639`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 918-926 · 核对日期 2026-09-06

**定义**

**简体中文定义**

检索系统只检出相关内容对象的能力；通常以检出的相关内容对象数除以检出的内容对象总数计算百分比。高查准率提高结果相关性，但可能漏掉部分相关对象。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 918-926 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 查准率（`tm-bd0ee821-6214-4efe-8771-67403605f612`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：查准率是信息检索中对检出结果相关程度的行业名称；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- precision（`tm-9962ad11-5853-4ed6-aa79-43335bb9aa59`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 918-926 · 核对日期 2026-09-06

**历史形式**

无。

**互操作性**（`tc-98d2d330-cabe-493f-8453-104822e92a0d`）


**概念依据**

- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.29；docs/references/iso-25964.md 已核定义表 · 核对日期 2026-08-29

**定义**

**简体中文定义**

两个或更多系统或组件交换并使用所交换信息的能力。

依据：
- [ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.29；docs/references/iso-25964.md 已核定义表 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 互操作性（`tm-4270711e-8a98-48d0-9ba3-5a1fc25eaf22`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：互操作性同时包括信息交换与使用，不能仅等同文件可导入；仅为既有概念的模型知识译名判断，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- interoperability（`tm-fd044b18-8d70-430b-b64e-2c81f72632cf`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval · 2011](https://www.iso.org/standard/53657.html) · §2.29；docs/references/iso-25964.md 已核定义表 · 核对日期 2026-08-29

**历史形式**

无。

## 词表间映射

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| 映射 | mapping | zh-Hans：映射过程的产物，即一个词表中的一个概念与另一个词表中一个或多个概念之间的关系。 | — | tc-b544dcf4-e88e-4456-bb9e-824b74d7abc8 |
| 映射簇 | mapping cluster | zh-Hans：三个或更多词表的概念之间协调维护的一组映射。 | — | tc-c96ff99a-aef7-4d8d-b4d5-2c3e2835a64b |
| 名称规范表 | name authority list | zh-Hans：用于一致命名特定实体的受控词表；这些实体是唯一的个体而非类。 | — | tc-c47ee168-3ad4-4489-bc26-1cc64f94407f |
| 对照表 | crosswalk | zh-Hans：两个或更多结构化词表中的概念之间映射的表。 | — | tc-dc56c863-cea8-485d-afcd-c606ce2a8a4b |
| 源词表 | source vocabulary | zh-Hans：映射关系中提供被映射概念、作为出发端的词表。 | — | tc-14b64c1a-938e-4d43-8e05-e18e0dd4e4f3 |
| 目标词表 | target vocabulary | zh-Hans：映射关系中提供对应概念、作为目标端的词表。 | — | tc-b98ed928-3bbd-42a8-8f7f-b447c735b4c7 |
| 等价映射 | equivalence mapping | zh-Hans：说明目标词表中的概念与源词表中的概念在范围上被视为相同的映射。 | — | tc-405390d9-57dc-47ca-9317-0120d5aa86eb |
| 精确等价 | exact equivalence | zh-Hans：源词表与目标词表中的两个概念具有相同范围的等价关系。 | — | tc-5d5225be-ab9d-44e4-866b-e321c998d766 |
| 不精确等价 | inexact equivalence | zh-Hans：两个概念的范围有交集，但各自仍有另一概念未涵盖部分的等价关系。 | — | tc-11c76a96-ef73-4369-9650-0f044c8eb0e7 |
| 部分等价 | partial equivalence | zh-Hans：两个概念范围不相同，且一个概念范围完全包含在另一概念范围内的等价关系。 | — | tc-531f3821-4ee7-4345-831e-778371f56302 |
| 层级映射 | hierarchical mapping | zh-Hans：连接不同词表中范围较宽与较窄概念的有向映射；按目标相对源概念的范围区分宽义或狭义方向。 | — | tc-4d6508b0-a334-4017-aa7d-205469ae902e |
| 相关映射 | associative mapping | zh-Hans：连接不同词表中语义相关概念的映射；两端不属于同义、近义或宽窄关系。 | — | tc-64b64810-6aef-4db4-b09f-aa169129c448 |
| 区分式映射 | differentiated mapping | zh-Hans：旨在区分映射不同类型和质量的方法。 | — | tc-eb9e1973-6b39-47f1-8b3e-845798b14ba4 |
| 中心辐射 | hub structure | zh-Hans：指定一个词表作为中心，其他参与词表通过与中心建立概念映射而相互衔接的结构。 | — | tc-bf5e9356-ac91-49ae-9be3-8196dd66167c |

**映射**（`tc-b544dcf4-e88e-4456-bb9e-824b74d7abc8`）


**概念依据**

- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.41；docs/references/iso-25964.md 已核定义表 · 核对日期 2026-08-29

**定义**

**简体中文定义**

映射过程的产物，即一个词表中的一个概念与另一个词表中一个或多个概念之间的关系。

依据：
- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.41；docs/references/iso-25964.md 已核定义表 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 映射（`tm-9be97554-ada5-484d-848e-8d07cda553e1`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：映射是信息组织中表示不同词表概念对应关系的既有中文表达；本行严格限于 §3.41 关系产物，不引入过程义。外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- mapping（`tm-180f1491-60d9-4ad6-ba75-1ba53e68fc61`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.41；docs/references/iso-25964.md 已核定义表 · 核对日期 2026-08-29

**历史形式**

无。

**映射簇**（`tc-c96ff99a-aef7-4d8d-b4d5-2c3e2835a64b`）


**概念依据**

- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.42，PDFp.12，L512–518 · 核对日期 2026-09-06

**定义**

**简体中文定义**

三个或更多词表的概念之间协调维护的一组映射。

依据：
- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.42，PDFp.12，L512–518 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 映射簇（`tm-3911501b-963b-4f98-abdb-d9f4cc97b7e5`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：映射簇是协调的多词表映射集合，保留原三个或更多的源定义条件。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- mapping cluster（`tm-0b3df564-f31a-41b9-bcd8-ae62a8b5b2aa`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.42，PDFp.12，L512–518 · 核对日期 2026-09-06

**历史形式**

无。

**名称规范表**（`tc-c47ee168-3ad4-4489-bc26-1cc64f94407f`）


**概念依据**

- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.50；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

用于一致命名特定实体的受控词表；这些实体是唯一的个体而非类。

依据：
- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.50；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 名称规范表（`tm-a92be9a9-8e86-4aac-931c-4a5072bb461a`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：名称规范表是规范控制中对个体名称保持一致的名称列表表达；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- name authority list（`tm-6936dadd-bd45-487a-b3e1-0ec61a2f7c64`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.50；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**对照表**（`tc-dc56c863-cea8-485d-afcd-c606ce2a8a4b`）


**概念依据**

- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.21，PDFp.9，L360–363 · 核对日期 2026-09-06

**定义**

**简体中文定义**

两个或更多结构化词表中的概念之间映射的表。

依据：
- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.21，PDFp.9，L360–363 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 对照表（`tm-5976ab3d-1bf1-424f-af90-3fc111527a8e`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：对照表严格指原词表层crosswalk；不复用已撤的metadata-crosswalk提案ID或更换概念。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- crosswalk（`tm-145bf65b-7bb4-4d85-9511-95c04d9dd084`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.21，PDFp.9，L360–363 · 核对日期 2026-09-06

**历史形式**

无。

**源词表**（`tc-14b64c1a-938e-4d43-8e05-e18e0dd4e4f3`）


**概念依据**

- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.27，PDFp.10，L401–405 source/target两端语境 · 核对日期 2026-09-06

**定义**

**简体中文定义**

映射关系中提供被映射概念、作为出发端的词表。

依据：
- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.27，PDFp.10，L401–405 source/target两端语境 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 源词表（`tm-101132c3-86ad-4115-8d07-44caba815192`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：源词表是映射中的一端角色；原并列两项分开，不当同义词，不需制造未读独立条款。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- source vocabulary（`tm-2549ff94-fbe5-4854-bbba-79a658e6e46a`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.27，PDFp.10，L401–405 source/target两端语境 · 核对日期 2026-09-06

**历史形式**

无。

**目标词表**（`tc-b98ed928-3bbd-42a8-8f7f-b447c735b4c7`）


**概念依据**

- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.27，PDFp.10，L401–405 source/target两端语境 · 核对日期 2026-09-06

**定义**

**简体中文定义**

映射关系中提供对应概念、作为目标端的词表。

依据：
- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.27，PDFp.10，L401–405 source/target两端语境 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 目标词表（`tm-a946b241-c351-47b7-b4d8-e67a02a83c2c`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：目标词表是映射中的一端角色；原并列两项分开，不当同义词，不需制造未读独立条款。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- target vocabulary（`tm-7f2a566a-083a-48ee-9396-6cd2b7f100ff`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.27，PDFp.10，L401–405 source/target两端语境 · 核对日期 2026-09-06

**历史形式**

无。

**等价映射**（`tc-405390d9-57dc-47ca-9317-0120d5aa86eb`）


**概念依据**

- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.27；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

说明目标词表中的概念与源词表中的概念在范围上被视为相同的映射。

依据：
- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.27；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 等价映射（`tm-7d69db17-67ab-436d-9994-539c6702b0e0`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：等价映射限定跨词表的概念对应，与表内词的等价关系区分；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- equivalence mapping（`tm-a570aee4-b8a3-4fa4-a3a4-1d40403444dc`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.27；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**精确等价**（`tc-5d5225be-ab9d-44e4-866b-e321c998d766`）


**概念依据**

- [Differences between SKOS and ISO standards · 2009-02-13](https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html) · Mapping between thesauri a–c；L131–140 · 核对日期 2026-09-06

**定义**

**简体中文定义**

源词表与目标词表中的两个概念具有相同范围的等价关系。

依据：
- [Differences between SKOS and ISO standards · 2009-02-13](https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html) · Mapping between thesauri a–c；L131–140 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 精确等价（`tm-a10f14d1-2756-456f-90b1-754ad286e2a0`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：精确等价按Will2009明确范围判据解释；这是个人作者解释，不伪称ISO2013§11逐项核实或SKOS属性公理。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- exact equivalence（`tm-730b11b7-c904-4533-bdd1-ecaea57a3bf3`；preferredTerm-admn-sts）
  - 依据：[Differences between SKOS and ISO standards · 2009-02-13](https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html) · Mapping between thesauri a–c；L131–140 · 核对日期 2026-09-06

**历史形式**

无。

**不精确等价**（`tc-11c76a96-ef73-4369-9650-0f044c8eb0e7`）


**概念依据**

- [Differences between SKOS and ISO standards · 2009-02-13](https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html) · Mapping between thesauri a–c；L131–140 · 核对日期 2026-09-06

**定义**

**简体中文定义**

两个概念的范围有交集，但各自仍有另一概念未涵盖部分的等价关系。

依据：
- [Differences between SKOS and ISO standards · 2009-02-13](https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html) · Mapping between thesauri a–c；L131–140 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 不精确等价（`tm-04654a55-fb23-444b-a74f-36f6a8793cc3`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：不精确等价按Will2009明确范围判据解释；这是个人作者解释，不伪称ISO2013§11逐项核实或SKOS属性公理。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- inexact equivalence（`tm-4f940b74-b5de-43bc-8e22-502a17babe23`；preferredTerm-admn-sts）
  - 依据：[Differences between SKOS and ISO standards · 2009-02-13](https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html) · Mapping between thesauri a–c；L131–140 · 核对日期 2026-09-06

**历史形式**

无。

**部分等价**（`tc-531f3821-4ee7-4345-831e-778371f56302`）


**概念依据**

- [Differences between SKOS and ISO standards · 2009-02-13](https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html) · Mapping between thesauri a–c；L131–140 · 核对日期 2026-09-06

**定义**

**简体中文定义**

两个概念范围不相同，且一个概念范围完全包含在另一概念范围内的等价关系。

依据：
- [Differences between SKOS and ISO standards · 2009-02-13](https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html) · Mapping between thesauri a–c；L131–140 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 部分等价（`tm-8065ee4d-eebb-493d-ad78-20ad9edc976e`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：部分等价按Will2009明确范围判据解释；这是个人作者解释，不伪称ISO2013§11逐项核实或SKOS属性公理。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- partial equivalence（`tm-d33a709f-8a18-4c9e-8209-9d354dce8e4b`；preferredTerm-admn-sts）
  - 依据：[Differences between SKOS and ISO standards · 2009-02-13](https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html) · Mapping between thesauri a–c；L131–140 · 核对日期 2026-09-06

**历史形式**

无。

**层级映射**（`tc-4d6508b0-a334-4017-aa7d-205469ae902e`）


**概念依据**

- [The Information Retrieval Thesaurus](https://www.isko.org/cyclo/thesaurus) · §3.2/Figure3 · 核对日期 2026-09-06
- [MARC Proposal 2014-05 · 2014](https://wwws.loc.gov/marc/mac/2014/2014-05.html) · §1 BACKGROUND，BM/NM · 核对日期 2026-09-06

**定义**

**简体中文定义**

连接不同词表中范围较宽与较窄概念的有向映射；按目标相对源概念的范围区分宽义或狭义方向。

依据：
- [The Information Retrieval Thesaurus](https://www.isko.org/cyclo/thesaurus) · §3.2/Figure3 · 核对日期 2026-09-06
- [MARC Proposal 2014-05 · 2014](https://wwws.loc.gov/marc/mac/2014/2014-05.html) · §1 BACKGROUND，BM/NM · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 层级映射（`tm-d1c40f39-ba5d-446c-93dc-7d232d73facb`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：层级映射保留跨词表上下位及方向；不是把ISO原未读目录冒称正文。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- hierarchical mapping（`tm-f898b175-8fa7-45c1-94ef-c548e0928757`；preferredTerm-admn-sts）
  - 依据：[The Information Retrieval Thesaurus](https://www.isko.org/cyclo/thesaurus) · §3.2/Figure3 · 核对日期 2026-09-06
  - 依据：[MARC Proposal 2014-05 · 2014](https://wwws.loc.gov/marc/mac/2014/2014-05.html) · §1 BACKGROUND，BM/NM · 核对日期 2026-09-06

**历史形式**

无。

**相关映射**（`tc-64b64810-6aef-4db4-b09f-aa169129c448`）


**概念依据**

- [The Information Retrieval Thesaurus](https://www.isko.org/cyclo/thesaurus) · §3.2/Figure3 · 核对日期 2026-09-06
- [MARC Proposal 2014-05 · 2014](https://wwws.loc.gov/marc/mac/2014/2014-05.html) · §1 BACKGROUND，RM · 核对日期 2026-09-06

**定义**

**简体中文定义**

连接不同词表中语义相关概念的映射；两端不属于同义、近义或宽窄关系。

依据：
- [The Information Retrieval Thesaurus](https://www.isko.org/cyclo/thesaurus) · §3.2/Figure3 · 核对日期 2026-09-06
- [MARC Proposal 2014-05 · 2014](https://wwws.loc.gov/marc/mac/2014/2014-05.html) · §1 BACKGROUND，RM · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 相关映射（`tm-f3dee102-5326-406c-a50e-0035c274fb25`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：相关映射按原跨词表相关范围解释，排除等价与层级；不把RM代码新增为英文术语。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- associative mapping（`tm-d61bdf72-b103-4fd6-b4dd-75cf1bd7efdb`；preferredTerm-admn-sts）
  - 依据：[The Information Retrieval Thesaurus](https://www.isko.org/cyclo/thesaurus) · §3.2/Figure3 · 核对日期 2026-09-06
  - 依据：[MARC Proposal 2014-05 · 2014](https://wwws.loc.gov/marc/mac/2014/2014-05.html) · §1 BACKGROUND，RM · 核对日期 2026-09-06

**历史形式**

无。

**区分式映射**（`tc-eb9e1973-6b39-47f1-8b3e-845798b14ba4`）


**概念依据**

- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.23；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**定义**

**简体中文定义**

旨在区分映射不同类型和质量的方法。

依据：
- [ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.23；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**术语形式**

**简体中文形式**

- 区分式映射（`tm-8812567a-6b12-4d95-a87c-363250e59b95`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：区分式映射表达区分映射类型与质量的既有中文名称，不引入新的程度类别；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- differentiated mapping（`tm-63f76467-9cba-462a-bf20-40fa3ef63225`；preferredTerm-admn-sts）
  - 依据：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies · 2013](https://www.iso.org/standard/53658.html) · §3.23；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本 · 核对日期 2026-08-29

**历史形式**

无。

**中心辐射**（`tc-bf5e9356-ac91-49ae-9be3-8196dd66167c`）


**概念依据**

- [Interoperability · 2019](https://www.isko.org/cyclo/interoperability) · §5.2 Models of mapping process；Table2，期刊2019p.138 · 核对日期 2026-09-06

**定义**

**简体中文定义**

指定一个词表作为中心，其他参与词表通过与中心建立概念映射而相互衔接的结构。

依据：
- [Interoperability · 2019](https://www.isko.org/cyclo/interoperability) · §5.2 Models of mapping process；Table2，期刊2019p.138 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 中心辐射（`tm-bb2e31d0-f6c8-4913-9ed3-a7cde4cb69bd`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：中心辐射限定参与映射结构的词表，不要求世界上所有词表或所有非中心词表互相直接映射。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- hub structure（`tm-9a48db30-ee9b-44c4-8476-fff03dcf758f`；preferredTerm-admn-sts）
  - 依据：[Interoperability · 2019](https://www.isko.org/cyclo/interoperability) · §5.2 Models of mapping process；Table2，期刊2019p.138 · 核对日期 2026-09-06

**历史形式**

无。

## 知识体系

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| 知识体系 | body of knowledge | zh-Hans：一个学科或职业领域内的知识总和。 | en：BoK | tc-e340f2b4-4515-4203-b5d1-8bafee5af81a |
| 知识领域 | knowledge area | zh-Hans：CS2023知识模型中一组相互关联的知识单元。 | en：KA | tc-3945b496-c4ac-4553-81ad-4c6dab62d81c |
| 知识单元 | knowledge unit | zh-Hans：CS2023知识模型中一组相关主题以及这些主题的学习成果。 | en：KU | tc-89c27e71-9c5a-4e5e-a588-15c0ae59345d |
| 主题 | topic | zh-Hans：CS2023知识单元内的知识主题，按课程模型标为核心或选修。 | — | tc-c5f9771f-7271-4128-854d-88b12df9f7ed |
| 普遍接受的知识 | generally accepted knowledge | zh-Hans：在大多数项目的大多数情况下适用，且其价值和作用获得广泛共识的知识。 | — | tc-fbe9f215-a5f4-4292-92fa-b734f6c4b3ee |

**知识体系**（`tc-e340f2b4-4515-4203-b5d1-8bafee5af81a`）


**概念依据**

- [软件工程知识体系指南 v4.0 / Guide to the Software Engineering Body of Knowledge v4.0 · 4.0](https://www.computer.org/education/bodies-of-knowledge/software-engineering) · 官方页面Focus on Generally Accepted Knowledge；实际urllib读取 · 核对日期 2026-09-06

**定义**

**简体中文定义**

一个学科或职业领域内的知识总和。

依据：
- [软件工程知识体系指南 v4.0 / Guide to the Software Engineering Body of Knowledge v4.0 · 4.0](https://www.computer.org/education/bodies-of-knowledge/software-engineering) · 官方页面Focus on Generally Accepted Knowledge；实际urllib读取 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 知识体系（`tm-7e28b4bb-070a-496c-a255-42b104a2f334`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：知识体系指知识总和，不是Guide的结构化清单；Guide仅描述其中普遍接受的部分。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- body of knowledge（`tm-96fe4b79-c997-4371-be2c-34cffcfa045c`；preferredTerm-admn-sts）
  - 依据：[软件工程知识体系指南 v4.0 / Guide to the Software Engineering Body of Knowledge v4.0 · 4.0](https://www.computer.org/education/bodies-of-knowledge/software-engineering) · 官方页面Focus on Generally Accepted Knowledge；实际urllib读取 · 核对日期 2026-09-06
- BoK（`tm-4fe0093b-b34e-4012-b499-5fede4796ac8`；admittedTerm-admn-sts）
  - 依据：[软件工程知识体系指南 v4.0 / Guide to the Software Engineering Body of Knowledge v4.0 · 4.0](https://www.computer.org/education/bodies-of-knowledge/software-engineering) · 官方页面Focus on Generally Accepted Knowledge；实际urllib读取 · 核对日期 2026-09-06

**历史形式**

无。

**知识领域**（`tc-3945b496-c4ac-4553-81ad-4c6dab62d81c`）


**概念依据**

- [计算机科学课程 2023 / Computer Science Curricula 2023 · 2024-01](https://csed.acm.org/final-report/) · 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1 · 核对日期 2026-09-06

**定义**

**简体中文定义**

CS2023知识模型中一组相互关联的知识单元。

依据：
- [计算机科学课程 2023 / Computer Science Curricula 2023 · 2024-01](https://csed.acm.org/final-report/) · 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 知识领域（`tm-1e9a4505-f837-4791-b088-dbf23a42b1a5`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：知识领域在此限定来源模型分组，不外推出所有知识体系固定层数。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- knowledge area（`tm-fefcd455-00ba-430b-9a70-6a62d846f22c`；preferredTerm-admn-sts）
  - 依据：[计算机科学课程 2023 / Computer Science Curricula 2023 · 2024-01](https://csed.acm.org/final-report/) · 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1 · 核对日期 2026-09-06
- KA（`tm-886ced2e-3c75-4147-9fda-ad2d6197f9db`；admittedTerm-admn-sts）
  - 依据：[计算机科学课程 2023 / Computer Science Curricula 2023 · 2024-01](https://csed.acm.org/final-report/) · 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1 · 核对日期 2026-09-06

**历史形式**

无。

**知识单元**（`tc-89c27e71-9c5a-4e5e-a588-15c0ae59345d`）


**概念依据**

- [计算机科学课程 2023 / Computer Science Curricula 2023 · 2024-01](https://csed.acm.org/final-report/) · 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1 · 核对日期 2026-09-06

**定义**

**简体中文定义**

CS2023知识模型中一组相关主题以及这些主题的学习成果。

依据：
- [计算机科学课程 2023 / Computer Science Curricula 2023 · 2024-01](https://csed.acm.org/final-report/) · 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 知识单元（`tm-30d3ded1-73eb-4069-911b-4a8c7615a2b8`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：知识单元不仅是主题簇，补足来源明确的学习成果。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- knowledge unit（`tm-41116f5f-b8a3-4a24-ba19-d630df03609c`；preferredTerm-admn-sts）
  - 依据：[计算机科学课程 2023 / Computer Science Curricula 2023 · 2024-01](https://csed.acm.org/final-report/) · 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1 · 核对日期 2026-09-06
- KU（`tm-706fc397-2755-416b-8987-c49b655a6257`；admittedTerm-admn-sts）
  - 依据：[计算机科学课程 2023 / Computer Science Curricula 2023 · 2024-01](https://csed.acm.org/final-report/) · 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1 · 核对日期 2026-09-06

**历史形式**

无。

**主题**（`tc-c5f9771f-7271-4128-854d-88b12df9f7ed`）


**概念依据**

- [计算机科学课程 2023 / Computer Science Curricula 2023 · 2024-01](https://csed.acm.org/final-report/) · 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1 · 核对日期 2026-09-06

**定义**

**简体中文定义**

CS2023知识单元内的知识主题，按课程模型标为核心或选修。

依据：
- [计算机科学课程 2023 / Computer Science Curricula 2023 · 2024-01](https://csed.acm.org/final-report/) · 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 主题（`tm-58846829-6118-4a4a-b97c-8ebb5f11ede7`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：主题在本行限知识单元组成内容，核心/选修为来源课程属性，不改变本库topics层级或状态。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- topic（`tm-dddee160-7342-44b8-8fe9-6eb8c6e47880`；preferredTerm-admn-sts）
  - 依据：[计算机科学课程 2023 / Computer Science Curricula 2023 · 2024-01](https://csed.acm.org/final-report/) · 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1 · 核对日期 2026-09-06

**历史形式**

无。

**普遍接受的知识**（`tc-fbe9f215-a5f4-4292-92fa-b734f6c4b3ee`）


**概念依据**

- [软件工程知识体系指南 v4.0 / Guide to the Software Engineering Body of Knowledge v4.0 · 4.0](https://www.computer.org/education/bodies-of-knowledge/software-engineering) · 官方FAQ How do you define generally accepted knowledge?；实际urllib读取 · 核对日期 2026-09-06

**定义**

**简体中文定义**

在大多数项目的大多数情况下适用，且其价值和作用获得广泛共识的知识。

依据：
- [软件工程知识体系指南 v4.0 / Guide to the Software Engineering Body of Knowledge v4.0 · 4.0](https://www.computer.org/education/bodies-of-knowledge/software-engineering) · 官方FAQ How do you define generally accepted knowledge?；实际urllib读取 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 普遍接受的知识（`tm-87f6f03d-4e23-47f5-bf01-a50df55d039e`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：普遍接受的知识保持SWEBOK所引PMI语境，不要求所有项目统一应用；删除全部知识体系只收此子集的旧混淆。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- generally accepted knowledge（`tm-192f1290-b8f5-4bc8-88e1-e9e59f3c076b`；preferredTerm-admn-sts）
  - 依据：[软件工程知识体系指南 v4.0 / Guide to the Software Engineering Body of Knowledge v4.0 · 4.0](https://www.computer.org/education/bodies-of-knowledge/software-engineering) · 官方FAQ How do you define generally accepted knowledge?；实际urllib读取 · 核对日期 2026-09-06

**历史形式**

无。

## 元数据

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| — | Dublin Core Metadata Element Set | zh-Hans：由十五个元素构成的通用元数据元素集。 | en：Dublin Core | tc-42c4b942-41ba-486e-903d-1f2f18e37e45 |
| — | DCMI Metadata Terms | zh-Hans：DCMI 维护的元数据属性、类、数据类型和词表编码方案集合。 | — | tc-99ace251-fdee-4ab9-93e8-a016e7e98127 |
| — | DCMI Type Vocabulary | zh-Hans：用于按资源性质或体裁分类的 DCMI 类集合。 | — | tc-3f06d868-d7d2-4612-ad2b-35614912ba40 |
| 资源 | resource | zh-Hans：被元数据描述的对象，例如文档、图像、数据集和软件。 | — | tc-30abb1cd-3364-4b41-a0e9-e0b8338aa348 |
| 内容单元 | — | zh-Hans：知识库中可独立引用、可独立标引的最小内容单位；有标题，并围绕一个主题组织。 | — | tc-56bf269d-a675-4fc3-a2c1-b1f38a734d81 |

**Dublin Core Metadata Element Set**（`tc-42c4b942-41ba-486e-903d-1f2f18e37e45`）


**概念依据**

- [DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1 Introduction；/elements/1.1十五元素集说明 · 核对日期 2026-09-06

**定义**

**简体中文定义**

由十五个元素构成的通用元数据元素集。

依据：
- [DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1 Introduction；/elements/1.1十五元素集说明 · 核对日期 2026-09-06

**术语形式**

**英文形式**

- Dublin Core Metadata Element Set（`tm-b85464df-26a7-4638-91c8-5444d5bb0b22`；preferredTerm-admn-sts）
  - 依据：[DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1 Introduction；/elements/1.1十五元素集说明 · 核对日期 2026-09-06
- Dublin Core（`tm-844d9f9e-7c57-4bcb-9f9f-434c46fd2129`；admittedTerm-admn-sts）
  - 依据：[DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1 Introduction；/elements/1.1十五元素集说明 · 核对日期 2026-09-06

**历史形式**

无。

**DCMI Metadata Terms**（`tc-99ace251-fdee-4ab9-93e8-a016e7e98127`）


**概念依据**

- [DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1；DCMIType 条目；dc:type 条目；DCMI Metadata Terms 包含 properties、classes、datatypes、vocabulary encoding schemes；不是只有属性与类 · 核对日期 2026-09-06

**定义**

**简体中文定义**

DCMI 维护的元数据属性、类、数据类型和词表编码方案集合。

依据：
- [DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1；DCMIType 条目；dc:type 条目；DCMI Metadata Terms 包含 properties、classes、datatypes、vocabulary encoding schemes；不是只有属性与类 · 核对日期 2026-09-06

**术语形式**

**英文形式**

- DCMI Metadata Terms（`tm-94cd7a7d-4b17-4493-968d-12bdee0c0bb7`；preferredTerm-admn-sts）
  - 依据：[DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1；DCMIType 条目；dc:type 条目；DCMI Metadata Terms 包含 properties、classes、datatypes、vocabulary encoding schemes；不是只有属性与类 · 核对日期 2026-09-06

**历史形式**

无。

**DCMI Type Vocabulary**（`tc-3f06d868-d7d2-4612-ad2b-35614912ba40`）


**概念依据**

- [DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1；DCMIType 条目；dc:type 条目；DCMI 官方将 DCMIType 定义为用于分类资源性质或体裁的类集合；`dcterms:type` 建议使用受控词表 · 核对日期 2026-09-06

**定义**

**简体中文定义**

用于按资源性质或体裁分类的 DCMI 类集合。

依据：
- [DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1；DCMIType 条目；dc:type 条目；DCMI 官方将 DCMIType 定义为用于分类资源性质或体裁的类集合；`dcterms:type` 建议使用受控词表 · 核对日期 2026-09-06

**术语形式**

**英文形式**

- DCMI Type Vocabulary（`tm-f04583f9-f962-4c1f-bf3e-8cf3748b4205`；preferredTerm-admn-sts）
  - 依据：[DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1；DCMIType 条目；dc:type 条目；DCMI 官方将 DCMIType 定义为用于分类资源性质或体裁的类集合；`dcterms:type` 建议使用受控词表 · 核对日期 2026-09-06

**历史形式**

无。

**资源**（`tc-30abb1cd-3364-4b41-a0e9-e0b8338aa348`）


**概念依据**

- [DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1 Introduction and Definitions；资源描述语境 · 核对日期 2026-09-06

**定义**

**简体中文定义**

被元数据描述的对象，例如文档、图像、数据集和软件。

依据：
- [DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1 Introduction and Definitions；资源描述语境 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 资源（`tm-58221260-71b0-4fe5-a010-49fa7a359bb7`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：资源以被描述对象为范围，示例不是封闭枚举，不引入rdfs:Resource类身份。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- resource（`tm-e034d071-30c6-4f9d-ad39-0c283caceccf`；preferredTerm-admn-sts）
  - 依据：[DCMI Metadata Terms · 2020-01-20](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · §1 Introduction and Definitions；资源描述语境 · 核对日期 2026-09-06

**历史形式**

无。

**内容单元**（`tc-56bf269d-a675-4fc3-a2c1-b1f38a734d81`）


**概念依据**

- 项目决定依据，不是外部来源
- 采纳决定：decision-term-data-values
- 项目原文：`aae24737ff25cb8fbdb9ab9086b162dfb144ab81:docs/design/model/content-model.md` · 内容单元；并参docs/decisions/form-independence.md后果
- 采用理由：既有项目定义，DITA只作参考，不冒充外部同概念定义

**定义**

**简体中文定义**

知识库中可独立引用、可独立标引的最小内容单位；有标题，并围绕一个主题组织。

依据：
- 项目决定依据，不是外部来源
- 采纳决定：decision-term-data-values
- 项目原文：`aae24737ff25cb8fbdb9ab9086b162dfb144ab81:docs/design/model/content-model.md` · 内容单元；并参docs/decisions/form-independence.md后果
- 采用理由：既有项目定义，DITA只作参考，不冒充外部同概念定义

**术语形式**

**简体中文形式**

- 内容单元（`tm-55467569-4a21-4fae-a9ad-ef64e59f47f3`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：内容单元继承现行项目模型与form-independence决定，不等同DITA topic；没有已确认英文形式，不补造英文。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**历史形式**

无。

## 应用与生成

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| — | Application Profile | zh-Hans：为特定应用规定 metadata term、约束、使用与编码语法的文档集合 | — | tc-cb8ba91f-0bce-4b3d-ac6a-26bfca9ab7c9 |
| — | Reproducible Builds | zh-Hans：软件产品的构建过程具有可重现性，是指在指定其源码的具体版本及全部构建依赖后，无论在哪种环境执行，每次构建都产生逐比特相同的产物。 | — | tc-224b9f45-d624-4543-bc81-f64d02f81aa0 |

**Application Profile**（`tc-cb8ba91f-0bce-4b3d-ac6a-26bfca9ab7c9`）


**概念依据**

- [The Singapore Framework for Dublin Core™ Application Profiles · 2008-01-14](https://www.dublincore.org/specifications/dublin-core/singapore-framework/) · §3.1–3.3；docs/references/dcmi-application-profiles.md 已核阅读范围 · 核对日期 2026-09-01

**定义**

**简体中文定义**

为特定应用规定 metadata term、约束、使用与编码语法的文档集合

依据：
- [The Singapore Framework for Dublin Core™ Application Profiles · 2008-01-14](https://www.dublincore.org/specifications/dublin-core/singapore-framework/) · §3.1–3.3；docs/references/dcmi-application-profiles.md 已核阅读范围 · 核对日期 2026-09-01

**术语形式**

**英文形式**

- Application Profile（`tm-e35cfb69-400f-4114-925b-5b139615c090`；preferredTerm-admn-sts）
  - 依据：[The Singapore Framework for Dublin Core™ Application Profiles · 2008-01-14](https://www.dublincore.org/specifications/dublin-core/singapore-framework/) · §3.1–3.3；docs/references/dcmi-application-profiles.md 已核阅读范围 · 核对日期 2026-09-01

**历史形式**

无。

**Reproducible Builds**（`tc-224b9f45-d624-4543-bc81-f64d02f81aa0`）


**概念依据**

- [Reproducible Builds: Increasing the Integrity of Software Supply Chains · arXiv v1](https://arxiv.org/pdf/2104.06020v1) · [定位](https://arxiv.org/pdf/2104.06020v1) · PDF p. 2，Reproducible Builds，Definition 1 · 核对日期 2026-09-06

**定义**

**简体中文定义**

软件产品的构建过程具有可重现性，是指在指定其源码的具体版本及全部构建依赖后，无论在哪种环境执行，每次构建都产生逐比特相同的产物。

依据：
- [Reproducible Builds: Increasing the Integrity of Software Supply Chains · arXiv v1](https://arxiv.org/pdf/2104.06020v1) · [定位](https://arxiv.org/pdf/2104.06020v1) · PDF p. 2，Reproducible Builds，Definition 1 · 核对日期 2026-09-06

**术语形式**

**英文形式**

- Reproducible Builds（`tm-849f1000-68b5-456c-954f-1b05750ebea3`；preferredTerm-admn-sts）
  - 依据：[Reproducible Builds: Increasing the Integrity of Software Supply Chains · arXiv v1](https://arxiv.org/pdf/2104.06020v1) · [定位](https://arxiv.org/pdf/2104.06020v1) · PDF p. 2，Reproducible Builds，Definition 1 · 核对日期 2026-09-06

**历史形式**

无。

## 写作与设计方法

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| 相关 | relevant | zh-Hans：文档包含读者为当前目的所需要的信息，并尽量少包含读者不需要的信息。 | — | tc-2cdb43fb-ad5e-4aec-ad71-56eb596b78eb |
| 可找到 | findable | zh-Hans：文档的结构和设计使读者能够找到自己需要的信息。 | — | tc-2938e52c-9172-4bc1-b3ea-a1c0476fe909 |
| 可理解 | understandable | zh-Hans：读者能够理解自己找到的信息。 | — | tc-973e68b6-1e0f-47a9-9ab7-0660d591969c |
| 可使用 | usable | zh-Hans：读者能够使用获得的信息。 | — | tc-9985f5e9-89cc-4fe1-849f-c2be99f97727 |
| 第一原理 | first principle | zh-Hans：在一门学科的证明中作为直接起点，不由更先命题证明的基本命题。 | — | tc-327c7d8a-74ac-42b2-9022-da47959a339e |
| 设计理由 | design rationale | zh-Hans：对设计系统或人工制品时所作选择及其背后推理的明确表达。 | — | tc-fd033cdd-75b1-455c-9b39-431d1b9f3747 |
| 被替代 | superseded | zh-Hans：决定记录被后续决定取代，但仍保留供查阅的状态。 | — | tc-a64c6780-fab4-4422-86ce-d8590dae3e52 |
| 内容模型 | content model | zh-Hans：规定结构化内容允许包含哪些组成部分，以及其组合、次序与重复方式的约束。 | — | tc-c484ee2c-a757-4f0f-9113-d2eda506c1bf |
| 知识组织 | knowledge organization | zh-Hans：围绕知识及其文献表示进行描述、标引、分类和组织的活动，以及支持这些活动的系统。 | — | tc-c99988e5-3f77-492b-bd6e-aeca8e11ff6f |
| 公众人物 | public figure | zh-Hans：在美国诽谤法语境中，因广泛名望或影响而具有一般公众人物地位，或因在某项公共争议中承担突出角色而仅就相关问题具有公众人物地位的人。 | — | tc-2cc8a5dc-aa02-43fd-9cd7-f7fd9f3c3382 |
| 个体 | individual | zh-Hans：在所描述领域中作为单个对象识别的对象，而不是概括一类对象的类。 | — | tc-9e03d16f-3787-4d16-9316-c46a686e0c03 |
| 划分 | partition | zh-Hans：一个集合的非空子集所组成的集合，各子集两两不相交，且并集等于原集合。 | — | tc-ceeab73a-dc10-4197-8bc0-8074a1eaba15 |

**相关**（`tc-2cdb43fb-ad5e-4aec-ad71-56eb596b78eb`）


**概念依据**

- [Plain language — Part 1: Governing principles and guidelines · 2023](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf) · ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 1；PDF pp. 9–11（印刷 pp. 3–5），§5.1.1–§5.1.6 · 核对日期 2026-09-06

**定义**

**简体中文定义**

文档包含读者为当前目的所需要的信息，并尽量少包含读者不需要的信息。

依据：
- [Plain language — Part 1: Governing principles and guidelines · 2023](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf) · ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 1；PDF pp. 9–11（印刷 pp. 3–5），§5.1.1–§5.1.6 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 相关（`tm-e1b3aa8a-c184-4ee7-a2bd-0f9cacb93187`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：相关强调内容符合读者当前信息需要；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- relevant（`tm-76611867-5bf8-4ba7-91b8-98328562a9aa`；preferredTerm-admn-sts）
  - 依据：[Plain language — Part 1: Governing principles and guidelines · 2023](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf) · ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 1；PDF pp. 9–11（印刷 pp. 3–5），§5.1.1–§5.1.6 · 核对日期 2026-09-06

**历史形式**

无。

**可找到**（`tc-2938e52c-9172-4bc1-b3ea-a1c0476fe909`）


**概念依据**

- [Plain language — Part 1: Governing principles and guidelines · 2023](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf) · ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 2；PDF p. 11（印刷 p. 5），§5.2.1–§5.2.3 · 核对日期 2026-09-06

**定义**

**简体中文定义**

文档的结构和设计使读者能够找到自己需要的信息。

依据：
- [Plain language — Part 1: Governing principles and guidelines · 2023](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf) · ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 2；PDF p. 11（印刷 p. 5），§5.2.1–§5.2.3 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 可找到（`tm-290bf765-6c24-4495-9a46-ebe1e7fe462a`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：可找到强调结构和设计支持定位信息；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- findable（`tm-aeb4615f-2f52-4dfd-a5e9-380a05c4e374`；preferredTerm-admn-sts）
  - 依据：[Plain language — Part 1: Governing principles and guidelines · 2023](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf) · ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 2；PDF p. 11（印刷 p. 5），§5.2.1–§5.2.3 · 核对日期 2026-09-06

**历史形式**

无。

**可理解**（`tc-973e68b6-1e0f-47a9-9ab7-0660d591969c`）


**概念依据**

- [Plain language — Part 1: Governing principles and guidelines · 2023](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf) · ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 3 · 核对日期 2026-09-06

**定义**

**简体中文定义**

读者能够理解自己找到的信息。

依据：
- [Plain language — Part 1: Governing principles and guidelines · 2023](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf) · ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 3 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 可理解（`tm-8da4cfa3-6bcd-4bbb-84e8-e36f3db0e01f`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：可理解强调读者对所找到信息的理解；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- understandable（`tm-71fd160f-eff7-42b2-898f-4c56dd08230d`；preferredTerm-admn-sts）
  - 依据：[Plain language — Part 1: Governing principles and guidelines · 2023](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf) · ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 3 · 核对日期 2026-09-06

**历史形式**

无。

**可使用**（`tc-9985f5e9-89cc-4fe1-849f-c2be99f97727`）


**概念依据**

- [Plain language — Part 1: Governing principles and guidelines · 2023](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf) · ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 4 及原则关系段 · 核对日期 2026-09-06

**定义**

**简体中文定义**

读者能够使用获得的信息。

依据：
- [Plain language — Part 1: Governing principles and guidelines · 2023](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf) · ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 4 及原则关系段 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 可使用（`tm-d3c0e7d5-190f-4e6a-9b6b-4b395590ed75`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：可使用强调信息支持读者完成预期任务；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- usable（`tm-73551363-0781-49db-b2fb-ae329c7ed476`；preferredTerm-admn-sts）
  - 依据：[Plain language — Part 1: Governing principles and guidelines · 2023](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf) · ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 4 及原则关系段 · 核对日期 2026-09-06

**历史形式**

无。

**第一原理**（`tc-327c7d8a-74ac-42b2-9022-da47959a339e`）


**概念依据**

- [Posterior Analytics](https://classics.mit.edu/Aristotle/posterior.1.i.html) · BookI Part2 immediate proposition；Part3 · 核对日期 2026-09-06
- [Metaphysics](https://classics.mit.edu/Aristotle/metaphysics.1.i.html) · BookI Part2/7 first principles · 核对日期 2026-09-06

**定义**

**简体中文定义**

在一门学科的证明中作为直接起点，不由更先命题证明的基本命题。

依据：
- [Posterior Analytics](https://classics.mit.edu/Aristotle/posterior.1.i.html) · BookI Part2 immediate proposition；Part3 · 核对日期 2026-09-06
- [Metaphysics](https://classics.mit.edu/Aristotle/metaphysics.1.i.html) · BookI Part2/7 first principles · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 第一原理（`tm-2ef489fa-422e-4a9c-94d8-4a32b003561e`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：第一原理保留证明起点概念，不扩大成一般拆解技巧，也不意味着不可质疑或不需认识依据。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- first principle（`tm-04fb5e11-67df-42c5-a27f-634508227d21`；preferredTerm-admn-sts）
  - 依据：[Posterior Analytics](https://classics.mit.edu/Aristotle/posterior.1.i.html) · BookI Part2 immediate proposition；Part3 · 核对日期 2026-09-06
  - 依据：[Metaphysics](https://classics.mit.edu/Aristotle/metaphysics.1.i.html) · BookI Part2/7 first principles · 核对日期 2026-09-06

**历史形式**

无。

**设计理由**（`tc-fd033cdd-75b1-455c-9b39-431d1b9f3747`）


**概念依据**

- [Design Argumentation as Design Rationale · KMI-95-14](https://kmi.open.ac.uk/publications/techreport/kmi-95-14) · KMI-95-14摘要首句 · 核对日期 2026-09-06

**定义**

**简体中文定义**

对设计系统或人工制品时所作选择及其背后推理的明确表达。

依据：
- [Design Argumentation as Design Rationale · KMI-95-14](https://kmi.open.ac.uk/publications/techreport/kmi-95-14) · KMI-95-14摘要首句 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 设计理由（`tm-aba00e29-f04b-459b-9fff-08488ae115a2`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：设计理由是理由与推理的表示，不限软件架构ADR或IBIS文档格式。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- design rationale（`tm-f5b9ffce-b288-452a-b7db-9310c5d4430d`；preferredTerm-admn-sts）
  - 依据：[Design Argumentation as Design Rationale · KMI-95-14](https://kmi.open.ac.uk/publications/techreport/kmi-95-14) · KMI-95-14摘要首句 · 核对日期 2026-09-06

**历史形式**

无。

**被替代**（`tc-a64c6780-fab4-4422-86ce-d8590dae3e52`）


**概念依据**

- [Documenting Architecture Decisions · 2011-11-15](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) · 正文旧决定保留并mark superseded段 · 核对日期 2026-09-06

**定义**

**简体中文定义**

决定记录被后续决定取代，但仍保留供查阅的状态。

依据：
- [Documenting Architecture Decisions · 2011-11-15](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) · 正文旧决定保留并mark superseded段 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 被替代（`tm-1869ad52-b5a3-4232-bf4f-2af24209e450`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：被替代保留ADR语境；不把来源状态扩展为任意项目对象deprecated。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- superseded（`tm-69349502-3d1e-4e46-b82f-851ba3f2360b`；preferredTerm-admn-sts）
  - 依据：[Documenting Architecture Decisions · 2011-11-15](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) · 正文旧决定保留并mark superseded段 · 核对日期 2026-09-06

**历史形式**

无。

**内容模型**（`tc-c484ee2c-a757-4f0f-9113-d2eda506c1bf`）


**概念依据**

- [Extensible Markup Language (XML) 1.0 (Fifth Edition) · 2008-11-26](https://www.w3.org/TR/REC-xml/) · §3.2.1 Element Content，允许类型/次序及重复规则 · 核对日期 2026-09-06
- [DITA 1.3 / Darwin Information Typing Architecture 1.3 · 1.3](http://docs.oasis-open.org/dita/dita/v1.3/os/part1-base/dita-v1.3-os-part1-base.html) · DITA1.3 §2.6.3.1 Content models defined as entities · 核对日期 2026-09-06

**定义**

**简体中文定义**

规定结构化内容允许包含哪些组成部分，以及其组合、次序与重复方式的约束。

依据：
- [Extensible Markup Language (XML) 1.0 (Fifth Edition) · 2008-11-26](https://www.w3.org/TR/REC-xml/) · §3.2.1 Element Content，允许类型/次序及重复规则 · 核对日期 2026-09-06
- [DITA 1.3 / Darwin Information Typing Architecture 1.3 · 1.3](http://docs.oasis-open.org/dita/dita/v1.3/os/part1-base/dita-v1.3-os-part1-base.html) · DITA1.3 §2.6.3.1 Content models defined as entities · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 内容模型（`tm-94f6f1e0-2b90-4a19-852d-0b812a36abf6`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：内容模型保留原SGML/DITA结构化内容语境；不换成CMS业务实体模型，原SGML来源只保留历史。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- content model（`tm-c89a4642-bfe3-4c06-8fcf-ee648ef2dada`；preferredTerm-admn-sts）
  - 依据：[Extensible Markup Language (XML) 1.0 (Fifth Edition) · 2008-11-26](https://www.w3.org/TR/REC-xml/) · §3.2.1 Element Content，允许类型/次序及重复规则 · 核对日期 2026-09-06
  - 依据：[DITA 1.3 / Darwin Information Typing Architecture 1.3 · 1.3](http://docs.oasis-open.org/dita/dita/v1.3/os/part1-base/dita-v1.3-os-part1-base.html) · DITA1.3 §2.6.3.1 Content models defined as entities · 核对日期 2026-09-06

**历史形式**

无。

**知识组织**（`tc-c99988e5-3f77-492b-bd6e-aeca8e11ff6f`）


**概念依据**

- [Knowledge organization (KO)](https://www.isko.org/cyclo/knowledge_organization) · §1 Introduction末两段，KOP与KOS · 核对日期 2026-09-06

**定义**

**简体中文定义**

围绕知识及其文献表示进行描述、标引、分类和组织的活动，以及支持这些活动的系统。

依据：
- [Knowledge organization (KO)](https://www.isko.org/cyclo/knowledge_organization) · §1 Introduction末两段，KOP与KOS · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 知识组织（`tm-2a5b2ad3-d169-488b-b6ad-2498b42dc07e`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：知识组织包括过程和系统两方面；KOS只指系统，不自动与整个KO名称同义。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- knowledge organization（`tm-8d5071d7-c12a-4c9c-bca1-e8c34f309cb5`；preferredTerm-admn-sts）
  - 依据：[Knowledge organization (KO)](https://www.isko.org/cyclo/knowledge_organization) · §1 Introduction末两段，KOP与KOS · 核对日期 2026-09-06

**历史形式**

无。

**公众人物**（`tc-2cc8a5dc-aa02-43fd-9cd7-f7fd9f3c3382`）


**概念依据**

- [Gertz v. Robert Welch, Inc., 418 U.S. 323 · 1974-06-25](https://www.law.cornell.edu/supremecourt/text/418/323) · 多数意见345、351–352页；一般声名/特定公共争议与发表作品反例 · 核对日期 2026-09-06

**定义**

**简体中文定义**

在美国诽谤法语境中，因广泛名望或影响而具有一般公众人物地位，或因在某项公共争议中承担突出角色而仅就相关问题具有公众人物地位的人。

依据：
- [Gertz v. Robert Welch, Inc., 418 U.S. 323 · 1974-06-25](https://www.law.cornell.edu/supremecourt/text/418/323) · 多数意见345、351–352页；一般声名/特定公共争议与发表作品反例 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 公众人物（`tm-cfe309d6-ff92-46fb-95ad-f8f58a4c3d87`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：公众人物是此美国诽谤法语境的既有中文名；作者/维护者身份不自动达到法律门槛。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- public figure（`tm-6f053261-8f43-4149-b2f6-3bf771797ecf`；preferredTerm-admn-sts）
  - 依据：[Gertz v. Robert Welch, Inc., 418 U.S. 323 · 1974-06-25](https://www.law.cornell.edu/supremecourt/text/418/323) · 多数意见345、351–352页；一般声名/特定公共争议与发表作品反例 · 核对日期 2026-09-06

**历史形式**

无。

**个体**（`tc-9e03d16f-3787-4d16-9316-c46a686e0c03`）


**概念依据**

- [OWL 2 Web Ontology Language Primer (Second Edition) · 2012-12-11](https://www.w3.org/TR/owl2-primer/) · §3/4.1/4.7 对象、类与不同名称不保证不同个体 · 核对日期 2026-09-06

**定义**

**简体中文定义**

在所描述领域中作为单个对象识别的对象，而不是概括一类对象的类。

依据：
- [OWL 2 Web Ontology Language Primer (Second Edition) · 2012-12-11](https://www.w3.org/TR/owl2-primer/) · §3/4.1/4.7 对象、类与不同名称不保证不同个体 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 个体（`tm-5a9478c7-39d8-4cc8-b1b2-acfa722afe7a`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：个体不限自然人；名称规范表收录是项目用法，不作为一般定义必要条件。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- individual（`tm-bb67e2c7-8ddc-4400-8ef4-eebad39d015a`；preferredTerm-admn-sts）
  - 依据：[OWL 2 Web Ontology Language Primer (Second Edition) · 2012-12-11](https://www.w3.org/TR/owl2-primer/) · §3/4.1/4.7 对象、类与不同名称不保证不同个体 · 核对日期 2026-09-06

**历史形式**

无。

**划分**（`tc-ceeab73a-dc10-4197-8bc0-8074a1eaba15`）


**概念依据**

- [CS 3110 Recitation 14 · 2012 Fall](https://www.cs.cornell.edu/courses/cs3110/2012fa/recitations/rec14.html) · Recitation14首段 · 核对日期 2026-09-06

**定义**

**简体中文定义**

一个集合的非空子集所组成的集合，各子集两两不相交，且并集等于原集合。

依据：
- [CS 3110 Recitation 14 · 2012 Fall](https://www.cs.cornell.edu/courses/cs3110/2012fa/recitations/rec14.html) · Recitation14首段 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 划分（`tm-c8657af5-0a96-4208-a590-068abdaa6ecf`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：划分保留集合论的非空、互斥和覆盖条件，不是磁盘分区或任意分类操作。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- partition（`tm-d2a7e27b-39b8-46db-b043-5b4909291305`；preferredTerm-admn-sts）
  - 依据：[CS 3110 Recitation 14 · 2012 Fall](https://www.cs.cornell.edu/courses/cs3110/2012fa/recitations/rec14.html) · Recitation14首段 · 核对日期 2026-09-06

**历史形式**

无。

## 笔记的类型

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| 体裁 | genre | zh-Hans：按内容性质及其新闻或知识表达特征区分的文本类别。 | — | tc-9e701a8f-b994-4a0d-8eab-3ea769ae1b6c |
| 排障 | troubleshooting | zh-Hans：用于记录问题情形或症状、可能原因及纠正办法的DITA主题类型。 | — | tc-1f71845d-b74c-4a84-84c8-3976145bd5f6 |
| 闪念笔记 | fleeting note | zh-Hans：在忙于其他事情时快速记下的当下想法提醒；它通常不是完整表达，需要尽快处理，值得保留的内容再改写为长期笔记。 | — | tc-e5c11065-dc49-4ac8-b297-aadb2edd1196 |
| 文献笔记 | literature note | zh-Hans：针对读过的材料所作的笔记，保存在与永久笔记分开的地方；不能只复制摘录，应回看并思考它怎样服务于正在发展的想法，通常需要改写。 | — | tc-80512a5e-8cde-40f7-8abe-896d973ee851 |
| 永久笔记 | permanent note | zh-Hans：经过处理、值得长期保留、以他人也能理解的方式写成，并在卡片盒中继续连接和发展的笔记。 | — | tc-5a5c6042-effa-4ebe-8a85-4560468e3adc |
| 隐性知识 | tacit knowledge | zh-Hans：高度个人化、植根于行动和经验，难以形式化和交流的知识。 | — | tc-2eb24dc0-1754-4f0b-a8c9-7239f29c1943 |
| 显性知识 | explicit knowledge | zh-Hans：能够用正式、系统的语言表达，并较容易处理、传递和存储的知识。 | — | tc-78034548-e62f-4b31-9921-5b22e661d1ff |
| 速查表 | cheat sheet | zh-Hans：为快速查阅而汇总信息的简明资料。 | — | tc-505c5536-a7dd-4100-999a-fe0472b66b1c |
| 札记簿 | commonplace book | zh-Hans：将阅读、听闻或个人观察所得的摘录和笔记按选定标题组织起来的笔记本。 | — | tc-066aff06-6bef-4b2d-9870-f6ff7551db7f |
| 认知过程维度 | cognitive process dimension | zh-Hans：修订版教育目标分类中区分记忆、理解、应用、分析、评价和创造的认知过程维度。 | — | tc-b49a8de0-d20e-42da-b7f0-f8d09ce44dc2 |
| 帕累托原则 | Pareto principle | zh-Hans：少数因素对总体效果起主要作用、其余多数因素作用较小的现象；本条不规定固定的 80/20 比例。 | — | tc-9706ac56-d951-4eb6-9f27-cf7baa983a81 |

**体裁**（`tc-9e701a8f-b994-4a0d-8eab-3ea769ae1b6c`）


**概念依据**

- [IPTC NewsCodes 体裁词表 / IPTC NewsCodes Genre](https://cv.iptc.org/newscodes/genre/) · NewsCodes Guidelines §1.1 Descriptive NewsCodes，Genre整体说明 · 核对日期 2026-09-06

**定义**

**简体中文定义**

按内容性质及其新闻或知识表达特征区分的文本类别。

依据：
- [IPTC NewsCodes 体裁词表 / IPTC NewsCodes Genre](https://cv.iptc.org/newscodes/genre/) · NewsCodes Guidelines §1.1 Descriptive NewsCodes，Genre整体说明 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 体裁（`tm-af21a492-0a41-4c6a-aab3-9b86dd6d740d`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：体裁对应IPTC总体性质说明，本库genre选作者立场子集；Diátaxis需求属于另一组织依据，不作genre定义或英文同义证据。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- genre（`tm-9fe850d2-b2dc-47ac-a0c7-a7e2a4967744`；preferredTerm-admn-sts）
  - 依据：[IPTC NewsCodes 体裁词表 / IPTC NewsCodes Genre](https://cv.iptc.org/newscodes/genre/) · NewsCodes Guidelines §1.1 Descriptive NewsCodes，Genre整体说明 · 核对日期 2026-09-06

**历史形式**

无。

**排障**（`tc-1f71845d-b74c-4a84-84c8-3976145bd5f6`）


**概念依据**

- [DITA 1.3 / Darwin Information Typing Architecture 1.3 · 1.3](http://docs.oasis-open.org/dita/dita/v1.3/os/part1-base/dita-v1.3-os-part1-base.html) · DITA1.3 §2.7.1.6 dita-troubleshooting-topic.html首段及信息类型结构 · 核对日期 2026-09-06

**定义**

**简体中文定义**

用于记录问题情形或症状、可能原因及纠正办法的DITA主题类型。

依据：
- [DITA 1.3 / Darwin Information Typing Architecture 1.3 · 1.3](http://docs.oasis-open.org/dita/dita/v1.3/os/part1-base/dita-v1.3-os-part1-base.html) · DITA1.3 §2.7.1.6 dita-troubleshooting-topic.html首段及信息类型结构 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 排障（`tm-ec8494d2-3dc5-4059-88c7-c6b8cb0e7770`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：排障在原行指承载纠正信息的主题类型，不偷偷换成一般排障活动；原因与办法可未知。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- troubleshooting（`tm-948869da-f697-4671-b64a-d0fcc988e012`；preferredTerm-admn-sts）
  - 依据：[DITA 1.3 / Darwin Information Typing Architecture 1.3 · 1.3](http://docs.oasis-open.org/dita/dita/v1.3/os/part1-base/dita-v1.3-os-part1-base.html) · DITA1.3 §2.7.1.6 dita-troubleshooting-topic.html首段及信息类型结构 · 核对日期 2026-09-06

**历史形式**

无。

**闪念笔记**（`tc-e5c11065-dc49-4ac8-b297-aadb2edd1196`）


**概念依据**

- [Zettelkasten "Super" Notes: with Dr Sönke Ahrens](https://examstudyexpert.com/zettelkasten/) · [定位](https://examstudyexpert.com/zettelkasten/) · ; captured L91-L95 · 核对日期 2026-09-06

**定义**

**简体中文定义**

在忙于其他事情时快速记下的当下想法提醒；它通常不是完整表达，需要尽快处理，值得保留的内容再改写为长期笔记。

依据：
- [Zettelkasten "Super" Notes: with Dr Sönke Ahrens](https://examstudyexpert.com/zettelkasten/) · [定位](https://examstudyexpert.com/zettelkasten/) · ; captured L91-L95 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 闪念笔记（`tm-01f3402c-0616-4c48-8bd4-e959046120d2`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：闪念笔记强调临时想法提醒与后续处理；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- fleeting note（`tm-021f20e2-f065-4e09-ba80-2542f94f0c17`；preferredTerm-admn-sts）
  - 依据：[Zettelkasten "Super" Notes: with Dr Sönke Ahrens](https://examstudyexpert.com/zettelkasten/) · [定位](https://examstudyexpert.com/zettelkasten/) · ; captured L91-L95 · 核对日期 2026-09-06

**历史形式**

无。

**文献笔记**（`tc-80512a5e-8cde-40f7-8abe-896d973ee851`）


**概念依据**

- [Zettelkasten "Super" Notes: with Dr Sönke Ahrens](https://examstudyexpert.com/zettelkasten/) · [定位](https://examstudyexpert.com/zettelkasten/) · ; captured L103-L106 · 核对日期 2026-09-06

**定义**

**简体中文定义**

针对读过的材料所作的笔记，保存在与永久笔记分开的地方；不能只复制摘录，应回看并思考它怎样服务于正在发展的想法，通常需要改写。

依据：
- [Zettelkasten "Super" Notes: with Dr Sönke Ahrens](https://examstudyexpert.com/zettelkasten/) · [定位](https://examstudyexpert.com/zettelkasten/) · ; captured L103-L106 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 文献笔记（`tm-494f248e-2538-4d16-ac58-ff1d43102dc3`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：文献笔记强调针对阅读材料而作，不等同复制摘录；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- literature note（`tm-34df14ea-ab98-4b85-a833-9d7d06773428`；preferredTerm-admn-sts）
  - 依据：[Zettelkasten "Super" Notes: with Dr Sönke Ahrens](https://examstudyexpert.com/zettelkasten/) · [定位](https://examstudyexpert.com/zettelkasten/) · ; captured L103-L106 · 核对日期 2026-09-06

**历史形式**

无。

**永久笔记**（`tc-5a5c6042-effa-4ebe-8a85-4560468e3adc`）


**概念依据**

- [Zettelkasten "Super" Notes: with Dr Sönke Ahrens](https://examstudyexpert.com/zettelkasten/) · [定位](https://examstudyexpert.com/zettelkasten/) · ; captured L95-L102；https://examstudyexpert.com/zettelkasten/ ; captured L113-L114 · 核对日期 2026-09-06

**定义**

**简体中文定义**

经过处理、值得长期保留、以他人也能理解的方式写成，并在卡片盒中继续连接和发展的笔记。

依据：
- [Zettelkasten "Super" Notes: with Dr Sönke Ahrens](https://examstudyexpert.com/zettelkasten/) · [定位](https://examstudyexpert.com/zettelkasten/) · ; captured L95-L102；https://examstudyexpert.com/zettelkasten/ ; captured L113-L114 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 永久笔记（`tm-3d623e69-aa38-46cc-874b-506af3f67671`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：永久笔记强调经过处理并长期连接发展的笔记；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- permanent note（`tm-fdbe3135-7fb4-423f-bcbc-8376810130d5`；preferredTerm-admn-sts）
  - 依据：[Zettelkasten "Super" Notes: with Dr Sönke Ahrens](https://examstudyexpert.com/zettelkasten/) · [定位](https://examstudyexpert.com/zettelkasten/) · ; captured L95-L102；https://examstudyexpert.com/zettelkasten/ ; captured L113-L114 · 核对日期 2026-09-06

**历史形式**

无。

**隐性知识**（`tc-2eb24dc0-1754-4f0b-a8c9-7239f29c1943`）


**概念依据**

- [Managing Industrial Knowledge, Chapter 1](https://api.pageplace.de/preview/DT0400.9781847876621_A23446119/preview-9781847876621_A23446119.pdf) · 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式 · 核对日期 2026-09-06

**定义**

**简体中文定义**

高度个人化、植根于行动和经验，难以形式化和交流的知识。

依据：
- [Managing Industrial Knowledge, Chapter 1](https://api.pageplace.de/preview/DT0400.9781847876621_A23446119/preview-9781847876621_A23446119.pdf) · 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 隐性知识（`tm-4a653060-87cf-44bb-bbad-9ef409ef92d1`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：隐性知识是知识管理中对应既有英文概念的行业表达；替代已读作者章节不伪称Nonaka1991原文已读。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- tacit knowledge（`tm-5d81868a-1cfc-4d4d-aca9-07b816ae464b`；preferredTerm-admn-sts）
  - 依据：[Managing Industrial Knowledge, Chapter 1](https://api.pageplace.de/preview/DT0400.9781847876621_A23446119/preview-9781847876621_A23446119.pdf) · 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式 · 核对日期 2026-09-06

**历史形式**

无。

**显性知识**（`tc-78034548-e62f-4b31-9921-5b22e661d1ff`）


**概念依据**

- [Managing Industrial Knowledge, Chapter 1](https://api.pageplace.de/preview/DT0400.9781847876621_A23446119/preview-9781847876621_A23446119.pdf) · 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式 · 核对日期 2026-09-06

**定义**

**简体中文定义**

能够用正式、系统的语言表达，并较容易处理、传递和存储的知识。

依据：
- [Managing Industrial Knowledge, Chapter 1](https://api.pageplace.de/preview/DT0400.9781847876621_A23446119/preview-9781847876621_A23446119.pdf) · 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 显性知识（`tm-d140d129-94ad-47e1-9181-60fb0d66c2cb`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：显性知识是知识管理中对应既有英文概念的行业表达；替代已读作者章节不伪称Nonaka1991原文已读。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- explicit knowledge（`tm-91d7f224-0be5-401a-8c0e-4a0abfe252f5`；preferredTerm-admn-sts）
  - 依据：[Managing Industrial Knowledge, Chapter 1](https://api.pageplace.de/preview/DT0400.9781847876621_A23446119/preview-9781847876621_A23446119.pdf) · 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式 · 核对日期 2026-09-06

**历史形式**

无。

**速查表**（`tc-505c5536-a7dd-4100-999a-fe0472b66b1c`）


**概念依据**

- [The American Heritage Dictionary of the English Language, Fifth Edition · Fifth Edition (2022)](https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0) · [定位](https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0) · Fifth Edition ©2022，cheat sheet义项2 · 核对日期 2026-09-06

**定义**

**简体中文定义**

为快速查阅而汇总信息的简明资料。

依据：
- [The American Heritage Dictionary of the English Language, Fifth Edition · Fifth Edition (2022)](https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0) · [定位](https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0) · Fifth Edition ©2022，cheat sheet义项2 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 速查表（`tm-2923a9eb-c720-4de1-8491-c7e6665243a6`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：速查表是技术文档中cheat sheet的惯用表达；不把任何笔记集或作弊材料纳入此概念。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- cheat sheet（`tm-98076d19-5e2f-419d-82a4-353f20652a57`；preferredTerm-admn-sts）
  - 依据：[The American Heritage Dictionary of the English Language, Fifth Edition · Fifth Edition (2022)](https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0) · [定位](https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0) · Fifth Edition ©2022，cheat sheet义项2 · 核对日期 2026-09-06

**历史形式**

无。

**札记簿**（`tc-066aff06-6bef-4b2d-9870-f6ff7551db7f`）


**概念依据**

- [The Fragment and the Whole](https://takenote.library.harvard.edu/fragment-and-whole) · Tiffany Stern正文6–8段，L133–138 · 核对日期 2026-09-06

**定义**

**简体中文定义**

将阅读、听闻或个人观察所得的摘录和笔记按选定标题组织起来的笔记本。

依据：
- [The Fragment and the Whole](https://takenote.library.harvard.edu/fragment-and-whole) · Tiffany Stern正文6–8段，L133–138 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 札记簿（`tm-e7af64e3-ac9e-4fbd-baaa-fecf3782cc5a`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：札记簿为原中文登记，在此按主题标题组织摘录和观察的明确范围沿用；没有更强中文证据，不为换取文路径强制改为摘录簿。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- commonplace book（`tm-a922627b-3c76-4142-ad1b-b0b38c1bab3c`；preferredTerm-admn-sts）
  - 依据：[The Fragment and the Whole](https://takenote.library.harvard.edu/fragment-and-whole) · Tiffany Stern正文6–8段，L133–138 · 核对日期 2026-09-06

**历史形式**

无。

**认知过程维度**（`tc-b49a8de0-d20e-42da-b7f0-f8d09ce44dc2`）


**概念依据**

- [A Revision of Bloom’s Taxonomy: An Overview · 2002](https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf) · PDFindex2–5/印刷pp.214–217，Cognitive Process dimension及Tables2–3 · 核对日期 2026-09-06

**定义**

**简体中文定义**

修订版教育目标分类中区分记忆、理解、应用、分析、评价和创造的认知过程维度。

依据：
- [A Revision of Bloom’s Taxonomy: An Overview · 2002](https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf) · PDFindex2–5/印刷pp.214–217，Cognitive Process dimension及Tables2–3 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 认知过程维度（`tm-164f05a0-6ba3-447f-8cd9-2f1e9bf71bb3`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：认知过程维度准确对应原条目本意引用的修订版分类，不泛称理解深度；知识维度另有其义，不合并。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- cognitive process dimension（`tm-5877c07e-3cae-4a9e-9e48-d91b2ed09416`；preferredTerm-admn-sts）
  - 依据：[A Revision of Bloom’s Taxonomy: An Overview · 2002](https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf) · PDFindex2–5/印刷pp.214–217，Cognitive Process dimension及Tables2–3 · 核对日期 2026-09-06

**历史形式**

无。

**帕累托原则**（`tc-9706ac56-d951-4eb6-9f27-cf7baa983a81`）


**概念依据**

- [The Non-Pareto Principle; Mea Culpa · 1974](https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf) · [定位](https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf，PDF) · page index 0-2（印刷页 1-3），lines 1-21、158-168、194-209 · 核对日期 2026-09-06

**定义**

**简体中文定义**

少数因素对总体效果起主要作用、其余多数因素作用较小的现象；本条不规定固定的 80/20 比例。

依据：
- [The Non-Pareto Principle; Mea Culpa · 1974](https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf) · [定位](https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf，PDF) · page index 0-2（印刷页 1-3），lines 1-21、158-168、194-209 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 帕累托原则（`tm-13c4955e-8bec-4ddf-8a06-f8b061153bdf`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：帕累托原则是管理与质量领域对关键少数现象的行业表达，不把它改成项目选材义务；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- Pareto principle（`tm-75b287e7-ec70-47f6-a0be-610f6d79cc7e`；preferredTerm-admn-sts）
  - 依据：[The Non-Pareto Principle; Mea Culpa · 1974](https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf) · [定位](https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf，PDF) · page index 0-2（印刷页 1-3），lines 1-21、158-168、194-209 · 核对日期 2026-09-06

**历史形式**

无。

## 治理与维护

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| 治理 | governance of organizations | zh-Hans：组织为实现其既定目的而被指导、监督并被问责的以人为本系统。 | en：governance | tc-aadb304c-3ed0-4f60-94cf-c968953d838c |
| 治理政策 | governance policy | zh-Hans：治理主体正式表达的组织意向和方向。 | — | tc-24c3f7b9-c6a2-4e1c-91f2-b3ee234219c8 |
| 决策权 | decision rights | zh-Hans：被赋予对特定事项作出决定的权限，明确哪些主体能在何种范围与条件下作出哪些决定。 | — | tc-e61924e8-88b7-4c88-aaf2-5dad229a89ed |
| 监测 | monitoring | zh-Hans：持续、系统地收集或整理指定指标及其他资料，以掌握实施进展、结果和相关背景的过程。 | — | tc-09ff3cd6-f825-4e90-b401-4ef25c2cc084 |
| 评估 | evaluation | zh-Hans：对计划中、进行中或已完成的干预及其设计、实施和结果进行系统、客观评价的过程。 | — | tc-f881797d-c9ff-4f57-9523-b6a1c01c8b2c |
| 审计追踪 | audit trail | zh-Hans：在安全相关事务中，按时间顺序记录活动，使特定操作、过程或事件从开始到结果的活动序列能够被重建和检查的记录。 | — | tc-36a1e0f4-8fe1-459a-9083-b31022a1bda1 |
| 治理评审 | governance review | zh-Hans：对治理安排及其有效性的评审。 | — | tc-9ebb317b-d01a-4852-a71f-463f595a50a4 |
| 审计 | audit | zh-Hans：对记录和活动进行独立审查与检查，以评价系统控制的充分性，并确认是否符合既定政策和操作程序。 | — | tc-ec453431-dede-440d-87aa-40b745fea33a |
| 处置 | disposition | zh-Hans：执行文件保管、销毁或移交决定的一系列过程；这些决定记录在处置授权或其他文件里。 | — | tc-362abd86-fd94-42b4-8f6e-aaca8aa3660b |
| 断言 | assertion | zh-Hans：本库中由人作出判断、而不是直接抄自来源的字段值。 | — | tc-9db2bd8b-938e-4752-865f-bec2da9c4083 |
| 指标 | indicator | zh-Hans：与干预及其结果或发生背景有关的定量或定性因素、变量。 | — | tc-0aa7aa33-d7af-4c82-ad56-6efe59c4138c |
| 阈值 | threshold | zh-Hans：用于判定指标何时触发复核或提案的界值。 | — | tc-549c1bed-5db4-4073-aaab-bf23c9be47ac |
| 批准 | approve | zh-Hans：完成接受程序并允许候选词作为词纳入受控词表的操作。 | — | tc-ab1c42d3-59d8-49db-9aa9-eebc09a98d6c |

**治理**（`tc-aadb304c-3ed0-4f60-94cf-c968953d838c`）


**概念依据**

- [Governance of organizations — Guidance · 2021](https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf) · §3.1.1，PDFp.9/印刷p.1 · 核对日期 2026-09-06

**定义**

**简体中文定义**

组织为实现其既定目的而被指导、监督并被问责的以人为本系统。

依据：
- [Governance of organizations — Guidance · 2021](https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf) · §3.1.1，PDFp.9/印刷p.1 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 治理（`tm-fbdc1cb5-9e94-4eaf-ba39-857028742488`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：治理保留组织层指导/监督/问责机制，不把对管理的管理概述当完整定义。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- governance of organizations（`tm-06b33584-8d3e-4053-ba8d-fb7658308c79`；preferredTerm-admn-sts）
  - 依据：[Governance of organizations — Guidance · 2021](https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf) · §3.1.1，PDFp.9/印刷p.1 · 核对日期 2026-09-06
- governance（`tm-37d5c3fd-96dc-4d05-9676-3e7955c10f52`；admittedTerm-admn-sts）
  - 依据：[Governance of organizations — Guidance · 2021](https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf) · §3.1.1，PDFp.9/印刷p.1 · 核对日期 2026-09-06

**历史形式**

无。

**治理政策**（`tc-24c3f7b9-c6a2-4e1c-91f2-b3ee234219c8`）


**概念依据**

- [Governance of organizations — Guidance · 2021](https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf) · §3.2.9，PDFp.12/印刷p.4 · 核对日期 2026-09-06

**定义**

**简体中文定义**

治理主体正式表达的组织意向和方向。

依据：
- [Governance of organizations — Guidance · 2021](https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf) · §3.2.9，PDFp.12/印刷p.4 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 治理政策（`tm-54912589-583d-4140-88b2-e3d749a4c82f`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：治理政策补足原行治理主体限定，源词头不是一般policy；旧必须遵守的规则概述与方向定义有实质差异，需明确采纳。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- governance policy（`tm-acdb0fe2-bc90-41f2-90b0-079e9ea8d300`；preferredTerm-admn-sts）
  - 依据：[Governance of organizations — Guidance · 2021](https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf) · §3.2.9，PDFp.12/印刷p.4 · 核对日期 2026-09-06

**历史形式**

无。

**决策权**（`tc-e61924e8-88b7-4c88-aaf2-5dad229a89ed`）


**概念依据**

- [DND/CAF (Department of National Defence and the Canadian Armed Forces) Data Governance Framework · 2022-07-28](https://www.canada.ca/en/department-national-defence/corporate/reports-publications/data-governance.html) · 2022-07-28独立发表版；AppendixB data governance定义；§6.4.2 Chief Data Officer；§6.4.3.1 Data Governors · 核对日期 2026-09-06

**定义**

**简体中文定义**

被赋予对特定事项作出决定的权限，明确哪些主体能在何种范围与条件下作出哪些决定。

依据：
- [DND/CAF (Department of National Defence and the Canadian Armed Forces) Data Governance Framework · 2022-07-28](https://www.canada.ca/en/department-national-defence/corporate/reports-publications/data-governance.html) · 2022-07-28独立发表版；AppendixB data governance定义；§6.4.2 Chief Data Officer；§6.4.3.1 Data Governors · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 决策权（`tm-641a6f25-0b53-4451-9834-f0d3ea1ce134`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：决策权是作决定的权限，区别执行职责和结果问责；DND具体主体与事项提供概念对应，不冒称DAMA付费原典。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- decision rights（`tm-bf128cba-2cb0-4d40-ae87-74222efdc371`；preferredTerm-admn-sts）
  - 依据：[DND/CAF (Department of National Defence and the Canadian Armed Forces) Data Governance Framework · 2022-07-28](https://www.canada.ca/en/department-national-defence/corporate/reports-publications/data-governance.html) · 2022-07-28独立发表版；AppendixB data governance定义；§6.4.2 Chief Data Officer；§6.4.3.1 Data Governors · 核对日期 2026-09-06

**历史形式**

无。

**监测**（`tc-09ff3cd6-f825-4e90-b401-4ef25c2cc084`）


**概念依据**

- [Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese · Second edition, 2024, EN-ZH](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf) · Monitoring，PDFp.39，官方英文/中文对应 · 核对日期 2026-09-06

**定义**

**简体中文定义**

持续、系统地收集或整理指定指标及其他资料，以掌握实施进展、结果和相关背景的过程。

依据：
- [Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese · Second edition, 2024, EN-ZH](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf) · Monitoring，PDFp.39，官方英文/中文对应 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 监测（`tm-cde84c16-a9a4-47fc-8ac3-205a5d51f1cc`；preferredTerm-admn-sts）
  - 依据：[Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese · Second edition, 2024, EN-ZH](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf) · Monitoring，PDFp.39，官方英文/中文对应 · 核对日期 2026-09-06

**英文形式**

- monitoring（`tm-d7c39844-82c4-4c45-ba9c-9902f7b17f51`；preferredTerm-admn-sts）
  - 依据：[Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese · Second edition, 2024, EN-ZH](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf) · Monitoring，PDFp.39，官方英文/中文对应 · 核对日期 2026-09-06

**历史形式**

无。

**评估**（`tc-f881797d-c9ff-4f57-9523-b6a1c01c8b2c`）


**概念依据**

- [Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese · Second edition, 2024, EN-ZH](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf) · Evaluation，PDFp.29，官方英文/中文对应 · 核对日期 2026-09-06

**定义**

**简体中文定义**

对计划中、进行中或已完成的干预及其设计、实施和结果进行系统、客观评价的过程。

依据：
- [Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese · Second edition, 2024, EN-ZH](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf) · Evaluation，PDFp.29，官方英文/中文对应 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 评估（`tm-deb24ad5-acf0-4260-b259-4c50c19bca4c`；preferredTerm-admn-sts）
  - 依据：[Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese · Second edition, 2024, EN-ZH](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf) · Evaluation，PDFp.29，官方英文/中文对应 · 核对日期 2026-09-06

**英文形式**

- evaluation（`tm-6f0fed97-fada-4463-b83f-92193c721185`；preferredTerm-admn-sts）
  - 依据：[Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese · Second edition, 2024, EN-ZH](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf) · Evaluation，PDFp.29，官方英文/中文对应 · 核对日期 2026-09-06

**历史形式**

无。

**审计追踪**（`tc-36a1e0f4-8fe1-459a-9083-b31022a1bda1`）


**概念依据**

- [Security and Privacy Controls for Information Systems and Organizations · Revision 5 (updates 2020-12-10)](https://doi.org/10.6028/NIST.SP.800-53r5) · [定位](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf) · PDFp.422，AppendixA印刷p.395，audit trail · 核对日期 2026-09-06

**定义**

**简体中文定义**

在安全相关事务中，按时间顺序记录活动，使特定操作、过程或事件从开始到结果的活动序列能够被重建和检查的记录。

依据：
- [Security and Privacy Controls for Information Systems and Organizations · Revision 5 (updates 2020-12-10)](https://doi.org/10.6028/NIST.SP.800-53r5) · [定位](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf) · PDFp.422，AppendixA印刷p.395，audit trail · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 审计追踪（`tm-28bdb398-c344-489c-acef-a642f04ae4d2`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：审计追踪强调可重建的连续活动记录；谁/何时/何事可作为实现字段，不是全部定义。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- audit trail（`tm-f3f51b2d-e126-4c4a-a2d5-3e621f5070f5`；preferredTerm-admn-sts）
  - 依据：[Security and Privacy Controls for Information Systems and Organizations · Revision 5 (updates 2020-12-10)](https://doi.org/10.6028/NIST.SP.800-53r5) · [定位](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf) · PDFp.422，AppendixA印刷p.395，audit trail · 核对日期 2026-09-06

**历史形式**

无。

**治理评审**（`tc-9ebb317b-d01a-4852-a71f-463f595a50a4`）


**概念依据**

- [External governance reviews: guide for FE college corporations and designated institutions · 2026-08-11](https://www.gov.uk/guidance/external-governance-reviews-guide-for-fe-college-corporations-and-designated-institutions) · 2026-08-11更新发表版；Benefits of an external governance review；Scope of the review · 核对日期 2026-09-06

**定义**

**简体中文定义**

对治理安排及其有效性的评审。

依据：
- [External governance reviews: guide for FE college corporations and designated institutions · 2026-08-11](https://www.gov.uk/guidance/external-governance-reviews-guide-for-fe-college-corporations-and-designated-institutions) · 2026-08-11更新发表版；Benefits of an external governance review；Scope of the review · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 治理评审（`tm-f2c73c67-527c-442e-b5a7-882795cce1fc`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：治理评审有官方实际用法；本库年度复审政策/决策权/阈值为项目实施规则，不冒称ISO37000有独立词条。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- governance review（`tm-73cdf874-2e2b-4404-9eaf-6d0b71d41d0b`；preferredTerm-admn-sts）
  - 依据：[External governance reviews: guide for FE college corporations and designated institutions · 2026-08-11](https://www.gov.uk/guidance/external-governance-reviews-guide-for-fe-college-corporations-and-designated-institutions) · 2026-08-11更新发表版；Benefits of an external governance review；Scope of the review · 核对日期 2026-09-06

**历史形式**

无。

**审计**（`tc-ec453431-dede-440d-87aa-40b745fea33a`）


**概念依据**

- [Security and Privacy Controls for Information Systems and Organizations · Revision 5 (updates 2020-12-10)](https://doi.org/10.6028/NIST.SP.800-53r5) · [定位](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf) · PDFp.422，AppendixA印刷p.395，audit [CNSSI4009] · 核对日期 2026-09-06

**定义**

**简体中文定义**

对记录和活动进行独立审查与检查，以评价系统控制的充分性，并确认是否符合既定政策和操作程序。

依据：
- [Security and Privacy Controls for Information Systems and Organizations · Revision 5 (updates 2020-12-10)](https://doi.org/10.6028/NIST.SP.800-53r5) · [定位](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf) · PDFp.422，AppendixA印刷p.395，audit [CNSSI4009] · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 审计（`tm-37aeadd2-d0a1-4a1f-9845-d3ba5b6b2b45`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：审计与审计追踪不同，前者是评价过程，后者是记录；原符合规则概述补足证据和准则机制。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- audit（`tm-4794e766-7ce2-4386-8b90-0c7ea06ce27a`；preferredTerm-admn-sts）
  - 依据：[Security and Privacy Controls for Information Systems and Organizations · Revision 5 (updates 2020-12-10)](https://doi.org/10.6028/NIST.SP.800-53r5) · [定位](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf) · PDFp.422，AppendixA印刷p.395，audit [CNSSI4009] · 核对日期 2026-09-06

**历史形式**

无。

**处置**（`tc-362abd86-fd94-42b4-8f6e-aaca8aa3660b`）


**概念依据**

- [Information and documentation — Records management — Part 1: Concepts and principles · 2016](https://www.iso.org/standard/62542.html) · [定位](https://cdn.standards.iteh.ai/samples/62542/fe383f4fe10448d5b22ce628b1542ed6/ISO-15489-1-2016.pdf) · PDF p. 10（印刷 p. 2），§3.8 disposition · 核对日期 2026-09-06

**定义**

**简体中文定义**

执行文件保管、销毁或移交决定的一系列过程；这些决定记录在处置授权或其他文件里。

依据：
- [Information and documentation — Records management — Part 1: Concepts and principles · 2016](https://www.iso.org/standard/62542.html) · [定位](https://cdn.standards.iteh.ai/samples/62542/fe383f4fe10448d5b22ce628b1542ed6/ISO-15489-1-2016.pdf) · PDF p. 10（印刷 p. 2），§3.8 disposition · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 处置（`tm-47d9bbbe-00da-47da-bb2f-738a62d9bfce`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：处置是文件管理中对保管、销毁或移交决定的执行，不等于删除；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- disposition（`tm-55036694-aa11-45ee-9c54-73f98f209ffd`；preferredTerm-admn-sts）
  - 依据：[Information and documentation — Records management — Part 1: Concepts and principles · 2016](https://www.iso.org/standard/62542.html) · [定位](https://cdn.standards.iteh.ai/samples/62542/fe383f4fe10448d5b22ce628b1542ed6/ISO-15489-1-2016.pdf) · PDF p. 10（印刷 p. 2），§3.8 disposition · 核对日期 2026-09-06

**历史形式**

无。

**断言**（`tc-9db2bd8b-938e-4752-865f-bec2da9c4083`）


**概念依据**

- 项目决定依据，不是外部来源
- 采纳决定：decision-term-data-values
- 项目原文：`aae24737ff25cb8fbdb9ab9086b162dfb144ab81:docs/design/governance/maintenance.md` · 断言
- 采用理由：既有本库人工赋值用法；PROV-O只支持溯源，不冒充此定义来源

**定义**

**简体中文定义**

本库中由人作出判断、而不是直接抄自来源的字段值。

依据：
- 项目决定依据，不是外部来源
- 采纳决定：decision-term-data-values
- 项目原文：`aae24737ff25cb8fbdb9ab9086b162dfb144ab81:docs/design/governance/maintenance.md` · 断言
- 采用理由：既有本库人工赋值用法；PROV-O只支持溯源，不冒充此定义来源

**术语形式**

**简体中文形式**

- 断言（`tm-25528895-b7ab-4c59-b885-003d51cdf632`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：断言在本条是本库限定用法，保留原名称，不扩大到所有命题断言。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- assertion（`tm-657b1a85-79d5-44c1-b355-f37b4e7aff07`；preferredTerm-admn-sts）
  - 依据：项目决定依据，不是外部来源
  - 依据：采纳决定：decision-term-data-values
  - 依据：项目原文：`aae24737ff25cb8fbdb9ab9086b162dfb144ab81:docs/glossary.md` · 治理与维护，断言/assertion原登记
  - 依据：采用理由：仅此既有英文形式的项目准入追溯；不是模型英文兜底

**历史形式**

无。

**指标**（`tc-0aa7aa33-d7af-4c82-ad56-6efe59c4138c`）


**概念依据**

- [Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese · Second edition, 2024, EN-ZH](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf) · Indicator，PDFp.35，英文及官方中文指标紧邻 · 核对日期 2026-09-06

**定义**

**简体中文定义**

与干预及其结果或发生背景有关的定量或定性因素、变量。

依据：
- [Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese · Second edition, 2024, EN-ZH](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf) · Indicator，PDFp.35，英文及官方中文指标紧邻 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 指标（`tm-e81a6d8c-836b-4599-9dd9-6487df397223`；preferredTerm-admn-sts）
  - 依据：[Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese · Second edition, 2024, EN-ZH](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf) · Indicator，PDFp.35，英文及官方中文指标紧邻 · 核对日期 2026-09-06

**英文形式**

- indicator（`tm-e36008bf-48ec-4391-991d-e4dc25d973e5`；preferredTerm-admn-sts）
  - 依据：[Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese · Second edition, 2024, EN-ZH](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf) · Indicator，PDFp.35，英文及官方中文指标紧邻 · 核对日期 2026-09-06

**历史形式**

无。

**阈值**（`tc-549c1bed-5db4-4073-aaab-bf23c9be47ac`）


**概念依据**

- 项目决定依据，不是外部来源
- 采纳决定：decision-term-data-values
- 项目原文：`aae24737ff25cb8fbdb9ab9086b162dfb144ab81:docs/design/governance/maintenance.md` · 阈值；触发与动作
- 采用理由：现行阈值触发复核或提案，不自动批准修改

**定义**

**简体中文定义**

用于判定指标何时触发复核或提案的界值。

依据：
- 项目决定依据，不是外部来源
- 采纳决定：decision-term-data-values
- 项目原文：`aae24737ff25cb8fbdb9ab9086b162dfb144ab81:docs/design/governance/maintenance.md` · 阈值；触发与动作
- 采用理由：现行阈值触发复核或提案，不自动批准修改

**术语形式**

**简体中文形式**

- 阈值（`tm-f998c038-aacd-4c65-84df-c55042284579`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：阈值保留既有指标界值用法，明确到达阈值不授予自动修改权限。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- threshold（`tm-1facfe30-6843-4a4a-989d-a7d8338cf57f`；preferredTerm-admn-sts）
  - 依据：项目决定依据，不是外部来源
  - 依据：采纳决定：decision-term-data-values
  - 依据：项目原文：`aae24737ff25cb8fbdb9ab9086b162dfb144ab81:docs/glossary.md` · 治理与维护，阈值/threshold原登记
  - 依据：采用理由：仅此既有英文形式的项目登记追溯

**历史形式**

无。

**批准**（`tc-ab1c42d3-59d8-49db-9aa9-eebc09a98d6c`）


**概念依据**

- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.6 Candidate Terms，PDFp.105/印刷p.94；§11.4.5 · 核对日期 2026-09-06

**定义**

**简体中文定义**

完成接受程序并允许候选词作为词纳入受控词表的操作。

依据：
- [ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.6 Candidate Terms，PDFp.105/印刷p.94；§11.4.5 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 批准（`tm-0abd2dc1-3755-4169-9f04-dfa271540391`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：批准在此是源实际approved动词语境的接受动作，不伪造独立定义号，也不从标准授予本库机器审批权。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- approve（`tm-def01f3e-50b7-4676-a941-bdda43a2dc21`；preferredTerm-admn-sts）
  - 依据：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies · 2005 (R2010)](https://www.niso.org/publications/ansiniso-z3919-2005-r2010) · §11.1.6 Candidate Terms，PDFp.105/印刷p.94；§11.4.5 · 核对日期 2026-09-06

**历史形式**

无。

## 知识图谱

| 中文 | 英文 | 定义 | 允许形式 | 概念 ID |
|---|---|---|---|---|
| 三元组 | triple | zh-Hans：由主语、谓语和宾语组成的 RDF 数据单元。 | — | tc-589ad410-5fc7-4f1b-ba5a-fd06c366016f |
| 实体 | entity | zh-Hans：知识图谱中由节点表示的对象；节点及其标识用于表示和区分对象，不等于对象本身。 | — | tc-79c1fd4b-5f06-4d1e-a8d8-cd323c441939 |
| 关系 | relation | zh-Hans：知识图谱所表示的实体之间的语义联系。 | — | tc-4aa4867f-ea92-4a56-a56f-e8ffe45c1f91 |
| 边 | edge | zh-Hans：图中连接节点的结构；在知识图谱中可用来表示实体之间的关系。 | — | tc-95d07268-89f1-4c7f-86b0-98f60eeeef52 |
| 属性 | property | zh-Hans：在属性图中，与节点或边关联、以属性名和值构成的键值对表达的信息；值的具体形态由所用属性图模型规定。 | — | tc-605b0308-57af-486b-81ba-81e18b993b07 |
| — | schema | zh-Hans：知识图谱或数据模型的高层结构说明，可涉及类型、关系和约束。 | en：Schema | tc-daa1c79a-56f0-4d62-a360-ddaa9b332d0f |
| 推理 | reasoning | zh-Hans：依据已有知识及本体或规则所表达的条件，推导或判定进一步知识是否成立的过程。 | en：inference | tc-e0ddd60c-cecf-4652-8b9d-2234f194a7a1 |
| — | Resource Description Framework | zh-Hans：用于 Web 信息表示、以主语—谓语—宾语三元组构成图的数据框架。 | en：RDF | tc-acd244b6-0d82-4366-ac25-3fb7260c6473 |
| — | RDFS | zh-Hans：用于 RDF 数据的数据建模词汇。 | — | tc-a07a37d8-13b6-4a9d-b86c-ba96f0c080b4 |
| — | OWL | zh-Hans：用于表达本体、具有形式语义并可与 RDF 一起使用的 Web 本体语言。 | — | tc-b4f8bca4-b3cf-405b-8cf1-ea45112783d2 |
| — | SPARQL | zh-Hans：用于 RDF 数据的查询语言。 | — | tc-e638bec2-4c85-4eed-9721-8175f5417f6d |
| — | Simple Knowledge Organization System | zh-Hans：以 RDF 表达知识组织系统的数据模型；其 Reference 是 W3C Recommendation。 | en：SKOS | tc-2633b390-938e-4c0b-9bec-deebf8f65e8b |
| 属性图 | property graph | zh-Hans：允许为节点和边关联标签及属性—值对的图数据模型。 | — | tc-5c59be76-71b8-4e7e-8bd7-3763d8058473 |
| — | Cypher | zh-Hans：用于属性图的声明式查询语言。 | — | tc-1141d95e-3a9c-4955-bb15-2e7ff25b4cf2 |
| — | GQL | zh-Hans：ISO/IEC39075:2024规定的属性图数据管理语言。 | — | tc-5a533328-0f05-496f-b0dd-0436c4ef63b0 |

**三元组**（`tc-589ad410-5fc7-4f1b-ba5a-fd06c366016f`）


**概念依据**

- [RDF 1.1 Concepts and Abstract Syntax · 2014-02-25](https://www.w3.org/TR/rdf11-concepts/) · §3.1 Triples；RDF triple 的 subject、predicate、object 三组件；顺序为 subject-predicate-object · 核对日期 2026-09-06

**定义**

**简体中文定义**

由主语、谓语和宾语组成的 RDF 数据单元。

依据：
- [RDF 1.1 Concepts and Abstract Syntax · 2014-02-25](https://www.w3.org/TR/rdf11-concepts/) · §3.1 Triples；RDF triple 的 subject、predicate、object 三组件；顺序为 subject-predicate-object · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 三元组（`tm-9fdaa528-7ee8-4a29-ae7f-a8b08aaa0380`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：三元组在 RDF 中明确对应主语、谓语、宾语三组件；仅判断既有概念的行业表达，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- triple（`tm-eecf3ffd-6446-4574-966d-09a7304e8a7c`；preferredTerm-admn-sts）
  - 依据：[RDF 1.1 Concepts and Abstract Syntax · 2014-02-25](https://www.w3.org/TR/rdf11-concepts/) · §3.1 Triples；RDF triple 的 subject、predicate、object 三组件；顺序为 subject-predicate-object · 核对日期 2026-09-06

**历史形式**

无。

**实体**（`tc-79c1fd4b-5f06-4d1e-a8d8-cd323c441939`）


**概念依据**

- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · P1 L72–L88；nodes represent entities 与 identity 讨论；work/reviews/2026-09-06-term-web-model-coverage.json · 核对日期 2026-09-06

**定义**

**简体中文定义**

知识图谱中由节点表示的对象；节点及其标识用于表示和区分对象，不等于对象本身。

依据：
- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · P1 L72–L88；nodes represent entities 与 identity 讨论；work/reviews/2026-09-06-term-web-model-coverage.json · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 实体（`tm-9fb55b4b-7fe8-475f-a552-10bd90c5855d`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：实体是知识表示领域对被表示对象的行业称呼，不把实体等同于图节点或标识符。外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- entity（`tm-77ec69a0-9cb0-48f7-8194-1adae82bdbf6`；preferredTerm-admn-sts）
  - 依据：[Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · P1 L72–L88；nodes represent entities 与 identity 讨论；work/reviews/2026-09-06-term-web-model-coverage.json · 核对日期 2026-09-06

**历史形式**

无。

**关系**（`tc-4aa4867f-ea92-4a56-a56f-e8ffe45c1f91`）


**概念依据**

- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.1 L68–88，nodes represent entities/edges represent relations · 核对日期 2026-09-06

**定义**

**简体中文定义**

知识图谱所表示的实体之间的语义联系。

依据：
- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.1 L68–88，nodes represent entities/edges represent relations · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 关系（`tm-d5811399-5efc-4f04-bcf1-ccea4145a933`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：关系是语义联系，不是其图表示边；原relation与edge拆开，不泛化RDF predicate身份。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- relation（`tm-a3356e3f-f6c3-43bb-b088-fe607d15a8c7`；preferredTerm-admn-sts）
  - 依据：[Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.1 L68–88，nodes represent entities/edges represent relations · 核对日期 2026-09-06

**历史形式**

无。

**边**（`tc-95d07268-89f1-4c7f-86b0-98f60eeeef52`）


**概念依据**

- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.4 L192–200 directed edge-labelled graphs · 核对日期 2026-09-06

**定义**

**简体中文定义**

图中连接节点的结构；在知识图谱中可用来表示实体之间的关系。

依据：
- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.4 L192–200 directed edge-labelled graphs · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 边（`tm-28070939-fa29-4c92-bfdc-f96ba6758174`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：边是图连接的行业名称，原定义已出现该词；作为独立中文designation本包明确提出模型第5级，不谎称旧表已经独立登记。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- edge（`tm-b99aaec5-5d0c-4f7e-9ead-e73294328226`；preferredTerm-admn-sts）
  - 依据：[Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.4 L192–200 directed edge-labelled graphs · 核对日期 2026-09-06

**历史形式**

无。

**属性**（`tc-605b0308-57af-486b-81ba-81e18b993b07`）


**概念依据**

- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · P6 L316–L322；property graph 中 nodes/edges 关联 property–value pairs；work/reviews/2026-09-06-term-web-model-coverage.json · 核对日期 2026-09-06

**定义**

**简体中文定义**

在属性图中，与节点或边关联、以属性名和值构成的键值对表达的信息；值的具体形态由所用属性图模型规定。

依据：
- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · P6 L316–L322；property graph 中 nodes/edges 关联 property–value pairs；work/reviews/2026-09-06-term-web-model-coverage.json · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 属性（`tm-16fe2abb-fe52-4f08-97a4-5bb36f6c2f15`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：属性是图数据模型中描述节点或边特征的信息；本条明确属性图语境，并区别属性名与其值。外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- property（`tm-a91f7e4f-a2bb-4681-ba36-86d3529b7cbe`；preferredTerm-admn-sts）
  - 依据：[Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · P6 L316–L322；property graph 中 nodes/edges 关联 property–value pairs；work/reviews/2026-09-06-term-web-model-coverage.json · 核对日期 2026-09-06

**历史形式**

无。

**schema**（`tc-daa1c79a-56f0-4d62-a360-ddaa9b332d0f`）


**概念依据**

- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.1 L84–88 high-level structure · 核对日期 2026-09-06

**定义**

**简体中文定义**

知识图谱或数据模型的高层结构说明，可涉及类型、关系和约束。

依据：
- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.1 L84–88 high-level structure · 核对日期 2026-09-06

**术语形式**

**英文形式**

- schema（`tm-f46f87b7-417d-492b-b34f-9bcb2a74fcef`；preferredTerm-admn-sts）
  - 依据：[Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.1 L84–88 high-level structure · 核对日期 2026-09-06
- Schema（`tm-bfe84c3f-798d-441f-9306-ea6e990a168a`；admittedTerm-admn-sts）
  - 依据：[Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.1 L84–88 high-level structure · 核对日期 2026-09-06

**历史形式**

无。

**推理**（`tc-e0ddd60c-cecf-4652-8b9d-2234f194a7a1`）


**概念依据**

- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，§4.3 Reasoning、§4.3.1 Rules，Table6/Figure22 · 核对日期 2026-09-06

**定义**

**简体中文定义**

依据已有知识及本体或规则所表达的条件，推导或判定进一步知识是否成立的过程。

依据：
- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，§4.3 Reasoning、§4.3.1 Rules，Table6/Figure22 · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 推理（`tm-ac9b494f-ac60-4b34-9f0c-c1deb91ad26d`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：推理在此是规则或本体条件下的推导/蕴涵判定，可物化或查询重写，不必写入新边；不扩成全部归纳学习。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- reasoning（`tm-e5a02701-e0ef-4995-99a9-67f4132da244`；preferredTerm-admn-sts）
  - 依据：[Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，§4.3 Reasoning、§4.3.1 Rules，Table6/Figure22 · 核对日期 2026-09-06
- inference（`tm-8e2fa2f3-0729-4c4c-a8eb-bbc5df747e6e`；admittedTerm-admn-sts）
  - 依据：[RDF Semantics · 2004-02-10](https://www.w3.org/TR/rdf-mt/) · AppendixB Glossary (Informative)，Inference，L1282 · 核对日期 2026-09-06

**历史形式**

无。

**Resource Description Framework**（`tc-acd244b6-0d82-4366-ac25-3fb7260c6473`）


**概念依据**

- [RDF 1.1 Concepts and Abstract Syntax · 2014-02-25](https://www.w3.org/TR/rdf11-concepts/) · Introduction；§3.1 Triples · 核对日期 2026-09-06

**定义**

**简体中文定义**

用于 Web 信息表示、以主语—谓语—宾语三元组构成图的数据框架。

依据：
- [RDF 1.1 Concepts and Abstract Syntax · 2014-02-25](https://www.w3.org/TR/rdf11-concepts/) · Introduction；§3.1 Triples · 核对日期 2026-09-06

**术语形式**

**英文形式**

- Resource Description Framework（`tm-ceea4cbc-ecb1-4aa5-9d44-82267d0d943c`；preferredTerm-admn-sts）
  - 依据：[RDF 1.1 Concepts and Abstract Syntax · 2014-02-25](https://www.w3.org/TR/rdf11-concepts/) · Introduction；§3.1 Triples · 核对日期 2026-09-06
- RDF（`tm-4e708f52-6a2a-4ae6-b9cb-b7286d3a85d0`；admittedTerm-admn-sts）
  - 依据：[RDF 1.1 Concepts and Abstract Syntax · 2014-02-25](https://www.w3.org/TR/rdf11-concepts/) · Introduction；§3.1 Triples · 核对日期 2026-09-06

**历史形式**

无。

**RDFS**（`tc-a07a37d8-13b6-4a9d-b86c-ba96f0c080b4`）


**概念依据**

- [RDF Schema 1.1 · 2014-02-25](https://www.w3.org/TR/rdf-schema/) · Abstract；§1 · 核对日期 2026-09-06

**定义**

**简体中文定义**

用于 RDF 数据的数据建模词汇。

依据：
- [RDF Schema 1.1 · 2014-02-25](https://www.w3.org/TR/rdf-schema/) · Abstract；§1 · 核对日期 2026-09-06

**术语形式**

**英文形式**

- RDFS（`tm-b710284d-ad1f-47d2-911d-616d0aba7688`；preferredTerm-admn-sts）
  - 依据：[RDF Schema 1.1 · 2014-02-25](https://www.w3.org/TR/rdf-schema/) · Abstract；§1 · 核对日期 2026-09-06

**历史形式**

无。

**OWL**（`tc-b4f8bca4-b3cf-405b-8cf1-ea45112783d2`）


**概念依据**

- [OWL 2 Web Ontology Language Document Overview (Second Edition) · 2012-12-11](https://www.w3.org/TR/owl2-overview/) · Abstract；§1 · 核对日期 2026-09-06

**定义**

**简体中文定义**

用于表达本体、具有形式语义并可与 RDF 一起使用的 Web 本体语言。

依据：
- [OWL 2 Web Ontology Language Document Overview (Second Edition) · 2012-12-11](https://www.w3.org/TR/owl2-overview/) · Abstract；§1 · 核对日期 2026-09-06

**术语形式**

**英文形式**

- OWL（`tm-e587b46e-66cd-43a1-8423-339602565de7`；preferredTerm-admn-sts）
  - 依据：[OWL 2 Web Ontology Language Document Overview (Second Edition) · 2012-12-11](https://www.w3.org/TR/owl2-overview/) · Abstract；§1 · 核对日期 2026-09-06

**历史形式**

无。

**SPARQL**（`tc-e638bec2-4c85-4eed-9721-8175f5417f6d`）


**概念依据**

- [SPARQL 1.1 Query Language · 2013-03-21](https://www.w3.org/TR/sparql11-query/) · §1 Introduction；SPARQL 1.1 规范定义 RDF 查询语言的 syntax 和 semantics · 核对日期 2026-09-06

**定义**

**简体中文定义**

用于 RDF 数据的查询语言。

依据：
- [SPARQL 1.1 Query Language · 2013-03-21](https://www.w3.org/TR/sparql11-query/) · §1 Introduction；SPARQL 1.1 规范定义 RDF 查询语言的 syntax 和 semantics · 核对日期 2026-09-06

**术语形式**

**英文形式**

- SPARQL（`tm-be311ab7-f917-4c29-840c-2ef0e64c23cf`；preferredTerm-admn-sts）
  - 依据：[SPARQL 1.1 Query Language · 2013-03-21](https://www.w3.org/TR/sparql11-query/) · §1 Introduction；SPARQL 1.1 规范定义 RDF 查询语言的 syntax 和 semantics · 核对日期 2026-09-06

**历史形式**

无。

**Simple Knowledge Organization System**（`tc-2633b390-938e-4c0b-9bec-deebf8f65e8b`）


**概念依据**

- [W3C SKOS 参考 / W3C SKOS Simple Knowledge Organization System Reference · 2009-08-18](https://www.w3.org/TR/skos-reference/) · Introduction；SKOS data model · 核对日期 2026-09-06

**定义**

**简体中文定义**

以 RDF 表达知识组织系统的数据模型；其 Reference 是 W3C Recommendation。

依据：
- [W3C SKOS 参考 / W3C SKOS Simple Knowledge Organization System Reference · 2009-08-18](https://www.w3.org/TR/skos-reference/) · Introduction；SKOS data model · 核对日期 2026-09-06

**术语形式**

**英文形式**

- Simple Knowledge Organization System（`tm-7019ad5a-e9f6-4db3-8596-3e29c256455c`；preferredTerm-admn-sts）
  - 依据：[W3C SKOS 参考 / W3C SKOS Simple Knowledge Organization System Reference · 2009-08-18](https://www.w3.org/TR/skos-reference/) · Introduction；SKOS data model · 核对日期 2026-09-06
- SKOS（`tm-e854dfc3-779a-4e51-8253-520cc3722fec`；admittedTerm-admn-sts）
  - 依据：[W3C SKOS 参考 / W3C SKOS Simple Knowledge Organization System Reference · 2009-08-18](https://www.w3.org/TR/skos-reference/) · Introduction；SKOS data model · 核对日期 2026-09-06

**历史形式**

无。

**属性图**（`tc-5c59be76-71b8-4e7e-8bd7-3763d8058473`）


**概念依据**

- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.6 L277–328 property graphs · 核对日期 2026-09-06

**定义**

**简体中文定义**

允许为节点和边关联标签及属性—值对的图数据模型。

依据：
- [Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.6 L277–328 property graphs · 核对日期 2026-09-06

**术语形式**

**简体中文形式**

- 属性图（`tm-a6977c3d-9ff1-4b1b-803b-0b604a67dacd`；preferredTerm-admn-sts）
  - 依据：模型知识 · 第 5 级，外部中文用法未核实
  - 依据：模型名称：gpt-6-astra
  - 依据：判断日期：2026-09-06
  - 依据：判断理由：属性图保留原图模型概念；Hogan已核正文支持定义，不伪称ISO39075完整条款已读。；模型知识第5级，外部中文用法未核实。
  - 依据：采纳授权：decision-term-data-values

**英文形式**

- property graph（`tm-53e44f07-69b0-4040-8946-8098102fb3d1`；preferredTerm-admn-sts）
  - 依据：[Knowledge Graphs · arXiv v6](https://arxiv.org/pdf/2003.02320v6) · arXivv6，PDFp.6 L277–328 property graphs · 核对日期 2026-09-06

**历史形式**

无。

**Cypher**（`tc-1141d95e-3a9c-4955-bb15-2e7ff25b4cf2`）


**概念依据**

- [Cypher: An Evolving Query Language for Property Graphs · 2018](https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf) · SIGMOD18作者稿PDFp.3/论文p.1434，§2 The Cypher Language · 核对日期 2026-09-06

**定义**

**简体中文定义**

用于属性图的声明式查询语言。

依据：
- [Cypher: An Evolving Query Language for Property Graphs · 2018](https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf) · SIGMOD18作者稿PDFp.3/论文p.1434，§2 The Cypher Language · 核对日期 2026-09-06

**术语形式**

**英文形式**

- Cypher（`tm-7e361d24-7036-4df6-b1d1-89d2ae56c6d1`；preferredTerm-admn-sts）
  - 依据：[Cypher: An Evolving Query Language for Property Graphs · 2018](https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf) · SIGMOD18作者稿PDFp.3/论文p.1434，§2 The Cypher Language · 核对日期 2026-09-06

**历史形式**

无。

**GQL**（`tc-5a533328-0f05-496f-b0dd-0436c4ef63b0`）


**概念依据**

- [Information technology — Database languages — GQL · 2024](https://www.iso.org/standard/76120.html) · 官方Abstract：规定用于property graphs的数据管理语言syntax与semantics；Edition1，2024-04 · 核对日期 2026-09-06

**定义**

**简体中文定义**

ISO/IEC39075:2024规定的属性图数据管理语言。

依据：
- [Information technology — Database languages — GQL · 2024](https://www.iso.org/standard/76120.html) · 官方Abstract：规定用于property graphs的数据管理语言syntax与semantics；Edition1，2024-04 · 核对日期 2026-09-06

**术语形式**

**英文形式**

- GQL（`tm-3b963620-d52f-49e0-9c5b-3e3d9f52bcd2`；preferredTerm-admn-sts）
  - 依据：[Information technology — Database languages — GQL · 2024](https://www.iso.org/standard/76120.html) · 官方Abstract：规定用于property graphs的数据管理语言syntax与semantics；Edition1，2024-04 · 核对日期 2026-09-06

**历史形式**

无。

## 补充说明

- 来源分级｜de-jure / de-facto / vendor / archival｜来源记录的分档值，影响可用引用用途与复核周期；具体分档、用途限制和变更须遵循现行来源规则。Z39.19的组织依据说明项目选择的依据，不定义这四个档次。｜docs/design/model/entities.md；docs/design/model/sources-registry.md；docs/design/governance/maintenance.md
  - 范围：来源tier枚举的治理说明，de-jure/de-facto/vendor/archival不因出现而成为四个术语概念。
  - 依据：本库字段说明，引用现行项目规则，不伪装外部四档术语定义。
- exactMatch / closeMatch｜—｜skos:exactMatch 表示概念可在广泛的信息检索应用中高可信地互换使用；skos:closeMatch 表示概念在某些信息检索应用中足够相近、可互换使用。exactMatch 具有传递性；closeMatch 不声明传递性，不据此作传递推断。｜W3C SKOS Reference §10.4、§10.6
  - 范围：跨concept scheme的映射属性；不将closeMatch当作ISO inexact equivalence的无条件同义表示，也不把未声明传递性误写成反传递。
- broadMatch / narrowMatch / relatedMatch｜—｜skos:broadMatch 从源概念指向含义较宽的目标概念；skos:narrowMatch 指向含义较窄的目标概念；skos:relatedMatch 表示概念间的相关映射。它们是SKOS跨概念方案映射属性，不是本库新增关系类别。｜W3C SKOS Reference §10
  - 范围：SKOS broadMatch/narrowMatch/relatedMatch为映射属性标识，按W3C映射语义引用，不造三个TC。

## 关系符号

- USE / UF：关系指示符，参考所链接的关系概念；不作为英文术语形式。 参见 `tc-75e8012c-351f-4303-b8c0-523454b9b730`。
- USE+ / UF+：关系指示符，参考所链接的关系概念；不作为英文术语形式。 参见 `tc-ad90ba40-f5b0-44e7-9f59-fa2783d837b3`。
- BT / NT：关系指示符，参考所链接的关系概念；不作为英文术语形式。 参见 `tc-278494cf-719c-43f9-b954-2a54c61e5c45`。
- BTG / NTG：关系指示符，参考所链接的关系概念；不作为英文术语形式。 参见 `tc-54e74c2d-103e-4935-aab7-fb44a129af69`。
- BTP / NTP：关系指示符，参考所链接的关系概念；不作为英文术语形式。 参见 `tc-818463b8-0d48-4ddf-98fb-228ef4591308`。
- BTI / NTI：关系指示符，参考所链接的关系概念；不作为英文术语形式。 参见 `tc-9fde9fd8-eb29-4477-acc1-295f9de9adf5`。
- RT：关系指示符，参考所链接的关系概念；不作为英文术语形式。 参见 `tc-589f6145-5330-4773-b2dd-27eeeaa6bc84`。

## 历史名称

- 术语表 / 代码表：已退出所列概念的当前准用名称。
  - 原称术语表／代码表，现用列表；两旧称仅供历史检索与解释，不作为此概念的准用名称。
  - 原因：原行实际概念为NISO§5.4.1 list；术语表容易指带定义的glossary，代码表指代码及取值清单，两者不能无条件作为一般list同义名。建议采用列表；不为代码表另建code-list概念。
  - 效力：名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
  - 目标：`tc-94e9bdfe-cefd-445c-9a12-f276bfe75e63`
- paradigmatic：已退出所列概念的当前准用名称。
  - 原英文paradigmatic，完整名称为paradigmatic relationship。
  - 原因：原单独形容词省略relationship；采用已核ISO完整名称，旧省略写法不再作独立当前designation。
  - 效力：名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
  - 目标：`tc-df2d8160-1717-4372-a38f-db96925ac980`
- syntagmatic：已退出所列概念的当前准用名称。
  - 原英文syntagmatic，完整名称为syntagmatic relationship。
  - 原因：原单独形容词未完整表示关系名称，按作者用法补足relationship。
  - 效力：名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
  - 目标：`tc-1b0b91bc-d29e-44d4-854c-cddd05aebc13`
- 认知层级 / cognitive level：已退出所列概念的当前准用名称。
  - 旧称认知层级／cognitive level；来源概念名称为认知过程维度／cognitive process dimension。
  - 原因：Krathwohl原名称是Cognitive Process dimension，旧名称将维度简化为单一深度。作为外部概念名称建议纠正；本库level字段可选和自评用途仍按现行模型，不由名称纠正更改。
  - 效力：名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
  - 目标：`tc-b49a8de0-d20e-42da-b7f0-f8d09ce44dc2`
- 政策 / policy：已退出所列概念的当前准用名称。
  - 原政策／policy在本行治理语境明确为治理政策／governance policy。
  - 原因：采用实际原词头governance policy与治理政策；不无条件把一般policy作为同义。旧项目政策规则的约束效力按governance文档保持，术语改名不取消实际义务。
  - 效力：名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
  - 目标：`tc-24c3f7b9-c6a2-4e1c-91f2-b3ee234219c8`
- 监控与评价 / monitoring and evaluation：已退出所列概念的当前准用名称。
  - 原组合监控与评价；分别见监测（monitoring）与评估（evaluation）。
  - 原因：原组合是两种活动，不是一个同义名称；采用OECD已核监测/评估，旧中文组合仅保留迁移前检索，不自动作为单概念准用词。
  - 效力：名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
  - 目标：`tc-09ff3cd6-f825-4e90-b401-4ef25c2cc084`、`tc-f881797d-c9ff-4f57-9523-b6a1c01c8b2c`

## 引用的标准与文献

- ISO 25964-1:2011 / -2:2013｜叙词表国际标准，见 [笔记](references/iso-25964.md)
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- GB/T 13190.1-2015 / .2-2018｜等同采用 ISO 25964 的国标
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- ANSI/NISO Z39.19-2005 (R2010)｜美国受控词表标准，全文免费
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- ISO 704｜术语工作原则与方法，Wüster 理论的标准化版本；未核对
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- W3C SKOS / RDF / OWL / SPARQL｜语义网标准族
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- ISO/IEC 39075:2024 GQL｜属性图查询语言标准
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- Cutter (1876)｜字典式目录规则，主题标目“一主题一词”的源头；未核对
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- Hulme (1911)｜*Principles of Book Classification*,Library Association Record 连载；文献依据的源头
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- Dewey (1876)｜十进分类法；未核对
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- Ranganathan (1933)｜冒号分类法，分面分析的源头；经 Z39.19 §5.3.4 转述
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- Wüster (1931)｜斯图加特博士论文 Internationale Sprachnormung in der Technik；术语学历史资料。旧登记的机构起源说明本批未核，不作为已核事实展示。
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- Gruber (1993)｜计算机领域本体的定义；未核对
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- Hogan et al. (2021)｜知识图谱综述，[arXiv](https://arxiv.org/abs/2003.02320)
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。
- Ehrlinger & Wöß (2016)｜知识图谱定义梳理，[CEUR](https://ceur-ws.org/Vol-1695/paper4.pdf)
  - 核验：继承现行文献说明；原未核标记保留，本次未以这些说明证明定义事实。
  - 说明：既有书目线索；未核的历史或版本对应不因本批结构迁移升级为已核事实。

## 来源目录

- ahrens-zettelkasten-interview：[Zettelkasten "Super" Notes: with Dr Sönke Ahrens](https://examstudyexpert.com/zettelkasten/)
- american-heritage-dictionary-5-cheat-sheet：[The American Heritage Dictionary of the English Language, Fifth Edition](https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0)
- aristotle-metaphysics-ross：[Metaphysics](https://classics.mit.edu/Aristotle/metaphysics.1.i.html)
- aristotle-posterior-analytics-mure：[Posterior Analytics](https://classics.mit.edu/Aristotle/posterior.1.i.html)
- buckingham-shum-1995-design-rationale：[Design Argumentation as Design Rationale](https://kmi.open.ac.uk/publications/techreport/kmi-95-14)
- clarke-information-retrieval-thesaurus：[The Information Retrieval Thesaurus](https://www.isko.org/cyclo/thesaurus)
- cornell-cs3110-2012-partition：[CS 3110 Recitation 14](https://www.cs.cornell.edu/courses/cs3110/2012fa/recitations/rec14.html)
- cs2023：[计算机科学课程 2023 / Computer Science Curricula 2023](https://csed.acm.org/final-report/)
- dcmi-metadata-terms：[DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- dcmi-singapore-framework：[The Singapore Framework for Dublin Core™ Application Profiles](https://www.dublincore.org/specifications/dublin-core/singapore-framework/)
- dfe-external-governance-reviews：[External governance reviews: guide for FE college corporations and designated institutions](https://www.gov.uk/guidance/external-governance-reviews-guide-for-fe-college-corporations-and-designated-institutions)
- dita：[DITA 1.3 / Darwin Information Typing Architecture 1.3](http://docs.oasis-open.org/dita/dita/v1.3/os/part1-base/dita-v1.3-os-part1-base.html)
- dnb-marc-2014-05：[MARC Proposal 2014-05](https://wwws.loc.gov/marc/mac/2014/2014-05.html)
- dnd-caf-data-governance：[DND/CAF (Department of National Defence and the Canadian Armed Forces) Data Governance Framework](https://www.canada.ca/en/department-national-defence/corporate/reports-publications/data-governance.html)
- dunn-bourcier-nomenclature：[Nomenclature for Museum Cataloging](https://www.isko.org/cyclo/nomenclature.htm)
- francis-et-al-2018-cypher：[Cypher: An Evolving Query Language for Property Graphs](https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf)
- gertz-1974：[Gertz v. Robert Welch, Inc., 418 U.S. 323](https://www.law.cornell.edu/supremecourt/text/418/323)
- gruber-official：[Ontology](https://tomgruber.org/writing/definition-of-ontology/)
- hearst-2009-search-user-interfaces：[Search User Interfaces](https://searchuserinterfaces.com/book/sui_ch8_navigation_and_search.html)
- hjorland-domain-analysis：[Domain analysis](https://www.isko.org/cyclo/domain_analysis)
- hjorland-facet-analysis：[Facet analysis](https://www.isko.org/cyclo/facet_analysis)
- hjorland-knowledge-organization：[Knowledge organization (KO)](https://www.isko.org/cyclo/knowledge_organization)
- hogan-paper：[Knowledge Graphs](https://arxiv.org/pdf/2003.02320v6)
- iptc-genre：[IPTC NewsCodes 体裁词表 / IPTC NewsCodes Genre](https://cv.iptc.org/newscodes/genre/)
- iso-1087-2019：[Terminology work and terminology science — Vocabulary](https://cdn.standards.iteh.ai/samples/62330/f8493dfbf02f4f23b9d9524832aa0b9b/ISO-1087-2019.pdf)
- iso-15489-1：[Information and documentation — Records management — Part 1: Concepts and principles](https://www.iso.org/standard/62542.html)
- iso-24495-1：[Plain language — Part 1: Governing principles and guidelines](https://cdn.standards.iteh.ai/samples/78907/d194fac21d6a45f38bfcfec9657f7498/ISO-24495-1-2023.pdf)
- iso-25964-1：[ISO 25964-1:2011 叙词表 / ISO 25964-1:2011 Thesauri for information retrieval](https://www.iso.org/standard/53657.html)
- iso-25964-2：[ISO 25964-2:2013 与其他词表的互操作 / ISO 25964-2:2013 Interoperability with other vocabularies](https://www.iso.org/standard/53658.html)
- iso-37000-2021：[Governance of organizations — Guidance](https://cdn.standards.iteh.ai/samples/65036/68ac8ac92aac4aa6b0568042fdab2da5/ISO-37000-2021.pdf)
- iso-39075-2024：[Information technology — Database languages — GQL](https://www.iso.org/standard/76120.html)
- iso25964-xsd-1-4：[ISO 25964-1 XML Schema](https://www.niso.org/schemas/iso25964/iso25964-1_v1.4.xsd)
- juran-1974-non-pareto：[The Non-Pareto Principle; Mea Culpa](https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf)
- kaula-1980-canons：[Canons in Analytico-Synthetic Classification](https://article.imrpress.com/journal/KO/7/3/10.5771/0943-7444-1980-3-118/4a183d5ac38a2c528b0133c11817a7a7.pdf)
- krathwohl-2002-taxonomy：[A Revision of Bloom’s Taxonomy: An Overview](https://cmapspublic2.ihmc.us/rid=1Q2PTM7HL-26LTFBX-9YN8/Krathwohl%202002.pdf)
- lamb-zacchiroli-2021-reproducible-builds：[Reproducible Builds: Increasing the Integrity of Software Supply Chains](https://arxiv.org/pdf/2104.06020v1)
- mazzocchi-knowledge-organization-system：[Knowledge organization system](https://www.isko.org/cyclo/kos)
- nist-dads-node：[Dictionary of Algorithms and Data Structures: node](https://xlinux.nist.gov/dads/HTML/node.html)
- nist-dads-tree：[Dictionary of Algorithms and Data Structures: tree](https://xlinux.nist.gov/dads/HTML/tree.html)
- nist-sp-800-53r5：[Security and Privacy Controls for Information Systems and Organizations](https://doi.org/10.6028/NIST.SP.800-53r5)
- nonaka-toyama-konno-managing-industrial-knowledge：[Managing Industrial Knowledge, Chapter 1](https://api.pageplace.de/preview/DT0400.9781847876621_A23446119/preview-9781847876621_A23446119.pdf)
- nygard-2011-architecture-decisions：[Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- oecd-2024-evaluation-glossary-en-zh：[Glossary of Key Terms in Evaluation and Results-Based Management for Sustainable Development (Second edition), English/Chinese](https://www.oecd.org/content/dam/oecd/zh/publications/reports/2023/06/glossary-of-key-terms-in-evaluation-and-results-based-management-for-sustainable-development-second-edition_2767e14e/74f41029-en-zh.pdf)
- owl2：[OWL 2 Web Ontology Language Document Overview (Second Edition)](https://www.w3.org/TR/owl2-overview/)
- owl2-primer：[OWL 2 Web Ontology Language Primer (Second Edition)](https://www.w3.org/TR/owl2-primer/)
- rdf11：[RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/)
- rdfs11：[RDF Schema 1.1](https://www.w3.org/TR/rdf-schema/)
- skos：[W3C SKOS 参考 / W3C SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/skos-reference/)
- sparql11：[SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)
- star-bowker-2007-enacting-silence：[Enacting silence](https://link.springer.com/article/10.1007/s10676-007-9141-7)
- stern-fragment-whole：[The Fragment and the Whole](https://takenote.library.harvard.edu/fragment-and-whole)
- swebok：[软件工程知识体系指南 v4.0 / Guide to the Software Engineering Body of Knowledge v4.0](https://www.computer.org/education/bodies-of-knowledge/software-engineering)
- w3c-rdf-semantics-2004：[RDF Semantics](https://www.w3.org/TR/rdf-mt/)
- w3c-udc-use-case：[Universal Decimal Classification](https://www.w3.org/2006/07/SWD/wiki/EucUDC)
- w3c-xml-1-0：[Extensible Markup Language (XML) 1.0 (Fifth Edition)](https://www.w3.org/TR/REC-xml/)
- will-2009-skos-iso：[Differences between SKOS and ISO standards](https://lists.w3.org/Archives/Public/public-esw-thes/2009Feb/0033.html)
- will-2012-iso-data-model：[The ISO 25964 data model for the structure of an information retrieval thesaurus](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/bult.2012.1720380413)
- z39-19：[ANSI/NISO Z39.19-2005 (R2010) / ANSI/NISO Z39.19-2005 (R2010) Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies](https://www.niso.org/publications/ansiniso-z3919-2005-r2010)
- zeng-interoperability：[Interoperability](https://www.isko.org/cyclo/interoperability)

## 模型译名

- AI 攻击准备 / AI Attack Staging：topics/ai-attack-staging
  - topics/ai-attack-staging：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指利用已掌握的目标知识和访问定制攻击，如构造对抗样本，区别于通用资源准备。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- AI 模型访问 / AI Model Access：topics/ai-model-access
  - topics/ai-model-access：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指对模型取得可供后续技术使用的某种访问能力，不等同于访问模型所在主机。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- API 与 Web 服务 / API and Web Service：topics/api-and-web-service
  - topics/api-and-web-service：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留 API 的通行缩写，并保留 Web 服务这一并列对象，范围为接口暴露涉及的安全要求。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- NoSQL 系统 / NoSQL Systems：topics/nosql-systems
  - topics/nosql-systems：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留 NoSQL 技术类别名称，涵盖键值、文档与图等系统，不将其误解为完全不能使用 SQL。；design/decisions/structured-label-basis.md#批次授权
- OAuth 与 OIDC / OAuth and OIDC：topics/oauth-and-oidc
  - topics/oauth-and-oidc：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留协议名称与缩写，区分 OAuth 的委托授权框架和 OIDC 的身份层。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- Shell 脚本编程 / Shell Scripting：topics/shell-scripting
  - topics/shell-scripting：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指运用 Shell 脚本组合命令、管道和环境变量等完成计算任务，保留 scripting 的编写活动含义。；design/decisions/structured-label-basis.md#批次授权
- Web 前端安全 / Web Frontend Security：topics/web-frontend-security
  - topics/web-frontend-security：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；限定浏览器侧 Web 前端及其攻击面，不扩展为所有应用接口安全。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- Web 实时通信 / WebRTC：topics/webrtc
  - topics/webrtc：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按 WebRTC 的通行展开理解为实时语音、视频和数据通信技术，范围仍限定于 WebRTC。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- Web 平台 / Web Platforms：topics/web-platforms
  - topics/web-platforms：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指 Web 语言、框架、标准及应用环境，保留 Web 限定，不泛化为所有网络平台。；design/decisions/structured-label-basis.md#批次授权
- 专用平台开发 / Specialized Platform Development：topics/specialized-platform-development
  - topics/specialized-platform-development：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指面向 Web、移动、机器人等特定平台约束的开发，专用不表示私有或封闭。；design/decisions/structured-label-basis.md#批次授权
- 中和处理不当 / Improper Neutralization：topics/improper-neutralization
  - topics/improper-neutralization：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；中和指使结构化数据中的危险内容不再产生非预期解释，包含相关编码、转义等处理而不限于删除。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 事件驱动与响应式程序设计 / Event-Driven and Reactive Programming：topics/event-driven-and-reactive-programming
  - topics/event-driven-and-reactive-programming：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；分别对应事件触发处理与随输入变化作出响应的程序设计方式，不把两个范式合并成单一名称。；design/decisions/structured-label-basis.md#批次授权
- 交互 / Interaction：topics/interaction
  - topics/interaction：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指人与图形或计算界面的输入响应关系，涵盖手势、触觉与多模态界面。；design/decisions/structured-label-basis.md#批次授权
- 交互式计算平台 / Interactive Computing Platforms：topics/interactive-computing-platforms
  - topics/interactive-computing-platforms：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指通过交互方式开展计算的开发平台，既有范围含数据分析、提示词编程和量子平台。；design/decisions/structured-label-basis.md#批次授权
- 产品需求 / Product Requirements：topics/product-requirements
  - topics/product-requirements：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指产品应具备的功能与质量要求，兼有获取与一致性等要求管理问题。；design/decisions/structured-label-basis.md#批次授权
- 人机交互 / Human-Computer Interaction：topics/human-computer-interaction
  - topics/human-computer-interaction：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指用户与计算系统的交互及其设计和评估，保留人的需求与系统两侧。；design/decisions/structured-label-basis.md#批次授权
- 代码生成 / Code Generation：topics/code-generation
  - topics/code-generation：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；在编译语境中指由程序表示生成目标代码，涵盖指令选择、调度及寄存器分配。；design/decisions/structured-label-basis.md#批次授权
- 仿真 / Simulation：topics/simulation, forms/simulation
  - topics/simulation：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；在图形学中指按模型模拟物理或规则系统的动态行为，包含碰撞、粒子和流体。；design/decisions/structured-label-basis.md#批次授权
  - forms/simulation：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指可操作的模型环境及模拟活动，保留与按步骤实际操作观察的实验形式的区别。；design/decisions/structured-label-basis.md#批次授权
- 会话管理 / Session Management：topics/session-management
  - topics/session-management：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应身份会话的唯一性、不可预测性、失效和超时控制，不指会议组织。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 传输层 / Transport Layer：topics/transport-layer
  - topics/transport-layer：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应为应用提供端到端通信服务的协议层，同时涵盖 TCP 和 UDP。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 伦理分析方法 / Methods for Ethical Analysis：topics/methods-for-ethical-analysis
  - topics/methods-for-ethical-analysis：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指伦理理论、论证和决策框架等分析方法，不将伦理判断缩为法律合规。；design/decisions/structured-label-basis.md#批次授权
- 体系结构与组织 / Architecture and Organization：topics/architecture-and-organization
  - topics/architecture-and-organization：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；同时保留计算机体系结构与机器组织两个方面，范围涵盖指令、存储和硬件实现。；design/decisions/structured-label-basis.md#批次授权
- 侦察 / Reconnaissance：topics/reconnaissance, topics/reconnaissance-artificial-intelligence
  - topics/reconnaissance：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指为后续攻击规划收集目标信息，与进入环境后了解内部系统的发现战术区分。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/reconnaissance-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指为攻击规划收集 AI 系统信息，AI 语境由既有概念范围限定。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 保护与安全 / Protection and Safety：topics/protection-and-safety
  - topics/protection-and-safety：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留原名的保护和安全两部分；现有范围涉及访问保护、攻击和缓解，不额外推定 safety 的工程边界。；design/decisions/structured-label-basis.md#批次授权
- 保护机制失效 / Protection Mechanism Failure：topics/protection-mechanism-failure
  - topics/protection-mechanism-failure：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；覆盖保护机制缺失和使用错误导致的防护失败，不仅指机制运行后崩溃。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 共同方面与共同关注点 / Common Aspects/Shared Concerns：topics/common-aspects-shared-concerns
  - topics/common-aspects-shared-concerns：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指各专用平台共有的约束、语言和开发问题，保留原名斜线两侧的近义表达。；design/decisions/structured-label-basis.md#批次授权
- 关系数据库 / Relational Databases：topics/relational-databases
  - topics/relational-databases：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；关系对应关系数据模型，范围涵盖完整性、模式映射与规范化。；design/decisions/structured-label-basis.md#批次授权
- 内存管理 / Memory Management：topics/memory-management
  - topics/memory-management：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指地址空间、地址转换和分页等内存资源管理，区别于包含持久介质的广义存储管理。；design/decisions/structured-label-basis.md#批次授权
- 几何建模 / Geometric Modeling：topics/geometric-modeling
  - topics/geometric-modeling：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指以几何表示构造、处理和重建形状，涵盖曲面、体与多分辨率表示。；design/decisions/structured-label-basis.md#批次授权
- 凭据访问 / Credential Access：topics/credential-access, topics/credential-access-artificial-intelligence
  - topics/credential-access：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按攻击战术理解为取得账户名、口令等凭据，不表示合法用户读取自己的凭据。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/credential-access-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指窃取可用于 AI 环境的账户名、口令等凭据，不是模型训练数据访问。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 函数式程序设计 / Functional Programming：topics/functional-programming
  - topics/functional-programming：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应函数、不可变或无副作用计算、高阶函数与闭包的程序设计范式。；design/decisions/structured-label-basis.md#批次授权
- 分布式数据库与云计算 / Distributed Databases/Cloud Computing：topics/distributed-databases-cloud-computing
  - topics/distributed-databases-cloud-computing：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留原名并列的数据库与云计算两部分，既有范围以分布式和并行数据库为主。；design/decisions/structured-label-basis.md#批次授权
- 初始访问 / Initial Access：topics/initial-access, topics/initial-access-artificial-intelligence
  - topics/initial-access：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指通过入口向量首次取得目标网络立足点，不表示已提升权限。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/initial-access-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指取得 AI 系统所在环境的初始访问，与直接取得模型访问能力区分。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 功能组织 / Functional Organization：topics/functional-organization
  - topics/functional-organization：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指数据通路、控制单元和流水线如何组织以实现处理器功能，不是机构职能划分。；design/decisions/structured-label-basis.md#批次授权
- 半结构化与非结构化数据库 / Semi-structured and Unstructured Databases：topics/semi-structured-and-unstructured-databases
  - topics/semi-structured-and-unstructured-databases：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；分别保留半结构化及非结构化数据的数据库处理范围，包括 JSON 与向量存储。；design/decisions/structured-label-basis.md#批次授权
- 协调 / Coordination：topics/coordination
  - topics/coordination：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指并行和分布式活动间的依赖、控制和原子性协调，不指团队行政协调。；design/decisions/structured-label-basis.md#批次授权
- 单跳通信 / Single Hop Communication：topics/single-hop-communication
  - topics/single-hop-communication：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指相邻节点之间的一跳传递，涵盖介质、成帧和介质访问，不扩为多跳路由。；design/decisions/structured-label-basis.md#批次授权
- 发现 / Discovery：topics/discovery, topics/discovery-artificial-intelligence
  - topics/discovery：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指攻击者探知目标系统和内部网络环境，区别于为行动规划开展的侦察。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/discovery-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指了解目标 AI 环境内部情况，与行动规划阶段的侦察区分。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 叙述性文本 / Narrative text：forms/narrative-text
  - forms/narrative-text：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指连续展开的叙述正文，不限于文学故事，保留与表格及索引等形式的区别。；design/decisions/structured-label-basis.md#批次授权
- 可持续性 / Sustainability：topics/sustainability
  - topics/sustainability：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；涵盖计算实现的环境、社会和文化影响，范围比单独能耗或绿色硬件更广。；design/decisions/structured-label-basis.md#批次授权
- 可持续性议题 / Sustainability Issues：topics/sustainability-issues
  - topics/sustainability-issues：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指体系结构实现决策的环境影响，保留议题含义，不扩成一般可持续发展领域。；design/decisions/structured-label-basis.md#批次授权
- 可视化 / Visualization：topics/visualization
  - topics/visualization：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指把科学或信息数据转成可理解视觉表达的过程，包含感知和认知因素。；design/decisions/structured-label-basis.md#批次授权
- 可访问性与包容性设计 / Accessibility and Inclusive Design：topics/accessibility-and-inclusive-design
  - topics/accessibility-and-inclusive-design：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；可访问性关注不同能力用户能否使用，包容性设计关注更广泛用户差异，保持并列关系。；design/decisions/structured-label-basis.md#批次授权
- 可靠性支持 / Reliability Support：topics/reliability-support
  - topics/reliability-support：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指为可靠传递提供的差错、流量和拥塞控制机制，不是一般设备可靠性评估。；design/decisions/structured-label-basis.md#批次授权
- 命令与控制 / Command and Control：topics/command-and-control, topics/command-and-control-artificial-intelligence
  - topics/command-and-control：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指攻击者与受控系统通信并下达控制指令，不指组织指挥管理。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/command-and-control-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指对手与受控 AI 系统通信并控制系统，不将正常提示交互自动归为攻击。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 团队协作 / Teamwork：topics/teamwork
  - topics/teamwork：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指软件团队角色、沟通和协同工作过程，不仅是多人同时编程。；design/decisions/structured-label-basis.md#批次授权
- 图像 / Figure：forms/figure
  - forms/figure：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按现有范围指照片、插图等非示意性图像；不取数字、人物或笼统的所有附图义，也不并入示意图。；design/decisions/structured-label-basis.md#批次授权
- 图像处理 / Image Processing：topics/image-processing
  - topics/image-processing：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指对图像进行增强、复原、编码和形态学等处理，不等同于完整计算机视觉任务。；design/decisions/structured-label-basis.md#批次授权
- 图形学与互动技术 / Graphics and Interactive Techniques：topics/graphics-and-interactive-techniques
  - topics/graphics-and-interactive-techniques：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；图形学对应建模与渲染，互动技术对应交互、沉浸与物理计算，复用同 ID 试译形式。；design/decisions/structured-label-basis.md#批次授权
- 图表 / Graph：forms/graph
  - forms/graph：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按现有范围指数据的图形化表达，区别于行列表格、结构示意图及图论中的图。；design/decisions/structured-label-basis.md#批次授权
- 基本概念 / Basic Concepts：topics/basic-concepts
  - topics/basic-concepts：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按系统基础归属理解数字与模拟、状态、时序及逻辑门等概念，保留泛称的原有范围。；design/decisions/structured-label-basis.md#批次授权
- 基本概念 / Fundamental Concepts：topics/fundamental-concepts
  - topics/fundamental-concepts：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按图形学与互动技术归属理解，涵盖视觉、颜色和图形输出；领域限定仍由归属与范围承担。；design/decisions/structured-label-basis.md#批次授权
- 基本问题 / Fundamental Issues：topics/fundamental-issues
  - topics/fundamental-issues：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；在人工智能领域指智能行为、智能体与问题特征等根本问题，不等同于所有基础技术。；design/decisions/structured-label-basis.md#批次授权
- 基础数据结构 / Fundamental Data Structures：topics/fundamental-data-structures
  - topics/fundamental-data-structures：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指列表、栈、队列、集合等常用结构及其选择，不合并为数据结构与算法知识单元。；design/decisions/structured-label-basis.md#批次授权
- 基础数据结构与算法 / Foundational Data Structures and Algorithms：topics/foundational-data-structures-and-algorithms
  - topics/foundational-data-structures-and-algorithms：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；基础同时修饰数据结构和算法，包含常用结构、查找与排序。；design/decisions/structured-label-basis.md#批次授权
- 复杂度 / Complexity：topics/complexity
  - topics/complexity：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；在算法分析语境中指时间、空间及可解性问题，不指一般事物的复杂程度。；design/decisions/structured-label-basis.md#批次授权
- 多个行为正确实体间的交互不当 / Improper Interaction Between Multiple Correctly-Behaving Entities：topics/improper-interaction-between-multiple-correctly-behaving-entities
  - topics/improper-interaction-between-multiple-correctly-behaving-entities：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留实体各自行为正确这一条件，弱点产生于实体集成后的交互而非单个实体内部。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 多样性、公平、包容与可访问性 / Diversity, Equity, Inclusion, and Accessibility：topics/diversity-equity-inclusion-and-accessibility
  - topics/diversity-equity-inclusion-and-accessibility：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；逐项保留差异、公平条件、参与包容和可使用性，不将 equity 误作财务股权。；design/decisions/structured-label-basis.md#批次授权
- 存储层次 / Memory Hierarchy：topics/memory-hierarchy
  - topics/memory-hierarchy：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；涵盖缓存、主存与持久存储的层次及局部性，存储比仅指主存的内存更符合范围。；design/decisions/structured-label-basis.md#批次授权
- 安全 / Security：topics/security
  - topics/security：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按计算领域的安全总称理解，涵盖安全编码、工程、密码学与治理，不指金融证券。；design/decisions/structured-label-basis.md#批次授权
- 安全分析、设计与工程 / Security Analysis, Design, and Engineering：topics/security-analysis-design-and-engineering
  - topics/security-analysis-design-and-engineering：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留问题分析、方案设计及工程实现三个方面，安全贯穿整体而不只修饰分析。；design/decisions/structured-label-basis.md#批次授权
- 安全基础 / Foundational Security：topics/foundational-security
  - topics/foundational-security：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指贯穿计算安全的基本属性、概念与思维，和安全总领域的完整范围区分。；design/decisions/structured-label-basis.md#批次授权
- 安全处理器体系结构 / Secure Processor Architectures：topics/secure-processor-architectures
  - topics/secure-processor-architectures：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指支持安全目标的处理器硬件结构，涵盖信任根、内存保护和可信执行。；design/decisions/structured-label-basis.md#批次授权
- 安全政策、法律与计算机犯罪 / Security Policies, Laws and Computer Crimes：topics/security-policies-laws-and-computer-crimes
  - topics/security-policies-laws-and-computer-crimes：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留政策、法律和犯罪三个方面，涵盖计算犯罪行为及相应救济。；design/decisions/structured-label-basis.md#批次授权
- 安全日志记录与错误处理 / Security Logging and Error Handling：topics/security-logging-and-error-handling
  - topics/security-logging-and-error-handling：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；日志记录是安全相关事件的记录活动，错误处理还要求安全失败，保留两个并列方面。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 安全治理 / Security Governance：topics/security-governance
  - topics/security-governance：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指组织目标、风险与策略层面的安全安排，不等同于单项技术防护。；design/decisions/structured-label-basis.md#批次授权
- 安全编码 / Secure Coding：topics/secure-coding
  - topics/secure-coding：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指通过编程实践防止注入、越界等漏洞，编码在此不是数据加密或字符编码。；design/decisions/structured-label-basis.md#批次授权
- 安全编码与体系结构 / Secure Coding and Architecture：topics/secure-coding-and-architecture
  - topics/secure-coding-and-architecture：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留编码实践和体系结构设计两个方面，安全限定整个并列范围。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 安全通信 / Secure Communication：topics/secure-communication
  - topics/secure-communication：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应传输中数据与通信通道的保护，不缩小为某种加密协议。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 实体与物理计算 / Tangible/Physical Computing：topics/tangible-physical-computing
  - topics/tangible-physical-computing：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；实体对应可交互的物理制品，物理计算指计算与物理世界的感知及作用，不是研究物理的数值计算。；design/decisions/structured-label-basis.md#批次授权
- 实时与嵌入式系统 / Real-time and Embedded Systems：topics/real-time-and-embedded-systems
  - topics/real-time-and-embedded-systems：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；分别保留时间约束和嵌入设备的系统特性，二者有交集但不互相等同。；design/decisions/structured-label-basis.md#批次授权
- 实验 / Experiment：forms/experiment
  - forms/experiment：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指按步骤操作并观察结果的活动，不将所有可操作仿真都合并为实验。；design/decisions/structured-label-basis.md#批次授权
- 容错 / Fault tolerance：topics/fault-tolerance
  - topics/fault-tolerance：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指系统在故障条件下保持可用或正确服务的能力及冗余、检测和纠错机制。；design/decisions/structured-label-basis.md#批次授权
- 嵌入式平台 / Embedded Platforms：topics/embedded-platforms
  - topics/embedded-platforms：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指面向嵌入式设备的开发环境及实时、资源和安全约束，不仅是硬件板卡。；design/decisions/structured-label-basis.md#批次授权
- 工具与环境 / Tools and Environments：topics/tools-and-environments
  - topics/tools-and-environments：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按软件工程语境保留开发工具与配套环境，包括版本、发布、测试和文档工具。；design/decisions/structured-label-basis.md#批次授权
- 工程基础 / Engineering Foundations：topics/engineering-foundations
  - topics/engineering-foundations：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指软件工程适用的一般工程原理、统计度量与根因分析等，不限于软件实现技巧。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 并发 / Concurrency：topics/concurrency
  - topics/concurrency：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指线程和进程执行的交错及同步问题，不把并发等同于必须同时执行的并行。；design/decisions/structured-label-basis.md#批次授权
- 并行与分布式程序 / Programs：topics/programs
  - topics/programs：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；用既有领域语境补足泛称，指并行与分布式活动的表达、启动及执行映射。；design/decisions/structured-label-basis.md#批次授权
- 并行与分布式算法 / Algorithms：topics/algorithms
  - topics/algorithms：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；依据归属补足泛称，覆盖多核、集群、云等环境中的算法表达与实现。；design/decisions/structured-label-basis.md#批次授权
- 并行与分布式计算 / Parallel and Distributed Computing：topics/parallel-and-distributed-computing, topics/parallel-and-distributed-computing-foundations-of-programming-languages
  - topics/parallel-and-distributed-computing：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留同时计算与跨系统分布两个方面，涵盖程序、通信、协调和算法。；design/decisions/structured-label-basis.md#批次授权
  - topics/parallel-and-distributed-computing-foundations-of-programming-languages：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留原名，与同名领域使用一致译名；本记录由范围和归属限定语言支持、执行与内存语义。；design/decisions/structured-label-basis.md#批次授权
- 幻灯片 / Slide：forms/slide
  - forms/slide：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指分页展示的演示材料单元，不取滑动动作或显微镜载玻片义。；design/decisions/structured-label-basis.md#批次授权
- 应用与社会影响 / Applications and Societal Impact：topics/applications-and-societal-impact
  - topics/applications-and-societal-impact：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；同时保留人工智能应用案例和部署后的社会影响，不将后者缩为技术性能。；design/decisions/structured-label-basis.md#批次授权
- 应用层 / Application Layer：topics/application-layer
  - topics/application-layer：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应互联网协议族最高层及其用户和支持协议，保留其与 OSI 分层的范围差异。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 异常状况检查或处理不当 / Improper Check or Handling of Exceptional Conditions：topics/improper-check-or-handling-of-exceptional-conditions
  - topics/improper-check-or-handling-of-exceptional-conditions：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留检查与处理两方面；异常状况不限于编程语言抛出的异常对象。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 异构体系结构 / Heterogeneous Architectures：topics/heterogeneous-architectures
  - topics/heterogeneous-architectures：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指不同计算与存储部件组合的体系结构，涵盖 GPU、专用加速器与异构存储。；design/decisions/structured-label-basis.md#批次授权
- 形式化开发方法 / Formal Development Methodologies：topics/formal-development-methodologies
  - topics/formal-development-methodologies：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指使用形式规约、证明和验证进行开发的方法，形式化不表示仅遵循文档格式。；design/decisions/structured-label-basis.md#批次授权
- 形式语义 / Formal Semantics：topics/formal-semantics
  - topics/formal-semantics：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指用数学或逻辑形式规定程序含义，涵盖操作、指称和公理等方法。；design/decisions/structured-label-basis.md#批次授权
- 影响 / Impact：topics/impact, topics/impact-artificial-intelligence
  - topics/impact：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按战术语境指操纵、中断或破坏系统与数据的攻击目标，不是一般影响力或风险度量。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/impact-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按攻击战术理解为操纵、中断、破坏或削弱对 AI 系统和数据的信任。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 性能与能效 / Performance and Energy Efficiency：topics/performance-and-energy-efficiency
  - topics/performance-and-energy-efficiency：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；分别对应执行性能和能源使用效率，涵盖性能与功耗评估及硬件优化。；design/decisions/structured-label-basis.md#批次授权
- 性能评估 / Performance Evaluation：topics/performance-evaluation
  - topics/performance-evaluation：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指通过指标、工作负载、基准和模型测量分析性能，与性能本身区分。；design/decisions/structured-label-basis.md#批次授权
- 感知与计算机视觉 / Perception and Computer Vision：topics/perception-and-computer-vision
  - topics/perception-and-computer-vision：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；感知保留视觉之外的语音与触觉等模态，计算机视觉对应其中的视觉分析。；design/decisions/structured-label-basis.md#批次授权
- 执行 / Execution：topics/execution, topics/execution-artificial-intelligence
  - topics/execution：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；限定对手在本地或远程系统运行受其控制的恶意代码，不指计划执行。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/execution-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指运行嵌入 AI 制品或软件中的恶意代码，不将正常模型推理本身视为此战术。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 持久化 / Persistence：topics/persistence, topics/persistence-artificial-intelligence
  - topics/persistence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指攻击者跨重启或凭据变化保持系统访问，不是数据库持久存储。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/persistence-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指借助 AI 制品或软件保持攻击立足点，不是模型参数的常规保存。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 授权 / Authorization：topics/authorization
  - topics/authorization：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应向获准主体授予访问及最小特权控制，与身份认证区分。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 接口与通信 / Interfacing and Communication：topics/interfacing-and-communication
  - topics/interfacing-and-communication：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；在体系结构语境中指设备接口、输入输出、中断与总线通信，不是人际沟通。；design/decisions/structured-label-basis.md#批次授权
- 控制流管理不足 / Insufficient Control Flow Management：topics/insufficient-control-flow-management
  - topics/insufficient-control-flow-management：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指代码执行路径缺乏充分约束而可被非预期改变，不指业务流程管理。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 搜索 / Search：topics/search
  - topics/search：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按人工智能状态空间与博弈搜索理解，包含启发式搜索，不限于网页检索。；design/decisions/structured-label-basis.md#批次授权
- 操作系统 / Operating Systems：topics/operating-systems
  - topics/operating-systems：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指管理计算机资源并提供程序运行服务的系统软件及其原理。；design/decisions/structured-label-basis.md#批次授权
- 操作系统原理 / Principles of Operating System：topics/principles-of-operating-system
  - topics/principles-of-operating-system：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指操作系统的设计组织、抽象与接口原则，不限于某一具体系统的使用方法。；design/decisions/structured-label-basis.md#批次授权
- 操作系统的作用与目的 / Role and Purpose of Operating Systems：topics/role-and-purpose-of-operating-systems
  - topics/role-and-purpose-of-operating-systems：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；同时保留操作系统的中介作用及提供通用、专门服务的目的。；design/decisions/structured-label-basis.md#批次授权
- 收集 / Collection：topics/collection, topics/collection-artificial-intelligence
  - topics/collection：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指汇集与攻击目标相关的数据；数据尚未必传出受害环境。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/collection-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指汇集 AI 制品与目标相关信息，区别于将其窃取传出环境。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 数字逻辑与数字系统 / Digital Logic and Digital Systems：topics/digital-logic-and-digital-systems
  - topics/digital-logic-and-digital-systems：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；数字对应离散逻辑电路，涵盖组合与时序逻辑及数字硬件系统。；design/decisions/structured-label-basis.md#批次授权
- 数学和统计基础 / Mathematical and Statistical Foundations：topics/mathematical-and-statistical-foundations
  - topics/mathematical-and-statistical-foundations：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；涵盖计算所需的离散数学、概率统计、线性代数与微积分，不指专门研究数学根基的领域。；design/decisions/structured-label-basis.md#批次授权
- 数学基础 / Mathematical Foundations：topics/mathematical-foundations
  - topics/mathematical-foundations：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指支撑软件工程推理与实现的数学知识，不限定为数学哲学中的基础问题。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 数据保护 / Data Protection：topics/data-protection
  - topics/data-protection：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；包含需保护数据的界定和访问保护，不限于个人信息或静态加密。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 数据分析 / Data Analytics：topics/data-analytics
  - topics/data-analytics：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指探索性分析及分类、聚类等数据分析过程，与数据存储管理区分。；design/decisions/structured-label-basis.md#批次授权
- 数据外传 / Exfiltration：topics/exfiltration, topics/exfiltration-artificial-intelligence
  - topics/exfiltration：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指攻击者将目标数据从受害网络窃取传出，与环境内的数据收集区分。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/exfiltration-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指窃取传出 AI 制品或系统信息，范围不局限于训练数据。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 数据安全与隐私 / Data Security and Privacy：topics/data-security-and-privacy
  - topics/data-security-and-privacy：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；分别保留攻击防护和个人信息使用保护，二者相关但不是同一属性。；design/decisions/structured-label-basis.md#批次授权
- 数据库管理系统内部机制 / DBMS Internals：topics/dbms-internals
  - topics/dbms-internals：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；内部机制对应缓冲、事务、并发控制与恢复，展开 DBMS 但不扩充概念范围。；design/decisions/structured-label-basis.md#批次授权
- 数据库系统核心概念 / Core Database System Concepts：topics/core-database-system-concepts
  - topics/core-database-system-concepts：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指数据库系统目的、组成、核心功能与数据独立性等概念，保留系统层范围。；design/decisions/structured-label-basis.md#批次授权
- 数据建模 / Data Modeling：topics/data-modeling
  - topics/data-modeling：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指以关系、概念和半结构化等模型描述数据及其关系，不限于物理存储设计。；design/decisions/structured-label-basis.md#批次授权
- 数据的作用与生命周期 / The Role of Data and the Data Life Cycle：topics/the-role-of-data-and-the-data-life-cycle
  - topics/the-role-of-data-and-the-data-life-cycle：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留数据的作用及创建至销毁的阶段过程，生命周期不只指存储时长。；design/decisions/structured-label-basis.md#批次授权
- 文件处理 / File Handling：topics/file-handling
  - topics/file-handling：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；涵盖文件接收、访问、存储和使用中的处理活动，不缩小为文件上传。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 文件系统接口与实现 / File Systems API and Implementation：topics/file-systems-api-and-implementation
  - topics/file-systems-api-and-implementation：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；API 对应程序调用接口，保留接口及内部文件组织实现两部分，不仅指文件格式。；design/decisions/structured-label-basis.md#批次授权
- 新兴主题 / Emerging Topics：topics/emerging-topics
  - topics/emerging-topics：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按网络领域理解新出现或发展的主题，保留开放主题集合的原名而不固化其成员。；design/decisions/structured-label-basis.md#批次授权
- 智能体与认知系统 / Agents and Cognitive Systems：topics/agents-and-cognitive-systems
  - topics/agents-and-cognitive-systems：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；智能体对应可感知、行动或作决策的人工智能实体，涵盖软件及多智能体，不指人类代理商。；design/decisions/structured-label-basis.md#批次授权
- 机器人学 / Robotics：topics/robotics
  - topics/robotics：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指机器人感知、定位、运动与控制的研究领域，不只是机器人设备。；design/decisions/structured-label-basis.md#批次授权
- 机器人平台 / Robot Platforms：topics/robot-platforms
  - topics/robot-platforms：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指机器人设备及其软件环境、接口与库，区别于机器人学总领域。；design/decisions/structured-label-basis.md#批次授权
- 机器级数据表示 / Machine-Level Data Representation：topics/machine-level-data-representation
  - topics/machine-level-data-representation：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指位、字节、机器字和数据编码，保留机器级限定，不等同于数据库建模。；design/decisions/structured-label-basis.md#批次授权
- 权限提升 / Privilege Escalation：topics/privilege-escalation, topics/privilege-escalation-artificial-intelligence
  - topics/privilege-escalation：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指从现有访问能力取得更高级别权限，不等同于初始访问。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/privilege-escalation-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指在 AI 环境取得更高级别权限，不等同于增加模型能力。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 查询处理 / Query Processing：topics/query-processing
  - topics/query-processing：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指数据库执行、优化和调优查询的机制，与用户构造查询语句区分。；design/decisions/structured-label-basis.md#批次授权
- 查询构造 / Query Construction：topics/query-construction
  - topics/query-construction：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指用 SQL 等语言表达和编写查询，与数据库内部执行查询的查询处理区分。；design/decisions/structured-label-basis.md#批次授权
- 概率表示与推理 / Probabilistic Representation and Reasoning：topics/probabilistic-representation-and-reasoning
  - topics/probabilistic-representation-and-reasoning：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指概率式知识表示和基于概率的推理与决策，保留不确定性处理的含义。；design/decisions/structured-label-basis.md#批次授权
- 横向移动 / Lateral Movement：topics/lateral-movement, topics/lateral-movement-artificial-intelligence
  - topics/lateral-movement：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指进入并控制同一网络环境中的其他系统，不等同于在当前系统提升权限。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/lateral-movement-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指在 AI 环境中访问并控制其他系统，不指模型跨任务迁移。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 比较错误 / Incorrect Comparison：topics/incorrect-comparison
  - topics/incorrect-comparison：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指安全相关语境中对实体的比较不正确，与一般数值计算错误区分。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 汇编级机器组织 / Assembly Level Machine Organization：topics/assembly-level-machine-organization
  - topics/assembly-level-machine-organization：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；以汇编可见的指令与执行结构理解机器组织，涵盖控制单元、指令周期和指令集。；design/decisions/structured-label-basis.md#批次授权
- 沉浸 / Immersion：topics/immersion
  - topics/immersion：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指虚拟、增强和混合现实等技术提供的沉浸程度，与主观临场感保持区别。；design/decisions/structured-label-basis.md#批次授权
- 沟通 / Communication：topics/communication-society-ethics-and-the-profession
  - topics/communication-society-ethics-and-the-profession：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指团队、客户和公众之间的口头、书面及技术沟通，与机器间通信区分。；design/decisions/structured-label-basis.md#批次授权
- 渲染应用与技术 / Applied Rendering and Techniques：topics/applied-rendering-and-techniques
  - topics/applied-rendering-and-techniques：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应渲染的应用和相关技术，范围包括场景、相机、投影与光照，不将 applied 解释成独立应用软件。；design/decisions/structured-label-basis.md#批次授权
- 游戏平台 / Game Platforms：topics/game-platforms
  - topics/game-platforms：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指游戏开发运行环境、引擎与工具，按既有范围不只理解为游戏分发商店。；design/decisions/structured-label-basis.md#批次授权
- 用户理解及个体目标与人际交互 / Understanding the User: Individual goals and interactions with others：topics/understanding-the-user-individual-goals-and-interactions-with-others
  - topics/understanding-the-user-individual-goals-and-interactions-with-others：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留原名的用户理解、个体目标及与他人交互三层信息，范围涵盖用户特征与协作。；design/decisions/structured-label-basis.md#批次授权
- 着色与高级渲染 / Shading and Advanced Rendering：topics/shading-and-advanced-rendering
  - topics/shading-and-advanced-rendering：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；着色对应表面光照等计算，渲染对应更广的成像过程，保留两者范围差别。；design/decisions/structured-label-basis.md#批次授权
- 知识产权 / Intellectual Property：topics/intellectual-property
  - topics/intellectual-property：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指智力成果相关权利与许可、作者身份等议题，不将其缩成版权一种权利。；design/decisions/structured-label-basis.md#批次授权
- 知识表示与推理基础 / Fundamental Knowledge Representation and Reasoning：topics/fundamental-knowledge-representation-and-reasoning
  - topics/fundamental-knowledge-representation-and-reasoning：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；基础覆盖知识表示及推理两方面，范围含贝叶斯推理、概率与决策。；design/decisions/structured-label-basis.md#批次授权
- 示意图 / Diagram：forms/diagram
  - forms/diagram：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指用线条与符号表达结构或过程的图，区别于照片插图类图像及数据关系图表。；design/decisions/structured-label-basis.md#批次授权
- 社会、伦理与职业 / Society, Ethics, and the Profession：topics/society-ethics-and-the-profession, topics/society-ethics-and-the-profession-algorithmic-foundations, topics/society-ethics-and-the-profession-data-management, topics/society-ethics-and-the-profession-foundations-of-programming-languages, topics/society-ethics-and-the-profession-graphics-and-interactive-techniques, topics/society-ethics-and-the-profession-human-computer-interaction, topics/society-ethics-and-the-profession-operating-systems, topics/society-ethics-and-the-profession-security, topics/society-ethics-and-the-profession-software-development-fundamentals, topics/society-ethics-and-the-profession-systems-fundamentals
  - topics/society-ethics-and-the-profession：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；职业指计算专业群体及其规范与责任，保留社会、伦理和职业三个方面。；design/decisions/structured-label-basis.md#批次授权
  - topics/society-ethics-and-the-profession-algorithmic-foundations：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；复用相同英文的统一译名；本记录以算法公平、隐私、透明与经济环境影响为范围，领域差别由归属与范围保留。；design/decisions/structured-label-basis.md#批次授权
  - topics/society-ethics-and-the-profession-data-management：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；复用相同英文的统一译名；本记录以数据隐私、归属、托管、用途与溯源为范围，领域差别由归属与范围保留。；design/decisions/structured-label-basis.md#批次授权
  - topics/society-ethics-and-the-profession-foundations-of-programming-languages：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；复用相同英文的统一译名；本记录以语言设计的人因、语言中心倾向、可访问性与包容性为范围，领域差别由归属与范围保留。；design/decisions/structured-label-basis.md#批次授权
  - topics/society-ethics-and-the-profession-graphics-and-interactive-techniques：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；复用相同英文的统一译名；本记录以图形与互动应用的可访问性、隐私及知识产权为范围，领域差别由归属与范围保留。；design/decisions/structured-label-basis.md#批次授权
  - topics/society-ethics-and-the-profession-human-computer-interaction：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；复用相同英文的统一译名；本记录以设计问责、用户参与、可访问性与设计影响为范围，领域差别由归属与范围保留。；design/decisions/structured-label-basis.md#批次授权
  - topics/society-ethics-and-the-profession-operating-systems：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；复用相同英文的统一译名；本记录以开源及操作系统维护终止的影响为范围，领域差别由归属与范围保留。；design/decisions/structured-label-basis.md#批次授权
  - topics/society-ethics-and-the-profession-security：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；复用相同英文的统一译名；本记录以隐私实践、安全失效的社会影响与职业责任为范围，领域差别由归属与范围保留。；design/decisions/structured-label-basis.md#批次授权
  - topics/society-ethics-and-the-profession-software-development-fundamentals：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；复用相同英文的统一译名；本记录以程序知识产权、学术诚信与代码责任为范围，领域差别由归属与范围保留。；design/decisions/structured-label-basis.md#批次授权
  - topics/society-ethics-and-the-profession-systems-fundamentals：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；复用相同英文的统一译名；本记录以计算机系统的知识产权、软件许可与计算机犯罪为范围，领域差别由归属与范围保留。；design/decisions/structured-label-basis.md#批次授权
- 社会情境 / Social Context：topics/social-context
  - topics/social-context：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指计算技术所处及影响的社会环境与关系，包含对个人和群体的作用。；design/decisions/structured-label-basis.md#批次授权
- 移动平台 / Mobile Platforms：topics/mobile-platforms
  - topics/mobile-platforms：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指移动设备应用开发环境及其约束和异步计算，不指移动网络本身。；design/decisions/structured-label-basis.md#批次授权
- 移动性 / Mobility：topics/mobility
  - topics/mobility：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；在网络语境中指移动设备与无线网络通信的相关能力，不指社会流动或软件移植。；design/decisions/structured-label-basis.md#批次授权
- 程序分析与分析器 / Program Analysis and Analyzers：topics/program-analysis-and-analyzers
  - topics/program-analysis-and-analyzers：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；同时保留分析方法和执行分析的工具，涵盖控制流与数据流等程序性质。；design/decisions/structured-label-basis.md#批次授权
- 程序抽象与表示 / Program Abstraction and Representation：topics/program-abstraction-and-representation
  - topics/program-abstraction-and-representation：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指语言构成、程序抽象以及 BNF 等表示方式，保留抽象和表示两个层面。；design/decisions/structured-label-basis.md#批次授权
- 程序设计基本概念与实践 / Fundamental Programming Concepts and Practices：topics/fundamental-programming-concepts-and-practices
  - topics/fundamental-programming-concepts-and-practices：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；基本同时限定概念与实践，涵盖变量、状态、表达式与基本控制构造。；design/decisions/structured-label-basis.md#批次授权
- 程序设计语言基础 / Foundations of Programming Languages：topics/foundations-of-programming-languages
  - topics/foundations-of-programming-languages：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；涵盖语言范式、类型、语义与实现的共同基础，不限于某门语言的入门语法。；design/decisions/structured-label-basis.md#批次授权
- 程序设计语言的设计原则 / Design Principles of Programming Languages：topics/design-principles-of-programming-languages
  - topics/design-principles-of-programming-languages：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指语言自身的设计准则及互操作、可移植性等要求，与用语言设计应用区分。；design/decisions/structured-label-basis.md#批次授权
- 算法 / Algorithms：topics/algorithms-software-development-fundamentals
  - topics/algorithms-software-development-fundamentals：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按软件开发基础归属理解常见算法及效率入门，保留原名并由范围区分并行与分布式算法。；design/decisions/structured-label-basis.md#批次授权
- 算法基础 / Algorithmic Foundations：topics/algorithmic-foundations
  - topics/algorithmic-foundations：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；涵盖数据结构、算法策略、复杂度与计算模型，基础限定整个算法知识领域。；design/decisions/structured-label-basis.md#批次授权
- 算法策略 / Algorithmic Strategies：topics/algorithmic-strategies
  - topics/algorithmic-strategies：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指分治、动态规划、贪心和回溯等求解策略，保持其高于具体算法实现的范围。；design/decisions/structured-label-basis.md#批次授权
- 类型系统 / Type Systems：topics/type-systems
  - topics/type-systems：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指语言中类型规则及其对值、变量和运算的约束，不是普通对象分类体系。；design/decisions/structured-label-basis.md#批次授权
- 系统可靠性 / System Reliability：topics/system-reliability
  - topics/system-reliability：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指系统避免失效的能力及冗余等实现途径，保留系统整体范围而非只软件故障。；design/decisions/structured-label-basis.md#批次授权
- 系统基础 / Systems Fundamentals：topics/systems-fundamentals
  - topics/systems-fundamentals：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指计算机系统的共同原理，包括资源、性能、可靠性、安全和设计。；design/decisions/structured-label-basis.md#批次授权
- 系统安全 / System Security：topics/system-security
  - topics/system-security：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指计算机系统面临的攻击与防护，包括拒绝服务和窃听，不等同于可靠性。；design/decisions/structured-label-basis.md#批次授权
- 系统性能 / System Performance：topics/system-performance
  - topics/system-performance：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指计算机系统的延迟、缓存与存储层次等性能因素，与性能的测量评估方法区分。；design/decisions/structured-label-basis.md#批次授权
- 系统执行与内存模型 / Systems Execution and Memory Model：topics/systems-execution-and-memory-model
  - topics/systems-execution-and-memory-model：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留执行和内存模型两部分，涵盖栈堆、寻址及运行时表示。；design/decisions/structured-label-basis.md#批次授权
- 系统设计 / System Design：topics/system-design, topics/system-design-systems-fundamentals
  - topics/system-design：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；在人机交互归属下指原型、界面和交互等系统设计，领域限定由既有范围承担。；design/decisions/structured-label-basis.md#批次授权
  - topics/system-design-systems-fundamentals：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按系统基础归属指活性、健壮性、扩展性与安全等设计准则，与人机交互同名项由范围区分。；design/decisions/structured-label-basis.md#批次授权
- 索引 / Index：forms/index
  - forms/index：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指以条目导向内容位置的检索形式，不取指标或数据库索引技术的专门义。；design/decisions/structured-label-basis.md#批次授权
- 练习 / Exercise：forms/exercise
  - forms/exercise：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指供学习者完成的任务或题目，不隐含考试评分或身体锻炼义。；design/decisions/structured-label-basis.md#批次授权
- 编码与净化 / Encoding and Sanitization：topics/encoding-and-sanitization
  - topics/encoding-and-sanitization：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；编码指面向输出上下文的安全编码；净化指处理不可信数据中的危险内容，保留两类措施的区别。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 编码规范遵循不当 / Improper Adherence to Coding Standards：topics/improper-adherence-to-coding-standards
  - topics/improper-adherence-to-coding-standards：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指未按适用编码规则开发而引入或加重弱点，不是对规范本身质量的判断。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 编译器语义分析 / Compiler Semantic Analysis：topics/compiler-semantic-analysis
  - topics/compiler-semantic-analysis：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指编译器对作用域、绑定和静态语义等的分析，与语法结构分析区分。；design/decisions/structured-label-basis.md#批次授权
- 网络与通信 / Networking and Communication：topics/networking-and-communication
  - topics/networking-and-communication：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；同时涵盖计算机网络组织与数据通信，包括应用、路由、单跳通信与移动性。；design/decisions/structured-label-basis.md#批次授权
- 网络基础 / Fundamentals：topics/fundamentals
  - topics/fundamentals：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；以网络归属补足泛称，涵盖互联网组织、交换与分层等基础内容。；design/decisions/structured-label-basis.md#批次授权
- 网络安全 / Network Security：topics/network-security
  - topics/network-security：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指网络特有的威胁、攻击和防护机制，保持网络层面的范围。；design/decisions/structured-label-basis.md#批次授权
- 网络应用 / Networked Applications：topics/networked-applications
  - topics/networked-applications：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指依赖网络通信的应用及其分布式范式，不限于浏览器内的 Web 应用。；design/decisions/structured-label-basis.md#批次授权
- 网际层 / Internet Layer：topics/internet-layer
  - topics/internet-layer：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应以 IP 实现跨网络主机间数据传递的层，不将其改为 OSI 网络层概念。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 考试 / Exam：forms/exam
  - forms/exam：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指有评分的测验活动，与一般练习或收集信息的问卷区分。；design/decisions/structured-label-basis.md#批次授权
- 职业伦理 / Professional Ethics：topics/professional-ethics
  - topics/professional-ethics：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指计算专业人士的责任、规范与职业行为，不是个人偏好或一般社会伦理的全部。；design/decisions/structured-label-basis.md#批次授权
- 自包含令牌 / Self-contained Tokens：topics/self-contained-tokens
  - topics/self-contained-tokens：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；令牌自身携带供接收方判断的声明，仍需验证完整性和适用上下文。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 自我评估 / Self assessment：forms/self-assessment
  - forms/self-assessment：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指学习者自行评价掌握程度的活动，保留自我判断主体，而非由外部组织的考试。；design/decisions/structured-label-basis.md#批次授权
- 虚拟化 / Virtualization：topics/virtualization
  - topics/virtualization：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指以抽象和隔离提供虚拟资源或执行环境，涵盖容器、虚拟机和虚拟设备。；design/decisions/structured-label-basis.md#批次授权
- 表格 / Table：forms/table
  - forms/table：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指按行列组织数据的呈现形式，与图形化数据图表区分。；design/decisions/structured-label-basis.md#批次授权
- 规划 / Planning：topics/planning
  - topics/planning：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指人工智能中的行动序列与状态空间规划，不是项目管理的工作计划。；design/decisions/structured-label-basis.md#批次授权
- 计算史 / Computing History：topics/computing-history
  - topics/computing-history：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；涵盖计算硬件、软件、人和组织的发展，也包含前数字时代，不限于现代计算机产品史。；design/decisions/structured-label-basis.md#批次授权
- 计算基础 / Computing Foundations：topics/computing-foundations
  - topics/computing-foundations：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指软件工程所需的计算机科学基础，不取基础算术或日常计算机操作之义。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 计算机动画 / Computer Animation：topics/computer-animation
  - topics/computer-animation：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指用计算机生成随时间变化的运动表现，涵盖关键帧、运动学和动作捕捉。；design/decisions/structured-label-basis.md#批次授权
- 计算机系统概览 / Overview of Computer Systems：topics/overview-of-computer-systems
  - topics/overview-of-computer-systems：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指从基本硬件构件到软件抽象的总体介绍，概览表达原有内容层次。；design/decisions/structured-label-basis.md#批次授权
- 计算模型与形式语言 / Computational Models and Formal Languages：topics/computational-models-and-formal-languages
  - topics/computational-models-and-formal-languages：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应自动机、文法、可判定性和计算能力的形式研究，不指自然语言文体。；design/decisions/structured-label-basis.md#批次授权
- 计算经济 / Economies of Computing：topics/economies-of-computing
  - topics/economies-of-computing：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指计算领域的市场、定价、资源获取和劳动力等经济形态，不指节约运算量或仅算法效率。；design/decisions/structured-label-basis.md#批次授权
- 计算错误 / Incorrect Calculation：topics/incorrect-calculation
  - topics/incorrect-calculation：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指运算结果错误或非预期，并可能影响安全决策和资源管理。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 讲授 / Lecture：forms/lecture
  - forms/lecture：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指面向听众讲解的教学活动，形式可承载讲授内容，不限定必须是书面讲义。；design/decisions/structured-label-basis.md#批次授权
- 设备管理 / Device management：topics/device-management
  - topics/device-management：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指操作系统对输入输出设备、接口与驱动的管理，不指办公设备台账。；design/decisions/structured-label-basis.md#批次授权
- 设计中的问责与责任 / Accountability and Responsibility in Design：topics/accountability-and-responsibility-in-design
  - topics/accountability-and-responsibility-in-design：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；问责对应对设计结果作出解释并接受追究，责任对应应承担的义务，保留两者区别。；design/decisions/structured-label-basis.md#批次授权
- 设计评估 / Evaluating the Design：topics/evaluating-the-design
  - topics/evaluating-the-design：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指对设计开展用户研究、定量分析与影响评价，不仅指评定视觉美观。；design/decisions/structured-label-basis.md#批次授权
- 访问控制不当 / Improper Access Control：topics/improper-access-control
  - topics/improper-access-control：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；包含未实施和错误实施访问限制两种情况，不仅指权限设置过宽。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 评估 / Evaluation：topics/evaluation
  - topics/evaluation：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按并行与分布式领域理解正确性要求和性能的评估，不限于运行速度。；design/decisions/structured-label-basis.md#批次授权
- 语法分析 / Syntax Analysis：topics/syntax-analysis
  - topics/syntax-analysis：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按编译领域理解程序文本的词法与语法结构分析，不涉及自然语言句法教学。；design/decisions/structured-label-basis.md#批次授权
- 语言翻译与执行 / Language Translation and Execution：topics/language-translation-and-execution
  - topics/language-translation-and-execution：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；翻译指编译、解释和转译等程序语言处理，执行指运行模型，不是自然语言翻译。；design/decisions/structured-label-basis.md#批次授权
- 语言语用 / Language Pragmatics：topics/language-pragmatics
  - topics/language-pragmatics：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；在程序设计语言语境中指语言使用及设计选择的实际影响，非自然语言会话语用学。；design/decisions/structured-label-basis.md#批次授权
- 调度 / Scheduling：topics/scheduling
  - topics/scheduling：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指操作系统向进程或线程分配执行机会的策略，非一般项目排期。；design/decisions/structured-label-basis.md#批次授权
- 资源开发 / Resource Development：topics/resource-development, topics/resource-development-artificial-intelligence
  - topics/resource-development：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指创建、购买或窃取支持攻击行动的资源，不限于开发软件或编写攻击代码。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
  - topics/resource-development-artificial-intelligence：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指建立支持针对 AI 系统行动的资源，不将其理解为正常模型开发。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 资源生命周期控制不当 / Improper Control of a Resource Through its Lifetime：topics/improper-control-of-a-resource-through-its-lifetime
  - topics/improper-control-of-a-resource-through-its-lifetime：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；涵盖资源创建、使用和释放全过程的控制缺失或错误，不缩小为资源泄漏。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 资源管理 / Resource Management：topics/resource-management
  - topics/resource-management：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指处理器、内存、磁盘和带宽等系统资源的分配与调度，不指项目人力资源。；design/decisions/structured-label-basis.md#批次授权
- 路由与转发 / Routing and Forwarding：topics/routing-and-forwarding
  - topics/routing-and-forwarding：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；路由对应确定路径，转发对应按表处理数据包，保留控制与实际传递的区别。；design/decisions/structured-label-basis.md#批次授权
- 身份认证 / Authentication：topics/authentication
  - topics/authentication：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指确认个人或设备的身份真实性，与决定其访问权限的授权区分。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件体系结构 / Software Architecture：topics/software-architecture
  - topics/software-architecture：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应软件结构、相关表示与工作产品及其分析评估，不指硬件体系结构。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件可靠性 / Software Reliability：topics/software-reliability
  - topics/software-reliability：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指软件在规定条件下避免失效的程度及其度量，与安全和可用性保持区别。；design/decisions/structured-label-basis.md#批次授权
- 软件安全 / Software Security：topics/software-security
  - topics/software-security：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；在软件语境中指抵御误用和恶意活动的安全，不将其等同于可靠性或一般故障安全。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件工程模型与方法 / Software Engineering Models and Methods：topics/software-engineering-models-and-methods
  - topics/software-engineering-models-and-methods：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留模型和方法两个方面，着重软件工程活动的系统性与可重复性。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件工程管理 / Software Engineering Management：topics/software-engineering-management
  - topics/software-engineering-management：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应软件项目规划、估算、控制、协调和风险管理，区别于系统技术运维。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件工程经济学 / Software Engineering Economics：topics/software-engineering-economics
  - topics/software-engineering-economics：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指软件相关成本、价值及业务战略目标下的经济决策，不限于项目预算管理。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件工程职业实践 / Software Engineering Professional Practice：topics/software-engineering-professional-practice
  - topics/software-engineering-professional-practice：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应以专业、负责方式从业所需的知识、技能和态度，不限于技术实操训练。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件工程过程 / Software Engineering Process：topics/software-engineering-process
  - topics/software-engineering-process：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指组织软件工程活动的过程、生命周期和评估，不缩小为具体操作步骤。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件工程运维 / Software Engineering Operations：topics/software-engineering-operations
  - topics/software-engineering-operations：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应软件部署、运行与支持及稳定性维护，区别于项目规划和组织管理。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件开发基础 / Software Development Fundamentals：topics/software-development-fundamentals
  - topics/software-development-fundamentals：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；涵盖编程概念、基础数据结构、算法和开发实践，不仅是编程语法。；design/decisions/structured-label-basis.md#批次授权
- 软件开发实践 / Software Development Practices：topics/software-development-practices
  - topics/software-development-practices：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指测试、调试、可读性和文档等开发活动，不限于编写功能代码。；design/decisions/structured-label-basis.md#批次授权
- 软件测试 / Software Testing：topics/software-testing
  - topics/software-testing：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指通过选定测试用例动态确认行为，区别于仅靠静态审查的确认活动。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件维护 / Software Maintenance：topics/software-maintenance
  - topics/software-maintenance：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指交付后因需求等变化开展的软件演化活动，不与运行支持完全等同。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件设计 / Software Design：topics/software-design
  - topics/software-design：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指软件结构、组件和接口等设计，涵盖架构及程序层次，不等同于界面视觉设计。；design/decisions/structured-label-basis.md#批次授权
- 软件质量 / Software Quality：topics/software-quality
  - topics/software-quality：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；包含质量概念及质量管理、保证和控制，不等同于测试通过率。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件配置管理 / Software Configuration Management：topics/software-configuration-management
  - topics/software-configuration-management：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应全生命周期配置项及其完整性和正确性控制，不限于编辑配置文件。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件需求 / Software Requirements：topics/software-requirements
  - topics/software-requirements：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；涵盖需要和约束的表达以及获取、分析、规约、确认与管理，不限于需求文档。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 软件验证与确认 / Software Verification and Validation：topics/software-verification-and-validation
  - topics/software-verification-and-validation：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；验证关注满足规定要求，确认关注满足预期用途，保留两种判断而不统称测试。；design/decisions/structured-label-basis.md#批次授权
- 运行时行为与系统 / Run-time Behavior and Systems：topics/run-time-behavior-and-systems
  - topics/run-time-behavior-and-systems：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；运行时同时限定程序行为和支撑系统，涵盖活动记录、方法查找与对象分配。；design/decisions/structured-label-basis.md#批次授权
- 进程模型 / Process Model：topics/process-model
  - topics/process-model：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指进程的抽象、内存布局、加载与切换，process 在此不是软件开发过程。；design/decisions/structured-label-basis.md#批次授权
- 通信 / Communication：topics/communication
  - topics/communication：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指并行和分布式执行实体之间的信息传递，与职业领域的人际沟通区分。；design/decisions/structured-label-basis.md#批次授权
- 速查表 / Cheat sheet：forms/cheat-sheet
  - forms/cheat-sheet：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指供快速参考的简明笔记集，按现有范围不取作弊用小抄义，也不要求一定按行列排版。；design/decisions/structured-label-basis.md#批次授权
- 逻辑程序设计 / Logic Programming：topics/logic-programming
  - topics/logic-programming：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应以事实、规则和目标表达计算并通过推理求解的范式，不是泛指程序逻辑。；design/decisions/structured-label-basis.md#批次授权
- 逻辑表示与推理 / Logical Representation and Reasoning：topics/logical-representation-and-reasoning
  - topics/logical-representation-and-reasoning：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指以命题、谓词等逻辑表示知识并推导结论，与概率方法区分。；design/decisions/structured-label-basis.md#批次授权
- 配置 / Configuration：topics/configuration
  - topics/configuration：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指应用开发、构建和部署中的配置安全要求，不扩大为组织配置管理过程。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 重构与代码演化 / Refactoring and Code Evolution：topics/refactoring-and-code-evolution
  - topics/refactoring-and-code-evolution：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；保留行为保持的结构调整与代码持续变化两个方面，涵盖兼容和版本化问题。；design/decisions/structured-label-basis.md#批次授权
- 量子体系结构 / Quantum Architectures：topics/quantum-architectures
  - topics/quantum-architectures：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；按体系结构领域中的量子计算知识单元理解，涵盖量子门与量子信息操作。；design/decisions/structured-label-basis.md#批次授权
- 链路层 / Link Layer：topics/link-layer
  - topics/link-layer：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指与直接相连网络通信且依赖具体网络技术的层，不擅自改为 OSI 数据链路层。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 问卷 / Questionnaire：forms/questionnaire
  - forms/questionnaire：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指供填答的一组问题，主要用于收集回答，不自动等同于评分考试。；design/decisions/structured-label-basis.md#批次授权
- 问题陈述 / Problem statement：forms/problem-statement
  - forms/problem-statement：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指给出待解决问题的表述，形式本身不提供解法，也不强加评分要求。；design/decisions/structured-label-basis.md#批次授权
- 防御削弱 / Defense Impairment：topics/defense-impairment
  - topics/defense-impairment：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指削弱、禁用或破坏防御机制及其可信性，区别于仅隐藏攻击活动。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 防御规避 / Defense Evasion：topics/defense-evasion
  - topics/defense-evasion：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指避开 AI 赋能安全软件的检测，不等同于破坏防御机制或一般模型性能退化。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 隐私与公民自由 / Privacy and Civil Liberties：topics/privacy-and-civil-liberties
  - topics/privacy-and-civil-liberties：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；同时保留个人信息与隐私保护及公民自由两方面，不把权利议题缩为加密技术。；design/decisions/structured-label-basis.md#批次授权
- 隐蔽 / Stealth：topics/stealth
  - topics/stealth：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指隐藏行为或混入正常活动以降低检测概率，区别于主动削弱安全机制。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 面向切面程序设计 / Aspect-Oriented Programming：topics/aspect-oriented-programming
  - topics/aspect-oriented-programming：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；切面对应横切关注点及连接点、切点、通知和织入机制，不指一般几何方面。；design/decisions/structured-label-basis.md#批次授权
- 验证与业务逻辑 / Validation and Business Logic：topics/validation-and-business-logic
  - topics/validation-and-business-logic：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；验证指检查输入是否符合业务和功能约束；业务逻辑还覆盖流程顺序、绕过与自动化滥用。模型知识判断，外部用法未核实。；design/decisions/structured-label-basis.md#批次授权
- 高级文件系统 / Advanced File systems：topics/advanced-file-systems
  - topics/advanced-file-systems：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；对应深入的文件系统结构与实现，包括日志、分布式和加密文件系统，高级表示内容层次。；design/decisions/structured-label-basis.md#批次授权
- 高级程序设计构造 / Advanced Programming Constructs：topics/advanced-programming-constructs
  - topics/advanced-programming-constructs：模型知识 · 第 5 级，外部用法未核实；gpt-6-astra；2026-09-05；指封装、求值与控制抽象等语言构造，不将高级理解为高性能或高级职级。；design/decisions/structured-label-basis.md#批次授权
