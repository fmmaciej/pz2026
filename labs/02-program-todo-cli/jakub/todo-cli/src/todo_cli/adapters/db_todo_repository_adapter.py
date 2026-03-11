from __future__ import annotations

from ..domain import TodoList
from ..ports import TodoRepositoryPort


class DBTodoRepositoryAdapter(TodoRepositoryPort):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def load(self) -> TodoList: ...

    def save(self, todos: TodoList) -> None: ...
