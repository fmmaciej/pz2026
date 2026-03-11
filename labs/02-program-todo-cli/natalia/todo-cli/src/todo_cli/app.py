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

        return Result(
            code=0,
            out=out,
            err=""
        )

    def add(self, title: str) -> Result:
        todos = self.repo.load()
        new_item = todos.add(title)
        self.repo.save(todos)

        return Result(
            code=0,
            out=f"Added: {new_item.title}",
            err=""
        )


    def done(self, id: int) -> Result:
        todos = self.repo.load()
        todos.done(id)
        self.repo.save(todos)

        return Result(
            code=0,
            out=f"Marked: {id}",
            err=""
        )

    def rm(self, id: int) -> Result:
        todos = self.repo.load()
        todos.remove(id)
        self.repo.save(todos)

        return Result(
            code=0,
            out=f"Removed: {id}",
            err=""
        )
