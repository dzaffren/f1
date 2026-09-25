"""Rebuild tests/fixtures/fastf1_cache from the network.

Run once by hand: uv run python tests/fixtures/capture.py
Not run in CI. The unrun race (2026 round 15) must be captured before it
runs on 2026-09-26, so its results are empty in the fixture.
"""

import shutil
from pathlib import Path

import fastf1

CACHE = Path(__file__).parent / "fastf1_cache"
RACES = [(2024, 1), (2024, 3), (2026, 15)]


def main() -> None:
    shutil.rmtree(CACHE, ignore_errors=True)
    CACHE.mkdir()
    fastf1.Cache.enable_cache(str(CACHE))
    for season, round_ in RACES:
        schedule = fastf1.get_event_schedule(season, include_testing=False)
        race = schedule.get_event_by_round(round_).get_race()
        race.load(laps=False, telemetry=False, weather=False, messages=False)
        print(season, round_, race.event.EventName, len(race.results), "results")


if __name__ == "__main__":
    main()
