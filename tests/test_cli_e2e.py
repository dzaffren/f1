def test_scores_bahrain_2024(run_f1):
    result = run_f1("score", "--season", "2024", "--round", "1")

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    lines = result.stdout.splitlines()
    assert lines[0] == "2024 Bahrain Grand Prix (round 1)"
    assert "Drivers scored: 20" in lines
    assert lines[-1] == "Mean position error: 2.30 places"
