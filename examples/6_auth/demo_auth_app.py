from pathlib import Path
from typing import Any, Optional, cast

import violit as vl
from sqlmodel import Field, SQLModel


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "auth_demo.db"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str
    role: str = "user"


app = vl.App(
    title="Violit Very Simple Auth Example",
    theme="violit_light_jewel",
    container_width="820px",
    db=str(DB_PATH),
    migrate="auto",
)
app.setup_auth(User)

auth_tick = app.state(0, key="auth_example_tick")


def refresh_auth_ui() -> None:
    auth_tick.set(auth_tick.value + 1)


reactivity = cast(Any, app.reactivity)


app.html(
    """
    <div class="mb-5 rounded-[28px] border border-slate-200/80 bg-gradient-to-br from-white via-emerald-50 to-sky-100 p-6 shadow-[0_28px_90px_-48px_rgba(15,23,42,0.55)]">
        <div class="text-[11px] font-black uppercase tracking-[0.32em] text-emerald-700">Violit Example 06</div>
        <h1 class="mt-2 text-3xl font-black tracking-tight text-slate-900">Very Simple Auth</h1>
        <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
            Create an account, log in, see a protected area, and log out.
        </p>
    </div>
    """
)


@reactivity
def render_auth_example() -> None:
    auth_tick.value
    current_user = app.auth.current_user()
    total_users = app.db.count(User)

    app.caption(f"Database: {DB_PATH.name} | users: {total_users}")

    if current_user is not None:
        with app.container(
            cls="mb-4 rounded-[24px] border border-emerald-200/80 bg-white/90 p-5 shadow-[0_18px_55px_-40px_rgba(16,185,129,0.55)]"
        ):
            app.success(f"Logged in as {current_user.username}")
            app.caption(f"role: {current_user.role}")
            app.text("This box is the protected part of the page. It only appears after login.")

            def do_logout() -> None:
                app.auth.logout()
                refresh_auth_ui()
                app.toast("Logged out.", variant="success")

            app.button("Logout", on_click=do_logout, variant="neutral")

        with app.container(border=True):
            app.subheader("Protected Content")
            app.text("If you can see this, the session is authenticated.")
            app.code(
                """user = app.auth.current_user()\nif user:\n    app.text(f\"Hello, {user.username}\")""",
                language="python",
                copy_button=False,
            )
        return

    columns = app.columns(2)

    with columns[0]:
        with app.container(
            cls="rounded-[24px] border border-slate-200/80 bg-white/90 p-5 shadow-[0_18px_55px_-42px_rgba(15,23,42,0.35)]"
        ):
            app.subheader("Sign Up")
            signup_username = app.text_input("Username", key="auth_signup_username")
            signup_password = app.text_input(
                "Password",
                key="auth_signup_password",
                type="password",
            )

            def do_signup() -> None:
                username = signup_username.value.strip()
                password = signup_password.value.strip()
                if not username or not password:
                    app.toast("Enter a username and password.", variant="danger")
                    return
                if app.db.exists(User, User.username == username):
                    app.toast("That username already exists.", variant="danger")
                    return
                app.auth.create_user(username, password)
                app.auth.login(username, password)
                signup_username.set("")
                signup_password.set("")
                refresh_auth_ui()
                app.toast("Account created. You are now logged in.", variant="success")

            app.button("Create Account", on_click=do_signup)

    with columns[1]:
        with app.container(
            cls="rounded-[24px] border border-slate-200/80 bg-white/90 p-5 shadow-[0_18px_55px_-42px_rgba(15,23,42,0.35)]"
        ):
            app.subheader("Login")
            login_username = app.text_input("Username", key="auth_login_username")
            login_password = app.text_input(
                "Password",
                key="auth_login_password",
                type="password",
            )

            def do_login() -> None:
                username = login_username.value.strip()
                password = login_password.value.strip()
                if not username or not password:
                    app.toast("Enter a username and password.", variant="danger")
                    return
                if app.auth.login(username, password):
                    login_username.set("")
                    login_password.set("")
                    refresh_auth_ui()
                    app.toast("Login successful.", variant="success")
                else:
                    app.toast("Invalid username or password.", variant="danger")

            app.button("Login", on_click=do_login, variant="neutral")

    app.info("Create a user on the left, or log in with an existing user on the right.")
    app.text("After login, the protected card appears automatically.")


render_auth_example()


app.run()