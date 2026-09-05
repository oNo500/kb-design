# Obsidian 文件合同修正实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `kb-design`、`kb-obsidian` 和持久 `kb-vault` 的项目控制路径统一为小写 kebab-case，修正内部链接与报告人机表示，并以完整重建替换错误合同。

**Architecture:** `kb-design` 先确定小写 reference artifact contract，`kb-obsidian` 同时按已批准规格改写完整应用布局；两条生成链完成后，以 `kb-design` 最终提交更新应用 pin 并在同一 disposable vault 汇合。报告目录一次原子发布人读 Markdown 与机器 JSON；持久 vault 只在用户写集仍为空且候选验收通过后切换，旧目录保留为备份。

**Tech Stack:** Python 3.9+、PyYAML 6、Obsidian CLI 1.13.7、`unittest`、Git、标准库文件与 hash 接口。

**Spec:** `docs/superpowers/specs/2026-09-03-obsidian-file-contract-repair-design.md`

## 全局约束

- 项目控制目录与文件使用小写 kebab-case；仅 `.obsidian/` 与另经批准建立的 `AGENTS.md` 允许大写例外。
- 正式对象路径是 `kb/<collection>/<stable-id>.md`；内容路径是 `content/<uuidv4>.md`。
- 生成的 vault 内部链接一律使用 vault 根路径 Wikilink；Markdown link 只用于外部 URL。
- 人读入口只能链接 Obsidian 支持格式；JSON 只位于 `app/reports/data/`，不得进入人读导航。
- `app/reports/` 同时包含人读 Markdown 与机器 JSON，并作为一次原子替换的完整集合。
- 新旧路径不双写，不建立符号链接或大小写兼容目录，不依赖 Obsidian 自动更新链接修复生成物。
- `kb-design` 完成全部正式设计与 exporter 改动并形成最终提交后，`kb-obsidian` 才更新支持提交 pin。
- 不改变概念、designation、正式 ID、关系、内容字段语义、权限、来源或术语状态。
- 测试只覆盖命名唯一性、链接解析与 UI 格式资格、manifest 覆盖、稳定身份、原子报告集合、快照 pin 和持久切换保护。
- 实施不引入插件、MCP、语义索引、自动分类、回流或通用非空 vault 更新。

---

### Task 1: 正式合同与参考导出

**Repository:** `/Users/xiu/code/kb-design`

**Files:**
- Modify: `design/targets/obsidian.md`
- Modify: `scripts/export_obsidian.py`
- Modify: `tests/test_export_obsidian.py`

**Interfaces:**
- Consumes: approved file-contract repair spec and the six existing `vocab/*.yaml` inputs.
- Produces: standalone reference export containing `index.md`, `kb/**`, and `manifest.json`, with every internal link using the lowercase vault-root contract.

- [ ] **Step 1: Rewrite the target sections**

Rewrite the complete file-layout, generated-representation, internal-link, manifest, publication and acceptance sections of `design/targets/obsidian.md`. Do not append a compatibility note. The target must show the lowercase layout, distinguish UI-supported Markdown/Base from machine JSON, and state that legacy uppercase paths are invalid output.

- [ ] **Step 2: Write failing export tests**

Add focused assertions equivalent to:

```python
self.assertTrue((output / "index.md").is_file())
self.assertTrue((output / "kb" / "topics" / "machine-learning.md").is_file())
self.assertTrue((output / "kb" / "views" / "topics.base").is_file())
self.assertFalse((output / "README.md").exists())
self.assertFalse((output / "KB").exists())
```

Scan every generated project-controlled path and fail on uppercase ASCII, spaces, underscores, repeated hyphens or a non-lowercase extension. Parse every generated Markdown file and assert all vault-internal generated links use `[[...]]`, start with `kb/`, and resolve to an actual Markdown or Base target.

- [ ] **Step 3: Verify RED**

Run `python3 -m unittest tests.test_export_obsidian -v`.

Expected: failures identify `README.md`, `KB/`, PascalCase Base names and uppercase Wikilink targets from the old exporter.

- [ ] **Step 4: Rewrite exporter paths**

Replace the output contract in `scripts/export_obsidian.py` as one coherent rewrite:

```text
README.md                 -> index.md
KB/Arrays/                -> kb/arrays/
KB/Entities/              -> kb/entities/
KB/Forms/                 -> kb/forms/
KB/Genres/                -> kb/genres/
KB/Sources/               -> kb/sources/
KB/Topics/                -> kb/topics/
KB/Types/                 -> kb/types/
KB/Views/Topics.base      -> kb/views/topics.base
KB/Views/Entities.base    -> kb/views/entities.base
KB/Views/Sources.base     -> kb/views/sources.base
```

Update manifest identity, path safety, link rendering, file counts and verification to consume only the new paths. Do not emit old aliases.

