"""Main pipeline orchestration for BenchmarkRadarAgent."""

from typing import Any, Callable

from .cache import load_cache, save_cache

ProgressCallback = Callable[[str, dict[str, Any]], None]


def _noop_callback(step: str, data: dict[str, Any]) -> None:
    """Default no-op progress callback."""


def _extract_thinking(response_text: str) -> tuple[str, str]:
    """Split LLM response into (thinking, answer) parts."""
    thinking_lines: list[str] = []
    answer_lines: list[str] = []
    for line in response_text.split("\n"):
        if line.startswith("[Thinking]:"):
            thinking_lines.append(line[len("[Thinking]:"):].strip())
        else:
            answer_lines.append(line)
    return "\n".join(thinking_lines), "\n".join(answer_lines).strip()


def run_benchmark_radar(
    topic: str,
    mode: str,
    use_cache: bool = True,
    progress_callback: ProgressCallback | None = None,
) -> dict:
    """
    Main pipeline: planner → searcher → extractor → scorer → judge → reporter

    Args:
        topic: Research topic (e.g., "AI Agent Evaluation Benchmark")
        mode: Recommendation mode (课程实验/科研调研/快速复现)
        use_cache: Whether to use cached data when available
        progress_callback: Optional callback(step, data) for real-time progress

    Returns:
        dict with keys: topic, mode, plan, raw_report, benchmarks, ranked_benchmarks, final_report
    """
    from . import planner, searcher, extractor, scorer, judge, reporter

    on = progress_callback or _noop_callback
    result: dict[str, Any] = {"topic": topic, "mode": mode}

    # ---- Step 1: Planner ----
    on("planner", {"status": "running"})

    if use_cache:
        plan = load_cache(topic, "planner_result.json")
    else:
        plan = None

    if plan is None:
        plan = planner.plan_queries(topic, mode)
        save_cache(topic, "planner_result.json", plan)

    result["plan"] = plan
    on("planner", {"status": "done", "plan": plan})

    # ---- Step 2: Searcher ----
    on("search", {"status": "running"})

    if use_cache:
        raw_report = load_cache(topic, "raw_report.md")
    else:
        raw_report = None

    if raw_report is None:
        raw_report = searcher.run_research(topic, plan)
        save_cache(topic, "raw_report.md", raw_report)

    result["raw_report"] = raw_report
    # Extract candidate count from raw report (count "### Benchmark X:" headers)
    import re
    candidate_count = len(re.findall(r"### Benchmark \d+:", raw_report or ""))
    on("search", {"status": "done", "candidate_count": candidate_count})

    # ---- Step 3: Extractor ----
    on("extract", {"status": "running"})

    if use_cache:
        benchmarks = load_cache(topic, "benchmarks.json")
    else:
        benchmarks = None

    if benchmarks is None:
        benchmarks = extractor.extract_benchmarks(raw_report, topic)
        benchmarks = [b.model_dump() if hasattr(b, "model_dump") else b for b in benchmarks]
        save_cache(topic, "benchmarks.json", benchmarks)

    result["benchmarks"] = benchmarks
    bm_names = [b.get("name", "Unknown") for b in (benchmarks or [])]
    on("extract", {"status": "done", "benchmark_count": len(benchmarks or []), "benchmark_names": bm_names})

    # ---- Step 4: Scorer ----
    on("score", {"status": "running"})

    if use_cache:
        ranked_benchmarks = load_cache(topic, "ranked_benchmarks.json")
    else:
        ranked_benchmarks = None

    if ranked_benchmarks is None:
        ranked_benchmarks = scorer.score_benchmarks(benchmarks, mode)
        save_cache(topic, "ranked_benchmarks.json", ranked_benchmarks)

    result["ranked_benchmarks"] = ranked_benchmarks
    top_scores = [
        {"name": b.get("name", "?"), "score": b.get("task_fit_score", 0)}
        for b in (ranked_benchmarks or [])[:3]
    ]
    on("score", {"status": "done", "ranked_count": len(ranked_benchmarks or []), "top3": top_scores})

    # ---- Step 5: Judge ----
    on("judge", {"status": "running", "total": len(ranked_benchmarks or [])})

    ranked_benchmarks = result["ranked_benchmarks"]
    for i, bm in enumerate(ranked_benchmarks):
        if not bm.get("recommendation_reason"):
            on("judge", {"status": "progress", "current": i + 1, "total": len(ranked_benchmarks), "name": bm.get("name", "?")})
            reason = judge.generate_recommendation_reason(bm, mode)
            thinking, _ = _extract_thinking(reason)
            bm["recommendation_reason"] = reason
            on("judge", {
                "status": "item_done",
                "current": i + 1,
                "total": len(ranked_benchmarks),
                "name": bm.get("name", "?"),
                "score": bm.get("task_fit_score", 0),
                "thinking": thinking,
            })

    save_cache(topic, "ranked_benchmarks.json", ranked_benchmarks)
    result["ranked_benchmarks"] = ranked_benchmarks
    on("judge", {"status": "done"})

    # ---- Step 6: Reporter ----
    on("report", {"status": "running"})

    if use_cache:
        final_report = load_cache(topic, "final_report.md")
    else:
        final_report = None

    if final_report is None:
        final_report = reporter.generate_report(topic, mode, ranked_benchmarks)
        thinking, _ = _extract_thinking(final_report)
        save_cache(topic, "final_report.md", final_report)
        on("report", {"status": "done", "thinking": thinking})
    else:
        on("report", {"status": "done", "thinking": ""})

    result["final_report"] = final_report

    return result
