# 标准关系审查

状态：待采纳。检查范围为 SWEBOK 的 18 条 match、16 条 source、1 个数组；RFC 1122 的四层 match/source 和 1 个数组；LOM 的 15 条载体 match。LOM 两个已按 Q16 隔离的数组不重审。[逐项记录](2026-09-06-standard-relations.json)保留 identity、完整旧值、实际证据位置、日期及明确缺口，未改变任何关系。

## 分层依据

[RFC 1122 原文](https://www.rfc-editor.org/rfc/rfc1122.html)§1.1.3 分别说明四层：应用层与传输层在印刷页 9，网际层与链路层在页 10。本库四条 scope 与各自段落对应；四条 match、四条 source 及数组组引用均给出待采纳建议。每条 locator 均含具体层名，不用一个总段落替代四份判断。

旧 item 均为 1.1.3，本报告不发明新外部编号，依各自 locator/basis 区分。四个概念不是彼此等同；原文分层可支持此批关系，也不表示全部协议条款仍为现行要求。

## 版本补核

首次未取得 4.0 的观察保存在 JSON 的 review_history。随后各限 3 个版本端点查找：[UWS 贡献者书目](https://research-portal.uws.ac.uk/en/publications/guide-to-the-software-engineering-body-of-knowledge-v40/)确认出版身份，其官方链接失败；[Studylib 镜像](https://studylib.net/doc/27764293/swebok-v4)可读 4.0 的第二手转录，但止于 17-4 页，不能称取得全书。没有借用 4.0a。

已按各章实际可读位置更新建议：17 条 match、16 条 source 和 1 个外部组。source 只支持目录概念的生成派生，组引用只支持 Table I.1；两者不批准 scope 全部内容。第 3、4 章与已读 CS2023 概念指向同类设计和构造对象，现给出来源语境下的对应推断；多来源与缺少 scope 本身不作为阻断。第 7 章 match 继续暂缓，因为 scope 只写交付后；第 18 章则按下述目录门槛补核形成建议，正文仍未取得。具体位置与 before/after 均在 JSON，未修改原关系。

## 草案限度

已读[原登记 LICEF 镜像](https://github.com/LICEF/lompad/blob/master/documentation/LOM_1484_12_1_v1_Final_Draft.pdf)的 165 KB PDF。封面明确其为 2002-07-15 批准草案，最终出版仍可能编辑；这是第二手托管材料，不能自动视为正式 2002 出版文本。

5.2 的值表包含本库对应的 15 个英文取值，但逐值词义指向 OED:1989 与教育实践社群，没有给出各值的完整定义。因而全部 15 条 match 暂缓，保留“值存在已核、scope 等同未核”的区别。尤其 figure 排除示意图、exam 必须评分、problem statement 不给解法等本库限定，不能由取值列表直接推出；simulation 和 narrative text 的邻近示例也不等于排他定义。

本次未将选用版升级为 2020，未以 Q16 两组分类充当词义依据。原始小文件保存在 build/source-verification/，JSON 记录 URL、散列与实际核对日期 2026-09-06；没有回填成 2026-09-05 的观察。

## 原件查找

LOM 的新增有限查找已封闭：[IEEE 出版页](https://standards.ieee.org/standard/1484_12_1-2002.html)确认 2002-09-06 出版，只提供购买/订阅入口；Xplore 的 1032843 元数据与 stamp 两端点未提供可读正文。没有再次使用 LICEF 草案代替正式出版文本。三次新增观察单独保存，15 条原有缺口保持。

## 维护范围

第 7 章的完整替换提案如下；before/after 和段落依据见 JSON 的 scope_proposals。尚未采纳或改动数据。

SWEBOK v4 第 7 章。软件维护：为运行中的软件提供经济有效的支持所需的全部活动，包括交付前的维护规划、可维护性与交接准备，以及交付后的软件监测、修改、培训和帮助台支持。

## 目录复核

仅复核既有镜像目录 xxiii 的第 18 章条目：工程过程、设计、抽象与实验方法，以及统计分析、度量、根因分析覆盖当前 scope 概述。结合 scope 明确限定 SWEBOK v4 第 18 章，现提出源限定的 exactMatch 对应推断；basis 明写目录，不冒充章正文。原正文缺失观察保留在 review_history，scope、id、label 和 rel 均未改变。
