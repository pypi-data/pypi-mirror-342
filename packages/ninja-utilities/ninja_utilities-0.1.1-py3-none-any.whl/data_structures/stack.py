from typing import Any
from collections.abc import Iterable

from data_structures import Node


class Stack(Iterable):
    def __init__(self, items: Iterable[Any] = None, freeze: bool = False) -> None:
        self.__top = None
        self.__bottom = None
        self.__iter_stack = None
        self.__size = 0
        self.__frozen = False

        if items:
            for item in items:
                self.push(item)

        if freeze:
            self.freeze()

    @property
    def top(self) -> Any:
        if self.__top:
            return self.__top.data
        return None

    @top.setter
    def top(self, value: Any) -> None:
        if self.__top:
            self.__top.data = value
            return
        raise "The stack is empty"

    @property
    def bottom(self) -> Any:
        if self.__bottom:
            return self.__bottom.data
        return None

    @bottom.setter
    def bottom(self, value: Any) -> None:
        if self.__bottom:
            self.__bottom.data = value
            return
        raise "The stack is empty"

    @property
    def top_node(self) -> Node:
        return self.__top

    @top_node.setter
    def top_node(self, node: Node) -> None:
        if isinstance(node, Node) or node is None:
            self.__top = node
            return
        raise "Invalid value"

    @property
    def bottom_node(self) -> Node:
        return self.__bottom

    @bottom_node.setter
    def bottom_node(self, node: Node) -> None:
        if isinstance(node, Node) or node is None:
            self.__bottom = node
            return
        raise "Invalid value"

    def freeze(self) -> None:
        self.__frozen = True
        node = self.__top
        while not node is None:
            node.freeze()
            node = node.next

    def unfreeze(self) -> None:
        self.__frozen = False
        node = self.__top
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

        if self.__top is None:
            self.__top = node
            self.__bottom = self.__top
            return
        self.__top.prev = node
        node.next = self.__top
        self.__top = node

    def is_empty(self) -> bool:
        return len(self) == 0

    def pop(self) -> Any:
        if self.is_frozen():
            raise "Cannot change state of a frozen stack"
        if self.is_empty():
            raise Exception("The Stack is empty")

        item = self.__top.data
        self.__size -= 1
        if self.__top is self.__bottom:
            self.__top = None
            self.__bottom = None
            return item
        self.__top = self.__top.next
        self.__top.prev = None
        return item

    def peek(self) -> Any:
        if self.is_empty():
            raise Exception("The Stack is empty")

        return self.__top.data

    def __list__(self) -> list[Any]:
        node = self.__top
        items = []
        while not node is None:
            items.append(node.data)
            node = node.next
        return items

    def remove(self, item: Any) -> Any:
        if self.is_frozen():
            raise "Cannot change state of a frozen stack"
        node = self.__top
        while not node is None:
            if node.data == item:
                data = node.data
                self.__size -= 1
                if self.__top is node and self.__top is self.__bottom:
                    self.__top = None
                    self.__bottom = None
                    return data
                if self.__top is node:
                    self.__top = self.__top.next
                    self.__top.prev = None
                    return data
                if self.__bottom is node:
                    self.__bottom = self.__bottom.prev
                    self.__bottom.next = None
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
            node.prev = self.__bottom
            self.__bottom.next = node
            self.__bottom = node
            return

        node_insert = self.__top
        while index >= 0:
            if index == 0:
                if node_insert is self.__top:
                    node.next = self.__top
                    self.__top.prev = node
                    self.__top = node
                    return
                if node_insert is self.__bottom:
                    node.next = self.__bottom
                    node.prev = self.__bottom.prev
                    self.__bottom.prev.next = node
                    self.__bottom.prev = node
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
        self.__top = None
        self.__bottom = None
        self.__size = 0

    def gen(self):
        node = self.__top
        while not node is None:
            yield node.data
            node = node.next

    def __getitem__(self, index: int) -> Any:
        if index < 0:
            index += len(self)
        if index >= len(self):
            raise IndexError("Index overflow")
        node = self.__top
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
            node = self.__top
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
        self.__iter_stack.push(self.__top)
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
