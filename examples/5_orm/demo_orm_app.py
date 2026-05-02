from pathlib import Path
from typing import Any, Optional, cast

from sqlmodel import Field, SQLModel

import violit as vl


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "todo.db"


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    done: bool = False


app = vl.App(
    title="Violit Very Simple ORM Example",
    theme="violit_light_jewel",
    container_width="760px",
    db=str(DB_PATH),
    migrate="auto",
)

refresh_tick = app.state(0, key="orm_example_refresh")

app.title("Very Simple ORM Example")
app.caption(f"Database: {DB_PATH.name} | migrate='auto'")
app.text("One model, one SQLite file, and a few app.db calls.")


def touch_db() -> None:
    refresh_tick.set(refresh_tick.value + 1)


def add_todo(_value: str | None = None) -> None:
    title = new_title.value.strip()
    if not title:
        app.toast("Type a title first.", variant="danger")
        return
    app.db.add(Todo(title=title))
    new_title.set("")
    touch_db()
    app.toast("Saved to SQLite.", variant="success")


def add_demo_rows() -> None:
    for title in ["Learn the model", "Insert a row", "Try a migration"]:
        if not app.db.exists(Todo, Todo.title == title):
            app.db.add(Todo(title=title))
    touch_db()


def clear_done_rows() -> None:
    app.db.delete_by(Todo, Todo.done == True)
    touch_db()


with app.container(border=True):
    new_title = app.text_input(
        "New todo",
        key="orm_example_title",
        placeholder="Write one short task",
        on_submit=add_todo,
        submit_on_enter=True,
    )
    controls = app.columns(3)


with controls[0]:
    app.button("Add Todo", on_click=add_todo)
with controls[1]:
    app.button("Add Demo Rows", on_click=add_demo_rows, variant="neutral")
with controls[2]:
    app.button("Clear Done", on_click=clear_done_rows, variant="danger")


def toggle_todo(todo_id: int) -> None:
    todo = app.db.get(Todo, todo_id)
    if todo is None:
        return
    todo.done = not todo.done
    app.db.save(todo)
    touch_db()


def delete_todo(todo_id: int) -> None:
    todo = app.db.get(Todo, todo_id)
    if todo is None:
        return
    app.db.delete(todo)
    touch_db()


reactivity = cast(Any, app.reactivity)


@reactivity
def render_todos() -> None:
    refresh_tick.value
    todos = app.db.filter(Todo, order_by=Todo.id.desc())
    done_count = sum(1 for todo in todos if todo.done)

    app.divider()
    app.text(f"Rows in database: {len(todos)} | Done: {done_count}")

    if not todos:
        app.info("No rows yet. Add one above.")
        return

    for todo in todos:
        with app.container(border=True):
            row = app.columns(3)
            with row[0]:
                status = "done" if todo.done else "open"
                app.markdown(f"**{todo.title}**")
                app.caption(f"id={todo.id} | status={status}")
            with row[1]:
                label = "Undo" if todo.done else "Done"
                app.button(label, on_click=lambda todo_id=todo.id: toggle_todo(todo_id), variant="neutral")
            with row[2]:
                app.button("Delete", on_click=lambda todo_id=todo.id: delete_todo(todo_id), variant="danger")


render_todos()


app.run()