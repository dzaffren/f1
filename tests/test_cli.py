from pathlib import Path

from f1.cli import DEFAULT_CACHE_DIR

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_default_cache_is_at_repo_root():
    assert DEFAULT_CACHE_DIR == REPO_ROOT / ".cache" / "fastf1"
