
"""Search Agent module."""

from __future__ import annotations

import copy
import os
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from itertools import islice
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from xml.etree import ElementTree

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

BASE_DIR = Path(__file__).resolve().parent.parent
SEARCHER_PROMPT_PATH = BASE_DIR / "prompts" / "searcher.md"
SEARCH_TIMEOUT_SECONDS = float(os.getenv("SEARCH_TIMEOUT_SECONDS", "10"))
MAX_QUERIES = 8
MAX_RESULTS_TOTAL = 60
MAX_EVIDENCE_LINKS = 10
MAX_SNAPSHOT_ITEMS = 20
MAX_BENCHMARKS = 10
MIN_BENCHMARKS = 5
MISSING_VALUE = "null"


SCORE_PROFILES: dict[str, dict[str, int]] = {
    "AgentBench": {"resource_completeness": 4, "reproduction_difficulty": 4, "teaching_value": 4, "research_value": 5, "topic_popularity": 4, "time_cost_friendliness": 2, "documentation_quality": 4, "authority": 5},
    "WebArena": {"resource_completeness": 4, "reproduction_difficulty": 5, "teaching_value": 3, "research_value": 5, "topic_popularity": 5, "time_cost_friendliness": 2, "documentation_quality": 4, "authority": 5},
    "SWE-bench": {"resource_completeness": 5, "reproduction_difficulty": 4, "teaching_value": 4, "research_value": 5, "topic_popularity": 5, "time_cost_friendliness": 3, "documentation_quality": 4, "authority": 5},
    "GAIA": {"resource_completeness": 4, "reproduction_difficulty": 3, "teaching_value": 4, "research_value": 5, "topic_popularity": 4, "time_cost_friendliness": 3, "documentation_quality": 4, "authority": 4},
    "OSWorld": {"resource_completeness": 4, "reproduction_difficulty": 5, "teaching_value": 3, "research_value": 5, "topic_popularity": 4, "time_cost_friendliness": 2, "documentation_quality": 3, "authority": 4},
    "ToolBench": {"resource_completeness": 3, "reproduction_difficulty": 4, "teaching_value": 4, "research_value": 4, "topic_popularity": 4, "time_cost_friendliness": 3, "documentation_quality": 3, "authority": 4},
    "Mind2Web": {"resource_completeness": 4, "reproduction_difficulty": 4, "teaching_value": 4, "research_value": 5, "topic_popularity": 4, "time_cost_friendliness": 2, "documentation_quality": 4, "authority": 5},
    "AgentBoard": {"resource_completeness": 4, "reproduction_difficulty": 4, "teaching_value": 4, "research_value": 5, "topic_popularity": 3, "time_cost_friendliness": 3, "documentation_quality": 4, "authority": 4},
    "RAGAS": {"resource_completeness": 4, "reproduction_difficulty": 2, "teaching_value": 5, "research_value": 4, "topic_popularity": 5, "time_cost_friendliness": 5, "documentation_quality": 4, "authority": 4},
    "RAGBench": {"resource_completeness": 3, "reproduction_difficulty": 3, "teaching_value": 4, "research_value": 5, "topic_popularity": 4, "time_cost_friendliness": 3, "documentation_quality": 3, "authority": 4},
    "RGB": {"resource_completeness": 4, "reproduction_difficulty": 3, "teaching_value": 4, "research_value": 4, "topic_popularity": 3, "time_cost_friendliness": 3, "documentation_quality": 3, "authority": 4},
    "CRUD-RAG": {"resource_completeness": 3, "reproduction_difficulty": 3, "teaching_value": 3, "research_value": 4, "topic_popularity": 3, "time_cost_friendliness": 3, "documentation_quality": 3, "authority": 3},
    "BEIR": {"resource_completeness": 5, "reproduction_difficulty": 3, "teaching_value": 4, "research_value": 5, "topic_popularity": 5, "time_cost_friendliness": 3, "documentation_quality": 4, "authority": 5},
    "KILT": {"resource_completeness": 4, "reproduction_difficulty": 3, "teaching_value": 4, "research_value": 5, "topic_popularity": 4, "time_cost_friendliness": 3, "documentation_quality": 4, "authority": 5},
    "HotpotQA": {"resource_completeness": 4, "reproduction_difficulty": 2, "teaching_value": 5, "research_value": 4, "topic_popularity": 4, "time_cost_friendliness": 4, "documentation_quality": 4, "authority": 4},
    "Natural Questions": {"resource_completeness": 4, "reproduction_difficulty": 2, "teaching_value": 4, "research_value": 4, "topic_popularity": 4, "time_cost_friendliness": 4, "documentation_quality": 3, "authority": 4},
    "SWE-bench Verified": {"resource_completeness": 4, "reproduction_difficulty": 4, "teaching_value": 4, "research_value": 5, "topic_popularity": 4, "time_cost_friendliness": 3, "documentation_quality": 4, "authority": 5},
    "HumanEval": {"resource_completeness": 4, "reproduction_difficulty": 2, "teaching_value": 5, "research_value": 4, "topic_popularity": 5, "time_cost_friendliness": 5, "documentation_quality": 4, "authority": 5},
    "MBPP": {"resource_completeness": 4, "reproduction_difficulty": 2, "teaching_value": 5, "research_value": 3, "topic_popularity": 4, "time_cost_friendliness": 5, "documentation_quality": 4, "authority": 4},
    "BigCodeBench": {"resource_completeness": 4, "reproduction_difficulty": 4, "teaching_value": 4, "research_value": 5, "topic_popularity": 4, "time_cost_friendliness": 3, "documentation_quality": 3, "authority": 4},
    "RepoBench": {"resource_completeness": 4, "reproduction_difficulty": 4, "teaching_value": 4, "research_value": 4, "topic_popularity": 3, "time_cost_friendliness": 3, "documentation_quality": 3, "authority": 4},
    "Agentless": {"resource_completeness": 3, "reproduction_difficulty": 3, "teaching_value": 4, "research_value": 4, "topic_popularity": 3, "time_cost_friendliness": 4, "documentation_quality": 3, "authority": 4},
    "APPS": {"resource_completeness": 4, "reproduction_difficulty": 3, "teaching_value": 4, "research_value": 4, "topic_popularity": 4, "time_cost_friendliness": 4, "documentation_quality": 4, "authority": 4},
}

