# 工程约定收录

## 授权范围

用户确认收录工程约定及相关实体，继续使用现有 vendor 关系；terms 以业界惯例为准，无依据时不新增。本次只建立一篇工程约定笔记，核心实体关联为 uv、Bun、npm、fnm、Node.js。检索和编辑工具作为正文命令保留，不因提及而逐一建实体。

## 内容价值

笔记回答日常开发中如何选择工具、何时例外，以及如何避免混用安装器、遗漏搜索范围和误改源码。新增价值是汇总用户已选定的默认行为及例外条件。类型采用 reference，体裁采用 advice，主题采用现有 tools-and-environments；不把个人约定称为行业标准，也不新增“工程约定”主题或术语。

正文保留依赖与运行、检索范围、修改方式和参考资料四节。对原文的调整是区分包管理器与运行时、明确单一包管理器按同一套依赖理解，以及补充 Bun 默认信任名单与显式名单的关系。没有删除原文的工具选择和修改限制。

## 实体依据

新增软件实体 bun、npm、fnm、nodejs，状态为 candidate。名称保持官方产品写法，不新增译名。npm 的范围限定为命令行客户端，不与 registry 或同名公司混同。

uv 保留 vendor: astral，补入官方依据；去除 scope 中未经本次证实的“Wikidata 无条目”绝对断言，旧值保留在历史。Bun 使用 vendor: anthropic；当前 [Bun 官方公告](https://bun.com/blog/bun-joins-anthropic)明确被 Anthropic 收购，[Wikidata](https://www.wikidata.org/wiki/Q113048518)的 owned by 指向 Anthropic。其余新软件未填 vendor；不为了填满字段而新增人员或推定组织归属。

新增 uv-docs、npm-docs、fnm-docs 三条资料实体，承接当前 basis 只能引用 standard／publication 实体的合同。沿用既有厂商文档 kind: standard、tier: vendor 的项目做法，这不宣称它们是标准组织颁布的技术标准。记录保持 candidate、version: null；没有登记来源用途，没有批准定期复核或观察任务。

新增记录的 subjects 使用 tools-and-environments；标引依据由 CS2023 SE-Tools 的主题范围与产品文档／Wikidata 的具体功能共同支撑。这是本次对应判断，不表示 CS2023 点名推荐这些产品。uv 的旧归属判断保持原样。

## 外部映射

- Bun：Q113115405 实际跳转到 Q113048518，采用后者；标签、运行时与包管理器类别、官网指向同一产品。
- Node.js：Q756100，标签、描述、软件类别和官网相符。
- npm：检索命中 Q7067518，但原页与实体 JSON 读取失败，暂不采纳映射。
- fnm：本次 Wikidata 检索未取得可核对应，不据此断言没有条目。

## 核对材料

- [uv 官方文档](https://docs.astral.sh/uv/)：名称、范围、命令及 Astral 关系。
- [npm 官方文档](https://docs.npmjs.com/)与 [npm 命令说明](https://docs.npmjs.com/cli/v11/commands/npm/)：文档身份、客户端名称及用途。
- [fnm 项目文档](https://github.com/Schniz/fnm#readme)：名称、用途、版本文件和 shell 配置。
- [Bun](https://bun.com/)与 [Node.js](https://nodejs.org/en/about)：软件功能。
- [CS2023](https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm)：SE-Tools 的主题范围。

其余命令依据位于笔记文末。外部资料只读核对，不持久下载。

## 收录校验

`uv run kb-core check-sources --root .` 返回零项问题。结构化比较确认除 uv 外的旧实体完整不变，uv 原有历史保持前缀完整；本次只增加关系与范围依据、修正范围中的未核断言并追加历史。topics、terms 和来源用途不在写集内。

CS2023 的网页超过浏览工具大小限制，改用内存读取原网页的 SE-Tools 段落核对；其中明确包含配置复现、依赖管理和工具集成。没有把读取失败记成成功，也没有保存网页副本。
