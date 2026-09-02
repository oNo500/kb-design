# Obsidian 应用 (Obsidian Application)

`kb-obsidian` 从固定版本的 `kb-design` 初始化一个新的 Obsidian vault，并提供内容建立、只读校验和派生报告命令。`kb-design` 仍是概念、正式词表、内容模型和治理规则的唯一权威；实际知识内容保存在用户 vault，不进入本仓库。

## 安装

本项目需要 Python 3.9+ 和 Git。在仓库根目录安装可编辑版本：

```bash
python3 -m pip install -e .
kb-obsidian --help
```

## 设计来源

所有命令都要求通过 `--design-root` 传入 `kb-design` 仓库根目录。当前唯一支持的设计提交是：

```text
356f02bc0a61d28c045139b2dc5f41bf40291a78
```

该目录必须是这个提交的干净 Git checkout；tracked 文件有修改、HEAD 不匹配或传入的不是仓库根目录时，命令会失败。运行时路径由参数传入，应用不把本机目录写入生成内容。

## 新库初始化

目标目录必须不存在或为空。初始化不会更新非空 vault，也不会合并或覆盖其中的用户文件。

```bash
kb-obsidian init \
  --design-root /path/to/kb-design \
  --output /path/to/new-vault
```

命令创建 `Home.md`、用户内容目录、`KB/` 正式参考表示、`App/` 受管理文件和最低限度的 `.obsidian/` 配置。受管理 manifest 不把用户内容、报告或 Obsidian 配置声明为受管理知识文件。

## 内容建立

以下命令创建一条 `draft` 内容。`--subject` 至少出现一次；`--subject`、`--entity` 和 `--reference` 都可以重复。`--form`、`--level` 和 `--language` 是可选参数，语言默认是 `zh`。

```bash
kb-obsidian new-content \
  --design-root /path/to/kb-design \
  --vault /path/to/new-vault \
  --title '内容标题' \
  --type explanation \
  --genre analysis \
  --subject artificial-intelligence \
  --subject security \
  --entity openai \
  --reference gbt-13745 \
  --form narrative-text \
  --level understand \
  --language en
```

内容保存为 `Content/<UUIDv4>.md`。成功 JSON 的 `path` 是新文件的绝对路径。文件名承担稳定身份；一级标题、`title` property 和唯一派生 alias 使用同一标题。Quick Switcher 可通过 alias 按标题打开 UUID 文件，Search 和 Bases 用于按 properties 查询，用户不需要记忆 UUID。

## 内容校验

校验只读取 `Content/*.md`，不改写或修复内容：

```bash
kb-obsidian validate \
  --design-root /path/to/kb-design \
  --vault /path/to/new-vault
```

没有 issue 时，命令向 stdout 写一行排序紧凑 JSON 并返回 0。有 issue 时，stdout 为空，stderr 写一行 `KB_OBSIDIAN_ERROR: <排序紧凑 JSON 摘要>` 并返回 1；摘要包含每个 issue 的 `path`、`field`、`code` 和 `message`。

## 使用报告

报告命令先执行同一内容校验，再用有效内容刷新派生报告：

```bash
kb-obsidian report \
  --design-root /path/to/kb-design \
  --vault /path/to/new-vault
```

报告只写 `App/Reports/`。无效内容不进入正式计数；命令不会修改 `Content/`、`KB/`、模板、视图、规则、设计来源或正式数据，也不会根据报告自动返回、修复或切换任何内容。

## 命令输出

四个命令成功时都只向 stdout 写一个排序、紧凑的单行 JSON object，并以 LF 结束。预期的参数、设计源、文件系统或解析错误只向 stderr 写一行以 `KB_OBSIDIAN_ERROR: ` 开头的消息，并返回 1；`--help` 返回 0。

## 应用边界

本应用不实现非空 vault 更新、内容回流、自动修复、查询日志、社区插件或 Obsidian GUI 自动化。Quick Switcher 的交互、Bases 的实际显示和视觉布局需要在 Obsidian 中人工验收；解析 YAML、JSON 或 Base 文件只证明生成文件合同，不替代 GUI 验收。