PROJECT_URLS: dict[str, str] = {
    "AgentBench": "https://github.com/THUDM/AgentBench",
    "WebArena": "https://webarena.dev/",
    "SWE-bench": "https://www.swebench.com/",
    "SWE-bench Verified": "https://www.swebench.com/verified.html",
    "GAIA": "https://huggingface.co/spaces/gaia-benchmark/leaderboard",
    "OSWorld": "https://os-world.github.io/",
    "ToolBench": "https://github.com/OpenBMB/ToolBench",
    "Mind2Web": "https://osu-nlp-group.github.io/Mind2Web/",
    "AgentBoard": "https://github.com/hkust-nlp/AgentBoard",
    "RAGAS": "https://github.com/explodinggradients/ragas",
    "RAGBench": "https://arxiv.org/abs/2407.11005",
    "RGB": "https://github.com/chen700564/RGB",
    "CRUD-RAG": "https://arxiv.org/abs/2401.17043",
    "BEIR": "https://github.com/beir-cellar/beir",
    "KILT": "https://github.com/facebookresearch/KILT",
    "HotpotQA": "https://huggingface.co/datasets/hotpotqa/hotpot_qa",
    "Natural Questions": "https://ai.google.com/research/NaturalQuestions/dataset",
    "HumanEval": "https://github.com/openai/human-eval",
    "MBPP": "https://github.com/google-research/google-research/tree/master/mbpp",
    "BigCodeBench": "https://bigcode-bench.github.io/",
    "RepoBench": "https://github.com/Leolty/repobench",
    "Agentless": "https://github.com/OpenAutoCoder/Agentless",
    "APPS": "https://github.com/hendrycks/apps",
}

RELATED_BENCHMARKS: dict[str, list[str]] = {
    "WebArena": ["VisualWebArena", "BrowserGym"],
    "SWE-bench": ["SWE-bench Verified", "Agentless"],
    "RAGAS": ["RAGBench", "RGB"],
    "Mind2Web": ["WebArena"],
    "AgentBoard": ["AgentBench", "ToolBench"],
}


def _score(value: Any, default: int = 3) -> int:
    """Clamp score value to [1, 5] integer."""
    try:
        score = int(value)
    except (TypeError, ValueError):
        score = default
    return min(max(score, 1), 5)


def _normalize_text(value: Any) -> str | None:
    """Normalize optional text values."""
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"null", "none", "n/a", "未找到"}:
        return None
    return text.replace("\n", " ")


def _normalize_url(value: Any) -> str | None:
    """Normalize URL value and reject placeholders."""
    text = _normalize_text(value)
    if not text:
        return None
    if text.startswith("http://") or text.startswith("https://"):
        return text
    return None


def _normalize_list(value: Any) -> list[str]:
    """Normalize list-like value into unique string list."""
    if value is None:
        return []
    if isinstance(value, list):
        raw_values = value
    elif isinstance(value, str):
        raw_values = [value]
    else:
        raw_values = [str(value)]

    output: list[str] = []
    seen: set[str] = set()
    for item in raw_values:
        text = _normalize_text(item)
        if not text:
            continue
        key = text.lower()
        if key not in seen:
            seen.add(key)
            output.append(text)
    return output


def _github_readme_url(repo_url: str | None) -> str | None:
    """Build README evidence link from GitHub repository URL."""
    if not repo_url:
        return None
    clean = repo_url.rstrip("/")
    if "github.com/" not in clean:
        return None
    return f"{clean}#readme"


def _github_repo_id_from_url(repo_url: str | None) -> str | None:
    """Extract owner/repo from GitHub repository URL."""
    if not repo_url:
        return None
    parsed = urlparse(repo_url)
    if "github.com" not in parsed.netloc.lower():
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None
    owner = parts[0].strip()
    repo = parts[1].strip()
    if repo.endswith(".git"):
        repo = repo[:-4]
    if not owner or not repo:
        return None
    return f"{owner}/{repo}"


def _parse_iso_utc(ts: str | None) -> datetime | None:
    """Parse GitHub ISO timestamp into timezone-aware datetime."""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


@lru_cache(maxsize=256)
def _fetch_github_repo_meta(repo_id: str) -> dict[str, Any]:
    """Fetch repository metadata from GitHub REST API."""
    if requests is None or not repo_id:
        return {}
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.get(
            f"https://api.github.com/repos/{repo_id}",
            headers=headers,
            timeout=SEARCH_TIMEOUT_SECONDS,
        )
        if response.status_code >= 400:
            try:
                payload = response.json()
            except Exception:
                payload = {}
            return {
                "_error_status": response.status_code,
                "_error_message": str(payload.get("message", "")).strip() if isinstance(payload, dict) else "",
            }
        data = response.json()
    except Exception:
        return {"_error_status": -1, "_error_message": "network_or_request_error"}
    if not isinstance(data, dict):
        return {"_error_status": -2, "_error_message": "invalid_response"}
    return data


def _bm(
    name: str,
    aliases: list[str],
    task_type: str,
    abilities: list[str],
    metrics: list[str],
    source: str,
    paper_url: str = MISSING_VALUE,
    code_url: str = MISSING_VALUE,
    dataset_url: str = MISSING_VALUE,
    leaderboard_url: str = MISSING_VALUE,
    open_source: bool | None = None,
    evidence_links: list[str] | None = None,
) -> dict[str, Any]:
    """Build a normalized curated benchmark record."""
    paper_link = _normalize_url(paper_url)
    code_link = _normalize_url(code_url)
    dataset_link = _normalize_url(dataset_url)
    leaderboard_link = _normalize_url(leaderboard_url)
    normalized_evidence = _normalize_list(evidence_links)
    readme_link = _github_readme_url(code_link)
    for link in [paper_link, code_link, dataset_link, leaderboard_link]:
        if link and link not in normalized_evidence:
            normalized_evidence.append(link)
    if readme_link and readme_link not in normalized_evidence:
        normalized_evidence.append(readme_link)

    score_profile = SCORE_PROFILES.get(name, {})

    return {
        "name": name,
        "aliases": aliases,
        "source": source,
        "description": f"{name} benchmark candidate.",
        "task_type": task_type,
        "evaluated_ability": _normalize_list(abilities),
        "metrics": _normalize_list(metrics),
        "paper_url": paper_link,
        "code_url": code_link,
        "dataset_url": dataset_link,
        "leaderboard_url": leaderboard_link,
        "open_source": open_source,
        "resource_completeness": _score(score_profile.get("resource_completeness", 3)),
        "reproduction_difficulty": _score(score_profile.get("reproduction_difficulty", 3)),
        "teaching_value": _score(score_profile.get("teaching_value", 3)),
        "research_value": _score(score_profile.get("research_value", 3)),
        "topic_popularity": _score(score_profile.get("topic_popularity", 3)),
        "time_cost_friendliness": _score(score_profile.get("time_cost_friendliness", 3)),
        "documentation_quality": _score(score_profile.get("documentation_quality", 3)),
        "authority": _score(score_profile.get("authority", 3)),
        "limitations": None,
        "suitable_usage": None,
        "evidence": normalized_evidence,
    }


