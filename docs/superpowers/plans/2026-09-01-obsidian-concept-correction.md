# Obsidian 概念纠偏实施计划 (Obsidian Concept Correction Implementation Plan)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 补齐 Obsidian 映射的概念与来源依据，按冻结结论重写设计并修正能力误报，使概念、方法、决定、设计、实现和验证重新一致。

**Architecture:** 先分别冻结 DCMI、Obsidian 和生成 artifact 的来源事实，再建立 Application Profile 与 Reproducible Builds 概念文和方法登记。项目设计采用“应用无关模型—应用约束—Obsidian 表示”三层，导出 artifact contract 独立处理序列化、manifest、完整性和发布；只有概念与 L3 决定闭合后才修改现行设计和代码。

**Tech Stack:** Markdown、Python 3.9.6、PyYAML 6.0.3、JSON、Obsidian Markdown／Bases、`unittest`、Git。

**Spec:** [Obsidian 概念纠偏设计](../specs/2026-09-01-obsidian-concept-correction-design.md)

## 全局约束

- 只在 `/Users/xiu/code/kb-design` 的 `feat/terminology-governance` 分支执行，不创建 worktree，不修改 `master`。
- 概念结论可以推翻现有 Obsidian 设计和实现；不得从当前代码倒推依据。
- DCMI、Obsidian、Reproducible Builds、RFC、W3C、Python／POSIX 来源按各自职责使用，不能互相替代。
- 译名按现行阶梯核对；“应用纲要”未核到 GB/T 正文前只作候选，核不到时保留 `Application Profile`。
- 当前不宣称符合 DCAP、DCAM、DSP、DCTAP、JCS、BagIt、SLSA 或正式 reproducible build。
- 不实现 RDF、SHACL、DCTAP、JCS、BagIt、签名、TUF、fsync 链、内容导出或回流。
- “只读参考区”只表示项目效力和无回流，不表示 Obsidian UI 权限；Bases 可以编辑 properties。
- 旧决定记录不修改；新的 L3 决定必须先形成精确提案，再由用户明确采纳后写入 `design/decisions/`。
- Superpowers 的规格、计划、决定包和审查证据留在 Superpowers 目录，不混入项目正文。
- 文档不为 RED／GREEN 形式新增测试；代码行为不变时复用已有测试。只保留 designation、语义分层、能力误报、生成确定性和安全写入的必要门禁。
- 提交说明按最高决策级别使用 `[L1]`、`[L2]` 或 `[L3]`；不得推送、合并或发版。

---

### Task 1: DCMI 来源

**Files:**

- Create: `sources/dcmi-application-profiles.md`

**Interfaces:**

- Consumes: DCMI Application Profile Guidelines、Singapore Framework、Profile Guidelines、DCAM、DCTAP 及官方规范状态表。
- Produces: Application Profile、DCAP、Functional Requirements、Domain Model、DSP、Usage Guidelines、Encoding Syntax Guidelines、Syntax Encoding Scheme、metadata crosswalk 的来源边界与译名核验结论。

- [ ] **Step 1: 核对官方材料身份**

逐项打开并记录版本、状态、发布日期、已读小节和核对日期：

```text
https://www.dublincore.org/specifications/dublin-core/application-profile-guidelines/
https://www.dublincore.org/specifications/dublin-core/singapore-framework/
https://www.dublincore.org/specifications/dublin-core/profile-guidelines/
https://www.dublincore.org/specifications/dublin-core/abstract-model/
https://www.dublincore.org/specifications/dctap/
https://www.dublincore.org/specifications/dublin-core/
```

正文必须明确 DCMI 当前状态：历史 Recommendation／Note／Draft 只作概念和文档结构依据，不形成 conformance 声明；DCTAP 的 Community Specification 与 Draft 状态分别记录。

- [ ] **Step 2: 核对概念职责**

按下表写入来源笔记，不合并相邻概念：

