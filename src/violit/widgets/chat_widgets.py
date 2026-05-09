import base64
import html as html_lib
import asyncio
import json
import re
import time
from typing import Optional, Union, Callable, Any, Sequence, cast
from ..background import CancelledError
from ..component import Component
from ..context import fragment_ctx, session_ctx, view_ctx, layout_ctx
from ..state import get_session_store
from ..style_utils import merge_cls, merge_style
from .input_widgets import UploadedFile


def _reset_dynamic_chat_children(message_id: str):
    if session_ctx.get() is None:
        return

    store = get_session_store()
    store['fragment_components'][message_id] = []


def _sanitize_chat_key(value: Any) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", str(value)).strip("_") or "chat"


def _clone_chat_item(item: Any):
    if not isinstance(item, dict):
        return item

    cloned = dict(item)
    for field in ("chunks", "trace", "artifacts"):
        value = cloned.get(field)
        if isinstance(value, list):
            cloned[field] = [dict(entry) if isinstance(entry, dict) else entry for entry in value]
    return cloned


def _clone_chat_items(messages_state):
    return [_clone_chat_item(item) for item in messages_state.value]


def _build_chat_uploaded_file(payload: Any) -> Optional[UploadedFile]:
    if isinstance(payload, UploadedFile):
        return payload
    if not isinstance(payload, dict):
        return None

    content = payload.get("content")
    if not content:
        return None

    uploaded = UploadedFile(
        payload.get("name") or "attachment",
        payload.get("type") or "application/octet-stream",
        int(payload.get("size") or 0),
        content,
    )
    relative_path = _coerce_chat_text(payload.get("relative_path")).strip()
    if relative_path:
        setattr(uploaded, "relative_path", relative_path)
    sample_rate = payload.get("sample_rate") or payload.get("audio_sample_rate")
    if sample_rate is not None:
        try:
            setattr(uploaded, "sample_rate", int(sample_rate))
        except Exception:
            pass
    return uploaded


def _parse_chat_submit_value(value: Any) -> Any:
    data = value
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("{") or stripped.startswith('"'):
            try:
                data = json.loads(stripped)
            except Exception:
                return stripped
        else:
            return stripped

        if isinstance(data, str):
            return data.strip()

    if not isinstance(data, dict):
        return data

    files: list[UploadedFile] = []
    raw_files = data.get("files")
    if isinstance(raw_files, list):
        for entry in raw_files:
            uploaded = _build_chat_uploaded_file(entry)
            if uploaded is not None:
                files.append(uploaded)
    elif isinstance(raw_files, dict):
        uploaded = _build_chat_uploaded_file(raw_files)
        if uploaded is not None:
            files.append(uploaded)

    audio_file = _build_chat_uploaded_file(data.get("audio"))
    payload: dict[str, Any] = {
        "text": _coerce_chat_text(data.get("text") if "text" in data else data.get("value")).strip(),
        "files": files,
        "audio": audio_file,
    }
    if data.get("audio_sample_rate") is not None:
        raw_audio_sample_rate = data.get("audio_sample_rate")
        try:
            payload["audio_sample_rate"] = int(cast(Any, raw_audio_sample_rate))
        except Exception:
            payload["audio_sample_rate"] = raw_audio_sample_rate
    return payload


def _chat_submit_has_value(value: Any) -> bool:
    if isinstance(value, dict):
        return bool(
            _coerce_chat_text(value.get("text")).strip()
            or list(value.get("files") or [])
            or value.get("audio")
        )
    if isinstance(value, str):
        return bool(value.strip())
    return bool(value)


def _chat_submit_display_text(value: Any) -> str:
    if isinstance(value, dict):
        parts: list[str] = []
        text = _coerce_chat_text(value.get("text")).strip()
        if text:
            parts.append(text)

        files = [entry for entry in list(value.get("files") or []) if isinstance(entry, UploadedFile)]
        if files:
            names = ", ".join(file.name or "attachment" for file in files[:3])
            extra = f" (+{len(files) - 3} more)" if len(files) > 3 else ""
            parts.append(f"Attachments: {names}{extra}")

        audio_file = value.get("audio")
        if isinstance(audio_file, UploadedFile):
            parts.append(f"Audio: {audio_file.name or 'voice-note'}")

        return "\n\n".join(part for part in parts if part).strip()

    return _coerce_chat_text(value).strip()


def _guess_chat_attachment_mime_type(file_name: str) -> str:
    suffix = file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""
    return {
        "gif": "image/gif",
        "jpeg": "image/jpeg",
        "jpg": "image/jpeg",
        "png": "image/png",
        "svg": "image/svg+xml",
        "webp": "image/webp",
    }.get(suffix, "application/octet-stream")


def _chat_attachment_mime_type(entry: UploadedFile) -> str:
    return _coerce_chat_text(getattr(entry, "type", "")).strip() or _guess_chat_attachment_mime_type(getattr(entry, "name", ""))


def _is_chat_image_attachment(entry: UploadedFile) -> bool:
    return _chat_attachment_mime_type(entry).startswith("image/")


def _chat_attachment_data_url(entry: UploadedFile) -> str:
    file_bytes = entry.getvalue() or b""
    if not file_bytes:
        return ""
    header = _coerce_chat_text(getattr(entry, "header", "")).strip()
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    if header.startswith("data:"):
        return f"{header},{encoded}"
    return f"data:{_chat_attachment_mime_type(entry)};base64,{encoded}"


def _chat_message_files(item: Any) -> list[UploadedFile]:
    if not isinstance(item, dict):
        return []
    return [entry for entry in list(item.get("files") or []) if isinstance(entry, UploadedFile)]


def _chat_message_audio(item: Any) -> Optional[UploadedFile]:
    if not isinstance(item, dict):
        return None
    audio_file = item.get("audio")
    return audio_file if isinstance(audio_file, UploadedFile) else None


def _chat_message_has_attachments(item: Any) -> bool:
    return bool(_chat_message_files(item) or _chat_message_audio(item))


def _chat_history_display_text(item: Any) -> str:
    if not isinstance(item, dict):
        return _coerce_chat_text(item)
    if _chat_message_has_attachments(item):
        text = _coerce_chat_text(item.get("text")).strip()
        if text:
            return text
    return _coerce_chat_text(item.get("content"))


def _normalize_chat_content_format(value: Any) -> str:
    normalized = _coerce_chat_text(value).strip().lower()
    return "text" if normalized == "text" else "markdown"


def _resolve_chat_content_format(item: Any, content_format: Optional[str] = None) -> str:
    if content_format is not None:
        return _normalize_chat_content_format(content_format)
    if isinstance(item, dict):
        return _normalize_chat_content_format(item.get("content_format"))
    return "markdown"


def _render_chat_attachment_html(item: Any) -> str:
    files = _chat_message_files(item)
    audio_file = _chat_message_audio(item)
    if not files and audio_file is None:
        return ""

    image_files = [entry for entry in files if _is_chat_image_attachment(entry)]
    other_files = [entry for entry in files if not _is_chat_image_attachment(entry)]
    sections: list[str] = []

    if image_files:
        image_cards: list[str] = []
        for entry in image_files[:4]:
            data_url = _chat_attachment_data_url(entry)
            if not data_url:
                continue
            safe_name = html_lib.escape(_coerce_chat_text(entry.name) or "image")
            image_cards.append(
                f'''<figure data-chat-part="attachment-image" style="margin:0;display:flex;flex-direction:column;gap:0.35rem;min-width:0;flex:0 1 220px;">
<img src="{html_lib.escape(data_url, quote=True)}" alt="{html_lib.escape(safe_name, quote=True)}" style="display:block;width:100%;max-width:220px;max-height:180px;object-fit:cover;border-radius:16px;border:1px solid color-mix(in srgb, var(--vl-border) 72%, transparent);box-shadow:0 10px 24px color-mix(in srgb, var(--vl-border) 10%, transparent);background:var(--vl-bg-card);" />
<figcaption style="font-size:0.74rem;color:var(--vl-text-muted);line-height:1.3;word-break:break-word;">{safe_name}</figcaption>
</figure>'''
            )
        if image_cards:
            sections.append(
                "<div data-chat-part=\"attachment-images\" style=\"display:flex;flex-wrap:wrap;gap:0.75rem;margin-top:0.8rem;\">"
                + "".join(image_cards)
                + "</div>"
            )

    badges: list[str] = []
    for entry in other_files[:6]:
        safe_name = html_lib.escape(_coerce_chat_text(entry.name) or "attachment")
        badges.append(
            f'''<span data-chat-part="attachment-badge" style="display:inline-flex;align-items:center;gap:0.5rem;padding:0.42rem 0.72rem;border-radius:999px;background:color-mix(in srgb, var(--vl-bg-card) 88%, white 12%);border:1px solid color-mix(in srgb, var(--vl-border) 78%, transparent);font-size:0.78rem;color:var(--vl-text);max-width:100%;">
<span style="display:inline-flex;align-items:center;justify-content:center;padding:0.18rem 0.38rem;border-radius:999px;background:color-mix(in srgb, var(--vl-text-muted) 14%, transparent);font-size:0.62rem;font-weight:700;letter-spacing:0.04em;">FILE</span>
<span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{safe_name}</span>
</span>'''
        )
    if audio_file is not None:
        safe_audio_name = html_lib.escape(_coerce_chat_text(audio_file.name) or "voice-note")
        badges.append(
            f'''<span data-chat-part="attachment-badge" style="display:inline-flex;align-items:center;gap:0.5rem;padding:0.42rem 0.72rem;border-radius:999px;background:color-mix(in srgb, var(--vl-bg-card) 88%, white 12%);border:1px solid color-mix(in srgb, var(--vl-border) 78%, transparent);font-size:0.78rem;color:var(--vl-text);max-width:100%;">
<span style="display:inline-flex;align-items:center;justify-content:center;padding:0.18rem 0.38rem;border-radius:999px;background:color-mix(in srgb, var(--vl-primary) 12%, transparent);font-size:0.62rem;font-weight:700;letter-spacing:0.04em;">AUDIO</span>
<span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{safe_audio_name}</span>
</span>'''
        )
    if badges:
        sections.append(
            "<div data-chat-part=\"attachment-badges\" style=\"display:flex;flex-wrap:wrap;gap:0.55rem;margin-top:0.8rem;\">"
            + "".join(badges)
            + "</div>"
        )

    return "".join(sections)


def _resolve_chat_file_accept_mode(accept_file: Union[bool, str]) -> tuple[bool, bool, bool]:
    if accept_file is True:
        return True, False, False
    if isinstance(accept_file, str):
        normalized = accept_file.strip().lower()
        if normalized in {"", "false", "off", "none"}:
            return False, False, False
        if normalized == "multiple":
            return True, True, False
        if normalized == "directory":
            return True, True, True
        return True, False, False
    return False, False, False


def _resolve_chat_file_accept_attr(file_type: Optional[Union[str, Sequence[str]]]) -> str:
    if file_type is None:
        return "*"

    if isinstance(file_type, str):
        tokens = [token.strip() for token in file_type.split(",") if token.strip()]
    else:
        tokens = [str(token).strip() for token in file_type if str(token).strip()]

    normalized: list[str] = []
    for token in tokens:
        if token == "*" or "/" in token or token.startswith("."):
            normalized.append(token)
        else:
            normalized.append(f".{token.lstrip('.')}")
    return ",".join(normalized) or "*"


def _patch_last_chat_item(messages_state, **updates):
    items = _clone_chat_items(messages_state)
    if not items:
        return
    items[-1] = {**items[-1], **updates}
    messages_state.set(items)


def _chat_submit_inflight_key(cid: str) -> str:
    return f"_violit_chat_submit_inflight:{cid}"


def _chat_submit_queue_key(cid: str) -> str:
    return f"_violit_chat_submit_queue:{cid}"


def _chat_submit_task_key(cid: str) -> str:
    return f"_violit_chat_submit_task:{cid}"


def _is_chat_submit_inflight(store, cid: str) -> bool:
    return bool(store.get(_chat_submit_inflight_key(cid)))


def _set_chat_submit_inflight(store, cid: str, active: bool):
    key = _chat_submit_inflight_key(cid)
    if active:
        store[key] = True
        return
    store.pop(key, None)


def _enqueue_chat_submit(store, cid: str, value: Any):
    key = _chat_submit_queue_key(cid)
    queued = list(store.get(key) or [])
    queued.append(value)
    store[key] = queued


def _dequeue_chat_submit(store, cid: str):
    key = _chat_submit_queue_key(cid)
    queued = list(store.get(key) or [])
    if not queued:
        store.pop(key, None)
        return None
    next_value = queued.pop(0)
    if queued:
        store[key] = queued
    else:
        store.pop(key, None)
    return next_value


def _get_chat_submit_task(store, cid: str):
    return store.get(_chat_submit_task_key(cid))


def _set_chat_submit_task(store, cid: str, task):
    key = _chat_submit_task_key(cid)
    if task is None:
        store.pop(key, None)
        return
    store[key] = task


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
            try:
                running_loop = asyncio.get_running_loop()
            except RuntimeError:
                running_loop = None

            if running_loop is main_loop:
                main_loop.create_task(app.ws_engine.push_updates(sid, dirty, view_id=current_view_id))
                return

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


_AGENT_EVENT_TYPES = {
    "artifact",
    "artifacts",
    "done",
    "error",
    "observation",
    "phase",
    "status",
    "step",
    "summary",
    "text",
    "tool_call",
}


def _coerce_chat_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _html_attr(name: str, value: Any) -> str:
    text = _coerce_chat_text(value).strip()
    if not text:
        return ""
    return f' {name}="{html_lib.escape(text, quote=True)}"'


