"""
Violit Background Task System

Allows long-running Python functions (e.g. ML training, data processing) to execute
in a background thread without blocking the UI. State changes made inside the
background function are automatically pushed to the originating user's session.

Usage:
    task = app.background(train_model, on_complete=lambda: app.toast("Done!"))
    app.button("Start", on_click=task.start)
    app.button("Cancel", on_click=task.cancel)
"""

import threading
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future
from typing import Any, Callable, Optional

from .context import session_ctx, view_ctx

logger = logging.getLogger(__name__)


class CancelledError(Exception):
    """Raised when a background task is cancelled via task.cancel()."""
    pass

# Shared executor pools (created once per type, reused across all BackgroundTask instances)
_executors = {}  # {"thread": ThreadPoolExecutor, "process": ProcessPoolExecutor}
_executor_lock = threading.Lock()


def _get_executor(executor_type: str = "thread", max_workers: int = 4):
    """Get or create a shared executor pool by type."""
    global _executors
    with _executor_lock:
        if executor_type == "thread":
            key = "thread"
            if key not in _executors or _executors[key]._shutdown:
                _executors[key] = ThreadPoolExecutor(
                    max_workers=max_workers,
                    thread_name_prefix="violit-bg",
                )
            return _executors[key]
        
        elif executor_type == "process":
            key = "process"
            if key not in _executors or _executors[key]._broken:
                _executors[key] = ProcessPoolExecutor(
                    max_workers=max_workers,
                )
            return _executors[key]
        
        elif executor_type == "celery":
            raise NotImplementedError(
                "Celery executor is planned for a future release. "
                "Use executor='thread' (default) or executor='process' for now."
            )
        
        else:
            raise ValueError(
                f"Unknown executor type: '{executor_type}'. "
                f"Supported: 'thread', 'process', 'celery' (future)."
            )


class BackgroundTask:
    """Handle returned by app.background() for controlling a background task.

    Properties:
        state      - Current state: 'idle' | 'running' | 'completed' | 'failed' | 'cancelled'
        is_running - True if state == 'running'

    Methods:
        start()    - Start the task (usually connected to on_click)
        cancel()   - Cancel/interrupt the task
    """

    def __init__(
        self,
        fn: Callable,
        app: Any,  # App instance (avoid circular import)
        on_complete: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
        singleton: bool = False,
        max_workers: int = 4,
        executor: str = "thread",
        flush_interval: float = 0.2,
    ):
        self._fn = fn
        self._app = app
        self._on_complete = on_complete
        self._on_error = on_error
        self._singleton = singleton
        self._max_workers = max_workers
        self._executor_type = executor
        self._flush_interval = max(0.01, float(flush_interval))
        self._state = "idle"
        self._future: Optional[Future] = None
        self._result: Any = None
        self._error: Optional[Exception] = None
        self._cancel_event = threading.Event()

    # Properties

    @property
    def state(self) -> str:
        return self._state

    @property
    def is_running(self) -> bool:
        return self._state == "running"

    @property
    def is_cancelled(self) -> bool:
        return self._cancel_event.is_set()

    @property
    def result(self) -> Any:
        """Return value of the background function (available after completion)."""
        return self._result

    @property
    def error(self) -> Optional[Exception]:
        """Exception from the background function (available after failure)."""
        return self._error

    # Control methods

    def start(self, *args):
        """Start the background task. Captures current session automatically.

        Designed to be passed directly to on_click:
            app.button("Start", on_click=task.start)
        """
        # Singleton guard
        if self._singleton and self._state == "running":
            logger.debug("[background] Singleton task already running, ignoring start()")
            return

        # Capture session ID from the calling context (on_click handler)
        sid = session_ctx.get()
        current_view_id = view_ctx.get()
        if sid is None:
            logger.warning("[background] No session context available. Task may not push updates correctly.")

        self._state = "running"
        self._result = None
        self._error = None
        self._cancel_event.clear()

        pool = _get_executor(self._executor_type, self._max_workers)
        self._future = pool.submit(self._run, sid, current_view_id)

    def cancel(self, *args):
        """Cancel the background task.

        Designed to be passed directly to on_click:
            app.button("Cancel", on_click=task.cancel)
        
        Note: Python threads cannot be forcefully killed. The background
        function should call task.check_cancelled() in its loop to
        cooperatively stop when cancelled.
        """
        if self._state == "running":
            self._cancel_event.set()
            self._state = "cancelled"
            logger.debug("[background] Task marked as cancelled")

    def check_cancelled(self):
        """Check if cancel was requested and raise CancelledError if so.
        
        Call this inside your background function's loop:
        
            def train():
                for epoch in range(100):
                    task.check_cancelled()  # Raises if cancelled
                    model.train()
                    progress.set(epoch / 100)
        """
        if self._cancel_event.is_set():
            raise CancelledError("Background task cancelled by user")

    # Internal helpers

    def _run(self, sid: str, current_view_id: str):
        """Execute the background function in a worker thread."""
        # Restore session context in the worker thread
        t = session_ctx.set(sid) if sid else None
        view_token = view_ctx.set(current_view_id) if current_view_id else None

        # Start periodic flusher: pushes dirty state updates every 200ms
        # so that progress.set() / status.set() are reflected in real-time
        stop_flusher = threading.Event()
        flusher = threading.Thread(
            target=self._periodic_flush,
            args=(sid, current_view_id, stop_flusher),
            daemon=True,
        )
        flusher.start()

        try:
            self._result = self._fn()

            # Skip completion if cancelled during execution
            if self._cancel_event.is_set():
                self._state = "cancelled"
                logger.debug("[background] Task cancelled during execution")
                self._push_dirty_to_session(sid, current_view_id)
                return

            self._state = "completed"
            logger.debug("[background] Task completed successfully")

            # Final flush to ensure last state changes are pushed
            self._push_dirty_to_session(sid, current_view_id)

            # on_complete callback
            if self._on_complete:
                self._on_complete()
                # on_complete may have triggered more state changes (e.g. toast)
                self._push_dirty_to_session(sid, current_view_id)

        except CancelledError:
            self._state = "cancelled"
            logger.debug("[background] Task cancelled via check_cancelled()")
            self._push_dirty_to_session(sid, current_view_id)

        except Exception as e:
            self._error = e
            self._state = "failed"
            logger.error(f"[background] Task failed: {e}")

            # on_error callback
            if self._on_error:
                try:
                    self._on_error(e)
                    self._push_dirty_to_session(sid, current_view_id)
                except Exception:
                    pass

        finally:
            stop_flusher.set()
            flusher.join(timeout=1)
            if view_token is not None:
                view_ctx.reset(view_token)
            if t is not None:
                session_ctx.reset(t)

    def _periodic_flush(self, sid: str, current_view_id: str, stop_event: threading.Event):
        """Periodically push dirty state updates to the client (runs in a helper thread)."""
        # Restore session context so _get_dirty_rendered works correctly
        t = session_ctx.set(sid) if sid else None
        view_token = view_ctx.set(current_view_id) if current_view_id else None
        try:
            while not stop_event.is_set():
                stop_event.wait(self._flush_interval)
                if not stop_event.is_set():
                    self._push_dirty_to_session(sid, current_view_id)
        finally:
            if view_token is not None:
                view_ctx.reset(view_token)
            if t is not None:
                session_ctx.reset(t)

    def _push_dirty_to_session(self, sid: str, current_view_id: str):
        """Push any dirty component updates to the specific user session."""
        if not sid or not current_view_id:
            return

        try:
            dirty = self._app._get_dirty_rendered()

            if self._app.ws_engine and self._app.ws_engine.has_socket(sid, current_view_id):
                if not dirty:
                    return

                main_loop = getattr(self._app, '_main_loop', None)
                if main_loop is not None and main_loop.is_running():
                    # Submit the coroutine to uvicorn's loop from this worker thread.
                    # run_coroutine_threadsafe is thread-safe and reuses the existing loop.
                    future = asyncio.run_coroutine_threadsafe(
                        self._app.ws_engine.push_updates(sid, dirty, view_id=current_view_id),
                        main_loop,
                    )
                    future.result(timeout=5)  # block until sent (or timeout)
                else:
                    # Fallback: main loop not captured yet (e.g. HTMX/lite mode)
                    loop = asyncio.new_event_loop()
                    try:
                        loop.run_until_complete(
                            self._app.ws_engine.push_updates(sid, dirty, view_id=current_view_id)
                        )
                    finally:
                        loop.close()

                logger.debug(f"[background] Pushed {len(dirty)} updates to session {sid[:8]}...")
                return

            if self._app.lite_engine:
                payload = self._app._build_lite_oob_payload(dirty)
                if not payload:
                    return
                self._app._enqueue_lite_stream_payload(sid, payload, view_id=current_view_id)
                logger.debug(f"[background] Enqueued lite stream payload for session {sid[:8]}...")
                return

            logger.debug(f"[background] Session {sid[:8]}... not connected, skipping push")

        except Exception as e:
            logger.debug(f"[background] Failed to push updates: {e}")
