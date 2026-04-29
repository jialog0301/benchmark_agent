"""Cache management for BenchmarkRadarAgent."""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CACHE_DIR = BASE_DIR / "data" / "cache"


def _sanitize_topic(topic: str) -> str:
    """Convert topic to safe directory name."""
    return topic.lower().replace(" ", "_").replace("/", "_")


def get_cache_dir(topic: str) -> Path:
    """Get cache directory for a topic."""
    topic_dir = CACHE_DIR / _sanitize_topic(topic)
    topic_dir.mkdir(parents=True, exist_ok=True)
    return topic_dir


def load_cache(topic: str, filename: str):
    """Load cached data from JSON file."""
    cache_file = get_cache_dir(topic) / filename
    if not cache_file.exists():
        return None

    if filename.endswith(".json"):
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    elif filename.endswith(".md"):
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read()
    return None


def save_cache(topic: str, filename: str, data) -> None:
    """Save data to cache file."""
    cache_file = get_cache_dir(topic) / filename
    cache_file.parent.mkdir(parents=True, exist_ok=True)

    if filename.endswith(".json"):
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    elif filename.endswith(".md"):
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(data)


def get_all_cached_topics() -> list[str]:
    """List all topics with cached data."""
    if not CACHE_DIR.exists():
        return []
    return [d.name for d in CACHE_DIR.iterdir() if d.is_dir()]
