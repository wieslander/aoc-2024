from aoc.geometry import GridMap, MapCell, Point
from aoc.parsers import transform_lines
from aoc.search import a_star


def get_empty_grid(size: int):
    grid = GridMap()
    for y in range(size):
        for x in range(size):
            grid[(x, y)] = MapCell.EMPTY
    return grid


@transform_lines(Point.parse)
def part_1(positions: list[Point]):
    grid = get_empty_grid(71)

    for pos in positions[:1024]:
        grid[pos] = MapCell.OBSTACLE

    goal = Point(70, 70)

    path = a_star(
        start=Point(0, 0),
        next_states=lambda pos: ((n, 1) for n in grid.empty_neighbors(pos)),
        is_goal=lambda pos: pos == goal,
        h=goal.manhattan_distance,
    )

    return len(path) - 1


@transform_lines(Point.parse)
def part_2(positions: list[Point]):
    grid = get_empty_grid(71)

    for pos in positions[:1024]:
        grid[pos] = MapCell.OBSTACLE

    goal = Point(70, 70)

    for byte in positions:
        grid[byte] = MapCell.OBSTACLE
        path = a_star(
            start=Point(0, 0),
            next_states=lambda pos: ((n, 1) for n in grid.empty_neighbors(pos)),
            is_goal=lambda pos: pos == goal,
            h=goal.manhattan_distance,
        )
        if not path:
            return f"{byte.x},{byte.y}"

    raise ValueError("There are still open paths after dropping all the bytes")
