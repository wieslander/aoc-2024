from aoc import parsers


def parse(input: str):
    lines = [line.split(":") for line in parsers.lines(input)]
    return [(int(result), parsers.numbers(operands)) for result, operands in lines]


def is_valid(result: int, operands: list[int], allow_concat: bool = False) -> bool:
    if len(operands) == 1:
        return operands[0] == result

    a, b, *rest = operands
    if a > result:
        return False

    if is_valid(result, [a + b, *rest], allow_concat):
        return True
    if is_valid(result, [a * b, *rest], allow_concat):
        return True
    if allow_concat and is_valid(result, [int(f"{a}{b}"), *rest], allow_concat):
        return True

    return False


def part_1(equations: list[tuple[int, list[int]]]):
    valid_results = [
        result for result, operands in equations if is_valid(result, operands)
    ]
    return sum(valid_results)


def part_2(equations: list[tuple[int, list[int]]]):
    valid_results = [
        result
        for result, operands in equations
        if is_valid(result, operands, allow_concat=True)
    ]
    return sum(valid_results)
