# BenchmarkRadarAgent 需求文档

## 1. 项目名称

**BenchmarkRadarAgent：AI Benchmark 自动调研、结构化对比与任务适配推荐智能体**

---

## 2. 项目定位

BenchmarkRadarAgent 是一个面向 AI 领域 Benchmark 调研的智能体系统。

用户输入一个 AI 研究方向，例如：

```text
AI Agent Evaluation Benchmark
RAG Evaluation Benchmark
LLM Tool Use Benchmark
Web Agent Benchmark
Code Agent Benchmark
```

系统自动完成：

```text
任务规划 → 资料检索 → Benchmark 信息抽取 → 结构化对比 → Task-Fit Score 评分 → 推荐报告生成 → 可视化展示
```

本系统**不是复现 Benchmark 的平台**，而是一个帮助用户快速了解、比较和选择 Benchmark 的调研与推荐系统。

---

## 3. 项目背景

AI 领域发展迅速，各类 Benchmark、Dataset、Leaderboard、评测指标和开源实现分散在论文、GitHub、官网、博客和综述文章中。

用户如果想了解某个方向的评测体系，通常需要手动完成：

```text
1. 搜索相关 Benchmark
2. 阅读论文和 GitHub
3. 对比评测任务、指标和数据集
4. 判断是否开源、是否容易复现
5. 根据自己的目的选择合适 Benchmark
```

这个过程耗时较高，也容易遗漏重要信息。

因此，本项目希望构建一个智能体系统，自动完成 Benchmark 调研与任务适配推荐。

---

## 4. 核心目标

本项目目标是构建一个基于 GPT Researcher / Search API / 大模型的 Benchmark 调研智能体，完成以下功能：

```text
1. 根据用户输入主题，自动规划搜索任务。
2. 自动检索论文、GitHub、官网、Leaderboard 等公开资料。
3. 从非结构化资料中抽取 Benchmark 结构化信息。
4. 根据不同使用场景计算 Task-Fit Score。
5. 输出 Benchmark 对比表、推荐排序和推荐理由。
6. 自动生成 Markdown 调研报告。
7. 使用 Streamlit 提供可交互 Demo 页面。
8. 支持缓存，保证展示稳定。
```

---

## 5. 系统输入与输出

### 5.1 系统输入

系统输入包括两个部分：

#### 1. 调研主题 `topic`

用户想了解的 Benchmark 方向。

示例：

```text
AI Agent Evaluation Benchmark
LLM Tool Use Benchmark
RAG Evaluation Benchmark
Web Agent Benchmark
Code Agent Benchmark
Multimodal LLM Benchmark
Text-to-SQL Benchmark
```

#### 2. 推荐模式 `mode`

用户使用 Benchmark 的目的。

系统初期支持三种模式：

```text
1. 课程实验模式
2. 科研调研模式
3. 快速复现模式
```

---

### 5.2 系统输出

系统最终输出：

```text
1. 搜索规划结果
2. 原始调研报告
3. Benchmark 结构化对比表
4. Task-Fit Score 排名
5. 每个 Benchmark 的推荐理由
6. 适合当前模式的使用建议
7. Markdown 格式最终报告
```

---

## 6. 推荐模式设计

### 6.1 为什么需要模式？

同一个 Benchmark 在不同使用目的下，优先级不同。

例如：

| Benchmark | 科研调研 | 课程实验 | 快速复现 |
|---|---:|---:|---:|
| SWE-bench | 高 | 中 | 低 |
| WebArena | 高 | 中高 | 低 |
| GAIA / GAIA-lite | 中高 | 高 | 高 |
| ToolBench | 中高 | 高 | 中高 |

如果不区分用户目标，系统可能推荐一个“学术价值高但复现很难”的 Benchmark 给想快速做 Demo 的用户，导致推荐不实用。

因此系统引入 `mode`，根据用户目标动态调整评分标准。

---

### 6.2 模式一：课程实验模式

