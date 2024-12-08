from dataclasses import dataclass
from aoc.geometry import MapCell, Point, GridMap, MapDirection
from aoc.parsers import transform


@dataclass
class Guard:
    position: Point
    direction: MapDirection

    def forward_position(self):
        match self.direction:
            case MapDirection.UP:
                return self.position + Point(0, -1)
            case MapDirection.DOWN:
                return self.position + Point(0, 1)
            case MapDirection.LEFT:
                return self.position + Point(-1, 0)
            case MapDirection.RIGHT:
                return self.position + Point(1, 0)

    def move_forward(self):
        position = self.forward_position()
        return Guard(position, self.direction)

    def rotate_clockwise(self):
        direction = self.direction.rotate_clockwise()
        return Guard(self.position, direction)

    def clone(self):
        return Guard(self.position, self.direction)

    def __hash__(self):
        return hash((self.position, self.direction))


class World(GridMap):
    def __init__(self, input: str | None = None):
        self.guard: Guard | None = None
        self._history = set[Guard]()
        super().__init__(input)

    def parse_cell(self, pos: Point, raw_value: str):
        for direction in MapDirection:
            if raw_value == direction.value:
                self.guard = Guard(pos, direction)
                return MapCell.EMPTY
        return super().parse_cell(pos, raw_value)

    def move_guard(self):
        if not self.guard:
            return False

        self._history.add(self.guard)

        next_pos = self.guard.forward_position()
        if next_pos not in self._grid:
            self.guard = None
            return False

        match self[next_pos]:
            case MapCell.EMPTY:
                self.guard = self.guard.move_forward()
                return False
            case MapCell.OBSTACLE:
                self.guard = self.guard.rotate_clockwise()
                return True

    def visited_cells(self):
        while self.guard:
            self.move_guard()
        return {entry.position for entry in self._history}

    def clone(self):
        clone = super().clone()
        self._history = self._history.copy()
        if self.guard:
            clone.guard = self.guard.clone()
        return clone

    def has_loop(self):
        while self.guard:
            turned = self.move_guard()
            if turned and self.guard in self._history:
                return True

        return False


@transform(World)
def part_1(world: World):
    return len(world.visited_cells())


@transform(World)
def part_2(world: World):
    targets = set[Point]()
    checked_locations = set[Point]()

    while world.guard:
        pos = world.guard.forward_position()
        if pos not in checked_locations and world.get(pos) == MapCell.EMPTY:
            clone = world.clone()
            clone[pos] = MapCell.OBSTACLE
            if clone.has_loop():
                targets.add(pos)
            checked_locations.add(pos)
        world.move_guard()

    return len(targets)
