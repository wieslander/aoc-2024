import re

from aoc.geometry import Point
from aoc.parsers import transform

coord_pattern = r".*X[+=](?P<x>\d+), Y[+=](?P<y>\d+)"


class Machine:
    def __init__(self, input: str):
        lines = input.split("\n")
        matches = [re.match(coord_pattern, line) for line in lines]
        self.a, self.b, self.prize = [
            Point(int(m.group("x")), int(m.group("y")))
            for m in matches
            if m is not None
        ]


def parse_machines(input: str):
    machine_blocks = input.split("\n\n")
    return [Machine(block) for block in machine_blocks]


def min_tokens_to_win(machine: Machine):
    prize = machine.prize
    btn_a = machine.a
    btn_b = machine.b
    b_numerator = prize.x * btn_a.y - prize.y * btn_a.x
    b_denominator = btn_b.x * btn_a.y - btn_b.y * btn_a.x
    if b_numerator % b_denominator != 0:
        return 0

    b = b_numerator // b_denominator
    a_numerator = prize.x - btn_b.x * b
    a_denominator = btn_a.x
    if a_numerator % a_denominator != 0:
        return 0

    a = a_numerator // a_denominator

    return a * 3 + b


@transform(parse_machines)
def part_1(machines: list[Machine]):
    return sum(min_tokens_to_win(m) for m in machines)


@transform(parse_machines)
def part_2(machines: list[Machine]):
    for m in machines:
        m.prize.x += 10_000_000_000_000
        m.prize.y += 10000000000000
    return sum(min_tokens_to_win(m) for m in machines)