适用场景：

```text
用户想找适合课程作业、课堂展示、学生实验的 Benchmark。
```

关注维度：

```text
教学价值
资源完整度
复现友好度
方向热度
时间成本
```

推荐倾向：

```text
任务清晰、容易解释、资源完整、适合短周期完成的 Benchmark。
```

---

### 6.3 模式二：科研调研模式

适用场景：

```text
用户想了解某个方向的代表性 Benchmark，用于论文调研、related work、研究综述。
```

关注维度：

```text
科研价值
权威性
方向热度
覆盖范围
资源完整度
```

推荐倾向：

```text
代表性强、引用价值高、任务真实、能体现领域前沿问题的 Benchmark。
```

---

### 6.4 模式三：快速复现模式

适用场景：

```text
用户想尽快跑通一个 Benchmark，用于 Demo、小实验或快速验证。
```

关注维度：

```text
代码完整度
数据可获得性
文档质量
环境复杂度
运行成本
时间成本
```

推荐倾向：

```text
代码开源、文档清楚、数据容易获取、环境简单、能快速运行的 Benchmark。
```

---

## 7. 系统功能需求

### 7.1 Query Planner：任务规划模块

#### 功能说明

用户输入 `topic` 和 `mode` 后，系统首先调用大模型生成调研计划。

#### 输入示例

```json
{
  "topic": "AI Agent Evaluation Benchmark",
  "mode": "课程实验"
}
```

#### 输出示例

```json
{
  "topic": "AI Agent Evaluation Benchmark",
  "mode": "课程实验",
  "search_goals": [
    "查找 AI Agent 评测 Benchmark",
    "查找对应论文和 GitHub 仓库",
    "查找 Benchmark 的评测任务和指标",
    "判断 Benchmark 是否适合课程实验",
    "整理复现难度和教学价值"
  ],
  "search_queries": [
    "AI Agent evaluation benchmark 2024 2025",
    "LLM agent benchmark GitHub",
    "AgentBench WebArena SWE-bench GAIA OSWorld comparison",
    "tool use agent benchmark leaderboard",
    "AI agent evaluation survey"
  ],
  "expected_outputs": [
    "Benchmark 对比表",
    "Task-Fit Score 排名",
    "推荐理由",
    "最终调研报告"
  ]
}
```

#### 要求

```text
1. 搜索 query 不能写死为 AI Agent，要根据 topic 动态生成。
2. 不同 mode 下，搜索目标应略有差异。
3. 输出必须是结构化 JSON。
```

---

### 7.2 Search Agent：资料检索模块

#### 功能说明

根据 Query Planner 生成的搜索计划，调用 GPT Researcher 或 Search API 获取相关资料。

#### 可选数据源

```text
1. GPT Researcher
2. Tavily Search API
3. DuckDuckGo Search
4. arXiv API
5. GitHub Search API
6. Semantic Scholar API
7. 本地缓存
```

#### 输入

```json
{
  "topic": "AI Agent Evaluation Benchmark",
  "search_queries": [
    "AI Agent evaluation benchmark 2024 2025",
    "LLM agent benchmark GitHub"
  ]
}
```

#### 输出

原始调研报告：

```markdown
# AI Agent Evaluation Benchmark Research Report

## AgentBench
AgentBench is ...

## WebArena
WebArena is ...

## SWE-bench
SWE-bench is ...

## GAIA
GAIA is ...
```

或结构化搜索结果：

```json
[
  {
    "title": "AgentBench: Evaluating LLMs as Agents",
    "url": "https://...",
    "snippet": "AgentBench evaluates LLMs as agents across multiple environments.",
    "source": "web"
  }
]
```

#### 要求

```text
1. 至少支持一种 Search API。
2. 支持缓存，避免重复请求。
3. 如果 GPT Researcher 调用失败，允许读取本地 raw_report 作为兜底。
```

---

### 7.3 Benchmark Extractor：Benchmark 信息抽取模块

