from functools import cache

from aoc.parsers import transform, numbers


@cache
def stone_count_after_transform(stone: int, iterations: int) -> int:
    if iterations == 0:
        return 1

    new_stones = list[int]()
    stone_digits = str(stone)
    digit_count = len(stone_digits)

    if stone == 0:
        new_stones.append(1)
    elif digit_count % 2 == 0:
        split_pos = digit_count // 2
        new_stones.append(int(stone_digits[:split_pos]))
        new_stones.append(int(stone_digits[split_pos:]))
    else:
        new_stones.append(stone * 2024)

    return sum(stone_count_after_transform(s, iterations - 1) for s in new_stones)


@transform(numbers)
def part_1(stones: list[int]):
    return sum(stone_count_after_transform(stone, iterations=25) for stone in stones)


@transform(numbers)
def part_2(stones: list[int]):
    return sum(stone_count_after_transform(stone, iterations=75) for stone in stones)
