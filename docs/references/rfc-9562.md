# RFC 9562 阅读笔记

本文记录 [RFC 9562: Universally Unique IDentifiers (UUIDs)](https://www.rfc-editor.org/rfc/rfc9562.html) 与 DCMI `identifier` 中和内容身份有关的事实。核对日期为 2026-09-02。RFC 9562 是 Standards Track RFC；DCMI `identifier` 是 DCMI Metadata Terms 的 property。

## 阅读范围

实际读取 RFC 9562 的摘要、第 1 节 `Introduction`、第 4 节 `UUID Format`、第 4.2 节 `Version Field`、第 5.4 节 `UUID Version 4`、第 5.7 节 `UUID Version 7`、第 6.7 节 `Collision Resistance`、第 6.8 节 `Global and Local Uniqueness`、第 6.9 节 `Unguessability`、第 6.10 节 `UUIDs That Do Not Identify the Host`、第 6.11 节 `Sorting`、第 6.12 节 `Opacity` 和第 8 节 `Security Considerations`。

实际读取 [DCMI Identifier](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/terms/identifier/) 的 Definition、Comment、Has Range 和 Examples。

## 引用语义

DCMI 把 `identifier` 定义为在给定语境内对资源的无歧义引用，并建议使用符合某种 identification system 的字符串。该定义允许 UUID 成为一种候选表示，但不要求资源使用 UUID，也不决定 UUID 的版本或项目字符串格式。

## 格式事实

UUID 是 128-bit identifier，不需要中央登记。RFC 9562 规定的文本表示是 `hex-and-dash`：十六进制字符分组后以连字符分隔。

## 版本事实

UUIDv4 使用随机或伪随机位生成。版本位和 variant 位占用固定位置，其余位来自随机数据。

UUIDv7 包含 Unix Epoch 时间：最高 48 bits 保存 UTC 1970-01-01 起的毫秒数；除版本位和 variant 位外，其余 74 bits 可以全部使用随机数据，也可以依次组合可选的亚毫秒时间部分、计数器和剩余随机数据。UUIDv7 的字段布局支持按时间排序；RFC 9562 还说明 UUIDv6 和 UUIDv7 可按不透明原始 bytes 排序，无需先解析内部字段。

## 性质边界

唯一性、不可猜测性、排序和不透明性是不同要求。

| 性质 | RFC 9562 支持的判断 | 不能推出 |
|---|---|---|
| 唯一性 | UUID 可以在具体应用语境中提供实用的低碰撞身份 | 在没有共享知识机制时保证绝对的全局唯一 |
| 不可猜测性 | CSPRNG 可以同时降低碰撞概率和预测可能性 | 任意 UUID 都不可猜，或 UUID 可以充当 security capability |
| 排序 | UUIDv7 支持时间排序，规范文本表示也面向词法排序 | 排序值不包含时间信息，或排序结果等于内容语义顺序 |
| 不透明性 | 应用通常应避免不必要地解析 UUID | UUID 的内部布局没有版本、时间或随机字段 |

第 8 节还说明，UUID 不提供人工可见的完整性检查；嵌入的 timestamp 可以暴露创建顺序。由此，唯一性不能替代不可猜测性，不可猜测性不能替代访问控制，排序能力也不能证明值对应用不泄露时间语义。

## 项目边界

RFC 9562 不决定本项目应使用哪一版 UUID，也不批准 `cu-` 前缀。DCMI `identifier` 只给出资源引用的语义边界，同样不能批准具体发放算法、唯一范围、前缀、路径绑定或采用状态。

## 未读范围

- 未通读 RFC 9562 的其他 UUID 版本、完整 bit layout、生成器状态、monotonicity 算法、IANA 登记细节、测试向量、示例实现、参考文献和勘误记录。
- 未核对 UUID 库的跨语言实现、数据库性能、碰撞概率计算或本项目实际内容规模。
- DCMI 页面只读取“阅读范围”所列内容，未据其示例扩展本项目规则。
