# 生成基线

本报告在 `feat/terminology-governance` 分支的 `9e7b411c23e890d13d70fc16d443b760313126c4` 上复现现行术语表、主题词表及其构建和校验链。报告只记录当前事实与已批准草案的未来边界，不修改脚本、生成输入或正式输出。

## 基线边界

本次读取了[实施准备计划](../../../docs/superpowers/plans/2026-08-31-governance-implementation-prep.md)、[来源治理草案](../../../design/drafts/source-governance.md)、[术语治理草案](../../../design/drafts/terminology-governance.md)、[术语治理设计](../../../docs/superpowers/specs/2026-08-27-terminology-governance-design.md)，以及生成链直接引用的现行设计、概念文、来源笔记、数据、脚本和测试。

本次没有使用新的外部事实，也没有重新解释标准正文。未来边界只引用已批准草案已经提出的 `basis`、`source`、`match`、`vocab/terms.yaml`、`term_concept`、工作流状态和术语管理状态；具体模式版本、标识格式、周期、阈值、正式文件位置和迁移范围继续待人决定。

基线环境如下。

| 项目 | 当前值 |
|---|---|
| 分支 | `feat/terminology-governance` |
| HEAD | `9e7b411c23e890d13d70fc16d443b760313126c4` |
| Python | `3.9.6` |
| PyYAML | `6.0.3` |
| 正式写集 | 无 |
| 本任务写集 | 本报告 |

## 当前链路

现行两条链路的职责不同。

| 对象 | 当前编辑位置 | 当前处理 | 当前输出或报告 |
|---|---|---|---|
| 术语表 | [concepts/glossary.md](../../../concepts/glossary.md) | 人工直接编辑；[check-terms.py](../../../scripts/check-terms.py) 读取全部 Markdown 表格前两列，并与三个词表的标签合并后扫描正文 | 标准输出中的待人工判断字符串；没有术语表生成器或结构校验器 |
| 主题词表 | [vocab/build](../../../vocab/build) 与 [build-topics.py](../../../scripts/build-topics.py) | 构建脚本读取固定输入并覆盖 `vocab/topics.yaml` | [vocab/topics.yaml](../../../vocab/topics.yaml) |
| 词表校验 | 六份现行词表及 `signals.yaml` | [check-topics.py](../../../scripts/check-topics.py) 读取并校验，同时输出指标 | 标准输出；只有传入 `--record` 才改写 `signals.yaml` |
| 链接校验 | 全库 Markdown | [check-links.py](../../../scripts/check-links.py) 检查相对文件和标题锚点 | 标准输出 |

`vocab/terms.yaml` 当前不存在，`term_concept` 当前也没有进入正式词表数据。现行主题词表构建器不读取术语表，现行术语识别器不生成术语表或主题词表。

## 输入清单

主题词表构建器实际读取下列输入。数量来自逐项解析，不以目录名或字符串命中推断用途。

| 输入 | 当前内容 | 生成用途 |
|---|---:|---|
| `cs2023-kus.json` | 17 个知识领域、161 个知识单元 | 建立 `computing` 下的来源结构 |
| `cs2023-zh.json` | 178 个键 | 为上述 17 个知识领域和 161 个知识单元提供现行输入形式；键集合完整 |
| `extra-arrays.json` | 4 个上位、7 个来源数组、90 个条目 | 建立现行额外来源数组；全部条目进入构建 |
| `gbt-13745.json` | 7 个顶层输入、86 个二级条目、351 个三级条目 | 构建器只读取 110、120、630、740、860、880 六支的 385 个二三级条目；520 支的 52 个条目不进入当前输出 |
| `gbt_en.py` | 380 个显式中英映射及“其他学科”回退函数 | 为上述六支 385 个条目提供英文输入；当前无未解析项 |
| 构建器内的 870 清单 | 5 个二级条目、37 个三级条目 | 建立图书馆、情报与文献学分支；该清单不在 JSON 中 |
| `label-decisions.json` | 85 项决定，72 项采纳、13 项否决 | 处理查到的译名回查结果；缺少决定的回查项按现行脚本不译 |
| `scope-zh.json` | 253 个键 | 当前 240 个键为缺少中文标签的记录提供 `scope`；未消费的 13 个键是一项说明和 12 个已经取得中文标签的条目 |

以下材料位于构建目录，但不被 `build-topics.py` 读取。

