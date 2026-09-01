# RFC 8785 阅读笔记

## 材料身份

本笔记记录 [RFC 8785: JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785.html) 的输入与序列化条件，并以 [Python `json` 文档](https://docs.python.org/3/library/json.html) 核对当前参数的直接行为，核对日期为 2026-09-01。JCS 是一组条件的组合，不能由键排序、UTF-8 或固定缩进中的任一单项推出。

## 阅读范围

| 材料 | 实际读到的位置 |
|---|---|
| RFC 8785 | 第 3.1 节 `Creation of Input Data`；第 3.2.1 节 `Whitespace`；第 3.2.2 节 `Serialization of Primitive Data Types`；第 3.2.3 节 `Sorting of Object Properties`；第 3.2.4 节 `UTF-8 Generation` |
| Python `json` 文档 | basic usage 中的 pretty printing；`ensure_ascii`、`indent` 和 `sort_keys` 参数说明 |

## 输入约束

JCS 要求输入适配 I-JSON：object 不得有重复 property name，string 必须可表达为 Unicode，number 必须可表达为 IEEE 754 double precision；解析后的 string 在后续序列化中不得被改变。JCS 不对 string 做 Unicode normalization，而是保留现有 Unicode 数据。[RFC 8785 第 3.1 节](https://www.rfc-editor.org/rfc/rfc8785.html#section-3.1)

## 序列化规则

JCS 必须同时满足以下规则。

- JSON primitive 按 ECMAScript 的 serialization rules 输出，包括 literal、string 和 number 的表示。
- JSON token 之间不输出 whitespace。
- object properties 递归排序；array 顺序不变，但其中 object 的 properties 仍须排序。
- property name 使用未转义字符串的 UTF-16 code units，并按无符号整数值、与 locale 无关地排序。
- 最终结果编码为 UTF-8。

这些条件分别来自 [RFC 8785 第 3.2.1 至 3.2.4 节](https://www.rfc-editor.org/rfc/rfc8785.html#section-3.2)。只满足其中一部分不能证明输出符合 JCS。

## 现状对照

当前 Obsidian exporter 的 manifest 使用以下参数事实：

```text
Python json.dumps(sort_keys=True, indent=2, ensure_ascii=False)
!= RFC 8785 JCS
```

`indent=2` 会输出用于 pretty printing 的换行和缩进，与 JCS 的 token 间无 whitespace 要求不同。`sort_keys=True` 只说明 Python 对 mapping keys 排序，不能证明使用 JCS 的 UTF-16 code unit 顺序；`ensure_ascii=False` 只说明非 ASCII 字符通常原样输出，不能证明 primitive serialization、I-JSON 输入约束和其余 JCS 条件全部成立。

当前使用参数事实描述，不使用 `canonical JSON` 或 JCS designation。实现中的局部标识符或错误消息不能替代逐项符合性判断。

## 适用边界

固定参数和 UTF-8 编码可以参与当前受控输入下的 deterministic behavior，但不能证明 JCS conformance、真实性、签名、provenance 或 reproducible build。JCS 规定可供密码学方法使用的字节表示，本身不提供签名或真实性证明。

## 未读范围

- 未通读 RFC 8785 的示例 canonicalizer、数字样例、实现指南、参考文献和勘误记录。
- 未核对 ECMAScript、I-JSON 和 IEEE 754 的完整规范正文，也未执行 JCS conformance test suite。
