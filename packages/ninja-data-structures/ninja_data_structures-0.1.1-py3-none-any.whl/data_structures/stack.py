from typing import Any
from collections.abc import Iterable

from docutils.parsers.rst.directives import value_or

from data_structures import Node


class Stack(Iterable):
    def __init__(self, items: Iterable[Any] = None, freeze: bool = False) -> None:
        self.__head = None
        self.__tail = None
        self.__iter_stack = None
        self.__size = 0
        self.__frozen = False

        if items:
            for item in items:
                self.push(item)

        if freeze:
            self.freeze()

    @property
    def head(self) -> Any:
        if self.__head:
            return self.__head.data
        return None

    @property
    def tail(self) -> Any:
        if self.__tail:
            return self.__tail.data
        return None

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

    def is_frozen(self) -> bool:
        return self.__frozen

    def push(self, item: Any) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen stack"
        node = Node(item)
        self.__size += 1

        if self.__head is None:
            self.__head = node
            self.__tail = self.__head
            return
        self.__head.prev = node
        node.next = self.__head
        self.__head = node

    def is_empty(self) -> bool:
        return len(self) == 0

    def pop(self) -> Any:
        if self.is_frozen():
            raise "Cannot change state of a frozen stack"
        if self.is_empty():
            raise Exception("The Stack is empty")

        item = self.__head.data
        self.__size -= 1
        if self.__head is self.__tail:
            self.__head = None
            self.__tail = None
            return item
        self.__head = self.__head.next
        self.__head.prev = None
        return item

    def peek(self) -> Any:
        if self.is_empty():
            raise Exception("The Stack is empty")

        return self.__head.data

    def __list__(self) -> list[Any]:
        node = self.__head
        items = []
        while not node is None:
            items.append(node.data)
            node = node.next
        return items

    def remove(self, item: Any) -> Any:
        if self.is_frozen():
            raise "Cannot change state of a frozen stack"
        node = self.__head
        while not node is None:
            if node.data == item:
                data = node.data
                self.__size -= 1
                if self.__head is node and self.__head is self.__tail:
                    self.__head = None
                    self.__tail = None
                    return data
                if self.__head is node:
                    self.__head = self.__head.next
                    self.__head.prev = None
                    return data
                if self.__tail is node:
                    self.__tail = self.__tail.prev
                    self.__tail.next = None
                    return data
                node.prev.next = node.next
                node.next.prev = node.prev
                return data
            node = node.next

    def insert(self, index: int, item: Any) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen stack"
        if len(self) == 0:
            self.push(item)
            return
        if index < 0:
            index += len(self)
        node = Node(item)
        self.__size += 1
        if index > len(self) - 2 or abs(index + 1) > len(self) - 2:
            node.prev = self.__tail
            self.__tail.next = node
            self.__tail = node
            return

        node_insert = self.__head
        while index >= 0:
            if index == 0:
                if node_insert is self.__head:
                    node.next = self.__head
                    self.__head.prev = node
                    self.__head = node
                    return
                if node_insert is self.__tail:
                    node.next = self.__tail
                    node.prev = self.__tail.prev
                    self.__tail.prev.next = node
                    self.__tail.prev = node
                    return
                node.next = node_insert
                node.prev = node_insert.prev
                node_insert.prev.next = node
                node_insert.prev = node
                return
            node_insert = node_insert.next
            index -= 1

    def clean(self) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen stack"
        self.__head = None
        self.__tail = None
        self.__size = 0

    def gen(self):
        node = self.__head
        while not node is None:
            yield node.data
            node = node.next

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

    def __setitem__(self, index, data) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen stack"
        try:
            if index < 0:
                index += len(self)
            node = self.__head
            while index >= 0:
                if index == 0:
                    node.data = data
                    return
                node = node.next
                index -= 1
        except Exception:
            raise IndexError("Index overflow")

    def __iter__(self) -> "Stack":
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

    def __repr__(self) -> str:
        return f"Stack({list(self)!r})"

    def __len__(self) -> int:
        return self.__size
