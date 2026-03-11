from ..use_cases.todo_app_port import TodoAppPort


class TyperAdapter(TodoAppPort):
    def __init__(self, app_port: TodoAppPort = None):
        self.app_port = app_port

    def run(self, argv: list, db_path: str): ...
