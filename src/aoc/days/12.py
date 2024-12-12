from aoc.geometry import Line, Point, StringGrid
from aoc.parsers import transform


def fence_segment(outer: Point, inner: Point):
    diff = outer - inner
    match diff:
        case Point(-1, 0):
            return Line(inner + Point(0, 1), inner)
        case Point(1, 0):
            return Line(outer, outer + Point(0, 1))
        case Point(0, -1):
            return Line(inner, inner + Point(1, 0))
        case Point(0, 1):
            return Line(outer + Point(1, 0), outer)
        case _:
            raise ValueError(
                "Cannot calculate fence segments for points that are "
                f"not adjacent: {outer}, {inner}"
            )


def merge_fence_segments(segments: set[Line]):
    sides = list[Line]()
    for segment in segments:
        direction = segment.direction()
        same_line_sides = [side for side in sides if side.direction() == direction]
        before = [side for side in same_line_sides if side.end == segment.start]
        after = [side for side in same_line_sides if segment.end == side.start]
        if before:
            assert len(before) == 1
            before[0].end = segment.end
        if after:
            assert len(after) == 1
            after[0].start = segment.start
        if before and after:
            before[0].end = after[0].end
            sides.remove(after[0])
        if not before and not after:
            sides.append(segment)
    return sides


def flood_fill(grid: StringGrid, start: Point):
    perimeter = 0
    region = set[Point]()
    plant_type = grid[start]
    fence_segments = set[Line]()

    open_set = {start}
    while open_set:
        pos = open_set.pop()
        region.add(pos)
        for n in pos.neighbors():
            if n not in grid or grid[n] != plant_type:
                fence_segments.add(fence_segment(outer=n, inner=pos))
                perimeter += 1
            elif n not in region:
                open_set.add(n)

    sides = merge_fence_segments(fence_segments)

    return region, perimeter, len(sides)


def find_regions(grid: StringGrid):
    visited_locations = set[Point]()

    for pos in grid.points():
        if pos in visited_locations:
            continue
        region, perimeter, sides = flood_fill(grid, pos)
        visited_locations.update(region)
        yield region, perimeter, sides


@transform(StringGrid)
def part_1(grid: StringGrid):
    return sum(perimeter * len(region) for region, perimeter, _ in find_regions(grid))


@transform(StringGrid)
def part_2(grid: StringGrid):
    return sum(sides * len(region) for region, _, sides in find_regions(grid))
