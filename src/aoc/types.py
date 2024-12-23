from typing import Any, Literal, Protocol

type Result = int | str
type PuzzlePart = Literal[1, 2]


class Comparable(Protocol):
    def __lt__(self, value: Any, /) -> bool: ...
