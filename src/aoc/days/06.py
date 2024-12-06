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
            return

        self._history.add(self.guard)

        next_pos = self.guard.forward_position()
        if next_pos not in self._grid:
            self.guard = None
            return

        match self[next_pos]:
            case MapCell.EMPTY:
                self.guard = self.guard.move_forward()
            case MapCell.OBSTACLE:
                self.guard = self.guard.rotate_clockwise()

    def guard_path(self):
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
            self.move_guard()
            if self.guard in self._history:
                return True

        return False


@transform(World)
def part_1(world: World):
    return len(world.guard_path())


@transform(World)
def part_2(world: World):
    loop_count = 0

    for pos in world.clone().guard_path():
        assert world.guard
        if pos != world.guard.position:
            clone = world.clone()
            clone[pos] = MapCell.OBSTACLE
            if clone.has_loop():
                loop_count += 1

    return loop_count
