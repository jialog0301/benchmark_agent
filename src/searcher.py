
"""Search Agent module."""

from __future__ import annotations

import copy
import os
from datetime import datetime, timezone
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
MAX_BENCHMARKS = 8
MIN_BENCHMARKS = 5
MISSING_VALUE = "未找到"


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
    return {
        "name": name,
        "aliases": aliases,
        "source": source,
        "description": f"{name} benchmark candidate.",
        "task_type": task_type,
        "evaluated_ability": abilities,
        "metrics": metrics,
        "paper_url": paper_url,
        "code_url": code_url,
        "dataset_url": dataset_url,
        "leaderboard_url": leaderboard_url,
        "open_source": open_source,
        "resource_completeness": "medium",
        "reproduction_difficulty": "medium",
        "fit_for_course_lab": "medium",
        "fit_for_research_survey": "high",
        "fit_for_quick_reproduction": "medium",
        "evidence_links": evidence_links or [],
    }


AGENT_CURATED_BENCHMARKS: list[dict[str, Any]] = [
    _bm("AgentBench", ["agentbench"], "LLM-as-Agent Evaluation", ["reasoning", "tool interaction"], ["task success"], "arXiv + GitHub", paper_url="https://arxiv.org/abs/2308.03688", code_url="https://github.com/THUDM/AgentBench", open_source=True, evidence_links=["https://arxiv.org/abs/2308.03688", "https://github.com/THUDM/AgentBench"]),
    _bm("WebArena", ["webarena", "web-arena"], "Web Agent Evaluation", ["web navigation", "planning", "tool use"], ["task success rate"], "arXiv + GitHub + website", paper_url="https://arxiv.org/abs/2307.13854", code_url="https://github.com/web-arena-x/webarena", leaderboard_url="https://webarena.dev/", open_source=True, evidence_links=["https://arxiv.org/abs/2307.13854", "https://github.com/web-arena-x/webarena", "https://webarena.dev/"]),
    _bm("SWE-bench", ["swe-bench", "swebench"], "Software Engineering Agent Evaluation", ["issue resolution", "patch generation"], ["resolved issue rate"], "arXiv + GitHub + leaderboard", paper_url="https://arxiv.org/abs/2310.06770", code_url="https://github.com/swe-bench/SWE-bench", leaderboard_url="https://www.swebench.com/", open_source=True, evidence_links=["https://arxiv.org/abs/2310.06770", "https://github.com/swe-bench/SWE-bench", "https://www.swebench.com/"]),
    _bm("GAIA", ["gaia", "gaia-benchmark"], "General Assistant / Agent Evaluation", ["reasoning", "web browsing", "tool use"], ["accuracy"], "arXiv + HF", paper_url="https://arxiv.org/abs/2311.12983", dataset_url="https://huggingface.co/datasets/gaia-benchmark/GAIA", leaderboard_url="https://huggingface.co/spaces/gaia-benchmark/leaderboard", evidence_links=["https://arxiv.org/abs/2311.12983", "https://huggingface.co/datasets/gaia-benchmark/GAIA", "https://huggingface.co/spaces/gaia-benchmark/leaderboard"]),
    _bm("OSWorld", ["osworld", "os-world"], "Computer-use Agent Evaluation", ["GUI operation", "desktop task solving"], ["task success rate"], "arXiv + GitHub + website", paper_url="https://arxiv.org/abs/2404.07972", code_url="https://github.com/xlang-ai/OSWorld", leaderboard_url="https://os-world.github.io/", open_source=True, evidence_links=["https://arxiv.org/abs/2404.07972", "https://github.com/xlang-ai/OSWorld", "https://os-world.github.io/"]),
    _bm("ToolBench", ["toolbench"], "Tool-use Agent Evaluation", ["API selection", "tool use"], ["pass rate"], "GitHub", code_url="https://github.com/OpenBMB/ToolBench", open_source=True, evidence_links=["https://github.com/OpenBMB/ToolBench"]),
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
        from duckduckgo_search import DDGS
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
            f"{topic} SWE-bench Verified HumanEval MBPP BigCodeBench RepoBench",
            f"{topic} coding agent benchmark github leaderboard",
            f"{topic} software engineering agent evaluation dataset metrics",
        ]
    if topic_type == "agent":
        return [
            f"{topic} AgentBench WebArena SWE-bench GAIA OSWorld ToolBench",
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
        url = str(item.get("url", "")).strip()
        if url and url not in seen_urls:
            seen_urls.add(url)
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
        url = str(result.get("url", "")).strip()
        if not url:
            continue
        if url not in candidate.get("evidence_links", []):
            candidate.setdefault("evidence_links", []).append(url)

        link_type = _classify_link(url)
        if link_type in {"paper_url", "code_url", "dataset_url", "leaderboard_url"}:
            current = str(candidate.get(link_type, MISSING_VALUE)).strip()
            if not current or current in {MISSING_VALUE, "null"}:
                candidate[link_type] = url

    ordered: list[dict] = [by_name[n] for n in matched]
    for item in base:
        if item["name"] not in matched:
            ordered.append(item)

    if len(ordered) < MIN_BENCHMARKS:
        ordered.extend(copy.deepcopy(AGENT_CURATED_BENCHMARKS))

    deduped: list[dict] = []
    seen: set[str] = set()
    for item in ordered:
        name = str(item.get("name", "")).strip()
        if name and name not in seen:
            seen.add(name)
            deduped.append(item)
    return deduped[:MAX_BENCHMARKS]


def _render_list(value: list[str]) -> str:
    """Render list as comma-separated text."""
    cleaned = [str(x).strip() for x in value if str(x).strip()]
    return ", ".join(cleaned) if cleaned else MISSING_VALUE


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
        lines.append(f"- {MISSING_VALUE}")

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
    for index, bm in enumerate(candidates, start=1):
        evidence_links: list[str] = []
        for link in bm.get("evidence_links", []):
            link_text = str(link).strip()
            if link_text and link_text not in evidence_links:
                evidence_links.append(link_text)
        evidence_links = evidence_links[:MAX_EVIDENCE_LINKS]

        lines.extend(
            [
                f"### Benchmark {index}: {bm['name']}",
                f"- name: {bm['name']}",
                f"- source: {bm.get('source', MISSING_VALUE)}",
                f"- description: {bm.get('description', MISSING_VALUE)}",
                f"- task_type: {bm.get('task_type', MISSING_VALUE)}",
                f"- evaluated_ability: {_render_list(bm.get('evaluated_ability', []))}",
                f"- metrics: {_render_list(bm.get('metrics', []))}",
                f"- paper_url: {bm.get('paper_url', MISSING_VALUE)}",
                f"- code_url: {bm.get('code_url', MISSING_VALUE)}",
                f"- dataset_url: {bm.get('dataset_url', MISSING_VALUE)}",
                f"- leaderboard_url: {bm.get('leaderboard_url', MISSING_VALUE)}",
                f"- open_source: {_to_bool_text(bm.get('open_source'))}",
                f"- resource_completeness_initial: {bm.get('resource_completeness', MISSING_VALUE)}",
                f"- reproduction_difficulty_initial: {bm.get('reproduction_difficulty', MISSING_VALUE)}",
                f"- fit_for_course_lab_initial: {bm.get('fit_for_course_lab', MISSING_VALUE)}",
                f"- fit_for_research_survey_initial: {bm.get('fit_for_research_survey', MISSING_VALUE)}",
                f"- fit_for_quick_reproduction_initial: {bm.get('fit_for_quick_reproduction', MISSING_VALUE)}",
                "- evidence_links:",
            ]
        )
        if evidence_links:
            lines.extend([f"  - {link}" for link in evidence_links])
        else:
            lines.append(f"  - {MISSING_VALUE}")
        lines.append("")

    lines.extend([
        "## Notes",
        "- Searcher 仅提供事实型调研信息，不输出最终推荐排序。",
        "- 缺失链接已标注为‘未找到’或 null，未编造 URL。",
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
