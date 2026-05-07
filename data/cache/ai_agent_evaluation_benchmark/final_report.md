1. **Topic**: AI Agent Evaluation Benchmark
2. **Mode**: 课程实验 (Course Experiment)
3. **Benchmarks**: 7 benchmarks total, ranked by Task-Fit Score

Let me organize the data:

**Rankings by Task-Fit Score:**
1. Mind2Web - 3.75
2. ToolBench - 3.7
3. GAIA - 3.6
4. SWE-bench - 3.45
5. AgentBench - 3.4
6. WebArena - 3.1
7. OSWorld - 2.1

**Key metrics from the data:**
- Resource completeness ranges from 3-4
- Reproduction difficulty ranges from 2-5
- Teaching value ranges from 2-4
- Research value ranges from 3-5
- Topic popularity ranges from 3-5
- Time cost friendliness ranges from 1-4
- Documentation quality ranges from 3-4
- Authority ranges from 4-5

Now let me generate the report following the exact format requested:

```markdown
# BenchmarkRadar Report: AI Agent Evaluation Benchmark

## 1. 调研主题
AI Agent Evaluation Benchmark

## 2. 推荐模式
课程实验

## 3. 背景与动机
Brief introduction about why this research direction is important...

## 4. Benchmark 总览
Overview of the 7 benchmarks...

## 5. Benchmark 结构化对比表及排名
Table with all 7 benchmarks...

## 6. Top Benchmark 深度分析
Detailed analysis of top 3...

## 7. 推荐使用方案
Recommendations based on mode...

## 8. 局限性
Limitations of the report...

## 9. 参考资料


References with links...
```

I'll now write the full report in Chinese with all the data properly organized.


# BenchmarkRadar Report: AI Agent Evaluation Benchmark

## 1. 调研主题

AI Agent Evaluation Benchmark

## 2. 推荐模式

课程实验

## 3. 背景与动机

随着大型语言模型（LLM）技术的快速发展，AI Agent（人工智能代理）已成为当前学术研究和工业应用的核心方向之一。AI Agent 能够自主完成复杂任务，如网页导航、代码生成、工具调用和操作系统控制等。然而，如何科学、系统地评估 AI Agent 的能力边界仍是该领域面临的关键挑战。

Benchmark（基准测试）在 AI Agent 研究中扮演着至关重要的角色。它不仅为研究者提供了统一的评估标准和量化指标，还能够帮助学生和开发者理解不同 Agent 系统的能力差异。本报告针对 **课程实验** 这一推荐模式，对主流的 AI Agent Evaluation Benchmark 进行系统梳理和深度分析，旨在帮助教育者和学生快速定位适合教学实践的高质量评测基准，降低实验门槛，提升学习效率。

## 4. Benchmark 总览

本报告共抽取并分析了 **7 个** AI Agent 评测基准，涵盖 Web 代理、工具学习、软件工程、通用助手和操作系统等多个核心领域。整体来看，这 7 个基准均已开源，具备较高的研究价值，但在教学适用性上存在显著差异。

从资源完整度来看，大多数基准（5/7）提供了 4/5 的资源完整度评分，说明其代码、数据集和文档配套相对完善。从复现难度来看，评分跨度较大（2-5 分），其中 Mind2Web 和 GAIA 复现友好度最高（2/5），而 OSWorld 复现难度最大（5/5）。从时间友好度来看，GAIA 表现最佳（4/5），而 OSWorld 仅为 1/5，不适合短期课程项目。

所有基准均支持开源获取，学生可以访问论文、代码仓库和数据集进行学习和实践。综合 Task-Fit Score 排名，排名前三的 **Mind2Web、ToolBench 和 GAIA** 在课程实验场景下展现出最佳的综合适配性。

## 5. Benchmark 结构化对比表及排名

| 排名 | Benchmark 名称 | Task-Fit Score | 任务类型 | 教学价值 | 科研价值 | 资源完整度 |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 1 | Mind2Web | 3.75 | Web Agent Evaluation | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 2 | ToolBench | 3.70 | Tool Learning Evaluation | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 3 | GAIA | 3.60 | General AI Assistant Evaluation | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 4 | SWE-bench | 3.45 | Software Engineering Agent Evaluation | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 5 | AgentBench | 3.40 | LLM-as-Agent Evaluation | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 6 | WebArena | 3.10 | Web Agent Evaluation | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 7 | OSWorld | 2.10 | OS Agent Evaluation | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## 6. Top Benchmark 深度分析

### 6.1 Mind2Web（排名第 1，Task-Fit Score: 3.75）

**基本概述**

Mind2Web 是一个专注于 Web 代理评测的数据集，包含真实的网页交互任务，旨在评估 AI Agent 在复杂 Web 环境中的导航、操作和推理能力。该基准由俄亥俄州立大学（OSU）NLP 团队开发和维护，在学术界具有较高的影响力。

**核心优势**

