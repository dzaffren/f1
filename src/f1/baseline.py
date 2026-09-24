"""The grid baseline: guess that every driver finishes where they started."""

import pandas as pd


def score_grid(results: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    """Return the per-driver table and the mean position error."""
    table = pd.DataFrame(
        {
            "Driver": results["Abbreviation"],
            "Grid": results["GridPosition"].astype(int),
            "Finish": results["Position"].astype(int),
            "Status": results["Status"],
        }
    ).sort_values("Finish")
    table["Off"] = (table["Finish"] - table["Grid"]).abs()
    return table.reset_index(drop=True), float(table["Off"].mean())
