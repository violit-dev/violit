"""Form Widgets Mixin for Violit"""

from typing import Union, Callable, Optional
from ..component import Component
from ..context import rendering_ctx, fragment_ctx
from ..state import get_session_store
from ..style_utils import auto_split_widget_cls, merge_cls, merge_style, merge_part_cls, serialize_part_cls


class FormWidgetsMixin:
    """Form-related widgets (form, form_submit_button, button, download_button, link_button, page_link)"""

    @staticmethod
    def _wa_button_theme(variant: str):
        variant_map = {
            "primary": ("brand", "accent"),
            "default": ("neutral", "outlined"),
            "secondary": ("neutral", "outlined"),
            "text": ("neutral", "plain"),
            "success": ("success", "accent"),
            "warning": ("warning", "accent"),
            "danger": ("danger", "accent"),
        }
        return variant_map.get(variant, ("neutral", "outlined"))
    
    def button(self, text: Union[str, Callable], on_click: Optional[Callable] = None,
               variant="primary", type="primary",
               disabled=False, use_container_width=False, icon=None,
               cls: str = "", style: str = "", height: Union[str, int, float] = "auto", **props):
        """Display button

        Args:
            type: Streamlit button type - "primary", "secondary", "tertiary" (maps to Web Awesome variant)
            disabled: If True, button is grayed out
            use_container_width: If True, button spans the full container width
            icon: Icon name (Font Awesome/Web Awesome icon, e.g. "gear", "circle-plus", or emoji)
            height: Button height - "auto", "fill", or any CSS size value
        """
        # Streamlit compat: map type to variant
        _type_map = {"primary": "primary", "secondary": "default", "tertiary": "text"}
        _variant = _type_map.get(type, variant) if type != "primary" or variant == "primary" else variant
        if type != "primary": _variant = _type_map.get(type, "primary")

        cid = self._get_next_cid("btn")
        user_part_cls = props.pop("part_cls", None)
        def builder():
            token = rendering_ctx.set(cid)
            bt = text() if callable(text) else text
            rendering_ctx.reset(token)
            attrs = self.engine.click_attrs(cid)
            theme_variant, appearance = self._wa_button_theme(_variant)
            icon_html = f'<wa-icon slot="start" name="{icon}"></wa-icon>' if icon and not any(ord(c) > 127 for c in str(icon)) else ''
            icon_emoji = f'{icon} ' if icon and any(ord(c) > 127 for c in str(icon)) else ''
            disabled_attr = 'disabled' if disabled else ''
            _wd = self._get_widget_defaults("button")
            default_host_cls, default_auto_part_cls = auto_split_widget_cls("button", _wd.get("cls", ""))
            user_host_cls, user_auto_part_cls = auto_split_widget_cls("button", cls)
            _fc = merge_cls(default_host_cls, user_host_cls, "vl-button-fill" if height == "fill" else "")
            _fs = merge_style(_wd.get("style", ""), style)
            _part_cls = merge_part_cls(default_auto_part_cls, _wd.get("part_cls", {}), user_auto_part_cls, user_part_cls)
            host_style = _fs
            if use_container_width:
                host_style = merge_style(host_style, "width:100%;")
            if height not in (None, "", "auto"):
                if height == "fill":
                    host_style = merge_style(host_style, "height:100%;")
                elif isinstance(height, (int, float)):
                    host_style = merge_style(host_style, f"height:{int(height)}px;")
                else:
                    host_style = merge_style(host_style, f"height:{height};")
            host_props = dict(props)
            part_bridge_script = ""
            if _part_cls:
                host_props["data_vl_part_cls"] = serialize_part_cls(_part_cls)
                part_bridge_script = f'''<script>(function() {{
                    let attempts = 0;
                    const run = function() {{
                        attempts += 1;
                        const el = document.getElementById('{cid}');
                        if (el && el.shadowRoot && window.applyPartStyles) {{
                            window.applyPartStyles(el);
                            return;
                        }}
                        if (attempts < 20) setTimeout(run, 80);
                    }};
                    run();
                }})();</script>'''
            inner = Component("wa-button", id=cid, content=f"{icon_html}{icon_emoji}{bt}",
                              class_=_fc or None, style=host_style or None,
                              variant=theme_variant, appearance=appearance,
                              with_start=bool(icon_html) or None, **attrs, **host_props)
            # Inject disabled attribute manually since Component may not handle it
            inner_html = inner.render()
            if disabled:
                inner_html = inner_html.replace(f'id="{cid}"', f'id="{cid}" disabled', 1)
            inner_html += part_bridge_script
            return Component(None, id=cid, content=inner_html)
        self._register_component(cid, builder, action=on_click)

    def download_button(self, label, data, file_name, mime="text/plain", on_click=None,
                         type="primary", disabled=False, use_container_width=False, icon=None,
                         cls: str = "", style: str = "", **props):
        """Download button (Streamlit-compatible interface)

        Args:
            label: Button label
            data: Data to download (str, bytes, or file-like)
            file_name: Name for the downloaded file
            mime: MIME type of the file
            on_click: Optional callback when button is clicked (called AFTER download)
            type: Button type - "primary" or "secondary"
            disabled: If True, button is grayed out
            use_container_width: If True, button spans full width
            icon: Icon name or emoji
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
                            store['toasts'].append({"message": f"Saved to {os.path.basename(save_location)}", "variant": "success", "icon": "circle-check"})

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
                     <wa-button variant="brand" appearance="accent" hx-post="/action/{cid}" hx-swap="none" hx-trigger="click">
                         <wa-icon slot="start" name="download"></wa-icon>
                         {label}
                     </wa-button>
                     '''
                 else:
                     html = f'''
                     <wa-button variant="brand" appearance="accent" onclick="window.sendAction('{cid}')">
                         <wa-icon slot="start" name="download"></wa-icon>
                         {label}
                     </wa-button>
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
                <wa-button variant="brand" appearance="accent" onclick="download_{cid}()">
                    <wa-icon slot="start" name="download"></wa-icon>
                    {label}
                </wa-button>
                '''
            _wd = self._get_widget_defaults("download_button")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style("display:flex; justify-content:center;", _wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder, action=on_click)

    def link_button(self, label, url, disabled=False, use_container_width=False, icon=None,
                     cls: str = "", style: str = "", **props):
        """Display link button

        Args:
            disabled: If True, button is grayed out
            use_container_width: If True, button spans full width
            icon: Icon name or emoji
        """
        cid = self._get_next_cid("link_btn")

        def builder():
            icon_html = f'<wa-icon slot="start" name="{icon}"></wa-icon>' if icon and not any(ord(c) > 127 for c in str(icon)) else ''
            icon_emoji = f'{icon} ' if icon and any(ord(c) > 127 for c in str(icon)) else ''
            if not icon:
                icon_html = '<wa-icon slot="start" name="arrow-up-right-from-square"></wa-icon>'
            disabled_attr = 'disabled' if disabled else ''
            width_attr = 'style="width:100%;"' if use_container_width else ''
            html = f'''
            <wa-button variant="brand" appearance="accent" href="{url}" target="_blank" with-start {disabled_attr} {width_attr}>
                {icon_html}{icon_emoji}{label}
            </wa-button>
            '''
            _wd = self._get_widget_defaults("link_button")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style("display:flex; justify-content:center;", _wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)

        self._register_component(cid, builder)

    def page_link(self, page, label, icon=None, disabled=False, cls: str = "", style: str = "", **props):
        """Display page navigation link

        Args:
            disabled: If True, link is grayed out and not clickable
        """
        cid = self._get_next_cid("page_link")
        
        def builder():
            icon_html = f'<wa-icon name="{icon}"></wa-icon>' if icon else ""
            disabled_style = "pointer-events:none;opacity:0.5;" if disabled else ""
            html = f'''
            <a href="{page}" style="display:inline-flex;align-items:center;gap:0.5rem;color:var(--vl-primary);text-decoration:none;padding:0.5rem 1rem;border-radius:0.25rem;transition:background 0.2s;{disabled_style}">
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
        """Switch to a different page (navigation).

        Accepts a Page object, page function, page title, url_path slug,
        or hash URL such as '#settings' or '/#settings'.
        """
        target_page = None
        target_key = None
        target_hash = None
        target_url = None

        if hasattr(page, 'key') and hasattr(page, 'url_path') and hasattr(page, 'title'):
            target_page = page
        elif callable(page):
            target_page = getattr(self, '_navigation_pages_by_entry', {}).get(page)
        elif isinstance(page, str):
            page_str = page.strip()
            if not page_str:
                return
            if page_str.startswith('http://') or page_str.startswith('https://'):
                target_url = page_str
            elif page_str.startswith('/#'):
                target_hash = page_str[2:]
            elif page_str.startswith('#'):
                target_hash = page_str[1:]
            else:
                target_page = (
                    getattr(self, '_navigation_pages_by_path', {}).get(page_str)
                    or getattr(self, '_navigation_pages_by_title', {}).get(page_str)
                    or getattr(self, '_navigation_pages_by_title', {}).get(page_str.lower())
                )
                if target_page is None and '/' in page_str:
                    target_url = page_str
                elif target_page is None:
                    target_hash = page_str

        if target_page is not None:
            target_key = target_page.key
            target_hash = target_page.url_path
        elif target_hash and target_key is None:
            resolved = getattr(self, '_navigation_pages_by_path', {}).get(target_hash)
            target_key = resolved.key if resolved is not None else f"page_{target_hash}"

        if target_key and getattr(self, '_navigation_states', None):
            for nav_state in self._navigation_states:
                nav_state.set(target_key)

            code = (
                "(function(){"
                "window._pageScrollPositions=window._pageScrollPositions||{};"
                "if(window._currentPageKey){window._pageScrollPositions[window._currentPageKey]=window.scrollY;}"
                f"window._pendingPageKey='{target_key}';"
                f"window._currentPageKey='{target_key}';"
                f"window.location.hash='{target_hash}';"
                "window.scrollTo(0, window._pageScrollPositions[window._currentPageKey] || 0);"
                "})();"
            )
        else:
            final_url = target_url
            if final_url is None and target_hash is not None:
                final_url = f"/#{target_hash}"
            if final_url is None:
                final_url = str(page)
            code = f"window.location.href = '{final_url}';"

        if self.mode == 'ws':
            store = get_session_store()
            if 'eval_queue' not in store:
                store['eval_queue'] = []
            store['eval_queue'].append(code)
        else:
            cid = self._get_next_cid("page_switch")
            def builder():
                html = f'<script>{code}</script>'
                return Component("div", id=cid, content=html, style="display:none;")
            self._register_component(cid, builder)

    def form(self, key=None, clear_on_submit=False, border=True, enter_to_submit=True):
        """Create a form container

        Args:
            clear_on_submit: If True, clear form inputs after submission
            border: If True, show border around form (default: True)
            enter_to_submit: If True, pressing Enter submits the form (default: True)
        """
        form_id = f"form_{key}" if key else self._get_next_cid("form")
        
        class FormContext:
            def __init__(self, app, form_id, clear_on_submit, border, enter_to_submit):
                self.app = app
                self.form_id = form_id
                self.clear_on_submit = clear_on_submit
                self.border = border
                self.enter_to_submit = enter_to_submit
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
                    border_style = "border:1px solid var(--vl-border);" if self.border else ""
                    if self.enter_to_submit:
                        # Trigger the submit button's onclick (WebSocket action) on Enter,
                        # but skip textareas where Enter should insert a newline.
                        enter_handler = (
                            'onkeydown="if(event.key===\'Enter\'&&!event.shiftKey'
                            '&&event.target.tagName!==\'TEXTAREA\'){'
                            'event.preventDefault();'
                            'var btn=this.querySelector(\'wa-button[type=submit]\');'
                            'if(btn)btn.click();}"'
                        )
                    else:
                        enter_handler = 'onkeydown="if(event.key===\'Enter\')event.preventDefault()"'
                    html = f'''
                    <form id="{self.form_id}_element" {enter_handler} onsubmit="return false;" style="display:flex;flex-direction:column;gap:1rem;padding:1rem;{border_style}border-radius:0.5rem;background:var(--vl-bg-card);">
                        {inner_html}
                    </form>
                    '''
                    return Component("div", id=self.form_id, content=html)
                
                self.app._register_component(self.form_id, builder)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
        
        return FormContext(self, form_id, clear_on_submit, border, enter_to_submit)

    def form_submit_button(self, label="Submit", on_click=None,
                            type="primary", disabled=False, use_container_width=False, icon=None,
                            cls: str = "", style: str = "", **props):
        """Form submit button

        Args:
            type: Button type - "primary" or "secondary"
            disabled: If True, button is grayed out
            use_container_width: If True, button spans full width
            icon: Icon name or emoji
        """
        cid = self._get_next_cid("form_submit")
        
        def action():
            # Collect form data and call on_click
            if on_click:
                on_click()
        
        def builder():
            attrs = self.engine.click_attrs(cid)
            attrs_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())
            _variant = "default" if type == "secondary" else "primary"
            icon_html = ''
            if icon and not any(ord(c) > 127 for c in str(icon)):
                icon_html = f'<wa-icon slot="start" name="{icon}"></wa-icon>'
            elif icon:
                icon_html = f'{icon} '
            else:
                icon_html = '<wa-icon slot="start" name="circle-check"></wa-icon>'
            disabled_attr = 'disabled' if disabled else ''
            width_attr = 'style="width:100%;"' if use_container_width else ''
            variant, appearance = self._wa_button_theme(type)
            html = f'''
            <wa-button type="submit" variant="{variant}" appearance="{appearance}" with-start {disabled_attr} {width_attr} {attrs_str}>
                {icon_html}
                {label}
            </wa-button>
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
                self.toast(toast_message, variant="success", icon="circle-check")
            
            return True
            
        except Exception as e:
            self.toast(f"Failed to save file: {str(e)}", variant="danger", icon="circle-xmark")
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