def _theme_tone(accent: str, *, bg_weight: int = 14, border_weight: int = 22) -> tuple[str, str]:
    safe_bg_weight = max(0, min(100, int(bg_weight)))
    safe_border_weight = max(0, min(100, int(border_weight)))
    bg = f"color-mix(in srgb, {accent} {safe_bg_weight}%, var(--vl-bg-card) {100 - safe_bg_weight}%)"
    border = f"color-mix(in srgb, {accent} {safe_border_weight}%, var(--vl-border) {100 - safe_border_weight}%)"
    return bg, border


def _phase_accent_color(phase: str) -> str:
    normalized_phase = (phase or "").strip().lower()
    return {
        "thinking": "var(--vl-primary)",
        "running": "color-mix(in srgb, var(--vl-primary) 38%, var(--vl-text) 62%)",
        "done": "var(--vl-success)",
        "error": "var(--vl-danger)",
    }.get(normalized_phase, "var(--vl-text-muted)")


def _trace_kind_accent_color(kind: str) -> str:
    normalized_kind = (kind or "").strip().lower()
    return {
        "status": "var(--vl-primary)",
        "tool_call": "var(--vl-success)",
        "observation": "var(--vl-warning)",
        "step": "color-mix(in srgb, var(--vl-primary) 18%, var(--vl-text) 82%)",
    }.get(normalized_kind, "var(--vl-text-muted)")


def _normalize_chat_phase(item: Any) -> str:
    if not isinstance(item, dict):
        return ""

    phase = _coerce_chat_text(item.get("phase")).strip().lower()
    if phase:
        return phase

    status = _coerce_chat_text(item.get("status")).strip().lower()
    if status == "streaming":
        return "running"
    return status


def _is_agent_event(value: Any) -> bool:
    if not isinstance(value, dict):
        return False

    event_type = _coerce_chat_text(value.get("type") or value.get("event")).strip().lower()
    if event_type in _AGENT_EVENT_TYPES:
        return True

    return any(
        key in value
        for key in ("phase", "trace", "artifacts", "summary", "status_text", "thinking_label")
    )


def _normalize_trace_step(step: Any):
    if isinstance(step, dict):
        kind = _coerce_chat_text(step.get("kind") or step.get("type") or "step").strip().lower() or "step"
        title = _coerce_chat_text(step.get("title") or step.get("label"))
        text = _coerce_chat_text(step.get("text") or step.get("content") or step.get("message"))
        status = _coerce_chat_text(step.get("status"))
        normalized = dict(step)
        normalized["kind"] = kind
        if title:
            normalized["title"] = title
        if text:
            normalized["text"] = text
        if status:
            normalized["status"] = status
        return normalized

    text = _coerce_chat_text(step).strip()
    if not text:
        return None
    return {"kind": "step", "text": text}


def _render_agent_status_html(status_text: str, phase: str) -> str:
    text = _coerce_chat_text(status_text).strip()
    if not text:
        return ""

    safe_text = html_lib.escape(text).replace("\n", "<br>")
    normalized_phase = (phase or "running").strip().lower() or "running"
    badge_label = {
        "thinking": "Thinking",
        "running": "Running",
        "done": "Done",
        "error": "Error",
    }.get(normalized_phase, normalized_phase.title() or "Status")
    badge_color = _phase_accent_color(normalized_phase)
    badge_bg, card_border = _theme_tone(badge_color, bg_weight=14, border_weight=22)
    spinner_html = ""
    if normalized_phase in {"thinking", "running"}:
        spinner_html = '<wa-spinner style="font-size:0.78rem; --indicator-color: currentColor;"></wa-spinner>'

    return f'''
    <div class="vl-agent-status vl-chat-meta-card vl-chat-meta-card--status vl-chat-meta-card--{normalized_phase}" data-chat-part="agent-status" data-agent-phase="{html_lib.escape(normalized_phase, quote=True)}" style="display:flex;align-items:flex-start;gap:0.75rem;margin-bottom:0.8rem;padding:0.75rem 0.85rem;border-radius:14px;background:color-mix(in srgb, var(--vl-bg-card) 88%, var(--vl-bg) 12%);border:1px solid {card_border};box-shadow:0 10px 24px color-mix(in srgb, var(--vl-border) 12%, transparent);">
        <div class="vl-agent-status__icon" data-chat-part="agent-status-icon" style="flex-shrink:0;display:flex;align-items:center;justify-content:center;color:{badge_color};min-height:1.1rem;">{spinner_html}</div>
        <div class="vl-agent-status__body" data-chat-part="agent-status-body" style="min-width:0;flex:1;">
            <div class="vl-agent-status__badge" data-chat-part="agent-status-badge" style="display:inline-flex;align-items:center;gap:0.35rem;padding:0.18rem 0.48rem;border-radius:999px;background:{badge_bg};color:{badge_color};font-size:0.72rem;font-weight:700;letter-spacing:0.02em;text-transform:uppercase;">{html_lib.escape(badge_label)}</div>
            <div class="vl-agent-status__text" data-chat-part="agent-status-text" style="margin-top:0.42rem;color:var(--vl-text);font-size:0.94rem;line-height:1.5;">{safe_text}</div>
        </div>
    </div>
    '''


def _render_agent_summary_html(summary: str) -> str:
    text = _coerce_chat_text(summary).strip()
    if not text:
        return ""

    safe_text = html_lib.escape(text).replace("\n", "<br>")
    return f'''
    <div class="vl-agent-summary vl-chat-meta-card vl-chat-meta-card--summary" data-chat-part="agent-summary" style="margin-bottom:0.85rem;padding:0.8rem 0.9rem;border-radius:14px;background:linear-gradient(180deg, color-mix(in srgb, var(--vl-bg-card) 94%, white 6%), color-mix(in srgb, var(--vl-bg-card) 86%, var(--vl-bg) 14%));border:1px solid color-mix(in srgb, var(--vl-border) 88%, var(--vl-primary) 12%);box-shadow:0 10px 24px color-mix(in srgb, var(--vl-border) 10%, transparent);">
        <div class="vl-agent-summary__label" data-chat-part="agent-summary-label" style="font-size:0.72rem;font-weight:700;letter-spacing:0.04em;text-transform:uppercase;color:var(--vl-text-muted, #64748b);margin-bottom:0.35rem;">Summary</div>
        <div class="vl-agent-summary__text" data-chat-part="agent-summary-text" style="color:var(--vl-text);font-size:0.95rem;line-height:1.55;">{safe_text}</div>
    </div>
    '''


def _render_agent_error_html(error_text: str) -> str:
    text = _coerce_chat_text(error_text).strip()
    if not text:
        return ""

    safe_text = html_lib.escape(text).replace("\n", "<br>")
    error_bg, error_border = _theme_tone("var(--vl-danger)", bg_weight=14, border_weight=28)
    return f'''
    <div class="vl-agent-error vl-chat-meta-card vl-chat-meta-card--error" data-chat-part="agent-error" style="margin-bottom:0.85rem;padding:0.8rem 0.9rem;border-radius:14px;background:{error_bg};border:1px solid {error_border};color:color-mix(in srgb, var(--vl-danger) 82%, var(--vl-text) 18%);box-shadow:0 10px 24px color-mix(in srgb, var(--vl-danger) 10%, transparent);">
        <div class="vl-agent-error__label" data-chat-part="agent-error-label" style="font-size:0.72rem;font-weight:700;letter-spacing:0.04em;text-transform:uppercase;margin-bottom:0.35rem;">Error</div>
        <div class="vl-agent-error__text" data-chat-part="agent-error-text" style="font-size:0.94rem;line-height:1.55;">{safe_text}</div>
    </div>
    '''


def _render_agent_trace_html(trace: Any, collapsed: bool = True) -> str:
    if not trace:
        return ""

    items = trace if isinstance(trace, list) else [trace]
    rows = []
    for raw_step in items:
        step = _normalize_trace_step(raw_step)
        if not step:
            continue

        kind = _coerce_chat_text(step.get("kind") or "step").strip().lower() or "step"
        title = _coerce_chat_text(step.get("title")).strip()
        text = _coerce_chat_text(step.get("text") or step.get("content") or step.get("message")).strip()
        status = _coerce_chat_text(step.get("status")).strip()
        badge_color = _trace_kind_accent_color(kind)
        badge_bg, row_border = _theme_tone(badge_color, bg_weight=14, border_weight=20)
        safe_title = html_lib.escape(title)
        safe_text = html_lib.escape(text).replace("\n", "<br>")
        safe_status = html_lib.escape(status)
        body_html = ""
        if safe_title or safe_text:
            body_html = f'<div class="vl-agent-trace__body" data-chat-part="agent-trace-body" style="margin-top:0.34rem;color:var(--vl-text);font-size:0.93rem;line-height:1.5;">'
            if safe_title:
                body_html += f'<strong class="vl-agent-trace__title" data-chat-part="agent-trace-title" style="font-weight:650;">{safe_title}</strong>'
                if safe_text:
                    body_html += '<span style="opacity:0.66;">: </span>'
            if safe_text:
                body_html += safe_text
            body_html += '</div>'
        status_html = f'<div class="vl-agent-trace__status" data-chat-part="agent-trace-status" style="margin-top:0.28rem;font-size:0.8rem;color:var(--vl-text-muted, #64748b);">{safe_status}</div>' if safe_status else ''
        rows.append(
            f'''
            <div class="vl-agent-trace__row vl-agent-trace__row--{html_lib.escape(kind, quote=True)}" data-chat-part="agent-trace-row" data-trace-kind="{html_lib.escape(kind, quote=True)}" style="padding:0.72rem 0.15rem;{'' if not rows else f'border-top:1px solid {row_border};'}">
                <div class="vl-agent-trace__header" data-chat-part="agent-trace-header" style="display:flex;align-items:center;gap:0.45rem;flex-wrap:wrap;">
                    <span class="vl-agent-trace__badge" data-chat-part="agent-trace-badge" style="display:inline-flex;align-items:center;padding:0.18rem 0.48rem;border-radius:999px;background:{badge_bg};color:{badge_color};font-size:0.72rem;font-weight:700;letter-spacing:0.02em;text-transform:uppercase;">{html_lib.escape(kind.replace('_', ' '))}</span>
                </div>
                {body_html}
                {status_html}
            </div>
            '''
        )

    if not rows:
        return ""

    open_attr = "" if collapsed else "open"
    return f'''
    <wa-details class="vl-agent-trace" data-chat-part="agent-trace" {open_attr} style="margin-bottom:0.85rem;border-radius:14px;--summary-icon-color: var(--vl-text-muted);">
        <span slot="summary" class="vl-agent-trace__summary" data-chat-part="agent-trace-summary" style="font-weight:650;color:var(--vl-text);">Trace <span class="vl-agent-trace__count" data-chat-part="agent-trace-count" style="margin-left:0.35rem;color:var(--vl-text-muted, #64748b);font-size:0.84rem;">{len(rows)} steps</span></span>
        <div class="vl-agent-trace__content" data-chat-part="agent-trace-content" style="padding:0.2rem 0.1rem 0.1rem;">
            {''.join(rows)}
        </div>
    </wa-details>
    '''


def _render_agent_artifacts_html(artifacts: Any, collapsed: bool = True) -> str:
    if not artifacts:
        return ""

    items = artifacts if isinstance(artifacts, list) else [artifacts]
    cards = []
    for raw_artifact in items:
        if isinstance(raw_artifact, dict):
            kind = _coerce_chat_text(raw_artifact.get("kind") or raw_artifact.get("type") or "artifact").strip() or "artifact"
            title = _coerce_chat_text(raw_artifact.get("title") or raw_artifact.get("label") or raw_artifact.get("name") or kind).strip() or "artifact"
            text = _coerce_chat_text(raw_artifact.get("text") or raw_artifact.get("content") or raw_artifact.get("summary")).strip()
            url = _coerce_chat_text(raw_artifact.get("url") or raw_artifact.get("href")).strip()
            safe_title = html_lib.escape(title)
            safe_text = html_lib.escape(text).replace("\n", "<br>") if text else ""
            link_html = ""
            if url:
                safe_url = html_lib.escape(url, quote=True)
                link_html = f'<div class="vl-agent-artifact__link-wrap" data-chat-part="agent-artifact-link-wrap" style="margin-top:0.45rem;"><a class="vl-agent-artifact__link" data-chat-part="agent-artifact-link" href="{safe_url}" target="_blank" rel="noopener noreferrer" style="color:var(--vl-primary);text-decoration:none;font-weight:600;">Open artifact</a></div>'
            cards.append(
                f'''
                <div class="vl-agent-artifact vl-agent-artifact--card" data-chat-part="agent-artifact" style="padding:0.72rem 0.82rem;border-radius:12px;background:color-mix(in srgb, var(--vl-bg-card) 90%, var(--vl-bg) 10%);border:1px solid color-mix(in srgb, var(--vl-border) 88%, var(--vl-primary) 12%);box-shadow:0 10px 24px color-mix(in srgb, var(--vl-border) 10%, transparent);">
                    <div class="vl-agent-artifact__kind" data-chat-part="agent-artifact-kind" style="font-size:0.78rem;font-weight:700;letter-spacing:0.03em;text-transform:uppercase;color:var(--vl-text-muted, #64748b);margin-bottom:0.28rem;">{html_lib.escape(kind)}</div>
                    <div class="vl-agent-artifact__title" data-chat-part="agent-artifact-title" style="font-weight:650;color:var(--vl-text);">{safe_title}</div>
                    {f'<div class="vl-agent-artifact__text" data-chat-part="agent-artifact-text" style="margin-top:0.35rem;color:var(--vl-text);font-size:0.92rem;line-height:1.5;">{safe_text}</div>' if safe_text else ''}
                    {link_html}
                </div>
                '''
            )
            continue

        text = _coerce_chat_text(raw_artifact).strip()
        if text:
            safe_plain_text = html_lib.escape(text).replace("\n", "<br>")
            cards.append(
                f'<div class="vl-agent-artifact vl-agent-artifact--plain" data-chat-part="agent-artifact" style="padding:0.72rem 0.82rem;border-radius:12px;background:color-mix(in srgb, var(--vl-bg-card) 90%, var(--vl-bg) 10%);border:1px solid color-mix(in srgb, var(--vl-border) 88%, var(--vl-primary) 12%);color:var(--vl-text);font-size:0.92rem;line-height:1.5;">{safe_plain_text}</div>'
            )

    if not cards:
        return ""

    open_attr = "" if collapsed else "open"
    return f'''
    <wa-details class="vl-agent-artifacts" data-chat-part="agent-artifacts" {open_attr} style="margin-top:0.9rem;border-radius:14px;--summary-icon-color: var(--vl-text-muted);">
        <span slot="summary" class="vl-agent-artifacts__summary" data-chat-part="agent-artifacts-summary" style="font-weight:650;color:var(--vl-text);">Artifacts <span class="vl-agent-artifacts__count" data-chat-part="agent-artifacts-count" style="margin-left:0.35rem;color:var(--vl-text-muted, #64748b);font-size:0.84rem;">{len(cards)}</span></span>
        <div class="vl-agent-artifacts__content" data-chat-part="agent-artifacts-content" style="display:grid;gap:0.65rem;padding:0.2rem 0.1rem 0.1rem;">
            {''.join(cards)}
        </div>
    </wa-details>
    '''


