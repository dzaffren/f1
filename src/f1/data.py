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


class DataError(Exception):
    """A race could not be loaded. The message is shown to the user as is."""


class NoSuchRound(DataError):
    pass


class NoResultsYet(DataError):
    pass


class FetchFailed(DataError):
    def __init__(self, season: int, round_: int):
        super().__init__(
            f"Could not fetch {season} round {round_}: no network and nothing cached. "
            "The first run for a race needs internet."
        )


@dataclass
class RaceResult:
    season: int
    round: int
    event_name: str
    results: pd.DataFrame


def load_race(
    season: int, round_: int, cache_dir: Path, now: pd.Timestamp | None = None
) -> RaceResult:
    """Load one Grand Prix's results.

    FastF1 returns an empty table both for a race that hasn't run and for a
    race it couldn't fetch, so the race start time decides which it is.
    """
    now = now if now is not None else pd.Timestamp.now(tz="UTC").tz_localize(None)
    cache_dir.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(cache_dir))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            schedule = fastf1.get_event_schedule(season, include_testing=False)
        except ValueError as err:
            raise FetchFailed(season, round_) from err
        try:
            event = schedule.get_event_by_round(round_)
        except ValueError as err:
            rounds = schedule["RoundNumber"]
            raise NoSuchRound(
                f"{season} has no round {round_} (rounds {rounds.min()} to {rounds.max()})"
            ) from err
        race = event.get_race()
        race.load(laps=False, telemetry=False, weather=False, messages=False)

    if race.results.empty:
        if event["Session5DateUtc"] > now:
            raise NoResultsYet(f"No results yet for {season} round {round_}")
        raise FetchFailed(season, round_)
    results = pd.DataFrame(race.results[["Abbreviation", "GridPosition", "Position", "Status"]])
    return RaceResult(season, round_, event.EventName, results)
