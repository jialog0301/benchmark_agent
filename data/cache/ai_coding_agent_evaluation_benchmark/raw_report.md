# AI coding Agent Evaluation Benchmark Research Report

## Metadata
- topic: AI coding Agent Evaluation Benchmark
- mode: 科研调研
- topic_type: code
- generated_at_utc: 2026-05-07T07:41:43.700414+00:00
- total_search_results: 60
- note: 本报告用于后续 extractor 抽取，不包含最终推荐排名。

## Search Goals
- 了解AI编程代理评估基准的学术研究现状与趋势
- 收集主流基准的论文、作者及其引用信息
- 分析各基准的评测指标、任务覆盖范围与数据集规模
- 获取相关基准的开源代码、GitHub仓库与数据集链接
- 对比基准在学术界与工业界的排名、影响力与复现性

## Search Queries
- AI coding agent evaluation benchmark survey paper
- code generation agent benchmark dataset leaderboard
- metrics for evaluating AI programming agent performance reproducibility
- GitHub repository of AI coding agent evaluation framework
- comparison of AI coding agent benchmarks coverage analysis
- state-of-the-art AI software engineering agent evaluation leaderboard
- reproducibility study of autonomous coding agent benchmarks
- AI coding Agent Evaluation Benchmark SWE-bench Verified HumanEval MBPP BigCodeBench RepoBench APPS

