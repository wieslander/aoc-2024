from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from functools import total_ordering
from typing import Any, Iterable

from aoc import parsers


@total_ordering
@dataclass
class Point:
    x: int
    y: int

    def as_tuple(self):
        return (self.x, self.y)

    def neighbors(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return [self + Point(*d) for d in directions]

    def manhattan_distance(self, other: "Point"):
        diff = other - self
        return abs(diff.x) + abs(diff.y)

    def __hash__(self):
        return hash(self.as_tuple())

    def __eq__(self, other: Any):
        return isinstance(other, Point) and self.as_tuple() == other.as_tuple()

    def __lt__(self, other: Any):
        return isinstance(other, Point) and self.as_tuple() < other.as_tuple()

    def __add__(self, other: Any):
        if not isinstance(other, Point):
            raise TypeError(f"Cannot add Point and {type(other)}")
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Any):
        if not isinstance(other, Point):
            raise TypeError(f"Cannot subtract Point and {type(other)}")
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, factor: Any):
        if not isinstance(factor, int):
            raise TypeError(f"Cannot multiply Point and {type(factor)}")
        return Point(self.x * factor, self.y * factor)


type PointTuple = tuple[int, int]


@total_ordering
@dataclass
class Line:
    start: Point
    end: Point

    def direction(self):
        raw_direction = self.end - self.start
        match raw_direction:
            case Point(0, 0):
                return raw_direction
            case Point(0, y) if y > 0:
                return Point(0, 1)
            case Point(0, y) if y < 0:
                return Point(0, -1)
            case Point(x, 0) if x > 0:
                return Point(1, 0)
            case Point(x, 0) if x < 0:
                return Point(-1, 0)
            case Point(x, y):
                fraction = Fraction(x, y)
                return Point(fraction.numerator, fraction.denominator)

    def __hash__(self):
        return hash((self.start, self.end))

    def __eq__(self, other: Any):
        return (
            isinstance(other, Line)
            and self.start == other.start
            and self.end == other.end
        )

    def __lt__(self, other: Any):
        return (
            isinstance(other, Line)
            and (self.start, self.end) < (other.start, other.end),
        )


class Grid[T](ABC):
    def __init__(self, input: str | None = None):
        self._grid: dict[Point, T] = {}
        if not input:
            return

        for y, line in enumerate(parsers.lines(input)):
            for x, value in enumerate(line):
                pos = Point(x, y)
                self[(x, y)] = self.parse_cell(pos, value)

    def set(self, point: Point | PointTuple, value: T):
        if isinstance(point, tuple):
            point = Point(*point)
        self._grid[point] = value

    def get(self, point: Point | PointTuple, default: T | None = None):
        if isinstance(point, tuple):
            point = Point(*point)
        try:
            return self[point]
        except KeyError:
            return default

    def points(self) -> Iterable[Point]:
        return self._grid.keys()

    def cells(self) -> Iterable[tuple[Point, T]]:
        return self._grid.items()

    def neighbors(self, point: Point):
        return [p for p in point.neighbors() if p in self._grid]

    def clone(self):
        clone = type(self)()
        clone._grid = self._grid.copy()
        return clone

    @abstractmethod
    def parse_cell(self, pos: Point, raw_value: str) -> T: ...

    def __setitem__(self, point: Point | PointTuple, value: T):
        self.set(point, value)

    def __getitem__(self, point: Point | PointTuple):
        if isinstance(point, tuple):
            point = Point(*point)
        return self._grid[point]

    def __contains__(self, item: Any):
        return item in self._grid


class StringGrid(Grid[str]):
    def parse_cell(self, pos: Point, raw_value: str):
        return raw_value


class MapCell(Enum):
    EMPTY = "."
    OBSTACLE = "#"


@total_ordering
class MapDirection(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    @staticmethod
    def parse(char: str):
        for direction in MapDirection:
            if char == direction.value:
                return direction
        raise ValueError(f"Unknown direction {char}")

    def rotate_clockwise(self):
        match self:
            case MapDirection.UP:
                return MapDirection.RIGHT
            case MapDirection.DOWN:
                return MapDirection.LEFT
            case MapDirection.LEFT:
                return MapDirection.UP
            case MapDirection.RIGHT:
                return MapDirection.DOWN

    def rotate_counterclockwise(self):
        match self:
            case MapDirection.UP:
                return MapDirection.LEFT
            case MapDirection.DOWN:
                return MapDirection.RIGHT
            case MapDirection.LEFT:
                return MapDirection.DOWN
            case MapDirection.RIGHT:
                return MapDirection.UP

    def point(self):
        match self:
            case MapDirection.UP:
                return Point(0, -1)
            case MapDirection.DOWN:
                return Point(0, 1)
            case MapDirection.LEFT:
                return Point(-1, 0)
            case MapDirection.RIGHT:
                return Point(1, 0)

    def __lt__(self, other: Any):
        if not isinstance(other, MapDirection):
            return False
        directions = list(MapDirection)
        return directions.index(self) < directions.index(other)


class GridMap(Grid[MapCell]):
    def parse_cell(self, pos: Point, raw_value: str):
        for cell in MapCell:
            if raw_value == cell.value:
                return cell
        raise ValueError(f"Unknown cell value {raw_value}")


class HeightMap(Grid[int]):
    def parse_cell(self, pos: Point, raw_value: str):
        return int(raw_value)
