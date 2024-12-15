from enum import Enum

from aoc.geometry import Grid, Point, MapDirection


class MapCell(Enum):
    EMPTY = "."
    OBSTACLE = "#"
    BOX = "O"


class World(Grid[MapCell]):
    def __init__(self, input: str):
        self.robot: Point
        super().__init__(input)

    def parse_cell(self, pos: Point, raw_value: str):
        if raw_value == "@":
            self.robot = pos
            return MapCell.EMPTY

        for cell in MapCell:
            if raw_value == cell.value:
                return cell

        raise ValueError(f"Unknown cell value {raw_value}")

    def move_robot(self, direction: MapDirection):
        target_position = self.robot + direction.point()
        cell = self.get(target_position)

        match cell:
            case None:
                return
            case MapCell.OBSTACLE:
                return
            case MapCell.EMPTY:
                self.robot = target_position
            case MapCell.BOX:
                if self.move_boxes(target_position, direction):
                    self.robot = target_position

    def move_boxes(self, start: Point, direction: MapDirection):
        next_pos = start
        while next_pos in self:
            match self[next_pos]:
                case MapCell.EMPTY:
                    self[start] = MapCell.EMPTY
                    self[next_pos] = MapCell.BOX
                    return True
                case MapCell.BOX:
                    next_pos = next_pos + direction.point()
                case MapCell.OBSTACLE:
                    return False
        return False


class WideMapCell(Enum):
    EMPTY = "."
    OBSTACLE = "#"
    BOX_LEFT = "["
    BOX_RIGHT = "]"


class WideWorld(Grid[WideMapCell]):
    def __init__(self, input: str):
        world = World(input)
        self.robot: Point
        super().__init__()
        self.robot = Point(world.robot.x * 2, world.robot.y)
        for pos, cell in world.cells():
            left = Point(pos.x * 2, pos.y)
            right = left + Point(1, 0)
            match cell:
                case MapCell.EMPTY:
                    self[left] = WideMapCell.EMPTY
                    self[right] = WideMapCell.EMPTY
                case MapCell.OBSTACLE:
                    self[left] = WideMapCell.OBSTACLE
                    self[right] = WideMapCell.OBSTACLE
                case MapCell.BOX:
                    self[left] = WideMapCell.BOX_LEFT
                    self[right] = WideMapCell.BOX_RIGHT

    def parse_cell(self, pos: Point, raw_value: str):
        # Dummy implementation as we don't actually parse input in this class
        return WideMapCell.EMPTY

    def move_robot(self, direction: MapDirection):
        target_position = self.robot + direction.point()
        cell = self.get(target_position)

        if cell == WideMapCell.EMPTY:
            self.robot = target_position
        elif cell in (WideMapCell.BOX_LEFT, WideMapCell.BOX_RIGHT):
            old_grid = self._grid.copy()
            if self.move_boxes(target_position, direction):
                self.robot = target_position
            else:
                self._grid = old_grid

    def move_boxes(self, start: Point, direction: MapDirection):
        box_coords = self.get_box_coords(start)
        all_targets = tuple(pos + direction.point() for pos in box_coords)
        all_targets = tuple(pos for pos in all_targets if pos not in box_coords)

        if any(target not in self for target in all_targets):
            return False
        if any(self[target] == WideMapCell.OBSTACLE for target in all_targets):
            return False
        elif all(self[target] == WideMapCell.EMPTY for target in all_targets):
            self.move_box(start, direction)
            return True

        blocked_targets = [
            target
            for target in all_targets
            if self[target] in (WideMapCell.BOX_LEFT, WideMapCell.BOX_RIGHT)
        ]
        blocking_boxes = set(self.get_box_coords(target) for target in blocked_targets)
        if all(self.move_boxes(left, direction) for left, _ in blocking_boxes):
            self.move_box(start, direction)
            return True
        return False

    def move_box(self, box: Point, direction: MapDirection):
        box_coords = self.get_box_coords(box)
        # Clear old coords
        for pos in box_coords:
            self[pos] = WideMapCell.EMPTY

        # Update new coords
        new_coords = tuple(pos + direction.point() for pos in box_coords)
        left, right = new_coords
        self[left] = WideMapCell.BOX_LEFT
        self[right] = WideMapCell.BOX_RIGHT

    def get_box_coords(self, pos: Point):
        if self[pos] == WideMapCell.BOX_LEFT:
            return (pos, pos + Point(1, 0))
        elif self[pos] == WideMapCell.BOX_RIGHT:
            return (pos - Point(1, 0), pos)
        else:
            raise ValueError(f"No box found at position {pos}")

    def __str__(self):
        width = max(p.x for p in self.points()) + 1
        height = max(p.y for p in self.points()) + 1
        lines = list[str]()

        for y in range(height):
            line = list[str]()
            for x in range(width):
                pos = Point(x, y)
                if pos == self.robot:
                    line.append("@")
                else:
                    line.append(self[pos].value)
            lines.append("".join(line))

        return "\n".join(lines)


def gps_sum(world: World | WideWorld):
    total = 0
    for point, cell in world.cells():
        if cell in (MapCell.BOX, WideMapCell.BOX_LEFT):
            total += point.y * 100 + point.x
    return total


def part_1(input: str):
    world_input, moves_input = input.split("\n\n")
    world = World(world_input)
    moves = [MapDirection.parse(char) for char in moves_input.replace("\n", "")]

    for direction in moves:
        world.move_robot(direction)

    return gps_sum(world)


def part_2(input: str):
    world_input, moves_input = input.split("\n\n")
    world = WideWorld(world_input)
    moves = [MapDirection.parse(char) for char in moves_input.replace("\n", "")]

    for direction in moves:
        # print(world)
        world.move_robot(direction)

    return gps_sum(world)
