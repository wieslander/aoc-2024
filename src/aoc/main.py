import sys
from datetime import datetime

from aoc.solver import solve
from aoc.types import PuzzlePart


def parse_day(args: list[str]):
    if args:
        return int(args[0])
    else:
        today = datetime.now()
        if today.month == 12:
            return today.day
    raise ValueError("Cannot determine puzzle from today's date")


def parse_part(args: list[str]) -> PuzzlePart | None:
    if len(args) >= 2:
        part = int(args[1])
        if part not in (1, 2):
            raise ValueError(f"Invalid puzzle part {part}")
        return part


def parse_example(args: list[str]):
    return len(args) > 0 and args[-1] == "--example"


def main():
    args = sys.argv[1:]
    day = parse_day(args)
    part = parse_part(args)
    example = parse_example(args)
    solve(day, part, example)


if __name__ == "__main__":
    main()
