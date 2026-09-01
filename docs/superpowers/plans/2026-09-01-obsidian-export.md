# Obsidian 导出计划 (Obsidian Export Implementation Plan)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development and superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立从六份正式词表到安全、确定、可浏览的 Obsidian 管理目录的一向导出，并形成项目原生应用映射。

**Architecture:** 单一 Python 模块负责加载、校验、渲染和原子写入；内部先构造完整 `path → bytes` 集合，再生成 manifest 并写入同级临时目录。Markdown 笔记保存扁平 properties 和正文表格，Bases 提供可选浏览，正式数据与导出输出保持单向关系。

**Tech Stack:** Python 3.9.6、PyYAML 6.0.3、Markdown、YAML、JSON、Obsidian Bases、`unittest`、Git。

**Spec:** [Obsidian 导出设计](../specs/2026-09-01-obsidian-export-design.md)

## 全局约束

- 只在 `/Users/xiu/code/kb-design` 的 `feat/terminology-governance` 分支执行，不创建 worktree，不修改 `master`。
- 正式输入只取 `vocab/topics.yaml`、`entities.yaml`、`sources.yaml`、`types.yaml`、`genres.yaml`、`forms.yaml` 和导出器自身。不得读取迁移账本、草案、候选报告、未激活术语配置或未来 `vocab/terms.yaml`。
- 当前输入计数为 700 topics、24 arrays、61 entities、31 sources、6 types、5 genres、16 forms，共 843 个对象。输出内容文件为 843 个对象笔记、3 个 Bases 和 1 个 README，共 847 项；另有 1 个 manifest，总文件数 848。
- 对象路径固定为 `KB/<Kind>/<id>.md`；稳定 `id` 决定路径，标签和 alias 不决定文件名。所有引用使用 vault 根相对 Wikilink。
- properties 只允许标量或标量列表，不允许嵌套 dict／list-of-dict。`basis`、`match`、`history` 等嵌套值进入正文，不能静默丢失。
- aliases 只消费正式记录中已有非空形式，不翻译、不规范化出新形式、不从研究草案取名称。
- 主题、实体、来源、数组和受控值的引用目标必须存在。重复路径、悬空引用、非法 ID、未知字段和非空／符号链接输出目标均阻断，不留下目标。
- 导出目录不受 Git 跟踪；真实验证输出只写本计划 ignored 工作区或 `/tmp`。不得提交 848 个生成文件。
- manifest 排除自身条目；`content_files=847`，`total_files=848`。相同输入连续导出逐字节一致，不写时间、绝对路径、用户名或 mtime。
- 本阶段不导入、不回流、不覆盖 live vault、不生成内容单元、不激活正式术语数据、不实现 TBX。
- 只保留能发现错误数据、静默丢失、悬空链接、非确定输出和覆盖用户目录的行为测试。文档、文件存在、常量和包装入口不另造测试。
- 每个代码任务严格 RED／GREEN；每任务提交并执行高价值语义／行为审查。提交说明标 `[L2]`，不得推送、合并或发版。

---

### Task 1: 导出模型

**Files:**

- Create: `scripts/export_obsidian.py`
- Create: `tests/test_export_obsidian.py`

**Interfaces:**

- Produces: `ExportError`；`load_repository(repo_root: pathlib.Path) -> dict`；`build_content_files(repo_root: pathlib.Path) -> dict[str, bytes]`。
- Consumes: 六份正式 YAML 和本模块的固定映射。

- [ ] **Step 1: 写入内容失败测试**

在 `tests/test_export_obsidian.py` 使用真实仓库输入，写两个行为测试。

1. `test_build_content_files_maps_every_formal_object`：调用 `build_content_files(ROOT)`，手工断言返回 847 个唯一路径；对象目录计数精确为 700／24／61／31／6／5／16，且包含三个 `.base` 和根 README。
2. `test_topic_note_uses_flat_properties_and_resolvable_links`：解析 `KB/Topics/security.md` frontmatter，断言所有 property 值只为标量或标量列表，`kb_id=security`、`kb_object=topic`、status／broader／arrays 与正式输入一致；解析正文并确认 basis 和 match 值无损出现；每个 Wikilink 目标在返回集合中存在。