def _chat_item_has_visible_content(item: Any) -> bool:
    if not isinstance(item, dict):
        return bool(_coerce_chat_text(item).strip())

    content = _coerce_chat_text(item.get("content")).strip()
    if content:
        return True
    if any(item.get(field) for field in ("summary", "trace", "artifacts", "status_text", "error")):
        return True
    chunks = item.get("chunks")
    if isinstance(chunks, list) and any(_coerce_chat_text(chunk).strip() for chunk in chunks):
        return True
    return False


def _apply_agent_event(item: Any, event: dict[str, Any], *, cursor: Optional[str] = None):
    next_item: dict[str, Any] = _clone_chat_item(item)
    if not isinstance(next_item, dict):
        next_item = {"role": "assistant", "content": _coerce_chat_text(next_item)}

    event_type = _coerce_chat_text(event.get("type") or event.get("event")).strip().lower()
    text_value = _coerce_chat_text(
        event.get("text")
        or event.get("content")
        or event.get("message")
        or event.get("status")
    )

    if event_type == "status":
        if text_value:
            next_item["status_text"] = text_value
            next_item["thinking_label"] = text_value
        next_item["phase"] = "running" if _chat_item_has_visible_content(next_item) else "thinking"
        next_item["status"] = "thinking"
        return next_item

    if event_type in {"step", "tool_call", "observation"}:
        step = _normalize_trace_step(event)
        if step:
            trace: list[Any] = list(next_item.get("trace") or [])
            trace.append(step)
            next_item["trace"] = trace
            step_label = _coerce_chat_text(step.get("title") or step.get("text")).strip()
            if step_label:
                next_item["status_text"] = step_label
                next_item["thinking_label"] = step_label
        next_item["phase"] = "running"
        next_item["status"] = "streaming"
        return next_item

    if event_type == "summary":
        if text_value:
            next_item["summary"] = text_value
        next_item["phase"] = "running"
        next_item["status"] = "streaming"
        return next_item

    if event_type == "text":
        if text_value:
            chunks: list[str] = list(next_item.get("chunks") or [])
            chunks.append(text_value)
            next_item["chunks"] = chunks
            next_item["content"] = "".join(_coerce_chat_text(chunk) for chunk in chunks)
            next_item["cursor"] = cursor
        next_item["phase"] = "running"
        next_item["status"] = "streaming"
        return next_item

    if event_type in {"artifact", "artifacts"}:
        payload = event.get("items") if event_type == "artifacts" else event.get("artifact")
        if payload is None:
            payload = event.get("artifacts") if event_type == "artifacts" else dict(event)
        artifacts: list[Any] = list(next_item.get("artifacts") or [])
        if isinstance(payload, list):
            artifacts.extend(payload)
        elif payload is not None:
            artifacts.append(payload)
        next_item["artifacts"] = artifacts
        next_item["phase"] = "running"
        next_item["status"] = "streaming"
        return next_item

    if event_type == "error":
        if text_value:
            next_item["error"] = text_value
            next_item["status_text"] = text_value
            next_item["thinking_label"] = text_value
        next_item["cursor"] = None
        next_item["phase"] = "error"
        next_item["status"] = "error"
        return next_item

    if event_type == "done":
        next_item["cursor"] = None
        next_item["phase"] = "done"
        next_item["status"] = "done"
        next_item["status_text"] = ""
        return next_item

    if event_type == "phase":
        phase = _coerce_chat_text(event.get("phase") or text_value).strip().lower()
        if phase:
            next_item["phase"] = phase
            next_item["status"] = "error" if phase == "error" else ("done" if phase == "done" else next_item.get("status", "streaming"))
        return next_item

    for field in ("phase", "summary", "status_text", "thinking_label", "error"):
        if field in event and event[field] is not None:
            next_item[field] = event[field]
    for field in ("trace", "artifacts"):
        if field in event and event[field] is not None:
            next_item[field] = event[field] if isinstance(event[field], list) else [event[field]]
    if "content" in event and isinstance(event.get("content"), str):
        next_item["content"] = event["content"]
    if "chunks" in event and isinstance(event.get("chunks"), list):
        next_item["chunks"] = list(event["chunks"])
    if "status" in event and event["status"] is not None:
        next_item["status"] = event["status"]
    return next_item


