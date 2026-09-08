# 词表预览

本应用为词表维护者展示仓库工作区数据。按 [Application Profile](../../concepts/application-profile.md)的方法分开数据模型、页面表示与应用行为，方法登记见[项目方法](../governance/principles.md)。现行字段语义以模型设计为准，页面不另建词表或概念身份。

## 数据来源

输入为 `data/vocab/` 中的六份词表及 `data/references/bibliography.yaml`，包含未提交的编辑。书目与普通实体分别显示、搜索和解析；书目不计作新增受控词表，职责见[参考文献目录](../model/bibliography.md)。页面显示读取时间、来源文件哈希及条目的原始 YAML；这些信息描述当前工作区，不证明人工审核、正式来源或术语切换。

同一读取批次的文件字节会复核是否变化。它用于避免读取过程中出现不一致，不把用户连续编辑多份文件解释成一个原子事务。

## 页面表示

六份词表与书目均要求 schema_version 为 3，实体、书目和来源用途另要求对应 schema。三份文档使用核心 schema 检查闭合字段，派生、映射、外部分组与项目判断按各自结构检查；错误保留上次有效快照。页面检查表示结构，不替代外部事实、用途决定作用范围或正式准入检查。普通实体直接 URL 依据只用于[限定事实字段](../model/entities.md#事实依据)，不作为 subjects、术语或映射的后备。旧 entity 依据和跨目录引用报错，不尝试双格式读取。

| 字段 | 页面表示与引用 | 信息保存 |
|---|---|---|
| 名称、ID、项目 status | 列表、详情、项目状态筛选 | 保留身份与原文字，不翻译 |
| source_status | 详情“外部状态” | 与项目状态分开；来源缺值显示“外部状态未核实”，不推导 current，一般实体不加此提示 |
| 来源 version | 详情与来源卡片 | null 显示“未登记可核实版本”，不表示无版本 |
| urls、review、watch、history | 逐字段展开的详情 | 保存全部地址、主地址标记、复核日期及义务 ID、观察信号和周期、历史前后值；无来源文件写回 |
| roles | 逐项展示角色、状态和决定 | proposed、approved、retired 不混同；来源卡片也显示状态与真实决定 ID |
| 外部 basis | 字段、适用主题、文献与定位 | subjects 保留 values／references 分组；reference 依据边指向书目，不假造来源用途；直接 URL 只展示官方链接、定位与真实 checked，不生成文献身份或权限 |
| 用途 reference | 书目身份链接 | 与普通实体及用途登记自身身份分开 |
| assertions | 独立“项目判断”详情 | 保存 original、disposition、migration 和适用值，不生成外部依据边 |
| source、match、external_group | 独立完整详情与来源用途链接 | 保存 registry、item、locator 或 rel 及相邻依据；外部分组使用 structure 含义，不表示成员逐序完整复制 |
| 载体数组 local_analysis | 独立“隔离记录”详情 | 保留旧显示字符串、isolated 状态及决定 ID，不形成来源图边、用途或有效本地分析 |
| 语言 basis | 独立名称依据详情 | 保留等级、来源、模型判断与“外部用法未核实”；不把模型或 legacy 标记生成外部依据边 |

主题层级允许多上位条目出现在多个分支；分组与上下位关系分别展示。关系图只画能够解析到现有对象的关系，不以图中缺边证明原数据没有引用。按[来源收尾](../../decisions/source-completion.md)隔离的 17 条旧 match 不在当前 YAML、映射详情和图边中，因而页面不提供这些历史关系的浏览与跳转；原值与结论须查决定隔离清单及 Git 历史。现有对象、标签、项目状态及其他关系仍显示。24 个数组的成员和顺序表示项目选择，SPD-SEP 缺项及顺序差异没有被外部分组依据消除。所有记录另有原始 YAML、输入哈希及读取时间；这些信息不是采纳凭证。

## 实时行为

本地服务约每秒接受一次页面状态查询，文件内容改变后重载页面。搜索、筛选、展开状态的精细保留后置。错误时保留上一次有效表示并显示错误，恢复后继续更新；所有请求均为只读，不提供词表写入接口。

本应用与 Obsidian 的已提交快照导出用途不同，不能相互替代。它没有持久导出产物或正式切换行为，不增加 [Reproducible Builds](../../concepts/reproducible-builds.md)符合性声明。应用归属与范围见[预览归属](../../decisions/vocab-preview-location.md)，启动与维护见[应用说明](../../../apps/vocab-preview/README.md)。
