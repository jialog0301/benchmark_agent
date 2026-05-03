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
- `data/cache/ai_agent_evaluation_benchmark/planner_result.json`
- `data/cache/ai_agent_evaluation_benchmark/raw_report.md`
- `data/cache/ai_agent_evaluation/planner_result.json`
- `data/cache/ai_agent_evaluation/raw_report.md`



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
- 优先调用 LLM（`call_llm(..., json_mode=True)`）
- 做鲁棒 JSON 解析（code fence、解释文本、thinking 混杂）
- LLM 不可用时走 deterministic fallback（不抛错）
- `mode` 会影响搜索方向：
  - 课程实验：教学价值、资源完整度、复现成本、时间成本
  - 科研调研：论文、综述、权威性、leaderboard、覆盖度
  - 快速复现：GitHub、开源实现、文档、quickstart、dataset availability

## 5. searcher.py 做了什么
- 接收 `topic` 和 `plan`
- 基于 `search_queries` 做多源检索（Tavily 优先，失败降级）
- 支持 Tavily / DuckDuckGo / arXiv / GitHub，逐源容错
- 输出 Markdown 格式 `raw_report.md`
- 每个 benchmark 用统一字段模板，便于 extractor 抽取
- 不做最终排名，不输出最终推荐结论（D/E 职责）

## 6. Topic-aware fallback 说明
Searcher 的 fallback 不是固定 AI-Agent 候选，而是按 topic 类型选择：

AI Agent 主题：
- AgentBench
- WebArena
- SWE-bench
- GAIA
- OSWorld
- ToolBench
- Mind2Web
- AgentBoard

RAG 主题：
- RAGAS
- RAGBench
- RGB
- CRUD-RAG
- BEIR
- KILT
- HotpotQA
- Natural Questions

Code Agent 主题：
- SWE-bench
- SWE-bench Verified
- HumanEval
- MBPP
- BigCodeBench
- RepoBench
- Agentless
- APPS

说明：
- fallback 用于无 API key、无网络、搜索结果不足
- 链接缺失统一写 `null`，不编造 URL
- RAG / Code Agent 不会被固定 AI-Agent 候选污染

## 7. raw_report.md 与 benchmarks.json 字段约定的关系
- B 模块不直接生成 `benchmarks.json`
- B 模块只生成 `raw_report.md`
- `raw_report.md` 中每个 benchmark 已按稳定英文字段名组织
- C 模块负责从 `raw_report.md` 抽取并输出 `benchmarks.json`
- C 产出的 `benchmarks.json` 需遵守《benchmarks.json 字段约定》
- D 依赖这些字段计算 `task_fit_score` 和 `rank`，字段名/类型不能随意变
- B 的 `raw_report.md` 不包含：
  - `rank`
  - `task_fit_score`
  - `recommendation_reason`

## 8. raw_report.md 字段结构（给 C/D/E）
每个 benchmark 块形如：

```text
### Benchmark N: <name>
name:
description:
task_type:
evaluated_ability:
metrics:
paper_url:
code_url:
dataset_url:
leaderboard_url:
project_url:
open_source:
resource_evidence:
reproduction_evidence:
teaching_evidence:
research_evidence:
popularity_evidence:
time_cost_evidence:
documentation_evidence:
authority_evidence:
resource_completeness:
reproduction_difficulty:
teaching_value:
research_value:
topic_popularity:
time_cost_friendliness:
documentation_quality:
authority:
suggested_scores_for_extractor:
limitations:
suitable_usage:
evidence:
```

关键约束：
- `evaluated_ability` / `metrics` / `evidence` 为列表
- 8 个评分字段是 `1-5` 整数
- 缺失链接为 `null`
- 空列表统一为 `[]`（已修复，不再输出 `- null`）

## 9. 缓存文件说明
pipeline 会生成：
- `planner_result.json`
- `raw_report.md`

当前保留两个目录以兼容开发指南和 `cache.py`：
- `data/cache/ai_agent_evaluation_benchmark/`
- `data/cache/ai_agent_evaluation/`

原因：
- `cache.py` 会把 `AI Agent Evaluation Benchmark` 映射到 `ai_agent_evaluation_benchmark`
- 开发指南示例目录是 `ai_agent_evaluation`

## 10. 给 C 同学的注意事项
- `raw_report.md` 是 Markdown，不是 JSON
- 按 `### Benchmark` 分块再逐字段抽取
- 字段可能为 `null` 或 `[]`，不是错误
- 不要假设每条 benchmark 都有完整 paper/code/dataset/leaderboard
- Searcher 提供候选与证据，不提供最终排序

## 11. 给 D/E 同学的注意事项
- B 不做最终推荐排序
- B 不输出 recommendation_reason
- `raw_report` 中“适配性描述”只是初步信息
- 缺失链接不应导致报错，建议在资源完整度等维度扣分处理




## 13. 环境变量
可选环境变量：

```env
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_BASE_URL=https://api.minimax.chat/v1
MINIMAX_MODEL=MiniMax-M1
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_BASE_URL=https://api.anthropic.com
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
TAVILY_API_KEY=your_tavily_api_key_here
GITHUB_TOKEN=your_github_token_here
```

说明：
- 无 LLM key：planner 自动 fallback
- 无 Tavily key / 无网络：searcher 自动 fallback
- 不要提交 `.env`
- `.env.example` 只保留占位符

## 14. B 模块自测命令
语法检查：

```bash
python -m py_compile src/planner.py src/searcher.py src/pipeline.py src/cache.py src/schemas.py src/llm_client.py
```

最小 smoke test（Linux/macOS）：

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

最小 smoke test（Windows PowerShell）：

```powershell
@'
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
'@ | python -
```

最终验收目标：
- `FINAL: PASS`
- topic 覆盖 AI Agent / RAG / Code Agent
- mode 覆盖 课程实验 / 科研调研 / 快速复现
- 每个 topic 至少 5 个 benchmark（当前常见为 8）
- RAG `fixed_hit` 低（通常 0）
- Code Agent `fixed_hit` 低（通常 0~1）

## 15. 已知边界
- 搜索结果受网络/API 影响，会波动
- 无网络时 fallback 是稳定 demo 数据
- Searcher 不保证每个链接字段都完整
- Searcher 不负责最终排序
- 其他模块不要把 raw_report 的自然语言顺序当最终 rank
- 新增 topic 时，建议补充对应 topic-aware fallback 候选池
