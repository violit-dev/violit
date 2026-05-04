import html as html_lib
import asyncio
import json
import re
import time
from typing import Optional, Union, Callable, Any, Sequence
from ..component import Component
from ..context import fragment_ctx, session_ctx, view_ctx, layout_ctx
from ..state import get_session_store
from ..style_utils import merge_cls, merge_style


def _reset_dynamic_chat_children(message_id: str):
    if session_ctx.get() is None:
        return

    store = get_session_store()
    store['fragment_components'][message_id] = []


def _sanitize_chat_key(value: Any) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", str(value)).strip("_") or "chat"


def _clone_chat_items(messages_state):
    return [dict(item) for item in messages_state.value]


def _patch_last_chat_item(messages_state, **updates):
    items = _clone_chat_items(messages_state)
    if not items:
        return
    items[-1] = {**items[-1], **updates}
    messages_state.set(items)


def _push_stream_frame(app):
    sid = session_ctx.get()
    current_view_id = view_ctx.get()
    if not sid or not current_view_id:
        return

    dirty = app._get_dirty_rendered()
    if not dirty:
        return

    if app.ws_engine and app.ws_engine.has_socket(sid, current_view_id):
        main_loop = getattr(app, "_main_loop", None)
        if main_loop is not None and main_loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                app.ws_engine.push_updates(sid, dirty, view_id=current_view_id),
                main_loop,
            )
            future.result(timeout=5)
            return

        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(app.ws_engine.push_updates(sid, dirty, view_id=current_view_id))
        finally:
            loop.close()
        return

    if app.lite_engine:
        payload = app._build_lite_oob_payload(dirty)
        if payload:
            app._enqueue_lite_stream_payload(sid, payload, view_id=current_view_id)


def _iter_stream_text_fragments(text: str, preferred_size: int = 12, mode: str = "chunk"):
    if not text:
        return

    normalized_mode = (mode or "chunk").strip().lower()

    if normalized_mode == "raw":
        yield text
        return

    if normalized_mode == "char":
        for char in text:
            yield char
        return

    tokens = re.findall(r"\S+\s*|\s+", text)
    if normalized_mode == "word":
        for token in tokens:
            yield token
        return

    for token in tokens:
        if len(token) <= preferred_size:
            yield token
            continue

        for start in range(0, len(token), preferred_size):
            yield token[start:start + preferred_size]


def _resolve_stream_speed_value(stream_speed: Any) -> Optional[str]:
    candidate = stream_speed.value if hasattr(stream_speed, "value") else stream_speed
    if callable(candidate) and not isinstance(candidate, str):
        candidate = candidate()
    if candidate is None:
        return None
    return str(candidate)


