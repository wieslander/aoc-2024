from typing import Any

from aoc.types import Comparable


class Edge[T: Comparable]:
    def __init__(self, node_a: T, node_b: T):
        self._node_a, self._node_b = sorted([node_a, node_b])

    def nodes(self):
        return (self._node_a, self._node_b)

    def __hash__(self):
        return hash((self._node_a, self._node_b))

    def __eq__(self, other: Any):
        if isinstance(other, Edge):
            return self.nodes() == other.nodes()
        elif isinstance(other, tuple):
            return self.nodes() == other
        return False

    def __contains__(self, value: Any):
        return value in self.nodes()


class Graph[T: Comparable]:
    def __init__(self):
        self._nodes = set[T]()
        self._edges = set[Edge[T]]()

    def add_edge(self, node_a: T, node_b: T):
        self.add_nodes(node_a, node_b)
        edge = Edge(node_a, node_b)
        if edge not in self._edges:
            self._edges.add(edge)

    def add_nodes(self, *nodes: T):
        self._nodes.update(nodes)

    def has_edge(self, node_a: T, node_b: T):
        e = Edge(node_a, node_b)
        return e in self._edges

    def nodes(self):
        return self._nodes

    def edges(self):
        return self._edges

    def neighbors(self, node: T):
        for edge in self._edges:
            if node in edge:
                nodes = set(edge.nodes())
                nodes.remove(node)
                yield nodes.pop()
