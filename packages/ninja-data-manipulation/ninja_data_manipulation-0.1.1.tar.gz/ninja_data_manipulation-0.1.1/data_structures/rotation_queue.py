from typing import Any
from collections.abc import Iterable

from data_structures import Queue


class RotationQueue(Queue):
    def __init__(
        self, items: Iterable[Any] = None, queue_size: int = 0, freeze: bool = False
    ) -> None:
        super().__init__(items, queue_size, freeze)

    def rotate(self, times: int = 1, reverse: bool = False) -> None:
        if self.is_frozen():
            raise "Cannot rotate a frozen queue"
        if self.is_empty() or len(self) == 1:
            return
        if reverse:
            for _ in range(times):
                self.__reverse_rotation()
            return
        for _ in range(times):
            self.__rotation()

    def __reverse_rotation(self) -> None:
        node = self.first_node
        node.prev = self.last_node
        self.last_node.next = node
        self.first_node = node.next
        node.next = None
        self.first_node.prev = None
        self.last_node = node

    def __rotation(self) -> None:
        node = self.last_node
        node.next = self.first_node
        self.first_node.prev = node
        self.first_node = node
        self.last_node = node.prev
        self.last_node.next = None
        node.prev = None

    def __repr__(self) -> str:
        return (
            f"RotationQueue({list(self)!r}, {self.__queue_size!r}, {self.__frozen!r})"
        )
