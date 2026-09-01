# Application Profile

## 定义

Application Profile 是为特定应用选择已有 `metadata term`、规定使用约束并说明应用语境的一组文档。它可以组合多个词汇表中的 `term`，但不改写来源定义；例如，本库可以沿用 Dublin Core 的 `subject`，再规定该字段必须引用正式主题词表，而不重新定义 `subject` 的语义。

[Dublin Core™ Application Profile Guidelines](https://www.dublincore.org/specifications/dublin-core/application-profile-guidelines/) 给出选择与约束 `term` 的早期定义，[The Singapore Framework for Dublin Core™ Application Profiles](https://www.dublincore.org/specifications/dublin-core/singapore-framework/) 则把功能范围、模型、字段约束、使用说明和编码说明组织成一组应用文档。

## 解决的问题

Application Profile 让通用 metadata 在具体应用中取得可执行的边界。

| 问题 | 本库例子 | 处理方式 |
|---|---|---|
| 通用 `term` 的适用范围太宽 | Dublin Core 没有替本库决定哪些内容单元必须有 `subject` | 说明功能范围，并规定字段的必填性与基数 |
| 字段和值的来源容易混在一起 | `subject` 是 metadata 字段，字段值来自正式主题词表 | 分别引用 metadata vocabulary 与受控词表 |
| 语义规则容易被载体细节取代 | 同一字段可以进入 Obsidian properties 或 DITA prolog | 先固定应用约束，再由 target 规定表示方式 |
| 创建者不知道怎样选择与填写值 | 多个可用字段都可能描述资源关系 | 用使用指南解释选择条件与填写方式 |

本库采用这一方法，是为了从应用需求导出约束，而不是让某个输出格式决定内容模型。

## 组成部分

Singapore Framework 与后续 Profile Guidelines 把不同职责分给不同文档组件。下表沿用这些历史材料的职责边界，不把组件名称当作本库已经取得的符合性身份。

| 组件 | 回答的问题 | 本库例子 |
|---|---|---|
| `Functional Requirements` | 应用支持和排除哪些功能 | 是否需要按正式主题浏览内容 |
| `Domain Model` | 应用描述哪些对象及其关系 | 内容单元、主题概念与来源怎样关联 |
| `Description Set Profile` | 哪些 property 可用，值和基数受什么约束 | `subject` 必须引用正式主题词表中的概念 |
| `Usage Guidelines` | 创建者为何以及怎样使用 property | 何时使用 `subject`，怎样选择对应概念 |
| `Encoding Syntax Guidelines` | 整条 metadata record 怎样进入具体机器语法 | target 怎样安排 YAML、XML 或其他表示 |

功能范围先界定应用目的，模型再界定对象，字段约束和使用说明规定应用规则，编码说明最后处理具体表示。这一顺序避免用文件格式反推字段语义。

## 相邻概念

这些对象回答不同问题，不能因都涉及字段或编码而互换。

| 对象 | 职责 | 反例 |
|---|---|---|
| `Application Profile` | 规定一个应用怎样选择、约束、使用和编码 metadata | 不负责在两个独立 schema 之间建立对应 |
| `crosswalk` | 记录两个或更多独立 metadata standard、schema 或 profile 的对应 | 本库把一个 property 放进某个 target field，不构成 `crosswalk` |
| `field binding` | 把既定 property 绑定到一个 target field、路径或表示位置 | 把 `subject` 写入 Obsidian 的某个 property，只是应用内部表示，不是完整的 `Application Profile` |
| `Encoding Syntax Guidelines` | 规定整条 metadata record 的具体机器语法 | 它不只规定单个 field，也不规定单个字符串的 datatype |
| `Syntax Encoding Scheme` | 规定一组字符串到一组 resource 的映射规则 | 日期字符串的解释规则不是 YAML、Markdown、目录布局或整条 record 的编码方式 |

因此，本库把 application binding 留在具体 target 中；只有两个独立 metadata schema 或 profile 之间的对应才进入 `crosswalk` 的职责范围。

## 项目分层

本库把 metadata 应用拆成三个可以独立核对的层次。

| 层次 | 职责 | `subject` 例子 |
|---|---|---|
| 应用无关模型 | 保存字段语义、对象关系和正式词表身份 | `subject` 继续表示资源主题，值引用正式主题词表 |
| 应用约束 | 规定功能范围、字段基数、值来源和使用条件 | 某类内容必须至少关联一个正式主题概念 |
| 具体表示 | 由每个 target 规定 field、路径、syntax 和 binding | Obsidian 可用 YAML property，DITA 可用 prolog 表达同一字段 |

具体表示可以随 target 改变，但不能反向改写应用约束或应用无关模型。本库采用这一分层不产生 DCAP、DCAM 或 DCTAP conformance。

## 适用边界

Application Profile 只取得选择、约束和说明已有 `metadata term` 的职责，不取得改写来源语义、批准新 designation 或改变正式词表的权力。当前 kb-design 只借用 DCMI 历史材料的职责分解和分层框架，没有因此建立正式 DCAP，也不使设计草案、映射或 target 接口生效。

DCMI 将本文采用的 2005、2007、2008 和 2009 材料列入 past specifications；它们可以支持概念与文档结构分析，不能支持当前 conformance 主张。DCTAP 的 Primer 与 Elements 也有不同状态，不能把其中一个文档的身份扩大到整套材料。

`Application Profile` 的中文 designation 核验结论为 `UNVERIFIED`，因此本库只登记英文 designation，不登记中文名称。

## 权威来源

- [DCMI Application Profiles 阅读笔记](../sources/dcmi-application-profiles.md)：材料身份、职责边界、规范状态、译名结论和项目边界
- [Dublin Core™ Application Profile Guidelines](https://www.dublincore.org/specifications/dublin-core/application-profile-guidelines/)：`term` 的选择、约束与应用语境
- [The Singapore Framework for Dublin Core™ Application Profiles](https://www.dublincore.org/specifications/dublin-core/singapore-framework/)：Application Profile 的组件与分层
- [Guidelines for Dublin Core™ Application Profiles](https://www.dublincore.org/specifications/dublin-core/profile-guidelines/)：功能范围、模型、字段约束、使用指南和编码指南
- [DCMI Abstract Model](https://www.dublincore.org/specifications/dublin-core/abstract-model/)：metadata 模型、encoding guideline 与 `Syntax Encoding Scheme`
- [Obsidian 官方帮助阅读笔记](../sources/obsidian-help.md)：properties、YAML 和应用能力边界

偏离约定：Application Profile 的中文 designation 未经现行阶梯核实，文章标题保留来源原名。
