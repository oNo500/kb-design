# 词表校验规则 (Vocabulary SHACL)

本包用 SHACL 描述[词表数据规范](../../docs/model/vocabulary/设计-词表数据规范.md)中的资源和字段。字段统计与结构校验共用这些定义，没有另一份 JSON 字段清单。

## 字段统计

在仓库根目录运行，默认统计全部资源类型和字段：

```sh
uv run kb-vocab-shacl inventory packages/kb-vocab-shacl/examples/valid.ttl --output build/vocab-inventory
```

替换示例文件路径即可统计自己的词表。输出目录中有 Markdown 表格和 `inventory.json`；目录已存在时会停止，避免覆盖上次报告。省略 `--output` 则直接显示表格。

只看概念字段：

```sh
uv run kb-vocab-shacl inventory vocabulary.ttl --type Concept
```

报告区分“有字段”“无字段”“对象不存在”和“需指定对象范围”。一个字段有多个值只算一个有字段对象；空字符串另计空值。可选字段也统计，缺省不判错。全图字段表还包括辅助资源上的字段。

资源按类型和结构中列明的关系选取；例如名称使用了 `literalForm`，即使漏写 `rdf:type`，也会列入名称统计。条件规则单列适用对象、范围是否指定及指定对象数；统计不会把“范围已指定”写成“校验已通过”。

统计只读取 TTL、建立计数，不运行 pySHACL，不修改词表。

## 结构入口

打开 [structure.ttl](src/kb_vocab_shacl/shapes/structure.ttl)，按资源入口查看：

| 入口 | 对象 |
|---|---|
| `resource:ConceptScheme` | 词表 |
| `resource:Concept` | 概念 |
| `resource:Label` | 独立名称记录 |
| `resource:Collection` | 集合，含已采用的集合子类型 |
| `resource:OrderedCollection` | 有序集合 |
| `resource:ConceptGroup`、`resource:ThesaurusArray` | 概念组、数组 |
| `resource:Note` | 独立说明，需要明确指定对象 |

`sh:property` 列字段，`sh:path` 指定属性，`sh:node` 引用共同字段。`common:Metadata`、`common:Notes`、`common:Evidence` 分别集中来源兼容、说明、依据字段；`rule:` 引用已有字段约束。数量条件和设计出处随字段保存。

这些是校验结构的标识，不是给词表新增资源类型。加载完整结构用 `read_shapes("structure")`，它会补齐共享定义。不要只把 `structure.ttl` 单文件交给校验器。

## 结构校验

需要检查已经表达的数量和值类型约束时，将同一结构交给 pySHACL：

```python
from rdflib import Graph
from pyshacl import validate
from kb_vocab_shacl import read_shapes

rules = Graph().parse(data=read_shapes("structure"), format="turtle")
data = Graph().parse("vocabulary.ttl", format="turtle")
conforms, report, text = validate(data, shacl_graph=rules)
print(text)
```

字段列全不等于所有业务要求都能自动判断。本地新增记录、日期和独立说明的条件规则，须指定对象后执行；外部管理记录另行核对。具体范围见[规则覆盖](COVERAGE.md)。

名称字段共用非空文字约束；数量、值类型和类型声明缺失会在结构校验中检查。统计中的空值计数与校验是否通过是两项分别报告的结果。

## 其他校验

原有 `standard` 和 `target` 校验组合继续保留，包含类型、名称、关系冲突等检查。它们与 `structure` 分别选择，字段统计不会自动运行它们；现有词表的发布流程也未切换。

`Violation`、`Warning`、`Info` 在具体规则的 `sh:severity` 上设置。pySHACL 默认严格结果会将三个等级都计入不符合；是否放行由调用方另行决定。

## 维护方式

修改资源字段和共同字段时，编辑 `structure.ttl`；修改复用的约束时，编辑其所在的原规则文件。保留规则 IRI 和设计依据，条件要求不得擅自改成全局必填。

```sh
uv run python -m unittest discover -s packages/kb-vocab-shacl/tests -v
```

测试核对设计字段是否漏列、统计口径及结构的可执行性。未知资源选项、不支持的路径或解析失败会明确报错；存在缺项本身不会让统计命令失败。