| 材料 | 当前内容 | 当前用途 |
|---|---:|---|
| `label-lookup.json` | 692 项，85 项查到、607 项未查到 | `lookup-labels.py` 的联网查询结果，供人审 |
| `label-review.md` | 85 项查到结果的审阅表 | 人工复核材料 |
| `__pycache__/gbt_en.cpython-314.pyc` | 一项受 Git 跟踪的缓存文件 | 不作为本基线的逻辑输入；当前复现由 `gbt_en.py` 提供模块源码 |

术语识别器的当前输入如下。

| 输入 | 当前内容 | 读取边界 |
|---|---:|---|
| `concepts/glossary.md` | 141 条以“术语”为表头的数据行；首列 141 个值均唯一，数据行无空单元格 | 实现实际读取文件内全部 162 条表格数据行的前两列，得到 390 个去重写法，其中包含缩写表和标准表，不只读取 141 条术语行 |
| `topics.yaml` | 700 个概念 | 读取 `label`、`alt`、`hidden` 中的全部字符串 |
| `entities.yaml` | 61 个实体 | 同上 |
| `types.yaml` | 6 个类型 | 同上 |
| `concepts/*.md`、`design/**/*.md` | 38 个被扫描文件 | 扫描标题、加粗内容和中文引号；排除术语表、围栏代码、行内代码和链接目标 |

术语表得到 390 个写法，三个词表得到 854 个写法，两组重叠 2 个，合并后当前已登记写法为 1242 个。

## 哈希清单

下列 SHA-256 固定本次构建输入、输出和术语表。

| 文件 | SHA-256 |
|---|---|
| `concepts/glossary.md` | `7d60a1da6ec8257115eb1fb0b09059504b867f8c167dfcc639a95d48ff572d39` |
| `vocab/topics.yaml` | `4c746ac51b9ad585445037ee57abd34d5542a48e04f3667e3ea32866d8171993` |
| `vocab/build/cs2023-kus.json` | `a59470e2405c323b63b87c7f49c435a3fb056b4b01e5adb11a214107767112d3` |
| `vocab/build/cs2023-zh.json` | `c83351956b8587c8e74f441909499fa82b301e77d2f6a7776c40de85744d69d9` |
| `vocab/build/extra-arrays.json` | `bd58a7fa71a248fd17d2f6032dae6db5461df0f374f9c015d9a9c45f9c2bca10` |
| `vocab/build/gbt-13745.json` | `1e42c14d8159fd45b1260388cc70908058bb76aad7166ebdd09d10d1c569da18` |
| `vocab/build/gbt_en.py` | `727eef56242b83fcfe70dd487f0dffc9a09765014ad2740e608dd6d59528dc51` |
| `vocab/build/label-decisions.json` | `e9996ec1e6beec003cb73b4a57d270ba925ae711e3ec40b646e3c38d54b6b271` |
| `vocab/build/scope-zh.json` | `8266dc0f38a68b1169e53ad7b0ad5961cc7ec77b0d66e62a2596580f73844ee4` |
| `scripts/build-topics.py` | `49bd7b063005a3e9a7e7213a290fcbaa6d68597e0027ff5bb33e1365dcdbcc70` |

下列 SHA-256 固定上游审查材料、校验器、测试及校验器读取的其他数据。

| 文件 | SHA-256 |
|---|---|
| `vocab/build/label-lookup.json` | `70e8b0d7ef2028882da034fa543d45f75acb51918e23cc8c358552114eab7398` |
| `vocab/build/label-review.md` | `8e1032439694890e2c2589c0e7d70dea73740641d03e60315af63938b79e34c0` |
| `vocab/build/__pycache__/gbt_en.cpython-314.pyc` | `fbdd82d2bde28595603a645c25036ae3705ba7b3376053bba910cd1075a12718` |
| `scripts/lookup-labels.py` | `7990f6ecae111bb732e9fbca3101c252099348f9ef7f43a6054c6d425b65b103` |
| `scripts/check-topics.py` | `a2c4bf725736027f128e8edf3ea93565b2b060fca23f854900c6e8f76a1e2fb8` |
| `scripts/check-terms.py` | `87f03c09c17781344df7a7f1f61ab6db0b2509de40aae29494f852c8fb0d9af9` |
| `scripts/check-links.py` | `136215f94f718744b3feb07c47899347887ddf2f64d8c4635fe6322bb1a9dcb2` |
| `tests/test_check_terms.py` | `f5c3855c9f628750fdd202fe430fd1dd5d82729c0b0cb97560beb73430a842b4` |
| `vocab/entities.yaml` | `63020dd3edbb3a25339846943fa67d774335b866e687a7b70f8a110a3ac50ff7` |
| `vocab/sources.yaml` | `1f550993984e2ba4329828b01fcf08ddee97d7433027265207c98277173c50ff` |
| `vocab/types.yaml` | `4013f6b08a05fa0e464c8332c4037728f54b7c7372abe05e142dbc4e4f520947` |
| `vocab/genres.yaml` | `7ec8fdc737d20f1d0034168e3abc16dd111c52673af3f0d48a0042ef036310f6` |
| `vocab/forms.yaml` | `8343b951a7bdf6cf231aa1bac326e92be4ece7d4af3846b9a8acba11a88ac78f` |
| `vocab/signals.yaml` | `aa832bf456260fad927b47cdede104f2fe3f7488a46391c2d6e8fcf06920d0c8` |

