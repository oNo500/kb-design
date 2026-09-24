# Obsidian 词表应用 (Obsidian Vocabulary Use)

`kb-obsidian-rdf` 为 PARA 知识库提供词条生成、选择、引用和检索，支持独立的开发预览与正式使用实例。知识库保存文章、资料和可用条目；原始词表、版本清单、校验报告和恢复资料保存在库外。

## 文件结构

```text
knowledge-base/
├─ home.md
├─ 00-inbox/
├─ 01-projects/
├─ 02-areas/
├─ 03-resources/
├─ 04-archives/
├─ 05-vocabulary/
│  ├─ concepts/
│  ├─ entities/
│  ├─ document-types/
│  ├─ genres/
│  ├─ forms/
│  └─ references/
├─ 06-views/
│  ├─ article-list.base
│  ├─ inbox.base
│  ├─ drafts.base
│  ├─ recently-modified.base
│  ├─ projects.base
│  ├─ areas.base
│  ├─ resources.base
│  └─ archives.base
├─ 07-templates/article.md
├─ 08-attachments/
└─ .obsidian/
   ├─ app.json
   ├─ templates.json
   └─ types.json
```

新文件和目录使用小写，空格与下划线替换为中划线。中文保留，页面 title、名称及原始 ID 不变。例如标题“JavaScript 数组排序教程”对应文件 `javascript-数组排序教程.md`。词条同目录重名以身份短摘要区分；文章同名不会覆盖，需作者明确区分。

`00-inbox` 用于自由捕获，PARA 四区按用途组织内容，`05-vocabulary` 跨目录共同使用。顶层编号固定导航顺序，目录内文件名和 `home.md` 不因编号改变。归档不改文章 UUID、status 或条目状态；文件夹名称不自动成为主题。

新库的 `.obsidian/` 初始配置设置附件目录 `08-attachments`、模板目录 `07-templates`、自动更新内部链接及原生属性类型。界面的 List 类型在 `types.json` 中使用 `multitext`，aliases 使用原生专用类型 `aliases`。外观、工作区、插件开关等个人偏好由用户维护。

## 数据流转

```text
工程项目中的词表与规则
           |
     prepare 固定输入
           |
       init 分离交付
       /           \
PARA 知识库       库外工程状态
文章与词条       原件、索引、清单、报告
       |
查词 → 选择引用 → 写作 → 按引用找文章
```

## 正式库创建

正式库位于 `/Users/xiu/Documents/knowledge-base`，创建范围见[正式库创建](../../docs/applications/obsidian/决定-正式库创建.md)。所有操作显式指定目标；原 `/Users/xiu/Documents/kb-vault` 与开发库独立保留。

```bash
uv run kb-obsidian-rdf prepare \
  --mode formal \
  --source-root /Users/xiu/code/kb-design \
  --authority docs/applications/obsidian/决定-正式库创建.md \
  --entities output/vocabulary/entities/current \
  --output build/obsidian-formal/input.json

uv run kb-obsidian-rdf init \
  --input build/obsidian-formal/input.json \
  --vault /Users/xiu/Documents/knowledge-base
```

prepare 将实体 current 固定到具体版本，复验统一交付，保存原状态、来源、基本字段结果及完整原件；正式使用采用该版本的可用清单，不会仅凭 candidate 禁用记录。CCS 分流未决概念保留查阅，不能自动新选用。辅助值域沿用其既有采用规则。

正式模式须有本地使用范围与授权记录及摘要，不是把 preview 改成 formal 就能创建。初建只接受空目标，不复制开发文章、不迁移旧库内容。首次使用时，在 Obsidian 仓库管理器选择“打开本地仓库”，选定目标目录，再从 `home.md` 开始；之后可使用原生 CLI 打开已登记的实例。

## 开发库创建

省略 mode 或指定 preview 保持开发行为，示例如下：

```bash
uv run kb-obsidian-rdf prepare \
  --source-root /Users/xiu/code/kb-design \
  --authority apps/obsidian-rdf/inputs/开发预览范围.md \
  --output build/obsidian-para/input.json

uv run kb-obsidian-rdf init \
  --input build/obsidian-para/input.json \
  --vault output/obsidian-rdf/development-para
```

