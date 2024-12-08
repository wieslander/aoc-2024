from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable

from aoc import parsers


@dataclass
class Point:
    x: int
    y: int

    def as_tuple(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash(self.as_tuple())

    def __eq__(self, other: Any):
        return isinstance(other, Point) and self.as_tuple() == other.as_tuple()

    def __add__(self, other: Any):
        if not isinstance(other, Point):
            raise TypeError(f"Cannot add Point and {type(other)}")
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Any):
        if not isinstance(other, Point):
            raise TypeError(f"Cannot subtract Point and {type(other)}")
        return Point(self.x - other.x, self.y - other.y)


type PointTuple = tuple[int, int]


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
        return self._grid.get(point, default)

    def points(self) -> Iterable[Point]:
        return self._grid.keys()

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


class MapDirection(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

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


class GridMap(Grid[MapCell]):
    def parse_cell(self, pos: Point, raw_value: str):
        for cell in MapCell:
            if raw_value == cell.value:
                return cell
        raise ValueError(f"Unknown cell value {raw_value}")
