# 依赖依据

RDF、YAML 和 SHACL 使用仓库已有的 RDFLib、PyYAML、PySHACL 与 `kb-vocab-shacl`，实际版本固定在根 `uv.lock`。

文章标题按 Markdown 结构检查，使用 `markdown-it-py` 4.x，避免将代码块中的井号当标题或拒绝合法 Setext 标题。只读取语法树，不执行或渲染源 HTML。

2026-09-23 核对：[PyPI 发布记录](https://pypi.org/project/markdown-it-py/)列出 2026-05 的 4.2.0，wheel 约 91.7 KB，最低 Python 3.10；符合本包最低 Python 3.11。带入的 `mdurl` 与实际安装版本一并见锁文件。

[历史安全通告](https://github.com/advisories/GHSA-vrjv-mxr7-vjf8)列出的 CVE-2023-26303 影响低于 2.2.0，已在 2.2.0 修复。4.x 不在该影响范围；这不是“没有任何风险”的保证。[官方安全说明](https://markdown-it-py.readthedocs.io/en/latest/security.html)提醒默认原始 HTML 的处理边界，本包只解析 token，不输出 HTML。
