# 同学 C Extractor 模块交接说明

## 1. 我负责的范围

我负责的是 Benchmark Extractor 模块，也就是把 B 同学生成的原始调研报告整理成 D 同学可直接使用的结构化 `benchmarks.json`。

对应文件：

- `src/extractor.py`
- `src/schemas.py`
- `prompts/extractor.md`
- `data/cache/ai_agent_evaluation/benchmarks.json`

我没有负责：

- `src/planner.py`
- `src/searcher.py`
- `src/scorer.py`
- `src/judge.py`
- `src/reporter.py`
- `src/pipeline.py` 的整体编排逻辑

## 2. 模块在整体 pipeline 中的位置

整体流程是：

User Input
→ Planner
→ Searcher
→ Extractor
→ Scorer
→ Judge
→ Reporter

Extractor 的作用是承上启下：

- 输入 B 模块生成的 `raw_report.md`
- 输出 C 模块生成的 `benchmarks.json`
- 这个输出会被 D 模块直接读取并计算 `task_fit_score`、`rank` 和推荐理由

## 3. 对外接口

Extractor 的核心接口不要改签名：

```python
def extract_benchmarks(raw_report: str, topic: str) -> list[Benchmark]:
    ...
```

调用关系在 `src/pipeline.py` 中是：

```python
benchmarks = extractor.extract_benchmarks(raw_report, topic)
```

## 4. 输入是什么

Extractor 的输入不是 `planner_result.json`，也不是用户直接给的 JSON。

它的输入是：

- `raw_report.md`
- 类型是 Markdown 字符串
- 来源是 Searcher 的输出

这个原始报告里通常包含：

- Benchmark 名称
- 简要介绍
- 任务类型
- 能力点
- 指标
- 论文链接
- 代码链接
- 数据集链接
- 榜单链接
- 证据链接

## 5. 输出是什么

Extractor 最终输出的是 `list[Benchmark]`，保存到缓存后就是 `benchmarks.json`。

每个 Benchmark 至少包含这些字段：

- `name`
- `evaluated_ability`
- `resource_completeness`
- `reproduction_difficulty`
- `teaching_value`
- `research_value`
- `topic_popularity`
- `time_cost_friendliness`
- `documentation_quality`
- `authority`
- `evidence`

此外还支持这些字段：

- `description`
- `task_type`
- `metrics`
- `paper_url`
- `code_url`
- `dataset_url`
- `leaderboard_url`
- `open_source`
- `limitations`
- `suitable_usage`

## 6. `benchmarks.json` 字段约定

当前实现严格按《benchmarks.json 字段约定》输出，重点规则如下：

- `evaluated_ability` 必须是 `list[str]`
- 8 个评分字段必须是 `1-5` 的整数
- `evidence` 必须是 `list[str]`
- `evidence` 尽量至少保留 1 个真实来源链接
- `paper_url`、`code_url`、`dataset_url`、`leaderboard_url` 可以是字符串或 `null`
- 实在无法确认时再填 `null`，不要编造

## 7. extractor.py 做了什么

`src/extractor.py` 目前有两条路径：

### 7.1 LLM 抽取路径

- 读取 `prompts/extractor.md`
- 把 `topic` 和 `raw_report` 填入 prompt
- 调用 `call_llm(..., json_mode=True)`
- 从模型输出里解析第一个 JSON 数组
- 校验数量，至少要有 5 个 Benchmark
- 转成 `Benchmark` 对象后返回

### 7.2 Fallback 路径

如果 LLM 调用失败、JSON 解析失败、或者抽取结果不够 5 条，就会走本地兜底：

- 根据 topic 关键词选择一组 Benchmark 模板
- 当前支持 agent / rag / tool / generic 几类
- fallback 使用真实论文、代码、榜单链接
- 避免因为模型或网络问题导致整条链路中断

### 7.3 后处理补全

为了减少空值，当前 extractor 还会做一层后处理：

- 去重 `evaluated_ability`、`metrics`、`evidence`
- 把能从名称、任务类型、已有链接推出来的字段尽量补齐
- 自动补 `description`
- 自动补 `metrics`
- 自动补 `limitations`
- 自动补 `suitable_usage`
- 若 `open_source` 缺失，会结合 `code_url` 粗略判断
- 若 `evidence` 为空，会优先用 `paper_url`、`code_url`、`dataset_url`、`leaderboard_url` 补上

## 8. prompts/extractor.md 做了什么

prompt 里定义了：

- 角色设定
- 输入结构
- 输出 JSON 数组格式
- 评分字段说明
- 字段填写要求

当前 prompt 的核心要求是：

- 至少抽取 5 个 Benchmark
- 能从报告中找到或合理推断的字段尽量填写，不要轻易留空
- 实在无法确认的字段再填 `null`
- `evidence` 至少保留一个真实链接
- 只输出 JSON，不要输出其他文字

## 9. 输出目录和缓存规则

缓存路径由 `src/cache.py` 决定：

- topic 会被转换成安全目录名
- `AI Agent Evaluation Benchmark` 对应的目录名通常是 `ai_agent_evaluation_benchmark`
- 你当前看到的缓存目录是：`data/cache/ai_agent_evaluation/`

Extractor 最终会在该目录下生成：

- `benchmarks.json`

## 10. 交给 D 同学时要注意什么

- 不要改字段名
- 不要把 `evaluated_ability` 改成字符串
- 不要把评分字段改成字符串或浮点数
- 不要把 `evidence` 留空
- 不要把 `benchmarks.json` 当成自由格式文本
- D 同学会直接基于这些字段计算 `task_fit_score`

## 11. 当前实现特点

- LLM 不可用时仍然能产出稳定结果
- fallback 已经覆盖多个 topic 类型
- 输出尽量少空值，便于后续评分模块使用
- 真实证据链接优先，不编造 URL
- 兼容 `src/pipeline.py` 的现有调用方式

## 12. 已知边界

- LLM 接口失败时会看到 502，这时会自动降级到 fallback
- `dataset_url` 和 `leaderboard_url` 不是每个 Benchmark 都有
- 如果原始报告本身没有提供某个字段，后处理也不能凭空生成真实来源
- `evidence` 会尽量补真实链接，但仍以原始信息和已知公开链接为准

## 13. 自测方式

可以用下面的方式检查 Extractor 是否正常：

```bash
c:/Users/15318/PycharmProjects/benchmark_agent/.venv/Scripts/python.exe -c "from src.extractor import extract_benchmarks; from src.cache import load_cache; report = load_cache('ai_agent_evaluation', 'raw_report.md'); items = [b.model_dump() for b in extract_benchmarks(report, 'AI Agent Evaluation Benchmark')]; print('count=', len(items)); print('first keys=', list(items[0].keys()) if items else 'empty'); print('first evidence=', items[0].get('evidence') if items else 'empty')"
```

预期结果：

- 至少 5 条 Benchmark
- 第一条里 `evidence` 不为空
- 8 个评分字段都在 `1-5` 范围内

## 14. 交接结论

Extractor 模块当前已经完成，能够：

- 接收 B 模块的 `raw_report.md`
- 输出符合约定的 `benchmarks.json`
- 在 LLM 失败时自动兜底
- 尽量减少空字段

可以直接交给 D 同学继续做评分和推荐理由。