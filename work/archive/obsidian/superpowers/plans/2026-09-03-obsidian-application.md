# Obsidian 应用实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立一个可以从 `kb-design` 初始化新 Obsidian vault、创建 UUIDv4 内容单元、校验元数据与引用并生成使用报告的独立应用仓库。

**Architecture:** `kb-obsidian` 只实现应用行为，`kb-design` 继续承担概念、正式词表、内容模型和治理规则。应用通过固定设计提交和现有 exporter CLI 消费六份正式词表；用户文件、受管理表示和派生报告使用分离模块与写集，首轮只创建空目标，不更新非空 vault。

**Tech Stack:** Python 3.9+、PyYAML 6、标准库 `argparse`／`dataclasses`／`hashlib`／`json`／`pathlib`／`subprocess`／`tempfile`／`uuid`、`unittest`。

**Spec:** `/Users/xiu/code/kb-design/docs/superpowers/specs/2026-09-02-obsidian-knowledge-base-application-design.md`

## 全局约束

- 设计来源固定为 `/Users/xiu/code/kb-design` 的提交 `356f02bc0a61d28c045139b2dc5f41bf40291a78`；运行时路径由 CLI 参数传入，不硬编码用户目录。
- 设计源必须是 Git 工作区、HEAD 等于支持提交且 tracked 工作树干净；不读取未提交设计。
- 正式主题、实体、来源用途、类型、体裁和载体只从 `kb-design` 正式词表及其 exporter 取得，不在本仓库复制或编辑。
- 新内容 identifier 是无前缀、小写、标准连字符 UUIDv4；文件路径是 `Content/<UUIDv4>.md`。
- 内容 `title` 同时写入一级标题、`title` Text property 和 `aliases` 中恰好一个派生值；人的搜索不依赖 UUID。
- `Inbox/` 和 `Sources/` 不是内容单元；Web Clipper、模板和临时文件不能直接创建正式内容或词表对象。
- 正式计数只读取通过内容校验的受控字段；正文链接、Backlinks、Indexes、aliases、unlinked mentions 和 Graph edges 不进入计数。
- 报告只写 `App/Reports/`，不得修改用户内容、`KB/`、受管理模板／视图／规则、设计源或正式数据。
- 初始化器只接受不存在或为空的目标目录；不实现非空 vault 更新、回流、自动修复、查询日志或社区插件。
- 受管理 manifest 记录设计提交、设计输入 hashes 和受管理文件 hashes；不宣称 JCS、BagIt、reproducible build 或 durability。
- TDD 只用于稳定身份、用户写集、引用语义、状态约束和正式计数等高风险行为；静态模板、目录和固定 JSON 使用直接校验。
- 每个任务提交只含计划列出的文件；提交说明使用 `[L1]`、`[L2]` 或 `[L3]`。

---

### Task 1: 仓库骨架

**Files:**
- Create: `AGENTS.md`
- Create: `README.md`
- Create: `.gitignore`
- Create: `pyproject.toml`
- Create: `src/kb_obsidian/__init__.py`
- Create: `src/kb_obsidian/__main__.py`
- Create: `src/kb_obsidian/errors.py`
- Create: `tests/__init__.py`

**Interfaces:**
- Produces: package `kb_obsidian`, `ApplicationError`, console entry point `kb-obsidian`.
- Consumes: no earlier task.

- [ ] **Step 1: 写仓库约定**

`AGENTS.md` 必须记录本仓库只实现应用、正式数据来自 `kb-design`、用户／管理／报告写集分开、UUIDv4 与元数据搜索规则、无自动回流、审查与测试价值门禁、禁止在 `master` 上实施。

- [ ] **Step 2: 写包配置**

`pyproject.toml` 使用 setuptools：

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "kb-obsidian"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = ["PyYAML>=6,<7"]

[project.scripts]
kb-obsidian = "kb_obsidian.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
```

- [ ] **Step 3: 写错误接口**

`errors.py`：

```python
class ApplicationError(ValueError):
    """User-facing failure that must not leave a partial published result."""
