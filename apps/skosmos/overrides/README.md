# 展示兼容

`tab-hierarchy.js` 和 `messages.zh.json` 来自固定的 Skosmos v3.4 官方镜像，按随附 MIT 许可证保留。升级镜像时需重新核对覆盖文件。

- `tab-hierarchy.js`：体系名称兼容 `prefLabel`；当前合并词表通过 `navigation.js` 消费应用导航 JSON，其他词表仍走上游流程。错误加载显示提示，不把失败显示为空数据。
- `navigation.js`：本地应用代码，复用 Skosmos 的树组件和详情页面；按体系成员过滤关系，支持缺少顶层声明的浏览入口、多上位关系和环路终止。选中概念时展开一条路径，不修改 RDF。
- `messages.zh.json`：仅调整 `A-Z`、`Hier-nav`、`Group-nav`，显示“字母索引”“层级”“分组”，其余保留上游翻译。

全部通过 Compose 只读挂载。代码更新后若浏览器保留旧脚本，使用强制刷新。导航 JSON 更新随 `import-current.sh` 完成，来源 SHA-256 保存在 JSON 中。
