# AI Agent Evaluation Benchmark Research Report

## Metadata
- topic: AI Agent Evaluation Benchmark
- mode: ????
- topic_type: agent
- generated_at_utc: 2026-04-30T10:36:43.033010+00:00
- total_search_results: 13
- note: 本报告用于后续 extractor 抽取，不包含最终推荐排名。

## Search Goals
- 梳理 AI Agent Evaluation Benchmark 相关 benchmark 的代表性候选
- 收集每个 benchmark 的论文、代码、数据集和 leaderboard 入口
- 总结各 benchmark 的评测任务、能力维度和关键指标
- 比较资源完整度、文档质量与复现门槛
- 提炼适用于后续结构化抽取的证据链接集合
- 梳理主题相关 benchmark 的代表性候选
- 收集论文、代码、数据集与 leaderboard 入口
- 总结评测任务、能力维度与核心指标

## Search Queries
- AI Agent Evaluation Benchmark benchmark paper GitHub leaderboard
- AI Agent Evaluation Benchmark evaluation benchmark dataset metrics
- AI Agent Evaluation Benchmark benchmark survey comparison
- AI Agent Evaluation Benchmark GitHub open source implementation
- AI Agent Evaluation Benchmark arxiv benchmark 2024 2025
- AI Agent Evaluation Benchmark evaluation benchmark dataset metrics comparison
- AI Agent Evaluation Benchmark benchmark survey open source implementation
- AI Agent Evaluation Benchmark AgentBench WebArena SWE-bench GAIA OSWorld ToolBench

