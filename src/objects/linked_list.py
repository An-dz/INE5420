from typing import Optional
import numpy as np
from numpy.typing import NDArray

Item = NDArray[np.float64]


class Vertex:
    def __init__(
        self,
        uid: str,
        value: Item,
        is_intersection: bool,
        next_: Optional["Vertex"] = None,
    ) -> None:
        self.__uid = uid
        self.__is_intersection = is_intersection
        self.__value = value
        self.__next = self if next_ is None else next_

    def set_next(self, node: "Vertex") -> None:
        self.__next = node

    def next_node(self) -> "Vertex":
        return self.__next

    def uid(self) -> str:
        return self.__uid

    def coords(self) -> Item:
        return self.__value

    def is_intersection(self) -> bool:
        return self.__is_intersection


class CircularLinkedList:
    def __init__(self, uid_prefix: str) -> None:
        self.__uid_prefix = uid_prefix
        self.__length = 0
        self.__head: Vertex | None = None
        self.__tail: Vertex | None = None
        self.__left: Vertex | None = None
        self.__right: Vertex | None = None
        self.__top: Vertex | None = None
        self.__bottom: Vertex | None = None

    def __len__(self) -> int:
        return self.__length

    def head(self) -> Vertex | None:
        return self.__head

    def append(self, value: Item, is_intersection: bool = False) -> Vertex:
        node = Vertex(
            "{}{}".format(self.__uid_prefix, self.__length),
            value,
            is_intersection,
            self.__head,
        )
        self.__length += 1

        if self.__head and self.__tail:
            if not self.__tail.is_intersection():
                self.__tail.set_next(node)
            self.__tail = node
        else:
            self.__head = node
            self.__tail = node

        if self.__length == 1:
            self.__top = node
        elif self.__length == 2:
            self.__right = node
        elif self.__length == 3:
            self.__bottom = node
        elif self.__length == 4:
            self.__left = node

        return node

    def __append_generic(
        self,
        value: Item,
        current: Vertex | None,
        is_intersection: bool,
    ) -> Vertex:
        if current is None:
            raise UnboundLocalError("Window list should've been initialised beforehand")

        node = Vertex(
            "{}{}".format(self.__uid_prefix, self.__length),
            value,
            is_intersection,
            current.next_node(),
        )
        current.set_next(node)
        self.__length += 1
        return node

    def append_bottom(self, value: Item, is_intersection: bool = True) -> Vertex:
        node = self.__append_generic(value, self.__bottom, is_intersection)
        self.__bottom = node
        return node

    def append_left(self, value: Item, is_intersection: bool = True) -> Vertex:
        node = self.__append_generic(value, self.__left, is_intersection)
        self.__left = node
        return node

    def append_right(self, value: Item, is_intersection: bool = True) -> Vertex:
        node = self.__append_generic(value, self.__right, is_intersection)
        self.__right = node
        return node

    def append_top(self, value: Item, is_intersection: bool = True) -> Vertex:
        node = self.__append_generic(value, self.__top, is_intersection)
        self.__top = node
        return node

    def __repr__(self) -> str:
        return "(CircularLinkedList: {})".format(self.__str__())

    def __str__(self) -> str:
        string = "["
        current = self.__head
        i = self.__length

        while i > 0 and current:
            i -= 1
            string += "\n\t{}, {}, {}".format(str(current.coords()), current.is_intersection(), current.next_node().coords())
            current = current.next_node()

        return string + "\n]"
