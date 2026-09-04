# 映射库存

盘点基线为 `feat/terminology-governance` 的 `9e7b411`。逐行库存见 [match-inventory.tsv](match-inventory.tsv)，共 756 条正式映射。

## 范围边界

- 正式映射只存在于五份 `vocab/*.yaml`；每个 YAML `match` 项形成一条库存身份。
- `scripts/build-topics.py` 是主题映射的生成者，`scripts/check-topics.py` 是当前校验消费者；脚本中的生成模板和枚举不是第二份正式映射，不重复计数。
- `vocab/build/*.json` 为代码、标签和范围的构建输入；其中没有 `match` 字段，只作为逐项上下文，不建立独立库存身份。
- Markdown 中的设计说明、示例和计划不是正式数据，不计入 TSV；它们只用于解释当前语义与消费者。
- 字符串、目录、次数和标签同名只用于定位。没有任何一条因同名、同源复制或当前 `exactMatch` 字符串自动取得精确等价结论。

## 接口边界

- TSV 严格使用准备计划规定的九列接口。`草案分类` 全部为已批准草案对象 `match`。
- 当前 `source`、`id`、`rel` 分别只作为拟议 `match.registry`、`match.item`、`match.rel` 的待复核输入。
- 756 条映射的当前结构均没有与关系相邻的 `basis`。记录级 `basis` 只支持标签或 `subjects`，不能挪作 `match.basis`。
- 现行来源登记虽都含 `mapping` role，但尚无草案要求的逐角色 `approved` 状态与决定引用；库存不把现行 role 自动升级为批准用途。
- 映射关系、概念对应和迁移去向均为 L2 提案；库存不作草案生效、来源改档、schema、ID、周期、阈值或范围决定。

## 文件分布

| 文件 | 映射 |
|---|---:|
| `vocab/entities.yaml` | 23 |
| `vocab/forms.yaml` | 16 |
| `vocab/genres.yaml` | 6 |
| `vocab/topics.yaml` | 703 |
| `vocab/types.yaml` | 8 |

## 关系分布

| 当前 rel | 映射 |
|---|---:|
| `closeMatch` | 8 |
| `exactMatch` | 748 |

当前值只有 `exactMatch` 与 `closeMatch`；这只是库存事实，不表示关系已通过草案门禁。

## 来源分布

| 当前 registry 候选 | 映射 |
|---|---:|
| `asvs` | 17 |
| `atlas` | 16 |
| `attack` | 15 |
| `cs2023` | 178 |
| `cwe` | 10 |
| `diataxis` | 4 |
| `dita` | 2 |
| `gbt-13745` | 435 |
| `iptc-genre` | 5 |
| `lom` | 15 |
| `owasp-llm-top10` | 10 |
| `rfc-1122` | 4 |
| `schema-org` | 3 |
| `swebok` | 18 |
| `wikidata` | 24 |

## 状态分布

| 状态 | 映射 |
|---|---:|
| 可机械迁移 | 0 |
| 需要复核 | 39 |
| 待人决定 | 717 |
| 无需迁移 | 0 |

“需要复核”表示本次能读到官方条目或类型说明，但仍缺本地关系 `basis` 与 L2 结论。“待人决定”表示外部 item 身份、定义／范围或版本边界仍有未读或歧义，不能先选 `rel`。

## 材料边界

