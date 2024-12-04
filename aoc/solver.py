import importlib

import aocd
from aocd.models import Puzzle

from aoc import parsers
from aoc.types import PuzzlePart, Result

YEAR = 2024


def aocd_part(part: PuzzlePart) -> aocd.types.PuzzlePart:
    part_mapping: dict[PuzzlePart, aocd.types.PuzzlePart] = {1: "a", 2: "b"}
    return part_mapping[part]


class Solver:
    def __init__(self, day: int):
        self._day = day
        self._puzzle = Puzzle(year=YEAR, day=self._day)
        self._solver_module = self._get_solver_module()

    def solve_part(self, part: PuzzlePart, print_title: bool = True):
        if print_title:
            self._print_title()
        result = self._solve(part)
        if result is not None:
            print(f" - part {part}: {result}")
            aocd.submit(answer=str(result), day=self._day, part=aocd_part(part))

    def solve_all(self):
        self._print_title()
        self.solve_part(part=1, print_title=False)
        self.solve_part(part=2, print_title=False)

    def _print_title(self):
        print(f"Day {self._day} - {self._puzzle.title}")

    def _solve(self, part: PuzzlePart) -> Result | None:
        solver_function = self._get_solver_function(part)
        if not solver_function:
            return None
        parsed_input = self._parse_input()
        return solver_function(parsed_input)

    def _parse_input(self):
        parser = self._get_parser()
        return parser(self._puzzle.input_data)

    def _get_parser(self):
        return getattr(self._solver_module, "parse", parsers.raw)

    def _get_solver_function(self, part: PuzzlePart):
        part_name = f"part_{part}"
        return getattr(self._solver_module, part_name, None)

    def _get_solver_module(self):
        module_name = f"days.{self._day:02}"
        return importlib.import_module(module_name)


def solve(day: int, part: PuzzlePart | None):
    solver = Solver(day)
    if part:
        solver.solve_part(part)
    else:
        solver.solve_all()
