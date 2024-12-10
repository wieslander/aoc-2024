from aoc.geometry import Point, HeightMap
from aoc.parsers import transform


def trail_score(grid: HeightMap, start_position: Point):
    end_points = set(trail[-1] for trail in find_trails(grid, start_position))
    return len(end_points)


def trail_rating(grid: HeightMap, start_position: Point):
    trails = list(find_trails(grid, start_position))
    return len(trails)


def find_trails(grid: HeightMap, start_position: Point):
    open_set: list[tuple[Point, ...]] = [(start_position,)]

    while open_set:
        path = open_set.pop()
        p = path[-1]
        height = grid[p]

        if height == 9:
            yield path
            continue

        for n in grid.neighbors(p):
            if grid[n] == height + 1:
                open_set.append(path + (n,))


@transform(HeightMap)
def part_1(grid: HeightMap):
    start_positions = [p for p, height in grid.cells() if height == 0]
    return sum(trail_score(grid, p) for p in start_positions)


@transform(HeightMap)
def part_2(grid: HeightMap):
    start_positions = [p for p, height in grid.cells() if height == 0]
    return sum(trail_rating(grid, p) for p in start_positions)
