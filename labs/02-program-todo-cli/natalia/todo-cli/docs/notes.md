# Notes

```python
from typing import Protocol

class TodoRepositoryPort(Protocol) {
    def load() -> TodoList: ...
    def save(todos: TodoList) -> None: ...
}

from .TodoRepositoryPort import TodoRepositoryPort
class JsonTodoRepositoryAdapter(TodoRepositoryPort) {
    def load() -> TodoList:
        raise ToBeImplemented
    def save(todos: TodoList) -> None:
        raise ToBeImplemented
}
```

```python
from databases import database

@dataclass
class TodoItem():
    int id
```
