# 同学 B Search 模块交接说明

## 1. 我负责的范围
我负责以下模块：
- Query Planner
- Search Agent

对应文件：
- src/planner.py
- src/searcher.py
- prompts/planner.md
- prompts/searcher.md
- requirements.txt
- .env.example
- data/cache/ai_agent_evaluation_benchmark/planner_result.json
- data/cache/ai_agent_evaluation_benchmark/raw_report.md
- data/cache/ai_agent_evaluation/planner_result.json
- data/cache/ai_agent_evaluation/raw_report.md

我没有负责以下模块：
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

B 模块产物会传给 C 同学：
- planner_result.json
- raw_report.md

## 3. 对外接口
以下函数签名不要改：

```python
def plan_queries(topic: str, mode: str) -> dict:
    ...

def run_research(topic: str, plan: dict) -> str:
    ...
```

`pipeline.py` 中会调用：

```python
plan = planner.plan_queries(topic, mode)
raw_report = searcher.run_research(topic, plan)
```

## 4. planner.py 做了什么
`planner.py` 的核心职责：
- 读取 `prompts/planner.md`
- 根据 `topic` 和 `mode` 生成 `search_goals`、`search_queries`、`expected_outputs`
- 优先调用 LLM
- 支持 JSON 清洗和解析
- LLM 不可用时使用 deterministic fallback
- `mode` 会影响搜索方向

三种 mode 差异：
- 课程实验：教学价值、资源完整度、复现成本、时间成本
- 科研调研：论文、综述、权威性、leaderboard、覆盖度
- 快速复现：GitHub、开源实现、文档、quickstart、dataset availability

## 5. searcher.py 做了什么
`searcher.py` 的核心职责：
- 接收 `topic` 和 `plan`
- 根据 `search_queries` 执行搜索
- 优先使用 Tavily
- 没有 Tavily 或网络失败时 fallback
- 输出 Markdown 格式 `raw_report`
- 每个 benchmark 尽量包含名称、来源、描述、任务类型、评测能力、指标、paper/code/dataset/leaderboard URL、开源情况、复现难度等
- 不做最终排序，不写最终推荐结论（这是 D/E 的职责）

## 6. Topic-aware fallback 说明
`searcher` 不会固定返回同一组 AI Agent 候选，而是根据 topic 动态选择 fallback。

AI Agent 主题 fallback 候选：
- AgentBench
- WebArena
- SWE-bench
- GAIA
- OSWorld
- ToolBench

RAG 主题 fallback 候选：
- RAGAS
- RAGBench
- RGB
- CRUD-RAG
- BEIR
- KILT
- HotpotQA
- Natural Questions

Code Agent 主题 fallback 候选：
- SWE-bench
- SWE-bench Verified
- HumanEval
- MBPP
- BigCodeBench
- RepoBench
- Agentless

说明：
- fallback 主要用于无 API Key、无网络、搜索结果不足时
- 不确定的链接写“未找到”，不编造 URL
- RAG 和 Code Agent 不会被固定 AI-Agent 候选污染

## 7. 缓存文件说明
pipeline 会生成：
- planner_result.json
- raw_report.md

目前为了兼容文档和 `cache.py`，保留了两个缓存目录：
- `data/cache/ai_agent_evaluation_benchmark/`
- `data/cache/ai_agent_evaluation/`

原因：
- `cache.py` 会把 `AI Agent Evaluation Benchmark` 转成 `ai_agent_evaluation_benchmark`
- 框架开发指南里写的是 `ai_agent_evaluation`
- 所以两个目录都保留，避免对不上

## 8. 给 C 同学的注意事项
C 同学负责 extractor 时，请注意：
- `raw_report.md` 是 Markdown，不是 JSON
- 每个 benchmark 用统一结构写出，便于抽取
- 可能有字段写“未找到”或 `null`，这不是错误
- 不要假设每个 benchmark 都有完整 paper/code/dataset/leaderboard
- C 的 extractor 应该能容忍缺字段
- Searcher 不保证最终排名，只提供候选和证据
- Extractor 应该从 `raw_report.md` 中抽取结构化 benchmark list

## 9. 给 D/E 同学的注意事项
D/E 同学负责 scorer、judge、report writer 时，请注意：
- B 模块不做最终推荐排序
- `raw_report` 中“适合课程实验/科研调研/快速复现”只是初步判断
- 最终分数、推荐理由、排序应由 scorer/judge/reporter 完成
- 如果某些 benchmark 链接缺失，不代表不能评分，应降低资源完整度分而不是直接报错

## 10. 给 UI 同学的注意事项
UI 调用主 pipeline 即可，不建议直接调用 searcher。

如果需要展示中间结果，可以展示：
- `planner_result.json` 中的 `search_goals` / `search_queries`
- `raw_report.md` 的 Markdown 内容
- 当前 `topic` 和 `mode`

## 11. 环境变量
可选环境变量：

```bash
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_BASE_URL=https://api.minimax.chat/v1
MINIMAX_MODEL=MiniMax-M1
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_BASE_URL=https://api.anthropic.com
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
TAVILY_API_KEY=your_tavily_api_key_here
```

说明：
- 没有 LLM key 时 planner 会 fallback
- 没有 Tavily key 时 searcher 会 fallback 或尝试其他搜索方式
- 不要提交 `.env`
- `.env.example` 只能放占位符，不能放真实 key

## 12. 如何运行 B 模块自测
先运行：

```bash
python -m py_compile src/planner.py src/searcher.py src/pipeline.py src/cache.py src/schemas.py src/llm_client.py
```

最小 smoke test：

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

最终验收说明：
- 最终验收脚本已覆盖 topic：
- AI Agent Evaluation Benchmark
- RAG Evaluation Benchmark
- Code Agent Benchmark

- 并覆盖三种 mode：
- 课程实验
- 科研调研
- 快速复现

结果：
- FINAL: PASS
- RAG fixed_hit = 0
- Code Agent fixed_hit = 0–1
- 每个 topic 都至少生成 5 个 benchmark

## 13. 已知边界
- 搜索结果依赖网络和 API，可变动
- 无网络时 fallback 是稳定 demo 数据
- Searcher 不保证链接 100% 全字段完整
- Searcher 不负责最终排名
- 其他同学不要依赖 raw_report 中的自然语言顺序作为最终排序
- 如果新增 topic，建议补充对应 topic-aware fallback candidates

## 14. 提交前注意事项
- 提交前运行 `py_compile` 和最终验收脚本
