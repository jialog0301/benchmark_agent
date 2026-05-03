# 同学 D Scorer & Judge 模块交接说明

## 1. 我负责的范围

我负责的是 Scorer & Judge 模块，也就是把 C 同学生成的结构化 `benchmarks.json` 转成带 Task-Fit Score、排名和推荐理由的 `ranked_benchmarks.json`。

对应文件：

- `src/scorer.py`
- `src/judge.py`
- `prompts/judge.md`
- `data/cache/<topic目录>/ranked_benchmarks.json`

我没有负责：

- `src/planner.py`
- `src/searcher.py`
- `src/extractor.py`
- `src/reporter.py`
- `app.py`
- `src/pipeline.py` 的整体编排逻辑

---

## 2. 模块在整体 pipeline 中的位置

整体流程是：

User Input  
→ Query Planner  
→ Search Agent  
→ Benchmark Extractor  
→ Task-Fit Scorer  
→ LLM Judge  
→ Report Writer  
→ Streamlit UI

D 模块承接 C 模块，向 E 模块提供可直接展示和写报告的数据：

- 输入：`benchmarks.json`
- 输出：`ranked_benchmarks.json`

D 模块的作用：

- 根据用户选择的 `mode` 计算 Task-Fit Score
- 对 Benchmark 进行排序
- 为每个 Benchmark 生成推荐理由
- 保留 C 输出的所有原始字段，方便 E/UI 做表格和详情展示

---

## 3. 对外接口

核心接口不要改签名：

```python
def score_benchmarks(benchmarks: list[dict], mode: str) -> list[dict]:
    ...
```

```python
def generate_recommendation_reason(benchmark: dict, mode: str) -> str:
    ...
```

`pipeline.py` 当前调用方式：

```python
ranked_benchmarks = scorer.score_benchmarks(benchmarks, mode)

for bm in ranked_benchmarks:
    if not bm.get("recommendation_reason"):
        reason = judge.generate_recommendation_reason(bm, mode)
        bm["recommendation_reason"] = reason
```

---

## 4. 输入是什么

D 的输入不是用户原始输入，也不是 `raw_report.md`。

D 的输入是 C 模块输出的结构化 Benchmark 列表：

```text
benchmarks.json
```

每条 Benchmark 通常包含：

- `name`
- `description`
- `task_type`
- `evaluated_ability`
- `metrics`
- `paper_url`
- `code_url`
- `dataset_url`
- `leaderboard_url`
- `open_source`
- `resource_completeness`
- `reproduction_difficulty`
- `teaching_value`
- `research_value`
- `topic_popularity`
- `time_cost_friendliness`
- `documentation_quality`
- `authority`
- `limitations`
- `suitable_usage`
- `evidence`

D 依赖其中 8 个评分字段：

```text
resource_completeness
reproduction_difficulty
teaching_value
research_value
topic_popularity
time_cost_friendliness
documentation_quality
authority
```

这些字段必须是 1-5 的整数。如果 C 输出缺失或类型异常，D 会做保守归一化，默认按 3 分处理。

---

## 5. 输出是什么

D 最终输出的是 `list[dict]`，保存到缓存后就是：

```text
ranked_benchmarks.json
```

每条数据会保留 C 的所有字段，并新增：

```json
{
  "mode": "课程实验",
  "task_fit_score": 3.4,
  "rank": 1,
  "recommendation_reason": "中文推荐理由"
}
```

字段说明：

- `mode`: 当前推荐模式
- `task_fit_score`: 当前模式下的任务适配分数，0-5，保留两位小数
- `rank`: 当前模式下的排名，从 1 开始
- `recommendation_reason`: 推荐理由，中文，结合 mode、分数和维度解释

---

## 6. topic 和 mode 的关系

系统整体是根据用户输入的 `topic + mode` 排名，而不是对所有 Benchmark 做全局排名。

但 D 模块不直接使用 `topic` 字符串。

实际关系是：

```text
用户输入 topic
→ B/C 生成该 topic 对应的 benchmarks.json
→ D 对这个 benchmarks.json 按 mode 排名
```

所以：

- `topic` 决定候选 Benchmark 集合
- `mode` 决定评分权重和推荐理由关注点
- D 消费当前 topic 对应的 `benchmarks.json`

如果手动把一个混合多个 topic 的测试文件传给 D，D 会如实对这个混合列表排序。这只是测试行为，不代表正式 pipeline 无视 topic。

---

## 7. scorer.py 做了什么

`src/scorer.py` 负责计算 Task-Fit Score 并排序。

主要逻辑：

