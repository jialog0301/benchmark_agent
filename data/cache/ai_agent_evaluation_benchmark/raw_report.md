# AI Agent Evaluation Benchmark Research Report

## Metadata
- topic: AI Agent Evaluation Benchmark
- mode: 课程实验
- topic_type: agent
- generated_at_utc: 2026-05-07T07:34:29.443199+00:00
- total_search_results: 44
- note: 本报告用于后续 extractor 抽取，不包含最终推荐排名。

## Search Goals
- 了解当前主流的AI Agent评估基准及其评价指标
- 获取用于课程实验的AI Agent评估基准的完整资源（代码、数据集、文档）
- 评估不同基准的易用性、再现性和教学价值
- 比较基准在时间成本和资源需求方面的差异
- 寻找适合学生实验的快速上手和可复现的基准项目

## Search Queries
- AI agent evaluation benchmark reproducibility course experiment GitHub dataset metrics
- AI agent benchmark teaching value assignment lab resources open source
- comparison of AI agent evaluation benchmarks leaderboard metrics reproducibility
- AI agent evaluation benchmark quickstart guide for course lab assignment
- AI agent benchmark dataset availability and documentation for teaching
- AI Agent Evaluation Benchmark AgentBench WebArena SWE-bench GAIA OSWorld ToolBench Mind2Web AgentBoard
- AI Agent Evaluation Benchmark agent evaluation benchmark leaderboard
- AI Agent Evaluation Benchmark web agent tool use benchmark

