# Obsidian 映射

本文是 Obsidian target 的现行 `Application Profile` 与导出 artifact contract。它按[内容模型](../content-model.md)引用应用无关语义，规定 Obsidian 表示的语义选择，再单独规定所选表示怎样物化为文件。分层依据见 [Application Profile](../../concepts/application-profile.md)、[Reproducible Builds](../../concepts/reproducible-builds.md)、[方法登记](../principles.md)和[应用约束与表示分层](../decisions/application-profile-boundary.md)。

当前实现只把六份正式词表生成成单向词表参考区。内容表示只有未来应用必须遵守的约束；仓库没有知识库内容、内容导出器、内容校验器、检索记录或回流接口。

## 功能范围

当前 `Application Profile` 支持用户浏览、链接和筛选正式词表表示。

- 浏览正式对象的稳定身份、显示形式、状态、关系、范围与依据表示；
- 沿 Wikilink 查看上位、相关、数组成员、实体和来源用途之间的正式引用；
- 通过 Base 按既定 properties 排序和筛选正式词表表示；
- 为未来内容应用规定字段位置、target type、reference form、受控值引用、使用条件和允许的 loss。

未来内容 binding 只规定应用语义。当前没有内容消费者，不生成或读取知识库内容，不执行内容查询、引用统计、未匹配检索统计或回流。

生成文件、确定 file set、写入项目 manifest、post-generation validation 和 publication 不属于本节的应用功能，只由“导出合同”和“发布边界”规定。导入、既有 vault 合并、来源或术语正式激活、TBX，以及 DCAP、DCTAP、JCS、BagIt 或 reproducible build conformance 也不在当前功能范围内。

## 效力边界

- `vocab/topics.yaml`、`vocab/entities.yaml`、`vocab/sources.yaml`、`vocab/types.yaml`、`vocab/genres.yaml` 和 `vocab/forms.yaml` 是导出的正式输入。
- `vocab/topics.yaml` 的编辑路径仍由[主题词表设计](../topics.md)规定；其他正式词表仍按各自设计维护。
- 生成的 Markdown、Base、README 和项目 manifest 可以被文件系统工具或 Obsidian 编辑，但都不是正式词表、术语表、迁移账本或新的编辑源。
- 导出器不读取生成目录中的修改。修改不会回流本仓库，不取得 designation、概念、关系、状态或项目决定的效力；再次导出可以覆盖修改。
- 导出器不读取来源与术语迁移账本、候选记录、未激活模式、草案、诊断报告或 Superpowers 过程文件。
- `concepts/glossary.md` 继续承担 designation 与中英对照的现行编辑权；正式术语数据尚未激活。

## 模型引用

本 target 引用[内容模型](../content-model.md)的内容单元、字段语义、受控值、标识符和生命周期，引用[主题词表设计](../topics.md)、[命名实体词表设计](../entities.md)与[来源名称规范表](../sources-registry.md)的正式对象，并引用[层级结构](../hierarchy.md)的多上位和数组规则。

`Application Profile` 只为这些既定对象选择 Obsidian location、type、reference form 和允许的 loss。field／property／path binding 是同一应用内部的表示规则，不是 `metadata crosswalk`；它也不改变词表层 `crosswalk` 对概念映射的现行含义。

target binding 不得修改字段语义、基数、值域、稳定身份、对象关系或正式词表身份。Obsidian 无法直接支持某项约束时，应用保留并校验该约束，或把不能无损进入 property 的信息移到正文；不得通过放宽内容模型、改成自由 tag 或自动建立概念来绕过。

## 字段约束

每篇词表对象笔记使用下列公共 properties；不存在的值省略，不写空字符串、空列表或 `null`。

| Property | Obsidian type | 取值 |
|---|---|---|
| `kb_id` | Text | 正式稳定 ID |
| `kb_object` | Text | `topic`、`array`、`entity`、`source`、`type`、`genre` 或 `form` |
| `kb_label` | Text | 中文标签、英文标签、ID 的固定回退结果 |
| `kb_status` | Text | 正式记录已有的状态 |
| `kb_version` | Text | 所属正式词表的版本 ID |
| `aliases` | List | 正式 `label`、`alt` 和 `hidden` 中除显示形式外的非空形式 |
| `tags` | Tags | `kb-design/<object>` |

