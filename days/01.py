from aoc import parsers


def parse(input: str):
    lines = parsers.number_lines(input)
    return tuple(map(sorted, zip(*lines, strict=True)))


def similarity_score(n: int, right: list[int]):
    return n * sum(1 for x in right if x == n)


def part_1(location_lists: tuple[list[int], list[int]]):
    return sum(map(lambda a, b: abs(a - b), *location_lists))


def part_2(location_lists: tuple[list[int], list[int]]):
    left, right = location_lists
    return sum(similarity_score(n, right) for n in left)
