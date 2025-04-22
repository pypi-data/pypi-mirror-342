from typing import Any
from collections.abc import Iterable

from data_structures import Stack


class RotationStack(Stack):
    def __init__(self, items: Iterable[Any] = None, freeze: bool = False) -> None:
        super().__init__(items, freeze)

    def rotate(self, times: int = 1, reverse: bool = False) -> None:
        if self.is_frozen():
            raise "Cannot rotate a frozen queue"
        if self.is_empty() or len(self) == 1:
            return
        if reverse:
            self.__reverse_rotation(times)
            return
        self.__rotation(times)

    def __reverse_rotation(self, times: int) -> None:
        for _ in range(times):
            node = self.top_node
            node.prev = self.bottom_node
            self.bottom_node.next = node
            self.top_node = node.next
            node.next = None
            self.top_node.prev = None
            self.bottom_node = node

    def __rotation(self, times: int) -> None:
        for _ in range(times):
            node = self.bottom_node
            node.next = self.top_node
            self.top_node.prev = node
            self.top_node = node
            self.bottom_node = node.prev
            self.bottom_node.next = None
            node.prev = None

    def __repr__(self) -> str:
        return f"RotationQueue({list(self)!r}, {self.__frozen!r})"