def _patch_last_chat_item_with_event(messages_state, event: dict[str, Any], *, cursor: Optional[str] = None):
    items = _clone_chat_items(messages_state)
    if not items:
        return None
    items[-1] = _apply_agent_event(items[-1], event, cursor=cursor)
    messages_state.set(items)
    return items[-1]

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

    def chat_message(
        self,
        name: str,
        avatar: Optional[str] = None,
        *,
        width: Union[str, int] = "stretch",
        thinking: bool = False,
        thinking_label: str = "Thinking...",
        phase: Optional[str] = None,
        status: str = "",
        cls: str = "",
        style: str = "",
        key: Optional[str] = None,
    ):
        """
        Insert a primitive chat message container.

        Use ``thinking=True`` and ``thinking_label=...`` for a lightweight
        assistant placeholder. Use ``phase=...`` and ``status=...`` when you
        want the primitive bubble to expose a small built-in status treatment
        without switching to ``agent_turn(...)``.
        """

        return self._chat_message_impl(
            name,
            avatar,
            width=width,
            thinking=thinking,
            thinking_label=thinking_label,
            phase=phase,
            status_text=status,
            cls=cls,
            style=style,
            key=key,
        )

    def agent_turn(
        self,
        name: str,
        avatar: Optional[str] = None,
        *,
        width: Union[str, int] = "stretch",
        cls: str = "",
        style: str = "",
        thinking: bool = False,
        thinking_label: str = "Thinking...",
        phase: Optional[str] = None,
        status_text: str = "",
        summary: str = "",
        trace: Optional[list[Any]] = None,
        artifacts: Optional[list[Any]] = None,
        error_text: str = "",
        trace_collapsed: bool = True,
        artifacts_collapsed: bool = True,
        key: Optional[str] = None,
    ):
        """
        Insert one advanced single-turn renderer with agent-oriented metadata.

        Use this when a single message may need status, thinking state,
        summary, trace, artifacts, or error rendering inside the bubble.
        For whole histories, prefer ``chat_history(...)`` or
        ``agent_history(...)``.
        """
        return self._chat_message_impl(
            name,
            avatar,
            width=width,
            cls=cls,
            style=style,
            thinking=thinking,
            thinking_label=thinking_label,
            phase=phase,
            status_text=status_text,
            summary=summary,
            trace=trace,
            artifacts=artifacts,
            error_text=error_text,
            trace_collapsed=trace_collapsed,
            artifacts_collapsed=artifacts_collapsed,
            key=key,
        )

    def _chat_message_impl(
        self,
        name: str,
        avatar: Optional[str] = None,
        *,
        width: Union[str, int] = "stretch",
        cls: str = "",
        style: str = "",
        thinking: bool = False,
        thinking_label: str = "Thinking...",
        phase: Optional[str] = None,
        status_text: str = "",
        summary: str = "",
        trace: Optional[list[Any]] = None,
        artifacts: Optional[list[Any]] = None,
        error_text: str = "",
        trace_collapsed: bool = True,
        artifacts_collapsed: bool = True,
        key: Optional[str] = None,
    ):
        cid = f"chat_message_{_sanitize_chat_key(key)}" if key is not None else self._get_next_cid("chat_message")
        
        class ChatMessageContext:
            def __init__(self, app, message_id, name, avatar, user_cls="", user_style="", thinking=False, thinking_label="Thinking...", phase=None, status_text="", summary="", trace=None, artifacts=None, error_text="", trace_collapsed=True, artifacts_collapsed=True, key=None):
                self.app = app
                self.message_id = message_id
                self.name = name
                self.avatar = avatar
                self.user_cls = user_cls
                self.user_style = user_style
                self.thinking = thinking
                self.thinking_label = thinking_label
                self.phase = phase
                self.status_text = status_text
                self.summary = summary
                self.trace = list(trace or [])
                self.artifacts = list(artifacts or [])
                self.error_text = error_text
                self.trace_collapsed = trace_collapsed
                self.artifacts_collapsed = artifacts_collapsed
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
                    normalized_phase = _coerce_chat_text(self.phase).strip().lower()
                    user_class_attr = _html_attr("class", merge_cls("vl-chat-message-root", self.user_cls))
                    
                    # Icons handling
                    if self.avatar:
                        if self.avatar.startswith("http") or self.avatar.startswith("data:"):
                            safe_avatar = html_lib.escape(self.avatar, quote=True)
                            avatar_content = f'<img class="vl-chat-avatar-inner vl-chat-avatar-inner--image" data-chat-part="avatar-inner" src="{safe_avatar}" style="width:var(--vl-chat-avatar-size, 42px);height:var(--vl-chat-avatar-size, 42px);border-radius:999px;object-fit:cover;border:1px solid color-mix(in srgb, var(--vl-border) 78%, transparent);box-shadow:var(--vl-chat-avatar-shadow, 0 10px 24px color-mix(in srgb, var(--vl-border) 10%, transparent));">'
                        else:
                            safe_avatar = html_lib.escape(self.avatar)
                            avatar_content = f'<div class="vl-chat-avatar-inner vl-chat-avatar-inner--label" data-chat-part="avatar-inner" style="width:var(--vl-chat-avatar-size, 42px);height:var(--vl-chat-avatar-size, 42px);border-radius:999px;background:linear-gradient(135deg, color-mix(in srgb, var(--vl-bg-card) 76%, var(--vl-bg) 24%) 0%, color-mix(in srgb, var(--vl-border) 76%, var(--vl-bg-card) 24%) 100%);border:1px solid color-mix(in srgb, var(--vl-border) 78%, transparent);display:flex;align-items:center;justify-content:center;font-size:var(--vl-chat-avatar-font-size, 18px);font-weight:700;color:color-mix(in srgb, var(--vl-text) 78%, var(--vl-primary) 22%);box-shadow:var(--vl-chat-avatar-shadow, 0 10px 24px color-mix(in srgb, var(--vl-border) 10%, transparent));">{safe_avatar}</div>'
                    else:
                        if role == "user":
                            avatar_content = '<div class="vl-chat-avatar-inner vl-chat-avatar-inner--user" data-chat-part="avatar-inner" style="width:var(--vl-chat-avatar-size, 42px);height:var(--vl-chat-avatar-size, 42px);border-radius:999px;background:linear-gradient(135deg, var(--vl-primary) 0%, var(--vl-secondary) 100%);color:color-mix(in srgb, white 88%, var(--vl-bg) 12%);display:flex;align-items:center;justify-content:center;box-shadow:var(--vl-chat-avatar-shadow, 0 10px 24px color-mix(in srgb, var(--vl-primary) 18%, transparent));"><wa-icon name="user"></wa-icon></div>'
                        elif role == "assistant":
                            avatar_content = '<div class="vl-chat-avatar-inner vl-chat-avatar-inner--assistant" data-chat-part="avatar-inner" style="width:var(--vl-chat-avatar-size, 42px);height:var(--vl-chat-avatar-size, 42px);border-radius:999px;background:linear-gradient(135deg, color-mix(in srgb, var(--vl-secondary) 72%, var(--vl-primary) 28%) 0%, color-mix(in srgb, var(--vl-text) 24%, var(--vl-secondary) 76%) 100%);color:color-mix(in srgb, white 88%, var(--vl-bg) 12%);display:flex;align-items:center;justify-content:center;box-shadow:var(--vl-chat-avatar-shadow, 0 10px 24px color-mix(in srgb, var(--vl-secondary) 18%, transparent));"><wa-icon name="sparkles"></wa-icon></div>'
                        else:
                            initial = self.name[0].upper() if self.name else "?"
                            avatar_content = f'<div class="vl-chat-avatar-inner vl-chat-avatar-inner--generic" data-chat-part="avatar-inner" style="width:var(--vl-chat-avatar-size, 42px);height:var(--vl-chat-avatar-size, 42px);border-radius:999px;background:linear-gradient(135deg, var(--vl-text-muted) 0%, color-mix(in srgb, var(--vl-text-muted) 62%, var(--vl-secondary) 38%) 100%);color:color-mix(in srgb, white 90%, var(--vl-bg) 10%);display:flex;align-items:center;justify-content:center;font-weight:700;box-shadow:var(--vl-chat-avatar-shadow, 0 10px 24px color-mix(in srgb, var(--vl-text-muted) 16%, transparent));">{html_lib.escape(initial)}</div>'

                    if role == "user":
                        bubble_bg = "linear-gradient(180deg, color-mix(in srgb, var(--vl-primary) 18%, var(--vl-bg-card) 82%) 0%, color-mix(in srgb, var(--vl-primary) 10%, var(--vl-bg-card) 90%) 100%)"
                        bubble_border = "1px solid color-mix(in srgb, var(--vl-primary) 28%, var(--vl-border) 72%)"
                        bubble_shadow = "0 12px 28px color-mix(in srgb, var(--vl-primary) 16%, transparent)"
                        name_color = "var(--vl-primary)"
                    elif normalized_phase == "error":
                        bubble_bg = "linear-gradient(180deg, color-mix(in srgb, var(--vl-danger) 16%, var(--vl-bg-card) 84%) 0%, color-mix(in srgb, var(--vl-danger) 10%, var(--vl-bg-card) 90%) 100%)"
                        bubble_border = "1px solid color-mix(in srgb, var(--vl-danger) 28%, var(--vl-border) 72%)"
                        bubble_shadow = "0 14px 30px color-mix(in srgb, var(--vl-danger) 12%, transparent)"
                    elif self.thinking:
                        bubble_bg = "linear-gradient(180deg, color-mix(in srgb, var(--vl-text-muted) 12%, var(--vl-bg-card) 88%) 0%, color-mix(in srgb, var(--vl-bg) 16%, var(--vl-bg-card) 84%) 100%)"
                        bubble_border = "1px solid color-mix(in srgb, var(--vl-text-muted) 16%, var(--vl-border) 84%)"
                        bubble_shadow = "0 14px 30px color-mix(in srgb, var(--vl-text-muted) 10%, transparent)"

                    before_content_html = "".join(
                        part
                        for part in (
                            _render_agent_status_html(self.status_text, normalized_phase or ("thinking" if self.thinking else "running")),
                            _render_agent_trace_html(self.trace, collapsed=self.trace_collapsed),
                            _render_agent_summary_html(self.summary),
                            _render_agent_error_html(self.error_text),
                        )
                        if part
                    )
                    after_content_html = _render_agent_artifacts_html(self.artifacts, collapsed=self.artifacts_collapsed)

                    if self.thinking and not inner_html and not before_content_html and not after_content_html:
                        label = html_lib.escape(self.thinking_label)
                        inner_html = f'''
                        <div class="vl-chat-thinking" data-chat-part="thinking" style="display:flex;align-items:center;gap:0.8rem;min-height:1.4rem;">
                            <wa-spinner style="font-size:1rem;--indicator-color: var(--vl-accent, #2563eb);"></wa-spinner>
                            <div class="vl-chat-thinking__body" data-chat-part="thinking-body">
                                <div class="vl-chat-thinking__label" data-chat-part="thinking-label" style="font-weight:600;color:var(--vl-text);">{label}</div>
                                <div class="vl-chat-thinking__caption" data-chat-part="thinking-caption" style="font-size:0.88rem;color:var(--vl-text-muted, #64748b);margin-top:0.15rem;">The response is being prepared in the background.</div>
                            </div>
                        </div>
                        '''

                    inner_html = f"{before_content_html}{inner_html}{after_content_html}".strip()

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
                    <div class="chat-message vl-chat-message chat-message--{role} vl-chat-message--{role}{' vl-chat-message--thinking' if self.thinking else ''}{' vl-chat-message--error' if normalized_phase == 'error' else ''}" data-chat-message="true" data-chat-role="{role}" data-chat-phase="{html_lib.escape(normalized_phase or ('thinking' if self.thinking else 'done'), quote=True)}" data-chat-thinking="{'true' if self.thinking else 'false'}" data-chat-part="message"{safe_key_attr}{user_class_attr} style="--vl-chat-author-color-base:{name_color};--vl-chat-bubble-bg-base:{bubble_bg};--vl-chat-bubble-border-base:{bubble_border};--vl-chat-bubble-shadow-base:{bubble_shadow};display:flex; gap:var(--vl-chat-row-gap, 14px); align-items:flex-start; justify-content:{row_justify}; margin-bottom:var(--vl-chat-message-spacing, 18px);">
                        <div class="chat-avatar vl-chat-avatar" data-chat-part="avatar" style="flex-shrink:0; padding-top:2px;">
                           {avatar_content}
                        </div>
                        <div class="chat-content vl-chat-content" data-chat-part="content" style="flex:1; min-width:0; overflow-wrap:break-word; display:flex; flex-direction:column; gap:0.5rem; {width_style}">
                            <div class="chat-author vl-chat-author" data-chat-part="author" style="font-size:var(--vl-chat-author-size, 0.8rem); letter-spacing:var(--vl-chat-author-tracking, 0.03em); text-transform:uppercase; font-weight:700; color:var(--vl-chat-author-color, var(--vl-chat-author-color-base)); padding:0 0.2rem;">{safe_name}</div>
                            <div class="chat-bubble vl-chat-bubble" data-chat-part="bubble" style="background:var(--vl-chat-bubble-bg, var(--vl-chat-bubble-bg-base)); border:var(--vl-chat-bubble-border, var(--vl-chat-bubble-border-base)); box-shadow:var(--vl-chat-bubble-shadow, var(--vl-chat-bubble-shadow-base)); border-radius:var(--vl-chat-bubble-radius, 20px); padding:var(--vl-chat-bubble-py, 16px) var(--vl-chat-bubble-px, 18px); color:var(--vl-text); line-height:1.6; backdrop-filter:saturate(140%) blur(3px);">
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
                
        return ChatMessageContext(self, cid, name, avatar, cls, style, thinking, thinking_label, phase, status_text, summary, trace, artifacts, error_text, trace_collapsed, artifacts_collapsed, key)

    def chat_thread(
        self,
        height: Union[int, str] = "58vh",
        auto_scroll: Union[bool, str] = True,
        scroll_behavior: str = "smooth",
        cls: str = "",
        style: str = "",
        border: bool = False,
        **kwargs,
    ):
        """Create a dedicated chat conversation surface.

        This is the recommended container for rendering chat messages. It provides
        a scrollable thread surface with stable spacing and is designed to work
        with managed_chat_input(auto_scroll=...). Primitive chat surfaces also
        inherit the same auto-scroll behavior here, so `chat_message(...)`
        stacks inside `chat_thread(...)` stay pinned to the latest message by
        default.
        """
        cid = self._get_next_cid("chat_thread")
        scroll_mode = self._resolve_chat_scroll_mode(auto_scroll)
        surface_style = merge_style(
            """
            border-radius: var(--vl-chat-thread-radius, 24px) !important;
            padding: var(--vl-chat-thread-padding, 0.25rem 0.35rem 0.5rem);
            background: linear-gradient(180deg, color-mix(in srgb, var(--vl-bg-card) 90%, var(--vl-bg) 10%), color-mix(in srgb, var(--vl-bg-card) 82%, var(--vl-bg) 18%)) !important;
            border: 1px solid color-mix(in srgb, var(--vl-border) 88%, var(--vl-primary) 12%) !important;
            box-shadow: var(--vl-chat-thread-shadow, inset 0 1px 0 color-mix(in srgb, white 24%, transparent), 0 18px 40px color-mix(in srgb, var(--vl-border) 10%, transparent)) !important;
            """,
            style,
        )
        surface_cls = merge_cls("vl-chat-thread", cls)

        container_ctx = self.container(
            border=border,
            height=height,
            cls=surface_cls,
            style=surface_style,
            data_chat_thread="true",
            data_chat_thread_id=cid,
            data_chat_scroll_mode=scroll_mode,
            data_chat_scroll_behavior=scroll_behavior,
            **kwargs,
        )

        class ChatThreadContext:
            def __init__(self, app, thread_cid, wrapped_ctx, scroll_mode_value, scroll_behavior_value):
                self.app = app
                self.thread_cid = thread_cid
                self.wrapped_ctx = wrapped_ctx
                self.scroll_mode_value = scroll_mode_value
                self.scroll_behavior_value = scroll_behavior_value
                self._entered = None

            def __enter__(self):
                self._entered = self.wrapped_ctx.__enter__()
                self.app.html(
                    f"""
                    <script>
                    (function() {{
                        const thread = document.querySelector('[data-chat-thread-id="{self.thread_cid}"]');
                        if (!thread) return;
                        const scrollMode = {json.dumps(self.scroll_mode_value)};
                        const scrollBehavior = {json.dumps(self.scroll_behavior_value)};
                        const observerKey = '__violitChatThreadObserver_{self.thread_cid}';
                        const frameKey = '__violitChatThreadFrame_{self.thread_cid}';
                        if (window[observerKey]) {{
                            window[observerKey].disconnect();
                        }}
                        const syncBottom = (behavior) => {{
                            const nextTop = Math.max(thread.scrollHeight - thread.clientHeight, 0);
                            thread.scrollTop = nextTop;
                            if (typeof thread.scrollTo === 'function') {{
                                thread.scrollTo({{ top: nextTop, behavior }});
                            }}
                        }};
                        const maybeScrollToLatest = () => {{
                            if (scrollMode !== 'bottom') return;
                            syncBottom('auto');
                            requestAnimationFrame(() => syncBottom(scrollBehavior === 'instant' ? 'auto' : scrollBehavior));
                            setTimeout(() => syncBottom('auto'), 80);
                        }};
                        const scheduleScrollToLatest = () => {{
                            if (scrollMode !== 'bottom') return;
                            if (window[frameKey]) {{
                                cancelAnimationFrame(window[frameKey]);
                            }}
                            window[frameKey] = requestAnimationFrame(() => {{
                                maybeScrollToLatest();
                                requestAnimationFrame(maybeScrollToLatest);
                            }});
                        }};
                        window[observerKey] = new MutationObserver((mutations) => {{
                            for (const mutation of mutations) {{
                                if (mutation.type === 'childList' || mutation.type === 'characterData') {{
                                    scheduleScrollToLatest();
                                    break;
                                }}
                            }}
                        }});
                        window[observerKey].observe(thread, {{
                            childList: true,
                            subtree: true,
                            characterData: true,
                        }});
                        scheduleScrollToLatest();
                        setTimeout(scheduleScrollToLatest, 120);
                        setTimeout(scheduleScrollToLatest, 320);
                    }})();
                    </script>
                    """,
                    unsafe_allow_html=True,
                )
                return self._entered

            def __exit__(self, exc_type, exc_val, exc_tb):
                return self.wrapped_ctx.__exit__(exc_type, exc_val, exc_tb)

            def __getattr__(self, name):
                return getattr(self._entered or self.wrapped_ctx, name)

        return ChatThreadContext(self, cid, container_ctx, scroll_mode, scroll_behavior)

    def _render_chat_history_body(
        self,
        item: Any,
        *,
        cursor: Optional[str] = "|",
        content_format: Optional[str] = None,
    ) -> bool:
        content = _chat_history_display_text(item)
        chunks = item.get("chunks") if isinstance(item, dict) else None
        resolved_content_format = _resolve_chat_content_format(item, content_format)
        rendered = False
        rendered_text_from_chunks = False

        if chunks:
            if isinstance(chunks, (list, tuple)) and all(isinstance(chunk, str) for chunk in chunks):
                streamed_text = "".join(chunks)
                status = _coerce_chat_text(item.get("status")).strip().lower() if isinstance(item, dict) else ""
                if status == "streaming" and cursor:
                    streamed_text += str(cursor)
                if resolved_content_format == "text":
                    self.text(streamed_text)
                else:
                    self.markdown(streamed_text)
            else:
                status = _coerce_chat_text(item.get("status")).strip().lower() if isinstance(item, dict) else ""
                self.write_stream(chunks, cursor=cursor if status == "streaming" else None)
            rendered_text_from_chunks = True
            rendered = True

        if content and not rendered_text_from_chunks:
            if resolved_content_format == "text":
                self.text(content)
            else:
                self.markdown(content)
            rendered = True

        attachment_html = _render_chat_attachment_html(item)
        if attachment_html:
            self.html(attachment_html)
            rendered = True

        return rendered

    def render_chat_message_body(
        self,
        item: Any,
        *,
        cursor: Optional[str] = "|",
        content_format: Optional[str] = None,
    ) -> bool:
        """Render the shared chat transcript body inside a manual chat_message block.

        Use this helper when building primitive chat UIs with ``chat_thread(...)`` and
        ``chat_message(...)`` directly. It renders plain text, streamed chunks, and the
        default attachment previews used by ``chat_history(...)`` and ``agent_history(...)``.

        ``content_format`` accepts ``"markdown"`` or ``"text"``. When omitted,
        a dict item may supply ``item["content_format"]``; otherwise markdown is used.
        """
        return self._render_chat_history_body(item, cursor=cursor, content_format=content_format)

    def _chat_history_plain_impl(
        self,
        messages,
        *,
        height: Union[int, str] = "58vh",
        cursor: Optional[str] = "|",
        content_format: Optional[str] = None,
        cls: str = "",
        style: str = "",
        border: bool = False,
    ):
        """Render plain chat history without agent-specific metadata."""
        items = messages.value if hasattr(messages, "value") else messages
        with self.chat_thread(height=height, cls=cls, style=style, border=border):
            for item in items or []:
                role = item.get("role", "assistant") if isinstance(item, dict) else "assistant"
                phase = _normalize_chat_phase(item)
                status = _coerce_chat_text(item.get("status")).strip().lower() if isinstance(item, dict) else ""
                thinking_label = _coerce_chat_text(item.get("thinking_label") or "Thinking...").strip() if isinstance(item, dict) else "Thinking..."
                status_text = ""
                if isinstance(item, dict):
                    has_text_output = False
                    chunks = item.get("chunks")
                    if isinstance(chunks, (list, tuple)):
                        has_text_output = any(_coerce_chat_text(chunk).strip() for chunk in chunks)
                    if not has_text_output:
                        has_text_output = bool(_chat_history_display_text(item).strip())
                    has_attachment_output = _chat_message_has_attachments(item)
                    status_text = _coerce_chat_text(item.get("status_text")).strip()
                    thinking = role == "assistant" and not has_text_output and not has_attachment_output and (
                        phase in {"thinking", "running"} or status in {"thinking", "streaming"}
                    )
                    has_visible_primitive_meta = bool(status_text) or thinking
                    if not has_text_output and not has_attachment_output and not has_visible_primitive_meta and role == "assistant":
                        continue
                else:
                    thinking = False
                    has_attachment_output = False
                    has_visible_primitive_meta = False

                with self.chat_message(
                    role,
                    avatar=item.get("avatar") if isinstance(item, dict) else None,
                    thinking=thinking,
                    thinking_label=thinking_label,
                    phase=phase or None,
                    status=status_text,
                    key=item.get("key") if isinstance(item, dict) else None,
                ):
                    if self._render_chat_history_body(item, cursor=cursor, content_format=content_format):
                        continue
                    if isinstance(item, dict) and has_visible_primitive_meta:
                        continue
                    if isinstance(item, dict) and _coerce_chat_text(item.get("error")).strip():
                        self.markdown(_coerce_chat_text(item.get("error")))

    def _chat_history_agent_impl(
        self,
        messages,
        *,
        height: Union[int, str] = "58vh",
        cursor: Optional[str] = "|",
        show_status: bool = True,
        show_summary: bool = True,
        show_trace: bool = True,
        show_artifacts: bool = True,
        cls: str = "",
        style: str = "",
        border: bool = False,
    ):
        """Render chat history from a list-like state using Violit chat widgets.

        Rich agent fields remain part of the message schema. The show_* flags only
        control whether those fields are rendered for this view.
        """
        items = messages.value if hasattr(messages, "value") else messages
        with self.chat_thread(height=height, cls=cls, style=style, border=border):
            for item in items or []:
                role = item.get("role", "assistant") if isinstance(item, dict) else "assistant"
                phase = _normalize_chat_phase(item)
                status = _coerce_chat_text(item.get("status")).strip().lower() if isinstance(item, dict) else ""
                content = item.get("content") if isinstance(item, dict) else str(item)
                chunks = item.get("chunks") if isinstance(item, dict) else None
                thinking_label = item.get("thinking_label", "Thinking...") if isinstance(item, dict) else "Thinking..."
                summary_value = item.get("summary", "") if isinstance(item, dict) and show_summary else ""
                trace_value = item.get("trace") if isinstance(item, dict) and show_trace else None
                artifacts_value = item.get("artifacts") if isinstance(item, dict) and show_artifacts else None
                error_value = item.get("error", "") if isinstance(item, dict) else ""
                has_text_output = False
                if isinstance(chunks, (list, tuple)):
                    has_text_output = any(_coerce_chat_text(chunk).strip() for chunk in chunks)
                if not has_text_output:
                    has_text_output = bool(_chat_history_display_text(item).strip())
                has_attachment_output = _chat_message_has_attachments(item)

                is_agent_item = False
                if isinstance(item, dict):
                    is_agent_item = any(
                        (
                            summary_value,
                            trace_value,
                            artifacts_value,
                            item.get("status_text") if show_status else "",
                            error_value,
                            item.get("phase"),
                        )
                    )

                status_text = ""
                if isinstance(item, dict) and show_status and is_agent_item and not has_text_output:
                    status_text = _coerce_chat_text(
                        item.get("status_text")
                        or (thinking_label if phase in {"thinking", "running"} else "")
                    )

                thinking = show_status and is_agent_item and not has_text_output and (
                    phase in {"thinking", "running"} or status in {"thinking", "streaming"}
                )
                has_visible_agent_meta = any(
                    (
                        _coerce_chat_text(status_text).strip(),
                        summary_value,
                        trace_value,
                        artifacts_value,
                        error_value,
                    )
                )

                if not has_text_output and not has_attachment_output and not has_visible_agent_meta and role == "assistant":
                    continue

                with self.agent_turn(
                    role,
                    avatar=item.get("avatar") if isinstance(item, dict) else None,
                    thinking=thinking,
                    thinking_label=thinking_label,
                    phase=phase,
                    status_text=status_text,
                    summary=summary_value,
                    trace=trace_value,
                    artifacts=artifacts_value,
                    error_text=error_value,
                    key=item.get("key") if isinstance(item, dict) else None,
                ):
                    if self._render_chat_history_body(item, cursor=cursor):
                        pass
                    elif isinstance(item, dict) and error_value:
                        pass
                    elif isinstance(item, dict) and has_visible_agent_meta:
                        pass
                    else:
                        self.caption(thinking_label)

    def chat_history(
        self,
        messages,
        *,
        height: Union[int, str] = "58vh",
        cursor: Optional[str] = "|",
        content_format: Optional[str] = None,
        show_status: bool = True,
        show_summary: bool = True,
        show_trace: bool = True,
        show_artifacts: bool = True,
        cls: str = "",
        style: str = "",
        border: bool = False,
    ):
        """Preferred high-level renderer for chat history state.

        This is the canonical high-level partner for
        ``managed_chat_input(...)`` when you want a general chat transcript.
        It renders the shared chat message schema inside ``chat_thread(...)``
        with plain chat bubbles and ignores agent-only rich metadata.
        """
        return self._chat_history_plain_impl(
            messages,
            height=height,
            cursor=cursor,
            content_format=content_format,
            cls=cls,
            style=style,
            border=border,
        )

    def agent_history(
        self,
        messages,
        *,
        height: Union[int, str] = "58vh",
        cursor: Optional[str] = "|",
        show_status: bool = True,
        show_summary: bool = True,
        show_trace: bool = True,
        show_artifacts: bool = True,
        cls: str = "",
        style: str = "",
        border: bool = False,
    ):
        """Primary high-level renderer for agent-oriented chat history.

        Use this name when the transcript schema is primarily agent-generated
        and rich fields like trace, artifacts, and summary are expected.
        """
        return self._chat_history_agent_impl(
            messages,
            height=height,
            cursor=cursor,
            show_status=show_status,
            show_summary=show_summary,
            show_trace=show_trace,
            show_artifacts=show_artifacts,
            cls=cls,
            style=style,
            border=border,
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
        on_submit: Optional[Callable[..., Any]] = None,
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[dict[str, Any]] = None,
        width: Union[str, int] = "stretch",
        height: Union[str, int] = "content",
        cls: str = "",
        style: str = "",
    ):
        """
        Display a primitive chat input widget.

        This returns the just-submitted value or ``None``.

        When ``accept_file`` or ``accept_audio`` is enabled, the submitted
        value becomes a dict with ``text``, ``files``, and ``audio`` keys.

        For automatic transcript management and assistant reply orchestration,
        use ``managed_chat_input(...)``.
        """

        return self._chat_input_impl(
            placeholder,
            key=key,
            max_chars=max_chars,
            accept_file=accept_file,
            file_type=file_type,
            accept_audio=accept_audio,
            audio_sample_rate=audio_sample_rate,
            disabled=disabled,
            on_submit=on_submit,
            messages=None,
            user_name="user",
            assistant_name="assistant",
            stream_cursor="|",
            stream_speed=None,
            flush_interval=0.01,
            args=args,
            kwargs=kwargs,
            width=width,
            height=height,
            auto_scroll=True,
            cls=cls,
            style=style,
            multiline=True,
            submit_on_enter=True,
            submit_policy="drop",
            auto_disable_while_pending=True,
            show_stop_button=False,
            pinned=None,
            scroll_behavior="smooth",
        )

    def managed_chat_input(
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
        submit_policy: str = "drop",
        auto_disable_while_pending: bool = True,
        show_stop_button: bool = False,
        pinned: Optional[bool] = None,
        scroll_behavior: str = "smooth",
    ):
        """
        Display a high-level managed chat input.

        This layer can append user messages, create assistant placeholders,
        stream text or typed agent events, and manage submit/cancel policy.

        When ``accept_file`` or ``accept_audio`` is enabled, ``on_submit``
        receives a dict with ``text``, ``files``, and ``audio`` keys.

        Pair this with ``chat_history(...)`` for the default high-level chat
        surface, or with ``agent_history(...)`` in agent-first apps.
        """
        return self._chat_input_impl(
            placeholder,
            key=key,
            max_chars=max_chars,
            accept_file=accept_file,
            file_type=file_type,
            accept_audio=accept_audio,
            audio_sample_rate=audio_sample_rate,
            disabled=disabled,
            on_submit=on_submit,
            messages=messages,
            user_name=user_name,
            assistant_name=assistant_name,
            stream_cursor=stream_cursor,
            stream_speed=stream_speed,
            flush_interval=flush_interval,
            args=args,
            kwargs=kwargs,
            width=width,
            height=height,
            auto_scroll=auto_scroll,
            cls=cls,
            style=style,
            multiline=multiline,
            submit_on_enter=submit_on_enter,
            submit_policy=submit_policy,
            auto_disable_while_pending=auto_disable_while_pending,
            show_stop_button=show_stop_button,
            pinned=pinned,
            scroll_behavior=scroll_behavior,
        )

    def _chat_input_impl(
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
        submit_policy: str = "drop",
        auto_disable_while_pending: bool = True,
        show_stop_button: bool = False,
        pinned: Optional[bool] = None,
        scroll_behavior: str = "smooth",
    ):
        """
        Internal implementation for primitive and high-level chat input layers.

        If `messages` is provided and `on_submit` returns a string, the string
        becomes the assistant reply. If it returns an iterable, the iterable is
        streamed into the assistant bubble automatically.

        `stream_speed` accepts presets like "fast", "balanced", "smooth",
        "cinematic" or a smoothness score from 1 to 10, where 10 is the
        smoothest. It can also be provided as a State-like object or callable
        so the active preset is resolved when the user submits a message.

        `submit_policy` controls what happens when the same chat input is
        submitted again while a previous reply is still running. Supported
        values are "drop" (default) and "queue".

        If `auto_disable_while_pending` is True, pending Enter submits are
        blocked while a reply is in flight, but the textarea stays editable so
        draft text is preserved until the run finishes. If it is False,
        pending Enter submits follow `submit_policy`: `queue` submits the
        draft for the next turn and `drop` clears the current draft without
        sending it.

        If `show_stop_button` is True, the send button becomes a stop button
        while a reply is in flight. Clicking stop temporarily locks the input
        until cancellation finishes, then the send button returns so the user
        can continue the conversation. Pressing Enter never acts as stop.

        When file or audio capture is enabled, submitted values are normalized
        into a dict payload with ``text``, ``files``, and ``audio`` entries.
        """
        file_upload_enabled, file_upload_multiple, file_upload_directory = _resolve_chat_file_accept_mode(accept_file)
        file_accept_attr = _resolve_chat_file_accept_attr(file_type)
        audio_capture_enabled = bool(accept_audio)

        cid = f"chat_input_{_sanitize_chat_key(key)}" if key is not None else self._get_next_cid("chat_input")
        stop_cid = f"{cid}__stop"
        store = get_session_store()
        normalized_submit_policy = str(submit_policy).strip().lower() or "drop"
        if normalized_submit_policy not in {"drop", "queue"}:
            raise ValueError("submit_policy must be either 'drop' or 'queue'.")
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
            submit_callback = on_submit
            val = _parse_chat_submit_value(val)
            if isinstance(val, str):
                val = val.strip()
            if not _chat_submit_has_value(val):
                return

            if _is_chat_submit_inflight(store, cid):
                if normalized_submit_policy == "queue":
                    _enqueue_chat_submit(store, cid, val)
                return

            def clear_submit_lock():
                _set_chat_submit_inflight(store, cid, False)
                _set_chat_submit_task(store, cid, None)
                store.setdefault('forced_dirty', set()).add(cid)
                _push_stream_frame(self)

            def clear_submit_lock_and_continue():
                clear_submit_lock()
                next_value = _dequeue_chat_submit(store, cid)
                if next_value is not None:
                    handler(next_value)

            if messages is None:
                _set_chat_submit_inflight(store, cid, True)
                try:
                    submit_callback(*callback_args, val, **callback_kwargs)
                finally:
                    clear_submit_lock_and_continue()
                return

            _set_chat_submit_inflight(store, cid, True)

            try:
                user_message: dict[str, Any] = {
                    "role": user_name,
                    "content": _chat_submit_display_text(val),
                    "status": "done",
                }
                if isinstance(val, dict):
                    user_message["text"] = _coerce_chat_text(val.get("text")).strip()
                    if val.get("files"):
                        user_message["files"] = list(val.get("files") or [])
                    if val.get("audio") is not None:
                        user_message["audio"] = val.get("audio")

                messages.set(_clone_chat_items(messages) + [
                    user_message,
                    {
                        "role": assistant_name,
                        "content": "",
                        "chunks": [],
                        "status": "thinking",
                        "phase": "thinking",
                        "thinking_label": "Thinking...",
                        "cursor": None,
                    },
                ])

                stream_profile = _resolve_stream_profile(
                    _resolve_stream_speed_value(stream_speed),
                    flush_interval,
                )

                def run_reply():
                    task = _get_chat_submit_task(store, cid)

                    def check_cancelled():
                        if task is not None:
                            task.check_cancelled()

                    result = submit_callback(*callback_args, val, **callback_kwargs)
                    check_cancelled()

                    if isinstance(result, str):
                        reply = result.strip()
                        if not reply:
                            raise RuntimeError("Chat reply was empty.")
                        _patch_last_chat_item(
                            messages,
                            content=reply,
                            chunks=[],
                            status="done",
                            phase="done",
                            status_text="",
                            cursor=None,
                        )
                        return reply

                    candidate = result() if callable(result) and not hasattr(result, "__iter__") else result
                    if not hasattr(candidate, "__iter__"):
                        reply = str(result).strip()
                        if not reply:
                            raise RuntimeError("Chat reply was empty.")
                        _patch_last_chat_item(
                            messages,
                            content=reply,
                            chunks=[],
                            status="done",
                            phase="done",
                            status_text="",
                            cursor=None,
                        )
                        return reply

                    chunks = []
                    agent_stream_seen = False
                    last_emit_at = time.perf_counter()
                    pending_emit_chars = 0
                    for raw_chunk in cast(Any, candidate):
                        check_cancelled()
                        if _is_agent_event(raw_chunk):
                            agent_stream_seen = True
                            event_type = _coerce_chat_text(raw_chunk.get("type") or raw_chunk.get("event")).strip().lower() if isinstance(raw_chunk, dict) else ""
                            event_text = _coerce_chat_text(
                                raw_chunk.get("text") or raw_chunk.get("content") or raw_chunk.get("message")
                            ) if isinstance(raw_chunk, dict) else ""
                            event_should_stream = True
                            if isinstance(raw_chunk, dict) and raw_chunk.get("stream") is not None:
                                event_should_stream = bool(raw_chunk.get("stream"))

                            if event_type == "text" and event_text and event_should_stream:
                                fragments = list(
                                    _iter_stream_text_fragments(
                                        event_text,
                                        preferred_size=stream_profile["fragment_size"],
                                        mode=stream_profile["fragment_mode"],
                                    )
                                )
                                for fragment in fragments:
                                    check_cancelled()
                                    fragment_event = dict(raw_chunk)
                                    fragment_event["text"] = fragment
                                    _patch_last_chat_item_with_event(messages, fragment_event, cursor=stream_cursor)
                                    pending_emit_chars += len(fragment)
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
                                continue

                            _patch_last_chat_item_with_event(messages, raw_chunk, cursor=stream_cursor)
                            _push_stream_frame(self)
                            last_emit_at = time.perf_counter()
                            pending_emit_chars = 0
                            continue

                        chunk = self._extract_stream_chunk(raw_chunk)
                        text = chunk if isinstance(chunk, str) else str(chunk)
                        if not text:
                            continue

                        if agent_stream_seen:
                            chunks.append(text)
                            _patch_last_chat_item(
                                messages,
                                chunks=list(chunks),
                                content="".join(chunks),
                                status="streaming",
                                phase="running",
                                status_text="",
                                cursor=stream_cursor,
                            )
                            _push_stream_frame(self)
                            continue

                        fragments = list(
                            _iter_stream_text_fragments(
                                text,
                                preferred_size=stream_profile["fragment_size"],
                                mode=stream_profile["fragment_mode"],
                            )
                        )
                        for fragment in fragments:
                            check_cancelled()
                            chunks.append(fragment)
                            pending_emit_chars += len(fragment)
                            _patch_last_chat_item(
                                messages,
                                chunks=list(chunks),
                                status="streaming",
                                phase="running",
                                status_text="",
                                cursor=stream_cursor,
                            )
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
                    if agent_stream_seen:
                        last_item = (_clone_chat_items(messages)[-1] if getattr(messages, "value", None) else None)
                        final_updates: dict[str, Any] = {
                            "cursor": None,
                        }
                        if last_item and _normalize_chat_phase(last_item) != "error":
                            final_updates["phase"] = "done"
                            final_updates["status"] = "done"
                            final_updates["status_text"] = ""
                        if reply:
                            final_updates["content"] = reply
                            final_updates["chunks"] = list(chunks)
                        _patch_last_chat_item(messages, **final_updates)
                        final_item = _clone_chat_items(messages)[-1]
                        if not _chat_item_has_visible_content(final_item):
                            raise RuntimeError("Chat reply was empty.")
                        return reply or _coerce_chat_text(final_item.get("summary")).strip() or "done"

                    if not reply:
                        raise RuntimeError("Chat reply was empty.")
                    _patch_last_chat_item(
                        messages,
                        content=reply,
                        chunks=list(chunks),
                        status="done",
                        phase="done",
                        status_text="",
                        cursor=None,
                    )
                    return reply

                def cancel_reply():
                    last_item = (_clone_chat_items(messages)[-1] if getattr(messages, "value", None) else None)
                    stop_notice = "대화가 중단되었습니다."
                    last_content = ""
                    last_chunks: list[str] = []
                    if isinstance(last_item, dict):
                        last_content = _coerce_chat_text(last_item.get("content"))
                        raw_chunks = last_item.get("chunks")
                        if isinstance(raw_chunks, list):
                            last_chunks = [_coerce_chat_text(chunk) for chunk in raw_chunks]
                    base_content = last_content.rstrip()
                    if not base_content and last_chunks:
                        base_content = "".join(last_chunks).rstrip()
                    final_updates: dict[str, Any] = {
                        "content": f"{base_content}\n\n{stop_notice}" if base_content else stop_notice,
                        "chunks": [],
                        "cursor": None,
                        "status": "done",
                        "phase": "done",
                        "status_text": "",
                    }
                    _patch_last_chat_item(messages, **final_updates)
                    clear_submit_lock_and_continue()

                def fail_reply(exc):
                    _patch_last_chat_item(
                        messages,
                        content=f"Error:\n\n```text\n{exc}\n```",
                        chunks=[],
                        status="error",
                        phase="error",
                        status_text="",
                        cursor=None,
                    )

                def fail_reply_and_unlock(exc):
                    try:
                        fail_reply(exc)
                    finally:
                        clear_submit_lock_and_continue()

                task = self.background(
                    run_reply,
                    on_complete=clear_submit_lock_and_continue,
                    on_cancel=cancel_reply,
                    on_error=fail_reply_and_unlock,
                    flush_interval=stream_profile["flush_interval"],
                )
                _set_chat_submit_task(store, cid, task)
                task.start()
            except Exception:
                clear_submit_lock_and_continue()
                raise

        def stop_handler(_val=None):
            task = _get_chat_submit_task(store, cid)
            if task is None:
                return
            task.cancel()
        
        # Use static_actions for initial registration, but the handler
        # captures the session-specific on_submit callback via closure
        self.static_actions[cid] = handler
        self.static_actions[stop_cid] = stop_handler
            
        def builder():
            # Fixed bottom input
            # We use window.lastActiveChatInput to restore focus after re-render/replacement
            server_submit_pending = _is_chat_submit_inflight(store, cid)
            effective_disabled = bool(disabled)
            stop_button_active = bool(show_stop_button and server_submit_pending)
            placeholder_js = json.dumps(placeholder)
            submit_on_enter_js = "true" if submit_on_enter else "false"
            scroll_mode = self._resolve_chat_scroll_mode(auto_scroll)
            scroll_mode_js = json.dumps(scroll_mode)
            scroll_behavior_js = json.dumps(scroll_behavior)
            stop_button_js = "true" if stop_button_active else "false"
            file_upload_enabled_js = "true" if file_upload_enabled else "false"
            audio_capture_enabled_js = "true" if audio_capture_enabled else "false"
            audio_sample_rate_js = json.dumps(audio_sample_rate)
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

            attachment_controls_html = ""
            if file_upload_enabled:
                attachment_controls_html += f'''
                        <wa-button id="attach_{cid}" type="button" size="small" variant="text" appearance="plain" style="flex:0 0 auto; --wa-button-padding-inline: 0.55rem;" title="Attach file">
                            <span aria-hidden="true" style="display:flex;align-items:center;justify-content:center;line-height:0;">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width:1rem;height:1rem;display:block;fill:currentColor;"><path d="M208 64c-61.9 0-112 50.1-112 112v184c0 79.5 64.5 144 144 144s144-64.5 144-144V184c0-35.3-28.7-64-64-64s-64 28.7-64 64v168c0 8.8-7.2 16-16 16s-16-7.2-16-16V192h-48v160c0 35.3 28.7 64 64 64s64-28.7 64-64V184c0-61.9-50.1-112-112-112s-112 50.1-112 112v176h48V184c0-35.3 28.7-64 64-64z"/></svg>
                            </span>
                        </wa-button>
                        <input type="file" id="file_{cid}" accept="{html_lib.escape(file_accept_attr, quote=True)}" {'multiple' if file_upload_multiple else ''} {'webkitdirectory directory' if file_upload_directory else ''} style="display:none;" />
                '''
            if audio_capture_enabled:
                attachment_controls_html += f'''
                        <wa-button id="audio_{cid}" type="button" size="small" variant="text" appearance="plain" style="flex:0 0 auto; --wa-button-padding-inline: 0.55rem;" title="Record audio">
                            <span aria-hidden="true" style="display:flex;align-items:center;justify-content:center;line-height:0;">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" style="width:0.95rem;height:0.95rem;display:block;fill:currentColor;"><path d="M192 0c-53 0-96 43-96 96v128c0 53 43 96 96 96s96-43 96-96V96c0-53-43-96-96-96zm-128 224H32c0 88.4 63.1 162 148 174.4V480H120c-13.3 0-24 10.7-24 24s10.7 24 24 24h144c13.3 0 24-10.7 24-24s-10.7-24-24-24h-60v-81.6C288.9 386 352 312.4 352 224h-32c0 70.7-57.3 128-128 128S64 294.7 64 224z"/></svg>
                            </span>
                        </wa-button>
                '''
            attachment_meta_html = ""
            if file_upload_enabled or audio_capture_enabled:
                attachment_meta_html = f'''
                        <div id="meta_{cid}" data-chat-part="input-meta" style="display:none;font-size:0.78rem;color:var(--vl-text-muted);padding:0 12px 8px;line-height:1.35;"></div>
                '''
            
            html = f'''
            <div class="chat-input-container vl-chat-input-container{(' ' + html_lib.escape(cls, quote=True)) if cls else ''}" data-chat-pinned="{'true' if effective_pinned else 'false'}" data-chat-part="input-container" style="
                {container_style}
            ">
                <div class="vl-chat-input-root" data-chat-input-root="{cid}" data-chat-submit-pending="{'true' if server_submit_pending else 'false'}" data-chat-part="input-root" style="
                    {width_style}
                    max-width: 860px;
                    display: flex;
                    align-items: flex-end;
                    gap: 10px;
                    pointer-events: auto;
                ">
                    <div class="vl-chat-input-surface" data-chat-part="input-surface" style="
                        flex: 1;
                        min-width: 0;
                        background: color-mix(in srgb, var(--vl-bg-card) 92%, var(--vl-bg) 8%);
                        border: 1px solid color-mix(in srgb, var(--vl-border) 80%, transparent);
                        border-radius: var(--vl-chat-input-surface-radius, 24px);
                        padding: var(--vl-chat-input-surface-padding, 10px);
                        box-shadow: 0 20px 40px color-mix(in srgb, var(--vl-border) 10%, transparent);
                    ">
                        {('<div class="vl-chat-input-toolbar" data-chat-part="input-toolbar" style="display:flex;align-items:center;gap:6px;padding:2px 6px 6px;">' + attachment_controls_html + '<div style="flex:1 1 auto;"></div></div>') if attachment_controls_html else ''}
                        <textarea id="input_{cid}" class="chat-input-box vl-chat-input-box" data-chat-part="input-textarea" placeholder={placeholder_js}
                            rows="1"
                            {"maxlength=" + '"' + str(max_chars) + '"' if max_chars else ""}
                            {"disabled" if effective_disabled else ""}
                            oninput="window.syncChatInput_{cid} && window.syncChatInput_{cid}()"
                            style="
                                width: 100%;
                                border: none;
                                background: transparent;
                                padding: 10px 12px;
                                font-size: var(--vl-chat-input-font-size, 1rem);
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
                        {attachment_meta_html}
                    </div>
                    <wa-button id="send_{cid}" type="button" size="small" variant="brand" appearance="accent" {"" if stop_button_active else ("disabled" if disabled else "")} style="flex: 0 0 var(--vl-chat-input-button-size, 48px); min-width: var(--vl-chat-input-button-size, 48px); width: var(--vl-chat-input-button-size, 48px); height: var(--vl-chat-input-button-size, 48px); margin-bottom: 2px; --wa-button-padding-inline: 0;" onclick="
                        {f'window.stopChatInput_{cid}();' if stop_button_active else f'window.submitChatInput_{cid}();'}
                    ">
                        <span aria-hidden="true" style="display:flex;align-items:center;justify-content:center;width:100%;height:100%;line-height:0;">
                            {('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width:1rem;height:1rem;display:block;fill:currentColor;"><rect x="128" y="128" width="256" height="256" rx="32" ry="32"/></svg>') if stop_button_active else ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width:1rem;height:1rem;display:block;fill:currentColor;transform:translate(-1.5px, 1px);transform-origin:center;"><path d="M476.6 3.2c18.6 10.5 27.5 32.4 21.8 53.1l-96 352c-4 14.8-18.2 25.3-33.5 25.7s-30-9.1-34.8-23.6l-48.6-145.9-145.9-48.6C125.1 211 115.2 196.4 115.6 181s10.9-29.5 25.7-33.5l352-96c20.7-5.7 42.6 3.2 53.1 21.8zM176.9 177.1l125.4 41.8 41.8 125.4L426.7 41.6 176.9 177.1z"/></svg>')}
                        </span>
                    </wa-button>
                </div>
            </div>
            {spacer_html}
            <script>
                (function() {{
                    const el = document.getElementById('input_{cid}');
                    const sendButton = document.getElementById('send_{cid}');
                    const attachButton = document.getElementById('attach_{cid}');
                    const fileInput = document.getElementById('file_{cid}');
                    const audioButton = document.getElementById('audio_{cid}');
                    const attachmentMeta = document.getElementById('meta_{cid}');
                    const root = document.querySelector('[data-chat-input-root="{cid}"]');
                    if (!el) return;
                    const surface = root?.querySelector('[data-chat-part="input-surface"]');
                    const clientPendingKey = '__violitChatClientPending_{cid}';
                    const pendingPhaseKey = '__violitChatPendingPhase_{cid}';
                    const pendingSeenChatKey = '__violitChatPendingSeenChat_{cid}';
                    const draftKey = '__violitChatDraft_{cid}';
                    const fileStateKey = '__violitChatFiles_{cid}';
                    const audioStateKey = '__violitChatAudio_{cid}';
                    const audioErrorKey = '__violitChatAudioError_{cid}';
                    const audioRecorderKey = '__violitChatAudioRecorder_{cid}';
                    const audioStreamKey = '__violitChatAudioStream_{cid}';
                    const dropDepthKey = '__violitChatDropDepth_{cid}';
                    const initialDisabled = {'true' if effective_disabled else 'false'};
                    const autoDisableWhilePending = {'true' if auto_disable_while_pending else 'false'};
                    const tracksAssistantMessages = {'true' if messages is not None else 'false'};
                    const submitPolicy = {json.dumps(normalized_submit_policy)};
                    const fileUploadEnabled = {file_upload_enabled_js};
                    const audioCaptureEnabled = {audio_capture_enabled_js};
                    const preferredAudioSampleRate = {audio_sample_rate_js};
                    const isServerPending = () => root?.dataset.chatSubmitPending === 'true';
                    if (typeof window[pendingPhaseKey] !== 'string') {{
                        window[pendingPhaseKey] = 'idle';
                    }}
                    if (typeof window[pendingSeenChatKey] !== 'boolean') {{
                        window[pendingSeenChatKey] = false;
                    }}
                    if (!Array.isArray(window[fileStateKey])) {{
                        window[fileStateKey] = [];
                    }}
                    if (typeof window[audioStateKey] === 'undefined') {{
                        window[audioStateKey] = null;
                    }}
                    if (typeof window[audioErrorKey] !== 'string') {{
                        window[audioErrorKey] = '';
                    }}
                    if (typeof window[dropDepthKey] !== 'number') {{
                        window[dropDepthKey] = 0;
                    }}
                    const getPendingPhase = () => {{
                        const phase = window[pendingPhaseKey];
                        return phase === 'submitted' || phase === 'server' || phase === 'stopping' ? phase : 'idle';
                    }};
                    const setPendingPhase = (phase) => {{
                        const nextPhase = phase === 'submitted' || phase === 'server' || phase === 'stopping' ? phase : 'idle';
                        window[pendingPhaseKey] = nextPhase;
                        window[clientPendingKey] = nextPhase !== 'idle';
                        if (nextPhase === 'idle') {{
                            window[pendingSeenChatKey] = false;
                        }}
                    }};
                    const hasRunningAssistantMessage = () => {{
                        const chatThread = getChatThread();
                        if (!chatThread) return false;
                        return !!chatThread.querySelector(
                            '[data-chat-message="true"][data-chat-role="assistant"][data-chat-phase="thinking"], ' +
                            '[data-chat-message="true"][data-chat-role="assistant"][data-chat-phase="running"], ' +
                            '[data-chat-message="true"][data-chat-role="assistant"][data-chat-thinking="true"]'
                        );
                    }};
                    const hasCompletedAssistantAfterLatestUser = () => {{
                        const chatThread = getChatThread();
                        if (!chatThread) return false;
                        const messages = Array.from(chatThread.querySelectorAll('[data-chat-message="true"]'));
                        let lastUserIndex = -1;
                        let lastCompletedAssistantIndex = -1;
                        messages.forEach((node, index) => {{
                            if (!(node instanceof Element)) return;
                            const role = node.getAttribute('data-chat-role');
                            const phase = node.getAttribute('data-chat-phase');
                            if (role === 'user') {{
                                lastUserIndex = index;
                            }}
                            if (role === 'assistant' && (phase === 'done' || phase === 'error')) {{
                                lastCompletedAssistantIndex = index;
                            }}
                        }});
                        return lastUserIndex !== -1 && lastCompletedAssistantIndex > lastUserIndex;
                    }};
                    const clearStaleServerPendingFromTranscript = () => {{
                        if (!root || !isServerPending() || !window[pendingSeenChatKey]) return false;
                        if (hasRunningAssistantMessage()) return false;
                        if (!hasCompletedAssistantAfterLatestUser()) return false;
                        root.dataset.chatSubmitPending = 'false';
                        return true;
                    }};
                    const syncPendingPhase = () => {{
                        clearStaleServerPendingFromTranscript();
                        if (getPendingPhase() === 'stopping') {{
                            if (isServerPending() || hasRunningAssistantMessage()) {{
                                setPendingPhase('server');
                                window[pendingSeenChatKey] = true;
                                return;
                            }}
                            setPendingPhase('idle');
                            return;
                        }}
                        if (isServerPending()) {{
                            setPendingPhase('server');
                            window[pendingSeenChatKey] = true;
                            return;
                        }}
                        if (hasRunningAssistantMessage()) {{
                            setPendingPhase('server');
                            window[pendingSeenChatKey] = true;
                            return;
                        }}
                        if (getPendingPhase() === 'server') {{
                            setPendingPhase('idle');
                            return;
                        }}
                        if (getPendingPhase() === 'submitted' && !tracksAssistantMessages) {{
                            setPendingPhase('idle');
                            return;
                        }}
                        if (getPendingPhase() === 'submitted' && window[pendingSeenChatKey]) {{
                            setPendingPhase('idle');
                        }}
                    }};
                    setPendingPhase(getPendingPhase());
                    const isClientPending = () => tracksAssistantMessages && getPendingPhase() !== 'idle';
                    const isPending = () => isServerPending() || isClientPending();
                    const isStopping = () => getPendingPhase() === 'stopping';
                    const isInputHardDisabled = () => {'true' if disabled else 'false'};
                    const getSelectedFiles = () => Array.isArray(window[fileStateKey]) ? window[fileStateKey] : [];
                    const setSelectedFiles = (files) => {{
                        window[fileStateKey] = Array.isArray(files) ? files : [];
                    }};
                    const getRecordedAudio = () => window[audioStateKey] && typeof window[audioStateKey] === 'object' ? window[audioStateKey] : null;
                    const setRecordedAudio = (audio) => {{
                        window[audioStateKey] = audio || null;
                    }};
                    const getAudioError = () => typeof window[audioErrorKey] === 'string' ? window[audioErrorKey] : '';
                    const setAudioError = (message) => {{
                        window[audioErrorKey] = typeof message === 'string' ? message : '';
                    }};
                    const isRecordingAudio = () => root?.dataset.chatAudioRecording === 'true';
                    const setRecordingAudio = (active) => {{
                        if (root) {{
                            root.dataset.chatAudioRecording = active ? 'true' : 'false';
                        }}
                    }};
                    const stopAudioStream = () => {{
                        const stream = window[audioStreamKey];
                        if (stream && typeof stream.getTracks === 'function') {{
                            stream.getTracks().forEach((track) => track.stop());
                        }}
                        window[audioStreamKey] = null;
                    }};
                    const extensionFromMime = (mime) => {{
                        const normalized = String(mime || '').toLowerCase();
                        if (normalized.includes('ogg')) return 'ogg';
                        if (normalized.includes('mp4') || normalized.includes('mpeg')) return 'm4a';
                        if (normalized.includes('wav')) return 'wav';
                        return 'webm';
                    }};
                    const renderAttachmentMeta = () => {{
                        if (!attachmentMeta) return;
                        const parts = [];
                        const files = getSelectedFiles();
                        const audio = getRecordedAudio();
                        const audioError = getAudioError();
                        if (isRecordingAudio()) {{
                            parts.push('Recording audio...');
                        }}
                        if (files.length) {{
                            const names = files.slice(0, 3).map((file) => file.name || 'attachment').join(', ');
                            const extra = files.length > 3 ? ` (+${{files.length - 3}} more)` : '';
                            parts.push(`Files: ${{names}}${{extra}}`);
                        }}
                        if (audio) {{
                            parts.push(`Audio: ${{audio.name || 'voice-note'}}`);
                        }}
                        if (audioError) {{
                            parts.push(audioError);
                        }}
                        attachmentMeta.textContent = parts.join(' • ');
                        attachmentMeta.style.display = parts.length ? 'block' : 'none';
                    }};
                    const clearAttachmentState = () => {{
                        setSelectedFiles([]);
                        setRecordedAudio(null);
                        setAudioError('');
                        if (fileInput) {{
                            fileInput.value = '';
                        }}
                        renderAttachmentMeta();
                    }};
                    const hasAttachmentValue = () => getSelectedFiles().length > 0 || !!getRecordedAudio();
                    const isFileDragEvent = (event) => {{
                        const types = Array.from(event?.dataTransfer?.types || []);
                        return types.includes('Files');
                    }};
                    const setDropActive = (active) => {{
                        if (!surface) return;
                        surface.dataset.chatDropActive = active ? 'true' : 'false';
                        surface.style.borderColor = active
                            ? 'color-mix(in srgb, var(--vl-primary, #7c3aed) 72%, white 28%)'
                            : 'color-mix(in srgb, var(--vl-border) 80%, transparent)';
                        surface.style.background = active
                            ? 'color-mix(in srgb, var(--vl-bg-card) 84%, var(--vl-primary, #7c3aed) 16%)'
                            : 'color-mix(in srgb, var(--vl-bg-card) 92%, var(--vl-bg) 8%)';
                        surface.style.boxShadow = active
                            ? '0 0 0 3px color-mix(in srgb, var(--vl-primary, #7c3aed) 18%, transparent), 0 20px 40px color-mix(in srgb, var(--vl-border) 10%, transparent)'
                            : '0 20px 40px color-mix(in srgb, var(--vl-border) 10%, transparent)';
                    }};
                    const renderSendButtonMode = () => {{
                        if (!sendButton) return;
                        const stopActive = {'true' if show_stop_button else 'false'} && isPending();
                        sendButton.innerHTML = stopActive
                            ? '<span aria-hidden="true" style="display:flex;align-items:center;justify-content:center;width:100%;height:100%;line-height:0;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width:1rem;height:1rem;display:block;fill:currentColor;"><rect x="128" y="128" width="256" height="256" rx="32" ry="32"/></svg></span>'
                            : '<span aria-hidden="true" style="display:flex;align-items:center;justify-content:center;width:100%;height:100%;line-height:0;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width:1rem;height:1rem;display:block;fill:currentColor;transform:translate(-1.5px, 1px);transform-origin:center;"><path d="M476.6 3.2c18.6 10.5 27.5 32.4 21.8 53.1l-96 352c-4 14.8-18.2 25.3-33.5 25.7s-30-9.1-34.8-23.6l-48.6-145.9-145.9-48.6C125.1 211 115.2 196.4 115.6 181s10.9-29.5 25.7-33.5l352-96c20.7-5.7 42.6 3.2 53.1 21.8zM176.9 177.1l125.4 41.8 41.8 125.4L426.7 41.6 176.9 177.1z"/></svg></span>';
                        sendButton.onclick = stopActive
                            ? () => window.stopChatInput_{cid}()
                            : () => window.submitChatInput_{cid}();
                    }};
                    const renderAudioButtonMode = () => {{
                        if (!audioButton) return;
                        if (isRecordingAudio()) {{
                            audioButton.innerHTML = '<span aria-hidden="true" style="display:flex;align-items:center;justify-content:center;line-height:0;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width:0.95rem;height:0.95rem;display:block;fill:currentColor;"><rect x="128" y="128" width="256" height="256" rx="32" ry="32"/></svg></span>';
                            audioButton.title = 'Stop recording';
                            return;
                        }}
                        audioButton.innerHTML = '<span aria-hidden="true" style="display:flex;align-items:center;justify-content:center;line-height:0;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" style="width:0.95rem;height:0.95rem;display:block;fill:currentColor;"><path d="M192 0c-53 0-96 43-96 96v128c0 53 43 96 96 96s96-43 96-96V96c0-53-43-96-96-96zm-128 224H32c0 88.4 63.1 162 148 174.4V480H120c-13.3 0-24 10.7-24 24s10.7 24 24 24h144c13.3 0 24-10.7 24-24s-10.7-24-24-24h-60v-81.6C288.9 386 352 312.4 352 224h-32c0 70.7-57.3 128-128 128S64 294.7 64 224z"/></svg></span>';
                        audioButton.title = getRecordedAudio() ? 'Replace audio recording' : 'Record audio';
                    }};
                    const syncTextareaDisabledState = () => {{
                        el.disabled = isInputHardDisabled() || isStopping();
                    }};
                    const syncAuxButtonState = () => {{
                        const disableAttach = isInputHardDisabled() || isPending() || isStopping() || isRecordingAudio();
                        if (attachButton) {{
                            attachButton.disabled = disableAttach;
                        }}
                        if (audioButton) {{
                            audioButton.disabled = isInputHardDisabled() || isPending();
                        }}
                        renderAudioButtonMode();
                    }};
                    if (!initialDisabled && !isPending()) {{
                        setPendingPhase('idle');
                    }}
                    if (typeof window[draftKey] !== 'string') {{
                        window[draftKey] = '';
                    }}

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

                    const syncDraftState = () => {{
                        window[draftKey] = el.value || '';
                    }};

                    window.syncChatInput_{cid} = () => {{
                        syncDraftState();
                        autoResize();
                        syncSendButtonState();
                    }};

                    const restoreDraftState = () => {{
                        const savedDraft = typeof window[draftKey] === 'string' ? window[draftKey] : '';
                        if (!savedDraft) return;
                        if ((el.value || '') === savedDraft) return;
                        el.value = savedDraft;
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
                        if (!sendButton) return;
                        syncPendingPhase();
                        syncTextareaDisabledState();
                        syncAuxButtonState();
                        renderSendButtonMode();
                        if (isStopping() || isRecordingAudio()) {{
                            sendButton.disabled = true;
                            sendButton.setAttribute('aria-disabled', 'true');
                            return;
                        }}
                        if ({'true' if show_stop_button else 'false'} && isPending()) {{
                            sendButton.disabled = false;
                            sendButton.setAttribute('aria-disabled', 'false');
                            return;
                        }}
                        if (isInputHardDisabled() || isPending()) {{
                            sendButton.disabled = true;
                            sendButton.setAttribute('aria-disabled', 'true');
                            return;
                        }}
                        const hasValue = !!((el.value || '').trim()) || hasAttachmentValue();
                        sendButton.disabled = !hasValue;
                        sendButton.setAttribute('aria-disabled', hasValue ? 'false' : 'true');
                    }};

                    const isInteractiveChatTarget = (target) => {{
                        if (!(target instanceof Element)) return false;
                        return !!target.closest(
                            'textarea, input, button, a, label, select, option, summary, [contenteditable="true"], [data-chat-interactive="true"], wa-button, wa-icon-button, wa-select, wa-input, wa-textarea, wa-dropdown'
                        );
                    }};

                    const readSelectedFiles = (files) => Promise.all(files.map((file) => new Promise((resolve, reject) => {{
                        const reader = new FileReader();
                        reader.onload = (event) => resolve({{
                            name: file.name,
                            type: file.type,
                            size: file.size,
                            content: event.target?.result || '',
                            relative_path: file.webkitRelativePath || '',
                        }});
                        reader.onerror = (error) => reject(error);
                        reader.readAsDataURL(file);
                    }})));
                    const processSelectedFiles = async (selected) => {{
                        if (!selected.length) {{
                            setSelectedFiles([]);
                            renderAttachmentMeta();
                            syncSendButtonState();
                            return;
                        }}
                        setAudioError('');
                        if (attachmentMeta) {{
                            attachmentMeta.textContent = 'Reading attachments...';
                            attachmentMeta.style.display = 'block';
                        }}
                        try {{
                            const payloads = await readSelectedFiles(selected);
                            setSelectedFiles({"payloads" if file_upload_multiple else "payloads.slice(0, 1)"});
                        }} catch (_error) {{
                            setAudioError('Failed to read the selected file.');
                        }}
                        renderAttachmentMeta();
                        syncSendButtonState();
                    }};

                    const stopAudioRecording = () => {{
                        const recorder = window[audioRecorderKey];
                        if (recorder && recorder.state !== 'inactive') {{
                            recorder.stop();
                        }}
                    }};

                    const startAudioRecording = async () => {{
                        if (!audioCaptureEnabled) return;
                        if (isRecordingAudio()) {{
                            stopAudioRecording();
                            return;
                        }}
                        if (isInputHardDisabled() || isPending()) return;
                        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || typeof MediaRecorder === 'undefined') {{
                            setAudioError('Audio recording is not supported in this browser.');
                            renderAttachmentMeta();
                            syncSendButtonState();
                            return;
                        }}

                        try {{
                            const constraints = preferredAudioSampleRate
                                ? {{ audio: {{ sampleRate: {{ ideal: preferredAudioSampleRate }} }} }}
                                : {{ audio: true }};
                            const stream = await navigator.mediaDevices.getUserMedia(constraints);
                            const mimeCandidates = ['audio/webm;codecs=opus', 'audio/webm', 'audio/ogg;codecs=opus', 'audio/ogg', 'audio/mp4'];
                            let mimeType = '';
                            for (const candidate of mimeCandidates) {{
                                if (MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(candidate)) {{
                                    mimeType = candidate;
                                    break;
                                }}
                            }}
                            const recorder = mimeType ? new MediaRecorder(stream, {{ mimeType }}) : new MediaRecorder(stream);
                            const chunks = [];
                            window[audioRecorderKey] = recorder;
                            window[audioStreamKey] = stream;
                            setAudioError('');
                            setRecordedAudio(null);
                            recorder.ondataavailable = (event) => {{
                                if (event.data && event.data.size > 0) {{
                                    chunks.push(event.data);
                                }}
                            }};
                            recorder.onerror = () => {{
                                setAudioError('Failed to capture audio.');
                                setRecordingAudio(false);
                                stopAudioStream();
                                renderAttachmentMeta();
                                syncSendButtonState();
                            }};
                            recorder.onstop = () => {{
                                const blobType = (chunks[0] && chunks[0].type) || recorder.mimeType || mimeType || 'audio/webm';
                                const blob = new Blob(chunks, {{ type: blobType }});
                                setRecordingAudio(false);
                                stopAudioStream();
                                window[audioRecorderKey] = null;
                                if (!blob.size) {{
                                    renderAttachmentMeta();
                                    syncSendButtonState();
                                    return;
                                }}
                                const reader = new FileReader();
                                reader.onload = (event) => {{
                                    setRecordedAudio({{
                                        name: `voice-note.${{extensionFromMime(blobType)}}`,
                                        type: blobType,
                                        size: blob.size,
                                        content: event.target?.result || '',
                                        sample_rate: preferredAudioSampleRate || null,
                                    }});
                                    renderAttachmentMeta();
                                    syncSendButtonState();
                                }};
                                reader.onerror = () => {{
                                    setAudioError('Failed to read the recorded audio.');
                                    renderAttachmentMeta();
                                    syncSendButtonState();
                                }};
                                reader.readAsDataURL(blob);
                            }};
                            setRecordingAudio(true);
                            renderAttachmentMeta();
                            syncSendButtonState();
                            recorder.start();
                        }} catch (_error) {{
                            setAudioError('Microphone permission was denied or unavailable.');
                            setRecordingAudio(false);
                            stopAudioStream();
                            renderAttachmentMeta();
                            syncSendButtonState();
                        }}
                    }};

                    window.submitChatInput_{cid} = function() {{
                        syncPendingPhase();
                        if (isInputHardDisabled() || isStopping() || isRecordingAudio()) return;
                        const viewport = {{ x: window.scrollX, y: window.scrollY }};
                        const rawValue = el.value || '';
                        const trimmed = rawValue.trim();
                        const files = fileUploadEnabled ? getSelectedFiles() : [];
                        const audio = audioCaptureEnabled ? getRecordedAudio() : null;
                        const hasAttachments = files.length > 0 || !!audio;
                        if (!trimmed && !hasAttachments) {{
                            if (document.activeElement && typeof document.activeElement.blur === 'function') {{
                                document.activeElement.blur();
                            }}
                            preserveViewport(viewport);
                            return;
                        }}
                        const pending = isPending();
                        if (pending && autoDisableWhilePending) return;
                        if (pending && submitPolicy === 'drop') {{
                            window[draftKey] = '';
                            el.value = '';
                            clearAttachmentState();
                            autoResize();
                            syncSendButtonState();
                            return;
                        }}
                        window.lastActiveChatInput = 'input_{cid}';
                        if (!pending) {{
                            setPendingPhase('submitted');
                            window[pendingSeenChatKey] = false;
                        }}
                        if (typeof window._vlAllowNextFocusedUpdate === 'function') {{
                            window._vlAllowNextFocusedUpdate('{cid}');
                        }}
                        const payload = (fileUploadEnabled || audioCaptureEnabled)
                            ? {{ text: trimmed, files: files, audio: audio, audio_sample_rate: preferredAudioSampleRate }}
                            : trimmed;
                        {f"window.sendAction('{cid}', payload);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: JSON.stringify(payload), _csrf_token: window._csrf_token || '', _vl_lite_stream_dirty: 'true'}}, swap: 'none'}});"}
                        window[draftKey] = '';
                        el.value = '';
                        clearAttachmentState();
                        autoResize();
                        syncSendButtonState();
                        scheduleScrollToLatest();
                    }};

                    window.stopChatInput_{cid} = function() {{
                        if (!{'true' if show_stop_button else 'false'} || !isPending()) return;
                        setPendingPhase('stopping');
                        if (typeof window._vlAllowNextFocusedUpdate === 'function') {{
                            window._vlAllowNextFocusedUpdate('{cid}');
                        }}
                        {f"window.sendAction('{stop_cid}', 'stop');" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{stop_cid}', {{values: {{value: 'stop', _csrf_token: window._csrf_token || '', _vl_lite_stream_dirty: 'true'}}, swap: 'none'}});"}
                        syncSendButtonState();
                    }};

                    if (!el.dataset.chatReady) {{
                        el.dataset.chatReady = 'true';
                        el.addEventListener('input', () => {{
                            window.syncChatInput_{cid}();
                        }});
                        el.addEventListener('keydown', function(event) {{
                            if ({submit_on_enter_js} && event.key === 'Enter' && !event.shiftKey) {{
                                event.preventDefault();
                                window.submitChatInput_{cid}();
                            }}
                        }});
                    }}

                    if (attachButton && fileInput && !attachButton.dataset.chatReady) {{
                        attachButton.dataset.chatReady = 'true';
                        attachButton.dataset.chatInteractive = 'true';
                        attachButton.addEventListener('click', () => {{
                            if (attachButton.disabled) return;
                            fileInput.click();
                        }});
                        fileInput.addEventListener('change', async (event) => {{
                            const selected = Array.from(event.target.files || []);
                            await processSelectedFiles(selected);
                        }});
                    }}

                    if (surface && fileUploadEnabled && !surface.dataset.chatDropReady) {{
                        surface.dataset.chatDropReady = 'true';
                        surface.addEventListener('dragenter', (event) => {{
                            if (!isFileDragEvent(event)) return;
                            event.preventDefault();
                            window[dropDepthKey] = Number(window[dropDepthKey] || 0) + 1;
                            if (!isInputHardDisabled() && !isPending() && !isStopping() && !isRecordingAudio()) {{
                                setDropActive(true);
                            }}
                        }});
                        surface.addEventListener('dragover', (event) => {{
                            if (!isFileDragEvent(event)) return;
                            event.preventDefault();
                            if (event.dataTransfer) {{
                                event.dataTransfer.dropEffect = 'copy';
                            }}
                            if (!isInputHardDisabled() && !isPending() && !isStopping() && !isRecordingAudio()) {{
                                setDropActive(true);
                            }}
                        }});
                        surface.addEventListener('dragleave', (event) => {{
                            if (!isFileDragEvent(event)) return;
                            event.preventDefault();
                            window[dropDepthKey] = Math.max(Number(window[dropDepthKey] || 1) - 1, 0);
                            if (window[dropDepthKey] === 0) {{
                                setDropActive(false);
                            }}
                        }});
                        surface.addEventListener('drop', async (event) => {{
                            if (!isFileDragEvent(event)) return;
                            event.preventDefault();
                            window[dropDepthKey] = 0;
                            setDropActive(false);
                            if (isInputHardDisabled() || isPending() || isStopping() || isRecordingAudio()) return;
                            const selected = Array.from(event.dataTransfer?.files || []);
                            if (!selected.length) return;
                            await processSelectedFiles(selected);
                        }});
                    }}

                    if (audioButton && !audioButton.dataset.chatReady) {{
                        audioButton.dataset.chatReady = 'true';
                        audioButton.dataset.chatInteractive = 'true';
                        audioButton.addEventListener('click', () => {{
                            startAudioRecording();
                        }});
                    }}

                    if (surface && !surface.dataset.chatFocusReady) {{
                        surface.dataset.chatFocusReady = 'true';
                        surface.addEventListener('click', (event) => {{
                            if (isInputHardDisabled() || isStopping()) return;
                            if (isInteractiveChatTarget(event.target)) return;
                            focusInput();
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

                    const noteChatMutationDuringPending = () => {{
                        if (getPendingPhase() !== 'submitted') return;
                        if (!isServerPending() && !hasRunningAssistantMessage() && !hasCompletedAssistantAfterLatestUser()) return;
                        window[pendingSeenChatKey] = true;
                        if (!isServerPending()) {{
                            setPendingPhase('server');
                        }}
                    }};

                    window.__violitChatObserver_{cid} = new MutationObserver((mutationList) => {{
                        if (scrollMode !== 'bottom') return;
                        for (const mutation of mutationList) {{
                            if ((mutation.type === 'childList' || mutation.type === 'characterData') && mutationTouchesChat(mutation)) {{
                                noteChatMutationDuringPending();
                                syncSendButtonState();
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

                    restoreDraftState();
                    setDropActive(false);
                    renderAttachmentMeta();
                    window.syncChatInput_{cid}();

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
        val = _parse_chat_submit_value(val)
        
        # To prevent stale values on subsequent non-related runs (e.g. other buttons),
        # we ideally need to know 'who' triggered the run.
        # But for now, returning what's in store is the best approximation.
        # If another button is clicked, `store['actions']` might still have this cid's old value 
        # if we don't clear it. 
        # However, `store['actions']` is persistent in the current `app.py` logic?
        # Let's check app.py action handler. 
        
        return val