测试导入尚不存在的 `scripts.export_obsidian`，并使用安全 YAML 解析 frontmatter。

- [ ] **Step 2: 运行 RED**

```bash
python3 -m unittest tests.test_export_obsidian -v
```

预期因模块或接口不存在失败；不得因测试数据、导入路径或 YAML 语法错误失败。

- [ ] **Step 3: 实现加载与公共渲染**

实现：

- 六份文件与顶层集合的显式加载；
- 稳定 ID、重复 ID、允许字段和引用目标校验；
- `display_label(record)`：中文、英文、id 的固定回退；
- `aliases(record)`：从 label、alt、hidden 取正式非空形式，排除主显示形式，稳定去重；
- `link(kind, id, label)`：生成 `[[KB/<Kind>/<id>|<label>]]`；
- 固定顺序、无嵌套值的 frontmatter；
- Markdown 表格值和 YAML 文本转义。

未知字段默认 `ExportError`，错误消息包含输入文件、对象 ID 和字段路径。

- [ ] **Step 4: 实现七类对象渲染**

按规格实现 topic、array、entity、source、type、genre、form 的路径、properties 和正文。数组成员从正式主题顺序反向构造；来源用途链接实体；受控值复用公共标签／basis／match 规则。实现三个最小 `.base` 文件和生成目录 README。

`build_content_files()` 返回排序后插入的普通 dict，值均为 UTF-8 bytes、LF、末尾一个换行；不写磁盘。

- [ ] **Step 5: 运行 GREEN**

运行同一 unittest，预期 2 项通过且无警告。删除任一引用目标或把嵌套 dict 放入 property 的临时 mutation 必须使对应测试失败；恢复后重跑 GREEN。

- [ ] **Step 6: 提交导出模型**

```bash
git add scripts/export_obsidian.py tests/test_export_obsidian.py
git commit -m "[L2] Obsidian:建立词表笔记映射"
```

### Task 2: 安全写入

**Files:**

- Modify: `scripts/export_obsidian.py`
- Modify: `tests/test_export_obsidian.py`

**Interfaces:**

- Consumes: `build_content_files()`。
- Produces: `build_manifest(repo_root: pathlib.Path, files: Mapping[str, bytes]) -> bytes`；`write_export(repo_root: pathlib.Path, output: pathlib.Path) -> dict`；CLI `main(argv=None) -> int`。

- [ ] **Step 1: 写入安全失败测试**

增加四个行为测试。

1. `test_write_export_is_deterministic_and_manifest_is_complete`：导出到两个不存在目录，递归逐字节比较；解析 manifest，断言 schema/version、七类计数、847 条 file entries、`content_files=847`、`total_files=848`、每个 SHA-256 和内容集合哈希正确，manifest 不列自身。
2. `test_write_export_rejects_nonempty_output_without_changes`：目标先有 sentinel，调用失败，sentinel 字节不变，无额外文件。
3. `test_write_export_rejects_dangling_reference_without_target`：复制最小正式输入到临时 repo，把一个 broader 改成不存在 ID；调用失败，目标不存在。
4. `test_write_export_rejects_unknown_field_without_target`：在临时输入记录加入未知字段；调用失败，目标不存在。

- [ ] **Step 2: 运行 RED**

运行完整测试模块。预期新增 4 项因 manifest／write 接口不存在失败，Task 1 修正后的 8 项继续通过。

- [ ] **Step 3: 实现 manifest**

实现 canonical JSON。正式输入条目保存路径、version、SHA-256；文件条目按 path 排序，保存 path、object、id、sha256；README 和 Base 使用 object 值 `index`／`base`、id 使用稳定文件 stem。内容集合哈希对按 path 排序的 `path + NUL + sha256 + LF` 字节计算。

`exporter_sha256` 取当前模块实际字节。manifest 不列自身，且不参与内容集合哈希。

- [ ] **Step 4: 实现安全原子写入**

实现输出路径解析与禁止目录检查。先在目标同级用 `tempfile.mkdtemp()` 创建目录，写全部内容、重新读取并核对哈希、解析所有 Markdown frontmatter 和 Base YAML、验证全部链接和 manifest 双向覆盖；成功时：

