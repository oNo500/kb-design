# 词表版本

版本是对整份词表某一时刻状态的命名。概念级的 `history` 记单条变更，版本记整体发布。依据：ISO 25964-1 数据模型的 VersionHistory 类（identifier、date、versionNote、currentVersion），见 [ISO 25964 笔记](../sources/iso-25964.md)。

## 版本块

每份词表文件头部一个 `version` 块：

```yaml
version:
  id: "2026.08"                  # 年.月；同月第二版加序号 2026.08.2
  date: 2026-08-23
  note: 初版：八个顶层、computing 下 17 个知识领域、…
```

五份词表共用一个版本号，一起发版；CHANGELOG 按词表分列。版本号用日期，不用语义化三段：词表没有“破坏性变更”的概念——id 一经引用不变，`deprecated` 不删，任何版本的引用都能解析——所以主次版本号没有可表达的内容。ATLAS 的内容版本也用 YYYY.MM。

## 发版时机

发版是治理的一个动作，触发条件见[维护](maintenance.md)“触发与动作”。

## 内容单元与版本

内容单元不记录它引用的词表版本。原因：id 规则保证 id 不变，生命周期规则保证 `deprecated` 不删，所以旧引用永远可解析；版本只回答“这一版新增、废弃了什么”，不参与引用解析。

## 变更记录

`vocab/CHANGELOG.md`，每版一节，按五份词表分列：新增、废弃（含 `replaced_by`）、改名（`label` 变，id 不变）、来源更新。只追加，不改旧节——与[决定记录](decisions/)的原则一致。

## 待定事项