## 复现命令

构建器没有输出路径参数，会覆盖其仓库根下的 `vocab/topics.yaml`。本次把 `scripts/` 与 `vocab/` 复制到临时目录后运行，未在当前检出中执行写入型构建命令。

```bash
baseline_dir=$(mktemp -d /tmp/kb-generation-baseline.XXXXXX)
cp -R scripts vocab "$baseline_dir"/
python3 "$baseline_dir/scripts/build-topics.py" > "$baseline_dir/build-1.stdout"
cp "$baseline_dir/vocab/topics.yaml" "$baseline_dir/topics-run-1.yaml"
python3 "$baseline_dir/scripts/build-topics.py" > "$baseline_dir/build-2.stdout"
shasum -a 256 \
  vocab/topics.yaml \
  "$baseline_dir/topics-run-1.yaml" \
  "$baseline_dir/vocab/topics.yaml"
cmp -s "$baseline_dir/topics-run-1.yaml" "$baseline_dir/vocab/topics.yaml"
cmp -s vocab/topics.yaml "$baseline_dir/vocab/topics.yaml"
git diff --no-index --stat -- vocab/topics.yaml "$baseline_dir/vocab/topics.yaml"
```

只读校验命令如下。没有运行会写入 `signals.yaml` 的 `python3 scripts/check-topics.py --record`，也没有运行会联网并写入 `label-lookup.json` 的 `lookup-labels.py`。

```bash
python3 scripts/check-topics.py
python3 scripts/check-terms.py
python3 scripts/check-terms.py --all
python3 -m unittest tests/test_check_terms.py -v
python3 scripts/check-links.py
```

## 输出快照

主题词表两次临时生成都输出“700 个概念，24 个数组”。两个临时输出和当前正式输出均为 6825 行、251530 字节，SHA-256 均为 `4c746ac51b9ad585445037ee57abd34d5542a48e04f3667e3ea32866d8171993`；两次 `cmp` 均返回 0，`git diff --no-index --stat` 无差异。

当前主题词表结构如下。

| 检查项 | 当前结果 |
|---|---:|
| 概念 | 700 |
| 概念唯一标识 | 700 |
| 重复概念标识 | 0 |
| 数组 | 24 |
| 数组唯一标识 | 24 |
| 重复数组标识 | 0 |
| 概念与数组标识交集 | 0 |
| `active` | 8 |
| `unassigned` | 692 |
| 其他状态 | 0 |
| 无任何标签的概念 | 0 |
| 缺中文标签且 `basis.zh` 为 `none` | 240 |
| 缺英文标签且 `basis.en` 为 `none` | 374 |
| 空标识、空状态、空日期或空语言依据 | 0 |
| 空 `broader` | 8 个顶层概念 |

现行[主题词表设计](../../../design/topics.md)写明 `label.zh` 必填，但生成器和校验器允许 `basis.zh: none` 时不写中文标签；当前有 240 条。该不一致不影响本次逐字节复现，但在任何模式迁移或生成器替换前必须待人决定，不能由库存补出默认值。

主题校验返回 0，摘要为“0 处问题；700 概念，24 数组，61 实体，31 来源”。校验器另报告 20 个重复英文标签，并明确把它们视为不同上位下允许存在的同名概念。

术语识别器当前结果如下。

| 模式 | 识别总数 | 输出明细 | 输出 SHA-256 |
|---|---:|---:|---|
| 默认 | 298 | 15 条，限出现于至少两个文件 | `83db028ef94d244cc691e2a7cd795001fafa54fa410bd4cc79a7fd3f006eab47` |
| `--all` | 298 | 298 条 | `c67f05ce3675806dbc545e52ef6bce0e774daf3f9c53c8a3cda6ddc2322bd399` |

