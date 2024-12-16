from enum import Enum
from functools import partial
from itertools import dropwhile
from typing import NamedTuple

from aoc.geometry import Grid, MapDirection, Point
from aoc.parsers import transform
from aoc.search import a_star


class Cell(Enum):
    EMPTY = "."
    OBSTACTLE = "#"
    START = "S"
    END = "E"


class Maze(Grid[Cell]):
    def parse_cell(self, pos: Point, raw_value: str):
        for cell in Cell:
            if raw_value == cell.value:
                return cell
        raise ValueError(f"Unknown cell type {raw_value}")


class State(NamedTuple):
    position: Point
    direction: MapDirection

    def next_states(self, maze: Maze):
        forward_pos = self.position + self.direction.point()
        if maze.get(forward_pos) in (Cell.EMPTY, Cell.END):
            yield self.update(position=forward_pos), 1
        yield self.update(direction=self.direction.rotate_clockwise()), 1000
        yield self.update(direction=self.direction.rotate_counterclockwise()), 1000

    def update(
        self, position: Point | None = None, direction: MapDirection | None = None
    ):
        new_position = position if position else self.position
        new_direction = direction if direction else self.direction
        return State(new_position, new_direction)


def print_path(path: list[tuple[State, int]], maze: Maze):
    width = max(p.x for p in maze.points()) + 1
    height = max(p.y for p in maze.points()) + 1
    lines = list[list[str]]()

    for y in range(height):
        line = list[str]()
        for x in range(width):
            line.append(maze[(x, y)].value)
        lines.append(line)

    for step, _ in path:
        pos = step.position
        lines[pos.y][pos.x] = step.direction.value

    for line in lines:
        print("".join(line))


@transform(Maze)
def part_1(maze: Maze):
    start_pos = next(dropwhile(lambda p: maze[p] != Cell.START, maze.points()))
    goal = next(dropwhile(lambda p: maze[p] != Cell.END, maze.points()))
    start_state = State(start_pos, MapDirection.RIGHT)
    path = a_star(
        start_state,
        partial(State.next_states, maze=maze),
        lambda state: state.position == goal,
        lambda state: state.position.manhattan_distance(goal),
    )
    if not path:
        raise ValueError("No path found")

    print_path(path, maze)

    _, cost = path.pop()

    return cost