## Search Evidence Snapshot
1. [Sola-Visibility-ISPM: Benchmarking Agentic AI for Identity Security Posture Management Visibility](https://arxiv.org/abs/2601.07880v1) | source: arxiv | query: `AI Agent Evaluation Benchmark benchmark paper GitHub leaderboard`
2. [A Human-Grounded Evaluation Benchmark for Local Explanations of Machine Learning](https://arxiv.org/abs/1801.05075v2) | source: arxiv | query: `AI Agent Evaluation Benchmark benchmark paper GitHub leaderboard`
3. [SECQUE: A Benchmark for Evaluating Real-World Financial Analysis Capabilities](https://arxiv.org/abs/2504.04596v1) | source: arxiv | query: `AI Agent Evaluation Benchmark benchmark paper GitHub leaderboard`
4. [The ML.ENERGY Benchmark: Toward Automated Inference Energy Measurement and Optimization](https://arxiv.org/abs/2505.06371v2) | source: arxiv | query: `AI Agent Evaluation Benchmark benchmark paper GitHub leaderboard`
5. [BEDD: The MineRL BASALT Evaluation and Demonstrations Dataset for Training and Benchmarking Agents that Solve Fuzzy Tasks](https://arxiv.org/abs/2312.02405v1) | source: arxiv | query: `AI Agent Evaluation Benchmark evaluation benchmark dataset metrics`
6. [AI Agents: Evolution, Architecture, and Real-World Applications](https://arxiv.org/abs/2503.12687v1) | source: arxiv | query: `AI Agent Evaluation Benchmark benchmark survey comparison`
7. [Docling: An Efficient Open-Source Toolkit for AI-driven Document Conversion](https://arxiv.org/abs/2501.17887v1) | source: arxiv | query: `AI Agent Evaluation Benchmark GitHub open source implementation`
8. [AI prediction leads people to forgo guaranteed rewards](https://arxiv.org/abs/2603.28944v1) | source: arxiv | query: `AI Agent Evaluation Benchmark GitHub open source implementation`
9. [FormationEval, an open multiple-choice benchmark for petroleum geoscience](https://arxiv.org/abs/2601.02158v2) | source: arxiv | query: `AI Agent Evaluation Benchmark benchmark survey open source implementation`
10. [SWE-bench Goes Live!](https://arxiv.org/abs/2505.23419v2) | source: arxiv | query: `AI Agent Evaluation Benchmark AgentBench WebArena SWE-bench GAIA OSWorld ToolBench`
11. [The Gaia mission](https://arxiv.org/abs/1609.04153v1) | source: arxiv | query: `AI Agent Evaluation Benchmark AgentBench WebArena SWE-bench GAIA OSWorld ToolBench`
12. [Gaia Data Release 3: The Galaxy in your preferred colours. Synthetic photometry from Gaia low-resolution spectra](https://arxiv.org/abs/2206.06215v2) | source: arxiv | query: `AI Agent Evaluation Benchmark AgentBench WebArena SWE-bench GAIA OSWorld ToolBench`
13. [Gaia Data Release 1. Summary of the astrometric, photometric, and survey properties](https://arxiv.org/abs/1609.04172v1) | source: arxiv | query: `AI Agent Evaluation Benchmark AgentBench WebArena SWE-bench GAIA OSWorld ToolBench`

## Benchmark Candidates
### Benchmark 1: SWE-bench
- name: SWE-bench
- source: arXiv + GitHub + leaderboard
- description: SWE-bench benchmark candidate.
- task_type: Software Engineering Agent Evaluation
- evaluated_ability: issue resolution, patch generation
- metrics: resolved issue rate
- paper_url: https://arxiv.org/abs/2310.06770
- code_url: https://github.com/swe-bench/SWE-bench
- dataset_url: 未找到
- leaderboard_url: https://www.swebench.com/
- open_source: true
- resource_completeness_initial: medium
- reproduction_difficulty_initial: medium
- fit_for_course_lab_initial: medium
- fit_for_research_survey_initial: high
- fit_for_quick_reproduction_initial: medium
- evidence_links:
  - https://arxiv.org/abs/2310.06770
  - https://github.com/swe-bench/SWE-bench
  - https://www.swebench.com/
  - https://arxiv.org/abs/2505.23419v2

### Benchmark 2: GAIA
- name: GAIA
- source: arXiv + HF
- description: GAIA benchmark candidate.
- task_type: General Assistant / Agent Evaluation
- evaluated_ability: reasoning, web browsing, tool use
- metrics: accuracy
- paper_url: https://arxiv.org/abs/2311.12983
- code_url: 未找到
- dataset_url: https://huggingface.co/datasets/gaia-benchmark/GAIA
- leaderboard_url: https://huggingface.co/spaces/gaia-benchmark/leaderboard
- open_source: null
- resource_completeness_initial: medium
- reproduction_difficulty_initial: medium
- fit_for_course_lab_initial: medium
- fit_for_research_survey_initial: high
- fit_for_quick_reproduction_initial: medium
- evidence_links:
  - https://arxiv.org/abs/2311.12983
  - https://huggingface.co/datasets/gaia-benchmark/GAIA
  - https://huggingface.co/spaces/gaia-benchmark/leaderboard
  - https://arxiv.org/abs/1609.04153v1
  - https://arxiv.org/abs/2206.06215v2
  - https://arxiv.org/abs/1609.04172v1

### Benchmark 3: AgentBench
- name: AgentBench
- source: arXiv + GitHub
- description: AgentBench benchmark candidate.
- task_type: LLM-as-Agent Evaluation
- evaluated_ability: reasoning, tool interaction
- metrics: task success
- paper_url: https://arxiv.org/abs/2308.03688
- code_url: https://github.com/THUDM/AgentBench
- dataset_url: 未找到
- leaderboard_url: 未找到
- open_source: true
- resource_completeness_initial: medium
- reproduction_difficulty_initial: medium
- fit_for_course_lab_initial: medium
- fit_for_research_survey_initial: high
- fit_for_quick_reproduction_initial: medium
- evidence_links:
  - https://arxiv.org/abs/2308.03688
  - https://github.com/THUDM/AgentBench

### Benchmark 4: WebArena
- name: WebArena
- source: arXiv + GitHub + website
- description: WebArena benchmark candidate.
- task_type: Web Agent Evaluation
- evaluated_ability: web navigation, planning, tool use
- metrics: task success rate
- paper_url: https://arxiv.org/abs/2307.13854
- code_url: https://github.com/web-arena-x/webarena
- dataset_url: 未找到
- leaderboard_url: https://webarena.dev/
- open_source: true
- resource_completeness_initial: medium
- reproduction_difficulty_initial: medium
- fit_for_course_lab_initial: medium
- fit_for_research_survey_initial: high
- fit_for_quick_reproduction_initial: medium
- evidence_links:
  - https://arxiv.org/abs/2307.13854
  - https://github.com/web-arena-x/webarena
  - https://webarena.dev/

### Benchmark 5: OSWorld
- name: OSWorld
- source: arXiv + GitHub + website
- description: OSWorld benchmark candidate.
- task_type: Computer-use Agent Evaluation
- evaluated_ability: GUI operation, desktop task solving
- metrics: task success rate
- paper_url: https://arxiv.org/abs/2404.07972
- code_url: https://github.com/xlang-ai/OSWorld
- dataset_url: 未找到
- leaderboard_url: https://os-world.github.io/
- open_source: true
- resource_completeness_initial: medium
- reproduction_difficulty_initial: medium
- fit_for_course_lab_initial: medium
- fit_for_research_survey_initial: high
- fit_for_quick_reproduction_initial: medium
- evidence_links:
  - https://arxiv.org/abs/2404.07972
  - https://github.com/xlang-ai/OSWorld
  - https://os-world.github.io/

### Benchmark 6: ToolBench
- name: ToolBench
- source: GitHub
- description: ToolBench benchmark candidate.
- task_type: Tool-use Agent Evaluation
- evaluated_ability: API selection, tool use
- metrics: pass rate
- paper_url: 未找到
- code_url: https://github.com/OpenBMB/ToolBench
- dataset_url: 未找到
- leaderboard_url: 未找到
- open_source: true
- resource_completeness_initial: medium
- reproduction_difficulty_initial: medium
- fit_for_course_lab_initial: medium
- fit_for_research_survey_initial: high
- fit_for_quick_reproduction_initial: medium
- evidence_links:
  - https://github.com/OpenBMB/ToolBench

## Notes
- Searcher 仅提供事实型调研信息，不输出最终推荐排序。
- 缺失链接已标注为‘未找到’或 null，未编造 URL。
