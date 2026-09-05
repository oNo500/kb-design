# 文档关系核对

本次只核 12 条剩余映射；已批准的 Explanation、Analysis、Obsidian 不在逐项提案中。先读既有写作阅读记录与当前词表，再查官方具体定义；结果见 [逐项记录](2026-09-06-document-relations.json)。所有 checked 均为 2026-09-06 的新观察，不改原阅读日期、正式数据或中文 designation。

## 范围判断

| 本地对象 | 外部对象 | 建议 | 原因 |
|---|---|---|---|
| types/types/tutorial | diataxis / tutorials | 保留 exactMatch，待采纳 | 本地学习、动手、带着做与成功要求覆盖核心；成功是编写目标，不是对一切情形的事实保证。 |
| types/types/how-to | diataxis / how-to-guides | 保留 exactMatch，待采纳 | 本地具体任务、步骤、不解释相符；步骤不能被读成只有线性机械操作。 |
| types/types/reference | diataxis / reference | 保留 exactMatch，待采纳 | 本地事实查阅、中立及镜像结构相符；此对应限文档用途，不等于整套写作规则全部采纳。 |
| genres/genres/background | iptc-genre / http://cv.iptc.org/newscodes/genre/Background | 保留 closeMatch，待采纳 | 本地事实原理说明不限于所报事件，IPTC限定新闻事件；双方均承担提供理解所需背景的用途，存在可解释的语义接近。建议保留closeMatch，不能据此把任意不评价的文本都视为IPTC Background。 |
| genres/genres/opinion | iptc-genre / http://cv.iptc.org/newscodes/genre/Opinion | 保留 closeMatch，待采纳 | 本地心得偏好立场较广，不要求新闻编辑形式；共同的作者观点维度支持近似而非完全等同。 |
| genres/genres/review | iptc-genre / http://cv.iptc.org/newscodes/genre/Review | 保留 closeMatch，待采纳 | 本地工具书课程的好坏评价与之有共同评价功能，列举对象不完全同域；支持close而非exact。 |
| genres/genres/advice | iptc-genre / http://cv.iptc.org/newscodes/genre/Advice | 阻断直接采纳 | 本地分类依据是操作建议的内容目的；IPTC定义依据是私人问题来信与回答的栏目形式，原文未规定答复必为操作建议。二者可能重叠，但当前定义未提供足够用途接近依据；阻断直接采纳源于证据不足，不是仅因范围不全等。 |
| types/types/how-to | schema-org / HowTo | 阻断直接采纳 | 目标与步骤核心相近，可作为closeMatch候选；未读到所选30.0冻结定义，不能直接批准对30.0的证据。 |
| types/types/reference | schema-org / TechArticle | 阻断直接采纳 | TechArticle跨本库多个类型，本地reference是信息查阅用途；既有closeMatch并无近似替换证明，且30.0定义未核。 |
| genres/genres/review | schema-org / Review | 阻断直接采纳 | 本地好坏评价核心相近，可作为closeMatch候选；仅开发页证据不足以确认所选30.0。 |
| types/types/troubleshooting | dita / 2.7.1.6 | 保留 exactMatch，待采纳 | 本地纠正已出现问题及症状原因处理与用途一致；三项不是每篇都必须已知；映射不表示文档满足XML结构约束。 |
| types/types/glossary-entry | dita / 2.7.1.7 | 保留 exactMatch，待采纳 | 本地一个术语一个义项与概念界定对应；没有声明DITA元素结构符合性。 |

## 版本边界

DITA 两页来自所选 1.3 的 `os` 目录，页脚均为 2015-12-17，章节号与库存一致；没有使用 Errata 02。它们支持用途概念的关系，不证明任何本库文档符合 DITA XML 结构。

Diátaxis 三页支持按学习、工作任务、事实查阅区分用途，未显示整站 `2026-08` 发行标识。IPTC 四条已读当前官方定义，均显示最后修改于 2010-12-15；没有据此假装取得 2024-02-13 冻结词表。该版本限制与本次定义支持分别保存。

Schema.org 三个 canonical 页面均明确标为 development version。尝试 `/version/30.0/HowTo`、`TechArticle`、`Review` 均抓取失败；未抓整站或发行大包。因此 HowTo、Review 仅有定义相近的候选依据，未作为 30.0 的直接采纳提案。TechArticle 另有实质范围问题，不能把技术文章总类当作 reference 的近义类型。

## 原文位置