#### 功能说明

从原始调研报告或搜索结果中抽取 Benchmark 的结构化信息。

#### 输入

```text
raw_report.md
```

#### 输出字段

每个 Benchmark 输出如下结构：

```json
{
  "name": "WebArena",
  "description": "A realistic web environment for evaluating autonomous agents.",
  "task_type": "Web Agent Evaluation",
  "evaluated_ability": [
    "web navigation",
    "tool use",
    "long-horizon planning"
  ],
  "metrics": [
    "Task Success Rate"
  ],
  "paper_url": "https://...",
  "code_url": "https://...",
  "dataset_url": "https://...",
  "leaderboard_url": "https://...",
  "open_source": true,
  "resource_completeness": 4,
  "reproduction_difficulty": 4,
  "teaching_value": 5,
  "research_value": 5,
  "topic_popularity": 5,
  "time_cost_friendliness": 2,
  "documentation_quality": 3,
  "authority": 5,
  "limitations": "Environment deployment is relatively complex.",
  "suitable_usage": "Suitable for research analysis and advanced course demonstration.",
  "evidence": [
    "https://...",
    "https://..."
  ]
}
```

#### 字段说明

| 字段 | 含义 |
|---|---|
| name | Benchmark 名称 |
| description | 简要介绍 |
| task_type | 任务类型 |
| evaluated_ability | 评测能力 |
| metrics | 评测指标 |
| paper_url | 论文链接 |
| code_url | 代码链接 |
| dataset_url | 数据链接 |
| leaderboard_url | 榜单链接 |
| open_source | 是否开源 |
| resource_completeness | 资源完整度，1-5 |
| reproduction_difficulty | 复现难度，1-5，越高越难 |
| teaching_value | 教学价值，1-5 |
| research_value | 科研价值，1-5 |
| topic_popularity | 方向热度，1-5 |
| time_cost_friendliness | 时间友好度，1-5 |
| documentation_quality | 文档质量，1-5 |
| authority | 权威性，1-5 |
| limitations | 局限性 |
| suitable_usage | 适合的使用场景 |
| evidence | 证据来源 |

#### 要求

```text
1. 至少抽取 5 个 Benchmark。
2. 不确定字段允许为 null，不允许编造链接。
3. 每个 Benchmark 至少保留一个 evidence。
4. 输出必须是 JSON 数组。
```

---

### 7.4 Task-Fit Scorer：任务适配评分模块

#### 功能说明

根据用户选择的 `mode`，计算每个 Benchmark 对当前任务目标的适配程度。

#### 评分总称

```text
Task-Fit Score
```

当 `mode = 课程实验` 时，Task-Fit Score 相当于 Course-Fit Score。

---

#### 7.4.1 课程实验模式评分公式

```text
Task-Fit Score =
0.30 × Teaching Value
+ 0.25 × Resource Completeness
+ 0.20 × Reproduction Friendliness
+ 0.15 × Topic Popularity
+ 0.10 × Time Cost Friendliness
```

其中：

```text
Reproduction Friendliness = 6 - Reproduction Difficulty
```

---

#### 7.4.2 科研调研模式评分公式

```text
Task-Fit Score =
0.30 × Research Value
+ 0.25 × Authority
+ 0.20 × Topic Popularity
+ 0.15 × Resource Completeness
+ 0.10 × Coverage
```

如果暂时没有 `coverage` 字段，可以用 `evaluated_ability` 数量或 LLM Judge 估计。

---

#### 7.4.3 快速复现模式评分公式

```text
Task-Fit Score =
0.35 × Reproduction Friendliness
+ 0.25 × Resource Completeness
+ 0.20 × Documentation Quality
+ 0.15 × Time Cost Friendliness
+ 0.05 × Topic Popularity
```

#### 输出示例

