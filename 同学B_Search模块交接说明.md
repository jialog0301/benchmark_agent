# 同学 B Search 模块交接说明

## 1. 我负责的范围

我负责：

- Query Planner
- Search Agent

对应文件：

- `src/planner.py`
- `src/searcher.py`
- `prompts/planner.md`
- `prompts/searcher.md`
- `requirements.txt`
- `.env.example`
- `data/cache/ai_agent_evaluation/planner_result.json`
- `data/cache/ai_agent_evaluation/raw_report.md`

我没有负责：

- Extractor
- Scorer
- Judge
- Report Writer
- UI 展示优化

## 2. 模块在整体 pipeline 中的位置

整体流程：

User Input  
→ Query Planner  
→ Search Agent  
→ Benchmark Extractor  
→ Task-Fit Scorer  
→ LLM Judge  
→ Report Writer  
→ Streamlit UI

B 模块向 C 模块提供中间产物：

- `planner_result.json`
- `raw_report.md`

## 3. 对外接口（不要改签名）

```python
def plan_queries(topic: str, mode: str) -> dict:
    ...

def run_research(topic: str, plan: dict) -> str:
    ...
```

`pipeline.py` 调用方式：

```python
plan = planner.plan_queries(topic, mode)
raw_report = searcher.run_research(topic, plan)
```

## 4. planner.py 做了什么

- 读取 `prompts/planner.md`
- 根据 `topic`、`mode` 生成 `search_goals` / `search_queries` / `expected_outputs`
- 优先调用 LLM
- 支持 JSON 清洗与鲁棒解析
- LLM 不可用时使用 deterministic fallback
- mode 会影响搜索方向：
  - 课程实验：教学价值、资源完整度、复现成本、时间成本
  - 科研调研：论文、综述、权威性、leaderboard、覆盖度
  - 快速复现：GitHub、开源实现、文档、quickstart、dataset availability

## 5. searcher.py 做了什么

- 接收 `topic` 和 `plan`
- 按 `search_queries` 执行搜索（优先 Tavily，失败降级）
- 多源容错（Tavily / DuckDuckGo / arXiv / GitHub）
- 统一输出 Markdown `raw_report`
- 每个 benchmark 使用固定字段名，便于 extractor 抽取
- 不做最终排序，不输出最终推荐结论（D/E 负责）

## 6. Topic-aware fallback 说明

searcher 的 fallback 不是固定 AI-Agent 候选，而是按 topic 类型选择：

AI Agent 主题候选：

- AgentBench
- WebArena
- SWE-bench
- GAIA
- OSWorld
- ToolBench

RAG 主题候选：

- RAGAS
- RAGBench
- RGB
- CRUD-RAG
- BEIR
- KILT
- HotpotQA
- Natural Questions

Code Agent 主题候选：

- SWE-bench
- SWE-bench Verified
- HumanEval
- MBPP
- BigCodeBench
- RepoBench
- Agentless

说明：

- fallback 主要用于无 API key、无网络、搜索结果不足
- 不确定链接写 `null`，不编造 URL
- RAG / Code Agent 不会被固定 AI-Agent 候选污染

## 7. 缓存文件说明

pipeline 会生成：

- `planner_result.json`
- `raw_report.md`

当前保留两个目录以兼容文档与 `cache.py`：

- `data/cache/ai_agent_evaluation_benchmark/`
- `data/cache/ai_agent_evaluation/`

原因：

- `cache.py` 会把 `AI Agent Evaluation Benchmark` 映射到 `ai_agent_evaluation_benchmark`
- 开发指南示例目录是 `ai_agent_evaluation`
- 两者同时保留可以避免联调路径不一致

## 8. raw_report.md 与 benchmarks.json 字段约定的关系

- B 模块不直接生成 `benchmarks.json`
- B 模块只生成 `raw_report.md`
- `raw_report.md` 中每个 benchmark 已按稳定英文字段名输出，便于 C 抽取
- C 模块负责从 `raw_report.md` 抽取并产出最终 `benchmarks.json`
- C 的 `benchmarks.json` 必须遵守《benchmarks.json 字段约定》
- D 会依赖这些字段做 `task_fit_score` 和 `rank`，字段名与类型不能随意改
- B 的 `raw_report` 不包含 `rank` / `task_fit_score` / `recommendation_reason`（属于 D/E）

## 9. 给 C 同学的注意事项

- `raw_report.md` 是 Markdown，不是 JSON
- 每个 benchmark 使用固定字段名
- `evaluated_ability` / `metrics` / `evidence` 是列表
- 评分字段是 `1-5` 整数
- 可能存在 `null` 字段，不是错误
- 不要假设每个 benchmark 都有完整 paper/code/dataset/leaderboard

## 10. 给 D/E 同学的注意事项

- B 不做最终推荐排序
- B 不输出推荐理由
- `raw_report` 中内容是候选信息和证据，不是最终结果
- 若链接缺失，建议降低“资源完整度”相关分，不要直接报错



## 12. 环境变量




说明：

- 无 LLM key：planner 自动 fallback
- 无 Tavily key 或网络失败：searcher 自动 fallback
- `.env.example` 只能放占位符，不能放真实 key
- 不要提交 `.env`

## 13. B 模块自测

```bash
python -m py_compile src/planner.py src/searcher.py src/pipeline.py src/cache.py src/schemas.py src/llm_client.py
```

```bash
python - <<'PY'
from src.planner import plan_queries
from src.searcher import run_research
topic = "AI Agent Evaluation Benchmark"
mode = "课程实验"
plan = plan_queries(topic, mode)
assert isinstance(plan, dict)
assert plan["topic"] == topic
assert plan["mode"] == mode
assert len(plan["search_goals"]) >= 5
assert len(plan["search_queries"]) >= 5
assert len(plan["expected_outputs"]) >= 4
report = run_research(topic, plan)
assert isinstance(report, str)
assert "# " in report
for name in ["AgentBench", "WebArena", "SWE-bench", "GAIA", "OSWorld"]:
    assert name in report, f"missing {name}"
print("B module smoke test passed")
PY
```

最终验收覆盖：

- topics: AI Agent / RAG / Code Agent
- modes: 课程实验 / 科研调研 / 快速复现

目标结果：

- `FINAL: PASS`
- RAG 的 `fixed_hit` 低（0~2）
- Code Agent 的 `fixed_hit` 低（0~1）
- 每个 topic 至少 5 个 benchmark

## 14. 已知边界

- 搜索结果依赖网络与 API，有波动
- 无网络时 fallback 是稳定 demo 数据
- Searcher 不保证每个链接字段都完整
- Searcher 不负责最终排序
- 不要把 raw_report 的自然语言顺序当最终排名
