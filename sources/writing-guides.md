# 写作规范阅读笔记

读了六份写作规范,按「原则 → 中文书面语 → 技术写作 → 文档分类」四层提炼可用规则,每条标原始出处。目的是给概念文「写作规范」和 `design/writing.md` 提供依据。

本文自身按这些规则写,标点用全角。

## 读了什么

| 来源 | 层 | 覆盖 | 档位 |
|---|---|---|---|
| [ISO 24495-1:2023 Plain language — Part 1](https://www.iso.org/standard/78907.html) | 原则 | 写作的四条原则 | de-jure;正文未读,四原则据 [IPLF 摘要](https://www.iplfederation.org/iso-standard/) |
| [GB/T 15834-2011《标点符号用法》](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=22EA6D162E4110E752259661E1A0D0A8) | 中文书面语 | 标点的形式与用法 | de-jure;已读 §4.8–4.14 |
| [W3C《中文排版需求》clreq](https://www.w3.org/TR/clreq/) | 中文书面语 | 中西文混排、字距 | de-facto(W3C Group Note Draft,2026-08-04);已读 §6.3.3 |
| [Google developer documentation style guide](https://developers.google.com/style) | 技术写作 | 语气、语法、标题、列表、表格、链接 | de-facto;已读 highlights、headings、tables |
| [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice) | 技术写作 | 简洁、语气、大小写、标点 | de-facto;已读 top 10 |
| [Diátaxis](https://diataxis.fr/) | 文档分类 | 四类文档及其写法 | de-facto;已读 start-here、explanation、reference |

阮一峰《中文技术文档的写作规范》曾作为来源,已废弃:其可引条目均转述自 GB/T 15834、clreq 或企业内规,无自有原理;句长 20/30/40 字、段落不超七行等数字规则源头是某企业规范,本库不采用。

## 原则

ISO 24495-1:2023 的四条:

| 原则 | 含义 |
|---|---|
| Relevant 相关 | 读者得到他们需要的 |
| Findable 可找到 | 读者能轻易找到需要的 |
| Understandable 可理解 | 读者能轻易理解找到的 |
| Usable 可使用 | 读者能轻易使用这些信息 |

下面各层的规则都可归到这四条之一。

## 中文书面语

| 规则 | 出处 | 原则 |
|---|---|---|
| 中文句子用全角标点 | GB/T 15834 §4 各条形式 | 可理解 |
| 引号用“ ”,内层‘ ’;竖排用﹃﹄﹁﹂。「」不在国标内 | GB/T 15834 §4.8 | 可理解 |
| 括号主要形式全角（）;方括号［］、六角括号〔〕、方头括号【】另有用途;避免套用同形括号 | GB/T 15834 §4.9 | 可理解 |
| 破折号——占两字位 | GB/T 15834 §4.10 | 可理解 |
| 省略号……六点占两字位 | GB/T 15834 §4.11 | 可理解 |
| 连接号:短横线-半字位(号码、化合物);一字线―一字位(起止);浪纹线～一字位(数值范围) | GB/T 15834 §4.13 | 可理解 |
| 间隔号·半字位,外国人名、书名与篇名分界 | GB/T 15834 §4.14 | 可理解 |
| 汉字与西文字母、欧洲数字之间留不超过四分之一汉字宽的间距;Markdown 中以半角空格实现 | clreq §6.3.3 | 可理解 |

## 技术写作

| 规则 | 出处 | 原则 |
|---|---|---|
| 第二人称「你」,不用「我们」 | Google highlights | 可理解 |
| 主动语态,说清谁在做 | Google highlights | 可理解 |
| 条件放在指令前面 | Google highlights | 可使用 |
| 不预告(「后面会讲」「即将支持」) | Google highlights | 相关 |
| 链接文字描述目标,不写「点这里」 | Google highlights | 可找到 |
| 有顺序用编号列表,无顺序用项目列表;一对相关数据用描述列表;三个以上相关数据用表格 | Google highlights、tables | 可找到 |
| 只有一行或一列不用表格;表格前用完整句子说明用途;表头简短、不以标点结尾;不合并单元格 | Google tables | 可使用 |
| 概念性标题用名词短语;任务性标题用动词原形 | Google headings | 可找到 |
| 标题不用序号表示顺序、不放代码和链接、标点从简;不空标题;不跳级;下级标题不重复上级 | Google headings | 可找到 |
| 引用一组小节说「以下各节」,不说「本节」「这些节」 | Google headings | 可理解 |
| 标题末不加句号或冒号 | Microsoft top 10 | 可找到 |
| 句首大写(sentence case),不用 Title Case | Google、Microsoft | 可理解 |
| 序列逗号 | Google、Microsoft | 可理解 |
| 简短;去掉 *there is* 类弱写法;以动词开头 | Microsoft top 10 | 可理解 |
| 代码相关文字用代码字体;界面元素用粗体 | Google highlights | 可找到 |
| 日期格式无歧义 | Google highlights | 可使用 |

## 文档分类

Diátaxis 把文档分四类,两条轴:给做事还是给认知、服务学习还是服务工作。

| | 学习 | 工作 |
|---|---|---|
| 做事 | 教程 | 操作指南 |
| 认知 | 解释 | 参考 |

核心主张:四类不能混。教程里塞解释、参考里塞观点,是大量文档问题的根源。

| 规则 | 出处 | 原则 |
|---|---|---|
| 一篇文档只服务一类需求 | Diátaxis start-here | 相关 |
| 解释类:回答为什么,像讨论,承认观点、给多角度,标题隐含「关于」 | Diátaxis explanation | 相关 |
| 参考类:陈述事实,克制中立,结构镜像被描述对象,不掺观点和指导 | Diátaxis reference | 可使用 |

对本库的映射:`concepts/` 解释,`design/` 参考(定义段允许解释),`sources/` 参考。

## 本次犯的错对应哪条

| 错 | 规则 | 原则 |
|---|---|---|
| `形式`、`三类关系`作标题 | 标题用描述性名词短语 | 可找到 |
| `0. 一图看懂` | 标题不用序号、不用动词开头 | 可找到 |
| `**不覆盖**:`充当标题 | 不用格式标签冒充标题层级 | 可找到 |
| 「待写……」写在正文 | 不预告 | 相关 |
| 生造「不覆盖」「骨架」「档」 | 术语从标准取 | 可理解 |
| 「见 §4」 | 标题不用序号,引用用标题名 | 可找到 |
| 中文用半角逗号、引号用「」 | GB/T 15834 | 可理解 |
| `design/topics.md` 同时解释和规定 | 四类不混 | 相关 |
| 「一句话:」「说白了」 | 不用口语强调,直接陈述 | 可理解 |

九条里只有一条是用词。其余是结构、段落、类型混淆。

## 待办

- 读 ISO 24495-1 正文(收费),核四原则下的具体指南
- 据本文写概念文「写作规范」和 `design/writing.md`
