from collections.abc import Iterable
from typing import Any

from data_structures import Node, Stack


class LinkedList(Iterable):
    def __init__(self, items: Iterable[Any] = None, freeze: bool = False) -> None:
        self.__size = 0
        self.__head = None
        self.__tail = None
        self.__iter_stack = None
        self.__frozen = False

        if items:
            for item in items:
                self.add_last(item)

        if freeze:
            self.freeze()

    @property
    def head(self) -> Any:
        return self.__head

    @property
    def tail(self) -> Any:
        return self.__tail

    @head.setter
    def head(self, value: Any) -> None:
        if self.__head:
            self.__head.data = value
            return
        raise "The list is empty"

    @tail.setter
    def tail(self, value: Any) -> None:
        if self.__tail:
            self.__tail.data = value
        raise "The list is empty"

    @property
    def head_node(self) -> Node:
        return self.__head

    @head_node.setter
    def head_node(self, node: Node) -> None:
        if isinstance(node, Node) or node is None:
            self.__head = node
            return
        raise "Invalid value"

    @property
    def tail_node(self) -> Node:
        return self.__tail

    @tail_node.setter
    def tail_node(self, node: Node) -> None:
        if isinstance(node, Node) or node is None:
            self.__tail = node
            return
        raise "Invalid value"

    def is_frozen(self) -> bool:
        return self.__frozen

    def freeze(self) -> None:
        self.__frozen = True
        node = self.__head
        while not node is None:
            node.freeze()
            node = node.next

    def unfreeze(self) -> None:
        self.__frozen = False
        node = self.__head
        while not node is None:
            node.unfreeze()
            node = node.next

    def add_last(self, item: Any) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen list"
        node = Node(item)
        self.__size += 1
        if self.__head is None:
            self.__head = node
            self.__tail = node
            return
        node.prev = self.__tail
        self.__tail.next = node
        self.__tail = node

    def add_first(self, item: Any) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen list"
        node = Node(item)
        self.__size += 1
        if self.__head is None:
            self.__head = node
            self.__tail = node
            return
        node.next = self.__head
        self.__head.prev = node
        self.__head = node

    def find(self, item: Any) -> bool:
        node = self.__head
        while not node is None:
            if node.data == item:
                return True
            node = node.next
        return False

    def pop_last(self) -> Any:
        if self.is_frozen():
            raise "Cannot change state of a frozen list"
        if self.is_empty():
            raise "Empty list"
        self.__size -= 1
        data = self.__tail.data
        if self.__head == self.__tail:
            self.__head = None
            self.__tail = None
            return data
        self.__tail = self.__tail.prev
        self.__tail.next = None
        return data

    def pop_first(self) -> Any:
        if self.is_frozen():
            raise "Cannot change state of a frozen list"
        if self.is_empty():
            raise "Empty list"
        self.__size -= 1
        data = self.__head
        if self.__head is self.__tail:
            self.__head = None
            self.__tail = None
            return data
        self.__head = self.__head.next
        self.__head.prev = None
        return data

    def remove(self, item: Any) -> Any:
        if self.is_frozen():
            raise "Cannot change state of a frozen list"
        if self.is_empty():
            return None
        if self.__head is self.__tail:
            if self.__head.data == item:
                self.__size -= 1
                return self.__head.data
            return None
        node = self.__head
        while not node is None:
            if node.data == item:
                self.__size -= 1
                if node is self.__head:
                    self.__head = self.__head.next
                    self.__head.prev = None
                    return node.data
                if node is self.__tail:
                    self.__tail = self.__tail.prev
                    self.__tail.next = None
                    return node.data
                node.prev.next = node.next
                node.next.prev = node.prev
                return node.data
            node = node.next
        return None

    def insert(self, index: int, item: Any) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen list"
        if index < 0:
            index += len(self)
        if index >= len(self):
            self.add_last(item)
            return
        self.__size += 1
        insert_node = Node(item)
        if index == 0:
            self.__head.prev = insert_node
            insert_node.next = self.__head
            self.__head = insert_node
            return
        if index == len(self) - 2:
            insert_node.next = self.__tail
            insert_node.prev = self.__tail.prev
            self.__tail.prev.next = insert_node
            self.__tail.prev = insert_node
            return
        node = self.__head
        while not node is None:
            if index == 0:
                insert_node.next = node
                insert_node.prev = node.prev
                node.prev.next = insert_node
                node.prev = insert_node
                return
            node = node.next
            index -= 1
        raise "Error"

    def clean(self) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen list"
        self.__head = None
        self.__tail = None
        self.__size = 0

    def is_empty(self) -> bool:
        return len(self) == 0

    def gen(self):
        node = self.__head
        while not node is None:
            yield node.data
            node = node.next

    def __list__(self) -> list[Any]:
        items_list = []
        node = self.__head
        while not node is None:
            items_list.append(node.data)
            node = node.next
        return items_list

    def __getitem__(self, index: int) -> Any:
        if index < 0:
            index += len(self)
        if index >= len(self):
            raise IndexError("Index overflow")
        node = self.__head
        while not node is None:
            if index == 0:
                return node.data
            node = node.next
            index -= 1

    def __setitem__(self, index: int, item: Any) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen list"
        if index < 0:
            index += len(self)
        if index >= len(self):
            raise IndexError("Index overflow")
        node = self.__head
        while not node is None:
            if index == 0:
                node.data = item
                return
            node = node.next
            index -= 1

    def __iter__(self) -> "LinkedList":
        if not self.__iter_stack:
            self.__iter_stack = Stack()
        self.__iter_stack.push(self.__head)
        return self

    def __next__(self) -> Any:
        node = self.__iter_stack.peek()
        if node is None:
            self.__iter_stack.pop()
            raise StopIteration
        self.__iter_stack[0] = node.next
        return node.data

    def __len__(self) -> int:
        return self.__size

    def __repr__(self) -> str:
        return f"LinkedList({list(self)!r})"
