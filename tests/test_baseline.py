import pandas as pd
import pytest

from f1.baseline import score_grid


def results(*rows):
    return pd.DataFrame(rows, columns=["Abbreviation", "GridPosition", "Position", "Status"])


def test_pit_lane_start_counts_as_last_grid_slot():
    table, mean = score_grid(
        results(
            ("VER", 1.0, 1.0, "Finished"),
            ("NOR", 2.0, 2.0, "Finished"),
            ("OCO", 0.0, 3.0, "Lapped"),
        )
    )

    oco = table.set_index("Driver").loc["OCO"]
    assert oco["Grid"] == "PL"
    assert oco["Off"] == 0
    assert mean == 0.0


def test_retirement_is_scored_at_classified_position():
    table, mean = score_grid(
        results(
            ("SAI", 2.0, 1.0, "Finished"),
            ("LEC", 3.0, 2.0, "Finished"),
            ("VER", 1.0, 3.0, "Retired"),
        )
    )

    assert table["Driver"].tolist() == ["SAI", "LEC", "VER"]
    assert table.set_index("Driver").loc["VER", "Off"] == 2
    assert mean == pytest.approx(4 / 3)


def test_withdrew_is_dropped():
    table, mean = score_grid(
        results(
            ("HAM", 1.0, 1.0, "Finished"),
            ("RUS", 2.0, 2.0, "Finished"),
            ("STR", 0.0, 3.0, "Withdrew"),
        )
    )

    assert table["Driver"].tolist() == ["HAM", "RUS"]
    assert mean == 0.0
