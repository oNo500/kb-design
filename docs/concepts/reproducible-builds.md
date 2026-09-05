# Reproducible Builds

## 定义

Reproducible Builds 是使任何一方能够在相同 source、environment 和 instructions 下，重建逐比特相同的指定 artifacts 的实践。[Definitions](https://reproducible-builds.org/docs/definition/) 把“任何一方”和“指定 artifacts”都纳入定义，因此同一台机器重复生成相同 bytes 只是确定性证据，不是完整的可重建证据。

例如，本库若要提出这一主张，就必须给另一方同一份输入快照、已界定的工具与环境、可执行的生成指令和明确的输出集合，并由对方独立生成逐比特相同的输出。只在当前环境运行两次并比较目录，尚未完成这项证明。

## 解决的问题

Reproducible Builds 把“输出看起来一样”拆成可以核对的输入、环境、步骤和结果。

| 问题 | 本库例子 | 处理方式 |
|---|---|---|
| 隐藏环境状态改变输出 | locale、timezone、工具版本或遍历顺序参与生成 | 明确 environment，并控制或排除环境输入 |
| 一次成功无法证明输出稳定 | 同一命令只运行一次 | 在受控环境双跑并逐字节比较 |
| 本机稳定无法让别人复核 | 另一方拿不到相同 instructions 或依赖版本 | 发布可执行指令和完整环境边界，执行 independent rebuild |
| 输出范围不明确 | 主文件一致，但辅助 artifact 没有纳入声明 | 在声明前界定 specified artifacts |

本库当前使用这套方法限制完成声明，不把局部一致性扩大成尚未取得的证据。

## 证据层次

四类证据各自回答一个问题，后一类不能由前一类自动推出。

| 证据 | 能证明 | 不能证明 |
|---|---|---|
| 确定性 | 同一受控 source 和 environment 下重复执行产生相同 bytes | 另一方能够独立重建 |
| `independent rebuild` | 另一方依据已声明的 source、environment 和 instructions 重建相同 specified artifacts | manifest 的覆盖完整性、provenance 或语义正确性 |
| `manifest`／`checksum` | 已列 artifact 的 bytes 与记录值一致；另有覆盖规则时可检查文件集合 | bytes 的 provenance、真实性、审批、语义或可重建性 |
| `provenance` | 记录 Entity、Activity、Usage、Generation 或 Derivation 等来源关系 | 记录真实、bytes 确定、checksum 正确或任何一方可重建 |

例如，同环境双跑一致可以支持第一行；另一方重建支持第二行；项目 manifest 的 hash 支持第三行的局部完整性；生成活动与输入输出关系属于第四行。四种记录即使同时存在，也要分别核对各自条件。

## 相邻机制

生成链中的相邻机制可以提供局部保证，但各自不能替代 Reproducible Builds。

| 机制 | 局部作用 | 边界 |
|---|---|---|
| 稳定序列化 | 固定输入顺序和输出参数，减少非确定性 | 固定参数不自动满足 JCS |
| JCS | 同时约束 I-JSON、primitive serialization、property 排序、whitespace 和 UTF-8 | 满足部分条件不能声称 JCS conformance，也不能证明可重建性 |
| BagIt manifest | 按 RFC 8493 记录 payload 或 tag files 及 checksum | 普通项目 manifest 不是 BagIt；checksum 不证明 provenance |
| W3C PROV | 表达 Entity、Activity 及 Usage、Generation、Derivation | provenance 关系不证明真实性、字节确定性或可重建性 |
| 原子替换 | 成功时提供单个目标目录项的可见切换 | 不等于 `fsync` durability、多文件事务或内容正确性 |

本库按这些机制各自的来源条件描述能力，不用一个机制的证据替另一个机制背书。

## 项目用法

本库当前只取得同环境双跑的确定性证据：固定同一 source 快照和当前 environment，按同一 instructions 生成两次，再逐字节比较指定 artifacts。该证据只允许说明当前受控环境中的输出稳定。

当前没有由另一方执行的 independent rebuild，也没有把 environment 封装与 instructions 发布成可供任何一方复现的完整输入。因此，项目只用 Reproducible Builds 方法限制完成声明，不把现有导出描述为 reproducible build。

## 适用边界

同环境双跑、稳定 JSON 参数、manifest checksum、provenance 记录和原子替换都可以成为生成证据的一部分，但任何一项都不能单独证明 reproducible build。当前项目 manifest 不是 BagIt manifest；固定 JSON 参数不产生 JCS conformance；输入输出字段不自动构成 W3C PROV 记录；原子可见性也不产生 durability 保证。

本库只有在另一方依据已声明的 source、environment 和 instructions 独立重建全部指定 artifacts，并得到逐比特相同结果后，才具备定义要求的 independent rebuild 证据。当前不作这一完成声明。

## 权威来源

- [Reproducible Builds 阅读笔记](../references/reproducible-builds.md)：定义、环境输入和当前项目边界
- [Definitions](https://reproducible-builds.org/docs/definition/)：source、environment、instructions、specified artifacts 与任何一方重建
- [Deterministic build systems](https://reproducible-builds.org/docs/deterministic-build-systems/) 与 [Stable order for inputs](https://reproducible-builds.org/docs/stable-inputs/)：稳定输入、稳定输出和输入顺序
- [BagIt 文件包格式阅读笔记](../references/rfc-8493.md)：manifest、checksum、complete bag 与 valid bag 的边界
- [RFC 8785 阅读笔记](../references/rfc-8785.md)：JCS 的组合条件与当前参数边界
- [W3C PROV 阅读笔记](../references/w3c-prov.md)：provenance 对象、关系和证明边界
- [Python 文件系统阅读笔记](../references/python-filesystem.md)：原子可见性、持久性与事务边界
