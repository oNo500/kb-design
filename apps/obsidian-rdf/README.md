# Obsidian 词表应用 (Obsidian Vocabulary Use)

`kb-obsidian-rdf` 为 PARA 知识库提供词条生成、选择、引用和检索。知识库保存文章、资料和可用条目；原始词表、版本清单、校验报告和恢复资料保存在库外。

## 文件结构

```text
development-para/
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
│  └─ recently-modified.base
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

## 开发库生成

从工具所在仓库根目录执行：

```bash
uv run kb-obsidian-rdf prepare \
  --source-root /Users/xiu/code/kb-design \
  --authority apps/obsidian-rdf/inputs/开发预览范围.md \
  --output build/obsidian-para/input.json

uv run kb-obsidian-rdf init \
  --input build/obsidian-para/input.json \
  --vault output/obsidian-rdf/development-para
```

输入准备核对三份既有 RDF 交付及辅助元数据词表，不修改原始数据。初建只接受空目标；其他 RDF 可以提供符合[输入合同](../../docs/applications/obsidian/提案-Obsidian%20导出与导入.md#输入清单)的清单。

在 Obsidian 中把生成目录作为库打开，从 `home.md` 开始。模板功能通过 Obsidian 的 Templates 核心插件使用；工具不接管已有的插件开关。正式目录以后通过 `--vault` 显式指定，指定目录不会自动批准正式数据采用。

## 常用视图

收件箱只显示 `00-inbox` 下的 Markdown 文件，允许没有文章属性的临时笔记。草稿显示 PARA 四区中声明小写 UUIDv4 identifier 且 status 为 draft 的文章；最近修改覆盖同样声明 UUID 的文章，按文件实际修改时间从新到旧排序。两者均排除收件箱与词条目录。UUID 筛选不代替内容校验，也不表示正式准用。

既有文章列表保留，用于查看 PARA 四区中的 Markdown 文件，包含自由笔记。所有视图都可由用户调整，普通词表刷新不会覆盖这些调整。

## 条目选择

```bash
uv run kb-obsidian-rdf search \
  --vault output/obsidian-rdf/development-para \
  --field subject --query 人工智能

uv run kb-obsidian-rdf get \
  --vault output/obsidian-rdf/development-para \
  --field entities --term JavaScript --link
```

先限定字段，再查名称或别名：subject 查主题，entities 查实体，type、genre、form、references 分别查对应值域。省略 search 的 query 可列选项；默认排除不可新选用记录。

get 的 link 输出可粘贴到文章属性，例如 `[[05-vocabulary/entities/javascript|JavaScript]]`。同名不唯一时返回候选，不自动选择；用 `--ref` 指定明确身份或路径。`--json` 返回结构化摘要，`--details` 才展开完整条目信息。

## 文章建立

```bash
uv run kb-obsidian-rdf new \
  --vault output/obsidian-rdf/development-para \
  --folder 01-projects/knowledge-base \
  --title 'JavaScript 数组排序教程' \
  --type tutorial --genre background \
  --subject-name '排序与查找' --entity-name JavaScript
```

工具分配 UUID、日期和 draft，按原身份核对选择，再写入指定的 PARA 目录。省略 folder 时放 `03-resources`。精确身份仍可用 subject、entity 参数传入；不能根据文件夹或正文自动推定主题。

已建立文章可在 Obsidian 中继续写作。正文模板只提供小节，不重复添加主标题。工具刷新不覆盖 PARA 内容、私人视图、模板或附件。

## 内容查找

```bash
uv run kb-obsidian-rdf articles \
  --vault output/obsidian-rdf/development-para \
  --field entities --term JavaScript

uv run kb-obsidian-rdf articles \
  --vault output/obsidian-rdf/development-para \
  --field subject --term 人工智能 --descendants
```

查询覆盖 PARA 四区，按真实元数据引用匹配；正文提及不算标引。下位展开只用于当前主题，按明确关系和文章身份去重，不能将历史版本套入当前层级。

## 内容检查

```bash
uv run kb-obsidian-rdf check \
  --vault output/obsidian-rdf/development-para
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

当前开发版要求状态与库位于同一文件系统；不满足时写前拒绝，可显式选择同卷的库外状态目录。手工搬动库之后需要明确重新绑定，工具不会凭名称接管未知库。

## 条目更新

```bash
uv run kb-obsidian-rdf prepare \
  --source-root /Users/xiu/code/kb-design \
  --authority apps/obsidian-rdf/inputs/开发预览范围.md \
  --previous-vault output/obsidian-rdf/development-para \
  --output build/obsidian-para/next.json

uv run kb-obsidian-rdf refresh \
  --input build/obsidian-para/next.json \
  --vault output/obsidian-rdf/development-para
```

默认只比较变化。关闭该库、停止同步与其他编辑后，增加 `--apply --offline` 才切换。仅更新 `05-vocabulary` 与库外工程交付；配置、首页、视图和模板只给候选差异，不执行产物维护。已有身份保持既有路径，改译名不等于批量改文章链接。第 2 版实例须先显式迁移，普通刷新不自动增加目录编号。

条目刷新中断后保留现场，执行 `recover --vault <目录> --offline`。恢复核对两个位置的实际版本和新增引用，不通过删除用户内容来恢复，也不宣称跨目录事务或断电持久性。

## 产物维护

维护配置、首页与常用视图时，先预览：

```bash
uv run kb-obsidian-rdf maintain \
  --vault output/obsidian-rdf/development-para
```

默认只生成库外报告与候选，知识库文件不变。关闭目标库、停止同步和其他编辑后执行：

```bash
uv run kb-obsidian-rdf maintain \
  --vault output/obsidian-rdf/development-para --apply --offline
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

## 开发边界

本版为 `0.3.0.dev0`，使用第 3 版分离交付与编号目录。旧的 development、development-usage 实例仍保留原样，不在上述布局迁移范围内，也不由普通刷新迁移。

本版用于开发实例，正式库切换另行决定。程序只生成初始结构及明确的受管理条目，运行中的知识库不是可清空重建的目录；版本说明和目录合同不表示某个既有实例已经迁移。

此前 `0.2.0.dev0` 的验证结果为 164 项行为检查通过，2,779 个知识生成文件与 15 个工程交付文件重建一致；当时的新库内没有工具的 TTL、JSON 清单或运行报告。该结果不作为第 3 版或本次迁移的验证结论，历史证据见[实施记录](../../work/plans/2026-09-23-obsidian-para-layout.md#验证结果)。

`0.3.0.dev0` 已通过 164 项原有行为测试及 11 项迁移检查，`development-para` 已完成编号迁移。原身份与输入保留，Obsidian 未解析链接为 0，文章查询及 Base 均能找到原示例。实际写集、备份和刷新预览见[编号迁移记录](../../work/plans/2026-09-23-obsidian-numbered-layout.md)。

```bash
uv run --package kb-obsidian-rdf --with pytest \
  pytest apps/obsidian-rdf/tests -q
```

依赖依据见 [DEPENDENCIES.md](DEPENDENCIES.md)。设计见[使用与维护](../../docs/applications/obsidian/提案-词表使用与维护.md)、[元数据](../../docs/applications/obsidian/提案-Obsidian%20元数据.md)和[导出合同](../../docs/applications/obsidian/提案-Obsidian%20导出与导入.md)。
