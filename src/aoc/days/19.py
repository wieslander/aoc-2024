from functools import cache


def get_patterns_and_designs(input: str):
    raw_patterns, raw_designs = input.split("\n\n")
    patterns = raw_patterns.split(", ")
    patterns.sort(key=len, reverse=True)
    designs = raw_designs.split("\n")
    return tuple(patterns), designs


@cache
def pattern_combinations(design: str, patterns: tuple[str, ...]) -> int:
    combos = 0
    for pattern in patterns:
        if pattern == design:
            combos += 1
        elif design.startswith(pattern):
            combos += pattern_combinations(design[len(pattern) :], patterns)
    return combos


def part_1(input: str):
    patterns, designs = get_patterns_and_designs(input)
    possible_designs = [d for d in designs if pattern_combinations(d, patterns) > 0]
    return len(possible_designs)


def part_2(input: str):
    patterns, designs = get_patterns_and_designs(input)
    return sum(pattern_combinations(design, patterns) for design in designs)
