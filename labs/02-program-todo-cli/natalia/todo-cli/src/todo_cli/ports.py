from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from todo_cli.domain import TodoList


@dataclass
class Result:
    code: int
    out: str
    err: str


@dataclass
class RunResult:
    code: int
    stdout: str
    stderr: str


class TodoAppPort(Protocol):
    def add(self, title: str) -> Result: ...
    def list(self) -> Result: ...
    def done(self, id: int) -> Result: ...
    def rm(self, id: int) -> Result: ...


class TodoRepositoryPort(Protocol):
    def load(self) -> TodoList: ...
    def save(self, todos: TodoList) -> None: ...


class TodoCliPort(Protocol):
    def run(self, argv: list[str], db_path: Path) -> RunResult: ...
