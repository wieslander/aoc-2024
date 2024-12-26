from collections import deque
import itertools
from functools import cache

from aoc.parsers import lines, transform

NUMPAD_MOVES = {
    "A": [("<", "0"), ("^", "3")],
    "0": [(">", "A"), ("^", "2")],
    "1": [(">", "2"), ("^", "4")],
    "2": [("<", "1"), ("^", "5"), (">", "3"), ("v", "0")],
    "3": [("<", "2"), ("^", "6"), ("v", "A")],
    "4": [(">", "5"), ("^", "7"), ("v", "1")],
    "5": [("<", "4"), ("^", "8"), (">", "6"), ("v", "2")],
    "6": [("<", "5"), ("^", "9"), ("v", "3")],
    "7": [(">", "8"), ("v", "4")],
    "8": [("<", "7"), (">", "9"), ("v", "5")],
    "9": [("<", "8"), ("v", "6")],
}

DPAD_MOVES = {
    "<": [(">", "v")],
    ">": [("<", "v"), ("^", "A")],
    "v": [("<", "<"), (">", ">"), ("^", "^")],
    "^": [(">", "A"), ("v", "v")],
    "A": [("<", "^"), ("v", ">")],
}


def expand_move(start_key: str, end_key: str, keymap: dict[str, list[tuple[str, str]]]):
    dpad_sequences: list[str] = []
    open_set: deque[tuple[str, str]] = deque([(start_key, "")])
    visited = set[str]()

    while open_set:
        numpad_key, path = open_set.popleft()
        visited.add(numpad_key)

        if numpad_key == end_key:
            # Press the A key on the D-pad to activate the button
            dpad_sequences.append(path + "A")
            continue

        for dpad_key, neighbor in keymap[numpad_key]:
            if neighbor not in visited:
                open_set.append((neighbor, path + dpad_key))

    return dpad_sequences


def expand_numpad_move(start_key: str, end_key: str):
    return expand_move(start_key, end_key, NUMPAD_MOVES)


@cache
def expand_dpad_move(start_key: str, end_key: str):
    return expand_move(start_key, end_key, DPAD_MOVES)


@cache
def shortest_dpad_sequence_expansion(sequence: str, robot_dpad_count: int):
    dpad_moves = itertools.pairwise("A" + sequence)
    return sum(
        shortest_dpad_keypress_length(start_key, end_key, robot_dpad_count)
        for start_key, end_key in dpad_moves
    )


@cache
def shortest_dpad_keypress_length(
    start_key: str, end_key: str, robot_dpad_count: int
) -> int:
    if robot_dpad_count == 0:
        return 1
    dpad_sequences = expand_dpad_move(start_key, end_key)
    return min(
        shortest_dpad_sequence_expansion(sequence, robot_dpad_count - 1)
        for sequence in dpad_sequences
    )


def shortest_numpad_keypress_length(
    start_key: str, end_key: str, robot_dpad_count: int
) -> int:
    dpad_sequences = expand_numpad_move(start_key, end_key)
    return min(
        shortest_dpad_sequence_expansion(sequence, robot_dpad_count)
        for sequence in dpad_sequences
    )


def shortest_numpad_code_expansion(code: str, robot_dpad_count: int):
    numpad_moves = itertools.pairwise("A" + code)
    return sum(
        shortest_numpad_keypress_length(start_key, end_key, robot_dpad_count)
        for start_key, end_key in numpad_moves
    )


def complexity(code: str, robot_dpad_count: int):
    numeric_value = int(code.removesuffix("A"))
    dpad_keypresses = shortest_numpad_code_expansion(code, robot_dpad_count)
    return numeric_value * dpad_keypresses


@transform(lines)
def part_1(codes: list[str]):
    return sum(complexity(code, 2) for code in codes)


@transform(lines)
def part_2(codes: list[str]):
    return sum(complexity(code, 25) for code in codes)