1. **复现友好度高**：复现难度仅为 2/5，学生可以在短时间内完成环境搭建和基准测试，降低了课程实验的入门门槛。
2. **教学价值突出**：教学价值评分高达 4/5，任务场景直观易懂，学生可以快速理解 Web 代理的工作原理和评估方法。
3. **资源完整度优秀**：提供完整的开源代码（GitHub）和 HuggingFace 数据集，学生可以方便地获取实验材料。
4. **适合课堂演示**：Web 交互任务可视化程度高，教师可以在课堂上演示 Agent 的决策过程，增强教学效果。

**局限性**

数据集规模相对较小，评估场景有限。对于需要大规模验证的科研项目可能不够充分，但对于基础课程作业而言足够使用。

**适用场景**

- Web 代理入门学习
- 课堂教学演示
- 课程作业和小型实验项目

**推荐理由**

> Mind2Web 在课程实验模式下 Task-Fit Score 达 3.75，排名第 1。教学价值 4/5、资源完整度 4/5，且复现难度仅 2/5（复现友好度高），非常适合学生进行 Web 交互代理的入门学习和课堂演示。虽然数据集规模相对较小、评估场景有限，但对于基础课程作业而言足够使用，开源代码和数据集已开源，学生可以快速上手实践。

---

### 6.2 ToolBench（排名第 2，Task-Fit Score: 3.70）

**基本概述**

ToolBench 是由清华大学 OpenBMB 团队开发的工具学习评测基准，用于评估 LLM 使用外部工具解决问题的能力。该基准覆盖了丰富的工具 API 调用场景，是当前工具学习领域最具代表性的评测标准之一。

**核心优势**

1. **任务场景前沿**：工具学习是 Agent 能力的核心组成部分，ToolBench 紧跟学术前沿，能够帮助学生深入理解工具调用的技术原理。
2. **教学与科研兼顾**：教学价值 4/5、科研价值 4/5，既适合教学演示，也能支撑有一定深度的课程项目。
3. **资源完整度高**：提供完整的 GitHub 代码仓库和 HuggingFace 数据集，学生可以系统性地学习工具学习的全流程。
4. **话题热度适中**：Topic Popularity 为 4/5，属于当前 AI 领域的热门方向，有助于学生了解行业发展趋势。

**局限性**

工具 API 调用可能产生额外成本，工具集规模庞大可能导致实验周期延长。建议教师提前预设简化工具集以控制实验时间。

**适用场景**

- 工具学习研究
- 智能助手开发
- 中高级课程实验项目

**推荐理由**

> ToolBench 任务拟合分数 3.7，排名第 2，是工具学习方向的高质量评测基准，适合作为课程实验选题。教学价值 4/5、资源完整度 4/5，提供了完整的开源代码和数据集，学生可快速上手工具调用与函数推理任务。复现友好度中等（复现难度 3/5），主要挑战在于工具 API 调用成本和工具集规模，建议教师提前预设简化工具集以控制实验时间，整体而言是兼具前沿性和实操性的课程实验候选。

---

### 6.3 GAIA（排名第 3，Task-Fit Score: 3.60）

**基本概述**

GAIA（General AI Assistant）是一个通用 AI 助手评估基准，测试 AI 系统处理多种类型问题的能力，涵盖问答、推理和事实核查等核心能力。该基准旨在提供贴近真实需求的评测场景，评估 Agent 的综合智能水平。

**核心优势**

1. **时间友好度最高**：Time Cost Friendliness 为 4/5，学生在有限的课程周期内即可完成完整的实验流程。
2. **任务多样性**：覆盖问答、推理和事实核查等多种能力，任务场景贴近真实需求，能够全面评估学生的理解能力。
3. **数据集易获取**：官方提供 HuggingFace 数据集，数据下载和预处理流程相对简单。
4. **综合教学价值**：教学价值 4/5，学生可以全面理解通用 AI 助手评估流程，培养系统性思维。

**局限性**

代码实现尚不完整，部分评估可能需要人工介入，评估标准的自动化程度有待提升。

**适用场景**

- 通用 AI 助手评测
- 课程作业评估
- AI 基础理论学习

**推荐理由**

> GAIA 适合作为课程实验选择，Task-Fit Score 达 3.6，排名第 3。教学价值 4/5，覆盖问答、推理和事实核查等多种能力，任务场景贴近真实需求，学生能全面理解通用 AI 助手评估流程。复现友好度 4/5，官方提供 HuggingFace 数据集且开源，复现成本可控。虽然代码实现不完整且部分评估需人工介入，但整体难度适中，适合课程作业周期。

---

### 6.4 排名 4-7 的基准概览

| 排名 | Benchmark | Task-Fit Score | 特点与局限 |
|:---:|---|---|---|
| 4 | SWE-bench | 3.45 | 代码生成与 bug 修复方向优秀，但时间成本高（2/5），适合高年级学生 |
| 5 | AgentBench | 3.40 | 综合能力强但需要 GPU 资源，不适合资源受限的课程环境 |
| 6 | WebArena | 3.10 | 环境配置复杂，适合研究生高级项目而非本科课程 |
| 7 | OSWorld | 2.10 | 需要完整操作系统环境，资源消耗极大，不推荐作为课程实验资源 |

