import pandas as pd
import pytest

from f1.data import FetchFailed, NoResultsYet, load_race

TODAY = pd.Timestamp("2026-09-25")


def test_unrun_race(cache_dir, offline):
    with pytest.raises(NoResultsYet) as err:
        load_race(2026, 15, cache_dir, now=TODAY)

    assert str(err.value) == "No results yet for 2026 round 15"


def test_past_race_empty_results_is_fetch_failure(cache_dir, offline):
    # The 2024 schedule is cached but round 2 is not, so the race load fails
    # quietly and FastF1 returns an empty table.
    with pytest.raises(FetchFailed) as err:
        load_race(2024, 2, cache_dir, now=TODAY)

    assert str(err.value) == (
        "Could not fetch 2024 round 2: no network and nothing cached. "
        "The first run for a race needs internet."
    )