输入文件名已存在时须另选新名称。其他 RDF 可提供符合[输入合同](../../docs/applications/obsidian/提案-Obsidian%20导出与导入.md#输入清单)的清单；开发与正式实例不能借普通刷新互相转换。

## 常用视图

首页集中链接八个视图。收件箱展示 `00-inbox` 中的 Markdown 文件；项目、领域、资源、归档分别展示对应 PARA 目录，资源按所在子目录分组。全部笔记保留 `article-list.base` 路径，覆盖 PARA 四区中的 Markdown 文件，包含自由笔记，排除词条、模板和首页。

草稿限定 PARA 四区中声明小写 UUIDv4 identifier 且 status 为 draft 的文章；最近修改覆盖同样声明 UUID 的文章。目录移动不改变文章状态；视图筛选也不代替完整内容校验。

默认显示可点击的标题、主题、实体、文档类型和修改时间，按文件修改时间降序排列。标题缺失时显示文件名。原生 Bases 筛选器可按属性进一步筛选，用户调整保留；普通词表刷新不覆盖视图。已有视图升级须显式审阅候选，不通过普通维护覆盖私人排序和筛选。语法依据见 [Bases](https://obsidian.md/help/bases/syntax)。

## 条目选择

```bash
uv run kb-obsidian-rdf search \
  --vault /Users/xiu/Documents/knowledge-base \
  --field subject --query 人工智能

uv run kb-obsidian-rdf get \
  --vault /Users/xiu/Documents/knowledge-base \
  --field entities --term Obsidian --link
```

先限定字段，再查名称或别名：subject 查主题，entities 查实体，type、genre、form、references 分别查对应值域。省略 search 的 query 可列选项；默认排除不可新选用记录。

get 的 link 输出可粘贴到文章属性，例如 `[[05-vocabulary/entities/obsidian|Obsidian]]`。同名不唯一时返回候选，不自动选择；用 `--ref` 指定明确身份或路径。`--json` 返回结构化摘要，`--details` 才展开完整条目信息。

## 文章建立

```bash
uv run kb-obsidian-rdf new \
  --vault /Users/xiu/Documents/knowledge-base \
  --folder 01-projects/knowledge-base \
  --title 'Obsidian 使用笔记' \
  --type tutorial --genre background \
  --subject-name '信息系统' --entity-name Obsidian
```

工具分配 UUID、日期和 draft，按原身份核对选择，再写入指定的 PARA 目录。省略 folder 时放 `03-resources`。精确身份仍可用 subject、entity 参数传入；不能根据文件夹或正文自动推定主题。

已建立文章可在 Obsidian 中继续写作。正文模板只提供小节，不重复添加主标题。工具刷新不覆盖 PARA 内容、私人视图、模板或附件。

## 内容查找

```bash
uv run kb-obsidian-rdf articles \
  --vault /Users/xiu/Documents/knowledge-base \
  --field entities --term Obsidian

uv run kb-obsidian-rdf articles \
  --vault /Users/xiu/Documents/knowledge-base \
  --field subject --term 人工智能 --descendants
```

查询覆盖 PARA 四区，按真实元数据引用匹配；正文提及不算标引。下位展开只用于当前主题，按明确关系和文章身份去重，不能将历史版本套入当前层级。

## 内容检查

```bash
uv run kb-obsidian-rdf check \
  --vault /Users/xiu/Documents/knowledge-base
```

声明 identifier 的记录按内容模型校验。无声明文件保留，列明为未登记、未检查，不计为通过，也不自动判定其文档类型。已有身份声明但格式损坏或字段不合法时仍报错；普通未登记文件不阻止创建新文章。

检查报告位于库外状态的 reports 中，终端给出实际路径。查询只核对其明确的数据范围，不重跑 SHACL，也不把结构通过当成语义正确或正式准用。

## 库外状态

默认位置：

```text
output/obsidian-rdf/state/<库标识>/
├─ binding.json             绑定的库路径及实例 ID
├─ current.json             当前安装凭据
├─ current/
│  ├─ manifest.json
│  ├─ records.json
│  ├─ resources.json
│  ├─ projection.json
│  ├─ validation.json
│  └─ inputs/
├─ reports/
├─ receipts/
├─ product/
│  ├─ baseline.json          初始及显式维护写入的文件摘要
│  └─ operations/            每次维护的报告、候选及旧值备份
└─ backups/
```

中断时另有 `recovery.json`。状态不可当作普通构建缓存随意清理。所有命令可用 `--state-root /库外目录` 覆盖默认位置；读写时须使用一致的状态根目录。互斥锁位于目标库的父目录，同样在库外。

当前实现要求状态与库位于同一文件系统；不满足时写前拒绝，可显式选择同卷的库外状态目录。手工搬动库之后需要明确重新绑定，工具不会凭名称接管未知库。

## 条目更新

正式库先固定新的数据版本和当前已安装基准，再预览更新：

```bash
uv run kb-obsidian-rdf prepare \
  --mode formal \
  --source-root /Users/xiu/code/kb-design \
  --authority docs/applications/obsidian/决定-正式库创建.md \
  --entities output/vocabulary/entities/current \
  --previous-vault /Users/xiu/Documents/knowledge-base \
  --output build/obsidian-formal/next.json

uv run kb-obsidian-rdf refresh \
  --input build/obsidian-formal/next.json \
  --vault /Users/xiu/Documents/knowledge-base
```

默认只比较变化。关闭该库、暂停其他编辑与同步后，增加 `--apply --offline` 才切换。仅更新 `05-vocabulary` 与库外工程交付，配置、首页、视图和模板只给候选差异，文章不在写集内。已有身份保持已安装路径，改译名不等于批量改文章链接。

开发库刷新继续使用 preview 输入与开发路径。第 2 版布局须显式迁移，模式不同也不能普通刷新。条目刷新中断后执行 `recover --vault <明确目标> --offline`；恢复核对实际数据及引用，不删除用户内容，也不宣称跨目录事务或断电持久性。

## 产物维护

维护配置、首页与常用视图时，先预览：

```bash
uv run kb-obsidian-rdf maintain \
  --vault /Users/xiu/Documents/knowledge-base
```

默认只生成库外报告与候选，知识库文件不变。关闭目标库、停止同步和其他编辑后执行：

```bash
uv run kb-obsidian-rdf maintain \
  --vault /Users/xiu/Documents/knowledge-base --apply --offline
```

配置只补缺项，已有不同值和未知属性原样保留并报告。缺失的视图和模板可以建立；已有文件即使与候选只有格式差异也不重写，其他差异留作候选供审阅。首页只有在完全符合本工具记录的生成基准，或符合本次明确识别的旧版首页时才更新；用户修改的首页保留。

报告逐项列出文件、写入范围、差异、保留的设置、候选、备份、原摘要与实际结果，终端给出绝对路径。配置与首页的旧内容先备份，再逐文件写入并核对；基准独立保存在 `product/`，不进入词表交付清单。维护不刷新词表，词表刷新不维护配置；两种命令都不编辑文章及其引用。

维护失败后保留已有成果和当次备份，修复报告所述原因后重试同一 `maintain --apply --offline` 命令。重试重新核对现有文件，补齐尚缺项，保留后来改变的个人值；不使用词表的 `recover` 命令，也不宣称多个文件整体原子切换。

## 布局迁移

迁移脚本只接受第 2 版 PARA 开发实例，并将其转换为第 3 版编号布局。先准备计划：

```bash
uv run --package kb-obsidian-rdf python \
  apps/obsidian-rdf/scripts/migrate-numbered-layout.py \
  --vault output/obsidian-rdf/development-para
```

此命令只准备候选并输出 plan 文件的绝对路径，不改原库。计划保存在库外状态的 `layout-migrations/<operation-id>/` 下；应用时将完整原库与旧工程交付分别移入该目录的 `backup/`，另保留原绑定及安装凭据。

关闭目标库、停止同步及其他外部编辑后，使用输出的 plan 路径应用迁移：

```bash
uv run --package kb-obsidian-rdf python \
  apps/obsidian-rdf/scripts/migrate-numbered-layout.py \
  --plan '<输出的 plan 绝对路径>' --apply --offline
```

迁移移动顶层目录并同步内部链接、查询路径、身份对应、文件清单及摘要，保留对象 ID、文章 UUID、正文内容和内部文件名。脚本当前只支持完整路径形式的原生 wikilinks；需要改写的普通 Markdown 链接或示例中的旧路径会在准备时拒绝，不能通过批量替换绕过。

失败或中断时保留现场，使用同一条 `--plan … --apply --offline` 命令继续；布局迁移不使用普通 `recover` 命令恢复。

## 实例边界

`0.4.0` 使用第 3 版分离交付和编号目录，明确区分 preview 与 formal。正式实例表示已经获准按指定范围写作和使用词条，不改变来源事实核验、词表状态或内容状态。工程文件与校验报告继续在库外保存。

旧 development、development-usage 实例和原 kb-vault 保留原样；运行中的知识库不可清空重建。对旧开发实例的编号迁移见[迁移记录](../../work/plans/2026-09-23-obsidian-numbered-layout.md)，配置与视图维护见[独立维护验收](../../work/reviews/2026-09-24-maintenance-adoption.json)。正式创建的临时验收、实际写集和结果见[本次实施](../../work/plans/2026-09-24-formal-obsidian.md)。

```bash
uv run --package kb-obsidian-rdf --with pytest \
  pytest apps/obsidian-rdf/tests -q
```

依赖依据见 [DEPENDENCIES.md](DEPENDENCIES.md)。设计见[使用与维护](../../docs/applications/obsidian/提案-词表使用与维护.md)、[元数据](../../docs/applications/obsidian/提案-Obsidian%20元数据.md)、[导出合同](../../docs/applications/obsidian/提案-Obsidian%20导出与导入.md)与[产物维护](../../docs/applications/obsidian/设计-产物维护.md)。
