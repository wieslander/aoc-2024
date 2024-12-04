from dataclasses import dataclass
from typing import Iterable


@dataclass
class Point:
    x: int
    y: int

    def as_tuple(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash(self.as_tuple())


type PointTuple = tuple[int, int]


class Grid[T]:
    def __init__(self):
        self._grid: dict[Point, T] = {}

    @classmethod
    def from_rows(cls, rows: Iterable[Iterable[T]]):
        grid = cls()
        for y, row in enumerate(rows):
            for x, value in enumerate(row):
                grid[(x, y)] = value
        return grid

    def set(self, point: Point | PointTuple, value: T):
        if isinstance(point, tuple):
            point = Point(*point)
        self._grid[point] = value

    def get(self, point: Point | PointTuple):
        if isinstance(point, tuple):
            point = Point(*point)
        return self._grid[point]

    def points(self) -> Iterable[Point]:
        return self._grid.keys()

    def __setitem__(self, point: Point | PointTuple, value: T):
        self.set(point, value)

    def __getitem__(self, point: Point | PointTuple):
        return self.get(point)
