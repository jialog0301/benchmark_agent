"""Benchmark Extractor module."""

from src.schemas import Benchmark


def extract_benchmarks(raw_report: str, topic: str) -> list[Benchmark]:
    """
    Extract structured Benchmark information from raw report.

    Args:
        raw_report: Raw research report markdown
        topic: Research topic

    Returns:
        List of Benchmark objects
    """
    # TODO: Implement with LLM + JSON parsing
    return []