```json
{
  "name": "GAIA",
  "mode": "课程实验",
  "task_fit_score": 4.45,
  "rank": 1,
  "recommendation_reason": "GAIA 任务形式清晰，复现成本相对较低，适合作为课程中的通用 Agent 能力评测案例。"
}
```

#### 要求

```text
1. 不同 mode 使用不同评分权重。
2. 输出最终排名。
3. 每个 Benchmark 必须生成推荐理由。
4. 分数保留两位小数。
```

---

### 7.5 LLM Judge：推荐理由生成模块

#### 功能说明

根据结构化 Benchmark 信息和 Task-Fit Score，调用大模型生成推荐解释。

#### 输入

```json
{
  "name": "WebArena",
  "mode": "快速复现",
  "task_fit_score": 2.85,
  "resource_completeness": 4,
  "reproduction_difficulty": 4,
  "documentation_quality": 3,
  "time_cost_friendliness": 2
}
```

#### 输出

```json
{
  "recommendation_reason": "WebArena 能评测真实网页环境中的 Agent 能力，资源较完整，但部署环境复杂，快速复现成本较高，因此不适合作为短时间 Demo 的首选。"
}
```

#### 要求

```text
1. 推荐理由必须结合 mode。
2. 推荐理由不能泛泛而谈。
3. 如果不推荐，也要说明原因。
```

---

### 7.6 Report Writer：报告生成模块

#### 功能说明

根据 Benchmark 对比表、Task-Fit Score 排名和推荐理由，生成最终 Markdown 报告。

#### 报告结构

```markdown
# BenchmarkRadar Report

## 1. 调研主题

## 2. 推荐模式

## 3. 背景与动机

## 4. Benchmark 总览

## 5. Benchmark 结构化对比表

## 6. Task-Fit Score 排名

## 7. Top Benchmark 分析

## 8. 推荐使用方案

## 9. 局限性

## 10. 参考资料
```

#### 输出示例

```markdown
# BenchmarkRadar Report: AI Agent Evaluation Benchmark

## 推荐模式：课程实验

本报告围绕 AI Agent Evaluation Benchmark 进行调研，并根据课程实验模式对相关 Benchmark 进行排序。

## 推荐结论

1. GAIA / GAIA-lite：适合作为通用 Agent 能力评测实验。
2. ToolBench：适合作为工具调用能力实验。
3. WebArena：教学价值高，但部署成本较高，适合作为进阶展示案例。
```

#### 要求

```text
1. 报告必须与用户选择的 mode 对齐。
2. 报告中要包含排序表。
3. 报告中要包含每个推荐 Benchmark 的理由。
4. 报告中要保留参考来源。
```

---

### 7.7 Streamlit UI：可视化交互界面

#### 功能说明

使用 Streamlit 构建可交互 Demo 页面。

#### 页面组件

```text
1. 系统标题
2. 调研主题输入框
3. 推荐模式下拉框
4. 是否使用缓存选项
5. 开始分析按钮
6. Planner 输出展示
7. Agent 执行过程展示
8. Benchmark 对比表
9. Task-Fit Score 排名
10. Markdown 报告展示
11. 报告下载按钮
```

#### 页面示意

```text
BenchmarkRadarAgent

请输入调研主题：
[ AI Agent Evaluation Benchmark ]

请选择推荐模式：
[ 课程实验 / 科研调研 / 快速复现 ]

[ 使用缓存 Demo ]  [ 开始分析 ]

Agent 执行过程：
✓ Planner Agent 生成搜索计划
✓ Search Agent 检索资料
✓ Extractor Agent 抽取 Benchmark 信息
✓ Scorer Agent 计算 Task-Fit Score
✓ Judge Agent 生成推荐理由
✓ Report Agent 生成报告

Benchmark 对比表：
...

Task-Fit Score 排名：
...

最终报告：
...
```

#### 要求

```text
1. 页面可以一键运行。
2. 表格清晰展示 Benchmark 信息。
3. 支持报告下载。
4. 支持读取缓存 Demo。
```

