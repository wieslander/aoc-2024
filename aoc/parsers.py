from collections.abc import Callable
from functools import wraps

from aoc.types import Result


def transform[T](parser: Callable[[str], T]):
    def make_wrapper(f: Callable[[T], Result]):
        @wraps(f)
        def wrapper(input: str):
            return f(parser(input))

        return wrapper

    return make_wrapper


def raw(input: str):
    return input


def lines(input: str):
    return input.split("\n")


def numbers(input: str):
    return [int(x) for x in input.split()]


def number_lines(input: str):
    return [numbers(line) for line in lines(input)]
