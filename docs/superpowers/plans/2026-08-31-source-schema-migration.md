# 来源迁移计划 (Source Schema Migration Implementation Plan)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans in the current session. 只有写集互斥且没有顺序依赖的实现任务使用 superpowers:dispatching-parallel-agents。审查和回归按本计划的阶段门禁执行，不恢复逐任务复审。Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不自动裁定来源身份、用途、依据、派生或映射语义的前提下，建立来源实体与用途模式、共享引用结构、反向引用、复核义务、只读探测、可审计迁移预演和原子切换能力。

**Architecture:** `vocab/entities.yaml` 继续保存唯一来源实体身份，`vocab/sources.yaml` 只保存用途角色，`basis`、`source`、`match` 共享结构由来源治理模式统一校验。离线校验、反向索引、联网探测和迁移器分别实现；迁移批次在决定获准后生成可复核账本与候选树，只有全部语义门禁关闭并另获批准后，才在一个原子提交中切换正式数据、生成输入、生成器和校验器。

**Tech Stack:** Python 3.9.6、PyYAML 6.0.3、[jsonschema 4.23.0](https://pypi.org/project/jsonschema/4.23.0/)、JSON Schema Draft 2020-12、`unittest`、YAML、JSON、Markdown、Git。

**Spec:** [术语治理设计](../specs/2026-08-27-terminology-governance-design.md)、[来源治理草案](../../../design/drafts/source-governance.md)、[术语治理草案](../../../design/drafts/terminology-governance.md)、[来源计划输入](../../../.superpowers/sdd/2026-08-31-governance-implementation-prep/source-plan-input.md)

## 全局约束

- 只在 `/Users/xiu/code/kb-design` 的 `feat/terminology-governance` 分支执行；每批开始时验证 `HEAD` 与冻结输入，不创建 worktree，不修改 `master`。
- 两份治理草案内容已经获人接受，但仍未生效。本计划是实施提案，不批准模式、生效、来源身份、来源用途、迁移、改档、术语准入、范围、回退或发版。
- 人在“决定锁”对应项目给出 accepted patches 前，只允许运行只读基线命令；受跟踪与 ignored 写集均为零，不得创建 schema、测试、夹具、候选树、报告、数据、脚本、设计、决定记录或生成物。
- `basis`、`source` 和 `match` 的语义与字段只取自来源治理草案。术语数据只能消费该接口，不得定义第二套来源引用结构。
- 来源实体、用途角色、外部状态、项目工作流、现行 `tier`、外部证据、实际派生、概念映射和项目决定分别处理；名称、URL、相同代码、消费者数量和现行字段名都不能自动给出语义结论。
- 当前阶段零自定。来源标签、题名、转录、代码和值不因迁移成为可复用项目概念名称；任何术语准入另走术语治理与人的决定。
- 31 个现行来源实体的 `id` 全部冻结。迁移不得复用已发布 `id`，不得删除或改写既有决定与历史，不得用新摘要覆盖旧审计材料。
- 本计划不改变任何来源的 `tier`，不改变知识库范围；来源草案只在 `decision-source-0004` 的独立 L3 决定后生效；术语草案与三份旁路草案保持未生效；不实现 TBX、Obsidian、应用映射、导入或往返编辑。
- 离线校验不得联网；联网探测只读 `watch` 与获准地址，输出到 ignored 运行目录，正式项目写集必须为零。
- 正式文档改动涉及一节以上时，先列旧节去向，再按目的整节或整篇重写并逐项核销；不得顺手修复 31 个标题债务、8 个只追加旧标题或 2 个旧 SDD 链接。
- 生成输入先于生成输出。`scripts/build-topics.py`、`vocab/build/` 与 `vocab/topics.yaml` 必须在同一切换批次对账，连续两次生成逐字节一致。
- 只有“验证矩阵”保留的高风险行为测试使用 RED／GREEN；文档、静态模式、确定性数据和纯机械迁移使用直接解析、schema、哈希、差异或端到端门禁，不为 TDD 形式另造测试。每个任务运行定向检查、核对写集、说明回滚边界并提交。全量回归只在离线校验、迁移预演、文档分流和原子切换四个阶段结束时运行；机械事实不另派独立复审。提交说明标注本批最高决策级别。
- 冻结库存中的身份、旧值、旧哈希、文件、字段路径、消费者和既有分类由程序无损继承。只有新增或改变外部状态、实体边界、角色批准、正式 `basis`、实际派生、概念关系、删除或正式效力时，才需要 identity／field 级人工决定。
- 任何任务的人工门禁未满足时，执行者记录阻断并停止该任务；不得采用计划推荐、空值、兼容字段或迁移分类冒充人的批准。

---

## 输入锁

直接计划输入的 SHA-256 为 `56087db27519ea4d700e9010500c5d3cee69dd742fd538d4296e5c26cd02d69a`。它绑定分支 `feat/terminology-governance` 的提交 `9e7b411c23e890d13d70fc16d443b760313126c4`，并登记下列 18 个依赖哈希。

| 输入 | SHA-256 |
|---|---|
| `docs/superpowers/plans/2026-08-31-governance-implementation-prep.md` | `28b936359d49f5c8618d2dff63740497a766da43931fa4f47b7ad6dd9c232ecd` |
| `design/drafts/source-governance.md` | `0bc61207215f35065652bb66f043ef2d11a807bbe0bc44465814e469b5671526` |
| `design/drafts/terminology-governance.md` | `2d48c869b8a2119346739303accaaff0cbe40418d7074f29a4a18599950767d7` |
| `source-entities.tsv` | `843d3606407264e8d6ccca9ae8b9f03590aa403f98101c4a53a780bab5dc37f4` |
| `source-entities.md` | `10b76c321c28d611c33e1f1a41e27cb61005cfd7f5c226b74854119e749d9f06` |
| `source-roles.tsv` | `f291027de735d21aa21fd953a7301db9d7fcc34a6ec9d266e12ceab07e030cb9` |
| `source-roles.md` | `82fe12c4685ce2cd50900110a74234b3c1a3ad37a85eb4f6d1d6393ae6fc7601` |
| `basis-inventory.tsv` | `3da438227ee676f0d2c5e31ac16c73a3bb4a5d10716b15f175fd81257642c43c` |
| `basis-inventory.md` | `ed8c041a2b180a7a94fd73d68e2e847c175f2b5cb91af4aaf9e788fcd7ef8efb` |
| `source-inventory.tsv` | `0cb9b6df2f218629eb0dedb05ac5c83030b89e4d8dbca7580a8ccfee4b323c1f` |
| `source-inventory.md` | `57e5266910356d811a906a0b4b8cec7110ec05dcf8e9ebf650bed090461bd310` |
| `match-inventory.tsv` | `3f9701f6c2ef64a5d3c5a18144fc052f91e80d11384bb4023c85c74381d5d988` |
| `match-inventory.md` | `0d634286ffa5e4b6885b21b8ad9d68c39a33723fd8be6a4d55385f629d19b1ce` |
| `origin-inventory.tsv` | `06d0df76aa5ac7bd63cfe107ac52a5e712223f251e362b3bb9a0f4d95cbd1e3d` |
| `origin-inventory.md` | `5407ac17ed5f61a08bf4b957f4dc4d9ef5fb135a789e1e73444fb577a69a604a` |
| `generation-baseline.md` | `70388f7a105e69de2397a030d2d1dfb41d6e8ef6a59a43f502fd69126b97ed2e` |
| `maintenance-baseline.md` | `494bb0e3d85700cc1860537eea8bb2e8c376619041b1277958a1544351f3383b` |
| `quality-debt.md` | `9a0bcbf0aca72283761c97750b2afbaa598fd97277e11373f151e3a18a5e2660` |

冻结口径为 138 个来源身份（31 个现行实体与 107 个未登记身份）、47 个用途角色、1,496 个正式 `basis` 叶值、726 个直接 `source` 字段、756 个 `match`、正式数据中的 0 个 `origin` 值、700 个主题概念和 24 个数组。所有验收按稳定身份逐项比较，不只比较总数。

## 文件职责

以下写集只在对应决定获准后的后续执行中生效。

| 文件 | 操作 | 单一职责 |
|---|---|---|
| `requirements-dev.txt` | 创建 | 锁定 Python 3.9 可用的 `PyYAML==6.0.3` 与 `jsonschema==4.23.0` |
| `schemas/source-entities.schema.json` | 创建 | 校验 `vocab/entities.yaml` 及其中 standard/publication 来源实体 |
| `schemas/source-uses.schema.json` | 创建 | 校验 `vocab/sources.yaml` 的用途、角色、状态、决定和历史 |
| `schemas/source-obligations.schema.json` | 创建 | 校验来源复核义务及只追加生命周期 |
| `schemas/source-reference-index.schema.json` | 创建 | 校验确定性反向引用索引 |
| `schemas/source-probe.schema.json` | 创建 | 校验 ignored 探测观察，不赋予正式事实效力 |
| `schemas/source-migration.schema.json` | 创建 | 校验六份迁移账本、处置枚举和冻结身份 |
| `schemas/decision.schema.json` | 创建 | 校验来源决定记录的 front matter、状态、级别和替代引用 |
| `scripts/source_model.py` | 创建 | 提供共享类型、加载、模式校验、引用与历史比较接口 |
| `scripts/check_sources.py` | 创建 | 执行纯离线来源校验并输出稳定问题列表 |
| `scripts/check_link_baseline.py` | 创建 | 把恰有两条冻结旧 SDD 链接失败转换为零退出门禁 |
| `scripts/build_source_index.py` | 创建 | 从正式文件确定性生成逐字段反向引用索引 |
| `scripts/probe_sources.py` | 创建 | 执行受限只读探测并只写指定 ignored 目录 |
| `scripts/plan_source_migration.py` | 创建 | 从冻结库存和 accepted DecisionPatch 生成六份迁移账本与候选写集 |
| `scripts/apply_source_migration.py` | 创建 | 在临时根目录应用已关闭阻断项的账本并验证原子写集 |
| `tests/test_source_schema.py` | 创建 | 覆盖模式正反例与共享引用结构 |
| `tests/test_check_sources.py` | 创建 | 覆盖离线语义门禁、历史与状态转换 |
| `tests/test_source_index.py` | 创建 | 覆盖索引完整性、双向性和稳定字段路径 |
| `tests/test_probe_sources.py` | 创建 | 覆盖六类探测、权限和正式写集隔离 |
| `tests/test_source_migration.py` | 创建 | 覆盖库存身份、分流、迁移账本、回滚和阻断 |
| `tests/test_build_topics_sources.py` | 创建 | 覆盖生成器不会恢复旧 `basis`、`source`、`match` 和数组来源接口 |
| `tests/test_source_obligations.py` | 创建 | 覆盖来源义务创建、结清、再触发和术语衔接 |
| `tests/test_source_docs.py` | 创建 | 覆盖 19 个 `origin` 身份的整节去向和冻结质量债务边界 |
| `tests/test_source_cutover.py` | 创建 | 覆盖严格模式、身份对账、原子切换和发版前停止 |
| `tests/source_governance_helpers.py` | 创建 | 保存跨来源测试文件共享的 ReferenceUse 与 YAML 夹具辅助函数 |
| `tests/fixtures/source-governance/` | 创建 | 保存模式、状态、探测、索引和迁移的最小真实风险夹具 |
| `vocab/migrations/source-v1/entities.yaml` | 创建 | 对账 138 个来源身份及 16 个身份歧义 |
| `vocab/migrations/source-v1/uses.yaml` | 创建 | 对账 47 个角色及 5 个旧 `candidate` |
| `vocab/migrations/source-v1/basis.yaml` | 创建 | 对账 1,496 个正式值、1 个生成配置值和 4 个文档展示值 |
| `vocab/migrations/source-v1/source.yaml` | 创建 | 对账 726 个直接字段及 692／24／8／2 分流 |
| `vocab/migrations/source-v1/match.yaml` | 创建 | 对账 756 个映射及逐项关系依据 |
| `vocab/migrations/source-v1/origin.yaml` | 创建 | 对账 19 个规则、过程、示例与零使用身份 |
| `vocab/source-obligations.yaml` | 创建 | 保存正式来源复核义务，不保存目标字段的新值 |
| `vocab/generated/source-reference-index.json` | 生成 | 保存可复现的逐字段反向引用，不成为编辑源 |
| `vocab/generated/source-cutover-payload.json` | 完整候选后生成并先行绑定 | 只保存无自引用的待应用正式路径与 candidate after SHA-256 |
| `vocab/generated/source-cutover-handoff.json` | payload 后生成并先行绑定 | 保存 payload 绑定、来源契约、七份 schema、主题、账本、Markdown、输出与写集 |
| `vocab/entities.yaml` | 原子切换时修改 | 继续保存唯一实体记录，对 standard/publication 应用来源实体模式 |
| `vocab/sources.yaml` | 原子切换时修改 | 保存用途记录和逐角色状态，不保存实体状态 |
| `vocab/topics.yaml` | 原子切换时生成 | 消费获准共享引用结构，不手工编辑生成结果 |
| `vocab/forms.yaml`、`vocab/types.yaml`、`vocab/genres.yaml` | 原子切换时修改 | 迁移本文件中获准的 `basis`、`source` 和 `match` |
| `vocab/build/extra-arrays.json` | 原子切换时修改 | 保存获准数组分组输入，不使用旧来源名称标量冒充实际派生 |
| `scripts/build-topics.py` | 原子切换时修改 | 从迁移后的输入写出新共享结构并保留确定性 |
| `scripts/check-topics.py` | 原子切换时修改 | 调用新来源校验，不再恢复或接受旧紧缩结构 |
| `design/decisions/source-governance-schema.md` | 门禁后创建 | 记录 `decision-source-0001` 的模式与路径决定 |
| `design/decisions/source-validation-policy.md` | 门禁后创建 | 记录 `decision-source-0009` 的离线校验控制规则，不填写真实来源结论 |
| `design/decisions/source-identity-boundaries.md` | 门禁后创建 | 记录 `decision-source-0002` 的身份判据与逐项结论 |
| `design/decisions/source-role-uses.md` | 门禁后创建 | 记录 `decision-source-0003` 的 47 个逐角色结论 |
| `design/decisions/source-governance-effective.md` | 生效时创建 | 记录 `decision-source-0004` 的草案生效边界 |
| `design/decisions/source-schema-cutover.md` | 切换前创建 | 记录 `decision-source-0005` 对 handoff 与 payload 两组 path／SHA-256 的绑定 |
| `design/decisions/source-schema-rollback.md` | 切换前创建 | 记录 `decision-source-0006` 的回退触发和审计保留 |
| `design/decisions/source-schema-rollback-result.md` | 触发回退时创建 | 记录 `decision-source-0008` 的补偿结果，不删除先行决定或历史 |
| `design/decisions/source-schema-release.md` | 发版时创建 | 记录 `decision-source-0007` 的独立发版决定 |
| `design/source-governance.md` | 生效批次创建 | 保存生效后的来源规则；未生效时不得创建 |
| `design/governance.md`、`design/maintenance.md`、`design/entities.md`、`design/sources-registry.md`、`design/topics.md`、`design/content-model.md`、`design/principles.md`、`design/README.md`、`AGENTS.md`、`README.md` | 生效与切换批次整节重写 | 移除与生效规则冲突的旧接口并同步摘要 |
| `.superpowers/sdd/2026-08-31-source-schema-migration/` | ignored 运行写入 | 保存输入复核、探测观察、候选树、快照、差异、命令输出和失败证据 |

## 接口锁

共享来源契约只在 `scripts/source_model.py` 实现。来源任务、术语任务和未来消费者都直接导入该模块；任何消费者侧适配器、重复枚举或第二套引用解析都视为接口错误。

模式标识如下。

七份 schema 的 `$id`、正式数据 `schema` 和版本固定如下。现行发布元数据 `version.id: "2026.08"` 在独立发版决定前不变；schema 版本不冒充词表发版。

| 文件 | JSON Schema `$id` | 正式数据 `schema` | 版本 |
|---|---|---|---:|
| `schemas/source-entities.schema.json` | `urn:kb-design:schema:source-entities:2` | `urn:kb-design:data:entities` | 2 |
| `schemas/source-uses.schema.json` | `urn:kb-design:schema:source-uses:2` | `urn:kb-design:data:source-uses` | 2 |
| `schemas/source-obligations.schema.json` | `urn:kb-design:schema:source-obligations:1` | `urn:kb-design:data:source-obligations` | 1 |
| `schemas/source-reference-index.schema.json` | `urn:kb-design:schema:source-reference-index:1` | `urn:kb-design:data:source-reference-index` | 1 |
| `schemas/source-probe.schema.json` | `urn:kb-design:schema:source-probe:1` | `urn:kb-design:data:source-probe` | 1 |
| `schemas/source-migration.schema.json` | `urn:kb-design:schema:source-migration:1` | `urn:kb-design:data:source-migration` | 1 |
| `schemas/decision.schema.json` | `urn:kb-design:schema:decision:1` | `urn:kb-design:data:decision` | 1 |

`schemas/source-entities.schema.json#/$defs/basisItem` 是唯一 `basis` 项定义；`schemas/source-migration.schema.json#/$defs/source` 与 `#/$defs/match` 是唯一派生和映射定义。术语 schema 只用这三个本地 URN `$ref`，不复制字段。

共享类型如下。

`scripts/source_model.py` 必须公开下列 Python 3.9 类型和签名，字段顺序属于契约。

```python
from pathlib import Path
from typing import Dict, List, Literal, NamedTuple, Optional, Sequence

ReferenceKind = Literal["basis", "source", "match", "external_group"]
SCHEMA_IDS = {
    "source-entities.schema.json": "urn:kb-design:schema:source-entities:2",
    "source-uses.schema.json": "urn:kb-design:schema:source-uses:2",
    "source-obligations.schema.json": "urn:kb-design:schema:source-obligations:1",
    "source-reference-index.schema.json": "urn:kb-design:schema:source-reference-index:1",
    "source-probe.schema.json": "urn:kb-design:schema:source-probe:1",
    "source-migration.schema.json": "urn:kb-design:schema:source-migration:1",
    "decision.schema.json": "urn:kb-design:schema:decision:1",
}
ROLE_QUALIFICATIONS = {"basis": None, "source": "structure", "match": "mapping",
                       "external_group": "structure"}
ERROR_CODES = (
    "SOURCE_SCHEMA_INVALID", "SOURCE_REFERENCE_KIND_INVALID",
    "SOURCE_REFERENCE_VALUE_INVALID", "SOURCE_ENTITY_MISSING", "SOURCE_USE_MISSING",
    "SOURCE_ROLE_NOT_APPROVED", "SOURCE_ROLE_DECISION_MISSING",
    "SOURCE_BASIS_LOCATOR_MISSING", "SOURCE_BASIS_CHECKED_MISSING",
    "SOURCE_SOURCE_ITEM_MISSING", "SOURCE_SOURCE_LOCATOR_MISSING",
    "SOURCE_SOURCE_BASIS_MISSING", "SOURCE_MATCH_REL_INVALID",
    "SOURCE_MATCH_BASIS_MISSING", "SOURCE_STABLE_ID_CHANGED",
    "SOURCE_HISTORY_NOT_APPEND_ONLY", "SOURCE_OBLIGATION_REOPENED",
    "SOURCE_OBLIGATION_TARGET_MISSING", "SOURCE_DECISION_MISSING",
    "SOURCE_LEGACY_FIELD", "SOURCE_INDEX_MISMATCH", "SOURCE_PROBE_FORMAL_WRITE",
    "SOURCE_EXTERNAL_GROUP_ROLE_NOT_APPROVED", "SOURCE_CUTOVER_MANIFEST_INVALID",
    "SOURCE_DECISION_DELIVERY_MISSING", "SOURCE_DECISION_PATCH_CONFLICT",
)

class Issue(NamedTuple):
    code: str
    file: str
    record: str
    field_path: str
    message: str

class ReferenceUse(NamedTuple):
    kind: ReferenceKind
    file: str
    record: str
    field_path: str
    value: object

class DecisionPatch(NamedTuple):
    identity: str
    field: str
    value: object
    qid: str

class ApplyResult(NamedTuple):
    written: Sequence[str]
    blocked: Sequence[str]

def validate_references(root: Path,
                        references: Sequence[ReferenceUse]) -> List[Issue]:
    return _validate_references(root, references)

def collect_reference_uses(file: Path, document: object) -> List[ReferenceUse]:
    return list(_walk_reference_uses(file, document))

def _format_reference_path(parts) -> str:
    value = ""
    for part in parts:
        value += f"[{part}]" if isinstance(part, int) else (("." if value else "") + part)
    return value

def _has_exact_keys(value, required) -> bool:
    return isinstance(value, dict) and required <= set(value)

def _walk_reference_uses(file: Path, value: object, path=(),
                         record: str = "document"):
    if isinstance(value, dict):
        current_record = record
        if isinstance(value.get("id"), str):
            collection = ".".join(str(part) for part in path[:-1]) or "root"
            current_record = f"{collection}:{value['id']}"
        for key, nested in value.items():
            child = path + (key,)
            if key == "basis" and isinstance(nested, list):
                for index, item in enumerate(nested):
                    if _has_exact_keys(item, {"entity", "locator"}):
                        yield ReferenceUse("basis", str(file), current_record,
                                           _format_reference_path(child + (index,)), item)
            elif key == "source" and _has_exact_keys(
                    nested, {"registry", "item", "locator", "basis"}):
                yield ReferenceUse("source", str(file), current_record,
                                   _format_reference_path(child), nested)
            elif key == "match" and isinstance(nested, list):
                for index, item in enumerate(nested):
                    if _has_exact_keys(item, {"registry", "item", "rel", "basis"}):
                        yield ReferenceUse("match", str(file), current_record,
                                           _format_reference_path(child + (index,)), item)
            elif key == "external_group" and _has_exact_keys(
                    nested, {"registry", "item", "locator", "basis"}):
                yield ReferenceUse("external_group", str(file), current_record,
                                   _format_reference_path(child), nested)
            yield from _walk_reference_uses(file, nested, child, current_record)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            yield from _walk_reference_uses(file, nested, path + (index,), record)

def validate_repository(root: Path,
                        previous_root: Optional[Path] = None,
                        allow_legacy: bool = False) -> List[Issue]:
    references = collect_repository_references(root, allow_legacy)
    issues = validate_references(root, references)
    issues.extend(validate_repository_objects(root, previous_root, allow_legacy))
    return sort_issues(issues)
```

`ReferenceUse` 的构造规则固定如下。

- `basis`：每个 basis item 单独构造一项，`value` 是含 `entity`、`locator` 和可选 `checked` 的对象，`field_path` 指到该 item。
- `source`：每个记录级 source 对象构造一项，`value` 含 `registry`、`item`、`locator`、非空 `basis`，`field_path` 指到 source 对象。
- `match`：每个 match item 单独构造一项，`value` 含 `registry`、`item`、`rel`、非空 `basis`，`field_path` 指到该 item。
- `external_group`：每个数组级 external_group 对象构造一项，`value` 含 `registry`、`item`、`locator`、非空 `basis`，`field_path` 指到该对象。
- 访问器递归遍历任意 YAML／JSON 映射与列表，不硬编码 `concepts`、`entities`、`forms` 或未来 `terms` 集合。进入含稳定 `id` 的对象时，`record` 更新为 `<集合路径>:<id>`；没有新 `id` 的嵌套对象继承父记录。

角色资格如下。

角色资格是来源契约的固定枚举，不由消费者推导。

| 引用 | 必须解析 | 用途资格 | 禁止外推 |
|---|---|---|---|
| `basis` | `entity` 指向 source entity | 不要求用途角色 | 依据不能推出项目批准、派生或映射 |
| `source` | `registry` 指向 source use | 该 use 的 `structure` 为 `approved`，且有有效决定 | `mapping`、`group`、`discovery` 都不能授权派生 |
| `match` | `registry` 指向 source use | 该 use 的 `mapping` 为 `approved`，且有有效决定 | `structure`、`group`、`discovery` 都不能授权映射 |
| `external_group` | `registry` 指向 source use | 该 use 的 `structure` 为 `approved`，且有有效决定 | 只授权数组分组，不产生记录级 `source` |

`group` 只消费已经获准的映射，`discovery` 只输出发现线索；两者不得让 `validate_references()` 接受新的 `source`、`match` 或术语记录。

错误代码如下。

`Issue.code` 只取下表稳定值。新增或改名须提升来源契约版本；术语侧只在显示层前缀化为 `TERM_SOURCE_CONTRACT_<code>`，保留来源 `file`、`record` 与 `field_path`。

| code | 触发条件 |
|---|---|
| `SOURCE_SCHEMA_INVALID` | 文档不符合对应 `$id` 的 schema |
| `SOURCE_REFERENCE_KIND_INVALID` | `ReferenceUse.kind` 不是 basis、source、match、external_group |
| `SOURCE_REFERENCE_VALUE_INVALID` | `value` 不是该 kind 的对象结构 |
| `SOURCE_ENTITY_MISSING` | basis entity 或 use entity 不存在 |
| `SOURCE_USE_MISSING` | source／match registry 不存在 |
| `SOURCE_ROLE_NOT_APPROVED` | source 缺 approved structure，或 match 缺 approved mapping |
| `SOURCE_ROLE_DECISION_MISSING` | approved／retired 角色没有有效决定 |
| `SOURCE_BASIS_LOCATOR_MISSING` | basis locator 空或缺失 |
| `SOURCE_BASIS_CHECKED_MISSING` | 可变化内容缺 checked |
| `SOURCE_SOURCE_ITEM_MISSING` | source item 空或缺失 |
| `SOURCE_SOURCE_LOCATOR_MISSING` | source locator 空或缺失 |
| `SOURCE_SOURCE_BASIS_MISSING` | source basis 为空或缺失 |
| `SOURCE_MATCH_REL_INVALID` | match rel 不在五值枚举 |
| `SOURCE_MATCH_BASIS_MISSING` | match basis 为空或缺失 |
| `SOURCE_EXTERNAL_GROUP_ROLE_NOT_APPROVED` | external_group registry 不存在 approved structure 或其决定无效 |
| `SOURCE_STABLE_ID_CHANGED` | 已冻结 ID 被改名或复用 |
| `SOURCE_HISTORY_NOT_APPEND_ONLY` | history 删除、改写或重排 |
| `SOURCE_OBLIGATION_REOPENED` | resolved 义务复用原 ID |
| `SOURCE_OBLIGATION_TARGET_MISSING` | 义务 target 不能解析 |
| `SOURCE_DECISION_MISSING` | 引用的决定不存在或未 accepted |
| `SOURCE_LEGACY_FIELD` | 严格模式发现旧共享引用结构 |
| `SOURCE_INDEX_MISMATCH` | 反向索引与正式引用不双向相等 |
| `SOURCE_PROBE_FORMAL_WRITE` | 探测改变正式树或输出正式字段 |
| `SOURCE_CUTOVER_MANIFEST_INVALID` | 交付清单缺字段、哈希或写集不一致 |
| `SOURCE_DECISION_DELIVERY_MISSING` | decision-source-0005 未指向获准交付清单 |
| `SOURCE_DECISION_PATCH_CONFLICT` | 同一 `(identity, field)` 出现多个决定补丁或 Q 越过字段所有权 |

决定输入如下。

来源决定记录使用 YAML front matter，正文继续使用 ADR 的背景、决定与后果结构。每个 Q 项物化为字段补丁，不提供完整迁移行。

```python
class DecisionPatch(NamedTuple):
    identity: str
    field: str
    value: object
    qid: str
```

Q 到字段与 identity 域的所有权固定如下。`operation`、`disposition`、`blocks_cutover` 等字段可以由多个 Q 使用，但这些 Q 的 identity 域必须互斥；`validate_patch_ownership()` 同时验证字段和域。

| Q | identity 域 | 允许字段 |
|---|---|---|
| Q01 | `@control:paths` | `paths` |
| Q02 | `@control:schema` | `schema_versions`、`compatibility` |
| Q03 | 全部 entity／use 行及 `@control:ids` | `proposed_id`、`id_policy` |
| Q04 | 未登记 entity 行 | `identity_class` |
| Q05 | focus entity 行 | `identity_resolution`、`operation`、`disposition`、`new_value`、`blocks_cutover` |
| Q06 | `@control:addresses` 及现行与新 entity 行 | `url_policy`、`new_value.urls` |
| Q07 | `@control:review` 及现行 entity 行 | `review_policy`、`new_value.review` |
| Q08 | 现行 entity 行 | `new_value.watch` |
| Q09 | 现行 entity 行及 `@control:unavailability` | `new_value.unavailability_policy`、`release_block_policy` |
| Q10 | `@control:external-status` 及现行 entity 行 | `status_policy`、`new_value.status`、`new_value.replaced_by`、`operation`、`disposition`、`blocks_cutover` |
| Q11 | `@control:roles` 及非 Q12 特殊 use-role 行 | `role_policy`、`new_role`、`new_status`、`decision`、`operation`、`disposition`、`blocks_cutover` |
| Q12 | 5 个 candidate、11 个空 mapping 与空 group 行 | `new_role`、`new_status`、`decision`、`operation`、`disposition`、`blocks_cutover` |
| Q13 | `@control:source` 及非 Q14／Q15／Q16／Q17 source 行 | `source_policy`、`operation`、`disposition`、`new_value`、`blocks_cutover` |
| Q14 | 三个多来源 concept source 行 | `operation`、`disposition`、`new_value`、`blocks_cutover` |
| Q15 | 24 个主题 array source 行 | `operation`、`disposition`、`new_value`、`blocks_cutover` |
| Q16 | 两个 form array source 行 | `operation`、`disposition`、`new_value`、`blocks_cutover` |
| Q17 | 四个 RFC 1122 source 行与对应 match 行 | `operation`、`disposition`、`new_value`、`blocks_cutover` |
| Q18 | `@control:match` 及非 Q17 match 行 | `match_policy`、`operation`、`disposition`、`new_value`、`blocks_cutover` |
| Q19 | `@control:basis` 及非 Q20 basis 行 | `basis_policy`、`operation`、`disposition`、`new_value`、`blocks_cutover` |
| Q20 | 630 个 none 与 13 个正式 self basis 行 | `operation`、`disposition`、`new_value`、`blocks_cutover` |
| Q21 | `@control:origin` 及 19 个 origin 行 | `origin_policy`、`operation`、`disposition`、`new_value`、`blocks_cutover` |
| Q22 | `@control:obligation-bridge` | `source_term_bridge` |
| Q23 | 现行 entity 行 | `tier_change` |
| Q24 | `@control:term-admission` | `term_admissions` |
| Q25 | `@control:cutover` | `cutover_sequence`、`rollback_sequence`、`release_sequence` |

```python
Q_FIELD_OWNERSHIP = {
    "Q01": frozenset(("paths",)),
    "Q02": frozenset(("schema_versions", "compatibility")),
    "Q03": frozenset(("proposed_id", "id_policy")),
    "Q04": frozenset(("identity_class",)),
    "Q05": frozenset(("identity_resolution", "operation", "disposition", "new_value",
                       "blocks_cutover")),
    "Q06": frozenset(("url_policy", "new_value.urls")),
    "Q07": frozenset(("review_policy", "new_value.review")),
    "Q08": frozenset(("new_value.watch",)),
    "Q09": frozenset(("new_value.unavailability_policy", "release_block_policy")),
    "Q10": frozenset(("status_policy", "new_value.status", "new_value.replaced_by", "operation",
                       "disposition", "blocks_cutover")),
    "Q11": frozenset(("role_policy", "new_role", "new_status", "decision", "operation",
                       "disposition", "blocks_cutover")),
    "Q12": frozenset(("new_role", "new_status", "decision", "operation",
                       "disposition", "blocks_cutover")),
    "Q13": frozenset(("source_policy", "operation", "disposition", "new_value",
                       "blocks_cutover")),
    "Q14": frozenset(("operation", "disposition", "new_value", "blocks_cutover")),
    "Q15": frozenset(("operation", "disposition", "new_value", "blocks_cutover")),
    "Q16": frozenset(("operation", "disposition", "new_value", "blocks_cutover")),
    "Q17": frozenset(("operation", "disposition", "new_value", "blocks_cutover")),
    "Q18": frozenset(("match_policy", "operation", "disposition", "new_value",
                       "blocks_cutover")),
    "Q19": frozenset(("basis_policy", "operation", "disposition", "new_value",
                       "blocks_cutover")),
    "Q20": frozenset(("operation", "disposition", "new_value", "blocks_cutover")),
    "Q21": frozenset(("origin_policy", "operation", "disposition", "new_value",
                       "blocks_cutover")),
    "Q22": frozenset(("source_term_bridge",)),
    "Q23": frozenset(("tier_change",)),
    "Q24": frozenset(("term_admissions",)),
    "Q25": frozenset(("cutover_sequence", "rollback_sequence", "release_sequence")),
}
Q_CONTROL_IDENTITIES = {
    "Q01": frozenset(("@control:paths",)),
    "Q02": frozenset(("@control:schema",)),
    "Q03": frozenset(("@control:ids",)),
    "Q06": frozenset(("@control:addresses",)),
    "Q07": frozenset(("@control:review",)),
    "Q09": frozenset(("@control:unavailability",)),
    "Q10": frozenset(("@control:external-status",)),
    "Q11": frozenset(("@control:roles",)),
    "Q13": frozenset(("@control:source",)),
    "Q18": frozenset(("@control:match",)),
    "Q19": frozenset(("@control:basis",)),
    "Q21": frozenset(("@control:origin",)),
    "Q22": frozenset(("@control:obligation-bridge",)),
    "Q24": frozenset(("@control:term-admission",)),
    "Q25": frozenset(("@control:cutover",)),
}
```

```yaml
---
id: decision-source-0003
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: 2026-08-31
level: L2
scope: source-role-uses
supersedes: []
answers:
  - question: Q11
    resolution: replacement
    patches:
      - identity: source-roles.tsv:2
        field: new_status
        value: approved
      - identity: source-roles.tsv:2
        field: decision
        value: decision-source-0003
---
```

`load_decision_patches(paths: Sequence[Path]) -> Sequence[DecisionPatch]` 为每个 patch 注入所属 answer 的 qid，拒绝未 accepted 决定、空 patches、未知 Q 和无字段补丁。`materialize_decision_patches(base_rows, patches)` 按冻结 inventory 先生成一个 `identity -> base row`，再按 `(qid, identity, field)` 排序应用补丁；同一 `(identity, field)` 出现两次即返回 `SOURCE_DECISION_PATCH_CONFLICT`，即使值相同也拒绝。每个最终行保存 `decision_trace[]`，逐 patch 记录 qid、field 与规范 JSON value SHA-256。控制 identity 写入单独 `controls` 对象，不计入 3,187 个库存行。

切换交付如下。

完整 ignored candidate root 必须先生成并通过候选校验。随后生成 payload，再生成 handoff，最后才允许人创建绑定决定。交付只有两层，字段所有权固定如下。

- `vocab/generated/source-cutover-payload.json` 的顶层键恰为 `schema`、`schema_version`、`entries`。entries 只列原子切换尚待应用的正式路径及 candidate `after_sha256`；payload 自身、handoff、先行决定、六份账本和义务不进入 entries。
- `vocab/generated/source-cutover-handoff.json` 的顶层键恰为 `schema`、`schema_version`、`payload`、`source_contract`、`schemas`、`topics_sha256`、`migration_ledgers`、`markdown_manifest`、`outputs`、`tracked_write_set`。`payload` 恰含 `path` 与 `sha256`；handoff 不含自身路径或自身 SHA-256。
- `decision-source-0005` 的绑定键恰为 `delivery_handoff`、`handoff_sha256`、`delivery_payload`、`payload_sha256`。handoff 路径固定为 `vocab/generated/source-cutover-handoff.json`，payload 路径固定为 `vocab/generated/source-cutover-payload.json`；不得使用 `delivery_manifest` 或 `payload_manifest_sha256` 作为来源决定键。

```python
import hashlib
import json
from pathlib import Path
from typing import List

import yaml

from scripts.source_model import ERROR_CODES, ROLE_QUALIFICATIONS, Issue

PAYLOAD_PATH = "vocab/generated/source-cutover-payload.json"
HANDOFF_PATH = "vocab/generated/source-cutover-handoff.json"
HANDOFF_FIELDS = (
    "schema", "schema_version", "payload", "source_contract", "schemas",
    "topics_sha256", "migration_ledgers", "markdown_manifest", "outputs",
    "tracked_write_set",
)
DECISION_DELIVERY_FIELDS = (
    "delivery_handoff", "handoff_sha256", "delivery_payload", "payload_sha256",
)

def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def serialize_payload_manifest(manifest) -> bytes:
    return (json.dumps(manifest, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")

def build_payload_manifest(candidate_root: Path, apply_paths):
    entries = []
    for relative in sorted(set(apply_paths)):
        if relative in (PAYLOAD_PATH, HANDOFF_PATH):
            raise ValueError("SOURCE_CUTOVER_MANIFEST_INVALID self entry")
        target = candidate_root / relative
        entries.append({"path": relative,
                        "after_sha256": sha256_path(target) if target.is_file() else None})
    if not entries or "vocab/topics.yaml" not in {row["path"] for row in entries}:
        raise ValueError("SOURCE_CUTOVER_MANIFEST_INVALID missing topics")
    manifest = {"schema": "urn:kb-design:data:source-cutover-payload",
                "schema_version": 1, "entries": entries}
    payload = serialize_payload_manifest(manifest)
    topics_sha256 = next(row["after_sha256"] for row in entries
                         if row["path"] == "vocab/topics.yaml")
    return manifest, hashlib.sha256(payload).hexdigest(), topics_sha256

def serialize_source_handoff(handoff) -> bytes:
    return (json.dumps(handoff, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")

def build_source_handoff(candidate_root: Path, payload_bytes: bytes, tracked_write_set,
                         markdown_paths, schema_paths, ledger_paths):
    payload = json.loads(payload_bytes)
    validate_payload_manifest(payload)
    topics_path = candidate_root / "vocab/topics.yaml"
    topics = yaml.safe_load(topics_path.read_text(encoding="utf-8"))
    schemas = []
    for path in sorted(schema_paths):
        document = json.loads((candidate_root / path).read_text(encoding="utf-8"))
        schemas.append({"path": path, "$id": document["$id"],
                        "schema_version": int(document["$id"].rsplit(":", 1)[1]),
                        "sha256": sha256_path(candidate_root / path)})
    handoff = {
        "schema": "urn:kb-design:data:source-cutover-handoff",
        "schema_version": 1,
        "payload": {"path": PAYLOAD_PATH,
                    "sha256": hashlib.sha256(payload_bytes).hexdigest()},
        "source_contract": {
            "module": "scripts/source_model.py",
            "sha256": sha256_path(candidate_root / "scripts/source_model.py"),
            "reference_kinds": ["basis", "source", "match", "external_group"],
            "role_qualifications": dict(ROLE_QUALIFICATIONS),
            "error_codes": list(ERROR_CODES),
        },
        "schemas": schemas,
        "topics_sha256": sha256_path(topics_path),
        "migration_ledgers": [{"path": path, "sha256": sha256_path(candidate_root / path)}
                              for path in sorted(ledger_paths)],
        "markdown_manifest": [{"path": path, "sha256": sha256_path(candidate_root / path)}
                              for path in sorted(markdown_paths)],
        "outputs": [
            {"path": "vocab/topics.yaml", "kind": "topics",
             "sha256": sha256_path(topics_path),
             "concepts": len(topics["concepts"]), "arrays": len(topics["arrays"])},
            {"path": "vocab/generated/source-reference-index.json", "kind": "source_index",
             "sha256": sha256_path(candidate_root /
                                    "vocab/generated/source-reference-index.json")},
        ],
        "tracked_write_set": sorted(tracked_write_set),
    }
    validate_source_handoff(handoff)
    return handoff, hashlib.sha256(serialize_source_handoff(handoff)).hexdigest()

```

`verify_source_handoff(repo_root: Path, handoff_path: Path, payload_path: Path, candidate_root: Path) -> List[Issue]` 是切换交付的唯一公开预验接口。四个路径参数都必须显式传入：`repo_root` 提供仓库身份和正式路径边界，`handoff_path` 与 `payload_path` 指向本次实际验证的字节，`candidate_root` 提供 handoff 中 schema、主题、账本、Markdown 和输出的候选内容。函数只从传入的 `payload_path` 读取 payload；即使 handoff 的逻辑 `payload.path` 固定为未来正式路径，也不得在函数内部改读 `repo_root / handoff["payload"]["path"]`。每个失败返回 `Issue`，`code` 取既有稳定错误码，`file` 取实际 handoff 或 payload 路径，`record` 固定为 `source-cutover-handoff` 或 `source-cutover-payload`，`field_path` 指向失败字段；函数不得返回字符串。

生成顺序固定为：完整 candidate root → payload bytes／SHA-256 → handoff bytes／SHA-256 → 调用 `verify_source_handoff(repo_root, ignored_handoff_path, ignored_payload_path, candidate_root)` → 人核对 → `decision-source-0005` → 先行审计提交 → 原子应用。`write_payload_manifest()` 和 `write_source_handoff()` 都写独立 ignored delivery 目录。payload entries 按 path 排序且唯一；删除操作以 `after_sha256: null` 表达；其他 entry 的 hash 必须与 candidate 文件逐字相等。handoff 的七份 schema 恰好覆盖 `SCHEMA_IDS`，六份账本恰好覆盖冻结 ledger 集，topics output 必须为 700／24，`tracked_write_set` 必须逐字等于 payload entry paths。

`decision-source-0005` 只有在人核对 candidate、payload 和 handoff 后才可 accepted。先行决定提交把 decision、handoff、payload 作为审计文件保留；原子应用先验证 decision 的四个绑定键，再以正式 handoff 路径、正式 payload 路径和 candidate root 调用同一个 `verify_source_handoff()`，最后只应用 payload entries。安装完成后再以 `candidate_root=repo_root` 调用同一接口验证正式字节。术语 T01 使用同一顺序与同一键名：decision → handoff → payload。

公开生产接口固定为 24 个：`validate_references`、`collect_reference_uses`、`validate_repository`、`load_decision_patches`、`compute_next_due`、`is_review_overdue`、`build_reference_index`、`load_probe_endpoints`、`probe_repository`、`schedule_due`、`select_evidence`、`evaluate_unavailability`、`append_false_positive`、`build_migration_plan`、`apply_migration`、`open_obligation`、`resolve_obligation`、`build_payload_manifest`、`build_source_handoff`、`verify_source_handoff`、`load_bound_source_delivery`、`apply_bound_payload`、`load_rollback_plan`、`build_compensation_candidate`。其他函数均为任务内部帮助函数，不得由术语侧导入。

## 决定锁

下列 25 项都是待批准提案。执行者把人的逐项答复写入 `design/decisions/source-governance-schema.md`、`source-identity-boundaries.md` 和 `source-role-uses.md`；人的答复与推荐不一致时，只消费人的精确替代值。没有精确答复时执行对应的“不批准时行为”。

1. 正式路径

   精确问题：来源实体、用途登记、决定记录、来源复核义务、探测材料和反向引用索引分别写入哪个受跟踪正式路径；哪些是编辑源，哪些是确定性生成物，哪些是忽略的运行材料？

   推荐选项：来源实体继续以 `vocab/entities.yaml` 为唯一编辑源；用途登记继续以 `vocab/sources.yaml` 为唯一编辑源；决定记录写入 `design/decisions/source-*.md`；来源义务写入 `vocab/source-obligations.yaml`；反向索引生成到 `vocab/generated/source-reference-index.json`；探测材料只写 `.superpowers/sdd/2026-08-31-source-schema-migration/probes/`。前四类与索引受跟踪，索引只读，探测材料 ignored。

   理由：保留 31 个现行实体和用途的唯一身份，避免拆出重复来源记录；同时把义务、索引和运行观察按职责物理隔离。

   若错误的代价：`entities.yaml` 的混合实体模式可能增加条件校验复杂度；拆分过晚会提高未来独立发布来源目录的成本。

   不批准时行为：停止模式契约任务及全部后续任务；受跟踪与 ignored 写集均为零。

2. 模式版本

   精确问题：每类正式文件采用什么 schema 标识和版本值；兼容规则、升级顺序和旧结构禁用时点是什么？

   推荐选项：采用“接口锁”表中的七个 URN；`entities` 与 `source-uses` 使用 `schema_version` 2，其余使用 1。先提交 schema 与双读校验器，再完成获准候选树；原子切换提交同时把默认校验改为严格模式并禁用旧紧缩 `basis`、旧 `source`、旧 `match.source`、旧 `origin` 和旧角色数组。现行 `version.id: "2026.08"` 在独立发版决定前不变。

   理由：模式升级与数据发版分离，兼容读取只服务迁移预演，不让旧结构在切换后继续成为第二套正式接口。

   若错误的代价：一次性严格切换会扩大最后一个提交的写集；长期双读则会让生成器继续恢复旧结构。

   不批准时行为：停止模式契约任务及全部后续任务；不创建 schema、测试或 ignored 草稿。

3. 标识规则

   精确问题：来源实体、用途登记、决定和复核义务的 `id` 各采用什么格式、分配者和冲突处理；31 个现行一对一 `id` 是否全部冻结；107 个身份何时取得新 `id`？

   推荐选项：31 个现行实体和用途 `id` 原样冻结；新实体使用小写 ASCII slug `^[a-z0-9]+(?:-[a-z0-9]+)*$`，由迁移账本提出并由人随身份决定批准；用途 `id` 与一对一实体 `id` 相同；决定使用 `decision-source-0001` 起的四位顺序号；义务使用 `source-review-YYYYMMDD-NNN`。分配器遇到冲突即失败，不加随机后缀、不复用旧号。107 个身份只有在其账本行获准为独立实体时才取得 `id`。

   理由：冻结现有 1,625 次引用，新增标识仍符合仓库现行格式；顺序决定号和带日期义务号便于审计而不从名称推断状态。

   若错误的代价：slug 中含版本时，身份判据错误会造成难以改名的永久标识；顺序号需要串行分配。

   不批准时行为：停止身份迁移任务；不生成任何输出。

4. 身份判据

   精确问题：新版本、修订项目、标准分部、汇总页、样章、镜像、存档快照和状态页分别在什么判据下成为新实体、同一实体的地址／定位，或仅为依据材料？

   推荐选项：具有发布方独立标识、可独立引用正文和独立生命周期的版本或分部是新实体；仅有修订项目元数据而无已发布正文时只作探测材料；汇总页和状态页作 `status` 地址或 `watch`；官方样章作 `locator` 材料；镜像与存档快照作 `mirror`／`archive` 地址，不能替代规范身份；勘误与修改单在未形成合并版前作现有实体的依据材料。

   理由：身份取决于可引用作品和生命周期，不取决于 URL、题名相似或页面所在域名。

   若错误的代价：把分部拆得过细会增加用途和复核数量；合并过度会使版本、替代和定位无法精确表达。

   不批准时行为：停止身份迁移任务；不生成任何输出。

5. 重点身份

   精确问题：`rfc-http`／`rfc-9110`、聚合 `iso-25964`／两个分部、DITA 三个 Part、LOM 2002／2020、Z39.19 地址链和 BCP 47 信息页／两份 RFC 的具体身份结论是什么？

   推荐选项：保留 `rfc-9110`，废止 `rfc-http` 集合别名；ISO 25964-1 与 ISO 25964-2 保持两个实体，聚合名不建实体；DITA 1.3 三个 Part 作为同一 `dita` 实体的三个正文地址，因为共享版本与发布生命周期；`lom` 冻结为 2002 实体，IEEE 1484.12.1-2020 新建 `lom-2020`，发布方证据确认后前者才可指向后者；Z39.19 出版页、DOI、正文和 PDF 属同一 `z39-19` 地址链，修订页只作状态观察；BCP 47 信息页作聚合入口，RFC 5646 与 RFC 4647 分别建实体。

   理由：这些结论逐项应用 Q04 判据，同时保留现行稳定 `id` 的既有语义。

   若错误的代价：DITA Part 若实际拥有独立生命周期会被合并过度；LOM 关系若不是正式替代会错误形成 `replaced_by`。

   不批准时行为：停止相关实体、用途、`source`、`match` 任务；不生成默认结论。

6. 地址结构

   精确问题：单一 `url` 是否扩展为带角色的多地址；若扩展，规范地址、正文、DOI、PDF、状态页、镜像和存档各使用什么枚举与优先顺序？

   推荐选项：扩展为 `urls[]`，每项含 `role`、`url`、`primary`。角色只取 `canonical`、`landing`、`doi`、`full_text`、`status`、`mirror`、`archive`；身份与引用优先顺序为 canonical、doi、landing、full_text、status、archive、mirror；探测优先顺序为 status、canonical、landing、full_text，mirror 与 archive 只作失败后的证据入口。每实体恰有一个 `primary: true`。

   理由：Z39.19、DITA 和 LOM 已证明一个标量不能同时表达规范入口、正文和状态观察。

   若错误的代价：角色过细会增加维护；优先顺序错误可能让镜像取代发布方记录。

   不批准时行为：停止实体模式与探测任务；不修改地址或生成探测夹具。

7. 复核周期

   精确问题：现行 `tier` 的 24、12、6 个月和 archival 规则如何迁入 `review.next_due`；每类来源的复核周期、起算日期、宽限和兼容字段删除条件是什么？

   推荐选项：de-jure 为 24 个月、de-facto 为 12 个月、vendor 为 6 个月；archival 的内容 `next_due` 为 `null`，地址探测每 12 个月运行。起算日只取经人确认的 `review.checked`，不能直接复制来源级或用途级 `checked`；到期宽限为 30 日。31 个实体全部取得确认过的 `review`、严格校验零旧读取者且原子切换获准后，在切换提交删除 `tier` 兼容字段；本次不改变任何实体档级。

   理由：保留现行周期数值但停止让 `tier` 推出用途与外部状态；人工复核日期和探测日程保持分离。

   若错误的代价：现行周期可能未经首轮维护校准；删除兼容字段会使未迁移读取者失败。

   不批准时行为：停止实体模式、周期与切换任务；不生成 `review` 值。

8. 探测策略

   精确问题：只读探测按什么频率运行；动态页面的内容变化采用整页摘要、目标片段摘要还是发布方版本元数据；误报如何记录而不回写正式事实？

   推荐选项：所有 `watch` 每月检查 availability 与 redirect；de-jure 每月、de-facto 每 3 个月、vendor 每 6 个月、archival 每 12 个月检查 version、revision、replacement 与 withdrawal。内容变化优先取发布方版本元数据，其次取获准 `locator` 的规范化片段摘要，整页摘要只作低置信信号。误报追加到同一 ignored 观察流，记录 `classification: false_positive`、复核日期、理由和前一观察标识，不回写正式字段。

   理由：高噪动态页面不应依靠整页摘要决定内容变化，且探测频率不等于人工复核周期。

   若错误的代价：月度探测可能产生请求和误报负担；片段定位失效会降低变化检测覆盖。

   不批准时行为：停止探测任务；不创建测试、观察或调度材料。

9. 不可访问

   精确问题：持续不可访问达到多长时间、多少次独立观察或哪些条件后才阻断发布；镜像、存档快照和出版者状态页的证据优先顺序是什么？

   推荐选项：首次失败只创建义务；同一规范入口在至少 14 日内出现 3 次不同日期的独立失败，且发布方状态页、DOI／landing、获准 archive、mirror 依次均不能让人工复核重现被引内容时，阻断受影响记录的发布。证据优先顺序为出版者状态页、DOI／landing、获准存档、镜像；任何一次失败都不得产生 `withdrawn`。

   理由：时间跨度、重复观察和人工重现共同降低短期网络故障造成的误阻断。

   若错误的代价：14 日窗口可能让真实撤回延迟阻断，也可能对长期地域性访问故障过严。

   不批准时行为：停止探测与义务任务；不创建正式或 ignored 观察。

10. 外部状态

   精确问题：31 个现行来源的外部 `status` 分别是什么，依据定位在哪里；哪些 `replaced_by` 已被发布方明确支持？现行命名实体 `active/candidate` 不作为答案。

   推荐选项：本计划不批准 31 个外部状态；31／31 在迁移账本中使用 `classification: unresolved_external_status`，这不是正式 schema 值，且 `replaced_by` 全部保持未批准。每个实体只有在 `source-identity-boundaries.md` 增加发布方定位、核对日期和逐实体结论后才能离开阻断。

   理由：冻结库存明确说明现行工作流状态不能映射到发布方状态，现有材料不足以安全给出 31 个逐实体事实。

   若错误的代价：推荐会阻止正式实体切换并延长双读阶段。

   不批准时行为：停止现行实体任务；不生成任何输出。

11. 角色状态

   精确问题：47 个角色各自进入 `proposed`、`approved` 还是 `retired`；每个 `approved` 或 `retired` 角色引用哪个已存在或新获准决定 `id`？

   推荐选项：`decision-source-0003` 一次批准“现行角色无损登记为同名 `proposed`、`decision: null`”的类别规则，迁移器按冻结身份确定性展开 47 行；不因现行同名 role 或消费者数量批准。只有转为 `approved`、`retired` 或改名的角色须在 `source-role-uses.md` 逐项列出并引用决定。

   理由：`proposed` 不扩大用途资格，保持现状可由一次类别决定安全展开；批准、退役和改名仍改变效力，必须逐项决定。

   若错误的代价：未获批准的角色仍不能供 `source.registry` 或 `match.registry` 使用；正式派生与映射数量可能减少。

   不批准时行为：停止用途角色任务；不生成任何输出。

12. 候选角色

   精确问题：五个旧 `candidate` 角色是否在草案生效后的哪一个获准批次转为 `discovery`；11 个无实际 `match` 的 `mapping` 与空的 `owasp-top10` 组资格是否保留？

   推荐选项：五个旧 `candidate` 在“用途角色”批次按类别规则转为 `proposed discovery`，不取得批准；11 个无消费者 `mapping` 保持 `proposed`；空的 `owasp-top10` `group` 保持 `proposed`。只有后续批准、退役或改名才新增逐角色决定。

   理由：保存发现与未来用途提案，不把历史声明、空集合或未使用角色当作资格。

   若错误的代价：保留未用提案会增加维护清单；直接退役可能丢失尚未复核的预期用途。

   不批准时行为：停止用途角色任务；不生成三类角色的迁移材料。

13. 派生材料

   精确问题：692 个实际派生按什么最小复核材料证明条目身份与派生；同一来源中 locator 模板可否复用，若可复用，怎样仍保持逐项可重复定位？

   推荐选项：每行至少具有 approved `structure` 角色、唯一外部 `item`、可重复 `locator`、证明条目身份与实际复制关系的 `source.basis`、核对日期和处置决定。允许同一 registry 使用带 `{item}` 的固定 locator 模板，但迁移账本必须保存每行渲染后的完整 locator，并由测试证明 692 行逐项回读到唯一外部位置。

   理由：模板减少重复输入，但渲染结果仍逐值相邻、可核对、可进入反向索引。

   若错误的代价：模板规则错误会系统性错位整个 registry；逐行复制则增加维护成本。

   不批准时行为：停止实际派生任务；不生成任何输出。

14. 多来源概念

   精确问题：`cryptography`、`software-design` 和 `software-construction` 的第二来源是否表示第二个实际派生；若是，单个 `source` 接口如何表达；若否，哪个现行关系被保留为数组成员或 `match` 而不伪装派生？

   推荐选项：三条记录的唯一实际派生保持 `cs2023`；`cryptography` 的 ASVS、`software-design` 与 `software-construction` 的 SWEBOK 只保留为获准数组成员和独立 `match`，不扩展单值 `source`。

   理由：现行生成器只证明 CS2023 首次创建记录，后续来源只追加数组和映射；库存没有第二次实际复制的证据。

   若错误的代价：若真实形成过程确有联合派生，单值记录会低报 provenance。

   不批准时行为：停止三条记录所在派生批次；不生成任何输出或默认结论。

15. 主题数组

   精确问题：24 个主题来源名称数组使用什么获准结构保存来源显示与成员分组；它们是否保留，且为什么不能复用实际派生 `source`？

   推荐选项：24 个数组全部保留，使用数组级 `external_group` 对象，字段固定为 `registry`、`item`、`locator`、`basis`；成员仍通过概念的 `arrays` 引用。`external_group` 证明分组身份，不证明每个成员记录从该来源实际派生，因此不得复用记录级 `source`。

   理由：保留现有导航和分组身份，同时阻止数组显示来源外推为 24 组成员的派生结论。

   若错误的代价：新增 `external_group` 扩大来源草案接口，需要同步模式与文档；分组若确为外部复制会与 `source` 产生相邻语义。

   不批准时行为：停止主题数组批次与原子切换；不生成任何输出。

16. 载体数组

   精确问题：`forms-presentation` 和 `forms-activity` 是否保留；若保留，其本地分析身份、成员边界与 LOM/Wikidata 混合来源使用什么已批准结构表达？

   推荐选项：两数组及成员全部保留，成员关系逐字不变；原数组 `source: lom` 机械隔离为 `local_analysis: {legacy_source_label: lom, state: isolated, decision: decision-source-0005}`。该对象只保存旧显示字符串和隔离状态，不进入 `ReferenceUse`，不取得 `basis`、`source`、`match`、用途或本地分析语义，账本 disposition 为 `isolated_local_analysis` 且 `blocks_cutover: false`。LOM 与 Wikidata 只在各成员已有逐值决定时形成 `basis` 或 `match`。划分特征草案继续旁路，不成为共享来源接口切换前置。

   理由：隔离旧字符串可以消除 `source` 语义冲突并保留全部成员，不使旁路草案生效，也不阻断术语计划所需的共享引用契约。

   若错误的代价：若消费者错误读取 `legacy_source_label` 作为 provenance，会重新引入语义混用；测试必须证明通用访问器忽略该对象。

   不批准时行为：停止实际派生任务与原子切换；不生成任何输出。

17. RFC 层次

   精确问题：RFC 1122 四层分别使用哪个唯一外部 `item` 与可重复 `locator`；若标准没有四个可独立引用的 item，哪些记录不形成 `source` 或 `match`？

   推荐选项：四个 `item` 分别为 `Application Layer`、`Transport Layer`、`Internet Layer`、`Link Layer`；四项 locator 均为 `RFC 1122 § 1.1.3, Figure 1 and the corresponding layer description`，并在账本保存精确文本范围。只有外部文本能分别定位这四个标题和说明时形成 `source`；`match` 还需逐条比较本地范围，不能因同章成立。任一标题无法独立定位时，该记录不形成 `source` 或 `match`。

   理由：`item` 标识外部对象，`locator` 可以共享章节但必须指出各自文本；现行共同 `1.1.3` 不能同时承担两种职责。

   若错误的代价：标题可能不是稳定外部标识，后续版本会改变文字定位。

   不批准时行为：停止 RFC 1122 所在派生与映射批次；不生成四条迁移记录。

18. 映射材料

   精确问题：756 个映射按什么材料证明双方概念范围与关系；LOM 2020 正文、GB/T 两个修改单与 435 个条目、24 个 Wikidata Q 条目未核完时，对应批次是保持待人、取消迁移还是另取获准材料？

   推荐选项：每条映射须有本地定义或范围定位、外部定义或范围定位、逐条比较结论、五值关系和决定引用。LOM 2020、GB/T 435 条与两个修改单、24 个 Wikidata Q 条目在材料未核完时一律保持 `blocked_unread_material` 迁移分类，不取消现行语义、不采用非官方替代材料，也不进入原子切换。

   理由：关系依据必须与映射相邻，未读材料无法支持继承 748 个 `exactMatch`。

   若错误的代价：阻断量大，可能使严格切换长期不能完成。

   不批准时行为：停止概念映射任务；不生成任何输出。

19. 核对日期

   精确问题：`basis.checked` 对哪些内容必填；同一来源、同一 locator 支持多个值时怎样逐值关联；151 个紧缩字符串中的 23 个无位置值无法补证时如何处置？

   推荐选项：HTTP 页面、动态数据库、状态页和任何未锁定内容哈希的材料必填 `checked`；只有固定版本、固定文件哈希且定位在该文件内的材料可以省略。一个 locator 支持多个值时，在每个具体值旁重复完整 `basis` 项，不使用 YAML anchor 或全局默认。23 个无位置值无法补证时记 `not_migrated_missing_locator`，保留旧值的冻结审计行，禁止作为严格模式现行依据。

   理由：逐值重复保证模式能唯一定位，内容可变性而非来源档级决定是否需要日期。

   若错误的代价：重复依据增加文件体积；严格阻断会使 23 个字段不能随其记录切换。

   不批准时行为：停止逐值依据任务；不生成任何输出。

20. 无依据值

   精确问题：630 个 `none` 和 13 个正式 `self` 在旧数据对账中分别以什么非 `basis` 状态保留历史；删除旧叶值前用什么审计材料证明没有伪造语言形式或外部依据？

   推荐选项：迁移账本使用 `no_external_basis` 对账 630 个 `none`，使用 `project_assertion` 对账 13 个 `self`；两者都不是正式 `basis` 值。删除旧叶值前，`vocab/migrations/source-v1/basis.yaml` 必须逐行保存文件、稳定记录、字段路径、旧值、冻结文件哈希、处置、决定或义务 `id`，并证明 643 行前后身份一一对应、没有新增形式或外部实体。

   理由：把缺失与项目断言留在迁移审计层，避免伪造成外部证据。

   若错误的代价：正式记录仍需其他已批准状态表达“当前值存在但无外部依据”，否则对应记录会保持阻断。

   不批准时行为：停止逐值依据任务；不生成任何输出。

21. 旧字段分流

   精确问题：旧 `origin` 的发现记录采用哪个正式位置和结构；内容单元与 publication/standard 两种目标怎样分开；去掉旧保留理由后，内容单元保留决定由什么独立规则支撑？

   推荐选项：本迁移不创建正式发现记录；发现观察只写 `.superpowers/sdd/2026-08-31-source-schema-migration/discovery/observations.tsv`，列为 `observed_text`、`file`、`record`、`field_path`、`entity`、`locator`、`observed_at`、`state`、`decision`。内容单元只记录文件与稳定内容身份，publication/standard 只引用来源实体；内容单元保留继续由 `design/content-model.md` 的现行不删规则和独立项目决定支撑，不再由 `origin` 支撑。

   理由：正式数据中没有 `origin`，迁移不应为规则示例创造填空对象；发现线索也不能取得术语或来源资格。

   若错误的代价：发现线索在正式治理中暂时没有长期编辑源，只能作为迁移与复核材料保存。

   不批准时行为：停止文档分流任务；不生成任何输出。

22. 义务衔接

   精确问题：来源变化影响术语时，来源义务 `id` 怎样进入术语义务；两类义务的正式路径、索引和关闭责任怎样保持分离？

   推荐选项：术语义务只在 `trigger` 保存 `{kind: source_obligation, id: source-review-YYYYMMDD-NNN}`；不得复制来源义务的 trigger、targets、state 或结论。来源义务位于 `vocab/source-obligations.yaml` 并进入来源索引；术语义务未来位于 `vocab/term-obligations.yaml` 并进入术语索引。来源复核只关闭来源义务，术语复核只关闭术语义务，即使由同一人执行也须分成两次状态转换。

   理由：稳定 `id` 提供衔接，物理文件、索引和状态机保持职责隔离。

   若错误的代价：跨文件查询增加一次跳转；关闭责任分离会产生更多开放义务。

   不批准时行为：停止反向索引与义务任务；不生成来源或术语目标清单。

23. 来源改档

   精确问题：本次迁移涉及哪些具体来源 `tier` 变化？如果答案不是“无”，须逐来源给出 L3 改档决定及下游处置；库存不提供默认改档。

   推荐选项：无。31 个现行 `tier` 在兼容阶段保持原值，原子切换删除兼容字段也不把任何实体映射到新档位；未来改档逐来源另走 L3 决定。

   理由：来源实体外部状态、用途和复核周期拆分不需要改变现有档级事实。

   若错误的代价：现行档级本身可能有错误，但本计划不会顺手纠正。

   不批准时行为：停止涉及改档的实体批次及下游切换；不生成替代档级。

24. 术语准入

   精确问题：来源整理中发现的字符串是否有任何一个拟作为可复用项目概念名称？若有，须逐项给出形式、语言、概念身份、准入依据和人的准入决定；没有这些材料时只保留来源标签、题名或转录，不创建术语记录。

   推荐选项：无。本次来源迁移不把任何发现字符串作为可复用项目概念名称；全部只保留为来源标签、题名、外部 item、locator 或转录。

   理由：来源整理没有提供独立的形式、概念身份和人的术语准入决定。

   若错误的代价：确有价值的项目术语需要在术语计划中重新登记和复核。

   不批准时行为：停止涉及该字符串的来源批次；不创建来源侧或术语侧记录。

25. 生效切换

   精确问题：草案何时生效、每个实际迁移批次何时获准、切换失败时由哪个决定授权回退；生效、迁移、来源改档、术语准入和发版必须分别记录，不能合并成一次默认批准。

   推荐选项：模式、离线校验、索引、探测隔离和完整 ignored candidate application root 全部 GREEN，且 25 项决定 patches 已经物化、六份账本零阻断后，依次生成不含自身 entry 的 payload 与不含自身 hash 的 handoff；`decision-source-0005` 精确绑定 handoff path／SHA-256 与 payload path／SHA-256。随后先提交不可删除的审计提交：`decision-source-0004` 使草案生效，`decision-source-0005` 接受双层交付，`decision-source-0006` 以 Q25 patches 预授权补偿，同时提交六份账本、已分配 ID、初始历史和来源义务。下一提交先验证 decision → handoff → payload，再只应用 payload entries。失败时新建 `decision-source-0008` 与补偿提交，恢复旧消费者和旧数据表示，但保留 `decision-source-0004` 至 `0006`、所有 ID、history、义务、账本、handoff 与 payload；禁止整提交反转或反向 patch 删除这些证据。改档与术语准入保持“无”；补偿后或切换通过后都由独立 `decision-source-0007` 决定是否发版。

   理由：生效、数据变更、失败处置和公开发布的风险与证据不同，必须分别审计。

   若错误的代价：补偿提交不能做到字节级恢复，必须逐对象说明恢复后的活动表示、保留审计对象和消费者模式。

   不批准时行为：草案保持未生效并停止全部实施任务；受跟踪与 ignored 写集均为零。

## 执行门禁

正式任务按各节列出的 Q 项逐批解锁。任一必需 Q 没有 accepted 决定、patches 不完整或出现 identity／field 冲突时，立即停止；不得创建受跟踪文件、ignored 夹具、候选树、预演报告或提交。

```bash
git branch --show-current
git rev-parse HEAD
shasum -a 256 .superpowers/sdd/2026-08-31-governance-implementation-prep/source-plan-input.md
git diff --name-only -- requirements-dev.txt schemas scripts tests vocab design AGENTS.md README.md
```

预期分支为 `feat/terminology-governance`，计划输入哈希为 `56087db27519ea4d700e9010500c5d3cee69dd742fd538d4296e5c26cd02d69a`。`HEAD` 与冻结提交不同时，重新计算全部 18 个依赖哈希并逐项解释变化；不能只更新哈希。正式写集中的既有未提交修改必须为零，否则停止，不覆盖用户修改。

模式契约任务开始前，用下列命令验证 `decision-source-0001` 已接受 Q01、Q02、Q03、Q06、Q07、Q21、Q22。命令只读决定文件；失败退出 1。

```bash
python3 - <<'PY'
from pathlib import Path
import yaml

path = Path("design/decisions/source-governance-schema.md")
if not path.exists():
    raise SystemExit("SOURCE_DECISION_MISSING decision-source-0001")
text = path.read_text(encoding="utf-8")
if not text.startswith("---\n") or "\n---\n" not in text[4:]:
    raise SystemExit("SOURCE_SCHEMA_INVALID decision front matter")
front = yaml.safe_load(text.split("---\n", 2)[1])
required = {"Q01", "Q02", "Q03", "Q06", "Q07", "Q21", "Q22"}
answers = front.get("answers", [])
seen = {row.get("question") for row in answers if row.get("patches")}
if front.get("id") != "decision-source-0001" or front.get("status") != "accepted":
    raise SystemExit("SOURCE_DECISION_MISSING decision-source-0001")
if seen != required:
    raise SystemExit(f"SOURCE_DECISION_DELIVERY_MISSING expected={sorted(required)} actual={sorted(seen)}")
print("SOURCE_DECISIONS_OK decision=decision-source-0001 count=7")
PY
```

后续任务统一运行 `python3 scripts/source_model.py decisions --require Q04,Q05` 形式的门禁；`--require` 参数按任务 Interfaces 列出的 Q 集合传入。命令调用 `load_decision_patches()`，输出实际 `resolution`、patch 数和 patch 集 SHA-256。无损同类迁移可以由 accepted 类别规则绑定冻结输入哈希和确定性物化器，每个生成行记录规则与输入身份；凡新增或改变外部状态、实体边界、角色批准、正式 `basis`、实际派生、概念关系或删除结论，仍须 identity／field 级 accepted patch。测试断言每个实际 patch 都进入唯一最终行的 `decision_trace`，但不为保持现状的行制造重复 patch。

所有任务使用同一个零退出链接基线命令 `python3 scripts/check_link_baseline.py`。该脚本必须验证 `scripts/check-links.py` 退出 1 且 stdout 逐字等于以下三行，然后输出 `KNOWN_LINK_BASELINE_OK count=2` 并退出 0：

```text
.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/agentic-plan.md:11: 文件不存在 ../specs/2026-08-30-basic-unit-consumer-classification-design.md
.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/human-decision-package.md:340: 锚点不存在 ../../../../design/sources-registry.md#L68
2 处问题
```

出现 0、1、3 个问题、路径／行号／错误种类变化或 `check-links.py` 退出码变化时，基线脚本退出 1。这样四个阶段回归门禁都能继续执行后续 `git diff --check` 与其他验证。

### 模式契约

**Files:**

- Create: `requirements-dev.txt`
- Create: `scripts/source_model.py`
- Create: `scripts/check_link_baseline.py`
- Create: `schemas/source-entities.schema.json`
- Create: `schemas/source-uses.schema.json`
- Create: `schemas/source-obligations.schema.json`
- Create: `schemas/source-reference-index.schema.json`
- Create: `schemas/source-probe.schema.json`
- Create: `schemas/source-migration.schema.json`
- Create: `schemas/decision.schema.json`
- Create: `tests/test_source_schema.py`
- Create: `tests/test_source_contract.py`
- Create: `tests/source_governance_helpers.py`
- Create: `tests/fixtures/source-governance/valid/entities.yaml`
- Create: `tests/fixtures/source-governance/valid/sources.yaml`
- Create: `tests/fixtures/source-governance/valid/obligations.yaml`
- Create: `tests/fixtures/source-governance/valid/decision.yaml`
- Create: `tests/fixtures/source-governance/valid/source-cutover-handoff.yaml`
- Create: `tests/fixtures/source-governance/invalid/basis-missing-locator.yaml`
- Create: `tests/fixtures/source-governance/invalid/source-missing-basis.yaml`
- Create: `tests/fixtures/source-governance/invalid/match-invalid-rel.yaml`
- Create: `tests/fixtures/source-governance/invalid/entity-scalar-url.yaml`
- Create: `tests/fixtures/source-governance/invalid/role-missing-decision.yaml`
- Create: `tests/fixtures/source-governance/invalid/obligation-reopened.yaml`
- Create: `tests/fixtures/source-governance/invalid/migration-unknown-disposition.yaml`
- Create: `tests/fixtures/source-governance/invalid/decision-missing-id.yaml`
- Create: `tests/fixtures/source-governance/invalid/cutover-manifest-missing-topics-hash.yaml`
- Create: `tests/fixtures/source-governance/invalid/cutover-manifest-self-entry.yaml`
- Create: `tests/fixtures/source-governance/invalid/source-handoff-missing-schemas.yaml`

**Interfaces:**

- Consumes: 决定锁 Q01、Q02、Q03、Q06、Q07、Q21、Q22 的获准值，以及来源治理草案的共享结构和枚举。
- Produces: `scripts/source_model.py` 的 `Issue`、`ReferenceUse`、`validate_references()`、稳定错误码和角色资格；七个 JSON Schema Draft 2020-12 合约；零退出旧链接基线。

**人工门禁:** `decision-source-0001` 必须逐字列出七个 `$id`、数据版本、正式路径、共享类型、错误码、角色资格、地址枚举、周期字段、兼容规则和禁用时点。门禁命令不通过时停止，本任务所有写集为零。

- [ ] **写入失败测试**

  `tests/test_source_contract.py` 固定消费者可导入接口、错误码、角色资格和 schema `$id`。

```python
import json
import pathlib
import unittest
from pathlib import Path
from typing import List, Sequence, get_args, get_type_hints

import yaml

from scripts.source_model import (
    ERROR_CODES, ROLE_QUALIFICATIONS, DecisionPatch, Issue, ReferenceKind, ReferenceUse,
    SCHEMA_IDS, validate_references,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]

class SourceContractTests(unittest.TestCase):
    def test_public_types_have_exact_fields(self):
        self.assertEqual(("code", "file", "record", "field_path", "message"), Issue._fields)
        self.assertEqual(("kind", "file", "record", "field_path", "value"), ReferenceUse._fields)
        self.assertEqual(("identity", "field", "value", "qid"), DecisionPatch._fields)
        self.assertEqual(("basis", "source", "match", "external_group"),
                         get_args(ReferenceKind))

    def test_validate_references_has_exact_signature(self):
        self.assertEqual({"root": Path, "references": Sequence[ReferenceUse],
                          "return": List[Issue]}, get_type_hints(validate_references))

    def test_schema_ids_are_exact(self):
        expected = {
            "source-entities.schema.json": "urn:kb-design:schema:source-entities:2",
            "source-uses.schema.json": "urn:kb-design:schema:source-uses:2",
            "source-obligations.schema.json": "urn:kb-design:schema:source-obligations:1",
            "source-reference-index.schema.json": "urn:kb-design:schema:source-reference-index:1",
            "source-probe.schema.json": "urn:kb-design:schema:source-probe:1",
            "source-migration.schema.json": "urn:kb-design:schema:source-migration:1",
            "decision.schema.json": "urn:kb-design:schema:decision:1",
        }
        self.assertEqual(expected, SCHEMA_IDS)

    def test_role_qualifications_are_exact(self):
        self.assertEqual({"basis": None, "source": "structure", "match": "mapping",
                          "external_group": "structure"}, ROLE_QUALIFICATIONS)

    def test_error_codes_are_exact_and_stable(self):
        self.assertEqual(26, len(ERROR_CODES))
        self.assertEqual(26, len(set(ERROR_CODES)))
        self.assertIn("SOURCE_ROLE_NOT_APPROVED", ERROR_CODES)
        self.assertIn("SOURCE_DECISION_DELIVERY_MISSING", ERROR_CODES)

```

  `tests/test_source_schema.py` 读取七份完整 schema 和正反例。

  `tests/source_governance_helpers.py` 是唯一跨测试文件公共模块；每个消费者显式导入，不依赖另一测试文件的全局名称。

```python
from pathlib import Path

import yaml

from scripts.source_model import ReferenceUse

def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def approved_and_unapproved_role_references():
    basis = [{"entity": "cs2023", "locator": "SE overview", "checked": "2026-08-31"}]
    return [
        ReferenceUse("source", "vocab/terms.yaml", "concept:tc-1", "source",
                     {"registry": "mapping-only", "item": "SE", "locator": "SE",
                      "basis": basis}),
        ReferenceUse("match", "vocab/terms.yaml", "concept:tc-1", "match[0]",
                     {"registry": "mapping-only", "item": "SE", "rel": "exactMatch",
                      "basis": basis}),
    ]

def unapproved_external_group_reference():
    return ReferenceUse("external_group", "vocab/topics.yaml", "array:security-asvs",
                        "arrays[0].external_group",
                        {"registry": "mapping-only", "item": "V11",
                         "locator": "ASVS chapter V11",
                         "basis": [{"entity": "asvs", "locator": "V11",
                                    "checked": "2026-08-31"}]})
```

```python
import json
import pathlib
import unittest

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "source-governance"
SCHEMA_NAMES = (
    "source-entities.schema.json", "source-uses.schema.json",
    "source-obligations.schema.json", "source-reference-index.schema.json",
    "source-probe.schema.json", "source-migration.schema.json", "decision.schema.json",
)

def load_schema(name):
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))

def load_fixture(name):
    return yaml.safe_load((FIXTURES / name).read_text(encoding="utf-8"))

def errors(schema_name, fixture_name):
    return list(Draft202012Validator(load_schema(schema_name),
                format_checker=FormatChecker()).iter_errors(load_fixture(fixture_name)))

def validate_definition(schema_name, definition, value):
    schema = load_schema(schema_name)
    definition_schema = {"$schema": schema["$schema"], "$defs": schema["$defs"],
                         "$ref": f"#/$defs/{definition}"}
    return list(Draft202012Validator(definition_schema,
                format_checker=FormatChecker()).iter_errors(value))

class SourceSchemaTests(unittest.TestCase):
    def test_all_seven_schemas_pass_meta_validation(self):
        for name in sorted(SCHEMA_NAMES):
            Draft202012Validator.check_schema(load_schema(name))

    def test_valid_documents_pass(self):
        self.assertEqual([], errors("source-entities.schema.json", "valid/entities.yaml"))
        self.assertEqual([], errors("source-uses.schema.json", "valid/sources.yaml"))
        self.assertEqual([], errors("source-obligations.schema.json", "valid/obligations.yaml"))
        self.assertEqual([], errors("decision.schema.json", "valid/decision.yaml"))

    def test_basis_requires_locator(self):
        self.assertTrue(errors("source-entities.schema.json", "invalid/basis-missing-locator.yaml"))

    def test_source_requires_nested_basis(self):
        self.assertTrue(validate_definition("source-migration.schema.json", "source",
                                            load_fixture("invalid/source-missing-basis.yaml")))

    def test_match_rejects_unknown_relation(self):
        self.assertTrue(validate_definition("source-migration.schema.json", "match",
                                            load_fixture("invalid/match-invalid-rel.yaml")))

    def test_entity_rejects_scalar_url_in_strict_schema(self):
        self.assertTrue(errors("source-entities.schema.json", "invalid/entity-scalar-url.yaml"))

    def test_approved_role_requires_decision(self):
        self.assertTrue(errors("source-uses.schema.json", "invalid/role-missing-decision.yaml"))

    def test_resolved_obligation_cannot_reopen(self):
        self.assertTrue(errors("source-obligations.schema.json", "invalid/obligation-reopened.yaml"))

    def test_migration_rejects_unknown_disposition(self):
        self.assertTrue(errors("source-migration.schema.json", "invalid/migration-unknown-disposition.yaml"))

    def test_decision_front_matter_requires_stable_id(self):
        self.assertTrue(errors("decision.schema.json", "invalid/decision-missing-id.yaml"))

    def test_payload_manifest_requires_topics_after_hash(self):
        invalid = load_fixture("invalid/cutover-manifest-missing-topics-hash.yaml")
        self.assertTrue(validate_definition("source-migration.schema.json",
                                            "cutoverPayloadManifest", invalid))

    def test_payload_manifest_rejects_its_own_path(self):
        invalid = load_fixture("invalid/cutover-manifest-self-entry.yaml")
        self.assertTrue(validate_definition("source-migration.schema.json",
                                            "cutoverPayloadManifest", invalid))

    def test_valid_source_handoff_passes(self):
        value = load_fixture("valid/source-cutover-handoff.yaml")
        self.assertEqual([], validate_definition("source-migration.schema.json",
                                                 "sourceCutoverHandoff", value))

    def test_source_handoff_requires_seven_schemas(self):
        invalid = load_fixture("invalid/source-handoff-missing-schemas.yaml")
        self.assertTrue(validate_definition("source-migration.schema.json",
                                            "sourceCutoverHandoff", invalid))
```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_source_contract tests.test_source_schema -v`

  Expected: ERROR，明确报告 `scripts.source_model`、七份 schema 与基线脚本不存在；失败不得来自 YAML 语法。

- [ ] **实现共享类型与常量**

  `requirements-dev.txt` 只写两行：

```text
PyYAML==6.0.3
jsonschema==4.23.0
```

  在 `scripts/source_model.py` 写入接口锁中的 `ReferenceKind`、`Issue`、`ReferenceUse`、`DecisionPatch`、`ApplyResult`，并逐字写入 `SCHEMA_IDS`、`ROLE_QUALIFICATIONS` 和 26 个 `ERROR_CODES`。模块级 `__all__` 只公开 `ReferenceKind`、`Issue`、`ReferenceUse`、`DecisionPatch`、`ApplyResult`、`SCHEMA_IDS`、`ROLE_QUALIFICATIONS`、`ERROR_CODES`、`validate_references`、`collect_reference_uses`、`validate_repository`。

- [ ] **实现七份完整 schema**

  `build_schema_documents()` 使用以下完整构造算法；每个对象都通过 `closed()` 设置 `additionalProperties: false`，所有数组显式设置 `items`，所有 ID、日期、哈希和枚举都由共享定义约束。执行 `python3 scripts/source_model.py write-schemas --directory schemas` 按键排序和两空格缩进写出七份 JSON。

```python
from copy import deepcopy

META = "https://json-schema.org/draft/2020-12/schema"
ID = {"type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"}
DATE = {"type": "string", "format": "date"}
HASH = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
NONEMPTY = {"type": "string", "minLength": 1}

def array(items, minimum=0):
    value = {"type": "array", "items": items}
    if minimum:
        value["minItems"] = minimum
    return value

def closed(required, properties):
    return {"type": "object", "additionalProperties": False,
            "required": list(required), "properties": properties}

BASIS_ITEM = closed(("entity", "locator"),
                    {"entity": ID, "locator": NONEMPTY, "checked": DATE})
BASIS_LIST = array({"$ref": "#/$defs/basisItem"}, 1)
SOURCE = closed(("registry", "item", "locator", "basis"),
                {"registry": ID, "item": NONEMPTY, "locator": NONEMPTY,
                 "basis": BASIS_LIST})
MATCH = closed(("registry", "item", "rel", "basis"),
               {"registry": ID, "item": NONEMPTY,
                "rel": {"enum": ["exactMatch", "closeMatch", "broadMatch",
                                  "narrowMatch", "relatedMatch"]},
                "basis": BASIS_LIST})
LOCAL_ANALYSIS = closed(("legacy_source_label", "state", "decision"),
                        {"legacy_source_label": NONEMPTY,
                         "state": {"const": "isolated"},
                         "decision": {"const": "decision-source-0005"}})
EXTERNAL_GROUP = closed(("registry", "item", "locator", "basis"),
                        {"registry": ID, "item": NONEMPTY, "locator": NONEMPTY,
                         "basis": BASIS_LIST})
URL = closed(("role", "url", "primary"),
             {"role": {"enum": ["canonical", "landing", "doi", "full_text",
                                      "status", "mirror", "archive"]},
              "url": {"type": "string", "format": "uri"},
              "primary": {"type": "boolean"}})
REVIEW = closed(("checked", "next_due", "interval_months", "grace_days", "obligations"),
                {"checked": {"oneOf": [DATE, {"type": "null"}]},
                 "next_due": {"oneOf": [DATE, {"type": "null"}]},
                 "interval_months": {"oneOf": [{"enum": [6, 12, 24]}, {"type": "null"}]},
                 "grace_days": {"const": 30},
                 "obligations": array(ID)})
WATCH = closed(("locator", "signals", "cadence_months"),
               {"locator": {"type": "string", "format": "uri"},
                "signals": array({"enum": ["availability", "redirect", "version",
                                                    "revision", "replacement", "withdrawal"]}, 1),
                "cadence_months": closed(("availability", "redirect", "content"),
                                           {"availability": {"const": 1},
                                            "redirect": {"const": 1},
                                            "content": {"enum": [1, 3, 6, 12]}})})
HISTORY = closed(("date", "action", "fields", "decisions"),
                 {"date": DATE, "action": NONEMPTY, "fields": array(NONEMPTY),
                  "decisions": array(ID), "basis": array(BASIS_ITEM),
                  "before": {}, "after": {}})
ROLE = closed(("role", "status", "decision"),
              {"role": {"enum": ["mapping", "structure", "group", "discovery"]},
               "status": {"enum": ["proposed", "approved", "retired"]},
               "decision": {"oneOf": [ID, {"type": "null"}]}})
ROLE["allOf"] = [
    {"if": {"properties": {"status": {"enum": ["approved", "retired"]}}},
     "then": {"properties": {"decision": ID}}},
    {"if": {"properties": {"status": {"const": "proposed"}}},
     "then": {"properties": {"decision": {"type": "null"}}}},
]
TARGET = closed(("kind", "file", "record", "field_path"),
                {"kind": {"enum": ["basis", "source", "match", "use_role",
                                     "decision", "obligation"]},
                 "file": NONEMPTY, "record": NONEMPTY, "field_path": NONEMPTY})
DISPOSITIONS = ["register", "merge_address", "merge_locator", "retain_legacy",
                "not_migrated_missing_locator", "no_external_basis", "project_assertion",
                "blocked_unread_material", "unresolved_external_status", "proposed_role",
                "approved_role", "retired_role", "not_in_scope", "isolated_local_analysis"]

def base_schema(name, version, defs=None):
    value = {"$schema": META, "$id": SCHEMA_IDS[name]}
    if defs:
        value["$defs"] = defs
    return value

def build_schema_documents():
    entity = closed(
        ("id", "label", "kind"),
        {"id": ID, "label": {"type": "object", "minProperties": 1,
                               "additionalProperties": {"type": "string"}},
         "kind": NONEMPTY, "version": {"oneOf": [NONEMPTY, {"type": "null"}]},
         "urls": array(URL, 1), "status": {"enum": ["current", "superseded", "withdrawn"]},
         "basis": {"type": "object", "minProperties": 1,
                    "additionalProperties": array(BASIS_ITEM, 1)},
         "review": REVIEW, "watch": array(WATCH),
         "replaced_by": {"oneOf": [ID, {"type": "null"}]},
         "history": array(HISTORY, 1)})
    entity["allOf"] = [{
        "if": {"properties": {"kind": {"enum": ["standard", "publication"]}},
               "required": ["kind"]},
        "then": {"required": ["version", "urls", "status", "basis", "review",
                                "watch", "replaced_by", "history"]},
    }]
    entities = base_schema("source-entities.schema.json", 2, {"basisItem": BASIS_ITEM})
    entities.update(closed(("schema", "schema_version", "version", "entities"),
                           {"schema": {"const": "urn:kb-design:data:entities"},
                            "schema_version": {"const": 2}, "version": {"type": "object"},
                            "entities": array(entity, 1)}))

    use = closed(("id", "entity", "roles", "history"),
                 {"id": ID, "entity": ID, "roles": array(ROLE, 1),
                  "history": array(HISTORY, 1)})
    uses = base_schema("source-uses.schema.json", 2)
    uses.update(closed(("schema", "schema_version", "version", "sources"),
                       {"schema": {"const": "urn:kb-design:data:source-uses"},
                        "schema_version": {"const": 2}, "version": {"type": "object"},
                        "sources": array(use, 1)}))

    obligation = closed(("id", "entity", "trigger", "targets", "decisions", "previous",
                         "state", "opened", "resolved", "history"),
                        {"id": ID, "entity": ID,
                         "trigger": {"enum": ["periodic", "address_change", "content_change",
                                              "new_version", "replacement", "withdrawal",
                                              "temporarily_unavailable", "decision_adopted",
                                              "decision_superseded", "decision_overturned"]},
                         "targets": array(TARGET, 1), "decisions": array(ID),
                         "previous": {"oneOf": [ID, {"type": "null"}]},
                         "state": {"enum": ["open", "resolved"]}, "opened": DATE,
                         "resolved": {"oneOf": [DATE, {"type": "null"}]},
                         "history": array({"type": "object"}, 1)})
    obligation["allOf"] = [
        {"if": {"properties": {"state": {"const": "open"}}},
         "then": {"properties": {"resolved": {"type": "null"}}}},
        {"if": {"properties": {"state": {"const": "resolved"}}},
         "then": {"properties": {"resolved": DATE}}},
    ]
    obligations = base_schema("source-obligations.schema.json", 1)
    obligations.update(closed(("schema", "schema_version", "obligations"),
                              {"schema": {"const": "urn:kb-design:data:source-obligations"},
                               "schema_version": {"const": 1},
                               "obligations": array(obligation)}))

    index_entry = closed(("target_kind", "target_id", "reference_kind", "file", "record",
                          "field_path"),
                         {"target_kind": NONEMPTY, "target_id": ID,
                          "reference_kind": NONEMPTY, "file": NONEMPTY,
                          "record": NONEMPTY, "field_path": NONEMPTY})
    index = base_schema("source-reference-index.schema.json", 1)
    index.update(closed(("schema", "schema_version", "entries"),
                        {"schema": {"const": "urn:kb-design:data:source-reference-index"},
                         "schema_version": {"const": 1}, "entries": array(index_entry)}))

    observation = closed(("id", "observed_at", "entity", "endpoint", "request", "response",
                          "signals", "previous", "errors"),
                         {"id": ID, "observed_at": {"type": "string", "format": "date-time"},
                          "entity": ID, "endpoint": {"type": "string", "format": "uri"},
                          "request": closed(("method",), {"method": {"enum": ["HEAD", "GET"]}}),
                          "response": {"type": "object"}, "signals": array(NONEMPTY),
                          "previous": {"oneOf": [ID, {"type": "null"}]},
                          "errors": array(NONEMPTY)})
    probe = base_schema("source-probe.schema.json", 1)
    probe.update(closed(("schema", "schema_version", "observations"),
                        {"schema": {"const": "urn:kb-design:data:source-probe"},
                         "schema_version": {"const": 1},
                         "observations": array(observation)}))

    trace = closed(("qid", "field", "value_sha256"),
                   {"qid": {"pattern": "^Q(?:0[1-9]|1[0-9]|2[0-5])$"},
                    "field": NONEMPTY, "value_sha256": HASH})
    row = closed(("identity", "operation", "disposition", "new_value",
                  "decision_trace", "blocks_cutover"),
                 {"identity": NONEMPTY,
                  "operation": {"enum": ["keep", "set", "delete", "isolate"]},
                  "disposition": {"enum": DISPOSITIONS},
                  "decision": ID, "decision_trace": array(trace, 1),
                  "blocks_cutover": {"type": "boolean"},
                  "old_file": NONEMPTY, "old_record": NONEMPTY, "old_value": {},
                  "new_value": {}, "decisions": array(ID), "rollback_key": NONEMPTY})
    payload_entry = closed(("path", "after_sha256"),
                           {"path": {"allOf": [NONEMPTY,
                                               {"not": {"enum": [
                                                   "vocab/generated/source-cutover-payload.json",
                                                   "vocab/generated/source-cutover-handoff.json"]}}]},
                            "after_sha256": {"oneOf": [HASH, {"type": "null"}]}})
    cutover = closed(("schema", "schema_version", "entries"),
                     {"schema": {"const": "urn:kb-design:data:source-cutover-payload"},
                      "schema_version": {"const": 1},
                      "entries": {"type": "array", "minItems": 1,
                                  "uniqueItems": True, "items": payload_entry,
                                  "contains": closed(("path", "after_sha256"),
                                                     {"path": {"const": "vocab/topics.yaml"},
                                                      "after_sha256": HASH})}})
    path_hash = closed(("path", "sha256"), {"path": NONEMPTY, "sha256": HASH})
    schema_hash = closed(("path", "$id", "schema_version", "sha256"),
                         {"path": NONEMPTY, "$id": NONEMPTY,
                          "schema_version": {"type": "integer", "minimum": 1},
                          "sha256": HASH})
    source_contract = closed(("module", "sha256", "reference_kinds",
                              "role_qualifications", "error_codes"),
                             {"module": {"const": "scripts/source_model.py"},
                              "sha256": HASH,
                              "reference_kinds": {"type": "array", "minItems": 4,
                                                  "maxItems": 4, "uniqueItems": True,
                                                  "items": {"enum": ["basis", "source", "match",
                                                                     "external_group"]}},
                              "role_qualifications": closed(
                                  ("basis", "source", "match", "external_group"),
                                  {"basis": {"type": "null"},
                                   "source": {"const": "structure"},
                                   "match": {"const": "mapping"},
                                   "external_group": {"const": "structure"}}),
                              "error_codes": {"type": "array", "minItems": 26,
                                              "maxItems": 26, "uniqueItems": True,
                                              "items": NONEMPTY}})
    output = closed(("path", "kind", "sha256"),
                    {"path": NONEMPTY, "kind": {"enum": ["topics", "source_index"]},
                     "sha256": HASH, "concepts": {"type": "integer"},
                     "arrays": {"type": "integer"}})
    handoff = closed(("schema", "schema_version", "payload", "source_contract", "schemas",
                      "topics_sha256", "migration_ledgers", "markdown_manifest",
                      "outputs", "tracked_write_set"),
                     {"schema": {"const": "urn:kb-design:data:source-cutover-handoff"},
                      "schema_version": {"const": 1}, "payload": path_hash,
                      "source_contract": source_contract,
                      "schemas": {"type": "array", "minItems": 7, "maxItems": 7,
                                  "uniqueItems": True, "items": schema_hash},
                      "topics_sha256": HASH,
                      "migration_ledgers": {"type": "array", "minItems": 6,
                                            "maxItems": 6, "uniqueItems": True,
                                            "items": path_hash},
                      "markdown_manifest": array(path_hash, 1),
                      "outputs": {"type": "array", "minItems": 2, "maxItems": 2,
                                  "uniqueItems": True, "items": output},
                      "tracked_write_set": array(NONEMPTY, 1)})
    migration = base_schema("source-migration.schema.json", 1,
                            {"basisItem": BASIS_ITEM, "source": SOURCE, "match": MATCH,
                             "externalGroup": EXTERNAL_GROUP,
                             "localAnalysis": LOCAL_ANALYSIS,
                             "row": row, "cutoverPayloadManifest": cutover,
                             "sourceCutoverHandoff": handoff})
    migration.update(closed(("schema", "schema_version", "rows"),
                            {"schema": {"const": "urn:kb-design:data:source-migration"},
                             "schema_version": {"const": 1}, "rows": array(row)}))

    patch = closed(("identity", "field", "value"),
                   {"identity": NONEMPTY, "field": NONEMPTY, "value": {}})
    answer = closed(("question", "resolution", "patches"),
                    {"question": {"pattern": "^Q(?:0[1-9]|1[0-9]|2[0-5])$"},
                     "resolution": {"enum": ["recommended", "replacement"]},
                     "patches": array(patch, 1)})
    decision = base_schema("decision.schema.json", 1)
    decision.update(closed(("id", "schema", "schema_version", "status", "date", "level",
                            "scope", "supersedes", "answers"),
                           {"id": ID, "schema": {"const": "urn:kb-design:data:decision"},
                            "schema_version": {"const": 1},
                            "status": {"enum": ["proposed", "accepted", "superseded", "overturned"]},
                            "date": DATE, "level": {"enum": ["L1", "L2", "L3"]},
                            "scope": NONEMPTY, "supersedes": array(ID),
                            "answers": array(answer, 1),
                            "delivery_handoff": NONEMPTY, "handoff_sha256": HASH,
                            "delivery_payload": NONEMPTY, "payload_sha256": HASH}))
    return {"source-entities.schema.json": entities, "source-uses.schema.json": uses,
            "source-obligations.schema.json": obligations,
            "source-reference-index.schema.json": index, "source-probe.schema.json": probe,
            "source-migration.schema.json": migration, "decision.schema.json": decision}
```

  CLI 使用 `argparse` 的两个子命令：`write-schemas --directory PATH` 调用 `build_schema_documents()` 并以排序键、两空格缩进和末尾换行写 JSON；`decisions --directory design/decisions --require Q01,Q02` 调用 `load_decision_patches()`，要求每个 Q 至少一项 patch，按 Q 排序打印 `Q resolution patch_count patch_set_sha256`，缺失时打印 `SOURCE_DECISION_DELIVERY_MISSING` 并退出 1。没有第三种隐式模式。

- [ ] **实现旧链接基线**

  `scripts/check_link_baseline.py` 使用下列完整实现；要求退出码 1 与执行门禁三行 stdout 逐字相等，相等时只输出零退出状态，否则打印 unified diff 并退出 1。

```python
#!/usr/bin/env python3
import difflib
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED = (
    ".superpowers/sdd/2026-08-30-basic-unit-consumer-classification/agentic-plan.md:11: "
    "文件不存在 ../specs/2026-08-30-basic-unit-consumer-classification-design.md\n"
    ".superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/"
    "human-decision-package.md:340: 锚点不存在 ../../../../design/sources-registry.md#L68\n"
    "2 处问题\n"
)

result = subprocess.run([sys.executable, "scripts/check-links.py"], cwd=ROOT,
                        text=True, capture_output=True)
if result.returncode != 1 or result.stdout != EXPECTED or result.stderr:
    sys.stdout.writelines(difflib.unified_diff(
        EXPECTED.splitlines(True), result.stdout.splitlines(True),
        fromfile="expected-link-baseline", tofile="actual-link-baseline"))
    if result.stderr:
        sys.stderr.write(result.stderr)
    raise SystemExit(1)
print("KNOWN_LINK_BASELINE_OK count=2")
```

- [ ] **安装并运行 GREEN**

  Run: `python3 -m pip install -r requirements-dev.txt && python3 scripts/source_model.py write-schemas --directory schemas && python3 -m unittest tests.test_source_contract tests.test_source_schema -v && python3 scripts/check_link_baseline.py`

  Expected: 19 项高风险测试通过；七份 schema 通过 meta validation；有效夹具零错误；payload 自引用／缺 topics hash 与 handoff 缺七份 schema 反例被拒绝；输出 `KNOWN_LINK_BASELINE_OK count=2`。

- [ ] **延后阶段回归**

  本任务只运行模式契约的定向 GREEN 与写集检查；完整回归并入离线校验的契约闭合门禁。

- [ ] **核对写集**

  Run: `git diff --name-only -- requirements-dev.txt scripts/source_model.py scripts/check_link_baseline.py schemas tests/source_governance_helpers.py tests/test_source_contract.py tests/test_source_schema.py tests/fixtures/source-governance`

  Expected: 只列本任务 Files 中的创建文件。

- [ ] **说明回滚**

  回滚边界是依赖、共享模块、schema、基线脚本、夹具和测试，不触碰正式数据。若提交后被拒绝，使用 `apply_patch` 恢复任务前内容并创建新的 `[L2] revert: compensate source governance schema task` 补偿提交；不删除任何已经被决定引用的 ID 或决定文件。

- [ ] **提交任务**

```bash
git add requirements-dev.txt scripts/source_model.py scripts/check_link_baseline.py schemas tests/source_governance_helpers.py tests/test_source_contract.py tests/test_source_schema.py tests/fixtures/source-governance
git commit -m "[L2] feat: define source governance schemas"
```

### 离线校验

**Files:**

- Modify: `scripts/source_model.py`
- Create: `scripts/check_sources.py`
- Create: `tests/test_check_sources.py`
- Create: `tests/fixtures/source-governance/previous/`
- Create: `tests/fixtures/source-governance/current/`
- Create: `tests/fixtures/source-governance/reference-contract/`

**Interfaces:**

- Consumes: 七个 schema、正式根目录、可选前一快照、`ReferenceUse` 序列和 accepted 决定 patches。
- Produces: `validate_references(root: Path, references: Sequence[ReferenceUse]) -> List[Issue]`、`validate_repository(root: Path, previous_root: Optional[Path] = None, allow_legacy: bool = False) -> List[Issue]`、`compute_next_due(checked: date, interval_months: Optional[int]) -> Optional[date]`、`is_review_overdue(next_due: Optional[date], today: date, grace_days: int = 30) -> bool`、`load_decision_patches(paths: Sequence[Path]) -> Sequence[DecisionPatch]`。

**人工门禁:** Q02、Q03、Q07、Q09、Q10、Q11、Q13、Q18、Q19 有 accepted patches。任一缺失时停止，不创建测试或 ignored 输出。

- [ ] **写入失败测试**

```python
import hashlib
import json
import pathlib
import unittest

from datetime import date
import yaml

from scripts.source_model import (
    DecisionPatch, ReferenceUse, compute_next_due, is_review_overdue,
    load_decision_patches, validate_references, validate_repository,
)
from tests.source_governance_helpers import (
    approved_and_unapproved_role_references, unapproved_external_group_reference,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "source-governance"

class CheckSourcesTests(unittest.TestCase):
    def issues(self, name, previous=None, allow_legacy=False):
        old = FIXTURES / previous if previous else None
        return validate_repository(FIXTURES / name, old, allow_legacy)

    def test_valid_repository_has_no_issues(self):
        self.assertEqual([], self.issues("valid"))

    def test_stable_id_change_is_rejected(self):
        self.assertIn("SOURCE_STABLE_ID_CHANGED",
                      {x.code for x in self.issues("current", "previous")})

    def test_history_deletion_and_reordering_are_rejected(self):
        codes = {x.code for x in self.issues("current", "previous")}
        self.assertIn("SOURCE_HISTORY_NOT_APPEND_ONLY", codes)

    def test_role_decision_and_registry_role_are_checked(self):
        codes = {x.code for x in self.issues("current")}
        self.assertTrue({"SOURCE_ROLE_DECISION_MISSING", "SOURCE_ROLE_NOT_APPROVED"} <= codes)

    def test_mutable_basis_requires_checked(self):
        self.assertIn("SOURCE_BASIS_CHECKED_MISSING", {x.code for x in self.issues("current")})

    def test_temporary_failure_cannot_withdraw_entity(self):
        self.assertIn("SOURCE_SCHEMA_INVALID", {x.code for x in self.issues("current")})

    def test_resolved_obligation_retrigger_gets_new_id(self):
        self.assertIn("SOURCE_OBLIGATION_REOPENED",
                      {x.code for x in self.issues("current", "previous")})

    def test_strict_mode_rejects_legacy_fields(self):
        self.assertIn("SOURCE_LEGACY_FIELD",
                      {x.code for x in self.issues("current", allow_legacy=False)})

    def test_basis_reference_needs_existing_entity(self):
        ref = ReferenceUse("basis", "vocab/terms.yaml", "concept:tc-1",
                           "definitions[0].basis[0]",
                           {"entity": "missing", "locator": "§ 1"})
        self.assertEqual("SOURCE_ENTITY_MISSING",
                         validate_references(FIXTURES / "reference-contract", [ref])[0].code)

    def test_source_and_match_consume_distinct_approved_roles(self):
        refs = approved_and_unapproved_role_references()
        issues = validate_references(FIXTURES / "reference-contract", refs)
        self.assertEqual(["SOURCE_ROLE_NOT_APPROVED"], [issue.code for issue in issues])

    def test_external_group_requires_approved_structure_role(self):
        issues = validate_references(FIXTURES / "reference-contract",
                                     [unapproved_external_group_reference()])
        self.assertEqual(["SOURCE_EXTERNAL_GROUP_ROLE_NOT_APPROVED"],
                         [issue.code for issue in issues])

    def test_next_due_uses_calendar_months(self):
        self.assertEqual(date(2028, 2, 29), compute_next_due(date(2026, 2, 28), 24))
        self.assertEqual(date(2027, 8, 31), compute_next_due(date(2026, 8, 31), 12))
        self.assertEqual(date(2027, 2, 28), compute_next_due(date(2026, 8, 31), 6))

    def test_archival_review_has_no_content_due_date(self):
        self.assertIsNone(compute_next_due(date(2026, 8, 31), None))

    def test_review_grace_boundary_is_exact(self):
        self.assertFalse(is_review_overdue(date(2026, 8, 31), date(2026, 9, 30)))
        self.assertTrue(is_review_overdue(date(2026, 8, 31), date(2026, 10, 1)))

    def test_replacement_decision_patches_are_returned_verbatim(self):
        patches = load_decision_patches([FIXTURES / "reference-contract/replacement-decision.md"])
        expected = [DecisionPatch(**row) for row in yaml.safe_load(
            (FIXTURES / "reference-contract/replacement-patches.yaml").read_text(encoding="utf-8"))]
        self.assertEqual(expected, list(patches))
```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_check_sources -v`

  Expected: FAIL，报告 `validate_references`、周期函数、决定读取或稳定错误码尚未实现。

- [ ] **实现共享校验器**

  `_validate_references()` 按输入顺序验证每个 `ReferenceUse`，但最终 Issue 按 `(file, record, field_path, code)` 排序；不修改输入。算法固定为：先验证 kind 与 value schema；basis 解析 entity；source／match 解析 registry，再读取相应 role，要求 `approved` 和 accepted decision；最后递归验证嵌套 basis。失败只使用接口锁错误码。

```python
def validate_repository(root, previous_root=None, allow_legacy=False):
    documents = load_documents(root)
    issues = validate_schemas(documents)
    issues.extend(validate_ids(documents, previous_root))
    issues.extend(validate_references(root, collect_repository_references(root, allow_legacy)))
    issues.extend(validate_obligations(documents, previous_root))
    issues.extend(validate_history(documents, previous_root))
    issues.extend(validate_legacy_fields(documents, allow_legacy))
    return sort_issues(issues)
```

  `validate_references()` 的最小实现按下列算法写入同一模块，不把结构或角色逻辑留给消费者。

```python
def validate_references(root: Path,
                        references: Sequence[ReferenceUse]) -> List[Issue]:
    entities = load_source_entities(root / "vocab/entities.yaml")
    uses = load_source_uses(root / "vocab/sources.yaml")
    accepted = load_accepted_decision_ids(root / "design/decisions")
    issues = []
    for reference in references:
        if reference.kind not in ROLE_QUALIFICATIONS:
            issues.append(issue(reference, "SOURCE_REFERENCE_KIND_INVALID"))
            continue
        structural = validate_reference_value(reference.kind, reference.value)
        if structural:
            issues.extend(issue(reference, code) for code in structural)
            continue
        if reference.kind == "basis":
            entity = entities.get(reference.value["entity"])
            if entity is None:
                issues.append(issue(reference, "SOURCE_ENTITY_MISSING"))
                continue
            if not reference.value.get("locator"):
                issues.append(issue(reference, "SOURCE_BASIS_LOCATOR_MISSING"))
            if content_is_mutable(entity, reference.value) and not reference.value.get("checked"):
                issues.append(issue(reference, "SOURCE_BASIS_CHECKED_MISSING"))
            continue
        registry = reference.value["registry"]
        source_use = uses.get(registry)
        if source_use is None:
            issues.append(issue(reference, "SOURCE_USE_MISSING"))
            continue
        role_name = ROLE_QUALIFICATIONS[reference.kind]
        role = next((row for row in source_use["roles"] if row["role"] == role_name), None)
        if role is None or role["status"] != "approved":
            code = ("SOURCE_EXTERNAL_GROUP_ROLE_NOT_APPROVED"
                    if reference.kind == "external_group" else "SOURCE_ROLE_NOT_APPROVED")
            issues.append(issue(reference, code))
        elif role.get("decision") not in accepted:
            code = ("SOURCE_EXTERNAL_GROUP_ROLE_NOT_APPROVED"
                    if reference.kind == "external_group" else "SOURCE_ROLE_DECISION_MISSING")
            issues.append(issue(reference, code))
        for index, basis in enumerate(reference.value["basis"]):
            nested = ReferenceUse("basis", reference.file, reference.record,
                                  f"{reference.field_path}.basis[{index}]", basis)
            issues.extend(validate_references(root, [nested]))
    return sort_issues(issues)
```

  `load_source_entities()` 只返回 kind 为 standard／publication 的 `id -> record`；`load_source_uses()` 返回 use ID 映射；`load_accepted_decision_ids()` 解析所有 source 决定 front matter 并只返回 status accepted 的 ID。`validate_reference_value()` 先用 `$defs` 校验对象类型；非对象返回 `SOURCE_REFERENCE_VALUE_INVALID`；basis 缺 locator 返回 `SOURCE_BASIS_LOCATOR_MISSING`；source 与 external_group 缺 item／locator／basis 分别返回 `SOURCE_SOURCE_ITEM_MISSING`、`SOURCE_SOURCE_LOCATOR_MISSING`、`SOURCE_SOURCE_BASIS_MISSING`；match rel 非五值返回 `SOURCE_MATCH_REL_INVALID`，缺 basis 返回 `SOURCE_MATCH_BASIS_MISSING`。`issue()` 总是复制 ReferenceUse 的 file、record、field_path。`content_is_mutable()` 仅在来源实体 basis 指向固定版本且固定文件 SHA-256 时返回 false。

  周期函数使用下列实现；月末来源保持目标月末，其他日期按目标月天数截断。

```python
import calendar
from datetime import date, timedelta

def add_calendar_months(value, months):
    absolute = value.year * 12 + value.month - 1 + months
    year, month0 = divmod(absolute, 12)
    month = month0 + 1
    old_last = calendar.monthrange(value.year, value.month)[1]
    new_last = calendar.monthrange(year, month)[1]
    day = new_last if value.day == old_last else min(value.day, new_last)
    return date(year, month, day)

def compute_next_due(checked, interval_months):
    return None if interval_months is None else add_calendar_months(checked, interval_months)

def is_review_overdue(next_due, today, grace_days=30):
    return next_due is not None and today > next_due + timedelta(days=grace_days)
```

  `load_decision_patches()` 解析 front matter，要求 accepted、Q 唯一、patches 非空；为每项构造 `DecisionPatch(identity, field, value, qid)` 并返回排序后的不可变序列。`decision_patch_sha256()` 对 qid、identity、field、value 的排序键紧凑 JSON 计算哈希。不把 `recommended` 固化为代码分支。

  `allow_legacy=True` 只允许迁移读取器识别旧结构并生成 `SOURCE_LEGACY_FIELD`，不把旧值视为通过；默认严格模式拒绝紧缩 basis、旧 match.source、角色字符串数组、旧 origin 和单值 url。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_check_sources -v`

  Expected: 15 项高风险测试通过；稳定错误码、external_group 资格、24／12／6 个月、archival null、30 日边界和 replacement patches 全部通过。

- [ ] **验证命令接口**

  Run: `python3 scripts/check_sources.py --root tests/fixtures/source-governance/valid && python3 scripts/check_sources.py --root tests/fixtures/source-governance/current --previous tests/fixtures/source-governance/previous`

  Expected: 第一条退出 0 且输出 `0 source governance issues`；第二条退出 1 并逐项列出测试期待的 code、文件、记录与字段路径。

- [ ] **运行契约闭合回归**

  Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v && python3 scripts/check-topics.py && python3 scripts/check_link_baseline.py && git diff --check`

  Expected: 全部测试通过；链接基线输出 `KNOWN_LINK_BASELINE_OK count=2`；差异检查继续运行并通过。

- [ ] **核对写集**

  Run: `git diff --name-only -- scripts/source_model.py scripts/check_sources.py tests/test_check_sources.py tests/fixtures/source-governance/previous tests/fixtures/source-governance/current`

  Expected: 只列本任务文件。

- [ ] **说明回滚**

  若任务提交后被拒绝，使用 `apply_patch` 恢复本任务修改并创建新的 `[L2] revert: compensate offline source validation task` 补偿提交；不得删除模式决定、已分配 ID 或历史。

- [ ] **提交任务**

```bash
git add scripts/source_model.py scripts/check_sources.py tests/test_check_sources.py tests/fixtures/source-governance/previous tests/fixtures/source-governance/current
git commit -m "[L2] feat: add offline source validation"
```

### 反向索引

**Files:**

- Create: `scripts/build_source_index.py`
- Create: `tests/test_source_index.py`
- Create: `tests/fixtures/source-governance/index-root/`
- Create: `tests/fixtures/source-governance/index-expected.json`
- Create: `tests/fixtures/source-governance/future-consumer/vocab/terms.yaml`
- Generate at cutover: `vocab/generated/source-reference-index.json`

**Interfaces:**

- Consumes: 所有受跟踪正式 YAML／JSON、决定 front matter、来源义务；迁移预演另以 `include_legacy=True` 读取旧共享结构。
- Produces: `build_reference_index(root: Path, include_legacy: bool) -> Dict[str, object]`；每项含 `target_kind`、`target_id`、`reference_kind`、`file`、`record`、`field_path`，按六字段稳定排序。
- Internal: `discover_formal_documents(root) -> Sequence[Path]`、`collect_reference_uses(file, document) -> List[ReferenceUse]`、`visit_reference_use(use) -> Dict[str, str]`、`visit_uses(root)`、`visit_replacements(root)`、`visit_decisions(root)`、`visit_obligations(root)`、`visit_legacy_references(root)`。

**人工门禁:** Q01 与 Q22 的路径和职责获准；索引仍是确定性生成物，不得手改结论。

- [ ] **写入失败测试**

```python
import ast
import json
import pathlib
import unittest

from scripts.build_source_index import build_reference_index
from scripts.source_model import collect_reference_uses
from tests.source_governance_helpers import load_yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "source-governance" / "index-root"
EXPECTED = ROOT / "tests" / "fixtures" / "source-governance" / "index-expected.json"

def reference_key(row):
    return tuple(row[key] for key in
                 ("target_kind", "target_id", "reference_kind", "file", "record", "field_path"))

def formal_reference_set(root):
    del root
    return {reference_key(row) for row in json.loads(EXPECTED.read_text(encoding="utf-8"))}

def index_reference_set(entries):
    return {reference_key(row) for row in entries}

def reference_use_index_key(use):
    if use.kind == "basis":
        return ("source_entity", use.value["entity"], "basis.entity", use.file,
                use.record, use.field_path + ".entity")
    return ("source_use", use.value["registry"], f"{use.kind}.registry", use.file,
            use.record, use.field_path + ".registry")

class SourceIndexTests(unittest.TestCase):
    def entries(self, legacy=False):
        return build_reference_index(FIXTURE, include_legacy=legacy)["entries"]

    def test_index_covers_all_required_reference_kinds(self):
        kinds = {row["reference_kind"] for row in self.entries()}
        required = {"basis.entity", "source.registry", "match.registry", "use.entity",
                    "entity.replaced_by", "role.decision", "obligation.decisions",
                    "obligation.previous", "history.decision", "obligation.target"}
        self.assertTrue(required <= kinds)

    def test_every_reference_has_stable_record_and_field_path(self):
        self.assertTrue(all(row["record"] and row["field_path"] for row in self.entries()))

    def test_index_and_formal_references_are_bidirectionally_equal(self):
        self.assertEqual(formal_reference_set(FIXTURE), index_reference_set(self.entries()))

    def test_legacy_mode_includes_generator_and_array_inputs(self):
        kinds = {row["reference_kind"] for row in self.entries(legacy=True)}
        self.assertTrue({"legacy.basis", "legacy.source", "legacy.match", "legacy.array_source"} <= kinds)

    def test_two_runs_are_byte_identical(self):
        self.assertEqual(build_reference_index(FIXTURE), build_reference_index(FIXTURE))

    def test_future_terms_consumer_is_found_without_new_visitor(self):
        root = ROOT / "tests/fixtures/source-governance/future-consumer"
        entries = build_reference_index(root)["entries"]
        paths = {row["field_path"] for row in entries if row["file"] == "vocab/terms.yaml"}
        self.assertEqual({"concepts[0].basis[0].entity", "concepts[0].source.registry",
                          "concepts[0].match[0].registry",
                          "concepts[0].terms[0].basis[0].entity"}, paths)

    def test_isolated_local_analysis_is_not_a_source_reference(self):
        rows = [row for row in self.entries() if "local_analysis" in row["field_path"]]
        self.assertEqual([], rows)

    def test_external_group_is_indexed_as_structure_use(self):
        rows = [row for row in self.entries()
                if row["reference_kind"] == "external_group.registry"]
        self.assertEqual(24, len(rows))
        self.assertTrue(all(row["target_kind"] == "source_use" for row in rows))

    def test_index_shared_rows_equal_public_collector_rows(self):
        document_path = FIXTURE / "vocab/topics.yaml"
        uses = collect_reference_uses(pathlib.Path("vocab/topics.yaml"),
                                      load_yaml(document_path))
        expected = {reference_use_index_key(use) for use in uses}
        actual = {reference_key(row) for row in self.entries()
                  if row["reference_kind"] in {"basis.entity", "source.registry",
                                                "match.registry", "external_group.registry"}
                  and row["file"] == "vocab/topics.yaml"}
        self.assertEqual(expected, actual)

```

  `reference_use_index_key()` 是测试侧的直接 kind 映射：basis → source_entity／basis.entity／`.entity`，其他三类 → source_use／`<kind>.registry`／`.registry`。`index-expected.json` 由人逐行列出夹具中的全部正式引用，不能由生产索引生成；`index_reference_set()` 只读取生成条目。

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_source_index -v`

  Expected: FAIL，报告索引模块、通用访问器或未来消费者处理尚未实现。

- [ ] **实现索引生成**

```python
import json

import yaml

from scripts.source_model import collect_reference_uses

FORMAL_SUFFIXES = {".yaml", ".yml", ".json"}
EXCLUDED_PARTS = {"generated", "migrations", ".superpowers"}

def discover_formal_documents(root):
    return tuple(sorted(path for path in root.rglob("*")
                        if path.is_file() and path.suffix in FORMAL_SUFFIXES
                        and not EXCLUDED_PARTS.intersection(path.relative_to(root).parts)))

def visit_reference_use(use):
    if use.kind == "basis":
        return index_row("source_entity", use.value["entity"], "basis.entity",
                         use.file, use.record,
                         use.field_path + ".entity")
    return index_row("source_use", use.value["registry"], f"{use.kind}.registry",
                     use.file, use.record,
                     use.field_path + ".registry")

def index_row(target_kind, target_id, reference_kind, file, record, field_path):
    return {"target_kind": target_kind, "target_id": target_id,
            "reference_kind": reference_kind, "file": str(file),
            "record": record, "field_path": field_path}

def build_reference_index(root, include_legacy=False):
    entries = []
    for path in discover_formal_documents(root):
        document = load_yaml_or_json(path)
        relative = path.relative_to(root)
        entries.extend(visit_reference_use(use)
                       for use in collect_reference_uses(relative, document))
    entries.extend(visit_uses(root))
    entries.extend(visit_replacements(root))
    entries.extend(visit_decisions(root))
    entries.extend(visit_obligations(root))
    if include_legacy:
        entries.extend(visit_legacy_references(root))
    entries = unique_entries(entries)
    entries.sort(key=lambda row: tuple(row[key] for key in
                 ("target_kind", "target_id", "reference_kind", "file", "record", "field_path")))
    return {"schema": "urn:kb-design:data:source-reference-index", "schema_version": 1,
            "entries": entries}
```

  四个专用访问器按下列算法生成非共享键引用；没有空函数或按文件计数的替代实现。

```python
def visit_uses(root):
    document = load_yaml_or_json(root / "vocab/sources.yaml")
    rows = []
    for use_index, source_use in enumerate(document["sources"]):
        record = f"source_use:{source_use['id']}"
        rows.append(index_row("source_entity", source_use["entity"], "use.entity",
                              "vocab/sources.yaml", record,
                              f"sources[{use_index}].entity"))
        for role_index, role in enumerate(source_use["roles"]):
            if role.get("decision"):
                rows.append(index_row("decision", role["decision"], "role.decision",
                                      "vocab/sources.yaml", record,
                                      f"sources[{use_index}].roles[{role_index}].decision"))
    return rows

def visit_replacements(root):
    document = load_yaml_or_json(root / "vocab/entities.yaml")
    return [index_row("source_entity", entity["replaced_by"], "entity.replaced_by",
                      "vocab/entities.yaml", f"entity:{entity['id']}",
                      f"entities[{index}].replaced_by")
            for index, entity in enumerate(document["entities"])
            if entity.get("replaced_by")]

def visit_decisions(root):
    rows = []
    for path in sorted((root / "design/decisions").glob("source-*.md")):
        front = load_front_matter(path)
        record = f"decision:{front['id']}"
        for field_path, decision_id in walk_decision_ids(front):
            if decision_id != front["id"]:
                rows.append(index_row("decision", decision_id, "history.decision",
                                      str(path.relative_to(root)), record, field_path))
    return rows

def visit_obligations(root):
    document = load_yaml_or_json(root / "vocab/source-obligations.yaml")
    rows = []
    for index, obligation in enumerate(document["obligations"]):
        record = f"source_obligation:{obligation['id']}"
        for decision_index, decision in enumerate(obligation["decisions"]):
            rows.append(index_row("decision", decision, "obligation.decisions",
                                  "vocab/source-obligations.yaml", record,
                                  f"obligations[{index}].decisions[{decision_index}]"))
        if obligation.get("previous"):
            rows.append(index_row("source_obligation", obligation["previous"],
                                  "obligation.previous", "vocab/source-obligations.yaml",
                                  record, f"obligations[{index}].previous"))
        for target_index, target in enumerate(obligation["targets"]):
            rows.append(index_row(target["kind"], target_identity(target),
                                  "obligation.target", "vocab/source-obligations.yaml",
                                  record, f"obligations[{index}].targets[{target_index}]"))
    return rows
```

  共享键的递归、对象判据和字段路径只由 `scripts/source_model.py::_walk_reference_uses`、`_has_exact_keys` 与 `_format_reference_path` 实现；索引模块不得定义局部递归访问器。`walk_decision_ids()` 只访问字段名 `decision`、`decisions`、`supersedes` 和 history 内相同键；`target_identity()` 按 target.kind 返回稳定 ID。每个专用访问器返回完整 index row，不只返回计数。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_source_index -v`

  Expected: 9 项高风险测试通过；basis／source／match／external_group 的索引条目逐字等于 public collector 转换结果；未来术语夹具无需新增 visitor 即进入索引；隔离载体数组不产生来源引用。

- [ ] **运行迁移基线索引**

  Run: `python3 scripts/build_source_index.py --root . --include-legacy --output .superpowers/sdd/2026-08-31-source-schema-migration/baseline/source-reference-index.json`

  Expected: 记录七份词表中的 1,625 次来源引用、29 个被消费来源、756 条映射、692 条实际派生和 26 个数组来源；差异按身份逐项报告，不能只输出计数。

- [ ] **延后阶段回归**

  本任务只运行反向索引的定向 GREEN 与写集检查；完整回归并入迁移预演的工具链闭合门禁。

- [ ] **核对写集**

  Run: `git diff --name-only -- scripts/build_source_index.py tests/test_source_index.py tests/fixtures/source-governance/index-root vocab/generated/source-reference-index.json`

  Expected: 切换前不出现 `vocab/generated/source-reference-index.json`，其余只列本任务创建文件。

- [ ] **说明回滚**

  删除精确 ignored 基线目录即可撤销运行结果。代码提交被拒绝时，用 `apply_patch` 恢复本任务文件并创建新的 `[L2] revert: compensate source index task` 补偿提交；不删除决定或正式历史。

- [ ] **提交任务**

```bash
git add scripts/build_source_index.py tests/test_source_index.py tests/fixtures/source-governance/index-root tests/fixtures/source-governance/index-expected.json tests/fixtures/source-governance/future-consumer
git commit -m "[L2] feat: build source reverse-reference index"
```

### 只读探测

**Files:**

- Create: `scripts/probe_sources.py`
- Create: `tests/test_probe_sources.py`
- Create: `tests/fixtures/source-governance/probes/address-change.json`
- Create: `tests/fixtures/source-governance/probes/content-change.json`
- Create: `tests/fixtures/source-governance/probes/new-version.json`
- Create: `tests/fixtures/source-governance/probes/replacement.json`
- Create: `tests/fixtures/source-governance/probes/withdrawal.json`
- Create: `tests/fixtures/source-governance/probes/temporarily-unavailable.json`
- Create: `tests/fixtures/source-governance/probes/human-reproducible.json`
- Runtime write: `.superpowers/sdd/2026-08-31-source-schema-migration/probes/`

**Interfaces:**

- Consumes: `watch.cadence_months`、`urls` 角色、完整观察序列、前次摘要、Q08 与 Q09 的 accepted patches；测试只用固定 transport。
- Produces: `load_probe_endpoints(root, previous) -> Sequence[Dict[str, object]]`、`probe_repository(root, output_dir, transport, today, human_reproducible) -> Dict[str, object]`、`schedule_due(last_observed, cadence_months, today) -> bool`、`select_evidence(observations) -> Optional[Dict[str, object]]`、`evaluate_unavailability(observations, today, human_reproducible) -> bool`、`append_false_positive(path, observation_id, classified_at, reviewer, reason) -> Dict[str, object]`。

**人工门禁:** Q06、Q08、Q09 有 accepted patches。任一缺失时停止，不创建探测脚本、夹具或 ignored 观察。真实联网另需调用者显式传 `--live`；默认命令只接受 fixture transport。

- [ ] **写入失败测试**

```python
import hashlib
import json
import pathlib
import tempfile
import unittest
from datetime import date
from datetime import date, datetime, timezone

from scripts.probe_sources import (
    ALLOWED_METHODS, append_false_positive, evaluate_unavailability,
    classify_response, load_probe_endpoints, probe_due_endpoints, probe_repository,
    schedule_due, select_evidence,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "source-governance"

def load_response(path):
    return json.loads(path.read_text(encoding="utf-8"))

def fixed_transport(response):
    def request(method, url):
        if method not in ALLOWED_METHODS:
            raise ValueError(method)
        return dict(response, requested_url=url, requested_method=method)
    return request

def endpoint_transport(responses):
    def request(method, url):
        if method not in ALLOWED_METHODS:
            raise ValueError(method)
        return dict(responses[url], requested_url=url, requested_method=method)
    return request

def tree_hash(root):
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()

def failure_series(*dates):
    return [{"id": f"failure-{index}", "observed_at": value,
             "signal": "temporarily_unavailable", "available": False}
            for index, value in enumerate(dates, 1)]

def evidence_observation(role):
    return {"id": f"evidence-{role}", "observed_at": "2026-08-31",
            "role": role, "available": True}

def evidence_series(*roles):
    return [evidence_observation(role) for role in roles]

class ProbeSourcesTests(unittest.TestCase):
    def run_case(self, name):
        root = FIXTURES / "valid"
        response = load_response(FIXTURES / "probes" / name)
        with tempfile.TemporaryDirectory() as tmp:
            before = tree_hash(root)
            result = probe_repository(root, pathlib.Path(tmp), fixed_transport(response),
                                      date(2026, 8, 31), {})
            self.assertEqual(before, tree_hash(root))
            return result

    def test_address_change_only_requests_review(self):
        self.assertEqual("address_change", self.run_case("address-change.json")["signals"][0])

    def test_content_change_only_requests_review(self):
        self.assertEqual("content_change", self.run_case("content-change.json")["signals"][0])

    def test_new_version_only_requests_review(self):
        self.assertEqual("new_version", self.run_case("new-version.json")["signals"][0])

    def test_replacement_only_requests_review(self):
        self.assertEqual("replacement", self.run_case("replacement.json")["signals"][0])

    def test_withdrawal_signal_does_not_set_formal_status(self):
        self.assertNotIn("status", self.run_case("withdrawal.json"))

    def test_temporary_unavailability_does_not_block_release(self):
        self.assertFalse(self.run_case("temporarily-unavailable.json")["release_blocked"])

    def test_transport_allows_only_head_and_get(self):
        self.assertEqual({"HEAD", "GET"}, set(ALLOWED_METHODS))

    def test_probe_never_writes_formal_root(self):
        self.run_case("content-change.json")

    def test_monthly_and_quarterly_schedule_boundaries(self):
        self.assertTrue(schedule_due(date(2026, 7, 31), 1, date(2026, 8, 31)))
        self.assertFalse(schedule_due(date(2026, 6, 1), 3, date(2026, 8, 31)))
        self.assertTrue(schedule_due(date(2026, 5, 31), 3, date(2026, 8, 31)))

    def test_semiannual_and_annual_schedule_boundaries(self):
        self.assertTrue(schedule_due(date(2026, 2, 28), 6, date(2026, 8, 31)))
        self.assertTrue(schedule_due(date(2025, 8, 31), 12, date(2026, 8, 31)))

    def test_three_failures_under_fourteen_days_do_not_block(self):
        observations = failure_series("2026-08-18", "2026-08-24", "2026-08-30")
        self.assertFalse(evaluate_unavailability(observations, date(2026, 8, 31), False))

    def test_three_distinct_failures_spanning_fourteen_days_block_when_unreproducible(self):
        observations = failure_series("2026-08-17", "2026-08-24", "2026-08-31")
        self.assertTrue(evaluate_unavailability(observations, date(2026, 8, 31), False))

    def test_duplicate_day_is_not_an_independent_observation(self):
        observations = failure_series("2026-08-17", "2026-08-17", "2026-08-31")
        self.assertFalse(evaluate_unavailability(observations, date(2026, 8, 31), False))

    def test_evidence_priority_is_status_doi_archive_mirror(self):
        selected = select_evidence(evidence_series("mirror", "archive", "doi", "status"))
        self.assertEqual("status", selected["role"])

    def test_available_official_evidence_prevents_unavailability_block(self):
        observations = failure_series("2026-08-17", "2026-08-24", "2026-08-31")
        observations.append(evidence_observation("doi"))
        self.assertFalse(evaluate_unavailability(observations, date(2026, 8, 31), False))

    def test_url_roles_create_real_evidence_endpoints(self):
        endpoints = load_probe_endpoints(FIXTURES / "valid", [])
        evidence_roles = {row["role"] for row in endpoints if row["purpose"] == "evidence"}
        self.assertEqual({"status", "doi", "landing", "archive", "mirror"}, evidence_roles)

    def test_production_probe_selects_highest_priority_collected_evidence(self):
        root = FIXTURES / "valid"
        endpoints = load_probe_endpoints(root, [])
        responses = {row["locator"]: {"available": True, "status_code": 200}
                     for row in endpoints}
        with tempfile.TemporaryDirectory() as tmp:
            result = probe_repository(root, pathlib.Path(tmp), endpoint_transport(responses),
                                      date(2026, 8, 31), {})
        self.assertEqual("status", result["selected_evidence"]["z39-19"]["role"])

    def test_missing_publisher_version_does_not_signal_new_version(self):
        endpoint = {"locator": "https://example.test", "previous_version": "2005"}
        self.assertNotIn("new_version", classify_response(endpoint, {"available": True}))

    def test_equal_publisher_version_does_not_signal_new_version(self):
        endpoint = {"locator": "https://example.test", "previous_version": "2005"}
        response = {"available": True, "publisher_version": "2005"}
        self.assertNotIn("new_version", classify_response(endpoint, response))

    def test_explicit_different_publisher_version_signals_new_version(self):
        endpoint = {"locator": "https://example.test", "previous_version": "2005"}
        response = {"available": True, "publisher_version": "2010"}
        self.assertIn("new_version", classify_response(endpoint, response))

    def test_false_positive_is_appended_and_preserves_prior_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "observations.jsonl"
            path.write_text('{"id":"probe-1"}\n', encoding="utf-8")
            row = append_false_positive(path, "probe-1", "2026-08-31T12:00:00Z",
                                        "human", "dynamic navigation")
            self.assertEqual("false_positive", row["classification"])
            self.assertEqual(2, len(path.read_text(encoding="utf-8").splitlines()))

    def test_observation_sequence_links_previous_id(self):
        previous = [{"id": "probe-old", "entity": "z39-19",
                     "signal": "content_change", "observed_at": "2026-07-31"}]
        endpoint = {"entity": "z39-19", "locator": "https://example.test/z39",
                    "role": "status", "signal": "content_change",
                    "previous_version": "2005"}
        response = {"available": True, "content_changed": True,
                    "publisher_version": "2010"}
        rows = probe_due_endpoints([endpoint], previous, fixed_transport(response),
                                   date(2026, 8, 31))
        self.assertEqual("probe-old", rows[0]["previous"])
```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_probe_sources -v`

  Expected: FAIL，报告调度、观察窗口、证据排序或追加式误报接口尚未实现。

- [ ] **实现受限探测器**

```python
import hashlib
import json
import os
from datetime import date

import yaml

from scripts.source_model import add_calendar_months

ALLOWED_METHODS = frozenset(("HEAD", "GET"))
FORMAL_FIELDS = frozenset(("url", "urls", "version", "status", "review", "roles",
                           "basis", "source", "match"))
EVIDENCE_PRIORITY = {"status": 0, "doi": 1, "landing": 1, "archive": 2, "mirror": 3}
EVIDENCE_ROLES = frozenset(EVIDENCE_PRIORITY)

def parse_date(value):
    return date.fromisoformat(value[:10])

def load_observation_sequence(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]

def observation_id(entity, signal, endpoint, observed_at):
    identity = f"{entity}\t{signal}\t{endpoint}\t{observed_at}".encode("utf-8")
    return "probe-" + hashlib.sha256(identity).hexdigest()[:24]

def previous_observation_id(rows, entity, signal):
    matches = [row for row in rows if row.get("entity") == entity and row.get("signal") == signal]
    return matches[-1]["id"] if matches else None

def probe_due_endpoints(endpoints, previous, transport, today):
    rows = []
    for endpoint in sorted(endpoints, key=lambda row: (row["entity"], row["locator"])):
        response = transport("HEAD", endpoint["locator"])
        if response_requires_body(response):
            response = transport("GET", endpoint["locator"])
        if endpoint["purpose"] == "evidence":
            observed_at = today.isoformat()
            rows.append({"id": observation_id(endpoint["entity"], "evidence", endpoint["locator"],
                                               observed_at),
                         "observed_at": observed_at, "entity": endpoint["entity"],
                         "endpoint": endpoint["locator"], "role": endpoint["role"],
                         "signal": "evidence", "available": response.get("available", False),
                         "previous": previous_observation_id(previous + rows,
                                                             endpoint["entity"], "evidence"),
                         "response": sanitize_response(response)})
            continue
        for signal in classify_response(endpoint, response):
            if signal != endpoint["signal"]:
                continue
            observed_at = today.isoformat()
            row = {"id": observation_id(endpoint["entity"], signal, endpoint["locator"], observed_at),
                   "observed_at": observed_at, "entity": endpoint["entity"],
                   "endpoint": endpoint["locator"], "role": endpoint["role"],
                   "signal": signal, "available": response.get("available", False),
                   "previous": previous_observation_id(previous + rows, endpoint["entity"], signal),
                   "response": sanitize_response(response)}
            if signal == "content_change":
                row.update(content_fingerprint(endpoint, response))
            rows.append(row)
    return rows

def content_fingerprint(endpoint, response):
    if response.get("publisher_version"):
        return {"method": "publisher_version", "value": response["publisher_version"],
                "confidence": "high"}
    if response.get("locator_fragment"):
        normalized = " ".join(response["locator_fragment"].split())
        return {"method": "locator_fragment_sha256",
                "value": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
                "confidence": "medium"}
    normalized = " ".join(response.get("body", "").split())
    return {"method": "whole_page_sha256",
            "value": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
            "confidence": "low"}

def write_observations(output_dir, observations, summary):
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "observations.jsonl").open("a", encoding="utf-8") as stream:
        for row in observations:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8")

def response_requires_body(response):
    return response.get("available", False) and not (
        response.get("publisher_version") or response.get("locator_fragment")
        or response.get("withdrawal") or response.get("replacement"))

def classify_response(endpoint, response):
    signals = []
    if not response.get("available", False):
        return ["temporarily_unavailable"]
    if response.get("redirect") and response["redirect"] != endpoint["locator"]:
        signals.append("address_change")
    if response.get("content_changed"):
        signals.append("content_change")
    if ("publisher_version" in response
            and response["publisher_version"] != endpoint.get("previous_version")):
        signals.append("new_version")
    if response.get("replacement"):
        signals.append("replacement")
    if response.get("withdrawal"):
        signals.append("withdrawal")
    return signals

def sanitize_response(response):
    allowed = ("available", "status_code", "redirect", "etag", "last_modified",
               "publisher_version", "replacement", "withdrawal", "error")
    return {key: response[key] for key in allowed if key in response}

def hash_formal_tree(root):
    digest = hashlib.sha256()
    for directory in ("design", "scripts", "vocab"):
        for path in sorted((root / directory).rglob("*")):
            if path.is_file():
                digest.update(str(path.relative_to(root)).encode("utf-8"))
                digest.update(path.read_bytes())
    return digest.hexdigest()

def last_observed_date(previous, entity, signal):
    dates = [parse_date(row["observed_at"]) for row in previous
             if row.get("entity") == entity and row.get("signal") == signal]
    return max(dates) if dates else date(1970, 1, 1)

def unique_endpoints(rows):
    unique = {}
    for row in rows:
        key = (row["entity"], row["purpose"], row["role"], row["signal"], row["locator"])
        unique[key] = row
    return list(unique.values())

def load_probe_endpoints(root, previous):
    document = yaml.safe_load((root / "vocab/entities.yaml").read_text(encoding="utf-8"))
    rows = []
    for entity in document["entities"]:
        url_roles = {row["url"]: row["role"] for row in entity.get("urls", [])}
        for address in entity.get("urls", []):
            if address["role"] in EVIDENCE_ROLES:
                rows.append({"entity": entity["id"], "locator": address["url"],
                             "role": address["role"], "purpose": "evidence",
                             "signal": "evidence",
                             "last_observed": last_observed_date(previous, entity["id"],
                                                                  "evidence"),
                             "cadence_months": 1,
                             "previous_version": entity.get("version")})
        for watch in entity.get("watch", []):
            for signal in watch["signals"]:
                cadence_key = "content" if signal not in ("availability", "redirect") else signal
                rows.append({"entity": entity["id"], "locator": watch["locator"],
                             "role": url_roles.get(watch["locator"], "watch"),
                             "purpose": "signal", "signal": signal,
                             "last_observed": last_observed_date(previous, entity["id"], signal),
                             "cadence_months": watch["cadence_months"][cadence_key],
                             "previous_version": entity.get("version")})
    return sorted(unique_endpoints(rows),
                  key=lambda row: (row["entity"], row["purpose"], row["role"],
                                   row["signal"], row["locator"]))

def group_by_entity(observations):
    grouped = {}
    for row in observations:
        grouped.setdefault(row["entity"], []).append(row)
    return grouped

def summarize_observations(observations, today, human_reproducible):
    by_entity = group_by_entity(observations)
    blocked = sorted(entity for entity, rows in by_entity.items()
                     if evaluate_unavailability(rows, today,
                                                human_reproducible.get(entity, False)))
    return {"needs_review": sorted({row["entity"] for row in observations if row.get("signal")}),
            "release_blocked": bool(blocked), "blocked_entities": blocked,
            "selected_evidence": {entity: select_evidence(rows)
                                  for entity, rows in by_entity.items()
                                  if select_evidence(rows) is not None}}

def schedule_due(last_observed, cadence_months, today):
    return today >= add_calendar_months(last_observed, cadence_months)

def select_evidence(observations):
    candidates = [row for row in observations
                  if row.get("available") and row.get("role") in EVIDENCE_PRIORITY]
    return min(candidates, key=lambda row: (EVIDENCE_PRIORITY[row["role"]], row["observed_at"])) \
           if candidates else None

def evaluate_unavailability(observations, today, human_reproducible):
    failures = sorted({parse_date(row["observed_at"]) for row in observations
                       if row.get("signal") == "temporarily_unavailable"})
    spans_fourteen = len(failures) >= 3 and (failures[-1] - failures[0]).days >= 14
    return spans_fourteen and select_evidence(observations) is None and not human_reproducible

def append_false_positive(path, observation_id, classified_at, reviewer, reason):
    row = {"observation": observation_id, "classification": "false_positive",
           "classified_at": classified_at, "reviewer": reviewer, "reason": reason}
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    return row

def probe_repository(root, output_dir, transport, today, human_reproducible):
    before = hash_formal_tree(root)
    previous = load_observation_sequence(output_dir / "observations.jsonl")
    due = [endpoint for endpoint in load_probe_endpoints(root, previous)
           if schedule_due(endpoint["last_observed"], endpoint["cadence_months"], today)]
    observations = probe_due_endpoints(due, previous, transport, today)
    result = summarize_observations(previous + observations, today, human_reproducible)
    write_observations(output_dir, observations, result)
    if before != hash_formal_tree(root):
        raise RuntimeError("probe modified formal repository")
    if FORMAL_FIELDS.intersection(result):
        raise RuntimeError("probe result contains formal fields")
    return {"observations": previous + observations, **result}
```

  `probe_due_endpoints()` 为每项生成稳定 observation ID，`previous` 指向同实体同 signal 的最近一项；内容信号优先发布方版本元数据，其次 locator 片段规范化 SHA-256，整页摘要只标 `confidence: low`。网络实现拒绝认证参数、cookies、表单 body、PUT、POST、PATCH、DELETE 和自动接受远端状态变化；重定向最多 5 次，请求超时 20 秒。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_probe_sources -v`

  Expected: 22 项高风险测试通过；六类场景、五类 urls 证据 endpoint、生产证据选择、publisher_version 缺失／相同／不同边界、1／3／6／12 月调度、14 日三次独立观察、误报追加和 previous 链均通过，正式夹具哈希不变。

- [ ] **验证命令隔离**

  Run: `python3 scripts/probe_sources.py --root tests/fixtures/source-governance/valid --fixture-dir tests/fixtures/source-governance/probes --human-reproducible-file tests/fixtures/source-governance/probes/human-reproducible.json --output .superpowers/sdd/2026-08-31-source-schema-migration/probes/test-run`

  Expected: 只创建 `test-run/observations.jsonl` 与 `test-run/summary.json`，`git status --short` 不增加受跟踪文件。

- [ ] **延后阶段回归**

  本任务只运行探测隔离的定向 GREEN 与零正式写集检查；完整回归并入迁移预演的工具链闭合门禁。

- [ ] **核对写集**

  Run: `git diff --name-only -- scripts/probe_sources.py tests/test_probe_sources.py tests/fixtures/source-governance/probes vocab design`

  Expected: 只列脚本、测试和六个探测夹具；`vocab` 与 `design` 零写入。

- [ ] **说明回滚**

  未提交运行材料只删除精确 `test-run` 目录。代码提交被拒绝时，用 `apply_patch` 恢复本任务文件并创建新的 `[L2] revert: compensate source probe task` 补偿提交；探测观察不取得正式事实效力。

- [ ] **提交任务**

```bash
git add scripts/probe_sources.py tests/test_probe_sources.py tests/fixtures/source-governance/probes
git commit -m "[L2] feat: add isolated source probing"
```

### 迁移预演

**Files:**

- Create: `scripts/plan_source_migration.py`
- Create: `scripts/apply_source_migration.py`
- Create: `tests/test_source_migration.py`
- Create: `tests/fixtures/source-governance/decisions/`
- Create: `tests/fixtures/source-governance/replacement-decisions/`
- Create: `tests/fixtures/source-governance/missing-decisions/`
- Create: `tests/fixtures/source-governance/duplicate-field-decisions/`
- Create: `tests/fixtures/source-governance/wrong-field-decisions/`
- Create: `tests/fixtures/source-governance/wrong-domain-decisions/`
- Create: `tests/fixtures/source-governance/blocked-plan/`
- Create: `tests/fixtures/source-governance/candidate-input/`
- Create: `tests/fixtures/source-governance/candidate-plan/`
- Runtime write: `.superpowers/sdd/2026-08-31-source-schema-migration/candidate/`
- Runtime write: `.superpowers/sdd/2026-08-31-source-schema-migration/snapshots/`

**Interfaces:**

- Consumes: 18 个哈希锁定输入、25 项批准决定、现行仓库和六份迁移 schema。
- Produces: `build_migration_plan(root: Path, inventory_dir: Path, decision_dir: Path) -> Dict[str, object]` 与 `apply_migration(root: Path, plan_dir: Path, output_root: Path) -> ApplyResult`；正式根目录永远不是 `output_root`。
- Internal: `verify_frozen_hashes()`、`load_inventory_rows()`、`load_decision_patches()`、`build_base_rows()`、`materialize_decision_patches()`、`validate_patch_ownership()`、`validate_q_coverage()`、`validate_identity_coverage()`、`load_and_validate_ledgers()`、`apply_row()`、`write_candidate_tree()`。

**人工门禁:** Q01 至 Q25 均有 accepted patches；未回答、重复或冲突立即停止，输出路径不得创建。

- [ ] **写入失败测试**

```python
import hashlib
import json
import pathlib
import tempfile
import unittest
from datetime import date

from scripts.plan_source_migration import build_migration_plan
from scripts.apply_source_migration import apply_migration
from tests.source_governance_helpers import load_yaml
from scripts.source_model import (
    ApplyResult, DecisionPatch, compute_next_due, load_decision_patches,
)
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
INPUT = ROOT / ".superpowers" / "sdd" / "2026-08-31-governance-implementation-prep"
FIXTURES = ROOT / "tests" / "fixtures" / "source-governance"
DECISIONS = FIXTURES / "decisions"
BLOCKED_PLAN = FIXTURES / "blocked-plan"
REPLACEMENT = FIXTURES / "replacement-decisions"
ACTUAL_DECISIONS = ROOT / "design" / "decisions"

def load_ledger(path, section):
    document = load_yaml(path)
    if section == "roles":
        return document["roles"]
    return [row for row in document["rows"] if row["class"] == section]

def all_plan_rows(plan):
    return [row for name in sorted(plan["ledgers"]) for row in plan["ledgers"][name]["rows"]]

def value_sha256(value):
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def patches(directory, qids=None):
    rows = load_decision_patches(sorted(directory.glob("source-*.md")))
    return [row for row in rows if qids is None or row.qid in set(qids)]

def expected_patch_signatures(directory, qids=None):
    return sorted((row.qid, row.identity, row.field, value_sha256(row.value))
                  for row in patches(directory, qids))

def actual_patch_signatures(plan, qids=None):
    accepted = None if qids is None else set(qids)
    signatures = []
    for row in all_plan_rows(plan):
        for trace in row["decision_trace"]:
            if accepted is None or trace["qid"] in accepted:
                signatures.append((trace["qid"], row["identity"], trace["field"],
                                   trace["value_sha256"]))
    for identity, control in plan["controls"].items():
        for trace in control["decision_trace"]:
            if accepted is None or trace["qid"] in accepted:
                signatures.append((trace["qid"], identity, trace["field"],
                                   trace["value_sha256"]))
    return sorted(signatures)

def assert_q_patches_consumed(testcase, qids, plan, directory=ACTUAL_DECISIONS):
    testcase.assertEqual(expected_patch_signatures(directory, qids),
                         actual_patch_signatures(plan, qids))

def rows_touched_by_q(plan, qid):
    return [row for row in all_plan_rows(plan)
            if any(trace["qid"] == qid for trace in row["decision_trace"])]

def fixture_plan(directory):
    return build_migration_plan(ROOT, INPUT, directory)

def actual_plan():
    return build_migration_plan(ROOT, INPUT, ACTUAL_DECISIONS)

def decision_is_accepted(decision_id):
    for path in ACTUAL_DECISIONS.glob("source-*.md"):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        front = yaml.safe_load(text.split("---\n", 2)[1])
        if front.get("id") == decision_id:
            return front.get("status") == "accepted"
    return False

class SourceMigrationTests(unittest.TestCase):
    def plan(self):
        return build_migration_plan(ROOT, INPUT, DECISIONS)

    def test_all_eighteen_input_hashes_are_verified(self):
        self.assertEqual(18, self.plan()["verified_hash_count"])

    def test_frozen_identity_counts_are_exact(self):
        counts = self.plan()["counts"]
        self.assertEqual({"entities": 138, "uses": 47, "basis": 1501,
                          "source": 726, "match": 756, "origin": 19}, counts)

    def test_entity_inventory_keeps_31_and_107_separate(self):
        self.assertEqual((31, 107), tuple(self.plan()["entity_partitions"]))

    def test_source_inventory_keeps_692_24_8_2_separate(self):
        self.assertEqual((692, 24, 8, 2), tuple(self.plan()["source_partitions"]))

    def test_identity_ambiguities_are_not_merged(self):
        self.assertEqual(16, self.plan()["blocked_identity_ambiguities"])

    def test_blocked_decision_patches_prevent_any_candidate_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = pathlib.Path(tmp) / "candidate"
            result = apply_migration(ROOT, BLOCKED_PLAN, output)
            self.assertTrue(result.blocked)
            self.assertFalse(output.exists())

    def test_missing_decision_stops_before_output_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "SOURCE_DECISION_DELIVERY_MISSING"):
                build_migration_plan(ROOT, INPUT, FIXTURES / "missing-decisions")
            self.assertEqual([], list(pathlib.Path(tmp).iterdir()))

    def test_recommended_patches_are_consumed_once(self):
        plan = build_migration_plan(ROOT, INPUT, DECISIONS)
        self.assertEqual(expected_patch_signatures(DECISIONS), actual_patch_signatures(plan))

    def test_replacement_patches_rebuild_fields_without_duplicate_rows(self):
        plan = build_migration_plan(ROOT, INPUT, REPLACEMENT)
        self.assertEqual(expected_patch_signatures(REPLACEMENT), actual_patch_signatures(plan))
        self.assertEqual(3187, len(all_plan_rows(plan)))
        self.assertNotEqual(actual_patch_signatures(self.plan()), actual_patch_signatures(plan))

    def test_duplicate_identity_field_patch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "SOURCE_DECISION_PATCH_CONFLICT"):
            build_migration_plan(ROOT, INPUT, FIXTURES / "duplicate-field-decisions")

    def test_q_field_ownership_violation_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "SOURCE_DECISION_PATCH_CONFLICT"):
            build_migration_plan(ROOT, INPUT, FIXTURES / "wrong-field-decisions")

    def test_q_identity_domain_violation_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "SOURCE_DECISION_PATCH_CONFLICT"):
            build_migration_plan(ROOT, INPUT, FIXTURES / "wrong-domain-decisions")

    def test_all_qids_are_covered_by_patches(self):
        qids = {signature[0] for signature in actual_patch_signatures(self.plan())}
        self.assertEqual({f"Q{number:02d}" for number in range(1, 26)}, qids)

    def test_plan_is_deterministic(self):
        self.assertEqual(self.plan(), self.plan())

    def test_apply_rejects_output_inside_formal_root(self):
        with self.assertRaises(ValueError):
            apply_migration(ROOT, BLOCKED_PLAN, ROOT / "vocab")

    def test_apply_returns_one_apply_result_and_uses_absent_child_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = pathlib.Path(tmp) / "candidate"
            result = apply_migration(FIXTURES / "candidate-input",
                                     FIXTURES / "candidate-plan", output)
            self.assertIsInstance(result, ApplyResult)
            self.assertTrue(output.is_dir())
            self.assertTrue(all(isinstance(path, str) for path in result.written))
```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_source_migration -v`

  Expected: FAIL，报告 DecisionPatch 所有权、重复字段、Q 覆盖、候选应用或单层 ApplyResult 尚未实现。

- [ ] **实现确定性预演**

```python
INVENTORIES = (
    "source-entities.tsv", "source-roles.tsv", "basis-inventory.tsv",
    "source-inventory.tsv", "match-inventory.tsv", "origin-inventory.tsv",
)
EXPECTED_COUNTS = {"entities": 138, "uses": 47, "basis": 1501,
                   "source": 726, "match": 756, "origin": 19}

def build_migration_plan(root, inventory_dir, decision_dir):
    verify_frozen_hashes(inventory_dir)
    inventories = load_inventory_rows(inventory_dir, INVENTORIES)
    assert_inventory_counts(inventories, EXPECTED_COUNTS)
    base_rows = build_base_rows(inventories)
    patches = load_decision_patches(sorted(decision_dir.glob("source-*.md")))
    final_rows, controls = materialize_decision_patches(base_rows, patches)
    validate_identity_coverage(base_rows, final_rows)
    validate_q_coverage(base_rows, controls, patches)
    return summarize_ledgers(final_rows, controls, verified_hash_count=18)

def apply_migration(root, plan_dir, output_root):
    if output_root == root or root in output_root.parents:
        raise ValueError("output_root must be outside formal root")
    plan = load_and_validate_ledgers(plan_dir)
    return write_candidate_tree(root, plan, output_root)
```

  `load_inventory_rows()` 逐个读取六份九列 TSV，拒绝空单元格、重复 identity、非法状态和计数差异。`build_base_rows()` 为每个 inventory identity 建立唯一行，保存 ledger、class、old_file、old_record、field_path、old_value、冻结哈希、`decision_domains`、默认 `operation: keep`、`disposition: retain_legacy`、`new_value` 等于 old_value、`blocks_cutover: true` 和空 `decision_trace`。控制 identity 不进入 base rows。

```python
def deep_set(target, field, value):
    parts = field.split(".")
    current = target
    for part in parts[:-1]:
        nested = current.setdefault(part, {})
        if not isinstance(nested, dict):
            raise ValueError(f"SOURCE_DECISION_PATCH_CONFLICT non-object field {field}")
        current = nested
    current[parts[-1]] = value

def materialize_decision_patches(base_rows, patches):
    final_rows = {identity: deepcopy(row) for identity, row in base_rows.items()}
    controls = {}
    seen = set()
    for patch in sorted(patches, key=lambda row: (row.qid, row.identity, row.field)):
        key = (patch.identity, patch.field)
        if key in seen:
            raise ValueError(f"SOURCE_DECISION_PATCH_CONFLICT {key}")
        seen.add(key)
        validate_patch_ownership(final_rows, patch)
        target = (controls.setdefault(patch.identity, {"decision_trace": []})
                  if patch.identity.startswith("@control:") else final_rows[patch.identity])
        deep_set(target, patch.field, deepcopy(patch.value))
        target["decision_trace"].append({"qid": patch.qid, "field": patch.field,
                                         "value_sha256": decision_patch_sha256(patch)})
    validate_final_rows(final_rows)
    return final_rows, controls

def validate_patch_ownership(final_rows, patch):
    ownership = Q_FIELD_OWNERSHIP.get(patch.qid)
    if ownership is None or patch.field not in ownership:
        raise ValueError(f"SOURCE_DECISION_PATCH_CONFLICT {patch.qid} {patch.field}")
    if patch.identity.startswith("@control:"):
        if patch.identity not in Q_CONTROL_IDENTITIES.get(patch.qid, frozenset()):
            raise ValueError(f"SOURCE_DECISION_PATCH_CONFLICT {patch.qid} {patch.identity}")
        return
    row = final_rows.get(patch.identity)
    if row is None or patch.qid not in row["decision_domains"]:
        raise ValueError(f"SOURCE_DECISION_PATCH_CONFLICT {patch.qid} {patch.identity}")
```

  `Q_FIELD_OWNERSHIP` 与 `Q_CONTROL_IDENTITIES` 逐字来自“决定输入”矩阵。`assign_decision_domains()` 使用冻结 identity 集合定义互斥域：Q11 排除 Q12 的 17 个特殊角色；Q13 排除 Q14 的 3 行、Q15 的 24 行、Q16 的 2 行和 Q17 的 4 行；Q18 排除 Q17 match；Q19 排除 Q20 的 643 行。`validate_q_coverage()` 要求 Q01–Q25 各至少一项 patch，并要求每个域 identity 的 required fields 都有对应 qid trace。`validate_identity_coverage()` 要求最终 3,187 行 identity 与 base rows 完全相等且无重复；`load_and_validate_ledgers()` 要求六份文件、正确 schema、各自冻结计数和总计 3,187。

  `write_candidate_tree()` 只有在阻断数为 0 时才创建 output_root：先复制受影响正式文件；按 `(file, record, field_path, identity)` 排序应用行；`apply_row()` 在修改前断言旧值逐字相等，`keep` 不写、`set` 精确替换、`delete` 只删除获准叶值、`isolate` 把 Q16 两数组的旧 source 字符串移入 `local_analysis` 对象；任何前置值不符时删除未完成 candidate 目录并失败。写完重新加载全部 YAML／JSON，运行七份 schema、`validate_repository()`、索引双向检查和生成确定性，再返回排序写集。

```python
PATH_TOKEN = re.compile(r"([A-Za-z_][A-Za-z0-9_-]*)|\[(\d+)\]")

def parse_field_path(value):
    tokens = []
    for key, index in PATH_TOKEN.findall(value):
        tokens.append(int(index) if index else key)
    if not tokens:
        raise ValueError(f"invalid field path: {value}")
    return tokens

def locate_parent(document, field_path):
    tokens = parse_field_path(field_path)
    current = document
    for token in tokens[:-1]:
        current = current[token]
    return current, tokens[-1]

def apply_row(document, row):
    parent, key = locate_parent(document, row["field_path"])
    actual = parent[key]
    if actual != row["old_value"]:
        raise ValueError(f"old value mismatch: {row['identity']}")
    if row["operation"] == "keep":
        return False
    if row["operation"] == "set":
        parent[key] = deepcopy(row["new_value"])
    elif row["operation"] == "delete":
        del parent[key]
    elif row["operation"] == "isolate":
        if not isinstance(actual, str):
            raise ValueError(f"isolate expects scalar: {row['identity']}")
        del parent[key]
        parent["local_analysis"] = deepcopy(row["new_value"])
    else:
        raise ValueError(f"unknown operation: {row['operation']}")
    return True

def write_candidate_tree(root, plan, output_root):
    blockers = [row["identity"] for row in plan["rows"] if row["blocks_cutover"]]
    if blockers:
        return ApplyResult((), tuple(sorted(blockers)))
    if output_root.exists() or root == output_root or root in output_root.parents:
        raise ValueError("candidate output must be absent and outside formal root")
    temporary = output_root.with_name(output_root.name + ".building")
    if temporary.exists():
        shutil.rmtree(temporary)
    try:
        shutil.copytree(root, temporary,
                        ignore=shutil.ignore_patterns(".git", ".superpowers", "__pycache__"))
        changed = set()
        grouped = group_rows_by_file(plan["rows"])
        for relative, rows in sorted(grouped.items()):
            path = temporary / relative
            document = load_yaml_or_json(path)
            for row in sorted(rows, key=lambda item: (item["record"], item["field_path"],
                                                       item["identity"])):
                if apply_row(document, row):
                    changed.add(relative)
            write_yaml_or_json(path, document)
        apply_approved_file_rewrites(temporary, plan["file_rewrites"], changed)
        run_candidate_validations(temporary)
        temporary.rename(output_root)
        return ApplyResult(tuple(sorted(changed)), ())
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
```

  `group_rows_by_file()` 拒绝非正式相对路径和同一 field_path 的多行；`write_yaml_or_json()` 对 JSON 使用排序键和两空格缩进，对 YAML 使用 `sort_keys=False`；`apply_approved_file_rewrites()` 只消费 accepted patches 组合出的完整旧文件 SHA-256 与完整新文件内容；`run_candidate_validations()` 依次运行七份 schema、`validate_repository()`、索引双向相等、主题双构建和写集比较，任一失败使 `.building` 被删除且 output_root 不存在。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_source_migration -v`

  Expected: 16 项高风险测试通过；推荐与 replacement patches 分别物化最终字段；重复 identity／field、字段越权和 identity 域越权被拒绝；25 个 Q 全覆盖；缺决定零输出；阻断计划零 candidate 写入；零阻断计划返回单层 ApplyResult。

- [ ] **运行真实只读预演**

  Run: `python3 scripts/plan_source_migration.py --root . --inventory-dir .superpowers/sdd/2026-08-31-governance-implementation-prep --decision-dir design/decisions --output .superpowers/sdd/2026-08-31-source-schema-migration/plan`

  Expected: 18 个哈希、25 个 accepted Q、3,187 个 identity 和六类冻结计数通过；输出每行最终字段、decision_trace、阻断和候选写集；正式 Git 差异不变。

- [ ] **运行工具链闭合回归**

  Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v && python3 scripts/check-topics.py && python3 scripts/check_link_baseline.py && git diff --check`

  Expected: 全部测试通过；链接基线零退出；差异检查继续运行并通过。

- [ ] **核对写集**

  Run: `git diff --name-only -- scripts/plan_source_migration.py scripts/apply_source_migration.py tests/test_source_migration.py tests/fixtures/source-governance/decisions vocab design`

  Expected: 只列两个脚本、测试和决定夹具；`vocab` 与 `design` 零写入。

- [ ] **说明回滚**

  未提交候选只删除精确 `.superpowers/sdd/2026-08-31-source-schema-migration/plan`。代码提交被拒绝时，用 `apply_patch` 恢复本任务文件并创建新的 `[L2] revert: compensate source migration planner task` 补偿提交；不删除决定 patches 或 decision_trace 证据。

- [ ] **提交任务**

```bash
git add scripts/plan_source_migration.py scripts/apply_source_migration.py tests/test_source_migration.py tests/fixtures/source-governance/decisions tests/fixtures/source-governance/replacement-decisions tests/fixtures/source-governance/blocked-plan tests/fixtures/source-governance/candidate-input tests/fixtures/source-governance/candidate-plan
git commit -m "[L2] feat: add source migration dry run"
```

### 现行实体

**Files:**

- Create: `vocab/migrations/source-v1/entities.yaml`
- Modify: `tests/test_source_migration.py`
- Create after human decision: `design/decisions/source-identity-boundaries.md`

**Interfaces:**

- Consumes: 31 个 `vocab/entities.yaml` 现行来源身份、Q03 至 Q10 的获准决定、`decision-source-0002`。
- Produces: `entities.yaml` 账本中 31 个 `existing` 行；每行保存冻结身份、旧路径、旧哈希、拟议记录、依据、决定、阻断和回滚键。

**人工门禁:** `decision-source-0002` 必须逐项给出 31 个外部状态、依据定位、地址结构和 `replaced_by`。缺一项即停止，不生成账本。

- [ ] **扩充失败测试**

```python
def test_existing_entity_ids_are_frozen(self):
    rows = load_ledger(ROOT / "vocab/migrations/source-v1/entities.yaml", "existing")
    self.assertEqual(31, len(rows))
    self.assertTrue(all(row["old_id"] == row["proposed_id"] for row in rows))

def test_q10_replacement_can_materialize_resolved_statuses(self):
    rows = rows_touched_by_q(fixture_plan(REPLACEMENT), "Q10")
    self.assertTrue(any(row["disposition"] == "register" and
                        not row["blocks_cutover"] for row in rows))

def test_existing_entity_ledger_preserves_old_record_hashes(self):
    rows = load_ledger(ROOT / "vocab/migrations/source-v1/entities.yaml", "existing")
    self.assertTrue(all(len(row["old_record_sha256"]) == 64 for row in rows))

def test_existing_entity_review_and_watch_values_consume_q07_to_q09(self):
    plan = actual_plan()
    assert_q_patches_consumed(self, ("Q07", "Q08", "Q09"), plan)
    rows = load_ledger(ROOT / "vocab/migrations/source-v1/entities.yaml", "existing")
    for row in rows:
        review = row.get("new_value", {}).get("review")
        if review and review["checked"] is not None:
            self.assertEqual(review["next_due"],
                             compute_next_due(date.fromisoformat(review["checked"]),
                                              review["interval_months"]).isoformat())
```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_source_migration.SourceMigrationTests.test_existing_entity_ids_are_frozen tests.test_source_migration.SourceMigrationTests.test_q10_replacement_can_materialize_resolved_statuses tests.test_source_migration.SourceMigrationTests.test_existing_entity_ledger_preserves_old_record_hashes tests.test_source_migration.SourceMigrationTests.test_existing_entity_review_and_watch_values_consume_q07_to_q09 -v`

  Expected: FAIL，报告账本不存在或 31 行未生成。

- [ ] **生成最小账本**

  Run: `python3 scripts/plan_source_migration.py --root . --inventory-dir .superpowers/sdd/2026-08-31-governance-implementation-prep --decision-dir design/decisions --section existing-entities --ledger vocab/migrations/source-v1/entities.yaml`

  每行使用下列结构；31 行按冻结 TSV 顺序生成，不按名称重排。

```yaml
- identity: source-entities.tsv:2
  class: existing
  old_file: vocab/entities.yaml
  old_record: entity:gbt-13745
  old_id: gbt-13745
  proposed_id: gbt-13745
  old_record_sha256: e90028f90c50a50802611bb49dd2503e34ee0859de66f9838b4592a4b6b1a076
  operation: keep
  disposition: unresolved_external_status
  new_value: null
  decision: decision-source-0002
  decision_trace:
    - { qid: Q10, field: operation, value_sha256: 0fc9e981262ade8d19676d1ee3a1d34733be1c113a52e6c07980ffc200e2e37d }
    - { qid: Q10, field: disposition, value_sha256: 6e3f92c81107200e4ec2fca86f20503b3bc74537c4bd89a15fca09e118f0d68b }
    - { qid: Q10, field: new_value, value_sha256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b }
    - { qid: Q10, field: blocks_cutover, value_sha256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b }
  tier_change: none
  decisions: [decision-source-0002]
  blocks_cutover: true
  rollback_key: entity:gbt-13745
```

  `old_record_sha256` 使用 `yaml.safe_dump(record, sort_keys=True, allow_unicode=True)` 的 UTF-8 字节计算。四个 trace 哈希分别对补丁 value 的排序键紧凑 JSON UTF-8 字节计算；真实账本使用同一算法。Q10 required fields 未完整覆盖 31 行时命令失败且不写文件。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_source_migration -v`

  Expected: 本任务 4 项高风险测试通过；推荐 patch fixture 保持阻断，replacement patch fixture 可形成非阻断行；旧 ID、旧记录哈希和复核语义保持。

- [ ] **延后阶段回归**

  本任务只运行现行实体的定向 GREEN 与写集检查；完整回归并入文档分流的迁移账本闭合门禁。

- [ ] **核对写集**

  Run: `git diff --name-only -- vocab/migrations/source-v1/entities.yaml tests/test_source_migration.py vocab/entities.yaml design/decisions/source-identity-boundaries.md`

  Expected: Q10 采用推荐时只列迁移账本与测试；人的正式决定存在时另列精确决定文件；不列 `vocab/entities.yaml`。

- [ ] **说明回滚**

  账本提交被拒绝时，用 `apply_patch` 恢复账本与测试并创建新的 `[L2] revert: compensate existing source entity ledger` 补偿提交；`decision-source-0002` 与 decision_trace 保留可查询。

- [ ] **提交任务**

```bash
git add vocab/migrations/source-v1/entities.yaml tests/test_source_migration.py
git commit -m "[L2] data: record existing source entity migration"
```

### 新增身份

**Files:**

- Modify: `vocab/migrations/source-v1/entities.yaml`
- Modify: `tests/test_source_migration.py`
- Read: `.superpowers/sdd/2026-08-31-governance-implementation-prep/source-entities.tsv`

**Interfaces:**

- Consumes: 107 个未登记身份、16 个身份歧义、Q03 至 Q06 的获准判据与重点结论。
- Produces: 107 个 `unregistered` 账本行；处置只取 `register`、`merge_address`、`merge_locator`、`retain_legacy` 或阻断值。

**人工门禁:** 每个 `register` 行须有人的独立实体结论和获准 `id`；每个 merge 行须指出目标实体与地址／定位角色。没有逐字段 accepted patches 时停止，不生成账本。

- [ ] **扩充失败测试**

```python
def test_unregistered_inventory_has_exactly_107_rows(self):
    rows = load_ledger(ROOT / "vocab/migrations/source-v1/entities.yaml", "unregistered")
    self.assertEqual(107, len(rows))

def test_sixteen_identity_ambiguities_remain_explicit(self):
    rows = load_ledger(ROOT / "vocab/migrations/source-v1/entities.yaml", "unregistered")
    self.assertEqual(16, sum(row["identity_ambiguous"] for row in rows))

def test_no_new_id_exists_without_register_disposition(self):
    rows = load_ledger(ROOT / "vocab/migrations/source-v1/entities.yaml", "unregistered")
    self.assertTrue(all((row.get("proposed_id") is not None) ==
                        (row["disposition"] == "register") for row in rows))
```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_source_migration.SourceMigrationTests.test_unregistered_inventory_has_exactly_107_rows tests.test_source_migration.SourceMigrationTests.test_sixteen_identity_ambiguities_remain_explicit tests.test_source_migration.SourceMigrationTests.test_no_new_id_exists_without_register_disposition -v`

  Expected: FAIL，现有账本只有 31 个 existing 行。

- [ ] **追加未登记账本**

  Run: `python3 scripts/plan_source_migration.py --root . --inventory-dir .superpowers/sdd/2026-08-31-governance-implementation-prep --decision-dir design/decisions --section unregistered-entities --ledger vocab/migrations/source-v1/entities.yaml`

  生成器从 Q03 至 Q06 patches 按 identity／field 写入 107 个 base row。Q05 推荐被 accepted 时应用推荐 patches；replacement 被 accepted 时应用 replacement patches；代码中不保存 `rfc-http`、DITA、LOM 或 BCP 47 的固定结果。Q05 未覆盖的 required fields 使命令在写文件前失败。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_source_migration -v`

  Expected: 本任务 3 项高风险测试通过；账本共 138 行，31 与 107 分区不混合；16 个歧义保持，未批准身份不生成新 ID。

- [ ] **延后阶段回归**

  本任务只运行新增身份的定向 GREEN 与写集检查；完整回归并入文档分流的迁移账本闭合门禁。

- [ ] **核对写集**

  Run: `git diff --name-only -- vocab/migrations/source-v1/entities.yaml tests/test_source_migration.py vocab/entities.yaml`

  Expected: 只列账本与测试，不列 `vocab/entities.yaml`。

- [ ] **说明回滚**

  提交被拒绝时，用 `apply_patch` 恢复本批账本与测试并创建新的 `[L2] revert: compensate new source identity ledger` 补偿提交；`decision-source-0002`、已分配 ID 与 decision_trace 保留。

- [ ] **提交任务**

```bash
git add vocab/migrations/source-v1/entities.yaml tests/test_source_migration.py
git commit -m "[L2] data: classify unregistered source identities"
```

### 用途角色

**Files:**

- Create: `vocab/migrations/source-v1/uses.yaml`
- Modify: `tests/test_source_migration.py`
- Create after human decision: `design/decisions/source-role-uses.md`

**Interfaces:**

- Consumes: 47 个角色、实际消费者、Q11 与 Q12 的获准结论、`decision-source-0003`。
- Produces: 47 行逐角色账本；同名 `proposed` 行由获准类别规则确定性生成，`approved` 或 `retired` 行独立保存角色决定和历史动作。

**人工门禁:** `decision-source-0003` 批准“现行角色无损登记为同名 `proposed`、`decision: null`”的类别规则，并逐项列出任何 `approved` 或 `retired` 角色及其决定引用。保持 `proposed` 的行不再要求重复人工签字；缺少批准或退役决定时只阻断对应效力变化。

- [ ] **扩充失败测试**

```python
def test_role_ledger_has_exactly_47_rows(self):
    rows = load_ledger(ROOT / "vocab/migrations/source-v1/uses.yaml", "roles")
    self.assertEqual(47, len(rows))

def test_role_inventory_preserves_five_candidate_and_eleven_unused_mapping_identities(self):
    rows = load_ledger(ROOT / "vocab/migrations/source-v1/uses.yaml", "roles")
    self.assertEqual(5, sum(row["old_role"] == "candidate" for row in rows))
    self.assertEqual(11, sum(row["old_role"] == "mapping" and not row["consumers"]
                             for row in rows))

def test_approved_and_retired_roles_have_accepted_decision(self):
    rows = load_ledger(ROOT / "vocab/migrations/source-v1/uses.yaml", "roles")
    decided = [row for row in rows if row["new_status"] in ("approved", "retired")]
    self.assertTrue(all(row["decision"] and decision_is_accepted(row["decision"])
                        for row in decided))

def test_replacement_patches_can_approve_roles(self):
    rows = rows_touched_by_q(fixture_plan(REPLACEMENT), "Q11")
    self.assertTrue(any(row["new_status"] == "approved" and
                        not row["blocks_cutover"] for row in rows))
```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_source_migration.SourceMigrationTests.test_role_ledger_has_exactly_47_rows tests.test_source_migration.SourceMigrationTests.test_role_inventory_preserves_five_candidate_and_eleven_unused_mapping_identities tests.test_source_migration.SourceMigrationTests.test_approved_and_retired_roles_have_accepted_decision tests.test_source_migration.SourceMigrationTests.test_replacement_patches_can_approve_roles -v`

  Expected: FAIL，`uses.yaml` 不存在。

- [ ] **生成角色账本**

  Run: `python3 scripts/plan_source_migration.py --root . --inventory-dir .superpowers/sdd/2026-08-31-governance-implementation-prep --decision-dir design/decisions --section uses --ledger vocab/migrations/source-v1/uses.yaml`

  账本逐角色而不是逐来源汇总。每行固定保存 inventory identity、use ID、entity、old role、消费者路径、new role、new status、角色决定、operation、disposition、decision_trace 与 blocks_cutover。获准类别规则为保持现状的行生成同名 `proposed`；只有 `approved`、`retired` 或角色改名由 Q11／Q12 identity／field patches 写入。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_source_migration -v`

  Expected: 本任务 4 项高风险测试通过；47 行一一对应；推荐 patch fixture 保持 proposed，replacement patch fixture 可批准角色且带 accepted 决定。

- [ ] **延后阶段回归**

  本任务只运行用途角色的定向 GREEN 与写集检查；完整回归并入文档分流的迁移账本闭合门禁。

- [ ] **核对写集**

  Run: `git diff --name-only -- vocab/migrations/source-v1/uses.yaml tests/test_source_migration.py vocab/sources.yaml design/decisions/source-role-uses.md`

  Expected: 推荐获准时只列迁移账本与测试；不列 `vocab/sources.yaml`。

- [ ] **说明回滚**

  提交被拒绝时，用 `apply_patch` 恢复账本与测试并创建新的 `[L2] revert: compensate source role ledger` 补偿提交；角色决定和 decision_trace 保留。

- [ ] **提交任务**

```bash
git add vocab/migrations/source-v1/uses.yaml tests/test_source_migration.py
git commit -m "[L2] data: record source role migration"
```

### 逐值依据

**Files:**

- Create: `vocab/migrations/source-v1/basis.yaml`
- Modify: `tests/test_source_migration.py`
- Create: `tests/test_build_topics_sources.py`
- Read: `vocab/topics.yaml`
- Read: `vocab/entities.yaml`
- Read: `vocab/forms.yaml`
- Read: `vocab/build/extra-arrays.json`
- Read: `design/maintenance.md`
- Read: `design/topics.md`

**Interfaces:**

- Consumes: 1,501 个库存行、Q13、Q18、Q19、Q20 的获准规则、来源实体解析结果。
- Produces: 1,501 行账本；正式数据 1,496 行、生成配置 1 行、文档展示 4 行分别对账；候选树夹具不含伪造 `basis`。

**人工门禁:** Q19 与 Q20 的类别规则已获准。630 个 `none` 确定性记为 `no_external_basis`，13 个 `self` 记为 `project_assertion`，23 个缺 locator 的值记为阻断审计；这些行不产生正式 `basis`，也不要求逐字段人工 patch。只有拟登记为正式 `basis` 的值必须逐项具有实体、locator、按 Q19 决定的 checked 和 accepted patch。

- [ ] **扩充失败测试**

```python
def test_basis_ledger_has_1501_rows_and_correct_partitions(self):
    ledger = load_yaml(ROOT / "vocab/migrations/source-v1/basis.yaml")
    self.assertEqual(1501, len(ledger["rows"]))
    self.assertEqual({"formal": 1496, "generator": 1, "documentation": 4}, ledger["partitions"])

def test_old_none_and_self_counts_remain_auditable(self):
    rows = load_yaml(ROOT / "vocab/migrations/source-v1/basis.yaml")["rows"]
    self.assertEqual(630, sum(row["old_value"] == "none" and row["scope"] == "formal"
                              for row in rows))
    self.assertEqual(13, sum(row["old_value"] == "self" and row["scope"] == "formal"
                             for row in rows))

def test_replacement_patches_can_supply_missing_locators(self):
    replacement = rows_touched_by_q(fixture_plan(REPLACEMENT), "Q19")
    self.assertNotEqual(actual_patch_signatures(fixture_plan(DECISIONS), ("Q19",)),
                        actual_patch_signatures(fixture_plan(REPLACEMENT), ("Q19",)))
    self.assertTrue(any(row["disposition"] == "register" for row in replacement))

def test_each_migrated_basis_is_adjacent_to_one_value_path(self):
    rows = load_yaml(ROOT / "vocab/migrations/source-v1/basis.yaml")["rows"]
    migrated = [row for row in rows if row["disposition"] == "register"]
    self.assertTrue(all(row["field_path"] and len(row["new_basis"]) >= 1 for row in migrated))

def test_basis_ledger_preserves_old_file_hash_and_value(self):
    rows = load_yaml(ROOT / "vocab/migrations/source-v1/basis.yaml")["rows"]
    self.assertTrue(all(len(row["old_file_sha256"]) == 64 and
                        "old_value" in row for row in rows))
```

  在 `tests/test_build_topics_sources.py` 先写入独立候选树辅助函数，再写测试。夹具 `candidate-plan` 不含阻断，只覆盖库存中的 CS2023、ASVS、SWEBOK、RFC 1122、LOM 与 Wikidata 风险身份。

```python
import pathlib
import tempfile
import unittest

import yaml

from scripts.apply_source_migration import apply_migration
from tests.source_governance_helpers import load_yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "source-governance"

def candidate_files():
    with tempfile.TemporaryDirectory() as tmp:
        output = pathlib.Path(tmp) / "candidate"
        result = apply_migration(FIXTURES / "candidate-input", FIXTURES / "candidate-plan", output)
        if result.blocked:
            raise AssertionError(result.blocked)
        return {
            "topics_bytes": (output / "vocab/topics.yaml").read_bytes(),
            "topics": yaml.safe_load((output / "vocab/topics.yaml").read_text(encoding="utf-8")),
            "forms": yaml.safe_load((output / "vocab/forms.yaml").read_text(encoding="utf-8")),
            "old_topics": yaml.safe_load((FIXTURES / "candidate-input/vocab/topics.yaml").read_text(encoding="utf-8")),
        }

def walk(value):
    yield value
    if isinstance(value, dict):
        for nested in value.values():
            yield from walk(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from walk(nested)

def build_candidate_topics():
    return candidate_files()["topics"]

def build_candidate_topics_bytes():
    return candidate_files()["topics_bytes"]

def find_scalar_basis(document):
    return any(isinstance(value.get("basis"), str) for value in walk(document)
               if isinstance(value, dict) and "basis" in value)

def find_legacy_basis_values(document, legacy):
    return any(isinstance(item, str) and item in legacy
               for value in walk(document) if isinstance(value, dict) and "basis" in value
               for item in walk(value["basis"]))

def find_source_scalar(document, expected):
    return any(value.get("source") == expected for value in walk(document)
               if isinstance(value, dict))

def array_memberships(document):
    return {row["id"]: tuple(row.get("arrays", [])) for row in document["concepts"]}

def frozen_and_candidate_array_memberships():
    files = candidate_files()
    return array_memberships(files["old_topics"]), array_memberships(files["topics"])

def collect_candidate_matches():
    return [match for value in walk(build_candidate_topics()) if isinstance(value, dict)
            for match in value.get("match", []) if isinstance(match, dict)]

def collect_candidate_match_relations():
    return {item["rel"] for item in collect_candidate_matches()}

class BuildTopicsSourceTests(unittest.TestCase):
    def test_candidate_generation_does_not_emit_scalar_basis(self):
        output = build_candidate_topics()
        self.assertFalse(find_scalar_basis(output))

    def test_candidate_generation_does_not_restore_source_none_or_self_basis(self):
        output = build_candidate_topics()
        self.assertFalse(find_legacy_basis_values(output, {"source", "none", "self"}))

    def test_candidate_generation_is_byte_deterministic(self):
        self.assertEqual(build_candidate_topics_bytes(), build_candidate_topics_bytes())

```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_source_migration tests.test_build_topics_sources -v`

  Expected: FAIL，账本与候选生成辅助函数不存在；旧生成器仍会写出紧缩值。

- [ ] **生成依据账本**

  Run: `python3 scripts/plan_source_migration.py --root . --inventory-dir .superpowers/sdd/2026-08-31-governance-implementation-prep --decision-dir design/decisions --section basis --ledger vocab/migrations/source-v1/basis.yaml`

  生成器逐项消费 Q19／Q20 patches。候选树测试调用 `apply_migration()` 写不存在的临时子目录，不修改正式 `scripts/build-topics.py` 或 `vocab/topics.yaml`。推荐与 replacement 使用同一字段物化代码。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_source_migration tests.test_build_topics_sources -v`

  Expected: 新增 8 项高风险测试全部通过；1,501 行完整，旧 630／13／23 身份可审计，候选生成连续两次逐字节一致。

- [ ] **延后阶段回归**

  本任务只运行逐值依据的定向 GREEN、冻结输出和写集检查；完整回归并入文档分流的迁移账本闭合门禁。

- [ ] **核对写集**

  Run: `git diff --name-only -- vocab/migrations/source-v1/basis.yaml tests/test_source_migration.py tests/test_build_topics_sources.py vocab/topics.yaml vocab/entities.yaml vocab/forms.yaml vocab/build/extra-arrays.json design/maintenance.md design/topics.md scripts/build-topics.py`

  Expected: 只列账本与两份测试；正式输入、输出、脚本和文档零差异。

- [ ] **说明回滚**

  提交被拒绝时，用 `apply_patch` 恢复账本与测试并创建新的 `[L2] revert: compensate basis ledger` 补偿提交；Q19／Q20 决定与 decision_trace 保留。

- [ ] **提交任务**

```bash
git add vocab/migrations/source-v1/basis.yaml tests/test_source_migration.py tests/test_build_topics_sources.py
git commit -m "[L2] data: record per-value basis migration"
```

### 实际派生

**Files:**

- Create: `vocab/migrations/source-v1/source.yaml`
- Modify: `tests/test_source_migration.py`
- Modify: `tests/test_build_topics_sources.py`
- Read: `vocab/topics.yaml`
- Read: `vocab/forms.yaml`
- Read: `vocab/build/extra-arrays.json`

**Interfaces:**

- Consumes: 726 个直接字段、Q13 至 Q17 的获准决定、用途角色账本。
- Produces: 692 个实际派生候选、24 个主题数组、8 个项目 `self` 与 2 个载体数组的互斥账本；689 个唯一 registry/item 组合单独对账。

**人工门禁:** Q13 至 Q17 的类别规则和 registry 级 locator 模板已获准。692 个候选先由模板确定性展开完整 item、locator 和 source.basis；只有模板异常、多来源例外、角色未批准或语义不确定的行进入人工决定。每个最终登记的派生仍必须对应 approved structure、item、locator 与 source.basis；旧 `source` 标量本身不能自动取得派生效力。

- [ ] **扩充失败测试**

```python
def test_source_ledger_has_726_rows_and_four_partitions(self):
    ledger = load_yaml(ROOT / "vocab/migrations/source-v1/source.yaml")
    self.assertEqual(726, len(ledger["rows"]))
    self.assertEqual({"derivation": 692, "array_label": 24,
                      "project_assertion": 8, "local_analysis": 2}, ledger["partitions"])

def test_q16_recommended_patches_isolate_two_form_arrays_without_blocking(self):
    rows = [row for row in rows_touched_by_q(fixture_plan(DECISIONS), "Q16")
            if row["partition"] == "local_analysis"]
    self.assertEqual({"forms-presentation", "forms-activity"}, {row["record_id"] for row in rows})
    self.assertTrue(all(row["operation"] == "isolate" and
                        row["disposition"] == "isolated_local_analysis" and
                        not row["blocks_cutover"] for row in rows))

def test_every_registered_source_has_approved_structure_and_complete_value(self):
    rows = load_yaml(ROOT / "vocab/migrations/source-v1/source.yaml")["rows"]
    registered = [row for row in rows if row["disposition"] == "register"]
    self.assertTrue(all(row["role_status"] == "approved" and
                        set(row["new_value"]) == {"registry", "item", "locator", "basis"}
                        for row in registered))
```

  候选树夹具测试再加入：

```python
def test_candidate_generation_never_emits_source_self(self):
    self.assertFalse(find_source_scalar(build_candidate_topics(), "self"))

def test_candidate_generation_preserves_all_array_memberships(self):
    before, after = frozen_and_candidate_array_memberships()
    self.assertEqual(before, after)
```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_source_migration tests.test_build_topics_sources -v`

  Expected: FAIL，`source.yaml` 不存在且旧生成器仍写单值数组来源。

- [ ] **生成派生账本**

  Run: `python3 scripts/plan_source_migration.py --root . --inventory-dir .superpowers/sdd/2026-08-31-governance-implementation-prep --decision-dir design/decisions --section source --ledger vocab/migrations/source-v1/source.yaml`

  生成器只按 identity／field 应用 Q13 至 Q17 patches。Q16 推荐 accepted 时，两个载体数组的最终行生成 `isolate`，并由通用访问器忽略 local_analysis；replacement accepted 时逐项采用 replacement。八个顶层 self、三条多来源概念、24 个主题数组和 RFC 四层都没有代码默认分支。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_source_migration tests.test_build_topics_sources -v`

  Expected: 新增 5 项高风险测试全部通过；726 行与 692／24／8／2 完整对账；推荐与 replacement patch fixture 都可独立物化最终语义。

- [ ] **延后阶段回归**

  本任务只运行实际派生的定向 GREEN 与写集检查；完整回归并入文档分流的迁移账本闭合门禁。

- [ ] **核对写集**

  Run: `git diff --name-only -- vocab/migrations/source-v1/source.yaml tests/test_source_migration.py tests/test_build_topics_sources.py vocab/topics.yaml vocab/forms.yaml vocab/build/extra-arrays.json scripts/build-topics.py`

  Expected: 只列账本与测试，不列正式输入、输出或生成器。

- [ ] **说明回滚**

  提交被拒绝时，用 `apply_patch` 恢复账本与测试并创建新的 `[L2] revert: compensate source derivation ledger` 补偿提交；Q13 至 Q17 决定与 decision_trace 保留。

- [ ] **提交任务**

```bash
git add vocab/migrations/source-v1/source.yaml tests/test_source_migration.py tests/test_build_topics_sources.py
git commit -m "[L2] data: record source derivation migration"
```

### 概念映射

**Files:**

- Create: `vocab/migrations/source-v1/match.yaml`
- Modify: `tests/test_source_migration.py`
- Modify: `tests/test_build_topics_sources.py`
- Read: `vocab/topics.yaml`
- Read: `vocab/entities.yaml`
- Read: `vocab/forms.yaml`
- Read: `vocab/types.yaml`
- Read: `vocab/genres.yaml`

**Interfaces:**

- Consumes: 756 个映射库存行、Q17 与 Q18 的获准结论、逐角色 approved `mapping` 用途。
- Produces: 756 行映射账本；每行保存 registry、item、候选 rel、本地范围依据、外部范围依据、关系依据、决定和阻断。

**人工门禁:** Q17 与 Q18 有 accepted patches；每个拟迁移行的 mapping 角色已批准，双方范围可定位，关系依据与决定齐备。缺一项 required patch 即停止，不生成账本。

- [ ] **扩充失败测试**

```python
def test_match_ledger_has_exactly_756_rows(self):
    rows = load_yaml(ROOT / "vocab/migrations/source-v1/match.yaml")["rows"]
    self.assertEqual(756, len(rows))

def test_no_current_relation_is_inherited_without_adjacent_basis(self):
    rows = load_yaml(ROOT / "vocab/migrations/source-v1/match.yaml")["rows"]
    migrated = [row for row in rows if row["disposition"] == "register"]
    self.assertTrue(all(row["new_value"]["basis"] and row["decision"] for row in migrated))

def test_old_relation_counts_remain_auditable(self):
    rows = load_yaml(ROOT / "vocab/migrations/source-v1/match.yaml")["rows"]
    self.assertEqual(748, sum(row["old_rel"] == "exactMatch" for row in rows))
    self.assertEqual(8, sum(row["old_rel"] == "closeMatch" for row in rows))

def test_recommended_and_replacement_match_patches_both_materialize(self):
    recommended = fixture_plan(DECISIONS)
    replacement_plan = fixture_plan(REPLACEMENT)
    replacement = rows_touched_by_q(replacement_plan, "Q18")
    self.assertNotEqual(actual_patch_signatures(recommended, ("Q18",)),
                        actual_patch_signatures(replacement_plan, ("Q18",)))
    self.assertTrue(any(not row["blocks_cutover"] for row in replacement))

def test_match_requires_approved_mapping_role(self):
    rows = load_yaml(ROOT / "vocab/migrations/source-v1/match.yaml")["rows"]
    migrated = [row for row in rows if row["disposition"] == "register"]
    self.assertTrue(all(row["mapping_role_status"] == "approved" for row in migrated))
```

  候选树测试再加入：

```python
def test_candidate_generation_emits_only_five_match_relations(self):
    relations = collect_candidate_match_relations()
    self.assertTrue(relations <= {"exactMatch", "closeMatch", "broadMatch",
                                  "narrowMatch", "relatedMatch"})

def test_candidate_match_items_all_have_adjacent_basis(self):
    self.assertTrue(all(item["basis"] for item in collect_candidate_matches()))
```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_source_migration tests.test_build_topics_sources -v`

  Expected: FAIL，`match.yaml` 不存在或 accepted Q17／Q18 patches 尚未进入唯一最终行。

- [ ] **生成映射账本**

  Run: `python3 scripts/plan_source_migration.py --root . --inventory-dir .superpowers/sdd/2026-08-31-governance-implementation-prep --decision-dir design/decisions --section match --ledger vocab/migrations/source-v1/match.yaml`

  生成器只按 identity／field 应用 Q17／Q18 patches。推荐 accepted 时可以组合出 `blocked_unread_material`；replacement accepted 时可以在完整 basis、approved mapping 和决定齐备后组合出 `register`。代码不硬编码 LOM、GB/T、Wikidata 或 748 个 exactMatch 的迁移处置。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_source_migration tests.test_build_topics_sources -v`

  Expected: 新增 7 项高风险测试全部通过；756 行完整；旧关系计数保留审计；推荐与 replacement patches 各自物化；所有 register 行有相邻 basis 与 approved mapping。

- [ ] **延后阶段回归**

  本任务只运行概念映射的定向 GREEN 与写集检查；完整回归并入文档分流的迁移账本闭合门禁。

- [ ] **核对写集**

  Run: `git diff --name-only -- vocab/migrations/source-v1/match.yaml tests/test_source_migration.py tests/test_build_topics_sources.py vocab/topics.yaml vocab/entities.yaml vocab/forms.yaml vocab/types.yaml vocab/genres.yaml`

  Expected: 只列账本与测试。

- [ ] **说明回滚**

  提交被拒绝时，用 `apply_patch` 恢复账本与测试并创建新的 `[L2] revert: compensate source mapping ledger` 补偿提交；Q17／Q18 决定与 decision_trace 保留。

- [ ] **提交任务**

```bash
git add vocab/migrations/source-v1/match.yaml tests/test_source_migration.py tests/test_build_topics_sources.py
git commit -m "[L2] data: record concept mapping migration"
```

### 复核义务

**Files:**

- Modify: `scripts/source_model.py`
- Create: `tests/test_source_obligations.py`
- Create: `tests/fixtures/source-governance/obligation-transitions/`
- Generate at cutover: `vocab/source-obligations.yaml`

**Interfaces:**

- Consumes: 来源实体、反向索引、决定索引、前一义务快照和 Q22 的衔接规则。
- Produces: `open_obligation(document: Dict[str, object], entity: str, trigger: str, targets: Sequence[Dict[str, str]], decisions: Sequence[str], opened: str, obligation_id: str) -> Dict[str, object]` 与 `resolve_obligation(document: Dict[str, object], obligation_id: str, resolved: str, conclusions: Dict[str, object], decisions: Sequence[str]) -> Dict[str, object]`；两者返回新文档，不原地改写输入。
- Internal: `latest_resolved(document, entity, trigger) -> Optional[str]`、`active_same_trigger(document, entity, trigger) -> bool`、`unique_obligation(document, obligation_id) -> Dict[str, object]`、`require_open(row) -> None`、`require_all_target_conclusions(targets, conclusions) -> None`、`require_required_decisions(conclusions, decisions) -> None`、`stable_union(left, right) -> List[str]`。

**人工门禁:** 来源义务模式、正式路径、ID 格式、决定变化触发和来源／术语衔接已经获准。义务不能替代任何正式值或项目决定。

- [ ] **写入失败测试**

```python
import copy
import unittest

from scripts.source_model import open_obligation, resolve_obligation

def empty_document():
    return {"schema": "urn:kb-design:data:source-obligations",
            "schema_version": 1, "obligations": []}

def targets():
    return [{"kind": "basis", "file": "vocab/topics.yaml",
             "record": "concept:controlled-vocabulary",
             "field_path": "definitions[0].basis[0]"}]

def target_conclusions():
    return {"vocab/topics.yaml:concept:controlled-vocabulary:definitions[0].basis[0]":
            {"outcome": "retain", "reviewed": "2026-09-01"}}

def open_document():
    return open_obligation(empty_document(), "z39-19", "new_version", targets(), [],
                           "2026-08-31", "source-review-20260831-001")

def resolved_document():
    return resolve_obligation(open_document(), "source-review-20260831-001",
                              "2026-09-01", target_conclusions(), ["decision-source-0002"])

def retrigger(document, obligation_id):
    return open_obligation(document, "z39-19", "new_version", targets(), [],
                           "2026-09-02", obligation_id)

def term_trigger(obligation_id):
    return {"kind": "source_obligation", "id": obligation_id}

class SourceObligationTests(unittest.TestCase):
    def test_new_obligation_is_open_with_first_history_entry(self):
        result = open_obligation(empty_document(), "z39-19", "new_version", targets(), [],
                                 "2026-08-31", "source-review-20260831-001")
        row = result["obligations"][0]
        self.assertEqual(("open", "2026-08-31", None),
                         (row["state"], row["opened"], row["resolved"]))
        self.assertEqual("opened", row["history"][0]["action"])

    def test_opening_does_not_mutate_input_document(self):
        source = empty_document()
        frozen = copy.deepcopy(source)
        open_obligation(source, "z39-19", "new_version", targets(), [],
                        "2026-08-31", "source-review-20260831-001")
        self.assertEqual(frozen, source)

    def test_resolution_requires_all_target_conclusions_and_decisions(self):
        with self.assertRaises(ValueError):
            resolve_obligation(open_document(), "source-review-20260831-001",
                               "2026-09-01", {}, [])

    def test_resolved_obligation_cannot_reopen(self):
        resolved = resolved_document()
        with self.assertRaises(ValueError):
            open_obligation(resolved, "z39-19", "new_version", targets(), [],
                            "2026-09-02", "source-review-20260831-001")

    def test_retrigger_creates_new_id_and_previous_reference(self):
        result = retrigger(resolved_document(), "source-review-20260902-001")
        self.assertEqual("source-review-20260831-001", result["obligations"][-1]["previous"])

```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_source_obligations -v`

  Expected: ERROR，`open_obligation` 与 `resolve_obligation` 尚未定义。

- [ ] **实现纯函数状态机**

```python
def open_obligation(document, entity, trigger, targets, decisions, opened, obligation_id):
    result = copy.deepcopy(document)
    if any(row["id"] == obligation_id for row in result["obligations"]):
        raise ValueError("obligation id already exists")
    previous = latest_resolved(result, entity, trigger)
    if active_same_trigger(result, entity, trigger):
        raise ValueError("same trigger already open")
    result["obligations"].append({
        "id": obligation_id, "entity": entity, "trigger": trigger,
        "targets": list(targets), "decisions": list(decisions),
        "previous": previous, "state": "open", "opened": opened, "resolved": None,
        "history": [{"date": opened, "action": "opened", "targets": list(targets)}],
    })
    return result

def resolve_obligation(document, obligation_id, resolved, conclusions, decisions):
    result = copy.deepcopy(document)
    row = unique_obligation(result, obligation_id)
    require_open(row)
    require_all_target_conclusions(row["targets"], conclusions)
    require_required_decisions(conclusions, decisions)
    row["state"] = "resolved"
    row["resolved"] = resolved
    row["decisions"] = stable_union(row["decisions"], decisions)
    row["history"].append({"date": resolved, "action": "resolved",
                           "conclusions": conclusions, "decisions": list(decisions)})
    return result
```

  决定采纳、替代或推翻只调用 `open_obligation()`；调用前用反向索引生成 targets，不调用实体、角色、basis、source 或 match 的写入函数。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_source_obligations -v`

  Expected: 5 项高风险测试通过；输入文档保持不变，resolved 不重开，再触发得到新 ID 与 previous。

- [ ] **延后阶段回归**

  本任务只运行复核义务的定向 GREEN 与写集检查；完整回归并入文档分流的迁移账本闭合门禁。

- [ ] **核对写集**

  Run: `git diff --name-only -- scripts/source_model.py tests/test_source_obligations.py tests/fixtures/source-governance/obligation-transitions vocab/source-obligations.yaml`

  Expected: 只列脚本、测试和夹具，不列 `vocab/source-obligations.yaml`。

- [ ] **说明回滚**

  本任务只加纯函数与夹具。提交被拒绝时，用 `apply_patch` 恢复本任务文件并创建新的 `[L2] revert: compensate source obligation lifecycle task` 补偿提交；决定、ID 与已存在义务历史不删除。

- [ ] **提交任务**

```bash
git add scripts/source_model.py tests/test_source_obligations.py tests/fixtures/source-governance/obligation-transitions
git commit -m "[L2] feat: add source review obligation lifecycle"
```

### 文档分流

**Files:**

- Create: `vocab/migrations/source-v1/origin.yaml`
- Modify: `tests/test_source_migration.py`
- Create: `tests/test_source_docs.py`
- Create: `tests/fixtures/source-governance/candidate-docs/section-disposition.yaml`
- Create: `tests/fixtures/source-governance/candidate-docs/formal/`
- Read: `concepts/classifying-new-subjects.md`
- Read: `design/content-model.md`
- Read: `design/drafts/terminology-governance.md`
- Read: `design/entities.md`
- Read: `design/maintenance.md`
- Read: `design/principles.md`
- Read: `design/topics.md`
- Read: `docs/superpowers/specs/2026-08-27-terminology-governance-design.md`
- Read: `scripts/build-topics.py`
- Read: `scripts/check-topics.py`
- Read: `vocab/topics.yaml`

**Interfaces:**

- Consumes: 19 个 `origin` 库存身份、Q21 的获准分流、各文档旧节目录。
- Produces: 19 行账本，每行只取 `discovery_observation`、`basis_rule`、`source_rule`、`process_rule`、`zero_use_evidence`、`not_in_scope`；候选文档逐节去向表。

**人工门禁:** Q21 有 accepted patches；`design/content-model.md` 的内容单元保留规则另有有效依据。缺失时停止，不生成账本或候选文档。

- [ ] **写入失败测试**

```python
def test_origin_ledger_has_exactly_19_rows(self):
    rows = load_yaml(ROOT / "vocab/migrations/source-v1/origin.yaml")["rows"]
    self.assertEqual(19, len(rows))

def test_origin_ledger_does_not_create_formal_origin_values(self):
    rows = load_yaml(ROOT / "vocab/migrations/source-v1/origin.yaml")["rows"]
    self.assertFalse(any("new_origin" in row for row in rows))

def test_origin_zero_use_evidence_stays_separate_from_data(self):
    rows = load_yaml(ROOT / "vocab/migrations/source-v1/origin.yaml")["rows"]
    self.assertTrue(any(row["disposition"] == "zero_use_evidence" for row in rows))

```

  `tests/test_source_docs.py` 写入：

```python
import pathlib
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "tests" / "fixtures" / "source-governance" / "candidate-docs"

def disposition_document():
    return yaml.safe_load((CANDIDATE / "section-disposition.yaml").read_text(encoding="utf-8"))

def count_closed_origin_dispositions():
    return sum(row["status"] == "closed" for row in disposition_document()["rows"])

def candidate_docs():
    return "\n".join(path.read_text(encoding="utf-8")
                      for path in sorted((CANDIDATE / "formal").rglob("*.md")))

def find_generic_origin_definition(text):
    return "origin 是通用来源字段" in text or "origin 统一表示" in text

def content_retention_has_independent_rule(text):
    return "design/content-model.md#保留规则" in text and "origin" not in retention_rule_line(text)

def retention_rule_line(text):
    return next(line for line in text.splitlines() if "design/content-model.md#保留规则" in line)

def candidate_document_write_set():
    return disposition_document()["write_set"]

class SourceDocsTests(unittest.TestCase):
    def test_candidate_docs_have_disposition_for_all_old_origin_sections(self):
        self.assertEqual(19, count_closed_origin_dispositions())

    def test_candidate_docs_do_not_define_generic_origin(self):
        self.assertFalse(find_generic_origin_definition(candidate_docs()))

    def test_content_retention_cites_content_model_rule_not_origin(self):
        self.assertTrue(content_retention_has_independent_rule(candidate_docs()))

    def test_frozen_debt_files_are_not_in_document_write_set(self):
        write_set = candidate_document_write_set()
        self.assertNotIn("vocab/CHANGELOG.md", write_set)
        self.assertFalse(any(path.startswith(".superpowers/sdd/2026-08-30-") for path in write_set))
```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_source_migration tests.test_source_docs -v`

  Expected: FAIL，`origin.yaml` 与候选文档去向不存在。

- [ ] **生成分流账本与候选文档**

  Run: `python3 scripts/plan_source_migration.py --root . --inventory-dir .superpowers/sdd/2026-08-31-governance-implementation-prep --decision-dir design/decisions --section origin --ledger vocab/migrations/source-v1/origin.yaml --candidate .superpowers/sdd/2026-08-31-source-schema-migration/candidate/docs`

  每个 Markdown 文件先生成旧标题、旧职责、目标标题、目标职责、依据和动作。发现观察只指向 Q21 的 ignored TSV；`basis` 和 `source` 示例只在真实实体、真实对象和相邻依据齐备时保留；正式 YAML/JSON 仍为 0 个 `origin`。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_source_migration tests.test_source_docs -v`

  Expected: 新增 7 项高风险测试全部通过；19 行全部关闭，零正式 `origin`，冻结债务写集为零。

- [ ] **运行迁移账本闭合回归**

  Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v && python3 scripts/check-topics.py && python3 scripts/check_link_baseline.py && git diff --check`

  Expected: 全部测试通过；链接基线输出 `KNOWN_LINK_BASELINE_OK count=2`；正式文档零差异；差异检查继续运行。

- [ ] **核对写集**

  Run: `git diff --name-only -- vocab/migrations/source-v1/origin.yaml tests/test_source_migration.py tests/test_source_docs.py concepts design scripts vocab/topics.yaml docs/superpowers/specs`

  Expected: 只列账本与测试，不列读取的正式文档、脚本、规格或词表。

- [ ] **说明回滚**

  提交被拒绝时，用 `apply_patch` 恢复账本、测试与候选文档夹具并创建新的 `[L2] revert: compensate source document disposition task` 补偿提交；正式文档与决定历史不删除。

- [ ] **提交任务**

```bash
git add vocab/migrations/source-v1/origin.yaml tests/test_source_migration.py tests/test_source_docs.py tests/fixtures/source-governance/candidate-docs
git commit -m "[L2] docs: record origin interface dispositions"
```

### 原子切换

**Files:**

- Create: `tests/test_source_cutover.py`
- Create: `tests/fixtures/source-governance/compensation-decision.md`
- Create: `tests/fixtures/source-governance/tampered-handoff/`
- Create: `tests/fixtures/source-governance/tampered-payload/`
- Create: `design/source-governance.md`
- Delete after L3 effectiveness decision: `design/drafts/source-governance.md`
- Create: `design/decisions/source-governance-effective.md`
- Create: `design/decisions/source-schema-cutover.md`
- Create: `design/decisions/source-schema-rollback.md`
- Create on compensation: `design/decisions/source-schema-rollback-result.md`
- Create: `vocab/source-obligations.yaml`
- Generate: `vocab/generated/source-reference-index.json`
- Generate before audit decision: `vocab/generated/source-cutover-payload.json`
- Generate after payload: `vocab/generated/source-cutover-handoff.json`
- Modify: `vocab/entities.yaml`
- Modify: `vocab/sources.yaml`
- Generate: `vocab/topics.yaml`
- Modify: `vocab/forms.yaml`
- Modify: `vocab/types.yaml`
- Modify: `vocab/genres.yaml`
- Modify: `vocab/build/extra-arrays.json`
- Modify: `scripts/build-topics.py`
- Modify: `scripts/check-topics.py`
- Modify: `design/governance.md`
- Modify: `design/maintenance.md`
- Modify: `design/entities.md`
- Modify: `design/sources-registry.md`
- Modify: `design/topics.md`
- Modify: `design/content-model.md`
- Modify: `design/principles.md`
- Modify: `design/README.md`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Runtime write: `.superpowers/sdd/2026-08-31-source-schema-migration/release-candidate/`
- Runtime write: `.superpowers/sdd/2026-08-31-source-schema-migration/delivery/`
- Runtime write: `.superpowers/sdd/2026-08-31-source-schema-migration/verification.md`
- Runtime write: `.superpowers/sdd/2026-08-31-source-schema-migration/compensation-candidate/`

**Interfaces:**

- Consumes: 六份零阻断迁移账本、严格校验器、accepted Q01–Q25、完整候选树、显式 ignored handoff 路径和显式 ignored payload 路径。
- Produces: `build_payload_manifest(candidate_root: Path, apply_paths: Sequence[str]) -> Tuple[Dict[str, object], str, str]`、`build_source_handoff(candidate_root: Path, payload_bytes: bytes, tracked_write_set: Sequence[str], markdown_paths: Sequence[str], schema_paths: Sequence[str], ledger_paths: Sequence[str]) -> Tuple[Dict[str, object], str]`、`verify_source_handoff(repo_root: Path, handoff_path: Path, payload_path: Path, candidate_root: Path) -> List[Issue]`、`load_bound_source_delivery(repo_root: Path, decision_path: Path, candidate_root: Path) -> Tuple[Dict[str, object], Dict[str, object]]`、`apply_bound_payload(repo_root: Path, candidate_root: Path, decision_path: Path) -> Sequence[str]`、`load_rollback_plan(decision_path: Path) -> Dict[str, object]`、`build_compensation_candidate(repo_root: Path, rollback: Dict[str, object], output_root: Path, decision_path: Path) -> Path`；一个先行审计提交、一个只含 bound payload entries 的原子切换提交；不执行发版。

**人工门禁:** Q25 accepted patches 允许生成候选；六份账本 `blocks_cutover` 总数为 0。ignored candidate、payload 和 handoff 先由 `verify_source_handoff()` 验证；人核对后分别 accepted `decision-source-0004`、`0005`、`0006`，之后才能创建先行审计提交。任一条件缺失即停止，不创建审计提交或修改正式树。改档与术语准入仍为“无”。

- [ ] **写入正式树失败测试**

```python
import hashlib
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

import yaml

from scripts.apply_source_migration import (
    HANDOFF_FIELDS, HANDOFF_PATH, PAYLOAD_PATH, build_compensation_candidate,
    load_bound_source_delivery, load_rollback_plan, verify_source_handoff,
)
from scripts.build_source_index import build_reference_index
from scripts.source_model import Issue, validate_repository

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_yaml_document(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def ledger_rows(plan_dir):
    rows = []
    for path in sorted(plan_dir.glob("*.yaml")):
        document = load_yaml_document(path)
        rows.extend(document.get("rows", document.get("roles", [])))
    return rows

def count_cutover_blockers(plan_dir):
    return sum(bool(row.get("blocks_cutover")) for row in ledger_rows(plan_dir))

def find_legacy_source_fields(root):
    return [issue for issue in validate_repository(root, allow_legacy=False)
            if issue.code == "SOURCE_LEGACY_FIELD"]

def formal_topic_and_array_counts(root):
    topics = load_yaml_document(root / "vocab/topics.yaml")
    return len(topics["concepts"]), len(topics["arrays"])

def unexplained_identity_changes(root):
    return [row["identity"] for row in ledger_rows(root / "vocab/migrations/source-v1")
            if row.get("identity_changed") and not row.get("decisions")]

def unresolved_obligation_references(root):
    obligations = load_yaml_document(root / "vocab/source-obligations.yaml")["obligations"]
    ids = {row["id"] for row in obligations}
    index = load_json(root / "vocab/generated/source-reference-index.json")["entries"]
    referenced = {row["target_id"] for row in index
                  if row["target_kind"] == "source_obligation"}
    return sorted(referenced - ids)

def run_build_topics_in_copy(root):
    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / "repo"
        shutil.copytree(root, copy,
                        ignore=shutil.ignore_patterns(".git", ".superpowers", "__pycache__"))
        subprocess.run(["python3", "scripts/build-topics.py"], cwd=copy, check=True,
                       text=True, capture_output=True)
        return hashlib.sha256((copy / "vocab/topics.yaml").read_bytes()).hexdigest()

def sha256_path(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def decision_front(path):
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---\n", 2)[1])

def audit_sequences_preserved(before_root, after_root):
    before_entities = {row["id"]: row for row in
                       load_yaml_document(before_root / "vocab/entities.yaml")["entities"]}
    after_entities = {row["id"]: row for row in
                      load_yaml_document(after_root / "vocab/entities.yaml")["entities"]}
    if not set(before_entities) <= set(after_entities):
        return False
    for identity, before in before_entities.items():
        old_history = before.get("history", [])
        if after_entities[identity].get("history", [])[:len(old_history)] != old_history:
            return False
    before_obligations = {row["id"]: row for row in
                          load_yaml_document(before_root / "vocab/source-obligations.yaml")["obligations"]}
    after_obligations = {row["id"]: row for row in
                         load_yaml_document(after_root / "vocab/source-obligations.yaml")["obligations"]}
    return all(identity in after_obligations and
               after_obligations[identity]["history"][:len(row["history"])] == row["history"]
               for identity, row in before_obligations.items())

class SourceCutoverTests(unittest.TestCase):
    def test_formal_tree_passes_strict_source_validation(self):
        self.assertEqual([], validate_repository(ROOT, allow_legacy=False))

    def test_all_six_ledgers_have_zero_cutover_blockers(self):
        self.assertEqual(0, count_cutover_blockers(ROOT / "vocab/migrations/source-v1"))

    def test_formal_counts_match_frozen_identities(self):
        self.assertEqual((700, 24), formal_topic_and_array_counts(ROOT))

    def test_every_count_change_has_approved_mapping(self):
        self.assertEqual([], unexplained_identity_changes(ROOT))

    def test_generated_index_is_bidirectionally_complete(self):
        generated = load_json(ROOT / "vocab/generated/source-reference-index.json")
        self.assertEqual(build_reference_index(ROOT), generated)

    def test_source_obligations_and_term_handoffs_resolve_by_id(self):
        self.assertEqual([], unresolved_obligation_references(ROOT))

    def test_build_topics_is_byte_deterministic(self):
        first = run_build_topics_in_copy(ROOT)
        second = run_build_topics_in_copy(ROOT)
        self.assertEqual(first, second)

    def test_probe_runtime_paths_are_not_tracked(self):
        tracked = subprocess.run(
            ["git", "ls-files", ".superpowers/sdd/2026-08-31-source-schema-migration"],
            cwd=ROOT, text=True, capture_output=True, check=True,
        ).stdout
        self.assertEqual("", tracked)

    def test_payload_excludes_both_delivery_files_and_matches_formal_files(self):
        payload = load_json(ROOT / PAYLOAD_PATH)
        self.assertEqual({"schema", "schema_version", "entries"}, set(payload))
        paths = {row["path"] for row in payload["entries"]}
        self.assertTrue({PAYLOAD_PATH, HANDOFF_PATH}.isdisjoint(paths))
        for row in payload["entries"]:
            path = ROOT / row["path"]
            if row["after_sha256"] is None:
                self.assertFalse(path.exists())
            else:
                self.assertEqual(row["after_sha256"], sha256_path(path))

    def test_same_handoff_verifier_accepts_ignored_and_installed_bytes(self):
        formal_handoff = ROOT / HANDOFF_PATH
        formal_payload = ROOT / PAYLOAD_PATH
        with tempfile.TemporaryDirectory() as tmp:
            ignored = pathlib.Path(tmp) / "delivery"
            ignored.mkdir()
            ignored_handoff = ignored / "source-cutover-handoff.json"
            ignored_payload = ignored / "source-cutover-payload.json"
            shutil.copy2(formal_handoff, ignored_handoff)
            shutil.copy2(formal_payload, ignored_payload)
            issues = verify_source_handoff(ROOT, ignored_handoff, ignored_payload, ROOT)
            self.assertEqual([], issues)
            self.assertTrue(all(isinstance(issue, Issue) for issue in issues))
        self.assertEqual([], verify_source_handoff(
            ROOT, formal_handoff, formal_payload, ROOT,
        ))
        handoff = load_json(formal_handoff)
        self.assertEqual(set(HANDOFF_FIELDS), set(handoff))
        self.assertEqual({"path", "sha256"}, set(handoff["payload"]))
        self.assertEqual(7, len(handoff["schemas"]))
        self.assertEqual(6, len(handoff["migration_ledgers"]))
        self.assertEqual({row["path"] for row in load_json(formal_payload)["entries"]},
                         set(handoff["tracked_write_set"]))

    def test_decision_0005_binds_handoff_and_payload_bytes(self):
        front = decision_front(ROOT / "design/decisions/source-schema-cutover.md")
        handoff_path = ROOT / HANDOFF_PATH
        payload_path = ROOT / PAYLOAD_PATH
        self.assertEqual("decision-source-0005", front["id"])
        self.assertEqual(HANDOFF_PATH, front["delivery_handoff"])
        self.assertEqual(sha256_path(handoff_path), front["handoff_sha256"])
        self.assertEqual(PAYLOAD_PATH, front["delivery_payload"])
        self.assertEqual(sha256_path(payload_path), front["payload_sha256"])

    def test_bound_loader_verifies_decision_then_handoff_then_payload(self):
        handoff, payload = load_bound_source_delivery(
            ROOT, ROOT / "design/decisions/source-schema-cutover.md", ROOT,
        )
        self.assertEqual(handoff["payload"]["sha256"], sha256_path(ROOT / PAYLOAD_PATH))
        self.assertEqual(set(handoff["tracked_write_set"]),
                         {row["path"] for row in payload["entries"]})

    def test_tampered_handoff_is_rejected_by_decision_binding(self):
        fixture = ROOT / "tests/fixtures/source-governance/tampered-handoff"
        with self.assertRaisesRegex(ValueError, "SOURCE_DECISION_DELIVERY_MISSING handoff hash"):
            load_bound_source_delivery(
                fixture, fixture / "design/decisions/source-schema-cutover.md", fixture,
            )

    def test_tampered_payload_is_rejected_by_handoff_binding(self):
        fixture = ROOT / "tests/fixtures/source-governance/tampered-payload"
        direct = verify_source_handoff(
            fixture,
            fixture / HANDOFF_PATH,
            fixture / PAYLOAD_PATH,
            fixture,
        )
        self.assertTrue(direct)
        self.assertTrue(all(isinstance(issue, Issue) for issue in direct))
        with self.assertRaisesRegex(ValueError, "SOURCE_DECISION_DELIVERY_MISSING payload hash"):
            load_bound_source_delivery(
                fixture, fixture / "design/decisions/source-schema-cutover.md", fixture,
            )

    def test_compensation_preserves_decisions_ids_history_and_obligations(self):
        rollback = load_rollback_plan(ROOT / "design/decisions/source-schema-rollback.md")
        with tempfile.TemporaryDirectory() as tmp:
            candidate = build_compensation_candidate(
                ROOT, rollback, pathlib.Path(tmp) / "candidate",
                ROOT / "tests/fixtures/source-governance/compensation-decision.md",
            )
            for path in rollback["preserve_paths"]:
                self.assertEqual((ROOT / path).read_bytes(), (candidate / path).read_bytes())
            self.assertTrue(audit_sequences_preserved(ROOT, candidate))

```

- [ ] **运行 RED**

  Run: `python3 -m unittest tests.test_source_cutover -v`

  Expected: FAIL；当前正式树仍含旧结构，`decision-source-0004` 至 `0006`、交付文件、正式义务或生成索引至少一项不存在。缺 accepted patches 时在此停止。

- [ ] **实现统一交付预验**

  在 `scripts/apply_source_migration.py` 实现接口锁中的 `verify_source_handoff()`。它不得接收已解析 handoff，不得把 `candidate_root` 设为可选，也不得从 handoff 声明的未来正式路径读取 payload。实现先读取显式 `handoff_path` 与 `payload_path`，再读取 `candidate_root` 下的富交付对象；所有失败都构造 `Issue`。

```python
import hashlib
import json
from pathlib import Path
from typing import List

from scripts.source_model import (
    ERROR_CODES, ROLE_QUALIFICATIONS, SCHEMA_IDS, Issue, load_decision_patches,
)

def delivery_issue(path, record, field_path, message):
    return Issue("SOURCE_CUTOVER_MANIFEST_INVALID", str(path), record,
                 field_path, message)

def read_delivery_json(path, record, issues):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        issues.append(delivery_issue(path, record, "$", str(error)))
        return None

def delivery_sha256(path, record, field_path, issues):
    try:
        return sha256_existing(path)
    except OSError as error:
        issues.append(delivery_issue(path, record, field_path, str(error)))
        return None

def verify_source_handoff(repo_root: Path, handoff_path: Path, payload_path: Path,
                          candidate_root: Path) -> List[Issue]:
    issues = []
    handoff = read_delivery_json(handoff_path, "source-cutover-handoff", issues)
    payload = read_delivery_json(payload_path, "source-cutover-payload", issues)
    if handoff is None or payload is None:
        return sorted(issues)
    if set(handoff) != set(HANDOFF_FIELDS):
        issues.append(delivery_issue(handoff_path, "source-cutover-handoff", "$",
                                     f"top-level keys {sorted(handoff)}"))
        return sorted(issues)
    if set(payload) != {"schema", "schema_version", "entries"}:
        issues.append(delivery_issue(payload_path, "source-cutover-payload", "$",
                                     f"top-level keys {sorted(payload)}"))
        return sorted(issues)
    try:
        validate_source_handoff(handoff)
        validate_payload_manifest(payload)
    except ValueError as error:
        issues.append(delivery_issue(handoff_path, "source-cutover-handoff", "$", str(error)))
        return sorted(issues)
    if handoff["payload"] != {
        "path": PAYLOAD_PATH,
        "sha256": delivery_sha256(
            payload_path, "source-cutover-payload", "$", issues,
        ),
    }:
        issues.append(delivery_issue(handoff_path, "source-cutover-handoff", "payload",
                                     "explicit payload bytes do not match binding"))
    if payload_path.read_bytes() != serialize_payload_manifest(payload):
        issues.append(delivery_issue(payload_path, "source-cutover-payload", "$",
                                     "payload bytes are not canonical"))
    if handoff_path.read_bytes() != serialize_source_handoff(handoff):
        issues.append(delivery_issue(handoff_path, "source-cutover-handoff", "$",
                                     "handoff bytes are not canonical"))
    payload_paths = {row["path"] for row in payload["entries"]}
    if {PAYLOAD_PATH, HANDOFF_PATH} & payload_paths:
        issues.append(delivery_issue(payload_path, "source-cutover-payload", "entries",
                                     "delivery file appears in entries"))
    if set(handoff["tracked_write_set"]) != payload_paths:
        issues.append(delivery_issue(handoff_path, "source-cutover-handoff",
                                     "tracked_write_set", "entry path set differs"))
    contract = handoff["source_contract"]
    contract_sha256 = delivery_sha256(
        candidate_root / "scripts/source_model.py",
        "source-cutover-handoff", "source_contract.sha256", issues,
    )
    if contract != {
        "module": "scripts/source_model.py",
        "sha256": contract_sha256,
        "reference_kinds": ["basis", "source", "match", "external_group"],
        "role_qualifications": dict(ROLE_QUALIFICATIONS),
        "error_codes": list(ERROR_CODES),
    }:
        issues.append(delivery_issue(handoff_path, "source-cutover-handoff",
                                     "source_contract", "source contract differs"))
    if len(handoff["schemas"]) != 7:
        issues.append(delivery_issue(handoff_path, "source-cutover-handoff", "schemas",
                                     "schema count differs"))
    for index, row in enumerate(handoff["schemas"]):
        target = candidate_root / row["path"]
        try:
            document = json.loads(target.read_text(encoding="utf-8"))
            valid = (SCHEMA_IDS.get(target.name) == row["$id"]
                     and document["$id"] == row["$id"]
                     and int(row["$id"].rsplit(":", 1)[1]) == row["schema_version"]
                     and delivery_sha256(
                         target, "source-cutover-handoff", f"schemas[{index}]", issues,
                     ) == row["sha256"])
        except (OSError, KeyError, ValueError, json.JSONDecodeError):
            valid = False
        if not valid:
            issues.append(delivery_issue(handoff_path, "source-cutover-handoff",
                                         f"schemas[{index}]", row["path"]))
    topics_path = candidate_root / "vocab/topics.yaml"
    topics_sha256 = delivery_sha256(
        topics_path, "source-cutover-handoff", "topics_sha256", issues,
    )
    if handoff["topics_sha256"] != topics_sha256:
        issues.append(delivery_issue(handoff_path, "source-cutover-handoff",
                                     "topics_sha256", "topics hash differs"))
    for collection in ("migration_ledgers", "markdown_manifest", "outputs"):
        for index, row in enumerate(handoff[collection]):
            target = candidate_root / row["path"]
            actual = delivery_sha256(
                target, "source-cutover-handoff", f"{collection}[{index}]", issues,
            )
            if actual != row["sha256"]:
                issues.append(delivery_issue(handoff_path, "source-cutover-handoff",
                                             f"{collection}[{index}]", row["path"]))
    topics_outputs = [row for row in handoff["outputs"] if row["kind"] == "topics"]
    if len(topics_outputs) != 1 or topics_outputs[0].get("concepts") != 700 \
            or topics_outputs[0].get("arrays") != 24 \
            or topics_outputs[0].get("sha256") != handoff["topics_sha256"]:
        issues.append(delivery_issue(handoff_path, "source-cutover-handoff", "outputs",
                                     "topics output differs from 700/24 binding"))
    return sorted(issues)
```

  `_verify_source_handoff()` 不再存在；所有调用者只调用上述公开函数。`repo_root` 只提供本次仓库身份、逻辑正式路径常量和错误位置基准；`handoff_path` 与 `payload_path` 可以指向仓库内 ignored delivery 或安装后的正式文件，函数不得要求其物理路径等于 handoff 中的逻辑正式路径，也不得用 `repo_root` 替换显式 `payload_path`。`sha256_existing()` 对缺失文件抛出带路径的错误；调用点捕获后转换为相应 `Issue`，不会让单个缺失文件绕过完整问题列表。

- [ ] **实现决定绑定与应用**

  `load_bound_source_delivery()` 只负责决定绑定顺序，并把富交付校验委托给唯一公开接口。`apply_bound_payload()` 在写入前用 candidate root 调用同一接口，写入后再用正式根调用同一接口。

```python
def load_bound_source_delivery(repo_root, decision_path, candidate_root):
    decision = load_front_matter(decision_path)
    if decision.get("id") != "decision-source-0005" or decision.get("status") != "accepted":
        raise ValueError("SOURCE_DECISION_MISSING decision-source-0005")
    if tuple(key for key in DECISION_DELIVERY_FIELDS if key not in decision):
        raise ValueError("SOURCE_DECISION_DELIVERY_MISSING decision fields")
    if {"delivery_manifest", "payload_manifest_sha256"} & set(decision):
        raise ValueError("SOURCE_DECISION_DELIVERY_MISSING deprecated decision fields")
    if decision["delivery_handoff"] != HANDOFF_PATH:
        raise ValueError("SOURCE_DECISION_DELIVERY_MISSING handoff path")
    if decision["delivery_payload"] != PAYLOAD_PATH:
        raise ValueError("SOURCE_DECISION_DELIVERY_MISSING payload path")
    handoff_path = repo_root / decision["delivery_handoff"]
    payload_path = repo_root / decision["delivery_payload"]
    if sha256_existing(handoff_path) != decision["handoff_sha256"]:
        raise ValueError("SOURCE_DECISION_DELIVERY_MISSING handoff hash")
    if sha256_existing(payload_path) != decision["payload_sha256"]:
        raise ValueError("SOURCE_DECISION_DELIVERY_MISSING payload hash")
    issues = verify_source_handoff(
        repo_root, handoff_path, payload_path, candidate_root,
    )
    if issues:
        raise ValueError("; ".join(
            f"{issue.code} {issue.file} {issue.field_path} {issue.message}"
            for issue in issues
        ))
    return (json.loads(handoff_path.read_text(encoding="utf-8")),
            json.loads(payload_path.read_text(encoding="utf-8")))

def apply_bound_payload(repo_root, candidate_root, decision_path):
    handoff, payload = load_bound_source_delivery(repo_root, decision_path, candidate_root)
    verify_apply_targets_clean(repo_root, payload["entries"])
    for entry in payload["entries"]:
        candidate_path = candidate_root / entry["path"]
        if sha256_optional(candidate_path) != entry["after_sha256"]:
            raise ValueError(f"candidate hash mismatch: {entry['path']}")
    backup = create_apply_backup(repo_root, payload["entries"])
    try:
        for entry in payload["entries"]:
            target = repo_root / entry["path"]
            if entry["after_sha256"] is None:
                target.unlink()
            else:
                copy_path(candidate_root / entry["path"], target)
        failures = verify_payload_application(repo_root, payload)
        failures.extend(verify_source_handoff(
            repo_root, repo_root / HANDOFF_PATH, repo_root / PAYLOAD_PATH, repo_root,
        ))
        if failures:
            raise ValueError("; ".join(str(item) for item in failures))
    except Exception:
        restore_apply_backup(repo_root, backup)
        raise
    return tuple(entry["path"] for entry in payload["entries"])
```

  `verify_apply_targets_clean()` 要求 bound payload entries 对应路径没有未提交用户改动；`copy_path()` 使用同目录临时文件、`fsync()` 和 `os.replace()`；`sha256_optional()` 对不存在路径返回 `None`。`create_apply_backup()` 在第一次写入前保存全部目标的存在状态和字节，`restore_apply_backup()` 只恢复这些目标。

- [ ] **实现补偿候选**

```python
def load_rollback_plan(decision_path):
    patches = load_decision_patches([decision_path])
    matches = [patch.value for patch in patches
               if patch.qid == "Q25" and patch.identity == "@control:cutover"
               and patch.field == "rollback_sequence"]
    required = {"pre_cutover_commit", "restore_paths", "preserve_paths", "compensation_paths"}
    if len(matches) != 1 or set(matches[0]) != required:
        raise ValueError("SOURCE_DECISION_DELIVERY_MISSING rollback patches")
    return matches[0]

def build_compensation_candidate(repo_root, rollback, output_root, decision_path):
    decision = load_front_matter(decision_path)
    if (decision.get("id") != "decision-source-0008"
            or decision.get("status") != "accepted"
            or decision.get("supersedes") != ["decision-source-0005"]):
        raise ValueError("SOURCE_DECISION_MISSING decision-source-0008")
    if output_root.exists():
        raise ValueError("compensation output already exists")
    shutil.copytree(repo_root, output_root,
                    ignore=shutil.ignore_patterns(".git", ".superpowers", "__pycache__"))
    for relative in rollback["restore_paths"]:
        content = git_blob(repo_root, rollback["pre_cutover_commit"], relative)
        write_bytes(output_root / relative, content)
    for relative in rollback["preserve_paths"]:
        if (output_root / relative).read_bytes() != (repo_root / relative).read_bytes():
            raise ValueError(f"preserve path changed: {relative}")
    rewrite_compensation_documents(output_root, rollback["compensation_paths"], decision["id"])
    append_rollback_history(output_root / "vocab/entities.yaml", decision["id"])
    append_rollback_history(output_root / "vocab/sources.yaml", decision["id"])
    append_rollback_obligation(output_root / "vocab/source-obligations.yaml", decision["id"])
    run_candidate_validations(output_root, mode="legacy_compatibility")
    return output_root
```

  `git_blob()` 只允许 rollback plan 的 pre_cutover_commit 和 restore_paths；`rewrite_compensation_documents()` 整节写明当前活动表示为 legacy compatibility、来源规则仍有效、ID／history／义务保留；`append_rollback_history()` 与 `append_rollback_obligation()` 只追加 `decision-source-0008`，不删除旧项。

- [ ] **生成候选树**

  Run: `python3 scripts/apply_source_migration.py candidate --root . --plan-dir vocab/migrations/source-v1 --output-root .superpowers/sdd/2026-08-31-source-schema-migration/release-candidate --result .superpowers/sdd/2026-08-31-source-schema-migration/candidate-result.json`

  Expected: 只有阻断数为 0 时生成不存在的 output 子目录、完整 candidate application root 和 `candidate-result.json`；result.written 是待原子应用正式路径的排序数组。每个未来 payload entry 的最终字节都已存在，此后不再修改 candidate entry。脚本先改生成输入和生成器，再生成 `vocab/topics.yaml`，最后用通用访问器生成来源索引。Q16 两数组变为隔离对象，成员关系不变且不产生 local_analysis ReferenceUse。

- [ ] **生成 payload**

  候选根完整验证后才生成 payload；输出到独立 ignored delivery 目录，不写进 candidate，也不出现在 entries。

  Run: `python3 scripts/apply_source_migration.py payload --candidate .superpowers/sdd/2026-08-31-source-schema-migration/release-candidate --apply-result .superpowers/sdd/2026-08-31-source-schema-migration/candidate-result.json --output .superpowers/sdd/2026-08-31-source-schema-migration/delivery/source-cutover-payload.json`

  Expected: payload 顶层键恰为 `schema`、`schema_version`、`entries`；entries 与 candidate-result.written 逐字相等；每个非删除 entry 的 after hash 与 candidate 相同；payload 与 handoff 自身都不在 entries；命令输出 `payload_sha256` 与 `topics_sha256`。

- [ ] **生成 handoff**

  Run: `python3 scripts/apply_source_migration.py handoff --candidate .superpowers/sdd/2026-08-31-source-schema-migration/release-candidate --payload .superpowers/sdd/2026-08-31-source-schema-migration/delivery/source-cutover-payload.json --output .superpowers/sdd/2026-08-31-source-schema-migration/delivery/source-cutover-handoff.json`

  Expected: handoff 顶层键恰为 `schema`、`schema_version`、`payload`、`source_contract`、`schemas`、`topics_sha256`、`migration_ledgers`、`markdown_manifest`、`outputs`、`tracked_write_set`；payload 恰含 path／sha256。`markdown_manifest` 由正式 repo 的受跟踪 Markdown 路径集合叠加 candidate Create／Modify／Delete 计算，不在无 `.git` candidate 中运行 `git ls-files`；只排除 `design/decisions/source-schema-cutover.md`，该决定由绑定链单独验证。命令输出 `handoff_sha256`。

- [ ] **预验 ignored 交付**

  `verify-delivery` 子命令只把四个 CLI 参数一一转给 `verify_source_handoff(Path(root), Path(handoff), Path(payload), Path(candidate))`。它不读取决定文件，不改写参数路径；返回空列表时输出 `SOURCE_DELIVERY_OK issues=0` 并退出 0，否则逐行输出五个 `Issue` 字段并退出 1。

  Run: `python3 scripts/check_sources.py --root .superpowers/sdd/2026-08-31-source-schema-migration/release-candidate && python3 scripts/build_source_index.py --root .superpowers/sdd/2026-08-31-source-schema-migration/release-candidate --output /tmp/kb-source-index-check.json && diff -u /tmp/kb-source-index-check.json .superpowers/sdd/2026-08-31-source-schema-migration/release-candidate/vocab/generated/source-reference-index.json && python3 scripts/apply_source_migration.py verify-delivery --root . --candidate .superpowers/sdd/2026-08-31-source-schema-migration/release-candidate --payload .superpowers/sdd/2026-08-31-source-schema-migration/delivery/source-cutover-payload.json --handoff .superpowers/sdd/2026-08-31-source-schema-migration/delivery/source-cutover-handoff.json`

  Expected: 严格校验零问题；索引无差异；候选树两次生成逐字节相同；700／24 身份不变或每项变化有 accepted patches；唯一公开预验接口返回空 `List[Issue]`。将 ignored payload 移到另一路径但保持字节不变时仍通过；篡改该显式路径中的字节时失败，证明函数没有改读未来正式 payload 路径。

- [ ] **提交先行审计**

  人核对 candidate、payload 与 handoff 后，创建 accepted `decision-source-0004`、`decision-source-0005`、`decision-source-0006`。`decision-source-0005` 的四个绑定键恰为 `delivery_handoff`、`handoff_sha256`、`delivery_payload`、`payload_sha256`；`decision-source-0006` 用 Q25 patches 保存 pre-cutover commit、restore／preserve／compensation paths。把来源正式规则、三份决定、六份账本、已分配 ID 清单、`vocab/source-obligations.yaml` 和 ignored payload／handoff 原字节写入正式审计路径。

  Run: `python3 scripts/apply_source_migration.py install-audit --root . --candidate .superpowers/sdd/2026-08-31-source-schema-migration/release-candidate --payload-source .superpowers/sdd/2026-08-31-source-schema-migration/delivery/source-cutover-payload.json --handoff-source .superpowers/sdd/2026-08-31-source-schema-migration/delivery/source-cutover-handoff.json --decision-dir .superpowers/sdd/2026-08-31-source-schema-migration/delivery/decisions`

  Expected: 命令复制前先以 ignored 两路径和 candidate 调用 `verify_source_handoff()`，复制后再以正式两路径和同一 candidate 调用它；只写固定审计路径。handoff／payload 字节与 `decision-source-0005` 两组绑定 hash 相同；正式数据和消费者仍是切换前表示。payload entries 不含两个交付文件。

  Run: `python3 scripts/apply_source_migration.py verify-delivery --root . --candidate .superpowers/sdd/2026-08-31-source-schema-migration/release-candidate --payload vocab/generated/source-cutover-payload.json --handoff vocab/generated/source-cutover-handoff.json`

  Expected: 正式安装后的 handoff／payload 仍由同一公开接口返回 `SOURCE_DELIVERY_OK issues=0`。

```bash
git add design/source-governance.md design/drafts/source-governance.md design/decisions/source-governance-effective.md design/decisions/source-schema-cutover.md design/decisions/source-schema-rollback.md vocab/migrations/source-v1 vocab/source-obligations.yaml vocab/generated/source-cutover-payload.json vocab/generated/source-cutover-handoff.json
git commit -m "[L3] governance: authorize source schema cutover"
```

  Expected: 先行提交可单独解析全部决定、ID、history、义务、账本、handoff 与 payload；尚未切换正式数据和消费者。后续任何补偿都不得删除这些路径。

- [ ] **应用清单写集**

  Run: `python3 scripts/apply_source_migration.py apply-bound --root . --candidate .superpowers/sdd/2026-08-31-source-schema-migration/release-candidate --decision design/decisions/source-schema-cutover.md`

  Expected: 先验证 decision 的 handoff path／SHA-256 和 payload path／SHA-256，再以正式 handoff、正式 payload 与 candidate 调用 `verify_source_handoff()`，最后只应用 payload entries；写入完成后以 candidate_root 为正式 root 再调用同一接口。每个写入后哈希等于 after_sha256；任一不符先恢复 backup，再进入补偿流程，不删除先行审计提交。

- [ ] **运行 GREEN**

  Run: `python3 -m unittest tests.test_source_cutover -v`

  Expected: 15 项高风险测试通过；ignored 与正式安装阶段使用同一四路径 verifier，返回类型为 `Issue`；严格模式零旧结构，反向索引双向完整，义务引用可解析，decision → handoff → payload 两层绑定一致，篡改 handoff 或 payload 都被拒绝，补偿夹具保留全部审计对象。

- [ ] **运行正式切换闭合回归**

  Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v && python3 scripts/check_sources.py --root . && python3 scripts/check-topics.py && python3 scripts/build-topics.py && shasum -a 256 vocab/topics.yaml > /tmp/kb-source-topics-first.sha256 && python3 scripts/build-topics.py && shasum -a 256 vocab/topics.yaml > /tmp/kb-source-topics-second.sha256 && diff -u /tmp/kb-source-topics-first.sha256 /tmp/kb-source-topics-second.sha256 && python3 scripts/check_link_baseline.py && python3 scripts/check-terms.py --all > .superpowers/sdd/2026-08-31-source-schema-migration/terms-after.txt && git diff --check`

  Expected: 全部单元测试和来源／词表校验通过；两次生成哈希相同；链接基线输出 `KNOWN_LINK_BASELINE_OK count=2`；术语报告只作人工复核线索，不产生准入；`git diff --check` 无输出。

- [ ] **核对正式身份**

  Run: `python3 scripts/plan_source_migration.py --root . --inventory-dir .superpowers/sdd/2026-08-31-governance-implementation-prep --decision-dir design/decisions --verify-cutover vocab/migrations/source-v1 --handoff vocab/generated/source-cutover-handoff.json --payload vocab/generated/source-cutover-payload.json --output .superpowers/sdd/2026-08-31-source-schema-migration/verification.md`

  Expected: 138、47、1,501、726、756、19 全部逐行关闭；31／107、692／24／8／2 不混合；700／24 保持或逐项有批准映射；13 个 self、630 个 none 与 23 个无 locator 均有审计处置而非伪造 basis。

- [ ] **核对写集**

  Run: `python3 scripts/apply_source_migration.py verify-write-set --root . --decision design/decisions/source-schema-cutover.md`

  Expected: Git 差异逐字等于 bound payload entries；不列 payload、handoff、先行审计文件、`vocab/CHANGELOG.md`、`vocab/signals.yaml`、`concepts/`、术语治理草案、旧决定、旧 SDD 输入或 ignored 运行材料。

- [ ] **说明回滚**

  任一 GREEN 失败时先保存失败输出，由人按 `decision-source-0006` 创建 `decision-source-0008`。运行 `python3 scripts/apply_source_migration.py compensate --root . --rollback-decision design/decisions/source-schema-rollback.md --decision design/decisions/source-schema-rollback-result.md --output .superpowers/sdd/2026-08-31-source-schema-migration/compensation-candidate`。候选必须：从 Q25 rollback patches 的 pre_cutover_commit 恢复 restore_paths 的活动表示；逐字保留 preserve_paths；整节重写 compensation_paths，声明共享来源规则仍有效但消费者处于 legacy compatibility；向现有实体、角色和义务追加 rollback history，不删除 ID、旧 history 或义务。

  验证 compensation candidate 后，用 `apply-manifest --mode compensation` 写正式树并创建新的补偿提交：

```bash
git add design scripts vocab AGENTS.md README.md
git commit -m "[L3] fix: compensate failed source schema cutover"
```

  补偿提交后重新运行全部回归，并验证 `decision-source-0004` 至 `0006`、`decision-source-0008`、六份账本、handoff、payload、全部 ID、history 与义务仍可查询。禁止整提交反转或反向 patch 删除证据。

- [ ] **提交原子切换**

  使用 bound payload entries 生成 NUL 分隔 pathspec 并只暂存这些路径：

```bash
python3 scripts/apply_source_migration.py pathspec --decision design/decisions/source-schema-cutover.md | git add --pathspec-from-file=- --pathspec-file-nul
git commit -m "[L3] feat: switch to source governance schema"
```

- [ ] **停止于发版门禁**

  原子提交和回归通过后停止。只有人另行采纳 `decision-source-0007`，才可创建 `design/decisions/source-schema-release.md`、修改各词表 `version.id` 与 `vocab/CHANGELOG.md` 并发版；本计划不把切换提交解释为发版。

## 验证矩阵

计划只设计 139 项高风险测试，覆盖 schema 负例、语义效力、稳定身份、迁移完整性、确定性、正式写集、交付绑定、篡改拒绝和补偿回滚。文件存在、实现形状、重复 patch 对账、重复计数、字面量自证和已经由阶段命令覆盖的链接基线不建立单元测试。任务中的保留测试按以下关系闭合。

| 需求 | RED／GREEN 位置 | 关键反例 |
|---|---|---|
| 来源实体与用途分离 | `test_source_schema.py`、`test_check_sources.py`、现行实体与用途角色任务 | entity `current` 或消费者数量自动批准角色 |
| 消费者契约 | `test_source_contract.py`、`test_check_sources.py` | 术语侧适配器、未知错误码、source／external_group 缺 approved structure |
| 共享引用结构 | `test_source_schema.py`、逐值依据、实际派生、概念映射任务 | `self`、`none`、裸 URL、悬空 external_group、同名或默认 exactMatch |
| 替代决定 | `test_source_migration.py` 的最终字段、状态和冲突测试 | 重复 identity／field、Q 越权、替代决定未改变最终语义 |
| 外部状态与历史 | `test_check_sources.py`、现行实体任务 | `candidate` 映射 current、暂不可用映射 withdrawn、历史改写 |
| 反向引用 | `test_source_index.py`、原子切换任务 | 只存计数／文件名、external_group 或未来 terms 消费者漏报、索引单向不等 |
| 复核义务 | `test_source_obligations.py`、`test_check_sources.py` | resolved 重开、义务写正式值、决定变化自动关闭 |
| 六类探测 | `test_probe_sources.py` | urls 证据端点未采集、缺 publisher_version 误报新版、调度边界错误、13 日阻断、误报覆盖旧观察 |
| 身份迁移 | `test_source_migration.py` 的 31／107 测试 | URL 或题名自动归一、16 个歧义消失 |
| 角色迁移 | `test_source_migration.py` 的 47 行测试 | 5 个 candidate 连带批准、空 group 自动批准 |
| 依据迁移 | `test_source_migration.py` 与 `test_build_topics_sources.py` | 630 none、13 self、23 无位置值包装成 basis |
| 派生迁移 | `test_source_migration.py` 的 692／24／8／2 测试 | 数组来源名、项目 self、本地分析冒充派生、旁路数组阻断共享切换 |
| 映射迁移 | `test_source_migration.py` 的 756 行测试 | 748 个 exactMatch 继承、未读材料通过 |
| origin 分流 | `test_source_docs.py` 与 origin 账本测试 | 创建填空 origin、发现线索证明一切 |
| 生成确定性 | `test_build_topics_sources.py`、`test_source_cutover.py` | 重新生成恢复旧结构、重复 ID 静默覆盖 |
| 链接基线 | 4 个阶段回归的直接命令门禁 | 已知退出 1 使后续命令短路、旧失败数量漂移 |
| 双层交付绑定 | `test_source_schema.py`、`test_source_cutover.py` | payload 自引用、handoff 缺富字段、决定未绑定 handoff／payload、ignored 预验改读未来正式 payload、安装后另写第二套 verifier、应用绕过绑定路径 |
| 原子切换与补偿 | `test_source_cutover.py` | 双层 ApplyResult、已存在 output、整提交反转、删除 ID／history／义务、切换即发版 |

## 完成条件

- 每个任务要求的 Q 项都有 accepted patches；推荐或 replacement 都由同一字段物化器消费，未批准任务不产生受跟踪或 ignored 写入。
- 保留的 139 项高风险行为测试均有预期 RED 与 GREEN；不使用 TDD 的任务有直接解析、schema、哈希、差异或端到端证据。14 个任务均有定向检查、写集和回滚证据；离线校验、迁移预演、文档分流和原子切换四个阶段另有完整回归证据，统一写入 ignored `verification.md`。
- 六份迁移账本分别完整覆盖 138、47、1,501、726、756、19 个 identity；每个 identity 只有一个 base row 和一个最终行，每个 `(identity, field)` 最多一个 patch。每份账本分别统计 `mechanically_inherited`、`human_decided` 和 `blocked`；机械继承必须保持旧身份、旧值和旧哈希，不取得新的语义资格。
- `scripts/source_model.py` 公开精确 `ReferenceKind`、`Issue`、`ReferenceUse`、`DecisionPatch` 和 `validate_references()`；`scripts/apply_source_migration.py` 公开唯一 `verify_source_handoff(repo_root, handoff_path, payload_path, candidate_root) -> List[Issue]`。七个 `$id`、26 个错误码和四类角色资格逐字一致，术语侧无需适配器。
- 来源实体、用途角色、`basis`、`source`、`match`、`external_group`、义务和通用反向索引的类型、字段名和枚举与“接口锁”一致；external_group 要求 approved structure 并进入 source use 索引；未来 `vocab/terms.yaml` 夹具无需新增 visitor 即被发现。
- 只读探测的正式写集为零；生产流程从 urls 采集 status／doi／landing／archive／mirror 证据；publisher_version 缺失／相同／不同、1／3／6／12 月调度、24／12／6 月 next_due、30 日宽限、14 日三次独立观察、证据优先级和误报追加均有边界测试。
- 原子切换前 `blocks_cutover` 为 0；切换后严格模式拒绝全部旧来源结构，生成器不会恢复旧值。
- `blocks_cutover` 只统计准备进入正式来源结构却缺少语义材料或决定的行。仅保存旧值审计的 `none`、`self`、旧关系和旧角色不要求人工逐行签字，也不因未取得新效力阻断工具与账本实现。
- 当前 700 个主题概念、24 个数组和所有稳定身份保持不变，或每个变化都引用 accepted DecisionPatch 和迁移账本行；`decision-source-0005` 绑定 handoff path／SHA-256 与 payload path／SHA-256，handoff 提供 topics_sha256。
- payload 在完整 ignored candidate application root 后生成，只列待原子应用路径与 after_sha256，明确排除 payload 与 handoff；handoff 绑定富交付元数据且不含自身 hash。ignored 预验、先行审计安装后验证和正式应用后验证都调用同一四路径 verifier；原子应用按 decision → handoff → payload 顺序验证后只消费 payload entries。
- 两个载体数组隔离为非来源对象，成员不变、local_analysis 不被访问器收集、`blocks_cutover: false`；24 个 external_group 被收集、验证和索引；三份旁路草案不成为前置。
- `scripts/check_link_baseline.py` 以 0 退出验证恰有两条旧 SDD 链接失败，4 个阶段回归门禁均在其后继续执行；31 个标题债务和 8 个只追加旧标题不改。
- 来源改档为 0，术语准入为 0，范围变化为 0；草案生效、迁移、回退和发版分别有决定。
- `decision-source-0004` 至 `0006`、六份账本、ID、history、义务和 manifest 位于切换前先行提交；失败只用 `decision-source-0008` 与补偿提交，保留全部审计对象。
- 原子切换提交完成但没有 `decision-source-0007` 时，状态只能是“已验证，未发版”。
