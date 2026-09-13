# 词表浏览

Skosmos 3.4 + Apache Jena Fuseki 6.2.0，用于本地浏览 SKOS Turtle。支持 IEEE 2025 评估数据及当前自有词表，不改变正式词表、概念身份或来源关系。

## 浏览入口

打开 [IEEE 词表](http://localhost:9090/ieee/zh/)。搜索 `LLM` 可找到 `Large language models`；左侧查看层级，右侧查看上位、下位、相关概念和别名。右上角可切换英文界面。中文采用上游翻译，部分文字尚未翻译。

## 启停命令

以下命令在本目录运行，Docker Desktop 须已启动。

```bash
./fetch-runtime.sh
docker compose up -d
./import-ieee.sh
```

首次启动后，待 Fuseki 日志出现 `Start Fuseki` 再导入。后续启动无需重新导入；数据保存在 `output/databases/`。

```bash
docker compose logs --tail 30
docker compose stop
docker compose up -d --pull never
```

`docker compose down` 移除容器，保留绑定目录的数据。镜像与数据库位于本机，服务仅监听 `127.0.0.1`。

## 数据路径

| 路径 | 职责 |
|---|---|
| `config/skosmos.ttl` | 浏览器语言、词表名称及查询端点 |
| `config/fuseki.ttl` | TDB2 数据库和 Jena Text 标签索引 |
| `output/runtime/` | 经校验的 Fuseki JAR |
| `output/databases/` | 可从 Turtle 重建的数据库和搜索索引 |
| `output/verification.json` | 本次导入与读取一致性证据 |
| `../../packages/kb-vocab/output/ieee-2025-resolved/vocabulary.ttl` | 当前导入文件，脚本只读 |

`import-ieee.sh` 使用 Graph Store PUT，仅替换 `urn:kb-design:preview:ieee-2025` 图，不累加旧三元组。此图名是部署配置，不是概念标识。重新生成 Turtle 后，显式运行导入脚本更新浏览副本。

Fuseki 本机端点为 `http://127.0.0.1:9030/skosmos/sparql`；浏览网页不提供词表编辑。不要直接编辑数据库目录。

## 依赖依据

使用 [Skosmos 官方镜像](https://github.com/NatLibFi/Skosmos/wiki/Install-Skosmos-with-Fuseki-in-Docker)，配置参考固定的 [v3.4 示例](https://github.com/NatLibFi/Skosmos/tree/v3.4/dockerfiles/config)。Skosmos 使用 MIT 许可证；Apache Jena 使用 Apache-2.0。镜像摘要在 Compose 中固定，Fuseki JAR 使用 SHA-256 校验；未新增 Python 或 Node 依赖。

2026-09-13 核对：Skosmos 3.4 于 2026-08-31 发布，公开 GitHub 安全公告接口未列出公告，这不代表无漏洞。Jena 6.2.0 修复了影响至 6.1.0 的 CVE-2026-61372，见 [Jena 安全公告](https://jena.apache.org/security/advisories.html)。本次未做完整容器漏洞扫描。

本机 Docker 报告镜像大小约为 Skosmos 116 MB、Temurin 119 MB，另有 Fuseki JAR 57 MB 和数据库。Skosmos 官方镜像为 amd64，本机 Apple Silicon 通过 Docker 模拟运行；Fuseki Java 镜像为 arm64。配置为本地预览用途。

## 合并词表

[当前合并词表](http://localhost:9090/current/zh/?clang=en)读取 `output/vocabulary/current/vocabulary.ttl` 的浏览副本。在本目录运行 `./import-current.sh` 更新；脚本先固定并校验 current 指向的构建，再从同一份主图准备数据库与导航数据。完成后刷新浏览器。

`sync-current.py` 在内存中补齐原预览脚本规定的标准反向关系，再导入独立命名图。数据库读回图必须与预期同构，导航写入也必须核对，全部成功才写入 `output/sync-receipt.json`。记录绑定构建清单、来源文件、导航文件、应用配置和相关代码的摘要。

```bash
./import-current.sh
./import-current.sh --check
# 指定保留版本也可同步：
./import-current.sh --build ../../output/vocabulary/versions/BUILD_ID
```

`--check` 实时核对当前所选构建、导航和数据库；构建已变化而应用尚未更新时明确失败。历史 `verification.json` 等文件只作旧验收记录，不再作为当前同步依据。

导入期间持有写锁。失败会尝试恢复旧数据库、导航及同步记录，并将 `sync-status.json` 标为回滚或恢复失败；不会留下本次成功状态。进程强杀或断电可能留下 running 状态及写锁，需要排查后重新同步；本流程不承诺不中断切换或崩溃恢复。反向关系只用于浏览，不写回原始 Turtle。

`build-navigation.py` 使用已有 RDFLib 生成 `output/navigation/navigation.json`，为合并词表提供应用导航：

- 有明确顶层概念时，以这些概念为入口。
- 未指定顶层时，以本体系成员中没有体系内直接上位概念的节点作为浏览入口，并显示说明；不声明它们是来源顶层概念。
- 未被入口覆盖的成员仍列出，避免断开的环路或不完整顶层声明隐藏成员。
- 分支只展示本体系内已有的直接关系；多上位关系保留，环路回到当前路径已出现节点时停止展开并显示 `↻`。右侧概念详情仍显示原图的跨体系关系。
- 概念详情页刷新后，导航展开一条到该概念的路径；其他上位路径仍可手动展开。

当前发布数据为一个 `kb-design` 概念体系，八个领域使用 `skos:Collection`；八个领域从“分组”页进入，“层级”页展示概念体系及概念上下位关系。Skosmos 配置显式指定该主体系，内容语言设为 `en`、`zh`。分组按 `skos:Collection` 读取。前端覆盖文件及上游版本见 [展示兼容](overrides/README.md)。首次下载约 10 MB 的导航 JSON，随后在当前页面展开无需请求下层数据。

验证命令：

```bash
node --test tests/navigation.test.cjs
uv run --package kb-vocab python -m unittest discover -s tests
```
