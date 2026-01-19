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
from typing import Any, Callable, Dict, List, Optional, Set, Union
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import inspect
import uvicorn
import webview
import pandas as pd
import os
import subprocess
from pathlib import Path
import plotly.graph_objects as go
import plotly.io as pio

from .context import session_ctx, rendering_ctx, fragment_ctx, app_instance_ref, layout_ctx
from .theme import Theme
from .component import Component
from .engine import LiteEngine, WsEngine
from .state import State, get_session_store
from .broadcast import Broadcaster

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
    """Simple file watcher to detect changes"""
    def __init__(self, debug_mode=False):
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
        """Scan current directory for py files and their mtimes"""
        for p in Path(".").rglob("*.py"):
            if self._is_ignored(p): continue
            try:
                # Use absolute path to ensure consistency
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
        for p in list(Path(".").rglob("*.py")): 
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
    def __init__(self, entry_point, title=None, icon=None, url_path=None):
        self.entry_point = entry_point
        self.title = title or entry_point.__name__.replace("_", " ").title()
        self.icon = icon
        self.url_path = url_path or self.title.lower().replace(" ", "-")
        self.key = f"page_{self.url_path}"

    def run(self):
        self.entry_point()


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
    
    def __init__(self, mode='ws', title="Violit App", theme='light', allow_selection=True, animation_mode='soft', icon=None, width=1024, height=768, on_top=True, container_width='800px'):
        self.mode = mode
        self.app_title = title  # Renamed to avoid conflict with title() method
        self.theme_manager = Theme(theme)
        self.fastapi = FastAPI()
        
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
        
        # Container width: numeric (px), percentage (%), or 'none' (full width)
        if container_width == 'none' or container_width == '100%':
            self.container_max_width = 'none'
        elif isinstance(container_width, int):
            self.container_max_width = f'{container_width}px'
        else:
            self.container_max_width = container_width

        
        # Static definitions
        self.static_builders: Dict[str, Callable] = {}
        self.static_order: List[str] = []
        self.static_sidebar_order: List[str] = []
        self.static_actions: Dict[str, Callable] = {}
        self.static_fragments: Dict[str, Callable] = {}
        self.static_fragment_components: Dict[str, List[Any]] = {}
        
        self.state_count = 0
        self._fragments: Dict[str, Callable] = {}
        
        # Broadcasting System
        self.broadcaster = Broadcaster(self)
        self._fragment_count = 0
        
        # Internal theme/settings state
        self._theme_state = self.state(self.theme_manager.mode)
        self._selection_state = self.state(allow_selection)
        self._animation_state = self.state(animation_mode)
        
        self.ws_engine = WsEngine() if mode == 'ws' else None
        self.lite_engine = LiteEngine() if mode == 'lite' else None
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

    def state(self, default_value, key=None) -> State:
        """Create a reactive state variable"""
        if key is None:
            name = f"state_{self.state_count}"
            self.state_count += 1
        else:
            name = key
        return State(name, default_value)

    def _get_next_cid(self, prefix: str) -> str:
        """Generate next component ID"""
        store = get_session_store()
        cid = f"{prefix}_{store['component_count']}"
        store['component_count'] += 1
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
        
        Use as context manager for reactive if/for loops
        """
        if func is not None:
            # Decorator mode - deprecated
            warnings.warn(
                "@app.reactivity decorator is deprecated and will be removed in a future version. "
                "Please use 'with app.reactivity():' context manager instead.",
                DeprecationWarning,
                stacklevel=2
            )
            return self.fragment(func)
        
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
                
                # Register the reactivity scope as a component
                self._register_component(ctx_self.fid, reactivity_builder)
        
        return ReactivityContext(self)

    def _render_all(self):
        """Render all components"""
        store = get_session_store()
        
        main_html = []
        sidebar_html = []

        def render_cids(cids, target_list):
            for cid in cids:
                builder = store['builders'].get(cid) or self.static_builders.get(cid)
                if builder:
                    target_list.append(builder().render())

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
        dirty_states = store.get('dirty_states', set())
        aff = set()
        for s in dirty_states: aff.update(store['tracker'].get_dirty_components(s))
        store['dirty_states'] = set()
        
        res = []
        for cid in aff:
            builder = store['builders'].get(cid) or self.static_builders.get(cid)
            if builder:
                res.append(builder())
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
                </script>
            '''
            return Component("div", id=cid, style="display:none", content=script_content)
        self._register_component(cid, builder)

    def navigation(self, pages: List[Any], position="sidebar", auto_run=True):
        """Create multi-page navigation"""
        # Normalize pages
        final_pages = []
        for p in pages:
            if isinstance(p, Page): final_pages.append(p)
            elif callable(p): final_pages.append(Page(p))
        
        if not final_pages: return None
        
        # Singleton state for navigation
        current_page_key_state = self.state(final_pages[0].key, key="__nav_selection__")
        
        # Navigation Menu Builder
        cid = self._get_next_cid("nav_menu")
        nav_cid = cid  # Capture for use in nav_action closure
        def nav_builder():
            token = rendering_ctx.set(cid)
            curr = current_page_key_state.value
            
            items = []
            for p in final_pages:
                is_active = p.key == curr
                click_attr = ""
                if self.mode == 'lite':
                    # Lite mode: update hash and HTMX post
                    page_hash = p.key.replace("page_", "")
                    click_attr = f'onclick="window.location.hash = \'{page_hash}\'" hx-post="/action/{cid}" hx-vals=\'{{"value": "{p.key}"}}\' hx-target="#{cid}" hx-swap="outerHTML"'  
                else:
                    # WebSocket mode (including native)
                    click_attr = f'onclick="window.sendAction(\'{cid}\', \'{p.key}\')"'
                
                # Styling for active/inactive nav items
                if is_active:
                    style = "width: 100%; justify-content: start; --sl-color-primary-500: var(--sl-primary); --sl-color-primary-600: var(--sl-primary);"
                    variant = "primary"
                else:
                    style = "width: 100%; justify-content: start; --sl-color-neutral-700: var(--sl-text);"
                    variant = "text"
                
                icon_html = f'<sl-icon name="{p.icon}" slot="prefix"></sl-icon> ' if p.icon else ""
                items.append(f'<sl-button style="{style}" variant="{variant}" {click_attr}>{icon_html}{p.title}</sl-button>')
            
            rendering_ctx.reset(token)
            return Component("div", id=cid, content="<br>".join(items), class_="nav-container")
            
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
            def __init__(self, app, page_state, pages_map):
                self.app = app
                self.state = page_state
                self.pages_map = pages_map
            
            def run(self):
                # Progressive Mode: Register page renderer as a regular component
                # The builder function reads the navigation state, enabling reactivity
                # WITHOUT wrapping the entire page function in a fragment
                cid = self.app._get_next_cid("page_renderer")
                
                def page_builder():
                    # Read the navigation state here - this creates the dependency
                    token = rendering_ctx.set(cid)
                    try:
                        key = self.state.value
                        
                        # Execute the current page function
                        p = self.pages_map.get(key)
                        if p:
                            # Collect components from the page
                            store = get_session_store()
                            # Clear previous dynamic order for this page render
                            previous_order = store['order'].copy()
                            previous_fragments = {k: v.copy() for k, v in store['fragment_components'].items()}
                            store['order'] = []
                            store['fragment_components'] = {}  # Clear fragments to prevent duplicates
                            
                            try:
                                # Execute page function
                                # CRITICAL: Execute inside rendering_ctx so any state access registers dependency
                                p.entry_point()
                                
                                # Render all components from this page
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
                        rendering_ctx.reset(token)
                
                # Register the page renderer as a regular component
                self.app._register_component(cid, page_builder)


        page_runner = PageRunner(self, current_page_key_state, {p.key: p for p in final_pages})
        
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
            # Note: _theme_state, _selection_state, _animation_state and their updaters
            # are already initialized in __init__, no need to re-initialize here
            
            main_c, sidebar_c = self._render_all()
            store = get_session_store()
            t = store['theme']
            
            sidebar_style = "" if (sidebar_c or self.static_sidebar_order) else "display: none;"
            
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
            
            html = HTML_TEMPLATE.replace("%CONTENT%", main_c).replace("%SIDEBAR_CONTENT%", sidebar_c).replace("%SIDEBAR_STYLE%", sidebar_style).replace("%MODE%", self.mode).replace("%TITLE%", self.app_title).replace("%THEME_CLASS%", t.theme_class).replace("%CSS_VARS%", t.to_css_vars()).replace("%SPLASH%", self._splash_html if self.show_splash else "").replace("%CONTAINER_MAX_WIDTH%", self.container_max_width).replace("%CSRF_SCRIPT%", csrf_script).replace("%DEBUG_SCRIPT%", debug_script)
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
                act(v) if v is not None else act()
                
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
            
            self.debug_print(f"[WEBSOCKET] Session: {sid[:8]}...")
            
            # Set session context (outside while loop - very important!)
            t = session_ctx.set(sid)
            self.ws_engine.sockets[sid] = ws
            
            # Message processing function
            async def process_message(data):
                if data.get('type') != 'click':
                    return
                
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
                
                if act:
                    store['eval_queue'] = []
                    self.debug_print(f"  Executing action for CID: {cid}...")
                    act(v) if v is not None else act()
                    self.debug_print(f"  Action executed")
                    
                    for code in store.get('eval_queue', []):
                        await self.ws_engine.push_eval(sid, code)
                    store['eval_queue'] = []
                    
                    dirty = self._get_dirty_rendered()
                    self.debug_print(f"  Dirty components: {len(dirty)} ({[c.id for c in dirty]})")
                    
                    # Send all dirty components via WebSocket
                    if dirty:
                        self.debug_print(f"  Sending {len(dirty)} updates via WebSocket...")
                        await self.ws_engine.push_updates(sid, dirty)
                        self.debug_print(f"  [OK] Updates sent successfully")
                    else:
                        self.debug_print(f"  [!] No dirty components found - nothing to update")
            
            try:
                # Message processing loop
                while True:
                    data = await ws.receive_json()
                    await process_message(data)
            except WebSocketDisconnect:
                if sid and sid in self.ws_engine.sockets: 
                    del self.ws_engine.sockets[sid]
                    self.debug_print(f"[WEBSOCKET] Disconnected: {sid[:8]}...")
            finally:
                if t is not None:
                    session_ctx.reset(t)

    def _run_web_reload(self, args):
        """Run with hot reload in web mode (process restart)"""
        self.debug_print(f"[HOT RELOAD] Watching {os.getcwd()}...")
        
        iteration = 0
        while True:
            iteration += 1
            # Prepare environment
            env = os.environ.copy()
            env["VIOLIT_WORKER"] = "1"
            
            # Start worker
            self.debug_print(f"\n[Web Reload] Starting server (iteration {iteration})...", flush=True)
            p = subprocess.Popen([sys.executable] + sys.argv, env=env)
            
            # Watch for changes
            watcher = FileWatcher(debug_mode=self.debug_mode)
            intentional_restart = False
            
            try:
                while p.poll() is None:
                    if watcher.check():
                        self.debug_print("\n[Web Reload] 🔄 Reloading server...", flush=True)
                        intentional_restart = True
                        p.terminate()
                        try:
                            p.wait(timeout=2)
                            self.debug_print("[Web Reload] ✓ Server stopped gracefully", flush=True)
                        except subprocess.TimeoutExpired:
                            self.debug_print("[Web Reload] WARNING: Force killing server...", flush=True)
                            p.kill()
                            p.wait()
                        break
                    time.sleep(0.5)
            except KeyboardInterrupt:
                p.terminate()
                sys.exit(0)
            
            # If it was an intentional restart, wait a bit so browser can detect server is down
            if intentional_restart:
                time.sleep(1.5)  # Give browser time to detect server is down (increased for reliability)
                continue
            
            # If process exited unexpectedly (crashed), wait for file change
            if p.returncode is not None:
                self.debug_print("[Web Reload] WARNING: Server exited unexpectedly. Waiting for file changes...", flush=True)
                while not watcher.check():
                    time.sleep(0.5)
                self.debug_print("[Web Reload] Reloading after crash...", flush=True)

    def _run_native_reload(self, args):
        """Run with hot reload in desktop mode"""
        # Generate security token for native mode
        self.native_token = secrets.token_urlsafe(32)
        self.is_native_mode = True
        
        self.debug_print(f"[HOT RELOAD] Desktop mode - Watching {os.getcwd()}...")
        
        # Shared state for the server process
        server_process = [None]
        should_exit = [False]
        
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
                server_process[0] = subprocess.Popen(
                    [sys.executable] + sys.argv, 
                    env=env,
                    stdout=subprocess.PIPE if iteration > 1 else None,
                    stderr=subprocess.STDOUT if iteration > 1 else None
                )
                
                # Give server time to start
                time.sleep(0.3)
                
                watcher = FileWatcher(debug_mode=self.debug_mode)
                
                # Watch loop
                intentional_restart = False
                while server_process[0].poll() is None and not should_exit[0]:
                    if watcher.check():
                        self.debug_print("\n[Server Manager] 🔄 Reloading server...", flush=True)
                        intentional_restart = True
                        server_process[0].terminate()
                        try:
                            server_process[0].wait(timeout=2)
                            self.debug_print("[Server Manager] ✓ Server stopped gracefully", flush=True)
                        except subprocess.TimeoutExpired:
                            self.debug_print("[Server Manager] WARNING: Force killing server...", flush=True)
                            server_process[0].kill()
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
            'on_top': self.on_top
        }
        
        # Pass icon to start (for non-WinForms backends)
        start_args = {}
        sig_start = inspect.signature(webview.start)
        if 'icon' in sig_start.parameters and self.app_icon:
            start_args['icon'] = self.app_icon

        webview.create_window(self.app_title, f"http://127.0.0.1:{args.port}?_native_token={self.native_token}", **win_args)
        webview.start(**start_args)
        
        # Cleanup
        should_exit[0] = True
        if server_process[0]:
            try:
                server_process[0].terminate()
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

    def run(self):
        """Run the application"""
        p = argparse.ArgumentParser()
        p.add_argument("--native", action="store_true")
        p.add_argument("--nosplash", action="store_true", help="Disable splash screen")
        p.add_argument("--reload", action="store_true", help="Enable hot reload")
        p.add_argument("--lite", action="store_true", help="Use Lite mode (HTMX)")
        p.add_argument("--debug", action="store_true", help="Enable developer tools (native mode)")
        p.add_argument("--port", type=int, default=8000)
        args, _ = p.parse_known_args()

        if args.lite:
            self.mode = "lite"
            # Also create lite engine if not already created
            if self.lite_engine is None:
                from .engine import LiteEngine
                self.lite_engine = LiteEngine()

        # Handle internal env var to force "Server Only" mode (for native reload)
        if os.environ.get("VIOLIT_SERVER_ONLY"):
            args.native = False
            
        # Hot Reload Manager Logic
        if args.reload and not os.environ.get("VIOLIT_WORKER"):
            if args.native:
                self._run_native_reload(args)
            else:
                self._run_web_reload(args)
            return
        
        self.show_splash = not args.nosplash
        if self.show_splash:
            self._splash_html = """
            <div id="splash" style="position:fixed;top:0;left:0;width:100%;height:100%;background:var(--sl-bg);z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;transition:opacity 0.4s ease;">
                <sl-spinner style="font-size: 3rem; --indicator-color: var(--sl-primary); margin-bottom: 1rem;"></sl-spinner>
                <div style="font-size:1.5rem;font-weight:600;color:var(--sl-text);" class="gradient-text">Loading...</div>
            </div>
            <script>
            window.addEventListener('load', ()=>{ 
                setTimeout(()=>{
                    const s=document.getElementById('splash');
                    if(s){
                        s.style.opacity=0;
                        setTimeout(()=>s.remove(), 400);
                    }
                }, 800); 
            });
            </script>
            """
        
        if args.native:
            # Generate security token for native mode
            self.native_token = secrets.token_urlsafe(32)
            self.is_native_mode = True
            
            # Disable CSRF in native mode (local app security)
            self.csrf_enabled = False
            print("[SECURITY] CSRF protection disabled (native mode)")
            
            # Use a shared flag to signal server shutdown
            server_shutdown = threading.Event()
            
            def srv(): 
                # Run uvicorn in a way we can control or just let it die with daemon
                # Since we use daemon=True, it should die when main thread dies.
                # However, sometimes keeping the main thread alive for webview.start() 
                # might cause issues if not cleaned up properly.
                # We'll stick to daemon=True but force exit after webview.start returns.
                uvicorn.run(self.fastapi, host="127.0.0.1", port=args.port, log_level="warning")
            
            t = threading.Thread(target=srv, daemon=True)
            t.start()
            
            time.sleep(1)
            
            # Patch webview to use custom icon (Windows)
            self._patch_webview_icon()
            
            # Start WebView - This blocks until window is closed
            win_args = {
                'text_select': True, 
                'width': self.width, 
                'height': self.height, 
                'on_top': self.on_top
            }
            
            # Pass icon and debug mode to start (for non-WinForms backends)
            start_args = {}
            sig_start = inspect.signature(webview.start)
            
            # Enable developer tools (when --debug flag is used)
            if args.debug:
                start_args['debug'] = True
                print("🔍 Debug mode enabled: Press F12 or Ctrl+Shift+I to open developer tools")
            
            if 'icon' in sig_start.parameters and self.app_icon:
                start_args['icon'] = self.app_icon

            # Add native token to URL for initial access
            webview.create_window(self.app_title, f"http://127.0.0.1:{args.port}?_native_token={self.native_token}", **win_args)
            webview.start(**start_args)
            
            # Force exit after window closes to kill the uvicorn thread immediately
            print("App closed. Exiting...")
            os._exit(0)
        else:
            uvicorn.run(self.fastapi, host="0.0.0.0", port=args.port)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html class="%THEME_CLASS%">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="htmx-config" content='{"defaultSwapDelay":0,"defaultSettleDelay":0}'>
    <title>%TITLE%</title>
    %CSRF_SCRIPT%
    %DEBUG_SCRIPT%
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.12.0/cdn/themes/light.css" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.12.0/cdn/themes/dark.css" />
    <script type="module" src="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.12.0/cdn/shoelace-autoloader.js"></script>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script src="https://cdn.jsdelivr.net/npm/ag-grid-community@31.0.0/dist/ag-grid-community.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root { 
            %CSS_VARS%
        }
        sl-alert { --sl-color-primary-500: var(--sl-primary); --sl-color-primary-600: var(--sl-primary); }
        sl-alert::part(base) { border: 1px solid var(--sl-border); }
        
        sl-button {
             --sl-color-primary-500: var(--sl-primary);
             --sl-color-primary-600: color-mix(in srgb, var(--sl-primary), black 10%);
        }
        body { margin: 0; background: var(--sl-bg); color: var(--sl-text); font-family: 'Inter', sans-serif; min-height: 100vh; transition: background 0.3s, color 0.3s; }
        
        /* Soft Animation Mode - Only for sidebar and page transitions */
        body.anim-soft #sidebar { transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), padding 0.3s ease, opacity 0.3s ease; }
        body.anim-soft .page-container { animation: fade-in 0.3s ease-out; }
        
        /* Hard Animation Mode */
        body.anim-hard *, body.anim-hard ::part(base) { transition: none !important; animation: none !important; }
        
        #root { display: flex; width: 100%; min-height: 100vh; }
        #sidebar { 
            width: 300px; 
            background: var(--sl-bg-card); 
            border-right: 1px solid var(--sl-border); 
            padding: 2rem 1rem; 
            display: flex; 
            flex-direction: column; 
            gap: 1rem; 
            flex-shrink: 0; 
            overflow-y: auto; 
            overflow-x: hidden; 
            white-space: nowrap; 
            position: sticky; 
            top: 0; 
            height: 100vh;
        }
        #sidebar.collapsed { width: 0; padding: 2rem 0; border-right: none; opacity: 0; }
        
        #main { 
            flex: 1; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            padding: 0 1.5rem 3rem 1.5rem; 
            transition: padding 0.3s ease;
        }
        #header { width: 100%; max-width: %CONTAINER_MAX_WIDTH%; padding: 1rem 0; display: flex; align-items: center; }
        #app { width: 100%; max-width: %CONTAINER_MAX_WIDTH%; display: flex; flex-direction: column; gap: 1.5rem; }
        
        .fragment { display: flex; flex-direction: column; gap: 1.25rem; width: 100%; }
        .page-container { display: flex; flex-direction: column; gap: 1rem; width: 100%; }
        .card { background: var(--sl-bg-card); border: 1px solid var(--sl-border); padding: 1.5rem; border-radius: var(--sl-radius); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 0.5rem; }
        
        /* Widget spacing - natural breathing room */
        .page-container > div { margin-bottom: 0.5rem; }
        
        /* Headings need more space above to separate sections */
        h1, h2, h3 { font-weight: 600; margin: 0; }
        h1 { font-size: 2.25rem; line-height: 1.2; margin-bottom: 1rem; }
        h2 { font-size: 1.5rem; line-height: 1.3; margin-top: 1.5rem; margin-bottom: 0.75rem; }
        h3 { font-size: 1.25rem; line-height: 1.4; margin-top: 1.25rem; margin-bottom: 0.5rem; }
        .page-container > h1:first-child, .page-container > h2:first-child, .page-container > h3:first-child,
        h1:first-child, h2:first-child, h3:first-child { margin-top: 0; }
        
        /* Shoelace component spacing */
        sl-input, sl-select, sl-textarea, sl-range, sl-checkbox, sl-switch, sl-radio-group, sl-color-picker {
            display: block;
            margin-bottom: 1rem;
        }
        sl-alert {
            display: block;
            margin-bottom: 1.25rem;
        }
        sl-button {
            margin-top: 0.25rem;
            margin-bottom: 0.5rem;
        }
        sl-divider, .divider { 
            --color: var(--sl-border); 
            margin: 1.5rem 0; 
            width: 100%; 
        }
        
        /* Column layouts */
        .columns { display: flex; gap: 1rem; width: 100%; margin-bottom: 0.5rem; }
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
        .violit-list-container sl-card {
            width: 100%;
        }
        
        .gradient-text { background: linear-gradient(to right, var(--sl-primary), var(--sl-secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .text-muted { color: var(--sl-text-muted); }
        .metric-label { color: var(--sl-text-muted); font-size: 0.875rem; margin-bottom: 0.25rem; }
        .metric-value { font-size: 2rem; font-weight: 600; }
        .no-select { -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; }
        
        @keyframes fade-in {
            from { opacity: 0; transform: translateY(10px); filter: blur(4px); }
            to { opacity: 1; transform: translateY(0); filter: blur(0); }
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
    </style>
    <script>
        const mode = "%MODE%";
        
        // Debug logging helper
        const debugLog = (...args) => {
            if (window._debug_mode) {
                console.log(...args);
            }
        };
        
        // [LOCK] HTMX에 CSRF 토큰 자동 추가 (Lite Mode)
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

        if (mode === 'ws') {
            // [FIX] Pre-define sendAction with queue to handle clicks before WebSocket connects
            // Use window properties for debugging access
            window._wsReady = false;
            window._actionQueue = [];
            window._ws = null;
            
            // Define sendAction IMMEDIATELY (before WebSocket connection)
            window.sendAction = (cid, val) => {
                debugLog(`[sendAction] Called with cid=${cid}, val=${val}`);
                
                const payload = {
                    type: 'click', 
                    id: cid, 
                    value: val
                };
                
                // CSRF 토큰 추가
                if (window._csrf_token) {
                    payload._csrf_token = window._csrf_token;
                }
                
                // [SECURE] Native 토큰 추가 (pywebview에서 필요)
                const urlParams = new URLSearchParams(window.location.search);
                const nativeToken = urlParams.get('_native_token');
                if (nativeToken) {
                    payload._native_token = nativeToken;
                }
                
                // Check if this is a navigation menu click (nav_menu_X)
                if (cid.startsWith('nav_menu')) {
                    // Update URL hash to reflect current page
                    // val is "page_reactive-logic", we make it #reactive-logic
                    const pageName = val.replace('page_', '');
                    window.location.hash = pageName;
                    debugLog(`🔗 Updated Hash: #${pageName}`);
                }
                
                // Queue action if WebSocket not ready, otherwise send immediately
                if (!window._wsReady || !window._ws) {
                    debugLog(`⏳ WebSocket not ready (wsReady=${window._wsReady}, ws=${!!window._ws}), queueing action: ${cid}`);
                    window._actionQueue.push(payload);
                } else {
                    debugLog(`✅ Sending action to server: ${cid}`);
                    window._ws.send(JSON.stringify(payload));
                }
            };
            
            // Now connect WebSocket
            window._ws = new WebSocket((location.protocol === 'https:' ? 'wss:' : 'ws:') + "//" + location.host + "/ws");
            
            // Auto-reconnect/reload logic
            window._ws.onclose = () => {
                window._wsReady = false;
                debugLog("🔌 Connection lost. Auto-reloading...");

                const checkServer = () => {
                   fetch(location.href)
                       .then(r => {
                           if(r.ok) {
                               debugLog("✓ Server back online. Reloading...");
                               window.location.reload();
                           } else {
                               setTimeout(checkServer, 300);
                           }
                       })
                       .catch(() => setTimeout(checkServer, 300));
                };
                setTimeout(checkServer, 300);
            };
            
            // CRITICAL: Restore from hash ONLY after WebSocket is connected
            window._ws.onopen = () => {
                debugLog("✅ [WebSocket] Connected successfully!");
                window._wsReady = true;
                
                // Process queued actions
                if (window._actionQueue.length > 0) {
                    debugLog(`📤 Processing ${window._actionQueue.length} queued action(s)...`);
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
                debugLog("❌ WebSocket error:", error);
            };

            window._ws.onmessage = (e) => {
                debugLog("[WebSocket] Message received");
                const msg = JSON.parse(e.data);
                if(msg.type === 'update') {
                    // Separate page transitions from regular updates
                    const pageUpdates = [];
                    const regularUpdates = [];
                    
                    msg.payload.forEach(item => {
                        // Only page_renderer gets smooth transition
                        if (item.id.startsWith('page_renderer')) {
                            pageUpdates.push(item);
                        } else {
                            regularUpdates.push(item);
                        }
                    });
                    
                    // Regular updates: apply immediately without animation
                    regularUpdates.forEach(item => {
                        const el = document.getElementById(item.id);
                        
                        // Focus Guard: Skip update if element is focused input to prevent interrupting typing
                        if (document.activeElement && el) {
                             const isSelfOrChild = document.activeElement.id === item.id || el.contains(document.activeElement);
                             const isShadowChild = document.activeElement.closest && document.activeElement.closest(`#${item.id}`);
                             
                             if (isSelfOrChild || isShadowChild) {
                                 // Check if it's actually an input that needs protection
                                 const tag = document.activeElement.tagName.toLowerCase();
                                 const isInput = tag === 'input' || tag === 'textarea' || tag.startsWith('sl-input') || tag.startsWith('sl-textarea');
                                 
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
                                const newCheckbox = temp.querySelector('sl-checkbox, sl-switch');
                                
                                if (newCheckbox) {
                                    // Find the actual checkbox element (may be direct or nested)
                                    const checkboxEl = el.tagName && (el.tagName.toLowerCase() === 'sl-checkbox' || el.tagName.toLowerCase() === 'sl-switch')
                                        ? el 
                                        : el.querySelector('sl-checkbox, sl-switch');
                                    
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
                            
                            // Data Editor: Update AG Grid data only
                            if (widgetType === 'data' && item.id.includes('editor')) {
                                // item.id is like "data_editor_xxx_wrapper", extract base cid
                                const baseCid = item.id.replace('_wrapper', '');
                                const gridApi = window['gridApi_' + baseCid];
                                if (gridApi) {
                                    // Extract rowData from new HTML
                                    const match = item.html.match(/rowData:\s*(\[.*?\])/s);
                                    if (match) {
                                        try {
                                            const newData = JSON.parse(match[1]);
                                            gridApi.setRowData(newData);
                                            smartUpdated = true;
                                        } catch (e) {
                                            console.error('Failed to parse AG Grid data:', e);
                                        }
                                    }
                                }
                            }
                            
                            // Default: Full DOM replacement
                            if (!smartUpdated) {
                                purgePlotly(el);
                                el.outerHTML = item.html;
                                
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
                        }
                    });
                    
                    // Page updates: use View Transitions if available
                    if (pageUpdates.length > 0) {
                        const updatePages = () => {
                            pageUpdates.forEach(item => {
                                const el = document.getElementById(item.id);
                                if(el) {
                                    purgePlotly(el);
                                    el.outerHTML = item.html;
                                    
                                    const temp = document.createElement('div');
                                    temp.innerHTML = item.html;
                                    temp.querySelectorAll('script').forEach(s => {
                                        const script = document.createElement('script');
                                        script.textContent = s.textContent;
                                        document.body.appendChild(script);
                                        script.remove();
                                    });
                                }
                            });
                        };
                        
                        if (document.body.classList.contains('anim-soft') && document.startViewTransition) {
                            document.startViewTransition(() => updatePages());
                        } else {
                            updatePages();
                        }
                    }
                } else if (msg.type === 'eval') {
                    const func = new Function(msg.code);
                    func();
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
                                    debugLog("✓ Server back online. Reloading...");
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
                                debugLog("🔌 Server down. Waiting for restart...");
                                // Dim the page to indicate connection lost
                                document.body.style.transition = 'opacity 0.5s';
                                document.body.style.opacity = '0.5';
                                document.body.style.pointerEvents = 'none';
                            }
                            serverAlive = false;
                        });
                };
                setInterval(checkServerHealth, 200);
            });
        }
        
        function toggleSidebar() {
            const sb = document.getElementById('sidebar');
            sb.classList.toggle('collapsed');
        }
        function createToast(message, variant = 'primary', icon = 'info-circle') {
            const variantColors = { primary: '#0ea5e9', success: '#10b981', warning: '#f59e0b', danger: '#ef4444' };
            const toast = document.createElement('div');
            // Use CSS variables directly so theme changes are reflected automatically
            toast.style.cssText = `position: fixed; top: 20px; right: 20px; z-index: 10000; min-width: 300px; background: var(--sl-panel-background-color, var(--sl-bg-card)); color: var(--sl-text); border: 1px solid var(--sl-border); border-left: 4px solid ${variantColors[variant]}; border-radius: 4px; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); display: flex; align-items: center; gap: 12px; opacity: 0; transform: translateX(400px); transition: all 0.3s;`;
            toast.innerHTML = `<div style="flex: 1; font-size: 14px;">${message}</div><button onclick="this.parentElement.remove()" style="background: none; border: none; cursor: pointer; padding: 4px; color: var(--sl-text-muted); font-size: 20px;">&times;</button>`;
            document.body.appendChild(toast);
            requestAnimationFrame(() => { toast.style.opacity = '1'; toast.style.transform = 'translateX(0)'; });
            setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(400px)'; setTimeout(() => toast.remove(), 300); }, 3300);
        }
        function createBalloons() {
            const emojis = ['🎈', '🎈', '🎈', '✨', '🎈', '🎈'];
            for (let i = 0; i < 60; i++) {
                const b = document.createElement('div');
                b.className = 'balloon';
                b.textContent = emojis[Math.floor(Math.random() * emojis.length)];
                b.style.left = Math.random() * 100 + 'vw';
                const startY = 10;
                b.style.setProperty('--start-y', startY + 'vh');
                const duration = 3 + Math.random() * 3;
                b.style.setProperty('--duration', duration + 's');
                b.style.animationDelay = Math.random() * 0.2 + 's';
                document.body.appendChild(b);
                setTimeout(() => b.remove(), (duration + 1) * 1000);
            }
        }
        function createSnow() {
            const emojis = ['❄️', '❅', '❆', '❄️'];
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
            // 🔄 URL 해시 디코딩 (한글 등 인코딩된 문자 처리)
            let hash = window.location.hash.substring(1); // Remove #
            try {
                hash = decodeURIComponent(hash);
            } catch (e) {
                debugLog('Hash decode error:', e);
            }
            
            // If no hash, force navigation to Home to reset server state
            if (!hash || hash === 'home' || hash === '홈') {
                debugLog('🏠 No hash - forcing Home page');
                const tryClickHome = (attempts = 0) => {
                    if (attempts >= 20) return;
                    const navButtons = document.querySelectorAll('#sidebar sl-button');
                    if (navButtons.length > 0) {
                        const homeBtn = navButtons[0]; // First button is Home
                        if (homeBtn.getAttribute('variant') !== 'primary') {
                            homeBtn.click();
                            debugLog('🏠 Clicked Home button');
                        }
                    } else {
                        setTimeout(() => tryClickHome(attempts + 1), 100);
                    }
                };
                tryClickHome();
                return;
            }
            
            const targetKey = 'page_' + hash;
            debugLog(`📍 Restoring from Hash: "${hash}" (key: ${targetKey})`);
            
            const tryRestore = (attempts = 0) => {
                // Stop after 5 seconds
                if (attempts >= 50) {
                     console.warn(`⚠ Failed to restore hash "${hash}"`);
                     return;
                }
                
                const navButtons = document.querySelectorAll('#sidebar sl-button');
                if (navButtons.length === 0) {
                    setTimeout(() => tryRestore(attempts + 1), 100);
                    return;
                }
                
                for (let btn of navButtons) {
                    const onclick = btn.getAttribute('onclick') || '';
                    const hxVals = btn.getAttribute('hx-vals') || '';
                    
                    // Match either onclick (WS mode) or hx-vals (Lite mode)
                    if (onclick.includes(targetKey) || hxVals.includes(targetKey)) {
                        debugLog(`✓ Found target button for hash "${hash}". Clicking...`);
                        
                        // Check if already active to avoid redundant clicks
                        if (btn.getAttribute('variant') === 'primary') {
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
</head>
<body>
    %SPLASH%
    <div id="root">
        <div id="sidebar" style="%SIDEBAR_STYLE%">
            %SIDEBAR_CONTENT%
        </div>
        <div id="main">
            <div id="header">
                 <sl-icon-button name="list" style="font-size: 1.5rem; color: var(--sl-text);" onclick="toggleSidebar()"></sl-icon-button>
            </div>
            <div id="app">%CONTENT%</div>
        </div>
    </div>
    <div id="toast-injector" style="display:none;"></div>
</body>
</html>
"""
