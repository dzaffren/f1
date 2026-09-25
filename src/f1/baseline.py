"""The grid baseline: guess that every driver finishes where they started."""

import pandas as pd

PIT_LANE = 0


def score_grid(results: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    """Return the per-driver table and the mean position error.

    Drivers who withdrew never started, so they are left out. A pit-lane
    start (grid 0) counts as the last grid slot and shows as "PL".
    """
    started = results[results["Status"] != "Withdrew"]
    grid = started["GridPosition"].astype(int)
    grid_slot = grid.where(grid != PIT_LANE, len(started))
    finish = started["Position"].astype(int)
    table = pd.DataFrame(
        {
            "Driver": started["Abbreviation"],
            "Grid": grid.astype(object).where(grid != PIT_LANE, "PL"),
            "Finish": finish,
            "Off": (finish - grid_slot).abs(),
            "Status": started["Status"],
        }
    ).sort_values("Finish")
    return table.reset_index(drop=True), float(table["Off"].mean())
