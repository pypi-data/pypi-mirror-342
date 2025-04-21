from typing import Any
from collections.abc import Iterable

from data_structures import Node, Stack


class Queue(Iterable):
    def __init__(
        self, items: Iterable[Any] = None, queue_size: int = 0, freeze: bool = False
    ) -> None:
        self.queue_size = queue_size
        self.__iter_stack = None
        self.__first = None
        self.__last = None
        self.__size = 0
        self.__frozen = False

        if items:
            for item in items:
                self.enqueue(item)

        if freeze:
            self.freeze()

    @property
    def queue_size(self) -> int:
        return self.__queue_size

    @queue_size.setter
    def queue_size(self, size: int) -> None:
        if isinstance(size, int):
            self.__queue_size = size
            return
        raise f"Invalid queue size value {size}"

    @property
    def first_node(self) -> Node:
        return self.__first

    @property
    def last_node(self) -> Node:
        return self.__last

    @property
    def first(self) -> Any:
        if self.__first:
            return self.__first.data
        return None

    @first.setter
    def first(self, value: Any) -> None:
        if self.__first:
            self.__first.data = value
            return
        raise "The queue is empty"

    @first_node.setter
    def first_node(self, node: Node = None) -> None:
        if isinstance(node, Node) or node is None:
            self.__first = node
            return
        raise "Invalid value"

    @property
    def last(self) -> Any:
        if self.__last:
            return self.__last.data
        return None

    @last.setter
    def last(self, value: Any) -> None:
        if self.__last:
            self.__last.data = value
            return
        raise "The queue is empty"

    @last_node.setter
    def last_node(self, node: Node = None) -> None:
        if isinstance(node, Node) or node is None:
            self.__last = node
            return
        raise "Invalid value"

    def freeze(self) -> None:
        self.__frozen = True
        node = self.__first
        while not node is None:
            node.freeze()
            node = node.next

    def unfreeze(self) -> None:
        self.__frozen = False
        node = self.__first
        while not node is None:
            node.unfreeze()
            node = node.next

    def is_empty(self) -> bool:
        return len(self) == 0

    def is_frozen(self) -> bool:
        return self.__frozen

    def enqueue(self, item: Any) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen queue"
        node = Node(item)
        self.__size += 1
        if self.__first is None:
            self.__first = node
            self.__last = node
            return
        if self.__first == self.__last:
            self.__first.next = node
            node.prev = self.__first
            self.__last = node
            return
        node.prev = self.__last
        self.__last.next = node
        self.__last = node

    def dequeue(self) -> Any:
        if self.is_frozen():
            raise "Cannot change state of a frozen queue"
        if self.is_empty():
            raise "The Queue is empty"
        self.__size -= 1
        data = self.__first.data
        if self.__first is self.__last:
            self.__first = None
            self.__last = None
            return data
        self.__first = self.__first.next
        self.__first.prev = None
        return data

    def peek(self) -> Any:
        if self.is_empty():
            raise "The Queue is empty"
        return self.__first.data

    def poll(self) -> Any:
        if self.is_frozen():
            raise "Cannot change state of a frozen queue"
        try:
            return self.dequeue()
        except:
            return None

    def offer(self, item: Any) -> bool:
        if self.is_frozen():
            raise "Cannot change state of a frozen queue"
        if self.is_full():
            return False
        self.enqueue(item)
        return True

    def remove(self, item: Any) -> Any:
        if self.is_frozen():
            raise "Cannot change state of a frozen queue"
        if self.is_empty():
            return None
        if self.__first is self.__last:
            if self.__first.data == item:
                data = self.__first.data
                self.__first = None
                self.__last = None
                self.__size -= 1
                return data
            return None
        node = self.__first
        while not node is None:
            if node.data == item:
                self.__size -= 1
                if node is self.__first:
                    self.__first = self.__first.next
                    self.__first.prev = None
                    return node.data
                if node is self.__last:
                    self.__last = self.__last.prev
                    self.__last.next = None
                    return node.data
                node.prev.next = node.next
                node.next.prev = node.prev
                return node.data
            node = node.next
        return None

    def find(self, item: Any) -> bool:
        node = self.__first
        while not node is None:
            if node.data == item:
                return True
            node = node.next
        return False

    def is_full(self) -> bool:
        if self.queue_size == 0:
            return False
        return len(self) == self.queue_size

    def clean(self) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen queue"
        self.__first = None
        self.__last = None
        self.__size = 0

    def insert(self, index: int, item: Any) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen queue"
        if index < 0:
            index += len(self)
        if index >= len(self):
            self.enqueue(item)
        self.__size += 1
        insert_node = Node(item)
        if index == 0:
            insert_node.next = self.__first
            self.__first.prev = insert_node
            self.__first = insert_node
            return
        if index == len(self) - 2:
            insert_node.next = self.__last
            insert_node.prev = self.__last.prev
            self.__last.prev.next = insert_node
            self.__last.prev = insert_node
            return
        node = self.__first
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

    def gen(self):
        node = self.__first
        while not node is None:
            yield node.data
            node = node.next

    def __getitem__(self, index: int) -> Any:
        if index < 0:
            index += len(self)
        if index >= len(self):
            raise IndexError("Index overflow")
        node = self.__first
        while not node is None:
            if index == 0:
                return node.data
            node = node.next
            index -= 1
        raise "Error"

    def __setitem__(self, index, item) -> None:
        if self.is_frozen():
            raise "Cannot change state of a frozen queue"
        if index < 0:
            index += len(self)
        if index >= len(self):
            raise IndexError("Index overflow")
        node = self.__first
        while not node is None:
            if index == 0:
                node.data = item
                return
            node = node.next
            index -= 1
        raise "Error"

    def __iter__(self) -> "Queue":
        if not self.__iter_stack:
            self.__iter_stack = Stack()
        self.__iter_stack.push(self.__first)
        return self

    def __next__(self) -> Any:
        node = self.__iter_stack.peek()
        if node is None:
            self.__iter_stack.pop()
            raise StopIteration
        self.__iter_stack[0] = node.next
        return node.data

    def __list__(self) -> list[Any]:
        queue_list = []
        node = self.__first
        while not node is None:
            queue_list.append(node.data)
            node = node.next
        return queue_list

    def __len__(self) -> int:
        return self.__size

    def __repr__(self) -> str:
        return f"Queue({list(self)!r})"
