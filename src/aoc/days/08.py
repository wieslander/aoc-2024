from collections import defaultdict
import itertools

from aoc.geometry import Point, Grid
from aoc.parsers import transform


class AntennaGrid(Grid[str | None]):
    def __init__(self, input: str):
        self.antennas = defaultdict[str, set[Point]](set)
        super().__init__(input)

    def parse_cell(self, pos: Point, raw_value: str):
        if raw_value == ".":
            return None
        self.antennas[raw_value].add(pos)
        return raw_value


def find_antinodes(points: set[Point], grid: AntennaGrid | None = None):
    for p0, p1 in itertools.combinations(points, 2):
        delta = p1 - p0

        if grid:
            pos = p1
            while pos in grid:
                yield pos
                pos += delta
            pos = p0
            while pos in grid:
                yield pos
                pos -= delta
        else:
            yield p1 + delta
            yield p0 - delta


@transform(AntennaGrid)
def part_1(grid: AntennaGrid):
    antinodes = set[Point]()
    for locations in grid.antennas.values():
        antinodes.update(find_antinodes(locations))
    return len([a for a in antinodes if a in grid])


@transform(AntennaGrid)
def part_2(grid: AntennaGrid):
    antinodes = set[Point]()
    for locations in grid.antennas.values():
        antinodes.update(find_antinodes(locations, grid))
    return len(antinodes)