| Designation | 必须记录 | 反例 |
|---|---|---|
| `Application Profile` | metadata term 选择、约束和应用语境 | 不是两个 schema 的 crosswalk |
| `Functional Requirements` | 支持和排除的功能 | 不是实现清单 |
| `Domain Model` | 被描述对象及基本关系 | 不是 YAML layout |
| `Description Set Profile` | property、resource 和 value 结构约束 | 不处理版本、词汇定义和人读说明 |
| `Usage Guidelines` | application context 中的使用说明 | 不能改变源 term 语义 |
| `Encoding Syntax Guidelines` | 整个 record 的具体语法 | 不是单个值的 datatype |
| `Syntax Encoding Scheme` | 字符串到资源的规则／datatype | 不是 Markdown、YAML 或目录 |
| `metadata crosswalk` | 两个独立 metadata standard／schema／profile 的对应 | 不是 field binding |

- [ ] **Step 3: 核对中文 designation**

读取 GB/T 25100.2―2025 可取得的正式正文或国家标准公开文本，定位 `Application Profile` 对应文字和适用语境。结论只允许二选一：

```text
VERIFIED：正文直接把 Application Profile 称为“应用纲要”，记录标准号、页码／条款和原句位置。
UNVERIFIED：只核到起草稿、参考文献题名或二手论文；项目保留 Application Profile，不登记中文名称。
```

不得把 `Dublin Core Application Profile`、`Description Set Profile`、`Encoding Syntax Guidelines` 或 `metadata crosswalk` 自动套用同一中文译名。

- [ ] **Step 4: 写来源笔记**

`sources/dcmi-application-profiles.md` 使用以下完整结构：

```markdown
# DCMI Application Profiles

## 材料身份
## 阅读范围
## 概念职责
## 分层关系
## 规范状态
## 译名依据
## 项目边界
## 未读范围
## 权威来源
```

“项目边界”必须写明当前 kb-design 只能借用框架，不宣称 DCAP／DCAM／DCTAP conformance；Obsidian field binding 不是 metadata crosswalk。

- [ ] **Step 5: 运行文档检查**

```bash
python3 scripts/check_link_baseline.py
python3 scripts/check-terms.py --all
git diff --check
```

预期：链接基线仍为 `KNOWN_LINK_BASELINE_OK count=2`；术语扫描只生成 `report-only` 线索；差异检查无输出。

- [ ] **Step 6: 提交 DCMI 来源**

```bash
git add sources/dcmi-application-profiles.md
git commit -m "[L1] Obsidian:补充 DCMI 应用来源"
```

### Task 2: Obsidian 来源

**Files:**

- Create: `sources/obsidian-help.md`

**Interfaces:**

- Consumes: Obsidian 官方 data storage、properties、links、aliases、accepted formats、Bases、Bases syntax 和 table view 页面。
- Produces: vault、property、alias、internal link、Base 的官方行为和应用限制；现行映射的事实差异表。

- [ ] **Step 1: 核对官方页面**

逐项打开并记录实际阅读范围：

```text
https://obsidian.md/help/data-storage
https://obsidian.md/help/properties
https://obsidian.md/help/links
https://obsidian.md/help/aliases
https://obsidian.md/help/Files%2Band%2Bfolders/Accepted%2Bfile%2Bformats
https://obsidian.md/help/bases
https://obsidian.md/help/bases/syntax
https://obsidian.md/help/bases/views/table
```

- [ ] **Step 2: 冻结对象边界**

来源笔记必须逐项记录：

```text
vault：本地文件夹；Markdown 纯文本；嵌套 vault 只是官方不建议，不是禁止。
property：YAML frontmatter；官方类型名 Text/List/Number/Checkbox/Date/Date & time/Tags；同名 property 在 vault 内使用同一类型。
nested properties：Obsidian 当前不支持；YAML 本身仍可保存嵌套结构。
alias：aliases YAML list；选择后链接真实文件并使用 alias 作显示文本。
internal link：Wikilink／Markdown link；vault 根路径；悬空链接可能创建文件。
Base：core plugin；读取 Markdown properties；可以查看、筛选、排序和编辑；不是技术只读。
accepted formats：.md 与 .base 在清单内；普通 .json 不作为 Obsidian content format。
```

- [ ] **Step 3: 写设计差异表**

对 `design/targets/obsidian.md` 至少记录四项：

