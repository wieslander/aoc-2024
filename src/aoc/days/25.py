import itertools


def parse_lock(lines: list[str]):
    heights = [0, 0, 0, 0, 0]
    for line in lines[1:]:
        for pin_index, char in enumerate(line):
            if char == "#":
                heights[pin_index] += 1
    return tuple(heights)


def parse_key(lines: list[str]):
    # A key looks just like a reversed lock
    return parse_lock(list(reversed(lines)))


def parse_input(input: str):
    locks: list[tuple[int, ...]] = []
    keys: list[tuple[int, ...]] = []

    for segment in input.split("\n\n"):
        lines = segment.split("\n")
        if lines[0] == "#####":
            locks.append(parse_lock(lines))
        else:
            keys.append(parse_key(lines))

    return locks, keys


def part_1(input: str):
    locks, keys = parse_input(input)
    matching_combinations = 0

    for lock, key in itertools.product(locks, keys):
        if all(lock[col] + key[col] <= 5 for col in range(5)):
            matching_combinations += 1

    return matching_combinations
