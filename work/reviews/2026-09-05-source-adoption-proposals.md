# 来源采纳提案

状态：待人采纳。基线为 `cf80d1d`，执行范围按已确认的[来源执行](../../docs/decisions/source-execution-boundary.md)。本文只给出字段级提案；没有执行正式数据转换，不把已读笔记误称为新核对的外部原文。

## 材料选择

本批优先直接阅读 [ISO 25964 笔记](../../docs/references/iso-25964.md#材料身份)、[NISO 笔记](../../docs/references/z39-19.md#材料身份)和[元数据标准笔记](../../docs/references/metadata-standards.md#阅读范围)。这些记录都明确原核对日期为 2026-08-29，并保存了发布者页面及已读位置。

它们比尚需取得原始标准或条目 revision 的对象更适合先形成字段提案。本轮没有打开 PDF、OCR、解析 HTML、下载或联网。原始网页本轮不重访，提案的证据性质是“已留存的发布者页面阅读记录”；日期沿用记录中的 2026-08-29，不使用本次工作日期。

## 具体提案

以下 P 编号只用于本报告内审阅，不是来源或项目决定 ID。目标字段是后续来源 v2 候选中的字段；不得把 `status: current` 直接写回仍采用项目生命周期状态的正式旧表。

| 提案 | 目标 | 旧值与建议值 | 依据与理由 | 不采纳时 |
|---|---|---|---|---|
| P1 | `iso-25964-1` 的 v2 `version`、`status` 及相邻依据 | `version: "2011"` 保留；旧项目 `status: active` 不做值映射；另建议外部 `status: current`，仅依据 2026-08-29 的已留存观察 | ISO 笔记记载第 1 版、2011-08、2022 年复审确认，官方页在原核对时仍列为现行版本；不是从 active 推导 current | 保留旧记录，该外部状态本轮不进入候选 |
| P2 | `iso-25964-2` 的 v2 `version`、`status` 及相邻依据 | `version: "2013"` 保留；不转换旧 active；另建议外部 `status: current`，证据日期仍为 2026-08-29 | ISO 笔记记载第 1 版、2013-03、2023 年复审确认，以及原核对时的官方现行版本状态 | 同 P1；不借 Part 1 的材料代替 Part 2 |
| P3 | `z39-19` 的 v2 `version`、`urls` 及相邻依据 | 保留 `version: "2005 (R2010)"`；旧 url 转为主 landing；新增已记录的 DOI 地址，非主地址 | NISO 笔记保存出版页的版本、材料类型和 DOI，以及项目页 version of record 说明；只使用已留存文本，不复读 184 页 PDF | 保留旧单地址；不新增 DOI，不改变状态或 PDF 地址 |
| P4 | `skos` 的 v2 `version` 及相邻依据 | 保留 `version: "2009-08-18"`；补文档日期定位。外部 status 不在本提案中赋值 | 元数据笔记明确保存 2009-08-18 的 W3C Recommendation 及原阅读范围；Recommendation 身份不单独证明本轮仍为 current | 版本按旧值保留，不增加本次依据条目 |

P1、P2 的提案不是“今天重新确认仍现行”。若本次正式迁移要求更新的外部状态观察，这两项相应状态标记“不核对”，不能改日期或声称已有新观察。采纳这个历史观察也不批准对应来源全部字段、用途角色、引用或正式切换。

## 字段值

下列片段给出具体建议值，省略部分保持原值或继续待定。`basis.checked` 仅表示相应观察的原日期，不给整个来源生成一次新的完整 review。

P1：

```yaml
id: iso-25964-1
version: "2011"
status: current
basis:
  version:
    - entity: iso-25964-1
      locator: "https://www.iso.org/standard/53657.html；ISO 25964-1:2011，第 1 版，2011-08"
      checked: "2026-08-29"
  status:
    - entity: iso-25964-1
      locator: "https://www.iso.org/standard/53657.html；现行版本与 2022 年复审确认信息"
      checked: "2026-08-29"
```

P2：

```yaml
id: iso-25964-2
version: "2013"
status: current
basis:
  version:
    - entity: iso-25964-2
      locator: "https://www.iso.org/standard/53658.html；ISO 25964-2:2013，第 1 版，2013-03"
      checked: "2026-08-29"
  status:
    - entity: iso-25964-2
      locator: "https://www.iso.org/standard/53658.html；现行版本与 2023 年复审确认信息"
      checked: "2026-08-29"
```

P3：

```yaml
id: z39-19
version: "2005 (R2010)"
urls:
  - role: landing
    url: https://www.niso.org/publications/ansiniso-z3919-2005-r2010
    primary: true
  - role: doi
    url: https://doi.org/10.3789/ansi.niso.z39.19-2005R2010
    primary: false
basis:
  version:
    - entity: z39-19
      locator: "https://www.niso.org/publications/ansiniso-z3919-2005-r2010；出版标题；项目出版页的 2005 edition / 2010 reaffirmation version of record 说明"
      checked: "2026-08-29"
  urls:
    - entity: z39-19
      locator: "https://www.niso.org/publications/ansiniso-z3919-2005-r2010；出版页地址及 DOI 栏"
      checked: "2026-08-29"
```

P4：

```yaml
id: skos
version: "2009-08-18"
basis:
  version:
    - entity: skos
      locator: "https://www.w3.org/TR/skos-reference/；文档状态及 W3C Recommendation 日期"
      checked: "2026-08-29"
```

这些是部分字段提案，不是完整候选实体。真实的 `review`、`watch`、`replaced_by`、`history` 和其他字段不由省略产生默认值。已登记实体可以作为其发布信息的依据目标；本地阅读笔记的路径、哈希和性质随审查记录保留，不能将项目笔记 ID 冒充发布者实体。

## 核对取舍

| 材料或判断 | 本轮状态 | 原因与影响 |
|---|---|---|
| ISO 两部分已保存的官方状态记录 | 已读本地记录，形成 P1/P2 | 不读取样本 PDF，不复核标准定义，不决定新的映射 |
| NISO 已保存的出版信息与 DOI | 已读本地记录，形成 P3 | 不重做 PDF 解析；修订项目不作为已发布新版或替代关系 |
| SKOS 已保存的版本与文档状态记录 | 已读本地记录，形成 P4 | 保留版本依据提案；是否仍现行、勘误及其他条款不核对 |
| Diátaxis Explanation 阅读摘要 | 已读本地记录，用途相符结论沿用 | 未覆盖的讨论、视角与观点原段落不核对；不形成新的 exactMatch 采纳 |
| IPTC Analysis 的旧定义转录 | 已读本地记录，语境适配结论沿用 | 原条目版本、退役状态和具体关系依据不核对；保留旧 closeMatch |
| GB/T 520 转载清单 | 已读可读文本，代码与名称结论沿用 | 原标准及修改单需要另取材料或解析，本轮不核对；不新批严格关系 |
| Obsidian 的 Wikidata 条目 | 不核对 | 缺本地 revision 与条目正文，不联网抓取，不从 Q 号补造事实 |
| 访谈、共享限制、插件权限及外部示例原页 | 不核对 | 本地没有对应可直接回查的原文；保留普通链接，不生成正式引用身份 |
| 新外部状态、重定向、替代与退役事实 | 不核对 | 需要新的外部观察；不得从旧日期、active/candidate 或网址可见性推出 |
| 其他尚未选定直接可读取证段落的来源 | 本轮不核对 | 不声称没有材料；不为清零库存继续全盘检索或解析 |

“不核对”会阻止依赖该事实的正式值进入切换，但不会阻止 P1–P4 的审阅或其他无依赖工作。它不是删除条件或让校验绕过失败的开关。

## 迁移影响

采纳 P1–P4 后，允许将所列字段与依据纳入后续候选；不等于正式候选整体可通过校验。正式 `data/vocab/entities.yaml` 继续保持原字节，`sources.yaml` 和所有角色也不改变，直至整体字段处置与消费接口明确。

本批不新增来源身份、designation、类别、映射关系、review 完成日期或回滚代码。Git 保留提案基线及后续修改，实际撤销使用明确提交范围的 revert。没有要求为这些部分字段另造通用候选框架或补偿链。

## 核查记录

本地材料的 SHA-256 如下，用于回查提案所依据的笔记版本，不作为原始网站内容哈希：

| 材料 | SHA-256 |
|---|---|
| `docs/references/iso-25964.md` | `bb73f712124a7af934f6e97148cf538268017da01dc7fbc7d2cc49e5b4672fb0` |
| `docs/references/z39-19.md` | `e02ac9dcc3795cb92973c6e83082e0b3d4aed3d7bbfb25b41a55001a3b87e7ba` |
| `docs/references/metadata-standards.md` | `d56542d28d763c439c8e70a29387d30089b66db5d1e35e9ac7e2c93f6768c935` |

四份片段按现有 `source-entities` schema 的对应字段定义校验通过；这只证明所列字段可表达，没有做完整实体、整库引用或事实充分性通过声明。独立语义审查未发现 Important 或 Critical 问题；重点核对了历史日期、依据性质、部分字段范围及阶段授权。本次没有代码变更，不重复运行应用或迁移回归。