| 现行主张 | 结论 | 纠偏方向 |
|---|---|---|
| “布尔值”是 property type | 不精确 | 官方 type 是 Checkbox，YAML 值为 boolean |
| nested properties 无法表达 | 过强 | 改为 Obsidian 当前不支持 |
| Base 提供只读表格 | 错误 | 改为项目用作浏览入口，但 UI 可以编辑 |
| manifest 是 Obsidian 输出对象 | 需限缩 | 是同目录项目清单，不是 accepted content format |

- [ ] **Step 4: 写来源笔记**

`sources/obsidian-help.md` 使用以下结构：

```markdown
# Obsidian 官方帮助

## 材料身份
## 阅读范围
## 对象边界
## 存储行为
## 属性行为
## 链接行为
## 视图行为
## 格式范围
## 设计差异
## 适用边界
## 未读范围
```

“适用边界”必须明确官方帮助不能决定稳定 ID、正式数据效力、designation 准入、字段基数、导出失败政策、回流、确定性或安全替换。

- [ ] **Step 5: 运行文档检查**

```bash
python3 scripts/check_link_baseline.py
python3 scripts/check-terms.py --all
git diff --check
```

预期与 Task 1 相同；不运行导出测试。

- [ ] **Step 6: 提交 Obsidian 来源**

```bash
git add sources/obsidian-help.md
git commit -m "[L1] Obsidian:补充官方功能来源"
```

### Task 3: 生成来源

**Files:**

- Create: `sources/reproducible-builds.md`
- Create: `sources/rfc-8493.md`
- Create: `sources/rfc-8785.md`
- Create: `sources/w3c-prov.md`
- Create: `sources/python-filesystem.md`

**Interfaces:**

- Consumes: Reproducible Builds definition／deterministic systems、RFC 8493、RFC 8785、W3C PROV-DM、Python JSON、Python `os.replace()`／`fsync()` 和 POSIX rename。
- Produces: 确定性、可重现性、manifest 完整性、provenance、原子可见性与持久性的独立边界。

- [ ] **Step 1: 写 Reproducible Builds 笔记**

`sources/reproducible-builds.md` 必须记录：

```text
reproducible build = same source + environment + instructions -> any party can recreate bit-for-bit identical specified artifacts。
本机同环境双跑一致只证明当前受控环境的确定性，不证明 independent rebuild。
环境变量包括工具版本、locale、timezone、路径、时间、随机数和遍历顺序等可能输入。
当前 Obsidian exporter 不宣称 reproducible build。
```

已读入口：

```text
https://reproducible-builds.org/docs/definition/
https://reproducible-builds.org/docs/deterministic-build-systems/
https://reproducible-builds.org/docs/stable-inputs/
```

- [ ] **Step 2: 写 RFC 8493 笔记**

`sources/rfc-8493.md` 必须区分 payload manifest、tag manifest、complete bag 和 valid bag，并明确本项目没有 `bagit.txt`、`data/` 和 BagIt 文件结构，因此只是项目 manifest。

必须记录 checksum 不能证明 provenance、真实性、审批、语义或可重建性；不引入签名。

- [ ] **Step 3: 写 RFC 8785 笔记**

`sources/rfc-8785.md` 必须逐项记录 JCS 的 I-JSON、ECMAScript primitive serialization、UTF-16 code unit 排序、无 token 间空白和 UTF-8 输出。

加入现实现对照：

```text
Python json.dumps(sort_keys=True, indent=2, ensure_ascii=False)
!= RFC 8785 JCS
```

结论固定为：当前使用参数事实描述，不使用 `canonical JSON` 或 JCS designation。

- [ ] **Step 4: 写 W3C PROV 笔记**

`sources/w3c-prov.md` 必须分别记录 Entity、Activity、Usage、Generation 和 Derivation，并明确：输入被 activity 使用、输出由 activity 生成，不自动证明输入实际影响输出；PROV 表达生成关系，不证明记录真实性、签名、字节确定性或可重建性。

已读入口：

```text
https://www.w3.org/TR/prov-dm/
https://www.w3.org/TR/prov-o/
```

