# 批量翻译

英文基准决定节点、英文名称和关系。脚本提取缺少中文的首选名，agent 只生成译文；脚本按原任务 ID 写回同一个 URI，输出独立双语文件。当前只翻译首选名，不处理别名、定义或权威术语核验。

## 同步规则

[中文标签设计](../../../docs/model/vocabulary/设计-中文标签.md#增量同步)规定：以 vocabulary.ttl 为基准，移除当前已不存在的对象，只翻译增量，按稳定 URI 复用已有译文。英文名称或结构变化不自动重译；旧译文继续保留原批次元数据，历史文件不删除。

跨版本的译文复用、删除清理及统一切换尚未完整实现。下面的提取命令只跳过基准中已有中文的对象，不会自动读取以前的翻译结果，不能当作增量同步命令。

## 提取命令

```bash
uv run --package kb-vocab python packages/kb-vocab/scripts/extract-translation-tasks.py \
  output/vocabulary/current/vocabulary.ttl --output NEW_RUN \
  --batch-size 200 --model gpt-5.6-luna
```

`tasks.json` 固定基准版本与哈希、原节点 URI 和英文文字；小批输入仅包含 ID、英文及最多两个上位名提示。已有中文不覆盖。分派器将实际 agent ID 填入 `orchestration.json` 的 owners，模型值必须与实际指定模型一致。

## 翻译输出

每个 `.input.json` 对应一个 `.output.json`，使用 `{"任务ID":"中文"}`；也兼容 `[{"id":"任务ID","zh":"中文"}]`。纯缩写、宜保留的专名或无法确定的项可为 null，不把英文占位当中文。只能用模型直接翻译，不使用词块替换。

## 合并命令

```bash
uv run --package kb-vocab python packages/kb-vocab/scripts/merge-translation-run.py --run RUN
uv run --package kb-vocab python packages/kb-vocab/scripts/merge-translation-run.py --run RUN --output NEW_RESULT
```

合并校验 ID、英文原文、基准哈希与中文标签写集，保留全部原始三元组。输出 translations.zh.ttl、vocabulary.multilingual.ttl、label-provenance.json、report.json 与文件哈希清单。纠正批次放在 corrections，仍只按原 ID 覆盖译文，并独立记录实际译者批次。

依据按批次保存 AI、模型、agent、输出文件时间、输入输出哈希；每条中文只关联批次。它是展示用 AI 初译，不是已核实的权威术语，也不经过旧的逐项 label-adoptions 工作流。

## 展示命令

```bash
uv run --package kb-vocab python apps/skosmos/sync-translated.py RESULT
```

[AI 中文词表](http://localhost:9090/translated/zh/?clang=zh)与英文基准浏览入口使用独立图，不覆盖原始 vocabulary.ttl。页面在名称附近展示批次模型与时间提示。