| 材料 | 本次已核边界 | 未读边界 |
|---|---|---|
| [W3C SKOS 映射属性](https://www.w3.org/TR/skos-reference/#mapping) | 核到五种映射属性；`exactMatch` 要求高置信度、可跨广泛检索场景互换且可传递，`closeMatch` 不声明传递 | SKOS 只给关系语义，不替本库判断 756 对概念 |
| [GB/T 13745-2009 官方页](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4C13F521FD6ECB6E5EC026FCD779986E) | 核到标准身份、现行状态和两个修改单 | 435 个代码对应的官方正文定义与修改单影响未逐项读；当前清单来自转载或构建内联数据 |
| [CS2023 官方报告](https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm) | 确认当前库使用该官方入口 | 本次读取失败；178 个 KA/KU 只核当前构建快照与本地摘要，不猜官方正文 |
| [SWEBOK 官方页](https://www.computer.org/education/bodies-of-knowledge/software-engineering) | 确认当前库使用该 IEEE 入口 | 本次读取失败；18 章只核当前构建快照与本地摘要 |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | 核到 5.0.0、项目范围、章号规则和版本化引用提示 | 17 个章的 Control Objective 未逐章重读 |
| [MITRE CWE](https://cwe.mitre.org/) | 核到当前入口和 4.20 | 十个 pillar 条目未逐页重读 |
| [MITRE ATT&CK Enterprise tactics](https://attack.mitre.org/tactics/enterprise/) | 核到 15 个战术的 ID、名称和摘要 | 未形成 15 条关系的本地 `basis` |
| [MITRE ATLAS tactics](https://atlas.mitre.org/tactics/) | 确认当前库使用该官方入口 | 本次读取失败；16 条仅有当前构建快照和本地摘要 |
| [OWASP LLM Top 10 2025](https://genai.owasp.org/llm-top-10/) | 核到十个编号、名称与摘要入口 | 未形成十条关系的本地 `basis` |
| [RFC 1122 §1.1.3](https://www.rfc-editor.org/rfc/rfc1122.html#section-1.1.3) | 读到四层标题与说明 | 当前四条都用 `1.1.3`，章节定位不能唯一标识四个外部概念 |
| [IPTC Genre](https://cv.iptc.org/newscodes/genre/) | 核到五个目标条目的 URI、名称、定义和未退役状态 | 本地将新闻语境改为笔记语境，五条仍须比较范围并补 `basis` |
| [OASIS DITA 1.3 文档类型](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/archSpec/technicalContent/dita-technicalContent-InformationTypes.html) | 核到 troubleshooting 与 glossary entry 的说明 | 两条本地 `exactMatch` 仍无关系依据 |
| [IEEE 1484.12.1-2020](https://standards.ieee.org/ieee/1484.12.1/7699/) | 核到 2020 版 active 且 superseding 2002 | 收费正文中的 Learning Resource Type 值域未读；15 条 2002 值不能假定仍可用 |
| [Diátaxis](https://diataxis.fr/) | 核到四种用户需求与对应文档形式 | 四条本地 `exactMatch` 仍须比较本地 scope |
| [Schema.org HowTo](https://schema.org/HowTo)、[TechArticle](https://schema.org/TechArticle)、[Review](https://schema.org/Review) | 核到三个类型说明 | Schema.org 类型与本地受控概念的 `closeMatch` 仍需关系依据 |
| [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) | 官方服务可读 | 24 个 Q 条目未逐项打开；Q 号与同名不能替代身份和范围依据 |

## 消费者

- `scripts/check-topics.py` 读取五份词表中的全部 `match`，但只检查 registry 是否登记，并仅对主题映射检查 `rel` 值域；它不验证 item 存在、标签同名风险、定义范围或关系依据。
- `scripts/build-topics.py` 生成主题映射，并用 `source + id` 查找部分中文范围摘要；当前生成逻辑把复制记录统一写成 `exactMatch`，没有逐关系 `basis`。
- 内容模型分别通过 `subject`、`entities`、`type`、`genre`、`form` 消费五类本地对象；消费者使用本地 id，不直接证明外部映射。
- TSV 每行另列当前正式数据中的直接反向引用；无实例时明确写“无”，不以目录或出现次数推断消费者。

## 风险清单

- 748 条当前值为 `exactMatch`，但全部缺关系 `basis`；这些值只能进入逐项复核，不能批量迁移。
- RFC 1122 的四个本地层概念共用 `item=1.1.3`；当前 item 只定位章节，不唯一标识四个外部概念。
- 15 条 LOM 映射指向 2002 值；IEEE 官方页显示 2020 版取代 2002，而 2020 收费正文值域未读。
- 435 条 GB/T 映射只有代码和名称层面的当前材料；官方页另列两个修改单，逐项正文和修改单影响未核。
- 23 条实体 Wikidata 映射与 1 条载体 Wikidata 映射未逐项重开外部条目；名称、Q 号和 `status: active` 都不能补足身份及范围比较。
- `gbt-13745`、`diataxis`、`wikidata`、`schema-org` 的来源实体当前仍为 `candidate`，且 `basis.subjects: self`；现行来源 role 不能自动成为草案中的 approved mapping 用途。

## 待定事项

- 逐 registry 决定哪些现行来源用途可进入 approved `mapping`，并为每项决定留稳定引用；库存不预填决定 id。
- 为每条映射取得双方定义或范围的可重复 locator，再决定保留、降为 `closeMatch`、改为层级／相关关系，或不迁移。
- 为 RFC 1122 四层选择能够唯一标识外部概念的 item，或决定这些记录不形成 `match`；不能继续把共同章节号当作四个 item。
- 读取 IEEE 1484.12.1-2020 相关值域后，决定 15 个 LOM 2002 值的版本与关系去向。
- 核对 GB/T 两个修改单及 435 个代码条目；没有定义或范围时，不因代码和标签一致保留 `exactMatch`。

## 校验结果

- TSV 数据行：756；身份：756 个且无重复。
- 九列空字段：0；状态值域外：0；决策级别：{'L2': 756}。
- 当前关系依据完整：0；`match.basis` 缺失：756。
- TSV SHA-256：`3f9701f6c2ef64a5d3c5a18144fc052f91e80d11384bb4023c85c74381d5d988`。
- 输入 SHA-256：
  - `vocab/entities.yaml`：`63020dd3edbb3a25339846943fa67d774335b866e687a7b70f8a110a3ac50ff7`
  - `vocab/forms.yaml`：`8343b951a7bdf6cf231aa1bac326e92be4ece7d4af3846b9a8acba11a88ac78f`
  - `vocab/genres.yaml`：`7ec8fdc737d20f1d0034168e3abc16dd111c52673af3f0d48a0042ef036310f6`
  - `vocab/topics.yaml`：`4c746ac51b9ad585445037ee57abd34d5542a48e04f3667e3ea32866d8171993`
  - `vocab/types.yaml`：`4013f6b08a05fa0e464c8332c4037728f54b7c7372abe05e142dbc4e4f520947`
