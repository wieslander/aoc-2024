from typing import Iterable

from aoc.geometry import StringGrid, Point
from aoc.parsers import transform


def find_word(grid: StringGrid, points: Iterable[Point], word: str):
    try:
        chars = [grid[p] for p in points]
    except KeyError:
        return False
    found_word = "".join(chars)
    return found_word in (word, "".join(reversed(word)))


def find_horizontal(grid: StringGrid, point: Point, word: str):
    points = [Point(point.x + offset, point.y) for offset in range(len(word))]
    return find_word(grid, points, word)


def find_vertical(grid: StringGrid, point: Point, word: str):
    points = [Point(point.x, point.y + offset) for offset in range(len(word))]
    return find_word(grid, points, word)


def find_diagonal_right(grid: StringGrid, point: Point, word: str):
    points = [Point(point.x + offset, point.y + offset) for offset in range(len(word))]
    return find_word(grid, points, word)


def find_diagonal_left(grid: StringGrid, point: Point, word: str):
    points = [Point(point.x - offset, point.y + offset) for offset in range(len(word))]
    return find_word(grid, points, word)


def is_x_mas(grid: StringGrid, top_left: Point):
    top_right = Point(top_left.x + 2, top_left.y)
    return find_diagonal_right(grid, top_left, "MAS") and find_diagonal_left(
        grid, top_right, "MAS"
    )


@transform(StringGrid)
def part_1(grid: StringGrid):
    count = 0
    for point in grid.points():
        args = (grid, point, "XMAS")
        if find_horizontal(*args):
            count += 1
        if find_vertical(*args):
            count += 1
        if find_diagonal_right(*args):
            count += 1
        if find_diagonal_left(*args):
            count += 1
    return count


@transform(StringGrid)
def part_2(grid: StringGrid):
    return sum(1 for p in grid.points() if is_x_mas(grid, p))
