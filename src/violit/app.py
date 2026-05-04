"""
Violit - A Streamlit-like framework with reactive components
Refactored with modular widget mixins
"""

import uuid
import sys
import threading
import time
import queue
import warnings
import secrets
import logging
from typing import Any, Callable, Dict, List, Optional, Set, Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
import inspect
import os
from pathlib import Path

from .app_launcher import AppLauncherMixin
from .app_runtime import AppRuntimeMixin
from .app_support import FileWatcher, IntervalHandle, Page, SidebarProxy, print_terminal_splash
from .context import session_ctx, view_ctx, rendering_ctx, fragment_ctx, app_instance_ref, layout_ctx, page_ctx, action_ctx, initial_render_ctx, pending_shared_views_ctx
from .theme import Theme
from .component import Component
from .engine import LiteEngine, WsEngine
from .state import APP_STATE_STORE, SHARED_STATE_LAST_TOUCH, SHARED_STATE_STORES, State, clear_view_scoped_dependencies, get_session_store, STATIC_STORE, VIEW_STORE, SESSION_STORE, unregister_component_from_scoped_trackers
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


class App(
    AppRuntimeMixin,
    AppLauncherMixin,
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
        self.boot_id = uuid.uuid4().hex
        self.app_title = title  # Renamed to avoid conflict with title() method
        self.theme_manager = Theme(theme)

        # ── Initialize ORM / DB ──────────────────────────────────────────────
        self.db = None
        if db is not None:
            from .db import ViolItDB, normalize_db_url
            self.db = ViolItDB(normalize_db_url(db), migrate=migrate)
        self._db_migrate_mode = migrate

        # ── Initialize Auth ────────────────────────────────────────────────
        self.auth = None
        from contextlib import asynccontextmanager

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            def _do():
                import pandas  # noqa: F401
                import plotly.graph_objects  # noqa: F401
            threading.Thread(target=_do, daemon=True).start()
            yield

        self.fastapi = FastAPI(lifespan=lifespan)
        self.fastapi.add_middleware(GZipMiddleware, minimum_size=1000)
        
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
        from .state import STATIC_STORE, VIEW_STORE, SESSION_STORE
        STATIC_STORE.clear() # Prevent leakage across hot reloads when forked on Linux
        VIEW_STORE.clear()
        SESSION_STORE.clear()
        APP_STATE_STORE['states'].clear()
        APP_STATE_STORE['tracker'].subscribers.clear()
        SHARED_STATE_STORES.clear()
        SHARED_STATE_LAST_TOUCH.clear()
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
        self._lite_stream_queues: Dict[tuple[str, str], queue.Queue] = {}
        self._lite_stream_lock = threading.Lock()
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

    def _resolve_state_name(self, key=None, *, stack_depth: int = 1) -> str:
        if key is not None:
            return key

        frame = inspect.currentframe()
        try:
            caller_frame = frame
            for _ in range(stack_depth):
                if caller_frame is None:
                    break
                caller_frame = caller_frame.f_back

            if caller_frame is None:
                self.state_count += 1
                return f"state_{self.state_count}"

            filename = os.path.basename(caller_frame.f_code.co_filename)
            lineno = caller_frame.f_lineno
            return f"state_{filename}_{lineno}"
        finally:
            del frame

    def state(self, default_value, key=None, *, scope: str = 'view', namespace: str | None = None) -> State:
        """Create a reactive state variable.

        Defaults to view-local state. Prefer the dedicated helpers for wider scopes:
        ``session_state()``, ``app_state()``, and ``shared_state()``.
        """
        name = self._resolve_state_name(key, stack_depth=1)
        return State(name, default_value, scope=scope, namespace=namespace)

    def view_state(self, default_value, key=None) -> State:
        """Create view-local state explicitly.

        This is an alias for ``state(...)`` and exists for symmetry with the
        wider-scope helpers.
        """
        name = self._resolve_state_name(key, stack_depth=2)
        return State(name, default_value, scope='view', namespace=None)

    def session_state(self, default_value, key=None) -> State:
        """Create browser-session state shared across tabs in one session."""
        name = self._resolve_state_name(key, stack_depth=2)
        return State(name, default_value, scope='session', namespace=None)

    def app_state(self, default_value, key=None) -> State:
        """Create process-local app-wide state shared across all users."""
        name = self._resolve_state_name(key, stack_depth=2)
        return State(name, default_value, scope='app', namespace=None)

    def shared_state(self, default_value, key=None, *, namespace: str) -> State:
        """Create namespace-scoped shared state for rooms, boards, and similar spaces."""
        name = self._resolve_state_name(key, stack_depth=2)
        return State(name, default_value, scope='shared', namespace=namespace)

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
        current_session_id = session_ctx.get()
        current_view_id = view_ctx.get()
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
                unregister_component_from_scoped_trackers(current_session_id, current_view_id, cid)
                
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
                unregister_component_from_scoped_trackers(current_session_id, current_view_id, cid)
        return res

    async def _flush_view_updates_async(self, session_id: str, current_view_id: str) -> None:
        if not session_id or not current_view_id:
            return

        session_token = session_ctx.set(session_id)
        view_token = view_ctx.set(current_view_id)
        try:
            dirty = self._get_dirty_rendered()
            if not dirty:
                return

            if self.ws_engine and self.ws_engine.has_socket(session_id, current_view_id):
                await self.ws_engine.push_updates(session_id, dirty, view_id=current_view_id)
                return

            if self.lite_engine:
                payload = self._build_lite_oob_payload(dirty)
                if payload:
                    self._enqueue_lite_stream_payload(session_id, payload, view_id=current_view_id)
        finally:
            view_ctx.reset(view_token)
            session_ctx.reset(session_token)

    async def _flush_scoped_state_views_async(
        self,
        view_keys: Set[tuple[str, str]],
        *,
        exclude_current: bool = False,
    ) -> None:
        current_key = (session_ctx.get(), view_ctx.get())
        for session_id, current_view_id in set(view_keys):
            if exclude_current and current_key == (session_id, current_view_id):
                continue
            await self._flush_view_updates_async(session_id, current_view_id)

    async def _flush_pending_scoped_state_updates_async(self, *, exclude_current: bool = False) -> None:
        pending_views = pending_shared_views_ctx.get()
        if not pending_views:
            return
        try:
            await self._flush_scoped_state_views_async(set(pending_views), exclude_current=exclude_current)
        finally:
            pending_views.clear()

    def _schedule_scoped_state_flush(
        self,
        view_keys: Set[tuple[str, str]],
        *,
        exclude_current: bool = False,
    ) -> None:
        if not view_keys:
            return

        coroutine = self._flush_scoped_state_views_async(set(view_keys), exclude_current=exclude_current)

        try:
            running_loop = asyncio.get_running_loop()
        except RuntimeError:
            running_loop = None

        if running_loop is not None:
            running_loop.create_task(coroutine)
            return

        main_loop = getattr(self, '_main_loop', None)
        if main_loop is not None and main_loop.is_running():
            asyncio.run_coroutine_threadsafe(coroutine, main_loop)
            return

        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(coroutine)
        finally:
            loop.close()

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
        store = get_session_store()
        interval_callbacks = store.setdefault('interval_callbacks', {})
        interval_count = store.get('_interval_count', 0)
        interval_id = f"__vl_interval_{interval_count}__"
        store['_interval_count'] = interval_count + 1

        initial_state = 'running' if autostart else 'paused'

        interval_callbacks[interval_id] = {
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
        """Send interval control message to the current active view."""
        if not self.ws_engine:
            return

        sid = session_ctx.get()
        current_view_id = view_ctx.get()
        if not sid or not current_view_id:
            return

        async def _push():
            ws_sock = self.ws_engine.get_socket(sid, current_view_id)
            if ws_sock is None:
                return
            try:
                await ws_sock.send_json({
                    'type': 'interval_ctrl',
                    'id': interval_id,
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
        flush_interval: float = 0.2,
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
            flush_interval: Seconds between live UI flushes while the task runs
        
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
            flush_interval=flush_interval,
        )

    # End Background Task API

    def setup_auth(
        self,
        user_model,
        username_field: str = "username",
        password_field: str = "hashed_password",
        role_field: str = "role",
        login_page: str = "Login",
        require_auth: bool = False,
    ):
        """
        Initialize the Auth system.

        Parameters
        ----------
        user_model : SQLModel class
            The User model.
        username_field : str
            The column name for the username (default: 'username').
        password_field : str
            The column name for the hashed password (default: 'hashed_password').
        role_field : str
            The column name for the role (default: 'role').
        login_page : str
            The title of the page to redirect to when unauthenticated access occurs (default: 'Login').
        require_auth : bool
            If True, automatically protects all pages.

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
                            # ── Check Auth Access ───────────────────────
                            if self.app.auth is not None:
                                if not self.app.auth.check_page_access(p):
                                    # Unauthenticated / Insufficient role: return empty container
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



