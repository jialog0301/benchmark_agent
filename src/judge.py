"""LLM Judge module - recommendation reason generation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .llm_client import call_llm

BASE_DIR = Path(__file__).resolve().parent.parent
JUDGE_PROMPT_PATH = BASE_DIR / "prompts" / "judge.md"


def _load_prompt(path: Path) -> str:
    """Load prompt template from disk."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _extract_first_json_object(text: str) -> dict:
    """Extract the first JSON object from mixed model output."""
    if not text or not text.strip():
        raise ValueError("Empty LLM response.")

    cleaned = text.strip()
    cleaned = re.sub(r"```(?:json)?", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.replace("```", "")

    decoder = json.JSONDecoder()
    for match in re.finditer(r"\{", cleaned):
        try:
            parsed, _ = decoder.raw_decode(cleaned[match.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    raise ValueError("No JSON object found in model output.")


def _score(value: Any, default: int = 3) -> int:
    """Convert a score-like value to an integer in [1, 5]."""
    try:
        score = int(value)
    except (TypeError, ValueError):
        score = default
    return min(max(score, 1), 5)


def _score_label(score: float) -> str:
    """Map a Task-Fit Score to a concise judgment phrase."""
    if score >= 4.0:
        return "很适合作为优先候选"
    if score >= 3.3:
        return "适合作为可选方案"
    if score >= 2.6:
        return "可以作为补充参考"
    return "不适合作为首选"


def _fallback_recommendation_reason(benchmark: dict, mode: str) -> str:
    """Generate a deterministic recommendation reason when LLM is unavailable."""
    name = str(benchmark.get("name") or "该 Benchmark")
    task_fit_score = float(benchmark.get("task_fit_score") or 0)
    rank = benchmark.get("rank")
    rank_text = f"当前排名第 {rank}，" if rank else ""

    resource = _score(benchmark.get("resource_completeness"))
    difficulty = _score(benchmark.get("reproduction_difficulty"))
    teaching = _score(benchmark.get("teaching_value"))
    research = _score(benchmark.get("research_value"))
    popularity = _score(benchmark.get("topic_popularity"))
    time_cost = _score(benchmark.get("time_cost_friendliness"))
    documentation = _score(benchmark.get("documentation_quality"))
    authority = _score(benchmark.get("authority"))
    reproduction_friendliness = 6 - difficulty

    if "科研调研" in mode:
        return (
            f"{name} 在{mode}下的 Task-Fit Score 为 {task_fit_score:.2f}，"
            f"{rank_text}{_score_label(task_fit_score)}。"
            f"它的科研价值为 {research}/5、权威性为 {authority}/5、方向热度为 {popularity}/5，"
            "适合用于 related work、代表性 Benchmark 梳理和横向对比。"
            f"需要注意资源完整度为 {resource}/5，若要深入复现实验，还应结合原始论文和代码进一步确认细节。"
        )

    if "快速复现" in mode:
        return (
            f"{name} 在{mode}下的 Task-Fit Score 为 {task_fit_score:.2f}，"
            f"{rank_text}{_score_label(task_fit_score)}。"
            f"它的复现友好度为 {reproduction_friendliness}/5、资源完整度为 {resource}/5、文档质量为 {documentation}/5，"
            "这些维度直接影响能否快速跑通 Demo。"
            f"如果时间成本友好度只有 {time_cost}/5，建议先确认数据、依赖和运行示例是否完整。"
        )

    return (
        f"{name} 在{mode}下的 Task-Fit Score 为 {task_fit_score:.2f}，"
        f"{rank_text}{_score_label(task_fit_score)}。"
        f"它的教学价值为 {teaching}/5、资源完整度为 {resource}/5、复现友好度为 {reproduction_friendliness}/5，"
        "这些指标决定了它是否适合课程作业、课堂展示和学生实验。"
        f"同时方向热度为 {popularity}/5、时间成本友好度为 {time_cost}/5，可作为安排实验周期时的参考。"
    )


def generate_recommendation_reason(benchmark: dict, mode: str) -> str:
    """
    Generate recommendation explanation for a benchmark.

    Args:
        benchmark: Benchmark dict with scores
        mode: Recommendation mode

    Returns:
        Recommendation reason string
    """
    fallback = _fallback_recommendation_reason(benchmark, mode)

    try:
        template = _load_prompt(JUDGE_PROMPT_PATH)
        prompt = template.format(
            benchmark=json.dumps(benchmark, ensure_ascii=False, indent=2),
            mode=mode,
        )
        response = call_llm(prompt, json_mode=True, max_tokens=800)
        parsed = _extract_first_json_object(response)
        reason = str(parsed.get("recommendation_reason", "")).strip()
        if reason:
            return reason
    except Exception:
        pass

    return fallback
