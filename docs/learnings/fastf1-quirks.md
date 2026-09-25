# FastF1 quirks

Confirmed against FastF1 3.8.3 on 2026-09-25 (POC and walking-skeleton build).

- `Cache.enable_cache` raises `NotADirectoryError` if the folder is missing. Create it first.
- Loading a race that hasn't run, and a race that failed to fetch, both return an
  empty `results` table with no error. Tell them apart by the race start date.
- With no network and no cached schedule, `get_event_schedule` raises a plain
  `ValueError("Failed to load any schedule data.")`, the same type
  `get_event_by_round` raises for a bad round. Map errors by call site.
- A pit-lane start is `GridPosition == 0.0`. A driver who never started is still
  listed, with `Status == "Withdrew"` and grid 0.
- Cache entries expire after 12h but are served stale on network errors.
  `requests_cache` logs a traceback when it does that. Silence its logger.
- `set_log_level("ERROR")` does not cover Python `UserWarning`s from the ergast module.
- F1 live timing ("Failed to load session info data!") failed from this laptop.
  Results still load via Jolpica. Recheck before any slice that needs lap timing.
- Never call `requests_cache` `SQLiteCache.reset_expiration()` on a cache whose
  entries have expired: it rewrites rows under a live cursor and loops forever.
  Materialise `list(cache.filter())` first. Passed during build, hung at review.
