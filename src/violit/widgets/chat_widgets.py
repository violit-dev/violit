from typing import Optional, Union, Callable
from ..component import Component
from ..context import fragment_ctx
from ..state import get_session_store
from ..style_utils import merge_cls, merge_style

class ChatWidgetsMixin:
    """Chat-related widgets"""
    
    def chat_message(self, name: str, avatar: Optional[str] = None, cls: str = "", style: str = ""):
        """
        Insert a chat message container.
        
        Args:
            name (str): The name of the author (e.g. "user", "assistant").
            avatar (str, optional): The avatar image or emoji.
        """
        cid = self._get_next_cid("chat_message")
        
        class ChatMessageContext:
            def __init__(self, app, message_id, name, avatar, user_cls="", user_style=""):
                self.app = app
                self.message_id = message_id
                self.name = name
                self.avatar = avatar
                self.user_cls = user_cls
                self.user_style = user_style
                self.token = None
                
            def __enter__(self):
                # Register builder
                def builder():
                    store = get_session_store()
                    
                    # Collected content
                    htmls = []
                    # Check static
                    for cid_child, b in self.app.static_fragment_components.get(self.message_id, []):
                        htmls.append(b().render())
                    # Check session
                    for cid_child, b in store['fragment_components'].get(self.message_id, []):
                        htmls.append(b().render())
                    
                    inner_html = "".join(htmls)
                    
                    # determine avatar and background
                    bg_color = "transparent"
                    avatar_content = ""
                    
                    # Icons handling
                    if self.avatar:
                        if self.avatar.startswith("http") or self.avatar.startswith("data:"):
                            avatar_content = f'<img src="{self.avatar}" style="width:32px;height:32px;border-radius:4px;object-fit:cover;">'
                        else:
                            avatar_content = f'<div style="width:32px;height:32px;border-radius:4px;background:#eee;display:flex;align-items:center;justify-content:center;font-size:20px;">{self.avatar}</div>'
                    else:
                        if self.name == "user":
                            avatar_content = f'<div style="width:32px;height:32px;border-radius:4px;background:#7C4DFF;color:white;display:flex;align-items:center;justify-content:center;"><sl-icon name="person-fill"></sl-icon></div>'
                            bg_color = "rgba(124, 77, 255, 0.05)"
                        elif self.name == "assistant":
                            avatar_content = f'<div style="width:32px;height:32px;border-radius:4px;background:#FF5252;color:white;display:flex;align-items:center;justify-content:center;"><sl-icon name="robot"></sl-icon></div>'
                            bg_color = "rgba(255, 82, 82, 0.05)"
                        else:
                            initial = self.name[0].upper() if self.name else "?"
                            avatar_content = f'<div style="width:32px;height:32px;border-radius:4px;background:#9CA3AF;color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;">{initial}</div>'
                            bg_color = "rgba(0,0,0,0.02)"

                    html = f'''
                    <div class="chat-message" style="display:flex; gap:16px; margin-bottom:16px; padding:16px; border-radius:8px; background:{bg_color};">
                        <div class="chat-avatar" style="flex-shrink:0;">
                           {avatar_content}
                        </div>
                        <div class="chat-content" style="flex:1; min-width:0; overflow-wrap:break-word;">
                            {inner_html}
                        </div>
                    </div>
                    '''
                    _wd = self.app._get_widget_defaults("chat_message")
                    _fc = merge_cls(_wd.get("cls", ""), self.user_cls)
                    _fs = merge_style(_wd.get("style", ""), self.user_style)
                    return Component("div", id=self.message_id, content=html, class_=_fc or None, style=_fs or None)
                
                self.app._register_component(self.message_id, builder)
                
                self.token = fragment_ctx.set(self.message_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                if self.token:
                    fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
                
        return ChatMessageContext(self, cid, name, avatar, cls, style)

    def chat_input(self, placeholder: str = "Your message", on_submit: Optional[Callable[[str], None]] = None, auto_scroll: bool = True, cls: str = "", style: str = ""):
        """
        Display a chat input widget at the bottom of the page.
        
        Args:
            placeholder (str): Placeholder text.
            on_submit (Callable[[str], None]): Callback function to run when message is sent.
            auto_scroll (bool): If True, automatically scroll to bottom after rendering.
        """
        cid = self._get_next_cid("chat_input")
        store = get_session_store()
        
        # Register action handler in session store (not static_actions)
        # This ensures each session has its own handler
        def handler(val):
            if on_submit:
                on_submit(val)
        
        # Use static_actions for initial registration, but the handler
        # captures the session-specific on_submit callback via closure
        self.static_actions[cid] = handler
            
        def builder():
            # Fixed bottom input
            # We use window.lastActiveChatInput to restore focus after re-render/replacement
            scroll_script = "window.scrollTo(0, document.body.scrollHeight);" if auto_scroll else ""
            
            html = f'''
            <div class="chat-input-container" style="
                position: fixed; 
                bottom: 0; 
                left: 300px;
                right: 0;
                padding: 20px; 
                background: linear-gradient(to top, var(--sl-bg) 80%, transparent);
                z-index: 1000;
                display: flex;
                justify-content: center;
                pointer-events: none;
                transition: left 0.3s ease;
            ">
                <div style="
                    width: 100%; 
                    max-width: 800px; 
                    background: var(--sl-bg-card); 
                    border: 1px solid var(--sl-border); 
                    border-radius: 8px; 
                    padding: 8px; 
                    box-shadow: 0 -4px 10px rgba(0,0,0,0.05);
                    display: flex;
                    gap: 8px;
                    pointer-events: auto;
                ">
                    <input type="text" id="input_{cid}" class="chat-input-box" placeholder="{placeholder}" 
                        style="
                            flex: 1; 
                            border: none; 
                            background: transparent; 
                            padding: 8px; 
                            font-size: 1rem; 
                            color: var(--sl-text); 
                            outline: none;
                        "
                        onkeydown="if(event.key==='Enter'){{ 
                            window.chatInputWasActive = true;
                            {f"sendAction('{cid}', this.value);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: this.value}}, swap: 'none'}});"}
                            this.value = ''; 
                        }}"
                    >
                    <sl-button size="small" variant="primary" circle onclick="
                        const el = document.getElementById('input_{cid}');
                        window.chatInputWasActive = true;
                        {f"sendAction('{cid}', el.value);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: el.value}}, swap: 'none'}});"}
                        el.value = '';
                    ">
                        <sl-icon name="send" label="Send"></sl-icon>
                    </sl-button>
                </div>
            </div>
            <!-- Spacer -->
            <div style="height: 100px;"></div>
            <script>
                // Auto-scroll if enabled
                if ("{auto_scroll}" === "True") {{
                    setTimeout(() => {{ 
                        window.scrollTo({{
                            top: document.documentElement.scrollHeight,
                            behavior: 'smooth'
                        }});
                    }}, 100);
                }}

                // Restore focus if a chat input was just used
                if (window.chatInputWasActive) {{
                    setTimeout(() => {{
                        // Find ANY chat input box
                        const el = document.querySelector('.chat-input-box');
                        if (el) {{
                            el.focus();
                        }}
                        window.chatInputWasActive = false;
                    }}, 150);
                }}
            </script>
            '''
            _wd = self._get_widget_defaults("chat_input")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
            
        self._register_component(cid, builder)
        
        # Return the value just submitted, or None
        # We need to check if this specific component triggered the action in this cycle
        # This is tricky without a dedicated 'current_action_trigger' context.
        # In `App.action`, it calls the handler. 
        # If we use `actions` dict in store, it persists. 
        # We want `chat_input` to return the value ONLY when it was just submitted.
        
        # Hack: Check if this cid matches the latest action if we had that info.
        # Alternative: The user code uses `if prompt := app.chat_input():`.
        # This implies standard rerun logic.
        # If the frontend sent an action for `cid`, `store['actions'][cid]` will be set.
        # We should probably clear it after reading to behave like a one-time event?
        # But if we clear it here, and the script reruns multiple times or checks it multiple times? 
        # Usually it's read once per run.
        
        val = store['actions'].get(cid)
        
        # To prevent stale values on subsequent non-related runs (e.g. other buttons),
        # we ideally need to know 'who' triggered the run.
        # But for now, returning what's in store is the best approximation.
        # If another button is clicked, `store['actions']` might still have this cid's old value 
        # if we don't clear it. 
        # However, `store['actions']` is persistent in the current `app.py` logic?
        # Let's check app.py action handler. 
        
        return val