## Search Evidence Snapshot
1. [ResearchClawBench: Evaluating AI Agents for Automated ... - GitHub](https://github.com/InternScience/ResearchClawBench) | source: tavily | query: `AI agent evaluation benchmark reproducibility course experiment GitHub dataset metrics`
2. [philschmid/ai-agent-benchmark-compendium ... - GitHub](https://github.com/philschmid/ai-agent-benchmark-compendium) | source: tavily | query: `AI agent evaluation benchmark reproducibility course experiment GitHub dataset metrics`
3. [15 Datasets for Training and Evaluating AI Agents | by ODSC](https://odsc.medium.com/15-datasets-for-training-and-evaluating-ai-agents-c171dde4e0ce) | source: tavily | query: `AI agent evaluation benchmark reproducibility course experiment GitHub dataset metrics`
4. [Vvkmnn/awesome-ai-eval - GitHub](https://github.com/Vvkmnn/awesome-ai-eval) | source: tavily | query: `AI agent evaluation benchmark reproducibility course experiment GitHub dataset metrics`
5. [GitHub - danielrosehill/Awesome-AI-Evaluations-Tools](https://github.com/danielrosehill/Awesome-AI-Evaluations-Tools) | source: tavily | query: `AI agent evaluation benchmark reproducibility course experiment GitHub dataset metrics`
6. [Benchmarking AI agents against 800+ open source tests - AI Tinkerers](https://nyc.aitinkerers.org/talks/rsvp_oHcOn4pn-yw) | source: tavily | query: `AI agent benchmark teaching value assignment lab resources open source`
7. [Awesome AI Agents: Tools, Resources, and Projects - GitHub](https://github.com/jim-schwoebel/awesome_ai_agents) | source: tavily | query: `AI agent benchmark teaching value assignment lab resources open source`
8. [Evaluating AI Agents in 2025 - by Nilesh Barla](https://labs.adaline.ai/p/evaluating-ai-agents-in-2025) | source: tavily | query: `AI agent benchmark teaching value assignment lab resources open source`
9. [An Open-Source AI Agent for Doing Tasks on the Web | Stanford HAI](https://hai.stanford.edu/news/an-open-source-ai-agent-for-doing-tasks-on-the-web) | source: tavily | query: `AI agent benchmark teaching value assignment lab resources open source`
10. [AstaBench: Rigorous benchmarking of AI agents with a holistic scientific research suite  | Ai2](https://allenai.org/blog/astabench) | source: tavily | query: `AI agent benchmark teaching value assignment lab resources open source`
11. [Efficient Benchmarking of AI Agents](https://arxiv.org/html/2603.23749v1) | source: tavily | query: `comparison of AI agent evaluation benchmarks leaderboard metrics reproducibility`
12. [𝜏-Bench leaderboard: compare, explore, and understand agent performance | Sierra](https://sierra.ai/blog/t-bench-leaderboard) | source: tavily | query: `comparison of AI agent evaluation benchmarks leaderboard metrics reproducibility`
13. [Agent Evaluation Framework 2026: Metrics, Rubrics & Benchmarks](https://galileo.ai/blog/agent-evaluation-framework-metrics-rubrics-benchmarks) | source: tavily | query: `comparison of AI agent evaluation benchmarks leaderboard metrics reproducibility`
14. [Best AI Agent Evaluation Benchmarks: 2025 Complete Guide](https://o-mega.ai/articles/the-best-ai-agent-evals-and-benchmarks-full-2025-guide) | source: tavily | query: `comparison of AI agent evaluation benchmarks leaderboard metrics reproducibility`
15. [AI Agent Benchmarks: What They Measure & Where They Fall Short](https://redis.io/blog/ai-agent-benchmarks/) | source: tavily | query: `comparison of AI agent evaluation benchmarks leaderboard metrics reproducibility`
16. [The Complete Guide to AI Agent Evaluation: Key Steps, Metrics & Best…](https://delight.ai/blog/ai-agent/ai-agent-evaluation-guide) | source: tavily | query: `AI agent evaluation benchmark quickstart guide for course lab assignment`
17. [Evaluating AI Agents in 2025: A Practical Guide - Turing College](https://www.turingcollege.com/blog/evaluating-ai-agents-practical-guide) | source: tavily | query: `AI agent evaluation benchmark quickstart guide for course lab assignment`
18. [Agent Evaluation: How to Test and Measure Agentic AI Performance - MachineLearningMastery.com](https://machinelearningmastery.com/agent-evaluation-how-to-test-and-measure-agentic-ai-performance/) | source: tavily | query: `AI agent evaluation benchmark quickstart guide for course lab assignment`
19. [AI Agent Evaluation: How to Build Custom Benchmarks That Actually Test Intelligence | MindStudio](https://www.mindstudio.ai/blog/ai-agent-custom-benchmarks-evaluation/) | source: tavily | query: `AI agent evaluation benchmark quickstart guide for course lab assignment`
20. [Agentic Evaluations: Benchmark AI Agent Quality, Performance & Safety | Solo.io](https://www.solo.io/blog/agentic-quality-benchmarking-with-agent-evals) | source: tavily | query: `AI agent evaluation benchmark quickstart guide for course lab assignment`

## Benchmark Candidates
### Benchmark 1: WebArena
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
dataset_url: https://odsc.medium.com/15-datasets-for-training-and-evaluating-ai-agents-c171dde4e0ce
leaderboard_url: https://webarena.dev/
project_url: https://webarena.dev/
open_source: true
resource_evidence:
  paper_available: true
  code_available: true
  dataset_available: true
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
  github_api_status: ok
  github_api_error_message: none
  github_stars: 1453
  github_forks: 236
  leaderboard_or_project_available: true
  recent_repository_activity: true
  last_push_utc: 2025-11-26T21:16:00Z
  related_benchmarks_or_extensions:
    - VisualWebArena
    - BrowserGym
  popularity_notes: Topic popularity score=5; stars=1453, forks=236, recent_activity=true.
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
  - https://odsc.medium.com/15-datasets-for-training-and-evaluating-ai-agents-c171dde4e0ce
  - https://nyc.aitinkerers.org/talks/rsvp_oHcOn4pn-yw
  - https://byteiota.com/berkeley-breaks-ai-agent-benchmarks-100-scores-zero-solutions/
  - https://leaderboard.steel.dev/results
  - https://o-mega.ai/articles/top-10-agentic-evals-benchmarking-actionable-ai-2025

### Benchmark 2: AgentBench
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
  github_api_status: ok
  github_api_error_message: none
  github_stars: 3394
  github_forks: 250
  leaderboard_or_project_available: true
  recent_repository_activity: true
  last_push_utc: 2026-02-08T17:01:05Z
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=4; stars=3394, forks=250, recent_activity=true.
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
  - https://galileo.ai/blog/agent-evaluation-framework-metrics-rubrics-benchmarks
  - https://o-mega.ai/articles/the-best-ai-agent-evals-and-benchmarks-full-2025-guide
  - https://www.turingcollege.com/blog/evaluating-ai-agents-practical-guide
  - https://benchmarkingagents.com/agent-benchmarks/
  - https://github.com/jackjin1997/AgentBench-Live
  - https://github.com/SanJueLogic/MeiGen-DesignAgentBench

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
code_url: https://github.com/Pandagan-85/React_agent_Gaia
dataset_url: https://huggingface.co/datasets/gaia-benchmark/GAIA
leaderboard_url: https://huggingface.co/spaces/gaia-benchmark/leaderboard
project_url: https://huggingface.co/spaces/gaia-benchmark/leaderboard
open_source: null
resource_evidence:
  paper_available: true
  code_available: true
  dataset_available: true
  leaderboard_available: true
  official_site_available: true
  install_instructions_available: true
  quick_walkthrough_available: true
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
  github_repository_available: true
  github_api_status: ok
  github_api_error_message: none
  github_stars: 1
  github_forks: 0
  leaderboard_or_project_available: true
  recent_repository_activity: false
  last_push_utc: 2025-06-18T11:31:30Z
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=4; stars=1, forks=0, recent_activity=false.
time_cost_evidence:
  quick_walkthrough_available: true
  small_demo_possible: true
  full_evaluation_cost: medium
  estimated_demo_time: 1-2_days
  estimated_full_reproduction_time: 1-2_days
  time_cost_notes: Time friendliness=3; reproduction difficulty=3.
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
  - https://github.com/Pandagan-85/React_agent_Gaia
  - https://github.com/pradeepdas/gaia-agentbeats

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
  github_api_status: ok
  github_api_error_message: none
  github_stars: 2828
  github_forks: 450
  leaderboard_or_project_available: true
  recent_repository_activity: true
  last_push_utc: 2026-05-07T02:47:31Z
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=4; stars=2828, forks=450, recent_activity=true.
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
  github_api_status: ok
  github_api_error_message: none
  github_stars: 5629
  github_forks: 485
  leaderboard_or_project_available: true
  recent_repository_activity: false
  last_push_utc: 2025-05-21T15:46:59Z
  related_benchmarks_or_extensions: []
  popularity_notes: Topic popularity score=4; stars=5629, forks=485, recent_activity=false.
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
  github_api_status: ok
  github_api_error_message: none
  github_stars: 986
  github_forks: 123
  leaderboard_or_project_available: true
  recent_repository_activity: false
  last_push_utc: 2025-11-05T00:38:41Z
  related_benchmarks_or_extensions:
    - WebArena
  popularity_notes: Topic popularity score=4; stars=986, forks=123, recent_activity=false.
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
  github_api_status: ok
  github_api_error_message: none
  github_stars: 413
  github_forks: 42
  leaderboard_or_project_available: true
  recent_repository_activity: false
  last_push_utc: 2024-05-20T13:44:42Z
  related_benchmarks_or_extensions:
    - AgentBench
    - ToolBench
  popularity_notes: Topic popularity score=3; stars=413, forks=42, recent_activity=false.
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
