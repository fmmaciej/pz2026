from __future__ import annotations

import json
from pathlib import Path

from todo_cli.domain import TodoItem, TodoList
from todo_cli.ports import TodoRepositoryPort


class JsonTodoRepositoryAdapter(TodoRepositoryPort):
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def load(self) -> TodoList:
        if not self.file_path.exists():
            return TodoList.empty()

        raw = self.file_path.read_text().strip()
        if not raw:
            return TodoList.empty()
        data = json.loads(raw)

        items: list[TodoItem] = []
        for it in data:
            item = TodoItem(
                title=it["title"],
                id=it["id"],
                done=it.get("done", False)
            )

            items.append(item)

        return TodoList(items)

    def save(self, todos: TodoList) -> None:
        #1 O ile nie istnieje, utwórz katalog
        #2 Przeiteruj po elementach todos
        #3 Zapisać do zmiennej a zmienną do pliku (write_text)

        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        data = [x.__dict__ for x in todos.items]
        self.file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )

