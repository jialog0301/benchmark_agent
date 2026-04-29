"""Query Planner module."""

from src.schemas import PlanResult


def plan_queries(topic: str, mode: str) -> dict:
    """
    Generate search plan based on topic and mode.

    Args:
        topic: Research topic
        mode: Recommendation mode (课程实验/科研调研/快速复现)

    Returns:
        dict with search_goals, search_queries, expected_outputs
    """
    # TODO: Implement with LLM
    return {
        "topic": topic,
        "mode": mode,
        "search_goals": [],
        "search_queries": [],
        "expected_outputs": []
    }
