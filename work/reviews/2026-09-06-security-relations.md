# 安全来源关系

状态：待采纳。基线 `633f684`。仅完成当前 41 条映射、同记录派生及三个数组的有限核对；没有修改正式数据、实现或采纳记录。

## 核对方法

先读离线生成输入与范围注释，再按条目读取 CWE 4.20、ATT&CK 19.2 官方页及 ATLAS 2026.07 固定数据。逐条对照定义的对象、目的与范围；代码同名不作概念对应证明。全部准确旧值、字段身份、实际出处、范围判断及建议新值见[逐项记录](2026-09-06-security-relations.json)。

CWE 实际页标题标明 4.20；[ATT&CK 官方版本页](https://attack.mitre.org/resources/versions/)明确将 `/versions/v19` 标作 v19.2；ATLAS 使用已指定 [Git blob](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42)，核对 Git blob SHA-1 与 `collection.version=2026.07`。未下载全仓、登录、OCR 或操作真实 vault。

## 关系判断

41 条现有 exactMatch 的核心范围均有对应定义支持，建议保留，但仍需逐字段采纳。其中 Stealth 与 Defense Impairment 的边界须按 v19 解释；ATLAS 的 Defense Evasion 仍是其固定版本中的独立条目。摘要未展开全部例子不自动构成窄匹配；本报告也不为摘要未明说的范围扩张背书。

| 当前身份 | 外部条目 | 范围对应 |
|---|---|---|
| `improper-access-control` | [CWE-284](https://cwe.mitre.org/data/definitions/284.html) | 未实施和错误实施访问限制均在范围内；对象是未授权主体对资源的访问。 |
| `improper-interaction-between-multiple-correctly-behaving-entities` | [CWE-435](https://cwe.mitre.org/data/definitions/435.html) | 独立运行正确、集成后交互产生错误行为，是同一判据；不是一般组件自身错误。 |
| `improper-control-of-a-resource-through-its-lifetime` | [CWE-664](https://cwe.mitre.org/data/definitions/664.html) | 创建、使用、释放全过程的资源控制均对应；不是只指释放或泄漏。 |
| `incorrect-calculation` | [CWE-682](https://cwe.mitre.org/data/definitions/682.html) | 计算结果错误或非预期，且后用于安全关键决策或资源管理，两项限制均保留。 |
| `insufficient-control-flow-management` | [CWE-691](https://cwe.mitre.org/data/definitions/691.html) | 执行期间控制流管理不足而可被非预期改变，与原文因果和范围一致。 |
| `protection-mechanism-failure` | [CWE-693](https://cwe.mitre.org/data/definitions/693.html) | 保护机制未用或误用，未充分防御针对性攻击，与原文一致。 |
| `incorrect-comparison` | [CWE-697](https://cwe.mitre.org/data/definitions/697.html) | 两个实体的错误比较，并保留安全相关语境限制。 |
| `improper-check-or-handling-of-exceptional-conditions` | [CWE-703](https://cwe.mitre.org/data/definitions/703.html) | 罕见异常条件的预见与处理，两种缺陷均保留。 |
| `improper-neutralization` | [CWE-707](https://cwe.mitre.org/data/definitions/707.html) | 结构化消息或数据、上游读取或下游发送、格式与安全性质均对应；未确保概括未做及做错。 |
| `improper-adherence-to-coding-standards` | [CWE-710](https://cwe.mitre.org/data/definitions/710.html) | 开发编码规则不遵循及其造成衍生弱点或加重漏洞的后果均对应。 |
| `reconnaissance` | [TA0043](https://attack.mitre.org/versions/v19/tactics/TA0043/) | 事前收集信息以规划后续行动，与条目目的相同；区别于进入环境后的 Discovery。 |
| `resource-development` | [TA0042](https://attack.mitre.org/versions/v19/tactics/TA0042/) | 为行动建立资源，包含创建、购买、窃取；本地未排除其他取得方式。 |
| `initial-access` | [TA0001](https://attack.mitre.org/versions/v19/tactics/TA0001/) | 通过入口向量取得网络初始立足点，与定义一致。 |
| `execution` | [TA0002](https://attack.mitre.org/versions/v19/tactics/TA0002/) | 本地或远程系统执行攻击者控制的恶意代码，与定义一致。 |
| `persistence` | [TA0003](https://attack.mitre.org/versions/v19/tactics/TA0003/) | 跨重启、凭据变化及其他中断保持访问，与定义一致。 |
| `privilege-escalation` | [TA0004](https://attack.mitre.org/versions/v19/tactics/TA0004/) | 系统或网络的更高权限，与定义一致；未限定某一提权方法。 |
| `stealth` | [TA0005](https://attack.mitre.org/versions/v19/tactics/TA0005/) | 隐藏行为并混入正常活动对应 Stealth；官方特别排除干扰安全控制，该细节本地摘要未展开，不能解释为包含 TA0112。 |
| `defense-impairment` | [TA0112](https://attack.mitre.org/versions/v19/tactics/TA0112/) | 削弱安全机制及观测可信性对应 Defense Impairment；区别于仅隐藏正常外观的 TA0005。 |
| `credential-access` | [TA0006](https://attack.mitre.org/versions/v19/tactics/TA0006/) | 窃取账户名、口令等凭据对应 Credential Access；并非一般访问控制。 |
| `discovery` | [TA0007](https://attack.mitre.org/versions/v19/tactics/TA0007/) | 了解已进入的系统与内部网络对应 Discovery；本地摘要未展开入侵后的阶段语境。 |
| `lateral-movement` | [TA0008](https://attack.mitre.org/versions/v19/tactics/TA0008/) | 进入并控制远程系统以及环境内移动，对应横向移动范围。 |
| `collection` | [TA0009](https://attack.mitre.org/versions/v19/tactics/TA0009/) | 收集与攻击目标相关的数据，对应 Collection；未把收集自动等同外传。 |
| `command-and-control` | [TA0011](https://attack.mitre.org/versions/v19/tactics/TA0011/) | 与受控系统通信以控制它们，对应 Command and Control；通信目的限制保留。 |
| `exfiltration` | [TA0010](https://attack.mitre.org/versions/v19/tactics/TA0010/) | 从目标网络窃取数据，对应 Exfiltration；与单纯收集区分。 |
| `impact` | [TA0040](https://attack.mitre.org/versions/v19/tactics/TA0040/) | 操纵、中断或破坏系统及数据、损害可用性或完整性，对应 Impact。 |
| `reconnaissance-artificial-intelligence` | [AML.TA0002](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 收集目标 AI 系统信息以规划行动。 |
| `resource-development-artificial-intelligence` | [AML.TA0003](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 建立可支持攻击的资源，AI 场景由本地数组语境承接。 |
| `initial-access-artificial-intelligence` | [AML.TA0004](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | AI 系统初始访问，网络、移动或边缘场景均对应。 |
| `ai-model-access` | [AML.TA0000](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | AI 模型的不同程度访问，为后续攻击提供条件。 |
| `execution-artificial-intelligence` | [AML.TA0005](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | AI 制品或软件中的恶意代码执行。 |
| `persistence-artificial-intelligence` | [AML.TA0006](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 通过 AI 制品或软件维持访问。 |
| `privilege-escalation-artificial-intelligence` | [AML.TA0012](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 取得更高权限，AI 语境由所属矩阵承接。 |
| `defense-evasion` | [AML.TA0007](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 规避 AI 安全软件检测；不能套用 ATT&CK v19 的改名。 |
| `credential-access-artificial-intelligence` | [AML.TA0013](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 窃取凭据，AI 语境由所属矩阵承接。 |
| `discovery-artificial-intelligence` | [AML.TA0008](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 了解目标 AI 环境；定义包含系统和内部网络。 |
| `lateral-movement-artificial-intelligence` | [AML.TA0015](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 在 AI 环境移动并访问控制其他系统或组件。 |
| `collection-artificial-intelligence` | [AML.TA0009](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 收集 AI 制品与相关信息，区别于外传。 |
| `ai-attack-staging` | [AML.TA0001](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 利用目标知识和访问来准备针对 AI 模型的攻击。 |
| `command-and-control-artificial-intelligence` | [AML.TA0014](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 与受控 AI 系统通信以控制它们。 |
| `exfiltration-artificial-intelligence` | [AML.TA0010](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 窃取 AI 制品或系统信息。 |
| `impact-artificial-intelligence` | [AML.TA0011](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) | 影响 AI 系统和数据，包含削弱信任。 |

## 派生依据

派生逐条保存在 `derivation_review`，与 `relation_review` 分开。现有 extra-arrays 的源条目和 scope-zh 的定义摘要，经生成器进入当前记录；此次官方条目核对支持这条实际生成链的语义对应。建议为每条 source 写明 registry、item、定位和本次核对日期。此证据不证明历史月份曾做同样的外部核验，不倒签 checked，也不自动批准 structure 角色或修改模型知识译名。

## 数组依据

| 数组 | 核对结果 |
|---|---|
| `security-cwe` | 图中十个顶层 Pillar 与本地成员逐一对应。外部分组定位须明确顶层 Pillar 子集，不得把本地数组等同整个 View-1000。 [实际出处](https://cwe.mitre.org/data/definitions/1000.html) |
| `security-attack` | Enterprise 战术表包含十五项，并含 TA0005 Stealth 与 TA0112 Defense Impairment；不是旧版十四战术表。 [实际出处](https://attack.mitre.org/versions/v19/tactics/enterprise/) |
| `artificial-intelligence-atlas` | 固定集合的 tactics 字典对应本地十六项；并非拿 ATT&CK 战术复用到 AI，也不混入 technique。 [实际出处](https://api.github.com/repos/mitre-atlas/atlas-data/git/blobs/275c840f6e6ccc2b7be9fe8607fdc3344c242a42) |

三个数组建议改用明确 external_group，保留原 id、superordinate 和成员。CWE 必须定位到 View-1000 的顶层 Pillar 子集；ATT&CK 是 Enterprise 战术集合；ATLAS 是固定集合的全部 tactics。外部分组不证明本地 security 或 artificial-intelligence 归属，不能用数组证据替代成员 source 或 match。

## 采纳边界

当前没有发现需改变映射方向的定义冲突；建议值仍为审查提案。来源用途、项目父项归属和中文名称各有独立效力，不由这次关系核对采纳。未运行测试、生成器或正式切换；取证文件保存在 Git 忽略的 build/source-verification，审查 JSON 保存了实际 URL、定位、哈希与旧记录快照。