def _resolve_stream_profile(stream_speed: Optional[str], flush_interval: float):
    fallback_delay = max(0.01, float(flush_interval))
    normalized = (stream_speed or "balanced").strip().lower()

    profiles = {
        "fast": {"delay": 0.0, "fragment_size": 9999, "fragment_mode": "raw", "punctuation_pause": 0.0, "space_pause": 0.0, "flush_interval": 0.01, "emit_interval": 0.0, "emit_chars": 9999, "emit_on_punctuation": True},
        "snappy": {"delay": 0.0, "fragment_size": 9999, "fragment_mode": "raw", "punctuation_pause": 0.0, "space_pause": 0.0, "flush_interval": 0.01, "emit_interval": 0.0, "emit_chars": 9999, "emit_on_punctuation": True},
        "balanced": {"delay": 0.012, "fragment_size": 9999, "fragment_mode": "word", "punctuation_pause": 0.02, "space_pause": 0.0, "flush_interval": 0.02, "emit_interval": 0.028, "emit_chars": 20, "emit_on_punctuation": True},
        "default": {"delay": 0.012, "fragment_size": 9999, "fragment_mode": "word", "punctuation_pause": 0.02, "space_pause": 0.0, "flush_interval": 0.02, "emit_interval": 0.028, "emit_chars": 20, "emit_on_punctuation": True},
        "normal": {"delay": 0.012, "fragment_size": 9999, "fragment_mode": "word", "punctuation_pause": 0.02, "space_pause": 0.0, "flush_interval": 0.02, "emit_interval": 0.028, "emit_chars": 20, "emit_on_punctuation": True},
        "smooth": {"delay": 0.03, "fragment_size": 2, "fragment_mode": "chunk", "punctuation_pause": 0.06, "space_pause": 0.01, "flush_interval": 0.03, "emit_interval": 0.05, "emit_chars": 4, "emit_on_punctuation": True},
        "slow": {"delay": 0.03, "fragment_size": 2, "fragment_mode": "chunk", "punctuation_pause": 0.06, "space_pause": 0.01, "flush_interval": 0.03, "emit_interval": 0.05, "emit_chars": 4, "emit_on_punctuation": True},
        "cinematic": {"delay": 0.085, "fragment_size": 1, "fragment_mode": "char", "punctuation_pause": 0.18, "space_pause": 0.03, "flush_interval": 0.05, "emit_interval": 0.09, "emit_chars": 1, "emit_on_punctuation": True},
        "dramatic": {"delay": 0.085, "fragment_size": 1, "fragment_mode": "char", "punctuation_pause": 0.18, "space_pause": 0.03, "flush_interval": 0.05, "emit_interval": 0.09, "emit_chars": 1, "emit_on_punctuation": True},
    }
    profile = profiles.get(normalized)
    if profile is not None:
        return profile
    return {"delay": fallback_delay, "fragment_size": 18, "fragment_mode": "chunk", "punctuation_pause": 0.0, "space_pause": 0.0, "flush_interval": min(0.04, fallback_delay), "emit_interval": max(0.02, fallback_delay), "emit_chars": 18, "emit_on_punctuation": True}


def _stream_fragment_pause(fragment: str, base_delay: float, punctuation_pause: float, space_pause: float = 0.0) -> float:
    pause = max(0.0, float(base_delay))
    if space_pause > 0 and fragment.isspace():
        pause += space_pause
        return pause
    if punctuation_pause <= 0:
        return pause
    if any(mark in fragment for mark in (".", "!", "?", ";", ":", "\n")):
        pause += punctuation_pause
    elif "," in fragment:
        pause += punctuation_pause * 0.5
    return pause


