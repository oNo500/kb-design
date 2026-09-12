# 项目约定入口

状态：已采纳，2026-08-29。决定记录只追加不修改；推翻时新建一条并把本条标为“被替代”。

## 背景

根目录的项目约定是[写作规则](../writing.md)和[治理](../governance.md)的摘要，内容适用于处理本库的 AI，不依赖 Claude Code。旧文件名 `CLAUDE.md` 把通用约定绑定到一个产品，也不能作为 Codex 默认发现的项目约定入口。

OpenAI 的 [AGENTS.md 官方说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md)明确说明，Codex 在开始工作前读取 `AGENTS.md`，并从项目根目录向当前目录逐层发现项目约定。当前阶段使用 Codex，不要求 Claude Code 自动加载本库约定。保留两份相同正文会增加摘要不同步的风险。

## 决定

根目录以 `AGENTS.md` 作为项目约定的唯一摘要入口，`design/writing.md` 仍是完整写作规则；两处冲突以 `design/writing.md` 为准。删除 `CLAUDE.md`，不保留副本或兼容文件。现行文档统一引用 `AGENTS.md`；旧决定记录中的 `CLAUDE.md` 作为历史事实保留。

如果以后需要其他 AI 自动加载本库约定，另行提案入口兼容方式，不复制 `AGENTS.md` 正文。

## 后果

- Codex 能按官方约定发现根目录的项目约定
- 项目约定不再以单一产品命名
- Claude Code 当前不保证自动加载项目约定
- 摘要仍只有一份，写作规则或治理规则变化时同步 `AGENTS.md` 和 README