- [ ] **Step 5: 写文件系统笔记**

`sources/python-filesystem.md` 必须记录：

```text
os.replace 成功时是单目录项原子替换；非空目录、权限、平台和跨文件系统可能失败。
原子可见性 != fsync 持久性 != 多文件事务 != 内容正确性。
当前需求只控制生成完成前不可见和失败不覆盖用户目标，不要求掉电持久性。
```

- [ ] **Step 6: 运行来源对账**

检索四份笔记，必须各自出现一条“不能证明”边界：

```bash
rg -n "不能证明|不证明|不等于" \
  sources/reproducible-builds.md \
  sources/rfc-8493.md \
  sources/rfc-8785.md \
  sources/w3c-prov.md \
  sources/python-filesystem.md
python3 scripts/check_link_baseline.py
git diff --check
```

预期：五份文件都有边界；链接基线通过；差异检查无输出。

- [ ] **Step 7: 提交生成来源**

```bash
git add sources/reproducible-builds.md sources/rfc-8493.md sources/rfc-8785.md sources/w3c-prov.md sources/python-filesystem.md
git commit -m "[L1] Obsidian:补充生成完整性来源"
```

### Task 4: 概念方法

**Files:**

- Create: `concepts/application-profile.md`
- Create: `concepts/reproducible-builds.md`
- Modify: `concepts/metadata.md`
- Modify: `concepts/glossary.md`
- Modify: `concepts/README.md`
- Modify: `design/principles.md`

**Interfaces:**

- Consumes: Tasks 1–3 的来源结论和译名结果。
- Produces: 两份概念文、designation 登记、概念索引与方法登记；Task 5 的决定依据。

- [ ] **Step 1: 写 Application Profile 概念文**

文件固定为 `concepts/application-profile.md`。标题按 Task 1 的译名结论二选一：

```markdown
# 应用纲要 (Application Profile)   <!-- 仅 VERIFIED 时 -->
# Application Profile              <!-- UNVERIFIED 时 -->
```

正文必须包含：

```markdown
## 定义
## 解决的问题
## 组成部分
## 相邻概念
## 项目分层
## 适用边界
## 权威来源
```

“相邻概念”逐项反例 Application Profile、crosswalk、field binding、Encoding Syntax Guidelines 和 Syntax Encoding Scheme；“项目分层”导出应用无关模型、应用约束和具体表示，不声称 DCAP conformance。

- [ ] **Step 2: 写 Reproducible Builds 概念文**

文件和标题固定为：

```markdown
# Reproducible Builds
```

没有权威中文 designation 时不补中文名。正文结构：

```markdown
## 定义
## 解决的问题
## 证据层次
## 相邻机制
## 项目用法
## 适用边界
## 权威来源
```

“证据层次”分别写确定性、independent rebuild、manifest/checksum 和 provenance；“项目用法”明确当前只取得同环境双跑证据。

- [ ] **Step 3: 重写元数据应用段**

整节重写 `concepts/metadata.md` 的“在知识库中”：

- 内容模型继续取 Dublin Core 字段；
- 受控字段继续引用正式词表；
- Application Profile 规定应用约束，具体 target 规定 encoding/binding；
- Obsidian properties 或 DITA prolog 不改变字段语义；
- application binding 不是 vocabulary mapping 或 metadata crosswalk。

- [ ] **Step 4: 登记 designation**

在 `concepts/glossary.md` 新建“应用与生成”节。Application Profile 行按译名结果二选一；Reproducible Builds 保留英文：

```markdown
| 应用纲要 | Application Profile | 为特定应用规定 metadata term、约束、使用与编码语法的文档集合 | GB/T 25100.2―2025；DCMI Singapore Framework |
| Application Profile | Application Profile | 为特定应用规定 metadata term、约束、使用与编码语法的文档集合 | DCMI Singapore Framework；中文查无高阶正文依据 |
| Reproducible Builds | Reproducible Builds | 使任何一方在相同 source、environment 和 instructions 下重建逐字节相同 artifacts 的实践 | Reproducible Builds definition |
```

只能写入 Application Profile 两行中的一行。不得登记 JCS、BagIt、crosswalk 或中文自译。

