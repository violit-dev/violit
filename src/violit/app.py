"""
Violit - A Streamlit-like framework with reactive components
Refactored with modular widget mixins
"""

import uuid
import sys
import argparse
import threading
import time
import json
import warnings
import secrets
import hmac
import hashlib
import logging
from typing import Any, Callable, Dict, List, Optional, Set, Union
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.gzip import GZipMiddleware
import inspect
import uvicorn
import os
import subprocess
from pathlib import Path

from .context import session_ctx, rendering_ctx, fragment_ctx, app_instance_ref, layout_ctx, page_ctx, action_ctx, initial_render_ctx
from .theme import Theme
from .component import Component
from .engine import LiteEngine, WsEngine
from .state import State, get_session_store, STATIC_STORE
from .broadcast import Broadcaster
from .background import BackgroundTask
import asyncio

REACTIVE_PARENT_PREFIXES = ('if_', 'for_', 'reactivity_', 'page_renderer')

# Import all widget mixins
from .widgets import (
    TextWidgetsMixin,
    InputWidgetsMixin,
    DataWidgetsMixin,
    ChartWidgetsMixin,
    MediaWidgetsMixin,
    LayoutWidgetsMixin,
    StatusWidgetsMixin,
    FormWidgetsMixin,
    ChatWidgetsMixin,
    CardWidgetsMixin,
    ListWidgetsMixin,
)

class FileWatcher:
    """Simple file watcher to detect changes (cross-platform)"""
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
        """Scan watch directory for py files and their mtimes"""
        for p in self.watch_dir.rglob("*.py"):
            if self._is_ignored(p): continue
            try:
                abs_p = p.resolve()
                self.mtimes[abs_p] = abs_p.stat().st_mtime
            except OSError:
                pass
                
    def check(self):
        """Check if any file changed"""
        # Re-scan to detect new files or modifications
        # Optimization: Scan is cheap for small projects, but we could optimize.
        # For now, simplistic scan is fine.
        changed = False
        for p in list(self.watch_dir.rglob("*.py")): 
            if self._is_ignored(p): continue
            try:
                abs_p = p.resolve()
                mtime = abs_p.stat().st_mtime
                
                if abs_p not in self.mtimes:
                    self.mtimes[abs_p] = mtime
                    # Only print if this isn't the first check (initialized)
                    # Use sys.stdout.write for immediate output
                    if self.initialized:
                         if self.debug_mode:
                             print(f"\n[HOT RELOAD] New file detected: {p}", flush=True)
                         changed = True
                elif mtime > self.mtimes[abs_p]:
                    self.mtimes[abs_p] = mtime
                    if self.initialized:
                        if self.debug_mode:
                            print(f"\n[HOT RELOAD] File changed: {p}", flush=True)
                        changed = True
            except OSError:
                pass
        
        self.initialized = True
        return changed


class SidebarProxy:
    """Proxy for sidebar context"""
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
    """Represents a page in multi-page app"""
    def __init__(self, entry_point, title=None, icon=None, url_path=None,
                 require_auth: bool = False, require_role: str = None):
        self.entry_point = entry_point
        self.title = title or entry_point.__name__.replace("_", " ").title()
        self.icon = icon
        self.url_path = url_path or self.title.lower().replace(" ", "-")
        self.key = f"page_{self.url_path}"
        self.require_auth = require_auth      # True이면 로그인 필요
        self.require_role = require_role      # "admin" 등 역할 지정 시 해당 역할 필요

    def run(self):
        self.entry_point()


class IntervalHandle:
    """Handle returned by app.interval() for controlling the timer.
    
    Methods:
        pause()   - Pause the timer (ticks stop firing)
        resume()  - Resume a paused timer
        stop()    - Permanently stop and unregister the timer
    
    Properties:
        state      - Current state: 'running' | 'paused' | 'stopped'
        is_running - True if state == 'running'
    """
    def __init__(self, interval_id: str, app: 'App'):
        self._id = interval_id
        self._app = app

    @property
    def state(self) -> str:
        info = self._app._interval_callbacks.get(self._id)
        return info['state'] if info else 'stopped'

    @property
    def is_running(self) -> bool:
        return self.state == 'running'

    def pause(self):
        """Pause the timer. Ticks stop until resume() is called."""
        info = self._app._interval_callbacks.get(self._id)
        if info and info['state'] == 'running':
            info['state'] = 'paused'
            self._app._send_interval_ctrl(self._id, 'pause')

    def resume(self):
        """Resume a paused timer."""
        info = self._app._interval_callbacks.get(self._id)
        if info and info['state'] == 'paused':
            info['state'] = 'running'
            self._app._send_interval_ctrl(self._id, 'resume')

    def stop(self):
        """Permanently stop the timer and unregister the callback."""
        if self._id in self._app._interval_callbacks:
            self._app._interval_callbacks[self._id]['state'] = 'stopped'
            self._app._send_interval_ctrl(self._id, 'stop')
            del self._app._interval_callbacks[self._id]


