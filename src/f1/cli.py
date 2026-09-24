import argparse
import os
import sys
from pathlib import Path

from f1.baseline import score_grid
from f1.data import DataError, load_race


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="f1")
    commands = parser.add_subparsers(dest="command", required=True)
    score = commands.add_parser(
        "score", help='Score the "finishing order = starting grid" guess for one Grand Prix.'
    )
    score.add_argument("--season", type=int, required=True, metavar="YEAR")
    score.add_argument("--round", type=int, required=True, metavar="N")
    args = parser.parse_args(argv)

    cache_dir = Path(os.environ.get("F1_CACHE_DIR", ".cache/fastf1"))
    try:
        race = load_race(args.season, args.round, cache_dir)
    except DataError as err:
        print(err, file=sys.stderr)
        return 1
    table, mean = score_grid(race.results)

    print(f"{race.season} {race.event_name} (round {race.round})")
    print("Guess: finishing order = starting grid")
    print()
    print(f"{'Driver':<6}  {'Grid':>4}  {'Finish':>6}  {'Off':>3}  Status")
    for row in table.itertuples():
        print(f"{row.Driver:<6}  {row.Grid:>4}  {row.Finish:>6}  {row.Off:>3}  {row.Status}")
    print()
    print(f"Drivers scored: {len(table)}")
    print(f"Mean position error: {mean:.2f} places")
    return 0


if __name__ == "__main__":
    sys.exit(main())
