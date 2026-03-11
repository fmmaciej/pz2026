from todo_cli.core import TodoList, TodoError


def test_add_creates_new_task_with_next_id():
    t = TodoList.empty()
    item = t.add("Kup jajka")

    assert item.id == 1
    assert item.title == "Kup jajka"
    assert item.done is False


def test_add_multiple_increments_id():
    t = TodoList.empty()
    t.add("Umyj okna")
    item2 = t.add("Umyj naczynia")

    assert item2.id == 2
