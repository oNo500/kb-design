# Python 文件系统

## 材料身份

本笔记记录 Python `os.replace()`、Python `os.fsync()` 与 POSIX rename 的可见性和持久性边界，核对日期为 2026-09-01。它只解释当前目录替换策略能提供什么，不把原子替换扩大成持久性、事务或内容正确性保证。

## 阅读范围

| 材料 | 实际读到的位置 |
|---|---|
| [Python `os` 文档](https://docs.python.org/3/library/os.html) | `os.replace()` 与 `os.fsync()` 条目 |
| [POSIX.1-2024 `rename()`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/rename.html) | DESCRIPTION、ERRORS 中与替换、原子性和失败有关的条款 |
| [POSIX.1-2024 General Concepts](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html) | 文件系统操作的 atomicity 说明 |

## 替换行为

`os.replace(src, dst)` 将 `src` rename 为 `dst`。当 `dst` 是既有文件且调用者有权限时，它会被替换；当 `dst` 是非空目录时抛出 `OSError`；`src` 与 `dst` 跨文件系统时操作可能失败。Python 文档只在操作成功时承诺 rename 是 atomic operation，并说明这是 POSIX 要求。[Python `os.replace()`](https://docs.python.org/3/library/os.html#os.replace)

因此，`os.replace` 成功时是单目录项原子替换；非空目录、权限、平台和跨文件系统可能失败。原子性描述的是成功操作的目录项可见切换，不是无条件成功保证。

## 持久边界

`os.fsync(fd)` 强制把该 file descriptor 关联的数据写入磁盘；若从 Python buffered file object 开始，文档要求先 `flush()`，再对其 file descriptor 调用 `os.fsync()`。[Python `os.fsync()`](https://docs.python.org/3/library/os.html#os.fsync)

原子可见性不等于 `fsync` 持久性，不等于多文件事务，也不等于内容正确性。rename 的观察者不会看到目标目录项的中间替换状态，不能由此推出文件内容与包含目录已经满足掉电恢复要求，也不能推出一组文件具有全有或全无的事务语义。

## 项目边界

当前 Obsidian exporter 先在临时目录写完并校验全部输出，再以 `os.replace()` 将临时目录放到目标路径。当前需求只控制生成完成前不可见和失败不覆盖用户目标，不要求掉电持久性；因此当前实现不得描述为 durability protocol 或多文件事务。

该替换策略不证明生成内容正确、manifest 完整、provenance、JCS conformance 或 reproducible build；这些问题必须由各自独立的规则和检查回答。

## 未读范围

- 未核对各操作系统和文件系统对 rename、directory `fsync`、缓存、网络文件系统与掉电恢复的全部实现差异。
- 未设计或实现持久性协议、事务日志、回滚日志、锁、并发写入协调或故障注入测试。
