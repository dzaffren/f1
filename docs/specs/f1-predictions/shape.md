# F1 predictions

**Project type:** Data app (greenfield) · **Status:** Shaped

## Problem
You want to learn machine learning on a problem you care about: predicting
F1 qualifying order, then race order, before the weekend. The learning only
counts if you can tell whether a model beats a naive guess, and nothing
measures that today.

## Today

```
  public F1 data                         you
  (results, grids, timing)  ──── ✗ ────▶ (some ML, want to learn)
                              │
                              └─ pain: no predictions, no baseline,
                                 no honest score to learn from
```

The data exists publicly. Nothing turns it into predictions, and nothing scores them.

## Slices

```
 [0] skeleton ──▶ [1] baseline scoreboard ──┬──▶ [2] race model (real grid) ──┐
                                            │                                 ├──▶ [4] full weekend ──▶ [5] live 2026
                                            └──▶ [3] quali model ─────────────┘
```

Slices 2 and 3 both need only slice 1. They can be built in either order.
Slice 4 needs both.

| # | Slice | What ships | Why this order |
|---|-------|-----------|----------------|
| 0 | Walking skeleton | One command pulls one past race, scores "race order = grid order", prints the score. One test. CI runs it. | Empty repo. Proves the data source, stack, and test rails before any ML. |
| 1 | Baseline scoreboard | Backtest of both naive baselines across past seasons: quali = previous race's quali order, race = grid order. One table of scores. | Every later model is judged against this. It also settles the metric. |
| 2 | Race model, real grid known | First trained model: predicts race order after quali. Walk-forward backtest, scored next to the grid baseline. | Easiest real ML problem here. The grid is a strong feature, so the first model has something solid to beat. |
| 3 | Quali model | Predicts quali order before the weekend. Backtested against the previous-race baseline. | Needed before slice 4. Doesn't depend on slice 2. |
| 4 | Full weekend prediction | Quali prediction feeds the race model as a predicted grid. Backtested end to end. | This is the "e2e" goal. It needs both models. |
| 5 | Live 2026 predictions | Predicts an upcoming race before the weekend, then scores itself once results are in. | Last because it's only worth trusting after slices 1 to 4 show the model beats the baseline. |

Terms:
- **Walk-forward backtest:** train only on races before race N, predict race N,
  move to N+1. It stops the model seeing the future. That leak is the most
  common way a first ML project fools itself.
- **Baseline:** the naive guess a model has to beat to have learned anything.

## Not doing

| Considered | Why not |
|---|---|
| Beat bookmaker odds | Rejected for now. The goal is learning, and the baseline is the honest test. Odds data can come after slice 5. |
| A hit-rate target (e.g. top-3 right X% of the time) | You picked the baseline instead. A fixed target says nothing without one. |
| Web dashboard | Not needed to learn ML. Terminal output and notebooks are enough. |
| Lap-by-lap or strategy simulation | A different problem, and a much bigger one. |
| Deep learning | Not needed to beat these baselines. Pick it later only if a simpler model hits a wall. |

## Open items

| ID | What | Type | Raised at | Owner | Status | Answer |
| -- | ---- | ---- | --------- | ----- | ------ | ------ |
| O1 | "e2e" read as: quali prediction feeds race prediction, run as a backtest on past seasons and live on 2026 races | assumption | shape | user | Open | — |
| O2 | Which data source: FastF1, the Jolpica API, a Kaggle dump, or something else. Decide on coverage, rate limits and licence | question | shape | spec 0 | Resolved | FastF1 3.8.3, results via Jolpica (walking-skeleton spec, 2026-09-25) |
| O3 | Stack: language, libraries, CI host (GitHub or GitLab), where it runs | question | shape | spec 0 | Resolved | Python, pandas, scikit-learn, uv, pytest, ruff, GitHub Actions. CLI, plus Jupyter for exploring |
| O4 | 2026 brought major new technical regulations. Models trained on earlier seasons may not carry over to 2026 | flag | shape | user | Open | — |
| O5 | Which scoring metric: rank correlation, mean position error, top-N hit rate, or several | question | shape | spec 1 | Resolved | Mean position error. Slice 1 may add more |
| O6 | How DNFs, DSQs and pit-lane starts count, in both the scoring and the features | question | shape | spec 1 | Resolved | Official classification for everyone. Grid 0 counts as the last grid slot |
| O7 | Which seasons to train and backtest on | question | shape | spec 1 | Open | — |
| O8 | Assuming personal use only, run on your laptop. "Deployed" means a runnable command plus CI, not a hosted service | assumption | shape | user | Resolved | Confirmed 2026-09-25 |
| O9 | Assuming "some ML" means comfortable with pandas and scikit-learn. Slices explain modelling choices, not Python basics | assumption | shape | user | Open | — |
