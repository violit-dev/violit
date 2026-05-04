# 5. Very Simple ORM Example

This example is a small introduction to Violit ORM with SQLite.

It shows how to:

- define one table with SQLModel
- add rows with `app.db.add(...)`
- read rows with `app.db.filter(...)`
- update rows with `app.db.save(...)`
- delete rows with `app.db.delete(...)`

It also uses `migrate="auto"`, so simple model changes can update the SQLite schema automatically.

## Files

- `demo_orm_app.py`: the whole example
- `todo.db`: created automatically the first time you run the app

## Run

```bash
cd examples/5_orm
python demo_orm_app.py
```

## What The App Does

The app gives you a small todo manager.

You can:

- type a todo and press Enter
- click `Add Todo`
- click `Add Demo Rows`
- mark a row as `Done` or `Undo`
- click `Delete`
- click `Clear Done`

The input clears after saving, and the list refreshes immediately.

## Read The Code In This Order

### 1. The model

```python
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    done: bool = False
```

This is one Python class and one database table.

### 2. The app setup

```python
app = vl.App(
    db=str(DB_PATH),
    migrate="auto",
)
```

That is enough to create and use the SQLite database.

### 3. The input

```python
new_title = app.text_input(
    "New todo",
    on_submit=add_todo,
)
```

With `on_submit` present, Enter submits automatically, so the example works with both Enter and the button.

### 4. Database actions

```python
app.db.add(Todo(title=title))
app.db.save(todo)
app.db.delete(todo)
app.db.delete_by(Todo, Todo.done == True)
```

These lines cover create, update, and delete.

### 5. Reactive rendering

```python
@reactivity
def render_todos() -> None:
    refresh_tick.value
    todos = app.db.filter(Todo, order_by=Todo.id.desc())
```

The example uses a small refresh state so the UI rerenders after each database action.

## Try A Migration In 30 Seconds

Open `demo_orm_app.py` and add one more field to the `Todo` model.

Example:

```python
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    done: bool = False
    priority: int = 0
```

Then run the app again:

```bash
python demo_orm_app.py
```

Because this example uses `migrate="auto"`, Violit will add the missing column to `todo.db`.

## Reset The Example

Delete `todo.db` if you want to start from a clean database.
