# 主题生成器 (KB Topics)

从 `data/inputs/topics/` 和现行采纳记录生成主题词表。包依赖 `kb-core` 的公共校验能力，生成流程与边界见[主题生成包](../../docs/development/设计-主题生成包.md)。

## 使用方法

在仓库根目录执行：

```bash
uv sync --all-packages --locked
uv run kb-topics --help
uv run kb-topics --output build/topics-review.yaml
```

候选输出路径必须尚不存在。省略 `--output` 会重建正式 `data/vocab/topics.yaml`，运行前应完成输入审阅。生成后按改动范围执行 `uv run kb-core check-topics`。

`--references` 指定来源采纳输入，`KB_DESIGN_ROOT` 显式选择数据仓库。安装 wheel 后须设置该环境变量；仓库内默认沿用核心包的仓库定位。旧命令 `uv run kb-core build-topics` 仍可转交本包。

## 开发验证

```bash
uv run python -m unittest discover -s packages/kb-topics/tests
```

测试检查生成语义保持、授权缺失、输出路径和参数错误的写入边界。当前包拆分不改变关系表示、概念状态或来源规则。
