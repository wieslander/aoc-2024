from collections import Counter, deque
from itertools import islice, pairwise
from functools import cache
from aoc.parsers import transform, numbers


@cache
def mix_and_prune(n: int, mix_number: int):
    return (n ^ mix_number) % 2**24


@cache
def next_secret_number(n: int) -> int:
    n = mix_and_prune(n, n * 64)
    n = mix_and_prune(n, n // 32)
    n = mix_and_prune(n, n * 2048)
    return n


@cache
def secret_number(seed: int, iterations: int):
    start = iterations
    stop = start + 1
    return next(islice(secret_numbers(seed), start, stop))


def secret_numbers(seed: int):
    yield seed
    n = seed
    while True:
        n = next_secret_number(n)
        yield n


def prices(seed: int):
    return map(lambda n: n % 10, secret_numbers(seed))


def prices_with_change_history(seed: int, iterations: int):
    change_history = deque[int](maxlen=4)
    for prev_price, price in islice(pairwise(prices(seed)), iterations + 2):
        diff = price - prev_price
        change_history.append(diff)
        if len(change_history) == 4:
            yield price, tuple(change_history)


def max_bananas(seeds: list[int], iterations: int):
    diff_counter = Counter[tuple[int, ...]]()
    for seed in seeds:
        buyer_diffs = set[tuple[int, ...]]()
        for price, change_history in prices_with_change_history(seed, iterations):
            if change_history not in buyer_diffs:
                diff_counter[change_history] += price
                buyer_diffs.add(change_history)
    _, total_price = diff_counter.most_common(1)[0]
    return total_price


@transform(numbers)
def part_1(seeds: list[int]):
    return sum(secret_number(seed, iterations=2000) for seed in seeds)


@transform(numbers)
def part_2(seeds: list[int]):
    return max_bananas(seeds, iterations=2000)