```

`__main__.py` 只调用 `cli.main()`；`__init__.py` 暴露 `__version__ = "0.1.0"`。

- [ ] **Step 4: 写项目入口**

README 说明四个未来命令 `init`、`new-content`、`validate`、`report`，明确当前任务逐步实现，实际知识内容不进入本仓库。

- [ ] **Step 5: 直接验证**

```bash
python3 -m pip install -e .
python3 -c 'import kb_obsidian; assert kb_obsidian.__version__ == "0.1.0"'
git diff --check
```

- [ ] **Step 6: 提交**

```bash
git add AGENTS.md README.md .gitignore pyproject.toml src tests
git commit -m '[L2] 应用:建立仓库骨架'
```

### Task 2: 设计源适配

**Files:**
- Create: `src/kb_obsidian/design_source.py`
- Create: `src/kb_obsidian/reference_export.py`
- Create: `tests/test_design_source.py`
- Create: `tests/fixtures/design/.gitkeep`

**Interfaces:**
- Produces:
  - `SUPPORTED_DESIGN_COMMIT: str`
  - `DesignSnapshot(root: Path, commit: str, documents: Mapping[str, Mapping], input_hashes: Mapping[str, str])`
  - `load_design(root: Path) -> DesignSnapshot`
  - `export_reference(snapshot: DesignSnapshot, output: Path) -> Mapping[str, object]`
- Consumes: `ApplicationError`.

- [ ] **Step 1: 写失败测试**

```python
def test_load_design_requires_supported_clean_git_head(self):
    with self.assertRaisesRegex(ApplicationError, "design HEAD"):
        load_design(self.unsupported_repo)

def test_export_reference_returns_verified_manifest(self):
    snapshot = load_design(DESIGN_ROOT)
    manifest = export_reference(snapshot, self.output)
    self.assertEqual(snapshot.commit, manifest["design_commit"])
    self.assertTrue((self.output / "KB" / "Topics").is_dir())
