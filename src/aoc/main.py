from argparse import ArgumentParser
from datetime import datetime

from aoc.solver import solve
from aoc.types import PuzzlePart


def puzzle_day(value: str):
    if value:
        return int(value)
    else:
        today = datetime.now()
        if today.month == 12:
            return today.day
    raise ValueError("Cannot determine puzzle from today's date")


def puzzle_part(value: str) -> PuzzlePart | None:
    if value:
        part = int(value)
        if part not in (1, 2):
            raise ValueError(f"Invalid puzzle part {part}")
        return part


def main():
    parser = ArgumentParser()
    parser.add_argument("day", nargs="?", default="", type=puzzle_day)
    parser.add_argument("part", nargs="?", default="", type=puzzle_part)
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    solve(args.day, args.part, args.example)


if __name__ == "__main__":
    main()