## Search Evidence Snapshot
1. [Evaluation and Benchmarking of LLM Agents: A Survey](https://dl.acm.org/doi/pdf/10.1145/3711896.3736570) | source: tavily | query: `AI coding agent evaluation benchmark survey paper`
2. [ProjDevBench: Benchmarking AI Coding Agents on End-to ... - arXiv](https://arxiv.org/abs/2602.01655) | source: tavily | query: `AI coding agent evaluation benchmark survey paper`
3. [Benchmarking AI Coding Agents on End-to-End Project Development](https://arxiv.org/html/2602.01655v1) | source: tavily | query: `AI coding agent evaluation benchmark survey paper`
4. [A Systematic Survey of AI Agent Evaluation Methods and Metrics](https://www.researchgate.net/publication/400639175_A_Systematic_Survey_of_AI_Agent_Evaluation_Methods_and_Metrics) | source: tavily | query: `AI coding agent evaluation benchmark survey paper`
5. [A 360 review of AI agent benchmarks - IBM Research](https://research.ibm.com/blog/AI-agent-benchmarks) | source: tavily | query: `AI coding agent evaluation benchmark survey paper`
6. [Sola-Visibility-ISPM: Benchmarking Agentic AI for Identity Security Posture Management Visibility](https://arxiv.org/abs/2601.07880v1) | source: arxiv | query: `AI coding agent evaluation benchmark survey paper`
7. [This paper has been withdrawn](https://arxiv.org/abs/cond-mat/0309395v2) | source: arxiv | query: `AI coding agent evaluation benchmark survey paper`
8. [AI Agents: Evolution, Architecture, and Real-World Applications](https://arxiv.org/abs/2503.12687v1) | source: arxiv | query: `AI coding agent evaluation benchmark survey paper`
9. [Foundations of GenIR](https://arxiv.org/abs/2501.02842v1) | source: arxiv | query: `AI coding agent evaluation benchmark survey paper`
10. [Big Code Models Leaderboard - a Hugging Face Space by bigcode](https://huggingface.co/spaces/bigcode/bigcode-models-leaderboard) | source: tavily | query: `code generation agent benchmark dataset leaderboard`
11. [DA-Code: Agent Data Science Code Generation Benchmark for Large Language Models](https://da-code-bench.github.io/) | source: tavily | query: `code generation agent benchmark dataset leaderboard`
12. [Code Generation Benchmarks 2026: SOTA LLMs ...](https://www.codesota.com/code-generation) | source: tavily | query: `code generation agent benchmark dataset leaderboard`
13. [SWE-bench Leaderboards](https://www.swebench.com/) | source: tavily | query: `code generation agent benchmark dataset leaderboard`
14. [LiveBench](https://livebench.ai/) | source: tavily | query: `code generation agent benchmark dataset leaderboard`
15. [The RSNA Abdominal Traumatic Injury CT (RATIC) Dataset](https://arxiv.org/abs/2405.19595v1) | source: arxiv | query: `code generation agent benchmark dataset leaderboard`
16. [JaCoText: A Pretrained Model for Java Code-Text Generation](https://arxiv.org/abs/2303.12869v1) | source: arxiv | query: `code generation agent benchmark dataset leaderboard`
17. [On the Workflows and Smells of Leaderboard Operations (LBOps): An Exploratory Study of Foundation Model Leaderboards](https://arxiv.org/abs/2407.04065v4) | source: arxiv | query: `code generation agent benchmark dataset leaderboard`
18. [BEDD: The MineRL BASALT Evaluation and Demonstrations Dataset for Training and Benchmarking Agents that Solve Fuzzy Tasks](https://arxiv.org/abs/2312.02405v1) | source: arxiv | query: `code generation agent benchmark dataset leaderboard`
19. [Mastering Agents:  Metrics for Evaluating AI Agents](https://galileo.ai/blog/metrics-for-evaluating-ai-agents) | source: tavily | query: `metrics for evaluating AI programming agent performance reproducibility`
20. [AI agent evaluation: Metrics, strategies, and best practices - Medium](https://medium.com/online-inference/ai-agent-evaluation-metrics-strategies-and-best-practices-8a00a5b17377) | source: tavily | query: `metrics for evaluating AI programming agent performance reproducibility`

## Benchmark Candidates
### Benchmark 1: SWE-bench
name: SWE-bench
description: SWE-bench benchmark candidate.
task_type: Software Engineering Agent Benchmark
evaluated_ability:
  - issue resolution
  - repo navigation
  - patch generation
metrics:
  - resolved issue rate
paper_url: https://arxiv.org/abs/2310.06770
code_url: https://github.com/swe-bench/SWE-bench
dataset_url: null
leaderboard_url: https://www.swebench.com/
project_url: https://www.swebench.com/
open_source: true
resource_evidence:
  paper_available: true
  code_available: true
  dataset_available: false
  leaderboard_available: true
  official_site_available: true
  install_instructions_available: true
  quick_walkthrough_available: true
  docker_or_environment_files_available: true
  evidence_notes: Resource completeness score=5; evidence links include paper/code/dataset/leaderboard/readme where available.
reproduction_evidence:
  setup_requirements:
    - Python environment
    - Repository checkout
    - Evaluation harness configuration
  requires_gpu: true
  requires_api_key: depends_on_agent_model
  estimated_setup_cost: high
  reproduction_notes: Reproduction difficulty=4 (higher is harder). Complexity inferred from task type and setup dependencies.
teaching_evidence:
  task_clarity: high
  example_tasks_available: true
  classroom_demo_value: high
  student_friendliness: medium
  teaching_notes: Teaching value=4; time friendliness=3. README/examples availability used as proxy evidence.
research_evidence:
  representative_benchmark: true
  realistic_environment: true
  leaderboard_available: true
  baseline_results_available: true
  research_notes: Research value=5; authority=5. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: ok
  github_api_error_message: none
  github_stars: 4856
  github_forks: 852
  leaderboard_or_project_available: true
  recent_repository_activity: true
  last_push_utc: 2026-04-01T05:16:30Z
  related_benchmarks_or_extensions:
    - SWE-bench Verified
    - Agentless
  popularity_notes: Topic popularity score=5; stars=4856, forks=852, recent_activity=true.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: true
  full_evaluation_cost: high
  estimated_demo_time: 1-2_days
  estimated_full_reproduction_time: multiple_days
  time_cost_notes: Time friendliness=3; reproduction difficulty=4.
documentation_evidence:
  readme_quality: high
  installation_steps_available: true
  examples_available: true
  evaluation_instructions_available: likely
  documentation_notes: Documentation quality score=4; README and project docs links are used as evidence.
authority_evidence:
  paper_available: true
  official_project_site: true
  official_github_repository: true
  leaderboard_available: true
  authority_notes: Authority score=5; based on availability of paper/repo/project/leaderboard.
resource_completeness: 5
reproduction_difficulty: 4
teaching_value: 4
research_value: 5
topic_popularity: 5
time_cost_friendliness: 3
documentation_quality: 4
authority: 5
suggested_scores_for_extractor:
  resource_completeness: 5
  reproduction_difficulty: 4
  teaching_value: 4
  research_value: 5
  topic_popularity: 5
  time_cost_friendliness: 3
  documentation_quality: 4
  authority: 5
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2310.06770
  - https://github.com/swe-bench/SWE-bench
  - https://www.swebench.com/
  - https://github.com/swe-bench/SWE-bench#readme
  - https://www.codesota.com/code-generation
  - https://live-swe-agent.github.io/
  - https://labs.scale.com/leaderboard/swe_bench_pro_public
  - https://www.swebench.com/verified.html
  - https://epoch.ai/benchmarks/swe-bench-verified
  - https://www.reddit.com/r/GithubCopilot/comments/1odgwbp/a_more_accurate_benchmark_for_coding_agents/

### Benchmark 2: SWE-bench Verified
name: SWE-bench Verified
description: SWE-bench Verified benchmark candidate.
task_type: Software Engineering Agent Benchmark
evaluated_ability:
  - issue resolution on verified split
metrics:
  - resolved issue rate
paper_url: https://www.swebench.com/verified.html
code_url: https://github.com/swe-bench/SWE-bench
dataset_url: null
leaderboard_url: https://www.swebench.com/verified.html
project_url: https://www.swebench.com/verified.html
open_source: true
resource_evidence:
  paper_available: true
  code_available: true
  dataset_available: false
  leaderboard_available: true
  official_site_available: true
  install_instructions_available: true
  quick_walkthrough_available: true
  docker_or_environment_files_available: true
  evidence_notes: Resource completeness score=4; evidence links include paper/code/dataset/leaderboard/readme where available.
reproduction_evidence:
  setup_requirements:
    - Python environment
    - Repository checkout
    - Evaluation harness configuration
  requires_gpu: true
  requires_api_key: depends_on_agent_model
  estimated_setup_cost: high
  reproduction_notes: Reproduction difficulty=4 (higher is harder). Complexity inferred from task type and setup dependencies.
teaching_evidence:
  task_clarity: high
  example_tasks_available: true
  classroom_demo_value: high
  student_friendliness: medium
  teaching_notes: Teaching value=4; time friendliness=3. README/examples availability used as proxy evidence.
research_evidence:
  representative_benchmark: true
  realistic_environment: true
  leaderboard_available: true
  baseline_results_available: true
  research_notes: Research value=5; authority=5. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: ok
  github_api_error_message: none
  github_stars: 4856
  github_forks: 852
  leaderboard_or_project_available: true
  recent_repository_activity: true
  last_push_utc: 2026-04-01T05:16:30Z
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=4; stars=4856, forks=852, recent_activity=true.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: true
  full_evaluation_cost: high
  estimated_demo_time: 1-2_days
  estimated_full_reproduction_time: multiple_days
  time_cost_notes: Time friendliness=3; reproduction difficulty=4.
documentation_evidence:
  readme_quality: high
  installation_steps_available: true
  examples_available: true
  evaluation_instructions_available: likely
  documentation_notes: Documentation quality score=4; README and project docs links are used as evidence.
authority_evidence:
  paper_available: true
  official_project_site: true
  official_github_repository: true
  leaderboard_available: true
  authority_notes: Authority score=5; based on availability of paper/repo/project/leaderboard.
resource_completeness: 4
reproduction_difficulty: 4
teaching_value: 4
research_value: 5
topic_popularity: 4
time_cost_friendliness: 3
documentation_quality: 4
authority: 5
suggested_scores_for_extractor:
  resource_completeness: 4
  reproduction_difficulty: 4
  teaching_value: 4
  research_value: 5
  topic_popularity: 4
  time_cost_friendliness: 3
  documentation_quality: 4
  authority: 5
limitations: null
suitable_usage: null
evidence:
  - https://www.swebench.com/verified.html
  - https://github.com/swe-bench/SWE-bench
  - https://github.com/swe-bench/SWE-bench#readme

### Benchmark 3: HumanEval
name: HumanEval
description: HumanEval benchmark candidate.
task_type: Code Generation Benchmark
evaluated_ability:
  - function synthesis
  - algorithmic coding
metrics:
  - pass@1
  - pass@k
paper_url: https://arxiv.org/abs/2107.03374
code_url: https://github.com/openai/human-eval
dataset_url: null
leaderboard_url: null
project_url: https://github.com/openai/human-eval
open_source: true
resource_evidence:
  paper_available: true
  code_available: true
  dataset_available: false
  leaderboard_available: false
  official_site_available: true
  install_instructions_available: true
  quick_walkthrough_available: true
  docker_or_environment_files_available: unknown
  evidence_notes: Resource completeness score=4; evidence links include paper/code/dataset/leaderboard/readme where available.
reproduction_evidence:
  setup_requirements:
    - Python environment
    - Repository checkout
    - Evaluation harness configuration
  requires_gpu: false
  requires_api_key: optional
  estimated_setup_cost: low
  reproduction_notes: Reproduction difficulty=2 (higher is harder). Complexity inferred from task type and setup dependencies.
teaching_evidence:
  task_clarity: high
  example_tasks_available: true
  classroom_demo_value: high
  student_friendliness: high
  teaching_notes: Teaching value=5; time friendliness=5. README/examples availability used as proxy evidence.
research_evidence:
  representative_benchmark: true
  realistic_environment: partial
  leaderboard_available: false
  baseline_results_available: true
  research_notes: Research value=4; authority=5. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: ok
  github_api_error_message: none
  github_stars: 3224
  github_forks: 445
  leaderboard_or_project_available: true
  recent_repository_activity: false
  last_push_utc: 2025-01-17T18:22:17Z
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=5; stars=3224, forks=445, recent_activity=false.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: true
  full_evaluation_cost: low
  estimated_demo_time: hours_to_1_day
  estimated_full_reproduction_time: hours_to_1_day
  time_cost_notes: Time friendliness=5; reproduction difficulty=2.
documentation_evidence:
  readme_quality: high
  installation_steps_available: true
  examples_available: true
  evaluation_instructions_available: likely
  documentation_notes: Documentation quality score=4; README and project docs links are used as evidence.
authority_evidence:
  paper_available: true
  official_project_site: true
  official_github_repository: true
  leaderboard_available: false
  authority_notes: Authority score=5; based on availability of paper/repo/project/leaderboard.
resource_completeness: 4
reproduction_difficulty: 2
teaching_value: 5
research_value: 4
topic_popularity: 5
time_cost_friendliness: 5
documentation_quality: 4
authority: 5
suggested_scores_for_extractor:
  resource_completeness: 4
  reproduction_difficulty: 2
  teaching_value: 5
  research_value: 4
  topic_popularity: 5
  time_cost_friendliness: 5
  documentation_quality: 4
  authority: 5
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2107.03374
  - https://github.com/openai/human-eval
  - https://github.com/openai/human-eval#readme

### Benchmark 4: MBPP
name: MBPP
description: MBPP benchmark candidate.
task_type: Code Generation Benchmark
evaluated_ability:
  - python problem solving
metrics:
  - pass@k
  - accuracy
paper_url: https://arxiv.org/abs/2108.07732
code_url: https://github.com/google-research/google-research/blob/master/mbpp/README.md
dataset_url: https://github.com/google-research/google-research/tree/master/mbpp
leaderboard_url: null
project_url: https://github.com/google-research/google-research/tree/master/mbpp
open_source: true
resource_evidence:
  paper_available: true
  code_available: true
  dataset_available: true
  leaderboard_available: false
  official_site_available: true
  install_instructions_available: true
  quick_walkthrough_available: true
  docker_or_environment_files_available: unknown
  evidence_notes: Resource completeness score=4; evidence links include paper/code/dataset/leaderboard/readme where available.
reproduction_evidence:
  setup_requirements:
    - Python environment
    - Repository checkout
    - Evaluation harness configuration
  requires_gpu: false
  requires_api_key: optional
  estimated_setup_cost: low
  reproduction_notes: Reproduction difficulty=2 (higher is harder). Complexity inferred from task type and setup dependencies.
teaching_evidence:
  task_clarity: high
  example_tasks_available: true
  classroom_demo_value: high
  student_friendliness: high
  teaching_notes: Teaching value=5; time friendliness=5. README/examples availability used as proxy evidence.
research_evidence:
  representative_benchmark: likely
  realistic_environment: partial
  leaderboard_available: false
  baseline_results_available: true
  research_notes: Research value=3; authority=4. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: ok
  github_api_error_message: none
  github_stars: 37850
  github_forks: 8405
  leaderboard_or_project_available: true
  recent_repository_activity: true
  last_push_utc: 2026-05-06T12:13:49Z
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=4; stars=37850, forks=8405, recent_activity=true.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: true
  full_evaluation_cost: low
  estimated_demo_time: hours_to_1_day
  estimated_full_reproduction_time: hours_to_1_day
  time_cost_notes: Time friendliness=5; reproduction difficulty=2.
documentation_evidence:
  readme_quality: high
  installation_steps_available: true
  examples_available: true
  evaluation_instructions_available: likely
  documentation_notes: Documentation quality score=4; README and project docs links are used as evidence.
authority_evidence:
  paper_available: true
  official_project_site: true
  official_github_repository: true
  leaderboard_available: false
  authority_notes: Authority score=4; based on availability of paper/repo/project/leaderboard.
resource_completeness: 4
reproduction_difficulty: 2
teaching_value: 5
research_value: 3
topic_popularity: 4
time_cost_friendliness: 5
documentation_quality: 4
authority: 4
suggested_scores_for_extractor:
  resource_completeness: 4
  reproduction_difficulty: 2
  teaching_value: 5
  research_value: 3
  topic_popularity: 4
  time_cost_friendliness: 5
  documentation_quality: 4
  authority: 4
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2108.07732
  - https://github.com/google-research/google-research/tree/master/mbpp
  - https://github.com/google-research/google-research/blob/master/mbpp/README.md
  - https://github.com/google-research/google-research/blob/master/mbpp/README.md#readme

### Benchmark 5: BigCodeBench
name: BigCodeBench
description: BigCodeBench benchmark candidate.
task_type: Code Generation Benchmark
evaluated_ability:
  - complex coding task solving
metrics:
  - pass@1
  - task success
paper_url: https://arxiv.org/abs/2406.15877
code_url: https://github.com/bigcode-project/bigcodebench
dataset_url: null
leaderboard_url: https://bigcode-bench.github.io/
project_url: https://bigcode-bench.github.io/
open_source: true
resource_evidence:
  paper_available: true
  code_available: true
  dataset_available: false
  leaderboard_available: true
  official_site_available: true
  install_instructions_available: true
  quick_walkthrough_available: true
  docker_or_environment_files_available: true
  evidence_notes: Resource completeness score=4; evidence links include paper/code/dataset/leaderboard/readme where available.
reproduction_evidence:
  setup_requirements:
    - Python environment
    - Repository checkout
    - Evaluation harness configuration
  requires_gpu: true
  requires_api_key: optional
  estimated_setup_cost: high
  reproduction_notes: Reproduction difficulty=4 (higher is harder). Complexity inferred from task type and setup dependencies.
teaching_evidence:
  task_clarity: high
  example_tasks_available: true
  classroom_demo_value: high
  student_friendliness: medium
  teaching_notes: Teaching value=4; time friendliness=3. README/examples availability used as proxy evidence.
research_evidence:
  representative_benchmark: true
  realistic_environment: partial
  leaderboard_available: true
  baseline_results_available: true
  research_notes: Research value=5; authority=4. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: ok
  github_api_error_message: none
  github_stars: 498
  github_forks: 72
  leaderboard_or_project_available: true
  recent_repository_activity: true
  last_push_utc: 2026-01-03T07:22:42Z
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=4; stars=498, forks=72, recent_activity=true.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: true
  full_evaluation_cost: high
  estimated_demo_time: 1-2_days
  estimated_full_reproduction_time: multiple_days
  time_cost_notes: Time friendliness=3; reproduction difficulty=4.
documentation_evidence:
  readme_quality: medium
  installation_steps_available: true
  examples_available: true
  evaluation_instructions_available: likely
  documentation_notes: Documentation quality score=3; README and project docs links are used as evidence.
authority_evidence:
  paper_available: true
  official_project_site: true
  official_github_repository: true
  leaderboard_available: true
  authority_notes: Authority score=4; based on availability of paper/repo/project/leaderboard.
resource_completeness: 4
reproduction_difficulty: 4
teaching_value: 4
research_value: 5
topic_popularity: 4
time_cost_friendliness: 3
documentation_quality: 3
authority: 4
suggested_scores_for_extractor:
  resource_completeness: 4
  reproduction_difficulty: 4
  teaching_value: 4
  research_value: 5
  topic_popularity: 4
  time_cost_friendliness: 3
  documentation_quality: 3
  authority: 4
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2406.15877
  - https://github.com/bigcode-project/bigcodebench
  - https://bigcode-bench.github.io/
  - https://github.com/bigcode-project/bigcodebench#readme

### Benchmark 6: RepoBench
name: RepoBench
description: RepoBench benchmark candidate.
task_type: Repository-level Code Benchmark
evaluated_ability:
  - cross-file retrieval
  - repo-level completion
metrics:
  - task completion metrics
paper_url: https://arxiv.org/abs/2306.03091
code_url: https://github.com/Leolty/repobench
dataset_url: null
leaderboard_url: null
project_url: https://github.com/Leolty/repobench
open_source: true
resource_evidence:
  paper_available: true
  code_available: true
  dataset_available: false
  leaderboard_available: false
  official_site_available: true
  install_instructions_available: true
  quick_walkthrough_available: true
  docker_or_environment_files_available: true
  evidence_notes: Resource completeness score=4; evidence links include paper/code/dataset/leaderboard/readme where available.
reproduction_evidence:
  setup_requirements:
    - Python environment
    - Repository checkout
    - Evaluation harness configuration
  requires_gpu: true
  requires_api_key: optional
  estimated_setup_cost: high
  reproduction_notes: Reproduction difficulty=4 (higher is harder). Complexity inferred from task type and setup dependencies.
teaching_evidence:
  task_clarity: high
  example_tasks_available: true
  classroom_demo_value: high
  student_friendliness: medium
  teaching_notes: Teaching value=4; time friendliness=3. README/examples availability used as proxy evidence.
research_evidence:
  representative_benchmark: true
  realistic_environment: partial
  leaderboard_available: false
  baseline_results_available: true
  research_notes: Research value=4; authority=4. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: ok
  github_api_error_message: none
  github_stars: 204
  github_forks: 12
  leaderboard_or_project_available: true
  recent_repository_activity: false
  last_push_utc: 2024-08-16T07:08:32Z
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=3; stars=204, forks=12, recent_activity=false.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: true
  full_evaluation_cost: high
  estimated_demo_time: 1-2_days
  estimated_full_reproduction_time: multiple_days
  time_cost_notes: Time friendliness=3; reproduction difficulty=4.
documentation_evidence:
  readme_quality: medium
  installation_steps_available: true
  examples_available: true
  evaluation_instructions_available: likely
  documentation_notes: Documentation quality score=3; README and project docs links are used as evidence.
authority_evidence:
  paper_available: true
  official_project_site: true
  official_github_repository: true
  leaderboard_available: false
  authority_notes: Authority score=4; based on availability of paper/repo/project/leaderboard.
resource_completeness: 4
reproduction_difficulty: 4
teaching_value: 4
research_value: 4
topic_popularity: 3
time_cost_friendliness: 3
documentation_quality: 3
authority: 4
suggested_scores_for_extractor:
  resource_completeness: 4
  reproduction_difficulty: 4
  teaching_value: 4
  research_value: 4
  topic_popularity: 3
  time_cost_friendliness: 3
  documentation_quality: 3
  authority: 4
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2306.03091
  - https://github.com/Leolty/repobench
  - https://github.com/Leolty/repobench#readme

### Benchmark 7: Agentless
name: Agentless
description: Agentless benchmark candidate.
task_type: Software Engineering Agent Evaluation Reference
evaluated_ability:
  - localization
  - repair
  - patch validation
metrics:
  - resolved issue rate
  - cost efficiency
paper_url: https://arxiv.org/abs/2407.01489
code_url: https://github.com/OpenAutoCoder/Agentless
dataset_url: null
leaderboard_url: null
project_url: https://github.com/OpenAutoCoder/Agentless
open_source: true
resource_evidence:
  paper_available: true
  code_available: true
  dataset_available: false
  leaderboard_available: false
  official_site_available: true
  install_instructions_available: true
  quick_walkthrough_available: true
  docker_or_environment_files_available: unknown
  evidence_notes: Resource completeness score=3; evidence links include paper/code/dataset/leaderboard/readme where available.
reproduction_evidence:
  setup_requirements:
    - Python environment
    - Repository checkout
    - Evaluation harness configuration
  requires_gpu: false
  requires_api_key: depends_on_agent_model
  estimated_setup_cost: medium
  reproduction_notes: Reproduction difficulty=3 (higher is harder). Complexity inferred from task type and setup dependencies.
teaching_evidence:
  task_clarity: high
  example_tasks_available: true
  classroom_demo_value: high
  student_friendliness: high
  teaching_notes: Teaching value=4; time friendliness=4. README/examples availability used as proxy evidence.
research_evidence:
  representative_benchmark: true
  realistic_environment: true
  leaderboard_available: false
  baseline_results_available: true
  research_notes: Research value=4; authority=4. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: ok
  github_api_error_message: none
  github_stars: 2042
  github_forks: 230
  leaderboard_or_project_available: true
  recent_repository_activity: false
  last_push_utc: 2024-12-22T19:29:31Z
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=3; stars=2042, forks=230, recent_activity=false.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: true
  full_evaluation_cost: medium
  estimated_demo_time: hours_to_1_day
  estimated_full_reproduction_time: 1-2_days
  time_cost_notes: Time friendliness=4; reproduction difficulty=3.
documentation_evidence:
  readme_quality: medium
  installation_steps_available: true
  examples_available: true
  evaluation_instructions_available: likely
  documentation_notes: Documentation quality score=3; README and project docs links are used as evidence.
authority_evidence:
  paper_available: true
  official_project_site: true
  official_github_repository: true
  leaderboard_available: false
  authority_notes: Authority score=4; based on availability of paper/repo/project/leaderboard.
resource_completeness: 3
reproduction_difficulty: 3
teaching_value: 4
research_value: 4
topic_popularity: 3
time_cost_friendliness: 4
documentation_quality: 3
authority: 4
suggested_scores_for_extractor:
  resource_completeness: 3
  reproduction_difficulty: 3
  teaching_value: 4
  research_value: 4
  topic_popularity: 3
  time_cost_friendliness: 4
  documentation_quality: 3
  authority: 4
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2407.01489
  - https://github.com/OpenAutoCoder/Agentless
  - https://github.com/OpenAutoCoder/Agentless#readme

### Benchmark 8: APPS
name: APPS
description: APPS benchmark candidate.
task_type: Code Generation Benchmark
evaluated_ability:
  - program synthesis
  - multi-step reasoning
  - execution correctness
metrics:
  - pass rate
  - test case accuracy
paper_url: https://arxiv.org/abs/2105.09938
code_url: https://github.com/hendrycks/apps
dataset_url: null
leaderboard_url: null
project_url: https://github.com/hendrycks/apps
open_source: true
resource_evidence:
  paper_available: true
  code_available: true
  dataset_available: false
  leaderboard_available: false
  official_site_available: true
  install_instructions_available: true
  quick_walkthrough_available: true
  docker_or_environment_files_available: unknown
  evidence_notes: Resource completeness score=4; evidence links include paper/code/dataset/leaderboard/readme where available.
reproduction_evidence:
  setup_requirements:
    - Python environment
    - Repository checkout
    - Evaluation harness configuration
  requires_gpu: false
  requires_api_key: optional
  estimated_setup_cost: medium
  reproduction_notes: Reproduction difficulty=3 (higher is harder). Complexity inferred from task type and setup dependencies.
teaching_evidence:
  task_clarity: high
  example_tasks_available: true
  classroom_demo_value: high
  student_friendliness: high
  teaching_notes: Teaching value=4; time friendliness=4. README/examples availability used as proxy evidence.
research_evidence:
  representative_benchmark: true
  realistic_environment: partial
  leaderboard_available: false
  baseline_results_available: true
  research_notes: Research value=4; authority=4. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: ok
  github_api_error_message: none
  github_stars: 526
  github_forks: 70
  leaderboard_or_project_available: true
  recent_repository_activity: false
  last_push_utc: 2024-06-19T06:32:49Z
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=4; stars=526, forks=70, recent_activity=false.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: true
  full_evaluation_cost: medium
  estimated_demo_time: hours_to_1_day
  estimated_full_reproduction_time: 1-2_days
  time_cost_notes: Time friendliness=4; reproduction difficulty=3.
documentation_evidence:
  readme_quality: high
  installation_steps_available: true
  examples_available: true
  evaluation_instructions_available: likely
  documentation_notes: Documentation quality score=4; README and project docs links are used as evidence.
authority_evidence:
  paper_available: true
  official_project_site: true
  official_github_repository: true
  leaderboard_available: false
  authority_notes: Authority score=4; based on availability of paper/repo/project/leaderboard.
resource_completeness: 4
reproduction_difficulty: 3
teaching_value: 4
research_value: 4
topic_popularity: 4
time_cost_friendliness: 4
documentation_quality: 4
authority: 4
suggested_scores_for_extractor:
  resource_completeness: 4
  reproduction_difficulty: 3
  teaching_value: 4
  research_value: 4
  topic_popularity: 4
  time_cost_friendliness: 4
  documentation_quality: 4
  authority: 4
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2105.09938
  - https://github.com/hendrycks/apps
  - https://github.com/hendrycks/apps#readme

## Notes
- Searcher 仅提供事实型调研信息，不输出最终推荐排序。
- 缺失链接统一输出为 null，不编造 URL。