298 个字符串分布于 315 个“字符串―文件”关联中，单个字符串最多涉及 3 个文件。当前实现只保留文件集合，不保留同一文件内的出现次数和逐次位置，因此不能从当前报告恢复维护设计所列的总出现次数和上下文。

## 现有测试

仓库当前只有 `tests/test_check_terms.py` 一份测试文件。本次运行 6 项测试，全部通过：

- 纳入标题、加粗内容和中文引号；
- 排除行内代码、围栏代码和链接目标；
- 排除已登记首选、替代和隐藏标签，但不猜测未批准变体；
- 报告待人工判断字符串，不输出术语裁定；
- 保留冻结的字符串身份变量；
- 同一夹具连续运行输出相同。

当前没有为 `build-topics.py`、`check-topics.py` 或 `check-links.py` 建立单元测试或固定夹具。当前构建确定性由本次临时双跑和哈希证明，不由自动测试持续保护。

全库链接检查返回 2 处既存问题：

- `.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/agentic-plan.md:11` 的相对链接目标不存在；
- `.superpowers/sdd/2026-08-30-basic-unit-consumer-classification/artifacts/human-decision-package.md:340` 使用 `#L68`，不是当前链接校验器识别的标题锚点。

这两处不在本任务写集内，未修改。

## 手工边界

当前正式 `topics.yaml` 与构建结果逐字节一致，因此当前没有输出文件中的后置手工差异。文件头的警告仍然有效：一旦有人直接修改输出，再运行构建器会覆盖修改。

当前构建链的人工编辑点如下。

| 编辑点 | 当前作用 | 风险边界 |
|---|---|---|
| `build-topics.py` 中的 `TOPS` | 固定八个顶层、标签、代码和依据 | 是范围与身份决定，不是普通生成参数 |
| `build-topics.py` 中的 `LIS` | 固定 870 分支 | 与 `gbt-13745.json` 分离，修改须同时核对来源和输出身份 |
| `build-topics.py` 中的两个多层级追加 | 为两个现有概念追加第二上位 | 属于概念归属判断，不得由字符串自动重建 |
| `extra-arrays.json` | 保存额外来源数组和条目 | 来源、数组和概念对应须逐项复核 |
| `label-decisions.json` | 保存 85 项人工回查决定 | 不能由 `label-lookup.json` 自动重算批准结论 |
| `scope-zh.json` | 保存不译记录的解释材料 | 253 个键中当前只有 240 个进入输出，不能把未消费键自动删除 |
| `cs2023-zh.json` 与 `gbt_en.py` | 提供构建时使用的语言形式 | 当前标识由英文形式经 `slug` 得到；修改形式可能改变标识，稳定标识的后续处理待人决定 |
| `TODAY` 与 `VERSION` 常量 | 固定输出日期和版本 | 具体版本规则仍待人决定，不能从常量推出未来规则 |

`lookup-labels.py` 会联网并写 `label-lookup.json`，其输出只供人审；`label-review.md` 与 `label-lookup.json` 都不进入确定性构建。把联网结果直接接入构建会越过现行人工决定边界。

## 未来边界

已批准草案提出的未来边界如下，但草案仍未生效。

- `vocab/terms.yaml` 拟成为术语的唯一正式编辑源；当前文件不存在，具体 `schema`、`version` 和标识规则待人决定。
- `concepts/glossary.md` 拟从已校验的术语记录确定性生成，并带只读声明；当前文件仍直接编辑，当前没有生成器。
- 生成视图只消费 `active` 概念；`candidate` 不进入标题、正文、术语表或受委托标签。
- 每种语言的唯一优先术语作为主显示形式；允许术语可以作为替代入口；废弃和被替代术语只进入获准的历史或检索区。
- 生成器不得补译、改写或从另一语言生成形式；缺少目标语言术语时保留有依据的原语言形式。
- 受 `term_concept` 委托的标签与术语表必须读取同一生成快照；未建立委托的词表标签继续由原词表治理。
- 相同的已校验输入、模式版本和生成器版本须得到逐字节相同输出，连续运行无差异；人工修改生成文件须校验失败。
- TBX 继续后置，只能从已发布内部快照单向导出；当前不设计导入或往返编辑。
- 现有 `build-topics.py` 是否退出正式写入流程，须在实施计划中根据本基线、差异和独立提案决定。本报告不作退役决定。

未来生成器不得复制来源治理草案已经定义的共享接口；它只能消费 `basis`、`source` 和 `match`。来源变化先形成来源复核义务；影响术语时再建立术语复核义务，不能让生成器自动改写状态、替代关系、委托或历史。

