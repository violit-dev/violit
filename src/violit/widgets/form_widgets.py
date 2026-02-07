"""Form Widgets Mixin for Violit"""

from typing import Union, Callable, Optional
from ..component import Component
from ..context import rendering_ctx, fragment_ctx
from ..state import get_session_store
from ..style_utils import merge_cls, merge_style


class FormWidgetsMixin:
    """Form-related widgets (form, form_submit_button, button, download_button, link_button, page_link)"""
    
    def button(self, text: Union[str, Callable], on_click: Optional[Callable] = None, variant="primary", cls: str = "", style: str = "", **props):
        """Display button"""
        cid = self._get_next_cid("btn")
        def builder():
            token = rendering_ctx.set(cid)
            bt = text() if callable(text) else text
            rendering_ctx.reset(token)
            attrs = self.engine.click_attrs(cid)
            _wd = self._get_widget_defaults("button")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            inner = Component("sl-button", id=cid, content=bt, variant=variant, **attrs, **props)
            if _fc or _fs:
                # Center button in wrapper (buttons are inline elements, must be explicitly centered)
                wrap_style = merge_style("display:flex; justify-content:center;", _fs)
                return Component("div", id=f"{cid}_wrap", content=inner.render(), class_=_fc or None, style=wrap_style)
            return inner
        self._register_component(cid, builder, action=on_click)

    def download_button(self, label, data, file_name, mime="text/plain", on_click=None, cls: str = "", style: str = "", **props):
        """Download button (Streamlit-compatible interface)
        
        Args:
            label: Button label
            data: Data to download (str, bytes, or file-like)
            file_name: Name for the downloaded file
            mime: MIME type of the file
            on_click: Optional callback when button is clicked (called AFTER download)
        
        Returns:
            None
        """
        cid = self._get_next_cid("download_btn")
        
        def builder():
            import base64
            
            # Convert data to downloadable format
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            elif isinstance(data, bytes):
                data_bytes = data
            else:
                # Try to convert to string
                data_bytes = str(data).encode('utf-8')
            
            # Create data URL
            data_base64 = base64.b64encode(data_bytes).decode('utf-8')
            data_url = f"data:{mime};base64,{data_base64}"
            
            # Check for Native Mode (pywebview)
            is_native = False
            try:
                import webview
                if len(webview.windows) > 0:
                    is_native = True
            except ImportError:
                pass
                
            if is_native:
                # Native Mode: Use Server-Side Save Dialog
                def native_save_action(v=None):
                    try:
                        import webview
                        import os
                        
                        # Open Save Dialog
                        # Open Save Dialog
                        ext = file_name.split('.')[-1] if '.' in file_name else "*"
                        file_types = (f"{ext.upper()} File (*.{ext})", "All files (*.*)")
                        save_location = webview.windows[0].create_file_dialog(
                            webview.SAVE_DIALOG, 
                            save_filename=file_name,
                            file_types=file_types
                        )
                        
                        if save_location:
                            if isinstance(save_location, list): save_location = save_location[0]
                            with open(save_location, "wb") as f:
                                f.write(data_bytes)
                            
                            # Toast is not easily accessible here without app reference or a way to push JS
                            # But we can try pushing a toast if we are in a callback
                            # For now, just print to console or rely on OS feedback (file created)
                            print(f"[Native] Saved to {save_location}")
                            
                            # Try to trigger a success toast via eval if possible
                            from ..state import get_session_store
                            store = get_session_store()
                            if 'toasts' not in store: store['toasts'] = []
                            store['toasts'].append({"message": f"Saved to {os.path.basename(save_location)}", "variant": "success", "icon": "check-circle"})

                    except Exception as e:
                        print(f"[Native] Save failed: {e}")
                
                # Register the native save action
                # We need to register it with the SAME cid
                # NOTE: The outer _register_component calls with action=on_click (None). 
                # We need to override that or use a different mechanism.
                # Since we are inside builder, we can re-register or use a specific event handler?
                # Actually, the simplest way is to overwrite the action in the store right here, 
                # BUT builder is called during render. Registering action during render is tricky for the *current* cycle 
                # if the component ID is already registered.
                # However, this builder is run by the framework.
                
                # BETTER APPROACH: Set the onclick to sendAction
                # and ensure the action mapped to this CID is our native_save_action.
                
                # We'll rely on the fact that if we provide an onclick behavior that sends action,
                # we need the backend to execute native_save_action.
                
                # Let's monkey-patch the action for this specific instance if we can, 
                # OR return a component that has the right onclick attribute.
                
                # In App.register_component, actions are stored.
                # We can't easily change the registered action from *inside* the builder 
                # because the registration happens *outside* usually (lines 51 self._register_component).
                
                # TRICK: We will not use the `on_click` argument passed to download_button for the native logic.
                # Instead, we define the action wrapper here and stick it into the store manually? 
                # Or we can just modify the way download_button registers itself.
                pass 
                
            if is_native:
                 # Override global action for this component to be the save dialog
                 from ..state import get_session_store
                 store = get_session_store()
                 store['actions'][cid] = native_save_action
                 
                 # Check if we're in lite mode or ws mode
                 if self.mode == 'lite':
                     html = f'''
                     <sl-button variant="primary" hx-post="/action/{cid}" hx-swap="none" hx-trigger="click">
                         <sl-icon slot="prefix" name="download"></sl-icon>
                         {label}
                     </sl-button>
                     '''
                 else:
                     html = f'''
                     <sl-button variant="primary" onclick="window.sendAction('{cid}')">
                         <sl-icon slot="prefix" name="download"></sl-icon>
                         {label}
                     </sl-button>
                     '''
            else:
                 # Web Mode: JS Download
                download_script = f"""
                <script>
                window.download_{cid} = function() {{
                    const link = document.createElement('a');
                    link.href = '{data_url}';
                    link.download = '{file_name}';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }};
                </script>
                """
                
                html = f'''
                {download_script}
                <sl-button variant="primary" onclick="download_{cid}()">
                    <sl-icon slot="prefix" name="download"></sl-icon>
                    {label}
                </sl-button>
                '''
            _wd = self._get_widget_defaults("download_button")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style("display:flex; justify-content:center;", _wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder, action=on_click)

    def link_button(self, label, url, cls: str = "", style: str = "", **props):
        """Display link button"""
        cid = self._get_next_cid("link_btn")
        
        def builder():
            html = f'''
            <sl-button variant="primary" href="{url}" target="_blank">
                <sl-icon slot="prefix" name="box-arrow-up-right"></sl-icon>
                {label}
            </sl-button>
            '''
            _wd = self._get_widget_defaults("link_button")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style("display:flex; justify-content:center;", _wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder)

    def page_link(self, page, label, icon=None, cls: str = "", style: str = "", **props):
        """Display page navigation link"""
        cid = self._get_next_cid("page_link")
        
        def builder():
            icon_html = f'<sl-icon slot="prefix" name="{icon}"></sl-icon>' if icon else ""
            # In a real implementation, this would trigger page navigation
            # For now, just render as a styled link
            html = f'''
            <a href="{page}" style="display:inline-flex;align-items:center;gap:0.5rem;color:var(--sl-primary);text-decoration:none;padding:0.5rem 1rem;border-radius:0.25rem;transition:background 0.2s;">
                {icon_html}
                {label}
            </a>
            '''
            _wd = self._get_widget_defaults("page_link")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder)

    def switch_page(self, page):
        """Switch to a different page (navigation)"""
        # This would be implemented with the navigation system
        # For now, we can use JavaScript to navigate
        code = f"window.location.href = '{page}';"
        if self.mode == 'ws':
            store = get_session_store()
            if 'eval_queue' not in store: store['eval_queue'] = []
            store['eval_queue'].append(code)
        else:
            # For lite mode, we could inject a script
            cid = self._get_next_cid("page_switch")
            def builder():
                html = f'<script>{code}</script>'
                return Component("div", id=cid, content=html, style="display:none;")
            self._register_component(cid, builder)

    def form(self, key=None, clear_on_submit=False):
        """Create a form container"""
        form_id = f"form_{key}" if key else self._get_next_cid("form")
        
        class FormContext:
            def __init__(self, app, form_id, clear_on_submit):
                self.app = app
                self.form_id = form_id
                self.clear_on_submit = clear_on_submit
                self.submitted = False
                self.form_data = {}
                
            def __enter__(self):
                self.token = fragment_ctx.set(self.form_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                fragment_ctx.reset(self.token)
                
                # Register form builder
                def builder():
                    store = get_session_store()
                    
                    # Render form components
                    htmls = []
                    # Check static
                    for cid, b in self.app.static_fragment_components.get(self.form_id, []):
                        htmls.append(b().render())
                    # Check session
                    for cid, b in store['fragment_components'].get(self.form_id, []):
                        htmls.append(b().render())
                    
                    inner_html = "".join(htmls)
                    html = f'''
                    <form id="{self.form_id}_element" style="display:flex;flex-direction:column;gap:1rem;padding:1rem;border:1px solid var(--sl-border);border-radius:0.5rem;background:var(--sl-bg-card);">
                        {inner_html}
                    </form>
                    '''
                    return Component("div", id=self.form_id, content=html)
                
                self.app._register_component(self.form_id, builder)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return FormContext(self, form_id, clear_on_submit)

    def form_submit_button(self, label="Submit", on_click=None, cls: str = "", style: str = "", **props):
        """Form submit button"""
        cid = self._get_next_cid("form_submit")
        
        def action():
            # Collect form data and call on_click
            if on_click:
                on_click()
        
        def builder():
            attrs = self.engine.click_attrs(cid)
            html = f'''
            <sl-button type="submit" variant="primary" **{attrs}>
                <sl-icon slot="prefix" name="check-circle"></sl-icon>
                {label}
            </sl-button>
            '''
            _wd = self._get_widget_defaults("form_submit_button")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style("display:flex; justify-content:center;", _wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder, action=action)

    def save_file(self, data, file_path, toast_message=None):
        """Save data to local file system
        
        Args:
            data: Data to save (str, bytes, or file-like object)
            file_path: Path where to save the file
            toast_message: Optional success message to show
        
        Returns:
            bool: True if successful, False otherwise
        """
        import os
        
        try:
            # Convert data to bytes if needed
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            elif isinstance(data, bytes):
                data_bytes = data
            elif hasattr(data, 'read'):
                # File-like object
                data_bytes = data.read()
                if isinstance(data_bytes, str):
                    data_bytes = data_bytes.encode('utf-8')
            else:
                data_bytes = str(data).encode('utf-8')
            
            # Create directory if needed
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Write file
            with open(file_path, 'wb') as f:
                f.write(data_bytes)
            
            # Show toast if message provided
            if toast_message:
                self.toast(toast_message, variant="success", icon="check-circle")
            
            return True
            
        except Exception as e:
            self.toast(f"Failed to save file: {str(e)}", variant="danger", icon="x-circle")
            return False
    
    def download_file(self, data, file_name, mime="application/octet-stream", toast_message=None):
        """Trigger file download (auto-detects Native/Web mode)
        
        Args:
            data: Data to download (str, bytes, or file-like object)
            file_name: Name for the downloaded file
            mime: MIME type of the file
            toast_message: Optional message to show
        
        This is a helper that works in button callbacks.
        For declarative UI, use download_button() instead.
        """
        import os
        
        # Convert data to bytes
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        elif isinstance(data, bytes):
            data_bytes = data
        elif hasattr(data, 'read'):
            data_bytes = data.read()
            if isinstance(data_bytes, str):
                data_bytes = data_bytes.encode('utf-8')
        else:
            data_bytes = str(data).encode('utf-8')
        
        # Check if running in Native mode
        is_native = False
        try:
            import webview
            if len(webview.windows) > 0:
                is_native = True
        except ImportError:
            pass
        
        if is_native:
            # Native Mode: File save dialog
            try:
                import webview
                ext = file_name.split('.')[-1] if '.' in file_name else "*"
                file_types = (f"{ext.upper()} File (*.{ext})", "All files (*.*)")
                
                save_location = webview.windows[0].create_file_dialog(
                    webview.SAVE_DIALOG,
                    save_filename=file_name,
                    file_types=file_types
                )
                
                if save_location:
                    if isinstance(save_location, list):
                        save_location = save_location[0]
                    
                    with open(save_location, "wb") as f:
                        f.write(data_bytes)
                    
                    msg = toast_message or f"Saved to {os.path.basename(save_location)}"
                    self.toast(msg, variant="success")
                    
            except Exception as e:
                self.toast(f"Save failed: {str(e)}", variant="danger")
        else:
            # Web Mode: JavaScript download
            import base64
            data_b64 = base64.b64encode(data_bytes).decode('utf-8')
            
            from ..state import get_session_store
            store = get_session_store()
            if 'eval_queue' not in store:
                store['eval_queue'] = []
            
            js_code = f"""
            (function() {{
                const a = document.createElement('a');
                a.href = 'data:{mime};base64,{data_b64}';
                a.download = '{file_name}';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }})();
            """
            store['eval_queue'].append(js_code)
            
            msg = toast_message or f"Downloading {file_name}"
            self.toast(msg, variant="success")
