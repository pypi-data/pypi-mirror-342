from typing import Any
from collections.abc import Iterable

from data_structures import LinkedList


class RotationLinkedList(LinkedList):
    def __init__(self, items: Iterable[Any], freeze: bool = False) -> None:
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
            node = self.head_node
            node.prev = self.tail_node
            self.tail_node.next = node
            self.head_node = node.next
            node.next = None
            self.head_node.prev = None
            self.tail_node = node

    def __rotation(self, times: int) -> None:
        for _ in range(times):
            node = self.tail_node
            node.next = self.head_node
            self.head_node.prev = node
            self.head_node = node
            self.tail_node = node.prev
            self.tail_node.next = None
            node.prev = None
