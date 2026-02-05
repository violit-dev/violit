"""Status Widgets Mixin for Violit"""

from typing import Union, Callable, Optional
from ..component import Component
from ..context import rendering_ctx
from ..state import get_session_store, State


class StatusWidgetsMixin:
    """Status display widgets (success, info, warning, error, toast, progress, spinner, status, balloons, snow, exception)"""
    
    def success(self, *args): 
        """Display success alert"""
        self.alert(*args, variant="success", icon="check-circle")
    
    def warning(self, *args): 
        """Display warning alert"""
        self.alert(*args, variant="warning", icon="exclamation-triangle")
    
    def error(self, *args): 
        """Display error alert"""
        self.alert(*args, variant="danger", icon="x-circle")
    
    def info(self, *args): 
        """Display info alert"""
        self.alert(*args, variant="primary", icon="info-circle")
    
    def alert(self, *args, variant="primary", icon=None):
        """Display alert message with Signal support (multiple arguments supported)"""
        import html as html_lib
        
        cid = self._get_next_cid("alert")
        def builder():
            # Signal handling for multiple arguments
            parts = []
            token = rendering_ctx.set(cid)
            
            try:
                for arg in args:
                    if isinstance(arg, State):
                        parts.append(str(arg.value))
                    elif callable(arg):
                        parts.append(str(arg()))
                    else:
                        parts.append(str(arg))
            finally:
                rendering_ctx.reset(token)
            
            val = " ".join(parts)
            
            # XSS protection: escape content
            escaped_val = html_lib.escape(str(val))
            
            icon_html = f'<sl-icon slot="icon" name="{icon}"></sl-icon>' if icon else ""
            html_output = f'<sl-alert variant="{variant}" open>{icon_html}{escaped_val}</sl-alert>'
            return Component("div", id=cid, content=html_output)
        self._register_component(cid, builder)

    def toast(self, *args, icon="info-circle", variant="primary"):
        """Display toast notification (Signal support via evaluation)"""
        import json
        from ..state import State
        
        # Check if any argument requires dynamic binding
        is_dynamic = any(isinstance(a, (State, Callable)) for a in args)
        
        if is_dynamic:
            cid = self._get_next_cid("toast_trigger")
            def builder():
                token = rendering_ctx.set(cid)
                parts = []
                for arg in args:
                    if isinstance(arg, State):
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

    def exception(self, exception: Exception):
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
            <sl-alert variant="danger" open style="margin-bottom:1rem;">
                <sl-icon slot="icon" name="exclamation-octagon"></sl-icon>
                <strong>{escaped_name}:</strong> {escaped_msg}
                <pre style="margin-top:0.5rem;padding:0.5rem;background:rgba(0,0,0,0.1);border-radius:0.25rem;overflow-x:auto;font-size:0.85rem;">{escaped_tb}</pre>
            </sl-alert>
            '''
            return Component("div", id=cid, content=html_output)
        self._register_component(cid, builder)

    def _enqueue_eval(self, code, **lite_data):
        """Internal helper to enqueue JS evaluation or store for lite mode"""
        if self.mode == 'ws':
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

    def progress(self, value=0, *args):
        """Display progress bar with Signal support"""
        import html as html_lib
        from ..state import State
        
        cid = self._get_next_cid("progress")
        
        def builder():
            # Handle Signal
            val_num = value
            if isinstance(value, State):
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
                    if isinstance(arg, State):
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
                    <span style="font-size:0.875rem;color:var(--sl-text);">{escaped_text}</span>
                    <span style="font-size:0.875rem;color:var(--sl-text-muted);">{val_num}%</span>
                </div>
                <sl-progress-bar value="{val_num}"></sl-progress-bar>
            </div>
            '''
            return Component("div", id=cid, content=html_output)
        self._register_component(cid, builder)

    def spinner(self, *args):
        """Display loading spinner"""
        import html as html_lib
        from ..state import State
        
        cid = self._get_next_cid("spinner")
        
        def builder():
            parts = []
            if args:
                token = rendering_ctx.set(cid)
                for arg in args:
                    if isinstance(arg, State):
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
                <sl-spinner style="font-size:1.5rem;"></sl-spinner>
                <span style="color:var(--sl-text-muted);font-size:0.875rem;">{escaped_text}</span>
            </div>
            '''
            return Component("div", id=cid, content=html_output)
        self._register_component(cid, builder)
    
    def status(self, label: str, state: str = "running", expanded: bool = True):
        from ..context import fragment_ctx
        
        cid = self._get_next_cid("status")
        
        class StatusContext:
            def __init__(self, app, status_id, label, state, expanded):
                self.app = app
                self.status_id = status_id
                self.label = label
                self.state = state
                self.expanded = expanded
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
                        icon = '<sl-spinner style="font-size:1rem;"></sl-spinner>'
                        border_color = "var(--sl-primary)"
                    elif self.state == "complete":
                        icon = '<sl-icon name="check-circle-fill" style="color:#10b981;font-size:1rem;"></sl-icon>'
                        border_color = "#10b981"
                    elif self.state == "error":
                        icon = '<sl-icon name="x-circle-fill" style="color:#ef4444;font-size:1rem;"></sl-icon>'
                        border_color = "#ef4444"
                    else:
                        icon = '<sl-icon name="info-circle-fill" style="color:var(--sl-primary);font-size:1rem;"></sl-icon>'
                        border_color = "var(--sl-primary)"
                    
                    # XSS protection: escape label
                    import html as html_lib
                    escaped_label = html_lib.escape(str(self.label))
                    
                    # Build status container
                    html_output = f'''
                    <sl-details {"open" if self.expanded else ""} style="margin-bottom:1rem;">
                        <div slot="summary" style="display:flex;align-items:center;gap:0.5rem;font-weight:600;">
                            {icon}
                            <span>{escaped_label}</span>
                        </div>
                        <div style="padding:0.5rem 0 0 1.5rem;border-left:2px solid {border_color};margin-left:0.5rem;">
                            {inner_html}
                        </div>
                    </sl-details>
                    '''
                    return Component("div", id=self.status_id, content=html_output)
                
                self.app._register_component(self.status_id, builder)
                
                self.token = fragment_ctx.set(self.status_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                if self.token:
                    fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
                
        return StatusContext(self, cid, label, state, expanded)