class App(
    TextWidgetsMixin,
    InputWidgetsMixin,
    DataWidgetsMixin,
    ChartWidgetsMixin,
    MediaWidgetsMixin,
    LayoutWidgetsMixin,
    StatusWidgetsMixin,
    FormWidgetsMixin,
    ChatWidgetsMixin,
    CardWidgetsMixin,
    ListWidgetsMixin,
):
    """Main Violit App class"""
    
    def __init__(self, mode='ws', title="Violit App", theme='violit_light_jewel', allow_selection=True, animation_mode='soft', icon=None, width=1024, height=768, on_top=False, container_width='800px', widget_gap='1rem', use_cdn=False, disconnect_timeout=0, db: str = None, migrate='auto'):
        self.mode = mode
        self.use_cdn = use_cdn
        self.disconnect_timeout = disconnect_timeout
        self.app_title = title  # Renamed to avoid conflict with title() method
        self.theme_manager = Theme(theme)

        # ── ORM / DB 초기화 ──────────────────────────────────────────────
        self.db = None
        if db is not None:
            from .db import ViolItDB, normalize_db_url
            self.db = ViolItDB(normalize_db_url(db), migrate=migrate)
        self._db_migrate_mode = migrate

        # ── Auth 초기화 ────────────────────────────────────────────────
        self.auth = None
        self.fastapi = FastAPI()
        self.fastapi.add_middleware(GZipMiddleware, minimum_size=1000)
        
        # Background preload: import heavy libraries after server starts
        # so they're cached in sys.modules before any widget needs them
        @self.fastapi.on_event("startup")
        async def _preload_heavy_libs():
            def _do():
                import pandas  # noqa: F401
                import plotly.graph_objects  # noqa: F401
            threading.Thread(target=_do, daemon=True).start()
        
        # Mount static files for offline support
        static_path = Path(__file__).parent / "static"
        if static_path.exists():
            self.fastapi.mount("/static", StaticFiles(directory=static_path), name="static")
        
        # Debug mode: Check for --debug flag
        self.debug_mode = '--debug' in sys.argv
        
        # Native mode security: Read from environment
        self.native_token = os.environ.get("VIOLIT_NATIVE_TOKEN")
        self.is_native_mode = bool(os.environ.get("VIOLIT_NATIVE_MODE"))
        
        # CSRF protection (disabled in native mode for local app security)
        self.csrf_enabled = not self.is_native_mode
        self.csrf_secret = secrets.token_urlsafe(32)
        
        if self.debug_mode:
            if self.is_native_mode and self.native_token:
                print(f"[SECURITY] Native mode detected - Token: {self.native_token[:20]}... - CSRF disabled")
            elif self.is_native_mode:
                print("[WARNING] Native mode flag set but no token found!")
        
        # Icon Setup
        self.app_icon = icon
        if self.app_icon is None:
            # Set default icon path
            base_path = os.path.dirname(os.path.abspath(__file__))
            default_icon = os.path.join(base_path, "assets", "violit_icon_sol.ico")
            if os.path.exists(default_icon):
                self.app_icon = default_icon

        self.width = width
        self.height = height
        self.on_top = on_top
        
        # Determine if splash should be shown by default. 
        # The run() method will set VIOLIT_NOSPLASH="1" if --nosplash is passed,
        # which will be safely inherited by Uvicorn worker child processes.
        self.show_splash = not bool(os.environ.get("VIOLIT_NOSPLASH", False))
        
        self._splash_html = f"""
        <style>
            @keyframes vl-splash-rotate {{
                to {{ transform: rotate(360deg); }}
            }}
        </style>
        <div id="splash" style="position:fixed;top:0;left:0;width:100%;height:100%;background:var(--vl-bg, #ffffff);z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden;transition:opacity 0.34s cubic-bezier(0.22, 1, 0.36, 1);">
            <div style="width:3.4rem;height:3.4rem;display:grid;place-items:center;flex:0 0 3.4rem;margin-bottom:0.95rem;">
                <svg aria-hidden="true" viewBox="0 0 64 64" width="52" height="52" style="display:block;animation:vl-splash-rotate 0.95s linear infinite;overflow:visible;">
                    <circle cx="32" cy="32" r="22" fill="none" stroke="color-mix(in srgb, var(--vl-primary, #7c3aed), white 84%)" stroke-width="2.5" opacity="0.38"></circle>
                    <circle cx="32" cy="32" r="22" fill="none" stroke="var(--vl-primary, #7c3aed)" stroke-width="3" stroke-linecap="round" stroke-dasharray="58 80"></circle>
                </svg>
            </div>
            <div style="min-height:1.5rem;line-height:1.5rem;font-size:1.2rem;font-weight:700;color:var(--vl-primary, #7c3aed);letter-spacing:-0.02em;text-align:center;white-space:nowrap;font-family:'Segoe UI',system-ui,-apple-system,BlinkMacSystemFont,sans-serif;">Loading...</div>
        </div>
        <script>
        (function() {{
            const splash = document.getElementById('splash');
            const splashMountedAt = performance.now();
            const minVisibleMs = 220;
            let domReady = document.readyState !== 'loading';
            let wsReady = ("{self.mode}" !== "ws");
            let resourcesReady = false;
            let resourcesStarted = false;
            let hidden = false;
            let hasServerRenderedContent = false;
            let rootRevealedAt = null;

            const detectInitialContent = () => {{
                const app = document.getElementById('app');
                const sidebar = document.getElementById('sidebar');
                const appHasContent = !!(app && (app.children.length > 0 || app.textContent.trim().length > 0));
                const sidebarHasContent = !!(sidebar && sidebar.style.display !== 'none' && (sidebar.children.length > 0 || sidebar.textContent.trim().length > 0));
                hasServerRenderedContent = appHasContent || sidebarHasContent;
            }};

            const waitForCriticalStyles = () => new Promise((resolve) => {{
                const links = Array.from(document.querySelectorAll('link[data-vl-critical="true"]')).filter((link) => !link.disabled);
                if (!links.length) {{
                    resolve();
                    return;
                }}

                let pending = 0;
                const markDone = () => {{
                    pending -= 1;
                    if (pending <= 0) resolve();
                }};

                links.forEach((link) => {{
                    let loaded = false;
                    try {{
                        loaded = !!link.sheet;
                    }} catch (err) {{
                        loaded = false;
                    }}

                    if (loaded) return;

                    pending += 1;
                    const finish = () => {{
                        link.removeEventListener('load', finish);
                        link.removeEventListener('error', finish);
                        markDone();
                    }};

                    link.addEventListener('load', finish, {{ once: true }});
                    link.addEventListener('error', finish, {{ once: true }});
                }});

                if (!pending) resolve();
            }});

            const waitForWebAwesomeComponents = () => {{
                const root = document.getElementById('root');
                const scope = root || document;
                const tags = [...new Set(
                    Array.from(scope.querySelectorAll('*'))
                        .map((el) => el.tagName.toLowerCase())
                        .filter((tag) => tag.startsWith('wa-') && !customElements.get(tag))
                )];

                const ready = tags.length
                    ? Promise.all(tags.map((tag) => customElements.whenDefined(tag)))
                    : Promise.resolve();

                return ready.then(() => new Promise((resolve) => {{
                    requestAnimationFrame(() => requestAnimationFrame(resolve));
                }}));
            }};

            const waitForTailwindRuntime = () => new Promise((resolve) => {{
                if (window.__vlTailwindReady) {{
                    resolve();
                    return;
                }}

                const finish = () => {{
                    window.removeEventListener('violit:tailwind-ready', finish);
                    resolve();
                }};

                window.addEventListener('violit:tailwind-ready', finish, {{ once: true }});
            }});

            const markResourcesReady = () => {{
                if (resourcesStarted) return;
                resourcesStarted = true;
                Promise.all([waitForCriticalStyles(), waitForWebAwesomeComponents(), waitForTailwindRuntime()]).then(() => {{
                    resourcesReady = true;
                    requestAnimationFrame(() => requestAnimationFrame(hideSplash));
                }});
            }};

            const revealRoot = () => {{
                const root = document.getElementById('root');
                if (!root) return;
                if (rootRevealedAt === null) rootRevealedAt = performance.now();
                root.style.visibility = 'visible';
                requestAnimationFrame(() => {{
                    root.style.opacity = '1';
                }});
            }};

            const unlockViewport = () => {{
                document.documentElement.classList.remove('vl-splash-active');
                document.body.classList.remove('vl-splash-active');
            }};

            const publishInitialRenderMetrics = () => {{
                const splashRemovedAt = performance.now();
                const metrics = {{
                    pageVisibleMs: rootRevealedAt === null ? splashRemovedAt : rootRevealedAt,
                    splashRemovedMs: splashRemovedAt,
                    splashMountedMs: splashMountedAt,
                    pageVisibleSeconds: Number((((rootRevealedAt === null ? splashRemovedAt : rootRevealedAt) / 1000)).toFixed(3)),
                    splashRemovedSeconds: Number((splashRemovedAt / 1000).toFixed(3)),
                    splashVisibleMs: Number((splashRemovedAt - splashMountedAt).toFixed(1)),
                }};
                window.__vlInitialRenderMetrics = metrics;
                window.dispatchEvent(new CustomEvent('violit:initial-render-ready', {{ detail: metrics }}));
            }};

            const finishSplash = () => {{
                unlockViewport();
                if (splash && splash.isConnected) splash.remove();
                publishInitialRenderMetrics();
            }};
            
            const hideSplash = () => {{
                if (hidden || !splash) return;
                if (!(domReady && resourcesReady && (wsReady || hasServerRenderedContent))) return;

                const elapsed = performance.now() - splashMountedAt;
                if (elapsed < minVisibleMs) {{
                    setTimeout(hideSplash, minVisibleMs - elapsed);
                    return;
                }}

                hidden = true;
                splash.style.opacity = '0';
                splash.style.pointerEvents = 'none';
                setTimeout(revealRoot, 90);
                splash.addEventListener('transitionend', finishSplash, {{ once: true }});
                setTimeout(finishSplash, 460);
            }};

            const markDomReady = () => {{
                domReady = true;
                detectInitialContent();
                markResourcesReady();
                requestAnimationFrame(hideSplash);
            }};

            if (domReady) {{
                markDomReady();
            }} else {{
                document.addEventListener('DOMContentLoaded', markDomReady, {{ once: true }});
            }}
            
            if ("{self.mode}" === "ws") {{
                const checkWS = setInterval(() => {{
                    if (window._wsReady) {{
                        wsReady = true;
                        clearInterval(checkWS);
                        hideSplash();
                    }}
                }}, 30);
            }}
            
            // Fail-safe: Maximum 1.5 seconds
            setTimeout(() => {{ 
                domReady = true; 
                resourcesReady = true;
                wsReady = true; 
                hideSplash(); 
            }}, 2500);
        }})();
        </script>
        """ if self.show_splash else ""

        # Container width: numeric (px), percentage (%), or 'none' (full width)
        if container_width == 'none' or container_width == '100%':
            self.container_max_width = 'none'
        elif isinstance(container_width, int):
            self.container_max_width = f'{container_width}px'
        else:
            self.container_max_width = container_width

        # Widget gap: controls spacing between widgets in page-container
        if isinstance(widget_gap, (int, float)):
            self.widget_gap = f'{widget_gap}rem'
        else:
            self.widget_gap = widget_gap

        self._sidebar_width = self._normalize_css_size('300px', fallback='300px')
        self._sidebar_min_width = self._normalize_css_size('220px', fallback='220px')
        self._sidebar_max_width = self._normalize_css_size('560px', fallback='560px')
        self._sidebar_resizable = False

        
        # Static definitions
        from .state import STATIC_STORE
        STATIC_STORE.clear() # Prevent leakage across hot reloads when forked on Linux
        self.static_builders: Dict[str, Callable] = {}
        self.static_order: List[str] = []
        self.static_sidebar_order: List[str] = []
        self.static_actions: Dict[str, Callable] = {}
        self.static_fragments: Dict[str, Callable] = {} # Deprecated. It was for the @app.fragments decorator.
        self.static_fragment_components: Dict[str, List[Any]] = {} # For children components of container widgets.
        
        self.state_count = 0
        self._fragments: Dict[str, Callable] = {} # Deprecated. It was used for dynamci fragment, but fragment_components in session store is used now.
        
        # Styling System: configure_widget defaults + user CSS
        self._widget_defaults: Dict[str, Dict[str, Any]] = {}
        self._user_css: List[str] = []
        
        # Broadcasting System
        self.broadcaster = Broadcaster(self)
        self._fragment_count = 0 # Used for  App.reactivity (with or decorator)
        
        # Interval System (app.interval API)
        self._interval_count = 0
        self._interval_callbacks: Dict[str, Dict] = {}

        # Navigation registry for programmatic page switching
        self._navigation_pages_by_key: Dict[str, Page] = {}
        self._navigation_pages_by_title: Dict[str, Page] = {}
        self._navigation_pages_by_path: Dict[str, Page] = {}
        self._navigation_pages_by_entry: Dict[Callable, Page] = {}
        self._navigation_states: List[State] = []
        
        # Internal theme/settings state
        self._theme_state = self.state(self.theme_manager.mode)
        self._selection_state = self.state(allow_selection)
        self._animation_state = self.state(animation_mode)
        
        self.ws_engine = WsEngine() if mode == 'ws' else None
        self.lite_engine = LiteEngine() if mode == 'lite' else None
        self._main_loop: asyncio.AbstractEventLoop | None = None
        app_instance_ref[0] = self
        
        # Register core fragments/updaters
        self._theme_updater()
        self._selection_updater()
        self._animation_updater()
        
        self._setup_routes()

    @property
    def sidebar(self):
        """Access sidebar context"""
        return SidebarProxy(self)

    @property
    def engine(self):
        """Get current engine (WS or Lite)"""
        return self.ws_engine if self.mode == 'ws' else self.lite_engine

    def _generate_csrf_token(self, session_id: str) -> str:
        """Generate CSRF token for session"""
        if not session_id:
            return ""
        message = f"{session_id}:{self.csrf_secret}"
        return hmac.new(
            self.csrf_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _verify_csrf_token(self, session_id: str, token: str) -> bool:
        """Verify CSRF token"""
        if not self.csrf_enabled:
            return True
        if not session_id or not token:
            return False
        expected = self._generate_csrf_token(session_id)
        return hmac.compare_digest(expected, token)

    def debug_print(self, *args, **kwargs):
        """Print only in debug mode"""
        if self.debug_mode:
            print(*args, **kwargs)

    def configure_widget(self, widget_type: str, cls: str = "", style: str = "", part_cls: Optional[Dict[str, str]] = None):
        """Set default cls/style/part_cls for a specific widget type.
        
        These defaults are merged with per-widget cls/style values.
        Per-widget values take higher priority (appended after defaults).
        
        Args:
            widget_type: Widget function name (e.g. "button", "card", "text_input")
            cls: Default Tailwind / utility classes
            style: Default inline CSS (e.g. CSS variables)
            part_cls: Default Tailwind classes for supported shadow DOM parts
            
        Example:
            app.configure_widget("button", cls="rounded-full shadow-md")
            app.configure_widget("card", cls="rounded-2xl shadow-lg")
        """
        self._widget_defaults[widget_type] = {'cls': cls, 'style': style, 'part_cls': part_cls or {}}

    def add_css(self, css: str):
        """Add custom CSS rules to the page.
        
        Use this to define custom classes, ::part() selectors for Web Awesome components,
        or any CSS that needs to be globally available.
        
        Args:
            css: Raw CSS string
            
        Example:
            app.add_css('''
                .cyan-btn { --vl-primary: cyan; }
                .glass { backdrop-filter: blur(16px); background: rgba(255,255,255,0.6); }
                #my-btn::part(base) { border-radius: 9999px; }
            ''')
        """
        self._user_css.append(css)

    def _normalize_css_size(self, value, fallback='300px') -> str:
        """Normalize numeric or string sizes to CSS-compatible values."""
        if value is None:
            return fallback
        if isinstance(value, (int, float)):
            return f"{value}px"
        size = str(value).strip()
        return size or fallback

    def configure_sidebar(self, width=None, min_width=None, max_width=None, resizable=None):
        """Configure sidebar sizing and optional desktop drag-resize behavior.

        Args:
            width: Default sidebar width. Numbers are treated as pixels.
            min_width: Minimum sidebar width when resized.
            max_width: Maximum sidebar width when resized.
            resizable: Enable desktop drag resizing.

        Example:
            app.configure_sidebar(width=340, min_width=240, max_width=640, resizable=True)
        """
        if width is not None:
            self._sidebar_width = self._normalize_css_size(width, fallback=self._sidebar_width)
        if min_width is not None:
            self._sidebar_min_width = self._normalize_css_size(min_width, fallback=self._sidebar_min_width)
        if max_width is not None:
            self._sidebar_max_width = self._normalize_css_size(max_width, fallback=self._sidebar_max_width)
        if resizable is not None:
            self._sidebar_resizable = bool(resizable)

    def _get_widget_defaults(self, widget_type: str) -> Dict[str, Any]:
        """Get default cls/style/part_cls for a widget type (internal helper)."""
        return self._widget_defaults.get(widget_type, {})

    def state(self, default_value, key=None) -> State:
        """Create a reactive state variable"""
        if key is None:
            # Streamlit-style: Generate stable key from caller's location
            frame = inspect.currentframe()
            try:
                caller_frame = frame.f_back
                filename = os.path.basename(caller_frame.f_code.co_filename)
                lineno = caller_frame.f_lineno
                # Create stable key: filename_linenumber
                name = f"state_{filename}_{lineno}"
            finally:
                del frame  # Avoid reference cycles
        else:
            name = key
        return State(name, default_value)

    def _get_next_cid(self, prefix: str) -> str:
        """Generate next component ID
        
        When inside a reactive block (If/For/reactivity), the block's ID is
        prefixed to prevent ID collisions with external components.
        """
        store = get_session_store()
        parent_ctx = rendering_ctx.get()
        count = store['component_count']
        is_reactive_parent = bool(parent_ctx and parent_ctx.startswith(REACTIVE_PARENT_PREFIXES))
        is_action = action_ctx.get(False)

        # Fast path for initial page render: the page is being built from scratch,
        # so phantom-widget prevention and action-specific ID rules are unnecessary.
        if initial_render_ctx.get(False) and not is_action:
            cid = f"{parent_ctx}_{prefix}_{count}" if is_reactive_parent else f"{prefix}_{count}"
            store['component_count'] = count + 1
            return cid

        temp_cid = f"{parent_ctx}_{prefix}_{count}" if is_reactive_parent else f"{prefix}_{count}"
        
        # In an action (e.g. on_click), if we are NOT in a render context,
        # we check for an existing component to prevent duplication.
        if is_action and parent_ctx is None:
            # We are in an action. If the component already exists, 
            # return its ID without incrementing count.
            if temp_cid in store['builders'] or temp_cid in self.static_builders:
                return temp_cid
            
            # [SIDELINE REDIRECTION]
            # When an action creates a widget (e.g. app.success() in an event handler),
            # it technically should NOT have a matching stable ID if it wasn't rendered
            # during the standard build. To keep the UI stable, we append a suffix
            # that marks it as an "orphaned/action-spawned" widget.
            # This allows it to increment the counter locally for that action session
            # without colliding with the next render's static IDs.
            cid = f"action_{prefix}_{count}"
            store['component_count'] = count + 1
            return cid

        # Check if we're inside a reactive block that needs namespacing
        if is_reactive_parent:
            # Namespace the ID under the reactive block
            cid = f"{parent_ctx}_{prefix}_{count}"
        else:
            cid = f"{prefix}_{count}"
        
        # [REACTIVE DRAG FIX]
        # Only increment count if we are NOT in an action.
        # This keeps IDs stable during rapid value changes (like dragging a slider).
        # We do NOT increment here even if rendering_ctx is active, because 
        # sub-renders (If/For) should rely on their own internal ID management
        # or reuse existing IDs from the store.
        if not is_action:
            store['component_count'] = count + 1
        return cid

    def _register_component(self, cid: str, builder: Callable, action: Optional[Callable] = None):
        """Register a component with builder and optional action"""
        store = get_session_store()
        sid = session_ctx.get()
        
        store['builders'][cid] = builder
        if action:
            store['actions'][cid] = action
            
        curr_frag = fragment_ctx.get()
        l_ctx = layout_ctx.get()

        if curr_frag:
            # Inside a fragment
            # IMPORTANT: Still respect sidebar context even inside fragments!
            if l_ctx == "sidebar":
                # Register to sidebar, not fragment
                if sid is None:
                    self.static_builders[cid] = builder
                    if action: self.static_actions[cid] = action
                    if cid not in self.static_sidebar_order:
                        self.static_sidebar_order.append(cid)
                else:
                    if action: store['actions'][cid] = action
                    store['sidebar_order'].append(cid)
            else:
                # Normal fragment component registration
                if sid is None:
                    # Static nesting (e.g. inside columns/expander at top level)
                    if curr_frag not in self.static_fragment_components:
                        self.static_fragment_components[curr_frag] = []
                    self.static_fragment_components[curr_frag].append((cid, builder))
                    # Store action and builder for components inside fragments
                    if action:
                        self.static_actions[cid] = action
                    self.static_builders[cid] = builder
                else:
                    # Dynamic Nesting (Runtime)
                    if curr_frag not in store['fragment_components']:
                        store['fragment_components'][curr_frag] = []
                    store['fragment_components'][curr_frag].append((cid, builder))
        else:
            if sid is None:
                # Static Root Registration
                self.static_builders[cid] = builder
                if action: self.static_actions[cid] = action
                
                if l_ctx == "sidebar":
                    if cid not in self.static_sidebar_order:
                        self.static_sidebar_order.append(cid)
                else:
                    if cid not in self.static_order:
                        self.static_order.append(cid)
            else:
                # Dynamic Root Registration
                if action: store['actions'][cid] = action
                current_order = store['sidebar_order'] if l_ctx == "sidebar" else store['order']
                is_initial = initial_render_ctx.get(False)
                is_action = action_ctx.get(False)

                # Fast path for initial page render: the session order has just been reset,
                # so duplicate/orphan checks are unnecessary.
                if is_initial and not is_action:
                    current_order.append(cid)
                    return
                
                if rendering_ctx.get() is None and is_action:
                    # Not in render context and in an action -> this is an orphaned widget 
                    # created in an action (e.g. app.success() in on_click).
                    # We should mark it as forced dirty so _get_dirty_rendered() picks it up,
                    # but we do NOT append it to the session order, which prevents it 
                    # from appearing at the bottom of the page in future renders.
                    if 'forced_dirty' not in store: store['forced_dirty'] = set()
                    store['forced_dirty'].add(cid)
                    
                    # [DUPLICATE PREVENTION] Ensure it is NOT in any order
                    if cid in current_order:
                        current_order.remove(cid)
                elif cid in current_order:
                    # Already registered in this session's root order
                    pass
                else:
                    if l_ctx == "sidebar":
                        store['sidebar_order'].append(cid)
                    else:
                        store['order'].append(cid)

    def simple_card(self, content_fn: Union[Callable, str, State]):
        """Display content in a simple card
        
        Accepts State object, callable, or string content
        """
        cid = self._get_next_cid("simple_card")
        def builder():
            token = rendering_ctx.set(cid)
            # Handle State object, callable, or direct value
            if isinstance(content_fn, State):
                val = content_fn.value
            elif callable(content_fn):
                val = content_fn()
            else:
                val = content_fn
            
            if val is None:
                val = "_No data_"
            
            rendering_ctx.reset(token)
            return Component("div", id=cid, content=str(val), class_="card")
        self._register_component(cid, builder)

    def fragment(self, func: Callable) -> Callable:
        """Create a reactive fragment (decorator)
        
        .. deprecated::
            This method is deprecated. Please use alternative patterns for managing reactive content.
        
        Always returns a wrapper that registers on call.
        Call the decorated function to register and render it.
        """
        warnings.warn(
            "@app.fragment is deprecated and will be removed in a future version. "
            "Please consider using alternative patterns.",
            DeprecationWarning,
            stacklevel=2
        )
        
        fid = f"fragment_{self._fragment_count}"
        self._fragment_count += 1
        
        # Track if already registered
        registered = [False]
        
        def fragment_builder():
            token = fragment_ctx.set(fid)
            render_token = rendering_ctx.set(fid)
            store = get_session_store()
            store['fragment_components'][fid] = []
            
            # Execute fragment logic
            func()
            
            # Render children
            htmls = []
            for cid, b in store['fragment_components'][fid]:
                htmls.append(b().render())
            
            fragment_ctx.reset(token)
            rendering_ctx.reset(render_token)
            
            inner = f'<div id="{fid}" class="fragment">{" ".join(htmls)}</div>'
            return Component("div", id=f"{fid}_wrapper", content=inner)
        
        # Store builder
        self.static_builders[fid] = fragment_builder
        self.static_fragments[fid] = func
        
        def wrapper():
            """Wrapper that registers fragment on first call"""
            if registered[0]:
                return
            registered[0] = True
            
            sid = session_ctx.get()
            if sid is None:
                # Static context: add to static_order
                if fid not in self.static_order:
                    self.static_order.append(fid)
            else:
                # Dynamic context: add to dynamic order
                self._register_component(fid, fragment_builder)
        
        return wrapper
    
    def reactivity(self, func: Optional[Callable] = None):
        """Create a reactive scope for complex control flow
        
        Can be used as:
        1. Decorator: @app.reactivity for function-wrapped reactive blocks
        2. Context Manager: with app.reactivity(): for inline reactive blocks (triggers page rerun)
        
        Example (Decorator - Partial Rerun):
            @app.reactivity
            def my_reactive_block():
                if count.value > 5:
                    app.success("Big!")
            my_reactive_block()
            
        Example (Context Manager - Page Rerun):
            with app.reactivity():
                if count.value > 5:
                    app.success("Big!")
        """
        if func is not None:
            # Decorator mode: wrap function as a reactive fragment
            # This enables PARTIAL RERUN of just this function
            fid = f"reactivity_{self._fragment_count}"
            self._fragment_count += 1
            
            # Track if already registered
            registered = [False]
            
            def fragment_builder():
                token = fragment_ctx.set(fid)
                render_token = rendering_ctx.set(fid)
                store = get_session_store()
                store['fragment_components'][fid] = []
                
                # [ID SYNC FIX] Reset component_count for this specific sub-render
                # This ensures widgets created inside a builder get the SAME IDs as before.
                prev_count = store['component_count']

                # Execute the user's function
                try:
                    func()
                finally:
                    # Restore global count after sub-render
                    store['component_count'] = prev_count
                
                # Render children
                htmls = []
                for cid, b in store['fragment_components'][fid]:
                    htmls.append(b().render())
                
                fragment_ctx.reset(token)
                rendering_ctx.reset(render_token)
                
                inner = f'<div id="{fid}" class="fragment">{" ".join(htmls)}</div>'
                return Component("div", id=f"{fid}_wrapper", content=inner)
            
            # Store builder
            self.static_builders[fid] = fragment_builder
            self.static_fragments[fid] = func
            
            def wrapper():
                """Wrapper that registers fragment on first call"""
                sid = session_ctx.get()
                if sid is None:
                    # Static context: register once
                    if registered[0]: return
                    registered[0] = True
                    if fid not in self.static_order:
                        self.static_order.append(fid)
                else:
                    # Dynamic context: Always register to add to current order
                    self._register_component(fid, fragment_builder)
            
            return wrapper
        
        # Context manager mode
        class ReactivityContext:
            def __init__(ctx_self, app):
                ctx_self.app = app
                ctx_self.fid = None
                ctx_self.fragment_token = None
                # DON'T create new rendering_ctx - keep parent's!
                
            def __enter__(ctx_self):
                # Create a temporary fragment scope for component collection
                ctx_self.fid = f"reactivity_{self._fragment_count}"
                self._fragment_count += 1
                
                # Set fragment context only (state access registers with parent)
                ctx_self.fragment_token = fragment_ctx.set(ctx_self.fid)
                
                # IMPORTANT: If inside a page, enable subscription to the page renderer
                # This allows if/for blocks inside with app.reactivity(): to trigger page re-runs
                p_ctx = page_ctx.get()
                ctx_self.rendering_token = None
                if p_ctx:
                     ctx_self.rendering_token = rendering_ctx.set(p_ctx)
                
                store = get_session_store()
                store['fragment_components'][ctx_self.fid] = []
                return ctx_self
                
            def __exit__(ctx_self, exc_type, exc_val, exc_tb):
                store = get_session_store()
                
                # Build the fragment
                def reactivity_builder():
                    htmls = []
                    for cid, b in store['fragment_components'][ctx_self.fid]:
                        htmls.append(b().render())
                    inner = f'<div id="{ctx_self.fid}" class="fragment">{" ".join(htmls)}</div>'
                    return Component("div", id=f"{ctx_self.fid}_wrapper", content=inner)
                
                fragment_ctx.reset(ctx_self.fragment_token)
                if ctx_self.rendering_token:
                    rendering_ctx.reset(ctx_self.rendering_token)
                
                # Register the reactivity scope as a component
                self._register_component(ctx_self.fid, reactivity_builder)
        
        return ReactivityContext(self)

    def If(self, condition, then_block=None, else_block=None, *, then=None, else_=None):
        """Reactive conditional rendering widget.
        
        Args:
            condition: Boolean or Callable[[], bool]. 
                       If callable (e.g. lambda: count.value > 5), it's re-evaluated on render.
            then_block: Function to call when True
            else_block: Function to call when False
        """
        # Resolve positional vs keyword
        actual_then = then_block if then_block is not None else then
        actual_else = else_block if else_block is not None else else_
        
        cid = self._get_next_cid("if")
        
        def if_builder():
            # Set rendering context for dependency tracking
            token = rendering_ctx.set(cid)
            store = get_session_store()
            
            # [ID SYNC FIX] Reset component_count for this specific sub-render
            # This ensures widgets created inside a builder get the SAME IDs as before.
            prev_count = store['component_count']

            try:
                # Evaluate condition dynamically
                current_cond = condition
                if callable(condition):
                    current_cond = condition()
                elif hasattr(condition, 'value'):
                    current_cond = condition.value
                
                if current_cond:
                    if actual_then:
                        prev_order = store['order'].copy()
                        store['order'] = []
                        
                        actual_then()
                        
                        htmls = []
                        for child_cid in store['order']:
                            builder = store['builders'].get(child_cid) or self.static_builders.get(child_cid)
                            if builder:
                                htmls.append(builder().render())
                        
                        store['order'] = prev_order
                        content = '\n'.join(htmls)
                        return Component("div", id=cid, content=content, class_="if-block if-then")
                else:
                    if actual_else:
                        prev_order = store['order'].copy()
                        store['order'] = []
                        
                        actual_else()
                        
                        htmls = []
                        for child_cid in store['order']:
                            builder = store['builders'].get(child_cid) or self.static_builders.get(child_cid)
                            if builder:
                                htmls.append(builder().render())
                        
                        store['order'] = prev_order
                        content = '\n'.join(htmls)
                        return Component("div", id=cid, content=content, class_="if-block if-else")
                
                return Component("div", id=cid, content="", class_="if-block if-empty")
            finally:
                # Restore global count after sub-render
                store['component_count'] = prev_count
                rendering_ctx.reset(token)
        
        self._register_component(cid, if_builder)

    def For(self, items, render_fn=None, empty_fn=None, *, render=None, empty=None):
        """Reactive loop rendering widget.
        
        Args:
            items: List, State, or Callable[[], List].
            render_fn: Function(item) or Function(item, index)
            empty_fn: Function when list is empty
        """
        # Resolve positional vs keyword
        actual_render = render_fn if render_fn is not None else render
        actual_empty = empty_fn if empty_fn is not None else empty

        # Check once at registration time whether render_fn accepts (item, index) or just (item).
        # Caching this avoids calling inspect.signature() on every item on every render.
        _render_with_index = False
        if actual_render is not None:
            try:
                sig = inspect.signature(actual_render)
                _render_with_index = len(sig.parameters) >= 2
            except (ValueError, TypeError):
                _render_with_index = False

        cid = self._get_next_cid("for")
        
        def for_builder():
            token = rendering_ctx.set(cid)
            store = get_session_store()
            
            # [ID SYNC FIX] Reset component_count for this specific sub-render
            # This ensures widgets created inside a builder get the SAME IDs as before.
            prev_count = store['component_count']

            try:
                # Evaluate items dynamically
                current_items = items
                if hasattr(items, 'value'): # State object
                    current_items = items.value
                elif callable(items):       # Lambda
                    current_items = items()
                
                # If current_items is an integer, convert to range
                # This allows: app.For(count, render=...) where count is an int State
                if isinstance(current_items, int):
                    current_items = range(max(0, current_items))
                
                # Check if empty
                if not current_items or len(current_items) == 0:
                    if actual_empty:
                        prev_order = store['order'].copy()
                        store['order'] = []
                        
                        actual_empty()
                        
                        htmls = []
                        for child_cid in store['order']:
                            builder = store['builders'].get(child_cid) or self.static_builders.get(child_cid)
                            if builder:
                                htmls.append(builder().render())
                        
                        store['order'] = prev_order
                        content = '\n'.join(htmls)
                        return Component("div", id=cid, content=content, class_="for-block for-empty")
                    else:
                        return Component("div", id=cid, content="", class_="for-block for-empty")
                
                # Render each item
                if actual_render:
                    all_htmls = []
                    
                    for idx, item in enumerate(current_items):
                        prev_order = store['order'].copy()
                        store['order'] = []
                        
                        # Use the signature check cached at For() registration time
                        if _render_with_index:
                            actual_render(item, idx)
                        else:
                            actual_render(item)
                        
                        for child_cid in store['order']:
                            builder = store['builders'].get(child_cid) or self.static_builders.get(child_cid)
                            if builder:
                                all_htmls.append(builder().render())
                        
                        store['order'] = prev_order
                    
                    content = '\n'.join(all_htmls)
                    return Component("div", id=cid, content=content, class_="for-block")
                
                return Component("div", id=cid, content="", class_="for-block")
            finally:
                # Restore global count after sub-render
                store['component_count'] = prev_count
                rendering_ctx.reset(token)
        
        self._register_component(cid, for_builder)

    def _render_all(self):
        """Render all components"""
        store = get_session_store()
        
        main_html = []
        sidebar_html = []

        def render_cids(cids, target_list):
            for cid in cids:
                builder = store['builders'].get(cid) or self.static_builders.get(cid)
                if builder:
                    try:
                        target_list.append(builder().render())
                    except Exception as e:
                        import logging
                        logging.getLogger(__name__).error(
                            f"[render] component '{cid}' failed: {e}"
                        )
                        target_list.append(
                            f'<div id="{cid}" style="border:1px solid var(--vl-danger,red);'
                            f'padding:0.75rem;border-radius:0.375rem;color:var(--vl-danger,red);'
                            f'font-size:0.85rem;">'
                            f'[Render error] <code>{cid}</code>: {e}'
                            f'</div>'
                        )

        # Static Components
        render_cids(self.static_order, main_html)
        render_cids(self.static_sidebar_order, sidebar_html)
        
        # Dynamic Components
        render_cids(store['order'], main_html)
        render_cids(store['sidebar_order'], sidebar_html)
        
        return "".join(main_html), "".join(sidebar_html)

    def _get_dirty_rendered(self):
        """Get components that need updating"""
        store = get_session_store()
        tracker = store['tracker']
        dirty_states = store.get('dirty_states', set())
        aff = set()
        for s in dirty_states: aff.update(tracker.get_dirty_components(s))
        
        # [NEW] Handle forced dirty components (async data loading)
        forced = store.get('forced_dirty', set())
        if forced:
            aff.update(forced)
            store['forced_dirty'] = set() # Clear after collection
            
        store['dirty_states'] = set()
        
        res = []
        for cid in aff:
            builder = store['builders'].get(cid) or self.static_builders.get(cid)
            if builder:
                # Clear stale subscriptions before re-rendering so that:
                # 1. Dependencies that are no longer read get removed.
                # 2. The upcoming builder() call re-registers only current deps.
                tracker.unregister_component(cid)
                
                # [FIX PHANTOM WIDGETS] Use a token to ensure widgets created 
                # inside a DIRTY re-render are correctly registered.
                # This ensures they are kids of the dirty component, not root level phantoms.
                token = rendering_ctx.set(cid)
                
                # [ID SYNC FIX] Reset component_count for this specific sub-render
                # This ensures widgets created inside a builder get the SAME IDs as before.
                prev_count = store['component_count']
                
                try:
                    res.append(builder())
                except Exception as e:
                    import logging
                    logging.getLogger(__name__).error(
                        f"[render] dirty component '{cid}' failed: {e}"
                    )
                    from .component import Component
                    res.append(Component(
                        "div", id=cid,
                        content=(
                            f'<span style="color:var(--vl-danger,red);font-size:0.85rem;">'
                            f'[Render error] <code>{cid}</code>: {e}</span>'
                        )
                    ))
                finally:
                    rendering_ctx.reset(token)
                    # Restore global count after sub-render
                    store['component_count'] = prev_count
            else:
                # Component is permanently gone (e.g. navigation page switch,
                # If-block condition flip).  Clean it from the tracker so it
                # never appears in future dirty sets.
                tracker.unregister_component(cid)
        return res

    # Theme and settings methods
    def set_theme(self, p):
        """Set theme preset"""
        import time
        store = get_session_store()
        store['theme'].set_preset(p)
        if self._theme_state: 
            # Use timestamp to force dirty even if same theme selected twice
            self._theme_state.set(f"{p}_{time.time()}")

    def set_selection_mode(self, enabled: bool):
        """Enable/disable text selection"""
        if self._selection_state:
            self._selection_state.set(enabled)

    def set_animation_mode(self, mode: str):
        """Set animation mode ('soft' or 'hard')"""
        if self._animation_state:
            self._animation_state.set(mode)

    def set_primary_color(self, c):
        """Set primary theme color"""
        store = get_session_store()
        store['theme'].set_color('primary', c)
        if self._theme_state: 
            self._theme_state.set(str(time.time()))

    def _selection_updater(self):
        """Update selection mode"""
        cid = "__selection_updater__"
        def builder():
            token = rendering_ctx.set(cid)
            enabled = self._selection_state.value
            rendering_ctx.reset(token)
            
            action = "remove" if enabled else "add"
            script = f"<script>document.body.classList.{action}('no-select');</script>"
            return Component("div", id=cid, style="display:none", content=script)
        self._register_component(cid, builder)

    def _patch_webview_icon(self):
        """Monkey-patch pywebview's WinForms BrowserForm to use custom icon"""
        if os.name != 'nt' or not self.app_icon:
            return
            
        try:
            from webview.platforms import winforms
            
            # Store reference to icon path for closure
            icon_path = self.app_icon
            
            # Check if already patched
            if hasattr(winforms.BrowserView.BrowserForm, '_violit_patched'):
                return
                
            # Get original __init__
            original_init = winforms.BrowserView.BrowserForm.__init__
            
            def patched_init(self, window, cache_dir):
                """Patched __init__ that sets custom icon after original init"""
                original_init(self, window, cache_dir)
                
                try:
                    from System.Drawing import Icon as DotNetIcon
                    if os.path.exists(icon_path):
                        self.Icon = DotNetIcon(icon_path)
                except Exception:
                    pass  # Silently fail if icon can't be set
            
            # Apply patch
            winforms.BrowserView.BrowserForm.__init__ = patched_init
            winforms.BrowserView.BrowserForm._violit_patched = True
            
        except Exception:
            pass  # If patching fails, continue without custom icon

    def _animation_updater(self):
        """Update animation mode"""
        cid = "__animation_updater__"
        def builder():
            token = rendering_ctx.set(cid)
            mode = self._animation_state.value
            rendering_ctx.reset(token)
            
            script = f"<script>document.body.classList.remove('anim-soft', 'anim-hard'); document.body.classList.add('anim-{mode}');</script>"
            return Component("div", id=cid, style="display:none", content=script)
        self._register_component(cid, builder)

    def _theme_updater(self):
        """Update theme"""
        cid = "__theme_updater__"
        def builder():
            token = rendering_ctx.set(cid)
            _ = self._theme_state.value 
            rendering_ctx.reset(token)
            
            store = get_session_store()
            t = store['theme']
            vars_str = t.to_css_vars()
            cls = t.theme_class
            
            script_content = f'''
                <script>
                    (function() {{
                        document.documentElement.className = '{cls}';
                        const root = document.documentElement;
                        const vars = `{vars_str}`.split('\\n');
                        vars.forEach(v => {{
                            const parts = v.split(':');
                            if(parts.length === 2) {{
                                const key = parts[0].trim();
                                const val = parts[1].replace(';', '').trim();
                                root.style.setProperty(key, val);
                            }}
                        }});
                        
                        // Update Extra CSS
                        let extraStyle = document.getElementById('theme-extra');
                        if (!extraStyle) {{
                            extraStyle = document.createElement('style');
                            extraStyle.id = 'theme-extra';
                            document.head.appendChild(extraStyle);
                        }}
                        extraStyle.textContent = `{t.extra_css}`;
                    }})();

                    // Theme Extra JS (cleanup previous, then apply new)
                    if (window._vlThemeCleanup) {{ window._vlThemeCleanup(); window._vlThemeCleanup = null; }}
                    {t.extra_js}
                </script>
            '''
            return Component("div", id=cid, style="display:none", content=script_content)
        self._register_component(cid, builder)

    # Interval API

    def interval(
        self,
        callback: Callable,
        ms: int = 1000,
        condition: Optional[Callable[[], bool]] = None,
        autostart: bool = True,
    ) -> IntervalHandle:
        """Register a periodic timer that calls a Python callback.
        
        Uses client-side setInterval to send lightweight 'tick' messages
        over WebSocket. No DOM manipulation, no hidden buttons.
        
        Args:
            callback:   Function to call on each tick
            ms:         Interval in milliseconds (default: 1000)
            condition:  Optional callable returning bool.
                        If provided, callback only fires when condition() is True.
                        Useful with State: condition=lambda: pump_on.value
            autostart:  If True (default), timer starts immediately.
                        If False, call handle.resume() to start.
        
        Returns:
            IntervalHandle with pause() / resume() / stop() / state
        
        Example:
            timer = app.interval(update_data, ms=500)
            app.button("Pause", on_click=timer.pause)
            app.button("Resume", on_click=timer.resume)
            
            # Conditional:
            app.interval(poll, ms=1000, condition=lambda: is_active.value)
        """
        interval_id = f"__vl_interval_{self._interval_count}__"
        self._interval_count += 1

        initial_state = 'running' if autostart else 'paused'

        self._interval_callbacks[interval_id] = {
            'callback':  callback,
            'ms':        ms,
            'condition': condition,
            'state':     initial_state,
        }

        # Inject minimal JS to create the client-side interval.
        # _vlCreateInterval is defined in the HTML template's script block.
        autostart_js = 'true' if autostart else 'false'
        js_code = (
            f"(function(){{"
            f"function _init(){{"
            f"if(typeof window._vlCreateInterval==='function'){{"
            f"window._vlCreateInterval('{interval_id}',{ms},{autostart_js});"
            f"}}else{{setTimeout(_init,100);}}}}"
            f"_init();}})();"
        )

        # [FIX] When called inside a button click handler (action_ctx=True),
        # self.html() creates a new DOM element that doesn't exist on the client,
        # so the script is silently dropped. Instead, use eval_queue to send
        # the JS directly to the client as an 'eval' message.
        if action_ctx.get(False):
            store = get_session_store()
            if store is not None:
                if 'eval_queue' not in store:
                    store['eval_queue'] = []
                store['eval_queue'].append(js_code)
        else:
            self.html(f"<script>{js_code}</script>")

        return IntervalHandle(interval_id, self)

    def _send_interval_ctrl(self, interval_id: str, action: str):
        """Send interval control message (pause/resume/stop) to all connected clients."""
        if not self.ws_engine:
            return

        async def _push():
            for sid, ws_sock in list(self.ws_engine.sockets.items()):
                try:
                    await ws_sock.send_json({
                        'type': 'interval_ctrl',
                        'id':   interval_id,
                        'action': action,
                    })
                except Exception:
                    pass

        def _run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_push())
            loop.close()

        threading.Thread(target=_run, daemon=True).start()

    # End Interval API

    # Background Task API

    def background(
        self,
        fn: Callable,
        on_complete: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
        singleton: bool = False,
        max_workers: int = 4,
        executor: str = "thread",
    ) -> 'BackgroundTask':
        """Run a long-running function in the background without blocking the UI.
        
        The function executes in a worker thread. State changes inside the
        function are automatically pushed to the user who started the task.
        Other users and UI interactions are unaffected.
        
        Args:
            fn:          Function to run in the background
            on_complete: Optional callback when the task finishes successfully
            on_error:    Optional callback(exception) when the task fails
            singleton:   If True, prevents starting a second instance while running
            max_workers: Max concurrent background tasks (shared pool, default: 4)
            executor:    'thread' (default) or 'process' (for CPU-heavy, future)
        
        Returns:
            BackgroundTask handle with start() / cancel() / state / is_running
        
        Example:
            progress = app.state(0)
            
            def train():
                for i in range(100):
                    model.train_one_epoch()
                    progress.set(i / 100)
            
            task = app.background(
                train,
                on_complete=lambda: app.toast('Training complete!', 'success'),
                on_error=lambda e: app.toast(f'Error: {e}', 'danger'),
            )
            app.button('Start Training', on_click=task.start)
            app.button('Cancel', on_click=task.cancel)
            app.progress_bar(progress)
        """
        return BackgroundTask(
            fn=fn,
            app=self,
            on_complete=on_complete,
            on_error=on_error,
            singleton=singleton,
            max_workers=max_workers,
            executor=executor,
        )

    # End Background Task API

    def setup_auth(
        self,
        user_model,
        username_field: str = "username",
        password_field: str = "hashed_password",
        role_field: str = "role",
        login_page: str = "로그인",
        require_auth: bool = False,
    ):
        """
        Auth 시스템 초기화.

        Parameters
        ----------
        user_model : SQLModel 클래스
            User 모델.
        username_field : str
            아이디 콼럼 이름 (기본값: 'username').
        password_field : str
            해시 비밀번호 콼럼 이름 (기본값: 'hashed_password').
        role_field : str
            역할 콼럼 이름 (기본값: 'role').
        login_page : str
            미인증 접근 시 이동할 페이지 제목 (기본값: '로그인').
        require_auth : bool
            True 이면 모든 페이지를 자동 보호.

        Example::

            app.setup_auth(User)
            app.setup_auth(User, login_page="Login", require_auth=True)
        """
        from .auth import ViolItAuth
        self.auth = ViolItAuth(
            app=self,
            user_model=user_model,
            username_field=username_field,
            password_field=password_field,
            role_field=role_field,
            login_page=login_page,
            require_auth=require_auth,
        )

    def navigation(self, pages: List[Any], position="sidebar", align="center", auto_run=True, reactivity_mode=False):
        """Create multi-page navigation
        
        Args:
            pages: List of Page objects or functions
            position: 'sidebar' or 'top' (default: sidebar)
            align: 'left', 'center', or 'right' (default: left)
            auto_run: Run logic immediately (default: True)
            reactivity_mode: If True, treats each page as a reactive scope (auto pre-evaluates).
                             This allows standard 'if' statements to be reactive.
        """
        # Normalize pages
        final_pages = []
        for p in pages:
            if isinstance(p, Page): final_pages.append(p)
            elif callable(p): final_pages.append(Page(p))
        
        if not final_pages: return None
        
        # Navigation Menu Builder
        cid = self._get_next_cid("nav_menu")

        # Per-instance state key derived from cid; allows multiple navigation()
        # instances (e.g. sidebar + top tabs) to coexist without sharing state.
        current_page_key_state = self.state(final_pages[0].key, key=f"__nav_selection_{cid}__")
        for p in final_pages:
            self._navigation_pages_by_key[p.key] = p
            self._navigation_pages_by_title[p.title] = p
            self._navigation_pages_by_title[p.title.lower()] = p
            self._navigation_pages_by_path[p.url_path] = p
            self._navigation_pages_by_entry[p.entry_point] = p
        self._navigation_states.append(current_page_key_state)
        nav_cid = cid  # Capture for use in nav_action closure
        def nav_builder():
            token = rendering_ctx.set(cid)
            curr = current_page_key_state.value
            
            items = []
            if align == "left":
                items.append(f"<style>#{cid} wa-button::part(base) {{ justify-content: flex-start; }}</style>")
            elif align == "right":
                items.append(f"<style>#{cid} wa-button::part(base) {{ justify-content: flex-end; }}</style>")

            for p in final_pages:
                is_active = p.key == curr
                page_hash = p.key.replace("page_", "")
                if self.mode == 'lite':
                    # Lite mode: scroll-save + hash + HTMX post
                    onclick_prefix = (
                        f'if(window._currentPageKey){{window._pageScrollPositions=window._pageScrollPositions||{{}};window._pageScrollPositions[window._currentPageKey]=window.scrollY;}}'
                        f"window._currentPageKey='{p.key}';"
                        f"window.location.hash='{page_hash}';"
                    )
                    click_attr = (
                        f'onclick="{onclick_prefix}'
                        f"setTimeout(function(){{window.scrollTo(0,window._pageScrollPositions&&window._pageScrollPositions['{p.key}']||0);}},100);"
                        f'" hx-post="/action/{cid}" hx-vals=\'{{"value": "{p.key}"}}\' hx-target="#{cid}" hx-swap="outerHTML"'
                    )
                else:
                    # WebSocket mode: simple direct sendAction – it already handles scroll save and hash update
                    click_attr = f"""onclick="window.sendAction('{cid}','{p.key}')" """
                
                # Styling for active/inactive nav items
                if is_active:
                    style = "width: 100%; justify-content: start;"
                    variant = "brand"
                    appearance = "accent"
                else:
                    style = "width: 100%; justify-content: start;"
                    variant = "neutral"
                    appearance = "plain"
                
                icon_html = f'<wa-icon name="{p.icon}" slot="start" style="pointer-events: none;"></wa-icon>' if p.icon else ""
                with_start_attr = "with-start" if icon_html else ""
                items.append(f'<wa-button data-page-key="{p.key}" data-nav-active="{"true" if is_active else "false"}" style="{style}" variant="{variant}" appearance="{appearance}" {with_start_attr} {click_attr}>{icon_html}<span style="pointer-events: none;">{p.title}</span></wa-button>')
            
            rendering_ctx.reset(token)
            return Component("div", id=cid, content="\n".join(items), class_="nav-container")
            
        def nav_action(key):
            current_page_key_state.set(key)

        # Register Nav Component
        if position == "sidebar":
            token = layout_ctx.set("sidebar")
            try:
                self._register_component(cid, nav_builder, action=nav_action)
            finally:
                layout_ctx.reset(token)
        else:
            self._register_component(cid, nav_builder, action=nav_action)

        # Return the runner wrapper
        current_key = current_page_key_state.value
        
        class PageRunner:
            def __init__(self, app, page_state, pages_map, reactivity_mode):
                self.app = app
                self.state = page_state
                self.pages_map = pages_map
                self.reactivity_mode = reactivity_mode
            
            def run(self):
                # Progressive Mode: Register page renderer as a regular component
                # Navigation state changes trigger page re-render.
                # If reactivity_mode=True, we subscribe to state changes inside page function too.
                cid = self.app._get_next_cid("page_renderer")
                
                def page_builder():
                    # Set context ONLY for reading navigation state.
                    # When page_builder is called from _get_dirty_rendered(), the outer render
                    # path may already have rendering_ctx=cid. In non-reactive mode we must
                    # still execute the page body with rendering_ctx cleared, otherwise child
                    # widgets get namespaced as page_renderer_X_btn_Y after navigation.
                    token = rendering_ctx.set(cid)
                    
                     # Store Current Page Renderer CID for Reactivity Blocks
                    p_token = page_ctx.set(cid)

                    try:
                        key = self.state.value  # Subscribe to navigation state
                        
                        # Execute the current page function
                        p = self.pages_map.get(key)
                        if p:
                            # ── Auth 접근 권한 확인 ───────────────────────
                            if self.app.auth is not None:
                                if not self.app.auth.check_page_access(p):
                                    # 미인증 / 권한 부족: 빈 컨테이너 반환
                                    return Component("div", id=cid, content="", class_="page-container")

                            # Collect components from the page
                            store = get_session_store()
                            # Clear previous dynamic order for this page render
                            previous_order = store['order'].copy()
                            previous_fragments = {k: v.copy() for k, v in store['fragment_components'].items()}
                            
                            # [ID NAVIGATION SYNC]
                            # When switching pages or re-rendering a page, we must 
                            # ensure the component_count starts AFTER the static layout 
                            # (sidebar/top nav) to keep IDs stable for interactive widgets.
                            store['component_count'] = STATIC_STORE.get('component_count', 0)
                            
                            store['order'] = []
                            store['fragment_components'] = {}  # Clear fragments to prevent duplicates
                            
                            try:
                                # Start executing page function
                                # If reactivity_mode is False, reset context (default, non-reactive page script)
                                # If reactivity_mode is True, KEEP context (page script registers dependencies on page_renderer)
                                page_body_token = None
                                if not self.reactivity_mode:
                                    page_body_token = rendering_ctx.set(None)
                                
                                p.entry_point()
                                
                                # Re-enable rendering_ctx if it was reset
                                if not self.reactivity_mode and page_body_token is not None:
                                    rendering_ctx.reset(page_body_token)
                                
                                htmls = []
                                for page_cid in store['order']:
                                    builder = store['builders'].get(page_cid) or self.app.static_builders.get(page_cid)
                                    if builder:
                                        htmls.append(builder().render())
                                
                                content = '\n'.join(htmls)
                                return Component("div", id=cid, content=content, class_="page-container")
                            finally:
                                # Restore previous state (always, even on exception)
                                store['order'] = previous_order
                                store['fragment_components'] = previous_fragments
                        
                        return Component("div", id=cid, content="", class_="page-container")
                    finally:
                         # Ensure context is reset
                        if rendering_ctx.get() == cid:
                             rendering_ctx.reset(token)
                        page_ctx.reset(p_token)
                
                # Register the page renderer as a regular component
                self.app._register_component(cid, page_builder)


        page_runner = PageRunner(self, current_page_key_state, {p.key: p for p in final_pages}, reactivity_mode)
        
        # Auto-run if enabled
        if auto_run:
            page_runner.run()
        
        return page_runner

    # --- Routes ---
    def _setup_routes(self):
        """Setup FastAPI routes"""
        @self.fastapi.middleware("http")
        async def mw(request: Request, call_next):
            # Native mode security: Block web browser access
            if self.native_token is not None:
                token_from_request = request.query_params.get("_native_token")
                token_from_cookie = request.cookies.get("_native_token")
                user_agent = request.headers.get("user-agent", "")
                
                # Debug logging for security check
                self.debug_print(f"[NATIVE SECURITY CHECK]")
                self.debug_print(f"  Token from request: {token_from_request[:20] if token_from_request else None}...")
                self.debug_print(f"  Token from cookie: {token_from_cookie[:20] if token_from_cookie else None}...")
                self.debug_print(f"  Expected token: {self.native_token[:20]}...")
                self.debug_print(f"  User-Agent: {user_agent}")
                
                # Verify token
                is_valid_token = (token_from_request == self.native_token or token_from_cookie == self.native_token)
                
                # Block if token is invalid
                if not is_valid_token:
                    from fastapi.responses import HTMLResponse
                    self.debug_print(f"  [X] ACCESS DENIED - Invalid or missing token")
                    return HTMLResponse(
                        content="""
                        <html>
                        <head><title>Access Denied</title></head>
                        <body style="font-family: system-ui; padding: 2rem; text-align: center;">
                            <h1>[LOCK] Access Denied</h1>
                            <p>This application is running in <strong>native desktop mode</strong>.</p>
                            <p>Web browser access is disabled for security reasons.</p>
                            <hr style="margin: 2rem auto; width: 50%;">
                            <small>If you are the owner, please use the desktop application.</small>
                        </body>
                        </html>
                        """,
                        status_code=403
                    )
                else:
                    self.debug_print(f"  [OK] ACCESS GRANTED - Valid token")
            
            # Session ID: get from cookie (all tabs share same session)
            sid = request.cookies.get("ss_sid") or str(uuid.uuid4())
            
            t = session_ctx.set(sid)
            response = await call_next(request)
            session_ctx.reset(t)
            
            # Set cookie
            is_https = request.url.scheme == "https"
            response.set_cookie(
                "ss_sid", 
                sid, 
                httponly=True,
                secure=is_https,
                samesite="lax"
            )
            
            # Set native token cookie
            if self.native_token and not request.cookies.get("_native_token"):
                response.set_cookie(
                    "_native_token", 
                    self.native_token, 
                    httponly=True,
                    secure=is_https,
                    samesite="strict"
                )
            
            return response

        @self.fastapi.get("/")
        async def index(request: Request):
            # [RESET SESSION STATE] 
            # When the user refreshes the page via GET /, we clear their session builders/order
            # to prevent duplicate registrations and "Phantom Widgets" from previous runs.
            # This is essential for maintaining a clean page on every reload.
            store = get_session_store()
            builders = store.get('builders')
            if builders:
                builders.clear()
            order = store.get('order')
            if order:
                order.clear()
            sidebar_order = store.get('sidebar_order')
            if sidebar_order:
                sidebar_order.clear()
            fragment_components = store.get('fragment_components')
            if fragment_components:
                fragment_components.clear()
            base_component_count = STATIC_STORE.get('component_count', 0)
            if store.get('component_count') != base_component_count:
                store['component_count'] = base_component_count
            
            # Note: _theme_state, _selection_state, _animation_state and their updaters
            # are already initialized in __init__, no need to re-initialize here
            
            # [CRITICAL] Set initial_render_ctx to True during first page load
            # This allows widgets (like charts) to defer heavy data serialization
            token = initial_render_ctx.set(True)
            try:
                main_c, sidebar_c = self._render_all()
            finally:
                initial_render_ctx.reset(token)
                
            store = get_session_store()
            t = store['theme']
            
            sidebar_style = "" if (sidebar_c or self.static_sidebar_order) else "display: none;"
            main_class = "" if (sidebar_c or self.static_sidebar_order) else "sidebar-collapsed"
            
            # Generate CSRF token
            # Get sid from context (set by middleware) instead of cookies (not set yet on first visit)
            try:
                sid = session_ctx.get()
            except LookupError:
                sid = request.cookies.get("ss_sid")
            
            csrf_token = self._generate_csrf_token(sid) if sid and self.csrf_enabled else ""
            csrf_script = f'<script>window._csrf_token = "{csrf_token}";</script>' if csrf_token else ""
            
            if self.debug_mode:
                print(f"[DEBUG] Session ID: {sid[:8] if sid else 'None'}...")
                print(f"[DEBUG] CSRF enabled: {self.csrf_enabled}")
                print(f"[DEBUG] CSRF token generated: {bool(csrf_token)}")
            
            # Debug flag injection
            debug_script = f'<script>window._debug_mode = {str(self.debug_mode).lower()};</script>'
            
            # Vendor Resources Selection
            active_theme_name = "dark" if t.mode == "dark" else "light"
            inactive_theme_name = "light" if active_theme_name == "dark" else "dark"
            if self.use_cdn:
                vendor_resources = """
    <link rel="stylesheet" data-vl-critical="true" href="https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/styles/webawesome.css" />
    <link rel="preload" data-vl-critical="true" as="style" href="https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/styles/themes/default.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/styles/themes/default.css" /></noscript>
    <script type="module" src="https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/webawesome.loader.js"></script>
    <script type="module">
        import { getIconLibrary, registerIconLibrary, setDefaultIconFamily } from 'https://cdn.jsdelivr.net/npm/@awesome.me/webawesome@3.5.0/dist-cdn/webawesome.loader.js';

        const legacyViolitIconAliases = Object.freeze({
            'person-fill': 'user',
            'check-circle': 'circle-check',
            'x-circle': 'circle-xmark',
            'info-circle': 'circle-info',
            'exclamation-triangle': 'triangle-exclamation',
            'exclamation-circle': 'circle-exclamation',
            'exclamation-octagon': 'octagon-exclamation',
            'plus-circle': 'circle-plus',
            'circle-fill': 'circle',
            'journal-text': 'note-sticky',
            'check2': 'check'
        });

        const defaultLibrary = getIconLibrary('default');
        if (defaultLibrary) {
            registerIconLibrary('default', {
                resolver: (name, family, variant, autoWidth) => {
                    const normalized = legacyViolitIconAliases[name] || name;
                    return defaultLibrary.resolver(normalized, family, variant, autoWidth);
                },
                mutator: defaultLibrary.mutator,
                spriteSheet: defaultLibrary.spriteSheet
            });
        }

        setDefaultIconFamily('classic');
        window.__vlNormalizeIconName = function(name) {
            return legacyViolitIconAliases[name] || name || 'circle-question';
        };
    </script>
    <script src="https://unpkg.com/htmx.org@1.9.10" defer></script>
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet"></noscript>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4" defer onload="window.__vlTailwindReady = true; window.dispatchEvent(new Event('violit:tailwind-ready'));" onerror="window.__vlTailwindReady = true; window.dispatchEvent(new Event('violit:tailwind-ready')); console.error('Failed to load Tailwind CSS browser runtime');"></script>
    <link rel="preload" as="style" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-dark.min.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-dark.min.css" /></noscript>
    <style>
        .violit-code-light pre code.hljs { background: transparent !important; }
        .violit-code-dark pre code.hljs { background: transparent !important; }
    </style>
    <script>
        // On-demand library loader used by widgets that need heavy vendor scripts
    (function() {
        var _libs = {
            'Plotly':  'https://cdn.plot.ly/plotly-2.27.0.min.js',
            'agGrid':  'https://cdn.jsdelivr.net/npm/ag-grid-community@31.0.1/dist/ag-grid-community.min.js',
                'hljs':    'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js',
                'katex':   'https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.js'
        };
        var _q = {};  // callback queues per lib
        var _s = {};  // loading state: 0=idle, 1=loading, 2=ready
        window._vlLoadLib = function(name, cb) {
            if (window[name]) { cb(); return; }
            if (!_q[name]) _q[name] = [];
            _q[name].push(cb);
            if (_s[name]) return;  // already loading
            _s[name] = 1;
            var s = document.createElement('script');
            s.src = _libs[name];
            s.onload = function() {
                _s[name] = 2;
                var cbs = _q[name] || [];
                _q[name] = [];
                cbs.forEach(function(fn) { fn(); });
            };
            document.head.appendChild(s);
        };

        window._vlPreloadLib = function(name) {
            if (window[name] || _s[name]) return;

            var run = function() {
                window._vlLoadLib(name, function() {});
            };

            if ('requestIdleCallback' in window) {
                window.requestIdleCallback(run, { timeout: 1500 });
            } else {
                setTimeout(run, 200);
            }
        };

        var _deferredActionQueue = [];
        var _deferredActionKeys = new Set();
        var _deferredActionBusy = false;

        function _drainDeferredActions() {
            if (_deferredActionBusy || !_deferredActionQueue.length) return;

            if (!window.sendAction) {
                setTimeout(_drainDeferredActions, 50);
                return;
            }

            _deferredActionBusy = true;
            var next = _deferredActionQueue.shift();
            _deferredActionKeys.delete(next.cid + '::' + next.value);
            window.sendAction(next.cid, next.value);

            setTimeout(function() {
                _deferredActionBusy = false;
                if (_deferredActionQueue.length) {
                    if ('requestIdleCallback' in window) {
                        window.requestIdleCallback(_drainDeferredActions, { timeout: 250 });
                    } else {
                        setTimeout(_drainDeferredActions, 16);
                    }
                }
            }, 16);
        }

        window._vlQueueDeferredAction = function(cid, value) {
            var key = cid + '::' + value;
            if (_deferredActionKeys.has(key)) return;

            _deferredActionKeys.add(key);
            _deferredActionQueue.push({ cid: cid, value: value });

            if ('requestIdleCallback' in window) {
                window.requestIdleCallback(_drainDeferredActions, { timeout: 250 });
            } else {
                setTimeout(_drainDeferredActions, 0);
            }
        };
    })();
    </script>
                """.replace("__ACTIVE_THEME__", active_theme_name).replace("__INACTIVE_THEME__", inactive_theme_name)
            else:
                # Local/Offline Mode
                # Added 'defer' to non-critical heavy scripts to unblock rendering (LCP/FCP improvement)
                vendor_resources = """
    <link rel="stylesheet" data-vl-critical="true" href="/static/vendor/webawesome/styles/webawesome.css" />
    <link rel="preload" data-vl-critical="true" as="style" href="/static/vendor/webawesome/styles/themes/default.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="/static/vendor/webawesome/styles/themes/default.css" /></noscript>
    <script type="module" src="/static/vendor/webawesome/webawesome.loader.js"></script>
    <script type="module">
        import { getIconLibrary, registerIconLibrary, setDefaultIconFamily } from '/static/vendor/webawesome/webawesome.loader.js';

        const legacyViolitIconAliases = Object.freeze({
            'person-fill': 'user',
            'check-circle': 'circle-check',
            'x-circle': 'circle-xmark',
            'info-circle': 'circle-info',
            'exclamation-triangle': 'triangle-exclamation',
            'exclamation-circle': 'circle-exclamation',
            'exclamation-octagon': 'octagon-exclamation',
            'plus-circle': 'circle-plus',
            'circle-fill': 'circle',
            'journal-text': 'note-sticky',
            'check2': 'check'
        });

        const defaultLibrary = getIconLibrary('default');
        if (defaultLibrary) {
            registerIconLibrary('default', {
                resolver: (name, family, variant, autoWidth) => {
                    const normalized = legacyViolitIconAliases[name] || name;
                    return defaultLibrary.resolver(normalized, family, variant, autoWidth);
                },
                mutator: defaultLibrary.mutator,
                spriteSheet: defaultLibrary.spriteSheet
            });
        }

        setDefaultIconFamily('classic');
        window.__vlNormalizeIconName = function(name) {
            return legacyViolitIconAliases[name] || name || 'circle-question';
        };
    </script>
    <script src="/static/vendor/htmx/htmx.min.js" defer></script>
    <script src="/static/vendor/tailwindcss/tailwind.browser.js" defer onload="window.__vlTailwindReady = true; window.dispatchEvent(new Event('violit:tailwind-ready'));" onerror="window.__vlTailwindReady = true; window.dispatchEvent(new Event('violit:tailwind-ready')); console.error('Failed to load Tailwind CSS browser runtime');"></script>
    <link rel="preload" as="style" href="/static/vendor/highlightjs/atom-one-dark.min.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="/static/vendor/highlightjs/atom-one-dark.min.css" /></noscript>
    <style>
        .violit-code-light pre code.hljs { background: transparent !important; }
        .violit-code-dark pre code.hljs { background: transparent !important; }
    </style>
    <script>
    // On-demand library loader used by widgets that need heavy vendor scripts
    (function() {
        var _libs = {
            'Plotly':  '/static/vendor/plotly/plotly-2.27.0.min.js',
            'agGrid':  '/static/vendor/ag-grid/ag-grid-community.min.js',
            'hljs':    '/static/vendor/highlightjs/highlight.min.js',
            'katex':   'https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.js'
        };
        var _q = {};  // callback queues per lib
        var _s = {};  // loading state: 0=idle, 1=loading, 2=ready
        window._vlLoadLib = function(name, cb) {
            if (window[name]) { cb(); return; }
            if (!_q[name]) _q[name] = [];
            _q[name].push(cb);
            if (_s[name]) return;  // already loading
            _s[name] = 1;
            var s = document.createElement('script');
            s.src = _libs[name];
            s.onload = function() {
                _s[name] = 2;
                var cbs = _q[name] || [];
                _q[name] = [];
                cbs.forEach(function(fn) { fn(); });
            };
            document.head.appendChild(s);
        };

        window._vlPreloadLib = function(name) {
            if (window[name] || _s[name]) return;

            var run = function() {
                window._vlLoadLib(name, function() {});
            };

            if ('requestIdleCallback' in window) {
                window.requestIdleCallback(run, { timeout: 1500 });
            } else {
                setTimeout(run, 200);
            }
        };

        var _deferredActionQueue = [];
        var _deferredActionKeys = new Set();
        var _deferredActionBusy = false;

        function _drainDeferredActions() {
            if (_deferredActionBusy || !_deferredActionQueue.length) return;

            if (!window.sendAction) {
                setTimeout(_drainDeferredActions, 50);
                return;
            }

            _deferredActionBusy = true;
            var next = _deferredActionQueue.shift();
            _deferredActionKeys.delete(next.cid + '::' + next.value);
            window.sendAction(next.cid, next.value);

            setTimeout(function() {
                _deferredActionBusy = false;
                if (_deferredActionQueue.length) {
                    if ('requestIdleCallback' in window) {
                        window.requestIdleCallback(_drainDeferredActions, { timeout: 250 });
                    } else {
                        setTimeout(_drainDeferredActions, 16);
                    }
                }
            }, 16);
        }

        window._vlQueueDeferredAction = function(cid, value) {
            var key = cid + '::' + value;
            if (_deferredActionKeys.has(key)) return;

            _deferredActionKeys.add(key);
            _deferredActionQueue.push({ cid: cid, value: value });

            if ('requestIdleCallback' in window) {
                window.requestIdleCallback(_drainDeferredActions, { timeout: 250 });
            } else {
                setTimeout(_drainDeferredActions, 0);
            }
        };
    })();
    </script>
    <!-- Fonts: Inter (local vendor woff2) -->
    <style>
        @font-face {
            font-family: 'Inter';
            font-style: normal;
            font-weight: 100 900;
            font-display: swap;
            src: url('/static/vendor/fonts/inter/inter-latin-ext.woff2') format('woff2');
            unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
        }
        @font-face {
            font-family: 'Inter';
            font-style: normal;
            font-weight: 100 900;
            font-display: swap;
            src: url('/static/vendor/fonts/inter/inter-latin.woff2') format('woff2');
            unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
        }
    </style>
                """

            # Build user CSS from add_css() calls
            user_css = ""
            if self._user_css:
                user_css = "<style id=\"violit-user-css\">\n" + "\n".join(self._user_css) + "\n</style>"
            
            root_style = "visibility:hidden;opacity:0;transition:opacity 0.4s cubic-bezier(0.22, 1, 0.36, 1);" if self.show_splash else ""
            html_class = f"{t.theme_class} {'vl-splash-active' if self.show_splash else ''}".strip()
            body_class = "vl-splash-active" if self.show_splash else ""
            sidebar_resizer_style = "" if (self._sidebar_resizable and (sidebar_c or self.static_sidebar_order)) else "display: none;"
            html = HTML_TEMPLATE.replace("%CONTENT%", main_c).replace("%SIDEBAR_CONTENT%", sidebar_c).replace("%SIDEBAR_STYLE%", sidebar_style).replace("%SIDEBAR_RESIZER_STYLE%", sidebar_resizer_style).replace("%MAIN_CLASS%", main_class).replace("%MODE%", self.mode).replace("%TITLE%", self.app_title).replace("%HTML_CLASS%", html_class).replace("%BODY_CLASS%", body_class).replace("%CSS_VARS%", t.to_css_vars()).replace("%SPLASH%", self._splash_html if self.show_splash else "").replace("%CONTAINER_MAX_WIDTH%", self.container_max_width).replace("%WIDGET_GAP%", self.widget_gap).replace("%SIDEBAR_WIDTH%", self._sidebar_width).replace("%SIDEBAR_MIN_WIDTH%", self._sidebar_min_width).replace("%SIDEBAR_MAX_WIDTH%", self._sidebar_max_width).replace("%SIDEBAR_RESIZABLE%", "true" if self._sidebar_resizable else "false").replace("%CSRF_SCRIPT%", csrf_script).replace("%DEBUG_SCRIPT%", debug_script).replace("%VENDOR_RESOURCES%", vendor_resources).replace("%USER_CSS%", user_css).replace("%ROOT_STYLE%", root_style).replace("%DISCONNECT_TIMEOUT%", str(self.disconnect_timeout))
            return HTMLResponse(html)

        @self.fastapi.post("/action/{cid}")
        async def action(request: Request, cid: str):
            # Session ID: get from cookie
            sid = request.cookies.get("ss_sid")
            
            # CSRF verification
            if self.csrf_enabled:
                f = await request.form()
                csrf_token = f.get("_csrf_token") or request.headers.get("X-CSRF-Token")
                
                if not csrf_token or not self._verify_csrf_token(sid, csrf_token):
                    from fastapi.responses import JSONResponse
                    return JSONResponse(
                        {"error": "Invalid CSRF token"},
                        status_code=403
                    )
            else:
                f = await request.form()
            
            v = f.get("value")
            store = get_session_store()
            act = store['actions'].get(cid) or self.static_actions.get(cid)
            if act:
                if not callable(act):
                    # Debug: print what we got instead
                    self.debug_print(f"ERROR: Action for {cid} is not callable. Got: {type(act)} = {repr(act)}")
                    return HTMLResponse("")
                
                store['eval_queue'] = []
                
                # [PHANTOM WIDGET FIX] Mark current context as action
                act_token = action_ctx.set(True)
                try:
                    act(v) if v is not None else act()
                finally:
                    action_ctx.reset(act_token)
                
                dirty = self._get_dirty_rendered()
                
                # Separate clicked component from other updates
                clicked_component = None
                other_dirty = []
                for c in dirty:
                    if c.id == cid:
                        clicked_component = c
                    else:
                        other_dirty.append(c)
                
                # Re-render clicked component if not dirty
                if clicked_component is None:
                    builder = store['builders'].get(cid) or self.static_builders.get(cid)
                    if builder:
                        clicked_component = builder()
                
                # Build response: clicked component HTML + OOB for others
                response_html = clicked_component.render() if clicked_component else ""
                response_html += self.lite_engine.wrap_oob(other_dirty)
                
                # Process Toasts
                toasts = store.get('toasts', [])
                if toasts:
                    import html as html_lib
                    toasts_json = json.dumps(toasts)
                    toasts_escaped = html_lib.escape(toasts_json)
                    
                    toast_injector = f'''<div id="toast-injector" hx-swap-oob="true" data-toasts="{toasts_escaped}">
                    <script>
                    (function() {{
                        var container = document.getElementById('toast-injector');
                        if (!container) return;
                        var toastsAttr = container.getAttribute('data-toasts');
                        if (!toastsAttr) return;
                        var toasts = JSON.parse(toastsAttr);
                        toasts.forEach(function(t) {{
                            if (typeof createToast === 'function') {{
                                createToast(t.message, t.variant, t.icon);
                            }}
                        }});
                        container.removeAttribute('data-toasts');
                    }})();
                    </script>
                    </div>'''
                    response_html += toast_injector
                    store['toasts'] = []
                
                # Process Effects (Balloons, Snow)
                effects = store.get('effects', [])
                if effects:
                    effects_json = json.dumps(effects)
                    effect_injector = f'''<div id="effects-injector" hx-swap-oob="true" data-effects='{effects_json}'>
                    <script>
                    (function() {{
                        const container = document.getElementById('effects-injector');
                        if (!container) return;
                        const effects = JSON.parse(container.getAttribute('data-effects'));
                        effects.forEach(e => {{
                            if (e === 'balloons') createBalloons();
                            if (e === 'snow') createSnow();
                        }});
                        container.removeAttribute('data-effects');
                    }})();
                    </script>
                    </div>'''
                    response_html += effect_injector
                    store['effects'] = []
                
                return HTMLResponse(response_html)
            return HTMLResponse("")

        @self.fastapi.websocket("/ws")
        async def ws(ws: WebSocket):
            await ws.accept()
            
            # Session ID: get from cookie (all tabs share same session)
            sid = ws.cookies.get("ss_sid") or str(uuid.uuid4())
            
            # [WS SYNC] Ensure store exists for this session
            store = get_session_store()
            
            self.debug_print(f"[WEBSOCKET] Session: {sid[:8]}...")

            # Capture uvicorn's event loop once; used by background tasks
            # to push updates via run_coroutine_threadsafe instead of
            # spawning a new loop per push.
            if self._main_loop is None:
                self._main_loop = asyncio.get_event_loop()
            
            # Set session context (outside while loop - very important!)
            t = session_ctx.set(sid)
            self.ws_engine.sockets[sid] = ws
            
            # Message processing function
            async def process_message(data):
                msg_type = data.get('type')
                if msg_type != 'click' and msg_type != 'tick':
                    return
                
                # [WS CONTEXT FIX]
                # Ensure session context is active for the current WebSocket message.
                msg_token = session_ctx.set(sid)
                try:
                    # Interval tick handler
                    if msg_type == 'tick':
                        interval_id = data.get('id')
                        info = self._interval_callbacks.get(interval_id)
                        if info and info['state'] == 'running':
                            condition = info.get('condition')
                            if condition is None or condition():
                                store = get_session_store()
                                store['eval_queue'] = []
                                info['callback']()
                                for code in store.get('eval_queue', []):
                                    await self.ws_engine.push_eval(sid, code)
                                store['eval_queue'] = []
                                dirty = self._get_dirty_rendered()
                                if dirty:
                                    await self.ws_engine.push_updates(sid, dirty)
                        return
                    # End interval tick handler

                    # Debug WebSocket data
                    self.debug_print(f"[WEBSOCKET ACTION] CID: {data.get('id')}")
                    self.debug_print(f"  Native mode: {self.native_token is not None}")
                    self.debug_print(f"  CSRF enabled: {self.csrf_enabled}")
                    self.debug_print(f"  Native token in payload: {data.get('_native_token')[:20] if data.get('_native_token') else None}...")
                    
                    # Native mode verification (high priority)
                    if self.native_token is not None:
                        native_token = data.get('_native_token')
                        if native_token != self.native_token:
                            self.debug_print(f"  [X] Native token mismatch!")
                            await ws.send_json({"type": "error", "message": "Invalid native token"})
                            return
                        else:
                            self.debug_print(f"  [OK] Native token valid - Skipping CSRF check")
                    else:
                        # CSRF verification for WebSocket (non-native only)
                        if self.csrf_enabled:
                            csrf_token = data.get('_csrf_token')
                            if not csrf_token or not self._verify_csrf_token(sid, csrf_token):
                                self.debug_print(f"  [X] CSRF token invalid")
                                await ws.send_json({"type": "error", "message": "Invalid CSRF token"})
                                return
                            else:
                                self.debug_print(f"  [OK] CSRF token valid")
                    
                    cid, v = data.get('id'), data.get('value')
                    store = get_session_store()
                    act = store['actions'].get(cid) or self.static_actions.get(cid)
                    
                    self.debug_print(f"  Action found: {act is not None}")
                    
                    # Detect if this is a navigation action (nav menu click)
                    is_navigation = cid.startswith('nav_menu')
                    
                    if act:
                        store['eval_queue'] = []
                        self.debug_print(f"  Executing action for CID: {cid} (navigation={is_navigation})...")
                        
                        # [PHANTOM WIDGET FIX] Mark current context as action
                        act_token = action_ctx.set(True)
                        try:
                            act(v) if v is not None else act()
                        finally:
                            action_ctx.reset(act_token)
                        
                        self.debug_print(f"  Action executed")
                        
                        for code in store.get('eval_queue', []):
                            await self.ws_engine.push_eval(sid, code)
                        store['eval_queue'] = []
                        
                        dirty = self._get_dirty_rendered()
                        self.debug_print(f"  Dirty components: {len(dirty)} ({[c.id for c in dirty]})")
                        
                        # Send all dirty components via WebSocket
                        # Pass is_navigation flag to enable/disable smooth transitions
                        if dirty:
                            self.debug_print(f"  Sending {len(dirty)} updates via WebSocket (navigation={is_navigation})...")
                            await self.ws_engine.push_updates(sid, dirty, is_navigation=is_navigation)
                            self.debug_print(f"  [OK] Updates sent successfully")
                        else:
                            self.debug_print(f"  [!] No dirty components found - nothing to update")
                finally:
                    session_ctx.reset(msg_token)
            
            try:
                # Message processing loop
                while True:
                    data = await ws.receive_json()
                    if data.get("type") == "ping":
                        continue
                    await process_message(data)
            except WebSocketDisconnect:
                if sid and sid in self.ws_engine.sockets: 
                    del self.ws_engine.sockets[sid]
                    self.debug_print(f"[WEBSOCKET] Disconnected: {sid[:8]}...")
            finally:
                if t is not None:
                    session_ctx.reset(t)

    def _run_web_reload(self, args):
        """Run with hot reload in web mode using uvicorn's native reload"""
        import inspect
        import uvicorn
        
        self.debug_print(f"[HOT RELOAD] Starting with uvicorn native reload...")
        
        # Trace back to find the caller's module and variable name
        frame = inspect.currentframe()
        app_var_name = None
        module_string = None
        file_path = None
        
        try:
            while frame:
                if frame.f_code.co_name == "<module>":
                    file_path = frame.f_globals.get("__file__")
                    if file_path:
                        # Convert filepath to module string (e.g. "my_app")
                        module_string = os.path.splitext(os.path.basename(file_path))[0]
                        
                        # Find the variable holding this App instance
                        for name, obj in frame.f_globals.items():
                            if obj is self:
                                app_var_name = name
                                break
                        
                        if app_var_name:
                            break
                frame = frame.f_back
        finally:
            del frame

        def _run_subprocess_reload(script_path):
            """Fallback reloader for apps not exposed as a module-level App variable."""
            watch_dir = os.path.dirname(os.path.abspath(script_path)) if script_path else os.getcwd()
            self.debug_print(f"[HOT RELOAD] Falling back to subprocess reload watcher for {watch_dir}")
            print(f"INFO:     Violit web app running on http://localhost:{args.port} (hot reload)")
            print(f"INFO:     (listening on all interfaces: 0.0.0.0:{args.port})")

            is_unix = sys.platform != 'win32'
            popen_kwargs = {}
            if is_unix:
                popen_kwargs['start_new_session'] = True

            child = None

            def _terminate_process(proc):
                try:
                    if is_unix:
                        import signal
                        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                    else:
                        proc.terminate()
                except (ProcessLookupError, OSError):
                    pass

            def _kill_process(proc):
                try:
                    if is_unix:
                        import signal
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    else:
                        proc.kill()
                except (ProcessLookupError, OSError):
                    pass

            try:
                while True:
                    env = os.environ.copy()
                    env["VIOLIT_WORKER"] = "1"

                    self.debug_print("[HOT RELOAD] Starting child server process...", flush=True)
                    child = subprocess.Popen([sys.executable] + sys.argv, env=env, **popen_kwargs)
                    time.sleep(0.3)

                    watcher = FileWatcher(watch_dir=watch_dir, debug_mode=self.debug_mode)
                    intentional_restart = False

                    while child.poll() is None:
                        if watcher.check():
                            self.debug_print("\n[HOT RELOAD] File change detected. Restarting server...", flush=True)
                            intentional_restart = True
                            _terminate_process(child)
                            try:
                                child.wait(timeout=2)
                            except subprocess.TimeoutExpired:
                                _kill_process(child)
                                child.wait()
                            break
                        time.sleep(0.5)

                    if intentional_restart:
                        time.sleep(0.3)
                        continue

                    self.debug_print("[HOT RELOAD] Child server exited. Waiting for file changes...", flush=True)
                    while not watcher.check():
                        time.sleep(0.5)
            except KeyboardInterrupt:
                if child and child.poll() is None:
                    _terminate_process(child)
                    try:
                        child.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        _kill_process(child)
                print("INFO:     Stopping reloader process")
                return
            
        # On Windows, uvicorn's native reload path is prone to duplicate bind
        # behavior when user scripts call app.run() at module scope. The existing
        # subprocess-based watcher is more reliable there.
        if sys.platform == 'win32':
            self.debug_print("[HOT RELOAD] Windows detected; using subprocess-based reload watcher.")
            _run_subprocess_reload(file_path or sys.argv[0])
            return

        if app_var_name and module_string:
            uvicorn_target = f"{module_string}:{app_var_name}.fastapi"
            self.debug_print(f"[HOT RELOAD] Delegating to uvicorn -> {uvicorn_target}")
            
            # Use uvicorn's run with reload=True
            reload_dir = os.path.dirname(os.path.abspath(file_path)) if file_path else os.getcwd()
            
            # [CROSS-PLATFORM] Ensure the script's directory is importable
            # On Linux/macOS, CWD may differ from the script's directory,
            # which would prevent uvicorn workers from importing the module.
            if reload_dir not in sys.path:
                sys.path.insert(0, reload_dir)
            
            # Mark uvicorn reload import/worker processes so module-level app.run()
            # can safely no-op when the script is imported instead of executed.
            os.environ["VIOLIT_WORKER"] = "1"
            os.environ["VIOLIT_UVICORN_RELOAD"] = "1"
            
            # Suppress uvicorn's default "Uvicorn running on http://0.0.0.0:..." message
            # so only our user-friendly localhost URL is shown
            class _SuppressUvicornRunningFilter(logging.Filter):
                def filter(self, record):
                    return 'Uvicorn running on' not in record.getMessage()
            logging.getLogger("uvicorn.error").addFilter(_SuppressUvicornRunningFilter())
            
            try:
                print(f"INFO:     Violit web app running on http://localhost:{args.port} (hot reload)")
                print(f"INFO:     (listening on all interfaces: 0.0.0.0:{args.port})")
                uvicorn.run(
                    uvicorn_target,
                    host="0.0.0.0",
                    port=args.port,
                    reload=True,
                    reload_dirs=[reload_dir],
                    reload_includes=["*.py"],
                    reload_delay=0.1
                )
            except Exception as e:
                self.debug_print(f"[HOT RELOAD] Failed to start uvicorn: {e}")
                sys.exit(1)
        else:
            self.debug_print("[HOT RELOAD] Could not dynamically resolve a module-level App instance.")
            self.debug_print("[HOT RELOAD] Falling back to subprocess-based reloader.")
            _run_subprocess_reload(file_path or sys.argv[0])

    def _run_native_reload(self, args):
        """Run with hot reload in desktop mode"""
        import webview
        # Generate security token for native mode
        self.native_token = secrets.token_urlsafe(32)
        self.is_native_mode = True
        
        # [CROSS-PLATFORM] Watch the script's directory, not CWD
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0])) or os.getcwd()
        self.debug_print(f"[HOT RELOAD] Desktop mode - Watching {script_dir}...")
        
        is_unix = sys.platform != 'win32'
        
        # Shared state for the server process
        server_process = [None]
        should_exit = [False]
        
        def _terminate_process(proc):
            """Cross-platform process termination with process group support"""
            try:
                if is_unix:
                    # On Unix, kill the entire process group to clean up children
                    import signal
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                else:
                    proc.terminate()
            except (ProcessLookupError, OSError):
                pass
        
        def _kill_process(proc):
            """Cross-platform force kill"""
            try:
                if is_unix:
                    import signal
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                else:
                    proc.kill()
            except (ProcessLookupError, OSError):
                pass
        
        def server_manager():
            iteration = 0
            while not should_exit[0]:
                iteration += 1
                env = os.environ.copy()
                env["VIOLIT_WORKER"] = "1"
                env["VIOLIT_SERVER_ONLY"] = "1"
                env["VIOLIT_NATIVE_TOKEN"] = self.native_token
                env["VIOLIT_NATIVE_MODE"] = "1"
                
                # Start server
                self.debug_print(f"\n[Server Manager] Starting server (iteration {iteration})...", flush=True)
                popen_kwargs = {}
                if is_unix:
                    popen_kwargs['start_new_session'] = True
                server_process[0] = subprocess.Popen(
                    [sys.executable] + sys.argv, 
                    env=env,
                    stdout=subprocess.PIPE if iteration > 1 else None,
                    stderr=subprocess.STDOUT if iteration > 1 else None,
                    **popen_kwargs
                )
                
                # Give server time to start
                time.sleep(0.3)
                
                watcher = FileWatcher(watch_dir=script_dir, debug_mode=self.debug_mode)
                
                # Watch loop
                intentional_restart = False
                while server_process[0].poll() is None and not should_exit[0]:
                    if watcher.check():
                        self.debug_print("\n[Server Manager] Reloading server...", flush=True)
                        intentional_restart = True
                        _terminate_process(server_process[0])
                        try:
                            server_process[0].wait(timeout=2)
                            self.debug_print("[Server Manager] Server stopped gracefully", flush=True)
                        except subprocess.TimeoutExpired:
                            self.debug_print("[Server Manager] WARNING: Force killing server...", flush=True)
                            _kill_process(server_process[0])
                            server_process[0].wait()
                        break
                    time.sleep(0.5)
                
                # If it was an intentional restart, reload webview and continue
                if intentional_restart:
                    # Wait for server to be ready
                    time.sleep(0.5)
                    # Reload webview
                    try:
                        if webview.windows:
                            webview.windows[0].load_url(f"http://127.0.0.1:{args.port}?_native_token={self.native_token}")
                            self.debug_print("[Server Manager] \u2713 Webview reloaded", flush=True)
                    except Exception as e:
                        self.debug_print(f"[Server Manager] \u26a0 Webview reload failed: {e}", flush=True)
                    continue
                
                # If exited unexpectedly (crashed), wait for file change
                if server_process[0].poll() is not None and not should_exit[0]:
                     self.debug_print("[Server Manager] WARNING: Server exited unexpectedly. Waiting for file changes...", flush=True)
                     while not watcher.check() and not should_exit[0]:
                         time.sleep(0.5)

        # Start server manager thread
        t = threading.Thread(target=server_manager, daemon=True)
        t.start()
        
        # Patch webview to use custom icon (Windows)
        self._patch_webview_icon()
        
        # Start WebView (Main Thread)
        win_args = {
            'text_select': True, 
            'width': self.width, 
            'height': self.height, 
            'on_top': self.on_top,
        }
        
        # Pass icon to start (for non-WinForms backends)
        start_args = {}
        sig_start = inspect.signature(webview.start)
        if 'icon' in sig_start.parameters and self.app_icon:
            start_args['icon'] = self.app_icon

        window = webview.create_window(self.app_title, f"http://127.0.0.1:{args.port}?_native_token={self.native_token}", **win_args)
        # Bring window to front when it appears
        def _bring_to_front_reload():
            try:
                import ctypes
                hwnd = window.gui
                ctypes.windll.user32.SwitchToThisWindow(hwnd, True)
            except Exception:
                pass
        window.events.shown += _bring_to_front_reload
        webview.start(**start_args)
        
        # Cleanup
        should_exit[0] = True
        if server_process[0]:
            try:
                _terminate_process(server_process[0])
            except: 
                pass
        sys.exit(0)

    # Broadcasting Methods (WebSocket-based real-time sync)
    def broadcast_eval(self, js_code: str, exclude_current: bool = False):
        self.broadcaster.eval_all(js_code, exclude_current=exclude_current)
    
    def broadcast_reload(self, exclude_current: bool = False):
        self.broadcaster.reload_all(exclude_current=exclude_current)
    
    def broadcast_dom_update(self, container_id: str, html: str,
                            position: str = 'prepend', animate: bool = True,
                            exclude_current: bool = False):
        self.broadcaster.broadcast_dom_update(
            container_id, html, position, animate, exclude_current
        )
    
    def broadcast_event(self, event_name: str, data: dict,
                       exclude_current: bool = False):
        self.broadcaster.broadcast_event(event_name, data, exclude_current)
    
    def broadcast_dom_remove(self, selector: str = None,
                            element_id: str = None,
                            data_attribute: tuple = None,
                            animate: bool = True,
                            animation_type: str = 'fade-right',
                            duration: int = 500,
                            exclude_current: bool = False):
        """Remove DOM element from all clients with animation
        
        Example:
            # Remove by ID 
            app.broadcast_dom_remove(element_id='my-element')
            
            # Remove by CSS selector
             app.broadcast_dom_remove(selector='.old-posts')
        """
        self.broadcaster.broadcast_dom_remove(
            selector=selector,
            element_id=element_id,
            data_attribute=data_attribute,
            animate=animate,
            animation_type=animation_type,
            duration=duration,
            exclude_current=exclude_current
        )

    def run(self, port: int = None):
        """Run the application"""
        p = argparse.ArgumentParser()
        p.add_argument("--native", action="store_true")
        p.add_argument("--nosplash", action="store_true", help="Disable splash screen")
        p.add_argument("--reload", action="store_true", help="Enable hot reload")
        p.add_argument("--lite", action="store_true", help="Use Lite mode (HTMX)")
        p.add_argument("--debug", action="store_true", help="Enable developer tools (native mode)")
        p.add_argument("--on-top", action="store_true", help="Keep window always on top (native mode)")
        p.add_argument("--port", type=int, default=8000)
        # DB 마이그레이션 CLI 인자
        p.add_argument("--make-migration", metavar="MSG", default=None,
                       help="Alembic 마이그레이션 파일 생성 후 종료 (migrate='files' 모드 필요)")
        p.add_argument("--apply", action="store_true",
                       help="미적용 Alembic 마이그레이션 적용 후 종료")
        p.add_argument("--rollback", type=int, metavar="N", nargs="?", const=1, default=None,
                       help="Alembic 마이그레이션 N단계 롤백 후 종료")
        args, _ = p.parse_known_args()
        if port is not None:
            args.port = port

        # ── DB 마이그레이션 CLI 인자 처리 (서버 시작 없이 종료) ─────────
        if self.db is not None:
            if args.make_migration is not None:
                self.db.make_migration(args.make_migration)
                return
            if args.apply:
                self.db.apply()
                return
            if args.rollback is not None:
                self.db.rollback(steps=args.rollback)
                return
        if args.on_top:
            self.on_top = True

        # Uvicorn hot reload may import or re-execute the user script in child
        # processes. If a script calls app.run() at module scope, those children
        # must not start another server themselves.
        if os.environ.get("VIOLIT_UVICORN_RELOAD"):
            self.debug_print("[HOT RELOAD] Uvicorn reload child/import detected; skipping nested app.run()")
            return

        # [Logging Filter] Reduce noise by filtering out polling requests
        try:
            import logging
            class PollingFilter(logging.Filter):
                def filter(self, record: logging.LogRecord) -> bool:
                    return "/?_t=" not in record.getMessage()
            
            # Apply filter to uvicorn.access logger
            logging.getLogger("uvicorn.access").addFilter(PollingFilter())
            
            # [Logging Filter] Suppress static vendor file logs unless in debug mode
            if not args.debug:
                class StaticResourceFilter(logging.Filter):
                    def filter(self, record: logging.LogRecord) -> bool:
                        return "/static/vendor/" not in record.getMessage()
                logging.getLogger("uvicorn.access").addFilter(StaticResourceFilter())
        except Exception:
            pass # Ignore if logging setup fails

        # ── 서버 시작 전 자동 마이그레이션 ──────────────────────────────
        if self.db is not None:
            try:
                self.db._run_startup_migration()
            except Exception as _db_exc:
                import logging as _logging
                _logging.getLogger("violit.db").error(
                    f"[violit:db] 시작 시 마이그레이션 오류: {_db_exc}"
                )

        if args.lite:
            self.mode = "lite"
            # Also create lite engine if not already created
            if self.lite_engine is None:
                from .engine import LiteEngine
                self.lite_engine = LiteEngine()

        # Handle internal env var to force "Server Only" mode (for native reload)
        is_server_only = bool(os.environ.get("VIOLIT_SERVER_ONLY"))
        if is_server_only:
            args.native = False
            
        if args.nosplash:
            os.environ["VIOLIT_NOSPLASH"] = "1"
            
        # Hot Reload Manager Logic
        if args.reload and not os.environ.get("VIOLIT_WORKER"):
            if args.native:
                self._run_native_reload(args)
            else:
                self._run_web_reload(args)
            return
        
        # Splash screen logic is already initialized in __init__ using OS environment vars

        if args.native:
            import webview
            # Generate security token for native mode
            self.native_token = secrets.token_urlsafe(32)
            self.is_native_mode = True
            
            # Disable CSRF in native mode (local app security)
            self.csrf_enabled = False
            
            # Use a shared flag to signal server shutdown
            server_shutdown = threading.Event()
            
            @self.fastapi.on_event("startup")
            async def _on_native_startup():
                # Suppress the "Uvicorn running on..." and 403 Forbidden logs.
                class _SuppressUvicornRunningFilter(logging.Filter):
                    def filter(self, record):
                        return 'Uvicorn running on' not in record.getMessage()
                
                class _Suppress403Filter(logging.Filter):
                    def filter(self, record):
                        return '403' not in record.getMessage()
                
                logging.getLogger("uvicorn.error").addFilter(_SuppressUvicornRunningFilter())
                logging.getLogger("uvicorn.access").addFilter(_Suppress403Filter())
                print(f"INFO:     Violit desktop app running on port {args.port}")
            
            def srv(): 
                uvicorn.run(self.fastapi, host="127.0.0.1", port=args.port)
            
            t = threading.Thread(target=srv, daemon=True)
            t.start()
            
            # Do not wait for the server; let the webview initialize in parallel.
            # By the time WebView2 engine initializes (~1s), the server will already be ready
            
            # Patch webview to use custom icon (Windows)
            self._patch_webview_icon()
            
            # Start WebView - This blocks until window is closed
            win_args = {
                'text_select': True, 
                'width': self.width, 
                'height': self.height, 
                'on_top': self.on_top,
            }
            
            # Pass icon and debug mode to start (for non-WinForms backends)
            start_args = {}
            sig_start = inspect.signature(webview.start)
            
            # Enable developer tools (when --debug flag is used)
            if args.debug:
                start_args['debug'] = True
                print("INFO:     Debug mode enabled: Press F12 or Ctrl+Shift+I to open developer tools")
            
            if 'icon' in sig_start.parameters and self.app_icon:
                start_args['icon'] = self.app_icon

            # Add native token to URL for initial access
            window = webview.create_window(self.app_title, f"http://127.0.0.1:{args.port}?_native_token={self.native_token}", **win_args)
            # Bring window to front when it appears
            def _bring_to_front():
                try:
                    import ctypes
                    hwnd = window.gui
                    ctypes.windll.user32.SwitchToThisWindow(hwnd, True)
                except Exception:
                    pass
            window.events.shown += _bring_to_front
            webview.start(**start_args)
            
            # Force exit after window closes to kill the uvicorn thread immediately
            print("App closed. Exiting...")
            os._exit(0)
        elif is_server_only:
            # Native reload subprocess: suppress 403 logs and print a custom startup message.
            @self.fastapi.on_event("startup")
            async def _on_native_reload_startup():
                # Suppress both 403 Forbidden and "Uvicorn running on..." logs.
                class _SuppressForbiddenAndRunningFilter(logging.Filter):
                    def filter(self, record):
                        msg = record.getMessage()
                        return '403' not in msg and 'Uvicorn running on' not in msg
                logging.getLogger("uvicorn.access").addFilter(_SuppressForbiddenAndRunningFilter())
                logging.getLogger("uvicorn.error").addFilter(_SuppressForbiddenAndRunningFilter())
                print(f"INFO:     Violit desktop app running on port {args.port} (hot reload)")
            uvicorn.run(self.fastapi, host="0.0.0.0", port=args.port)
        else:
            # Web mode: print a custom startup message.
            @self.fastapi.on_event("startup")
            async def _on_web_startup():
                # Suppress the default "Uvicorn running on..." message.
                class _SuppressUvicornRunningFilter(logging.Filter):
                    def filter(self, record):
                        return 'Uvicorn running on' not in record.getMessage()
                logging.getLogger("uvicorn.error").addFilter(_SuppressUvicornRunningFilter())
                
                reload_tag = " (hot reload)" if args.reload else ""
                print(f"INFO:     Violit web app running on http://localhost:{args.port}{reload_tag}")
            uvicorn.run(self.fastapi, host="0.0.0.0", port=args.port)


HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html class="%HTML_CLASS%">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="htmx-config" content='{"defaultSwapDelay":0,"defaultSettleDelay":0}'>
    <link rel="preconnect" href="https://cdn.jsdelivr.net">
    <link rel="preconnect" href="https://unpkg.com">
    <link rel="preconnect" href="https://cdn.plot.ly">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <title>%TITLE%</title>
    <script>const mode = "%MODE%";</script>
    %CSRF_SCRIPT%
    %DEBUG_SCRIPT%
    %VENDOR_RESOURCES%
    <style>
        *, *::before, *::after { box-sizing: border-box; }
        :root { 
            %CSS_VARS%
            --sidebar-width: %SIDEBAR_WIDTH%;
            --sidebar-min-width: %SIDEBAR_MIN_WIDTH%;
            --sidebar-max-width: %SIDEBAR_MAX_WIDTH%;
            --vl-sidebar-width: var(--sidebar-width);
        }
           wa-callout { --wa-color-brand-fill-loud: var(--vl-primary); }
           wa-callout::part(base) { border: 1px solid var(--vl-border); }
        
           wa-button {
               --wa-color-brand-fill-loud: var(--vl-primary);
               --wa-color-brand-border-loud: color-mix(in srgb, var(--vl-primary), black 10%);
             caret-color: transparent;
        }
        html {
            overflow-y: scroll;
            scrollbar-gutter: stable;
        }
        html.vl-splash-active, body.vl-splash-active {
            overflow: hidden !important;
            overscroll-behavior: none;
        }
        body { margin: 0; background: var(--vl-bg); color: var(--vl-text); font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; min-height: 100vh; overflow-x: hidden; transition: background 0.3s, color 0.3s; }
        
        /* Soft Animation Mode - Only for sidebar; page transitions are applied by JS on navigation only */
        body.anim-soft #sidebar { transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), padding 0.3s ease, opacity 0.3s ease; }
        
        /* Hard Animation Mode */
        body.anim-hard *, body.anim-hard ::part(base) { transition: none !important; animation: none !important; }
        
        #root { display: flex; width: 100%; min-height: 100vh; }
        #sidebar {
            position: fixed;
            top: 0;
            left: 0;
            width: var(--vl-sidebar-width);
            height: 100vh;
            background: var(--vl-bg-card);
            border-right: 1px solid var(--vl-border);
            padding: 2rem 1rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            overflow-y: auto;
            overflow-x: hidden;
            white-space: nowrap;
            z-index: 1100;
            transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), padding 0.3s ease, opacity 0.3s ease;
        }
        #sidebar.collapsed { width: 0 !important; padding: 2rem 0 !important; border-right: none !important; opacity: 0 !important; pointer-events: none; }
        #sidebar-resizer {
            position: fixed;
            top: 0;
            left: var(--vl-sidebar-width);
            width: 14px;
            height: 100vh;
            transform: translateX(-50%);
            cursor: col-resize;
            z-index: 1101;
            background: transparent;
            touch-action: none;
            transition: opacity 0.2s ease;
        }
        #sidebar-resizer::after {
            content: '';
            position: absolute;
            inset: 0;
            width: 2px;
            margin: 0 auto;
            background: color-mix(in srgb, var(--vl-border), var(--vl-primary) 22%);
            opacity: 0.55;
            transition: background 0.2s ease, opacity 0.2s ease;
        }
        #sidebar-resizer:hover::after,
        body.sidebar-resizing #sidebar-resizer::after {
            background: var(--vl-primary);
            opacity: 1;
        }
        #sidebar.collapsed + #sidebar-resizer,
        #sidebar-resizer[style*='display: none'] {
            opacity: 0;
            pointer-events: none;
        }
        body.sidebar-resizing {
            cursor: col-resize;
            user-select: none;
        }
        
        #main {
            flex: 1;
            margin-left: var(--vl-sidebar-width);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 0 1.5rem 3rem 2.5rem;
            transition: margin-left 0.3s ease, padding 0.3s ease;
        }
        #main.sidebar-collapsed { margin-left: 0; }
        /* Chat input container positioning - respects sidebar */
        .chat-input-container { left: var(--vl-sidebar-width) !important; transition: left 0.3s ease; }
        #sidebar.collapsed ~ #main .chat-input-container,
        #main.sidebar-collapsed .chat-input-container { left: 0 !important; }
        
        #header { width: 100%; max-width: %CONTAINER_MAX_WIDTH%; padding: 1rem 0; display: flex; align-items: center; }
        #app { width: 100%; max-width: %CONTAINER_MAX_WIDTH%; display: flex; flex-direction: column; gap: 1.5rem; }
        .nav-container {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            width: 100%;
        }
        .nav-container wa-button {
            width: 100%;
            caret-color: transparent;
        }
        
        .fragment { display: flex; flex-direction: column; gap: 1.25rem; width: 100%; }
        .page-container { display: flex; flex-direction: column; gap: %WIDGET_GAP%; width: 100%; }
        .card { background: var(--vl-bg-card); border: 1px solid var(--vl-border); padding: 1.5rem; border-radius: var(--vl-radius); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 0.5rem; }
        
        /* Widget spacing - natural breathing room */
        .page-container > div { margin-bottom: 0.5rem; }
        
        /* Headings need more space above to separate sections */
        h1, h2, h3 { font-weight: 600; margin: 0; }
        h1 { font-size: 2.25rem; line-height: 1.2; margin-bottom: 1rem; }
        h2 { font-size: 1.5rem; line-height: 1.3; margin-top: 1.5rem; margin-bottom: 0.75rem; }
        h3 { font-size: 1.25rem; line-height: 1.4; margin-top: 1.25rem; margin-bottom: 0.5rem; }
        .page-container > h1:first-child, .page-container > h2:first-child, .page-container > h3:first-child,
        h1:first-child, h2:first-child, h3:first-child { margin-top: 0; }
        
        /* Web Awesome component spacing */
        wa-input, wa-select, wa-textarea, wa-slider, wa-checkbox, wa-switch, wa-radio-group, wa-color-picker {
            display: block;
            margin-bottom: 1rem;
        }
        wa-textarea::part(form-control-input) {
            min-height: 6.25rem;
        }
        wa-textarea::part(textarea) {
            min-height: 6.25rem;
            line-height: 1.5;
            box-sizing: border-box;
        }
        wa-callout {
            display: block;
            margin-bottom: 1.25rem;
        }
        wa-button {
            margin-top: 0.25rem;
            margin-bottom: 0.5rem;
        }
        wa-divider, .divider {
            --color: var(--vl-border);
            margin: 1.5rem 0;
            width: 100%;
        }
        
        /* Column layouts - using CSS variables for flexible override */
        .columns { 
            display: grid; 
            grid-template-columns: var(--vl-cols, 1fr 1fr); 
            gap: var(--vl-gap, 1rem); 
            align-items: stretch;
            width: 100%; 
            margin-bottom: 0.5rem; 
        }
        .column-item {
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            min-width: 0;
        }
        .column { flex: 1; display: flex; flex-direction: column; gap: 0.75rem; }
        
        /* List container - predefined layout for reactive lists */
        .violit-list-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            width: 100%;
        }
        .violit-list-container > * {
            width: 100%;
        }
        .violit-list-container wa-card {
            width: 100%;
        }
        
        .gradient-text { background: linear-gradient(to right, var(--vl-primary), var(--vl-secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .text-muted { color: var(--vl-text-muted); }
        .metric-label { color: var(--vl-text-muted); font-size: 0.875rem; margin-bottom: 0.25rem; }
        .metric-value { font-size: 2rem; font-weight: 600; }
        .no-select { -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; }
        
        @keyframes fade-in {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        /* Animations for Balloons and Snow */
        @keyframes float-up {
            0% { transform: translateY(var(--start-y, 100vh)) rotate(0deg); opacity: 1; }
            100% { transform: translateY(-20vh) rotate(360deg); opacity: 0; }
        }
        @keyframes fall-down {
            0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
        }
        .balloon, .snowflake {
            position: fixed;
            z-index: 9999;
            pointer-events: none;
            font-size: 2rem;
            user-select: none;
        }
        .balloon { animation: float-up var(--duration) linear forwards; }
        .snowflake { animation: fall-down var(--duration) linear forwards; }
        
        /* ===== Mobile Responsive ===== */
        @media (max-width: 768px) {
            /* Prevent horizontal scroll at root level */
            html, body { overflow-x: hidden; }
            
            /* Force text wrapping on mobile */
            body {
                font-size: 17px !important;
                line-height: 1.7 !important;
                overflow-wrap: break-word;
                word-wrap: break-word;
            }
            
            /* Sidebar: off-canvas overlay on mobile */
            #sidebar {
                width: 280px !important;
                transform: translateX(-100%);
                transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease !important;
                z-index: 2000;
            }
            #sidebar-resizer {
                display: none !important;
            }
            #sidebar.mobile-open {
                transform: translateX(0) !important;
                box-shadow: 4px 0 24px rgba(0,0,0,0.18);
            }
            #sidebar.collapsed {
                transform: translateX(-100%) !important;
                width: 280px !important;
                padding: 2rem 1rem !important;
                opacity: 1 !important;
            }
            
            /* Sidebar backdrop for overlay */
            .vl-sidebar-backdrop {
                position: fixed;
                inset: 0;
                background: rgba(0,0,0,0.4);
                z-index: 1999;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.3s ease;
            }
            .vl-sidebar-backdrop.active {
                opacity: 1;
                pointer-events: auto;
            }
            
            /* Main: full width, no sidebar offset */
            #main {
                margin-left: 0 !important;
                padding: 0 1rem 2rem 1rem !important;
                max-width: 100vw;
            }
            
            /* App container: constrain width, less gap */
            #app {
                gap: 1rem;
                max-width: 100%;
            }
            
            /* Columns: stack vertically on mobile */
            .columns {
                grid-template-columns: 1fr !important;
            }
            .column-item {
                height: auto !important;
            }
            
            /* Chat input: full width on mobile */
            .chat-input-container {
                left: 0 !important;
                width: 100% !important;
            }
            
            /* Typography: improve readability on mobile */
            h1 { font-size: 1.75rem !important; }
            h2 { font-size: 1.3rem !important; }
            h3 { font-size: 1.1rem !important; }
            p, span, div, li { overflow-wrap: break-word; word-wrap: break-word; }
            
            /* Images & videos: prevent overflow */
            img, video, iframe { max-width: 100%; height: auto; }
            
            /* Code blocks: constrain to viewport */
            .violit-code-block { max-width: calc(100vw - 2rem); overflow: hidden; }
            pre, .code-block { overflow-x: auto; max-width: 100%; }
            pre { font-size: 0.82rem !important; }
            
            /* Cards: tighter padding on mobile */
            .card { padding: 1rem; }
            
            /* Table: horizontal scroll wrapper */
            .ag-theme-alpine, .ag-theme-alpine-dark, table {
                display: block;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                max-width: 100%;
            }

            .vl-ag-grid {
                border: 1px solid var(--ag-border-color, var(--vl-border));
                border-radius: var(--vl-radius);
                overflow: hidden;
                background: var(--ag-background-color, var(--vl-bg-card));
                color: var(--ag-foreground-color, var(--vl-text));
            }

            .vl-ag-grid .ag-root-wrapper,
            .vl-ag-grid .ag-header,
            .vl-ag-grid .ag-row,
            .vl-ag-grid .ag-cell,
            .vl-ag-grid .ag-input-field-input,
            .vl-ag-grid .ag-picker-field-wrapper {
                transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
            }
            
            /* Ensure minimum readable font size for small text */
            .page-container p, .page-container span, .page-container div {
                font-size: max(0.9rem, inherit);
            }
            
            /* Hide hamburger when no sidebar content */
            #sidebar[style*="display: none"] ~ #main #header {
                display: none;
            }
        }
    </style>
    %USER_CSS%