- 目标不存在：`os.replace(temp, output)`；
- 目标存在且为空：直接尝试 `os.replace(temp, output)`；平台不支持目录替换时失败并保留原空目录，不先删除目标；
- 任一失败：删除本次 temp，目标保持原状态。

非空目录和符号链接在创建 temp 前拒绝。不得递归删除用户目标。

- [ ] **Step 5: 实现 CLI**

命令：

```bash
python3 scripts/export_obsidian.py --repo-root . --output /absolute/new/path
```

成功输出一行 canonical JSON 摘要，包含 output、content_files、total_files 和 content_sha256；失败向 stderr 输出 `OBSIDIAN_EXPORT_ERROR <message>` 并退出 1。输出路径不得写入 manifest。

- [ ] **Step 6: 运行 GREEN**

运行完整测试模块，预期全部通过。复审新增的输入快照、CLI 错误、空符号链接、目录替换失败、写后回读失败、实体依据标题和共享 property 类型门禁必须保留。再对真实仓库执行两个独立 `/tmp` 导出，`diff -ru` 预期无差异；运行 `git status --short`，受跟踪写集只含代码和测试。

- [ ] **Step 7: 提交安全导出**

```bash
git add scripts/export_obsidian.py tests/test_export_obsidian.py
git commit -m "[L2] Obsidian:实现安全确定导出"
```

### Task 3: 应用设计

**Files:**

- Create: `design/targets/obsidian.md`
- Modify: `design/README.md`
- Modify: `README.md`
- Modify: `docs/superpowers/plans/2026-08-31-project-roadmap.md`

**Interfaces:**

- Consumes: 规格和 Tasks 1–2 的实际 CLI、properties、路径、manifest 与失败边界。
- Produces: 项目原生 Obsidian 映射、可发现入口和关闭后的项目路线。

- [ ] **Step 1: 写应用映射**

创建 `design/targets/obsidian.md`，逐项回答内容模型 5 个问题。只记录实现中真实存在的词表导出；内容笔记映射明确为应用契约，不宣称已有内容导出。列文件布局、公共属性、七类对象、内容字段、Bases、manifest、命令、安全、回流边界、未映射字段和验收。

正文链接 Obsidian 官方 properties、links、aliases、data storage、accepted formats 和 Bases syntax 页面；外部文档只支持应用事实，不产生项目字段。

- [ ] **Step 2: 重写设计索引**

整篇重写 `design/README.md`，在现行设计分支登记 Obsidian 应用映射；项目草案保持十份未生效。阅读顺序把应用映射放在内容模型后，不把导出脚本写成正式词表编辑源。

- [ ] **Step 3: 重写项目入口**

整篇重写 `README.md`，更新 `design/targets/`、当前路线和 Obsidian 状态；删除“当前尚未建立”“下一阶段是首轮维护”等旧状态。明确导出命令写新目录、词表单向、内容回流未实现、TBX 后置。

- [ ] **Step 4: 关闭项目路线**

整行同步应用映射目标和“执行顺序”：Obsidian 映射与导出标为当前范围完成；TBX 继续触发式草案，严格来源／术语激活和开放 L2／L3 决定不被误写完成。下一步不再自动进入新阶段，只列条件式后置门禁。

- [ ] **Step 5: 运行最终门禁**

运行：

```bash
python3 -m unittest tests.test_export_obsidian -v
python3 scripts/check_link_baseline.py
python3 scripts/check-topics.py
python3 scripts/check-terms.py --all
git diff --check
git status --short
```

再导出两个真实临时目录并逐字节比较；核对 manifest 848 文件、所有 Markdown frontmatter、Base YAML、内部链接、正式输入哈希和受跟踪写集。全库既有测试红灯只作基线，不扩大本阶段修复。

- [ ] **Step 6: 提交应用设计**

```bash
git add design/targets/obsidian.md design/README.md README.md docs/superpowers/plans/2026-08-31-project-roadmap.md
git commit -m "[L2] Obsidian:完成应用映射与导出"
```
