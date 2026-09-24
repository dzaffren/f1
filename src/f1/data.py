"""Race data from FastF1. The only module that imports fastf1."""

import logging
import warnings
from dataclasses import dataclass
from pathlib import Path

import fastf1
import pandas as pd

fastf1.set_log_level("ERROR")
# requests_cache logs a full traceback at WARNING whenever it serves a stale
# entry because the network failed. The stale entry is the right answer.
logging.getLogger("requests_cache").setLevel(logging.ERROR)


@dataclass
class RaceResult:
    season: int
    round: int
    event_name: str
    results: pd.DataFrame


def load_race(season: int, round_: int, cache_dir: Path) -> RaceResult:
    cache_dir.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(cache_dir))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        schedule = fastf1.get_event_schedule(season, include_testing=False)
        event = schedule.get_event_by_round(round_)
        race = event.get_race()
        race.load(laps=False, telemetry=False, weather=False, messages=False)
    results = pd.DataFrame(race.results[["Abbreviation", "GridPosition", "Position", "Status"]])
    return RaceResult(season, round_, event.EventName, results)
