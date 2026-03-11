from __future__ import annotations

from todo_cli.domain import TodoList
from todo_cli.ports import TodoRepositoryPort


class CloudTodoRepositoryAdapter(TodoRepositoryPort):
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def load(self) -> TodoList: ...

    def save(self, todos: TodoList) -> None: ...
