from pathlib import Path
from typing import TYPE_CHECKING

from .context import layout_ctx

if TYPE_CHECKING:
    from .app import App


class FileWatcher:
    """Simple file watcher to detect changes (cross-platform)."""

    def __init__(self, watch_dir=None, debug_mode=False):
        self.watch_dir = Path(watch_dir).resolve() if watch_dir else Path(".").resolve()
        self.mtimes = {}
        self.initialized = False
        self.ignore_dirs = {'.git', '__pycache__', 'venv', '.venv', 'env', 'node_modules', '.idea', '.vscode'}
        self.debug_mode = debug_mode
        self.scan()

    def _is_ignored(self, path: Path):
        for part in path.parts:
            if part in self.ignore_dirs:
                return True
        return False

    def scan(self):
        """Scan watch directory for py files and their mtimes."""
        for path in self.watch_dir.rglob("*.py"):
            if self._is_ignored(path):
                continue
            try:
                abs_path = path.resolve()
                self.mtimes[abs_path] = abs_path.stat().st_mtime
            except OSError:
                pass

    def check(self):
        """Check if any file changed."""
        changed = False
        for path in list(self.watch_dir.rglob("*.py")):
            if self._is_ignored(path):
                continue
            try:
                abs_path = path.resolve()
                mtime = abs_path.stat().st_mtime

                if abs_path not in self.mtimes:
                    self.mtimes[abs_path] = mtime
                    if self.initialized:
                        if self.debug_mode:
                            print(f"\n[HOT RELOAD] New file detected: {path}", flush=True)
                        changed = True
                elif mtime > self.mtimes[abs_path]:
                    self.mtimes[abs_path] = mtime
                    if self.initialized:
                        if self.debug_mode:
                            print(f"\n[HOT RELOAD] File changed: {path}", flush=True)
                        changed = True
            except OSError:
                pass

        self.initialized = True
        return changed


class SidebarProxy:
    """Proxy for sidebar context."""

    def __init__(self, app):
        self.app = app

    def __enter__(self):
        self.token = layout_ctx.set("sidebar")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        layout_ctx.reset(self.token)

    def __getattr__(self, name):
        attr = getattr(self.app, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                token = layout_ctx.set("sidebar")
                try:
                    return attr(*args, **kwargs)
                finally:
                    layout_ctx.reset(token)

            return wrapper
        return attr


class Page:
    """Represents a page in multi-page app."""

    def __init__(
        self,
        entry_point,
        title=None,
        icon=None,
        url_path=None,
        require_auth: bool = False,
        require_role: str = None,
    ):
        self.entry_point = entry_point
        self.title = title or entry_point.__name__.replace("_", " ").title()
        self.icon = icon
        self.url_path = url_path or self.title.lower().replace(" ", "-")
        self.key = f"page_{self.url_path}"
        self.require_auth = require_auth
        self.require_role = require_role

    def run(self):
        self.entry_point()


class IntervalHandle:
    """Handle returned by app.interval() for controlling the timer."""

    def __init__(self, interval_id: str, app: 'App'):
        self._id = interval_id
        self._app = app

    def _get_interval_callbacks(self):
        from .state import get_session_store

        store = get_session_store()
        return store.setdefault('interval_callbacks', {})

    @property
    def state(self) -> str:
        info = self._get_interval_callbacks().get(self._id)
        return info['state'] if info else 'stopped'

    @property
    def is_running(self) -> bool:
        return self.state == 'running'

    def pause(self):
        """Pause the timer. Ticks stop until resume() is called."""
        info = self._get_interval_callbacks().get(self._id)
        if info and info['state'] == 'running':
            info['state'] = 'paused'
            self._app._send_interval_ctrl(self._id, 'pause')

    def resume(self):
        """Resume a paused timer."""
        info = self._get_interval_callbacks().get(self._id)
        if info and info['state'] == 'paused':
            info['state'] = 'running'
            self._app._send_interval_ctrl(self._id, 'resume')

    def stop(self):
        """Permanently stop the timer and unregister the callback."""
        interval_callbacks = self._get_interval_callbacks()
        if self._id in interval_callbacks:
            interval_callbacks[self._id]['state'] = 'stopped'
            self._app._send_interval_ctrl(self._id, 'stop')
            del interval_callbacks[self._id]


def print_terminal_splash():
    """Print a welcome banner and repository link to the terminal."""
    import sys

    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    splash = (
        "\033[95m\n"
        " ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        " ┃                                                             ┃\n"
        " ┃   V I O L I T   \u26a1  Pure Python Web Framework               ┃\n"
        " ┃                                                             ┃\n"
        " ┃   \U0001F31F Love Violit? Please support us with a star on GitHub!  ┃\n"
        " ┃   \U0001F449 https://github.com/violit-dev/violit                   ┃\n"
        " ┃                                                             ┃\n"
        " ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\033[0m\n"
    )
    print(splash)