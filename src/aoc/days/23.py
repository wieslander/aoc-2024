from itertools import combinations
from typing import Generator

from aoc.graph import Graph
from aoc.parsers import lines, transform


def parse_graph(input: str):
    graph = Graph[str]()
    raw_edges = lines(input)
    for edge in raw_edges:
        nodes = edge.split("-")
        graph.add_edge(*nodes)
    return graph


def find_triangles(graph: Graph[str]):
    triangles = set[tuple[str, ...]]()
    for node in graph.nodes():
        neighbors = set(graph.neighbors(node))
        for a, b in combinations(neighbors, 2):
            if graph.has_edge(a, b):
                triangles.add(tuple(sorted([node, a, b])))
    return triangles


def find_maximum_clique(graph: Graph[str]):
    def bron_kerbosch(r: set[str], p: set[str], x: set[str]) -> Generator[set[str]]:
        if not p and not x:
            yield r
        while p:
            node = p.pop()
            neighbors = set(graph.neighbors(node))
            for clique in bron_kerbosch(
                r.union({node}),
                p.intersection(neighbors),
                x.intersection(neighbors),
            ):
                yield clique
            x = x.union({node})

    max_clique = set[str]()
    for clique in bron_kerbosch(set(), set(graph.nodes()), set()):
        if len(clique) > len(max_clique):
            max_clique = clique
    return max_clique


@transform(parse_graph)
def part_1(graph: Graph[str]):
    triangles = find_triangles(graph)
    return len([t for t in triangles if any(node.startswith("t") for node in t)])


@transform(parse_graph)
def part_2(graph: Graph[str]):
    clique = find_maximum_clique(graph)
    nodes = sorted(clique)
    return ",".join(nodes)