---

### 7.8 Cache Manager：缓存模块

#### 功能说明

缓存固定主题的中间结果和最终结果，保证展示稳定。

#### 缓存内容

每个 Demo Case 建议包含：

```text
planner_result.json
raw_report.md
benchmarks.json
ranked_benchmarks.json
final_report.md
```

#### 推荐缓存目录

```text
data/cache/
├── ai_agent_evaluation/
│   ├── planner_result.json
│   ├── raw_report.md
│   ├── benchmarks.json
│   ├── ranked_benchmarks.json
│   └── final_report.md
├── llm_tool_use/
│   └── ...
└── rag_evaluation/
    └── ...
```

#### 要求

```text
1. 展示时默认使用缓存。
2. 用户可以选择重新搜索。
3. 如果 API 失败，自动回退到缓存。
```

---

## 8. 非功能需求

### 8.1 可运行性

项目应支持一键启动：

```bash
streamlit run app.py
```

---

### 8.2 稳定性

至少准备一个完整缓存案例：

```text
AI Agent Evaluation Benchmark + 课程实验模式
```

推荐额外准备：

```text
LLM Tool Use Benchmark + 快速复现模式
RAG Evaluation Benchmark + 科研调研模式
```

---

### 8.3 可解释性

系统所有评分都必须有：

```text
1. 评分维度
2. 分数
3. 推荐理由
```

---

### 8.4 可扩展性

系统应允许未来扩展：

```text
1. 更多推荐模式
2. 更多搜索源
3. 更多 Benchmark 领域
4. 更多评分维度
```

---

### 8.5 成本控制

```text
1. 开发阶段尽量使用缓存。
2. 展示阶段默认读取缓存。
3. 只有用户主动选择时才实时调用 API。
```

---

## 9. MVP 最小可交付版本

如果时间紧，最低版本必须完成：

```text
1. 输入 topic
2. 选择 mode
3. 生成搜索规划 JSON
4. 读取或生成 raw_report
5. 抽取至少 5 个 Benchmark
6. 输出结构化对比表
7. 计算 Task-Fit Score
8. 生成推荐理由
9. 生成 Markdown 报告
10. Streamlit 页面展示结果
```

MVP 主案例：

```text
topic = AI Agent Evaluation Benchmark
mode = 课程实验
```

MVP 至少包含 Benchmark：

```text
AgentBench
WebArena
SWE-bench
GAIA
OSWorld
```

可选 Benchmark：

```text
ToolBench
Mind2Web
MLE-bench
τ-bench
```

---

## 10. 系统架构

### 10.1 整体流程

```text
User Input
  ↓
Query Planner
  ↓
Search Agent / GPT Researcher
  ↓
Benchmark Extractor
  ↓
Task-Fit Scorer
  ↓
LLM Judge
  ↓
Report Writer
  ↓
Streamlit UI
```

---

### 10.2 推荐项目目录

```text
BenchmarkRadarAgent/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── data/
│   ├── cache/
│   │   ├── ai_agent_evaluation/
│   │   ├── llm_tool_use/
│   │   └── rag_evaluation/
│   └── demo_cases/
├── prompts/
│   ├── planner.md
│   ├── extractor.md
│   ├── judge.md
│   └── report_writer.md
├── src/
│   ├── pipeline.py
│   ├── planner.py
│   ├── searcher.py
│   ├── extractor.py
│   ├── scorer.py
│   ├── judge.py
│   ├── reporter.py
│   ├── cache.py
│   └── schemas.py
└── outputs/
    ├── benchmark_table.csv
    └── final_report.md
```

---

## 11. 模块接口设计

### 11.1 主流程接口

```python
def run_benchmark_radar(
    topic: str,
    mode: str,
    use_cache: bool = True
) -> dict:
    """
    输入调研主题和推荐模式，输出完整分析结果。
    """
```

返回：

