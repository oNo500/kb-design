# 应用安全关系

状态：待人采纳。取证日期为 2026-09-06，未改正式数据，未审批角色或关系。逐项旧值、原文定位、语义比较、建议值和阻断见[完整记录](2026-09-06-owasp-relations.json)。

## 材料版本

ASVS 只取得一份官方固定 release JSON，未批量下载章节。JSON 的 Version 为 5.0.0；17 章与本地“5.0”输入逐项对应，建议本次迁移明确选用 5.0.0。它不能证明旧输入与正式 release 字节一致。LLM 逐项阅读 2025 目录和详情，Misinformation 详情读取失败，只有目录摘要。

[ASVS 发布数据](https://github.com/OWASP/ASVS/releases/download/v5.0.0_release/OWASP_Application_Security_Verification_Standard_5.0.0_en.json)；[LLM 风险目录](https://genai.owasp.org/llm-top-10/)。ASVS 原始字节哈希和路径在 JSON 中；网页未保存原始响应，不伪造其哈希。

## 映射比较

表中 proposed 仅为建议，不是已采纳或正式可用；blocked 项不生成建议 after。

| 本地对象 | 外部对象 | 处置 | 语义比较 |
|---|---|---|---|
| `cryptography` | `asvs:V11` | blocked | 外部章要求安全实现、加密、哈希、随机数、公钥和使用中数据保护；本地 cryptography 无 scope，来自 CS2023 SEC-Crypto，同名合并不是两个范围完全等同的证据。 |
| `encoding-and-sanitization` | `asvs:V1` | proposed | 编码、注入防御、净化、内存与非托管代码、安全反序列化组成该章；本地 scope 明确限定 ASVS 第 1 章，不把它当一般文本编码。 |
| `validation-and-business-logic` | `asvs:V2` | proposed | 输入验证、业务流程安全与反自动化对应本地输入预期、步骤不可绕过及自动化攻击控制。 |
| `web-frontend-security` | `asvs:V3` | proposed | 浏览器上下文解释、cookie、浏览器安全头、同源隔离与资源完整性对应本地 Web 前端攻击边界。 |
| `api-and-web-service` | `asvs:V4` | proposed | HTTP 消息结构、GraphQL、WebSocket 等服务安全要求对应本地面向消费者的 API 安全；本地举例不是穷尽列举。 |
| `file-handling` | `asvs:V5` | proposed | 上传、存储、下载及类型尺寸约束对应本地文件处理与拒绝服务、未授权读取风险。 |
| `authentication` | `asvs:V6` | proposed | 口令、认证因素生命周期、MFA、带外与身份提供方要求对应本地认证与抗冒充；本次关系比较不重新批准本地 NIST 占比陈述。 |
| `session-management` | `asvs:V7` | proposed | 令牌验证、超时、终止、防滥用与联合再认证对应本地会话唯一、失效和闲置超时边界。 |
| `authorization` | `asvs:V8` | proposed | 功能、数据及字段授权与可信服务层实施对应本地授权规则与最小权限。 |
| `self-contained-tokens` | `asvs:V9` | proposed | 签名或 MAC 完整性、算法限制、时间与接收上下文验证对应本地自包含令牌声明的信任条件。 |
| `oauth-and-oidc` | `asvs:V10` | proposed | OAuth 客户端、资源服务器、授权服务器、OIDC 客户端与提供方、同意管理对应本地委托授权与身份层安全要求。 |
| `secure-communication` | `asvs:V12` | proposed | TLS 版本与套件、对外 HTTPS、服务间通信要求对应本地传输保护范围。 |
| `configuration` | `asvs:V13` | proposed | 后端通信认证、机密管理与非预期信息泄漏对应本地应用配置安全；关系比较不证明所有默认配置已经安全。 |
| `data-protection` | `asvs:V14` | proposed | 数据分类、通用保护与客户端清理对应本地保护对象和客户端未授权访问边界。 |
| `secure-coding-and-architecture` | `asvs:V15` | proposed | 架构依赖、防御性编码与安全并发对应本地应用设计开发安全要求。 |
| `security-logging-and-error-handling` | `asvs:V16` | proposed | 日志文档、事件、保护及安全失败对应本地检测调查与错误处理。 |
| `webrtc` | `asvs:V17` | proposed | TURN、媒体与信令三个部分对应本地实时通信基础设施安全；本地 scope 已明确这是 ASVS 第 17 章。 |
| `prompt-injection` | `owasp-llm-top10:LLM01:2025` | proposed | 原文限定输入使 LLM 行为或输出发生非预期改变，含直接与间接输入；本地来自该风险条目，在 AI 数组内，没有额外扩大定义的 scope。可按这个来源限定的风险概念建议保留关系。 |
| `sensitive-information-disclosure` | `owasp-llm-top10:LLM02:2025` | blocked | 原文涉及 LLM 及应用的个人、商业、凭证等敏感数据输出；本地无 scope，名称可能被理解为一般信息泄露。需要明确保留的是该 LLM 风险范围，不能单凭同名批准 exactMatch。 |
| `supply-chain` | `owasp-llm-top10:LLM03:2025` | blocked | 原文聚焦 LLM 训练数据、预训练模型、第三方依赖与部署平台的供应链风险；本地仅名为供应链、无 scope，不能证明其限定为风险而不是整个供应链概念。 |
| `data-and-model-poisoning` | `owasp-llm-top10:LLM04:2025` | proposed | 原文涵盖预训练、微调、嵌入数据操纵与模型后门；本地由该 2025 风险条目建立，无其他范围或合并来源，可建议保留这个来源限定的风险对应。 |
| `improper-output-handling` | `owasp-llm-top10:LLM05:2025` | proposed | 原文明确 LLM 输出进入下游前的验证、净化与处理不足，并区别于过度依赖；本地由该风险建立且无其他范围，可建议在此边界内保留对应。 |
| `excessive-agency` | `owasp-llm-top10:LLM06:2025` | blocked | 原文包含过多功能、权限和自主性三类根因；本地中文“过度授权”且无 scope 可能只表达权限。需明确完整概念边界与既有译名处置，不能自动采纳 exactMatch。 |
| `system-prompt-leakage` | `owasp-llm-top10:LLM07:2025` | blocked | 原文重点是系统提示含敏感信息及底层控制缺陷，并明确系统提示文字泄露本身不是核心风险；本地无 scope，需排除仅指提示文字可见性的解释。 |
| `vector-and-embedding-weaknesses` | `owasp-llm-top10:LLM08:2025` | proposed | 原文限定 RAG 中向量和嵌入生成、存储、检索弱点，可影响信息访问或模型输出；本地由该风险建立，无其他范围，可建议保留来源限定的对应。 |
| `misinformation` | `owasp-llm-top10:LLM09:2025` | blocked | 2025 目录标题与摘要可读；详情页后续两次读取失败，未取得完整定义边界。本地“信息误导”无 scope，不以目录摘要填成完整关系证据。 |
| `unbounded-consumption` | `owasp-llm-top10:LLM10:2025` | proposed | 原文限定 LLM 应用允许过量且不受控推理，含拒绝服务、经济损失与模型窃取；本地由该风险建立，无其他范围，可建议按该范围保留对应。 |

## 实际派生

26 项 source 分别记录输入 JSON 指针、生成器建立路径与外部章节／风险原文位置。派生建议只确认本地记录由这些条目建立，不批准 rel、译名、scope、broader 或 status。cryptography 保留主 source:cs2023，不补造 ASVS 派生。LLM09 的记录来历可由目录和输入核实，但其完整映射仍阻断。

## 数组边界

两个数组分别保存外部集合身份、输入成员顺序及当前文档成员顺序。external_group 使用 structure 资格，不能新增 group 代替。ASVS cryptography 在全局主题表提前出现，当前文档顺序与 V1–V17 不同；成员集合相同不能宣称顺序已保存。集合 item 使用已读发布数据或列表地址，不自造外部集合代码；可变列表的 2025 身份由正文及 checked 限定。

## 采纳条件

版本与 mapping／structure 用途可以集中提案，但不自动批准关系。ASVS cryptography 的 CS2023 合并范围、LLM 的一般信息泄露／供应链范围、过度授权译名与完整 agency 的区别、系统提示泄露的风险边界，以及未取得的 Misinformation 定义分别保留阻断。LLM 其他建议只适用于来源限定的 2025 风险概念，不授权未来按广义名称扩大范围。

本记录不是完整来源实体候选，source_status、其他字段与角色仍由总提案处理；不因本批条目可定位而宣称全部来源或全部关系已核。

## 有限复核

以下补充结论仅更新 LLM02、LLM03、LLM07、LLM09 和 LLM06 的映射建议；前文保存初次审查历史，当前建议以本节及 JSON 的 followup 为准。未重抓原文，没有新增外部 checked。

LLM02、LLM03、LLM07 的本地记录都是唯一来源与唯一映射，双语语言依据指向同一个 2025 风险代码，只有 artificial-intelligence 父项及对应数组，无其他来源合并或相反 scope。初次审查仅因没有 scope 而假设广义名称会扩大概念，门槛过高。现建议保留来源限定的 exactMatch；原文中的风险限定留在相邻依据，不改 ID 或创建新概念。

| 对象 | 当前建议 | 具体依据与限制 |
|---|---|---|
| LLM02 | proposed exactMatch | 未见一般信息泄露范围断言；沿用已读 LLM 及应用敏感数据风险定义 |
| LLM03 | proposed exactMatch | 未见一般供应链管理范围断言；身份由 LLM03:2025 与唯一来源限定 |
| LLM07 | proposed exactMatch | 未见“所有提示文字必须保密”的本地断言；原文敏感信息及底层控制缺陷边界保留 |
| LLM09 | proposed exactMatch，限源限定条目身份 | 已读官方 2025 目录的代码、名称、摘要，加本地唯一来源的建入路径，可确认同一风险条目；详情页失败保留，不声称完整定义、案例或缓解内容已核 |
| LLM06 | blocked | 中文“过度授权”与原文功能、权限、自主性三维存在具体表示偏差，继续独立处置；不以来源限定原则掩盖 |

五项精确 v2 建议值或 blocked 原因见 JSON followup；原 records 不覆盖。建议不是采纳，角色及具体关系仍待决定，原 unassigned 状态、译名与其他字段全部保留。未来出现跨来源合并或范围扩张时重新判断，不把本节当作普遍放行同名关系的规则。