- [ ] **Step 5: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_export_obsidian -v
python3 scripts/export_obsidian.py --repo-root . --output "$(mktemp -d)/export"
git diff --check
```

Expected: focused suite passes; the disposable export has no legacy path and its manifest covers the lowercase file set.

- [ ] **Step 6: Commit Task 1**

```bash
git add design/targets/obsidian.md scripts/export_obsidian.py tests/test_export_obsidian.py
git commit -m '[L2] Obsidian:统一参考导出路径'
```

### Task 2: 应用核心布局

**Repository:** `/Users/xiu/code/kb-obsidian`

**Files:**
- Modify: `AGENTS.md`
- Modify: `src/kb_obsidian/managed.py`
- Modify: `src/kb_obsidian/reference_export.py`
- Modify: `src/kb_obsidian/vault.py`
- Modify: `src/kb_obsidian/content.py`
- Modify: `src/kb_obsidian/create_content.py`
- Modify: `src/kb_obsidian/validation.py`
- Modify: `tests/test_design_source.py`
- Modify: `tests/test_vault_init.py`
- Modify: `tests/test_vault_binding.py`
- Modify: `tests/test_content_validation.py`
- Modify: `tests/test_create_content.py`

**Interfaces:**
- Consumes: Task 1 lowercase reference export; during parallel development tests may use a temporary local commit value, but the production pin is finalized only in Task 4.
- Produces: lowercase initialized vault, lowercase controlled links, and the same stable content semantics at `content/<uuidv4>.md`.

- [ ] **Step 1: Write failing layout tests**

Rewrite expected paths in the initialization and binding suites, then add one whole-tree naming assertion:

```python
expected = {
    "home.md", "inbox", "sources", "content", "indexes",
    "attachments", "kb", "app", ".obsidian",
}
self.assertEqual(expected, {path.name for path in vault.iterdir()})
```

Assert `.obsidian/app.json` uses `attachments`, `.obsidian/templates.json` uses `app/templates`, Home Wikilinks use lowercase vault-root paths, and the manifest contains no path beginning `KB/` or `App/`.

- [ ] **Step 2: Verify layout RED**

Run `python3 -m unittest tests.test_vault_init tests.test_vault_binding -v`.

Expected: failures identify old directory names, old Home paths, old configuration values and old manifest prefixes.

- [ ] **Step 3: Rewrite managed and vault layout**

Replace the path constants and generated bytes in `managed.py` and `vault.py` with the approved matrix. The managed prefixes become:

```python
{
    "kb/": "reference",
    "app/templates/": "template",
    "app/views/": "view",
    "app/rules/": "rule",
}
```

The user directories become lowercase, the root entry becomes `home.md`, rules entry becomes `app/rules/index.md`, and every generated Home link is a path-qualified Wikilink. Preserve `.obsidian` as the product-fixed configuration directory.

- [ ] **Step 4: Rewrite reference consumption**

Change `reference_export.py` and `managed.py` to verify and copy only the upstream `kb/` tree. Update manifest path classification and formal target expectations; old `KB/` input must fail before publication.

- [ ] **Step 5: Rewrite content paths and references**

Change all content and controlled-reference contracts together:

```text
Content/<uuid>.md    -> content/<uuid>.md
KB/Topics/<id>.md   -> kb/topics/<id>.md
KB/Entities/<id>.md -> kb/entities/<id>.md
KB/Types/<id>.md    -> kb/types/<id>.md
KB/Genres/<id>.md   -> kb/genres/<id>.md
KB/Forms/<id>.md    -> kb/forms/<id>.md
```

Parser issue paths, relation resolution, source branches, readback validation and collision protection must all use the new paths. Do not accept old-case references as compatibility input.

- [ ] **Step 6: Verify content GREEN**

Run:

```bash
python3 -m unittest tests.test_design_source tests.test_vault_init \
  tests.test_vault_binding tests.test_content_validation \
  tests.test_create_content -v
git diff --check
```

Expected: all scoped tests pass and no production or fixture path retains the old contract.

- [ ] **Step 7: Commit Task 2**

```bash
git add AGENTS.md src/kb_obsidian tests/test_design_source.py \
  tests/test_vault_init.py tests/test_vault_binding.py \
  tests/test_content_validation.py tests/test_create_content.py
