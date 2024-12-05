from itertools import pairwise

from aoc import parsers
from aoc.parsers import transform


def is_safe(report: tuple[int, ...]):
    diffs = [a - b for a, b in pairwise(report)]
    return all(d in range(1, 4) for d in diffs) or all(d in range(-3, 0) for d in diffs)


def is_safe_with_dampener(report: tuple[int, ...]):
    if is_safe(report):
        return True

    for pos in range(len(report)):
        if is_safe(report[:pos] + report[pos + 1 :]):
            return True

    return False


@transform(parsers.number_lines)
def part_1(reports: list[list[int]]):
    safe_reports = [r for r in reports if is_safe(tuple(r))]
    return len(safe_reports)


@transform(parsers.number_lines)
def part_2(reports: list[list[int]]):
    safe_reports = [r for r in reports if is_safe_with_dampener(tuple(r))]
    return len(safe_reports)
