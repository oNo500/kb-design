# BagIt 文件包格式

## 材料身份

本笔记记录 [RFC 8493: The BagIt File Packaging Format (V1.0)](https://www.rfc-editor.org/rfc/rfc8493.html) 的文件结构、manifest 和校验边界，核对日期为 2026-09-01。RFC 8493 是 Informational RFC；本文只按其明示条件判断 BagIt 对象，不把一般项目清单类比成 BagIt。

## 阅读范围

实际读取 RFC 8493 的摘要、第 1.3 节 `Terminology`、第 2 节 `Structure`、第 2.1.1 节 `Bag Declaration`、第 2.1.2 节 `Payload Directory`、第 2.1.3 节 `Payload Manifest`、第 2.2.1 节 `Tag Manifest`、第 2.4 节 `Bag Checksum Algorithms` 和第 3 节 `Complete and Valid Bags`。

## 清单边界

RFC 8493 中的 manifest 是 filepath 到 checksum 的映射，分为两类。

| 对象 | 规范职责 |
|---|---|
| payload manifest | Bag 的必需 tag file；每份 payload manifest 必须把 `data/` 下每个 payload file 恰好列出一次，并记录相应 checksum |
| tag manifest | 可选 tag file；记录其他 tag files 及其 checksum，必须列出所有 payload manifests，不得列出 payload files 或其他 tag manifests |

payload manifest 用于 payload 完整性检查，tag manifest 用于 tag files 完整性检查。两者有不同覆盖对象，不能把任意包含路径和 checksum 的项目文件直接称为其中之一。

## 完整边界

complete bag 必须具备 RFC 8493 要求的元素，包括 `bagit.txt`、`data/` 和至少一份 payload manifest；manifest 所列文件必须存在，每个 payload file 必须被每份 payload manifest 列出，现有元素还须符合 BagIt 1.0。

valid bag 先必须是 complete bag，再要求每份 payload manifest 和 tag manifest 中的每个 checksum 都已与对应文件内容成功核验。complete 只回答结构与覆盖是否齐全，valid 还回答 manifest checksum 是否核验成功；二者不是同一状态。

## 校验边界

checksum 可以检查某组 bytes 是否与记录值一致，不能证明这些 bytes 的 provenance、真实性、审批状态、语义正确性或可重建性。RFC 8493 的 checksum 核验也不等于数字签名；本项目不因采用项目 manifest 而引入签名。

## 项目边界

当前 Obsidian exporter 的输出没有 `bagit.txt`、`data/` 和 RFC 8493 规定的 BagIt 文件结构，因此 `manifest.json` 只是项目 manifest，不是 BagIt payload manifest 或 tag manifest；输出目录也不据此成为 complete bag 或 valid bag。项目 manifest 的文件覆盖和 checksum 检查不能被描述为 BagIt conformance。

## 未读范围

- 未通读 RFC 8493 的示例、安全考虑、实践考虑、ABNF、参考文献和勘误记录。
- 未评估或引入 BagIt 工具、序列化传输、签名、远程 payload 或 `fetch.txt`。
