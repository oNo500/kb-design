# Obsidian 词表应用 (Obsidian Vocabulary Use)

`kb-obsidian-rdf` 为 PARA 知识库提供词条生成、选择、引用和检索。知识库保存文章、资料和可用条目；原始词表、版本清单、校验报告和恢复资料保存在库外。

## 文件结构

```text
development-para/
├─ home.md
├─ inbox/
├─ projects/
├─ areas/
├─ resources/
├─ archives/
├─ vocabulary/
│  ├─ concepts/
│  ├─ entities/
│  ├─ document-types/
│  ├─ genres/
│  ├─ forms/
│  └─ references/
├─ views/article-list.base
├─ templates/article.md
└─ attachments/
```

新文件和目录使用小写，空格与下划线替换为中划线。中文保留，页面 title、名称及原始 ID 不变。例如标题“JavaScript 数组排序教程”对应文件 `javascript-数组排序教程.md`。词条同目录重名以身份短摘要区分；文章同名不会覆盖，需作者明确区分。

`inbox` 用于自由捕获，PARA 四区按用途组织内容，`vocabulary` 跨目录共同使用。归档不改文章 UUID、status 或条目状态；文件夹名称不自动成为主题。Obsidian 自己的 `.obsidian/` 配置由应用维护。

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

在 Obsidian 中把生成目录作为库打开，从 `home.md` 开始。正式目录以后通过 `--vault` 显式指定，指定目录不会自动批准正式数据采用。

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

get 的 link 输出可粘贴到文章属性，例如 `[[vocabulary/entities/javascript|JavaScript]]`。同名不唯一时返回候选，不自动选择；用 `--ref` 指定明确身份或路径。`--json` 返回结构化摘要，`--details` 才展开完整条目信息。

## 文章建立

```bash
uv run kb-obsidian-rdf new \
  --vault output/obsidian-rdf/development-para \
  --folder projects/knowledge-base \
  --title 'JavaScript 数组排序教程' \
  --type tutorial --genre background \
  --subject-name '排序与查找' --entity-name JavaScript
```

工具分配 UUID、日期和 draft，按原身份核对选择，再写入指定的 PARA 目录。省略 folder 时放 resources。精确身份仍可用 subject、entity 参数传入；不能根据文件夹或正文自动推定主题。

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

默认只比较变化。关闭该库、停止同步与其他编辑后，增加 `--apply --offline` 才切换。仅更新 vocabulary 与库外工程交付；首页、视图和模板只给候选差异，不覆盖用户修改。已有身份保持既有路径，改译名不等于批量改文章链接。

中断后保留现场，执行 `recover --vault <目录> --offline`。恢复核对两个位置的实际版本和新增引用，不通过删除用户内容来恢复，也不宣称跨目录事务或断电持久性。

## 开发边界

本版为 `0.2.0.dev0`，使用第 2 版分离交付。旧的 development、development-usage 实例保留原样，本版不静默搬出它们的工程数据或重命名旧文件；旧实例迁移另行列出写集。

本轮仅验证新开发实例，正式库未修改，不做视觉检查。程序只生成初始结构及明确的受管理条目，运行中的知识库不是可清空重建的目录。

本轮 164 项行为检查通过；2,779 个知识生成文件与 15 个工程交付文件重建一致。新库内没有工具的 TTL、JSON 清单或运行报告。验证和已知边界见[实施记录](../../work/plans/2026-09-23-obsidian-para-layout.md#验证结果)。

```bash
uv run --package kb-obsidian-rdf --with pytest \
  pytest apps/obsidian-rdf/tests -q
```

依赖依据见 [DEPENDENCIES.md](DEPENDENCIES.md)。设计见[使用与维护](../../docs/applications/obsidian/提案-词表使用与维护.md)、[元数据](../../docs/applications/obsidian/提案-Obsidian%20元数据.md)和[导出合同](../../docs/applications/obsidian/提案-Obsidian%20导出与导入.md)。
