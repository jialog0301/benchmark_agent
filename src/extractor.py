"""Benchmark Extractor module."""

from __future__ import annotations

import json
import re
from pathlib import Path

from src.llm_client import call_llm
from src.schemas import Benchmark

BASE_DIR = Path(__file__).resolve().parent.parent
EXTRACTOR_PROMPT_PATH = BASE_DIR / "prompts" / "extractor.md"

MIN_BENCHMARKS = 5
MAX_BENCHMARKS = 20


def _dedupe_strings(values: list[str]) -> list[str]:
    """Return a de-duplicated list while preserving order."""
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def _extract_urls_from_text(text: str) -> list[str]:
    """Collect real URLs from raw text in their original order."""
    if not text:
        return []
    return _dedupe_strings(re.findall(r"https?://[^\s\)\]\}>\"']+", text))


def _infer_metrics(name: str, task_type: str | None, evaluated_ability: list[str]) -> list[str]:
    """Infer likely metrics from benchmark metadata."""
    text = f"{name} {task_type or ''} {' '.join(evaluated_ability)}".lower()
    candidates: list[str] = []

    if any(keyword in text for keyword in ["agent", "web", "tool", "assistant"]):
        candidates.extend(["task success rate", "pass rate", "accuracy"])
    if any(keyword in text for keyword in ["rag", "retrieval", "qa", "question"]):
        candidates.extend(["accuracy", "f1", "nDCG@10", "recall@k"])
    if any(keyword in text for keyword in ["code", "software", "swe", "bug"]):
        candidates.extend(["resolved issue rate", "pass@1", "task success rate"])
    if any(keyword in text for keyword in ["function", "api", "tool"]):
        candidates.extend(["pass rate", "accuracy"])

    if not candidates:
        candidates.extend(["accuracy", "task success rate"])

    return _dedupe_strings(candidates)[:4]


def _infer_description(name: str, task_type: str | None, evaluated_ability: list[str]) -> str:
    """Create a concise description when the model leaves it empty."""
    abilities = "、".join(evaluated_ability[:3]) if evaluated_ability else "核心能力评测"
    task = task_type or "相关任务"
    return f"{name} 是用于 {task} 的 Benchmark，主要关注 {abilities}。"


def _infer_limitations(name: str, task_type: str | None, evidence: list[str]) -> str:
    """Create a short limitation note when nothing explicit is available."""
    if evidence:
        return f"{name} 主要依赖公开论文、代码或榜单信息，跨环境复现时可能需要额外配置。"
    if task_type:
        return f"{name} 的公开资料有限，部分细节可能需要结合原始报告进一步确认。"
    return f"{name} 的公开资料有限。"


def _infer_suitable_usage(task_type: str | None, evaluated_ability: list[str]) -> str:
    """Create a practical usage note when the model leaves it empty."""
    if task_type:
        return f"适合用于 {task_type} 的横向对比、课程讲解和研究分析。"
    if evaluated_ability:
        return f"适合用于围绕 {evaluated_ability[0]} 的调研、对比和课程展示。"
    return "适合用于 Benchmark 调研、对比和课程展示。"


