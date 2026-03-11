from todo_cli.ports import Result, TodoAppPort, TodoRepositoryPort


class TodoApp(TodoAppPort):
    def __init__(self, repo: TodoRepositoryPort):
        self.repo = repo

    def list(self) -> Result:
        todos = self.repo.load()
        lines: list[str] = []
        for item in todos.items:
            if item.done:
                mark = "OK"
            else:
                mark = "  "
            lines.append(f'[{mark}] {item.id}: {item.title}')
        out="\n".join(lines)
        out += "\n"

        return Result(
            code=0,
            out=out,
            err=""
        )

    def add(self, title: str) -> Result:
        todos = self.repo.load()
        item = todos.add(title)
        self.repo.save(todos)
        out = f"Added: {item.id}: {item.title}\n"
        return Result(
            code=0,
            out=out,
            err=""
        )

    def done(self, id: int) -> Result:
        todos = self.repo.load()
        todos.done(id)
        self.repo.save(todos)
        out = f"Marked todo: {id} as done\n"
        return Result(
            code=0,
            out=out,
            err=""
        )

    def rm(self, id: int) -> Result:
        todos = self.repo.load()
        todos.remove(id)
        self.repo.save(todos)
        out = f"Removed todo {id}\n"
        return Result(
            code=0,
            out=out,
            err=""
        )
