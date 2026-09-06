# Reproducible Builds

## 构建定义

软件产品的构建过程具有可重现性，是指在指定其源码的具体版本及全部构建依赖后，无论在哪种环境执行，每次构建都产生逐比特相同的产物。这是 Lamb 与 Zacchiroli 的 IEEE Software 论文 Definition 1 的定义条件。

例如，本库若要据此描述参考导出的构建过程，就需要明确源码与输入快照、全部构建依赖及所比较的产物。同一环境运行两次结果相同，只能证明这两次执行的确定性，不能证明环境变化不影响结果，也不能证明依赖已完整列出。

## 定义的差异

Reproducible Builds 项目官网的 Definitions 页面采用另一组条件：任何一方在相同源码、构建环境和构建指令下，可以重建逐比特相同的指定产物。这里把相同环境作为前提；IEEE 论文则要求指定源码版本及全部依赖后，结果不受执行环境影响。两种表述不能只互换来源链接而保持定义不变。

本库以 IEEE 论文定义为概念依据。官网页面保留为实践入口和条件对照，其“相同环境与指令”不替代论文的“全部构建依赖”和“无论在哪种环境执行”。

## 证据的边界

同环境确定性、独立重建、完整性检查与来源记录回答不同问题，不能互相替代。

同环境双跑比较指定文件的字节，可以发现当前受控环境中的不稳定输出。由另一方独立重建并比较结果，则能检查其是否可以用给定输入和依赖得到相同产物；一次成功的独立重建仍不能单独证明所有环境下的每次构建均相同。

项目 manifest 与 checksum 可以核对已列文件的字节；配合文件集合规则，才能检查声明范围内的完整性。它们不证明生成者身份、审批、语义正确性或可重现性。provenance 记录表达输入、活动、输出及派生关系，记录存在也不自动证明其真实或产物正确。

例如，两个导出目录的 hash 相同说明字节比较结果相同；manifest 列齐文件说明清单范围得到覆盖；另一方生成相同目录提供独立重建证据。这三项分别需要自己的输入和核对记录。

## 相邻机制

稳定序列化和输入顺序可以减少非确定性，但固定几个 JSON 参数并不自动满足 JCS。JCS 同时约束 I-JSON、基本值序列化、属性排序、空白和 UTF-8。

BagIt manifest 按 RFC 8493 记录文件及 checksum；普通项目 manifest 不能因此称为 BagIt。W3C PROV 可以表达 Entity、Activity、Usage、Generation 和 Derivation，但来源关系记录不替字节比较或真实性核对作保证。

目标目录的原子替换在成功时提供可见切换，不等于持久性、多文件事务或内容正确性。这些机制可分别支持构建和交付，但都不是 Reproducible Builds 定义的替代物。

## 项目用法

本库当前只取得同环境确定性证据：固定输入快照与当前环境，按同一指令重复生成并比较指定产物。当前尚未证明全部构建依赖已完整指定、跨环境构建一致或任意构建均逐比特相同；也没有由另一方完成的独立重建记录。

因此，词条采用 IEEE 论文定义不改变应用能力的声明范围。现有参考导出仍只声明同环境确定性、项目 manifest 完整性和成功目录替换的原子可见性，不声明 reproducible build conformance、BagIt、JCS 或持久性。

## 权威来源

- Lamb, C. 与 Zacchiroli, S. [Reproducible Builds: Increasing the Integrity of Software Supply Chains](https://arxiv.org/pdf/2104.06020v1)，IEEE Software，2021，[DOI](https://doi.org/10.1109/MS.2021.3073045)：固定作者稿第 2 页 Definition 1，源码版本、全部依赖与环境无关条件。
- [Definitions](https://reproducible-builds.org/docs/definition/)：官网条件对照与实践入口，不承担本库定义依据。
- [Reproducible Builds 阅读笔记](../references/reproducible-builds.md)：官网材料的既有核对记录；其中相同环境条件不替代 IEEE 论文定义。
- [BagIt 文件包格式阅读笔记](../references/rfc-8493.md)：manifest、checksum、complete bag 与 valid bag 的边界。
- [RFC 8785 阅读笔记](../references/rfc-8785.md)：JCS 的组合条件与当前参数边界。
- [W3C PROV 阅读笔记](../references/w3c-prov.md)：provenance 对象、关系与证明边界。
- [Python 文件系统阅读笔记](../references/python-filesystem.md)：原子可见性、持久性与事务边界。