`aliases` 只保存正式数据中已经存在的形式，不翻译、不补名、不规范化出新形式。选择 alias 建立链接时，真实目标仍是稳定 ID 对应的文件。

当前词表表示使用 Text、List、Date 和 Tags。若未来选择 Checkbox，YAML 值必须是 `true` 或 `false`；Checkbox 是 Obsidian type，boolean 是其 YAML 值形态。相同 property name 在一个 vault 中必须保持同一 Obsidian type。

## 文件布局

导出目录使用固定路径。

```text
README.md
manifest.json
KB/
  Topics/
  Arrays/
  Entities/
  Sources/
  Types/
  Genres/
  Forms/
  Views/
    Topics.base
    Entities.base
    Sources.base
```

对象文件名为 `<id>.md`。标签、别名和译名变化不改路径。内部链接从 vault 根开始并使用正斜线。`manifest.json` 与 Obsidian 文件同目录发布，但普通 `.json` 不在 Obsidian accepted content formats 中；该文件是项目清单，不是 Obsidian 内容对象。

## Obsidian 表示

对象笔记使用 UTF-8 Markdown。一级标题保存显示标签；YAML frontmatter 保存可平坦表达并用于查询的 properties；范围、形式依据、归属依据、外部映射和历史记录进入正文。

Obsidian 当前不支持 nested properties，但 YAML 本身能够保存嵌套结构。本 target 为了应用编辑和查询兼容性，不在 properties 中选择嵌套值；列表元素也只使用 scalar。不能平坦表达的正式结构进入正文表格或 YAML 代码块，内容仍来自正式输入。

`.base` 文件使用 YAML 保存 filters 和 table view。`.md` 与 `.base` 是 Obsidian 支持的内容格式；项目 manifest 的 `.json` 格式只服务导出校验。

## 词表表示

正式对象按下列规则生成。引用单值使用 Text link，引用多值使用由 Text link 组成的 List；日期使用 Date，其他已有 scalar 使用 Text。`kb_creator`、`kb_broader`、`kb_related`、`kb_arrays`、`kb_subjects`、`kb_members` 和 `kb_roles` 是 List；`kb_added` 与 `kb_checked` 是 Date；其余专有 properties 是 Text。不存在的可选值仍省略。

| 对象 | 路径 | 专有 properties | 正文保留 |
|---|---|---|---|
| 主题 | `KB/Topics/<id>.md` | `kb_broader`、`kb_related`、`kb_arrays`、`kb_source`、`kb_added`、`kb_replaced_by` | 范围、替代形式、隐藏形式、形式依据、外部映射、历史记录 |
| 主题数组 | `KB/Arrays/<id>.md` | `kb_superordinate`、`kb_source`、`kb_members` | 数组的分组职责 |
| 实体 | `KB/Entities/<id>.md` | `kb_kind`、`kb_subjects`、`kb_vendor`、`kb_creator`、`kb_replaced_by`、`kb_form`、`kb_tier`、`kb_url`、`kb_watch`、`kb_checked`、`kb_added`、`kb_entity_version` | 范围、归属依据、外部映射、历史记录 |
| 来源用途 | `KB/Sources/<id>.md` | `kb_entity`、`kb_roles`、`kb_checked` | 来源用途与来源实体身份的区别 |
| 文档类型 | `KB/Types/<id>.md` | `kb_broader`、`kb_related`、`kb_arrays`、`kb_source`、`kb_added`、`kb_replaced_by` | 范围、已有形式、依据、映射和历史 |
| 体裁 | `KB/Genres/<id>.md` | 同文档类型 | 范围、已有形式、依据、映射和历史 |
| 载体 | `KB/Forms/<id>.md` | 同文档类型 | 范围、已有形式、依据、映射和历史 |

数组成员从正式主题记录反向构造，并保持正式主题记录顺序。主题数组只表达树内分组，不取得主题概念、分面或手工概念组的效力。

