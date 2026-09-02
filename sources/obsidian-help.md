# Obsidian 官方帮助

## 材料身份

本文只记录 [Obsidian Help](https://obsidian.md/help/) 的产品帮助页面。下表材料均在 2026-09-02 核对；英文产品名称和页面小节名只转录来源，不登记为项目术语。它们可以说明 Obsidian 的产品行为和限制，不能决定本项目的数据效力、字段约束、稳定身份或治理结论。

## 阅读范围

下表逐项记录本次实际阅读的页面、小节、行为、限制和对未来应用设计的相关性。“相关性”只说明该能力可为哪一类界面或表示提供事实依据，不赋予任何文件项目效力。

| 能力 | 来源与实际阅读小节 | 行为 | 限制 | 项目相关性 |
|---|---|---|---|---|
| vault 存储 | [How Obsidian stores data](https://obsidian.md/help/Files%2Band%2Bfolders/How%2BObsidian%2Bstores%2Bdata)：全文，含 local files、configuration files、metadata cache 和 IndexedDB | vault 是本地文件系统中的文件夹，笔记是 Markdown 纯文本；Obsidian 将变化与本地 metadata cache 同步，外部编辑器和文件管理器可以编辑文件。 | 官方建议不要嵌套 vault，因为内部链接属于单一 vault，可能无法正确更新；这是建议，不是禁止。 | 说明本地文件、应用配置和缓存的产品边界；文件可被外部修改不等于项目会读取、接受或赋予该修改效力。 |
| Properties | [Properties](https://obsidian.md/help/properties)：Add properties to a note、Property types、Advanced uses、Not supported、Property format、Text、List、Checkbox、JSON properties 和 Default properties | properties 位于文件开头的 YAML；支持 Text、List、Number、Checkbox、Date、Date & time 和 Tags。同一 property name 在一个 vault 中使用同一 type；Text 和 List 可保存加引号的内部链接。 | 不支持 nested properties 的应用内查看与编辑，但 YAML 本身仍可保存嵌套结构；不支持原生 bulk-editing；properties 不渲染 Markdown。JSON frontmatter 会在保存时转为 YAML。 | 说明 Markdown property 的可编辑表示、类型一致性和受限编辑范围。Checkbox 的 YAML 值是 `true` 或 `false`，不是另一种 property type。 |
| Aliases | [Aliases](https://obsidian.md/help/aliases)：Add an alias to a note、Link to a note using an alias | alias 是笔记的替代名称；`aliases` 使用 YAML list。以 alias 选取链接时，链接仍以真实文件为目标。 | alias 只处理同一笔记的替代名称；一次链接的显示文本应使用内部链接的显示文本能力。 | 说明替代名称与目标文件可以分开，不能据此证明正式同义、关系或身份判断。 |
| 内部链接 | [Internal links](https://obsidian.md/help/Linking%2Bnotes%2Band%2Bfiles/Internal%2Blinks)：Supported formats for internal links、Link to a file、Link to a heading in a note | 支持 Wikilink 和 Markdown link；路径从 vault 根开始并使用 `/`。未存在的笔记目标可在该路径创建；Wikilink 可指定显示文本，重命名时可自动更新内部链接。 | Markdown link 的目标需要 URL encoding；有些字符不适合作为链接；非 Markdown 的已支持格式须带扩展名。 | 说明文件、路径、显示文本和链接目标的产品行为；普通链接本身不能证明正式关系。 |
| 支持格式 | [Accepted file formats](https://obsidian.md/help/Files%2Band%2Bfolders/Accepted%2Bfile%2Bformats)：Supported file types、Embed files | 官方列出 Markdown `.md`、Bases `.base`、JSON Canvas `.canvas`、图像、音频、视频和 PDF；可嵌入多种媒体与 PDF。 | 其他格式要靠 community plugins；音视频等支持取决于设备 codec。普通 `.json` 不在内容格式清单中。 | 区分可被 Obsidian 作为内容处理的格式与同目录的项目文件；property 的 JSON frontmatter 规则不使普通 `.json` 成为内容格式，项目 manifest 也只是同目录项目清单。 |
| Bases | [Introduction to Bases](https://obsidian.md/help/bases)：Introduction、How to use bases、View types；[Bases syntax](https://obsidian.md/help/bases/syntax)：Introduction、Filters、Properties、Views 和 Note properties；[Table view](https://obsidian.md/help/bases/views/table)：Introduction、Summaries 和 Shortcuts | Bases 是 core plugin，可基于本地 Markdown 与 properties 建立多种 view，并可查看、编辑、排序和筛选文件及其 properties；`.base` 保存 view、filter 和 formula 配置。默认数据集包含 vault 内全部文件，filters 可收窄范围；表格支持粘贴、撤销、重做、清除单元格和切换 checkbox。 | Base 的 note properties 只适用于 Markdown 文件；`file.backlinks` 与 `file.properties` 不会在 vault 变化时自动刷新。Base 的可编辑性不使它成为技术上的只读表格。 | 说明未来浏览、筛选和诊断界面可以读取及编辑本地表示；这种编辑不证明其数据有效或已回流。 |
| Search | [Search](https://obsidian.md/help/Plugins/Search)：Search terms、Search operators、Search properties、Change result sort order、Copy search results、Use regular expressions、Configure search settings 和 Embed search results in a note | Search 可搜索笔记和 Canvas 的正文，并以 `file:`、`path:`、`content:` 等操作符搜索文件名、路径或内容；方括号语法可搜索 properties。 | excluded files 不出现在结果中；默认不搜索任意附件的路径或文件名。所读官方页面只说明查询、结果和复制操作，未给出可供本项目留存和复核的 search-event interface。 | 说明内容、路径和 property 的交互查询能力；查询结果或嵌入结果不能充当可审计的项目搜索记录。 |
| Backlinks | [Backlinks](https://obsidian.md/help/Plugins/Backlinks)：Introduction、Show backlinks、View backlinks for a note 和 Show backlinks in a note | Backlinks 显示指向活动笔记的 linked mentions，以及按笔记名称匹配的 unlinked mentions；可筛选、排序并显示上下文。 | excluded files 不出现在 unlinked mentions；unlinked mention 只是未链接的名称出现。 | 说明进入相关笔记和探索提及的能力，不能把反向链接或名称共现视为正式关系证明。 |
| Graph | [Graph view](https://obsidian.md/help/Plugins/Graph%2Bview)：Introduction、Settings、Filters、Groups、Display、Forces 和 Local Graph | Graph 以节点显示笔记、以边显示内部链接；可按搜索条件、tag、附件、孤立节点等过滤，也可查看活动笔记的局部图。 | 图中的边来自内部链接，显示布局可由设置改变；excluded files 不出现。 | 说明链接网络的探索和导航能力，不能由邻近、节点大小或图形边直接证明正式关系。 |
| Bookmarks | [Bookmarks](https://obsidian.md/help/Plugins/Bookmarks)：Introduction、Add a bookmark、Add a bookmark group、Remove a bookmark group 和 Bookmark multiple files | Bookmarks 是常用项目的快捷入口，可收藏文件、文件夹、搜索、图、标题、块和链接，并用 bookmark groups 组织和排序。 | local graph 不能被收藏；bookmark group 可连同其中 bookmarks 一起删除。 | 说明个人导航入口与组织能力，不能把收藏或分组视为正式关系、分类或证明。 |
| Templates | [Templates](https://obsidian.md/help/Plugins/Templates)：Set your template folder、Template variables、Create a template、Insert a template into the active note、Template properties 和 Insert current date and time into the active note | Templates 是插入活动笔记的预定义文本片段；`{{title}}`、`{{date}}` 和 `{{time}}` 可替换为标题、日期和时间，模板中的 properties 会与笔记 properties 合并。 | 插入位置是当前或上次光标位置；Live Preview 中未加引号的 template variables 可能被 properties 面板覆盖。官方功能是插入与替换，不验证受控值。 | 说明可辅助创建片段、标题与日期，不承担字段校验或正式内容建立。 |
| Unique note creator | [Unique note creator](https://obsidian.md/help/Plugins/Unique%2Bnote%2Bcreator)：Introduction、Create a unique note 和 Create unique notes from a template | 这个 core plugin 按时间创建笔记名称；若同名时间戳已存在，则使用下一个可用时间戳，也可使用模板。 | 名称来自创建时间，文档没有把它定义为任何外部或项目身份。 | 说明时间命名的创建便利，不能建立项目内容 identifier。 |
| Web Clipper | [Introduction to Obsidian Web Clipper](https://obsidian.md/help/web-clipper)：Introduction、How to use Web Clipper 和 Privacy；[Clip web pages](https://obsidian.md/help/web-clipper/capture)：Capture a page、Download images、Interface functionality | Web Clipper 是浏览器扩展，可高亮页面并把网页内容保存到本地 vault；可从正文、选区或 highlights 提取内容，界面可选择 vault 和 folder，并显示待保存 properties 与正文。 | 默认只尝试提取主要文章内容；图片默认只保留网页 URL，不会下载，离线或 URL 失效时不可访问。 | 说明外部网页材料可进入本地文件；保存动作不能取得项目效力。 |
| Clipper 模板 | [Templates](https://obsidian.md/help/web-clipper/templates)：Create or edit a template、Import and export Web Clipper templates、Template settings、Behavior、Automatically trigger a template 和 Interpreter context | 模板可按 URL 或 schema.org 选择，并用 variables、filters 组织网页 metadata；behavior 可创建新笔记，或在已有笔记、daily note 的开头或末尾追加内容。 | daily note 行为要求启用相应插件；匹配按模板列表的第一个匹配项，未匹配时使用列表首项。 | 说明网页保存的目标和追加方式；创建或追加文件不取得项目效力。 |
| Clipper 变量 | [Variables](https://obsidian.md/help/web-clipper/variables)：Introduction、Preset variables、Prompt variables、When to use prompt variables、Meta variables、Selector variables 和 Schema.org variables；[Interpreter](https://obsidian.md/help/web-clipper/interpreter)：Examples of prompts、Get started、How it works、Context、Models 和 Local models | preset variables 根据页面自动取得作者、内容、日期、标题、URL 等，可放在 note name、location、properties 和 content。prompt variables 由 Interpreter 使用自然语言提取或变换页面数据。 | `{{content}}` 只尝试取得主要内容，未必符合需要。prompt variables 需要 Obsidian 外的语言模型处理；不同 provider 会带来速度、成本和隐私差异，第三方 provider 会直接收到请求，局部或本地模型也有自己的配置、资源与上下文限制。 | 说明网页元数据、正文和预设变量可辅助捕获；语言模型输出和网页提取都不能自动成为项目数据或判断。 |

## 能力边界

上述页面共同说明 Obsidian 能存放和编辑本地 Markdown、properties、内部链接与 Base，也能以模板、时间命名或网页剪藏创建或追加文件。它们不提供本项目的受控值校验、内容 identifier、正式关系证明、可审计搜索事件或项目效力判断。

Backlinks、Graph 和 Bookmarks 分别提供入链查看、链接网络可视化和快捷入口。它们是导航或探索能力；内部链接、名称共现、图形邻近、节点大小、收藏和分组都不能单独证明正式关系。

## 适用边界

官方帮助只支持本页列出的产品行为、格式和限制。它不能决定本项目的稳定 ID、正式数据效力、designation 准入、字段基数、导出失败政策、回流、确定性或安全替换；这些问题仍须由项目的概念、治理与应用设计材料回答。

## 未读范围

- 未读取版本历史、release notes、API、开发者文档、community plugins 页面或外部规范；未把作者博客、公共 vault 或社区模板当作产品行为依据。
- 未在 Obsidian 应用中建立 vault、创建 property、编辑 Base、执行 Search、运行模板或 Web Clipper；本文只记录上述官方帮助页面直接陈述的能力与限制。
