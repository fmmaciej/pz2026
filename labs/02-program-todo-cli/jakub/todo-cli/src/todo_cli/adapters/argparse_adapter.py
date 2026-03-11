from __future__ import annotations

import argparse
from pathlib import Path

from todo_cli.adapters.json_todo_repository_adapter import JsonTodoRepositoryAdapter
from todo_cli.app import TodoApp

#from todo_cli.domain import InputDTO
from todo_cli.ports import RunResult, TodoCliPort


class ArgparseTodoCliAdapter(TodoCliPort):
    def run(self, argv: list[str], db_path: Path ) -> RunResult:
        if not db_path:
            db_path = Path(".todo.json")
        p = argparse.ArgumentParser(prog="Todo")
        sub = p.add_subparsers(dest="cmd", required=True)

        add = sub.add_parser("add")
        add.add_argument("title")

        sub.add_parser("list")

        done = sub.add_parser("done")
        done.add_argument("id")

        rm = sub.add_parser("rm")
        rm.add_argument("id")

        args = p.parse_args(argv)
        #input_args = InputDTO(args.title, args.id, args.done) -
        # Poprawnie należało by utworzyć dodatkowy obiekt którego odpowiedzialnościa będzie
        # dopilnowanie odpowiednich typów, które mają być przekazane do use-cases'ów.
        # Jako rozwiązanie (hotfix) zrobimy rzutowanie w 45 i 47 linijce

        repo = JsonTodoRepositoryAdapter(db_path)
        app = TodoApp(repo)

        if args.cmd == "add":
            res = app.add(args.title)
        elif args.cmd == "list":
            res = app.list()
        elif args.cmd == "done":
            res = app.done(int(args.id))
        elif args.cmd == "rm":
            res = app.rm(int(args.id))
        else:
            return RunResult(
                code=2,
                stdout="",
                stderr="Unknown command.\n"
            )
        return RunResult(
            code=res.code,
            stdout=res.out,
            stderr=res.err
        )
