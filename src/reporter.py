"""Report Writer module."""


def generate_report(topic: str, mode: str, ranked_benchmarks: list[dict]) -> str:
    """
    Generate final Markdown report.

    Args:
        topic: Research topic
        mode: Recommendation mode
        ranked_benchmarks: List of ranked benchmarks

    Returns:
        Markdown report string
    """
    # TODO: Implement report generation
    return f"# BenchmarkRadar Report: {topic}\n\n## 推荐模式：{mode}\n\n(TODO: Generate report)"