`forms.yaml` 中的载体数组不生成另一类对象笔记。导出根 README 逐项保存其 ID、上位根和来源；每篇载体笔记保存已有数组 ID。该表示保留正式值，不制造第八种对象。

## 内容表示

内容单元不由当前导出器生成。真实知识库应用将来创建 Obsidian 内容笔记时，必须按下表 binding，不得用文件名、标题、alias、tag、反向链接或文件时间替代内容模型字段。

| 内容字段 | Obsidian 表示 |
|---|---|
| `identifier` | `kb_id` Text；稳定值由知识库应用提供 |
| `title` | 一级标题；需要查询时同时保存 `title` Text |
| `type` | `kb_type` Text link，指向 Types |
| `genre` | `kb_genre` Text link，指向 Genres |
| `form` | `kb_form` Text link，指向 Forms |
| `level` | `kb_level` Text，保持内容模型的正式值 |
| `subject` | `kb_subjects` List，指向 Topics |
| `entities` | `kb_entities` List，指向 Entities |
| `source` | `kb_source` Text link，按内容模型识别内容单元或实体目标 |
| `references` | `kb_references` List，指向作为文献或标准的 Entities |
| `created` | `kb_created` Date |
| `modified` | `kb_modified` Date |
| `status` | `kb_status` Text |
| `isReplacedBy` | `kb_is_replaced_by` Text link，指向内容笔记 |
| `relation` | `kb_relation` List，指向内容笔记 |
| `language` | `kb_language` Text；默认 `zh` 时可以省略 |
| 正文 | frontmatter 后的 Markdown 正文 |

应用必须校验恰好一个 `type`、恰好一个 `genre`、至少一个 `subject`、受控值目标、内容单元引用和生命周期约束。当前没有实现这些内容接口；本节不构成消费者启用或运行证据。

## 引用语法

所有对象引用都以目标稳定 ID 计算路径，以目标正式标签计算显示文本。

```md
[[KB/Topics/security|安全]]
```

显示文本缺少中文时使用英文，两者都缺少时使用 ID。显示文本不参与目标解析。主题层级、相关关系、数组成员、实体关系和来源用途必须解析到已生成目标；悬空引用阻断整个导出。

property 中的链接整体按 YAML 字符串保存。Text 和 List property 中的内部链接加引号。本 target 不使用标题引用或块引用，避免把可变正文位置当作身份。

## 表达缺口

正式记录中的 `basis`、`match` 和 `history` 含嵌套结构，Obsidian 当前不支持把它们作为 nested properties 编辑和查看，因此进入正文表格或 YAML 代码块；`scope`、替代形式和隐藏形式也进入正文。该 loss 只发生在可查询 property 结构上，信息本身仍写入生成笔记；正文不替代正式 YAML 的编辑权。

当前导出器对每类正式记录使用显式允许字段表。遇到未知字段、非法 ID、重复 ID、无法解析的引用、重复输出路径或不能安全序列化的值时，导出失败；它不把未知值放入兜底字段，也不丢弃后继续生成。

内容应用以后遇到 Obsidian 不能表达的约束时，必须在应用校验器中保留约束并阻断无效内容。

## 浏览入口

导出器生成 Topics、Entities 和 Sources 三个 `.base` 文件。每个 Base 用 `file.inFolder()` 和 Markdown 扩展名收窄默认数据集，并提供 table view；当前不使用 formulas、反向链接聚合、插件视图或自动写回动作。

Base 是可编辑界面。Obsidian 可以通过 table view 编辑文件和 properties；本项目只把这些 Base 用作浏览、排序和筛选入口。经 Base 发生的修改与直接编辑 Markdown 一样，不回流本仓库、不取得项目效力，并可能在重新导出时被覆盖。删除或修改 `.base` 文件不改变正式数据，但经 Base 修改对象笔记会改变该份生成目录中的本地文件。

当前验收只证明 `.base` 按现行生成规则产生并可解析为 YAML，没有证明在 Obsidian 应用内完成交互测试。

## 导出合同

