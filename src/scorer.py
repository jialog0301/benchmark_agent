"""Task-Fit Scorer module."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .schemas import RankedBenchmark

SCORE_FIELDS = {
    "resource_completeness",
    "reproduction_difficulty",
    "teaching_value",
    "research_value",
    "topic_popularity",
    "time_cost_friendliness",
    "documentation_quality",
    "authority",
}


def _score(value: Any, default: int = 3) -> int:
    """Convert a score-like value to an integer in [1, 5]."""
    try:
        score = int(value)
    except (TypeError, ValueError):
        score = default
    return min(max(score, 1), 5)


def _coverage_score(benchmark: dict) -> int:
    """
    Estimate coverage from evaluated_ability count.

    The requirement allows using evaluated_ability count when no explicit
    coverage field exists. Clamp to the same 1-5 scale as other dimensions.
    """
    abilities = benchmark.get("evaluated_ability", [])
    if isinstance(abilities, str):
        abilities = [abilities]
    if not isinstance(abilities, list):
        abilities = []
    return min(max(len([item for item in abilities if str(item).strip()]), 1), 5)


def _calculate_task_fit_score(benchmark: dict, mode: str) -> float:
    """Calculate Task-Fit Score for a benchmark under the selected mode."""
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
        coverage = _coverage_score(benchmark)
        score = (
            0.30 * research
            + 0.25 * authority
            + 0.20 * popularity
            + 0.15 * resource
            + 0.10 * coverage
        )
    elif "快速复现" in mode:
        score = (
            0.35 * reproduction_friendliness
            + 0.25 * resource
            + 0.20 * documentation
            + 0.15 * time_cost
            + 0.05 * popularity
        )
    else:
        score = (
            0.30 * teaching
            + 0.25 * resource
            + 0.20 * reproduction_friendliness
            + 0.15 * popularity
            + 0.10 * time_cost
        )

    return round(score, 2)


def _ranking_tiebreaker(benchmark: dict) -> tuple:
    """Stable tie-breaker that favors practical, complete resources."""
    return (
        -_score(benchmark.get("resource_completeness")),
        -(6 - _score(benchmark.get("reproduction_difficulty"))),
        -_score(benchmark.get("documentation_quality")),
        -_score(benchmark.get("authority")),
        benchmark.get("_original_index", 0),
    )


def _normalize_benchmark(benchmark: dict) -> dict:
    """Preserve input fields while normalizing score fields for validation."""
    normalized = deepcopy(benchmark)
    for field in SCORE_FIELDS:
        normalized[field] = _score(normalized.get(field))
    for field in ["evaluated_ability", "metrics", "evidence"]:
        value = normalized.get(field, [])
        if isinstance(value, list):
            normalized[field] = value
        elif value is None:
            normalized[field] = []
        else:
            normalized[field] = [str(value)]
    return normalized


def score_benchmarks(benchmarks: list[dict], mode: str) -> list[dict]:
    """
    Calculate Task-Fit Score and rank benchmarks.

    Args:
        benchmarks: List of Benchmark dicts
        mode: Recommendation mode (课程实验/科研调研/快速复现)

    Returns:
        List of ranked benchmarks with task_fit_score
    """
    scored: list[dict] = []
    for original_index, benchmark in enumerate(benchmarks or []):
        if not isinstance(benchmark, dict):
            if hasattr(benchmark, "model_dump"):
                benchmark = benchmark.model_dump()
            else:
                continue

        item = _normalize_benchmark(benchmark)
        item["_original_index"] = original_index
        item["mode"] = mode
        item["task_fit_score"] = _calculate_task_fit_score(item, mode)
        scored.append(item)

    scored.sort(
        key=lambda item: (
            -item["task_fit_score"],
            *_ranking_tiebreaker(item),
        ),
    )

    ranked: list[dict] = []
    for index, item in enumerate(scored, start=1):
        item["rank"] = index
        item.pop("_original_index", None)
        ranked_item = RankedBenchmark.model_validate(item).model_dump()
        ranked.append(ranked_item)

    return ranked
