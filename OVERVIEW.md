# F1

**Status:** Active · **Updated:** 2026-09-25 by /ship walking-skeleton

Machine learning models that predict Formula 1 qualifying and race results.
User: the repo owner.

## Run it

| Task    | Command                                              |
| ------- | ---------------------------------------------------- |
| install | `uv sync` (README.md)                                |
| run     | `uv run f1 score --season 2024 --round 1` (README.md) |
| test    | `uv run pytest` (.github/workflows/ci.yml)           |
| lint    | `uv run ruff check . && uv run ruff format --check .` (.github/workflows/ci.yml) |

## Where things are

- `src/f1/` — the `f1` package: CLI, FastF1 data loading, baseline scoring
- `tests/` — pytest suite; `tests/fixtures/` holds the saved FastF1 cache and its capture script
- `docs/specs/` — shape doc and per-slice specs
- `docs/learnings/` — lessons from building
- `.github/workflows/` — CI

## Slices

| Slice            | Status | What it does | Page |
| ---------------- | ------ | ------------ | ---- |
| walking-skeleton | Built  | One command scores the "race finishes in grid order" guess for a past Grand Prix | https://claude.ai/artifact/7c9ssmGM6CuK39ab7j6951 |

## More

docs/ARCHITECTURE.md