```json
{
  "topic": "AI Agent Evaluation Benchmark",
  "mode": "课程实验",
  "plan": {},
  "raw_report": "...",
  "benchmarks": [],
  "ranked_benchmarks": [],
  "final_report": "..."
}
```

---

### 11.2 Planner 接口

```python
def plan_queries(topic: str, mode: str) -> dict:
    """
    输入主题和模式，输出搜索规划。
    """
```

---

### 11.3 Searcher 接口

```python
def run_research(topic: str, plan: dict) -> str:
    """
    输入主题和搜索计划，输出原始调研报告。
    """
```

---

### 11.4 Extractor 接口

```python
def extract_benchmarks(raw_report: str, topic: str) -> list[dict]:
    """
    输入原始调研报告，输出 Benchmark 结构化信息。
    """
```

---

### 11.5 Scorer 接口

```python
def score_benchmarks(
    benchmarks: list[dict],
    mode: str
) -> list[dict]:
    """
    根据 mode 计算 Task-Fit Score 并排序。
    """
```

---

### 11.6 Judge 接口

```python
def generate_recommendation_reason(
    benchmark: dict,
    mode: str
) -> str:
    """
    生成当前模式下的推荐理由。
    """
```

---

### 11.7 Reporter 接口

```python
def generate_report(
    topic: str,
    mode: str,
    ranked_benchmarks: list[dict]
) -> str:
    """
    生成 Markdown 调研报告。
    """
```

---

## 12. 加分项对应关系

| 加分项 | 本系统实现方式 |
|---|---|
| 使用大模型通用规划 | Query Planner 自动拆解搜索目标和 query |
| 使用更友好的交互界面 | Streamlit 可视化页面 |
| 使用更高级的评估策略 | Task-Fit Score + LLM Judge |
| 使用微调模型 | 不建议做，可用 Few-shot Prompt 作为替代 |
| 使用强化学习 | 不建议做，可作为未来工作：用户反馈调权 |

---

## 13. 五人技术分工

不包含 PPT 和汇报的情况下，建议如下：

| 成员 | 角色 | 负责模块 | 交付物 |
|---|---|---|---|
| A | Pipeline & Cache 负责人 | 主流程、数据结构、缓存、模块集成 | `pipeline.py`、`cache.py`、`schemas.py` |
| B | Search 负责人 | GPT Researcher / Search API 接入、raw report 生成 | `searcher.py`、`raw_report.md` |
| C | Extractor 负责人 | Benchmark 抽取 Prompt、JSON 解析与校验 | `extractor.py`、`prompts/extractor.md` |
| D | Scorer & Judge 负责人 | Task-Fit Score、模式权重、推荐理由 | `scorer.py`、`judge.py` |
| E | UI & Report 负责人 | Streamlit 页面、报告生成、下载功能 | `app.py`、`reporter.py` |

---

### A：Pipeline & Cache 负责人

任务：

```text
1. 搭建项目目录。
2. 定义统一 Benchmark JSON 字段。
3. 串联 planner/searcher/extractor/scorer/judge/reporter。
4. 实现缓存读取和保存。
5. 保证最终一键运行。
```

交付：

```text
src/pipeline.py
src/cache.py
src/schemas.py
```

---

### B：Search 负责人

任务：

```text
1. 跑通 GPT Researcher 或 Search API。
2. 根据 Planner 生成的 query 搜索资料。
3. 生成 raw_report.md。
4. 准备至少一个完整缓存案例。
```

交付：

```text
src/searcher.py
data/cache/ai_agent_evaluation/raw_report.md
```

---

### C：Extractor 负责人

任务：

```text
1. 编写 Benchmark 抽取 Prompt。
2. 从 raw_report 中抽取结构化 JSON。
3. 处理字段缺失和 JSON 格式错误。
4. 保证至少抽取 5 个 Benchmark。
```

交付：

```text
src/extractor.py
prompts/extractor.md
data/cache/ai_agent_evaluation/benchmarks.json
```

