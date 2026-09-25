def test_scores_bahrain_2024(run_f1):
    result = run_f1("score", "--season", "2024", "--round", "1")

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    lines = result.stdout.splitlines()
    assert lines[0] == "2024 Bahrain Grand Prix (round 1)"
    assert "Drivers scored: 20" in lines
    assert lines[-1] == "Mean position error: 2.30 places"


def test_retirement_is_scored(run_f1):
    result = run_f1("score", "--season", "2024", "--round", "3")

    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    assert "Drivers scored: 19" in lines
    assert lines[-1] == "Mean position error: 3.89 places"
    ver = next(line for line in lines if line.startswith("VER"))
    assert ver.split() == ["VER", "1", "19", "18", "Retired"]


def test_round_out_of_range(run_f1):
    result = run_f1("score", "--season", "2024", "--round", "25")

    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == "2024 has no round 25 (rounds 1 to 24)\n"


def test_offline_empty_cache(run_f1, tmp_path):
    result = run_f1("score", "--season", "2024", "--round", "1", cache=tmp_path / "empty")

    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == (
        "Could not fetch 2024 round 1: no network and nothing cached. "
        "The first run for a race needs internet.\n"
    )


def test_missing_flag(run_f1):
    result = run_f1("score", "--season", "2024")

    assert result.returncode == 2
    assert "the following arguments are required: --round" in result.stderr