导出 artifact contract 从 `Application Profile` 完成语义选择后开始，只负责把已选表示由输入快照确定性物化为 bytes、文件集合和可校验发布物。它不得改变 field 的 target location、type、reference form 或允许的 loss。

现行物化规则包括：

- 一次读取六份正式输入的原始 bytes，同一快照同时用于内容和 manifest；
- 按对象稳定 ID 和固定路径排序生成文件，数组成员保持正式记录顺序；
- Markdown、Base 和 JSON 使用 UTF-8，生成文本使用 LF，生成文件以换行结束；
- frontmatter 的 property 顺序由生成器固定，字符串按 JSON quoting 写入 YAML scalar，列表逐项写入；
- Base 由固定 mapping 顺序生成 YAML；
- 项目 manifest 使用 `json.dumps(ensure_ascii=False, indent=2, sort_keys=True)` 并以换行结束；
- 全部文件写入后回读，完成 post-generation validation，再进入发布步骤。

同一受控 source 和当前 environment 下的双跑逐字节一致，只证明现行条件下的 deterministic behavior。项目没有发布可供任何一方独立重建的完整 environment 与 instructions，也没有 independent rebuild 证据，因此不宣称 reproducible build。

固定 JSON 参数不满足 JCS 的全部条件。现行 pretty-printed JSON 有 token 间 whitespace，且没有证明 I-JSON、ECMAScript primitive serialization 或 UTF-16 code unit 排序；当前不宣称 JCS conformance。

## 清单边界

`manifest.json` 是项目 manifest，保存：

- schema 名称与版本；
- 六份正式输入的路径、版本和 SHA-256；
- 导出器 bytes 的 SHA-256；
- 各正式对象种类的动态计数；
- 除 manifest 自身外，每个生成文件的相对路径、对象种类、输出标识和 SHA-256；
- 内容文件数、包含 manifest 的总文件数和内容集合 SHA-256。

正式对象的输出标识是稳定 ID；README 与 Base 使用文件 stem 作为 manifest 内部标识。manifest 不保存生成时间、绝对路径、用户名、输出目录或 mtime，也不把自身列入文件条目和内容集合 hash。

项目 manifest 的双向文件覆盖和 checksum 只证明当前目录中的已列 bytes 与记录一致。输出没有 `bagit.txt`、`data/`、payload manifest 或 tag manifest，不是 BagIt bag，也不宣称 BagIt conformance。checksum 不证明 provenance、真实性、审批、语义正确性或可重建性。

## 发布边界

从仓库根运行：

```bash
python3 scripts/export_obsidian.py --repo-root . --output /absolute/new/path
```

输出目录必须不存在或为空。导出器拒绝符号链接、仓库根、文件系统根、用户主目录和仓库中的正式数据、设计、概念、来源、脚本与测试目录；它不提供覆盖非空目录、合并现有 vault 或删除旧目录的参数。

全部文件先写入目标同级的新临时目录，再回读并校验文件集合、逐文件 hash、Markdown frontmatter、Base YAML、内部链接和 manifest 双向覆盖。校验通过后，导出器以 `os.replace()` 尝试把临时目录放到目标目录项；失败时只删除本次创建的临时目录，不递归删除用户目标。

`os.replace()` 成功只提供目标目录项的 atomic visibility：观察者不会看到发布步骤的中间目录项状态。它可能因平台、权限、非空目标或跨文件系统等条件失败；当前实现没有 file 或 directory `fsync`，不提供 durability、掉电恢复、多文件事务、并发协调或内容正确性保证。

成功时标准输出是一行排序 JSON，只含 `output`、`content_files`、`total_files` 和 `content_sha256`。参数错误、输入错误或写入错误时，标准错误以 `OBSIDIAN_EXPORT_ERROR` 开头并退出 `1`；`--help` 正常退出 `0`。

导出目录可以作为独立 vault，也可以在人工核对项目 manifest 后复制到现有 vault 的一个管理目录。更新已有参考区时应导出到另一个新目录、核对项目 manifest，再由人决定替换旧目录。

## 回流边界

