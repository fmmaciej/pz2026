from __future__ import annotations

import sys
from pathlib import Path

from todo_cli.adapters.argparse_adapter import ArgparseTodoCliAdapter


def main(argv: list[str] | None = None):
    if argv is None:
        argv = sys.argv[1:]

    db_path = Path.home() / "todo-cli" / "src" / "todo_cli" / ".todo.json"
    cli = ArgparseTodoCliAdapter()
    res = cli.run(argv, db_path)

    if res.stdout:
        sys.stdout.write(res.stdout)
    if res.stderr:
        sys.stderr.write(res.stderr)
    return res.code

if __name__ == "__main__":
    main()
