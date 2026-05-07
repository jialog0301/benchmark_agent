# BenchmarkRadarAgent

AI Benchmark 自动调研、结构化对比与任务适配推荐智能体。

## 项目简介

输入一个 AI 研究方向（如 "AI Agent Evaluation Benchmark"），系统自动完成：

```
任务规划 → 资料检索 → Benchmark 信息抽取 → Task-Fit Score 评分 → 推荐报告生成
```

系统帮助用户快速了解、比较和选择 Benchmark，而非复现 Benchmark 的平台。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，至少配置以下之一：
#   MINIMAX_API_KEY / MINIMAX_BASE_URL （MiniMax API）
#   ANTHROPIC_API_KEY                    （Anthropic 官方 API）
#   OPENAI_BASE_URL                      （Ollama 等本地模型）
# 可选：TAVILY_API_KEY（搜索增强）、GITHUB_TOKEN（GitHub 元数据）

# 启动 Streamlit 界面
streamlit run app.py

# 命令行指定主题和模式
streamlit run app.py -- --topic "AI Agent Evaluation Benchmark" --mode "课程实验"
```

## 推荐模式

| 模式 | 说明 | 评分侧重 |
|------|------|----------|
| 课程实验 | 适合课堂教学和学生实验 | 教学价值、资源完整度、复现友好度 |
| 科研调研 | 适合论文 related work 和系统性对比 | 科研价值、权威性、方向热度 |
| 快速复现 | 适合快速跑通 Demo 验证可行性 | 复现友好度、资源完整度、文档质量 |

## 项目结构

```
benchmark_agent/
├── app.py                  # Streamlit 前端入口
├── src/
│   ├── pipeline.py         # 主流水线编排
│   ├── planner.py          # 查询规划（LLM + 模板兜底）
│   ├── searcher.py         # 多源搜索（Tavily/DDG/arXiv/GitHub）+ 精选库兜底
│   ├── extractor.py        # Benchmark 结构化抽取（LLM JSON 提取）
│   ├── scorer.py           # Task-Fit Score 计算（纯 Python，无 LLM 依赖）
│   ├── judge.py            # 推荐理由生成（LLM）
│   ├── reporter.py         # Markdown 报告 + CSV 导出
│   ├── llm_client.py       # 统一 LLM 调用（MiniMax → Anthropic → OpenAI 降级链）
│   ├── cache.py            # 缓存管理（data/cache/<topic>/）
│   └── schemas.py          # Pydantic 数据模型
├── prompts/                # 各模块的 LLM prompt 模板
│   ├── planner.md
│   ├── searcher.md
│   ├── extractor.md
│   ├── judge.md
│   └── report_writer.md
├── data/cache/             # 缓存目录（按主题分文件夹）
├── outputs/                # 最终报告输出（.md + .csv）
└── docs/                   # 需求文档与模块交接说明
```

## 评分公式

**课程实验：**
```
0.30 × 教学价值 + 0.25 × 资源完整度 + 0.20 × 复现友好度 + 0.15 × 方向热度 + 0.10 × 时间成本友好度
```

**科研调研：**
```
0.30 × 科研价值 + 0.25 × 权威性 + 0.20 × 方向热度 + 0.15 × 资源完整度 + 0.10 × 覆盖度
```

**快速复现：**
```
0.35 × 复现友好度 + 0.25 × 资源完整度 + 0.20 × 文档质量 + 0.15 × 时间成本友好度 + 0.05 × 方向热度
```

> 复现友好度 = 6 − 复现难度评分；所有维度评分区间 [1, 5]。

## 核心设计

- **多层兜底机制**：每个调用 LLM 或外部 API 的模块都有确定性兜底逻辑，外部服务不可用时系统仍可完整运行
- **缓存优先**：Pipeline 每步先查缓存，命中则跳过 LLM/API 调用；Demo 模式默认使用缓存
- **主题感知**：Searcher 自动识别主题类型（Agent/RAG/Code/通用），匹配对应的精选 Benchmark 池
- **多源搜索**：Tavily（优先）→ DuckDuckGo（免费），并行调用 arXiv API 和 GitHub Search API
- **纯 Python 评分**：Scorer 不依赖 LLM，结果可复现、可预测

## 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `MINIMAX_API_KEY` | MiniMax API 密钥 | 至少配置一个 LLM |
| `MINIMAX_BASE_URL` | MiniMax 接口地址 | 默认 `https://api.minimax.chat/v1` |
| `MINIMAX_MODEL` | 模型名称 | 默认 `MiniMax-M2.7` |
| `ANTHROPIC_API_KEY` | Anthropic 官方 API 密钥 | 可选 |
| `OPENAI_BASE_URL` | OpenAI 兼容接口地址 | 默认 `http://localhost:11434/v1` |
| `TAVILY_API_KEY` | Tavily 搜索 API 密钥 | 可选（增强搜索） |
| `GITHUB_TOKEN` | GitHub Personal Access Token | 可选（获取仓库元数据） |
