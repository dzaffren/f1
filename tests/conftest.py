import datetime
import os
import shutil
import subprocess
from pathlib import Path

import pytest
import requests_cache

FIXTURE_CACHE = Path(__file__).parent / "fixtures" / "fastf1_cache"
DEAD_PROXY = "http://127.0.0.1:9"


@pytest.fixture
def cache_dir(tmp_path):
    """A copy of the fixture cache with every entry expired.

    CI always runs more than 12 hours after capture, when FastF1's cache
    entries have expired and are only served because the network fails.
    Expiring them here makes every run take that same path.
    """
    target = tmp_path / "fastf1_cache"
    shutil.copytree(FIXTURE_CACHE, target)
    cache = requests_cache.SQLiteCache(str(target / "fastf1_http_cache.sqlite"))
    # Not cache.reset_expiration(): it rewrites rows while a cursor is still
    # reading them, and once the entries have expired the rewritten rows sort
    # ahead of the cursor and the loop never ends. Read them all first.
    for response in list(cache.filter()):
        response.reset_expiration(datetime.timedelta(seconds=-1))
        cache.responses[response.cache_key] = response
    return target


@pytest.fixture
def offline(monkeypatch):
    """Point every HTTP request at a closed port so nothing reaches the internet."""
    for var in ("HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy"):
        monkeypatch.setenv(var, DEAD_PROXY)
    for var in ("NO_PROXY", "no_proxy"):
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def run_f1(cache_dir, offline):
    def run(*args, cache=None):
        env = {**os.environ, "F1_CACHE_DIR": str(cache or cache_dir)}
        return subprocess.run(
            [shutil.which("f1"), *args], capture_output=True, text=True, env=env, timeout=60
        )

    return run
