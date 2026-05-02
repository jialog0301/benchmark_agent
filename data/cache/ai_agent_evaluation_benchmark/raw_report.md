# AI Agent Evaluation Benchmark Research Report

## Metadata
- topic: AI Agent Evaluation Benchmark
- mode: 课程实验
- topic_type: agent
- generated_at_utc: 2026-05-02T09:06:28.313068+00:00
- total_search_results: 10
- note: 本报告用于后续 extractor 抽取，不包含最终推荐排名。

## Search Goals
- 梳理 AI Agent Evaluation Benchmark 相关 benchmark 的代表性候选
- 收集每个 benchmark 的论文、代码、数据集和 leaderboard 入口
- 总结各 benchmark 的评测任务、能力维度和关键指标
- 比较资源完整度、文档质量与复现门槛
- 提炼适用于后续结构化抽取的证据链接集合
- 评估各候选 benchmark 的教学价值与课堂可讲解性
- 比较资源完整度（文档、代码、数据、示例）
- 判断复现友好度和环境部署复杂度

## Search Queries
- AI Agent Evaluation Benchmark benchmark paper GitHub leaderboard
- AI Agent Evaluation Benchmark evaluation benchmark dataset metrics
- AI Agent Evaluation Benchmark benchmark survey comparison
- AI Agent Evaluation Benchmark GitHub open source implementation
- AI Agent Evaluation Benchmark arxiv benchmark 2024 2025
- AI Agent Evaluation Benchmark teaching friendly benchmark tutorial reproducibility
- AI Agent Evaluation Benchmark benchmark documentation setup guide student project
- AI Agent Evaluation Benchmark benchmark quick demo time cost reproducible experiment

