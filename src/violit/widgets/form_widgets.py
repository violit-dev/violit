"""Form Widgets Mixin for Violit"""

from typing import Union, Callable, Optional
from ..component import Component
from ..context import rendering_ctx, fragment_ctx
from ..state import get_session_store
from ..style_utils import build_cls


class FormWidgetsMixin:
    """Form-related widgets (form, form_submit_button, button, download_button, link_button, page_link)"""
    
    def button(self, text: Union[str, Callable], on_click: Optional[Callable] = None, 
               variant="primary", icon: str = None, outline: bool = False, 
               loading: bool = False, size: str = "medium", pill: bool = False, cls: str = "", **props):
        """Display button"""
        cid = self._get_next_cid("btn")
        
        # Extract style OUTSIDE builder (safe for multiple renders)
        user_style = props.pop('style', '')
        remaining_props = props.copy()
        
        def builder():
            token = rendering_ctx.set(cid)
            bt = text() if callable(text) else text
            rendering_ctx.reset(token)
            
            attrs_dict = self.engine.click_attrs(cid)
            
            # Build extra attrs
            extra_attrs = []
            if outline:
                extra_attrs.append('outline')
            if loading:
                extra_attrs.append('loading')
            if pill:
                extra_attrs.append('pill')
            
            icon_html = f'<sl-icon slot="prefix" name="{icon}"></sl-icon>' if icon else ''
            
            # Add default Streamlit-like styling: display inline-flex, max-content width
            # Users can override with cls or props
            default_style = "display: inline-flex; width: auto;"
            combined_style = f"{default_style} {user_style}".strip()
            
            final_cls = build_cls(cls, **remaining_props)
            
            attrs_str = ' '.join(f'{k}="{v}"' for k, v in attrs_dict.items())
            
            html = f'''<sl-button id="{cid}" variant="{variant}" size="{size}" 
                {attrs_str} {' '.join(extra_attrs)} class="{final_cls}" style="{combined_style}">
                {icon_html}{bt}
            </sl-button>'''
            
            return Component("span", id=cid, content=html)
        self._register_component(cid, builder, action=on_click)

    def download_button(self, label, data, file_name, mime="text/plain", on_click=None, cls: str = "", **props):
        """Download button (Streamlit-compatible interface)"""
        cid = self._get_next_cid("download_btn")
        
        def builder():
            import base64
            
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            elif isinstance(data, bytes):
                data_bytes = data
            else:
                data_bytes = str(data).encode('utf-8')
            
            data_base64 = base64.b64encode(data_bytes).decode('utf-8')
            data_url = f"data:{mime};base64,{data_base64}"
            
            is_native = False
            try:
                import webview
                if len(webview.windows) > 0:
                    is_native = True
            except ImportError:
                pass
                
            if is_native:
                def native_save_action(v=None):
                    try:
                        import webview
                        import os
                        
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
                            
                            print(f"[Native] Saved to {save_location}")
                            
                            from ..state import get_session_store
                            store = get_session_store()
                            if 'toasts' not in store: store['toasts'] = []
                            store['toasts'].append({"message": f"Saved to {os.path.basename(save_location)}", "variant": "success", "icon": "check-circle"})

                    except Exception as e:
                        print(f"[Native] Save failed: {e}")
                
                pass 
                
            final_cls = build_cls(cls, **props)
            
            if is_native:
                 from ..state import get_session_store
                 store = get_session_store()
                 store['actions'][cid] = native_save_action
                 
                 if self.mode == 'lite':
                     html = f'''
                     <sl-button variant="primary" hx-post="/action/{cid}" hx-swap="none" hx-trigger="click" class="{final_cls}">
                         <sl-icon slot="prefix" name="download"></sl-icon>
                         {label}
                     </sl-button>
                     '''
                 else:
                     html = f'''
                     <sl-button variant="primary" onclick="window.sendAction('{cid}')" class="{final_cls}">
                         <sl-icon slot="prefix" name="download"></sl-icon>
                         {label}
                     </sl-button>
                     '''
            else:
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
                <sl-button variant="primary" onclick="download_{cid}()" class="{final_cls}">
                    <sl-icon slot="prefix" name="download"></sl-icon>
                    {label}
                </sl-button>
                '''
            return Component("div", id=cid, content=html)
        
        self._register_component(cid, builder, action=on_click)

    def link_button(self, label, url, cls: str = "", **props):
        """Display link button"""
        cid = self._get_next_cid("link_btn")
        
        def builder():
            final_cls = build_cls(cls, **props)
            html = f'''
            <sl-button variant="primary" href="{url}" target="_blank" class="{final_cls}">
                <sl-icon slot="prefix" name="box-arrow-up-right"></sl-icon>
                {label}
            </sl-button>
            '''
            return Component("div", id=cid, content=html)
        
        self._register_component(cid, builder)

    def page_link(self, page, label, icon=None, cls: str = "", **props):
        """Display page navigation link"""
        cid = self._get_next_cid("page_link")
        
        def builder():
            icon_html = f'<sl-icon slot="prefix" name="{icon}"></sl-icon>' if icon else ""
            final_cls = build_cls(f"inline-flex ai:center gap:0.5rem color:primary text-decoration:none px:1rem py:0.5rem r:0.25rem transition:background|0.2s {cls}", **props)
            html = f'''
            <a href="{page}" class="{final_cls}">
                {icon_html}
                {label}
            </a>
            '''
            return Component("div", id=cid, content=html)
        
        self._register_component(cid, builder)

    def switch_page(self, page):
        """Switch to a different page (navigation)"""
        code = f"window.location.href = '{page}';"
        if self.mode == 'ws':
            store = get_session_store()
            if 'eval_queue' not in store: store['eval_queue'] = []
            store['eval_queue'].append(code)
        else:
            cid = self._get_next_cid("page_switch")
            def builder():
                html = f'<script>{code}</script>'
                return Component("div", id=cid, content=html, style="display:none;")
            self._register_component(cid, builder)

    def form(self, key=None, clear_on_submit=False, cls: str = "", **props):
        """Create a form container"""
        form_id = f"form_{key}" if key else self._get_next_cid("form")
        
        class FormContext:
            def __init__(self, app, form_id, clear_on_submit, cls, props):
                self.app = app
                self.form_id = form_id
                self.clear_on_submit = clear_on_submit
                self.submitted = False
                self.form_data = {}
                self.cls = cls
                self.props = props
                
            def __enter__(self):
                self.token = fragment_ctx.set(self.form_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                fragment_ctx.reset(self.token)
                
                def builder():
                    store = get_session_store()
                    
                    htmls = []
                    for cid, b in self.app.static_fragment_components.get(self.form_id, []):
                        htmls.append(b().render())
                    for cid, b in store['fragment_components'].get(self.form_id, []):
                        htmls.append(b().render())
                    
                    inner_html = "".join(htmls)
                    
                    final_cls = build_cls(f"flex flex:col gap:1rem p:1rem b:1|solid|border r:0.5rem bg:bg-card {self.cls}", **self.props)
                    
                    html = f'''
                    <form id="{self.form_id}_element" class="{final_cls}">
                        {inner_html}
                    </form>
                    '''
                    return Component("div", id=self.form_id, content=html)
                
                self.app._register_component(self.form_id, builder)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return FormContext(self, form_id, clear_on_submit, cls, props)

    def form_submit_button(self, label="Submit", on_click=None, cls: str = "", **props):
        """Form submit button"""
        cid = self._get_next_cid("form_submit")
        
        def action():
            if on_click:
                on_click()
        
        def builder():
            attrs = self.engine.click_attrs(cid)
            # Convert attrs dict to string
            attrs_str = ' '.join(f'{k}="{v}"' for k, v in attrs.items())
            
            final_cls = build_cls(cls, **props)
            
            html = f'''
            <sl-button type="submit" variant="primary" {attrs_str} class="{final_cls}">
                <sl-icon slot="prefix" name="check-circle"></sl-icon>
                {label}
            </sl-button>
            '''
            return Component("div", id=cid, content=html)
        
        self._register_component(cid, builder, action=action)

    def save_file(self, data, file_path, toast_message=None):
        """Save data to local file system"""
        import os
        
        try:
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
            
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(file_path, 'wb') as f:
                f.write(data_bytes)
            
            if toast_message:
                self.toast(toast_message, variant="success", icon="check-circle")
            
            return True
            
        except Exception as e:
            self.toast(f"Failed to save file: {str(e)}", variant="danger", icon="x-circle")
            return False
    
    def download_file(self, data, file_name, mime="application/octet-stream", toast_message=None):
        """Trigger file download"""
        import os
        
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
        
        is_native = False
        try:
            import webview
            if len(webview.windows) > 0:
                is_native = True
        except ImportError:
            pass
        
        if is_native:
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
