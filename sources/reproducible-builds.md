# 可重现构建 (Reproducible Builds)

## 材料身份

本笔记只记录 [Reproducible Builds](https://reproducible-builds.org/) 项目公开文档中与定义、确定性和稳定输入有关的内容，核对日期为 2026-09-01。文档给出软件构建的可重现性边界，不替本项目证明任何具体导出已经满足该边界。

## 阅读范围

| 材料 | 实际读到的位置 |
|---|---|
| [Definitions](https://reproducible-builds.org/docs/definition/) | `When is a build reproducible?`、`Explanations` |
| [Deterministic build systems](https://reproducible-builds.org/docs/deterministic-build-systems/) | 开头说明、`Drawing the line`、`In a nutshell` |
| [Stable order for inputs](https://reproducible-builds.org/docs/stable-inputs/) | 开头说明、`Example: Makefile`、`Example: tar` |

## 概念边界

reproducible build 的边界是：给定相同的 source code、build environment 和 build instructions，任何一方都能重建全部指定 artifacts 的逐比特相同副本。指定 artifacts 是声明可重现性时明确的主要输出，不自动包括日志等辅助输出。[Definitions](https://reproducible-builds.org/docs/definition/)

deterministic behavior 回答受控输入下输出是否稳定；reproducible build 还要求任何一方能够依据已界定的 source、environment 和 instructions 独立重建指定 artifacts。本机在同一环境中双跑一致，只证明当前受控环境下的确定性，不能证明 independent rebuild，也不等于 reproducible build。

## 环境输入

build environment 的相关属性可包括依赖及其版本、构建配置和被构建系统使用的环境变量，例如 locale。[Definitions](https://reproducible-builds.org/docs/definition/) 对本项目的生成过程，工具版本、locale、timezone、路径、当前时间、随机数和文件遍历顺序都可能成为输入或影响输入顺序，必须明确控制或排除，不能因一次双跑一致就假定它们已经稳定。

[Deterministic build systems](https://reproducible-builds.org/docs/deterministic-build-systems/) 将基本做法概括为稳定输入、稳定输出，并尽量少捕获环境状态。[Stable order for inputs](https://reproducible-builds.org/docs/stable-inputs/) 进一步说明文件系统遍历顺序和受 locale 影响的排序可能使同一来源产生不同结果。

## 项目边界

当前 Obsidian exporter 不宣称 reproducible build。项目可以用同环境双跑和字节比较检查当前受控环境中的 deterministic behavior，但该检查不能证明另一方能够按已声明的环境和指令独立重建，也不能把当前输出描述为 reproducible build。

## 未读范围

- 未通读 Reproducible Builds 文档索引中的其他页面、工具实现、发行版认证和外部案例。
- 未据这三页材料建立本项目的环境封装、构建指令发布、第三方重建或认证流程。