1. 接收 `benchmarks` 和 `mode`
2. 归一化评分字段到 1-5
3. 根据 `mode` 选择不同评分公式
4. 计算 `task_fit_score`
5. 按分数降序排序
6. 生成 `rank`
7. 使用 `RankedBenchmark` schema 做结构校验
8. 返回 `list[dict]`

### 7.1 课程实验模式

适用场景：

```text
课程作业、课堂展示、学生实验
```

评分公式：

```text
Task-Fit Score =
0.30 × teaching_value
+ 0.25 × resource_completeness
+ 0.20 × (6 - reproduction_difficulty)
+ 0.15 × topic_popularity
+ 0.10 × time_cost_friendliness
```

说明：

- `reproduction_difficulty` 越高越难
- 所以要用 `6 - reproduction_difficulty` 转成复现友好度

### 7.2 科研调研模式

适用场景：

```text
论文调研、related work、研究综述、代表性 Benchmark 梳理
```

评分公式：

```text
Task-Fit Score =
0.30 × research_value
+ 0.25 × authority
+ 0.20 × topic_popularity
+ 0.15 × resource_completeness
+ 0.10 × coverage
```

其中：

```text
coverage = evaluated_ability 数量，限制在 1-5
```

### 7.3 快速复现模式

适用场景：

```text
快速 demo、小实验、短时间跑通 benchmark
```

评分公式：

```text
Task-Fit Score =
0.35 × (6 - reproduction_difficulty)
+ 0.25 × resource_completeness
+ 0.20 × documentation_quality
+ 0.15 × time_cost_friendliness
+ 0.05 × topic_popularity
```

---

## 8. 同分排序规则

如果多个 Benchmark 的 `task_fit_score` 相同，D 会使用稳定 tie-breaker：

```text
resource_completeness
reproduction_friendliness
documentation_quality
authority
原始输入顺序
```

这样可以避免完全随机排序，同时不改变 Task-Fit Score 本身。

---

## 9. judge.py 做了什么

`src/judge.py` 负责为每个已排序 Benchmark 生成推荐理由。

主要逻辑：

1. 读取 `prompts/judge.md`
2. 将 `benchmark` 和 `mode` 填入 prompt
3. 调用 `call_llm(..., json_mode=True)`
4. 从模型输出中解析第一个 JSON object
5. 提取 `recommendation_reason`
6. 如果 LLM 失败，使用本地 fallback 生成推荐理由

核心接口：

```python
def generate_recommendation_reason(benchmark: dict, mode: str) -> str:
    ...
```

---

## 10. prompts/judge.md 做了什么

`prompts/judge.md` 用于指导 LLM 生成推荐理由。

当前 prompt 要求：

- 输出中文
- 2-4 句话
- 点名 Benchmark 名称
- 引用 `task_fit_score`
- 引用 `rank`
- 至少引用 2 个与当前 mode 相关的具体分数
- 说明为什么适合或不适合当前 mode
- 不编造输入中没有的事实
- 只输出 JSON object：

```json
{
  "recommendation_reason": "中文推荐理由"
}
```

不同 mode 的解释重点：

### 课程实验

- `teaching_value`
- `resource_completeness`
- `6 - reproduction_difficulty`
- `topic_popularity`
- `time_cost_friendliness`

### 科研调研

- `research_value`
- `authority`
- `topic_popularity`
- `resource_completeness`
- `evaluated_ability` 覆盖范围

### 快速复现

- `6 - reproduction_difficulty`
- `resource_completeness`
- `documentation_quality`
- `time_cost_friendliness`
- `open_source`
- `code_url`
- `dataset_url`

---

## 11. 缓存文件说明

标准 pipeline 会把 D 的输出保存为：

```text
data/cache/<topic目录>/ranked_benchmarks.json
```

例如：

```text
topic = "AI Agent Evaluation Benchmark"
```

对应：

```text
data/cache/ai_agent_evaluation_benchmark/ranked_benchmarks.json
```

注意：

```text
data/cache/benchmarks.json
```

这是手动测试文件，不是标准 pipeline 默认读取路径。

D 的正式输入应来自：

```python
load_cache(topic, "benchmarks.json")
```

而不是固定读取 `data/cache/benchmarks.json`。

---

## 12. 环境变量和 LLM 配置//可自由配置

D 的 Judge 会通过 `src.llm_client.call_llm()` 调用 LLM。

如果没有可用 LLM，D 不会中断，而是走 fallback 推荐理由。

当前测试中可用 DeepSeek 的 OpenAI-compatible 配置：

```bash
unset MINIMAX_API_KEY
unset MINIMAX_BASE_URL
unset ANTHROPIC_API_KEY
unset ANTHROPIC_BASE_URL

export OPENAI_API_KEY="your_deepseek_api_key"
export OPENAI_BASE_URL="https://api.deepseek.com"
export MINIMAX_MODEL="deepseek-chat"
```

