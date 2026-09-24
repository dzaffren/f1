# F1

Predict Formula 1 qualifying and race results, and score every prediction
against a naive baseline.

## Setup

Needs [uv](https://docs.astral.sh/uv/).

```
uv sync
```

## Score the grid baseline for one race

```
uv run f1 score --season 2024 --round 1
```

Prints each driver's grid slot, finishing position and how many places they
moved, then the mean position error of the guess "race finishes in grid
order". The first run for a race needs internet; race data is cached in
`.cache/fastf1/` after that.

## Tests and lint

```
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Explore in Jupyter

```
uv run jupyter lab
```
