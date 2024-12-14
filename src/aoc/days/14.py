from functools import reduce
import operator
import re
from dataclasses import dataclass

from aoc.geometry import Point
from aoc.parsers import transform_lines

robot_pattern = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"

WIDTH = 101
HEIGHT = 103


@dataclass
class Robot:
    position: Point
    velocity: Point

    @classmethod
    def from_line(cls, line: str):
        match = re.match(robot_pattern, line)
        if not match:
            raise ValueError(f"Could not parse robot spec: {line}")
        px, py, vx, vy = match.group(1, 2, 3, 4)
        position = Point(int(px), int(py))
        velocity = Point(int(vx), int(vy))
        return cls(position, velocity)

    def step(self):
        new_pos = self.position + self.velocity
        self.position = Point(new_pos.x % WIDTH, new_pos.y % HEIGHT)

    def quadrant(self):
        x, y = self.position.as_tuple()
        if x < WIDTH // 2 and y < HEIGHT // 2:
            return 0
        if x < WIDTH // 2 and y > HEIGHT // 2:
            return 1
        if x > WIDTH // 2 and y < HEIGHT // 2:
            return 2
        if x > WIDTH // 2 and y > HEIGHT // 2:
            return 3


def move_robots(robots: list[Robot]):
    for robot in robots:
        robot.step()


def safety_factor(robots: list[Robot]):
    quadrants = [0] * 4
    for robot in robots:
        quadrant = robot.quadrant()
        if quadrant is not None:
            quadrants[quadrant] += 1
    return reduce(operator.mul, quadrants)


def is_xmas_tree(robots: list[Robot]):
    # Simply check if an unusual number of robots are placed
    # close together
    robot_positions = {r.position for r in robots}
    max_adjacent = 0
    for x in range(WIDTH):
        adjacent = 0
        for y in range(HEIGHT):
            if Point(x, y) in robot_positions:
                adjacent += 1
                max_adjacent = max(adjacent, max_adjacent)
            else:
                adjacent = 0
    for y in range(WIDTH):
        adjacent = 0
        for x in range(HEIGHT):
            if Point(x, y) in robot_positions:
                adjacent += 1
                max_adjacent = max(adjacent, max_adjacent)
            else:
                adjacent = 0
    return max_adjacent > 10


def print_robots(robots: list[Robot]):
    robot_positions = {r.position for r in robots}
    for y in range(HEIGHT):
        line = list[str]()
        for x in range(WIDTH):
            if Point(x, y) in robot_positions:
                line.append("#")
            else:
                line.append(".")
        print("".join(line))


@transform_lines(Robot.from_line)
def part_1(robots: list[Robot]):
    for _ in range(100):
        move_robots(robots)
    return safety_factor(robots)


@transform_lines(Robot.from_line)
def part_2(robots: list[Robot]):
    steps = 0
    while True:
        move_robots(robots)
        steps += 1
        if is_xmas_tree(robots):
            print_robots(robots)
            return steps