- [ ] **Step 5: 同步概念索引与方法登记**

在 `concepts/README.md` 登记两份概念文。在 `design/principles.md` 登记两种方法：

```text
Application Profile：从 metadata／应用需求导出功能范围、模型引用、字段约束、使用指南和 encoding；不产生 DCAP conformance。
Reproducible Builds：从 source／environment／instructions／artifact 导出确定性与可重建证据边界；当前只使用它限制完成声明。
```

方法行必须链接概念文和 Tasks 1–3 的来源笔记，不能只链接 Obsidian 目标设计。

- [ ] **Step 6: 运行概念门禁**

```bash
python3 scripts/check-terms.py --all
python3 scripts/check_link_baseline.py
git diff --check
```

再人工对账：概念文中的每条规则能指向来源笔记；glossary 没有同时登记两个 Application Profile 译名分支；`design/principles.md` 没有 conformance 主张。

- [ ] **Step 7: 提交概念方法**

```bash
git add concepts/application-profile.md concepts/reproducible-builds.md concepts/metadata.md concepts/glossary.md concepts/README.md design/principles.md
git commit -m "[L2] Obsidian:建立应用与生成概念"
```

### Task 5: 决定提案

**Files:**

- Create: `.superpowers/sdd/2026-09-01-obsidian-concept-correction/decision-proposal.md`

**Interfaces:**

- Consumes: Task 4 的概念文和方法登记。
- Produces: 可由用户逐项批准的 L3 决定文本；Task 6 的唯一人工门禁。

- [ ] **Step 1: 写决定提案**

提案必须包含下列精确决定：

1. 保留应用无关内容模型；每个 target 另写功能范围、模型引用、字段约束、使用指南和具体表示。
2. Obsidian field/property/path 关系称普通 binding／表示规则，不称 metadata crosswalk。
3. 导出 artifact contract 与 Application Profile 分开，负责输入、序列化、manifest、校验和发布。
4. target 文件存在不等于内容消费者启用；引用统计和回流须等待真实消费者。
5. 生成文件可以在 Obsidian 中编辑，但修改不回流、不取得项目效力。
6. 当前不宣称 DCAP、DCTAP、JCS、BagIt 或 reproducible build conformance。
7. `design/decisions/form-independence.md` 的核心分层继续有效；新决定补充应用约束和消费者门禁，不修改旧文件。

提案同时列出受影响文件、保持不变的正式数据、负面后果和不采用后果。

- [ ] **Step 2: 做语义自审**

逐项核对：

```text
没有采用未登记 designation。
没有把 source note 变成规则。
没有宣称真实内容消费者存在。
没有修改正式词表或 glossary 编辑权。
没有要求无消费者的标准实现。
```

- [ ] **Step 3: 请求 L3 决定**

向用户展示决定正文和影响文件，只接受“采纳”“修改后采纳”或“不采纳”。在用户明确回复前停止 Task 6，不创建 `design/decisions/application-profile-boundary.md`，不修改现行设计。

### Task 6: 设计重写

**Files:**

- Create: `design/decisions/application-profile-boundary.md`
- Rewrite: `design/targets/obsidian.md`
- Modify: `design/content-model.md`
- Modify: `design/governance.md`
- Modify: `design/maintenance.md`
- Modify: `design/hierarchy.md`
- Modify: `design/drafts/facet-field.md`
- Modify: `design/README.md`
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `docs/superpowers/plans/2026-08-31-project-roadmap.md`

**Interfaces:**

- Consumes: 用户采纳的 Task 5 决定、Task 4 的概念与方法。
- Produces: 已采纳 ADR、三层 Obsidian 设计和全部当前态入口。

- [ ] **Step 1: 写已采纳决定**

只有 Task 5 获得明确“采纳”后，创建 `design/decisions/application-profile-boundary.md`：

```markdown
# 应用约束与表示分层

状态：已采纳，2026-09-01。

## 背景
## 决定
## 后果
```

“决定”逐字覆盖 Task 5 的七项；“后果”明确旧 `form-independence` 决定不修改、内容消费者仍不存在、正式数据和术语编辑权不变。

