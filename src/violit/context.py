import contextvars
from typing import Any, Optional

# Global Contexts
session_ctx: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("session_id", default=None)
view_ctx: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("view_id", default=None)
rendering_ctx: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("rendering_component", default=None)
fragment_ctx: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("current_fragment", default=None)
page_ctx: contextvars.ContextVar[Optional[Any]] = contextvars.ContextVar("current_page_renderer", default=None)
layout_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("layout_ctx", default="main")  # "main" or "sidebar"
action_ctx: contextvars.ContextVar[bool] = contextvars.ContextVar("action_ctx", default=False)
initial_render_ctx: contextvars.ContextVar[bool] = contextvars.ContextVar("initial_render", default=False) # for large-scale data rendering
pending_shared_views_ctx: contextvars.ContextVar[Optional[set[tuple[str, str]]]] = contextvars.ContextVar("pending_shared_views", default=None)

# Global Reference for App Instance (used for initial theme sync)
app_instance_ref: list[Any | None] = [None]