git commit -m '[L2] Vault:统一应用路径合同'
```

### Task 3: 报告人机分层

**Repository:** `/Users/xiu/code/kb-obsidian`

**Files:**
- Modify: `src/kb_obsidian/reports.py`
- Modify: `tests/test_reports.py`

**Interfaces:**
- Consumes: Task 2 lowercase `app/` and `content/` paths plus `ValidationResult.valid_records`.
- Produces: one atomic `app/reports/` tree containing five Markdown files and two JSON files under `data/`.

- [ ] **Step 1: Write failing report tests**

Freeze the exact report set:

```python
expected = {
    "app/reports/index.md",
    "app/reports/validation.md",
    "app/reports/topic-usage.md",
    "app/reports/topic-coverage.md",
    "app/reports/unassigned-topics.md",
    "app/reports/data/validation.json",
    "app/reports/data/topic-usage.json",
}
self.assertEqual(expected, set(build_reports(snapshot, validation, vault)))
```

Assert `index.md` contains exactly four path-qualified Wikilinks to Markdown reports, contains no Markdown internal link and no `.json` target, and that human validation/topic-use rows carry the same issue IDs and topic counts as their JSON counterparts.

- [ ] **Step 2: Verify report RED**

Run `python3 -m unittest tests.test_reports -v`.

Expected: old five-file report mapping, JSON navigation and uppercase `App/Reports` fail.

- [ ] **Step 3: Rewrite report builders**

Create deterministic `_validation_markdown` and `_topic_usage_markdown` builders from the same in-memory structures used by `_json_bytes`. Render `index.md` with:

```md
- [[app/reports/validation|内容校验]]
- [[app/reports/topic-usage|主题使用]]
- [[app/reports/topic-coverage|主题覆盖]]
- [[app/reports/unassigned-topics|主题复核]]
```

Keep the existing report-only and no-automatic-action statements in every human report.

- [ ] **Step 4: Preserve atomic publication**

Rewrite report-tree validation to allow the exact nested `data/` directory and reject every extra file, symlink or mismatched byte. Keep Darwin atomic directory exchange for replacing the complete `app/reports/` tree; failed rollback must preserve the old tree recovery path.

- [ ] **Step 5: Verify report GREEN**

Run `python3 -m unittest tests.test_reports -v` followed by `git diff --check`.

Expected: deterministic seven-file set, human/machine parity and failure preservation pass.

- [ ] **Step 6: Commit Task 3**

```bash
git add src/kb_obsidian/reports.py tests/test_reports.py
git commit -m '[L2] 报告:分离人读与机器表示'
```

### Task 4: 快照固定与文档同步

**Repositories:** `/Users/xiu/code/kb-design`, then `/Users/xiu/code/kb-obsidian`

**Files:**
- Modify: `docs/superpowers/specs/2026-09-03-obsidian-cli-agent-design.md`
- Modify: `AGENTS.md` and `README.md` in `kb-design` only when they contain old application paths
- Modify: `src/kb_obsidian/design_source.py`
- Modify: `tests/test_design_source.py`
- Modify: `tests/test_cli.py`
- Modify: `README.md` and `AGENTS.md` in `kb-obsidian`

**Interfaces:**
- Consumes: committed Task 1 final `kb-design` HEAD and committed Tasks 2–3 application interfaces.
- Produces: one exact supported design commit and user-facing docs containing only the corrected paths.

- [ ] **Step 1: Synchronize the terminal spec**

Rewrite every old path in the terminal-access spec, preserving its Obsidian CLI evidence and timeout boundaries. Add the human/JSON report split and state that terminal AI may read `app/reports/data/*.json` but human navigation only opens Markdown.

- [ ] **Step 2: Close the design commit**

Run the scoped design checks and commit all remaining `kb-design` documentation changes:

```bash
python3 -m unittest tests.test_export_obsidian -v
python3 scripts/check-links.py
git diff --check
git add design/targets/obsidian.md \
  docs/superpowers/specs/2026-09-03-obsidian-cli-agent-design.md \
  AGENTS.md README.md scripts/export_obsidian.py tests/test_export_obsidian.py
git commit -m '[L2] Obsidian:同步文件合同入口'
git rev-parse HEAD
```

If AGENTS or README does not contain an affected statement, do not edit or stage it. The resulting commit is the only new `SUPPORTED_DESIGN_COMMIT` value.

- [ ] **Step 3: Update the application pin**

Set `SUPPORTED_DESIGN_COMMIT` in `kb-obsidian/src/kb_obsidian/design_source.py` to the exact 40-character hash from Step 2. Replace all old expected hashes in design-source and CLI tests; do not accept a range or branch name.

- [ ] **Step 4: Rewrite application documentation**

Rewrite the layout, command examples and ownership sections of `kb-obsidian/README.md` and `AGENTS.md` so all project paths use the corrected contract. Explain Markdown human reports and JSON machine reports separately.

- [ ] **Step 5: Run the integration suite**

Run:

```bash
python3 -m unittest discover -s tests
python3 -m compileall -q src tests
git diff --check
```

Expected: all application tests pass against the exact clean `kb-design` HEAD.

- [ ] **Step 6: Commit Task 4**

```bash
git add AGENTS.md README.md src/kb_obsidian/design_source.py \
  tests/test_design_source.py tests/test_cli.py
git commit -m '[L2] 应用:固定修正后的设计快照'
```

### Task 5: 候选 Vault 验收

**Repositories:** read-only use of both repositories; candidate under `/Users/xiu/code`.

**Files:**
- Create ignored evidence under `kb-obsidian/.superpowers/sdd/2026-09-03-obsidian-file-contract-repair/verification.md`
- No tracked-file edits unless a Blocker or Important acceptance failure is reproduced.

**Interfaces:**
- Consumes: exact clean `kb-design` pin and complete `kb-obsidian` CLI.
- Produces: a disposable candidate vault that passes the new file contract.

- [ ] **Step 1: Generate a candidate**

Create a same-parent candidate directory with `mktemp -d /Users/xiu/code/.kb-vault-candidate.XXXXXX`, then run `kb-obsidian init` against the corrected design commit. Do not point initialization at the persistent vault.

- [ ] **Step 2: Verify names and links**

Mechanically assert:

```text
no uppercase project-controlled path except .obsidian and AGENTS.md
no spaces or underscores in project-controlled generated paths
no legacy KB, App, Content, Home.md or README.md
all internal generated links are path-qualified Wikilinks
all human navigation targets have .md or .base effective formats
all machine JSON is under app/reports/data and absent from index.md
```

Parse YAML, JSON and Base files, verify the manifest bidirectionally, and run `obsidian unresolved total` after registering or opening the candidate vault.

- [ ] **Step 3: Exercise content and reports**

Create two UUIDv4 content records with different real topics, run validate and report, then verify:

```text
content/<uuid>.md paths
lowercase controlled Wikilinks
validation.md and validation.json issue parity
topic-usage.md and topic-usage.json count parity
report refresh changes only app/reports
```

- [ ] **Step 4: Verify UI opening**

Use Obsidian CLI to open `home.md`, every Home target, `app/reports/index.md`, four human reports and the Base entries. Inspect `workspace` after each class and prove none becomes an empty tab. Do not use `links` alone as UI-open evidence.

- [ ] **Step 5: Run final repository checks**

Run both risk-boundary suites, compile checks and clean-status checks. Record exact commits, test counts, candidate path, file counts, link counts and UI-open results in the ignored verification file.

### Task 6: 持久 Vault 切换

**Target:** `/Users/xiu/code/kb-vault`

**Files:**
- Existing persistent vault is external user state, not a Git worktree.
- Preserve old vault at `/Users/xiu/code/kb-vault-backup-<timestamp>`.

**Interfaces:**
- Consumes: Task 5 accepted candidate and a fresh user-write-set inventory.
- Produces: persistent `kb-vault` using the corrected file contract, with a recoverable old-vault backup.

- [ ] **Step 1: Recheck user state**

Hash and list every file under old `Inbox`, `Sources`, `Content`, `Indexes`, `Attachments` and their lowercase equivalents. If any user file exists, stop automatic cutover, keep the candidate, and report an explicit migration list.

- [ ] **Step 2: Preserve configuration evidence**

List `.obsidian` files and compare them with candidate baseline configuration. Do not copy `workspace.json`, `appearance.json`, plugin state or unknown settings automatically. Record which files will be left only in the backup.

- [ ] **Step 3: Quiesce and switch**

Ensure no generation or report command is writing the vault. Rename the old vault to the timestamped backup, rename the accepted same-parent candidate to `/Users/xiu/code/kb-vault`, and restore the backup name if the second rename fails. Never recursively delete either directory.

- [ ] **Step 4: Reopen and verify**

Open the new path in Obsidian, verify `obsidian vaults verbose`, then repeat the Home, report, Base, content creation, validate, report, manifest and unresolved-link checks on the persistent path.

- [ ] **Step 5: Report residual state**

Report the exact new vault path, backup path, application commit, design commit, test counts and any personal configuration not copied. Keep the backup until the user separately authorizes deletion.

### Task 7: 分支收口

**Repositories:** both Git repositories.

**Files:** no planned content changes.

**Interfaces:**
- Consumes: complete verified implementation and persistent-vault evidence.
- Produces: clean feature branches ready for user-selected integration.

- [ ] **Step 1: Run final high-value review**

Review only cross-repository snapshot binding, naming matrix, human/machine report parity, user-write-set preservation and UI-openability. Mechanical counts and formatting are proved by commands and are not independently re-reviewed.

- [ ] **Step 2: Fix only Blocker or Important findings**

Allow one bounded fix wave. Any new architecture question stops implementation and returns to the user; Minor findings are recorded without extending this phase.

- [ ] **Step 3: Re-run verification**

Re-run the two full suites, candidate/persistent link checks, compile checks, `git diff --check` and branch status after the last tracked commit.

- [ ] **Step 4: Present integration choices**

Keep both feature branches unmerged until the user chooses local merge, push and pull request, or preservation as-is. Do not delete the persistent vault backup as part of Git branch cleanup.