- [ ] **Step 2: 整篇重写 Obsidian 设计**

`design/targets/obsidian.md` 使用以下稳定结构：

```markdown
# Obsidian 映射
## 功能范围
## 效力边界
## 模型引用
## 字段约束
## 文件布局
## Obsidian 表示
## 词表表示
## 内容表示
## 引用语法
## 表达缺口
## 浏览入口
## 导出合同
## 清单边界
## 发布边界
## 回流边界
## 验收门禁
## 待定事项
## 权威来源
```

必须修正 Checkbox、nested properties、Base 可编辑性、`.json` format 边界、`canonical JSON`、BagIt／JCS／reproducible claim 和原子可见性。保留当前字段、路径、对象类型、计数动态性、内容未实现和无回流边界。

- [ ] **Step 3: 重写应用接口**

整节重写 `design/content-model.md` 的“应用映射”：

- 保留原五问作为操作检查；
- 增加 Functional Requirements、Domain Model reference、field constraints、usage 和 encoding syntax 的上层结构；
- 明确 target binding 不能修改字段语义；
- 明确 mapping 文件存在不等于消费者启用。

同步 `design/governance.md` 的对象范围、变更控制和应用映射验收；新 target 必须引用概念文、方法登记和决定。

- [ ] **Step 4: 同步关联设计**

按新决定整节重写受影响部分：

```text
maintenance：内容计数仍等待真实消费者，不把 profile 文件当运行记录。
hierarchy：Obsidian 保留全部 broader，不选择主上位。
facet-field：Application Profile 存在，但没有分面查询消费者；草案保持未生效。
```

不修改正式数据、阈值、范围和草案状态。

- [ ] **Step 5: 同步入口**

同步 `design/README.md`、`README.md`、`AGENTS.md` 和项目路线：

- 登记两份新概念文、方法和决定；
- Obsidian 状态写为“概念纠偏完成，词表导出保留”；
- 内容消费者、回流、正式激活和 TBX 继续后置；
- 不复制易漂移文件计数。

- [ ] **Step 6: 运行设计门禁**

```bash
python3 scripts/check_link_baseline.py
python3 scripts/check-terms.py --all
git diff --check
rg -n "canonical JSON|只读表格|Base 只是浏览视图|应用映射为 0|首个应用映射落地前" \
  README.md AGENTS.md concepts design --glob '*.md'
```

预期：前三项通过；最后检索只允许概念或来源中的反例说明，不得命中现行能力主张。

- [ ] **Step 7: 提交设计重写**

```bash
git add design/decisions/application-profile-boundary.md design/targets/obsidian.md \
  design/content-model.md design/governance.md design/maintenance.md design/hierarchy.md \
  design/drafts/facet-field.md design/README.md README.md AGENTS.md \
  docs/superpowers/plans/2026-08-31-project-roadmap.md
git commit -m "[L3] Obsidian:按概念重写应用设计"
```

### Task 7: 实现纠偏

**Files:**

- Modify: `scripts/export_obsidian.py`
- Modify: `docs/superpowers/specs/2026-09-01-obsidian-export-design.md`

**Interfaces:**

- Consumes: Task 6 的导出合同。
- Produces: `_deterministic_json(document: Mapping[str, Any]) -> bytes`；行为不变的 JSON 字节；准确的验证错误和历史规格状态。

- [ ] **Step 1: 运行现有行为基线**

```bash
PYTHONPYCACHEPREFIX=/tmp/kb-design-pycache \
  python3 -m unittest tests.test_export_obsidian -v
```

预期：17 项全部通过。此任务不新增测试，因为序列化字节、manifest schema、文件集合和 CLI 行为均不改变，现有端到端测试已经覆盖。

- [ ] **Step 2: 修正代码 designation**

在 `scripts/export_obsidian.py` 做三处机械重命名：

```python
def _deterministic_json(document: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    ).encode("utf-8")
```

- `_canonical_json` → `_deterministic_json`；
- 两个调用点同步；
- `manifest is not canonical JSON` → `manifest does not use the required deterministic JSON serialization`。