---

### D：Scorer & Judge 负责人

任务：

```text
1. 实现不同 mode 下的 Task-Fit Score。
2. 对 Benchmark 排名。
3. 调用 LLM Judge 生成推荐理由。
4. 输出 ranked_benchmarks.json。
```

交付：

```text
src/scorer.py
src/judge.py
data/cache/ai_agent_evaluation/ranked_benchmarks.json
```

---

### E：UI & Report 负责人

任务：

```text
1. 实现 Streamlit 页面。
2. 展示 topic 输入和 mode 下拉框。
3. 展示 Planner、执行日志、Benchmark 表格和报告。
4. 支持 Markdown 报告下载。
```

交付：

```text
app.py
src/reporter.py
outputs/final_report.md
```

---

## 14. 三天开发计划

### Day 1：完成 MVP 闭环

目标：

```text
输入 topic + mode → 读取/生成 raw_report → 抽取 Benchmark → 计算分数 → 页面展示表格
```

任务：

```text
A：搭项目结构，定义统一接口和缓存格式。
B：跑通搜索，生成 raw_report。
C：完成第一版 Benchmark 抽取。
D：完成第一版 Task-Fit Score。
E：完成 Streamlit 页面骨架。
```

验收：

```text
Day 1 晚上必须展示出一张 Benchmark 对比表。
```

---

### Day 2：完善智能体能力

目标：

```text
Planner + Judge + Report + Cache 全部接入。
```

任务：

```text
A：集成所有模块，加入缓存。
B：优化搜索结果，准备第二个 demo case。
C：完善抽取字段和 JSON 稳定性。
D：加入 LLM Judge 推荐理由。
E：完善页面展示和报告下载。
```

验收：

```text
Day 2 晚上必须能完整演示一次。
```

---

### Day 3：稳定展示版本

目标：

```text
不新增大功能，只修 bug、补缓存、优化展示。
```

任务：

```text
A：保证一键运行。
B：准备稳定缓存数据。
C：检查抽取结果准确性。
D：检查评分合理性。
E：美化页面并导出报告。
```

验收：

```text
Day 3 晚上完成最终可展示版本。
```

---

## 15. 风险与兜底方案

### 风险 1：GPT Researcher 原版集成困难

兜底：

```text
使用 Tavily / DuckDuckGo / arXiv / GitHub Search API 自写轻量 Searcher。
```

---

### 风险 2：Search API 不稳定

兜底：

```text
提前缓存 raw_report、benchmarks、ranked_benchmarks 和 final_report。
```

---

### 风险 3：Extractor 输出 JSON 不稳定

兜底：

```text
使用 JSON mode / pydantic 校验 / 失败重试 / 人工修正缓存。
```

---

### 风险 4：评分被质疑主观

兜底：

```text
展示评分公式、模式权重、维度解释和 LLM Judge 推荐理由。
```

---

### 风险 5：输入过于开放导致效果不稳定

兜底：

```text
展示时重点支持 2-3 个固定 Demo Case。
```

推荐 Demo Case：

```text
AI Agent Evaluation Benchmark + 课程实验
LLM Tool Use Benchmark + 快速复现
RAG Evaluation Benchmark + 科研调研
```

---

## 16. 最终交付清单

```text
1. 可运行代码
2. Streamlit Demo 页面
3. 至少一个完整缓存案例
4. Benchmark 对比表
5. Task-Fit Score 排名
6. 推荐理由
7. Markdown 调研报告
8. README.md
9. .env.example
10. requirements.txt
```

---

## 17. 最终一句话介绍

> BenchmarkRadarAgent 是一个面向 AI Benchmark 调研的智能体系统。它能够根据用户输入的研究方向和使用目标，自动规划搜索任务、检索公开资料、抽取 Benchmark 结构化信息，并通过 Task-Fit Score 对 Benchmark 进行任务适配推荐，最终生成可视化对比表和调研报告。