def _should_emit_stream_frame(profile: dict[str, float], last_emit_at: float, pending_chars: int, fragment: str) -> bool:
    force_on_punctuation = bool(profile.get("emit_on_punctuation", False))
    min_emit_interval = max(0.0, float(profile.get("emit_interval", 0.0)))
    min_emit_chars = max(1, int(profile.get("emit_chars", 1)))

    if force_on_punctuation and any(mark in fragment for mark in (".", "!", "?", ";", ":", "\n")):
        return True
    if pending_chars >= min_emit_chars:
        return True
    if min_emit_interval <= 0:
        return True
    return (time.perf_counter() - last_emit_at) >= min_emit_interval

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

    def chat_messages(
        self,
        messages,
        *,
        height: Union[int, str] = "58vh",
        cursor: Optional[str] = "|",
        cls: str = "",
        style: str = "",
        border: bool = False,
    ):
        """Render chat history from a list-like state using Violit chat widgets."""
        items = messages.value if hasattr(messages, "value") else messages
        with self.chat_thread(height=height, cls=cls, style=style, border=border):
            for item in items or []:
                role = item.get("role", "assistant") if isinstance(item, dict) else "assistant"
                with self.chat_message(role):
                    chunks = item.get("chunks") if isinstance(item, dict) else None
                    status = item.get("status") if isinstance(item, dict) else None
                    content = item.get("content") if isinstance(item, dict) else str(item)
                    if chunks:
                        if isinstance(chunks, (list, tuple)) and all(isinstance(chunk, str) for chunk in chunks):
                            streamed_text = "".join(chunks)
                            if status == "streaming" and cursor:
                                streamed_text += str(cursor)
                            self.markdown(streamed_text)
                        else:
                            self.write_stream(chunks, cursor=cursor if status == "streaming" else None)
                    elif content:
                        self.markdown(content)
                    else:
                        self.caption(item.get("thinking_label", "Thinking...") if isinstance(item, dict) else "Thinking...")

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
        on_submit: Optional[Callable[..., Any]] = None,
        messages: Optional[Any] = None,
        user_name: str = "user",
        assistant_name: str = "assistant",
        stream_cursor: Optional[str] = "|",
        stream_speed: Any = None,
        flush_interval: float = 0.01,
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
        Violit chat input widget with a Streamlit-like surface.

        If `messages` is provided and `on_submit` returns a string, the string
        becomes the assistant reply. If it returns an iterable, the iterable is
        streamed into the assistant bubble automatically.

        `stream_speed` accepts presets like "fast", "balanced", "smooth",
        "cinematic" or a smoothness score from 1 to 10, where 10 is the
        smoothest. It can also be provided as a State-like object or callable
        so the active preset is resolved when the user submits a message.
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
        if pinned is None:
            # Treat chat_input like a regular widget when it is nested inside
            # a layout fragment (columns, containers, tabs, forms, etc.).
            effective_pinned = layout_ctx.get() == "main" and fragment_ctx.get() is None
        else:
            effective_pinned = bool(pinned)
        # Register action handler in session store (not static_actions)
        # This ensures each session has its own handler
        def handler(val):
            if not on_submit:
                return
            if isinstance(val, str):
                val = val.strip()
            if not val:
                return

            if messages is None:
                on_submit(*callback_args, val, **callback_kwargs)
                return

            messages.set(_clone_chat_items(messages) + [
                {"role": user_name, "content": val, "status": "done"},
                {"role": assistant_name, "content": "", "chunks": [], "status": "thinking"},
            ])

            stream_profile = _resolve_stream_profile(
                _resolve_stream_speed_value(stream_speed),
                flush_interval,
            )

            def run_reply():
                result = on_submit(*callback_args, val, **callback_kwargs)

                if isinstance(result, str):
                    reply = result.strip()
                    if not reply:
                        raise RuntimeError("Chat reply was empty.")
                    _patch_last_chat_item(messages, content=reply, chunks=[], status="done", cursor=None)
                    return reply

                candidate = result() if callable(result) and not hasattr(result, "__iter__") else result
                if not hasattr(candidate, "__iter__"):
                    reply = str(result).strip()
                    if not reply:
                        raise RuntimeError("Chat reply was empty.")
                    _patch_last_chat_item(messages, content=reply, chunks=[], status="done", cursor=None)
                    return reply

                chunks = []
                last_emit_at = time.perf_counter()
                pending_emit_chars = 0
                for raw_chunk in candidate:
                    chunk = self._extract_stream_chunk(raw_chunk)
                    text = chunk if isinstance(chunk, str) else str(chunk)
                    if not text:
                        continue
                    fragments = list(
                        _iter_stream_text_fragments(
                            text,
                            preferred_size=stream_profile["fragment_size"],
                            mode=stream_profile["fragment_mode"],
                        )
                    )
                    for fragment in fragments:
                        chunks.append(fragment)
                        pending_emit_chars += len(fragment)
                        _patch_last_chat_item(messages, chunks=list(chunks), status="streaming", cursor=stream_cursor)
                        if _should_emit_stream_frame(stream_profile, last_emit_at, pending_emit_chars, fragment):
                            _push_stream_frame(self)
                            last_emit_at = time.perf_counter()
                            pending_emit_chars = 0
                        pause = _stream_fragment_pause(
                            fragment,
                            stream_profile["delay"],
                            stream_profile["punctuation_pause"],
                            stream_profile["space_pause"],
                        )
                        if pause > 0:
                            time.sleep(pause)

                if chunks and pending_emit_chars > 0:
                    _push_stream_frame(self)

                reply = "".join(chunks).strip()
                if not reply:
                    raise RuntimeError("Chat reply was empty.")
                _patch_last_chat_item(messages, content=reply, chunks=list(chunks), status="done", cursor=None)
                return reply

            def fail_reply(exc):
                _patch_last_chat_item(
                    messages,
                    content=f"Error:\n\n```text\n{exc}\n```",
                    chunks=[],
                    status="error",
                    cursor=None,
                )

            self.background(
                run_reply,
                on_error=fail_reply,
                flush_interval=stream_profile["flush_interval"],
            ).start()
        
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
            <div class="chat-input-container" data-chat-pinned="{'true' if effective_pinned else 'false'}" style="
                {container_style}
            ">
                <div data-chat-input-root="{cid}" style="
                    {width_style}
                    max-width: 860px;
                    display: flex;
                    align-items: flex-end;
                    gap: 10px;
                    pointer-events: auto;
                ">
                    <div style="
                        flex: 1;
                        min-width: 0;
                        background: color-mix(in srgb, var(--vl-bg-card) 92%, white 8%);
                        border: 1px solid color-mix(in srgb, var(--vl-border) 80%, transparent);
                        border-radius: 24px;
                        padding: 10px;
                        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.10);
                    ">
                        <textarea id="input_{cid}" class="chat-input-box" placeholder={placeholder_js}
                            rows="1"
                            {"maxlength=" + '"' + str(max_chars) + '"' if max_chars else ""}
                            {"disabled" if disabled else ""}
                            style="
                                width: 100%;
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
                                box-sizing: border-box;
                            "
                        ></textarea>
                    </div>
                    <wa-button id="send_{cid}" type="button" size="small" variant="brand" appearance="accent" {"disabled" if disabled else ""} style="flex: 0 0 48px; min-width: 48px; width: 48px; height: 48px; margin-bottom: 2px; --wa-button-padding-inline: 0;" onclick="
                        window.submitChatInput_{cid}();
                    ">
                        <span aria-hidden="true" style="display:flex;align-items:center;justify-content:center;width:100%;height:100%;line-height:0;">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width:1rem;height:1rem;display:block;fill:currentColor;transform:translate(-1.5px, 1px);transform-origin:center;"><path d="M476.6 3.2c18.6 10.5 27.5 32.4 21.8 53.1l-96 352c-4 14.8-18.2 25.3-33.5 25.7s-30-9.1-34.8-23.6l-48.6-145.9-145.9-48.6C125.1 211 115.2 196.4 115.6 181s10.9-29.5 25.7-33.5l352-96c20.7-5.7 42.6 3.2 53.1 21.8zM176.9 177.1l125.4 41.8 41.8 125.4L426.7 41.6 176.9 177.1z"/></svg>
                        </span>
                    </wa-button>
                </div>
            </div>
            {spacer_html}
            <script>
                (function() {{
                    const el = document.getElementById('input_{cid}');
                    const sendButton = document.getElementById('send_{cid}');
                    const root = document.querySelector('[data-chat-input-root="{cid}"]');
                    if (!el) return;

                    const resolveChatScope = () => {{
                        if (!root) return document.body;
                        let current = root.parentElement;
                        while (current) {{
                            if (current.querySelector('[data-chat-thread="true"]')) {{
                                return current;
                            }}
                            current = current.parentElement;
                        }}
                        return root.parentElement || root;
                    }};

                    const chatScope = resolveChatScope();

                    const getChatThread = () => {{
                        if (!chatScope) return null;
                        return chatScope.querySelector('[data-chat-thread="true"]');
                    }};

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
                        const chatThread = getChatThread();
                        if (chatThread) {{
                            const messages = Array.from(chatThread.querySelectorAll('[data-chat-message="true"]'));
                            return messages[messages.length - 1] || chatThread;
                        }}
                        if (!root) return el;
                        return root;
                    }};

                    const maybeScrollToLatest = () => {{
                        if (scrollMode !== 'bottom') return;
                        const target = latestChatTarget();
                        if (!target) return;
                        const chatThread = getChatThread();
                        const scrollParent = chatThread || findScrollableAncestor(target) || findScrollableAncestor(root);
                        if (!scrollParent) return;
                        const syncBottom = () => {{
                            const nextTop = Math.max(scrollParent.scrollHeight - scrollParent.clientHeight, 0);
                            scrollParent.scrollTop = nextTop;
                            scrollParent.scrollTo({{ top: nextTop, behavior: 'auto' }});
                        }};
                        syncBottom();
                        requestAnimationFrame(syncBottom);
                        setTimeout(syncBottom, 80);
                    }};

                    const scheduleScrollToLatest = () => {{
                        if (window.__violitChatScrollFrame_{cid}) {{
                            cancelAnimationFrame(window.__violitChatScrollFrame_{cid});
                        }}
                        window.__violitChatScrollFrame_{cid} = requestAnimationFrame(() => {{
                            maybeScrollToLatest();
                            requestAnimationFrame(maybeScrollToLatest);
                        }});
                    }};

                    const focusInput = () => {{
                        try {{
                            el.focus({{ preventScroll: true }});
                        }} catch (_err) {{
                            el.focus();
                        }}
                    }};

                    const preserveViewport = (position) => {{
                        if (!position) return;
                        const restore = () => {{
                            window.scrollTo(position.x || 0, position.y || 0);
                        }};
                        restore();
                        requestAnimationFrame(() => {{
                            restore();
                            requestAnimationFrame(restore);
                        }});
                        setTimeout(restore, 80);
                    }};

                    const syncSendButtonState = () => {{
                        if (!sendButton || {'true' if disabled else 'false'}) return;
                        const hasValue = !!((el.value || '').trim());
                        sendButton.disabled = !hasValue;
                        sendButton.setAttribute('aria-disabled', hasValue ? 'false' : 'true');
                    }};

                    window.submitChatInput_{cid} = function() {{
                        if ({'true' if disabled else 'false'}) return;
                        const viewport = {{ x: window.scrollX, y: window.scrollY }};
                        const rawValue = el.value || '';
                        const trimmed = rawValue.trim();
                        if (!trimmed) {{
                            if (document.activeElement && typeof document.activeElement.blur === 'function') {{
                                document.activeElement.blur();
                            }}
                            preserveViewport(viewport);
                            return;
                        }}
                        window.lastActiveChatInput = 'input_{cid}';
                        {f"window.sendAction('{cid}', trimmed);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: trimmed, _csrf_token: window._csrf_token || ''}}, swap: 'none'}});"}
                        el.value = '';
                        autoResize();
                        syncSendButtonState();
                        scheduleScrollToLatest();
                    }};

                    if (!el.dataset.chatReady) {{
                        el.dataset.chatReady = 'true';
                        el.addEventListener('input', () => {{
                            autoResize();
                            syncSendButtonState();
                        }});
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

                    const mutationTouchesChat = (mutation) => {{
                        const targetNode = mutation.target instanceof Element ? mutation.target : mutation.target?.parentElement;
                        if (targetNode && targetNode.closest && targetNode.closest('[data-chat-thread="true"]')) {{
                            return true;
                        }}
                        for (const node of mutation.addedNodes || []) {{
                            if (node instanceof Element && (node.matches('[data-chat-thread="true"], [data-chat-message="true"]') || node.querySelector('[data-chat-thread="true"], [data-chat-message="true"]'))) {{
                                return true;
                            }}
                        }}
                        for (const node of mutation.removedNodes || []) {{
                            if (node instanceof Element && (node.matches('[data-chat-thread="true"], [data-chat-message="true"]') || node.querySelector('[data-chat-thread="true"], [data-chat-message="true"]'))) {{
                                return true;
                            }}
                        }}
                        return false;
                    }};

                    window.__violitChatObserver_{cid} = new MutationObserver((mutationList) => {{
                        if (scrollMode !== 'bottom') return;
                        for (const mutation of mutationList) {{
                            if ((mutation.type === 'childList' || mutation.type === 'characterData') && mutationTouchesChat(mutation)) {{
                                scheduleScrollToLatest();
                                break;
                            }}
                        }}
                    }});

                    window.__violitChatObserver_{cid}.observe(chatScope || document.body, {{
                        childList: true,
                        subtree: true,
                        characterData: true,
                    }});

                    autoResize();
                    syncSendButtonState();

                    setTimeout(scheduleScrollToLatest, 100);
                    setTimeout(scheduleScrollToLatest, 320);

                    if (window.lastActiveChatInput === 'input_{cid}') {{
                        setTimeout(() => {{
                            const viewport = {{ x: window.scrollX, y: window.scrollY }};
                            focusInput();
                            preserveViewport(viewport);
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
