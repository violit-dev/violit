import html as html_lib
import json
import re
from typing import Optional, Union, Callable, Any, Sequence
from ..component import Component
from ..context import fragment_ctx, session_ctx, layout_ctx
from ..state import get_session_store
from ..style_utils import merge_cls, merge_style


def _reset_dynamic_chat_children(message_id: str):
    if session_ctx.get() is None:
        return

    store = get_session_store()
    store['fragment_components'][message_id] = []


def _sanitize_chat_key(value: Any) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", str(value)).strip("_") or "chat"

class ChatWidgetsMixin:
    """Chat-related widgets"""

    def _resolve_chat_scroll_mode(self, auto_scroll: Union[bool, str]) -> str:
        if isinstance(auto_scroll, str):
            normalized = auto_scroll.strip().lower()
            if normalized in {"bottom", "preserve"}:
                return normalized
            if normalized in {"false", "off", "none", "stay"}:
                return "preserve"
            return "bottom"
        return "bottom" if auto_scroll else "preserve"

    def message(
        self,
        body,
        is_user: bool = False,
        key: Optional[str] = None,
        avatar_style: Optional[str] = None,
        logo: Optional[str] = None,
        allow_html: bool = False,
        name: Optional[str] = None,
        avatar: Optional[str] = None,
        thinking: bool = False,
        thinking_label: str = "Thinking...",
        cls: str = "",
        style: str = "",
        **props,
    ):
        """Render one chat bubble with a streamlit-chat-like API surface."""
        del avatar_style, props

        role_name = name or ("user" if is_user else "assistant")
        resolved_avatar = avatar if avatar is not None else logo

        with self.chat_message(
            role_name,
            avatar=resolved_avatar,
            cls=cls,
            style=style,
            thinking=thinking,
            thinking_label=thinking_label,
            key=key,
        ):
            if body is None:
                return
            if allow_html:
                self.html(str(body), unsafe_allow_html=True)
            else:
                self.markdown(str(body))
    
    def chat_message(
        self,
        name: str,
        avatar: Optional[str] = None,
        *,
        width: Union[str, int] = "stretch",
        cls: str = "",
        style: str = "",
        thinking: bool = False,
        thinking_label: str = "Thinking...",
        key: Optional[str] = None,
    ):
        """
        Insert a chat message container.
        
        Streamlit-compatible chat message container.
        """
        cid = self._get_next_cid("chat_message")
        
        class ChatMessageContext:
            def __init__(self, app, message_id, name, avatar, user_cls="", user_style="", thinking=False, thinking_label="Thinking...", key=None):
                self.app = app
                self.message_id = message_id
                self.name = name
                self.avatar = avatar
                self.user_cls = user_cls
                self.user_style = user_style
                self.thinking = thinking
                self.thinking_label = thinking_label
                self.key = key
                self.token = None
                
            def __enter__(self):
                # Register builder
                def builder():
                    store = get_session_store()
                    
                    # Collected content
                    htmls = []
                    seen_child_ids = set()
                    # Check static
                    for cid_child, b in self.app.static_fragment_components.get(self.message_id, []):
                        if cid_child in seen_child_ids:
                            continue
                        seen_child_ids.add(cid_child)
                        htmls.append(b().render())
                    # Check session
                    for cid_child, b in store['fragment_components'].get(self.message_id, []):
                        if cid_child in seen_child_ids:
                            continue
                        seen_child_ids.add(cid_child)
                        htmls.append(b().render())
                    
                    inner_html = "".join(htmls).strip()
                    role = (self.name or "assistant").strip().lower()
                    
                    # determine avatar and background
                    row_justify = "flex-start"
                    bubble_bg = "var(--vl-bg-card)"
                    bubble_border = "1px solid var(--vl-border)"
                    bubble_shadow = "0 12px 28px rgba(15, 23, 42, 0.06)"
                    name_color = "var(--vl-text-muted, #64748b)"
                    avatar_content = ""
                    
                    # Icons handling
                    if self.avatar:
                        if self.avatar.startswith("http") or self.avatar.startswith("data:"):
                            safe_avatar = html_lib.escape(self.avatar, quote=True)
                            avatar_content = f'<img src="{safe_avatar}" style="width:42px;height:42px;border-radius:999px;object-fit:cover;border:1px solid rgba(148, 163, 184, 0.25);">'
                        else:
                            safe_avatar = html_lib.escape(self.avatar)
                            avatar_content = f'<div style="width:42px;height:42px;border-radius:999px;background:linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);border:1px solid rgba(148, 163, 184, 0.25);display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700;color:#334155;">{safe_avatar}</div>'
                    else:
                        if role == "user":
                            avatar_content = '<div style="width:42px;height:42px;border-radius:999px;background:linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);color:white;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px rgba(37, 99, 235, 0.18);"><wa-icon name="user"></wa-icon></div>'
                        elif role == "assistant":
                            avatar_content = '<div style="width:42px;height:42px;border-radius:999px;background:linear-gradient(135deg, #0f172a 0%, #334155 100%);color:white;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px rgba(15, 23, 42, 0.2);"><wa-icon name="sparkles"></wa-icon></div>'
                        else:
                            initial = self.name[0].upper() if self.name else "?"
                            avatar_content = f'<div style="width:42px;height:42px;border-radius:999px;background:linear-gradient(135deg, #64748b 0%, #475569 100%);color:white;display:flex;align-items:center;justify-content:center;font-weight:700;box-shadow:0 10px 24px rgba(71, 85, 105, 0.2);">{html_lib.escape(initial)}</div>'

                    if role == "user":
                        bubble_bg = "linear-gradient(180deg, rgba(37, 99, 235, 0.12) 0%, rgba(37, 99, 235, 0.07) 100%)"
                        bubble_border = "1px solid rgba(37, 99, 235, 0.18)"
                        bubble_shadow = "0 12px 28px rgba(37, 99, 235, 0.12)"
                        name_color = "#1d4ed8"
                    elif self.thinking:
                        bubble_bg = "linear-gradient(180deg, rgba(15, 23, 42, 0.06) 0%, rgba(148, 163, 184, 0.10) 100%)"
                        bubble_border = "1px solid rgba(148, 163, 184, 0.30)"
                        bubble_shadow = "0 14px 30px rgba(15, 23, 42, 0.08)"

                    if self.thinking and not inner_html:
                        label = html_lib.escape(self.thinking_label)
                        inner_html = f'''
                        <div class="vl-chat-thinking" style="display:flex;align-items:center;gap:0.8rem;min-height:1.4rem;">
                            <wa-spinner style="font-size:1rem;--indicator-color: var(--vl-accent, #2563eb);"></wa-spinner>
                            <div>
                                <div style="font-weight:600;color:var(--vl-text);">{label}</div>
                                <div style="font-size:0.88rem;color:var(--vl-text-muted, #64748b);margin-top:0.15rem;">The response is being prepared in the background.</div>
                            </div>
                        </div>
                        '''

                    safe_name = html_lib.escape(self.name or "assistant")

                    width_style = ""
                    if isinstance(width, int):
                        width_style = f"max-width:min(100%, {int(width)}px);"
                    elif isinstance(width, str):
                        normalized_width = width.strip().lower()
                        if normalized_width == "content":
                            width_style = "max-width:min(100%, fit-content); width:fit-content;"
                        elif normalized_width != "stretch":
                            width_style = f"max-width:min(100%, {html_lib.escape(normalized_width, quote=True)});"

                    safe_key_attr = ""
                    if self.key:
                        safe_key_attr = f' data-chat-key="{html_lib.escape(str(self.key), quote=True)}"'

                    html = f'''
                    <div class="chat-message chat-message--{role}" data-chat-message="true" data-chat-role="{role}" data-chat-thinking="{'true' if self.thinking else 'false'}"{safe_key_attr} style="display:flex; gap:14px; align-items:flex-start; justify-content:{row_justify}; margin-bottom:18px;">
                        <div class="chat-avatar" style="flex-shrink:0; padding-top:2px;">
                           {avatar_content}
                        </div>
                        <div class="chat-content" style="flex:1; min-width:0; overflow-wrap:break-word; display:flex; flex-direction:column; gap:0.5rem; {width_style}">
                            <div class="chat-author" style="font-size:0.8rem; letter-spacing:0.03em; text-transform:uppercase; font-weight:700; color:{name_color}; padding:0 0.2rem;">{safe_name}</div>
                            <div class="chat-bubble" style="background:{bubble_bg}; border:{bubble_border}; box-shadow:{bubble_shadow}; border-radius:20px; padding:16px 18px; color:var(--vl-text); line-height:1.6;">
                                {inner_html}
                            </div>
                        </div>
                    </div>
                    '''
                    _wd = self.app._get_widget_defaults("chat_message")
                    _fc = merge_cls(_wd.get("cls", ""), self.user_cls)
                    _fs = merge_style(_wd.get("style", ""), self.user_style)
                    return Component("div", id=self.message_id, content=html, class_=_fc or None, style=_fs or None)
                
                self.app._register_component(self.message_id, builder)
                _reset_dynamic_chat_children(self.message_id)
                
                self.token = fragment_ctx.set(self.message_id)
                return self
                
            def __exit__(self, exc_type, exc_val, exc_tb):
                if self.token:
                    fragment_ctx.reset(self.token)
            
            def __getattr__(self, name):
                return getattr(self.app, name)
                
        return ChatMessageContext(self, cid, name, avatar, cls, style, thinking, thinking_label, key)

    def chat_thread(
        self,
        height: Union[int, str] = "58vh",
        cls: str = "",
        style: str = "",
        border: bool = False,
        **kwargs,
    ):
        """Create a dedicated chat conversation surface.

        This is the recommended container for rendering chat messages. It provides
        a scrollable thread surface with stable spacing and is designed to work
        with chat_input(auto_scroll=...).
        """
        surface_style = merge_style(
            """
            border-radius: 24px;
            padding: 0.25rem 0.35rem 0.5rem;
            background: linear-gradient(180deg, rgba(248, 250, 252, 0.82), rgba(255, 255, 255, 0.94));
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7);
            """,
            style,
        )
        surface_cls = merge_cls("vl-chat-thread", cls)
        return self.container(
            border=border,
            height=height,
            cls=surface_cls,
            style=surface_style,
            data_chat_thread="true",
            **kwargs,
        )

    def chat_input(
        self,
        placeholder: str = "Your message",
        *,
        key: Optional[Union[str, int]] = None,
        max_chars: Optional[int] = None,
        accept_file: Union[bool, str] = False,
        file_type: Optional[Union[str, Sequence[str]]] = None,
        accept_audio: bool = False,
        audio_sample_rate: Optional[int] = 16000,
        disabled: bool = False,
        on_submit: Optional[Callable[..., None]] = None,
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[dict[str, Any]] = None,
        width: Union[str, int] = "stretch",
        height: Union[str, int] = "content",
        auto_scroll: Union[bool, str] = True,
        cls: str = "",
        style: str = "",
        multiline: bool = True,
        submit_on_enter: bool = True,
        pinned: Optional[bool] = None,
        scroll_behavior: str = "smooth",
    ):
        """
        Streamlit-compatible chat input widget.
        """
        if accept_file:
            raise NotImplementedError("accept_file is not supported yet by violit.chat_input.")
        if accept_audio:
            raise NotImplementedError("accept_audio is not supported yet by violit.chat_input.")
        del file_type, audio_sample_rate

        cid = f"chat_input_{_sanitize_chat_key(key)}" if key is not None else self._get_next_cid("chat_input")
        store = get_session_store()
        callback_args = tuple(args or ())
        callback_kwargs = dict(kwargs or {})
        effective_pinned = (layout_ctx.get() == "main") if pinned is None else bool(pinned)
        
        # Register action handler in session store (not static_actions)
        # This ensures each session has its own handler
        def handler(val):
            if not on_submit:
                return
            if isinstance(val, str):
                val = val.strip()
            if val:
                on_submit(*callback_args, val, **callback_kwargs)
        
        # Use static_actions for initial registration, but the handler
        # captures the session-specific on_submit callback via closure
        self.static_actions[cid] = handler
            
        def builder():
            # Fixed bottom input
            # We use window.lastActiveChatInput to restore focus after re-render/replacement
            placeholder_js = json.dumps(placeholder)
            submit_on_enter_js = "true" if submit_on_enter else "false"
            scroll_mode = self._resolve_chat_scroll_mode(auto_scroll)
            scroll_mode_js = json.dumps(scroll_mode)
            scroll_behavior_js = json.dumps(scroll_behavior)
            width_style = "width: 100%;"
            if isinstance(width, int):
                width_style = f"width: min(100%, {int(width)}px);"

            min_height_px = 48
            max_height_px = 180 if multiline else 48
            if isinstance(height, int):
                min_height_px = max(48, int(height))
            elif isinstance(height, str):
                normalized_height = height.strip().lower()
                if normalized_height == "stretch":
                    min_height_px = 96

            if effective_pinned:
                container_style = '''
                position: fixed;
                bottom: 0;
                left: 300px;
                right: 0;
                padding: 18px 20px 22px;
                background: linear-gradient(to top, color-mix(in srgb, var(--vl-bg) 94%, transparent) 68%, transparent 100%);
                backdrop-filter: blur(10px);
                z-index: 1000;
                display: flex;
                justify-content: center;
                pointer-events: none;
                transition: left 0.3s ease;
                '''
                spacer_html = '<div style="height: 124px;"></div>'
            else:
                container_style = '''
                position: relative;
                padding: 0;
                display: flex;
                justify-content: center;
                width: 100%;
                pointer-events: none;
                '''
                spacer_html = ""
            
            html = f'''
            <div class="chat-input-container" style="
                {container_style}
            ">
                <div data-chat-input-root="{cid}" style="
                    {width_style}
                    max-width: 860px;
                    background: color-mix(in srgb, var(--vl-bg-card) 92%, white 8%);
                    border: 1px solid color-mix(in srgb, var(--vl-border) 80%, transparent);
                    border-radius: 24px;
                    padding: 10px;
                    box-shadow: 0 20px 40px rgba(15, 23, 42, 0.10);
                    display: flex;
                    align-items: flex-end;
                    gap: 10px;
                    pointer-events: auto;
                ">
                    <textarea id="input_{cid}" class="chat-input-box" placeholder={placeholder_js}
                        rows="1"
                        {"maxlength=" + '"' + str(max_chars) + '"' if max_chars else ""}
                        {"disabled" if disabled else ""}
                        style="
                            flex: 1;
                            border: none;
                            background: transparent;
                            padding: 10px 12px;
                            font-size: 1rem;
                            color: var(--vl-text);
                            outline: none;
                            resize: none;
                            min-height: {min_height_px}px;
                            max-height: {max_height_px}px;
                            line-height: 1.5;
                            font-family: inherit;
                        "
                    ></textarea>
                    <wa-button size="small" variant="brand" appearance="accent" {"disabled" if disabled else ""} onclick="
                        window.submitChatInput_{cid}();
                    ">
                        <wa-icon name="send" label="Send"></wa-icon>
                    </wa-button>
                </div>
            </div>
            {spacer_html}
            <script>
                (function() {{
                    const el = document.getElementById('input_{cid}');
                    const root = document.querySelector('[data-chat-input-root="{cid}"]');
                    if (!el) return;

                    const autoResize = () => {{
                        el.style.height = 'auto';
                        el.style.height = Math.min(el.scrollHeight, {max_height_px}) + 'px';
                    }};

                    const scrollMode = {scroll_mode_js};
                    const scrollBehavior = {scroll_behavior_js};

                    const findScrollableAncestor = (node) => {{
                        let current = node ? node.parentElement : null;
                        while (current) {{
                            const styles = window.getComputedStyle(current);
                            const overflowY = styles.overflowY;
                            const canScroll = ['auto', 'scroll', 'overlay'].includes(overflowY);
                            if (canScroll && current.scrollHeight > current.clientHeight + 4) {{
                                return current;
                            }}
                            current = current.parentElement;
                        }}
                        return null;
                    }};

                    const latestChatTarget = () => {{
                        if (!root) return el;
                        const messages = Array.from(document.querySelectorAll('[data-chat-message="true"]'));
                        let candidate = null;
                        for (const node of messages) {{
                            const position = node.compareDocumentPosition(root);
                            if (position & Node.DOCUMENT_POSITION_FOLLOWING) {{
                                candidate = node;
                            }}
                        }}
                        return candidate || root;
                    }};

                    const maybeScrollToLatest = () => {{
                        if (scrollMode !== 'bottom') return;
                        const target = latestChatTarget();
                        if (!target) return;
                        const scrollParent = findScrollableAncestor(target) || findScrollableAncestor(root);
                        if (scrollParent) {{
                            const parentRect = scrollParent.getBoundingClientRect();
                            const targetRect = target.getBoundingClientRect();
                            const nextTop = scrollParent.scrollTop + (targetRect.bottom - parentRect.top) - scrollParent.clientHeight + 16;
                            scrollParent.scrollTo({{ top: Math.max(nextTop, 0), behavior: scrollBehavior }});
                            return;
                        }}
                        if (typeof target.scrollIntoView === 'function') {{
                            target.scrollIntoView({{ block: 'end', behavior: scrollBehavior, inline: 'nearest' }});
                        }}
                    }};

                    const scheduleScrollToLatest = () => {{
                        if (window.__violitChatScrollFrame_{cid}) {{
                            cancelAnimationFrame(window.__violitChatScrollFrame_{cid});
                        }}
                        window.__violitChatScrollFrame_{cid} = requestAnimationFrame(() => {{
                            maybeScrollToLatest();
                        }});
                    }};

                    window.submitChatInput_{cid} = function() {{
                        if ({'true' if disabled else 'false'}) return;
                        const rawValue = el.value || '';
                        const trimmed = rawValue.trim();
                        if (!trimmed) {{
                            el.focus();
                            return;
                        }}
                        window.lastActiveChatInput = 'input_{cid}';
                        {f"window.sendAction('{cid}', trimmed);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: trimmed}}, swap: 'none'}});"}
                        el.value = '';
                        autoResize();
                    }};

                    if (!el.dataset.chatReady) {{
                        el.dataset.chatReady = 'true';
                        el.addEventListener('input', autoResize);
                        el.addEventListener('keydown', function(event) {{
                            if ({submit_on_enter_js} && event.key === 'Enter' && !event.shiftKey) {{
                                event.preventDefault();
                                window.submitChatInput_{cid}();
                            }}
                        }});
                    }}

                    if (window.__violitChatObserver_{cid}) {{
                        window.__violitChatObserver_{cid}.disconnect();
                    }}

                    window.__violitChatObserver_{cid} = new MutationObserver((mutationList) => {{
                        if (scrollMode !== 'bottom') return;
                        for (const mutation of mutationList) {{
                            if (mutation.type === 'childList' || mutation.type === 'characterData') {{
                                scheduleScrollToLatest();
                                break;
                            }}
                        }}
                    }});

                    window.__violitChatObserver_{cid}.observe(document.body, {{
                        childList: true,
                        subtree: true,
                        characterData: true,
                    }});

                    autoResize();

                    setTimeout(scheduleScrollToLatest, 100);
                    setTimeout(scheduleScrollToLatest, 320);

                    if (window.lastActiveChatInput === 'input_{cid}') {{
                        setTimeout(() => {{
                            el.focus();
                            window.lastActiveChatInput = null;
                        }}, 120);
                    }}
                }})();
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
        
        val = store.get('submitted_values', {}).pop(cid, None)
        
        # To prevent stale values on subsequent non-related runs (e.g. other buttons),
        # we ideally need to know 'who' triggered the run.
        # But for now, returning what's in store is the best approximation.
        # If another button is clicked, `store['actions']` might still have this cid's old value 
        # if we don't clear it. 
        # However, `store['actions']` is persistent in the current `app.py` logic?
        # Let's check app.py action handler. 
        
        return val
