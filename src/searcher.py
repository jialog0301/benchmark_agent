"""Search Agent module."""

import os


def run_research(topic: str, plan: dict) -> str:
    """
    Execute web research based on search plan.

    Args:
        topic: Research topic
        plan: Search plan from planner

    Returns:
        Raw research report as markdown string
    """
    # TODO: Implement with Search API / GPT Researcher
    # Falls back to cached raw_report.md if available
    return f"# {topic} Research Report\n\n(TODO: Implement search agent)"