## 7. 推荐使用方案

基于 **课程实验** 模式的需求，本报告提出以下分级推荐方案：

### 7.1 首选推荐（可直接使用）

| Benchmark | 适用场景 | 使用建议 |
|---|---|---|
| **Mind2Web** | Web 代理入门、课堂演示、基础课程作业 | 推荐指数：⭐⭐⭐⭐⭐<br>优先用于 Web 交互相关的课程实验，环境搭建简单，学生可快速产出成果 |
| **GAIA** | 通用 AI 能力评估、短期课程作业 | 推荐指数：⭐⭐⭐⭐⭐<br>时间成本最低，适合 2-4 周的短期实验项目 |

### 7.2 备选推荐（需提前准备）

| Benchmark | 适用场景 | 使用建议 |
|---|---|---|
| **ToolBench** | 工具学习方向、中高级课程项目 | 推荐指数：⭐⭐⭐⭐<br>建议教师提前预设简化工具集（建议选取 5-10 个核心工具），并控制 API 调用次数 |
| **SWE-bench** | 高年级软件工程相关课程、研究导向项目 | 推荐指数：⭐⭐⭐<br>适合作为课程项目或毕业设计方向，不建议作为大规模课程作业 |

### 7.3 不推荐作为课程实验资源

| Benchmark | 原因 |
|---|---|
| **AgentBench** | 需要 GPU 资源，数据集不可直接下载，完整评估成本高 |
| **WebArena** | 环境配置复杂，运行时间较长，资源受限场景下难以完成 |
| **OSWorld** | 需要完整操作系统环境，资源消耗极大，实验周期不可控 |

### 7.4 课程实施方案建议

对于 **Web 代理方向** 的课程实验，建议采用以下方案：

1. **Week 1-2**：以 Mind2Web 为核心，让学生熟悉 Web 代理的基本架构和评测流程，完成基线实验
2. **Week 3-4**：引入 ToolBench 的简化版本（预设 5 个核心工具），让学生动手实现简单的工具调用 Agent
3. **Week 5-6**：使用 GAIA 进行综合能力评估，让学生对比不同 Agent 在问答、推理任务上的表现差异

## 8. 局限性

本报告存在以下局限性，需读者在使用时予以考虑：

### 8.1 数据时效性

本报告基于当前可获取的 Benchmark 信息编制，AI Agent 领域发展迅速，新的评测基准和更新版本可能持续涌现。报告中的评分和推荐可能随时间推移而发生变化，建议读者结合最新学术动态进行综合判断。

### 8.2 评分主观性

Benchmark 的各项评分（包括教学价值、科研价值、复现难度等）基于综合考量确定，存在一定的主观性。不同教育背景、不同实验条件下的实际体验可能与报告评分存在偏差。建议教师和学生根据自身实际情况调整选择策略。

### 8.3 资源依赖差异

报告中涉及的资源需求（如 GPU 资源、API 调用成本等）可能因具体实验环境、课程预算等因素而存在显著差异。OSWorld 等需要高计算资源的基准在本报告中评分较低，但在具备相应条件的科研环境中可能具有更高的实用价值。

### 8.4 评测场景覆盖有限

本报告重点关注课程实验场景下的 Benchmark 适用性，对于其他使用模式（如科研项目、企业评估等）的参考价值可能有限。不同模式下的最优选择可能存在较大差异。

## 9. 参考资料

- **Mind2Web**: [论文链接](https://arxiv.org/abs/2306.13327) | [代码链接](https://github.com/OSU-NLP-Group/Mind2Web) | [数据集链接](https://huggingface.co/datasets/OhioStateMind2Web/Mind2Web)
- **ToolBench**: [论文链接](https://arxiv.org/abs/2305.16504) | [代码链接](https://github.com/OpenBMB/ToolBench) | [数据集链接](https://huggingface.co/datasets/OpenBMB/ToolBench)
- **GAIA**: [论文链接](https://arxiv.org/abs/2311.12983) | [数据集链接](https://huggingface.co/datasets/gaia-benchmark/GAIA)
- **SWE-bench**: [论文链接](https://arxiv.org/abs/2312.15064) | [代码链接](https://github.com/princeton-nlp/SWE-bench) | [数据集链接](https://huggingface.co/datasets/princeton-nlp/SWE-bench)
- **AgentBench**: [论文链接](https://arxiv.org/abs/2308.03688) | [代码链接](https://github.com/THUDM/AgentBench)
- **WebArena**: [论文链接](https://arxiv.org/abs/2307.13854) | [代码/数据集链接](https://github.com/web-arena-x/webarena)
- **OSWorld**: [论文链接](https://arxiv.org/abs/2307.14758) | [代码链接](https://github.com/OSWorld-benchmark/OSWorld)

---

*本报告由 BenchmarkRadar 自动化生成，生成日期：2024 年。报告内容仅供参考，实际使用时请结合具体需求进行调整。*