不得修改 `json.dumps()` 参数、manifest schema、hash 或文件内容。

- [ ] **Step 3: 标明历史规格状态**

在 `docs/superpowers/specs/2026-09-01-obsidian-export-design.md` 标明：

```text
状态：历史实施规格。概念和能力主张由 2026-09-01-obsidian-concept-correction-design.md 纠正；实现字段与测试证据继续作为历史输入。
```

历史正文中的 `canonical JSON` 保留为被纠正的原主张，不把历史规格静默改写成新设计。

- [ ] **Step 4: 运行实现回归**

```bash
PYTHONPYCACHEPREFIX=/tmp/kb-design-pycache \
  python3 -m unittest tests.test_export_obsidian -v
PYTHONPYCACHEPREFIX=/tmp/kb-design-pycache \
  python3 -m py_compile scripts/export_obsidian.py tests/test_export_obsidian.py
git diff --check
```

预期：17 项通过，编译通过，差异检查无输出。

- [ ] **Step 5: 提交实现纠偏**

```bash
git add scripts/export_obsidian.py docs/superpowers/specs/2026-09-01-obsidian-export-design.md
git commit -m "[L2] Obsidian:修正导出能力名称"
```

### Task 8: 阶段验收

**Files:**

- Create: `.superpowers/sdd/2026-09-01-obsidian-concept-correction/final-review.md`

**Interfaces:**

- Consumes: Tasks 1–7 的全部提交。
- Produces: 当前 Obsidian 阶段的 `PASS`、`PASS_WITH_KNOWN_ISSUES` 或 `WITHDRAWN` 结论及证据。

- [ ] **Step 1: 运行最终回归**

```bash
PYTHONPYCACHEPREFIX=/tmp/kb-design-pycache \
  python3 -m unittest tests.test_export_obsidian -v
python3 scripts/check_link_baseline.py
python3 scripts/check-terms.py --all
git diff --check
```

预期：17 项通过；链接基线仍为 2 个既有 Superpowers 审计链接；术语为 report-only；差异检查无输出。

- [ ] **Step 2: 运行双导出**

使用两个新的 `/tmp` 目标运行：

```bash
python3 scripts/export_obsidian.py --repo-root . --output /tmp/kb-obsidian-concept-final-a
python3 scripts/export_obsidian.py --repo-root . --output /tmp/kb-obsidian-concept-final-b
diff -ru /tmp/kb-obsidian-concept-final-a /tmp/kb-obsidian-concept-final-b
```

预期：两次命令成功；`diff` 无输出；manifest 报告相同 `content_sha256`。若固定路径已存在，先选择新的带随机后缀目录，不删除已有用户目录。

- [ ] **Step 3: 做语义复审**

只安排一次独立复审，回答：

```text
concepts 是否由 sources 推出；
译名是否按阶梯登记；
Application Profile、binding 和 crosswalk 是否分开；
确定性、reproducibility、manifest、provenance 和 atomicity 是否分开；
Base 可编辑性、nested properties 和 JSON 表示是否准确；
L3 决定、现行设计和实现是否一致；
正式数据、草案、术语编辑权和消费者状态是否未被误改。
```

机械计数、测试、hash 和写集不交给第二代理重复确认。

- [ ] **Step 4: 写最终结论**

`.superpowers/sdd/2026-09-01-obsidian-concept-correction/final-review.md` 使用：

```markdown
# Obsidian 概念纠偏验收

## 结论
## 概念证据
## 设计一致性
## 实现证据
## 已知边界
## 后置事项
```

结论规则：

```text
PASS：概念、决定、设计、实现一致，只有明确后置的内容消费者／回流／正式激活。
PASS_WITH_KNOWN_ISSUES：仍有不影响当前词表导出的已知问题，逐项列出。
WITHDRAWN：概念结论否定现行核心映射或实现，停止宣称阶段完成。
```

- [ ] **Step 5: 核对分支状态**

```bash
git status --short --branch
git log --oneline -10
```

预期：工作区干净，分支仍为 `feat/terminology-governance`。不提交 ignored Superpowers 验收文件，不推送、不合并、不发版。
