"""Status Widgets Mixin for Violit"""

from typing import Union, Callable, Optional
from ..component import Component
from ..context import rendering_ctx
from ..state import get_session_store, State
from ..style_utils import merge_cls, merge_style, resolve_value


class StatusWidgetsMixin:
    """Status display widgets (success, info, warning, error, toast, progress, spinner, status, balloons, snow, exception)"""
    
    def success(self, *args, icon: str = None, cls: str = "", style: str = ""): 
        """Display success alert"""
        self.alert(*args, variant="success", icon=icon or "circle-check", cls=cls, style=style)
    
    def warning(self, *args, icon: str = None, cls: str = "", style: str = ""): 
        """Display warning alert"""
        self.alert(*args, variant="warning", icon=icon or "triangle-exclamation", cls=cls, style=style)
    
    def error(self, *args, icon: str = None, cls: str = "", style: str = ""): 
        """Display error alert"""
        self.alert(*args, variant="danger", icon=icon or "circle-xmark", cls=cls, style=style)
    
    def info(self, *args, icon: str = None, cls: str = "", style: str = ""): 
        """Display info alert"""
        self.alert(*args, variant="primary", icon=icon or "circle-info", cls=cls, style=style)
    
    def alert(self, *args, variant="primary", icon=None, cls: str = "", style: str = ""):
        """Display alert message.

        Each positional argument may be a plain value, State, ComputedState,
        or a callable (lambda / function).  All are resolved at render time
        so the widget stays reactive.
        Multiple arguments are joined with a space.
        """
        import html as html_lib

        cid = self._get_next_cid("alert")
        def builder():
            token = rendering_ctx.set(cid)
            try:
                parts = [str(resolve_value(arg)) for arg in args]
            finally:
                rendering_ctx.reset(token)

            import re as _re
            escaped_val = html_lib.escape(" ".join(parts))
            # Inline markdown: bold, italic, code + newline support
            escaped_val = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escaped_val)
            escaped_val = _re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', escaped_val)
            escaped_val = _re.sub(r'`(.+?)`', r'<code>\1</code>', escaped_val)
            escaped_val = escaped_val.replace('\n', '<br>')
            variant_map = {"primary": "brand", "danger": "danger"}.get(variant, variant)
            icon_html = f'<wa-icon slot="icon" name="{icon}"></wa-icon>' if icon else ""
            html_output = f'<wa-callout variant="{variant_map}" appearance="filled-outlined">{icon_html}{escaped_val}</wa-callout>'
            _wd = self._get_widget_defaults("alert")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html_output, class_=_fc or None, style=_fs or None)
        self._register_component(cid, builder)

    # Callout / Admonition
    _CALLOUT_VARIANTS = {
        "tip": {
            "icon": "lightbulb",
            "bg": "#fffbeb", "border": "#fde68a", "accent": "#f59e0b",
            "title_color": "#92400e", "text_color": "#78350f",
        },
        "info": {
            "icon": "circle-info",
            "bg": "#eff6ff", "border": "#bfdbfe", "accent": "#3b82f6",
            "title_color": "#1e40af", "text_color": "#1e3a5f",
        },
        "warning": {
            "icon": "triangle-exclamation",
            "bg": "#fef2f2", "border": "#fecaca", "accent": "#ef4444",
            "title_color": "#991b1b", "text_color": "#7f1d1d",
        },
        "danger": {
            "icon": "octagon-exclamation",
            "bg": "#fef2f2", "border": "#fecaca", "accent": "#dc2626",
            "title_color": "#991b1b", "text_color": "#7f1d1d",
        },
        "success": {
            "icon": "circle-check",
            "bg": "#f0fdf4", "border": "#bbf7d0", "accent": "#22c55e",
            "title_color": "#166534", "text_color": "#14532d",
        },
        "note": {
            "icon": "note-sticky",
            "bg": "#f8fafc", "border": "#e2e8f0", "accent": "#64748b",
            "title_color": "#334155", "text_color": "#475569",
        },
    }

    def callout(self, body, title=None, variant="info", icon=None,
                allow_html=False, cls: str = "", style: str = ""):
        """Display a callout / admonition box with colored left-border accent.

        Args:
            body: Content text (supports State/ComputedState for reactive updates)
            title: Optional bold title shown above the body
            variant: "tip" | "info" | "warning" | "danger" | "success" | "note"
            icon: Custom Web Awesome icon name (auto-selected by variant if None)
            allow_html: If True, body/title are rendered as raw HTML (like app.html).
                        If False (default), content is escaped for XSS safety.
            cls: Additional CSS classes
            style: Additional inline styles

        Example:
            app.callout("Remember to save!", title="TIP", variant="tip")
            app.callout("Use <code>app.text()</code> for safe output", variant="info", allow_html=True)
        """
        import html as html_lib
        from ..state import State, ComputedState

        cid = self._get_next_cid("callout")
        v = self._CALLOUT_VARIANTS.get(variant, self._CALLOUT_VARIANTS["info"])
        icon_name = icon or v["icon"]

        def builder():
            token = rendering_ctx.set(cid)
            try:
                if isinstance(body, (State, ComputedState)):
                    body_val = str(body.value)
                elif callable(body):
                    body_val = str(body())
                else:
                    body_val = str(body)
            finally:
                rendering_ctx.reset(token)

            display_body = body_val if allow_html else html_lib.escape(body_val)

            title_html = ""
            if title:
                display_title = str(title) if allow_html else html_lib.escape(str(title))
                title_html = (
                    f'<div style="font-weight:700;font-size:0.8rem;'
                    f'color:{v["title_color"]};margin-bottom:0.25rem;">'
                    f'{display_title}</div>'
                )

            html_output = (
                f'<div style="display:flex;gap:0.75rem;padding:1rem 1.25rem;'
                f'background:{v["bg"]};border:1px solid {v["border"]};'
                f'border-radius:0.625rem;margin:0.75rem 0 1.25rem;'
                f'border-left:4px solid {v["accent"]};">'
                f'<wa-icon name="{icon_name}" style="font-size:1.1rem;'
                f'color:{v["accent"]};flex-shrink:0;margin-top:0.1rem;"></wa-icon>'
                f'<div>{title_html}'
                f'<div style="font-size:0.85rem;color:{v["text_color"]};'
                f'line-height:1.6;">{display_body}</div>'
                f'</div></div>'
            )

            _wd = self._get_widget_defaults("callout")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html_output, class_=_fc or None, style=_fs or None)

        self._register_component(cid, builder)

    def callout_tip(self, body, title="TIP", **kwargs):
        """Shortcut for callout(variant='tip')"""
        self.callout(body, title=title, variant="tip", **kwargs)

    def callout_info(self, body, title="INFO.", **kwargs):
        """Shortcut for callout(variant='info')"""
        self.callout(body, title=title, variant="info", **kwargs)

    def callout_warning(self, body, title="WARNING", **kwargs):
        """Shortcut for callout(variant='warning')"""
        self.callout(body, title=title, variant="warning", **kwargs)

    def callout_danger(self, body, title="DANGER", **kwargs):
        """Shortcut for callout(variant='danger')"""
        self.callout(body, title=title, variant="danger", **kwargs)

    def callout_success(self, body, title="SUCCESS", **kwargs):
        """Shortcut for callout(variant='success')"""
        self.callout(body, title=title, variant="success", **kwargs)

    def callout_note(self, body, title="NOTE", **kwargs):
        """Shortcut for callout(variant='note')"""
        self.callout(body, title=title, variant="note", **kwargs)

    def toast(self, *args, icon="circle-info", variant="primary"):
        """Display toast notification (Signal support via evaluation)"""
        import json
        from ..state import State, ComputedState
        
        # Check if any argument requires dynamic binding
        is_dynamic = any(isinstance(a, (State, ComputedState, Callable)) for a in args)
        
        if is_dynamic:
            cid = self._get_next_cid("toast_trigger")
            def builder():
                token = rendering_ctx.set(cid)
                parts = []
                for arg in args:
                    if isinstance(arg, (State, ComputedState)):
                        parts.append(str(arg.value))
                    elif callable(arg):
                        parts.append(str(arg()))
                    else:
                        parts.append(str(arg))
                val = " ".join(parts)
                rendering_ctx.reset(token)
                
                # XSS protection: safely escape with JSON.stringify
                safe_val = json.dumps(str(val))
                safe_variant = json.dumps(str(variant))
                safe_icon = json.dumps(str(icon))
                code = f"createToast({safe_val}, {safe_variant}, {safe_icon})"
                return Component("script", id=cid, content=code)
            self._register_component(cid, builder)
        else:
            message = " ".join(str(a) for a in args)
            # XSS protection: safely escape with JSON.stringify
            safe_message = json.dumps(str(message))
            safe_variant = json.dumps(str(variant))
            safe_icon = json.dumps(str(icon))
            code = f"createToast({safe_message}, {safe_variant}, {safe_icon})"
            self._enqueue_eval(code, toast_data={"message": str(message), "icon": str(icon), "variant": str(variant)})

    def balloons(self):
        """Display balloons animation"""
        code = "createBalloons()"
        self._enqueue_eval(code, effect="balloons")

    def snow(self):
        """Display snow animation"""
        code = "createSnow()"
        self._enqueue_eval(code, effect="snow")

    def exception(self, exception: Exception, cls: str = "", style: str = ""):
        """Display exception with traceback"""
        import traceback
        import html as html_lib
        
        cid = self._get_next_cid("exception")
        tb = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        
        def builder():
            # XSS protection: escape exception message and traceback
            escaped_name = html_lib.escape(type(exception).__name__)
            escaped_msg = html_lib.escape(str(exception))
            escaped_tb = html_lib.escape(tb)
            
            html_output = f'''
            <wa-callout variant="danger" appearance="filled-outlined" style="margin-bottom:1rem;">
                <wa-icon slot="icon" name="circle-exclamation"></wa-icon>
                <strong>{escaped_name}:</strong> {escaped_msg}
                <pre style="margin-top:0.5rem;padding:0.5rem;background:rgba(0,0,0,0.1);border-radius:0.25rem;overflow-x:auto;font-size:0.85rem;">{escaped_tb}</pre>
            </wa-callout>
            '''
            _wd = self._get_widget_defaults("exception")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html_output, class_=_fc or None, style=_fs or None)
        self._register_component(cid, builder)

    def _enqueue_eval(self, code, **lite_data):
        """Internal helper to enqueue JS evaluation or store for lite mode"""
        import asyncio
        from ..context import session_ctx

        if self.mode == 'ws':
            sid = session_ctx.get()
            if sid and getattr(self, 'ws_engine', None) and sid in self.ws_engine.sockets:
                try:
                    loop = asyncio.get_running_loop()
                    store = get_session_store()
                    if 'eval_queue' not in store: store['eval_queue'] = []
                    store['eval_queue'].append(code)
                except RuntimeError:
                    # Sync context (e.g. background thread) -> push immediately
                    _loop = asyncio.new_event_loop()
                    try:
                        _loop.run_until_complete(self.ws_engine.push_eval(sid, code))
                    finally:
                        _loop.close()
            else:
                store = get_session_store()
                if 'eval_queue' not in store: store['eval_queue'] = []
                store['eval_queue'].append(code)
        else:
            store = get_session_store()
            if 'toasts' not in store: store['toasts'] = []
            if 'effects' not in store: store['effects'] = []
            
            if 'toast_data' in lite_data:
                store['toasts'].append(lite_data['toast_data'])
            if 'effect' in lite_data:
                store['effects'].append(lite_data['effect'])

    def progress(self, value=0, *args, cls: str = "", style: str = ""):
        """Display progress bar with Signal support"""
        import html as html_lib
        from ..state import State, ComputedState
        
        cid = self._get_next_cid("progress")
        
        def builder():
            # Handle Signal
            val_num = value
            if isinstance(value, (State, ComputedState)):
                token = rendering_ctx.set(cid)
                val_num = value.value
                rendering_ctx.reset(token)
            elif callable(value):
                token = rendering_ctx.set(cid)
                val_num = value()
                rendering_ctx.reset(token)
            
            # Resolve text args
            parts = []
            if args:
                token = rendering_ctx.set(cid)
                for arg in args:
                    if isinstance(arg, (State, ComputedState)):
                        parts.append(str(arg.value))
                    elif callable(arg):
                        parts.append(str(arg()))
                    else:
                        parts.append(str(arg))
                rendering_ctx.reset(token)
                progress_text = " ".join(parts)
            else:
                progress_text = f"{val_num}%"
            
            # XSS protection: escape text
            escaped_text = html_lib.escape(str(progress_text))
            
            html_output = f'''
            <div style="margin-bottom:0.5rem;">
                <div style="display:flex;justify-content:space-between;margin-bottom:0.25rem;">
                    <span style="font-size:0.875rem;color:var(--vl-text);">{escaped_text}</span>
                    <span style="font-size:0.875rem;color:var(--vl-text-muted);">{val_num}%</span>
                </div>
                <wa-progress-bar value="{val_num}"></wa-progress-bar>
            </div>
            '''
            _wd = self._get_widget_defaults("progress")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html_output, class_=_fc or None, style=_fs or None)
        self._register_component(cid, builder)

    def spinner(self, *args, cls: str = "", style: str = ""):
        """Display loading spinner"""
        import html as html_lib
        from ..state import State, ComputedState
        
        cid = self._get_next_cid("spinner")
        
        def builder():
            parts = []
            if args:
                token = rendering_ctx.set(cid)
                for arg in args:
                    if isinstance(arg, (State, ComputedState)):
                        parts.append(str(arg.value))
                    elif callable(arg):
                        parts.append(str(arg()))
                    else:
                        parts.append(str(arg))
                rendering_ctx.reset(token)
                text = " ".join(parts)
            else:
                text = "Loading..."
            
            # XSS protection: escape text
            escaped_text = html_lib.escape(str(text))
            
            html_output = f'''
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:1rem;">
                <wa-spinner style="font-size:1.5rem;"></wa-spinner>
                <span style="color:var(--vl-text-muted);font-size:0.875rem;">{escaped_text}</span>
            </div>
            '''
            _wd = self._get_widget_defaults("spinner")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html_output, class_=_fc or None, style=_fs or None)
        self._register_component(cid, builder)
    
    def status(self, label: str, state: str = "running", expanded: bool = True, cls: str = "", style: str = ""):
        from ..context import fragment_ctx
        
        cid = self._get_next_cid("status")
        
        class StatusContext:
            def __init__(self, app, status_id, label, state, expanded, user_cls="", user_style=""):
                self.app = app
                self.status_id = status_id
                self.label = label
                self.state = state
                self.expanded = expanded
                self.user_cls = user_cls
                self.user_style = user_style
                self.token = None
                
            def __enter__(self):
                # Register builder
                def builder():
                    store = get_session_store()
                    
                    # Collect nested content
                    htmls = []
                    # Check static
                    for cid_child, b in self.app.static_fragment_components.get(self.status_id, []):
                        htmls.append(b().render())
                    # Check session
                    for cid_child, b in store['fragment_components'].get(self.status_id, []):
                        htmls.append(b().render())
                    
                    inner_html = "".join(htmls)
                    
                    # Status icon and color based on state
                    if self.state == "running":
                        icon = '<wa-spinner style="font-size:1rem;"></wa-spinner>'
                        border_color = "var(--vl-primary)"
                    elif self.state == "complete":
                        icon = '<wa-icon name="circle-check" style="color:#10b981;font-size:1rem;"></wa-icon>'
                        border_color = "#10b981"
                    elif self.state == "error":
                        icon = '<wa-icon name="circle-xmark" style="color:#ef4444;font-size:1rem;"></wa-icon>'
                        border_color = "#ef4444"
                    else:
                        icon = '<wa-icon name="circle-info" style="color:var(--vl-primary);font-size:1rem;"></wa-icon>'
                        border_color = "var(--vl-primary)"
                    
                    # XSS protection: escape label
                    import html as html_lib
                    escaped_label = html_lib.escape(str(self.label))
                    
                    # Build status container
                    html_output = f'''
                    <wa-details {"open" if self.expanded else ""} style="margin-bottom:1rem;">
                        <div slot="summary" style="display:flex;align-items:center;gap:0.5rem;font-weight:600;">
                            {icon}
                            <span>{escaped_label}</span>
                        </div>
                        <div style="padding:0.5rem 0 0 1.5rem;border-left:2px solid {border_color};margin-left:0.5rem;">
                            {inner_html}
                        </div>
                    </wa-details>
                    '''
                    _wd = self.app._get_widget_defaults("status")
                    _fc = merge_cls(_wd.get("cls", ""), self.user_cls)
                    _fs = merge_style(_wd.get("style", ""), self.user_style)
                    return Component("div", id=self.status_id, content=html_output, class_=_fc or None, style=_fs or None)
                
                self.app._register_component(self.status_id, builder)
                
                self.token = fragment_ctx.set(self.status_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                if self.token:
                    fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
                
        return StatusContext(self, cid, label, state, expanded, cls, style)