def _load_prompt(path: Path) -> str:
    """Load prompt template from disk."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _extract_first_json_array(text: str) -> list[dict]:
    """
    Extract the first valid JSON array from mixed model output.

    Handles fenced blocks, prefixed/suffixed text, and thinking traces.
    """
    if not text or not text.strip():
        raise ValueError("Empty LLM response.")

    cleaned = text.strip()
    # Remove markdown code fences
    cleaned = re.sub(r"```(?:json)?", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.replace("```", "")

    decoder = json.JSONDecoder()
    for match in re.finditer(r"\[", cleaned):
        start = match.start()
        try:
            parsed, _ = decoder.raw_decode(cleaned[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, list):
            return parsed
    raise ValueError("No valid JSON array found in model output.")


def _normalize_benchmark_dict(data: dict, topic: str | None = None, report_urls: list[str] | None = None) -> dict:
    """Normalize and validate extracted benchmark data."""
    # Ensure required fields exist
    if "name" not in data or not data.get("name"):
        data["name"] = data.get("name", "Unknown Benchmark")
    
    if "task_type" not in data:
        data["task_type"] = None
    
    # Normalize list fields
    for field in ["evaluated_ability", "metrics", "evidence"]:
        if field not in data or not isinstance(data[field], list):
            data[field] = []

    data["evaluated_ability"] = _dedupe_strings([str(item) for item in data["evaluated_ability"] if item is not None])
    data["metrics"] = _dedupe_strings([str(item) for item in data["metrics"] if item is not None])
    data["evidence"] = _dedupe_strings([str(item) for item in data["evidence"] if item is not None])
    
    # Normalize integer score fields (1-5)
    for field in [
        "resource_completeness",
        "reproduction_difficulty",
        "teaching_value",
        "research_value",
        "topic_popularity",
        "time_cost_friendliness",
        "documentation_quality",
        "authority",
    ]:
        if field not in data:
            data[field] = 3
        else:
            try:
                score = int(data[field])
                data[field] = min(max(score, 1), 5)
            except (TypeError, ValueError):
                data[field] = 3
    
    # Normalize boolean field
    if "open_source" not in data:
        data["open_source"] = None
    elif isinstance(data["open_source"], str):
        data["open_source"] = data["open_source"].lower() in {"true", "yes", "1"}
    
    # Normalize optional text fields
    for field in ["description", "limitations", "suitable_usage"]:
        if field not in data or data[field] is None:
            data[field] = None
        else:
            text = str(data[field]).strip()
            if text.lower() in {"null", "none", "n/a", "未找到"}:
                data[field] = None
            else:
                data[field] = text.replace("\n", " ")

    if not data.get("description"):
        data["description"] = _infer_description(data["name"], data.get("task_type"), data["evaluated_ability"])

    if not data.get("metrics"):
        data["metrics"] = _infer_metrics(data["name"], data.get("task_type"), data["evaluated_ability"])

    if data.get("open_source") is None:
        has_code = bool(data.get("code_url")) and "github.com" in str(data.get("code_url"))
        data["open_source"] = has_code

    if not data.get("limitations"):
        data["limitations"] = _infer_limitations(data["name"], data.get("task_type"), data["evidence"])

    if not data.get("suitable_usage"):
        data["suitable_usage"] = _infer_suitable_usage(data.get("task_type"), data["evaluated_ability"])
    
    # Normalize URL fields
    for field in ["paper_url", "code_url", "dataset_url", "leaderboard_url"]:
        if field not in data or data[field] is None:
            data[field] = None
        else:
            url = str(data[field]).strip()
            if url.startswith("http://") or url.startswith("https://"):
                data[field] = url
            else:
                data[field] = None

    if not data["evidence"]:
        evidence_candidates = [data.get("paper_url"), data.get("code_url"), data.get("dataset_url"), data.get("leaderboard_url")]
        if report_urls:
            evidence_candidates.extend(report_urls)
        data["evidence"] = _dedupe_strings([url for url in evidence_candidates if url])
    
    return data


def _fallback_benchmarks(topic: str) -> list[Benchmark]:
    """
    Fallback when LLM extraction fails.
    
    Returns a curated set of benchmark templates with real evidence links.
    These are based on topic keywords and include authentic paper/code URLs.
    """
    fallback_map = {
        "agent": [
            Benchmark(
                name="AgentBench",
                task_type="Agent Evaluation",
                evaluated_ability=["task planning", "tool use", "reasoning"],
                paper_url="https://arxiv.org/abs/2308.03688",
                code_url="https://github.com/THUDM/AgentBench",
                resource_completeness=4,
                authority=5,
                research_value=5,
                evidence=["https://arxiv.org/abs/2308.03688", "https://github.com/THUDM/AgentBench"],
            ),
            Benchmark(
                name="WebArena",
                task_type="Web Navigation Agent Evaluation",
                evaluated_ability=["web navigation", "tool use", "long-horizon planning"],
                paper_url="https://arxiv.org/abs/2307.13854",
                code_url="https://github.com/web-arena-x/webarena",
                leaderboard_url="https://webarena.dev/",
                resource_completeness=4,
                authority=5,
                research_value=5,
                evidence=["https://arxiv.org/abs/2307.13854", "https://github.com/web-arena-x/webarena", "https://webarena.dev/"],
            ),
            Benchmark(
                name="OSWorld",
                task_type="Computer-use Agent Evaluation",
                evaluated_ability=["GUI operation", "desktop task solving", "OS interaction"],
                paper_url="https://arxiv.org/abs/2404.07972",
                code_url="https://github.com/xlang-ai/OSWorld",
                leaderboard_url="https://os-world.github.io/",
                resource_completeness=4,
                authority=5,
                research_value=5,
                evidence=["https://arxiv.org/abs/2404.07972", "https://github.com/xlang-ai/OSWorld", "https://os-world.github.io/"],
            ),
            Benchmark(
                name="GAIA",
                task_type="General Assistant / Agent Evaluation",
                evaluated_ability=["reasoning", "web browsing", "tool use", "multi-step planning"],
                paper_url="https://arxiv.org/abs/2311.12983",
                dataset_url="https://huggingface.co/datasets/gaia-benchmark/GAIA",
                leaderboard_url="https://huggingface.co/spaces/gaia-benchmark/leaderboard",
                resource_completeness=4,
                authority=5,
                research_value=4,
                evidence=["https://arxiv.org/abs/2311.12983", "https://huggingface.co/datasets/gaia-benchmark/GAIA"],
            ),
            Benchmark(
                name="SWE-bench",
                task_type="Software Engineering Agent Evaluation",
                evaluated_ability=["issue resolution", "patch generation", "code understanding"],
                paper_url="https://arxiv.org/abs/2310.06770",
                code_url="https://github.com/swe-bench/SWE-bench",
                leaderboard_url="https://www.swebench.com/",
                resource_completeness=4,
                authority=5,
                research_value=5,
                evidence=["https://arxiv.org/abs/2310.06770", "https://github.com/swe-bench/SWE-bench", "https://www.swebench.com/"],
            ),
            Benchmark(
                name="ToolBench",
                task_type="Tool-use Agent Evaluation",
                evaluated_ability=["tool calling", "API understanding", "parameter binding"],
                paper_url="https://arxiv.org/abs/2307.16490",
                code_url="https://github.com/OpenBMB/ToolBench",
                leaderboard_url="https://toolbench.opencompass.org.cn/",
                resource_completeness=4,
                authority=4,
                research_value=4,
                evidence=["https://arxiv.org/abs/2307.16490", "https://github.com/OpenBMB/ToolBench"],
            ),
        ],
        "rag": [
            Benchmark(
                name="RAGAS",
                task_type="RAG Evaluation",
                evaluated_ability=["retrieval", "generation", "relevance assessment"],
                code_url="https://github.com/explodinggradients/ragas",
                resource_completeness=4,
                authority=4,
                research_value=4,
                evidence=["https://github.com/explodinggradients/ragas"],
            ),
            Benchmark(
                name="BEIR",
                task_type="Information Retrieval Evaluation",
                evaluated_ability=["retrieval", "ranking", "document relevance"],
                paper_url="https://arxiv.org/abs/2104.08663",
                code_url="https://github.com/beir-cellar/beir",
                resource_completeness=4,
                authority=5,
                research_value=5,
                evidence=["https://arxiv.org/abs/2104.08663", "https://github.com/beir-cellar/beir"],
            ),
            Benchmark(
                name="MIRACL",
                task_type="Multilingual Retrieval Evaluation",
                evaluated_ability=["multilingual retrieval", "cross-lingual ranking"],
                paper_url="https://arxiv.org/abs/2210.09520",
                code_url="https://github.com/project-miracl/miracl",
                resource_completeness=4,
                authority=4,
                research_value=4,
                evidence=["https://arxiv.org/abs/2210.09520", "https://github.com/project-miracl/miracl"],
            ),
            Benchmark(
                name="KILT",
                task_type="Knowledge-Intensive Evaluation",
                evaluated_ability=["retrieval", "knowledge integration", "QA"],
                paper_url="https://arxiv.org/abs/2104.07143",
                code_url="https://github.com/facebookresearch/KILT",
                resource_completeness=4,
                authority=5,
                research_value=4,
                evidence=["https://arxiv.org/abs/2104.07143", "https://github.com/facebookresearch/KILT"],
            ),
            Benchmark(
                name="HotpotQA",
                task_type="Multi-hop QA Evaluation",
                evaluated_ability=["multi-hop reasoning", "retrieval", "QA"],
                paper_url="https://arxiv.org/abs/1809.02776",
                code_url="https://github.com/hotpotqa/hotpot",
                resource_completeness=4,
                authority=5,
                research_value=4,
                evidence=["https://arxiv.org/abs/1809.02776", "https://github.com/hotpotqa/hotpot"],
            ),
        ],
        "tool": [
            Benchmark(
                name="ToolBench",
                task_type="Tool Use",
                evaluated_ability=["tool calling", "API understanding"],
                paper_url="https://arxiv.org/abs/2307.16490",
                code_url="https://github.com/OpenBMB/ToolBench",
                resource_completeness=4,
                authority=4,
                research_value=4,
                evidence=["https://arxiv.org/abs/2307.16490", "https://github.com/OpenBMB/ToolBench"],
            ),
            Benchmark(
                name="APIBank",
                task_type="API Calling Evaluation",
                evaluated_ability=["api selection", "tool use", "parameter understanding"],
                paper_url="https://arxiv.org/abs/2304.08244",
                code_url="https://github.com/AlibabaResearch/APIBank",
                resource_completeness=3,
                authority=4,
                research_value=3,
                evidence=["https://arxiv.org/abs/2304.08244", "https://github.com/AlibabaResearch/APIBank"],
            ),
            Benchmark(
                name="BFCL",
                task_type="Function Calling Evaluation",
                evaluated_ability=["function calling", "parameter binding"],
                paper_url="https://arxiv.org/abs/2404.16151",
                code_url="https://github.com/ShishirPatil/gorilla",
                resource_completeness=4,
                authority=4,
                research_value=4,
                evidence=["https://arxiv.org/abs/2404.16151", "https://github.com/ShishirPatil/gorilla"],
            ),
            Benchmark(
                name="Gorilla",
                task_type="Tool/API Use Evaluation",
                evaluated_ability=["api invocation", "tool selection", "function calling"],
                paper_url="https://arxiv.org/abs/2305.15334",
                code_url="https://github.com/ShishirPatil/gorilla",
                leaderboard_url="https://gorilla.cs.berkeley.edu/",
                resource_completeness=4,
                authority=4,
                research_value=4,
                evidence=["https://arxiv.org/abs/2305.15334", "https://github.com/ShishirPatil/gorilla"],
            ),
            Benchmark(
                name="HuggingGPT",
                task_type="Tool Orchestration Evaluation",
                evaluated_ability=["planning", "tool orchestration", "task decomposition"],
                paper_url="https://arxiv.org/abs/2303.17580",
                code_url="https://github.com/microsoft/JARVIS",
                resource_completeness=3,
                authority=4,
                research_value=4,
                evidence=["https://arxiv.org/abs/2303.17580", "https://github.com/microsoft/JARVIS"],
            ),
        ],
    }

    topic_lower = topic.lower()
    selected = None
    for keyword, benchmarks in fallback_map.items():
        if keyword in topic_lower:
            selected = benchmarks
            break

    if selected is None:
        # Generic fallback with real-world benchmarks
        selected = [
            Benchmark(
                name="AgentBench",
                task_type="Agent Evaluation",
                evaluated_ability=["task planning", "tool use"],
                paper_url="https://arxiv.org/abs/2308.03688",
                code_url="https://github.com/THUDM/AgentBench",
                resource_completeness=4,
                authority=5,
                evidence=["https://arxiv.org/abs/2308.03688", "https://github.com/THUDM/AgentBench"],
            ),
            Benchmark(
                name="WebArena",
                task_type="Web Navigation",
                evaluated_ability=["web interaction", "tool use"],
                paper_url="https://arxiv.org/abs/2307.13854",
                code_url="https://github.com/web-arena-x/webarena",
                resource_completeness=4,
                authority=5,
                evidence=["https://arxiv.org/abs/2307.13854", "https://github.com/web-arena-x/webarena"],
            ),
            Benchmark(
                name="GAIA",
                task_type="General Assistant Evaluation",
                evaluated_ability=["reasoning", "web browsing", "tool use"],
                paper_url="https://arxiv.org/abs/2311.12983",
                dataset_url="https://huggingface.co/datasets/gaia-benchmark/GAIA",
                resource_completeness=4,
                authority=5,
                evidence=["https://arxiv.org/abs/2311.12983", "https://huggingface.co/datasets/gaia-benchmark/GAIA"],
            ),
            Benchmark(
                name="SWE-bench",
                task_type="Software Engineering",
                evaluated_ability=["issue resolution", "code generation"],
                paper_url="https://arxiv.org/abs/2310.06770",
                code_url="https://github.com/swe-bench/SWE-bench",
                resource_completeness=4,
                authority=5,
                evidence=["https://arxiv.org/abs/2310.06770", "https://github.com/swe-bench/SWE-bench"],
            ),
            Benchmark(
                name="RAGAS",
                task_type="RAG Evaluation",
                evaluated_ability=["retrieval", "generation"],
                code_url="https://github.com/explodinggradients/ragas",
                resource_completeness=4,
                authority=4,
                evidence=["https://github.com/explodinggradients/ragas"],
            ),
        ]

    normalized = []
    for benchmark in selected[:MAX_BENCHMARKS]:
        normalized.append(Benchmark(**_normalize_benchmark_dict(benchmark.model_dump(), topic=topic)))
    return normalized


def extract_benchmarks(raw_report: str, topic: str) -> list[Benchmark]:
    """
    Extract structured Benchmark information from raw report.

    Args:
        raw_report: Raw research report markdown
        topic: Research topic

    Returns:
        List of Benchmark objects
    """
    if not raw_report or not raw_report.strip():
        return _fallback_benchmarks(topic)

    report_urls = _extract_urls_from_text(raw_report)
    
    # Load prompt template
    try:
        prompt_template = _load_prompt(EXTRACTOR_PROMPT_PATH)
    except FileNotFoundError:
        # If prompt file doesn't exist, use fallback
        return _fallback_benchmarks(topic)
    
    # Format prompt with topic and report
    prompt = prompt_template.format(
        topic=topic,
        raw_report=raw_report[:8000],  # Limit report length to avoid token overflow
    )
    
    # Call LLM
    try:
        response = call_llm(
            prompt=prompt,
            max_tokens=8192,
            json_mode=True,
        )
    except Exception as e:
        print(f"LLM call failed: {e}")
        return _fallback_benchmarks(topic)
    
    # Extract JSON array
    try:
        benchmarks_data = _extract_first_json_array(response)
    except ValueError as e:
        print(f"JSON extraction failed: {e}")
        return _fallback_benchmarks(topic)
    
    # Validate minimum count
    if not benchmarks_data or len(benchmarks_data) < MIN_BENCHMARKS:
        print(f"Extracted {len(benchmarks_data)} benchmarks, minimum {MIN_BENCHMARKS} required")
        return _fallback_benchmarks(topic)
    
    # Normalize and convert to Benchmark objects
    benchmarks = []
    for i, item in enumerate(benchmarks_data[:MAX_BENCHMARKS]):
        try:
            normalized = _normalize_benchmark_dict(item, topic=topic, report_urls=report_urls)
            benchmark = Benchmark(**normalized)
            benchmarks.append(benchmark)
        except Exception as e:
            print(f"Failed to parse benchmark {i}: {e}")
            continue
    
    # Return extracted benchmarks or fallback if too few
    if benchmarks:
        return benchmarks
    else:
        return _fallback_benchmarks(topic)
