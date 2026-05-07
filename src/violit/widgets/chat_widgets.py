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
        Insert a chat message container.
        
        Streamlit-compatible chat message container.
        """
        cid = self._get_next_cid("chat_message")
        
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
                        bubble_bg = "linear-gradient(180deg, color-mix(in srgb, var(--vl-text-muted) 10%, var(--vl-bg-card) 90%) 0%, color-mix(in srgb, var(--vl-primary) 8%, var(--vl-bg-card) 92%) 100%)"
                        bubble_border = "1px solid color-mix(in srgb, var(--vl-primary) 18%, var(--vl-border) 82%)"
                        bubble_shadow = "0 14px 30px color-mix(in srgb, var(--vl-primary) 10%, transparent)"

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
            border-radius: var(--vl-chat-thread-radius, 24px) !important;
            padding: var(--vl-chat-thread-padding, 0.25rem 0.35rem 0.5rem);
            background: linear-gradient(180deg, color-mix(in srgb, var(--vl-bg-card) 90%, var(--vl-bg) 10%), color-mix(in srgb, var(--vl-bg-card) 82%, var(--vl-bg) 18%)) !important;
            border: 1px solid color-mix(in srgb, var(--vl-border) 88%, var(--vl-primary) 12%) !important;
            box-shadow: var(--vl-chat-thread-shadow, inset 0 1px 0 color-mix(in srgb, white 24%, transparent), 0 18px 40px color-mix(in srgb, var(--vl-border) 10%, transparent)) !important;
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
                    has_text_output = bool(_coerce_chat_text(content).strip())

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

                if not has_text_output and not has_visible_agent_meta and role == "assistant":
                    continue

                with self.chat_message(
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
                    elif isinstance(item, dict) and error_value:
                        pass
                    elif isinstance(item, dict) and has_visible_agent_meta:
                        pass
                    else:
                        self.caption(thinking_label)

    def agent_messages(
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
        """Alias for chat_messages for discoverability in agent-focused apps."""
        return self.chat_messages(
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
                result = on_submit(*callback_args, val, **callback_kwargs)

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
                for raw_chunk in candidate:
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
            <div class="chat-input-container vl-chat-input-container{(' ' + html_lib.escape(cls, quote=True)) if cls else ''}" data-chat-pinned="{'true' if effective_pinned else 'false'}" data-chat-part="input-container" style="
                {container_style}
            ">
                <div class="vl-chat-input-root" data-chat-input-root="{cid}" data-chat-part="input-root" style="
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
                        <textarea id="input_{cid}" class="chat-input-box vl-chat-input-box" data-chat-part="input-textarea" placeholder={placeholder_js}
                            rows="1"
                            {"maxlength=" + '"' + str(max_chars) + '"' if max_chars else ""}
                            {"disabled" if disabled else ""}
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
                    </div>
                    <wa-button id="send_{cid}" type="button" size="small" variant="brand" appearance="accent" {"disabled" if disabled else ""} style="flex: 0 0 var(--vl-chat-input-button-size, 48px); min-width: var(--vl-chat-input-button-size, 48px); width: var(--vl-chat-input-button-size, 48px); height: var(--vl-chat-input-button-size, 48px); margin-bottom: 2px; --wa-button-padding-inline: 0;" onclick="
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
                        {f"window.sendAction('{cid}', trimmed);" if self.mode == 'ws' else f"htmx.ajax('POST', '/action/{cid}', {{values: {{value: trimmed, _csrf_token: window._csrf_token || '', _vl_lite_stream_dirty: 'true'}}, swap: 'none'}});"}
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