说明：

- 当前 `llm_client.py` 默认模型变量仍使用 `MINIMAX_MODEL`
- 使用 DeepSeek 时需要把 `MINIMAX_MODEL` 设为 `deepseek-chat`
- `deepseek-chat` 是非思考模式
- 不要提交真实 API key

---

## 13. D 模块自测命令

### 13.1 语法检查

```bash
python -m py_compile src/scorer.py src/judge.py src/schemas.py src/llm_client.py
```

### 13.2 Scorer 最小测试

```bash
python - <<'PY'
from src.cache import load_cache
from src.scorer import score_benchmarks

topic = "AI Agent Evaluation Benchmark"
benchmarks = load_cache(topic, "benchmarks.json")

for mode in ["课程实验", "科研调研", "快速复现"]:
    ranked = score_benchmarks(benchmarks, mode)
    assert ranked
    assert ranked[0]["rank"] == 1
    assert "task_fit_score" in ranked[0]
    print(mode, ranked[0]["name"], ranked[0]["task_fit_score"])

print("Scorer smoke test passed")
PY
```

### 13.3 Judge 是否真的调用 LLM

```bash
python - <<'PY'
from src.cache import load_cache
from src.scorer import score_benchmarks
import src.judge as judge

topic = "AI Agent Evaluation Benchmark"
mode = "课程实验"

benchmarks = load_cache(topic, "benchmarks.json")
ranked = score_benchmarks(benchmarks, mode)

judge._fallback_recommendation_reason = lambda benchmark, mode: "__FALLBACK_USED__"

reason = judge.generate_recommendation_reason(ranked[0], mode)
print(reason)

assert reason != "__FALLBACK_USED__", "LLM Judge failed; fallback was used."
print("LLM Judge passed")
PY
```

### 13.4 生成 ranked_benchmarks.json

```bash
python - <<'PY'
from src.cache import load_cache, save_cache
from src.scorer import score_benchmarks
from src.judge import generate_recommendation_reason

topic = "AI Agent Evaluation Benchmark"
mode = "课程实验"

benchmarks = load_cache(topic, "benchmarks.json")
ranked = score_benchmarks(benchmarks, mode)

for bm in ranked:
    bm["recommendation_reason"] = generate_recommendation_reason(bm, mode)

save_cache(topic, "ranked_benchmarks.json", ranked)

print("saved:", len(ranked))
for bm in ranked:
    print(bm["rank"], bm["name"], bm["task_fit_score"])
PY
```

---

## 14. 给 E/UI 同学的注意事项

E/UI 应该使用：

```python
result = run_benchmark_radar(topic, mode, use_cache)
```

然后展示：

```python
result["ranked_benchmarks"]
```

推荐展示字段：

- `rank`
- `name`
- `task_type`
- `task_fit_score`
- `recommendation_reason`
- `resource_completeness`
- `reproduction_difficulty`
- `teaching_value`
- `research_value`
- `topic_popularity`
- `time_cost_friendliness`
- `documentation_quality`
- `authority`
- `paper_url`
- `code_url`
- `dataset_url`
- `leaderboard_url`

注意：

- `reproduction_difficulty` 越高越难，不是越高越好。
- 不同 `mode` 下排序会变化。
- UI 不要重新实现评分公式。
- UI 不要把所有缓存目录下的数据混合排名。
- `recommendation_reason` 已由 D 生成，E 可以直接展示。

---

## 15. 已知边界

- D 的排序质量依赖 C 输出的 `benchmarks.json`。
- 如果 C 的候选重复、topic 混杂或评分字段过于同质化，D 会如实排序，但最终展示效果会受影响。
- 如果 LLM 不可用，Judge 会使用 fallback 理由，质量略低但能保证 pipeline 不报错。
- D 不负责判断 Benchmark 是否应该属于某个 topic，这由 B/C 负责。
- D 不负责生成最终 Markdown 报告，这由 E 的 `reporter.py` 负责。

---

## 16. 交接结论

D 模块当前已经完成，能够：

- 接收 C 输出的 `benchmarks.json`
- 根据 `mode` 计算 Task-Fit Score
- 输出稳定排名
- 生成 `rank`
- 调用 LLM 生成推荐理由
- 在 LLM 失败时 fallback
- 产出可供 E/UI 展示和 Reporter 写报告的 `ranked_benchmarks.json`

一句话总结：

```text
D 模块负责把当前 topic 对应的 benchmarks.json 转换成 mode-aware 的 ranked_benchmarks.json，并补充每个 Benchmark 的中文推荐理由。
```
