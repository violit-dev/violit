import asyncio
import hashlib
import hmac
import json
import logging
import queue
import uuid
from typing import List, Optional

from fastapi import Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

from .app_assets import get_vendor_resources
from .app_shell import build_html_response, build_shell_html, build_user_css
from .app_template import HTML_TEMPLATE
from .component import Component
from .context import action_ctx, initial_render_ctx, session_ctx, view_ctx
from .state import STATIC_STORE, get_session_store


class AppRuntimeMixin:
    def _resolve_http_view_id(self, request: Request, *, generate: bool = False) -> Optional[str]:
        view_id = request.headers.get("X-Violit-View") or request.query_params.get("_vl_view_id")
        if view_id:
            return view_id
        if generate:
            return uuid.uuid4().hex
        return None

    def _resolve_ws_view_id(self, ws: WebSocket) -> Optional[str]:
        return ws.headers.get("X-Violit-View") or ws.query_params.get("_vl_view_id") or None

    def _set_runtime_context(self, sid: Optional[str], current_view_id: Optional[str]):
        session_token = session_ctx.set(sid)
        view_token = view_ctx.set(current_view_id)
        return session_token, view_token

    def _reset_runtime_context(self, session_token, view_token):
        view_ctx.reset(view_token)
        session_ctx.reset(session_token)

    def _replace_lite_stream_queue(self, sid: str, current_view_id: str):
        key = (sid, current_view_id)
        with self._lite_stream_lock:
            stream_queue = queue.Queue()
            self._lite_stream_queues[key] = stream_queue
            return stream_queue

    def _enqueue_lite_stream_payload(self, sid: str, payload: str, view_id: Optional[str] = None):
        if not sid or not payload or not self.lite_engine:
            return
        current_view_id = view_id or view_ctx.get()
        if not current_view_id:
            return
        key = (sid, current_view_id)
        with self._lite_stream_lock:
            stream_queue = self._lite_stream_queues.get(key)
        if stream_queue is None:
            return
        try:
            stream_queue.put_nowait(payload)
        except Exception as exc:
            logging.getLogger(__name__).debug(f"[lite-stream] Failed to enqueue payload: {exc}")

    def _drain_lite_side_effects(self, store) -> str:
        html = ""

        toasts = store.get('toasts', [])
        if toasts:
            import html as html_lib
            toasts_json = json.dumps(toasts)
            toasts_escaped = html_lib.escape(toasts_json)

            html += f'''<div id="toast-injector" hx-swap-oob="true" data-toasts="{toasts_escaped}">
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
            store['toasts'] = []

        effects = store.get('effects', [])
        if effects:
            effects_json = json.dumps(effects)
            html += f'''<div id="effects-injector" hx-swap-oob="true" data-effects='{effects_json}'>
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
            store['effects'] = []

        return html

    def _build_lite_oob_payload(self, components: Optional[List[Component]] = None) -> str:
        store = get_session_store()
        html = ""
        if components and self.lite_engine:
            html += self.lite_engine.wrap_oob(components)
        html += self._drain_lite_side_effects(store)
        return html

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

    def _setup_routes(self):
        """Setup FastAPI routes"""
        @self.fastapi.middleware("http")
        async def mw(request: Request, call_next):
            if self.native_token is not None:
                token_from_request = request.query_params.get("_native_token")
                token_from_cookie = request.cookies.get("_native_token")
                user_agent = request.headers.get("user-agent", "")

                self.debug_print(f"[NATIVE SECURITY CHECK]")
                self.debug_print(f"  Token from request: {token_from_request[:20] if token_from_request else None}...")
                self.debug_print(f"  Token from cookie: {token_from_cookie[:20] if token_from_cookie else None}...")
                self.debug_print(f"  Expected token: {self.native_token[:20]}...")
                self.debug_print(f"  User-Agent: {user_agent}")

                is_valid_token = (token_from_request == self.native_token or token_from_cookie == self.native_token)

                if not is_valid_token:
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

            sid = request.cookies.get("ss_sid") or str(uuid.uuid4())
            current_view_id = self._resolve_http_view_id(
                request,
                generate=request.method == "GET" and request.url.path == "/",
            )

            session_token, view_token = self._set_runtime_context(sid, current_view_id)
            response = await call_next(request)
            self._reset_runtime_context(session_token, view_token)

            is_https = request.url.scheme == "https"
            response.set_cookie(
                "ss_sid",
                sid,
                httponly=True,
                secure=is_https,
                samesite="lax"
            )

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
            store = get_session_store()
            builders = store.get('builders')
            if builders:
                builders.clear()
            actions = store.get('actions')
            if actions:
                actions.clear()
            submitted_values = store.get('submitted_values')
            if submitted_values:
                submitted_values.clear()
            order = store.get('order')
            if order:
                order.clear()
            sidebar_order = store.get('sidebar_order')
            if sidebar_order:
                sidebar_order.clear()
            fragment_components = store.get('fragment_components')
            if fragment_components:
                fragment_components.clear()
            tracker = store.get('tracker')
            if tracker and getattr(tracker, 'subscribers', None) is not None:
                tracker.subscribers.clear()
            dirty_states = store.get('dirty_states')
            if dirty_states:
                dirty_states.clear()
            forced_dirty = store.get('forced_dirty')
            if forced_dirty:
                forced_dirty.clear()
            eval_queue = store.get('eval_queue')
            if eval_queue:
                eval_queue.clear()
            deferred_charts = store.get('_vl_chart_requested')
            if deferred_charts:
                deferred_charts.clear()
            base_component_count = STATIC_STORE.get('component_count', 0)
            if store.get('component_count') != base_component_count:
                store['component_count'] = base_component_count

            token = initial_render_ctx.set(True)
            try:
                main_c, sidebar_c = self._render_all()
            finally:
                initial_render_ctx.reset(token)

            store = get_session_store()
            theme = store['theme']

            sidebar_style = "" if (sidebar_c or self.static_sidebar_order) else "display: none;"
            main_class = "" if (sidebar_c or self.static_sidebar_order) else "sidebar-collapsed"

            try:
                sid = session_ctx.get()
            except LookupError:
                sid = request.cookies.get("ss_sid")
            try:
                current_view_id = view_ctx.get()
            except LookupError:
                current_view_id = self._resolve_http_view_id(request, generate=True)

            csrf_token = self._generate_csrf_token(sid) if sid and self.csrf_enabled else ""
            csrf_script = f'<script>window._csrf_token = "{csrf_token}";</script>' if csrf_token else ""

            if self.debug_mode:
                print(f"[DEBUG] Session ID: {sid[:8] if sid else 'None'}...")
                print(f"[DEBUG] CSRF enabled: {self.csrf_enabled}")
                print(f"[DEBUG] CSRF token generated: {bool(csrf_token)}")

            debug_script = (
                f'<script>'
                f'window._vlBootId = "{self.boot_id}";'
                f'window._vlServerBootId = null;'
                f'window._vlWsHelloReceived = false;'
                f'window._debug_mode = {str(self.debug_mode).lower()};'
                f'</script>'
            )

            active_theme_name = "dark" if theme.mode == "dark" else "light"
            inactive_theme_name = "light" if active_theme_name == "dark" else "dark"
            vendor_resources = get_vendor_resources(
                use_cdn=self.use_cdn,
                active_theme_name=active_theme_name,
                inactive_theme_name=inactive_theme_name,
            )

            user_css = build_user_css(self._user_css)

            root_style = "visibility:hidden;opacity:0;transition:opacity 0.4s cubic-bezier(0.22, 1, 0.36, 1);" if self.show_splash else ""
            html_class = f"{theme.theme_class} {'vl-splash-active' if self.show_splash else ''}".strip()
            body_class = "vl-splash-active" if self.show_splash else ""
            sidebar_resizer_style = "" if (self._sidebar_resizable and (sidebar_c or self.static_sidebar_order)) else "display: none;"
            html = build_shell_html(
                HTML_TEMPLATE,
                content=main_c,
                sidebar_content=sidebar_c,
                sidebar_style=sidebar_style,
                sidebar_resizer_style=sidebar_resizer_style,
                main_class=main_class,
                mode=self.mode,
                title=self.app_title,
                html_class=html_class,
                body_class=body_class,
                css_vars=theme.to_css_vars(),
                splash_html=self._splash_html if self.show_splash else "",
                container_max_width=self.container_max_width,
                widget_gap=self.widget_gap,
                sidebar_width=self._sidebar_width,
                sidebar_min_width=self._sidebar_min_width,
                sidebar_max_width=self._sidebar_max_width,
                sidebar_resizable=self._sidebar_resizable,
                csrf_script=csrf_script,
                debug_script=debug_script,
                vendor_resources=vendor_resources,
                user_css=user_css,
                root_style=root_style,
                disconnect_timeout=self.disconnect_timeout,
                view_id=current_view_id or "",
            )
            return build_html_response(html)

        @self.fastapi.get("/__violit_boot")
        async def boot_probe():
            return JSONResponse(
                {"bootId": self.boot_id},
                headers={
                    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
                    "Pragma": "no-cache",
                    "Expires": "0",
                },
            )

        @self.fastapi.get("/lite-stream")
        async def lite_stream(request: Request):
            sid = request.cookies.get("ss_sid")
            current_view_id = self._resolve_http_view_id(request, generate=False)
            if not sid or not current_view_id:
                return HTMLResponse("", status_code=204)

            stream_queue = self._replace_lite_stream_queue(sid, current_view_id)

            async def event_stream():
                try:
                    yield "retry: 1000\n\n"
                    while True:
                        if await request.is_disconnected():
                            break
                        try:
                            payload = await asyncio.to_thread(stream_queue.get, True, 0.5)
                        except queue.Empty:
                            yield ": keep-alive\n\n"
                            continue
                        if not payload:
                            continue
                        yield f"event: oob\ndata: {json.dumps(payload)}\n\n"
                finally:
                    with self._lite_stream_lock:
                        key = (sid, current_view_id)
                        current = self._lite_stream_queues.get(key)
                        if current is stream_queue:
                            self._lite_stream_queues.pop(key, None)

            return StreamingResponse(
                event_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache, no-transform",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                },
            )

        @self.fastapi.post("/action/{cid}")
        async def action(request: Request, cid: str):
            sid = request.cookies.get("ss_sid")
            current_view_id = self._resolve_http_view_id(request, generate=False)

            if self.csrf_enabled:
                form = await request.form()
                csrf_token = form.get("_csrf_token") or request.headers.get("X-CSRF-Token")

                if not csrf_token or not self._verify_csrf_token(sid, csrf_token):
                    return JSONResponse(
                        {"error": "Invalid CSRF token"},
                        status_code=403
                    )
            else:
                form = await request.form()

            current_view_id = current_view_id or form.get("_vl_view_id")
            if not sid or not current_view_id:
                return JSONResponse({"error": "Missing view id"}, status_code=400)

            session_token, view_token = self._set_runtime_context(sid, current_view_id)
            try:
                value = form.get("value")
                store = get_session_store()
                if value is not None:
                    store.setdefault('submitted_values', {})[cid] = value
                action_callback = store['actions'].get(cid) or self.static_actions.get(cid)
                if action_callback:
                    if not callable(action_callback):
                        self.debug_print(f"ERROR: Action for {cid} is not callable. Got: {type(action_callback)} = {repr(action_callback)}")
                        return HTMLResponse("")

                    store['eval_queue'] = []

                    action_token = action_ctx.set(True)
                    try:
                        action_callback(value) if value is not None else action_callback()
                    finally:
                        action_ctx.reset(action_token)

                    dirty = self._get_dirty_rendered()

                    clicked_component = None
                    other_dirty = []
                    for component in dirty:
                        if component.id == cid:
                            clicked_component = component
                        else:
                            other_dirty.append(component)

                    if clicked_component is None:
                        builder = store['builders'].get(cid) or self.static_builders.get(cid)
                        if builder:
                            clicked_component = builder()

                    response_html = clicked_component.render() if clicked_component else ""
                    response_html += self._build_lite_oob_payload(other_dirty)

                    return HTMLResponse(response_html)
                return HTMLResponse("")
            finally:
                self._reset_runtime_context(session_token, view_token)

        @self.fastapi.websocket("/ws")
        async def ws(ws: WebSocket):
            await ws.accept()

            sid = ws.cookies.get("ss_sid") or str(uuid.uuid4())
            current_view_id = self._resolve_ws_view_id(ws) or uuid.uuid4().hex

            self.debug_print(f"[WEBSOCKET] Session: {sid[:8]}...")

            if self._main_loop is None:
                self._main_loop = asyncio.get_event_loop()

            session_token, view_token = self._set_runtime_context(sid, current_view_id)
            self.ws_engine.register_socket(sid, current_view_id, ws)
            await ws.send_json({"type": "hello", "bootId": self.boot_id, "viewId": current_view_id})

            async def process_message(data):
                msg_type = data.get('type')
                if msg_type != 'click' and msg_type != 'tick':
                    return

                msg_session_token, msg_view_token = self._set_runtime_context(sid, current_view_id)
                try:
                    if msg_type == 'tick':
                        interval_id = data.get('id')
                        store = get_session_store()
                        info = store.get('interval_callbacks', {}).get(interval_id)
                        if info and info['state'] == 'running':
                            condition = info.get('condition')
                            if condition is None or condition():
                                store['eval_queue'] = []
                                info['callback']()
                                for code in store.get('eval_queue', []):
                                    await self.ws_engine.push_eval(sid, code, view_id=current_view_id)
                                store['eval_queue'] = []
                                dirty = self._get_dirty_rendered()
                                if dirty:
                                    await self.ws_engine.push_updates(sid, dirty, view_id=current_view_id)
                        return

                    self.debug_print(f"[WEBSOCKET ACTION] CID: {data.get('id')}")
                    self.debug_print(f"  Native mode: {self.native_token is not None}")
                    self.debug_print(f"  CSRF enabled: {self.csrf_enabled}")
                    self.debug_print(f"  Native token in payload: {data.get('_native_token')[:20] if data.get('_native_token') else None}...")

                    if self.native_token is not None:
                        native_token = data.get('_native_token')
                        if native_token != self.native_token:
                            self.debug_print(f"  [X] Native token mismatch!")
                            await ws.send_json({"type": "error", "message": "Invalid native token"})
                            return
                        else:
                            self.debug_print(f"  [OK] Native token valid - Skipping CSRF check")
                    else:
                        if self.csrf_enabled:
                            csrf_token = data.get('_csrf_token')
                            if not csrf_token or not self._verify_csrf_token(sid, csrf_token):
                                self.debug_print(f"  [X] CSRF token invalid")
                                await ws.send_json({"type": "error", "message": "Invalid CSRF token"})
                                return
                            else:
                                self.debug_print(f"  [OK] CSRF token valid")

                    cid, value = data.get('id'), data.get('value')
                    store = get_session_store()
                    if value is not None:
                        store.setdefault('submitted_values', {})[cid] = value
                    action_callback = store['actions'].get(cid) or self.static_actions.get(cid)

                    self.debug_print(f"  Action found: {action_callback is not None}")

                    is_navigation = cid.startswith('nav_menu')

                    if action_callback:
                        store['eval_queue'] = []
                        self.debug_print(f"  Executing action for CID: {cid} (navigation={is_navigation})...")

                        action_token = action_ctx.set(True)
                        try:
                            action_callback(value) if value is not None else action_callback()
                        finally:
                            action_ctx.reset(action_token)

                        self.debug_print(f"  Action executed")

                        for code in store.get('eval_queue', []):
                            await self.ws_engine.push_eval(sid, code, view_id=current_view_id)
                        store['eval_queue'] = []

                        dirty = self._get_dirty_rendered()
                        self.debug_print(f"  Dirty components: {len(dirty)} ({[c.id for c in dirty]})")

                        if dirty:
                            self.debug_print(f"  Sending {len(dirty)} updates via WebSocket (navigation={is_navigation})...")
                            await self.ws_engine.push_updates(sid, dirty, is_navigation=is_navigation, view_id=current_view_id)
                            self.debug_print(f"  [OK] Updates sent successfully")
                        else:
                            self.debug_print(f"  [!] No dirty components found - nothing to update")
                finally:
                    self._reset_runtime_context(msg_session_token, msg_view_token)

            try:
                while True:
                    data = await ws.receive_json()
                    if data.get("type") == "ping":
                        await ws.send_json({"type": "pong"})
                        continue
                    await process_message(data)
            except WebSocketDisconnect:
                if sid:
                    self.ws_engine.unregister_socket(sid, current_view_id, ws)
                    self.debug_print(f"[WEBSOCKET] Disconnected: {sid[:8]}...")
            finally:
                self._reset_runtime_context(session_token, view_token)