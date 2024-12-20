from aoc.geometry import GridMap, MapCell, Point
from aoc.parsers import transform
from aoc.search import a_star


class RaceTrack(GridMap):
    def __init__(self, input: str):
        self.start: Point
        self.end: Point
        super().__init__(input)

    def parse_cell(self, pos: Point, raw_value: str):
        if raw_value == "S":
            self.start = pos
            return MapCell.EMPTY
        if raw_value == "E":
            self.end = pos
            return MapCell.EMPTY
        return super().parse_cell(pos, raw_value)


def shortest_path(track: RaceTrack, start: Point | None = None):
    if not start:
        start = track.start
    return a_star(
        start=start,
        next_states=lambda pos: ((n, 1) for n in track.empty_neighbors(pos)),
        is_goal=lambda pos: pos == track.end,
        h=track.end.manhattan_distance,
    )


def find_cheats(path: list[tuple[Point, int]], max_cheat_length: int):
    cheats = dict[tuple[Point, Point], int]()

    for cheat_start, start_cost in path:
        for cheat_end, end_cost in path[start_cost + 1 :]:
            cheat_manhattan = cheat_end.manhattan_distance(cheat_start)
            if cheat_manhattan > max_cheat_length:
                continue
            cheat_savings = (end_cost - start_cost) - cheat_manhattan
            cheats[(cheat_start, cheat_end)] = cheat_savings

    return cheats


@transform(RaceTrack)
def part_1(track: RaceTrack):
    path = shortest_path(track)
    cheats = find_cheats(path, max_cheat_length=2)
    return len([saved_time for saved_time in cheats.values() if saved_time >= 100])


@transform(RaceTrack)
def part_2(track: RaceTrack):
    path = shortest_path(track)
    cheats = find_cheats(path, max_cheat_length=20)
    return len([saved_time for saved_time in cheats.values() if saved_time >= 100])