## Search Evidence Snapshot
1. [Sola-Visibility-ISPM: Benchmarking Agentic AI for Identity Security Posture Management Visibility](https://arxiv.org/abs/2601.07880v1) | source: arxiv | query: `AI Agent Evaluation Benchmark benchmark paper GitHub leaderboard`
2. [A Human-Grounded Evaluation Benchmark for Local Explanations of Machine Learning](https://arxiv.org/abs/1801.05075v2) | source: arxiv | query: `AI Agent Evaluation Benchmark benchmark paper GitHub leaderboard`
3. [SECQUE: A Benchmark for Evaluating Real-World Financial Analysis Capabilities](https://arxiv.org/abs/2504.04596v1) | source: arxiv | query: `AI Agent Evaluation Benchmark benchmark paper GitHub leaderboard`
4. [The ML.ENERGY Benchmark: Toward Automated Inference Energy Measurement and Optimization](https://arxiv.org/abs/2505.06371v2) | source: arxiv | query: `AI Agent Evaluation Benchmark benchmark paper GitHub leaderboard`
5. [BEDD: The MineRL BASALT Evaluation and Demonstrations Dataset for Training and Benchmarking Agents that Solve Fuzzy Tasks](https://arxiv.org/abs/2312.02405v1) | source: arxiv | query: `AI Agent Evaluation Benchmark evaluation benchmark dataset metrics`
6. [AI Agents: Evolution, Architecture, and Real-World Applications](https://arxiv.org/abs/2503.12687v1) | source: arxiv | query: `AI Agent Evaluation Benchmark benchmark survey comparison`
7. [Docling: An Efficient Open-Source Toolkit for AI-driven Document Conversion](https://arxiv.org/abs/2501.17887v1) | source: arxiv | query: `AI Agent Evaluation Benchmark GitHub open source implementation`
8. [AI prediction leads people to forgo guaranteed rewards](https://arxiv.org/abs/2603.28944v1) | source: arxiv | query: `AI Agent Evaluation Benchmark GitHub open source implementation`
9. [CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility Agent Benchmark](https://arxiv.org/abs/2409.11363v1) | source: arxiv | query: `AI Agent Evaluation Benchmark teaching friendly benchmark tutorial reproducibility`
10. [Agent-as-a-Judge: Evaluate Agents with Agents](https://arxiv.org/abs/2410.10934v2) | source: arxiv | query: `AI Agent Evaluation Benchmark benchmark documentation setup guide student project`

## Benchmark Candidates
### Benchmark 1: AgentBench
name: AgentBench
description: AgentBench benchmark candidate.
task_type: LLM-as-Agent Evaluation
evaluated_ability:
  - reasoning
  - tool interaction
metrics:
  - task success
paper_url: https://arxiv.org/abs/2308.03688
code_url: https://github.com/THUDM/AgentBench
dataset_url: null
leaderboard_url: null
project_url: https://github.com/THUDM/AgentBench
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
  requires_gpu: true
  requires_api_key: depends_on_agent_model
  estimated_setup_cost: high
  reproduction_notes: Reproduction difficulty=4 (higher is harder). Complexity inferred from task type and setup dependencies.
teaching_evidence:
  task_clarity: high
  example_tasks_available: true
  classroom_demo_value: high
  student_friendliness: low
  teaching_notes: Teaching value=4; time friendliness=2. README/examples availability used as proxy evidence.
research_evidence:
  representative_benchmark: true
  realistic_environment: true
  leaderboard_available: false
  baseline_results_available: true
  research_notes: Research value=5; authority=5. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: rate_limited_or_forbidden
  github_api_error_message: API rate limit exceeded for 66.90.98.146. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)
  github_stars: unknown
  github_forks: unknown
  leaderboard_or_project_available: true
  recent_repository_activity: unknown
  last_push_utc: unknown
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=4; stars=unknown, forks=unknown, recent_activity=unknown.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: false
  full_evaluation_cost: high
  estimated_demo_time: multiple_days
  estimated_full_reproduction_time: multiple_days
  time_cost_notes: Time friendliness=2; reproduction difficulty=4.
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
reproduction_difficulty: 4
teaching_value: 4
research_value: 5
topic_popularity: 4
time_cost_friendliness: 2
documentation_quality: 4
authority: 5
suggested_scores_for_extractor:
  resource_completeness: 4
  reproduction_difficulty: 4
  teaching_value: 4
  research_value: 5
  topic_popularity: 4
  time_cost_friendliness: 2
  documentation_quality: 4
  authority: 5
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2308.03688
  - https://github.com/THUDM/AgentBench
  - https://github.com/THUDM/AgentBench#readme

### Benchmark 2: WebArena
name: WebArena
description: WebArena benchmark candidate.
task_type: Web Agent Evaluation
evaluated_ability:
  - web navigation
  - planning
  - tool use
metrics:
  - task success rate
paper_url: https://arxiv.org/abs/2307.13854
code_url: https://github.com/web-arena-x/webarena
dataset_url: null
leaderboard_url: https://webarena.dev/
project_url: https://webarena.dev/
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
    - Browser automation dependencies
    - Website/service configuration
  requires_gpu: true
  requires_api_key: depends_on_agent_model
  estimated_setup_cost: very_high
  reproduction_notes: Reproduction difficulty=5 (higher is harder). Complexity inferred from task type and setup dependencies.
teaching_evidence:
  task_clarity: medium
  example_tasks_available: true
  classroom_demo_value: medium
  student_friendliness: low
  teaching_notes: Teaching value=3; time friendliness=2. README/examples availability used as proxy evidence.
research_evidence:
  representative_benchmark: true
  realistic_environment: true
  leaderboard_available: true
  baseline_results_available: true
  research_notes: Research value=5; authority=5. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: rate_limited_or_forbidden
  github_api_error_message: API rate limit exceeded for 66.90.98.146. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)
  github_stars: unknown
  github_forks: unknown
  leaderboard_or_project_available: true
  recent_repository_activity: unknown
  last_push_utc: unknown
  related_benchmarks_or_extensions:
    - VisualWebArena
    - BrowserGym
  popularity_notes: Topic popularity score=5; stars=unknown, forks=unknown, recent_activity=unknown.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: false
  full_evaluation_cost: very_high
  estimated_demo_time: multiple_days
  estimated_full_reproduction_time: multiple_days
  time_cost_notes: Time friendliness=2; reproduction difficulty=5.
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
reproduction_difficulty: 5
teaching_value: 3
research_value: 5
topic_popularity: 5
time_cost_friendliness: 2
documentation_quality: 4
authority: 5
suggested_scores_for_extractor:
  resource_completeness: 4
  reproduction_difficulty: 5
  teaching_value: 3
  research_value: 5
  topic_popularity: 5
  time_cost_friendliness: 2
  documentation_quality: 4
  authority: 5
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2307.13854
  - https://github.com/web-arena-x/webarena
  - https://webarena.dev/
  - https://github.com/web-arena-x/webarena#readme

### Benchmark 3: SWE-bench
name: SWE-bench
description: SWE-bench benchmark candidate.
task_type: Software Engineering Agent Evaluation
evaluated_ability:
  - issue resolution
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
  github_api_status: rate_limited_or_forbidden
  github_api_error_message: API rate limit exceeded for 66.90.98.146. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)
  github_stars: unknown
  github_forks: unknown
  leaderboard_or_project_available: true
  recent_repository_activity: unknown
  last_push_utc: unknown
  related_benchmarks_or_extensions:
    - SWE-bench Verified
    - Agentless
  popularity_notes: Topic popularity score=5; stars=unknown, forks=unknown, recent_activity=unknown.
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

### Benchmark 4: GAIA
name: GAIA
description: GAIA benchmark candidate.
task_type: General Assistant / Agent Evaluation
evaluated_ability:
  - reasoning
  - web browsing
  - tool use
metrics:
  - accuracy
paper_url: https://arxiv.org/abs/2311.12983
code_url: null
dataset_url: https://huggingface.co/datasets/gaia-benchmark/GAIA
leaderboard_url: https://huggingface.co/spaces/gaia-benchmark/leaderboard
project_url: https://huggingface.co/spaces/gaia-benchmark/leaderboard
open_source: null
resource_evidence:
  paper_available: true
  code_available: false
  dataset_available: true
  leaderboard_available: true
  official_site_available: true
  install_instructions_available: false
  quick_walkthrough_available: false
  docker_or_environment_files_available: unknown
  evidence_notes: Resource completeness score=4; evidence links include paper/code/dataset/leaderboard/readme where available.
reproduction_evidence:
  setup_requirements:
    - Python environment
  requires_gpu: false
  requires_api_key: depends_on_agent_model
  estimated_setup_cost: medium
  reproduction_notes: Reproduction difficulty=3 (higher is harder). Complexity inferred from task type and setup dependencies.
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
  research_notes: Research value=5; authority=4. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: false
  github_api_status: not_github_repo
  github_api_error_message: none
  github_stars: unknown
  github_forks: unknown
  leaderboard_or_project_available: true
  recent_repository_activity: unknown
  last_push_utc: unknown
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=4; stars=unknown, forks=unknown, recent_activity=unknown.
time_cost_evidence:
  quick_walkthrough_available: false
  small_demo_possible: true
  full_evaluation_cost: medium
  estimated_demo_time: 1-2_days
  estimated_full_reproduction_time: 1-2_days
  time_cost_notes: Time friendliness=3; reproduction difficulty=3.
documentation_evidence:
  readme_quality: high
  installation_steps_available: false
  examples_available: true
  evaluation_instructions_available: likely
  documentation_notes: Documentation quality score=4; README and project docs links are used as evidence.
authority_evidence:
  paper_available: true
  official_project_site: true
  official_github_repository: false
  leaderboard_available: true
  authority_notes: Authority score=4; based on availability of paper/repo/project/leaderboard.
resource_completeness: 4
reproduction_difficulty: 3
teaching_value: 4
research_value: 5
topic_popularity: 4
time_cost_friendliness: 3
documentation_quality: 4
authority: 4
suggested_scores_for_extractor:
  resource_completeness: 4
  reproduction_difficulty: 3
  teaching_value: 4
  research_value: 5
  topic_popularity: 4
  time_cost_friendliness: 3
  documentation_quality: 4
  authority: 4
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2311.12983
  - https://huggingface.co/datasets/gaia-benchmark/GAIA
  - https://huggingface.co/spaces/gaia-benchmark/leaderboard

### Benchmark 5: OSWorld
name: OSWorld
description: OSWorld benchmark candidate.
task_type: Computer-use Agent Evaluation
evaluated_ability:
  - GUI operation
  - desktop task solving
metrics:
  - task success rate
paper_url: https://arxiv.org/abs/2404.07972
code_url: https://github.com/xlang-ai/OSWorld
dataset_url: null
leaderboard_url: https://os-world.github.io/
project_url: https://os-world.github.io/
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
    - VM or desktop environment
    - GUI automation setup
  requires_gpu: true
  requires_api_key: depends_on_agent_model
  estimated_setup_cost: very_high
  reproduction_notes: Reproduction difficulty=5 (higher is harder). Complexity inferred from task type and setup dependencies.
teaching_evidence:
  task_clarity: medium
  example_tasks_available: true
  classroom_demo_value: medium
  student_friendliness: low
  teaching_notes: Teaching value=3; time friendliness=2. README/examples availability used as proxy evidence.
research_evidence:
  representative_benchmark: true
  realistic_environment: true
  leaderboard_available: true
  baseline_results_available: true
  research_notes: Research value=5; authority=4. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: rate_limited_or_forbidden
  github_api_error_message: API rate limit exceeded for 66.90.98.146. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)
  github_stars: unknown
  github_forks: unknown
  leaderboard_or_project_available: true
  recent_repository_activity: unknown
  last_push_utc: unknown
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=4; stars=unknown, forks=unknown, recent_activity=unknown.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: false
  full_evaluation_cost: very_high
  estimated_demo_time: multiple_days
  estimated_full_reproduction_time: multiple_days
  time_cost_notes: Time friendliness=2; reproduction difficulty=5.
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
reproduction_difficulty: 5
teaching_value: 3
research_value: 5
topic_popularity: 4
time_cost_friendliness: 2
documentation_quality: 3
authority: 4
suggested_scores_for_extractor:
  resource_completeness: 4
  reproduction_difficulty: 5
  teaching_value: 3
  research_value: 5
  topic_popularity: 4
  time_cost_friendliness: 2
  documentation_quality: 3
  authority: 4
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2404.07972
  - https://github.com/xlang-ai/OSWorld
  - https://os-world.github.io/
  - https://github.com/xlang-ai/OSWorld#readme

### Benchmark 6: ToolBench
name: ToolBench
description: ToolBench benchmark candidate.
task_type: Tool-use Agent Evaluation
evaluated_ability:
  - API selection
  - tool use
metrics:
  - pass rate
paper_url: null
code_url: https://github.com/OpenBMB/ToolBench
dataset_url: null
leaderboard_url: null
project_url: https://github.com/OpenBMB/ToolBench
open_source: true
resource_evidence:
  paper_available: false
  code_available: true
  dataset_available: false
  leaderboard_available: false
  official_site_available: true
  install_instructions_available: true
  quick_walkthrough_available: true
  docker_or_environment_files_available: true
  evidence_notes: Resource completeness score=3; evidence links include paper/code/dataset/leaderboard/readme where available.
reproduction_evidence:
  setup_requirements:
    - Python environment
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
  leaderboard_available: false
  baseline_results_available: likely
  research_notes: Research value=4; authority=4. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: rate_limited_or_forbidden
  github_api_error_message: API rate limit exceeded for 66.90.98.146. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)
  github_stars: unknown
  github_forks: unknown
  leaderboard_or_project_available: true
  recent_repository_activity: unknown
  last_push_utc: unknown
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=4; stars=unknown, forks=unknown, recent_activity=unknown.
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
  evaluation_instructions_available: unknown
  documentation_notes: Documentation quality score=3; README and project docs links are used as evidence.
authority_evidence:
  paper_available: false
  official_project_site: true
  official_github_repository: true
  leaderboard_available: false
  authority_notes: Authority score=4; based on availability of paper/repo/project/leaderboard.
resource_completeness: 3
reproduction_difficulty: 4
teaching_value: 4
research_value: 4
topic_popularity: 4
time_cost_friendliness: 3
documentation_quality: 3
authority: 4
suggested_scores_for_extractor:
  resource_completeness: 3
  reproduction_difficulty: 4
  teaching_value: 4
  research_value: 4
  topic_popularity: 4
  time_cost_friendliness: 3
  documentation_quality: 3
  authority: 4
limitations: null
suitable_usage: null
evidence:
  - https://github.com/OpenBMB/ToolBench
  - https://github.com/OpenBMB/ToolBench#readme

### Benchmark 7: Mind2Web
name: Mind2Web
description: Mind2Web benchmark candidate.
task_type: Web Agent Evaluation
evaluated_ability:
  - web navigation
  - instruction following
  - action grounding
metrics:
  - task success rate
paper_url: https://arxiv.org/abs/2306.06070
code_url: https://github.com/OSU-NLP-Group/Mind2Web
dataset_url: https://huggingface.co/datasets/osunlp/Mind2Web
leaderboard_url: null
project_url: https://osu-nlp-group.github.io/Mind2Web/
open_source: true
resource_evidence:
  paper_available: true
  code_available: true
  dataset_available: true
  leaderboard_available: false
  official_site_available: true
  install_instructions_available: true
  quick_walkthrough_available: true
  docker_or_environment_files_available: true
  evidence_notes: Resource completeness score=4; evidence links include paper/code/dataset/leaderboard/readme where available.
reproduction_evidence:
  setup_requirements:
    - Python environment
    - Browser automation dependencies
    - Website/service configuration
  requires_gpu: true
  requires_api_key: depends_on_agent_model
  estimated_setup_cost: high
  reproduction_notes: Reproduction difficulty=4 (higher is harder). Complexity inferred from task type and setup dependencies.
teaching_evidence:
  task_clarity: high
  example_tasks_available: true
  classroom_demo_value: high
  student_friendliness: low
  teaching_notes: Teaching value=4; time friendliness=2. README/examples availability used as proxy evidence.
research_evidence:
  representative_benchmark: true
  realistic_environment: true
  leaderboard_available: false
  baseline_results_available: true
  research_notes: Research value=5; authority=5. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: rate_limited_or_forbidden
  github_api_error_message: API rate limit exceeded for 66.90.98.146. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)
  github_stars: unknown
  github_forks: unknown
  leaderboard_or_project_available: true
  recent_repository_activity: unknown
  last_push_utc: unknown
  related_benchmarks_or_extensions:
    - WebArena
  popularity_notes: Topic popularity score=4; stars=unknown, forks=unknown, recent_activity=unknown.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: false
  full_evaluation_cost: high
  estimated_demo_time: multiple_days
  estimated_full_reproduction_time: multiple_days
  time_cost_notes: Time friendliness=2; reproduction difficulty=4.
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
reproduction_difficulty: 4
teaching_value: 4
research_value: 5
topic_popularity: 4
time_cost_friendliness: 2
documentation_quality: 4
authority: 5
suggested_scores_for_extractor:
  resource_completeness: 4
  reproduction_difficulty: 4
  teaching_value: 4
  research_value: 5
  topic_popularity: 4
  time_cost_friendliness: 2
  documentation_quality: 4
  authority: 5
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2306.06070
  - https://github.com/OSU-NLP-Group/Mind2Web
  - https://huggingface.co/datasets/osunlp/Mind2Web
  - https://github.com/OSU-NLP-Group/Mind2Web#readme

### Benchmark 8: AgentBoard
name: AgentBoard
description: AgentBoard benchmark candidate.
task_type: Cross-domain Agent Benchmark
evaluated_ability:
  - planning
  - tool use
  - long-horizon decision making
metrics:
  - normalized task score
paper_url: https://arxiv.org/abs/2401.13178
code_url: https://github.com/hkust-nlp/AgentBoard
dataset_url: null
leaderboard_url: null
project_url: https://github.com/hkust-nlp/AgentBoard
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
  leaderboard_available: false
  baseline_results_available: true
  research_notes: Research value=5; authority=4. Presence of paper/leaderboard/code improves research comparability.
popularity_evidence:
  github_repository_available: true
  github_api_status: rate_limited_or_forbidden
  github_api_error_message: API rate limit exceeded for 66.90.98.146. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)
  github_stars: unknown
  github_forks: unknown
  leaderboard_or_project_available: true
  recent_repository_activity: unknown
  last_push_utc: unknown
  related_benchmarks_or_extensions:
    - AgentBench
    - ToolBench
  popularity_notes: Topic popularity score=3; stars=unknown, forks=unknown, recent_activity=unknown.
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
  leaderboard_available: false
  authority_notes: Authority score=4; based on availability of paper/repo/project/leaderboard.
resource_completeness: 4
reproduction_difficulty: 4
teaching_value: 4
research_value: 5
topic_popularity: 3
time_cost_friendliness: 3
documentation_quality: 4
authority: 4
suggested_scores_for_extractor:
  resource_completeness: 4
  reproduction_difficulty: 4
  teaching_value: 4
  research_value: 5
  topic_popularity: 3
  time_cost_friendliness: 3
  documentation_quality: 4
  authority: 4
limitations: null
suitable_usage: null
evidence:
  - https://arxiv.org/abs/2401.13178
  - https://github.com/hkust-nlp/AgentBoard
  - https://github.com/hkust-nlp/AgentBoard#readme

## Notes
- Searcher 仅提供事实型调研信息，不输出最终推荐排序。
- 缺失链接统一输出为 null，不编造 URL。
