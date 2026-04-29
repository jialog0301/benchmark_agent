"""Pydantic schemas for BenchmarkRadarAgent."""

from pydantic import BaseModel, Field


class Benchmark(BaseModel):
    """Structured Benchmark information."""

    name: str
    description: str | None = None
    task_type: str | None = None
    evaluated_ability: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)
    paper_url: str | None = None
    code_url: str | None = None
    dataset_url: str | None = None
    leaderboard_url: str | None = None
    open_source: bool | None = None
    resource_completeness: int = 3  # 1-5
    reproduction_difficulty: int = 3  # 1-5, higher = harder
    teaching_value: int = 3  # 1-5
    research_value: int = 3  # 1-5
    topic_popularity: int = 3  # 1-5
    time_cost_friendliness: int = 3  # 1-5
    documentation_quality: int = 3  # 1-5
    authority: int = 3  # 1-5
    limitations: str | None = None
    suitable_usage: str | None = None
    evidence: list[str] = Field(default_factory=list)


class RankedBenchmark(Benchmark):
    """Benchmark with Task-Fit Score ranking."""

    mode: str
    task_fit_score: float = Field(ge=0, le=5)
    rank: int
    recommendation_reason: str | None = None


class PlanResult(BaseModel):
    """Query Planner output."""

    topic: str
    mode: str
    search_goals: list[str] = Field(default_factory=list)
    search_queries: list[str] = Field(default_factory=list)
    expected_outputs: list[str] = Field(default_factory=list)


class PipelineResult(BaseModel):
    """Full pipeline output."""

    topic: str
    mode: str
    plan: dict | None = None
    raw_report: str | None = None
    benchmarks: list[dict] = Field(default_factory=list)
    ranked_benchmarks: list[dict] = Field(default_factory=list)
    final_report: str | None = None
