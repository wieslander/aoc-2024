from heapq import heappop, heappush
from math import inf
from typing import Callable, Iterable


def backtrack[State](
    came_from: dict[State, tuple[State, int]], current: State, total_cost: int
):
    path = [(current, total_cost)]
    while current in came_from:
        current, cost = came_from[current]
        path.append((current, cost))
    path.reverse()
    return path


def a_star[State](
    start: State,
    next_states: Callable[[State], Iterable[tuple[State, int]]],
    is_goal: Callable[[State], bool],
    h: Callable[[State], int],
) -> list[tuple[State, int]]:
    f_costs = dict[State, int]()
    g_costs = dict[State, int]()
    f_costs[start] = h(start)
    g_costs[start] = 0
    open_set = [(g_costs[start], start)]
    came_from = dict[State, tuple[State, int]]()

    while open_set:
        _, current = heappop(open_set)
        if is_goal(current):
            total_cost = g_costs[current]
            return backtrack(came_from, current, total_cost)

        for neighbor, edge_cost in next_states(current):
            tentative_cost = g_costs[current] + edge_cost
            if tentative_cost < g_costs.get(neighbor, inf):
                g_costs[neighbor] = tentative_cost
                f_costs[neighbor] = tentative_cost + h(neighbor)
                came_from[neighbor] = (current, g_costs[current])
                heappush(open_set, (f_costs[neighbor], neighbor))

    return []