</head>
<body class="%BODY_CLASS%">
    %SPLASH%
    <div id="root" style="%ROOT_STYLE%">
        <div id="sidebar" style="%SIDEBAR_STYLE%">
            %SIDEBAR_CONTENT%
        </div>
        <div id="sidebar-resizer" style="%SIDEBAR_RESIZER_STYLE%" aria-hidden="true"></div>
    <div id="main" class="%MAIN_CLASS%">
        <div id="header">
             <wa-button variant="neutral" appearance="plain" onclick="toggleSidebar()"><wa-icon name="list" style="pointer-events: none;"></wa-icon></wa-button>
        </div>
        <div id="app">%CONTENT%</div>
    </div>
    </div>
    <div id="toast-injector" style="display:none;"></div>
    <script>
        // Honor server-provided debug mode only.
        window._debug_mode = window._debug_mode === true;

        // Sidebar navigation is handled via direct onclick on each wa-button.
        // No delegated listener needed.
        window._vlSidebarResizable = %SIDEBAR_RESIZABLE%;
        window._vlSidebarStorageKey = 'violit:sidebar-width:' + window.location.pathname;
        
        // Debug logging helper
        const debugLog = (...args) => {
            if (window._debug_mode) {
                console.log(...args);
            }
        };
        
        // [LOCK] Automatically attach the HTMX CSRF token in Lite mode.
        if (mode === 'lite' && window._csrf_token) {
            document.addEventListener('DOMContentLoaded', function() {
                document.body.addEventListener('htmx:configRequest', function(evt) {
                    evt.detail.parameters['_csrf_token'] = window._csrf_token;
                });
            });
        }
        
        // Helper to clean up Plotly instances before removing elements
        function purgePlotly(container) {
            if (!window.Plotly) return;
            if (container.classList && container.classList.contains('js-plotly-plot')) {
                Plotly.purge(container);
            }
            if (container.querySelectorAll) {
                container.querySelectorAll('.js-plotly-plot').forEach(p => Plotly.purge(p));
            }
        }

        function resolveCssSizeToPx(value) {
            if (!value) return 0;
            if (typeof value === 'number') return value;
            const probe = document.createElement('div');
            probe.style.position = 'absolute';
            probe.style.visibility = 'hidden';
            probe.style.width = value;
            document.body.appendChild(probe);
            const px = probe.getBoundingClientRect().width;
            probe.remove();
            return px;
        }

        function applySidebarWidth(widthValue, persist = true) {
            const root = document.getElementById('root');
            if (!root) return;
            root.style.setProperty('--vl-sidebar-width', widthValue);
            document.documentElement.style.setProperty('--vl-sidebar-width', widthValue);
            if (persist && window._vlSidebarResizable) {
                try {
                    localStorage.setItem(window._vlSidebarStorageKey, widthValue);
                } catch (err) {
                    debugLog('Failed to persist sidebar width', err);
                }
            }
        }

        function syncSidebarWidthFromStorage() {
            if (!window._vlSidebarResizable) return;
            try {
                const savedWidth = localStorage.getItem(window._vlSidebarStorageKey);
                if (savedWidth) {
                    applySidebarWidth(savedWidth, false);
                }
            } catch (err) {
                debugLog('Failed to restore sidebar width', err);
            }
        }

        function setupSidebarResizer() {
            if (!window._vlSidebarResizable) return;
            const resizer = document.getElementById('sidebar-resizer');
            const sidebar = document.getElementById('sidebar');
            if (!resizer || !sidebar) return;

            let dragState = null;

            const endDrag = () => {
                if (!dragState) return;
                dragState = null;
                document.body.classList.remove('sidebar-resizing');
                window.removeEventListener('pointermove', onDrag);
                window.removeEventListener('pointerup', endDrag);
                window.removeEventListener('pointercancel', endDrag);
            };

            const onDrag = (event) => {
                if (!dragState || window.innerWidth <= 768) return;
                const nextWidth = Math.min(dragState.maxWidth, Math.max(dragState.minWidth, dragState.startWidth + (event.clientX - dragState.startX)));
                applySidebarWidth(`${Math.round(nextWidth)}px`);
            };

            resizer.addEventListener('pointerdown', (event) => {
                if (window.innerWidth <= 768 || sidebar.classList.contains('collapsed')) return;
                const computed = getComputedStyle(document.documentElement);
                const minWidth = resolveCssSizeToPx(computed.getPropertyValue('--sidebar-min-width').trim()) || 220;
                const maxWidth = resolveCssSizeToPx(computed.getPropertyValue('--sidebar-max-width').trim()) || 560;
                dragState = {
                    startX: event.clientX,
                    startWidth: sidebar.getBoundingClientRect().width,
                    minWidth,
                    maxWidth,
                };
                document.body.classList.add('sidebar-resizing');
                resizer.setPointerCapture(event.pointerId);
                window.addEventListener('pointermove', onDrag);
                window.addEventListener('pointerup', endDrag);
                window.addEventListener('pointercancel', endDrag);
                event.preventDefault();
            });
        }

        const VL_PART_BRIDGE_PROPERTIES = [
            'background',
            'background-color',
            'background-image',
            'color',
            'border',
            'border-color',
            'border-width',
            'border-style',
            'border-radius',
            'box-shadow',
            'backdrop-filter',
            'filter',
            'opacity',
            'transform',
            'font-size',
            'font-weight',
            'font-family',
            'font-style',
            'line-height',
            'letter-spacing',
            'text-transform',
            'text-decoration',
            'text-align',
            'padding',
            'padding-top',
            'padding-right',
            'padding-bottom',
            'padding-left',
            'white-space'
        ];

        const VL_PART_BRIDGE_ALIASES = {
            'WA-INPUT': {
                'form-control-input': 'input',
            },
            'WA-SELECT': {
                'form-control-input': 'display-input',
                'input': 'display-input',
            },
            'WA-TEXTAREA': {
                'form-control-input': 'textarea',
            },
        };

        function getPartBridgeRoot() {
            let root = document.getElementById('vl-part-bridge-root');
            if (root) return root;
            root = document.createElement('div');
            root.id = 'vl-part-bridge-root';
            root.setAttribute('aria-hidden', 'true');
            root.style.cssText = 'position:absolute;left:-9999px;top:0;width:0;height:0;overflow:hidden;visibility:hidden;pointer-events:none;';
            document.body.appendChild(root);
            return root;
        }

        function waitForAnimationFrames(count = 2) {
            return new Promise((resolve) => {
                const step = (remaining) => {
                    if (remaining <= 0) {
                        resolve();
                        return;
                    }
                    requestAnimationFrame(() => step(remaining - 1));
                };
                step(count);
            });
        }

        function splitUtilityTokens(className) {
            if (!className) return [];

            const tokens = [];
            let current = '';
            let bracketDepth = 0;
            let parenDepth = 0;
            let quoteChar = null;
            let escapeNext = false;

            for (const char of String(className).trim()) {
                if (escapeNext) {
                    current += char;
                    escapeNext = false;
                    continue;
                }

                if (char === '\\') {
                    current += char;
                    escapeNext = true;
                    continue;
                }

                if (quoteChar) {
                    current += char;
                    if (char === quoteChar) quoteChar = null;
                    continue;
                }

                if (char === '"' || char === "'") {
                    current += char;
                    quoteChar = char;
                    continue;
                }

                if (char === '[') {
                    bracketDepth += 1;
                    current += char;
                    continue;
                }

                if (char === ']') {
                    bracketDepth = Math.max(0, bracketDepth - 1);
                    current += char;
                    continue;
                }

                if (char === '(') {
                    parenDepth += 1;
                    current += char;
                    continue;
                }

                if (char === ')') {
                    parenDepth = Math.max(0, parenDepth - 1);
                    current += char;
                    continue;
                }

                if (/\s/.test(char) && bracketDepth === 0 && parenDepth === 0) {
                    const token = current.trim();
                    if (token) tokens.push(token);
                    current = '';
                    continue;
                }

                current += char;
            }

            const finalToken = current.trim();
            if (finalToken) tokens.push(finalToken);
            return tokens;
        }

        function expandHostStateSelectors(selector, partSelector) {
            const variants = [selector];
            const mappings = [
                {
                    needle: `${partSelector}:hover`,
                    replacements: [`:host(:hover) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:active`,
                    replacements: [`:host(:active) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:focus-visible`,
                    replacements: [`:host(:focus-within) ${partSelector}`, `:host(:state(focused)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:focus-within`,
                    replacements: [`:host(:focus-within) ${partSelector}`, `:host(:state(focused)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:focus`,
                    replacements: [`:host(:focus-within) ${partSelector}`, `:host(:state(focused)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:disabled`,
                    replacements: [`:host([disabled]) ${partSelector}`, `:host(:state(disabled)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:checked`,
                    replacements: [`:host([checked]) ${partSelector}`, `:host(:state(checked)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:indeterminate`,
                    replacements: [`:host([indeterminate]) ${partSelector}`, `:host(:state(indeterminate)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:invalid`,
                    replacements: [`:host(:state(user-invalid)) ${partSelector}`],
                },
                {
                    needle: `${partSelector}:valid`,
                    replacements: [`:host(:state(user-valid)) ${partSelector}`],
                },
            ];

            mappings.forEach(({ needle, replacements }) => {
                if (!selector.includes(needle)) return;
                replacements.forEach((replacement) => {
                    variants.push(selector.split(needle).join(replacement));
                });
            });

            if (selector === partSelector || selector.startsWith(`${partSelector}[`) || selector.startsWith(`${partSelector}.`)) {
                variants.push(`:host([checked]) ${partSelector}`);
                variants.push(`:host(:state(checked)) ${partSelector}`);
                variants.push(`:host([disabled]) ${partSelector}`);
                variants.push(`:host(:state(disabled)) ${partSelector}`);
                variants.push(`:host(:focus-within) ${partSelector}`);
                variants.push(`:host(:state(focused)) ${partSelector}`);
            }

            return Array.from(new Set(variants));
        }

        function transformUtilitySelectorForPart(selector, classSelector, partSelector) {
            if (!selector || !selector.includes(classSelector)) return [];
            const rewritten = selector.split(classSelector).join(partSelector).trim();
            if (!rewritten) return [];
            const expanded = expandHostStateSelectors(rewritten, partSelector);
            return Array.from(new Set(expanded.flatMap((item) => {
                const normalized = String(item || '').trim();
                if (!normalized) return [];
                if (normalized.includes(':host')) return [normalized];
                return [normalized, `:host ${normalized}`];
            })));
        }

        function serializeImportantStyleDeclaration(styleDecl) {
            if (!styleDecl) return '';
            return Array.from(styleDecl)
                .map((prop) => {
                    const value = styleDecl.getPropertyValue(prop);
                    if (!value) return '';
                    return `${prop}:${value.trim()} !important;`;
                })
                .filter(Boolean)
                .join('');
        }

        function collectDeclaredProperties(cssText) {
            const props = new Set();
            if (!cssText) return props;
            const matches = String(cssText).matchAll(/([a-zA-Z-]+)\s*:/g);
            for (const match of matches) {
                const prop = match[1] && match[1].trim().toLowerCase();
                if (prop) props.add(prop);
            }
            return props;
        }

        function isPropCoveredByGeneratedCss(prop, declaredProps) {
            const normalized = String(prop || '').trim().toLowerCase();
            if (!normalized) return false;
            if (declaredProps.has(normalized)) return true;

            if (normalized === 'background' || normalized.startsWith('background-')) {
                return declaredProps.has('background') || declaredProps.has('background-color') || declaredProps.has('background-image');
            }

            if (normalized === 'border' || normalized.startsWith('border-')) {
                return declaredProps.has('border')
                    || declaredProps.has('border-color')
                    || declaredProps.has('border-width')
                    || declaredProps.has('border-style')
                    || declaredProps.has('border-radius');
            }

            if (normalized.startsWith('padding-') || normalized === 'padding') {
                return declaredProps.has('padding')
                    || declaredProps.has('padding-top')
                    || declaredProps.has('padding-right')
                    || declaredProps.has('padding-bottom')
                    || declaredProps.has('padding-left');
            }

            if (normalized.startsWith('color')) {
                return declaredProps.has('color');
            }

            return false;
        }

        function serializeUtilityRuleForPart(rule, classSelector, partSelector, parentSelector = '') {
            if (!rule) return '';

            const selectorText = String(rule.selectorText || '').trim();
            const resolvedSelector = selectorText && parentSelector && selectorText.includes('&')
                ? selectorText.split('&').join(parentSelector)
                : selectorText;

            if (rule.type === CSSRule.STYLE_RULE) {
                const selectors = resolvedSelector
                    ? resolvedSelector
                        .split(',')
                        .map((selector) => selector.trim())
                        .flatMap((selector) => transformUtilitySelectorForPart(selector, classSelector, partSelector))
                    : [];

                const declarationText = serializeImportantStyleDeclaration(rule.style);
                const ownRule = selectors.length && declarationText
                    ? `${Array.from(new Set(selectors)).join(',')}{${declarationText}}`
                    : '';
                const nestedRules = Array.from(rule.cssRules || [])
                    .map((childRule) => serializeUtilityRuleForPart(childRule, classSelector, partSelector, resolvedSelector))
                    .filter(Boolean)
                    .join('');
                return `${ownRule}${nestedRules}`;
            }

            if (rule.type === CSSRule.MEDIA_RULE) {
                const inner = Array.from(rule.cssRules || [])
                    .map((childRule) => serializeUtilityRuleForPart(childRule, classSelector, partSelector, parentSelector))
                    .join('');
                return inner ? `@media ${rule.conditionText}{${inner}}` : '';
            }

            if (rule.type === CSSRule.SUPPORTS_RULE) {
                const inner = Array.from(rule.cssRules || [])
                    .map((childRule) => serializeUtilityRuleForPart(childRule, classSelector, partSelector, parentSelector))
                    .join('');
                return inner ? `@supports ${rule.conditionText}{${inner}}` : '';
            }

            if (rule.type === CSSRule.KEYFRAMES_RULE || rule.type === CSSRule.FONT_FACE_RULE) {
                return rule.cssText;
            }

            if (rule.cssRules?.length) {
                return Array.from(rule.cssRules)
                    .map((childRule) => serializeUtilityRuleForPart(childRule, classSelector, partSelector, parentSelector))
                    .filter(Boolean)
                    .join('');
            }

            return '';
        }

        function transformCssTextForPart(cssText, token, partSelector) {
            if (!cssText) return '';

            const root = getPartBridgeRoot();
            const parserStyle = document.createElement('style');
            parserStyle.textContent = cssText;
            root.appendChild(parserStyle);

            try {
                const classSelector = `.${CSS.escape(token)}`;
                return Array.from(parserStyle.sheet?.cssRules || [])
                    .map((rule) => serializeUtilityRuleForPart(rule, classSelector, partSelector))
                    .filter(Boolean)
                    .join('\n');
            } catch (err) {
                debugLog('Failed to transform utility rule for part bridge', err);
                return '';
            } finally {
                parserStyle.remove();
            }
        }

        async function ensureTailwindTokensGenerated(className) {
            const normalized = (className || '').trim();
            if (!normalized) return;

            const root = getPartBridgeRoot();
            const probe = document.createElement('div');
            probe.className = normalized;
            probe.style.cssText = 'display:block;position:absolute;left:-9999px;top:0;visibility:hidden;pointer-events:none;';
            probe.textContent = 'M';
            root.appendChild(probe);
            await waitForAnimationFrames(2);
            probe.remove();
        }

        function getTailwindRuntimeSheets() {
            if (window._vlTailwindRuntimeSheets?.length) {
                return window._vlTailwindRuntimeSheets;
            }

            const sheets = Array.from(document.styleSheets || []).filter((sheet) => {
                const owner = sheet.ownerNode;
                if (!owner || owner.tagName !== 'STYLE') return false;
                const text = owner.textContent || '';
                return text.includes('tailwindcss v4') || text.includes('@layer theme, base, components, utilities');
            });

            window._vlTailwindRuntimeSheets = sheets;
            return sheets;
        }

        function collectGeneratedCssForToken(token, partSelector) {
            const classSelector = `.${CSS.escape(token)}`;
            const cssBlocks = [];

            getTailwindRuntimeSheets().forEach((sheet) => {
                try {
                    Array.from(sheet.cssRules || []).forEach((rule) => {
                        const cssBlock = serializeUtilityRuleForPart(rule, classSelector, partSelector);
                        if (cssBlock) cssBlocks.push(cssBlock);
                    });
                } catch (err) {
                    // Ignore cross-origin or protected stylesheets.
                }
            });

            return cssBlocks.join('\n');
        }

        async function buildTailwindPartCss(className, partSelector) {
            const normalized = (className || '').trim();
            if (!normalized) return '';

            window._vlTailwindPartCssCache = window._vlTailwindPartCssCache || new Map();
            const cacheKey = `${partSelector}::${normalized}`;
            if (window._vlTailwindPartCssCache.has(cacheKey)) {
                return window._vlTailwindPartCssCache.get(cacheKey);
            }

            await ensureTailwindTokensGenerated(normalized);

            const cssBlocks = [];
            for (const token of splitUtilityTokens(normalized)) {
                const cssBlock = collectGeneratedCssForToken(token, partSelector);
                if (cssBlock) cssBlocks.push(cssBlock);
            }

            const finalCss = cssBlocks.join('\n');
            window._vlTailwindPartCssCache.set(cacheKey, finalCss);
            return finalCss;
        }

        async function computeTailwindPartStyles(className) {
            const normalized = (className || '').trim();
            if (!normalized) return {};

            window._vlTailwindPartStyleCache = window._vlTailwindPartStyleCache || new Map();
            if (window._vlTailwindPartStyleCache.has(normalized)) {
                return window._vlTailwindPartStyleCache.get(normalized);
            }

            const root = getPartBridgeRoot();
            const baseline = document.createElement('div');
            const probe = document.createElement('div');
            const baseCss = 'display: block; position: absolute; left: -9999px; top: 0; visibility: hidden; pointer-events: none;';
            baseline.style.cssText = baseCss;
            probe.style.cssText = baseCss;
            baseline.textContent = 'M';
            probe.textContent = 'M';

            await ensureTailwindTokensGenerated(normalized);

            probe.className = normalized;
            root.appendChild(baseline);
            root.appendChild(probe);
            await waitForAnimationFrames(1);

            const baselineStyle = getComputedStyle(baseline);
            const probeStyle = getComputedStyle(probe);
            const styles = {};

            VL_PART_BRIDGE_PROPERTIES.forEach((prop) => {
                const nextValue = probeStyle.getPropertyValue(prop).trim();
                const baseValue = baselineStyle.getPropertyValue(prop).trim();
                if (nextValue && nextValue !== baseValue) {
                    styles[prop] = nextValue;
                }
            });

            baseline.remove();
            probe.remove();
            window._vlTailwindPartStyleCache.set(normalized, styles);
            return styles;
        }

        async function applyTailwindPartStyles(host) {
            if (!host || !host.shadowRoot) return;

            let partMap = null;
            try {
                partMap = JSON.parse(host.getAttribute('data-vl-part-cls') || '{}');
            } catch (err) {
                debugLog('Failed to parse data-vl-part-cls', err);
                return;
            }

            host.shadowRoot.querySelectorAll('[data-vl-part-props]').forEach((partEl) => {
                const previousProps = (partEl.getAttribute('data-vl-part-props') || '')
                    .split('|')
                    .map((item) => item.trim())
                    .filter(Boolean);
                previousProps.forEach((prop) => partEl.style.removeProperty(prop));
                partEl.removeAttribute('data-vl-part-props');
            });

            let combinedCss = '';

            for (const [partName, className] of Object.entries(partMap)) {
                if (!partName || !className) continue;
                const aliasMap = VL_PART_BRIDGE_ALIASES[host.tagName] || {};
                const resolvedPartName = aliasMap[partName] || partName;
                const selector = `[part~="${CSS.escape(resolvedPartName)}"]`;
                const cssText = await buildTailwindPartCss(className, selector);
                const styles = await computeTailwindPartStyles(className);
                const declaredProps = collectDeclaredProperties(cssText);

                if (cssText) {
                    combinedCss += `${cssText}\n`;
                }

                host.shadowRoot.querySelectorAll(selector).forEach((partEl) => {
                    const appliedProps = [];
                    Object.entries(styles).forEach(([prop, value]) => {
                        if (!value) return;
                        if (isPropCoveredByGeneratedCss(prop, declaredProps)) return;
                        partEl.style.setProperty(prop, value, 'important');
                        appliedProps.push(prop);
                    });

                    if (appliedProps.length) {
                        partEl.setAttribute('data-vl-part-props', appliedProps.join('|'));
                    } else {
                        partEl.removeAttribute('data-vl-part-props');
                    }
                });
            }

            let styleEl = host.shadowRoot.querySelector('style[data-vl-part-style="true"]');
            if (combinedCss.trim()) {
                if (!styleEl) {
                    styleEl = document.createElement('style');
                    styleEl.setAttribute('data-vl-part-style', 'true');
                    host.shadowRoot.appendChild(styleEl);
                }
                styleEl.textContent = combinedCss;
            } else if (styleEl) {
                styleEl.remove();
            }
        }

        async function runTailwindPartBridge(scope = document) {
            const hosts = scope && scope.querySelectorAll ? scope.querySelectorAll('[data-vl-part-cls]') : [];
            await Promise.all(Array.from(hosts).map((host) => applyTailwindPartStyles(host)));
        }

        window._vlApplyPartBridge = function(scope = document) {
            const schedule = () => {
                const invoke = () => {
                    requestAnimationFrame(() => {
                        requestAnimationFrame(() => runTailwindPartBridge(scope));
                    });
                };

                invoke();
                setTimeout(invoke, 120);
                setTimeout(invoke, 360);
            };

            if (window.__vlTailwindReady) {
                schedule();
                return;
            }

            window.addEventListener('violit:tailwind-ready', schedule, { once: true });
        };

        window.applyPartStyles = applyTailwindPartStyles;

        // [FIX] Plotly Auto-Resize Logic
        // Handles resizing when:
        // 1. Window resizes
        // 2. Tab switches (visibility changes)
        // 3. Container size changes (sidebar toggle, etc)
        function setupPlotlyResizer() {
            if (!window.Plotly || window._vlPlotlyResizerBound) return;
            window._vlPlotlyResizerBound = true;

            const resizeTimers = new WeakMap();
            const sizeCache = new WeakMap();

            const requestPlotResize = (el, force = false, delay = 80) => {
                if (!el) return;
                const pending = resizeTimers.get(el);
                if (pending) {
                    clearTimeout(pending);
                }

                const timer = setTimeout(() => {
                    resizeTimers.delete(el);
                    if (el.offsetParent === null) return;

                    if (typeof window._vlPlotlyRequestResize === 'function' && el.id) {
                        window._vlPlotlyRequestResize(el.id, force);
                        return;
                    }

                    if (window.Plotly && el.querySelector('.plot-container')) {
                        Plotly.Plots.resize(el);
                    }
                }, delay);

                resizeTimers.set(el, timer);
            };

            // 1. Resize on window resize (with debounce for performance)
            let resizeTimer;
            window.addEventListener('resize', () => {
                clearTimeout(resizeTimer);
                resizeTimer = setTimeout(() => {
                    document.querySelectorAll('.js-plotly-plot').forEach(el => {
                        if (el.offsetParent !== null) {
                            requestPlotResize(el, true, 60);
                        }
                    });
                }, 150);
            });

            // 2. Resize on Tab Switch
            // Charts in previously hidden tabs are handled by IntersectionObserver
            // in the chart render script. This handler covers charts that were
            // already rendered but may need resizing after a tab switch.
            document.addEventListener('wa-tab-show', (event) => {
                requestAnimationFrame(() => {
                    requestAnimationFrame(() => {
                        document.querySelectorAll('.js-plotly-plot').forEach(el => {
                            if (el.offsetParent !== null) {
                                requestPlotResize(el, true, 40);
                            }
                        });
                    });
                });
            });
            
            // 3. ResizeObserver for container changes
            const ro = new ResizeObserver(entries => {
                for (let entry of entries) {
                    const el = entry.target;
                    if (!el.classList.contains('js-plotly-plot') || el.offsetParent === null) {
                        continue;
                    }

                    const nextSize = {
                        width: Math.round(entry.contentRect.width || 0),
                        height: Math.round(entry.contentRect.height || 0),
                    };
                    if (nextSize.width < 10) {
                        continue;
                    }

                    const prevSize = sizeCache.get(el);
                    sizeCache.set(el, nextSize);
                    if (prevSize && Math.abs(prevSize.width - nextSize.width) < 2 && Math.abs(prevSize.height - nextSize.height) < 2) {
                        continue;
                    }

                    requestPlotResize(el, true, 60);
                }
            });

            // Observe existing plots
            document.querySelectorAll('.js-plotly-plot').forEach(el => ro.observe(el));

            // Observe new plots added dynamically
            const mo = new MutationObserver(mutations => {
                for (let mutation of mutations) {
                    for (let node of mutation.addedNodes) {
                        if (node.nodeType === 1) {
                            if (node.classList.contains('js-plotly-plot')) {
                                ro.observe(node);
                            }
                            node.querySelectorAll('.js-plotly-plot').forEach(el => ro.observe(el));
                        }
                    }
                }
            });
            mo.observe(document.body, { childList: true, subtree: true });
        }

        // Initialize Resizer
        document.addEventListener('DOMContentLoaded', function() {
            syncSidebarWidthFromStorage();
            setupSidebarResizer();
            window._vlLoadLib('Plotly', setupPlotlyResizer);
            window._vlApplyPartBridge(document);
        });

        if (mode === 'ws') {
            // Interval infrastructure
            window._vlIntervals = window._vlIntervals || {};

            window._vlCreateInterval = function(id, ms, autostart) {
                if (window._vlIntervals[id]) return; // prevent duplicates

                var ctrl = {
                    _timer:   null,
                    _paused:  !autostart,
                    _stopped: false,
                    _ms:      ms,
                    _id:      id,

                    _tick: function() {
                        if (window._ws && window._ws.readyState === 1) {
                            window._ws.send(JSON.stringify({ type: 'tick', id: id }));
                        }
                    },

                    start: function() {
                        if (!ctrl._paused && !ctrl._stopped && !ctrl._timer) {
                            ctrl._timer = setInterval(ctrl._tick, ctrl._ms);
                        }
                    },

                    pause: function() {
                        ctrl._paused = true;
                        if (ctrl._timer) { clearInterval(ctrl._timer); ctrl._timer = null; }
                    },

                    resume: function() {
                        ctrl._paused = false;
                        ctrl._stopped = false;
                        ctrl.start();
                    },

                    stop: function() {
                        ctrl._stopped = true;
                        if (ctrl._timer) { clearInterval(ctrl._timer); ctrl._timer = null; }
                        delete window._vlIntervals[id];
                    }
                };

                window._vlIntervals[id] = ctrl;

                // Wait for WebSocket to be ready, then start
                if (autostart) {
                    function waitAndStart() {
                        if (window._ws && window._ws.readyState === 1) {
                            ctrl.start();
                        } else {
                            setTimeout(waitAndStart, 200);
                        }
                    }
                    waitAndStart();
                }
            };
            // End interval infrastructure

            window._wsReady = false;
            window._actionQueue = [];
            window._ws = null;
            
            // Page scroll position memory: { pageKey: scrollY }
            window._pageScrollPositions = {};
            window._currentPageKey = null;
            window._pendingScrollRestore = null;

            window._vlFindAgGridViewport = (root) => {
                const scope = root && typeof root.querySelectorAll === 'function' ? root : document;
                const candidates = Array.from(scope.querySelectorAll('.ag-center-cols-viewport, .ag-body-viewport'));
                if (!candidates.length) {
                    return null;
                }
                return candidates.find((candidate) => {
                    return candidate.scrollTop > 0 || candidate.scrollLeft > 0 || candidate.scrollHeight > candidate.clientHeight || candidate.scrollWidth > candidate.clientWidth;
                }) || candidates[0];
            };

            window._vlCaptureAgGridScroll = (root) => {
                const viewport = window._vlFindAgGridViewport(root);
                if (!viewport) {
                    return null;
                }
                return {
                    top: viewport.scrollTop || 0,
                    left: viewport.scrollLeft || 0
                };
            };

            window._vlHideAgGridDuringScrollRestore = (root, state) => {
                if (!root || !state || ((state.top || 0) === 0 && (state.left || 0) === 0)) {
                    return () => {};
                }

                const previousVisibility = root.style.visibility;
                root.style.visibility = 'hidden';

                return () => {
                    root.style.visibility = previousVisibility;
                };
            };

            window._vlRestoreAgGridScroll = (root, state, onDone) => {
                if (!state) {
                    if (typeof onDone === 'function') {
                        onDone();
                    }
                    return;
                }

                let attempts = 0;
                const maxAttempts = 12;
                let finished = false;

                const finish = () => {
                    if (finished) {
                        return;
                    }
                    finished = true;
                    if (typeof onDone === 'function') {
                        onDone();
                    }
                };

                const restore = () => {
                    const viewport = window._vlFindAgGridViewport(root);
                    if (!viewport) {
                        if (attempts < maxAttempts) {
                            attempts += 1;
                            requestAnimationFrame(restore);
                        } else {
                            finish();
                        }
                        return;
                    }

                    viewport.scrollTop = state.top || 0;
                    viewport.scrollLeft = state.left || 0;

                    if (attempts < 2) {
                        attempts += 1;
                        requestAnimationFrame(restore);
                        return;
                    }

                    setTimeout(() => {
                        const finalViewport = window._vlFindAgGridViewport(root);
                        if (finalViewport) {
                            finalViewport.scrollTop = state.top || 0;
                            finalViewport.scrollLeft = state.left || 0;
                        }
                        finish();
                    }, 80);
                };

                restore();
            };
            
            // Define sendAction IMMEDIATELY (before WebSocket connection)
            window.sendAction = (cid, val) => {
                debugLog(`[sendAction] Called with cid=${cid}, val=${val}`);

                window._pendingScrollRestore = {
                    x: window.scrollX || 0,
                    y: window.scrollY || window.pageYOffset || 0
                };
                
                const payload = {
                    type: 'click',
                    id: cid,
                    value: val
                };
                
                if (window._csrf_token) {
                    payload._csrf_token = window._csrf_token;
                }
                
                const urlParams = new URLSearchParams(window.location.search);
                const nativeToken = urlParams.get('_native_token');
                if (nativeToken) {
                    payload._native_token = nativeToken;
                }
                
                if (cid.startsWith('nav_menu')) {
                    if (window._currentPageKey) {
                        window._pageScrollPositions[window._currentPageKey] = window.scrollY;
                        debugLog(`Saved scroll ${window.scrollY}px for page: ${window._currentPageKey}`);
                    }
                    window._pendingPageKey = val;
                    const pageName = val.replace('page_', '');
                    window.location.hash = pageName;
                    debugLog(`Updated hash: #${pageName}`);
                }
                
                if (!window._wsReady || !window._ws) {
                    debugLog(`WebSocket not ready, queueing action: ${cid}`);
                    window._actionQueue.push(payload);
                } else {
                    debugLog(`Sending action to server: ${cid}`);
                    window._ws.send(JSON.stringify(payload));
                }
            };

            window._ws = null;

            // Now connect WebSocket
            window._ws = new WebSocket((location.protocol === 'https:' ? 'wss:' : 'ws:') + "//" + location.host + "/ws");
            
            window._intentionalDisconnect = false;
            window._vlTimeout = %DISCONNECT_TIMEOUT%;
            window._vlLastActivity = Date.now();

            if (window._vlTimeout >= 0) {
                // Send ping every 25 seconds to prevent network timeout
                setInterval(() => {
                    if (window._ws && window._ws.readyState === 1) {
                        if (window._vlTimeout > 0 && (Date.now() - window._vlLastActivity) > window._vlTimeout * 1000) {
                            debugLog("[WebSocket] Disconnecting due to inactivity timeout.");
                            window._intentionalDisconnect = true;
                            window._ws.close();
                            document.body.style.transition = 'opacity 0.5s';
                            document.body.style.opacity = '0.5';
                            document.body.style.pointerEvents = 'none';
                        } else {
                            window._ws.send(JSON.stringify({ type: 'ping' }));
                        }
                    }
                }, 25000);

                if (window._vlTimeout > 0) {
                    const resetActivity = () => { window._vlLastActivity = Date.now(); };
                    document.addEventListener('mousemove', resetActivity, {passive: true});
                    document.addEventListener('keydown', resetActivity, {passive: true});
                    document.addEventListener('click', resetActivity, {passive: true});
                    document.addEventListener('scroll', resetActivity, {passive: true});
                }
            }

            // Auto-reconnect/reload logic
            window._ws.onclose = () => {
                if (window._intentionalDisconnect) return;
                window._wsReady = false;
                debugLog("[WebSocket] Connection lost. Auto-reloading...");

                let retryDelay = 50;
                const maxDelay = 2000;
                
                const checkServer = () => {
                   fetch(location.href)
                       .then(r => {
                           if(r.ok) {
                               debugLog("[Hot Reload] Server back online. Reloading...");
                               window.location.reload();
                           } else {
                               retryDelay = Math.min(retryDelay * 1.5, maxDelay);
                               setTimeout(checkServer, retryDelay);
                           }
                       })
                       .catch(() => {
                           retryDelay = Math.min(retryDelay * 1.5, maxDelay);
                           setTimeout(checkServer, retryDelay);
                       });
                };
                setTimeout(checkServer, retryDelay);
            };
            
            // CRITICAL: Restore from hash ONLY after WebSocket is connected
            window._ws.onopen = () => {
                debugLog("[WebSocket] Connected successfully");
                window._wsReady = true;
                
                // Process queued actions
                if (window._actionQueue.length > 0) {
                    debugLog(`[WebSocket] Processing ${window._actionQueue.length} queued action(s)...`);
                    window._actionQueue.forEach(payload => {
                        window._ws.send(JSON.stringify(payload));
                    });
                    window._actionQueue.length = 0; // Clear queue
                }
                
                // Restore from hash after processing queue
                setTimeout(restoreFromHash, 100);
            };
            
            // Handle WebSocket errors
            window._ws.onerror = (error) => {
                window._wsReady = false;
                debugLog("[WebSocket] Error:", error);
            };

            window._ws.onmessage = (e) => {
                debugLog("[WebSocket] Message received");
                const msg = JSON.parse(e.data);
                if(msg.type === 'update') {
                    // Check if this is a navigation update (page transition)
                    // Server sends isNavigation flag based on action type
                    const isNavigation = msg.isNavigation === true;
                    
                    // Helper function to apply updates
                    const applyUpdates = (items) => {
                        items.forEach(item => {
                            const el = document.getElementById(item.id);
                            
                            // Focus Guard: Skip update if element is focused input to prevent interrupting typing
                            if (document.activeElement && el) {
                                 const isSelfOrChild = document.activeElement.id === item.id || el.contains(document.activeElement);
                                 const isShadowChild = document.activeElement.closest && document.activeElement.closest(`#${item.id}`);
                                 
                                 if (isSelfOrChild || isShadowChild) {
                                     // Check if it's actually an input that needs protection
                                     const tag = document.activeElement.tagName.toLowerCase();
                                     const isInput = tag === 'input' || tag === 'textarea' || tag.startsWith('wa-input') || tag.startsWith('wa-textarea') || tag.startsWith('wa-slider');
                                     
                                     // If it's an input, block update. If it's a button (nav menu), ALLOW update.
                                     if (isInput) {
                                         return;
                                     }
                                 }
                            }

                            if(el) {
                                // Smart update for specific widget types to preserve animations/instances
                                const widgetType = item.id.split('_')[0];
                                let smartUpdated = false;
                                
                                // Checkbox/Toggle: Update checked property only (preserve animation)
                                if (widgetType === 'checkbox' || widgetType === 'toggle') {
                                    // Parse new HTML to extract checked state
                                    const temp = document.createElement('div');
                                    temp.innerHTML = item.html;
                                    const newCheckbox = temp.querySelector('wa-checkbox, wa-switch');
                                    
                                    if (newCheckbox) {
                                        // Find the actual checkbox element (may be direct or nested)
                                        const checkboxEl = el.tagName && (el.tagName.toLowerCase() === 'wa-checkbox' || el.tagName.toLowerCase() === 'wa-switch')
                                            ? el 
                                            : el.querySelector('wa-checkbox, wa-switch');
                                        
                                        if (checkboxEl) {
                                            const shouldBeChecked = newCheckbox.hasAttribute('checked');
                                            // Only update if different to avoid interrupting user interaction
                                            if (checkboxEl.checked !== shouldBeChecked) {
                                                checkboxEl.checked = shouldBeChecked;
                                            }
                                            smartUpdated = true;
                                        }
                                    }
                                }
                                
                                // Slider: Update value property only (preserve drag interaction)
                                if (widgetType === 'slider') {
                                    const temp = document.createElement('div');
                                    temp.innerHTML = item.html;
                                    const newRange = temp.querySelector('wa-slider');
                                    if (newRange) {
                                        const rangeEl = el.tagName && el.tagName.toLowerCase() === 'wa-slider'
                                            ? el : el.querySelector('wa-slider');
                                        if (rangeEl) {
                                            const newVal = newRange.getAttribute('value');
                                            if (newVal !== null && rangeEl.value !== parseFloat(newVal)) {
                                                rangeEl.value = parseFloat(newVal);
                                            }
                                            smartUpdated = true;
                                        }
                                    }
                                }
                                
                                // AG Grid-backed widgets: update rowData without replacing the whole DOM.
                                // This avoids the destroy/recreate flash that happens when dataframe widgets
                                // are rerendered reactively after a click.
                                if (widgetType === 'df' || (widgetType === 'data' && item.id.includes('editor'))) {
                                    const baseCid = item.id.replace('_wrapper', '');
                                    const gridApi = window['gridApi_' + baseCid];
                                    if (gridApi) {
                                        const match = item.html.match(/rowData:\s*(\[.*?\])/s);
                                        if (match) {
                                            try {
                                                const newData = JSON.parse(match[1]);
                                                const gridRoot = document.getElementById(baseCid) || el.querySelector(`#${baseCid}`) || el;
                                                const agGridScrollState = window._vlCaptureAgGridScroll(gridRoot);

                                                if (typeof gridApi.setGridOption === 'function') {
                                                    gridApi.setGridOption('rowData', newData);
                                                } else if (typeof gridApi.setRowData === 'function') {
                                                    gridApi.setRowData(newData);
                                                }

                                                window._vlRestoreAgGridScroll(gridRoot, agGridScrollState);
                                                smartUpdated = true;
                                            } catch (e) {
                                                console.error('Failed to parse AG Grid data:', e);
                                            }
                                        }
                                    }
                                }

                                // Tabs: when only the active panel changed, preserve the existing DOM
                                // so nested chart/widget instances don't get torn down and redrawn.
                                if (!smartUpdated && widgetType === 'tabs') {
                                    const temp = document.createElement('div');
                                    temp.innerHTML = item.html;
                                    const nextGroup = temp.querySelector('wa-tab-group');
                                    const currentGroup = el.tagName && el.tagName.toLowerCase() === 'wa-tab-group'
                                        ? el
                                        : el.querySelector('wa-tab-group');

                                    if (currentGroup && nextGroup) {
                                        const currentPanels = Array.from(currentGroup.querySelectorAll(':scope > wa-tab-panel'));
                                        const nextPanels = Array.from(nextGroup.querySelectorAll(':scope > wa-tab-panel'));
                                        const currentTabs = Array.from(currentGroup.querySelectorAll(':scope > wa-tab[slot="nav"]'));
                                        const nextTabs = Array.from(nextGroup.querySelectorAll(':scope > wa-tab[slot="nav"]'));

                                        const samePanelMarkup = currentPanels.length === nextPanels.length && currentPanels.every((panel, index) => {
                                            const nextPanel = nextPanels[index];
                                            return !!nextPanel && panel.getAttribute('name') === nextPanel.getAttribute('name') && panel.innerHTML === nextPanel.innerHTML;
                                        });

                                        const sameTabMarkup = currentTabs.length === nextTabs.length && currentTabs.every((tab, index) => {
                                            const nextTab = nextTabs[index];
                                            return !!nextTab && tab.getAttribute('panel') === nextTab.getAttribute('panel') && tab.textContent === nextTab.textContent;
                                        });

                                        if (samePanelMarkup && sameTabMarkup) {
                                            const nextActive = nextGroup.getAttribute('active');
                                            if (nextActive) {
                                                currentGroup.setAttribute('active', nextActive);
                                                requestAnimationFrame(() => {
                                                    currentGroup.setAttribute('active', nextActive);
                                                    if (typeof currentGroup.updateActiveTab === 'function') {
                                                        currentGroup.updateActiveTab();
                                                    }
                                                });
                                            }
                                            smartUpdated = true;
                                        }
                                    }
                                }
                                
                                // Default: Full DOM replacement
                                if (!smartUpdated) {
                                    const agGridScrollState = window._vlCaptureAgGridScroll(el);
                                    purgePlotly(el);
                                    el.outerHTML = item.html;
                                    
                                    // [FIX] Force animation restart for page transitions
                                    // When replacing outerHTML with same ID, browser might optimize away the animation.
                                    // We force a reflow to ensure the fade-in plays.
                                    const newEl = document.getElementById(item.id);
                                    const revealGrid = window._vlHideAgGridDuringScrollRestore(newEl, agGridScrollState);
                                    window._vlRestoreAgGridScroll(newEl, agGridScrollState, revealGrid);
                                    if (isNavigation && newEl && newEl.classList.contains('page-container') && document.body.classList.contains('anim-soft')) {
                                        newEl.style.animation = 'none';
                                        void newEl.offsetWidth; // Trigger reflow
                                        newEl.style.animation = 'fade-in 0.3s ease-out';
                                    }
                                    
                                    // Execute scripts
                                    const temp = document.createElement('div');
                                    temp.innerHTML = item.html;
                                    temp.querySelectorAll('script').forEach(s => {
                                        const script = document.createElement('script');
                                        script.textContent = s.textContent;
                                        document.body.appendChild(script);
                                        script.remove();
                                    });
                                }
                            } else {
                                // If the element does not exist, it might be a new element that belongs inside a re-rendered parent container.
                                // It will automatically be created when its parent container replaces its innerHTML.
                                // But if we are in Lite mode or handled via generic layout, we might need to append it if it's top-level or absolute (like dialogs)
                                if (item.id.includes('dialog')) {
                                    debugLog("[WebSocket] Element not found for dialog, appending to body: " + item.id);
                                    const container = document.createElement('div');
                                    container.id = item.id;
                                    container.innerHTML = item.html;
                                    document.body.appendChild(container);

                                    // Trigger scripts for the newly appended dialog
                                    container.querySelectorAll('script').forEach(s => {
                                        const script = document.createElement('script');
                                        script.textContent = s.textContent;
                                        document.body.appendChild(script);
                                        script.remove();
                                    });
                                } else {
                                    debugLog("[WebSocket] Element not found for update, skipping appending to end: " + item.id);
                                }
                            }
                        });
                    };
                    
                    // Apply updates immediately (no View Transition).
                    // CSS fade-in on .page-container handles the smooth entrance.
                    applyUpdates(msg.payload);
                    window._vlApplyPartBridge(document);

                    // Preserve the user's viewport position for same-page reactive updates.
                    if (!isNavigation && window._pendingScrollRestore) {
                        const restore = window._pendingScrollRestore;
                        const restoreScroll = () => {
                            window.scrollTo(restore.x || 0, restore.y || 0);
                        };

                        requestAnimationFrame(() => {
                            restoreScroll();
                            requestAnimationFrame(() => {
                                restoreScroll();
                                setTimeout(restoreScroll, 80);
                            });
                        });

                        debugLog(`[Scroll] Restored viewport to y=${restore.y}px after reactive update`);
                        window._pendingScrollRestore = null;
                    }
                    
                    // Page scroll position management after navigation
                    if (isNavigation && window._pendingPageKey) {
                        const targetKey = window._pendingPageKey;
                        window._currentPageKey = targetKey;
                        window._pendingPageKey = null;
                        window._pendingScrollRestore = null;
                        
                        // Restore saved scroll position, or scroll to top for first visit
                        const savedScroll = window._pageScrollPositions[targetKey];
                        // Use requestAnimationFrame to ensure DOM is updated before scrolling
                        requestAnimationFrame(() => {
                            if (savedScroll !== undefined && savedScroll > 0) {
                                window.scrollTo(0, savedScroll);
                                debugLog(`[Navigation] Restored scroll ${savedScroll}px for page: ${targetKey}`);
                            } else {
                                window.scrollTo(0, 0);
                                debugLog(`[Navigation] Scroll to top for page: ${targetKey}`);
                            }
                        });
                    }
                    
                    // Re-highlight code blocks after DOM update
                    if (typeof hljs !== 'undefined') {
                        document.querySelectorAll('.violit-code-block pre code:not(.hljs)').forEach(function(block) {
                            hljs.highlightElement(block);
                        });
                    }
                } else if (msg.type === 'eval') {
                    const func = new Function(msg.code);
                    func();
                } else if (msg.type === 'interval_ctrl') {
                    // Server-initiated interval control (pause/resume/stop)
                    const ctrl = window._vlIntervals && window._vlIntervals[msg.id];
                    if (ctrl) {
                        if      (msg.action === 'pause')  ctrl.pause();
                        else if (msg.action === 'resume') ctrl.resume();
                        else if (msg.action === 'stop')   ctrl.stop();
                    }
                }
            };
        } else {
             // Lite Mode (HTMX) specifics
            document.addEventListener('DOMContentLoaded', () => {
                document.body.addEventListener('htmx:beforeSwap', function(evt) {
                    if (evt.detail.target) {
                        purgePlotly(evt.detail.target);
                    }
                });
                
                // Hot reload support for lite mode: poll server health
                let serverAlive = true;
                const checkServerHealth = () => {
                    // Add timestamp to prevent caching
                    const pollUrl = location.href.split('#')[0] + (location.href.indexOf('?') === -1 ? '?' : '&') + '_t=' + Date.now();
                    
                    fetch(pollUrl, { cache: 'no-store' })
                        .then(r => {
                            if (r.ok) {
                                if (!serverAlive) {
                                    debugLog("[Hot Reload] Server back online. Reloading...");
                                    document.body.style.opacity = '1'; // Restore opacity
                                    window.location.reload();
                                }
                                serverAlive = true;
                                // Ensure opacity is 1 if server is alive
                                document.body.style.opacity = '1';
                                document.body.style.pointerEvents = 'auto';
                            } else {
                                throw new Error('Server error');
                            }
                        })
                        .catch(() => {
                            if (serverAlive) {
                                debugLog("[Hot Reload] Server down. Waiting for restart...");
                                // Dim the page to indicate connection lost
                                document.body.style.transition = 'opacity 0.5s';
                                document.body.style.opacity = '0.5';
                                document.body.style.pointerEvents = 'none';
                            }
                            serverAlive = false;
                        });
                };
                setInterval(checkServerHealth, 2000);
            });
        }
        
        function toggleSidebar() {
            const sb = document.getElementById('sidebar');
            const main = document.getElementById('main');
            const isMobile = window.innerWidth <= 768;
            
            if (isMobile) {
                // Mobile: slide-over overlay mode
                const isOpen = sb.classList.contains('mobile-open');
                sb.classList.toggle('mobile-open');
                
                let backdrop = document.querySelector('.vl-sidebar-backdrop');
                if (!isOpen) {
                    // Opening
                    if (!backdrop) {
                        backdrop = document.createElement('div');
                        backdrop.className = 'vl-sidebar-backdrop';
                        backdrop.onclick = toggleSidebar;
                        document.body.appendChild(backdrop);
                    }
                    requestAnimationFrame(() => backdrop.classList.add('active'));
                    sb.style.display = 'flex'; // Ensure visible
                } else {
                    // Closing
                    if (backdrop) {
                        backdrop.classList.remove('active');
                        setTimeout(() => backdrop.remove(), 300);
                    }
                }
            } else {
                // Desktop: original collapse behavior
                sb.classList.toggle('collapsed');
                main.classList.toggle('sidebar-collapsed');
            }
        }
        
        // Auto-close sidebar on mobile after nav button click
        document.addEventListener('click', function(e) {
            const btn = e.target.closest('#sidebar wa-button');
            if (btn) {
                if (window.innerWidth <= 768) {
                    setTimeout(function() {
                        var sb = document.getElementById('sidebar');
                        if (sb && sb.classList.contains('mobile-open')) {
                            toggleSidebar();
                        }
                    }, 150);
                }
            }
        });

        function createToast(message, variant = 'primary', icon = 'circle-info') {
            const variantColors = { primary: '#0ea5e9', success: '#10b981', warning: '#f59e0b', danger: '#ef4444' };
            const toast = document.createElement('div');
            // Use CSS variables directly so theme changes are reflected automatically
            toast.style.cssText = `position: fixed; top: 20px; right: 20px; z-index: 10000; min-width: 300px; background: var(--wa-color-surface-raised, var(--vl-bg-card)); color: var(--vl-text); border: 1px solid var(--vl-border); border-left: 4px solid ${variantColors[variant]}; border-radius: 4px; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); display: flex; align-items: center; gap: 12px; opacity: 0; transform: translateX(400px); transition: all 0.3s;`;
            const normalizedIcon = window.__vlNormalizeIconName ? window.__vlNormalizeIconName(icon) : icon;
            const iconEl = document.createElement('wa-icon');
            iconEl.setAttribute('name', normalizedIcon || 'circle-info');
            iconEl.style.fontSize = '1rem';
            iconEl.style.color = variantColors[variant] || 'var(--vl-text-muted)';

            const messageEl = document.createElement('div');
            messageEl.style.flex = '1';
            messageEl.style.fontSize = '14px';
            messageEl.textContent = message;

            const closeButton = document.createElement('button');
            closeButton.type = 'button';
            closeButton.textContent = '\u00D7';
            closeButton.onclick = function() { toast.remove(); };
            closeButton.style.cssText = 'background: none; border: none; cursor: pointer; padding: 4px; color: var(--vl-text-muted); font-size: 20px;';

            toast.appendChild(iconEl);
            toast.appendChild(messageEl);
            toast.appendChild(closeButton);
            document.body.appendChild(toast);
            requestAnimationFrame(() => { toast.style.opacity = '1'; toast.style.transform = 'translateX(0)'; });
            setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(400px)'; setTimeout(() => toast.remove(), 300); }, 3300);
        }
        function createBalloons() {
            const emojis = ['\uD83C\uDF88', '\uD83C\uDF89', '\u2728', '\uD83C\uDF8A', '\uD83C\uDF81', '\uD83C\uDF8F'];
            for (let i = 0; i < 60; i++) {
                const b = document.createElement('div');
                b.className = 'balloon';
                b.textContent = emojis[Math.floor(Math.random() * emojis.length)];
                b.style.left = (Math.random() * 100) + 'vw';
                const startY = 100 + Math.random() * 20; // Start at 100vh-120vh (bottom)
                b.style.setProperty('--start-y', startY + 'vh');
                const duration = 4 + Math.random() * 3;
                b.style.setProperty('--duration', duration + 's');
                b.style.animationDelay = (Math.random() * 0.5) + 's';
                document.body.appendChild(b);
                setTimeout(() => b.remove(), (duration + 1) * 1000);
            }
        }
        function createSnow() {
            const emojis = ['\u2744\uFE0F', '\u2603\uFE0F', '\u2745', '\uD83E\uDDCA'];
            for (let i = 0; i < 50; i++) {
                const s = document.createElement('div');
                s.className = 'snowflake';
                s.textContent = emojis[Math.floor(Math.random() * emojis.length)];
                s.style.left = Math.random() * 100 + 'vw';
                const duration = 4 + Math.random() * 4;
                s.style.setProperty('--duration', duration + 's');
                s.style.animationDelay = Math.random() * 1.0 + 's';
                document.body.appendChild(s);
                setTimeout(() => s.remove(), (duration + 5) * 1000);
            }
        }
        
        // Restore state from URL Hash (or force Home if no hash)
        function restoreFromHash() {
            const getNavButtonPageKey = (btn) => {
                if (!btn) return null;
                const dataKey = btn.getAttribute('data-page-key');
                if (dataKey) return dataKey;
                const onclickAttr = btn.getAttribute('onclick') || '';
                const keyMatch = onclickAttr.match(/'(page_[^']+)'/);
                if (keyMatch) return keyMatch[1];
                const hxVals = btn.getAttribute('hx-vals') || '';
                const hxMatch = hxVals.match(/"value"\s*:\s*"(page_[^"]+)"/);
                return hxMatch ? hxMatch[1] : null;
            };

            const isNavButtonActive = (btn) => {
                if (!btn) return false;
                return btn.getAttribute('data-nav-active') === 'true'
                    || (btn.getAttribute('variant') === 'brand' && btn.getAttribute('appearance') === 'accent');
            };

            // Decode the URL hash, including encoded non-ASCII characters.
            let hash = window.location.hash.substring(1); // Remove #
            try {
                hash = decodeURIComponent(hash);
            } catch (e) {
                debugLog('Hash decode error:', e);
            }
            
            // If no hash, treat it as Home and avoid stale initial navigation state.
            if (!hash || hash === 'home') {
                debugLog('[Navigation] No hash found, forcing Home page');
                // Initialize current page key for scroll tracking
                window._currentPageKey = 'page_home';
                const tryClickHome = (attempts = 0) => {
                    if (attempts >= 20) return;
                    const navButtons = document.querySelectorAll('#sidebar wa-button');
                    if (navButtons.length > 0) {
                        const homeBtn = navButtons[0]; // First button is Home
                        const homeKey = getNavButtonPageKey(homeBtn);
                        if (homeKey) window._currentPageKey = homeKey;
                        if (!isNavButtonActive(homeBtn)) {
                            homeBtn.click();
                            debugLog('[Navigation] Clicked Home button');
                        }
                    } else {
                        setTimeout(() => tryClickHome(attempts + 1), 100);
                    }
                };
                tryClickHome();
                return;
            }
            
            const targetKey = 'page_' + hash;
            // Initialize current page key for scroll tracking
            window._currentPageKey = targetKey;
            debugLog(`[Navigation] Restoring from hash: "${hash}" (key: ${targetKey})`);
            
            const tryRestore = (attempts = 0) => {
                // Stop after 5 seconds
                if (attempts >= 50) {
                     console.warn(`[Navigation] Failed to restore hash "${hash}"`);
                     return;
                }
                
                const navButtons = document.querySelectorAll('#sidebar wa-button');
                if (navButtons.length === 0) {
                    setTimeout(() => tryRestore(attempts + 1), 100);
                    return;
                }
                
                for (let btn of navButtons) {
                    const btnKey = getNavButtonPageKey(btn);
                    if (btnKey === targetKey) {
                        debugLog(`[Navigation] Found target button for hash "${hash}". Clicking...`);
                        
                        // Check if already active to avoid redundant clicks
                        if (isNavButtonActive(btn)) {
                            debugLog('  - Already active, skipping click.');
                            return;
                        }
                        
                        btn.click();
                        return;
                    }
                }
                
                // Keep retrying in case the specific button hasn't rendered yet (unlikely if container exists)
                setTimeout(() => tryRestore(attempts + 1), 100);
            };
            
            tryRestore();
        }
        
        // Note: For ws mode, restoreFromHash is called from ws.onopen
        // For lite mode, call it on load:
        if (mode !== 'ws') {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => setTimeout(restoreFromHash, 200));
            } else {
                setTimeout(restoreFromHash, 200);
            }
        }
    </script>
</body>
</html>
"""
