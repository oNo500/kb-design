# 来源用途登记

`data/vocab/sources.yaml` 以稳定 id 登记来源用途，entity 指向[命名实体词表](entities.md)中的来源实体。名称、类别、档级、版本、地址与外部状态留在实体表，不重复保存。理论见[词表映射](../../concepts/vocabulary-mapping.md)与[知识体系](../../concepts/body-of-knowledge.md)。

本文采用已采纳的[来源字段合同](../../decisions/source-v2-field-contract.md)。正式来源数据及其引用尚未完成迁移；新合同、工具与字段采纳不等于完整记录、角色、关系或正式切换获准。严格入口只接受 v2，旧格式仅由 Git 和迁移审计保留。

## 对象分工

| 对象 | 职责 | 效力边界 |
|---|---|---|
| 来源实体 | 身份、名称、版本、地址、档级及外部状态 | 不批准用途或具体关系 |
| 用途记录 | id、entity、roles、history | 不改变来源身份，不自动产生派生或映射 |
| basis | 支持具体字段值的外部依据 | 不表示实际派生、映射或项目批准 |
| source | 记录或结构的实际派生 | 不表示普通参考、项目判断或概念等同 |
| match | 本地与外部对象的具体映射 | 不替代标签、范围或层级依据 |
| external_group | 外部数组分组的身份与依据 | 不证明每个成员由该来源派生 |
| assertions | 明确保留既有项目判断 | 不取得外部依据效力 |

项目决定独立保存。批准结构只回答可以怎样表示，不能推出具体来源状态、用途资格或关系结论。

## 用途记录

id 与 entity 保持现有一对一关系，entity 必须指向 kind 为 standard 或 publication 的实体。roles 是非空的逐角色记录列表，每项包含 role、status、decision。history 只追加真实动作、日期、字段与决定；旧用途 checked 保留在迁移前值中，不成为角色批准日期或实体复核日期。

| role | 资格用途 | 对应引用 |
|---|---|---|
| mapping | 具体外部映射 | match.registry |
| structure | 实际结构、记录派生与外部数组分组 | source.registry、external_group.registry |
| group | 从现有映射确定性计算派生概念组 | 不作为 external_group 的资格 |
| discovery | 发现材料与待审线索 | 不取得前三种资格 |

role 的 status 只取 proposed、approved、retired。proposed 的 decision 为 null；approved 或 retired 必须指向确实批准该对象、角色与状态的已采纳决定。旧 mapping、structure、group 不自动升级；旧 candidate 转为 proposed discovery，不产生概念、名称或试用资格。

现有用途的适用限制继续保留：structure 同时要求 mapping，并受[层级结构](hierarchy.md)的来源选择、复制深度与同一视角规则约束；来源为 de-jure 或有版本号的 de-facto。无版本 de-facto 和 vendor 不因格式迁移取得结构用途，archival 也不因此取得用途。group 继续要求 mapping，只使用本库已有映射；它不由一条映射或消费者使用自动批准。任何适用范围扩展均须另行决定。

当前来源清单以[正式数据](../../../data/vocab/sources.yaml)为准；该文件的旧角色并不是新合同中的 approved。tier 决定档级与复核周期，不决定外部状态或角色批准。按[来源数据批次](../../decisions/source-data-batch.md)，source_status 可省略，version 必有但可为 null；前者表示外部状态未核实，后者表示未登记可核实版本。它们不批准任何用途，无版本 de-facto 的 structure 限制保持。

## 严格引用

| 对象 | 字段 | 条件 |
|---|---|---|
| basis 项 | entity、locator、按可变性要求的 checked | 指向来源实体；不要求用途角色；定位可重复核对 |
| source | registry、item、locator、basis | structure 已获准；locator 保存逐行最终定位，不只保存模板 |
| match 项 | registry、item、rel、basis | mapping 已获准；每条关系有相邻非空依据 |
| external_group | registry、item、locator、basis | structure 已获准；只表达分组依据 |

可变内容的 basis 必须有真实 checked。固定版本与真实内容哈希共同确定引用内容时才可省略；版本字符串本身不足以证明内容固定，version: null 更不能触发该例外。entity 指来源实体，registry 指用途登记，两者不能互换。

source_status 缺省不自动否定具体历史或固定材料，也不批准其关系。引用仍须核对所选材料、定位、真实日期、用途资格和逐条采纳；确实依赖外部现行状态的操作在缺值时阻断。已填写状态保持发布者依据与精确字段采纳，不以可省略为由覆盖合格结论。

收集器先识别受约束字段，再检查内容；缺字段、多余键、旧字符串或旧 match.source 都须报错，不能被静默漏掉。语言依据 references 的 source 是其[独立合同](topics.md#语言依据)，不等于旧派生字段，也不由这次迁移改变译名等级。

## 本地结构

本地建立、综合判断或只受材料支持的记录不填外部 source。原 source: self 的事实通过 assertions.source 保存 disposition: project_assertion、original: self 与 migration 审计定位；它不表示外部派生，与 source 互斥。

载体数组按[来源迁移](../../decisions/source-migration-policy.md) Q16 保存 local_analysis，字段为 legacy_source_label、state: isolated、decision。decision 指向批准本地分析隔离的决定；原标签、父项与成员保留，不转换为 external_group，不新建来源或划分特征。该记录只保存既有本地分析，不进入外部来源索引。

外部数组的 external_group 与成员的 source 分别核对。CS2023 主派生与补充来源、match 按 Q14 分开；RFC 层次按 Q17 逐层保存依据。派生概念组仍是已有映射的确定性视图，不能显示尚未建立的缺口、创建概念或替代结构复制。

## 映射关系

映射不建立在数组本身或层级位置上。item 保存外部条目标识，无编号时保存永久地址；rel 使用以下五种关系。

| rel | 含义 |
|---|---|
| exactMatch | 同一概念，可以互换；传递 |
| closeMatch | 基本同一；不传递 |
| broadMatch | 外部概念更宽 |
| narrowMatch | 外部概念更窄 |
| relatedMatch | 相关 |

不能确认完全一致时使用 closeMatch 的现有规则不免除范围判断与关系证据。相同标签、旧 rel、来源登记、角色批准或迁移账本分类都不能自动成立一条映射。实体映射还须核对是否同一个体，不能用概念等同规则混淆身份。

## 实施边界

schema、严格校验、反向索引、迁移准备和应用表示按同一合同实施。旧紧凑依据、旧 source、旧 match、role 字符串数组和标量 watch 不进入正式新快照；未核对必需事实阻断对应转换，不通过丢字段、补空证明或改状态解除。

反向索引只提供影响位置，不作修改结论。项目判断、本地分析与历史 before／after 不产生正式外部引用边。历史来源账本保留原基线与哈希，当前变化另行记录，不重写旧账本为已批准。

来源探测的固定 HEAD／GET 夹具只提供信号，live 与正式周期运行没有因本合同开放；观察不回写状态、日期或依据。来源复核义务接口不能凭空创建正式义务、目标或解决结论。术语正式激活与来源迁移分开。

恢复只使用明确提交范围的 Git revert。全部数据和消费者验收完成前不得合并 master；正式切换、发版与正式 vault 刷新分别处理。

## 待定事项

- 尚未核实的具体来源版本与外部状态如何取得材料；缺省表示已由[来源数据批次](../../decisions/source-data-batch.md)确定，不增加 unknown，不用抓取日期冒充版本。
- MDN Web 的结构用途与 mdn-curriculum 的 group 用途仍须分别决定，格式迁移不改变其资格。