当前没有回流接口。人工直接或经 Base 修改导出笔记中的 properties、正文、aliases、链接、文件名或 `.base`，都不会写回本仓库，也不取得项目效力；下次导出不读取这些修改。

未来回流必须另行设计，并至少保存 vault 文件、位置和上下文，读取稳定 `kb_id`，区分用户正文与生成表示，报告差异，把未解析字符串交人工，分别完成概念、designation、权限和来源判断。它不得从文件名、alias、tag、链接或反向链接自动创建记录、关系或状态。

target 文件、内容字段契约、生成目录或 Base 存在都不等于真实内容消费者启用。引用次数和未匹配检索次数必须等待消费者提供可审计的内容与检索记录。

## 验收门禁

本映射保留下列具有独有风险证据的验收。

- `Application Profile` 的功能范围、模型引用、字段约束、使用条件和 encoding 与内容模型一致；target binding 没有改写字段语义。
- 每个正式对象恰有一条稳定路径，全部正式引用都有生成目标，全部 `broader` 均被保留。
- properties 可由安全 YAML 解析且只有 scalar 或 scalar list；正文完整保存未进入 properties 的嵌套数据。
- aliases 只来自正式已有形式，没有新增名称或译名。
- 项目 manifest 与生成目录双向一致，并证明生成内容和 manifest 使用同一输入快照。
- 相同输入在同一受控环境中的两个独立导出目录逐字节一致；该证据只支持确定性。
- 非空目标、符号链接、目录替换失败和写后回读失败不损坏用户目标；成功替换只宣称 atomic visibility。
- 正式词表、术语编辑权、内容模型、草案状态和发版状态不因导出或 Obsidian 编辑改变。
- 能力说明不宣称 DCAP、DCTAP、JCS、BagIt 或 reproducible build conformance。

机械计数和 hash 由导出器、测试及一次端到端导出证明，不另交第二代理重复确认。内容表示只有真实知识库消费者实现后，才能验收内容生成、引用统计和回流。

## 待定事项

- 真实知识库内容目录、文件布局和调用方出现后，实现并校验内容表示、使用指南和消费者接口。
- 只有回流需求出现后，另行设计上下文保存、差异报告、人工判断和权限门禁。
- 若未来需要 reproducible build 主张，另行界定 specified artifacts、source、environment 和 instructions，并取得 independent rebuild 证据。
- 若未来需要 durability，另行设计 file 与 directory `fsync`、故障模型和恢复验证；不从当前原子可见性推导。
- TBX 只按[未生效草案](../drafts/tbx-export.md)中的真实接收方条件重新进入设计。

## 权威来源

- [Application Profile](../../concepts/application-profile.md)：功能范围、模型、字段约束、使用指南、encoding 和 target binding 的分层。
- [Reproducible Builds](../../concepts/reproducible-builds.md)：确定性、独立重建、manifest、JCS、BagIt、原子可见性和 durability 的边界。
- [应用约束与表示分层](../decisions/application-profile-boundary.md)：本 target 的已采纳职责、消费者、编辑效力和符合性边界。
- [设计与应用分离](../decisions/form-independence.md)：应用无关模型与 target 分离、正式词表单向导出的现行决定。
- [Obsidian 官方帮助阅读笔记](../../sources/obsidian-help.md)：vault、properties、Checkbox、nested properties、links、aliases、accepted formats 和 Bases 行为。
- [DCMI Application Profiles 阅读笔记](../../sources/dcmi-application-profiles.md)：Application Profile 组件、`metadata crosswalk`、历史材料状态与项目边界。
- [Reproducible Builds 阅读笔记](../../sources/reproducible-builds.md)：确定性与 reproducible build 的证据边界。
- [BagIt 文件包格式阅读笔记](../../sources/rfc-8493.md)：项目 manifest 与 BagIt 的边界。
- [RFC 8785 阅读笔记](../../sources/rfc-8785.md)：现行 JSON 参数与 JCS 条件的差异。
- [Python 文件系统阅读笔记](../../sources/python-filesystem.md)：`os.replace()`、atomic visibility、`fsync` 与 durability 的边界。