## 正反例需求

后续模式、生成器和校验器至少需要以下正例。具体夹具标识、目录和模式版本待实施计划决定。

- 相同输入连续生成两次，术语表、受委托标签和正文一致性检查读取同一快照，所有输出逐字节相同；
- `active` 概念中每种语言恰有一个优先术语，允许术语作为替代入口出现；
- 缺少目标语言术语时只显示有依据的原语言形式，不产生回退译名；
- 不同概念中的同形术语分别保留，并形成复核报告，不自动合并；
- 已批准的 `term_concept` 让同一概念、同一语言只有一个正式编辑位置；
- 当前主题词表固定输入能继续生成 700 个唯一概念和 24 个唯一数组，或迁移计划逐项解释任何变化。

后续模式、生成器和校验器至少需要以下反例。

- 顶层键、必填项、基数、语言标签、工作流状态或术语管理状态不合法；
- 概念或术语标识重复、内部引用悬空，或同一概念同一语言的形式重复；
- 同一概念同一语言没有优先术语或有多个优先术语；
- `candidate` 概念进入术语表、正文或受委托标签；
- 废弃或被替代术语被当作新的正文用语，或被替代术语缺少合格的 `replaced_by`；
- `basis`、`source` 或 `match` 不符合共享接口，或把标签相同直接变成概念映射；
- 不同文字体系被自动转换，缺失语言被自动翻译，或记录外出现新形式；
- 生成文件被手工修改后仍通过校验；
- 受委托标签和术语表使用不同快照或不同形式；
- 主题词表输入出现重复概念标识而校验器因字典覆盖没有报告；
- 标签变化导致现有主题概念标识变化却没有迁移对账和人工决定；
- 联网回查结果未经人工决定直接进入正式输出。

## 已知疑虑

- 现行主题设计要求 `label.zh` 必填，当前生成器与校验器却允许 240 条记录缺中文标签并以 `basis.zh: none` 表示不译；未来模式不能自行选择其中一边。
- `check-topics.py` 先把列表转成以标识为键的字典，没有显式报告原列表中的重复标识；本次独立审计确认当前无重复，但现有校验器缺少该负例。
- 当前主题概念标识由英文输入经 `slug` 计算，形式变更可能改变标识，与现行“标识一经引用不改”的政策存在实施风险；稳定化方式待人决定。
- `gbt-13745.json` 中 520 支的 52 个条目不被当前构建器读取，870 支则硬编码在脚本中；目录位置不能证明数据被消费。
- `scope-zh.json` 有 13 个当前未消费键；它们不是空值，也不能仅凭未消费自动删除。
- 术语识别器把术语表中的缩写表和标准表也纳入已登记写法，并只保留文件集合，不保留逐次位置；它不能直接满足未来逐项术语记录和维护计数要求。
- 当前只有术语识别器测试；构建器、主题校验器、术语表结构和人工编辑漂移都缺少持续回归测试。
- `vocab/build/__pycache__/gbt_en.cpython-314.pyc` 受 Git 跟踪，但当前基线环境是 Python 3.9.6；缓存文件是否保留不在本任务权限内。
- 全库链接检查有 2 处既存失败，均位于旧 `.superpowers` 产物，不属于本任务写集。

## 自查结果

本次自查结果如下。

| 门禁 | 结果 |
|---|---|
| 写集 | 只新增本报告；正式脚本、输入和输出未修改 |
| 身份唯一 | 700 个概念标识、24 个数组标识、61 个实体标识、31 个来源标识、6 个类型标识、5 个体裁标识和 16 个载体标识分别唯一；术语表 141 个首列值唯一 |
| 空字段 | 当前生成输出没有空标识、空状态、空日期、空语言依据或全空标签；8 个顶层的 `broader` 为空；240 个中文标签和 374 个英文标签按现行生成规则缺省并分别以 `none` 表示 |
| 状态值域 | 主题词表只出现 `active` 与 `unassigned`；实体只出现 `candidate` 与 `active`；类型和体裁只出现 `active`；载体只出现 `unassigned`；都落在各自现行校验值域内 |
| 幂等性 | 两次临时生成与当前正式输出逐字节相同，SHA-256 均为 `4c746ac51b9ad585445037ee57abd34d5542a48e04f3667e3ea32866d8171993` |
| 现行校验 | `check-topics.py` 为 0 问题；6 项术语识别器测试通过；链接检查保留 2 处既存失败 |
| Git 差异 | 受 Git 跟踪文件差异为 0 |