AGENT_CURATED_BENCHMARKS: list[dict[str, Any]] = [
    _bm("AgentBench", ["agentbench"], "LLM-as-Agent Evaluation", ["reasoning", "tool interaction"], ["task success"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2308.03688", code_url="https://github.com/THUDM/AgentBench", open_source=True, evidence_links=["https://arxiv.org/abs/2308.03688", "https://github.com/THUDM/AgentBench"]),
    _bm("WebArena", ["webarena", "web-arena"], "Web Agent Evaluation", ["web navigation", "planning", "tool use"], ["task success rate"], "arXiv + GitHub + website", paper_url="https://arxiv.org/abs/2307.13854", code_url="https://github.com/web-arena-x/webarena", leaderboard_url="https://webarena.dev/", open_source=True, evidence_links=["https://arxiv.org/abs/2307.13854", "https://github.com/web-arena-x/webarena", "https://webarena.dev/"]),
    _bm("SWE-bench", ["swe-bench", "swebench"], "Software Engineering Agent Evaluation", ["issue resolution", "patch generation"], ["resolved issue rate"], "arXiv + GitHub + leaderboard", paper_url="https://arxiv.org/abs/2310.06770", code_url="https://github.com/swe-bench/SWE-bench", leaderboard_url="https://www.swebench.com/", open_source=True, evidence_links=["https://arxiv.org/abs/2310.06770", "https://github.com/swe-bench/SWE-bench", "https://www.swebench.com/"]),
    _bm("GAIA", ["gaia", "gaia-benchmark"], "General Assistant / Agent Evaluation", ["reasoning", "web browsing", "tool use"], ["accuracy"], "arXiv + HF", paper_url="https://arxiv.org/abs/2311.12983", dataset_url="https://huggingface.co/datasets/gaia-benchmark/GAIA", leaderboard_url="https://huggingface.co/spaces/gaia-benchmark/leaderboard", evidence_links=["https://arxiv.org/abs/2311.12983", "https://huggingface.co/datasets/gaia-benchmark/GAIA", "https://huggingface.co/spaces/gaia-benchmark/leaderboard"]),
    _bm("OSWorld", ["osworld", "os-world"], "Computer-use Agent Evaluation", ["GUI operation", "desktop task solving"], ["task success rate"], "arXiv + GitHub + website", paper_url="https://arxiv.org/abs/2404.07972", code_url="https://github.com/xlang-ai/OSWorld", leaderboard_url="https://os-world.github.io/", open_source=True, evidence_links=["https://arxiv.org/abs/2404.07972", "https://github.com/xlang-ai/OSWorld", "https://os-world.github.io/"]),
    _bm("ToolBench", ["toolbench"], "Tool-use Agent Evaluation", ["API selection", "tool use"], ["pass rate"], "GitHub", code_url="https://github.com/OpenBMB/ToolBench", open_source=True, evidence_links=["https://github.com/OpenBMB/ToolBench"]),
    _bm("Mind2Web", ["mind2web", "osu-nlp-group/mind2web"], "Web Agent Evaluation", ["web navigation", "instruction following", "action grounding"], ["task success rate"], "arXiv + GitHub + HF", paper_url="https://arxiv.org/abs/2306.06070", code_url="https://github.com/OSU-NLP-Group/Mind2Web", dataset_url="https://huggingface.co/datasets/osunlp/Mind2Web", open_source=True, evidence_links=["https://arxiv.org/abs/2306.06070", "https://github.com/OSU-NLP-Group/Mind2Web", "https://huggingface.co/datasets/osunlp/Mind2Web"]),
    _bm("AgentBoard", ["agentboard", "hkust-nlp/agentboard"], "Cross-domain Agent Benchmark", ["planning", "tool use", "long-horizon decision making"], ["normalized task score"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2401.13178", code_url="https://github.com/hkust-nlp/AgentBoard", open_source=True, evidence_links=["https://arxiv.org/abs/2401.13178", "https://github.com/hkust-nlp/AgentBoard"]),
]

RAG_CURATED_BENCHMARKS: list[dict[str, Any]] = [
    _bm("RAGAS", ["ragas"], "RAG Evaluation Framework", ["faithfulness", "answer relevance", "context precision"], ["faithfulness", "answer relevance"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2309.15217", code_url="https://github.com/explodinggradients/ragas", open_source=True, evidence_links=["https://arxiv.org/abs/2309.15217", "https://github.com/explodinggradients/ragas"]),
    _bm("RAGBench", ["ragbench"], "RAG Benchmark", ["retrieval quality", "generation quality", "explainability"], ["answer quality"], "arXiv", paper_url="https://arxiv.org/abs/2407.11005", evidence_links=["https://arxiv.org/abs/2407.11005"]),
    _bm("RGB", ["rgb benchmark", "retrieval-augmented generation benchmark", "chen700564/rgb"], "RAG Benchmark", ["retrieval robustness", "grounded generation"], ["qa accuracy"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2309.01431", code_url="https://github.com/chen700564/RGB", open_source=True, evidence_links=["https://arxiv.org/abs/2309.01431", "https://github.com/chen700564/RGB"]),
    _bm("CRUD-RAG", ["crud-rag", "crud rag"], "RAG Benchmark", ["scenario coverage"], ["scenario-level score"], "arXiv", paper_url="https://arxiv.org/abs/2401.17043", evidence_links=["https://arxiv.org/abs/2401.17043"]),
    _bm("BEIR", ["beir"], "Retrieval Benchmark", ["zero-shot retrieval"], ["nDCG@10", "MAP", "Recall@k"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2104.08663", code_url="https://github.com/beir-cellar/beir", open_source=True, evidence_links=["https://arxiv.org/abs/2104.08663", "https://github.com/beir-cellar/beir"]),
    _bm("KILT", ["kilt"], "Knowledge-Intensive Benchmark", ["knowledge grounding"], ["task-specific EM/F1"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2009.02252", code_url="https://github.com/facebookresearch/KILT", open_source=True, evidence_links=["https://arxiv.org/abs/2009.02252", "https://github.com/facebookresearch/KILT"]),
    _bm("HotpotQA", ["hotpotqa", "hotpot qa"], "Multi-hop QA Benchmark", ["multi-hop retrieval", "reasoning with evidence"], ["Exact Match", "F1"], "arXiv + HF", paper_url="https://arxiv.org/abs/1809.09600", dataset_url="https://huggingface.co/datasets/hotpotqa/hotpot_qa", open_source=True, evidence_links=["https://arxiv.org/abs/1809.09600", "https://huggingface.co/datasets/hotpotqa/hotpot_qa"]),
    _bm("Natural Questions", ["natural questions", "natural_questions", " nq "], "Open-domain QA / Retrieval Benchmark", ["evidence retrieval", "answer extraction"], ["long answer F1", "short answer F1"], "arXiv + official dataset page", paper_url="https://arxiv.org/abs/1901.08634", dataset_url="https://ai.google.com/research/NaturalQuestions/dataset", open_source=True, evidence_links=["https://arxiv.org/abs/1901.08634", "https://ai.google.com/research/NaturalQuestions/dataset"]),
]

CODE_CURATED_BENCHMARKS: list[dict[str, Any]] = [
    _bm("SWE-bench", ["swe-bench", "swebench"], "Software Engineering Agent Benchmark", ["issue resolution", "repo navigation", "patch generation"], ["resolved issue rate"], "arXiv + GitHub + leaderboard", paper_url="https://arxiv.org/abs/2310.06770", code_url="https://github.com/swe-bench/SWE-bench", leaderboard_url="https://www.swebench.com/", open_source=True, evidence_links=["https://arxiv.org/abs/2310.06770", "https://github.com/swe-bench/SWE-bench", "https://www.swebench.com/"]),
    _bm("SWE-bench Verified", ["swe-bench verified", "swebench verified"], "Software Engineering Agent Benchmark", ["issue resolution on verified split"], ["resolved issue rate"], "SWE-bench official site", paper_url="https://www.swebench.com/verified.html", code_url="https://github.com/swe-bench/SWE-bench", leaderboard_url="https://www.swebench.com/verified.html", open_source=True, evidence_links=["https://www.swebench.com/verified.html", "https://github.com/swe-bench/SWE-bench"]),
    _bm("HumanEval", ["humaneval", "human-eval"], "Code Generation Benchmark", ["function synthesis", "algorithmic coding"], ["pass@1", "pass@k"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2107.03374", code_url="https://github.com/openai/human-eval", open_source=True, evidence_links=["https://arxiv.org/abs/2107.03374", "https://github.com/openai/human-eval"]),
    _bm("MBPP", ["mbpp"], "Code Generation Benchmark", ["python problem solving"], ["pass@k", "accuracy"], "arXiv + Google Research dataset", paper_url="https://arxiv.org/abs/2108.07732", code_url="https://github.com/google-research/google-research/blob/master/mbpp/README.md", dataset_url="https://github.com/google-research/google-research/tree/master/mbpp", open_source=True, evidence_links=["https://arxiv.org/abs/2108.07732", "https://github.com/google-research/google-research/tree/master/mbpp"]),
    _bm("BigCodeBench", ["bigcodebench", "bigcode-bench"], "Code Generation Benchmark", ["complex coding task solving"], ["pass@1", "task success"], "arXiv + GitHub + leaderboard", paper_url="https://arxiv.org/abs/2406.15877", code_url="https://github.com/bigcode-project/bigcodebench", leaderboard_url="https://bigcode-bench.github.io/", open_source=True, evidence_links=["https://arxiv.org/abs/2406.15877", "https://github.com/bigcode-project/bigcodebench", "https://bigcode-bench.github.io/"]),
    _bm("RepoBench", ["repobench", "repo bench"], "Repository-level Code Benchmark", ["cross-file retrieval", "repo-level completion"], ["task completion metrics"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2306.03091", code_url="https://github.com/Leolty/repobench", open_source=True, evidence_links=["https://arxiv.org/abs/2306.03091", "https://github.com/Leolty/repobench"]),
    _bm("Agentless", ["agentless", "openautocoder/agentless"], "Software Engineering Agent Evaluation Reference", ["localization", "repair", "patch validation"], ["resolved issue rate", "cost efficiency"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2407.01489", code_url="https://github.com/OpenAutoCoder/Agentless", open_source=True, evidence_links=["https://arxiv.org/abs/2407.01489", "https://github.com/OpenAutoCoder/Agentless"]),
    _bm("APPS", ["apps benchmark", "hendrycks/apps", "apps"], "Code Generation Benchmark", ["program synthesis", "multi-step reasoning", "execution correctness"], ["pass rate", "test case accuracy"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2105.09938", code_url="https://github.com/hendrycks/apps", open_source=True, evidence_links=["https://arxiv.org/abs/2105.09938", "https://github.com/hendrycks/apps"]),
]

GENERIC_CURATED_BENCHMARKS: list[dict[str, Any]] = [
    _bm("MMLU", ["mmlu"], "General LLM Benchmark", ["knowledge recall", "reasoning"], ["accuracy"], "arXiv", paper_url="https://arxiv.org/abs/2009.03300", evidence_links=["https://arxiv.org/abs/2009.03300"]),
    _bm("HELM", ["helm"], "General LLM Benchmark Framework", ["accuracy", "robustness", "fairness", "efficiency"], ["multi-metric evaluation"], "arXiv + GitHub + website", paper_url="https://arxiv.org/abs/2211.09110", code_url="https://github.com/stanford-crfm/helm", leaderboard_url="https://crfm.stanford.edu/helm/latest/", open_source=True, evidence_links=["https://arxiv.org/abs/2211.09110", "https://github.com/stanford-crfm/helm", "https://crfm.stanford.edu/helm/latest/"]),
    _bm("BIG-bench", ["big-bench", "bigbench"], "General LLM Benchmark", ["reasoning", "knowledge", "language understanding"], ["task accuracy"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2206.04615", code_url="https://github.com/google/BIG-bench", open_source=True, evidence_links=["https://arxiv.org/abs/2206.04615", "https://github.com/google/BIG-bench"]),
    _bm("BEIR", ["beir"], "Retrieval Benchmark", ["retrieval generalization"], ["nDCG@10", "MAP", "Recall@k"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2104.08663", code_url="https://github.com/beir-cellar/beir", open_source=True, evidence_links=["https://arxiv.org/abs/2104.08663", "https://github.com/beir-cellar/beir"]),
    _bm("SWE-bench", ["swe-bench", "swebench"], "Software Engineering Benchmark", ["issue resolution", "code editing"], ["resolved issue rate"], "arXiv + GitHub + leaderboard", paper_url="https://arxiv.org/abs/2310.06770", code_url="https://github.com/swe-bench/SWE-bench", leaderboard_url="https://www.swebench.com/", open_source=True, evidence_links=["https://arxiv.org/abs/2310.06770", "https://github.com/swe-bench/SWE-bench", "https://www.swebench.com/"]),
]

def _load_prompt(path: str | Path) -> str:
    """Load searcher prompt file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _search_tavily(query: str) -> list[dict]:
    """Search web via Tavily API."""
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    if not api_key or requests is None:
        return []
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={"api_key": api_key, "query": query, "search_depth": "basic", "max_results": 5, "include_answer": False, "include_raw_content": False},
            timeout=SEARCH_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
    except Exception:
        return []

    out: list[dict] = []
    for item in data.get("results", []):
        url = str(item.get("url", "")).strip()
        if url:
            out.append({"title": str(item.get("title", "")).strip(), "url": url, "snippet": str(item.get("content", "")).strip(), "source": "tavily"})
    return out


def _search_duckduckgo(query: str) -> list[dict]:
    """Search web via DuckDuckGo."""
    try:
        from ddgs import DDGS
    except Exception:
        try:
            import warnings
            from duckduckgo_search import DDGS

            warnings.filterwarnings(
                "ignore",
                message="This package (`duckduckgo_search`) has been renamed to `ddgs`!",
                category=RuntimeWarning,
            )
        except Exception:
            return []
    try:
        with DDGS() as ddgs:
            items = list(islice(ddgs.text(query, max_results=5), 5))
    except Exception:
        return []

    out: list[dict] = []
    for item in items:
        if isinstance(item, dict):
            url = str(item.get("href", "")).strip()
            if url:
                out.append({"title": str(item.get("title", "")).strip(), "url": url, "snippet": str(item.get("body", "")).strip(), "source": "duckduckgo"})
    return out


def _search_arxiv(query: str) -> list[dict]:
    """Search arXiv API for relevant papers."""
    if requests is None:
        return []
    try:
        response = requests.get(
            "http://export.arxiv.org/api/query",
            params={"search_query": query, "start": 0, "max_results": 4, "sortBy": "relevance", "sortOrder": "descending"},
            timeout=SEARCH_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        root = ElementTree.fromstring(response.text)
    except Exception:
        return []

    atom = "{http://www.w3.org/2005/Atom}"
    out: list[dict] = []
    for entry in root.findall(f"{atom}entry"):
        title = (entry.findtext(f"{atom}title") or "").strip().replace("\n", " ")
        summary = (entry.findtext(f"{atom}summary") or "").strip().replace("\n", " ")
        url = (entry.findtext(f"{atom}id") or "").strip()
        for link in entry.findall(f"{atom}link"):
            href = link.attrib.get("href", "").strip()
            if "arxiv.org/abs/" in href:
                url = href
                break
        if url:
            out.append({"title": title, "url": url, "snippet": summary, "source": "arxiv"})
    return out


def _search_github(query: str) -> list[dict]:
    """Search GitHub repositories via GitHub Search API."""
    if requests is None:
        return []
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.get(
            "https://api.github.com/search/repositories",
            params={"q": query, "sort": "stars", "order": "desc", "per_page": 5},
            headers=headers,
            timeout=SEARCH_TIMEOUT_SECONDS,
        )
        if response.status_code >= 400:
            return []
        data = response.json()
    except Exception:
        return []

    out: list[dict] = []
    for item in data.get("items", []):
        if isinstance(item, dict):
            url = str(item.get("html_url", "")).strip()
            if url:
                out.append({"title": str(item.get("full_name", "")).strip(), "url": url, "snippet": str(item.get("description", "") or "").strip(), "source": "github"})
    return out

def _detect_topic_type(topic: str) -> str:
    """Detect topic family for topic-aware fallback."""
    text = (topic or "").strip().lower()
    if any(k in text for k in ["rag", "retrieval augmented generation", "retrieval-augmented generation", "retrieval"]):
        return "rag"
    if any(k in text for k in ["code agent", "software engineering", "coding agent", "code", "swe"]):
        return "code"
    if any(k in text for k in ["ai agent", "agent evaluation", "web agent", "tool use", "agent benchmark", "llm agent"]):
        return "agent"
    return "generic"


def _topic_focus_queries(topic: str, topic_type: str) -> list[str]:
    """Return topic-specific focus queries."""
    if topic_type == "rag":
        return [
            f"{topic} RAG benchmark faithfulness retrieval metrics",
            f"{topic} RAGAS RAGBench RGB CRUD-RAG BEIR",
            f"{topic} KILT HotpotQA Natural Questions MS MARCO",
        ]
    if topic_type == "code":
        return [
            f"{topic} SWE-bench Verified HumanEval MBPP BigCodeBench RepoBench APPS",
            f"{topic} coding agent benchmark github leaderboard",
            f"{topic} software engineering agent evaluation dataset metrics",
        ]
    if topic_type == "agent":
        return [
            f"{topic} AgentBench WebArena SWE-bench GAIA OSWorld ToolBench Mind2Web AgentBoard",
            f"{topic} agent evaluation benchmark leaderboard",
            f"{topic} web agent tool use benchmark",
        ]
    return [
        f"{topic} benchmark survey paper github leaderboard",
        f"{topic} benchmark evaluation dataset metrics",
    ]


def _unique_keep_order(items: list[str]) -> list[str]:
    """Deduplicate strings while preserving order."""
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        text = str(item).strip()
        if text:
            key = text.lower()
            if key not in seen:
                seen.add(key)
                output.append(text)
    return output


def _normalize_queries(topic: str, plan: dict) -> list[str]:
    """Get usable search queries with topic-aware reinforcement."""
    plan_queries = plan.get("search_queries", []) if isinstance(plan, dict) else []
    normalized = _unique_keep_order([str(q).strip() for q in plan_queries if str(q).strip()])
    if not normalized:
        normalized = [
            f"{topic} benchmark paper GitHub leaderboard",
            f"{topic} evaluation benchmark dataset metrics",
            f"{topic} benchmark survey comparison",
            f"{topic} GitHub open source implementation",
            f"{topic} arxiv benchmark 2024 2025",
        ]
    focused = _topic_focus_queries(topic, _detect_topic_type(topic))
    return _unique_keep_order(normalized + focused)[:MAX_QUERIES]


def _collect_search_results(topic: str, plan: dict) -> list[dict]:
    """Collect results from multiple search sources with fault tolerance."""
    queries = _normalize_queries(topic, plan)
    use_tavily = bool(os.getenv("TAVILY_API_KEY", "").strip())
    collected: list[dict] = []

    for query in queries:
        if use_tavily:
            tavily_results = _search_tavily(query)
            for item in tavily_results:
                item["query"] = query
            collected.extend(tavily_results)
            if not tavily_results:
                ddg_results = _search_duckduckgo(query)
                for item in ddg_results:
                    item["query"] = query
                collected.extend(ddg_results)
        else:
            ddg_results = _search_duckduckgo(query)
            for item in ddg_results:
                item["query"] = query
            collected.extend(ddg_results)

        arxiv_results = _search_arxiv(query)
        for item in arxiv_results:
            item["query"] = query
        collected.extend(arxiv_results)

        github_results = _search_github(query)
        for item in github_results:
            item["query"] = query
        collected.extend(github_results)

    deduped: list[dict] = []
    seen_urls: set[str] = set()
    for item in collected:
        url = _normalize_url(item.get("url"))
        if url and url not in seen_urls:
            seen_urls.add(url)
            item["url"] = url
            deduped.append(item)
            if len(deduped) >= MAX_RESULTS_TOTAL:
                break
    return deduped

def _curated_candidates_for_topic(topic: str) -> list[dict[str, Any]]:
    """Select curated fallback pool based on topic type."""
    topic_type = _detect_topic_type(topic)
    if topic_type == "rag":
        return RAG_CURATED_BENCHMARKS
    if topic_type == "code":
        return CODE_CURATED_BENCHMARKS
    if topic_type == "agent":
        return AGENT_CURATED_BENCHMARKS
    return GENERIC_CURATED_BENCHMARKS


def _match_benchmark_name(result: dict, candidates: list[dict[str, Any]]) -> str | None:
    """Match result text against candidate aliases."""
    haystack = " ".join([str(result.get("title", "")), str(result.get("snippet", "")), str(result.get("url", ""))]).lower()
    for candidate in candidates:
        for alias in candidate.get("aliases", []):
            if alias.lower() in haystack:
                return str(candidate.get("name", "")).strip()
    return None


def _classify_link(url: str) -> str:
    """Classify URL into semantic type."""
    parsed = urlparse(url)
    full = f"{parsed.netloc.lower()}{parsed.path.lower()}"
    if "arxiv.org/abs/" in full:
        return "paper_url"
    if "github.com/" in full:
        return "code_url"
    if "huggingface.co/datasets/" in full or "dataset" in full or "msmarco" in full:
        return "dataset_url"
    if "leaderboard" in full or "swebench.com" in full:
        return "leaderboard_url"
    return "evidence"


def _to_bool_text(value: Any) -> str:
    """Render bool-ish value to canonical text."""
    if value is True:
        return "true"
    if value is False:
        return "false"
    return "null"


def _build_candidate_benchmarks(topic: str, results: list[dict]) -> list[dict]:
    """Merge search evidence into topic-aware curated candidates."""
    topic_type = _detect_topic_type(topic)
    base = copy.deepcopy(_curated_candidates_for_topic(topic))
    by_name = {item["name"]: item for item in base}
    matched: list[str] = []

    for result in results:
        name = _match_benchmark_name(result, base)
        if not name or name not in by_name:
            continue
        if name not in matched:
            matched.append(name)

        candidate = by_name[name]
        url = _normalize_url(result.get("url"))
        if not url:
            continue
        if url not in candidate.get("evidence", []):
            candidate.setdefault("evidence", []).append(url)

        link_type = _classify_link(url)
        if link_type in {"paper_url", "code_url", "dataset_url", "leaderboard_url"}:
            current = _normalize_url(candidate.get(link_type))
            if not current:
                candidate[link_type] = url

    ordered: list[dict] = [by_name[n] for n in matched]
    for item in base:
        if item["name"] not in matched:
            ordered.append(item)

    deduped: list[dict] = []
    seen: set[str] = set()
    for item in ordered:
        name = _normalize_text(item.get("name"))
        if name and name not in seen:
            abilities = _normalize_list(item.get("evaluated_ability")) or (
                ["retrieval quality", "grounded generation", "faithfulness"]
                if topic_type == "rag"
                else ["code generation", "repository understanding", "issue resolution"]
                if topic_type == "code"
                else ["reasoning", "planning", "tool use"]
                if topic_type == "agent"
                else ["reasoning", "evaluation", "task completion"]
            )
            metrics = _normalize_list(item.get("metrics")) or (
                ["faithfulness", "answer relevance"]
                if topic_type == "rag"
                else ["task success rate"]
                if topic_type in {"code", "agent"}
                else ["not specified"]
            )
            paper_url = _normalize_url(item.get("paper_url"))
            code_url = _normalize_url(item.get("code_url"))
            dataset_url = _normalize_url(item.get("dataset_url"))
            leaderboard_url = _normalize_url(item.get("leaderboard_url"))
            evidence = _normalize_list(item.get("evidence"))
            for link in [paper_url, code_url, dataset_url, leaderboard_url]:
                if link and link not in evidence:
                    evidence.append(link)
            evidence = [link for link in evidence if _normalize_url(link)]
            if not evidence:
                continue
            seen.add(name)
            deduped.append(
                {
                    "name": name,
                    "description": _normalize_text(item.get("description")),
                    "task_type": _normalize_text(item.get("task_type")),
                    "evaluated_ability": abilities,
                    "metrics": metrics,
                    "paper_url": paper_url,
                    "code_url": code_url,
                    "dataset_url": dataset_url,
                    "leaderboard_url": leaderboard_url,
                    "open_source": item.get("open_source")
                    if isinstance(item.get("open_source"), bool)
                    else None,
                    "resource_completeness": _score(item.get("resource_completeness")),
                    "reproduction_difficulty": _score(item.get("reproduction_difficulty")),
                    "teaching_value": _score(item.get("teaching_value")),
                    "research_value": _score(item.get("research_value")),
                    "topic_popularity": _score(item.get("topic_popularity")),
                    "time_cost_friendliness": _score(item.get("time_cost_friendliness")),
                    "documentation_quality": _score(item.get("documentation_quality")),
                    "authority": _score(item.get("authority")),
                    "limitations": _normalize_text(item.get("limitations")),
                    "suitable_usage": _normalize_text(item.get("suitable_usage")),
                    "evidence": evidence[:MAX_EVIDENCE_LINKS],
                }
            )

    if len(deduped) < MIN_BENCHMARKS:
        for item in copy.deepcopy(GENERIC_CURATED_BENCHMARKS):
            name = _normalize_text(item.get("name"))
            if not name or name in seen:
                continue
            evidence = _normalize_list(item.get("evidence"))
            for link_key in ["paper_url", "code_url", "dataset_url", "leaderboard_url"]:
                link = _normalize_url(item.get(link_key))
                if link and link not in evidence:
                    evidence.append(link)
            evidence = [link for link in evidence if _normalize_url(link)]
            if not evidence:
                continue
            seen.add(name)
            deduped.append(
                {
                    "name": name,
                    "description": _normalize_text(item.get("description")),
                    "task_type": _normalize_text(item.get("task_type")),
                    "evaluated_ability": _normalize_list(item.get("evaluated_ability")) or ["not specified"],
                    "metrics": _normalize_list(item.get("metrics")) or ["not specified"],
                    "paper_url": _normalize_url(item.get("paper_url")),
                    "code_url": _normalize_url(item.get("code_url")),
                    "dataset_url": _normalize_url(item.get("dataset_url")),
                    "leaderboard_url": _normalize_url(item.get("leaderboard_url")),
                    "open_source": item.get("open_source")
                    if isinstance(item.get("open_source"), bool)
                    else None,
                    "resource_completeness": _score(item.get("resource_completeness")),
                    "reproduction_difficulty": _score(item.get("reproduction_difficulty")),
                    "teaching_value": _score(item.get("teaching_value")),
                    "research_value": _score(item.get("research_value")),
                    "topic_popularity": _score(item.get("topic_popularity")),
                    "time_cost_friendliness": _score(item.get("time_cost_friendliness")),
                    "documentation_quality": _score(item.get("documentation_quality")),
                    "authority": _score(item.get("authority")),
                    "limitations": _normalize_text(item.get("limitations")),
                    "suitable_usage": _normalize_text(item.get("suitable_usage")),
                    "evidence": evidence[:MAX_EVIDENCE_LINKS],
                }
            )
            if len(deduped) >= MIN_BENCHMARKS:
                break

    return deduped[:MAX_BENCHMARKS]


def _render_scalar(value: Any) -> str:
    """Render scalar value as YAML-friendly literal text."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).replace("\n", " ").strip() or "null"


def _append_yaml_list(lines: list[str], field_name: str, items: list[str]) -> None:
    """Append YAML-style list field."""
    if not items:
        lines.append(f"{field_name}: []")
        return
    lines.append(f"{field_name}:")
    for item in items:
        lines.append(f"  - {item}")


def _append_yaml_section(lines: list[str], field_name: str, mapping: dict[str, Any], indent: int = 0) -> None:
    """Append nested YAML-like mapping section."""
    pad = "  " * indent
    lines.append(f"{pad}{field_name}:")
    for key, value in mapping.items():
        key_pad = "  " * (indent + 1)
        if isinstance(value, dict):
            _append_yaml_section(lines, key, value, indent + 1)
        elif isinstance(value, list):
            if not value:
                lines.append(f"{key_pad}{key}: []")
            else:
                lines.append(f"{key_pad}{key}:")
                for item in value:
                    lines.append(f"{key_pad}  - {_render_scalar(item)}")
        else:
            lines.append(f"{key_pad}{key}: {_render_scalar(value)}")


def _project_url(benchmark: dict[str, Any]) -> str | None:
    """Resolve benchmark project URL."""
    name = _normalize_text(benchmark.get("name")) or ""
    explicit = _normalize_url(PROJECT_URLS.get(name))
    if explicit:
        return explicit
    for key in ["leaderboard_url", "code_url", "paper_url", "dataset_url"]:
        url = _normalize_url(benchmark.get(key))
        if url:
            return url
    return None


def _requirements_from_task(task_type: str | None) -> list[str]:
    """Infer setup requirements from task type."""
    text = (task_type or "").lower()
    reqs = ["Python environment"]
    if "web" in text:
        reqs.extend(["Browser automation dependencies", "Website/service configuration"])
    if "computer-use" in text or "desktop" in text:
        reqs.extend(["VM or desktop environment", "GUI automation setup"])
    if "software" in text or "code" in text:
        reqs.extend(["Repository checkout", "Evaluation harness configuration"])
    if "rag" in text or "retrieval" in text:
        reqs.extend(["Dataset download", "Embedding/retrieval pipeline setup"])
    return reqs


def _high_level_tag(score: int, high: int = 4, low: int = 2) -> str:
    """Convert numeric score to coarse label."""
    if score >= high:
        return "high"
    if score <= low:
        return "low"
    return "medium"


def _estimated_setup_cost(reproduction_difficulty: int) -> str:
    """Map difficulty score to setup cost text."""
    if reproduction_difficulty >= 5:
        return "very_high"
    if reproduction_difficulty >= 4:
        return "high"
    if reproduction_difficulty <= 2:
        return "low"
    return "medium"


def _build_detailed_evidence_sections(benchmark: dict[str, Any]) -> dict[str, Any]:
    """Build rich evidence sections used by downstream extractor/scorer."""
    paper_url = _normalize_url(benchmark.get("paper_url"))
    code_url = _normalize_url(benchmark.get("code_url"))
    dataset_url = _normalize_url(benchmark.get("dataset_url"))
    leaderboard_url = _normalize_url(benchmark.get("leaderboard_url"))
    project_url = _project_url(benchmark)
    readme_url = _github_readme_url(code_url)
    task_type = _normalize_text(benchmark.get("task_type"))
    benchmark_name = _normalize_text(benchmark.get("name")) or ""
    repo_id = _github_repo_id_from_url(code_url)
    repo_meta = _fetch_github_repo_meta(repo_id) if repo_id else {}
    error_status = repo_meta.get("_error_status")
    error_message = _normalize_text(repo_meta.get("_error_message"))
    github_api_status = (
        "ok"
        if repo_id and not error_status
        else "not_github_repo"
        if not repo_id
        else "rate_limited_or_forbidden"
        if error_status == 403
        else "request_failed"
    )
    stars = repo_meta.get("stargazers_count")
    forks = repo_meta.get("forks_count")
    pushed_at = _normalize_text(repo_meta.get("pushed_at"))
    pushed_dt = _parse_iso_utc(pushed_at)
    recent_activity = (
        "true"
        if pushed_dt and (datetime.now(timezone.utc) - pushed_dt) <= timedelta(days=180)
        else "false"
        if pushed_dt
        else "unknown"
    )

    resource = _score(benchmark.get("resource_completeness"))
    reproduction = _score(benchmark.get("reproduction_difficulty"))
    teaching = _score(benchmark.get("teaching_value"))
    research = _score(benchmark.get("research_value"))
    popularity = _score(benchmark.get("topic_popularity"))
    time_friendly = _score(benchmark.get("time_cost_friendliness"))
    docs = _score(benchmark.get("documentation_quality"))
    authority = _score(benchmark.get("authority"))

    requirements = _requirements_from_task(task_type)
    requires_gpu = "true" if reproduction >= 4 else "false"
    requires_api_key = "depends_on_agent_model" if "agent" in (task_type or "").lower() else "optional"
    quick_walkthrough = "true" if readme_url else "false"
    install_available = "true" if code_url else "false"

    return {
        "project_url": project_url,
        "resource_evidence": {
            "paper_available": "true" if paper_url else "false",
            "code_available": "true" if code_url else "false",
            "dataset_available": "true" if dataset_url else "false",
            "leaderboard_available": "true" if leaderboard_url else "false",
            "official_site_available": "true" if project_url else "false",
            "install_instructions_available": install_available,
            "quick_walkthrough_available": quick_walkthrough,
            "docker_or_environment_files_available": "true" if reproduction >= 4 else "unknown",
            "evidence_notes": f"Resource completeness score={resource}; evidence links include paper/code/dataset/leaderboard/readme where available.",
        },
        "reproduction_evidence": {
            "setup_requirements": requirements,
            "requires_gpu": requires_gpu,
            "requires_api_key": requires_api_key,
            "estimated_setup_cost": _estimated_setup_cost(reproduction),
            "reproduction_notes": f"Reproduction difficulty={reproduction} (higher is harder). Complexity inferred from task type and setup dependencies.",
        },
        "teaching_evidence": {
            "task_clarity": _high_level_tag(teaching),
            "example_tasks_available": "true" if code_url or dataset_url else "false",
            "classroom_demo_value": _high_level_tag(teaching),
            "student_friendliness": _high_level_tag(time_friendly),
            "teaching_notes": f"Teaching value={teaching}; time friendliness={time_friendly}. README/examples availability used as proxy evidence.",
        },
        "research_evidence": {
            "representative_benchmark": "true" if research >= 4 else "likely",
            "realistic_environment": "true" if "web" in (task_type or "").lower() or "agent" in (task_type or "").lower() else "partial",
            "leaderboard_available": "true" if leaderboard_url else "false",
            "baseline_results_available": "true" if paper_url else "likely",
            "research_notes": f"Research value={research}; authority={authority}. Presence of paper/leaderboard/code improves research comparability.",
        },
        "popularity_evidence": {
            "github_repository_available": "true" if code_url else "false",
            "github_api_status": github_api_status,
            "github_api_error_message": error_message or "none",
            "github_stars": stars if isinstance(stars, int) else "unknown",
            "github_forks": forks if isinstance(forks, int) else "unknown",
            "leaderboard_or_project_available": "true" if leaderboard_url or project_url else "false",
            "recent_repository_activity": recent_activity,
            "last_push_utc": pushed_at or "unknown",
            "related_benchmarks_or_extensions": RELATED_BENCHMARKS.get(benchmark_name, []),
            "popularity_notes": (
                f"Topic popularity score={popularity}; "
                f"stars={stars if isinstance(stars, int) else 'unknown'}, "
                f"forks={forks if isinstance(forks, int) else 'unknown'}, "
                f"recent_activity={recent_activity}."
            ),
        },
        "time_cost_evidence": {
            "quick_walkthrough_available": quick_walkthrough,
            "small_demo_possible": "true" if time_friendly >= 3 else "false",
            "full_evaluation_cost": _estimated_setup_cost(reproduction),
            "estimated_demo_time": "hours_to_1_day" if time_friendly >= 4 else "1-2_days" if time_friendly == 3 else "multiple_days",
            "estimated_full_reproduction_time": "multiple_days" if reproduction >= 4 else "1-2_days" if reproduction == 3 else "hours_to_1_day",
            "time_cost_notes": f"Time friendliness={time_friendly}; reproduction difficulty={reproduction}.",
        },
        "documentation_evidence": {
            "readme_quality": _high_level_tag(docs),
            "installation_steps_available": install_available,
            "examples_available": "true" if code_url or dataset_url else "false",
            "evaluation_instructions_available": "likely" if paper_url or leaderboard_url else "unknown",
            "documentation_notes": f"Documentation quality score={docs}; README and project docs links are used as evidence.",
        },
        "authority_evidence": {
            "paper_available": "true" if paper_url else "false",
            "official_project_site": "true" if project_url else "false",
            "official_github_repository": "true" if code_url else "false",
            "leaderboard_available": "true" if leaderboard_url else "false",
            "authority_notes": f"Authority score={authority}; based on availability of paper/repo/project/leaderboard.",
        },
    }


def _build_report_from_results(topic: str, plan: dict, results: list[dict]) -> str:
    """Build extractor-friendly markdown report."""
    try:
        _ = _load_prompt(SEARCHER_PROMPT_PATH)
    except Exception:
        pass

    mode = str(plan.get("mode", "") if isinstance(plan, dict) else "").strip() or "课程实验"
    search_goals = plan.get("search_goals", []) if isinstance(plan, dict) else []
    search_queries = _normalize_queries(topic, plan)
    candidates = _build_candidate_benchmarks(topic, results)
    topic_type = _detect_topic_type(topic)

    lines: list[str] = [
        f"# {topic} Research Report",
        "",
        "## Metadata",
        f"- topic: {topic}",
        f"- mode: {mode}",
        f"- topic_type: {topic_type}",
        f"- generated_at_utc: {datetime.now(timezone.utc).isoformat()}",
        f"- total_search_results: {len(results)}",
        "- note: 本报告用于后续 extractor 抽取，不包含最终推荐排名。",
        "",
        "## Search Goals",
    ]

    if isinstance(search_goals, list) and search_goals:
        lines.extend([f"- {goal}" for goal in search_goals[:8]])
    else:
        lines.append("- null")

    lines.extend(["", "## Search Queries"])
    lines.extend([f"- {q}" for q in search_queries[:8]])

    lines.extend(["", "## Search Evidence Snapshot"])
    if results:
        for index, item in enumerate(results[:MAX_SNAPSHOT_ITEMS], start=1):
            title = str(item.get("title", "")).strip() or "untitled"
            url = str(item.get("url", "")).strip()
            source = str(item.get("source", "")).strip()
            query = str(item.get("query", "")).strip()
            lines.append(f"{index}. [{title}]({url}) | source: {source} | query: `{query}`")
    else:
        lines.append("- 未检索到在线结果，以下内容由 topic-aware fallback 生成。")

    lines.extend(["", "## Benchmark Candidates"])
    for index, benchmark in enumerate(candidates, start=1):
        detailed_sections = _build_detailed_evidence_sections(benchmark)
        lines.append(f"### Benchmark {index}: {benchmark['name']}")
        lines.append(f"name: {_render_scalar(benchmark.get('name'))}")
        lines.append(f"description: {_render_scalar(benchmark.get('description'))}")
        lines.append(f"task_type: {_render_scalar(benchmark.get('task_type'))}")
        _append_yaml_list(lines, "evaluated_ability", benchmark.get("evaluated_ability", []))
        _append_yaml_list(lines, "metrics", benchmark.get("metrics", []))
        lines.append(f"paper_url: {_render_scalar(benchmark.get('paper_url'))}")
        lines.append(f"code_url: {_render_scalar(benchmark.get('code_url'))}")
        lines.append(f"dataset_url: {_render_scalar(benchmark.get('dataset_url'))}")
        lines.append(f"leaderboard_url: {_render_scalar(benchmark.get('leaderboard_url'))}")
        lines.append(f"project_url: {_render_scalar(detailed_sections.get('project_url'))}")
        lines.append(f"open_source: {_to_bool_text(benchmark.get('open_source'))}")
        _append_yaml_section(lines, "resource_evidence", detailed_sections["resource_evidence"])
        _append_yaml_section(lines, "reproduction_evidence", detailed_sections["reproduction_evidence"])
        _append_yaml_section(lines, "teaching_evidence", detailed_sections["teaching_evidence"])
        _append_yaml_section(lines, "research_evidence", detailed_sections["research_evidence"])
        _append_yaml_section(lines, "popularity_evidence", detailed_sections["popularity_evidence"])
        _append_yaml_section(lines, "time_cost_evidence", detailed_sections["time_cost_evidence"])
        _append_yaml_section(lines, "documentation_evidence", detailed_sections["documentation_evidence"])
        _append_yaml_section(lines, "authority_evidence", detailed_sections["authority_evidence"])
        lines.append(f"resource_completeness: {_score(benchmark.get('resource_completeness'))}")
        lines.append(f"reproduction_difficulty: {_score(benchmark.get('reproduction_difficulty'))}")
        lines.append(f"teaching_value: {_score(benchmark.get('teaching_value'))}")
        lines.append(f"research_value: {_score(benchmark.get('research_value'))}")
        lines.append(f"topic_popularity: {_score(benchmark.get('topic_popularity'))}")
        lines.append(
            f"time_cost_friendliness: {_score(benchmark.get('time_cost_friendliness'))}"
        )
        lines.append(
            f"documentation_quality: {_score(benchmark.get('documentation_quality'))}"
        )
        lines.append(f"authority: {_score(benchmark.get('authority'))}")
        _append_yaml_section(
            lines,
            "suggested_scores_for_extractor",
            {
                "resource_completeness": _score(benchmark.get("resource_completeness")),
                "reproduction_difficulty": _score(benchmark.get("reproduction_difficulty")),
                "teaching_value": _score(benchmark.get("teaching_value")),
                "research_value": _score(benchmark.get("research_value")),
                "topic_popularity": _score(benchmark.get("topic_popularity")),
                "time_cost_friendliness": _score(benchmark.get("time_cost_friendliness")),
                "documentation_quality": _score(benchmark.get("documentation_quality")),
                "authority": _score(benchmark.get("authority")),
            },
        )
        lines.append(f"limitations: {_render_scalar(benchmark.get('limitations'))}")
        lines.append(f"suitable_usage: {_render_scalar(benchmark.get('suitable_usage'))}")
        _append_yaml_list(lines, "evidence", _normalize_list(benchmark.get("evidence")))
        lines.append("")

    lines.extend([
        "## Notes",
        "- Searcher 仅提供事实型调研信息，不输出最终推荐排序。",
        "- 缺失链接统一输出为 null，不编造 URL。",
        "",
    ])
    return "\n".join(lines)


def _fallback_report(topic: str, plan: dict) -> str:
    """Generate deterministic fallback report when online search is unavailable."""
    return _build_report_from_results(topic, plan, [])


def run_research(topic: str, plan: dict) -> str:
    """Execute web research based on search plan."""
    safe_topic = (topic or "").strip() or "AI Benchmark"
    safe_plan = plan if isinstance(plan, dict) else {"topic": safe_topic, "mode": "课程实验"}
    try:
        results = _collect_search_results(safe_topic, safe_plan)
        report = _build_report_from_results(safe_topic, safe_plan, results)
        if not report.strip():
            return _fallback_report(safe_topic, safe_plan)
        return report
    except Exception:
        return _fallback_report(safe_topic, safe_plan)
