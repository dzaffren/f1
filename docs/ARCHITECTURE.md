# F1 · architecture

**Status:** Active · **Updated:** 2026-09-25 by /ship walking-skeleton

## Context

```mermaid
flowchart LR
    U((you)) -- "f1 score" --> P[F1] -- "results" --> J[(Jolpica via FastF1)]
    P -- "per-driver table + mean position error" --> U
```

## Components

```mermaid
flowchart LR
    C[cli.py] -- "season, round" --> D[data.py]
    D -- "results table" --> C
    C -- "results table" --> B[baseline.py]
    B -- "table + mean" --> C
    D -- "load, cache" --> F[(fastf1 + .cache/fastf1)]
```

| Component   | Folder    | Does |
| ----------- | --------- | ---- |
| cli.py      | `src/f1/` | Parses flags, prints the table, turns data errors into one line and exit 1 |
| data.py     | `src/f1/` | The only FastF1 caller: loads one race, raises NoSuchRound / NoResultsYet / FetchFailed |
| baseline.py | `src/f1/` | Scores the grid guess: drops withdrawals, pit-lane as last slot, mean position error |
