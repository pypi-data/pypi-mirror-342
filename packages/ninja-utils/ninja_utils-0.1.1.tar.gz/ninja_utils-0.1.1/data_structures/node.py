from typing import Any


class Node:
    def __init__(
        self, data: Any, next: "Node" = None, prev: "Node" = None, freeze: bool = False
    ) -> None:
        self.__data = data
        self.__next = next
        self.__prev = prev
        self.__frozen = freeze

    @property
    def data(self) -> Any:
        return self.__data

    @data.setter
    def data(self, value) -> None:
        if not self.__frozen:
            self.__data = value
            return
        raise "Cannot change state of a frozen node"

    @property
    def next(self) -> "Node":
        return self.__next

    @next.setter
    def next(self, node: "Node" = None) -> None:
        if not self.__frozen:
            self.__next = node
            return
        raise "Cannot change state of a frozen node"

    @property
    def prev(self) -> "Node":
        return self.__prev

    @prev.setter
    def prev(self, node: "Node" = None) -> None:
        if not self.__frozen:
            self.__prev = node
            return
        raise "Cannot change state of a frozen node"

    def freeze(self) -> None:
        self.__frozen = True

    def unfreeze(self) -> None:
        self.__frozen = False

    def is_frozen(self) -> bool:
        return self.__frozen

    def __repr__(self) -> str:
        return f"Node({self.data!r}, {self.next!r}, {self.prev!r})"
