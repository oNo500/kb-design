# 词表分类树 (Vocabulary Tree)

只读浏览 Turtle 词表，像文件夹一样展开和收起分类。直接读取 `.ttl`，不转换回 YAML，不运行 SHACL，也不写回数据。

## 启动方式

在仓库根目录运行：

```sh
uv run kb-vocab-rdf-preview
```

打开 <http://127.0.0.1:8766>。默认读取 `output/vocabulary/ccs/build-48644c2ed653/vocabulary.ttl`；终端按 `Ctrl+C` 停止。

指定其他文件或端口：

```sh
uv run kb-vocab-rdf-preview /绝对路径/vocabulary.ttl --port 8767
```

词表重建后刷新浏览器，页面会重新读取文件；展开状态随刷新重置。仅监听本机，不依赖外部网页资源。

## 浏览方式

- 点击分类行展开或收起，右侧数字是直接下级数量。
- 名称读取 SKOS 或 SKOS-XL 首选名，优先已有中文，其次英文；没有名称时显示 IRI，不自动翻译。
- 分类按名称排序，上下位关系同时读取 `broader` 和 `narrower`；同一概念可以出现在多个分支。
- 循环引用显示后停止展开；没有可达顶层的部分也保留浏览入口，不改变源关系。

只显示声明为 `skos:Concept` 的概念，不包含搜索、详情编辑或关系图。

## 维护位置

`src/kb_vocab_rdf_preview/server.py` 负责读取与本地服务；`template.html` 负责树形页面。依赖复用已有 RDFLib，旧 YAML 预览应用保持独立。

```sh
uv run python -m unittest discover -s apps/vocab-rdf-preview/tests -v
```