- [diataxis / tutorials](https://diataxis.fr/tutorials/)：开头、Obligations of the teacher、Aspire to perfect reliability。以学习为目的，导师引导实践，要求学习者可完成并获得成功。
- [diataxis / how-to-guides](https://diataxis.fr/how-to-guides/)：开头、What how-to guides are not、Key principles。为有实际目标且已有能力的使用者提供操作指导，排除教学解释；允许分支、判断和多入口。
- [diataxis / reference](https://diataxis.fr/reference/)：开头、Describe and only describe、Respect the structure of the machinery。查阅用的中立技术描述；结构跟随对象，包含描述正确使用方式，区别于带做任务。
- [iptc-genre / http://cv.iptc.org/newscodes/genre/Background](https://cv.iptc.org/newscodes/genre/)：genre:Background 的 Definition；单条HTTPS入口失败后采用官方词表同一条目。为正在报道的事件设置背景并作解释。
- [iptc-genre / http://cv.iptc.org/newscodes/genre/Opinion](https://cv.iptc.org/newscodes/genre/Opinion)：Definition、modified、retired。作者观点的编辑性评论；modified为2010-12-15，retired为空。
- [iptc-genre / http://cv.iptc.org/newscodes/genre/Review](https://cv.iptc.org/newscodes/genre/Review)：Definition、modified、retired。对创造性活动或服务作批评评价，举书籍、电影、餐馆为例。
- [iptc-genre / http://cv.iptc.org/newscodes/genre/Advice](https://cv.iptc.org/newscodes/genre/Advice)：Definition、modified、retired。读者个人问题的来信与回答。
- [schema-org / HowTo](https://schema.org/HowTo)：页首development version、类型定义、step属性。通过一系列步骤达到结果的指令，step可为步骤或步骤分节。
- [schema-org / TechArticle](https://schema.org/TechArticle)：页首development version、类型定义。技术文章的例子包括任务操作、分步、程序化排障和规格。
- [schema-org / Review](https://schema.org/Review)：页首development version、类型定义、itemReviewed。对一个对象的评价，示例含餐馆电影商店，itemReviewed指出被评对象。
- [dita / 2.7.1.6](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/archSpec/technicalContent/dita-troubleshooting-topic.html)：2.7.1.6 开头、The troubleshooting information type、页脚。纠正异常状态的内容；症状、原因、补救是最简模式，允许多组配对及未知原因或未知补救。
- [dita / 2.7.1.7](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/archSpec/technicalContent/dita-glossary-topic.html)：2.7.1.7 开头、The structure of the glossentry topic、页脚。单个词的单个义项；同词多义应分别建条目，可附词性缩写。

## 采纳边界

8 条建议保留既有关系，4 条阻断直接采纳。这里的保留不是因名称同义，而是按用途、对象与边界比较；closeMatch 允许范围与场景差异，Background、Opinion、Review 的差异不构成自动阻断。Advice 当前缺少充分用途接近依据，不能通过未经授权地缩写本地 scope 或新造类别修复。本次没有删除映射，blocked 的 suggested_after 为 null，后续需针对范围或所选版证据决定，不能把 null 当删除指令。

## 定版补充

此前三条 30.0 缺口是当时观察，原记录保留。随后根代理取得 [Schema.org 30.0 官方 JSON-LD](https://schema.org/version/30.0/schemaorg-current-https.jsonld)，本次于 2026-09-06 只读本地 `build/source-verification/schema-org-30.0.jsonld` 的三个具体条目，精确位置分别为 `@graph` 中 `schema:HowTo`、`schema:Review`、`schema:TechArticle` 的 `rdfs:comment`；文件哈希记录在 JSON 补充字段。

HowTo 的步骤达成结果、Review 的对象评价定义均与此前观察一致，现建议保留两条 closeMatch，所选版缺口已解除。TechArticle 的所选版证据同样补齐，但定义仍横跨操作、任务、排障和规格，近似替换范围未获支持，保留范围阻断。当前汇总为 10 条建议保留、2 条阻断（IPTC Advice 与 Schema.org TechArticle），原先 8/4 为补充前历史结果。本次没有重抓、修改 data 或提交。

## 候选形状

JSON 中可保留项与 Schema.org 30.0 后续观察的 suggested_after 已补为 v2 match，basis 包含实际读取 URL、条目位置和 2026-09-06；before 和旧缺口历史保持不变。所有候选均待采纳，blocked 的 null 不表示删除。
