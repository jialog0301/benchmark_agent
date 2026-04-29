"""Main pipeline orchestration for BenchmarkRadarAgent."""

from .cache import load_cache, save_cache


def run_benchmark_radar(topic: str, mode: str, use_cache: bool = True) -> dict:
    """
    Main pipeline: planner → searcher → extractor → scorer → judge → reporter

    Args:
        topic: Research topic (e.g., "AI Agent Evaluation Benchmark")
        mode: Recommendation mode (课程实验/科研调研/快速复现)
        use_cache: Whether to use cached data when available

    Returns:
        dict with keys: topic, mode, plan, raw_report, benchmarks, ranked_benchmarks, final_report
    """
    # Import here to avoid circular imports; modules B-E will implement these
    from . import planner, searcher, extractor, scorer, judge, reporter

    result = {"topic": topic, "mode": mode}

    # Step 1: Planner
    if use_cache:
        plan = load_cache(topic, "planner_result.json")
    else:
        plan = None

    if plan is None:
        plan = planner.plan_queries(topic, mode)
        save_cache(topic, "planner_result.json", plan)

    result["plan"] = plan

    # Step 2: Searcher
    if use_cache:
        raw_report = load_cache(topic, "raw_report.md")
    else:
        raw_report = None

    if raw_report is None:
        raw_report = searcher.run_research(topic, plan)
        save_cache(topic, "raw_report.md", raw_report)

    result["raw_report"] = raw_report

    # Step 3: Extractor
    if use_cache:
        benchmarks = load_cache(topic, "benchmarks.json")
    else:
        benchmarks = None

    if benchmarks is None:
        benchmarks = extractor.extract_benchmarks(raw_report, topic)
        # Convert to list of dicts for JSON serialization
        benchmarks = [b.model_dump() if hasattr(b, "model_dump") else b for b in benchmarks]
        save_cache(topic, "benchmarks.json", benchmarks)

    result["benchmarks"] = benchmarks

    # Step 4: Scorer
    if use_cache:
        ranked_benchmarks = load_cache(topic, "ranked_benchmarks.json")
    else:
        ranked_benchmarks = None

    if ranked_benchmarks is None:
        ranked_benchmarks = scorer.score_benchmarks(benchmarks, mode)
        save_cache(topic, "ranked_benchmarks.json", ranked_benchmarks)

    result["ranked_benchmarks"] = ranked_benchmarks

    # Step 5: Judge - generate recommendation reasons
    ranked_benchmarks = result["ranked_benchmarks"]
    for bm in ranked_benchmarks:
        if not bm.get("recommendation_reason"):
            reason = judge.generate_recommendation_reason(bm, mode)
            bm["recommendation_reason"] = reason
    save_cache(topic, "ranked_benchmarks.json", ranked_benchmarks)
    result["ranked_benchmarks"] = ranked_benchmarks

    # Step 6: Reporter
    if use_cache:
        final_report = load_cache(topic, "final_report.md")
    else:
        final_report = None

    if final_report is None:
        final_report = reporter.generate_report(topic, mode, ranked_benchmarks)
        save_cache(topic, "final_report.md", final_report)

    result["final_report"] = final_report

    return result
