# 6. Very Simple Auth Example

This example is a small introduction to Violit Auth.

It shows how to:

- create a user with `app.auth.create_user(...)`
- log in with `app.auth.login(...)`
- read the current user with `app.auth.current_user()`
- log out with `app.auth.logout()`

The app stores users in SQLite, so accounts remain after restart.

## Files

- `demo_auth_app.py`: the whole example
- `auth_demo.db`: created automatically when you run the app

## Run

```bash
cd examples/6_auth
python demo_auth_app.py
```

## What The App Does

This example keeps everything on one page.

When you are logged out, it shows two cards:

- `Sign Up`
- `Login`

When you are logged in, it shows:

- your username and role
- a `Logout` button
- a small protected content box that only appears for authenticated sessions

After sign up, the example logs the user in automatically.

## Read The Code In This Order

### 1. Define the user table

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str
    role: str = "user"
```

### 2. Enable auth

```python
app = vl.App(db=str(DB_PATH), migrate="auto")
app.setup_auth(User)
```

That turns on the built-in auth system for this model.

### 3. Sign up

```python
app.auth.create_user(username, password)
app.auth.login(username, password)
```

The password is hashed before storage, and the demo logs the new user in right away.

### 4. Log in and log out

```python
app.auth.login(username, password)
app.auth.logout()
```

### 5. Read the session user

```python
current_user = app.auth.current_user()
```

The page switches its UI based on whether `current_user` exists.

### 6. Reactive auth

```python
@reactivity
def render_auth_example() -> None:
    current_user = app.auth.current_user()
```

`app.auth.current_user()` now participates in render-time dependency tracking, so the screen updates right after sign up, login, and logout without a manual helper state.

## Why This Example Is Small

There is no custom auth backend and no page router in this demo.

You only need:

- a `User` model
- a database path
- `app.setup_auth(User)`
- a few calls to `app.auth.*`

## Next Step

If you later want route protection, you can move from this single-page example to `app.navigation(...)` with `require_auth=True` pages.
