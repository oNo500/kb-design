# 断言的依据

词表和内容模型里有些字段的值不是从来源抄来的，是人判断的：一个实体属于哪个主题（`subjects`）、一个本地概念挂在哪个上位（`broader`）、`form` 取 Wikidata 多个类里的哪个、`scope` 怎么写。这些判断如果不记依据，半年后就成了事实，再被当作推断的前提——零自定防的是自造的词，本文防的是自造的断言。

依据：Z39.19 §11.1.4 词记录要有“来源”字段（对新词尤其重要，可引出版物或咨询的人）；ISO 15489-1 第 4 章原则 (c) 元数据描述记录的背景；W3C PROV 把“由谁、据什么产生”作为溯源的基本要素。

## 哪些字段是判断

| 词表 | 判断字段 |
|---|---|
| 主题词表 | 本地概念的 `broader`、`related`、`scope`；借入概念之间的合并（同名归一） |
| 命名实体词表 | `subjects`、`form`（多个 Wikidata 类取一个时）、`scope`、`vendor` |
| 内容单元 | `subject`、`type` |

借入的值（`source` 非 self 的 `broader`、`match`、`label`）不是判断，不记依据。

## 记录

判断字段旁边记 `basis`，值是依据的标识：

```yaml
- id: eslint
  subjects: [tools-and-environments]
  basis:
    subjects: cs2023:SE-Tools#3        # 来源 id + 条目 + 主题编号：SE-Tools 主题 3“静态和动态分析工具”
- id: uv
  subjects: [tools-and-environments]
  basis:
    subjects: self                      # 没核到依据
```

`basis` 的值：

| 值 | 含义 |
|---|---|
| `<来源 id>:<条目>[#<位置>]` | 在该来源的该条目里核到了支持这个判断的文字 |
| `wikidata:<Q 号>/P31` | `form` 取自该条目的 instance of；多个值时全部记在 `form`，不挑 |
| `self` | 本库判断，未核到外部依据 |

## 规则

1. 有任何 `basis: self` 的记录，`status` 不得为 `active`，留在 `candidate`
2. `basis` 引用的来源改版时，这些断言随来源复核（[来源复核](review.md)）
3. 校验脚本统计 `self` 的数量，按词表和字段列出，与盲区地图并列——它是本库的判断债
4. 把 `self` 转为有依据，只能靠核到文字；不能靠“用了很久没出问题”

## 校验

- `basis` 里的来源 id 在 `sources.yaml` 中
- 有 `basis: self` 而 `status: active` 的，报错
- 输出：每份词表 `self` 断言数、占判断字段总数的比例

## 待定事项

- 内容单元的 `subject`、`type` 是否也记 `basis`，还是由回流的引用计数代替
- `basis` 条目里“#位置”的写法是否统一为来源自己的编号

## 权威来源

- ANSI/NISO Z39.19-2005 §11.1.4 Term Records
- [ISO 15489-1:2016](https://www.iso.org/standard/62542.html) §4 (c)，见[笔记](../sources/iso-15489.md)
- [W3C PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/)，2013 Recommendation
