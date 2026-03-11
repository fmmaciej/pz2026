from __future__ import annotations

from dataclasses import dataclass


class TodoError(Exception): ...


@dataclass
class InputDTO:
    def __init__(self, title: str, id: str, done: bool):
        self.title: str = title
        self.id: int = int(id)
        self.done: bool = done


@dataclass
class TodoItem:
    title: str
    id: int
    done: bool


@dataclass
class TodoList:
    items: list[TodoItem]

    @classmethod
    def empty(cls) -> TodoList:
        return cls(items=[])

    def add(self, title: str) -> TodoItem:
        item_id = self._next_id()
        item = TodoItem(title=title, id=item_id, done=False)
        self.items.append(item)
        return item

    def remove(self, id: int) -> None:
        index = self._find_index(id)
        if self.items[index].id != 1:
            for item in self.items[index:]:
                item.id -= 1
        self.items.pop(index)

    def done(self, id: int) -> None:
        index = self._find_index(id)
        self.items[index].done = True

    def _next_id(self) -> int:
        if not self.items:
            return 1
        return max(item.id for item in self.items) + 1

    def _find_index(self, id: int) -> int:
        for ind, item in enumerate(self.items):
            if item.id == id:
                return ind
        raise TodoError(f"Couldn't find the index of item of id: {id}")
