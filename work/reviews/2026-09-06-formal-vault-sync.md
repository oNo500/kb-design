# 正式库同步

## 授权范围

用户在基础设施验收后明确批准正式库同步：恢复已核实的一张参考页表格格式，刷新参考资料并检查内容及链接。目标为 `/Users/xiu/Documents/kb-vault/`，不包含合并 master、发版、批量内容修改或新消费者授权。

## 同步结果

Obsidian CLI 确认目标路径。同步前仅 `kb/topics/software-verification-and-validation.md` 与原 manifest 不一致，其哈希与上次预检相同；恢复到已核实的原字节后，正式 dry-run 通过。

正常刷新从 cf80d1d34c4aeef6e590f4f6d81c00643acc3eb3 升至干净设计快照 f19dc38c311647ba87615ca7ce52121ed54d321b。新增 208 页、更新 844 页、删除零页，路径逐项等于[已批准写集](2026-09-06-formal-vault-write-set.json)，另更新 app/manifest.json。

刷新入口的正文引用检查通过。随后内容校验为 21 条有效、零问题；136 个非参考保护文件在恢复格式前与刷新后逐字节相同。所有受管理文件哈希均符合新 manifest。未改内容、配置或 notes vault。

现有刷新工具生成备份 `/Users/xiu/Documents/.kb-vault.refresh-backup-k_xy6rik`，本次保留。原格式差异及命令原始输出保存在本 worktree 的忽略目录 build/term-complete-acceptance/formal-sync-*；本记录和路径写集提供持久验收结论。

## 完成边界

正式库参考同步已完成，包含获准术语参考页。现有内容的有效性与链接可用性已经验证，但不据此宣称内容价值、组织效果或实际使用验收完成，不开启委托、周期义务、查询日志、回流或 TBX。master 未合并。
