# 词表预览 (Vocabulary Preview)

只读浏览仓库工作区中的六份词表，保留条目搜索、主题层级、关系图、来源依据和原始 YAML。保存词表后页面自动更新，包括尚未提交的修改；这些显示不代表修改已经审核或正式采用。

## 启动方式

在仓库根目录运行：

```bash
uv sync --all-packages --locked
uv run kb-vocab-preview
```

浏览器打开 <http://127.0.0.1:8765>。终端按 `Ctrl+C` 停止服务。缓存齐全时，uv 命令可加 `--offline`。

指定其他数据目录或端口：

```bash
uv run kb-vocab-preview --repo-root /path/to/kb-design --port 8766
```

默认数据目录取应用所在仓库，不依赖启动时的工作目录；只监听 `127.0.0.1`。

## 更新方式

服务读取 `data/vocab/` 下的 `topics.yaml`、`entities.yaml`、`sources.yaml`、`types.yaml`、`genres.yaml` 和 `forms.yaml`。页面约每秒查询一次变化，以文件内容判定是否更新，不依赖 Git 提交或文件修改时间。

文件变化后自动重载页面，因此搜索、筛选和展开状态会重置。文件暂时缺失、YAML 格式或显示结构错误时，页面显示错误并保留服务本次运行中上一次有效内容；修正文件后自动恢复。首次启动就有错误时显示等待页面。

预览直接在内存中生成，不写入词表，也不需要生成 `index.html` 或 `snapshot.json` 文件。`output/obsidian/` 的生成与刷新仍由 Obsidian 应用负责。

## 维护位置

| 文件 | 职责 |
|---|---|
| `src/kb_vocab_preview/server.py` | 读取数据、检测变化、基础显示结构检查与本地 HTTP 服务 |
| `src/kb_vocab_preview/template.html` | 词表列表、搜索、层级、关系图和详情表示 |
| `tests/test_preview.py` | 更新、错误恢复、只读边界和安全嵌入检查 |

词表结构或依据表示发生变化时，同时检查采集器与页面的字段处理。这里的结构检查只保证可显示，不替代核心程序的正式数据校验。修改 Python 服务后重启命令；修改页面模板后手动刷新浏览器。

```bash
uv run python -m unittest discover -s apps/vocab-preview/tests
```

验收实时行为时使用临时数据副本，不为演示修改正式词表。原本地预览目录保留为历史备份，应用运行不依赖它；旧生成快照、重复的脚本提取文件和研究缓存不作为本应用源码维护。
