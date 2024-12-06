from functools import cmp_to_key
from typing import NamedTuple

from aoc import parsers


class OrderingRule(NamedTuple):
    first: int
    second: int


def split_input(input: str):
    rules: list[OrderingRule] = []
    page_updates: list[list[int]] = []

    parsing_rules = True

    for line in parsers.lines(input):
        if not line:
            parsing_rules = False
            continue

        if parsing_rules:
            rule_parts = parsers.numbers(line, sep="|")
            rules.append(OrderingRule(*rule_parts))
        else:
            pages = parsers.numbers(line, sep=",")
            page_updates.append(pages)

    return rules, page_updates


def is_valid(update: list[int], rules: list[OrderingRule]):
    for rule in rules:
        try:
            first_index = update.index(rule.first)
            second_index = update.index(rule.second)
            if second_index < first_index:
                return False
        except ValueError:
            pass
    return True


def get_valid_updates(page_updates: list[list[int]], rules: list[OrderingRule]):
    for update in page_updates:
        if is_valid(update, rules):
            yield update


def get_invalid_updates(page_updates: list[list[int]], rules: list[OrderingRule]):
    for update in page_updates:
        if not is_valid(update, rules):
            yield update


def part_1(input: str):
    rules, page_updates = split_input(input)
    valid_updates = list(get_valid_updates(page_updates, rules))
    return sum(pages[len(pages) // 2] for pages in valid_updates)


def part_2(input: str):
    rules, page_updates = split_input(input)
    invalid_updates = list(get_invalid_updates(page_updates, rules))

    def cmp(a: int, b: int):
        if any(r.first == a and r.second == b for r in rules):
            return -1
        if any(r.first == b and r.second == a for r in rules):
            return 1
        return 0

    for update in invalid_updates:
        update.sort(key=cmp_to_key(cmp))

    return sum(pages[len(pages) // 2] for pages in invalid_updates)
