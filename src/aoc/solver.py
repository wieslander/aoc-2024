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
    def __init__(self, day: int, example: bool = False):
        self._day = day
        self._puzzle = Puzzle(year=YEAR, day=self._day)
        self._solver_module = self._get_solver_module()
        self._example = example

    def solve_part(self, part: PuzzlePart, print_title: bool = True):
        if print_title:
            self._print_title()
        result = self._solve(part)
        if result is not None:
            self._handle_result(part, result)

    def solve_all(self):
        self._print_title()
        self.solve_part(part=1, print_title=False)
        self.solve_part(part=2, print_title=False)

    def _print_title(self):
        print(f"Day {self._day} - {self._puzzle.title}")

    def _handle_result(self, part: PuzzlePart, result: Result):
        print(f" - part {part}: {result}")
        serialized_result = str(result)

        if self._example:
            example_answer = self._get_example_answer(part)
            if serialized_result == example_answer:
                print("   That's the correct answer for the example!")
            else:
                print(
                    f"   That's not the right answer.  The correct answer is {example_answer}"
                )
        else:
            aocd.submit(answer=serialized_result, day=self._day, part=aocd_part(part))

    def _get_example_answer(self, part: PuzzlePart):
        example = self._get_example(part)
        if part == 1:
            return example.answer_a
        else:
            return example.answer_b

    def _solve(self, part: PuzzlePart) -> Result | None:
        solver_function = self._get_solver_function(part)
        if not solver_function:
            return None
        parsed_input = self._parse_input(part)
        return solver_function(parsed_input)

    def _parse_input(self, part: PuzzlePart):
        parser = self._get_parser()
        return parser(self._get_raw_input(part))

    def _get_raw_input(self, part: PuzzlePart):
        if self._example:
            example = self._get_example(part)
            return example.input_data
        else:
            return self._puzzle.input_data

    def _get_example(self, part: PuzzlePart):
        required_attribute = f"answer_{aocd_part(part)}"
        for example in self._puzzle.examples:
            if getattr(example, required_attribute) is not None:
                return example
        raise ValueError(f"Could not find any example for part {part}")

    def _get_parser(self):
        return getattr(self._solver_module, "parse", parsers.raw)

    def _get_solver_function(self, part: PuzzlePart):
        part_name = f"part_{part}"
        return getattr(self._solver_module, part_name, None)

    def _get_solver_module(self):
        module_name = f"aoc.days.{self._day:02}"
        return importlib.import_module(module_name)


def solve(day: int, part: PuzzlePart | None, example: bool = False):
    solver = Solver(day, example)
    if part:
        solver.solve_part(part)
    else:
        solver.solve_all()
