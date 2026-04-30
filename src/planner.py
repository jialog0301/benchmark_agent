"""Query Planner module."""

from __future__ import annotations

import json
import re
from pathlib import Path

from src.llm_client import call_llm
from src.schemas import PlanResult

BASE_DIR = Path(__file__).resolve().parent.parent
PLANNER_PROMPT_PATH = BASE_DIR / "prompts" / "planner.md"

MIN_GOALS = 5
MIN_QUERIES = 5
MIN_EXPECTED_OUTPUTS = 4


def _load_prompt(path: Path) -> str:
    """Load prompt template from disk."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _extract_first_json_object(text: str) -> dict:
    """
    Extract the first valid JSON object from mixed model output.

    Handles fenced blocks, prefixed/suffixed text, and thinking traces.
    """
    if not text or not text.strip():
        raise ValueError("Empty LLM response.")

    cleaned = text.strip()
    cleaned = re.sub(r"```(?:json)?", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.replace("```", "")

    decoder = json.JSONDecoder()
    for match in re.finditer(r"\{", cleaned):
        start = match.start()
        try:
            parsed, _ = decoder.raw_decode(cleaned[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    raise ValueError("No valid JSON object found in model output.")


def _mode_profile(mode: str) -> tuple[list[str], list[str]]:
    """Return mode-specific goals and queries."""
    mode_text = mode.strip()

    if "课程实验" in mode_text:
        goals = [
            "评估各候选 benchmark 的教学价值与课堂可讲解性",
            "比较资源完整度（文档、代码、数据、示例）",
            "判断复现友好度和环境部署复杂度",
            "估算在课程周期内完成实验的时间成本",
            "识别适合学生分组实验与结果复核的评测方案",
        ]
        queries = [
            "teaching friendly benchmark tutorial reproducibility",
            "benchmark documentation setup guide student project",
            "benchmark quick demo time cost reproducible experiment",
        ]
        return goals, queries

    if "科研调研" in mode_text:
        goals = [
            "检索该方向的代表性论文与高引用 benchmark",
            "梳理权威榜单、官方评测站点和公开 leaderboard",
            "比较 benchmark 的任务覆盖范围与指标体系",
            "收集 survey 或综述中常被引用的评测框架",
            "识别近两年的新 benchmark 与研究趋势",
        ]
        queries = [
            "benchmark survey authoritative leaderboard paper",
            "arxiv benchmark state of the art evaluation",
            "benchmark coverage metrics taxonomy comparison",
        ]
        return goals, queries

    if "快速复现" in mode_text:
        goals = [
            "优先查找可直接运行的开源实现与 quickstart",
            "确认数据集可获取性与下载门槛",
            "比较部署依赖、环境复杂度与运行成本",
            "筛选文档清晰且示例完整的 benchmark 项目",
            "评估短时间内完成端到端复现的可行性",
        ]
        queries = [
            "GitHub open source benchmark quickstart",
            "benchmark install run example reproducible",
            "benchmark dataset availability download open access",
        ]
        return goals, queries

    goals = [
        "梳理主题相关 benchmark 的代表性候选",
        "收集论文、代码、数据集与 leaderboard 入口",
        "总结评测任务、能力维度与核心指标",
        "比较资源完整度与复现门槛",
        "形成可用于后续抽取与评分的原始事实依据",
    ]
    queries = [
        "benchmark paper GitHub leaderboard",
        "evaluation benchmark dataset metrics comparison",
        "benchmark survey open source implementation",
    ]
    return goals, queries


def _unique_keep_order(items: list[str]) -> list[str]:
    """Deduplicate strings while preserving order."""
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        text = str(item).strip()
        if not text:
            continue
        if text in seen:
            continue
        seen.add(text)
        output.append(text)
    return output


def _fallback_plan(topic: str, mode: str) -> dict:
    """Generate deterministic fallback plan for any topic."""
    base_goals = [
        f"梳理 {topic} 相关 benchmark 的代表性候选",
        "收集每个 benchmark 的论文、代码、数据集和 leaderboard 入口",
        "总结各 benchmark 的评测任务、能力维度和关键指标",
        "比较资源完整度、文档质量与复现门槛",
        "提炼适用于后续结构化抽取的证据链接集合",
    ]
    base_queries = [
        f"{topic} benchmark paper GitHub leaderboard",
        f"{topic} evaluation benchmark dataset metrics",
        f"{topic} benchmark survey comparison",
        f"{topic} GitHub open source implementation",
        f"{topic} arxiv benchmark 2024 2025",
    ]
    mode_goals, mode_queries = _mode_profile(mode)

    goals = _unique_keep_order(base_goals + mode_goals)
    queries = _unique_keep_order(base_queries + [f"{topic} {q}" for q in mode_queries])

    expected_outputs = [
        "Benchmark candidate list with evidence links",
        "Structured fields for extractor (task, metric, urls, resource clues)",
        "初步的资源完整度与复现难度判断依据",
        "可供后续评分模块使用的事实型调研摘要",
    ]

    if len(goals) < MIN_GOALS:
        goals.extend([f"补充目标 {i}" for i in range(1, MIN_GOALS - len(goals) + 1)])
    if len(queries) < MIN_QUERIES:
        queries.extend(
            [f"{topic} benchmark query {i}" for i in range(1, MIN_QUERIES - len(queries) + 1)]
        )
    if len(expected_outputs) < MIN_EXPECTED_OUTPUTS:
        expected_outputs.extend(
            [f"expected_output_{i}" for i in range(1, MIN_EXPECTED_OUTPUTS - len(expected_outputs) + 1)]
        )

    return {
        "topic": topic,
        "mode": mode,
        "search_goals": goals[:8],
        "search_queries": queries[:8],
        "expected_outputs": expected_outputs[:6],
    }


def _normalize_and_validate_plan(candidate: dict, topic: str, mode: str) -> dict:
    """Validate plan schema and enforce minimum required counts."""
    fallback = _fallback_plan(topic, mode)
    merged = {
        "topic": topic,
        "mode": mode,
        "search_goals": candidate.get("search_goals", []),
        "search_queries": candidate.get("search_queries", []),
        "expected_outputs": candidate.get("expected_outputs", []),
    }

    validated = PlanResult.model_validate(merged).model_dump()
    validated["topic"] = topic
    validated["mode"] = mode

    validated["search_goals"] = _unique_keep_order(validated.get("search_goals", []))
    validated["search_queries"] = _unique_keep_order(validated.get("search_queries", []))
    validated["expected_outputs"] = _unique_keep_order(validated.get("expected_outputs", []))

    if len(validated["search_goals"]) < MIN_GOALS:
        validated["search_goals"] = _unique_keep_order(
            validated["search_goals"] + fallback["search_goals"]
        )
    if len(validated["search_queries"]) < MIN_QUERIES:
        validated["search_queries"] = _unique_keep_order(
            validated["search_queries"] + fallback["search_queries"]
        )
    if len(validated["expected_outputs"]) < MIN_EXPECTED_OUTPUTS:
        validated["expected_outputs"] = _unique_keep_order(
            validated["expected_outputs"] + fallback["expected_outputs"]
        )

    validated["search_goals"] = validated["search_goals"][:8]
    validated["search_queries"] = validated["search_queries"][:8]
    validated["expected_outputs"] = validated["expected_outputs"][:6]
    return validated


def plan_queries(topic: str, mode: str) -> dict:
    """
    Generate search plan based on topic and mode.

    Args:
        topic: Research topic
        mode: Recommendation mode (课程实验/科研调研/快速复现)

    Returns:
        dict with search_goals, search_queries, expected_outputs.
    """
    topic = (topic or "").strip()
    mode = (mode or "").strip()
    if not topic:
        topic = "AI Benchmark"
    if not mode:
        mode = "课程实验"

    fallback = _fallback_plan(topic, mode)

    try:
        template = _load_prompt(PLANNER_PROMPT_PATH)
        prompt = template.format(topic=topic, mode=mode)
    except Exception:
        return fallback

    try:
        llm_response = call_llm(prompt, json_mode=True)
        parsed = _extract_first_json_object(llm_response)
        return _normalize_and_validate_plan(parsed, topic, mode)
    except Exception:
        return fallback
