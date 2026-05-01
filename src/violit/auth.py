"""
violit/auth.py
==============
Violit Auth system.

Stores user_id on top of the existing ss_sid session store (GLOBAL_STORE[sid]).
Uses bcrypt directly for password hashing.

Usage:
    app = vl.App(db="./app.db")
    app.setup_auth(User)

    app.auth.login("username", "password")  → bool
    app.auth.current_user()                 → User | None
    app.auth.logout()
    app.auth.is_authenticated()             → bool
    app.auth.has_role("admin")              → bool
    app.auth.create_user("user", "pass")    → User
    app.auth.change_password(user, "pw")    → User
    app.auth.delete_user(user)
"""

from __future__ import annotations

import logging
from typing import Optional, Type, TypeVar

logger = logging.getLogger("violit.auth")

try:
    import bcrypt as _bcrypt
    _BCRYPT_AVAILABLE = True
except ImportError:
    _BCRYPT_AVAILABLE = False

T = TypeVar("T")

# Session store key used to persist user_id inside violit's internal session
_AUTH_USER_ID_KEY = "auth_user_id"


def _check_bcrypt():
    if not _BCRYPT_AVAILABLE:
        raise ImportError(
            "[violit.auth] bcrypt package is required.\n"
            "  pip install bcrypt"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Password hashing utilities
# ─────────────────────────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    """Hash a plaintext password with bcrypt."""
    _check_bcrypt()
    salt = _bcrypt.gensalt()
    return _bcrypt.hashpw(plain.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Compare a plaintext password against a bcrypt hash in a timing-safe manner."""
    _check_bcrypt()
    try:
        return _bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# ViolItAuth
# ─────────────────────────────────────────────────────────────────────────────

class ViolItAuth:
    """
    Violit Auth accessor object. Access via ``app.auth``.

    Parameters
    ----------
    app : App
        The violit App instance.
    user_model : Type[T]
        SQLModel-based User model class.
    username_field : str
        Name of the username column (default: "username").
    password_field : str
        Name of the hashed password column (default: "hashed_password").
    role_field : str
        Name of the role column (default: "role").
        If the User model does not have this field, has_role() always returns False.
    login_page : str
        Title of the page to redirect to on unauthenticated access (default: "Login").
    require_auth : bool
        If True, all pages are automatically protected (default: False).
    """

    def __init__(
        self,
        app,
        user_model: Type[T],
        username_field: str = "username",
        password_field: str = "hashed_password",
        role_field: str = "role",
        login_page: str = "Login",
        require_auth: bool = False,
    ):
        self._app = app
        self._user_model = user_model
        self._username_field = username_field
        self._password_field = password_field
        self._role_field = role_field
        self._login_page = login_page
        self._require_all = require_auth

    # ─────────────────────────────────────────────────────────────────────
    # Internal: session store read/write
    # ─────────────────────────────────────────────────────────────────────

    def _get_store(self) -> dict:
        from .state import get_browser_session_store
        return get_browser_session_store()

    def _get_user_id(self) -> Optional[int]:
        """Return the user_id stored in the current session, or None if not logged in."""
        return self._get_store().get(_AUTH_USER_ID_KEY)

    def _set_user_id(self, user_id: Optional[int]) -> None:
        """Write user_id to the current session. Removes the key if None."""
        store = self._get_store()
        if user_id is None:
            store.pop(_AUTH_USER_ID_KEY, None)
        else:
            store[_AUTH_USER_ID_KEY] = user_id

    # ─────────────────────────────────────────────────────────────────────
    # Internal: page navigation
    # ─────────────────────────────────────────────────────────────────────

    def _redirect_to_login(self) -> None:
        """Navigate to the login page by directly setting _navigation_states."""
        page_title = self._login_page
        p = (
            self._app._navigation_pages_by_title.get(page_title)
            or self._app._navigation_pages_by_title.get(page_title.lower())
        )
        if p is None:
            logger.warning(
                f"[violit.auth] Login page '{page_title}' not found. "
                f"Check that the page title matches what was registered in navigation()."
            )
            return
        for nav_state in self._app._navigation_states:
            nav_state.set(p.key)

    # ─────────────────────────────────────────────────────────────────────
    # Public API: authentication
    # ─────────────────────────────────────────────────────────────────────

    def login(self, username: str, password: str) -> bool:
        """
        Log in with username and password.

        Stores user_id in the session on success and returns True.
        Returns False on failure.

        Example::

            if app.auth.login(username.value, password.value):
                app.navigation_go("Home")
            else:
                app.toast("Invalid credentials", "danger")
        """
        if self._app.db is None:
            raise RuntimeError(
                "[violit.auth] app.db is not configured. "
                "Set a database with App(db='...')."
            )

        # Look up the user by username
        user = self._app.db.first(
            self._user_model,
            getattr(self._user_model, self._username_field) == username,
        )

        if user is None:
            # User does not exist — compare against a dummy hash to prevent timing attacks
            verify_password(password, "$2b$12$dummyhashfortimingantiattack1234567890abcdef")
            return False

        hashed = getattr(user, self._password_field, None)
        if hashed is None or not verify_password(password, hashed):
            return False

        self._set_user_id(user.id)
        logger.info(f"[violit.auth] Login successful: {username}")
        return True

    def logout(self) -> None:
        """
        Log out by removing user_id from the current session.

        Example::

            app.button("Logout", on_click=lambda: (app.auth.logout(), app.navigation_go("Login")))
        """
        uid = self._get_user_id()
        self._set_user_id(None)
        if uid is not None:
            logger.info("[violit.auth] Logged out")

    def current_user(self) -> Optional[T]:
        """
        Return the currently logged-in User object, or None if not authenticated.

        Example::

            user = app.auth.current_user()
            if user:
                app.text(f"Hello, {user.username}!")
        """
        user_id = self._get_user_id()
        if user_id is None:
            return None
        if self._app.db is None:
            return None
        return self._app.db.get(self._user_model, user_id)

    def is_authenticated(self) -> bool:
        """
        Return True if the current session has a logged-in user.

        Example::

            if app.auth.is_authenticated():
                app.text("You are logged in")
        """
        return self._get_user_id() is not None

    def has_role(self, role: str) -> bool:
        """
        Check whether the current user has the given role.

        Checks against the User model's role field.
        Supports comma-separated multi-role values (e.g. "admin,editor").

        Example::

            if app.auth.has_role("admin"):
                app.button("Admin Panel")
        """
        user = self.current_user()
        if user is None:
            return False
        user_role = getattr(user, self._role_field, None)
        if user_role is None:
            return False
        # Support comma-separated multi-role strings: "admin,editor"
        if isinstance(user_role, str):
            return role in [r.strip() for r in user_role.split(",")]
        if isinstance(user_role, (list, tuple, set)):
            return role in user_role
        return False

    # ─────────────────────────────────────────────────────────────────────
    # Public API: user management
    # ─────────────────────────────────────────────────────────────────────

    def create_user(self, username: str, password: str, **kwargs) -> T:
        """
        Create a new user. The password is automatically hashed with bcrypt.

        Parameters
        ----------
        username : str
            Login identifier.
        password : str
            Plaintext password (automatically hashed internally).
        **kwargs
            Additional model fields (e.g. email="...", role="admin").

        Example::

            app.auth.create_user("john", "secure1234", role="admin", email="john@co.com")
        """
        if self._app.db is None:
            raise RuntimeError("[violit.auth] app.db is not configured.")

        hashed = hash_password(password)
        user_data = {
            self._username_field: username,
            self._password_field: hashed,
            **kwargs,
        }
        user = self._user_model(**user_data)
        created = self._app.db.add(user)
        logger.info(f"[violit.auth] User created: {username}")
        return created

    def change_password(self, user: T, new_password: str) -> T:
        """
        Change a user's password.

        Example::

            app.auth.change_password(user, "new_secure_pw_123")
        """
        if self._app.db is None:
            raise RuntimeError("[violit.auth] app.db is not configured.")
        setattr(user, self._password_field, hash_password(new_password))
        return self._app.db.save(user)

    def delete_user(self, user: T) -> None:
        """
        Delete a user from the database.

        Example::

            app.auth.delete_user(target_user)
        """
        if self._app.db is None:
            raise RuntimeError("[violit.auth] app.db is not configured.")
        uid = getattr(user, "id", None)
        self._app.db.delete(user)
        logger.info(f"[violit.auth] User deleted: id={uid}")

    # ─────────────────────────────────────────────────────────────────────
    # Internal: page access control (Page.require_auth / require_role check)
    # ─────────────────────────────────────────────────────────────────────

    def check_page_access(self, page) -> bool:
        """
        Check whether the current user may access the given page.
        Called by PageRunner.page_builder.

        Returns:
            True  → access granted
            False → access denied (redirect has been performed)
        """
        # Determine whether authentication is required for this page
        needs_auth = getattr(page, "require_auth", False) or self._require_all
        required_role = getattr(page, "require_role", None)

        # The login page itself is never protected
        login_p = (
            self._app._navigation_pages_by_title.get(self._login_page)
            or self._app._navigation_pages_by_title.get(self._login_page.lower())
        )
        if login_p and page is login_p:
            return True

        if needs_auth and not self.is_authenticated():
            self._redirect_to_login()
            return False

        if required_role and not self.has_role(required_role):
            # Authenticated but insufficient role
            logger.warning(
                f"[violit.auth] Insufficient role: '{required_role}' required"
            )
            return False

        return True
