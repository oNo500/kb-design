# PARA 应用布局

用户批准以 PARA 组织主要内容，词条作为共用支持，并将工程数据全部放在库外；新生成的文件和文件夹使用小写与中划线。保留源 title、名称和身份原值，不更改词表内容或既有正式库。只建立新的开发实例，不做视觉检查，不自动迁移旧实例，不提交。

## 使用结构

库内为 home.md、inbox、projects、areas、resources、archives、vocabulary、views、templates、attachments。vocabulary 下只有供引用的 concepts、entities、document-types、genres、forms、references 页面；明确历史引用所需的知识页可以保留，但原始图、工程备份与登记不进入库。概念体系和集合保留在源数据及库外资源记录中，不直接生成用户目录。

PARA 四区共享原有文章字段和稳定 UUID；归档位置不自动改变 status 或词条可用性。inbox 是自由捕获区域，不自动视为已进入内容模型。生成器只提供初始结构与配套页面，用户文章与私人修改永久保留。

## 交付接口

`common.Delivery(vault_files: dict[str,bytes], state_files: dict[str,bytes])` 明确区分两套文件。vault_files 包含初始 home/views/templates 与 vocabulary 页面；state_files 包含 inputs、records.json、projection.json、validation.json、resources.json、manifest.json。manifest format_version=2，files 只列受管理的 vocabulary 文件，state_files 列外部数据文件且不包含 manifest 自身。records 内部格式仍为 1。

`layout.py` 集中目录常量与映射。记录 kind 保持 concepts/entities/types/genres/forms/references，types 的目录映射为 document-types；不改概念或实体身份。

`storage.state_directory(vault, state_root=None)` 定位库外实例记录。默认 state_root 为工具所在项目的 output/obsidian-rdf/state，支持显式参数及 KB_OBSIDIAN_STATE_ROOT。实例目录按规范化绝对路径派生键，binding.json 保存工具实例 ID 和目标路径；没有库内 marker。不静默重新绑定移动过的库。

外部实例目录包含 binding.json、current.json、current/（本次完整 state_files）、receipts、reports、backups、recovery.json。状态目录必须在库外，禁止符号链接、祖先路径包含及写集交叉。当前实现要求状态与目标处于同一文件系统，可显式选同卷的库外 state_root；不宣称跨文件系统事务。

`initialize/inspect/refresh/recover/vault_lock` 沿用现有参数并增加 state_root=None。inspect 返回 manifest、manifest_sha256、records、receipt、pending、vault、state_dir、files、state_files。可提供 `read_state(vault,state_root=None)` 进行只核外部绑定、凭据、manifest、records 的快读；具体页面核验仍独立，不把快读当全库通过。

`query`、`content` 公共入口增加 state_root=None。文章读取递归扫描 projects/areas/resources/archives，排除 inbox、vocabulary、views、templates、attachments。new_content 增加 folder='resources'，只允许 PARA 四区中的明确目录；生成文件名为小写中划线，title 与 UUID 保留。source、subject、实体、类型等原有语义与约束不变。

prepare 的 previous_delivery 使用 `{path: vault绝对路径, state_root: 状态根目录绝对路径, sha256: 当前manifest摘要}`。build.read_previous 通过新的绑定读取固定旧交付，不读取旧库内工程文件；不默默迁移第 1 版实例。需要迁移时另列写集。

## 写入保护

初建只接受空目标和未占用的状态实例，首次更改前保存可恢复记录。刷新只替换 vocabulary 和外部 current 状态，不覆盖 PARA 内容、home、views、templates、attachments 或 Obsidian 自身配置。用户资料、候选差异和原始输入不能混写进库。

恢复核对实际文件与记录，保护中断后新增引用，保留阶段备份；不能通过清空用户内容来恢复。目录切换与外部状态之间存在中断窗口，以恢复记录与读写门禁处理，不宣称整库跨目录事务或断电持久性。

## 执行分工

- [x] 生成与命名：Delivery 拆分、小写中划线路径、PARA 初始文件、源信息完整保留。
- [x] 库外状态：绑定、核验、初建、刷新与恢复，只管理明确写集。
- [x] 内容与查询：四区扫描、指定目录建立、跨目录查询，归档不推断状态。
- [x] 命令与文档：state-root 参数、报告外移、设计与 README 整理。
- [x] 整体验证：新开发库不含工程数据，同名与大小写冲突保护，创建查询与更新恢复，以及固定输入重建一致。

## 检查依据

错误路径会写入或覆盖私人资料；用非空目标、重叠目录、符号链接及双实例验证。中断会导致内容和外部索引错版；用实际阶段故障注入验证恢复。PARA 扫描错误会漏查文章或把词条当文章；用四区相同主题、归档及自由捕获记录验证。命名错误会串身份；用大小写、空格、中划线、Unicode 与同名记录验证。现有写入、历史及语义测试保留，按新交付形式迁移，避免为包装函数重复造测试。

## 识别边界

PARA 四区也保存普通资料。应用以顶层 identifier 声明识别待校验文章；未声明的文件明确列为未登记、未检查，不推定资料类型或计为通过。删除原文章身份也会列入此清单，受控引用指向它仍报错；声明了无效身份或损坏字段的记录仍按原规则报错。这是应用读取范围，不授予正式资格，不改变内容模型的必填约束。

## 验证结果

- 独立审查未发现新增高风险缺陷；补齐了默认终端与 Markdown 报告的未登记覆盖说明。164 项行为测试通过，包含真实阶段中断、资料引用保护、命名、四区扫描及归档后身份保持。
- 新库位于 `output/obsidian-rdf/development-para/`，工程状态位于 `output/obsidian-rdf/state/4893c6f8f87f714e24a7fb99ff57989d5e20f6b0671220f1b479b6e43aefc7a8/`。旧实例和正式库没有修改。
- 初始库内 2,779 个文件全部为知识 Markdown 或 Base；没有大写、空格、下划线文件名，没有 TTL、JSON 清单或运行报告。包含 2,365 个概念、302 个实体及既有辅助条目。
- 2,779 个知识生成文件与 15 个工程交付文件重建字节一致；第二次生成耗时 33.46 秒。结果见 `build/obsidian-para/rebuild-check.json` 和 `layout-check.json`。
- 通过名称建立 `projects/demo/javascript-数组排序教程.md`，title 保留“JavaScript 数组排序教程”；文章检索找到该记录。检查 0 错误，2 条正式准用未确认，报告保存于库外。
- 已用实际外部绑定执行 prepare 的 previous-vault 路径，确认下一版输入引用外部 state_root 与 manifest。没有执行实际开发库的版本切换；切换与恢复由行为测试验证。
- 未做视觉检查，未提交。当前 0.2.0.dev0／格式 2，不自动迁移旧格式实例；状态与目标同文件系统等工程限制见应用 README。