```

- [ ] **Step 2: 确认失败**

```bash
python3 -m unittest tests.test_design_source -v
```

Expected: import or missing-function failure.

- [ ] **Step 3: 实现设计快照**

`load_design` 必须：

1. 解析绝对路径；
2. 检查 `git rev-parse HEAD` 等于 `356f02bc0a61d28c045139b2dc5f41bf40291a78`；
3. 检查 `git status --porcelain --untracked-files=no` 为空；
4. 一次读取六份 `vocab/*.yaml` bytes；
5. 计算 SHA-256；
6. 使用 `yaml.safe_load` 并返回冻结快照。

- [ ] **Step 4: 复用现行导出器**

`export_reference` 用 `sys.executable` 调用：

```text
<design-root>/scripts/export_obsidian.py --repo-root <design-root> --output <temporary-output>
```

读取根 manifest，验证其中六个 input hashes 与 `DesignSnapshot.input_hashes` 相同，再把 `KB/` 复制到指定空 output。返回值加入 `design_commit`，但不修改上游 manifest bytes。

- [ ] **Step 5: 运行测试**

```bash
python3 -m unittest tests.test_design_source -v
```

Expected: all tests pass; unsupported/dirty design roots fail before export.

- [ ] **Step 6: 提交**

```bash
git add src/kb_obsidian/design_source.py src/kb_obsidian/reference_export.py tests/test_design_source.py tests/fixtures/design/.gitkeep
git commit -m '[L2] 设计源:建立冻结快照适配'
```

### Task 3: 新库初始化

**Files:**
- Create: `src/kb_obsidian/render.py`
- Create: `src/kb_obsidian/managed.py`
- Create: `src/kb_obsidian/vault.py`
- Create: `tests/test_vault_init.py`

**Interfaces:**
- Produces:
  - `render_frontmatter(properties: Mapping[str, object]) -> str`
  - `build_managed_files(snapshot: DesignSnapshot, reference_root: Path) -> Mapping[str, bytes]`
  - `initialize_vault(design_root: Path, target: Path) -> Mapping[str, object]`
- Consumes: `load_design`, `export_reference`, `ApplicationError`.

- [ ] **Step 1: 写安全行为测试**

```python
def test_initialize_vault_refuses_nonempty_target_without_changes(self):
    marker = self.target / "keep.txt"
    marker.parent.mkdir()
    marker.write_text("keep", encoding="utf-8")
    with self.assertRaisesRegex(ApplicationError, "empty"):
        initialize_vault(DESIGN_ROOT, self.target)
    self.assertEqual("keep", marker.read_text(encoding="utf-8"))

def test_initialize_vault_builds_user_managed_and_config_boundaries(self):
    summary = initialize_vault(DESIGN_ROOT, self.target)
    self.assertTrue((self.target / "Home.md").is_file())
    self.assertTrue((self.target / "KB" / "Topics").is_dir())
    self.assertTrue((self.target / "App" / "manifest.json").is_file())
    self.assertEqual("356f02bc0a61d28c045139b2dc5f41bf40291a78", summary["design_commit"])
```

- [ ] **Step 2: 确认失败**

```bash
python3 -m unittest tests.test_vault_init -v
```

- [ ] **Step 3: 实现受管理文件**

生成：

```text
KB/<现有 exporter 文件>
App/Templates/inbox.md
App/Templates/reference.md
App/Views/content.base
App/Views/drafts.base
App/Views/formal-topics.base
App/Views/unassigned-topics.base
App/Rules/README.md
App/manifest.json
```

manifest 保存 schema、app version、design commit、六个 input hashes，以及除自身和 `App/Reports/` 外每个受管理文件的 path、kind 和 SHA-256。

- [ ] **Step 4: 实现用户初始文件**

生成 `Home.md` 和职责目录：`Inbox/`、`Sources/Clippings/`、`Sources/References/`、`Sources/Files/`、`Content/`、`Indexes/`、`Attachments/`、`App/Reports/`。Home 链接到全部必要入口；初始化后不进入 managed manifest。

- [ ] **Step 5: 实现最低配置**

写 `.obsidian/app.json`、`templates.json`、`types.json` 和 `core-plugins.json`。`app.json` 固定 `attachmentFolderPath: "Attachments"` 与 `alwaysUpdateLinks: true`；`templates.json` 固定 `folder: "App/Templates"`。

`core-plugins.json` 只把下列当前核心插件 ID 设为 `true`：

```json
{
  "file-explorer": true,
  "global-search": true,
  "switcher": true,
  "graph": true,
  "backlink": true,
  "page-preview": true,
  "templates": true,
  "command-palette": true,
  "outline": true,
  "file-recovery": true,
  "canvas": true,
  "properties": true,
  "bookmarks": true,
  "bases": true
}
```

`types.json` 使用 `{"types": {...}}`，至少把 `aliases` 设为 `aliases`，日期字段设为 `date`，单值字段设为 `text`，List 字段设为 `multitext`，`tags` 设为 `tags`。配置不包含主题、窗口布局、快捷键、Sync 或社区插件。

- [ ] **Step 6: 实现安全发布**

在目标同级临时目录完成全部写入和回读校验；目标不存在或为空才可进入发布。失败只清理本次临时目录，不递归删除目标。

- [ ] **Step 7: 运行测试**

```bash
python3 -m unittest tests.test_vault_init -v
```

Expected: empty target initializes; nonempty, symlink and protected targets remain unchanged.

- [ ] **Step 8: 提交**

```bash
git add src/kb_obsidian/render.py src/kb_obsidian/managed.py src/kb_obsidian/vault.py tests/test_vault_init.py
git commit -m '[L2] Vault:实现安全初始化'
```

### Task 4: 内容校验

**Files:**
- Create: `src/kb_obsidian/content.py`
- Create: `src/kb_obsidian/validation.py`
- Create: `tests/test_content_validation.py`
- Create: `tests/fixtures/vault-invalid/Content/.gitkeep`

**Interfaces:**
- Produces:
  - `ContentRecord(identifier, title, path, properties, body)`
  - `Issue(code, path, field, message)`
  - `ValidationResult(records, issues)` with `valid_records` and `is_valid`
  - `validate_content(snapshot: DesignSnapshot, vault: Path) -> ValidationResult`
- Consumes: design vocabulary documents and `ApplicationError`.

- [ ] **Step 1: 写稳定身份测试**

```python
def test_valid_content_requires_canonical_uuid_path_and_title_alias(self):
    result = validate_content(self.snapshot, self.vault)
    self.assertTrue(result.is_valid)
    self.assertEqual(self.uuid, result.records[0].identifier)

def test_title_alias_or_stem_drift_is_reported_without_rewrite(self):
    before = self.note.read_bytes()
    result = validate_content(self.snapshot, self.vault)
    self.assertEqual({"content.title_mismatch", "content.path_mismatch"}, {i.code for i in result.issues})
    self.assertEqual(before, self.note.read_bytes())
```

- [ ] **Step 2: 写语义引用测试**

覆盖：恰好一个 type／genre、至少一个非 deprecated subject、form／level 值域、entity target、reference kind、source 的 content/entity 分支、relation 互反、deprecated replacement、重复 UUID。

- [ ] **Step 3: 确认失败**

```bash
python3 -m unittest tests.test_content_validation -v
```

- [ ] **Step 4: 实现解析器**

只读取 `Content/*.md`，解析文件开头 YAML frontmatter、首个一级标题和正文。拒绝嵌套 property 值、未知 `kb_*` 字段、重复键、非规范 Wikilink 和无法解析目标。解析器不修改文件。

- [ ] **Step 5: 实现校验器**

UUID 使用 `uuid.UUID(value).version == 4` 和 `str(parsed) == value`；文件 stem 必须相同。`aliases` 必须是只含 `title` 的单项列表。校验器收集全部 issue，按 path、field、code 排序，不因第一个错误提前停止。

- [ ] **Step 6: 运行测试**

```bash
python3 -m unittest tests.test_content_validation -v
```

Expected: valid sample passes; each high-risk invariant has a focused failing fixture; no file bytes change.

- [ ] **Step 7: 提交**

```bash
git add src/kb_obsidian/content.py src/kb_obsidian/validation.py tests/test_content_validation.py tests/fixtures/vault-invalid/Content/.gitkeep
git commit -m '[L2] 内容:实现只读语义校验'
```

### Task 5: 内容建立

**Files:**
- Create: `src/kb_obsidian/create_content.py`
- Create: `tests/test_create_content.py`

**Interfaces:**
- Produces: `create_content(snapshot, vault, *, title, type_id, genre_id, subjects, form=None, level=None, entities=(), references=(), language="zh", uuid_factory=uuid.uuid4, today=date.today) -> Path`.
- Consumes: content renderer, controlled indexes and validator.

- [ ] **Step 1: 写 UUID 与搜索测试**

```python
def test_create_content_uses_uuid_filename_and_title_search_metadata(self):
    path = create_content(self.snapshot, self.vault, title="主题目录", type_id="explanation", genre_id="analysis", subjects=["controlled-vocabulary"], uuid_factory=lambda: UUID(TEST_UUID))
    self.assertEqual(f"{TEST_UUID}.md", path.name)
    properties, heading = read_note(path)
    self.assertEqual(TEST_UUID, properties["kb_id"])
    self.assertEqual("主题目录", properties["title"])
    self.assertEqual(["主题目录"], properties["aliases"])
    self.assertEqual("主题目录", heading)
```

- [ ] **Step 2: 写安全失败测试**

重复 UUID factory 第一次返回已有值、第二次返回新值时必须重试；无效 subject、deprecated subject、无效 type/genre、空标题和非 vault 目标必须在写入前失败。

- [ ] **Step 3: 确认失败**

```bash
python3 -m unittest tests.test_create_content -v
```

- [ ] **Step 4: 实现建立器**

生成 `status: draft`、当前日期和规范 Wikilink；写到同目录临时文件，回读并通过单文件校验后 `os.replace` 到最终 UUID 路径。失败清理临时文件，不修改已有内容。

- [ ] **Step 5: 运行测试**

```bash
python3 -m unittest tests.test_create_content -v
```

- [ ] **Step 6: 提交**

```bash
git add src/kb_obsidian/create_content.py tests/test_create_content.py
git commit -m '[L2] 内容:实现 UUIDv4 建立流程'
```

### Task 6: 使用报告

**Files:**
- Create: `src/kb_obsidian/reports.py`
- Create: `tests/test_reports.py`

**Interfaces:**
- Produces: `build_reports(snapshot: DesignSnapshot, validation: ValidationResult, vault: Path) -> Mapping[str, bytes]` and `write_reports(...) -> Mapping[str, object]`.
- Consumes: only `ValidationResult.valid_records`; invalid records never enter counts.

- [ ] **Step 1: 写计数边界测试**

```python
def test_topic_counts_use_only_valid_controlled_subjects(self):
    reports = build_reports(self.snapshot, self.validation, self.vault)
    usage = json.loads(reports["App/Reports/topic-usage.json"])
    self.assertEqual(1, usage["direct"]["security"])
    self.assertEqual(0, usage["direct"]["artificial-intelligence"])
```

测试正文链接、Indexes 链接、alias 和 invalid content 不增加 direct count；descendant aggregation 增加上位统计但不改变 direct count 或内容文件。

- [ ] **Step 2: 写报告写集测试**

报告生成失败或成功都不得改变 `Content/`、`KB/`、`App/Templates/`、`App/Views/`、`App/Rules/` 或设计源 hashes。

- [ ] **Step 3: 确认失败**

```bash
python3 -m unittest tests.test_reports -v
```

- [ ] **Step 4: 实现报告**

生成：

```text
App/Reports/validation.json
App/Reports/topic-usage.json
App/Reports/topic-coverage.md
App/Reports/unassigned-topics.md
App/Reports/README.md
```

JSON 使用固定 UTF-8、排序键、两空格缩进和末尾换行；Markdown 列出直接计数、分支聚合、unassigned、零引用和现行 10% 过度使用阈值命中。报告明确标为派生结果和人工复核线索。

- [ ] **Step 5: 安全发布**

先写 `App/.reports-tmp-*`，完成回读和文件集合检查后替换 `App/Reports/`。只清理本次临时目录；不把旧报告作为输入。

- [ ] **Step 6: 运行测试**

```bash
python3 -m unittest tests.test_reports -v
```

- [ ] **Step 7: 提交**

```bash
git add src/kb_obsidian/reports.py tests/test_reports.py
git commit -m '[L2] 报告:实现主题使用与覆盖统计'
```

### Task 7: 命令集成

**Files:**
- Create: `src/kb_obsidian/cli.py`
- Create: `tests/test_cli.py`
- Modify: `README.md`

**Interfaces:**
- Produces commands:
  - `kb-obsidian init --design-root PATH --output PATH`
  - `kb-obsidian new-content --design-root PATH --vault PATH --title TEXT --type ID --genre ID --subject ID...`
  - `kb-obsidian validate --design-root PATH --vault PATH`
  - `kb-obsidian report --design-root PATH --vault PATH`
- Consumes: Tasks 2–6 public functions.

- [ ] **Step 1: 写 CLI 行为测试**

成功 stdout 是一行排序 JSON；用户错误 stderr 以 `KB_OBSIDIAN_ERROR` 开头并退出 1；`--help` 退出 0。测试 init → new-content → validate → report 端到端路径。

- [ ] **Step 2: 确认失败**

```bash
python3 -m unittest tests.test_cli -v
```

- [ ] **Step 3: 实现 CLI**

`main(argv=None) -> int` 只做参数解析、调用和 JSON 输出；业务逻辑不复制到 CLI。捕获 `ApplicationError`、YAML/JSON 解析错误和预期文件错误，保留具体对象路径与字段上下文。

- [ ] **Step 4: 更新使用说明**

README 给出从固定 `kb-design` checkout 初始化新 vault、创建一条 draft、运行校验和生成报告的完整命令。明确 Quick Switcher 通过派生 alias 按标题打开 UUID 文件，Search/Bases 承担元数据查询。

- [ ] **Step 5: 运行测试**

```bash
python3 -m unittest tests.test_cli -v
python3 -m unittest discover -s tests -v
```

Expected: all tests pass with no warnings; only this risk boundary runs the full suite.

- [ ] **Step 6: 提交**

```bash
git add src/kb_obsidian/cli.py tests/test_cli.py README.md
git commit -m '[L2] CLI:集成新库内容与报告流程'
```

### Task 8: 应用验收

**Files:**
- Create: `.superpowers/sdd/2026-09-03-obsidian-application/verification.md`

**Interfaces:**
- Consumes: complete CLI and source tree.
- Produces: ignored verification evidence; no tracked files.

- [ ] **Step 1: 运行完整流程**

在 `mktemp -d` 下运行 init，创建至少两条不同主题内容，运行 validate 和 report；保存 stdout JSON、文件树、manifest hashes 和报告摘要。

- [ ] **Step 2: 验证 Obsidian 文件**

安全解析全部 YAML frontmatter、JSON 和 Base YAML；确认 UUID 文件 aliases 包含标题，Wikilink 目标存在，Home 与 App/Views 入口存在。

- [ ] **Step 3: 验证失败保护**

对副本制造 title/alias 漂移、悬空 subject、重复 UUID 和非空 init 目标；确认各命令失败且用户文件 bytes 不变。

- [ ] **Step 4: 运行最终检查**

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q src tests
git diff --check
git status --short
```

- [ ] **Step 5: 写验收记录**

记录设计提交、应用 HEAD、命令、测试数、实际文件集合、失败保护和未验证边界。若无法自动操作 Obsidian GUI，明确把 Quick Switcher、Bases 交互和视觉布局标为待人工应用验收，不得用 YAML 解析冒充 UI 验证。
